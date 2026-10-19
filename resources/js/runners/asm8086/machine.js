// El Gólem por dentro (D110): un 8086 que ejecuta las instrucciones que armó assembler.js, con la memoria
// de 1 MB, los registros, las banderas y las interrupciones de DOS y de la BIOS que usa el curso (las mismas
// que atiende herramientas/dos8086.py del material, para que la salida sea idéntica).

import { JUMP_CONDITIONS } from './assembler.js';

const R16 = { ax: 0, cx: 1, dx: 2, bx: 3, sp: 4, bp: 5, si: 6, di: 7 };
const R8 = { al: [0, 0], cl: [1, 0], dl: [2, 0], bl: [3, 0], ah: [0, 8], ch: [1, 8], dh: [2, 8], bh: [3, 8] };
const SEGS = ['es', 'cs', 'ss', 'ds'];
export const FLAG_BITS = { cf: 0, pf: 2, af: 4, zf: 6, sf: 7, tf: 8, if: 9, df: 10, of: 11 };

export const PSP = 0x0700;
const COLS = 80;
const ROWS = 25;
export const CLEARED = '----- (aca se borra la pantalla) -----';

/** La pantalla de texto 80×25 de DOS, con el color de cada celda (para el tablero) y el historial. */
export class Screen {
    constructor() {
        this.history = [];
        this.clear();
    }

    clear() {
        this.cells = Array.from({ length: ROWS }, () => Array(COLS).fill(' '));
        this.colors = Array.from({ length: ROWS }, () => Array(COLS).fill(7));
        this.row = 0;
        this.col = 0;
    }

    lines() {
        const rows = this.cells.map((r) => r.join('').replace(/\s+$/, ''));
        while (rows.length && !rows[rows.length - 1]) rows.pop();
        return rows;
    }

    wipe() {
        const lines = this.lines();
        if (lines.length || this.history.length) this.history.push(...lines, CLEARED);
        this.clear();
    }

    down() {
        this.row++;
        if (this.row === ROWS) {
            this.history.push(this.cells.shift().join('').replace(/\s+$/, ''));
            this.colors.shift();
            this.cells.push(Array(COLS).fill(' '));
            this.colors.push(Array(COLS).fill(7));
            this.row = ROWS - 1;
        }
    }

    put(c, color = null) {
        if (c === 0x0d) this.col = 0;
        else if (c === 0x0a) this.down();
        else if (c === 0x08) this.col = Math.max(0, this.col - 1);
        else if (c === 0x07) { /* campana */ }
        else {
            this.cells[this.row][this.col] = c === 0 ? ' ' : cp437(c);
            if (color !== null) this.colors[this.row][this.col] = color;
            this.col++;
            if (this.col === COLS) {
                this.col = 0;
                this.down();
            }
        }
    }

    move(row, col) {
        this.row = Math.min(row, ROWS - 1);
        this.col = Math.min(col, COLS - 1);
    }

    text() {
        return [...this.history, ...this.lines()].join('\n');
    }
}

const CP437_HIGH = 'ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■ ';
function cp437(c) {
    if (c >= 0x20 && c < 0x7f) return String.fromCharCode(c);
    if (c >= 0x80) return CP437_HIGH[c - 0x80];
    // Como dos8086.py (cp437 de Python): los de control salen tal cual (el tabulador es un tabulador).
    return String.fromCharCode(c);
}

/** Termina la ejecución (con el motivo, como dos8086.py). */
class Halt {
    constructor(reason, code = 0, normal = false) {
        this.reason = reason;
        this.code = code;
        this.normal = normal;
    }
}

