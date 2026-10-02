<?php

use App\Livewire\Admin\Settings;
use App\Models\Setting;
use App\Models\User;
use App\Notifications\PlatformNotification;
use App\Notifications\SafeMailChannel;
use App\Support\MailBudget;
use Illuminate\Support\Facades\Mail;
use Livewire\Livewire;

/*
 * El correo de la plataforma (Configuración → Correo): un interruptor, un tope por día y un mail que falla
 * no rompe ninguna página. El Gmail del docente tiene un límite diario que comparte con su otra página.
 */

beforeEach(function () {
    // Un SMTP que no existe: si algo intentara mandar de verdad, fallaría la conexión.
    config(['mail.default' => 'smtp', 'mail.mailers.smtp.host' => 'smtp.no-existe.invalid', 'mail.mailers.smtp.port' => 2525, 'mail.mailers.smtp.timeout' => 2]);
    $this->admin = User::factory()->admin()->create(['email' => 'profe@ejemplo.com']);
});

test('de fábrica el correo está apagado: ningún mail sale y los avisos quedan en la campanita', function () {
    expect(MailBudget::enabled())->toBeFalse()
        ->and((new PlatformNotification('prueba', 'Hola', 'Un aviso', '/'))->via($this->admin))->toBe(['database']);

    // Un mail suelto (recuperar la clave, por ejemplo) se cancela antes de conectarse.
    Mail::raw('Hola', fn ($m) => $m->to('alguien@ejemplo.com'));
    expect(MailBudget::sentToday())->toBe(0);
});

test('prendido, si el servidor de correo falla el aviso igual se guarda y no hay error', function () {
    Setting::put('mail_enabled', '1');
    expect((new PlatformNotification('prueba', 'Hola', 'Un aviso', '/'))->via($this->admin))->toContain(SafeMailChannel::class);

    PlatformNotification::toAdmins(new PlatformNotification('prueba', 'Nueva solicitud', 'Alguien pidió un curso.', '/'));

    expect($this->admin->notifications()->count())->toBe(1);
});

test('al llegar al tope del día no sale nada más, y si Gmail avisa su límite se corta hasta mañana', function () {
    Setting::put('mail_enabled', '1');
    Setting::put('mail_daily_limit', '2');
    MailBudget::record();
    expect(MailBudget::canSend())->toBeTrue();
    MailBudget::record();
    expect(MailBudget::canSend())->toBeFalse()
        ->and((new PlatformNotification('prueba', 'Hola', 'Un aviso', '/'))->via($this->admin))->toBe(['database']);

    $this->travel(1)->days();
    expect(MailBudget::canSend())->toBeTrue();
    MailBudget::exhaust();
    expect(MailBudget::canSend())->toBeFalse();
});

test('el administrador prende el correo, cambia el tope y ve cuántos salieron hoy', function () {
    MailBudget::record();

    Livewire::actingAs($this->admin)->test(Settings::class)
        ->assertSee('data-test="mail-counter"', false)
        ->assertSee('1 <span', false)
        ->set('mail_enabled', true)
        ->set('mail_daily_limit', 250)
        ->call('saveMail')
        ->assertHasNoErrors();

    expect(MailBudget::enabled())->toBeTrue()->and(MailBudget::limit())->toBe(250);
});
