<?php

namespace App\Console\Commands;

use App\Models\Course;
use App\Models\GlossaryTerm;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Storage;

/**
 * Carga el logo del curso y el de su moneda desde una carpeta (logo.webp y moneda.webp), lo mismo que subirlos en
 * *Admin → Cursos* y en el diccionario: sirve para dejarlos iguales en local y en producción.
 */
class CourseBrand extends Command
{
    protected $signature = 'app:course-brand {slug : El slug del curso} {path : La carpeta con logo.webp y moneda.webp}';

    protected $description = 'Carga el logo del curso y el de su moneda desde una carpeta';

    public function handle(): int
    {
        $course = Course::where('slug', $this->argument('slug'))->first();
        $folder = rtrim((string) $this->argument('path'), '/');
        if (! $course || ! is_file("{$folder}/logo.webp") || ! is_file("{$folder}/moneda.webp")) {
            $this->error('Falta el curso, o logo.webp y moneda.webp en esa carpeta.');

            return self::FAILURE;
        }

        $logo = "cursos/logos/{$course->slug}.webp";
        Storage::disk('public')->put($logo, (string) file_get_contents("{$folder}/logo.webp"));
        $course->update(['logo' => $logo]);

        $coin = "glossary/{$course->slug}-coin.webp";
        Storage::disk('public')->put($coin, (string) file_get_contents("{$folder}/moneda.webp"));
        GlossaryTerm::where('course_id', $course->id)->where('key', 'coin.course')->update(['icon_path' => $coin]);

        $this->info("Listo: logo y moneda de {$course->title}.");

        return self::SUCCESS;
    }
}
