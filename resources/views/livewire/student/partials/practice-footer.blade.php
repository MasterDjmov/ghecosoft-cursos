{{-- Pie de una hoja (dentro de PracticeCard): estado a la izquierda, acciones a la derecha.
     $submitDisabled: expresión de Alpine que deshabilita "Entregar" (null = botón de formulario). --}}
<div class="-mx-6 flex flex-col gap-3 border-t border-outline px-6 pt-5 sm:flex-row sm:items-center sm:justify-between">
    <div class="flex min-w-0 flex-col gap-1">
        <p class="flex items-center gap-2 text-sm" style="color: {{ $statusColor }}">
            @if ($statusIcon)
                <flux:icon :name="$statusIcon" variant="micro" class="shrink-0" />
            @endif
            <span @class(['text-ink-muted' => ! $status])>{{ $footerStatus }}</span>
        </p>
        @if ($reviewNotice)
            <p class="flex items-start gap-2 text-xs text-warning" data-test="review-notice"><flux:icon name="moon" variant="micro" class="mt-px shrink-0" /> {{ $reviewNotice }}</p>
        @endif
        @if ($blocker && $status !== 'approved')
            <p class="flex items-start gap-2 text-xs text-ink-muted"><flux:icon name="information-circle" variant="micro" class="mt-px shrink-0" /> {{ $blocker }}</p>
        @endif
    </div>

    <div class="flex flex-wrap items-center gap-2 sm:shrink-0 sm:justify-end">
        @if ($trial)
            <flux:button variant="primary" icon="ticket" :href="route('student.course', $course)" wire:navigate data-test="trial-enroll">Pedir abono</flux:button>
        @endif
        @if ($showMark)
            @if ($mode === \App\Enums\SubmissionMode::None)
                <flux:button icon="check" wire:click="toggleMark" :disabled="! $canSubmit">Marcar como completada</flux:button>
            @else
                <flux:button :icon="$marked ? 'check-circle' : 'check'" wire:click="toggleMark">
                    {{ $marked ? 'Marcada como completada' : 'Marcar como completada' }}
                </flux:button>
            @endif
        @endif

        @if ($canSubmit && ($usesCode || $usesFile))
            @if ($submitDisabled)
                <flux:button variant="primary" icon="paper-airplane" x-on:click="$wire.submit(code)"
                    x-bind:disabled="{{ $submitDisabled }}" wire:loading.attr="disabled" wire:target="file,submit">Entregar</flux:button>
            @else
                <flux:button type="submit" variant="primary" icon="paper-airplane" wire:loading.attr="disabled" wire:target="file,submit">Entregar</flux:button>
            @endif
        @endif
    </div>
</div>
