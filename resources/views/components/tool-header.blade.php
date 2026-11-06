@props(['title', 'inWindow' => false])

{{-- Encabezado de una herramienta (D120). En la ventana flotante no va: su barra ya dice cuál es. --}}
@unless ($inWindow)
    <header class="flex flex-col gap-1">
        <div class="flex flex-wrap items-center justify-between gap-2">
            <p class="tech-label">Herramientas</p>
            <button type="button" data-tool-window="{{ url()->current() }}" data-tool-title="{{ $title }}" data-test="tool-open-window" {{ $attributes }}
                class="inline-flex items-center gap-1.5 rounded-md border border-outline px-2.5 py-1 text-xs text-ink-muted transition hover:border-primary-bright hover:text-ink">
                <flux:icon name="arrow-top-right-on-square" variant="micro" /> Abrir en ventana
            </button>
        </div>
        <h1 class="font-display text-2xl font-semibold text-white">{{ $title }}</h1>
        <p class="text-sm text-ink-muted">{{ $slot }}</p>
    </header>
@endunless
