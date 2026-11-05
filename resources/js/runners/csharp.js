// Ejecuta C# en el navegador, en un worker con tiempo límite: compilador y runtime en WebAssembly. La primera vez baja
// ~14 MB; después queda en la caché del navegador. El código del alumno nunca se ejecuta en el servidor.
import { explainCsharpErrors, explainCurse } from './csharp-errors.js';

let worker = null;
let loaded = false;
let sequence = 0;

/** Lo que tarda en compilar no cuenta para el programa; tiene su propio tope, generoso (Roslyn corre interpretado). */
const COMPILE_TIMEOUT = 45000;

/**
 * @returns {Promise<{output: string, error: string|null, stderr: string, ms: number, timedOut?: boolean}>}
 */
export async function runCsharp(code, { stdin = '', timeout = 5000, onStatus } = {}) {
    onStatus?.(loaded ? 'Compilando…' : 'Cargando C# (la primera vez baja ~14 MB)…');
    worker ??= new Worker(new URL('../workers/csharp.worker.js', import.meta.url), { type: 'module' });
    const current = worker;
    const id = ++sequence;

    const result = await new Promise((resolve) => {
        let timer = null;
        const cut = (reason) => () => {
            current.terminate();
            if (worker === current) {
                worker = null;
                loaded = false;
            }
            resolve({ type: reason });
        };
        const arm = (ms, reason) => {
            clearTimeout(timer);
            timer = setTimeout(cut(reason), ms);
        };
        if (loaded) arm(COMPILE_TIMEOUT, 'compile-timeout');
        current.onerror = (event) => {
            clearTimeout(timer);
            resolve({ type: 'failed', message: event.message });
        };
        current.onmessage = ({ data }) => {
            if (data.id !== id) return;
            if (data.type === 'loaded') {
                loaded = true;
                onStatus?.('Compilando…');
                arm(COMPILE_TIMEOUT, 'compile-timeout');
                return;
            }
            if (data.type === 'compiled') {
                onStatus?.('Ejecutando…');
                arm(timeout, 'timeout');
                return;
            }
            clearTimeout(timer);
            resolve(data);
        };
        current.postMessage({ id, code, stdin });
    });

    if (result.type === 'timeout') {
        return { output: '', error: `Se cortó a los ${timeout / 1000} segundos. ¿Hay un bucle que no termina?`, stderr: '', ms: timeout, timedOut: true };
    }
    if (result.type === 'compile-timeout') {
        return { output: '', error: 'El compilador tardó demasiado. Probá ejecutar de nuevo.', stderr: '', ms: COMPILE_TIMEOUT, timedOut: true };
    }
    if (result.type === 'failed') {
        current.terminate();
        if (worker === current) {
            worker = null;
            loaded = false;
        }

        return { output: '', error: `No se pudo ejecutar C#: ${result.message}`, stderr: '', ms: 0, unavailable: true };
    }
    if (!result.compiled) {
        return { output: '', error: explainCsharpErrors(result.errors), stderr: '', ms: result.ms };
    }

    return {
        output: result.output,
        error: result.curse ? explainCurse(result.curse) : null,
        stderr: (result.warnings ?? []).join('\n'),
        ms: result.ms,
    };
}
