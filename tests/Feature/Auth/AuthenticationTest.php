<?php

use App\Models\User;
use Laravel\Fortify\Features;

test('la pantalla de login se muestra', function () {
    $this->get(route('login'))->assertOk()->assertSee('Usuario o email');
});

test('se puede entrar con el email', function () {
    $user = User::factory()->create();

    $this->post(route('login.store'), ['login' => $user->email, 'password' => 'password'])
        ->assertSessionHasNoErrors()
        ->assertRedirect(route('home', absolute: false));

    $this->assertAuthenticatedAs($user);
});

test('se puede entrar con el usuario, sin importar mayúsculas', function () {
    $user = User::factory()->create(['username' => 'kira_perez']);

    $this->post(route('login.store'), ['login' => 'Kira_Perez', 'password' => 'password'])
        ->assertSessionHasNoErrors();

    $this->assertAuthenticatedAs($user);
});

test('no se puede entrar con una contraseña incorrecta', function () {
    $user = User::factory()->create();

    $this->post(route('login.store'), ['login' => $user->username, 'password' => 'incorrecta'])
        ->assertSessionHasErrors('login');

    $this->assertGuest();
});

test('con 2FA activado se pide el código', function () {
    $this->skipUnlessFortifyHas(Features::twoFactorAuthentication());

    $user = User::factory()->withTwoFactor()->create();

    $this->post(route('login.store'), ['login' => $user->email, 'password' => 'password'])
        ->assertRedirect(route('two-factor.login'));

    $this->assertGuest();
});

test('se puede salir de la cuenta', function () {
    $user = User::factory()->create();

    $this->actingAs($user)->post(route('logout'))->assertRedirect('/');

    $this->assertGuest();
});

test('después de entrar, cada rol va a su inicio', function () {
    $this->actingAs(User::factory()->create())->get(route('home'))->assertRedirect(route('student.worlds'));
    $this->actingAs(User::factory()->admin()->create())->get(route('home'))->assertRedirect(route('admin.dashboard'));
});
