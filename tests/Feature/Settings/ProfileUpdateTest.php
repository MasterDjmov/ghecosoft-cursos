<?php

use App\Livewire\Settings\Profile;
use App\Models\User;
use Livewire\Livewire;

test('la página de mi cuenta se muestra', function () {
    $this->actingAs(User::factory()->create())->get(route('profile.edit'))->assertOk();
});

test('el alumno actualiza sus datos, DNI y fecha de nacimiento', function () {
    $user = User::factory()->create();

    Livewire::actingAs($user)->test(Profile::class)
        ->set('name', 'Kira')
        ->set('last_name', 'Pérez')
        ->set('username', 'Kira_Perez')
        ->set('email', 'kira@example.com')
        ->set('dni', '40123456')
        ->set('birth_date', '2010-05-01')
        ->call('updateProfileInformation')
        ->assertHasNoErrors();

    $user->refresh();
    expect($user->username)->toBe('kira_perez')
        ->and($user->dni)->toBe('40123456')
        ->and($user->isMinor())->toBeTrue();
});

test('el DNI es opcional pero tiene que ser válido y único', function () {
    User::factory()->create(['dni' => '30111222']);
    $user = User::factory()->create();

    Livewire::actingAs($user)->test(Profile::class)->set('dni', '')->call('updateProfileInformation')->assertHasNoErrors();
    Livewire::actingAs($user)->test(Profile::class)->set('dni', '30.111.222')->call('updateProfileInformation')->assertHasErrors('dni');
    Livewire::actingAs($user)->test(Profile::class)->set('dni', '30111222')->call('updateProfileInformation')->assertHasErrors('dni');
});
