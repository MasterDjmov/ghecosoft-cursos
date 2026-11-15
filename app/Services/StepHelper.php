<?php

namespace App\Services;

use App\Models\NodeStep;
use App\Models\StepAttempt;
use App\Models\StepHelp;
use App\Models\User;
use App\Support\LineDiff;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Session;
use InvalidArgumentException;

/**
 * D123: el botón «Necesito ayuda» de las micro-misiones. Todo sale de comparar el código inicial con la solución,
 * así que sirve para cualquier micro-misión sin escribir nada nuevo:
 * - «¿Dónde toco?»: los renglones del código inicial que hay que cambiar (o al lado de los que hay que agregar).
 * - «Mostrame una línea»: un renglón de la solución por cada intento fallido. La solución nunca sale entera de una
 *   vez: recién cuando se mostraron todos los renglones que cambian se entrega completa.
 * Si vio alguna línea, la micro-misión paga la mitad de XP y de oro (para que el ranking siga siendo justo).
 *
 * Se anota en `step_helps` (el Recorrido del docente). El staff y la Clase 0 de prueba no dejan registros (D71):
 * para ellos lo mostrado se recuerda en la sesión y no se pide un fallo antes de cada línea.
 */
class StepHelper
{
    /** Los fallos que habilitan la próxima línea (no la criatura de inglés). */
    private const FAIL_KINDS = ['output', 'checks', 'error'];

    public function __construct(private readonly StepCompleter $completer, private readonly TreeAccess $access) {}

    /** ¿Tiene con qué ayudar? Hace falta una solución y que no sea de inglés. */
    public function available(NodeStep $step): bool
    {
        return filled($step->solution) && ! $step->node->course->language->isSelfChecked();
    }

    /**
     * «¿Dónde toco?»: los números de renglón (desde 1) del código inicial que cambian. Donde solo hay que agregar,
     * se marca el renglón de arriba (o el primero). Vacío si el código inicial está vacío: ahí todo es nuevo.
     *
     * @return list<int>
     */
    public function whereLines(NodeStep $step): array
    {
        if (blank($step->starter_code) || blank($step->solution)) {
            return [];
        }
        $starter = LineDiff::lines((string) $step->starter_code);
        $marks = [];
        $lastSame = null;
        foreach (LineDiff::ops((string) $step->starter_code, (string) $step->solution) as $op) {
            if ($op['op'] === 'same') {
                $lastSame = $op['a'];
            } elseif ($op['op'] === 'del') {
                $marks[] = $op['a'] + 1;
            } else {
                $marks[] = $lastSame === null ? 1 : $lastSame + 1;
            }
        }
        $marks = array_values(array_unique(array_filter($marks, fn ($n) => $n >= 1 && $n <= max(1, count($starter)))));
        sort($marks);

        return $marks;
    }

    /**
     * Los renglones de la solución que no están en el código inicial (sin los vacíos), en orden.
     *
     * @return list<array{number: int, text: string}>
     */
    public function changedLines(NodeStep $step): array
    {
        $solution = LineDiff::lines((string) $step->solution);
        $changed = [];
        foreach (LineDiff::ops((string) $step->starter_code, (string) $step->solution) as $op) {
            if ($op['op'] === 'add' && trim($solution[$op['b']]) !== '') {
                $changed[] = ['number' => $op['b'] + 1, 'text' => rtrim($solution[$op['b']])];
            }
        }

        return $changed;
    }

    /**
     * Los renglones de la solución que ya se le mostraron.
     *
     * @return list<int>
     */
    public function shownLines(User $user, NodeStep $step): array
    {
        if ($this->keepsNoRecord($user, $step)) {
            return Session::get($this->sessionKey($step), []);
        }

        return StepHelp::where('user_id', $user->id)->where('node_step_id', $step->id)->where('kind', 'line')
            ->orderBy('id')->pluck('line')->filter()->values()->all();
    }

    /** Si vio alguna línea de la solución, la micro-misión paga la mitad (StepCompleter). */
    public function usedSolution(User $user, NodeStep $step): bool
    {
        return ! $this->keepsNoRecord($user, $step)
            && StepHelp::where('user_id', $user->id)->where('node_step_id', $step->id)->where('kind', 'line')->exists();
    }

