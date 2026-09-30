@php
    use App\Support\Markdown;
    use App\Support\Narrative;

    $md = fn (?string $text) => Narrative::render($text, $course);
    // Las resoluciones vienen como código suelto o como markdown con ``` (FORMATO-CURSO).
    $code = fn (?string $text) => str_contains((string) $text, '```')
        ? Markdown::render($text)
        : '<pre class="overflow-x-auto rounded-md border border-outline bg-[#05070d] p-3 font-mono text-xs text-ink">'.e($text).'</pre>';
    $typeLabel = ['root' => 'Clase 0', 'boss' => 'Jefe', 'extra' => 'Extra', 'window' => 'Ventana'];
    $number = 0;
@endphp

<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8 print:max-w-none print:p-0"
    x-data="{ all(open) { $root.querySelectorAll('details[data-fold]').forEach((d) => d.open = open) } }"
    x-on:beforeprint.window="all(true)" data-test="syllabus">
    <x-admin.page-header :label="$course->title" title="Temario"
        subtitle="El árbol entero en orden, para dar la clase: qué enseña cada nodo, los enunciados de sus prácticas y las resoluciones. Solo lo ven el administrador y los docentes.">
        <x-slot:actions>
            <flux:button size="sm" icon="chevron-double-down" x-on:click="all(true)" class="print:hidden">Desplegar todo</flux:button>
            <flux:button size="sm" variant="ghost" icon="chevron-double-up" x-on:click="all(false)" class="print:hidden">Plegar todo</flux:button>
            <flux:button size="sm" variant="ghost" icon="printer" x-on:click="window.print()" class="print:hidden">Imprimir</flux:button>
        </x-slot:actions>
    </x-admin.page-header>

    {{-- Índice --}}
    <nav class="panel flex flex-col gap-4 p-5" aria-label="Índice del curso">
        <p class="tech-label">{{ $sections->sum(fn ($s) => $s['nodes']->count()) }} {{ term('node', $course, 2) }} · {{ $practiceCount }} {{ term('practice', $course, $practiceCount) }}</p>
        <div class="grid gap-4 sm:grid-cols-2">
            @php($n = 0)
            @foreach ($sections as $section)
                <div class="flex flex-col gap-1">
                    <p class="text-sm font-medium text-white">
                        {{ $section['branch']?->title ?? 'Inicio' }}
                        @if ($section['branch']?->kind === \App\Enums\BranchKind::Path)
                            <flux:badge size="sm" color="pink">{{ ucfirst(term('branch.path', $course)) }}</flux:badge>
                        @elseif ($section['branch']?->is_extra)
                            <flux:badge size="sm" color="violet">Extras</flux:badge>
                        @endif
                    </p>
                    <ol class="flex flex-col gap-0.5 text-sm">
                        @foreach ($section['nodes'] as $node)
                            <li><a href="#nodo-{{ $node->id }}" class="text-ink-muted hover:text-primary-bright">{{ ++$n }}. {{ $node->title }}</a></li>
                        @endforeach
                    </ol>
                </div>
            @endforeach
        </div>
    </nav>

    @foreach ($sections as $section)
        <section class="flex flex-col gap-4">
            @if ($section['branch'])
                <h2 class="font-display text-xl font-semibold text-white print:break-before-page">{{ $section['branch']->title }}</h2>
            @endif

            @foreach ($section['nodes'] as $node)
                <article id="nodo-{{ $node->id }}" class="panel flex scroll-mt-20 flex-col gap-4 p-5 print:break-inside-avoid-page" wire:key="syllabus-node-{{ $node->id }}">
                    <header class="flex flex-wrap items-baseline gap-2">
                        <span class="font-mono text-xs text-ink-muted">{{ ++$number }} · {{ $node->code }}</span>
                        <h3 class="font-display text-lg font-semibold text-white">{{ $node->title }}</h3>
                        @isset($typeLabel[$node->type->value])
                            <flux:badge size="sm" :color="$node->isBoss() ? 'red' : 'zinc'">{{ $typeLabel[$node->type->value] }}</flux:badge>
                        @endisset
                        @unless ($node->is_published)
                            <flux:badge size="sm" color="amber">Sin publicar</flux:badge>
                        @endunless
                        <a href="{{ route('student.node', [$course, $node]) }}" wire:navigate class="ms-auto text-xs text-primary-bright hover:underline print:hidden">Ver como el alumno</a>
                    </header>

                    @if ($node->objectives)
                        <div class="prose-sm text-ink">{!! $md($node->objectives) !!}</div>
                    @endif

                    @if ($node->content || $node->example_code || $node->before_you_start)
                        <details data-fold class="rounded-lg border border-outline px-4 py-3">
                            <summary class="cursor-pointer text-sm font-medium text-white">Explicación y ejemplo</summary>
                            <div class="mt-3 flex flex-col gap-3 text-sm text-ink">
                                @if ($node->before_you_start)
                                    <div><p class="tech-label mb-1">Antes de empezar</p>{!! $md($node->before_you_start) !!}</div>
                                @endif
                                @if ($node->content)
                                    <div>{!! $md($node->content) !!}</div>
                                @endif
                                @if ($node->example_code)
                                    <div><p class="tech-label mb-1">Código de ejemplo</p>{!! $code($node->example_code) !!}</div>
                                @endif
                                @if ($node->expected_output)
                                    <div><p class="tech-label mb-1">Salida esperada</p>{!! $code($node->expected_output) !!}</div>
                                @endif
                            </div>
                        </details>
                    @endif

                    @if ($node->practices->isNotEmpty())
                        <div class="flex flex-col gap-3">
                            <p class="tech-label">{{ ucfirst(term('practice', $course, 2)) }}</p>
                            @foreach ($node->practices as $i => $practice)
                                <div class="flex flex-col gap-2 border-s-2 ps-4 {{ $practice->is_required ? 'border-primary-bright/60' : 'border-dashed border-[#a855f7]/60' }}">
                                    <p class="text-sm font-medium text-white">
                                        {{ $i + 1 }}. {{ $practice->title }}
                                        <span class="text-xs font-normal text-ink-muted">· {{ $practice->is_required ? 'obligatoria' : 'optativa' }} · {{ $practice->submission_mode->label() }}</span>
                                    </p>
                                    @if ($practice->instructions)
                                        <div class="text-sm text-ink">{!! $md($practice->instructions) !!}</div>
                                    @endif
                                    @if ($practice->approval_criteria)
                                        <div class="text-xs text-ink-muted"><span class="tech-label">Para aprobar</span> {!! $md($practice->approval_criteria) !!}</div>
                                    @endif
                                    @if ($practice->sample_input || $practice->expected_output || $practice->reference_solution)
                                        <details data-fold class="rounded-md border border-outline px-3 py-2">
                                            <summary class="cursor-pointer text-xs font-medium text-success">Resolución</summary>
                                            <div class="mt-2 flex flex-col gap-2 text-sm">
                                                @if ($practice->sample_input)
                                                    <div><p class="tech-label mb-1">Entrada de ejemplo</p>{!! $code($practice->sample_input) !!}</div>
                                                @endif
                                                @if ($practice->expected_output)
                                                    <div><p class="tech-label mb-1">Salida esperada</p>{!! $code($practice->expected_output) !!}</div>
                                                @endif
                                                @if ($practice->reference_solution)
                                                    <div><p class="tech-label mb-1">Solución de referencia</p>{!! $code($practice->reference_solution) !!}</div>
                                                @endif
                                            </div>
                                        </details>
                                    @endif
                                </div>
                            @endforeach
                        </div>
                    @endif

                    @if ($node->teacher_solutions)
                        <details data-fold class="rounded-lg border border-warning/40 bg-warning/5 px-4 py-3">
                            <summary class="cursor-pointer text-sm font-medium text-warning">Notas del docente (tiempos, dificultades, soluciones)</summary>
                            <div class="mt-3 text-sm text-ink">{!! $md($node->teacher_solutions) !!}</div>
                        </details>
                    @endif
                </article>
            @endforeach
        </section>
    @endforeach
</div>
