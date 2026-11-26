// El SDL3 de la plataforma (D126): corre un juego en C compilado en el navegador (Clang, D98) y resuelve lo de SDL3
// (resources/js/runners/sdl3/SDL.h) dibujando en un lienzo. Vive en su propio worker: no ve la página ni la sesión,
// y si se cuelga se lo corta. El bucle del juego (`while (jugando)`) se pausa en SDL_Delay y SDL_RenderPresent
// con JSPI (WebAssembly.Suspending): mientras tanto el navegador dibuja y llegan el teclado y el joystick.
import { WASI, File, Directory, OpenFile, ConsoleStdout, PreopenDirectory, WASIProcExit } from '@bjorn3/browser_wasi_shim';
import { glyphOf } from '../runners/sdl3/font8x8.js';

const EVENT = {
    QUIT: 0x100, KEY_DOWN: 0x300, KEY_UP: 0x301,
    MOUSE_MOTION: 0x400, MOUSE_BUTTON_DOWN: 0x401, MOUSE_BUTTON_UP: 0x402, MOUSE_WHEEL: 0x403,
    PAD_AXIS: 0x650, PAD_BUTTON_DOWN: 0x651, PAD_BUTTON_UP: 0x652, PAD_ADDED: 0x653, PAD_REMOVED: 0x654,
};
// Los botones del «mapeo estándar» del navegador, en el orden de SDL_GamepadButton.
const PAD_BUTTONS = [0, 1, 2, 3, 8, 16, 9, 10, 11, 4, 5, 12, 13, 14, 15];

let memory = null;
let screen = null; // el lienzo de la página (OffscreenCanvas)
let back = null; // donde se dibuja hasta SDL_RenderPresent (como el «buffer de atrás» de SDL)
let ctx = null;
let size = { w: 0, h: 0 };
let color = [0, 0, 0, 255];
let blend = 0;
let scale = [1, 1];
let keysPointer = 0;
let keyCount = 0;
let started = 0;
let lastYield = 0;
let lastAlive = 0;
let vsync = 0;
let lastFrame = 0; // cuándo se presentó el último cuadro (para el VSync)
let frames = 0; // cuadros presentados desde el último aviso (los cuadros por segundo, para las pruebas)
const queue = [];
const mouse = { x: 0, y: 0, buttons: 0 };
const pads = new Map(); // id → { name, axes[], buttons[] }
const glyphs = new Map();
let exports = null; // lo que exporta el juego: la memoria, la tabla de funciones y la pila (__stack_pointer)
let display = { w: 1920, h: 1080, density: 1 };
let files = null; // la carpeta del juego (WASI), para guardar prefs/ en el navegador
let filesTimer = 0;

// Los hilos emulados (SDL_CreateThread): cada uno es otra «pila» de JSPI sobre la misma memoria, con su propio pedazo
// de pila de C. Se turnan en cada pausa; `fiber` dice quién corre (0 = el juego) y cada pausa repone su pila al volver.
let fiber = 0;
let threadSeq = 0;
const threads = new Map(); // id → { done, result, promise }
const timers = new Map(); // id → { callback, userdata, interval, handle }
let timerSeq = 0;
const mutexes = new Map(); // puntero → { owner, depth }
const streams = new Map(); // id → { format, channels, freq, paused, pendingMs, playEnd, callback, userdata }
let streamSeq = 0;
const textures = new Map(); // id → { canvas, ctx, w, h, smooth, alpha, tint, tinted }
let textureSeq = 0;
let target = 0; // 0 = la ventana; si no, la textura donde se dibuja (SDL_SetRenderTarget)
const blobs = new Map(); // datos que esperan que C los copie a su memoria (imágenes decodificadas, PNG, texto)
let blobSeq = 0;
const fonts = new Map(); // id → nombre de la fuente cargada en el worker
let fontSeq = 0;
// SDL3_mixer: los audios y las pistas los reproduce la página; acá se lleva la cuenta de qué suena.
const mixAudios = new Map(); // id → { ms }
const mixTracks = new Map(); // id → { audio, playingUntil, paused }
let mixSeq = 0;
// SDL3_net, la red de mentira: la página conecta los juegos por número de puerto.
const netServers = new Map(); // id → { port, pending: [socket ids] }
const netSockets = new Map(); // id → { status, conn, inbox: [Uint8Array], closed, waiters: [] }
let netSeq = 0;

// La prueba de una micro-misión (D126, fase 4): el «robot de Arcadia» juega solo. Con un reloj de mentira (cada cuadro
// con VSync son 16,7 ms y SDL_Delay suma lo que pide, sin esperar de verdad) y el azar con semilla fija, el mismo
// código da siempre el mismo resultado. Las teclas llegan en el cuadro que dice la prueba; al final se arma el informe.
let test = null; // { timeline: [{ at, message }], end, checks: [renglones] }
let testFrame = 0;
let virtualMs = 0;
let seed = 0;
let windowTitle = '';
let frameTexts = []; // lo escrito con SDL_RenderDebugText en el cuadro que se está dibujando
let shownTexts = []; // … y en el último cuadro presentado
let soundUsed = false;

const bytes = () => new Uint8Array(memory.buffer);
const view = () => new DataView(memory.buffer);
const string = (pointer) => {
    const all = bytes();
    let end = pointer;
    while (all[end]) end++;
    return new TextDecoder().decode(all.subarray(pointer, end));
};
const post = (message) => self.postMessage(message);
const fill = () => `rgba(${color[0]},${color[1]},${color[2]},${blend === 0 ? 1 : color[3] / 255})`;

/** Cede el control al navegador: dibuja lo presentado y deja entrar el teclado y el joystick. */
function pause(ms) {
    const now = performance.now();
    // Que la página sepa que el juego sigue vivo (sin mandarle un mensaje por cuadro).
    if (now - lastAlive > 1000) {
        post({ type: 'alive', fps: Math.round((frames * 1000) / (now - lastAlive)) });
        lastAlive = now;
        frames = 0;
    }
    lastYield = now;
    feedAudio();
    // Ceder sin esperar: un mensaje a uno mismo no tiene el mínimo de 4 ms de setTimeout (si no, SDL_Delay(16) daría
    // unos 47 cuadros por segundo en vez de 60).
    if (ms <= 0) return new Promise((resolve) => { const channel = new MessageChannel(); channel.port1.onmessage = () => resolve(); channel.port2.postMessage(0); });
    return new Promise((resolve) => setTimeout(resolve, ms));
}

