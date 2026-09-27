<?php

namespace App\Models;

use App\Enums\RequestKind;
use App\Enums\RequestStatus;
use App\Enums\RequestType;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable(['user_id', 'course_id', 'cohort_id', 'kind', 'type', 'receipt_path', 'receipt_original_name', 'message'])]
class EnrollmentRequest extends Model
{
    /** Mismos valores por defecto que la base. */
    protected $attributes = ['kind' => 'new', 'type' => 'receipt', 'status' => 'pending'];

    protected function casts(): array
    {
        return [
            'kind' => RequestKind::class,
            'type' => RequestType::class,
            'status' => RequestStatus::class,
            'reviewed_at' => 'datetime',
        ];
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }

    public function cohort(): BelongsTo
    {
        return $this->belongsTo(Cohort::class);
    }
}
