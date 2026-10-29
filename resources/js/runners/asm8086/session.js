// El tablero del Gólem (D110): una ejecución que se puede mirar por dentro. Corre por tandas (sin trabar la
// página), avanza de a una orden, espera las teclas que pide el programa y arma lo que dibuja el tablero.
// Todo es del navegador del alumno.

import { assemble, describeError, stateReport, LIMIT } from './index.js';
import { Machine, FLAG_BITS, hex } from './machine.js';
import { encode, hexBytes } from './encoder.js';

export const REGISTER_ORDER = ['ax', 'bx', 'cx', 'dx', 'si', 'di', 'bp', 'sp', 'cs', 'ds', 'ss', 'es', 'ip'];
export const FLAG_ORDER = ['zf', 'sf', 'cf', 'of', 'pf', 'af', 'df', 'if', 'tf'];
const CGA = ['#000000', '#1d4ed8', '#16a34a', '#0891b2', '#b91c1c', '#9333ea', '#a16207', '#cbd5e1',
    '#64748b', '#60a5fa', '#4ade80', '#22d3ee', '#f87171', '#e879f9', '#fde047', '#ffffff'];

// D110: qué interruptores mira cada salto condicional (para decir por qué saltó o no).
const CONDITIONS = {
    z: ['ZF = 1', ['zf']], nz: ['ZF = 0', ['zf']], c: ['CF = 1', ['cf']], nc: ['CF = 0', ['cf']],
    a: ['CF = 0 y ZF = 0', ['cf', 'zf']], be: ['CF = 1 o ZF = 1', ['cf', 'zf']],
    g: ['ZF = 0 y SF = OF', ['zf', 'sf', 'of']], ge: ['SF = OF', ['sf', 'of']], l: ['SF ≠ OF', ['sf', 'of']],
    le: ['ZF = 1 o SF ≠ OF', ['zf', 'sf', 'of']], s: ['SF = 1', ['sf']], ns: ['SF = 0', ['sf']],
    o: ['OF = 1', ['of']], no: ['OF = 0', ['of']], p: ['PF = 1', ['pf']], np: ['PF = 0', ['pf']],
};

// Lo que significa cada interruptor (se muestra al tocarlo).
export const FLAG_INFO = {
    zf: 'Cero: se prende si el resultado dio 0. Después de cmp, si los dos eran iguales.',
    sf: 'Signo: copia el bit más alto del resultado. Mirado con signo, 1 es negativo.',
    cf: 'Acarreo: se prende si la cuenta sin signo se pasó («me llevo uno») o tuvo que pedir prestado. Ahí cae también el bit que sale al correr.',
    of: 'Desborde: se prende si la cuenta con signo se pasó de rango (dos positivos que dan negativo, o al revés).',
    pf: 'Paridad: 1 si el byte bajo del resultado tiene una cantidad par de unos.',
    af: 'Acarreo auxiliar: del bit 3 al 4 (lo usan las cuentas en BCD).',
    df: 'Dirección: 0, las órdenes de cadena avanzan; 1, retroceden.',
    if: 'Interrupciones: 1, el procesador atiende las del hardware.',
    tf: 'Trampa: 1, el procesador se frena después de cada orden (así trabajan los depuradores).',
};

const nibbles = (v, bits) => v.toString(2).padStart(bits, '0').replace(/(.{4})(?=.)/g, '$1 ');

const escapeHtml = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);

export class AsmSession {
    constructor(code, { stdin = '', checks = '' } = {}) {
        this.code = code;
        this.stdin = stdin;
        this.checks = checks;
        this.machine = null;
        this.error = null;
        this.stopped = false;
        this.memoryBase = null;
        // Si el alumno eligió a qué cajón ir, la memoria no se mueve sola.
        this.memoryManual = false;
        this.lastChanges = { regs: new Set(), flags: new Set(), mem: new Set(), read: new Set() };
        // D110: qué hizo la última orden (en criollo) y qué pestañas tienen novedades (palpitan).
        this.explain = null;
        this.pulse = {};
        // D110: el camino que hizo el paso a paso (las últimas órdenes, con los saltos).
        this.trail = [];
    }

