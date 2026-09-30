<?php

namespace App\Livewire\Student\Concerns;

use App\Enums\PracticeEnvironment;
use App\Enums\SubmissionMode;
use App\Models\PracticeMark;
use App\Models\PracticeMessage;
use App\Models\Submission;
use App\Rules\SafeUpload;
use App\Services\PracticeSubmitter;
use App\Services\SubmissionReviewer;
use App\Support\Narrative;
use App\Support\ReviewHours;
use DomainException;
use Flux\Flux;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Entregar, marcar y comentar una práctica, y los datos para dibujarla.
 * Lo comparten la tarjeta del nodo (PracticeCard) y el modo misión (Mission).
 * Quien lo usa declara `Practice $practice`, `$file` y `string $comment` (y WithFileUploads).
 */
trait WorksOnPractice
{
    public function submit(PracticeSubmitter $submitter, ?string $code = null): void
    {
        $this->authorize('view', $this->practice->node);

        if ($this->tooMany('submit', 10)) {
            return;
        }

        $extensions = $this->practice->allowed_extensions ?: 'py,txt,zip,pdf';
        $this->validate([
            'file' => ['nullable', 'file', 'extensions:'.$extensions, new SafeUpload, 'max:'.config('uploads.submission.max_kb')],
        ], [], ['file' => 'archivo']);

        if ($code !== null && mb_strlen($code) > 100_000) {
            Flux::toast(variant: 'danger', text: 'El código es demasiado largo.');

            return;
        }

        try {
            $submitter->submit(auth()->user(), $this->practice, $code, $this->file);
        } catch (DomainException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());

            return;
        }

        $this->reset('file');
        $this->dispatch('practice-updated');
        Flux::toast(variant: 'success', text: '¡Entregado! '.(ReviewHours::notice(now()) ?? 'Te avisamos cuando el profe la corrija.'));
    }

    public function toggleMark(PracticeSubmitter $submitter): void
    {
        $this->authorize('view', $this->practice->node);

        try {
            $reward = $submitter->toggleMark(auth()->user(), $this->practice);
        } catch (DomainException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());

            return;
        }

        if ($reward) {
            $summary = $reward->summary();
            Flux::toast(variant: 'success', text: '¡Completada!'.($summary ? ' '.$summary : ''));
            $this->dispatch('practice-approved');
        }
    }

    public function addComment(int $submissionId, SubmissionReviewer $reviewer): void
    {
        $submission = Submission::where('practice_id', $this->practice->id)->findOrFail($submissionId);
        $this->authorize('comment', $submission);

        $this->validate(['comment' => ['required', 'string', 'max:2000']], [], ['comment' => 'comentario']);
        if ($this->tooMany('comment', 10)) {
            return;
        }

        $reviewer->comment($submission, auth()->user(), $this->comment);
        $this->reset('comment');
    }

    private function tooMany(string $action, int $perMinute): bool
    {
        $key = "{$action}:".auth()->id();
        if (RateLimiter::tooManyAttempts($key, $perMinute)) {
            Flux::toast(variant: 'danger', text: 'Demasiados intentos seguidos. Esperá un minuto.');

            return true;
        }
        RateLimiter::hit($key, 60);

        return false;
    }

    /** Estado de la práctica para el alumno: intentos, devolución, si puede entregar, código de arranque. */
    protected function practiceState(PracticeSubmitter $submitter): array
    {
        $user = auth()->user();
        $attempts = Submission::with(['comments.user:id,name,last_name,role'])
            ->where('user_id', $user->id)
            ->where('practice_id', $this->practice->id)
            ->orderByDesc('attempt')
            ->get();

        $approved = $attempts->contains(fn ($s) => $s->status->value === 'approved');
        $latest = $attempts->first();
        $course = $this->practice->node->course;

        return [
            'course' => $course,
            'instructionsHtml' => Narrative::render($this->practice->instructions, $course, $user),
            'criteriaHtml' => Narrative::render($this->practice->approval_criteria, $course, $user),
            'isLocal' => $this->practice->environment === PracticeEnvironment::Local,
            'attempts' => $attempts,
            'latest' => $latest,
            'status' => $approved ? 'approved' : $latest?->status->value,
            'messageCount' => PracticeMessage::thread($this->practice, $user)->count(),
            'unreadMessages' => PracticeMessage::thread($this->practice, $user)->unreadFor($user)->count(),
            // Si la última entrega espera corrección y llegó fuera de horario: cuándo se revisa.
            'reviewNotice' => ! $approved && $latest?->status->value === 'submitted' ? ReviewHours::notice($latest->submitted_at) : null,
            'blocker' => $submitter->blocker($user, $this->practice),
            'marked' => PracticeMark::where('user_id', $user->id)->where('practice_id', $this->practice->id)->exists(),
            'mode' => $this->practice->submission_mode,
            'usesCode' => in_array($this->practice->submission_mode, [SubmissionMode::Code, SubmissionMode::Both], true),
            'usesFile' => in_array($this->practice->submission_mode, [SubmissionMode::File, SubmissionMode::Both], true),
            // Última devolución del docente (vista previa de la fila contraída y columna de la misión).
            'lastFeedback' => $attempts->flatMap->comments->filter(fn ($c) => $c->user->isAdmin())->sortByDesc('created_at')->first(),
            // Arranca con lo último que entregó (para rehacer) o con el código inicial.
            'startingCode' => $latest?->code ?? (string) $this->practice->starter_code,
        ];
    }
}
