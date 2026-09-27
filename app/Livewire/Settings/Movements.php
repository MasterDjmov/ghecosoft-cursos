<?php

namespace App\Livewire\Settings;

use App\Models\CoinTransaction;
use App\Models\XpTransaction;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Mi cuenta → Movimientos: de dónde salen mis monedas y mi XP. */
#[Title('Movimientos')]
class Movements extends Component
{
    public function render()
    {
        $user = auth()->user();

        return view('livewire.settings.movements', [
            'coins' => CoinTransaction::with('currency.course')->where('user_id', $user->id)->latest('id')->limit(100)->get(),
            'xp' => XpTransaction::where('user_id', $user->id)->latest('id')->limit(100)->get(),
        ]);
    }
}
