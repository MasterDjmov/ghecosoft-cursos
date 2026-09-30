<?php

namespace App\Livewire\Admin;

use App\Enums\BranchKind;
use App\Models\Course;
use App\Models\Node;
use Livewire\Attributes\Title;
use Livewire\Component;

/**
 * Temario del curso para dar la clase (D72, solo administrador y docentes): el árbol entero como
 * índice, en el orden del curso, con lo que enseña cada nodo, los enunciados de sus prácticas y
 * las resoluciones (de referencia y las notas del docente). Se imprime con todo desplegado.
 */
#[Title('Temario')]
class Syllabus extends Component
{
    public Course $course;

    public function render()
    {
        $nodes = $this->course->nodes()->with(['branch', 'practices' => fn ($q) => $q->orderBy('position')])->get();
        $branches = $this->course->branches()->get()
            // Primero el camino principal, después las Sendas y al final los extras.
            ->sortBy(fn ($branch) => [$branch->is_extra ? 2 : ($branch->kind === BranchKind::Path ? 1 : 0), $branch->position])
            ->values();

        $sections = collect([['branch' => null, 'nodes' => $nodes->whereNull('branch_id')->sortBy(fn (Node $n) => [$n->isRoot() ? 0 : 1, $n->position])->values()]])
            ->concat($branches->map(fn ($branch) => ['branch' => $branch, 'nodes' => $nodes->where('branch_id', $branch->id)->sortBy('position')->values()]))
            ->filter(fn ($section) => $section['nodes']->isNotEmpty())
            ->values();

        return view('livewire.admin.syllabus', [
            'sections' => $sections,
            'practiceCount' => $nodes->sum(fn (Node $node) => $node->practices->count()),
        ])->title('Temario · '.$this->course->title);
    }
}
