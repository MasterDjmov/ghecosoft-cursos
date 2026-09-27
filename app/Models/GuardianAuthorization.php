<?php

namespace App\Models;

use App\Enums\AuthorizationStatus;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable(['user_id', 'file_path', 'original_name'])]
class GuardianAuthorization extends Model
{
    /** Mismos valores por defecto que la base. */
    protected $attributes = ['status' => 'pending'];

    protected function casts(): array
    {
        return ['status' => AuthorizationStatus::class, 'reviewed_at' => 'datetime'];
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
