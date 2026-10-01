@props(['key', 'course' => null, 'color' => 'text-primary-bright'])

@php
    $companion = app(\App\Support\Glossary::class)->resolve($key, $course);
    $name = \Illuminate\Support\Str::ucfirst($companion['singular']);
    $px = \App\Support\Portraits::companion();
@endphp

{{-- Un personaje de la compañía (Diccionario): retrato si tiene ícono, si no su inicial. --}}
<span {{ $attributes->class('inline-flex items-center gap-2') }} title="{{ $companion['short_description'] }}">
    @if ($companion['icon_path'])
        <img src="{{ Storage::disk('public')->url($companion['icon_path']) }}" alt="" class="shrink-0 rounded-lg border border-outline object-cover" style="width: {{ $px }}px; height: {{ $px }}px">
    @else
        <span class="grid size-9 shrink-0 place-items-center rounded-full border border-outline bg-surface-highest font-display text-xs font-semibold {{ $color }}" aria-hidden="true">
            {{ \Illuminate\Support\Str::upper(\Illuminate\Support\Str::substr(\Illuminate\Support\Str::after($name, ' ') ?: $name, 0, 1)) }}
        </span>
    @endif
    <span class="tech-label">{{ $name }}</span>
</span>
