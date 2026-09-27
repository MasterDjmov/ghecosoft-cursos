<?php

namespace App\Services;

use App\Enums\NodeType;
use App\Enums\SubmissionStatus;
use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\Currency;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Models\Practice;
use App\Models\Submission;
use App\Models\User;

/**
 * Decide, en cada request, qué puede ver y abrir un alumno del árbol.
 *
 * - Ver un nodo: haberlo abierto alguna vez (el acceso a lo visto es permanente).
 * - Abrir un nodo: abono vigente + raíz abierto + obligatorias del nodo padre aprobadas + saldo.
 * - Entregar: nodo abierto + abono vigente.
 */
class TreeAccess
{
    public const STATE_LOCKED = 'locked';

    public const STATE_AVAILABLE = 'available';

    public const STATE_UNLOCKED = 'unlocked';

    public const STATE_COMPLETED = 'completed';

    public const BLOCK_ALREADY_UNLOCKED = 'already_unlocked';

    public const BLOCK_UNPUBLISHED = 'unpublished';

    public const BLOCK_NO_SUBSCRIPTION = 'no_subscription';

    public const BLOCK_ROOT_CLOSED = 'root_closed';

    public const BLOCK_PARENT_INCOMPLETE = 'parent_incomplete';

    public const BLOCK_INSUFFICIENT_FUNDS = 'insufficient_funds';

    public function __construct(private readonly Ledger $ledger) {}

    public function activeSubscription(User $user, Course $course): ?CourseSubscription
    {
        return CourseSubscription::active()
            ->where('user_id', $user->id)
            ->where('course_id', $course->id)
            ->orderByDesc('ends_at')
            ->first();
    }

    public function hasActiveSubscription(User $user, Course $course): bool
    {
        return $this->activeSubscription($user, $course) !== null;
    }

    public function isUnlocked(User $user, Node $node): bool
    {
        return NodeUnlock::where('user_id', $user->id)->where('node_id', $node->id)->exists();
    }

    public function isRootOpen(User $user, Course $course): bool
    {
        return NodeUnlock::where('user_id', $user->id)
            ->whereHas('node', fn ($q) => $q->where('course_id', $course->id)->where('type', NodeType::Root))
            ->exists();
    }

    /** Todas las obligatorias del nodo tienen al menos una entrega aprobada del alumno. */
    public function requiredPracticesApproved(User $user, Node $node): bool
    {
        $required = Practice::where('node_id', $node->id)->where('is_required', true)->pluck('id');

        if ($required->isEmpty()) {
            return true;
        }

        $approved = Submission::where('user_id', $user->id)
            ->whereIn('practice_id', $required)
            ->where('status', SubmissionStatus::Approved)
            ->distinct()
            ->count('practice_id');

        return $approved === $required->count();
    }

    public function isCompleted(User $user, Node $node): bool
    {
        return $this->isUnlocked($user, $node) && $this->requiredPracticesApproved($user, $node);
    }

    /**
     * Motivos por los que el alumno no puede abrir el nodo (vacío = puede).
     *
     * @return list<string>
     */
    public function unlockBlockers(User $user, Node $node): array
    {
        if ($this->isUnlocked($user, $node)) {
            return [self::BLOCK_ALREADY_UNLOCKED];
        }

        $blockers = [];

        if (! $node->is_published || ! $node->course->is_published) {
            $blockers[] = self::BLOCK_UNPUBLISHED;
        }

        if (! $this->hasActiveSubscription($user, $node->course)) {
            $blockers[] = self::BLOCK_NO_SUBSCRIPTION;
        }

        if (! $node->isRoot()) {
            if (! $this->isRootOpen($user, $node->course)) {
                $blockers[] = self::BLOCK_ROOT_CLOSED;
            }

            if ($node->parent && ! $this->isCompleted($user, $node->parent)) {
                $blockers[] = self::BLOCK_PARENT_INCOMPLETE;
            }
        }

        if ($this->ledger->balance($user, $this->paymentCurrency($node)) < $node->price) {
            $blockers[] = self::BLOCK_INSUFFICIENT_FUNDS;
        }

        return $blockers;
    }

    public function canUnlock(User $user, Node $node): bool
    {
        return $this->unlockBlockers($user, $node) === [];
    }

    /** El raíz se paga siempre con la moneda del curso: el comodín nunca abre un raíz. */
    public function paymentCurrency(Node $node): Currency
    {
        return $node->isRoot()
            ? Currency::forCourse($node->course)
            : $node->paymentCurrency();
    }

    public function canView(User $user, Node $node): bool
    {
        return $user->isAdmin() || $this->isUnlocked($user, $node);
    }

    public function canSubmit(User $user, Practice $practice): bool
    {
        $node = $practice->node;

        return $this->isUnlocked($user, $node) && $this->hasActiveSubscription($user, $node->course);
    }

    public function state(User $user, Node $node): string
    {
        if ($this->isUnlocked($user, $node)) {
            return $this->requiredPracticesApproved($user, $node) ? self::STATE_COMPLETED : self::STATE_UNLOCKED;
        }

        $blockers = array_diff($this->unlockBlockers($user, $node), [self::BLOCK_INSUFFICIENT_FUNDS, self::BLOCK_NO_SUBSCRIPTION]);

        return $blockers === [] ? self::STATE_AVAILABLE : self::STATE_LOCKED;
    }
}
