@php
    $coinName = $practice->is_required ? term('coin.course', $course, $practice->coin_reward) : term('coin.wildcard', null, $practice->coin_reward);
    $statusBadge = [
        'approved' => ['Aprobada', 'green'],
        'submitted' => ['Esperando corrección', 'amber'],
        'redo' => ['Rehacer', 'red'],
    ];
    $canSubmit = $blocker === null;
@endphp

<article id="practica-{{ $practice->id }}" class="panel flex scroll-mt-20 flex-col gap-4 p-5" data-test="practice-{{ $practice->id }}">
    <header class="flex flex-wrap items-center gap-2">
        <h3 class="font-medium text-white">{{ $practice->title }}</h3>
        <flux:badge size="sm" :color="$practice->is_required ? 'cyan' : 'violet'">{{ $practice->is_required ? 'Obligatoria' : 'Optativa' }}</flux:badge>
        @if ($status)
            <flux:badge size="sm" :color="$statusBadge[$status][1]">{{ $statusBadge[$status][0] }}</flux:badge>
        @endif
        <span class="ms-auto font-mono text-xs text-ink-muted">
            @if ($practice->coin_reward > 0) +{{ $practice->coin_reward }} {{ $coinName }} · @endif
            +{{ $practice->xp_reward }} {{ term('xp.short') }}
        </span>
    </header>

    @if ($instructionsHtml)
        <div class="markdown text-sm">{!! $instructionsHtml !!}</div>
    @endif

    {{-- Entregar --}}
    @if ($mode === \App\Enums\SubmissionMode::None)
        <div class="flex flex-wrap items-center gap-3">
            @if ($status === 'approved')
                <p class="flex items-center gap-2 text-sm text-success"><flux:icon name="check-circle" variant="mini" /> Completada</p>
            @else
                <flux:button variant="primary" icon="check" wire:click="toggleMark" :disabled="! $canSubmit">Marcar como completada</flux:button>
                @if ($blocker)
                    <span class="text-xs text-ink-muted">{{ $blocker }}</span>
                @endif
            @endif
        </div>
    @else
        @if ($usesCode)
            <x-code-runner :code="$startingCode" :stdin="$practice->sample_input" :language="$course->language->value"
                :read-only="! $canSubmit" wire:key="editor-{{ $practice->id }}-{{ $latest?->id }}">
                <x-slot:actions>
                    @if ($canSubmit && ! $usesFile)
                        <flux:button size="sm" variant="primary" icon="paper-airplane" x-on:click="$wire.submit(code)" wire:loading.attr="disabled" wire:target="submit">Entregar</flux:button>
                    @endif
                </x-slot:actions>
                @if ($canSubmit && $usesFile)
                    <x-slot:footer>
                        <div class="flex flex-col gap-2">
                            <flux:label>Archivo{{ $practice->allowed_extensions ? ' ('.$practice->allowed_extensions.')' : '' }}{{ $usesCode ? ' (opcional si entregás código)' : '' }}</flux:label>
                            <input type="file" wire:model="file"
                                class="text-sm text-ink-muted file:me-3 file:rounded-md file:border-0 file:bg-surface-highest file:px-3 file:py-2 file:text-ink hover:file:bg-surface-high">
                            <div wire:loading wire:target="file" class="text-xs text-ink-muted">Subiendo…</div>
                            <flux:error name="file" />
                        </div>
                        <div>
                            <flux:button variant="primary" icon="paper-airplane" x-on:click="$wire.submit(code)" wire:loading.attr="disabled" wire:target="file,submit">Entregar</flux:button>
                        </div>
                    </x-slot:footer>
                @endif
            </x-code-runner>
        @elseif ($canSubmit)
            <form wire:submit="submit" class="flex flex-col gap-3">
                <div class="flex flex-col gap-2">
                            <flux:label>Archivo{{ $practice->allowed_extensions ? ' ('.$practice->allowed_extensions.')' : '' }}{{ $usesCode ? ' (opcional si entregás código)' : '' }}</flux:label>
                            <input type="file" wire:model="file"
                                class="text-sm text-ink-muted file:me-3 file:rounded-md file:border-0 file:bg-surface-highest file:px-3 file:py-2 file:text-ink hover:file:bg-surface-high">
                            <div wire:loading wire:target="file" class="text-xs text-ink-muted">Subiendo…</div>
                            <flux:error name="file" />
                        </div>
                <div>
                    <flux:button type="submit" variant="primary" icon="paper-airplane" wire:loading.attr="disabled" wire:target="file,submit">Entregar</flux:button>
                </div>
            </form>
        @endif

        @if ($blocker && $status !== 'approved')
            <p class="flex items-center gap-2 text-xs text-ink-muted"><flux:icon name="information-circle" variant="micro" /> {{ $blocker }}</p>
        @endif

        <div @class(['hidden' => $status === 'approved'])>
            <flux:button size="xs" variant="ghost" :icon="$marked ? 'check-circle' : 'check'" wire:click="toggleMark">
                {{ $marked ? 'Marcada como completada' : 'Marcar como completada' }}
            </flux:button>
        </div>
    @endif

    {{-- Historial de intentos y comentarios --}}
    @if ($attempts->isNotEmpty() && $mode !== \App\Enums\SubmissionMode::None)
        <details class="flex flex-col gap-3 border-t border-outline pt-3" @if ($latest && $latest->status->value !== 'submitted' && $latest->comments->isNotEmpty()) open @endif>
            <summary class="cursor-pointer text-sm text-ink-muted">Tus entregas ({{ $attempts->count() }})</summary>
            <ol class="mt-3 flex flex-col gap-4">
                @foreach ($attempts as $attempt)
                    <li class="flex flex-col gap-2 rounded-lg border border-outline bg-surface-lowest/60 p-3" wire:key="attempt-{{ $attempt->id }}">
                        <div class="flex flex-wrap items-center gap-2 text-xs">
                            <span class="font-mono text-ink">Intento {{ $attempt->attempt }}</span>
                            <span class="text-ink-muted">{{ $attempt->submitted_at->format('d/m/Y H:i') }}</span>
                            <flux:badge size="sm" :color="$statusBadge[$attempt->status->value][1]">{{ $statusBadge[$attempt->status->value][0] }}</flux:badge>
                            @if ($attempt->file_path)
                                <a href="{{ route('files.submission', $attempt) }}" class="flex items-center gap-1 text-primary-bright hover:underline">
                                    <flux:icon name="paper-clip" variant="micro" /> {{ $attempt->file_original_name }}
                                </a>
                            @endif
                        </div>
                        @if ($attempt->code && ! $loop->first)
                            <details class="text-xs">
                                <summary class="cursor-pointer text-ink-muted">Ver código</summary>
                                <pre class="mt-2 max-h-60 overflow-auto rounded border border-outline bg-[#05070d] p-2 font-mono text-ink">{{ $attempt->code }}</pre>
                            </details>
                        @endif
                        @foreach ($attempt->comments as $item)
                            <div @class(['rounded-md p-2 text-sm', 'bg-primary/10 border-s-2 border-primary-bright' => $item->user->isAdmin(), 'bg-surface-high' => ! $item->user->isAdmin()])>
                                <p class="text-xs text-ink-muted">{{ $item->user->isAdmin() ? 'El profe' : 'Vos' }} · {{ $item->created_at->format('d/m H:i') }}</p>
                                <p class="text-ink">{!! nl2br(e($item->body)) !!}</p>
                            </div>
                        @endforeach
                        @if ($loop->first)
                            <form wire:submit="addComment({{ $attempt->id }})" class="flex items-end gap-2">
                                <flux:textarea wire:model="comment" rows="1" placeholder="Escribile al profe…" class="flex-1" aria-label="Comentario" />
                                <flux:button type="submit" size="sm" icon="paper-airplane" aria-label="Enviar comentario" />
                            </form>
                            <flux:error name="comment" />
                        @endif
                    </li>
                @endforeach
            </ol>
        </details>
    @endif
</article>
