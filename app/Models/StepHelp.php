<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** D123: una ayuda que pidió un alumno en una micro-misión; la anota `App\Services\StepHelper`. */
#[Fillable(['user_id', 'node_step_id', 'course_id', 'kind', 'line', 'created_at'])]
class StepHelp extends Model
{
    public const UPDATED_AT = null;

    /** Lo que se puede anotar, con su nombre para el docente. */
    public const KINDS = [
        'offer' => 'Gheco le ofreció ayuda',
        'read' => 'escuchó el desafío',
        'guide' => '¿Qué me piden?',
        'where' => '¿Dónde toco?',
        'compare' => 'Comparemos',
        'line' => 'vio una línea de la solución',
    ];

    protected function casts(): array
    {
        return ['line' => 'integer', 'created_at' => 'datetime'];
    }

    public function step(): BelongsTo
    {
        return $this->belongsTo(NodeStep::class, 'node_step_id');
    }
}
