<?php

namespace App\Services;

use App\Enums\CoinReason;
use App\Exceptions\NodeLocked;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Models\User;
use Illuminate\Support\Facades\DB;

class NodeUnlocker
{
    public function __construct(
        private readonly TreeAccess $access,
        private readonly Ledger $ledger,
        private readonly SubmissionReviewer $reviewer,
    ) {}

    /** @throws NodeLocked */
    public function unlock(User $user, Node $node): NodeUnlock
    {
        $unlock = DB::transaction(function () use ($user, $node) {
            // Bloquea al usuario antes de revisar: dos pedidos simultáneos se ejecutan de a uno.
            User::whereKey($user->id)->lockForUpdate()->first();

            $blockers = $this->access->unlockBlockers($user, $node);
            if ($blockers !== []) {
                throw new NodeLocked($blockers);
            }

            $currency = $this->access->paymentCurrency($node);

            $unlock = NodeUnlock::create([
                'user_id' => $user->id,
                'node_id' => $node->id,
                'currency_id' => $currency->id,
                'price_paid' => $node->price,
                'unlocked_at' => now(),
            ]);

            if ($node->price > 0) {
                $this->ledger->debit($user, $currency, $node->price, CoinReason::NodeUnlock, $unlock, $node->course);
            }

            return $unlock;
        });

        // Sin obligatorias, abrirlo ya lo completa (XP del nodo, curso completado, historia).
        if ($this->access->requiredPracticesApproved($user, $node)) {
            $this->reviewer->completeOnOpen($user, $node);
        }

        return $unlock;
    }
}
