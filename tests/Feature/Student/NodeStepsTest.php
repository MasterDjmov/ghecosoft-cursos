<?php

use App\Enums\Language;
use App\Enums\XpReason;
use App\Livewire\Admin\Students\Show;
use App\Livewire\Admin\Students\Tree;
use App\Livewire\Settings\Profile;
use App\Livewire\Student\NodeView;
use App\Models\CoinTransaction;
use App\Models\Course;
use App\Models\Currency;
use App\Models\Node;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\NodeUnlock;
use App\Models\NodeVisit;
use App\Models\StepAttempt;
use App\Models\StepHelp;
use App\Models\Submission;
use App\Models\User;
use App\Models\XpTransaction;
use App\Services\ActivityLog;
use App\Services\CourseImporter;
use App\Services\PracticeSubmitter;
use App\Services\StepCompleter;
use App\Services\StepHelper;
use App\Services\TreeAccess;
use App\Support\LineDiff;
use App\Support\StudentJourney;
use Illuminate\Contracts\Auth\Access\Gate;
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
        // Si la salida no coincide, la consola la muestra renglón por renglón con ✓ y ✗.
        ->and($html)->toContain('data-test="output-lines"')
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
        ->assertReturned(['ok' => true, 'xp' => 10, 'gold' => 5, 'halved' => false])
        ->assertSee('data-test="step-success"', false);

    $component->call('completeStep', $first->id, 'otra cosa', 'print("otra cosa")')
        ->assertReturned(['ok' => false, 'error' => 'La salida no es la esperada.']);

    $component->call('$refresh')
        ->assertSee('data-test="step-done"', false)
        ->assertSee('data-test="step-my-code"', false)
        ->assertSee('data-test="step-done-image"', false)
        ->assertSee('data-test="step-zoom"', false)
        ->assertSee('data-test="image-lightbox"', false)
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

/*
 * Una micro-misión en otro lenguaje que su curso (SQL en Java): el bloque del código inicial dice el lenguaje y la
 * página la ejecuta con ese (SQLite en el navegador), sin el «pegá la salida» de Java.
 */

test('el bloque del código inicial marca una micro-misión de otro lenguaje que el curso', function () {
    $sqlStep = str_replace(["```python\n# tu conjuro\n```", "#### Solución\n```python\nprint(\"Hola, Valle\")\n```"],
        ["```sql\nSELECT ___;\n```", "#### Solución\n```sql\nSELECT 'Hola, Valle' AS saludo;\n```"], STEPS_MD);
    $report = app(CourseImporter::class)->import(stepsCourseFile(fn ($md) => str_replace('### Misión R00-N01-M1', $sqlStep.'### Misión R00-N01-M1', $md)), dryRun: false);
    expect($report->errors)->toBe([]);
    $course = Course::where('slug', 'python-import')->firstOrFail();
    $course->update(['is_published' => true]);
    [$first, $second] = $course->rootNode->steps()->get()->all();

    expect($first->language)->toBe('sql')
        ->and($first->runLanguage($course))->toBe(Language::Sql)
        ->and($second->language)->toBeNull()
        ->and($second->runLanguage($course))->toBe($course->language)
        ->and(Language::Sql->studentCanRun())->toBeTrue();

    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $html = $this->actingAs($student)->get(route('student.node', [$course, $course->rootNode]))->assertOk()->getContent();
    expect($html)->toContain('r00-n01-p1.sql')
        ->and($html)->not->toContain('data-test="step-paste"');
});

/*
 * C para el alumno (D98): la micro-misión se ejecuta con Clang en su navegador, y si el compilador no carga, la puede
 * compilar en su compu y pegar la salida.
 */

