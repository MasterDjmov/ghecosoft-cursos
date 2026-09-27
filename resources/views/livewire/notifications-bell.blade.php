<div wire:poll.60s.visible class="relative" x-data="{ open: false }" x-on:keydown.escape.window="open = false" x-on:click.outside="open = false">
    <div>
        <button type="button" x-on:click="open = ! open" x-bind:aria-expanded="open" class="relative grid size-9 place-items-center rounded-lg text-ink-muted transition hover:bg-surface-high hover:text-ink" aria-label="Avisos{{ $unread ? " ({$unread} sin leer)" : '' }}">
            <flux:icon name="bell" variant="outline" class="size-5" />
            @if ($unread)
                <span class="absolute -top-0.5 -right-0.5 grid min-w-4 place-items-center rounded-full bg-danger px-1 font-mono text-[10px] font-bold text-white">{{ $unread > 9 ? '9+' : $unread }}</span>
            @endif
        </button>

        <div x-show="open" x-cloak x-transition.opacity class="panel absolute end-0 top-11 z-50 flex max-h-[70vh] w-80 max-w-[calc(100vw-2rem)] flex-col gap-1 overflow-y-auto p-2">
            <div class="flex items-center justify-between px-2 py-1">
                <span class="font-display text-sm font-semibold text-white">Avisos</span>
                @if ($unread)
                    <button type="button" wire:click="markAllRead" class="text-xs text-primary-bright hover:underline">Marcar todo como leído</button>
                @endif
            </div>
            @forelse ($items as $item)
                <button type="button" wire:click="open('{{ $item->id }}')" x-on:click="open = false" wire:key="notification-{{ $item->id }}"
                    @class(['flex items-start gap-3 rounded-md p-2 text-start transition hover:bg-surface-high', 'bg-primary/5' => ! $item->read_at])>
                    <flux:icon :name="$item->data['icon'] ?? 'bell'" variant="mini" @class(['mt-0.5 shrink-0', 'text-primary-bright' => ! $item->read_at, 'text-ink-muted' => $item->read_at]) />
                    <span class="flex min-w-0 flex-col">
                        <span @class(['truncate text-sm', 'font-medium text-white' => ! $item->read_at, 'text-ink' => $item->read_at])>{{ $item->data['title'] ?? '' }}</span>
                        <span class="line-clamp-2 text-xs text-ink-muted">{{ $item->data['body'] ?? '' }}</span>
                        <span class="text-[11px] text-ink-muted">{{ $item->created_at->diffForHumans() }}</span>
                    </span>
                </button>
            @empty
                <p class="p-4 text-center text-sm text-ink-muted">No tenés avisos.</p>
            @endforelse
        </div>
    </div>
</div>
