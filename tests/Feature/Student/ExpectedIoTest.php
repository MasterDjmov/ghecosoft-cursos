<?php

use App\Enums\PracticeEnvironment;
use App\Services\NodeUnlocker;

/** D73: «Cómo debería verse» (entrada de ejemplo + salida esperada) igual en todos los cursos. */
function practiceWithSample(string $language, PracticeEnvironment $environment): array
{
    $data = makeCourse(['language' => $language]);
    $student = enrolledStudent($data['course']);
    app(NodeUnlocker::class)->unlock($student, $data['root']);
    $practice = $data['root']->practices()->first();
    $practice->update([
        'environment' => $environment,
        'sample_input' => "ENTRADA-DE-EJEMPLO\n3",
        'expected_output' => 'SALIDA-ESPERADA',
    ]);

    return [...$data, 'student' => $student, 'practice' => $practice];
}

test('el indicio muestra la entrada y la salida, en la tarjeta del nodo y en el modo misión', function (string $language, PracticeEnvironment $environment) {
    ['course' => $course, 'root' => $root, 'student' => $student, 'practice' => $practice] = practiceWithSample($language, $environment);

    $this->actingAs($student)->get(route('student.node', [$course, $root]))
        ->assertOk()
        ->assertSeeInOrder(['Cómo debería verse', 'Entrada de ejemplo', 'ENTRADA-DE-EJEMPLO', 'Salida esperada', 'SALIDA-ESPERADA']);

    // En el modo misión, una sola vez y en la consigna (panel izquierdo), antes del editor.
    $mission = $this->actingAs($student)->get(route('student.mission', [$course, $root, $practice]))
        ->assertOk()
        ->assertSeeInOrder(['Cómo debería verse', 'Entrada de ejemplo', 'ENTRADA-DE-EJEMPLO', 'Salida esperada', 'SALIDA-ESPERADA', 'x-ref="editor"'], false)
        ->getContent();
    expect(substr_count($mission, 'data-test="expected-io"'))->toBe(1);
})->with([
    'Python en el navegador' => ['python', PracticeEnvironment::Browser],
    'C++ en la compu' => ['cpp', PracticeEnvironment::Local],
    'PHP en la compu' => ['php', PracticeEnvironment::Local],
]);

test('el indicio va cerrado de entrada y no aparece si la práctica no tiene ejemplo', function () {
    ['course' => $course, 'root' => $root, 'student' => $student, 'practice' => $practice] = practiceWithSample('cpp', PracticeEnvironment::Local);

    $html = $this->actingAs($student)->get(route('student.node', [$course, $root]))->getContent();
    expect($html)->toMatch('/<details[^>]*data-test="expected-io"/')
        ->and($html)->not->toMatch('/<details[^>]*open[^>]*data-test="expected-io"/');

    $practice->update(['sample_input' => null, 'expected_output' => null]);
    $this->actingAs($student)->get(route('student.node', [$course, $root]))->assertDontSee('Cómo debería verse');
});
