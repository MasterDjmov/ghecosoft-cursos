<?php

namespace App\Livewire\Admin\Courses;

use App\Enums\BranchKind;
use App\Enums\NodeType;
use App\Exceptions\TreeEditRefused;
use App\Models\Course;
use App\Models\Currency;
use App\Models\Node;
use App\Services\TreeEditor;
use App\Support\Reorder;
use App\Support\TreeGraph;
use Flux\Flux;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\Rule;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;

/** Editor del árbol: ramas, nodos (orden y rama por arrastre) y alta rápida de nodos. */
#[Title('Árbol del curso')]
class Tree extends Component
{
    public Course $course;

    /** 'list' (editar) o 'tree' (el árbol dibujado, como lo verá el alumno). */
    #[Url(as: 'vista', except: 'list')]
    public string $view = 'list';

    // Modal de rama.
    public ?int $branchId = null;

    public string $branchTitle = '';

    /** trunk | extra | path (Senda). */
    public string $branchKind = 'trunk';

    // Modal de nodo nuevo.
    public ?int $nodeBranchId = null;

    public string $nodeTitle = '';

    public string $nodeType = 'topic';

    public ?int $nodeParentId = null;

    public int $nodePrice = 10;

    /** 'course' | 'wildcard' (cualquier nodo salvo el raíz; por ejemplo, la entrada a una Senda). */
    public string $nodePaidWith = 'course';

    // Confirmación de borrado.
    public ?int $deletingNodeId = null;

    public function openBranch(?int $branchId = null): void
    {
        $branch = $branchId ? $this->course->branches()->findOrFail($branchId) : null;

        $this->branchId = $branch?->id;
        $this->branchTitle = $branch->title ?? '';
        $this->branchKind = $branch?->kind->value ?? BranchKind::Trunk->value;
        $this->resetValidation();

        Flux::modal('branch')->show();
    }

    public function saveBranch(TreeEditor $editor): void
    {
        $this->validate([
            'branchTitle' => ['required', 'string', 'max:120'],
            'branchKind' => ['required', Rule::enum(BranchKind::class)],
        ], [], ['branchTitle' => 'nombre de la rama', 'branchKind' => 'tipo de rama']);

        if ($this->branchId) {
            $this->course->branches()->findOrFail($this->branchId)
                ->update(['title' => $this->branchTitle, 'kind' => BranchKind::from($this->branchKind)]);
        } else {
            $editor->createBranch($this->course, $this->branchTitle, BranchKind::from($this->branchKind));
        }

        Flux::modal('branch')->close();
    }

    public function deleteBranch(int $branchId, TreeEditor $editor): void
    {
        $this->attempt(fn () => $editor->deleteBranch($this->course->branches()->findOrFail($branchId)), 'Rama borrada.');
    }

    public function openNode(?int $branchId = null): void
    {
        $branch = $branchId ? $this->course->branches()->findOrFail($branchId) : null;

        // Por defecto depende del último nodo de la rama (o del raíz si la rama está vacía).
        $lastInBranch = $branch?->nodes()->reorder()->orderByDesc('position')->first();

        $this->nodeBranchId = $branch?->id;
        $this->nodeTitle = '';
        // Extras: nodo extra en comodines. Senda: su primer nodo (la entrada) en comodines; los de adentro, en la moneda del curso.
        $isExtra = $branch?->kind === BranchKind::Extra;
        $isPathEntry = $branch?->isPath() && ! $lastInBranch;
        $this->nodeType = $isExtra ? NodeType::Extra->value : NodeType::Topic->value;
        $this->nodeParentId = $lastInBranch->id ?? $this->course->rootNode?->id;
        $this->nodePrice = $isExtra || $isPathEntry ? 3 : 10;
        $this->nodePaidWith = $isExtra || $isPathEntry ? 'wildcard' : 'course';
        $this->resetValidation();

        Flux::modal('node')->show();
    }

    public function saveNode(TreeEditor $editor)
    {
        $this->validate([
            'nodeTitle' => ['required', 'string', 'max:255'],
            'nodeType' => ['required', Rule::in(array_map(fn (NodeType $t) => $t->value, NodeType::editable()))],
            'nodeBranchId' => ['nullable', Rule::exists('branches', 'id')->where('course_id', $this->course->id)],
            'nodeParentId' => ['required', 'integer'],
            'nodePrice' => ['required', 'integer', 'min:0', 'max:1000'],
        ], [], ['nodeTitle' => 'título', 'nodeType' => 'tipo', 'nodeParentId' => 'requisito', 'nodePrice' => 'precio']);

        $node = $this->attempt(fn () => $editor->createNode($this->course, [
            'title' => $this->nodeTitle,
            'type' => $this->nodeType,
            'branch_id' => $this->nodeBranchId,
            'parent_id' => $this->nodeParentId,
            'price' => $this->nodePrice,
            'price_currency_id' => $this->nodePaidWith === 'wildcard' ? Currency::wildcard()->id : null,
            // Un nodo sin hojas no se publica: queda en borrador hasta tener una obligatoria.
            'is_published' => false,
        ]), 'Nodo creado como borrador: agregale una práctica obligatoria y publicalo.');

        if ($node) {
            Flux::modal('node')->close();

            return $this->redirectRoute('admin.nodes.edit', [$this->course, $node], navigate: true);
        }

        return null;
    }

