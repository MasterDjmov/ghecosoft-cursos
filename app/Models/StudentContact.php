<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** Un mensaje del docente a un alumno desde *Alumnos* (lo manda `App\Services\StudentAccounts::contact`). */
#[Fillable(['user_id', 'sent_by', 'body', 'created_at'])]
class StudentContact extends Model
{
    public const UPDATED_AT = null;

    protected function casts(): array
    {
        return ['created_at' => 'datetime'];
    }

    public function sender(): BelongsTo
    {
        return $this->belongsTo(User::class, 'sent_by');
    }
}
