<?php

namespace App\Livewire\Student;

use App\Livewire\Student\Concerns\WorksOnPractice;
use App\Models\Course;
use App\Models\Node;
use App\Models\Practice;
use App\Services\PracticeSubmitter;
use App\Support\Narrative;
use App\Support\TreeGraph;
use Livewire\Attributes\Layout;
use Livewire\Attributes\On;
use Livewire\Component;
use Livewire\Features\SupportFileUploads\TemporaryUploadedFile;
use Livewire\WithFileUploads;

/**
 * Modo misión: una práctica a pantalla completa (historia, consigna y teoría a la
 * izquierda, editor y consola al centro, devolución a la derecha). Es otra
 * presentación de la misma práctica: entrega y reglas son las de PracticeCard.
 */
#[Layout('layouts::mission')]
class Mission extends Component
{
    use WithFileUploads, WorksOnPractice;

    public Course $course;

    public Node $node;

    public Practice $practice;

    /** @var TemporaryUploadedFile|null */
    public $file = null;

    public string $comment = '';

    public function mount(Course $course, Node $node, Practice $practice): void
    {
        abort_unless($node->course_id === $course->id && $practice->node_id === $node->id, 404);
        $this->authorize('view', $node);
    }

    #[On('practice-updated')]
    #[On('practice-approved')]
    public function refreshState(): void {}

    public function render(PracticeSubmitter $submitter)
    {
        $user = auth()->user();
        $state = $this->practiceState($submitter);
        $practices = $this->node->practices()->get();
        $statuses = TreeGraph::practiceStatuses($user, collect([$this->node->setRelation('practices', $practices)]));
        $render = fn (?string $text) => Narrative::render($text, $this->course, $user);

        return view('livewire.student.mission', [
            ...$state,
            'practices' => $practices,
            'statuses' => $statuses,
            'number' => $practices->search(fn (Practice $p) => $p->id === $this->practice->id) + 1,
            'chronicle' => $render($this->node->chronicle),
            'theory' => array_filter([
                'content' => $render($this->node->content),
                'uses' => $render($this->node->use_cases),
                'errors' => $render($this->node->common_errors),
            ]),
            // La columna de la devolución aparece solo cuando hay algo que leer.
            'showSide' => $state['attempts']->contains(fn ($attempt) => $attempt->comments->isNotEmpty()),
        ])->title($this->practice->title.' · Misión');
    }
}
