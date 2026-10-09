{{-- El prólogo animado (D84 § 1): las 6 tomas de «El mundo que vive en tu mente», con la voz de Gheco y música.
     Arranca con una bienvenida («Ingresar a la historia» o «Ver sin música») que prende juntos el pase automático y la música. Se ve en Mis Crónicas → Prólogo. --}}
@php
    $scenes = [
        ['tag' => 'La vigilia solitaria', 'text' => 'Hay un mundo que no aparece en ningún mapa. No está al otro lado del mar ni detrás de las montañas: está adentro de la cabeza de quien programa. Se enciende la primera vez que alguien escribe una instrucción y la ve cobrar vida en la pantalla.', 'gheco' => 'Todo gran viaje empieza en una noche de dudas.'],
        ['tag' => 'El portal de Gheco', 'text' => 'Esa noche, un portal se abrió frente a vos. Del otro lado te espera Gheco, un gecko de escamas cian que conoce todos los caminos, porque trepa por las paredes entre un mundo y otro.', 'gheco' => '—Tranquila, tranquilo. Nadie llega sabiendo. Se llega aprendiendo.'],
        ['tag' => 'Los senderos y las lenguas', 'text' => 'Lo llaman el Mundo del Código. A sus regiones no se llega a pie: se llega por portales, y cada portal es una lengua. Algunos huelen a bosque; otros, a hierro recién forjado; otros brillan como vidrio de colores.', 'gheco' => 'Elegí una puerta. Lo que aprendas en una va a abrir las demás.'],
        ['tag' => 'Cruzando el umbral', 'text' => 'Nadie los conoce todos. Nadie terminó nunca de recorrerlo, porque cada puerta que se abre deja ver otras dos. Cada instrucción que escribís es una chispa que despierta tu propio portal.', 'gheco' => 'Tocalo sin miedo. El código responde a lo que escribís.'],
        ['tag' => 'El horizonte infinito', 'text' => 'Por eso, en este mundo, lo que aprendés no se pierde: cada rama que crece en tu árbol se toca con otra. Lo que te enseñe una región te va a servir en la siguiente, y en la que todavía no existe.', 'gheco' => 'Mirá ese horizonte: cada castillo se levantó línea por línea.'],
        ['tag' => 'El futuro también se programa', 'text' => 'El Mundo del Código vive en la mente de quien programa. Aprender no es llegar a un final: es seguir abriendo puertas. El árbol nunca termina y todo se conecta.', 'gheco' => 'Mejor código, sueños más grandes. El futuro también se programa…'],
    ];
