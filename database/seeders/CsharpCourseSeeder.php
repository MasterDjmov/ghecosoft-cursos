<?php

namespace Database\Seeders;

use App\Services\CourseImporter;
use Illuminate\Database\Seeder;
use RuntimeException;

/** C# (D119) para desarrollo local: se importa de cursos/csharp/ con sus escenas. */
class CsharpCourseSeeder extends Seeder
{
    public function run(CourseImporter $importer): void
    {
        $files = collect(glob(base_path('cursos/csharp/*.md')))->sort()
            ->map(fn (string $file) => ['name' => basename($file), 'content' => file_get_contents($file)])
            ->values()->all();

        $report = $importer->import($files, dryRun: false, assetsDir: base_path('cursos/csharp'));
        if ($report->errors !== []) {
            throw new RuntimeException("El curso de C# no se pudo importar:\n".implode("\n", $report->errors));
        }
    }
}
