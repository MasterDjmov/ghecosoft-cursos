<?php

namespace App\Enums;

enum RequestType: string
{
    case Receipt = 'receipt';
    case Contact = 'contact';

    public function label(): string
    {
        return match ($this) {
            self::Receipt => 'Comprobante',
            self::Contact => 'Contacto',
        };
    }
}
