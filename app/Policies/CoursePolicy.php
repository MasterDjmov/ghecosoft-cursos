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

    /** El árbol se ve recién con el raíz abierto (y para siempre, aunque venza el abono). */
    public function viewTree(User $user, Course $course): bool
    {
        return $this->access->isRootOpen($user, $course);
    }
}
