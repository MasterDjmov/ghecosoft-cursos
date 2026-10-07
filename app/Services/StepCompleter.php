<?php

namespace App\Services;

use App\Enums\XpReason;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use InvalidArgumentException;

/**
 * Superar una micro-misión (D84 § 3). El código corre en el navegador del alumno; acá se recibe la salida que
 * obtuvo y se compara con la esperada. Como lo que viene del navegador se puede falsificar, solo da premios
 * de juego (XP por el Ledger): nunca monedas del curso, aperturas de nodos ni nada que cuente para el CV.
 */
class StepCompleter
{
    public function __construct(private readonly TreeAccess $access, private readonly Ledger $ledger) {}

    /** Puede jugarla: ve el nodo (abierto o Clase 0 de prueba, D71/D84) y superó las anteriores. */
    public function canPlay(User $user, NodeStep $step): bool
    {
        $node = $step->node;
        if (! $node->is_published && ! $user->isStaff()) {
            return false;
        }
        if (! $this->access->canView($user, $node)) {
            return false;
        }
        $previous = NodeStep::where('node_id', $node->id)->where('position', '<', $step->position)->pluck('id');

        return $previous->isEmpty()
            || NodeStepCompletion::where('user_id', $user->id)->whereIn('node_step_id', $previous)->count() === $previous->count();
    }

    public function isCompleted(User $user, NodeStep $step): bool
    {
        return NodeStepCompletion::where('user_id', $user->id)->where('node_step_id', $step->id)->exists();
    }

    /**
     * @return bool true si la superó ahora (y ganó la XP); false si ya la tenía superada.
     *
     * @throws InvalidArgumentException si no puede jugarla o la salida no es la esperada.
     */
    public function complete(User $user, NodeStep $step, string $output): bool
    {
        if (! $this->canPlay($user, $step)) {
            throw new InvalidArgumentException('Esta micro-misión todavía no está disponible.');
        }
        if (! $step->accepts($output)) {
            throw new InvalidArgumentException('La salida no es la esperada.');
        }

        return DB::transaction(function () use ($user, $step) {
            $completion = NodeStepCompletion::firstOrCreate(
                ['user_id' => $user->id, 'node_step_id' => $step->id],
                ['completed_at' => now()],
            );
            if (! $completion->wasRecentlyCreated) {
                return false;
            }
            // El staff prueba sin sumar XP.
            if ($step->xp_reward > 0 && ! $user->isStaff()) {
                $this->ledger->addXp($user, $step->xp_reward, XpReason::StepCompleted, $step, $step->node->course);
            }

            return true;
        });
    }
}
