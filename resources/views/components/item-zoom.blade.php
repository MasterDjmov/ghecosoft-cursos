@props(['item', 'name', 'count' => null])

{{-- La ficha grande de un ítem (D90): la imagen entera, sus datos y, en el slot, lo que se puede hacer con él. --}}
<flux:modal :name="$name" class="w-full max-w-md" data-test="zoom-{{ $item->code }}">
    <div class="flex flex-col gap-4">
        <div @class(['relative mx-auto grid aspect-square w-full max-w-[28rem] place-items-center overflow-hidden rounded-xl border-2 bg-surface-lowest', $item->rarity->classes()])>
            @if ($url = $item->imageUrl())
                <img src="{{ $url }}" alt="{{ $item->name }}" class="size-full object-cover" loading="lazy">
            @else
                <flux:icon :name="$item->kind->icon()" class="size-20" />
            @endif
            @if ($count !== null)
                <span class="absolute right-2 bottom-2 rounded bg-[#05070d]/90 px-1.5 font-mono text-sm text-white">×{{ $count }}</span>
            @endif
        </div>
        <div class="flex flex-col gap-1">
            <flux:heading size="lg">{{ $item->name }}</flux:heading>
            <p @class(['text-xs tracking-wide uppercase', $item->rarity->classes()])>{{ $item->rarity->label() }} · {{ $item->kind->label() }}{{ $item->course ? '' : ' · común' }}</p>
            @if ($bonuses = $item->bonuses())
                <p class="font-mono text-sm text-success">{{ implode(' · ', $bonuses) }}</p>
            @endif
            @if ($item->description)
                <p class="text-sm text-ink-muted">{{ $item->description }}</p>
            @endif
        </div>
        @if ($slot->isNotEmpty())
            <div class="flex flex-wrap items-center gap-2 border-t border-outline/60 pt-3 text-xs">{{ $slot }}</div>
        @endif
    </div>
</flux:modal>
