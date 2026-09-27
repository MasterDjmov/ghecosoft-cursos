<?php

namespace App\Livewire\Admin\Submissions;

use App\Models\Cohort;
use App\Models\Course;
use App\Models\Submission;
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

    public function updated(): void
    {
        $this->resetPage();
    }

    public function render()
    {
        $submissions = Submission::with(['user:id,name,last_name,username', 'practice.node.course'])
            ->when($this->status !== 'all', fn ($q) => $q->where('status', $this->status))
            ->when($this->courseId !== '', fn ($q) => $q->whereHas('practice.node', fn ($n) => $n->where('course_id', (int) $this->courseId)))
            ->when($this->cohortId !== '', fn ($q) => $q->whereHas('user.subscriptions', fn ($s) => $s->where('cohort_id', (int) $this->cohortId)))
            ->when(trim($this->search) !== '', function ($q) {
                $term = '%'.trim($this->search).'%';
                $q->whereHas('user', fn ($u) => $u->where('name', 'like', $term)->orWhere('last_name', 'like', $term)->orWhere('username', 'like', $term));
            })
            ->when($this->status === 'submitted', fn ($q) => $q->oldest('submitted_at'), fn ($q) => $q->latest('submitted_at'))
            ->paginate(25);

        return view('livewire.admin.submissions.index', [
            'submissions' => $submissions,
            'courses' => Course::orderBy('position')->get(['id', 'title']),
            'cohorts' => Cohort::when($this->courseId !== '', fn ($q) => $q->where('course_id', (int) $this->courseId))->orderBy('name')->get(['id', 'name']),
            'pendingCount' => Submission::where('status', 'submitted')->count(),
        ]);
    }
}