const getSP = () => exports.__stack_pointer.value;
const setSP = (value) => { exports.__stack_pointer.value = value; };
const fn = (pointer) => exports.__indirect_function_table.get(pointer);

/**
 * Una función de SDL que puede pausar al que la llama (el juego o un hilo). Si devuelve una promesa, al volver repone
 * la pila y el hilo del que se pausó: mientras tanto pudo correr otro.
 */
const suspending = (body) => new WebAssembly.Suspending((...args) => {
    const result = body(...args);
    if (!(result instanceof Promise)) return result;
    const mine = { sp: getSP(), fiber };
    return result.then((value) => {
        setSP(mine.sp);
        fiber = mine.fiber;
        return value;
    });
});

/** El azar de la prueba: siempre la misma serie (mulberry32). */
function seededRandom() {
    seed = (seed + 0x6d2b79f5) | 0;
    let t = seed;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}

/** Lo que le toca al cuadro que se acaba de presentar en la prueba: las teclas que siguen, o el informe si terminó. */
function testFrameDone() {
    virtualMs += vsync ? 1000 / 60 : 1;
    testFrame++;
    deliverTest();
    if (testFrame >= test.end) {
        post({ type: 'test', report: testReport(false) });
        return new Promise(() => {}); // el juego queda quieto: la página lo corta
    }
    return pause(0);
}

/** Entrega las teclas, el mouse y el joystick de la prueba que tocan hasta este cuadro. */
function deliverTest() {
    while (test.timeline.length && test.timeline[0].at <= testFrame) receive(test.timeline.shift().message);
}

const hex = (r, g, b) => '#' + [r, g, b].map((v) => v.toString(16).padStart(2, '0')).join('');

/**
 * El informe de la prueba, un renglón por pedido de «Estado» (lo mismo arma la solución al escribir la salida esperada):
 * ventana · pixel X Y · buscar #rrggbb · textos · sonido · terminó.
 */
function testReport(exited, exit = 0) {
    let image = null;
    const pixels = () => {
        if (!image) image = screen.getContext('2d').getImageData(0, 0, screen.width, screen.height);
        return image;
    };
    return test.checks.map((line) => {
        const words = line.trim().split(/\s+/);
        const what = words[0].toLowerCase();
        if (what === 'ventana') return size.w ? `ventana: «${windowTitle}» ${size.w}x${size.h}` : 'ventana: no se abrió';
        if (what === 'pixel') {
            const x = Number(words[1]);
            const y = Number(words[2]);
            if (!size.w) return `pixel ${x} ${y}: no hay ventana`;
            if (!(x >= 0 && y >= 0 && x < screen.width && y < screen.height)) return `pixel ${x} ${y}: afuera de la ventana`;
            const { data, width } = pixels();
            const i = (y * width + x) * 4;
            return `pixel ${x} ${y}: ${hex(data[i], data[i + 1], data[i + 2])}`;
        }
        if (what === 'buscar') {
            const wanted = (words[1] ?? '').toLowerCase();
            if (!size.w) return `buscar ${wanted}: no hay ventana`;
            const { data, width, height } = pixels();
            let x1 = Infinity, y1 = Infinity, x2 = -1, y2 = -1;
            for (let y = 0; y < height; y++) {
                for (let x = 0; x < width; x++) {
                    const i = (y * width + x) * 4;
                    if (hex(data[i], data[i + 1], data[i + 2]) !== wanted) continue;
                    x1 = Math.min(x1, x); y1 = Math.min(y1, y); x2 = Math.max(x2, x); y2 = Math.max(y2, y);
                }
            }
            return x2 < 0 ? `buscar ${wanted}: no está` : `buscar ${wanted}: x ${x1}, y ${y1}, ancho ${x2 - x1 + 1}, alto ${y2 - y1 + 1}`;
        }
        if (what === 'textos') return `textos: ${shownTexts.filter(Boolean).join(' | ') || '(ninguno)'}`;
        if (what === 'sonido') return `sonido: ${soundUsed ? 'sí' : 'no'}`;
        if (what === 'terminó' || what === 'termino') return `terminó: ${exited ? `sí (devolvió ${exit})` : 'no'}`;
        return `${line.trim()}: no se entiende`;
    });
}

/** Guarda bytes para que C los copie (sdlw_blob_copy) cuando ya reservó la memoria. */
function keepBlob(data) {
    const id = ++blobSeq;
    blobs.set(id, data);
    return id;
}

/** Los píxeles del juego (32 bits, en el formato que diga) a RGBA, como los entiende el lienzo. */
function toRGBA(pointer, w, h, pitch, format) {
    const src = bytes();
    const out = new Uint8ClampedArray(w * h * 4);
    // Dónde está cada canal dentro del píxel (en memoria, de a bytes), según SDL_PixelFormat.
    const order = {
        0x16362004: [2, 1, 0, 3], 0x16161804: [2, 1, 0, -1], 0x16462004: [3, 2, 1, 0], 0x16862004: [1, 2, 3, 0],
    }[format] ?? [0, 1, 2, 3];
    for (let y = 0; y < h; y++) {
        let from = pointer + y * pitch;
        let to = y * w * 4;
        for (let x = 0; x < w; x++, from += 4, to += 4) {
            out[to] = src[from + order[0]];
            out[to + 1] = src[from + order[1]];
            out[to + 2] = src[from + order[2]];
            out[to + 3] = order[3] < 0 ? 255 : src[from + order[3]];
        }
    }
    return out;
}

