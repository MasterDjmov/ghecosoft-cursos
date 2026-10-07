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

        @include('livewire.student.partials.hero-points', ['heading' => '2. Sus atributos', 'action' => 'takeControl', 'label' => 'Tomar el control de '.$protagonist['name']])
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
                @if ($editing)
                    <div class="panel p-4">
                        @include('livewire.student.partials.hero-points', ['heading' => 'Reacomodar los puntos', 'action' => 'redistribute', 'label' => 'Guardar', 'cancel' => true])
                    </div>
                @endif
                {{-- Atributos: se suben con oro --}}
                <section @class(['panel flex flex-col gap-3 p-4', 'hidden' => $editing]) data-test="hero-stats">
                    <div class="flex flex-wrap items-center justify-between gap-2">
                        <h2 class="font-display text-lg font-semibold text-white">Atributos</h2>
                        <span class="text-xs text-ink-muted">Cada punto cuesta 100 × su valor actual</span>
                    </div>
                    @if ($canRedistribute)
                        <p class="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-primary/30 bg-primary/5 px-3 py-2 text-xs text-ink">
                            <span>Mientras no compres puntos con oro, podés reacomodar los del principio gratis.</span>
                            <button type="button" wire:click="startEditing" class="text-primary-bright hover:underline" data-test="redistribute">Reacomodar puntos</button>
                        </p>
                    @endif
                    @foreach (\App\Models\Hero::STATS as $stat)
                        @php($cost = $hero->upgradeCost($stat))
                        <div class="flex items-center gap-3 rounded-lg border border-outline/70 p-2.5" wire:key="up-{{ $stat }}">
                            <span class="grid size-10 shrink-0 place-items-center rounded-md border border-primary/40 bg-primary/10 font-mono text-xs font-bold text-primary-bright">{{ \App\Models\Hero::statShort($stat) }}</span>
                            <div class="flex min-w-0 flex-1 flex-col">
                                <span class="font-medium text-white">{{ \App\Models\Hero::statLabel($stat) }} <span class="font-mono text-primary-bright" data-test="value-{{ $stat }}">{{ $hero->{$stat} }}</span>@if ($b = $hero->bonus($stat)) <span class="font-mono text-sm text-success" title="Por el equipo">{{ $b > 0 ? '+' : '' }}{{ $b }}</span>@endif</span>
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

                {{-- Equipo (D90): se equipa desde la mochila. --}}
                <section class="panel flex flex-col gap-3 p-4" data-test="hero-equipment">
                    <div class="flex flex-wrap items-center justify-between gap-2">
                        <h2 class="font-display text-lg font-semibold text-white">Equipo</h2>
                        <span class="font-mono text-xs text-ink-muted">ATQ {{ $hero->bonus('attack') }} · DEF {{ $hero->bonus('defense') }}</span>
                    </div>
                    <div class="grid gap-2 sm:grid-cols-3">
                        @foreach (\App\Enums\ItemKind::slots() as $slot)
                            @php($worn = $hero->equipment()->get($slot))
                            @php($kindOfSlot = \App\Enums\ItemKind::forSlot($slot))
                            <div @class(['flex flex-col items-center gap-1 rounded-lg border p-3 text-center', 'border-dashed border-outline' => ! $worn, $worn?->rarity->classes() => $worn]) data-test="slot-{{ $slot }}">
                                @if ($worn?->imageUrl())
                                    <img src="{{ $worn->imageUrl() }}" alt="" class="size-10 rounded object-cover">
                                @else
                                    <flux:icon :name="$kindOfSlot->icon()" @class(['text-ink-muted' => ! $worn]) />
                                @endif
                                <span class="text-xs text-ink-muted">{{ $kindOfSlot->label() }}</span>
                                <span class="text-sm text-white">{{ $worn?->name ?? 'Vacío' }}</span>
                                @if ($worn && ($bonuses = $worn->bonuses()))
                                    <span class="font-mono text-[11px] text-success">{{ implode(' · ', $bonuses) }}</span>
                                @endif
                            </div>
                        @endforeach
                    </div>
                    <div class="flex flex-wrap gap-2">
                        <flux:button size="sm" icon="shopping-bag" :href="route('student.inventory', ['solapa' => $course->slug])" wire:navigate data-test="hero-bag">Mochila: equipar</flux:button>
                        @if ($protagonist['expeditions'] ?? null)
                            <flux:button size="sm" icon="map" :href="route('student.expeditions', $course)" wire:navigate data-test="hero-expeditions">Expediciones</flux:button>
                            <flux:button size="sm" icon="trophy" :href="route('student.stables')" wire:navigate data-test="hero-stables">Establos</flux:button>
                        @endif
                        @if ($protagonist['shop'] ?? null)
                            <flux:button size="sm" icon="building-storefront" :href="route('student.shop', $course)" wire:navigate data-test="hero-shop">{{ $protagonist['shop']['name'] }}</flux:button>
                        @endif
                    </div>
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
