<?php

namespace App\Actions\Fortify;

use App\Concerns\PasswordValidationRules;
use App\Concerns\ProfileValidationRules;
use App\Models\User;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Str;
use Illuminate\Validation\ValidationException;
use Laravel\Fortify\Contracts\CreatesNewUsers;

class CreateNewUser implements CreatesNewUsers
{
    use PasswordValidationRules, ProfileValidationRules;

    /**
     * Crea un alumno desde el formulario público. El rol nunca viene del formulario.
     *
     * @param  array<string, string>  $input
     */
    public function create(array $input): User
    {
        $throttleKey = 'register:'.request()->ip();
        if (RateLimiter::tooManyAttempts($throttleKey, 6)) {
            throw ValidationException::withMessages([
                'email' => __('Too many login attempts. Please try again in :seconds seconds.', ['seconds' => RateLimiter::availableIn($throttleKey)]),
            ]);
        }
        RateLimiter::hit($throttleKey, 60);

        $input['username'] = Str::lower(trim($input['username'] ?? ''));
        $input['email'] = Str::lower(trim($input['email'] ?? '')) ?: null;
        $input['phone'] = trim($input['phone'] ?? '') ?: null;

        Validator::make($input, [
            ...$this->profileRules(),
            'password' => $this->passwordRules(),
        ], $this->profileMessages())->validate();

        return User::create([
            'name' => $input['name'],
            'last_name' => $input['last_name'],
            'username' => $input['username'],
            'email' => $input['email'],
            'phone' => $input['phone'],
            'password' => $input['password'],
        ]);
    }
}
