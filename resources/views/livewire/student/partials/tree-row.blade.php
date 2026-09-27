{{-- Un nodo en la vista de lista del árbol del alumno. --}}
@php
    $open = in_array($node['state'], ['unlocked', 'completed'], true);
    [$badgeColor, $icon] = match ($node['state']) {
        'completed' => ['green', 'check-circle'],
        'unlocked' => ['cyan', 'lock-open'],
        'available' => ['amber', 'sparkles'],
        default => ['zinc', 'lock-closed'],
    };
    $typeIcon = match ($node['type']) {
        'root' => 'star',
        'boss' => 'fire',
        'extra' => 'sparkles',
        'window' => 'eye',
        default => 'cube',
    };
@endphp

<li class="list-none" wire:key="row-{{ $node['id'] }}" data-test="tree-node-{{ $node['id'] }}">
    <div @class([
        'panel flex flex-col gap-3 p-3 sm:flex-row sm:items-center',
        'panel-active' => $node['state'] === 'available',
        'opacity-70' => $node['state'] === 'locked',
    ])>
        <div class="flex min-w-0 flex-1 items-center gap-3">
            <div @class([
                'grid size-10 shrink-0 place-items-center rounded-full',
                'bg-primary/20 text-primary-bright' => $node['type'] === 'root' || $node['type'] === 'topic',
                'bg-danger/20 text-danger' => $node['type'] === 'boss',
                'bg-secondary/20 text-secondary-bright' => $node['type'] === 'extra',
                'bg-[#2dd4bf]/20 text-[#2dd4bf]' => $node['type'] === 'window',
                'grayscale' => $node['state'] === 'locked',
            ])>
                <flux:icon :name="$typeIcon" variant="mini" />
            </div>
            <div class="flex min-w-0 flex-col gap-1">
                <div class="flex flex-wrap items-center gap-2">
                    @if ($open)
                        <a href="{{ $node['url'] }}" wire:navigate class="font-medium text-white hover:text-primary-bright">{{ $node['title'] }}</a>
                    @else
                        <span class="font-medium text-ink">{{ $node['title'] }}</span>
                    @endif
                    <flux:badge size="sm" :color="$badgeColor" :icon="$icon">{{ term('state.'.$node['state'], $course) }}</flux:badge>
                </div>
                @if ($open && $leaves->isNotEmpty())
                    <div class="flex flex-wrap gap-1.5" aria-label="Prácticas">
                        @foreach ($leaves as $leaf)
                            <span title="{{ $leaf['title'] }}" @class([
                                'size-2.5 rounded-full',
                                'bg-success' => $leaf['status'] === 'approved',
                                'bg-warning' => $leaf['status'] === 'submitted',
                                'bg-danger' => $leaf['status'] === 'redo',
                                'bg-surface-highest ring-1 ring-outline' => $leaf['status'] === 'pending',
                            ])></span>
                        @endforeach
                    </div>
                @elseif (! $open)
                    <p class="text-xs text-ink-muted">{{ $node['price_label'] }}@if ($node['state'] === 'locked' && $node['blockers']) · {{ $node['blockers'][0] }}@endif</p>
                @endif
            </div>
        </div>
        <div class="shrink-0">
            @if ($open)
                <flux:button size="sm" icon-trailing="arrow-right" :href="$node['url']" wire:navigate>Entrar</flux:button>
            @elseif ($node['state'] === 'available')
                <flux:button size="sm" variant="primary" icon="lock-open" wire:click="selectNode({{ $node['id'] }})">Abrir · {{ $node['price_label'] }}</flux:button>
            @else
                <flux:button size="sm" variant="ghost" icon="information-circle" wire:click="selectNode({{ $node['id'] }})">Por qué</flux:button>
            @endif
        </div>
    </div>
</li>
