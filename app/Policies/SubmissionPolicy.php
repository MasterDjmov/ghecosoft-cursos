<?php

namespace App\Policies;

use App\Models\Submission;
use App\Models\User;
use App\Services\TeacherScope;

class SubmissionPolicy
{
    public function __construct(private readonly TeacherScope $scope) {}

    /**
     * Una entrega la ve su autor, el docente de su comisión en ese curso (D72) y el administrador
     * (por Gate::before). Nunca otro alumno.
     */
    public function view(User $user, Submission $submission): bool
    {
        return $submission->user_id === $user->id || $this->review($user, $submission);
    }

    /** Comentar en el hilo: el autor de la entrega y quien la corrige. */
    public function comment(User $user, Submission $submission): bool
    {
        return $this->view($user, $submission);
    }

    /** Corregir (aprobar, pedir rehacer): el docente de la comisión del alumno en ese curso. */
    public function review(User $user, Submission $submission): bool
    {
        return $user->isTeacher() && $this->scope->canSeeSubmission($user, $submission);
    }
}
