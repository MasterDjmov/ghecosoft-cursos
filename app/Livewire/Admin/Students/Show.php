<?php

namespace App\Livewire\Admin\Students;

use App\Enums\CoinReason;
use App\Enums\XpReason;
use App\Exceptions\InsufficientFunds;
use App\Models\CoinTransaction;
use App\Models\Currency;
use App\Models\Submission;
use App\Models\User;
use App\Models\XpTransaction;
use App\Services\Ledger;
use Flux\Flux;
use InvalidArgumentException;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Ficha del alumno: cursos, abonos, saldos, movimientos, entregas y ajuste manual. */
#[Title('Alumno')]
class Show extends Component
{
    public User $user;

    /** 'xp' o el id de una moneda. */
    public string $target = 'xp';

    public int $amount = 0;

    public string $reason = '';

    public function mount(User $user): void
    {
        abort_unless($user->isStudent(), 404);
    }

    /** Dar o quitar monedas o XP. El motivo es obligatorio y queda en el libro. */
    public function adjust(Ledger $ledger): void
    {
        $this->validate([
            'target' => ['required', 'string'],
            'amount' => ['required', 'integer', 'not_in:0', 'between:-10000,10000'],
            'reason' => ['required', 'string', 'min:3', 'max:255'],
        ], ['amount.not_in' => 'Poné un monto distinto de 0 (negativo para quitar).'], ['amount' => 'monto', 'reason' => 'motivo']);

        try {
            if ($this->target === 'xp') {
                $ledger->addXp($this->user, $this->amount, XpReason::ManualAdjustment, note: $this->reason, by: auth()->user());
            } else {
                $currency = Currency::findOrFail((int) $this->target);
                $this->amount > 0
                    ? $ledger->credit($this->user, $currency, $this->amount, CoinReason::ManualAdjustment, note: $this->reason, by: auth()->user())
                    : $ledger->debit($this->user, $currency, -$this->amount, CoinReason::ManualAdjustment, note: $this->reason, by: auth()->user());
            }
        } catch (InsufficientFunds|InvalidArgumentException) {
            $this->addError('amount', 'No alcanza el saldo para quitar esa cantidad.');

            return;
        }

        $this->reset('amount', 'reason');
        Flux::toast(variant: 'success', text: 'Ajuste registrado.');
    }

    public function render(Ledger $ledger)
    {
        $balances = $ledger->balances($this->user);

        return view('livewire.admin.students.show', [
            'subscriptions' => $this->user->subscriptions()->with(['course', 'cohort'])->orderByDesc('ends_at')->get(),
            'balances' => $balances,
            'currencies' => Currency::with('course')->get()->sortBy(fn ($c) => $c->is_wildcard ? 'zzz' : $c->course?->title),
            'coinMovements' => CoinTransaction::with(['currency.course', 'creator:id,name'])->where('user_id', $this->user->id)->latest('id')->limit(30)->get(),
            'xpMovements' => XpTransaction::with('creator:id,name')->where('user_id', $this->user->id)->latest('id')->limit(30)->get(),
            'submissions' => Submission::with('practice.node')->where('user_id', $this->user->id)->latest('submitted_at')->limit(15)->get(),
            'badges' => $this->user->badges()->get(),
        ])->title($this->user->fullName());
    }
}
