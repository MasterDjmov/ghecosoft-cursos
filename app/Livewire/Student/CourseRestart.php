<?php

namespace App\Livewire\Student;

use App\Models\Course;
use App\Services\CourseRestarter;
use Flux\Flux;
use Illuminate\Support\Str;
use Livewire\Attributes\Locked;
use Livewire\Component;

/** «Reiniciar este curso» (D117): cada uno borra su propio progreso en el curso, escribiendo REINICIAR para confirmar. */
class CourseRestart extends Component
{
    public const WORD = 'REINICIAR';

    #[Locked]
    public Course $course;

    public string $confirmation = '';

    public function restart(CourseRestarter $restarter)
    {
        $this->authorize('restart', $this->course);

        if (Str::upper(trim($this->confirmation)) !== self::WORD) {
            $this->addError('confirmation', 'Escribí '.self::WORD.' para confirmar.');

            return null;
        }

        $restarter->restart(auth()->user(), $this->course);
        Flux::toast(variant: 'success', text: 'Listo: '.$this->course->title.' arranca de cero.');

        return $this->redirectRoute('student.tree', $this->course, navigate: true);
    }

    public function render()
    {
        return view('livewire.student.course-restart', ['word' => self::WORD]);
    }
}
