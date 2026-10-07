<?php

namespace App\Models;

use App\Enums\ItemReason;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\MorphTo;

/** Un movimiento de la mochila (D90): la cantidad de un ítem es la suma. Se escribe solo con `Inventory`. */
#[Fillable(['user_id', 'item_id', 'quantity', 'reason', 'source_type', 'source_id', 'note', 'created_by'])]
class ItemMovement extends Model
{
    protected function casts(): array
    {
        return ['quantity' => 'integer', 'reason' => ItemReason::class];
    }

    public function item(): BelongsTo
    {
        return $this->belongsTo(Item::class);
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function source(): MorphTo
    {
        return $this->morphTo();
    }
}
