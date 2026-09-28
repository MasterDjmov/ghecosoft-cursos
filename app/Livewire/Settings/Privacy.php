<?php

namespace App\Livewire\Settings;

use App\Enums\AuthorizationStatus;
use App\Enums\RankingDisplay;
use App\Models\User;
use App\Notifications\PlatformNotification;
use App\Rules\SafeUpload;
use App\Services\Ranking;
use Flux\Flux;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;
use Livewire\Attributes\Title;
use Livewire\Component;
use Livewire\Features\SupportFileUploads\TemporaryUploadedFile;
use Livewire\WithFileUploads;

/** Mi cuenta → Privacidad: CV público, nombre o apodo, y autorización de menores. */
#[Title('Privacidad')]
class Privacy extends Component
{
    use WithFileUploads;

    public bool $cv_public = false;

    public string $ranking_display = 'name';

    public string $nickname = '';

    /** @var TemporaryUploadedFile|null */
    public $authorization = null;

    public function mount(): void
    {
        $user = auth()->user();
        $this->cv_public = $user->cv_public;
        $this->ranking_display = $user->ranking_display->value;
        $this->nickname = (string) $user->nickname;
    }

    public function save(): void
    {
        $user = auth()->user();

        $this->validate([
            'cv_public' => ['boolean'],
            'ranking_display' => ['required', Rule::enum(RankingDisplay::class)],
            'nickname' => [Rule::requiredIf($this->ranking_display === 'nickname'), 'nullable', 'string', 'min:3', 'max:30', 'regex:/^[\pL\pN _.-]+$/u'],
        ], ['nickname.required' => 'Elegí un apodo para usarlo en el ranking.'], ['nickname' => 'apodo']);

        if ($this->cv_public && ($blocker = $user->publicProfileBlocker())) {
            $this->addError('cv_public', $blocker);
            $this->cv_public = false;

            return;
        }

        $user->forceFill([
            'cv_public' => $this->cv_public,
            'ranking_display' => $this->ranking_display,
            'nickname' => $this->nickname ?: null,
        ])->save();

        Ranking::forget();
        foreach ($user->subscriptions()->pluck('course_id')->unique() as $courseId) {
            Cache::forget("ranking.course.{$courseId}");
        }

        Flux::toast(variant: 'success', text: 'Privacidad guardada.');
    }

    /** Link nuevo para el CV: el anterior deja de funcionar. */
    public function newCvLink(): void
    {
        auth()->user()->forceFill(['cv_slug' => User::newCvSlug(auth()->user())])->save();
        Ranking::forget();
        Flux::toast(variant: 'success', text: 'Listo: tu CV tiene un link nuevo y el anterior ya no funciona.');
    }

    /** Pedir (o dejar de pedir) un código de 6 cifras para ver el CV. */
    public function toggleCvCode(): void
    {
        $user = auth()->user();
        $user->forceFill(['cv_code' => $user->cv_code ? null : User::newCvCode()])->save();
        Flux::toast(variant: 'success', text: $user->cv_code ? 'Ahora tu CV pide un código. Pasalo junto con el link.' : 'Tu CV ya no pide código: lo ve quien tenga el link.');
    }

    /** Código nuevo: quien usó el anterior tiene que poner el nuevo. */
    public function newCvCode(): void
    {
        $user = auth()->user();
        if ($user->cv_code) {
            $user->forceFill(['cv_code' => User::newCvCode()])->save();
            Flux::toast(variant: 'success', text: 'Código nuevo. El anterior ya no sirve.');
        }
    }

    public function uploadAuthorization(): void
    {
        $user = auth()->user();

        $this->validate([
            'authorization' => ['required', 'file', 'extensions:'.implode(',', config('uploads.receipt.mimes')), 'mimes:'.implode(',', config('uploads.receipt.mimes')), new SafeUpload, 'max:'.config('uploads.receipt.max_kb')],
        ], [], ['authorization' => 'autorización']);

        if ($user->guardianAuthorizations()->where('status', AuthorizationStatus::Pending)->exists()) {
            $this->addError('authorization', 'Ya mandaste una autorización: esperá que el profe la revise.');

            return;
        }

        $user->guardianAuthorizations()->create([
            'file_path' => $this->authorization->storeAs('authorizations', Str::uuid().'.'.Str::lower($this->authorization->getClientOriginalExtension()), 'local'),
            'original_name' => Str::limit($this->authorization->getClientOriginalName(), 250, ''),
        ]);

        PlatformNotification::toAdmins(new PlatformNotification(
            'authorization.new', 'Autorización de menor: '.$user->fullName(), 'Subió la nota firmada para revisar.',
            route('admin.authorizations'), 'document-check',
        ));

        $this->reset('authorization');
        Flux::toast(variant: 'success', text: 'Listo: el profe la va a revisar.');
    }

    public function render()
    {
        $user = auth()->user();

        return view('livewire.settings.privacy', [
            'blocker' => $user->publicProfileBlocker(),
            'isMinor' => $user->isMinor(),
            'authorizations' => $user->guardianAuthorizations()->latest()->get(),
            'hasApproved' => $user->hasApprovedGuardianAuthorization(),
            'cvUrl' => route('cv.show', $user->cv_slug),
            'cvCode' => $user->cv_code,
        ]);
    }
}
