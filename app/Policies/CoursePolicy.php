<?php

namespace App\Policies;

use App\Models\Course;
use App\Models\User;
use App\Services\TreeAccess;

class CoursePolicy
{
    public function __construct(private readonly TreeAccess $access) {}

    /** La ficha del curso (descripción, inscripción) es visible si está publicado. */
    public function view(User $user, Course $course): bool
    {
        return $course->is_published;
    }

    /**
     * El árbol se ve con el raíz abierto (y para siempre, aunque venza el abono) o mientras
     * se prueba la Clase 0 (D71): los demás nodos se ven cerrados, con su nombre y precio.
     */
    public function viewTree(User $user, Course $course): bool
    {
        return $user->isStaff() || $this->access->isRootOpen($user, $course) || $this->access->canTryCourse($user, $course);
    }

    /** El ranking del curso, solo para los que entraron (la Clase 0 de prueba no cuenta, D71). */
    public function viewRanking(User $user, Course $course): bool
    {
        return $user->isStaff() || $this->access->isRootOpen($user, $course);
    }
}
