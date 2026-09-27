<?php

namespace App\Exceptions;

use DomainException;

class InsufficientFunds extends DomainException
{
    public function __construct(public readonly int $balance, public readonly int $required)
    {
        parent::__construct("Saldo insuficiente: tenés {$balance} y hacen falta {$required}.");
    }
}
