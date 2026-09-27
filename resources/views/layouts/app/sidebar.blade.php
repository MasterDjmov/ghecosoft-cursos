<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}" class="dark">
    <head>
        @include('partials.head')
    </head>
    <body class="min-h-screen">
        <flux:sidebar sticky collapsible="mobile" class="border-e border-outline bg-surface-lowest/95 backdrop-blur-md">
            <flux:sidebar.header>
                <x-app-logo href="{{ route('home') }}" wire:navigate />
                <flux:sidebar.collapse class="lg:hidden" />
            </flux:sidebar.header>

            <flux:sidebar.nav>
                @if (auth()->user()->isAdmin())
                    <flux:sidebar.group heading="Docente" class="grid">
                        <flux:sidebar.item icon="squares-2x2" :href="route('admin.dashboard')" :current="request()->routeIs('admin.dashboard')" wire:navigate>
                            Inicio
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="share" :href="route('admin.courses.index')" :current="request()->routeIs('admin.courses.*', 'admin.nodes.*')" wire:navigate>
                            Cursos y árboles
                        </flux:sidebar.item>
                    </flux:sidebar.group>
                    <flux:sidebar.group heading="Juego" class="grid">
                        <flux:sidebar.item icon="book-open" :href="route('admin.glossary')" :current="request()->routeIs('admin.glossary')" wire:navigate>
                            Diccionario
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="chart-bar" :href="route('admin.levels')" :current="request()->routeIs('admin.levels')" wire:navigate>
                            Niveles
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="trophy" :href="route('admin.badges')" :current="request()->routeIs('admin.badges')" wire:navigate>
                            Insignias
                        </flux:sidebar.item>
                    </flux:sidebar.group>
                    <flux:sidebar.group heading="Vista del alumno" class="grid">
                        <flux:sidebar.item icon="globe-americas" :href="route('student.worlds')" :current="request()->routeIs('student.worlds')" wire:navigate>
                            Mundos
                        </flux:sidebar.item>
                    </flux:sidebar.group>
                @else
                    <flux:sidebar.group heading="Aprender" class="grid">
                        <flux:sidebar.item icon="globe-americas" :href="route('student.worlds')" :current="request()->routeIs('student.worlds')" wire:navigate>
                            Mundos
                        </flux:sidebar.item>
                    </flux:sidebar.group>
                @endif
            </flux:sidebar.nav>

            <flux:spacer />

            <flux:sidebar.nav>
                <flux:sidebar.item icon="user-circle" :href="route('profile.edit')" :current="request()->routeIs('profile.edit', 'security.edit')" wire:navigate>
                    Mi cuenta
                </flux:sidebar.item>
            </flux:sidebar.nav>
        </flux:sidebar>

        {{-- Barra superior: saldos (alumno) y menú del avatar. --}}
        <flux:header class="sticky top-0 z-20 border-b border-outline bg-surface/80 backdrop-blur-md">
            <flux:sidebar.toggle class="lg:hidden" icon="bars-2" inset="left" />

            @unless (auth()->user()->isAdmin())
                <x-wallet-bar class="hidden sm:flex" />
            @endunless

            <flux:spacer />

            <x-desktop-user-menu />
        </flux:header>

        {{ $slot }}

        @persist('toast')
            <flux:toast.group>
                <flux:toast />
            </flux:toast.group>
        @endpersist

        @fluxScripts
    </body>
</html>
