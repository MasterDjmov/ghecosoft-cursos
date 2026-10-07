{{-- El protagonista del curso (D89): «Tomá el control» la primera vez; después, su panel. --}}
<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-wrap items-end justify-between gap-3">
        <div class="flex flex-col gap-1">
            <a href="{{ route('student.course', $course) }}" wire:navigate class="tech-label hover:text-white">← {{ $course->title }}</a>
            <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">
                {{ $hero ? $protagonist['name'] : 'Tomá el control de '.$protagonist['name'] }}
            </h1>
            <p class="text-ink-muted">{{ $hero ? $protagonist['title'].' · '.$course->title : 'Vos sos la mente que mueve a '.$protagonist['name'].'. Elegí cómo se ve y repartí sus puntos.' }}</p>
        </div>
        <div class="panel flex items-center gap-2 py-1.5 ps-2 pe-4" data-test="hero-gold">
            <x-gold-icon class="size-7" />
            <span class="font-mono text-lg font-semibold text-white">{{ number_format($gold, 0, ',', '.') }}</span>
            <span class="text-sm text-ink-muted">de oro</span>
        </div>
    </header>

    @if (! $hero)
        {{-- Tomá el control: el aspecto y los 24 puntos. --}}
        <div class="panel flex items-start gap-4 p-4" data-test="hero-intro">
            <img src="{{ asset('img/personajes/profe.webp') }}" alt="" class="size-14 shrink-0 rounded-full border border-secondary/40 object-cover">
            <div class="flex flex-col gap-1 text-sm">
                <p class="font-medium text-white">El Profe</p>
                <p class="text-ink">—Cada mundo tiene su protagonista, y vos lo manejás. El <strong>aspecto</strong> es cosmético: lo podés cambiar cuando quieras. Los <strong>atributos</strong> sí cuentan en las expediciones y las peleas, y quedan fijos: después solo se suben con <strong>oro</strong>, que ganás superando micro-misiones.</p>
            </div>
        </div>

        <section class="flex flex-col gap-3">
            <h2 class="font-display text-lg font-semibold text-white">1. Su aspecto</h2>
            <div class="grid grid-cols-2 gap-3 sm:grid-cols-3" role="radiogroup" aria-label="Aspecto">
                @foreach ($looks as $option)
                    <button type="button" wire:click="changeLook({{ $option['n'] }})" wire:key="look-{{ $option['n'] }}" role="radio" aria-checked="{{ $look === $option['n'] ? 'true' : 'false' }}" data-test="look-{{ $option['n'] }}"
                        @class(['panel flex flex-col items-center gap-2 p-3 text-center transition', 'panel-active ring-2 ring-primary-bright' => $look === $option['n'], 'opacity-80 hover:opacity-100' => $look !== $option['n']])>
                        <img src="{{ $option['url'] }}" alt="" class="aspect-square w-full rounded-lg object-cover" loading="lazy">
                        <span class="text-sm font-medium text-white">{{ $option['name'] }}</span>
                    </button>
                @endforeach
            </div>
        </section>

        <section class="flex flex-col gap-3" x-data="{
                stats: $wire.entangle('stats'),
                total: {{ \App\Models\Hero::POINTS }}, min: {{ \App\Models\Hero::MIN_STAT }}, max: {{ \App\Models\Hero::MAX_START }},
                get used() { return Object.values(this.stats).reduce((a, b) => a + Number(b), 0) },
                get left() { return this.total - this.used },
                add(stat, delta) {
                    const value = Number(this.stats[stat]) + delta;
                    if (value < this.min || value > this.max || (delta > 0 && this.left <= 0)) return;
                    this.stats[stat] = value;
                },
            }">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <h2 class="font-display text-lg font-semibold text-white">2. Sus atributos</h2>
                <span class="rounded-md border px-2 py-1 font-mono text-sm" :class="left === 0 ? 'border-success/50 text-success' : 'border-warning/50 text-warning'" data-test="points-left">
                    Puntos sin repartir: <span x-text="left"></span>
                </span>
            </div>
            <p class="text-sm text-ink-muted">Repartí {{ \App\Models\Hero::POINTS }} puntos. Cada atributo va de {{ \App\Models\Hero::MIN_STAT }} a {{ \App\Models\Hero::MAX_START }}.</p>
            <div class="grid gap-3 sm:grid-cols-2">
                @foreach (\App\Models\Hero::STATS as $stat)
                    <div class="panel flex items-center gap-3 p-3" wire:key="stat-{{ $stat }}">
                        <span class="grid size-10 shrink-0 place-items-center rounded-md border border-primary/40 bg-primary/10 font-mono text-xs font-bold text-primary-bright">{{ \App\Models\Hero::statShort($stat) }}</span>
                        <div class="flex min-w-0 flex-1 flex-col">
                            <span class="font-medium text-white">{{ \App\Models\Hero::statLabel($stat) }}</span>
                            <span class="text-xs text-ink-muted">{{ \App\Models\Hero::statHelp($stat) }}</span>
                        </div>
                        <div class="flex items-center gap-1.5">
                            <flux:button size="sm" variant="ghost" icon="minus" x-on:click="add('{{ $stat }}', -1)" aria-label="Bajar {{ \App\Models\Hero::statLabel($stat) }}" />
                            <span class="w-7 text-center font-mono text-lg font-semibold text-white" x-text="stats.{{ $stat }}" data-test="stat-{{ $stat }}"></span>
                            <flux:button size="sm" variant="ghost" icon="plus" x-on:click="add('{{ $stat }}', 1)" aria-label="Subir {{ \App\Models\Hero::statLabel($stat) }}" />
                        </div>
                    </div>
                @endforeach
            </div>
            <p class="flex flex-wrap gap-4 font-mono text-sm text-ink-muted">
                <span>Vida: <span class="text-success" x-text="50 + 10 * stats.strength"></span></span>
                <span>Maná: <span class="text-primary-bright" x-text="20 + 5 * stats.intelligence"></span></span>
            </p>
            <flux:error name="stats" />
            <div class="flex justify-end">
                <flux:button variant="primary" icon="bolt" wire:click="takeControl" x-bind:disabled="left !== 0" data-test="take-control">
                    Tomar el control de {{ $protagonist['name'] }}
                </flux:button>
            </div>
        </section>
    @else
        <div class="grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.3fr)]">
            {{-- Retrato, nivel, vida y maná --}}
            <section class="panel flex flex-col gap-4 p-4" data-test="hero-card">
                <div class="flex items-center gap-4">
                    <img src="{{ \App\Services\Heroes::lookUrl($protagonist, $hero->look) }}" alt="{{ $protagonist['name'] }}" class="size-28 shrink-0 rounded-xl border-2 border-primary-bright/60 object-cover shadow-[0_0_24px_rgba(56,189,248,.25)]" data-test="hero-look">
                    <div class="flex min-w-0 flex-col gap-1">
                        <p class="font-display text-2xl font-semibold text-white">{{ $protagonist['name'] }}</p>
                        <p class="text-sm text-secondary-bright">{{ $protagonist['looks'][$hero->look] }}</p>
                        <p class="font-mono text-xs text-ink-muted">
                            {{ $level?->name() ?? \Illuminate\Support\Str::ucfirst(term('level')).' 1' }} · {{ auth()->user()->xp_total }} {{ term('xp.short') }}
                            @if ($nextLevel)
                                <span class="block">Faltan {{ $nextLevel->xp_required - auth()->user()->xp_total }} {{ term('xp.short') }} para el próximo</span>
                            @endif
                        </p>
                        <flux:modal.trigger name="looks">
                            <button type="button" class="self-start text-xs text-primary-bright hover:underline" data-test="change-look">Cambiar aspecto</button>
                        </flux:modal.trigger>
                    </div>
                </div>
                <div class="flex flex-col gap-2">
                    <div class="flex items-center justify-between text-sm"><span class="text-success">Vida</span><span class="font-mono text-white" data-test="hero-hp">{{ $hero->hp() }} / {{ $hero->hp() }}</span></div>
                    <div class="h-2 overflow-hidden rounded-full bg-surface-high"><div class="h-full w-full rounded-full bg-success"></div></div>
                    <div class="flex items-center justify-between text-sm"><span class="text-primary-bright">Maná</span><span class="font-mono text-white" data-test="hero-mp">{{ $hero->mp() }} / {{ $hero->mp() }}</span></div>
                    <div class="h-2 overflow-hidden rounded-full bg-surface-high"><div class="h-full w-full rounded-full bg-primary-bright"></div></div>
                </div>
                <div class="grid grid-cols-2 gap-2 text-center text-sm">
                    <div class="rounded-lg border border-outline p-2"><p class="font-mono text-lg text-white">{{ $courseXp }}</p><p class="text-xs text-ink-muted">{{ term('xp.short') }} en este mundo</p></div>
                    <a href="{{ route('student.grimoire') }}" wire:navigate class="rounded-lg border border-secondary/40 p-2 hover:bg-secondary/10" data-test="hero-grimoire">
                        <p class="font-mono text-lg text-secondary-bright">{{ $cards }}</p><p class="text-xs text-ink-muted">cartas del grimorio</p>
                    </a>
                </div>
            </section>

            <div class="flex flex-col gap-6">
                {{-- Atributos: se suben con oro --}}
                <section class="panel flex flex-col gap-3 p-4" data-test="hero-stats">
                    <div class="flex flex-wrap items-center justify-between gap-2">
                        <h2 class="font-display text-lg font-semibold text-white">Atributos</h2>
                        <span class="text-xs text-ink-muted">Cada punto cuesta 100 × su valor actual</span>
                    </div>
                    @foreach (\App\Models\Hero::STATS as $stat)
                        @php($cost = $hero->upgradeCost($stat))
                        <div class="flex items-center gap-3 rounded-lg border border-outline/70 p-2.5" wire:key="up-{{ $stat }}">
                            <span class="grid size-10 shrink-0 place-items-center rounded-md border border-primary/40 bg-primary/10 font-mono text-xs font-bold text-primary-bright">{{ \App\Models\Hero::statShort($stat) }}</span>
                            <div class="flex min-w-0 flex-1 flex-col">
                                <span class="font-medium text-white">{{ \App\Models\Hero::statLabel($stat) }} <span class="font-mono text-primary-bright" data-test="value-{{ $stat }}">{{ $hero->{$stat} }}</span></span>
                                <span class="text-xs text-ink-muted">{{ \App\Models\Hero::statHelp($stat) }}</span>
                            </div>
                            @if ($hero->{$stat} >= \App\Models\Hero::MAX_STAT)
                                <span class="text-xs text-success">Al máximo</span>
                            @else
                                <flux:button size="sm" wire:click="upgrade('{{ $stat }}')" :disabled="$gold < $cost" data-test="upgrade-{{ $stat }}">
                                    <span class="flex items-center gap-1">+1 · <x-gold-icon class="size-4" /> {{ number_format($cost, 0, ',', '.') }}</span>
                                </flux:button>
                            @endif
                        </div>
                    @endforeach
                </section>

                {{-- Equipo: llega con la tienda y las expediciones (fases B y C) --}}
                <section class="panel flex flex-col gap-3 p-4" data-test="hero-equipment">
                    <h2 class="font-display text-lg font-semibold text-white">Equipo</h2>
                    <div class="grid grid-cols-3 gap-2">
                        @foreach (['Arma' => 'bolt', 'Ropa' => 'shield-check', 'Accesorio' => 'sparkles'] as $slot => $icon)
                            <div class="flex flex-col items-center gap-1 rounded-lg border border-dashed border-outline p-3 text-center">
                                <flux:icon :name="$icon" class="text-ink-muted" />
                                <span class="text-sm text-white">{{ $slot }}</span>
                                <span class="text-xs text-ink-muted">Vacío</span>
                            </div>
                        @endforeach
                    </div>
                    <p class="text-xs text-ink-muted">Pronto: el puesto de Baldo y las expediciones por el Valle.</p>
                </section>
            </div>
        </div>

        <flux:modal name="looks" class="w-full max-w-2xl">
            <div class="flex flex-col gap-4">
                <flux:heading size="lg">El aspecto de {{ $protagonist['name'] }}</flux:heading>
                <flux:text>Es solo cosmético: no cambia nada del juego.</flux:text>
                <div class="grid grid-cols-2 gap-3 sm:grid-cols-3">
                    @foreach ($looks as $option)
                        <button type="button" wire:click="changeLook({{ $option['n'] }})" wire:key="modal-look-{{ $option['n'] }}"
                            @class(['panel flex flex-col items-center gap-2 p-2 text-center', 'panel-active ring-2 ring-primary-bright' => $hero->look === $option['n']])>
                            <img src="{{ $option['url'] }}" alt="" class="aspect-square w-full rounded-lg object-cover" loading="lazy">
                            <span class="text-xs text-white">{{ $option['name'] }}</span>
                        </button>
                    @endforeach
                </div>
            </div>
        </flux:modal>
    @endif
</div>
