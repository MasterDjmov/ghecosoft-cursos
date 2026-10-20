<?php

namespace App\Support;

use App\Models\Node;
use App\Models\NodeStep;
use App\Models\StepAttempt;
use App\Models\User;
use Carbon\CarbonInterface;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Query\Builder as QueryBuilder;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

/**
 * D107 fase 2: los números del panel *Admin → Estadísticas* que salen de lo que registra ActivityLog (intentos de
 * las micro-misiones y visitas a los nodos) y de los accesos (D109). Cuentan solo los alumnos de `$students` (una
 * consulta que elige users.id: todos, los de una comisión, los del docente o uno solo) y, si se pasan, los cursos
 * de `$courseIds` (los de las comisiones del docente).
 */
class ProgressStats
{
    /**
     * @param  Builder<User>  $students
     * @param  list<int>|null  $courseIds
     */
    public function __construct(
        private Builder $students,
        private ?int $courseId = null,
        private ?CarbonInterface $since = null,
        private ?array $courseIds = null,
    ) {}

    /** Intentos de los alumnos elegidos, en el curso y el período. */
    private function attempts(): Builder
    {
        return StepAttempt::query()
            ->whereIn('step_attempts.user_id', $this->students)
            ->when($this->courseId, fn ($q) => $q->where('step_attempts.course_id', $this->courseId))
            ->when($this->courseIds !== null, fn ($q) => $q->whereIn('step_attempts.course_id', $this->courseIds ?: [0]))
            ->when($this->since, fn ($q) => $q->where('step_attempts.created_at', '>=', $this->since));
    }

    private function visits(): QueryBuilder
    {
        return DB::table('node_visits')
            ->whereIn('node_visits.user_id', $this->students)
            ->when($this->courseId, fn ($q) => $q->where('node_visits.course_id', $this->courseId))
            ->when($this->courseIds !== null, fn ($q) => $q->whereIn('node_visits.course_id', $this->courseIds ?: [0]))
            ->when($this->since, fn ($q) => $q->where('node_visits.visited_on', '>=', $this->since->toDateString()));
    }

    /** @return array{students: int, attempts: int, fails: int, success_rate: ?int, visits: int, stuck: int} */
    public function summary(): array
    {
        $row = $this->attempts()->selectRaw('COUNT(*) as total, SUM(passed = 0) as fails')->first();
        $total = (int) $row->total;
        $fails = (int) $row->fails;
        $active = $this->attempts()->distinct()->pluck('step_attempts.user_id')
            ->merge($this->visits()->distinct()->pluck('node_visits.user_id'))->unique()->count();

        return [
            'students' => $active,
            'attempts' => $total,
            'fails' => $fails,
            'success_rate' => $total > 0 ? (int) round(100 * ($total - $fails) / $total) : null,
            'visits' => (int) $this->visits()->sum('views'),
            'stuck' => $this->stuck()->count(),
        ];
    }

    /**
     * Desde dónde entran (D109): alumnos y días de acceso por tipo de aparato. Los accesos no son de un curso:
     * con un curso elegido, cuentan los alumnos que tienen actividad en él.
     *
     * @return Collection<int, array{device: string, label: string, students: int, days: int, percent: int}>
     */
    public function devices(): Collection
    {
        $users = $this->courseId ? $this->attempts()->select('step_attempts.user_id')->union($this->visits()->select('node_visits.user_id')) : $this->students;
        $rows = DB::table('user_accesses')
            ->whereIn('user_id', $users)
            ->when($this->since, fn ($q) => $q->where('accessed_on', '>=', $this->since->toDateString()))
            ->selectRaw('device, COUNT(DISTINCT user_id) as students, COUNT(DISTINCT user_id, accessed_on) as days')
            ->groupBy('device')->get();
        $total = max(1, (int) $rows->sum('days'));
        $labels = ['desktop' => 'Compu', 'mobile' => 'Celular', 'tablet' => 'Tablet'];

        return $rows->map(fn ($row) => [
            'device' => $row->device,
            'label' => $labels[$row->device] ?? ucfirst($row->device),
            'students' => (int) $row->students,
            'days' => (int) $row->days,
            'percent' => (int) round(100 * $row->days / $total),
        ])->sortByDesc('days')->values();
    }

