<?php

use App\Enums\CoinReason;
use App\Livewire\Admin\Students\Tree as StudentTree;
use App\Livewire\Student\CourseRestart;
use App\Models\Currency;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\NodeUnlock;
use App\Models\Submission;
use App\Models\User;
use App\Notifications\PlatformNotification;
use App\Services\CourseRestarter;
use App\Services\Heroes;
use App\Services\Ledger;
use App\Services\NodeUnlocker;
use App\Services\StepCompleter;
use App\Services\StudentAccounts;
use App\Services\TreeAccess;
use Illuminate\Support\Facades\Notification;
use Livewire\Livewire;

// D117: cada uno reinicia su propio progreso en un curso, sin tocar los otros.

function restartStep($node, int $position = 1): NodeStep
{
    return NodeStep::create([
        'node_id' => $node->id, 'code' => "T{$node->id}-P{$position}", 'position' => $position, 'title' => "Paso {$position}", 'expected_output' => 'hola',
        'xp_reward' => 7, 'gold_reward' => 5,
    ]);
}

test('toda tabla con datos del alumno tiene decidido qué pasa al reiniciar un curso', function () {
    expect(array_values(array_diff(array_keys(StudentAccounts::RESET), CourseRestarter::WIPED, CourseRestarter::KEPT)))->toBe([]);
});

test('reiniciar borra el progreso del curso, deja el abono y las monedas de inscripción, y no toca el otro curso', function () {
    $made = makeCourse();
    $other = makeCourse(['title' => 'Otro']);
    $student = studentWithRootOpen($made);
    enrolledStudent($other['course'], $student);
    app(NodeUnlocker::class)->unlock($student, $other['root']);

    $step = restartStep($made['root']);
    $otherStep = restartStep($other['root']);
    app(StepCompleter::class)->complete($student, $step, 'hola');
    app(StepCompleter::class)->complete($student, $otherStep, 'hola');
    $submission = Submission::create(['practice_id' => $made['root']->practices()->first()->id, 'user_id' => $student->id, 'attempt' => 1, 'submitted_at' => now()]);

    $ledger = app(Ledger::class);
    $otherXp = (int) $student->xpTransactions()->where('course_id', $other['course']->id)->sum('amount');
    expect($otherXp)->toBeGreaterThan(0);

    app(CourseRestarter::class)->restart($student, $made['course']);
    $student->refresh();

    // Este curso: de cero, con el abono y lo justo para abrir el raíz.
    expect(NodeUnlock::where('user_id', $student->id)->where('node_id', $made['root']->id)->exists())->toBeFalse()
        ->and(NodeStepCompletion::where('user_id', $student->id)->where('node_step_id', $step->id)->exists())->toBeFalse()
        ->and(Submission::whereKey($submission->id)->exists())->toBeFalse()
        ->and(app(TreeAccess::class)->hasActiveSubscription($student, $made['course']))->toBeTrue()
        ->and($ledger->balance($student, Currency::forCourse($made['course'])))->toBe($made['course']->root_price);

    // El otro curso, intacto; la XP total es solo la de ese curso.
    expect(NodeUnlock::where('user_id', $student->id)->where('node_id', $other['root']->id)->exists())->toBeTrue()
        ->and(NodeStepCompletion::where('user_id', $student->id)->where('node_step_id', $otherStep->id)->exists())->toBeTrue()
        ->and((int) $student->xp_total)->toBe((int) $student->xpTransactions()->sum('amount'))
        ->and((int) $student->xpTransactions()->sum('amount'))->toBe($otherXp);

    // Puede volver a abrir el raíz.
    app(NodeUnlocker::class)->unlock($student, $made['root']);
    expect(app(TreeAccess::class)->isRootOpen($student, $made['course']))->toBeTrue();
});

test('el oro ganado queda y no se vuelve a pagar: reiniciar no sirve para juntar oro', function () {
    config(['game.gold_enabled' => true]);
    $made = makeCourse();
    $student = studentWithRootOpen($made);
    $step = restartStep($made['root']);
    app(StepCompleter::class)->complete($student, $step, 'hola');
    $gold = app(Heroes::class)->gold($student);
    expect($gold)->toBe(5);

    app(CourseRestarter::class)->restart($student, $made['course']);
    expect(app(Heroes::class)->gold($student))->toBe($gold);

    app(NodeUnlocker::class)->unlock($student, $made['root']);
    app(StepCompleter::class)->complete($student, $step, 'hola');
    expect(app(Heroes::class)->gold($student))->toBe($gold)
        ->and((int) $student->fresh()->xp_total)->toBeGreaterThan(0);
});

