{{-- El tablero del Gólem (D110): la consola del ensamblador 8086. Vive dentro de un x-data="codeRunner(...)" y usa su estado
     (asm, asmMode, asmError, output, status…). Los nombres del juego van con el nombre real al lado: así se aprende
     el término técnico sin perder la metáfora. --}}
@php
    $btn = 'inline-flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-medium transition disabled:opacity-40';
    $tab = '-mb-px border-b-2 px-2.5 py-2 text-xs font-medium whitespace-nowrap transition';
@endphp
<div {{ $attributes->class('flex flex-col bg-[#05070d]') }} data-test="asm-board">
    {{-- Controles --}}
    <div class="flex flex-wrap items-center gap-1.5 border-b border-outline/60 px-2 py-1.5">
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
    <div class="flex items-center gap-1 overflow-x-auto border-b border-outline/60 px-2" role="tablist">
        @foreach (['registers' => 'Palancas · registros', 'screen' => 'Pantalla', 'memory' => 'Cajones · memoria', 'stack' => 'Torre · pila'] as $key => $label)
            <button type="button" role="tab" x-on:click="asmPanel = '{{ $key }}'" x-bind:aria-selected="asmPanel === '{{ $key }}'" class="{{ $tab }}"
                x-bind:class="asmPanel === '{{ $key }}' ? 'border-primary-bright text-ink' : 'border-transparent text-ink-muted hover:text-ink'">{{ $label }}</button>
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

        {{-- Palancas (registros) e interruptores (banderas) --}}
        <div x-show="asm && asmPanel === 'registers'" x-cloak class="flex flex-col gap-3" data-test="asm-registers">
            <div class="grid grid-cols-2 gap-1.5 sm:grid-cols-4">
                <template x-for="r in asm?.registers ?? []" :key="r.name">
                    <div class="flex items-center justify-between rounded-md px-2 py-1 font-mono text-xs transition-colors duration-300"
                        x-bind:class="r.changed ? 'bg-yellow-400 text-black' : 'bg-surface-high text-ink'">
                        <span class="opacity-70" x-text="r.name"></span>
                        <span>
                            <span class="font-semibold" x-text="r.value"></span>
                            <span class="ms-1 hidden text-[10px] opacity-60 sm:inline" x-show="r.high !== null" x-text="`(${r.name[0]}H ${r.high} · ${r.name[0]}L ${r.low})`"></span>
                        </span>
                    </div>
                </template>
            </div>
            <div>
                <p class="mb-1 text-[11px] text-ink-muted">Interruptores · banderas</p>
                <div class="flex flex-wrap gap-1.5">
                    <template x-for="f in asm?.flags ?? []" :key="f.name">
                        <span class="rounded-md px-2 py-0.5 font-mono text-xs transition-colors duration-300"
                            x-bind:class="f.changed ? 'bg-yellow-400 text-black' : (f.value ? 'bg-success/20 text-success' : 'bg-surface-high text-ink-muted')"
                            x-text="`${f.name} ${f.value}`"></span>
                    </template>
                </div>
            </div>
            <p class="text-[11px] text-ink-muted" x-show="! asm?.atFin">En amarillo, lo que cambió la última orden. Órdenes ejecutadas: <span class="font-mono" x-text="asm?.steps"></span></p>
            <p class="text-[11px] text-secondary-bright" x-show="asm?.atFin" x-cloak>Así quedó el Gólem al llegar a <code class="font-mono">fin:</code>, antes de apagarse (es lo que se comprueba). Órdenes ejecutadas: <span class="font-mono" x-text="asm?.steps"></span></p>
        </div>

        {{-- La pantalla del Gólem --}}
        <div x-show="asmPanel === 'screen' || (asmPanel === 'registers' && asmMode === 'done' && asm?.screenHtml)" x-cloak class="mt-3" data-test="asm-screen">
            <p class="mb-1 text-[11px] text-ink-muted" x-show="asmPanel === 'registers'">Pantalla</p>
            <pre class="max-h-72 min-h-16 overflow-auto rounded-md bg-black p-2 font-mono text-sm whitespace-pre-wrap text-slate-200" x-html="asm?.screenHtml ?? ''"></pre>
        </div>

        {{-- Cajones (memoria) --}}
        <div x-show="asm && asmPanel === 'memory'" x-cloak data-test="asm-memory">
            <form class="mb-2 flex items-center gap-2 text-xs" x-on:submit.prevent="asmGoto($refs.asmAddr.value)">
                <span class="text-ink-muted">Ir al cajón</span>
                <input x-ref="asmAddr" placeholder="0000" class="w-20 rounded border border-outline bg-surface-lowest px-1.5 py-0.5 font-mono text-ink">
                <button class="rounded bg-surface-high px-2 py-0.5 text-ink">Ir</button>
                <span class="text-ink-muted">(direcciones dentro de los datos, en hexa)</span>
            </form>
            <div class="overflow-x-auto">
                <table class="font-mono text-[11px]">
                    <template x-for="row in asm?.memory ?? []" :key="row.address">
                        <tr>
                            <td class="pe-2 text-ink-muted" x-text="row.address"></td>
                            <template x-for="(c, i) in row.cells" :key="i">
                                <td class="px-0.5">
                                    <span class="relative inline-block rounded px-0.5 transition-colors duration-300" x-bind:title="c.name ? `${c.name} (${row.address.slice(0, 3)}${i.toString(16).toUpperCase()}h)` : ''"
                                        x-bind:class="c.changed ? 'bg-yellow-400 text-black' : (c.name ? 'text-primary-bright underline decoration-dotted' : (c.value === '00' ? 'text-ink-muted/50' : 'text-ink'))" x-text="c.value"></span>
                                </td>
                            </template>
                            <td class="ps-2 whitespace-pre text-ink-muted" x-text="row.cells.map((c) => c.char).join('')"></td>
                        </tr>
                    </template>
                </table>
            </div>
            <p class="mt-1 text-[11px] text-ink-muted">Subrayado: donde empieza una variable (pasá el dedo o el mouse para ver su nombre). Cada cajón guarda un byte.</p>
        </div>

        {{-- Torre de platos (pila) --}}
        <div x-show="asm && asmPanel === 'stack'" x-cloak data-test="asm-stack">
            <p class="mb-1 text-[11px] text-ink-muted">Arriba, el último plato que se apiló (SP apunta ahí). PUSH apila; POP saca el de arriba.</p>
            <template x-for="p in asm?.stack ?? []" :key="p.address">
                <div class="flex w-48 items-center justify-between border-x border-t border-outline px-2 py-1 font-mono text-xs last:border-b"
                    x-bind:class="p.top ? 'bg-primary/15 text-primary-bright' : 'text-ink'">
                    <span class="opacity-60" x-text="p.address"></span><span x-text="p.value"></span>
                </div>
            </template>
            <p class="text-xs text-ink-muted" x-show="(asm?.stack ?? []).length === 0">La torre está vacía.</p>
        </div>

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
