<?php

namespace App\Enums;

/** Cuándo se abre un fragmento de Mis Crónicas (D80). */
enum FragmentTrigger: string
{
    case NodeCompleted = 'node_completed';
    case BranchCompleted = 'branch_completed';
    case CourseStarted = 'course_started';
    case CourseCompleted = 'course_completed';

    public function label(): string
    {
        return match ($this) {
            self::NodeCompleted => 'Al completar el nodo',
            self::BranchCompleted => 'Al terminar la rama',
            self::CourseStarted => 'Al empezar el curso',
            self::CourseCompleted => 'Al terminar el curso',
        };
    }
}
