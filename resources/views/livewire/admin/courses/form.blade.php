<div class="mx-auto flex w-full max-w-4xl flex-col gap-8 p-4 sm:p-8">
    <x-admin.page-header :label="$course ? 'Cursos · '.$course->title : 'Cursos'" :title="$course ? 'Datos del curso' : 'Nuevo curso'">
        <x-slot:actions>
            @if ($course)
                <flux:button icon="share" :href="route('admin.courses.tree', $course)" wire:navigate>Ir al árbol</flux:button>
            @endif
            <flux:button variant="ghost" icon="arrow-left" :href="route('admin.courses.index')" wire:navigate>Cursos</flux:button>
        </x-slot:actions>
    </x-admin.page-header>

    <form wire:submit="save" class="panel flex flex-col gap-6 p-5 sm:p-6">
        <div class="grid gap-6 sm:grid-cols-2">
            <flux:input wire:model.live.debounce.400ms="title" label="Título" required />
            <flux:input wire:model="slug" label="Dirección" description:trailing="Aparece en el link: /cursos/{{ $slug ?: 'python' }}" required />
        </div>

        <flux:input wire:model="short_description" label="Descripción corta" description:trailing="Una línea para la tarjeta del mapa." />

        <flux:textarea wire:model="description" label="Descripción" rows="6" description:trailing="Admite markdown (**negrita**, listas, `código`)." />

        <div class="grid gap-6 sm:grid-cols-3">
            <flux:select wire:model="language" label="Lenguaje">
                @foreach ($languages as $option)
                    <flux:select.option :value="$option->value">{{ $option->label() }}</flux:select.option>
                @endforeach
            </flux:select>
            <flux:input wire:model="root_price" type="number" min="1" label="Precio del raíz"
                description:trailing="Monedas que se acreditan al aprobar el pago (y lo que cuesta abrir el raíz)." />
            <flux:input wire:model="subscription_days" type="number" min="1" label="Días de abono" />
        </div>

        <div class="flex flex-col gap-3">
            <flux:label>Logo</flux:label>
            <div class="flex flex-wrap items-center gap-4">
                @if ($logo && $logo->isPreviewable())
                    <img src="{{ $logo->temporaryUrl() }}" alt="" class="size-16 rounded-full border border-primary-bright/40 object-cover">
                @elseif ($course)
                    <x-course-logo :course="$course" size="size-16" />
                @endif
                <input type="file" wire:model="logo" accept="image/png,image/jpeg,image/webp"
                    class="text-sm text-ink-muted file:me-3 file:rounded-md file:border-0 file:bg-surface-highest file:px-3 file:py-2 file:text-ink hover:file:bg-surface-high">
                @if ($course?->logo)
                    <flux:button size="sm" variant="ghost" wire:click="removeLogo">Quitar logo</flux:button>
                @endif
            </div>
            <flux:description>PNG, JPG o WEBP, cuadrado, hasta 2 MB. Va en el centro del árbol y en la moneda del curso.</flux:description>
            <flux:error name="logo" />
        </div>

        <flux:switch wire:model="is_published" label="Publicado" description="Si está apagado, los alumnos no ven el curso en el mapa." />

        <div class="flex flex-wrap items-center justify-between gap-3">
            <flux:button variant="primary" type="submit">{{ $course ? 'Guardar' : 'Crear curso' }}</flux:button>
            @if ($course)
                <flux:modal.trigger name="delete-course">
                    <flux:button variant="ghost" icon="trash" class="text-danger!">Borrar curso</flux:button>
                </flux:modal.trigger>
            @endif
        </div>
    </form>

    @if ($course)
        <flux:modal name="delete-course" class="max-w-md">
            <div class="flex flex-col gap-4">
                <flux:heading size="lg">¿Borrar «{{ $course->title }}»?</flux:heading>
                <flux:text>Se borran sus ramas, nodos, hojas y recursos. Si ya tiene alumnos no se puede: despublicalo.</flux:text>
                <div class="flex justify-end gap-2">
                    <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                    <flux:button variant="danger" wire:click="delete">Borrar</flux:button>
                </div>
            </div>
        </flux:modal>
    @endif
</div>
