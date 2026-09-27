<?php

namespace App\Policies;

use App\Models\EnrollmentRequest;
use App\Models\User;

class EnrollmentRequestPolicy
{
    /** El comprobante lo ve quien lo subió (y el docente, por Gate::before). */
    public function view(User $user, EnrollmentRequest $request): bool
    {
        return $request->user_id === $user->id;
    }
}
