<?php

namespace App\Services;

use App\Enums\CoinReason;
use App\Enums\ItemKind;
use App\Enums\ItemReason;
use App\Exceptions\InsufficientFunds;
use App\Models\Course;
use App\Models\Currency;
use App\Models\Hero;
use App\Models\Item;
use App\Models\ItemMovement;
use App\Models\Level;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\User;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;
use InvalidArgumentException;

/**
 * La mochila del jugador (D90): cada ítem que entra o sale queda en `item_movements` (la cantidad es la suma,
 * como las monedas en el Ledger). Lo equipado sigue siendo suyo, pero no está disponible para otro uso.
 * El oro de las compras pasa por el Ledger.
 */
class Inventory
{
    public function __construct(private readonly Ledger $ledger) {}

    public static function playerLevel(User $user): int
    {
        return Level::forXp((int) $user->xp_total)?->number ?? 1;
    }

    /** @return Collection<int, int> cantidad por item_id (solo las mayores que cero) */
    public function owned(User $user): Collection
    {
        return ItemMovement::where('user_id', $user->id)->groupBy('item_id')
            ->selectRaw('item_id, SUM(quantity) as total')->pluck('total', 'item_id')
            ->map(fn ($total) => (int) $total)->filter(fn ($total) => $total > 0);
    }

    /** @return Collection<int, int> cuántas unidades de cada ítem tiene puestas entre todos sus héroes */
    public function equipped(User $user): Collection
    {
        return Hero::where('user_id', $user->id)->get(ItemKind::slots())
            ->flatMap(fn (Hero $hero) => collect(ItemKind::slots())->map(fn ($slot) => $hero->{$slot})->filter())
            ->countBy()->map(fn ($count) => (int) $count);
    }

    /** Las que puede usar, vender o equipar (las que no tiene puestas). */
    public function available(User $user, Item $item): int
    {
        return ($this->owned($user)[$item->id] ?? 0) - ($this->equipped($user)[$item->id] ?? 0);
    }

    public function grant(User $user, Item $item, int $quantity, ItemReason $reason, ?Model $source = null, ?string $note = null, ?User $by = null): ItemMovement
    {
        if ($quantity <= 0) {
            throw new InvalidArgumentException('La cantidad tiene que ser mayor que 0.');
        }

        return ItemMovement::create([
            'user_id' => $user->id, 'item_id' => $item->id, 'quantity' => $quantity, 'reason' => $reason,
            'source_type' => $source?->getMorphClass(), 'source_id' => $source?->getKey(), 'note' => $note, 'created_by' => $by?->id,
        ]);
    }

    /** Saca unidades disponibles (no las equipadas). */
    public function take(User $user, Item $item, int $quantity, ItemReason $reason, ?Model $source = null, ?string $note = null): ItemMovement
    {
        if ($quantity <= 0) {
            throw new InvalidArgumentException('La cantidad tiene que ser mayor que 0.');
        }

        return DB::transaction(function () use ($user, $item, $quantity, $reason, $source, $note) {
            User::whereKey($user->id)->lockForUpdate()->first();
            if ($this->available($user, $item) < $quantity) {
                throw new InvalidArgumentException('No tenés suficientes «'.$item->name.'».');
            }

            return ItemMovement::create([
                'user_id' => $user->id, 'item_id' => $item->id, 'quantity' => -$quantity, 'reason' => $reason,
                'source_type' => $source?->getMorphClass(), 'source_id' => $source?->getKey(), 'note' => $note,
            ]);
        });
    }

    /**
     * Comprar en la tienda del mundo con oro.
     *
     * @throws InsufficientFunds si no le alcanza el oro.
     */
    public function buy(User $user, Item $item, int $quantity = 1): void
    {
        if (! $item->in_shop || $item->price === null) {
            throw new InvalidArgumentException('Ese ítem no se vende.');
        }
        if ($quantity < 1 || $quantity > 20) {
            throw new InvalidArgumentException('Comprá entre 1 y 20 por vez.');
        }
        if (self::playerLevel($user) < $item->min_level) {
            throw new InvalidArgumentException('Necesitás nivel '.$item->min_level.' para comprarlo.');
        }

        DB::transaction(function () use ($user, $item, $quantity) {
            $this->ledger->debit($user, Currency::gold(), $item->price * $quantity, CoinReason::ShopPurchase, $item, $item->course,
                $item->name.($quantity > 1 ? ' ×'.$quantity : ''));
            $this->grant($user, $item, $quantity, ItemReason::ShopPurchase, $item);
        });
    }

    /** Ponerle un ítem al héroe (reemplaza lo que tenía en ese lugar, que vuelve a la mochila). */
    public function equip(Hero $hero, Item $item): void
    {
        $slot = $item->kind->slot();
        if ($slot === null) {
            throw new InvalidArgumentException('Ese ítem no se equipa.');
        }
        if (! $item->fitsCourse($hero->course)) {
            throw new InvalidArgumentException('Ese ítem es de otro mundo.');
        }

        DB::transaction(function () use ($hero, $item, $slot) {
            User::whereKey($hero->user_id)->lockForUpdate()->first();
            $free = $this->available($hero->user, $item) + ((int) $hero->{$slot} === $item->id ? 1 : 0);
            if ($free < 1) {
                throw new InvalidArgumentException('No te queda ningún «'.$item->name.'» libre.');
            }
            $hero->update([$slot => $item->id]);
        });
    }

