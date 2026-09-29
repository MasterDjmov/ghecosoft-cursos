<?php

use App\Enums\NodeType;
use App\Livewire\Admin\Courses\Form;
use App\Livewire\Admin\Courses\Index;
use App\Models\Course;
use App\Models\Currency;
use App\Models\User;
use Livewire\Livewire;

beforeEach(function () {
    $this->admin = User::factory()->admin()->create();
    $this->actingAs($this->admin);
});

test('las pantallas del docente cargan', function () {
    ['course' => $course, 'topic1' => $topic1] = makeCourse();

    foreach ([
        route('admin.courses.index'), route('admin.courses.create'), route('admin.courses.edit', $course),
        route('admin.courses.tree', $course), route('admin.nodes.edit', [$course, $topic1]),
        route('admin.glossary'), route('admin.levels'), route('admin.badges'),
    ] as $url) {
        $this->get($url)->assertOk();
    }
});

test('un alumno no entra a ninguna pantalla del editor', function () {
    ['course' => $course, 'topic1' => $topic1] = makeCourse();
    $this->actingAs(User::factory()->create());

    foreach ([
        route('admin.courses.index'), route('admin.courses.tree', $course), route('admin.nodes.edit', [$course, $topic1]),
        route('admin.glossary'), route('admin.levels'), route('admin.badges'),
    ] as $url) {
        $this->get($url)->assertRedirect(route('home'));
    }
});

test('un nodo de otro curso da 404 en el editor', function () {
    ['course' => $course] = makeCourse();
    ['topic1' => $foreign] = makeCourse();

    $this->get(route('admin.nodes.edit', [$course, $foreign]))->assertNotFound();
});

test('crear un curso le crea su moneda y su nodo raíz con el precio del raíz', function () {
    Livewire::test(Form::class)
        ->set('title', 'C desde cero')
        ->assertSet('slug', 'c-desde-cero')
        ->set('language', 'c')
        ->set('root_price', 12)
        ->set('subscription_days', 45)
        ->call('save')
        ->assertHasNoErrors()
        ->assertRedirect(route('admin.courses.tree', 'c-desde-cero'));

    $course = Course::where('slug', 'c-desde-cero')->firstOrFail();

    expect($course->subscription_days)->toBe(45)
        ->and(Currency::where('course_id', $course->id)->exists())->toBeTrue()
        ->and($course->rootNode->type)->toBe(NodeType::Root)
        ->and($course->rootNode->price)->toBe(12);
});

test('cambiar el precio del raíz actualiza el precio del nodo raíz', function () {
    ['course' => $course, 'root' => $root] = makeCourse();

    Livewire::test(Form::class, ['course' => $course])
        ->set('root_price', 15)
        ->call('save')
        ->assertHasNoErrors();

    expect($root->fresh()->price)->toBe(15);
});

test('la dirección del curso es única y con formato de link', function () {
    ['course' => $course] = makeCourse();

    Livewire::test(Form::class)->set('title', 'Otro')->set('slug', $course->slug)->call('save')->assertHasErrors('slug');
    Livewire::test(Form::class)->set('title', 'Otro')->set('slug', 'Con Espacios')->call('save')->assertHasErrors(['slug' => 'regex']);
});

test('no se borra un curso que ya tiene alumnos', function () {
    ['course' => $course] = makeCourse();
    enrolledStudent($course);

    Livewire::test(Form::class, ['course' => $course])->call('delete');

    expect($course->fresh())->not->toBeNull();
});

test('un curso sin alumnos se borra entero', function () {
    ['course' => $course] = makeCourse();

    Livewire::test(Form::class, ['course' => $course])->call('delete')->assertRedirect(route('admin.courses.index'));

    expect(Course::find($course->id))->toBeNull();
});

test('publicar y ordenar cursos desde el listado', function () {
    ['course' => $a] = makeCourse(['is_published' => false]);
    ['course' => $b] = makeCourse();

    Livewire::test(Index::class)
        ->call('togglePublished', $a->id)
        ->call('sort', $b->id, 0);

    expect($a->fresh()->is_published)->toBeTrue()
        ->and($b->fresh()->position)->toBe(1)
        ->and($a->fresh()->position)->toBe(2);
});
