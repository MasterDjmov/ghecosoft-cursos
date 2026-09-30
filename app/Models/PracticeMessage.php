<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** Un mensaje del hilo de consultas de un alumno sobre una práctica (D63). */
#[Fillable(['practice_id', 'student_id', 'author_id', 'body', 'read_at'])]
class PracticeMessage extends Model
{
    protected function casts(): array
    {
        return ['read_at' => 'datetime'];
    }

    public function practice(): BelongsTo
    {
        return $this->belongsTo(Practice::class);
    }

    public function student(): BelongsTo
    {
        return $this->belongsTo(User::class, 'student_id');
    }

    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'author_id');
    }

    public function scopeThread(Builder $query, Practice $practice, User $student): void
    {
        $query->where('practice_id', $practice->id)->where('student_id', $student->id);
    }

    /** Mensajes que $viewer todavía no leyó: los que escribió el otro lado. */
    public function scopeUnreadFor(Builder $query, User $viewer): void
    {
        $query->whereNull('read_at')->where('author_id', '!=', $viewer->id);
    }
}
