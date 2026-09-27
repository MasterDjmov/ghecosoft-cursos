<?php

namespace App\Livewire\Admin\Courses;

use App\Models\Course;
use App\Models\CourseSubscription;
use App\Support\Reorder;
use Livewire\Attributes\Title;
use Livewire\Component;

#[Title('Cursos')]
class Index extends Component
{
    public function togglePublished(int $id): void
    {
        $course = Course::findOrFail($id);
        $course->update(['is_published' => ! $course->is_published]);
    }

    public function sort(int $id, int $position): void
    {
        Reorder::move(Course::query(), Course::findOrFail($id), $position);
    }

    public function render()
    {
        return view('livewire.admin.courses.index', [
            'courses' => Course::withCount(['nodes', 'branches'])->orderBy('position')->orderBy('id')->get(),
            'activeStudents' => CourseSubscription::active()->selectRaw('course_id, count(distinct user_id) as total')
                ->groupBy('course_id')->pluck('total', 'course_id'),
        ]);
    }
}
