@props([
    'code' => '',
    'stdin' => '',
    'expected' => '',
    'language' => 'python',
    'runnable' => true,
    'readOnly' => false,
    'showStdin' => null,
    'title' => null,
])

{{-- Editor CodeMirror + "Ejecutar" con Pyodide. El slot "actions" va junto a Ejecutar
     y ve las variables de Alpine (code, stdin), por ejemplo: $wire.submit(code). --}}
<div {{ $attributes->class('flex flex-col gap-3') }}
    x-data="codeRunner(@js([
        'code' => (string) $code, 'stdin' => (string) $stdin, 'expected' => (string) $expected, 'language' => $language,
        'readOnly' => $readOnly, 'runnable' => $runnable && $language === 'python',
        'pyodideUrl' => config('services.pyodide.url'), 'timeout' => config('services.pyodide.timeout_ms'),
    ]))">
    <div class="flex flex-wrap items-center justify-between gap-2">
        @if ($title)
            <span class="tech-label">{{ $title }}</span>
        @else
            <span></span>
        @endif
        <div class="flex flex-wrap items-center gap-2">
            <flux:button size="sm" variant="ghost" icon="clipboard" x-on:click="copy"><span x-text="copied ? '¡Copiado!' : 'Copiar'">Copiar</span></flux:button>
            @unless ($readOnly)
                <flux:button size="sm" variant="ghost" icon="arrow-uturn-left" x-on:click="restore" x-show="code !== original" x-cloak>Restaurar</flux:button>
            @endunless
            @if ($runnable && $language === 'python')
                <flux:button size="sm" icon="play" x-on:click="run" x-bind:disabled="running">
                    <span x-text="running ? 'Ejecutando…' : 'Ejecutar'">Ejecutar</span>
                </flux:button>
            @endif
            {{ $actions ?? '' }}
        </div>
    </div>

    {{-- Mientras carga CodeMirror se ve el código plano. --}}
    <div x-ref="editor" wire:ignore class="min-h-24 overflow-hidden rounded-lg">
        <pre class="rounded-lg border border-outline bg-surface-lowest p-3 font-mono text-sm whitespace-pre-wrap text-ink">{{ $code }}</pre>
    </div>

    @if ($runnable && $language === 'python')
        <details class="text-sm" @if ($showStdin ?? filled($stdin)) open @endif>
            <summary class="cursor-pointer text-ink-muted">Entrada (una línea por cada <code class="font-mono">input()</code>)</summary>
            <textarea x-model="stdin" rows="2" spellcheck="false"
                class="mt-2 w-full rounded-lg border border-outline bg-surface-lowest p-2 font-mono text-sm text-ink focus:ring-2 focus:ring-accent focus:outline-none"></textarea>
        </details>

        <div class="flex flex-col gap-2" x-show="output !== null" x-cloak>
            <div class="flex items-center justify-between text-xs">
                <span class="tech-label">Salida</span>
                <span class="font-mono" x-bind:class="error ? 'text-danger' : 'text-ink-muted'" x-text="status"></span>
            </div>
            <pre class="max-h-72 overflow-auto rounded-lg border border-outline bg-[#05070d] p-3 font-mono text-sm whitespace-pre-wrap"
                x-bind:class="error ? 'text-danger' : 'text-success'" x-text="output"></pre>
            <p class="text-xs text-success" x-show="matches === true">✓ Coincide con la salida esperada.</p>
        </div>
    @endif

    {{ $footer ?? '' }}

    @if (filled($expected))
        <details class="text-sm">
            <summary class="cursor-pointer text-ink-muted">Salida esperada</summary>
            <pre class="mt-2 overflow-auto rounded-lg border border-outline bg-surface-lowest p-3 font-mono text-sm text-ink-muted">{{ $expected }}</pre>
        </details>
    @endif
</div>
