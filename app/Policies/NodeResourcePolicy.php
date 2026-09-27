<?php

namespace App\Policies;

use App\Models\NodeResource;
use App\Models\User;
use App\Services\TreeAccess;

class NodeResourcePolicy
{
    public function __construct(private readonly TreeAccess $access) {}

    /** Solo quien abrió el nodo (el admin pasa por Gate::before). */
    public function view(User $user, NodeResource $resource): bool
    {
        return $this->access->canView($user, $resource->node);
    }
}