/** Una textura con color (SDL_SetTextureColorMod): se tiñe una copia una vez y se guarda. */
function tinted(texture) {
    if (texture.tint === 0xffffff) return texture.canvas;
    if (texture.tinted?.key === texture.tint && texture.tinted.version === texture.version) return texture.tinted.canvas;
    const canvas = new OffscreenCanvas(texture.w, texture.h);
    const c = canvas.getContext('2d');
    c.drawImage(texture.canvas, 0, 0);
    c.globalCompositeOperation = 'multiply';
    c.fillStyle = `#${texture.tint.toString(16).padStart(6, '0')}`;
    c.fillRect(0, 0, texture.w, texture.h);
    c.globalCompositeOperation = 'destination-in';
    c.drawImage(texture.canvas, 0, 0);
    texture.tinted = { key: texture.tint, version: texture.version, canvas };
    return canvas;
}

function fontCss(id, size, style) {
    return `${style & 2 ? 'italic ' : ''}${style & 1 ? 'bold ' : ''}${Math.max(1, size)}px "${fonts.get(id)}"`;
}

function textBox(c, text) {
    const metrics = c.measureText(text);
    const ascent = Math.ceil(metrics.fontBoundingBoxAscent ?? metrics.actualBoundingBoxAscent);
    const descent = Math.ceil(metrics.fontBoundingBoxDescent ?? metrics.actualBoundingBoxDescent);
    return { w: Math.max(1, Math.ceil(metrics.width)), h: Math.max(1, ascent + descent), ascent };
}

function netSend(message) {
    post({ type: 'net', ...message });
}

function crash(error) {
    post({ type: 'crash', message: String(error?.message ?? error) });
}

function glyph(code) {
    if (!glyphs.has(code)) {
        const rows = glyphOf(code);
        const image = rows && new ImageData(8, 8);
        for (let y = 0; rows && y < 8; y++) {
            for (let x = 0; x < 8; x++) {
                if (rows[y] & (1 << x)) image.data.set([255, 255, 255, 255], (y * 8 + x) * 4);
            }
        }
        glyphs.set(code, image);
    }
    return glyphs.get(code);
}

// Cada letra, ya pintada de un color, se guarda: el texto de cada cuadro se arma copiando (rápido).
const painted = new Map(); // `${código}|${color}` → lienzo de 8 x 8

function paintedGlyph(code, color) {
    const key = `${code}|${color}`;
    let tile = painted.get(key);
    if (tile === undefined) {
        const image = glyph(code);
        tile = null;
        if (image) {
            tile = new OffscreenCanvas(8, 8);
            const c = tile.getContext('2d');
            c.putImageData(image, 0, 0);
            c.globalCompositeOperation = 'source-in';
            c.fillStyle = color;
            c.fillRect(0, 0, 8, 8);
        }
        if (painted.size > 4000) painted.clear();
        painted.set(key, tile);
    }
    return tile;
}

/** Texto de 8 x 8 píxeles como SDL_RenderDebugText, del color de dibujo. */
function drawText(x, y, text) {
    const color = fill();
    let cx = x;
    for (const char of text) {
        const tile = paintedGlyph(char.codePointAt(0), color);
        if (tile) ctx.drawImage(tile, cx, y);
        cx += 8;
    }
}

