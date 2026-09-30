<?php

namespace App\Livewire\Student;

use App\Exceptions\NodeLocked;
use App\Models\Course;
use App\Models\Node;
use App\Services\NodeUnlocker;
use App\Services\TreeAccess;
use App\Support\Story;
use App\Support\TreeGraph;
use App\Support\UnlockMessages;
use Flux\Flux;
use Illuminate\Support\Facades\RateLimiter;
use Livewire\Attributes\Title;
use Livewire\Component;

/** El árbol del curso para el alumno: lista por rama o dibujado, y abrir nodos. */
#[Title('Árbol')]
class CourseTree extends Component
{
    public Course $course;

    public ?int $selectedNodeId = null;

    public function mount(Course $course)
    {
        $this->authorize('view', $course);

        // Sin el raíz abierto, el árbol no se ve: a la ficha del curso.
        if (! auth()->user()->can('viewTree', $course)) {
            return $this->redirectRoute('student.course', $course, navigate: true);
        }
    }

    /** Tocar un nodo cerrado: muestra precio, motivos y el botón Abrir. */
    public function selectNode(int $nodeId): void
    {
        $node = $this->visibleNode($nodeId);
        $this->selectedNodeId = $node->id;

        Flux::modal('node')->show();
    }

    public function unlock(int $nodeId, NodeUnlocker $unlocker)
    {
        $node = $this->visibleNode($nodeId);

        $key = 'unlock:'.auth()->id();
        if (RateLimiter::tooManyAttempts($key, 20)) {
            Flux::toast(variant: 'danger', text: 'Demasiados intentos. Esperá un minuto.');

            return null;
        }
        RateLimiter::hit($key, 60);

        try {
            $unlocker->unlock(auth()->user(), $node);
        } catch (NodeLocked $e) {
            Flux::toast(variant: 'danger', text: implode(' ', UnlockMessages::for(auth()->user(), $node, $e->reasons)));

            return null;
        }

        Flux::toast(variant: 'success', text: '¡Abriste «'.$node->title.'»!');

        return $this->redirectRoute('student.node', [$this->course, $node], navigate: true);
    }

    /** Un nodo del curso que el alumno puede ver en el árbol (publicado o ya abierto). */
    private function visibleNode(int $nodeId): Node
    {
        $node = $this->course->nodes()->findOrFail($nodeId);
        abort_unless($node->is_published || app(TreeAccess::class)->isUnlocked(auth()->user(), $node), 404);

        return $node;
    }

    public function render(TreeAccess $access)
    {
        $user = auth()->user();
        $graph = TreeGraph::forStudent($this->course, $user);
        $selected = $this->selectedNodeId ? collect($graph['nodes'])->firstWhere('id', $this->selectedNodeId) : null;

        return view('livewire.student.course-tree', [
            'graph' => $graph,
            'subscription' => $access->activeSubscription($user, $this->course),
            // Clase 0 de prueba (D71): todavía no abrió el raíz y no tiene abono.
            'trial' => $access->canTryCourse($user, $this->course),
            'staff' => $user->isStaff(),
            'paidUntil' => $access->paidUntil($user, $this->course),
            'selected' => $selected,
            'selectedCanUnlock' => $selected && $access->canUnlock($user, $this->course->nodes()->find($selected['id'])),
            // Historia en pantalla (Fase 9): bienvenida, rama completada y fin del curso.
            'intro' => Story::get('story.course_intro', $this->course, $user),
            'branchStory' => Story::get('story.branch_completed', $this->course, $user, requireText: false),
            'finale' => $access->isCourseCompleted($user, $this->course)
                ? Story::get('story.course_completed', $this->course, $user, requireText: false)
                : null,
        ])->title('Árbol · '.$this->course->title);
    }
}
