<div class="mx-auto flex w-full max-w-7xl flex-col gap-6 p-4 sm:p-8" wire:poll.20s.visible>
    <header class="flex flex-wrap items-end justify-between gap-3">
        <div class="flex flex-col gap-1">
            <h1 class="font-display text-2xl font-semibold text-white">Mensajes</h1>
            <p class="text-sm text-ink-muted">Las consultas de los alumnos sobre cada práctica y cada micro-misión. Las que no leíste van primero.</p>
        </div>
        @if ($filteredStudent)
            <flux:button size="sm" variant="ghost" icon="x-mark" wire:click="$set('student', '')">Solo {{ $filteredStudent->fullName() }} · ver todos</flux:button>
        @endif
    </header>

    <div class="grid gap-4 lg:grid-cols-[minmax(0,2fr)_minmax(0,5fr)]">
        <section class="panel flex max-h-[80vh] flex-col overflow-y-auto p-2" aria-label="Conversaciones">
            @forelse ($threads as $item)
                <button type="button" wire:click="open('{{ $item->key }}')" wire:key="thread-{{ $item->key }}" data-test="thread-{{ $item->key }}"
                    @class([
                        'flex flex-col gap-1 rounded-lg p-3 text-start transition hover:bg-surface-high',
                        'bg-primary/10 ring-1 ring-primary-bright/60' => $thread === $item->key,
                    ])>
                    <span class="flex items-center gap-2">
                        <span @class(['min-w-0 flex-1 truncate text-sm', 'font-semibold text-white' => $item->unread, 'text-ink' => ! $item->unread])>{{ $item->student->fullName() }}</span>
                        @if ($item->unread)
                            <span class="grid min-w-5 place-items-center rounded-full bg-danger px-1.5 font-mono text-[11px] font-bold text-white">{{ $item->unread }}</span>
                        @endif
                        <span class="shrink-0 text-[11px] text-ink-muted">{{ $item->last->created_at->diffForHumans(short: true) }}</span>
                    </span>
                    <span class="flex items-center gap-1.5 truncate text-xs text-ink-muted">
                        @if ($item->isStep)
                            <flux:badge size="sm" color="cyan">micro</flux:badge>
                        @endif
                        <span class="truncate">{{ $item->subject->node->course->title }} · {{ $item->subject->node->title }} · {{ $item->subject->title }}</span>
                    </span>
                    <span class="line-clamp-2 text-xs text-ink">{{ $item->last->author_id === $item->student->id ? '' : 'Vos: ' }}{{ $item->last->body }}</span>
                </button>
            @empty
                <p class="p-6 text-center text-sm text-ink-muted">Todavía no llegó ninguna consulta.</p>
            @endforelse
        </section>

        <section class="panel flex min-w-0 flex-col gap-4 p-5" aria-label="Conversación">
            @if ($subject)
                <div class="flex flex-col gap-1">
                    <p class="tech-label">{{ $subject->node->course->title }} · {{ $subject->node->title }} · {{ $isStep ? 'micro-misión '.$subject->code : 'práctica' }}</p>
                    <h2 class="font-display text-lg font-semibold text-white">{{ $subject->title }}</h2>
                    <p class="text-sm text-ink-muted">
                        <a href="{{ route('admin.students.show', $selectedStudent) }}" wire:navigate class="text-primary-bright hover:underline">{{ $selectedStudent->fullName() }}</a>
                        · <a href="{{ route('admin.nodes.edit', [$subject->node->course, $subject->node]) }}" wire:navigate class="hover:underline">ver el nodo</a>
                    </p>
                </div>

                {{-- D110: todo para ayudar sin salir del chat: la consigna, su código y la solución, con «Ejecutar». --}}
                <div class="flex flex-col gap-3" wire:key="context-{{ $thread }}" data-test="message-context">
                    @if (filled($context['challenge']))
                        <details class="rounded-lg border border-outline/70 px-3 py-2 text-sm" open>
                            <summary class="cursor-pointer text-ink-muted">{{ $isStep ? 'El desafío' : 'La consigna' }}</summary>
                            <div class="markdown mt-2 text-ink">{!! \Illuminate\Support\Str::markdown($context['challenge'], ['html_input' => 'escape']) !!}</div>
                        </details>
                    @endif
                    <div class="grid gap-3 xl:grid-cols-2">
                        <div class="flex min-w-0 flex-col gap-1">
                            <p class="text-xs font-medium text-ink">Su código
                                <span class="font-normal text-ink-muted">{{ $context['studentCodeFrom'] ? '('.$context['studentCodeFrom'].')' : '' }}</span></p>
                            @if (filled($context['studentCode']))
                                <x-code-runner :code="$context['studentCode']" :stdin="$context['stdin']" :expected="$context['expected']" :checks="$context['checks']"
                                    :language="$context['language']" name="alumno" :read-only="true" data-test="message-student-code" />
                            @else
                                <p class="rounded-lg border border-dashed border-outline p-3 text-xs text-ink-muted">No mandó código con la consulta ni lo resolvió todavía.</p>
                            @endif
                        </div>
                        <div class="flex min-w-0 flex-col gap-1">
                            <p class="text-xs font-medium text-ink">La solución <span class="font-normal text-ink-muted">(el alumno no la ve)</span></p>
                            @if (filled($context['solution']))
                                <x-code-runner :code="$context['solution']" :stdin="$context['stdin']" :expected="$context['expected']" :checks="$context['checks']"
                                    :language="$context['language']" name="solucion" :read-only="true" data-test="message-solution" />
                            @else
                                <p class="rounded-lg border border-dashed border-outline p-3 text-xs text-ink-muted">Esta {{ $isStep ? 'micro-misión' : 'práctica' }} no tiene solución cargada.</p>
                            @endif
                        </div>
                    </div>
                </div>

                <livewire:practice-chat :practice="$isStep ? null : $subject" :step="$isStep ? $subject : null" :student="$selectedStudent" :key="'admin-chat-'.$thread" />
            @else
                <p class="py-10 text-center text-sm text-ink-muted">Elegí una conversación de la lista.</p>
            @endif
        </section>
    </div>
</div>
