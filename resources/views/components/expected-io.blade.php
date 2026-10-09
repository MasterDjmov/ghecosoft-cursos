@props(['input' => '', 'expected' => '', 'references' => [], 'inspector' => false])

{{-- «Cómo debería verse» (D73): la entrada de ejemplo y la salida esperada, iguales en todos los cursos; en
     HTML y CSS, las capturas de la página resuelta en celular y en compu (D77).
     Cerrado de entrada: es un recurso que el alumno abre si lo necesita. --}}
@php($references = array_filter($references ?? []))
@if (filled($input) || filled($expected) || $references)
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
                    <p class="tech-label mb-1">{{ $inspector ? 'Lo que tiene que encontrar el inspector' : 'Salida esperada' }}</p>
                    <pre class="max-h-40 overflow-auto font-mono text-sm whitespace-pre-wrap text-ink-muted">{{ $expected }}</pre>
                </div>
            @endif
            @if ($references)
                <div class="flex flex-col gap-3 sm:flex-row sm:items-start" data-test="expected-references">
                    @foreach (['mobile' => ['Celular', 'sm:w-48'], 'desktop' => ['Compu', 'sm:flex-1']] as $device => [$label, $width])
                        @isset ($references[$device])
                            <figure class="flex min-w-0 flex-col gap-1 {{ $width }}">
                                <figcaption class="tech-label">{{ $label }}</figcaption>
                                <a href="{{ $references[$device] }}" target="_blank" rel="noopener" class="block max-h-80 overflow-y-auto rounded border border-outline bg-white">
                                    <img src="{{ $references[$device] }}" alt="Así tiene que quedar en {{ Str::lower($label) }}" loading="lazy" class="w-full">
                                </a>
                            </figure>
                        @endisset
                    @endforeach
                </div>
                <p class="text-xs text-ink-muted">Así tiene que quedar tu página. Con «Comparar», en la vista previa, la ves en el mismo tamaño que la tuya.</p>
            @endif
        </div>
    </details>
@endif
