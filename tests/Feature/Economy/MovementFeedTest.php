<?php

use App\Livewire\MovementFeed;
use App\Models\Submission;
use App\Models\User;
use App\Services\NodeUnlocker;
use App\Services\SubmissionReviewer;
use Livewire\Livewire;

beforeEach(function () {
    $this->python = makeCourse(['title' => 'Python']);
    $this->c = makeCourse(['title' => 'Lenguaje C', 'slug' => 'c-paralelo']);
    $this->student = enrolledStudent($this->python['course']);
    enrolledStudent($this->c['course'], $this->student);
    $this->admin = User::factory()->admin()->create();

    app(NodeUnlocker::class)->unlock($this->student, $this->python['root']);
    $practice = $this->python['root']->practices()->first();
    $submission = Submission::create(['practice_id' => $practice->id, 'user_id' => $this->student->id, 'attempt' => 1, 'submitted_at' => now()]);
    app(SubmissionReviewer::class)->approve($submission, $this->admin);
});

test('los movimientos se separan por curso y dicen qué práctica y qué nodo', function () {
    $component = Livewire::actingAs($this->student)->test(MovementFeed::class, ['user' => $this->student]);

    // Todos: la práctica aprobada con sus monedas y su XP juntas, y el curso de cada hecho.
    $component->assertSee('Práctica aprobada: «Primer programa»')
        ->assertSee('Misión de «Clase 0»')
        ->assertSee('Abriste «Clase 0»')
        ->assertSee('Python')
        ->assertSee('Lenguaje C');

    // Solo C: la inscripción, nada de Python.
    $component->call('selectCourse', 'c-paralelo')
        ->assertSee('Movimientos en Lenguaje C')
        ->assertSee('Inscripción aprobada')
        ->assertDontSee('Primer programa')
        ->assertSet('course', 'c-paralelo');
});

test('un alumno no ve los movimientos de otro; el docente sí, con quién los hizo', function () {
    $other = User::factory()->create();

    Livewire::actingAs($other)->test(MovementFeed::class, ['user' => $this->student])->assertForbidden();

    Livewire::actingAs($this->admin)->test(MovementFeed::class, ['user' => $this->student, 'showAuthor' => true])
        ->assertOk()
        ->assertSee('por '.$this->admin->name);
});

test('la página de Mi cuenta muestra los movimientos', function () {
    $this->actingAs($this->student)->get(route('movements'))->assertOk()->assertSee('Primer programa');
});
