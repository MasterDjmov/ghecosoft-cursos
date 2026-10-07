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

        <div class="grid gap-6 sm:grid-cols-2">
            <flux:select wire:model="language" label="Lenguaje">
                @foreach ($languages as $option)
                    <flux:select.option :value="$option->value">{{ $option->label() }}</flux:select.option>
                @endforeach
            </flux:select>
            <flux:select wire:model="level" label="Nivel">
                @foreach ($levels as $option)
                    <flux:select.option :value="$option->value">{{ $option->label() }}</flux:select.option>
                @endforeach
            </flux:select>
        </div>

        <div class="grid gap-6 sm:grid-cols-2">
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

        <div class="flex flex-col gap-3">
            <flux:label>Portada</flux:label>
            <div class="flex flex-wrap items-center gap-4">
                @if ($cover && $cover->isPreviewable())
                    <img src="{{ $cover->temporaryUrl() }}" alt="" class="h-20 w-36 rounded-lg border border-outline object-cover">
                @elseif ($course?->coverUrl())
                    <img src="{{ $course->coverUrl() }}" alt="" class="h-20 w-36 rounded-lg border border-outline object-cover">
                @endif
                <input type="file" wire:model="cover" accept="image/png,image/jpeg,image/webp"
                    class="text-sm text-ink-muted file:me-3 file:rounded-md file:border-0 file:bg-surface-highest file:px-3 file:py-2 file:text-ink hover:file:bg-surface-high">
                @if ($course?->cover)
                    <flux:button size="sm" variant="ghost" wire:click="removeCover">Quitar portada</flux:button>
                @endif
            </div>
            <flux:description>Horizontal (16:9). Es la imagen de referencia de las tarjetas "Próximamente" y de la landing.</flux:description>
            <flux:error name="cover" />
        </div>

        <flux:textarea wire:model="syllabus" label="Temario corto" rows="5" placeholder="Variables y tipos&#10;Condicionales&#10;Bucles&#10;Funciones"
            description:trailing="Un tema por línea. Se muestra en las tarjetas del catálogo, sobre todo en «Próximamente»." />

        <div class="grid gap-4 sm:grid-cols-3">
            <flux:switch wire:model.live="is_published" label="Publicado" description="Si está apagado, no se puede abrir ni inscribirse." />
            <flux:switch wire:model="is_upcoming" label="Próximamente" :disabled="$is_published"
                description="Sin publicar: se muestra como adelanto, con «Avisame cuando salga»." />
            <flux:switch wire:model="is_featured" label="Destacado" description="Sale en la landing entre los cursos que más se dictan." />
        </div>

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
        <livewire:admin.courses.cohorts :course="$course" />

        <flux:modal name="delete-course" class="max-w-md">
            <div class="flex flex-col gap-4">
                <flux:heading size="lg">¿Borrar «{{ $course->title }}»?</flux:heading>
                @if ($impact['students'] === 0 && $impact['requests'] === 0)
                    <flux:text>Se borran sus ramas, nodos, hojas y recursos. Todavía no tiene alumnos.</flux:text>
                    <div class="flex justify-end gap-2">
                        <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                        <flux:button variant="danger" wire:click="delete">Borrar</flux:button>
                    </div>
                @else
                    {{-- Con alumnos (D87): se muestra todo lo que se pierde y se confirma escribiendo el nombre corto. --}}
                    <flux:callout icon="exclamation-triangle" color="red" data-test="delete-impact">
                        <flux:callout.text>
                            <strong>Este curso tiene alumnos.</strong> Se pierde para siempre:
                            {{ $impact['students'] }} {{ $impact['students'] === 1 ? 'alumno' : 'alumnos' }} con su progreso ({{ $impact['active'] }} con el abono vigente),
                            {{ $impact['submissions'] }} entregas, {{ $impact['requests'] }} solicitudes con sus comprobantes de pago,
                            las monedas del curso, {{ $impact['nodes'] }} nodos y {{ $impact['practices'] }} prácticas.
                            Las cuentas y la XP ganada quedan.
                        </flux:callout.text>
                    </flux:callout>
                    <flux:text>Para <strong>actualizar</strong> el curso no hace falta borrarlo: reimportalo (no toca el progreso) y, mientras tanto, ponelo en mantenimiento desde Configuración. Antes de borrar, hacé una copia de la base (<code class="font-mono">scripts/backup.sh</code>).</flux:text>
                    <flux:input wire:model="deleteConfirm" :label="'Escribí «'.$course->slug.'» para confirmar'" autocomplete="off" data-test="delete-confirm" />
                    <div class="flex justify-end gap-2">
                        <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                        <flux:button variant="danger" wire:click="deleteWithStudents">Borrar con todo</flux:button>
                    </div>
                @endif
            </div>
        </flux:modal>
    @endif
</div>
