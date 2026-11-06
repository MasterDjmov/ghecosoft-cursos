@props(['name'])

{{-- Los íconos de la tabla de caracteres: Windows, Linux (el pingüino) y DOS. --}}
<svg viewBox="0 0 24 24" {{ $attributes->merge(['class' => 'size-4 shrink-0']) }} aria-hidden="true">
    @if ($name === 'windows')
        <path fill="currentColor" d="M3 5.4 10.5 4.3v7.2H3zM11.5 4.2 21 2.8v8.7h-9.5zM3 12.5h7.5v7.2L3 18.6zM11.5 12.5H21v8.7l-9.5-1.4z" />
    @elseif ($name === 'linux')
        <ellipse cx="12" cy="12.5" rx="6.5" ry="9" fill="currentColor" />
        <ellipse cx="12" cy="15" rx="3.7" ry="5.5" fill="#fff" />
        <circle cx="10.2" cy="7.6" r="1.1" fill="#fff" /><circle cx="13.8" cy="7.6" r="1.1" fill="#fff" />
        <path fill="#f59e0b" d="M10.5 9.3h3L12 11.3zM6 19.5c1.6-.8 3.4-.5 4.2 1.4.2.6-.2 1.1-.8 1.1H6.3c-1 0-1.4-2-.3-2.5zM18 19.5c-1.6-.8-3.4-.5-4.2 1.4-.2.6.2 1.1.8 1.1h3.1c1 0 1.4-2 .3-2.5z" />
    @else
        <path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M3 4.5h18v12H3zM9 20.5h6M12 16.5v4M6.5 8l3 2.5-3 2.5M11.5 13h4" />
    @endif
</svg>
