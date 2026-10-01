<?php

namespace App\Support;

use App\Models\Setting;

/** Tamaño de los retratos del Diccionario en los nodos (se elige en Admin → Diccionario). */
class Portraits
{
    public const DEFAULTS = ['portrait_companion_px' => 48, 'portrait_beast_px' => 80];

    /** La compañía y la mentora. */
    public static function companion(): int
    {
        return self::size('portrait_companion_px');
    }

    /** Las criaturas del bestiario. */
    public static function beast(): int
    {
        return self::size('portrait_beast_px');
    }

    private static function size(string $key): int
    {
        return max(24, min(200, (int) Setting::get($key, (string) self::DEFAULTS[$key])));
    }
}
