<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header title="Comisiones"
        :subtitle="auth()->user()->isAdmin()
            ? 'Las comisiones de todos los cursos y su docente. Cada docente corrige y atiende a los alumnos de sus comisiones.'
            : 'Creá tus comisiones en los cursos que das y sumales alumnos desde Alumnos → Sumar alumnos. Vas a corregir y atender a los que estén en ellas.'" />

    @forelse ($courses as $course)
        <div class="flex flex-col gap-2" wire:key="board-{{ $course->id }}">
            <div class="flex items-center gap-3">
                <x-course-logo :course="$course" size="size-10" />
                <div class="flex min-w-0 flex-1 flex-col">
                    <span class="font-display font-semibold text-white">{{ $course->title }}</span>
                    <span class="text-xs text-ink-muted">{{ $course->language->label() }}</span>
                </div>
                <flux:button size="sm" icon="list-bullet" :href="route('admin.syllabus', $course)" wire:navigate>Temario</flux:button>
                <flux:button size="sm" variant="ghost" icon="book-open" :href="route('student.tree', $course)" wire:navigate>Ver el curso</flux:button>
            </div>
            <livewire:admin.courses.cohorts :course="$course" :heading="'Comisiones de '.$course->language->label()" wire:key="cohorts-{{ $course->id }}" />
        </div>
    @empty
        <div class="panel p-8 text-center text-ink-muted">Todavía no hay cursos publicados.</div>
    @endforelse
</div>
