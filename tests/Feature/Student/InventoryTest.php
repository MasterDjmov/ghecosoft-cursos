<?php

use App\Enums\CoinReason;
use App\Enums\ItemReason;
use App\Exceptions\InsufficientFunds;
use App\Livewire\Admin\Items as AdminItems;
use App\Livewire\Student\Inventory as BagPage;
use App\Livewire\Student\Shop;
use App\Models\Currency;
use App\Models\Item;
use App\Models\ItemMovement;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\User;
use App\Services\Heroes;
use App\Services\Inventory;
use App\Services\Ledger;
use App\Services\StepCompleter;
use Livewire\Livewire;

/*
 * La mochila, la tienda y el equipo (D90): los ítems pasan por un libro de movimientos, el oro por el Ledger.
 */

function bagWorld(): array
{
    $course = makeCourse();
    $course['course']->update(['slug' => 'python']);
    $step = NodeStep::create([
        'node_id' => $course['root']->id, 'code' => 'R00-N01-P1', 'position' => 1, 'title' => 'La botica',
        'xp_reward' => 5, 'gold_reward' => 0, 'expected_output' => 'ok', 'item' => 'Poción de Curación x3',
    ]);
    $student = studentWithRootOpen($course);
    $sword = Item::create(['code' => 'vara', 'name' => 'Vara', 'kind' => 'weapon', 'course_id' => $course['course']->id, 'attack' => 2, 'strength' => 2, 'price' => 100, 'in_shop' => true]);
    $robe = Item::create(['code' => 'tunica', 'name' => 'Túnica', 'kind' => 'armor', 'defense' => 3, 'price' => 500, 'min_level' => 5, 'in_shop' => true]);
    $foreign = Item::create(['code' => 'espada-c', 'name' => 'Espada de C', 'kind' => 'weapon', 'course_id' => makeCourse(['slug' => 'c-otro'])['course']->id, 'attack' => 9]);
    $hero = app(Heroes::class)->create($student, $course['course'], 1, ['strength' => 6, 'dexterity' => 6, 'intelligence' => 6, 'luck' => 6]);

    return [...$course, 'step' => $step, 'student' => $student, 'sword' => $sword, 'robe' => $robe, 'foreign' => $foreign, 'hero' => $hero];
}

function giveGold(User $user, int $amount): void
{
    app(Ledger::class)->credit($user, Currency::gold(), $amount, CoinReason::ManualAdjustment);
}

test('el ítem de una micro-misión entra a la mochila una vez, con su cantidad, y también el de las ya superadas', function () {
    $w = bagWorld();
    $bag = app(Inventory::class);

    app(StepCompleter::class)->complete($w['student'], $w['step'], 'ok');
    app(StepCompleter::class)->complete($w['student'], $w['step'], 'ok');
    $potion = Item::where('name', 'Poción de Curación')->first();
    expect($potion->kind->value)->toBe('story')->and($bag->owned($w['student'])[$potion->id])->toBe(3);

    // Uno que la superó antes de que existiera la mochila.
    $other = studentWithRootOpen($w);
    NodeStepCompletion::create(['user_id' => $other->id, 'node_step_id' => $w['step']->id, 'completed_at' => now()]);
    $bag->settleItems($other);
    $bag->settleItems($other);
    expect($bag->owned($other)[$potion->id])->toBe(3);
});

test('se compra con oro, respetando el nivel mínimo, y sin oro no', function () {
    $w = bagWorld();
    $bag = app(Inventory::class);

    expect(fn () => $bag->buy($w['student'], $w['sword']))->toThrow(InsufficientFunds::class);
    giveGold($w['student'], 1000);
    $bag->buy($w['student'], $w['sword']);
    expect(fn () => $bag->buy($w['student'], $w['robe']))->toThrow(InvalidArgumentException::class, 'nivel 5');

    expect($bag->owned($w['student'])[$w['sword']->id])->toBe(1)
        ->and(app(Heroes::class)->gold($w['student']))->toBe(900)
        ->and(ItemMovement::where('reason', ItemReason::ShopPurchase)->count())->toBe(1);
});

test('equipar suma los bonos al héroe; no se equipa lo que no tiene ni lo de otro mundo', function () {
    $w = bagWorld();
    $bag = app(Inventory::class);

    expect(fn () => $bag->equip($w['hero'], $w['sword']))->toThrow(InvalidArgumentException::class);
    $bag->grant($w['student'], $w['sword'], 1, ItemReason::ManualAdjustment);
    $bag->grant($w['student'], $w['foreign'], 1, ItemReason::ManualAdjustment);

    $bag->equip($w['hero'], $w['sword']);
    $hero = $w['hero']->fresh();
    expect($hero->total('strength'))->toBe(8)->and($hero->hp())->toBe(130)->and($hero->bonus('attack'))->toBe(2)
        ->and($bag->available($w['student'], $w['sword']))->toBe(0)
        ->and(fn () => $bag->equip($hero, $w['foreign']))->toThrow(InvalidArgumentException::class, 'otro mundo')
        ->and(fn () => $bag->take($w['student'], $w['sword'], 1, ItemReason::Used))->toThrow(InvalidArgumentException::class);

    $bag->unequip($hero, 'weapon_item_id');
    expect($bag->available($w['student'], $w['sword']))->toBe(1);
});

