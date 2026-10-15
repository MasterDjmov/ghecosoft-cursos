<?php

namespace App\Services;

use App\Models\Node;
use App\Models\NodeStep;
use App\Models\StepAttempt;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Lottery;
use Illuminate\Support\Str;

/**
 * D107: anota lo que hace el alumno para saber dónde se traba: los intentos de las micro-misiones (los fallos
 * los avisa su navegador; acá no se comprueba ni se ejecuta nada) y los nodos que mira. El staff no se anota.
 * La Clase 0 de prueba (D71) no deja registros. Los intentos viejos se borran de a poco, sin cron (cada tanto,
 * al anotar uno nuevo).
 */
class ActivityLog
{
    public function __construct(private readonly TreeAccess $access) {}

    /** Meses que se guardan los intentos. */
    public const KEEP_MONTHS = 6;

    public function attempt(User $user, NodeStep $step, bool $passed, ?string $kind = null, ?string $answer = null): void
    {
        if ($user->isStaff() || $this->access->isTrial($user, $step->node)) {
            return;
        }
        $answer = $answer === null ? null : Str::limit(trim($answer), 495, '…');
        $kind = $kind === null ? null : Str::limit(preg_replace('/[^a-z_-]/', '', strtolower($kind)), 20, '');

        // El mismo fallo seguido (apretar «Ejecutar» sin cambiar nada) cuenta una sola vez.
        if (! $passed) {
            $last = StepAttempt::where('user_id', $user->id)->where('node_step_id', $step->id)->latest('id')->first();
            if ($last && ! $last->passed && $last->kind === $kind && $last->answer === $answer) {
                return;
            }
        }

        StepAttempt::create([
            'user_id' => $user->id,
            'node_step_id' => $step->id,
            'node_id' => $step->node_id,
            'course_id' => $step->node->course_id,
            'passed' => $passed,
            'kind' => $kind ?: null,
            'answer' => $answer === '' ? null : $answer,
            'created_at' => now(),
        ]);

        Lottery::odds(1, 200)->winner(fn () => $this->prune())->choose();
    }

    public function visit(User $user, Node $node): void
    {
        if ($user->isStaff() || $this->access->isTrial($user, $node)) {
            return;
        }
        $now = now();
        DB::table('node_visits')->upsert(
            [['user_id' => $user->id, 'node_id' => $node->id, 'course_id' => $node->course_id, 'visited_on' => $now->toDateString(), 'views' => 1, 'first_at' => $now, 'last_at' => $now]],
            ['user_id', 'node_id', 'visited_on'],
            ['views' => DB::raw('views + 1'), 'last_at' => $now],
        );
    }

    /** Borra los intentos de más de KEEP_MONTHS meses. @return int cuántos borró */
    public function prune(): int
    {
        return StepAttempt::where('created_at', '<', now()->subMonths(self::KEEP_MONTHS))->delete();
    }
}
