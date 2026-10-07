<?php

use App\Enums\XpReason;
use App\Livewire\Admin\Students\Tree;
use App\Livewire\Student\NodeView;
use App\Models\CoinTransaction;
use App\Models\Course;
use App\Models\Currency;
use App\Models\Node;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\NodeUnlock;
use App\Models\Submission;
use App\Models\User;
use App\Models\XpTransaction;
use App\Services\CourseImporter;
use App\Services\PracticeSubmitter;
use App\Services\StepCompleter;
use App\Services\TreeAccess;
use Livewire\Livewire;

/*
 * Micro-misiones (D84 § 3): pasos cortos del nodo que se comprueban solos (salida esperada) y solo dan
 * premios de juego. Se escriben en el .md del curso («### Micro-misión R00-N01-P1 · …») y se importan.
 */

const STEPS_MD = <<<'MD'
### Micro-misión R00-N01-P1 · El pergamino habla

```meta
lugar: La orilla del río
personajes: Mia, Gheco, Ofidia
carta: print | print("texto")
recompensa: xp 10, oro 5
```

#### Escena
Despertás con un pergamino en blanco, {heroe}.

#### Gheco sugiere
`print("...")` muestra texto.

#### Desafío
Hacé que el pergamino diga *Hola, Valle*.

#### Código inicial
```python
# tu conjuro
```

#### Salida esperada
```
Hola, Valle
```

#### Solución
```python
print("Hola, Valle")
```

#### Al superarla
Las letras brillan en verde.

#### Imagen
- Mia en la orilla del río.

### Micro-misión R00-N01-P2 · Dos líneas

```meta
recompensa: xp 15
```

#### Desafío
Dos líneas.

#### Salida esperada
```
uno
dos
```

#### Solución
```python
print("uno")
print("dos")
```


MD;

function stepsCourseFile(callable $edit): array
{
    return [['name' => 'curso.md', 'content' => $edit(file_get_contents(base_path('tests/Fixtures/curso-ejemplo.md')))]];
}

function coursesWithSteps(): Course
{
    $report = app(CourseImporter::class)->import(stepsCourseFile(fn ($md) => str_replace('### Misión R00-N01-M1', STEPS_MD.'### Misión R00-N01-M1', $md)), dryRun: false);
    expect($report->errors)->toBe([]);
    $course = Course::where('slug', 'python-import')->firstOrFail();
    $course->update(['is_published' => true]);

    return $course;
}

test('el importador lee las micro-misiones del nodo con sus partes', function () {
    $course = coursesWithSteps();
    $root = Node::where('course_id', $course->id)->where('code', 'R00-N01')->firstOrFail();
    $steps = $root->steps()->get();

    expect($steps)->toHaveCount(2)
        ->and($steps[0]->code)->toBe('R00-N01-P1')
        ->and($steps[0]->title)->toBe('El pergamino habla')
        ->and($steps[0]->place)->toBe('La orilla del río')
        ->and($steps[0]->card_title)->toBe('print')
        ->and($steps[0]->card_body)->toBe('print("texto")')
        ->and($steps[0]->xp_reward)->toBe(10)
        ->and($steps[0]->gold_reward)->toBe(5)
        ->and($steps[0]->starter_code)->toBe('# tu conjuro')
        ->and($steps[0]->expected_output)->toBe('Hola, Valle')
        ->and($steps[0]->solution)->toBe('print("Hola, Valle")')
        ->and($steps[0]->success_text)->toBe('Las letras brillan en verde.')
        ->and($steps[1]->position)->toBe(2)
        ->and($root->practices()->count())->toBe(3);
});

test('reimportar actualiza por ID sin perder quién las superó, y borra las que ya no están', function () {
    $course = coursesWithSteps();
    $step = NodeStep::where('code', 'R00-N01-P1')->firstOrFail();
    $student = User::factory()->create();
    NodeStepCompletion::create(['user_id' => $student->id, 'node_step_id' => $step->id, 'completed_at' => now()]);

    $report = app(CourseImporter::class)->import(stepsCourseFile(fn ($md) => str_replace('### Misión R00-N01-M1',
        str_replace('El pergamino habla', 'El pergamino canta', strstr(STEPS_MD, '### Micro-misión R00-N01-P2', true)).'### Misión R00-N01-M1', $md)), dryRun: false);

    expect($report->errors)->toBe([])
        ->and($step->fresh()->title)->toBe('El pergamino canta')
        ->and(NodeStepCompletion::where('node_step_id', $step->id)->exists())->toBeTrue()
        ->and(NodeStep::where('code', 'R00-N01-P2')->exists())->toBeFalse();
});

