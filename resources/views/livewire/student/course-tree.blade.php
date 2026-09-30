@php
    use App\Services\TreeAccess;

    $nodes = collect($graph['nodes']);
    $practices = collect($graph['practices'])->groupBy('node_id');
    $root = $nodes->firstWhere('type', 'root');
    $branches = collect($graph['branches'])->sortBy([['is_extra', 'asc'], ['position', 'asc']]);
    $loose = $nodes->where('type', '!=', 'root')->filter(fn ($n) => ! $branches->contains('id', $n['branch_id']));
    // El progreso cuenta el tronco (como "curso completado" y el CV); Sendas y extras van aparte.
    $kinds = collect($graph['branches'])->pluck('kind', 'id');
    $isTrunk = fn ($n) => $n['type'] !== 'extra' && ($n['branch_id'] === null || ($kinds[$n['branch_id']] ?? 'trunk') === 'trunk');
    $trunk = $nodes->filter($isTrunk);
    $trunkDone = $trunk->where('state', 'completed')->count();
    $branchDone = fn ($branchId) => ($branchNodes = $nodes->where('branch_id', $branchId))->isNotEmpty()
        && $branchNodes->every(fn ($n) => $n['state'] === 'completed');
    $optional = $branches->filter(fn ($b) => $b['kind'] !== 'trunk')
        ->map(fn ($b) => ['branch' => $b, 'nodes' => $nodes->where('branch_id', $b['id'])])
        ->filter(fn ($item) => $item['nodes']->isNotEmpty());
@endphp

