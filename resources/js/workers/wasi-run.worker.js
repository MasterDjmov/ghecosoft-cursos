// Ejecuta un programa WebAssembly (WASI) compilado en el navegador, con la entrada de ejemplo (D66, D98).
// Vive en su propio worker: si no termina, se lo corta sin perder el compilador.
import { WASI, File, OpenFile, ConsoleStdout, PreopenDirectory } from '@bjorn3/browser_wasi_shim';

self.onmessage = async ({ data: { id, wasm, stdin } }) => {
    const decoder = new TextDecoder();
    let output = '';
    let errors = '';
    const fds = [
        new OpenFile(new File(new TextEncoder().encode(stdin ?? ''))),
        new ConsoleStdout((b) => { output += decoder.decode(b, { stream: true }); }),
        new ConsoleStdout((b) => { errors += decoder.decode(b, { stream: true }); }),
        // Una carpeta vacía en memoria para fopen (archivos de texto y binarios, D98): nace y muere con la ejecución.
        new PreopenDirectory('.', new Map()),
    ];
    const started = performance.now();
    try {
        const wasi = new WASI(['programa'], [], fds);
        const module = await WebAssembly.compile(wasm);
        const instance = await WebAssembly.instantiate(module, { wasi_snapshot_preview1: wasi.wasiImport });
        const exit = wasi.start(instance);
        self.postMessage({ id, output, errors, exit, ms: Math.round(performance.now() - started) });
    } catch (e) {
        self.postMessage({ id, output, errors: errors + String(e?.message ?? e), exit: 1, ms: Math.round(performance.now() - started), crashed: true });
    }
};
