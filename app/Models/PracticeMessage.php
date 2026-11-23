<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/**
 * Un mensaje del hilo de consultas de un alumno sobre una práctica (D63), una micro-misión (D110) o una práctica
 * guardada en Mis prácticas (D124). Los del alumno
 * guardan la foto del código que tenía en el editor y de lo que le dio al ejecutar.
 */
#[Fillable(['practice_id', 'node_step_id', 'saved_practice_id', 'student_id', 'author_id', 'body', 'code', 'output', 'read_at'])]
class PracticeMessage extends Model
{
    protected function casts(): array
    {
        return ['read_at' => 'datetime'];
    }

    public function practice(): BelongsTo
    {
        return $this->belongsTo(Practice::class)->withoutGlobalScope(Practice::ACTIVE);
    }

    public function nodeStep(): BelongsTo
    {
        return $this->belongsTo(NodeStep::class);
    }

    public function savedPractice(): BelongsTo
    {
        return $this->belongsTo(SavedPractice::class);
    }

    public function student(): BelongsTo
    {
        return $this->belongsTo(User::class, 'student_id');
    }

    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'author_id');
    }

    /** De qué es la consulta: la práctica, la micro-misión o la práctica guardada. */
    public function subject(): Practice|NodeStep|SavedPractice|null
    {
        return $this->practice ?? $this->nodeStep ?? $this->savedPractice;
    }

    /** La columna del hilo según de qué es la consulta. */
    public static function subjectColumn(Practice|NodeStep|SavedPractice $subject): string
    {
        return match (true) {
            $subject instanceof Practice => 'practice_id',
            $subject instanceof NodeStep => 'node_step_id',
            default => 'saved_practice_id',
        };
    }

    public function scopeThread(Builder $query, Practice|NodeStep|SavedPractice $subject, User $student): void
    {
        $query->where(self::subjectColumn($subject), $subject->id)->where('student_id', $student->id);
    }

    /** Mensajes que $viewer todavía no leyó: los que escribió el otro lado. */
    public function scopeUnreadFor(Builder $query, User $viewer): void
    {
        $query->whereNull('read_at')->where('author_id', '!=', $viewer->id);
    }

    /** La clave del hilo en Admin → Mensajes: «idPráctica-idAlumno», «m idMicroMisión-idAlumno» o «p idGuardada-idAlumno». */
    public static function threadKey(Practice|NodeStep|SavedPractice $subject, User|int $student): string
    {
        $studentId = $student instanceof User ? $student->id : $student;
        $prefix = match (true) {
            $subject instanceof NodeStep => 'm',
            $subject instanceof SavedPractice => 'p',
            default => '',
        };

        return $prefix.$subject->id.'-'.$studentId;
    }

    /**
     * Lo contrario de threadKey.
     *
     * @return array{0: Practice|NodeStep|SavedPractice|null, 1: User|null}
     */
    public static function fromThreadKey(string $key): array
    {
        if (! preg_match('/^([mp]?)(\d+)-(\d+)$/', $key, $m)) {
            return [null, null];
        }
        $student = User::find((int) $m[3]);
        $subject = match ($m[1]) {
            'm' => NodeStep::with('node.course')->find((int) $m[2]),
            // La práctica guardada tiene que ser de ese alumno.
            'p' => SavedPractice::where('user_id', (int) $m[3])->find((int) $m[2]),
            default => Practice::with('node.course')->find((int) $m[2]),
        };

        return [$subject, $student];
    }
}
