@props([
    'sidebar' => false,
])

<a {{ $attributes->merge(['class' => 'flex items-center gap-2.5']) }}>
    <img src="/images/logo-mark.jpg" alt="" class="size-9 rounded-full ring-1 ring-primary-bright/40">
    <span class="font-display text-lg font-semibold tracking-tight text-white">
        GhecoSoft<span class="text-primary-bright">-Code</span>
    </span>
</a>
