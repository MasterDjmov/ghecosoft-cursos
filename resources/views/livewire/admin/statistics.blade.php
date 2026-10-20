<div class="mx-auto flex w-full max-w-6xl flex-col gap-8 p-4 sm:p-8">
    <x-admin.page-header title="Estadísticas"
        subtitle="Qué miran los alumnos, dónde fallan y en qué capítulo se traban. Las visitas y los fallos de las micro-misiones se registran desde el 15/10/2026; los aparatos, desde el 16/10/2026." />

    <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4" data-test="stats-filters">
        <flux:select wire:model.live="course" aria-label="Curso">
            <flux:select.option value="">Todos los cursos</flux:select.option>
            @foreach ($courses as $option)
                <flux:select.option :value="(string) $option->id">{{ $option->title }}</flux:select.option>
            @endforeach
        </flux:select>
        <flux:select wire:model.live="cohort" aria-label="Comisión">
            <flux:select.option value="">Todas las comisiones</flux:select.option>
            @foreach ($cohortOptions as $option)
                <flux:select.option :value="(string) $option->id">{{ $option->name }}{{ $selectedCourse ? '' : ' · '.$option->course?->title }}</flux:select.option>
            @endforeach
        </flux:select>
        <flux:select wire:model.live="student" aria-label="Alumno">
            <flux:select.option value="">Todos los alumnos</flux:select.option>
            @foreach ($studentOptions as $option)
                <flux:select.option :value="(string) $option->id">{{ $option->fullName() }} ({{ $option->username }})</flux:select.option>
            @endforeach
        </flux:select>
        <flux:select wire:model.live="period" aria-label="Período">
            @foreach ($periods as $value => $label)
                <flux:select.option :value="(string) $value">{{ $label }}</flux:select.option>
            @endforeach
        </flux:select>
    </div>

    @if ($chosen && $selectedCourse)
        <flux:callout icon="map" color="cyan">
            <flux:callout.text>
                Capítulo por capítulo, con sus respuestas equivocadas:
                <flux:link :href="route('admin.students.tree', [$chosen, $selectedCourse])" wire:navigate>el recorrido de {{ $chosen->fullName() }}</flux:link>.
            </flux:callout.text>
        </flux:callout>
    @endif

    {{-- Resumen de las micro-misiones y las visitas. --}}
    @php
        $cards = [
            ['label' => 'Alumnos activos', 'value' => $summary['students'], 'hint' => 'miraron o probaron algo', 'icon' => 'users', 'color' => 'text-primary-bright'],
            ['label' => 'Visitas a capítulos', 'value' => $summary['visits'], 'hint' => 'veces que abrieron un nodo', 'icon' => 'eye', 'color' => 'text-primary-bright'],
            ['label' => 'Intentos', 'value' => $summary['attempts'], 'hint' => 'de micro-misiones', 'icon' => 'play', 'color' => 'text-ink'],
            ['label' => 'Fallos', 'value' => $summary['fails'], 'hint' => 'intentos que no salieron', 'icon' => 'x-circle', 'color' => 'text-[#fca5a5]'],
            ['label' => 'Salen bien', 'value' => $summary['success_rate'] === null ? '—' : $summary['success_rate'].'%', 'hint' => 'de los intentos', 'icon' => 'check-circle', 'color' => 'text-success'],
            ['label' => 'Trabados', 'value' => $summary['stuck'], 'hint' => \App\Support\StudentJourney::STUCK_FAILS.' fallos o más sin acertar', 'icon' => 'exclamation-triangle', 'color' => 'text-[#fbbf24]'],
        ];
    @endphp
    <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6" data-test="stats-summary">
        @foreach ($cards as $card)
            <div class="panel flex flex-col gap-2 p-4">
                <flux:icon :name="$card['icon']" class="size-5 {{ $card['color'] }}" />
                <span class="font-display text-2xl font-semibold text-white">{{ $card['value'] }}</span>
                <span class="text-sm text-ink">{{ $card['label'] }}</span>
                <span class="text-xs text-ink-muted">{{ $card['hint'] }}</span>
            </div>
        @endforeach
    </div>

    <div class="grid gap-4 lg:grid-cols-3">
        {{-- Embudo por capítulo (con un curso elegido). --}}
        <section class="panel flex flex-col gap-3 p-5 lg:col-span-2" data-test="stats-funnel">
            <div>
                <h2 class="font-medium text-white">Embudo por capítulo</h2>
                <p class="text-xs text-ink-muted">Cuántos alumnos abrieron cada {{ $selectedCourse ? term('node', $selectedCourse) : 'nodo' }}, cuántos lo miraron y cuántos superaron todas sus micro-misiones. Donde la barra se achica, se cae la gente.</p>
            </div>
            @if (! $selectedCourse)
                <flux:text>Elegí un curso para ver su embudo.</flux:text>
            @else
                @php
                    $max = max(1, $funnel->max('unlocked'), $funnel->max('seen'));
                @endphp
                @forelse ($funnel as $row)
                    <div class="flex flex-col gap-1 border-t border-outline/60 pt-2" wire:key="funnel-{{ $row['id'] }}">
                        <div class="flex items-baseline justify-between gap-3 text-sm">
                            <span class="min-w-0 truncate text-ink"><span class="font-mono text-xs text-ink-muted">{{ $row['code'] }}</span> {{ $row['title'] }}</span>
                            <span class="shrink-0 font-mono text-[11px] text-ink-muted">
                                {{ $row['unlocked'] }} abrieron · {{ $row['seen'] }} miraron · {{ $row['finished'] === null ? 'sin micro-misiones' : $row['finished'].' terminaron' }}
                            </span>
                        </div>
                        <div class="relative h-2 overflow-hidden rounded-full bg-surface-high" aria-hidden="true">
                            <div class="absolute inset-y-0 left-0 rounded-full bg-primary/40" style="width: {{ round(100 * max($row['unlocked'], $row['seen']) / $max) }}%"></div>
                            @if ($row['finished'] !== null)
                                <div class="absolute inset-y-0 left-0 rounded-full bg-success" style="width: {{ round(100 * $row['finished'] / $max) }}%"></div>
                            @endif
                        </div>
                    </div>
                @empty
                    <flux:text>Todavía no hay datos en este período.</flux:text>
                @endforelse
            @endif
        </section>

        {{-- Desde dónde entran (D109). --}}
        <section class="panel flex flex-col gap-3 p-5" data-test="stats-devices">
            <div>
                <h2 class="font-medium text-white">Desde dónde entran</h2>
                <p class="text-xs text-ink-muted">Días de uso por aparato (un alumno que entra desde dos aparatos el mismo día cuenta en los dos).</p>
            </div>
            @forelse ($devices as $device)
                <div class="flex flex-col gap-1 border-t border-outline/60 pt-2" wire:key="device-{{ $device['device'] }}">
                    <div class="flex items-baseline justify-between text-sm">
                        <span class="text-ink">{{ $device['label'] }}</span>
                        <span class="font-mono text-xs text-ink-muted">{{ $device['percent'] }}% · {{ $device['students'] }} {{ $device['students'] === 1 ? 'alumno' : 'alumnos' }}</span>
                    </div>
                    <div class="h-2 overflow-hidden rounded-full bg-surface-high" aria-hidden="true">
                        <div class="h-full rounded-full bg-primary-bright" style="width: {{ $device['percent'] }}%"></div>
                    </div>
                </div>
            @empty
                <flux:text>Todavía no hay accesos en este período.</flux:text>
            @endforelse
        </section>
    </div>

    <div class="grid gap-4 lg:grid-cols-2">
        {{-- Micro-misiones más difíciles. --}}
        <section class="panel flex flex-col gap-3 p-5" data-test="stats-hardest-steps">
            <div>
                <h2 class="font-medium text-white">Micro-misiones más difíciles</h2>
                <p class="text-xs text-ink-muted">Las de más fallos, con las respuestas equivocadas que más se repiten.</p>
            </div>
            @forelse ($hardestSteps as $step)
                <div class="flex items-start gap-3 border-t border-outline/60 pt-2" wire:key="hard-step-{{ $step['id'] }}">
                    <span class="w-5 shrink-0 pt-0.5 text-right font-mono text-xs text-ink-muted">{{ $loop->iteration }}</span>
                    <div class="flex min-w-0 flex-1 flex-col gap-0.5">
                        <span class="font-medium text-ink">{{ $step['title'] }}</span>
                        <span class="truncate text-xs text-ink-muted">{{ $selectedCourse ? '' : $step['course'].' · ' }}{{ $step['node'] }} · {{ $step['code'] }}</span>
                        <span class="flex flex-wrap gap-x-3 font-mono text-[11px] text-ink-muted">
                            <span class="text-[#fca5a5]">{{ $step['fails'] }} {{ $step['fails'] === 1 ? 'fallo' : 'fallos' }}</span>
                            <span>{{ $step['students'] }} {{ $step['students'] === 1 ? 'alumno falló' : 'alumnos fallaron' }}</span>
                            @if ($step['pending'] > 0)
                                <span class="text-[#fbbf24]">{{ $step['pending'] }} sin superarla</span>
                            @endif
                            @if ($step['per_pass'] !== null)
                                <span>{{ str_replace('.', ',', (string) $step['per_pass']) }} intentos por acierto</span>
                            @endif
                        </span>
                        @foreach ($step['answers'] as $answer)
                            <div class="mt-1 flex items-start gap-2 text-xs">
                                <code class="min-w-0 flex-1 truncate rounded bg-surface-high px-1.5 py-0.5 text-[#fca5a5]" title="{{ $answer['text'] }}">{{ \Illuminate\Support\Str::limit($answer['text'], 90) }}</code>
                                <span class="shrink-0 font-mono text-ink-muted">×{{ $answer['times'] }}</span>
                            </div>
                        @endforeach
                    </div>
                </div>
            @empty
                <flux:text>Ningún fallo en este período.</flux:text>
            @endforelse
        </section>

        {{-- Alumnos trabados. --}}
        <section class="panel flex flex-col gap-3 p-5" data-test="stats-stuck">
            <div class="flex items-start justify-between gap-3">
                <div>
                    <h2 class="font-medium text-white">Alumnos trabados</h2>
                    <p class="text-xs text-ink-muted">Con una micro-misión fallada {{ \App\Support\StudentJourney::STUCK_FAILS }} veces o más y sin superar. Los que no entran hace días están en Demorados.</p>
                </div>
                <flux:button size="sm" variant="ghost" icon="clock" :href="route('admin.students.delayed')" wire:navigate>Demorados</flux:button>
            </div>
            @forelse ($stuck as $row)
                <div class="flex flex-col gap-1 border-t border-outline/60 pt-2" wire:key="stuck-{{ $row['student']->id }}-{{ $row['course']->id }}" data-test="stuck-{{ $row['student']->username }}">
                    <div class="flex items-baseline justify-between gap-3">
                        <a href="{{ route('admin.students.tree', [$row['student'], $row['course']]) }}" wire:navigate class="font-medium text-white hover:underline">{{ $row['student']->fullName() }}</a>
                        <span class="shrink-0 text-xs text-ink-muted">{{ $row['last_at']->format('d/m H:i') }}</span>
                    </div>
                    @unless ($selectedCourse)
                        <span class="text-xs text-ink-muted">{{ $row['course']->title }}</span>
                    @endunless
                    <ul class="flex flex-col gap-0.5 text-xs">
                        @foreach ($row['steps'] as $step)
                            <li class="flex justify-between gap-3"><span class="min-w-0 truncate text-ink"><span class="font-mono text-ink-muted">{{ $step['code'] }}</span> {{ $step['title'] }}</span><span class="shrink-0 font-mono text-[#fca5a5]">{{ $step['fails'] }} fallos</span></li>
                        @endforeach
                    </ul>
                </div>
            @empty
                <flux:text>Nadie trabado en este período.</flux:text>
            @endforelse
        </section>
    </div>

    {{-- Prácticas (entregas corregidas por el docente): lo que antes estaba en el Inicio. --}}
    <section class="flex flex-col gap-4" data-test="practice-stats">
        <div>
            <p class="tech-label">Entregas</p>
            <h2 class="font-display text-xl font-semibold text-white">Prácticas</h2>
        </div>
        @php
            $stats = [
                ['label' => 'Entregas', 'value' => $practiceSummary['total'], 'hint' => $practiceSummary['students'].' '.($practiceSummary['students'] === 1 ? 'alumno' : 'alumnos'), 'icon' => 'arrow-up-tray', 'color' => 'text-primary-bright'],
                ['label' => 'Aprobadas', 'value' => $practiceSummary['approved'], 'hint' => $practiceSummary['pending'].' sin corregir', 'icon' => 'check-circle', 'color' => 'text-success'],
                ['label' => 'Para rehacer', 'value' => $practiceSummary['redo'], 'hint' => 'intentos con errores', 'icon' => 'arrow-path', 'color' => 'text-[#fca5a5]'],
                ['label' => 'Vuelven a rehacer', 'value' => $practiceSummary['redo_rate'] === null ? '—' : $practiceSummary['redo_rate'].'%', 'hint' => 'de lo corregido', 'icon' => 'chart-pie', 'color' => 'text-[#fbbf24]'],
                ['label' => 'Fallan las pruebas', 'value' => $practiceSummary['failing'], 'hint' => 'al probarlas al corregir', 'icon' => 'beaker', 'color' => 'text-[#fca5a5]'],
                ['label' => 'Consultas', 'value' => $practiceSummary['questions'], 'hint' => 'que escribieron los alumnos', 'icon' => 'chat-bubble-left-right', 'color' => 'text-[#c4b5fd]'],
            ];
        @endphp
        <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">
            @foreach ($stats as $stat)
                <div class="panel flex flex-col gap-2 p-4">
                    <flux:icon :name="$stat['icon']" class="size-5 {{ $stat['color'] }}" />
                    <span class="font-display text-2xl font-semibold text-white">{{ $stat['value'] }}</span>
                    <span class="text-sm text-ink">{{ $stat['label'] }}</span>
                    <span class="text-xs text-ink-muted">{{ $stat['hint'] }}</span>
                </div>
            @endforeach
        </div>

        <div class="grid gap-4 lg:grid-cols-2">
            @foreach ([
                ['title' => 'Las más elegidas', 'subtitle' => 'Las que más alumnos entregaron. Las optativas son las que eligen.', 'rows' => $mostChosen, 'test' => 'stats-chosen'],
                ['title' => 'Donde más se traban', 'subtitle' => 'Más intentos para rehacer, más intentos por alumno, pruebas que fallan y consultas.', 'rows' => $hardest, 'test' => 'stats-hardest'],
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
