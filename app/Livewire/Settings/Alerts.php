<?php

namespace App\Livewire\Settings;

use Flux\Flux;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Mi cuenta → Avisos: el sonido y la notificación del sistema cuando llega algo nuevo (D62). */
#[Title('Avisos')]
class Alerts extends Component
{
    public bool $alert_sound = true;

    public bool $alert_desktop = false;

    public function mount(): void
    {
        $this->alert_sound = auth()->user()->alert_sound;
        $this->alert_desktop = auth()->user()->alert_desktop;
    }

    public function save(): void
    {
        $this->validate(['alert_sound' => ['boolean'], 'alert_desktop' => ['boolean']]);
        auth()->user()->update(['alert_sound' => $this->alert_sound, 'alert_desktop' => $this->alert_desktop]);

        // La campanita toma las preferencias nuevas sin recargar.
        $this->dispatch('alert-preferences', sound: $this->alert_sound, desktop: $this->alert_desktop);
        Flux::toast(variant: 'success', text: 'Listo, guardamos tus avisos.');
    }

    public function render()
    {
        return view('livewire.settings.alerts');
    }
}
