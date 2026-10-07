{{-- El taller (crafteo, D93). --}}
<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-wrap items-end justify-between gap-3">
        <div class="flex flex-col gap-1">
            <p class="tech-label">El jugador</p>
            <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Taller</h1>
            <p class="text-ink-muted">Con los materiales que traen las expediciones se mejoran las armas, la ropa y los accesorios. Cada receta tarda un rato; mientras tanto, seguí jugando. Tu nivel: <span class="font-mono text-primary-bright">{{ $level }}</span></p>
        </div>
        <a href="{{ route('student.inventory') }}" wire:navigate class="panel flex items-center gap-2 px-3 py-2 text-sm text-ink hover:text-white"><flux:icon name="shopping-bag" variant="mini" /> Mochila</a>
    </header>

    {{-- Lo que se está fabricando --}}
    @if ($active)
        <section class="panel panel-active flex flex-wrap items-center gap-4 p-4" data-test="craft-active" wire:key="craft-{{ $active->id }}-{{ $active->ends_at->timestamp }}"
            x-data="{ left: {{ (int) max(0, ceil(now()->diffInSeconds($active->ends_at, false))) }}, t: null }"
            x-init="t = setInterval(() => { if (left > 0) left--; }, 1000)" x-on:livewire:navigating.window="clearInterval(t)">
            <div class="flex min-w-0 flex-1 items-center gap-3">
                <flux:icon name="wrench-screwdriver" class="size-8 shrink-0 text-primary-bright" />
                <div class="flex flex-col">
                    <p class="tech-label text-primary-bright">En el taller</p>
                    <p class="font-display text-lg font-semibold text-white">{{ $active->item->name }}{{ $active->quantity > 1 ? ' ×'.$active->quantity : '' }}</p>
                </div>
            </div>
            <span class="font-mono text-2xl text-primary-bright" x-show="left > 0" x-text="String(Math.floor(left / 60)).padStart(2, '0') + ':' + String(left % 60).padStart(2, '0')"></span>
            <flux:button variant="primary" icon="check" wire:click="collect" x-show="left <= 0" x-cloak data-test="craft-collect">Recoger</flux:button>
        </section>
    @endif

    <section class="grid gap-4 lg:grid-cols-2">
        @forelse ($recipes as $recipe)
            @php
                $ready = collect($recipe['needs'])->every(fn ($need) => $have($need['item']) >= $need['quantity']);
                $levelOk = $level >= $recipe['min_level'];
            @endphp
            <article class="panel flex flex-col gap-3 p-4" wire:key="recipe-{{ $recipe['code'] }}" data-test="recipe-{{ $recipe['code'] }}">
                <x-item-card :item="$recipe['gives']" :count="$recipe['quantity'] > 1 ? $recipe['quantity'] : null" class="border" />
                <div class="flex flex-col gap-1.5">
                    <p class="tech-label">Necesitás</p>
                    @foreach ($recipe['needs'] as $need)
                        @php $got = $have($need['item']); @endphp
                        <div class="flex flex-wrap items-center gap-x-2 gap-y-0.5 text-sm" data-test="need-{{ $need['item']->code }}">
                            <span @class(['font-mono', 'text-success' => $got >= $need['quantity'], 'text-warning' => $got < $need['quantity']])>{{ min($got, $need['quantity']) }}/{{ $need['quantity'] }}</span>
                            <span class="text-white">{{ $need['item']->name }}</span>
                            @if ($got < $need['quantity'])
                                @if ($where = $sources($need['item']))
                                    <span class="w-full ps-10 text-xs text-ink-muted">Cae en: {{ implode(', ', array_slice($where, 0, 4)) }}{{ count($where) > 4 ? '…' : '' }}</span>
                                @elseif ($need['item']->in_shop)
                                    <span class="w-full ps-10 text-xs text-ink-muted">Se compra en la tienda de su mundo.</span>
                                @endif
                            @endif
                        </div>
                    @endforeach
                </div>
                <div class="mt-auto flex flex-wrap items-center justify-between gap-2 border-t border-outline/60 pt-3">
                    <span class="flex items-center gap-1 text-sm text-ink-muted"><flux:icon name="clock" variant="micro" />
                        {{ ($s = $seconds($recipe)) >= 60 ? round($s / 60).' min' : $s.' s' }} · nivel {{ $recipe['min_level'] }}</span>
                    <flux:button size="sm" variant="primary" wire:click="craft('{{ $recipe['code'] }}')" :disabled="! $ready || ! $levelOk || $active" data-test="craft-{{ $recipe['code'] }}">
                        {{ ! $levelOk ? 'Pide nivel '.$recipe['min_level'] : ($active ? 'Taller ocupado' : 'Fabricar') }}
                    </flux:button>
                </div>
            </article>
        @empty
            <p class="text-ink-muted" data-test="workshop-empty">Todavía no hay recetas.</p>
        @endforelse
    </section>
</div>
