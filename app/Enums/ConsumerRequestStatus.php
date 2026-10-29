<?php

namespace App\Enums;

enum ConsumerRequestStatus: string
{
    case Pending = 'pending';
    case Handled = 'handled';

    public function label(): string
    {
        return match ($this) {
            self::Pending => 'Pendiente',
            self::Handled => 'Resuelto',
        };
    }
}
