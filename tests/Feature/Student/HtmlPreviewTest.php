<?php

use App\Enums\Language;
use App\Livewire\Admin\Submissions\Show;
use App\Models\User;
use App\Services\PracticeSubmitter;

/*
 * HTML y CSS (D76): el alumno ve su página dibujada en una caja aislada (iframe sandbox="", sin JavaScript,
 * formularios ni red), en el ejemplo del nodo, en la práctica y en el modo misión. Nada corre en el servidor.
 */

function htmlCourse(): array
{
    $made = makeCourse(['language' => 'html']);
    $made['root']->update(['example_code' => '<!DOCTYPE html><html><head></head><body><h1>Hola</h1></body></html>', 'example_runnable' => true]);

    return [...$made, 'student' => studentWithRootOpen($made), 'practice' => $made['root']->practices()->first()];
}

test('solo Python y HTML corren para los alumnos', function () {
    expect(Language::Html->runsForStudents())->toBeTrue()
        ->and(Language::Python->runsForStudents())->toBeTrue()
        ->and(Language::Cpp->runsForStudents())->toBeFalse()
        ->and(Language::Php->runsForStudents())->toBeFalse()
        ->and(Language::Html->extension())->toBe('html')
        ->and(Language::Html->label())->toBe('HTML y CSS');
});

test('en un curso de HTML, el alumno ve su página en la caja aislada y no la consola', function () {
    ['course' => $course, 'root' => $root, 'student' => $student, 'practice' => $practice] = htmlCourse();

    $node = $this->actingAs($student)->get(route('student.node', [$course, $root]))->assertOk()->getContent();
    expect($node)->toContain('data-test="html-preview"')
        ->and($node)->toContain('sandbox=""')
        ->and($node)->not->toContain('Entrada (stdin)');

    $this->actingAs($student)->get(route('student.mission', [$course, $root, $practice]))
        ->assertOk()
        ->assertSee('data-test="html-preview"', false)
        ->assertSee('practica_1.html');
});

test('la caja nunca recibe permisos: el iframe no lleva allow-scripts, allow-forms ni allow-same-origin', function () {
    $html = view('components.html-preview')->render();

    expect($html)->toMatch('/<iframe\b[^>]*\ssandbox=""\s/')
        ->and($html)->not->toContain('allow-scripts')
        ->and($html)->not->toContain('allow-same-origin')
        ->and($html)->not->toContain('allow-forms');
});

test('en Python sigue la consola de siempre', function () {
    $made = makeCourse();
    $made['root']->update(['example_code' => 'print(1)', 'example_runnable' => true]);
    $student = studentWithRootOpen($made);

    $this->actingAs($student)->get(route('student.node', [$made['course'], $made['root']]))
        ->assertOk()
        ->assertDontSee('data-test="html-preview"', false)
        ->assertSee('Entrada (stdin)');
});

test('el docente también ve la página dibujada al corregir', function () {
    ['practice' => $practice, 'student' => $student] = htmlCourse();
    $submission = app(PracticeSubmitter::class)->submit($student, $practice, '<p>Mi vitral</p>');

    Livewire\Livewire::actingAs(User::factory()->admin()->create())
        ->test(Show::class, ['submission' => $submission])
        ->assertSee('data-test="html-preview"', false);
});
