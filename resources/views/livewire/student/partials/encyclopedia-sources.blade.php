{{-- Dónde se consigue (artefactos y monedas): se ve también en lo no descubierto, es la pista. --}}
@if ($entry['sources'] ?? [])
    <div class="flex flex-col gap-1.5 border-t border-outline/60 pt-3" data-test="entry-sources">
        <p class="text-xs tracking-wide text-ink-muted uppercase">{{ $entry['section'] === \App\Support\EncyclopediaItems::COINS ? 'Cómo se gana' : 'Dónde se consigue' }}</p>
        <ul class="flex flex-col gap-1 text-sm text-cyan-100">
            @foreach ($entry['sources'] as $source)
                <li class="flex items-start gap-1.5"><flux:icon name="map-pin" variant="micro" class="mt-0.5 shrink-0 text-cyan-300" /> {{ $source }}</li>
            @endforeach
        </ul>
    </div>
@elseif ($entry['section'] === \App\Support\EncyclopediaItems::ARTIFACTS)
    <p class="border-t border-outline/60 pt-3 text-sm text-ink-muted">Todavía no se sabe dónde se consigue.</p>
@endif
