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
                        <flux:sidebar.item icon="inbox-arrow-down" :href="route('admin.requests')" :current="request()->routeIs('admin.requests')" wire:navigate
                            :badge="\App\Models\EnrollmentRequest::where('status', 'pending')->count() ?: null">
                            Solicitudes
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="code-bracket-square" :href="route('admin.submissions.index')" :current="request()->routeIs('admin.submissions.*')" wire:navigate
                            :badge="\App\Models\Submission::where('status', 'submitted')->count() ?: null">
                            Entregas
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="users" :href="route('admin.students.index')" :current="request()->routeIs('admin.students.*')" wire:navigate>
                            Alumnos
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="document-check" :href="route('admin.authorizations')" :current="request()->routeIs('admin.authorizations')" wire:navigate
                            :badge="\App\Models\GuardianAuthorization::where('status', 'pending')->count() ?: null">
                            Autorizaciones
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
                        <flux:sidebar.item icon="cog-6-tooth" :href="route('admin.settings')" :current="request()->routeIs('admin.settings')" wire:navigate>
                            Configuración
                        </flux:sidebar.item>
                    </flux:sidebar.group>
                    <flux:sidebar.group heading="Vista del alumno" class="grid">
                        <flux:sidebar.item icon="globe-americas" :href="route('student.worlds')" :current="request()->routeIs('student.*')" wire:navigate>
                            Mundos
                        </flux:sidebar.item>
                    </flux:sidebar.group>
                @else
                    <flux:sidebar.group heading="Aprender" class="grid">
                        <flux:sidebar.item icon="globe-americas" :href="route('student.worlds')" :current="request()->routeIs('student.worlds', 'student.course', 'student.tree', 'student.node')" wire:navigate>
                            Mundos
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="trophy" :href="route('student.ranking')" :current="request()->routeIs('student.ranking*')" wire:navigate>
                            Ranking
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="identification" :href="route('cv.show', auth()->user()->username)" target="_blank">
                            Mi CV
                        </flux:sidebar.item>
                    </flux:sidebar.group>
                @endif
            </flux:sidebar.nav>

            <flux:spacer />

            <flux:sidebar.nav>
                <flux:sidebar.item icon="user-circle" :href="route('profile.edit')" :current="request()->routeIs('profile.edit', 'security.edit', 'movements', 'privacy')" wire:navigate>
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

            <livewire:notifications-bell />
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
