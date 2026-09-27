<?php

namespace App\Models;

use App\Enums\ResourceType;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable(['node_id', 'type', 'title', 'url', 'file_path', 'original_name', 'position'])]
class NodeResource extends Model
{
    protected function casts(): array
    {
        return ['type' => ResourceType::class];
    }

    public function node(): BelongsTo
    {
        return $this->belongsTo(Node::class);
    }
}