<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8"
    x-data="{ tab: (() => { try { return localStorage.getItem('tree-tab') } catch (e) { return null } })() ?? (window.innerWidth < 768 ? 'list' : 'tree') }"
    x-init="$watch('tab', value => { try { localStorage.setItem('tree-tab', value) } catch (e) {} })">

    <header class="flex flex-col gap-4 sm:flex-row sm:items-center">
        <x-course-logo :course="$course" size="size-16" />
        <div class="flex min-w-0 flex-1 flex-col gap-1">
            <p class="tech-label">{{ term('world.name') }} · {{ $course->title }}</p>
            <h1 class="font-display text-2xl font-semibold text-white">Tu árbol</h1>
            <p class="text-sm text-ink-muted">
                <span data-test="trunk-progress">{{ $trunkDone }}/{{ $trunk->count() }} {{ term('node', $course, $trunk->count()) }} del camino principal</span> ·
                <a href="{{ route('student.ranking.course', $course) }}" wire:navigate class="text-primary-bright hover:underline">Top 10 del curso</a>
            </p>
        </div>
        @if ($paidUntil)
            <x-subscription-countdown :until="$paidUntil" :total="$course->subscription_days" class="self-start sm:self-center" />
        @endif
        <div class="inline-flex self-start rounded-lg border border-outline bg-surface-low p-1 sm:self-center" role="tablist">
            <button type="button" role="tab" x-on:click="tab = 'tree'" class="flex items-center gap-2 rounded-md px-3 py-1.5 text-sm font-medium transition"
                x-bind:class="tab === 'tree' ? 'bg-primary-bright text-surface' : 'text-ink-muted hover:text-ink'">
                <flux:icon name="share" variant="micro" /> Árbol
            </button>
            <button type="button" role="tab" x-on:click="tab = 'list'" class="flex items-center gap-2 rounded-md px-3 py-1.5 text-sm font-medium transition"
                x-bind:class="tab === 'list' ? 'bg-primary-bright text-surface' : 'text-ink-muted hover:text-ink'">
                <flux:icon name="list-bullet" variant="micro" /> Lista
            </button>
        </div>
    </header>

    {{-- Fin del curso --}}
    @if ($finale)
        <x-story-card :story="$finale" :course="$course" icon="trophy" tone="success" data-test="course-finale">
            <div>
                <flux:button size="sm" icon="identification" :href="route('cv.show', auth()->user()->cv_slug)" target="_blank">Ver mi CV</flux:button>
            </div>
        </x-story-card>
    @endif

    {{-- Bienvenida: se puede cerrar; queda un botón para volver a verla. --}}
    @if ($intro)
        <div x-data="{ hidden: (() => { try { return localStorage.getItem('story-intro-{{ $course->id }}') === '1' } catch (e) { return false } })() }">
            <div x-show="! hidden">
                <x-story-card :story="$intro" :course="$course" icon="book-open" data-test="course-intro">
                    <div class="flex justify-end">
                        <flux:button size="xs" variant="ghost" icon="x-mark" x-on:click="hidden = true; try { localStorage.setItem('story-intro-{{ $course->id }}', '1') } catch (e) {}">Cerrar</flux:button>
                    </div>
                </x-story-card>
            </div>
            <button type="button" x-show="hidden" x-cloak class="flex items-center gap-1.5 text-xs text-secondary-bright hover:underline"
                x-on:click="hidden = false; try { localStorage.removeItem('story-intro-{{ $course->id }}') } catch (e) {}">
                <flux:icon name="book-open" variant="micro" /> {{ $intro['title'] }}
            </button>
        </div>
    @endif

    @if ($optional->isNotEmpty())
        <div class="-mt-2 flex flex-wrap gap-2" data-test="optional-progress">
            @foreach ($optional as $item)
                <span @class([
                    'rounded-full border px-2.5 py-1 text-xs',
                    'border-[#f472b6]/50 text-[#f9a8d4]' => $item['branch']['kind'] === 'path',
                    'border-secondary/50 text-secondary-bright' => $item['branch']['kind'] === 'extra',
                ])>
                    {{ $item['branch']['title'] }} · {{ $item['nodes']->where('state', 'completed')->count() }}/{{ $item['nodes']->count() }}
                </span>
            @endforeach
        </div>
    @endif

    <x-wallet-bar class="sm:hidden" />

    @if ($trial)
        <flux:callout icon="sparkles" color="cyan" data-test="trial-banner">
            <flux:callout.heading>Estás probando {{ $course->title }} gratis</flux:callout.heading>
            <flux:callout.text>
                Entrá a la clase 0 sin pagar: leé, mirá el ejemplo y practicá. Para que el profe te corrija y abrir el resto del árbol,
                <flux:link :href="route('student.course', $course)" wire:navigate>pedí tu abono</flux:link> (el mes empieza a correr cuando se aprueba).
            </flux:callout.text>
        </flux:callout>
    @elseif (! $subscription && ! $staff)
        <flux:callout icon="clock" color="amber">
            <flux:callout.heading>Tu abono no está vigente</flux:callout.heading>
            <flux:callout.text>
                Podés repasar todo lo que abriste. Para abrir {{ term('node', $course, 2) }} nuevos y entregar,
                <flux:link :href="route('student.course', $course)" wire:navigate>renová el abono</flux:link>.
            </flux:callout.text>
        </flux:callout>
    @endif

    {{-- Árbol dibujado --}}
    <template x-if="tab === 'tree'">
        <section class="relative h-[72vh] min-h-[460px] overflow-hidden rounded-lg border border-outline bg-[#05070d]/90"
            wire:key="student-graph-{{ md5(json_encode($graph)) }}"
            x-data="skillTree(@js($graph))">
            <div x-ref="canvas" class="absolute inset-0" wire:ignore></div>
            @include('livewire.student.partials.tree-legend')
            <div class="absolute bottom-3 left-3">
                <flux:button size="xs" icon="arrows-pointing-out" x-on:click="fit">Ver todo</flux:button>
            </div>
        </section>
    </template>

    {{-- Lista por rama --}}
    <div x-show="tab === 'list'" x-cloak class="flex flex-col gap-5">
        @if ($root)
            @include('livewire.student.partials.tree-row', ['node' => $root, 'leaves' => $practices[$root['id']] ?? collect()])
        @endif

        @foreach ($branches as $branch)
            @php($branchNodes = $nodes->where('branch_id', $branch['id'])->sortBy('position'))
            @continue($branchNodes->isEmpty())
            <section class="flex flex-col gap-2">
                <h2 class="flex items-center gap-2 font-display text-lg font-semibold text-white">
                    {{ $branch['title'] }}
                    @if ($branchDone($branch['id']))
                        <flux:badge size="sm" color="green" icon="check">Completada</flux:badge>
                    @endif
                    @if ($branch['kind'] === 'path')
                        <flux:badge size="sm" color="pink">{{ ucfirst(term('branch.path', $course)) }}</flux:badge>
                    @elseif ($branch['is_extra'])
                        <flux:badge size="sm" color="violet">Extras</flux:badge>
                    @endif
                </h2>
                <ol class="flex flex-col gap-2 border-s border-outline ps-4">
                    @foreach ($branchNodes as $node)
                        @include('livewire.student.partials.tree-row', ['node' => $node, 'leaves' => $practices[$node['id']] ?? collect()])
                    @endforeach
                </ol>
            </section>
        @endforeach

        @if ($loose->isNotEmpty())
            <section class="flex flex-col gap-2">
                <ol class="flex flex-col gap-2">
                    @foreach ($loose->sortBy('position') as $node)
                        @include('livewire.student.partials.tree-row', ['node' => $node, 'leaves' => $practices[$node['id']] ?? collect()])
                    @endforeach
                </ol>
            </section>
        @endif
    </div>

    {{-- Nodo cerrado: precio, motivos y Abrir --}}
    <flux:modal name="node" class="w-full max-w-md">
        @if ($selected)
            <div class="flex flex-col gap-4">
                <div class="flex flex-col gap-1">
                    <p class="tech-label">{{ term('state.'.$selected['state'], $course) }}</p>
                    <flux:heading size="lg">{{ $selected['title'] }}</flux:heading>
                </div>
                <p class="text-ink">Cuesta <strong class="text-white">{{ $selected['price_label'] }}</strong>.</p>
                @if ($selected['blockers'])
                    <ul class="flex flex-col gap-1 text-sm text-warning">
                        @foreach ($selected['blockers'] as $blocker)
                            <li class="flex items-start gap-2"><flux:icon name="lock-closed" variant="micro" class="mt-0.5 shrink-0" /> {{ $blocker }}</li>
                        @endforeach
                    </ul>
                @endif
                <div class="flex justify-end gap-2">
                    <flux:modal.close><flux:button variant="ghost">Cerrar</flux:button></flux:modal.close>
                    @if ($selectedCanUnlock)
                        <flux:button variant="primary" icon="lock-open" wire:click="unlock({{ $selected['id'] }})">Abrir por {{ $selected['price_label'] }}</flux:button>
                    @endif
                </div>
            </div>
        @endif
    </flux:modal>
</div>
