@props(['fill' => false])

{{-- Consola del editor (Salida / Entrada); la salida esperada va en <x-expected-io> (D73). Vive dentro de un x-data="codeRunner(...)":
     usa sus variables (tab, output, stdin, status, error, matches). Con fill ocupa el alto que le den. --}}
<div {{ $attributes->class(['flex flex-col bg-[#05070d]', 'min-h-0' => $fill]) }}>
    {{-- La barra flotante: si la consola quedó más abajo de lo que se ve (mucho código), Ejecutar y la salida quedan a mano.
         Desplegada, en la compu va de costado a la derecha (el código queda a la vista); en el celular, abajo. --}}
    <div x-show="consoleDock" x-cloak x-transition.opacity
        class="fixed inset-x-2 bottom-2 z-40 mx-auto flex max-w-3xl flex-col gap-1.5 rounded-xl border border-primary/40 bg-[#05070d]/95 p-2 shadow-2xl shadow-black/60 backdrop-blur sm:inset-x-4"
        x-bind:class="consoleDockOpen && 'lg:inset-x-auto lg:end-3 lg:top-20 lg:bottom-3 lg:w-[27rem] lg:max-w-none'" data-test="console-dock">
        <div class="flex flex-wrap items-center gap-1.5">
            <button type="button" x-on:click="run" x-bind:disabled="running" class="inline-flex items-center gap-1.5 rounded-md bg-primary/15 px-2.5 py-1.5 text-xs font-medium text-primary-bright transition hover:bg-primary/25 disabled:opacity-40">
                <flux:icon name="play" variant="micro" /> <span x-text="running ? 'Ejecutando…' : 'Ejecutar'">Ejecutar</span>
            </button>
            <span class="min-w-0 flex-1 truncate font-mono text-[11px]" x-bind:class="error ? 'text-danger' : (matches === true ? 'text-success' : 'text-ink-muted')"
                x-text="matches === true ? '✓ Coincide con la salida esperada' : status"></span>
            <button type="button" x-on:click="consoleDockOpen = ! consoleDockOpen" data-test="console-dock-toggle"
                class="inline-flex items-center gap-1.5 rounded-md border border-outline px-2.5 py-1.5 text-xs font-medium text-ink-muted transition hover:text-ink"
                x-bind:title="consoleDockOpen ? 'Achicar' : 'Ver la salida y la entrada sin bajar'">
                <flux:icon name="chevron-up" variant="micro" class="transition" x-bind:class="consoleDockOpen && 'rotate-180'" />
                <span x-text="consoleDockOpen ? 'Menos' : 'Más'">Más</span>
            </button>
        </div>
        {{-- Achicada: el primer renglón de la salida, para ver de un vistazo qué pasó. --}}
        <p class="truncate font-mono text-[11px]" x-show="! consoleDockOpen && output" x-cloak
            x-bind:class="error ? 'text-danger' : 'text-success'" x-text="(output ?? '').split('\n').find((l) => l.trim() !== '') ?? ''"></p>
        <div x-show="consoleDockOpen" x-cloak class="flex min-h-0 flex-1 flex-col gap-2 overflow-y-auto" data-test="console-dock-panel">
            <p class="text-[11px] text-ink-muted">Salida</p>
            <pre class="max-h-[30vh] min-h-8 overflow-auto font-mono text-sm whitespace-pre-wrap lg:max-h-none" x-show="output !== null && ! lines"
                x-bind:class="error ? 'text-danger' : 'text-success'" x-text="output"></pre>
            <div class="max-h-[30vh] overflow-auto font-mono text-sm lg:max-h-none" x-show="lines">
                <template x-for="(line, i) in lines ?? []" :key="i">
                    <div class="flex gap-2" x-bind:class="line.ok ? 'text-success' : 'text-warning'">
                        <span class="w-4 shrink-0 select-none text-center" x-text="line.ok ? '✓' : '✗'"></span>
                        <span class="min-w-0 whitespace-pre-wrap" x-bind:class="line.missing && 'italic opacity-80'"
                            x-text="line.missing ? 'Falta: «' + line.text + '»' : (line.text === '' ? ' ' : line.text)"></span>
                    </div>
                </template>
            </div>
            <p class="text-xs text-ink-muted" x-show="output === null">Tocá <strong class="text-ink">Ejecutar</strong> para ver la salida.</p>
            <p class="text-[11px] text-ink-muted">Entrada (stdin)</p>
            <textarea x-model="stdin" rows="2" spellcheck="false" aria-label="Entrada estándar"
                class="w-full rounded-md border border-outline bg-surface-lowest p-2 font-mono text-sm text-ink focus:ring-2 focus:ring-accent focus:outline-none"></textarea>
        </div>
    </div>

    <div class="flex shrink-0 items-center gap-1 border-b border-outline/60 px-2" role="tablist"
        x-init="let below = false, near = false;
            const update = () => { consoleDock = below && near };
            new IntersectionObserver(([e]) => { below = ! e.isIntersecting && e.boundingClientRect.top > 0; update() }).observe($el);
            new IntersectionObserver(([e]) => { near = e.isIntersecting; update() }).observe($el.closest('[x-data]') ?? $el)">
        <button type="button" role="tab" x-on:click="tab = 'output'" x-bind:aria-selected="tab === 'output'"
            class="-mb-px border-b-2 px-2.5 py-2 text-xs font-medium transition"
            x-bind:class="tab === 'output' ? 'border-primary-bright text-ink' : 'border-transparent text-ink-muted hover:text-ink'">Salida</button>
        <button type="button" role="tab" x-on:click="tab = 'input'" x-bind:aria-selected="tab === 'input'"
            class="-mb-px flex items-center gap-1.5 border-b-2 px-2.5 py-2 text-xs font-medium whitespace-nowrap transition"
            x-bind:class="tab === 'input' ? 'border-primary-bright text-ink' : 'border-transparent text-ink-muted hover:text-ink'">
            Entrada (stdin)
            <span class="size-1.5 rounded-full bg-primary-bright" x-show="stdin.trim() !== ''" x-cloak title="Tiene datos de entrada"></span>
        </button>
        <span class="ms-auto truncate ps-2 font-mono text-[11px]" x-bind:class="error ? 'text-danger' : 'text-ink-muted'" x-text="status"></span>
    </div>

    <div x-show="tab === 'output'" role="tabpanel" @class(['flex flex-col gap-1 p-3', 'min-h-0 flex-1 overflow-auto' => $fill])>
        <pre @class(['min-h-12 font-mono text-sm whitespace-pre-wrap', 'max-h-72 overflow-auto' => ! $fill]) x-show="output !== null && ! lines" x-cloak
            x-bind:class="error ? 'text-danger' : 'text-success'" x-text="output"></pre>
        {{-- No coincide: cada renglón con ✓ (igual al esperado) o ✗ (ahí hay que corregir), y los que faltan. --}}
        <div @class(['min-h-12 font-mono text-sm', 'max-h-72 overflow-auto' => ! $fill]) x-show="lines" x-cloak data-test="output-lines">
            <template x-for="(line, i) in lines ?? []" :key="i">
                <div class="flex gap-2" x-bind:class="line.ok ? 'text-success' : 'text-warning'">
                    <span class="w-4 shrink-0 select-none text-center" x-text="line.ok ? '✓' : '✗'" x-bind:title="line.ok ? 'Igual a la esperada' : (line.missing ? 'Falta este renglón' : 'Distinta de la esperada')"></span>
                    <span class="min-w-0 whitespace-pre-wrap" x-bind:class="line.missing && 'italic opacity-80'"
                        x-text="line.missing ? 'Falta: «' + line.text + '»' : (line.text === '' ? ' ' : line.text)"></span>
                </div>
            </template>
            <p class="mt-1 text-xs text-ink-muted">✓ igual a lo esperado · ✗ revisá ese renglón</p>
        </div>
        <p class="min-h-12 text-xs text-ink-muted" x-show="output === null">Tocá <strong class="text-ink">Ejecutar</strong> (o Ctrl+Enter en el editor) para ver la salida acá.</p>
        <p class="text-xs text-success" x-show="matches === true" x-cloak>✓ Coincide con la salida esperada.</p>
    </div>
    <div x-show="tab === 'input'" x-cloak role="tabpanel" @class(['flex flex-col gap-1.5 p-3', 'min-h-0 flex-1 overflow-auto' => $fill])>
        <textarea x-model="stdin" rows="3" spellcheck="false" aria-label="Entrada estándar"
            class="w-full rounded-md border border-outline bg-surface-lowest p-2 font-mono text-sm text-ink focus:ring-2 focus:ring-accent focus:outline-none"></textarea>
        <p class="text-xs text-ink-muted">Una línea por cada <code class="font-mono">input()</code>.</p>
    </div>
</div>