test('una micro-misión de C se ejecuta en el navegador del alumno y ofrece pegar la salida', function () {
    $cStep = str_replace(["```python\n# tu conjuro\n```", "#### Solución\n```python\nprint(\"Hola, Valle\")\n```"],
        ["```c\n#include <stdio.h>\nint main(void) { ___ }\n```", "#### Solución\n```c\n#include <stdio.h>\nint main(void) { printf(\"Hola, Valle\\n\"); return 0; }\n```"], STEPS_MD);
    $report = app(CourseImporter::class)->import(stepsCourseFile(fn ($md) => str_replace('### Misión R00-N01-M1', $cStep.'### Misión R00-N01-M1', $md)), dryRun: false);
    expect($report->errors)->toBe([]);
    $course = Course::where('slug', 'python-import')->firstOrFail();
    $course->update(['is_published' => true]);
    $first = $course->rootNode->steps()->first();

    expect($first->runLanguage($course))->toBe(Language::C);

    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $html = $this->actingAs($student)->get(route('student.node', [$course, $course->rootNode]))->assertOk()->getContent();
    expect($html)->toContain('r00-n01-p1.c')
        ->and($html)->toContain('data-test="step-paste"')
        ->and($html)->toContain('¿No carga el compilador?')
        ->and($html)->toContain('runnable\\u0022:true');
});

/*
 * HTML y CSS (D102): la micro-misión trae qué revisa el inspector, que lee el código sin ejecutarlo; su informe es
 * la salida esperada y el servidor lo compara igual que una salida.
 */

function htmlStepsMd(bool $withInspector = true): string
{
    $step = str_replace(
        ["```python\n# tu conjuro\n```", "#### Salida esperada\n```\nHola, Valle\n```", "#### Solución\n```python\nprint(\"Hola, Valle\")\n```"],
        ["```html\n<h1>___</h1>\n```", ($withInspector ? "#### Inspector\n```\nh1\nimg @alt\n```\n\n" : '')."#### Salida esperada\n```\nh1: Hola, Valle\nimg @alt: El río\n```",
            "#### Solución\n```html\n<h1>Hola, Valle</h1><img src=\"rio.webp\" alt=\"El río\">\n```"],
        STEPS_MD);

    return str_replace(["#### Salida esperada\n```\nuno\ndos\n```", "```python\nprint(\"uno\")\nprint(\"dos\")"],
        ["#### Inspector\n```\np\n```\n\n#### Salida esperada\n```\np: uno\np: dos\n```", "```html\n<p>uno</p><p>dos</p>"], $step);
}

test('una micro-misión de HTML guarda lo que revisa el inspector, y sin inspector no se importa', function () {
    $html = fn (bool $inspector) => stepsCourseFile(fn ($md) => str_replace(['lenguaje: python', '### Misión R00-N01-M1'],
        ['lenguaje: html', htmlStepsMd($inspector).'### Misión R00-N01-M1'], $md));

    $report = app(CourseImporter::class)->import($html(false), dryRun: true);
    expect(collect($report->errors)->implode(' '))->toContain('no tiene «Inspector»');

    $report = app(CourseImporter::class)->import($html(true), dryRun: false);
    expect(collect($report->errors)->filter(fn ($e) => str_contains($e, 'R00-N01-P1'))->all())->toBe([]);
    $step = NodeStep::where('code', 'R00-N01-P1')->firstOrFail();

    expect($step->checks)->toBe("h1\nimg @alt")
        ->and($step->expected_output)->toBe("h1: Hola, Valle\nimg @alt: El río")
        ->and($step->accepts("h1: Hola, Valle\r\nimg @alt: El río\n"))->toBeTrue()
        ->and($step->accepts("h1: Hola, Valle\nimg @alt: (no tiene)"))->toBeFalse();
});

test('el alumno ve el inspector en la micro-misión de HTML y nunca la solución', function () {
    $report = app(CourseImporter::class)->import(stepsCourseFile(fn ($md) => str_replace(['lenguaje: python', '### Misión R00-N01-M1'],
        ['lenguaje: html', htmlStepsMd().'### Misión R00-N01-M1'], $md)), dryRun: false);
    $course = Course::where('slug', 'python-import')->firstOrFail();
    $course->update(['is_published' => true]);

    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $page = $this->actingAs($student)->get(route('student.node', [$course, $course->rootNode]))->assertOk()->getContent();

    expect($page)->toContain('data-test="html-inspector"')
        ->and($page)->toContain('Lo que tiene que encontrar el inspector')
        ->and($page)->not->toContain('rio.webp');
});

/* D107: intentos y visitas para las estadísticas del docente. */

