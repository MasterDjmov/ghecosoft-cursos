<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** D95: las prácticas de un nodo abiertas por el docente antes de que el alumno termine las micro-misiones. */
#[Fillable(['user_id', 'node_id', 'granted_by'])]
class PracticeGrant extends Model
{
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function node(): BelongsTo
    {
        return $this->belongsTo(Node::class);
    }
}
