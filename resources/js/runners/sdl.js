// Juegos en C con SDL3 en el navegador (D126): compila con el Clang de C (D98, mismo worker) usando el SDL3 de la
// plataforma (sdl3/SDL.h) y corre el juego en su propio worker (workers/sdl-run.worker.js), que dibuja en un lienzo.
// La página le manda el teclado, el mouse y los joysticks; si el juego deja de responder, se corta (el Bucle Eterno).
import { compile } from './cpp.js';

// Las teclas por su lugar (KeyboardEvent.code → SDL_Scancode). Las que escriben letras o números dan su keycode
// en minúscula (SDLK_A = 'a'); las demás, el scancode con la máscara de SDL3.
const SCANCODES = {
    Enter: 40, Escape: 41, Backspace: 42, Tab: 43, Space: 44, Pause: 72,
    ArrowRight: 79, ArrowLeft: 80, ArrowDown: 81, ArrowUp: 82,
    ControlLeft: 224, ShiftLeft: 225, AltLeft: 226, ControlRight: 228, ShiftRight: 229, AltRight: 230,
};
for (let i = 0; i < 26; i++) SCANCODES[`Key${String.fromCharCode(65 + i)}`] = 4 + i;
for (let i = 1; i <= 9; i++) SCANCODES[`Digit${i}`] = 29 + i;
SCANCODES.Digit0 = 39;
for (let i = 1; i <= 12; i++) SCANCODES[`F${i}`] = 57 + i;
// El teclado numérico tiene sus propias teclas en SDL3 (SDLK_KP_1…), distintas de los números de arriba.
Object.assign(SCANCODES, { NumpadDivide: 84, NumpadMultiply: 85, NumpadSubtract: 86, NumpadAdd: 87, NumpadEnter: 88, Numpad0: 98, NumpadDecimal: 99 });
for (let i = 1; i <= 9; i++) SCANCODES[`Numpad${i}`] = 88 + i;

const PRINTABLE = { 40: 0x0d, 41: 0x1b, 42: 0x08, 43: 0x09, 44: 0x20 };

function keycode(scancode) {
    if (scancode >= 4 && scancode <= 29) return 0x61 + scancode - 4;
    if (scancode >= 30 && scancode <= 38) return 0x31 + scancode - 30;
    if (scancode === 39) return 0x30;
    return PRINTABLE[scancode] ?? ((scancode | 0x40000000) >>> 0);
}

function modifiers(event) {
    return (event.shiftKey ? 0x0001 : 0) | (event.ctrlKey ? 0x0040 : 0) | (event.altKey ? 0x0100 : 0);
}

// ---------------- La prueba de una micro-misión (D126, fase 4): el robot de Arcadia juega solo

// Los nombres de las teclas en la prueba, en castellano o como los dice el navegador (KeyW, ArrowUp…).
const KEY_NAMES = {
    arriba: 'ArrowUp', abajo: 'ArrowDown', izquierda: 'ArrowLeft', derecha: 'ArrowRight',
    espacio: 'Space', enter: 'Enter', escape: 'Escape', esc: 'Escape', tab: 'Tab', borrar: 'Backspace',
    shift: 'ShiftLeft', control: 'ControlLeft', ctrl: 'ControlLeft', alt: 'AltLeft',
};
// Los botones del joystick (mapeo estándar del navegador) y la palanca izquierda.
const PAD_BUTTON_NAMES = { a: 0, b: 1, x: 2, y: 3, lb: 4, rb: 5, back: 8, start: 9, arriba: 12, abajo: 13, izquierda: 14, derecha: 15 };
const STICK = { centro: [0, 0], izquierda: [-1, 0], derecha: [1, 0], arriba: [0, -1], abajo: [0, 1] };

function scancodeOf(name) {
    const lower = name.toLowerCase();
    const code = KEY_NAMES[lower] ?? (/^[a-z]$/.test(lower) ? `Key${lower.toUpperCase()}` : /^[0-9]$/.test(lower) ? `Digit${lower}` : name);
    return SCANCODES[code];
}

