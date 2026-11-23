<?php

namespace App\Policies;

use App\Models\CourseSubscription;
use App\Models\NodeStep;
use App\Models\Practice;
use App\Models\SavedPractice;
use App\Models\User;
use App\Services\TeacherScope;
use App\Services\TreeAccess;

/**
 * Consultas por práctica (D63), por micro-misión (D110) y por práctica guardada (D124). El administrador ve y
 * responde todo (Gate::before). Un alumno solo ve su propio hilo, y solo de prácticas o micro-misiones de nodos
 * que abrió, o de sus prácticas guardadas.
 */
class PracticeMessagePolicy
{
    public function __construct(private readonly TreeAccess $access) {}

    public function viewThread(User $user, Practice|NodeStep|SavedPractice $subject, User $student): bool
    {
        // D124: la práctica guardada no es de un curso: la ve el docente de cualquier comisión del alumno.
        if ($subject instanceof SavedPractice) {
            if ($subject->user_id !== $student->id) {
                return false;
            }

            return $user->isTeacher() ? app(TeacherScope::class)->teaches($user, $student) : $user->id === $student->id;
        }

        // El docente de la comisión del alumno en ese curso (D72) ve y responde su hilo.
        if ($user->isTeacher()) {
            return app(TeacherScope::class)->teaches($user, $student, $subject->node->course);
        }

        // isUnlocked, no canView: la Clase 0 de prueba (D71) no abre consultas al profe.
        return $user->id === $student->id && $this->access->isUnlocked($user, $subject->node);
    }

    /** Escribir, además, pide el abono vigente (como entregar); por una práctica guardada, el de algún curso. */
    public function send(User $user, Practice|NodeStep|SavedPractice $subject, User $student): bool
    {
        if ($user->isTeacher()) {
            return $this->viewThread($user, $subject, $student);
        }
        if (! $this->viewThread($user, $subject, $student)) {
            return false;
        }

        return $subject instanceof SavedPractice
            ? CourseSubscription::active()->where('user_id', $user->id)->exists()
            : $this->access->hasActiveSubscription($user, $subject->node->course);
    }
}
