<!DOCTYPE html>
<html lang="es" class="dark">
    <head>
        @include('partials.head', ['title' => 'Árbol de '.$user->fullName().' · '.$course->title])
        <meta name="robots" content="noindex">
    </head>
    {{-- El árbol de un curso del CV, solo para mirar: colores de avance, sin links ni contenido. --}}
    <body class="min-h-screen">
        <main class="mx-auto flex w-full max-w-6xl flex-col gap-4 p-4 sm:p-8">
            <a href="{{ route('cv.show', $user->cv_slug) }}" class="inline-flex items-center gap-1.5 self-start text-sm text-ink-muted hover:text-white">
                <flux:icon name="chevron-left" variant="micro" /> Volver al CV de {{ $user->fullName() }}
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
                x-data="skillTree(@js($graph), { readOnly: true })" data-test="cv-tree">
                <div x-ref="canvas" class="absolute inset-0"></div>
                @include('livewire.student.partials.tree-legend')
                <div class="absolute bottom-3 left-3">
                    <flux:button size="xs" icon="arrows-pointing-out" x-on:click="fit">Ver todo</flux:button>
                </div>
            </section>
        </main>
        @fluxScripts
    </body>
</html>
