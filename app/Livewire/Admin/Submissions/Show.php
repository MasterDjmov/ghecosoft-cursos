<?php

namespace App\Livewire\Admin\Submissions;

use App\Enums\SubmissionStatus;
use App\Models\Submission;
use App\Services\SubmissionReviewer;
use App\Support\Markdown;
use DomainException;
use Flux\Flux;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Corregir una entrega: ver y ejecutar el código, Aprobar o Rehacer, y el hilo. */
#[Title('Corregir entrega')]
class Show extends Component
{
    public Submission $submission;

    public string $comment = '';

    public string $reply = '';

    /** "Corregir la más vieja": la primera sin corregir de la bandeja. */
    public static function nextPending(?int $exceptId = null): ?Submission
    {
        return Submission::where('status', SubmissionStatus::Submitted)
            ->when($exceptId, fn ($q) => $q->whereKeyNot($exceptId))
            ->oldest('submitted_at')
            ->first();
    }

    public function approve(SubmissionReviewer $reviewer)
    {
        $this->validate(['comment' => ['nullable', 'string', 'max:2000']]);

        try {
            $reward = $reviewer->approve($this->submission, auth()->user(), $this->comment ?: null);
        } catch (DomainException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());

            return null;
        }

        Flux::toast(variant: 'success', text: 'Aprobada. '.$reward->summary());

        return $this->goToNext();
    }

    public function redo(SubmissionReviewer $reviewer)
    {
        $this->validate(
            ['comment' => ['required', 'string', 'max:2000']],
            ['comment.required' => 'Contale qué tiene que corregir.'],
            ['comment' => 'comentario'],
        );

        try {
            $reviewer->redo($this->submission, auth()->user(), $this->comment);
        } catch (DomainException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());

            return null;
        }

        Flux::toast(text: 'Marcada para rehacer.');

        return $this->goToNext();
    }

    public function addReply(SubmissionReviewer $reviewer): void
    {
        $this->validate(['reply' => ['required', 'string', 'max:2000']], [], ['reply' => 'comentario']);
        $reviewer->comment($this->submission, auth()->user(), $this->reply);
        $this->reset('reply');
    }

    private function goToNext()
    {
        $next = self::nextPending($this->submission->id);

        return $next
            ? $this->redirectRoute('admin.submissions.show', $next, navigate: true)
            : $this->redirectRoute('admin.submissions.index', navigate: true);
    }

    public function render()
    {
        $submission = $this->submission->load(['user', 'practice.node.course', 'comments.user:id,name,last_name,role', 'reviewer:id,name']);
        $practice = $submission->practice;

        return view('livewire.admin.submissions.show', [
            'practice' => $practice,
            'node' => $practice->node,
            'course' => $practice->node->course,
            'instructionsHtml' => Markdown::render($practice->instructions),
            'criteriaHtml' => Markdown::render($practice->approval_criteria),
            'previous' => Submission::where('user_id', $submission->user_id)->where('practice_id', $practice->id)
                ->whereKeyNot($submission->id)->orderByDesc('attempt')->get(),
            'pendingCount' => Submission::where('status', SubmissionStatus::Submitted)->count(),
        ])->title('Corregir · '.$practice->title);
    }
}
