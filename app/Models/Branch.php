<?php

namespace App\Models;

use App\Enums\BranchKind;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

#[Fillable(['course_id', 'code', 'title', 'kind', 'position', 'is_extra'])]
class Branch extends Model
{
    /** Mismos valores por defecto que la base. */
    protected $attributes = ['position' => 0, 'kind' => 'trunk', 'is_extra' => false];

    protected function casts(): array
    {
        return ['is_extra' => 'boolean', 'kind' => BranchKind::class];
    }

    /** `kind` manda; `is_extra` queda como "no es tronco". Si solo se tocó `is_extra`, se deduce el tipo. */
    protected static function booted(): void
    {
        static::saving(function (Branch $branch) {
            if ($branch->isDirty('kind') || ! $branch->isDirty('is_extra')) {
                $branch->is_extra = $branch->kind->isOptional();
            } else {
                $branch->kind = $branch->is_extra ? BranchKind::Extra : BranchKind::Trunk;
            }
        });
    }

    public function isPath(): bool
    {
        return $this->kind === BranchKind::Path;
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }

    public function nodes(): HasMany
    {
        return $this->hasMany(Node::class)->orderBy('position');
    }
}
