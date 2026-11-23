{{-- D124: Mis prácticas: lo guardado desde Herramientas → Practicar. --}}
<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-col gap-1">
        <p class="tech-label">Herramientas</p>
        <h1 class="font-display text-2xl font-semibold text-white">Mis prácticas</h1>
        <p class="text-sm text-ink-muted">
            Lo que guardaste en Practicar, el Gólem 8086 o la caja de la Feria, para seguirlo cuando quieras, también desde otra compu. Abrí una para continuar,
            bajar el archivo{{ $canConsult ? ' o preguntarle al profe sobre ese código' : '' }}. No cuenta para el curso.
        </p>
    </header>

    <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
        <flux:input wire:model.live.debounce.300ms="search" icon="magnifying-glass" placeholder="Buscar por nombre" class="sm:flex-1" aria-label="Buscar" />
        @if ($languages->count() > 1)
            <flux:select wire:model.live="language" class="sm:w-48" aria-label="Lenguaje">
                <flux:select.option value="">Todos los lenguajes</flux:select.option>
                @foreach ($languages as $key => $label)
                    <flux:select.option :value="$key">{{ $label }}</flux:select.option>
                @endforeach
            </flux:select>
        @endif
        @if ($tools->isNotEmpty())
            <flux:dropdown>
                <flux:button variant="primary" icon="plus" icon:trailing="chevron-down">Nueva</flux:button>
                <flux:menu>
                    @foreach ($tools as $tool)
                        <flux:menu.item :href="$tool['url']" wire:navigate>{{ $tool['label'] }}</flux:menu.item>
                    @endforeach
                </flux:menu>
            </flux:dropdown>
        @endif
    </div>

    @if ($practices->isEmpty())
        <div class="panel flex flex-col items-center gap-2 p-10 text-center" data-test="saved-practices-empty">
            <flux:icon name="bookmark" class="size-8 text-secondary-bright" />
            <p class="text-ink">{{ $total ? 'Ninguna práctica coincide con lo que buscás.' : 'Todavía no guardaste ninguna práctica.' }}</p>
            @unless ($total)
                <p class="text-sm text-ink-muted">Entrá a <strong>Practicar</strong>, al <strong>Gólem 8086</strong> o a <strong>la caja de la Feria</strong> (en Herramientas), escribí lo que quieras y tocá <strong>Guardar</strong>.</p>
            @endunless
        </div>
    @else
        <ul class="flex flex-col gap-2" data-test="saved-practices">
            @foreach ($practices as $practice)
                <li class="panel flex flex-wrap items-center gap-3 px-4 py-3" wire:key="saved-{{ $practice->id }}" data-test="saved-practice-{{ $practice->id }}">
                    <a href="{{ $practice->url() }}" wire:navigate class="flex min-w-0 flex-1 flex-col gap-0.5 hover:underline">
                        <span class="truncate font-medium text-white">{{ $practice->title }}</span>
                        <span class="flex flex-wrap items-center gap-x-2 text-xs text-ink-muted">
                            <span class="rounded border border-outline px-1.5 py-px font-mono text-[11px]">{{ $practice->languageLabel() }}</span>
                            guardada {{ $practice->updated_at->diffForHumans() }}
                            @if ($practice->unread_count)
                                <span class="flex items-center gap-1 text-danger" data-test="saved-practice-unread"><flux:icon name="chat-bubble-left-right" variant="micro" /> el profe te respondió</span>
                            @elseif ($practice->messages_count)
                                <span class="flex items-center gap-1"><flux:icon name="chat-bubble-left-right" variant="micro" /> con consulta</span>
                            @endif
                        </span>
                    </a>
                    <div class="flex shrink-0 items-center gap-1">
                        <flux:button size="sm" variant="primary" icon="play" :href="$practice->url()" wire:navigate>Abrir</flux:button>
                        <flux:button size="sm" variant="ghost" icon="arrow-down-tray" wire:click="download({{ $practice->id }})" data-test="saved-practice-download">Bajar</flux:button>
                        <flux:button size="sm" variant="ghost" icon="trash" wire:click="delete({{ $practice->id }})" aria-label="Borrar"
                            wire:confirm="¿Borrar «{{ $practice->title }}»? Se borra también su conversación con el profe." data-test="saved-practice-delete" />
                    </div>
                </li>
            @endforeach
        </ul>
        <p class="text-xs text-ink-muted">{{ $total }} de {{ $limit }} prácticas guardadas.</p>
    @endif
</div>
