<?php

namespace App\Livewire\Admin;

use App\Enums\ConsumerRequestStatus;
use App\Models\ConsumerRequest;
use Flux\Flux;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;

/** D112: pedidos de arrepentimiento y de baja; el administrador devuelve o da de baja y lo marca resuelto. */
#[Title('Arrepentimientos y bajas')]
class ConsumerRequests extends Component
{
    #[Url(as: 'estado', except: 'pending')]
    public string $status = 'pending';

    /** @var array<int, string> */
    public array $notes = [];

    public function resolve(int $id): void
    {
        $request = ConsumerRequest::where('status', ConsumerRequestStatus::Pending)->findOrFail($id);

        $request->forceFill([
            'status' => ConsumerRequestStatus::Handled,
            'admin_note' => trim($this->notes[$id] ?? '') ?: null,
            'handled_at' => now(),
            'handled_by' => auth()->id(),
        ])->save();

        unset($this->notes[$id]);
        Flux::toast(variant: 'success', text: 'Pedido '.$request->code.' resuelto.');
    }

    public function render()
    {
        return view('livewire.admin.consumer-requests', [
            'requests' => ConsumerRequest::with(['user', 'handler:id,name'])
                ->when($this->status !== 'all', fn ($q) => $q->where('status', $this->status))
                ->latest()->get(),
        ]);
    }
}
