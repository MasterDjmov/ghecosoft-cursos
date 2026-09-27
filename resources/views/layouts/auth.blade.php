<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}" class="dark">
    <head>
        @include('partials.head')
    </head>
    <body class="min-h-screen">
        <div class="grid min-h-svh lg:grid-cols-[1.15fr_1fr]">
            {{-- Banner: solo en pantallas grandes. --}}
            <div class="relative hidden overflow-hidden border-e border-outline lg:block">
                <img src="/images/banner.webp" alt="" class="absolute inset-0 size-full object-cover">
                <div class="absolute inset-0 bg-linear-to-t from-surface via-surface/40 to-transparent"></div>
                <div class="absolute inset-x-0 bottom-0 p-10">
                    <p class="tech-label"><span class="live-dot me-2"></span>Plataforma de cursos</p>
                    <p class="mt-3 max-w-md font-display text-3xl font-semibold leading-tight text-white">
                        Aprendé a programar avanzando por tu árbol de habilidades.
                    </p>
                </div>
            </div>

            <div class="flex flex-col items-center justify-center gap-8 px-4 py-10 sm:px-10">
                <x-app-logo href="{{ route('login') }}" />

                <div class="panel w-full max-w-md p-6 sm:p-8">
                    {{ $slot }}
                </div>
            </div>
        </div>

        @persist('toast')
            <flux:toast.group>
                <flux:toast />
            </flux:toast.group>
        @endpersist

        @fluxScripts
    </body>
</html>
