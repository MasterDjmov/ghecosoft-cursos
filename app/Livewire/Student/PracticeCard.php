<?php

namespace App\Livewire\Student;

use App\Enums\PracticeEnvironment;
use App\Enums\SubmissionMode;
use App\Models\Practice;
use App\Models\PracticeMark;
use App\Models\Submission;
use App\Services\PracticeSubmitter;
use App\Services\SubmissionReviewer;
use App\Support\Narrative;
use DomainException;
use Flux\Flux;
use Illuminate\Support\Facades\RateLimiter;
use Livewire\Component;
use Livewire\Features\SupportFileUploads\TemporaryUploadedFile;
use Livewire\WithFileUploads;

/** Una hoja dentro del nodo: consigna, editor, entregar, historial y comentarios. */
class PracticeCard extends Component
{
    use WithFileUploads;

    public Practice $practice;

    /** Número de la hoja dentro del nodo (para el nombre del archivo: practica_N.py). */
    public int $number = 1;

    /** @var TemporaryUploadedFile|null */
    public $file = null;

    public string $comment = '';

    public function mount(Practice $practice): void
    {
        // El componente vive dentro de NodeView, que ya autorizó el nodo; igual se revisa.
        $this->authorize('view', $practice->node);
    }

    public function submit(PracticeSubmitter $submitter, ?string $code = null): void
    {
        $this->authorize('view', $this->practice->node);

        if ($this->tooMany('submit', 10)) {
            return;
        }

        $extensions = $this->practice->allowed_extensions ?: 'py,txt,zip,pdf';
        $this->validate([
            'file' => ['nullable', 'file', 'extensions:'.$extensions, 'max:'.config('uploads.submission.max_kb')],
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
        Flux::toast(variant: 'success', text: '¡Entregado! Te avisamos cuando el profe la corrija.');
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

    public function render(PracticeSubmitter $submitter)
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

        return view('livewire.student.practice-card', [
            'course' => $course,
            'instructionsHtml' => Narrative::render($this->practice->instructions, $course, $user),
            'criteriaHtml' => Narrative::render($this->practice->approval_criteria, $course, $user),
            'isLocal' => $this->practice->environment === PracticeEnvironment::Local,
            'attempts' => $attempts,
            'latest' => $latest,
            'status' => $approved ? 'approved' : $latest?->status->value,
            'blocker' => $submitter->blocker($user, $this->practice),
            'marked' => PracticeMark::where('user_id', $user->id)->where('practice_id', $this->practice->id)->exists(),
            'mode' => $this->practice->submission_mode,
            'usesCode' => in_array($this->practice->submission_mode, [SubmissionMode::Code, SubmissionMode::Both], true),
            'usesFile' => in_array($this->practice->submission_mode, [SubmissionMode::File, SubmissionMode::Both], true),
            // Arranca con lo último que entregó (para rehacer) o con el código inicial.
            // Última devolución del docente, para la vista previa de la fila contraída.
            'lastFeedback' => $attempts->flatMap->comments->filter(fn ($c) => $c->user->isAdmin())->sortByDesc('created_at')->first(),
            'startingCode' => $latest?->code ?? (string) $this->practice->starter_code,
        ]);
    }
}
