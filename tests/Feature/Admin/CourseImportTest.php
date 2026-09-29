<?php

use App\Enums\NodeType;
use App\Enums\PracticeEnvironment;
use App\Enums\SubmissionMode;
use App\Livewire\Admin\Courses\Import;
use App\Livewire\Student\NodeView;
use App\Models\Course;
use App\Models\GlossaryTerm;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Models\Practice;
use App\Models\Submission;
use App\Models\User;
use App\Services\CourseImporter;
use App\Services\NodeUnlocker;
use Illuminate\Http\UploadedFile;
use Livewire\Livewire;

function exampleCourseFile(?callable $edit = null): array
{
    $content = file_get_contents(base_path('tests/Fixtures/curso-ejemplo.md'));

    return [['name' => 'curso.md', 'content' => $edit ? $edit($content) : $content]];
}

test('revisar no guarda nada y cuenta lo que se crearía', function () {
    $report = app(CourseImporter::class)->import(exampleCourseFile(), dryRun: true);

    expect($report->ok())->toBeTrue()
        ->and($report->counts['nodos']['created'])->toBe(4)
        ->and($report->counts['prácticas']['created'])->toBe(6)
        ->and(Course::where('slug', 'python-import')->exists())->toBeFalse();
});

test('importar crea el curso completo: ramas, nodos con sus secciones, prácticas, insignia y diccionario', function () {
    $report = app(CourseImporter::class)->import(exampleCourseFile(), dryRun: false);
    expect($report->errors)->toBe([]);

    $course = Course::where('slug', 'python-import')->firstOrFail();
    $root = Node::where('course_id', $course->id)->where('code', 'R00-N01')->firstOrFail();
    $variables = Node::where('course_id', $course->id)->where('code', 'R01-N01')->firstOrFail();
    $boss = Node::where('course_id', $course->id)->where('code', 'R01-N02')->firstOrFail();
    $extra = Node::where('course_id', $course->id)->where('code', 'R90-N01')->firstOrFail();

    expect($course->is_published)->toBeFalse()
        ->and($course->description)->toContain('primer `print`')
        ->and($root->type)->toBe(NodeType::Root)
        ->and($root->branch_id)->toBeNull()
        ->and($root->chronicle)->toBe('Cruzás el portal y caés sobre el pasto del Valle.')
        ->and($root->content)->toContain('#### Tu primer programa')
        ->and($root->content)->toContain('# Esto es un comentario')
        ->and($root->example_code)->toBe('print("Hola, mundo")')
        ->and($root->expected_output)->toBe('Hola, mundo')
        ->and($root->beast_key)->toBe('beast.slime')
        ->and($root->self_check)->toBe([
            ['question' => '¿Qué muestra print(1 + 1)?', 'answer' => '2'],
            ['question' => '¿Dónde está el tipo de error en el traceback?', 'answer' => 'En la última línea.'],
        ])
        ->and($root->teacher_solutions)->toBe('Tiempo estimado: 60 minutos.')
        ->and($variables->parent_id)->toBe($root->id)
        ->and($variables->beast_key)->toBe('beast.esqueleto')
        ->and($boss->type)->toBe(NodeType::Boss)
        ->and($boss->badge->name)->toBe('Cazador de slimes')
        ->and($extra->type)->toBe(NodeType::Extra)
        ->and($extra->priceCurrency->is_wildcard)->toBeTrue()
        ->and($extra->branch->is_extra)->toBeTrue();

    [$install, $program, $ticket] = $root->practices()->get()->all();
    expect($install->submission_mode)->toBe(SubmissionMode::None)
        ->and($install->environment)->toBe(PracticeEnvironment::Local)
        ->and($program->is_required)->toBeTrue()
        ->and($program->coin_reward)->toBe(10)
        ->and($program->approval_criteria)->toBe('- Usa `print()` dos veces.')
        ->and($program->reference_solution)->toBe("print(\"Kira\")\nprint(\"La Rioja\")")
        ->and($ticket->is_required)->toBeFalse()
        ->and($variables->practices()->first()->sample_input)->toBe('15');

    expect(GlossaryTerm::where('key', 'coin.course')->where('course_id', $course->id)->value('singular'))->toBe('escama')
        ->and(GlossaryTerm::where('key', 'world.name')->whereNull('course_id')->value('singular'))->toBe('Aetheria')
        ->and(term('mentor.name', $course))->toBe('Ofidia');
});

