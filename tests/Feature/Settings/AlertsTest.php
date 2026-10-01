<?php

use App\Livewire\NotificationsBell;
use App\Livewire\Settings\Alerts;
use App\Models\User;
use App\Notifications\PlatformNotification;
use Livewire\Livewire;

test('cada usuario elige si suenan los avisos y si salen fuera del navegador', function () {
    $user = User::factory()->create();
    expect($user->alert_sound)->toBeTrue()->and($user->alert_desktop)->toBeFalse();

    $this->actingAs($user)->get(route('alerts'))->assertOk()->assertSee('Sonar cuando llega algo nuevo');
    Livewire::actingAs($user)->test(Alerts::class)
        ->set('alert_sound', false)
        ->set('alert_desktop', true)
        ->call('save')
        ->assertDispatched('alert-preferences', sound: false, desktop: true);

    expect($user->fresh())->alert_sound->toBeFalse()->alert_desktop->toBeTrue();
});

test('la campanita manda al navegador la cantidad sin leer, el último aviso y las preferencias', function () {
    $user = User::factory()->create(['alert_sound' => false]);
    $user->notify(new PlatformNotification('prueba', 'Te corrigieron', 'Aprobada', url('/mundos')));

    Livewire::actingAs($user)->test(NotificationsBell::class)
        ->assertDispatched('live-alerts', fn ($name, $params) => $params['unread'] === 1
            && $params['newest']['title'] === 'Te corrigieron'
            && $params['sound'] === false
            && $params['user'] === $user->id)
        ->assertSeeHtml('x-data="liveBell"');
});
