{{-- Lista arrastrable de nodos de una rama. $groupId = id de la rama o 'none'. --}}
<ol class="flex min-h-12 flex-col gap-2" wire:sort="sortNode" wire:sort:group="nodes" wire:sort:group-id="{{ $groupId }}">
    @forelse ($nodes as $node)
        @php
            $wildcard = $node->priceCurrency?->is_wildcard;
            $parent = $node->parent_id ? $nodesById[$node->parent_id] ?? null : null;
            // Aviso de economía: las obligatorias del requisito no alcanzan para pagar este nodo.
            $shortfall = ! $wildcard && $parent && (int) $parent->required_reward < $node->price;
            $icon = match ($node->type) {
                \App\Enums\NodeType::Boss => 'fire',
                \App\Enums\NodeType::Extra => 'sparkles',
                \App\Enums\NodeType::Window => 'eye',
                default => 'cube',
            };
        @endphp
        <li class="flex flex-col gap-3 rounded-lg border border-outline bg-surface-low/70 p-3 sm:flex-row sm:items-center"
            wire:key="node-{{ $node->id }}" wire:sort:item="{{ $node->id }}" data-test="node-{{ $node->id }}">
            <div class="flex min-w-0 flex-1 items-center gap-3">
                <flux:icon name="bars-3" class="size-4 shrink-0 cursor-grab text-ink-muted" wire:sort:handle />
                <flux:icon :name="$icon" @class(['size-5 shrink-0', 'text-danger' => $node->isBoss(), 'text-secondary-bright' => $node->type === \App\Enums\NodeType::Extra, 'text-primary-bright' => $node->type === \App\Enums\NodeType::Topic, 'text-[#2dd4bf]' => $node->type === \App\Enums\NodeType::Window]) />
                <div class="flex min-w-0 flex-col gap-0.5">
                    <div class="flex flex-wrap items-center gap-2">
                        <a href="{{ route('admin.nodes.edit', [$course, $node]) }}" wire:navigate class="truncate font-medium text-white hover:text-primary-bright">{{ $node->title }}</a>
                        @unless ($node->is_published)
                            <flux:badge size="sm">Sin publicar</flux:badge>
                        @endunless
                        @if ($node->required_count === 0)
                            <flux:badge size="sm" color="amber" icon="exclamation-triangle" data-test="no-required">Sin obligatorias</flux:badge>
                        @endif
                        @if ($node->badge)
                            <flux:badge size="sm" color="amber" icon="trophy">{{ $node->badge->name }}</flux:badge>
                        @endif
                    </div>
                    <p class="font-mono text-[11px] text-ink-muted">
                        requiere: {{ $node->parent?->title ?? '—' }} ·
                        {{ $node->price }} {{ $wildcard ? term('coin.wildcard', null, $node->price) : term('coin.course', $course, $node->price) }} ·
                        {{ $node->required_count }} oblig. + {{ $node->optional_count }} opt.
                    </p>
                    @if ($shortfall)
                        <p class="flex items-center gap-1 text-[11px] text-warning">
                            <flux:icon name="exclamation-triangle" variant="micro" />
                            Las obligatorias de «{{ $parent->title }}» pagan {{ (int) $parent->required_reward }} y este nodo cuesta {{ $node->price }}.
                        </p>
                    @endif
                </div>
            </div>
            <div class="flex shrink-0 flex-wrap gap-1 sm:justify-end">
                <flux:button size="xs" icon="plus" :href="route('admin.nodes.edit', [$course, $node]).'?hoja=nueva'" wire:navigate>Nueva hoja</flux:button>
                <flux:button size="xs" variant="ghost" icon="pencil-square" :href="route('admin.nodes.edit', [$course, $node])" wire:navigate aria-label="Editar" />
                <flux:dropdown position="bottom" align="end">
                    <flux:button size="xs" variant="ghost" icon="ellipsis-horizontal" aria-label="Más opciones" />
                    <flux:menu>
                        <flux:menu.item :icon="$node->is_published ? 'eye-slash' : 'eye'" wire:click="togglePublished({{ $node->id }})">{{ $node->is_published ? 'Despublicar' : 'Publicar' }}</flux:menu.item>
                        <flux:menu.item icon="document-duplicate" wire:click="duplicateNode({{ $node->id }})">Duplicar</flux:menu.item>
                        <flux:menu.item icon="trash" variant="danger" wire:click="confirmDeleteNode({{ $node->id }})">Borrar</flux:menu.item>
                    </flux:menu>
                </flux:dropdown>
            </div>
        </li>
    @empty
        <li class="rounded-lg border border-dashed border-outline p-4 text-center text-sm text-ink-muted" wire:sort:ignore>
            Sin nodos. Tocá «Nodo» o arrastrá uno acá.
        </li>
    @endforelse
</ol>
