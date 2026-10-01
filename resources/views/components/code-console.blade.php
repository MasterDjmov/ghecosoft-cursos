@props(['fill' => false])

{{-- Consola del editor (Salida / Entrada); la salida esperada va en <x-expected-io> (D73). Vive dentro de un x-data="codeRunner(...)":
     usa sus variables (tab, output, stdin, status, error, matches). Con fill ocupa el alto que le den. --}}
<div {{ $attributes->class(['flex flex-col bg-[#05070d]', 'min-h-0' => $fill]) }}>
    <div class="flex shrink-0 items-center gap-1 border-b border-outline/60 px-2" role="tablist">
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
        <pre @class(['min-h-12 font-mono text-sm whitespace-pre-wrap', 'max-h-72 overflow-auto' => ! $fill]) x-show="output !== null" x-cloak
            x-bind:class="error ? 'text-danger' : 'text-success'" x-text="output"></pre>
        <p class="min-h-12 text-xs text-ink-muted" x-show="output === null">Tocá <strong class="text-ink">Ejecutar</strong> (o Ctrl+Enter en el editor) para ver la salida acá.</p>
        <p class="text-xs text-success" x-show="matches === true" x-cloak>✓ Coincide con la salida esperada.</p>
    </div>
    <div x-show="tab === 'input'" x-cloak role="tabpanel" @class(['flex flex-col gap-1.5 p-3', 'min-h-0 flex-1 overflow-auto' => $fill])>
        <textarea x-model="stdin" rows="3" spellcheck="false" aria-label="Entrada estándar"
            class="w-full rounded-md border border-outline bg-surface-lowest p-2 font-mono text-sm text-ink focus:ring-2 focus:ring-accent focus:outline-none"></textarea>
        <p class="text-xs text-ink-muted">Una línea por cada <code class="font-mono">input()</code>.</p>
    </div>
</div>