    /**
     * Embudo de un curso, capítulo por capítulo (en el orden de los códigos): cuántos alumnos lo abrieron, cuántos
     * lo miraron y cuántos superaron todas sus micro-misiones.
     *
     * @return Collection<int, array{id: int, code: string, title: string, steps: int, unlocked: int, seen: int, finished: ?int}>
     */
    public function funnel(): Collection
    {
        if (! $this->courseId) {
            return collect();
        }
        $nodes = Node::where('course_id', $this->courseId)->where('is_published', true)->withCount('steps')->orderBy('code')->get(['id', 'code', 'title']);

        $unlocked = DB::table('node_unlocks')->whereIn('node_id', $nodes->pluck('id'))->whereIn('user_id', $this->students)
            ->when($this->since, fn ($q) => $q->where('unlocked_at', '>=', $this->since))
            ->groupBy('node_id')->selectRaw('node_id, COUNT(DISTINCT user_id) as n')->pluck('n', 'node_id');
        $seen = $this->visits()->groupBy('node_visits.node_id')->selectRaw('node_visits.node_id, COUNT(DISTINCT node_visits.user_id) as n')->pluck('n', 'node_id');
        // Quién superó todas: alumnos con tantas micro-misiones superadas como tiene el nodo.
        $finished = DB::table('node_step_completions as c')->join('node_steps as s', 's.id', '=', 'c.node_step_id')
            ->whereIn('s.node_id', $nodes->pluck('id'))->whereIn('c.user_id', $this->students)
            ->groupBy('s.node_id', 'c.user_id')
            ->when($this->since, fn ($q) => $q->havingRaw('MAX(c.completed_at) >= ?', [$this->since]))
            ->selectRaw('s.node_id, c.user_id, COUNT(*) as done')->get()
            ->filter(fn ($row) => $row->done >= ($nodes->firstWhere('id', $row->node_id)?->steps_count ?? PHP_INT_MAX))
            ->countBy('node_id');

        return $nodes->map(fn (Node $node) => [
            'id' => $node->id,
            'code' => $node->code,
            'title' => $node->title,
            'steps' => $node->steps_count,
            'unlocked' => (int) ($unlocked[$node->id] ?? 0),
            'seen' => (int) ($seen[$node->id] ?? 0),
            'finished' => $node->steps_count > 0 ? (int) ($finished[$node->id] ?? 0) : null,
        ])->filter(fn (array $row) => $row['unlocked'] + $row['seen'] > 0)->values();
    }

