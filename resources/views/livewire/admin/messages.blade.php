<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8" wire:poll.20s.visible>
    <header class="flex flex-wrap items-end justify-between gap-3">
        <div class="flex flex-col gap-1">
            <h1 class="font-display text-2xl font-semibold text-white">Mensajes</h1>
            <p class="text-sm text-ink-muted">Las consultas de los alumnos sobre cada práctica. Las que no leíste van primero.</p>
        </div>
        @if ($filteredStudent)
            <flux:button size="sm" variant="ghost" icon="x-mark" wire:click="$set('student', '')">Solo {{ $filteredStudent->fullName() }} · ver todos</flux:button>
        @endif
    </header>

    <div class="grid gap-4 lg:grid-cols-[minmax(0,2fr)_minmax(0,3fr)]">
        <section class="panel flex max-h-[75vh] flex-col overflow-y-auto p-2" aria-label="Conversaciones">
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
                    <span class="truncate text-xs text-ink-muted">{{ $item->practice->node->course->title }} · {{ $item->practice->node->title }} · {{ $item->practice->title }}</span>
                    <span class="line-clamp-2 text-xs text-ink">{{ $item->last->author_id === $item->student->id ? '' : 'Vos: ' }}{{ $item->last->body }}</span>
                </button>
            @empty
                <p class="p-6 text-center text-sm text-ink-muted">Todavía no llegó ninguna consulta.</p>
            @endforelse
        </section>

        <section class="panel flex flex-col gap-4 p-5" aria-label="Conversación">
            @if ($practice)
                <div class="flex flex-col gap-1">
                    <p class="tech-label">{{ $practice->node->course->title }} · {{ $practice->node->title }}</p>
                    <h2 class="font-display text-lg font-semibold text-white">{{ $practice->title }}</h2>
                    <p class="text-sm text-ink-muted">
                        <a href="{{ route('admin.students.show', $selectedStudent) }}" wire:navigate class="text-primary-bright hover:underline">{{ $selectedStudent->fullName() }}</a>
                        · <a href="{{ route('admin.nodes.edit', [$practice->node->course, $practice->node]) }}" wire:navigate class="hover:underline">ver la práctica</a>
                    </p>
                </div>
                <livewire:practice-chat :practice="$practice" :student="$selectedStudent" :key="'admin-chat-'.$thread" />
            @else
                <p class="py-10 text-center text-sm text-ink-muted">Elegí una conversación de la lista.</p>
            @endif
        </section>
    </div>
</div>
