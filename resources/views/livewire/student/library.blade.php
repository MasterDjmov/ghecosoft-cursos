{{-- Crónicas en Inglés (D106): la biblioteca de episodios. El alumno elige qué leer o practicar; cada
     episodio muestra su avance. Se abren sin monedas: el primero con el abono y el resto al terminar el anterior. --}}
@php
    use App\Services\TreeAccess;

    $done = $episodes->where('state', TreeAccess::STATE_COMPLETED)->count();
@endphp

<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8" data-test="library">
    <header class="relative overflow-hidden rounded-2xl border border-outline">
        @if ($scene)
            <img src="{{ $scene }}" alt="" class="absolute inset-0 size-full object-cover opacity-40">
        @endif
        <div class="relative flex flex-col gap-4 bg-gradient-to-r from-surface via-surface/90 to-surface/40 p-6 sm:flex-row sm:items-center">
            <x-course-logo :course="$course" size="size-16" />
            <div class="flex min-w-0 flex-1 flex-col gap-1">
                <p class="tech-label">Biblioteca · {{ $course->title }}</p>
                <h1 class="font-display text-2xl font-semibold text-white">Elegí qué leer o practicar</h1>
                <p class="text-sm text-ink-muted"><span data-test="library-progress">{{ $done }} de {{ $episodes->count() }}</span> episodios terminados. Cada episodio se lee en inglés, se escucha y se practica: se comprueba solo.</p>
            </div>
            @if ($paidUntil)
                <x-subscription-countdown :until="$paidUntil" :total="$course->subscription_days" class="self-start sm:self-center" />
            @endif
        </div>
    </header>

    @if ($trial)
        <flux:callout icon="sparkles" color="cyan" data-test="trial-banner">
            <flux:callout.heading>Estás probando {{ $course->title }} gratis</flux:callout.heading>
            <flux:callout.text>
                El primer episodio se lee y se practica sin pagar. Para seguir con los demás,
                <flux:link :href="route('student.course', $course)" wire:navigate>pedí tu abono</flux:link> (el mes empieza a correr cuando se aprueba).
            </flux:callout.text>
        </flux:callout>
    @elseif (! $subscription && ! $staff)
        <flux:callout icon="clock" color="amber" data-test="expired-banner">
            <flux:callout.heading>Tu abono no está vigente</flux:callout.heading>
            <flux:callout.text>
                Podés releer y repasar los episodios que abriste. Para abrir episodios nuevos,
                <flux:link :href="route('student.course', $course)" wire:navigate>renová el abono</flux:link>.
            </flux:callout.text>
        </flux:callout>
    @endif

    <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        @foreach ($episodes as $episode)
            @php
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
                    @endif
                    <span class="absolute left-3 top-3 rounded-md bg-surface/85 px-2 py-0.5 font-mono text-xs text-ink">Episodio {{ $loop->iteration }}</span>
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
                                {{ $node->parent ? 'Se abre al terminar «'.$node->parent->title.'».' : 'Se abre con el abono del curso.' }}
                            </p>
                        @endif
                    </div>
                </div>
            </article>
        @endforeach
    </div>
</div>
