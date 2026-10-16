<?php

namespace App\Livewire\Admin\Students;

use App\Models\Cohort;
use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\User;
use App\Services\DelayedStudents;
use App\Services\TeacherScope;
use Flux\Flux;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;

/**
 * Alumnos demorados: con el abono vigente y sin avanzar hace DelayedStudents::DAYS días o más. El docente ve
 * a los de sus comisiones (TeacherScope) y les manda un aviso (mail + campanita, con copia interna).
 */
#[Title('Alumnos demorados')]
class Delayed extends Component
{
    #[Url(as: 'curso', except: '')]
    public string $courseId = '';

    public ?int $studentId = null;

    public ?int $remindCourseId = null;

    public string $body = '';

    public function open(DelayedStudents $delayed, int $studentId, int $courseId): void
    {
        $student = User::findOrFail($studentId);
        $course = Course::findOrFail($courseId);
        $this->authorize('remindDelayed', [$student, $course]);

        $row = $delayed->for(auth()->user(), $course->id)->first(fn ($row) => $row['student']->id === $student->id);
        $this->studentId = $student->id;
        $this->remindCourseId = $course->id;
        $this->body = DelayedStudents::defaultBody($student, $course, $row['days'] ?? DelayedStudents::DAYS);
        $this->resetErrorBag();
        Flux::modal('remind')->show();
    }

    public function send(DelayedStudents $delayed): void
    {
        $this->validate(['body' => ['required', 'string', 'min:10', 'max:2000']], [], ['body' => 'mensaje']);
        $student = User::findOrFail($this->studentId);
        $course = Course::findOrFail($this->remindCourseId);
        $this->authorize('remindDelayed', [$student, $course]);

        $delayed->remind(auth()->user(), $student, $course, trim($this->body));
        $this->reset('studentId', 'remindCourseId', 'body');
        Flux::modal('remind')->close();
        Flux::toast(variant: 'success', text: 'Aviso enviado a '.$student->fullName().' (mail y campanita).');
    }

    public function render(DelayedStudents $delayed, TeacherScope $scope)
    {
        $viewer = auth()->user();
        $rows = $delayed->for($viewer, $this->courseId === '' ? null : (int) $this->courseId);
        $courses = Course::whereIn('id', $viewer->isAdmin()
            ? CourseSubscription::active()->select('course_id')
            : Cohort::whereIn('id', $scope->cohortIds($viewer) ?: [0])->select('course_id'))
            ->orderBy('title')->get(['id', 'title']);

        return view('livewire.admin.students.delayed', [
            'rows' => $rows,
            'courses' => $courses,
            'reminding' => $this->studentId ? User::find($this->studentId) : null,
            'remindCourse' => $this->remindCourseId ? Course::find($this->remindCourseId) : null,
        ]);
    }
}
