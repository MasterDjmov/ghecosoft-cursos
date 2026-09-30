@props(['count' => 0])

{{-- Cantidad de entregas de una práctica: 1 verde, 2–3 amarillo, 4 o más rojo (para pensar antes de entregar). --}}
@if ($count > 0)
    @php($color = match (true) { $count === 1 => '#10b981', $count <= 3 => '#f59e0b', default => '#f87171' })
    <span {{ $attributes->class('inline-flex shrink-0 items-center gap-1 rounded-md border px-1.5 py-0.5 font-mono text-[11px] leading-none') }}
        style="color: {{ $color }}; border-color: {{ $color }}66; background-color: {{ $color }}14; text-shadow: 0 0 6px {{ $color }}66"
        title="{{ $count }} {{ $count === 1 ? 'intento' : 'intentos' }}" data-test="attempts" data-attempts="{{ $count }}">
        <flux:icon name="arrow-path" variant="micro" class="size-3" />{{ $count }}
    </span>
@endif
