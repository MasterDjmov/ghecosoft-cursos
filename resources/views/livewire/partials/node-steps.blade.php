{{-- Micro-misiones (D84): una a la vez. Se comprueban solas en el navegador; al coincidir la salida, se avisa
     al servidor (que la vuelve a comparar y da la XP). Solo premios de juego. --}}
@php
    // El oro existe desde la D89 (config game.gold_enabled); los ítems y lo que «se abre», recién cuando
    // exista el inventario (config game.inventory_enabled).
    $gold = (bool) config('game.gold_enabled');
    $inventory = (bool) config('game.inventory_enabled');
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

    {{-- Todavía no tomó el control del protagonista (D89): se lo invita, sin frenar las micro-misiones. --}}
    @php($protagonist = app(\App\Services\Heroes::class)->protagonist($course))
    @if ($protagonist && auth()->user()->isStudent() && ! app(\App\Services\Heroes::class)->heroOf(auth()->user(), $course))
        <a href="{{ route('student.hero', $course) }}" wire:navigate class="flex items-center gap-3 rounded-lg border border-warning/50 bg-warning/10 px-4 py-3 text-sm transition hover:bg-warning/15" data-test="take-control-prompt">
            <img src="{{ \App\Services\Heroes::lookUrl($protagonist, 1) }}" alt="" class="size-10 shrink-0 rounded-full object-cover">
            <span class="flex-1 text-ink"><strong class="text-warning">Tomá el control de {{ $protagonist['name'] }}</strong>: elegí su aspecto y repartí sus puntos. El oro que ganes acá sube sus atributos.</span>
            <flux:icon name="chevron-right" variant="mini" class="text-warning" />
        </a>
    @endif

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
                @php($mine = $doneSteps[$step->id])
                <div class="flex flex-col gap-3 border-t border-success/20 px-4 py-3">
                    {{-- La imagen sigue acompañando la lectura (o el fondo del mundo, si todavía no tiene). --}}
                    @if ($image = $step->imageUrl() ?? $fallbackScene)
                        <img src="{{ $image }}" alt="" class="aspect-[16/7] w-full rounded-lg border border-outline object-cover" loading="lazy" data-test="step-done-image">
                    @endif
                    @if ($texts['scene'])
                        <div class="markdown text-sm text-ink-muted">{!! $texts['scene'] !!}</div>
                    @endif
                    @if ($texts['challenge'])
                        <div class="markdown text-sm text-white">{!! $texts['challenge'] !!}</div>
                    @endif
                    {{-- Lo que escribió y lo que obtuvo. --}}
                    @if (filled($mine->code))
                        <div class="flex flex-col gap-1" data-test="step-my-code">
                            <div class="flex items-center justify-between">
                                <p class="tech-label">Tu código</p>
                                <button type="button" class="text-xs text-primary-bright hover:underline"
                                    x-data x-on:click="navigator.clipboard.writeText(@js($mine->code)); $el.textContent = '¡Copiado!'">Copiar</button>
                            </div>
                            <pre class="overflow-x-auto rounded-lg border border-outline bg-surface-lowest p-3 font-mono text-sm text-ink">{{ $mine->code }}</pre>
                        </div>
                    @endif
                    @if (filled($mine->output))
                        <div class="flex flex-col gap-1">
                            <p class="tech-label">Lo que obtuviste</p>
                            <pre class="overflow-x-auto rounded-lg border border-success/30 bg-surface-lowest p-3 font-mono text-sm text-success">{{ $mine->output }}</pre>
                        </div>
                    @endif
                    @if ($texts['success'])
                        <div class="markdown text-sm text-ink">{!! $texts['success'] !!}</div>
                    @endif
                    @if ($step->card_title)
                        <p class="flex flex-wrap items-center gap-2 text-xs">
                            <span class="flex items-center gap-1.5 rounded border border-secondary/40 px-2 py-1 text-secondary-bright"><flux:icon name="book-open" variant="micro" /> {{ $step->card_title }}</span>
                            @if ($step->card_body)
                                <span class="font-mono text-ink-muted">{{ $step->card_body }}</span>
                            @endif
                        </p>
                    @endif
                </div>
            </details>
        @elseif ($currentStep?->is($step))
            {{-- La que toca: escena, pista de Gheco, desafío y el editor. --}}
            {{-- result: lo que contestó el servidor al superarla (se queda en pantalla hasta tocar «Siguiente»). --}}
            <article class="panel panel-active flex flex-col overflow-hidden" wire:key="step-current-{{ $step->id }}" data-test="step-current"
                x-data="{ result: null }">
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

                    {{-- Una micro-misión puede ser de otro lenguaje que el curso (SQL en Java, con SQLite en el navegador). --}}
                    @php($stepLanguage = $step->runLanguage($course))
                    <x-code-runner :code="(string) $step->starter_code" :stdin="(string) $step->sample_input" :expected="$step->expected_output"
                        :language="$stepLanguage->value" :name="strtolower($step->code)" :runnable="$stepLanguage->studentCanRun()"
                        :show-stdin="filled($step->sample_input)">
                        <x-slot:footer>
                            {{-- Al coincidir la salida, se avisa una sola vez. --}}
                            <div x-data="{ sent: false }" x-effect="if (matches === true && ! sent) { sent = true; $wire.completeStep({{ $step->id }}, output, code).then((r) => { result = r; if (! r.ok) sent = false }) }">
                                <p x-show="matches === false" x-cloak class="flex items-center gap-2 text-sm text-warning" data-test="step-mismatch">
                                    <flux:icon name="exclamation-triangle" variant="micro" /> Todavía no: tu salida no es igual a la esperada. Comparalas línea por línea.
                                </p>
                                <p x-show="result && ! result.ok" x-cloak class="flex items-center gap-2 text-sm text-danger" x-text="result?.error"></p>
                            </div>
                            {{-- Java (D85): sin el ejecutor abierto, se corre en la compu o el IDE y se pega la salida. --}}
                            @if ($stepLanguage->runsOnLocalRunner())
                                <details class="mt-2 rounded-lg border border-outline/70 px-3 py-2 text-sm" x-show="! result?.ok" x-data="{ pasted: '', checking: false, wrong: false }" data-test="step-paste">
                                    <summary class="cursor-pointer text-ink-muted hover:text-white">¿No tenés el ejecutor abierto? Corré el programa en tu compu y pegá acá lo que mostró</summary>
                                    <div class="mt-2 flex flex-col gap-2">
                                        <textarea x-model="pasted" rows="4" class="w-full rounded-md border border-outline bg-surface-lowest p-2 font-mono text-sm text-ink" placeholder="La salida de tu programa, tal cual" data-test="step-paste-output"></textarea>
                                        <div class="flex items-center gap-3">
                                            <flux:button size="sm" variant="primary" x-bind:disabled="checking || pasted.trim() === ''" data-test="step-paste-check"
                                                x-on:click="checking = true; wrong = false; $wire.completeStep({{ $step->id }}, pasted, code).then((r) => { checking = false; if (r.ok) { result = r } else { wrong = true } })">Comprobar</flux:button>
                                            <span x-show="wrong" x-cloak class="text-warning">Todavía no: esa salida no es igual a la esperada. Comparalas línea por línea.</span>
                                        </div>
                                    </div>
                                </details>
                            @endif
                        </x-slot:footer>
                    </x-code-runner>

                    {{-- Superada: qué pasó en la historia, qué ganó y recién ahí «Siguiente». --}}
                    <section x-show="result?.ok" x-cloak x-transition class="flex flex-col gap-4 rounded-lg border border-success/40 bg-success/10 p-5" data-test="step-success">
                        <p class="flex items-center gap-2 font-display text-lg font-semibold text-success">
                            <flux:icon name="check-badge" variant="mini" /> ¡Micro-misión superada!
                        </p>
                        @if ($texts['success'])
                            <div class="markdown text-ink">{!! $texts['success'] !!}</div>
                        @endif
                        <div class="flex flex-col gap-2">
                            <p class="tech-label">Ganaste</p>
                            <ul class="flex flex-wrap gap-2 text-sm">
                                <li class="flex items-center gap-1.5 rounded-lg border border-warning/40 bg-warning/10 px-3 py-1.5 text-warning">
                                    <flux:icon name="sparkles" variant="micro" />
                                    <span x-text="result?.xp > 0 ? '+' + result.xp + ' {{ term('xp.short') }}' : '{{ term('xp.short') }} (ya la tenías o sos del staff)'"></span>
                                </li>
                                @if ($step->card_title)
                                    <li class="flex items-center gap-1.5 rounded-lg border border-secondary/40 bg-secondary/10 px-3 py-1.5 text-secondary-bright" title="{{ $step->card_body }}">
                                        <flux:icon name="book-open" variant="micro" /> Carta del grimorio: {{ $step->card_title }}
                                    </li>
                                @endif
                                @if ($gold && $step->gold_reward > 0)
                                    <li class="flex items-center gap-1.5 rounded-lg border border-warning/40 bg-warning/10 px-3 py-1.5 text-warning" data-test="step-gold">
                                        <x-gold-icon class="size-4" /> <span x-text="result?.xp > 0 ? '+{{ $step->gold_reward }} de oro' : 'Oro (ya lo tenías o sos del staff)'"></span>
                                    </li>
                                @endif
                                @if ($inventory && $step->item)
                                    <li class="flex items-center gap-1.5 rounded-lg border border-success/40 bg-success/10 px-3 py-1.5 text-success">
                                        <flux:icon name="gift" variant="micro" /> {{ $step->item }}
                                    </li>
                                @endif
                            </ul>
                            @if ($step->card_body)
                                <p class="font-mono text-xs text-ink-muted">{{ $step->card_body }}</p>
                            @endif
                            @if ($inventory && $texts['unlocks'])
                                <div class="markdown text-sm text-ink"><strong>Se abre:</strong> {!! $texts['unlocks'] !!}</div>
                            @endif
                        </div>
                        <p class="text-sm text-ink-muted">Tomate un momento: mirá tu código y la salida. Cuando quieras, seguí.</p>
                        <div class="flex justify-end">
                            @if ($loop->last)
                                <flux:button variant="primary" icon:trailing="arrow-down" x-on:click="$wire.$refresh()" data-test="step-next">Terminar las micro-misiones</flux:button>
                            @else
                                <flux:button variant="primary" icon:trailing="arrow-right" x-on:click="$wire.$refresh()" data-test="step-next">Siguiente micro-misión</flux:button>
                            @endif
                        </div>
                    </section>

                    <p x-show="! result?.ok" class="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-ink-muted">
                        <span class="flex items-center gap-1"><flux:icon name="sparkles" variant="micro" class="text-warning" /> +{{ $step->xp_reward }} {{ term('xp.short') }}</span>
                        @if ($step->card_title)
                            <span class="flex items-center gap-1"><flux:icon name="book-open" variant="micro" class="text-secondary-bright" /> Carta: {{ $step->card_title }}</span>
                        @endif
                        @if ($gold && $step->gold_reward > 0)
                            <span class="flex items-center gap-1"><x-gold-icon class="size-3.5" /> +{{ $step->gold_reward }} de oro</span>
                        @endif
                        @if ($inventory && $step->item)
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
