<?php

use App\Enums\CoinReason;
use App\Exceptions\NodeLocked;
use App\Models\Currency;
use App\Models\EnrollmentRequest;
use App\Models\NodeUnlock;
use App\Models\User;
use App\Services\EnrollmentApprover;
use App\Services\Ledger;
use App\Services\NodeUnlocker;
use App\Services\TreeAccess;

beforeEach(function () {
    ['course' => $this->course, 'root' => $this->root, 'topic1' => $this->topic1, 'topic2' => $this->topic2, 'extra' => $this->extra] = makeCourse();
    $this->access = app(TreeAccess::class);
    $this->unlocker = app(NodeUnlocker::class);
    $this->ledger = app(Ledger::class);
});

test('sin abono no se puede abrir el raíz, aunque tenga monedas', function () {
    $student = User::factory()->create();
    $this->ledger->credit($student, Currency::forCourse($this->course), 10, CoinReason::ManualAdjustment);

    expect($this->access->unlockBlockers($student, $this->root))->toContain(TreeAccess::BLOCK_NO_SUBSCRIPTION);
    expect(fn () => $this->unlocker->unlock($student, $this->root))->toThrow(NodeLocked::class);
});

test('el alumno abre el raíz con las monedas del pago', function () {
    $student = enrolledStudent($this->course);

    expect($this->access->state($student, $this->root))->toBe(TreeAccess::STATE_AVAILABLE);

    $this->unlocker->unlock($student, $this->root);

    expect($this->access->isUnlocked($student, $this->root))->toBeTrue()
        ->and($this->ledger->balance($student, Currency::forCourse($this->course)))->toBe(0);
});

test('abrir el mismo nodo dos veces no cobra dos veces', function () {
    $student = enrolledStudent($this->course);
    $this->unlocker->unlock($student, $this->root);

    expect(fn () => $this->unlocker->unlock($student, $this->root))->toThrow(NodeLocked::class);
    expect(NodeUnlock::count())->toBe(1);
});

test('para abrir el siguiente nodo hacen falta las obligatorias aprobadas Y las monedas', function () {
    $student = enrolledStudent($this->course);
    $this->unlocker->unlock($student, $this->root);
    $coin = Currency::forCourse($this->course);

    // Tiene monedas de sobra pero no aprobó las obligatorias del raíz: el ahorro no saltea prácticas.
    $this->ledger->credit($student, $coin, 50, CoinReason::ManualAdjustment);
    expect($this->access->unlockBlockers($student, $this->topic1))->toBe([TreeAccess::BLOCK_PARENT_INCOMPLETE])
        ->and($this->access->state($student, $this->topic1))->toBe(TreeAccess::STATE_LOCKED);

    approveRequiredPractices($student, $this->root);
    expect($this->access->canUnlock($student, $this->topic1))->toBeTrue();

    $this->unlocker->unlock($student, $this->topic1);
    expect($this->ledger->balance($student, $coin))->toBe(40);
});

test('con las obligatorias aprobadas pero sin monedas, el nodo queda "listo para abrir"', function () {
    $student = enrolledStudent($this->course);
    $this->unlocker->unlock($student, $this->root);
    approveRequiredPractices($student, $this->root);

    expect($this->access->unlockBlockers($student, $this->topic1))->toBe([TreeAccess::BLOCK_INSUFFICIENT_FUNDS])
        ->and($this->access->state($student, $this->topic1))->toBe(TreeAccess::STATE_AVAILABLE);
});

test('con el abono vencido no abre ni entrega, pero sigue viendo lo que abrió', function () {
    $student = enrolledStudent($this->course);
    $this->unlocker->unlock($student, $this->root);
    approveRequiredPractices($student, $this->root);
    $this->ledger->credit($student, Currency::forCourse($this->course), 10, CoinReason::ManualAdjustment);

    $this->travel(31)->days();

    expect($this->access->unlockBlockers($student, $this->topic1))->toContain(TreeAccess::BLOCK_NO_SUBSCRIPTION)
        ->and($this->access->canSubmit($student, $this->root->practices()->first()))->toBeFalse()
        ->and($this->access->canView($student, $this->root))->toBeTrue()
        ->and($this->access->canView($student, $this->topic1))->toBeFalse();
});

test('los extras se pagan con comodines, no con monedas del curso', function () {
    $student = enrolledStudent($this->course);
    $this->unlocker->unlock($student, $this->root);
    approveRequiredPractices($student, $this->root);
    $this->ledger->credit($student, Currency::forCourse($this->course), 10, CoinReason::ManualAdjustment);

    expect($this->access->unlockBlockers($student, $this->extra))->toBe([TreeAccess::BLOCK_INSUFFICIENT_FUNDS]);

    $this->ledger->credit($student, Currency::wildcard(), 3, CoinReason::PracticeApproved);
    $this->unlocker->unlock($student, $this->extra);

    expect($this->ledger->balance($student, Currency::wildcard()))->toBe(0)
        ->and($this->ledger->balance($student, Currency::forCourse($this->course)))->toBe(10);
});

test('el comodín nunca abre un raíz', function () {
    $this->root->update(['price_currency_id' => Currency::wildcard()->id]);
    $student = User::factory()->create();
    app(EnrollmentApprover::class)->approve(
        EnrollmentRequest::create(['user_id' => $student->id, 'course_id' => $this->course->id, 'kind' => 'renewal', 'type' => 'contact']),
        User::factory()->admin()->create(),
    );
    $this->ledger->credit($student, Currency::wildcard(), 50, CoinReason::PracticeApproved);

    expect($this->access->unlockBlockers($student, $this->root->fresh()))->toBe([TreeAccess::BLOCK_INSUFFICIENT_FUNDS]);
});

test('un nodo de otro curso sin raíz abierto está bloqueado', function () {
    ['topic1' => $otherTopic] = makeCourse();
    $student = enrolledStudent($this->course);

    expect($this->access->unlockBlockers($student, $otherTopic))->toContain(TreeAccess::BLOCK_NO_SUBSCRIPTION, TreeAccess::BLOCK_ROOT_CLOSED);
});
