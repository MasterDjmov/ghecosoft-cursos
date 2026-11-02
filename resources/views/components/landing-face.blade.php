@props(['character'])

{{-- La cara redonda de un personaje en la portada. Con `bust`, la imagen es de cuerpo entero (Enciclopedia) y se
     muestra solo la cabeza y los hombros; si no, es un avatar y se agranda un poco para que no se vea su marco. --}}
<div {{ $attributes->class('relative size-28 shrink-0 overflow-hidden rounded-full bg-surface-lowest ring-2 transition hover:scale-105') }}>
    <img src="{{ $character['image'] }}" alt="{{ $character['name'] }}" loading="lazy"
        @class([
            'absolute top-[-11%] left-[-95%] w-[290%] max-w-none' => $character['bust'],
            'size-full scale-[1.12] object-cover' => ! $character['bust'],
        ])>
</div>
