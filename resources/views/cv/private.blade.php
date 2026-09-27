<!DOCTYPE html>
<html lang="es" class="dark">
    <head>
        @include('partials.head', ['title' => 'Perfil privado'])
        <meta name="robots" content="noindex">
    </head>
    <body class="grid min-h-screen place-items-center p-6">
        <div class="panel flex max-w-md flex-col items-center gap-4 p-8 text-center">
            <img src="/images/logo-mark.jpg" alt="" class="size-16 rounded-full">
            <h1 class="font-display text-xl font-semibold text-white">Este perfil es privado</h1>
            <p class="text-ink-muted">La persona no compartió su CV o el link no existe.</p>
            <a href="{{ url('/') }}" class="text-sm text-primary-bright hover:underline">{{ config('app.name') }}</a>
        </div>
    </body>
</html>
