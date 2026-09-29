<?php

namespace Database\Seeders;

use App\Enums\Modality;
use App\Models\Course;
use App\Services\CourseImporter;
use Illuminate\Database\Seeder;
use RuntimeException;

/**
 * Curso de Java para desarrollo local: se importa de cursos/java/ con el mismo
 * importador que usa el docente (Admin → Cursos → Importar).
 */
class JavaCourseSeeder extends Seeder
{
    public function run(CourseImporter $importer): void
    {
        $files = collect(glob(base_path('cursos/java/*.md')))->sort()
            ->map(fn (string $file) => ['name' => basename($file), 'content' => file_get_contents($file)])
            ->values()->all();

        $report = $importer->import($files, dryRun: false);
        if ($report->errors !== []) {
            throw new RuntimeException("El curso de Java no se pudo importar:\n".implode("\n", $report->errors));
        }

        $course = Course::where('slug', 'java')->firstOrFail();
        $course->cohorts()->firstOrCreate(['name' => 'Java – Clases individuales'], [
            'modality' => Modality::Virtual,
            'schedule_text' => 'A coordinar con el profe',
        ]);
    }
}
