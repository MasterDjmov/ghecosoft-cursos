// El compilador de TypeScript en un Web Worker (D115, fase 5): revisa los tipos y pasa el código a JavaScript, en el
// navegador de quien ejecuta. No ejecuta nada: el JavaScript que sale lo corre la caja de la Feria (js-caja.js).
// La primera vez baja el compilador (~2 MB comprimido, de public/toolchains/typescript); después queda en memoria.
import { compile } from '../runners/ts-compile.js';

let ts = null;
let libs = null;

async function download(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`No se pudo bajar ${url} (${response.status}).`);
    let bytes = new Uint8Array(await response.arrayBuffer());
    // Algunos servidores mandan el .gz con Content-Encoding y el navegador ya lo descomprimió.
    if (bytes[0] === 0x1f && bytes[1] === 0x8b) {
        bytes = new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer());
    }

    return new TextDecoder().decode(bytes);
}

async function load(base, version) {
    const [compiler, lib, spanish] = await Promise.all([
        download(`${base}/typescript-${version}.js.gz`),
        download(`${base}/libs-${version}.json.gz`),
        download(`${base}/es-${version}.json.gz`),
    ]);
    // typescript.js arma `var ts`: se evalúa en su propia función y se devuelve.
    // eslint-disable-next-line no-new-func
    ts = new Function(`${compiler}\nreturn ts;`)();
    libs = JSON.parse(lib);
    ts.setLocalizedDiagnosticMessages(JSON.parse(spanish));
}

self.onmessage = async ({ data }) => {
    const { id, files, base, version } = data;
    try {
        if (!ts) {
            await load(base, version);
            self.postMessage({ id, type: 'loaded' });
        }
        const started = performance.now();
        const result = compile(ts, libs, files);
        self.postMessage({ id, type: 'done', ...result, ms: Math.round(performance.now() - started) });
    } catch (error) {
        self.postMessage({ id, type: 'failed', message: String(error?.message ?? error) });
    }
};
