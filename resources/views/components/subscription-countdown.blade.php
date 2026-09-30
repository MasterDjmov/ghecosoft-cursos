@props(['until', 'total' => 30, 'compact' => false])

{{-- Días de abono que le quedan al alumno en un curso (cada curso tiene los suyos), en neón:
     cian con más de 7, ámbar de 7 a 4, rojo y latiendo con 3 o menos. $until = TreeAccess::paidUntil(). --}}
@php
    $days = max(0, (int) ceil(now()->diffInMinutes($until, false) / 1440));
    $color = match (true) { $days <= 3 => '#f87171', $days <= 7 => '#f59e0b', default => '#22d3ee' };
    $percent = min(100, max(4, (int) round($days / max(1, $total) * 100)));
    $label = match (true) { $days === 0 => 'vence hoy', $days === 1 => 'día de abono', default => 'días de abono' };
@endphp

<div {{ $attributes->class(['inline-flex shrink-0 items-center rounded-lg border bg-surface-lowest/60', 'gap-2 px-2.5 py-1.5' => $compact, 'gap-3 px-3.5 py-2' => ! $compact, 'animate-pulse' => $days <= 3]) }}
    style="border-color: {{ $color }}80; box-shadow: 0 0 14px {{ $color }}33, inset 0 0 14px {{ $color }}14"
    title="Abono pago hasta el {{ $until->format('d/m/Y H:i') }}" data-test="countdown" data-days="{{ $days }}">
    <span @class(['font-display font-bold leading-none tabular-nums', 'text-xl' => $compact, 'text-3xl' => ! $compact])
        style="color: {{ $color }}; text-shadow: 0 0 6px {{ $color }}, 0 0 16px {{ $color }}99">{{ $days === 0 ? '0' : $days }}</span>
    <span class="flex flex-col gap-1">
        <span class="font-mono text-[10px] tracking-widest uppercase" style="color: {{ $color }}">{{ $label }}</span>
        <span @class(['block h-1 overflow-hidden rounded-full bg-surface-highest', 'w-16' => $compact, 'w-24' => ! $compact])>
            <span class="block h-full rounded-full" style="width: {{ $percent }}%; background-color: {{ $color }}; box-shadow: 0 0 6px {{ $color }}"></span>
        </span>
    </span>
</div>
