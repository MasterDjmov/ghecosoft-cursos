{{-- El árbol de un alumno en un curso: colores de avance, sin links ni contenido; debajo, los nodos que siguen. --}}
<div class="mx-auto flex w-full max-w-6xl flex-col gap-4 p-4 sm:p-8">
    <a href="{{ $canSeeFile ? route('admin.students.show', $user) : route('admin.students.index') }}" wire:navigate
        class="inline-flex items-center gap-1.5 self-start text-sm text-ink-muted hover:text-white">
        <flux:icon name="chevron-left" variant="micro" /> {{ $canSeeFile ? 'Volver a la ficha de '.$user->fullName() : 'Volver a Alumnos' }}
    </a>
    <header class="flex flex-col gap-4 sm:flex-row sm:items-center">
        <x-course-logo :course="$course" size="size-16" />
        <div class="flex min-w-0 flex-col gap-1">
            <p class="tech-label">Árbol de {{ $user->fullName() }}</p>
            <h1 class="font-display text-2xl font-semibold text-white">{{ $course->title }}</h1>
            <p class="text-sm text-ink-muted">
                {{ $completed }}/{{ $total }} {{ term('node', $course, $total) }} del camino principal · los de color son los que recorrió
            </p>
        </div>
    </header>

    <section class="relative h-[75vh] min-h-[460px] overflow-hidden rounded-lg border border-outline bg-[#05070d]/90"
        x-data="skillTree(@js($graph), { readOnly: true })" wire:ignore data-test="student-progress-tree">
        <div x-ref="canvas" class="absolute inset-0"></div>
        @include('livewire.student.partials.tree-legend')
        <div class="absolute bottom-3 left-3">
            <flux:button size="xs" icon="arrows-pointing-out" x-on:click="fit">Ver todo</flux:button>
        </div>
    </section>

    {{-- D107: el recorrido capítulo por capítulo: qué miró, cuántas veces probó y dónde se traba. --}}
    <section class="panel flex flex-col gap-3 p-5" data-test="student-journey">
        <div>
            <h2 class="font-display font-semibold text-white">Recorrido</h2>
            <p class="text-sm text-ink-muted">Los {{ term('node', $course, 2) }} que abrió o miró. «Trabado»: una micro-misión con {{ \App\Support\StudentJourney::STUCK_FAILS }} fallos o más sin acertarla, o {{ \App\Support\StudentJourney::STUCK_DAYS }} días sin avanzar. Las visitas y los fallos se registran desde el 15/10/2026.</p>
        </div>
        @forelse ($chapters as $chapter)
            <details class="border-t border-outline/60 pt-3" wire:key="chapter-{{ $chapter['id'] }}" @if ($chapter['stuck_steps']->isNotEmpty() || $chapter['idle_since']) open @endif>
                <summary class="flex cursor-pointer flex-col gap-1 sm:flex-row sm:items-center sm:gap-3">
                    <span class="flex min-w-0 flex-1 items-center gap-2 font-medium text-ink">
                        @if ($chapter['completed'])
                            <flux:icon name="check-circle" variant="micro" class="shrink-0 text-success" />
                        @elseif ($chapter['stuck_steps']->isNotEmpty() || $chapter['idle_since'])
                            <flux:icon name="exclamation-triangle" variant="micro" class="shrink-0 text-warning" />
                        @else
                            <flux:icon name="play-circle" variant="micro" class="shrink-0 text-primary-bright" />
                        @endif
                        <span class="truncate">{{ $chapter['title'] }}</span>
                        @if ($chapter['code'])<span class="font-mono text-xs text-ink-muted">{{ $chapter['code'] }}</span>@endif
                    </span>
                    <span class="flex flex-wrap gap-x-3 font-mono text-xs text-ink-muted">
                        @if ($chapter['steps']->isNotEmpty())
                            <span>{{ $chapter['steps_done'] }}/{{ $chapter['steps']->count() }} micro-misiones</span>
                        @endif
                        <span @class(['text-warning' => $chapter['fails'] > 0])>{{ $chapter['fails'] }} {{ $chapter['fails'] === 1 ? 'fallo' : 'fallos' }}</span>
                        <span>{{ $chapter['days'] ? 'entró '.$chapter['days'].' '.($chapter['days'] === 1 ? 'día' : 'días') : 'sin visitas registradas' }}</span>
                        @if ($chapter['last_seen'])<span>última {{ $chapter['last_seen']->format('d/m H:i') }}</span>@endif
                    </span>
                </summary>
                <div class="mt-2 flex flex-col gap-1 pl-6 text-sm">
                    <p class="text-xs text-ink-muted">
                        @if ($chapter['unlocked_at'])Abierto el {{ $chapter['unlocked_at']->format('d/m/Y') }}.@endif
                        @if ($chapter['first_seen']) Lo miró por primera vez el {{ $chapter['first_seen']->format('d/m/Y H:i') }} ({{ $chapter['views'] }} {{ $chapter['views'] === 1 ? 'vez' : 'veces' }}).@endif
                        @if ($chapter['idle_since'])<span class="text-warning"> Sin avanzar desde el {{ $chapter['idle_since']->format('d/m/Y') }}.</span>@endif
                    </p>
                    @foreach ($chapter['steps'] as $step)
                        <div class="flex items-center gap-2" wire:key="journey-step-{{ $step['id'] }}">
                            @if ($step['done'])
                                <flux:icon name="check" variant="micro" class="shrink-0 text-success" />
                            @elseif ($step['stuck'])
                                <flux:icon name="exclamation-triangle" variant="micro" class="shrink-0 text-warning" />
                            @else
                                <flux:icon name="minus" variant="micro" class="shrink-0 text-ink-muted" />
                            @endif
                            <span @class(['flex-1 truncate', 'text-warning' => $step['stuck'], 'text-ink' => ! $step['stuck']])>{{ $step['title'] }}</span>
                            @if ($step['fails'])
                                <span class="font-mono text-xs text-ink-muted">{{ $step['fails'] }} {{ $step['fails'] === 1 ? 'fallo' : 'fallos' }}</span>
                            @endif
                        </div>
                    @endforeach
                </div>
            </details>
        @empty
            <flux:text>Todavía no abrió ni miró ningún {{ term('node', $course) }}.</flux:text>
        @endforelse

        @if ($recentFails->isNotEmpty())
            <div class="flex flex-col gap-2 border-t border-outline/60 pt-3" data-test="student-recent-fails">
                <h3 class="tech-label">Últimas respuestas equivocadas</h3>
                @foreach ($recentFails as $fail)
                    <div class="flex flex-col gap-0.5 text-sm sm:flex-row sm:items-baseline sm:gap-3" wire:key="fail-{{ $fail->id }}">
                        <span class="shrink-0 font-mono text-xs text-ink-muted">{{ $fail->created_at->format('d/m H:i') }}</span>
                        <span class="shrink-0 text-ink-muted">{{ $fail->step?->title }}</span>
                        <span class="min-w-0 flex-1 truncate font-mono text-warning" title="{{ $fail->answer }}">{{ $fail->answer ?? '—' }}</span>
                        @if ($fail->kind)<span class="shrink-0 font-mono text-xs text-ink-muted">{{ $fail->kindLabel() }}</span>@endif
                    </div>
                @endforeach
            </div>
        @endif
    </section>

    {{-- D95: prácticas que esperan micro-misiones; si se traba (sin ejecutor de Java, por ejemplo), se las abrís. --}}
    @if ($lockedPractices->isNotEmpty())
        <section class="panel flex flex-col gap-3 p-5" data-test="student-locked-practices">
            <div>
                <h2 class="font-display font-semibold text-white">{{ ucfirst(term('practice', $course, 2)) }} que esperan micro-misiones</h2>
                <p class="text-sm text-ink-muted">Las ve al superar las micro-misiones del {{ term('node', $course) }}. Si se traba, abríselas: las micro-misiones le quedan para después.</p>
            </div>
            @foreach ($lockedPractices as $item)
                <div class="flex flex-col gap-2 border-t border-outline/60 pt-3 sm:flex-row sm:items-center" wire:key="locked-{{ $item['id'] }}">
                    <span class="flex-1 font-medium text-ink">{{ $item['title'] }} <span class="font-mono text-xs text-ink-muted">· {{ $item['done'] }} de {{ $item['total'] }} micro-misiones</span></span>
                    <flux:button size="sm" icon="lock-open" wire:click="grantPractices({{ $item['id'] }})" data-test="grant-practices-{{ $item['id'] }}"
                        wire:confirm="¿Abrirle las {{ term('practice', $course, 2) }} de «{{ $item['title'] }}» a {{ $user->name }} sin que termine las micro-misiones?">Abrirle las {{ term('practice', $course, 2) }}</flux:button>
                </div>
            @endforeach
        </section>
    @endif

    {{-- Lo que sigue: si se traba, se lo abrís con sus monedas (mismas reglas que si lo abriera él). --}}
    <section class="panel flex flex-col gap-3 p-5" data-test="student-next-nodes">
        <div>
            <h2 class="font-display font-semibold text-white">Lo que sigue</h2>
            <p class="text-sm text-ink-muted">Los {{ term('node', $course, 2) }} que vienen después de lo que abrió. Si se traba, abriselo vos: se paga con sus monedas, con las mismas reglas, y le llega un aviso.</p>
        </div>
        @forelse ($next as $item)
            <div class="flex flex-col gap-2 border-t border-outline/60 pt-3 sm:flex-row sm:items-center" wire:key="next-{{ $item['id'] }}">
                <div class="flex min-w-0 flex-1 flex-col gap-0.5">
                    <span class="font-medium text-ink">{{ $item['title'] }} <span class="font-mono text-xs text-ink-muted">· {{ $item['price'] }}</span></span>
                    @if ($item['reasons'])
                        <span class="flex items-start gap-1.5 text-xs text-warning"><flux:icon name="lock-closed" variant="micro" class="mt-0.5 shrink-0" /> {{ implode(' ', $item['reasons']) }}</span>
                    @else
                        <span class="text-xs text-success">Lo puede abrir ya.</span>
                    @endif
                </div>
                @unless ($item['reasons'])
                    <flux:button size="sm" variant="primary" icon="lock-open" wire:click="unlockFor({{ $item['id'] }})" data-test="unlock-for-{{ $item['id'] }}"
                        wire:confirm="¿Abrirle «{{ $item['title'] }}» a {{ $user->name }}? Se paga con {{ $item['price'] }} de su saldo.">Abrírselo</flux:button>
                @endunless
            </div>
        @empty
            <flux:text>No tiene {{ term('node', $course, 2) }} cerrados a continuación: abrió todo lo que tenía disponible o terminó el curso.</flux:text>
        @endforelse
    </section>

    {{-- D103: restaurar el avance (solo el administrador): abrir, micro-misiones y prácticas, de a una o el nodo entero. --}}
    @if ($restoreRows)
        <section class="panel flex flex-col gap-3 p-5" data-test="restore-progress">
            <div>
                <h2 class="font-display font-semibold text-white">Restaurar avance</h2>
                <p class="text-sm text-ink-muted">
                    Para devolverle lo que ya tenía hecho. Va en el orden del árbol (primero el padre) y paga lo mismo que si lo hubiera hecho él:
                    {{ term('coin.course', $course, 2) }}, XP, oro e insignias. El {{ term('node', $course) }} se cobra si le alcanza el saldo; si no, se abre sin cobrar.
                    Las {{ term('practice', $course, 2) }} quedan aprobadas sin entrega.
                </p>
            </div>
            @foreach ($restoreRows as $row)
                <details class="group border-t border-outline/60 pt-2" wire:key="restore-{{ $row['id'] }}" style="margin-left: {{ min($row['depth'], 6) * 0.75 }}rem">
                    <summary class="flex cursor-pointer list-none flex-wrap items-center gap-2 py-1">
                        <flux:icon name="chevron-right" variant="micro" class="text-ink-muted transition group-open:rotate-90" />
                        @if ($row['complete'])
                            <flux:icon name="check-circle" variant="micro" class="text-success" />
                        @elseif ($row['unlocked'])
                            <flux:icon name="lock-open" variant="micro" class="text-warning" />
                        @else
                            <flux:icon name="lock-closed" variant="micro" class="text-ink-muted" />
                        @endif
                        <span class="flex-1 font-medium text-ink">
                            @if ($row['code'])<span class="font-mono text-xs text-ink-muted">{{ $row['code'] }}</span>@endif
                            {{ $row['title'] }}
                            <span class="font-mono text-xs text-ink-muted">
                                · {{ $row['steps']->where('done', true)->count() }}/{{ $row['steps']->count() }} micro-misiones
                                · {{ $row['practices']->where('done', true)->count() }}/{{ $row['practices']->count() }} {{ term('practice', $course, 2) }}
                            </span>
                        </span>
                        @unless ($row['unlocked'])
                            <flux:button size="xs" icon="lock-open" wire:click="restoreUnlock({{ $row['id'] }})" data-test="restore-unlock-{{ $row['id'] }}">Abrir</flux:button>
                        @endunless
                        @unless ($row['complete'])
                            <flux:button size="xs" variant="primary" icon="check" wire:click="restoreNode({{ $row['id'] }})" data-test="restore-node-{{ $row['id'] }}"
                                wire:confirm="¿Darle por aprobado «{{ $row['title'] }}» entero a {{ $user->name }}? Se abre si hace falta, con todas sus micro-misiones y {{ term('practice', $course, 2) }} obligatorias.">Aprobar entero</flux:button>
                        @endunless
                    </summary>
                    <div class="flex flex-col gap-1 py-2 ps-6 text-sm">
                        @foreach ($row['steps'] as $step)
                            <div class="flex items-center gap-2" wire:key="restore-step-{{ $step['id'] }}">
                                <span class="flex-1 {{ $step['done'] ? 'text-success' : 'text-ink' }}">Micro-misión · {{ $step['title'] }}</span>
                                @if ($step['done'])
                                    <flux:icon name="check" variant="micro" class="text-success" />
                                @elseif ($row['unlocked'])
                                    <flux:button size="xs" variant="ghost" wire:click="restoreStep({{ $step['id'] }})" data-test="restore-step-{{ $step['id'] }}">Dar por superada</flux:button>
                                @endif
                            </div>
                        @endforeach
                        @foreach ($row['practices'] as $practice)
                            <div class="flex items-center gap-2" wire:key="restore-practice-{{ $practice['id'] }}">
                                <span class="flex-1 {{ $practice['done'] ? 'text-success' : 'text-ink' }}">
                                    {{ ucfirst(term('practice', $course)) }} · {{ $practice['title'] }}
                                    @unless ($practice['required'])<span class="text-xs text-ink-muted">(opcional)</span>@endunless
                                </span>
                                @if ($practice['done'])
                                    <flux:icon name="check" variant="micro" class="text-success" />
                                @elseif ($row['unlocked'])
                                    <flux:button size="xs" variant="ghost" wire:click="restorePractice({{ $practice['id'] }})" data-test="restore-practice-{{ $practice['id'] }}">Aprobar</flux:button>
                                @endif
                            </div>
                        @endforeach
                        @if ($row['steps']->isEmpty() && $row['practices']->isEmpty())
                            <span class="text-ink-muted">Sin micro-misiones ni {{ term('practice', $course, 2) }}: se completa al abrirlo.</span>
                        @endif
                        @unless ($row['unlocked'])
                            <span class="text-xs text-ink-muted">Abrilo para ir de a una.</span>
                        @endunless
                    </div>
                </details>
            @endforeach
        </section>
    @endif
</div>
