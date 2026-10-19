// Ensamblador 8086 en el navegador (D110): ensamblar, correr y armar el informe de estado de una micro-misión.
// El código del alumno nunca sale del navegador: es un intérprete, no ejecuta JavaScript ajeno.

import { assemble, AsmError, REG16, REG8, SREG, parseNumber } from './assembler.js';
import { Machine, FLAG_BITS, hex } from './machine.js';

export { assemble, AsmError, Machine, hex };

export const LIMIT = 5_000_000;
export const STATE_HEADER = '── Estado ──';

// La criatura del bestiario que nace de cada error del ensamblador (GUION.md, cap. 26).
const CREATURES = {
    A2209: 'slime', A2142: 'slime', A2099: 'slime', A2150: 'slime', A2056: 'slime',
    A2048: 'goblin', A2182: 'goblin', A2030: 'goblin', A2049: 'goblin', A2033: 'goblin',
    A2102: 'skeleton', A2053: 'orc',
};

const SPANISH = {
    A2209: 'El Gólem no reconoce esa palabra (¿está bien escrita? ¿es una palabra reservada?)',
    A2142: 'Un bloque quedó abierto: falta su «endp» (o el «endp» no tiene el mismo nombre)',
    A2099: 'Falta «end main» al final del programa',
    A2150: 'A la expresión le falta un operador (¿falta una coma o un «+»?)',
    A2056: 'Ese nombre ya está usado: dos etiquetas o variables no pueden llamarse igual',
    A2048: 'Los dos operandos tienen que ser del mismo tamaño (byte con byte, word con word)',
    A2182: 'No se sabe si es un byte o un word: agregá «byte ptr» o «word ptr»',
    A2030: 'Esa orden no existe en el 8086 (es de un procesador más nuevo)',
    A2049: 'Esa combinación de operandos no existe (por ejemplo, de memoria a memoria)',
    A2033: 'Entre corchetes solo van BX, BP, SI y DI',
    A2102: 'Ese nombre no está definido (¿error de tipeo? ¿falta declararlo en .data?)',
    A2053: 'El salto queda demasiado lejos: un salto condicional llega a 127 bytes',
};

/** El error del ensamblador explicado para el alumno, con la criatura y el mensaje real (como en emu8086). */
export function describeError(e) {
    if (!(e instanceof AsmError)) return { line: null, message: String(e.message ?? e), raw: '', creature: 'ogre' };
    // El hueco de una micro-misión que todavía no se completó.
    if (e.raw.includes('___')) return { line: e.line, message: 'Todavía hay un ___ para completar en esta línea.', raw: e.raw, creature: 'slime', code: e.code };
    return { line: e.line, message: SPANISH[e.code] ?? e.message, raw: e.raw, creature: CREATURES[e.code] ?? 'slime', code: e.code };
}

/**
 * Ensambla y corre el programa de una vez (para comprobar una micro-misión).
 * @returns {{ output, error, ms, line?, state?, halt? }}
 */
export function runAsm(code, { stdin = '', checks = '', limit = LIMIT, timeout = 5000 } = {}) {
    const t0 = Date.now();
    let program;
    try {
        program = assemble(code);
    } catch (e) {
        const d = describeError(e);
        return { output: '', error: `Línea ${d.line ?? '?'}: ${d.message}\n(${d.raw})`, ms: Date.now() - t0, line: d.line, creature: d.creature };
    }
    const m = new Machine(program, { input: stdin });
    let status = 'ok';
    let done = 0;
    while (done < limit) {
        status = m.run(Math.min(100_000, limit - done));
        done += 100_000;
        if (status !== 'ok') break;
        if (Date.now() - t0 > timeout) break;
    }
    const output = m.screen.text();
    if (status === 'ok') {
        return { output, error: 'El Gólem se quedó dando vueltas: el programa no terminó (¿un bucle sin salida?)', timedOut: true, ms: Date.now() - t0 };
    }
    const halt = m.halted;
    const report = checks ? stateReport(m.snapshot ?? m, checks) : '';
    const full = report ? (output ? `${output}\n${report}` : report) : output;
    if (!halt.normal) {
        // Una entrada que se terminó no es un error del programa (como en dos8086.py).
        const soft = halt.reason.startsWith('se termino la entrada');
        return { output: full, error: soft ? null : friendlyHalt(halt), halt: halt.reason, ms: Date.now() - t0 };
    }
    return { output: full, error: null, ms: Date.now() - t0, halt: halt.reason };
}

