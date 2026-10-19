<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/**
 * Un mensaje del hilo de consultas de un alumno sobre una práctica (D63) o una micro-misión (D110). Los del alumno
 * guardan la foto del código que tenía en el editor y de lo que le dio al ejecutar.
 */
#[Fillable(['practice_id', 'node_step_id', 'student_id', 'author_id', 'body', 'code', 'output', 'read_at'])]
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

    public function nodeStep(): BelongsTo
    {
        return $this->belongsTo(NodeStep::class);
    }

    public function student(): BelongsTo
    {
        return $this->belongsTo(User::class, 'student_id');
    }

    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'author_id');
    }

    /** De qué es la consulta: la práctica o la micro-misión. */
    public function subject(): Practice|NodeStep|null
    {
        return $this->practice ?? $this->nodeStep;
    }

    public function scopeThread(Builder $query, Practice|NodeStep $subject, User $student): void
    {
        $query->where($subject instanceof Practice ? 'practice_id' : 'node_step_id', $subject->id)->where('student_id', $student->id);
    }

    /** Mensajes que $viewer todavía no leyó: los que escribió el otro lado. */
    public function scopeUnreadFor(Builder $query, User $viewer): void
    {
        $query->whereNull('read_at')->where('author_id', '!=', $viewer->id);
    }

    /** La clave del hilo en Admin → Mensajes: «idPráctica-idAlumno» o «m idMicroMisión-idAlumno». */
    public static function threadKey(Practice|NodeStep $subject, User|int $student): string
    {
        $studentId = $student instanceof User ? $student->id : $student;

        return ($subject instanceof NodeStep ? 'm' : '').$subject->id.'-'.$studentId;
    }

    /**
     * Lo contrario de threadKey.
     *
     * @return array{0: Practice|NodeStep|null, 1: User|null}
     */
    public static function fromThreadKey(string $key): array
    {
        if (! preg_match('/^(m?)(\d+)-(\d+)$/', $key, $m)) {
            return [null, null];
        }
        $subject = $m[1] === 'm' ? NodeStep::with('node.course')->find((int) $m[2]) : Practice::with('node.course')->find((int) $m[2]);

        return [$subject, User::find((int) $m[3])];
    }
}
