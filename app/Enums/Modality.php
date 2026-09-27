<?php

namespace App\Enums;

enum Modality: string
{
    case InPerson = 'in_person';
    case Virtual = 'virtual';
    case Hybrid = 'hybrid';

    public function label(): string
    {
        return match ($this) {
            self::InPerson => 'Presencial',
            self::Virtual => 'Virtual',
            self::Hybrid => 'Híbrida',
        };
    }
}
