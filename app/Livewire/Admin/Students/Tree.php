<?php

namespace App\Livewire\Admin\Students;

use App\Enums\SubmissionStatus;
use App\Exceptions\NodeLocked;
use App\Models\Course;
use App\Models\Node;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\NodeUnlock;
use App\Models\Practice;
use App\Models\PracticeGrant;
use App\Models\StepAttempt;
use App\Models\Submission;
use App\Models\User;
use App\Notifications\PlatformNotification;
use App\Services\NodeUnlocker;
use App\Services\ProgressRestorer;
use App\Services\TreeAccess;
use App\Support\StudentJourney;
use App\Support\TreeGraph;
use App\Support\UnlockMessages;
use DomainException;
use Flux\Flux;
use Illuminate\Support\Collection;
use Livewire\Attributes\Title;
use Livewire\Component;

/**
 * El árbol de avance de un alumno en un curso (como el del CV, D64), para el administrador y su docente.
 * Debajo, los nodos que siguen: si el alumno se traba, se los abren con sus monedas y las mismas reglas.
 * El administrador, además, le restaura el avance nodo por nodo (D103, ProgressRestorer).
 */
#[Title('Árbol del alumno')]
class Tree extends Component
{
    public User $user;

    public Course $course;

    /** El fallo que el docente abrió para ver el código, la salida esperada y la solución (D107). */
    public ?int $openFail = null;

    public function mount(User $user, Course $course): void
    {
        abort_unless($user->isStudent(), 404);
        $this->authorize('viewProgress', [$user, $course]);
    }

    public function toggleFail(int $attemptId): void
    {
        $this->openFail = $this->openFail === $attemptId ? null : $attemptId;
    }

    /**
     * Lo que hace falta para corroborar un fallo: su código (si lo mandó), lo que obtuvo, lo esperado y la solución,
     * con «Ejecutar» (Java, con el ejecutor de la compu del docente).
     *
     * @return array{attempt: StepAttempt, step: NodeStep, language: string, challenge: ?string, solution: ?string, stdin: string, expected: string, checks: ?string, done: ?string}|null
     */
    private function failDetail(): ?array
    {
        if ($this->openFail === null) {
            return null;
        }
        $attempt = StepAttempt::where('user_id', $this->user->id)->where('course_id', $this->course->id)->find($this->openFail);
        $step = $attempt?->step;
        if (! $step) {
            return null;
        }

        return [
            'attempt' => $attempt,
            'step' => $step,
            'language' => $step->runLanguage($this->course)->value,
            'challenge' => $step->challenge,
            'solution' => $step->solution,
            'stdin' => (string) $step->sample_input,
            'expected' => (string) $step->expected_output,
            'checks' => $step->checks,
            // Si después la superó, su código de ese momento.
            'done' => NodeStepCompletion::where('user_id', $this->user->id)->where('node_step_id', $step->id)->value('code'),
        ];
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

    /** D103: abrirle el nodo respetando el orden del árbol; se cobra si le alcanza, si no, sin cobrar. */
    public function restoreUnlock(int $nodeId, ProgressRestorer $restorer): void
    {
        $node = $this->restorableNode($nodeId);
        $this->restore(function () use ($restorer, $node) {
            $charged = $restorer->unlock($this->user, $node, auth()->user());

            return 'Abriste «'.$node->title.'»'.($charged ? ' ('.UnlockMessages::price($node).' de su saldo).' : ' sin cobrar.');
        });
    }

    public function restoreStep(int $stepId, ProgressRestorer $restorer): void
    {
        $this->authorize('restoreProgress', [$this->user, $this->course]);
        $step = NodeStep::whereIn('node_id', $this->course->nodes()->select('id'))->findOrFail($stepId);
        $this->restore(fn () => $restorer->completeStep($this->user, $step)
            ? 'Micro-misión «'.$step->title.'» superada.'
            : 'Ya la tenía superada.');
    }

    public function restorePractice(int $practiceId, ProgressRestorer $restorer): void
    {
        $this->authorize('restoreProgress', [$this->user, $this->course]);
        $practice = Practice::whereIn('node_id', $this->course->nodes()->select('id'))->findOrFail($practiceId);
        $this->restore(fn () => $restorer->approvePractice($this->user, $practice, auth()->user())
            ? ucfirst(term('practice', $this->course)).' «'.$practice->title.'» aprobada.'
            : 'Ya estaba aprobada.');
    }

    /** El nodo entero: abrirlo si hace falta, todas sus micro-misiones y sus prácticas obligatorias. */
    public function restoreNode(int $nodeId, ProgressRestorer $restorer): void
    {
        $node = $this->restorableNode($nodeId);
        $this->restore(function () use ($restorer, $node) {
            $restorer->completeNode($this->user, $node, auth()->user());

            return '«'.$node->title.'» aprobado entero. Ya le llegó el aviso.';
        });
    }

    private function restorableNode(int $nodeId): Node
    {
        $this->authorize('restoreProgress', [$this->user, $this->course]);

        return $this->course->nodes()->where('is_published', true)->findOrFail($nodeId);
    }

    /** @param callable(): string $action */
    private function restore(callable $action): void
    {
        try {
            Flux::toast(variant: 'success', text: $action());
        } catch (DomainException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());
        }
    }

