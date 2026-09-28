<section class="panel flex flex-col gap-4 p-5 sm:p-6">
    <div class="flex flex-wrap items-start justify-between gap-3">
        <div class="flex flex-col gap-1">
            <h2 class="font-display font-semibold text-white">Comisiones</h2>
            <p class="text-sm text-ink-muted">Opcionales: sirven para agrupar alumnos y filtrar las correcciones. No cambian aperturas, monedas ni abonos.</p>
        </div>
        <flux:button size="sm" variant="primary" icon="plus" wire:click="create">Nueva comisión</flux:button>
    </div>

    <ul class="divide-y divide-outline text-sm">
        @forelse ($cohorts as $cohort)
            <li class="flex flex-wrap items-center gap-x-3 gap-y-2 py-3" wire:key="cohort-{{ $cohort->id }}">
                <div class="flex min-w-0 flex-1 flex-col gap-0.5">
                    <span class="font-medium text-ink">{{ $cohort->name }}</span>
                    <span class="text-xs text-ink-muted">
                        {{ $cohort->modality->label() }}
                        @if ($cohort->schedule_text) · {{ $cohort->schedule_text }} @endif
                        @if ($cohort->starts_on) · desde el {{ $cohort->starts_on->format('d/m/Y') }} @endif
                        · {{ $cohort->students_count }} {{ $cohort->students_count === 1 ? 'alumno' : 'alumnos' }}
                    </span>
                </div>
                <flux:badge size="sm" :color="$cohort->is_open_for_enrollment ? 'green' : 'zinc'">{{ $cohort->is_open_for_enrollment ? 'Abierta' : 'Cerrada' }}</flux:badge>
                <div class="flex gap-1">
                    <flux:button size="xs" variant="ghost" wire:click="toggleOpen({{ $cohort->id }})">{{ $cohort->is_open_for_enrollment ? 'Cerrar' : 'Abrir' }}</flux:button>
                    <flux:button size="xs" icon="pencil-square" wire:click="edit({{ $cohort->id }})">Editar</flux:button>
                    <flux:button size="xs" variant="ghost" icon="trash" wire:click="delete({{ $cohort->id }})"
                        wire:confirm="¿Borrar la comisión «{{ $cohort->name }}»? Sus alumnos siguen cursando, pero quedan sin comisión.">Borrar</flux:button>
                </div>
            </li>
        @empty
            <li class="py-3 text-ink-muted">Sin comisiones. Los alumnos se inscriben igual.</li>
        @endforelse
    </ul>

    <flux:modal name="cohort-form" class="w-full max-w-lg">
        <form wire:submit="save" class="flex flex-col gap-5">
            <flux:heading size="lg">{{ $editingId ? 'Editar comisión' : 'Nueva comisión' }}</flux:heading>
            <flux:input wire:model="name" label="Nombre" placeholder="Martes y jueves tarde" />
            <div class="grid gap-5 sm:grid-cols-2">
                <flux:select wire:model="modality" label="Modalidad">
                    @foreach ($modalities as $option)
                        <flux:select.option :value="$option->value">{{ $option->label() }}</flux:select.option>
                    @endforeach
                </flux:select>
                <flux:input wire:model="starts_on" type="date" label="Inicio (opcional)" />
            </div>
            <flux:input wire:model="schedule_text" label="Horario (opcional)" placeholder="Mar y jue 18 a 20 h" />
            <flux:switch wire:model="is_open_for_enrollment" label="Abierta a inscripciones" description="Si está abierta, el alumno la puede elegir al inscribirse." />
            <div class="flex justify-end gap-2">
                <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                <flux:button variant="primary" type="submit">Guardar</flux:button>
            </div>
        </form>
    </flux:modal>
</section>
