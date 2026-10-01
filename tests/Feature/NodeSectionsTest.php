<?php

use App\Enums\PracticeEnvironment;
use App\Livewire\Admin\Nodes\Edit;
use App\Models\Submission;
use App\Models\User;
use App\Services\NodeUnlocker;
use Livewire\Livewire;

/** D37: el nodo por secciones y los campos nuevos de la práctica. Las soluciones nunca llegan al alumno. */
function nodeWithSections(): array
{
    $data = makeCourse();
    $data['root']->update([
        'chronicle' => 'Cruzás el portal y Ofidia te espera.',
        'objectives' => '- Mostrar texto con print()',
        'before_you_start' => 'Nada: es el primer paso.',
        'content' => '## Explicación del print',
        'use_cases' => 'Mostrar resultados en cualquier programa.',
        'common_errors' => 'Olvidar cerrar el paréntesis.',
        'beast_key' => 'beast.slime',
        'self_check' => [['question' => '¿Qué muestra print(1 + 1)?', 'answer' => '2']],
        'teacher_solutions' => 'SOLUCION-SECRETA-DEL-NODO',
    ]);
    $data['practice'] = $data['root']->practices()->first();
    $data['practice']->update([
        'approval_criteria' => 'Usa print dos veces.',
        'expected_output' => 'Hola',
        'environment' => PracticeEnvironment::Local,
        'reference_solution' => 'SOLUCION-SECRETA-DE-LA-HOJA',
    ]);

    return $data;
}

test('el alumno ve las secciones con su personaje, la criatura y la prueba del sello', function () {
    ['course' => $course, 'root' => $root] = nodeWithSections();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $root);

    $this->actingAs($student)->get(route('student.node', [$course, $root]))
        ->assertOk()
        ->assertSeeInOrder(['Crónica', 'Cruzás el portal', 'Al terminar, vas a poder', 'Explicación', 'Mia', '¿Para qué sirve?', 'Bron', 'Errores habituales', 'Zed', 'Slime'])
        ->assertSee('Prueba del sello')
        ->assertSee('¿Qué muestra print(1 + 1)?')
        ->assertSee('Para aprobar')
        ->assertSee('Usa print dos veces.')
        ->assertSee('Local');
});

test('las soluciones del docente nunca llegan al alumno', function () {
    ['course' => $course, 'root' => $root, 'practice' => $practice] = nodeWithSections();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $root);

    $this->actingAs($student)->get(route('student.node', [$course, $root]))
        ->assertOk()
        ->assertDontSee('SOLUCION-SECRETA-DEL-NODO')
        ->assertDontSee('SOLUCION-SECRETA-DE-LA-HOJA');

    // Tampoco se escapan si un modelo se pasa a array o JSON.
    expect(json_encode($root->fresh()))->not->toContain('SOLUCION-SECRETA')
        ->and(json_encode($practice->fresh()))->not->toContain('SOLUCION-SECRETA');
});

test('al corregir, el docente ve el criterio y la solución de referencia', function () {
    ['course' => $course, 'root' => $root, 'practice' => $practice] = nodeWithSections();
    $student = enrolledStudent($course);
    $submission = Submission::create(['practice_id' => $practice->id, 'user_id' => $student->id, 'attempt' => 1, 'code' => 'print("Hola")', 'submitted_at' => now()]);

    $this->actingAs(User::factory()->admin()->create())
        ->get(route('admin.submissions.show', $submission))
        ->assertOk()
        ->assertSee('Criterio de aprobación')
        ->assertSee('Usa print dos veces.')
        ->assertSee('SOLUCION-SECRETA-DE-LA-HOJA');
});

test('el editor guarda las secciones, la prueba del sello sin filas vacías y las soluciones', function () {
    ['course' => $course, 'topic1' => $topic1] = makeCourse();
    $this->actingAs(User::factory()->admin()->create());

    Livewire::test(Edit::class, ['course' => $course, 'node' => $topic1])
        ->set('chronicle', 'Llegás a la posada.')
        ->set('objectives', '- Usar variables')
        ->set('use_cases', 'Guardar el total de una compra.')
        ->set('common_errors', 'NameError')
        ->set('beast_key', 'beast.skeleton')
        ->call('addSelfCheck')
        ->set('selfCheck.0.question', '¿Cuánto vale x?')
        ->set('selfCheck.0.answer', '3')
        ->call('addSelfCheck')
        ->set('teacher_solutions', 'x = 3')
        ->call('save')
        ->assertHasNoErrors();

    $topic1->refresh();
    expect($topic1->chronicle)->toBe('Llegás a la posada.')
        ->and($topic1->beast_key)->toBe('beast.skeleton')
        ->and($topic1->self_check)->toBe([['question' => '¿Cuánto vale x?', 'answer' => '3']])
        ->and($topic1->teacher_solutions)->toBe('x = 3');
});

test('el editor rechaza una criatura que no es del bestiario', function () {
    ['course' => $course, 'topic1' => $topic1] = makeCourse();
    $this->actingAs(User::factory()->admin()->create());

    Livewire::test(Edit::class, ['course' => $course, 'node' => $topic1])
        ->set('beast_key', 'coin.course')
        ->call('save')
        ->assertHasErrors('beast_key');
});

test('la hoja guarda criterio, entorno, salida esperada y solución', function () {
    ['course' => $course, 'topic1' => $topic1] = makeCourse();
    $this->actingAs(User::factory()->admin()->create());
    $practice = $topic1->practices()->first();

    Livewire::test(Edit::class, ['course' => $course, 'node' => $topic1])
        ->call('editPractice', $practice->id)
        ->set('practiceCriteria', 'Lee el nombre.')
        ->set('practiceEnvironment', 'local')
        ->set('practiceMode', 'file')
        ->set('practiceExpectedOutput', 'Hola, Kira')
        ->set('practiceSolution', 'print("Hola")')
        ->call('savePractice')
        ->assertHasNoErrors();

    $practice->refresh();
    expect($practice->approval_criteria)->toBe('Lee el nombre.')
        ->and($practice->environment)->toBe(PracticeEnvironment::Local)
        ->and($practice->expected_output)->toBe('Hola, Kira')
        ->and($practice->reference_solution)->toBe('print("Hola")');
});

test('cada nodo ofrece volver al curso en árbol o en lista', function () {
    ['course' => $course, 'root' => $root] = nodeWithSections();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $root);

    $this->actingAs($student)->get(route('student.node', [$course, $root]))
        ->assertOk()
        ->assertSee('data-test="node-tree-links"', false)
        ->assertSee(route('student.tree', $course).'#arbol', false)
        ->assertSee(route('student.tree', $course).'#lista', false);
});
