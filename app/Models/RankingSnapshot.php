<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;

/** Posición de un alumno en el ranking global en un día (la primera carga del día). */
#[Fillable(['taken_on', 'user_id', 'position'])]
class RankingSnapshot extends Model
{
    public $timestamps = false;

    protected function casts(): array
    {
        return ['taken_on' => 'date', 'position' => 'integer'];
    }
}
