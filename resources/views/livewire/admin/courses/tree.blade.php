<div class="mx-auto flex w-full max-w-6xl flex-col gap-8 p-4 sm:p-8">
    <x-admin.page-header :label="'Cursos · '.$course->title" title="Árbol del curso"
        subtitle="Arrastrá los nodos para ordenarlos o pasarlos a otra rama. El requisito de cada nodo es el que tiene que completar el alumno antes de abrirlo.">
        <x-slot:actions>
            <flux:button variant="primary" icon="plus" wire:click="openBranch">Nueva rama</flux:button>
            <flux:button icon="pencil-square" :href="route('admin.courses.edit', $course)" wire:navigate>Datos del curso</flux:button>
            <flux:button variant="ghost" icon="arrow-left" :href="route('admin.courses.index')" wire:navigate>Cursos</flux:button>
        </x-slot:actions>
    </x-admin.page-header>

    {{-- Lista (para editar) o árbol dibujado (como lo verá el alumno) --}}
    <div class="flex flex-wrap items-center gap-3">
        <div class="inline-flex rounded-lg border border-outline bg-surface-low p-1" role="tablist">
            @foreach (['list' => ['Lista', 'list-bullet'], 'tree' => ['Árbol', 'share']] as $value => [$label, $icon])
                <button type="button" role="tab" wire:click="$set('view', '{{ $value }}')" aria-selected="{{ $view === $value ? 'true' : 'false' }}"
                    @class(['flex items-center gap-2 rounded-md px-3 py-1.5 text-sm font-medium transition',
                        'bg-primary-bright text-surface' => $view === $value,
                        'text-ink-muted hover:text-ink' => $view !== $value])>
                    <flux:icon :name="$icon" variant="micro" /> {{ $label }}
                </button>
            @endforeach
        </div>
        @if ($view === 'tree')
            <flux:text class="text-sm">Arrastrá un nodo para acomodarlo (se guarda solo). Tocá un nodo o una hoja para editarla.</flux:text>
        @endif
    </div>

    @if ($view === 'tree')
        <section class="relative h-[70vh] min-h-[480px] overflow-hidden rounded-lg border border-outline bg-[#05070d]/90"
            wire:key="graph-{{ md5(json_encode($graph)) }}"
            x-data="skillTree(@js($graph), { editable: true })">
            <div x-ref="canvas" class="absolute inset-0" wire:ignore></div>

            @include('livewire.admin.courses.partials.tree-legend')

            <div class="absolute bottom-3 left-3 flex gap-2">
                <flux:button size="xs" icon="arrows-pointing-out" x-on:click="fit">Ver todo</flux:button>
                <flux:button size="xs" variant="ghost" icon="arrow-path" wire:click="resetLayout"
                    wire:confirm="¿Volver a ubicar todos los nodos automáticamente? Se pierden los retoques a mano.">Reacomodar</flux:button>
            </div>
        </section>
    @else
    {{-- Raíz --}}
        @if ($root)
            <section class="panel panel-active flex flex-col gap-4 p-5 sm:flex-row sm:items-center" data-test="root-node">
                <x-course-logo :course="$course" size="size-16" />
                <div class="flex min-w-0 flex-1 flex-col gap-1">
                    <p class="tech-label">{{ term('node.root', $course) }}</p>
                    <h2 class="font-display text-xl font-semibold text-white">{{ $root->title }}</h2>
                    <p class="font-mono text-xs text-ink-muted">
                        {{ $root->price }} {{ term('coin.course', $course, $root->price) }} ·
                        {{ $root->required_count }} obligatorias · {{ $root->optional_count }} optativas ·
                        pagan {{ (int) $root->required_reward }} {{ term('coin.course', $course, (int) $root->required_reward) }}
                    </p>
                </div>
                <div class="flex flex-wrap gap-2">
                    <flux:button size="sm" variant="primary" icon="pencil-square" :href="route('admin.nodes.edit', [$course, $root])" wire:navigate>Editar</flux:button>
                    <flux:button size="sm" icon="plus" :href="route('admin.nodes.edit', [$course, $root]).'?hoja=nueva'" wire:navigate>Nueva hoja</flux:button>
                </div>
            </section>
        @endif
    
        {{-- Ramas --}}
        <div class="flex flex-col gap-6" wire:sort="sortBranch">
            @foreach ($branches as $branch)
                <section class="panel flex flex-col gap-4 p-4 sm:p-5" wire:key="branch-{{ $branch->id }}" wire:sort:item="{{ $branch->id }}" data-test="branch-{{ $branch->id }}">
                    <header class="flex items-center gap-2 sm:gap-3">
                        <flux:icon name="bars-3" class="size-5 cursor-grab text-ink-muted" wire:sort:handle />
                        <h2 class="min-w-0 flex-1 truncate font-display text-lg font-semibold text-white">
                            {{ $branch->title }}
                            @if ($branch->is_extra)
                                <flux:badge size="sm" color="violet" class="ms-2 align-middle">Extras</flux:badge>
                            @endif
                        </h2>
                        <flux:button size="sm" icon="plus" wire:click="openNode({{ $branch->id }})">Nodo</flux:button>
                        <flux:dropdown position="bottom" align="end">
                            <flux:button size="sm" variant="ghost" icon="ellipsis-horizontal" aria-label="Opciones de la rama" />
                            <flux:menu>
                                <flux:menu.item icon="pencil-square" wire:click="openBranch({{ $branch->id }})">Renombrar</flux:menu.item>
                                <flux:menu.item icon="trash" variant="danger" wire:click="deleteBranch({{ $branch->id }})" wire:confirm="¿Borrar la rama «{{ $branch->title }}»?">Borrar rama</flux:menu.item>
                            </flux:menu>
                        </flux:dropdown>
                    </header>
    
                    @include('livewire.admin.courses.partials.node-list', ['nodes' => $nodesByBranch[$branch->id] ?? collect(), 'groupId' => $branch->id])
                </section>
            @endforeach
        </div>
    
        {{-- Nodos sueltos (sin rama) --}}
        @if (isset($nodesByBranch['none']) || $branches->isEmpty())
            <section class="panel flex flex-col gap-4 p-4 sm:p-5">
                <header class="flex items-center gap-3">
                    <h2 class="font-display text-lg font-semibold text-white">Sin rama</h2>
                    <flux:spacer />
                    <flux:button size="sm" icon="plus" wire:click="openNode">Nodo</flux:button>
                </header>
                @if ($branches->isEmpty())
                    <flux:text>Creá una rama (por ejemplo «Fundamentos») para agrupar los nodos. Cada rama termina en un jefe.</flux:text>
                @endif
                @include('livewire.admin.courses.partials.node-list', ['nodes' => $nodesByBranch['none'] ?? collect(), 'groupId' => 'none'])
            </section>
        @endif
    @endif

    {{-- Modal: rama --}}
    <flux:modal name="branch" class="w-full max-w-md">
        <form wire:submit="saveBranch" class="flex flex-col gap-5">
            <flux:heading size="lg">{{ $branchId ? 'Renombrar rama' : 'Nueva rama' }}</flux:heading>
            <flux:input wire:model="branchTitle" label="Nombre" placeholder="Fundamentos" autofocus />
            <flux:checkbox wire:model="branchIsExtra" label="Es una rama de extras" description="Nodos optativos, en el anillo exterior del árbol." />
            <div class="flex justify-end gap-2">
                <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                <flux:button variant="primary" type="submit">Guardar</flux:button>
            </div>
        </form>
    </flux:modal>

    {{-- Modal: nodo nuevo --}}
    <flux:modal name="node" class="w-full max-w-lg">
        <form wire:submit="saveNode" class="flex flex-col gap-5">
            <flux:heading size="lg">Nuevo nodo</flux:heading>
            <flux:input wire:model="nodeTitle" label="Título" placeholder="Variables" autofocus />

            <flux:radio.group wire:model.live="nodeType" label="Tipo" variant="segmented">
                @foreach ($nodeTypes as $type)
                    <flux:radio :value="$type->value" :label="$type->label()" />
                @endforeach
            </flux:radio.group>

            <flux:select wire:model="nodeParentId" label="Requisito" description="El alumno tiene que completar este nodo antes de abrir el nuevo.">
                @foreach ($parentOptions as $option)
                    <flux:select.option :value="$option->id">{{ $option->isRoot() ? '★ ' : '' }}{{ $option->title }}</flux:select.option>
                @endforeach
            </flux:select>

            <div class="grid gap-4 sm:grid-cols-2">
                <flux:input wire:model="nodePrice" type="number" min="0" label="Precio" />
                @if ($nodeType === 'extra')
                    <flux:select wire:model="nodePaidWith" label="Se paga con">
                        <flux:select.option value="course">{{ ucfirst(term('coin.course', $course, 2)) }}</flux:select.option>
                        <flux:select.option value="wildcard">{{ ucfirst(term('coin.wildcard', null, 2)) }}</flux:select.option>
                    </flux:select>
                @endif
            </div>

            <div class="flex justify-end gap-2">
                <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                <flux:button variant="primary" type="submit">Crear y editar</flux:button>
            </div>
        </form>
    </flux:modal>

    {{-- Modal: borrar nodo --}}
    <flux:modal name="delete-node" class="w-full max-w-md">
        <div class="flex flex-col gap-4">
            <flux:heading size="lg">¿Borrar «{{ $deletingNode?->title }}»?</flux:heading>
            <flux:text>Se borran sus hojas y recursos. Si algún alumno ya lo abrió, no se puede: despublicalo.</flux:text>
            <div class="flex justify-end gap-2">
                <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                <flux:button variant="danger" wire:click="deleteNode">Borrar</flux:button>
            </div>
        </div>
    </flux:modal>
</div>
