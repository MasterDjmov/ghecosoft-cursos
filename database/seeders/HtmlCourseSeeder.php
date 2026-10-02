<?php

namespace Database\Seeders;

use App\Enums\Modality;
use App\Models\Course;
use App\Services\CourseImporter;
use Illuminate\Database\Seeder;
use RuntimeException;

/**
 * Curso de HTML y CSS para desarrollo local: se importa de cursos/html/ con el mismo importador que usa el
 * docente, con la carpeta para que copie las capturas de «Así tiene que quedar» (D77, D78).
 */
class HtmlCourseSeeder extends Seeder
{
    public function run(CourseImporter $importer): void
    {
        $files = collect(glob(base_path('cursos/html/*.md')))->sort()
            ->map(fn (string $file) => ['name' => basename($file), 'content' => file_get_contents($file)])
            ->values()->all();

        $report = $importer->import($files, dryRun: false, assetsDir: base_path('cursos/html'));
        if ($report->errors !== []) {
            throw new RuntimeException("El curso de HTML y CSS no se pudo importar:\n".implode("\n", $report->errors));
        }

        $course = Course::where('slug', 'html')->firstOrFail();
        $course->cohorts()->firstOrCreate(['name' => 'HTML y CSS – Clases individuales'], [
            'modality' => Modality::Virtual,
            'schedule_text' => 'A coordinar con el profe',
        ]);
    }
}
