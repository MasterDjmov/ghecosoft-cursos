<?php

namespace App\Console\Commands;

use App\Concerns\ProfileValidationRules;
use App\Enums\Role;
use App\Models\User;
use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Str;
use Illuminate\Validation\Rules\NotIn;
use Illuminate\Validation\Rules\Password;

use function Laravel\Prompts\password;
use function Laravel\Prompts\text;

#[Signature('app:create-admin')]
#[Description('Crea la cuenta del docente (rol admin)')]
class CreateAdmin extends Command
{
    use ProfileValidationRules;

    public function handle(): int
    {
        $input = [
            'name' => text('Nombre', required: true),
            'last_name' => text('Apellido', required: true),
            'username' => Str::lower(text('Usuario', required: true)),
            'email' => Str::lower(text('Email', required: true)),
            'password' => password('Contraseña (mín. 8, mayúscula, minúscula y número)', required: true),
        ];

        $rules = $this->profileRules();
        // El admin sí puede usar nombres reservados como "admin" o "docente".
        $rules['username'] = array_values(array_filter($rules['username'], fn ($rule) => ! $rule instanceof NotIn));

        $validator = Validator::make($input, [...$rules, 'password' => ['required', Password::defaults()]]);

        if ($validator->fails()) {
            foreach ($validator->errors()->all() as $error) {
                $this->components->error($error);
            }

            return self::FAILURE;
        }

        $user = User::create($input);
        $user->forceFill(['role' => Role::Admin, 'email_verified_at' => now()])->save();

        $this->components->info("Admin \"{$user->username}\" creado.");

        return self::SUCCESS;
    }
}
