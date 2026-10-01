<?php

namespace App\Console\Commands;

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
 */
#[Signature('app:glossary-portraits {path : Carpeta con las imágenes} {--apply : Guardar (sin esto, solo muestra qué haría)}')]
#[Description('Carga los retratos de personajes y criaturas en el Diccionario general')]
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

        $rows = [];
        foreach ($images as $name => $path) {
            $key = self::FILES[$name] ?? null;
            if (! $key) {
                $rows[] = [basename($path), '—', 'no lo reconozco: se saltea'];

                continue;
            }
            if (filesize($path) > config('uploads.image.max_kb') * 1024) {
                $rows[] = [basename($path), $key, 'pesa más de '.config('uploads.image.max_kb').' KB: se saltea'];

                continue;
            }

            $term = GlossaryTerm::firstOrNew(['key' => $key, 'course_id' => null]);
            $resolved = $glossary->resolve($key);
            $rows[] = [basename($path), $key.' ('.$resolved['singular'].')', $term->icon_path ? 'reemplaza el retrato' : 'retrato nuevo'];
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
        }

        $this->table(['Archivo', 'Personaje', ''], $rows);
        if ($this->option('apply')) {
            Glossary::flush(null);
            $this->info('Listo: retratos cargados en el Diccionario general.');
        } else {
            $this->comment('Para guardar, repetí el comando con --apply.');
        }

        return self::SUCCESS;
    }
}
