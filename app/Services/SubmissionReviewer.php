<?php

namespace App\Services;

use App\Enums\CoinReason;
use App\Enums\SubmissionStatus;
use App\Enums\XpReason;
use App\Models\Course;
use App\Models\CourseCompletion;
use App\Models\CourseSubscription;
use App\Models\Currency;
use App\Models\Level;
use App\Models\Node;
use App\Models\Submission;
use App\Models\SubmissionComment;
use App\Models\User;
use App\Models\XpTransaction;
use App\Notifications\PlatformNotification;
use App\Support\Reward;
use App\Support\Story;
use DomainException;
use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\DB;

/**
 * Corrección de entregas: Aprobada o Rehacer (sin notas).
 * El **primer** aprobado de una práctica paga moneda y XP (una sola vez), y
 * revisa si con eso se completó el nodo o se venció al jefe (G7).
 */
class SubmissionReviewer
{
    public function __construct(private readonly Ledger $ledger, private readonly TreeAccess $access) {}

    /**
     * Con `$reconsider`, también una entrega marcada para rehacer por error (D82): solo si es la última
     * del alumno en esa práctica. Se paga igual que siempre, y nunca dos veces.
     */
    public function approve(Submission $submission, ?User $admin, ?string $comment = null, bool $notify = true, bool $reconsider = false): Reward
    {
        $reward = DB::transaction(function () use ($submission, $admin, $comment, $reconsider) {
            $submission = Submission::whereKey($submission->id)->lockForUpdate()->firstOrFail();
            $canReconsider = $reconsider && $submission->status === SubmissionStatus::Redo && self::isLatestAttempt($submission);
            if ($submission->status !== SubmissionStatus::Submitted && ! $canReconsider) {
                throw new DomainException($reconsider ? 'Solo se puede aprobar la última entrega marcada para rehacer.' : 'Esta entrega ya fue corregida.');
            }

            $student = $submission->user;
            $practice = $submission->practice;
            $node = $practice->node;
            $course = $node->course;
            $levelBefore = Level::forXp($student->fresh()->xp_total)?->number;
            $wasCompleted = $this->access->requiredPracticesApproved($student, $node);

            // ¿Ya tenía otra entrega aprobada de esta práctica? Entonces no se paga de nuevo.
            $alreadyPaid = Submission::where('user_id', $student->id)
                ->where('practice_id', $practice->id)
                ->where('status', SubmissionStatus::Approved)
                ->exists();

            $submission->forceFill([
                'status' => SubmissionStatus::Approved,
                'reviewed_at' => now(),
                'reviewed_by' => $admin?->id,
            ])->save();

            if ($comment) {
                $submission->comments()->create(['user_id' => $admin->id, 'body' => $comment]);
            }

            $reward = new Reward;

            if (! $alreadyPaid) {
                if ($practice->coin_reward > 0) {
                    $currency = $practice->is_required ? Currency::forCourse($course) : Currency::wildcard();
                    $this->ledger->credit($student, $currency, $practice->coin_reward, CoinReason::PracticeApproved, $submission, $course, by: $admin);
                    $reward->coins = $practice->coin_reward;
                    $reward->coinName = $practice->is_required
                        ? term('coin.course', $course, $practice->coin_reward)
                        : term('coin.wildcard', null, $practice->coin_reward);
                }
                if ($practice->xp_reward > 0) {
                    $this->ledger->addXp($student, $practice->xp_reward, XpReason::PracticeApproved, $submission, $course, by: $admin);
                    $reward->xp += $practice->xp_reward;
                }
            }

            if ($practice->is_required && ! $wasCompleted && $this->access->requiredPracticesApproved($student, $node)) {
                $this->completeNode($student, $node, $admin, $reward);
            }

            $levelAfter = Level::forXp($student->fresh()->xp_total)?->number;
            if ($levelAfter && $levelAfter !== $levelBefore) {
                $reward->newLevel = $levelAfter;
            }

            return $reward;
        });

        if ($notify && $admin) {
            $this->notifyStudent($submission->fresh(), 'approved', '¡Aprobada! '.$reward->summary());
        }
        $this->tellStory($submission->user, $submission->practice->node->course, $reward);

        return $reward;
    }

    public function redo(Submission $submission, User $admin, string $comment): void
    {
        DB::transaction(function () use ($submission, $admin, $comment) {
            $submission = Submission::whereKey($submission->id)->lockForUpdate()->firstOrFail();
            if ($submission->status !== SubmissionStatus::Submitted) {
                throw new DomainException('Esta entrega ya fue corregida.');
            }

            $submission->forceFill([
                'status' => SubmissionStatus::Redo,
                'reviewed_at' => now(),
                'reviewed_by' => $admin->id,
            ])->save();

            $submission->comments()->create(['user_id' => $admin->id, 'body' => $comment]);
        });

        $this->notifyStudent($submission->fresh(), 'redo', 'Hay que rehacerla: '.str($comment)->limit(120));
    }

