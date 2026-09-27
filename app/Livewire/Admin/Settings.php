<?php

namespace App\Livewire\Admin;

use App\Models\Setting;
use Flux\Flux;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Configuración general: WhatsApp del profe y el mensaje prearmado. */
#[Title('Configuración')]
class Settings extends Component
{
    public string $whatsapp_number = '';

    public string $whatsapp_message = '';

    public string $welcome_text = '';

    public function mount(): void
    {
        foreach (['whatsapp_number', 'whatsapp_message', 'welcome_text'] as $key) {
            $this->{$key} = (string) Setting::get($key, '');
        }
    }

    public function save(): void
    {
        $data = $this->validate([
            'whatsapp_number' => ['nullable', 'string', 'max:25', 'regex:/^\+?[0-9 ()-]{8,25}$/'],
            'whatsapp_message' => ['nullable', 'string', 'max:500'],
            'welcome_text' => ['nullable', 'string', 'max:255'],
        ], ['whatsapp_number.regex' => 'Escribí el número con código de país y de área, por ejemplo +54 9 380 412-3456.'], [
            'whatsapp_number' => 'WhatsApp', 'whatsapp_message' => 'mensaje',
        ]);

        foreach ($data as $key => $value) {
            Setting::put($key, $value);
        }

        Flux::toast(variant: 'success', text: 'Configuración guardada.');
    }

    public function render()
    {
        return view('livewire.admin.settings');
    }
}