test('los comodines ganados y gastados en el curso se van, y los de otro curso quedan', function () {
    $made = makeCourse();
    $other = makeCourse(['title' => 'Otro']);
    $student = studentWithRootOpen($made);
    $wildcard = Currency::wildcard();
    $ledger = app(Ledger::class);
    $ledger->credit($student, $wildcard, 2, CoinReason::PracticeApproved, null, $made['course']);
    $ledger->credit($student, $wildcard, 1, CoinReason::PracticeApproved, null, $other['course']);

    app(CourseRestarter::class)->restart($student, $made['course']);

    expect($ledger->balance($student, $wildcard))->toBe(1);
});

test('hay que escribir REINICIAR, y solo se borra lo de quien lo pide', function () {
    $made = makeCourse();
    $student = studentWithRootOpen($made);
    $classmate = studentWithRootOpen($made);

    Livewire::actingAs($student)->test(CourseRestart::class, ['course' => $made['course']])
        ->set('confirmation', 'dale')->call('restart')->assertHasErrors('confirmation');
    expect(app(TreeAccess::class)->isRootOpen($student, $made['course']))->toBeTrue();

    Livewire::actingAs($student)->test(CourseRestart::class, ['course' => $made['course']])
        ->set('confirmation', ' reiniciar ')->call('restart')->assertRedirect(route('student.tree', $made['course']));
    expect(app(TreeAccess::class)->isRootOpen($student, $made['course']))->toBeFalse()
        ->and(app(TreeAccess::class)->isRootOpen($classmate, $made['course']))->toBeTrue();
});

test('el administrador reinicia lo suyo sin abono; un alumno sin abono vigente no puede', function () {
    $made = makeCourse();
    $admin = User::factory()->admin()->create();
    $step = restartStep($made['root']);
    NodeStepCompletion::create(['user_id' => $admin->id, 'node_step_id' => $step->id, 'completed_at' => now()]);

    Livewire::actingAs($admin)->test(CourseRestart::class, ['course' => $made['course']])
        ->set('confirmation', 'REINICIAR')->call('restart')->assertRedirect();
    expect(NodeStepCompletion::where('user_id', $admin->id)->exists())->toBeFalse();

    $stranger = User::factory()->create();
    Livewire::actingAs($stranger)->test(CourseRestart::class, ['course' => $made['course']])
        ->set('confirmation', 'REINICIAR')->call('restart')->assertForbidden();

    $expired = studentWithRootOpen($made);
    $expired->subscriptions()->update(['ends_at' => now()->subDay()]);
    Livewire::actingAs($expired)->test(CourseRestart::class, ['course' => $made['course']])
        ->set('confirmation', 'REINICIAR')->call('restart')->assertForbidden();
    expect(app(TreeAccess::class)->isRootOpen($expired, $made['course']))->toBeTrue();
});

test('el botón aparece en el árbol del alumno', function () {
    $made = makeCourse();
    $student = studentWithRootOpen($made);

    $this->actingAs($student)->get(route('student.tree', $made['course']))
        ->assertOk()->assertSee('data-test="course-restart"', false)->assertSee('Reiniciar este curso');
});

test('el administrador le reinicia el curso a un alumno desde su árbol, con confirmación y aviso', function () {
    Notification::fake();
    $made = makeCourse();
    $other = makeCourse(['title' => 'Otro']);
    $student = studentWithRootOpen($made);
    enrolledStudent($other['course'], $student);
    app(NodeUnlocker::class)->unlock($student, $other['root']);
    $admin = User::factory()->admin()->create();

    $this->actingAs($admin)->get(route('admin.students.tree', [$student, $made['course']]))
        ->assertOk()->assertSee('data-test="student-course-restart"', false);

    Livewire::actingAs($admin)->test(StudentTree::class, ['user' => $student, 'course' => $made['course']])
        ->set('restartConfirmation', 'otra cosa')->call('restartCourse')->assertHasErrors('restartConfirmation');
    expect(NodeUnlock::where('user_id', $student->id)->where('node_id', $made['root']->id)->exists())->toBeTrue();

    Livewire::actingAs($admin)->test(StudentTree::class, ['user' => $student, 'course' => $made['course']])
        ->set('restartConfirmation', 'reiniciar')->call('restartCourse')->assertHasNoErrors();

    expect(NodeUnlock::where('user_id', $student->id)->where('node_id', $made['root']->id)->exists())->toBeFalse()
        ->and(NodeUnlock::where('user_id', $student->id)->where('node_id', $other['root']->id)->exists())->toBeTrue();
    Notification::assertSentTo($student, PlatformNotification::class);
});

test('el docente no le puede reiniciar el curso a un alumno de su comisión', function () {
    $made = makeCourse();
    $student = studentWithRootOpen($made);
    $teacher = User::factory()->create(['role' => 'teacher']);

    expect($teacher->can('restoreProgress', [$student, $made['course']]))->toBeFalse();
});
