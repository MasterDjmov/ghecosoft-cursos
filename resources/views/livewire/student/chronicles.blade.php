{{-- Mis Crónicas (D80): el prólogo y un libro por curso; lo bloqueado se ve en silueta, sin su texto. --}}
<div class="mx-auto flex w-full max-w-4xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-col gap-1">
        <p class="tech-label">Tu historia</p>
        <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Mis Crónicas</h1>
        <p class="text-ink-muted">Cada {{ term('node') }} que completás abre una página de tu historia. Lo que todavía no desbloqueaste se ve, pero no se lee: seguí avanzando.</p>
    </header>

    {{-- Los libros --}}
    <nav class="flex flex-wrap gap-2" aria-label="Libros" data-test="chronicle-books">
        <button type="button" wire:click="$set('book', 'prologo')"
            @class(['flex items-center gap-2 rounded-lg border px-3 py-2 text-sm transition', 'border-primary-bright bg-primary/10 text-white' => ! $course, 'border-outline text-ink-muted hover:text-white' => $course])>
            <flux:icon name="sparkles" variant="micro" /> Prólogo
        </button>
        @foreach ($courses as $option)
            <button type="button" wire:click="$set('book', '{{ $option->slug }}')" wire:key="book-{{ $option->id }}"
                @class(['flex items-center gap-2 rounded-lg border px-3 py-2 text-sm transition', 'border-primary-bright bg-primary/10 text-white' => $course?->is($option), 'border-outline text-ink-muted hover:text-white' => ! $course?->is($option)])>
                <x-course-logo :course="$option" size="size-6" /> {{ \Illuminate\Support\Str::before($option->title, ':') }}
            </button>
        @endforeach
    </nav>

    {{-- La portada: el mundo de fondo --}}
    <section class="relative flex min-h-56 flex-col justify-end overflow-hidden rounded-xl border border-outline" data-test="chronicle-cover">
        @if ($scene)
            <img src="{{ $scene }}" alt="" class="absolute inset-0 size-full object-cover">
        @endif
        <div class="absolute inset-0 bg-gradient-to-t from-[#070a14] via-[#070a14]/70 to-transparent"></div>
        <div class="relative flex flex-col gap-1 p-5">
            <p class="tech-label text-secondary-bright">{{ $course ? 'Libro' : 'Prólogo' }}</p>
            <h2 class="font-display text-2xl font-semibold text-white">{{ $course ? $course->title : ($prologue['title'] ?? 'El Mundo del Código') }}</h2>
            @if ($course)
                <p class="font-mono text-xs text-ink-muted">{{ $unlocked }} de {{ $total }} páginas desbloqueadas</p>
            @endif
        </div>
    </section>

    @if (! $course)
        @if ($prologue)
            <article class="panel flex flex-col gap-4 p-6" data-test="chronicle-prologue">
                <div class="markdown text-ink">{!! $prologue['html'] !!}</div>
            </article>
        @endif
        @if ($courses->isEmpty())
            <flux:callout icon="book-open" color="zinc">
                <flux:callout.text>Cuando empieces un curso, su libro aparece acá y se va abriendo con cada {{ term('node') }} que completes.</flux:callout.text>
            </flux:callout>
        @endif
    @else
        @foreach ($chapters as $chapter)
            <section class="flex flex-col gap-3" wire:key="chapter-{{ $loop->index }}">
                <p class="tech-label text-primary-bright">{{ $chapter['title'] }}</p>
                {{-- De lo bloqueado se muestra la próxima página; el resto del capítulo se resume en una tarjeta. --}}
                @php($shownLocked = false)
                @php($hidden = 0)
                @foreach ($chapter['pages'] as $page)
                    @if (! $page['unlocked'] && $shownLocked)
                        @php($hidden++)
                        @continue
                    @endif
                    @php($shownLocked = $shownLocked || ! $page['unlocked'])
                    @include('livewire.partials.chronicle-page', ['page' => $page, 'portrait' => $portrait($page['speaker']), 'hint' => $page['unlocked'] ? null : $hint()])
                @endforeach
                @if ($hidden > 0)
                    <p class="flex items-center gap-2 rounded-lg border border-dashed border-outline/70 px-5 py-3 text-sm text-ink-muted" data-test="chronicle-more">
                        <flux:icon name="lock-closed" variant="micro" /> + {{ $hidden }} {{ $hidden === 1 ? 'página por descubrir' : 'páginas por descubrir' }} en este capítulo
                    </p>
                @endif
            </section>
        @endforeach
        <div class="flex justify-center">
            <flux:button icon="share" :href="route('student.tree', $course)" wire:navigate>Seguir en el árbol</flux:button>
        </div>
    @endif
</div>