test('abrir el nodo anota una visita por día; el staff y la Clase 0 de prueba no dejan registro', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $node = ['course' => $course, 'node' => $course->rootNode];

    Livewire::actingAs($student)->test(NodeView::class, $node);
    Livewire::actingAs($student)->test(NodeView::class, $node);
    $this->travel(1)->days();
    Livewire::actingAs($student)->test(NodeView::class, $node);

    expect(NodeVisit::where('user_id', $student->id)->count())->toBe(2)
        ->and((int) NodeVisit::where('user_id', $student->id)->sum('views'))->toBe(3);

    Livewire::actingAs(User::factory()->admin()->create())->test(NodeView::class, $node);
    Livewire::actingAs(User::factory()->create())->test(NodeView::class, $node);   // Clase 0
    expect(NodeVisit::count())->toBe(2);
});

test('se anotan los aciertos y los fallos (el mismo fallo seguido, una vez), nunca en una micro-misión cerrada', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    [$first, $second] = $course->rootNode->steps()->get()->all();
    $component = Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode]);

    $component->call('failStep', $first->id, 'bad', 'He go')
        ->call('failStep', $first->id, 'bad', 'He go')
        ->call('failStep', $first->id, 'almost', 'He goe')
        ->call('completeStep', $first->id, 'Hola valle', '')
        ->call('completeStep', $first->id, 'Hola, Valle', 'print("Hola, Valle")')
        ->call('failStep', $second->id + 1000, 'bad', 'x');

    $attempts = StepAttempt::where('user_id', $student->id)->orderBy('id')->get();
    expect($attempts->map(fn ($a) => [$a->passed, $a->kind, $a->answer])->all())->toBe([
        [false, 'bad', 'He go'],
        [false, 'almost', 'He goe'],
        [false, 'output', 'Hola valle'],
        [true, null, null],
    ])->and($attempts[0]->course_id)->toBe($course->id);

    // La segunda está cerrada hasta superar la primera: con otro alumno no se anota.
    $other = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    Livewire::actingAs($other)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode])
        ->call('failStep', $second->id, 'bad', 'x');
    expect(StepAttempt::where('user_id', $other->id)->count())->toBe(0);
});

test('los fallos de código guardan el código del intento (los aciertos no)', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $first = $course->rootNode->steps()->first();

    Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode])
        ->call('failStep', $first->id, 'error', 'NameError', 'prin("Hola")')
        ->call('failStep', $first->id, 'error', 'NameError', 'prin("Hola")')
        ->call('failStep', $first->id, 'error', 'NameError', 'prnt("Hola")')
        ->call('completeStep', $first->id, 'Hola valle', 'print("Hola valle")')
        ->call('completeStep', $first->id, 'Hola, Valle', 'print("Hola, Valle")');

    // Mismo error con otro código cuenta aparte: el docente ve cada versión.
    expect(StepAttempt::where('user_id', $student->id)->orderBy('id')->pluck('code')->all())
        ->toBe(['prin("Hola")', 'prnt("Hola")', 'print("Hola valle")', null]);
});

test('el docente abre un fallo y ve su código, lo esperado y la solución', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $first = $course->rootNode->steps()->first();
    app(ActivityLog::class)->attempt($student, $first, false, 'output', 'Hola valle', 'print("Hola valle")');
    app(ActivityLog::class)->attempt($student, $first, false, 'output', 'Hola', null);
    [$withCode, $withoutCode] = StepAttempt::orderBy('id')->get()->all();

    $component = Livewire::actingAs(User::factory()->admin()->create())->test(Tree::class, ['user' => $student, 'course' => $course])
        ->assertDontSee('data-test="fail-detail"', false)
        ->call('toggleFail', $withCode->id)
        ->assertSee('data-test="fail-detail"', false)
        ->assertSee('data-test="fail-student-code"', false)
        ->assertSee('data-test="fail-solution"', false)
        ->assertSee('Hola, Valle');

    $component->call('toggleFail', $withoutCode->id)
        ->assertDontSee('data-test="fail-student-code"', false)
        ->assertSee('antes de que se guardara el código')
        ->call('toggleFail', $withoutCode->id)
        ->assertDontSee('data-test="fail-detail"', false);

    // Un intento de otro alumno no se abre desde este árbol.
    $other = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    app(ActivityLog::class)->attempt($other, $first, false, 'output', 'x', 'print("x")');
    $component->call('toggleFail', StepAttempt::latest('id')->value('id'))->assertDontSee('data-test="fail-detail"', false);
});

