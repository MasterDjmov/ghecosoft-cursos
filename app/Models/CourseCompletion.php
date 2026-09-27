<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable(['user_id', 'course_id', 'completed_at', 'days_taken'])]
class CourseCompletion extends Model
{
    public $timestamps = false;

    protected function casts(): array
    {
        return ['completed_at' => 'datetime'];
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }
}
