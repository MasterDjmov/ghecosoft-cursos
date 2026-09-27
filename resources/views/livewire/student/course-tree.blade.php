@php
    use App\Services\TreeAccess;

    $nodes = collect($graph['nodes']);
    $practices = collect($graph['practices'])->groupBy('node_id');
    $root = $nodes->firstWhere('type', 'root');
    $branches = collect($graph['branches'])->sortBy([['is_extra', 'asc'], ['position', 'asc']]);
    $loose = $nodes->where('type', '!=', 'root')->filter(fn ($n) => ! $branches->contains('id', $n['branch_id']));
    $total = $nodes->count();
@endphp

<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8"
    x-data="{ tab: (() => { try { return localStorage.getItem('tree-tab') } catch (e) { return null } })() ?? (window.innerWidth < 768 ? 'list' : 'tree') }"
    x-init="$watch('tab', value => { try { localStorage.setItem('tree-tab', value) } catch (e) {} })">

    <header class="flex flex-col gap-4 sm:flex-row sm:items-center">
        <x-course-logo :course="$course" size="size-14" />
        <div class="flex min-w-0 flex-1 flex-col gap-1">
            <p class="tech-label">{{ term('world.name') }} · {{ $course->title }}</p>
            <h1 class="font-display text-2xl font-semibold text-white">Tu árbol</h1>
            <p class="text-sm text-ink-muted">
                {{ $completed }}/{{ $total }} {{ term('node', $course, $total) }} completados ·
                <a href="{{ route('student.ranking.course', $course) }}" wire:navigate class="text-primary-bright hover:underline">Top 10 del curso</a>
            </p>
        </div>
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

    <x-wallet-bar class="sm:hidden" />

    @unless ($subscription)
        <flux:callout icon="clock" color="amber">
            <flux:callout.heading>Tu abono no está vigente</flux:callout.heading>
            <flux:callout.text>
                Podés repasar todo lo que abriste. Para abrir {{ term('node', $course, 2) }} nuevos y entregar,
                <flux:link :href="route('student.course', $course)" wire:navigate>renová el abono</flux:link>.
            </flux:callout.text>
        </flux:callout>
    @endunless

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
