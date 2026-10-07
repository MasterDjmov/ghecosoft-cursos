<?php

namespace App\Services;

use App\Enums\ItemReason;
use App\Models\Craft;
use App\Models\Item;
use App\Models\User;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;
use InvalidArgumentException;

/**
 * El taller (crafteo, D93): recetas fijas de `config('game.recipes')`. Al empezar se descuentan los
 * ingredientes de la mochila (por el libro de ítems); al terminar el tiempo, el jugador recoge el resultado.
 * Una cosa a la vez y sin cron: el reloj se mira cuando el jugador entra.
 */
class Crafting
{
    public function __construct(private readonly Inventory $inventory) {}

    /**
     * Las recetas cuyo resultado e ingredientes existen en el catálogo, con sus ítems ya cargados.
     *
     * @return Collection<int, array{code: string, gives: Item, quantity: int, needs: list<array{item: Item, quantity: int}>, minutes: int, min_level: int}>
     */
    public function recipes(): Collection
    {
        $codes = collect(config('game.recipes', []))->flatMap(fn (array $r) => [...array_keys($r['gives']), ...array_keys($r['needs'])])->unique();
        $items = Item::with('course')->whereIn('code', $codes)->get()->keyBy('code');

        return collect(config('game.recipes', []))
            ->filter(fn (array $r) => collect([...array_keys($r['gives']), ...array_keys($r['needs'])])->every(fn ($code) => $items->has($code)))
            ->map(fn (array $r) => [
                'code' => $r['code'],
                'gives' => $items[array_key_first($r['gives'])],
                'quantity' => (int) reset($r['gives']),
                'needs' => collect($r['needs'])->map(fn ($quantity, $code) => ['item' => $items[$code], 'quantity' => (int) $quantity])->values()->all(),
                'minutes' => (int) $r['minutes'],
                'min_level' => (int) ($r['min_level'] ?? 1),
            ])->values();
    }

    public function recipe(string $code): ?array
    {
        return $this->recipes()->firstWhere('code', $code);
    }

    /** Lo que se está fabricando (o lo que terminó y falta recoger). */
    public function active(User $user): ?Craft
    {
        return Craft::with('item')->where('user_id', $user->id)->whereNull('collected_at')->latest('id')->first();
    }

    public function seconds(array $recipe): int
    {
        return max(1, intdiv($recipe['minutes'] * 60, max(1, (int) config('game.expedition.speed', 1))));
    }

    /**
     * Dónde cae cada material: los lugares de expedición (de todos los mundos) con una criatura que lo deja.
     *
     * @return list<string>
     */
    public function sources(Item $item): array
    {
        $creatures = collect(config('game.creatures'))->filter(fn ($c) => ($c['material'] ?? null) === $item->code)->keys();
        if ($creatures->isEmpty()) {
            return [];
        }

        return collect(config('game.protagonists'))->flatMap(fn ($world) => collect($world['expeditions']['places'] ?? [])
            ->filter(fn ($place) => $creatures->intersect($place['creatures'])->isNotEmpty())
            ->map(fn ($place) => $place['name'].' (nivel '.$place['level'].')'))->values()->all();
    }

    public function start(User $user, string $code): Craft
    {
        $recipe = $this->recipe($code) ?? throw new InvalidArgumentException('Esa receta no existe.');
        if (Inventory::playerLevel($user) < $recipe['min_level']) {
            throw new InvalidArgumentException('Esta receta pide nivel '.$recipe['min_level'].'.');
        }

        return DB::transaction(function () use ($user, $recipe) {
            User::whereKey($user->id)->lockForUpdate()->first();
            if ($this->active($user)) {
                throw new InvalidArgumentException('El taller está ocupado: recogé lo que estás fabricando antes de empezar otra cosa.');
            }
            foreach ($recipe['needs'] as $need) {
                if ($this->inventory->available($user, $need['item']) < $need['quantity']) {
                    throw new InvalidArgumentException('Te falta '.$need['item']->name.' (necesitás '.$need['quantity'].'; las que tenés puestas no cuentan).');
                }
            }
            $craft = Craft::create([
                'user_id' => $user->id, 'recipe' => $recipe['code'], 'item_id' => $recipe['gives']->id, 'quantity' => $recipe['quantity'],
                'started_at' => now(), 'ends_at' => now()->addSeconds($this->seconds($recipe)),
            ]);
            foreach ($recipe['needs'] as $need) {
                $this->inventory->take($user, $need['item'], $need['quantity'], ItemReason::CraftingCost, $craft, 'Para fabricar '.$recipe['gives']->name);
            }

            return $craft;
        });
    }

    /** Terminó: el resultado entra a la mochila, una sola vez. */
    public function collect(User $user): Craft
    {
        return DB::transaction(function () use ($user) {
            User::whereKey($user->id)->lockForUpdate()->first();
            $craft = $this->active($user);
            if (! $craft || ! $craft->isReady()) {
                throw new InvalidArgumentException('Todavía no está listo.');
            }
            $this->inventory->grant($user, $craft->item, $craft->quantity, ItemReason::Crafted, $craft);
            $craft->update(['collected_at' => now()]);

            return $craft;
        });
    }
}
