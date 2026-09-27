<div class="mx-auto flex w-full max-w-3xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header title="Niveles"
        subtitle="La XP nunca baja: al llegar a la cantidad indicada, el alumno sube de nivel. El nombre es opcional (por ejemplo «Aprendiz»); el texto de historia se carga en el Diccionario.">
        <x-slot:actions>
            <flux:button icon="book-open" :href="route('admin.glossary', ['grupo' => 'levels'])" wire:navigate>Historia de cada nivel</flux:button>
        </x-slot:actions>
    </x-admin.page-header>

    <form wire:submit="save" class="panel flex flex-col gap-4 p-5">
        <div class="hidden grid-cols-[4rem_1fr_1fr] gap-4 sm:grid">
            <span class="tech-label">Nivel</span>
            <span class="tech-label">XP necesaria</span>
            <span class="tech-label">Nombre del rango</span>
        </div>

        @foreach ($rows as $number => $row)
            <div class="grid grid-cols-[3rem_1fr] items-start gap-3 sm:grid-cols-[4rem_1fr_1fr] sm:gap-4" wire:key="level-{{ $number }}">
                <span class="grid size-10 place-items-center rounded-full border border-primary-bright/40 bg-primary/10 font-display font-bold text-primary-bright">{{ $number }}</span>
                <flux:input wire:model="rows.{{ $number }}.xp_required" type="number" min="0" :disabled="$number === 1" aria-label="XP del nivel {{ $number }}" />
                <flux:input wire:model="rows.{{ $number }}.name" :placeholder="ucfirst(term('level')).' '.$number" aria-label="Nombre del nivel {{ $number }}" class="col-start-2 sm:col-start-auto" />
            </div>
        @endforeach

        <div class="flex flex-wrap items-center justify-between gap-2 pt-2">
            <div class="flex gap-2">
                <flux:button size="sm" icon="plus" wire:click="add">Agregar nivel</flux:button>
                @if (count($rows) > 1)
                    <flux:button size="sm" variant="ghost" icon="minus" wire:click="removeLast" wire:confirm="¿Quitar el último nivel?">Quitar el último</flux:button>
                @endif
            </div>
            <flux:button variant="primary" type="submit">Guardar</flux:button>
        </div>
    </form>
</div>
