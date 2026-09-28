<?php

use App\Enums\Role;
use App\Models\User;

function registrationData(array $overrides = []): array
{
    return [
        'name' => 'Kira',
        'last_name' => 'Pérez',
        'username' => 'kira_perez',
        'email' => 'kira@example.com',
        'password' => 'Secreta123',
        'password_confirmation' => 'Secreta123',
        ...$overrides,
    ];
}

test('la pantalla de registro se muestra', function () {
    $this->get(route('register'))->assertOk()->assertSee('Apellido');
});

test('un alumno se registra con nombre, apellido y usuario', function () {
    $this->post(route('register.store'), registrationData())
        ->assertSessionHasNoErrors()
        ->assertRedirect(route('home', absolute: false));

    $user = User::where('username', 'kira_perez')->firstOrFail();
    expect($user->last_name)->toBe('Pérez')
        ->and($user->role)->toBe(Role::Student);
    $this->assertAuthenticatedAs($user);
});

test('el registro nunca crea un admin aunque se mande el rol', function () {
    $this->post(route('register.store'), registrationData(['role' => 'admin']));

    expect(User::where('username', 'kira_perez')->first()->role)->toBe(Role::Student);
});

test('la contraseña necesita 8 caracteres, mayúscula, minúscula y número', function (string $password) {
    $this->post(route('register.store'), registrationData(['password' => $password, 'password_confirmation' => $password]))
        ->assertSessionHasErrors('password');

    $this->assertGuest();
})->with(['corta' => 'Ab1', 'sin mayúscula' => 'secreta123', 'sin minúscula' => 'SECRETA123', 'sin número' => 'Secretaaa']);

test('el usuario tiene que ser único, en minúsculas y no reservado', function (string $username) {
    User::factory()->create(['username' => 'ocupado']);

    $this->post(route('register.store'), registrationData(['username' => $username]))
        ->assertSessionHasErrors('username');
})->with(['repetido' => 'ocupado', 'reservado' => 'admin', 'con espacios' => 'kira perez', 'muy corto' => 'ab']);

test('el email es opcional y se puede dejar el teléfono (D36)', function () {
    $this->post(route('register.store'), registrationData(['email' => '', 'phone' => '+54 9 380 412-3456']))
        ->assertSessionHasNoErrors();

    $user = User::where('username', 'kira_perez')->firstOrFail();
    expect($user->email)->toBeNull()
        ->and($user->phone)->toBe('+54 9 380 412-3456');
});
