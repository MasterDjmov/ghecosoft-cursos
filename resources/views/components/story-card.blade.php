@props(['story', 'course', 'icon' => 'sparkles', 'tone' => 'secondary', 'scene' => null])

{{-- Un texto de historia con la mentora del curso (Diccionario: mentor.name). Con `scene`, el fondo del
     mundo (la región del curso o el Mundo del Código) detrás de un degradé que deja leer el texto. --}}
<aside {{ $attributes->class([
    'relative flex flex-col gap-3 overflow-hidden rounded-lg border px-6 py-5',
    'border-secondary/40 bg-secondary/10' => $tone === 'secondary',
    'border-success/40 bg-success/10' => $tone === 'success',
    'border-warning/40 bg-warning/10' => $tone === 'warning',
    'min-h-80 justify-end' => $scene,
]) }}>
    @if ($scene)
        <img src="{{ $scene }}" alt="" aria-hidden="true" class="pointer-events-none absolute inset-0 size-full object-cover" data-test="story-scene">
        <div class="pointer-events-none absolute inset-0 bg-gradient-to-t from-[#070a14] via-[#070a14]/80 to-transparent" aria-hidden="true"></div>
    @endif
    <div class="relative flex flex-wrap items-center justify-between gap-2">
        <p @class(['tech-label flex items-center gap-2', 'text-secondary-bright' => $tone === 'secondary', 'text-success' => $tone === 'success', 'text-warning' => $tone === 'warning'])>
            <flux:icon :name="$icon" variant="micro" /> {{ $story['title'] }}
        </p>
        <x-companion key="mentor.name" :course="$course" />
    </div>
    @if ($story['html'])
        <div @class(['markdown relative text-ink', 'drop-shadow-[0_1px_2px_rgba(0,0,0,0.9)]' => $scene])>{!! $story['html'] !!}</div>
    @endif
    @if ($slot->isNotEmpty())
        <div class="relative">{{ $slot }}</div>
    @endif
</aside>
