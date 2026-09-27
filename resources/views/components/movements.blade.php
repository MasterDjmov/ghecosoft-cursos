@props(['coins', 'xp', 'showAuthor' => false])

{{-- Libro de movimientos: monedas y XP. Es lo que explica cada saldo. --}}
<div {{ $attributes->class('grid gap-6 lg:grid-cols-2') }}>
    <section class="panel flex flex-col gap-3 p-5">
        <h3 class="font-display font-semibold text-white">Monedas</h3>
        <ul class="divide-y divide-outline text-sm">
            @forelse ($coins as $movement)
                <li class="flex items-start gap-3 py-2">
                    <span @class(['w-14 shrink-0 text-end font-mono font-semibold', 'text-success' => $movement->amount > 0, 'text-danger' => $movement->amount < 0])>
                        {{ $movement->amount > 0 ? '+' : '' }}{{ $movement->amount }}
                    </span>
                    <div class="flex min-w-0 flex-col">
                        <span class="text-ink">
                            {{ $movement->currency->is_wildcard ? term('coin.wildcard', null, abs($movement->amount)) : term('coin.course', $movement->currency->course, abs($movement->amount)) }}
                            · {{ $movement->reason->label() }}
                        </span>
                        <span class="text-xs text-ink-muted">
                            {{ $movement->created_at->format('d/m/Y H:i') }}
                            @if ($movement->currency->course) · {{ $movement->currency->course->title }} @endif
                            @if ($movement->note) · {{ $movement->note }} @endif
                            @if ($showAuthor && $movement->creator) · por {{ $movement->creator->name }} @endif
                        </span>
                    </div>
                </li>
            @empty
                <li class="py-2 text-ink-muted">Todavía no hay movimientos.</li>
            @endforelse
        </ul>
    </section>

    <section class="panel flex flex-col gap-3 p-5">
        <h3 class="font-display font-semibold text-white">{{ ucfirst(term('xp')) }}</h3>
        <ul class="divide-y divide-outline text-sm">
            @forelse ($xp as $movement)
                <li class="flex items-start gap-3 py-2">
                    <span @class(['w-14 shrink-0 text-end font-mono font-semibold', 'text-primary-bright' => $movement->amount > 0, 'text-danger' => $movement->amount < 0])>
                        {{ $movement->amount > 0 ? '+' : '' }}{{ $movement->amount }}
                    </span>
                    <div class="flex min-w-0 flex-col">
                        <span class="text-ink">{{ $movement->reason->label() }}</span>
                        <span class="text-xs text-ink-muted">
                            {{ $movement->created_at->format('d/m/Y H:i') }}
                            @if ($movement->note) · {{ $movement->note }} @endif
                            @if ($showAuthor && $movement->creator) · por {{ $movement->creator->name }} @endif
                        </span>
                    </div>
                </li>
            @empty
                <li class="py-2 text-ink-muted">Todavía no hay movimientos.</li>
            @endforelse
        </ul>
    </section>
</div>