/**
 * Lee los «Eventos» de una micro-misión de juego, un renglón por paso, y arma qué le llega al juego en cada cuadro:
 *   cuadros 30 · tecla W (apretar y soltar) · apretar Arriba · soltar Arriba · mouse 100 200 · clic 100 200 ·
 *   boton A · apretar boton A · soltar boton A · palanca izquierda|derecha|arriba|abajo|centro · cerrar
 * Si no hay eventos, el juego corre 30 cuadros. Devuelve { timeline, end, problems }.
 */
export function parseGameTest(text = '') {
    const timeline = [];
    const problems = [];
    let at = 0;
    let usesPad = false;
    const pad = { index: 0, name: 'Joystick de prueba', axes: [0, 0, 0, 0], buttons: Array(17).fill(0) };
    const padMessage = () => ({ type: 'pads', pads: [{ ...pad, axes: [...pad.axes], buttons: [...pad.buttons] }] });
    const key = (scancode, down) => ({ type: 'key', down, scancode, key: keycode(scancode), mod: 0, repeat: false });
    const lines = String(text).split('\n').map((line) => line.trim()).filter((line) => line && !line.startsWith('//'));
    for (const line of lines) {
        const words = line.split(/\s+/);
        const verb = words[0].toLowerCase();
        const wrong = () => problems.push(line);
        if (verb === 'cuadros') {
            const n = Number(words[1]);
            if (!Number.isInteger(n) || n < 1 || n > 3600) wrong();
            else at += n;
        } else if ((verb === 'tecla' || verb === 'apretar' || verb === 'soltar') && words[1]?.toLowerCase() !== 'boton') {
            const scancode = scancodeOf(words[1] ?? '');
            if (!scancode) { wrong(); continue; }
            if (verb !== 'soltar') timeline.push({ at, message: key(scancode, true) });
            if (verb === 'tecla') at++;
            if (verb !== 'apretar') timeline.push({ at, message: key(scancode, false) });
        } else if (verb === 'mouse' || verb === 'clic') {
            const [x, y] = [Number(words[1]), Number(words[2])];
            if (!Number.isFinite(x) || !Number.isFinite(y)) { wrong(); continue; }
            timeline.push({ at, message: { type: 'mouse', kind: 'move', x, y } });
            if (verb === 'clic') {
                timeline.push({ at, message: { type: 'mouse', kind: 'down', button: 1, x, y } });
                at++;
                timeline.push({ at, message: { type: 'mouse', kind: 'up', button: 1, x, y } });
            }
        } else if (verb === 'boton' || verb === 'botón' || ((verb === 'apretar' || verb === 'soltar') && words[1]?.toLowerCase() === 'boton')) {
            const name = (verb === 'boton' || verb === 'botón' ? words[1] : words[2])?.toLowerCase();
            const index = PAD_BUTTON_NAMES[name];
            if (index === undefined) { wrong(); continue; }
            usesPad = true;
            if (verb !== 'soltar') { pad.buttons[index] = 1; timeline.push({ at, message: padMessage() }); }
            if (verb === 'boton' || verb === 'botón') at++;
            if (verb !== 'apretar') { pad.buttons[index] = 0; timeline.push({ at, message: padMessage() }); }
        } else if (verb === 'palanca') {
            const axes = STICK[words[1]?.toLowerCase()];
            if (!axes) { wrong(); continue; }
            usesPad = true;
            [pad.axes[0], pad.axes[1]] = axes;
            timeline.push({ at, message: padMessage() });
        } else if (verb === 'cerrar') {
            timeline.push({ at, message: { type: 'quit' } });
        } else {
            wrong();
        }
    }
    // El joystick de prueba está enchufado desde el principio.
    if (usesPad) timeline.unshift({ at: 0, message: { type: 'pads', pads: [{ index: 0, name: pad.name, axes: [0, 0, 0, 0], buttons: Array(17).fill(0) }] } });
    timeline.sort((a, b) => a.at - b.at);
    const last = timeline.length ? timeline.at(-1).at + 1 : 0;
    return { timeline, end: Math.max(lines.length ? at : 30, last, 1), problems };
}

