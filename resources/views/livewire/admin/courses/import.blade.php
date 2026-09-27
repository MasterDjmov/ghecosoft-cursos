@php
    $entities = ['curso' => 'Curso', 'diccionario' => 'Diccionario', 'ramas' => 'Ramas', 'nodos' => 'Nodos', 'prácticas' => 'Prácticas', 'insignias' => 'Insignias', 'requisitos' => 'Requisitos extra'];
@endphp

<div class="mx-auto flex w-full max-w-4xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header label="Cursos" title="Importar curso"
        subtitle="Cargá los .md del curso (el formato de FORMATO-CURSO.md). Primero se revisa sin guardar; si está bien, se importa.">
        <x-slot:actions>
            <flux:button variant="ghost" icon="arrow-left" :href="route('admin.courses.index')" wire:navigate>Cursos</flux:button>
        </x-slot:actions>
    </x-admin.page-header>

    <section class="panel flex flex-col gap-4 p-5 sm:p-6">
        <div class="flex flex-col gap-2">
            <flux:label>Archivos .md (uno o varios; se leen en orden por nombre)</flux:label>
            <input type="file" wire:model="files" multiple accept=".md,.txt"
                class="text-sm text-ink-muted file:me-3 file:rounded-md file:border-0 file:bg-surface-highest file:px-3 file:py-2 file:text-ink hover:file:bg-surface-high">
            <div wire:loading wire:target="files" class="text-xs text-ink-muted">Subiendo…</div>
            <flux:error name="files" />
            <flux:error name="files.*" />
        </div>
        <ul class="flex flex-col gap-2 text-sm text-ink-muted">
            <li class="flex gap-2"><flux:icon name="shield-check" variant="micro" class="mt-0.5 shrink-0 text-success" /> Reimportar actualiza por ID (R01-N02…): no duplica, no borra y no toca el progreso de los alumnos.</li>
            <li class="flex gap-2"><flux:icon name="information-circle" variant="micro" class="mt-0.5 shrink-0 text-primary-bright" /> Si hay un error no se guarda nada. Un curso nuevo se crea como borrador.</li>
        </ul>
        <div class="flex flex-wrap justify-end gap-2">
            <flux:button icon="magnifying-glass" wire:click="review" wire:loading.attr="disabled" wire:target="files,review,import">Revisar</flux:button>
            <flux:button variant="primary" icon="arrow-down-tray" wire:click="import" wire:loading.attr="disabled" wire:target="files,review,import"
                :disabled="! $report || $report['errors'] !== [] || $applied"
                wire:confirm="¿Importar el curso? Se crean y actualizan ramas, nodos y prácticas.">Importar</flux:button>
        </div>
    </section>

    @if ($report)
        <section class="flex flex-col gap-4" data-test="import-report">
            @if ($report['errors'] !== [])
                <flux:callout icon="x-circle" color="red">
                    <flux:callout.heading>Hay {{ count($report['errors']) }} {{ count($report['errors']) === 1 ? 'error' : 'errores' }}: no se guardó nada</flux:callout.heading>
                    <flux:callout.text>
                        <ul class="mt-1 list-disc ps-5">
                            @foreach ($report['errors'] as $message)
                                <li>{{ $message }}</li>
                            @endforeach
                        </ul>
                    </flux:callout.text>
                </flux:callout>
            @elseif ($applied)
                <flux:callout icon="check-circle" color="green">
                    <flux:callout.heading>«{{ $report['courseTitle'] }}» importado</flux:callout.heading>
                    <flux:callout.text>
                        @if ($report['courseUrl'])
                            <flux:link :href="$report['courseUrl']" wire:navigate>Ver el árbol</flux:link>
                        @endif
                    </flux:callout.text>
                </flux:callout>
            @else
                <flux:callout icon="magnifying-glass" color="cyan">
                    <flux:callout.heading>Revisión de «{{ $report['courseTitle'] }}»: todo en orden</flux:callout.heading>
                    <flux:callout.text>No se guardó nada todavía. Si el resumen está bien, tocá <strong>Importar</strong>.</flux:callout.text>
                </flux:callout>
            @endif

            @if ($report['counts'] !== [])
                <div class="panel overflow-x-auto">
                    <table class="w-full text-sm">
                        <thead class="text-left text-ink-muted">
                            <tr class="border-b border-outline">
                                <th class="px-4 py-2 font-medium"></th>
                                <th class="px-4 py-2 font-medium">Nuevos</th>
                                <th class="px-4 py-2 font-medium">Cambiados</th>
                                <th class="px-4 py-2 font-medium">Iguales</th>
                            </tr>
                        </thead>
                        <tbody>
                            @foreach ($report['counts'] as $entity => $count)
                                <tr class="border-b border-outline/60 last:border-0">
                                    <td class="px-4 py-2 text-white">{{ $entities[$entity] ?? ucfirst($entity) }}</td>
                                    <td class="px-4 py-2 font-mono text-success">{{ $count['created'] }}</td>
                                    <td class="px-4 py-2 font-mono text-warning">{{ $count['updated'] }}</td>
                                    <td class="px-4 py-2 font-mono text-ink-muted">{{ $count['unchanged'] }}</td>
                                </tr>
                            @endforeach
                        </tbody>
                    </table>
                </div>
            @endif

            @if ($report['warnings'] !== [])
                <details class="panel p-4" open>
                    <summary class="cursor-pointer text-sm font-medium text-warning">Avisos ({{ count($report['warnings']) }})</summary>
                    <ul class="mt-3 flex flex-col gap-1 text-sm text-ink-muted">
                        @foreach ($report['warnings'] as $message)
                            <li class="flex gap-2"><flux:icon name="exclamation-triangle" variant="micro" class="mt-0.5 shrink-0 text-warning" /> {{ $message }}</li>
                        @endforeach
                    </ul>
                </details>
            @endif

            @if ($report['notes'] !== [])
                <ul class="flex flex-col gap-1 text-sm text-ink-muted">
                    @foreach ($report['notes'] as $message)
                        <li>· {{ $message }}</li>
                    @endforeach
                </ul>
            @endif
        </section>
    @endif
</div>