export class Machine {
    /**
     * @param program lo que devuelve assemble()
     * @param options.input  bytes de la entrada (lo que se «tipea»)
     * @param options.interactive si true, cuando se acaba la entrada pide una tecla en vez de terminar
     */
    constructor(program, { input = '', interactive = false } = {}) {
        this.p = program;
        this.mem = new Uint8Array(0x100000);
        this.regs = new Uint16Array(8);
        this.sregs = { es: PSP, cs: PSP + 0x10, ss: 0, ds: PSP };
        this.flags = 0x0002 | (1 << FLAG_BITS.if);
        this.screen = new Screen();
        this.input = typeof input === 'string' ? Array.from(new TextEncoder().encode(input)) : Array.from(input);
        this.inPos = 0;
        this.interactive = interactive;
        this.halted = null;
        this.waiting = null;
        this.steps = 0;
        this.changes = null;
        // D110: el «Estado esperado» se mira al llegar a la etiqueta fin: (antes de apagar el Gólem).
        const fin = program.symbols.get('fin');
        this.snapshotAt = fin && fin.address !== undefined ? fin.address : -1;
        this.snapshot = null;

        // Imagen del .EXE: código, datos y pila en párrafos seguidos (como lo cargaría DOS).
        const codeSeg = PSP + 0x10;
        const codeParas = Math.ceil(Math.max(program.codeSize, 1) / 16);
        this.dataSeg = codeSeg + codeParas;
        const dataParas = Math.ceil(Math.max(program.data.length, 1) / 16);
        this.sregs.cs = codeSeg;
        this.sregs.ss = this.dataSeg + dataParas;
        this.regs[R16.sp] = program.stackSize & 0xffff;
        this.initialSp = this.regs[R16.sp];
        this.ip = program.entry;
        this.mem.set(program.data, this.dataSeg * 16);
        this.mem[PSP * 16] = 0xcd;
        this.mem[PSP * 16 + 1] = 0x20;
        // El código no está en bytes de verdad: se ve como NOP en la memoria.
        this.mem.fill(0x90, codeSeg * 16, codeSeg * 16 + program.codeSize);
    }

    // ------------------------------------------------ registros y memoria

    get(name) {
        if (name in R16) return this.regs[R16[name]];
        if (name in R8) {
            const [i, shift] = R8[name];
            return (this.regs[i] >> shift) & 0xff;
        }
        if (SEGS.includes(name)) return this.sregs[name];
        if (name === 'ip') return this.ip;
        if (name === 'flags' || name === 'fl') return this.flags;
        if (name in FLAG_BITS) return (this.flags >> FLAG_BITS[name]) & 1;
        throw new Error(`registro desconocido: ${name}`);
    }

    set(name, value) {
        this.mark(name);
        if (name in R16) this.regs[R16[name]] = value & 0xffff;
        else if (name in R8) {
            const [i, shift] = R8[name];
            this.regs[i] = shift ? (this.regs[i] & 0x00ff) | ((value & 0xff) << 8) : (this.regs[i] & 0xff00) | (value & 0xff);
        } else if (SEGS.includes(name)) this.sregs[name] = value & 0xffff;
    }

    mark(name) {
        if (!this.changes) return;
        const full = name in R8 ? ['ax', 'cx', 'dx', 'bx'][R8[name][0]] : name;
        this.changes.regs.add(full);
    }

    flag(name) {
        return (this.flags >> FLAG_BITS[name]) & 1;
    }

    setFlag(name, on) {
        const bit = 1 << FLAG_BITS[name];
        const before = this.flags;
        this.flags = on ? this.flags | bit : this.flags & ~bit;
        if (this.changes && before !== this.flags) this.changes.flags.add(name);
    }

    phys(seg, off) {
        return ((seg << 4) + (off & 0xffff)) & 0xfffff;
    }

    read8(seg, off) {
        return this.mem[this.phys(seg, off)];
    }

    read16(seg, off) {
        return this.read8(seg, off) | (this.read8(seg, off + 1) << 8);
    }

    write8(seg, off, v) {
        const a = this.phys(seg, off);
        this.mem[a] = v & 0xff;
        if (this.changes) this.changes.mem.add(a);
    }

    write16(seg, off, v) {
        this.write8(seg, off, v);
        this.write8(seg, off + 1, v >> 8);
    }

    push(v) {
        const sp = (this.regs[R16.sp] - 2) & 0xffff;
        this.set('sp', sp);
        this.write16(this.sregs.ss, sp, v);
    }

    pop() {
        const sp = this.regs[R16.sp];
        const v = this.read16(this.sregs.ss, sp);
        this.set('sp', sp + 2);
        return v;
    }

    // ------------------------------------------------ operandos

