<?php

namespace App\Policies;

use App\Models\Practice;
use App\Models\User;
use App\Services\TeacherScope;
use App\Services\TreeAccess;

/**
 * Consultas por práctica (D63). El docente ve y responde todo (Gate::before).
 * Un alumno solo ve su propio hilo, y solo de prácticas de nodos que abrió.
 */
class PracticeMessagePolicy
{
    public function __construct(private readonly TreeAccess $access) {}

    public function viewThread(User $user, Practice $practice, User $student): bool
    {
        // El docente de la comisión del alumno en ese curso (D72) ve y responde su hilo.
        if ($user->isTeacher()) {
            return app(TeacherScope::class)->teachesPractice($user, $student, $practice);
        }

        // isUnlocked, no canView: la Clase 0 de prueba (D71) no abre consultas al profe.
        return $user->id === $student->id && $this->access->isUnlocked($user, $practice->node);
    }

    /** Escribir, además, pide el abono vigente (como entregar). */
    public function send(User $user, Practice $practice, User $student): bool
    {
        if ($user->isTeacher()) {
            return $this->viewThread($user, $practice, $student);
        }

        return $this->viewThread($user, $practice, $student)
            && $this->access->hasActiveSubscription($user, $practice->node->course);
    }
}