const sdl = {
    init(flags, keys, count) {
        keysPointer = keys;
        keyCount = count;
        return 1;
    },
    quit() {},
    create_window(title, w, h) {
        size = { w: Math.max(1, Math.min(w, 1920)), h: Math.max(1, Math.min(h, 1080)) };
        screen.width = size.w;
        screen.height = size.h;
        back = new OffscreenCanvas(size.w, size.h);
        ctx = back.getContext('2d');
        ctx.imageSmoothingEnabled = false;
        target = 0;
        windowTitle = string(title);
        post({ type: 'window', title: windowTitle, w: size.w, h: size.h });
        return 1;
    },
    set_title(title) {
        windowTitle = string(title);
        post({ type: 'title', title: string(title) });
        return 1;
    },
    create_renderer() {
        return ctx ? 1 : 0;
    },
    set_color(r, g, b, a) {
        color = [r, g, b, a];
        return 1;
    },
    get_color(pointer) {
        bytes().set(color, pointer);
    },
    set_blend(mode) {
        blend = mode;
        ctx.globalCompositeOperation = mode === 2 ? 'lighter' : 'source-over';
        return 1;
    },
    set_scale(x, y) {
        scale = [x, y];
        ctx.setTransform(x, 0, 0, y, 0, 0);
        return 1;
    },
    clear() {
        ctx.save();
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.globalCompositeOperation = 'copy';
        ctx.fillStyle = `rgba(${color[0]},${color[1]},${color[2]},${color[3] / 255})`;
        ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        ctx.restore();
        return 1;
    },
    rect(pointer, filled) {
        const v = view();
        const [x, y, w, h] = pointer
            ? [v.getFloat32(pointer, true), v.getFloat32(pointer + 4, true), v.getFloat32(pointer + 8, true), v.getFloat32(pointer + 12, true)]
            : [0, 0, size.w / scale[0], size.h / scale[1]];
        if (filled) {
            ctx.fillStyle = fill();
            ctx.fillRect(x, y, w, h);
        } else {
            ctx.strokeStyle = fill();
            ctx.lineWidth = 1;
            ctx.strokeRect(x + 0.5, y + 0.5, Math.max(0, w - 1), Math.max(0, h - 1));
        }
        return 1;
    },
    line(x1, y1, x2, y2) {
        ctx.strokeStyle = fill();
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(Math.floor(x1) + 0.5, Math.floor(y1) + 0.5);
        ctx.lineTo(Math.floor(x2) + 0.5, Math.floor(y2) + 0.5);
        ctx.stroke();
        return 1;
    },
    point(x, y) {
        ctx.fillStyle = fill();
        ctx.fillRect(Math.floor(x), Math.floor(y), 1, 1);
        return 1;
    },
    text(x, y, pointer) {
        if (!target) frameTexts.push(string(pointer).trim());
        drawText(x, y, string(pointer));
        return 1;
    },
    present: suspending(async () => {
        if (back) {
            const screenCtx = screen.getContext('2d');
            screenCtx.globalCompositeOperation = 'copy';
            screenCtx.drawImage(back, 0, 0);
        }
        frames++;
        shownTexts = frameTexts;
        frameTexts = [];
        if (test) return testFrameDone();
        // Con VSync, se espera hasta el próximo cuadro (60 por segundo); sin VSync, solo se cede un momento.
        const wait = vsync ? Math.max(0, lastFrame + 1000 / 60 - performance.now()) : 0;
        await pause(wait);
        lastFrame = performance.now();
        return 1;
    }),
    delay: suspending(async (ms) => {
        if (test) {
            virtualMs += ms >>> 0;
            return pause(0);
        }
        await pause(Math.min(ms >>> 0, 1000));
    }),
    set_vsync(value) {
        vsync = value ? 1 : 0;
        return 1;
    },
    get_vsync() {
        return vsync;
    },
    ticks() {
        if (test) return virtualMs;
        return performance.now() - started;
    },
    // Si el bucle no se pausa nunca, igual se cede de vez en cuando (si no, la página no le puede mandar teclas).
    poll: suspending((pointer, raw) => {
        const next = queue.shift();
        if (next) {
            const v = view();
            if (next.raw) {
                bytes().set(next.raw, raw);
                v.setInt32(pointer + 20, 1, true);
                return next.type;
            }
            next.data.forEach((value, i) => v.setInt32(pointer + i * 4, value | 0, true));
            return next.type;
        }
        if (performance.now() - lastYield > 200) return pause(0).then(() => 0);
        return 0;
    }),
    mouse(x, y) {
        const v = view();
        if (x) v.setFloat32(x, mouse.x, true);
        if (y) v.setFloat32(y, mouse.y, true);
        return mouse.buttons;
    },
    gamepads(pointer, max) {
        const ids = [...pads.keys()];
        if (pointer) ids.slice(0, max).forEach((id, i) => view().setUint32(pointer + i * 4, id, true));
        return ids.length;
    },
    gamepad_axis(id, axis) {
        const pad = pads.get(id);
        if (axis === -1) return pad ? 1 : 0;
        if (!pad) return 0;
        // Los gatillos van de 0 a 32767 (en la web son los botones 6 y 7).
        if (axis === 4 || axis === 5) return Math.round((pad.buttons[axis + 2] ?? 0) * 32767);
        const value = pad.axes[axis] ?? 0;
        return Math.max(-32768, Math.min(32767, Math.round(value * 32767)));
    },
    gamepad_button(id, button) {
        const pad = pads.get(id);
        return pad && (pad.buttons[PAD_BUTTONS[button]] ?? 0) > 0.5 ? 1 : 0;
    },
    gamepad_name(id, pointer, max) {
        const pad = pads.get(id);
        if (!pad) return 0;
        const text = new TextEncoder().encode(pad.name).slice(0, max - 1);
        bytes().set([...text, 0], pointer);
        return 1;
    },
    random() {
        if (test) return seededRandom();
        return Math.random();
    },
    log(pointer) {
        post({ type: 'output', text: string(pointer) + '\n' });
    },
    push_event(pointer) {
        const raw = bytes().slice(pointer, pointer + 128);
        queue.push({ type: new DataView(raw.buffer).getUint32(0, true), raw });
        return 1;
    },
    display(w, h, density) {
        const v = view();
        v.setInt32(w, display.w, true);
        v.setInt32(h, display.h, true);
        v.setFloat32(density, display.density, true);
    },

    // ---------- Audio: el juego arma las muestras; la página las reproduce (el worker no tiene audio)
    audio_open(format, channels, freq, callback, userdata) {
        if (channels < 1 || channels > 8 || freq < 1000 || freq > 192000) return 0;
        const id = ++streamSeq;
        streams.set(id, { format, channels, freq, paused: true, pendingMs: 0, playEnd: 0, callback, userdata });
        post({ type: 'audio', action: 'open', id, channels, freq });
        return id;
    },
    audio_put(id, pointer, length) {
        const stream = streams.get(id);
        if (!stream || length <= 0) return stream ? 1 : 0;
        const samples = toFloat(stream.format, pointer, length);
        const ms = (samples.length / stream.channels / stream.freq) * 1000;
        const now = performance.now();
        soundUsed = true;
        if (stream.paused) stream.pendingMs += ms;
        else stream.playEnd = Math.max(now, stream.playEnd) + ms;
        post({ type: 'audio', action: 'put', id, samples }, [samples.buffer]);
        return 1;
    },
    audio_queued(id) {
        const stream = streams.get(id);
        if (!stream) return -1;
        const ms = stream.paused ? stream.pendingMs : Math.max(0, stream.playEnd - performance.now());
        return Math.round((ms / 1000) * stream.freq) * stream.channels * bytesPerSample(stream.format);
    },
    audio_control(id, action, value) {
        const stream = streams.get(id);
        if (!stream) return 0;
        const now = performance.now();
        if (action === 1 && stream.paused) {
            stream.paused = false;
            stream.playEnd = now + stream.pendingMs;
            stream.pendingMs = 0;
        } else if (action === 2 && !stream.paused) {
            stream.paused = true;
            stream.pendingMs = 0;
        } else if (action === 3) {
            stream.pendingMs = 0;
            stream.playEnd = now;
        } else if (action === 4) {
            streams.delete(id);
        }
        post({ type: 'audio', action: ['', 'resume', 'pause', 'clear', 'destroy', 'gain'][action], id, value });
        return 1;
    },

    // ---------- Texturas (SDL_Texture): cada una es un lienzo chico
    tex_create(w, h) {
        if (w < 1 || h < 1 || w > 8192 || h > 8192) return 0;
        const canvas = new OffscreenCanvas(w, h);
        const id = ++textureSeq;
        textures.set(id, { canvas, ctx: canvas.getContext('2d'), w, h, smooth: true, alpha: 255, tint: 0xffffff, version: 0, tinted: null });
        return id;
    },
    tex_update(id, x, y, w, h, pixels, pitch, format) {
        const texture = textures.get(id);
        if (!texture || w < 1 || h < 1) return 0;
        texture.ctx.putImageData(new ImageData(toRGBA(pixels, w, h, pitch, format), w, h), x, y);
        texture.version++;
        return 1;
    },
    tex_draw(id, src, dst, angle, center, flip) {
        const texture = textures.get(id);
        if (!texture) return 0;
        const v = view();
        const rect = (p, w, h) => (p ? [v.getFloat32(p, true), v.getFloat32(p + 4, true), v.getFloat32(p + 8, true), v.getFloat32(p + 12, true)] : [0, 0, w, h]);
        const [sx, sy, sw, sh] = rect(src, texture.w, texture.h);
        const [dx, dy, dw, dh] = rect(dst, ctx.canvas.width / scale[0], ctx.canvas.height / scale[1]);
        if (sw <= 0 || sh <= 0 || dw === 0 || dh === 0) return 1;
        const cx = center ? v.getFloat32(center, true) : dw / 2;
        const cy = center ? v.getFloat32(center + 4, true) : dh / 2;
        ctx.save();
        ctx.imageSmoothingEnabled = texture.smooth;
        ctx.globalAlpha = texture.alpha / 255;
        ctx.translate(dx + cx, dy + cy);
        if (angle) ctx.rotate((angle * Math.PI) / 180);
        ctx.scale(flip & 1 ? -1 : 1, flip & 2 ? -1 : 1);
        ctx.drawImage(tinted(texture), sx, sy, sw, sh, -cx, -cy, dw, dh);
        ctx.restore();
        return 1;
    },
    tex_set(id, what, value) {
        const texture = textures.get(id);
        if (!texture) return 0;
        if (what === 1) texture.smooth = value === 1;
        else if (what === 2) texture.alpha = value & 255;
        else if (what === 3) texture.tint = value & 0xffffff;
        return 1;
    },
    tex_destroy(id) {
        if (target === id) sdl.set_target(0);
        textures.delete(id);
    },
    set_target(id) {
        const texture = id ? textures.get(id) : null;
        if (id && !texture) return 0;
        target = id;
        ctx = texture ? texture.ctx : back.getContext('2d');
        ctx.setTransform(scale[0], 0, 0, scale[1], 0, 0);
        ctx.imageSmoothingEnabled = false;
        if (texture) texture.version++;
        return 1;
    },

    // ---------- Imágenes (SDL3_image): el navegador decodifica y codifica
    image_decode: suspending(async (pointer, length, w, h) => {
        try {
            const image = await createImageBitmap(new Blob([bytes().slice(pointer, pointer + length)]));
            const canvas = new OffscreenCanvas(image.width, image.height);
            const c = canvas.getContext('2d');
            c.drawImage(image, 0, 0);
            const v = view();
            v.setInt32(w, image.width, true);
            v.setInt32(h, image.height, true);
            return keepBlob(c.getImageData(0, 0, image.width, image.height).data);
        } catch {
            return 0;
        }
    }),
    blob_copy(id, pointer) {
        const data = blobs.get(id);
        blobs.delete(id);
        if (data) bytes().set(data, pointer);
    },
    image_encode: suspending(async (pixels, w, h, pitch, format, size) => {
        try {
            const canvas = new OffscreenCanvas(w, h);
            canvas.getContext('2d').putImageData(new ImageData(toRGBA(pixels, w, h, pitch, format), w, h), 0, 0);
            const png = new Uint8Array(await (await canvas.convertToBlob({ type: 'image/png' })).arrayBuffer());
            view().setInt32(size, png.length, true);
            return keepBlob(png);
        } catch {
            return 0;
        }
    }),

    // ---------- Fuentes (SDL3_ttf): el archivo .ttf se carga en el worker y el lienzo dibuja el texto
    font_open: suspending(async (pointer, length) => {
        try {
            const id = ++fontSeq;
            const face = new FontFace(`sdlfuente${id}`, bytes().slice(pointer, pointer + length));
            await face.load();
            self.fonts.add(face);
            fonts.set(id, `sdlfuente${id}`);
            return id;
        } catch {
            return 0;
        }
    }),
    font_measure(id, size, style, text, length, w, h) {
        if (!fonts.has(id)) return 0;
        const c = new OffscreenCanvas(1, 1).getContext('2d');
        c.font = fontCss(id, size, style);
        const box = textBox(c, new TextDecoder().decode(bytes().slice(text, text + length)));
        const v = view();
        if (w) v.setInt32(w, box.w, true);
        if (h) v.setInt32(h, box.h, true);
        return 1;
    },
    font_render(id, size, style, text, length, fg, bg, mode, w, h) {
        if (!fonts.has(id)) return 0;
        const words = new TextDecoder().decode(bytes().slice(text, text + length));
        const measure = new OffscreenCanvas(1, 1).getContext('2d');
        measure.font = fontCss(id, size, style);
        const box = textBox(measure, words);
        const canvas = new OffscreenCanvas(box.w, box.h);
        const c = canvas.getContext('2d');
        const rgba = (n) => `rgba(${n >>> 24},${(n >>> 16) & 255},${(n >>> 8) & 255},${(n & 255) / 255})`;
        if (mode === 2) {
            c.fillStyle = rgba(bg);
            c.fillRect(0, 0, box.w, box.h);
        }
        c.font = fontCss(id, size, style);
        c.fillStyle = rgba(fg);
        c.textBaseline = 'alphabetic';
        c.fillText(words, 0, box.ascent);
        const data = c.getImageData(0, 0, box.w, box.h).data;
        // Solid: sin bordes suaves (cada píxel, lleno o vacío).
        if (mode === 1) for (let i = 3; i < data.length; i += 4) data[i] = data[i] >= 128 ? 255 : 0;
        const v = view();
        v.setInt32(w, box.w, true);
        v.setInt32(h, box.h, true);
        return keepBlob(data);
    },

    // ---------- SDL3_mixer: la página tiene el audio; acá, la cuenta de qué suena y hasta cuándo
    mix_create() {
        const id = ++mixSeq;
        post({ type: 'mix', action: 'mixer', id });
        return id;
    },
    mix_audio_pcm(format, channels, freq, pointer, length) {
        if (channels < 1 || freq < 1000) return 0;
        const id = ++mixSeq;
        const samples = toFloat(format, pointer, length);
        mixAudios.set(id, { ms: (samples.length / channels / freq) * 1000 });
        post({ type: 'mix', action: 'pcm', id, channels, freq, samples }, [samples.buffer]);
        return id;
    },
    mix_audio_encoded(pointer, length) {
        const id = ++mixSeq;
        mixAudios.set(id, { ms: null });
        post({ type: 'mix', action: 'encoded', id, data: bytes().slice(pointer, pointer + length) });
        return id;
    },
    mix_audio_sine(hz, amplitude, ms) {
        const id = ++mixSeq;
        const freq = 44100;
        const samples = new Float32Array(Math.max(1, Math.round((freq * Math.max(1, ms)) / 1000)));
        for (let i = 0; i < samples.length; i++) samples[i] = Math.sin((2 * Math.PI * hz * i) / freq) * amplitude;
        mixAudios.set(id, { ms });
        post({ type: 'mix', action: 'pcm', id, channels: 1, freq, samples }, [samples.buffer]);
        return id;
    },
    mix_track(mixer) {
        const id = ++mixSeq;
        mixTracks.set(id, { audio: 0, playingUntil: 0, paused: null });
        post({ type: 'mix', action: 'track', id, mixer });
        return id;
    },
    mix_control(what, id, arg, value) {
        const now = performance.now();
        const track = mixTracks.get(id);
        const length = (audio) => mixAudios.get(audio)?.ms ?? 0;
        switch (what) {
            case 1: if (!track) return 0; track.audio = arg; break;
            case 2:
                if (!track || !track.audio) return 0;
                track.paused = null;
                track.playingUntil = arg < 0 ? Infinity : now + length(track.audio) * (arg + 1);
                break;
            case 3: if (!track) return 0; if (track.playingUntil > now) track.paused = track.playingUntil - now; track.playingUntil = 0; break;
            case 4: if (!track) return 0; if (track.paused !== null) track.playingUntil = now + track.paused; track.paused = null; break;
            case 5: if (!track) return 0; track.playingUntil = 0; track.paused = null; break;
            case 7: return track && track.playingUntil > now ? 1 : 0;
            case 10: mixTracks.delete(id); break;
            case 9: mixAudios.delete(id); break;
            default: break;
        }
        if (what === 2 || what === 8) soundUsed = true;
        post({ type: 'mix', action: ['', 'set', 'play', 'pause', 'resume', 'stop', 'gain', '', 'fire', 'free-audio', 'free-track', 'free-mixer', 'master'][what], id, arg, value });
        return 1;
    },

    // ---------- SDL3_net: la red de mentira (los juegos de la página se conectan por número de puerto)
    net_listen(port) {
        for (const server of netServers.values()) if (server.port === port) return 0;
        const id = ++netSeq;
        netServers.set(id, { port, pending: [] });
        netSend({ op: 'listen', port, server: id });
        return id;
    },
    net_unlisten(id) {
        const server = netServers.get(id);
        if (!server) return;
        netServers.delete(id);
        netSend({ op: 'unlisten', port: server.port, server: id });
    },
    net_accept(id) {
        return netServers.get(id)?.pending.shift() ?? 0;
    },
    net_connect(port) {
        const id = ++netSeq;
        netSockets.set(id, { status: 0, conn: 0, inbox: [], closed: false, waiters: [] });
        netSend({ op: 'connect', port, sock: id });
        return id;
    },
    net_wait_connected: suspending((id, timeout) => {
        const sock = netSockets.get(id);
        if (!sock) return -1;
        if (sock.status !== 0 || timeout === 0) return sock.status;
        return new Promise((resolve) => {
            const done = () => resolve(sock.status);
            sock.waiters.push(done);
            if (timeout > 0) setTimeout(done, timeout);
            post({ type: 'alive' });
        });
    }),
    net_status(id) {
        return netSockets.get(id)?.status ?? -1;
    },
    net_write(id, pointer, length) {
        const sock = netSockets.get(id);
        if (!sock || sock.status !== 1 || sock.closed) return 0;
        if (length > 0) netSend({ op: 'data', conn: sock.conn, sock: id, data: bytes().slice(pointer, pointer + length) });
        return 1;
    },
    net_read(id, pointer, length) {
        const sock = netSockets.get(id);
        if (!sock) return -1;
        let read = 0;
        while (read < length && sock.inbox.length) {
            const chunk = sock.inbox[0];
            const n = Math.min(chunk.length, length - read);
            bytes().set(chunk.subarray(0, n), pointer + read);
            read += n;
            if (n === chunk.length) sock.inbox.shift();
            else sock.inbox[0] = chunk.subarray(n);
        }
        if (!read && (sock.closed || sock.status === -1)) return -1;
        return read;
    },
    net_close(id) {
        const sock = netSockets.get(id);
        if (!sock) return;
        netSockets.delete(id);
        if (sock.conn) netSend({ op: 'close', conn: sock.conn, sock: id });
    },
    net_wait_input: suspending((ids, count, timeout) => {
        const ready = () => {
            const v = view();
            let n = 0;
            for (let i = 0; i < count; i++) {
                const id = v.getInt32(ids + i * 4, true);
                const sock = netSockets.get(id);
                if ((sock && (sock.inbox.length || sock.closed)) || netServers.get(id)?.pending.length) n++;
            }
            return n;
        };
        const now = ready();
        if (now || timeout === 0) return now;
        const until = timeout < 0 ? Infinity : performance.now() + timeout;
        return new Promise((resolve) => {
            const check = () => {
                const n = ready();
                if (n || performance.now() >= until) resolve(n);
                else setTimeout(check, 5);
            };
            pause(5).then(check);
        });
    }),

    // ---------- Archivos: lo de prefs/ queda guardado en el navegador (los récords siguen ahí la próxima vez)
    files_changed() {
        clearTimeout(filesTimer);
        filesTimer = setTimeout(saveFiles, 200);
    },

    // ---------- Hilos, temporizadores y candados
    thread_create(pointer, data, stackTop) {
        const id = ++threadSeq;
        const parent = { sp: getSP(), fiber };
        const thread = { done: false, result: 0, promise: null };
        threads.set(id, thread);
        setSP(stackTop);
        fiber = id;
        let promise;
        try {
            promise = WebAssembly.promising(fn(pointer))(data);
        } finally {
            setSP(parent.sp);
            fiber = parent.fiber;
        }
        thread.promise = promise.then(
            (result) => { thread.done = true; thread.result = result; return result; },
            (error) => { thread.done = true; if (!(error instanceof WASIProcExit)) crash(error); return -1; },
        );
        return id;
    },
    thread_wait: suspending((id) => {
        const thread = threads.get(id);
        if (!thread) return 0;
        return thread.done ? thread.result : thread.promise;
    }),
    thread_current() {
        return BigInt(fiber + 1);
    },
    timer_add(interval, callback, userdata) {
        if (!callback) return 0;
        const id = ++timerSeq;
        const timer = { callback, userdata, interval: Math.max(1, interval >>> 0), handle: 0 };
        const fire = () => {
            if (!timers.has(id)) return;
            let next = 0;
            try {
                next = fn(timer.callback)(timer.userdata, id, timer.interval) >>> 0;
            } catch (error) {
                crash(error);
                return;
            }
            if (!next || !timers.has(id)) return void timers.delete(id);
            timer.interval = next;
            timer.handle = setTimeout(fire, next);
        };
        timer.handle = setTimeout(fire, timer.interval);
        timers.set(id, timer);
        return id;
    },
    timer_remove(id) {
        const timer = timers.get(id);
        if (!timer) return 0;
        clearTimeout(timer.handle);
        timers.delete(id);
        return 1;
    },
    // Un candado tomado por otro hilo: se espera (cediendo) hasta que lo suelte.
    mutex_lock: suspending((pointer) => {
        const take = () => {
            const lock = mutexes.get(pointer);
            if (!lock || lock.owner === fiber) {
                mutexes.set(pointer, { owner: fiber, depth: (lock?.depth ?? 0) + 1 });
                return true;
            }
            return false;
        };
        if (take()) return undefined;
        const me = fiber;
        return new Promise((resolve) => {
            const retry = () => {
                fiber = me;
                if (take()) resolve();
                else setTimeout(retry, 1);
            };
            setTimeout(retry, 1);
        });
    }),
    mutex_unlock(pointer) {
        const lock = mutexes.get(pointer);
        if (!lock || lock.owner !== fiber) return;
        if (--lock.depth <= 0) mutexes.delete(pointer);
    },
};

