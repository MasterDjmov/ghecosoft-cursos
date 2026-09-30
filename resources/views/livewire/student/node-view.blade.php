@php
    $coin = fn (int $n) => term('coin.course', $course, $n);
    $wild = fn (int $n) => term('coin.wildcard', null, $n);

    $required = $practices->where('is_required', true);
    $optional = $practices->where('is_required', false);
    $approvedCount = $practices->filter(fn ($p) => ($statuses[$p->id] ?? null) === 'approved')->count();
    $requiredPending = $required->filter(fn ($p) => ($statuses[$p->id] ?? null) !== 'approved')->count();
    // Los mismos colores que la leyenda del árbol.
    $chipColor = fn ($id) => ['approved' => '#10b981', 'submitted' => '#f59e0b', 'redo' => '#f87171'][$statuses[$id] ?? null] ?? '#475569';
@endphp

{{-- La hoja abierta vive en Alpine (y en #practica-ID). x-data no lleva datos del servidor
     para que Livewire no la reinicie al redibujar; la hoja inicial va en data-first-pending. --}}
<div class="mx-auto flex w-full max-w-4xl flex-col gap-6 p-4 sm:p-8" data-first-pending="{{ $firstPending }}"
    x-data="{
        openPractice: null,
        init() {
            const match = location.hash.match(/^#practica-(\d+)$/);
            const fromHash = match && document.getElementById('practica-' + match[1]) ? Number(match[1]) : null;
            this.openPractice = fromHash ?? (Number(this.$el.dataset.firstPending) || null);
            if (fromHash) this.$nextTick(() => this.scrollToPractice(fromHash));
        },
        togglePractice(id) {
            this.openPractice = this.openPractice === id ? null : id;
            this.syncHash();
        },
        goToPractice(id) {
            this.openPractice = id;
            this.syncHash();
            this.$nextTick(() => this.scrollToPractice(id));
        },
        fromHash() {
            const match = location.hash.match(/^#practica-(\d+)$/);
            if (match && document.getElementById('practica-' + match[1])) this.goToPractice(Number(match[1]));
        },
        scrollToPractice(id) {
            document.getElementById('practica-' + id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        },
        syncHash() {
            history.replaceState(history.state, '', location.pathname + location.search + (this.openPractice ? '#practica-' + this.openPractice : ''));
        },
    }"
    x-on:hashchange.window="fromHash()">
    <nav class="flex flex-wrap items-center gap-2 text-sm text-ink-muted">
        <a href="{{ route('student.worlds') }}" wire:navigate class="hover:text-ink">Mundos</a>
        <flux:icon name="chevron-right" variant="micro" />
        <a href="{{ route('student.tree', $course) }}" wire:navigate class="hover:text-ink">{{ $course->title }}</a>
        <flux:icon name="chevron-right" variant="micro" />
        <span class="text-ink">{{ $node->title }}</span>
    </nav>

    <header class="flex flex-col gap-2">
        <p class="tech-label">
            {{ $node->isRoot() ? term('node.root', $course) : ($node->isBoss() ? term('node.boss', $course) : ($node->branch?->title ?? $node->type->label())) }}
            @if ($completed) · <span class="text-success">{{ term('state.completed', $course) }}</span> @endif
        </p>
        <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">{{ $node->title }}</h1>

        {{-- Resumen de progreso de las hojas --}}
        @if ($practices->isNotEmpty())
            <div class="mt-2 flex flex-col gap-3" data-test="practice-progress">
                <div class="flex flex-col gap-1.5">
                    <p class="text-sm text-ink-muted">
                        <span class="font-medium text-ink">{{ $approvedCount }} de {{ $practices->count() }}</span> {{ term('practice', $course, $practices->count()) }}
                        ·
                        @if ($requiredPending > 0)
                            <span class="text-warning">{{ $requiredPending }} {{ $requiredPending === 1 ? 'obligatoria pendiente' : 'obligatorias pendientes' }}</span>
                        @else
                            <span class="text-success">obligatorias al día</span>
                        @endif
                    </p>
                    <div class="h-1.5 overflow-hidden rounded-full bg-surface-highest" role="progressbar"
                        aria-valuemin="0" aria-valuemax="{{ $practices->count() }}" aria-valuenow="{{ $approvedCount }}">
                        <div class="h-full rounded-full bg-success transition-all" style="width: {{ round($approvedCount / $practices->count() * 100) }}%"></div>
                    </div>
                </div>
                <div class="flex flex-wrap gap-2">
                    @foreach ($required->concat($optional) as $practice)
                        <button type="button" x-on:click="goToPractice({{ $practice->id }})" title="{{ $practice->title }}"
                            class="flex max-w-56 items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs text-ink transition hover:bg-surface-high {{ $practice->is_required ? '' : 'border-dashed' }}"
                            style="border-color: {{ $chipColor($practice->id) }}66; background-color: {{ $chipColor($practice->id) }}14"
                            x-bind:class="openPractice === {{ $practice->id }} && 'ring-1 ring-primary-bright'">
                            <span class="size-2 shrink-0 rounded-full" style="background-color: {{ $chipColor($practice->id) }}"></span>
                            <span class="truncate">{{ $practice->title }}</span>
                        </button>
                    @endforeach
                </div>
            </div>
        @endif
    </header>

    @if ($trial)
        {{-- Clase 0 de prueba (D71): se lee y se practica; para que el profe corrija, el abono. --}}
        <flux:callout icon="sparkles" color="cyan" data-test="trial-banner">
            <flux:callout.heading>Estás probando {{ $course->title }} gratis</flux:callout.heading>
            <flux:callout.text>
                Leé la clase, mirá el ejemplo y resolvé las {{ term('practice', $course, 2) }} en el editor. Cuando quieras que el profe te corrija y seguir con el resto del curso, pedí tu abono: el mes empieza a correr recién cuando se aprueba.
            </flux:callout.text>
            <x-slot name="actions">
                <flux:button variant="primary" size="sm" icon="ticket" :href="route('student.course', $course)" wire:navigate>Pedir abono</flux:button>
            </x-slot>
        </flux:callout>
    @elseif (! $subscription)
        <flux:callout icon="clock" color="amber">
            <flux:callout.text>Tu abono no está vigente: podés repasar este {{ term('node', $course) }}, pero no entregar.
                <flux:link :href="route('student.course', $course)" wire:navigate>Renovar</flux:link>
            </flux:callout.text>
        </flux:callout>
    @endif

    {{-- Presentación del jefe: qué se gana al vencerlo. --}}
    @if ($node->isBoss())
        <aside class="flex items-center gap-4 rounded-lg border border-danger/40 bg-danger/10 px-6 py-4" data-test="boss-banner">
            <span class="grid size-12 shrink-0 place-items-center rounded-full bg-danger/20 text-danger"><flux:icon name="fire" /></span>
            <div class="flex min-w-0 flex-col gap-0.5">
                <p class="tech-label text-danger">{{ ucfirst(term('node.boss', $course)) }}{{ $node->branch ? ' de «'.$node->branch->title.'»' : '' }}</p>
                <p class="text-ink">
                    Es un proyecto integrador: no trae teoría nueva. Vencelo y ganás
                    <strong class="text-white">+{{ $bossXp }} {{ term('xp.short') }}</strong>@if ($node->badge) y la {{ term('badge', $course) }}
                        <strong class="text-white">«{{ $node->badge->name }}»</strong>@endif.
                </p>
                @if ($node->badge?->description)
                    <p class="text-sm text-ink-muted">{{ $node->badge->description }}</p>
                @endif
            </div>
        </aside>
    @endif

    {{-- Crónica: la historia del nodo, antes de la teoría. --}}
    @if ($sections['chronicle'])
        <aside class="relative overflow-hidden rounded-lg border border-secondary/40 bg-secondary/10 px-6 py-5" data-test="chronicle">
            <p class="tech-label mb-2 flex items-center gap-2 text-secondary-bright"><flux:icon name="sparkles" variant="micro" /> Crónica</p>
            <div class="markdown text-ink italic">{!! $sections['chronicle'] !!}</div>
        </aside>
    @endif

    {{-- Teoría: objetivos, video, explicación, ejemplo, usos y errores (se puede contraer). --}}
    @if ($youtubeId || $node->video_url || $contentHtml || $node->example_code || $sections['objectives'] || $sections['before'] || $sections['uses'] || $sections['errors'])
        <section class="panel" x-data="{ theory: true }">
            <button type="button" class="flex w-full items-center gap-2 px-6 py-4 text-start" x-on:click="theory = ! theory" x-bind:aria-expanded="theory">
                <flux:icon name="book-open" variant="mini" class="text-primary-bright" />
                <h2 class="font-display text-lg font-semibold text-white">Teoría</h2>
                <flux:icon name="chevron-down" variant="micro" class="ms-auto text-ink-muted transition" x-bind:class="theory && 'rotate-180'" />
            </button>
            <div x-show="theory" x-collapse>
                <div class="flex flex-col gap-8 px-6 pb-6">
                    @if ($sections['objectives'] || $sections['before'])
                        <div class="grid gap-4 sm:grid-cols-2">
                            @if ($sections['objectives'])
                                <div class="rounded-lg border border-outline bg-surface-lowest/50 p-4">
                                    <p class="tech-label mb-2 flex items-center gap-2"><flux:icon name="flag" variant="micro" class="text-success" /> Al terminar, vas a poder</p>
                                    <div class="markdown text-sm">{!! $sections['objectives'] !!}</div>
                                </div>
                            @endif
                            @if ($sections['before'])
                                <div class="rounded-lg border border-outline bg-surface-lowest/50 p-4">
                                    <p class="tech-label mb-2 flex items-center gap-2"><flux:icon name="arrow-uturn-left" variant="micro" class="text-primary-bright" /> Antes de empezar</p>
                                    <div class="markdown text-sm">{!! $sections['before'] !!}</div>
                                </div>
                            @endif
                        </div>
                    @endif

                    @if ($youtubeId)
                        <div class="aspect-video overflow-hidden rounded-lg border border-outline">
                            <iframe class="size-full" src="https://www.youtube-nocookie.com/embed/{{ $youtubeId }}" title="{{ $node->title }}"
                                allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
                        </div>
                    @elseif ($node->video_url)
                        <flux:button icon="play" :href="$node->video_url" target="_blank" rel="noopener noreferrer" class="self-start">Ver el video</flux:button>
                    @endif

                    @if ($contentHtml)
                        <x-node-section title="Explicación" icon="light-bulb" companion="companion.theory" :course="$course">
                            <article class="markdown">{!! $contentHtml !!}</article>
                        </x-node-section>
                    @endif

                    @if ($node->example_code)
                        <x-node-section title="Ejemplo" icon="code-bracket">
                            <x-code-runner :code="$node->example_code" :stdin="$node->sample_input" :expected="$node->expected_output" name="ejemplo"
                                :language="$node->example_language ?? $course->language->value" :runnable="$runnable" />
                        </x-node-section>
                    @endif

                    @if ($sections['uses'])
                        <x-node-section title="¿Para qué sirve?" icon="wrench-screwdriver" companion="companion.uses" :course="$course" color="text-warning">
                            <div class="markdown">{!! $sections['uses'] !!}</div>
                        </x-node-section>
                    @endif

                    @if ($sections['errors'] || $beast)
                        <x-node-section title="Errores habituales" icon="bug-ant" companion="companion.errors" :course="$course" color="text-danger">
                            @if ($beast)
                                <div class="flex items-start gap-3 rounded-lg border border-danger/40 bg-danger/10 p-4" data-test="beast">
                                    @if ($beast['icon_path'])
                                        <img src="{{ Storage::disk('public')->url($beast['icon_path']) }}" alt="" class="size-12 shrink-0 rounded-md object-cover">
                                    @else
                                        <span class="grid size-12 shrink-0 place-items-center rounded-md bg-danger/20 text-danger"><flux:icon name="bug-ant" /></span>
                                    @endif
                                    <div class="flex min-w-0 flex-col gap-1">
                                        <p class="tech-label text-danger">Criatura</p>
                                        <p class="font-display font-semibold text-white">{{ ucfirst($beast['singular']) }}</p>
                                        @if ($beast['short_description'])
                                            <p class="text-sm text-ink-muted">{{ $beast['short_description'] }}</p>
                                        @endif
                                        @if ($beast['lore_html'])
                                            <details class="mt-1 text-sm">
                                                <summary class="cursor-pointer text-danger/90">Su historia</summary>
                                                <div class="markdown mt-2">{!! $beast['lore_html'] !!}</div>
                                            </details>
                                        @endif
                                    </div>
                                </div>
                            @endif
                            @if ($sections['errors'])
                                <div class="markdown">{!! $sections['errors'] !!}</div>
                            @endif
                        </x-node-section>
                    @endif
                </div>
            </div>
        </section>
    @endif

    {{-- Recursos --}}
    @if ($resources->isNotEmpty())
        <section class="panel flex flex-col gap-3 p-5 sm:p-6">
            <h2 class="font-display text-lg font-semibold text-white">Recursos</h2>
            <ul class="flex flex-col gap-2">
                @foreach ($resources as $resource)
                    <li>
                        @if ($resource->type === \App\Enums\ResourceType::File)
                            <a href="{{ route('files.resource', $resource) }}" class="flex items-center gap-2 text-primary-bright hover:underline">
                                <flux:icon name="paper-clip" variant="mini" /> {{ $resource->title }}
                            </a>
                        @else
                            <a href="{{ $resource->url }}" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 text-primary-bright hover:underline">
                                <flux:icon name="link" variant="mini" /> {{ $resource->title }}
                            </a>
                        @endif
                    </li>
                @endforeach
            </ul>
        </section>
    @endif

    {{-- Hojas (prácticas) --}}
    @if ($practices->isNotEmpty())
        <section class="mt-6 flex flex-col gap-7">
            <h2 class="font-display text-lg font-semibold text-white">{{ ucfirst(term('practice', $course, 2)) }}</h2>
            @foreach ($required as $practice)
                <livewire:student.practice-card :practice="$practice" :number="$numbers[$practice->id]" :key="'practice-'.$practice->id" />
            @endforeach

            @if ($optional->isNotEmpty())
                <h3 class="flex items-center gap-2 font-display text-base font-semibold text-white" @if ($required->isNotEmpty()) style="margin-top: 1rem" @endif>
                    <flux:icon name="sparkles" variant="mini" class="text-[#a855f7]" /> Desafíos extra
                </h3>
                @foreach ($optional as $practice)
                    <livewire:student.practice-card :practice="$practice" :number="$numbers[$practice->id]" :key="'practice-'.$practice->id" />
                @endforeach
            @endif
        </section>
    @endif

    {{-- Prueba del sello: autoevaluación sin nota. --}}
    @if ($selfCheck->isNotEmpty())
        <section class="panel flex flex-col gap-4 p-6" data-test="self-check">
            <div class="flex flex-col gap-1">
                <h2 class="flex items-center gap-2 font-display text-lg font-semibold text-white"><flux:icon name="shield-check" variant="mini" class="text-success" /> Prueba del sello</h2>
                <p class="text-sm text-ink-muted">Si podés responder esto, lo entendiste. Pensalo antes de ver la respuesta: no suma ni resta nada.</p>
            </div>
            <ol class="flex flex-col gap-3">
                @foreach ($selfCheck as $item)
                    <li class="rounded-lg border border-outline bg-surface-lowest/40">
                        <details class="group">
                            <summary class="flex cursor-pointer list-none items-start gap-3 px-4 py-3 text-ink">
                                <span class="font-mono text-xs text-ink-muted">{{ $loop->iteration }}.</span>
                                <span class="flex-1">{{ $item['question'] }}</span>
                                <span class="shrink-0 text-xs text-primary-bright group-open:hidden">Ver respuesta</span>
                            </summary>
                            <div class="markdown border-t border-outline px-4 py-3 text-sm">{!! $item['answer'] ?: '<p>—</p>' !!}</div>
                        </details>
                    </li>
                @endforeach
            </ol>
        </section>
    @endif

    {{-- Navegación --}}
    <nav class="flex flex-col gap-3 border-t border-outline pt-5 sm:flex-row sm:justify-between">
        @if ($parent)
            <flux:button variant="ghost" icon="arrow-left" :href="route('student.node', [$course, $parent])" wire:navigate>{{ $parent->title }}</flux:button>
        @else
            <flux:button variant="ghost" icon="share" :href="route('student.tree', $course)" wire:navigate>Volver al árbol</flux:button>
        @endif

        <div class="flex flex-col gap-2 sm:items-end">
            @foreach ($next as $item)
                @if (in_array($item['state'], ['unlocked', 'completed'], true))
                    <flux:button icon-trailing="arrow-right" :href="route('student.node', [$course, $item['node']])" wire:navigate>{{ $item['node']->title }}</flux:button>
                @elseif ($item['state'] === 'available')
                    <flux:button variant="primary" icon="lock-open" :href="route('student.tree', $course)" wire:navigate>Siguiente: {{ $item['node']->title }} · {{ $item['price'] }}</flux:button>
                @else
                    <span class="flex items-center gap-2 text-sm text-ink-muted">
                        <flux:icon name="lock-closed" variant="micro" /> {{ $item['node']->title }}: aprobá las obligatorias de este {{ term('node', $course) }}
                    </span>
                @endif
            @endforeach
        </div>
    </nav>
</div>
