<?php

use App\Enums\SubmissionStatus;
use App\Livewire\Admin\Submissions\Show;
use App\Models\User;
use App\Services\Ledger;
use App\Services\PracticeSubmitter;
use App\Services\SubmissionReviewer;
use App\Services\TreeAccess;
use Livewire\Livewire;

/* D82: una entrega marcada para rehacer por error se aprueba igual, sin que el alumno vuelva a entregar. */

beforeEach(function () {
    $this->admin = User::factory()->admin()->create();
    $this->made = makeCourse();
    $this->student = studentWithRootOpen($this->made);
    $this->practice = $this->made['root']->practices()->first();
    $this->submission = app(PracticeSubmitter::class)->submit($this->student, $this->practice, 'print("hola")');
    app(SubmissionReviewer::class)->redo($this->submission, $this->admin, 'Te falta el total.');
    $this->currency = app(TreeAccess::class)->paymentCurrency($this->made['root']);
});

test('se aprueba igual, cobra lo de siempre y una sola vez', function () {
    $before = app(Ledger::class)->balance($this->student, $this->currency);

    Livewire::actingAs($this->admin)->test(Show::class, ['submission' => $this->submission->fresh()])
        ->assertSee('data-test="approve-anyway"', false)
        ->set('comment', 'Perdón, estaba bien.')
        ->call('approveAnyway');

    expect($this->submission->fresh()->status)->toBe(SubmissionStatus::Approved)
        ->and(app(Ledger::class)->balance($this->student, $this->currency))->toBe($before + $this->practice->coin_reward)
        ->and($this->submission->comments()->where('body', 'Perdón, estaba bien.')->exists())->toBeTrue();

    // Ya aprobada, no se puede aprobar otra vez.
    expect(fn () => app(SubmissionReviewer::class)->approve($this->submission->fresh(), $this->admin, reconsider: true))->toThrow(DomainException::class);
    expect(app(Ledger::class)->balance($this->student, $this->currency))->toBe($before + $this->practice->coin_reward);
});

test('si el alumno ya mandó otra entrega, se corrige esa y no la vieja', function () {
    app(PracticeSubmitter::class)->submit($this->student, $this->practice, 'print("hola de nuevo")');

    Livewire::actingAs($this->admin)->test(Show::class, ['submission' => $this->submission->fresh()])
        ->assertDontSee('data-test="approve-anyway"', false)
        ->call('approveAnyway');

    expect($this->submission->fresh()->status)->toBe(SubmissionStatus::Redo);
});

test('una entrega sin corregir no muestra «Aprobar igual»', function () {
    $fresh = app(PracticeSubmitter::class)->submit($this->student, $this->practice, 'print(1)');

    Livewire::actingAs($this->admin)->test(Show::class, ['submission' => $fresh])->assertDontSee('data-test="approve-anyway"', false);
});
