@props(['course', 'size' => 'size-14'])

{{-- Logo del curso; si no tiene, la abreviatura del lenguaje. --}}
@if ($course->logoUrl())
    <img src="{{ $course->logoUrl() }}" alt="{{ $course->title }}" {{ $attributes->class([$size, 'shrink-0 rounded-full border border-primary-bright/40 object-cover']) }}>
@else
    <div {{ $attributes->class([$size, 'grid shrink-0 place-items-center rounded-full border border-primary-bright/40 bg-primary/10 font-display text-lg font-bold text-primary-bright']) }} title="{{ $course->language->label() }}">
        {{ $course->language->short() }}
    </div>
@endif
