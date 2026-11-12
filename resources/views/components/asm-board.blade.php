{{-- El tablero del Gólem (D110): la consola del ensamblador 8086. Vive dentro de un x-data="codeRunner(...)" y usa su estado
     (asm, asmMode, asmError, output, status…). Los nombres del juego van con el nombre real al lado: así se aprende
     el término técnico sin perder la metáfora. --}}
@php
    $btn = 'inline-flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-medium transition disabled:opacity-40';
    $tab = '-mb-px border-b-2 px-2.5 py-2 text-xs font-medium whitespace-nowrap transition';
@endphp
<div {{ $attributes->class('@container flex flex-col bg-[#05070d]') }} data-test="asm-board">
    {{-- Controles (si quedan más abajo de la pantalla, aparece la barra flotante de abajo) --}}
    <div class="flex flex-wrap items-center gap-1.5 border-b border-outline/60 px-2 py-1.5"
        x-init="let below = false, near = false;
            const update = () => { asmDock = below && near };
            new IntersectionObserver(([e]) => { below = ! e.isIntersecting && e.boundingClientRect.top > 0; update() }).observe($el);
            new IntersectionObserver(([e]) => { near = e.isIntersecting; update() }).observe($el.closest('[x-data]') ?? $el)">
        <button type="button" x-on:click="asmRun" x-bind:disabled="running" class="{{ $btn }} bg-primary/15 text-primary-bright hover:bg-primary/25" data-test="asm-run">
            <flux:icon name="play" variant="micro" /> <span x-text="asmMode === 'stepping' ? 'Seguir hasta el final' : 'Ejecutar'">Ejecutar</span>
        </button>
        <button type="button" x-on:click="asmStep" x-bind:disabled="running || asmMode === 'waiting'" class="{{ $btn }} bg-warning/15 text-warning hover:bg-warning/25" data-test="asm-step"
            title="Ejecuta una sola orden y muestra qué cambió">
            <flux:icon name="forward" variant="micro" /> <span x-text="asmMode === 'stepping' ? 'Una orden más' : 'Paso a paso'">Paso a paso</span>
        </button>
        <button type="button" x-on:click="asmStop" x-show="asmMode !== 'idle'" x-cloak class="{{ $btn }} text-ink-muted hover:bg-surface-high hover:text-ink" data-test="asm-stop">
            <flux:icon name="stop" variant="micro" /> <span x-text="running ? 'Pausar' : 'Reiniciar'">Reiniciar</span>
        </button>
        <span class="ms-auto truncate ps-2 font-mono text-[11px]" x-bind:class="error ? 'text-danger' : 'text-ink-muted'" x-text="status"></span>
    </div>

    {{-- La barra flotante: los mismos botones, la línea que sigue y las palancas e interruptores que acaban de cambiar. --}}
    {{-- Desplegada, en la compu va de costado a la derecha (el código queda a la vista); en el celular, abajo. --}}
    <div x-show="asmDock" x-cloak x-transition.opacity
        class="fixed inset-x-2 bottom-2 z-40 mx-auto flex max-w-3xl flex-col gap-1.5 rounded-xl border border-primary/40 bg-[#05070d]/95 p-2 shadow-2xl shadow-black/60 backdrop-blur sm:inset-x-4"
        x-bind:class="asmDockOpen && 'lg:inset-x-auto lg:end-3 lg:top-20 lg:bottom-3 lg:w-[27rem] lg:max-w-none'"
        data-test="asm-dock">
        <div class="flex flex-wrap items-center gap-1.5">
            <button type="button" x-on:click="asmRun" x-bind:disabled="running" class="{{ $btn }} bg-primary/15 text-primary-bright hover:bg-primary/25">
                <flux:icon name="play" variant="micro" /> <span x-text="asmMode === 'stepping' ? 'Seguir hasta el final' : 'Ejecutar'">Ejecutar</span>
            </button>
            <button type="button" x-on:click="asmStep" x-bind:disabled="running || asmMode === 'waiting'" class="{{ $btn }} bg-warning/15 text-warning hover:bg-warning/25" title="Ejecuta una sola orden y muestra qué cambió">
                <flux:icon name="forward" variant="micro" /> <span x-text="asmMode === 'stepping' ? 'Una orden más' : 'Paso a paso'">Paso a paso</span>
            </button>
            <button type="button" x-on:click="asmStop" x-show="asmMode !== 'idle'" x-cloak class="{{ $btn }} text-ink-muted hover:bg-surface-high hover:text-ink">
                <flux:icon name="stop" variant="micro" /> <span x-text="running ? 'Pausar' : 'Reiniciar'">Reiniciar</span>
            </button>
            <span class="font-mono text-[11px] text-warning" x-show="asm?.line" x-cloak x-text="`línea ${asm?.line}`"></span>
            <span class="ms-auto min-w-0 truncate font-mono text-[11px]" x-bind:class="error ? 'text-danger' : 'text-ink-muted'" x-text="status"></span>
            <button type="button" x-on:click="asmDockOpen = ! asmDockOpen" class="{{ $btn }} border border-outline text-ink-muted hover:text-ink" data-test="asm-dock-toggle"
                x-bind:title="asmDockOpen ? 'Achicar' : 'Ver palancas, pantalla, cajones, torre y camino sin bajar'">
                <flux:icon name="chevron-up" variant="micro" class="transition" x-bind:class="asmDockOpen && 'rotate-180'" />
                <span x-text="asmDockOpen ? 'Menos' : 'Más'">Más</span>
            </button>
        </div>
        {{-- Desplegada: las mismas pestañas del tablero, con su propia pestaña elegida. --}}
        <div x-show="asmDockOpen" x-cloak class="flex min-h-0 flex-1 flex-col" data-test="asm-dock-panels">
            <div class="flex items-center gap-1 overflow-x-auto border-b border-outline/60 [scrollbar-width:none]" role="tablist">
                @foreach (['registers' => 'Palancas', 'screen' => 'Pantalla', 'memory' => 'Cajones', 'stack' => 'Torre', 'flow' => 'Camino'] as $key => $label)
                    <button type="button" role="tab" x-on:click="asmDockPanel = '{{ $key }}'" x-bind:aria-selected="asmDockPanel === '{{ $key }}'" class="{{ $tab }}"
                        x-bind:class="asmDockPanel === '{{ $key }}' ? 'border-primary-bright text-ink' : 'border-transparent text-ink-muted hover:text-ink'">
                        <span class="relative">{{ $label }}
                            <span class="absolute -end-2 -top-1 flex size-2" x-show="asm?.pulse?.['{{ $key }}'] && asmDockPanel !== '{{ $key }}'" x-cloak>
                                <span class="absolute inline-flex size-full animate-ping rounded-full bg-yellow-400 opacity-75"></span>
                                <span class="relative inline-flex size-2 rounded-full bg-yellow-400"></span>
                            </span>
                        </span>
                    </button>
                @endforeach
            </div>
            <div class="max-h-[45vh] overflow-y-auto pt-2 lg:max-h-none lg:flex-1">
                <x-asm-board-panels dock />
            </div>
        </div>
        <div class="flex flex-wrap gap-x-3 gap-y-0.5 font-mono text-[11px]" x-show="asm && ! asmDockOpen" x-cloak>
            <template x-for="r in (asm?.registers ?? []).filter((r) => ['AX', 'BX', 'CX', 'DX', 'SI', 'DI', 'SP', 'IP'].includes(r.name))" :key="r.name">
                <span x-bind:class="r.changed ? 'text-primary-bright' : 'text-ink-muted'"><span x-text="r.name"></span>=<span x-text="r.value"></span></span>
            </template>
            <template x-for="f in (asm?.flags ?? []).filter((f) => ['ZF', 'SF', 'CF', 'OF'].includes(f.name))" :key="f.name">
                <span x-bind:class="f.changed ? 'text-warning' : 'text-ink-muted'"><span x-text="f.name"></span>=<span x-text="f.value"></span></span>
            </template>
        </div>
        <p class="truncate text-[11px] text-ink" x-show="asm?.explain?.text && ! asmDockOpen" x-cloak x-text="asm?.explain?.text"></p>
    </div>

    {{-- El error del ensamblador, con su criatura y el mensaje real (como lo muestra emu8086) --}}
    <div x-show="asmError" x-cloak class="flex items-start gap-3 border-b border-danger/30 bg-danger/10 px-3 py-2.5 text-sm" data-test="asm-error">
        <flux:icon name="bug-ant" class="mt-0.5 size-5 shrink-0 text-danger" />
        <div class="min-w-0">
            <p class="font-medium text-danger">
                <span x-text="{ slime: 'Un slime', goblin: 'Un goblin', skeleton: 'Un esqueleto', orc: 'Un orco', ogre: 'Un ogro', troll: 'Un troll' }[asmError?.creature] ?? 'Un slime'"></span>
                en la línea <span x-text="asmError?.line"></span>
            </p>
            <p class="text-ink" x-text="asmError?.message"></p>
            <p class="mt-1 font-mono text-[11px] text-ink-muted" x-text="asmError?.raw"></p>
        </div>
    </div>

    {{-- Pestañas (en la compu se ven palancas e interruptores siempre arriba) --}}
    <div class="flex items-center gap-1 overflow-x-auto border-b border-outline/60 px-2 [scrollbar-width:none]" role="tablist">
        @foreach (['registers' => 'Palancas · registros', 'screen' => 'Pantalla', 'memory' => 'Cajones · memoria', 'stack' => 'Torre · pila', 'flow' => 'Camino · flujo'] as $key => $label)
            <button type="button" role="tab" x-on:click="asmPanel = '{{ $key }}'" x-bind:aria-selected="asmPanel === '{{ $key }}'" class="{{ $tab }}"
                x-bind:class="asmPanel === '{{ $key }}' ? 'border-primary-bright text-ink' : 'border-transparent text-ink-muted hover:text-ink'">
                <span class="relative">{{ $label }}
                    {{-- D110: palpita la pestaña donde hubo novedades (lo que escribió en pantalla, los cajones que tocó, la pila). --}}
                    <span class="absolute -end-2 -top-1 flex size-2" x-show="asm?.pulse?.['{{ $key }}'] && asmPanel !== '{{ $key }}'" x-cloak data-test="asm-pulse-{{ $key }}">
                        <span class="absolute inline-flex size-full animate-ping rounded-full bg-yellow-400 opacity-75"></span>
                        <span class="relative inline-flex size-2 rounded-full bg-yellow-400"></span>
                    </span>
                </span>
            </button>
        @endforeach
        <button type="button" role="tab" x-on:click="asmPanel = 'input'" x-bind:aria-selected="asmPanel === 'input'" class="{{ $tab }} flex items-center gap-1.5"
            x-bind:class="asmPanel === 'input' ? 'border-primary-bright text-ink' : 'border-transparent text-ink-muted hover:text-ink'">
            Entrada <span class="size-1.5 rounded-full bg-primary-bright" x-show="stdin.trim() !== ''" x-cloak></span>
        </button>
    </div>

    <div class="p-3">
        <p class="text-xs text-ink-muted" x-show="asmPanel === 'screen' && asm && ! asm.screenHtml" x-cloak>El ojo del Gólem todavía no mostró nada.</p>
        <p class="text-xs text-ink-muted" x-show="! asm && ! asmError && output === null">
            Tocá <strong class="text-ink">Ejecutar</strong> para correr todo el programa, o <strong class="text-warning">Paso a paso</strong> para ver
            cómo cada orden mueve las palancas del Gólem.
        </p>

        <x-asm-board-panels />

        {{-- Entrada preparada (lo que se «tipea») --}}
        <div x-show="asmPanel === 'input'" x-cloak>
            <textarea x-model="stdin" rows="3" spellcheck="false" aria-label="Entrada"
                class="w-full rounded-md border border-outline bg-surface-lowest p-2 font-mono text-sm text-ink focus:ring-2 focus:ring-accent focus:outline-none"></textarea>
            <p class="text-xs text-ink-muted">Lo que el programa va a leer del teclado: una tecla o una línea por renglón. Si se acaba, el Gólem te lo pide.</p>
        </div>

        {{-- El programa pide una tecla o una línea --}}
        <form x-show="asmMode === 'waiting'" x-cloak class="mt-3 flex items-center gap-2 rounded-md border border-warning/40 bg-warning/10 p-2" x-on:submit.prevent="asmSend" data-test="asm-input">
            <flux:icon name="key" variant="micro" class="text-warning" />
            <span class="text-xs text-warning" x-text="asmWaiting === 'line' ? 'Escribí y apretá Enter:' : 'Apretá una tecla:'"></span>
            <input x-ref="asmKey" x-model="asmKey" class="min-w-0 flex-1 rounded border border-outline bg-surface-lowest px-2 py-1 font-mono text-sm text-ink"
                x-on:keydown="if (asmWaiting === 'key' && $event.key.length === 1) { asmKey = $event.key; $event.preventDefault(); $nextTick(() => asmSend()) } else if (asmWaiting === 'key' && $event.key === 'Enter') { asmKey = ''; $event.preventDefault(); asmSend() }">
        </form>

        {{-- Cómo terminó --}}
        <p class="mt-2 text-xs text-danger" x-show="asmEnd" x-cloak x-text="asmEnd"></p>
        <p class="mt-2 text-xs text-success" x-show="matches === true" x-cloak>✓ Coincide con lo esperado.</p>
    </div>
</div>
