<div class="mx-auto flex w-full max-w-6xl flex-col gap-8 p-4 sm:p-8">
    <x-admin.page-header title="Cursos" subtitle="Cada curso es un mundo con su árbol. Arrastrá para cambiar el orden del mapa.">
        <x-slot:actions>
            <flux:button icon="arrow-down-tray" :href="route('admin.courses.import')" wire:navigate>Importar</flux:button>
            <flux:button variant="primary" icon="plus" :href="route('admin.courses.create')" wire:navigate>Nuevo curso</flux:button>
        </x-slot:actions>
    </x-admin.page-header>

    <div class="flex flex-col gap-3" wire:sort="sort">
        @forelse ($courses as $course)
            <article class="panel flex flex-col gap-4 p-4 sm:flex-row sm:items-center" wire:key="course-{{ $course->id }}" wire:sort:item="{{ $course->id }}">
                <div class="flex items-center gap-4 sm:flex-1">
                    <flux:icon name="bars-3" class="size-5 shrink-0 cursor-grab text-ink-muted" wire:sort:handle />
                    <x-course-logo :course="$course" size="size-12" />
                    <div class="flex min-w-0 flex-col gap-1">
                        <div class="flex flex-wrap items-center gap-2">
                            <h2 class="font-display text-lg font-semibold text-white">{{ $course->title }}</h2>
                            @if ($course->is_published)
                                <flux:badge size="sm" color="green">Publicado</flux:badge>
                            @else
                                <flux:badge size="sm">Borrador</flux:badge>
                            @endif
                        </div>
                        <p class="font-mono text-xs text-ink-muted">
                            {{ $course->language->label() }} · {{ $course->branches_count }} ramas · {{ $course->nodes_count }} nodos ·
                            raíz {{ $course->root_price }} {{ term('coin.course', $course, $course->root_price) }} · abono {{ $course->subscription_days }} días ·
                            {{ $activeStudents[$course->id] ?? 0 }} con abono vigente
                        </p>
                    </div>
                </div>
                <div class="flex flex-wrap gap-2">
                    <flux:button size="sm" variant="primary" icon="share" :href="route('admin.courses.tree', $course)" wire:navigate>Árbol</flux:button>
                    <flux:button size="sm" icon="pencil-square" :href="route('admin.courses.edit', $course)" wire:navigate>Datos</flux:button>
                    <flux:button size="sm" variant="ghost" :icon="$course->is_published ? 'eye-slash' : 'eye'" wire:click="togglePublished({{ $course->id }})">
                        {{ $course->is_published ? 'Despublicar' : 'Publicar' }}
                    </flux:button>
                </div>
            </article>
        @empty
            <div class="panel p-8 text-center text-ink-muted">Todavía no creaste ningún curso.</div>
        @endforelse
    </div>
</div>
