<?php

namespace App\Livewire\Student;

use App\Models\Course;
use App\Services\Ranking;
use App\Services\TreeAccess;
use Livewire\Attributes\Title;
use Livewire\Component;

/**
 * Top 10 del curso (entre compañeros) o global (solo perfiles públicos). El global muestra además, abajo,
 * el top de cada curso en el que entró el alumno, con su puesto aunque esté fuera del top.
 */
#[Title('Ranking')]
class RankingBoard extends Component
{
    /** Cuántos se ven de cada curso en el ranking global (el top 10 completo, en la página del curso). */
    public const COURSE_TOP = 5;

    public ?Course $course = null;

    public function mount(?Course $course = null): void
    {
        if ($course?->exists) {
            // El ranking del curso lo ven los compañeros que entraron al curso (y el docente).
            $this->authorize('viewRanking', $course);
            $this->course = $course;
        }
    }

    public function render(Ranking $ranking, TreeAccess $access)
    {
        $user = auth()->user();
        $rows = $this->course ? $ranking->forCourse($this->course) : $ranking->global();
        $courses = Course::where('is_published', true)->orderBy('position')->get()
            ->filter(fn (Course $course) => $user->isAdmin() || $access->isRootOpen($user, $course));

        return view('livewire.student.ranking-board', [
            'top' => $rows->take(Ranking::TOP),
            'me' => $ranking->positionOf($rows, $user),
            'courses' => $courses,
            'byCourse' => $this->course ? collect() : $courses->map(function (Course $course) use ($ranking, $user) {
                $courseRows = $ranking->forCourse($course);

                return ['course' => $course, 'top' => $courseRows->take(self::COURSE_TOP), 'me' => $ranking->positionOf($courseRows, $user), 'count' => $courseRows->count()];
            })->values(),
            'publicBlocker' => $user->publicProfileBlocker(),
        ])->title($this->course ? 'Ranking · '.$this->course->title : 'Ranking global');
    }
}
