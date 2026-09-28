<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}" class="dark scroll-smooth">
    <head>
        @include('partials.head', ['title' => null])
        <meta name="description" content="Aprendé a programar avanzando por tu árbol de habilidades: nodos, monedas, héroes y ranking.">
    </head>
    <body class="min-h-screen">
        @php
            $medal = [1 => 'text-[#fbbf24] border-[#fbbf24]/60', 2 => 'text-[#cbd5e1] border-[#cbd5e1]/50', 3 => 'text-[#d97706] border-[#d97706]/60'];
            $initials = fn (array $row) => \Illuminate\Support\Str::upper(\Illuminate\Support\Str::substr($row['hero'] ?: $row['name'], 0, 2));
        @endphp

        {{-- Barra superior --}}
        <header class="sticky top-0 z-30 border-b border-outline bg-surface/85 backdrop-blur-md">
            <div class="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3 sm:px-8">
                <x-app-logo href="{{ route('landing') }}" />
                <nav class="flex items-center gap-1 text-sm sm:gap-4">
                    <a href="#cursos" class="hidden px-2 text-ink-muted hover:text-white sm:inline">Cursos</a>
                    <a href="#top" class="hidden px-2 text-ink-muted hover:text-white sm:inline">Top 10</a>
                    <flux:button size="sm" variant="ghost" :href="route('login')">Entrar</flux:button>
                    <flux:button size="sm" variant="primary" :href="route('register')">Crear cuenta</flux:button>
                </nav>
            </div>
        </header>

        {{-- Portada: qué es + login en la misma pantalla --}}
        <section class="relative overflow-hidden border-b border-outline">
            <img src="/images/banner.webp" alt="" class="absolute inset-0 size-full object-cover opacity-25">
            <div class="absolute inset-0 bg-linear-to-r from-surface via-surface/85 to-surface/60"></div>

            <div class="relative mx-auto grid max-w-6xl items-center gap-10 px-4 py-14 sm:px-8 lg:grid-cols-[1.2fr_1fr] lg:py-20">
                <div class="flex flex-col gap-6">
                    <p class="tech-label"><span class="live-dot me-2"></span>Plataforma de cursos de programación</p>
                    <h1 class="font-display text-4xl leading-tight font-semibold text-white sm:text-5xl">
                        Aprendé a programar avanzando por tu <span class="text-primary-bright">árbol de habilidades</span>.
                    </h1>
                    <p class="max-w-xl text-lg text-ink-muted">
                        Cada tema es un nodo. Resolvé sus prácticas, ganá monedas para abrir el siguiente y sumá experiencia para subir en el ranking con tu héroe.
                    </p>
                    <div class="flex flex-wrap gap-3">
                        <flux:button variant="primary" icon="academic-cap" href="#cursos">Ver cursos</flux:button>
                        <flux:button icon="trophy" href="#top">Top 10</flux:button>
                    </div>

                    <ol class="grid gap-3 pt-2 sm:grid-cols-3">
                        @foreach ([['lock-open', 'Abrí nodos', 'con las monedas del curso'], ['code-bracket', 'Resolvé prácticas', 'y el profe te devuelve cada una'], ['sparkles', 'Sumá experiencia', 'insignias y rango para tu héroe']] as [$icon, $title, $text])
                            <li class="panel flex items-start gap-3 p-3">
                                <flux:icon :name="$icon" class="size-5 shrink-0 text-primary-bright" />
                                <span class="text-sm"><span class="font-medium text-white">{{ $title }}</span> <span class="text-ink-muted">{{ $text }}</span></span>
                            </li>
                        @endforeach
                    </ol>
                </div>

                <div class="panel flex flex-col gap-5 p-6" id="entrar" data-test="landing-login">
                    <div>
                        <h2 class="font-display text-xl font-semibold text-white">Entrá a tu cuenta</h2>
                        <p class="text-sm text-ink-muted">Con tu usuario o email.</p>
                    </div>
                    <form method="POST" action="{{ route('login.store') }}" class="flex flex-col gap-4">
                        @csrf
                        <flux:input name="login" label="Usuario o email" type="text" required autocomplete="username" />
                        <div class="relative">
                            <flux:input name="password" label="Contraseña" type="password" required autocomplete="current-password" viewable />
                            <flux:link class="absolute end-0 top-0 text-sm" :href="route('password.request')">¿La olvidaste?</flux:link>
                        </div>
                        <flux:checkbox name="remember" label="Recordarme" />
                        <flux:button variant="primary" type="submit" class="w-full">Entrar</flux:button>
                    </form>
                    <p class="text-center text-sm text-ink-muted">¿No tenés cuenta? <flux:link :href="route('register')">Registrate</flux:link></p>
                    <x-teacher-contact />
                </div>
            </div>
        </section>

        <main class="mx-auto flex max-w-6xl flex-col gap-20 px-4 py-16 sm:px-8">
            {{-- Cursos que más se dictan --}}
            <section id="cursos" class="flex scroll-mt-20 flex-col gap-6">
                <div class="flex flex-col gap-1">
                    <p class="tech-label">Mundos</p>
                    <h2 class="font-display text-3xl font-semibold text-white">Los cursos que más se dictan</h2>
                    <p class="text-ink-muted">Se cursan en comisiones, con el profe. Creá tu cuenta y pedí tu lugar, o consultá por WhatsApp.</p>
                </div>
                <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
                    @forelse ($courses as $course)
                        <x-catalog-card :course="$course" :nodes="$course->published_nodes_count">
                            <flux:button size="sm" variant="primary" :href="route('register')" class="flex-1">Crear cuenta</flux:button>
                            @if ($whatsapp)
                                <flux:button size="sm" icon="chat-bubble-left-right" class="flex-1" target="_blank" rel="noopener"
                                    href="https://wa.me/{{ $whatsapp }}?text={{ rawurlencode('Hola profe, quiero saber más de «'.$course->title.'».') }}">Consultar</flux:button>
                            @endif
                        </x-catalog-card>
                    @empty
                        <div class="panel p-8 text-center text-ink-muted sm:col-span-2 lg:col-span-3">Muy pronto, los primeros cursos.</div>
                    @endforelse
                </div>
            </section>

            {{-- Próximamente --}}
            @if ($upcoming->isNotEmpty())
                <section class="flex flex-col gap-6" data-test="landing-upcoming">
                    <div class="flex flex-col gap-1">
                        <p class="tech-label">En preparación</p>
                        <h2 class="font-display text-3xl font-semibold text-white">Próximamente</h2>
                        <p class="text-ink-muted">Todavía no se pueden cursar. Creá tu cuenta y pedí que te avisemos cuando salgan.</p>
                    </div>
                    <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
                        @foreach ($upcoming as $course)
                            <x-catalog-card :course="$course">
                                <flux:button size="sm" icon="bell-alert" :href="route('register')" class="w-full">Avisame cuando salga</flux:button>
                            </x-catalog-card>
                        @endforeach
                    </div>
                </section>
            @endif

            {{-- Monedas coleccionables --}}
            @if ($coins->isNotEmpty())
                <section class="flex flex-col gap-6">
                    <div class="flex flex-col gap-1">
                        <p class="tech-label">Economía</p>
                        <h2 class="font-display text-3xl font-semibold text-white">Cada mundo tiene su moneda</h2>
                        <p class="text-ink-muted">Se ganan aprobando las prácticas obligatorias y sirven para abrir los nodos de ese curso. Juntalas todas.</p>
                    </div>
                    <div class="flex flex-wrap gap-4">
                        @foreach ($coins as $coin)
                            <div class="panel flex items-center gap-3 p-3 pe-5">
                                @if ($coin['icon_path'])
                                    <img src="{{ Storage::disk('public')->url($coin['icon_path']) }}" alt="" class="size-12 rounded-full border border-[#fbbf24]/50 object-cover">
                                @else
                                    <span class="grid size-12 place-items-center rounded-full border border-[#fbbf24]/50 bg-[#fbbf24]/10 font-mono text-sm font-bold text-[#fbbf24]">{{ $coin['course']->language->short() }}</span>
                                @endif
                                <div class="flex flex-col">
                                    <span class="font-display font-semibold text-white">{{ \Illuminate\Support\Str::ucfirst($coin['plural']) }}</span>
                                    <span class="text-xs text-ink-muted">{{ $coin['short_description'] ?: 'La moneda de '.$coin['course']->title }}</span>
                                </div>
                            </div>
                        @endforeach
                    </div>
                </section>
            @endif

            {{-- Top 10 de héroes --}}
            <section id="top" class="flex scroll-mt-20 flex-col gap-8" data-test="landing-top">
                <div class="flex flex-col gap-1">
                    <p class="tech-label">Salón de la fama</p>
                    <h2 class="font-display text-3xl font-semibold text-white">Top 10 de héroes</h2>
                    <p class="text-ink-muted">Por experiencia total. La experiencia nunca baja: premia la constancia.</p>
                </div>

                @if ($top->isEmpty())
                    <div class="panel p-8 text-center text-ink-muted">Todavía no hay héroes en el top. ¡El primer lugar está libre!</div>
                @else
                    {{-- Podio: 2.º, 1.º, 3.º --}}
                    <div class="grid grid-cols-3 items-end gap-3 sm:gap-6">
                        @foreach ([2, 1, 3] as $place)
                            @if ($row = $top->firstWhere('position', $place))
                                <div @class(['panel flex flex-col items-center gap-2 p-3 text-center sm:p-5', 'panel-active pb-8 sm:pb-10' => $place === 1])>
                                    @if ($place === 1)
                                        <flux:icon name="trophy" variant="solid" class="size-7 text-[#fbbf24]" />
                                    @endif
                                    <span @class(['grid place-items-center rounded-full border-2 bg-surface-high font-display font-semibold', $medal[$place], 'size-16 text-xl sm:size-20 sm:text-2xl' => $place === 1, 'size-12 text-base sm:size-14' => $place !== 1])>{{ $initials($row) }}</span>
                                    <span class="flex items-center gap-2 font-mono text-xs {{ explode(' ', $medal[$place])[0] }}">#{{ $place }} @include('partials.ranking-trend', ['row' => $row])</span>
                                    <span class="font-display font-semibold break-words text-white sm:text-lg">{{ $row['hero'] ?? $row['name'] }}</span>
                                    @if ($row['hero'])
                                        <span class="text-xs text-ink-muted">{{ $row['name'] }}</span>
                                    @endif
                                    <span class="font-mono text-sm text-primary-bright">{{ number_format($row['xp'], 0, ',', '.') }} {{ term('xp.short') }}</span>
                                    @if ($row['level'])
                                        <span class="hidden text-xs text-ink-muted sm:inline">{{ $row['level'] }}</span>
                                    @endif
                                </div>
                            @else
                                <div></div>
                            @endif
                        @endforeach
                    </div>

                    @if ($top->count() > 3)
                        <ol class="panel divide-y divide-outline">
                            @foreach ($top->slice(3) as $row)
                                <li class="flex items-center gap-3 px-4 py-3">
                                    <span class="w-7 font-mono text-sm text-ink-muted">#{{ $row['position'] }}</span>
                                    <span class="grid size-9 shrink-0 place-items-center rounded-full border border-outline bg-surface-high font-display text-sm text-white">{{ $initials($row) }}</span>
                                    <div class="flex min-w-0 flex-1 flex-col">
                                        <span class="truncate font-medium text-white">{{ $row['hero'] ?? $row['name'] }}</span>
                                        <span class="truncate text-xs text-ink-muted">
                                            {{ $row['hero'] ? $row['name'].' · ' : '' }}{{ $row['level'] }}@if ($row['badges']) · {{ $row['badges'] }} {{ $row['badges'] === 1 ? 'insignia' : 'insignias' }}@endif
                                        </span>
                                    </div>
                                    @include('partials.ranking-trend', ['row' => $row])
                                    <span class="w-24 text-end font-mono text-sm text-primary-bright">{{ number_format($row['xp'], 0, ',', '.') }} {{ term('xp.short') }}</span>
                                </li>
                            @endforeach
                        </ol>
                    @endif

                @endif
                <p class="text-center text-xs text-ink-muted">Solo aparecen quienes eligieron tener su perfil público.</p>
            </section>
        </main>

        <footer class="border-t border-outline">
            <div class="mx-auto flex max-w-6xl flex-col items-center justify-between gap-3 px-4 py-6 text-sm text-ink-muted sm:flex-row sm:px-8">
                <x-app-logo href="{{ route('landing') }}" />
                <span>Cursos de programación con árbol de habilidades.</span>
            </div>
        </footer>

        @fluxScripts
    </body>
</html>
