<?php

namespace App\Livewire;

use App\Models\NodeStep;
use App\Models\Practice;
use App\Models\PracticeMessage;
use App\Models\User;
use App\Services\PracticeMessenger;
use Flux\Flux;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Facades\RateLimiter;
use Livewire\Attributes\Locked;
use Livewire\Component;

/**
 * El hilo de consultas de un alumno sobre una práctica (D63) o una micro-misión (D110). Lo usan el alumno (modo
 * misión, tarjeta de la práctica y la micro-misión) y el docente (Admin → Mensajes). Se actualiza solo cada 20 s.
 * Si está adentro de un editor (codeRunner), el mensaje del alumno lleva la foto de su código y su salida.
 */
class PracticeChat extends Component
{
    #[Locked]
    public ?int $practiceId = null;

    #[Locked]
    public ?int $stepId = null;

    #[Locked]
    public int $studentId;

    public string $body = '';

    public function mount(User $student, ?Practice $practice = null, ?NodeStep $step = null): void
    {
        $subject = $practice ?? $step;
        abort_if($subject === null, 404);
        Gate::authorize('viewThread', [PracticeMessage::class, $subject, $student]);
        $this->practiceId = $practice?->id;
        $this->stepId = $practice ? null : $step->id;
        $this->studentId = $student->id;
    }

    public function send(PracticeMessenger $messenger, ?string $code = null, ?string $output = null): void
    {
        [$practice, $student] = $this->thread();
        Gate::authorize('send', [PracticeMessage::class, $practice, $student]);

        $this->validate(['body' => ['required', 'string', 'max:2000']], [
            'body.required' => 'Escribí tu mensaje.',
            'body.max' => 'El mensaje tiene hasta 2000 letras.',
        ]);

        $key = 'practice-chat:'.auth()->id();
        if (RateLimiter::tooManyAttempts($key, 10)) {
            Flux::toast(variant: 'danger', text: 'Mandaste muchos mensajes seguidos. Esperá un minuto.');

            return;
        }
        RateLimiter::hit($key, 60);

        $messenger->send(auth()->user(), $practice, $student, $this->body, $code, $output);
        $this->reset('body');
        $this->dispatch('practice-chat-sent');
    }

    /** @return array{0: Practice|NodeStep, 1: User} */
    private function thread(): array
    {
        $subject = $this->practiceId
            ? Practice::with('node.course')->findOrFail($this->practiceId)
            : NodeStep::with('node.course')->findOrFail($this->stepId);

        return [$subject, User::findOrFail($this->studentId)];
    }

    public function placeholder(): string
    {
        return '<div class="text-sm text-ink-muted">Cargando la conversación…</div>';
    }

    public function render(PracticeMessenger $messenger)
    {
        [$practice, $student] = $this->thread();
        $viewer = auth()->user();
        Gate::authorize('viewThread', [PracticeMessage::class, $practice, $student]);
        $messenger->markRead($viewer, $practice, $student);

        return view('livewire.practice-chat', [
            'practice' => $practice,
            'isStep' => $practice instanceof NodeStep,
            'student' => $student,
            'viewer' => $viewer,
            'messages' => PracticeMessage::thread($practice, $student)->with('author:id,name,last_name,role')->oldest()->get(),
            'canSend' => Gate::allows('send', [PracticeMessage::class, $practice, $student]),
        ]);
    }
}
