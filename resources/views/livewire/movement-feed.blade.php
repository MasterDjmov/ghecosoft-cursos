@php
    $amountClass = fn (array $amount) => $amount['amount'] < 0
        ? 'border-danger/40 bg-danger/10 text-danger'
        : ['coin' => 'border-success/40 bg-success/10 text-success', 'wildcard' => 'border-secondary-bright/40 bg-secondary/10 text-secondary-bright', 'xp' => 'border-primary/40 bg-primary/10 text-primary-bright'][$amount['type']];
@endphp

{{-- Movimientos separados por curso: resumen arriba, cada hecho con su detalle abajo. --}}
<div class="flex flex-col gap-6">
    @if ($courses->count() > 1)
        <div class="flex flex-wrap gap-2" data-test="movement-filter">
            <flux:button size="sm" :variant="$selected ? 'ghost' : 'primary'" wire:click="selectCourse('')">Todos</flux:button>
            @foreach ($courses as $item)
                <flux:button size="sm" :variant="$selected?->is($item['course']) ? 'primary' : 'ghost'" wire:click="selectCourse('{{ $item['course']->slug }}')">
                    {{ $item['course']->title }}
                </flux:button>
            @endforeach
        </div>
    @endif

    {{-- Resumen --}}
    <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        @foreach ($selected ? $courses->filter(fn ($item) => $item['course']->is($selected)) : $courses as $item)
            <button type="button" wire:click="selectCourse('{{ $item['course']->slug }}')" @class(['panel flex flex-col gap-2 p-4 text-start transition hover:border-primary/60', 'border-primary/60' => $selected])>
                <span class="tech-label truncate">{{ $item['course']->title }}</span>
                <span class="flex flex-wrap items-baseline gap-x-4 gap-y-1">
                    <span><span class="font-mono text-2xl font-semibold text-success">{{ $item['coins'] }}</span> <span class="text-sm text-ink-muted">{{ term('coin.course', $item['course'], $item['coins']) }}</span></span>
                    <span><span class="font-mono text-2xl font-semibold text-primary-bright">{{ $item['xp'] }}</span> <span class="text-sm text-ink-muted">{{ term('xp.short') }} en el curso</span></span>
                </span>
            </button>
        @endforeach

        <div class="panel flex flex-col gap-2 p-4">
            <span class="tech-label">Para todos los cursos</span>
            <span class="flex flex-wrap items-baseline gap-x-4 gap-y-1">
                <span><span class="font-mono text-2xl font-semibold text-secondary-bright">{{ $totals['wildcards'] }}</span> <span class="text-sm text-ink-muted">{{ term('coin.wildcard', null, $totals['wildcards']) }}</span></span>
                <span><span class="font-mono text-2xl font-semibold text-primary-bright">{{ $totals['xp'] }}</span> <span class="text-sm text-ink-muted">{{ term('xp.short') }} en total</span></span>
            </span>
        </div>
    </div>

    {{-- Detalle --}}
    <section class="panel flex flex-col p-5">
        <h3 class="font-display font-semibold text-white">{{ $selected ? 'Movimientos en '.$selected->title : 'Todos los movimientos' }}</h3>

        <ul class="mt-2 divide-y divide-outline text-sm" data-test="movement-list">
            @forelse ($entries as $entry)
                <li class="flex flex-col gap-2 py-3 sm:flex-row sm:items-center sm:gap-4" wire:key="movement-{{ $entry['sort'] }}">
                    <div class="flex min-w-0 flex-1 items-start gap-3">
                        <flux:icon :name="$entry['icon']" variant="mini" class="mt-0.5 size-5 shrink-0 text-ink-muted" />
                        <div class="flex min-w-0 flex-col">
                            <span class="text-ink">
                                @if ($entry['node'] && $entry['course'])
                                    <a href="{{ $showAuthor ? route('admin.nodes.edit', [$entry['course'], $entry['node']]) : route('student.node', [$entry['course'], $entry['node']]) }}" wire:navigate class="hover:text-primary-bright hover:underline">{{ $entry['title'] }}</a>
                                @else
                                    {{ $entry['title'] }}
                                @endif
                            </span>
                            <span class="text-xs text-ink-muted">
                                @if ($entry['detail']) {{ $entry['detail'] }} · @endif
                                @if (! $selected && $courses->count() > 1 && $entry['course']) {{ $entry['course']->title }} · @endif
                                {{ $entry['at']->format('d/m/Y H:i') }}
                                @if ($entry['note']) · «{{ $entry['note'] }}» @endif
                                @if ($showAuthor && $entry['author']) · por {{ $entry['author'] }} @endif
                            </span>
                        </div>
                    </div>
                    <div class="flex shrink-0 flex-wrap gap-1.5 ps-8 sm:justify-end sm:ps-0">
                        @foreach ($entry['amounts'] as $amount)
                            <span class="rounded-md border px-2 py-0.5 font-mono text-xs font-semibold {{ $amountClass($amount) }}">
                                {{ $amount['amount'] > 0 ? '+' : '' }}{{ $amount['amount'] }} {{ $amount['label'] }}
                            </span>
                        @endforeach
                    </div>
                </li>
            @empty
                <li class="py-3 text-ink-muted">Todavía no hay movimientos.</li>
            @endforelse
        </ul>

        @if ($hasMore)
            <flux:button size="sm" variant="ghost" class="mt-3 self-center" wire:click="more">Ver más</flux:button>
        @endif
    </section>
</div>
