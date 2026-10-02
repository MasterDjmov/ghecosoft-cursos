<?php

namespace App\Models;

use App\Enums\FragmentTrigger;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Facades\Storage;

/** Un trozo extra de historia de Mis Crónicas (D80, etapa 2), con imagen opcional. */
#[Fillable(['course_id', 'node_id', 'branch_id', 'trigger', 'title', 'body', 'image_path', 'position'])]
class StoryFragment extends Model
{
    protected $attributes = ['position' => 0];

    protected function casts(): array
    {
        return ['trigger' => FragmentTrigger::class];
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }

    public function node(): BelongsTo
    {
        return $this->belongsTo(Node::class);
    }

    public function imageUrl(): ?string
    {
        return $this->image_path ? Storage::disk('public')->url($this->image_path) : null;
    }
}
