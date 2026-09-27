<?php

namespace App\Support;

use App\Models\User;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;

/**
 * Nombre del héroe (D38): lo elige el alumno, es público y único en toda la plataforma
 * (sin distinguir mayúsculas ni tildes, por la intercalación de la base). El docente lo puede cambiar.
 */
class HeroName
{
    public const MIN = 3;

    public const MAX = 20;

    public static function normalize(?string $name): ?string
    {
        $name = Str::squish((string) $name);

        return $name === '' ? null : $name;
    }

    /** @return array<string, array<int, mixed>> */
    public static function rules(string $field, ?User $ignore = null): array
    {
        return [$field => [
            'nullable', 'string', 'min:'.self::MIN, 'max:'.self::MAX,
            // Letras (con tildes y ñ), números y espacios simples.
            'regex:/^[\pL\pN]+( [\pL\pN]+)*$/u',
            Rule::unique('users', 'hero_name')->ignore($ignore?->id),
        ]];
    }

    /** @return array<string, string> */
    public static function messages(string $field): array
    {
        return [
            "{$field}.regex" => 'El nombre del héroe lleva letras, números y espacios.',
            "{$field}.unique" => 'Ese héroe ya existe en la plataforma: elegí otro nombre.',
        ];
    }
}
