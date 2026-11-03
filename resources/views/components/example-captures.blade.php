@props(['references' => []])

{{-- «Así se ve»: el ejemplo del nodo ya dibujado, en celular (390 px) y en compu (1280 px), como las capturas de cada
     clase del material. Abierto: es lo primero que se mira; cada imagen se abre entera en otra pestaña. --}}
@php($references = array_filter($references ?? []))
@if ($references)
    <div {{ $attributes->class('flex flex-col gap-2') }} data-test="example-captures">
        <p class="tech-label flex items-center gap-2"><flux:icon name="photo" variant="micro" class="text-primary-bright" /> Así se ve</p>
        <div class="flex flex-col gap-3 sm:flex-row sm:items-start">
            @foreach (['mobile' => ['Celular', 'sm:w-56'], 'desktop' => ['Compu', 'sm:flex-1']] as $device => [$label, $width])
                @isset ($references[$device])
                    <figure class="flex min-w-0 flex-col gap-1 {{ $width }}">
                        <figcaption class="font-mono text-[11px] text-ink-muted">{{ $label }}</figcaption>
                        <a href="{{ $references[$device] }}" target="_blank" rel="noopener" class="block max-h-[28rem] overflow-y-auto rounded-lg border border-outline bg-white shadow-lg">
                            <img src="{{ $references[$device] }}" alt="El ejemplo en {{ Str::lower($label) }}" loading="lazy" class="w-full">
                        </a>
                    </figure>
                @endisset
            @endforeach
        </div>
    </div>
@endif
