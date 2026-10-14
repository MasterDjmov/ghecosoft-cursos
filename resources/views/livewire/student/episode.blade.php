{{-- Crónicas en Inglés (D106): un episodio. Cada micro-misión tiene su escena, la historia en inglés (cada palabra
     se toca y se escucha), la traducción, las palabras nuevas, la pista de Gheco y el ejercicio, que se comprueba en
     el navegador (resources/js/runners/english.js). Con ?leer=1, el episodio entero para leer y escuchar. --}}
@php
    $libraryUrl = route('student.tree', $course);
    $total = $steps->count();
    $doneCount = $steps->where('done', true)->count();
    $gold = (bool) config('game.gold_enabled');
    $allWords = $steps->flatMap(fn ($s) => $s['words'])->pluck('en')->unique()->values();
    $markClass = "{ 'border-success text-success': mark === 'ok', 'border-warning text-warning': mark === 'almost', 'border-danger text-danger': mark === 'bad' }";
@endphp

<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8" data-test="episode-page">
    <header class="flex flex-col gap-3 sm:flex-row sm:items-center">
        <a href="{{ $libraryUrl }}" wire:navigate class="flex items-center gap-1.5 text-sm text-ink-muted hover:text-white">
            <flux:icon name="chevron-left" variant="micro" /> Biblioteca
        </a>
        <div class="flex min-w-0 flex-1 flex-col">
            <p class="tech-label">{{ $course->title }}</p>
            <h1 class="font-display text-2xl font-semibold text-white">{{ $node->title }}</h1>
        </div>
        <div class="inline-flex self-start rounded-lg border border-outline bg-surface-low p-1 sm:self-center">
            <a href="{{ route('student.node', [$course, $node]) }}" wire:navigate class="flex items-center gap-2 rounded-md px-3 py-1.5 text-sm font-medium {{ $reading ? 'text-ink-muted hover:text-ink' : 'bg-primary-bright text-surface' }}">
                <flux:icon name="bolt" variant="micro" /> Practicar
            </a>
            <a href="{{ route('student.node', [$course, $node]) }}?leer=1" wire:navigate class="flex items-center gap-2 rounded-md px-3 py-1.5 text-sm font-medium {{ $reading ? 'bg-primary-bright text-surface' : 'text-ink-muted hover:text-ink' }}" data-test="episode-read-tab">
                <flux:icon name="book-open" variant="micro" /> Leer
            </a>
        </div>
    </header>

    @if ($reading)
        {{-- El episodio entero, para leer y escuchar. --}}
        <section class="flex flex-col gap-6" data-test="episode-reading"
            x-data="{ spanish: false, all: @js($steps->pluck('config.story')->implode(' ')) }">
            <div class="flex flex-wrap gap-2">
                <flux:button size="sm" variant="primary" icon="speaker-wave" x-on:click="window.speakEnglish(all)">Escuchar todo</flux:button>
                <flux:button size="sm" icon="stop" x-on:click="window.speechSynthesis?.cancel()">Parar</flux:button>
                <button type="button" x-on:click="spanish = ! spanish" class="rounded-lg border border-outline px-3 py-1.5 text-sm text-ink-muted transition hover:text-ink"
                    x-text="spanish ? 'Ocultar el español' : 'Ver en español'">Ver en español</button>
            </div>
            @foreach ($steps as $step)
                <article class="panel grid gap-4 overflow-hidden p-4 md:grid-cols-[minmax(0,2fr)_minmax(0,3fr)]">
                    @if ($step['image'])
                        <img src="{{ $step['image'] }}" alt="" class="aspect-video w-full rounded-lg border border-outline object-cover" loading="lazy">
                    @endif
                    <div class="flex flex-col gap-2">
                        <h2 class="font-display text-lg font-semibold text-white">{{ $step['model']->title }}</h2>
                        <p class="text-lg leading-relaxed text-ink">{{ $step['model']->scene }}</p>
                        <p x-show="spanish" x-cloak class="text-ink-muted">{{ $step['model']->translation }}</p>
                        <div class="flex gap-2">
                            <flux:button size="xs" icon="speaker-wave" x-on:click="window.speakEnglish(@js((string) $step['model']->scene))">English</flux:button>
                            <flux:button size="xs" icon="speaker-wave" x-on:click="window.speakEnglish(@js((string) $step['model']->translation), { lang: 'es' })">Español</flux:button>
                        </div>
                    </div>
                </article>
            @endforeach
        </section>
    @else
        <div class="flex items-center gap-3">
            <div class="h-1.5 flex-1 overflow-hidden rounded-full bg-surface-highest" role="progressbar" aria-valuemin="0" aria-valuemax="{{ $total }}" aria-valuenow="{{ $doneCount }}">
                <div class="h-full rounded-full bg-warning transition-all" style="width: {{ $total ? round($doneCount / $total * 100) : 0 }}%"></div>
            </div>
            <span class="font-mono text-xs text-ink-muted" data-test="episode-steps-progress">{{ $doneCount }} de {{ $total }}</span>
        </div>

        @foreach ($steps as $step)
            @php($model = $step['model'])
            @if ($step['done'] && ! $current?->is($model))
                <details class="group rounded-lg border border-success/30 bg-success/5" wire:key="en-done-{{ $model->id }}" data-test="en-step-done">
                    <summary class="flex cursor-pointer list-none items-center gap-3 px-4 py-3 text-sm">
                        <flux:icon name="check-circle" variant="mini" class="shrink-0 text-success" />
                        <span class="font-medium text-ink">{{ $model->title }}</span>
                        @if ($model->card_title)
                            <span class="ms-auto hidden rounded border border-secondary/40 px-2 py-0.5 font-mono text-[11px] text-secondary-bright sm:inline">{{ $model->card_title }}</span>
                        @endif
                    </summary>
                    <div class="flex flex-col gap-2 border-t border-success/20 px-4 py-3">
                        <p class="text-ink">{{ $model->scene }}</p>
                        <p class="text-sm text-ink-muted">{{ $model->translation }}</p>
                    </div>
                </details>
            @elseif ($current?->is($model))
                <article class="panel panel-active flex flex-col overflow-hidden" wire:key="en-current-{{ $model->id }}" data-test="en-step-current"
                    x-data="englishStep(@js($step['config']))" @if ($doneCount > 0) x-init="$nextTick(() => $el.scrollIntoView({ behavior: 'smooth', block: 'start' }))" @endif>
                    @if ($step['image'])
                        <figure class="relative aspect-[16/7] overflow-hidden border-b border-outline">
                            <img src="{{ $step['image'] }}" alt="" class="size-full object-cover">
                            <div class="absolute inset-0 bg-gradient-to-t from-[#070a14] via-transparent to-transparent"></div>
                            <figcaption class="absolute bottom-3 left-4 font-display text-xl font-semibold text-white">{{ $model->title }}</figcaption>
                        </figure>
                    @else
                        <h2 class="px-5 pt-5 font-display text-xl font-semibold text-white">{{ $model->title }}</h2>
                    @endif

                    <div class="grid gap-6 p-5 lg:grid-cols-2">
                        {{-- La historia --}}
                        <div class="flex flex-col gap-3">
                            <p class="whitespace-pre-wrap text-xl leading-relaxed text-white" data-test="en-story"><template x-for="(token, i) in tokens" :key="i"><span x-text="token.text" x-on:click="sayWord(token)" :class="token.word && 'cursor-pointer rounded hover:bg-primary/20 hover:text-primary-bright'"></span></template></p>
                            <p x-show="showSpanish" x-cloak class="text-ink-muted" data-test="en-translation">{{ $model->translation }}</p>
                            <div class="flex flex-wrap gap-2">
                                <flux:button size="sm" variant="primary" icon="speaker-wave" x-on:click="sayStory()">English</flux:button>
                                <flux:button size="sm" icon="speaker-wave" x-on:click="saySpanish()">Español</flux:button>
                                <button type="button" x-on:click="showSpanish = ! showSpanish" class="rounded-md border border-outline px-2.5 py-1 text-sm text-ink-muted transition hover:text-ink"
                                    x-text="showSpanish ? 'Ocultar el español' : 'Ver en español'">Ver en español</button>
                                <button type="button" x-on:click="slow = ! slow" class="rounded-md border px-2.5 py-1 text-sm transition"
                                    :class="slow ? 'border-warning text-warning' : 'border-outline text-ink-muted hover:text-ink'">🐢 <span x-text="slow ? 'Despacio' : 'Normal'"></span></button>
                            </div>
                            @if ($step['words'] !== [])
                                <div class="flex flex-col gap-1.5">
                                    <p class="tech-label">Palabras nuevas</p>
                                    <ul class="flex flex-wrap gap-2">
                                        @foreach ($step['words'] as $word)
                                            <li><button type="button" x-on:click="say(@js($word['en']))" class="flex items-center gap-1.5 rounded-lg border border-secondary/40 bg-secondary/10 px-2.5 py-1 text-sm hover:bg-secondary/20">
                                                <flux:icon name="speaker-wave" variant="micro" class="text-secondary-bright" />
                                                <span class="text-white">{{ $word['en'] }}</span>
                                                @if ($word['es'])
                                                    <span class="text-ink-muted">· {{ $word['es'] }}</span>
                                                @endif
                                            </button></li>
                                        @endforeach
                                    </ul>
                                </div>
                            @endif
                        </div>

                        {{-- El desafío --}}
                        <div class="flex flex-col gap-4" x-show="! (result?.ok)">
                            <p class="flex items-start gap-2 font-medium text-white" x-show="exercise.prompt">
                                <flux:icon name="sparkles" variant="mini" class="mt-0.5 shrink-0 text-warning" /> <span x-text="exercise.prompt"></span>
                            </p>

                            {{-- leer: la portada del episodio --}}
                            <template x-if="type === 'read'">
                                <flux:button variant="primary" icon:trailing="arrow-right" x-on:click="pass()" x-bind:disabled="sending" data-test="en-read-next">¡Sigamos!</flux:button>
                            </template>

                            {{-- escuchar --}}
                            <template x-if="type === 'listen'">
                                <div class="flex flex-col gap-3" data-test="en-listen">
                                    <div class="flex items-center gap-3">
                                        <flux:button variant="primary" icon="speaker-wave" x-on:click="playRound()">Escuchar</flux:button>
                                        <span class="font-mono text-xs text-ink-muted" x-text="`${Math.min(round + 1, exercise.items.length)} de ${exercise.items.length}`"></span>
                                    </div>
                                    <div class="grid grid-cols-2 gap-2 sm:grid-cols-3">
                                        <template x-for="option in exercise.options" :key="option">
                                            <button type="button" x-on:click="pickOption(option)" class="rounded-lg border border-outline bg-surface-low px-3 py-3 text-lg font-semibold text-white transition hover:border-primary-bright" x-text="option"></button>
                                        </template>
                                    </div>
                                </div>
                            </template>

                            {{-- completar (fichas) y escribir (se tipea) --}}
                            <template x-if="type === 'fill' || type === 'write'">
                                <div class="flex flex-col gap-3" data-test="en-holes">
                                    <template x-for="(item, i) in exercise.items" :key="i">
                                        <div class="flex flex-wrap items-center gap-1.5 text-lg text-white">
                                            <span x-show="item.swatch" class="size-7 rounded-md border border-outline" :style="`background: ${item.swatch}`"></span>
                                            <template x-for="(part, p) in item.parts" :key="p">
                                                <span class="contents">
                                                    <span x-show="part.t !== undefined" x-text="part.t"></span>
                                                    <template x-if="(part.hole || part.free) && exercise.bank.length">
                                                        <button type="button" x-data="{ get mark() { return marks[i][p] } }" x-on:click="selectHole(i, p)" x-on:dragover.prevent x-on:drop.prevent="dropChip($event, i, p)"
                                                            class="min-w-16 rounded-md border-2 border-dashed px-2 py-0.5 font-semibold" :class="Object.assign({{ $markClass }}, { 'border-primary-bright': selectedHole && selectedHole[0] === i && selectedHole[1] === p && ! mark, 'border-outline': ! mark })"
                                                            x-text="answers[i][p] || '…'"></button>
                                                    </template>
                                                    <template x-if="(part.hole || part.free) && ! exercise.bank.length">
                                                        <input type="text" x-data="{ get mark() { return marks[i][p] } }" x-model="answers[i][p]" x-on:keydown.enter="checkHoles()" autocomplete="off" autocapitalize="off" spellcheck="false"
                                                            class="w-32 rounded-md border-2 bg-surface-lowest px-2 py-0.5 font-semibold text-white" :class="Object.assign({{ $markClass }}, { 'border-outline': ! mark })" :placeholder="part.free === 'name' ? 'tu nombre' : (part.free === 'number' ? '0' : '')">
                                                    </template>
                                                </span>
                                            </template>
                                        </div>
                                    </template>
                                    <div class="flex flex-wrap gap-2" x-show="exercise.bank.length">
                                        <template x-for="chip in bankChips" :key="chip.index">
                                            <button type="button" draggable="true" x-on:dragstart="dragChip($event, chip)" x-on:click="placeChip(chip)" :disabled="chip.used"
                                                class="rounded-lg border border-primary-bright/50 bg-primary/15 px-3 py-1.5 font-semibold text-white transition hover:bg-primary/30 disabled:opacity-30" x-text="chip.word"></button>
                                        </template>
                                    </div>
                                    <div><flux:button variant="primary" x-on:click="checkHoles()" data-test="en-check">Comprobar</flux:button></div>
                                </div>
                            </template>

                            {{-- ordenar y letras --}}
                            <template x-if="type === 'order' || type === 'letters'">
                                <div class="flex flex-col gap-3" data-test="en-tiles">
                                    <div class="flex items-center gap-2" x-show="type === 'letters'">
                                        <flux:button size="sm" icon="speaker-wave" x-on:click="say(exercise.items[round]?.word)">Escuchar la palabra</flux:button>
                                        <span class="font-mono text-xs text-ink-muted" x-text="`${Math.min(round + 1, exercise.items.length)} de ${exercise.items.length}`"></span>
                                    </div>
                                    <div class="flex min-h-14 flex-wrap items-center gap-2 rounded-lg border-2 border-dashed border-outline p-2">
                                        <template x-for="tile in built" :key="tile.index">
                                            <button type="button" x-on:click="giveBack(tile)" class="rounded-md bg-primary-bright px-3 py-1.5 text-lg font-semibold text-surface" x-text="tile.word"></button>
                                        </template>
                                    </div>
                                    <div class="flex flex-wrap gap-2">
                                        <template x-for="tile in pool" :key="tile.index">
                                            <button type="button" x-on:click="take(tile)" class="rounded-md border border-outline bg-surface-low px-3 py-1.5 text-lg font-semibold text-white hover:border-primary-bright" x-text="tile.word"></button>
                                        </template>
                                    </div>
                                    <div><flux:button variant="primary" x-on:click="type === 'order' ? checkOrder() : checkLetters()" data-test="en-check">Comprobar</flux:button></div>
                                </div>
                            </template>

                            {{-- dictado --}}
                            <template x-if="type === 'dictation'">
                                <div class="flex flex-col gap-3" data-test="en-dictation">
                                    <div class="flex gap-2">
                                        <flux:button variant="primary" icon="speaker-wave" x-on:click="say(exercise.items[0].say)">Escuchar</flux:button>
                                        <flux:button icon="speaker-wave" x-on:click="window.speakEnglish(exercise.items[0].say, { rate: 0.55 })">Más despacio</flux:button>
                                    </div>
                                    <textarea x-model="dictationText" rows="2" autocomplete="off" autocapitalize="off" spellcheck="false" class="w-full rounded-md border border-outline bg-surface-lowest p-2 text-lg text-white" placeholder="Escribí lo que escuchás"></textarea>
                                    <p class="flex flex-wrap gap-1.5" x-show="dictationMarks.length">
                                        <template x-for="(m, i) in dictationMarks" :key="i">
                                            <span class="rounded px-1.5 py-0.5 font-mono text-sm" :class="m.ok ? 'bg-success/20 text-success' : 'bg-surface-highest text-ink-muted'" x-text="m.ok ? m.word : '•'.repeat(m.word.length)"></span>
                                        </template>
                                    </p>
                                    <div><flux:button variant="primary" x-on:click="checkDictation()" data-test="en-check">Comprobar</flux:button></div>
                                </div>
                            </template>

                            {{-- responder y transformar --}}
                            <template x-if="type === 'answer' || type === 'transform'">
                                <div class="flex flex-col gap-4" data-test="en-free">
                                    <template x-for="(item, i) in exercise.items" :key="i">
                                        <label class="flex flex-col gap-1.5">
                                            <span class="flex items-center gap-2 text-white">
                                                <button type="button" x-on:click="say(item.prompt.replace(/\(.*\)/, ''))" class="text-secondary-bright"><flux:icon name="speaker-wave" variant="micro" /></button>
                                                <span x-text="item.prompt"></span>
                                            </span>
                                            <input type="text" x-data="{ get mark() { return marks[i] } }" x-model="answers[i]" x-on:keydown.enter="checkFree()" autocomplete="off" autocapitalize="off" spellcheck="false"
                                                class="rounded-md border-2 bg-surface-lowest px-3 py-1.5 text-lg text-white" :class="Object.assign({{ $markClass }}, { 'border-outline': ! mark })">
                                        </label>
                                    </template>
                                    <div><flux:button variant="primary" x-on:click="checkFree()" data-test="en-check">Comprobar</flux:button></div>
                                </div>
                            </template>

                            <p x-show="feedback" x-cloak class="rounded-lg border px-3 py-2 text-sm" data-test="en-feedback"
                                :class="{ 'border-success/50 bg-success/10 text-success': feedback?.kind === 'ok', 'border-warning/50 bg-warning/10 text-warning': feedback?.kind === 'almost', 'border-danger/50 bg-danger/10 text-danger': feedback?.kind === 'bad' }"
                                x-text="feedback?.text"></p>

                            @if ($step['hint'])
                                <aside class="flex items-start gap-3 rounded-lg border border-primary-bright/30 bg-primary/10 p-3" x-show="tries > 0 || type === 'read'">
                                    <img src="{{ asset('img/personajes/gheco.webp') }}" alt="Gheco" class="size-10 shrink-0 rounded-full border border-primary-bright/50 bg-surface-lowest object-cover">
                                    <div class="flex min-w-0 flex-col gap-1">
                                        <p class="tech-label text-primary-bright">Gheco sugiere</p>
                                        <div class="markdown text-sm text-ink">{!! $step['hint'] !!}</div>
                                    </div>
                                </aside>
                            @endif

                            {{-- Decilo en voz alta (INGLES.md § 4 bis): opcional, nunca traba. --}}
                            <template x-if="exercise.speak && canListen">
                                <div class="flex flex-col gap-2 rounded-lg border border-outline/70 p-3" data-test="en-speak">
                                    <p class="text-sm text-ink-muted">Extra: decilo en voz alta → <span class="font-semibold text-white" x-text="exercise.speak.replace(/\{\*\w+\}/, '…')"></span></p>
                                    <div class="flex flex-wrap items-center gap-2">
                                        <flux:button size="sm" icon="microphone" x-on:click="listen()" x-bind:disabled="listening"><span x-text="listening ? 'Escuchando…' : 'Decilo'">Decilo</span></flux:button>
                                        <flux:button size="sm" variant="ghost" icon="speaker-wave" x-on:click="say(exercise.speak.replace(/\{\*\w+\}/, ''))" x-show="! listening">Escuchar</flux:button>
                                        <span x-show="listening" class="text-sm text-primary-bright">Hablá ahora 🎙️</span>
                                    </div>
                                    <p x-show="spoken && ! listening" x-cloak class="rounded-lg border px-3 py-2 text-sm" data-test="en-speak-result"
                                        :class="{ 'border-success/50 bg-success/10 text-success': spoken?.verdict === 'ok', 'border-warning/50 bg-warning/10 text-warning': spoken?.verdict === 'almost', 'border-danger/50 bg-danger/10 text-danger': spoken?.verdict === 'bad' || spoken?.verdict === 'error' }"
                                        x-text="spoken?.verdict === 'ok' ? `⭐ ¡Muy bien! Entendí «${spoken.heard}».${spokenXp ? ` +${spokenXp} XP` : ''}`
                                            : spoken?.verdict === 'almost' ? `¡Casi! Entendí «${spoken.heard}». Probá de nuevo, más despacio.`
                                            : spoken?.verdict === 'error' ? spoken.heard
                                            : (spoken?.heard ? `Entendí «${spoken.heard}». Escuchá el modelo y probá de nuevo.` : 'No te entendí. Escuchá el modelo y probá de nuevo.')"></p>
                                </div>
                            </template>
                        </div>

                        {{-- Superada --}}
                        <section x-show="result?.ok" x-cloak x-transition class="flex flex-col gap-3 rounded-lg border border-success/40 bg-success/10 p-5" data-test="en-success">
                            <p class="flex items-center gap-2 font-display text-lg font-semibold text-success">
                                <flux:icon name="check-badge" variant="mini" /> ¡Misión superada!
                            </p>
                            <ul class="flex flex-wrap gap-2 text-sm">
                                <li class="flex items-center gap-1.5 rounded-lg border border-warning/40 bg-warning/10 px-3 py-1.5 text-warning">
                                    <flux:icon name="sparkles" variant="micro" />
                                    <span x-text="result?.xp > 0 ? '+' + result.xp + ' {{ term('xp.short') }}' : '{{ term('xp.short') }} (ya la tenías)'"></span>
                                </li>
                                @if ($gold && $model->gold_reward > 0)
                                    <li class="flex items-center gap-1.5 rounded-lg border border-warning/40 bg-warning/10 px-3 py-1.5 text-warning">
                                        <x-gold-icon class="size-4" /> +{{ $model->gold_reward }} de oro
                                    </li>
                                @endif
                                @if ($model->card_title)
                                    <li class="flex items-center gap-1.5 rounded-lg border border-secondary/40 bg-secondary/10 px-3 py-1.5 text-secondary-bright">
                                        <flux:icon name="book-open" variant="micro" /> Carta: {{ $model->card_title }}
                                    </li>
                                @endif
                            </ul>
                            @if ($model->card_body)
                                <p class="text-sm text-ink">{{ $model->card_body }}</p>
                            @endif
                            <div class="flex justify-end">
                                <flux:button variant="primary" icon:trailing="arrow-right" x-on:click="$wire.$refresh()" data-test="en-next">{{ $loop->last ? 'Terminar el episodio' : 'Siguiente' }}</flux:button>
                            </div>
                        </section>
                    </div>
                </article>
            @else
                <div class="flex items-center gap-3 rounded-lg border border-dashed border-outline/70 px-4 py-3 text-sm text-ink-muted" wire:key="en-locked-{{ $model->id }}">
                    <flux:icon name="lock-closed" variant="micro" /> {{ $model->title }}
                </div>
            @endif
        @endforeach

        @if ($finished)
            <section class="panel flex flex-col gap-4 p-5" data-test="episode-finished" x-data="{ words: @js($allWords->implode('! ')) }">
                <p class="flex items-center gap-2 font-display text-xl font-semibold text-success"><flux:icon name="trophy" /> ¡Terminaste el episodio!</p>
                @if ($pet)
                    <div class="flex items-center gap-3 rounded-lg border border-secondary/40 bg-secondary/5 p-3" data-test="episode-pet">
                        <img src="{{ $pet['image'] }}" alt="{{ $pet['label'] }}" class="h-20 w-15 shrink-0 rounded-lg object-cover">
                        <div class="flex flex-col gap-0.5 text-sm">
                            @if ($pet['grewNow'])
                                <p class="font-display text-lg font-semibold text-secondary-bright" data-test="pet-grew">¡{{ $pet['name'] }} creció! Ahora es {{ $pet['label'] }}.</p>
                                <p class="text-ink">{{ $pet['says'] }}</p>
                            @else
                                <p class="font-semibold text-white">{{ $pet['label'] }}</p>
                            @endif
                            @if ($pet['next'])
                                <p class="text-ink-muted">{{ $pet['next']['missing'] === 1 ? 'Le falta 1 episodio' : 'Le faltan '.$pet['next']['missing'].' episodios' }} para ser {{ $pet['next']['label'] }}.</p>
                            @endif
                        </div>
                    </div>
                @endif
                @if ($allWords->isNotEmpty())
                    <div class="flex flex-col gap-2">
                        <p class="text-ink">{{ $pet['name'] ?? 'Eco' }} repite las palabras que aprendiste:</p>
                        <div class="flex flex-wrap gap-2">
                            @foreach ($allWords as $word)
                                <span class="rounded-lg border border-secondary/40 bg-secondary/10 px-2.5 py-1 text-sm text-white">{{ $word }}</span>
                            @endforeach
                        </div>
                        <div><flux:button size="sm" icon="speaker-wave" x-on:click="window.speakEnglish(words + '!')">Escuchar a Eco</flux:button></div>
                    </div>
                @endif
                <div class="flex flex-wrap gap-2">
                    <flux:button variant="primary" icon="book-open" :href="$libraryUrl" wire:navigate>Volver a la biblioteca</flux:button>
                    <flux:button icon="book-open" :href="route('student.node', [$course, $node]).'?leer=1'" wire:navigate>Leer el episodio entero</flux:button>
                </div>
            </section>
        @endif
    @endif
</div>
