<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** D107: un intento de una micro-misión (acierto o fallo), lo anota `ActivityLog`. */
#[Fillable(['user_id', 'node_step_id', 'node_id', 'course_id', 'passed', 'kind', 'answer', 'code', 'created_at'])]
class StepAttempt extends Model
{
    public const UPDATED_AT = null;

    protected $attributes = ['passed' => false];

    protected function casts(): array
    {
        return ['passed' => 'boolean', 'created_at' => 'datetime'];
    }

    /** El tipo de error, en palabras del docente. */
    public function kindLabel(): ?string
    {
        return match ($this->kind) {
            null => null,
            'output' => 'salida distinta',
            'checks' => 'le falta algo',
            'error' => 'error al ejecutar',
            'almost' => 'casi (una letra)',
            'bad' => 'mal',
            default => $this->kind,
        };
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function step(): BelongsTo
    {
        return $this->belongsTo(NodeStep::class, 'node_step_id');
    }
}
