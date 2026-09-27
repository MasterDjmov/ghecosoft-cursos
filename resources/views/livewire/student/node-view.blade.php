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
        scrollToPractice(id) {
            document.getElementById('practica-' + id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        },
        syncHash() {
            history.replaceState(history.state, '', location.pathname + location.search + (this.openPractice ? '#practica-' + this.openPractice : ''));
        },
    }">
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

    @unless ($subscription)
        <flux:callout icon="clock" color="amber">
            <flux:callout.text>Tu abono no está vigente: podés repasar este {{ term('node', $course) }}, pero no entregar.
                <flux:link :href="route('student.course', $course)" wire:navigate>Renovar</flux:link>
            </flux:callout.text>
        </flux:callout>
    @endunless

    {{-- Teoría: video, explicación y ejemplo (se puede contraer). --}}
    @if ($youtubeId || $node->video_url || $contentHtml || $node->example_code)
        <section class="panel" x-data="{ theory: true }">
            <button type="button" class="flex w-full items-center gap-2 px-6 py-4 text-start" x-on:click="theory = ! theory" x-bind:aria-expanded="theory">
                <flux:icon name="book-open" variant="mini" class="text-primary-bright" />
                <h2 class="font-display text-lg font-semibold text-white">Teoría</h2>
                <flux:icon name="chevron-down" variant="micro" class="ms-auto text-ink-muted transition" x-bind:class="theory && 'rotate-180'" />
            </button>
            <div x-show="theory" x-collapse>
                <div class="flex flex-col gap-6 px-6 pb-6">
                    @if ($youtubeId)
                        <div class="aspect-video overflow-hidden rounded-lg border border-outline">
                            <iframe class="size-full" src="https://www.youtube-nocookie.com/embed/{{ $youtubeId }}" title="{{ $node->title }}"
                                allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
                        </div>
                    @elseif ($node->video_url)
                        <flux:button icon="play" :href="$node->video_url" target="_blank" rel="noopener noreferrer" class="self-start">Ver el video</flux:button>
                    @endif

                    @if ($contentHtml)
                        <article class="markdown">{!! $contentHtml !!}</article>
                    @endif

                    @if ($node->example_code)
                        <div class="flex flex-col gap-2">
                            <h3 class="tech-label">Ejemplo</h3>
                            <x-code-runner :code="$node->example_code" :stdin="$node->sample_input" :expected="$node->expected_output" name="ejemplo"
                                :language="$node->example_language ?? $course->language->value" :runnable="$runnable" />
                        </div>
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
