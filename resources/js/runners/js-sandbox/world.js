// El mundo virtual de la caja de JavaScript (D115). Corre ADENTRO del <iframe sandbox="allow-scripts"> (sin mismo
// origen, sin red), antes que el código del alumno, y reemplaza todo lo que tocaría algo de verdad por una versión
// simulada que vive solo mientras dura la ejecución:
//   - el reloj (Date, performance.now) y los temporizadores (setTimeout, setInterval, requestAnimationFrame):
//     avanzan con un reloj propio, así una animación de 10 segundos se comprueba en un instante y da siempre igual;
//   - Math.random, con semilla fija;
//   - las cookies, localStorage y sessionStorage (empiezan vacíos o con lo que trae la consigna);
//   - fetch, contra el Puerto de Elefa simulado (/puerto/...); lo demás no sale: no hay red;
//   - alert, confirm y prompt (las respuestas salen de la Entrada), el portapapeles, la ubicación, la vibración,
//     las notificaciones y el sonido;
//   - un tope de vueltas en cada bucle y en cada función (__tick__, que inyecta js-instrument.js).
// Además graba lo que se dibuja en cada <canvas>, ejecuta los eventos de la consigna (click, escribir, teclas,
// esperar) y arma el «Estado» que se compara. Este archivo se inyecta como texto (no puede importar nada).
(() => {
    'use strict';

    const configNode = document.getElementById('caja-config');
    const CONFIG = JSON.parse(configNode.textContent);
    configNode.remove();

    const TOKEN = CONFIG.token;
    const real = {
        now: performance.now.bind(performance),
        Date: window.Date,
        setTimeout: window.setTimeout.bind(window),
        raf: window.requestAnimationFrame.bind(window),
        MessageChannel: window.MessageChannel,
        Response: window.Response,
        Request: window.Request,
        Headers: window.Headers,
        URL: window.URL,
        Blob: window.Blob,
        createObjectURL: URL.createObjectURL.bind(URL),
    };
    const post = (type, data = {}) => parent.postMessage({ caja: TOKEN, type, ...data }, '*');
    const define = (target, name, value) => Object.defineProperty(target, name, { value, configurable: true, writable: true });

    // ───────────────────────────── La salida ─────────────────────────────

    const MAX_OUTPUT = 200000;
    let output = '';
    let liveOutput = '';
    let phase = 'check';
    let cut = false;
    let indent = '';
    const notices = [];

    function write(text) {
        if (cut) return;
        const lines = String(text).split('\n').map((l) => indent + l).join('\n') + '\n';
        if (phase === 'live') {
            liveOutput += lines;
            scheduleFlush();
            return;
        }
        if (output.length + lines.length > MAX_OUTPUT) {
            output += '… (la salida es demasiado larga: se cortó acá)\n';
            cut = true;
            return;
        }
        output += lines;
    }

    function notice(kind, text) {
        if (notices.length < 200) notices.push({ kind, text, at: Math.round(now) });
        boardChanged();
    }

    // ───────────────────────────── El reloj y los temporizadores ─────────────────────────────

    // El reloj de la Feria arranca el 2 de marzo de 2026 a las 21:00 (hora argentina).
    const START = CONFIG.epoch ?? Date.UTC(2026, 2, 3, 0, 0, 0);
    const FRAME = 1000 / 60;
    // `now` cuenta los milisegundos desde START (un número chico: con el absoluto se pierden decimales y los
    // cuadros de 16,67 ms dejan de avanzar).
    let now = 0;
    let timerSeq = 0;
    let order = 0;
    let fired = 0;
    let nesting = 0;
    const MAX_FIRINGS = 200000;
    const timers = new Map();

    function schedule(kind, fn, delay, args, repeat) {
        if (typeof fn !== 'function') {
            throw new TypeError(`${kind === 'raf' ? 'requestAnimationFrame' : kind === 'interval' ? 'setInterval' : 'setTimeout'} necesita una función (en la caja no se ejecuta código escrito en un texto).`);
        }
        let wait = Math.max(0, Number(delay) || 0);
        // Como los navegadores: a partir del quinto temporizador anidado, menos de 4 ms cuenta como 4 ms.
        if (nesting >= 5 && wait < 4) wait = 4;
        const id = ++timerSeq;
        const at = kind === 'raf' ? (Math.floor(now / FRAME + 1e-6) + 1) * FRAME : now + wait;
        timers.set(id, { id, kind, fn, args: args ?? [], at, seq: ++order, repeat: repeat ? Math.max(wait, 1) : 0, nesting: nesting + 1 });
        boardChanged();
        return id;
    }

    function cancel(id) {
        if (timers.delete(Number(id))) boardChanged();
    }

    function nextTimer() {
        let best = null;
        for (const t of timers.values()) {
            if (!best || t.at < best.at || (t.at === best.at && t.seq < best.seq)) best = t;
        }
        return best;
    }

    /** Dispara el próximo temporizador (o todos los cuadros de animación de ese instante, juntos). */
    function fire(timer) {
        now = Math.max(now, timer.at);
        if (timer.kind === 'raf') {
            const batch = [...timers.values()].filter((t) => t.kind === 'raf' && t.at === timer.at).sort((a, b) => a.seq - b.seq);
            for (const t of batch) timers.delete(t.id);
            newFrame();
            const stamp = now;
            for (const t of batch) runCallback(t, [stamp]);
            return;
        }
        if (timer.repeat) {
            timer.at = now + timer.repeat;
            timer.seq = ++order;
        } else {
            timers.delete(timer.id);
        }
        runCallback(timer, timer.args);
    }

    function runCallback(timer, args) {
        if (++fired > MAX_FIRINGS) {
            stop('Se dispararon demasiados temporizadores: ¿hay uno que se vuelve a programar sin fin?');
            return;
        }
        const before = nesting;
        nesting = timer.nesting;
        startSegment();
        try {
            timer.fn(...args);
        } catch (error) {
            uncaught(error);
        } finally {
            nesting = before;
        }
    }

    window.setTimeout = (fn, delay, ...args) => schedule('timeout', fn, delay, args, false);
    window.setInterval = (fn, delay, ...args) => schedule('interval', fn, delay, args, true);
    window.clearTimeout = cancel;
    window.clearInterval = cancel;
    window.requestAnimationFrame = (fn) => schedule('raf', fn, 0, [], false);
    window.cancelAnimationFrame = cancel;
    window.requestIdleCallback = (fn) => schedule('timeout', () => fn({ didTimeout: false, timeRemaining: () => 50 }), 1, [], false);
    window.cancelIdleCallback = cancel;

    function VirtualDate(...args) {
        if (!new.target) return new real.Date(START + Math.floor(now)).toString();
        return Reflect.construct(real.Date, args.length ? args : [START + Math.floor(now)], new.target);
    }
    VirtualDate.prototype = real.Date.prototype;
    VirtualDate.now = () => START + Math.floor(now);
    VirtualDate.parse = real.Date.parse;
    VirtualDate.UTC = real.Date.UTC;
    Object.defineProperty(VirtualDate, 'name', { value: 'Date' });
    window.Date = VirtualDate;
    define(performance, 'now', () => now);

    const realTimeout = AbortSignal.timeout?.bind(AbortSignal);
    if (realTimeout) {
        define(AbortSignal, 'timeout', (ms) => {
            const controller = new AbortController();
            schedule('timeout', () => controller.abort(new DOMException('signal timed out', 'TimeoutError')), ms, [], false);
            return controller.signal;
        });
    }

    // Math.random con semilla (mulberry32): la misma ejecución da los mismos números.
    let seed = (CONFIG.seed ?? 2026) >>> 0;
    define(Math, 'random', () => {
        seed = (seed + 0x6d2b79f5) >>> 0;
        let t = seed;
        t = Math.imul(t ^ (t >>> 15), t | 1);
        t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    });

    // ───────────────────────────── El tope de vueltas y de tiempo ─────────────────────────────

    let dead = false;
    let timedOut = false;
    let stopReason = null;
    let ticks = 0;
    let deadline = real.now() + (CONFIG.timeout ?? 5000);

    class Stopped extends Error {}

    function startSegment() {
        // En vivo, cada evento o temporizador tiene su propio tiempo; al comprobar, vale el total de la ejecución.
        if (phase === 'live') deadline = real.now() + 1500;
    }

    function stop(reason) {
        if (dead) return;
        dead = true;
        stopReason = reason;
        timers.clear();
    }

    // js-instrument.js pone __begin__(n) al principio de cada script: hasta que arranca no se lo da por trabado.
    const started = new Set();
    Object.defineProperty(window, '__begin__', { value: (index) => started.add(index) });

    Object.defineProperty(window, '__tick__', {
        value() {
            if (dead) throw new Stopped(stopReason ?? 'Se cortó la ejecución.');
            if ((++ticks & 1023) === 0 && real.now() > deadline) {
                timedOut = true;
                stop(phase === 'live'
                    ? 'Se cortó: algo tardó más de un segundo y medio sin terminar. ¿Hay un bucle que no termina?'
                    : `Se cortó a los ${(CONFIG.timeout ?? 5000) / 1000} segundos. ¿Hay un bucle que no termina?`);
                throw new Stopped(stopReason);
            }
        },
    });

    // ───────────────────────────── Los errores ─────────────────────────────

    const scriptOffsets = new Map();
    let firstError = null;
    let errorCount = 0;

    function lineOf(error) {
        const stack = String(error?.stack ?? '');
        for (const match of stack.matchAll(/(blob:[^\s)]+?):(\d+):(\d+)/g)) {
            const where = scriptOffsets.get(match[1]);
            if (where) return { line: Number(match[2]) + where.offset, file: where.file };
        }
        return null;
    }

    function describeError(error, promise = false) {
        if (error instanceof Stopped) return null;
        const isError = error instanceof Error || (error && typeof error === 'object' && 'message' in error && 'name' in error);
        const where = isError ? lineOf(error) : null;
        return {
            name: isError ? String(error.name) : 'Error',
            message: isError ? String(error.message) : inspect(error),
            thrown: !isError,
            line: where?.line ?? null,
            file: where?.file ?? null,
            promise,
        };
    }

    function uncaught(error, promise = false) {
        const info = describeError(error, promise);
        if (!info) return;
        errorCount++;
        if (phase === 'live') {
            post('error', { error: info });
            return;
        }
        firstError ??= info;
    }

    window.addEventListener('error', (event) => {
        event.preventDefault();
        uncaught(event.error ?? new Error(event.message));
    });
    window.addEventListener('unhandledrejection', (event) => {
        event.preventDefault();
        uncaught(event.reason, true);
    });

    // ───────────────────────────── La consola ─────────────────────────────

    const IDENT = /^[A-Za-z_$][\w$]*$/;
    const quote = (s) => `'${String(s).replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/\n/g, '\\n')}'`;

    function functionLabel(fn) {
        const source = Function.prototype.toString.call(fn);
        if (/^class\b/.test(source)) {
            const parent = Object.getPrototypeOf(fn);
            return `[class ${fn.name || '(anonymous)'}${parent && parent.name ? ` extends ${parent.name}` : ''}]`;
        }
        const kind = fn.constructor?.name === 'AsyncFunction' ? 'AsyncFunction' : fn.constructor?.name === 'GeneratorFunction' ? 'GeneratorFunction' : 'Function';
        return `[${kind}${fn.name ? `: ${fn.name}` : ' (anonymous)'}]`;
    }

    function wrap(open, items, close, level) {
        if (!items.length) return `${open.trimEnd()}${close.trimStart()}`.replace(/\s+/g, ' ').replace('{ }', '{}').replace('[ ]', '[]');
        const single = `${open}${items.join(', ')}${close}`;
        if (single.length + level * 2 <= 76 && !items.some((i) => i.includes('\n'))) return single;
        const pad = '  '.repeat(level + 1);
        return `${open.trimEnd()}\n${items.map((i) => pad + i.replace(/\n/g, '\n' + pad)).join(',\n')}\n${'  '.repeat(level)}${close.trimStart()}`;
    }

    function inspect(value, level = 0, seen = new Set(), top = true) {
        switch (typeof value) {
            case 'string': return top ? value : quote(value);
            case 'number': return Object.is(value, -0) ? '-0' : String(value);
            case 'bigint': return `${value}n`;
            case 'boolean':
            case 'undefined': return String(value);
            case 'symbol': return value.toString();
            case 'function': return functionLabel(value);
        }
        if (value === null) return 'null';
        if (seen.has(value)) return '[Circular]';
        if (value instanceof Error) return value.message ? `${value.name}: ${value.message}` : value.name;
        if (value instanceof real.Date) return Number.isNaN(value.getTime()) ? 'Invalid Date' : value.toISOString();
        if (value instanceof RegExp) return String(value);
        if (value instanceof Promise) return 'Promise { … }';
        if (typeof Node !== 'undefined' && value instanceof Node) return nodeLabel(value);
        if (value === localStorage || value === sessionStorage) {
            return wrap('Storage { ', [...storageMaps.get(value)].map(([k, v]) => `${IDENT.test(k) ? k : quote(k)}: ${quote(v)}`), ' }', level);
        }
        if (level > 2) return Array.isArray(value) ? '[Array]' : '[Object]';

        seen.add(value);
        try {
            if (Array.isArray(value) || ArrayBuffer.isView(value)) {
                const items = [];
                let holes = 0;
                const max = Math.min(value.length, 100);
                for (let i = 0; i < max; i++) {
                    if (!(i in value)) { holes++; continue; }
                    if (holes) { items.push(`<${holes} empty item${holes > 1 ? 's' : ''}>`); holes = 0; }
                    items.push(inspect(value[i], level + 1, seen, false));
                }
                if (holes) items.push(`<${holes} empty item${holes > 1 ? 's' : ''}>`);
                if (value.length > 100) items.push(`... ${value.length - 100} more item${value.length - 100 > 1 ? 's' : ''}`);
                const prefix = Array.isArray(value) ? (value.constructor && value.constructor !== Array ? `${value.constructor.name}(${value.length}) ` : '') : `${value.constructor.name}(${value.length}) `;
                return prefix + wrap('[ ', items, ' ]', level);
            }
            if (value instanceof Map) {
                return `Map(${value.size}) ` + wrap('{ ', [...value].slice(0, 100).map(([k, v]) => `${inspect(k, level + 1, seen, false)} => ${inspect(v, level + 1, seen, false)}`), ' }', level);
            }
            if (value instanceof Set) {
                return `Set(${value.size}) ` + wrap('{ ', [...value].slice(0, 100).map((v) => inspect(v, level + 1, seen, false)), ' }', level);
            }
            const proto = Object.getPrototypeOf(value);
            const name = proto === null ? '[Object: null prototype]' : proto.constructor && proto.constructor !== Object ? proto.constructor.name : '';
            const items = [];
            for (const key of Reflect.ownKeys(value)) {
                const desc = Object.getOwnPropertyDescriptor(value, key);
                if (!desc.enumerable) continue;
                const label = typeof key === 'symbol' ? `[${key.toString()}]` : IDENT.test(key) ? key : quote(key);
                const shown = desc.get ? (desc.set ? '[Getter/Setter]' : '[Getter]') : desc.set ? '[Setter]' : inspect(desc.value, level + 1, seen, false);
                items.push(`${label}: ${shown}`);
            }
            return (name ? `${name} ` : '') + wrap('{ ', items, ' }', level);
        } finally {
            seen.delete(value);
        }
    }

    function nodeLabel(node) {
        if (node instanceof Element) {
            const id = node.id ? `#${node.id}` : '';
            const classes = node.classList.length ? '.' + [...node.classList].join('.') : '';
            return `<${node.tagName.toLowerCase()}${id}${classes}>`;
        }
        if (node instanceof Text) return quote(node.textContent);
        return node.nodeName;
    }

    /** console.log("Hola %s, tenés %d fichas", nombre, n) */
    function format(args) {
        if (typeof args[0] === 'string' && /%[sdifoOjc%]/.test(args[0])) {
            let rest = args.slice(1);
            const text = args[0].replace(/%([sdifoOjc%])/g, (all, kind) => {
                if (kind === '%') return '%';
                if (!rest.length) return all;
                const value = rest.shift();
                switch (kind) {
                    case 's': return typeof value === 'string' ? value : inspect(value, 1, new Set(), false);
                    case 'd':
                    case 'i': return typeof value === 'object' ? 'NaN' : String(kind === 'i' ? Math.trunc(Number(value)) : Number(value));
                    case 'f': return String(Number(value));
                    case 'j': return JSON.stringify(value);
                    case 'c': return '';
                    default: return inspect(value, 0, new Set(), false);
                }
            });
            args = [text, ...rest];
        }
        return args.map((a) => inspect(a)).join(' ');
    }

    function table(data, columns) {
        if (data === null || typeof data !== 'object') return write(format([data]));
        const rows = data instanceof Map ? [...data] : Object.entries(data);
        const keys = [];
        const hasValues = rows.some(([, v]) => v === null || typeof v !== 'object');
        for (const [, v] of rows) {
            if (v && typeof v === 'object') for (const k of Object.keys(v)) if (!keys.includes(k)) keys.push(k);
        }
        const cols = columns ?? keys;
        const head = ['(index)', ...cols, ...(hasValues ? ['Values'] : [])];
        const body = rows.map(([k, v]) => [String(k), ...cols.map((c) => (v && typeof v === 'object' && c in v ? inspect(v[c], 1, new Set(), false) : '')), ...(hasValues ? [v && typeof v === 'object' ? '' : inspect(v, 1, new Set(), false)] : [])]);
        const widths = head.map((h, i) => Math.max(h.length, ...body.map((r) => r[i].length)) + 2);
        const line = (l, m, r) => l + widths.map((w) => '─'.repeat(w)).join(m) + r;
        const row = (cells) => '│' + cells.map((c, i) => ' ' + c.padEnd(widths[i] - 1)).join('│') + '│';
        write([line('┌', '┬', '┐'), row(head), line('├', '┼', '┤'), ...body.map(row), line('└', '┴', '┘')].join('\n'));
    }

    const counts = new Map();
    const timersByLabel = new Map();
    const virtualConsole = {
        log: (...a) => write(format(a)),
        info: (...a) => write(format(a)),
        debug: (...a) => write(format(a)),
        warn: (...a) => write(format(a)),
        error: (...a) => write(format(a)),
        trace: (...a) => write(`Trace${a.length ? ': ' + format(a) : ''}`),
        dir: (v) => write(inspect(v, 0, new Set(), false)),
        table,
        assert: (ok, ...a) => { if (!ok) write(`Assertion failed${a.length ? ': ' + format(a) : ''}`); },
        group: (...a) => { if (a.length) write(format(a)); indent += '  '; },
        groupCollapsed: (...a) => { if (a.length) write(format(a)); indent += '  '; },
        groupEnd: () => { indent = indent.slice(2); },
        count: (label = 'default') => { counts.set(label, (counts.get(label) ?? 0) + 1); write(`${label}: ${counts.get(label)}`); },
        countReset: (label = 'default') => counts.delete(label),
        time: (label = 'default') => timersByLabel.set(label, now),
        timeLog: (label = 'default', ...a) => write(`${label}: ${Math.round((now - (timersByLabel.get(label) ?? now)) * 1000) / 1000}ms${a.length ? ' ' + format(a) : ''}`),
        timeEnd: (label = 'default') => { write(`${label}: ${Math.round((now - (timersByLabel.get(label) ?? now)) * 1000) / 1000}ms`); timersByLabel.delete(label); },
        clear: () => { if (phase === 'live') liveOutput = ''; else output = ''; },
    };
    define(window, 'console', virtualConsole);

    // ───────────────────────────── Ventanitas: alert, confirm, prompt ─────────────────────────────

    const input = String(CONFIG.stdin ?? '').replace(/\r/g, '').split('\n');
    if (input.length && input[input.length - 1] === '') input.pop();

    define(window, 'alert', (message = '') => { write(`[alerta] ${String(message)}`); notice('alerta', String(message)); });
    define(window, 'confirm', (message = '') => {
        const answer = input.length ? !/^(n|no|false|0|cancelar)$/i.test(input.shift().trim()) : true;
        write(`[confirmar] ${String(message)} → ${answer ? 'Aceptar' : 'Cancelar'}`);
        return answer;
    });
    define(window, 'prompt', (message = '', fallback) => {
        const answer = input.length ? input.shift() : fallback === undefined ? null : String(fallback);
        write(`[pregunta] ${String(message)} → ${answer === null ? '(cancelado)' : answer}`);
        return answer;
    });
    define(window, 'print', () => notice('imprimir', 'window.print()'));
    define(window, 'open', (url = '') => { notice('ventana', `window.open(${String(url)}): en la caja no se abren ventanas`); return null; });

    // ───────────────────────────── Almacenamiento y cookies ─────────────────────────────

    const storageMaps = new Map();

    function makeStorage(initial, label) {
        const map = new Map(Object.entries(initial ?? {}).map(([k, v]) => [String(k), String(v)]));
        const size = () => [...map].reduce((n, [k, v]) => n + k.length + v.length, 0);
        const api = {
            getItem: (k) => (map.has(String(k)) ? map.get(String(k)) : null),
            setItem: (k, v) => {
                map.set(String(k), String(v));
                if (size() > 5_000_000) {
                    map.delete(String(k));
                    throw new DOMException(`Se llenó el ${label} (5 MB).`, 'QuotaExceededError');
                }
                boardChanged();
            },
            removeItem: (k) => { map.delete(String(k)); boardChanged(); },
            clear: () => { map.clear(); boardChanged(); },
            key: (i) => [...map.keys()][i] ?? null,
        };
        const proxy = new Proxy(api, {
            get(target, prop) {
                if (prop === 'length') return map.size;
                if (prop in target) return target[prop];
                if (prop === Symbol.toStringTag) return 'Storage';
                return typeof prop === 'string' && map.has(prop) ? map.get(prop) : undefined;
            },
            set(target, prop, value) { api.setItem(prop, value); return true; },
            deleteProperty(target, prop) { api.removeItem(prop); return true; },
            has(target, prop) { return map.has(prop) || prop in target; },
            ownKeys() { return [...map.keys()]; },
            getOwnPropertyDescriptor(target, prop) {
                return map.has(prop) ? { value: map.get(prop), enumerable: true, configurable: true, writable: true } : undefined;
            },
        });
        storageMaps.set(proxy, map);
        return proxy;
    }

    const localStorage = makeStorage(CONFIG.storage?.local, 'localStorage');
    const sessionStorage = makeStorage(CONFIG.storage?.session, 'sessionStorage');
    define(window, 'localStorage', localStorage);
    define(window, 'sessionStorage', sessionStorage);

    // name → { value, expires (ms del reloj de la caja, o null), httpOnly }
    const jar = new Map();

    function purgeCookies() {
        for (const [name, cookie] of jar) if (cookie.expires !== null && cookie.expires <= now) jar.delete(name);
    }

    function setCookie(text, fromServer = false) {
        const [pair, ...attributes] = String(text).split(';');
        const eq = pair.indexOf('=');
        const name = (eq === -1 ? '' : pair.slice(0, eq)).trim();
        const value = (eq === -1 ? pair : pair.slice(eq + 1)).trim();
        let expires = null;
        let httpOnly = false;
        for (const attribute of attributes) {
            const [key, ...rest] = attribute.split('=');
            const k = key.trim().toLowerCase();
            const v = rest.join('=').trim();
            if (k === 'max-age') expires = now + Number(v) * 1000;
            else if (k === 'expires' && expires === null) expires = real.Date.parse(v) - START;
            else if (k === 'httponly') httpOnly = true;
        }
        // Desde JavaScript no se puede crear una cookie HttpOnly (el navegador la ignora), ni pisar una.
        if (!fromServer && (httpOnly || jar.get(name)?.httpOnly)) return;
        if (expires !== null && (Number.isNaN(expires) || expires <= now)) jar.delete(name);
        else jar.set(name, { value, expires, httpOnly });
        boardChanged();
    }

    for (const part of String(CONFIG.cookies ?? '').split(';')) if (part.trim()) setCookie(part.trim());

    Object.defineProperty(document, 'cookie', {
        configurable: true,
        get() {
            purgeCookies();
            return [...jar].filter(([, c]) => !c.httpOnly).map(([n, c]) => (n ? `${n}=${c.value}` : c.value)).join('; ');
        },
        set(text) { setCookie(text); },
    });

    function cookieHeader() {
        purgeCookies();
        return [...jar].map(([n, c]) => `${n}=${c.value}`).join('; ');
    }

    // ───────────────────────────── El Puerto de Elefa (fetch sin red) ─────────────────────────────

    const requests = [];
    const portState = {
        mensajes: [
            { id: 1, de: 'Sila', texto: '¿Dónde estás, Nima? Tu ficha sigue en el Archivo.' },
            { id: 2, de: 'Tizón', texto: 'Vi pasar las luces por las Forjas. Iban al norte.' },
        ],
        palomas: [],
        siguiente: 3,
    };
    const REGIONES = ['Valle', 'Forjas', 'Talleres', 'Puerto'];
    const PUESTOS = [
        { id: 1, nombre: 'Tiro al blanco', precio: 2, abierto: true },
        { id: 2, nombre: 'Pan con miel', precio: 1, abierto: true },
        { id: 3, nombre: 'La calesita', precio: 3, abierto: false },
        { id: 4, nombre: 'Títeres de luz', precio: 2, abierto: true },
    ];
    const FICHAS = Array.from({ length: 12 }, (_, i) => ({ id: i + 1, puesto: PUESTOS[i % 4].nombre, valor: (i % 3) + 1 }));
    const json = (status, body, delay = 300, extra = {}) => ({ status, body: JSON.stringify(body), type: 'application/json; charset=utf-8', delay, ...extra });

    const ROUTES = [
        ['GET', '/puerto/hola', () => json(200, { mensaje: '¡Hola, Nima! Te escribe Elefa desde el Puerto.', de: 'Elefa' })],
        ['GET', '/puerto/puestos', () => json(200, PUESTOS, 400)],
        ['GET', '/puerto/puestos/:id', ({ id }) => {
            const puesto = PUESTOS.find((p) => String(p.id) === id);
            return puesto ? json(200, puesto) : json(404, { error: `No hay ningún puesto con el número ${id}.` });
        }],
        ['GET', '/puerto/heroes', () => json(200, [
            { nombre: 'Mia', region: 'Valle de la Serpiente', nivel: 5 },
            { nombre: 'Kira', region: 'Forjas de Hierro', nivel: 6 },
            { nombre: 'Nilo', region: 'Puerto de los Mensajeros', nivel: 4 },
            { nombre: 'Nima', region: 'Feria de las Luces', nivel: 1 },
        ], 500)],
        ['GET', '/puerto/clima', () => json(200, { noche: true, viento: 'suave', temperatura: 18, luciernagas: 120 }, 200)],
        ['GET', '/puerto/mensajes', () => json(200, portState.mensajes)],
        ['POST', '/puerto/mensajes', (params, body) => {
            if (!body || typeof body !== 'object' || !body.texto) return json(422, { error: 'Falta el texto del mensaje.' });
            const mensaje = { id: portState.siguiente++, de: String(body.de ?? 'Nima'), texto: String(body.texto) };
            portState.mensajes.push(mensaje);
            return json(201, mensaje);
        }],
        ['GET', '/puerto/mensajes/:id', ({ id }) => {
            const mensaje = portState.mensajes.find((m) => String(m.id) === id);
            return mensaje ? json(200, mensaje) : json(404, { error: `No hay ningún mensaje con el número ${id}.` });
        }],
        ['PATCH', '/puerto/mensajes/:id', ({ id }, body) => {
            const mensaje = portState.mensajes.find((m) => String(m.id) === id);
            if (!mensaje) return json(404, { error: `No hay ningún mensaje con el número ${id}.` });
            if (!body || typeof body !== 'object' || !body.texto) return json(422, { error: 'Falta el texto del mensaje.' });
            mensaje.texto = String(body.texto);
            return json(200, mensaje);
        }],
        ['DELETE', '/puerto/mensajes/:id', ({ id }) => {
            const at = portState.mensajes.findIndex((m) => String(m.id) === id);
            if (at === -1) return json(404, { error: `No hay ningún mensaje con el número ${id}.` });
            portState.mensajes.splice(at, 1);
            return { status: 204, body: null, type: 'application/json; charset=utf-8', delay: 300 };
        }],
        // El Palomar (Senda S02): las palomas salen solo con la sesión iniciada.
        ['GET', '/puerto/palomas', (params, body, method, cookies) => (/(^|; )sesion=/.test(cookies)
            ? json(200, portState.palomas)
            : json(401, { error: 'Primero iniciá sesión.' }))],
        ['POST', '/puerto/palomas', (params, body, method, cookies) => {
            if (!/(^|; )sesion=/.test(cookies)) return json(401, { error: 'Primero iniciá sesión.' });
            if (!body || typeof body !== 'object' || !body.para || !body.texto) return json(422, { error: 'Una paloma necesita a quién (para) y qué (texto).' });
            if (!REGIONES.includes(body.para)) return json(422, { error: `Las palomas no saben llegar a «${body.para}». Destinos: ${REGIONES.join(', ')}.` });
            const paloma = { id: portState.palomas.length + 1, para: body.para, texto: String(body.texto), vuelo: 1000 * (REGIONES.indexOf(body.para) + 1) };
            portState.palomas.push(paloma);
            return json(201, paloma, 500);
        }],
        ['GET', '/puerto/lento', () => json(200, { mensaje: 'Perdón la demora: la marea estaba alta.' }, 3000)],
        ['GET', '/puerto/error', () => json(500, { error: 'Se cayó una grúa en el muelle. Probá más tarde.' })],
        ['GET', '/puerto/roto', () => ({ status: 200, body: '{"mensaje": "esto se cortó a la mit', type: 'application/json; charset=utf-8', delay: 300 })],
        ['GET', '/puerto/texto', () => ({ status: 200, body: 'Feria de las Luces', type: 'text/plain; charset=utf-8', delay: 200 })],
        ['POST', '/puerto/eco', (params, body, method) => json(200, { recibido: body, metodo: method })],
        ['POST', '/puerto/login', (params, body) => {
            if (body && body.usuario === 'nima' && body.clave === 'luciernaga') {
                return json(200, { ok: true, usuario: 'nima' }, 400, { cookies: ['sesion=farol-7f3a; Max-Age=3600; HttpOnly'] });
            }
            return json(401, { error: 'Usuario o clave incorrectos.' }, 400);
        }],
        ['GET', '/puerto/perfil', (params, body, method, cookies) => (/(^|; )sesion=/.test(cookies)
            ? json(200, { usuario: 'nima', nombre: 'Nima', fichas: 12 })
            : json(401, { error: 'Primero iniciá sesión.' }))],
        ['POST', '/puerto/salir', () => json(200, { ok: true }, 200, { cookies: ['sesion=; Max-Age=0'] })],
        ['GET', '/puerto/fichas', (params, body, method, cookies, query) => {
            const pagina = Math.max(1, Number(query.get('pagina')) || 1);
            return json(200, { pagina, porPagina: 5, total: FICHAS.length, datos: FICHAS.slice((pagina - 1) * 5, pagina * 5) });
        }],
    ];

    function matchRoute(method, path) {
        for (const custom of CONFIG.port ?? []) {
            if (custom.method.toUpperCase() === method && custom.path === path) {
                const body = typeof custom.body === 'string' ? custom.body : JSON.stringify(custom.body ?? null);
                return () => ({ status: custom.status ?? 200, body, type: custom.type ?? 'application/json; charset=utf-8', delay: custom.delay ?? 300 });
            }
        }
        let wrongMethod = null;
        for (const [m, pattern, handler] of ROUTES) {
            const names = [];
            const re = new RegExp('^' + pattern.replace(/:(\w+)/g, (all, name) => { names.push(name); return '([^/]+)'; }) + '/?$');
            const found = path.match(re);
            if (found) {
                const params = Object.fromEntries(names.map((n, i) => [n, decodeURIComponent(found[i + 1])]));
                if (m !== method) {
                    wrongMethod ??= m;
                    continue;
                }
                return (body, cookies, query) => handler(params, body, method, cookies, query);
            }
        }
        return wrongMethod ? () => json(405, { error: `${path} no atiende ${method} (probá con ${wrongMethod}).` }, 200) : null;
    }

    const STATUS = { 200: 'OK', 201: 'Created', 204: 'No Content', 400: 'Bad Request', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found', 405: 'Method Not Allowed', 422: 'Unprocessable Content', 500: 'Internal Server Error', 503: 'Service Unavailable' };

    async function bodyText(body) {
        if (body === undefined || body === null) return null;
        if (typeof body === 'string') return body;
        if (body instanceof URLSearchParams) return body.toString();
        if (body instanceof FormData) return JSON.stringify(Object.fromEntries(body));
        if (body instanceof real.Blob) return body.text();
        return String(body);
    }

    function parseBody(text) {
        if (text === null) return null;
        try {
            return JSON.parse(text);
        } catch {
            const params = new URLSearchParams(text);
            return text.includes('=') ? Object.fromEntries(params) : text;
        }
    }

    async function virtualFetch(resource, init = {}) {
        let url = resource;
        let method = init.method;
        let body = init.body;
        const signal = init.signal ?? (resource instanceof real.Request ? resource.signal : undefined);
        if (resource instanceof real.Request) {
            url = resource.url;
            method ??= resource.method;
            if (body === undefined && !['GET', 'HEAD'].includes(resource.method)) body = await resource.clone().text();
        }
        method = String(method ?? 'GET').toUpperCase();
        let target;
        try {
            target = new real.URL(String(url), document.baseURI);
        } catch {
            throw new TypeError(`Failed to parse URL from ${String(url)}`);
        }
        const path = target.pathname;
        const isPort = (path === '/puerto' || path.startsWith('/puerto/')) && (target.origin === new real.URL(document.baseURI).origin || target.host === 'puerto.feria');
        const request = { method, url: path + target.search, status: '…', sent: Math.round(now), ms: null };
        requests.push(request);
        boardChanged();
        if (signal?.aborted) {
            request.status = 'cancelado';
            throw signal.reason ?? new DOMException('This operation was aborted', 'AbortError');
        }
        if (!isPort) {
            request.status = 'sin red';
            notice('red', `${method} ${target.href}: la caja no tiene internet; usá el Puerto (/puerto/…)`);
            throw new TypeError('Failed to fetch');
        }

        const text = await bodyText(body);
        const handler = matchRoute(method, path.replace(/\/$/, '') || '/');
        let answer = handler
            ? handler(parseBody(text), cookieHeader(), target.searchParams)
            : json(404, { error: `El Puerto no tiene esa dirección: ${path}` }, 200);
        if (target.searchParams.get('falla') === '1') answer = json(503, { error: 'El Puerto está cerrado por tormenta.' });
        const delay = target.searchParams.has('demora') ? Number(target.searchParams.get('demora')) || 0 : answer.delay;

        return new Promise((resolve, reject) => {
            const timer = schedule('timeout', () => {
                signal?.removeEventListener('abort', onAbort);
                for (const cookie of answer.cookies ?? []) setCookie(cookie, true);
                const response = new real.Response(answer.status === 204 ? null : answer.body, {
                    status: answer.status,
                    statusText: STATUS[answer.status] ?? '',
                    headers: { 'content-type': answer.type },
                });
                Object.defineProperty(response, 'url', { value: target.href });
                request.status = answer.status;
                request.ms = delay;
                boardChanged();
                resolve(response);
            }, delay, [], false);
            const onAbort = () => {
                cancel(timer);
                request.status = 'cancelado';
                boardChanged();
                reject(signal.reason ?? new DOMException('This operation was aborted', 'AbortError'));
            };
            signal?.addEventListener('abort', onAbort, { once: true });
        });
    }
    define(window, 'fetch', virtualFetch);

    const noNetwork = (name) => class {
        constructor() {
            throw new Error(`${name} no está en la caja: no hay red. Para pedirle algo al Puerto, usá fetch('/puerto/…').`);
        }
    };
    define(window, 'XMLHttpRequest', noNetwork('XMLHttpRequest'));
    define(window, 'WebSocket', noNetwork('WebSocket'));
    define(window, 'EventSource', noNetwork('EventSource'));
    if (navigator.sendBeacon) define(navigator, 'sendBeacon', () => { notice('red', 'sendBeacon: no hay red'); return false; });

    // ───────────────────────────── El navegador: portapapeles, ubicación, vibración, sonido ─────────────────────────────

    let clipboard = '';
    define(navigator, 'clipboard', {
        writeText: (text) => { clipboard = String(text); notice('portapapeles', `copió «${clipboard}»`); return Promise.resolve(); },
        readText: () => Promise.resolve(clipboard),
    });
    // La Feria está en La Rioja.
    const position = () => ({ coords: { latitude: -29.4131, longitude: -66.8558, accuracy: 20, altitude: null, altitudeAccuracy: null, heading: null, speed: null }, timestamp: START + Math.floor(now) });
    define(navigator, 'geolocation', {
        getCurrentPosition: (ok) => { notice('ubicación', 'pidió la ubicación'); schedule('timeout', () => ok(position()), 200, [], false); },
        watchPosition: (ok) => schedule('timeout', () => ok(position()), 200, [], false),
        clearWatch: cancel,
    });
    define(navigator, 'vibrate', (pattern) => { notice('vibración', `vibró ${JSON.stringify(pattern)}`); return true; });
    define(window, 'Notification', class {
        static permission = 'granted';
        static requestPermission() { return Promise.resolve('granted'); }
        constructor(title, options = {}) { notice('notificación', `${title}${options.body ? ': ' + options.body : ''}`); }
        close() {}
    });
    define(HTMLMediaElement.prototype, 'play', function play() {
        notice('sonido', `suena ${this.currentSrc || this.src || 'un sonido'}`.replace(location.origin, ''));
        return Promise.resolve();
    });
    define(HTMLMediaElement.prototype, 'pause', function pause() {});

    // Los enlaces no sacan de la página (la caja no navega).
    document.addEventListener('click', (event) => {
        const link = event.target instanceof Element ? event.target.closest('a[href]') : null;
        if (!link) return;
        event.preventDefault();
        // Un «#seccion» tampoco: la página de la caja no tiene dirección propia y el salto la recargaría.
        if (link.getAttribute('href').startsWith('#')) {
            const id = decodeURIComponent(link.getAttribute('href').slice(1));
            if (id) document.getElementById(id)?.scrollIntoView();
            return;
        }
        notice('enlace', `iría a ${link.getAttribute('href')} (en la caja no se sale de la página)`);
    }, true);
    // location.href = … (no se puede impedir): se avisa, y la caja la saca.
    let left = false;
    window.addEventListener('beforeunload', () => {
        left = true;
        post('left');
    });
    document.addEventListener('submit', (event) => {
        if (!event.defaultPrevented) notice('formulario', 'se envió un formulario sin preventDefault(): la página se habría recargado');
    });

    // La caja no tiene permiso de formularios, así que el navegador ni siquiera dispara «submit».
    // Se simula el envío: el botón del formulario, Enter en un campo, requestSubmit() y el evento «enviar».
    function submitForm(form, submitter = null) {
        form.dispatchEvent(new SubmitEvent('submit', { bubbles: true, cancelable: true, submitter }));
    }
    define(HTMLFormElement.prototype, 'requestSubmit', function requestSubmit(submitter = null) {
        submitForm(this, submitter);
    });
    define(HTMLFormElement.prototype, 'submit', function submit() {
        notice('formulario', 'form.submit(): la página se habría recargado (sin pasar por el evento submit)');
    });
    const isSubmitter = (el) => el instanceof HTMLButtonElement ? el.type === 'submit' : el instanceof HTMLInputElement && ['submit', 'image'].includes(el.type);
    document.addEventListener('click', (event) => {
        const button = event.target instanceof Element ? event.target.closest('button, input') : null;
        if (event.defaultPrevented || !button || !isSubmitter(button) || !button.form || button.disabled) return;
        event.preventDefault();
        submitForm(button.form, button);
    });
    document.addEventListener('keydown', (event) => {
        const field = event.target;
        if (event.defaultPrevented || event.key !== 'Enter' || !(field instanceof HTMLInputElement) || !field.form) return;
        if (['button', 'checkbox', 'radio', 'submit', 'reset', 'file', 'image'].includes(field.type)) return;
        event.preventDefault();
        submitForm(field.form, field.form.querySelector('button:not([type]), button[type=submit], input[type=submit]'));
    });

    // ───────────────────────────── El lienzo (canvas): lo que se dibuja ─────────────────────────────

    const canvasLogs = new Map();
    // Las transformaciones también se anotan: sin ellas, girar o no girar dejaría el mismo registro.
    const DRAWING = ['fillRect', 'strokeRect', 'clearRect', 'fillText', 'strokeText', 'arc', 'rect', 'ellipse', 'moveTo', 'lineTo', 'fill', 'stroke', 'drawImage', 'save', 'restore', 'translate', 'rotate', 'scale'];
    const STYLED = { fillRect: 'fillStyle', fillText: 'fillStyle', fill: 'fillStyle', strokeRect: 'strokeStyle', strokeText: 'strokeStyle', stroke: 'strokeStyle' };
    const round = (n) => (typeof n === 'number' ? String(Math.round(n * 100) / 100) : typeof n === 'string' ? quote(n) : '…');

    for (const name of DRAWING) {
        const original = CanvasRenderingContext2D.prototype[name];
        if (!original) continue;
        define(CanvasRenderingContext2D.prototype, name, function drawn(...args) {
            const canvas = this.canvas;
            if (!canvasLogs.has(canvas)) canvasLogs.set(canvas, { frame: [], last: [] });
            const log = canvasLogs.get(canvas);
            if (log.frame.length < 500) {
                const shown = name === 'drawImage'
                    ? [`imagen ${String(args[0]?.currentSrc || args[0]?.src || args[0]?.id || '').replace(location.origin + '/', '').split('/').pop() || '…'}`, ...args.slice(1).map(round)]
                    : args.map(round);
                log.frame.push(`${name}(${shown.join(', ')})${STYLED[name] ? ` ${this[STYLED[name]]}` : ''}`);
            }
            return original.apply(this, args);
        });
    }

    function newFrame() {
        for (const log of canvasLogs.values()) {
            if (log.frame.length) {
                log.last = log.frame;
                log.frame = [];
            }
        }
    }

    // ───────────────────────────── El Estado (lo que se compara) ─────────────────────────────

    const squish = (text) => String(text ?? '').replace(/\s+/g, ' ').trim();

    function queryAll(selector) {
        try {
            return [...document.querySelectorAll(selector)].slice(0, 20);
        } catch {
            return null;
        }
    }

    function elementValue(el, attribute) {
        if (attribute === 'value' && 'value' in el) return el.value === '' ? '(vacío)' : String(el.value);
        if (attribute === 'checked' && 'checked' in el) return el.checked ? 'sí' : 'no';
        if (attribute === 'disabled' && 'disabled' in el) return el.disabled ? 'sí' : 'no';
        if (attribute === 'hidden') return el.hidden ? 'sí' : 'no';
        if (!el.hasAttribute(attribute)) return '(no tiene)';
        return squish(el.getAttribute(attribute)) || '(vacío)';
    }

    function stateLines(requests_) {
        const lines = [];
        for (const raw of String(requests_ ?? '').split('\n')) {
            const request = squish(raw);
            if (!request || request.startsWith('//')) continue;
            const words = request.split(' ');
            const head = words[0].toLowerCase();
            const rest = words.slice(1).join(' ');

            if (head === 'cookie' && rest) {
                purgeCookies();
                lines.push(`${request}: ${jar.has(rest) ? jar.get(rest).value || '(vacía)' : '(no hay)'}`);
            } else if (request === 'cookies') {
                purgeCookies();
                lines.push(`${request}: ${jar.size ? [...jar].map(([n, c]) => `${n}=${c.value}${c.httpOnly ? ' (HttpOnly)' : ''}`).join('; ') : '(ninguna)'}`);
            } else if ((head === 'local' || head === 'session') && words.length <= 2) {
                const storage = head === 'local' ? localStorage : sessionStorage;
                const map = storageMaps.get(storage);
                lines.push(rest
                    ? `${request}: ${map.has(rest) ? map.get(rest) : '(no hay)'}`
                    : `${request}: ${map.size ? [...map].map(([k, v]) => `${k}=${v}`).join('; ') : '(vacío)'}`);
            } else if (head === 'lienzo') {
                const canvas = rest ? document.querySelector(rest) : document.querySelector('canvas');
                const log = canvas && canvasLogs.get(canvas);
                const calls = log ? (log.frame.length ? log.frame : log.last) : [];
                if (!canvas) lines.push(`${request}: (no hay lienzo)`);
                else if (!calls.length) lines.push(`${request}: (no dibujó nada)`);
                else for (const call of calls.slice(0, 60)) lines.push(`${request}: ${call}`);
            } else if (request === 'pedidos') {
                if (!requests.length) lines.push(`${request}: (ninguno)`);
                for (const r of requests) lines.push(`${request}: ${r.method} ${r.url} → ${r.status}`);
            } else if (request === 'temporizadores') {
                lines.push(`${request}: ${timers.size}`);
            } else if (request === 'reloj') {
                lines.push(`${request}: ${Math.round(now)} ms`);
            } else if (head === 'estilo') {
                const match = rest.match(/^(.+?)\s*\{\s*([\w-]+)\s*\}$/);
                const el = match && queryAll(match[1])?.[0];
                lines.push(`${request}: ${!match ? '(pedido mal escrito)' : !el ? '(no hay)' : getComputedStyle(el).getPropertyValue(match[2]) || '(vacío)'}`);
            } else if (head === 'título') {
                lines.push(`${request}: ${document.title || '(vacío)'}`);
            } else {
                const count = request.match(/^(.+?)\s+#$/);
                const attribute = request.match(/^(.+?)\s+@([\w:-]+)$/);
                const selector = count ? count[1] : attribute ? attribute[1] : request;
                const found = queryAll(selector);
                if (found === null) lines.push(`${request}: (selector mal escrito)`);
                else if (count) lines.push(`${request}: ${document.querySelectorAll(selector).length}`);
                else if (!found.length) lines.push(`${request}: (no hay)`);
                else for (const el of found) lines.push(`${request}: ${attribute ? elementValue(el, attribute[2]) : squish(el.textContent) || '(vacío)'}`);
            }
        }
        return lines;
    }

    // ───────────────────────────── Los eventos de la consigna ─────────────────────────────

    const KEYS = { espacio: [' ', 'Space'], enter: ['Enter', 'Enter'], escape: ['Escape', 'Escape'], tab: ['Tab', 'Tab'] };
    const keyInfo = (name) => {
        const known = KEYS[name.toLowerCase()];
        if (known) return { key: known[0], code: known[1] };
        if (name.length === 1) return { key: name, code: /[a-z]/i.test(name) ? `Key${name.toUpperCase()}` : /\d/.test(name) ? `Digit${name}` : name };
        return { key: name, code: name };
    };
    const eventProblems = [];

    /** «click canvas 120 80»: si los dos últimos son números, son el punto; el resto es el selector (puede tener espacios). */
    function withPoint(words) {
        const n = words.length;
        if (n >= 3 && /^-?\d+(\.\d+)?$/.test(words[n - 1]) && /^-?\d+(\.\d+)?$/.test(words[n - 2])) {
            return { selector: words.slice(0, -2).join(' '), x: Number(words[n - 2]), y: Number(words[n - 1]) };
        }
        return { selector: words.join(' ') };
    }

    async function runEvent(line) {
        const [verb, ...rest] = squish(line).split(' ');
        const action = verb.toLowerCase();
        const target = (selector) => {
            const el = queryAll(selector)?.[0];
            if (!el) eventProblems.push(`${line}: no hay ningún elemento «${selector}»`);
            return el;
        };
        const mouse = (el, type, x, y) => {
            const box = el.getBoundingClientRect();
            const clientX = box.left + (x === undefined ? box.width / 2 : Number(x));
            const clientY = box.top + (y === undefined ? box.height / 2 : Number(y));
            el.dispatchEvent(new MouseEvent(type, { bubbles: !['mouseenter', 'mouseleave'].includes(type), cancelable: true, clientX, clientY, view: window }));
        };
        const keyboardTarget = () => document.activeElement && document.activeElement !== document.body ? document.activeElement : document.body;
        const key = (type, name) => keyboardTarget().dispatchEvent(new KeyboardEvent(type, { ...keyInfo(name), bubbles: true, cancelable: true }));

        switch (action) {
            case 'click': {
                const { selector, x, y } = withPoint(rest);
                const el = target(selector);
                if (!el) break;
                if (x !== undefined) {
                    mouse(el, 'mousedown', x, y);
                    mouse(el, 'mouseup', x, y);
                    mouse(el, 'click', x, y);
                } else {
                    el.click();
                }
                break;
            }
            case 'doble': { const el = target(rest.join(' ')); if (el) mouse(el, 'dblclick'); break; }
            case 'pasar': { const el = target(rest.join(' ')); if (el) { mouse(el, 'mouseover'); mouse(el, 'mouseenter'); } break; }
            case 'salir': { const el = target(rest.join(' ')); if (el) { mouse(el, 'mouseout'); mouse(el, 'mouseleave'); } break; }
            case 'mover': { const { selector, x, y } = withPoint(rest); const el = target(selector); if (el) mouse(el, 'mousemove', x, y); break; }
            case 'escribir': {
                const el = target(rest[0]);
                if (!el) break;
                el.focus();
                el.value = rest.slice(1).join(' ');
                el.dispatchEvent(new InputEvent('input', { bubbles: true, data: el.value, inputType: 'insertText' }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
                break;
            }
            case 'elegir': {
                const el = target(rest[0]);
                if (!el) break;
                el.value = rest.slice(1).join(' ');
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
                break;
            }
            case 'marcar': { const el = target(rest.join(' ')); if (el) el.click(); break; }
            case 'foco': { const el = target(rest.join(' ')); if (el) el.focus(); break; }
            case 'enviar': {
                const el = target(rest.join(' '));
                const form = el?.closest('form') ?? el;
                if (form) submitForm(form);
                break;
            }
            case 'tecla': key('keydown', rest[0] ?? ''); key('keyup', rest[0] ?? ''); break;
            case 'apretar': key('keydown', rest[0] ?? ''); break;
            case 'soltar': key('keyup', rest[0] ?? ''); break;
            case 'esperar': await advance(now + (Number(rest[0]) || 0)); return;
            case 'cuadros': await advance(now + (Number(rest[0]) || 0) * FRAME); return;
            default: eventProblems.push(`${line}: no conozco el evento «${verb}»`);
        }
        await advance(now);
    }

    // ───────────────────────────── El tablero (lo que se ve al costado) ─────────────────────────────

    function board() {
        purgeCookies();
        return {
            clock: Math.round(now),
            timers: timers.size,
            fired,
            cookies: [...jar].map(([name, c]) => ({ name, value: c.value, httpOnly: c.httpOnly, expires: c.expires === null ? null : Math.round(c.expires) })),
            local: [...storageMaps.get(localStorage)],
            session: [...storageMaps.get(sessionStorage)],
            requests: requests.slice(-50),
            notices: notices.slice(-50),
        };
    }

    let flushPending = false;
    function scheduleFlush() {
        if (flushPending || phase !== 'live') return;
        flushPending = true;
        real.setTimeout(() => {
            flushPending = false;
            post('live', { output: liveOutput, board: board() });
            liveOutput = '';
        }, 120);
    }
    function boardChanged() {
        if (phase === 'live') scheduleFlush();
    }

    // ───────────────────────────── El motor ─────────────────────────────

    function idle() {
        return new Promise((resolve) => {
            const channel = new real.MessageChannel();
            channel.port1.onmessage = () => resolve();
            channel.port2.postMessage(0);
        });
    }

    /** Dispara los temporizadores hasta `until` (en el reloj de la caja), dejando correr las promesas entre uno y otro. */
    async function advance(until, isDone = () => false, isRunning = () => true, jump = true) {
        let quiet = 0;
        for (;;) {
            await idle();
            if (dead || isDone()) break;
            if (real.now() > deadline) {
                timedOut = true;
                stop(`Se cortó a los ${(CONFIG.timeout ?? 5000) / 1000} segundos. ¿Hay algo que no termina?`);
                break;
            }
            const timer = nextTimer();
            if (timer && timer.at <= until) {
                quiet = 0;
                fire(timer);
                continue;
            }
            // Lo que el navegador resuelve solo (leer un Response, un Blob) puede tardar un par de vueltas.
            if (isRunning() && ++quiet > 8) break;
        }
        // «esperar 1000» mueve el reloj aunque no pase nada; el horizonte, solo si quedó algo andando.
        if (!dead && Number.isFinite(until) && (jump || timers.size)) now = Math.max(now, until);
    }

    /** Los otros archivos de la consigna (import … from './vec2.js'): js-instrument.js los renombró a «caja/vec2.js». */
    function loadFiles() {
        const imports = {};
        for (const file of CONFIG.files ?? []) {
            const url = real.createObjectURL(new real.Blob([file.code], { type: 'text/javascript' }));
            scriptOffsets.set(url, { offset: 0, file: file.name });
            imports[`caja/${file.name}`] = url;
        }
        if (!Object.keys(imports).length) return;
        const map = document.createElement('script');
        map.type = 'importmap';
        map.textContent = JSON.stringify({ imports });
        document.head.append(map);
    }

    async function runScripts() {
        loadFiles();
        for (const [index, script] of (CONFIG.scripts ?? []).entries()) {
            if (dead) return;
            const url = real.createObjectURL(new real.Blob([script.code], { type: 'text/javascript' }));
            scriptOffsets.set(url, { offset: script.offset ?? 0, file: null });
            let settled = false;
            import(url).then(() => (settled = true), (error) => {
                settled = true;
                uncaught(error);
            });
            // Mientras el programa espera (un await de un temporizador o del Puerto), el reloj avanza.
            const before = errorCount;
            await advance(Infinity, () => settled, () => started.has(index));
            if (!settled && !dead) {
                notice('espera', `el programa ${CONFIG.scripts.length > 1 ? `(script ${index + 1}) ` : ''}quedó esperando algo que nunca llegó (un await sin respuesta)`);
                stalled = true;
            }
            if (errorCount > before && !settled) break;
        }
    }

    let stalled = false;

    async function main() {
        const started = real.now();
        await runScripts();
        const events = String(CONFIG.events ?? '').split('\n').map(squish).filter((l) => l && !l.startsWith('//'));
        // Sin eventos, el reloj sigue hasta el horizonte (10 s de la Feria): así se ven las animaciones y los avisos.
        if (!dead) await advance(events.length ? now : (CONFIG.horizon ?? 10000), undefined, undefined, false);
        for (const line of events) {
            if (dead) break;
            await runEvent(line);
        }
        // Lo que dejó volando el último evento (un pedido al Puerto, y los que salen de su respuesta) se espera, como
        // en un navegador; los temporizadores no, porque un bucle del juego no termina nunca.
        const flying = () => requests.some((r) => r.status === '…');
        for (let calm = 0; events.length && !dead && calm < 4;) {
            if (flying()) {
                calm = 0;
                await advance(Infinity, () => !flying());
            } else {
                calm++;
                await idle();
            }
        }
        const state = CONFIG.checks ? [...eventProblems.map((p) => `! ${p}`), ...stateLines(CONFIG.checks)].join('\n') : null;
        post('done', {
            output,
            state,
            error: firstError,
            errors: errorCount,
            stopped: stopReason,
            timedOut,
            stalled,
            pending: timers.size,
            board: board(),
            ms: Math.round(real.now() - started),
            clock: Math.round(now),
            left,
        });
        if (CONFIG.live && !dead) goLive();
    }

    // En vivo (la página que se ve): el reloj de la caja sigue al reloj de verdad, y el alumno puede tocar.
    function goLive() {
        phase = 'live';
        const base = now;
        const realBase = real.now();
        const loop = () => {
            deadline = real.now() + 1500;
            if (dead) {
                post('live', { output: liveOutput, board: board(), stopped: stopReason });
                return;
            }
            const until = base + (real.now() - realBase);
            let budget = 2000;
            for (let timer = nextTimer(); timer && timer.at <= until && budget-- > 0 && !dead; timer = nextTimer()) fire(timer);
            now = Math.max(now, until);
            real.raf(loop);
        };
        real.raf(loop);
        post('live', { output: '', board: board() });
    }

    document.addEventListener('DOMContentLoaded', () => {
        main().catch((error) => post('done', { output, state: null, error: describeError(error), board: board(), ms: 0, clock: 0 }));
    });
})();
