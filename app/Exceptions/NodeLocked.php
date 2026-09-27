<?php

namespace App\Exceptions;

use DomainException;

class NodeLocked extends DomainException
{
    /** @param  list<string>  $reasons  Códigos de TreeAccess::unlockBlockers() */
    public function __construct(public readonly array $reasons)
    {
        parent::__construct('Todavía no podés abrir este nodo ('.implode(', ', $reasons).').');
    }
}