function bytesPerSample(format) {
    return (format & 0xff) / 8;
}

/** Las muestras del juego (U8, S8, S16, S32 o F32) a decimales entre -1 y 1, como las pide el audio del navegador. */
function toFloat(format, pointer, length) {
    const size = bytesPerSample(format);
    const count = Math.floor(length / size);
    const v = view();
    const little = (format & 0x1000) === 0;
    const out = new Float32Array(count);
    for (let i = 0, at = pointer; i < count; i++, at += size) {
        if (format === 0x0008) out[i] = (v.getUint8(at) - 128) / 128;
        else if (size === 1) out[i] = v.getInt8(at) / 128;
        else if (size === 2) out[i] = v.getInt16(at, little) / 32768;
        else if (format & 0x0100) out[i] = v.getFloat32(at, little);
        else out[i] = v.getInt32(at, little) / 2147483648;
    }
    return out;
}

/** Los audios con callback (SDL_OpenAudioDeviceStream con función): se les pide más cuando queda poco. */
function feedAudio() {
    for (const [id, stream] of streams) {
        if (!stream.callback || stream.paused) continue;
        const frameBytes = stream.channels * bytesPerSample(stream.format);
        const queued = sdl.audio_queued(id);
        const wanted = Math.round(stream.freq * 0.1) * frameBytes;
        if (queued < wanted) {
            try {
                fn(stream.callback)(stream.userdata, id, wanted - queued, wanted - queued);
            } catch (error) {
                crash(error);
            }
        }
    }
}

