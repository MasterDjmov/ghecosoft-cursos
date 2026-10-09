<div class="mx-auto flex w-full max-w-3xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-col gap-1">
        <p class="tech-label">{{ $course ? $course->title : term('world.name') }}</p>
        <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">{{ $course ? 'Top 10 del curso' : 'Ranking global' }}</h1>
        <p class="text-sm text-ink-muted">
            Ordenado por {{ term('xp') }}: la ganan las prácticas que aprueba el profe. Mide constancia y avance, no notas.
            Al lado de cada nombre, el {{ term('level') }} que da esa {{ term('xp.short') }}{{ $course ? ' en el curso' : '' }}.
        </p>
    </header>

    <nav class="flex flex-wrap gap-2" aria-label="Rankings">
        <flux:button size="sm" :variant="$course ? 'ghost' : 'primary'" :href="route('student.ranking')" wire:navigate>Global</flux:button>
        @foreach ($courses as $option)
            <flux:button size="sm" :variant="$course?->is($option) ? 'primary' : 'ghost'" :href="route('student.ranking.course', $option)" wire:navigate>{{ $option->title }}</flux:button>
        @endforeach
    </nav>

    <ol class="panel divide-y divide-outline overflow-hidden">
        @forelse ($top as $row)
            @include('partials.ranking-row', ['row' => $row, 'course' => $course])
        @empty
            <li class="p-8 text-center text-ink-muted">Todavía no hay nadie en el ranking.</li>
        @endforelse
    </ol>

    @if ($me && $me['position'] > \App\Services\Ranking::TOP)
        <p class="panel px-4 py-3 text-sm text-ink">Vas {{ $me['position'] }}.º con {{ $me['xp'] }} {{ term('xp.short') }}. ¡Seguí así!</p>
    @endif

    @if (! $course && auth()->user()->isStudent() && ! auth()->user()->hasPublicProfile())
        <flux:callout icon="eye-slash">
            <flux:callout.text>
                No figurás en el ranking global porque tu perfil no es público.
                {{ $publicBlocker ?? '' }}
                <flux:link :href="route('privacy')" wire:navigate>Privacidad</flux:link>
            </flux:callout.text>
        </flux:callout>
    @endif

    @if ($byCourse->isNotEmpty())
        <section class="flex flex-col gap-4" data-test="ranking-by-course">
            <h2 class="font-display text-xl font-semibold text-white">Por curso</h2>
            @foreach ($byCourse as $board)
                <div class="flex flex-col gap-2" wire:key="board-{{ $board['course']->id }}">
                    <div class="flex items-baseline justify-between gap-3">
                        <h3 class="font-medium text-white">{{ $board['course']->title }}</h3>
                        @if ($board['count'] > \App\Livewire\Student\RankingBoard::COURSE_TOP)
                            <a href="{{ route('student.ranking.course', $board['course']) }}" wire:navigate class="shrink-0 text-xs text-primary-bright hover:underline">Ver el top 10</a>
                        @endif
                    </div>
                    <ol class="panel divide-y divide-outline overflow-hidden">
                        @forelse ($board['top'] as $row)
                            @include('partials.ranking-row', ['row' => $row, 'course' => $board['course']])
                        @empty
                            <li class="px-4 py-4 text-center text-sm text-ink-muted">Todavía nadie ganó {{ term('xp.short', $board['course']) }} en este curso.</li>
                        @endforelse
                    </ol>
                    @if ($board['me'] && $board['me']['position'] > \App\Livewire\Student\RankingBoard::COURSE_TOP)
                        <p class="text-sm text-ink">Vas {{ $board['me']['position'] }}.º de {{ $board['count'] }} con {{ $board['me']['xp'] }} {{ term('xp.short', $board['course']) }}.</p>
                    @endif
                </div>
            @endforeach
            <p class="text-xs text-ink-muted">En el ranking de cada curso aparecés con tu nombre y la inicial del apellido, o con tu apodo si lo elegiste en
                <a href="{{ route('privacy') }}" wire:navigate class="text-primary-bright hover:underline">Privacidad</a>. Lo ven solo tus compañeros de ese curso.</p>
        </section>
    @endif

    @if ($course)
        <p class="text-xs text-ink-muted">En el ranking del curso aparecés con tu nombre y la inicial del apellido, o con tu apodo si lo elegiste en
            <a href="{{ route('privacy') }}" wire:navigate class="text-primary-bright hover:underline">Privacidad</a>.</p>
    @endif
</div>
