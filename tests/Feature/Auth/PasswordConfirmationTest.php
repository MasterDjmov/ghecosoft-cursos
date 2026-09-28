<?php

use App\Models\User;

test('la pantalla de confirmar la clave se muestra', function () {
    $this->actingAs(User::factory()->create())->get(route('password.confirm'))->assertOk();
});

test('con la clave correcta se entra a Seguridad', function () {
    $user = User::factory()->create();

    $this->actingAs($user)->get(route('security.edit'))->assertRedirect(route('password.confirm'));

    $this->actingAs($user)->post(route('password.confirm.store'), ['password' => 'password'])
        ->assertSessionHasNoErrors()
        ->assertRedirect(route('security.edit'));

    $this->actingAs($user)->get(route('security.edit'))->assertOk();
});

test('con la clave incorrecta avisa y no deja pasar', function () {
    $user = User::factory()->create();

    $this->actingAs($user)->post(route('password.confirm.store'), ['password' => 'incorrecta'])
        ->assertSessionHasErrors('password');

    $this->actingAs($user)->get(route('security.edit'))->assertRedirect(route('password.confirm'));
});
