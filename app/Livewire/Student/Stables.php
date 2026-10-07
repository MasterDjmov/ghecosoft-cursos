<?php

namespace App\Livewire\Student;

use App\Exceptions\InsufficientFunds;
use App\Services\Heroes;
use App\Services\Inventory;
use App\Services\Stables as Service;
use Flux\Flux;
use InvalidArgumentException;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Los establos (D91): la montura del jugador, una para todos sus héroes. */
#[Title('Establos')]
class Stables extends Component
{
    public string $species = '';

    /** La especie cuya ficha (sus 5 evoluciones) se está mirando; nada se compra ni se cambia con solo mirar. */
    public ?string $preview = null;

    public function mount(Service $stables): void
    {
        $this->species = $stables->mountOf(auth()->user())?->species ?? '';
    }

    public function inspect(string $species): void
    {
        $this->preview = array_key_exists($species, config('game.mounts.species')) ? $species : null;
    }

    public function closePreview(): void
    {
        $this->preview = null;
    }

    /** Desde la ficha: sin montura, la elige y la compra en n1; con montura, le cambia la especie (gratis). */
    public function choose(string $species, Service $stables): void
    {
        if (! array_key_exists($species, config('game.mounts.species'))) {
            return;
        }
        $this->preview = null;
        $this->species = $species;
        if (! $stables->mountOf(auth()->user())) {
            $this->buy($stables);

            return;
        }
        if ($stables->mountOf(auth()->user())) {
            try {
                $stables->changeSpecies(auth()->user(), $species);
                Flux::toast(variant: 'success', text: 'Ahora tu montura es '.config('game.mounts.species.'.$species).'.');
            } catch (InvalidArgumentException $e) {
                Flux::toast(variant: 'danger', text: $e->getMessage());
            }
        }
    }

    public function buy(Service $stables): void
    {
        try {
            $mount = $stables->buyOrUpgrade(auth()->user(), $this->species ?: null);
            Flux::toast(variant: 'success', text: $mount->name().' llega a n'.$mount->level.': las expediciones duran '.$mount->reduction().'% menos.');
        } catch (InsufficientFunds $e) {
            Flux::toast(variant: 'danger', text: 'No te alcanza el oro: tenés '.$e->balance.' y cuesta '.$e->required.'.');
        } catch (InvalidArgumentException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());
        }
    }

    public function render(Service $stables, Heroes $heroes)
    {
        $user = auth()->user();
        $mount = $stables->mountOf($user);

        return view('livewire.student.stables', [
            'mount' => $mount,
            'next' => $stables->next($mount),
            'nextLevel' => ($mount?->level ?? 0) + 1,
            'levels' => config('game.mounts.levels'),
            'allSpecies' => config('game.mounts.species'),
            'gold' => $heroes->gold($user),
            'playerLevel' => Inventory::playerLevel($user),
        ]);
    }
}
