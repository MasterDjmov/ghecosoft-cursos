{{-- Micro-misiones (D84): una a la vez. Se comprueban solas en el navegador; al coincidir la salida, se avisa
     al servidor (que la vuelve a comparar y da la XP). Solo premios de juego. --}}
@php
    $total = $steps->count();
    $doneCount = $doneSteps->count();
    // La última superada (la que viene justo antes de la actual) se muestra abierta: ahí está lo que pasó.
    $justDone = $steps->filter(fn ($s) => $doneSteps->has($s->id))->last(fn ($s) => ! $currentStep || $s->position < $currentStep->position);
@endphp
<section class="flex flex-col gap-4" data-test="node-steps">
    <div class="flex flex-wrap items-center justify-between gap-2">
        <h2 class="flex items-center gap-2 font-display text-lg font-semibold text-white">
            <flux:icon name="bolt" variant="mini" class="text-warning" /> Micro-misiones
        </h2>
        <span class="font-mono text-xs text-ink-muted" data-test="steps-progress">{{ $doneCount }} de {{ $total }}</span>
    </div>
    <div class="h-1.5 overflow-hidden rounded-full bg-surface-highest" role="progressbar" aria-valuemin="0" aria-valuemax="{{ $total }}" aria-valuenow="{{ $doneCount }}">
        <div class="h-full rounded-full bg-warning transition-all" style="width: {{ $total ? round($doneCount / $total * 100) : 0 }}%"></div>
    </div>

    @foreach ($steps as $step)
        @php($texts = $stepTexts[$step->id])
        @if ($doneSteps->has($step->id))
            {{-- Superada: se puede volver a leer. --}}
            <details class="group rounded-lg border border-success/30 bg-success/5" wire:key="step-done-{{ $step->id }}" data-test="step-done" @if ($justDone?->is($step)) open @endif>
                <summary class="flex cursor-pointer list-none items-center gap-3 px-4 py-3 text-sm">
                    <flux:icon name="check-circle" variant="mini" class="shrink-0 text-success" />
                    <span class="font-medium text-ink">{{ $step->title }}</span>
                    @if ($step->card_title)
                        <span class="ms-auto hidden rounded border border-secondary/40 px-2 py-0.5 font-mono text-[11px] text-secondary-bright sm:inline">{{ $step->card_title }}</span>
                    @endif
                    <flux:icon name="chevron-down" variant="micro" class="text-ink-muted transition group-open:rotate-180 {{ $step->card_title ? '' : 'ms-auto' }}" />
                </summary>
                <div class="flex flex-col gap-3 border-t border-success/20 px-4 py-3">
                    @if ($texts['scene'])
                        <div class="markdown text-sm text-ink-muted">{!! $texts['scene'] !!}</div>
                    @endif
                    @if ($texts['success'])
                        <div class="markdown text-sm text-ink">{!! $texts['success'] !!}</div>
                    @endif
                </div>
            </details>
        @elseif ($currentStep?->is($step))
            {{-- La que toca: escena, pista de Gheco, desafío y el editor. --}}
            <article class="panel panel-active flex flex-col overflow-hidden" wire:key="step-current-{{ $step->id }}" data-test="step-current">
                @if ($image = $step->imageUrl() ?? $fallbackScene)
                    <figure class="relative aspect-[16/7] overflow-hidden border-b border-outline">
                        <img src="{{ $image }}" alt="" class="size-full object-cover" loading="lazy" data-test="step-image">
                        <div class="absolute inset-0 bg-gradient-to-t from-[#070a14] via-transparent to-transparent"></div>
                        <figcaption class="absolute bottom-3 left-4 flex flex-col">
                            @if ($step->place)
                                <span class="tech-label text-secondary-bright">{{ $step->place }}</span>
                            @endif
                            <span class="font-display text-xl font-semibold text-white">{{ $step->title }}</span>
                        </figcaption>
                    </figure>
                @else
                    <header class="px-5 pt-5">
                        @if ($step->place)
                            <p class="tech-label text-secondary-bright">{{ $step->place }}</p>
                        @endif
                        <h3 class="font-display text-xl font-semibold text-white">{{ $step->title }}</h3>
                    </header>
                @endif

                <div class="flex flex-col gap-4 p-5">
                    @if ($texts['scene'])
                        <div class="markdown text-ink" data-test="step-scene">{!! $texts['scene'] !!}</div>
                    @endif

                    @if ($texts['hint'])
                        <aside class="flex items-start gap-3 rounded-lg border border-primary-bright/30 bg-primary/10 p-4" data-test="step-hint">
                            <img src="{{ asset('img/personajes/gheco.webp') }}" alt="Gheco" class="size-12 shrink-0 rounded-full border border-primary-bright/50 bg-surface-lowest object-cover">
                            <div class="flex min-w-0 flex-col gap-1">
                                <p class="tech-label text-primary-bright">Gheco sugiere</p>
                                <div class="markdown text-sm text-ink">{!! $texts['hint'] !!}</div>
                            </div>
                        </aside>
                    @endif

                    @if ($texts['challenge'])
                        <div class="flex items-start gap-2">
                            <flux:icon name="code-bracket" variant="mini" class="mt-0.5 shrink-0 text-warning" />
                            <div class="markdown font-medium text-white">{!! $texts['challenge'] !!}</div>
                        </div>
                    @endif

                    <x-code-runner :code="(string) $step->starter_code" :stdin="(string) $step->sample_input" :expected="$step->expected_output"
                        :language="$course->language->value" :name="strtolower($step->code)" :runnable="$course->language->studentCanRun()"
                        :show-stdin="filled($step->sample_input)">
                        <x-slot:footer>
                            {{-- Al coincidir la salida, se avisa una sola vez. --}}
                            <div x-data="{ sent: false }" x-effect="if (matches === true && ! sent) { sent = true; $wire.completeStep({{ $step->id }}, output) }">
                                <p x-show="matches === false" x-cloak class="flex items-center gap-2 text-sm text-warning" data-test="step-mismatch">
                                    <flux:icon name="exclamation-triangle" variant="micro" /> Todavía no: tu salida no es igual a la esperada. Comparalas línea por línea.
                                </p>
                                <p x-show="sent" x-cloak class="flex items-center gap-2 text-sm text-success">
                                    <flux:icon name="check-circle" variant="micro" /> ¡Coincide!
                                </p>
                            </div>
                        </x-slot:footer>
                    </x-code-runner>

                    <p class="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-ink-muted">
                        <span class="flex items-center gap-1"><flux:icon name="sparkles" variant="micro" class="text-warning" /> +{{ $step->xp_reward }} {{ term('xp.short') }}</span>
                        @if ($step->card_title)
                            <span class="flex items-center gap-1"><flux:icon name="book-open" variant="micro" class="text-secondary-bright" /> Carta: {{ $step->card_title }}</span>
                        @endif
                        @if ($step->item)
                            <span class="flex items-center gap-1"><flux:icon name="gift" variant="micro" class="text-success" /> {{ $step->item }}</span>
                        @endif
                        <span>Se comprueba sola: no la corrige el profe.</span>
                    </p>
                </div>
            </article>
        @else
            {{-- Todavía no: solo el título. --}}
            <div class="flex items-center gap-3 rounded-lg border border-dashed border-outline/70 px-4 py-3 text-sm text-ink-muted" wire:key="step-locked-{{ $step->id }}" data-test="step-locked">
                <flux:icon name="lock-closed" variant="micro" /> {{ $step->title }}
            </div>
        @endif
    @endforeach

    @if ($total > 0 && $doneCount === $total)
        <flux:callout icon="trophy" color="emerald" data-test="steps-finished">
            <flux:callout.heading>¡Superaste todas las micro-misiones de este {{ term('node', $course) }}!</flux:callout.heading>
            <flux:callout.text>Ahora sí: las prácticas que corrige el profe están más abajo. Si querés profundizar, abrí la teoría completa.</flux:callout.text>
        </flux:callout>
    @endif
</section>
