<div class="mx-auto flex w-full max-w-6xl flex-col gap-8 p-4 sm:p-8">
    <header class="flex flex-col gap-1">
        <p class="tech-label"><span class="live-dot me-2"></span>Panel del docente</p>
        <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Inicio</h1>
        <p class="text-ink-muted">{{ $students }} {{ $students === 1 ? 'alumno registrado' : 'alumnos registrados' }}.</p>
    </header>

    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        @foreach ($counters as $counter)
            <div class="panel flex flex-col gap-3 p-5">
                <flux:icon :name="$counter['icon']" class="size-6 text-primary-bright" />
                <span class="font-display text-3xl font-semibold text-white">{{ $counter['value'] }}</span>
                <span class="text-sm text-ink-muted">{{ $counter['label'] }}</span>
            </div>
        @endforeach
    </div>
</div>
