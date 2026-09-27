{{-- Adjuntar archivo en una hoja (dentro de PracticeCard). --}}
<div class="flex flex-col gap-2">
    <flux:label>{{ $hint }}</flux:label>
    <input type="file" wire:model="file"
        class="text-sm text-ink-muted file:me-3 file:rounded-md file:border-0 file:bg-surface-highest file:px-3 file:py-2 file:text-ink hover:file:bg-surface-high">
    <div wire:loading wire:target="file" class="text-xs text-ink-muted">Subiendo…</div>
    <flux:error name="file" />
</div>
