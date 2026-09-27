<?php

namespace App\Livewire\Student;

use App\Models\Course;
use App\Models\Node;
use App\Services\TreeAccess;
use App\Support\Glossary;
use App\Support\Markdown;
use App\Support\TreeGraph;
use App\Support\UnlockMessages;
use Livewire\Attributes\On;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Un nodo abierto: explicación, ejemplo ejecutable, recursos y hojas. */
#[Title('Nodo')]
class NodeView extends Component
{
    public Course $course;

    public Node $node;

    public function mount(Course $course, Node $node): void
    {
        abort_unless($node->course_id === $course->id, 404);
        $this->authorize('view', $node);
    }

    /** Se entregó o se completó una hoja: cambia el resumen de progreso (y quizás el estado del nodo). */
    #[On('practice-approved')]
    #[On('practice-updated')]
    public function refreshProgress(): void {}

    /** ID de YouTube si el video es de ahí (se muestra embebido); si no, se muestra el link. */
    public static function youtubeId(?string $url): ?string
    {
        if (! $url) {
            return null;
        }

        return preg_match('~(?:youtube\.com/(?:watch\?(?:.*&)?v=|embed/|shorts/)|youtu\.be/)([A-Za-z0-9_-]{11})~', $url, $m) ? $m[1] : null;
    }

    public function render(TreeAccess $access)
    {
        $user = auth()->user();
        $practices = $this->node->practices()->get();
        $statuses = TreeGraph::practiceStatuses($user, collect([$this->node->setRelation('practices', $practices)]));

        // Se abre la primera hoja pendiente (sin hacer o para rehacer), las obligatorias primero.
        $firstPending = $practices->sortByDesc('is_required')
            ->first(fn ($practice) => in_array($statuses[$practice->id] ?? null, [null, 'redo'], true));

        // Siguientes: los nodos que dependen de este, con su estado para el alumno.
        $next = $this->node->children()->where('is_published', true)->orderBy('position')->get()
            ->map(fn (Node $child) => [
                'node' => $child,
                'state' => $access->state($user, $child),
                'price' => UnlockMessages::price($child),
            ]);

        // Secciones del nodo (D37). Las soluciones del docente no se leen acá: nunca llegan al alumno.
        $node = $this->node;
        $sections = [
            'chronicle' => Markdown::render($node->chronicle),
            'objectives' => Markdown::render($node->objectives),
            'before' => Markdown::render($node->before_you_start),
            'uses' => Markdown::render($node->use_cases),
            'errors' => Markdown::render($node->common_errors),
        ];
        $selfCheck = collect($node->selfCheckItems())
            ->map(fn ($item) => ['question' => $item['question'], 'answer' => Markdown::render($item['answer'] ?? '')]);
        $beast = $node->beast_key ? ['key' => $node->beast_key, ...app(Glossary::class)->resolve($node->beast_key, $this->course)] : null;

        return view('livewire.student.node-view', [
            'contentHtml' => Markdown::render($node->content),
            'sections' => $sections,
            'selfCheck' => $selfCheck,
            'beast' => $beast,
            'practices' => $practices,
            'numbers' => $practices->pluck('id')->flip()->map(fn ($index) => $index + 1),
            'statuses' => $statuses,
            'firstPending' => $firstPending?->id,
            'resources' => $this->node->resources()->get(),
            'youtubeId' => self::youtubeId($this->node->video_url),
            'parent' => $this->node->parent && $access->canView($user, $this->node->parent) ? $this->node->parent : null,
            'next' => $next,
            'subscription' => $access->activeSubscription($user, $this->course),
            'completed' => $access->isCompleted($user, $this->node),
            'runnable' => $this->node->example_code && $this->course->language->value === 'python',
        ])->title($this->node->title.' · '.$this->course->title);
    }
}
