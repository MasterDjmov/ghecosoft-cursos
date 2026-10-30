// La caja de JavaScript (D115): arma el <iframe sandbox="allow-scripts"> SIN allow-same-origin (origen opaco: no ve
// las cookies ni la sesión de quien ejecuta, ni la página de afuera), con una CSP sin red, y le pasa el mundo virtual
// (js-sandbox/world.js) y el código ya preparado (js-instrument.js). Nunca se le agrega otro permiso al sandbox.
// Lo usa javascript.js en la plataforma y scripts/js-micro/ en las pruebas con Chrome; el mundo llega como texto.
import { instrument, splitPage } from './js-instrument.js';
import { explainError } from './js-errors.js';

const STATE_HEADER = '── Estado ──';
const LEFT = '✗ La página intentó irse a otra dirección (location.href = …): en la caja no se sale de la página.';

function policy(origin) {
    return [
        "default-src 'none'",
        "script-src 'unsafe-inline' blob:",
        "style-src 'unsafe-inline' https://fonts.googleapis.com",
        'font-src https://fonts.gstatic.com data:',
        `img-src ${origin} data: blob:`,
        `media-src ${origin} data: blob:`,
        "connect-src 'none'",
        "form-action 'none'",
        `base-uri ${origin}`,
    ].join('; ');
}

/** La página de la consigna (o la del alumno), con la política, la configuración y el mundo primero. */
function document_(world, page, config, origin) {
    const html = String(page ?? '');
    const head = html.match(/<head\b[^>]*>([\s\S]*?)<\/head>/i)?.[1] ?? '';
    const bodyMatch = html.match(/<body\b([^>]*)>([\s\S]*?)(<\/body>|$)/i);
    const body = bodyMatch ? bodyMatch[2] : /<html\b/i.test(html) ? '' : html;
    const bodyAttributes = bodyMatch ? bodyMatch[1] : '';
    const json = JSON.stringify(config).replace(/</g, '\\u003c');

    return '<!doctype html><html lang="es"><head><meta charset="utf-8">'
        + `<meta http-equiv="Content-Security-Policy" content="${policy(origin)}">`
        + `<meta name="viewport" content="width=device-width, initial-scale=1"><base href="${origin}/">`
        + `<script type="application/json" id="caja-config">${json}</script>`
        + `<script>${world}</script>${head}</head><body${bodyAttributes}>${body}</body></html>`;
}

let running = null;
// La página en vivo deja escuchando sus mensajes: al sacarla, se deja de escuchar.
const listeners = new WeakMap();

/** Saca la caja que esté corriendo en ese lugar (o la de la última ejecución en segundo plano). */
export function stopCaja(container = null) {
    const frame = container ? container.querySelector('iframe[data-caja]') : running;
    if (!frame) return;
    frame.remove();
    window.removeEventListener('message', listeners.get(frame));
    if (frame === running) running = null;
}

/**
 * Ejecuta el código del alumno en la caja.
 *
 * @param {string} world el texto de js-sandbox/world.js
 * @param {string} code JavaScript, o una página HTML entera con sus <script>
 * @param {object} options { stdin, page, events, checks, seed, horizon, timeout, storage, cookies, port, container,
 *   onLive(output, board, stopped), onLiveError(text) }
 * @returns {Promise<{output: string, error: string|null, stderr: string, ms: number, timedOut?: boolean, state: string|null,
 *   board: object|null, notes: string[], line: number|null}>}
 */
