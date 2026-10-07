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
                @if (auth()->user()->isStaff())
                    @php($isAdmin = auth()->user()->isAdmin())
                    <flux:sidebar.group :heading="$isAdmin ? 'Administración' : 'Docente'" class="grid">
                        @if ($isAdmin)
                            <flux:sidebar.item icon="squares-2x2" :href="route('admin.dashboard')" :current="request()->routeIs('admin.dashboard')" wire:navigate>
                                Inicio
                            </flux:sidebar.item>
                            <flux:sidebar.item icon="inbox-arrow-down" :href="route('admin.requests')" :current="request()->routeIs('admin.requests')" wire:navigate
                                :badge="\App\Models\EnrollmentRequest::where('status', 'pending')->count() ?: null">
                                Solicitudes
                            </flux:sidebar.item>
                        @endif
                        {{-- Entregas, mensajes y alumnos: del docente, los de sus comisiones (D72). --}}
                        <flux:sidebar.item icon="code-bracket-square" :href="route('admin.submissions.index')" :current="request()->routeIs('admin.submissions.*')" wire:navigate
                            :badge="app(\App\Services\TeacherScope::class)->submissions(\App\Models\Submission::query(), auth()->user())->where('status', 'submitted')->count() ?: null">
                            Entregas
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="chat-bubble-left-right" :href="route('admin.messages')" :current="request()->routeIs('admin.messages')" wire:navigate
                            :badge="\App\Livewire\Admin\Messages::unreadQuery()->count() ?: null">
                            Mensajes
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="users" :href="route('admin.students.index')" :current="request()->routeIs('admin.students.*')" wire:navigate>
                            Alumnos
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="user-group" :href="route('admin.cohorts')" :current="request()->routeIs('admin.cohorts', 'admin.syllabus')" wire:navigate>
                            Comisiones
                        </flux:sidebar.item>
                        @if ($isAdmin)
                        <flux:sidebar.item icon="document-check" :href="route('admin.authorizations')" :current="request()->routeIs('admin.authorizations')" wire:navigate
                            :badge="\App\Models\GuardianAuthorization::where('status', 'pending')->count() ?: null">
                            Autorizaciones
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="share" :href="route('admin.courses.index')" :current="request()->routeIs('admin.courses.*', 'admin.nodes.*')" wire:navigate>
                            Cursos y árboles
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="globe-alt" :href="route('admin.universe')" :current="request()->routeIs('admin.universe')" wire:navigate>
                            Universo
                        </flux:sidebar.item>
                        @endif
                    </flux:sidebar.group>
                    @if ($isAdmin)
                    <flux:sidebar.group heading="Juego" class="grid">
                        <flux:sidebar.item icon="book-open" :href="route('admin.glossary')" :current="request()->routeIs('admin.glossary')" wire:navigate>
                            Diccionario
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="sparkles" :href="route('admin.story')" :current="request()->routeIs('admin.story')" wire:navigate data-test="menu-story">
                            Historia
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="photo" :href="route('admin.scenes')" :current="request()->routeIs('admin.scenes')" wire:navigate data-test="menu-scenes">
                            Escenas
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
                    @endif
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
                        {{-- Mis Crónicas (D80): late cuando hay páginas nuevas sin leer. --}}
                        @php($newPages = (new \App\Support\Chronicles(auth()->user()))->newCount())
                        <flux:sidebar.item icon="book-open" :href="route('student.chronicles')" :current="request()->routeIs('student.chronicles')" wire:navigate data-test="menu-chronicles">
                            <span class="flex items-center gap-2">
                                Mis Crónicas
                                @if ($newPages > 0)
                                    <span class="relative flex size-5 items-center justify-center" data-test="chronicles-new" title="{{ $newPages }} {{ $newPages === 1 ? 'página nueva' : 'páginas nuevas' }}">
                                        <span class="absolute inline-flex size-full animate-ping rounded-full bg-warning/60"></span>
                                        <span class="relative grid size-5 place-items-center rounded-full bg-warning font-mono text-[10px] font-bold text-[#05070d]">{{ $newPages }}</span>
                                    </span>
                                @endif
                            </span>
                        </flux:sidebar.item>
                        <flux:sidebar.item icon="sparkles" :href="route('student.universe')" :current="request()->routeIs('student.universe')" wire:navigate data-test="menu-universe">
                            Universo
                        </flux:sidebar.item>
                        {{-- Herramientas → Ejecutor de Java (D85): para quien cursa o pidió un curso de Java. --}}
                        @if (\App\Models\Course::where('language', \App\Enums\Language::Java)->where(fn ($q) => $q->whereHas('subscriptions', fn ($s) => $s->where('user_id', auth()->id()))->orWhereHas('enrollmentRequests', fn ($r) => $r->where('user_id', auth()->id())))->exists())
                            <flux:sidebar.item icon="command-line" :href="route('student.java-runner')" :current="request()->routeIs('student.java-runner')" wire:navigate data-test="menu-java-runner">
                                Ejecutor de Java
                            </flux:sidebar.item>
                        @endif
                        <flux:sidebar.item icon="identification" :href="route('cv.show', auth()->user()->cv_slug)" target="_blank">
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

            @unless (auth()->user()->isStaff())
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
