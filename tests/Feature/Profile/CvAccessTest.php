<?php

use App\Livewire\Settings\Privacy;
use App\Models\User;
use App\Services\NodeUnlocker;
use Illuminate\Support\Facades\DB;
use Livewire\Livewire;

beforeEach(function () {
    $this->student = User::factory()->create(['name' => 'Valentina', 'last_name' => 'Ríos', 'username' => 'valen', 'birth_date' => '2000-01-01']);
    $this->student->forceFill(['cv_public' => true])->save();
});

test('el CV tiene su propio link, que no revela el usuario de login', function () {
    expect($this->student->cv_slug)->toStartWith('valentina-rios-')->not->toContain('valen-');

    $this->get('/cv/valen')->assertNotFound();
    $this->get(route('cv.show', $this->student->cv_slug))->assertOk()->assertSee('Valentina Ríos')->assertDontSee('valen"');
});

test('un link nuevo deja sin efecto el anterior', function () {
    $old = $this->student->cv_slug;

    Livewire::actingAs($this->student)->test(Privacy::class)->call('newCvLink');

    $this->get(route('cv.show', $old))->assertNotFound();
    $this->get(route('cv.show', $this->student->fresh()->cv_slug))->assertOk();
});

test('con código activado, hay que ponerlo para ver el CV', function () {
    Livewire::actingAs($this->student)->test(Privacy::class)->call('toggleCvCode')->assertSee($this->student->fresh()->cv_code);
    $student = $this->student->fresh();
    $url = route('cv.show', $student->cv_slug);
    auth()->logout();

    $this->get($url)->assertOk()->assertSee('Este CV pide un código')->assertDontSee('Valentina Ríos');

    $this->from($url)->post(route('cv.unlock', $student->cv_slug), ['code' => $student->cv_code === '000000' ? '111111' : '000000'])
        ->assertRedirect($url)->assertSessionHasErrors('code');

    $this->from($url)->post(route('cv.unlock', $student->cv_slug), ['code' => $student->cv_code])->assertRedirect($url);
    $this->get($url)->assertOk()->assertSee('Valentina Ríos');
});

test('un código nuevo le quita el acceso a quien usó el anterior', function () {
    Livewire::actingAs($this->student)->test(Privacy::class)->call('toggleCvCode');
    $student = $this->student->fresh();
    $url = route('cv.show', $student->cv_slug);
    auth()->logout();
    $this->post(route('cv.unlock', $student->cv_slug), ['code' => $student->cv_code]);
    $this->get($url)->assertSee('Valentina Ríos');

    auth()->logout();
    Livewire::actingAs($student)->test(Privacy::class)->call('newCvCode');
    auth()->logout();

    $this->get($url)->assertSee('Este CV pide un código');
});

test('después de 5 códigos mal desde la misma compu, se frena aunque el sexto sea correcto', function () {
    $this->student->forceFill(['cv_code' => '482913'])->save();
    $slug = $this->student->cv_slug;

    foreach (['111111', '222222', '333333', '444444', '555555'] as $wrong) {
        $this->post(route('cv.unlock', $slug), ['code' => $wrong]);
    }

    $this->post(route('cv.unlock', $slug), ['code' => '482913'])->assertSessionHasErrors('code');
    $this->get(route('cv.show', $slug))->assertSee('Demasiados intentos');
});

test('el dueño y el docente lo ven sin código; el código no se muestra en el CV', function () {
    $this->student->forceFill(['cv_code' => '482913'])->save();
    $url = route('cv.show', $this->student->cv_slug);

    $this->actingAs($this->student)->get($url)->assertOk()->assertSee('Valentina Ríos')->assertDontSee('482913');
    $this->actingAs(User::factory()->admin()->create())->get($url)->assertOk()->assertSee('Valentina Ríos');
});

test('el código se guarda cifrado en la base', function () {
    $this->student->forceFill(['cv_code' => '482913'])->save();

    expect(DB::table('users')->where('id', $this->student->id)->value('cv_code'))->not->toBe('482913')
        ->and($this->student->toArray())->not->toHaveKey('cv_code');
});

test('en el CV cada curso es un acordeón con su árbol, que se ve solo para mirar', function () {
    ['course' => $course, 'root' => $root, 'topic1' => $topic1] = makeCourse();
    enrolledStudent($course, $this->student);
    app(NodeUnlocker::class)->unlock($this->student, $root);

    $this->get(route('cv.show', $this->student->cv_slug))
        ->assertOk()
        ->assertSee('data-test="cv-course"', false)
        ->assertSee(route('cv.tree', [$this->student->cv_slug, $course]), false);

    $this->get(route('cv.tree', [$this->student->cv_slug, $course]))
        ->assertOk()
        ->assertSee('Árbol de Valentina Ríos')
        ->assertSee('Clase 0')
        ->assertDontSee('/nodos/', false)
        ->assertDontSee('Misión 1');
});

test('el árbol del CV respeta las reglas del CV y solo muestra cursos empezados', function () {
    ['course' => $course, 'root' => $root] = makeCourse();
    ['course' => $other] = makeCourse();
    enrolledStudent($course, $this->student);
    app(NodeUnlocker::class)->unlock($this->student, $root);

    $this->get(route('cv.tree', [$this->student->cv_slug, $other]))->assertNotFound();

    $this->student->forceFill(['cv_code' => '123456'])->save();
    $this->get(route('cv.tree', [$this->student->cv_slug, $course]))->assertRedirect(route('cv.show', $this->student->cv_slug));

    $this->student->forceFill(['cv_public' => false, 'cv_code' => null])->save();
    $this->get(route('cv.tree', [$this->student->cv_slug, $course]))->assertNotFound();
});
