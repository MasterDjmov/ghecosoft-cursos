<div class="mx-auto flex w-full max-w-6xl flex-col gap-8 p-4 sm:p-8">
    <header class="flex flex-col gap-1">
        <p class="tech-label"><span class="live-dot me-2"></span>{{ term('world.name') }}</p>
        <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Hola, {{ auth()->user()->name }}</h1>
        <p class="text-ink-muted">Elegí un mundo y seguí avanzando por su árbol.</p>
    </header>

    <x-wallet-bar class="sm:hidden" />

    @foreach ($worlds->filter(fn ($w) => $w['status'] === 'active' && $w['subscription']->ends_at->lte(now()->addDays(config('game.subscription_warning_days')))) as $world)
        <flux:callout icon="clock" color="amber">
            <flux:callout.text>
                Tu abono de <strong>{{ $world['course']->title }}</strong> vence el {{ $world['subscription']->ends_at->format('d/m/Y') }}.
                <flux:link :href="route('student.course', $world['course'])" wire:navigate>Renovalo</flux:link> para no frenar.
            </flux:callout.text>
        </flux:callout>
    @endforeach

    <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        @forelse ($worlds as $world)
            @php
                $course = $world['course'];
                $percent = $world['total'] > 0 ? intdiv($world['completed'] * 100, $world['total']) : 0;
                [$badge, $badgeClass] = match ($world['status']) {
                    'active' => ['En curso', 'text-success border-success/40'],
                    'expired' => ['Abono vencido', 'text-warning border-warning/40'],
                    'ready' => ['Listo para abrir', 'text-primary-bright border-primary-bright/40'],
                    'pending' => ['Solicitud pendiente', 'text-warning border-warning/40'],
                    default => ['Bloqueado', 'text-ink-muted border-outline'],
                };
            @endphp

            <article @class(['panel flex flex-col gap-4 p-5', 'panel-active' => in_array($world['status'], ['active', 'ready'])]) data-test="world-{{ $course->slug }}">
                <div class="flex items-start justify-between gap-3">
                    <x-course-logo :course="$course" />
                    <span class="rounded border px-2 py-0.5 font-mono text-[11px] {{ $badgeClass }}">{{ $badge }}</span>
                </div>

                <div class="flex flex-col gap-1">
                    <h2 class="font-display text-lg font-semibold text-white">{{ $course->title }}</h2>
                    <p class="text-sm text-ink-muted">{{ $course->short_description }}</p>
                </div>

                <div class="mt-auto flex flex-col gap-2">
                    <div class="flex justify-between text-xs text-ink-muted">
                        <span>{{ $world['completed'] }}/{{ $world['total'] }} {{ term('node', $course, 2) }}</span>
                        <span class="font-mono">{{ $percent }}%</span>
                    </div>
                    <div class="h-1.5 overflow-hidden rounded-full bg-surface-highest">
                        <div class="h-full rounded-full bg-primary-bright" style="width: {{ $percent }}%"></div>
                    </div>
                    @if ($world['subscription'])
                        <p class="text-xs text-ink-muted">Abono hasta el {{ $world['subscription']->ends_at->format('d/m/Y') }}</p>
                    @endif
                </div>

                @php
                    [$action, $actionUrl, $primary] = match ($world['status']) {
                        'active' => ['Entrar', route('student.tree', $course), true],
                        'expired' => ['Renovar', route('student.course', $course), false],
                        'ready' => ['Abrir el curso', route('student.course', $course), true],
                        default => ['Ver curso', route('student.course', $course), false],
                    };
                @endphp
                <flux:button :variant="$primary ? 'primary' : 'filled'" :href="$actionUrl" wire:navigate class="w-full">{{ $action }}</flux:button>
            </article>
        @empty
            <div class="panel p-8 text-center text-ink-muted sm:col-span-2 lg:col-span-3">
                Todavía no hay cursos publicados.
            </div>
        @endforelse
    </div>
</div>
