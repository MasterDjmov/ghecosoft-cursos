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
    // Micro-misión de HTML (D102): qué revisa el inspector; su informe se compara con `expected`.
    'checks' => null,
    // Ejemplo de varios archivos en solapas (D116, App\Support\CodeFiles): el ejemplo del nodo y la solución de referencia.
    'files' => false,
    // Herramientas (D120): lo escrito se recuerda en este navegador, con sugerencias al escribir.
    'keep' => null,
    'autocomplete' => false,
])

@php
    $languageEnum = \App\Enums\Language::tryFrom($language);
    $extension = $languageEnum?->extension() ?? 'txt';
    $languageLabel = $languageEnum?->label() ?? $language;
    // Python (Pyodide), HTML y CSS (vista previa aislada, D76), SQL, C y C++ (Clang en WebAssembly, D98, D100) corren para
    // todos en el navegador; Java, con el ejecutor de la compu de cada uno (D69 para el docente, D85 para el
    // alumno); PHP (D68), solo para el docente al corregir, en su navegador.
    $canRun = $runnable && ($languageEnum?->studentCanRun() || (in_array($language, ['c', 'cpp', 'php'], true) && auth()->user()?->isStaff()));
    // Al alumno, si el ejecutor de Java no responde, se le explica cómo instalarlo (al docente, cómo abrirlo).
    $javaHelpUrl = $language === 'java' && ! auth()->user()?->isStaff() ? route('student.java-runner') : null;
    $isHtml = $language === 'html';
    // Un ejemplo de varios archivos (`dado.h` + su bloque, `dado.c`…): una solapa por archivo (D116). Se ejecuta solo si
    // hay un único archivo del lenguaje del curso (los otros son tablas, configuración o la terminal).
    $fenced = $files && ! $isHtml && $language !== 'asm' ? \App\Support\CodeFiles::split((string) $code, $language, $name, $extension) : null;
    if ($fenced) {
        $canRun = $canRun && $fenced['run'] !== null;
        $fenced['files'] = array_map(fn ($f) => [
            ...$f, 'note' => $f['note'] ? \App\Support\Markdown::render($f['note']) : null, 'after' => $f['after'] ? \App\Support\Markdown::render($f['after']) : null,
        ], $fenced['files']);
    }
    // JavaScript (D115): la consigna de una micro-misión de página trae su HTML, los eventos y qué revisar (JSON en `checks`).
    $isJs = $language === 'javascript';
    $jsMission = $isJs && filled($checks) ? (json_decode((string) $checks, true) ?: ['checks' => (string) $checks]) : [];
    $jsHasPage = $isJs && (filled($jsMission['page'] ?? null) || str_starts_with(ltrim((string) $code), '<'));
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
        'references' => (object) array_filter($references), 'checks' => ($isHtml || $language === 'asm') && filled($checks) ? (string) $checks : null,
        'jsMission' => (object) $jsMission, 'jsHasPage' => $jsHasPage, 'fenced' => $fenced,
        'keep' => $keep ? 'practice:'.auth()->id().':'.$keep : null, 'autocomplete' => $autocomplete,
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
            <span class="min-w-0 truncate font-mono text-xs text-ink" @if ($fenced) x-text="files[fileTab]?.split('/').pop() ?? '{{ $name }}.{{ $extension }}'" @endif>{{ $name }}.{{ $extension }}</span>
            @unless ($fenced)
                <span class="tech-label hidden shrink-0 sm:inline">{{ $languageLabel }}</span>
            @endunless
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
                @if ($canRun && $language !== 'asm')
                    <button type="button" x-on:click="run" x-bind:disabled="running" title="Ejecutar (Ctrl+Enter)"
                        class="{{ $barButton }} bg-primary/15 text-primary-bright hover:bg-primary/25">
                        <flux:icon name="play" variant="micro" /> <span class="hidden sm:inline" x-text="running ? 'Ejecutando…' : '{{ $isHtml ? 'Ver' : 'Ejecutar' }}'">{{ $isHtml ? 'Ver' : 'Ejecutar' }}</span>
                    </button>
                @endif
                {{ $actions ?? '' }}
            </div>
        </div>

        @if ($isHtml || $fenced)
            <x-code-file-tabs />
        @endif
        @if ($fenced)
            <div x-show="fileNotes[fileTab]" x-cloak x-html="fileNotes[fileTab]" data-test="code-file-note"
                class="prose-sm border-b border-outline bg-surface-low/40 px-4 py-2 text-sm text-ink-muted [&_code]:text-primary-bright [&_p]:my-1"></div>
        @endif

        {{-- Mientras carga CodeMirror se ve el código plano. --}}
        <div x-ref="editor" wire:ignore>
            <pre class="code-window-fallback p-3 font-mono text-sm whitespace-pre-wrap text-ink">{{ $code }}</pre>
        </div>
        @if ($fenced)
            <div x-show="fileAfter[fileTab]" x-cloak x-html="fileAfter[fileTab]"
                class="border-t border-outline bg-surface-low/40 px-4 py-2 text-sm text-ink-muted [&_code]:text-primary-bright [&_p]:my-1 [&_pre]:my-1"></div>
        @endif

        {{-- Consola, o la página dibujada si es HTML y CSS --}}
        @if ($canRun && $isHtml)
            <x-html-preview class="border-t border-outline" />
            @if (filled($checks))
                <x-html-inspector class="border-t border-outline" :expected="$expected" />
            @endif
        @elseif ($canRun && $isJs)
            <x-js-board class="border-t border-outline" />
        @elseif ($canRun && $language === 'asm')
            <x-asm-board class="border-t border-outline" />
        @elseif ($canRun)
            <x-code-console class="border-t border-outline" />
        @endif
    </div>

    @if ($canRun && $javaHelpUrl)
        <p class="-mt-2 flex items-center gap-1.5 text-xs text-ink-muted" data-test="java-runner-hint">
            <flux:icon name="computer-desktop" variant="micro" /> Java se ejecuta en tu compu, con el
            <a href="{{ $javaHelpUrl }}" @if (request()->boolean('ventana')) target="_blank" @else wire:navigate @endif class="text-primary-bright hover:underline">Ejecutor de Java</a> abierto.
        </p>
    @endif

    <x-expected-io :input="$stdin" :expected="$expected" :references="$references" :inspector="$isHtml && filled($checks)" />

    {{ $footer ?? '' }}
</div>
