<?php

use App\Livewire\Admin\Characters;
use App\Models\User;
use App\Support\CharacterSheets;
use Livewire\Livewire;

/*
 * Historia → Personajes: las fichas de docs/historias/PERSONAJES.md con su pedido para Stitch. Solo el administrador.
 */

test('lee las fichas del .md, con su sección y si les falta la imagen', function () {
    $sheets = CharacterSheets::all()->keyBy('name');

    expect($sheets)->toHaveKeys(['Mia', 'Gheco', 'Sila', 'La cocinera de la Torre'])
        ->and($sheets['Mia']['protagonist'])->toBeTrue()
        ->and($sheets['Sila']['protagonist'])->toBeFalse()
        ->and($sheets['La cocinera de la Torre']['missing'])->toBeTrue()
        ->and($sheets['Sila']['missing'])->toBeFalse();

    $prompt = CharacterSheets::prompt($sheets['Sila']);
    expect($prompt)->toContain('Personaje: Sila')
        ->toContain('cuerpo entero 896×1200 y retrato circular')
        ->toContain(CharacterSheets::style())
        ->not->toContain('**');
});

test('el administrador ve las fichas y puede quedarse con las que faltan; el docente y el alumno no entran (los saca)', function () {
    $admin = User::factory()->admin()->create();
    $this->actingAs($admin)->get(route('admin.characters'))
        ->assertOk()->assertSee('Sila')->assertSee('data-test="copy-character-prompt"', false);

    Livewire::actingAs($admin)->test(Characters::class)
        ->set('onlyMissing', true)
        ->assertSee('La cocinera de la Torre')
        ->assertDontSee('data-test="character-sila"', false);

    $this->actingAs(User::factory()->teacher()->create())->get(route('admin.characters'))->assertRedirect();
    $this->actingAs(User::factory()->create())->get(route('admin.characters'))->assertRedirect();
});
