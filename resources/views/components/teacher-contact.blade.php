{{-- Ayuda para entrar: WhatsApp o llamada al número del profe (Configuración). Sin número, no se muestra. --}}
@php
    $number = preg_replace('/\D+/', '', (string) \App\Models\Setting::get('whatsapp_number'));
    $text = rawurlencode('Hola profe, no puedo entrar a mi cuenta de '.config('app.name').'.');
@endphp
@if ($number !== '')
    <div {{ $attributes->class('flex flex-col items-center gap-2 rounded-lg border border-outline bg-surface-low/60 p-3 text-center text-sm') }} data-test="teacher-contact">
        <p class="text-ink-muted">¿No tenés email o no te llega? Escribile al profe.</p>
        <div class="flex flex-wrap justify-center gap-2">
            <flux:button size="sm" icon="chat-bubble-left-right" href="https://wa.me/{{ $number }}?text={{ $text }}" target="_blank" rel="noopener">WhatsApp</flux:button>
            <flux:button size="sm" variant="ghost" icon="phone" href="tel:+{{ $number }}">Llamar</flux:button>
        </div>
    </div>
@endif