    ea(op) {
        let off = op.disp;
        if (op.base) off += this.regs[R16[op.base]];
        if (op.index) off += this.regs[R16[op.index]];
        return off & 0xffff;
    }

    segOf(op) {
        if (op.seg) return this.sregs[op.seg];
        return op.base === 'bp' ? this.sregs.ss : this.sregs.ds;
    }

    value(op, size) {
        if (op.k === 'reg' || op.k === 'sreg') return this.get(op.r);
        if (op.k === 'imm') {
            if (op.sym && op.sym.kind === 'segment') return this.dataSeg;
            return op.v & (size === 8 ? 0xff : 0xffff);
        }
        const seg = this.segOf(op);
        const off = this.ea(op);
        return size === 8 ? this.read8(seg, off) : this.read16(seg, off);
    }

    store(op, size, v) {
        if (op.k === 'reg' || op.k === 'sreg') return this.set(op.r, v);
        const seg = this.segOf(op);
        const off = this.ea(op);
        if (size === 8) this.write8(seg, off, v);
        else this.write16(seg, off, v);
    }

    // ------------------------------------------------ banderas

    szp(v, size) {
        const mask = size === 8 ? 0xff : 0xffff;
        v &= mask;
        this.setFlag('zf', v === 0);
        this.setFlag('sf', (v >> (size - 1)) & 1);
        let bits = v & 0xff;
        bits ^= bits >> 4;
        bits ^= bits >> 2;
        bits ^= bits >> 1;
        this.setFlag('pf', !(bits & 1));
    }

    arith(op, a, b, size, carry = 0) {
        const mask = size === 8 ? 0xff : 0xffff;
        const sign = size === 8 ? 0x80 : 0x8000;
        let r;
        if (op === 'add') {
            r = a + b + carry;
            this.setFlag('cf', r > mask);
            this.setFlag('of', ((a ^ r) & (b ^ r) & sign) !== 0);
            this.setFlag('af', ((a ^ b ^ r) & 0x10) !== 0);
        } else {
            r = a - b - carry;
            this.setFlag('cf', r < 0);
            this.setFlag('of', ((a ^ b) & (a ^ r) & sign) !== 0);
            this.setFlag('af', ((a ^ b ^ r) & 0x10) !== 0);
        }
        r &= mask;
        this.szp(r, size);
        return r;
    }

    logic(r, size) {
        this.setFlag('cf', 0);
        this.setFlag('of', 0);
        this.szp(r, size);
        return r & (size === 8 ? 0xff : 0xffff);
    }

    condition(c) {
        const f = (n) => this.flag(n);
        switch (c) {
            case 'z': return f('zf');
            case 'nz': return !f('zf');
            case 'c': return f('cf');
            case 'nc': return !f('cf');
            case 'a': return !f('cf') && !f('zf');
            case 'be': return f('cf') || f('zf');
            case 'g': return !f('zf') && f('sf') === f('of');
            case 'ge': return f('sf') === f('of');
            case 'l': return f('sf') !== f('of');
            case 'le': return f('zf') || f('sf') !== f('of');
            case 's': return f('sf');
            case 'ns': return !f('sf');
            case 'o': return f('of');
            case 'no': return !f('of');
            case 'p': return f('pf');
            case 'np': return !f('pf');
            default: return false;
        }
    }

    // ------------------------------------------------ ejecución

    /** El índice de la instrucción en IP (o null si IP no apunta a una instrucción). */
    current() {
        const i = this.p.byAddress.get(this.ip);
        return i === undefined ? null : this.p.instructions[i];
    }

    /**
     * Ejecuta una instrucción. Devuelve 'ok', 'halt' (terminó, ver this.halted) o 'input' (espera una tecla).
     * Con track=true deja en this.changes qué registros, banderas y bytes de memoria cambió.
     */
    step(track = false) {
        if (this.halted) return 'halt';
        this.changes = track ? { regs: new Set(), flags: new Set(), mem: new Set() } : null;
        const ins = this.current();
        if (!ins) {
            this.halted = new Halt(`el Gólem saltó a una dirección sin órdenes (IP = ${hex(this.ip, 4)}h)`, 4);
            return 'halt';
        }
        const before = this.ip;
        if (before === this.snapshotAt && !this.snapshot) this.snapshot = this.freeze();
        this.ip = (ins.address + ins.length) & 0xffff;
        try {
            this.exec(ins);
        } catch (e) {
            if (e instanceof Halt) {
                this.halted = e;
                return 'halt';
            }
            if (e === WAIT) {
                this.ip = before;
                return 'input';
            }
            throw e;
        }
        this.steps++;
        if (track && this.ip !== before) this.changes.regs.add('ip');
        return 'ok';
    }

