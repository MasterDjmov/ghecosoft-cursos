@php
    $familyColors = collect($graph['families'])->pluck('color', 'key');
    $status = fn ($row) => $row['taught_in']->isEmpty()
        ? ($row['used_in']->isNotEmpty() ? ['Falta y se usa', 'red'] : ['Falta', 'zinc'])
        : ($row['taught_in']->count() > 1 ? ['Repetido', 'amber'] : ['Enseñado', 'green']);
    $chip = fn ($courseId) => $courses[$courseId] ?? null;
@endphp

<div class="flex w-full flex-col gap-8 py-4 sm:py-8">
    <div class="mx-auto w-full max-w-7xl px-4 sm:px-8">
        <x-admin.page-header label="Cursos" title="Universo"
            subtitle="Todos los cursos en un mapa, unidos por los temas que enseñan (línea) y los que dan por sabidos (línea con partículas). Los temas salen de cursos/temas.md y se marcan en el Markdown de cada curso (temas: y usa:). Arrastrá para rotar, rueda para acercar, clic derecho para mover." />
    </div>

    {{-- El mapa: todo el ancho y casi todo el alto (y pantalla completa) para ver con detalle --}}
    <section class="relative mx-2 h-[calc(100vh-5rem)] min-h-[560px] overflow-hidden rounded-lg border border-outline bg-[#05070d] sm:mx-4"
        x-data="universeMap(@js($graph))" data-test="universe-map">
        <div x-ref="canvas" class="absolute inset-0" wire:ignore></div>

        {{-- Filtros --}}
        <div class="absolute top-3 left-3 flex max-h-[calc(100%-4.5rem)] w-64 flex-col gap-3 overflow-y-auto rounded-lg border border-outline bg-surface/90 p-3 text-xs backdrop-blur"
            x-data="{ open: window.innerWidth >= 768 }">
            <button type="button" class="flex items-center justify-between font-medium text-white" x-on:click="open = ! open">
                Filtros <flux:icon name="adjustments-horizontal" variant="micro" />
            </button>
            <div x-show="open" class="flex flex-col gap-3">
                <form class="flex gap-1" x-on:submit.prevent="search">
                    <input type="search" x-model="query" placeholder="Buscar nodo o tema…" aria-label="Buscar nodo o tema"
                        class="w-full rounded-md border border-outline bg-surface-lowest px-2 py-1 text-ink focus:outline-none focus:ring-2 focus:ring-accent">
                </form>
                <p x-show="notFound" x-cloak class="text-warning">No está entre lo que se ve.</p>

                <div class="flex flex-col gap-1">
                    <p class="tech-label">Cursos</p>
                    @foreach ($graph['courses'] as $course)
                        @continue(! $course['nodes'] && ! $course['upcoming'])
                        <label class="flex items-center gap-2 text-ink">
                            <input type="checkbox" value="{{ $course['id'] }}" x-model.number="courses">
                            <span class="size-2.5 rounded-full" style="background: {{ $course['color'] }}"></span>
                            <span class="truncate">{{ $course['title'] }}</span>
                            @if ($course['upcoming'])
                                <span class="text-ink-muted">(próx.)</span>
                            @endif
                        </label>
                    @endforeach
                </div>

                @foreach (['compartido' => 'Temas compartidos', 'lenguaje' => 'Temas de cada lenguaje'] as $scope => $heading)
                    <div class="flex flex-col gap-1">
                        <div class="flex items-center justify-between">
                            <p class="tech-label">{{ $heading }}</p>
                            <span class="flex gap-2">
                                <button type="button" class="text-primary-bright hover:underline" x-on:click="toggleScope('{{ $scope }}', true)">todos</button>
                                <button type="button" class="text-ink-muted hover:underline" x-on:click="toggleScope('{{ $scope }}', false)">ninguno</button>
                            </span>
                        </div>
                        @foreach (collect($graph['families'])->where('scope', $scope) as $family)
                            <label class="flex items-center gap-2 text-ink">
                                <input type="checkbox" value="{{ $family['key'] }}" x-model="families">
                                <span class="size-2.5 rotate-45" style="background: {{ $familyColors[$family['key']] }}"></span>
                                <span class="truncate">{{ $family['title'] }}</span>
                            </label>
                        @endforeach
                    </div>
                @endforeach

                <div class="flex flex-col gap-1">
                    <p class="tech-label">Mostrar</p>
                    <label class="flex items-center gap-2 text-ink"><input type="checkbox" x-model="missing"> Temas que faltan</label>
                    <label class="flex items-center gap-2 text-ink"><input type="checkbox" x-model="uses"> Lo que cada nodo usa</label>
                </div>
            </div>
        </div>

        {{-- Leyenda y controles --}}
        <div class="pointer-events-none absolute right-3 bottom-3 flex flex-col items-end gap-1 text-[11px] text-ink-muted">
            <span class="flex items-center gap-1.5"><span class="size-2.5 rounded-full bg-ink"></span> curso · nodo (color del curso)</span>
            <span class="flex items-center gap-1.5"><span class="size-2.5 rotate-45 bg-secondary-bright"></span> tema (color de su familia; brilla si se repite)</span>
            <span class="flex items-center gap-1.5"><span class="size-2.5 rotate-45 bg-[#ef4444]"></span> falta y algún nodo lo usa</span>
            <span class="flex items-center gap-1.5"><span class="size-2.5 rotate-45 bg-[#475569]"></span> falta (nadie lo enseña)</span>
        </div>
        <div class="absolute bottom-3 left-3 flex gap-2">
            <flux:button size="xs" icon="viewfinder-circle" x-on:click="fit">Ver todo</flux:button>
            <flux:button size="xs" icon="cube" x-on:click="toggleDimensions"><span x-text="dimensions === 3 ? 'Ver en 2D' : 'Ver en 3D'">Ver en 2D</span></flux:button>
            <flux:button size="xs" icon="arrows-pointing-out" x-on:click="document.fullscreenElement ? document.exitFullscreen() : $root.requestFullscreen()">Pantalla completa</flux:button>
        </div>

        {{-- Detalle de lo elegido --}}
        <aside x-show="selected" x-cloak x-transition
            class="absolute top-3 right-3 flex max-h-[calc(100%-6rem)] w-80 flex-col gap-3 overflow-y-auto rounded-lg border border-outline bg-surface/95 p-4 text-sm backdrop-blur"
            data-test="universe-detail">
            <template x-if="selected">
                <div class="flex flex-col gap-3">
                    <div class="flex items-start justify-between gap-2">
                        <div class="flex min-w-0 flex-col gap-0.5">
                            <p class="tech-label" x-text="selected.kind === 'node' ? selected.course + ' · ' + selected.code : selected.kind === 'topic' ? selected.family + ' · ' + selected.key : 'Curso'"></p>
                            <p class="font-display text-base font-semibold" x-bind:style="{ color: selected.color }" x-text="selected.title"></p>
                        </div>
                        <button type="button" class="text-ink-muted hover:text-ink" x-on:click="selected = null" aria-label="Cerrar"><flux:icon name="x-mark" variant="micro" /></button>
                    </div>

                    {{-- Curso --}}
                    <template x-if="selected.kind === 'course'">
                        <div class="flex flex-col gap-2">
                            <p class="text-ink" x-text="selected.nodes + ' nodos' + (selected.upcoming ? ' · próximamente' : '')"></p>
                            <a x-bind:href="selected.url" wire:navigate class="text-primary-bright hover:underline">Abrir su árbol</a>
                        </div>
                    </template>

                    {{-- Nodo --}}
                    <template x-if="selected.kind === 'node'">
                        <div class="flex flex-col gap-3">
                            <p class="text-xs text-ink-muted" x-text="(selected.branch ?? 'Raíz') + (selected.published ? '' : ' · sin publicar')"></p>
                            <div class="flex flex-col gap-1">
                                <p class="tech-label">Enseña</p>
                                <p x-show="! selected.teaches.length" class="text-ink-muted">Nada nuevo (integra lo anterior).</p>
                                <template x-for="topic in selected.teaches" :key="topic.key">
                                    <div class="flex flex-col gap-0.5">
                                        <button type="button" class="text-start hover:underline" x-bind:style="{ color: topic.color }" x-on:click="go(topic.id)" x-text="'◆ ' + topic.title"></button>
                                        <template x-for="other in topic.others" :key="other.id">
                                            <button type="button" class="ms-4 text-start text-xs text-ink-muted hover:text-ink" x-on:click="go(other.id)">
                                                también en <span x-bind:style="{ color: other.color }" x-text="other.course"></span> · <span x-text="other.title"></span>
                                            </button>
                                        </template>
                                    </div>
                                </template>
                            </div>
                            <div class="flex flex-col gap-1" x-show="selected.uses.length">
                                <p class="tech-label">Da por sabido</p>
                                <template x-for="topic in selected.uses" :key="topic.key">
                                    <div class="flex flex-col gap-0.5">
                                        <button type="button" class="text-start hover:underline" x-bind:style="{ color: topic.color }" x-on:click="go(topic.id)" x-text="'◇ ' + topic.title"></button>
                                        <p x-show="! topic.taughtBy.length" class="ms-4 text-xs text-danger">Ningún curso lo enseña.</p>
                                        <template x-for="other in topic.taughtBy" :key="other.id">
                                            <button type="button" class="ms-4 text-start text-xs text-ink-muted hover:text-ink" x-on:click="go(other.id)">
                                                se enseña en <span x-bind:style="{ color: other.color }" x-text="other.course"></span> · <span x-text="other.title"></span>
                                            </button>
                                        </template>
                                    </div>
                                </template>
                            </div>
                            <div class="flex flex-col gap-1">
                                <p class="tech-label" x-text="'Prácticas (' + selected.practices.length + ')'"></p>
                                <ul class="flex flex-col gap-0.5 text-xs text-ink">
                                    <template x-for="(practice, i) in selected.practices" :key="i">
                                        <li class="flex gap-1.5"><span x-text="practice.required ? '●' : '○'" class="text-ink-muted"></span><span x-text="practice.title"></span></li>
                                    </template>
                                </ul>
                            </div>
                            <a x-bind:href="selected.url" wire:navigate class="text-primary-bright hover:underline">Editar el nodo</a>
                        </div>
                    </template>

                    {{-- Tema --}}
                    <template x-if="selected.kind === 'topic'">
                        <div class="flex flex-col gap-3">
                            <p class="text-ink" x-text="selected.description"></p>
                            <p class="text-xs" x-bind:class="selected.status === 'needed' ? 'text-danger' : selected.status === 'repeated' ? 'text-warning' : 'text-ink-muted'"
                                x-text="selected.statusLabel + (selected.scope === 'lenguaje' ? ' · cada lenguaje lo enseña a su manera' : '')"></p>
                            <div class="flex flex-col gap-1">
                                <p class="tech-label" x-text="'Lo enseñan (' + selected.taught.length + ')'"></p>
                                <template x-for="node in selected.taught" :key="node.id">
                                    <button type="button" class="text-start text-xs text-ink hover:underline" x-on:click="go(node.id)">
                                        <span x-bind:style="{ color: node.color }" x-text="node.course"></span> · <span x-text="node.title"></span>
                                    </button>
                                </template>
                            </div>
                            <div class="flex flex-col gap-1" x-show="selected.used.length">
                                <p class="tech-label" x-text="'Lo usan (' + selected.used.length + ')'"></p>
                                <template x-for="node in selected.used" :key="node.id">
                                    <button type="button" class="text-start text-xs text-ink hover:underline" x-on:click="go(node.id)">
                                        <span x-bind:style="{ color: node.color }" x-text="node.course"></span> · <span x-text="node.title"></span>
                                    </button>
                                </template>
                            </div>
                        </div>
                    </template>
                </div>
            </template>
        </aside>
    </section>

    <div class="mx-auto flex w-full max-w-7xl flex-col gap-8 px-4 sm:px-8">
    {{-- Resumen --}}
    @php
        $allShared = $shared->flatMap(fn ($f) => $f['rows']);
    @endphp
    <section class="grid grid-cols-2 gap-3 sm:grid-cols-4" data-test="universe-summary">
        @foreach ([
            ['Temas compartidos enseñados', $shared->sum('taught').' / '.$allShared->count()],
            ['Repetidos entre cursos', $shared->sum('repeated')],
            ['Faltan y algún nodo los usa', $shared->sum('needed') + $language->sum('needed')],
            ['Nodos sin temas', $untagged],
        ] as [$label, $value])
            <div class="panel flex flex-col gap-1 p-4">
                <p class="tech-label">{{ $label }}</p>
                <p class="font-display text-2xl font-semibold text-white">{{ $value }}</p>
            </div>
        @endforeach
    </section>

    @if ($loose->isNotEmpty())
        <flux:callout icon="exclamation-triangle" color="amber">
            <flux:callout.heading>Temas que no están en el catálogo</flux:callout.heading>
            <flux:callout.text>{{ $loose->pluck('key')->implode(', ') }}. Agregalos a cursos/temas.md o corregí el Markdown del curso.</flux:callout.text>
        </flux:callout>
    @endif

    {{-- Temas compartidos: lo que se puede reusar entre cursos --}}
    <section class="flex flex-col gap-4">
        <div>
            <h2 class="font-display text-lg font-semibold text-white">Temas compartidos</h2>
            <flux:text>Lo que se puede reusar entre cursos: si dos cursos lo enseñan, está repetido; un curso nuevo de la familia se arma con lo que ya existe.</flux:text>
        </div>
        @foreach ($shared as $family)
            <details class="panel group p-4" @if ($family['needed'] || $family['repeated']) open @endif>
                <summary class="flex cursor-pointer flex-wrap items-center gap-3">
                    <span class="size-3 rotate-45" style="background: {{ $familyColors[$family['key']] }}"></span>
                    <span class="font-medium text-white">{{ $family['title'] }}</span>
                    <span class="text-xs text-ink-muted">{{ $family['taught'] }}/{{ $family['rows']->count() }} enseñados</span>
                    @if ($family['repeated'])
                        <flux:badge size="sm" color="amber">{{ $family['repeated'] }} repetidos</flux:badge>
                    @endif
                    @if ($family['needed'])
                        <flux:badge size="sm" color="red">{{ $family['needed'] }} faltan y se usan</flux:badge>
                    @endif
                </summary>
                <div class="mt-3 overflow-x-auto">
                    <table class="w-full text-sm">
                        <thead class="text-left text-xs text-ink-muted">
                            <tr><th class="py-1 pe-3 font-medium">Tema</th><th class="py-1 pe-3 font-medium">Lo enseña</th><th class="py-1 pe-3 font-medium">Lo usa</th><th class="py-1 font-medium">Estado</th></tr>
                        </thead>
                        <tbody>
                            @foreach ($family['rows'] as $row)
                                @php([$label, $color] = $status($row))
                                <tr class="border-t border-outline/60">
                                    <td class="py-1.5 pe-3 text-ink">{{ $row['title'] }} <span class="font-mono text-[11px] text-ink-muted">{{ $row['key'] }}</span></td>
                                    <td class="py-1.5 pe-3">
                                        @foreach ($row['taught_in'] as $courseId)
                                            <span class="me-1 inline-block rounded-full px-2 py-0.5 text-[11px]" style="background: {{ $chip($courseId)['color'] }}22; color: {{ $chip($courseId)['color'] }}">{{ $chip($courseId)['language'] }}</span>
                                        @endforeach
                                    </td>
                                    <td class="py-1.5 pe-3">
                                        @foreach ($row['used_in'] as $courseId)
                                            <span class="me-1 inline-block rounded-full border px-2 py-0.5 text-[11px]" style="border-color: {{ $chip($courseId)['color'] }}66; color: {{ $chip($courseId)['color'] }}">{{ $chip($courseId)['language'] }}</span>
                                        @endforeach
                                    </td>
                                    <td class="py-1.5"><flux:badge size="sm" :color="$color">{{ $label }}</flux:badge></td>
                                </tr>
                            @endforeach
                        </tbody>
                    </table>
                </div>
            </details>
        @endforeach
    </section>

    {{-- Cobertura por lenguaje: qué da cada curso de lo que cada lenguaje enseña a su manera --}}
    <section class="flex flex-col gap-4">
        <div>
            <h2 class="font-display text-lg font-semibold text-white">Cobertura de cada lenguaje</h2>
            <flux:text>Temas que cada lenguaje enseña a su manera (no es contenido repetido). Un hueco es un tema que ese curso todavía no da.</flux:text>
        </div>
        <div class="panel overflow-x-auto p-4">
            <table class="w-full text-sm" data-test="universe-coverage">
                <thead class="text-xs text-ink-muted">
                    <tr>
                        <th class="py-1 pe-3 text-left font-medium">Tema</th>
                        @foreach ($liveCourses as $course)
                            <th class="px-2 py-1 font-medium" style="color: {{ $course['color'] }}">{{ $course['language'] }}</th>
                        @endforeach
                    </tr>
                </thead>
                <tbody>
                    @foreach ($language as $family)
                        <tr><td colspan="{{ $liveCourses->count() + 1 }}" class="pt-4 pb-1 text-xs font-medium tracking-wide text-white uppercase">{{ $family['title'] }}</td></tr>
                        @foreach ($family['rows'] as $row)
                            <tr class="border-t border-outline/60">
                                <td class="py-1 pe-3 text-ink">{{ $row['title'] }}</td>
                                @foreach ($liveCourses as $course)
                                    <td class="px-2 py-1 text-center">
                                        @if ($row['taught_in']->contains($course['id']))
                                            <span style="color: {{ $course['color'] }}" title="Lo enseña">●</span>
                                        @elseif ($row['used_in']->contains($course['id']))
                                            <span class="text-danger" title="Lo usa sin enseñarlo">◇</span>
                                        @else
                                            <span class="text-outline">·</span>
                                        @endif
                                    </td>
                                @endforeach
                            </tr>
                        @endforeach
                    @endforeach
                </tbody>
            </table>
        </div>
    </section>
    </div>
</div>
