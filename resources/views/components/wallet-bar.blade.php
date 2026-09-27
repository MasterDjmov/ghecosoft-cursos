{{-- Saldos del alumno: monedas por tipo + XP y nivel. --}}
@php
    $user = auth()->user();
    $balances = app(\App\Services\Ledger::class)->balances($user);
    $currencies = \App\Models\Currency::with('course')->whereIn('id', $balances->keys())->get()->keyBy('id');
    $level = \App\Models\Level::forXp($user->xp_total);
@endphp

<div {{ $attributes->merge(['class' => 'flex flex-wrap items-center gap-2']) }}>
    @forelse ($balances as $currencyId => $amount)
        @php($currency = $currencies[$currencyId])
        <span class="panel flex items-center gap-1.5 px-2.5 py-1 text-xs" title="{{ $currency->course?->title ?? 'Sirve para extras de cualquier curso' }}">
            <span @class([
                'grid size-5 place-items-center rounded-full font-mono text-[10px] font-bold',
                'bg-secondary/25 text-secondary-bright' => $currency->is_wildcard,
                'bg-primary/20 text-primary-bright' => ! $currency->is_wildcard,
            ])>{{ $currency->is_wildcard ? '★' : mb_strtoupper(mb_substr($currency->course?->title ?? '?', 0, 2)) }}</span>
            <span class="font-mono font-medium text-white">{{ $amount }}</span>
            <span class="text-ink-muted">{{ $currency->is_wildcard ? term('coin.wildcard', null, $amount) : term('coin.course', $currency->course, $amount) }}</span>
        </span>
    @empty
        <span class="text-xs text-ink-muted">Sin {{ term('coin.course', null, 2) }} todavía</span>
    @endforelse

    <span class="panel flex items-center gap-1.5 px-2.5 py-1 text-xs">
        <span class="font-mono text-primary-bright">{{ \Illuminate\Support\Str::ucfirst(term('level')) }} {{ $level?->number ?? 1 }}</span>
        <span class="text-ink-muted">·</span>
        <span class="font-mono text-white">{{ $user->xp_total }}</span>
        <span class="text-ink-muted">{{ term('xp.short') }}</span>
    </span>
</div>
