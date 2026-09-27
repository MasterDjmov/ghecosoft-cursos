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
        <section class="panel flex flex-col gap-2 p-5 sm:p-6">
            <h2 class="font-display text-lg font-semibold text-white">Ejemplo</h2>
            <x-code-runner :code="$node->example_code" :stdin="$node->sample_input" :expected="$node->expected_output"
                :language="$node->example_language ?? $course->language->value" :runnable="$runnable" />
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
                <livewire:student.practice-card :practice="$practice" :key="'practice-'.$practice->id" />
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