    /**
     * «Mostrame una línea». Elige el primer renglón de la solución que cambia y que todavía no está en su código.
     * Devuelve todo lo mostrado hasta ahora (lines), la que se acaba de mostrar (new), si hace falta un intento
     * fallido antes de la próxima (wait) y la solución entera cuando ya se mostraron todos los renglones que cambian.
     *
     * @return array{lines: list<array{number: int, text: string}>, new: ?int, wait: bool, solution: ?string}
     *
     * @throws InvalidArgumentException si no puede jugarla o no hay solución.
     */
    public function revealLine(User $user, NodeStep $step, string $code): array
    {
        $this->guard($user, $step);
        $changed = collect($this->changedLines($step))->keyBy('number');
        $shown = $this->shownLines($user, $step);
        $remaining = $changed->except($shown);

        if ($remaining->isNotEmpty() && ! $this->mayRevealNext($user, $step, $shown)) {
            return $this->revealed($step, $changed, $shown, null, wait: true);
        }
        if ($remaining->isEmpty()) {
            return $this->revealed($step, $changed, $shown, null);
        }

        $mine = array_map(fn ($line) => trim($line), LineDiff::lines($code));
        $next = $remaining->first(fn ($line) => ! in_array(trim($line['text']), $mine, true)) ?? $remaining->first();
        $shown[] = $next['number'];
        $this->record($user, $step, 'line', $next['number']);

        return $this->revealed($step, $changed, $shown, $next['number']);
    }

    /** Lo ya mostrado (al volver a la página, la ayuda abierta se ve igual). */
    public function state(User $user, NodeStep $step): array
    {
        $changed = collect($this->changedLines($step))->keyBy('number');

        return $this->revealed($step, $changed, $this->shownLines($user, $step), null);
    }

    /** Anota una ayuda que no muestra nada del servidor («Comparemos», escuchar el desafío, la oferta de Gheco). */
    public function log(User $user, NodeStep $step, string $kind): void
    {
        if (! array_key_exists($kind, StepHelp::KINDS) || $kind === 'line') {
            throw new InvalidArgumentException('Esa ayuda no existe.');
        }
        $this->guard($user, $step, needsSolution: false);
        $this->record($user, $step, $kind);
    }

    /** «¿Dónde toco?» también queda anotado. */
    public function where(User $user, NodeStep $step): array
    {
        $this->guard($user, $step);
        $this->record($user, $step, 'where');

        return $this->whereLines($step);
    }

    /**
     * La primera línea, después del primer intento fallido; cada siguiente, después de otro fallo posterior a la
     * última que vio.
     *
     * @param  list<int>  $shown
     */
    private function mayRevealNext(User $user, NodeStep $step, array $shown): bool
    {
        if ($this->keepsNoRecord($user, $step)) {
            return true;
        }
        $fails = StepAttempt::where('user_id', $user->id)->where('node_step_id', $step->id)
            ->where('passed', false)->whereIn('kind', self::FAIL_KINDS);
        if ($shown === []) {
            return $fails->exists();
        }
        $last = StepHelp::where('user_id', $user->id)->where('node_step_id', $step->id)->where('kind', 'line')->latest('id')->value('created_at');

        return $fails->where('created_at', '>', $last)->exists();
    }

    /**
     * @param  Collection<int, array{number: int, text: string}>  $changed
     * @param  list<int>  $shown
     */
    private function revealed(NodeStep $step, $changed, array $shown, ?int $new, bool $wait = false): array
    {
        $complete = $changed->isNotEmpty() && $changed->keys()->diff($shown)->isEmpty();

        return [
            'lines' => $changed->only($shown)->sortKeys()->values()->all(),
            'new' => $new,
            'wait' => $wait,
            'solution' => $complete ? rtrim((string) $step->solution) : null,
        ];
    }

    private function guard(User $user, NodeStep $step, bool $needsSolution = true): void
    {
        if (! $this->completer->canPlay($user, $step)) {
            throw new InvalidArgumentException('Esta micro-misión todavía no está disponible.');
        }
        if ($needsSolution && ! $this->available($step)) {
            throw new InvalidArgumentException('Esta micro-misión no tiene ayuda.');
        }
    }

    private function record(User $user, NodeStep $step, string $kind, ?int $line = null): void
    {
        if ($this->keepsNoRecord($user, $step)) {
            if ($kind === 'line') {
                Session::put($this->sessionKey($step), [...Session::get($this->sessionKey($step), []), $line]);
            }

            return;
        }
        StepHelp::create([
            'user_id' => $user->id,
            'node_step_id' => $step->id,
            'course_id' => $step->node->course_id,
            'kind' => $kind,
            'line' => $line,
            'created_at' => now(),
        ]);
    }

    private function keepsNoRecord(User $user, NodeStep $step): bool
    {
        return $user->isStaff() || $this->access->isTrial($user, $step->node);
    }

    private function sessionKey(NodeStep $step): string
    {
        return 'step-help.'.$step->id;
    }
}
