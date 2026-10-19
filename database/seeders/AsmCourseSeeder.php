<?php

namespace Database\Seeders;

use App\Services\CourseImporter;
use Illuminate\Database\Seeder;
use RuntimeException;

/** Ensamblador 8086 (D110) para desarrollo local: se importa de cursos/ensamblador/ con sus escenas. */
class AsmCourseSeeder extends Seeder
{
    public function run(CourseImporter $importer): void
    {
        $files = collect(glob(base_path('cursos/ensamblador/*.md')))->sort()
            ->map(fn (string $file) => ['name' => basename($file), 'content' => file_get_contents($file)])
            ->values()->all();

        $report = $importer->import($files, dryRun: false, assetsDir: base_path('cursos/ensamblador'));
        if ($report->errors !== []) {
            throw new RuntimeException("El curso de Ensamblador no se pudo importar:\n".implode("\n", $report->errors));
        }
    }
}
