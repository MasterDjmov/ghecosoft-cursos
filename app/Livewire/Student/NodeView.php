<?php

namespace App\Livewire\Student;

use App\Livewire\Student\Concerns\UnlocksNodes;
use App\Models\Course;
use App\Models\Node;
use App\Models\NodeStepCompletion;
use App\Services\NodeUnlocker;
use App\Services\StepCompleter;
use App\Services\TreeAccess;
use App\Support\Glossary;
use App\Support\Narrative;
use App\Support\TreeGraph;
use App\Support\UnlockMessages;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Support\Str;
use InvalidArgumentException;
use Livewire\Attributes\On;
use Livewire\Attributes\Renderless;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Un nodo abierto: micro-misiones (D84), explicación, ejemplo ejecutable, recursos y hojas. */
#[Title('Nodo')]
class NodeView extends Component
{
    use UnlocksNodes;

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

    /**
     * Micro-misión superada (D84): el navegador ya comparó la salida; acá se vuelve a comparar y se da la XP
     * una sola vez (StepCompleter, solo premios de juego). No se vuelve a dibujar la página: el alumno ve lo que
     * ganó y pasa a la siguiente cuando toca «Siguiente».
     *
     * @return array{ok: bool, xp?: int, error?: string}
     */
    #[Renderless]
    public function completeStep(int $stepId, string $output, StepCompleter $completer): array
    {
        $step = $this->node->steps()->findOrFail($stepId);
        $key = 'steps:'.auth()->id();
        if (RateLimiter::tooManyAttempts($key, 30)) {
            return ['ok' => false, 'error' => 'Esperá un momento antes de volver a probar.'];
        }
        RateLimiter::hit($key, 60);

        try {
            $new = $completer->complete(auth()->user(), $step, Str::limit($output, 20000, ''));
        } catch (InvalidArgumentException $e) {
            return ['ok' => false, 'error' => $e->getMessage()];
        }

        return ['ok' => true, 'xp' => $new && ! auth()->user()->isStaff() ? $step->xp_reward : 0];
    }

    /** «Siguiente»: abrir desde acá un nodo que depende de este, sin tener que buscarlo en el árbol. */
    public function unlockNext(int $nodeId, NodeUnlocker $unlocker)
    {
        $next = $this->node->children()->where('is_published', true)->findOrFail($nodeId);

        return $this->openNode($next, $unlocker);
    }

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
        // {heroe}, {mentor}, {mundo} y {region} se reemplazan antes del markdown.
        $render = fn (?string $text) => Narrative::render($text, $this->course, $user);
        $sections = [
            'chronicle' => $render($node->chronicle),
            'objectives' => $render($node->objectives),
            'before' => $render($node->before_you_start),
            'uses' => $render($node->use_cases),
            'errors' => $render($node->common_errors),
        ];
        $selfCheck = collect($node->selfCheckItems())
            ->map(fn ($item) => ['question' => Narrative::fill($item['question'], $this->course, $user), 'answer' => $render($item['answer'] ?? '')]);
        $beast = $node->beast_key ? ['key' => $node->beast_key, ...app(Glossary::class)->resolve($node->beast_key, $this->course)] : null;
        if ($beast) {
            $beast['lore_html'] = $render($beast['lore']);
        }

        // Micro-misiones (D84): las superadas, la actual y las que faltan.
        $steps = $this->node->steps()->get();
        $doneSteps = $steps->isEmpty() ? collect() : NodeStepCompletion::where('user_id', $user->id)
            ->whereIn('node_step_id', $steps->pluck('id'))->pluck('node_step_id')->flip();
        $currentStep = $steps->first(fn ($step) => ! $doneSteps->has($step->id));
        $stepTexts = $steps->mapWithKeys(fn ($step) => [$step->id => [
            'scene' => $render($step->scene),
            'hint' => $render($step->hint),
            'challenge' => $render($step->challenge),
            'success' => $render($step->success_text),
            'unlocks' => $render($step->unlocks),
        ]]);

        return view('livewire.student.node-view', [
            'steps' => $steps,
            'doneSteps' => $doneSteps,
            'currentStep' => $currentStep,
            'stepTexts' => $stepTexts,
            'contentHtml' => $render($node->content),
            // La Clase 0 abre con el mundo del curso (Diccionario: world.region del curso, o world.name).
            'scene' => $this->node->isRoot() ? app(Glossary::class)->scene($this->course) : null,
            'sections' => $sections,
            'bossXp' => (int) config('game.boss_defeated_xp'),
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
            'trial' => $access->isTrial($user, $this->node),
            'completed' => $access->isCompleted($user, $this->node),
            'runnable' => $this->node->example_code && $this->node->example_runnable && $this->course->language->studentCanRun(),
        ])->title($this->node->title.' · '.$this->course->title);
    }
}
