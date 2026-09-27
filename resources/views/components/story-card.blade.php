@props(['story', 'course', 'icon' => 'sparkles', 'tone' => 'secondary'])

{{-- Un texto de historia con la mentora del curso (Diccionario: mentor.name). --}}
<aside {{ $attributes->class([
    'relative flex flex-col gap-3 overflow-hidden rounded-lg border px-6 py-5',
    'border-secondary/40 bg-secondary/10' => $tone === 'secondary',
    'border-success/40 bg-success/10' => $tone === 'success',
    'border-warning/40 bg-warning/10' => $tone === 'warning',
]) }}>
    <div class="flex flex-wrap items-center justify-between gap-2">
        <p @class(['tech-label flex items-center gap-2', 'text-secondary-bright' => $tone === 'secondary', 'text-success' => $tone === 'success', 'text-warning' => $tone === 'warning'])>
            <flux:icon :name="$icon" variant="micro" /> {{ $story['title'] }}
        </p>
        <x-companion key="mentor.name" :course="$course" />
    </div>
    @if ($story['html'])
        <div class="markdown text-ink">{!! $story['html'] !!}</div>
    @endif
    {{ $slot }}
</aside>
