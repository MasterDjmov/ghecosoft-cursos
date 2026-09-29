@props(['currency', 'size' => 'size-8'])

{{-- La moneda: su imagen del diccionario (coin.course del curso o coin.wildcard) o, si no hay, la sigla del lenguaje / ★. --}}
@php($icon = app(\App\Support\Glossary::class)->resolve($currency->is_wildcard ? 'coin.wildcard' : 'coin.course', $currency->is_wildcard ? null : $currency->course)['icon_path'])
@if ($icon)
    <img src="{{ Storage::disk('public')->url($icon) }}" alt="" {{ $attributes->class([$size, 'shrink-0 rounded-full object-cover']) }}>
@else
    <span {{ $attributes->class([
        $size, 'grid shrink-0 place-items-center rounded-full font-mono text-[11px] font-bold',
        'bg-secondary/25 text-secondary-bright' => $currency->is_wildcard,
        'bg-primary/20 text-primary-bright' => ! $currency->is_wildcard,
    ]) }}>{{ $currency->is_wildcard ? '★' : mb_strtoupper($currency->course?->language->short() ?? '?') }}</span>
@endif
