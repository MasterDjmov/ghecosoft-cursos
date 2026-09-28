<div class="mx-auto flex w-full max-w-3xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-col gap-1">
        <p class="tech-label">{{ $course ? $course->title : term('world.name') }}</p>
        <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">{{ $course ? 'Top 10 del curso' : 'Ranking global' }}</h1>
        <p class="text-sm text-ink-muted">
            Ordenado por {{ term('xp') }}: la ganan las prácticas que aprueba el profe. Mide constancia y avance, no notas.
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
            @php($isMe = $row['user_id'] === auth()->id())
            <li @class(['flex items-center gap-4 px-4 py-3', 'bg-primary/10' => $isMe]) wire:key="rank-{{ $row['user_id'] }}">
                <span @class([
                    'grid size-9 shrink-0 place-items-center rounded-full font-display font-bold',
                    'bg-warning/20 text-warning' => $row['position'] === 1,
                    'bg-ink-muted/20 text-ink' => $row['position'] === 2,
                    'bg-[#b45309]/25 text-[#f59e0b]' => $row['position'] === 3,
                    'bg-surface-highest text-ink-muted' => $row['position'] > 3,
                ])>{{ $row['position'] }}</span>
                <span class="min-w-0 flex-1 truncate text-white">
                    @if (($row['cv_slug'] ?? null) && ! $course)
                        <a href="{{ route('cv.show', $row['cv_slug']) }}" class="hover:text-primary-bright" target="_blank">{{ $row['name'] }}</a>
                    @else
                        {{ $row['name'] }}
                    @endif
                    @if ($isMe) <span class="text-xs text-primary-bright">(vos)</span> @endif
                    @if ($row['hero'] ?? null)
                        <span class="block truncate text-xs text-secondary-bright"><flux:icon name="sparkles" variant="micro" class="inline" /> {{ $row['hero'] }}</span>
                    @endif
                </span>
                <span class="font-mono text-sm text-primary-bright">{{ $row['xp'] }} {{ term('xp.short') }}</span>
            </li>
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

    @if ($course)
        <p class="text-xs text-ink-muted">En el ranking del curso aparecés con tu nombre y la inicial del apellido, o con tu apodo si lo elegiste en
            <a href="{{ route('privacy') }}" wire:navigate class="text-primary-bright hover:underline">Privacidad</a>.</p>
    @endif
</div>
