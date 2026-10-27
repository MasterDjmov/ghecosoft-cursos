@php
    $isAdmin = auth()->user()->isAdmin();
    $tabs = $isAdmin ? ['' => 'Alumnos', 'nuevos' => 'Nuevos', 'docentes' => 'Docentes'] : ['' => 'Mis alumnos', 'sumar' => 'Sumar alumnos'];
    $newSince = now()->subDays(\App\Livewire\Admin\Students\Index::NEW_DAYS);
    $placeholder = $finding ? 'Buscá por nombre o usuario para sumarlo a una comisión tuya' : 'Buscar por nombre, usuario, email, teléfono o DNI';
@endphp

<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header :title="$teachers ? 'Docentes' : 'Alumnos'"
        :subtitle="$isAdmin ? 'Tocá un alumno para ver sus cursos y su comisión en cada uno.' : 'Los alumnos de tus comisiones. Tocá uno para ver sus cursos; en «Sumar alumnos» buscás a otros para agregarlos a una comisión tuya.'">
        <x-slot:actions>
            <flux:button icon="clock" :href="route('admin.students.delayed')" wire:navigate data-test="delayed-link">
                Demorados @if ($delayedCount)<flux:badge size="sm" color="amber" class="ms-1">{{ $delayedCount }}</flux:badge>@endif
            </flux:button>
            @if ($isAdmin)
                <flux:button variant="primary" icon="user-plus" :href="route('admin.students.create')" wire:navigate>Nuevo alumno</flux:button>
            @endif
        </x-slot:actions>
    </x-admin.page-header>

    <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
        <div class="inline-flex self-start rounded-lg border border-outline bg-surface-low p-1" role="tablist">
            @foreach ($tabs as $value => $label)
                <button type="button" role="tab" wire:click="$set('tab', '{{ $value }}')" aria-selected="{{ $tab === $value ? 'true' : 'false' }}"
                    @class(['rounded-md px-3 py-1.5 text-sm font-medium transition', 'bg-primary-bright text-surface' => $tab === $value, 'text-ink-muted hover:text-ink' => $tab !== $value])>
                    {{ $label }}
                    @if ($value === 'nuevos' && $newCount)
                        <flux:badge size="sm" color="cyan" class="ms-1" data-test="new-count">{{ $newCount }}</flux:badge>
                    @endif
                </button>
            @endforeach
        </div>
        <flux:input class="flex-1" wire:model.live.debounce.400ms="search" :placeholder="$placeholder" icon="magnifying-glass" />
    </div>

    @if ($isAdmin && ! $teachers && $maintenanceOn)
        <flux:callout icon="wrench-screwdriver" color="amber" data-test="maintenance-hint">
            <flux:callout.text>Hay mantenimiento activo. Tildá <strong>Entra en mantenimiento</strong> en los alumnos que quieras dejar pasar para probar: entran a la plataforma y a los cursos cerrados. Hay {{ count($maintenanceAllowed) }} {{ count($maintenanceAllowed) === 1 ? 'habilitado' : 'habilitados' }}.</flux:callout.text>
        </flux:callout>
    @endif

    @if ($recent)
        <flux:text class="text-sm">Los alumnos que se registraron en los últimos {{ \App\Livewire\Admin\Students\Index::NEW_DAYS }} días, del más reciente al más viejo. Tocá uno para matricularlo o ver su ficha.</flux:text>
    @endif

    @if ($teachers)
        <flux:text class="text-sm">Para hacer docente a alguien, entrá a su ficha de alumno y tocá «Hacer docente». Un docente corrige y atiende a los alumnos de sus comisiones; no ve pagos ni edita cursos.</flux:text>
    @endif

    <div class="panel overflow-hidden">
        <ul class="divide-y divide-outline">
            @forelse ($people as $person)
                <li wire:key="person-{{ $person->id }}">
                    @if ($teachers)
                        <div class="flex items-center gap-4 p-4">
                            <flux:avatar size="sm" :initials="$person->initials()" />
                            <div class="flex min-w-0 flex-1 flex-col">
                                <span class="font-medium text-white">{{ $person->fullName() }}</span>
                                <span class="truncate font-mono text-xs text-ink-muted">{{ '@'.$person->username }}{{ $person->email ? ' · '.$person->email : '' }}</span>
                            </div>
                            <span class="text-xs text-ink-muted">{{ $person->taught_cohorts_count }} {{ $person->taught_cohorts_count === 1 ? 'comisión' : 'comisiones' }}</span>
                            <flux:button size="sm" variant="ghost" icon="arrow-uturn-left" wire:click="demote({{ $person->id }})"
                                wire:confirm="¿{{ $person->fullName() }} vuelve a ser alumno? Sus comisiones quedan sin docente (las atendés vos).">Volver a alumno</flux:button>
                        </div>
                    @else
                        <div class="flex items-center">
                        <button type="button" wire:click="toggle({{ $person->id }})" aria-expanded="{{ $expanded === $person->id ? 'true' : 'false' }}"
                            class="flex min-w-0 flex-1 items-center gap-4 p-4 text-start transition hover:bg-surface-high/50" data-test="student-row-{{ $person->username }}">
                            <flux:avatar size="sm" :initials="$person->initials()" />
                            <div class="flex min-w-0 flex-1 flex-col">
                                <span class="font-medium text-white">{{ $person->fullName() }}</span>
                                <span class="truncate font-mono text-xs text-ink-muted">
                                    {{ '@'.$person->username }}@unless ($finding){{ $person->email ? ' · '.$person->email : '' }}{{ $person->phone ? ' · '.$person->phone : '' }}@endunless
                                </span>
                                @if ($recent)
                                    <span class="text-xs text-ink-muted" data-test="registered-at">Se registró {{ $person->created_at->diffForHumans() }} · {{ $person->created_at->format('d/m H:i') }}</span>
                                @endif
                            </div>
                            @if (! $recent && $isAdmin && $person->created_at?->gte($newSince))
                                <flux:badge size="sm" color="cyan">Nuevo</flux:badge>
                            @endif
                            @if ($active->has($person->id))
                                <flux:badge size="sm" color="green">Abono vigente</flux:badge>
                            @endif
                            @unless ($finding)
                                <span class="font-mono text-xs text-ink-muted">{{ $person->xp_total }} {{ term('xp.short') }}</span>
                            @endunless
                            <flux:icon :name="$expanded === $person->id ? 'chevron-up' : 'chevron-down'" variant="micro" class="text-ink-muted" />
                        </button>
                        @if ($isAdmin)
                            {{-- Entra aunque haya mantenimiento (D86): para probar como lo ve un alumno. --}}
                            @php($allowed = isset($maintenanceAllowed[$person->id]))
                            <label class="flex shrink-0 cursor-pointer items-center gap-2 border-s border-outline px-4 py-2 text-xs {{ $allowed ? 'text-warning' : 'text-ink-muted' }}"
                                title="Entra a la plataforma y a los cursos aunque estén en mantenimiento" data-test="maintenance-access-{{ $person->username }}">
                                <input type="checkbox" class="size-4 accent-[#f59e0b]" @checked($allowed) wire:click="toggleMaintenanceAccess({{ $person->id }})">
                                <flux:icon name="wrench-screwdriver" variant="micro" />
                                <span class="hidden sm:inline">Entra en mantenimiento</span>
                            </label>
                        @endif
                        </div>

                        @if ($expanded === $person->id)
                            <div class="flex flex-col gap-3 border-t border-outline bg-surface-lowest/40 px-4 py-4 sm:ps-16" data-test="student-courses">
                                @forelse ($detail as $row)
                                    <div class="flex flex-col gap-2 sm:flex-row sm:items-center" wire:key="course-{{ $person->id }}-{{ $row['course']->id }}">
                                        <div class="flex min-w-0 flex-1 items-center gap-3">
                                            <x-course-logo :course="$row['course']" size="size-9" />
                                            <div class="flex min-w-0 flex-col">
                                                <span class="truncate text-sm text-white">{{ $row['course']->title }}</span>
                                                <span class="text-xs {{ $row['active'] ? 'text-success' : 'text-ink-muted' }}">{{ $row['active'] ? 'Abono vigente' : 'Abono vencido' }}</span>
                                            </div>
                                            @can('viewProgress', [$person, $row['course']])
                                                <flux:button size="xs" variant="ghost" icon="share" :href="route('admin.students.tree', [$person, $row['course']])" wire:navigate
                                                    data-test="student-tree-link-{{ $row['course']->id }}">Ver árbol</flux:button>
                                            @endcan
                                        </div>
                                        @if ($row['needsCohort'])
                                            {{-- Las comisiones se crean en Comisiones, dentro de cada curso; acá solo se elige. --}}
                                            <span class="text-sm text-ink-muted" data-test="needs-cohort-{{ $row['course']->id }}">
                                                {{ $isAdmin ? 'Este curso no tiene comisiones.' : 'No tenés comisiones de este curso.' }}
                                                <flux:link :href="route('admin.cohorts').'#comisiones-'.$row['course']->id">Creá una en Comisiones</flux:link>
                                            </span>
                                        @elseif ($row['canChange'])
                                            <flux:select size="sm" class="sm:w-72" aria-label="Comisión en {{ $row['course']->title }}"
                                                x-on:change="$wire.assignCohort({{ $person->id }}, {{ $row['course']->id }}, $event.target.value)">
                                                <flux:select.option value="" :selected="! $row['cohort']">Sin comisión</flux:select.option>
                                                @foreach ($row['options'] as $cohort)
                                                    <flux:select.option :value="(string) $cohort->id" :selected="$row['cohort']?->id === $cohort->id">
                                                        {{ $cohort->name }}{{ $isAdmin && $cohort->teacher ? ' · '.$cohort->teacher->name : '' }}
                                                    </flux:select.option>
                                                @endforeach
                                            </flux:select>
                                        @else
                                            <span class="text-sm text-ink-muted">
                                                {{ $row['cohort'] ? $row['cohort']->name.($row['cohort']->teacher ? ' · '.$row['cohort']->teacher->fullName() : '') : 'Sin comisión' }}
                                                @if (! $isAdmin && $row['cohort'])
                                                    · de otro docente
                                                @endif
                                            </span>
                                        @endif
                                    </div>
                                @empty
                                    <p class="text-sm text-ink-muted">Todavía no tiene abono en ningún curso (puede estar probando una clase 0). La comisión se elige con el abono.</p>
                                @endforelse
                                @if ($isAdmin)
                                    {{-- Matricular en otro curso (o renovar uno), como en el alta: pasa por el aprobador. --}}
                                    @php($taken = collect($detail)->pluck('course.id')->flip())
                                    <form wire:submit="enroll" class="flex flex-col gap-2 border-t border-outline pt-3 sm:flex-row sm:items-end" data-test="enroll-form">
                                        <flux:select size="sm" class="sm:flex-1" wire:model.live="enrollCourseId" label="Matricular en un curso">
                                            <flux:select.option value="">Elegí un curso…</flux:select.option>
                                            @foreach ($enrollCourses as $course)
                                                <flux:select.option :value="(string) $course->id">
                                                    {{ $course->title }}{{ $course->is_published ? '' : ' (sin publicar)' }}{{ $taken->has($course->id) ? ' · renueva el abono' : '' }}
                                                </flux:select.option>
                                            @endforeach
                                        </flux:select>
                                        @if ($enrollCohorts->isNotEmpty())
                                            <flux:select size="sm" class="sm:w-56" wire:model="enrollCohortId" label="Comisión">
                                                <flux:select.option value="">Sin comisión</flux:select.option>
                                                @foreach ($enrollCohorts as $cohort)
                                                    <flux:select.option :value="(string) $cohort->id">{{ $cohort->name }}</flux:select.option>
                                                @endforeach
                                            </flux:select>
                                        @endif
                                        <flux:button size="sm" type="submit" variant="primary" icon="academic-cap" :disabled="$enrollCourseId === ''">
                                            {{ $enrollCourseId !== '' && $taken->has((int) $enrollCourseId) ? 'Renovar abono' : 'Matricular' }}
                                        </flux:button>
                                    </form>
                                @endif
                                @can('viewStudent', $person)
                                    <div><flux:button size="sm" variant="ghost" icon="identification" :href="route('admin.students.show', $person)" wire:navigate>Ver la ficha completa</flux:button></div>
                                @endcan
                            </div>
                        @endif
                    @endif
                </li>
            @empty
                <li class="p-8 text-center text-ink-muted">
                    @if ($finding && mb_strlen(trim($search)) < 2)
                        Escribí al menos dos letras del nombre o el usuario.
                    @elseif (! $isAdmin && $tab === '')
                        Todavía no tenés alumnos: creá una comisión en <flux:link :href="route('admin.cohorts')" wire:navigate>Comisiones</flux:link> y sumalos desde «Sumar alumnos».
                    @elseif ($recent)
                        Nadie se registró en los últimos {{ \App\Livewire\Admin\Students\Index::NEW_DAYS }} días.
                    @else
                        No se encontraron {{ $teachers ? 'docentes' : 'alumnos' }}.
                    @endif
                </li>
            @endforelse
        </ul>
    </div>

    {{ $people->links() }}
</div>