test('reimportar actualiza por ID sin duplicar ni tocar el progreso de los alumnos', function () {
    $importer = app(CourseImporter::class);
    $importer->import(exampleCourseFile(), dryRun: false);
    $course = Course::where('slug', 'python-import')->firstOrFail();
    $root = Node::where('course_id', $course->id)->where('code', 'R00-N01')->firstOrFail();
    $practice = $root->practices()->where('code', 'R00-N01-M2')->firstOrFail();
    $course->update(['is_published' => true]);

    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $root);
    Submission::create(['practice_id' => $practice->id, 'user_id' => $student->id, 'attempt' => 1, 'code' => 'print(1)', 'submitted_at' => now()]);

    $same = $importer->import(exampleCourseFile(), dryRun: false);
    expect($same->counts['nodos'])->toBe(['created' => 0, 'updated' => 0, 'unchanged' => 4]);

    $changed = $importer->import(exampleCourseFile(fn ($c) => str_replace('Mostrá tu nombre y tu ciudad', 'Mostrá tu nombre, tu ciudad', $c)), dryRun: false);
    expect($changed->counts['prácticas']['updated'])->toBe(1)
        ->and(Node::where('course_id', $course->id)->count())->toBe(4)
        ->and($practice->fresh()->instructions)->toStartWith('Mostrá tu nombre, tu ciudad')
        ->and(NodeUnlock::where('user_id', $student->id)->where('node_id', $root->id)->exists())->toBeTrue()
        ->and(Submission::where('practice_id', $practice->id)->count())->toBe(1)
        ->and($course->fresh()->is_published)->toBeTrue(); // el archivo dice "publicado: no", pero solo vale al crear
});

test('el raíz de un curso existente adopta el ID y los nodos que no están en el archivo quedan igual', function () {
    ['course' => $course, 'root' => $root, 'topic1' => $topic1] = makeCourse(['slug' => 'python-import']);

    $report = app(CourseImporter::class)->import(exampleCourseFile(), dryRun: false);

    expect($report->errors)->toBe([])
        ->and($root->fresh()->code)->toBe('R00-N01')
        ->and($topic1->fresh()->exists)->toBeTrue()
        ->and(collect($report->notes)->implode(' '))->toContain('Tema 1');
});

test('con un error no se guarda nada', function (callable $edit, string $message) {
    $report = app(CourseImporter::class)->import(exampleCourseFile($edit), dryRun: false);

    expect($report->ok())->toBeFalse()
        ->and(collect($report->errors)->implode(' '))->toContain($message)
        ->and(Course::where('slug', 'python-import')->exists())->toBeFalse();
})->with([
    'padre inexistente' => [fn ($c) => str_replace('padre: R01-N01', 'padre: R09-N09', $c), 'R09-N09'],
    'dos raíces' => [fn ($c) => str_replace("tipo: tema\npadre: R00-N01", "tipo: raiz\npadre: R00-N01", $c), 'exactamente un nodo'],
    'ciclo' => [fn ($c) => str_replace("tipo: tema\npadre: R00-N01", "tipo: tema\npadre: R01-N02", $c), 'ciclo'],
    'entrega desconocida' => [fn ($c) => str_replace('entrega: codigo', 'entrega: telepatia', $c), 'telepatia'],
    'sin lenguaje' => [fn ($c) => str_replace('lenguaje: python', '', $c), 'lenguaje'],
]);

test('se aceptan archivos envueltos en un bloque ```markdown, como los copia un chat', function () {
    $report = app(CourseImporter::class)->import(exampleCourseFile(fn ($c) => "````markdown\n{$c}\n````\n"), dryRun: true);

    expect($report->errors)->toBe([])
        ->and($report->counts['nodos']['created'])->toBe(4);
});

test('un nodo publicado sin misiones obligatorias es un error; sin publicar, solo un aviso', function () {
    $sinHojas = "\n# RAMA R03 · Vacía\n\n## R03-N01 · Sin hojas\n\n```meta\npadre: R01-N01\n```\n";
    $bad = app(CourseImporter::class)->import(exampleCourseFile(fn ($c) => $c.$sinHojas), dryRun: true);
    expect(collect($bad->errors)->implode(' '))->toContain('R03-N01 no tiene ninguna práctica obligatoria');

    $draft = app(CourseImporter::class)->import(exampleCourseFile(fn ($c) => $c.str_replace('padre: R01-N01', "padre: R01-N01\npublicado: no", $sinHojas)), dryRun: true);
    expect($draft->errors)->toBe([])
        ->and(collect($draft->warnings)->implode(' '))->toContain('queda sin publicar');
});

test('los comentarios en el bloque meta se ignoran', function () {
    $report = app(CourseImporter::class)->import(exampleCourseFile(fn ($c) => str_replace('precio: 3', 'precio: 3   # en comodines', $c)), dryRun: false);

    expect($report->errors)->toBe([])
        ->and(Node::where('code', 'R90-N01')->value('price'))->toBe(3);
});

