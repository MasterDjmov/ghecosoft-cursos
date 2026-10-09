{{-- Una fila del ranking: puesto, nombre (y héroe), nivel y XP. $row sale de App\Services\Ranking; $course, si es el de un curso. --}}
@php($isMe = $row['user_id'] === auth()->id())
<li @class(['flex items-center gap-3 px-4 py-3 sm:gap-4', 'bg-primary/10' => $isMe]) wire:key="rank-{{ $course?->id ?? 'g' }}-{{ $row['user_id'] }}">
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
    @if ($row['level'] ?? null)
        <span class="shrink-0 rounded-full border border-secondary/40 bg-secondary/10 px-2 py-0.5 font-mono text-xs text-secondary-bright" data-test="rank-level">{{ term('level.'.$row['level'], $course) }}</span>
    @endif
    <span class="w-20 shrink-0 text-right font-mono text-sm text-primary-bright">{{ $row['xp'] }} {{ term('xp.short', $course) }}</span>
</li>