    public function unequip(Hero $hero, string $slot): void
    {
        if (! in_array($slot, ItemKind::slots(), true)) {
            throw new InvalidArgumentException('Ese lugar no existe.');
        }
        $hero->update([$slot => null]);
    }

    /** Usar un ítem fuera de las expediciones: hoy, el Pergamino del Reinicio sobre un héroe. */
    public function use(User $user, Item $item, Hero $hero): void
    {
        if ($item->code !== Item::RESPEC) {
            throw new InvalidArgumentException('Ese ítem se usa solo en las expediciones.');
        }
        if ($hero->user_id !== $user->id) {
            throw new InvalidArgumentException('Ese héroe no es tuyo.');
        }

        DB::transaction(function () use ($user, $item, $hero) {
            $this->take($user, $item, 1, ItemReason::Used, $hero, 'Reinicio de '.$hero->course->title);
            $hero->update(['respec_available' => true]);
        });
    }

    /**
     * El ítem de historia de una micro-misión («item: Llave del Puente» o «Poción de Curación x3»): se busca
     * en el catálogo por nombre (del mundo o común); si no está, se crea como ítem de la historia.
     *
     * @return array{0: Item, 1: int}|null
     */
    public function stepItem(NodeStep $step): ?array
    {
        $raw = trim((string) $step->item);
        if ($raw === '') {
            return null;
        }
        $quantity = 1;
        if (preg_match('/^(.*?)\s+x(\d+)$/iu', $raw, $m)) {
            [$raw, $quantity] = [trim($m[1]), max(1, (int) $m[2])];
        }
        $course = $step->node->course;
        $item = Item::where('name', $raw)->where(fn ($q) => $q->where('course_id', $course->id)->orWhereNull('course_id'))->first()
            ?? Item::firstOrCreate(
                ['code' => Str::limit($course->slug.'-'.Str::slug($raw), 80, '')],
                ['name' => $raw, 'kind' => ItemKind::Story, 'course_id' => $course->id, 'description' => 'Lo conseguiste en «'.$step->title.'».'],
            );

        return [$item, $quantity];
    }

    /** El ítem de una micro-misión superada, una sola vez (el staff prueba sin ganar). */
    public function creditStep(User $user, NodeStep $step): void
    {
        if (! config('game.inventory_enabled') || $user->isStaff() || ! ($pair = $this->stepItem($step))) {
            return;
        }
        [$item, $quantity] = $pair;
        DB::transaction(function () use ($user, $step, $item, $quantity) {
            User::whereKey($user->id)->lockForUpdate()->first();
            $given = ItemMovement::where('user_id', $user->id)->where('reason', ItemReason::StepReward)
                ->where('source_type', $step->getMorphClass())->where('source_id', $step->id)->exists();
            if (! $given) {
                $this->grant($user, $item, $quantity, ItemReason::StepReward, $step);
            }
        });
    }

    /** Los ítems de las micro-misiones ya superadas que todavía no recibió (las de antes de la mochila). */
    public function settleItems(User $user): void
    {
        if (! config('game.inventory_enabled') || $user->isStaff()) {
            return;
        }
        $given = ItemMovement::where('user_id', $user->id)->where('reason', ItemReason::StepReward)
            ->where('source_type', (new NodeStep)->getMorphClass())->pluck('source_id');
        NodeStep::with('node.course')
            ->whereIn('id', NodeStepCompletion::where('user_id', $user->id)->select('node_step_id'))
            ->whereNotIn('id', $given)->whereNotNull('item')->where('item', '!=', '')
            ->get()
            ->each(fn (NodeStep $step) => $this->creditStep($user, $step));
    }

    /**
     * Lo que se ve en la mochila: cada ítem con cuántos tiene y cuántos tiene puestos.
     *
     * @return Collection<int, array{item: Item, owned: int, equipped: int}>
     */
    public function contents(User $user): Collection
    {
        $owned = $this->owned($user);
        $equipped = $this->equipped($user);

        return Item::with('course')->whereIn('id', $owned->keys())->get()
            ->map(fn (Item $item) => ['item' => $item, 'owned' => $owned[$item->id], 'equipped' => (int) ($equipped[$item->id] ?? 0)])
            ->sortBy(fn ($row) => [$row['item']->kind->value, $row['item']->name])
            ->values();
    }

    /** @return Collection<int, Item> lo que vende la tienda de un mundo (lo suyo y lo común) */
    public function shop(Course $course): Collection
    {
        return Item::where('in_shop', true)->whereNotNull('price')
            ->where(fn ($q) => $q->where('course_id', $course->id)->orWhereNull('course_id'))
            ->orderBy('min_level')->orderBy('price')->get();
    }
}
