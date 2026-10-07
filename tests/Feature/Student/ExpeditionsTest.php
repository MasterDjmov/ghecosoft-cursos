<?php

use App\Enums\CoinReason;
use App\Enums\ItemReason;
use App\Livewire\Student\Expeditions as ExpeditionsPage;
use App\Livewire\Student\Stables as StablesPage;
use App\Models\CoinTransaction;
use App\Models\Currency;
use App\Models\Expedition;
use App\Models\Hero;
use App\Models\Item;
use App\Models\Level;
use App\Models\Mount;
use App\Models\User;
use App\Services\Expeditions;
use App\Services\Heroes;
use App\Services\Inventory;
use App\Services\Ledger;
use App\Services\Stables;
use Livewire\Livewire;

/*
 * Expediciones y monturas (D91): el servidor calcula la aventura con una semilla fija, el oro va por el Ledger
 * y los ítems por la mochila; si pierde, vuelve sin botín.
 */

function expeditionWorld(int $placeLevel = 1, array $stats = ['strength' => 12, 'dexterity' => 4, 'intelligence' => 4, 'luck' => 4]): array
{
    $course = makeCourse();
    $course['root']->update(['code' => 'R00-N01']);
    $course['topic1']->update(['code' => 'R01-N01']);
    config(['game.protagonists.python.expeditions' => [
        'opens_after' => 'R00-N01',
        'map' => 'img/mundos/valle/mapa.webp',
        'places' => [
            ['code' => 'orilla', 'name' => 'La Orilla', 'node' => 'R00-N01', 'level' => $placeLevel, 'creatures' => ['slime'], 'x' => 10, 'y' => 10, 'text' => 'El río.'],
            ['code' => 'mercado', 'name' => 'El Mercado', 'node' => 'R01-N01', 'level' => 2, 'creatures' => ['goblin'], 'x' => 20, 'y' => 20, 'text' => 'Toldos.'],
        ],
    ]]);
    $student = studentWithRootOpen($course);
    approveRequiredPractices($student, $course['root']);
    $hero = app(Heroes::class)->create($student, $course['course'], 1, $stats);

    return [...$course, 'student' => $student, 'hero' => $hero];
}

function finishTrip(Expedition $expedition): Expedition
{
    $expedition->update(['ends_at' => now()->subSecond()]);

    return app(Expeditions::class)->resolve($expedition->fresh());
}

test('se abren al completar el nodo indicado, y solo los lugares de nodos completos', function () {
    $w = expeditionWorld();
    $service = app(Expeditions::class);
    $places = $service->places($w['student'], $w['course'])->keyBy('code');

    expect($service->isOpen($w['student'], $w['course']))->toBeTrue()
        ->and($places['orilla']['open'])->toBeTrue()
        ->and($places['mercado']['open'])->toBeFalse()
        ->and(collect($service->offers($w['student'], $w['course']))->pluck('place.code')->unique()->all())->toBe(['orilla']);

    $newcomer = studentWithRootOpen($w);
    expect($service->isOpen($newcomer, $w['course']))->toBeFalse()->and($service->offers($newcomer, $w['course']))->toBe([]);
});

test('una a la vez, con su reloj, hasta 6 por día', function () {
    $w = expeditionWorld();
    $service = app(Expeditions::class);

    $trip = $service->start($w['student'], $w['hero'], 0);
    expect((int) $trip->ends_at->diffInSeconds($trip->started_at, true))->toBe(300)
        ->and(fn () => $service->start($w['student'], $w['hero'], 1))->toThrow(InvalidArgumentException::class, 'en camino');

    // Antes de tiempo no se resuelve.
    expect($service->resolve($trip)->resolved_at)->toBeNull();

    for ($i = 1; $i < 6; $i++) {
        finishTrip($service->active($w['student']));
        $service->start($w['student'], $w['hero'], 0);
    }
    finishTrip($service->active($w['student']));
    expect(fn () => $service->start($w['student'], $w['hero'], 0))->toThrow(InvalidArgumentException::class, 'de hoy');
});

test('la montura acorta el viaje', function () {
    $w = expeditionWorld();
    Mount::create(['user_id' => $w['student']->id, 'species' => 'serphira', 'level' => 3]);

    $trip = app(Expeditions::class)->start($w['student'], $w['hero'], 0);
    expect((int) $trip->ends_at->diffInSeconds($trip->started_at, true))->toBe(210);
});

test('al volver, la aventura se calcula una vez, siempre igual, y paga el botín por el Ledger y la mochila', function () {
    $w = expeditionWorld();
    $service = app(Expeditions::class);
    Item::create(['code' => 'baba-de-slime', 'name' => 'Baba de Slime', 'kind' => 'material']);

    $trip = finishTrip($service->start($w['student'], $w['hero'], 0));
    $again = $service->simulate($trip, $w['hero']->fresh());

    expect($trip->won)->toBeTrue()
        ->and($trip->log)->not->toBeEmpty()
        ->and($again['log'])->toBe($trip->log)
        ->and(app(Heroes::class)->gold($w['student']))->toBe($trip->rewards['gold'])
        ->and(CoinTransaction::where('reason', CoinReason::ExpeditionLoot)->count())->toBe(1);

    $service->resolve($trip);
    expect(CoinTransaction::where('reason', CoinReason::ExpeditionLoot)->count())->toBe(1);
});

