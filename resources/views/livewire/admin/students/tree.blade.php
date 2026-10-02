{{-- El árbol de un alumno en un curso: colores de avance, sin links ni contenido; debajo, los nodos que siguen. --}}
<div class="mx-auto flex w-full max-w-6xl flex-col gap-4 p-4 sm:p-8">
    <a href="{{ $canSeeFile ? route('admin.students.show', $user) : route('admin.students.index') }}" wire:navigate
        class="inline-flex items-center gap-1.5 self-start text-sm text-ink-muted hover:text-white">
        <flux:icon name="chevron-left" variant="micro" /> {{ $canSeeFile ? 'Volver a la ficha de '.$user->fullName() : 'Volver a Alumnos' }}
    </a>
    <header class="flex flex-col gap-4 sm:flex-row sm:items-center">
        <x-course-logo :course="$course" size="size-16" />
        <div class="flex min-w-0 flex-col gap-1">
            <p class="tech-label">Árbol de {{ $user->fullName() }}</p>
            <h1 class="font-display text-2xl font-semibold text-white">{{ $course->title }}</h1>
            <p class="text-sm text-ink-muted">
                {{ $completed }}/{{ $total }} {{ term('node', $course, $total) }} del camino principal · los de color son los que recorrió
            </p>
        </div>
    </header>

    <section class="relative h-[75vh] min-h-[460px] overflow-hidden rounded-lg border border-outline bg-[#05070d]/90"
        x-data="skillTree(@js($graph), { readOnly: true })" wire:ignore data-test="student-progress-tree">
        <div x-ref="canvas" class="absolute inset-0"></div>
        @include('livewire.student.partials.tree-legend')
        <div class="absolute bottom-3 left-3">
            <flux:button size="xs" icon="arrows-pointing-out" x-on:click="fit">Ver todo</flux:button>
        </div>
    </section>

    {{-- Lo que sigue: si se traba, se lo abrís con sus monedas (mismas reglas que si lo abriera él). --}}
    <section class="panel flex flex-col gap-3 p-5" data-test="student-next-nodes">
        <div>
            <h2 class="font-display font-semibold text-white">Lo que sigue</h2>
            <p class="text-sm text-ink-muted">Los {{ term('node', $course, 2) }} que vienen después de lo que abrió. Si se traba, abriselo vos: se paga con sus monedas, con las mismas reglas, y le llega un aviso.</p>
        </div>
        @forelse ($next as $item)
            <div class="flex flex-col gap-2 border-t border-outline/60 pt-3 sm:flex-row sm:items-center" wire:key="next-{{ $item['id'] }}">
                <div class="flex min-w-0 flex-1 flex-col gap-0.5">
                    <span class="font-medium text-ink">{{ $item['title'] }} <span class="font-mono text-xs text-ink-muted">· {{ $item['price'] }}</span></span>
                    @if ($item['reasons'])
                        <span class="flex items-start gap-1.5 text-xs text-warning"><flux:icon name="lock-closed" variant="micro" class="mt-0.5 shrink-0" /> {{ implode(' ', $item['reasons']) }}</span>
                    @else
                        <span class="text-xs text-success">Lo puede abrir ya.</span>
                    @endif
                </div>
                @unless ($item['reasons'])
                    <flux:button size="sm" variant="primary" icon="lock-open" wire:click="unlockFor({{ $item['id'] }})" data-test="unlock-for-{{ $item['id'] }}"
                        wire:confirm="¿Abrirle «{{ $item['title'] }}» a {{ $user->name }}? Se paga con {{ $item['price'] }} de su saldo.">Abrírselo</flux:button>
                @endunless
            </div>
        @empty
            <flux:text>No tiene {{ term('node', $course, 2) }} cerrados a continuación: abrió todo lo que tenía disponible o terminó el curso.</flux:text>
        @endforelse
    </section>
</div>
