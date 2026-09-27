<?php

namespace App\Enums;

enum Gender: string
{
    case Feminine = 'f';
    case Masculine = 'm';

    public function label(): string
    {
        return match ($this) {
            self::Feminine => 'Femenino',
            self::Masculine => 'Masculino',
        };
    }
}
