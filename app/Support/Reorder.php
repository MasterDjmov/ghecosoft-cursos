<?php

namespace App\Support;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\Relation;
use Illuminate\Support\Facades\DB;

/** Reordena hermanos (ramas, nodos, hojas, recursos) cuando se arrastra uno. */
class Reorder
{
    /**
     * Pone $item en $position (base 0) dentro de $siblings y renumera 1..n.
     *
     * @param  Builder<Model>|Relation<Model, Model, mixed>  $siblings
     */
    public static function move(Builder|Relation $siblings, Model $item, int $position): void
    {
        DB::transaction(function () use ($siblings, $item, $position) {
            $ids = $siblings->reorder()->orderBy('position')->orderBy('id')->pluck('id')
                ->reject(fn ($id) => $id === $item->getKey())
                ->values()
                ->all();

            array_splice($ids, max(0, min($position, count($ids))), 0, [$item->getKey()]);

            foreach ($ids as $index => $id) {
                $item->newQuery()->whereKey($id)->update(['position' => $index + 1]);
            }
        });
    }

    /** @param  Builder<Model>|Relation<Model, Model, mixed>  $siblings */
    public static function next(Builder|Relation $siblings): int
    {
        return (int) $siblings->max('position') + 1;
    }
}
