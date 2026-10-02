<?php

namespace App\Support;

use App\Models\Course;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Models\UniverseVote;
use App\Models\User;
use Illuminate\Support\Collection;

/**
 * Datos del mapa del universo (D70, Admin → Universo): todos los cursos con sus nodos, el catálogo
 * de temas y qué nodo enseña o usa cada tema, y los votos «Quiero aprender esto» (D81).
 *
 * Con un alumno (el Universo de su menú, D81) se arma su versión: solo los cursos publicados o que
 * vienen, sus nodos abiertos con título y el resto sin nombre (nunca ve lo que no abrió), sin enlaces
 * del panel ni nombres de quién votó.
 */
class UniverseGraph
{
    /** Color de cada lenguaje en el mapa (los cursos se reconocen por color). */
    private const COLORS = [
        'python' => '#facc15', 'c' => '#60a5fa', 'cpp' => '#a78bfa', 'java' => '#f97316', 'php' => '#818cf8',
        'javascript' => '#fde047', 'typescript' => '#38bdf8', 'sql' => '#34d399', 'arduino' => '#2dd4bf', 'html' => '#e879f9', 'other' => '#94a3b8',
    ];

    /** Colores de las familias de temas, en el orden del catálogo. */
    private const FAMILY_COLORS = ['#f472b6', '#22d3ee', '#a3e635', '#fb923c', '#c084fc', '#facc15', '#34d399', '#f87171', '#60a5fa',
        '#e879f9', '#2dd4bf', '#fbbf24', '#818cf8', '#4ade80', '#fb7185', '#38bdf8', '#d946ef', '#a78bfa'];

    /** @return array<string, mixed> */
    public static function build(?User $student = null): array
    {
        $courses = Course::orderBy('position')->orderBy('title')->get()
            ->when($student, fn ($all) => $all->filter(fn (Course $course) => $course->is_published || $course->isUpcoming())->values());
        $nodes = Node::with(['branch:id,title,kind', 'practices:id,node_id,title,is_required'])
            ->whereIn('course_id', $courses->pluck('id'))
            ->when($student, fn ($q) => $q->where('is_published', true))
            ->orderBy('course_id')->orderBy('position')
            ->get(['id', 'course_id', 'code', 'title', 'type', 'branch_id', 'parent_id', 'topics', 'uses', 'is_published']);
        $byCourse = $nodes->groupBy('course_id');
        $slugs = $courses->pluck('slug', 'id');
        $opened = $student ? NodeUnlock::where('user_id', $student->id)->pluck('node_id')->flip() : collect();
        $hidden = fn (Node $node) => $student && ! $opened->has($node->id);

        return [
            'courses' => $courses->map(fn (Course $course) => [
                'id' => $course->id,
                'slug' => $course->slug,
                'title' => $course->title,
                'language' => $course->language->label(),
                'short' => $course->language->short(),
                'logo' => $course->logoUrl(),
                'color' => self::COLORS[$course->language->value] ?? self::COLORS['other'],
                'upcoming' => $course->isUpcoming(),
                'published' => $course->is_published,
                'nodes' => $byCourse->get($course->id, collect())->count(),
                'url' => $student ? route('student.course', $course) : route('admin.courses.tree', $course),
            ])->values()->all(),
            'families' => array_map(fn (array $family, int $i) => [
                'key' => $family['key'],
                'title' => $family['title'],
                'scope' => $family['scope'],
                'color' => self::FAMILY_COLORS[$i % count(self::FAMILY_COLORS)],
                'topics' => $family['topics'],
            ], array_values(TopicCatalog::families()), array_keys(array_values(TopicCatalog::families()))),
            'topics' => self::topics($nodes),
            'nodes' => $nodes->map(fn (Node $node) => [
                'id' => $node->id,
                'course_id' => $node->course_id,
                // Lo que el alumno no abrió es un punto de luz sin nombre: se ve que hay, no qué es.
                'code' => $hidden($node) ? null : $node->code,
                'title' => $hidden($node) ? null : $node->title,
                'type' => $node->type->value,
                'branch' => $hidden($node) ? null : $node->branch?->title,
                'branch_kind' => $node->branch?->kind->value,
                'parent_id' => $node->parent_id,
                'topics' => $node->topics ?? [],
                'uses' => $node->uses ?? [],
                'published' => $node->is_published,
                'practices' => $student ? [] : $node->practices->map(fn ($practice) => [
                    'title' => $practice->title,
                    'required' => $practice->is_required,
                ])->values()->all(),
                'url' => match (true) {
                    ! $student => route('admin.nodes.edit', [$slugs[$node->course_id], $node->id]),
                    $hidden($node) => null,
                    default => route('student.node', [$slugs[$node->course_id], $node->id]),
                },
            ])->values()->all(),
            ...self::votes($student),
        ];
    }

