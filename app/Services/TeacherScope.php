<?php

namespace App\Services;

use App\Models\Cohort;
use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\Practice;
use App\Models\Submission;
use App\Models\User;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Query\Builder as QueryBuilder;
use Illuminate\Support\Collection;

/**
 * Qué alcanza un docente (D72): los alumnos de sus comisiones, en el curso de cada comisión.
 * El administrador alcanza todo. Todas las pantallas y Policies del docente pasan por acá.
 */
class TeacherScope
{
    /** @var array<int, list<int>> */
    private array $cohorts = [];

    /** @return list<int> Comisiones a cargo del docente. */
    public function cohortIds(User $teacher): array
    {
        return $this->cohorts[$teacher->id] ??= Cohort::where('teacher_id', $teacher->id)->pluck('id')->map(fn ($id) => (int) $id)->all();
    }

    /** El docente tiene al alumno en alguna de sus comisiones (de cualquier curso, o de uno). */
    public function teaches(User $teacher, User $student, ?Course $course = null): bool
    {
        if ($teacher->isAdmin()) {
            return true;
        }
        if (! $teacher->isTeacher() || ! $this->cohortIds($teacher)) {
            return false;
        }

        return CourseSubscription::where('user_id', $student->id)
            ->whereIn('cohort_id', $this->cohortIds($teacher))
            ->when($course, fn ($q) => $q->where('course_id', $course->id))
            ->exists();
    }

    public function teachesPractice(User $teacher, User $student, Practice $practice): bool
    {
        return $this->teaches($teacher, $student, $practice->node->course);
    }

    /** Solo lo que corrige el docente: entregas de alumnos de sus comisiones, en ese curso. */
    public function submissions(Builder $query, User $viewer): Builder
    {
        return $this->restrict($query, $viewer, 'submissions.practice_id', 'submissions.user_id');
    }

    /** Consultas por práctica de alumnos de sus comisiones, en ese curso. */
    public function messages(Builder $query, User $viewer): Builder
    {
        return $this->restrict($query, $viewer, 'practice_messages.practice_id', 'practice_messages.student_id');
    }

    /** Alumnos de sus comisiones (de cualquier curso). */
    public function students(Builder $query, User $viewer): Builder
    {
        if ($viewer->isAdmin()) {
            return $query;
        }

        return $query->whereIn('users.id', CourseSubscription::whereIn('cohort_id', $this->cohortIds($viewer) ?: [0])->select('user_id'));
    }

    public function canSeeSubmission(User $viewer, Submission $submission): bool
    {
        return $viewer->isAdmin() || $this->submissions(Submission::whereKey($submission->id), $viewer)->exists();
    }

    /**
     * Los docentes del alumno en ese curso (para avisarles de sus entregas y consultas).
     *
     * @return Collection<int, User>
     */
    public function teachersOf(User $student, Course $course): Collection
    {
        return User::whereIn('id', Cohort::whereNotNull('teacher_id')
            ->whereIn('id', CourseSubscription::where('user_id', $student->id)->where('course_id', $course->id)->select('cohort_id'))
            ->select('teacher_id'))
            ->get();
    }

    private function restrict(Builder $query, User $viewer, string $practiceColumn, string $studentColumn): Builder
    {
        if ($viewer->isAdmin()) {
            return $query;
        }
        $cohorts = $this->cohortIds($viewer) ?: [0];

        // Un abono del alumno, en una comisión del docente, del mismo curso que la práctica.
        return $query->whereExists(fn (QueryBuilder $sub) => $sub->from('course_subscriptions as ts')
            ->join('nodes as tn', 'tn.course_id', '=', 'ts.course_id')
            ->join('practices as tp', 'tp.node_id', '=', 'tn.id')
            ->whereColumn('tp.id', $practiceColumn)
            ->whereColumn('ts.user_id', $studentColumn)
            ->whereIn('ts.cohort_id', $cohorts));
    }
}
