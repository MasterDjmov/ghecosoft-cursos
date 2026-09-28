<?php

namespace App\Services;

use App\Enums\Role;
use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\Level;
use App\Models\RankingSnapshot;
use App\Models\User;
use App\Models\XpTransaction;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Cache;

/**
 * Rankings por XP (la XP nunca baja: mide constancia y avance, no notas).
 * - Por curso: top 10 entre compañeros (quienes tuvieron abono en el curso).
 * - Global: solo quienes tienen el perfil público (opt-in, G9/G10/G12).
 * Se guardan 5 minutos en caché, como arrays: el caché no deserializa clases
 * (`cache.serializable_classes`), así que una Collection volvería rota.
 */
class Ranking
{
    public const TOP = 10;

    /** @return Collection<int, array{position: int, user_id: int, name: string, xp: int}> */
    public function forCourse(Course $course): Collection
    {
        return collect(Cache::remember("ranking.course.{$course->id}", 300, function () use ($course) {
            $classmates = CourseSubscription::where('course_id', $course->id)->distinct()->pluck('user_id');

            $totals = XpTransaction::where('course_id', $course->id)
                ->whereIn('user_id', $classmates)
                ->groupBy('user_id')
                ->selectRaw('user_id, SUM(amount) as xp, MAX(created_at) as last_at')
                ->having('xp', '>', 0)
                ->orderByDesc('xp')
                ->orderBy('last_at')
                ->get();

            return $this->rows($totals->map(fn ($row) => ['user_id' => $row->user_id, 'xp' => (int) $row->xp]))->all();
        }));
    }

    /** @return Collection<int, array{position: int, user_id: int, name: string, xp: int}> */
    public function global(): Collection
    {
        return collect(Cache::remember('ranking.global', 300, function () {
            $candidates = User::where('role', Role::Student)->where('cv_public', true)->where('xp_total', '>', 0)
                ->orderByDesc('xp_total')->get()
                ->filter(fn (User $user) => $user->hasPublicProfile());

            return $this->rows($candidates->map(fn (User $user) => ['user_id' => $user->id, 'xp' => $user->xp_total]))->all();
        }));
    }

    /**
     * Top de la landing: héroe, cómo figura en el ranking, rango, insignias y XP.
     * Nunca el usuario de login ni datos personales (decidido 2026-09-27).
     *
     * @return Collection<int, array{position: int, hero: ?string, name: string, level: ?string, badges: int, xp: int, trend: ?int, new: bool}>
     */
    public function publicTop(): Collection
    {
        $rows = $this->global();
        $trends = $this->trends($rows);
        $top = $rows->take(self::TOP);
        $users = User::withCount('badges')->whereIn('id', $top->pluck('user_id'))->get()->keyBy('id');

        return $top->map(fn (array $row) => [
            'position' => $row['position'],
            'hero' => $row['hero'],
            'name' => $row['name'],
            'level' => Level::forXp($row['xp'])?->name(),
            'badges' => (int) ($users[$row['user_id']]->badges_count ?? 0),
            'xp' => $row['xp'],
            'trend' => $trends[$row['user_id']] ?? null,
            'new' => $trends !== [] && ! array_key_exists($row['user_id'], $trends),
        ]);
    }

    /**
     * Tendencia: cuántos puestos subió (+) o bajó (−) desde la foto del día anterior.
     * La foto de hoy se guarda la primera vez que alguien carga el ranking (sin cron).
     * Vacío si todavía no hay una foto anterior; sin clave, si ese alumno no estaba.
     *
     * @return array<int, int>
     */
    public function trends(Collection $rows): array
    {
        $today = today()->toDateString();
        if ($rows->isNotEmpty() && ! RankingSnapshot::whereDate('taken_on', $today)->exists()) {
            RankingSnapshot::insertOrIgnore($rows->map(fn (array $row) => [
                'taken_on' => $today, 'user_id' => $row['user_id'], 'position' => $row['position'],
            ])->all());
        }

        $previousDay = RankingSnapshot::whereDate('taken_on', '<', $today)->max('taken_on');
        if (! $previousDay) {
            return [];
        }
        $previous = RankingSnapshot::whereDate('taken_on', $previousDay)->pluck('position', 'user_id');

        return $rows->filter(fn (array $row) => $previous->has($row['user_id']))
            ->mapWithKeys(fn (array $row) => [$row['user_id'] => $previous[$row['user_id']] - $row['position']])
            ->all();
    }

    /** Posición de un alumno en una lista completa (aunque esté fuera del top). */
    public function positionOf(Collection $rows, User $user): ?array
    {
        return $rows->firstWhere('user_id', $user->id);
    }

    public static function forget(?Course $course = null): void
    {
        Cache::forget('ranking.global');
        if ($course) {
            Cache::forget("ranking.course.{$course->id}");
        }
    }

    /** @param  Collection<int, array{user_id: int, xp: int}>  $totals */
    private function rows(Collection $totals): Collection
    {
        $users = User::whereIn('id', $totals->pluck('user_id'))->get()->keyBy('id');

        return $totals->values()->map(fn (array $row, int $index) => [
            'position' => $index + 1,
            'user_id' => $row['user_id'],
            'name' => $users[$row['user_id']]?->rankingName() ?? '—',
            'hero' => $users[$row['user_id']]?->hero_name,
            'username' => $users[$row['user_id']]?->hasPublicProfile() ? $users[$row['user_id']]->username : null,
            'xp' => $row['xp'],
        ]);
    }
}
