@props(['course', 'nodes' => 0])

{{-- Tarjeta del catálogo (Mundos y landing). "Próximamente" lleva la portada y el temario, sin entrar. --}}
@php($upcoming = $course->isUpcoming())
<article {{ $attributes->class(['panel flex flex-col overflow-hidden', 'border-dashed' => $upcoming]) }} data-test="catalog-{{ $course->slug }}">
    @if ($upcoming && $course->coverUrl())
        <div class="relative h-32 overflow-hidden">
            <img src="{{ $course->coverUrl() }}" alt="" class="size-full object-cover opacity-80">
            <div class="absolute inset-0 bg-linear-to-t from-surface-low to-transparent"></div>
        </div>
    @endif

    <div class="flex flex-1 flex-col gap-4 p-5">
        <div class="flex items-start justify-between gap-3">
            <x-course-logo :course="$course" size="size-12" />
            @if ($upcoming)
                <span class="rounded border border-secondary-bright/40 px-2 py-0.5 font-mono text-[11px] text-secondary-bright">Próximamente</span>
            @endif
        </div>

        <div class="flex flex-col gap-1">
            <h3 class="font-display text-lg font-semibold text-white">{{ $course->title }}</h3>
            <p class="font-mono text-[11px] text-ink-muted">
                {{ $course->language->label() }} · {{ $course->level->label() }}@unless ($upcoming) · {{ $nodes }} {{ term('node', $course, $nodes) }}@endunless
            </p>
            @if ($course->short_description)
                <p class="text-sm text-ink-muted">{{ $course->short_description }}</p>
            @endif
        </div>

        @if ($items = $course->syllabusItems())
            <div class="flex flex-col gap-1">
                <p class="tech-label">{{ $upcoming ? 'Qué se va a dar' : 'Temario' }}</p>
                <ul class="flex flex-col gap-0.5 text-sm text-ink">
                    @foreach (array_slice($items, 0, 5) as $item)
                        <li class="flex gap-2"><span class="text-primary-bright">›</span> {{ $item }}</li>
                    @endforeach
                    @if (count($items) > 5)
                        <li class="text-xs text-ink-muted">y {{ count($items) - 5 }} {{ count($items) - 5 === 1 ? 'tema' : 'temas' }} más</li>
                    @endif
                </ul>
            </div>
        @endif

        <div class="mt-auto flex flex-wrap gap-2 pt-1">
            {{ $slot }}
        </div>
    </div>
</article>
