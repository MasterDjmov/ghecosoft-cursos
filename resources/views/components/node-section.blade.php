@props(['title', 'icon', 'companion' => null, 'course' => null, 'color' => 'text-primary-bright'])

{{-- Una sección del nodo (D37): título con ícono y, si corresponde, el personaje que la presenta. --}}
<section {{ $attributes->class('flex flex-col gap-3') }}>
    <header class="flex flex-wrap items-center justify-between gap-2">
        <h3 class="flex items-center gap-2 font-display text-base font-semibold text-white">
            <flux:icon :name="$icon" variant="mini" class="{{ $color }}" /> {{ $title }}
        </h3>
        @if ($companion)
            <x-companion :key="$companion" :course="$course" :color="$color" />
        @endif
    </header>
    {{ $slot }}
</section>
