<div class="mx-auto flex w-full max-w-6xl flex-col gap-8 p-4 sm:p-8">
    <header class="flex flex-col gap-1">
        <p class="tech-label"><span class="live-dot me-2"></span>{{ term('world.name') }}</p>
        <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Hola, {{ auth()->user()->name }}</h1>
        <p class="text-ink-muted">{{ $mine->isEmpty() ? 'Elegí tu primer mundo y empezá a armar tu árbol.' : 'Seguí donde dejaste o descubrí un mundo nuevo.' }}</p>
    </header>

    <x-wallet-bar class="sm:hidden" />

    @unless (auth()->user()->hero_name)
        <flux:callout icon="sparkles" color="violet" data-test="hero-prompt">
            <flux:callout.heading>Elegí el nombre de tu héroe</flux:callout.heading>
            <flux:callout.text>
                Hasta que lo elijas, en la historia te llaman {{ term('hero.name') }}. Es único en toda la plataforma y aparece en el ranking.
                <flux:link :href="route('profile.edit')" wire:navigate>Elegirlo ahora</flux:link>
            </flux:callout.text>
        </flux:callout>
    @endunless

    @foreach ($expiring as $world)
        <flux:callout icon="clock" color="amber">
            <flux:callout.text>
                Tu abono de <strong>{{ $world['course']->title }}</strong> vence el {{ $world['subscription']->ends_at->format('d/m/Y') }}.
                <flux:link :href="route('student.course', $world['course'])" wire:navigate>Renovalo</flux:link> para no frenar.
            </flux:callout.text>
        </flux:callout>
    @endforeach

    @if ($mine->isNotEmpty())
        <section class="flex flex-col gap-4" data-test="my-courses">
            <h2 class="flex items-center gap-2 font-display text-xl font-semibold text-white">
                <flux:icon name="play-circle" class="size-6 text-primary-bright" /> Seguí donde dejaste
            </h2>
            <div class="grid gap-5 lg:grid-cols-2">
                @foreach ($mine as $world)
                    @php
                        $course = $world['course'];
                        $percent = $world['total'] > 0 ? intdiv($world['completed'] * 100, $world['total']) : 0;
                        [$badge, $badgeClass] = match ($world['status']) {
                            'active' => ['En curso', 'text-success border-success/40'],
                            'expired' => ['Abono vencido', 'text-warning border-warning/40'],
                            'ready' => ['Listo para abrir', 'text-primary-bright border-primary-bright/40'],
                            default => ['Solicitud pendiente', 'text-warning border-warning/40'],
                        };
                        [$action, $actionUrl, $primary] = match (true) {
                            $world['status'] === 'active' && $world['current'] !== null => ['Continuar', route('student.node', [$course, $world['current']]), true],
                            $world['status'] === 'active' => ['Ir al árbol', route('student.tree', $course), true],
                            $world['status'] === 'expired' => ['Renovar', route('student.course', $course), false],
                            $world['status'] === 'ready' => ['Abrir el curso', route('student.course', $course), true],
                            default => ['Ver solicitud', route('student.course', $course), false],
                        };
                    @endphp
                    <article @class(['panel flex flex-col gap-4 p-5', 'panel-active' => in_array($world['status'], ['active', 'ready'])]) data-test="world-{{ $course->slug }}">
                        <div class="flex items-start gap-4">
                            <x-course-logo :course="$course" />
                            <div class="flex min-w-0 flex-1 flex-col gap-1">
                                <div class="flex flex-wrap items-center justify-between gap-2">
                                    <h3 class="font-display text-lg font-semibold text-white">{{ $course->title }}</h3>
                                    <span class="rounded border px-2 py-0.5 font-mono text-[11px] {{ $badgeClass }}">{{ $badge }}</span>
                                </div>
                                @if ($world['current'])
                                    <p class="text-sm text-ink" data-test="current-node">
                                        <span class="text-ink-muted">Vas por:</span> {{ $world['current']->title }}
                                    </p>
                                @else
                                    <p class="text-sm text-ink-muted">{{ $course->short_description }}</p>
                                @endif
                            </div>
                        </div>

                        <div class="flex flex-col gap-2">
                            <div class="flex justify-between text-xs text-ink-muted">
                                <span>{{ $world['completed'] }}/{{ $world['total'] }} {{ term('node', $course, 2) }}</span>
                                <span class="font-mono">{{ $percent }}%</span>
                            </div>
                            <div class="h-1.5 overflow-hidden rounded-full bg-surface-highest">
                                <div class="h-full rounded-full bg-primary-bright" style="width: {{ $percent }}%"></div>
                            </div>
                        </div>

                        <div class="mt-auto flex flex-wrap items-center justify-between gap-3">
                            <span class="text-xs text-ink-muted">
                                @if ($world['subscription']) Abono hasta el {{ $world['subscription']->ends_at->format('d/m/Y') }} @endif
                            </span>
                            <div class="flex gap-2">
                                @if ($world['status'] === 'active' && $world['current'])
                                    <flux:button variant="ghost" size="sm" icon="share" :href="route('student.tree', $course)" wire:navigate>Árbol</flux:button>
                                @endif
                                <flux:button :variant="$primary ? 'primary' : 'filled'" size="sm" :icon:trailing="$primary ? 'arrow-right' : null" :href="$actionUrl" wire:navigate>{{ $action }}</flux:button>
                            </div>
                        </div>
                    </article>
                @endforeach
            </div>
        </section>
    @else
        <flux:callout icon="map" color="cyan" data-test="welcome">
            <flux:callout.heading>¡Bienvenido a {{ term('world.name') }}!</flux:callout.heading>
            <flux:callout.text>Todavía no estás en ningún mundo. Mirá los cursos, entrá al que te guste y pedí tu lugar.</flux:callout.text>
        </flux:callout>
    @endif

    <section class="flex flex-col gap-4" data-test="discover">
        <h2 class="flex items-center gap-2 font-display text-xl font-semibold text-white">
            <flux:icon name="globe-americas" class="size-6 text-secondary-bright" /> {{ $mine->isEmpty() ? 'Elegí tu mundo' : 'Descubrí más mundos' }}
        </h2>
        <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            @forelse ($discover as $world)
                <x-catalog-card :course="$world['course']" :nodes="$world['total']" wire:key="catalog-{{ $world['course']->id }}">
                    @if ($world['status'] === 'upcoming')
                        @if ($interested->has($world['course']->id))
                            <div class="flex w-full items-center justify-between gap-2 rounded-lg border border-success/40 px-3 py-1.5 text-sm text-success">
                                <span class="flex items-center gap-2"><flux:icon name="check" variant="micro" /> Te avisamos cuando salga</span>
                                <flux:button size="xs" variant="ghost" wire:click="toggleInterest({{ $world['course']->id }})" data-test="interest-{{ $world['course']->slug }}">No avisar</flux:button>
                            </div>
                        @else
                            <flux:button size="sm" variant="primary" icon="bell-alert" wire:click="toggleInterest({{ $world['course']->id }})" class="w-full" data-test="interest-{{ $world['course']->slug }}">Avisame cuando salga</flux:button>
                        @endif
                    @else
                        <flux:button size="sm" variant="primary" icon:trailing="arrow-right" :href="route('student.course', $world['course'])" wire:navigate class="w-full">Ver el curso</flux:button>
                    @endif
                </x-catalog-card>
            @empty
                <div class="panel p-8 text-center text-ink-muted sm:col-span-2 lg:col-span-3">
                    {{ $mine->isEmpty() ? 'Todavía no hay cursos publicados.' : 'Ya estás en todos los mundos. ¡Vienen más!' }}
                </div>
            @endforelse
        </div>
    </section>
</div>
