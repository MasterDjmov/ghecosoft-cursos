<?php

namespace App\Livewire\Settings;

use Livewire\Attributes\Title;
use Livewire\Component;

/** Mi cuenta → Movimientos: de dónde salen mis monedas y mi XP. */
#[Title('Movimientos')]
class Movements extends Component
{
    public function render()
    {
        return view('livewire.settings.movements');
    }
}
