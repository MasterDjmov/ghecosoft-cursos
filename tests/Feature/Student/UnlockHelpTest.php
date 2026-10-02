<?php

use App\Enums\CoinReason;
use App\Livewire\Admin\Students\Tree as StudentTree;
use App\Livewire\Student\NodeView;
use App\Models\Cohort;
use App\Models\CourseSubscription;
use App\Models\NodeUnlock;
use App\Models\User;
use App\Services\Ledger;
use App\Services\PracticeSubmitter;
use App\Services\SubmissionReviewer;
use App\Services\TreeAccess;
use Livewire\Livewire;

/*
 * Cuando un alumno se traba al abrir el nodo siguiente: el «Siguiente» del nodo lo abre directo, y el
 * docente (de su comisión) o el administrador se lo pueden abrir desde su árbol, con sus monedas.
 */

beforeEach(function () {
    $this->data = makeCourse();
    $this->course = $this->data['course'];
    $this->admin = User::factory()->admin()->create();
    $this->student = studentWithRootOpen($this->data);
    // Aprueba la obligatoria del raíz: cobra 10 y el Tema 1 (precio 10) queda para abrir.
    $practice = $this->data['root']->practices()->first();
    $submission = app(PracticeSubmitter::class)->submit($this->student, $practice, 'print("hola")');
    app(SubmissionReviewer::class)->approve($submission, $this->admin, null);
    $this->currency = app(TreeAccess::class)->paymentCurrency($this->data['topic1']);
});

test('el administrador le abre el nodo con sus monedas, queda registrado y le llega el aviso', function () {
    Livewire::actingAs($this->admin)
        ->test(StudentTree::class, ['user' => $this->student, 'course' => $this->course])
        ->assertSee('data-test="student-next-nodes"', false)
        ->assertSee('Lo puede abrir ya.')
        ->call('unlockFor', $this->data['topic1']->id)
        ->assertHasNoErrors();

    $unlock = NodeUnlock::where('user_id', $this->student->id)->where('node_id', $this->data['topic1']->id)->first();
    expect($unlock)->not->toBeNull()
        ->and($unlock->unlocked_by)->toBe($this->admin->id)
        ->and(app(Ledger::class)->balance($this->student, $this->currency))->toBe(0)
        ->and($this->student->notifications()->where('data->kind', 'node_unlocked_for_you')->exists())->toBeTrue();
});

test('con las mismas reglas: si no le alcanza, no se abre y se ve por qué', function () {
    app(Ledger::class)->debit($this->student, $this->currency, 5, CoinReason::NodeUnlock, $this->data['topic1'], $this->course);

    Livewire::actingAs($this->admin)
        ->test(StudentTree::class, ['user' => $this->student, 'course' => $this->course])
        ->assertDontSee('data-test="unlock-for-'.$this->data['topic1']->id.'"', false)
        ->call('unlockFor', $this->data['topic1']->id);

    expect(NodeUnlock::where('user_id', $this->student->id)->where('node_id', $this->data['topic1']->id)->exists())->toBeFalse();
});

test('el docente se lo abre solo a los alumnos de su comisión', function () {
    $teacher = User::factory()->teacher()->create();
    $cohort = Cohort::create(['course_id' => $this->course->id, 'teacher_id' => $teacher->id, 'name' => 'Martes']);

    Livewire::actingAs($teacher)
        ->test(StudentTree::class, ['user' => $this->student, 'course' => $this->course])
        ->assertForbidden();

    CourseSubscription::where('user_id', $this->student->id)->update(['cohort_id' => $cohort->id]);
    Livewire::actingAs($teacher)
        ->test(StudentTree::class, ['user' => $this->student, 'course' => $this->course])
        ->call('unlockFor', $this->data['topic1']->id);

    expect(NodeUnlock::where('node_id', $this->data['topic1']->id)->value('unlocked_by'))->toBe($teacher->id);
});

test('al completar el nodo, el alumno ve el aviso arriba y lo abre desde ahí sin ir al árbol', function () {
    Livewire::actingAs($this->student)
        ->test(NodeView::class, ['course' => $this->course, 'node' => $this->data['root']])
        ->assertSee('data-test="node-next-ready"', false)
        ->assertSee('Abrir «Tema 1»')
        ->call('unlockNext', $this->data['topic1']->id)
        ->assertRedirect(route('student.node', [$this->course, $this->data['topic1']]));

    $unlock = NodeUnlock::where('user_id', $this->student->id)->where('node_id', $this->data['topic1']->id)->first();
    expect($unlock)->not->toBeNull()->and($unlock->unlocked_by)->toBeNull();
});

test('desde un nodo solo se abren sus siguientes', function () {
    Livewire::actingAs($this->student)
        ->test(NodeView::class, ['course' => $this->course, 'node' => $this->data['root']])
        ->call('unlockNext', $this->data['topic2']->id)
        ->assertNotFound();
});
