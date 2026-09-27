<?php

namespace App\Models;

use App\Enums\XpReason;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\MorphTo;

/** Solo lo escribe App\Services\Ledger. */
#[Fillable(['user_id', 'amount', 'reason', 'course_id', 'source_type', 'source_id', 'note', 'created_by'])]
class XpTransaction extends Model
{
    public const UPDATED_AT = null;

    protected function casts(): array
    {
        return ['reason' => XpReason::class, 'amount' => 'integer'];
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function source(): MorphTo
    {
        return $this->morphTo();
    }

    /** Quién hizo el movimiento (el docente en ajustes y correcciones). */
    public function creator(): BelongsTo
    {
        return $this->belongsTo(User::class, 'created_by');
    }
}