test('si pierde vuelve sin botín, pero las pociones que tomó se gastan', function () {
    $w = expeditionWorld(placeLevel: 40, stats: ['strength' => 4, 'dexterity' => 4, 'intelligence' => 12, 'luck' => 4]);
    $potion = Item::create(['code' => 'pocion', 'name' => 'Poción', 'kind' => 'potion', 'heal' => 20]);
    app(Inventory::class)->grant($w['student'], $potion, 5, ItemReason::ManualAdjustment);

    $trip = finishTrip(app(Expeditions::class)->start($w['student'], $w['hero'], 0));

    expect($trip->won)->toBeFalse()
        ->and(app(Heroes::class)->gold($w['student']))->toBe(0)
        ->and($trip->rewards['potions'])->toBeGreaterThan(0)
        ->and(app(Inventory::class)->owned($w['student'])[$potion->id])->toBe(5 - $trip->rewards['potions']);
});

test('los establos: comprar en n1 con nivel y oro, mejorar y cambiar de especie gratis', function () {
    $w = expeditionWorld();
    $stables = app(Stables::class);
    Level::create(['number' => 1, 'xp_required' => 0]);

    expect(fn () => $stables->buyOrUpgrade($w['student'], 'serphira'))->toThrow(InvalidArgumentException::class, 'nivel 3');
    Level::create(['number' => 3, 'xp_required' => 0]);
    app(Ledger::class)->credit($w['student'], Currency::gold(), 400, CoinReason::ManualAdjustment);

    $mount = $stables->buyOrUpgrade($w['student'], 'serphira');
    expect($mount->level)->toBe(1)->and(app(Heroes::class)->gold($w['student']))->toBe(100)
        ->and(fn () => $stables->buyOrUpgrade($w['student']))->toThrow(InvalidArgumentException::class, 'nivel 8');

    $stables->changeSpecies($w['student'], 'titan');
    expect($mount->fresh()->species)->toBe('titan')->and($mount->fresh()->level)->toBe(1);
});

test('desde la pantalla: mandar, volver y ver la pelea; y los establos', function () {
    $w = expeditionWorld();

    $page = Livewire::actingAs($w['student'])->test(ExpeditionsPage::class, ['course' => $w['course']])
        ->assertSee('La Orilla')
        ->call('send', 0)
        ->assertSee('en camino');
    Expedition::query()->update(['ends_at' => now()->subSecond()]);
    $page->call('claim')->assertSee('Saltar')->assertSee('botín');

    $this->actingAs($w['student'])->get(route('student.expeditions', $w['course']))->assertOk();
    $this->actingAs($w['student'])->get(route('student.expeditions.home'))->assertRedirect(route('student.expeditions', $w['course']));
    Livewire::actingAs($w['student'])->test(StablesPage::class)->assertSee('Serphira')->assertOk();
});

test('el héroe y la expedición son del jugador', function () {
    $w = expeditionWorld();
    $other = User::factory()->create();

    expect(fn () => app(Expeditions::class)->start($other, $w['hero'], 0))->toThrow(InvalidArgumentException::class);
    $trip = finishTrip(app(Expeditions::class)->start($w['student'], $w['hero'], 0));
    // Otro jugador (aunque pruebe la Clase 0) no ve ni mira las expediciones ajenas.
    Livewire::actingAs($other)->test(ExpeditionsPage::class, ['course' => $w['course']])
        ->assertDontSee('Las últimas')
        ->call('watch', $trip->id)->assertNotFound();
    expect(Hero::count())->toBe(1)->and($trip->user_id)->toBe($w['student']->id);
});

test('el Amuleto del Traceback equipado levanta al héroe una sola vez por expedición', function () {
    $w = expeditionWorld(placeLevel: 40);
    $amulet = Item::create(['code' => Item::TRACEBACK, 'name' => 'Amuleto del Traceback', 'kind' => 'accessory', 'rarity' => 'rare']);
    app(Inventory::class)->grant($w['student'], $amulet, 1, ItemReason::ManualAdjustment);
    app(Inventory::class)->equip($w['hero'], $amulet);

    $trip = finishTrip(app(Expeditions::class)->start($w['student'], $w['hero']->fresh(), 0));

    expect($trip->won)->toBeFalse()
        ->and(collect($trip->log)->where('t', 'revive')->count())->toBe(1);
});

test('el Reloj de Arena termina ya la expedición en camino y se gasta', function () {
    $w = expeditionWorld();
    $service = app(Expeditions::class);
    $hourglass = Item::create(['code' => Item::HOURGLASS, 'name' => 'Reloj de Arena', 'kind' => 'special', 'rarity' => 'rare']);

    $service->start($w['student'], $w['hero'], 0);
    expect(fn () => $service->hurry($w['student']))->toThrow(InvalidArgumentException::class, 'Reloj de Arena');

    app(Inventory::class)->grant($w['student'], $hourglass, 1, ItemReason::ManualAdjustment);
    Livewire::actingAs($w['student'])->test(ExpeditionsPage::class, ['course' => $w['course']])
        ->assertSee('Reloj de Arena (1)')
        ->call('hurry')
        ->call('claim')->assertSee('Saltar');

    expect(app(Inventory::class)->owned($w['student'])[$hourglass->id] ?? 0)->toBe(0)
        ->and(Expedition::first()->resolved_at)->not->toBeNull()
        ->and(fn () => $service->hurry($w['student']))->toThrow(InvalidArgumentException::class, 'en camino');
});
