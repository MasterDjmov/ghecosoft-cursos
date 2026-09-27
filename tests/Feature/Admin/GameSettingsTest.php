<?php

use App\Livewire\Admin\Badges;
use App\Livewire\Admin\Glossary;
use App\Livewire\Admin\Levels;
use App\Models\Badge;
use App\Models\GlossaryTerm;
use App\Models\Level;
use App\Models\User;
use Database\Seeders\LevelSeeder;
use Livewire\Livewire;

beforeEach(function () {
    $this->actingAs(User::factory()->admin()->create());
});

test('un término del curso reemplaza al general y se puede restaurar', function () {
    ['course' => $course] = makeCourse();

    Livewire::test(Glossary::class)
        ->set('scope', (string) $course->id)
        ->call('edit', 'coin.course')
        ->assertSet('singular', 'moneda')
        ->set('singular', 'escama')
        ->set('plural', 'escamas')
        ->set('gender', 'f')
        ->call('save')
        ->assertHasNoErrors();

    expect(term('coin.course', $course, 3))->toBe('escamas')
        ->and(term('coin.course', null, 3))->toBe('monedas');

    Livewire::test(Glossary::class)->set('scope', (string) $course->id)->call('revert', 'coin.course');

    expect(term('coin.course', $course, 3))->toBe('monedas');
});

test('clave propia y copiar del general a un curso', function () {
    ['course' => $course] = makeCourse();

    Livewire::test(Glossary::class)
        ->call('newKey')
        ->set('key', 'story.dragon_intro')
        ->set('singular', 'El dragón despierta')
        ->call('save')
        ->assertHasNoErrors();

    Livewire::test(Glossary::class)->call('newKey')->set('key', 'Con Espacios')->set('singular', 'x')->call('save')->assertHasErrors('key');

    Livewire::test(Glossary::class)->set('scope', (string) $course->id)->call('copyFromGeneral');

    expect(GlossaryTerm::where('course_id', $course->id)->where('key', 'story.dragon_intro')->exists())->toBeTrue();
});

test('los niveles guardan XP creciente y el nombre va al diccionario', function () {
    $this->seed(LevelSeeder::class);

    Livewire::test(Levels::class)
        ->set('rows.2.name', 'Aprendiz')
        ->set('rows.2.xp_required', 120)
        ->call('save')
        ->assertHasNoErrors();

    expect(Level::where('number', 2)->value('xp_required'))->toBe(120)
        ->and(Level::where('number', 2)->first()->name())->toBe('Aprendiz')
        ->and(Level::where('number', 3)->first()->name())->toBe('Nivel 3');

    Livewire::test(Levels::class)->set('rows.3.xp_required', 50)->call('save')->assertHasErrors('rows.3.xp_required');
});

test('agregar y quitar el último nivel', function () {
    $this->seed(LevelSeeder::class);
    $count = Level::count();

    Livewire::test(Levels::class)->call('add')->call('removeLast')->call('removeLast');

    expect(Level::count())->toBe($count - 1);
});

test('insignias: se crean y no se borra una que un alumno ganó', function () {
    Livewire::test(Badges::class)
        ->call('create')
        ->set('name', 'Cazador de slimes')
        ->assertSet('code', 'cazador_de_slimes')
        ->call('save')
        ->assertHasNoErrors();

    $badge = Badge::where('code', 'cazador_de_slimes')->firstOrFail();
    $badge->users()->attach(User::factory()->create(), ['awarded_at' => now()]);

    Livewire::test(Badges::class)->call('delete', $badge->id);

    expect(Badge::find($badge->id))->not->toBeNull();
});