    /** Una copia del estado (registros, banderas y datos) para el informe de una micro-misión. */
    freeze() {
        const copy = Object.create(Machine.prototype);
        copy.p = this.p;
        copy.regs = this.regs.slice();
        copy.sregs = { ...this.sregs };
        copy.flags = this.flags;
        copy.ip = this.ip;
        copy.dataSeg = this.dataSeg;
        copy.initialSp = this.initialSp;
        copy.steps = this.steps;
        copy.mem = this.mem.slice();
        copy.changes = null;
        return copy;
    }

    /** Corre hasta terminar, esperar una tecla o agotar `limit` instrucciones. */
    run(limit) {
        for (let i = 0; i < limit; i++) {
            const r = this.step(false);
            if (r !== 'ok') return r;
        }
        return 'ok';
    }

    exec(ins) {
        const [a, b] = ins.ops;
        const s = ins.size;
        switch (ins.m) {
            case 'mov':
                return this.store(a, s, this.value(b, s));
            case 'xchg': {
                const va = this.value(a, s);
                this.store(a, s, this.value(b, s));
                return this.store(b, s, va);
            }
            case 'lea':
                return this.set(a.r, this.ea(b));
            case 'push':
                return this.push(this.value(a, 16));
            case 'pop':
                return this.store(a, 16, this.pop());
            case 'pushf':
                return this.push(this.flags);
            case 'popf':
                this.flags = (this.pop() & 0x0fd5) | 0x0002;
                if (this.changes) Object.keys(FLAG_BITS).forEach((f) => this.changes.flags.add(f));
                return;
            case 'add':
            case 'adc':
                return this.store(a, s, this.arith('add', this.value(a, s), this.value(b, s), s, ins.m === 'adc' ? this.flag('cf') : 0));
            case 'sub':
            case 'sbb':
                return this.store(a, s, this.arith('sub', this.value(a, s), this.value(b, s), s, ins.m === 'sbb' ? this.flag('cf') : 0));
            case 'cmp':
                this.arith('sub', this.value(a, s), this.value(b, s), s);
                return;
            case 'inc':
            case 'dec': {
                const cf = this.flag('cf');
                const r = this.arith(ins.m === 'inc' ? 'add' : 'sub', this.value(a, s), 1, s);
                this.setFlag('cf', cf);
                return this.store(a, s, r);
            }
            case 'neg': {
                const v = this.value(a, s);
                const r = this.arith('sub', 0, v, s);
                this.setFlag('cf', v !== 0);
                return this.store(a, s, r);
            }
            case 'not':
                return this.store(a, s, ~this.value(a, s));
            case 'and':
                return this.store(a, s, this.logic(this.value(a, s) & this.value(b, s), s));
            case 'or':
                return this.store(a, s, this.logic(this.value(a, s) | this.value(b, s), s));
            case 'xor':
                return this.store(a, s, this.logic(this.value(a, s) ^ this.value(b, s), s));
            case 'test':
                this.logic(this.value(a, s) & this.value(b, s), s);
                return;
            case 'mul':
            case 'imul':
                return this.multiply(a, s, ins.m === 'imul');
            case 'div':
            case 'idiv':
                return this.divide(a, s, ins.m === 'idiv');
            case 'cbw':
                return this.set('ax', (this.get('al') & 0x80 ? 0xff00 : 0) | this.get('al'));
            case 'cwd':
                return this.set('dx', this.get('ax') & 0x8000 ? 0xffff : 0);
            case 'shl':
            case 'shr':
            case 'sar':
            case 'rol':
            case 'ror':
            case 'rcl':
            case 'rcr':
                return this.shift(ins.m, a, s, b.k === 'imm' ? 1 : this.get('cl'));
            case 'jmp':
                this.ip = a.k === 'imm' ? a.v : this.value(a, 16);
                return;
            case 'call': {
                const target = a.k === 'imm' ? a.v : this.value(a, 16);
                this.push(this.ip);
                this.ip = target;
                return;
            }
            case 'ret': {
                if (this.regs[R16.sp] === this.initialSp) throw new Halt('fin (RET con la pila vacía)', 0, true);
                this.ip = this.pop();
                if (a) this.set('sp', this.regs[R16.sp] + a.v);
                return;
            }
            case 'loop':
            case 'loope':
            case 'loopz':
            case 'loopne':
            case 'loopnz': {
                const cx = (this.get('cx') - 1) & 0xffff;
                this.set('cx', cx);
                let go = cx !== 0;
                if (ins.m === 'loope' || ins.m === 'loopz') go = go && this.flag('zf');
                if (ins.m === 'loopne' || ins.m === 'loopnz') go = go && !this.flag('zf');
                if (go) this.ip = a.v;
                return;
            }
            case 'jcxz':
                if (this.get('cx') === 0) this.ip = a.v;
                return;
            case 'clc': return this.setFlag('cf', 0);
            case 'stc': return this.setFlag('cf', 1);
            case 'cmc': return this.setFlag('cf', !this.flag('cf'));
            case 'cld': return this.setFlag('df', 0);
            case 'std': return this.setFlag('df', 1);
            case 'cli': return this.setFlag('if', 0);
            case 'sti': return this.setFlag('if', 1);
            case 'nop': return;
            case 'lahf': return this.set('ah', this.flags & 0xd5);
            case 'sahf':
                ['cf', 'pf', 'af', 'zf', 'sf'].forEach((f) => this.setFlag(f, (this.get('ah') >> FLAG_BITS[f]) & 1));
                return;
            case 'xlat':
                return this.set('al', this.read8(this.sregs.ds, this.get('bx') + this.get('al')));
            case 'hlt':
                throw new Halt('HLT: el Gólem se detuvo', 0, true);
            case 'int':
                return this.interrupt(a.v & 0xff);
            default:
                if (ins.m.length === 5 && /^(movs|lods|stos|cmps|scas)[bw]$/.test(ins.m)) return this.string(ins);
                if (ins.cond) {
                    if (this.condition(ins.cond)) this.ip = a.v;
                    return;
                }
                throw new Halt(`instrucción no soportada: ${ins.m}`, 2);
        }
    }