    /** Ensambla. Devuelve null si anduvo, o el error explicado (línea, mensaje, criatura, mensaje real). */
    start() {
        try {
            const program = assemble(this.code);
            this.machine = new Machine(program, { input: this.stdin, interactive: true });
            this.variables = new Map();
            for (const s of program.symbols.values()) {
                if (s.kind === 'data' && s.offset !== undefined) this.variables.set(s.offset, s.name);
            }
            this.labels = new Map();
            for (const s of program.symbols.values()) {
                if ((s.kind === 'label' || s.kind === 'proc') && s.address !== undefined && !this.labels.has(s.address)) this.labels.set(s.address, s.name);
            }
            this.trail = [];
            return null;
        } catch (e) {
            this.error = describeError(e);
            return this.error;
        }
    }

    get halted() {
        return this.machine?.halted ?? null;
    }

    get waiting() {
        return this.machine?.waiting ?? null;
    }

    /** La línea del código que se va a ejecutar ahora. */
    currentLine() {
        return this.machine?.current()?.line ?? null;
    }

    /** Una orden. Devuelve 'ok', 'halt' o 'input'. Deja armado qué hizo (this.explain) y qué palpita (this.pulse). */
    step() {
        const m = this.machine;
        const ins = m.current();
        const before = Object.fromEntries(REGISTER_ORDER.map((r) => [r, m.get(r)]));
        const flagsBefore = Object.fromEntries(FLAG_ORDER.map((f) => [f, m.flag(f)]));
        const memBefore = new Map();
        const screenBefore = m.screen.text();
        const ipBefore = m.ip;
        // La dirección de cada operando de memoria se calcula antes de que la orden cambie los registros.
        const operands = ins ? ins.ops.map((op) => this.operand(op, ins)) : [];
        // Para mostrar «de 03 a 04» en lo que escriba, se mira cada byte antes de que la orden lo toque.
        const write8 = m.write8.bind(m);
        m.write8 = (seg, off, v) => {
            const a = m.phys(seg, off);
            if (!memBefore.has(a)) memBefore.set(a, m.mem[a]);
            write8(seg, off, v);
        };
        let r;
        try {
            r = m.step(true);
        } finally {
            delete m.write8;
        }
        this.lastChanges = m.changes ?? this.lastChanges;
        if (r === 'input') {
            this.explain = null;
            return r;
        }
        this.describe(ins, before, flagsBefore, memBefore, screenBefore);
        if (ins) {
            const flow = this.flowOf(ins, flagsBefore);
            this.explain.flow = flow;
            this.explain.tech = this.techOf(ins, ipBefore, operands, flow);
            this.trail.push({ n: (this.trail.at(-1)?.n ?? 0) + 1, line: ins.line, text: ins.text, ip: hex(ipBefore, 4), jump: flow?.jumped ? (this.lineAt(m.ip) ?? hex(m.ip, 4) + 'h') : null });
            if (this.trail.length > 40) this.trail.shift();
        }
        return r;
    }

    /** El cajón (offset dentro de los datos) de una dirección física, o null si no es de los datos. */
    dataOffset(phys) {
        const off = phys - this.machine.dataSeg * 16;
        return off >= 0 && off <= 0xffff && off < Math.max(this.machine.p.data.length, 16) + 256 ? off : null;
    }

    /** El nombre de la variable que vive en ese cajón (o «variable+2» si cae adentro de una). */
    varName(off) {
        if (this.variables.has(off)) return this.variables.get(off);
        let best = null;
        for (const [start, name] of this.variables) if (start < off && (best === null || start > best[0])) best = [start, name];
        return best && off - best[0] < 64 ? `${best[1]}+${off - best[0]}` : null;
    }

