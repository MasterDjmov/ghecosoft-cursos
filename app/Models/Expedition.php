<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** Una expedición del héroe (D91). Se crea y se resuelve solo con `App\Services\Expeditions`. */
#[Fillable(['user_id', 'hero_id', 'course_id', 'place', 'length', 'started_at', 'ends_at', 'resolved_at', 'won', 'log', 'rewards'])]
class Expedition extends Model
{
    protected function casts(): array
    {
        return [
            'started_at' => 'datetime',
            'ends_at' => 'datetime',
            'resolved_at' => 'datetime',
            'won' => 'boolean',
            'log' => 'array',
            'rewards' => 'array',
        ];
    }

    public function isReady(): bool
    {
        return $this->resolved_at === null && now()->greaterThanOrEqualTo($this->ends_at);
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function hero(): BelongsTo
    {
        return $this->belongsTo(Hero::class);
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }
}