    /** XP del nodo completo (una sola vez) y, si es jefe, su XP e insignia. */
    /**
     * Un nodo sin prácticas obligatorias queda completo apenas se abre (lo llama
     * NodeUnlocker): da su XP, la insignia si es jefe y, si era el último, cierra el curso.
     */
    public function completeWithoutPractices(User $student, Node $node): ?Reward
    {
        if (! $this->access->isCompleted($student, $node)) {
            return null;
        }

        $reward = new Reward;
        $this->completeNode($student, $node, null, $reward);
        $this->tellStory($student, $node->course, $reward);

        return $reward;
    }

    private function completeNode(User $student, Node $node, ?User $admin, Reward $reward): void
    {
        $paid = fn (XpReason $reason) => XpTransaction::where('user_id', $student->id)
            ->where('reason', $reason)
            ->where('source_type', $node->getMorphClass())
            ->where('source_id', $node->id)
            ->exists();

        $reward->nodeCompleted = true;

        if (! $paid(XpReason::NodeCompleted) && ($xp = (int) config('game.node_completed_xp')) > 0) {
            $this->ledger->addXp($student, $xp, XpReason::NodeCompleted, $node, $node->course, by: $admin);
            $reward->xp += $xp;
        }

        if ($node->isBoss()) {
            if (! $paid(XpReason::BossDefeated) && ($xp = (int) config('game.boss_defeated_xp')) > 0) {
                $this->ledger->addXp($student, $xp, XpReason::BossDefeated, $node, $node->course, by: $admin);
                $reward->xp += $xp;
            }
            if ($node->badge && ! $student->badges()->whereKey($node->badge_id)->exists()) {
                $student->badges()->attach($node->badge_id, ['awarded_at' => now()]);
                $reward->badge = $node->badge;
            }
        }

        // ¿Con este nodo quedó completa su rama? (para el aviso de historia)
        if ($node->branch) {
            $branchNodes = $node->branch->nodes()->where('is_published', true)->get();
            if ($branchNodes->every(fn (Node $n) => $this->access->isCompleted($student, $n))) {
                $reward->branch = $node->branch;
            }
        }

        // ¿Con este nodo terminó el curso? Se guardan los días de cursada (para el CV).
        $course = $node->course;
        if (! CourseCompletion::where('user_id', $student->id)->where('course_id', $course->id)->exists()
            && $this->access->isCourseCompleted($student, $course)) {
            $firstStart = CourseSubscription::where('user_id', $student->id)->where('course_id', $course->id)->min('starts_at');
            CourseCompletion::create([
                'user_id' => $student->id,
                'course_id' => $course->id,
                'completed_at' => now(),
                'days_taken' => $firstStart ? max(1, (int) ceil(Carbon::parse($firstStart)->diffInDays(now()))) : 0,
            ]);
            $reward->courseCompleted = true;
        }
    }

    /** Historia en pantalla (Fase 9): aviso al completar una rama o el curso, con el texto del diccionario. */
    private function tellStory(User $student, Course $course, Reward $reward): void
    {
        $stories = array_filter([
            $reward->branch ? ['story.branch_completed', '¡«'.$reward->branch->title.'» completada!', 'flag'] : null,
            $reward->courseCompleted ? ['story.course_completed', '¡Terminaste '.$course->title.'!', 'trophy'] : null,
        ]);

        foreach ($stories as [$key, $title, $icon]) {
            $story = Story::get($key, $course, $student, requireText: false);
            $student->notify(new PlatformNotification(
                kind: $key,
                title: $title,
                body: str($story['text'] ?: $story['title'])->limit(300)->toString(),
                url: route('student.tree', $course),
                icon: $icon,
            ));
        }
    }

    private function notifyStudent(Submission $submission, string $kind, string $body): void
    {
        $practice = $submission->practice;
        $node = $practice->node;

        $submission->user->notify(new PlatformNotification(
            kind: 'submission.'.$kind,
            title: ($kind === 'approved' ? 'Aprobada: ' : 'Rehacer: ').$practice->title,
            body: $body,
            url: route('student.node', [$node->course, $node]).'#practica-'.$practice->id,
            icon: $kind === 'approved' ? 'check-circle' : 'arrow-path',
        ));
    }

    /** Comentario en el hilo de una entrega (alumno o docente); avisa al otro lado. */
    public function comment(Submission $submission, User $author, string $body): SubmissionComment
    {
        $comment = $submission->comments()->create(['user_id' => $author->id, 'body' => trim($body)]);
        $practice = $submission->practice;
        $node = $practice->node;

        if ($author->isStaff()) {
            $submission->user->notify(new PlatformNotification(
                'comment', 'Comentario del profe: '.$practice->title, str($body)->limit(140),
                route('student.node', [$node->course, $node]).'#practica-'.$practice->id, 'chat-bubble-left-right',
            ));
        } else {
            PlatformNotification::toStaff(new PlatformNotification(
                'comment', $author->fullName().' comentó: '.$practice->title, str($body)->limit(140),
                route('admin.submissions.show', $submission), 'chat-bubble-left-right',
            ), $submission->user, $node->course);
        }

        return $comment;
    }

    /** ¿Es el último intento del alumno en esa práctica? (si mandó otro después, se corrige ese). */
    public static function isLatestAttempt(Submission $submission): bool
    {
        return ! Submission::where('user_id', $submission->user_id)->where('practice_id', $submission->practice_id)
            ->where('attempt', '>', $submission->attempt)->exists();
    }
}
