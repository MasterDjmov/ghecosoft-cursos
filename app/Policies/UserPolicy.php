<?php

namespace App\Policies;

use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\User;
use App\Services\TeacherScope;

/**
 * Lo que un docente puede hacer con un alumno (D72); el administrador puede todo (Gate::before).
 * El docente alcanza a los alumnos de sus comisiones.
 */
class UserPolicy
{
    public function __construct(private readonly TeacherScope $scope) {}

    /** La ficha completa (cursos, progreso, entregas). */
    public function viewStudent(User $user, User $student): bool
    {
        return $user->isTeacher() && $student->isStudent() && $this->scope->teaches($user, $student);
    }

    /** Resetear la clave, si el alumno lo pide. */
    public function resetPassword(User $user, User $student): bool
    {
        return $this->viewStudent($user, $student);
    }

    /**
     * Cambiar la comisión del alumno en un curso: el docente lo pone en una comisión suya o lo saca
     * de una suya; no mueve alumnos de la comisión de otro docente.
     */
    public function assignCohort(User $user, User $student, Course $course, ?int $cohortId): bool
    {
        if (! $user->isTeacher() || ! $student->isStudent()) {
            return false;
        }
        $mine = $this->scope->cohortIds($user);
        $current = CourseSubscription::where('user_id', $student->id)->where('course_id', $course->id)->value('cohort_id');

        return ($current === null || in_array((int) $current, $mine, true))
            && ($cohortId === null || in_array($cohortId, $mine, true));
    }

    /** Ver un alumno en el buscador para sumarlo a una comisión propia (solo nombre y usuario). */
    public function findStudent(User $user, User $student): bool
    {
        return $user->isTeacher() && $student->isStudent();
    }
}
