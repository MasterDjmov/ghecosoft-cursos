<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header title="Insignias" subtitle="Se entregan al vencer a un jefe. Elegí cuál da cada jefe en el editor del nodo.">
        <x-slot:actions>
            <flux:button variant="primary" icon="plus" wire:click="create">Nueva insignia</flux:button>
        </x-slot:actions>
    </x-admin.page-header>

    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        @forelse ($badges as $badge)
            <article class="panel flex flex-col gap-3 p-5" wire:key="badge-{{ $badge->id }}">
                <div class="flex items-start gap-3">
                    @if ($badge->iconUrl())
                        <img src="{{ $badge->iconUrl() }}" alt="" class="size-14 shrink-0 rounded-full border border-warning/50 object-cover">
                    @else
                        <div class="grid size-14 shrink-0 place-items-center rounded-full border border-warning/50 bg-warning/10">
                            <flux:icon name="trophy" class="size-7 text-warning" />
                        </div>
                    @endif
                    <div class="flex min-w-0 flex-col gap-1">
                        <h2 class="font-display font-semibold text-white">{{ $badge->name }}</h2>
                        <p class="font-mono text-[11px] text-ink-muted">{{ $badge->code }} · {{ $badge->course?->title ?? 'General' }}</p>
                    </div>
                </div>
                @if ($badge->description)
                    <p class="text-sm text-ink-muted">{{ $badge->description }}</p>
                @endif
                <p class="text-xs text-ink-muted">
                    @if ($badge->nodes->isNotEmpty())
                        La da: {{ $badge->nodes->pluck('title')->join(', ') }}
                    @else
                        Ningún jefe la entrega todavía.
                    @endif
                    · {{ $badge->users_count }} {{ $badge->users_count === 1 ? 'alumno la ganó' : 'alumnos la ganaron' }}
                </p>
                <div class="mt-auto flex gap-1">
                    <flux:button size="xs" icon="pencil-square" wire:click="edit({{ $badge->id }})">Editar</flux:button>
                    <flux:button size="xs" variant="ghost" icon="trash" wire:click="delete({{ $badge->id }})" wire:confirm="¿Borrar la insignia «{{ $badge->name }}»?">Borrar</flux:button>
                </div>
            </article>
        @empty
            <div class="panel p-8 text-center text-ink-muted sm:col-span-2 lg:col-span-3">Todavía no hay insignias.</div>
        @endforelse
    </div>

    <flux:modal name="badge" class="w-full max-w-lg">
        <form wire:submit="save" class="flex flex-col gap-5">
            <flux:heading size="lg">{{ $badgeId ? 'Editar insignia' : 'Nueva insignia' }}</flux:heading>
            <div class="grid gap-5 sm:grid-cols-2">
                <flux:input wire:model.live.debounce.400ms="name" label="Nombre" placeholder="Cazador de slimes" />
                <flux:input wire:model="code" label="Código" description:trailing="Fijo, sin espacios." />
            </div>
            <flux:input wire:model="description" label="Descripción" placeholder="Venciste al Rey Slime." />
            <flux:select wire:model="course_id" label="Curso">
                <flux:select.option value="">General</flux:select.option>
                @foreach ($courses as $option)
                    <flux:select.option :value="(string) $option->id">{{ $option->title }}</flux:select.option>
                @endforeach
            </flux:select>
            <div class="flex flex-col gap-2">
                <flux:label>Imagen (opcional)</flux:label>
                <div class="flex items-center gap-3">
                    @if ($icon && $icon->isPreviewable())
                        <img src="{{ $icon->temporaryUrl() }}" alt="" class="size-12 rounded-full object-cover">
                    @endif
                    <input type="file" wire:model="icon" accept="image/png,image/jpeg,image/webp"
                        class="text-sm text-ink-muted file:me-3 file:rounded-md file:border-0 file:bg-surface-highest file:px-3 file:py-2 file:text-ink hover:file:bg-surface-high">
                </div>
                <flux:error name="icon" />
            </div>
            <div class="flex justify-end gap-2">
                <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                <flux:button variant="primary" type="submit">Guardar</flux:button>
            </div>
        </form>
    </flux:modal>
</div>