    /** El nombre del lugar del código (la etiqueta o la rutina) o su dirección. */
    placeName(ip) {
        const name = this.labels?.get(ip);
        return name ? `${name} (IP ${hex(ip, 4)}h)` : `IP ${hex(ip, 4)}h`;
    }

    /** La línea del código de la orden que vive en esa dirección. */
    lineAt(ip) {
        const i = this.machine.p.byAddress.get(ip);
        return i === undefined ? null : this.machine.p.instructions[i].line;
    }

    /** Por qué la orden siguió de largo o saltó (los saltos, los bucles, las llamadas y las vueltas). */
    flowOf(ins, flagsBefore) {
        const m = this.machine;
        if (m.halted) return null;
        const next = ins.address + ins.length;
        const jumped = m.ip !== next;
        const where = this.placeName(m.ip);
        const name = ins.m;
        let text = null;
        if (ins.cond && CONDITIONS[ins.cond]) {
            const [rule, used] = CONDITIONS[ins.cond];
            const seen = used.map((f) => `${f.toUpperCase()} = ${flagsBefore[f]}`).join(', ');
            text = `${name} salta solo si ${rule}. Con ${seen}, ${jumped ? `se cumple: saltó a ${where}.` : 'no se cumple: siguió con la orden de abajo.'}`;
        } else if (/^loop/.test(name)) {
            const extra = { loope: ' y ZF = 1', loopz: ' y ZF = 1', loopne: ' y ZF = 0', loopnz: ' y ZF = 0' }[name] ?? '';
            text = `${name} le resta 1 a CX (quedó en ${hex(m.get('cx'), 4)}h) y vuelve si CX no es 0${extra}: ${jumped ? `volvió a ${where}.` : 'terminó el bucle y siguió de largo.'}`;
        } else if (name === 'jcxz') {
            text = `jcxz salta solo si CX = 0: ${jumped ? `saltó a ${where}.` : 'CX no es 0, siguió de largo.'}`;
        } else if (name === 'jmp') {
            text = `jmp salta siempre: el programa sigue en ${where}.`;
        } else if (name === 'call') {
            text = `call guardó en la pila la dirección de vuelta (${hex(next, 4)}h, la orden de abajo) y fue a ${where}.`;
        } else if (name === 'ret' || name === 'retn') {
            text = `ret sacó de la pila la dirección de vuelta y volvió a ${where}, justo después del call.`;
        }
        return text ? { jumped, text } : null;
    }

    /** Cómo se ve un operando por dentro: registro, número dentro de la orden o cajón (con su dirección). */
    operand(op, ins) {
        const m = this.machine;
        if (op.k === 'reg' || op.k === 'sreg') {
            return { kind: 'registro', text: `${op.r.toUpperCase()} (${op.size} bits)` };
        }
        if (op.k === 'imm') {
            if (ins.m === 'int') return { kind: 'número de interrupción', text: `${hex(op.v & 0xff, 2)}h (el servicio lo elige AH)` };
            if (op.label) return { kind: 'dirección del código', text: `${op.label.name} = ${hex(op.v, 4)}h` };
            if (op.sym?.kind === 'segment') return { kind: 'segmento', text: `@data = ${hex(m.dataSeg, 4)}h` };
            const bits = ins.size || (ins.ops[0]?.size ?? 16) || 16;
            return { kind: 'inmediato (viaja dentro de la orden)', text: `${hex(op.v & (bits === 8 ? 0xff : 0xffff), bits === 8 ? 2 : 4)}h = ${op.v}` };
        }
        const seg = m.segOf(op);
        const segName = (op.seg ?? (op.base === 'bp' ? 'ss' : 'ds')).toUpperCase();
        const off = m.ea(op);
        const terms = [];
        if (op.base) terms.push(`${op.base.toUpperCase()} ${hex(m.get(op.base), 4)}h`);
        if (op.index) terms.push(`${op.index.toUpperCase()} ${hex(m.get(op.index), 4)}h`);
        if (op.disp || terms.length === 0) terms.push(`${hex(op.disp & 0xffff, 4)}h${op.sym?.kind === 'data' ? ` (${op.sym.name})` : ''}`);
        const size = op.size || ins.size;
        const name = segName === 'DS' ? this.varName(off) : null;
        return {
            kind: `memoria, ${size === 8 ? '1 byte' : size === 16 ? '2 bytes (word)' : 'sin tamaño'}`,
            text: `${terms.join(' + ')} = ${hex(off, 4)}h${name ? ` (${name})` : ''} · ${segName}:${hex(off, 4)} = ${hex(seg, 4)}:${hex(off, 4)} → dirección física ${hex(seg * 16 + off, 5)}h`,
        };
    }

