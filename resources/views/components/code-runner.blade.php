@props([
    'code' => '',
    'stdin' => '',
    'expected' => '',
    'language' => 'python',
    'runnable' => true,
    'readOnly' => false,
    'showStdin' => null,
    'name' => 'main',
])

@php
    $extension = [
        'python' => 'py', 'c' => 'c', 'cpp' => 'cpp', 'java' => 'java', 'javascript' => 'js',
        'typescript' => 'ts', 'php' => 'php', 'sql' => 'sql', 'arduino' => 'ino',
    ][$language] ?? 'txt';
    $languageLabel = \App\Enums\Language::tryFrom($language)?->label() ?? $language;
    $canRun = $runnable && $language === 'python';
    $barButton = 'inline-flex items-center gap-1.5 rounded-md px-2 py-1 text-xs font-medium transition disabled:opacity-50';
@endphp

{{-- Editor CodeMirror como "ventana": barra con archivo y acciones, y consola con pestañas
     (Salida / Entrada / Esperada) que ejecuta con Pyodide. Los slots "actions" (en la barra)
     y "footer" (debajo) ven las variables de Alpine (code, stdin), por ejemplo: $wire.submit(code). --}}
<div {{ $attributes->class('flex flex-col gap-4') }}
    x-data="codeRunner(@js([
        'code' => (string) $code, 'stdin' => (string) $stdin, 'expected' => (string) $expected, 'language' => $language,
        'readOnly' => $readOnly, 'runnable' => $canRun, 'tab' => ($showStdin ?? false) ? 'input' : 'output',
        'pyodideUrl' => config('services.pyodide.url'), 'timeout' => config('services.pyodide.timeout_ms'),
    ]))">
    <div class="code-window overflow-hidden rounded-lg border border-outline bg-surface-lowest transition focus-within:border-primary-bright/60">
        {{-- Barra de la ventana --}}
        <div class="flex items-center gap-2 border-b border-outline bg-surface-low px-3 py-1.5">
            <span class="hidden items-center gap-1.5 pe-1 sm:flex" aria-hidden="true">
                <span class="size-2.5 rounded-full bg-[#f87171]/70"></span>
                <span class="size-2.5 rounded-full bg-[#f59e0b]/70"></span>
                <span class="size-2.5 rounded-full bg-[#10b981]/70"></span>
            </span>
            <flux:icon name="document-text" variant="micro" class="shrink-0 text-ink-muted" />
            <span class="min-w-0 truncate font-mono text-xs text-ink">{{ $name }}.{{ $extension }}</span>
            <span class="tech-label hidden shrink-0 sm:inline">{{ $languageLabel }}</span>
            @if ($readOnly)
                <flux:icon name="lock-closed" variant="micro" class="shrink-0 text-ink-muted" aria-label="Solo lectura" />
            @endif

            <div class="ms-auto flex shrink-0 items-center gap-1">
                @unless ($readOnly)
                    <button type="button" x-on:click="restore" x-show="code !== original" x-cloak title="Restaurar"
                        class="{{ $barButton }} text-ink-muted hover:bg-surface-high hover:text-ink">
                        <flux:icon name="arrow-uturn-left" variant="micro" /> <span class="hidden sm:inline">Restaurar</span>
                    </button>
                @endunless
                <button type="button" x-on:click="copy" title="Copiar" class="{{ $barButton }} text-ink-muted hover:bg-surface-high hover:text-ink">
                    <flux:icon name="clipboard" variant="micro" /> <span class="hidden sm:inline" x-text="copied ? '¡Copiado!' : 'Copiar'">Copiar</span>
                </button>
                @if ($canRun)
                    <button type="button" x-on:click="run" x-bind:disabled="running" title="Ejecutar (Ctrl+Enter)"
                        class="{{ $barButton }} bg-primary/15 text-primary-bright hover:bg-primary/25">
                        <flux:icon name="play" variant="micro" /> <span class="hidden sm:inline" x-text="running ? 'Ejecutando…' : 'Ejecutar'">Ejecutar</span>
                    </button>
                @endif
                {{ $actions ?? '' }}
            </div>
        </div>

        {{-- Mientras carga CodeMirror se ve el código plano. --}}
        <div x-ref="editor" wire:ignore>
            <pre class="code-window-fallback p-3 font-mono text-sm whitespace-pre-wrap text-ink">{{ $code }}</pre>
        </div>

        {{-- Consola --}}
        @if ($canRun)
            <div class="border-t border-outline bg-[#05070d]">
                <div class="flex items-center gap-1 border-b border-outline/60 px-2" role="tablist">
                    <button type="button" role="tab" x-on:click="tab = 'output'" x-bind:aria-selected="tab === 'output'"
                        class="-mb-px border-b-2 px-2.5 py-2 text-xs font-medium transition"
                        x-bind:class="tab === 'output' ? 'border-primary-bright text-ink' : 'border-transparent text-ink-muted hover:text-ink'">Salida</button>
                    <button type="button" role="tab" x-on:click="tab = 'input'" x-bind:aria-selected="tab === 'input'"
                        class="-mb-px flex items-center gap-1.5 border-b-2 px-2.5 py-2 text-xs font-medium whitespace-nowrap transition"
                        x-bind:class="tab === 'input' ? 'border-primary-bright text-ink' : 'border-transparent text-ink-muted hover:text-ink'">
                        Entrada (stdin)
                        <span class="size-1.5 rounded-full bg-primary-bright" x-show="stdin.trim() !== ''" x-cloak title="Tiene datos de entrada"></span>
                    </button>
                    @if (filled($expected))
                        <button type="button" role="tab" x-on:click="tab = 'expected'" x-bind:aria-selected="tab === 'expected'"
                            class="-mb-px border-b-2 px-2.5 py-2 text-xs font-medium transition"
                            x-bind:class="tab === 'expected' ? 'border-primary-bright text-ink' : 'border-transparent text-ink-muted hover:text-ink'">Esperada</button>
                    @endif
                    <span class="ms-auto truncate ps-2 font-mono text-[11px]" x-bind:class="error ? 'text-danger' : 'text-ink-muted'" x-text="status"></span>
                </div>

                <div x-show="tab === 'output'" role="tabpanel" class="flex flex-col gap-1 p-3">
                    <pre class="max-h-72 min-h-12 overflow-auto font-mono text-sm whitespace-pre-wrap" x-show="output !== null" x-cloak
                        x-bind:class="error ? 'text-danger' : 'text-success'" x-text="output"></pre>
                    <p class="min-h-12 text-xs text-ink-muted" x-show="output === null">Tocá <strong class="text-ink">Ejecutar</strong> (o Ctrl+Enter en el editor) para ver la salida acá.</p>
                    <p class="text-xs text-success" x-show="matches === true" x-cloak>✓ Coincide con la salida esperada.</p>
                </div>
                <div x-show="tab === 'input'" x-cloak role="tabpanel" class="flex flex-col gap-1.5 p-3">
                    <textarea x-model="stdin" rows="3" spellcheck="false" aria-label="Entrada estándar"
                        class="w-full rounded-md border border-outline bg-surface-lowest p-2 font-mono text-sm text-ink focus:ring-2 focus:ring-accent focus:outline-none"></textarea>
                    <p class="text-xs text-ink-muted">Una línea por cada <code class="font-mono">input()</code>.</p>
                </div>
                @if (filled($expected))
                    <div x-show="tab === 'expected'" x-cloak role="tabpanel" class="p-3">
                        <pre class="max-h-72 overflow-auto font-mono text-sm whitespace-pre-wrap text-ink-muted">{{ $expected }}</pre>
                    </div>
                @endif
            </div>
        @endif
    </div>

    @if (filled($expected) && ! $canRun)
        <details class="text-sm">
            <summary class="cursor-pointer text-ink-muted">Salida esperada</summary>
            <pre class="mt-2 overflow-auto rounded-lg border border-outline bg-surface-lowest p-3 font-mono text-sm text-ink-muted">{{ $expected }}</pre>
        </details>
    @endif

    {{ $footer ?? '' }}
</div>
