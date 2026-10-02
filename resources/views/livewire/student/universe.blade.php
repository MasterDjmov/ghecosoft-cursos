{{-- El Universo para el alumno (D81): mirar, girar y votar «Quiero aprender esto». No cambia nada del curso. --}}
<div class="flex w-full flex-col gap-4 py-4 sm:py-6">
    <header class="mx-auto flex w-full max-w-7xl flex-col gap-1 px-4 sm:px-8">
        <p class="tech-label">Todos los mundos</p>
        <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">El Universo del Código</h1>
        <p class="max-w-3xl text-ink-muted">Cada mundo es un lenguaje, y sus temas se tocan con los de los otros: lo que aprendés en uno te sirve en el siguiente. Girá con el mouse o el dedo, acercá y tocá lo que quieras. Los temas que <span class="text-warning">laten</span> todavía no los enseña ningún curso: votá los que te gustaría aprender.</p>
    </header>

    <section class="relative mx-2 h-[calc(100vh-11rem)] min-h-[520px] overflow-hidden rounded-lg border border-outline bg-[#05070d] sm:mx-4"
        x-data="universeMap(@js($graph), { student: true })" data-test="student-universe">
        <div x-ref="canvas" class="absolute inset-0" wire:ignore></div>

        {{-- Filtros --}}
        <div class="absolute top-3 left-3 flex max-h-[calc(100%-4.5rem)] w-60 flex-col gap-3 overflow-y-auto rounded-lg border border-outline bg-surface/90 p-3 text-xs backdrop-blur"
            x-data="{ open: window.innerWidth >= 768 }">
            <button type="button" class="flex items-center justify-between font-medium text-white" x-on:click="open = ! open">
                Mundos <flux:icon name="adjustments-horizontal" variant="micro" />
            </button>
            <div x-show="open" class="flex flex-col gap-2">
                <form class="flex gap-1" x-on:submit.prevent="search">
                    <input type="search" x-model="query" placeholder="Buscar un tema…" aria-label="Buscar un tema"
                        class="w-full rounded-md border border-outline bg-surface-lowest px-2 py-1 text-ink focus:outline-none focus:ring-2 focus:ring-accent">
                </form>
                <p x-show="notFound" x-cloak class="text-warning">No está entre lo que se ve.</p>
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
                <label class="mt-1 flex items-center gap-2 text-ink"><input type="checkbox" x-model="missing"> Temas por crear</label>
            </div>
        </div>

        {{-- Leyenda y controles --}}
        <div class="pointer-events-none absolute right-3 bottom-3 hidden flex-col items-end gap-1 text-[11px] text-ink-muted sm:flex">
            <span class="flex items-center gap-1.5"><span class="size-2.5 rounded-full bg-ink"></span> un mundo y sus nodos</span>
            <span class="flex items-center gap-1.5"><span class="size-2.5 rounded-full bg-ink/30"></span> nodo por descubrir</span>
            <span class="flex items-center gap-1.5"><span class="size-2.5 rotate-45 bg-secondary-bright"></span> tema que se enseña</span>
            <span class="flex items-center gap-1.5"><span class="size-2.5 rotate-45 bg-warning"></span> tema por crear (laten los más pedidos)</span>
        </div>
        <div class="absolute bottom-3 left-3 flex gap-2">
            <flux:button size="xs" icon="viewfinder-circle" x-on:click="fit">Ver todo</flux:button>
            <flux:button size="xs" icon="arrows-pointing-out" x-on:click="document.fullscreenElement ? document.exitFullscreen() : $root.requestFullscreen()">Pantalla completa</flux:button>
        </div>

        {{-- Lo elegido --}}
        <aside x-show="selected" x-cloak x-transition
            class="absolute top-3 right-3 flex max-h-[calc(100%-6rem)] w-72 flex-col gap-3 overflow-y-auto rounded-lg border border-outline bg-surface/95 p-4 text-sm backdrop-blur"
            data-test="universe-detail">
            <template x-if="selected">
                <div class="flex flex-col gap-3">
                    <div class="flex items-start justify-between gap-2">
                        <div class="flex min-w-0 flex-col gap-0.5">
                            <p class="tech-label" x-text="selected.kind === 'node' ? selected.course : selected.kind === 'topic' ? selected.family : 'Mundo'"></p>
                            <p class="font-display text-base font-semibold" x-bind:style="{ color: selected.color }" x-text="selected.title ?? 'Un nodo por descubrir'"></p>
                        </div>
                        <button type="button" class="text-ink-muted hover:text-white" x-on:click="selected = null; map?.select(null)" aria-label="Cerrar">
                            <flux:icon name="x-mark" variant="micro" />
                        </button>
                    </div>

                    <template x-if="selected.kind === 'course'">
                        <div class="flex flex-col gap-2">
                            <p class="text-ink" x-text="selected.upcoming ? 'Próximamente: todavía se está preparando.' : selected.nodes + ' nodos para recorrer'"></p>
                            <a x-show="! selected.upcoming" x-bind:href="selected.url" wire:navigate class="text-primary-bright hover:underline">Ir a este mundo</a>
                        </div>
                    </template>

                    <template x-if="selected.kind === 'node'">
                        <div class="flex flex-col gap-2">
                            <p x-show="! selected.url" class="text-ink-muted">Todavía no lo abriste. Cuando llegues, vas a ver qué hay adentro.</p>
                            <a x-show="selected.url" x-bind:href="selected.url" wire:navigate class="text-primary-bright hover:underline">Ir al nodo</a>
                        </div>
                    </template>

                    <template x-if="selected.kind === 'topic'">
                        <div class="flex flex-col gap-2">
                            <p class="text-ink" x-text="selected.description"></p>
                            <p class="text-xs" x-bind:class="selected.canVote ? 'text-warning' : 'text-ink-muted'"
                                x-text="selected.canVote ? 'Todavía no lo enseña ningún curso.' : 'Lo enseñan ' + selected.taught.length + ' nodos de los cursos.'"></p>
                            <template x-for="reason in selected.reasons" :key="reason"><p class="text-xs text-ink-muted" x-text="'· ' + reason"></p></template>
                        </div>
                    </template>

                    {{-- «Quiero aprender esto»: un voto por tema o curso que viene --}}
                    <template x-if="selected.canVote">
                        <div class="flex flex-col gap-1.5 border-t border-outline pt-3" data-test="vote-box">
                            <button type="button" x-on:click="vote(selected.target)" x-bind:disabled="voting"
                                class="flex items-center justify-center gap-2 rounded-lg px-3 py-2 font-medium transition disabled:opacity-50"
                                x-bind:class="myVotes.includes(selected.target) ? 'bg-warning/20 text-warning ring-1 ring-warning/50' : 'bg-primary text-[#05070d] hover:bg-primary-bright'">
                                <flux:icon name="hand-raised" variant="micro" />
                                <span x-text="myVotes.includes(selected.target) ? '¡Lo pediste! (tocá para sacar el voto)' : 'Quiero aprender esto'"></span>
                            </button>
                            <p class="text-center text-xs text-ink-muted" x-text="(votes[selected.target] ?? 0) === 1 ? '1 alumno lo quiere' : (votes[selected.target] ?? 0) + ' alumnos lo quieren'"></p>
                        </div>
                    </template>
                </div>
            </template>
        </aside>
    </section>
</div>
