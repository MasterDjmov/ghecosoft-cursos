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
    if (now - lastAlive > 250) {
        post({ type: 'alive' });
        lastAlive = now;
    }
    lastYield = now;
    feedAudio();
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

let tile = null;

/** Texto de 8 x 8 píxeles como SDL_RenderDebugText, del color de dibujo. */
function drawText(x, y, text) {
    tile ??= new OffscreenCanvas(8, 8);
    const tileCtx = tile.getContext('2d');
    let cx = x;
    for (const char of text) {
        const image = glyph(char.codePointAt(0));
        if (image) {
            tileCtx.globalCompositeOperation = 'copy';
            tileCtx.putImageData(image, 0, 0);
            tileCtx.globalCompositeOperation = 'source-in';
            tileCtx.fillStyle = fill();
            tileCtx.fillRect(0, 0, 8, 8);
            ctx.drawImage(tile, cx, y);
        }
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
        post({ type: 'window', title: string(title), w: size.w, h: size.h });
        return 1;
    },
    set_title(title) {
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
        ctx.fillRect(0, 0, size.w, size.h);
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
        drawText(x, y, string(pointer));
        return 1;
    },
    present: suspending(async () => {
        if (back) {
            const screenCtx = screen.getContext('2d');
            screenCtx.globalCompositeOperation = 'copy';
            screenCtx.drawImage(back, 0, 0);
        }
        await pause(0);
        return 1;
    }),
    delay: suspending(async (ms) => {
        await pause(Math.min(ms >>> 0, 1000));
    }),
    ticks() {
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
    }
    // Una cola que nadie lee (el juego no llama a SDL_PollEvent) no crece sin fin.
    if (queue.length > 512) queue.splice(0, queue.length - 512);
}

self.onmessage = async ({ data }) => {
    if (data.type !== 'start') return receive(data);

    screen = data.canvas;
    display = data.display ?? display;
    files = new PreopenDirectory('.', restoreFiles(data.files));
    const decoder = new TextDecoder();
    const fds = [
        new OpenFile(new File(new Uint8Array())),
        new ConsoleStdout((b) => post({ type: 'output', text: decoder.decode(b, { stream: true }) })),
        new ConsoleStdout((b) => post({ type: 'output', text: decoder.decode(b, { stream: true }), stderr: true })),
        files,
    ];
    try {
        const wasi = new WASI(['juego'], [], fds);
        const module = await WebAssembly.compile(data.wasm);
        const instance = await WebAssembly.instantiate(module, { wasi_snapshot_preview1: wasi.wasiImport, sdl });
        memory = instance.exports.memory;
        exports = instance.exports;
        wasi.inst = instance;
        started = lastYield = performance.now();
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
        post({ type: 'exit', exit });
    } catch (e) {
        crash(e);
    }
};