    multiply(a, s, signed) {
        if (s === 8) {
            let x = this.get('al');
            let y = this.value(a, 8);
            if (signed) {
                x = (x << 24) >> 24;
                y = (y << 24) >> 24;
            }
            const r = (x * y) & 0xffff;
            this.set('ax', r);
            const high = signed ? ((r << 16) >> 16) !== ((r << 24) >> 24) : (r >> 8) !== 0;
            this.setFlag('cf', high);
            this.setFlag('of', high);
        } else {
            let x = this.get('ax');
            let y = this.value(a, 16);
            if (signed) {
                x = (x << 16) >> 16;
                y = (y << 16) >> 16;
            }
            const r = x * y;
            const lo = r & 0xffff;
            const hi = Math.floor(r / 0x10000) & 0xffff;
            this.set('ax', lo);
            this.set('dx', hi);
            const high = signed ? !(r >= -0x8000 && r <= 0x7fff) : hi !== 0;
            this.setFlag('cf', high);
            this.setFlag('of', high);
        }
    }

    divide(a, s, signed) {
        const overflow = () => {
            throw new Halt('Divide overflow (division por cero o cociente que no entra)', 1);
        };
        if (s === 8) {
            let n = this.get('ax');
            let d = this.value(a, 8);
            if (signed) {
                n = (n << 16) >> 16;
                d = (d << 24) >> 24;
            }
            if (d === 0) overflow();
            const q = Math.trunc(n / d);
            const r = n - q * d;
            if (signed ? q > 127 || q < -128 : q > 0xff) overflow();
            this.set('al', q);
            this.set('ah', r);
        } else {
            let n = this.get('dx') * 0x10000 + this.get('ax');
            let d = this.value(a, 16);
            if (signed) {
                n = n > 0x7fffffff ? n - 0x100000000 : n;
                d = (d << 16) >> 16;
            }
            if (d === 0) overflow();
            const q = Math.trunc(n / d);
            const r = n - q * d;
            if (signed ? q > 0x7fff || q < -0x8000 : q > 0xffff) overflow();
            this.set('ax', q);
            this.set('dx', r);
        }
    }

