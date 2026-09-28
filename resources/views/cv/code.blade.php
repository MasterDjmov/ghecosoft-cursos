<!DOCTYPE html>
<html lang="es" class="dark">
    <head>
        @include('partials.head', ['title' => 'CV protegido'])
        <meta name="robots" content="noindex">
    </head>
    <body class="grid min-h-screen place-items-center p-6">
        <div class="panel flex w-full max-w-sm flex-col items-center gap-4 p-8 text-center">
            <img src="/images/logo-mark.jpg" alt="" class="size-16 rounded-full">
            <h1 class="font-display text-xl font-semibold text-white">Este CV pide un código</h1>
            <p class="text-ink-muted">Escribí el código de 6 cifras que te pasó la persona para ver su CV.</p>

            <form method="POST" action="{{ route('cv.unlock', $slug) }}" class="flex w-full flex-col gap-3">
                @csrf
                <input name="code" inputmode="numeric" autocomplete="off" maxlength="7" required autofocus
                    placeholder="000000" data-test="cv-code"
                    class="w-full rounded-lg border border-outline bg-surface-lowest px-4 py-3 text-center font-mono text-2xl tracking-[0.4em] text-white placeholder:text-ink-muted/40 focus:border-primary focus:outline-none">
                @error('code')
                    <p class="text-sm text-danger">{{ $message }}</p>
                @enderror
                @if ($blocked && ! $errors->has('code'))
                    <p class="text-sm text-danger">Demasiados intentos. Probá de nuevo en {{ ceil($blocked / 60) }} minutos.</p>
                @endif
                <button type="submit" class="rounded-lg bg-primary px-4 py-2.5 font-semibold text-surface hover:bg-primary-bright">Ver el CV</button>
            </form>

            <a href="{{ url('/') }}" class="text-sm text-primary-bright hover:underline">{{ config('app.name') }}</a>
        </div>
    </body>
</html>
