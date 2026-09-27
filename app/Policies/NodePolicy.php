<?php

namespace App\Policies;

use App\Models\Node;
use App\Models\User;
use App\Services\TreeAccess;

class NodePolicy
{
    public function __construct(private readonly TreeAccess $access) {}

    /** El contenido de un nodo solo lo ve quien lo abrió. */
    public function view(User $user, Node $node): bool
    {
        return $this->access->canView($user, $node);
    }
}
