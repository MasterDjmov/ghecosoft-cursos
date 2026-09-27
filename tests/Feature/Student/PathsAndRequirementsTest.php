<?php

use App\Enums\BranchKind;
use App\Enums\CoinReason;
use App\Enums\NodeType;
use App\Exceptions\TreeEditRefused;
use App\Livewire\Admin\Nodes\Edit;
use App\Models\Branch;
use App\Models\Currency;
use App\Models\Node;
use App\Models\User;
use App\Services\CourseImporter;
use App\Services\Ledger;
use App\Services\NodeUnlocker;
use App\Services\TreeAccess;
use App\Services\TreeEditor;
use App\Support\TreeGraph;
use App\Support\UnlockMessages;
use Livewire\Livewire;

/** Fase 8: requisitos extra, Sendas y nodos Ventana. */
function courseWithPath(): array
{
    $data = makeCourse();
    ['course' => $course, 'root' => $root, 'topic1' => $topic1, 'topic2' => $topic2] = $data;

    $path = Branch::create(['course_id' => $course->id, 'title' => 'Senda Web', 'kind' => BranchKind::Path]);
    $window = Node::create(['course_id' => $course->id, 'parent_id' => $root->id, 'type' => NodeType::Window, 'title' => 'Ventana web', 'price' => 0]);
    $entry = Node::create([
        'course_id' => $course->id, 'branch_id' => $path->id, 'parent_id' => $window->id, 'type' => NodeType::Topic,
        'title' => 'HTML', 'price' => 3, 'price_currency_id' => Currency::wildcard()->id,
    ]);
    $inner = Node::create(['course_id' => $course->id, 'branch_id' => $path->id, 'parent_id' => $entry->id, 'type' => NodeType::Topic, 'title' => 'Plantillas', 'price' => 0]);
    $inner->requirements()->attach($topic2->id);

    return [...$data, 'path' => $path, 'window' => $window, 'entry' => $entry, 'inner' => $inner];
}

/** Alumno inscripto con saldo de sobra en las dos monedas. */
function studentWithFunds(array $data): User
{
    $student = enrolledStudent($data['course']);
    $ledger = app(Ledger::class);
    $ledger->credit($student, Currency::forCourse($data['course']), 100, CoinReason::ManualAdjustment, note: 'test');
    $ledger->credit($student, Currency::wildcard(), 100, CoinReason::ManualAdjustment, note: 'test');

    return $student;
}

test('un requisito extra sin completar bloquea el nodo, con una frase clara', function () {
    $data = courseWithPath();
    $student = studentWithFunds($data);
    $unlocker = app(NodeUnlocker::class);
    $access = app(TreeAccess::class);

    foreach (['root', 'window', 'entry'] as $key) {
        $unlocker->unlock($student, $data[$key]);
        approveRequiredPractices($student, $data[$key]);
    }

    expect($access->unlockBlockers($student, $data['inner']))->toContain(TreeAccess::BLOCK_REQUIREMENTS_INCOMPLETE)
        ->and(implode(' ', UnlockMessages::for($student, $data['inner'])))->toContain('Aprobá también')->toContain('«Tema 2»');

    // Completa el requisito: Tema 1 → Tema 2.
    foreach (['topic1', 'topic2'] as $key) {
        $unlocker->unlock($student, $data[$key]);
        approveRequiredPractices($student, $data[$key]);
    }

    expect($access->unlockBlockers($student, $data['inner']->fresh()))->toBe([]);
});

test('la entrada a una Senda se paga con comodines', function () {
    $data = courseWithPath();
    $student = studentWithFunds($data);
    $unlocker = app(NodeUnlocker::class);
    $ledger = app(Ledger::class);

    foreach (['root', 'window'] as $key) {
        $unlocker->unlock($student, $data[$key]);
        approveRequiredPractices($student, $data[$key]);
    }
    $before = $ledger->balance($student, Currency::wildcard());
    $unlocker->unlock($student, $data['entry']);

    expect($ledger->balance($student, Currency::wildcard()))->toBe($before - 3);
});

test('las Sendas no cuentan para completar el curso; las Ventanas sí', function () {
    $data = courseWithPath();
    $student = studentWithFunds($data);
    $unlocker = app(NodeUnlocker::class);
    $access = app(TreeAccess::class);

    foreach (['root', 'topic1', 'topic2'] as $key) {
        $unlocker->unlock($student, $data[$key]);
        approveRequiredPractices($student, $data[$key]);
    }
    expect($access->isCourseCompleted($student, $data['course']))->toBeFalse(); // falta la Ventana

    $unlocker->unlock($student, $data['window']);
    approveRequiredPractices($student, $data['window']);
    expect($access->isCourseCompleted($student, $data['course']))->toBeTrue(); // la Senda no hace falta
});

