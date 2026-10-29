<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header title="Arrepentimientos y bajas"
        subtitle="Pedidos del botón de arrepentimiento y del botón de baja (Defensa del Consumidor). El alumno ya recibió su código de trámite: escribile, devolvé o da de baja, y marcalo resuelto." />

    <flux:select wire:model.live="status" label="Estado" class="max-w-xs">
        <flux:select.option value="pending">Pendientes</flux:select.option>
        <flux:select.option value="handled">Resueltos</flux:select.option>
        <flux:select.option value="all">Todos</flux:select.option>
    </flux:select>

    <div class="flex flex-col gap-3">
        @forelse ($requests as $item)
            <article class="panel flex flex-col gap-3 p-4" wire:key="consumer-request-{{ $item->id }}">
                <div class="flex flex-wrap items-center gap-2">
                    <flux:badge size="sm" :color="$item->kind === \App\Enums\ConsumerRequestKind::Withdrawal ? 'red' : 'zinc'">{{ $item->kind->label() }}</flux:badge>
                    <span class="font-mono text-sm text-white">{{ $item->code }}</span>
                    @if ($item->user)
                        <a href="{{ route('admin.students.show', $item->user) }}" wire:navigate class="font-medium text-white hover:text-primary-bright">{{ $item->name }}</a>
                    @else
                        <span class="font-medium text-white">{{ $item->name }}</span>
                    @endif
                    <span class="text-sm text-ink-muted">{{ $item->contact }}{{ $item->course ? ' · '.$item->course : '' }} · {{ $item->created_at->format('d/m/Y H:i') }}</span>
                    <flux:badge size="sm" :color="$item->status === \App\Enums\ConsumerRequestStatus::Pending ? 'amber' : 'green'">{{ $item->status->label() }}</flux:badge>
                </div>
                @if ($item->details)
                    <p class="whitespace-pre-line text-sm text-ink">{{ $item->details }}</p>
                @endif
                @if ($item->status === \App\Enums\ConsumerRequestStatus::Pending)
                    <div class="flex flex-col gap-2 sm:flex-row sm:items-start">
                        <flux:input wire:model="notes.{{ $item->id }}" placeholder="Qué se hizo (opcional): devolución por transferencia, baja de la cuenta…" aria-label="Nota" class="flex-1" />
                        <flux:button variant="primary" icon="check" wire:click="resolve({{ $item->id }})">Marcar resuelto</flux:button>
                    </div>
                @elseif ($item->admin_note || $item->handler)
                    <p class="text-xs text-ink-muted">{{ $item->admin_note }}{{ $item->handler ? ' · resuelto por '.$item->handler->name.' el '.$item->handled_at?->format('d/m/Y') : '' }}</p>
                @endif
            </article>
        @empty
            <div class="panel p-8 text-center text-ink-muted">No hay pedidos {{ $status === 'pending' ? 'pendientes' : 'con ese filtro' }}.</div>
        @endforelse
    </div>
</div>
