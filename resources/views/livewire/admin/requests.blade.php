<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header title="Solicitudes"
        subtitle="Al aprobar una inscripción se acreditan las monedas del raíz y arranca el abono. Una renovación solo suma días." />

    <div class="grid gap-4 sm:grid-cols-2">
        <flux:select wire:model.live="status" label="Estado">
            <flux:select.option value="pending">Pendientes ({{ $pendingCount }})</flux:select.option>
            <flux:select.option value="approved">Aprobadas</flux:select.option>
            <flux:select.option value="rejected">Rechazadas</flux:select.option>
            <flux:select.option value="all">Todas</flux:select.option>
        </flux:select>
        <flux:select wire:model.live="courseId" label="Curso">
            <flux:select.option value="">Todos</flux:select.option>
            @foreach ($courses as $option)
                <flux:select.option :value="(string) $option->id">{{ $option->title }}</flux:select.option>
            @endforeach
        </flux:select>
    </div>

    <div class="flex flex-col gap-3">
        @forelse ($requests as $request)
            <article class="panel flex flex-col gap-3 p-4 sm:flex-row sm:items-center" wire:key="request-{{ $request->id }}" data-test="request-{{ $request->id }}">
                <div class="flex min-w-0 flex-1 flex-col gap-1">
                    <div class="flex flex-wrap items-center gap-2">
                        <span class="font-medium text-white">{{ $request->user->fullName() }}</span>
                        <span class="font-mono text-xs text-ink-muted">{{ '@'.$request->user->username }}</span>
                        <flux:badge size="sm" :color="$request->kind === \App\Enums\RequestKind::New ? 'cyan' : 'violet'">{{ $request->kind->label() }}</flux:badge>
                        <flux:badge size="sm" :color="match ($request->status) { \App\Enums\RequestStatus::Pending => 'amber', \App\Enums\RequestStatus::Approved => 'green', default => 'red' }">{{ $request->status->label() }}</flux:badge>
                    </div>
                    <p class="text-sm text-ink-muted">
                        {{ $request->course->title }}@if ($request->cohort) · {{ $request->cohort->name }}@endif
                        · {{ $request->created_at->format('d/m/Y H:i') }}
                        · {{ match ($request->type) { \App\Enums\RequestType::Receipt => 'con comprobante', \App\Enums\RequestType::Contact => 'avisó por WhatsApp', \App\Enums\RequestType::Admin => 'la cargaste vos' } }}
                    </p>
                    @if ($request->message)
                        <p class="text-sm text-ink">«{{ $request->message }}»</p>
                    @endif
                    @if ($request->admin_note)
                        <p class="text-xs text-ink-muted">Tu nota: {{ $request->admin_note }}</p>
                    @endif
                    @if ($request->reviewed_at)
                        <p class="text-xs text-ink-muted">Revisada el {{ $request->reviewed_at->format('d/m/Y H:i') }}{{ $request->reviewer ? ' por '.$request->reviewer->name : '' }}</p>
                    @endif
                </div>
                <div class="flex shrink-0 flex-wrap gap-2">
                    @if ($request->receipt_path)
                        <flux:button size="sm" icon="document-text" :href="route('files.receipt', $request)" target="_blank">Comprobante</flux:button>
                    @endif
                    @if ($request->user->phone)
                        <flux:button size="sm" variant="ghost" icon="phone" :href="'https://wa.me/'.preg_replace('/\D+/', '', $request->user->phone)" target="_blank">WhatsApp</flux:button>
                    @endif
                    @if ($request->status === \App\Enums\RequestStatus::Pending)
                        <flux:button size="sm" variant="primary" icon="check" wire:click="review({{ $request->id }}, 'approve')">Aprobar</flux:button>
                        <flux:button size="sm" variant="ghost" icon="x-mark" wire:click="review({{ $request->id }}, 'reject')">Rechazar</flux:button>
                    @endif
                </div>
            </article>
        @empty
            <div class="panel p-8 text-center text-ink-muted">No hay solicitudes {{ $status === 'pending' ? 'pendientes' : 'con ese filtro' }}.</div>
        @endforelse
    </div>

    {{ $requests->links() }}

    <flux:modal name="review" class="w-full max-w-md">
        @if ($reviewing)
            <form wire:submit="confirm" class="flex flex-col gap-4">
                <flux:heading size="lg">{{ $decision === 'approve' ? 'Aprobar' : 'Rechazar' }} · {{ $reviewing->user->fullName() }}</flux:heading>
                @if ($decision === 'approve')
                    <flux:text>
                        @if ($reviewing->kind === \App\Enums\RequestKind::New)
                            Se acreditan <strong>{{ $reviewing->course->root_price }} {{ term('coin.course', $reviewing->course, $reviewing->course->root_price) }}</strong>
                            y arranca un abono de {{ $reviewing->course->subscription_days }} días en {{ $reviewing->course->title }}.
                        @else
                            Se suman {{ $reviewing->course->subscription_days }} días al abono de {{ $reviewing->course->title }} (sin monedas).
                        @endif
                    </flux:text>
                @endif
                <flux:textarea wire:model="note" :label="$decision === 'approve' ? 'Nota (opcional)' : 'Motivo'" rows="3" />
                <div class="flex justify-end gap-2">
                    <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                    <flux:button :variant="$decision === 'approve' ? 'primary' : 'danger'" type="submit">{{ $decision === 'approve' ? 'Aprobar' : 'Rechazar' }}</flux:button>
                </div>
            </form>
        @endif
    </flux:modal>
</div>