export function execute(world, code, options = {}) {
    const started = performance.now();
    const split = splitPage(code);
    const page = split.page ?? options.page ?? '';
    const scripts = [];
    // Los otros archivos de la consigna (módulos que el código importa con './nombre.js').
    const names = Object.keys(options.files ?? {});
    const files = [];
    const sources = [...names.map((name) => ({ code: options.files[name], offset: 0, file: name })), ...split.scripts];
    for (const [index, script] of sources.entries()) {
        const prepared = instrument(script.code, script.file ? -1 : index - names.length, names);
        if (prepared.error) {
            const line = prepared.error.line + script.offset;
            return Promise.resolve({
                output: '',
                error: `✗ Error de escritura en la línea ${line}${script.file ? ` de ${script.file}` : ''}: ${prepared.error.message}\n  (SyntaxError: ${prepared.error.original})`,
                stderr: '',
                ms: Math.round(performance.now() - started),
                state: null,
                board: null,
                notes: [],
                line,
                syntax: true,
            });
        }
        if (script.file) files.push({ name: script.file, code: prepared.code });
        else scripts.push({ code: prepared.code, offset: script.offset });
    }

    const origin = options.origin ?? window.location.origin;
    const token = Math.random().toString(36).slice(2) + Date.now().toString(36);
    const timeout = options.timeout ?? 5000;
    const live = Boolean(options.container);
    const config = {
        token,
        scripts,
        files,
        stdin: options.stdin ?? '',
        events: options.events ?? '',
        checks: options.checks ?? '',
        seed: options.seed,
        horizon: options.horizon,
        timeout,
        storage: options.storage,
        cookies: options.cookies,
        port: options.port,
        live,
    };

    const frame = document.createElement('iframe');
    frame.dataset.caja = '';
    frame.setAttribute('sandbox', 'allow-scripts');
    frame.setAttribute('referrerpolicy', 'no-referrer');
    frame.title = 'Página del programa';
    if (live) {
        stopCaja(options.container);
        frame.className = 'h-full w-full bg-white';
        options.container.append(frame);
    } else {
        stopCaja();
        running = frame;
        frame.setAttribute('aria-hidden', 'true');
        frame.tabIndex = -1;
        frame.style.cssText = 'position:fixed;left:-10000px;top:0;width:800px;height:600px;border:0;';
        document.body.append(frame);
    }

    const notes = split.skipped.map((src) => `No se cargó ${src}: la caja no trae scripts de afuera.`);

    return new Promise((resolve) => {
        let finished = false;
        let loads = 0;
        const finish = (result) => {
            if (finished) return;
            finished = true;
            clearTimeout(watchdog);
            if (!live) {
                window.removeEventListener('message', onMessage);
                frame.remove();
                if (running === frame) running = null;
            }
            resolve(result);
        };
        const failed = (error, extra = {}) => finish({ output: '', error, stderr: '', ms: Math.round(performance.now() - started), state: null, board: null, notes, line: null, ...extra });

        const onMessage = (event) => {
            if (event.source !== frame.contentWindow || event.data?.caja !== token) return;
            const data = event.data;
            if (data.type === 'live') {
                options.onLive?.(data.output ?? '', data.board ?? null, data.stopped ?? null);
                return;
            }
            if (data.type === 'error') {
                options.onLiveError?.(explainError(data.error));
                return;
            }
            if (data.type === 'left') {
                frame.remove();
                failed(LEFT);
                return;
            }
            if (data.type !== 'done') return;
            if (data.left) return failed(LEFT);
            if (data.stalled) notes.push('El programa quedó esperando algo que nunca llegó (un await sin respuesta).');
            // Con la página en vivo, que algo siga andando (un juego, una animación) es lo esperable.
            if (data.pending && !data.stopped && !live) notes.push(`Al terminar ${data.pending > 1 ? `quedaron ${data.pending} temporizadores` : 'quedó 1 temporizador'} andando (el reloj de la caja llegó a ${(data.clock / 1000).toLocaleString('es-AR')} s).`);
            if (data.errors > 1) notes.push(`Hubo ${data.errors} errores; se muestra el primero.`);
            let output = data.output ?? '';
            if (data.state !== null && data.state !== undefined) {
                output = `${output.replace(/\n+$/, '')}${output.trim() ? '\n' : ''}${STATE_HEADER}\n${data.state}`;
            }
            const error = data.stopped ? data.stopped : data.error ? explainError(data.error) : null;
            finish({
                output: output.replace(/\n+$/, ''),
                error,
                stderr: '',
                ms: data.ms,
                timedOut: Boolean(data.timedOut),
                state: data.state ?? null,
                board: data.board ?? null,
                notes,
                line: data.error?.file ? null : data.error?.line ?? null,
                clock: data.clock,
            });
        };
        window.addEventListener('message', onMessage);
        listeners.set(frame, onMessage);
        // Si la página se va a otra dirección (location.href = …), ya no es la caja: se la saca.
        frame.addEventListener('load', () => {
            if (++loads > 1) {
                frame.remove();
                failed(LEFT);
            }
        });
        const watchdog = setTimeout(() => {
            frame.remove();
            failed(`Se cortó a los ${timeout / 1000} segundos. ¿Hay un bucle que no termina?`, { timedOut: true });
        }, timeout + 3000);

        frame.srcdoc = document_(world, page, config, origin);
    });
}