    shift(m, a, s, count) {
        count &= 0x1f;
        if (!count) return;
        const mask = s === 8 ? 0xff : 0xffff;
        const top = s - 1;
        let v = this.value(a, s);
        let cf = this.flag('cf');
        for (let i = 0; i < count; i++) {
            switch (m) {
                case 'shl': cf = (v >> top) & 1; v = (v << 1) & mask; break;
                case 'shr': cf = v & 1; v >>= 1; break;
                case 'sar': cf = v & 1; v = (v >> 1) | (v & (1 << top)); break;
                case 'rol': cf = (v >> top) & 1; v = ((v << 1) | cf) & mask; break;
                case 'ror': cf = v & 1; v = (v >> 1) | (cf << top); break;
                case 'rcl': { const out = (v >> top) & 1; v = ((v << 1) | cf) & mask; cf = out; break; }
                case 'rcr': { const out = v & 1; v = (v >> 1) | (cf << top); cf = out; break; }
                default: break;
            }
        }
        this.setFlag('cf', cf);
        const msb = (v >> top) & 1;
        if (m === 'shl' || m === 'rol' || m === 'rcl') this.setFlag('of', msb ^ cf);
        else if (m === 'shr') this.setFlag('of', (this.value(a, s) >> top) & 1);
        else if (m === 'sar') this.setFlag('of', 0);
        else this.setFlag('of', msb ^ ((v >> (top - 1)) & 1));
        if (m === 'shl' || m === 'shr' || m === 'sar') this.szp(v, s);
        this.store(a, s, v);
    }

    string(ins) {
        const op = ins.m.slice(0, 4);
        const size = ins.m.endsWith('w') ? 16 : 8;
        const n = size / 8;
        const step = this.flag('df') ? -n : n;
        const once = () => {
            const si = this.get('si');
            const di = this.get('di');
            const ds = this.sregs.ds;
            const es = this.sregs.es;
            const rd = (seg, off) => (size === 8 ? this.read8(seg, off) : this.read16(seg, off));
            const wr = (seg, off, v) => (size === 8 ? this.write8(seg, off, v) : this.write16(seg, off, v));
            const acc = size === 8 ? 'al' : 'ax';
            if (op === 'movs') {
                wr(es, di, rd(ds, si));
                this.set('si', si + step);
                this.set('di', di + step);
            } else if (op === 'lods') {
                this.set(acc, rd(ds, si));
                this.set('si', si + step);
            } else if (op === 'stos') {
                wr(es, di, this.get(acc));
                this.set('di', di + step);
            } else if (op === 'cmps') {
                this.arith('sub', rd(ds, si), rd(es, di), size);
                this.set('si', si + step);
                this.set('di', di + step);
            } else if (op === 'scas') {
                this.arith('sub', this.get(acc), rd(es, di), size);
                this.set('di', di + step);
            }
        };
        if (!ins.prefix) return once();
        while (this.get('cx') !== 0) {
            once();
            this.set('cx', this.get('cx') - 1);
            if ((op === 'cmps' || op === 'scas') && ins.prefix === 'repe' && !this.flag('zf')) break;
            if ((op === 'cmps' || op === 'scas') && ins.prefix === 'repne' && this.flag('zf')) break;
        }
    }

    // ------------------------------------------------ entrada

    /** Una tecla (01h, 07h, 08h, 16h): saltea los Enter sueltos, como dos8086.py. */
    key() {
        while (this.inPos < this.input.length) {
            const c = this.input[this.inPos++];
            if (c === 0x0d || c === 0x0a) continue;
            if (this.input[this.inPos] === 0x0a) this.inPos++;
            return c;
        }
        return this.noInput('se termino la entrada (el programa pidio mas teclas)', 'key');
    }

    noInput(reason, kind) {
        if (this.interactive) {
            this.waiting = kind;
            throw WAIT;
        }
        throw new Halt(reason, 0);
    }

