@props(['titles', 'start' => 0])

{{--
    Carrusel 3D (Mundos): la tarjeta del medio al frente y las de los costados giradas (resources/js/worlds-carousel.js).
    Cada tarjeta del slot lleva la clase `carousel-card`, `x-bind:style="cardStyle(i)"`, `x-bind:class="cardClass(i)"`
    y adentro <x-carousel-3d.pick :index="i" /> para que tocarla desde un costado la traiga al medio.
    $titles: los nombres de las tarjetas, en orden (para los puntos).
--}}
@php($count = count($titles))
<section {{ $attributes->class('flex flex-col gap-4') }}
         x-data="worldsCarousel({{ $count }}, {{ $start }})"
         @keydown.left.prevent="prev()" @keydown.right.prevent="next()">
    <div class="flex items-center justify-between gap-3">
        {{ $heading }}
        @if ($count > 1)
            <span class="tech-label" x-text="(active + 1) + ' / ' + count"></span>
        @endif
    </div>
    {{ $intro ?? '' }}

    {{-- Todas las tarjetas en la misma celda de la grilla: el escenario toma el alto de la más alta. --}}
    <div class="relative -mx-4 overflow-hidden px-4 py-6 [perspective:1100px] sm:-mx-8 sm:px-8">
        <div x-ref="stage" class="grid touch-pan-y justify-items-center select-none [transform-style:preserve-3d]"
             @pointerdown="pointerDown($event)" @pointermove="pointerMove($event)"
             @pointerup="pointerUp()" @pointercancel="pointerUp()" @click.capture="swallowClick($event)">
            {{ $slot }}
        </div>

        @if ($count > 1)
            {{-- Flechas a los costados, solo en la compu (en el celular se arrastra). --}}
            <button type="button" @click="prev()" :disabled="active === 0" aria-label="Anterior"
                    class="absolute top-1/2 left-2 z-40 hidden size-11 -translate-y-1/2 items-center justify-center rounded-full border border-primary-bright/40 bg-surface-low/90 text-primary-bright shadow-[0_0_14px_-2px_rgb(6_182_212/0.4)] backdrop-blur transition hover:bg-primary-bright/15 disabled:opacity-30 lg:flex">
                <flux:icon name="chevron-left" class="size-6" />
            </button>
            <button type="button" @click="next()" :disabled="active === count - 1" aria-label="Siguiente"
                    class="absolute top-1/2 right-2 z-40 hidden size-11 -translate-y-1/2 items-center justify-center rounded-full border border-primary-bright/40 bg-surface-low/90 text-primary-bright shadow-[0_0_14px_-2px_rgb(6_182_212/0.4)] backdrop-blur transition hover:bg-primary-bright/15 disabled:opacity-30 lg:flex">
                <flux:icon name="chevron-right" class="size-6" />
            </button>
        @endif
    </div>

    @if ($count > 1)
        <div class="flex flex-col items-center gap-2">
            <div class="flex flex-wrap items-center justify-center gap-2.5 rounded-full border border-outline bg-surface-low/80 px-4 py-2 backdrop-blur">
                @foreach (array_values($titles) as $i => $title)
                    <button type="button" @click="go({{ $i }})" aria-label="Ir a {{ $title }}" title="{{ $title }}"
                            class="h-2.5 rounded-full transition-all duration-300"
                            :class="active === {{ $i }} ? 'w-6 bg-primary-bright shadow-[0_0_10px_rgb(6_182_212/0.8)]' : 'w-2.5 bg-outline hover:bg-ink-muted'"></button>
                @endforeach
            </div>
            <p class="flex items-center gap-1.5 font-mono text-[11px] text-ink-muted">
                <flux:icon name="arrows-right-left" variant="micro" class="text-primary-bright" />
                <span class="lg:hidden">Deslizá o tocá un costado para cambiar de mundo</span>
                <span class="hidden lg:inline">Arrastrá, usá las flechas o tocá un mundo del costado</span>
            </p>
        </div>
    @endif
</section>
