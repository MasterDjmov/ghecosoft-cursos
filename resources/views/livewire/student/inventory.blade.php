{{-- La mochila (D90): una solapa por mundo y una de comunes; se equipa a cada héroe desde acá. --}}
<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-wrap items-end justify-between gap-3">
        <div class="flex flex-col gap-1">
            <p class="tech-label">El jugador</p>
            <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Mochila</h1>
            <p class="text-ink-muted">Lo que conseguiste en las micro-misiones, en las tiendas y en las expediciones. Es una sola para todos tus héroes.</p>
        </div>
        <div class="panel flex items-center gap-2 py-1.5 ps-2 pe-4">
            <x-gold-icon class="size-7" />
            <span class="font-mono text-lg font-semibold text-white">{{ number_format($gold, 0, ',', '.') }}</span>
            <span class="text-sm text-ink-muted">de oro</span>
        </div>
    </header>

    <nav class="flex flex-wrap gap-2" aria-label="Mundos" data-test="bag-tabs">
        @foreach ($tabs as $option)
            <button type="button" wire:click="$set('tab', '{{ $option['key'] }}')" wire:key="tab-{{ $option['key'] }}"
                @class(['flex items-center gap-2 rounded-lg border px-3 py-2 text-sm transition', 'border-primary-bright bg-primary/10 text-white' => $current['key'] === $option['key'], 'border-outline text-ink-muted hover:text-white' => $current['key'] !== $option['key']])>
                @if ($option['course'])<x-course-logo :course="$option['course']" size="size-5" />@else<flux:icon name="globe-americas" variant="micro" />@endif
                {{ $option['label'] }}
            </button>
        @endforeach
    </nav>

    {{-- El equipo puesto de los héroes de esta solapa --}}
    @foreach ($heroes->filter(fn ($hero) => ! $current['course'] || $hero->course_id === $current['course']->id) as $hero)
        @php($who = $protagonist($hero))
        <section class="panel flex flex-col gap-3 p-4" wire:key="worn-{{ $hero->id }}" data-test="worn-{{ $hero->id }}">
            <div class="flex items-center justify-between gap-2">
                <h2 class="font-display font-semibold text-white">Lo que tiene puesto {{ $who['name'] ?? 'el héroe' }}</h2>
                <a href="{{ route('student.hero', $hero->course) }}" wire:navigate class="text-xs text-primary-bright hover:underline">Ver el panel</a>
            </div>
            <div class="grid gap-2 sm:grid-cols-3">
                @foreach (\App\Enums\ItemKind::slots() as $slot)
                    @php($worn = $hero->equipment()->get($slot))
                    <div class="flex items-center gap-2 rounded-lg border border-dashed border-outline p-2">
                        <flux:icon :name="\App\Enums\ItemKind::forSlot($slot)->icon()" variant="mini" class="text-ink-muted" />
                        <div class="flex min-w-0 flex-1 flex-col">
                            <span class="text-xs text-ink-muted">{{ \App\Enums\ItemKind::forSlot($slot)->label() }}</span>
                            <span class="truncate text-sm text-white">{{ $worn?->name ?? 'Vacío' }}</span>
                        </div>
                        @if ($worn)
                            <button type="button" wire:click="unequip({{ $hero->id }}, '{{ $slot }}')" class="text-xs text-ink-muted hover:text-danger" data-test="unequip-{{ $slot }}">Quitar</button>
                        @endif
                    </div>
                @endforeach
            </div>
        </section>
    @endforeach

    @forelse ($groups as $kind => $rows)
        <section class="flex flex-col gap-3" wire:key="group-{{ $kind }}">
            <h2 class="flex items-center gap-2 font-display text-lg font-semibold text-white">
                <flux:icon :name="\App\Enums\ItemKind::from($kind)->icon()" variant="mini" /> {{ \App\Enums\ItemKind::from($kind)->plural() }}
            </h2>
            <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                @foreach ($rows as $row)
                    @php($item = $row['item'])
                    <x-item-card :item="$item" :count="$row['owned']" wire:key="bag-{{ $item->id }}">
                        <div class="mt-auto flex flex-wrap items-center gap-2 border-t border-outline/60 pt-2 text-xs">
                            @if ($row['equipped'] > 0)
                                <span class="rounded bg-success/15 px-1.5 py-0.5 text-success">{{ $row['equipped'] === 1 ? 'Puesto' : 'Puestos: '.$row['equipped'] }}</span>
                            @endif
                            @if ($item->isEquippable())
                                @php($free = $row['owned'] - $row['equipped'])
                                @forelse ($heroesFor($item) as $hero)
                                    @if ($hero->{$item->kind->slot()} !== $item->id && $free > 0)
                                        <flux:button size="xs" wire:click="equip({{ $item->id }}, {{ $hero->id }})" data-test="equip-{{ $item->code }}">Equipar a {{ $protagonist($hero)['name'] ?? 'tu héroe' }}</flux:button>
                                    @endif
                                @empty
                                    <span class="text-ink-muted">Tomá el control del héroe de este mundo para equiparlo.</span>
                                @endforelse
                            @elseif ($item->code === \App\Models\Item::RESPEC)
                                @foreach ($heroesFor($item) as $hero)
                                    <flux:button size="xs" wire:click="useOn({{ $item->id }}, {{ $hero->id }})" wire:confirm="¿Usar el pergamino con {{ $protagonist($hero)['name'] ?? 'este héroe' }}? Vas a poder reacomodar sus puntos del principio una vez." data-test="use-respec">Usar con {{ $protagonist($hero)['name'] ?? 'el héroe' }}</flux:button>
                                @endforeach
                            @elseif ($item->code === \App\Models\Item::HOURGLASS)
                                <span class="text-ink-muted">Se usa en Expediciones, con una en camino: termina al instante.</span>
                            @elseif ($item->kind === \App\Enums\ItemKind::Potion)
                                <span class="text-ink-muted">Se toma sola en las expediciones si la vida baja mucho.</span>
                            @elseif ($item->kind === \App\Enums\ItemKind::Material)
                                <span class="text-ink-muted">Material: pronto, para fabricar.</span>
                            @endif
                        </div>
                    </x-item-card>
                @endforeach
            </div>
        </section>
    @empty
        <div class="panel flex items-start gap-4 p-4" data-test="bag-empty">
            <img src="{{ asset('img/personajes/gheco.webp') }}" alt="" class="size-14 shrink-0 rounded-full border border-primary/40 object-cover">
            <p class="text-sm text-ink">—Nada por acá todavía. Las micro-misiones de la historia, la tienda de cada mundo y las expediciones llenan la mochila.</p>
        </div>
    @endforelse
</div>
