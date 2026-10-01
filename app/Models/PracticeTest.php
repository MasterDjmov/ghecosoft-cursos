<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** Prueba extra de una práctica (D73): solo del docente, nunca llega a una vista del alumno. */
#[Fillable(['practice_id', 'position', 'name', 'input', 'expected_output'])]
class PracticeTest extends Model
{
    /** Mismos valores por defecto que la base. */
    protected $attributes = ['position' => 0];

    protected function casts(): array
    {
        return ['position' => 'integer'];
    }

    public function practice(): BelongsTo
    {
        return $this->belongsTo(Practice::class);
    }
}
