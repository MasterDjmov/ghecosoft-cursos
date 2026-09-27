<?php

namespace App\Enums;

enum NodeType: string
{
    case Root = 'root';
    case Topic = 'topic';
    case Boss = 'boss';
    case Extra = 'extra';
    case Window = 'window';

    /** Los tipos que el docente elige al crear o editar (el raíz es uno solo por curso). */
    public static function editable(): array
    {
        return [self::Topic, self::Window, self::Boss, self::Extra];
    }

    public function label(): string
    {
        return match ($this) {
            self::Root => 'Raíz',
            self::Topic => 'Tema',
            self::Boss => 'Jefe',
            self::Extra => 'Extra',
            self::Window => 'Ventana',
        };
    }
}
