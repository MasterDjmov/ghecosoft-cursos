<?php

use App\Enums\CoinReason;
use App\Exceptions\InsufficientFunds;
use App\Livewire\Admin\Students\Show;
use App\Livewire\Student\Grimoire;
use App\Livewire\Student\Hero as HeroPage;
use App\Livewire\Student\Heroes as HeroesPage;
use App\Models\CoinTransaction;
use App\Models\Currency;
use App\Models\Hero;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\User;
use App\Services\Heroes;
use App\Services\Ledger;
use App\Services\StepCompleter;
use Livewire\Livewire;

/*
 * El héroe (D89): el protagonista de cada curso con su aspecto y sus atributos, el oro del jugador
 * (por el Ledger) y el grimorio con las cartas de las micro-misiones.
 */

function heroCourse(): array
{
    $course = makeCourse();
    $step = NodeStep::create([
        'node_id' => $course['root']->id, 'code' => 'R00-N01-P1', 'position' => 1, 'title' => 'El pergamino habla',
        'card_title' => 'print', 'card_body' => 'print("texto") · print(a, b, sep=" | ")',
        'xp_reward' => 10, 'gold_reward' => 15, 'expected_output' => 'Hola',
    ]);
    $course['course']->rootNode()?->update(['is_published' => true]);

    return [...$course, 'step' => $step];
}

function goldOf(User $user): int
{
    return app(Ledger::class)->balance($user, Currency::gold());
}

test('superar una micro-misión da su oro una sola vez, y el staff no gana', function () {
    $course = heroCourse();
    $student = studentWithRootOpen($course);

    app(StepCompleter::class)->complete($student, $course['step'], 'Hola');
    app(StepCompleter::class)->complete($student, $course['step'], 'Hola');
    expect(goldOf($student))->toBe(15);

    $admin = User::factory()->admin()->create();
    app(StepCompleter::class)->complete($admin, $course['step'], 'Hola');
    expect(goldOf($admin))->toBe(0);
});

test('el oro de las micro-misiones superadas antes de que existiera se acredita una vez al entrar', function () {
    $course = heroCourse();
    $student = studentWithRootOpen($course);
    NodeStepCompletion::create(['user_id' => $student->id, 'node_step_id' => $course['step']->id, 'completed_at' => now()]);

    expect(app(Heroes::class)->settleGold($student))->toBe(15)
        ->and(app(Heroes::class)->settleGold($student))->toBe(0)
        ->and(goldOf($student))->toBe(15)
        ->and(CoinTransaction::where('user_id', $student->id)->where('reason', CoinReason::StepCompleted)->count())->toBe(1);
});

test('tomar el control pide el aspecto y repartir 24 puntos, cada uno entre 4 y 12', function () {
    $course = heroCourse();
    $student = studentWithRootOpen($course);
    $heroes = app(Heroes::class);

    expect(fn () => $heroes->create($student, $course['course'], 1, ['strength' => 6, 'dexterity' => 6, 'intelligence' => 6, 'luck' => 5]))
        ->toThrow(InvalidArgumentException::class)
        ->and(fn () => $heroes->create($student, $course['course'], 1, ['strength' => 13, 'dexterity' => 4, 'intelligence' => 4, 'luck' => 3]))
        ->toThrow(InvalidArgumentException::class)
        ->and(fn () => $heroes->create($student, $course['course'], 7, ['strength' => 6, 'dexterity' => 6, 'intelligence' => 6, 'luck' => 6]))
        ->toThrow(InvalidArgumentException::class);

    $hero = $heroes->create($student, $course['course'], 3, ['strength' => 4, 'dexterity' => 4, 'intelligence' => 12, 'luck' => 4]);
    expect($hero->hp())->toBe(90)->and($hero->mp())->toBe(80)
        ->and(fn () => $heroes->create($student, $course['course'], 1, ['strength' => 6, 'dexterity' => 6, 'intelligence' => 6, 'luck' => 6]))
        ->toThrow(InvalidArgumentException::class);
});

test('un atributo se sube con oro (100 × el valor actual) y sin oro no se sube', function () {
    $course = heroCourse();
    $student = studentWithRootOpen($course);
    $heroes = app(Heroes::class);
    $hero = $heroes->create($student, $course['course'], 1, ['strength' => 6, 'dexterity' => 6, 'intelligence' => 6, 'luck' => 6]);

    expect(fn () => $heroes->upgrade($hero, 'strength'))->toThrow(InsufficientFunds::class);
    expect($hero->fresh()->strength)->toBe(6);

    app(Ledger::class)->credit($student, Currency::gold(), 650, CoinReason::ManualAdjustment);
    $heroes->upgrade($hero, 'strength');

    expect($hero->fresh()->strength)->toBe(7)->and(goldOf($student))->toBe(50);
});

test('desde el panel: tomar el control, cambiar el aspecto gratis y subir un atributo', function () {
    $course = heroCourse();
    $student = studentWithRootOpen($course);
    app(Ledger::class)->credit($student, Currency::gold(), 1000, CoinReason::ManualAdjustment);

    Livewire::actingAs($student)->test(HeroPage::class, ['course' => $course['course']])
        ->assertSee('Tomá el control de Mia')
        ->call('changeLook', 4)
        ->set('stats', ['strength' => 12, 'dexterity' => 4, 'intelligence' => 4, 'luck' => 4])
        ->call('takeControl')
        ->assertHasNoErrors()
        ->assertSee('Lectora de Runas', false)
        ->call('changeLook', 2)
        ->call('upgrade', 'luck');

    $hero = Hero::where('user_id', $student->id)->first();
    expect($hero->look)->toBe(2)->and($hero->strength)->toBe(12)->and($hero->luck)->toBe(5)
        ->and(goldOf($student))->toBe(600);
});

