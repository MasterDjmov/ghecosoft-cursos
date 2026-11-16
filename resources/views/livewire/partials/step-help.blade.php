{{-- D123: «Necesito ayuda» (docs/AYUDA.md). Va adentro del editor de la micro-misión (ve code, matches, output…). Las
     ayudas se abren de la más suave a la más directa; la solución nunca llega entera de una vez. --}}
@php
    $helper = app(\App\Services\StepHelper::class);
    $withSolution = $helper->available($step);
    $canWhere = $withSolution && $helper->whereLines($step) !== [];
    $canLine = $withSolution && $helper->changedLines($step) !== [];
    // Comparar renglón por renglón solo tiene sentido con una salida de texto (no el Gólem, ni el inspector de HTML o JS).
    $canCompare = filled($step->expected_output) && blank($step->checks)
        && ! in_array($stepLanguage, [\App\Enums\Language::Asm, \App\Enums\Language::Html], true);
    $state = $canLine ? $helper->state(auth()->user(), $step) : ['lines' => [], 'solution' => null];
    // Los pasos van numerados en el orden en que aparecen.
    $n = 0;
@endphp
<div class="mt-3 flex flex-col gap-3" x-show="! result?.ok" data-test="step-help"
    x-data="stepHelp(@js(['stepId' => $step->id, 'compare' => $canCompare, 'expected' => (string) $step->expected_output, 'state' => $state]))"
    x-effect="watchRun()"
    x-on:step-read.window="if ($event.detail.id === {{ $step->id }}) readAloud(document.getElementById('challenge-{{ $step->id }}'))">

    {{-- Gheco ofrece una mano solo, sin que haga falta animarse a pedir. --}}
    <div x-show="offer" x-cloak x-transition class="flex flex-wrap items-center gap-3 rounded-lg border border-primary-bright/40 bg-primary/10 p-3 text-sm" data-test="step-help-offer">
        <img src="{{ asset('img/personajes/gheco.webp') }}" alt="Gheco" class="size-10 shrink-0 rounded-full border border-primary-bright/50 bg-surface-lowest object-cover">
        <p class="min-w-0 flex-1 text-ink"><strong class="text-primary-bright">¿Te doy una mano?</strong> Trabarse es parte de aprender: te muestro por dónde seguir.</p>
        <div class="flex gap-2">
            <flux:button size="sm" variant="primary" x-on:click="acceptOffer()" data-test="step-help-accept">Sí, ayudame</flux:button>
            <flux:button size="sm" variant="ghost" x-on:click="offer = false">Ahora no</flux:button>
        </div>
    </div>

    <button type="button" x-on:click="helpOpen = ! helpOpen; offer = false" data-test="step-help-toggle"
        class="flex w-fit items-center gap-2 rounded-lg border border-primary-bright/40 bg-primary/10 px-3 py-1.5 text-sm font-medium text-primary-bright transition hover:bg-primary/20">
        <span class="relative grid size-5 place-items-center">
            <span x-show="offer" x-cloak class="absolute inset-0 animate-ping rounded-full bg-primary-bright/50 motion-reduce:animate-none"></span>
            <flux:icon name="lifebuoy" variant="micro" class="relative" />
        </span>
        Necesito ayuda
        <flux:icon name="chevron-down" variant="micro" class="transition" x-bind:class="helpOpen && 'rotate-180'" />
    </button>

    <div x-show="helpOpen" x-cloak x-transition class="flex flex-col gap-4 rounded-lg border border-outline bg-surface-low/60 p-4 text-sm" data-test="step-help-panel">
        <p class="text-ink-muted">Usá las que necesites, de a una: van de la más suave a la más directa.</p>

        @if (filled($guide))
            {{-- ¿Qué me piden? (fase 2): el desafío en pasos cortos y literales, sin historia. --}}
            <div class="flex flex-col gap-1" data-test="step-help-guide">
                <p class="font-medium text-white">{{ ++$n }}. ¿Qué me piden?</p>
                <p class="text-ink-muted">El desafío, de a un paso por vez.</p>
                <flux:button size="sm" icon="list-bullet" class="w-fit" x-show="! guideOpen" x-on:click="showGuide()" data-test="step-help-guide-button">Mostrame los pasos</flux:button>
                <div x-show="guideOpen" x-cloak class="flex items-start gap-2 rounded-md border border-outline/70 bg-surface-lowest/60 p-3">
                    <div class="markdown min-w-0 flex-1 text-white" id="guide-{{ $step->id }}" data-test="step-help-guide-text">{!! $guide !!}</div>
                    <button type="button" x-show="canRead()" title="Escuchar los pasos" aria-label="Escuchar los pasos"
                        x-on:click="readAloud(document.getElementById('guide-{{ $step->id }}'))"
                        class="shrink-0 rounded-md p-1 text-ink-muted transition hover:bg-surface-high hover:text-white">
                        <flux:icon name="speaker-wave" variant="mini" />
                    </button>
                </div>
            </div>
        @endif

        {{-- Escuchar el desafío --}}
        <div x-show="canRead()" class="flex flex-col gap-1">
            <p class="font-medium text-white">{{ ++$n }}. Escuchá el desafío</p>
            <p class="text-ink-muted">A veces se entiende mejor oyéndolo.</p>
            <flux:button size="sm" icon="speaker-wave" class="w-fit" data-test="step-help-read" x-on:click="readAloud(document.getElementById('challenge-{{ $step->id }}'))"><span x-text="reading ? 'Parar' : 'Leémelo'">Leémelo</span></flux:button>
            <p x-show="readError" x-cloak x-text="readError" class="text-warning" data-test="step-help-read-error"></p>
        </div>

        @if ($canWhere)
            {{-- 2. ¿Dónde toco? --}}
            <div class="flex flex-col gap-1" data-test="step-help-where">
                <p class="font-medium text-white">{{ ++$n }}. ¿Dónde toco?</p>
                <p class="text-ink-muted">Te marco en el editor los renglones que hay que cambiar.</p>
                <flux:button size="sm" icon="cursor-arrow-rays" class="w-fit" x-on:click="showWhere()" x-bind:disabled="helpBusy">Marcámelos</flux:button>
                <p x-show="whereLines" x-cloak class="text-warning" x-text="whereText()" data-test="step-help-where-text"></p>
            </div>
        @endif

        @if ($canCompare)
            {{-- 3. Comparemos --}}
            <div class="flex flex-col gap-1" data-test="step-help-compare">
                <p class="font-medium text-white">{{ ++$n }}. Comparemos</p>
                <p class="text-ink-muted" x-show="! canCompare()">Ejecutá tu programa: si la salida no coincide, acá te la muestro al lado de la esperada.</p>
                <flux:button size="sm" icon="arrows-right-left" class="w-fit" x-show="canCompare()" x-on:click="toggleCompare()"><span x-text="compareOpen ? 'Ocultar' : 'Mostrame la diferencia'">Mostrame la diferencia</span></flux:button>
                <div x-show="compareOpen && canCompare()" x-cloak class="overflow-x-auto rounded-md border border-outline">
                    <table class="w-full font-mono text-xs">
                        <thead class="bg-surface-high text-left text-ink-muted">
                            <tr><th class="w-12 px-2 py-1">#</th><th class="px-2 py-1">Se esperaba</th><th class="px-2 py-1">Tu programa mostró</th></tr>
                        </thead>
                        <tbody>
                            <template x-for="(row, i) in rows()" :key="i">
                                <tr x-bind:class="row.first ? 'bg-warning/15' : (row.ok ? '' : 'bg-danger/10')">
                                    <td class="px-2 py-0.5 whitespace-nowrap text-ink-muted" x-text="(row.ok ? '✓ ' : '✗ ') + (i + 1)"></td>
                                    <td class="px-2 py-0.5 whitespace-pre text-success" x-text="row.want ?? '(nada)'"></td>
                                    <td class="px-2 py-0.5 whitespace-pre" x-bind:class="row.ok ? 'text-success' : 'text-warning'" x-text="row.have ?? '(falta este renglón)'"></td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                    <p class="border-t border-outline px-2 py-1 text-xs text-ink-muted">En los renglones distintos, «·» es un espacio. El primero que no coincide está resaltado: empezá por ahí.</p>
                </div>
            </div>
        @endif

        @if ($canLine)
            {{-- 4. Mostrame una línea --}}
            <div class="flex flex-col gap-1" data-test="step-help-line">
                <p class="font-medium text-white">{{ ++$n }}. Mostrame una línea</p>
                <p class="text-ink-muted">Te muestro un renglón de la solución por cada intento que no salga. Escribilo vos en tu código: escribirlo también es aprender.
                    <span class="text-warning">Si usás esta ayuda, la micro-misión da la mitad de {{ term('xp.short') }}{{ config('game.gold_enabled') ? ' y de oro' : '' }}.</span></p>
                <ol class="flex flex-col gap-1" x-show="shownLines.length && ! fullSolution" x-cloak>
                    <template x-for="line in shownLines" :key="line.number">
                        <li class="flex items-baseline gap-2 rounded-md border px-2 py-1" x-bind:class="line.number === newLine ? 'border-warning/60 bg-warning/10' : 'border-outline bg-surface-lowest'">
                            <span class="shrink-0 font-mono text-xs text-ink-muted" x-text="'renglón ' + line.number"></span>
                            <code class="font-mono whitespace-pre-wrap text-white select-none" x-text="line.text"></code>
                        </li>
                    </template>
                </ol>
                <p x-show="lineWait" x-cloak class="text-warning" data-test="step-help-wait">Primero probá con lo que ya te mostré: escribilo y ejecutá. Si sigue sin salir, te muestro el siguiente renglón.</p>
                <div x-show="fullSolution" x-cloak class="flex flex-col gap-1" data-test="step-help-solution">
                    <p class="text-ink-muted">Ya viste todos los renglones que cambian. Así queda la solución completa:</p>
                    <pre class="overflow-x-auto rounded-md border border-outline bg-surface-lowest p-3 font-mono text-sm text-ink select-none" x-text="fullSolution"></pre>
                </div>
                <flux:button size="sm" icon="eye" class="w-fit" x-show="! fullSolution" x-on:click="showLine()" x-bind:disabled="helpBusy" data-test="step-help-line-button"><span x-text="shownLines.length ? 'Mostrame otra línea' : 'Mostrame una línea'">Mostrame una línea</span></flux:button>
            </div>
        @endif

        {{-- 5. El profe --}}
        <p class="text-ink-muted"><span class="font-medium text-white">{{ ++$n }}. ¿Seguís trabado?</span> Abrí «Preguntale al profe», acá abajo: le llega tu código.</p>

        <p x-show="helpError" x-cloak class="text-danger" x-text="helpError"></p>
    </div>
</div>
