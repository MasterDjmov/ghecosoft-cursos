<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header title="Autorizaciones de menores"
        subtitle="Nota firmada por el alumno, su adulto responsable y vos. Hasta que la apruebes, el alumno no puede tener CV público ni figurar en el ranking global." />

    <flux:select wire:model.live="status" label="Estado" class="max-w-xs">
        <flux:select.option value="pending">Pendientes</flux:select.option>
        <flux:select.option value="approved">Aprobadas</flux:select.option>
        <flux:select.option value="rejected">Rechazadas</flux:select.option>
        <flux:select.option value="all">Todas</flux:select.option>
    </flux:select>

    <div class="flex flex-col gap-3">
        @forelse ($authorizations as $item)
            <article class="panel flex flex-col gap-3 p-4" wire:key="authorization-{{ $item->id }}">
                <div class="flex flex-wrap items-center gap-2">
                    <a href="{{ route('admin.students.show', $item->user) }}" wire:navigate class="font-medium text-white hover:text-primary-bright">{{ $item->user->fullName() }}</a>
                    <span class="text-sm text-ink-muted">
                        {{ $item->user->birth_date ? $item->user->birth_date->age.' años' : 'sin fecha de nacimiento' }} · subida el {{ $item->created_at->format('d/m/Y') }}
                    </span>
                    <flux:badge size="sm" :color="['pending' => 'amber', 'approved' => 'green', 'rejected' => 'red'][$item->status->value]">{{ $item->status->label() }}</flux:badge>
                    <flux:spacer />
                    <flux:button size="sm" icon="document-text" :href="route('files.authorization', $item)" target="_blank">Ver nota</flux:button>
                </div>
                @if ($item->status === \App\Enums\AuthorizationStatus::Pending)
                    <div class="flex flex-col gap-2 sm:flex-row sm:items-start">
                        <div class="flex-1">
                            <flux:input wire:model="notes.{{ $item->id }}" placeholder="Nota (obligatoria para rechazar)" aria-label="Nota" />
                            <flux:error name="notes.{{ $item->id }}" />
                        </div>
                        <div class="flex gap-2">
                            <flux:button variant="ghost" icon="x-mark" wire:click="review({{ $item->id }}, 'reject')">Rechazar</flux:button>
                            <flux:button variant="primary" icon="check" wire:click="review({{ $item->id }}, 'approve')">Aprobar</flux:button>
                        </div>
                    </div>
                @elseif ($item->admin_note || $item->reviewer)
                    <p class="text-xs text-ink-muted">{{ $item->admin_note }}{{ $item->reviewer ? ' · revisada por '.$item->reviewer->name.' el '.$item->reviewed_at?->format('d/m/Y') : '' }}</p>
                @endif
            </article>
        @empty
            <div class="panel p-8 text-center text-ink-muted">No hay autorizaciones {{ $status === 'pending' ? 'pendientes' : 'con ese filtro' }}.</div>
        @endforelse
    </div>
</div>