    /**
     * «Quiero aprender esto» (D81): cuántos votos tiene cada tema o curso; el docente ve también quién
     * votó, y el alumno, lo que votó él.
     *
     * @return array{votes: array<string, int>, voters?: array<string, list<string>>, myVotes?: list<string>}
     */
    private static function votes(?User $student): array
    {
        $votes = UniverseVote::with('user:id,name,last_name,username')->get();
        $result = ['votes' => $votes->countBy('target')->all()];

        return $student
            ? [...$result, 'myVotes' => $votes->where('user_id', $student->id)->pluck('target')->values()->all()]
            : [...$result, 'voters' => $votes->groupBy('target')->map(fn ($group) => $group->map(fn ($vote) => $vote->user->fullName())->values()->all())->all()];
    }

    /** ¿Se puede votar? Un tema que ningún curso publicado o próximo enseña, o un curso que viene (próximamente). */
    public static function canVoteFor(string $target): bool
    {
        [$kind, $key] = array_pad(explode(':', $target, 2), 2, '');

        return match ($kind) {
            // Si ya lo enseña un curso publicado o uno que viene, no hace falta pedirlo.
            'topic' => array_key_exists($key, TopicCatalog::topics())
                && ! Node::where('is_published', true)
                    ->whereHas('course', fn ($q) => $q->where('is_published', true)->orWhere('is_upcoming', true))
                    ->whereJsonContains('topics', $key)->exists(),
            'course' => ctype_digit($key) && (Course::find((int) $key)?->isUpcoming() ?? false),
            default => false,
        };
    }

    /**
     * Los temas del catálogo con quién los enseña y quién los usa; al final, los que algún nodo
     * nombra pero no están en el catálogo (sueltos).
     *
     * @param  Collection<int, Node>  $nodes
     * @return list<array<string, mixed>>
     */
    private static function topics(Collection $nodes): array
    {
        $taught = [];
        $used = [];
        foreach ($nodes as $node) {
            foreach ($node->topics ?? [] as $topic) {
                $taught[$topic][] = $node->id;
            }
            foreach ($node->uses ?? [] as $topic) {
                $used[$topic][] = $node->id;
            }
        }

        $catalog = TopicCatalog::topics();
        $topics = array_values(array_map(fn (array $topic) => [
            ...$topic,
            'taught' => $taught[$topic['key']] ?? [],
            'used' => $used[$topic['key']] ?? [],
            'loose' => false,
        ], $catalog));

        $loose = array_diff(array_unique([...array_keys($taught), ...array_keys($used)]), array_keys($catalog));
        foreach ($loose as $key) {
            $topics[] = [
                'key' => $key, 'family' => explode('.', $key)[0], 'title' => $key, 'description' => 'No está en cursos/temas.md.',
                'order' => PHP_INT_MAX, 'taught' => $taught[$key] ?? [], 'used' => $used[$key] ?? [], 'loose' => true,
            ];
        }

        return $topics;
    }
}
