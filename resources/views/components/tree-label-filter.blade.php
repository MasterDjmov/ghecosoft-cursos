@props(['course'])

@php
    $groups = [
        'trunk' => ['Temas del camino principal', '#3b82f6'],
        'boss' => [ucfirst(term('node.boss', $course, 2)), '#ef4444'],
        'window' => [ucfirst(term('node.window', $course, 2)), '#2dd4bf'],
        'path' => [ucfirst(term('branch.path', $course, 2)), '#f472b6'],
        'extra' => ['Extras', '#a855f7'],
    ];
@endphp

{{-- Filtro de nombres del árbol dibujado (dentro de un x-data="skillTree"): ocultar nombres por categoría. --}}
<div class="flex flex-col gap-1.5" data-test="label-filter">
    <span class="tech-label">Nombres en el árbol</span>
    @foreach ($groups as $group => [$label, $color])
        <button type="button" class="flex items-center gap-2 text-start transition hover:text-white" x-on:click="toggleLabel('{{ $group }}')"
            x-bind:aria-pressed="labelVisible('{{ $group }}')" x-bind:class="labelVisible('{{ $group }}') ? 'text-ink' : 'text-ink-muted line-through'">
            <span class="grid size-3 place-items-center rounded-sm border" style="border-color: {{ $color }}"
                x-bind:style="labelVisible('{{ $group }}') ? 'background-color: {{ $color }}' : ''"></span>
            {{ $label }}
        </button>
    @endforeach
</div>
