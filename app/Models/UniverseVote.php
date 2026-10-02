<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** «Quiero aprender esto» (D81): el voto de un alumno a un tema o a un curso que viene. */
#[Fillable(['user_id', 'target'])]
class UniverseVote extends Model
{
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
