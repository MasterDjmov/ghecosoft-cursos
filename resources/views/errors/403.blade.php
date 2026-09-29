<!DOCTYPE html>
<html lang="es" class="dark">
    <head>
        @include('partials.head', ['title' => 'Zona prohibida'])
        <link rel="preload" as="image" href="/images/error-403.webp">
    </head>
    {{-- 403 de la plataforma: la imagen entera al centro, su propio reflejo desenfocado llena la pantalla y el mensaje va debajo. --}}
    <body class="min-h-screen overflow-x-hidden bg-surface-lowest">
        <div aria-hidden="true" class="fixed inset-0 -z-10">
            <img src="/images/error-403.webp" alt="" class="size-full scale-110 object-cover opacity-50 blur-2xl">
            <div class="absolute inset-0 bg-linear-to-b from-surface-lowest/30 via-surface-lowest/60 to-surface-lowest"></div>
        </div>

        <main class="flex min-h-screen flex-col items-center justify-center gap-6 px-4 py-8 sm:py-10">
            <img src="/images/error-403.webp" alt="Error 403: el geco guardián frena el paso ante una puerta sellada"
                style="width: min(100%, 72rem, calc((100vh - 22rem) * 1.79))"
                class="aspect-[1376/768] rounded-2xl border border-danger/40 object-cover shadow-[0_0_60px_-12px_rgb(239_68_68/0.55)]">

            <section class="panel flex w-full max-w-xl flex-col items-center gap-3 border-danger/40 bg-surface-low/85 p-6 text-center backdrop-blur sm:px-8">
                <p class="tech-label text-danger!">Error 403 · Zona prohibida</p>
                <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Esta puerta está sellada</h1>
                <p class="text-ink-muted">
                    El guardián no te deja pasar: esta zona no es para tu cuenta, o lo que buscás pertenece a otro héroe.
                    Si creés que es un error, escribile al profe.
                </p>
                <a href="{{ auth()->check() ? route('home') : route('landing') }}"
                    class="mt-2 inline-flex items-center gap-2 rounded-lg bg-primary-bright px-6 py-3 font-semibold text-surface-lowest shadow-[0_0_24px_-4px_rgb(34_211_238/0.7)] transition hover:brightness-110"
                    data-test="error-home">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-5" aria-hidden="true"><path fill-rule="evenodd" d="M9.293 2.293a1 1 0 0 1 1.414 0l7 7A1 1 0 0 1 17 11h-1v6a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-6H3a1 1 0 0 1-.707-1.707l7-7Z" clip-rule="evenodd" /></svg>
                    Volver a mi inicio
                </a>
            </section>
        </main>
    </body>
</html>
