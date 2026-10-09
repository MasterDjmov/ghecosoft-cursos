@props(['item', 'count' => null, 'zoom' => null])

{{-- Un ítem del juego (D90): marco por rareza, imagen (o el ícono de su tipo), nombre, tipo y bonos. El slot es para las acciones. Un clic en la imagen abre la ficha grande. --}}
@php($zoom ??= 'item-card-'.$item->id)
<article {{ $attributes->class(['flex flex-col gap-2 rounded-xl border-2 bg-surface-low/80 p-3', $item->rarity->classes()]) }} data-test="item-{{ $item->code }}">
    <div class="flex items-start gap-3">
        <flux:modal.trigger :name="$zoom">
            <button type="button" class="relative grid size-24 shrink-0 cursor-zoom-in place-items-center overflow-hidden rounded-lg border border-outline bg-surface-lowest transition hover:border-primary-bright" aria-label="Ver {{ $item->name }} en grande">
                @if ($url = $item->thumbUrl())
                    <img src="{{ $url }}" alt="" class="size-full object-cover" loading="lazy">
                @else
                    <flux:icon :name="$item->kind->icon()" class="size-9" />
                @endif
                @if ($count !== null)
                    <span class="absolute right-0.5 bottom-0.5 rounded bg-[#05070d]/90 px-1 font-mono text-[11px] text-white">×{{ $count }}</span>
                @endif
            </button>
        </flux:modal.trigger>
        <div class="flex min-w-0 flex-1 flex-col gap-0.5">
            <p class="font-medium text-white">{{ $item->name }}</p>
            <p class="text-[11px] tracking-wide uppercase">{{ $item->rarity->label() }} · {{ $item->kind->label() }}{{ $item->course ? '' : ' · común' }}</p>
            @if ($bonuses = $item->bonuses())
                <p class="font-mono text-xs text-success">{{ implode(' · ', $bonuses) }}</p>
            @endif
        </div>
    </div>
    @if ($item->description)
        <p class="text-xs text-ink-muted">{{ $item->description }}</p>
    @endif
    {{ $slot }}
    <x-item-zoom :item="$item" :name="$zoom" :count="$count" />
</article>