test('los intentos de más de seis meses se borran', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $first = $course->rootNode->steps()->first();
    $log = app(ActivityLog::class);

    $this->travel(-7)->months();
    $log->attempt($student, $first, false, 'bad', 'viejo');
    $this->travelBack();
    $log->attempt($student, $first, false, 'bad', 'nuevo');

    expect($log->prune())->toBe(1)
        ->and(StepAttempt::pluck('answer')->all())->toBe(['nuevo']);
});

test('el árbol del alumno muestra su recorrido: dónde se traba y sus respuestas equivocadas', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $first = $course->rootNode->steps()->first();
    foreach (['He go', 'He goes not', 'He gos'] as $answer) {
        app(ActivityLog::class)->attempt($student, $first, false, 'bad', $answer);
    }
    app(ActivityLog::class)->visit($student, $course->rootNode);

    $this->actingAs(User::factory()->admin()->create())->get(route('admin.students.tree', [$student, $course]))
        ->assertOk()
        ->assertSee('data-test="student-journey"', false)
        ->assertSee($course->rootNode->title)
        ->assertSee('3 fallos')
        ->assertSee('He gos')
        ->assertSee('data-test="student-recent-fails"', false);
});

/*
 * D123: «Necesito ayuda». Todo sale de comparar el código inicial con la solución; la solución llega de a una línea,
 * una por cada intento fallido, y si vio alguna la micro-misión paga la mitad.
 */

test('la comparación de líneas marca lo que cambia entre el código inicial y la solución', function () {
    $step = new NodeStep([
        'starter_code' => "nombre = \"Mia\"\nprint(___)\nfin = 1",
        'solution' => "nombre = \"Mia\"\nprint(nombre)\nprint(\"chau\")\nfin = 1",
    ]);
    $helper = app(StepHelper::class);

    expect(collect(LineDiff::ops($step->starter_code, $step->solution))->pluck('op')->all())->toBe(['same', 'add', 'add', 'del', 'same'])
        ->and($helper->whereLines($step))->toBe([1, 2])
        ->and($helper->changedLines($step))->toBe([['number' => 2, 'text' => 'print(nombre)'], ['number' => 3, 'text' => 'print("chau")']]);

    // Sin código inicial no hay dónde marcar: todo es nuevo.
    expect($helper->whereLines(new NodeStep(['starter_code' => '', 'solution' => 'print(1)'])))->toBe([]);
});

test('la primera línea de la solución recién después de un fallo, y cada siguiente después de otro', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    [$first, $second] = $course->rootNode->steps()->get()->all();
    app(StepCompleter::class)->complete($student, $first, 'Hola, Valle');
    $component = Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode]);

    // Sin fallar todavía, nada.
    $component->call('helpLine', $second->id, '')->assertReturned(fn ($r) => $r['ok'] && $r['wait'] && $r['lines'] === [] && $r['new'] === null);

    $component->call('failStep', $second->id, 'output', 'uno', 'print("uno")');
    // Elige la primera línea que todavía no está en su código: ya escribió print("uno").
    $component->call('helpLine', $second->id, 'print("uno")')
        ->assertReturned(fn ($r) => $r['ok'] && ! $r['wait'] && $r['new'] === 2 && $r['lines'] === [['number' => 2, 'text' => 'print("dos")']] && $r['solution'] === null);
    // Otra sin un fallo nuevo, no.
    $component->call('helpLine', $second->id, 'print("uno")')->assertReturned(fn ($r) => $r['wait'] && count($r['lines']) === 1);

    $this->travel(2)->seconds();
    $component->call('failStep', $second->id, 'output', 'uno', "print(\"uno\")\nprint(\"do\")");
    // Con todas las líneas vistas, la solución completa.
    $component->call('helpLine', $second->id, '')->assertReturned(fn ($r) => $r['new'] === 1 && count($r['lines']) === 2 && $r['solution'] === "print(\"uno\")\nprint(\"dos\")");

    expect(StepHelp::where('user_id', $student->id)->where('kind', 'line')->pluck('line')->all())->toBe([2, 1]);

    // Vio la solución: la mitad de XP (15 → 8).
    $xp = $student->fresh()->xp_total;
    $component->call('completeStep', $second->id, "uno\ndos", 'print("uno")')->assertReturned(['ok' => true, 'xp' => 8, 'gold' => 0, 'halved' => true]);
    expect($student->fresh()->xp_total)->toBe($xp + 8);
});

