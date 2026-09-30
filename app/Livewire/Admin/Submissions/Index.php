<?php

namespace App\Livewire\Admin\Submissions;

use App\Enums\Role;
use App\Models\Cohort;
use App\Models\Course;
use App\Models\Submission;
use App\Models\User;
use App\Services\TeacherScope;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;
use Livewire\WithPagination;

/** Bandeja de entregas: "Sin corregir" primero, las más viejas arriba. */
#[Title('Entregas')]
class Index extends Component
{
    use WithPagination;

    #[Url(as: 'estado', except: 'submitted')]
    public string $status = 'submitted';

    #[Url(as: 'curso', except: '')]
    public string $courseId = '';

    #[Url(as: 'comision', except: '')]
    public string $cohortId = '';

    #[Url(as: 'buscar', except: '')]
    public string $search = '';

    /** Solo el administrador: las de las comisiones de un docente ('none' = comisiones sin docente o alumnos sin comisión). */
    #[Url(as: 'docente', except: '')]
    public string $teacherId = '';

    public function updated(): void
    {
        $this->resetPage();
    }

    public function render(TeacherScope $scope)
    {
        $user = auth()->user();
        $teacherCohorts = $user->isAdmin() && ctype_digit($this->teacherId) ? Cohort::where('teacher_id', (int) $this->teacherId)->pluck('id') : null;

        $submissions = $scope->submissions(Submission::query(), $user)
            ->with(['user:id,name,last_name,username', 'practice.node.course'])
            ->when($this->status !== 'all', fn ($q) => $q->where('status', $this->status))
            ->when($this->courseId !== '', fn ($q) => $q->whereHas('practice.node', fn ($n) => $n->where('course_id', (int) $this->courseId)))
            // La comisión del alumno en el curso de la entrega (no la de otro curso).
            ->when($this->cohortId !== '', fn ($q) => $this->inCohorts($q, [(int) $this->cohortId]))
            ->when($teacherCohorts !== null, fn ($q) => $this->inCohorts($q, $teacherCohorts->all() ?: [0]))
            ->when(trim($this->search) !== '', function ($q) {
                $term = '%'.trim($this->search).'%';
                $q->whereHas('user', fn ($u) => $u->where('name', 'like', $term)->orWhere('last_name', 'like', $term)->orWhere('username', 'like', $term));
            })
            ->when($this->status === 'submitted', fn ($q) => $q->oldest('submitted_at'), fn ($q) => $q->latest('submitted_at'))
            ->paginate(25);

        $cohorts = Cohort::when($this->courseId !== '', fn ($q) => $q->where('course_id', (int) $this->courseId))
            ->when($user->isTeacher(), fn ($q) => $q->where('teacher_id', $user->id))
            ->when($teacherCohorts !== null, fn ($q) => $q->whereIn('id', $teacherCohorts))
            ->orderBy('name')->get(['id', 'name']);

        return view('livewire.admin.submissions.index', [
            'submissions' => $submissions,
            'courses' => Course::orderBy('position')->get(['id', 'title']),
            'cohorts' => $cohorts,
            'teachers' => $user->isAdmin() ? User::where('role', Role::Teacher)->orderBy('name')->get(['id', 'name', 'last_name']) : collect(),
            'pendingCount' => $scope->submissions(Submission::query(), $user)->where('status', 'submitted')->count(),
        ]);
    }

    /** Entregas de alumnos que, en el curso de la entrega, están en alguna de esas comisiones. */
    private function inCohorts($query, array $cohortIds)
    {
        return $query->whereExists(fn ($sub) => $sub->from('course_subscriptions as cs')
            ->join('nodes as cn', 'cn.course_id', '=', 'cs.course_id')
            ->join('practices as cp', 'cp.node_id', '=', 'cn.id')
            ->whereColumn('cp.id', 'submissions.practice_id')
            ->whereColumn('cs.user_id', 'submissions.user_id')
            ->whereIn('cs.cohort_id', $cohortIds));
    }
}
