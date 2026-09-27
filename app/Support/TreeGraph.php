<?php

namespace App\Support;

use App\Enums\NodeType;
use App\Models\Course;
use App\Models\Node;
use App\Models\Practice;

/**
 * Datos del árbol para el dibujo en canvas (resources/js/tree). El docente lo
 * ve completo; la vista del alumno (Fase 3) agrega el estado de cada nodo y hoja.
 */
class TreeGraph
{
    /** @return array<string, mixed> */
    public static function forAdmin(Course $course): array
    {
        $nodes = $course->nodes()->with(['practices', 'priceCurrency', 'parent:id,title'])->get();

        return [
            'course' => [
                'title' => $course->title,
                'short' => $course->language->short(),
                'logo' => $course->logoUrl(),
            ],
            'branches' => $course->branches()->get(['id', 'title', 'position', 'is_extra'])->toArray(),
            'nodes' => $nodes->map(fn (Node $node) => [
                'id' => $node->id,
                'title' => $node->title,
                'type' => $node->type->value,
                'branch_id' => $node->branch_id,
                'parent_id' => $node->parent_id,
                'position' => $node->position,
                'pos_x' => $node->pos_x,
                'pos_y' => $node->pos_y,
                'state' => $node->is_published ? 'admin' : 'draft',
                'price_label' => self::price($course, $node),
                'tooltip' => implode(' · ', array_filter([
                    $node->title,
                    $node->type->label(),
                    self::price($course, $node),
                    $node->parent ? 'requiere: '.$node->parent->title : null,
                    $node->is_published ? null : 'sin publicar',
                ])),
                'url' => route('admin.nodes.edit', [$course, $node]),
            ])->values()->all(),
            'practices' => $nodes->flatMap(fn (Node $node) => $node->practices->map(fn (Practice $practice) => [
                'id' => $practice->id,
                'node_id' => $node->id,
                'title' => $practice->title,
                'required' => $practice->is_required,
                'mode' => $practice->submission_mode->value,
                'status' => 'admin',
                'tooltip' => implode(' · ', [
                    $practice->title,
                    $practice->is_required ? 'Obligatoria' : 'Optativa',
                    $practice->submission_mode->label(),
                    '+'.$practice->coin_reward.' '.($practice->is_required
                        ? term('coin.course', $course, $practice->coin_reward)
                        : term('coin.wildcard', null, $practice->coin_reward)),
                    '+'.$practice->xp_reward.' '.term('xp.short'),
                ]),
                'url' => route('admin.nodes.edit', [$course, $node]).'?hoja='.$practice->id,
            ]))->values()->all(),
        ];
    }

    private static function price(Course $course, Node $node): string
    {
        $price = $node->type === NodeType::Root ? $course->root_price : $node->price;
        $wildcard = $node->type !== NodeType::Root && $node->priceCurrency?->is_wildcard;

        return $price.' '.($wildcard ? term('coin.wildcard', null, $price) : term('coin.course', $course, $price));
    }
}
