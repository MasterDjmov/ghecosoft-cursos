<?php

namespace Database\Seeders;

use App\Services\CourseImporter;
use Illuminate\Database\Seeder;
use RuntimeException;

/** TypeScript (D115) para desarrollo local: se importa de cursos/typescript/ (sus escenas, cuando estén). */
class TypescriptCourseSeeder extends Seeder
{
    public function run(CourseImporter $importer): void
    {
        $files = collect(glob(base_path('cursos/typescript/*.md')))->sort()
            ->map(fn (string $file) => ['name' => basename($file), 'content' => file_get_contents($file)])
            ->values()->all();

        $report = $importer->import($files, dryRun: false, assetsDir: base_path('cursos/typescript'));
        if ($report->errors !== []) {
            throw new RuntimeException("El curso de TypeScript no se pudo importar:\n".implode("\n", $report->errors));
        }
    }
}
