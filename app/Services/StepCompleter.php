<?php

namespace App\Services;

use App\Enums\CoinReason;
use App\Enums\XpReason;
use App\Models\CoinTransaction;
use App\Models\Currency;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\User;
use App\Models\XpTransaction;
use Illuminate\Support\Facades\DB;
use InvalidArgumentException;

/**
 * Superar una micro-misión (D84 § 3). El código corre en el navegador del alumno; acá se recibe la salida que
 * obtuvo y se compara con la esperada. Como lo que viene del navegador se puede falsificar, solo da premios
 * de juego (XP y oro por el Ledger, D89): nunca monedas del curso, aperturas de nodos ni nada que cuente para el CV.
 * Excepciones: D106, en un curso que se comprueba solo (inglés), superarlas todas completa el nodo; ese curso
 * no tiene monedas ni cuenta para el CV. D111, en un curso donde las micro-misiones completan el nodo (Java), las
 * que vienen de una misión pagan monedas del curso y superarlas todas completa el nodo (con sus obligatorias):
 * el docente aceptó que se puedan trampear.
 */
class StepCompleter
{
    public function __construct(private readonly TreeAccess $access, private readonly Ledger $ledger, private readonly Heroes $heroes, private readonly Inventory $inventory, private readonly SubmissionReviewer $reviewer) {}

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
    public function complete(User $user, NodeStep $step, string $output, ?string $code = null): bool
    {
        if (! $this->canPlay($user, $step)) {
            throw new InvalidArgumentException('Esta micro-misión todavía no está disponible.');
        }
        if (! $step->accepts($output)) {
            throw new InvalidArgumentException('La salida no es la esperada.');
        }

        return DB::transaction(function () use ($user, $step, $output, $code) {
            $completion = NodeStepCompletion::firstOrCreate(
                ['user_id' => $user->id, 'node_step_id' => $step->id],
                ['completed_at' => now(), 'code' => $code, 'output' => $output],
            );
            if (! $completion->wasRecentlyCreated) {
                // Si la vuelve a resolver, queda su última versión para releer (la XP no se repite).
                $completion->update(['code' => $code ?? $completion->code, 'output' => $output]);

                return false;
            }
            // El staff prueba sin sumar XP.
            if ($step->xp_reward > 0 && ! $user->isStaff()) {
                $this->ledger->addXp($user, $step->xp_reward, XpReason::StepCompleted, $step, $step->node->course);
            }
            $this->heroes->creditStep($user, $step);
            $this->inventory->creditStep($user, $step);
            $this->creditCoins($user, $step);

            // D106 y D111: superar la última completa el nodo (y abre a sus hijos).
            $course = $step->node->course;
            if (($course->language->isSelfChecked() || $course->steps_complete_nodes) && ! $user->isStaff()) {
                $this->reviewer->completeWithoutPractices($user, $step->node);
            }

            return true;
        });
    }

    /** D111: las monedas del curso de una micro-misión que vino de una misión, una sola vez. */
    private function creditCoins(User $user, NodeStep $step): void
    {
        $course = $step->node->course;
        if ($step->coin_reward <= 0 || $user->isStaff() || ! $course->steps_complete_nodes) {
            return;
        }
        $currency = Currency::forCourse($course);
        $paid = CoinTransaction::where('user_id', $user->id)->where('currency_id', $currency->id)
            ->where('reason', CoinReason::StepCompleted)
            ->where('source_type', $step->getMorphClass())->where('source_id', $step->id)->exists();
        if (! $paid) {
            $this->ledger->credit($user, $currency, $step->coin_reward, CoinReason::StepCompleted, $step, $course);
        }
    }

    /**
     * D106: el extra «Decilo en voz alta» de una micro-misión de inglés. El reconocimiento de voz corre en el
     * navegador, así que solo da un poco de XP (`game.spoken_xp`), una sola vez por micro-misión.
     *
     * @return int la XP que ganó ahora (0 si ya la había ganado).
     *
     * @throws InvalidArgumentException si no puede jugarla o no tiene frase para decir.
     */
    public function speak(User $user, NodeStep $step): int
    {
        if (! $this->canPlay($user, $step)) {
            throw new InvalidArgumentException('Esta micro-misión todavía no está disponible.');
        }
        if (! $step->node->course->language->isSelfChecked() || ! ($step->englishExercise()['speak'] ?? null)) {
            throw new InvalidArgumentException('Esta micro-misión no tiene una frase para decir.');
        }
        $xp = (int) config('game.spoken_xp');
        if ($xp <= 0 || $user->isStaff()) {
            return 0;
        }

        return DB::transaction(function () use ($user, $step, $xp) {
            User::whereKey($user->id)->lockForUpdate()->first();
            $paid = XpTransaction::where('user_id', $user->id)->where('reason', XpReason::SpokeAloud)
                ->where('source_type', $step->getMorphClass())->where('source_id', $step->id)->exists();
            if ($paid) {
                return 0;
            }
            $this->ledger->addXp($user, $xp, XpReason::SpokeAloud, $step, $step->node->course);

            return $xp;
        });
    }
}
