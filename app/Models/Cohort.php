<?php

namespace App\Models;

use App\Enums\Modality;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable(['course_id', 'name', 'modality', 'schedule_text', 'starts_on', 'is_open_for_enrollment'])]
class Cohort extends Model
{
    /** Mismos valores por defecto que la base. */
    protected $attributes = ['modality' => 'virtual', 'is_open_for_enrollment' => true];

    protected function casts(): array
    {
        return [
            'modality' => Modality::class,
            'starts_on' => 'date',
            'is_open_for_enrollment' => 'boolean',
        ];
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }
}
