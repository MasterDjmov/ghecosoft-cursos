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
use Carbon\CarbonInterface;

/**
 * Decide, en cada request, qué puede ver y abrir un alumno del árbol.
 *
 * - Ver un nodo: haberlo abierto alguna vez (el acceso a lo visto es permanente).
 * - Abrir un nodo: abono vigente + raíz abierto + obligatorias del nodo padre (y de sus
 *   requisitos extra) aprobadas + saldo.
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

    public const BLOCK_REQUIREMENTS_INCOMPLETE = 'requirements_incomplete';

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

    /**
     * Hasta cuándo tiene abono pagado: el fin del período vigente o, si ya renovó, el del último
     * período que sigue pegado (la renovación empieza donde termina el anterior). Null sin abono vigente.
     */
    public function paidUntil(User $user, Course $course): ?CarbonInterface
    {
        $current = $this->activeSubscription($user, $course);
        if ($current === null) {
            return null;
        }

        $until = $current->ends_at;
        $later = CourseSubscription::where('user_id', $user->id)
            ->where('course_id', $course->id)
            ->where('ends_at', '>', $until)
            ->orderBy('starts_at')
            ->get(['starts_at', 'ends_at']);
        foreach ($later as $subscription) {
            if ($subscription->starts_at->lte($until) && $subscription->ends_at->gt($until)) {
                $until = $subscription->ends_at;
            }
        }

        return $until;
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

            if ($this->incompleteRequirements($user, $node) !== []) {
                $blockers[] = self::BLOCK_REQUIREMENTS_INCOMPLETE;
            }
        }

        if ($this->ledger->balance($user, $this->paymentCurrency($node)) < $node->price) {
            $blockers[] = self::BLOCK_INSUFFICIENT_FUNDS;
        }

        return $blockers;
    }

    /**
     * Requisitos extra del nodo que el alumno todavía no completó.
     *
     * @return list<Node>
     */
    public function incompleteRequirements(User $user, Node $node): array
    {
        return $node->requirements
            ->reject(fn (Node $required) => $this->isCompleted($user, $required))
            ->values()
            ->all();
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
        return $user->isAdmin() || $this->isUnlocked($user, $node) || $this->isTrial($user, $node);
    }

    /**
     * Clase 0 de prueba (D71): sin abono de ese curso, el raíz publicado de un curso publicado se puede
     * leer y practicar (el editor y Ejecutar andan) sin abrirlo: no se paga, no se entrega ni se consulta
     * al profe y no queda registro. Al aprobarse el abono, el raíz se abre como siempre.
     */
    public function isTrial(User $user, Node $node): bool
    {
        return $node->isRoot()
            && $node->is_published
            && $node->course->is_published
            && ! $user->isAdmin()
            && ! $this->isUnlocked($user, $node)
            && ! $this->hasActiveSubscription($user, $node->course);
    }

    /** El raíz del curso se puede probar gratis (D71). */
    public function canTryCourse(User $user, Course $course): bool
    {
        $root = $course->rootNode;

        return $root !== null && $this->isTrial($user, $root);
    }

    public function canSubmit(User $user, Practice $practice): bool
    {
        $node = $practice->node;

        return $this->isUnlocked($user, $node) && $this->hasActiveSubscription($user, $node->course);
    }

    /** Completó todos los nodos publicados del tronco (los extras y las Sendas no cuentan). */
    public function isCourseCompleted(User $user, Course $course): bool
    {
        $nodes = $course->nodes()->where('is_published', true)->trunk()->get();

        return $nodes->isNotEmpty() && $nodes->every(fn (Node $node) => $this->isCompleted($user, $node));
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
