<?php

namespace App\Livewire\Admin;

use App\Support\TopicCatalog;
use App\Support\UniverseGraph;
use Livewire\Attributes\Title;
use Livewire\Component;

/**
 * Universo de cursos (D70): todos los árboles en un mapa 3D vinculados por los temas del catálogo
 * (cursos/temas.md), con lo repetido entre cursos y lo que falta. Solo mira: no cambia nada.
 */
#[Title('Universo')]
class Universe extends Component
{
    public function render()
    {
        $graph = UniverseGraph::build();
        $courses = collect($graph['courses'])->keyBy('id');
        $nodes = collect($graph['nodes'])->keyBy('id');
        $topics = collect($graph['topics']);

        // Por tema: en qué cursos se enseña y en cuáles se usa (sin repetir cursos).
        $coursesOf = fn (array $ids) => collect($ids)->map(fn ($id) => $nodes[$id]['course_id'])->unique()->values();
        $rows = $topics->map(fn (array $topic) => [
            ...$topic,
            'taught_in' => $coursesOf($topic['taught']),
            'used_in' => $coursesOf($topic['used']),
        ]);

        $families = collect($graph['families'])->map(function (array $family) use ($rows) {
            $familyRows = $rows->where('family', $family['key'])->where('loose', false)->values();

            return [
                ...$family,
                'rows' => $familyRows,
                'taught' => $familyRows->filter(fn ($row) => $row['taught_in']->isNotEmpty())->count(),
                'repeated' => $familyRows->filter(fn ($row) => $row['taught_in']->count() > 1)->count(),
                // Lo que un nodo da por sabido y ningún curso enseña: lo más urgente.
                'needed' => $familyRows->filter(fn ($row) => $row['taught_in']->isEmpty() && $row['used_in']->isNotEmpty())->count(),
            ];
        });

        // Lo que piden los alumnos (D81), de más a menos votado.
        $topicTitles = collect(TopicCatalog::topics())->map(fn ($topic) => $topic['title']);
        $requests = collect($graph['voters'] ?? [])->map(function ($names, string $target) use ($topicTitles, $courses) {
            [$kind, $key] = explode(':', $target, 2);

            return [
                'target' => $target,
                'title' => $kind === 'course' ? ($courses[(int) $key]['title'] ?? $target) : ($topicTitles[$key] ?? $key),
                'kind' => $kind === 'course' ? 'curso' : 'tema',
                'count' => count($names),
                'voters' => collect($names),
            ];
        })->sortByDesc('count')->values();

        return view('livewire.admin.universe', [
            'graph' => $graph,
            'requests' => $requests,
            'courses' => $courses,
            'shared' => $families->where('scope', TopicCatalog::SCOPE_SHARED)->values(),
            'language' => $families->where('scope', TopicCatalog::SCOPE_LANGUAGE)->values(),
            'loose' => $rows->where('loose', true)->values(),
            'untagged' => $nodes->filter(fn ($node) => ! $node['topics'] && ! $node['uses'] && $node['type'] !== 'root')->count(),
            'liveCourses' => $courses->where('nodes', '>', 0)->values(),
        ]);
    }
}
