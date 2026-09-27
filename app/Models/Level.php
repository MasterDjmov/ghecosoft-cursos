<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;

#[Fillable(['number', 'xp_required'])]
class Level extends Model
{
    /** Nombre del rango: el del diccionario (level.{n}) o "Nivel n". */
    public function name(): string
    {
        return term('level.'.$this->number);
    }

    public static function forXp(int $xp): ?self
    {
        return static::where('xp_required', '<=', $xp)->orderByDesc('number')->first();
    }
}
