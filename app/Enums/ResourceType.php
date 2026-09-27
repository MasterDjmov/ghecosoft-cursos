<?php

namespace App\Enums;

enum ResourceType: string
{
    case Link = 'link';
    case File = 'file';

    public function label(): string
    {
        return match ($this) {
            self::Link => 'Link',
            self::File => 'Archivo',
        };
    }
}
