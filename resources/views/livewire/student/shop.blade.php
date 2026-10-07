{{-- La tienda del mundo (D90). --}}
<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-wrap items-end justify-between gap-3">
        <div class="flex flex-col gap-1">
            <a href="{{ route('student.hero', $course) }}" wire:navigate class="tech-label hover:text-white">← Mi héroe</a>
            <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">{{ $shop['name'] }}</h1>
            <p class="text-ink-muted">{{ $course->title }} · tu nivel: <span class="font-mono text-primary-bright">{{ $level }}</span></p>
        </div>
        <div class="flex items-center gap-2">
            <a href="{{ route('student.inventory') }}" wire:navigate class="panel flex items-center gap-2 px-3 py-2 text-sm text-ink hover:text-white"><flux:icon name="shopping-bag" variant="mini" /> Mochila</a>
            <div class="panel flex items-center gap-2 py-1.5 ps-2 pe-4" data-test="shop-gold">
                <x-gold-icon class="size-7" />
                <span class="font-mono text-lg font-semibold text-white">{{ number_format($gold, 0, ',', '.') }}</span>
            </div>
        </div>
    </header>

    <div class="panel flex items-start gap-4 p-4">
        <img src="{{ asset($shop['portrait']) }}" alt="" class="size-14 shrink-0 rounded-full border border-warning/50 object-cover">
        <div class="flex flex-col gap-1 text-sm">
            <p class="font-medium text-white">{{ $shop['keeper'] }}</p>
            <p class="text-ink">{{ $shop['greeting'] }}</p>
        </div>
    </div>

    <nav class="flex flex-wrap gap-2" aria-label="Tipo">
        @foreach ($kinds as $option)
            <button type="button" wire:click="$set('kind', '{{ $option->value }}')" wire:key="kind-{{ $option->value }}" data-test="shop-tab-{{ $option->value }}"
                @class(['flex items-center gap-2 rounded-lg border px-3 py-2 text-sm transition', 'border-warning bg-warning/10 text-white' => $kind === $option->value, 'border-outline text-ink-muted hover:text-white' => $kind !== $option->value])>
                <flux:icon :name="$option->icon()" variant="micro" /> {{ $option->plural() }}
            </button>
        @endforeach
    </nav>

    <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        @forelse ($items as $item)
            <x-item-card :item="$item" wire:key="shop-{{ $item->id }}">
                <div class="mt-auto flex items-center justify-between gap-2 border-t border-outline/60 pt-2">
                    <span class="flex items-center gap-1 font-mono text-sm text-white"><x-gold-icon class="size-4" /> {{ number_format($item->price, 0, ',', '.') }}</span>
                    @if (($owned[$item->id] ?? 0) > 0)
                        <span class="text-xs text-ink-muted">Tenés {{ $owned[$item->id] }}</span>
                    @endif
                    @if ($level < $item->min_level)
                        <span class="text-xs text-warning">Nivel {{ $item->min_level }}</span>
                    @else
                        <flux:button size="sm" variant="primary" wire:click="buy({{ $item->id }})" :disabled="$gold < $item->price" data-test="buy-{{ $item->code }}">Comprar</flux:button>
                    @endif
                </div>
            </x-item-card>
        @empty
            <p class="text-sm text-ink-muted">{{ $shop['keeper'] }} no tiene nada de esto por ahora.</p>
        @endforelse
    </div>
</div>
