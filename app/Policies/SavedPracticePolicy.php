<?php

namespace App\Policies;

use App\Models\SavedPractice;
use App\Models\User;

/**
 * D124: cada uno ve, cambia y borra solo sus prácticas guardadas (también el administrador: Gate::before lo exceptúa). El
 * docente ve el código de un alumno solo cuando le consulta, en Admin → Mensajes (PracticeMessagePolicy).
 */
class SavedPracticePolicy
{
    public function view(User $user, SavedPractice $practice): bool
    {
        return $practice->user_id === $user->id;
    }

    public function update(User $user, SavedPractice $practice): bool
    {
        return $practice->user_id === $user->id;
    }

    public function delete(User $user, SavedPractice $practice): bool
    {
        return $practice->user_id === $user->id;
    }
}