test('vista la solución, el oro también es la mitad (para arriba)', function () {
    config(['game.gold_enabled' => true]);
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $first = $course->rootNode->steps()->first();
    StepHelp::create(['user_id' => $student->id, 'node_step_id' => $first->id, 'course_id' => $course->id, 'kind' => 'line', 'line' => 1]);

    app(StepCompleter::class)->complete($student, $first, 'Hola, Valle');

    expect(CoinTransaction::where('user_id', $student->id)->whereHas('currency', fn ($q) => $q->where('code', Currency::GOLD))->sum('amount'))->toEqual(3)
        ->and(XpTransaction::where('user_id', $student->id)->where('reason', XpReason::StepCompleted)->sum('amount'))->toEqual(5);
});

test('«¿Dónde toco?» devuelve los renglones y queda anotado; una ayuda inventada no', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $first = $course->rootNode->steps()->first();
    $component = Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode]);

    $component->call('helpWhere', $first->id)->assertReturned(['ok' => true, 'lines' => [1]]);
    $component->call('helpLog', $first->id, 'compare');
    $component->call('helpLog', $first->id, 'trampa');
    $component->call('helpLog', $first->id, 'line');

    expect(StepHelp::where('user_id', $student->id)->pluck('kind')->all())->toBe(['where', 'compare']);
});

test('no se pide ayuda de una micro-misión que todavía no puede jugar', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $second = $course->rootNode->steps()->get()[1];

    Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode])
        ->call('helpLine', $second->id, '')->assertReturned(['ok' => false, 'error' => 'Esta micro-misión todavía no está disponible.']);
    expect(StepHelp::count())->toBe(0);
});

test('el staff y la Clase 0 de prueba ven las líneas sin fallar antes y sin dejar registros ni bajar premios', function () {
    $course = coursesWithSteps();
    $visitor = User::factory()->create();
    $first = $course->rootNode->steps()->first();
    $this->actingAs($visitor);

    $r = app(StepHelper::class)->revealLine($visitor, $first, '');
    expect($r['new'])->toBe(1)
        ->and($r['solution'])->toBe('print("Hola, Valle")')
        ->and(StepHelp::count())->toBe(0)
        ->and(app(StepHelper::class)->usedSolution($visitor, $first))->toBeFalse();
});

test('la página muestra el botón de ayuda, sin la solución, y lo ya visto al volver', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);

    $html = $this->actingAs($student)->get(route('student.node', [$course, $course->rootNode]))->assertOk()->getContent();
    expect($html)->toContain('data-test="step-help"')
        ->and($html)->toContain('data-test="step-help-where"')
        ->and($html)->toContain('data-test="step-help-compare"')
        ->and($html)->toContain('data-test="step-help-line"')
        ->and($html)->toContain('data-test="step-read"')
        ->and($html)->not->toContain('Hola, Valle&quot;)')
        ->and($html)->not->toContain('print(\\u0022Hola');

    $first = $course->rootNode->steps()->first();
    StepHelp::create(['user_id' => $student->id, 'node_step_id' => $first->id, 'course_id' => $course->id, 'kind' => 'line', 'line' => 1]);
    $html = $this->actingAs($student)->get(route('student.node', [$course, $course->rootNode]))->getContent();
    expect($html)->toContain('Hola, Valle');
});

test('el recorrido del alumno muestra qué ayuda pidió', function () {
    $course = coursesWithSteps();
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $first = $course->rootNode->steps()->first();
    app(ActivityLog::class)->visit($student, $course->rootNode);
    foreach (['where', 'line', 'line'] as $kind) {
        StepHelp::create(['user_id' => $student->id, 'node_step_id' => $first->id, 'course_id' => $course->id, 'kind' => $kind, 'line' => $kind === 'line' ? 1 : null]);
    }

    $this->actingAs(User::factory()->admin()->create())->get(route('admin.students.tree', [$student, $course]))
        ->assertOk()
        ->assertSee('data-test="journey-step-helps"', false)
        ->assertSee('¿Dónde toco?, 2 líneas de la solución');
});

