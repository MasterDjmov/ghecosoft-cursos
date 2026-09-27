<?php

namespace App\Livewire\Admin;

use App\Enums\AuthorizationStatus;
use App\Models\GuardianAuthorization;
use App\Notifications\PlatformNotification;
use App\Services\Ranking;
use Flux\Flux;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;

/** Autorizaciones de menores: el docente revisa la nota firmada y la aprueba o la rechaza. */
#[Title('Autorizaciones')]
class Authorizations extends Component
{
    #[Url(as: 'estado', except: 'pending')]
    public string $status = 'pending';

    /** @var array<int, string> */
    public array $notes = [];

    public function review(int $id, string $decision): void
    {
        $authorization = GuardianAuthorization::where('status', AuthorizationStatus::Pending)->findOrFail($id);
        $approve = $decision === 'approve';
        $note = trim($this->notes[$id] ?? '');
        $this->resetErrorBag("notes.{$id}");

        if (! $approve && $note === '') {
            $this->addError("notes.{$id}", 'Escribí el motivo (por ejemplo, falta una firma).');

            return;
        }

        $authorization->forceFill([
            'status' => $approve ? AuthorizationStatus::Approved : AuthorizationStatus::Rejected,
            'admin_note' => $note ?: null,
            'reviewed_at' => now(),
            'reviewed_by' => auth()->id(),
        ])->save();

        Ranking::forget();

        $authorization->user->notify(new PlatformNotification(
            'authorization.'.($approve ? 'approved' : 'rejected'),
            $approve ? 'Autorización aprobada' : 'Autorización rechazada',
            $approve ? 'Ya podés activar tu CV público en Privacidad.' : $note,
            route('privacy'),
            $approve ? 'check-circle' : 'x-circle',
        ));

        unset($this->notes[$id]);
        Flux::toast(variant: 'success', text: $approve ? 'Autorización aprobada.' : 'Autorización rechazada.');
    }

    public function render()
    {
        return view('livewire.admin.authorizations', [
            'authorizations' => GuardianAuthorization::with(['user', 'reviewer:id,name'])
                ->when($this->status !== 'all', fn ($q) => $q->where('status', $this->status))
                ->latest()->get(),
        ]);
    }
}
