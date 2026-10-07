{{-- Los establos (D91). --}}
<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-wrap items-end justify-between gap-3">
        <div class="flex flex-col gap-1">
            <p class="tech-label">El jugador</p>
            <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Establos</h1>
            <p class="text-ink-muted">Una montura para todos tus héroes: acorta las expediciones. La especie es solo el aspecto; lo que cuenta es el nivel. Tu nivel: <span class="font-mono text-primary-bright">{{ $playerLevel }}</span></p>
        </div>
        <div class="panel flex items-center gap-2 py-1.5 ps-2 pe-4" data-test="stables-gold">
            <x-gold-icon class="size-7" />
            <span class="font-mono text-lg font-semibold text-white">{{ number_format($gold, 0, ',', '.') }}</span>
        </div>
    </header>

    <section class="panel flex flex-col gap-4 p-4 sm:flex-row sm:items-center" data-test="stables-current">
        @if ($mount)
            <img src="{{ \App\Models\Mount::imageUrl($mount->species, $mount->level) }}" alt="" class="size-40 shrink-0 rounded-xl border border-primary-bright/50 object-cover">
            <div class="flex flex-1 flex-col gap-1">
                <p class="font-display text-2xl font-semibold text-white">{{ $mount->name() }} <span class="text-primary-bright">n{{ $mount->level }}</span></p>
                <p class="text-ink">Las expediciones duran <strong class="text-success">{{ $mount->reduction() }}% menos</strong>.</p>
                @if ($next)
                    <p class="text-sm text-ink-muted">n{{ $nextLevel }}: −{{ $next['reduction'] }}% · {{ number_format($next['price'], 0, ',', '.') }} de oro · nivel {{ $next['min_level'] }}</p>
                @else
                    <p class="text-sm text-success">Está al máximo.</p>
                @endif
            </div>
        @else
            <div class="flex flex-1 flex-col gap-1">
                <p class="font-display text-xl font-semibold text-white">Todavía no tenés montura</p>
                <p class="text-ink">Elegí una especie abajo y comprala en n1: las expediciones duran {{ $levels[1]['reduction'] }}% menos. Cuesta {{ $levels[1]['price'] }} de oro y pide nivel {{ $levels[1]['min_level'] }}.</p>
            </div>
        @endif
        @if ($next)
            <flux:button variant="primary" wire:click="buy" :disabled="(! $mount && ! $species) || $gold < $next['price'] || $playerLevel < $next['min_level']" data-test="mount-buy">
                {{ $mount ? 'Mejorar a n'.$nextLevel : 'Comprar en n1' }} · {{ number_format($next['price'], 0, ',', '.') }}
            </flux:button>
        @endif
    </section>

    <section class="flex flex-col gap-3">
        <h2 class="font-display text-lg font-semibold text-white">{{ $mount ? 'Cambiar de especie (gratis)' : 'Elegí la especie' }}</h2>
        <div class="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-7">
            @foreach ($allSpecies as $code => $name)
                <button type="button" wire:click="choose('{{ $code }}')" wire:key="species-{{ $code }}" data-test="species-{{ $code }}"
                    @class(['panel flex flex-col items-center gap-1 p-2 text-center transition', 'panel-active ring-2 ring-primary-bright' => $this->species === $code, 'opacity-80 hover:opacity-100' => $this->species !== $code])>
                    <img src="{{ \App\Models\Mount::imageUrl($code, $mount?->level ?? 1) }}" alt="" class="aspect-square w-full rounded-lg object-cover" loading="lazy">
                    <span class="text-xs text-white">{{ $name }}</span>
                </button>
            @endforeach
        </div>
    </section>

    <section class="panel flex flex-col gap-2 p-4 text-sm">
        <h2 class="font-display font-semibold text-white">Niveles</h2>
        <div class="grid gap-2 sm:grid-cols-5">
            @foreach ($levels as $n => $level)
                <div @class(['rounded-lg border p-2 text-center', 'border-success/50 bg-success/10' => ($mount?->level ?? 0) >= $n, 'border-outline' => ($mount?->level ?? 0) < $n])>
                    <p class="font-mono text-white">n{{ $n }}</p>
                    <p class="text-success">−{{ $level['reduction'] }}%</p>
                    <p class="text-xs text-ink-muted">{{ number_format($level['price'], 0, ',', '.') }} oro · nivel {{ $level['min_level'] }}</p>
                </div>
            @endforeach
        </div>
    </section>
</div>
