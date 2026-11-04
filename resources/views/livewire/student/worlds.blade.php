<div class="mx-auto flex w-full max-w-6xl flex-col gap-8 p-4 sm:p-8">
    <header class="flex flex-col gap-1">
        <p class="tech-label"><span class="live-dot me-2"></span>{{ term('world.name') }}</p>
        <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Hola, {{ auth()->user()->name }}</h1>
        <p class="text-ink-muted">{{ $mine->isEmpty() ? 'Elegí tu primer mundo y empezá a armar tu árbol.' : 'Seguí donde dejaste o descubrí un mundo nuevo.' }}</p>
    </header>

    <x-wallet-bar class="sm:hidden" />

    @if ($closedCourse = session('maintenance_course'))
        {{-- Quiso entrar a un curso en mantenimiento (D86). --}}
        <flux:callout icon="wrench-screwdriver" color="amber" data-test="course-maintenance-notice">
            <flux:callout.heading>{{ $closedCourse }} está en mantenimiento</flux:callout.heading>
            <flux:callout.text>{{ \App\Support\Maintenance::DEFAULT_COURSE_MESSAGE }}</flux:callout.text>
        </flux:callout>
    @endif

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
                Tu abono de <strong>{{ $world['course']->title }}</strong> vence el {{ $world['paidUntil']->format('d/m/Y') }}.
                <flux:link :href="route('student.course', $world['course'])" wire:navigate>Renovalo</flux:link> para no frenar.
            </flux:callout.text>
        </flux:callout>
    @endforeach

    @if ($mine->isNotEmpty())
        <x-carousel-3d :titles="$mine->map(fn ($w) => $w['course']->title)->all()" data-test="my-courses">
            <x-slot:heading>
                <h2 class="flex items-center gap-2 font-display text-xl font-semibold text-white">
                    <flux:icon name="play-circle" class="size-6 text-primary-bright" /> Seguí donde dejaste
                </h2>
    </x-slot:heading>
            @foreach ($mine as $i => $world)
                @php
                    $course = $world['course'];
                    $percent = $world['total'] > 0 ? intdiv($world['completed'] * 100, $world['total']) : 0;
                    $closed = ! \App\Support\Maintenance::letsIntoCourse(auth()->user(), $course);
                    [$badge, $badgeClass] = $closed ? ['En mantenimiento', 'text-warning border-warning/40 bg-warning/10'] : match ($world['status']) {
                        'active' => ['En curso', 'text-success border-success/40 bg-success/10'],
                        'expired' => ['Abono vencido', 'text-warning border-warning/40 bg-warning/10'],
                        'ready' => ['Listo para abrir', 'text-primary-bright border-primary-bright/40 bg-primary-bright/10'],
                        default => ['Solicitud pendiente', 'text-warning border-warning/40 bg-warning/10'],
                    };
                    [$action, $actionUrl, $primary] = match (true) {
                        $world['status'] === 'active' && $world['current'] !== null => ['Continuar', route('student.node', [$course, $world['current']]), true],
                        $world['status'] === 'active' => ['Ir al árbol', route('student.tree', $course), true],
                        $world['status'] === 'expired' => ['Renovar', route('student.course', $course), false],
                        $world['status'] === 'ready' => ['Abrir el curso', route('student.course', $course), true],
                        default => ['Ver solicitud', route('student.course', $course), false],
                    };
                @endphp
                <article wire:key="world-{{ $course->id }}" class="panel carousel-card flex flex-col gap-3 p-4 lg:p-5"
                         :class="cardClass({{ $i }})" :style="cardStyle({{ $i }})" data-test="world-{{ $course->slug }}">
                    <x-carousel-3d.pick :index="$i" :label="$course->title" />

                    <div class="flex items-center justify-between gap-2">
                        <span class="rounded border px-2 py-0.5 font-mono text-[11px] tracking-wide uppercase {{ $badgeClass }}">{{ $badge }}</span>
                        <span class="text-xs text-ink-muted">
                            @if ($world['paidUntil'])
                                <x-subscription-countdown :until="$world['paidUntil']" :total="$course->subscription_days" compact />
                            @endif
                        </span>
                    </div>

                    <div class="flex items-center gap-3">
                        <x-course-logo :course="$course" size="size-14" />
                        <div class="flex min-w-0 flex-col gap-0.5">
                            <h3 class="font-display text-base leading-tight font-semibold text-white lg:text-lg">{{ $course->title }}</h3>
                            @if ($world['current'])
                                <p class="truncate font-mono text-xs text-primary-bright" data-test="current-node">
                                    <span class="text-ink-muted">Vas por:</span> {{ $world['current']->title }}
                                </p>
                            @endif
                        </div>
                    </div>

                    <div class="relative aspect-[4/3] overflow-hidden rounded-lg border border-outline bg-surface-lowest">
                        @if ($world['protagonist'])
                            <img src="{{ $world['protagonist']['image'] }}" alt="{{ $world['protagonist']['name'] }}" class="size-full object-cover object-center" loading="lazy" draggable="false">
                            <div class="absolute inset-0 bg-gradient-to-t from-surface-lowest via-transparent to-transparent"></div>
                            <div class="absolute inset-x-2 bottom-2 flex items-center justify-between gap-2 rounded-md border border-primary-bright/30 bg-surface-lowest/85 px-2.5 py-1.5 backdrop-blur">
                                <span class="truncate text-xs text-ink"><strong class="text-white">{{ $world['protagonist']['name'] }}</strong> · {{ $world['protagonist']['title'] }}</span>
                                <span class="font-mono text-xs font-bold text-secondary-bright">{{ $percent }}%</span>
                            </div>
                        @else
                            <div class="flex size-full flex-col items-center justify-center gap-3 p-4 text-center">
                                <x-course-logo :course="$course" size="size-24" />
                                <p class="line-clamp-3 text-sm text-ink-muted">{{ $course->short_description }}</p>
                            </div>
                        @endif
                    </div>

                    <div class="flex flex-col gap-1.5">
                        <div class="flex justify-between text-xs text-ink-muted">
                            <span>{{ $world['completed'] }}/{{ $world['total'] }} {{ term('node', $course, 2) }}</span>
                            <span class="font-mono text-primary-bright">{{ $percent }}%</span>
                        </div>
                        <div class="h-2 overflow-hidden rounded-full border border-outline bg-surface-highest/60 p-px">
                            <div class="h-full rounded-full bg-gradient-to-r from-primary-bright to-secondary-bright" style="width: {{ max($percent, 2) }}%"></div>
                        </div>
                    </div>

                    <div class="mt-auto flex flex-wrap justify-end gap-2">
                        @if ($closed)
                            <span class="flex items-center gap-1.5 text-xs text-warning" data-test="course-closed"><flux:icon name="wrench-screwdriver" variant="micro" /> Volvé en un rato</span>
                        @else
                            @if ($world['status'] === 'active' && $world['current'])
                                <flux:button variant="ghost" size="sm" icon="share" :href="route('student.tree', $course)" wire:navigate>Árbol</flux:button>
                            @endif
                            @if ($world['trialRoot'] ?? null)
                                <flux:button variant="ghost" size="sm" icon="play" :href="route('student.node', [$course, $world['trialRoot']])" wire:navigate>Probar la clase 0</flux:button>
                            @endif
                            <flux:button :variant="$primary ? 'primary' : 'filled'" size="sm" :icon:trailing="$primary ? 'arrow-right' : null" :href="$actionUrl" wire:navigate class="flex-1">{{ $action }}</flux:button>
                        @endif
                    </div>
                </article>
            @endforeach
        </x-carousel-3d>
    @else
        <flux:callout icon="map" color="cyan" data-test="welcome">
            <flux:callout.heading>¡Bienvenido a {{ term('world.name') }}!</flux:callout.heading>
            <flux:callout.text>Todavía no estás en ningún mundo. Mirá los cursos y <strong>probá gratis la clase 0</strong> del que te guste: leé, practicá y, si te convence, pedí tu lugar.</flux:callout.text>
        </flux:callout>
    @endif

    @php($discoverHeading = $mine->isEmpty() ? 'Elegí tu mundo' : 'Descubrí más mundos')
    @if ($discover->isEmpty())
        <section class="flex flex-col gap-4" data-test="discover">
            <h2 class="flex items-center gap-2 font-display text-xl font-semibold text-white">
                <flux:icon name="globe-americas" class="size-6 text-secondary-bright" /> {{ $discoverHeading }}
            </h2>
            <div class="panel p-8 text-center text-ink-muted">
                {{ $mine->isEmpty() ? 'Todavía no hay cursos publicados.' : 'Ya estás en todos los mundos. ¡Vienen más!' }}
            </div>
        </section>
    @else
        <x-carousel-3d :titles="$discover->map(fn ($w) => $w['course']->title)->all()" data-test="discover">
            <x-slot:heading>
                <h2 class="flex items-center gap-2 font-display text-xl font-semibold text-white">
                    <flux:icon name="globe-americas" class="size-6 text-secondary-bright" /> {{ $discoverHeading }}
                </h2>
            </x-slot:heading>
            <x-slot:intro>
                <p class="-mt-2 text-sm text-ink-muted">La clase 0 de cada mundo se prueba gratis: pedís el abono cuando quieras que el profe te corrija y seguir.</p>
            </x-slot:intro>
            @foreach ($discover as $i => $world)
                <x-catalog-card :course="$world['course']" :nodes="$world['total']" wire:key="catalog-{{ $world['course']->id }}"
                                class="carousel-card" x-bind:class="cardClass({{ $i }})" x-bind:style="cardStyle({{ $i }})">
                    <x-carousel-3d.pick :index="$i" :label="$world['course']->title" />
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
                        <div class="flex w-full gap-2">
                            @if ($world['trialRoot'] ?? null)
                                <flux:button size="sm" variant="primary" icon="play" :href="route('student.node', [$world['course'], $world['trialRoot']])" wire:navigate class="flex-1" data-test="try-{{ $world['course']->slug }}">Probar gratis</flux:button>
                            @endif
                            <flux:button size="sm" :variant="($world['trialRoot'] ?? null) ? 'filled' : 'primary'" icon:trailing="arrow-right" :href="route('student.course', $world['course'])" wire:navigate class="flex-1">Ver el curso</flux:button>
                        </div>
                    @endif
                </x-catalog-card>
            @endforeach
        </x-carousel-3d>
    @endif
</div>
