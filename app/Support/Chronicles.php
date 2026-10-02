<?php

namespace App\Support;

use App\Enums\BranchKind;
use App\Enums\NodeType;
use App\Enums\SubmissionStatus;
use App\Models\Course;
use App\Models\CourseCompletion;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Models\Practice;
use App\Models\Submission;
use App\Models\User;
use Illuminate\Support\Arr;
use Illuminate\Support\Collection;

/**
 * Mis Crónicas (D80): la historia de cada curso juntada en un libro que se abre a medida que el alumno
 * aprueba. Todo sale de lo que ya está escrito: la bienvenida (story.course_intro), la crónica de cada
 * nodo, el cierre de cada rama (story.branch_completed) y el epílogo (story.course_completed). Lo que
 * todavía no desbloqueó se ve, pero no se lee: el texto de una página bloqueada nunca sale del servidor.
 */
class Chronicles
{
    /** Qué abrió y qué completó el alumno, de una vez (para no consultar nodo por nodo). */
    private Collection $opened;

    private Collection $completed;

    private Collection $finishedCourses;

    public function __construct(private readonly User $user)
    {
        $this->opened = NodeUnlock::where('user_id', $user->id)->pluck('node_id')->flip();
        $required = Practice::whereIn('node_id', $this->opened->keys())->where('is_required', true)->get(['id', 'node_id'])->groupBy('node_id');
        $approved = Submission::where('user_id', $user->id)->where('status', SubmissionStatus::Approved)->pluck('practice_id')->flip();
        $this->completed = $this->opened->keys()
            ->filter(fn ($id) => $required->get($id, collect())->every(fn ($practice) => $approved->has($practice->id)))
            ->flip();
        $this->finishedCourses = CourseCompletion::where('user_id', $user->id)->pluck('course_id')->flip();
    }

    /** Los cursos que empezó (abrió su Clase 0), en el orden del catálogo. */
    public function courses(): Collection
    {
        $courseIds = Node::whereIn('id', $this->opened->keys())->where('type', NodeType::Root)->pluck('course_id');

        return Course::whereIn('id', $courseIds)->orderBy('position')->orderBy('title')->get();
    }

    /**
     * El libro de un curso: capítulos (el comienzo, cada rama y el final) con sus páginas. Con `$render`
     * en falso no se arma el texto (para contar páginas en el menú sin trabajo de más).
     *
     * @return list<array{title: string, pages: list<array<string, mixed>>}>
     */
    public function book(Course $course, bool $render = true): array
    {
        $nodes = Node::where('course_id', $course->id)->where('is_published', true)
            ->with('branch:id,title,kind,position')
            ->orderBy('position')
            ->get(['id', 'course_id', 'branch_id', 'type', 'title', 'chronicle', 'beast_key', 'position']);
        // Las historias del Diccionario (en caché): se cuentan igual que se muestran.
        $story = fn (string $key) => Story::get($key, $course, $this->user);

        $chapters = [['title' => 'El comienzo', 'pages' => array_filter([
            ($intro = $story('story.course_intro')) ? $this->page('intro', $intro['title'], $intro['html'], true, 'mentor.name') : null,
            ...$nodes->whereNull('branch_id')->map(fn (Node $node) => $this->nodePage($node, $course, $render))->all(),
        ])]];

        $branches = $nodes->whereNotNull('branch_id')->groupBy('branch_id')
            ->sortBy(fn ($group) => [$group->first()->branch->kind === BranchKind::Trunk ? 0 : 1, $group->first()->branch->position]);
        foreach ($branches as $group) {
            $branch = $group->first()->branch;
            $pages = $group->map(fn (Node $node) => $this->nodePage($node, $course, $render))->filter()->values()->all();
            if ($branch->kind === BranchKind::Trunk && ($end = $story('story.branch_completed'))) {
                $done = $group->every(fn (Node $node) => $this->completed->has($node->id));
                $pages[] = $this->page('branch_end', $end['title'], $done ? $end['html'] : null, $done, 'mentor.name', 'Terminá la rama para leer el cierre.');
            }
            if ($pages) {
                $chapters[] = ['title' => $branch->title, 'pages' => $pages];
            }
        }

        if ($epilogue = $story('story.course_completed')) {
            $done = $this->finishedCourses->has($course->id);
            $chapters[] = ['title' => 'Epílogo', 'pages' => [
                $this->page('epilogue', $epilogue['title'], $done ? $epilogue['html'] : null, $done, 'mentor.name', 'Terminá el curso para leer el epílogo.'),
            ]];
        }

        return array_values(array_filter($chapters, fn ($chapter) => $chapter['pages'] !== []));
    }

    /** Una página por cada nodo que tiene crónica. Se lee al completarlo. */
    private function nodePage(Node $node, Course $course, bool $render): ?array
    {
        if (blank($node->chronicle)) {
            return null;
        }
        $done = $this->completed->has($node->id);
        $open = $this->opened->has($node->id);
        // El título de un nodo que todavía no abrió tampoco se muestra: nunca ve lo que no abrió.
        $title = $done || $open ? $node->title : 'Una página por descubrir';
        $speaker = $node->type === NodeType::Boss ? ($node->beast_key ?: 'beast.dragon') : 'mentor.name';

        return $this->page('node', $title, $done && $render ? Narrative::render($node->chronicle, $course, $this->user) : null, $done, $speaker,
            $open ? "Completá «{$node->title}» para leer esta página." : 'Seguí avanzando por el árbol para llegar a esta página.', $node->id);
    }

    private function page(string $kind, string $title, ?string $html, bool $unlocked, string $speaker, ?string $missing = null, ?int $nodeId = null): array
    {
        return [
            'kind' => $kind,
            'title' => $title,
            'html' => $unlocked ? $html : null,
            'unlocked' => $unlocked,
            'speaker' => $speaker,
            'missing' => $unlocked ? null : $missing,
            'node_id' => $nodeId,
        ];
    }

    /** Páginas desbloqueadas en total (el prólogo cuenta): si hay más que las vistas, el menú late. */
    public function unlockedCount(): int
    {
        return 1 + $this->courses()->sum(fn (Course $course) => collect($this->book($course, render: false))
            ->sum(fn ($chapter) => collect($chapter['pages'])->where('unlocked', true)->count()));
    }

    public function newCount(): int
    {
        return max(0, $this->unlockedCount() - (int) $this->user->chronicles_seen);
    }

    /** Una frase de aliento al azar (Diccionario: story.locked_hints, una por línea). */
    public static function hint(?Course $course, User $user): string
    {
        $lines = collect(preg_split('/\R/', (string) app(Glossary::class)->resolve('story.locked_hints', $course)['lore']))
            ->map(fn ($line) => trim($line))->filter()->values();

        return $lines->isEmpty() ? '' : Narrative::fill(Arr::random($lines->all()), $course, $user);
    }
}
