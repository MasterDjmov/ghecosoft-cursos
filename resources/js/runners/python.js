// Ejecuta Python en un Web Worker con Pyodide (D5). Si el programa tarda más
// del límite (un while True, por ejemplo), se mata el worker y se crea otro.

let worker = null;
let loaded = false;
let sequence = 0;

function getWorker() {
    worker ??= new Worker(new URL('../workers/python.worker.js', import.meta.url), { type: 'module' });
    return worker;
}

/**
 * @returns {Promise<{output: string, error: string|null, ms: number, timedOut?: boolean}>}
 */
export function runPython(code, { stdin = '', url, timeout = 5000, onReady } = {}) {
    const id = ++sequence;
    const current = getWorker();

    return new Promise((resolve) => {
        let timer = null;
        // El primer uso descarga Python (~10 MB): el reloj arranca cuando está listo.
        const startTimer = () => {
            timer = setTimeout(() => {
                current.terminate();
                worker = null;
                loaded = false;
                resolve({ output: '', error: `Se cortó a los ${timeout / 1000} segundos. ¿Hay un bucle que no termina?`, ms: timeout, timedOut: true });
            }, timeout);
        };

        current.onmessage = ({ data }) => {
            if (data.id !== id) return;
            if (data.type === 'ready') {
                if (!loaded) onReady?.();
                loaded = true;
                startTimer();
                return;
            }
            clearTimeout(timer);
            if (data.loadFailed) {
                current.terminate();
                worker = null;
            }
            resolve(data);
        };

        current.postMessage({ id, code, stdin, url });
    });
}

export function isPythonLoaded() {
    return loaded;
}
