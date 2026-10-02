<?php

namespace App\Console\Commands;

use App\Models\Course;
use App\Models\GlossaryTerm;
use App\Support\Glossary;
use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

/**
 * Carga de una vez los retratos de la compañía y del bestiario en el Diccionario general (lo mismo que
 * subirlos uno por uno en Admin → Diccionario). Reconoce los archivos por el nombre: personaje_mia.jpeg,
 * slime.png… Los cursos que usan el mismo personaje (el mismo nombre) toman ese retrato.
 * También los fondos 16:9 de los mundos: mundo_codigo (el Mundo del Código, world.name del General) y
 * mundo_<líder> (mundo_ofidia, mundo_maese_ferrum…: la región del curso de esa líder, world.region).
 */
#[Signature('app:glossary-portraits {path : Carpeta con las imágenes} {--apply : Guardar (sin esto, solo muestra qué haría)}')]
#[Description('Carga los retratos de personajes y criaturas, y los fondos de los mundos, en el Diccionario')]
class GlossaryPortraits extends Command
{
    /** Nombre del archivo (sin extensión) → clave del Diccionario. */
    public const FILES = [
        'personaje_kira' => 'hero.name',
        'personaje_elprofe' => 'mentor.name',
        'personaje_mia' => 'companion.theory',
        'personaje_bron' => 'companion.uses',
        'personaje_zed' => 'companion.errors',
        'personaje_gremio' => 'companion.guild',
        'slime' => 'beast.slime',
        'goblin' => 'beast.goblin',
        'esqueleto' => 'beast.skeleton',
        'orco' => 'beast.orc',
        'ogro' => 'beast.ogre',
        'troll' => 'beast.troll',
        'dragon' => 'beast.dragon',
    ];

    public function handle(Glossary $glossary): int
    {
        $folder = rtrim((string) $this->argument('path'), '/');
        $images = collect(glob($folder.'/*.{jpg,jpeg,png,webp}', GLOB_BRACE))
            ->keyBy(fn ($path) => Str::lower(pathinfo($path, PATHINFO_FILENAME)));
        if ($images->isEmpty()) {
            $this->error("No hay imágenes en {$folder}.");

            return self::FAILURE;
        }

        // mundo_<líder> → la región del curso cuya líder (mentor.name) se llama así.
        $regions = GlossaryTerm::where('key', 'mentor.name')->whereNotNull('course_id')->get()
            ->mapWithKeys(fn (GlossaryTerm $mentor) => ['mundo_'.Str::slug($mentor->singular, '_') => $mentor->course_id]);

        $rows = [];
        foreach ($images as $name => $path) {
            [$key, $courseId] = match (true) {
                $name === 'mundo_codigo' => ['world.name', null],
                isset($regions[$name]) => ['world.region', $regions[$name]],
                default => [self::FILES[$name] ?? null, null],
            };
            if (! $key) {
                $rows[] = [basename($path), '—', str_starts_with($name, 'mundo_') ? 'fondo de un personaje: todavía no se usa, se saltea' : 'no lo reconozco: se saltea'];

                continue;
            }
            if (filesize($path) > config('uploads.image.max_kb') * 1024) {
                $rows[] = [basename($path), $key, 'pesa más de '.config('uploads.image.max_kb').' KB: se saltea'];

                continue;
            }

            $course = $courseId ? Course::find($courseId) : null;
            $term = GlossaryTerm::firstOrNew(['key' => $key, 'course_id' => $courseId]);
            $resolved = $glossary->resolve($key, $course);
            $what = $key.' ('.$resolved['singular'].($course ? ' · '.Str::before($course->title, ':') : '').')';
            $rows[] = [basename($path), $what, $term->icon_path ? 'reemplaza la imagen' : 'imagen nueva'];
            if (! $this->option('apply')) {
                continue;
            }

            if (! $term->exists) {
                $term->fill(['singular' => $resolved['singular'], 'plural' => $resolved['plural'], 'gender' => $resolved['gender']]);
            }
            if ($term->icon_path) {
                Storage::disk('public')->delete($term->icon_path);
            }
            $extension = Str::lower(pathinfo($path, PATHINFO_EXTENSION)) === 'jpeg' ? 'jpg' : Str::lower(pathinfo($path, PATHINFO_EXTENSION));
            $term->icon_path = 'glossary/'.Str::uuid().'.'.$extension;
            Storage::disk('public')->put($term->icon_path, file_get_contents($path));
            $term->save();
            Glossary::flush($courseId);
        }

        $this->table(['Archivo', 'Personaje', ''], $rows);
        if ($this->option('apply')) {
            Glossary::flush(null);
            $this->info('Listo: imágenes cargadas en el Diccionario.');
        } else {
            $this->comment('Para guardar, repetí el comando con --apply.');
        }

        return self::SUCCESS;
    }
}
