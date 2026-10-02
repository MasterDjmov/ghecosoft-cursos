<!DOCTYPE html>
<html lang="es" class="dark">
    <head>
        @include('partials.head', ['title' => $user->fullName().' · CV'])
        <meta name="robots" content="noindex">
        <meta name="description" content="Recorrido de {{ $user->fullName() }} en {{ config('app.name') }}: cursos, temas completados e insignias.">
    </head>
    <body class="min-h-screen">
        <main class="cv mx-auto flex w-full max-w-3xl flex-col gap-6 p-4 sm:p-8">
            @if ($preview)
                <div class="no-print panel border-warning/50 p-3 text-sm text-warning">
                    Vista previa: este CV es <strong>privado</strong>. Solo lo ven vos y el profe.
                    @if (auth()->id() === $user->id)
                        Para compartirlo, activalo en <a href="{{ route('privacy') }}" class="underline">Privacidad</a>.
                    @endif
                </div>
            @endif

            <header class="panel flex flex-col gap-4 p-6 sm:flex-row sm:items-center">
                <div class="grid size-20 shrink-0 place-items-center rounded-full border-2 border-primary-bright/50 bg-primary/10 font-display text-2xl font-bold text-primary-bright">{{ $user->initials() }}</div>
                <div class="flex min-w-0 flex-1 flex-col gap-1">
                    <p class="tech-label">Currículum · {{ config('app.name') }}</p>
                    <h1 class="font-display text-3xl font-semibold text-white">{{ $user->fullName() }}</h1>
                    @if ($user->hero_name)
                        <p class="flex items-center gap-1.5 text-sm text-secondary-bright" data-test="cv-hero"><flux:icon name="sparkles" variant="micro" /> Héroe: {{ $user->hero_name }}</p>
                    @endif
                    <p class="text-ink-muted">
                        {{ $level?->name() ?? ucfirst(term('level')).' 1' }} · {{ $user->xp_total }} {{ term('xp.short') }}
                        · {{ $approvedPractices }} {{ term('practice', null, $approvedPractices) }} aprobadas
                        · {{ $badges->count() }} {{ term('badge', null, $badges->count()) }}
                    </p>
                    @if ($chronicles['pages'] > 0 || $chronicles['pieces'] > 0)
                        <p class="flex items-center gap-1.5 text-sm text-warning" data-test="cv-chronicles">
                            <flux:icon name="book-open" variant="micro" /> Crónicas: {{ $chronicles['pages'] }} {{ $chronicles['pages'] === 1 ? 'página desbloqueada' : 'páginas desbloqueadas' }}
                            · {{ $chronicles['pieces'] }} de {{ $chronicles['totalPieces'] }} piezas del portal
                        </p>
                    @endif
                </div>
                <button type="button" onclick="window.print()" class="no-print inline-flex items-center gap-2 self-start rounded-lg bg-primary-bright px-4 py-2 text-sm font-medium text-surface hover:bg-primary">
                    <flux:icon name="arrow-down-tray" variant="mini" /> Descargar PDF
                </button>
            </header>

            <section class="flex flex-col gap-3">
                <h2 class="font-display text-lg font-semibold text-white">Cursos</h2>
                @forelse ($courses as $item)
                    @php($percent = $item['total'] ? intdiv($item['completedCount'] * 100, $item['total']) : 0)
                    {{-- Acordeón: cerrado de entrada (con muchos cursos el CV no se hace eterno); al imprimir se abre todo. --}}
                    <details class="cv-course panel group" data-test="cv-course">
                        <summary class="flex cursor-pointer list-none flex-col gap-3 p-5 [&::-webkit-details-marker]:hidden">
                            <div class="flex flex-wrap items-center gap-3">
                                <x-course-logo :course="$item['course']" size="size-12" />
                                <div class="flex min-w-0 flex-1 flex-col">
                                    <h3 class="font-medium text-white">{{ $item['course']->title }}</h3>
                                    <p class="text-xs text-ink-muted">
                                        @if ($item['since']) Desde {{ \Illuminate\Support\Carbon::parse($item['since'])->format('m/Y') }} · @endif
                                        {{ $item['completedCount'] }}/{{ $item['total'] }} {{ term('node', $item['course'], $item['total']) }}
                                    </p>
                                </div>
                                @if ($item['completion'])
                                    <span class="rounded border border-success/50 px-2 py-0.5 text-xs text-success">
                                        Completado el {{ $item['completion']->completed_at->format('d/m/Y') }} · {{ $item['completion']->days_taken }} días
                                    </span>
                                @else
                                    <span class="font-mono text-xs text-ink-muted">{{ $percent }}%</span>
                                @endif
                                <flux:icon name="chevron-down" variant="micro" class="no-print shrink-0 text-ink-muted transition group-open:rotate-180" />
                            </div>
                            <div class="h-1.5 overflow-hidden rounded-full bg-surface-highest"><div class="h-full bg-primary-bright" style="width: {{ $percent }}%"></div></div>
                        </summary>
                        <div class="flex flex-col gap-3 px-5 pb-5">
                            @if ($item['skills']->isNotEmpty())
                                <ul class="flex flex-wrap gap-1.5" aria-label="Temas completados">
                                    @foreach ($item['skills'] as $skill)
                                        <li class="rounded-md border border-outline bg-surface-high px-2 py-0.5 text-xs text-ink">{{ $skill }}</li>
                                    @endforeach
                                </ul>
                            @else
                                <p class="text-sm text-ink-muted">Recién empieza este curso.</p>
                            @endif
                            <a href="{{ route('cv.tree', [$user->cv_slug, $item['course']]) }}" data-test="cv-tree-link"
                                class="no-print inline-flex items-center gap-2 self-start rounded-lg border border-primary-bright/60 px-3 py-1.5 text-sm text-primary-bright transition hover:bg-primary/10">
                                <flux:icon name="share" variant="micro" /> Ver árbol
                            </a>
                        </div>
                    </details>
                @empty
                    <p class="panel p-5 text-ink-muted">Todavía no empezó ningún curso.</p>
                @endforelse
            </section>

            @if ($badges->isNotEmpty())
                <section class="flex flex-col gap-3">
                    <h2 class="font-display text-lg font-semibold text-white">{{ ucfirst(term('badge', null, 2)) }}</h2>
                    <ul class="grid gap-3 sm:grid-cols-2">
                        @foreach ($badges as $badge)
                            <li class="panel flex items-center gap-3 p-4">
                                @if ($badge->iconUrl())
                                    <img src="{{ $badge->iconUrl() }}" alt="" class="size-10 rounded-full object-cover">
                                @else
                                    <span class="grid size-10 place-items-center rounded-full bg-warning/15"><flux:icon name="trophy" class="size-5 text-warning" /></span>
                                @endif
                                <span class="flex flex-col">
                                    <span class="font-medium text-white">{{ $badge->name }}</span>
                                    <span class="text-xs text-ink-muted">{{ $badge->description }} · {{ \Illuminate\Support\Carbon::parse($badge->pivot->awarded_at)->format('d/m/Y') }}</span>
                                </span>
                            </li>
                        @endforeach
                    </ul>
                </section>
            @endif

            <footer class="border-t border-outline pt-4 text-xs text-ink-muted">
                Cada tema completado y cada {{ term('practice') }} aprobada fueron revisados por el docente. La {{ term('xp') }} mide constancia y avance, no notas.
                · {{ route('cv.show', $user->cv_slug) }}
            </footer>
        </main>
        <script>
            // Para imprimir (o guardar en PDF) se abren todos los cursos, y después vuelven como estaban.
            window.addEventListener('beforeprint', () => document.querySelectorAll('.cv-course').forEach((d) => {
                d.dataset.wasOpen = d.open ? '1' : '';
                d.open = true;
            }));
            window.addEventListener('afterprint', () => document.querySelectorAll('.cv-course').forEach((d) => (d.open = d.dataset.wasOpen === '1')));
        </script>
    </body>
</html>
