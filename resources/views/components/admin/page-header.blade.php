@props(['label' => 'Panel del docente', 'title', 'subtitle' => null])

<header {{ $attributes->class('flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between') }}>
    <div class="flex flex-col gap-1">
        <p class="tech-label">{{ $label }}</p>
        <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">{{ $title }}</h1>
        @if ($subtitle)
            <p class="text-ink-muted">{{ $subtitle }}</p>
        @endif
    </div>
    @isset($actions)
        <div class="flex shrink-0 flex-wrap items-center gap-2">{{ $actions }}</div>
    @endisset
</header>
