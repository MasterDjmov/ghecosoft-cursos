<?php

namespace App\Support;

use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
use InvalidArgumentException;

/**
 * «Así tiene que quedar» (D77): las capturas de una práctica de HTML y CSS. Se guardan en el disco público
 * con el nombre que sale de su contenido: la misma imagen siempre queda en el mismo archivo, así que
 * reimportar un curso no duplica nada.
 */
class PracticeReferences
{
    public const EXTENSIONS = ['png', 'jpg', 'jpeg', 'webp'];

    /** Una captura de una página larga en el celular puede ser alta, pero no pesada. */
    public const MAX_KB = 3072;

    /** Revisa que el archivo sea una imagen de verdad (el contenido, no solo la extensión). */
    public static function check(string $path, ?string $extension = null): ?string
    {
        $extension = Str::lower($extension ?? pathinfo($path, PATHINFO_EXTENSION));

        return match (true) {
            ! is_file($path) || ! is_readable($path) => 'no se encuentra',
            ! in_array($extension, self::EXTENSIONS, true) => 'tiene que ser PNG, JPG o WebP',
            filesize($path) > self::MAX_KB * 1024 => 'pesa más de '.self::MAX_KB.' KB',
            ! in_array(@getimagesize($path)[2] ?? null, [IMAGETYPE_PNG, IMAGETYPE_JPEG, IMAGETYPE_WEBP], true) => 'no es una imagen válida',
            default => null,
        };
    }

    /** Copia la imagen al disco público y devuelve su ruta (practice-refs/<sha1>.<ext>). */
    public static function store(string $path, ?string $extension = null): string
    {
        if ($problem = self::check($path, $extension)) {
            throw new InvalidArgumentException(basename($path).': '.$problem);
        }
        $extension = Str::lower($extension ?? pathinfo($path, PATHINFO_EXTENSION));
        $target = 'practice-refs/'.sha1_file($path).'.'.($extension === 'jpeg' ? 'jpg' : $extension);
        if (! Storage::disk('public')->exists($target)) {
            Storage::disk('public')->put($target, file_get_contents($path));
        }

        return $target;
    }
}
