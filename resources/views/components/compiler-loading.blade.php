{{-- Mientras se baja el compilador la primera vez (el estado empieza con «Cargando»): Gheco avisa que hay que esperar,
     para que nadie se quede mirando sin saber si anda. Vive dentro de un x-data="codeRunner(...)" (usa running y status). --}}
<div x-show="running && /^Cargando/.test(status ?? '')" x-cloak x-transition.opacity role="status" aria-live="polite"
    class="flex items-center gap-3 rounded-lg border border-primary/50 bg-primary/10 p-3 shadow-[0_0_18px_-4px] shadow-primary/40 motion-safe:animate-pulse"
    data-test="compiler-loading">
    <img src="{{ asset('img/personajes/gheco.webp') }}" alt="Gheco" class="size-14 shrink-0 object-contain motion-safe:animate-bounce" loading="lazy">
    <div class="min-w-0 text-sm">
        <p class="font-medium text-ink">Aguardá un momento: estoy preparando el compilador.</p>
        <p class="text-xs text-ink-muted">La primera vez tarda un poco porque se descarga; después queda guardado y arranca enseguida. No hace falta tocar nada.</p>
        <p class="mt-1 font-mono text-[11px] text-primary-bright" x-text="status"></p>
    </div>
</div>
