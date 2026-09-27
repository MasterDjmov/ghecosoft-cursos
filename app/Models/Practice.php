<?php

namespace App\Models;

use App\Enums\SubmissionMode;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

#[Fillable(['node_id', 'title', 'instructions', 'is_required', 'submission_mode', 'allowed_extensions', 'starter_code', 'sample_input', 'coin_reward', 'xp_reward', 'position'])]
class Practice extends Model
{
    /** Mismos valores por defecto que la base. */
    protected $attributes = ['is_required' => true, 'submission_mode' => 'code', 'coin_reward' => 0, 'xp_reward' => 0, 'position' => 0];

    protected function casts(): array
    {
        return [
            'is_required' => 'boolean',
            'submission_mode' => SubmissionMode::class,
            'coin_reward' => 'integer',
            'xp_reward' => 'integer',
        ];
    }

    public function node(): BelongsTo
    {
        return $this->belongsTo(Node::class);
    }

    public function hasStudentActivity(): bool
    {
        return $this->submissions()->exists() || PracticeMark::where('practice_id', $this->id)->exists();
    }

    public function submissions(): HasMany
    {
        return $this->hasMany(Submission::class);
    }
}
