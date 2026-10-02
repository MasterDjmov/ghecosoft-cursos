@props(['fill' => false])

{{-- Vista previa de HTML y CSS (D76): vive dentro de un x-data="codeRunner(...)" y usa preview, device,
     fullscreen y status. La página se dibuja en un <iframe sandbox=""> (sin JavaScript, sin formularios ni
     ventanas, con un origen propio) y con la CSP que le pone resources/js/runners/html.js. Se ve a 390 px
     (celular) o a 1280 px (compu), achicada para que entre; en pantalla completa, a su tamaño. --}}
<div {{ $attributes->class(['flex flex-col bg-[#05070d]', 'min-h-0' => $fill]) }} data-test="html-preview"
    x-on:keydown.escape.window="fullscreen = false">
    <div class="flex shrink-0 items-center gap-1 border-b border-outline/60 px-2" role="tablist" aria-label="Tamaño de pantalla">
        @foreach (['mobile' => ['device-phone-mobile', 'Celular'], 'desktop' => ['computer-desktop', 'Compu']] as $value => [$icon, $label])
            <button type="button" role="tab" x-on:click="device = '{{ $value }}'" x-bind:aria-selected="device === '{{ $value }}'"
                class="-mb-px flex items-center gap-1.5 border-b-2 px-2.5 py-2 text-xs font-medium transition"
                x-bind:class="device === '{{ $value }}' ? 'border-primary-bright text-ink' : 'border-transparent text-ink-muted hover:text-ink'">
                <flux:icon :name="$icon" variant="micro" /> {{ $label }}
            </button>
        @endforeach
        <span class="ms-auto truncate ps-2 font-mono text-[11px]" x-bind:class="error ? 'text-danger' : 'text-ink-muted'" x-text="showReference ? 'Así tiene que quedar' : status"></span>
        <button type="button" x-show="references[device]" x-cloak x-on:click="showReference = ! showReference" data-test="compare-reference"
            class="ms-1 flex items-center gap-1 rounded px-2 py-1 text-xs font-medium transition"
            x-bind:class="showReference ? 'bg-secondary/20 text-secondary-bright' : 'text-ink-muted hover:bg-surface-high hover:text-ink'"
            title="Ver cómo tiene que quedar, en el mismo tamaño">
            <flux:icon name="photo" variant="micro" /> <span x-text="showReference ? 'Ver la mía' : 'Comparar'">Comparar</span>
        </button>
        <button type="button" x-on:click="fullscreen = true" class="ms-1 rounded p-1.5 text-ink-muted hover:bg-surface-high hover:text-ink" title="Pantalla completa">
            <flux:icon name="arrows-pointing-out" variant="micro" />
        </button>
    </div>

    {{-- El escenario: en pantalla completa ocupa toda la ventana (el mismo iframe, sin recargar). --}}
    <div x-data="{ w: 0, h: 0, init() { new ResizeObserver(([e]) => { this.w = e.contentRect.width; this.h = e.contentRect.height }).observe(this.$refs.stage) } }"
        x-bind:class="fullscreen ? 'fixed inset-0 z-50 flex flex-col bg-[#05070d]' : '{{ $fill ? 'flex min-h-0 flex-1 flex-col' : 'flex flex-col' }}'">
        <div x-show="fullscreen" x-cloak class="flex shrink-0 items-center gap-2 border-b border-outline px-4 py-2">
            <span class="tech-label">Vista previa</span>
            <div class="flex rounded-lg border border-outline p-0.5">
                <button type="button" x-on:click="device = 'mobile'" class="rounded px-2.5 py-1 text-xs" x-bind:class="device === 'mobile' ? 'bg-surface-high text-white' : 'text-ink-muted'">Celular</button>
                <button type="button" x-on:click="device = 'desktop'" class="rounded px-2.5 py-1 text-xs" x-bind:class="device === 'desktop' ? 'bg-surface-high text-white' : 'text-ink-muted'">Compu</button>
            </div>
            <button type="button" x-on:click="fullscreen = false" class="ms-auto flex items-center gap-1.5 rounded-md px-2 py-1 text-xs text-ink-muted hover:bg-surface-high hover:text-ink">
                <flux:icon name="x-mark" variant="micro" /> Cerrar (Esc)
            </button>
        </div>
        <div x-ref="stage" @class(['relative overflow-hidden bg-[#0b1020]', 'min-h-0 flex-1' => $fill, 'h-[28rem]' => ! $fill])
            x-bind:class="fullscreen && 'min-h-0 flex-1'">
            @php($width = "(device === 'mobile' ? 390 : 1280)")
            {{-- La captura de referencia: mismo ancho (achicado igual que la página) y se recorre hacia abajo. --}}
            <div x-show="showReference && references[device]" x-cloak class="absolute inset-0 overflow-y-auto">
                <img x-bind:src="references[device]" alt="Así tiene que quedar" class="mx-auto block max-w-none bg-white shadow-lg"
                    x-bind:style="`width: ${ {{ $width }} * Math.min(1, w / {{ $width }}) }px`">
            </div>
            <iframe x-show="! (showReference && references[device])" sandbox="" referrerpolicy="no-referrer" title="Vista previa de la página" x-bind:srcdoc="preview" loading="lazy"
                class="absolute top-0 origin-top-left border-0 bg-white shadow-lg"
                x-bind:style="(() => { const d = {{ $width }}; const s = Math.min(1, w / d); return `width: ${d}px; height: ${s > 0 ? h / s : h}px; transform: scale(${s}); left: ${Math.max(0, (w - d * s) / 2)}px`; })()"></iframe>
        </div>
    </div>
</div>
