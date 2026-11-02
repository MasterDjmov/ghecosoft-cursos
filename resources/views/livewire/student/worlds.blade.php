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
        <section class="flex flex-col gap-4" data-test="my-courses"
                 x-data="worldsCarousel({{ $mine->count() }}, {{ $startAt }})"
                 @keydown.left.prevent="prev()" @keydown.right.prevent="next()">
            <div class="flex items-center justify-between gap-3">
                <h2 class="flex items-center gap-2 font-display text-xl font-semibold text-white">
                    <flux:icon name="play-circle" class="size-6 text-primary-bright" /> Seguí donde dejaste
                </h2>
                @if ($mine->count() > 1)
                    <span class="tech-label" x-text="(active + 1) + ' / ' + count"></span>
                @endif
            </div>

            {{-- Todas las tarjetas en la misma celda de la grilla: el escenario toma el alto de la más alta. --}}
            <div class="relative -mx-4 overflow-hidden px-4 py-6 [perspective:1100px] sm:-mx-8 sm:px-8">
                <div x-ref="stage" class="grid touch-pan-y justify-items-center select-none [transform-style:preserve-3d]"
                     @pointerdown="pointerDown($event)" @pointermove="pointerMove($event)"
                     @pointerup="pointerUp()" @pointercancel="pointerUp()" @click.capture="swallowClick($event)">
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
                        <article wire:key="world-{{ $course->id }}"
                                 class="panel relative col-start-1 row-start-1 flex w-[min(20rem,calc(100vw-5rem))] flex-col gap-3 p-4 transition-[transform,opacity,box-shadow,border-color] duration-500 ease-[cubic-bezier(0.25,1,0.5,1)] will-change-transform motion-reduce:transition-none lg:w-[23rem] lg:p-5"
                                 :class="active === {{ $i }} ? 'panel-active shadow-[0_0_36px_-4px_rgb(6_182_212/0.45)]' : 'brightness-75'"
                                 :style="cardStyle({{ $i }})"
                                 data-test="world-{{ $course->slug }}">
                            {{-- Las de los costados no se usan: tocarlas las trae al medio. --}}
                            <button type="button" x-show="active !== {{ $i }}" x-cloak @click="go({{ $i }})"
                                    class="absolute inset-0 z-10 cursor-pointer rounded-lg" aria-label="Ver {{ $course->title }}"></button>

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
                </div>

                @if ($mine->count() > 1)
                    {{-- Flechas a los costados, solo en la compu (en el celular se arrastra). --}}
                    <button type="button" @click="prev()" :disabled="active === 0" aria-label="Mundo anterior"
                            class="absolute top-1/2 left-2 z-40 hidden size-11 -translate-y-1/2 items-center justify-center rounded-full border border-primary-bright/40 bg-surface-low/90 text-primary-bright shadow-[0_0_14px_-2px_rgb(6_182_212/0.4)] backdrop-blur transition hover:bg-primary-bright/15 disabled:opacity-30 lg:flex">
                        <flux:icon name="chevron-left" class="size-6" />
                    </button>
                    <button type="button" @click="next()" :disabled="active === count - 1" aria-label="Mundo siguiente"
                            class="absolute top-1/2 right-2 z-40 hidden size-11 -translate-y-1/2 items-center justify-center rounded-full border border-primary-bright/40 bg-surface-low/90 text-primary-bright shadow-[0_0_14px_-2px_rgb(6_182_212/0.4)] backdrop-blur transition hover:bg-primary-bright/15 disabled:opacity-30 lg:flex">
                        <flux:icon name="chevron-right" class="size-6" />
                    </button>
                @endif
            </div>

            @if ($mine->count() > 1)
                <div class="flex flex-col items-center gap-2">
                    <div class="flex items-center gap-2.5 rounded-full border border-outline bg-surface-low/80 px-4 py-2 backdrop-blur">
                        @foreach ($mine as $i => $world)
                            <button type="button" @click="go({{ $i }})" aria-label="Ir a {{ $world['course']->title }}" title="{{ $world['course']->title }}"
                                    class="h-2.5 rounded-full transition-all duration-300"
                                    :class="active === {{ $i }} ? 'w-6 bg-primary-bright shadow-[0_0_10px_rgb(6_182_212/0.8)]' : 'w-2.5 bg-outline hover:bg-ink-muted'"></button>
                        @endforeach
                    </div>
                    <p class="flex items-center gap-1.5 font-mono text-[11px] text-ink-muted">
                        <flux:icon name="arrows-right-left" variant="micro" class="text-primary-bright" />
                        <span class="lg:hidden">Deslizá o tocá un costado para cambiar de mundo</span>
                        <span class="hidden lg:inline">Arrastrá, usá las flechas o tocá un mundo del costado</span>
                    </p>
                </div>
            @endif
        </section>
    @else
        <flux:callout icon="map" color="cyan" data-test="welcome">
            <flux:callout.heading>¡Bienvenido a {{ term('world.name') }}!</flux:callout.heading>
            <flux:callout.text>Todavía no estás en ningún mundo. Mirá los cursos y <strong>probá gratis la clase 0</strong> del que te guste: leé, practicá y, si te convence, pedí tu lugar.</flux:callout.text>
        </flux:callout>
    @endif

    <section class="flex flex-col gap-4" data-test="discover">
        <h2 class="flex items-center gap-2 font-display text-xl font-semibold text-white">
            <flux:icon name="globe-americas" class="size-6 text-secondary-bright" /> {{ $mine->isEmpty() ? 'Elegí tu mundo' : 'Descubrí más mundos' }}
        </h2>
        <p class="-mt-2 text-sm text-ink-muted">La clase 0 de cada mundo se prueba gratis: pedís el abono cuando quieras que el profe te corrija y seguir.</p>
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
                        <div class="flex w-full gap-2">
                            @if ($world['trialRoot'] ?? null)
                                <flux:button size="sm" variant="primary" icon="play" :href="route('student.node', [$world['course'], $world['trialRoot']])" wire:navigate class="flex-1" data-test="try-{{ $world['course']->slug }}">Probar gratis</flux:button>
                            @endif
                            <flux:button size="sm" :variant="($world['trialRoot'] ?? null) ? 'filled' : 'primary'" icon:trailing="arrow-right" :href="route('student.course', $world['course'])" wire:navigate class="flex-1">Ver el curso</flux:button>
                        </div>
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
