<?php

use App\Enums\SubmissionMode;
use App\Livewire\Admin\Submissions\Index;
use App\Livewire\Admin\Submissions\Show;
use App\Models\Cohort;
use App\Models\User;
use App\Services\PracticeSubmitter;
use App\Support\SubmissionCases;
use Livewire\Livewire;

/** D73, etapa 4: las pruebas corren en el navegador de quien corrige; el servidor solo da los casos y guarda el resultado. */
beforeEach(function () {
    $this->data = makeCourse();
    $this->practice = $this->data['root']->practices()->first();
    $this->practice->update(['sample_input' => '15', 'expected_output' => '15']);
    $this->practice->tests()->createMany([
        ['position' => 1, 'name' => 'Cero', 'input' => '0', 'expected_output' => '0'],
        ['position' => 2, 'name' => 'Mucho oro', 'input' => '999', 'expected_output' => 'PRUEBA-SECRETA-999'],
    ]);
    $this->admin = User::factory()->admin()->create();
    $this->student = studentWithRootOpen($this->data);
    $this->submission = app(PracticeSubmitter::class)->submit($this->student, $this->practice, 'print(input())');
});

test('los casos de una entrega son el ejemplo y las pruebas, y no hay en las de archivo', function () {
    expect(SubmissionCases::for($this->submission->fresh()))->toBe([
        ['label' => 'Ejemplo', 'input' => '15', 'expected' => '15'],
        ['label' => 'Cero', 'input' => '0', 'expected' => '0'],
        ['label' => 'Mucho oro', 'input' => '999', 'expected' => 'PRUEBA-SECRETA-999'],
    ]);

    $this->practice->update(['submission_mode' => SubmissionMode::File]);
    expect(SubmissionCases::for($this->submission->fresh()))->toBe([]);
});

test('al abrir la entrega, quien corrige recibe los casos para correrlos y guarda el resultado si cuadra', function () {
    $this->actingAs($this->admin)->get(route('admin.submissions.show', $this->submission))
        ->assertOk()->assertSee('data-test="submission-cases"', false)->assertSee('PRUEBA-SECRETA-999');

    Livewire::actingAs($this->admin)->test(Show::class, ['submission' => $this->submission])->call('saveCheck', 2, 5);
    expect($this->submission->fresh()->check_result)->toBeNull();   // no son 5 casos

    Livewire::actingAs($this->admin)->test(Show::class, ['submission' => $this->submission])->call('saveCheck', 2, 3);
    expect($this->submission->fresh()->check_result)->toMatchArray(['passed' => 2, 'total' => 3]);
});

test('el alumno no ve las pruebas ni el resultado; un docente ajeno no recibe los casos ni guarda', function () {
    $this->actingAs($this->student)->get(route('student.node', [$this->data['course'], $this->data['root']]))
        ->assertOk()->assertDontSee('PRUEBA-SECRETA-999');

    $stranger = User::factory()->teacher()->create();
    Cohort::create(['course_id' => $this->data['course']->id, 'teacher_id' => $stranger->id, 'name' => 'Otra']);
    Livewire::actingAs($stranger)->test(Index::class)->call('casesFor', $this->submission->id)->assertForbidden();
    Livewire::actingAs($stranger)->test(Index::class)->call('saveCheck', $this->submission->id, 3, 3)->assertForbidden();
    expect($this->submission->fresh()->check_result)->toBeNull();
});

test('la bandeja ofrece probar las pendientes, muestra la marca y filtra por pruebas', function () {
    $other = app(PracticeSubmitter::class)->submit(studentWithRootOpen($this->data), $this->practice, 'print("hola")');

    Livewire::actingAs($this->admin)->test(Index::class)
        ->assertSee('data-test="check-pending"', false)
        ->assertSee('Probar pendientes (2)')
        ->call('casesFor', $this->submission->id)->assertReturned(fn ($data) => $data['language'] === 'python' && count($data['cases']) === 3);

    Livewire::actingAs($this->admin)->test(Index::class)->call('saveCheck', $this->submission->id, 3, 3)->call('saveCheck', $other->id, 1, 3);

    Livewire::actingAs($this->admin)->test(Index::class)
        ->assertSee('data-test="check-'.$this->submission->id.'"', false)->assertSee('3/3')->assertSee('1/3')
        ->assertDontSee('data-test="check-pending"', false)
        ->set('checks', 'pass')->assertSee('data-test="check-'.$this->submission->id.'"', false)->assertDontSee('data-test="check-'.$other->id.'"', false)
        ->set('checks', 'fail')->assertSee('data-test="check-'.$other->id.'"', false)->assertDontSee('data-test="check-'.$this->submission->id.'"', false)
        ->set('checks', 'none')->assertSee('¡No hay nada para corregir!');
});
