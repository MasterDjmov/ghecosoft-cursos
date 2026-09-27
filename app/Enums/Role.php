<?php

namespace App\Enums;

enum Role: string
{
    case Admin = 'admin';
    case Student = 'student';

    public function label(): string
    {
        return match ($this) {
            self::Admin => 'Docente',
            self::Student => 'Alumno',
        };
    }
}