test('avisa si las obligatorias no alcanzan para pagar el nodo siguiente', function () {
    $report = app(CourseImporter::class)->import(exampleCourseFile(fn ($c) => str_replace("padre: R00-N01\nprecio: 10", "padre: R00-N01\nprecio: 25", $c)), dryRun: true);

    expect(collect($report->warnings)->implode(' '))->toContain('R01-N01 cuesta 25');
});

test('solo el docente entra a importar', function () {
    $this->actingAs(User::factory()->create())->get(route('admin.courses.import'))->assertRedirect(route('home'));
    $this->actingAs(User::factory()->admin()->create())->get(route('admin.courses.import'))->assertOk();
});

test('desde el admin se revisa y después se importa', function () {
    $this->actingAs(User::factory()->admin()->create());
    $file = UploadedFile::fake()->createWithContent('curso.md', file_get_contents(base_path('tests/Fixtures/curso-ejemplo.md')));

    $component = Livewire::test(Import::class)
        ->set('files', [$file])
        ->call('review')
        ->assertHasNoErrors()
        ->assertSee('todo en orden')
        ->assertSet('applied', false);
    expect(Course::where('slug', 'python-import')->exists())->toBeFalse();

    $component->call('import')->assertSet('applied', true)->assertSee('importado');
    expect(Course::where('slug', 'python-import')->exists())->toBeTrue();
});

test('el comando revisa por defecto e importa con --apply', function () {
    $path = base_path('tests/Fixtures/curso-ejemplo.md');

    $this->artisan('app:import-course', ['paths' => [$path]])->assertSuccessful();
    expect(Course::where('slug', 'python-import')->exists())->toBeFalse();

    $this->artisan('app:import-course', ['paths' => [$path], '--apply' => true])->assertSuccessful();
    expect(Course::where('slug', 'python-import')->exists())->toBeTrue();
});

test('el curso trae nivel, destacado y temario; un nodo puede no ejecutarse; los tabuladores de una salida se respetan', function () {
    $file = exampleCourseFile(fn (string $content) => str_replace(
        ["publicado: no\n```\n", "tipo: raiz\n", "### Salida esperada\n\n```\nHola, mundo\n```"],
        ["publicado: no\nnivel: intermedio\ndestacado: si\n```\n\n### Temario\n\n- Variables\n- Bucles\n", "tipo: raiz\nejecutable: no\n", "### Salida esperada\n\n```\nNombre:\tKira\n```"],
        $content,
    ));

    $report = app(CourseImporter::class)->import($file, dryRun: false);
    expect($report->errors)->toBe([]);

    $course = Course::where('slug', 'python-import')->firstOrFail();
    $root = Node::where('code', 'R00-N01')->firstOrFail();
    expect($course->level->label())->toBe('Intermedio')
        ->and($course->is_featured)->toBeTrue()
        ->and($course->syllabusItems())->toBe(['Variables', 'Bucles'])
        ->and($root->example_runnable)->toBeFalse()
        ->and($root->expected_output)->toBe("Nombre:\tKira")
        ->and(Node::where('code', 'R01-N01')->value('example_runnable'))->toBeTrue();
});

test('un ejemplo marcado "ejecutable: no" se muestra sin botón Ejecutar', function () {
    ['course' => $course, 'root' => $root] = makeCourse();
    $root->update(['example_code' => 'import pygame', 'example_language' => 'python', 'example_runnable' => false]);
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $root);

    Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $root])
        ->assertSee('import pygame')
        ->assertViewHas('runnable', false);
});

test('los cursos reales de cursos/ se importan sin errores ni avisos', function (string $carpeta) {
    $files = collect(glob(base_path("cursos/{$carpeta}/*.md")))->sort()
        ->map(fn (string $file) => ['name' => basename($file), 'content' => file_get_contents($file)])
        ->values()->all();

    $report = app(CourseImporter::class)->import($files, dryRun: true)->toArray();

    expect($files)->not->toBeEmpty()
        ->and($report['errors'])->toBe([])
        ->and($report['warnings'])->toBe([]);
})->with(['python', 'c', 'cpp']);

test('una entrada de ejemplo que empieza con una línea vacía la conserva', function () {
    $contenido = str_replace("#### Entrada de ejemplo\n\n```\n15\n```", "#### Entrada de ejemplo\n\n```\n\n15\n```", file_get_contents(base_path('tests/Fixtures/curso-ejemplo.md')));
    app(CourseImporter::class)->import([['name' => 'curso.md', 'content' => $contenido]], dryRun: false);

    expect(Practice::where('code', 'R01-N01-M1')->value('sample_input'))->toBe("\n15");
});