@endphp
<section class="flex flex-col gap-3" data-test="prologue-player" wire:ignore
    x-data="{
        scenes: @js($scenes), i: 0, playing: false, music: false, started: false, timer: null, seconds: 14,
        start(withMusic) { this.started = true; this.playing = true; this.schedule(); if (withMusic) this.toggleMusic(); },
        go(n) { this.i = (n + this.scenes.length) % this.scenes.length; if (this.playing) this.schedule(); },
        schedule() { clearTimeout(this.timer); this.timer = setTimeout(() => { if (this.i === this.scenes.length - 1) { this.playing = false; return; } this.go(this.i + 1); }, this.seconds * 1000); },
        toggle() { this.playing = ! this.playing; this.playing ? this.schedule() : clearTimeout(this.timer); },
        toggleMusic() { this.music = ! this.music; const a = this.$refs.audio; this.music ? a.play().catch(() => this.music = false) : a.pause(); },
    }"
    x-on:keydown.right.window="go(i + 1)" x-on:keydown.left.window="go(i - 1)"
    x-on:livewire:navigating.window="$refs.audio.pause(); clearTimeout(timer)">
    <div class="relative aspect-video w-full overflow-hidden rounded-xl border border-primary/40 bg-[#030712] shadow-[0_0_40px_rgba(6,182,212,.15)]">
        <template x-for="(scene, n) in scenes" :key="n">
            <img :src="'{{ asset('img/prologo') }}/c' + (n + 1) + '.webp'" alt="" loading="lazy"
                class="absolute inset-0 size-full object-cover transition-opacity duration-1000"
                :class="n === i ? 'opacity-100 prologue-kenburns' : 'opacity-0'">
        </template>
        <div class="absolute inset-0 bg-gradient-to-t from-[#030712] via-[#030712]/35 to-transparent"></div>

        <div class="absolute top-3 left-3 flex items-center gap-2">
            <span class="rounded-full border border-primary/50 bg-[#030712]/80 px-2.5 py-1 font-mono text-[11px] text-primary-bright" x-text="'Toma ' + String(i + 1).padStart(2, '0') + ' / 06'"></span>
            <span class="hidden rounded-full bg-[#030712]/70 px-2.5 py-1 text-xs text-ink sm:inline" x-text="scenes[i].tag"></span>
        </div>
        <button type="button" x-on:click="toggleMusic()" class="absolute top-3 right-3 flex items-center gap-1.5 rounded-full border border-outline bg-[#030712]/80 px-3 py-1 text-xs text-ink hover:text-primary-bright" data-test="prologue-music">
            <flux:icon name="musical-note" variant="micro" /> <span x-text="music ? 'Música: sí' : 'Música: no'"></span>
        </button>

        <button type="button" x-on:click="go(i - 1)" aria-label="Toma anterior" class="absolute top-1/2 left-3 grid size-10 -translate-y-1/2 place-items-center rounded-full border border-outline bg-[#030712]/70 text-white hover:border-primary-bright">‹</button>
        <button type="button" x-on:click="go(i + 1)" aria-label="Toma siguiente" class="absolute top-1/2 right-3 grid size-10 -translate-y-1/2 place-items-center rounded-full border border-outline bg-[#030712]/70 text-white hover:border-primary-bright" data-test="prologue-next">›</button>

        <div class="absolute inset-x-0 bottom-0 flex flex-col gap-2 p-4 sm:p-6">
            <p class="font-mono text-[11px] tracking-widest text-primary-bright uppercase" x-text="'Prólogo · Fragmento ' + ['I', 'II', 'III', 'IV', 'V', 'VI'][i]"></p>
            <p class="max-w-3xl text-sm leading-relaxed text-white italic drop-shadow-[0_2px_4px_rgba(0,0,0,.95)] sm:text-lg" x-text="'«' + scenes[i].text + '»'" data-test="prologue-text"></p>
        </div>

        {{-- La bienvenida: el navegador solo deja sonar la música después de un clic, así que este botón arranca todo junto. --}}
        <div x-show="! started" x-transition.opacity.duration.500ms class="absolute inset-0 z-10 grid place-items-center bg-[#030712]/75 p-4 backdrop-blur-[2px]" data-test="prologue-start">
            <div class="flex max-w-md flex-col items-center gap-3 rounded-2xl border border-primary/40 bg-[#070d1d]/85 p-5 text-center shadow-2xl sm:p-7">
                <span class="font-mono text-[11px] tracking-widest text-primary-bright uppercase">Prólogo · El Mundo del Código</span>
                <p class="font-display text-xl font-semibold text-white sm:text-2xl">El mundo que vive en tu mente</p>
                <p class="text-sm text-ink-muted">Seis tomas con música de fondo. Pasan solas; podés pausar cuando quieras.</p>
                <button type="button" x-on:click="start(true)" class="flex items-center gap-2 rounded-xl bg-gradient-to-r from-cyan-500 to-emerald-400 px-6 py-2.5 font-semibold text-[#030712] transition hover:scale-105" data-test="prologue-enter">
                    <flux:icon name="play" variant="micro" /> Ingresar a la historia
                </button>
                <button type="button" x-on:click="start(false)" class="text-xs text-ink-muted hover:text-white">Ver sin música</button>
            </div>
        </div>
    </div>

    <div class="flex flex-wrap items-center gap-3">
        <button type="button" x-on:click="toggle()" class="flex items-center gap-2 rounded-full bg-primary px-4 py-1.5 text-sm font-medium text-white hover:bg-primary-bright" data-test="prologue-play">
            <span x-text="playing ? 'Pausar' : (i === 0 ? 'Ver el prólogo' : 'Seguir')"></span>
        </button>
        <div class="h-1.5 min-w-32 flex-1 overflow-hidden rounded-full bg-surface-high">
            <div class="h-full rounded-full bg-gradient-to-r from-cyan-500 to-emerald-400 transition-all duration-500" :style="'width:' + ((i + 1) / scenes.length * 100) + '%'"></div>
        </div>
    </div>

    <div class="flex items-start gap-3 rounded-lg border border-primary/30 bg-primary/5 p-3">
        <img src="{{ asset('img/personajes/gheco.webp') }}" alt="" class="size-10 shrink-0 rounded-full object-cover">
        <p class="text-sm text-ink"><span class="font-medium text-primary-bright">Gheco:</span> <span x-text="'«' + scenes[i].gheco + '»'"></span></p>
    </div>

    <div class="grid grid-cols-6 gap-2">
        <template x-for="(scene, n) in scenes" :key="'t' + n">
            <button type="button" x-on:click="go(n)" class="overflow-hidden rounded-lg border-2 transition" :class="n === i ? 'border-primary-bright' : 'border-transparent opacity-60 hover:opacity-100'" :aria-label="'Toma ' + (n + 1)">
                <img :src="'{{ asset('img/prologo') }}/c' + (n + 1) + '.webp'" alt="" class="aspect-video w-full object-cover" loading="lazy">
            </button>
        </template>
    </div>

    <audio x-ref="audio" src="{{ asset('audio/prologo.mp3') }}" loop preload="none"></audio>
</section>
