{{-- La sala de guion (D80, etapa 2): el libro de cada curso con todo abierto y los fragmentos del docente. --}}
@php($editing = ! $student)
<div class="mx-auto flex w-full max-w-4xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header label="Juego" title="Historia"
        subtitle="El libro de cada curso como lo arma Mis Crónicas: la bienvenida, la crónica de cada nodo, los cierres de rama y el epílogo. Colgá fragmentos (texto e imagen) donde quieras: se abren con lo que cuelgan. Los textos de los nodos se editan en el .md del curso; los de la bienvenida y los cierres, en el Diccionario." />

    <div class="grid gap-4 sm:grid-cols-2">
        <flux:select wire:model.live="courseSlug" label="Libro">
            <flux:select.option value="">Prólogo (para todos)</flux:select.option>
            @foreach ($courses as $option)
                <flux:select.option :value="$option->slug">{{ $option->title }}{{ $option->is_published ? '' : ' (sin publicar)' }}</flux:select.option>
            @endforeach
        </flux:select>
        @if ($course)
            <flux:select wire:model.live="viewAs" label="Ver como" data-test="story-view-as">
                <flux:select.option value="">Todo abierto (para escribir)</flux:select.option>
                @foreach ($students as $option)
                    <flux:select.option :value="(string) $option->id">{{ $option->fullName() }}</flux:select.option>
                @endforeach
            </flux:select>
        @endif
    </div>

    @if ($student)
        <flux:callout icon="eye" color="amber">
            <flux:callout.text>Así lo ve <strong>{{ $student->fullName() }}</strong>: lo que todavía no desbloqueó, en silueta y sin su texto. Para editar, volvé a «Todo abierto».</flux:callout.text>
        </flux:callout>
    @endif

    <section class="relative flex min-h-48 flex-col justify-end overflow-hidden rounded-xl border border-outline">
        @if ($scene)
            <img src="{{ $scene }}" alt="" class="absolute inset-0 size-full object-cover">
        @endif
        <div class="absolute inset-0 bg-gradient-to-t from-[#070a14] via-[#070a14]/70 to-transparent"></div>
        <div class="relative flex flex-col gap-1 p-5">
            <p class="tech-label text-secondary-bright">{{ $course ? 'Libro' : 'Prólogo' }}</p>
            <h2 class="font-display text-2xl font-semibold text-white">{{ $course?->title ?? ($prologue['title'] ?? 'El Mundo del Código') }}</h2>
        </div>
    </section>

    @if (! $course)
        @if ($prologue)
            <article class="panel flex flex-col gap-4 p-6"><div class="markdown text-ink">{!! $prologue['html'] !!}</div></article>
        @endif
        <p class="text-sm text-ink-muted">El prólogo se edita en el <a href="{{ route('admin.glossary', ['grupo' => 'story']) }}" wire:navigate class="text-primary-bright hover:underline">Diccionario</a> (clave <code class="font-mono">story.prologue</code>), igual que las frases de aliento (<code class="font-mono">story.locked_hints</code>).</p>
    @else
        @foreach ($chapters as $chapter)
            <section class="flex flex-col gap-3" wire:key="chapter-{{ $loop->index }}" data-test="story-chapter">
                <p class="tech-label text-primary-bright">{{ $chapter['title'] }}</p>
                @foreach ($chapter['pages'] as $page)
                    <div class="flex flex-col gap-1.5" wire:key="page-{{ $loop->parent->index }}-{{ $loop->index }}">
                        @include('livewire.partials.chronicle-page', ['page' => $page, 'portrait' => $portrait($page['speaker']), 'hint' => $page['unlocked'] ? null : $hint()])
                        @if ($editing)
                            <div class="flex flex-wrap items-center justify-end gap-1 text-xs">
                                @if ($page['fragment_id'])
                                    <span class="me-auto text-secondary-bright">Fragmento · {{ $page['trigger'] }}</span>
                                    <flux:button size="xs" variant="ghost" icon="arrow-up" wire:click="moveFragment({{ $page['fragment_id'] }}, -1)" aria-label="Subir" />
                                    <flux:button size="xs" variant="ghost" icon="arrow-down" wire:click="moveFragment({{ $page['fragment_id'] }}, 1)" aria-label="Bajar" />
                                    <flux:button size="xs" icon="pencil-square" wire:click="editFragment({{ $page['fragment_id'] }})">Editar</flux:button>
                                    <flux:button size="xs" variant="ghost" icon="trash" wire:click="deleteFragment({{ $page['fragment_id'] }})" wire:confirm="¿Borrar este fragmento?" aria-label="Borrar" />
                                @elseif ($page['node_id'])
                                    <flux:button size="xs" variant="ghost" icon="plus" wire:click="newFragment('node_completed', {{ $page['node_id'] }})" data-test="add-fragment-node">Fragmento al completar este {{ term('node') }}</flux:button>
                                @elseif ($page['kind'] === 'intro')
                                    <flux:button size="xs" variant="ghost" icon="plus" wire:click="newFragment('course_started')">Fragmento al empezar el curso</flux:button>
                                @elseif ($page['kind'] === 'epilogue')
                                    <flux:button size="xs" variant="ghost" icon="plus" wire:click="newFragment('course_completed')">Fragmento al terminar el curso</flux:button>
                                @endif
                            </div>
                        @endif
                    </div>
                @endforeach
                @if ($editing && $chapter['branch_id'])
                    <flux:button size="xs" variant="ghost" icon="plus" class="self-end" wire:click="newFragment('branch_completed', null, {{ $chapter['branch_id'] }})">Fragmento al terminar esta rama</flux:button>
                @endif
            </section>
        @endforeach
        @if ($editing && ! collect($chapters)->contains('title', 'Epílogo'))
            <flux:button icon="plus" class="self-start" wire:click="newFragment('course_completed')">Fragmento al terminar el curso</flux:button>
        @endif
    @endif

    <flux:modal name="fragment" class="w-full max-w-2xl">
        <form wire:submit="saveFragment" class="flex flex-col gap-5">
            <div class="flex flex-col gap-1">
                <flux:heading size="lg">{{ $fragmentId ? 'Editar fragmento' : 'Nuevo fragmento' }}</flux:heading>
                <flux:text>
                    @switch($trigger)
                        @case('node_completed') Se abre al completar «{{ $anchorTitle }}». @break
                        @case('branch_completed') Se abre al terminar la rama. @break
                        @case('course_started') Se abre al empezar el curso. @break
                        @case('course_completed') Se abre al terminar el curso. @break
                    @endswitch
                </flux:text>
            </div>
            <flux:input wire:model="title" label="Título" placeholder="Una carta de Ferrum" />
            <flux:textarea wire:model="body" label="Texto" rows="8" description:trailing="Markdown. Podés usar {heroe}, {mentor}, {mundo} y {region}." />
            <div class="flex flex-col gap-2">
                <flux:label>Imagen (opcional)</flux:label>
                @if ($image && $image->isPreviewable())
                    <img src="{{ $image->temporaryUrl() }}" alt="" class="max-h-48 self-start rounded-lg">
                @endif
                <input type="file" wire:model="image" accept="image/png,image/jpeg,image/webp"
                    class="text-sm text-ink-muted file:me-3 file:rounded-md file:border-0 file:bg-surface-highest file:px-3 file:py-2 file:text-ink">
                @if ($fragmentId)
                    <flux:checkbox wire:model="removeImage" label="Quitar la imagen que tiene" />
                @endif
                <flux:error name="image" />
            </div>
            <div class="flex justify-end gap-2">
                <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                <flux:button variant="primary" type="submit">Guardar</flux:button>
            </div>
        </form>
    </flux:modal>
</div>
