<?php

namespace App\Livewire\Student;

use App\Enums\ItemKind;
use App\Exceptions\InsufficientFunds;
use App\Models\Course;
use App\Models\Item;
use App\Services\Heroes;
use App\Services\Inventory;
use Flux\Flux;
use Illuminate\Support\Facades\RateLimiter;
use InvalidArgumentException;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;

/** La tienda de un mundo (D90): en el Valle, el puesto de Baldo. Armas, ropa, accesorios, pociones y especiales. */
#[Title('Tienda')]
class Shop extends Component
{
    public Course $course;

    #[Url(as: 'tipo')]
    public string $kind = 'weapon';

    public function mount(Course $course, Heroes $heroes): void
    {
        $this->authorize('play', $course);
        abort_if(($heroes->protagonist($course)['shop'] ?? null) === null, 404);
    }

    public function buy(int $itemId, Inventory $inventory): void
    {
        $key = 'shop-buy:'.auth()->id();
        if (RateLimiter::tooManyAttempts($key, 30)) {
            Flux::toast(variant: 'danger', text: 'Más despacio: probá en un minuto.');

            return;
        }
        RateLimiter::hit($key, 60);

        $item = $inventory->shop($this->course)->firstWhere('id', $itemId);
        abort_unless($item instanceof Item, 404);
        try {
            $inventory->buy(auth()->user(), $item);
            Flux::toast(variant: 'success', text: '¡Compraste '.$item->name.'! Está en tu mochila.');
        } catch (InsufficientFunds $e) {
            Flux::toast(variant: 'danger', text: 'No te alcanza el oro: tenés '.$e->balance.' y cuesta '.$e->required.'.');
        } catch (InvalidArgumentException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());
        }
    }

    public function render(Heroes $heroes, Inventory $inventory)
    {
        $user = auth()->user();
        $items = $inventory->shop($this->course)->load('course');
        $kinds = collect([ItemKind::Weapon, ItemKind::Armor, ItemKind::Accessory, ItemKind::Potion, ItemKind::Special])
            ->filter(fn (ItemKind $kind) => $items->contains(fn (Item $item) => $item->kind === $kind))->values();

        return view('livewire.student.shop', [
            'shop' => $heroes->protagonist($this->course)['shop'],
            'kinds' => $kinds,
            'items' => $items->filter(fn (Item $item) => $item->kind->value === $this->kind)->values(),
            'gold' => $heroes->gold($user),
            'level' => Inventory::playerLevel($user),
            'owned' => $inventory->owned($user),
        ]);
    }
}
