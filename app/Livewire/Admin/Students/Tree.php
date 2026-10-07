<?php

namespace App\Livewire\Admin\Students;

use App\Exceptions\NodeLocked;
use App\Models\Course;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Models\PracticeGrant;
use App\Models\User;
use App\Notifications\PlatformNotification;
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

    /**
     * D95: abrirle las prácticas de un nodo sin que termine las micro-misiones (si no tiene el ejecutor de Java
     * o una micro-misión no le anda). Las micro-misiones siguen ahí para cuando pueda.
     */
    public function grantPractices(int $nodeId, TreeAccess $access): void
    {
        $this->authorize('unlockFor', [$this->user, $this->course]);
        $node = $this->course->nodes()->findOrFail($nodeId);
        abort_unless($access->isUnlocked($this->user, $node), 404);

        PracticeGrant::firstOrCreate(['user_id' => $this->user->id, 'node_id' => $node->id], ['granted_by' => auth()->id()]);
        $this->user->notify(new PlatformNotification(
            kind: 'practices_granted',
            title: 'Te abrieron las '.term('practice', $this->course, 2).' de «'.$node->title.'»',
            body: (auth()->user()->isAdmin() ? 'El profe' : 'Tu profe '.auth()->user()->name).' te abrió las '.term('practice', $this->course, 2)
                .' sin esperar a las micro-misiones. Cuando puedas, terminalas igual: dan XP y oro.',
            url: route('student.node', [$this->course, $node]),
            icon: 'lock-open',
        ));

        Flux::toast(variant: 'success', text: 'Le abriste las '.term('practice', $this->course, 2).' de «'.$node->title.'» a '.$this->user->name.'. Ya le llegó el aviso.');
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
            // D95: nodos abiertos con micro-misiones pendientes que todavía le tapan las prácticas.
            'lockedPractices' => $this->course->nodes()->whereHas('steps')->whereHas('practices')
                ->whereIn('id', NodeUnlock::where('user_id', $this->user->id)->select('node_id'))
                ->orderBy('position')->get()
                ->reject(fn (Node $node) => $access->practicesOpen($this->user, $node))
                ->map(fn (Node $node) => ['id' => $node->id, 'title' => $node->title, ...$access->stepProgress($this->user, $node)])
                ->values(),
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