    /** Lo que el alumno tipea en el tablero mientras el programa espera. */
    feed(text) {
        this.input.push(...new TextEncoder().encode(text));
        this.waiting = null;
    }

    // ------------------------------------------------ interrupciones

    interrupt(n) {
        const ah = this.get('ah');
        const al = this.get('al');
        if (n === 0x20) throw new Halt('fin (INT 20h)', 0, true);
        if (n === 0x21) return this.dos(ah, al);
        if (n === 0x10) return this.video(ah, al);
        if (n === 0x16 && ah === 0x00) return this.set('ax', this.key());
        if (n === 0x1a && ah === 0x00) {
            this.set('cx', 0x0012);
            this.set('dx', 0x3456);
            return;
        }
        throw new Halt(`interrupcion no soportada: INT ${hex(n, 2)}h AH=${hex(ah, 2)}h`, 2);
    }

    dos(ah, al) {
        const dl = this.get('dl');
        switch (ah) {
            case 0x01: {
                const c = this.key();
                if (c !== 0x0d) this.screen.put(c);
                return this.set('al', c);
            }
            case 0x07:
            case 0x08:
                return this.set('al', this.key());
            case 0x02:
                this.screen.put(dl);
                return this.set('al', dl);
            case 0x06:
                if (dl === 0xff) return this.set('al', this.key());
                return this.screen.put(dl);
            case 0x09: {
                const ds = this.sregs.ds;
                const dx = this.get('dx');
                for (let i = 0; i < 4096; i++) {
                    const c = this.read8(ds, dx + i);
                    if (c === 0x24) return this.set('al', 0x24);
                    this.screen.put(c);
                }
                throw new Halt("INT 21h/09h: la cadena no termina en '$'", 3);
            }
            case 0x0a:
                return this.readLine();
            case 0x2c:
                this.set('cx', (12 << 8) | 34);
                this.set('dx', (56 << 8) | 78);
                return;
            case 0x4c:
                throw new Halt('fin', al, true);
            default:
                throw new Halt(`funcion de DOS no soportada: INT 21h AH=${hex(ah, 2)}h`, 2);
        }
    }

    readLine() {
        const ds = this.sregs.ds;
        const dx = this.get('dx');
        const max = this.read8(ds, dx);
        // ¿Hay una línea entera en la entrada? Si no, y es interactivo, se espera a que la tipee.
        let end = this.inPos;
        while (end < this.input.length && this.input[end] !== 0x0a) end++;
        if (end >= this.input.length) {
            if (this.interactive) return this.noInput('', 'line');
            if (end === this.inPos) throw new Halt('se termino la entrada (el programa pidio otra linea)', 0);
        }
        const read = [];
        while (this.inPos < this.input.length) {
            const c = this.input[this.inPos++];
            if (c === 0x0d) continue;
            if (c === 0x0a) break;
            if (read.length < max - 1) {
                read.push(c);
                this.screen.put(c);
            }
        }
        this.write8(ds, dx + 1, read.length);
        read.forEach((c, i) => this.write8(ds, dx + 2 + i, c));
        this.write8(ds, dx + 2 + read.length, 0x0d);
    }

    video(ah, al) {
        const s = this.screen;
        const dx = this.get('dx');
        switch (ah) {
            case 0x00:
                return s.wipe();
            case 0x06:
            case 0x07:
                if (al === 0) s.wipe();
                return;
            case 0x02:
                return s.move(dx >> 8, dx & 0xff);
            case 0x03:
                this.set('dx', (s.row << 8) | s.col);
                this.set('cx', 0x0607);
                return;
            case 0x09: {
                const { row, col } = s;
                const color = this.get('bl');
                for (let i = 0; i < this.get('cx'); i++) s.put(al, color);
                return s.move(row, col);
            }
            case 0x0e:
                return s.put(al);
            default:
                throw new Halt(`funcion de video no soportada: INT 10h AH=${hex(ah, 2)}h`, 2);
        }
    }
}

const WAIT = Symbol('wait');

export function hex(v, width) {
    return (v >>> 0).toString(16).toUpperCase().padStart(width, '0');
}

export { JUMP_CONDITIONS };
