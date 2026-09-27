<?php

namespace App\Enums;

enum NodeType: string
{
    case Root = 'root';
    case Topic = 'topic';
    case Boss = 'boss';
    case Extra = 'extra';

    public function label(): string
    {
        return match ($this) {
            self::Root => 'Raíz',
            self::Topic => 'Tema',
            self::Boss => 'Jefe',
            self::Extra => 'Extra',
        };
    }
}
