@php($withdrawal = $kindEnum === \App\Enums\ConsumerRequestKind::Withdrawal)
<div class="flex flex-col gap-6" data-test="consumer-request-form">
    <div class="flex flex-col gap-2">
        <h1 class="font-display text-3xl font-semibold text-white">{{ $withdrawal ? 'Botón de arrepentimiento' : 'Botón de baja' }}</h1>
        @if ($withdrawal)
            <p class="text-ink">
                Si pagaste un abono, tenés {{ config('legal.withdrawal_days') }} días corridos desde que se aprobó para arrepentirte, sin dar motivos,
                y te devolvemos todo lo que pagaste. No hace falta que entres a tu cuenta.
            </p>
        @else
            <p class="text-ink">
                Pedí la baja de tu abono o de tu cuenta. El abono no se renueva solo, así que no se te va a volver a cobrar.
                Si querés que también borremos tu cuenta y tus datos, decilo en el detalle.
            </p>
        @endif
        <p class="text-sm text-ink-muted">Más información en los <a href="{{ route('legal.terms') }}" class="text-primary-bright hover:underline">Términos y condiciones</a>.</p>
    </div>

    @if ($code)
        <div class="panel flex flex-col gap-2 border-success/50 p-5" data-test="consumer-request-code">
            <p class="tech-label text-success!">Pedido recibido</p>
            <p class="text-ink">Tu código de trámite es</p>
            <p class="font-mono text-3xl tracking-widest text-white">{{ $code }}</p>
            <p class="text-sm text-ink-muted">Guardalo. El profe te escribe a {{ $contact }} para coordinar {{ $withdrawal ? 'la devolución' : 'la baja' }}.</p>
        </div>
    @else
        <form wire:submit="send" class="panel flex flex-col gap-5 p-5 sm:p-6">
            <flux:input wire:model="name" label="Nombre y apellido" required />
            <flux:input wire:model="contact" label="Email o teléfono" description="Para que te podamos responder." required />
            <flux:input wire:model="course" label="Curso (opcional)" placeholder="Python, Inglés Primaria…" />
            <flux:textarea wire:model="details" :label="$withdrawal ? 'Detalle (opcional)' : 'Qué querés dar de baja (opcional)'" rows="3"
                :placeholder="$withdrawal ? 'Fecha del pago, alias o CBU para la devolución…' : 'El abono de un curso, o también la cuenta y los datos'" />
            <div>
                <flux:button type="submit" variant="primary" icon="paper-airplane">{{ $withdrawal ? 'Enviar arrepentimiento' : 'Pedir la baja' }}</flux:button>
            </div>
        </form>
    @endif
</div>
