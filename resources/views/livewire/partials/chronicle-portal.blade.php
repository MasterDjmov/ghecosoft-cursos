{{-- El portal (Mis Crónicas, D80): una pieza del misterio por curso, que cuenta su líder al terminarlo. --}}
@php($found = collect($portal)->where('unlocked', true)->count())
<section class="flex flex-col gap-4" data-test="chronicle-portal">
    <p class="text-ink">El portal por el que llegaste guarda un secreto, {{ auth()->user()->name }}. Cada líder sabe una parte: terminá su curso y te la cuenta. <span class="font-mono text-sm text-warning">Pieza {{ $found }} de {{ count($portal) }}</span></p>
    <div class="flex gap-1" aria-hidden="true">
        @foreach ($portal as $piece)
            <span @class(['h-2 flex-1 rounded-full', 'bg-warning shadow-[0_0_10px_rgba(251,191,36,0.6)]' => $piece['unlocked'], 'bg-surface-highest' => ! $piece['unlocked']])></span>
        @endforeach
    </div>
    @foreach ($portal as $piece)
        @php($leader = $glossary->resolve('mentor.name', $piece['course']))
        @php($image = $leader['icon_path'] ? Storage::disk('public')->url($leader['icon_path']) : null)
        <article @class(['flex gap-4 p-5', 'panel border-warning/40' => $piece['unlocked'], 'rounded-lg border border-dashed border-outline bg-surface-lowest/60' => ! $piece['unlocked']])
            wire:key="piece-{{ $piece['course']->id }}" data-test="{{ $piece['unlocked'] ? 'portal-piece' : 'portal-locked' }}">
            <div class="relative size-14 shrink-0">
                @if ($image)
                    <img src="{{ $image }}" alt="" @class(['size-14 rounded-full object-cover', 'ring-2 ring-warning/60' => $piece['unlocked'], 'opacity-30 blur-[2px] grayscale' => ! $piece['unlocked']])>
                @else
                    <div class="size-14 rounded-full bg-surface-highest"></div>
                @endif
                @unless ($piece['unlocked'])
                    <flux:icon name="lock-closed" class="absolute inset-0 m-auto size-5 text-ink-muted" />
                @endunless
            </div>
            <div class="flex min-w-0 flex-col gap-1">
                <p class="tech-label">{{ \Illuminate\Support\Str::before($piece['course']->title, ':') }} · {{ $leader['singular'] }}</p>
                <h3 @class(['font-display text-lg font-semibold', 'text-white' => $piece['unlocked'], 'text-ink-muted' => ! $piece['unlocked']])>{{ $piece['title'] }}</h3>
                @if ($piece['unlocked'])
                    <div class="markdown text-ink italic">{!! $piece['html'] !!}</div>
                @else
                    <p class="text-sm text-ink-muted">{{ $piece['missing'] }}</p>
                @endif
            </div>
        </article>
    @endforeach
</section>
