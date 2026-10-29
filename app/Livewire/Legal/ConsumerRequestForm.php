<?php

namespace App\Livewire\Legal;

use App\Enums\ConsumerRequestKind;
use App\Models\ConsumerRequest;
use App\Notifications\PlatformNotification;
use Illuminate\Support\Facades\RateLimiter;
use Livewire\Attributes\Layout;
use Livewire\Attributes\Locked;
use Livewire\Component;

/**
 * D112: botón de arrepentimiento (Res. 424/2020) y botón de baja (Res. 316/2018). Se piden sin entrar a la
 * cuenta y dan el código de trámite en el momento; el administrador los resuelve en Admin → Arrepentimientos.
 */
#[Layout('layouts::legal')]
class ConsumerRequestForm extends Component
{
    #[Locked]
    public string $kind = 'withdrawal';

    public string $name = '';

    public string $contact = '';

    public string $course = '';

    public string $details = '';

    public ?string $code = null;

    public function mount(?string $kind = null): void
    {
        $this->kind = (ConsumerRequestKind::tryFrom((string) $kind)
            ?? (request()->routeIs('legal.cancellation') ? ConsumerRequestKind::Cancellation : ConsumerRequestKind::Withdrawal))->value;

        if ($user = auth()->user()) {
            $this->name = $user->fullName();
            $this->contact = (string) ($user->email ?? $user->phone ?? '');
        }
    }

    public function send(): void
    {
        $data = $this->validate([
            'name' => ['required', 'string', 'max:120'],
            'contact' => ['required', 'string', 'max:120'],
            'course' => ['nullable', 'string', 'max:120'],
            'details' => ['nullable', 'string', 'max:2000'],
        ], [], ['name' => 'nombre y apellido', 'contact' => 'email o teléfono', 'course' => 'curso', 'details' => 'detalle']);

        $key = 'consumer-request:'.request()->ip();
        if (RateLimiter::tooManyAttempts($key, 5)) {
            $this->addError('name', 'Demasiados pedidos seguidos. Probá de nuevo en un rato.');

            return;
        }
        RateLimiter::hit($key, 3600);

        $request = ConsumerRequest::create([
            ...$data,
            'kind' => ConsumerRequestKind::from($this->kind),
            'user_id' => auth()->id(),
        ]);

        PlatformNotification::toAdmins(new PlatformNotification(
            'consumer.'.$this->kind,
            'Pedido de '.mb_strtolower($request->kind->label()).' '.$request->code,
            $request->name.($request->course ? ' · '.$request->course : '').' · '.$request->contact,
            route('admin.consumer-requests'),
            'receipt-refund',
        ));

        $this->code = $request->code;
    }

    public function render()
    {
        $kind = ConsumerRequestKind::from($this->kind);

        return view('livewire.legal.consumer-request-form', ['kindEnum' => $kind])
            ->title($kind === ConsumerRequestKind::Withdrawal ? 'Botón de arrepentimiento' : 'Botón de baja');
    }
}
