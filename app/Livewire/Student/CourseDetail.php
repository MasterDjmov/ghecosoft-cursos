<?php

namespace App\Livewire\Student;

use App\Enums\RequestType;
use App\Exceptions\NodeLocked;
use App\Models\Course;
use App\Models\Currency;
use App\Models\EnrollmentRequest;
use App\Rules\SafeUpload;
use App\Services\EnrollmentRequester;
use App\Services\Ledger;
use App\Services\NodeUnlocker;
use App\Services\TreeAccess;
use App\Support\Markdown;
use App\Support\Story;
use App\Support\UnlockMessages;
use DomainException;
use Flux\Flux;
use Illuminate\Support\Facades\RateLimiter;
use Livewire\Attributes\Title;
use Livewire\Component;
use Livewire\Features\SupportFileUploads\TemporaryUploadedFile;
use Livewire\WithFileUploads;

/** Ficha de un curso: descripción, inscripción o renovación, y "Abrir el curso". */
#[Title('Curso')]
class CourseDetail extends Component
{
    use WithFileUploads;

    public Course $course;

    /** @var TemporaryUploadedFile|null */
    public $receipt = null;

    public string $message = '';

    public ?int $cohortId = null;

    public function mount(Course $course): void
    {
        $this->authorize('view', $course);
    }

    public function sendReceipt(EnrollmentRequester $requester): void
    {
        $this->validate([
            'receipt' => ['required', 'file', 'extensions:'.implode(',', config('uploads.receipt.mimes')), 'mimes:'.implode(',', config('uploads.receipt.mimes')), new SafeUpload, 'max:'.config('uploads.receipt.max_kb')],
            'message' => ['nullable', 'string', 'max:1000'],
        ], ['receipt.required' => 'Adjuntá el comprobante (foto o PDF).'], ['receipt' => 'comprobante', 'message' => 'mensaje']);

        $this->submit($requester, RequestType::Receipt);
    }

    /** "Contactar al profe": deja la solicitud registrada y abre WhatsApp. */
    public function contact(EnrollmentRequester $requester): void
    {
        $this->validate(['message' => ['nullable', 'string', 'max:1000']]);

        if ($this->submit($requester, RequestType::Contact) && ($url = $requester->whatsappUrl(auth()->user(), $this->course, $requester->pending(auth()->user(), $this->course)->kind))) {
            $this->js('window.open('.json_encode($url).', "_blank", "noopener")');
        }
    }

    private function submit(EnrollmentRequester $requester, RequestType $type): bool
    {
        $key = 'enrollment-request:'.auth()->id();
        if (RateLimiter::tooManyAttempts($key, 5)) {
            Flux::toast(variant: 'danger', text: 'Demasiados intentos. Probá de nuevo en unos minutos.');

            return false;
        }
        RateLimiter::hit($key, 600);

        try {
            $requester->request(auth()->user(), $this->course, $type, $this->receipt, $this->message ?: null, $this->cohortId);
        } catch (DomainException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());

            return false;
        }

        $this->reset('receipt', 'message');
        Flux::modal('request')->close();
        Flux::toast(variant: 'success', text: 'Listo: tu solicitud le llegó al profe. Te avisamos cuando la apruebe.');

        return true;
    }

    public function openCourse(NodeUnlocker $unlocker)
    {
        $root = $this->course->rootNode;
        abort_unless($root !== null, 404);

        try {
            $unlocker->unlock(auth()->user(), $root);
        } catch (NodeLocked $e) {
            Flux::toast(variant: 'danger', text: implode(' ', UnlockMessages::for(auth()->user(), $root, $e->reasons)));

            return null;
        }

        Flux::toast(variant: 'success', text: '¡Entraste a '.$this->course->title.'! Empezá por la clase 0.');

        return $this->redirectRoute('student.node', [$this->course, $root], navigate: true);
    }

    public function render(TreeAccess $access, EnrollmentRequester $requester, Ledger $ledger)
    {
        $user = auth()->user();
        $subscription = $access->activeSubscription($user, $this->course);
        $rootOpen = $access->isRootOpen($user, $this->course);
        $pending = $requester->pending($user, $this->course);
        $kind = $requester->kindFor($user, $this->course);

        return view('livewire.student.course-detail', [
            'intro' => Story::get('story.course_intro', $this->course, auth()->user()),
            'descriptionHtml' => Markdown::render($this->course->description),
            'subscription' => $subscription,
            'paidUntil' => $subscription ? $access->paidUntil($user, $this->course) : null,
            'lastSubscription' => $user->subscriptions()->where('course_id', $this->course->id)->orderByDesc('ends_at')->first(),
            'rootOpen' => $rootOpen,
            'pending' => $pending,
            'kind' => $kind,
            'balance' => $ledger->balance($user, Currency::forCourse($this->course)),
            'canOpen' => ! $rootOpen && $this->course->rootNode && $access->canUnlock($user, $this->course->rootNode),
            'canTry' => $access->canTryCourse($user, $this->course),
            'cohorts' => $this->course->cohorts()->where('is_open_for_enrollment', true)->get(),
            'history' => EnrollmentRequest::where('user_id', $user->id)->where('course_id', $this->course->id)
                ->where('status', '!=', 'pending')->latest()->limit(5)->get(),
            'whatsappAvailable' => $requester->whatsappUrl($user, $this->course, $kind) !== null,
            'nodeCount' => $this->course->nodes()->where('is_published', true)->count(),
        ])->title($this->course->title);
    }
}
