{{-- Las expediciones del mundo (D91). --}}
<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-wrap items-end justify-between gap-3">
        <div class="flex flex-col gap-1">
            <a href="{{ route('student.hero', $course) }}" wire:navigate class="tech-label hover:text-white">← Mi héroe</a>
            <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Expediciones</h1>
            <p class="text-ink-muted">{{ $course->title }} · hoy: <span class="font-mono text-white" data-test="expeditions-today">{{ $today }} de {{ $perDay }}</span></p>
        </div>
        <div class="flex flex-wrap items-center gap-2">
            <a href="{{ route('student.stables') }}" wire:navigate class="panel flex items-center gap-2 px-3 py-2 text-sm text-ink hover:text-white" data-test="go-stables">
                @if ($mount)
                    <img src="{{ \App\Models\Mount::imageUrl($mount->species, $mount->level) }}" alt="" class="size-6 rounded object-cover">
                    {{ $mount->name() }} n{{ $mount->level }} · −{{ $mount->reduction() }}%
                @else
                    <flux:icon name="sparkles" variant="mini" /> Establos
                @endif
            </a>
            <a href="{{ route('student.inventory', ['solapa' => $course->slug]) }}" wire:navigate class="panel flex items-center gap-2 px-3 py-2 text-sm text-ink hover:text-white"><flux:icon name="shopping-bag" variant="mini" /> Mochila</a>
        </div>
    </header>

    @if (! $open)
        <div class="panel flex items-start gap-4 p-4" data-test="expeditions-locked">
            <img src="{{ asset('img/personajes/profe.webp') }}" alt="" class="size-14 shrink-0 rounded-full border border-secondary/40 object-cover">
            <div class="flex flex-col gap-1 text-sm">
                <p class="font-medium text-white">El Profe</p>
                <p class="text-ink">—Todavía es temprano para salir a explorar. Las expediciones se abren cuando completes <strong>«{{ $opensAfter }}»</strong>. Ahí te muestro los establos y el mapa.</p>
            </div>
        </div>
    @elseif (! $hero)
        <a href="{{ route('student.hero', $course) }}" wire:navigate class="flex items-center gap-3 rounded-lg border border-warning/50 bg-warning/10 px-4 py-3 text-sm" data-test="expeditions-need-hero">
            <strong class="text-warning">Tomá el control de {{ $protagonist['name'] }}</strong> para mandarla de expedición.
        </a>
    @endif

    {{-- La pelea que se está mirando --}}
    @if ($fight)
        @include('livewire.student.partials.expedition-fight', ['fight' => $fight])
    @endif

    {{-- El mapa --}}
    <section class="relative overflow-hidden rounded-xl border border-outline" data-test="expedition-map">
        <img src="{{ asset($world['map']) }}" alt="Mapa de {{ term('world.region', $course) }}" class="w-full">
        @foreach ($places as $place)
            <div class="group absolute -translate-x-1/2 -translate-y-1/2" style="left: {{ $place['x'] }}%; top: {{ $place['y'] }}%" wire:key="pin-{{ $place['code'] }}">
                <span @class([
                    'relative grid size-6 place-items-center rounded-full border-2 font-mono text-[10px] font-bold shadow-lg sm:size-7',
                    'border-white bg-primary text-white shadow-cyan-500/40' => $place['open'],
                    'border-zinc-500 bg-zinc-800/90 text-zinc-400' => ! $place['open'],
                ]) data-test="pin-{{ $place['code'] }}">
                    @if ($place['open'])<span class="absolute inset-0 animate-ping rounded-full bg-primary/40"></span>@endif
                    <span class="relative">{{ $place['level'] }}</span>
                </span>
                <span class="pointer-events-none absolute top-8 left-1/2 z-10 hidden w-48 -translate-x-1/2 rounded-lg border border-outline bg-[#05070d]/95 p-2 text-xs group-hover:block">
                    <span class="block font-medium text-white">{{ $place['name'] }} · nivel {{ $place['level'] }}</span>
                    @if ($place['open'])
                        <span class="block text-ink-muted">{{ collect($place['creatures'])->map(fn ($c) => $service->creatureName($c, $course))->implode(', ') }}</span>
                    @else
                        <span class="block text-warning">Se abre al completar «{{ $place['node_title'] }}»</span>
                    @endif
                </span>
            </div>
        @endforeach
    </section>

    @if ($open && $hero)
        {{-- En camino --}}
        @if ($active)
            <section class="panel panel-active flex flex-col gap-3 p-4" data-test="expedition-active" wire:key="active-{{ $active->id }}-{{ $active->ends_at->timestamp }}"
                x-data="{ left: {{ (int) max(0, ceil(now()->diffInSeconds($active->ends_at, false))) }}, total: {{ (int) max(1, round($active->started_at->diffInSeconds($active->ends_at))) }}, t: null }"
                x-init="t = setInterval(() => { if (left > 0) left--; }, 1000)" x-on:livewire:navigating.window="clearInterval(t)">
                <div class="flex flex-wrap items-center gap-3">
                    @if ($heroImage)<img src="{{ $heroImage }}" alt="" class="size-12 rounded-full border border-primary-bright/60 object-cover">@endif
                    <div class="flex min-w-0 flex-1 flex-col">
                        <p class="tech-label text-primary-bright">Expedición {{ config('game.expedition.lengths.'.$active->length.'.label') }} en camino</p>
                        <p class="font-display text-lg font-semibold text-white">{{ $protagonist['name'] }} explora {{ $activePlace }}</p>
                    </div>
                    <span class="font-mono text-2xl text-primary-bright" x-show="left > 0" x-text="String(Math.floor(left / 60)).padStart(2, '0') + ':' + String(left % 60).padStart(2, '0')"></span>
                    @if ($hourglasses > 0)
                        <flux:button size="sm" icon="clock" wire:click="hurry" x-show="left > 0" wire:confirm="¿Usar un Reloj de Arena? La expedición termina ya y el reloj se gasta." data-test="expedition-hurry">Reloj de Arena ({{ $hourglasses }})</flux:button>
                    @endif
                    <flux:button variant="primary" icon="flag" wire:click="claim" x-show="left <= 0" x-cloak data-test="expedition-claim">Ver cómo le fue</flux:button>
                </div>
                <div class="h-2 overflow-hidden rounded-full bg-surface-high">
                    <div class="h-full rounded-full bg-gradient-to-r from-cyan-500 via-sky-400 to-amber-400 transition-all duration-1000" :style="'width:' + (100 - left / total * 100) + '%'"></div>
                </div>
                <p class="text-xs text-ink-muted">Podés seguir con las micro-misiones mientras tanto: la expedición sigue sola.</p>
            </section>
        @else
            {{-- Las 3 del momento --}}
            <section class="flex flex-col gap-3">
                <div class="flex items-center justify-between">
                    <h2 class="font-display text-lg font-semibold text-white">Elegí una expedición</h2>
                    @if ($today >= $perDay)<span class="text-sm text-warning">Ya hiciste las {{ $perDay }} de hoy. Mañana hay más.</span>@endif
                </div>
                <div class="grid gap-3 md:grid-cols-3">
                    @foreach ($offers as $offer)
                        <article class="panel flex flex-col gap-2 p-4" wire:key="offer-{{ $offer['index'] }}-{{ $offer['place']['code'] }}" data-test="offer-{{ $offer['length'] }}">
                            <div class="flex items-center justify-between">
                                <span class="rounded-md border border-primary/40 bg-primary/10 px-2 py-0.5 font-mono text-xs text-primary-bright">{{ $offer['label'] }}</span>
                                <span class="flex items-center gap-1 font-mono text-sm text-ink"><flux:icon name="clock" variant="micro" />
                                    {{ $offer['seconds'] >= 60 ? round($offer['seconds'] / 60, 1).' min' : $offer['seconds'].' s' }}</span>
                            </div>
                            <p class="font-medium text-white">{{ $offer['place']['name'] }} <span class="text-sm text-ink-muted">· nivel {{ $offer['place']['level'] }}</span></p>
                            <div class="flex -space-x-2">
                                @foreach ($offer['place']['creatures'] as $creature)
                                    <img src="{{ \App\Services\Expeditions::creatureImage($creature) }}" alt="{{ $service->creatureName($creature, $course) }}" title="{{ $service->creatureName($creature, $course) }}" class="size-9 rounded-full border-2 border-surface object-cover">
                                @endforeach
                            </div>
                            <p class="text-xs text-ink-muted">{{ $offer['place']['text'] }}</p>
                            <div class="mt-auto flex items-center justify-between gap-2 pt-1">
                                <span class="flex items-center gap-1 text-sm text-warning"><x-gold-icon class="size-4" /> ~{{ $offer['gold'] }}</span>
                                <flux:button size="sm" variant="primary" wire:click="send({{ $offer['index'] }})" :disabled="$today >= $perDay" data-test="send-{{ $offer['length'] }}">Mandar a {{ $protagonist['name'] }}</flux:button>
                            </div>
                        </article>
                    @endforeach
                </div>
            </section>
        @endif
    @endif

    {{-- Las últimas --}}
    @if ($history->isNotEmpty())
        <section class="flex flex-col gap-2">
            <h2 class="font-display text-lg font-semibold text-white">Las últimas</h2>
            @foreach ($history as $past)
                <div class="flex flex-wrap items-center gap-3 rounded-lg border border-outline/70 px-3 py-2 text-sm" wire:key="past-{{ $past->id }}" data-test="history-row">
                    <span @class(['rounded px-1.5 py-0.5 text-xs', 'bg-success/15 text-success' => $past->won, 'bg-danger/15 text-danger' => ! $past->won])>{{ $past->won ? 'Ganó' : 'Volvió sin botín' }}</span>
                    <span class="text-white">{{ $past->rewards['place'] ?? $past->place }}</span>
                    <span class="text-ink-muted">{{ config('game.expedition.lengths.'.$past->length.'.label') }} · {{ $past->resolved_at->diffForHumans() }}</span>
                    @if ($past->won)
                        <span class="flex items-center gap-1 text-warning"><x-gold-icon class="size-4" /> {{ $past->rewards['gold'] ?? 0 }}</span>
                        @foreach ($past->rewards['items'] ?? [] as $loot)
                            <span class="text-xs {{ \App\Enums\ItemRarity::from($loot['rarity'])->classes() }}">{{ $loot['name'] }}{{ $loot['quantity'] > 1 ? ' ×'.$loot['quantity'] : '' }}</span>
                        @endforeach
                    @endif
                    <button type="button" wire:click="watch({{ $past->id }})" class="ms-auto text-xs text-primary-bright hover:underline">Ver la pelea</button>
                </div>
            @endforeach
        </section>
    @endif
</div>
