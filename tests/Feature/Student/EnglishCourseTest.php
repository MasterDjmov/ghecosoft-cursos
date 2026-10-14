<?php

use App\Exceptions\NodeLocked;
use App\Livewire\Admin\Courses\Form as CourseForm;
use App\Livewire\Student\CourseDetail;
use App\Livewire\Student\CourseTree;
use App\Livewire\Student\NodeView;
use App\Models\Course;
use App\Models\Node;
use App\Models\NodeStep;
use App\Models\User;
use App\Services\CourseImporter;
use App\Services\NodeUnlocker;
use App\Services\StepCompleter;
use App\Services\TreeAccess;
use App\Support\CvData;
use App\Support\EnglishExercise;
use Livewire\Livewire;

/*
 * Crónicas en Inglés (D106): un curso que se comprueba solo. Los episodios (nodos) se completan al superar sus
 * micro-misiones, se abren sin monedas, no cuentan para el CV y se muestran como una biblioteca.
 */

function importEnglishPrimaria(): Course
{
    $files = collect(glob(base_path('cursos/ingles-primaria/*.md')))->sort()
        ->map(fn (string $file) => ['name' => basename($file), 'content' => file_get_contents($file)])
        ->values()->all();
    $report = app(CourseImporter::class)->import($files, dryRun: false);
    expect($report->errors)->toBe([]);

    $course = Course::where('slug', 'ingles-primaria')->firstOrFail();
    $course->update(['is_published' => true]);

    return $course->fresh();
}

/** Supera todas las micro-misiones de un episodio, como lo haría el navegador. */
function passEpisode($student, Node $node): void
{
    foreach ($node->steps()->get() as $step) {
        app(StepCompleter::class)->complete($student, $step, EnglishExercise::PASSED);
    }
}

test('el formato del ejercicio se arma y avisa lo que está mal', function () {
    $ok = EnglishExercise::parse("tipo: completar\nconsigna: Pintá.\nbanco: red, blue\n- [#EF4444] {red}\n- The glass is {blue|cyan}.");
    expect($ok['errors'])->toBe([])
        ->and($ok['exercise']['type'])->toBe('fill')
        ->and($ok['exercise']['items'][0]['swatch'])->toBe('#EF4444')
        ->and($ok['exercise']['items'][1]['parts'][1]['hole'])->toBe(['blue', 'cyan']);

    $free = EnglishExercise::parse("tipo: escribir\n- {Hello|Hi}! My name is {*nombre}.");
    expect($free['exercise']['items'][0]['parts'][2])->toBe(['free' => 'name']);

    expect(EnglishExercise::parse("tipo: volar\n- x")['errors'][0])->toContain('desconocido')
        ->and(EnglishExercise::parse("tipo: escuchar\nopciones: a, b\n- c")['errors'][0])->toContain('no está en «opciones:»')
        ->and(EnglishExercise::parse("tipo: completar\nbanco: a\n- sin huecos")['errors'][0])->toContain('no tiene huecos')
        ->and(EnglishExercise::parse("tipo: responder\n- Question?")['errors'][0])->toContain('=>');
});

test('el curso de Primaria se importa sin prácticas y cada micro-misión con su ejercicio', function () {
    $course = importEnglishPrimaria();

    expect($course->language->isSelfChecked())->toBeTrue()
        ->and($course->nodes()->count())->toBe(5)
        ->and($course->nodes()->where('is_published', true)->count())->toBe(5)
        ->and($course->nodes()->whereHas('practices')->exists())->toBeFalse();

    $step = NodeStep::where('code', 'R00-N01-P2')->whereIn('node_id', $course->nodes()->pluck('id'))->first();
    expect($step->englishExercise()['type'])->toBe('fill')
        ->and($step->expected_output)->toBe(EnglishExercise::PASSED)
        ->and($step->translation)->toContain('El vidrio es rojo')
        ->and($step->wordList()[0])->toBe(['en' => 'window', 'es' => 'ventana, vitral']);
});

test('una micro-misión de inglés sin ejercicio no se importa', function () {
    $md = "# CURSO\n\n```meta\nslug: ingles-roto\ntitulo: Roto\nlenguaje: english\n```\n\n## R00-N01 · Uno\n\n```meta\ntipo: raiz\n```\n\n"
        ."### Micro-misión R00-N01-P1 · Hola\n#### Inglés\nHello.\n";
    $report = app(CourseImporter::class)->import([['name' => 'x.md', 'content' => $md]], dryRun: true);

    expect(implode(' ', $report->errors))->toContain('no tiene «Ejercicio»');
});

