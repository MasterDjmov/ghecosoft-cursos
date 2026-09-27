<?php

namespace App\Enums;

/** Tipo de rama: el tronco obligatorio, un bloque de extras o una Senda de especialización. */
enum BranchKind: string
{
    case Trunk = 'trunk';
    case Extra = 'extra';
    case Path = 'path';

    public function label(): string
    {
        return match ($this) {
            self::Trunk => 'Tronco',
            self::Extra => 'Extras',
            self::Path => 'Senda',
        };
    }

    /** Lo que no es tronco es optativo: no cuenta para "curso completado". */
    public function isOptional(): bool
    {
        return $this !== self::Trunk;
    }
}
