@php
    $coin = fn (int $n) => term('coin.course', $course, $n);
    $wild = fn (int $n) => term('coin.wildcard', null, $n);
@endphp

<div class="mx-auto flex w-full max-w-4xl flex-col gap-6 p-4 sm:p-8">
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
    </header>

    @unless ($subscription)
        <flux:callout icon="clock" color="amber">
            <flux:callout.text>Tu abono no está vigente: podés repasar este {{ term('node', $course) }}, pero no entregar.
                <flux:link :href="route('student.course', $course)" wire:navigate>Renovar</flux:link>
            </flux:callout.text>
        </flux:callout>
    @endunless

    @if ($youtubeId)
        <div class="aspect-video overflow-hidden rounded-lg border border-outline">
            <iframe class="size-full" src="https://www.youtube-nocookie.com/embed/{{ $youtubeId }}" title="{{ $node->title }}"
                allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
        </div>
    @elseif ($node->video_url)
        <flux:button icon="play" :href="$node->video_url" target="_blank" rel="noopener noreferrer" class="self-start">Ver el video</flux:button>
    @endif

    @if ($contentHtml)
        <article class="panel markdown p-5 sm:p-6">{!! $contentHtml !!}</article>
    @endif

    {{-- Ejemplo ejecutable --}}
    @if ($node->example_code)
        <section class="panel flex flex-col gap-3 p-5 sm:p-6"
            x-data="codeRunner(@js(['code' => $node->example_code, 'stdin' => (string) $node->sample_input, 'expected' => (string) $node->expected_output, 'pyodideUrl' => config('services.pyodide.url'), 'timeout' => config('services.pyodide.timeout_ms')]))">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <h2 class="font-display text-lg font-semibold text-white">Ejemplo</h2>
                <div class="flex flex-wrap gap-2">
                    <flux:button size="sm" variant="ghost" icon="clipboard" x-on:click="copy"><span x-text="copied ? '¡Copiado!' : 'Copiar'">Copiar</span></flux:button>
                    <flux:button size="sm" variant="ghost" icon="arrow-uturn-left" x-on:click="restore" x-show="code !== original">Restaurar</flux:button>
                    @if ($runnable)
                        <flux:button size="sm" variant="primary" icon="play" x-on:click="run" x-bind:disabled="running">
                            <span x-text="running ? 'Ejecutando…' : 'Ejecutar'"></span>
                        </flux:button>
                    @endif
                </div>
            </div>

            <textarea x-model="code" spellcheck="false" rows="{{ min(18, substr_count($node->example_code, "\n") + 2) }}"
                class="w-full resize-y rounded-lg border border-outline bg-surface-lowest p-3 font-mono text-sm text-ink focus:ring-2 focus:ring-accent focus:outline-none"
                aria-label="Código de ejemplo" x-on:keydown.ctrl.enter.prevent="run"></textarea>

            @if ($runnable)
                <details class="text-sm" @if ($node->sample_input) open @endif>
                    <summary class="cursor-pointer text-ink-muted">Entrada (una línea por cada <code class="font-mono">input()</code>)</summary>
                    <textarea x-model="stdin" rows="2" spellcheck="false"
                        class="mt-2 w-full rounded-lg border border-outline bg-surface-lowest p-2 font-mono text-sm text-ink focus:ring-2 focus:ring-accent focus:outline-none"></textarea>
                </details>

                <div class="flex flex-col gap-2" x-show="output !== null || status" x-cloak>
                    <div class="flex items-center justify-between text-xs">
                        <span class="tech-label">Salida</span>
                        <span class="font-mono" x-bind:class="error ? 'text-danger' : 'text-ink-muted'" x-text="status"></span>
                    </div>
                    <pre class="max-h-72 overflow-auto rounded-lg border border-outline bg-[#05070d] p-3 font-mono text-sm whitespace-pre-wrap"
                        x-bind:class="error ? 'text-danger' : 'text-success'" x-text="output"></pre>
                    <p class="text-xs text-success" x-show="matches === true">✓ Coincide con la salida esperada.</p>
                </div>
            @endif

            @if ($node->expected_output)
                <details class="text-sm">
                    <summary class="cursor-pointer text-ink-muted">Salida esperada</summary>
                    <pre class="mt-2 overflow-auto rounded-lg border border-outline bg-surface-lowest p-3 font-mono text-sm text-ink-muted">{{ $node->expected_output }}</pre>
                </details>
            @endif
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
        <section class="flex flex-col gap-3">
            <h2 class="font-display text-lg font-semibold text-white">{{ ucfirst(term('practice', $course, 2)) }}</h2>
            @foreach ($practices as $practice)
                @php($status = $statuses[$practice->id] ?? null)
                <article id="practica-{{ $practice->id }}" class="panel flex scroll-mt-20 flex-col gap-3 p-5" wire:key="practice-{{ $practice->id }}">
                    <div class="flex flex-wrap items-center gap-2">
                        <h3 class="font-medium text-white">{{ $practice->title }}</h3>
                        <flux:badge size="sm" :color="$practice->is_required ? 'cyan' : 'violet'">{{ $practice->is_required ? 'Obligatoria' : 'Optativa' }}</flux:badge>
                        @if ($status)
                            <flux:badge size="sm" :color="['approved' => 'green', 'submitted' => 'amber', 'redo' => 'red'][$status]">
                                {{ ['approved' => 'Aprobada', 'submitted' => 'Entregada', 'redo' => 'Rehacer'][$status] }}
                            </flux:badge>
                        @endif
                        <span class="ms-auto font-mono text-xs text-ink-muted">
                            +{{ $practice->coin_reward }} {{ $practice->is_required ? $coin($practice->coin_reward) : $wild($practice->coin_reward) }}
                            · +{{ $practice->xp_reward }} {{ term('xp.short') }}
                        </span>
                    </div>
                    @if ($instructions[$practice->id])
                        <div class="markdown text-sm">{!! $instructions[$practice->id] !!}</div>
                    @endif
                    <p class="text-xs text-ink-muted">
                        <flux:icon name="clock" variant="micro" class="inline" />
                        Entrega: {{ $practice->submission_mode->label() }}. El editor y el botón Entregar llegan en la próxima actualización.
                    </p>
                </article>
            @endforeach
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
