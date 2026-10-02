<?php

namespace App\Support;

use App\Enums\NodeType;
use App\Enums\SubmissionStatus;
use App\Models\Course;
use App\Models\Level;
use App\Models\Node;
use App\Models\Submission;
use App\Models\User;
use App\Services\TreeAccess;

/**
 * Qué muestra el CV: cursos y nodos completados, prácticas aprobadas,
 * insignias, nivel y fechas. **Nunca** código ni comentarios.
 */
class CvData
{
    /** @return array<string, mixed> */
    public static function for(User $user): array
    {
        $access = app(TreeAccess::class);
        $completions = $user->courseCompletions()->get()->keyBy('course_id');

        // Los cursos en los que entró (abrió el raíz).
        $courses = Course::whereHas('nodes', fn ($n) => $n->where('type', NodeType::Root)->whereHas('unlocks', fn ($u) => $u->where('user_id', $user->id)))
            ->orderBy('position')
            ->get()
            ->map(function (Course $course) use ($user, $access, $completions) {
                $nodes = $course->nodes()->where('is_published', true)->orderBy('branch_id')->orderBy('position')->get();
                $completed = $nodes->filter(fn (Node $node) => $access->isCompleted($user, $node));
                // El progreso cuenta el tronco: los extras y las Sendas suman habilidades, no porcentaje.
                $trunkIds = $course->nodes()->where('is_published', true)->trunk()->pluck('id');

                return [
                    'course' => $course,
                    'total' => $trunkIds->count(),
                    'completedCount' => $completed->whereIn('id', $trunkIds)->count(),
                    'skills' => $completed->reject->isRoot()->pluck('title')->values(),
                    'completion' => $completions[$course->id] ?? null,
                    'since' => $user->subscriptions()->where('course_id', $course->id)->min('starts_at'),
                ];
            });

        return [
            // Mis Crónicas (D80): páginas de historia desbloqueadas y piezas del portal.
            'chronicles' => (function () use ($user) {
                $book = new Chronicles($user);
                $portal = collect($book->portal(render: false));

                return ['pages' => $book->unlockedCount() - 1 - $portal->where('unlocked', true)->count(), 'pieces' => $portal->where('unlocked', true)->count(), 'totalPieces' => $portal->count()];
            })(),
            'user' => $user,
            'level' => Level::forXp($user->xp_total),
            'courses' => $courses,
            'badges' => $user->badges()->orderByPivot('awarded_at')->get(),
            'approvedPractices' => Submission::where('user_id', $user->id)->where('status', SubmissionStatus::Approved)->distinct()->count('practice_id'),
        ];
    }
}
