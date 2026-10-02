<?php

namespace App\Livewire\Admin\Students;

use App\Exceptions\NodeLocked;
use App\Models\Course;
use App\Models\User;
use App\Services\NodeUnlocker;
use App\Services\TreeAccess;
use App\Support\TreeGraph;
use App\Support\UnlockMessages;
use Flux\Flux;
use Livewire\Attributes\Title;
use Livewire\Component;

/**
 * El árbol de avance de un alumno en un curso (como el del CV, D64), para el administrador y su docente.
 * Debajo, los nodos que siguen: si el alumno se traba, se los abren con sus monedas y las mismas reglas.
 */
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

    /** Abrirle al alumno un nodo que ya puede abrir: le cobra sus monedas y le llega un aviso. */
    public function unlockFor(int $nodeId, NodeUnlocker $unlocker): void
    {
        $this->authorize('unlockFor', [$this->user, $this->course]);
        $node = $this->course->nodes()->where('is_published', true)->findOrFail($nodeId);

        try {
            $unlocker->unlock($this->user, $node, auth()->user());
        } catch (NodeLocked $e) {
            Flux::toast(variant: 'danger', text: implode(' ', UnlockMessages::for($this->user, $node, $e->reasons)));

            return;
        }

        Flux::toast(variant: 'success', text: 'Le abriste «'.$node->title.'» a '.$this->user->name.' ('.UnlockMessages::price($node).'). Ya le llegó el aviso.');
    }

    public function render(TreeAccess $access)
    {
        $graph = TreeGraph::forVisitor($this->course, $this->user);
        // El avance cuenta el camino principal, igual que el CV (las Sendas y los extras suman aparte).
        $trunkIds = $this->course->nodes()->where('is_published', true)->trunk()->pluck('id')->flip();

        return view('livewire.admin.students.tree', [
            'graph' => $graph,
            'total' => $trunkIds->count(),
            'completed' => collect($graph['nodes'])->filter(fn ($n) => $trunkIds->has($n['id']) && $n['state'] === TreeAccess::STATE_COMPLETED)->count(),
            'canSeeFile' => auth()->user()->can('viewStudent', $this->user),
            'next' => $access->nextNodes($this->user, $this->course)->map(fn (array $item) => [
                'id' => $item['node']->id,
                'title' => $item['node']->title,
                'price' => UnlockMessages::price($item['node']),
                'reasons' => UnlockMessages::for($this->user, $item['node'], $item['blockers']),
            ]),
        ]);
    }
}
