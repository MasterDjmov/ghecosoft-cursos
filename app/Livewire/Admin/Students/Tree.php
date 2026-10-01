<?php

namespace App\Livewire\Admin\Students;

use App\Models\Course;
use App\Models\User;
use App\Services\TreeAccess;
use App\Support\TreeGraph;
use Livewire\Attributes\Title;
use Livewire\Component;

/** El árbol de avance de un alumno en un curso, solo para mirar (como el del CV, D64). Administrador y su docente. */
#[Title('Árbol del alumno')]
class Tree extends Component
{
    public User $user;

    public Course $course;

    public function mount(User $user, Course $course): void
    {
        abort_unless($user->isStudent(), 404);
        $this->authorize('viewProgress', [$user, $course]);
    }

    public function render()
    {
        $graph = TreeGraph::forVisitor($this->course, $this->user);
        // El avance cuenta el camino principal, igual que el CV (las Sendas y los extras suman aparte).
        $trunkIds = $this->course->nodes()->where('is_published', true)->trunk()->pluck('id')->flip();

        return view('livewire.admin.students.tree', [
            'graph' => $graph,
            'total' => $trunkIds->count(),
            'completed' => collect($graph['nodes'])->filter(fn ($n) => $trunkIds->has($n['id']) && $n['state'] === TreeAccess::STATE_COMPLETED)->count(),
            'canSeeFile' => auth()->user()->can('viewStudent', $this->user),
        ]);
    }
}
