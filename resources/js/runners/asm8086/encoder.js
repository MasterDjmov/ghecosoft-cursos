// El código máquina de cada orden (D110): los bytes que un 8086 de verdad leería, como los arma MASM.
// El emulador no ejecuta estos bytes (interpreta la orden ya entendida): sirven para mostrarle al alumno
// que `mov ax, 1234h` es B8 34 12. El largo coincide siempre con instructionSize() del ensamblador.

const R16 = { ax: 0, cx: 1, dx: 2, bx: 3, sp: 4, bp: 5, si: 6, di: 7 };
const R8 = { al: 0, cl: 1, dl: 2, bl: 3, ah: 4, ch: 5, dh: 6, bh: 7 };
const SREG = { es: 0, cs: 1, ss: 2, ds: 3 };
const ALU = { add: 0, or: 1, adc: 2, sbb: 3, and: 4, sub: 5, xor: 6, cmp: 7 };
const GROUP3 = { not: 2, neg: 3, mul: 4, imul: 5, div: 6, idiv: 7 };
const SHIFT = { rol: 0, ror: 1, rcl: 2, rcr: 3, shl: 4, shr: 5, sar: 7 };
const CC = { o: 0, no: 1, c: 2, nc: 3, z: 4, nz: 5, be: 6, a: 7, s: 8, ns: 9, p: 10, np: 11, l: 12, ge: 13, le: 14, g: 15 };
const LOOP = { loopne: 0xe0, loopnz: 0xe0, loope: 0xe1, loopz: 0xe1, loop: 0xe2, jcxz: 0xe3 };
const SINGLE = {
    clc: 0xf8, stc: 0xf9, cmc: 0xf5, cld: 0xfc, std: 0xfd, cli: 0xfa, sti: 0xfb, nop: 0x90, cbw: 0x98, cwd: 0x99,
    lahf: 0x9f, sahf: 0x9e, pushf: 0x9c, popf: 0x9d, hlt: 0xf4, xlat: 0xd7, movsb: 0xa4, movsw: 0xa5, lodsb: 0xac,
    lodsw: 0xad, stosb: 0xaa, stosw: 0xab, cmpsb: 0xa6, cmpsw: 0xa7, scasb: 0xae, scasw: 0xaf, into: 0xce, iret: 0xcf,
};
// Las 8 combinaciones de registros entre corchetes que entiende el 8086 (el campo r/m).
const RM = { 'bx+si': 0, 'bx+di': 1, 'bp+si': 2, 'bp+di': 3, si: 4, di: 5, bp: 6, bx: 7 };

const regCode = (op) => (op.k === 'sreg' ? SREG[op.r] : op.size === 16 ? R16[op.r] : R8[op.r]);
const word = (v) => [v & 0xff, (v >> 8) & 0xff];
const isAcc = (op) => op.k === 'reg' && (op.r === 'al' || op.r === 'ax');
const isDirect = (op) => op.k === 'mem' && !op.base && !op.index;

/** El byte ModR/M (con el desplazamiento que haga falta) para un operando registro o memoria. */
function modrm(reg, op) {
    if (op.k === 'reg' || op.k === 'sreg') return [0xc0 | (reg << 3) | regCode(op)];
    if (isDirect(op)) return [(reg << 3) | 6, ...word(op.disp)];
    const rm = RM[[op.base, op.index].filter(Boolean).join('+')];
    const d = op.disp;
    if (d === 0 && rm !== 6) return [(reg << 3) | rm];
    if (d >= -128 && d <= 127) return [0x40 | (reg << 3) | rm, d & 0xff];
    return [0x80 | (reg << 3) | rm, ...word(d)];
}

/**
 * Los bytes de una orden ya ensamblada.
 * @param ins una de program.instructions
 * @param dataSeg el segmento de datos (lo que vale @data cuando DOS carga el programa)
 */
