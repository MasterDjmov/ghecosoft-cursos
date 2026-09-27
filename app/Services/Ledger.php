<?php

namespace App\Services;

use App\Enums\CoinReason;
use App\Enums\XpReason;
use App\Exceptions\InsufficientFunds;
use App\Models\CoinTransaction;
use App\Models\Course;
use App\Models\Currency;
use App\Models\User;
use App\Models\XpTransaction;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;
use InvalidArgumentException;

/**
 * Único punto de escritura de monedas y XP. Cada movimiento queda en el libro
 * (coin_transactions / xp_transactions) y el saldo es la suma de movimientos.
 * Las escrituras bloquean la fila del usuario para que dos pedidos simultáneos
 * no gasten el mismo saldo.
 */
class Ledger
{
    public function balance(User $user, Currency $currency): int
    {
        return (int) CoinTransaction::where('user_id', $user->id)
            ->where('currency_id', $currency->id)
            ->sum('amount');
    }

    /** @return Collection<int, int> saldo por currency_id (solo los distintos de cero) */
    public function balances(User $user): Collection
    {
        return CoinTransaction::where('user_id', $user->id)
            ->groupBy('currency_id')
            ->selectRaw('currency_id, SUM(amount) as total')
            ->pluck('total', 'currency_id')
            ->map(fn ($total) => (int) $total)
            ->filter();
    }

    public function credit(
        User $user,
        Currency $currency,
        int $amount,
        CoinReason $reason,
        ?Model $source = null,
        ?Course $course = null,
        ?string $note = null,
        ?User $by = null,
    ): CoinTransaction {
        $this->assertPositive($amount);

        return DB::transaction(function () use ($user, $currency, $amount, $reason, $source, $course, $note, $by) {
            $this->lock($user);

            return $this->recordCoins($user, $currency, $amount, $reason, $source, $course, $note, $by);
        });
    }

    /** @throws InsufficientFunds */
    public function debit(
        User $user,
        Currency $currency,
        int $amount,
        CoinReason $reason,
        ?Model $source = null,
        ?Course $course = null,
        ?string $note = null,
        ?User $by = null,
    ): CoinTransaction {
        $this->assertPositive($amount);

        return DB::transaction(function () use ($user, $currency, $amount, $reason, $source, $course, $note, $by) {
            $this->lock($user);

            $balance = $this->balance($user, $currency);
            if ($balance < $amount) {
                throw new InsufficientFunds($balance, $amount);
            }

            return $this->recordCoins($user, $currency, -$amount, $reason, $source, $course, $note, $by);
        });
    }

    /** Suma (o resta, con monto negativo) XP y actualiza la caché users.xp_total. */
    public function addXp(
        User $user,
        int $amount,
        XpReason $reason,
        ?Model $source = null,
        ?Course $course = null,
        ?string $note = null,
        ?User $by = null,
    ): XpTransaction {
        if ($amount === 0) {
            throw new InvalidArgumentException('El movimiento de XP no puede ser 0.');
        }

        return DB::transaction(function () use ($user, $amount, $reason, $source, $course, $note, $by) {
            $locked = $this->lock($user);

            if ($locked->xp_total + $amount < 0) {
                throw new InvalidArgumentException('La experiencia no puede quedar negativa.');
            }

            $transaction = XpTransaction::create([
                'user_id' => $user->id,
                'amount' => $amount,
                'reason' => $reason,
                'course_id' => $course?->id,
                'source_type' => $source?->getMorphClass(),
                'source_id' => $source?->getKey(),
                'note' => $note,
                'created_by' => $by?->id,
            ]);

            $locked->increment('xp_total', $amount);
            $user->xp_total = $locked->xp_total;

            return $transaction;
        });
    }

    private function recordCoins(
        User $user,
        Currency $currency,
        int $amount,
        CoinReason $reason,
        ?Model $source,
        ?Course $course,
        ?string $note,
        ?User $by,
    ): CoinTransaction {
        return CoinTransaction::create([
            'user_id' => $user->id,
            'currency_id' => $currency->id,
            'amount' => $amount,
            'reason' => $reason,
            'course_id' => $course?->id ?? $currency->course_id,
            'source_type' => $source?->getMorphClass(),
            'source_id' => $source?->getKey(),
            'note' => $note,
            'created_by' => $by?->id,
        ]);
    }

    private function lock(User $user): User
    {
        return User::whereKey($user->id)->lockForUpdate()->firstOrFail();
    }

    private function assertPositive(int $amount): void
    {
        if ($amount <= 0) {
            throw new InvalidArgumentException('El monto tiene que ser mayor que 0.');
        }
    }
}
