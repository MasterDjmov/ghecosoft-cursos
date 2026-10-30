@props(['fill' => false])

{{-- La consola de JavaScript (D115): vive dentro de un x-data="codeRunner(...)". Arriba, la página del programa (si tiene),
     en la caja sandbox="allow-scripts" sin mismo origen ni red (resources/js/runners/js-caja.js); abajo, Salida, Tablero
     (lo que en un navegador de verdad está escondido en las herramientas de desarrollador: el reloj de la caja, las
     cookies, el almacenamiento, los pedidos al Puerto y los avisos) y Entrada (las respuestas de prompt y confirm).
     Todo es simulado y se borra al terminar: no toca nada de la compu de quien ejecuta. --}}
<div {{ $attributes->class(['flex flex-col bg-[#05070d]', 'min-h-0' => $fill]) }} data-test="js-board">
    <div x-show="jsHasPage" x-cloak class="relative border-b border-outline/60">
        <div class="flex items-center gap-2 border-b border-outline/60 px-3 py-1.5">
            <flux:icon name="window" variant="micro" class="text-ink-muted" />
            <span class="tech-label">La página</span>
            <span class="text-[11px] text-ink-muted" x-show="jsLive" x-cloak>· en vivo: tocala</span>
            <button type="button" x-show="jsLive" x-cloak x-on:click="jsStop()" class="ms-auto flex items-center gap-1 rounded px-2 py-0.5 text-xs text-ink-muted hover:bg-surface-high hover:text-ink">
                <flux:icon name="stop" variant="micro" /> Detener
            </button>
        </div>
        <div x-ref="jsPage" wire:ignore class="h-72 bg-white">
            <p class="p-4 text-sm text-slate-500" x-show="! jsLive">Tocá <strong>Ejecutar</strong> para ver la página.</p>
        </div>
    </div>

    {{-- Los otros archivos de la consigna (módulos que el código importa): se leen, no se cambian. --}}
    <template x-for="(source, file) in jsFiles" :key="file">
        <details class="border-b border-outline/60 px-3 py-2 text-xs" data-test="js-file">
            <summary class="cursor-pointer font-mono text-ink"><span x-text="file"></span> <span class="text-ink-muted">· otro archivo, se importa con './<span x-text="file"></span>'</span></summary>
            <pre class="mt-2 max-h-64 overflow-auto rounded bg-surface-lowest p-2 font-mono text-ink" x-text="source"></pre>
        </details>
    </template>

    <div class="flex shrink-0 items-center gap-1 border-b border-outline/60 px-2" role="tablist">
        @foreach (['output' => 'Salida', 'board' => 'Tablero', 'input' => 'Entrada'] as $value => $label)
            <button type="button" role="tab" x-on:click="tab = '{{ $value }}'" x-bind:aria-selected="tab === '{{ $value }}'"
                class="-mb-px flex items-center gap-1.5 border-b-2 px-2.5 py-2 text-xs font-medium whitespace-nowrap transition"
                x-bind:class="tab === '{{ $value }}' ? 'border-primary-bright text-ink' : 'border-transparent text-ink-muted hover:text-ink'">
                {{ $label }}
                @if ($value === 'board')
                    <span class="size-1.5 rounded-full bg-secondary-bright" x-show="jsBoardBusy()" x-cloak title="Tiene cookies, almacenamiento o pedidos"></span>
                @elseif ($value === 'input')
                    <span class="size-1.5 rounded-full bg-primary-bright" x-show="stdin.trim() !== ''" x-cloak title="Tiene respuestas preparadas"></span>
                @endif
            </button>
        @endforeach
        <span class="ms-auto truncate ps-2 font-mono text-[11px]" x-bind:class="error ? 'text-danger' : 'text-ink-muted'" x-text="status"></span>
    </div>

    <div x-show="tab === 'output'" role="tabpanel" @class(['flex flex-col gap-1 p-3', 'min-h-0 flex-1 overflow-auto' => $fill])>
        <pre @class(['min-h-12 font-mono text-sm whitespace-pre-wrap', 'max-h-72 overflow-auto' => ! $fill]) x-show="output !== null && ! lines" x-cloak
            x-bind:class="error ? 'text-danger' : 'text-success'" x-text="output"></pre>
        <div @class(['min-h-12 font-mono text-sm', 'max-h-72 overflow-auto' => ! $fill]) x-show="lines" x-cloak data-test="output-lines">
            <template x-for="(line, i) in lines ?? []" :key="i">
                <div class="flex gap-2" x-bind:class="line.ok ? 'text-success' : 'text-warning'">
                    <span class="w-4 shrink-0 select-none text-center" x-text="line.ok ? '✓' : '✗'"></span>
                    <span class="min-w-0 whitespace-pre-wrap" x-bind:class="line.missing && 'italic opacity-80'"
                        x-text="line.missing ? 'Falta: «' + line.text + '»' : (line.text === '' ? ' ' : line.text)"></span>
                </div>
            </template>
            <p class="mt-1 text-xs text-ink-muted">✓ igual a lo esperado · ✗ revisá ese renglón</p>
        </div>
        <template x-for="(note, i) in jsNotes" :key="'n' + i">
            <p class="text-xs text-warning" x-text="'ⓘ ' + note"></p>
        </template>
        <p class="min-h-12 text-xs text-ink-muted" x-show="output === null">Tocá <strong class="text-ink">Ejecutar</strong> (o Ctrl+Enter en el editor) para ver la salida acá.</p>
        <p class="text-xs text-success" x-show="matches === true" x-cloak>✓ Coincide con lo esperado.</p>
    </div>

    <div x-show="tab === 'board'" x-cloak role="tabpanel" @class(['grid gap-3 p-3 text-xs sm:grid-cols-2', 'min-h-0 flex-1 overflow-auto' => $fill, 'max-h-96 overflow-auto' => ! $fill]) data-test="js-board-panel">
        <p class="text-ink-muted sm:col-span-2" x-show="! jsBoard">Ejecutá el programa para ver qué guarda y qué pide. Todo es de mentira: vive solo mientras corre y no toca tu compu.</p>
        <template x-if="jsBoard">
            <div class="contents">
                <section class="rounded-md border border-outline/60 p-2.5">
                    <h4 class="tech-label mb-1.5 flex items-center gap-1"><flux:icon name="clock" variant="micro" /> El reloj de la caja</h4>
                    <p class="font-mono text-ink"><span x-text="(jsBoard.clock / 1000).toLocaleString('es-AR', { minimumFractionDigits: 1, maximumFractionDigits: 3 })"></span> s</p>
                    <p class="mt-0.5 text-ink-muted"><span x-text="jsBoard.fired"></span> temporizadores disparados · <span x-text="jsBoard.timers"></span> esperando</p>
                </section>
                <section class="rounded-md border border-outline/60 p-2.5">
                    <h4 class="tech-label mb-1.5 flex items-center gap-1"><flux:icon name="cake" variant="micro" /> Cookies</h4>
                    <p class="text-ink-muted" x-show="! jsBoard.cookies.length">(ninguna)</p>
                    <template x-for="c in jsBoard.cookies" :key="c.name">
                        <p class="font-mono break-all text-ink">
                            <span class="text-secondary-bright" x-text="c.name"></span>=<span x-text="c.value"></span>
                            <span class="text-ink-muted" x-show="c.httpOnly" title="JavaScript no la ve con document.cookie: solo viaja en los pedidos">🔒 HttpOnly</span>
                            <span class="text-ink-muted" x-show="c.expires !== null" x-text="'· vence a los ' + (c.expires / 1000).toLocaleString('es-AR') + ' s'"></span>
                        </p>
                    </template>
                </section>
                @foreach (['local' => 'localStorage', 'session' => 'sessionStorage'] as $key => $label)
                    <section class="rounded-md border border-outline/60 p-2.5">
                        <h4 class="tech-label mb-1.5 flex items-center gap-1"><flux:icon name="archive-box" variant="micro" /> {{ $label }}</h4>
                        <p class="text-ink-muted" x-show="! jsBoard.{{ $key }}.length">(vacío)</p>
                        <template x-for="[k, v] in jsBoard.{{ $key }}" :key="k">
                            <p class="font-mono break-all text-ink"><span class="text-secondary-bright" x-text="k"></span>: <span x-text="v"></span></p>
                        </template>
                    </section>
                @endforeach
                <section class="rounded-md border border-outline/60 p-2.5 sm:col-span-2">
                    <h4 class="tech-label mb-1.5 flex items-center gap-1"><flux:icon name="paper-airplane" variant="micro" /> Pedidos al Puerto (fetch)</h4>
                    <p class="text-ink-muted" x-show="! jsBoard.requests.length">(ninguno) · Probá <code class="font-mono">fetch('/puerto/hola')</code></p>
                    <template x-for="(r, i) in jsBoard.requests" :key="'r' + i">
                        <p class="font-mono text-ink">
                            <span class="text-ink-muted" x-text="(r.sent / 1000).toLocaleString('es-AR') + ' s'"></span>
                            <span class="text-secondary-bright" x-text="r.method"></span> <span x-text="r.url"></span> →
                            <span x-bind:class="typeof r.status === 'number' && r.status < 400 ? 'text-success' : 'text-warning'" x-text="r.status"></span>
                            <span class="text-ink-muted" x-show="r.ms !== null" x-text="'(tardó ' + r.ms + ' ms)'"></span>
                        </p>
                    </template>
                </section>
                <section class="rounded-md border border-outline/60 p-2.5 sm:col-span-2" x-show="jsBoard.notices.length">
                    <h4 class="tech-label mb-1.5 flex items-center gap-1"><flux:icon name="bell" variant="micro" /> Avisos</h4>
                    <template x-for="(n, i) in jsBoard.notices" :key="'a' + i">
                        <p class="text-ink"><span class="text-ink-muted" x-text="(n.at / 1000).toLocaleString('es-AR') + ' s · ' + n.kind + ':'"></span> <span x-text="n.text"></span></p>
                    </template>
                </section>
            </div>
        </template>
    </div>

    <div x-show="tab === 'input'" x-cloak role="tabpanel" @class(['flex flex-col gap-1.5 p-3', 'min-h-0 flex-1 overflow-auto' => $fill])>
        <textarea x-model="stdin" rows="3" spellcheck="false" aria-label="Respuestas para prompt y confirm"
            class="w-full rounded-md border border-outline bg-surface-lowest p-2 font-mono text-sm text-ink focus:ring-2 focus:ring-accent focus:outline-none"></textarea>
        <p class="text-xs text-ink-muted">Una línea por cada <code class="font-mono">prompt()</code> o <code class="font-mono">confirm()</code> (para confirm: <em>sí</em> o <em>no</em>).</p>
    </div>
</div>
