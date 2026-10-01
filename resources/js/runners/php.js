// Ejecuta PHP en el navegador del docente (D68), en un worker con tiempo límite. La primera vez baja PHP
// (~7 MB del sitio); después queda en la caché del navegador. Solo para corregir: el código del alumno
// nunca se ejecuta en el servidor.

let worker = null;
let loaded = false;
let sequence = 0;

/**
 * @returns {Promise<{output: string, error: string|null, stderr: string, ms: number, timedOut?: boolean}>}
 */
export async function runPhp(code, { stdin = '', timeout = 5000, onStatus } = {}) {
    onStatus?.(loaded ? 'Ejecutando…' : 'Cargando PHP (la primera vez baja ~7 MB)…');
    worker ??= new Worker(new URL('../workers/php.worker.js', import.meta.url), { type: 'module' });
    const current = worker;
    const id = ++sequence;

    const result = await new Promise((resolve) => {
        let timer = null;
        const cut = () => {
            current.terminate();
            if (worker === current) worker = null;
            resolve({ type: 'timeout' });
        };
        // El tiempo corre desde que PHP está cargado, no durante la descarga.
        if (loaded) timer = setTimeout(cut, timeout);
        current.onmessage = ({ data }) => {
            if (data.id !== id) return;
            if (data.type === 'loaded') {
                loaded = true;
                onStatus?.('Ejecutando…');
                timer ??= setTimeout(cut, timeout);
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
    if (result.type === 'failed') {
        current.terminate();
        if (worker === current) worker = null;
        return { output: '', error: `No se pudo ejecutar PHP: ${result.message}`, stderr: '', ms: 0, unavailable: true };
    }
    const errors = (result.errors ?? '').trim();
    const error = result.exit !== 0 ? `El programa terminó con código ${result.exit}.${errors ? '\n' + errors : ''}` : null;

    return { output: result.output, error, stderr: result.exit === 0 ? errors : '', ms: result.ms };
}
