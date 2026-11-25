// El SDL3 de la plataforma (D126): corre un juego en C compilado en el navegador (Clang, D98) y resuelve lo de SDL3
// (resources/js/runners/sdl3/SDL.h) dibujando en un lienzo. Vive en su propio worker: no ve la página ni la sesión,
// y si se cuelga se lo corta. El bucle del juego (`while (jugando)`) se pausa en SDL_Delay y SDL_RenderPresent
// con JSPI (WebAssembly.Suspending): mientras tanto el navegador dibuja y llegan el teclado y el joystick.
import { WASI, File, OpenFile, ConsoleStdout, PreopenDirectory, WASIProcExit } from '@bjorn3/browser_wasi_shim';
import { glyphOf } from '../runners/sdl3/font8x8.js';

const EVENT = {
    QUIT: 0x100, KEY_DOWN: 0x300, KEY_UP: 0x301,
    MOUSE_MOTION: 0x400, MOUSE_BUTTON_DOWN: 0x401, MOUSE_BUTTON_UP: 0x402,
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
    return new Promise((resolve) => setTimeout(resolve, ms));
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
    present: new WebAssembly.Suspending(async () => {
        if (back) {
            const screenCtx = screen.getContext('2d');
            screenCtx.globalCompositeOperation = 'copy';
            screenCtx.drawImage(back, 0, 0);
        }
        await pause(0);
        return 1;
    }),
    delay: new WebAssembly.Suspending(async (ms) => {
        await pause(Math.min(ms >>> 0, 1000));
    }),
    ticks() {
        return performance.now() - started;
    },
    // Si el bucle no se pausa nunca, igual se cede de vez en cuando (si no, la página no le puede mandar teclas).
    poll: new WebAssembly.Suspending((pointer) => {
        const next = queue.shift();
        if (next) {
            const v = view();
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
};

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
    const decoder = new TextDecoder();
    const fds = [
        new OpenFile(new File(new Uint8Array())),
        new ConsoleStdout((b) => post({ type: 'output', text: decoder.decode(b, { stream: true }) })),
        new ConsoleStdout((b) => post({ type: 'output', text: decoder.decode(b, { stream: true }), stderr: true })),
        new PreopenDirectory('.', new Map()),
    ];
    try {
        const wasi = new WASI(['juego'], [], fds);
        const module = await WebAssembly.compile(data.wasm);
        const instance = await WebAssembly.instantiate(module, { wasi_snapshot_preview1: wasi.wasiImport, sdl });
        memory = instance.exports.memory;
        wasi.inst = instance;
        started = lastYield = performance.now();
        let exit = 0;
        try {
            await WebAssembly.promising(instance.exports._start)();
        } catch (e) {
            if (!(e instanceof WASIProcExit)) throw e;
            exit = e.code;
        }
        post({ type: 'exit', exit });
    } catch (e) {
        post({ type: 'crash', message: String(e?.message ?? e) });
    }
};
