<?php

namespace App\Policies;

use App\Models\Submission;
use App\Models\User;

class SubmissionPolicy
{
    /** Una entrega la ve su autor (y el docente, por Gate::before). Nunca otro alumno. */
    public function view(User $user, Submission $submission): bool
    {
        return $submission->user_id === $user->id;
    }

    /** Comentar en el hilo: el autor de la entrega (y el docente). */
    public function comment(User $user, Submission $submission): bool
    {
        return $submission->user_id === $user->id;
    }
}
