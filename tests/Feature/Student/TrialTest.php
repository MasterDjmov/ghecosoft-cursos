<?php

use App\Models\CoinTransaction;
use App\Models\NodeUnlock;
use App\Models\PracticeMark;
use App\Models\Submission;
use App\Models\User;
use App\Services\NodeUnlocker;
use App\Services\PracticeSubmitter;
use App\Services\TreeAccess;

beforeEach(function () {
    $this->data = makeCourse();
    $this->course = $this->data['course'];
    $this->root = $this->data['root'];
    $this->student = User::factory()->create();
});

test('sin abono, un alumno prueba gratis la clase 0: la lee y la practica, y ve el árbol', function () {
    $this->actingAs($this->student)->get(route('student.node', [$this->course, $this->root]))
        ->assertOk()->assertSee('data-test="trial-banner"', false)->assertSee('Primer programa')->assertSee('Pedir abono');

    $this->actingAs($this->student)->get(route('student.tree', $this->course))
        ->assertOk()->assertSee('data-test="trial-banner"', false)->assertSee('Probar gratis');

    $this->actingAs($this->student)->get(route('student.course', $this->course))->assertOk()->assertSee('data-test="trial-offer"', false);
    $this->actingAs($this->student)->get(route('student.worlds'))->assertOk()->assertSee('data-test="try-'.$this->course->slug.'"', false);
});

test('la prueba es solo la clase 0: los demás nodos siguen cerrados', function () {
    $this->actingAs($this->student)->get(route('student.node', [$this->course, $this->data['topic1']]))->assertForbidden();
    $this->actingAs($this->student)->get(route('student.node', [$this->course, $this->data['extra']]))->assertForbidden();
});

test('en la prueba no se entrega, no se marca ni se consulta al profe, y no queda ningún registro', function () {
    $practice = $this->root->practices()->first();
    $submitter = app(PracticeSubmitter::class);

    expect(fn () => $submitter->submit($this->student, $practice, 'print(1)'))->toThrow(DomainException::class, 'Estás probando la clase gratis')
        ->and(fn () => $submitter->toggleMark($this->student, $practice))->toThrow(DomainException::class)
        ->and($this->student->can('viewThread', [$practice, $this->student]))->toBeFalse()
        ->and(Submission::where('user_id', $this->student->id)->exists())->toBeFalse()
        ->and(PracticeMark::where('user_id', $this->student->id)->exists())->toBeFalse()
        ->and(NodeUnlock::where('user_id', $this->student->id)->exists())->toBeFalse()
        ->and(CoinTransaction::where('user_id', $this->student->id)->exists())->toBeFalse();
});

test('no hay prueba si el curso o la clase 0 no están publicados', function () {
    $this->root->update(['is_published' => false]);
    $this->actingAs($this->student)->get(route('student.node', [$this->course, $this->root]))->assertForbidden();

    $this->root->update(['is_published' => true]);
    $this->course->update(['is_published' => false]);
    expect(app(TreeAccess::class)->isTrial($this->student, $this->root->fresh()))->toBeFalse();
});

test('con el abono aprobado la clase 0 se abre como siempre, con sus monedas, y deja de ser prueba', function () {
    $student = enrolledStudent($this->course, $this->student);
    $access = app(TreeAccess::class);

    // Con abono vigente no hay prueba: se abre con las monedas que dio la inscripción.
    expect($access->isTrial($student, $this->root))->toBeFalse()
        ->and($access->canView($student, $this->root))->toBeFalse();

    app(NodeUnlocker::class)->unlock($student, $this->root);
    $practice = $this->root->practices()->first();

    expect($access->isTrial($student, $this->root))->toBeFalse()
        ->and(app(PracticeSubmitter::class)->blocker($student, $practice))->toBeNull();
    $this->actingAs($student)->get(route('student.node', [$this->course, $this->root]))
        ->assertOk()->assertDontSee('data-test="trial-banner"', false);
});

test('quien ya abrió la clase 0 y se le venció el abono la repasa como siempre, sin volver a la prueba', function () {
    $student = enrolledStudent($this->course, $this->student);
    app(NodeUnlocker::class)->unlock($student, $this->root);
    $student->subscriptions()->update(['ends_at' => now()->subDay()]);

    expect(app(TreeAccess::class)->isTrial($student, $this->root))->toBeFalse();
    $this->actingAs($student)->get(route('student.node', [$this->course, $this->root]))
        ->assertOk()->assertDontSee('data-test="trial-banner"', false);
});

test('la landing invita a crear la cuenta y probar gratis', function () {
    $this->get(route('landing'))->assertOk()->assertSee('data-test="landing-trial"', false);
});