test('no se puede poner como requisito un nodo que depende del mismo (ciclo)', function () {
    $data = courseWithPath();

    // Tema 2 no puede pedir "Plantillas", porque Plantillas ya pide Tema 2.
    expect(fn () => app(TreeEditor::class)->setRequirements($data['topic2'], [$data['inner']->id]))
        ->toThrow(TreeEditRefused::class);
    // Tampoco a sí mismo.
    expect(fn () => app(TreeEditor::class)->setRequirements($data['inner'], [$data['inner']->id]))
        ->toThrow(TreeEditRefused::class);
});

test('el editor del nodo guarda los requisitos extra y la moneda de cualquier nodo', function () {
    $data = courseWithPath();
    $this->actingAs(User::factory()->admin()->create());

    Livewire::test(Edit::class, ['course' => $data['course'], 'node' => $data['topic2']])
        ->set('requirementIds', [(string) $data['window']->id])
        ->set('paidWith', 'wildcard')
        ->call('save')
        ->assertHasNoErrors();

    $topic2 = $data['topic2']->fresh();
    expect($topic2->requirements()->pluck('nodes.id')->all())->toBe([$data['window']->id])
        ->and($topic2->price_currency_id)->toBe(Currency::wildcard()->id);
});

test('el árbol del alumno trae el tipo de rama y los requisitos extra', function () {
    $data = courseWithPath();
    $student = studentWithFunds($data);
    app(NodeUnlocker::class)->unlock($student, $data['root']);

    $graph = TreeGraph::forStudent($data['course'], $student);

    expect(collect($graph['branches'])->firstWhere('id', $data['path']->id)['kind'])->toBe('path')
        ->and(collect($graph['nodes'])->firstWhere('id', $data['inner']->id)['requires'])->toBe([$data['topic2']->id])
        ->and(collect($graph['nodes'])->firstWhere('id', $data['window']->id)['type'])->toBe('window');
});

test('el importador guarda Sendas, Ventanas y requisitos, y frena los ciclos', function () {
    $senda = <<<'MD'

# RAMA R02 · Ventanas

## R02-N01 · Ventana: tu primera web

```meta
tipo: ventana
padre: R01-N01
```

# RAMA S01 · Senda Web

```meta
tipo: senda
```

## S01-N01 · HTML con Python

```meta
padre: R02-N01
precio: 3
moneda: comodin
```

## S01-N02 · Plantillas

```meta
padre: S01-N01
requiere: R01-N02
```
MD;
    $file = fn (string $extra) => [['name' => 'curso.md', 'content' => file_get_contents(base_path('tests/Fixtures/curso-ejemplo.md')).$extra]];

    $report = app(CourseImporter::class)->import($file($senda), dryRun: false);
    expect($report->errors)->toBe([]);

    $templates = Node::where('code', 'S01-N02')->firstOrFail();
    expect($templates->branch->kind)->toBe(BranchKind::Path)
        ->and(Node::where('code', 'R02-N01')->value('type'))->toBe(NodeType::Window)
        ->and(Node::where('code', 'S01-N01')->firstOrFail()->priceCurrency->is_wildcard)->toBeTrue()
        ->and($templates->requirements()->pluck('code')->all())->toBe(['R01-N02']);

    // El jefe R01-N02 no puede pedir Plantillas: Plantillas ya lo pide a él.
    $cycle = str_replace("padre: R01-N01\nprecio: 10\ninsignia:", "padre: R01-N01\nrequiere: S01-N02\nprecio: 10\ninsignia:", file_get_contents(base_path('tests/Fixtures/curso-ejemplo.md')));
    $bad = app(CourseImporter::class)->import([['name' => 'curso.md', 'content' => $cycle.$senda]], dryRun: false);
    expect(collect($bad->errors)->implode(' '))->toContain('ciclo')
        ->and(Node::where('code', 'R01-N02')->firstOrFail()->requirements()->count())->toBe(0);
});

test('el árbol del alumno cuenta el camino principal y muestra cada Senda aparte', function () {
    $data = courseWithPath();
    $student = studentWithFunds($data);
    app(NodeUnlocker::class)->unlock($student, $data['root']);
    approveRequiredPractices($student, $data['root']);

    // Tronco: raíz, Tema 1, Tema 2 y la Ventana (4). La Senda (2 nodos) va aparte.
    $this->actingAs($student)->get(route('student.tree', $data['course']))
        ->assertOk()
        ->assertSeeInOrder(['1/4', 'del camino principal'])
        ->assertSee('Senda Web · 0/2')
        ->assertSee('Nombres en el árbol');
});