    public function duplicateNode(int $nodeId, TreeEditor $editor): void
    {
        $this->attempt(fn () => $editor->duplicateNode($this->findNode($nodeId)), 'Nodo duplicado (queda sin publicar).');
    }

    public function confirmDeleteNode(int $nodeId): void
    {
        $this->deletingNodeId = $this->findNode($nodeId)->id;
        Flux::modal('delete-node')->show();
    }

    public function deleteNode(TreeEditor $editor): void
    {
        Flux::modal('delete-node')->close();
        $this->attempt(fn () => $editor->deleteNode($this->findNode($this->deletingNodeId)), 'Nodo borrado.');
        $this->deletingNodeId = null;
    }

    public function togglePublished(int $nodeId): void
    {
        $node = $this->findNode($nodeId);
        $node->update(['is_published' => ! $node->is_published]);
    }

    public function sortBranch(int $id, int $position): void
    {
        Reorder::move($this->course->branches(), $this->course->branches()->findOrFail($id), $position);
    }

    /** Arrastrar un nodo: cambia el orden y, si cae en otra rama, también la rama. */
    public function sortNode(int $id, int $position, string $branchId): void
    {
        $node = $this->findNode($id);
        $target = $branchId === 'none' ? null : $this->course->branches()->findOrFail((int) $branchId)->id;

        if ($node->isRoot()) {
            return;
        }

        DB::transaction(function () use ($node, $target, $position) {
            $node->update(['branch_id' => $target]);
            Reorder::move(Node::where('course_id', $this->course->id)->where('branch_id', $target), $node, $position);
        });
    }

    /** El docente arrastró un nodo en el árbol dibujado: se guarda su lugar. */
    public function moveNode(int $nodeId, int $x, int $y): void
    {
        $this->findNode($nodeId)->update(['pos_x' => max(-99999, min(99999, $x)), 'pos_y' => max(-99999, min(99999, $y))]);
        $this->skipRender();
    }

    /** Vuelve a la ubicación automática (radial por rama). */
    public function resetLayout(): void
    {
        $this->course->nodes()->update(['pos_x' => null, 'pos_y' => null]);
        Flux::toast(text: 'Árbol reacomodado automáticamente.');
    }

    private function findNode(?int $nodeId): Node
    {
        return $this->course->nodes()->findOrFail($nodeId);
    }

    /** Ejecuta un cambio del editor y muestra el aviso (o el motivo del rechazo). */
    private function attempt(callable $change, string $success): mixed
    {
        try {
            $result = $change();
        } catch (TreeEditRefused $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());

            return null;
        }

        Flux::toast(variant: 'success', text: $success);

        return $result ?? true;
    }

    public function render(TreeEditor $editor)
    {
        $nodes = $this->course->nodes()
            ->with(['parent:id,title', 'priceCurrency', 'badge:id,name'])
            ->withCount([
                'practices as required_count' => fn ($q) => $q->where('is_required', true),
                'practices as optional_count' => fn ($q) => $q->where('is_required', false),
            ])
            ->withSum(['practices as required_reward' => fn ($q) => $q->where('is_required', true)], 'coin_reward')
            ->orderBy('position')
            ->get();

        return view('livewire.admin.courses.tree', [
            'root' => $nodes->firstWhere('type', NodeType::Root),
            'branches' => $this->course->branches()->get(),
            'nodesByBranch' => $nodes->reject->isRoot()->groupBy(fn (Node $node) => $node->branch_id ?? 'none'),
            'nodesById' => $nodes->keyBy('id'),
            'parentOptions' => $editor->allowedParents($this->course),
            'nodeTypes' => NodeType::editable(),
            'branchKinds' => BranchKind::cases(),
            'graph' => $this->view === 'tree' ? TreeGraph::forAdmin($this->course) : null,
            'deletingNode' => $this->deletingNodeId ? $nodes->firstWhere('id', $this->deletingNodeId) : null,
        ])->title('Árbol · '.$this->course->title);
    }
}
