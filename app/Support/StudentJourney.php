<?php

namespace App\Support;

use App\Models\Course;
use App\Models\Node;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\NodeUnlock;
use App\Models\NodeVisit;
use App\Models\StepAttempt;
use App\Models\User;
use App\Services\TreeAccess;
use Carbon\CarbonInterface;
use Illuminate\Support\Collection;

/**
 * D107: el recorrido de un alumno por un curso, capítulo por capítulo: qué miró y cuándo, cuántas veces probó
 * cada micro-misión y dónde está trabado. Lo ven el administrador y su docente en el árbol del alumno.
 */
class StudentJourney
{
    /** Fallos sin acierto a partir de los cuales una micro-misión cuenta como «trabado». */
    public const STUCK_FAILS = 3;

    /** Días sin avanzar en un nodo abierto y sin terminar para marcarlo «trabado». */
    public const STUCK_DAYS = 7;

    public function __construct(private User $user, private Course $course) {}

    /**
     * Los nodos que abrió o miró, en el orden del curso.
     *
     * @param  array<int, string>  $states  estado de cada nodo (TreeAccess::STATE_*), por id
     * @return Collection<int, array<string, mixed>>
     */
    public function chapters(array $states): Collection
    {
        $unlocks = NodeUnlock::where('user_id', $this->user->id)->whereHas('node', fn ($q) => $q->where('course_id', $this->course->id))
            ->pluck('unlocked_at', 'node_id');
        $visits = NodeVisit::where('user_id', $this->user->id)->where('course_id', $this->course->id)
            ->selectRaw('node_id, MIN(first_at) as first_at, MAX(last_at) as last_at, COUNT(*) as days, SUM(views) as views')
            ->groupBy('node_id')->get()->keyBy('node_id');
        $attempts = StepAttempt::where('user_id', $this->user->id)->where('course_id', $this->course->id)
            ->selectRaw('node_step_id, SUM(passed = 0) as fails, SUM(passed = 1) as passes, MAX(created_at) as last_at')
            ->groupBy('node_step_id')->get()->keyBy('node_step_id');
        $done = NodeStepCompletion::where('user_id', $this->user->id)
            ->whereHas('step.node', fn ($q) => $q->where('course_id', $this->course->id))
            ->pluck('completed_at', 'node_step_id');

        $nodeIds = $unlocks->keys()->merge($visits->keys())->unique();

        // Por código (R00, R01-N01…, S01): la posición es dentro de cada rama.
        return Node::whereIn('id', $nodeIds)->with(['steps' => fn ($q) => $q->orderBy('position')])
            ->orderBy('code')->get()
            ->map(function (Node $node) use ($unlocks, $visits, $attempts, $done, $states) {
                $visit = $visits->get($node->id);
                $steps = $node->steps->map(fn (NodeStep $step) => [
                    'id' => $step->id,
                    'code' => $step->code,
                    'title' => $step->title,
                    'done' => $done->has($step->id),
                    'fails' => (int) ($attempts->get($step->id)?->fails ?? 0),
                    'stuck' => ! $done->has($step->id) && (int) ($attempts->get($step->id)?->fails ?? 0) >= self::STUCK_FAILS,
                ]);
                $completed = ($states[$node->id] ?? null) === TreeAccess::STATE_COMPLETED;
                $lastActivity = collect([
                    $unlocks->get($node->id),
                    $visit?->last_at,
                    ...$node->steps->map(fn (NodeStep $s) => $attempts->get($s->id)?->last_at),
                    ...$node->steps->map(fn (NodeStep $s) => $done->get($s->id)),
                ])->filter()->map(fn ($date) => $date instanceof CarbonInterface ? $date : now()->parse($date))->max();
                $idle = ! $completed && $unlocks->has($node->id) && $lastActivity && $lastActivity->lt(now()->subDays(self::STUCK_DAYS));

                return [
                    'id' => $node->id,
                    'code' => $node->code,
                    'title' => $node->title,
                    'unlocked_at' => $unlocks->get($node->id),
                    'first_seen' => $visit ? now()->parse($visit->first_at) : null,
                    'last_seen' => $visit ? now()->parse($visit->last_at) : null,
                    'days' => (int) ($visit?->days ?? 0),
                    'views' => (int) ($visit?->views ?? 0),
                    'completed' => $completed,
                    'steps' => $steps,
                    'steps_done' => $steps->where('done', true)->count(),
                    'fails' => $steps->sum('fails'),
                    'stuck_steps' => $steps->where('stuck', true)->values(),
                    'idle_since' => $idle ? $lastActivity : null,
                ];
            });
    }

    /** @return Collection<int, StepAttempt> sus últimos fallos, con la micro-misión */
    public function recentFails(int $limit = 15): Collection
    {
        return StepAttempt::where('user_id', $this->user->id)->where('course_id', $this->course->id)
            ->where('passed', false)->with('step:id,node_id,code,title')
            ->latest('id')->limit($limit)->get();
    }
}
