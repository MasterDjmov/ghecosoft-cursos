{{-- D124: en una práctica sin guardar, al alumno se le explica cómo consultarle al profe (la consulta va atada a una
     práctica guardada, con su código). --}}
@unless (auth()->user()->isStaff())
    <p class="mt-3 flex items-center gap-2 text-xs text-ink-muted" data-test="saved-chat-hint">
        <flux:icon name="chat-bubble-left-right" variant="micro" class="shrink-0 text-primary-bright" />
        ¿Tenés una duda? Tocá <strong class="text-secondary-bright">Guardar</strong> y en la práctica guardada te aparece «Preguntale al profe».
    </p>
@endunless
