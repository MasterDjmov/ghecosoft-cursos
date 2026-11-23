{{-- D124: la consulta al profe desde una práctica guardada; adentro del editor, se lleva el código y la salida. --}}
<details id="consulta" class="mt-3 rounded-lg border border-outline/70 px-3 py-2 text-sm" data-test="saved-practice-chat"
    x-data x-init="if (location.hash === '#consulta') $el.open = true">
    <summary class="flex cursor-pointer items-center gap-2 text-ink-muted hover:text-white">
        <flux:icon name="chat-bubble-left-right" variant="micro" class="text-primary-bright" /> Preguntale al profe
    </summary>
    <div class="mt-3">
        <livewire:practice-chat :saved="$saved" :student="auth()->user()" :key="'saved-chat-'.$saved->id" lazy />
    </div>
</details>