/** La carpeta prefs/ como { 'prefs/org/app/records.dat': bytes }, para que la página la guarde. */
function saveFiles() {
    const out = {};
    const walk = (dir, path) => {
        for (const [name, entry] of dir.contents) {
            if (entry instanceof Directory) walk(entry, `${path}${name}/`);
            else if (entry instanceof File) out[path + name] = entry.data;
        }
    };
    const prefs = files?.dir.contents.get('prefs');
    if (prefs instanceof Directory) walk(prefs, 'prefs/');
    post({ type: 'files', files: out });
}

/** Lo guardado de antes, otra vez como carpetas y archivos de WASI. */
function restoreFiles(saved) {
    const root = new Map();
    for (const [path, data] of Object.entries(saved ?? {})) {
        const parts = path.split('/').filter((part) => part && part !== '.' && part !== '..');
        if (parts[0] !== 'prefs' || parts.length < 2) continue;
        let dir = root;
        for (const part of parts.slice(0, -1)) {
            if (!dir.has(part)) dir.set(part, new Directory(new Map()));
            dir = dir.get(part).contents;
        }
        dir.set(parts.at(-1), new File(data));
    }
    return root;
}

function setKey(scancode, down) {
    if (keysPointer && scancode > 0 && scancode < keyCount) bytes()[keysPointer + scancode] = down ? 1 : 0;
}