    /** La capa técnica de la orden: tamaño de los operandos, dónde vive, cuántos bytes ocupa y cómo se movió IP. */
    techOf(ins, ipBefore, operands, flow) {
        const m = this.machine;
        const roles = operands.length === 2 ? ['destino', 'origen'] : ['operando'];
        const size = ins.size || ins.ops.find((o) => o.size)?.size || 0;
        return {
            size: size === 8 ? 'trabaja con bytes (8 bits)' : size === 16 ? 'trabaja con words (16 bits)' : null,
            code: `vive en CS:${hex(ipBefore, 4)} y ocupa ${ins.length} byte${ins.length === 1 ? '' : 's'} de código máquina`,
            // D110: los bytes que leería un 8086 de verdad (encoder.js, comprobado con objdump).
            bytes: (() => {
                const bytes = encode(ins, { dataSeg: m.dataSeg });
                return bytes ? hexBytes(bytes) : null;
            })(),
            ip: m.halted ? null : flow?.jumped
                ? `IP: ${hex(ipBefore, 4)}h → ${hex(m.ip, 4)}h (saltó; sin el salto habría ido a ${hex(ins.address + ins.length, 4)}h)`
                : `IP: ${hex(ipBefore, 4)}h + ${ins.length} = ${hex(m.ip, 4)}h (la orden de abajo)`,
            operands: operands.map((o, i) => ({ role: roles[i] ?? 'operando', ...o })),
        };
    }

    describe(ins, before, flagsBefore, memBefore, screenBefore) {
        const m = this.machine;
        const ch = this.lastChanges;
        const regs = REGISTER_ORDER.filter((r) => r !== 'ip' && m.get(r) !== before[r])
            .map((r) => ({ name: r.toUpperCase(), from: hex(before[r], 4), to: hex(m.get(r), 4) }));
        const flags = FLAG_ORDER.filter((f) => m.flag(f) !== flagsBefore[f]).map((f) => `${f.toUpperCase()} ${flagsBefore[f]}→${m.flag(f)}`);
        const stackSeg = m.sregs.ss * 16;
        const isStack = (a) => a >= stackSeg && a < stackSeg + 0x10000;
        const cell = (a, from = null) => {
            const off = this.dataOffset(a);
            const name = off === null ? null : this.varName(off);
            return { address: off === null ? null : hex(off, 4), name, value: hex(m.mem[a], 2), from: from === null ? null : hex(from, 2) };
        };
        const written = [...ch.mem].filter((a) => !isStack(a));
        const read = [...ch.read].filter((a) => !isStack(a) && !ch.mem.has(a));
        const screenChanged = m.screen.text() !== screenBefore;
        // Lo que más confunde al empezar: el número que aparece es una DIRECCIÓN, no un dato.
        const text = ins?.text ?? '';
        const off = /offset\s+([A-Za-z_?][\w?]*)/i.exec(text);
        const note = /@data/i.test(text)
            ? '@data es la dirección del segmento de datos: el lugar de la memoria donde empiezan los cajones. No es un dato: es «dónde están».'
            : off ? `offset ${off[1]} es la dirección del cajón donde empieza ${off[1]} (no lo que hay adentro).` : null;
        this.explain = {
            text,
            note,
            line: ins?.line ?? null,
            regs,
            flags,
            // Las cadenas largas (INT 21h 09h) leen muchos cajones: se muestran los primeros.
            reads: read.slice(0, 6).map((a) => cell(a)),
            moreReads: Math.max(0, read.length - 6),
            writes: written.slice(0, 6).map((a) => cell(a, memBefore.get(a))),
            stack: before.sp !== m.get('sp') ? (m.get('sp') < before.sp ? 'apiló un plato en la torre' : 'sacó un plato de la torre') : null,
            screen: screenChanged,
        };
        this.pulse = {
            screen: screenChanged,
            memory: written.length > 0 || read.length > 0,
            stack: before.sp !== m.get('sp') || [...ch.mem].some(isStack),
        };
        // La memoria va sola a donde pasó algo (si el alumno no eligió otro lugar).
        const focus = [...written, ...read].map((a) => this.dataOffset(a)).find((off) => off !== null);
        if (focus !== undefined && !this.memoryManual) {
            const base = this.memoryBase ?? 0;
            if (focus < base || focus >= base + 128) this.memoryBase = Math.max(0, (focus & 0xfff0) - 16);
        }
    }

