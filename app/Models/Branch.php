<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

#[Fillable(['course_id', 'title', 'position', 'is_extra'])]
class Branch extends Model
{
    /** Mismos valores por defecto que la base. */
    protected $attributes = ['position' => 0, 'is_extra' => false];

    protected function casts(): array
    {
        return ['is_extra' => 'boolean'];
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
