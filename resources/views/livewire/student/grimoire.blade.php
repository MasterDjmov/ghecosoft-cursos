{{-- El grimorio (D84 § 4, D89): las cartas de las micro-misiones superadas, para volver a consultar la sintaxis.
     Todo plegado (rama → nodo → carta) y con un buscador, para que no sea una pared de cartas. --}}
<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-col gap-1">
        <p class="tech-label">Tu memoria externa</p>
        <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Grimorio</h1>
        <p class="text-ink-muted">Cada micro-misión que superás te deja su carta. Si te olvidaste cómo se escribía algo, está acá: buscala, copiala y seguí.</p>
    </header>

    @if ($books->isEmpty())
        <div class="panel flex items-start gap-4 p-4" data-test="grimoire-empty">
            <img src="{{ asset('img/personajes/gheco.webp') }}" alt="" class="size-14 shrink-0 rounded-full border border-primary/40 object-cover">
            <p class="text-sm text-ink">—¡Todavía está en blanco! Superá tu primera micro-misión y aparece la primera carta. Están al principio de cada {{ term('node') }}.</p>
        </div>
    @else
        @if ($books->count() > 1)
            <nav class="flex flex-wrap gap-2" aria-label="Cursos" data-test="grimoire-tabs">
                @foreach ($books as $book)
                    <button type="button" wire:click="$set('tab', '{{ $book['course']->slug }}')" wire:key="tab-{{ $book['course']->id }}"
                        @class(['flex items-center gap-2 rounded-lg border px-3 py-2 text-sm transition', 'border-primary-bright bg-primary/10 text-white' => $current['course']->is($book['course']), 'border-outline text-ink-muted hover:text-white' => ! $current['course']->is($book['course'])])>
                        <x-course-logo :course="$book['course']" size="size-6" /> {{ \Illuminate\Support\Str::before($book['course']->title, ':') }}
                        <span class="font-mono text-xs">{{ $book['count'] }}</span>
                    </button>
                @endforeach
            </nav>
        @endif

        <div class="flex items-center justify-between gap-3">
            <h2 class="flex items-center gap-2 font-display text-lg font-semibold text-white">
                <x-course-logo :course="$current['course']" size="size-7" /> {{ $current['course']->title }}
            </h2>
            <span class="font-mono text-sm text-ink-muted" data-test="grimoire-count">{{ $current['count'] }} de {{ $totals[$current['course']->id] ?? $current['count'] }} cartas</span>
        </div>

        @php
            // El texto en el que busca cada carta (título, sintaxis y micro-misión).
            $cardText = fn ($step) => $step->card_title.' '.$step->card_body.' '.$step->title;
            $allText = $current['branches']->flatMap(fn ($part) => $part['nodes'])->flatMap(fn ($group) => $group['steps']->map($cardText))->implode(' ');
        @endphp

        {{-- El buscador abre solo lo que coincide; se filtra en el navegador, sin pedir nada al servidor. --}}
        <div class="flex flex-col gap-3" wire:key="book-{{ $current['course']->id }}"
            x-data="{
                q: '',
                norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '') },
                get searching() { return this.q.trim() !== '' },
                hit(text) { return ! this.searching || this.norm(text).includes(this.norm(this.q.trim())) },
            }">
            <label class="flex items-center gap-2 rounded-lg border border-outline bg-surface-lowest px-3 py-2 focus-within:border-primary-bright">
                <flux:icon name="magnifying-glass" variant="mini" class="text-ink-muted" />
                <input type="search" x-model.debounce.150ms="q" placeholder="Buscar una carta: print, lista, for, input…" aria-label="Buscar una carta"
                    class="w-full bg-transparent text-sm text-white outline-none placeholder:text-ink-muted" data-test="grimoire-search">
            </label>

            @foreach ($current['branches'] as $part)
                <details class="group/branch" wire:key="branch-{{ $part['branch']?->id ?? 0 }}" data-test="grimoire-branch"
                    x-show="hit(@js($part['nodes']->flatMap(fn ($group) => $group['steps']->map($cardText))->implode(' ')))" :open="searching || null">
                    <summary class="flex cursor-pointer items-center justify-between gap-3 rounded-lg border border-outline bg-surface px-4 py-3 hover:border-primary/60">
                        <span class="flex min-w-0 items-center gap-2">
                            @if ($part['branch'])<span class="tech-label shrink-0 text-secondary-bright">{{ $part['branch']->code }}</span>@endif
                            <span class="truncate font-display font-semibold text-white">{{ $part['branch'] ? \Illuminate\Support\Str::after($part['branch']->title, '· ') : 'Primeros pasos' }}</span>
                        </span>
                        <span class="flex shrink-0 items-center gap-2 text-xs text-ink-muted">{{ $part['count'] }} {{ $part['count'] === 1 ? 'carta' : 'cartas' }}
                            <flux:icon name="chevron-down" variant="micro" class="transition group-open/branch:rotate-180" /></span>
                    </summary>

                    <div class="mt-2 flex flex-col gap-2 ps-2 sm:ps-4">
                        @foreach ($part['nodes'] as $group)
                            <details class="panel group/node overflow-hidden" wire:key="node-{{ $group['node']->id }}" data-test="grimoire-node"
                                x-show="hit(@js($group['steps']->map($cardText)->implode(' ')))" :open="searching || null">
                                <summary class="flex cursor-pointer items-center justify-between gap-3 px-4 py-2.5">
                                    <span class="flex min-w-0 flex-col">
                                        <span class="tech-label text-primary-bright">{{ $group['node']->code }}</span>
                                        <span class="truncate font-medium text-white">{{ $group['node']->title }}</span>
                                    </span>
                                    <span class="flex shrink-0 items-center gap-2 text-xs text-ink-muted">{{ $group['steps']->count() }} {{ $group['steps']->count() === 1 ? 'carta' : 'cartas' }}
                                        <flux:icon name="chevron-down" variant="micro" class="transition group-open/node:rotate-180" /></span>
                                </summary>
                                <div class="flex flex-col gap-1.5 border-t border-outline/60 p-3">
                                    @foreach ($group['steps'] as $step)
                                        <details class="group/card rounded-lg border border-secondary/40 bg-secondary/5" wire:key="card-{{ $step->id }}" data-test="grimoire-card"
                                            x-show="hit(@js($cardText($step)))" :open="searching || null">
                                            <summary class="flex cursor-pointer items-center justify-between gap-2 px-3 py-2">
                                                <span class="flex min-w-0 items-center gap-2 font-medium text-secondary-bright">
                                                    <flux:icon name="book-open" variant="micro" class="shrink-0" /> <span class="truncate">{{ $step->card_title }}</span>
                                                </span>
                                                <flux:icon name="chevron-down" variant="micro" class="shrink-0 text-ink-muted transition group-open/card:rotate-180" />
                                            </summary>
                                            <div class="flex flex-col gap-2 px-3 pb-3">
                                                <p class="text-xs text-ink-muted">De «{{ $step->title }}»</p>
                                                @foreach (\App\Livewire\Student\Grimoire::snippets($step->card_body) as $snippet)
                                                    <div class="flex items-start gap-2 rounded-md border border-outline bg-surface-lowest px-2.5 py-1.5" x-data>
                                                        <code class="min-w-0 flex-1 break-words font-mono text-sm text-ink">{{ $snippet }}</code>
                                                        <button type="button" class="shrink-0 text-xs text-primary-bright hover:underline" title="Copiar"
                                                            x-on:click="navigator.clipboard.writeText(@js(trim(\Illuminate\Support\Str::before($snippet, ' → ')))); $el.textContent = '¡Listo!'">Copiar</button>
                                                    </div>
                                                @endforeach
                                            </div>
                                        </details>
                                    @endforeach
                                </div>
                            </details>
                        @endforeach
                    </div>
                </details>
            @endforeach

            <p x-show="searching && ! hit(@js($allText))" x-cloak class="text-sm text-ink-muted" data-test="grimoire-no-results">
                No hay ninguna carta con «<span x-text="q.trim()"></span>».
            </p>
        </div>
    @endif
</div>