    /**
     * Los nodos publicados en el orden del árbol (cada uno seguido de sus hijos), con lo que tiene hecho.
     *
     * @return Collection<int, array<string, mixed>>
     */
    private function restoreRows(TreeAccess $access): Collection
    {
        $nodes = $this->course->nodes()->where('is_published', true)
            ->with(['steps:id,node_id,title,position', 'practices:id,node_id,code,title,is_required,position'])
            ->orderBy('position')->orderBy('id')->get();
        $unlocked = NodeUnlock::where('user_id', $this->user->id)->whereIn('node_id', $nodes->pluck('id'))->pluck('node_id')->flip();
        $stepsDone = NodeStepCompletion::where('user_id', $this->user->id)
            ->whereIn('node_step_id', $nodes->pluck('steps')->flatten()->pluck('id'))->pluck('node_step_id')->flip();
        $approved = Submission::where('user_id', $this->user->id)->where('status', SubmissionStatus::Approved)
            ->whereIn('practice_id', $nodes->pluck('practices')->flatten()->pluck('id'))->pluck('practice_id')->flip();

        $children = $nodes->groupBy(fn (Node $node) => $node->parent_id ?? 0);
        $ordered = collect();
        $walk = function ($parentId, int $depth) use (&$walk, $children, $ordered) {
            foreach ($children->get($parentId, []) as $node) {
                $ordered->push([$node, $depth]);
                $walk($node->id, $depth + 1);
            }
        };
        $walk(0, 0);
        // Los que cuelgan de un nodo sin publicar quedan al final, para no perderlos.
        $nodes->reject(fn (Node $node) => $ordered->contains(fn ($pair) => $pair[0]->is($node)))->each(fn (Node $node) => $ordered->push([$node, 0]));

        return $ordered->map(function (array $pair) use ($unlocked, $stepsDone, $approved) {
            [$node, $depth] = $pair;
            $steps = $node->steps->map(fn ($step) => ['id' => $step->id, 'title' => $step->title, 'done' => $stepsDone->has($step->id)]);
            $practices = $node->practices->map(fn ($practice) => [
                'id' => $practice->id, 'title' => $practice->title, 'required' => $practice->is_required, 'done' => $approved->has($practice->id),
            ]);
            $isUnlocked = $unlocked->has($node->id);
            $requiredDone = $practices->where('required', true)->every(fn ($p) => $p['done']);

            return [
                'id' => $node->id,
                'code' => $node->code,
                'title' => $node->title,
                'depth' => $depth,
                'unlocked' => $isUnlocked,
                'complete' => $isUnlocked && $requiredDone && $steps->every(fn ($s) => $s['done']),
                'steps' => $steps,
                'practices' => $practices,
            ];
        });
    }

    public function render(TreeAccess $access)
    {
        $graph = TreeGraph::forVisitor($this->course, $this->user);
        // El avance cuenta el camino principal, igual que el CV (las Sendas y los extras suman aparte).
        $trunkIds = $this->course->nodes()->where('is_published', true)->trunk()->pluck('id')->flip();
        $journey = new StudentJourney($this->user, $this->course);

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
            // D107: qué miró, cuántas veces probó y dónde se traba.
            'chapters' => $journey->chapters(collect($graph['nodes'])->pluck('state', 'id')->all()),
            'recentFails' => $journey->recentFails(),
            'failDetail' => $this->failDetail(),
            'restoreRows' => auth()->user()->can('restoreProgress', [$this->user, $this->course]) ? $this->restoreRows($access) : null,
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
