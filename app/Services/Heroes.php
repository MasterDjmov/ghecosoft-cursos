<?php

namespace App\Services;

use App\Enums\CoinReason;
use App\Exceptions\InsufficientFunds;
use App\Models\CoinTransaction;
use App\Models\Course;
use App\Models\Currency;
use App\Models\Hero;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use InvalidArgumentException;

/**
 * El protagonista de cada curso y el oro del jugador (D84/D89). Todo el oro pasa por el Ledger.
 */
class Heroes
{
    public function __construct(private readonly Ledger $ledger) {}

    /**
     * El protagonista fijo del curso (config/game.php), o null si el curso no tiene (accesorios, cursos sin historia).
     *
     * @return array{name: string, slug: string, title: string, looks: array<int, string>}|null
     */
    public function protagonist(Course $course): ?array
    {
        return config('game.protagonists.'.$course->language->value);
    }

    public static function lookUrl(array $protagonist, int $look): string
    {
        return asset('img/protagonistas/'.$protagonist['slug'].'/'.$look.'.webp');
    }

    public function heroOf(User $user, Course $course): ?Hero
    {
        return Hero::where('user_id', $user->id)->where('course_id', $course->id)->first();
    }

    /**
     * «Tomá el control»: el aspecto y el reparto de los 24 puntos (cada atributo entre 4 y 12).
     *
     * @param  array<string, int>  $stats
     *
     * @throws InvalidArgumentException si el reparto no vale o ya lo tiene.
     */
    public function create(User $user, Course $course, int $look, array $stats): Hero
    {
        if ($this->protagonist($course) === null) {
            throw new InvalidArgumentException('Este curso no tiene protagonista.');
        }
        if ($look < 1 || $look > Hero::LOOKS) {
            throw new InvalidArgumentException('Elegí uno de los aspectos.');
        }
        $values = $this->checkDistribution($stats);

        return DB::transaction(function () use ($user, $course, $look, $values) {
            if ($this->heroOf($user, $course)) {
                throw new InvalidArgumentException('Ya tomaste el control de este personaje.');
            }

            return Hero::create(['user_id' => $user->id, 'course_id' => $course->id, 'look' => $look, ...$values]);
        });
    }

    /**
     * Reacomodar los 24 puntos del principio: gratis mientras no haya comprado ningún punto con oro
     * (después, solo con un Pergamino del Reinicio, que llega con los ítems).
     *
     * @param  array<string, int>  $stats
     */
    public function redistribute(Hero $hero, array $stats): void
    {
        if (! $this->canRedistribute($hero)) {
            throw new InvalidArgumentException('Ya mejoraste atributos con oro: los puntos quedan fijos.');
        }
        // Si lo reacomoda con un Pergamino del Reinicio, se gasta.
        $hero->update([...$this->checkDistribution($stats), 'respec_available' => false]);
    }

    /** Gratis mientras no compró puntos con oro; después, con un Pergamino del Reinicio usado. */
    public function canRedistribute(Hero $hero): bool
    {
        return $hero->respec_available || ! CoinTransaction::where('reason', CoinReason::StatUpgrade)
            ->where('source_type', $hero->getMorphClass())->where('source_id', $hero->id)->exists();
    }

    /**
     * @param  array<string, int>  $stats
     * @return array<string, int>
     */
    private function checkDistribution(array $stats): array
    {
        $values = [];
        foreach (Hero::STATS as $stat) {
            $value = $stats[$stat] ?? null;
            if (! is_int($value) || $value < Hero::MIN_STAT || $value > Hero::MAX_START) {
                throw new InvalidArgumentException('Cada atributo va de '.Hero::MIN_STAT.' a '.Hero::MAX_START.'.');
            }
            $values[$stat] = $value;
        }
        if (array_sum($values) !== Hero::POINTS) {
            throw new InvalidArgumentException('Tenés que repartir exactamente '.Hero::POINTS.' puntos.');
        }

        return $values;
    }

    /** El oro que gastó en atributos (lo que se devuelve al reiniciarlo). */
    public function spentOnStats(Hero $hero): int
    {
        return -(int) CoinTransaction::where('reason', CoinReason::StatUpgrade)
            ->where('source_type', $hero->getMorphClass())->where('source_id', $hero->id)->sum('amount');
    }

