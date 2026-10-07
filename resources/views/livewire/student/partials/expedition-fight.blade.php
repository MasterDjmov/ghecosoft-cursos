{{-- La aventura turno por turno (D91): el registro que calculó el servidor, renglón por renglón, con las barras de
     vida. «Saltar» muestra todo de una. --}}
@php
    $log = $fight->log ?? [];
    $rewards = $fight->rewards ?? [];
    $colors = ['narr' => 'text-ink-muted', 'event' => 'text-secondary-bright', 'appear' => 'text-warning', 'hit' => 'text-white', 'spell' => 'text-primary-bright',
        'crit' => 'text-amber-300 font-semibold', 'miss' => 'text-ink-muted', 'enemy' => 'text-danger', 'dodge' => 'text-success', 'potion' => 'text-success', 'revive' => 'text-violet-300 font-semibold',
        'down' => 'text-success font-semibold', 'victory' => 'text-success font-semibold', 'defeat' => 'text-danger font-semibold'];
@endphp
<section class="panel flex flex-col gap-4 p-4" data-test="expedition-fight" wire:key="fight-{{ $fight->id }}"
    x-data="{
        log: @js($log), shown: 0, timer: null,
        get now() { return this.log[Math.max(0, this.shown - 1)] ?? {} },
        get done() { return this.shown >= this.log.length },
        play() { clearInterval(this.timer); this.timer = setInterval(() => { if (this.done) { clearInterval(this.timer); return; } this.shown++; this.$nextTick(() => this.$refs.list?.scrollTo({ top: 99999, behavior: 'smooth' })); }, 750); },
        skip() { clearInterval(this.timer); this.shown = this.log.length; },
    }" x-init="shown = 1; play()" x-on:livewire:navigating.window="clearInterval(timer)">
    <div class="flex flex-wrap items-center justify-between gap-2">
        <h2 class="font-display text-lg font-semibold text-white">{{ $rewards['place'] ?? $fight->place }} · {{ config('game.expedition.lengths.'.$fight->length.'.label') }}</h2>
        <button type="button" x-show="! done" x-on:click="skip()" class="text-sm text-primary-bright hover:underline" data-test="fight-skip">Saltar</button>
    </div>

    {{-- Las barras --}}
    <div class="grid gap-4 sm:grid-cols-2">
        <div class="flex items-center gap-3">
            @if ($heroImage)<img src="{{ $heroImage }}" alt="" class="size-14 rounded-xl border border-primary-bright/60 object-cover">@endif
            <div class="flex flex-1 flex-col gap-1">
                <div class="flex justify-between text-xs"><span class="text-white">{{ $protagonist['name'] }}</span><span class="font-mono text-success" x-text="(now.hp ?? 0) + ' / ' + (now.hp_max ?? 0)"></span></div>
                <div class="h-2.5 overflow-hidden rounded-full bg-surface-high"><div class="h-full rounded-full bg-success transition-all duration-500" :style="'width:' + ((now.hp ?? 0) / (now.hp_max || 1) * 100) + '%'"></div></div>
            </div>
        </div>
        <div class="flex items-center gap-3" x-show="now.enemy">
            <div class="flex flex-1 flex-col gap-1">
                <div class="flex justify-between text-xs"><span class="text-white capitalize" x-text="now.enemy"></span><span class="font-mono text-danger" x-text="(now.ehp ?? 0) + ' / ' + (now.emax ?? 0)"></span></div>
                <div class="h-2.5 overflow-hidden rounded-full bg-surface-high"><div class="h-full rounded-full bg-danger transition-all duration-500" :style="'width:' + ((now.ehp ?? 0) / (now.emax || 1) * 100) + '%'"></div></div>
            </div>
            <img :src="'{{ asset('img/personajes') }}/' + now.img + '.webp'" alt="" class="size-14 rounded-xl border border-danger/50 object-cover" :class="(now.ehp ?? 1) <= 0 ? 'grayscale opacity-50' : ''">
        </div>
    </div>

    {{-- El registro --}}
    <ol x-ref="list" class="flex max-h-72 flex-col gap-1 overflow-y-auto rounded-lg border border-outline bg-surface-lowest p-3 font-mono text-sm" data-test="fight-log">
        @foreach ($log as $n => $entry)
            <li x-show="shown > {{ $n }}" x-transition.opacity class="{{ $colors[$entry['t']] ?? 'text-ink' }}">› {{ $entry['text'] }}</li>
        @endforeach
    </ol>

    {{-- El resultado --}}
    <div x-show="done" x-cloak class="flex flex-col gap-2 rounded-lg border p-3 {{ $fight->won ? 'border-success/40 bg-success/10' : 'border-danger/40 bg-danger/10' }}" data-test="fight-result">
        @if ($fight->won)
            <p class="font-medium text-success">¡Volvió con el botín!</p>
            <div class="flex flex-wrap items-center gap-2 text-sm">
                <span class="flex items-center gap-1 rounded-lg border border-warning/40 bg-warning/10 px-2 py-1 text-warning"><x-gold-icon class="size-4" /> +{{ $rewards['gold'] ?? 0 }} de oro</span>
                @foreach ($rewards['items'] ?? [] as $loot)
                    <span class="rounded-lg border-2 px-2 py-1 text-xs {{ \App\Enums\ItemRarity::from($loot['rarity'])->classes() }}">{{ $loot['name'] }}{{ $loot['quantity'] > 1 ? ' ×'.$loot['quantity'] : '' }}</span>
                @endforeach
            </div>
        @else
            <p class="font-medium text-danger">Volvió sin botín.</p>
            <p class="text-sm text-ink">No perdió nada de lo que tenía. Probá mejorar el equipo en la tienda, subir atributos con oro o elegir un lugar de menor nivel.</p>
        @endif
        @if (($rewards['potions'] ?? 0) > 0)
            <p class="text-xs text-ink-muted">Usó {{ $rewards['potions'] }} {{ $rewards['potions'] === 1 ? 'poción' : 'pociones' }}.</p>
        @endif
    </div>
</section>
