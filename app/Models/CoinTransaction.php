<?php

namespace App\Models;

use App\Enums\CoinReason;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\MorphTo;

/** Solo lo escribe App\Services\Ledger. */
#[Fillable(['user_id', 'currency_id', 'amount', 'reason', 'course_id', 'source_type', 'source_id', 'note', 'created_by'])]
class CoinTransaction extends Model
{
    public const UPDATED_AT = null;

    protected function casts(): array
    {
        return ['reason' => CoinReason::class, 'amount' => 'integer'];
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function currency(): BelongsTo
    {
        return $this->belongsTo(Currency::class);
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
