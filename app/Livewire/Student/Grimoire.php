<?php

namespace App\Livewire\Student;

use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;

/**
 * El grimorio (D84 § 4, D89): la carta de cada micro-misión superada, con su sintaxis para copiar.
 * Una solapa por curso y, adentro, todo plegado: rama → nodo → carta (con un buscador), para que no sea una
 * pared de cartas. Es la «memoria externa» del jugador.
 */
#[Title('Grimorio')]
class Grimoire extends Component
{
    #[Url(as: 'curso')]
    public string $tab = '';

    /**
     * Las piezas de la carta: el cuerpo separa los usos con « · » (`print("texto") · print(a, b, sep=" | ")`).
     *
     * @return list<string>
     */
    public static function snippets(?string $body): array
    {
        return array_values(array_filter(array_map('trim', explode(' · ', (string) $body)), fn ($piece) => $piece !== ''));
    }

    public function render()
    {
        $user = auth()->user();
        $done = NodeStepCompletion::where('user_id', $user->id)->pluck('completed_at', 'node_step_id');
        $steps = NodeStep::with('node.course', 'node.branch')
            ->whereIn('id', $done->keys())
            ->whereNotNull('card_title')
            ->get()
            ->sortBy(fn (NodeStep $step) => sprintf('%s|%05d', $step->node->code, $step->position));

        $books = $steps->groupBy(fn (NodeStep $step) => $step->node->course_id)
            ->map(fn ($courseSteps) => [
                'course' => $courseSteps->first()->node->course,
                'branches' => $courseSteps->groupBy(fn (NodeStep $step) => $step->node->branch_id ?? 0)
                    ->map(fn ($branchSteps) => [
                        'branch' => $branchSteps->first()->node->branch,
                        'count' => $branchSteps->count(),
                        'nodes' => $branchSteps->groupBy('node_id')->map(fn ($nodeSteps) => ['node' => $nodeSteps->first()->node, 'steps' => $nodeSteps->values()])->values(),
                    ])->values(),
                'count' => $courseSteps->count(),
            ])
            ->sortBy(fn ($book) => $book['course']->title)
            ->values();

        $current = $books->first(fn ($book) => $book['course']->slug === $this->tab) ?? $books->first();

        return view('livewire.student.grimoire', [
            'books' => $books,
            'current' => $current,
            // Cuántas cartas tiene cada curso en total (las que faltan se ven en silueta, como en Mis Crónicas).
            'totals' => NodeStep::whereNotNull('node_steps.card_title')
                ->join('nodes', 'nodes.id', '=', 'node_steps.node_id')
                ->whereIn('nodes.course_id', $books->pluck('course.id'))->where('nodes.is_published', true)
                ->groupBy('nodes.course_id')->selectRaw('nodes.course_id, count(*) as total')->pluck('total', 'course_id'),
        ]);
    }
}
