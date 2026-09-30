<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header title="Entregas" :subtitle="(auth()->user()->isTeacher() ? 'Las de los alumnos de tus comisiones. ' : '').'Aprobada paga las monedas y la XP de la hoja (una sola vez). Rehacer pide un comentario.'">
        <x-slot:actions>
            @if ($pendingCount > 0)
                <flux:button variant="primary" icon="play" :href="route('admin.submissions.next')" wire:navigate>Corregir la más vieja</flux:button>
            @endif
        </x-slot:actions>
    </x-admin.page-header>

    @if (auth()->user()->isTeacher() && $cohorts->isEmpty() && $courseId === '')
        <flux:callout icon="user-group" color="cyan">
            <flux:callout.text>Todavía no tenés comisiones. <flux:link :href="route('admin.cohorts')" wire:navigate>Creá una</flux:link> y sumale alumnos: vas a ver acá sus entregas.</flux:callout.text>
        </flux:callout>
    @endif

    <div @class(['grid gap-4 sm:grid-cols-2', 'lg:grid-cols-5' => $teachers->isNotEmpty(), 'lg:grid-cols-4' => $teachers->isEmpty()])>
        <flux:select wire:model.live="status" label="Estado">
            <flux:select.option value="submitted">Sin corregir ({{ $pendingCount }})</flux:select.option>
            <flux:select.option value="approved">Aprobadas</flux:select.option>
            <flux:select.option value="redo">Rehacer</flux:select.option>
            <flux:select.option value="all">Todas</flux:select.option>
        </flux:select>
        <flux:select wire:model.live="courseId" label="Curso">
            <flux:select.option value="">Todos</flux:select.option>
            @foreach ($courses as $option)
                <flux:select.option :value="(string) $option->id">{{ $option->title }}</flux:select.option>
            @endforeach
        </flux:select>
        @if ($teachers->isNotEmpty())
            <flux:select wire:model.live="teacherId" label="Docente">
                <flux:select.option value="">Todos</flux:select.option>
                @foreach ($teachers as $teacher)
                    <flux:select.option :value="(string) $teacher->id">{{ $teacher->fullName() }}</flux:select.option>
                @endforeach
            </flux:select>
        @endif
        <flux:select wire:model.live="cohortId" label="Comisión">
            <flux:select.option value="">Todas</flux:select.option>
            @foreach ($cohorts as $option)
                <flux:select.option :value="(string) $option->id">{{ $option->name }}</flux:select.option>
            @endforeach
        </flux:select>
        <flux:input wire:model.live.debounce.400ms="search" label="Alumno" placeholder="Nombre o usuario" icon="magnifying-glass" />
    </div>

    <div class="panel overflow-hidden">
        <ul class="divide-y divide-outline">
            @forelse ($submissions as $submission)
                <li wire:key="submission-{{ $submission->id }}">
                    <a href="{{ route('admin.submissions.show', $submission) }}" wire:navigate class="flex flex-col gap-1 p-4 transition hover:bg-surface-high/50 sm:flex-row sm:items-center sm:gap-4">
                        <div class="flex min-w-0 flex-1 flex-col gap-1">
                            <div class="flex flex-wrap items-center gap-2">
                                <span class="font-medium text-white">{{ $submission->user->fullName() }}</span>
                                <span class="font-mono text-xs text-ink-muted">{{ '@'.$submission->user->username }}</span>
                                <flux:badge size="sm" :color="['submitted' => 'amber', 'approved' => 'green', 'redo' => 'red'][$submission->status->value]">{{ $submission->status->label() }}</flux:badge>
                            </div>
                            <p class="truncate text-sm text-ink-muted">
                                {{ $submission->practice->node->course->title }} · {{ $submission->practice->node->title }} · <span class="text-ink">{{ $submission->practice->title }}</span>
                                · intento {{ $submission->attempt }}
                            </p>
                        </div>
                        <span class="shrink-0 font-mono text-xs text-ink-muted">{{ $submission->submitted_at->diffForHumans() }}</span>
                    </a>
                </li>
            @empty
                <li class="p-8 text-center text-ink-muted">{{ $status === 'submitted' ? '¡No hay nada para corregir!' : 'No hay entregas con ese filtro.' }}</li>
            @endforelse
        </ul>
    </div>

    {{ $submissions->links() }}
</div>
