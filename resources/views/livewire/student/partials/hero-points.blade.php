{{-- El reparto de los 24 puntos (D89): al tomar el control y al reacomodarlos. $action: el método que guarda. --}}
<section class="flex flex-col gap-3" data-test="hero-points" x-data="{
        stats: $wire.entangle('stats'),
        total: {{ \App\Models\Hero::POINTS }}, min: {{ \App\Models\Hero::MIN_STAT }}, max: {{ \App\Models\Hero::MAX_START }},
        hint: '',
        get used() { return Object.values(this.stats).reduce((a, b) => a + Number(b), 0) },
        get left() { return this.total - this.used },
        add(stat, delta) {
            const value = Number(this.stats[stat]) + delta;
            if (delta > 0 && this.left <= 0) { this.hint = 'No te quedan puntos: bajá otro atributo para subir este.'; return; }
            if (value > this.max) { this.hint = 'Al empezar, cada atributo llega hasta ' + this.max + '.'; return; }
            if (value < this.min) { this.hint = 'Cada atributo tiene por lo menos ' + this.min + '.'; return; }
            this.hint = '';
            this.stats = { ...this.stats, [stat]: value };
        },
    }">
    <div class="flex flex-wrap items-center justify-between gap-2">
        <h2 class="font-display text-lg font-semibold text-white">{{ $heading }}</h2>
        <span class="rounded-md border px-2 py-1 font-mono text-sm" :class="left === 0 ? 'border-success/50 text-success' : 'border-warning/50 text-warning'" data-test="points-left">
            Puntos libres: <span x-text="left"></span>
        </span>
    </div>
    <p class="text-sm text-ink-muted">Repartí {{ \App\Models\Hero::POINTS }} puntos con <strong>+</strong> y <strong>−</strong>. Cada atributo va de {{ \App\Models\Hero::MIN_STAT }} a {{ \App\Models\Hero::MAX_START }}.</p>
    <div class="grid gap-3 sm:grid-cols-2">
        @foreach (\App\Models\Hero::STATS as $stat)
            <div class="panel flex items-center gap-3 p-3" wire:key="stat-{{ $stat }}">
                <span class="grid size-10 shrink-0 place-items-center rounded-md border border-primary/40 bg-primary/10 font-mono text-xs font-bold text-primary-bright">{{ \App\Models\Hero::statShort($stat) }}</span>
                <div class="flex min-w-0 flex-1 flex-col">
                    <span class="font-medium text-white">{{ \App\Models\Hero::statLabel($stat) }}</span>
                    <span class="text-xs text-ink-muted">{{ \App\Models\Hero::statHelp($stat) }}</span>
                </div>
                <div class="flex items-center gap-1.5">
                    <button type="button" x-on:click="add('{{ $stat }}', -1)" aria-label="Bajar {{ \App\Models\Hero::statLabel($stat) }}" data-test="minus-{{ $stat }}"
                        class="grid size-9 place-items-center rounded-md border border-outline text-lg text-white hover:border-primary-bright hover:bg-primary/10">−</button>
                    <span class="w-7 text-center font-mono text-lg font-semibold text-white" x-text="stats.{{ $stat }}" data-test="stat-{{ $stat }}"></span>
                    <button type="button" x-on:click="add('{{ $stat }}', 1)" aria-label="Subir {{ \App\Models\Hero::statLabel($stat) }}" data-test="plus-{{ $stat }}"
                        class="grid size-9 place-items-center rounded-md border border-outline text-lg text-white hover:border-primary-bright hover:bg-primary/10">+</button>
                </div>
            </div>
        @endforeach
    </div>
    <p x-show="hint" x-text="hint" class="text-sm text-warning" x-cloak></p>
    <p class="flex flex-wrap gap-4 font-mono text-sm text-ink-muted">
        <span>Vida: <span class="text-success" x-text="50 + 10 * stats.strength"></span></span>
        <span>Maná: <span class="text-primary-bright" x-text="20 + 5 * stats.intelligence"></span></span>
    </p>
    <flux:error name="stats" />
    <div class="flex flex-wrap items-center justify-end gap-3">
        <span x-show="left > 0" class="text-sm text-ink-muted">Te faltan repartir <span x-text="left"></span> puntos.</span>
        @isset($cancel)
            <flux:button variant="ghost" wire:click="$set('editing', false)">Cancelar</flux:button>
        @endisset
        <button type="button" wire:click="{{ $action }}" x-bind:disabled="left !== 0" data-test="{{ $action === 'takeControl' ? 'take-control' : 'save-points' }}"
            class="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 font-medium text-white transition hover:bg-primary-bright disabled:cursor-not-allowed disabled:opacity-40">
            <flux:icon name="bolt" variant="mini" /> {{ $label }}
        </button>
    </div>
</section>