    /**
     * Corre hasta terminar, pedir una tecla, que lo paren o pasarse del límite (el bucle infinito).
     * @param onTick se llama entre tandas, para redibujar
     */
    async runToEnd(onTick = () => {}) {
        this.stopped = false;
        this.explain = null;
        const screenBefore = this.machine.screen.text();
        let done = 0;
        for (;;) {
            const r = this.machine.run(20_000);
            done += 20_000;
            if (r !== 'ok') {
                this.afterRun(screenBefore);
                return r;
            }
            if (this.stopped) return 'stopped';
            if (done >= LIMIT) return 'loop';
            onTick();
            await new Promise((resolve) => setTimeout(resolve, 0));
        }
    }

    /** Después de correr de una: se marcan los cajones de datos que quedaron distintos y lo que cambió palpita. */
    afterRun(screenBefore) {
        const m = this.machine;
        const base = m.dataSeg * 16;
        const changed = new Set();
        m.p.data.forEach((v, i) => {
            if (m.mem[base + i] !== v) changed.add(base + i);
        });
        this.lastChanges = { regs: new Set(), flags: new Set(), mem: changed, read: new Set() };
        this.pulse = { screen: m.screen.text() !== screenBefore, memory: changed.size > 0, stack: false };
        const first = [...changed][0];
        if (first !== undefined && !this.memoryManual) this.memoryBase = Math.max(0, ((first - base) & 0xfff0) - 16);
    }

    stop() {
        this.stopped = true;
    }

    feed(text) {
        this.machine.feed(text);
    }

    /** Lo que se compara con la salida esperada: la pantalla y, si la micro-misión lo pide, el estado. */
    result() {
        const m = this.machine;
        const output = m.screen.text();
        const report = this.checks ? stateReport(m.snapshot ?? m, this.checks) : '';
        return report ? (output ? `${output}\n${report}` : report) : output;
    }

