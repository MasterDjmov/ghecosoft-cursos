<?php

namespace App\Policies;

use App\Models\Practice;
use App\Models\User;
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
        return $user->id === $student->id && $this->access->canView($user, $practice->node);
    }

    /** Escribir, además, pide el abono vigente (como entregar). */
    public function send(User $user, Practice $practice, User $student): bool
    {
        return $this->viewThread($user, $practice, $student)
            && $this->access->hasActiveSubscription($user, $practice->node->course);
    }
}
