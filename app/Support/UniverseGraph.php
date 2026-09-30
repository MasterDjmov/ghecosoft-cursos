<?php

namespace App\Support;

use App\Models\Course;
use App\Models\Node;
use Illuminate\Support\Collection;

/**
 * Datos del mapa del universo (D70, Admin → Universo): todos los cursos con sus nodos, el catálogo
 * de temas y qué nodo enseña o usa cada tema. Solo para el docente: se analiza, no cambia nada.
 */
class UniverseGraph
{
    /** Color de cada lenguaje en el mapa (los cursos se reconocen por color). */
    private const COLORS = [
        'python' => '#facc15', 'c' => '#60a5fa', 'cpp' => '#a78bfa', 'java' => '#f97316', 'php' => '#818cf8',
        'javascript' => '#fde047', 'typescript' => '#38bdf8', 'sql' => '#34d399', 'arduino' => '#2dd4bf', 'other' => '#94a3b8',
    ];

    /** Colores de las familias de temas, en el orden del catálogo. */
    private const FAMILY_COLORS = ['#f472b6', '#22d3ee', '#a3e635', '#fb923c', '#c084fc', '#facc15', '#34d399', '#f87171', '#60a5fa',
        '#e879f9', '#2dd4bf', '#fbbf24', '#818cf8', '#4ade80', '#fb7185', '#38bdf8', '#d946ef', '#a78bfa'];

    /** @return array<string, mixed> */
    public static function build(): array
    {
        $courses = Course::orderBy('position')->orderBy('title')->get();
        $nodes = Node::with(['branch:id,title,kind', 'practices:id,node_id,title,is_required'])
            ->whereIn('course_id', $courses->pluck('id'))
            ->orderBy('course_id')->orderBy('position')
            ->get(['id', 'course_id', 'code', 'title', 'type', 'branch_id', 'parent_id', 'topics', 'uses', 'is_published']);
        $byCourse = $nodes->groupBy('course_id');
        $slugs = $courses->pluck('slug', 'id');

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
                'url' => route('admin.courses.tree', $course),
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
                'code' => $node->code,
                'title' => $node->title,
                'type' => $node->type->value,
                'branch' => $node->branch?->title,
                'branch_kind' => $node->branch?->kind->value,
                'parent_id' => $node->parent_id,
                'topics' => $node->topics ?? [],
                'uses' => $node->uses ?? [],
                'published' => $node->is_published,
                'practices' => $node->practices->map(fn ($practice) => [
                    'title' => $practice->title,
                    'required' => $practice->is_required,
                ])->values()->all(),
                'url' => route('admin.nodes.edit', [$slugs[$node->course_id], $node->id]),
            ])->values()->all(),
        ];
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
