<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header title="Alumnos demorados"
        :subtitle="'Con el abono vigente y sin avanzar hace '.\App\Services\DelayedStudents::DAYS.' días o más (entregar, superar una micro-misión o abrir un nodo). Mandales un aviso: les llega por mail y a la campanita.'">
        <x-slot:actions>
            <flux:button variant="ghost" icon="arrow-left" :href="route('admin.students.index')" wire:navigate>Alumnos</flux:button>
        </x-slot:actions>
    </x-admin.page-header>

    @if ($courses->count() > 1)
        <flux:select wire:model.live="courseId" class="max-w-sm">
            <flux:select.option value="">Todos los cursos</flux:select.option>
            @foreach ($courses as $course)
                <flux:select.option :value="$course->id">{{ $course->title }}</flux:select.option>
            @endforeach
        </flux:select>
    @endif

    <div class="panel overflow-hidden">
        <ul class="divide-y divide-outline">
            @forelse ($rows as $row)
                <li wire:key="delayed-{{ $row['student']->id }}-{{ $row['course']->id }}" class="flex flex-col gap-3 p-4 sm:flex-row sm:items-center" data-test="delayed-{{ $row['student']->username }}">
                    <div class="flex min-w-0 flex-1 items-center gap-4">
                        <flux:avatar size="sm" :initials="$row['student']->initials()" />
                        <div class="flex min-w-0 flex-col">
                            <a href="{{ route('admin.students.tree', [$row['student'], $row['course']]) }}" wire:navigate class="font-medium text-white hover:underline">{{ $row['student']->fullName() }}</a>
                            <span class="truncate text-xs text-ink-muted">
                                {{ $row['course']->title }}{{ $row['cohort'] ? ' · '.$row['cohort']->name : '' }}
                                · {{ $row['what'] }} el {{ $row['last']->format('d/m') }}
                            </span>
                            @if ($row['reminded'])
                                <span class="text-xs text-primary-bright">Avisado el {{ $row['reminded']->created_at->format('d/m H:i') }}</span>
                            @endif
                        </div>
                    </div>
                    <div class="flex items-center gap-3">
                        <flux:badge size="sm" :color="$row['days'] >= 10 ? 'red' : 'amber'">{{ $row['days'] }} días</flux:badge>
                        @if (! $row['student']->email)
                            <span class="text-xs text-ink-muted" title="No tiene email: el aviso le llega solo a la campanita">sin email</span>
                        @endif
                        <flux:button size="sm" icon="envelope" wire:click="open({{ $row['student']->id }}, {{ $row['course']->id }})">Avisar</flux:button>
                    </div>
                </li>
            @empty
                <li class="p-8 text-center text-ink-muted">No hay alumnos demorados. Todos avanzaron en los últimos {{ \App\Services\DelayedStudents::DAYS }} días.</li>
            @endforelse
        </ul>
    </div>

    <flux:modal name="remind" class="w-full max-w-lg">
        @if ($reminding && $remindCourse)
            <form wire:submit="send" class="flex flex-col gap-4">
                <flux:heading size="lg">Aviso a {{ $reminding->fullName() }}</flux:heading>
                <flux:text>Le llega {{ $reminding->email ? 'por mail ('.$reminding->email.') y' : 'solo' }} a la campanita, con un link a su árbol de «{{ $remindCourse->title }}». Queda anotado acá.</flux:text>
                <x-emoji-field><flux:textarea class="pe-10" wire:model="body" label="Mensaje" rows="5" /></x-emoji-field>
                <div class="flex justify-end gap-2">
                    <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                    <flux:button variant="primary" type="submit" icon="paper-airplane">Mandar aviso</flux:button>
                </div>
            </form>
        @endif
    </flux:modal>
</div>
