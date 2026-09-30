// Ejecuta PHP de consola en el navegador del docente (D68): PHP 8.3 compilado a WebAssembly (@php-wasm).
// El .wasm (~18 MB, ~7 MB comprimido) sale de public/toolchains/php. Un envoltorio da STDIN (la entrada de
// ejemplo), STDOUT, STDERR, readline() y $argv como en la terminal.
import { PHP, PHPResponse, loadPHPRuntime } from '@php-wasm/universal';
import * as loader from 'php-wasm-8-3-loader';
import { PHP_WASM_URL } from '../runners/php-config.js';

async function gunzip(response) {
    if (!response.ok) throw new Error(`No se pudo bajar ${response.url} (${response.status})`);
    const bytes = new Uint8Array(await response.arrayBuffer());
    // Algunos servidores mandan el .gz con Content-Encoding y el navegador ya lo descomprimió.
    if (bytes[0] !== 0x1f || bytes[1] !== 0x8b) return bytes;
    return new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer());
}

const WRAPPER = `<?php
// Como php en la terminal: los avisos y errores salen una vez, junto con la salida.
ini_set('display_errors', '1');
ini_set('log_errors', '0');
ini_set('html_errors', '0');
error_reporting(E_ALL);
date_default_timezone_set('America/Argentina/Buenos_Aires');
define('STDIN', fopen('/tmp/entrada.txt', 'r'));
define('STDOUT', fopen('php://output', 'w'));
define('STDERR', fopen('php://stderr', 'w'));
if (!function_exists('readline')) {
    function readline(?string $prompt = null): string|false
    {
        if ($prompt !== null) {
            echo $prompt;
        }
        $line = fgets(STDIN);

        return $line === false ? false : rtrim($line, "\\r\\n");
    }
}
$argv = ['main.php'];
$argc = 1;
require '/tmp/main.php';
`;

let php = null;

async function load() {
    globalThis.setImmediate ??= (fn) => setTimeout(fn, 0);
    const wasm = await fetch(PHP_WASM_URL).then(gunzip);
    const runtime = await loadPHPRuntime(loader, {
        phpWasmAsyncMode: 'asyncify',
        // Sin red: los sockets no hacen nada.
        websocket: { decorator: (Socket) => class extends Socket { constructor() { try { super(); } catch { /* sin red */ } } send() { return null; } } },
        instantiateWasm(imports, receive) {
            WebAssembly.instantiate(wasm, imports).then(({ instance, module }) => receive(instance, module));
            return {};
        },
    });
    return new PHP(runtime);
}

self.onmessage = async ({ data: { id, code, stdin } }) => {
    try {
        php ??= load();
        const instance = await php;
        self.postMessage({ id, type: 'loaded' });

        instance.writeFile('/tmp/main.php', code);
        instance.writeFile('/tmp/entrada.txt', stdin ?? '');
        instance.writeFile('/tmp/envoltorio.php', WRAPPER);
        const started = performance.now();
        // runStream (no run): con un error fatal, run() tira una excepción en vez de devolver la salida.
        const response = await PHPResponse.fromStreamedResponse(await instance.runStream({ scriptPath: '/tmp/envoltorio.php' }));
        self.postMessage({ id, type: 'done', output: response.text, errors: response.errors, exit: response.exitCode, ms: Math.round(performance.now() - started) });
    } catch (e) {
        php = null;
        self.postMessage({ id, type: 'failed', message: String(e?.message ?? e) });
    }
};
