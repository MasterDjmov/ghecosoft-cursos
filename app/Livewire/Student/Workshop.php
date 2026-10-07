<?php

namespace App\Livewire\Student;

use App\Services\Crafting;
use App\Services\Inventory;
use Flux\Flux;
use Illuminate\Support\Facades\RateLimiter;
use InvalidArgumentException;
use Livewire\Attributes\Title;
use Livewire\Component;

/**
 * El taller (crafteo, D93): las recetas con lo que tiene y lo que le falta (y dónde cae cada material), lo que
 * se está fabricando con su reloj y el botón para recogerlo. Es del jugador, como la mochila.
 */
#[Title('Taller')]
class Workshop extends Component
{
    public function craft(string $recipe, Crafting $crafting): void
    {
        $key = 'craft:'.auth()->id();
        if (RateLimiter::tooManyAttempts($key, 10)) {
            Flux::toast(variant: 'danger', text: 'Más despacio: probá en un minuto.');

            return;
        }
        RateLimiter::hit($key, 60);

        try {
            $craft = $crafting->start(auth()->user(), $recipe);
            Flux::toast(variant: 'success', text: '¡Manos a la obra! '.$craft->item->name.' va a estar listo en un rato.');
        } catch (InvalidArgumentException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());
        }
    }

    public function collect(Crafting $crafting): void
    {
        try {
            $craft = $crafting->collect(auth()->user());
            Flux::toast(variant: 'success', text: $craft->item->name.($craft->quantity > 1 ? ' ×'.$craft->quantity : '').' ya está en tu mochila.');
        } catch (InvalidArgumentException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());
        }
    }

    public function render(Crafting $crafting, Inventory $inventory)
    {
        $user = auth()->user();
        $owned = $inventory->owned($user);
        $equipped = $inventory->equipped($user);

        return view('livewire.student.workshop', [
            'recipes' => $crafting->recipes(),
            'have' => fn ($item) => ($owned[$item->id] ?? 0) - ($equipped[$item->id] ?? 0),
            'active' => $crafting->active($user),
            'level' => Inventory::playerLevel($user),
            'sources' => fn ($item) => $crafting->sources($item),
            'seconds' => fn ($recipe) => $crafting->seconds($recipe),
        ]);
    }
}
