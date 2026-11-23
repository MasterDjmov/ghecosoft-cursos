<?php

use App\Enums\CoinReason;
use App\Enums\SubmissionStatus;
use App\Livewire\Admin\Submissions\Show;
use App\Models\Cohort;
use App\Models\CourseSubscription;
use App\Models\User;
use App\Services\Ledger;
use App\Services\PracticeSubmitter;
use App\Services\SubmissionReviewer;
use App\Services\TreeAccess;
use Livewire\Livewire;

/* D125: una entrega aprobada por error vuelve a «Para rehacer» y se descuenta lo que cobró; al aprobarla de nuevo cobra una vez. */

beforeEach(function () {
    $this->admin = User::factory()->admin()->create();
    $this->made = makeCourse();
    $this->student = studentWithRootOpen($this->made);
    $this->practice = $this->made['root']->practices()->first();
    $this->currency = app(TreeAccess::class)->paymentCurrency($this->made['root']);
    $this->before = app(Ledger::class)->balance($this->student, $this->currency);
    $this->xpBefore = $this->student->fresh()->xp_total;
    $this->submission = app(PracticeSubmitter::class)->submit($this->student, $this->practice, 'print("mal")');
    app(SubmissionReviewer::class)->approve($this->submission, $this->admin);
});

test('vuelve a «Para rehacer», descuenta lo cobrado y le avisa; al aprobar la nueva cobra una sola vez', function () {
    $paidXp = $this->student->fresh()->xp_total - $this->xpBefore;

    Livewire::actingAs($this->admin)->test(Show::class, ['submission' => $this->submission->fresh()])
        ->assertSee('data-test="revoke-open"', false)
        ->call('revoke')->assertHasErrors('comment')
        ->set('comment', 'El recargo va sobre la deuda.')
        ->call('revoke')->assertHasNoErrors();

    $submission = $this->submission->fresh();
    expect($submission->status)->toBe(SubmissionStatus::Redo)
        ->and($submission->comments()->where('body', 'El recargo va sobre la deuda.')->exists())->toBeTrue()
        ->and(app(Ledger::class)->balance($this->student, $this->currency))->toBe($this->before)
        // La XP de la práctica se devuelve; la del nodo completo (si la hubo) queda.
        ->and($this->student->fresh()->xp_total)->toBe($this->xpBefore + $paidXp - $this->practice->xp_reward)
        ->and($this->student->coinTransactions()->where('reason', CoinReason::Reversal)->count())->toBe(1)
        ->and($this->student->notifications()->where('data->kind', 'submission.redo')->exists())->toBeTrue();

    // Ya no se puede volver atrás de nuevo.
    expect(fn () => app(SubmissionReviewer::class)->revoke($submission, $this->admin, 'otra vez'))->toThrow(DomainException::class);

    // Manda la corregida y se aprueba: cobra lo de la práctica una vez más (y no el nodo de nuevo).
    $again = app(PracticeSubmitter::class)->submit($this->student, $this->practice, 'print("bien")');
    app(SubmissionReviewer::class)->approve($again, $this->admin);
    expect(app(Ledger::class)->balance($this->student, $this->currency))->toBe($this->before + $this->practice->coin_reward)
        ->and($this->student->fresh()->xp_total)->toBe($this->xpBefore + $paidXp);
});

test('si ya gastó las monedas no se puede, y no cambia nada', function () {
    $balance = app(Ledger::class)->balance($this->student, $this->currency);
    app(Ledger::class)->debit($this->student, $this->currency, $balance, CoinReason::NodeUnlock);

    expect(fn () => app(SubmissionReviewer::class)->revoke($this->submission->fresh(), $this->admin, 'Rehacela'))
        ->toThrow(DomainException::class, 'Ya gastó');
    expect($this->submission->fresh()->status)->toBe(SubmissionStatus::Approved)
        ->and(app(Ledger::class)->balance($this->student, $this->currency))->toBe(0);
});

test('solo la última entrega aprobada, y solo quien la puede corregir', function () {
    // Un docente que no lo tiene en sus comisiones no entra.
    Livewire::actingAs(User::factory()->teacher()->create())->test(Show::class, ['submission' => $this->submission->fresh()])->assertForbidden();

    // El docente de su comisión sí.
    $teacher = User::factory()->teacher()->create();
    $cohort = Cohort::create(['course_id' => $this->made['course']->id, 'teacher_id' => $teacher->id, 'name' => 'Martes']);
    CourseSubscription::where('user_id', $this->student->id)->update(['cohort_id' => $cohort->id]);
    Livewire::actingAs($teacher)->test(Show::class, ['submission' => $this->submission->fresh()])
        ->assertSee('data-test="revoke-open"', false)
        ->set('comment', 'Revisá el total.')->call('revoke');
    expect($this->submission->fresh()->status)->toBe(SubmissionStatus::Redo);
});
