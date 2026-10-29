<?php

namespace App\Enums;

/** D112: pedidos de Defensa del Consumidor que se hacen desde el pie de cualquier página. */
enum ConsumerRequestKind: string
{
    case Withdrawal = 'withdrawal';
    case Cancellation = 'cancellation';

    public function label(): string
    {
        return match ($this) {
            self::Withdrawal => 'Arrepentimiento',
            self::Cancellation => 'Baja',
        };
    }
}
