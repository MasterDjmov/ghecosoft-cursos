<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Support\Facades\Storage;

#[Fillable(['code', 'course_id', 'name', 'description', 'icon'])]
class Badge extends Model
{
    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }

    /** Jefes que entregan esta insignia. */
    public function nodes(): HasMany
    {
        return $this->hasMany(Node::class);
    }

    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class, 'user_badges')->withPivot('awarded_at');
    }

    public function iconUrl(): ?string
    {
        return $this->icon ? Storage::disk('public')->url($this->icon) : null;
    }
}
