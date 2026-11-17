// El compilador de TypeScript del navegador, cargado en Node (D115, fase 5): el mismo ts-compile.js, con el
// compilador y los .d.ts de node_modules y los mensajes en español. Lo usan probar-compilador.mjs y
// scripts/js-micro/probar.mjs (los cursos de TypeScript).
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { compile, MAIN } from '../../resources/js/runners/ts-compile.js';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const LIB = path.join(ROOT, 'node_modules/typescript/lib');
export const ts = createRequire(import.meta.url)(path.join(ROOT, 'node_modules/typescript'));
export const libs = {};
const pending = ['esnext.full'];
while (pending.length) {
    const name = `lib.${pending.pop()}.d.ts`;
    if (libs[name] !== undefined) continue;
    libs[name] = fs.readFileSync(path.join(LIB, name), 'utf8');
    for (const found of libs[name].matchAll(/\/\/\/\s*<reference\s+lib="([^"]+)"/g)) pending.push(found[1].toLowerCase());
}
ts.setLocalizedDiagnosticMessages(JSON.parse(fs.readFileSync(path.join(LIB, 'es/diagnosticMessages.generated.json'), 'utf8')));

export { MAIN };

/** Compila main.ts y sus módulos (`vec2.ts`…) como en el navegador. */
export function compileFiles(files, tsconfig = null) {
    return compile(ts, libs, files, tsconfig);
}
