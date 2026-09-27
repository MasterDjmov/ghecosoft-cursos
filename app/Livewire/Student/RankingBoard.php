<?php

namespace App\Livewire\Student;

use App\Models\Course;
use App\Services\Ranking;
use App\Services\TreeAccess;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Top 10 del curso (entre compañeros) o global (solo perfiles públicos). */
#[Title('Ranking')]
class RankingBoard extends Component
{
    public ?Course $course = null;

    public function mount(?Course $course = null): void
    {
        if ($course?->exists) {
            // El ranking del curso lo ven los compañeros que entraron al curso (y el docente).
            $this->authorize('viewTree', $course);
            $this->course = $course;
        }
    }

    public function render(Ranking $ranking, TreeAccess $access)
    {
        $user = auth()->user();
        $rows = $this->course ? $ranking->forCourse($this->course) : $ranking->global();

        return view('livewire.student.ranking-board', [
            'top' => $rows->take(Ranking::TOP),
            'me' => $ranking->positionOf($rows, $user),
            'courses' => Course::where('is_published', true)->orderBy('position')->get()
                ->filter(fn (Course $course) => $user->isAdmin() || $access->isRootOpen($user, $course)),
            'publicBlocker' => $user->publicProfileBlocker(),
        ])->title($this->course ? 'Ranking · '.$this->course->title : 'Ranking global');
    }
}
