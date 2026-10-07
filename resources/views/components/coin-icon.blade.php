@props(['currency', 'size' => 'size-9'])

{{-- La moneda: su imagen del diccionario (coin.course del curso o coin.wildcard) o, si no hay, la sigla del lenguaje / ★. El oro (D89), su moneda. --}}
@php($icon = $currency->isGold() ? null : app(\App\Support\Glossary::class)->resolve($currency->is_wildcard ? 'coin.wildcard' : 'coin.course', $currency->is_wildcard ? null : $currency->course)['icon_path'])
@if ($currency->isGold())
    <x-gold-icon :attributes="$attributes->class([$size])" />
@elseif ($icon)
    <img src="{{ Storage::disk('public')->url($icon) }}" alt="" {{ $attributes->class([$size, 'shrink-0 rounded-full object-cover']) }}>
@else
    <span {{ $attributes->class([
        $size, 'grid shrink-0 place-items-center rounded-full font-mono text-[11px] font-bold',
        'bg-secondary/25 text-secondary-bright' => $currency->is_wildcard,
        'bg-primary/20 text-primary-bright' => ! $currency->is_wildcard,
    ]) }}>{{ $currency->is_wildcard ? '★' : mb_strtoupper($currency->course?->language->short() ?? '?') }}</span>
@endif