test('los Pasos se importan y salen en «¿Qué me piden?»; pedirlos queda anotado (fase 2)', function () {
    $report = app(CourseImporter::class)->import(stepsCourseFile(fn ($md) => str_replace('### Misión R00-N01-M1',
        str_replace("#### Código inicial\n```python\n# tu conjuro", "#### Pasos\n1. Escribí `print(\"Hola, Valle\")`.\n2. Tocá **Ejecutar**.\n\n#### Código inicial\n```python\n# tu conjuro", STEPS_MD).'### Misión R00-N01-M1', $md)), dryRun: false);
    expect($report->errors)->toBe([]);
    $course = Course::where('slug', 'python-import')->firstOrFail();
    $course->update(['is_published' => true]);
    [$first, $second] = $course->rootNode->steps()->get()->all();
    expect($first->guide)->toContain('2. Tocá **Ejecutar**.')
        ->and($second->guide)->toBeNull();

    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $html = $this->actingAs($student)->get(route('student.node', [$course, $course->rootNode]))->getContent();
    expect($html)->toContain('data-test="step-help-guide"')
        ->and($html)->toContain('<strong>Ejecutar</strong>');

    Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode])->call('helpLog', $first->id, 'guide');
    expect(StepHelp::where('user_id', $student->id)->where('kind', 'guide')->count())->toBe(1)
        ->and(StudentJourney::helpSummary(StepHelp::where('user_id', $student->id)->get()))->toBe('¿Qué me piden?');
});

test('modo enfoque (fase 3): el desafío y los Pasos arriba, la escena plegada; lo prende el alumno o su docente', function () {
    app(CourseImporter::class)->import(stepsCourseFile(fn ($md) => str_replace('### Misión R00-N01-M1',
        str_replace("#### Código inicial\n```python\n# tu conjuro", "#### Pasos\n1. Escribí `print(\"Hola, Valle\")`.\n2. Tocá **Ejecutar**.\n\n#### Código inicial\n```python\n# tu conjuro", STEPS_MD).'### Misión R00-N01-M1', $md)), dryRun: false);
    $course = Course::where('slug', 'python-import')->firstOrFail();
    $course->update(['is_published' => true]);
    $student = studentWithRootOpen(['course' => $course, 'root' => $course->rootNode]);
    $url = route('student.node', [$course, $course->rootNode]);

    expect($this->actingAs($student)->get($url)->getContent())
        ->toContain('data-test="step-help-guide"')
        ->not->toContain('data-test="step-focus-guide"');

    // El alumno lo prende en su perfil.
    Livewire::actingAs($student)->test(Profile::class)->set('focus_mode', true);
    expect($student->fresh()->focus_mode)->toBeTrue();

    $html = $this->actingAs($student->fresh())->get($url)->getContent();
    expect($html)->toContain('data-test="step-focus-guide"')
        ->toContain('data-test="step-focus-scene"')
        ->toContain('text-lg leading-relaxed')
        ->not->toContain('data-test="step-help-guide"')
        ->not->toContain('data-test="step-image"');
    // Ver los Pasos así no cuenta como ayuda pedida.
    expect(StepHelp::where('user_id', $student->id)->count())->toBe(0);

    // Lo apaga el administrador (o el docente de su comisión) desde la ficha.
    Livewire::actingAs(User::factory()->admin()->create())
        ->test(Show::class, ['user' => $student])
        ->assertSee('Modo enfoque: prendido')
        ->call('toggleFocusMode')
        ->assertSee('Modo enfoque: apagado');
    expect($student->fresh()->focus_mode)->toBeFalse();
});

test('un docente no cambia el modo enfoque de un alumno ajeno', function () {
    $made = makeCourse();
    $student = studentWithRootOpen($made);

    Livewire::actingAs(User::factory()->teacher()->create())
        ->test(Show::class, ['user' => $student])
        ->assertForbidden();
    expect(app(Gate::class)->forUser(User::factory()->teacher()->create())->allows('setFocusMode', $student))->toBeFalse();
});
