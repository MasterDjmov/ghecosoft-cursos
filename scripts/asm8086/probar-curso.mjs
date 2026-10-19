#!/usr/bin/env node
// Verifica un curso de Ensamblador 8086 (D110): cada micro-misión se resuelve con su «Solución» (salida y estado
// esperados), su «Código inicial» todavía no la resuelve, y cada «Código de ejemplo» da su «Salida esperada».
//   node scripts/asm8086/probar-curso.mjs cursos/ensamblador [filtro]
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { runAsm, normalizeStateLine, STATE_HEADER } from '../../resources/js/runners/asm8086/index.js';

const dir = process.argv[2] ?? 'cursos/ensamblador';
const filter = process.argv[3] ?? '';
const clean = (s) => (s ?? '').replace(/\r/g, '').split('\n').map((l) => l.replace(/\s+$/, '')).join('\n').replace(/^\n+|\n+$/g, '');
const block = (text) => {
    const m = /```[\w+-]*\n([\s\S]*?)\n```/.exec(text ?? '');
    return m ? m[1] : (text ?? '').trim();
};

function expectedOf(salida, estado) {
    const report = estado ? clean(estado).split('\n').map(normalizeStateLine).filter(Boolean) : [];
    const state = report.length ? `${STATE_HEADER}\n${report.join('\n')}` : '';
    const out = clean(salida);
    return out && state ? `${out}\n${state}` : out + state;
}

let ok = 0;
let bad = 0;
const fail = (where, msg) => { bad++; console.log(`✗ ${where}: ${msg}`); };

for (const file of readdirSync(dir).filter((f) => f.endsWith('.md')).sort()) {
    const text = readFileSync(join(dir, file), 'utf8');
    // Partes de nivel ### (micro-misiones y secciones del nodo) dentro de cada ## nodo.
    const nodes = text.split(/\n(?=## )/);
    for (const node of nodes) {
        const nodeId = /^## (\S+)/.exec(node)?.[1];
        if (!nodeId) continue;
        const sections = node.split(/\n(?=### )/);
        const get = (title) => sections.find((s) => s.startsWith(`### ${title}`));
        const example = get('Código de ejemplo');
        if (example && (!filter || nodeId.includes(filter))) {
            const r = runAsm(block(example.split('\n').slice(1).join('\n')), { stdin: block(get('Entrada de ejemplo')?.split('\n').slice(1).join('\n') ?? '') });
            const want = clean(block(get('Salida esperada')?.split('\n').slice(1).join('\n')));
            if (r.error) fail(`${nodeId} ejemplo`, r.error);
            else if (clean(r.output) !== want) fail(`${nodeId} ejemplo`, `obtuvo ${JSON.stringify(clean(r.output))}, esperaba ${JSON.stringify(want)}`);
            else ok++;
        }
        for (const s of sections.filter((x) => x.startsWith('### Micro-misión'))) {
            const id = /### Micro-misión (\S+)/.exec(s)[1];
            if (filter && !id.includes(filter)) continue;
            const parts = Object.fromEntries(s.split(/\n(?=#### )/).slice(1).map((p) => [p.split('\n')[0].slice(5).trim(), p.split('\n').slice(1).join('\n')]));
            const estado = parts['Estado esperado'] ? block(parts['Estado esperado']) : '';
            const expected = expectedOf(parts['Salida esperada'] ? block(parts['Salida esperada']) : '', estado);
            const stdin = parts.Entrada ? block(parts.Entrada) : '';
            if (!expected) { fail(id, 'no tiene salida ni estado esperado'); continue; }
            if (!parts['Solución']) { fail(id, 'no tiene Solución'); continue; }
            const r = runAsm(block(parts['Solución']), { stdin, checks: estado });
            if (r.error) fail(id, `la solución falla: ${r.error}`);
            else if (clean(r.output) !== expected) fail(id, `la solución da ${JSON.stringify(clean(r.output))}, se esperaba ${JSON.stringify(expected)}`);
            else ok++;
            if (parts['Código inicial']) {
                const start = runAsm(block(parts['Código inicial']), { stdin, checks: estado });
                if (!start.error && clean(start.output) === expected) fail(id, 'el código inicial ya la resuelve');
            }
        }
    }
}
console.log(`\n${ok} bien, ${bad} mal`);
process.exit(bad ? 1 : 0);
