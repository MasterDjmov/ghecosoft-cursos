<?php

namespace Database\Seeders;

use App\Services\CourseImporter;
use Illuminate\Database\Seeder;
use RuntimeException;

/** JavaScript (D115) para desarrollo local: se importa de cursos/javascript/ con sus escenas. */
class JavascriptCourseSeeder extends Seeder
{
    public function run(CourseImporter $importer): void
    {
        $files = collect(glob(base_path('cursos/javascript/*.md')))->sort()
            ->map(fn (string $file) => ['name' => basename($file), 'content' => file_get_contents($file)])
            ->values()->all();

        $report = $importer->import($files, dryRun: false, assetsDir: base_path('cursos/javascript'));
        if ($report->errors !== []) {
            throw new RuntimeException("El curso de JavaScript no se pudo importar:\n".implode("\n", $report->errors));
        }
    }
}
