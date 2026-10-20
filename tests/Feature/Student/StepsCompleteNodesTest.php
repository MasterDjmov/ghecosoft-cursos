<?php

use App\Enums\SubmissionStatus;
use App\Models\Course;
use App\Models\Currency;
use App\Models\Node;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\Practice;
use App\Models\Submission;
use App\Models\User;
use App\Services\CourseImporter;
use App\Services\Ledger;
use App\Services\NodeUnlocker;
use App\Services\StepCompleter;
use App\Services\SubmissionReviewer;
use App\Services\TreeAccess;

/** D111: un curso donde las micro-misiones completan el nodo y las que vienen de una misión pagan monedas. */
function stepFor(Node $node, string $code, int $coins = 0, int $position = 1): NodeStep
{
    return NodeStep::create(['node_id' => $node->id, 'code' => $code, 'position' => $position, 'title' => $code, 'expected_output' => 'ok', 'solution' => 'ok', 'xp_reward' => 10, 'coin_reward' => $coins]);
}

function approveFor(User $student, Practice $practice): void
{
    $submission = Submission::create(['practice_id' => $practice->id, 'user_id' => $student->id, 'attempt' => 1, 'submitted_at' => now()]);
    app(SubmissionReviewer::class)->approve($submission, User::factory()->admin()->create(), notify: false);
}

beforeEach(function () {
    $this->made = makeCourse();
    $this->course = $this->made['course'];
    $this->course->update(['steps_complete_nodes' => true]);
    // La Clase 0 pasó a micro-misiones: su misión se retiró.
    $this->made['root']->practices()->update(['retired_at' => now(), 'is_required' => false]);
    $this->rootStep = stepFor($this->made['root'], 'R00-N01-P1', coins: 10);
    $this->student = studentWithRootOpen($this->made);
    $this->coins = fn () => app(Ledger::class)->balance($this->student, Currency::forCourse($this->course));
});

test('superar las micro-misiones completa el nodo y paga las monedas para abrir el siguiente', function () {
    $access = app(TreeAccess::class);
    expect(($this->coins)())->toBe(0)
        ->and($access->isCompleted($this->student, $this->made['root']))->toBeFalse()
        ->and(Practice::where('node_id', $this->made['root']->id)->count())->toBe(0);

    app(StepCompleter::class)->complete($this->student, $this->rootStep, 'ok');

    expect(($this->coins)())->toBe(10)
        ->and($access->isCompleted($this->student, $this->made['root']))->toBeTrue();
    app(NodeUnlocker::class)->unlock($this->student, $this->made['topic1']);
    expect($access->isUnlocked($this->student, $this->made['topic1']))->toBeTrue();

    // Volver a superarla no paga de nuevo.
    app(StepCompleter::class)->complete($this->student, $this->rootStep, 'ok');
    expect(($this->coins)())->toBe(0);
});

test('un nodo con un proyecto necesita las micro-misiones y el proyecto aprobado', function () {
    app(StepCompleter::class)->complete($this->student, $this->rootStep, 'ok');
    app(NodeUnlocker::class)->unlock($this->student, $this->made['topic1']);
    $topic1 = $this->made['topic1'];
    $step = stepFor($topic1, 'R01-N01-P1', coins: 4);
    $access = app(TreeAccess::class);

    // Las dos misiones obligatorias del tema quedan como proyectos que corrige el docente.
    foreach ($topic1->practices()->where('is_required', true)->get() as $practice) {
        approveFor($this->student, $practice);
    }
    expect($access->isCompleted($this->student, $topic1))->toBeFalse();

    app(StepCompleter::class)->complete($this->student, $step, 'ok');
    expect($access->isCompleted($this->student, $topic1))->toBeTrue();
});

test('lo que ya estaba completo sigue completo aunque se le sumen micro-misiones', function () {
    app(StepCompleter::class)->complete($this->student, $this->rootStep, 'ok');
    stepFor($this->made['root'], 'R00-N01-P2', position: 2);

    expect(app(TreeAccess::class)->isCompleted($this->student, $this->made['root']))->toBeTrue();
});

test('sin el ajuste del curso, una micro-misión nunca paga monedas del curso', function () {
    $this->course->update(['steps_complete_nodes' => false]);

    app(StepCompleter::class)->complete($this->student, $this->rootStep, 'ok');

    expect(($this->coins)())->toBe(0);
});

test('el importador retira las misiones con entregas, borra las demás y da por superada la micro-misión a quien la tenía aprobada', function () {
    $file = fn (callable $edit) => [['name' => 'curso.md', 'content' => $edit(file_get_contents(base_path('tests/Fixtures/curso-ejemplo.md')))]];
    expect(app(CourseImporter::class)->import($file(fn ($md) => $md), dryRun: false)->errors)->toBe([]);
    $course = Course::where('slug', 'python-import')->firstOrFail();
    $root = Node::where('course_id', $course->id)->where('code', 'R00-N01')->firstOrFail();
    $student = User::factory()->create();
    $submission = Submission::create(['practice_id' => $root->practices()->where('code', 'R00-N01-M2')->value('id'), 'user_id' => $student->id, 'attempt' => 1, 'submitted_at' => now()]);
    $submission->forceFill(['status' => SubmissionStatus::Approved, 'reviewed_at' => now(), 'code' => 'print("Kira")'])->save();

    $step = <<<'MD'
### Micro-misión R00-N01-P1 · Tu primer programa

```meta
recompensa: xp 10, monedas 10
antes: R00-N01-M2
```

#### Desafío
Mostrá tu nombre y tu ciudad.

#### Salida esperada
```
Kira
La Rioja
```

#### Solución
```python
print("Kira")
print("La Rioja")
```


MD;
    $report = app(CourseImporter::class)->import($file(fn ($md) => preg_replace(
        '/### Misión R00-N01-M1.*?(?=### Encargo R00-N01-E1)/s',
        $step,
        str_replace('publicado: no', "publicado: no\nmicromisiones_completan: si", $md),
    )), dryRun: false);

    expect($report->errors)->toBe([])
        ->and($course->fresh()->steps_complete_nodes)->toBeTrue();
    $retired = Practice::withoutGlobalScope(Practice::ACTIVE)->where('node_id', $root->id)->where('code', 'R00-N01-M2')->firstOrFail();
    expect($retired->retired_at)->not->toBeNull()
        ->and($retired->is_required)->toBeFalse()
        ->and(Practice::withoutGlobalScope(Practice::ACTIVE)->where('node_id', $root->id)->where('code', 'R00-N01-M1')->exists())->toBeFalse()
        ->and($root->practices()->pluck('code')->all())->toBe(['R00-N01-E1'])
        ->and($submission->fresh()->practice->code)->toBe('R00-N01-M2');

    $newStep = NodeStep::where('node_id', $root->id)->where('code', 'R00-N01-P1')->firstOrFail();
    expect($newStep->coin_reward)->toBe(10)
        ->and(NodeStepCompletion::where('user_id', $student->id)->where('node_step_id', $newStep->id)->value('code'))->toBe('print("Kira")');
});
