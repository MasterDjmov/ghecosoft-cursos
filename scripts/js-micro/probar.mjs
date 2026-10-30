// Prueba las micro-misiones de un curso de JavaScript (D115) en la misma caja que usa el alumno, en Chrome sin
// ventana: corre la «Solución» de cada una (con su Página, Eventos, Estado, Almacenamiento y Entrada) y la compara
// con la «Salida esperada». Con --fill escribe la salida esperada que falte (o la que cambió, con --force).
// También avisa si el «Código inicial» ya da la salida (la micro-misión se resolvería sin hacer nada).
//   node scripts/js-micro/probar.mjs cursos/javascript [--only=R01] [--fill] [--force]
import fs from 'node:fs';
import path from 'node:path';
import { openChrome } from './chrome.mjs';

const args = process.argv.slice(2);
const folder = path.resolve(args.find((a) => !a.startsWith('--')) ?? 'cursos/javascript');
const only = (args.find((a) => a.startsWith('--only=')) ?? '').slice(7);
const fill = args.includes('--fill');
const force = args.includes('--force');

const FIELD = { 'solución': 'solution', 'código inicial': 'starter', 'página': 'page', 'eventos': 'events', 'estado': 'checks', 'almacenamiento': 'storage', 'entrada': 'stdin', 'salida esperada': 'expected' };

function block(text) {
    const fenced = text.match(/^\s*(`{3,}|~{3,})[\w+-]*[ \t]*\n([\s\S]*?)\n[ \t]*\1\s*$/);
    return fenced ? fenced[2] : text.trim();
}

/** Las micro-misiones del archivo: { code, start, end, fields: { solution, starter, page, … } }. */
function missions(text) {
    const found = [];
    const re = /^### Micro-misión ([A-Z0-9-]+) · .*$/gm;
    const heads = [];
    let m;
    while ((m = re.exec(text))) heads.push({ code: m[1], start: m.index });
    heads.forEach((h, i) => {
        const lineEnd = text.indexOf('\n', h.start);
        const next = text.slice(lineEnd).search(/^#{2,3} /m);
        const end = next === -1 ? text.length : lineEnd + next;
        const body = text.slice(h.start, end);
        const fields = {};
        const parts = body.split(/^#### /m).slice(1);
        for (const part of parts) {
            const newline = part.indexOf('\n');
            const title = part.slice(0, newline).trim().toLowerCase();
            if (FIELD[title]) fields[FIELD[title]] = block(part.slice(newline + 1).replace(/\n+$/, ''));
        }
        found.push({ code: h.code, start: h.start, end, fields });
    });
    return found;
}

function storageOf(text) {
    const storage = {};
    const cookies = [];
    for (const line of String(text ?? '').split('\n')) {
        const m = line.match(/^\s*(local|session|cookie)\s+([^=\s]+)\s*=\s*(.*?)\s*$/);
        if (!m) continue;
        if (m[1] === 'cookie') cookies.push(`${m[2]}=${m[3]}`);
        else (storage[m[1]] ??= {})[m[2]] = m[3];
    }
    return { storage, cookies: cookies.join('; ') };
}

const normalize = (t) => String(t ?? '').replace(/\r\n?/g, '\n').replace(/[ \t]+$/gm, '').replace(/^\n+|\n+$/g, '');

function writeExpected(file, mission, output) {
    let text = fs.readFileSync(file, 'utf8');
    const start = text.indexOf(`### Micro-misión ${mission.code} ·`);
    const lineEnd = text.indexOf('\n', start);
    const next = text.slice(lineEnd).search(/^#{2,3} /m);
    const end = next === -1 ? text.length : lineEnd + next;
    let body = text.slice(start, end);
    const section = `#### Salida esperada\n\`\`\`\n${output}\n\`\`\`\n\n`;
    body = /^#### Salida esperada\n[\s\S]*?(?=^#### |(?![\s\S]))/m.test(body)
        ? body.replace(/^#### Salida esperada\n[\s\S]*?(?=^#### |(?![\s\S]))/m, section)
        : body.replace(/^#### Solución/m, section + '#### Solución');
    fs.writeFileSync(file, text.slice(0, start) + body + text.slice(end));
}

const chrome = await openChrome();
let ok = 0;
let bad = 0;
let filled = 0;
for (const name of fs.readdirSync(folder).filter((f) => f.endsWith('.md')).sort()) {
    const file = path.join(folder, name);
    for (const mission of missions(fs.readFileSync(file, 'utf8'))) {
        if (only && !mission.code.startsWith(only)) continue;
        const f = mission.fields;
        if (!f.solution) {
            console.log(`  ? ${mission.code}: no tiene «Solución»`);
            bad++;
            continue;
        }
        const { storage, cookies } = storageOf(f.storage);
        const options = { page: f.page, events: f.events, checks: f.checks, stdin: f.stdin, storage, cookies };
        const result = await chrome.run(f.solution, options);
        if (result.error) {
            console.log(`  ✗ ${mission.code}: la solución falla: ${result.error}`);
            bad++;
            continue;
        }
        const output = normalize(result.output);
        if (!f.expected || (force && normalize(f.expected) !== output)) {
            if (fill) {
                writeExpected(file, mission, output);
                filled++;
                console.log(`  ✎ ${mission.code}: salida esperada escrita`);
            } else {
                console.log(`  ? ${mission.code}: falta la salida esperada (correr con --fill). Da:\n${output}`);
                bad++;
            }
            continue;
        }
        if (normalize(f.expected) !== output) {
            console.log(`  ✗ ${mission.code}: la solución no da la salida esperada.\n    esperada: ${JSON.stringify(normalize(f.expected))}\n    da:       ${JSON.stringify(output)}`);
            bad++;
            continue;
        }
        if (f.starter) {
            const starter = await chrome.run(f.starter, options);
            if (!starter.error && normalize(starter.output) === output) {
                console.log(`  ! ${mission.code}: el código inicial ya da la salida esperada`);
                bad++;
                continue;
            }
        }
        ok++;
    }
}
await chrome.close();
console.log(`\n${ok} bien${filled ? `, ${filled} escritas` : ''}${bad ? `, ${bad} con problemas` : ''}.`);
process.exit(bad ? 1 : 0);