/** La red de mentira: lo que la página reparte entre los juegos conectados. */
function receiveNet({ op, sock, server, conn, data }) {
    if (op === 'incoming') {
        // Alguien se conectó a un servidor de este juego: nace el socket de este lado, listo para NET_AcceptClient.
        const id = ++netSeq;
        netSockets.set(id, { status: 1, conn, inbox: [], closed: false, waiters: [] });
        netServers.get(server)?.pending.push(id);
        netSend({ op: 'accepted', conn, sock: id });
        return;
    }
    const socket = netSockets.get(sock);
    if (!socket) return;
    if (op === 'connected' || op === 'refused') {
        socket.status = op === 'connected' ? 1 : -1;
        socket.conn = conn ?? 0;
        socket.waiters.splice(0).forEach((wake) => wake());
    } else if (op === 'data') {
        socket.inbox.push(data);
    } else if (op === 'closed') {
        socket.closed = true;
    }
}

/** Lo que llega de la página: teclas, mouse, joysticks y el botón de cerrar. */
function receive(message) {
    switch (message.type) {
        case 'key':
            setKey(message.scancode, message.down);
            queue.push({ type: message.down ? EVENT.KEY_DOWN : EVENT.KEY_UP, data: [message.scancode, message.key, message.mod, message.repeat ? 1 : 0] });
            break;
        case 'mouse': {
            const { x, y, kind, button } = message;
            if (kind === 'move') {
                queue.push({ type: EVENT.MOUSE_MOTION, data: [x, y, x - mouse.x, y - mouse.y, mouse.buttons] });
            } else if (kind === 'wheel') {
                queue.push({ type: EVENT.MOUSE_WHEEL, data: [message.wheelX, message.wheelY, x, y] });
            } else {
                const mask = 1 << (button - 1);
                mouse.buttons = kind === 'down' ? mouse.buttons | mask : mouse.buttons & ~mask;
                queue.push({ type: kind === 'down' ? EVENT.MOUSE_BUTTON_DOWN : EVENT.MOUSE_BUTTON_UP, data: [x, y, button, 1] });
            }
            mouse.x = x;
            mouse.y = y;
            break;
        }
        case 'pads': {
            const seen = new Set();
            for (const pad of message.pads) {
                const id = pad.index + 1;
                seen.add(id);
                const before = pads.get(id);
                if (!before) queue.push({ type: EVENT.PAD_ADDED, data: [id] });
                PAD_BUTTONS.forEach((web, button) => {
                    const was = (before?.buttons[web] ?? 0) > 0.5;
                    const is = (pad.buttons[web] ?? 0) > 0.5;
                    if (was !== is) queue.push({ type: is ? EVENT.PAD_BUTTON_DOWN : EVENT.PAD_BUTTON_UP, data: [id, button] });
                });
                pad.axes.slice(0, 4).forEach((value, axis) => {
                    if (Math.abs(value - (before?.axes[axis] ?? 0)) > 0.01) {
                        queue.push({ type: EVENT.PAD_AXIS, data: [id, axis, Math.round(value * 32767)] });
                    }
                });
                pads.set(id, pad);
            }
            for (const id of [...pads.keys()]) {
                if (!seen.has(id)) {
                    pads.delete(id);
                    queue.push({ type: EVENT.PAD_REMOVED, data: [id] });
                }
            }
            break;
        }
        case 'quit':
            queue.push({ type: EVENT.QUIT, data: [] });
            break;
        case 'net':
            receiveNet(message);
            break;
    }
    // Una cola que nadie lee (el juego no llama a SDL_PollEvent) no crece sin fin.
    if (queue.length > 512) queue.splice(0, queue.length - 512);
}

