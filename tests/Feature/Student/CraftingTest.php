<?php

use App\Enums\ItemReason;
use App\Livewire\Student\Workshop;
use App\Models\Craft;
use App\Models\Item;
use App\Models\User;
use App\Services\Crafting;
use App\Services\Inventory;
use Livewire\Livewire;

/*
 * El taller (crafteo, D93): recetas fijas, los ingredientes salen de la mochila al empezar (por el libro de
 * ítems), el resultado entra al terminar el tiempo, una cosa a la vez y sin cron.
 */

function workshop(): array
{
    config(['game.recipes' => [
        ['code' => 'pluma-mejor', 'gives' => ['pluma-mejor' => 1], 'needs' => ['pluma' => 1, 'diente' => 3], 'minutes' => 10, 'min_level' => 1],
        ['code' => 'pocion-de-baba', 'gives' => ['pocion' => 2], 'needs' => ['baba' => 3], 'minutes' => 5, 'min_level' => 1],
        ['code' => 'alta', 'gives' => ['pocion' => 1], 'needs' => ['baba' => 1], 'minutes' => 5, 'min_level' => 50],
        ['code' => 'rota', 'gives' => ['no-existe' => 1], 'needs' => ['baba' => 1], 'minutes' => 5, 'min_level' => 1],
    ]]);
    $items = collect([
        ['code' => 'pluma', 'name' => 'Pluma', 'kind' => 'weapon'],
        ['code' => 'pluma-mejor', 'name' => 'Pluma Mejor', 'kind' => 'weapon', 'rarity' => 'rare', 'attack' => 6],
        ['code' => 'diente', 'name' => 'Diente de Goblin', 'kind' => 'material'],
        ['code' => 'baba', 'name' => 'Baba de Slime', 'kind' => 'material'],
        ['code' => 'pocion', 'name' => 'Poción', 'kind' => 'potion', 'heal' => 40],
    ])->mapWithKeys(fn ($row) => [$row['code'] => Item::create($row)]);

    return ['items' => $items, 'user' => User::factory()->create()];
}

test('solo muestra las recetas cuyos ítems existen', function () {
    workshop();

    expect(app(Crafting::class)->recipes()->pluck('code')->all())->toBe(['pluma-mejor', 'pocion-de-baba', 'alta']);
});

test('fabricar descuenta los ingredientes, tarda y al recoger entra el resultado una sola vez', function () {
    ['items' => $items, 'user' => $user] = workshop();
    $inventory = app(Inventory::class);
    $crafting = app(Crafting::class);
    $inventory->grant($user, $items['pluma'], 1, ItemReason::ManualAdjustment);
    $inventory->grant($user, $items['diente'], 4, ItemReason::ManualAdjustment);
    $inventory->grant($user, $items['baba'], 9, ItemReason::ManualAdjustment);

    $craft = $crafting->start($user, 'pluma-mejor');
    expect($inventory->owned($user)[$items['diente']->id])->toBe(1)
        ->and($inventory->owned($user)->has($items['pluma']->id))->toBeFalse()
        ->and((int) $craft->started_at->diffInSeconds($craft->ends_at))->toBe(600)
        ->and(fn () => $crafting->start($user, 'pocion-de-baba'))->toThrow(InvalidArgumentException::class, 'ocupado')
        ->and(fn () => $crafting->collect($user))->toThrow(InvalidArgumentException::class, 'listo');

    $this->travel(11)->minutes();
    $crafting->collect($user);
    expect($inventory->owned($user)[$items['pluma-mejor']->id])->toBe(1)
        ->and(fn () => $crafting->collect($user))->toThrow(InvalidArgumentException::class)
        ->and(Craft::first()->collected_at)->not->toBeNull();

    // Libre otra vez; las recetas con cantidad dan varias.
    $crafting->start($user, 'pocion-de-baba');
    $this->travel(6)->minutes();
    $crafting->collect($user);
    expect($inventory->owned($user)[$items['pocion']->id])->toBe(2);
});

test('no fabrica sin los ingredientes (los equipados no cuentan) ni sin el nivel', function () {
    ['items' => $items, 'user' => $user] = workshop();
    app(Inventory::class)->grant($user, $items['diente'], 3, ItemReason::ManualAdjustment);

    expect(fn () => app(Crafting::class)->start($user, 'pluma-mejor'))->toThrow(InvalidArgumentException::class, 'Te falta Pluma')
        ->and(fn () => app(Crafting::class)->start($user, 'alta'))->toThrow(InvalidArgumentException::class, 'nivel 50')
        ->and(fn () => app(Crafting::class)->start($user, 'rota'))->toThrow(InvalidArgumentException::class, 'no existe')
        ->and(Craft::count())->toBe(0);
});

test('el taller desde la pantalla: ve lo que le falta, fabrica y recoge', function () {
    ['items' => $items, 'user' => $user] = workshop();
    app(Inventory::class)->grant($user, $items['baba'], 3, ItemReason::ManualAdjustment);

    Livewire::actingAs($user)->test(Workshop::class)
        ->assertSee('Pluma Mejor')->assertSee('0/3')
        ->call('craft', 'pocion-de-baba')
        ->assertSee('En el taller');
    $this->travel(6)->minutes();
    Livewire::actingAs($user)->test(Workshop::class)->call('collect')->assertDontSee('En el taller');

    expect(app(Inventory::class)->owned($user)[$items['pocion']->id])->toBe(2);
    $this->actingAs($user)->get(route('student.workshop'))->assertOk()->assertSee('data-test="menu-workshop"', false);
});
