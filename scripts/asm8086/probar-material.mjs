#!/usr/bin/env node
// Prueba de aceptación del emulador 8086 (D110): ensambla y corre cada .asm del material del curso y compara
// con su .salida.txt (generada con herramientas/dos8086.py, la referencia). Uso:
//   node scripts/asm8086/probar-material.mjs [carpeta] [filtro]
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { assemble, Machine, describeError } from '../../resources/js/runners/asm8086/index.js';

const root = process.argv[2] ?? '/home/djmov/Programas/Cursos/FullCursos/26-Ensamblador-8086';
const filter = process.argv[3] ?? '';

function walk(dir) {
    return readdirSync(dir).flatMap((f) => {
        const p = join(dir, f);
        if (f === 'herramientas' || f.startsWith('.')) return [];
        return statSync(p).isDirectory() ? walk(p) : p.endsWith('.asm') ? [p] : [];
    });
}

const clean = (s) => s.replace(/\r/g, '').split('\n').map((l) => l.replace(/\s+$/, '')).join('\n').replace(/\n+$/, '');

let ok = 0;
let fail = 0;
for (const file of walk(root).sort()) {
    if (filter && !file.includes(filter)) continue;
    const base = file.slice(0, -4);
    const expectedFile = `${base}.salida.txt`;
    if (!existsSync(expectedFile)) continue;
    const input = existsSync(`${base}.entrada.txt`) ? readFileSync(`${base}.entrada.txt`) : new Uint8Array();
    let got;
    try {
        const program = assemble(readFileSync(file, 'latin1'));
        const m = new Machine(program, { input });
        const status = m.run(20_000_000);
        got = m.screen.text();
        if (status === 'ok') got += '\n[dos8086] bucle infinito (se supero el limite de instrucciones)';
        else if (m.halted.reason !== 'fin') got += `\n[dos8086] ${m.halted.reason}`;
    } catch (e) {
        const d = describeError(e);
        got = `ERROR ${d.raw || d.message}`;
        if (!d.raw) console.error(e);
    }
    const expected = readFileSync(expectedFile, 'latin1');
    if (clean(got) === clean(expected)) {
        ok++;
    } else {
        fail++;
        const a = clean(got).split('\n');
        const b = clean(expected).split('\n');
        const i = a.findIndex((l, k) => l !== b[k]);
        console.log(`✗ ${file.replace(root + '/', '')}\n   línea ${i + 1}\n   obtuvo:   ${JSON.stringify(a[i] ?? '(nada)')}\n   esperaba: ${JSON.stringify(b[i] ?? '(nada)')}`);
    }
}
console.log(`\n${ok} bien, ${fail} mal`);
process.exit(fail ? 1 : 0);
