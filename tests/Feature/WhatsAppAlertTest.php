<?php

use App\Models\User;
use App\Notifications\PlatformNotification;
use App\Support\WhatsAppAlert;
use Illuminate\Support\Facades\Http;

/** Avisos al WhatsApp del docente con CallMeBot. */
test('sin número ni clave no manda nada', function () {
    Http::fake();
    config(['services.callmebot.phone' => null, 'services.callmebot.apikey' => null]);

    expect(WhatsAppAlert::send('hola'))->toBeFalse();
    Http::assertNothingSent();
});

test('al registrarse alguien manda el aviso corto, sin su mail ni su teléfono', function () {
    Http::fake(['api.callmebot.com/*' => Http::response('Message queued')]);
    config(['services.callmebot.phone' => '+5493800000000', 'services.callmebot.apikey' => '123456']);
    User::factory()->admin()->create();

    PlatformNotification::toAdmins(new PlatformNotification('user.registered', 'Se registró Kira Pérez', '@kira · kira@example.com · 3804000000', 'https://ejemplo/alumnos?ver=nuevos'));
    app()->terminate();

    Http::assertSent(fn ($request) => str_starts_with($request->url(), 'https://api.callmebot.com/whatsapp.php')
        && $request['phone'] === '+5493800000000' && $request['apikey'] === '123456'
        && str_contains($request['text'], 'Se registró Kira Pérez')
        && ! str_contains($request['text'], 'kira@example.com') && ! str_contains($request['text'], '3804000000'));
});

test('los demás avisos no van al WhatsApp y un error de CallMeBot no rompe nada', function () {
    Http::fake(['api.callmebot.com/*' => Http::response('error', 500)]);
    config(['services.callmebot.phone' => '+5493800000000', 'services.callmebot.apikey' => '123456']);
    User::factory()->admin()->create();

    PlatformNotification::toAdmins(new PlatformNotification('privacy.request', 'Pedido de privacidad', 'x', 'https://ejemplo'));
    app()->terminate();
    Http::assertNothingSent();

    expect(WhatsAppAlert::send('hola'))->toBeFalse();
});
