<?php

namespace App\Console\Commands;

use App\Services\CourseImporter;
use App\Support\CourseImport\ImportReport;
use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;

#[Signature('app:import-course {paths* : Archivos .md o carpetas (se leen sus .md en orden alfabético)} {--apply : Guardar los cambios (sin esto, solo revisa)}')]
#[Description('Importa o actualiza un curso desde el formato de docs/FORMATO-CURSO.md')]
class ImportCourse extends Command
{
    public function handle(CourseImporter $importer): int
    {
        $files = [];
        foreach ($this->argument('paths') as $path) {
            $list = is_dir($path) ? glob(rtrim($path, '/').'/*.md') : [$path];
            sort($list);
            foreach ($list as $file) {
                if (! is_file($file) || ! is_readable($file)) {
                    $this->error("No se puede leer {$file}.");

                    return self::FAILURE;
                }
                $files[] = ['name' => basename($file), 'content' => file_get_contents($file)];
            }
        }

        if ($files === []) {
            $this->error('No hay archivos .md para importar.');

            return self::FAILURE;
        }

        $apply = (bool) $this->option('apply');
        $this->info(($apply ? 'Importando' : 'Revisando').' '.count($files).' archivo(s)…');
        // Las capturas de «Cómo debe quedar» (D77) se buscan desde la carpeta del curso.
        $first = $this->argument('paths')[0];
        $report = $importer->import($files, dryRun: ! $apply, assetsDir: is_dir($first) ? $first : dirname($first));
        $this->printReport($report);

        if (! $report->ok()) {
            $this->error('No se guardó nada: corregí los errores y volvé a intentar.');

            return self::FAILURE;
        }

        $apply
            ? $this->info("Listo: «{$report->courseTitle}» importado.")
            : $this->comment('Para guardar, repetí el comando con --apply.');

        return self::SUCCESS;
    }

    private function printReport(ImportReport $report): void
    {
        if ($report->counts !== []) {
            $this->table(['', 'Nuevos', 'Cambiados', 'Iguales'], collect($report->counts)
                ->map(fn ($c, $entity) => [$entity, $c['created'], $c['updated'], $c['unchanged']])->values()->all());
        }
        foreach ($report->errors as $message) {
            $this->line("<fg=red>✗</> {$message}");
        }
        foreach ($report->warnings as $message) {
            $this->line("<fg=yellow>!</> {$message}");
        }
        foreach ($report->notes as $message) {
            $this->line("· {$message}");
        }
    }
}