    /** Todo lo que dibuja el tablero, en objetos simples (para Alpine). */
    view() {
        if (!this.machine) return null;
        // Al terminar, el tablero muestra cómo quedó el Gólem al llegar a fin: (lo que se comprueba), no el apagado.
        const atFin = Boolean(this.machine.halted && this.machine.snapshot);
        const m = atFin ? this.machine.snapshot : this.machine;
        const ch = atFin ? { ...this.lastChanges, regs: new Set(), flags: new Set() } : this.lastChanges;
        const registers = REGISTER_ORDER.map((r) => ({
            name: r.toUpperCase(),
            value: hex(m.get(r), 4),
            // D110: el mismo número en decimal (sin y con signo) y en binario, al tocar la palanca.
            dec: m.get(r),
            signed: (m.get(r) << 16) >> 16,
            bin: nibbles(m.get(r), 16),
            high: r.length === 2 && 'abcd'.includes(r[0]) && r[1] === 'x' ? hex(m.get(`${r[0]}h`), 2) : null,
            low: r.length === 2 && 'abcd'.includes(r[0]) && r[1] === 'x' ? hex(m.get(`${r[0]}l`), 2) : null,
            changed: ch.regs.has(r),
        }));
        const flags = FLAG_ORDER.map((f) => ({ name: f.toUpperCase(), value: m.flag(f), changed: ch.flags.has(f), info: FLAG_INFO[f] }));
        // Dentro de qué rutinas está ahora (main → mostrar → …).
        const calls = [this.placeName(this.machine.p.entry).replace(/ \(IP.*$/, ''), ...this.machine.calls.map((c) => this.placeName(c.target).replace(/ \(IP.*$/, ''))];
        return {
            trail: [...this.trail].reverse(),
            calls,
            registers,
            flags,
            memory: this.memory(m, ch),
            stack: this.stack(m),
            screenHtml: this.screenHtml(),
            line: this.currentLine(),
            steps: this.machine.steps,
            atFin,
            explain: this.explain,
            pulse: this.pulse,
        };
    }

    /** Los cajones: 8 filas de 16 bytes desde el comienzo de los datos (o desde donde se pidió). */
    memory(m = this.machine, ch = this.lastChanges, rows = 8) {
        const base = this.memoryBase ?? 0;
        const out = [];
        for (let r = 0; r < rows; r++) {
            const offset = (base + r * 16) & 0xffff;
            const cells = [];
            for (let c = 0; c < 16; c++) {
                const off = (offset + c) & 0xffff;
                const phys = m.phys(m.dataSeg, off);
                const v = m.mem[phys];
                cells.push({ value: hex(v, 2), char: v >= 32 && v < 127 ? String.fromCharCode(v) : '·', changed: ch.mem.has(phys), read: Boolean(ch.read?.has(phys)) && !ch.mem.has(phys), name: this.variables.get(off) ?? null });
            }
            out.push({ address: hex(offset, 4), cells });
        }
        return out;
    }

    /** La torre de platos: desde SP hasta el fondo de la pila (lo de arriba es lo último que se apiló). */
    stack(m = this.machine, max = 10) {
        const out = [];
        for (let sp = m.get('sp'); sp < m.initialSp && out.length < max; sp += 2) {
            out.push({ address: hex(sp, 4), value: hex(m.read16(m.sregs.ss, sp), 4), top: sp === m.get('sp') });
        }
        return out;
    }

    /** La pantalla: el historial en texto plano y lo visible con sus colores (INT 10h, 09h). */
    screenHtml() {
        const s = this.machine.screen;
        const history = s.history.map(escapeHtml);
        const rows = s.lines().map((line, r) => {
            let html = '';
            for (let c = 0; c < line.length; c++) {
                const color = s.colors[r][c];
                const ch = escapeHtml(line[c]);
                html += color === 7 ? ch : `<span style="color:${CGA[color & 15]};background:${(color >> 4) & 7 ? CGA[(color >> 4) & 7] : 'transparent'}">${ch}</span>`;
            }
            return html;
        });
        return [...history, ...rows].join('\n');
    }

    /** El motivo del final, para el alumno. */
    endMessage() {
        const h = this.halted;
        if (!h) return null;
        if (h.normal) return null;
        if (h.reason.startsWith('Divide overflow')) return 'El Ogro de la división: dividiste por cero o el cociente no entra en el registro (Divide overflow).';
        if (h.reason.startsWith('se termino la entrada')) return null;
        return h.reason;
    }
}

export { FLAG_BITS };
