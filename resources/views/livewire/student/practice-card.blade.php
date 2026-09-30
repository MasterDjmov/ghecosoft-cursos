@php
    use App\Enums\SubmissionMode;

    $coinName = $practice->is_required ? term('coin.course', $course, $practice->coin_reward) : term('coin.wildcard', null, $practice->coin_reward);
    $statusBadge = [
        'approved' => ['Aprobada', 'green'],
        'submitted' => ['Esperando corrección', 'amber'],
        'redo' => ['Rehacer', 'red'],
    ];
    // Los mismos colores que la leyenda del árbol.
    $statusColor = ['approved' => '#10b981', 'submitted' => '#f59e0b', 'redo' => '#f87171'][$status] ?? '#475569';
    $statusIcon = ['approved' => 'check-circle', 'submitted' => 'clock', 'redo' => 'arrow-path'][$status] ?? null;
    $canSubmit = $blocker === null;
    $showMark = ! $usesCode && $status !== 'approved';
    $fileHint = 'Archivo'.($practice->allowed_extensions ? ' ('.$practice->allowed_extensions.')' : '').($usesCode ? ' (opcional si entregás código)' : '');
@endphp

<article id="practica-{{ $practice->id }}" data-test="practice-{{ $practice->id }}"
    class="panel scroll-mt-20 overflow-hidden border-s-4 {{ $practice->is_required ? '' : 'border-dashed border-[#a855f7]/60' }}"
    style="border-inline-start-color: {{ $statusColor }}">

    {{-- Fila de una línea: abre y cierra la práctica. --}}
    <button type="button" class="flex w-full items-center gap-3 px-6 py-4 text-start transition hover:bg-surface-high/40"
        x-on:click="togglePractice({{ $practice->id }})"
        x-bind:aria-expanded="openPractice === {{ $practice->id }}" aria-controls="practica-{{ $practice->id }}-body">
        @if ($statusIcon)
            <flux:icon :name="$statusIcon" variant="mini" class="shrink-0" style="color: {{ $statusColor }}" />
        @else
            <span class="size-5 shrink-0 rounded-full border-2 border-[#475569]" aria-hidden="true"></span>
        @endif
        <h3 class="min-w-0 truncate font-medium text-white">{{ $practice->title }}</h3>
        <flux:badge size="sm" class="shrink-0" :color="$statusBadge[$status][1] ?? 'zinc'">{{ $statusBadge[$status][0] ?? 'Sin hacer' }}</flux:badge>
        <x-attempts :count="$attempts->count()" />
        @if ($isLocal)
            <flux:badge size="sm" class="hidden shrink-0 sm:inline-flex" icon="computer-desktop" title="{{ $practice->environment->hint($mode) }}">Local</flux:badge>
        @endif
        <span class="min-w-0 flex-1">
            @if ($lastFeedback)
                <span class="hidden truncate text-xs text-ink-muted italic md:block" x-show="openPractice !== {{ $practice->id }}">
                    <span class="not-italic text-primary-bright">El profe:</span> {{ Str::limit($lastFeedback->body, 120) }}
                </span>
            @endif
        </span>
        <span class="hidden shrink-0 font-mono text-xs text-ink-muted sm:inline">
            @if ($practice->coin_reward > 0) +{{ $practice->coin_reward }} {{ $coinName }} · @endif
            +{{ $practice->xp_reward }} {{ term('xp.short') }}
        </span>
        <flux:icon name="chevron-down" variant="micro" class="shrink-0 text-ink-muted transition"
            x-bind:class="openPractice === {{ $practice->id }} && 'rotate-180'" />
    </button>

    <div id="practica-{{ $practice->id }}-body" x-show="openPractice === {{ $practice->id }}" x-collapse x-cloak>
        <div class="flex flex-col gap-5 px-6 pb-6">
            <p class="font-mono text-xs text-ink-muted sm:hidden">
                @if ($practice->coin_reward > 0) +{{ $practice->coin_reward }} {{ $coinName }} · @endif
                +{{ $practice->xp_reward }} {{ term('xp.short') }}
            </p>

            @if ($usesCode || ! $practice->is_required)
                <div class="flex flex-wrap items-center justify-between gap-3">
                    @unless ($practice->is_required)
                        <x-companion key="companion.guild" :course="$course" color="text-secondary-bright" />
                    @endunless
                    @if ($usesCode)
                        <flux:button size="sm" icon="arrows-pointing-out" class="ms-auto hidden lg:inline-flex" data-test="enter-mission"
                            :href="route('student.mission', [$course, $practice->node_id, $practice])" wire:navigate>Entrar a la misión</flux:button>
                    @endif
                </div>
            @endif

            @if ($instructionsHtml)
                <div class="markdown text-sm">{!! $instructionsHtml !!}</div>
            @endif

            @if ($criteriaHtml)
                <div class="rounded-lg border border-success/30 bg-success/5 px-4 py-3" data-test="criteria">
                    <p class="tech-label mb-1 flex items-center gap-2 text-success"><flux:icon name="clipboard-document-check" variant="micro" /> Para aprobar</p>
                    <div class="markdown text-sm">{!! $criteriaHtml !!}</div>
                </div>
            @endif

            @if ($isLocal)
                <flux:callout icon="computer-desktop" color="zinc">
                    <flux:callout.text>{{ $practice->environment->hint($mode) }}</flux:callout.text>
                </flux:callout>
            @endif

            {{-- Historial de intentos y comentarios (antes del editor: primero la devolución, después rehacer). --}}
            @if ($attempts->isNotEmpty() && $mode !== SubmissionMode::None)
                <details class="flex flex-col gap-3 rounded-lg border border-outline bg-surface-lowest/40 px-4 py-3"
                    @if ($latest && $latest->status->value !== 'submitted' && $latest->comments->isNotEmpty()) open @endif>
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
                                        <x-emoji-field class="flex-1"><flux:textarea class="pe-10" wire:model="comment" rows="1" placeholder="Escribile al profe…" aria-label="Comentario" /></x-emoji-field>
                                        <flux:button type="submit" size="sm" icon="paper-airplane" aria-label="Enviar comentario" />
                                    </form>
                                    <flux:error name="comment" />
                                @endif
                            </li>
                        @endforeach
                    </ol>
                </details>
            @endif

            {{-- Pie: estado o intentos a la izquierda; acciones a la derecha. --}}
            @php
                $footerStatus = match (true) {
                    $status === 'approved' => $mode === SubmissionMode::None ? 'Completada' : 'Aprobada en el intento '.$attempts->firstWhere('status.value', 'approved')?->attempt,
                    $status === 'submitted' => 'Intento '.$latest->attempt.' entregado · esperando corrección',
                    $status === 'redo' => 'Intento '.$latest->attempt.': el profe te pidió rehacerla',
                    default => $mode === SubmissionMode::None ? 'Sin completar' : 'Sin entregas todavía',
                };
            @endphp

            @if ($usesCode)
                <x-code-runner :code="$startingCode" :stdin="$practice->sample_input" :expected="$practice->expected_output" :language="$course->language->value"
                    :name="'practica_'.$number" :read-only="! $canSubmit" :runnable="! $isLocal" wire:key="editor-{{ $practice->id }}-{{ $latest?->id }}">
                    <x-slot:footer>
                        @if ($canSubmit && $usesFile)
                            @include('livewire.student.partials.practice-file', ['hint' => $fileHint])
                        @endif
                        @include('livewire.student.partials.practice-footer', ['submitDisabled' => $usesFile ? "code.trim() === '' && ! \$wire.file" : "code.trim() === ''"])
                    </x-slot:footer>
                </x-code-runner>
            @elseif ($usesFile && $canSubmit)
                <form wire:submit="submit" class="flex flex-col gap-5">
                    @include('livewire.student.partials.practice-file', ['hint' => $fileHint])
                    @include('livewire.student.partials.practice-footer', ['submitDisabled' => null])
                </form>
            @else
                @include('livewire.student.partials.practice-footer', ['submitDisabled' => null])
            @endif
        </div>
    </div>
</article>
