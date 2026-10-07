{{-- Mis héroes (D89): un protagonista por mundo. --}}
<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-wrap items-end justify-between gap-3">
        <div class="flex flex-col gap-1">
            <p class="tech-label">El jugador</p>
            <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Mis héroes</h1>
            <p class="text-ink-muted">Cada mundo tiene su protagonista. Vos sos la mente que los mueve: el oro es uno solo, para todos.</p>
        </div>
        <div class="panel flex items-center gap-2 py-1.5 ps-2 pe-4">
            <x-gold-icon class="size-7" />
            <span class="font-mono text-lg font-semibold text-white">{{ number_format($gold, 0, ',', '.') }}</span>
            <span class="text-sm text-ink-muted">de oro</span>
        </div>
    </header>

    @forelse ($cards as $card)
        <a href="{{ route('student.hero', $card['course']) }}" wire:navigate wire:key="hero-{{ $card['course']->id }}" data-test="hero-{{ $card['course']->slug }}"
            class="panel flex items-center gap-4 p-4 transition hover:border-primary-bright/60">
            <img src="{{ $card['image'] }}" alt="" class="size-20 shrink-0 rounded-xl border border-primary/40 object-cover">
            <div class="flex min-w-0 flex-1 flex-col gap-1">
                <p class="font-display text-xl font-semibold text-white">{{ $card['protagonist']['name'] }}</p>
                <p class="flex items-center gap-2 text-sm text-ink-muted"><x-course-logo :course="$card['course']" size="size-5" /> {{ $card['course']->title }}</p>
                @if ($card['hero'])
                    <p class="flex flex-wrap gap-x-3 font-mono text-xs text-ink">
                        @foreach (\App\Models\Hero::STATS as $stat)
                            <span>{{ \App\Models\Hero::statShort($stat) }} <span class="text-primary-bright">{{ $card['hero']->{$stat} }}</span></span>
                        @endforeach
                        <span class="text-success">Vida {{ $card['hero']->hp() }}</span>
                    </p>
                @endif
            </div>
            @if ($card['hero'])
                <flux:icon name="chevron-right" class="text-ink-muted" />
            @else
                <span class="rounded-md border border-warning/50 bg-warning/10 px-3 py-1.5 text-sm text-warning">Tomá el control</span>
            @endif
        </a>
    @empty
        <div class="panel p-4 text-sm text-ink-muted" data-test="heroes-empty">
            Cuando entres a un mundo, acá vas a encontrar a su protagonista.
            <a href="{{ route('student.worlds') }}" wire:navigate class="text-primary-bright hover:underline">Ver los mundos</a>
        </div>
    @endforelse
</div>