test('un episodio se completa al superar sus misiones y abre a los siguientes sin monedas', function () {
    $course = importEnglishPrimaria();
    $root = $course->rootNode;
    $episode2 = $course->nodes()->where('code', 'R01-N01')->first();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $root);
    $access = app(TreeAccess::class);

    // Con el primer episodio a medias, el segundo no se abre.
    app(StepCompleter::class)->complete($student, $root->steps()->first(), EnglishExercise::PASSED);
    expect($access->isCompleted($student, $root))->toBeFalse()
        ->and(fn () => app(NodeUnlocker::class)->unlock($student, $episode2))->toThrow(NodeLocked::class);

    passEpisode($student, $root);
    expect($access->isCompleted($student, $root))->toBeTrue()
        ->and($access->state($student, $episode2))->toBe(TreeAccess::STATE_AVAILABLE);

    app(NodeUnlocker::class)->unlock($student, $episode2);
    expect($access->state($student, $episode2))->toBe(TreeAccess::STATE_UNLOCKED);
    passEpisode($student, $episode2);
    expect($access->state($student, $episode2))->toBe(TreeAccess::STATE_COMPLETED);
});

test('lo que manda el navegador tiene que decir «superada»', function () {
    $course = importEnglishPrimaria();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $course->rootNode);

    expect(fn () => app(StepCompleter::class)->complete($student, $course->rootNode->steps()->first(), 'cualquier cosa'))
        ->toThrow(InvalidArgumentException::class);
});

test('el CV deja afuera el curso de inglés', function () {
    $english = importEnglishPrimaria();
    $python = makeCourse();
    $student = enrolledStudent($english);
    app(NodeUnlocker::class)->unlock($student, $english->rootNode);
    $student = enrolledStudent($python['course'], $student);
    app(NodeUnlocker::class)->unlock($student, $python['root']);

    $courses = collect(CvData::for($student)['courses'])->pluck('course.id');
    expect($courses)->toContain($python['course']->id)->not->toContain($english->id);
});

test('el alumno ve la biblioteca y el episodio, y «Leer» muestra el episodio entero', function () {
    $course = importEnglishPrimaria();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $course->rootNode);

    Livewire::actingAs($student)->test(CourseDetail::class, ['course' => $course])
        ->assertSee('Ir a la biblioteca');

    Livewire::actingAs($student)->test(CourseTree::class, ['course' => $course])
        ->assertSee('Elegí qué leer o practicar')
        ->assertSee('Iris Arrives')
        ->assertSee('Se abre al terminar');

    Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode])
        ->assertSee('This is Ada.')
        ->assertDontSee('Teo has an orange glass.');

    Livewire::actingAs($student)->withQueryParams(['leer' => 1])->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode])
        ->assertSee('Escuchar todo')
        ->assertSee('Teo has an orange glass.');
});

test('el alumno resuelve una misión desde la página del episodio', function () {
    $course = importEnglishPrimaria();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $course->rootNode);
    $step = $course->rootNode->steps()->first();

    Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode])
        ->call('completeStep', $step->id, EnglishExercise::PASSED, '')
        ->assertReturned(['ok' => true, 'xp' => $step->xp_reward]);
});

test('el admin guarda un curso de inglés con el primer episodio gratis; uno de programación necesita precio', function () {
    $english = importEnglishPrimaria();
    $admin = User::factory()->admin()->create();

    Livewire::actingAs($admin)->test(CourseForm::class, ['course' => $english])
        ->set('root_price', 0)->set('is_featured', true)
        ->call('save')->assertHasNoErrors();
    expect($english->fresh()->root_price)->toBe(0)
        ->and($english->rootNode->fresh()->price)->toBe(0);

    $python = makeCourse()['course'];
    Livewire::actingAs($admin)->test(CourseForm::class, ['course' => $python])
        ->set('root_price', 0)
        ->call('save')->assertHasErrors('root_price');
});

test('sin abono, la biblioteca deja probar el primer episodio y lleva a pedir el abono', function () {
    $course = importEnglishPrimaria();
    $student = User::factory()->create();

    Livewire::actingAs($student)->test(CourseTree::class, ['course' => $course])
        ->assertSee('Estás probando')
        ->assertSee('Practicar gratis')
        ->assertSee('Pedir abono')
        ->assertDontSee('Empezar');

    Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode])
        ->assertSee('This is Ada.');
});

test('la plataforma deja usar el micrófono solo a ella misma (el extra «hablar»)', function () {
    $this->get('/login')->assertHeader('Permissions-Policy', 'camera=(), microphone=(self), geolocation=(), payment=(), usb=()');
});
