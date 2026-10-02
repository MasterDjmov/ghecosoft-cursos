<?php

namespace App\Livewire\Student\Concerns;

use App\Exceptions\NodeLocked;
use App\Models\Node;
use App\Services\NodeUnlocker;
use App\Support\UnlockMessages;
use Flux\Flux;
use Illuminate\Support\Facades\RateLimiter;

/** Abrir un nodo desde el árbol o desde el «Siguiente» del nodo anterior: mismos límites y mensajes. */
trait UnlocksNodes
{
    protected function openNode(Node $node, NodeUnlocker $unlocker)
    {
        $key = 'unlock:'.auth()->id();
        if (RateLimiter::tooManyAttempts($key, 20)) {
            Flux::toast(variant: 'danger', text: 'Demasiados intentos. Esperá un minuto.');

            return null;
        }
        RateLimiter::hit($key, 60);

        try {
            $unlocker->unlock(auth()->user(), $node);
        } catch (NodeLocked $e) {
            Flux::toast(variant: 'danger', text: implode(' ', UnlockMessages::for(auth()->user(), $node, $e->reasons)));

            return null;
        }

        Flux::toast(variant: 'success', text: '¡Abriste «'.$node->title.'»!');

        return $this->redirectRoute('student.node', [$node->course, $node], navigate: true);
    }
}
