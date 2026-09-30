@php($pending = $submission->status === \App\Enums\SubmissionStatus::Submitted)

<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header :label="$course->title.' · '.$node->title" :title="$practice->title">
        <x-slot:actions>
            <flux:button variant="ghost" icon="arrow-left" :href="route('admin.submissions.index')" wire:navigate>Bandeja ({{ $pendingCount }})</flux:button>
        </x-slot:actions>
    </x-admin.page-header>

    <section class="panel flex flex-col gap-3 p-5 sm:flex-row sm:items-center">
        <div class="flex min-w-0 flex-1 flex-col gap-1">
            <div class="flex flex-wrap items-center gap-2">
                <a href="{{ route('admin.students.show', $submission->user) }}" wire:navigate class="font-medium text-white hover:text-primary-bright">{{ $submission->user->fullName() }}</a>
                <span class="font-mono text-xs text-ink-muted">{{ '@'.$submission->user->username }}</span>
                <flux:badge size="sm" :color="['submitted' => 'amber', 'approved' => 'green', 'redo' => 'red'][$submission->status->value]">{{ $submission->status->label() }}</flux:badge>
                <flux:badge size="sm" :color="$practice->is_required ? 'cyan' : 'violet'">{{ $practice->is_required ? 'Obligatoria' : 'Optativa' }}</flux:badge>
            </div>
            <p class="text-sm text-ink-muted">
                Intento {{ $submission->attempt }} · entregado {{ $submission->submitted_at->format('d/m/Y H:i') }}
                @if ($submission->reviewed_at) · corregido {{ $submission->reviewed_at->format('d/m/Y H:i') }}{{ $submission->reviewer ? ' por '.$submission->reviewer->name : '' }} @endif
            </p>
        </div>
        <span class="font-mono text-xs text-ink-muted">
            paga +{{ $practice->coin_reward }} {{ $practice->is_required ? term('coin.course', $course, $practice->coin_reward) : term('coin.wildcard', null, $practice->coin_reward) }}
            · +{{ $practice->xp_reward }} {{ term('xp.short') }}
        </span>
    </section>

    @if ($instructionsHtml)
        <details class="panel p-5">
            <summary class="cursor-pointer font-medium text-white">Consigna</summary>
            <div class="markdown mt-3 text-sm">{!! $instructionsHtml !!}</div>
        </details>
    @endif

    @if ($criteriaHtml)
        <section class="panel flex flex-col gap-2 border-s-4 border-s-success p-5" data-test="criteria">
            <p class="tech-label flex items-center gap-2 text-success"><flux:icon name="clipboard-document-check" variant="micro" /> Criterio de aprobación</p>
            <div class="markdown text-sm">{!! $criteriaHtml !!}</div>
        </section>
    @endif

    @if ($practice->reference_solution)
        <details class="panel p-5" data-test="reference-solution">
            <summary class="cursor-pointer font-medium text-white">Solución de referencia <span class="text-xs text-ink-muted">(solo vos)</span></summary>
            <pre class="mt-3 max-h-96 overflow-auto rounded-lg border border-outline bg-[#05070d] p-3 font-mono text-sm whitespace-pre-wrap text-ink">{{ $practice->reference_solution }}</pre>
        </details>
    @endif

    <section class="panel flex flex-col gap-4 p-5">
        @if ($submission->code)
            <x-code-runner :code="$submission->code" :stdin="$practice->sample_input" :expected="$practice->expected_output" :language="$course->language->value"
                read-only :name="'intento_'.$submission->attempt" wire:key="code-{{ $submission->id }}" />
            @if ($course->language->value === 'java')
                <x-local-run :code="$submission->code" :stdin="$practice->sample_input" :name="'intento_'.$submission->id" wire:key="local-{{ $submission->id }}" />
            @endif
        @endif
        @if ($submission->file_path)
            <flux:button icon="paper-clip" :href="route('files.submission', $submission)" class="self-start">{{ $submission->file_original_name }}</flux:button>
        @endif
        @if (! $submission->code && ! $submission->file_path)
            <flux:text>Práctica sin entrega: el alumno la marcó como completada.</flux:text>
        @endif
    </section>

    {{-- Hilo --}}
    <section class="panel flex flex-col gap-3 p-5">
        <h2 class="font-display font-semibold text-white">Comentarios</h2>
        @forelse ($submission->comments as $item)
            <div @class(['rounded-md p-3 text-sm', 'bg-primary/10 border-s-2 border-primary-bright' => $item->user->isStaff(), 'bg-surface-high' => ! $item->user->isStaff()])>
                <p class="text-xs text-ink-muted">{{ $item->user->is(auth()->user()) ? 'Vos' : ($item->user->isStaff() ? 'Profe '.$item->user->name : $item->user->fullName()) }} · {{ $item->created_at->format('d/m H:i') }}</p>
                <p class="text-ink">{!! nl2br(e($item->body)) !!}</p>
            </div>
        @empty
            <flux:text>Sin comentarios.</flux:text>
        @endforelse

        @unless ($pending)
            <form wire:submit="addReply" class="flex items-end gap-2">
                <x-emoji-field class="flex-1"><flux:textarea class="pe-10" wire:model="reply" rows="2" placeholder="Responder…" aria-label="Respuesta" /></x-emoji-field>
                <flux:button type="submit" icon="paper-airplane">Enviar</flux:button>
            </form>
            <flux:error name="reply" />
        @endunless
    </section>

    {{-- Corrección --}}
    @if ($pending)
        <section class="panel panel-active flex flex-col gap-4 p-5">
            <x-emoji-field><flux:textarea class="pe-10" wire:model="comment" label="Comentario" rows="3" placeholder="Opcional al aprobar; obligatorio para Rehacer." /></x-emoji-field>
            <div class="flex flex-wrap justify-end gap-2">
                <flux:button icon="arrow-path" wire:click="redo">Rehacer</flux:button>
                <flux:button variant="primary" icon="check" wire:click="approve">Aprobar</flux:button>
            </div>
        </section>
    @elseif ($pendingCount > 0)
        <flux:button variant="primary" icon="forward" :href="route('admin.submissions.next')" wire:navigate class="self-end">Siguiente sin corregir</flux:button>
    @endif

    @if ($previous->isNotEmpty())
        <details class="panel p-5">
            <summary class="cursor-pointer font-medium text-white">Intentos anteriores ({{ $previous->count() }})</summary>
            <ul class="mt-3 flex flex-col gap-2 text-sm">
                @foreach ($previous as $item)
                    <li class="flex flex-wrap items-center gap-2">
                        <a href="{{ route('admin.submissions.show', $item) }}" wire:navigate class="text-primary-bright hover:underline">Intento {{ $item->attempt }}</a>
                        <span class="text-ink-muted">{{ $item->submitted_at->format('d/m/Y H:i') }}</span>
                        <flux:badge size="sm" :color="['submitted' => 'amber', 'approved' => 'green', 'redo' => 'red'][$item->status->value]">{{ $item->status->label() }}</flux:badge>
                    </li>
                @endforeach
            </ul>
        </details>
    @endif
</div>
