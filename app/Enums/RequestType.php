<?php

namespace App\Enums;

enum RequestType: string
{
    case Receipt = 'receipt';
    case Contact = 'contact';
    /** El docente inscribió al alumno al crearle la cuenta. */
    case Admin = 'admin';

    public function label(): string
    {
        return match ($this) {
            self::Receipt => 'Comprobante',
            self::Contact => 'Contacto',
            self::Admin => 'Alta del docente',
        };
    }
}
