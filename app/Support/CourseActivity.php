<?php

namespace App\Support;

use App\Models\NodeVisit;
use App\Models\StepAttempt;
use App\Models\User;
use App\Models\XpTransaction;
use Carbon\CarbonImmutable;
use Illuminate\Support\Collection;

/**
 * Cómo viene un alumno en cada curso, para la lista de *Admin → Alumnos*: la XP que juntó en el curso y una tira con
 * los últimos días (activo o no). Un día cuenta como activo si el alumno miró un nodo del curso, intentó una
 * micro-misión o ganó XP en él (lo que registran ActivityLog y el Ledger). Los días anteriores a su primer abono no
 * se pintan de rojo: todavía no estaba en el curso.
 */
class CourseActivity
{
    public const DAYS = 14;

    /**
     * @param  array<int, CarbonImmutable>  $startedAt  desde cuándo está en cada curso (course_id → primer abono)
     * @return array<int, array{xp: int, last: ?CarbonImmutable, days: list<array{date: CarbonImmutable, state: string}>}>
     */
    public static function for(User $student, array $startedAt): array
    {
        $courseIds = array_keys($startedAt);
        if ($courseIds === []) {
            return [];
        }
        $today = CarbonImmutable::today();
        $from = $today->subDays(self::DAYS - 1);

        $xp = XpTransaction::where('user_id', $student->id)->whereIn('course_id', $courseIds)
            ->groupBy('course_id')->selectRaw('course_id, SUM(amount) as total')->pluck('total', 'course_id');

        // Días con actividad en la ventana, por curso: [course_id => ['2026-11-01' => true, ...]].
        $active = collect()
            ->merge(NodeVisit::where('user_id', $student->id)->whereIn('course_id', $courseIds)
                ->where('visited_on', '>=', $from->toDateString())
                ->get(['course_id', 'visited_on'])->map(fn ($v) => [$v->course_id, $v->visited_on->toDateString()]))
            ->merge(self::days(StepAttempt::class, $student, $courseIds, $from))
            ->merge(self::days(XpTransaction::class, $student, $courseIds, $from))
            ->groupBy(0)->map(fn (Collection $rows) => $rows->pluck(1)->flip());

        $last = collect([
            NodeVisit::where('user_id', $student->id)->whereIn('course_id', $courseIds)
                ->groupBy('course_id')->selectRaw('course_id, MAX(last_at) as at')->pluck('at', 'course_id'),
            StepAttempt::where('user_id', $student->id)->whereIn('course_id', $courseIds)
                ->groupBy('course_id')->selectRaw('course_id, MAX(created_at) as at')->pluck('at', 'course_id'),
            XpTransaction::where('user_id', $student->id)->whereIn('course_id', $courseIds)
                ->groupBy('course_id')->selectRaw('course_id, MAX(created_at) as at')->pluck('at', 'course_id'),
        ]);

        $result = [];
        foreach ($startedAt as $courseId => $start) {
            $days = [];
            for ($day = $from; $day->lte($today); $day = $day->addDay()) {
                $state = match (true) {
                    isset($active[$courseId][$day->toDateString()]) => 'on',
                    $day->lt($start->startOfDay()) => 'before',
                    default => 'off',
                };
                $days[] = ['date' => $day, 'state' => $state];
            }
            $at = $last->map(fn (Collection $byCourse) => $byCourse[$courseId] ?? null)->filter()->max();
            $result[$courseId] = [
                'xp' => (int) ($xp[$courseId] ?? 0),
                'last' => $at ? CarbonImmutable::parse($at) : null,
                'days' => $days,
            ];
        }

        return $result;
    }

    /**
     * Días (con su curso) en que hubo filas de `$model` desde `$from`.
     *
     * @param  class-string<StepAttempt|XpTransaction>  $model
     * @param  list<int>  $courseIds
     * @return Collection<int, array{0: int, 1: string}>
     */
    private static function days(string $model, User $student, array $courseIds, CarbonImmutable $from): Collection
    {
        return $model::where('user_id', $student->id)->whereIn('course_id', $courseIds)
            ->where('created_at', '>=', $from)
            ->selectRaw('course_id, DATE(created_at) as day')->distinct()->get()
            ->map(fn ($row) => [(int) $row->course_id, (string) $row->day]);
    }
}
