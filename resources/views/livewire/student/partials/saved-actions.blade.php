{{-- D124: «Guardar» (y «Copia») en la barra del editor; ve las variables de codeRunner (code, stdin). $extra suma
     argumentos de la herramienta (la caja de la Feria manda el lenguaje y la página). Avisa los cambios sin guardar. --}}
@php($extra = $extra ?? '')
<span class="flex items-center gap-1" x-data="{ savedCode: code, saving: false }"
    x-init="window.addEventListener('beforeunload', (e) => { if (@js((bool) $saved) && code !== savedCode) e.preventDefault() })">
    @if ($saved)
        <span x-show="code !== savedCode" x-cloak class="size-2 rounded-full bg-warning" title="Hay cambios sin guardar" data-test="unsaved-dot"></span>
    @endif
    <button type="button" x-bind:disabled="saving" data-test="practice-save" title="Guardar en Mis prácticas"
        x-on:click="saving = true; $wire.save(code, stdin{{ $extra }}).then(() => { savedCode = code; saving = false })"
        class="inline-flex items-center gap-1.5 rounded-md px-2 py-1 text-xs font-medium text-secondary-bright transition hover:bg-secondary/15 disabled:opacity-50">
        <flux:icon name="bookmark" variant="micro" /> <span class="hidden sm:inline">Guardar</span>
    </button>
    @if ($saved)
        <button type="button" data-test="practice-save-copy" title="Guardar una copia aparte" x-on:click="$wire.saveNew(code, stdin)"
            class="inline-flex items-center gap-1.5 rounded-md px-2 py-1 text-xs font-medium text-ink-muted transition hover:bg-surface-high hover:text-ink">
            <flux:icon name="document-duplicate" variant="micro" /> <span class="hidden md:inline">Copia</span>
        </button>
    @endif
</span>
