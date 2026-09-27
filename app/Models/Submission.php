<?php

namespace App\Models;

use App\Enums\SubmissionStatus;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

#[Fillable(['practice_id', 'user_id', 'attempt', 'code', 'file_path', 'file_original_name', 'submitted_at'])]
class Submission extends Model
{
    /** Mismos valores por defecto que la base. */
    protected $attributes = ['attempt' => 1, 'status' => 'submitted'];

    protected function casts(): array
    {
        return [
            'status' => SubmissionStatus::class,
            'submitted_at' => 'datetime',
            'reviewed_at' => 'datetime',
        ];
    }

    public function practice(): BelongsTo
    {
        return $this->belongsTo(Practice::class);
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function reviewer(): BelongsTo
    {
        return $this->belongsTo(User::class, 'reviewed_by');
    }

    public function comments(): HasMany
    {
        return $this->hasMany(SubmissionComment::class)->oldest();
    }
}
