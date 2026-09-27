<?php

use App\Enums\RequestStatus;
use App\Models\Currency;
use App\Models\EnrollmentRequest;
use App\Models\User;
use App\Services\EnrollmentApprover;
use App\Services\Ledger;
use App\Services\TreeAccess;

beforeEach(function () {
    ['course' => $this->course] = makeCourse(['root_price' => 10, 'subscription_days' => 30]);
    $this->student = User::factory()->create();
    $this->admin = User::factory()->admin()->create();
});

function requestFor(User $student, $course, string $kind = 'new'): EnrollmentRequest
{
    return EnrollmentRequest::create(['user_id' => $student->id, 'course_id' => $course->id, 'kind' => $kind, 'type' => 'receipt']);
}

test('una cuenta nueva arranca sin monedas', function () {
    expect(app(Ledger::class)->balances($this->student))->toBeEmpty();
});

test('aprobar una inscripción da las monedas del curso y 30 días de abono', function () {
    $this->travelTo(now()->startOfDay());

    $subscription = app(EnrollmentApprover::class)->approve(requestFor($this->student, $this->course), $this->admin);

    expect(app(Ledger::class)->balance($this->student, Currency::forCourse($this->course)))->toBe(10)
        ->and($subscription->ends_at->equalTo(now()->addDays(30)))->toBeTrue()
        ->and(app(TreeAccess::class)->hasActiveSubscription($this->student, $this->course))->toBeTrue();
});

test('las monedas del pago son del curso: no sirven como comodín', function () {
    app(EnrollmentApprover::class)->approve(requestFor($this->student, $this->course), $this->admin);

    expect(app(Ledger::class)->balance($this->student, Currency::wildcard()))->toBe(0);
});

test('renovar solo extiende el abono desde el vencimiento actual, sin dar monedas', function () {
    $this->travelTo(now()->startOfDay());
    $approver = app(EnrollmentApprover::class);
    $first = $approver->approve(requestFor($this->student, $this->course), $this->admin);

    $this->travel(10)->days();
    $renewal = $approver->approve(requestFor($this->student, $this->course, 'renewal'), $this->admin);

    expect($renewal->starts_at->equalTo($first->ends_at))->toBeTrue()
        ->and($renewal->ends_at->equalTo($first->ends_at->addDays(30)))->toBeTrue()
        ->and(app(Ledger::class)->balance($this->student, Currency::forCourse($this->course)))->toBe(10);
});

test('renovar con el abono vencido arranca hoy', function () {
    $approver = app(EnrollmentApprover::class);
    $approver->approve(requestFor($this->student, $this->course), $this->admin);

    $this->travel(45)->days();
    expect(app(TreeAccess::class)->hasActiveSubscription($this->student, $this->course))->toBeFalse();

    $renewal = $approver->approve(requestFor($this->student, $this->course, 'renewal'), $this->admin);
    expect($renewal->starts_at->isToday())->toBeTrue()
        ->and(app(TreeAccess::class)->hasActiveSubscription($this->student, $this->course))->toBeTrue();
});

test('una solicitud no se puede aprobar dos veces ni aprobar después de rechazarla', function () {
    $approver = app(EnrollmentApprover::class);
    $request = requestFor($this->student, $this->course);
    $approver->approve($request, $this->admin);

    expect(fn () => $approver->approve($request, $this->admin))->toThrow(DomainException::class);

    $other = requestFor($this->student, $this->course);
    $approver->reject($other, $this->admin, 'Comprobante ilegible');
    expect($other->fresh()->status)->toBe(RequestStatus::Rejected)
        ->and(fn () => $approver->approve($other, $this->admin))->toThrow(DomainException::class);

    expect(app(Ledger::class)->balance($this->student, Currency::forCourse($this->course)))->toBe(10);
});
