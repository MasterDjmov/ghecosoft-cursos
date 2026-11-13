<?php

use App\Enums\Language;
use App\Models\Course;
use App\Models\User;
use App\Services\CourseImporter;
use App\Services\NodeUnlocker;
use App\Support\CodeFiles;

// D119: el curso de C#. El código corre en el navegador del alumno, nunca en el servidor.

function importCsharp(): Course
{
    $files = collect(glob(base_path('cursos/csharp/*.md')))->sort()
        ->map(fn (string $file) => ['name' => basename($file), 'content' => file_get_contents($file)])->values()->all();
    $report = app(CourseImporter::class)->import($files, dryRun: false);
    expect($report->errors)->toBe([]);

    return Course::where('slug', 'csharp')->firstOrFail();
}

test('C# corre en el navegador del alumno y se entrega con su extensión', function () {
    expect(Language::Csharp->label())->toBe('C#')
        ->and(Language::Csharp->runsForStudents())->toBeTrue()
        ->and(Language::Csharp->runsOnLocalRunner())->toBeFalse()
        ->and(Language::Csharp->extension())->toBe('cs');
});

test('el curso se importa entero, con sus micro-misiones y sin mostrar las soluciones', function () {
    $course = importCsharp();
    $root = $course->rootNode;

    expect($course->language)->toBe(Language::Csharp)
        ->and($course->nodes()->count())->toBeGreaterThanOrEqual(5);

    $student = enrolledStudent($course, User::factory()->create());
    app(NodeUnlocker::class)->unlock($student, $root);

    $this->actingAs($student)->get(route('student.node', [$course, $root]))
        ->assertOk()
        ->assertSee('La primera nota')
        ->assertDontSee('Console.WriteLine(&quot;Hola, Conservatorio&quot;);', false);
});

test('Ceci tiene sus seis aspectos, y sus fichas y las de Clave y Bemol tienen imagen', function () {
    $hero = config('game.protagonists.csharp');

    expect($hero['name'])->toBe('Ceci')->and($hero['looks'])->toHaveCount(6);
    foreach (array_keys($hero['looks']) as $look) {
        expect(public_path("img/protagonistas/ceci/{$look}.webp"))->toBeFile();
    }
    foreach (['ceci', 'clave', 'bemol'] as $slug) {
        expect(public_path("img/enciclopedia/{$slug}.webp"))->toBeFile()
            ->and(public_path("img/enciclopedia/{$slug}-cuerpo.webp"))->toBeFile();
    }
});

test('toda micro-misión tiene su escena', function () {
    // Ramas cuyas escenas todavía no se generaron: mientras tanto se ven con el cartel «Escena en construcción».
    // Sacar la rama de la lista apenas estén sus escenas.
    $pending = ['R06'];
    $text = implode("\n", array_map('file_get_contents', glob(base_path('cursos/csharp/*.md'))));
    preg_match_all('/^### Micro-misión (R\d+-N\d+-P\d+)/m', $text, $ids);

    expect($ids[1])->not->toBeEmpty();
    foreach ($ids[1] as $id) {
        if (in_array(substr($id, 0, 3), $pending, true)) {
            continue;
        }
        expect(base_path("cursos/csharp/escenas/{$id}.webp"))->toBeFile();
    }
});

test('un ejemplo de C# con dos archivos se ve en solapas', function () {
    $split = CodeFiles::split("`Nota.cs`\n```csharp\nrecord Nota(string N);\n```\n\n`Program.cs`\n```cs\nConsole.WriteLine(1);\n```", 'csharp');

    expect(array_column($split['files'], 'name'))->toBe(['Nota.cs', 'Program.cs'])
        ->and(array_column($split['files'], 'language'))->toBe(['csharp', 'csharp']);
});
