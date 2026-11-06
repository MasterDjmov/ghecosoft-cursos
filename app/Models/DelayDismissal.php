<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;

/** Un alumno quitado a mano de la lista de demorados de un curso (hasta que vuelva a avanzar o renueve). */
#[Fillable(['user_id', 'course_id', 'dismissed_by', 'created_at'])]
class DelayDismissal extends Model
{
    public $timestamps = false;

    protected function casts(): array
    {
        return ['created_at' => 'datetime'];
    }
}
