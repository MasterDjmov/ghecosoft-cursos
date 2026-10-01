<?php

use App\Models\Course;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Models\Practice;
use App\Services\CourseImporter;
use App\Services\NodeUnlocker;
use App\Support\CourseImport\CourseFileParser;
use App\Support\LocalCodeRunner;
use Illuminate\Support\Facades\File;

/** D73: pruebas extra por práctica (#### Pruebas), solo del docente. */
function withTests(string $tests, string $solution = "oro = int(input())\nprint(oro)"): array
{
    $content = file_get_contents(base_path('tests/Fixtures/curso-ejemplo.md'));

    return [['name' => 'curso.md', 'content' => str_replace(
        "#### Salida esperada\n\n```\n15\n```\n",
        "#### Salida esperada\n\n```\n15\n```\n\n#### Solución de referencia\n\n```python\n{$solution}\n```\n\n#### Pruebas\n\n{$tests}\n",
        $content,
    )]];
}

const TWO_TESTS = "##### Cero\n```entrada\n0\n```\n```salida\n0\n```\n\n##### Mucho oro\n```entrada\n999\n```\n```salida\n999\n```";

function goldPractice(): Practice
{
    $course = Course::where('slug', 'python-import')->firstOrFail();

    return Practice::where('code', 'R01-N01-M1')->whereHas('node', fn ($q) => $q->where('course_id', $course->id))->firstOrFail();
}

test('el lector arma cada prueba con nombre, entrada y salida (una sin salida queda en null)', function () {
    $tests = CourseFileParser::parseTests("##### Vacía\n```entrada\n\nfin\n```\n```salida\nNo hay piezas.\n```\n\n##### Sin salida todavía\n```entrada\n3\n```\n```salida\n```\n\n##### Sin entrada\n```salida\nHola\n```");

    expect($tests)->toBe([
        ['name' => 'Vacía', 'input' => "\nfin", 'expected' => 'No hay piezas.'],
        ['name' => 'Sin salida todavía', 'input' => '3', 'expected' => null],
        ['name' => 'Sin entrada', 'input' => null, 'expected' => 'Hola'],
    ]);
});

test('importar guarda las pruebas en orden, y reimportar las reemplaza solo si cambiaron', function () {
    $report = app(CourseImporter::class)->import(withTests(TWO_TESTS), dryRun: false);
    expect($report->errors)->toBe([])
        ->and($report->counts['pruebas']['created'])->toBe(1);

    $tests = goldPractice()->tests;
    expect($tests->pluck('name')->all())->toBe(['Cero', 'Mucho oro'])
        ->and($tests->pluck('input')->all())->toBe(['0', '999'])
        ->and($tests->pluck('expected_output')->all())->toBe(['0', '999']);

    $again = app(CourseImporter::class)->import(withTests(TWO_TESTS), dryRun: false);
    expect($again->counts['pruebas']['unchanged'])->toBe(1);

    $changed = app(CourseImporter::class)->import(withTests("##### Uno\n```entrada\n1\n```\n```salida\n1\n```"), dryRun: false);
    expect($changed->counts['pruebas']['updated'])->toBe(1)
        ->and(goldPractice()->tests->pluck('name')->all())->toBe(['Uno']);
});

test('una prueba sin salida avisa y no se guarda', function () {
    $report = app(CourseImporter::class)->import(withTests("##### Sin salida\n```entrada\n7\n```"), dryRun: false);

    expect($report->ok())->toBeTrue()
        ->and(collect($report->warnings)->contains(fn ($w) => str_contains($w, 'sin salida')))->toBeTrue()
        ->and(goldPractice()->tests)->toHaveCount(0);
});

test('el alumno nunca recibe las pruebas extra', function () {
    app(CourseImporter::class)->import(withTests("##### Secreta\n```entrada\n424242\n```\n```salida\n424242\n```"), dryRun: false);
    $course = Course::where('slug', 'python-import')->firstOrFail();
    $course->update(['is_published' => true]);
    $node = Node::where('course_id', $course->id)->where('code', 'R01-N01')->firstOrFail();
    $student = enrolledStudent($course);
    $node->update(['is_published' => true]);
    app(NodeUnlocker::class)->unlock($student, Node::where('course_id', $course->id)->where('code', 'R00-N01')->firstOrFail());
    NodeUnlock::create(['user_id' => $student->id, 'node_id' => $node->id, 'price_paid' => 0, 'unlocked_at' => now()]);

    $practice = goldPractice();
    $this->actingAs($student)->get(route('student.node', [$course, $node]))->assertOk()->assertSee('Guardá tu oro')->assertDontSee('424242');
    $this->actingAs($student)->get(route('student.mission', [$course, $node, $practice]))->assertOk()->assertDontSee('424242');
});

test('app:course-tests completa las salidas que faltan con la solución de referencia y avisa lo que no coincide', function () {
    if (! (new LocalCodeRunner('python'))->available()) {
        $this->markTestSkipped('Falta python3 en esta compu.');
    }
    $dir = storage_path('framework/testing/curso-pruebas-'.uniqid());
    File::ensureDirectoryExists($dir);
    file_put_contents($dir.'/curso.md', withTests("##### Cero\n```entrada\n0\n```\n```salida\n```\n\n##### Sin bloque\n```entrada\n12\n```\n\n##### Mal escrita\n```entrada\n5\n```\n```salida\n6\n```")[0]['content']);

    $this->artisan('app:course-tests', ['path' => $dir])->assertFailed();   // «Mal escrita» no coincide
    $this->artisan('app:course-tests', ['path' => $dir, '--fill' => true])->assertFailed();

    $tests = CourseFileParser::parseTests(str(file_get_contents($dir.'/curso.md'))->after('#### Pruebas')->before('## R01-N02')->toString());
    expect($tests)->toBe([
        ['name' => 'Cero', 'input' => '0', 'expected' => '0'],
        ['name' => 'Sin bloque', 'input' => '12', 'expected' => '12'],
        ['name' => 'Mal escrita', 'input' => '5', 'expected' => '6'],
    ]);

    File::deleteDirectory($dir);
});
