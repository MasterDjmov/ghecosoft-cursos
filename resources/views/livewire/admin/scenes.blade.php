{{-- Historia → Escenas (D88): las imágenes de las micro-misiones, nodo por nodo con su crónica. --}}
<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header label="Juego" title="Escenas"
        subtitle="Las imágenes de las micro-misiones. El nombre del archivo es el ID de la micro-misión (el mismo del editor: r00-n01-p1). Copiá el pedido, generala y subila acá, o dejala en la carpeta escenas/ del curso para que la tome el importador." />

    <div class="flex flex-col gap-4 sm:flex-row sm:items-end">
        <flux:select wire:model.live="courseSlug" label="Curso" class="sm:w-80">
            @foreach ($courses as $option)
                <flux:select.option :value="$option->slug">{{ $option->title }}</flux:select.option>
            @endforeach
        </flux:select>
        <flux:switch wire:model.live="onlyMissing" label="Solo las que faltan" />
        @if ($course)
            <div class="flex flex-col gap-1 sm:ms-auto sm:items-end" data-test="scenes-counter">
                <span class="tech-label">Con imagen</span>
                <span class="font-display text-2xl font-semibold text-white">{{ $withImage }} <span class="text-base text-ink-muted">de {{ $total }}</span></span>
            </div>
        @endif
    </div>

    @if ($courses->isEmpty())
        <flux:callout icon="information-circle" color="zinc">
            <flux:callout.text>Todavía ningún curso tiene micro-misiones. Se escriben en el .md del curso (### Micro-misión R01-N01-P1 · …) y se importan.</flux:callout.text>
        </flux:callout>
    @endif

    @foreach ($nodes as $node)
        <section class="flex flex-col gap-3" wire:key="node-{{ $node->id }}" data-test="scene-node">
            <div class="flex flex-col gap-1">
                <p class="tech-label text-primary-bright">{{ $node->code }}</p>
                <h2 class="font-display text-lg font-semibold text-white">{{ $node->title }}</h2>
            </div>
            @if ($node->chronicle)
                <details class="rounded-lg border border-secondary/40 bg-secondary/10 px-4 py-2 text-sm">
                    <summary class="cursor-pointer text-secondary-bright">Crónica del nodo</summary>
                    <div class="markdown mt-2 text-ink italic">{!! $chronicle($node) !!}</div>
                </details>
            @endif

            @foreach ($node->steps as $step)
                @php
                    $prompt = trim(implode("\n", array_filter([
                        $step->code.' · '.$step->title,
                        $step->place ? 'Lugar: '.$step->place : null,
                        $step->characters ? 'Personajes: '.$step->characters : null,
                        $step->image_prompt,
                        \App\Livewire\Admin\Scenes::STYLE,
                    ])));
                @endphp
                <article @class(['panel flex flex-col gap-4 p-4 sm:flex-row', 'border-warning/50' => ! $step->image_path]) wire:key="step-{{ $step->id }}" data-test="scene-{{ $step->code }}">
                    {{-- La imagen o el lugar vacío --}}
                    <div class="flex shrink-0 flex-col gap-2 sm:w-64">
                        @if ($url = $step->imageUrl())
                            <img src="{{ $url }}" alt="" class="aspect-[16/9] w-full rounded-lg border border-outline object-cover" loading="lazy">
                        @else
                            <div class="flex aspect-[16/9] w-full items-center justify-center rounded-lg border border-dashed border-warning/60 text-xs text-warning">Falta la imagen</div>
                        @endif
                        <label class="flex cursor-pointer items-center justify-center gap-1.5 rounded-md border border-outline px-2 py-1.5 text-xs text-ink hover:bg-surface-high">
                            <flux:icon name="arrow-up-tray" variant="micro" /> {{ $step->image_path ? 'Cambiar' : 'Subir' }}
                            <input type="file" class="hidden" accept="image/png,image/jpeg,image/webp" wire:model="uploads.{{ $step->id }}">
                        </label>
                        <div wire:loading wire:target="uploads.{{ $step->id }}" class="text-center text-xs text-ink-muted">Subiendo…</div>
                        <flux:error name="uploads.{{ $step->id }}" />
                        @if ($step->image_path)
                            <button type="button" class="text-xs text-ink-muted hover:text-danger" wire:click="removeImage({{ $step->id }})" wire:confirm="¿Quitar la imagen de {{ $step->code }}?">Quitar</button>
                        @endif
                    </div>

                    {{-- Los datos de la micro-misión --}}
                    <div class="flex min-w-0 flex-1 flex-col gap-2">
                        <div class="flex flex-wrap items-center gap-2">
                            <button type="button" class="rounded border border-primary-bright/50 px-2 py-0.5 font-mono text-xs text-primary-bright hover:bg-primary/10"
                                x-data x-on:click="navigator.clipboard.writeText(@js(strtolower($step->code))); $el.textContent = '¡Copiado!'" title="Copiar el nombre del archivo">{{ strtolower($step->code) }}</button>
                            <span class="font-medium text-white">{{ $step->title }}</span>
                        </div>
                        <p class="text-xs text-ink-muted">
                            @if ($step->place)<span class="text-secondary-bright">{{ $step->place }}</span>@endif
                            @if ($step->characters) · {{ $step->characters }}@endif
                        </p>
                        @if ($step->scene)
                            <details class="text-sm">
                                <summary class="cursor-pointer text-ink-muted">Escena</summary>
                                <div class="markdown mt-1 text-ink">{!! $scene($step) !!}</div>
                            </details>
                        @endif
                        @if ($step->image_prompt)
                            <div class="flex flex-col gap-1">
                                <div class="flex items-center justify-between">
                                    <p class="tech-label">Pedido de imagen</p>
                                    <button type="button" class="flex items-center gap-1 text-xs text-primary-bright hover:underline" data-test="copy-prompt"
                                        x-data x-on:click="navigator.clipboard.writeText(@js($prompt)); $el.lastChild.textContent = ' ¡Copiado!'">
                                        <flux:icon name="clipboard" variant="micro" /><span> Copiar pedido</span>
                                    </button>
                                </div>
                                <div class="markdown rounded-lg border border-outline bg-surface-lowest p-3 text-sm text-ink">{!! \App\Support\Markdown::render($step->image_prompt) !!}</div>
                            </div>
                        @endif
                    </div>
                </article>
            @endforeach
        </section>
    @endforeach

    @if ($course && $nodes->isEmpty() && $onlyMissing)
        <flux:callout icon="check-circle" color="emerald">
            <flux:callout.text>¡No falta ninguna imagen en este curso!</flux:callout.text>
        </flux:callout>
    @endif
</div>
