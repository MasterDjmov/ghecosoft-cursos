{{-- Datos de acceso recién generados: $credentials = ['message' => ..., 'whatsapp' => url|null]. --}}
<div class="flex flex-col gap-3" x-data="{ copied: false }" data-test="credentials">
    <pre class="whitespace-pre-wrap rounded-lg border border-outline bg-surface-lowest p-4 font-mono text-sm text-ink" x-ref="message">{{ $credentials['message'] }}</pre>
    <p class="text-xs text-ink-muted">La clave provisoria se muestra solo ahora. Si se pierde, generás otra desde la ficha del alumno.</p>
    <div class="flex flex-wrap gap-2">
        <flux:button icon="clipboard-document" x-on:click="navigator.clipboard.writeText($refs.message.innerText).then(() => { copied = true; setTimeout(() => copied = false, 2000) })">
            <span x-text="copied ? '¡Copiado!' : 'Copiar datos de acceso'">Copiar datos de acceso</span>
        </flux:button>
        @if ($credentials['whatsapp'])
            <flux:button icon="chat-bubble-left-right" :href="$credentials['whatsapp'].'?text='.rawurlencode($credentials['message'])" target="_blank" rel="noopener">
                Mandar por WhatsApp
            </flux:button>
        @endif
    </div>
</div>
