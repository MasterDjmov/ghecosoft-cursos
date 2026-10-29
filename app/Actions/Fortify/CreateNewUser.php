<?php

namespace App\Actions\Fortify;

use App\Concerns\PasswordValidationRules;
use App\Concerns\ProfileValidationRules;
use App\Models\User;
use App\Support\Maintenance;
use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Str;
use Illuminate\Validation\ValidationException;
use Laravel\Fortify\Contracts\CreatesNewUsers;
use Throwable;

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
        // Plataforma en mantenimiento (D86): no se crean cuentas nuevas.
        if (Maintenance::platform()) {
            throw ValidationException::withMessages(['email' => Maintenance::message()]);
        }
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
            'terms' => ['accepted'],
            // D114: la fecha dice quién es menor; menos de 13, el acuerdo de su adulto responsable.
            'birth_date' => ['required', 'date', 'before:today', 'after:1900-01-01'],
            'guardian_consent' => self::needsGuardianConsent($input['birth_date'] ?? null) ? ['accepted'] : ['nullable'],
        ], [
            ...$this->profileMessages(),
            'terms.accepted' => 'Para crear la cuenta tenés que aceptar los Términos y la Política de privacidad.',
            'birth_date.required' => 'Contanos tu fecha de nacimiento.',
            'birth_date.before' => 'La fecha de nacimiento tiene que ser anterior a hoy.',
            'guardian_consent.accepted' => 'Como tenés menos de '.User::GUARDIAN_CONSENT_AGE.' años, tu adulto responsable tiene que estar de acuerdo.',
        ])->validate();

        $user = User::create([
            'name' => $input['name'],
            'last_name' => $input['last_name'],
            'username' => $input['username'],
            'email' => $input['email'],
            'phone' => $input['phone'],
            'birth_date' => $input['birth_date'],
            'password' => $input['password'],
        ]);

        // D112: qué versión de los Términos y la Privacidad aceptó, y cuándo.
        $user->forceFill([
            'terms_accepted_at' => now(),
            'terms_version' => config('legal.version'),
            'guardian_consent_at' => self::needsGuardianConsent($input['birth_date']) ? now() : null,
        ])->save();

        return $user;
    }

    private static function needsGuardianConsent(mixed $birthDate): bool
    {
        try {
            return is_string($birthDate) && $birthDate !== '' && Carbon::parse($birthDate)->age < User::GUARDIAN_CONSENT_AGE;
        } catch (Throwable) {
            return false;
        }
    }
}
