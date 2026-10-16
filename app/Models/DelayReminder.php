<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** Un aviso a un alumno demorado en un curso (la copia interna del mail). */
#[Fillable(['user_id', 'course_id', 'sent_by', 'body', 'created_at'])]
class DelayReminder extends Model
{
    public $timestamps = false;

    protected function casts(): array
    {
        return ['created_at' => 'datetime'];
    }

    public function student(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id');
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }

    public function sender(): BelongsTo
    {
        return $this->belongsTo(User::class, 'sent_by');
    }
}
