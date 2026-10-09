@props(['item', 'zoom', 'count' => null, 'label' => null, 'badge' => null])

{{--
    Un ítem como casillero (D90, al estilo de las mochilas de los RPG): la imagen grande con el marco de su rareza.
    Pasando el mouse se ven sus datos; con un clic (o tocándolo en el celular) se abre la ficha grande ($zoom).
--}}
{{-- El modal.trigger va afuera: es «display: contents» (no tiene caja), y si el tooltip lo toma de ancla sale en la esquina de la pantalla. --}}
<flux:modal.trigger :name="$zoom">
    <flux:tooltip position="bottom" class="w-full">
        <button type="button" {{ $attributes->class(['group relative block aspect-square w-full overflow-hidden rounded-xl border-2 bg-surface-lowest transition hover:-translate-y-0.5 hover:shadow-[0_0_18px_-4px_currentColor] focus-visible:outline-2 focus-visible:outline-primary-bright', $item->rarity->classes()]) }} aria-label="{{ $item->name }}" data-test="tile-{{ $item->code }}">
            @if ($url = $item->thumbUrl())
                <img src="{{ $url }}" alt="" class="size-full object-cover" loading="lazy">
            @else
                <span class="grid size-full place-items-center"><flux:icon :name="$item->kind->icon()" class="size-10" /></span>
            @endif
            @if ($count !== null && $count > 1)
                <span class="absolute right-1 bottom-1 rounded bg-[#05070d]/90 px-1 font-mono text-xs text-white">×{{ $count }}</span>
            @endif
            @if ($badge)
                <span class="absolute top-1 left-1 rounded bg-success/90 px-1 text-[10px] font-medium text-[#05070d]">{{ $badge }}</span>
            @endif
            @if ($label)
                <span class="absolute inset-x-0 top-0 bg-gradient-to-b from-[#05070d]/85 to-transparent px-1.5 pt-1 pb-3 text-left text-[11px] text-ink-muted">{{ $label }}</span>
            @endif
        </button>
        <flux:tooltip.content class="max-w-64 px-3 py-2">
            <p class="text-sm font-semibold text-white">{{ $item->name }}</p>
            <p @class(['text-[11px] tracking-wide uppercase', $item->rarity->classes()])>{{ $item->rarity->label() }} · {{ $item->kind->label() }}</p>
            @if ($bonuses = $item->bonuses())
                <p class="mt-1 font-mono text-xs text-success">{{ implode(' · ', $bonuses) }}</p>
            @endif
            @if ($item->description)
                <p class="mt-1 text-xs font-normal text-zinc-300">{{ $item->description }}</p>
            @endif
            <p class="mt-1.5 text-[10px] font-normal text-zinc-400">Clic para ver la ficha</p>
        </flux:tooltip.content>
    </flux:tooltip>
</flux:modal.trigger>