    /**
     * Las micro-misiones con más fallos: cuántos alumnos fallaron, cuántos siguen sin superarla, intentos por
     * acierto y las respuestas equivocadas que más se repiten.
     *
     * @return Collection<int, array<string, mixed>>
     */
    public function hardestSteps(int $limit = 10): Collection
    {
        $rows = $this->attempts()
            ->selectRaw('node_step_id, COUNT(*) as total, SUM(passed = 0) as fails, SUM(passed = 1) as passes, COUNT(DISTINCT CASE WHEN passed = 0 THEN user_id END) as students')
            ->groupBy('node_step_id')->havingRaw('SUM(passed = 0) > 0')
            ->orderByDesc('fails')->limit($limit)->get();
        if ($rows->isEmpty()) {
            return collect();
        }
        $ids = $rows->pluck('node_step_id');
        $steps = NodeStep::with('node:id,course_id,code,title', 'node.course:id,title')->whereIn('id', $ids)->get()->keyBy('id');
        // Alumnos que fallaron y todavía no la superaron.
        $pending = $this->attempts()->whereIn('node_step_id', $ids)->where('passed', false)
            ->whereNotExists(fn (QueryBuilder $q) => $q->from('node_step_completions as c')
                ->whereColumn('c.user_id', 'step_attempts.user_id')->whereColumn('c.node_step_id', 'step_attempts.node_step_id'))
            ->groupBy('node_step_id')->selectRaw('node_step_id, COUNT(DISTINCT step_attempts.user_id) as n')->pluck('n', 'node_step_id');
        $answers = $this->attempts()->whereIn('node_step_id', $ids)->where('passed', false)->whereNotNull('answer')
            ->selectRaw('node_step_id, answer, COUNT(*) as times, COUNT(DISTINCT user_id) as students')
            ->groupBy('node_step_id', 'answer')->orderByDesc('times')->get()->groupBy('node_step_id');

        return $rows->filter(fn ($row) => $steps->has($row->node_step_id))->map(function ($row) use ($steps, $pending, $answers) {
            $step = $steps[$row->node_step_id];

            return [
                'id' => $step->id,
                'code' => $step->code,
                'title' => $step->title ?: $step->code,
                'node' => $step->node->code.' · '.$step->node->title,
                'course' => $step->node->course->title,
                'fails' => (int) $row->fails,
                'students' => (int) $row->students,
                'pending' => (int) ($pending[$step->id] ?? 0),
                // Intentos por cada acierto: 1 es que sale de una.
                'per_pass' => (int) $row->passes > 0 ? round($row->total / $row->passes, 1) : null,
                'answers' => ($answers[$step->id] ?? collect())->take(3)->map(fn ($a) => ['text' => $a->answer, 'times' => (int) $a->times, 'students' => (int) $a->students])->values(),
            ];
        })->values();
    }

    /**
     * Alumnos trabados: con alguna micro-misión fallada StudentJourney::STUCK_FAILS veces o más y sin superar.
     * Un renglón por alumno y curso, con las micro-misiones donde se traban.
     *
     * @return Collection<int, array<string, mixed>>
     */
    public function stuck(int $limit = 50): Collection
    {
        $rows = $this->attempts()->where('passed', false)
            ->whereNotExists(fn (QueryBuilder $q) => $q->from('node_step_completions as c')
                ->whereColumn('c.user_id', 'step_attempts.user_id')->whereColumn('c.node_step_id', 'step_attempts.node_step_id'))
            ->selectRaw('step_attempts.user_id, step_attempts.course_id, node_step_id, COUNT(*) as fails, MAX(created_at) as last_at')
            ->groupBy('step_attempts.user_id', 'step_attempts.course_id', 'node_step_id')
            ->havingRaw('COUNT(*) >= ?', [StudentJourney::STUCK_FAILS])
            ->orderByDesc('last_at')->get();
        if ($rows->isEmpty()) {
            return collect();
        }
        $users = User::whereIn('id', $rows->pluck('user_id'))->get()->keyBy('id');
        $steps = NodeStep::with('node:id,course_id,code', 'node.course:id,title,slug')->whereIn('id', $rows->pluck('node_step_id'))->get()->keyBy('id');

        return $rows->groupBy(fn ($row) => $row->user_id.'-'.$row->course_id)
            ->map(function (Collection $group) use ($users, $steps) {
                $first = $group->first();
                $course = $steps[$first->node_step_id]->node->course;

                return [
                    'student' => $users[$first->user_id],
                    'course' => $course,
                    'last_at' => now()->parse($group->max('last_at')),
                    'steps' => $group->map(fn ($row) => ['code' => $steps[$row->node_step_id]->node->code.' · '.$steps[$row->node_step_id]->code, 'title' => $steps[$row->node_step_id]->title, 'fails' => (int) $row->fails])->values(),
                ];
            })->sortByDesc('last_at')->take($limit)->values();
    }
}
