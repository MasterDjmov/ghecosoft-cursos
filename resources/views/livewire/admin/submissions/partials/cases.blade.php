{{-- Corrección asistida (D73): el ejemplo y las pruebas de la práctica, corridos al abrir la entrega en el
     navegador de quien corrige. Es una ayuda: Aprobar o Rehacer sigue siendo decisión del docente. --}}
<section class="panel flex flex-col gap-3 p-5" wire:ignore data-test="submission-cases"
    x-data="submissionCases(@js([
        'language' => $course->language->value, 'code' => (string) $submission->code, 'cases' => $cases,
        'pyodideUrl' => config('services.pyodide.url'), 'javaRunnerUrl' => config('services.java_runner.url'), 'timeout' => config('services.pyodide.timeout_ms'),
    ]))">
    <div class="flex flex-wrap items-center gap-3">
        <h2 class="font-display font-semibold text-white">Pruebas</h2>
        <template x-if="running">
            <span class="flex items-center gap-2 text-sm text-ink-muted"><flux:icon.loading variant="micro" /> <span x-text="status || 'Probando…'"></span></span>
        </template>
        <template x-if="!running && !unavailable && results.length">
            <span class="rounded-full px-2.5 py-0.5 font-mono text-sm"
                x-bind:class="passed === total ? 'bg-success/15 text-success' : 'bg-danger/15 text-[#fca5a5]'"
                x-text="`${passed} de ${total} ${total === 1 ? 'prueba pasa' : 'pruebas pasan'}`"></span>
        </template>
        <flux:button size="xs" variant="ghost" icon="arrow-path" class="ms-auto" x-on:click="run" x-bind:disabled="running">Volver a probar</flux:button>
    </div>
    <p class="text-xs text-ink-muted">{{ count($cases) }} {{ count($cases) === 1 ? 'caso' : 'casos' }}: el de ejemplo y los que agregó el curso para corregir. Se ignoran los espacios al final de cada línea y las líneas vacías de las puntas.</p>

    <template x-if="unavailable">
        <pre class="max-h-60 overflow-auto rounded-md border border-danger/40 bg-danger/5 p-3 font-mono text-xs whitespace-pre-wrap text-[#fca5a5]" x-text="unavailable"></pre>
    </template>

    <ul class="flex flex-col gap-2" x-show="!unavailable">
        <template x-for="(result, i) in results" x-bind:key="i">
            <li class="rounded-md border border-outline">
                <details x-bind:open="!result.passed">
                    <summary class="flex cursor-pointer items-center gap-2 px-3 py-2 text-sm">
                        <span x-bind:class="result.passed ? 'text-success' : 'text-[#fca5a5]'" x-text="result.passed ? '✓' : '✗'"></span>
                        <span class="text-ink" x-text="result.label"></span>
                        <span class="ms-auto text-xs text-ink-muted" x-show="!result.passed"
                            x-text="result.compileError ? 'no compila' : (result.timedOut ? 'tiempo agotado' : (result.error && !/terminó con código|^SystemExit/.test(result.error) ? 'termina con error' : 'la salida no coincide'))"></span>
                    </summary>
                    <div class="flex flex-col gap-3 border-t border-outline p-3">
                        <div x-show="result.input !== ''">
                            <p class="tech-label mb-1">Entrada</p>
                            <pre class="max-h-40 overflow-auto font-mono text-xs whitespace-pre-wrap text-ink" x-text="result.input"></pre>
                        </div>
                        <template x-if="!result.passed">
                            <div class="grid gap-3 sm:grid-cols-2">
                                <div class="min-w-0">
                                    <p class="tech-label mb-1">Esperada</p>
                                    <pre class="max-h-72 overflow-auto rounded bg-[#05070d] p-2 font-mono text-xs"><template x-for="(line, j) in result.lines" x-bind:key="j"><span class="block min-h-4" x-bind:class="line.same ? 'text-ink-muted' : 'bg-success/10 text-success'" x-text="line.expected ?? ''"></span></template></pre>
                                </div>
                                <div class="min-w-0">
                                    <p class="tech-label mb-1">Obtenida</p>
                                    <pre class="max-h-72 overflow-auto rounded bg-[#05070d] p-2 font-mono text-xs"><template x-for="(line, j) in result.lines" x-bind:key="j"><span class="block min-h-4" x-bind:class="line.same ? 'text-ink-muted' : 'bg-danger/10 text-[#fca5a5]'" x-text="line.got ?? ''"></span></template></pre>
                                    <pre class="mt-1 font-mono text-xs whitespace-pre-wrap text-[#fca5a5]" x-show="result.error" x-text="result.error"></pre>
                                </div>
                            </div>
                        </template>
                    </div>
                </details>
            </li>
        </template>
    </ul>
</section>
