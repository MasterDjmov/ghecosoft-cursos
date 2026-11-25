{{-- D126: la «ventana» del juego (SDL3 de la plataforma). Vive dentro de un x-data="codeRunner(...)" con game: usa
     gamePlaying, gameTitle, gamePads, output, status y error. El lienzo lo pone runners/sdl.js en x-ref="gameScreen". --}}
<div {{ $attributes->class('flex flex-col bg-[#05070d]') }} data-test="game-board">
    <div class="flex flex-wrap items-center gap-2 border-b border-outline/60 px-3 py-1.5 text-xs">
        <flux:icon name="puzzle-piece" variant="micro" class="text-primary-bright" />
        <span class="min-w-0 flex-1 truncate font-mono text-ink" x-text="gameTitle || 'El juego'">El juego</span>
        <span class="flex items-center gap-1 text-ink-muted" x-show="gamePads > 0" x-cloak title="Joysticks conectados">
            🎮 <span x-text="gamePads"></span>
        </span>
        {{-- La red de mentira (SDL3_net): otra copia del mismo juego, conectada con esta (anfitrión e invitado). --}}
        <button type="button" x-on:click="gameSecondRun" x-show="gamePlaying && ! gameSecond" x-cloak data-test="game-second"
            title="Abre el mismo juego en otra ventana, conectada con esta por la red de mentira (como dos compus)"
            class="inline-flex items-center gap-1 rounded-md px-2 py-1 text-ink-muted transition hover:bg-surface-high hover:text-ink">
            <flux:icon name="square-2-stack" variant="micro" /> Otra ventana
        </button>
        <button type="button" x-on:click="gameFullscreen" x-show="gamePlaying" x-cloak data-test="game-fullscreen"
            class="inline-flex items-center gap-1 rounded-md px-2 py-1 text-ink-muted transition hover:bg-surface-high hover:text-ink">
            <flux:icon name="arrows-pointing-out" variant="micro" /> Pantalla completa
        </button>
        <button type="button" x-on:click="gameStop" x-show="gamePlaying" x-cloak data-test="game-stop"
            class="inline-flex items-center gap-1 rounded-md bg-danger/15 px-2 py-1 font-medium text-danger transition hover:bg-danger/25">
            <flux:icon name="stop" variant="micro" /> Cerrar el juego
        </button>
    </div>

    {{-- La pantalla: el lienzo se estira al ancho y conserva la forma de la ventana del juego. --}}
    <div class="grid min-h-48 items-center bg-black" x-bind:class="gameSecond && 'gap-1 lg:grid-cols-2'" data-test="game-screen">
        <p class="p-6 text-center text-sm text-ink-muted" x-show="! gameStarted">Tocá <strong class="text-ink">Jugar</strong> para compilar y abrir la ventana del juego.</p>
        <div x-ref="gameScreen" wire:ignore x-show="gameStarted" x-cloak
            class="w-full [&_canvas]:mx-auto [&_canvas]:block [&_canvas]:outline-none [&_canvas]:[image-rendering:pixelated] [&_canvas:focus]:ring-2 [&_canvas:focus]:ring-primary-bright/60"></div>
        <div x-show="gameSecond" x-cloak class="flex flex-col" data-test="game-second-screen">
            <p class="flex items-center justify-between gap-2 bg-surface-low/60 px-2 py-1 font-mono text-[11px] text-ink-muted">
                <span>Ventana 2 · <span x-text="gameSecondStatus"></span></span>
                <button type="button" x-on:click="gameSecondStop" class="text-danger hover:underline">Cerrar</button>
            </p>
            <div x-ref="gameScreen2" wire:ignore
                class="w-full [&_canvas]:mx-auto [&_canvas]:block [&_canvas]:outline-none [&_canvas]:[image-rendering:pixelated] [&_canvas:focus]:ring-2 [&_canvas:focus]:ring-primary-bright/60"></div>
        </div>
    </div>

    <p class="border-t border-outline/60 px-3 py-1.5 font-mono text-[11px]" data-test="game-status"
        x-bind:class="error ? 'text-danger' : (running ? 'text-primary-bright motion-safe:animate-pulse' : 'text-ink-muted')" x-text="status"></p>
    <pre class="max-h-48 overflow-auto border-t border-outline/60 px-3 py-2 font-mono text-xs whitespace-pre-wrap" x-show="output" x-cloak
        data-test="game-output" x-bind:class="error ? 'text-danger' : 'text-success'" x-text="output"></pre>
</div>
