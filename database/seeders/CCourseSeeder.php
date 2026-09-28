<?php

namespace Database\Seeders;

use App\Enums\Modality;
use App\Models\Course;
use App\Services\CourseImporter;
use Illuminate\Database\Seeder;
use RuntimeException;

/**
 * Curso de C para desarrollo local: se importa de cursos/c/ con el mismo
 * importador que usa el docente (Admin → Cursos → Importar).
 */
class CCourseSeeder extends Seeder
{
    public function run(CourseImporter $importer): void
    {
        $files = collect(glob(base_path('cursos/c/*.md')))->sort()
            ->map(fn (string $file) => ['name' => basename($file), 'content' => file_get_contents($file)])
            ->values()->all();

        $report = $importer->import($files, dryRun: false);
        if ($report->errors !== []) {
            throw new RuntimeException("El curso de C no se pudo importar:\n".implode("\n", $report->errors));
        }

        $course = Course::where('slug', 'c')->firstOrFail();
        $course->cohorts()->firstOrCreate(['name' => 'C – Clases individuales'], [
            'modality' => Modality::Virtual,
            'schedule_text' => 'A coordinar con el profe',
        ]);
    }
}
