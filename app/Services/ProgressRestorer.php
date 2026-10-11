<?php

namespace App\Services;

use App\Enums\CoinReason;
use App\Enums\SubmissionMode;
use App\Enums\SubmissionStatus;
use App\Enums\XpReason;
use App\Models\Node;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\NodeUnlock;
use App\Models\Practice;
use App\Models\PracticeMark;
use App\Models\Submission;
use App\Models\User;
use App\Notifications\PlatformNotification;
use App\Support\UnlockMessages;
use DomainException;
use Illuminate\Support\Facades\DB;

/**
 * Restaurar el avance de un alumno a mano (D103): si se le reinició la cuenta o se le perdió el avance, el
 * administrador le abre nodos, le da por superadas micro-misiones y le aprueba prácticas desde su árbol.
 * Respeta el orden del árbol (el padre completo, los requisitos y el abono) y paga lo mismo que si lo hubiera
 * hecho él (monedas, XP, oro, ítems, insignias), una sola vez. El nodo se cobra si le alcanza; si no, se abre
 * sin cobrar, porque lo que se repone es avance que ya tenía.
 */
class ProgressRestorer
{
    public const NOTE = 'Aprobada por el profe al restaurar tu avance.';

    public function __construct(
        private readonly TreeAccess $access,
        private readonly Ledger $ledger,
        private readonly SubmissionReviewer $reviewer,
        private readonly Heroes $heroes,
        private readonly Inventory $inventory,
    ) {}

    /**
     * @return bool true si se cobró el precio; false si se abrió sin cobrar (o ya estaba abierto).
     *
     * @throws DomainException si el árbol todavía no lo deja abrir.
     */
    public function unlock(User $student, Node $node, User $admin): bool
    {
        if ($this->access->isUnlocked($student, $node)) {
            return false;
        }

        return DB::transaction(function () use ($student, $node, $admin) {
            User::whereKey($student->id)->lockForUpdate()->first();

            $blockers = array_diff($this->access->unlockBlockers($student, $node), [TreeAccess::BLOCK_INSUFFICIENT_FUNDS]);
            if ($blockers !== []) {
                throw new DomainException($this->blockerText($student, $node, $blockers));
            }

            $currency = $this->access->paymentCurrency($node);
            $charge = $node->price > 0 && $this->ledger->balance($student, $currency) >= $node->price;

            $unlock = NodeUnlock::create([
                'user_id' => $student->id,
                'node_id' => $node->id,
                'currency_id' => $currency->id,
                'price_paid' => $charge ? $node->price : 0,
                'unlocked_by' => $admin->id,
                'unlocked_at' => now(),
            ]);
            if ($charge) {
                $this->ledger->debit($student, $currency, $node->price, CoinReason::NodeUnlock, $unlock, $node->course, by: $admin);
            }
            if (! $node->practices()->where('is_required', true)->exists()) {
                $this->reviewer->completeWithoutPractices($student, $node);
            }

            return $charge;
        });
    }

    /** @return bool true si la dio por superada ahora; false si ya la tenía. */
    public function completeStep(User $student, NodeStep $step): bool
    {
        $this->ensureUnlocked($student, $step->node);

        return DB::transaction(function () use ($student, $step) {
            $completion = NodeStepCompletion::firstOrCreate(
                ['user_id' => $student->id, 'node_step_id' => $step->id],
                ['completed_at' => now()],
            );
            if (! $completion->wasRecentlyCreated) {
                return false;
            }
            if ($step->xp_reward > 0) {
                $this->ledger->addXp($student, $step->xp_reward, XpReason::StepCompleted, $step, $step->node->course);
            }
            $this->heroes->creditStep($student, $step);
            $this->inventory->creditStep($student, $step);

            return true;
        });
    }

    /**
     * Aprueba la práctica: la entrega que espera corrección o, si no hay, una entrega vacía a su nombre.
     *
     * @return bool true si la aprobó ahora; false si ya estaba aprobada.
     */
    public function approvePractice(User $student, Practice $practice, User $admin): bool
    {
        $this->ensureUnlocked($student, $practice->node);

        if (Submission::where('user_id', $student->id)->where('practice_id', $practice->id)->where('status', SubmissionStatus::Approved)->exists()) {
            return false;
        }

        DB::transaction(function () use ($student, $practice, $admin) {
            $submission = Submission::where('user_id', $student->id)->where('practice_id', $practice->id)
                ->where('status', SubmissionStatus::Submitted)->latest('attempt')->first()
                ?? Submission::create([
                    'practice_id' => $practice->id,
                    'user_id' => $student->id,
                    'attempt' => (int) Submission::where('user_id', $student->id)->where('practice_id', $practice->id)->max('attempt') + 1,
                    'submitted_at' => now(),
                ]);
            if ($practice->submission_mode === SubmissionMode::None) {
                PracticeMark::firstOrCreate(['user_id' => $student->id, 'practice_id' => $practice->id], ['completed_at' => now()]);
            }
            $this->reviewer->approve($submission, $admin, self::NOTE, notify: false);
        });

        return true;
    }

    /** El nodo entero: lo abre si hace falta, todas sus micro-misiones y sus prácticas obligatorias. Le avisa. */
    public function completeNode(User $student, Node $node, User $admin): void
    {
        $this->unlock($student, $node, $admin);
        foreach ($node->steps as $step) {
            $this->completeStep($student, $step);
        }
        foreach ($node->practices->where('is_required', true) as $practice) {
            $this->approvePractice($student, $practice, $admin);
        }

        $student->notify(new PlatformNotification(
            kind: 'progress_restored',
            title: 'Recuperaste «'.$node->title.'»',
            body: 'El profe te restauró el avance de «'.$node->title.'»: ya lo tenés aprobado.',
            url: route('student.node', [$node->course, $node]),
            icon: 'arrow-path',
        ));
    }

    private function ensureUnlocked(User $student, Node $node): void
    {
        if (! $this->access->isUnlocked($student, $node)) {
            throw new DomainException('Primero abrile «'.$node->title.'».');
        }
    }

    /** @param list<string> $blockers */
    private function blockerText(User $student, Node $node, array $blockers): string
    {
        return implode(' ', UnlockMessages::for($student, $node, array_values($blockers)));
    }
}
