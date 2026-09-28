<?php

use App\Livewire\Settings\Security;
use App\Models\User;
use App\Support\TrustedProxies;
use Illuminate\Http\Middleware\TrustProxies;
use Illuminate\Support\Facades\Notification;
use Illuminate\Support\Facades\Route;
use Livewire\Livewire;

test('después de 5 claves mal para el mismo usuario, el login se frena aunque la sexta sea correcta', function () {
    $user = User::factory()->create();

    foreach (range(1, 5) as $i) {
        $this->post(route('login.store'), ['login' => $user->username, 'password' => 'mal'.$i])->assertSessionHasErrors('login');
    }

    $this->post(route('login.store'), ['login' => $user->username, 'password' => 'password'])
        ->assertSessionHasErrors(['login' => __('auth.throttle', ['seconds' => 60])]);

    $this->assertGuest();
});

test('desde una misma IP no se pueden probar muchos usuarios distintos', function () {
    foreach (range(1, 20) as $i) {
        $this->post(route('login.store'), ['login' => "usuario{$i}", 'password' => 'x']);
    }

    $user = User::factory()->create();
    $this->post(route('login.store'), ['login' => $user->username, 'password' => 'password'])
        ->assertSessionHasErrors('login');

    $this->assertGuest();
});

test('olvidé mi clave responde igual exista o no la cuenta, y tiene tope', function () {
    Notification::fake();

    $this->post(route('password.email'), ['email' => 'nadie@ejemplo.com'])
        ->assertSessionHasNoErrors()
        ->assertSessionHas('status', __('passwords.sent'));

    foreach (range(1, 4) as $i) {
        $this->post(route('password.email'), ['email' => "otro{$i}@ejemplo.com"]);
    }

    $this->post(route('password.email'), ['email' => 'ultimo@ejemplo.com'])->assertSessionHasErrors('email');
});

test('confirmar la clave tiene tope de intentos', function () {
    $user = User::factory()->create();

    foreach (range(1, 5) as $i) {
        $this->actingAs($user)->post(route('password.confirm.store'), ['password' => 'mal'.$i]);
    }

    $this->actingAs($user)->post(route('password.confirm.store'), ['password' => 'password'])
        ->assertSessionHasErrors('password');
});

test('cambiar la clave desde el perfil tiene tope de intentos', function () {
    $user = User::factory()->create();

    foreach (range(1, 5) as $i) {
        Livewire::actingAs($user)->test(Security::class)
            ->set('current_password', 'mal'.$i)->set('password', 'NuevaClave1')->set('password_confirmation', 'NuevaClave1')
            ->call('updatePassword');
    }

    Livewire::actingAs($user)->test(Security::class)
        ->set('current_password', 'password')->set('password', 'NuevaClave1')->set('password_confirmation', 'NuevaClave1')
        ->call('updatePassword')
        ->assertHasErrors('current_password');
});

test('las páginas llevan las cabeceras de seguridad', function () {
    $this->get(route('login'))
        ->assertHeader('X-Frame-Options', 'SAMEORIGIN')
        ->assertHeader('X-Content-Type-Options', 'nosniff')
        ->assertHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
});

test('detrás de Cloudflare se usa la IP real del alumno, y un X-Forwarded-For de afuera no engaña', function () {
    Route::middleware('web')->get('/_ip', fn () => request()->ip());

    config(['security.trusted_proxies' => 'cloudflare']);
    TrustedProxies::apply();

    $this->withServerVariables(['REMOTE_ADDR' => '173.245.48.10'])->withHeader('X-Forwarded-For', '200.45.1.7')
        ->get('/_ip')->assertSee('200.45.1.7');

    $this->withServerVariables(['REMOTE_ADDR' => '8.8.8.8'])->withHeader('X-Forwarded-For', '200.45.1.7')
        ->get('/_ip')->assertSee('8.8.8.8');

    TrustProxies::flushState();
});
