<?php

namespace App\Livewire\Settings;

use App\Concerns\PasswordValidationRules;
use Flux\Flux;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Livewire\Attributes\Layout;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Primer ingreso con la clave provisoria que dio el docente: elegir una propia. */
#[Layout('layouts::auth')]
#[Title('Elegí tu clave')]
class ChangeTemporaryPassword extends Component
{
    use PasswordValidationRules;

    public string $password = '';

    public string $password_confirmation = '';

    public function mount()
    {
        if (! Auth::user()->must_change_password) {
            return $this->redirectRoute('home', navigate: true);
        }
    }

    public function save()
    {
        $user = Auth::user();
        $this->validate(['password' => [...$this->passwordRules(), function ($attribute, $value, $fail) use ($user) {
            if (Hash::check($value, $user->password)) {
                $fail('Elegí una clave distinta de la provisoria.');
            }
        }]], attributes: ['password' => 'clave']);

        $user->forceFill(['password' => $this->password, 'must_change_password' => false])->save();
        Flux::toast(variant: 'success', text: '¡Listo! Ya tenés tu clave.');

        return $this->redirectRoute('home', navigate: true);
    }

    public function render()
    {
        return view('livewire.settings.change-temporary-password');
    }
}
