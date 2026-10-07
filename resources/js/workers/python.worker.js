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
        // numpy, pandas… (Senda del Reino): se bajan de la misma distribución oficial de Pyodide, solo la
        // primera vez, y antes de avisar «listo» para que la descarga no cuente en el tiempo límite.
        await pyodide.loadPackagesFromImports(code);
        // Importarlos también antes (pandas tarda varios segundos en importarse): solo los que vinieron de la
        // distribución, por su nombre de paquete.
        for (const name of Object.keys(pyodide.loadedPackages)) {
            if (/^[a-z_][a-z0-9_]*$/.test(name)) {
                try {
                    pyodide.runPython(`import ${name}`);
                } catch {
                    // Hay paquetes cuyo módulo se llama distinto: se importan cuando el programa los pida.
                }
            }
        }
        self.postMessage({ id, type: 'ready' });

        let output = '';
        let truncated = false;
        // Salida cruda (no "por líneas"): así el texto de input("Nivel: ") queda en la misma
        // línea que lo que sigue, igual que en la terminal, y se puede comparar con la esperada.
        const decoder = new TextDecoder();
        const write = (buffer) => {
            if (output.length > MAX_OUTPUT) {
                truncated = true;
            } else {
                output += decoder.decode(buffer, { stream: true });
            }
            return buffer.length;
        };
        pyodide.setStdout({ write });
        pyodide.setStderr({ write });

        const lines = String(stdin ?? '').split('\n');
        if (lines.at(-1) === '') lines.pop();
        pyodide.setStdin({ stdin: () => (lines.length ? lines.shift() : null) });

        // Cada ejecución arranca con variables limpias.
        const globals = pyodide.globals.get('dict')();
        // Como en la terminal: el programa es "__main__" (para el clásico if __name__ == "__main__":).
        globals.set('__name__', '__main__');
        const started = performance.now();
        let error = null;
        try {
            await pyodide.runPythonAsync(code, { globals });
        } catch (e) {
            error = cleanError(e.message);
        } finally {
            globals.destroy();
            // Lo último sin salto de línea (print(..., end="")) queda en el buffer: sacarlo ahora,
            // o aparecería al principio de la próxima ejecución.
            pyodide.runPython('import sys\nsys.stdout.flush()\nsys.stderr.flush()');
        }

        if (truncated) output += '\n… (la salida es muy larga: se cortó)';
        self.postMessage({ id, type: 'done', output, error, ms: Math.round(performance.now() - started) });
    } catch (e) {
        self.postMessage({ id, type: 'done', output: '', error: `No se pudo cargar Python: ${e.message}`, ms: 0, loadFailed: true });
    }
};
