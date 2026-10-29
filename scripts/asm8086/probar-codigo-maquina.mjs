#!/usr/bin/env node
// Verifica el código máquina del tablero (D110, encoder.js): arma los bytes de cada orden de los programas del
// material y del curso, los desarma con objdump (GNU binutils, modo 8086) y compara cada orden con la original.
// También comprueba que el largo de los bytes sea el que usó el ensamblador para las direcciones.
//   node scripts/asm8086/probar-codigo-maquina.mjs [material] [cursos/ensamblador]
import { readFileSync, readdirSync, statSync, writeFileSync, mkdtempSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { execFileSync } from 'node:child_process';
import { assemble } from '../../resources/js/runners/asm8086/index.js';
import { encode, hexBytes } from '../../resources/js/runners/asm8086/encoder.js';

const material = process.argv[2] ?? '/home/djmov/Programas/Cursos/FullCursos/26-Ensamblador-8086';
const course = process.argv[3] ?? 'cursos/ensamblador';
const DATA_SEG = 0x1234;
const work = mkdtempSync(join(tmpdir(), 'asm-bytes-'));

function walk(dir) {
    return readdirSync(dir).flatMap((f) => {
        const p = join(dir, f);
        if (f === 'herramientas' || f.startsWith('.')) return [];
        return statSync(p).isDirectory() ? walk(p) : p.endsWith('.asm') ? [p] : [];
    });
}

const programs = walk(material).map((p) => [p, readFileSync(p, 'utf8')]);
for (const f of readdirSync(course).filter((x) => x.endsWith('.md'))) {
    const text = readFileSync(join(course, f), 'utf8');
    for (const m of text.matchAll(/^#{3,4} (Solución|Código de ejemplo|Código inicial)[^\n]*\n+```[\w+-]*\n([\s\S]*?)\n```/gm)) {
        programs.push([`${f} ${m[1]}`, m[2]]);
    }
}

const COND = { z: 'je', nz: 'jne', c: 'jb', nc: 'jae', a: 'ja', be: 'jbe', g: 'jg', ge: 'jge', l: 'jl', le: 'jle', s: 'js', ns: 'jns', o: 'jo', no: 'jno', p: 'jp', np: 'jnp' };
const STRING = /^(movs|lods|stos|cmps|scas)[bw]$/;
const num = (s) => parseInt(s, 16);

/** La orden, como la escribiría objdump (sin tamaños ni espacios): para comparar. */
function ours(ins) {
    const w = (ins.size || ins.ops[0]?.size || ins.ops[1]?.size) === 16;
    let m = ins.cond ? COND[ins.cond] : ins.m === 'xlat' ? 'xlat' : ins.m;
    if (m === 'loopz') m = 'loope';
    if (m === 'loopnz') m = 'loopne';
    if (STRING.test(m)) return [ins.prefix ? `${ins.prefix} ${m.slice(0, 4)}` : m.slice(0, 4)].join('');
    const op = (o) => {
        if (o.k === 'reg' || o.k === 'sreg') return o.r;
        if (o.k === 'imm') {
            const v = o.sym?.kind === 'segment' ? DATA_SEG : o.v;
            return String(v & (w || ['ret', 'call', 'jmp'].includes(m) || ins.cond || m.startsWith('loop') || m === 'jcxz' ? 0xffff : m === 'int' ? 0xff : 0xff));
        }
        const parts = [o.base, o.index].filter(Boolean);
        const d = o.disp & 0xffff;
        return `${o.seg ? o.seg + ':' : ''}[${[...parts, d || !parts.length ? String(d) : null].filter(Boolean).join('+')}]`;
    };
    if (m === 'xlat') return 'xlat';
    let ops = ins.ops.map(op);
    if (m === 'xchg' || m === 'test') ops = ops.sort();
    return `${m} ${ops.join(',')}`.trim();
}

function theirs(text) {
    let t = text.toLowerCase().replace(/(byte|word) ptr /g, '').replace(/\s+/g, ' ').trim();
    const [m0, ...rest] = t.split(' ');
    let m = m0;
    let opsText = rest.join(' ');
    if (m === 'rep' || m === 'repz' || m === 'repnz' || m === 'repne') {
        const pre = m === 'repz' ? 'repe' : m === 'repnz' ? 'repne' : m;
        return `${pre} ${rest[0]}`;
    }
    if (STRING.test(m + 'b') && /\[/.test(opsText)) return m;
    if (m === 'xlat') return 'xlat';
    const ops = opsText ? opsText.split(',').map((o) => {
        o = o.trim();
        let seg = '';
        const sm = /^([cdes]s):(.*)$/.exec(o);
        if (sm) { seg = sm[1]; o = sm[2]; }
        if (/^0x[0-9a-f]+$/.test(o)) {
            if (seg) return `${seg === 'ds' ? '' : seg + ':'}[${num(o.slice(2))}]`;
            return String(num(o.slice(2)));
        }
        const mm = /^\[([^\]]+)\]$/.exec(o);
        if (mm) {
            const regs = [];
            let d = 0;
            for (const piece of mm[1].replace(/-/g, '+-').split('+').filter(Boolean)) {
                if (/^-?0x/.test(piece)) d += piece.startsWith('-') ? -num(piece.slice(3)) : num(piece.slice(2));
                else regs.push(piece);
            }
            d &= 0xffff;
            return `${seg ? seg + ':' : ''}[${[...regs, d || !regs.length ? String(d) : null].filter(Boolean).join('+')}]`;
        }
        if (/^\d+$/.test(o)) return o;
        return o;
    }) : [];
    if (m === 'xchg' || m === 'test') ops.sort();
    return `${m} ${ops.join(',')}`.trim();
}

let ok = 0;
let bad = 0;
const seen = new Set();
for (const [name, code] of programs) {
    let program;
    try { program = assemble(code); } catch { continue; }
    const image = [];
    const rows = [];
    for (const ins of program.instructions) {
        const bytes = encode(ins, { dataSeg: DATA_SEG });
        if (!bytes) { bad++; console.log(`✗ ${name} línea ${ins.line}: sin codificar «${ins.text}»`); continue; }
        if (bytes.length !== ins.length) { bad++; console.log(`✗ ${name} línea ${ins.line}: «${ins.text}» da ${bytes.length} bytes y ocupa ${ins.length}`); }
        while (image.length < ins.address) image.push(0x90);
        image.push(...bytes);
        rows.push([ins, bytes]);
    }
    const file = join(work, 'p.bin');
    writeFileSync(file, Uint8Array.from(image));
    const dis = new Map();
    for (const line of execFileSync('objdump', ['-D', '-b', 'binary', '-m', 'i8086', '-M', 'intel', file], { encoding: 'utf8' }).split('\n')) {
        const mm = /^\s*([0-9a-f]+):\t[0-9a-f ]+\t(.*)$/.exec(line);
        if (mm) dis.set(num(mm[1]), mm[2]);
    }
    for (const [ins, bytes] of rows) {
        const want = ours(ins);
        const got = theirs(dis.get(ins.address) ?? '(nada)');
        const key = `${want}|${got}`;
        if (want === got) { ok++; continue; }
        bad++;
        if (seen.has(key)) continue;
        seen.add(key);
        console.log(`✗ ${name} línea ${ins.line}: «${ins.text}» → ${hexBytes(bytes)} = «${dis.get(ins.address)}» (${want} ≠ ${got})`);
    }
}
console.log(`\n${ok} bien, ${bad} mal (${programs.length} programas)`);
process.exit(bad ? 1 : 0);
