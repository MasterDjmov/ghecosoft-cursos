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

    public function mount(Service $stables): void
    {
        $this->species = $stables->mountOf(auth()->user())?->species ?? '';
    }

    public function choose(string $species, Service $stables): void
    {
        $this->species = $species;
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
