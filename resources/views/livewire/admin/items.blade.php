{{-- Juego → Ítems (D90). --}}
<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header label="Juego" title="Ítems"
        subtitle="Armas, ropa, accesorios, pociones, materiales y especiales. Los de un mundo se venden en su tienda (si tienen precio y «En la tienda») y caen en sus expediciones (si marcás «Cae en expediciones»). Un ítem nunca cambia lo que el alumno puede programar: solo el juego." />

    <div class="flex flex-col gap-3 sm:flex-row sm:items-end">
        <flux:select wire:model.live="world" label="Mundo" class="sm:w-72">
            <flux:select.option value="">Todos</flux:select.option>
            <flux:select.option value="comunes">Comunes (todos los mundos)</flux:select.option>
            @foreach ($courses as $course)
                <flux:select.option :value="(string) $course->id">{{ $course->title }}</flux:select.option>
            @endforeach
        </flux:select>
        <flux:button variant="primary" icon="plus" wire:click="create" class="sm:ms-auto" data-test="item-new">Nuevo ítem</flux:button>
    </div>

    @forelse ($items as $kind => $group)
        <section class="flex flex-col gap-3" wire:key="kind-{{ $kind }}">
            <h2 class="font-display text-lg font-semibold text-white">{{ \App\Enums\ItemKind::from($kind)->plural() }} <span class="text-sm text-ink-muted">{{ $group->count() }}</span></h2>
            <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                @foreach ($group as $item)
                    <x-item-card :item="$item" wire:key="item-{{ $item->id }}">
                        <div class="mt-auto flex flex-wrap items-center gap-x-3 gap-y-1 border-t border-outline/60 pt-2 text-xs text-ink-muted">
                            <span>{{ $item->course?->title ?? 'Común' }}</span>
                            @if ($item->in_shop)<span class="text-warning">Tienda: {{ $item->price }} oro · nivel {{ $item->min_level }}</span>@endif
                            @if ($item->droppable)<span class="text-sky-300">Cae en expediciones</span>@endif
                            @if ($owners[$item->id] ?? 0)<span>{{ $owners[$item->id] }} lo tienen</span>@endif
                            <span class="ms-auto flex gap-2">
                                <button type="button" wire:click="edit({{ $item->id }})" class="text-primary-bright hover:underline" data-test="edit-{{ $item->code }}">Editar</button>
                                <button type="button" wire:click="delete({{ $item->id }})" wire:confirm="¿Borrar «{{ $item->name }}»?" class="hover:text-danger">Borrar</button>
                            </span>
                        </div>
                    </x-item-card>
                @endforeach
            </div>
        </section>
    @empty
        <flux:callout icon="information-circle" color="zinc">
            <flux:callout.text>No hay ítems. Los de ejemplo se crean con <code>php artisan app:game-items</code> (lo corre el deploy).</flux:callout.text>
        </flux:callout>
    @endforelse

    <flux:modal name="item" class="w-full max-w-2xl">
        <form wire:submit="save" class="flex flex-col gap-4">
            <flux:heading size="lg">{{ $editingId ? 'Editar ítem' : 'Nuevo ítem' }}</flux:heading>
            <div class="grid gap-3 sm:grid-cols-2">
                <flux:input wire:model="form.name" label="Nombre" data-test="form-name" />
                <flux:input wire:model="form.code" label="Código" description="Se arma solo con el nombre si lo dejás vacío." />
                <flux:select wire:model="form.kind" label="Tipo">
                    @foreach (\App\Enums\ItemKind::cases() as $kind)
                        <flux:select.option :value="$kind->value">{{ $kind->label() }}</flux:select.option>
                    @endforeach
                </flux:select>
                <flux:select wire:model="form.rarity" label="Rareza">
                    @foreach (\App\Enums\ItemRarity::cases() as $rarity)
                        <flux:select.option :value="$rarity->value">{{ $rarity->label() }}</flux:select.option>
                    @endforeach
                </flux:select>
                <flux:select wire:model="form.course_id" label="Mundo" class="sm:col-span-2">
                    <flux:select.option value="">Común (sirve en todos los mundos)</flux:select.option>
                    @foreach ($courses as $course)
                        <flux:select.option :value="(string) $course->id">{{ $course->title }}</flux:select.option>
                    @endforeach
                </flux:select>
                <flux:textarea wire:model="form.description" label="Descripción" rows="2" class="sm:col-span-2" />
            </div>
            <div class="grid grid-cols-3 gap-3 sm:grid-cols-7">
                <flux:input type="number" wire:model="form.attack" label="ATQ" />
                <flux:input type="number" wire:model="form.defense" label="DEF" />
                <flux:input type="number" wire:model="form.strength" label="FUE" />
                <flux:input type="number" wire:model="form.dexterity" label="DES" />
                <flux:input type="number" wire:model="form.intelligence" label="INT" />
                <flux:input type="number" wire:model="form.luck" label="SUE" />
                <flux:input type="number" wire:model="form.heal" label="Cura" />
            </div>
            <div class="grid gap-3 sm:grid-cols-2">
                <flux:input type="number" wire:model="form.price" label="Precio en oro" description="Vacío: no se vende." />
                <flux:input type="number" wire:model="form.min_level" label="Nivel mínimo" />
                <flux:checkbox wire:model="form.in_shop" label="En la tienda de su mundo" />
                <flux:checkbox wire:model="form.droppable" label="Cae en las expediciones" />
            </div>
            <div class="flex flex-col gap-2">
                <flux:input type="file" wire:model="image" label="Imagen (cuadrada, PNG, JPG o WebP)" accept="image/png,image/jpeg,image/webp" />
                <div wire:loading wire:target="image" class="text-xs text-ink-muted">Subiendo…</div>
                @if ($image)
                    <img src="{{ $image->temporaryUrl() }}" alt="" class="size-20 rounded-lg object-cover">
                @elseif ($editingId && ($current = \App\Models\Item::find($editingId)?->imageUrl()))
                    <div class="flex items-center gap-3">
                        <img src="{{ $current }}" alt="" class="size-20 rounded-lg object-cover">
                        <button type="button" wire:click="removeImage({{ $editingId }})" class="text-xs text-ink-muted hover:text-danger">Quitar imagen</button>
                    </div>
                @endif
            </div>
            <div class="flex justify-end gap-2">
                <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                <flux:button type="submit" variant="primary" data-test="item-save">Guardar</flux:button>
            </div>
        </form>
    </flux:modal>
</div>
