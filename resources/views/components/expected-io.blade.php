@props(['input' => '', 'expected' => ''])

{{-- «Cómo debería verse» (D73): la entrada de ejemplo y la salida esperada, iguales en todos los cursos.
     Cerrado de entrada: es un recurso que el alumno abre si lo necesita. --}}
@if (filled($input) || filled($expected))
    <details {{ $attributes->class('group text-sm') }} data-test="expected-io">
        <summary class="cursor-pointer text-ink-muted hover:text-ink">Cómo debería verse</summary>
        <div class="mt-2 flex flex-col gap-3 rounded-lg border border-outline bg-surface-lowest p-3">
            @if (filled($input))
                <div>
                    <p class="tech-label mb-1">Entrada de ejemplo</p>
                    <pre class="max-h-40 overflow-auto font-mono text-sm whitespace-pre-wrap text-ink">{{ $input }}</pre>
                    <p class="mt-1 text-xs text-ink-muted">Lo que se tipea al ejecutar, una línea por cada lectura.</p>
                </div>
            @endif
            @if (filled($expected))
                <div>
                    <p class="tech-label mb-1">Salida esperada</p>
                    <pre class="max-h-40 overflow-auto font-mono text-sm whitespace-pre-wrap text-ink-muted">{{ $expected }}</pre>
                </div>
            @endif
        </div>
    </details>
@endif
