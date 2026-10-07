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
        <span class="panel flex items-center gap-2 py-1 ps-1 pe-3 text-sm" title="{{ $currency->isGold() ? 'Oro del jugador: atributos, tienda y monturas' : ($currency->course?->title ?? 'Sirve para extras de cualquier curso') }}" @if ($currency->isGold()) data-test="wallet-gold" @endif>
            <x-coin-icon :currency="$currency" />
            <span class="font-mono font-medium text-white">{{ $amount }}</span>
            <span class="text-ink-muted">{{ $currency->label($amount) }}</span>
        </span>
    @empty
        <span class="panel px-3 py-1.5 text-sm text-ink-muted">0 {{ term('coin.course', null, 2) }}</span>
    @endforelse

    <span class="panel flex items-center gap-1.5 px-3 py-1.5 text-sm">
        <span class="font-mono text-primary-bright">{{ $level?->name() ?? \Illuminate\Support\Str::ucfirst(term('level')).' 1' }}</span>
        <span class="text-ink-muted">·</span>
        <span class="font-mono text-white">{{ $user->xp_total }}</span>
        <span class="text-ink-muted">{{ term('xp.short') }}</span>
    </span>
</div>
