@php
    use App\Enums\SubmissionMode;

    $coinName = $practice->is_required ? term('coin.course', $course, $practice->coin_reward) : term('coin.wildcard', null, $practice->coin_reward);
    $statusLabel = ['approved' => ['Aprobada', 'text-success border-success/50'], 'submitted' => ['Esperando corrección', 'text-warning border-warning/50'], 'redo' => ['Rehacer', 'text-[#fca5a5] border-[#f87171]/60']];
    $colors = ['approved' => '#10b981', 'submitted' => '#f59e0b', 'redo' => '#f87171'];
    $canSubmit = $blocker === null;
    // Una práctica "local" se resuelve en la compu del alumno: acá no se ejecuta.
    $canRun = $course->language->value === 'python' && ! $isLocal;
    $extension = ['python' => 'py', 'c' => 'c', 'cpp' => 'cpp', 'java' => 'java', 'javascript' => 'js', 'typescript' => 'ts', 'php' => 'php', 'sql' => 'sql', 'arduino' => 'ino'][$course->language->value] ?? 'txt';
    $submitDisabled = $usesFile ? "code.trim() === '' && ! \$wire.file" : "code.trim() === ''";
    $nodeUrl = route('student.node', [$course, $node]);
    $barButton = 'inline-flex items-center gap-1.5 rounded-md px-2 py-1 text-xs font-medium transition disabled:opacity-50';
@endphp

