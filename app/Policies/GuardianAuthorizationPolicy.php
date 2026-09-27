<?php

namespace App\Policies;

use App\Models\GuardianAuthorization;
use App\Models\User;

class GuardianAuthorizationPolicy
{
    /** La nota firmada la ve quien la subió (y el docente, por Gate::before). */
    public function view(User $user, GuardianAuthorization $authorization): bool
    {
        return $authorization->user_id === $user->id;
    }
}