test('el Pergamino del Reinicio deja reacomodar los puntos una vez, aunque ya haya comprado con oro', function () {
    $w = bagWorld();
    $heroes = app(Heroes::class);
    $bag = app(Inventory::class);
    giveGold($w['student'], 600);
    $heroes->upgrade($w['hero'], 'luck');
    expect($heroes->canRedistribute($w['hero']->fresh()))->toBeFalse();

    $scroll = Item::create(['code' => Item::RESPEC, 'name' => 'Pergamino del Reinicio', 'kind' => 'special']);
    $bag->grant($w['student'], $scroll, 1, ItemReason::ManualAdjustment);
    $bag->use($w['student'], $scroll, $w['hero']);

    $hero = $w['hero']->fresh();
    expect($heroes->canRedistribute($hero))->toBeTrue()->and($bag->available($w['student'], $scroll))->toBe(0);
    $heroes->redistribute($hero, ['strength' => 12, 'dexterity' => 4, 'intelligence' => 4, 'luck' => 4]);
    expect($heroes->canRedistribute($hero->fresh()))->toBeFalse()->and($hero->fresh()->strength)->toBe(12);
});

test('la tienda y la mochila desde la pantalla', function () {
    $w = bagWorld();
    giveGold($w['student'], 300);
    config(['game.protagonists.python.shop' => ['name' => 'El puesto de Baldo', 'keeper' => 'Baldo', 'portrait' => 'img/personajes/baldo.webp', 'greeting' => 'Hola']]);

    Livewire::actingAs($w['student'])->test(Shop::class, ['course' => $w['course']])
        ->assertSee('El puesto de Baldo')->assertSee('Vara')
        ->call('buy', $w['sword']->id);
    expect(app(Inventory::class)->owned($w['student'])[$w['sword']->id])->toBe(1);

    Livewire::actingAs($w['student'])->test(BagPage::class)
        ->assertSee('Vara')
        ->call('equip', $w['sword']->id, $w['hero']->id)
        ->assertSee('Puesto');
    expect($w['hero']->fresh()->weapon_item_id)->toBe($w['sword']->id);

    $this->actingAs($w['student'])->get(route('student.inventory'))->assertOk();
    $this->actingAs($w['student'])->get(route('student.shop', $w['course']))->assertOk();
});

test('el admin crea y edita ítems; uno que ya tienen jugadores no se borra', function () {
    $w = bagWorld();
    $admin = User::factory()->admin()->create();

    Livewire::actingAs($admin)->test(AdminItems::class)
        ->call('create')
        ->set('form.name', 'Escudo de Prueba')->set('form.kind', 'armor')->set('form.defense', 4)->set('form.price', 200)->set('form.in_shop', true)
        ->call('save')->assertHasNoErrors();
    expect(Item::where('code', 'escudo-de-prueba')->value('defense'))->toBe(4);

    app(Inventory::class)->grant($w['student'], $w['sword'], 1, ItemReason::ManualAdjustment);
    Livewire::actingAs($admin)->test(AdminItems::class)->call('delete', $w['sword']->id);
    expect(Item::find($w['sword']->id))->not->toBeNull();

    $this->actingAs($admin)->get(route('admin.items'))->assertOk();
    $this->actingAs($w['student'])->get(route('admin.items'))->assertRedirect();
});

test('cada ítem tiene su pedido de imagen: el catálogo lo completa sin pisar el del docente, y se filtran los que no tienen imagen', function () {
    makeCourse();
    $mine = Item::create(['code' => 'vara-de-junco', 'name' => 'Vara de Junco', 'kind' => 'weapon', 'image_prompt' => 'La mía, de sauce.']);
    $this->artisan('app:game-items')->assertSuccessful();

    expect($mine->fresh()->image_prompt)->toBe('La mía, de sauce.')
        ->and(Item::where('code', 'pocion-grande')->value('image_prompt'))->toContain('frasco grande');

    $prompt = Item::where('code', 'pocion-grande')->first()->fullImagePrompt();
    expect($prompt)->toContain('Ítem: Poción Grande')->toContain('brillo celeste')->toContain(Item::IMAGE_STYLE);

    $admin = User::factory()->admin()->create();
    Item::where('code', 'pocion-grande')->update(['image_path' => 'items/pocion.webp']);
    Livewire::actingAs($admin)->test(AdminItems::class)
        ->assertSee('data-test="copy-item-prompt-pocion-grande"', false)
        ->set('onlyMissing', true)
        ->assertDontSee('data-test="copy-item-prompt-pocion-grande"', false)
        ->assertSee('data-test="copy-item-prompt-pergamino-del-reinicio"', false)
        ->call('edit', $mine->id)->assertSet('form.image_prompt', 'La mía, de sauce.')
        ->set('form.image_prompt', 'De sauce llorón.')->call('save');
    expect($mine->fresh()->image_prompt)->toBe('De sauce llorón.');
});
