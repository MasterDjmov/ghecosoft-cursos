// Web Worker que ejecuta Python con Pyodide. El código del alumno corre acá,
// en su navegador: nunca en el servidor.

let pyodidePromise = null;

const MAX_OUTPUT = 20000;

function load(url) {
    pyodidePromise ??= import(/* @vite-ignore */ `${url}pyodide.mjs`).then(({ loadPyodide }) => loadPyodide({ indexURL: url }));
    return pyodidePromise;
}

/** Deja solo la parte del error que importa: lo del programa del alumno. */
function cleanError(message) {
    const lines = String(message).split('\n');
    const start = lines.findIndex((line) => line.includes('File "<exec>"'));
    const relevant = start === -1 ? lines.slice(-3) : ['Traceback (most recent call last):', ...lines.slice(start)];
    return relevant.join('\n').trim();
}

self.onmessage = async ({ data }) => {
    const { id, code, stdin, url } = data;

    try {
        const pyodide = await load(url);
        self.postMessage({ id, type: 'ready' });

        let output = '';
        let truncated = false;
        const write = (text) => {
            if (output.length > MAX_OUTPUT) {
                truncated = true;
                return;
            }
            output += text + '\n';
        };
        pyodide.setStdout({ batched: write });
        pyodide.setStderr({ batched: write });

        const lines = String(stdin ?? '').split('\n');
        if (lines.at(-1) === '') lines.pop();
        pyodide.setStdin({ stdin: () => (lines.length ? lines.shift() : null) });

        // Cada ejecución arranca con variables limpias.
        const globals = pyodide.globals.get('dict')();
        const started = performance.now();
        let error = null;
        try {
            await pyodide.runPythonAsync(code, { globals });
        } catch (e) {
            error = cleanError(e.message);
        } finally {
            globals.destroy();
        }

        if (truncated) output += '\n… (la salida es muy larga: se cortó)';
        self.postMessage({ id, type: 'done', output, error, ms: Math.round(performance.now() - started) });
    } catch (e) {
        self.postMessage({ id, type: 'done', output: '', error: `No se pudo cargar Python: ${e.message}`, ms: 0, loadFailed: true });
    }
};