test('una micro-misión sin salida esperada no se importa', function () {
    $report = app(CourseImporter::class)->import(stepsCourseFile(fn ($md) => str_replace('### Misión R00-N01-M1',
        "### Micro-misión R00-N01-P1 · Sin salida\n\n#### Desafío\nAlgo.\n\n### Misión R00-N01-M1", $md)), dryRun: true);

    expect($report->ok())->toBeFalse()
        ->and(implode(' ', $report->errors))->toContain('no tiene «Salida esperada»');
});

test('se supera con la salida correcta, en orden, y da la XP una sola vez', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    [$first, $second] = $course->rootNode->steps()->get()->all();
    $completer = app(StepCompleter::class);

    expect(fn () => $completer->complete($student, $second, "uno\ndos"))->toThrow(InvalidArgumentException::class, 'todavía no');
    expect(fn () => $completer->complete($student, $first, 'Hola valle'))->toThrow(InvalidArgumentException::class, 'no es la esperada');

    $xp = $student->fresh()->xp_total;
    expect($completer->complete($student, $first, "Hola, Valle  \n\n"))->toBeTrue()
        ->and($completer->complete($student, $first, 'Hola, Valle'))->toBeFalse()
        ->and($student->fresh()->xp_total)->toBe($xp + 10)
        ->and(XpTransaction::where('user_id', $student->id)->where('reason', XpReason::StepCompleted)->count())->toBe(1);

    expect($completer->complete($student, $second, "uno\r\ndos"))->toBeTrue();
});

test('no da monedas del curso ni abre nodos (solo oro, D89)', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $notGold = fn () => CoinTransaction::where('user_id', $student->id)->whereHas('currency', fn ($q) => $q->where('code', '!=', Currency::GOLD))->count();
    $coins = $notGold();
    $unlocks = NodeUnlock::where('user_id', $student->id)->count();

    $first = $course->rootNode->steps()->first();
    app(StepCompleter::class)->complete($student, $first, 'Hola, Valle');

    expect($notGold())->toBe($coins)
        ->and(NodeUnlock::where('user_id', $student->id)->count())->toBe($unlocks);
});

test('en la Clase 0 de prueba se juegan y quedan los premios; en un nodo cerrado no', function () {
    $course = coursesWithSteps();
    $visitor = User::factory()->create();
    $first = $course->rootNode->steps()->first();

    expect(app(StepCompleter::class)->complete($visitor, $first, 'Hola, Valle'))->toBeTrue();

    $closed = Node::where('course_id', $course->id)->where('code', 'R01-N01')->firstOrFail();
    $step = $closed->steps()->create(['code' => 'R01-N01-P1', 'title' => 'X', 'expected_output' => 'x', 'position' => 1]);
    expect(app(StepCompleter::class)->canPlay($visitor, $step))->toBeFalse();
});

test('el alumno ve la micro-misión actual, las siguientes bloqueadas y nunca la solución', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);

    $html = $this->actingAs($student)->get(route('student.node', [$course, $course->rootNode]))->assertOk()->getContent();
    expect($html)->toContain('data-test="node-steps"')
        ->and($html)->toContain('data-test="step-current"')
        ->and($html)->toContain('data-test="step-locked"')
        ->and($html)->toContain('El pergamino habla')
        ->and($html)->not->toContain('print("Hola, Valle")')
        ->and($html)->not->toContain('print("Hola, Valle")')
        ->and($html)->not->toContain('print(&quot;Hola, Valle&quot;)');
});

test('desde la página del nodo se supera, se queda en pantalla y «Siguiente» pasa a la otra', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $first = $course->rootNode->steps()->first();
    $first->update(['image_path' => 'practice-refs/escena.webp']);

    $component = Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode]);
    $component->call('completeStep', $first->id, 'Hola, Valle', 'print("Hola, Valle")')
        ->assertReturned(['ok' => true, 'xp' => 10])
        ->assertSee('data-test="step-success"', false);

    $component->call('completeStep', $first->id, 'otra cosa', 'print("otra cosa")')
        ->assertReturned(['ok' => false, 'error' => 'La salida no es la esperada.']);

    $component->call('$refresh')
        ->assertSee('data-test="step-done"', false)
        ->assertSee('data-test="step-my-code"', false)
        ->assertSee('data-test="step-done-image"', false)
        ->assertSee('print(&quot;Hola, Valle&quot;)', false)
        ->assertSee('Dos líneas');

    expect(NodeStepCompletion::where('user_id', $student->id)->count())->toBe(1);
});

test('un nodo sin micro-misiones se ve como siempre, con la teoría abierta', function () {
    $made = makeCourse();
    $student = studentWithRootOpen($made);

    $this->actingAs($student)->get(route('student.node', [$made['course'], $made['root']]))
        ->assertOk()
        ->assertDontSee('data-test="node-steps"', false);
});

