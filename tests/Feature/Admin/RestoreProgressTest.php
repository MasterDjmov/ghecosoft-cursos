<?php

use App\Enums\CoinReason;
use App\Enums\SubmissionStatus;
use App\Livewire\Admin\Students\Tree;
use App\Models\Cohort;
use App\Models\CourseSubscription;
use App\Models\Currency;
use App\Models\NodeStepCompletion;
use App\Models\NodeUnlock;
use App\Models\PracticeGrant;
use App\Models\Submission;
use App\Models\User;
use App\Services\Ledger;
use App\Services\PracticeSubmitter;
use App\Services\TreeAccess;
use Livewire\Livewire;

/*
 * D103: el administrador restaura el avance de un alumno desde su árbol (abrir, micro-misiones, prácticas o el
 * nodo entero), en el orden del árbol y pagando lo mismo que si lo hubiera hecho él. El docente, no.
 */

beforeEach(function () {
    $this->data = makeCourse();
    $this->course = $this->data['course'];
    $this->admin = User::factory()->admin()->create();
    $this->student = enrolledStudent($this->course);
    $this->coins = fn () => app(Ledger::class)->balance($this->student, Currency::forCourse($this->course));
});

test('el administrador aprueba nodos enteros en orden y se paga como si los hubiera hecho el alumno', function () {
    $access = app(TreeAccess::class);
    $tree = Livewire::actingAs($this->admin)->test(Tree::class, ['user' => $this->student, 'course' => $this->course])
        ->assertSee('data-test="restore-progress"', false)
        ->call('restoreNode', $this->data['root']->id);

    // El raíz se cobró (10) y su práctica pagó 10.
    expect($access->isCompleted($this->student, $this->data['root']))->toBeTrue()
        ->and(($this->coins)())->toBe(10)
        ->and(NodeUnlock::where('user_id', $this->student->id)->where('node_id', $this->data['root']->id)->value('price_paid'))->toBe(10)
        ->and($this->student->fresh()->xp_total)->toBeGreaterThan(0)
        ->and($this->student->notifications()->where('data->kind', 'progress_restored')->count())->toBe(1);

    $tree->call('restoreNode', $this->data['topic1']->id)->call('restoreUnlock', $this->data['topic2']->id);

    $optional = $this->data['topic1']->practices()->where('is_required', false)->first();
    expect($access->isCompleted($this->student, $this->data['topic1']))->toBeTrue()
        ->and($access->isCompleted($this->student, $this->data['topic2']))->toBeTrue()
        ->and(Submission::where('user_id', $this->student->id)->where('practice_id', $optional->id)->exists())->toBeFalse()
        ->and(($this->coins)())->toBe(0);
});

test('respeta el orden del árbol: sin el padre completo no abre', function () {
    Livewire::actingAs($this->admin)->test(Tree::class, ['user' => $this->student, 'course' => $this->course])
        ->call('restoreNode', $this->data['topic1']->id);

    expect(NodeUnlock::where('user_id', $this->student->id)->exists())->toBeFalse();
});

test('si no le alcanza el saldo, el nodo se abre sin cobrar', function () {
    app(Ledger::class)->debit($this->student, Currency::forCourse($this->course), 10, CoinReason::ManualAdjustment);

    Livewire::actingAs($this->admin)->test(Tree::class, ['user' => $this->student, 'course' => $this->course])
        ->call('restoreUnlock', $this->data['root']->id);

    expect(NodeUnlock::where('user_id', $this->student->id)->where('node_id', $this->data['root']->id)->value('price_paid'))->toBe(0)
        ->and(($this->coins)())->toBe(0);
});

test('de a una: micro-misión superada y práctica aprobada, usando la entrega que esperaba corrección', function () {
    $course = $this->course;
    $root = $this->data['root'];
    $step = $root->steps()->create(['code' => 'R00-N01-P1', 'title' => 'El pergamino habla', 'position' => 1, 'xp_reward' => 5, 'expected_output' => 'hola']);
    $root->steps()->create(['code' => 'R00-N01-P2', 'title' => 'Otra', 'position' => 2, 'xp_reward' => 5, 'expected_output' => 'chau']);
    $student = studentWithRootOpen($this->data);
    $practice = $root->practices()->where('is_required', true)->first();
    // Ya había entregado (con las prácticas abiertas por el profe) y esperaba corrección.
    PracticeGrant::create(['user_id' => $student->id, 'node_id' => $root->id, 'granted_by' => $this->admin->id]);
    $pending = app(PracticeSubmitter::class)->submit($student, $practice, 'print("hola")');

    $tree = Livewire::actingAs($this->admin)->test(Tree::class, ['user' => $student, 'course' => $course])
        ->call('restoreStep', $step->id)
        ->call('restoreStep', $step->id)
        ->call('restorePractice', $practice->id);

    expect(NodeStepCompletion::where('user_id', $student->id)->where('node_step_id', $step->id)->count())->toBe(1)
        ->and($pending->fresh()->status)->toBe(SubmissionStatus::Approved)
        ->and(Submission::where('user_id', $student->id)->where('practice_id', $practice->id)->count())->toBe(1);

    $tree->call('restoreNode', $root->id);
    expect(app(TreeAccess::class)->stepProgress($student, $root))->toBe(['done' => $root->steps()->count(), 'total' => $root->steps()->count()])
        ->and(app(TreeAccess::class)->isCompleted($student, $root))->toBeTrue();
});

test('el docente no restaura avance (ni ve la sección)', function () {
    $teacher = User::factory()->teacher()->create();
    $cohort = Cohort::create(['course_id' => $this->course->id, 'teacher_id' => $teacher->id, 'name' => 'Martes']);
    CourseSubscription::where('user_id', $this->student->id)->update(['cohort_id' => $cohort->id]);

    Livewire::actingAs($teacher)->test(Tree::class, ['user' => $this->student, 'course' => $this->course])
        ->assertOk()
        ->assertDontSee('data-test="restore-progress"', false)
        ->call('restoreNode', $this->data['root']->id)
        ->assertForbidden();

    expect(NodeUnlock::where('user_id', $this->student->id)->exists())->toBeFalse();
});
