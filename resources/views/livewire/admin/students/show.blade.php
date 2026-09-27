<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header label="Alumnos" :title="$user->fullName()" :subtitle="'@'.$user->username.' · '.$user->email.($user->phone ? ' · '.$user->phone : '').($user->dni ? ' · DNI '.$user->dni : '')">
        <x-slot:actions>
            <flux:button variant="ghost" icon="arrow-left" :href="route('admin.students.index')" wire:navigate>Alumnos</flux:button>
        </x-slot:actions>
    </x-admin.page-header>

    <form wire:submit="saveHero" class="panel flex flex-col gap-3 p-4 sm:flex-row sm:items-end" data-test="hero-moderation">
        <div class="flex-1">
            <flux:input wire:model="heroName" label="Héroe" :placeholder="term('hero.name').' (sin elegir)'" maxlength="20"
                description="Público y único. Cambialo si el nombre no es apropiado; vacío = vuelve al héroe por defecto." />
        </div>
        <flux:button type="submit" icon="check">Guardar héroe</flux:button>
    </form>

    <div class="grid gap-4 sm:grid-cols-3">
        <div class="panel flex flex-col gap-1 p-4">
            <span class="tech-label">{{ ucfirst(term('xp')) }}</span>
            <span class="font-display text-2xl font-semibold text-white">{{ $user->xp_total }} <span class="text-sm text-ink-muted">{{ \App\Models\Level::forXp($user->xp_total)?->name() }}</span></span>
        </div>
        <div class="panel flex flex-col gap-2 p-4 sm:col-span-2">
            <span class="tech-label">Saldos</span>
            <div class="flex flex-wrap gap-2">
                @forelse ($balances as $currencyId => $amount)
                    @php($currency = $currencies->firstWhere('id', $currencyId))
                    <flux:badge>{{ $amount }} {{ $currency?->is_wildcard ? term('coin.wildcard', null, $amount) : term('coin.course', $currency?->course, $amount).' ('.$currency?->course?->title.')' }}</flux:badge>
                @empty
                    <span class="text-sm text-ink-muted">Sin saldo.</span>
                @endforelse
            </div>
        </div>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
        <section class="panel flex flex-col gap-3 p-5">
            <h2 class="font-display font-semibold text-white">Cursos y abonos</h2>
            <ul class="divide-y divide-outline text-sm">
                @forelse ($subscriptions as $subscription)
                    @php($active = $subscription->starts_at->isPast() && $subscription->ends_at->isFuture())
                    <li class="flex flex-wrap items-center gap-2 py-2">
                        <span class="text-ink">{{ $subscription->course->title }}</span>
                        <span class="text-ink-muted">{{ $subscription->starts_at->format('d/m/Y') }} → {{ $subscription->ends_at->format('d/m/Y') }}</span>
                        @if ($subscription->cohort) <span class="text-ink-muted">· {{ $subscription->cohort->name }}</span> @endif
                        <flux:badge size="sm" :color="$active ? 'green' : ($subscription->starts_at->isFuture() ? 'cyan' : 'zinc')">{{ $active ? 'Vigente' : ($subscription->starts_at->isFuture() ? 'Programado' : 'Vencido') }}</flux:badge>
                    </li>
                @empty
                    <li class="py-2 text-ink-muted">Sin abonos.</li>
                @endforelse
            </ul>
            @if ($badges->isNotEmpty())
                <div class="flex flex-wrap gap-2 border-t border-outline pt-3">
                    @foreach ($badges as $badge)
                        <flux:badge color="amber" icon="trophy">{{ $badge->name }}</flux:badge>
                    @endforeach
                </div>
            @endif
        </section>

        <form wire:submit="adjust" class="panel flex flex-col gap-4 p-5">
            <h2 class="font-display font-semibold text-white">Ajuste manual</h2>
            <div class="grid gap-4 sm:grid-cols-2">
                <flux:select wire:model="target" label="Qué">
                    <flux:select.option value="xp">{{ ucfirst(term('xp')) }} ({{ term('xp.short') }})</flux:select.option>
                    @foreach ($currencies as $currency)
                        <flux:select.option :value="(string) $currency->id">
                            {{ $currency->is_wildcard ? ucfirst(term('coin.wildcard', null, 2)) : ucfirst(term('coin.course', $currency->course, 2)).' · '.$currency->course?->title }}
                        </flux:select.option>
                    @endforeach
                </flux:select>
                <flux:input wire:model="amount" type="number" label="Monto" description:trailing="Negativo para quitar." />
            </div>
            <flux:input wire:model="reason" label="Motivo" placeholder="Participación destacada en clase" />
            <div class="flex justify-end">
                <flux:button type="submit" variant="primary">Registrar</flux:button>
            </div>
        </form>
    </div>

    <section class="panel flex flex-col gap-3 p-5">
        <h2 class="font-display font-semibold text-white">Últimas entregas</h2>
        <ul class="divide-y divide-outline text-sm">
            @forelse ($submissions as $submission)
                <li class="flex flex-wrap items-center gap-2 py-2">
                    <a href="{{ route('admin.submissions.show', $submission) }}" wire:navigate class="text-primary-bright hover:underline">{{ $submission->practice->title }}</a>
                    <span class="text-ink-muted">{{ $submission->practice->node->title }} · intento {{ $submission->attempt }} · {{ $submission->submitted_at->format('d/m/Y') }}</span>
                    <flux:badge size="sm" :color="['submitted' => 'amber', 'approved' => 'green', 'redo' => 'red'][$submission->status->value]">{{ $submission->status->label() }}</flux:badge>
                </li>
            @empty
                <li class="py-2 text-ink-muted">Sin entregas.</li>
            @endforelse
        </ul>
    </section>

    <x-movements :coins="$coinMovements" :xp="$xpMovements" show-author />
</div>