test('el oro se muestra si existe (D89) y los ítems recién cuando exista el inventario', function () {
    $course = coursesWithSteps();
    NodeStep::where('code', 'R00-N01-P1')->update(['item' => 'Bolsa de cuero']);
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);

    config(['game.gold_enabled' => false, 'game.inventory_enabled' => false]);
    $this->actingAs($student)->get(route('student.node', [$course, $course->rootNode]))
        ->assertOk()
        ->assertDontSee('de oro')
        ->assertDontSee('Bolsa de cuero');

    config(['game.gold_enabled' => true]);
    $this->actingAs($student)->get(route('student.node', [$course, $course->rootNode]))
        ->assertSee('+5 de oro')
        ->assertDontSee('Bolsa de cuero');

    config(['game.inventory_enabled' => true]);
    $this->actingAs($student)->get(route('student.node', [$course, $course->rootNode]))
        ->assertSee('Bolsa de cuero');
});

/*
 * D95: en un nodo con micro-misiones, las prácticas, los recursos y la autoevaluación aparecen al superarlas.
 */

test('con micro-misiones pendientes no ve las prácticas ni la autoevaluación, y no puede entregar ni entrar al modo misión', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $practice = $course->rootNode->practices()->where('title', 'Tu primer programa')->firstOrFail();

    $html = $this->actingAs($student)->get(route('student.node', [$course, $course->rootNode]))->assertOk()->getContent();
    expect($html)->toContain('data-test="practices-locked"')
        ->and($html)->toContain('0 de 2')
        ->and($html)->not->toContain('data-test="practice-'.$practice->id.'"')
        ->and($html)->not->toContain('data-test="self-check"')
        ->and($html)->not->toContain('data-test="practice-progress"');

    $this->actingAs($student)->get(route('student.mission', [$course, $course->rootNode, $practice]))
        ->assertRedirect(route('student.node', [$course, $course->rootNode]));

    expect(app(PracticeSubmitter::class)->blocker($student, $practice))->toContain('micro-misiones')
        ->and(fn () => app(PracticeSubmitter::class)->submit($student, $practice, 'print(1)'))->toThrow(DomainException::class, 'micro-misiones');
});

test('al superar todas las micro-misiones aparecen las prácticas y puede entregar', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $practice = $course->rootNode->practices()->where('title', 'Tu primer programa')->firstOrFail();
    [$first, $second] = $course->rootNode->steps()->get()->all();
    app(StepCompleter::class)->complete($student, $first, 'Hola, Valle');
    app(StepCompleter::class)->complete($student, $second, "uno\ndos");

    $this->actingAs($student)->get(route('student.node', [$course, $course->rootNode]))->assertOk()
        ->assertDontSee('data-test="practices-locked"', false)
        ->assertSee('data-test="practice-'.$practice->id.'"', false)
        ->assertSee('data-test="self-check"', false);
    $this->actingAs($student)->get(route('student.mission', [$course, $course->rootNode, $practice]))->assertOk();
    expect(app(PracticeSubmitter::class)->blocker($student, $practice))->toBeNull();
});

test('quien ya entregó una práctica del nodo la sigue viendo; el staff y los nodos sin micro-misiones, siempre', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $access = app(TreeAccess::class);
    expect($access->practicesOpen($student, $course->rootNode))->toBeFalse();

    $practice = $course->rootNode->practices()->first();
    Submission::create(['practice_id' => $practice->id, 'user_id' => $student->id, 'attempt' => 1, 'submitted_at' => now()]);
    expect($access->practicesOpen($student, $course->rootNode))->toBeTrue()
        ->and($access->practicesOpen(User::factory()->admin()->create(), $course->rootNode))->toBeTrue();

    $made = makeCourse();
    expect($access->practicesOpen(studentWithRootOpen($made), $made['root']))->toBeTrue();
});

test('el docente le abre las prácticas desde el árbol del alumno y le llega el aviso', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $admin = User::factory()->admin()->create();

    Livewire::actingAs($admin)->test(Tree::class, ['user' => $student, 'course' => $course])
        ->assertSee('data-test="grant-practices-'.$course->rootNode->id.'"', false)
        ->call('grantPractices', $course->rootNode->id)
        ->assertDontSee('data-test="grant-practices-'.$course->rootNode->id.'"', false);

    expect(app(TreeAccess::class)->practicesOpen($student, $course->rootNode))->toBeTrue()
        ->and($student->notifications()->where('data->kind', 'practices_granted')->exists())->toBeTrue();

    // Otro alumno no puede abrírselas a nadie.
    $other = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    Livewire::actingAs($other)->test(Tree::class, ['user' => $student, 'course' => $course])->assertForbidden();
});
