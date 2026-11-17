// Cómo se reparten los archivos de una micro-misión de TypeScript (D115, fase 5) entre el compilador y la caja. Lo usan
// typescript.js (el navegador) y scripts/js-micro/probar.mjs (Node).

/**
 * Los archivos de la consigna: los .ts y .d.ts van al compilador; los .js (una biblioteca sin tipos, que se describe con
 * su .d.ts) van tal cual a la caja.
 */
export function splitFiles(code, files = {}) {
    const sources = { 'main.ts': code };
    const raw = {};
    for (const [name, text] of Object.entries(files ?? {})) {
        if (name.endsWith('.js')) raw[name] = text;
        else sources[name] = text;
    }

    return { sources, raw };
}

/** Lo que va a la caja además de main.js: el JavaScript de cada .ts (los .d.ts no generan nada). */
export function cajaFiles(sources, js) {
    const files = {};
    for (const name of Object.keys(sources)) {
        if (name === 'main.ts' || name.endsWith('.d.ts')) continue;
        files[name.replace(/\.ts$/, '.js')] = js[name.replace(/\.ts$/, '.js')] ?? '';
    }

    return files;
}