<div class="h-full">
    {{-- En pantallas chicas no hay modo misión: se sigue en la página del nodo. --}}
    <div class="flex h-full flex-col items-center justify-center gap-4 p-6 text-center lg:hidden">
        <flux:icon name="computer-desktop" class="size-10 text-primary-bright" />
        <p class="max-w-sm text-ink">El modo misión es para pantallas grandes. En el celular seguí la práctica desde la página del nodo.</p>
        <flux:button variant="primary" :href="$nodeUrl.'#practica-'.$practice->id" wire:navigate>Ir al nodo</flux:button>
    </div>

    <div class="hidden h-full flex-col lg:flex" data-test="mission"
        wire:key="mission-{{ $practice->id }}-{{ $latest?->id }}"
        x-data="codeRunner(@js([
            'code' => $startingCode, 'stdin' => (string) $practice->sample_input, 'expected' => (string) $practice->expected_output,
            'language' => $course->language->value, 'readOnly' => ! $canSubmit || ! $usesCode, 'runnable' => $canRun && $usesCode,
            'pyodideUrl' => config('services.pyodide.url'), 'timeout' => config('services.pyodide.timeout_ms'),
        ]))">

        {{-- A · Barra de misión --}}
        <header class="flex h-16 shrink-0 items-center gap-4 border-b border-outline bg-surface-lowest px-5">
            <a href="{{ $nodeUrl }}#practica-{{ $practice->id }}" wire:navigate class="flex shrink-0 items-center gap-1.5 text-sm text-ink-muted hover:text-white">
                <flux:icon name="chevron-left" variant="micro" /> Salir de la misión
            </a>
            <span class="h-7 w-px bg-outline"></span>
            <div class="flex min-w-0 flex-1 flex-col">
                <span class="tech-label truncate">{{ $course->title }} › {{ $node->title }}</span>
                <h1 class="truncate font-display text-lg font-semibold text-white">Misión {{ $number }} · {{ $practice->title }}</h1>
            </div>
            <span class="shrink-0 rounded-md border border-secondary-bright/60 px-2.5 py-1 font-mono text-xs text-[#c4b5fd]">+{{ $practice->xp_reward }} {{ term('xp.short') }}</span>
            @if ($practice->coin_reward > 0)
                <span class="shrink-0 rounded-md border border-[#b45309] px-2.5 py-1 font-mono text-xs text-[#fbbf24]">+{{ $practice->coin_reward }} {{ $coinName }}</span>
            @endif
            @if ($status)
                <span class="shrink-0 rounded-md border px-2.5 py-1 text-xs {{ $statusLabel[$status][1] }}" data-test="mission-status">{{ $statusLabel[$status][0] }}</span>
            @endif
            @if ($reviewNotice)
                <span class="inline-flex shrink-0 items-center gap-1 rounded-md border border-warning/50 px-2.5 py-1 text-xs text-warning" title="{{ $reviewNotice }}" data-test="review-notice">
                    <flux:icon name="moon" variant="micro" /> Fuera de horario
                </span>
            @endif

            @if ($canRun && $usesCode)
                <flux:button icon="play" x-on:click="run" x-bind:disabled="running" title="Ejecutar (Ctrl+Enter)">
                    <span x-text="running ? 'Ejecutando…' : 'Ejecutar'">Ejecutar</span>
                </flux:button>
            @endif
            @if ($canSubmit && $usesCode)
                <flux:button variant="primary" icon="paper-airplane" x-on:click="$wire.submit(code)"
                    x-bind:disabled="{{ $submitDisabled }}" wire:loading.attr="disabled" wire:target="file,submit" data-test="mission-submit">Entregar</flux:button>
            @elseif ($blocker && $status !== 'approved')
                <span class="flex max-w-xs items-center gap-1.5 text-xs text-ink-muted"><flux:icon name="information-circle" variant="micro" class="shrink-0" /> {{ $blocker }}</span>
            @endif
        </header>

        <div class="grid min-h-0 flex-1" style="grid-template-columns: auto minmax(0, 1fr){{ $showSide ? ' 300px' : '' }}">

            {{-- El estado del panel vive acá (no alrededor del editor: sus x-ref son de codeRunner). --}}
            <aside class="flex min-h-0 flex-col border-e border-outline bg-surface-low"
                x-data="{
                    panel: 'brief', left: true,
                    init() {
                        try { this.left = localStorage.getItem('mission-left') !== '0' } catch (e) {}
                        this.$watch('left', (v) => { try { localStorage.setItem('mission-left', v ? '1' : '0') } catch (e) {} })
                    },
                }"
                x-bind:class="left ? 'w-[360px]' : 'w-12'">
                <div class="flex shrink-0 items-center gap-1 border-b border-outline px-2" x-show="left">
                    @if ($chronicle)
                        <button type="button" x-on:click="panel = 'story'" class="-mb-px border-b-2 px-3 py-2.5 text-sm transition"
                            x-bind:class="panel === 'story' ? 'border-primary-bright font-semibold text-primary-bright' : 'border-transparent text-ink-muted hover:text-ink'">Historia</button>
                    @endif
                    <button type="button" x-on:click="panel = 'brief'" class="-mb-px border-b-2 px-3 py-2.5 text-sm transition"
                        x-bind:class="panel === 'brief' ? 'border-primary-bright font-semibold text-primary-bright' : 'border-transparent text-ink-muted hover:text-ink'">Consigna</button>
                    @if ($theory)
                        <button type="button" x-on:click="panel = 'theory'" class="-mb-px border-b-2 px-3 py-2.5 text-sm transition"
                            x-bind:class="panel === 'theory' ? 'border-primary-bright font-semibold text-primary-bright' : 'border-transparent text-ink-muted hover:text-ink'">Teoría</button>
                    @endif
                    <button type="button" x-on:click="left = false" class="ms-auto rounded p-1.5 text-ink-muted hover:bg-surface-high hover:text-ink" aria-label="Plegar el panel">
                        <flux:icon name="chevron-double-left" variant="micro" />
                    </button>
                </div>
                <button type="button" x-show="! left" x-cloak x-on:click="left = true" class="m-2 rounded p-1.5 text-ink-muted hover:bg-surface-high hover:text-ink" aria-label="Mostrar la consigna">
                    <flux:icon name="chevron-double-right" variant="micro" />
                </button>

                <div class="min-h-0 flex-1 overflow-y-auto p-5" x-show="left">
                    @if ($chronicle)
                        <div x-show="panel === 'story'" x-cloak class="markdown text-ink italic" data-test="mission-story">{!! $chronicle !!}</div>
                    @endif

                    <div x-show="panel === 'brief'" class="flex flex-col gap-4">
                        @unless ($practice->is_required)
                            <x-companion key="companion.guild" :course="$course" color="text-secondary-bright" />
                        @endunless
                        @if ($instructionsHtml)
                            <div class="markdown text-sm">{!! $instructionsHtml !!}</div>
                        @endif
                        @if ($criteriaHtml)
                            <div class="rounded-lg border border-success/30 bg-success/5 px-4 py-3">
                                <p class="tech-label mb-1 flex items-center gap-2 text-success"><flux:icon name="clipboard-document-check" variant="micro" /> Para aprobar</p>
                                <div class="markdown text-sm">{!! $criteriaHtml !!}</div>
                            </div>
                        @endif
                        @if ($isLocal)
                            <flux:callout icon="computer-desktop" color="zinc">
                                <flux:callout.text>{{ $practice->environment->hint($mode) }}</flux:callout.text>
                            </flux:callout>
                        @endif
                        @if ($canSubmit && $usesFile)
                            @include('livewire.student.partials.practice-file', ['hint' => 'Archivo'.($practice->allowed_extensions ? ' ('.$practice->allowed_extensions.')' : '').' (opcional si entregás código)'])
                        @endif
                    </div>

                    @if ($theory)
                        <div x-show="panel === 'theory'" x-cloak class="flex flex-col gap-6">
                            @isset ($theory['content'])
                                <x-node-section title="Explicación" icon="light-bulb" companion="companion.theory" :course="$course">
                                    <div class="markdown text-sm">{!! $theory['content'] !!}</div>
                                </x-node-section>
                            @endisset
                            @isset ($theory['uses'])
                                <x-node-section title="¿Para qué sirve?" icon="wrench-screwdriver" companion="companion.uses" :course="$course" color="text-warning">
                                    <div class="markdown text-sm">{!! $theory['uses'] !!}</div>
                                </x-node-section>
                            @endisset
                            @isset ($theory['errors'])
                                <x-node-section title="Errores habituales" icon="bug-ant" companion="companion.errors" :course="$course" color="text-danger">
                                    <div class="markdown text-sm">{!! $theory['errors'] !!}</div>
                                </x-node-section>
                            @endisset
                        </div>
                    @endif
                </div>

                {{-- Misiones del nodo: tocar una cambia de archivo sin salir --}}
                <nav class="shrink-0 border-t border-outline p-4" x-show="left" aria-label="Misiones del nodo">
                    <p class="tech-label mb-2">Misiones del nodo · {{ collect($statuses)->filter(fn ($s) => $s === 'approved')->count() }} de {{ $practices->count() }}</p>
                    <ul class="flex flex-col gap-1.5">
                        @foreach ($practices as $item)
                            @php
                                $itemStatus = $statuses[$item->id] ?? null;
                                $itemCodes = in_array($item->submission_mode, [SubmissionMode::Code, SubmissionMode::Both], true);
                                $href = $itemCodes ? route('student.mission', [$course, $node, $item]) : $nodeUrl.'#practica-'.$item->id;
                            @endphp
                            <li>
                                <a href="{{ $href }}" wire:navigate @class([
                                    'flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm transition hover:bg-surface-high',
                                    'border-s-4 bg-surface-container' => $item->is_required,
                                    'border border-dashed border-secondary/70' => ! $item->is_required,
                                    'ring-1 ring-primary-bright font-semibold text-white' => $item->id === $practice->id,
                                ]) style="{{ $item->is_required ? 'border-inline-start-color: '.($colors[$itemStatus] ?? '#475569') : '' }}"
                                    @if ($item->id === $practice->id) aria-current="page" @endif>
                                    <span class="min-w-0 flex-1 truncate">{{ $loop->iteration }} · {{ $item->title }}</span>
                                    <x-attempts :count="$attemptCounts[$item->id] ?? 0" />
                                    <span class="shrink-0 text-xs" style="color: {{ $colors[$itemStatus] ?? '#94a3b8' }}">
                                        {{ ['approved' => 'Aprobada', 'submitted' => 'En corrección', 'redo' => 'Rehacer'][$itemStatus] ?? ($item->is_required ? 'Pendiente' : 'Optativa') }}
                                    </span>
                                </a>
                            </li>
                        @endforeach
                    </ul>
                </nav>
            </aside>

            {{-- C y D · Editor y consola --}}
            <main class="flex min-h-0 min-w-0 flex-col gap-3 p-4">
                @if ($usesCode)
                    <section class="code-window flex min-h-0 flex-1 flex-col overflow-hidden rounded-lg border border-outline bg-surface-lowest focus-within:border-primary-bright/60">
                        <div class="flex shrink-0 items-center gap-2 border-b border-outline bg-surface-low px-3 py-1.5">
                            <span class="flex items-center gap-1.5 pe-1" aria-hidden="true">
                                <span class="size-2.5 rounded-full bg-[#f87171]/70"></span>
                                <span class="size-2.5 rounded-full bg-[#f59e0b]/70"></span>
                                <span class="size-2.5 rounded-full bg-[#10b981]/70"></span>
                            </span>
                            <span class="min-w-0 truncate font-mono text-xs text-ink">practica_{{ $number }}.{{ $extension }}</span>
                            <span class="tech-label">{{ $course->language->label() }}</span>
                            @unless ($canSubmit)
                                <flux:icon name="lock-closed" variant="micro" class="text-ink-muted" aria-label="Solo lectura" />
                            @endunless
                            <div class="ms-auto flex items-center gap-1">
                                @if ($canSubmit)
                                    <button type="button" x-on:click="restore" x-show="code !== original" x-cloak class="{{ $barButton }} text-ink-muted hover:bg-surface-high hover:text-ink">
                                        <flux:icon name="arrow-uturn-left" variant="micro" /> Restaurar
                                    </button>
                                @endif
                                <button type="button" x-on:click="copy" class="{{ $barButton }} text-ink-muted hover:bg-surface-high hover:text-ink">
                                    <flux:icon name="clipboard" variant="micro" /> <span x-text="copied ? '¡Copiado!' : 'Copiar'">Copiar</span>
                                </button>
                            </div>
                        </div>
                        <div x-ref="editor" wire:ignore class="mission-editor min-h-0 flex-1 overflow-hidden">
                            <pre class="code-window-fallback p-3 font-mono text-sm whitespace-pre-wrap text-ink">{{ $startingCode }}</pre>
                        </div>
                    </section>

                    @if ($canRun)
                        <x-code-console :expected="$practice->expected_output" fill class="h-56 shrink-0 overflow-hidden rounded-lg border border-outline" />
                    @elseif (filled($practice->expected_output))
                        <div class="shrink-0 rounded-lg border border-outline bg-surface-lowest p-3">
                            <p class="tech-label mb-1">Salida esperada</p>
                            <pre class="max-h-40 overflow-auto font-mono text-sm whitespace-pre-wrap text-ink-muted">{{ $practice->expected_output }}</pre>
                        </div>
                    @endif
                @else
                    <div class="panel flex flex-1 flex-col items-center justify-center gap-3 p-8 text-center text-ink-muted">
                        <p>Esta misión no se resuelve en el editor.</p>
                        <flux:button :href="$nodeUrl.'#practica-'.$practice->id" wire:navigate>Seguirla en el nodo</flux:button>
                    </div>
                @endif
            </main>

            {{-- E · Devolución del profe (solo si hay) --}}
            @if ($showSide)
                <aside class="flex min-h-0 flex-col gap-4 overflow-y-auto border-s border-outline bg-surface-low p-4" data-test="mission-feedback">
                    <h2 class="font-display font-semibold text-white">Devolución del profe</h2>
                    @if ($lastFeedback)
                        <div class="rounded-lg border border-primary-bright/40 bg-primary/10 p-3">
                            <p class="text-xs text-ink-muted">{{ $lastFeedback->created_at->format('d/m H:i') }}</p>
                            <p class="text-sm text-ink">{!! nl2br(e($lastFeedback->body)) !!}</p>
                        </div>
                    @endif

                    <div class="flex flex-col gap-2">
                        <p class="tech-label">Intentos</p>
                        @foreach ($attempts as $attempt)
                            <div class="flex items-center justify-between text-sm" wire:key="side-attempt-{{ $attempt->id }}">
                                <span>Intento {{ $attempt->attempt }} <span class="text-xs text-ink-muted">· {{ $attempt->submitted_at->format('d/m H:i') }}</span></span>
                                <span class="text-xs" style="color: {{ $colors[$attempt->status->value] }}">{{ $statusLabel[$attempt->status->value][0] }}</span>
                            </div>
                        @endforeach
                    </div>

                    @if ($latest)
                        <div class="mt-auto flex flex-col gap-2 border-t border-outline pt-3">
                            @foreach ($latest->comments->reject(fn ($c) => $c->id === $lastFeedback?->id) as $item)
                                <div @class(['rounded-md p-2 text-sm', 'border-s-2 border-primary-bright bg-primary/10' => $item->user->isAdmin(), 'bg-surface-high' => ! $item->user->isAdmin()])>
                                    <p class="text-xs text-ink-muted">{{ $item->user->isAdmin() ? 'El profe' : 'Vos' }} · {{ $item->created_at->format('d/m H:i') }}</p>
                                    <p class="text-ink">{!! nl2br(e($item->body)) !!}</p>
                                </div>
                            @endforeach
                            <form wire:submit="addComment({{ $latest->id }})" class="flex items-end gap-2">
                                <flux:textarea wire:model="comment" rows="1" placeholder="Escribile al profe…" class="flex-1" aria-label="Comentario" />
                                <flux:button type="submit" size="sm" icon="paper-airplane" aria-label="Enviar comentario" />
                            </form>
                            <flux:error name="comment" />
                        </div>
                    @endif
                </aside>
            @endif
        </div>
    </div>
</div>
