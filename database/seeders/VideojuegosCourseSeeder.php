<?php

namespace Database\Seeders;

use App\Services\CourseImporter;
use Illuminate\Database\Seeder;
use RuntimeException;

/** Videojuegos: Ciudad Arcadia (D126, sin publicar; pide C hasta R02-N07, por eso va después de C) para desarrollo local: se importa de cursos/videojuegos/ con sus escenas. */
class VideojuegosCourseSeeder extends Seeder
{
    public function run(CourseImporter $importer): void
    {
        $files = collect(glob(base_path('cursos/videojuegos/*.md')))->sort()
            ->map(fn (string $file) => ['name' => basename($file), 'content' => file_get_contents($file)])
            ->values()->all();

        $report = $importer->import($files, dryRun: false, assetsDir: base_path('cursos/videojuegos'));
        if ($report->errors !== []) {
            throw new RuntimeException("El curso de Videojuegos no se pudo importar:\n".implode("\n", $report->errors));
        }
    }
}
