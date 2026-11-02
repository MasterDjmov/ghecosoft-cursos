@props(['index', 'label'])

{{-- Tapa la tarjeta cuando está a un costado: tocarla la trae al medio (y no se usan sus botones de lejos). --}}
<button type="button" x-show="active !== {{ $index }}" x-cloak x-on:click="go({{ $index }})"
        class="absolute inset-0 z-10 cursor-pointer rounded-lg" aria-label="Ver {{ $label }}"></button>
