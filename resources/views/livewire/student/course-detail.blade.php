@php
    $coin = fn (int $n) => term('coin.course', $course, $n);
    // Los días cuentan hasta el final de lo pagado (con la renovación ya aprobada, si la hay).
    $daysLeft = $paidUntil ? (int) ceil(now()->diffInDays($paidUntil, false)) : null;
    // Se puede pedir: sin solicitud pendiente y sin abono, o con el abono vencido o por vencer (7 días).
    $canRequest = ! $pending && (! $subscription || $daysLeft <= 7);
    $isRenewal = $kind === \App\Enums\RequestKind::Renewal;
@endphp

<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <flux:button variant="ghost" size="sm" icon="arrow-left" :href="route('student.worlds')" wire:navigate class="self-start">Mundos</flux:button>

    <header class="panel flex flex-col gap-5 p-5 sm:flex-row sm:items-center sm:p-6">
        <x-course-logo :course="$course" size="size-24" />
        <div class="flex min-w-0 flex-1 flex-col gap-1">
            <p class="tech-label">{{ $course->language->label() }} · {{ $nodeCount }} {{ term('node', $course, $nodeCount) }}</p>
            <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">{{ $course->title }}</h1>
            @if ($course->short_description)
                <p class="text-ink-muted">{{ $course->short_description }}</p>
            @endif
        </div>
    </header>

    {{-- Estado del alumno en este curso --}}
    <section class="panel panel-active flex flex-col gap-4 p-5 sm:p-6" data-test="course-status">
        @if ($rootOpen && $subscription)
            <div class="flex flex-col gap-1">
                <x-subscription-countdown :until="$paidUntil" :total="$course->subscription_days" class="mb-2 self-start" />
                <p class="tech-label"><span class="live-dot me-2"></span>Estás cursando</p>
                <p class="text-ink">Tu abono vence el <strong class="text-white">{{ $paidUntil->format('d/m/Y') }}</strong> ({{ $daysLeft }} {{ $daysLeft === 1 ? 'día' : 'días' }}).</p>
            </div>
            <div class="flex flex-wrap gap-2">
                <flux:button variant="primary" icon="share" :href="route('student.tree', $course)" wire:navigate>Ir al árbol</flux:button>
            </div>
        @elseif ($rootOpen)
            <div class="flex flex-col gap-1">
                <p class="tech-label text-warning!">Abono vencido</p>
                <p class="text-ink">Tu abono venció el {{ $lastSubscription?->ends_at->format('d/m/Y') }}. Podés repasar todo lo que abriste, pero para abrir {{ term('node', $course, 2) }} nuevos y entregar tenés que renovarlo.</p>
            </div>
            <div class="flex flex-wrap gap-2">
                <flux:button icon="share" :href="route('student.tree', $course)" wire:navigate>Repasar el árbol</flux:button>
            </div>
        @elseif ($subscription)
            <div class="flex flex-col gap-1">
                <p class="tech-label"><span class="live-dot me-2"></span>Inscripción aprobada</p>
                <p class="text-ink">
                    Tenés <strong class="text-white">{{ $balance }} {{ $coin($balance) }}</strong>.
                    Abrir la {{ $course->rootNode?->title ?? 'clase 0' }} cuesta {{ $course->root_price }} {{ $coin($course->root_price) }}.
                </p>
            </div>
            <div class="flex flex-wrap gap-2">
                <flux:button variant="primary" icon="lock-open" wire:click="openCourse" :disabled="! $canOpen">Abrir el curso</flux:button>
            </div>
        @elseif ($pending)
            <div class="flex flex-col gap-1">
                <p class="tech-label text-warning!">Solicitud pendiente</p>
                <p class="text-ink">
                    Mandaste tu {{ $pending->kind === \App\Enums\RequestKind::Renewal ? 'pedido de renovación' : 'solicitud de inscripción' }}
                    el {{ $pending->created_at->format('d/m/Y') }}. Cuando el profe la apruebe, vas a poder {{ $pending->kind === \App\Enums\RequestKind::Renewal ? 'seguir avanzando' : 'abrir el curso' }}.
                </p>
            </div>
        @else
            <div class="flex flex-col gap-1">
                <p class="tech-label">¿Cómo empiezo?</p>
                <ol class="list-decimal space-y-1 ps-5 text-ink">
                    <li>Coordinás con el profe una clase inicial y le mandás el comprobante de pago (o le escribís por WhatsApp).</li>
                    <li>Cuando lo aprueba, recibís <strong class="text-white">{{ $course->root_price }} {{ $coin($course->root_price) }}</strong> y {{ $course->subscription_days }} días de abono.</li>
                    <li>Con esas {{ $coin(2) }} abrís la clase 0 y arranca tu árbol.</li>
                </ol>
            </div>
        @endif

        {{-- Clase 0 de prueba (D71): sin abono de este curso, se entra gratis a leer y practicar. --}}
        @if ($canTry)
            <div class="flex flex-col gap-3 rounded-lg border border-secondary/40 bg-secondary/10 p-4" data-test="trial-offer">
                <div class="flex flex-col gap-1">
                    <p class="flex items-center gap-2 font-medium text-white"><flux:icon name="sparkles" variant="micro" class="text-secondary-bright" /> Probalo gratis antes de pagar</p>
                    <p class="text-sm text-ink">
                        Entrá a la <strong class="text-white">{{ $course->rootNode->title }}</strong>: leé la clase, mirá el ejemplo y practicá sin pagar.
                        Para que el profe te corrija y seguir con el resto, pedís el abono; el mes empieza a correr recién cuando se aprueba.
                    </p>
                </div>
                <div class="flex flex-wrap gap-2">
                    <flux:button variant="primary" icon="play" :href="route('student.node', [$course, $course->rootNode])" wire:navigate>Probar la clase 0 gratis</flux:button>
                    <flux:button variant="ghost" icon="share" :href="route('student.tree', $course)" wire:navigate>Ver el árbol</flux:button>
                </div>
            </div>
        @endif

        @if ($pending && $subscription)
            <flux:callout icon="clock" color="amber">
                <flux:callout.text>Tu pedido de renovación está pendiente de aprobación.</flux:callout.text>
            </flux:callout>
        @endif

        @if ($canRequest)
            <div class="flex flex-col gap-3 border-t border-outline pt-4">
                @if ($subscription && $isRenewal)
                    <flux:text>Tu abono vence pronto: podés pedir la renovación desde ahora. Los días nuevos se suman al final.</flux:text>
                @endif
                <div class="flex flex-wrap gap-2">
                    <flux:modal.trigger name="request">
                        <flux:button :variant="$subscription || $rootOpen ? 'primary' : 'primary'" icon="document-arrow-up">
                            {{ $isRenewal ? 'Renovar abono' : 'Solicitar inscripción' }}
                        </flux:button>
                    </flux:modal.trigger>
                    @if ($whatsappAvailable)
                        <flux:button icon="chat-bubble-left-right" wire:click="contact">Contactar al profe</flux:button>
                    @endif
                </div>
            </div>
        @endif
    </section>

    @if ($intro)
        <x-story-card :story="$intro" :course="$course" :scene="$scene" icon="book-open" data-test="course-intro" />
    @endif

    @if ($descriptionHtml)
        <section class="panel flex flex-col gap-3 p-5 sm:p-6">
            <h2 class="font-display text-lg font-semibold text-white">De qué se trata</h2>
            <div class="markdown">{!! $descriptionHtml !!}</div>
        </section>
    @endif

    @if ($history->isNotEmpty())
        <section class="panel flex flex-col gap-3 p-5 sm:p-6">
            <h2 class="font-display text-lg font-semibold text-white">Tus solicitudes</h2>
            <ul class="divide-y divide-outline text-sm">
                @foreach ($history as $item)
                    <li class="flex flex-col gap-1 py-2">
                        <div class="flex flex-wrap items-center gap-2">
                            <span class="text-ink">{{ $item->kind->label() }} · {{ $item->created_at->format('d/m/Y') }}</span>
                            <flux:badge size="sm" :color="$item->status === \App\Enums\RequestStatus::Approved ? 'green' : 'red'">{{ $item->status->label() }}</flux:badge>
                        </div>
                        @if ($item->admin_note)
                            <p class="text-ink-muted">Nota del profe: {{ $item->admin_note }}</p>
                        @endif
                    </li>
                @endforeach
            </ul>
        </section>
    @endif

    <flux:modal name="request" class="w-full max-w-lg">
        <form wire:submit="sendReceipt" class="flex flex-col gap-5">
            <div class="flex flex-col gap-1">
                <flux:heading size="lg">{{ $isRenewal ? 'Renovar abono' : 'Solicitar inscripción' }} · {{ $course->title }}</flux:heading>
                <flux:text>Subí el comprobante del pago (foto o PDF, hasta 5 MB). {{ $isRenewal ? 'La renovación suma '.$course->subscription_days.' días y no da '.$coin(2).'.' : '' }}</flux:text>
            </div>

            <div class="flex flex-col gap-2">
                <flux:label>Comprobante</flux:label>
                <input type="file" wire:model="receipt" accept="image/jpeg,image/png,application/pdf"
                    class="text-sm text-ink-muted file:me-3 file:rounded-md file:border-0 file:bg-surface-highest file:px-3 file:py-2 file:text-ink hover:file:bg-surface-high">
                <div wire:loading wire:target="receipt" class="text-xs text-ink-muted">Subiendo…</div>
                <flux:error name="receipt" />
            </div>

            @if ($cohorts->count() > 1)
                <flux:select wire:model="cohortId" label="Comisión (opcional)">
                    <flux:select.option value="">Sin comisión</flux:select.option>
                    @foreach ($cohorts as $cohort)
                        <flux:select.option :value="$cohort->id">{{ $cohort->name }}{{ $cohort->schedule_text ? ' · '.$cohort->schedule_text : '' }}</flux:select.option>
                    @endforeach
                </flux:select>
            @endif

            <x-emoji-field><flux:textarea class="pe-10" wire:model="message" label="Mensaje para el profe (opcional)" rows="3" /></x-emoji-field>

            <div class="flex flex-wrap justify-end gap-2">
                <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                <flux:button variant="primary" type="submit" wire:loading.attr="disabled" wire:target="receipt,sendReceipt">Enviar</flux:button>
            </div>
        </form>
    </flux:modal>
</div>
