<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** D73: un comentario guardado de un docente, para insertarlo al corregir. Sin curso, sale en todos los suyos. */
#[Fillable(['user_id', 'course_id', 'body', 'position'])]
class ReviewSnippet extends Model
{
    protected $attributes = ['position' => 0];

    /** Los de un docente que sirven para un curso: los de ese curso y los de todos. */
    public function scopeFor(Builder $query, User $user, int $courseId): void
    {
        $query->where('user_id', $user->id)
            ->where(fn (Builder $q) => $q->whereNull('course_id')->orWhere('course_id', $courseId))
            ->orderBy('position')->orderBy('id');
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }
}
