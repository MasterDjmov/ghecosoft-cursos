{{-- D124: encabezado de una práctica de Mis prácticas abierta en su herramienta: el nombre se cambia ahí mismo. --}}
<header class="flex flex-col gap-2" data-test="saved-practice-header">
    <div class="flex flex-wrap items-center justify-between gap-2">
        <a href="{{ route('student.saved-practices') }}" wire:navigate class="tech-label flex items-center gap-1 hover:text-ink"><flux:icon name="arrow-left" variant="micro" /> Mis prácticas</a>
        <span class="text-xs text-ink-muted">{{ $toolLabel }} · guardada {{ $saved->updated_at->diffForHumans() }}</span>
    </div>
    <flux:input wire:model.blur="title" maxlength="120" aria-label="Nombre de la práctica" class="font-display text-lg" data-test="saved-practice-title" />
</header>
