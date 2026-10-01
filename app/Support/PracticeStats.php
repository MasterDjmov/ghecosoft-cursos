<?php

namespace App\Support;

use App\Enums\Role;
use App\Models\Practice;
use App\Models\PracticeMessage;
use App\Models\Submission;
use Carbon\CarbonInterface;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

/**
 * Números del panel del administrador: cuánto se entrega, cuánto vuelve para rehacer y qué prácticas
 * eligen más o les cuestan más a los alumnos. Solo cuentan las entregas de alumnos (no las del staff).
 * Un intento que el docente mandó a rehacer cuenta como «con errores».
 */
class PracticeStats
{
    public function __construct(private ?int $courseId = null, private ?CarbonInterface $since = null) {}

    /** Entregas de alumnos con su práctica y su nodo, filtradas por curso y período. */
    private function submissions(): Builder
    {
        return Submission::query()
            ->join('practices', 'practices.id', '=', 'submissions.practice_id')
            ->join('nodes', 'nodes.id', '=', 'practices.node_id')
            ->join('users', 'users.id', '=', 'submissions.user_id')
            ->where('users.role', Role::Student->value)
            ->when($this->courseId, fn ($q) => $q->where('nodes.course_id', $this->courseId))
            ->when($this->since, fn ($q) => $q->where('submissions.submitted_at', '>=', $this->since));
    }

    /** Las columnas que se suman en todos los cuadros. */
    private static function totals(): string
    {
        return "COUNT(*) as total,
            COUNT(DISTINCT submissions.user_id) as students,
            SUM(submissions.status = 'approved') as approved,
            SUM(submissions.status = 'redo') as redo,
            SUM(submissions.status = 'submitted') as pending,
            SUM(submissions.check_result IS NOT NULL
                AND JSON_EXTRACT(submissions.check_result, '$.passed') < JSON_EXTRACT(submissions.check_result, '$.total')) as failing";
    }

    /** % de los intentos corregidos que volvieron para rehacer. */
    private static function redoRate(int $approved, int $redo): ?int
    {
        return $approved + $redo > 0 ? (int) round(100 * $redo / ($approved + $redo)) : null;
    }

    /** Consultas que escribieron los alumnos, por práctica. @return Collection<int, int> */
    private function questions(): Collection
    {
        return PracticeMessage::query()
            ->join('practices', 'practices.id', '=', 'practice_messages.practice_id')
            ->join('nodes', 'nodes.id', '=', 'practices.node_id')
            ->whereColumn('practice_messages.author_id', 'practice_messages.student_id')
            ->when($this->courseId, fn ($q) => $q->where('nodes.course_id', $this->courseId))
            ->when($this->since, fn ($q) => $q->where('practice_messages.created_at', '>=', $this->since))
            ->groupBy('practice_messages.practice_id')
            ->pluck(DB::raw('COUNT(*)'), 'practice_messages.practice_id')
            ->map(fn ($count) => (int) $count);
    }

    /** @return array{total: int, approved: int, redo: int, pending: int, failing: int, students: int, redo_rate: ?int, questions: int} */
    public function summary(): array
    {
        $row = $this->submissions()->selectRaw(self::totals())->first();
        $approved = (int) $row->approved;
        $redo = (int) $row->redo;

        return [
            'total' => (int) $row->total,
            'students' => (int) $row->students,
            'approved' => $approved,
            'redo' => $redo,
            'pending' => (int) $row->pending,
            'failing' => (int) $row->failing,
            'redo_rate' => self::redoRate($approved, $redo),
            'questions' => $this->questions()->sum(),
        ];
    }

    /** Un renglón por curso, en el orden del catálogo. */
    public function byCourse(): Collection
    {
        return $this->submissions()
            ->join('courses', 'courses.id', '=', 'nodes.course_id')
            ->selectRaw('courses.id, courses.title, '.self::totals())
            ->groupBy('courses.id', 'courses.title', 'courses.position')
            ->orderBy('courses.position')
            ->get()
            ->map(fn ($row) => [
                'id' => $row->id,
                'title' => $row->title,
                'total' => (int) $row->total,
                'students' => (int) $row->students,
                'approved' => (int) $row->approved,
                'redo' => (int) $row->redo,
                'pending' => (int) $row->pending,
                'failing' => (int) $row->failing,
                'redo_rate' => self::redoRate((int) $row->approved, (int) $row->redo),
            ]);
    }

    /** Todas las prácticas con entregas, con sus números. */
    private function practices(): Collection
    {
        $questions = $this->questions();

        $rows = $this->submissions()
            ->join('courses', 'courses.id', '=', 'nodes.course_id')
            ->selectRaw('practices.id, practices.title, practices.is_required, nodes.title as node_title, courses.title as course_title, '.self::totals())
            ->groupBy('practices.id', 'practices.title', 'practices.is_required', 'nodes.title', 'courses.title')
            ->get()
            ->map(fn ($row) => [
                'id' => $row->id,
                'title' => $row->title,
                'is_required' => (bool) $row->is_required,
                'node' => $row->node_title,
                'course' => $row->course_title,
                'students' => (int) $row->students,
                'total' => (int) $row->total,
                'redo' => (int) $row->redo,
                'failing' => (int) $row->failing,
                'questions' => $questions[$row->id] ?? 0,
                // Intentos por alumno: 1 es que salió de una; más, que tuvieron que volver.
                'attempts' => round($row->total / max(1, $row->students), 1),
                'redo_rate' => self::redoRate((int) $row->approved, (int) $row->redo),
            ]);

        // Las que tienen consultas pero ninguna entrega: el alumno preguntó y todavía no pudo entregar.
        $onlyQuestions = Practice::with('node.course:id,title')
            ->whereIn('id', $questions->keys()->diff($rows->pluck('id')))
            ->get()
            ->map(fn (Practice $practice) => [
                'id' => $practice->id,
                'title' => $practice->title,
                'is_required' => $practice->is_required,
                'node' => $practice->node->title,
                'course' => $practice->node->course->title,
                'students' => 0,
                'total' => 0,
                'redo' => 0,
                'failing' => 0,
                'questions' => $questions[$practice->id],
                'attempts' => 0.0,
                'redo_rate' => null,
            ]);

        return $rows->concat($onlyQuestions);
    }

    /** Las que más alumnos hicieron (las optativas son las que eligen). */
    public function mostChosen(int $limit = 8): Collection
    {
        return $this->practices()->where('students', '>', 0)->sortBy([['students', 'desc'], ['total', 'desc']])->take($limit)->values();
    }

    /** Donde más se traban: más intentos para rehacer, después más intentos por alumno y más consultas. */
    public function hardest(int $limit = 8): Collection
    {
        return $this->practices()
            ->filter(fn (array $p) => $p['redo'] > 0 || $p['failing'] > 0 || $p['questions'] > 0)
            ->sortBy([['redo', 'desc'], ['attempts', 'desc'], ['questions', 'desc']])
            ->take($limit)
            ->values();
    }
}
