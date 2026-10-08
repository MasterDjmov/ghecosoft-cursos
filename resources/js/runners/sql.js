// Ejecuta SQL en el navegador (SQLite en WebAssembly) para las micro-misiones de SQL, en un worker con tiempo
// límite. La primera vez baja SQLite (~1 MB del sitio); después queda en la caché del navegador.

let worker = null;
let loaded = false;
let sequence = 0;

/**
 * @returns {Promise<{output: string, error: string|null, ms: number, timedOut?: boolean, unavailable?: boolean}>}
 */
export async function runSql(code, { timeout = 5000, onStatus } = {}) {
    onStatus?.(loaded ? 'Ejecutando…' : 'Cargando SQLite (la primera vez tarda un poco)…');
    worker ??= new Worker(new URL('../workers/sql.worker.js', import.meta.url), { type: 'module' });
    const current = worker;
    const id = ++sequence;

    const result = await new Promise((resolve) => {
        let timer = null;
        const cut = () => {
            current.terminate();
            if (worker === current) worker = null;
            resolve({ type: 'timeout' });
        };
        // El tiempo corre desde que SQLite está cargado, no durante la descarga.
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
        current.postMessage({ id, code });
    });

    if (result.type === 'timeout') {
        return { output: '', error: `Se cortó a los ${timeout / 1000} segundos. ¿Hay una consulta que no termina?`, ms: timeout, timedOut: true };
    }
    if (result.type === 'failed') {
        current.terminate();
        if (worker === current) worker = null;
        return { output: '', error: `No se pudo cargar SQLite: ${result.message}`, ms: 0, unavailable: true };
    }

    return { output: result.output, error: result.error, ms: result.ms };
}
