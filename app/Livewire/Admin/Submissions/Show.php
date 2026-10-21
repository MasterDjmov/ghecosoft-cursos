<?php

namespace App\Livewire\Admin\Submissions;

use App\Enums\SubmissionStatus;
use App\Models\ReviewSnippet;
use App\Models\Submission;
use App\Services\SubmissionReviewer;
use App\Services\TeacherScope;
use App\Support\Markdown;
use App\Support\SubmissionCases;
use DomainException;
use Flux\Flux;
use Livewire\Attributes\Renderless;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Corregir una entrega: ver y ejecutar el código, Aprobar o Rehacer, y el hilo. */
#[Title('Corregir entrega')]
class Show extends Component
{
    public Submission $submission;

    public string $comment = '';

    public string $reply = '';

    /** Al guardar el comentario como frecuente: para todos sus cursos o solo para el de esta entrega (D73). */
    public bool $snippetForAll = false;

    /** "Corregir la más vieja": la primera sin corregir de la bandeja (del docente: de sus comisiones, D72). */
    public static function nextPending(?int $exceptId = null): ?Submission
    {
        return app(TeacherScope::class)->submissions(Submission::query(), auth()->user())
            ->where('status', SubmissionStatus::Submitted)
            ->when($exceptId, fn ($q) => $q->whereKeyNot($exceptId))
            ->oldest('submitted_at')
            ->first();
    }

    public function mount(): void
    {
        $this->authorize('review', $this->submission);
    }

    public function approve(SubmissionReviewer $reviewer)
    {
        $this->authorize('review', $this->submission);
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

    /** La marcaste para rehacer por error: se aprueba igual, sin que el alumno vuelva a entregar (D82). */
    public function approveAnyway(SubmissionReviewer $reviewer)
    {
        $this->authorize('review', $this->submission);
        $this->validate(['comment' => ['nullable', 'string', 'max:2000']]);

        try {
            $reward = $reviewer->approve($this->submission, auth()->user(), $this->comment ?: null, reconsider: true);
        } catch (DomainException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());

            return null;
        }

        $this->reset('comment');
        Flux::toast(variant: 'success', text: 'Aprobada. '.$reward->summary());

        return null;
    }

    public function redo(SubmissionReviewer $reviewer)
    {
        $this->authorize('review', $this->submission);
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
        $this->authorize('review', $this->submission);
        $this->validate(['reply' => ['required', 'string', 'max:2000']], [], ['reply' => 'comentario']);
        $reviewer->comment($this->submission, auth()->user(), $this->reply);
        $this->reset('reply');
    }

    /** Lo que dieron las pruebas en el navegador de quien corrige (D73): una ayuda para la bandeja. */
    #[Renderless]
    public function saveCheck(int $passed, int $total): void
    {
        $this->authorize('review', $this->submission);
        SubmissionCases::store($this->submission, $passed, $total);
    }

    private function goToNext()
    {
        $next = self::nextPending($this->submission->id);

        return $next
            ? $this->redirectRoute('admin.submissions.show', $next, navigate: true)
            : $this->redirectRoute('admin.submissions.index', navigate: true);
    }

    /** D73: guarda el comentario escrito entre los frecuentes de quien corrige. */
    public function saveSnippet(): void
    {
        $this->authorize('review', $this->submission);
        $this->validate(['comment' => ['required', 'string', 'max:2000']], ['comment.required' => 'Escribí el comentario que querés guardar.']);
        $user = auth()->user();
        $body = trim($this->comment);
        $courseId = $this->snippetForAll ? null : $this->submission->practice->node->course_id;

        if (ReviewSnippet::where('user_id', $user->id)->where('course_id', $courseId)->where('body', $body)->exists()) {
            Flux::toast(text: 'Ese comentario ya lo tenías guardado.');

            return;
        }
        ReviewSnippet::create([
            'user_id' => $user->id,
            'course_id' => $courseId,
            'body' => $body,
            'position' => (int) ReviewSnippet::where('user_id', $user->id)->max('position') + 1,
        ]);
        Flux::toast(variant: 'success', text: 'Comentario guardado.');
    }

    /** Solo los propios: un docente nunca toca los comentarios de otro. */
    public function deleteSnippet(int $snippetId): void
    {
        ReviewSnippet::where('user_id', auth()->id())->whereKey($snippetId)->delete();
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
            'cases' => SubmissionCases::for($submission),
            'canApproveAnyway' => $submission->status === SubmissionStatus::Redo && SubmissionReviewer::isLatestAttempt($submission),
            'previous' => Submission::where('user_id', $submission->user_id)->where('practice_id', $practice->id)
                ->whereKeyNot($submission->id)->orderByDesc('attempt')->get(),
            'snippets' => ReviewSnippet::for(auth()->user(), $practice->node->course_id)->get(['id', 'course_id', 'body']),
            'pendingCount' => app(TeacherScope::class)->submissions(Submission::query(), auth()->user())->where('status', SubmissionStatus::Submitted)->count(),
        ])->title('Corregir · '.$practice->title);
    }
}
