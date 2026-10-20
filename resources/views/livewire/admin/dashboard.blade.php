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

    {{-- Resumen de los últimos 30 días; el detalle, con filtros, en Estadísticas (D107). --}}
    <section class="panel flex flex-col gap-4 p-5" data-test="stats-overview">
        <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
                <p class="tech-label">Últimos 30 días</p>
                <h2 class="font-display text-xl font-semibold text-white">Cómo vienen los alumnos</h2>
            </div>
            <flux:button icon="presentation-chart-line" :href="route('admin.statistics')" wire:navigate>Ver estadísticas</flux:button>
        </div>
        @php
            $overview = [
                ['label' => 'Alumnos activos', 'value' => $progress['students']],
                ['label' => 'Intentos de micro-misiones', 'value' => $progress['attempts'], 'hint' => $progress['success_rate'] === null ? null : $progress['success_rate'].'% salen bien'],
                ['label' => 'Trabados', 'value' => $progress['stuck'], 'warn' => $progress['stuck'] > 0],
                ['label' => 'Entregas', 'value' => $practices['total'], 'hint' => $practices['approved'].' aprobadas'],
                ['label' => 'Para rehacer', 'value' => $practices['redo'], 'hint' => $practices['redo_rate'] === null ? null : $practices['redo_rate'].'% de lo corregido'],
                ['label' => 'Consultas', 'value' => $practices['questions']],
            ];
        @endphp
        <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">
            @foreach ($overview as $item)
                <div class="flex flex-col gap-0.5">
                    <span class="font-display text-2xl font-semibold {{ ($item['warn'] ?? false) ? 'text-[#fbbf24]' : 'text-white' }}">{{ $item['value'] }}</span>
                    <span class="text-sm text-ink">{{ $item['label'] }}</span>
                    @if ($item['hint'] ?? null)
                        <span class="text-xs text-ink-muted">{{ $item['hint'] }}</span>
                    @endif
                </div>
            @endforeach
        </div>
    </section>
</div>
