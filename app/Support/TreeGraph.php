<?php

namespace App\Support;

use App\Enums\NodeType;
use App\Enums\SubmissionStatus;
use App\Models\Course;
use App\Models\Node;
use App\Models\Practice;
use App\Models\Submission;
use App\Models\User;
use App\Services\TreeAccess;
use Illuminate\Support\Collection;

/**
 * Datos del árbol para el dibujo en canvas (resources/js/tree). El docente lo
 * ve completo; la vista del alumno (Fase 3) agrega el estado de cada nodo y hoja.
 */
class TreeGraph
{
    /** @return array<string, mixed> */
    public static function forAdmin(Course $course): array
    {
        $nodes = $course->nodes()->with(['practices', 'priceCurrency', 'parent:id,title', 'requirements:id,title'])->get();

        return [
            'course' => self::courseData($course),
            'branches' => self::branches($course),
            'nodes' => $nodes->map(fn (Node $node) => [
                'id' => $node->id,
                'title' => $node->title,
                'type' => $node->type->value,
                'branch_id' => $node->branch_id,
                'parent_id' => $node->parent_id,
                'requires' => $node->requirements->pluck('id')->all(),
                'position' => $node->position,
                'pos_x' => $node->pos_x,
                'pos_y' => $node->pos_y,
                'state' => $node->is_published ? 'admin' : 'draft',
                'price_label' => self::price($course, $node),
                'tooltip' => implode(' · ', array_filter([
                    $node->title,
                    $node->type->label(),
                    self::price($course, $node),
                    $node->parent ? 'requiere: '.$node->parent->title.$node->requirements->map(fn ($r) => ', '.$r->title)->implode('') : null,
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

    /**
     * El árbol como lo ve el alumno: estados de cada nodo y de sus hojas. De los
     * nodos que no abrió se ve el nombre y el precio, nunca el contenido ni las consignas.
     *
     * @return array<string, mixed>
     */
    public static function forStudent(Course $course, User $user): array
    {
        $access = app(TreeAccess::class);
        $unlocked = $user->nodeUnlocks()->whereHas('node', fn ($q) => $q->where('course_id', $course->id))->pluck('node_id')->flip();

        // Sin publicar y sin abrir: no existe para el alumno.
        $nodes = $course->nodes()->with(['practices', 'priceCurrency', 'parent:id,title', 'course', 'requirements'])->get()
            ->filter(fn (Node $node) => $node->is_published || $unlocked->has($node->id))
            ->values();

        $statuses = self::practiceStatuses($user, $nodes);

        return [
            'course' => self::courseData($course),
            'branches' => self::branches($course),
            'nodes' => $nodes->map(function (Node $node) use ($access, $user, $course) {
                $state = $access->state($user, $node);
                $open = in_array($state, [TreeAccess::STATE_UNLOCKED, TreeAccess::STATE_COMPLETED], true);
                // Clase 0 de prueba (D71): se entra gratis, sin abrirla.
                $trial = ! $open && $access->isTrial($user, $node);
                if ($trial) {
                    $state = TreeAccess::STATE_AVAILABLE;
                }
                $blockers = $open || $trial ? [] : UnlockMessages::for($user, $node);

                return [
                    'id' => $node->id,
                    'title' => $node->title,
                    'type' => $node->type->value,
                    'branch_id' => $node->branch_id,
                    'parent_id' => $node->parent_id,
                    'requires' => $node->requirements->pluck('id')->all(),
                    'position' => $node->position,
                    'pos_x' => $node->pos_x,
                    'pos_y' => $node->pos_y,
                    'state' => $state,
                    'price_label' => UnlockMessages::price($node),
                    'blockers' => $blockers,
                    'tooltip' => $trial ? $node->title.' · Probala gratis' : implode(' · ', array_filter([
                        $node->title,
                        term('state.'.$state, $course),
                        $open ? null : UnlockMessages::price($node),
                        $state === TreeAccess::STATE_LOCKED ? ($blockers[0] ?? null) : null,
                    ])),
                    'url' => $open || $trial ? route('student.node', [$course, $node]) : null,
                ];
            })->all(),
            'practices' => $nodes->flatMap(function (Node $node) use ($unlocked, $statuses, $course) {
                $open = $unlocked->has($node->id);

                return $node->practices->map(fn (Practice $practice) => [
                    'id' => $practice->id,
                    'node_id' => $node->id,
                    'title' => $open ? $practice->title : '?',
                    'required' => $practice->is_required,
                    'mode' => $practice->submission_mode->value,
                    'status' => $open ? ($statuses[$practice->id] ?? 'pending') : 'pending',
                    'tooltip' => $open
                        ? $practice->title.' · '.($practice->is_required ? 'Obligatoria' : 'Optativa')
                        : 'Abrí «'.$node->title.'» para ver sus '.term('practice', $course, 2),
                    'url' => $open ? route('student.node', [$course, $node]).'#practica-'.$practice->id : null,
                ]);
            })->values()->all(),
        ];
    }

    /**
     * El árbol de un alumno para quien mira su CV: los mismos colores de avance, solo para mirar.
     * Sin links, precios ni motivos de bloqueo; las hojas de nodos cerrados siguen como «?».
     */
    public static function forVisitor(Course $course, User $user): array
    {
        $graph = self::forStudent($course, $user);
        $graph['nodes'] = array_map(fn (array $node) => [
            ...$node,
            'url' => null,
            'price_label' => null,
            'blockers' => [],
            'tooltip' => $node['title'].' · '.term('state.'.$node['state'], $course),
        ], $graph['nodes']);
        $graph['practices'] = array_map(fn (array $practice) => [...$practice, 'url' => null], $graph['practices']);

        return $graph;
    }

    /**
     * Estado de cada hoja para el alumno: approved si alguna entrega se aprobó;
     * si no, el de la última entrega (submitted | redo).
     *
     * @param  Collection<int, Node>  $nodes
     * @return array<int, string>
     */
    public static function practiceStatuses(User $user, Collection $nodes): array
    {
        $ids = $nodes->flatMap->practices->pluck('id');

        return Submission::where('user_id', $user->id)->whereIn('practice_id', $ids)
            ->orderBy('attempt')
            ->get(['practice_id', 'status'])
            ->groupBy('practice_id')
            ->map(fn ($attempts) => $attempts->contains('status', SubmissionStatus::Approved)
                ? 'approved'
                : $attempts->last()->status->value)
            ->all();
    }

    /** @return list<array{id: int, title: string, position: int, is_extra: bool, kind: string}> */
    private static function branches(Course $course): array
    {
        return $course->branches()->get(['id', 'title', 'position', 'is_extra', 'kind'])
            ->map(fn ($branch) => [
                'id' => $branch->id,
                'title' => $branch->title,
                'position' => $branch->position,
                'is_extra' => $branch->is_extra,
                'kind' => $branch->kind->value,
            ])->all();
    }

    /** @return array{title: string, short: string, logo: ?string} */
    private static function courseData(Course $course): array
    {
        return [
            'title' => $course->title,
            'short' => $course->language->short(),
            'logo' => $course->logoUrl(),
        ];
    }

    private static function price(Course $course, Node $node): string
    {
        $price = $node->type === NodeType::Root ? $course->root_price : $node->price;
        $wildcard = $node->type !== NodeType::Root && $node->priceCurrency?->is_wildcard;

        return $price.' '.($wildcard ? term('coin.wildcard', null, $price) : term('coin.course', $course, $price));
    }
}
