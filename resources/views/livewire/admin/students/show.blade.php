<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header label="Alumnos" :title="$user->fullName()" :subtitle="'@'.$user->username.($user->email ? ' · '.$user->email : ' · sin email').($user->phone ? ' · '.$user->phone : '').($user->dni ? ' · DNI '.$user->dni : '')">
        <x-slot:actions>
            <flux:button variant="ghost" icon="arrow-left" :href="route('admin.students.index')" wire:navigate>Alumnos</flux:button>
        </x-slot:actions>
    </x-admin.page-header>

    <div class="grid gap-4 lg:grid-cols-2">
        <form wire:submit="saveAccount" class="panel flex flex-col gap-4 p-4" data-test="account-form">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <h2 class="font-display font-semibold text-white">Cuenta y contacto</h2>
                <div class="flex flex-wrap gap-2">
                    @if ($user->whatsappUrl())
                        <flux:button size="sm" icon="chat-bubble-left-right" :href="$user->whatsappUrl()" target="_blank" rel="noopener">WhatsApp</flux:button>
                    @endif
                    <flux:modal.trigger name="confirm-reset">
                        <flux:button size="sm" icon="key">Resetear clave</flux:button>
                    </flux:modal.trigger>
                </div>
            </div>
            @if ($user->must_change_password)
                <p class="flex items-center gap-2 text-xs text-warning"><flux:icon name="clock" variant="micro" /> Todavía no cambió la clave provisoria.</p>
            @endif
            <flux:input wire:model="username" label="Usuario" size="sm" />
            <div class="grid gap-4 sm:grid-cols-2">
                <flux:input wire:model="email" type="email" label="Email" size="sm" placeholder="Sin email" />
                <flux:input wire:model="phone" type="tel" label="Teléfono" size="sm" placeholder="+54 9 380 412-3456" />
            </div>
            <div class="flex justify-end">
                <flux:button type="submit" size="sm" icon="check">Guardar cuenta</flux:button>
            </div>
        </form>

        <form wire:submit="saveHero" class="panel flex flex-col gap-3 p-4" data-test="hero-moderation">
            <h2 class="font-display font-semibold text-white">Héroe</h2>
            <flux:input wire:model="heroName" :placeholder="term('hero.name').' (sin elegir)'" maxlength="20" size="sm"
                description="Público y único. Cambialo si el nombre no es apropiado; vacío = vuelve al héroe por defecto." />
            <div class="flex justify-end">
                <flux:button type="submit" size="sm" icon="check">Guardar héroe</flux:button>
            </div>
        </form>
    </div>

    <flux:modal name="confirm-reset" class="max-w-md">
        <div class="flex flex-col gap-4">
            <flux:heading size="lg">¿Resetear la clave de {{ $user->name }}?</flux:heading>
            <flux:text>Se genera una clave provisoria nueva y la actual deja de andar. Al entrar, tiene que elegir una propia.</flux:text>
            <div class="flex justify-end gap-2">
                <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                <flux:button variant="danger" icon="key" wire:click="resetPassword" x-on:click="$flux.modal('confirm-reset').close()" data-test="reset-password-button">Resetear</flux:button>
            </div>
        </div>
    </flux:modal>

    <flux:modal name="credentials" class="max-w-lg">
        <div class="flex flex-col gap-4">
            <flux:heading size="lg">Clave nueva de {{ $user->name }}</flux:heading>
            @if ($credentials)
                @include('livewire.admin.students.partials.credentials', ['credentials' => $credentials])
            @endif
        </div>
    </flux:modal>

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
            @if ($courseCohorts->isNotEmpty())
                <div class="flex flex-col gap-3 border-t border-outline pt-3">
                    <span class="tech-label">Comisión</span>
                    @foreach ($courseCohorts as $subscription)
                        <flux:select size="sm" :label="$subscription->course->title" wire:key="cohort-course-{{ $subscription->course_id }}"
                            x-on:change="$wire.changeCohort({{ $subscription->course_id }}, $event.target.value)">
                            <flux:select.option value="" :selected="! $subscription->cohort_id">Sin comisión</flux:select.option>
                            @foreach ($subscription->course->cohorts->sortBy('name') as $cohort)
                                <flux:select.option :value="(string) $cohort->id" :selected="$subscription->cohort_id === $cohort->id">{{ $cohort->name }}{{ $cohort->is_open_for_enrollment ? '' : ' (cerrada)' }}</flux:select.option>
                            @endforeach
                        </flux:select>
                    @endforeach
                </div>
            @endif
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

    <section @class(['panel flex flex-col gap-3 p-5', 'border-warning/60' => $user->blocked_at]) data-test="account-security">
        <div class="flex flex-wrap items-center justify-between gap-2">
            <h2 class="font-display font-semibold text-white">Seguridad de la cuenta</h2>
            @if ($user->blocked_at)
                <flux:button size="sm" variant="primary" icon="lock-open" wire:click="unblock" data-test="unblock">Reactivar</flux:button>
            @else
                <flux:button size="sm" variant="danger" icon="lock-closed" wire:click="block" wire:confirm="¿Pausar la cuenta de {{ $user->name }}? Se cierran sus sesiones y no puede entrar hasta que la reactives." data-test="block">Pausar cuenta</flux:button>
            @endif
        </div>
        @if ($user->blocked_at)
            <p class="flex items-center gap-2 text-sm text-warning"><flux:icon name="lock-closed" variant="micro" /> Pausada desde el {{ $user->blocked_at->format('d/m/Y H:i') }}. Para devolverle el acceso: Reactivar y, si hace falta, Resetear clave.</p>
        @endif
        <p class="text-sm text-ink-muted">
            La cuenta solo puede estar abierta en un lugar a la vez: si entra desde otro, se cierra la sesión anterior.
            Si pasa {{ \App\Services\SingleSession::EVICTIONS_TO_WARN }} veces en 24 horas te llega un aviso.
        </p>
        <ul class="divide-y divide-outline text-sm">
            @forelse ($evictions as $eviction)
                <li class="flex flex-wrap items-center gap-2 py-2">
                    <span class="font-mono text-xs text-ink">{{ \Illuminate\Support\Carbon::parse($eviction->created_at)->format('d/m/Y H:i') }}</span>
                    <span class="text-ink-muted">sesión cerrada en {{ $eviction->ip ?? 'IP desconocida' }}</span>
                    <span class="truncate text-xs text-ink-muted">{{ \Illuminate\Support\Str::limit($eviction->user_agent, 80) }}</span>
                </li>
            @empty
                <li class="py-2 text-ink-muted">En los últimos 30 días no hubo sesiones cerradas por entrar desde otro lugar.</li>
            @endforelse
        </ul>
    </section>

    <section class="panel flex flex-col gap-3 p-5" data-test="student-messages">
        <div class="flex items-center justify-between gap-2">
            <h2 class="font-display font-semibold text-white">Consultas</h2>
            @if ($messageThreads->isNotEmpty())
                <a href="{{ route('admin.messages', ['alumno' => $user->id]) }}" wire:navigate class="text-sm text-primary-bright hover:underline">Ver todas en Mensajes</a>
            @endif
        </div>
        <ul class="divide-y divide-outline text-sm">
            @forelse ($messageThreads as $row)
                <li class="flex flex-wrap items-center gap-2 py-2">
                    <a href="{{ route('admin.messages', ['hilo' => $row->practice_id.'-'.$user->id]) }}" wire:navigate class="text-primary-bright hover:underline">{{ $row->practice?->title }}</a>
                    <span class="text-ink-muted">{{ $row->practice?->node->title }} · {{ $row->total }} {{ $row->total == 1 ? 'mensaje' : 'mensajes' }}</span>
                    @if ($row->unread)
                        <flux:badge size="sm" color="red">{{ $row->unread }} sin leer</flux:badge>
                    @endif
                </li>
            @empty
                <li class="py-2 text-ink-muted">No mandó consultas.</li>
            @endforelse
        </ul>
    </section>

    <livewire:movement-feed :user="$user" show-author />
</div>