function friendlyHalt(halt) {
    if (halt.reason.startsWith('Divide overflow')) return 'El Ogro de la división: dividiste por cero o el cociente no entra en el registro (Divide overflow).';
    return halt.reason;
}

// ------------------------------------------------ informe de estado («Estado esperado»)

const SIZES = Object.fromEntries([...REG16.map((r) => [r, 16]), ...REG8.map((r) => [r, 8]), ...SREG.map((r) => [r, 16]), ['ip', 16]]);

/**
 * Lee una línea del «Estado esperado»: «AX = 1234h», «ZF = 1», «[pociones] = 4», «word [monedas] = 4142h».
 * @returns {{ name, kind: 'reg'|'flag'|'mem', size, target, value } | null}
 */
export function parseStateLine(line) {
    const m = /^\s*(word\s+|byte\s+)?([^=]+?)\s*=\s*(.+?)\s*$/i.exec(line);
    if (!m) return null;
    const width = m[1] ? (m[1].trim().toLowerCase() === 'word' ? 16 : 8) : null;
    const name = m[2].trim();
    const lower = name.toLowerCase();
    const value = parseValue(m[3].trim());
    if (value === null) return null;
    if (SIZES[lower]) return { name: name.toUpperCase(), kind: 'reg', size: SIZES[lower], target: lower, value };
    if (lower in FLAG_BITS) return { name: name.toUpperCase(), kind: 'flag', size: 1, target: lower, value: value ? 1 : 0 };
    const mem = /^\[\s*(.+?)\s*\]$/.exec(name);
    if (mem) return { name: `${width === 16 ? 'word ' : ''}[${mem[1]}]`, kind: 'mem', size: width ?? 8, target: mem[1], value };
    return null;
}

function parseValue(text) {
    const str = /^'(.)'$/.exec(text);
    if (str) return str[1].charCodeAt(0);
    const t = text.replace(/^-/, '');
    // En el estado esperado se acepta «FFh» sin el 0 de adelante (en el código, MASM lo exige: 0FFh).
    const n = /^[0-9a-f]+h$/i.test(t) ? parseInt(t.slice(0, -1), 16) : parseNumber(t);
    if (n === null) return null;
    return text.startsWith('-') ? -n : n;
}

/** El valor como lo escribe el informe: hexa con «h» (4 cifras un word, 2 un byte) o 0/1 una bandera. */
export function formatValue(value, size) {
    if (size === 1) return String(value ? 1 : 0);
    const masked = value & (size === 8 ? 0xff : 0xffff);
    return `${hex(masked, size / 4)}h`;
}

/** La línea normalizada del estado esperado (la misma que arma el servidor al importar). */
export function normalizeStateLine(line) {
    const p = parseStateLine(line);
    return p ? `${p.name} = ${formatValue(p.value, p.size)}` : null;
}

/** El informe del estado real de la máquina, en el mismo orden y formato que el estado esperado. */
export function stateReport(machine, checks) {
    const lines = String(checks).split('\n').map((l) => l.trim()).filter(Boolean);
    const out = [STATE_HEADER];
    for (const line of lines) {
        const p = parseStateLine(line);
        if (!p) continue;
        let actual;
        if (p.kind === 'reg' || p.kind === 'flag') actual = machine.get(p.target);
        else actual = readMemory(machine, p.target, p.size);
        out.push(`${p.name} = ${actual === null ? '?' : formatValue(actual, p.size)}`);
    }
    return out.join('\n');
}

function readMemory(machine, target, size) {
    const sym = machine.p.symbols;
    // [nombre], [nombre+2], [0200h]
    const m = /^([A-Za-z_?][A-Za-z0-9_?]*)?\s*(?:([+-])\s*(\w+))?$/.exec(target.replace(/\s+/g, ' '));
    let offset;
    if (m && m[1] && sym.has(m[1].toLowerCase())) {
        const s = sym.get(m[1].toLowerCase());
        if (s.offset === undefined) return null;
        offset = s.offset;
        if (m[2]) offset += (m[2] === '-' ? -1 : 1) * (parseNumber(m[3]) ?? 0);
    } else {
        const n = parseNumber(target);
        if (n === null) return null;
        offset = n;
    }
    return size === 8 ? machine.read8(machine.dataSeg, offset) : machine.read16(machine.dataSeg, offset);
}
