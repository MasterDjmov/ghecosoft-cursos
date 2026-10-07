<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** Lo que el jugador está fabricando en el taller (D93). */
#[Fillable(['user_id', 'recipe', 'item_id', 'quantity', 'started_at', 'ends_at', 'collected_at'])]
class Craft extends Model
{
    protected function casts(): array
    {
        return ['started_at' => 'datetime', 'ends_at' => 'datetime', 'collected_at' => 'datetime', 'quantity' => 'integer'];
    }

    public function item(): BelongsTo
    {
        return $this->belongsTo(Item::class);
    }

    public function isReady(): bool
    {
        return $this->collected_at === null && now()->greaterThanOrEqualTo($this->ends_at);
    }
}
