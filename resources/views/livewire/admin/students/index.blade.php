<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header title="Alumnos" />

    <flux:input wire:model.live.debounce.400ms="search" placeholder="Buscar por nombre, usuario, email o DNI" icon="magnifying-glass" />

    <div class="panel overflow-hidden">
        <ul class="divide-y divide-outline">
            @forelse ($students as $student)
                <li wire:key="student-{{ $student->id }}">
                    <a href="{{ route('admin.students.show', $student) }}" wire:navigate class="flex items-center gap-4 p-4 transition hover:bg-surface-high/50">
                        <flux:avatar size="sm" :initials="$student->initials()" />
                        <div class="flex min-w-0 flex-1 flex-col">
                            <span class="font-medium text-white">{{ $student->fullName() }}</span>
                            <span class="truncate font-mono text-xs text-ink-muted">{{ '@'.$student->username }} · {{ $student->email }}</span>
                        </div>
                        @if ($active->has($student->id))
                            <flux:badge size="sm" color="green">Abono vigente</flux:badge>
                        @endif
                        <span class="font-mono text-xs text-ink-muted">{{ $student->xp_total }} {{ term('xp.short') }}</span>
                    </a>
                </li>
            @empty
                <li class="p-8 text-center text-ink-muted">No se encontraron alumnos.</li>
            @endforelse
        </ul>
    </div>

    {{ $students->links() }}
</div>
