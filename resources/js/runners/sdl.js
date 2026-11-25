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
export async function runGame(code, { container, onStatus, onOutput, onWindow, watchdog = 3000 } = {}) {
    if (!gamesSupported()) {
        return { ok: false, error: 'Este navegador no puede correr los juegos todavía: abrilo en Chrome o en Edge (actualizados).' };
    }
    onStatus?.('Compilando…');
    const compiled = await compile(code, 'c', () => onStatus?.('Compilando…'), true);
    if (compiled.type === 'loadFailed') return { ok: false, error: `No se pudo cargar el compilador: ${compiled.message}` };
    if (compiled.type === 'compileError') return { ok: false, error: 'No compila.', diagnostics: compiled.diagnostics };

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
        cleanups.forEach((cleanup) => cleanup());
        finish(result);
    };

    worker.onmessage = ({ data }) => {
        alive = performance.now();
        if (data.type === 'window') {
            size = { w: data.w, h: data.h };
            // Lo más grande que entre a lo ancho y en dos tercios del alto de la pantalla, sin deformarse.
            canvas.style.aspectRatio = `${data.w} / ${data.h}`;
            canvas.style.width = `min(100%, calc(65vh * ${data.w / data.h}))`;
            onWindow?.(data);
        } else if (data.type === 'title') {
            onWindow?.({ ...size, title: data.title });
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
        if (event.type === 'mousedown') canvas.focus();
        const kind = { mousemove: 'move', mousedown: 'down', mouseup: 'up' }[event.type];
        worker.postMessage({ type: 'mouse', kind, button: event.button === 1 ? 2 : event.button === 2 ? 3 : 1, ...point(event) });
    };
    ['mousemove', 'mousedown', 'mouseup'].forEach((type) => canvas.addEventListener(type, onMouse));
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
        if (json !== lastPads) {
            lastPads = json;
            worker.postMessage({ type: 'pads', pads });
        }
        frame = requestAnimationFrame(readPads);
    };
    frame = requestAnimationFrame(readPads);
    cleanups.push(() => cancelAnimationFrame(frame));

    onStatus?.('Jugando: hacé clic en el juego para usar el teclado');
    worker.postMessage({ type: 'start', wasm: compiled.wasm, canvas: offscreen }, [offscreen]);
    canvas.focus();

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
