<?php

namespace App\Enums;

enum RequestKind: string
{
    case New = 'new';
    case Renewal = 'renewal';

    public function label(): string
    {
        return match ($this) {
            self::New => 'Inscripción',
            self::Renewal => 'Renovación',
        };
    }
}
