<?php

namespace App\Livewire;

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
 * El hilo de consultas de un alumno sobre una práctica (D63). Lo usan el alumno (modo misión y
 * tarjeta de la práctica) y el docente (Admin → Mensajes). Se actualiza solo cada 20 s.
 */
class PracticeChat extends Component
{
    #[Locked]
    public int $practiceId;

    #[Locked]
    public int $studentId;

    public string $body = '';

    public function mount(Practice $practice, User $student): void
    {
        Gate::authorize('viewThread', [PracticeMessage::class, $practice, $student]);
        $this->practiceId = $practice->id;
        $this->studentId = $student->id;
    }

    public function send(PracticeMessenger $messenger): void
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

        $messenger->send(auth()->user(), $practice, $student, $this->body);
        $this->reset('body');
        $this->dispatch('practice-chat-sent');
    }

    /** @return array{0: Practice, 1: User} */
    private function thread(): array
    {
        return [Practice::with('node.course')->findOrFail($this->practiceId), User::findOrFail($this->studentId)];
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
            'student' => $student,
            'viewer' => $viewer,
            'messages' => PracticeMessage::thread($practice, $student)->with('author:id,name,last_name,role')->oldest()->get(),
            'canSend' => Gate::allows('send', [PracticeMessage::class, $practice, $student]),
        ]);
    }
}
