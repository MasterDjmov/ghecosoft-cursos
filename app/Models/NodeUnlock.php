<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable(['user_id', 'node_id', 'currency_id', 'price_paid', 'unlocked_at'])]
class NodeUnlock extends Model
{
    public $timestamps = false;

    protected function casts(): array
    {
        return ['unlocked_at' => 'datetime', 'price_paid' => 'integer'];
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function node(): BelongsTo
    {
        return $this->belongsTo(Node::class);
    }
}
