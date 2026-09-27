<?php

namespace App\Livewire\Student;

use App\Models\Course;
use App\Models\Node;
use App\Services\TreeAccess;
use App\Support\Markdown;
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

    /** Una hoja "sin entrega" se marcó completada: puede haber cambiado el estado del nodo. */
    #[On('practice-approved')]
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

        // Siguientes: los nodos que dependen de este, con su estado para el alumno.
        $next = $this->node->children()->where('is_published', true)->orderBy('position')->get()
            ->map(fn (Node $child) => [
                'node' => $child,
                'state' => $access->state($user, $child),
                'price' => UnlockMessages::price($child),
            ]);

        return view('livewire.student.node-view', [
            'contentHtml' => Markdown::render($this->node->content),
            'practices' => $practices,
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
