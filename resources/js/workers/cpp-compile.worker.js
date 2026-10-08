// Compila C y C++ en el navegador (C++ del docente, D66; C también del alumno, D98): Clang de YoWASP (WebAssembly, del CDN) con la biblioteca
// estándar de wasi-sdk con excepciones y un encabezado precompilado (public/toolchains/cpp). El programa
// resultante lo ejecuta otro worker (wasi-run.worker.js), así un bucle infinito no se lleva al compilador.
import { CLANG_URL, SYSROOT_URL, PCH_URL, COMPILE_FLAGS, LINK_FLAGS, C_FLAGS } from '../runners/cpp-config.js';
// El mismo encabezado con el que scripts/build-cpp-toolchain.sh armó el PCH: Clang lo pide junto al PCH.
import comun from '../runners/cpp-comun.hpp?raw';

async function gunzip(response) {
    if (!response.ok) throw new Error(`No se pudo bajar ${response.url} (${response.status})`);
    const bytes = new Uint8Array(await response.arrayBuffer());
    // Algunos servidores mandan el .gz con Content-Encoding y el navegador ya lo descomprimió.
    if (bytes[0] !== 0x1f || bytes[1] !== 0x8b) return bytes;
    return new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer());
}

/** Un .tar (ustar) a un árbol { carpeta: { archivo: bytes } }, como lo pide YoWASP. */
function untar(bytes) {
    const root = {};
    const text = (a, b) => new TextDecoder().decode(bytes.subarray(a, b)).replace(/\0.*$/s, '');
    for (let off = 0; off + 512 <= bytes.length;) {
        const name = text(off, off + 100);
        if (!name) break;
        const prefix = text(off + 345, off + 500);
        const size = parseInt(text(off + 124, off + 136).trim() || '0', 8);
        const type = String.fromCharCode(bytes[off + 156]);
        off += 512;
        if (type === '0' || type === '\0') {
            const parts = ((prefix ? prefix + '/' : '') + name).replace(/^\.\//, '').split('/').filter(Boolean);
            let dir = root;
            for (const part of parts.slice(0, -1)) dir = dir[part] ??= {};
            dir[parts.at(-1)] = bytes.slice(off, off + size);
        }
        off += Math.ceil(size / 512) * 512;
    }
    return root;
}

let tools = null;
let header = null;

/** Clang y la biblioteca. El encabezado precompilado (~14 MB) es solo de C++: el alumno de C no lo baja (D98). */
async function load(language) {
    tools ??= Promise.all([
        import(/* @vite-ignore */ CLANG_URL),
        fetch(SYSROOT_URL).then(gunzip).then(untar),
    ]).then(([clang, sysroot]) => ({ runClang: clang.runClang, sysroot }));
    if (language !== 'c') header ??= fetch(PCH_URL).then(gunzip);
    try {
        const loaded = await tools;
        return { ...loaded, pch: language === 'c' ? null : await header };
    } catch (e) {
        tools = null;
        header = null;
        throw e;
    }
}

self.onmessage = async ({ data: { id, code, language } }) => {
    try {
        const { runClang, sysroot, pch } = await load(language);
        self.postMessage({ id, type: 'loaded' });

        let diagnostics = '';
        const stderr = (bytes) => { if (bytes) diagnostics += new TextDecoder().decode(bytes); };
        try {
            // C: como gcc -std=c11 del curso (las cabeceras de C son livianas: no hace falta el PCH).
            const linked = language === 'c'
                ? await runClang(['clang', ...C_FLAGS, 'main.c', '-lm', '-o', 'programa.wasm'], { sysroot, 'main.c': code }, { stderr })
                : await runClang(['clang++', ...COMPILE_FLAGS, '-include-pch', 'comun.pch', '-Wall', '-Wextra', '-c', 'main.cpp', '-o', 'main.o'],
                    { sysroot, 'main.cpp': code, 'comun.pch': pch, 'comun.hpp': comun }, { stderr })
                    .then((object) => runClang(['clang++', ...LINK_FLAGS, 'main.o', '-o', 'programa.wasm'], { sysroot, 'main.o': object['main.o'] }, { stderr }));
            self.postMessage({ id, type: 'compiled', wasm: linked['programa.wasm'], diagnostics });
        } catch {
            self.postMessage({ id, type: 'compileError', diagnostics: diagnostics || 'No compila.' });
        }
    } catch (e) {
        self.postMessage({ id, type: 'loadFailed', message: String(e?.message ?? e) });
    }
};
