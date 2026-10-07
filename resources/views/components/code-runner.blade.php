@props([
    'code' => '',
    'stdin' => '',
    'expected' => '',
    'language' => 'python',
    'runnable' => true,
    'readOnly' => false,
    'showStdin' => null,
    'name' => 'main',
    'references' => [],
])

@php
    $languageEnum = \App\Enums\Language::tryFrom($language);
    $extension = $languageEnum?->extension() ?? 'txt';
    $languageLabel = $languageEnum?->label() ?? $language;
    // Python (Pyodide) y HTML y CSS (vista previa aislada, D76) corren para todos en el navegador; Java, con el
    // ejecutor de la compu de cada uno (D69 para el docente, D85 para el alumno); C, C++ (D66) y PHP (D68) solo
    // para el docente al corregir, en su navegador.
    $canRun = $runnable && ($languageEnum?->studentCanRun() || (in_array($language, ['c', 'cpp', 'php'], true) && auth()->user()?->isStaff()));
    // Al alumno, si el ejecutor de Java no responde, se le explica cómo instalarlo (al docente, cómo abrirlo).
    $javaHelpUrl = $language === 'java' && ! auth()->user()?->isStaff() ? route('student.java-runner') : null;
    $isHtml = $language === 'html';
    $barButton = 'inline-flex items-center gap-1.5 rounded-md px-2 py-1 text-xs font-medium transition disabled:opacity-50';
@endphp

{{-- Editor CodeMirror como "ventana": barra con archivo y acciones, y consola con pestañas
     (Salida / Entrada) que ejecuta con Pyodide, y debajo «Cómo debería verse» (D73). Los slots "actions" (en la barra)
     y "footer" (debajo) ven las variables de Alpine (code, stdin), por ejemplo: $wire.submit(code). --}}
<div {{ $attributes->class('flex flex-col gap-4') }}
    x-data="codeRunner(@js([
        'code' => (string) $code, 'stdin' => (string) $stdin, 'expected' => (string) $expected, 'language' => $language,
        'readOnly' => $readOnly, 'runnable' => $canRun, 'tab' => ($showStdin ?? false) ? 'input' : 'output',
        'pyodideUrl' => config('services.pyodide.url'), 'javaRunnerUrl' => config('services.java_runner.url'), 'javaHelpUrl' => $javaHelpUrl, 'timeout' => config('services.pyodide.timeout_ms'),
        'references' => (object) array_filter($references),
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
                        <flux:icon name="play" variant="micro" /> <span class="hidden sm:inline" x-text="running ? 'Ejecutando…' : '{{ $isHtml ? 'Ver' : 'Ejecutar' }}'">{{ $isHtml ? 'Ver' : 'Ejecutar' }}</span>
                    </button>
                @endif
                {{ $actions ?? '' }}
            </div>
        </div>

        {{-- Mientras carga CodeMirror se ve el código plano. --}}
        <div x-ref="editor" wire:ignore>
            <pre class="code-window-fallback p-3 font-mono text-sm whitespace-pre-wrap text-ink">{{ $code }}</pre>
        </div>

        {{-- Consola, o la página dibujada si es HTML y CSS --}}
        @if ($canRun && $isHtml)
            <x-html-preview class="border-t border-outline" />
        @elseif ($canRun)
            <x-code-console class="border-t border-outline" />
        @endif
    </div>

    @if ($canRun && $javaHelpUrl)
        <p class="-mt-2 flex items-center gap-1.5 text-xs text-ink-muted" data-test="java-runner-hint">
            <flux:icon name="computer-desktop" variant="micro" /> Java se ejecuta en tu compu, con el
            <a href="{{ $javaHelpUrl }}" wire:navigate class="text-primary-bright hover:underline">Ejecutor de Java</a> abierto.
        </p>
    @endif

    <x-expected-io :input="$stdin" :expected="$expected" :references="$references" />

    {{ $footer ?? '' }}
</div>