self.onmessage = async ({ data }) => {
    if (data.type !== 'start') return receive(data);

    screen = data.canvas;
    display = data.display ?? display;
    if (data.test) {
        test = { timeline: [...data.test.timeline], end: Math.max(1, data.test.end), checks: data.test.checks ?? [] };
        seed = 20261125;
    }
    files = new PreopenDirectory('.', restoreFiles(data.files));
    // Los archivos que trae el juego (fuentes, imágenes, sonidos): solo para leer.
    for (const [path, content] of Object.entries(data.assets ?? {})) {
        const parts = path.split('/').filter(Boolean);
        let dir = files.dir.contents;
        for (const part of parts.slice(0, -1)) {
            if (!dir.has(part)) dir.set(part, new Directory(new Map()));
            dir = dir.get(part).contents;
        }
        dir.set(parts.at(-1), new File(content, { readonly: true }));
    }
    const decoder = new TextDecoder();
    const fds = [
        new OpenFile(new File(new Uint8Array())),
        new ConsoleStdout((b) => post({ type: 'output', text: decoder.decode(b, { stream: true }) })),
        new ConsoleStdout((b) => post({ type: 'output', text: decoder.decode(b, { stream: true }), stderr: true })),
        files,
    ];
    try {
        const wasi = new WASI(['juego', ...(data.args ?? [])], [], fds);
        if (test) {
            // time() y clock() también con el reloj de mentira (srand(time(NULL)) da siempre lo mismo).
            wasi.wasiImport.clock_time_get = (id, precision, pointer) => {
                const base = id === 0 ? 1_780_000_000_000n : 0n; // REALTIME: un día fijo
                new DataView(memory.buffer).setBigUint64(pointer, (base + BigInt(Math.round(virtualMs))) * 1_000_000n, true);
                return 0;
            };
        }
        const module = await WebAssembly.compile(data.wasm);
        const instance = await WebAssembly.instantiate(module, { wasi_snapshot_preview1: wasi.wasiImport, sdl });
        memory = instance.exports.memory;
        exports = instance.exports;
        wasi.inst = instance;
        started = lastYield = performance.now();
        if (test) deliverTest();
        let exit = 0;
        try {
            await WebAssembly.promising(instance.exports._start)();
        } catch (e) {
            if (!(e instanceof WASIProcExit)) throw e;
            exit = e.code;
        }
        timers.forEach((timer) => clearTimeout(timer.handle));
        timers.clear();
        if (filesTimer) {
            clearTimeout(filesTimer);
            saveFiles();
        }
        if (test) post({ type: 'test', report: testReport(true, exit) });
        post({ type: 'exit', exit });
    } catch (e) {
        crash(e);
    }
};
