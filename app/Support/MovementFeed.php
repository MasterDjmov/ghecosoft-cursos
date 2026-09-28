<?php

namespace App\Support;

use App\Models\CoinTransaction;
use App\Models\Course;
use App\Models\EnrollmentRequest;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Models\Submission;
use App\Models\User;
use App\Models\XpTransaction;
use Illuminate\Support\Collection;

/**
 * El libro de movimientos de un alumno para mostrar: resumen por curso y una sola
 * lista donde las monedas y el XP de un mismo hecho van juntos ("Práctica aprobada:
 * «Hola, mundo» → +4 escamas, +10 XP"), con el detalle de qué lo originó.
 * Solo lee: los saldos siguen saliendo del Ledger.
 */
class MovementFeed
{
    /**
     * Cursos con movimientos del alumno: saldo de su moneda y XP ganada en cada uno.
     *
     * @return Collection<int, array{course: Course, coins: int, xp: int}>
     */
    public static function courses(User $user): Collection
    {
        $coins = CoinTransaction::where('coin_transactions.user_id', $user->id)
            ->join('currencies', 'currencies.id', '=', 'coin_transactions.currency_id')
            ->whereNotNull('currencies.course_id')
            ->groupBy('currencies.course_id')
            ->selectRaw('currencies.course_id, SUM(amount) as total')
            ->pluck('total', 'course_id');
        $xp = XpTransaction::where('user_id', $user->id)->whereNotNull('course_id')
            ->groupBy('course_id')->selectRaw('course_id, SUM(amount) as total')->pluck('total', 'course_id');
        $used = CoinTransaction::where('user_id', $user->id)->whereNotNull('course_id')->distinct()->pluck('course_id');

        return Course::whereIn('id', $coins->keys()->merge($xp->keys())->merge($used)->unique())
            ->orderBy('title')
            ->get()
            ->map(fn (Course $course) => ['course' => $course, 'coins' => (int) ($coins[$course->id] ?? 0), 'xp' => (int) ($xp[$course->id] ?? 0)]);
    }

    /** Saldo de comodines (sirven en todos los cursos) y XP total. */
    public static function totals(User $user): array
    {
        return [
            'wildcards' => (int) CoinTransaction::where('user_id', $user->id)
                ->whereHas('currency', fn ($query) => $query->where('is_wildcard', true))->sum('amount'),
            'xp' => (int) XpTransaction::where('user_id', $user->id)->sum('amount'),
        ];
    }

    /**
     * Los hechos más recientes (agrupados), del curso pedido o de todos.
     *
     * @return array{entries: Collection<int, array<string, mixed>>, has_more: bool}
     */
    public static function entries(User $user, ?Course $course, int $limit): array
    {
        // Se trae de más para que el agrupado no deje hechos por la mitad.
        $take = $limit * 3 + 1;
        $filter = fn ($query) => $query->where('user_id', $user->id)->when($course, fn ($q) => $q->where('course_id', $course->id));

        $coins = CoinTransaction::with(['currency.course', 'creator:id,name'])->tap($filter)->latest('id')->limit($take)->get();
        $xp = XpTransaction::with('creator:id,name')->tap($filter)->latest('id')->limit($take)->get();
        $truncated = $coins->count() === $take || $xp->count() === $take;

        $all = $coins->map(fn ($row) => ['kind' => 'coin', 'row' => $row])
            ->merge($xp->map(fn ($row) => ['kind' => 'xp', 'row' => $row]));
        self::loadSources($all->pluck('row'));
        $courses = Course::whereIn('id', $all->pluck('row.course_id')->filter()->unique())->get()->keyBy('id');

        $entries = $all
            ->groupBy(fn ($item) => $item['row']->source_type
                ? $item['row']->source_type.':'.$item['row']->source_id.':'.$item['row']->reason->value
                : $item['kind'].':'.$item['row']->id)
            ->map(fn (Collection $items) => self::entry($items, $courses))
            ->sortByDesc('sort')
            ->values();

        return ['entries' => $entries->take($limit), 'has_more' => $entries->count() > $limit || $truncated];
    }

    /** Carga de una vez lo que originó cada movimiento (práctica, nodo, solicitud). */
    private static function loadSources(Collection $rows): void
    {
        $rows->groupBy('source_type')->each(function (Collection $group, $type) {
            $relations = match ($type) {
                Submission::class => ['practice.node'],
                NodeUnlock::class => ['node'],
                default => [],
            };
            $sources = $type ? $type::with($relations)->whereIn('id', $group->pluck('source_id')->unique())->get()->keyBy('id') : collect();
            $group->each(fn ($row) => $row->setRelation('source', $sources[$row->source_id] ?? null));
        });
    }

    private static function entry(Collection $items, Collection $courses): array
    {
        $first = $items->first()['row'];
        $source = $first->source;
        $course = $courses[$first->course_id] ?? null;

        [$title, $detail, $node, $icon] = match (true) {
            $source instanceof Submission && $source->practice => [
                $first->reason->label().': «'.$source->practice->title.'»',
                ($source->practice->is_required ? 'Misión' : 'Optativa').' de «'.$source->practice->node->title.'»'.($source->attempt > 1 ? ' · intento '.$source->attempt : ''),
                $source->practice->node,
                'check-badge',
            ],
            $source instanceof NodeUnlock && $source->node => ['Abriste «'.$source->node->title.'»', null, $source->node, 'lock-open'],
            $source instanceof Node => [
                ($first->reason->value === 'boss_defeated' ? 'Venciste a ' : 'Completaste ').'«'.$source->title.'»',
                null, $source, $first->reason->value === 'boss_defeated' ? 'fire' : 'flag',
            ],
            $source instanceof EnrollmentRequest => [$first->reason->label(), 'Para abrir «'.($course?->nodes()->where('type', 'root')->value('title') ?? 'el primer nodo').'»', null, 'ticket'],
            default => [$first->reason->label(), null, null, 'adjustments-horizontal'],
        };

        return [
            'sort' => $first->created_at->format('YmdHis').str_pad((string) $items->max(fn ($item) => $item['row']->id), 10, '0', STR_PAD_LEFT),
            'title' => $title,
            'detail' => $detail,
            'icon' => $icon,
            'node' => $node,
            'course' => $course,
            'note' => $first->note,
            'author' => $items->map(fn ($item) => $item['row']->creator?->name)->filter()->first(),
            'at' => $first->created_at,
            'amounts' => $items->map(fn ($item) => $item['kind'] === 'xp'
                ? ['amount' => $item['row']->amount, 'label' => term('xp.short'), 'type' => 'xp']
                : ['amount' => $item['row']->amount, 'type' => $item['row']->currency->is_wildcard ? 'wildcard' : 'coin',
                    'label' => $item['row']->currency->is_wildcard ? term('coin.wildcard', null, abs($item['row']->amount)) : term('coin.course', $item['row']->currency->course, abs($item['row']->amount))])
                ->sortBy(fn ($amount) => ['coin' => 0, 'wildcard' => 1, 'xp' => 2][$amount['type']])
                ->values()
                ->all(),
        ];
    }
}
