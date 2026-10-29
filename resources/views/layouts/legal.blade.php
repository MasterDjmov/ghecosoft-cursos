<!DOCTYPE html>
<html lang="es" class="dark">
    <head>
        @include('partials.head')
    </head>
    <body class="min-h-screen">
        <header class="border-b border-outline bg-surface/85">
            <div class="mx-auto flex max-w-3xl items-center justify-between gap-4 px-4 py-3 sm:px-8">
                <x-app-logo href="{{ route('landing') }}" />
                @auth
                    <flux:button size="sm" variant="ghost" :href="route('home')">Volver a la plataforma</flux:button>
                @else
                    <flux:button size="sm" variant="ghost" :href="route('login')">Entrar</flux:button>
                @endauth
            </div>
        </header>

        <main class="mx-auto flex w-full max-w-3xl flex-col gap-6 px-4 py-8 sm:px-8">
            {{ $slot }}
        </main>

        <footer class="border-t border-outline px-4 py-6">
            <x-legal-links />
        </footer>

        @fluxScripts
    </body>
</html>
