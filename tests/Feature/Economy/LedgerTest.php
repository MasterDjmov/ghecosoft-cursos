<?php

use App\Enums\CoinReason;
use App\Enums\XpReason;
use App\Exceptions\InsufficientFunds;
use App\Models\CoinTransaction;
use App\Models\Currency;
use App\Models\User;
use App\Services\Ledger;

beforeEach(function () {
    $this->ledger = app(Ledger::class);
    $this->user = User::factory()->create();
    $this->currency = Currency::wildcard();
});

test('el saldo es la suma de los movimientos', function () {
    $this->ledger->credit($this->user, $this->currency, 10, CoinReason::ManualAdjustment, note: 'bonus');
    $this->ledger->credit($this->user, $this->currency, 5, CoinReason::PracticeApproved);
    $this->ledger->debit($this->user, $this->currency, 3, CoinReason::NodeUnlock);

    expect($this->ledger->balance($this->user, $this->currency))->toBe(12)
        ->and(CoinTransaction::where('user_id', $this->user->id)->count())->toBe(3);
});

test('no se puede gastar más de lo que hay y no queda registro', function () {
    $this->ledger->credit($this->user, $this->currency, 2, CoinReason::ManualAdjustment);

    expect(fn () => $this->ledger->debit($this->user, $this->currency, 5, CoinReason::NodeUnlock))
        ->toThrow(InsufficientFunds::class);

    expect($this->ledger->balance($this->user, $this->currency))->toBe(2)
        ->and(CoinTransaction::count())->toBe(1);
});

test('los montos tienen que ser positivos', function () {
    expect(fn () => $this->ledger->credit($this->user, $this->currency, 0, CoinReason::ManualAdjustment))
        ->toThrow(InvalidArgumentException::class);
    expect(fn () => $this->ledger->debit($this->user, $this->currency, -3, CoinReason::ManualAdjustment))
        ->toThrow(InvalidArgumentException::class);
});

test('cada tipo de moneda tiene su propio saldo', function () {
    $course = makeCourse()['course'];
    $courseCoin = Currency::forCourse($course);

    $this->ledger->credit($this->user, $courseCoin, 10, CoinReason::EnrollmentGrant);
    $this->ledger->credit($this->user, $this->currency, 3, CoinReason::PracticeApproved);

    expect($this->ledger->balance($this->user, $courseCoin))->toBe(10)
        ->and($this->ledger->balance($this->user, $this->currency))->toBe(3)
        ->and($this->ledger->balances($this->user)->all())->toEqualCanonicalizing([$courseCoin->id => 10, $this->currency->id => 3]);
});

test('la XP se registra y actualiza el total, y nunca queda negativa', function () {
    $this->ledger->addXp($this->user, 50, XpReason::PracticeApproved);
    $this->ledger->addXp($this->user, -20, XpReason::Reversal, note: 'corrección');

    expect($this->user->fresh()->xp_total)->toBe(30);

    expect(fn () => $this->ledger->addXp($this->user, -31, XpReason::Reversal))->toThrow(InvalidArgumentException::class);
    expect($this->user->fresh()->xp_total)->toBe(30);
});
