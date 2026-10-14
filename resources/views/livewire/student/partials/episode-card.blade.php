{{-- Una tarjeta de episodio de la biblioteca (D106). Recibe $episode, $number, $trial, $subscription, $staff y $course. --}}
@php
    use App\Services\TreeAccess;

    $node = $episode['node'];
    $state = $episode['state'];
    // El primer episodio de prueba (sin abono) se lee y se practica como si estuviera abierto.
    $tryingIt = $trial && $node->isRoot();
    $open = $tryingIt || in_array($state, [TreeAccess::STATE_UNLOCKED, TreeAccess::STATE_COMPLETED], true);
    $progress = $episode['progress'];
    $url = route('student.node', [$course, $node]);
@endphp
<article class="panel flex flex-col overflow-hidden {{ $open ? '' : 'opacity-80' }}" wire:key="episode-{{ $node->id }}" data-test="episode">
    <figure class="relative aspect-video overflow-hidden border-b border-outline bg-surface-lowest">
        @if ($episode['cover'])
            <img src="{{ $episode['cover'] }}" alt="" class="size-full object-cover {{ $state === TreeAccess::STATE_LOCKED ? 'grayscale' : '' }}" loading="lazy">
            @if ($state !== TreeAccess::STATE_LOCKED)
                {{-- Tocar la portada la muestra en grande (x-image-lightbox en la biblioteca) --}}
                <button type="button" class="group absolute inset-0 cursor-zoom-in" x-data x-on:click="$dispatch('zoom-image', { src: @js($episode['cover']) })" aria-label="Ver la portada en grande" data-test="episode-zoom">
                    <span class="absolute right-3 bottom-3 rounded-md bg-surface/80 p-1 text-white opacity-70 transition group-hover:opacity-100"><flux:icon name="magnifying-glass-plus" variant="micro" /></span>
                </button>
            @endif
        @endif
        <span class="absolute left-3 top-3 rounded-md bg-surface/85 px-2 py-0.5 font-mono text-xs text-ink">{{ $episode['optional'] ? 'Rama' : 'Episodio '.$number }}</span>
        @if ($state === TreeAccess::STATE_COMPLETED)
            <span class="absolute right-3 top-3 flex items-center gap-1 rounded-md bg-success/90 px-2 py-0.5 text-xs font-semibold text-surface" data-test="episode-done">
                <flux:icon name="check" variant="micro" /> Terminado
            </span>
        @elseif ($state === TreeAccess::STATE_LOCKED)
            <span class="absolute inset-0 flex items-center justify-center bg-surface/50"><flux:icon name="lock-closed" class="size-10 text-ink-muted" /></span>
        @endif
    </figure>
    <div class="flex flex-1 flex-col gap-3 p-4">
        <div class="flex flex-col gap-0.5">
            <h2 class="font-display text-lg font-semibold text-white">{{ $node->title }}</h2>
            @if ($episode['subtitle'])
                <p class="text-sm text-ink-muted">{{ $episode['subtitle'] }}</p>
            @endif
        </div>
        <div class="flex items-center gap-2">
            <div class="h-1.5 flex-1 overflow-hidden rounded-full bg-surface-highest" role="progressbar" aria-valuemin="0" aria-valuemax="{{ $progress['total'] }}" aria-valuenow="{{ $open ? $progress['done'] : 0 }}">
                <div class="h-full rounded-full bg-warning" style="width: {{ $open && $progress['total'] ? round($progress['done'] / $progress['total'] * 100) : 0 }}%"></div>
            </div>
            <span class="font-mono text-xs text-ink-muted" data-test="episode-progress">{{ $open ? $progress['done'] : 0 }} de {{ $progress['total'] }}</span>
        </div>
        <div class="mt-auto flex flex-wrap gap-2">
            @if ($tryingIt)
                <flux:button size="sm" icon="book-open" :href="$url.'?leer=1'" wire:navigate data-test="episode-read">Leer</flux:button>
                <flux:button size="sm" icon="bolt" :href="$url" wire:navigate data-test="episode-practice">Practicar gratis</flux:button>
                <flux:button size="sm" variant="primary" icon="ticket" :href="route('student.course', $course)" wire:navigate data-test="episode-subscribe">Pedir abono</flux:button>
            @elseif ($open)
                <flux:button size="sm" icon="book-open" :href="$url.'?leer=1'" wire:navigate data-test="episode-read">Leer</flux:button>
                <flux:button size="sm" variant="primary" icon="bolt" :href="$url" wire:navigate data-test="episode-practice">
                    {{ $state === TreeAccess::STATE_COMPLETED ? 'Repasar' : ($progress['done'] > 0 ? 'Seguir' : 'Practicar') }}
                </flux:button>
            @elseif ($state === TreeAccess::STATE_AVAILABLE && ! $subscription && ! $staff)
                <flux:button size="sm" variant="primary" icon="ticket" :href="route('student.course', $course)" wire:navigate data-test="episode-subscribe">Renovar el abono</flux:button>
            @elseif ($state === TreeAccess::STATE_AVAILABLE)
                <flux:button size="sm" variant="primary" icon="lock-open" wire:click="unlock({{ $node->id }})" data-test="episode-open">Empezar</flux:button>
            @else
                <p class="flex items-center gap-1.5 text-xs text-ink-muted">
                    <flux:icon name="lock-closed" variant="micro" />
                    {{ $episode['lockedReason'] ?? ($node->parent ? 'Se abre al terminar «'.$node->parent->title.'».' : 'Se abre con el abono del curso.') }}
                </p>
            @endif
        </div>
    </div>
</article>
