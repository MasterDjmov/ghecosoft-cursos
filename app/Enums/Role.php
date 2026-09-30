<?php

namespace App\Enums;

enum Role: string
{
    case Admin = 'admin';
    /** Docente (D72): corrige y atiende a los alumnos de sus comisiones; no maneja pagos ni contenido. */
    case Teacher = 'teacher';
    case Student = 'student';

    public function label(): string
    {
        return match ($this) {
            self::Admin => 'Administrador',
            self::Teacher => 'Docente',
            self::Student => 'Alumno',
        };
    }
}
