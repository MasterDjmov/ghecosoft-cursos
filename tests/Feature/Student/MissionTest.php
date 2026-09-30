<?php

use App\Livewire\Student\Mission;
use App\Models\Submission;
use App\Models\User;
use App\Services\NodeUnlocker;
use App\Services\SubmissionReviewer;
use App\Support\ReviewHours;
use Livewire\Livewire;

/** Modo misión: la misma práctica a pantalla completa, con las mismas reglas. */
function missionSetup(): array
{
    $data = makeCourse();
    $student = enrolledStudent($data['course']);
    app(NodeUnlocker::class)->unlock($student, $data['root']);
    $practice = $data['root']->practices()->first();
    $practice->update([
        'instructions' => 'Mostrá un saludo, {heroe}.',
        'approval_criteria' => 'Usa print.',
        'reference_solution' => 'print("SOLUCION-SECRETA")',
    ]);
    $data['root']->update(['chronicle' => 'El Valle te espera.']);

    return [...$data, 'student' => $student, 'practice' => $practice];
}

test('el nodo ofrece entrar a la misión y la misión muestra consigna, historia y misiones', function () {
    ['course' => $course, 'root' => $root, 'student' => $student, 'practice' => $practice] = missionSetup();

    $this->actingAs($student)->get(route('student.node', [$course, $root]))->assertSee('Entrar a la misión');

    $this->actingAs($student)->get(route('student.mission', [$course, $root, $practice]))
        ->assertOk()
        ->assertSee('Misión 1 · Primer programa')
        ->assertSee('Mostrá un saludo, Kira.')
        ->assertSee('Usa print.')
        ->assertSee('El Valle te espera.')
        ->assertSee('Misiones del nodo')
        ->assertDontSee('SOLUCION-SECRETA')
        ->assertDontSee('Devolución del profe'); // sin devolución, sin columna
});

test('no se entra a la misión de un nodo cerrado ni de una práctica de otro nodo', function () {
    ['course' => $course, 'root' => $root, 'topic1' => $topic1, 'student' => $student] = missionSetup();

    $this->actingAs($student)->get(route('student.mission', [$course, $topic1, $topic1->practices()->first()]))->assertForbidden();
    $this->actingAs($student)->get(route('student.mission', [$course, $root, $topic1->practices()->first()]))->assertNotFound();
});

test('desde la misión se entrega igual que desde el nodo', function () {
    ['course' => $course, 'root' => $root, 'student' => $student, 'practice' => $practice] = missionSetup();

    Livewire::actingAs($student)->test(Mission::class, ['course' => $course, 'node' => $root, 'practice' => $practice])
        ->call('submit', code: 'print("hola")');

    expect(Submission::where('user_id', $student->id)->where('practice_id', $practice->id)->value('code'))->toBe('print("hola")');
});

test('la devolución del profe aparece en su columna', function () {
    ['course' => $course, 'root' => $root, 'student' => $student, 'practice' => $practice] = missionSetup();
    $submission = Submission::create(['practice_id' => $practice->id, 'user_id' => $student->id, 'attempt' => 1, 'code' => 'print(1)', 'submitted_at' => now()]);
    app(SubmissionReviewer::class)->comment($submission, User::factory()->admin()->create(), 'Revisá el signo del elif.');

    $this->actingAs($student)->get(route('student.mission', [$course, $root, $practice]))
        ->assertOk()
        ->assertSee('Devolución del profe')
        ->assertSee('Revisá el signo del elif.');
});

test('cada práctica muestra cuántas veces se entregó, con su color', function () {
    ['course' => $course, 'root' => $root, 'student' => $student, 'practice' => $practice] = missionSetup();

    Livewire::actingAs($student)->test(Mission::class, ['course' => $course, 'node' => $root, 'practice' => $practice])
        ->assertDontSeeHtml('data-test="attempts"');

    foreach ([1, 2, 3, 4] as $attempt) {
        Submission::create(['practice_id' => $practice->id, 'user_id' => $student->id, 'attempt' => $attempt, 'code' => 'print(1)', 'submitted_at' => now()]);
    }
    Livewire::actingAs($student)->test(Mission::class, ['course' => $course, 'node' => $root, 'practice' => $practice])
        ->assertSeeHtml('data-attempts="4"')
        ->assertSeeHtml('color: #f87171');
    $this->actingAs($student)->get(route('student.node', [$course, $root]))->assertSee('4 intentos');
});

test('lo que se entrega fuera del horario de corrección avisa cuándo se revisa', function () {
    expect(ReviewHours::notice(Carbon\Carbon::parse('2026-10-01 10:00')))->toBeNull()
        ->and(ReviewHours::reviewDay(Carbon\Carbon::parse('2026-10-01 22:00'))->toDateString())->toBe('2026-10-02')
        ->and(ReviewHours::reviewDay(Carbon\Carbon::parse('2026-10-02 03:15'))->toDateString())->toBe('2026-10-02');

    ['course' => $course, 'root' => $root, 'student' => $student, 'practice' => $practice] = missionSetup();
    $this->travelTo(Carbon\Carbon::parse('2026-10-01 23:30'));

    Livewire::actingAs($student)->test(Mission::class, ['course' => $course, 'node' => $root, 'practice' => $practice])
        ->call('submit', 'print("hola")')
        ->assertSee('el profe la revisa mañana (02/10) entre las 8 y las 22 h')
        ->assertSeeHtml('data-test="review-notice"');

    $this->travelTo(Carbon\Carbon::parse('2026-10-02 10:00'));
    Livewire::actingAs($student)->test(Mission::class, ['course' => $course, 'node' => $root, 'practice' => $practice])
        ->assertSee('el profe la revisa hoy entre las 8 y las 22 h');
});
