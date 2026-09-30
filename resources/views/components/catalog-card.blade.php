@props(['course', 'nodes' => 0])

{{-- Tarjeta del catálogo (Mundos y landing). "Próximamente" lleva la portada y el temario, sin entrar. --}}
@php($upcoming = $course->isUpcoming())
@php($inline = fn (string $text) => Str::inlineMarkdown($text, ['html_input' => 'escape', 'allow_unsafe_links' => false]))
<article {{ $attributes->class(['panel flex flex-col overflow-hidden', 'border-dashed' => $upcoming]) }} data-test="catalog-{{ $course->slug }}">
    @if ($upcoming && $course->coverUrl())
        <div class="relative h-32 overflow-hidden">
            <img src="{{ $course->coverUrl() }}" alt="" class="size-full object-cover opacity-80">
            <div class="absolute inset-0 bg-linear-to-t from-surface-low to-transparent"></div>
        </div>
    @endif

    <div class="flex flex-1 flex-col gap-4 p-5">
        <div class="flex items-start justify-between gap-3">
            <x-course-logo :course="$course" size="size-50 max-w-full" />
            @if ($upcoming)
                <span class="rounded border border-secondary-bright/40 px-2 py-0.5 font-mono text-[11px] text-secondary-bright">Próximamente</span>
            @endif
        </div>

        <div class="flex flex-col gap-1">
            <h3 class="font-display text-lg font-semibold text-white">{{ $course->title }}</h3>
            <p class="font-mono text-[11px] text-ink-muted">
                {{ $course->language->label() }} · {{ $course->level->label() }}@unless ($upcoming) · {{ $nodes }} {{ term('node', $course, $nodes) }}@endunless
            </p>
            @if ($course->short_description)
                <p class="text-sm text-ink-muted">{{ $course->short_description }}</p>
            @endif
        </div>

        @php($items = $course->syllabusItems())
        @php($paths = $course->paths)
        @if ($items)
            <div class="flex flex-col gap-1">
                <p class="tech-label">{{ $upcoming ? 'Qué se va a dar' : 'Temario' }}</p>
                <ul class="flex flex-col gap-0.5 text-sm text-ink">
                    @foreach (array_slice($items, 0, 5) as $item)
                        <li class="flex gap-2"><span class="text-primary-bright">›</span> <span class="syllabus-item">{!! $inline($item) !!}</span></li>
                    @endforeach
                </ul>
                <div class="mt-1 flex flex-wrap items-center gap-x-3 gap-y-2">
                    @php($more = max(0, count($items) - 5))
                    @if ($more || $paths->isNotEmpty())
                        <span class="text-xs text-ink-muted">
                            {{ $more ? 'y '.$more.' '.($more === 1 ? 'tema' : 'temas').' más' : '' }}{{ $more && $paths->isNotEmpty() ? ' · ' : '' }}{{ $paths->isNotEmpty() ? '+ '.$paths->count().' '.($paths->count() === 1 ? 'Senda opcional' : 'Sendas opcionales') : '' }}
                        </span>
                    @endif
                    <flux:modal.trigger :name="'syllabus-'.$course->slug">
                        <flux:button size="xs" icon="list-bullet" class="ms-auto" data-test="syllabus-{{ $course->slug }}">Ver temario</flux:button>
                    </flux:modal.trigger>
                </div>
            </div>

            <flux:modal :name="'syllabus-'.$course->slug" class="w-full max-w-lg">
                <div class="flex flex-col gap-5">
                    <div class="flex items-center gap-3">
                        <x-course-logo :course="$course" size="size-20" />
                        <div class="flex flex-col gap-0.5">
                            <flux:heading size="lg">{{ $course->title }}</flux:heading>
                            <p class="font-mono text-[11px] text-ink-muted">
                                {{ $course->language->label() }} · {{ $course->level->label() }}@unless ($upcoming) · {{ $nodes }} {{ term('node', $course, $nodes) }}@endunless
                            </p>
                        </div>
                    </div>

                    <div class="flex flex-col gap-2">
                        <p class="tech-label">{{ $upcoming ? 'Qué se va a dar' : 'Temario' }}</p>
                        <ol class="flex flex-col gap-1.5 text-sm text-ink">
                            @foreach ($items as $item)
                                <li class="flex gap-3"><span class="w-5 shrink-0 text-end font-mono text-xs leading-5 text-primary-bright">{{ $loop->iteration }}</span> <span class="syllabus-item">{!! $inline($item) !!}</span></li>
                            @endforeach
                        </ol>
                    </div>

                    @if ($paths->isNotEmpty())
                        <div class="flex flex-col gap-2 rounded-lg border border-dashed border-secondary-bright/40 p-4">
                            <p class="tech-label text-secondary-bright!">Opcionales · Sendas</p>
                            <p class="text-xs text-ink-muted">Especializaciones que se abren con {{ term('coin.wildcard', null, 2) }}, que se ganan con las tareas optativas. No hacen falta para terminar el curso.</p>
                            <ul class="flex flex-col gap-1.5 text-sm">
                                @foreach ($paths as $path)
                                    @php([$pathName, $pathTopic] = array_pad(explode(': ', $path->title, 2), 2, null))
                                    <li class="flex gap-2">
                                        <span class="text-secondary-bright">✦</span>
                                        <span><span class="font-medium text-white">{{ $pathName }}</span>@if ($pathTopic)<span class="text-ink-muted"> — {{ $pathTopic }}</span>@endif</span>
                                    </li>
                                @endforeach
                            </ul>
                        </div>
                    @endif

                    <div class="flex justify-end">
                        <flux:modal.close><flux:button variant="ghost" size="sm">Cerrar</flux:button></flux:modal.close>
                    </div>
                </div>
            </flux:modal>
        @endif

        <div class="mt-auto flex flex-wrap gap-2 pt-1">
            {{ $slot }}
        </div>
    </div>
</article>