export function encode(ins, { dataSeg = 0 } = {}) {
    const [a, b] = ins.ops;
    const m = ins.m;
    const w = (ins.size || a?.size || b?.size) === 16 ? 1 : 0;
    const imm = (op) => (op.sym?.kind === 'segment' ? dataSeg : op.v);
    const pre = [];
    if (ins.prefix) pre.push(ins.prefix === 'repne' ? 0xf2 : 0xf3);
    for (const op of ins.ops) if (op.k === 'mem' && op.seg) pre.push(0x26 | (SREG[op.seg] << 3));
    const rel = (target, size) => target - (ins.address + ins.length);

    let out;
    if (SINGLE[m] !== undefined) out = [SINGLE[m]];
    else if (m === 'int') out = a.v === 3 ? [0xcc] : [0xcd, a.v & 0xff];
    else if (m === 'ret') out = a ? [0xc2, ...word(a.v)] : [0xc3];
    else if (m === 'call') out = a.k === 'imm' ? [0xe8, ...word(rel(a.v))] : [0xff, ...modrm(2, a)];
    else if (m === 'jmp') {
        if (a.k !== 'imm') out = [0xff, ...modrm(4, a)];
        else out = ins.short ? [0xeb, rel(a.v) & 0xff] : [0xe9, ...word(rel(a.v))];
    } else if (ins.cond) out = [0x70 | CC[ins.cond], rel(a.v) & 0xff];
    else if (LOOP[m]) out = [LOOP[m], rel(a.v) & 0xff];
    else if (m === 'push' || m === 'pop') {
        const push = m === 'push';
        if (a.k === 'reg') out = [(push ? 0x50 : 0x58) | R16[a.r]];
        else if (a.k === 'sreg') out = [(push ? 0x06 : 0x07) | (SREG[a.r] << 3)];
        else out = push ? [0xff, ...modrm(6, a)] : [0x8f, ...modrm(0, a)];
    } else if (m === 'inc' || m === 'dec') {
        const r = m === 'inc' ? 0 : 1;
        out = a.k === 'reg' && a.size === 16 ? [(m === 'inc' ? 0x40 : 0x48) | R16[a.r]] : [0xfe | w, ...modrm(r, a)];
    } else if (GROUP3[m] !== undefined) out = [0xf6 | w, ...modrm(GROUP3[m], a)];
    else if (SHIFT[m] !== undefined) out = [(b.k === 'imm' ? 0xd0 : 0xd2) | w, ...modrm(SHIFT[m], a)];
    else if (m === 'lea') out = [0x8d, ...modrm(R16[a.r], b)];
    else if (m === 'xchg') {
        const other = a.k === 'reg' && a.r === 'ax' ? b : a.r === 'ax' ? null : b.k === 'reg' && b.r === 'ax' ? a : null;
        if (other && other.k === 'reg' && other.size === 16) out = [0x90 | R16[other.r]];
        else if (a.k === 'reg') out = [0x86 | w, ...modrm(regCode(a), b)];
        else out = [0x86 | w, ...modrm(regCode(b), a)];
    } else if (m === 'mov') {
        if (a.k === 'sreg') out = [0x8e, ...modrm(SREG[a.r], b)];
        else if (b.k === 'sreg') out = [0x8c, ...modrm(SREG[b.r], a)];
        else if (a.k === 'reg' && b.k === 'imm') out = w ? [0xb8 | R16[a.r], ...word(imm(b))] : [0xb0 | R8[a.r], imm(b) & 0xff];
        else if (a.k === 'mem' && b.k === 'imm') out = [0xc6 | w, ...modrm(0, a), ...(w ? word(imm(b)) : [imm(b) & 0xff])];
        else if (isAcc(a) && isDirect(b)) out = [0xa0 | w, ...word(b.disp)];
        else if (isAcc(b) && isDirect(a)) out = [0xa2 | w, ...word(a.disp)];
        else if (a.k === 'reg') out = [0x8a | w, ...modrm(regCode(a), b)];
        else out = [0x88 | w, ...modrm(regCode(b), a)];
    } else if (m === 'test') {
        if (b.k === 'imm') out = isAcc(a) ? [0xa8 | w, ...(w ? word(imm(b)) : [imm(b) & 0xff])] : [0xf6 | w, ...modrm(0, a), ...(w ? word(imm(b)) : [imm(b) & 0xff])];
        else if (a.k === 'reg' && b.k === 'reg') out = [0x84 | w, ...modrm(regCode(b), a)];
        else out = [0x84 | w, ...modrm(regCode(a.k === 'reg' ? a : b), a.k === 'mem' ? a : b)];
    } else if (ALU[m] !== undefined) {
        const op = ALU[m];
        if (b.k === 'imm') {
            const v = imm(b);
            if (isAcc(a)) out = [(op << 3) | 0x04 | w, ...(w ? word(v) : [v & 0xff])];
            else if (!w) out = [0x80, ...modrm(op, a), v & 0xff];
            else if (v >= -128 && v <= 127) out = [0x83, ...modrm(op, a), v & 0xff];
            else out = [0x81, ...modrm(op, a), ...word(v)];
        } else if (a.k === 'reg') out = [(op << 3) | 0x02 | w, ...modrm(regCode(a), b)];
        else out = [(op << 3) | w, ...modrm(regCode(b), a)];
    } else {
        return null;
    }
    return [...pre, ...out];
}

/** Los bytes en hexa, separados por espacios («B8 34 12»). */
export function hexBytes(bytes) {
    return bytes.map((x) => x.toString(16).toUpperCase().padStart(2, '0')).join(' ');
}
