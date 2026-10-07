<?php

namespace App\Livewire\Admin;

use App\Models\Course;
use App\Models\Setting;
use App\Support\MailBudget;
use App\Support\Maintenance;
use Flux\Flux;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Configuración general: WhatsApp del profe, el mensaje prearmado, el correo (interruptor y tope diario) y el mantenimiento. */
#[Title('Configuración')]
class Settings extends Component
{
    public string $whatsapp_number = '';

    public string $whatsapp_message = '';

    public string $welcome_text = '';

    /** Correo (Support\MailBudget): si salen mails y cuántos por día como mucho. */
    public bool $mail_enabled = false;

    public int $mail_daily_limit = MailBudget::DEFAULT_LIMIT;

    /** Mantenimiento (Support\Maintenance, D86): la plataforma entera o algunos cursos. */
    public bool $maintenance_platform = false;

    public string $maintenance_message = '';

    /** @var list<string> ids de los cursos en mantenimiento */
    public array $maintenance_courses = [];

    public function mount(): void
    {
        foreach (['whatsapp_number', 'whatsapp_message', 'welcome_text'] as $key) {
            $this->{$key} = (string) Setting::get($key, '');
        }
        $this->mail_enabled = MailBudget::enabled();
        $this->mail_daily_limit = MailBudget::limit();
        $this->maintenance_platform = Maintenance::platform();
        $this->maintenance_message = (string) Setting::get('maintenance_message', '');
        $this->maintenance_courses = array_map('strval', Maintenance::courseIds());
    }

    public function saveMaintenance(): void
    {
        $this->validate([
            'maintenance_message' => ['nullable', 'string', 'max:300'],
            'maintenance_courses' => ['array'],
            'maintenance_courses.*' => ['integer', 'exists:courses,id'],
        ], [], ['maintenance_message' => 'mensaje']);
        Setting::put('maintenance_platform', $this->maintenance_platform ? '1' : '0');
        Setting::put('maintenance_message', trim($this->maintenance_message) ?: null);
        Setting::put('maintenance_courses', implode(',', array_map('intval', $this->maintenance_courses)) ?: null);

        $courses = count($this->maintenance_courses);
        Flux::toast(variant: $this->maintenance_platform ? 'warning' : 'success', text: match (true) {
            $this->maintenance_platform => 'Plataforma en mantenimiento: solo entrás vos. Los demás ven el aviso al entrar.',
            $courses > 0 => 'Plataforma abierta. '.($courses === 1 ? '1 curso queda' : $courses.' cursos quedan').' en mantenimiento.',
            default => 'Todo abierto: plataforma y cursos.',
        });
    }

    public function saveMail(): void
    {
        $this->validate(['mail_daily_limit' => ['required', 'integer', 'between:0,2000']], [], ['mail_daily_limit' => 'tope diario']);
        Setting::put('mail_enabled', $this->mail_enabled ? '1' : '0');
        Setting::put('mail_daily_limit', (string) $this->mail_daily_limit);

        Flux::toast(variant: 'success', text: $this->mail_enabled ? 'Correo activado: salen hasta '.$this->mail_daily_limit.' mails por día.' : 'Correo apagado: los avisos quedan solo en la campanita.');
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
        return view('livewire.admin.settings', [
            'mailSentToday' => MailBudget::sentToday(),
            'mailConfigured' => config('mail.default') === 'smtp',
            'courses' => Course::orderBy('position')->orderBy('title')->get(['id', 'title', 'is_published']),
            'defaultMaintenanceMessage' => Maintenance::DEFAULT_MESSAGE,
        ]);
    }
}
