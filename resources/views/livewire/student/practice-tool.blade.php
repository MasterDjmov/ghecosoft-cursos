<div @class(['mx-auto flex w-full max-w-5xl flex-col gap-6', 'p-4 sm:p-8' => ! $inWindow, 'p-3' => $inWindow])>
    @if ($saved)
        {{-- D124: una práctica de Mis prácticas: el nombre se cambia ahí mismo. --}}
        <header class="flex flex-col gap-2" data-test="saved-practice-header">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <a href="{{ route('student.saved-practices') }}" wire:navigate class="tech-label flex items-center gap-1 hover:text-ink"><flux:icon name="arrow-left" variant="micro" /> Mis prácticas</a>
                <span class="text-xs text-ink-muted">Practicar {{ $tool['label'] }} · guardada {{ $saved->updated_at->diffForHumans() }}</span>
            </div>
            <flux:input wire:model.blur="title" maxlength="120" aria-label="Nombre de la práctica" class="font-display text-lg" data-test="saved-practice-title" />
        </header>
    @else
        <x-tool-header :title="'Practicar '.$tool['label']" :in-window="$inWindow">
            Para probar lo que quieras sin instalar nada. Lo que escribís queda en este navegador, por si volvés, y no cuenta para el curso.
            Con <strong class="text-ink">Guardar</strong> queda en <a href="{{ route('student.saved-practices') }}" wire:navigate class="text-primary-bright hover:underline">Mis prácticas</a>, para seguirla cuando quieras (y desde otra compu).
        </x-tool-header>
    @endif

    {{-- Una guardada se abre con lo guardado (no con lo que quedó en el navegador). --}}
    <x-code-runner :code="$saved?->code ?? $tool['starter']" :stdin="(string) $saved?->stdin" :show-stdin="filled($saved?->stdin)" :language="$language"
        :name="$saved ? \Illuminate\Support\Str::beforeLast($saved->fileName(), '.') : ($tool['name'] ?? 'practica')"
        :keep="$saved ? null : $language" autocomplete download data-test="practice-tool" wire:key="runner-{{ $saved?->id ?? 'nueva' }}">
        <x-slot:actions>
            {{-- Guardar: lo de la caja en la práctica abierta (o en una nueva). Avisa si hay cambios sin guardar. --}}
            <span class="flex items-center gap-1" x-data="{ savedCode: code, saving: false }"
                x-init="window.addEventListener('beforeunload', (e) => { if (@js((bool) $saved) && code !== savedCode) e.preventDefault() })">
                @if ($saved)
                    <span x-show="code !== savedCode" x-cloak class="size-2 rounded-full bg-warning" title="Hay cambios sin guardar" data-test="unsaved-dot"></span>
                @endif
                <button type="button" x-bind:disabled="saving" data-test="practice-save" title="Guardar en Mis prácticas"
                    x-on:click="saving = true; $wire.save(code, stdin).then(() => { savedCode = code; saving = false })"
                    class="inline-flex items-center gap-1.5 rounded-md px-2 py-1 text-xs font-medium text-secondary-bright transition hover:bg-secondary/15 disabled:opacity-50">
                    <flux:icon name="bookmark" variant="micro" /> <span class="hidden sm:inline">Guardar</span>
                </button>
                @if ($saved)
                    <button type="button" data-test="practice-save-copy" title="Guardar una copia aparte"
                        x-on:click="$wire.saveNew(code, stdin)"
                        class="inline-flex items-center gap-1.5 rounded-md px-2 py-1 text-xs font-medium text-ink-muted transition hover:bg-surface-high hover:text-ink">
                        <flux:icon name="document-duplicate" variant="micro" /> <span class="hidden md:inline">Copia</span>
                    </button>
                @endif
            </span>
        </x-slot:actions>
        @if ($canConsult)
            <x-slot:footer>
                {{-- D124: la consulta al profe desde la práctica; adentro del editor, se lleva el código y la salida. --}}
                <details id="consulta" class="mt-3 rounded-lg border border-outline/70 px-3 py-2 text-sm" data-test="saved-practice-chat"
                    x-data x-init="if (location.hash === '#consulta') $el.open = true">
                    <summary class="flex cursor-pointer items-center gap-2 text-ink-muted hover:text-white">
                        <flux:icon name="chat-bubble-left-right" variant="micro" class="text-primary-bright" /> Preguntale al profe
                    </summary>
                    <div class="mt-3">
                        <livewire:practice-chat :saved="$saved" :student="auth()->user()" :key="'saved-chat-'.$saved->id" lazy />
                    </div>
                </details>
            </x-slot:footer>
        @endif
    </x-code-runner>

    <section class="panel flex flex-col gap-2 p-5 text-sm text-ink">
        <h2 class="font-display text-base font-semibold text-white">Para tener en cuenta</h2>
        <ul class="list-disc space-y-1 ps-5 text-ink-muted [&_code]:text-primary-bright [&_strong]:text-ink">
            @foreach ($tool['notes'] as $note)
                <li>{!! $note !!}</li>
            @endforeach
            <li>Mientras escribís te sugiere palabras y estructuras: con <strong>Tab</strong> o <strong>Enter</strong> aceptás la que está marcada.</li>
            <li><strong>Bajar</strong> te da el archivo para abrirlo en tu compu; <strong>Guardar</strong> lo deja en Mis prácticas.</li>
        </ul>
    </section>
</div>