    /**
     * Reiniciar el héroe para corregir (Admin → Alumnos, D89): le devuelve el oro que gastó en atributos
     * (queda en el libro) y lo borra; la próxima vez vuelve a «Tomá el control».
     *
     * @return int el oro devuelto
     */
    public function reset(Hero $hero, ?User $by = null): int
    {
        return DB::transaction(function () use ($hero, $by) {
            $locked = Hero::whereKey($hero->id)->lockForUpdate()->firstOrFail();
            $refund = $this->spentOnStats($locked);
            if ($refund > 0) {
                $this->ledger->credit($locked->user, Currency::gold(), $refund, CoinReason::Reversal, $locked, $locked->course,
                    'Reinicio del héroe: se devuelve el oro de los atributos', $by);
            }
            $locked->delete();

            return $refund;
        });
    }

    /** El aspecto es solo cosmético: se cambia cuando quiera y gratis. */
    public function changeLook(Hero $hero, int $look): void
    {
        if ($look < 1 || $look > Hero::LOOKS) {
            throw new InvalidArgumentException('Elegí uno de los aspectos.');
        }
        $hero->update(['look' => $look]);
    }

    /**
     * Sube un punto de un atributo pagando con oro (100 × el valor actual).
     *
     * @throws InsufficientFunds si no le alcanza el oro.
     */
    public function upgrade(Hero $hero, string $stat): void
    {
        if (! in_array($stat, Hero::STATS, true)) {
            throw new InvalidArgumentException('Ese atributo no existe.');
        }

        DB::transaction(function () use ($hero, $stat) {
            $locked = Hero::whereKey($hero->id)->lockForUpdate()->firstOrFail();
            if ($locked->{$stat} >= Hero::MAX_STAT) {
                throw new InvalidArgumentException(Hero::statLabel($stat).' ya está al máximo.');
            }
            $this->ledger->debit($hero->user, Currency::gold(), $locked->upgradeCost($stat), CoinReason::StatUpgrade, $locked, $hero->course,
                Hero::statLabel($stat).' '.$locked->{$stat}.' → '.($locked->{$stat} + 1));
            $locked->increment($stat);
            $hero->{$stat} = $locked->{$stat};
        });
    }

    public function gold(User $user): int
    {
        return $this->ledger->balance($user, Currency::gold());
    }

    /** El oro de una micro-misión superada, una sola vez (el staff prueba sin ganar). */
    public function creditStep(User $user, NodeStep $step): void
    {
        if (! config('game.gold_enabled') || $step->gold_reward <= 0 || $user->isStaff()) {
            return;
        }
        $gold = Currency::gold();
        DB::transaction(function () use ($user, $step, $gold) {
            User::whereKey($user->id)->lockForUpdate()->first();
            $paid = CoinTransaction::where('user_id', $user->id)->where('currency_id', $gold->id)
                ->where('reason', CoinReason::StepCompleted)
                ->where('source_type', $step->getMorphClass())->where('source_id', $step->id)->exists();
            if (! $paid) {
                $this->ledger->credit($user, $gold, $step->gold_reward, CoinReason::StepCompleted, $step, $step->node->course);
            }
        });
    }

    /**
     * El oro de todas las micro-misiones que ya superó y todavía no cobró (las de antes de que existiera
     * el oro, D89). Se llama al entrar al panel: es idempotente.
     */
    public function settleGold(User $user): int
    {
        if (! config('game.gold_enabled') || $user->isStaff()) {
            return 0;
        }
        $gold = Currency::gold();
        $paid = CoinTransaction::where('user_id', $user->id)->where('currency_id', $gold->id)
            ->where('reason', CoinReason::StepCompleted)->where('source_type', (new NodeStep)->getMorphClass())
            ->pluck('source_id');
        $pending = NodeStep::with('node.course')
            ->whereIn('id', NodeStepCompletion::where('user_id', $user->id)->select('node_step_id'))
            ->whereNotIn('id', $paid)
            ->where('gold_reward', '>', 0)
            ->get();
        $pending->each(fn (NodeStep $step) => $this->creditStep($user, $step));

        return $pending->sum('gold_reward');
    }
}