test('el panel pide poder ver el curso, y un curso sin protagonista no tiene héroe', function () {
    $course = heroCourse();
    $stranger = User::factory()->create();
    $course['course']->update(['is_published' => false]);

    Livewire::actingAs($stranger)->test(HeroPage::class, ['course' => $course['course']])->assertForbidden();

    $other = makeCourse(['language' => 'sql']);
    $student = studentWithRootOpen($other);
    Livewire::actingAs($student)->test(HeroPage::class, ['course' => $other['course']])->assertNotFound();
});

test('con el abono recién aprobado (sin la Clase 0 abierta) ya puede tomar el control', function () {
    $course = heroCourse();
    $student = enrolledStudent($course['course']);

    Livewire::actingAs($student)->test(HeroPage::class, ['course' => $course['course']])->assertOk()->assertSee('Tomá el control de Mia');
});

test('reacomodar los puntos es gratis hasta comprar uno con oro', function () {
    $course = heroCourse();
    $student = studentWithRootOpen($course);
    $heroes = app(Heroes::class);
    $hero = $heroes->create($student, $course['course'], 1, ['strength' => 6, 'dexterity' => 6, 'intelligence' => 6, 'luck' => 6]);

    $heroes->redistribute($hero, ['strength' => 4, 'dexterity' => 4, 'intelligence' => 12, 'luck' => 4]);
    expect($hero->fresh()->intelligence)->toBe(12);

    app(Ledger::class)->credit($student, Currency::gold(), 400, CoinReason::ManualAdjustment);
    $heroes->upgrade($hero->fresh(), 'strength');

    expect($heroes->canRedistribute($hero))->toBeFalse()
        ->and(fn () => $heroes->redistribute($hero, ['strength' => 6, 'dexterity' => 6, 'intelligence' => 6, 'luck' => 6]))
        ->toThrow(InvalidArgumentException::class);
});

test('Mis héroes muestra el protagonista de cada mundo que puede jugar', function () {
    $course = heroCourse();
    $student = studentWithRootOpen($course);

    Livewire::actingAs($student)->test(HeroesPage::class)
        ->assertSee('Mia')
        ->assertSee('Tomá el control');
});

test('el grimorio muestra solo las cartas de las micro-misiones superadas', function () {
    $course = heroCourse();
    $student = studentWithRootOpen($course);

    Livewire::actingAs($student)->test(Grimoire::class)->assertSee('Todavía está en blanco', false)->assertDontSee('sep=');

    app(StepCompleter::class)->complete($student, $course['step'], 'Hola');

    Livewire::actingAs($student)->test(Grimoire::class)
        ->assertSee('print("texto")')
        ->assertSee('print(a, b, sep=" | ")')
        ->assertSee('1 de 1 cartas');
});

test('las páginas del juego responden y el menú las muestra', function () {
    $course = heroCourse();
    $student = studentWithRootOpen($course);

    $this->actingAs($student)->get(route('student.heroes'))->assertOk()->assertSee('data-test="menu-grimoire"', false);
    $this->actingAs($student)->get(route('student.hero', $course['course']))->assertOk();
    $this->actingAs($student)->get(route('student.grimoire'))->assertOk();
});

test('desde la ficha del alumno se reinicia el héroe y se le devuelve el oro de los atributos', function () {
    $course = heroCourse();
    $student = studentWithRootOpen($course);
    $heroes = app(Heroes::class);
    $hero = $heroes->create($student, $course['course'], 1, ['strength' => 6, 'dexterity' => 6, 'intelligence' => 6, 'luck' => 6]);
    app(Ledger::class)->credit($student, Currency::gold(), 700, CoinReason::ManualAdjustment);
    $heroes->upgrade($hero, 'luck');
    expect(goldOf($student))->toBe(100);

    Livewire::actingAs(User::factory()->admin()->create())->test(Show::class, ['user' => $student])
        ->assertSee('Protagonistas')
        ->call('resetHero', $hero->id);

    expect(Hero::where('user_id', $student->id)->exists())->toBeFalse()
        ->and(goldOf($student))->toBe(700);
});

test('el docente reinicia héroes solo de los alumnos de su comisión', function () {
    $course = heroCourse();
    $student = studentWithRootOpen($course);
    $hero = app(Heroes::class)->create($student, $course['course'], 1, ['strength' => 6, 'dexterity' => 6, 'intelligence' => 6, 'luck' => 6]);
    $teacher = User::factory()->teacher()->create();
    $cohort = $course['course']->cohorts()->create(['name' => 'Tarde', 'teacher_id' => $teacher->id]);
    $student->subscriptions()->update(['cohort_id' => $cohort->id]);
    $other = User::factory()->teacher()->create();

    expect($other->can('resetHero', [$student, $course['course']]))->toBeFalse()
        ->and($teacher->can('resetHero', [$student, $course['course']]))->toBeTrue();

    Livewire::actingAs($teacher)->test(Show::class, ['user' => $student])->call('resetHero', $hero->id);
    expect(Hero::whereKey($hero->id)->exists())->toBeFalse();
});
