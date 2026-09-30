// Ejecuta C++ en el navegador del docente (D66): compila en un worker (Clang en WebAssembly) y corre el
// programa en otro, con tiempo límite. La primera vez baja el compilador (~105 MB del CDN) y la biblioteca
// (~20 MB del sitio); después queda en la caché del navegador. Solo para corregir: el código del alumno
// nunca se ejecuta en el servidor.

let compiler = null;
let loaded = false;
let sequence = 0;

function getCompiler() {
    compiler ??= new Worker(new URL('../workers/cpp-compile.worker.js', import.meta.url), { type: 'module' });
    return compiler;
}

function compile(code, language, onLoaded) {
    const id = ++sequence;
    const worker = getCompiler();

    return new Promise((resolve) => {
        worker.onmessage = ({ data }) => {
            if (data.id !== id) return;
            if (data.type === 'loaded') {
                if (!loaded) onLoaded?.();
                loaded = true;
                return;
            }
            if (data.type === 'loadFailed') {
                worker.terminate();
                compiler = null;
            }
            resolve(data);
        };
        worker.postMessage({ id, code, language });
    });
}

function execute(wasm, stdin, timeout) {
    const worker = new Worker(new URL('../workers/wasi-run.worker.js', import.meta.url), { type: 'module' });

    return new Promise((resolve) => {
        const timer = setTimeout(() => {
            worker.terminate();
            resolve({ output: '', errors: '', timedOut: true, ms: timeout });
        }, timeout);
        worker.onmessage = ({ data }) => {
            clearTimeout(timer);
            worker.terminate();
            resolve(data);
        };
        worker.postMessage({ id: 1, wasm, stdin });
    });
}

/**
 * @returns {Promise<{output: string, error: string|null, diagnostics: string, ms: number, timedOut?: boolean}>}
 */
export async function runCpp(code, { stdin = '', timeout = 5000, language = 'cpp', onStatus } = {}) {
    onStatus?.(loaded ? 'Compilando…' : 'Cargando el compilador (la primera vez baja ~120 MB y tarda)…');
    const compiled = await compile(code, language, () => onStatus?.('Compilando…'));

    if (compiled.type === 'loadFailed') {
        return { output: '', error: `No se pudo cargar el compilador: ${compiled.message}`, diagnostics: '', ms: 0 };
    }
    if (compiled.type === 'compileError') {
        return { output: '', error: 'No compila.', diagnostics: compiled.diagnostics, ms: 0, compileError: true };
    }

    onStatus?.('Ejecutando…');
    const result = await execute(compiled.wasm, stdin, timeout);
    if (result.timedOut) {
        return { output: '', error: `Se cortó a los ${timeout / 1000} segundos. ¿Hay un bucle que no termina?`, diagnostics: compiled.diagnostics, ms: timeout, timedOut: true };
    }
    const error = result.crashed
        ? `El programa se cortó: ${result.errors.trim()}`
        : result.exit !== 0 ? `El programa terminó con código ${result.exit}.${result.errors ? '\n' + result.errors.trim() : ''}` : null;

    return { output: result.output, error, diagnostics: compiled.diagnostics, stderr: result.exit === 0 ? result.errors : '', ms: result.ms };
}

export function isCppLoaded() {
    return loaded;
}
