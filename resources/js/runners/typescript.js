// TypeScript en el navegador de quien ejecuta (D115, fase 5). Dos pasos, ninguno en el servidor:
// 1. el compilador revisa los tipos en un Web Worker (workers/typescript.worker.js); si una pieza no encaja, el
//    programa NO se ejecuta y se explica el error en español;
// 2. el JavaScript que sale corre en la misma caja que JavaScript (js-caja.js: sin mismo origen, sin red, con el
//    mundo virtual), así que consola, página, eventos, lienzo y el Puerto andan igual.
// Las micro-misiones de tipo Compilador (`#### Compilador` en el .md) no ejecutan: su salida son los errores.
import { runJavaScript } from './javascript.js';
import { TS_BASE, TS_VERSION } from './typescript-config.js';
import { explainTypeErrors, summarizeTypeErrors } from './ts-errors.js';

/** Lo que tarda en bajar y revisar no cuenta para el programa: tiene su propio tope, generoso. */
const COMPILE_TIMEOUT = 60000;

let worker = null;
let loaded = false;
let sequence = 0;

function compileInWorker(files, onStatus) {
    worker ??= new Worker(new URL('../workers/typescript.worker.js', import.meta.url), { type: 'module' });
    const current = worker;
    const id = ++sequence;
    onStatus?.(loaded ? 'Revisando los tipos…' : 'Cargando TypeScript (la primera vez baja ~2 MB)…');

    return new Promise((resolve) => {
        const timer = setTimeout(() => {
            current.terminate();
            if (worker === current) {
                worker = null;
                loaded = false;
            }
            resolve({ type: 'failed', message: `El compilador no terminó en ${COMPILE_TIMEOUT / 1000} segundos.` });
        }, COMPILE_TIMEOUT);
        current.onerror = (event) => {
            clearTimeout(timer);
            resolve({ type: 'failed', message: event.message ?? 'el compilador no arrancó' });
        };
        current.onmessage = ({ data }) => {
            if (data.id !== id) return;
            if (data.type === 'loaded') {
                loaded = true;
                onStatus?.('Revisando los tipos…');
                return;
            }
            clearTimeout(timer);
            resolve(data);
        };
        current.postMessage({ id, files, base: TS_BASE, version: TS_VERSION });
    });
}

/** Del JavaScript al TypeScript: «línea N» (y «línea N de vec2.js») pasa a ser la línea del archivo .ts. */
function remap(text, maps) {
    if (!text) return text;

    return text.replace(/línea (\d+)(?: de ([\w.-]+\.js))?/g, (all, line, file) => {
        const original = maps[file ?? 'main.js']?.[Number(line)];
        return original ? `línea ${original}${file ? ` de ${file.replace(/\.js$/, '.ts')}` : ''}` : all;
    });
}

/**
 * @param {string} code el TypeScript del alumno (main.ts)
 * @param {object} options los de runJavaScript (js-caja.js), más `compiler` (micro-misión de tipo Compilador) y
 *   `onStatus`. Los `files` de la consigna son módulos .ts que el código importa con './nombre.js'.
 */
export async function runTypeScript(code, options = {}) {
    const started = performance.now();
    const sources = { 'main.ts': code };
    for (const [name, text] of Object.entries(options.files ?? {})) sources[name.replace(/\.js$/, '.ts')] = text;

    const compiled = await compileInWorker(sources, options.onStatus);
    const ms = Math.round(performance.now() - started);
    const empty = { stderr: '', ms, state: null, board: null, notes: [] };

    if (compiled.type === 'failed') {
        return { ...empty, output: '', error: `✗ No se pudo cargar el compilador de TypeScript: ${compiled.message}\n  Revisá la conexión y probá de nuevo.`, line: null };
    }
    const errors = compiled.diagnostics;
    const firstLine = errors.find((d) => d.file === 'main.ts')?.line ?? null;

    // Micro-misión de tipo Compilador: lo que se compara son los errores (o «Compila sin errores»).
    if (options.compiler) {
        return { ...empty, output: summarizeTypeErrors(errors), error: null, line: firstLine, typeErrors: errors };
    }
    if (errors.length) {
        return { ...empty, output: '', error: explainTypeErrors(errors), line: firstLine, typeErrors: errors, syntax: true };
    }

    const files = {};
    for (const name of Object.keys(sources)) {
        if (name !== 'main.ts') files[name.replace(/\.ts$/, '.js')] = compiled.js[name.replace(/\.ts$/, '.js')] ?? '';
    }
    options.onStatus?.('Ejecutando…');
    const result = await runJavaScript(compiled.js['main.js'] ?? '', { ...options, files });

    return {
        ...result,
        error: remap(result.error, compiled.maps),
        line: result.line ? (compiled.maps['main.js']?.[result.line] ?? result.line) : null,
        ms: result.ms + ms,
    };
}

export { stopCaja } from './javascript.js';
