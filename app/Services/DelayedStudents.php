<?php

namespace App\Services;

use App\Enums\Role;
use App\Models\Cohort;
use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\DelayReminder;
use App\Models\User;
use App\Notifications\PlatformNotification;
use Carbon\CarbonInterface;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

/**
 * Alumnos demorados: con el abono vigente en un curso y sin avanzar en él hace DAYS días o más. Avanzar es
 * entregar una práctica, superar una micro-misión o abrir un nodo; si todavía no hizo nada, cuenta desde que
 * empezó el abono. Se calcula al mirar (sin cron). El docente ve a los de sus comisiones, en el curso de cada
 * una (TeacherScope); el administrador, a todos. El aviso le llega al alumno por mail y a la campanita, y queda
 * la copia interna en `delay_reminders`.
 */
class DelayedStudents
{
    public const DAYS = 7;

    public function __construct(private readonly TeacherScope $scope) {}

    /**
     * @return Collection<int, array{student: User, course: Course, cohort: ?Cohort, last: CarbonInterface, days: int, what: string, reminded: ?DelayReminder}>
     */
    public function for(User $viewer, ?int $courseId = null): Collection
    {
        $subscriptions = CourseSubscription::active()
            ->with(['user', 'course', 'cohort'])
            ->whereHas('user', fn ($q) => $q->where('role', Role::Student)->whereNull('blocked_at'))
            ->when(! $viewer->isAdmin(), fn ($q) => $q->whereIn('cohort_id', $this->scope->cohortIds($viewer) ?: [0]))
            ->when($courseId, fn ($q) => $q->where('course_id', $courseId))
            ->orderByDesc('ends_at')
            ->get()
            ->unique(fn ($s) => $s->user_id.'-'.$s->course_id);

        if ($subscriptions->isEmpty()) {
            return collect();
        }

        $users = $subscriptions->pluck('user_id')->unique()->all();
        $courses = $subscriptions->pluck('course_id')->unique()->all();
        $progress = $this->lastProgress($users, $courses);
        $reminders = DelayReminder::whereIn('user_id', $users)->whereIn('course_id', $courses)
            ->orderByDesc('created_at')->get()->unique(fn ($r) => $r->user_id.'-'.$r->course_id)
            ->keyBy(fn ($r) => $r->user_id.'-'.$r->course_id);
        $limit = now()->subDays(self::DAYS);

        return $subscriptions->map(function (CourseSubscription $subscription) use ($progress, $reminders) {
            $key = $subscription->user_id.'-'.$subscription->course_id;
            [$last, $what] = $progress[$key] ?? [null, null];
            if ($last === null || $last->lt($subscription->starts_at)) {
                [$last, $what] = [$subscription->starts_at, 'Empezó el abono'];
            }

            return [
                'student' => $subscription->user,
                'course' => $subscription->course,
                'cohort' => $subscription->cohort,
                'last' => $last,
                'days' => (int) $last->diffInDays(now()),
                'what' => $what,
                'reminded' => $reminders->get($key),
            ];
        })->filter(fn ($row) => $row['last']->lte($limit))
            ->sortByDesc('days')->values();
    }

    /** El aviso: mail y campanita al alumno, y la copia interna. */
    public function remind(User $sender, User $student, Course $course, string $body): DelayReminder
    {
        $reminder = DelayReminder::create([
            'user_id' => $student->id,
            'course_id' => $course->id,
            'sent_by' => $sender->id,
            'body' => $body,
            'created_at' => now(),
        ]);

        $student->notify(new PlatformNotification(
            'delay-reminder',
            '¿Seguimos con «'.$course->title.'»?',
            $body,
            route('student.tree', $course),
            'clock',
        ));

        return $reminder;
    }

    /** El texto que se propone (el docente lo puede cambiar antes de mandarlo). */
    public static function defaultBody(User $student, Course $course, int $days): string
    {
        return 'Hola, '.$student->name.'. Hace '.$days.' días que no avanzás en «'.$course->title.'». '
            .'¿Te trabaste en algo? Escribime y lo vemos juntos, o entrá cuando puedas y seguí desde donde quedaste: '
            .'tu abono sigue vigente.';
    }

    /**
     * Lo último que hizo cada alumno en cada curso.
     *
     * @param  list<int>  $users
     * @param  list<int>  $courses
     * @return array<string, array{0: CarbonInterface, 1: string}>
     */
    private function lastProgress(array $users, array $courses): array
    {
        $sources = [
            'Entregó una práctica' => DB::table('submissions')->join('practices', 'practices.id', '=', 'submissions.practice_id')
                ->join('nodes', 'nodes.id', '=', 'practices.node_id')
                ->selectRaw('submissions.user_id, nodes.course_id, MAX(submissions.created_at) as last_at')
                ->whereIn('submissions.user_id', $users)->whereIn('nodes.course_id', $courses)
                ->groupBy('submissions.user_id', 'nodes.course_id'),
            'Superó una micro-misión' => DB::table('node_step_completions')->join('node_steps', 'node_steps.id', '=', 'node_step_completions.node_step_id')
                ->join('nodes', 'nodes.id', '=', 'node_steps.node_id')
                ->selectRaw('node_step_completions.user_id, nodes.course_id, MAX(node_step_completions.completed_at) as last_at')
                ->whereIn('node_step_completions.user_id', $users)->whereIn('nodes.course_id', $courses)
                ->groupBy('node_step_completions.user_id', 'nodes.course_id'),
            'Abrió un nodo' => DB::table('node_unlocks')->join('nodes', 'nodes.id', '=', 'node_unlocks.node_id')
                ->selectRaw('node_unlocks.user_id, nodes.course_id, MAX(node_unlocks.unlocked_at) as last_at')
                ->whereIn('node_unlocks.user_id', $users)->whereIn('nodes.course_id', $courses)
                ->groupBy('node_unlocks.user_id', 'nodes.course_id'),
        ];

        $last = [];
        foreach ($sources as $what => $query) {
            foreach ($query->get() as $row) {
                if ($row->last_at === null) {
                    continue;
                }
                $key = $row->user_id.'-'.$row->course_id;
                $at = now()->parse($row->last_at);
                if (! isset($last[$key]) || $at->gt($last[$key][0])) {
                    $last[$key] = [$at, $what];
                }
            }
        }

        return $last;
    }
}
