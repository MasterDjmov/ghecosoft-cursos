{{-- Historia → Personajes: las fichas de PERSONAJES.md con su pedido para generar las imágenes. --}}
<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-wrap items-end justify-between gap-3">
        <div class="flex flex-col gap-1">
            <p class="tech-label">Historia</p>
            <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Personajes</h1>
            <p class="text-ink-muted">La ficha de cada personaje, para generar sus imágenes siempre iguales. «Copiar pedido» copia la ficha con el estilo común, lista para pegar en Stitch. Se editan en <code class="font-mono text-sm">docs/historias/PERSONAJES.md</code>.</p>
        </div>
        <flux:switch wire:model.live="onlyMissing" label="Solo las que faltan ({{ $missing }})" data-test="only-missing" />
    </header>

    @forelse ($groups as $section => $sheets)
        <section class="flex flex-col gap-3" wire:key="section-{{ \Illuminate\Support\Str::slug($section) }}">
            <h2 class="font-display text-lg font-semibold text-white">{{ $section }}</h2>
            <div class="grid gap-3 md:grid-cols-2">
                @foreach ($sheets as $sheet)
                    <details class="panel group overflow-hidden" wire:key="sheet-{{ $sheet['slug'] }}" data-test="character-{{ $sheet['slug'] }}">
                        <summary class="flex cursor-pointer items-center justify-between gap-3 px-4 py-3">
                            <span class="font-medium text-white">{{ $sheet['name'] }}</span>
                            <span class="flex shrink-0 items-center gap-2">
                                @if ($sheet['missing'])
                                    <span class="rounded-md border border-warning/40 bg-warning/10 px-2 py-0.5 text-xs text-warning">Falta la imagen</span>
                                @endif
                                <flux:icon name="chevron-down" variant="micro" class="text-ink-muted transition group-open:rotate-180" />
                            </span>
                        </summary>
                        <div class="flex flex-col gap-3 border-t border-outline/60 p-4">
                            <div class="markdown text-sm text-ink">{!! \App\Support\Markdown::render($sheet['body']) !!}</div>
                            <button type="button" class="flex items-center gap-1 self-start text-sm text-primary-bright hover:underline" data-test="copy-character-prompt"
                                x-data x-on:click="navigator.clipboard.writeText(@js(\App\Support\CharacterSheets::prompt($sheet))); $el.lastChild.textContent = ' ¡Copiado!'">
                                <flux:icon name="clipboard" variant="micro" /><span> Copiar pedido</span>
                            </button>
                        </div>
                    </details>
                @endforeach
            </div>
        </section>
    @empty
        <p class="text-ink-muted" data-test="characters-empty">{{ $onlyMissing ? 'No falta ninguna imagen.' : 'No se encontró docs/historias/PERSONAJES.md.' }}</p>
    @endforelse
</div>
