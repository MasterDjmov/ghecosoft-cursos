<div class="mx-auto flex w-full max-w-6xl flex-col gap-8 p-4 sm:p-8">
    <header class="flex flex-col gap-1">
        <p class="tech-label"><span class="live-dot me-2"></span>Panel del docente</p>
        <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Inicio</h1>
        <p class="text-ink-muted">{{ $students }} {{ $students === 1 ? 'alumno registrado' : 'alumnos registrados' }}.</p>
    </header>

    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        @foreach ($counters as $counter)
            <a href="{{ $counter['url'] ?? '#' }}" @if (isset($counter['url'])) wire:navigate @endif class="panel flex flex-col gap-3 p-5 transition hover:border-primary-bright/50">
                <flux:icon :name="$counter['icon']" class="size-6 text-primary-bright" />
                <span class="font-display text-3xl font-semibold text-white">{{ $counter['value'] }}</span>
                <span class="text-sm text-ink-muted">{{ $counter['label'] }}</span>
            </a>
        @endforeach
    </div>

    {{-- Estadísticas de las prácticas: qué hacen más y dónde se traban (solo entregas de alumnos). --}}
    <section class="flex flex-col gap-4" data-test="practice-stats">
        <div class="flex flex-col gap-3 sm:flex-row sm:items-end">
            <div class="flex flex-1 flex-col gap-1">
                <p class="tech-label">Estadísticas</p>
                <h2 class="font-display text-xl font-semibold text-white">Prácticas</h2>
            </div>
            <div class="grid grid-cols-2 gap-3 sm:w-[28rem]">
                <flux:select wire:model.live="statsCourse" aria-label="Curso">
                    <flux:select.option value="">Todos los cursos</flux:select.option>
                    @foreach ($courses as $option)
                        <flux:select.option :value="(string) $option->id">{{ $option->title }}</flux:select.option>
                    @endforeach
                </flux:select>
                <flux:select wire:model.live="period" aria-label="Período">
                    @foreach ($periods as $value => $label)
                        <flux:select.option :value="(string) $value">{{ $label }}</flux:select.option>
                    @endforeach
                </flux:select>
            </div>
        </div>

        @php
            $stats = [
                ['label' => 'Entregas', 'value' => $summary['total'], 'hint' => $summary['students'].' '.($summary['students'] === 1 ? 'alumno' : 'alumnos'), 'icon' => 'arrow-up-tray', 'color' => 'text-primary-bright'],
                ['label' => 'Aprobadas', 'value' => $summary['approved'], 'hint' => $summary['pending'].' sin corregir', 'icon' => 'check-circle', 'color' => 'text-success'],
                ['label' => 'Para rehacer', 'value' => $summary['redo'], 'hint' => 'intentos con errores', 'icon' => 'arrow-path', 'color' => 'text-[#fca5a5]'],
                ['label' => 'Vuelven a rehacer', 'value' => $summary['redo_rate'] === null ? '—' : $summary['redo_rate'].'%', 'hint' => 'de lo corregido', 'icon' => 'chart-pie', 'color' => 'text-[#fbbf24]'],
                ['label' => 'Fallan las pruebas', 'value' => $summary['failing'], 'hint' => 'al probarlas al corregir', 'icon' => 'beaker', 'color' => 'text-[#fca5a5]'],
                ['label' => 'Consultas', 'value' => $summary['questions'], 'hint' => 'que escribieron los alumnos', 'icon' => 'chat-bubble-left-right', 'color' => 'text-[#c4b5fd]'],
            ];
        @endphp
        <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">
            @foreach ($stats as $stat)
                <div class="panel flex flex-col gap-2 p-4" data-test="stat-{{ $loop->index }}">
                    <flux:icon :name="$stat['icon']" class="size-5 {{ $stat['color'] }}" />
                    <span class="font-display text-2xl font-semibold text-white">{{ $stat['value'] }}</span>
                    <span class="text-sm text-ink">{{ $stat['label'] }}</span>
                    <span class="text-xs text-ink-muted">{{ $stat['hint'] }}</span>
                </div>
            @endforeach
        </div>

        @if ($byCourse->isNotEmpty())
            <div class="panel overflow-x-auto p-5" data-test="stats-by-course">
                <h3 class="mb-2 font-medium text-white">Por curso</h3>
                <table class="w-full text-sm">
                    <thead class="text-xs text-ink-muted">
                        <tr>
                            <th class="py-1 pe-3 text-left font-medium">Curso</th>
                            <th class="px-2 py-1 text-right font-medium">Alumnos</th>
                            <th class="px-2 py-1 text-right font-medium">Entregas</th>
                            <th class="px-2 py-1 text-right font-medium">Aprobadas</th>
                            <th class="px-2 py-1 text-right font-medium">Para rehacer</th>
                            <th class="px-2 py-1 text-right font-medium">% rehacer</th>
                            <th class="px-2 py-1 text-right font-medium">Fallan pruebas</th>
                            <th class="ps-2 py-1 text-right font-medium">Sin corregir</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach ($byCourse as $row)
                            <tr class="border-t border-outline/60" wire:key="stats-course-{{ $row['id'] }}">
                                <td class="py-1.5 pe-3"><button type="button" wire:click="$set('statsCourse', '{{ $row['id'] }}')" class="text-left text-ink hover:text-primary-bright">{{ $row['title'] }}</button></td>
                                <td class="px-2 py-1.5 text-right font-mono">{{ $row['students'] }}</td>
                                <td class="px-2 py-1.5 text-right font-mono text-white">{{ $row['total'] }}</td>
                                <td class="px-2 py-1.5 text-right font-mono text-success">{{ $row['approved'] }}</td>
                                <td class="px-2 py-1.5 text-right font-mono text-[#fca5a5]">{{ $row['redo'] }}</td>
                                <td class="px-2 py-1.5 text-right font-mono">{{ $row['redo_rate'] === null ? '—' : $row['redo_rate'].'%' }}</td>
                                <td class="px-2 py-1.5 text-right font-mono">{{ $row['failing'] }}</td>
                                <td class="ps-2 py-1.5 text-right font-mono">{{ $row['pending'] }}</td>
                            </tr>
                        @endforeach
                    </tbody>
                </table>
            </div>
        @endif

        <div class="grid gap-4 lg:grid-cols-2">
            @foreach ([
                ['title' => 'Las más elegidas', 'subtitle' => 'Las que más alumnos entregaron. Las optativas son las que eligen.', 'rows' => $mostChosen, 'test' => 'stats-chosen', 'hard' => false],
                ['title' => 'Donde más se traban', 'subtitle' => 'Más intentos para rehacer, más intentos por alumno, pruebas que fallan y consultas.', 'rows' => $hardest, 'test' => 'stats-hardest', 'hard' => true],
            ] as $list)
                <div class="panel flex flex-col gap-3 p-5" data-test="{{ $list['test'] }}">
                    <div>
                        <h3 class="font-medium text-white">{{ $list['title'] }}</h3>
                        <p class="text-xs text-ink-muted">{{ $list['subtitle'] }}</p>
                    </div>
                    @forelse ($list['rows'] as $practice)
                        <div class="flex items-start gap-3 border-t border-outline/60 pt-2" wire:key="{{ $list['test'] }}-{{ $practice['id'] }}">
                            <span class="w-5 shrink-0 pt-0.5 text-right font-mono text-xs text-ink-muted">{{ $loop->iteration }}</span>
                            <div class="flex min-w-0 flex-1 flex-col gap-0.5">
                                <div class="flex flex-wrap items-center gap-2">
                                    <span class="font-medium text-ink">{{ $practice['title'] }}</span>
                                    <flux:badge size="sm" :color="$practice['is_required'] ? 'cyan' : 'violet'">{{ $practice['is_required'] ? 'Obligatoria' : 'Optativa' }}</flux:badge>
                                </div>
                                <span class="truncate text-xs text-ink-muted">{{ $practice['course'] }} · {{ $practice['node'] }}</span>
                                <span class="flex flex-wrap gap-x-3 font-mono text-[11px] text-ink-muted">
                                    @if ($practice['students'] === 0)
                                        <span class="text-[#fbbf24]">todavía sin entregas</span>
                                    @else
                                        <span>{{ $practice['students'] }} {{ $practice['students'] === 1 ? 'alumno' : 'alumnos' }}</span>
                                        <span>{{ str_replace('.', ',', (string) $practice['attempts']) }} intentos c/u</span>
                                    @endif
                                    @if ($practice['redo'] > 0)
                                        <span class="text-[#fca5a5]">{{ $practice['redo'] }} a rehacer{{ $practice['redo_rate'] !== null ? ' ('.$practice['redo_rate'].'%)' : '' }}</span>
                                    @endif
                                    @if ($practice['failing'] > 0)
                                        <span>{{ $practice['failing'] }} con pruebas que fallan</span>
                                    @endif
                                    @if ($practice['questions'] > 0)
                                        <span class="text-[#c4b5fd]">{{ $practice['questions'] }} {{ $practice['questions'] === 1 ? 'consulta' : 'consultas' }}</span>
                                    @endif
                                </span>
                            </div>
                        </div>
                    @empty
                        <flux:text>Todavía no hay datos en este período.</flux:text>
                    @endforelse
                </div>
            @endforeach
        </div>
    </section>
</div>