/** ¿Este navegador puede pausar el bucle del juego? (JSPI: Chrome y Edge desde 2025; Firefox, en camino). */
export function gamesSupported() {
    return typeof WebAssembly.Suspending === 'function' && typeof WebAssembly.promising === 'function'
        && typeof OffscreenCanvas === 'function';
}

/**
 * Compila y arranca el juego dentro de `container` (un lienzo nuevo cada vez).
 *
 * @returns {Promise<{ok: boolean, error?: string, diagnostics?: string, stop?: () => void, done?: Promise<{exit?: number, error?: string}>}>}
 */
export async function runGame(code, { container, onStatus, onOutput, onWindow, storageKey = 'sdl', args = [], watchdog = 3000, test = null } = {}) {
    if (!gamesSupported()) {
        return { ok: false, error: 'Este navegador no puede correr los juegos todavía: abrilo en Chrome o en Edge (actualizados).' };
    }
    // El audio se prende con el clic en Jugar (el navegador no deja sonar sin que la persona toque algo).
    // En la prueba no suena nada ni se usan los récords guardados: arranca siempre igual.
    const audio = test ? { handle() {}, mix() {}, close() {} } : startAudio();
    const plan = test ? parseGameTest(test.events) : null;
    if (plan?.problems.length) return { ok: false, error: `La prueba tiene renglones que no se entienden: ${plan.problems.join(' · ')}` };
    onStatus?.('Compilando…');
    const compiled = await compile(code, 'c', () => onStatus?.('Compilando…'), true);
    if (compiled.type === 'loadFailed') return { ok: false, error: `No se pudo cargar el compilador: ${compiled.message}` };
    if (compiled.type === 'compileError') return { ok: false, error: 'No compila.', diagnostics: compiled.diagnostics };
    const assets = await loadAssets(code);

    container.replaceChildren();
    const canvas = document.createElement('canvas');
    canvas.tabIndex = 0;
    canvas.dataset.test = 'game-canvas';
    canvas.className = 'game-canvas';
    canvas.setAttribute('aria-label', 'La ventana del juego: hacé clic para jugar con el teclado');
    canvas.style.aspectRatio = '4 / 3';
    canvas.style.width = 'min(100%, calc(65vh * 4 / 3))';
    container.append(canvas);
    const offscreen = canvas.transferControlToOffscreen();

    const worker = new Worker(new URL('../workers/sdl-run.worker.js', import.meta.url), { type: 'module' });
    let size = { w: 640, h: 480 };
    let alive = performance.now();
    let finished = false;
    let finish;
    const done = new Promise((resolve) => (finish = resolve));
    const cleanups = [];

    const end = (result) => {
        if (finished) return;
        finished = true;
        worker.terminate();
        audio.close();
        network.drop(worker);
        cleanups.forEach((cleanup) => cleanup());
        finish(result);
    };

    worker.onmessage = ({ data }) => {
        alive = performance.now();
        if (data.type === 'alive' && data.fps !== undefined) window.sdlFps = data.fps; // para las pruebas
        if (data.type === 'window') {
            size = { w: data.w, h: data.h };
            // Lo más grande que entre a lo ancho y en dos tercios del alto de la pantalla, sin deformarse.
            canvas.style.aspectRatio = `${data.w} / ${data.h}`;
            canvas.style.width = `min(100%, calc(65vh * ${data.w / data.h}))`;
            onWindow?.(data);
        } else if (data.type === 'title') {
            onWindow?.({ ...size, title: data.title });
        } else if (data.type === 'audio') {
            audio.handle(data);
        } else if (data.type === 'mix') {
            audio.mix(data);
        } else if (data.type === 'net') {
            network.handle(worker, data);
        } else if (data.type === 'test') {
            end({ test: data.report });
        } else if (data.type === 'files' && !test) {
            saveFiles(storageKey, data.files, onOutput);
        } else if (data.type === 'output') {
            onOutput?.(data.text);
        } else if (data.type === 'exit') {
            end({ exit: data.exit });
        } else if (data.type === 'crash') {
            end({ error: `El juego se cortó: ${data.message}` });
        }
    };
    worker.onerror = (event) => end({ error: `El juego se cortó: ${event.message ?? 'error'}` });

    // El Bucle Eterno: un while que nunca llama a SDL_PollEvent, SDL_Delay ni SDL_RenderPresent cuelga el worker.
    const timer = setInterval(() => {
        if (performance.now() - alive > watchdog) {
            end({ error: `El juego dejó de responder (más de ${watchdog / 1000} segundos sin dibujar ni leer eventos). ¿Hay un bucle que no llama a SDL_PollEvent ni a SDL_RenderPresent?`, hung: true });
        }
    }, 500);
    cleanups.push(() => clearInterval(timer));

    // El teclado, solo con el juego enfocado (para no robarle las teclas al editor).
    const onKey = (event) => {
        if (test) return;
        const scancode = SCANCODES[event.code];
        if (!scancode) return;
        event.preventDefault();
        worker.postMessage({ type: 'key', down: event.type === 'keydown', scancode, key: keycode(scancode), mod: modifiers(event), repeat: event.repeat });
    };
    canvas.addEventListener('keydown', onKey);
    canvas.addEventListener('keyup', onKey);

    const point = (event) => {
        const rect = canvas.getBoundingClientRect();
        return {
            x: Math.round(((event.clientX - rect.left) * size.w) / rect.width),
            y: Math.round(((event.clientY - rect.top) * size.h) / rect.height),
        };
    };
    const onMouse = (event) => {
        if (test) return;
        if (event.type === 'mousedown') canvas.focus();
        const kind = { mousemove: 'move', mousedown: 'down', mouseup: 'up' }[event.type];
        worker.postMessage({ type: 'mouse', kind, button: event.button === 1 ? 2 : event.button === 2 ? 3 : 1, ...point(event) });
    };
    ['mousemove', 'mousedown', 'mouseup'].forEach((type) => canvas.addEventListener(type, onMouse));
    // La rueda: positivo hacia arriba (lejos de la persona), como en SDL3.
    canvas.addEventListener('wheel', (event) => {
        event.preventDefault();
        worker.postMessage({ type: 'mouse', kind: 'wheel', wheelX: Math.sign(event.deltaX), wheelY: -Math.sign(event.deltaY), ...point(event) });
    }, { passive: false });
    canvas.addEventListener('contextmenu', (event) => event.preventDefault());

    // Los joysticks solo se leen desde la página: se mandan cuando cambian.
    let lastPads = '';
    let frame = 0;
    const readPads = () => {
        const pads = [...(navigator.getGamepads?.() ?? [])].filter(Boolean).map((pad) => ({
            index: pad.index,
            name: pad.id.replace(/\s*\(.*$/, '').slice(0, 60) || 'Joystick',
            axes: [...pad.axes].map((value) => (Math.abs(value) < 0.08 ? 0 : value)),
            buttons: pad.buttons.map((button) => button.value),
        }));
        const json = JSON.stringify(pads);
        if (json !== lastPads && !test) {
            lastPads = json;
            worker.postMessage({ type: 'pads', pads });
        }
        frame = requestAnimationFrame(readPads);
    };
    frame = requestAnimationFrame(readPads);
    cleanups.push(() => cancelAnimationFrame(frame));

    // Abajo se ve si las teclas van al juego o no (si el foco quedó en el editor, las teclas escriben ahí).
    const focusStatus = () => !finished && !test && onStatus?.(document.activeElement === canvas
        ? '🎮 El teclado está en el juego (ESC vuelve al menú)'
        : 'Hacé clic en el juego para usar el teclado');
    canvas.addEventListener('focus', focusStatus);
    canvas.addEventListener('blur', focusStatus);
    worker.postMessage({
        type: 'start', wasm: compiled.wasm, canvas: offscreen, files: test ? {} : loadFiles(storageKey), assets, args,
        test: plan ? { timeline: plan.timeline, end: plan.end, checks: test.checks ?? [] } : null,
        display: { w: screen.width, h: screen.height, density: devicePixelRatio || 1 },
    }, [offscreen]);
    canvas.focus();
    focusStatus();

    return {
        ok: true,
        diagnostics: compiled.diagnostics,
        canvas,
        done,
        // Cerrar la ventana: el juego recibe SDL_EVENT_QUIT y, si no termina solo, se corta.
        stop() {
            if (finished) return;
            worker.postMessage({ type: 'quit' });
            setTimeout(() => end({ exit: 0, stopped: true }), 1500);
        },
        kill() {
            end({ exit: 0, stopped: true });
        },
    };
}

/**
 * El audio del juego (SDL_AudioStream): el worker manda las muestras y acá se ponen en fila, una detrás de la otra,
 * con el audio del navegador. Cada stream tiene su volumen y arranca en pausa, como en SDL3.
 */
function startAudio() {
    const Context = window.AudioContext ?? window.webkitAudioContext;
    const context = Context ? new Context() : null;
    context?.resume?.().catch(() => {});
    const streams = new Map();

    const schedule = (stream, samples) => {
        const frames = Math.floor(samples.length / stream.channels);
        if (!frames) return;
        const buffer = context.createBuffer(stream.channels, frames, stream.freq);
        for (let c = 0; c < stream.channels; c++) {
            const channel = buffer.getChannelData(c);
            for (let i = 0; i < frames; i++) channel[i] = samples[i * stream.channels + c];
        }
        const source = context.createBufferSource();
        source.buffer = buffer;
        source.connect(stream.gain);
        const at = Math.max(context.currentTime + 0.01, stream.end);
        source.start(at);
        stream.end = at + buffer.duration;
        stream.sources.add(source);
        source.onended = () => stream.sources.delete(source);
    };
    const stop = (stream) => {
        stream.sources.forEach((source) => { try { source.stop(); } catch { /* ya terminó */ } });
        stream.sources.clear();
        stream.pending = [];
        stream.end = 0;
    };

    // SDL3_mixer: los audios (ya decodificados), los mixers (un volumen general) y las pistas.
    const mixers = new Map(); // id → GainNode
    const sounds = new Map(); // id → AudioBuffer o Promise<AudioBuffer>
    const tracks = new Map(); // id → { mixer, audio, gain, source, loops, started, offset }
    const buffer = (channels, freq, samples) => {
        const frames = Math.max(1, Math.floor(samples.length / channels));
        const out = context.createBuffer(channels, frames, freq);
        for (let c = 0; c < channels; c++) {
            const channel = out.getChannelData(c);
            for (let i = 0; i < frames; i++) channel[i] = samples[i * channels + c] ?? 0;
        }
        return out;
    };
    const play = async (track, offset = 0) => {
        window.sdlAudioChunks = (window.sdlAudioChunks ?? 0) + 1; // para las pruebas
        const sound = await sounds.get(track.audio);
        if (!sound || tracks.get(track.id) !== track) return;
        track.source?.stop?.();
        const source = context.createBufferSource();
        source.buffer = sound;
        source.loop = track.loops !== 0;
        source.connect(track.gain);
        source.start(0, offset % sound.duration);
        track.started = context.currentTime - (offset % sound.duration);
        track.source = source;
        if (track.loops > 0) setTimeout(() => { if (track.source === source) source.loop = false; }, (sound.duration * (track.loops + 1) - offset) * 1000 - 50);
    };
    const halt = (track) => {
        try { track.source?.stop(); } catch { /* ya terminó */ }
        track.source = null;
    };

    return {
        handle({ action, id, channels, freq, samples, value }) {
            if (!context) return;
            if (action === 'open') {
                const gain = context.createGain();
                gain.connect(context.destination);
                streams.set(id, { channels, freq, gain, paused: true, pending: [], end: 0, sources: new Set() });
                return;
            }
            const stream = streams.get(id);
            if (!stream) return;
            if (action === 'put') {
                window.sdlAudioChunks = (window.sdlAudioChunks ?? 0) + 1; // para las pruebas: cuánto sonido llegó
                if (stream.paused) stream.pending.push(samples);
                else schedule(stream, samples);
            } else if (action === 'resume') {
                stream.paused = false;
                stream.pending.splice(0).forEach((chunk) => schedule(stream, chunk));
            } else if (action === 'pause') {
                stop(stream);
                stream.paused = true;
            } else if (action === 'clear') {
                stop(stream);
            } else if (action === 'gain') {
                stream.gain.gain.value = value;
            } else if (action === 'destroy') {
                stop(stream);
                stream.gain.disconnect();
                streams.delete(id);
            }
        },
        mix({ action, id, arg, value, channels, freq, samples, data, mixer }) {
            if (!context) return;
            if (action === 'mixer') {
                const gain = context.createGain();
                gain.connect(context.destination);
                mixers.set(id, gain);
            } else if (action === 'pcm') {
                sounds.set(id, buffer(channels, freq, samples));
            } else if (action === 'encoded') {
                sounds.set(id, context.decodeAudioData(data.buffer.slice(0)).catch(() => null));
            } else if (action === 'track') {
                const gain = context.createGain();
                gain.connect(mixers.get(mixer) ?? context.destination);
                tracks.set(id, { id, mixer, audio: 0, gain, source: null, loops: 0, started: 0, offset: 0 });
            } else if (action === 'fire') {
                window.sdlAudioChunks = (window.sdlAudioChunks ?? 0) + 1; // para las pruebas
                // Disparar y olvidar: suena una vez, encima de lo que haya.
                Promise.resolve(sounds.get(arg)).then((sound) => {
                    if (!sound) return;
                    const source = context.createBufferSource();
                    source.buffer = sound;
                    source.connect(mixers.get(id) ?? context.destination);
                    source.start();
                });
            } else if (action === 'master') {
                const gain = mixers.get(id);
                if (gain) gain.gain.value = value;
            } else if (action === 'free-audio') {
                sounds.delete(id);
            } else if (action === 'free-mixer') {
                mixers.get(id)?.disconnect();
                mixers.delete(id);
            } else {
                const track = tracks.get(id);
                if (!track) return;
                if (action === 'set') track.audio = arg;
                else if (action === 'play') { track.loops = arg; play(track); }
                else if (action === 'pause') { track.offset = track.source ? context.currentTime - track.started : 0; halt(track); }
                else if (action === 'resume') play(track, track.offset);
                else if (action === 'stop') halt(track);
                else if (action === 'gain') track.gain.gain.value = value;
                else if (action === 'free-track') { halt(track); track.gain.disconnect(); tracks.delete(id); }
            }
        },
        close() {
            tracks.forEach(halt);
            streams.forEach(stop);
            context?.close?.().catch(() => {});
        },
    };
}

// La carpeta prefs/ del juego (récords, opciones) queda en el navegador de cada uno: hasta 512 KB.
const FILES_LIMIT = 512 * 1024;

function loadFiles(key) {
    try {
        const saved = JSON.parse(localStorage.getItem(`${key}:archivos`) ?? '{}');
        return Object.fromEntries(Object.entries(saved).map(([path, base64]) => [path, Uint8Array.from(atob(base64), (c) => c.charCodeAt(0))]));
    } catch {
        return {};
    }
}

function saveFiles(key, files, onOutput) {
    let size = 0;
    const encoded = {};
    for (const [path, data] of Object.entries(files)) {
        size += data.length;
        let text = '';
        for (let i = 0; i < data.length; i += 0x8000) text += String.fromCharCode(...data.subarray(i, i + 0x8000));
        encoded[path] = btoa(text);
    }
    if (size > FILES_LIMIT) {
        onOutput?.(`\n(Los archivos del juego pasan de ${FILES_LIMIT / 1024} KB: no se guardan en el navegador.)\n`);
        return;
    }
    try {
        localStorage.setItem(`${key}:archivos`, JSON.stringify(encoded));
    } catch {
        /* sin lugar o sin permiso: el juego sigue igual */
    }
}

/**
 * La red de mentira (SDL3_net en la página): un «conmutador» que conecta los juegos abiertos en esta página por número
 * de puerto. No sale nada a internet: los bytes van de un worker a otro (o al mismo, si es «localhost»).
 */
const network = {
    servers: new Map(), // puerto → { worker, server }
    conns: new Map(), // id → { a: { worker, sock }, b: { worker, sock } }
    seq: 0,
    handle(worker, { op, port, server, sock, conn, data }) {
        if (op === 'listen') {
            if (!this.servers.has(port)) this.servers.set(port, { worker, server });
        } else if (op === 'unlisten') {
            if (this.servers.get(port)?.server === server && this.servers.get(port)?.worker === worker) this.servers.delete(port);
        } else if (op === 'connect') {
            const target = this.servers.get(port);
            if (!target) return worker.postMessage({ type: 'net', op: 'refused', sock });
            const id = ++this.seq;
            this.conns.set(id, { a: { worker, sock }, b: { worker: target.worker, sock: 0 } });
            target.worker.postMessage({ type: 'net', op: 'incoming', server: target.server, conn: id });
        } else if (op === 'accepted') {
            const link = this.conns.get(conn);
            if (!link) return;
            link.b.sock = sock;
            link.a.worker.postMessage({ type: 'net', op: 'connected', sock: link.a.sock, conn });
        } else if (op === 'data' || op === 'close') {
            const link = this.conns.get(conn);
            if (!link) return;
            const other = link.a.worker === worker && link.a.sock === sock ? link.b : link.a;
            if (op === 'data') other.worker.postMessage({ type: 'net', op: 'data', sock: other.sock, data }, [data.buffer]);
            else {
                other.worker.postMessage({ type: 'net', op: 'closed', sock: other.sock });
                this.conns.delete(conn);
            }
        }
    },
    /** Un juego que se cerró: sus servidores se apagan y a quien estaba conectado le llega el cierre. */
    drop(worker) {
        for (const [port, entry] of this.servers) if (entry.worker === worker) this.servers.delete(port);
        for (const [id, link] of this.conns) {
            if (link.a.worker !== worker && link.b.worker !== worker) continue;
            const other = link.a.worker === worker ? link.b : link.a;
            if (other.worker !== worker) other.worker.postMessage({ type: 'net', op: 'closed', sock: other.sock });
            this.conns.delete(id);
        }
    },
};

// Lo que trae la plataforma para los juegos (se lee como un archivo más: TTF_OpenFont("assets/fonts/DejaVuSans.ttf")).
const GAME_ASSETS = { 'assets/fonts/DejaVuSans.ttf': '/games/assets/fonts/DejaVuSans.ttf' };

async function loadAssets(code) {
    const wanted = Object.entries(GAME_ASSETS).filter(([path]) => code.includes(path.split('/').pop()));
    const loaded = await Promise.all(wanted.map(async ([path, url]) => {
        try {
            const response = await fetch(url);
            return response.ok ? [path, new Uint8Array(await response.arrayBuffer())] : null;
        } catch {
            return null;
        }
    }));
    return Object.fromEntries(loaded.filter(Boolean));
}
