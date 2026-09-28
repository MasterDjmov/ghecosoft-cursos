<?php

namespace App\Concerns;

use App\Models\User;
use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Validation\Rule;

trait ProfileValidationRules
{
    /** Usuarios que no se pueden elegir al registrarse (rutas y roles). */
    public const RESERVED_USERNAMES = ['admin', 'administrador', 'root', 'docente', 'profe', 'cv', 'mundos', 'cursos', 'soporte', 'ghecosoft', 'nuevo'];

    /**
     * @return array<string, array<int, ValidationRule|array<mixed>|string>>
     */
    protected function profileRules(?int $userId = null): array
    {
        return [
            'name' => $this->nameRules(),
            'last_name' => $this->nameRules(),
            'username' => $this->usernameRules($userId),
            'email' => $this->emailRules($userId),
            'phone' => $this->phoneRules(),
        ];
    }

    /**
     * @return array<int, ValidationRule|array<mixed>|string>
     */
    protected function nameRules(): array
    {
        return ['required', 'string', 'max:255'];
    }

    /**
     * Usuario: minúsculas, números, guion y guion bajo. No se muestra en público: el CV tiene su propio link (cv_slug).
     *
     * @return array<int, ValidationRule|array<mixed>|string>
     */
    protected function usernameRules(?int $userId = null): array
    {
        return [
            'required',
            'string',
            'min:3',
            'max:30',
            'regex:/^[a-z0-9][a-z0-9_-]*$/',
            // Es el link del CV público: no puede ser un DNI (solo números).
            'not_regex:/^\d+$/',
            Rule::notIn(self::RESERVED_USERNAMES),
            $userId === null
                ? Rule::unique(User::class)
                : Rule::unique(User::class)->ignore($userId),
        ];
    }

    /**
     * Opcional (D36): hay alumnos sin email; el docente les crea la cuenta y les resetea la clave.
     *
     * @return array<int, ValidationRule|array<mixed>|string>
     */
    protected function emailRules(?int $userId = null): array
    {
        return [
            'nullable',
            'string',
            'email',
            'max:255',
            $userId === null
                ? Rule::unique(User::class)
                : Rule::unique(User::class)->ignore($userId),
        ];
    }

    /**
     * Teléfono opcional, para que el profe pueda escribirle por WhatsApp.
     *
     * @return array<int, ValidationRule|array<mixed>|string>
     */
    protected function phoneRules(): array
    {
        return ['nullable', 'string', 'max:25', 'regex:/^\+?[0-9 ()-]{6,25}$/'];
    }

    /** @return array<string, string> */
    protected function profileMessages(): array
    {
        return ['phone.regex' => 'Escribí solo números (podés usar +, espacios y guiones), con código de área.'];
    }
}
