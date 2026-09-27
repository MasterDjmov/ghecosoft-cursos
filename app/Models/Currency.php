<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable(['code', 'course_id', 'is_wildcard'])]
class Currency extends Model
{
    public const WILDCARD = 'wildcard';

    protected function casts(): array
    {
        return ['is_wildcard' => 'boolean'];
    }

    public static function wildcard(): self
    {
        return static::firstOrCreate(['code' => self::WILDCARD], ['is_wildcard' => true]);
    }

    public static function forCourse(Course $course): self
    {
        return static::firstOrCreate(['course_id' => $course->id], ['code' => 'course-'.$course->slug]);
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }
}
