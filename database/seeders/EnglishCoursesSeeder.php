<?php

namespace Database\Seeders;

use App\Services\CourseImporter;
use Illuminate\Database\Seeder;
use RuntimeException;

/**
 * Crónicas en Inglés (D106) para desarrollo local: Primaria y Secundaria se importan de cursos/ingles-primaria/ y
 * cursos/ingles-secundaria/ con el mismo importador que usa el docente. La carpeta es la de cada curso: las escenas
 * se toman de cursos/ingles/escenas/ (las portadas de Ada y Eco) y de cursos/html/escenas/ («imagen: html/…»).
 */
class EnglishCoursesSeeder extends Seeder
{
    public function run(CourseImporter $importer): void
    {
        foreach (['ingles-primaria', 'ingles-secundaria'] as $folder) {
            $files = collect(glob(base_path("cursos/{$folder}/*.md")))->sort()
                ->map(fn (string $file) => ['name' => basename($file), 'content' => file_get_contents($file)])
                ->values()->all();

            $report = $importer->import($files, dryRun: false, assetsDir: base_path("cursos/{$folder}"));
            if ($report->errors !== []) {
                throw new RuntimeException("El curso {$folder} no se pudo importar:\n".implode("\n", $report->errors));
            }
        }
    }
}
