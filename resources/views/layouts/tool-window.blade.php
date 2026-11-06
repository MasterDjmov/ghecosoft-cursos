{{-- Una herramienta (D120) suelta, adentro de la ventana flotante: sin menú ni barra. --}}
<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}" class="dark" style="color-scheme: dark">
    <head>
        @include('partials.head')
    </head>
    <body class="min-h-screen">
        {{ $slot }}
        @fluxScripts
    </body>
</html>
