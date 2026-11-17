#!/usr/bin/env node
// Arma el compilador de TypeScript para el navegador (D115, fase 5), en public/toolchains/typescript/:
//   typescript-<versión>.js.gz   el compilador (lib/typescript.js de node_modules)
//   libs-<versión>.json.gz       los .d.ts de lib.esnext.full (ES más nuevo + DOM), los únicos que se usan
//   es-<versión>.json.gz         los mensajes de error en español del propio TypeScript
// El worker (resources/js/workers/typescript.worker.js) los baja la primera vez y quedan en la caché del navegador.
// Uso: node scripts/build-typescript-toolchain.mjs   (después de npm install; lo corre solo deploy.sh)
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const LIB = path.join(ROOT, 'node_modules/typescript/lib');
const OUT = path.join(ROOT, 'public/toolchains/typescript');
const config = fs.readFileSync(path.join(ROOT, 'resources/js/runners/typescript-config.js'), 'utf8');
const version = config.match(/TS_VERSION = '([^']+)'/)?.[1];
const installed = JSON.parse(fs.readFileSync(path.join(ROOT, 'node_modules/typescript/package.json'), 'utf8')).version;

if (!version || version !== installed) {
    console.error(`typescript-config.js pide la ${version} y node_modules tiene la ${installed}: que coincidan (npm install).`);
    process.exit(1);
}

// Los .d.ts que hacen falta: lib.esnext.full y todo lo que nombra con /// <reference lib="…" />.
const libs = {};
const pending = ['esnext.full'];
while (pending.length) {
    const name = `lib.${pending.pop()}.d.ts`;
    if (libs[name] !== undefined) continue;
    const text = fs.readFileSync(path.join(LIB, name), 'utf8');
    libs[name] = text;
    for (const found of text.matchAll(/\/\/\/\s*<reference\s+lib="([^"]+)"/g)) pending.push(found[1].toLowerCase());
}

const gzip = (text) => zlib.gzipSync(Buffer.from(text), { level: 9 });
fs.mkdirSync(OUT, { recursive: true });
for (const old of fs.readdirSync(OUT)) fs.rmSync(path.join(OUT, old));
fs.writeFileSync(path.join(OUT, `typescript-${version}.js.gz`), gzip(fs.readFileSync(path.join(LIB, 'typescript.js'), 'utf8')));
fs.writeFileSync(path.join(OUT, `libs-${version}.json.gz`), gzip(JSON.stringify(libs)));
fs.writeFileSync(path.join(OUT, `es-${version}.json.gz`), gzip(fs.readFileSync(path.join(LIB, 'es/diagnosticMessages.generated.json'), 'utf8')));

for (const file of fs.readdirSync(OUT)) {
    console.log(`${file}  ${(fs.statSync(path.join(OUT, file)).size / 1024 / 1024).toFixed(2)} MB`);
}
console.log(`${Object.keys(libs).length} archivos .d.ts`);
