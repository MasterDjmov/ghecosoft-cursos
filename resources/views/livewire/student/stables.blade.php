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
                <p class="text-ink">Tocá una especie abajo para ver sus evoluciones y comprala en n1: las expediciones duran {{ $levels[1]['reduction'] }}% menos. Cuesta {{ $levels[1]['price'] }} de oro y pide nivel {{ $levels[1]['min_level'] }}.</p>
            </div>
        @endif
        @if ($mount && $next)
            <flux:button variant="primary" wire:click="buy" :disabled="$gold < $next['price'] || $playerLevel < $next['min_level']" data-test="mount-buy">
                Mejorar a n{{ $nextLevel }} · {{ number_format($next['price'], 0, ',', '.') }}
            </flux:button>
        @endif
    </section>

    <section class="flex flex-col gap-3">
        <h2 class="font-display text-lg font-semibold text-white">{{ $mount ? 'Cambiar de especie (gratis)' : 'Elegí la especie' }}</h2>
        <p class="-mt-2 text-sm text-ink-muted">Tocá una para ver cómo evoluciona de n1 a n5 antes de decidir.</p>
        <div class="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-7">
            @foreach ($allSpecies as $code => $name)
                <button type="button" wire:click="inspect('{{ $code }}')" wire:key="species-{{ $code }}" data-test="species-{{ $code }}"
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

    {{-- La ficha de una especie: sus 5 evoluciones, para saber qué se compra a largo plazo. --}}
    @if ($preview)
        @php $isMine = $mount && $mount->species === $preview; @endphp
        <div class="fixed inset-0 z-50 flex items-end justify-center bg-black/70 p-0 sm:items-center sm:p-6" wire:key="preview-{{ $preview }}"
            x-data x-on:keydown.escape.window="$wire.closePreview()" x-on:click.self="$wire.closePreview()" data-test="species-preview">
            <div class="panel flex max-h-[92vh] w-full max-w-4xl flex-col gap-4 overflow-y-auto p-4 sm:p-6">
                <header class="flex items-start justify-between gap-3">
                    <div>
                        <p class="tech-label">Montura</p>
                        <h2 class="font-display text-2xl font-semibold text-white">{{ $allSpecies[$preview] }}</h2>
                        <p class="text-sm text-ink-muted">Así evoluciona al subirla de nivel. La especie es solo el aspecto: la reducción depende del nivel.</p>
                    </div>
                    <flux:button size="sm" variant="ghost" icon="x-mark" wire:click="closePreview" aria-label="Cerrar" data-test="preview-close" />
                </header>
                <div class="grid grid-cols-2 gap-3 sm:grid-cols-5">
                    @foreach ($levels as $n => $level)
                        @php $reached = $isMine && $mount->level >= $n; @endphp
                        <figure @class(['flex flex-col gap-1 rounded-lg border p-2 text-center', 'border-success/60 bg-success/10' => $reached, 'border-outline' => ! $reached]) data-test="evolution-{{ $n }}">
                            <img src="{{ \App\Models\Mount::imageUrl($preview, $n) }}" alt="{{ $allSpecies[$preview] }} n{{ $n }}" class="aspect-square w-full rounded-md object-cover" loading="lazy">
                            <figcaption class="flex flex-col">
                                <span class="font-mono text-white">n{{ $n }} @if ($isMine && $mount->level === $n)<span class="text-xs text-success">· la tuya</span>@endif</span>
                                <span class="text-sm text-success">−{{ $level['reduction'] }}%</span>
                                <span class="text-xs text-ink-muted">{{ number_format($level['price'], 0, ',', '.') }} oro · nivel {{ $level['min_level'] }}</span>
                            </figcaption>
                        </figure>
                    @endforeach
                </div>
                <footer class="flex flex-wrap items-center justify-end gap-2">
                    <flux:button variant="ghost" wire:click="closePreview">Volver</flux:button>
                    @if ($isMine)
                        <span class="text-sm text-success">Es tu montura actual.</span>
                    @elseif ($mount)
                        <flux:button variant="primary" wire:click="choose('{{ $preview }}')" data-test="preview-choose">Cambiar a {{ $allSpecies[$preview] }} (gratis, sigue en n{{ $mount->level }})</flux:button>
                    @else
                        <flux:button variant="primary" wire:click="choose('{{ $preview }}')" :disabled="$gold < $levels[1]['price'] || $playerLevel < $levels[1]['min_level']" data-test="preview-choose">
                            Comprar {{ $allSpecies[$preview] }} en n1 · {{ number_format($levels[1]['price'], 0, ',', '.') }}
                        </flux:button>
                    @endif
                </footer>
            </div>
        </div>
    @endif
</div>
