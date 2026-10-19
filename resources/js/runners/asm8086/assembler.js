// Ensamblador 8086 de la plataforma (D110): el subconjunto de MASM que usa la cursada (.model small, .stack,
// .data, .code, db/dw/dup/?, equ, offset, byte ptr/word ptr, proc/endp, macro/endm/local, end main).
// No genera código máquina: arma una lista de instrucciones ya analizadas, cada una con la dirección y el
// tamaño que tendría en un 8086 de verdad (así IP, CALL/RET y la pila se ven como en emu8086), y la imagen
// de los datos byte por byte. Los errores imitan los de JWasm/MASM (los que muestra el bestiario del curso).

export const REG16 = ['ax', 'cx', 'dx', 'bx', 'sp', 'bp', 'si', 'di'];
export const REG8 = ['al', 'cl', 'dl', 'bl', 'ah', 'ch', 'dh', 'bh'];
export const SREG = ['es', 'cs', 'ss', 'ds'];
const REG32 = ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'esp', 'ebp'];

const JCC = {
    je: 'z', jz: 'z', jne: 'nz', jnz: 'nz', jc: 'c', jb: 'c', jnae: 'c', jnc: 'nc', jae: 'nc', jnb: 'nc',
    ja: 'a', jnbe: 'a', jbe: 'be', jna: 'be', jg: 'g', jnle: 'g', jge: 'ge', jnl: 'ge', jl: 'l', jnge: 'l',
    jle: 'le', jng: 'le', js: 's', jns: 'ns', jo: 'o', jno: 'no', jp: 'p', jpe: 'p', jnp: 'np', jpo: 'np',
};
const LOOPS = ['loop', 'loope', 'loopz', 'loopne', 'loopnz', 'jcxz'];
const NOARGS = ['clc', 'stc', 'cmc', 'cld', 'std', 'cli', 'sti', 'nop', 'cbw', 'cwd', 'lahf', 'sahf', 'pushf',
    'popf', 'hlt', 'xlat', 'xlatb', 'movsb', 'movsw', 'lodsb', 'lodsw', 'stosb', 'stosw', 'cmpsb', 'cmpsw',
    'scasb', 'scasw', 'into', 'iret'];
const TWO = ['mov', 'add', 'adc', 'sub', 'sbb', 'cmp', 'and', 'or', 'xor', 'test', 'xchg', 'lea'];
const ONE = ['inc', 'dec', 'neg', 'not', 'mul', 'imul', 'div', 'idiv', 'push', 'pop'];
const SHIFTS = ['shl', 'sal', 'shr', 'sar', 'rol', 'ror', 'rcl', 'rcr'];
const BRANCH = ['jmp', 'call'];
const OTHER = ['ret', 'retn', 'int'];
const PREFIXES = ['rep', 'repe', 'repz', 'repne', 'repnz'];
const PRE186 = ['pusha', 'popa', 'enter', 'leave', 'bound', 'ins', 'outs', 'insb', 'outsb', 'movzx', 'movsx'];
export const MNEMONICS = new Set([...Object.keys(JCC), ...LOOPS, ...NOARGS, ...TWO, ...ONE, ...SHIFTS, ...BRANCH, ...OTHER]);

// Palabras reservadas de MASM que no pueden ser nombres (el bestiario: «Syntax error: record»).
const RESERVED = new Set(['record', 'name', 'length', 'size', 'type', 'mask', 'width', 'offset', 'ptr', 'byte',
    'word', 'dup', 'proc', 'endp', 'macro', 'endm', 'end', 'equ', 'db', 'dw', 'dd', 'seg', 'short', 'near', 'far',
    'this', 'high', 'low', 'local', 'title', 'page', 'segment', 'ends', 'assume', 'org', 'label', 'struc', 'public',
    'extrn', 'include', 'mod', 'shl', 'shr', 'and', 'or', 'xor', 'not', 'eq', 'ne', 'lt', 'gt', 'le', 'ge',
    ...REG16, ...REG8, ...SREG, ...MNEMONICS, ...PREFIXES]);

export class AsmError extends Error {
    constructor(line, code, message, detail = '') {
        super(`${code}: ${message}${detail}`);
        this.line = line;
        this.code = code;
        this.raw = `main.asm(${line}) : Error ${code}: ${message}${detail}`;
    }
}

const err = {
    syntax: (l, w) => new AsmError(l, 'A2209', 'Syntax error: ', w),
    undefined: (l, s) => new AsmError(l, 'A2102', 'Symbol not defined : ', s),
    already: (l, s) => new AsmError(l, 'A2056', 'Symbol already defined: ', s),
    size: (l, a, b) => new AsmError(l, 'A2048', 'Operands must be the same size: ', `${a} - ${b}`),
    operands: (l) => new AsmError(l, 'A2049', 'Invalid instruction operands'),
    mustSize: (l) => new AsmError(l, 'A2182', 'Instruction operand must have size'),
    indexReg: (l) => new AsmError(l, 'A2033', 'Must be index or base register'),
    cpu: (l) => new AsmError(l, 'A2030', 'Instruction or register not accepted in current CPU mode'),
    nesting: (l, s) => new AsmError(l, 'A2142', 'Unmatched block nesting: ', s),
    noEnd: (l) => new AsmError(l, 'A2099', 'END directive required at end of file'),
    operator: (l) => new AsmError(l, 'A2150', 'Missing operator in expression'),
    range: (l, n) => new AsmError(l, 'A2053', 'Jump out of range by ', `${n} byte(s)`),
};

// ---------------------------------------------------------------- texto

/** Saca el comentario (lo que sigue a ';' fuera de comillas). */
function stripComment(line) {
    let quote = null;
    for (let i = 0; i < line.length; i++) {
        const c = line[i];
        if (quote) {
            if (c === quote) quote = null;
        } else if (c === "'" || c === '"') {
            quote = c;
        } else if (c === ';') {
            return line.slice(0, i);
        }
    }
    return line;
}

/** Separa por comas que no están dentro de comillas, corchetes ni paréntesis. */
export function splitTop(text) {
    const parts = [];
    let depth = 0;
    let quote = null;
    let start = 0;
    for (let i = 0; i < text.length; i++) {
        const c = text[i];
        if (quote) {
            if (c === quote) quote = null;
        } else if (c === "'" || c === '"') {
            quote = c;
        } else if (c === '[' || c === '(' || c === '<') {
            depth++;
        } else if (c === ']' || c === ')' || c === '>') {
            depth--;
        } else if (c === ',' && depth === 0) {
            parts.push(text.slice(start, i).trim());
            start = i + 1;
        }
    }
    const last = text.slice(start).trim();
    if (last !== '' || parts.length) parts.push(last);
    return parts;
}

export function parseNumber(word) {
    const w = word.toLowerCase();
    if (/^[0-9][0-9a-f]*h$/.test(w)) return parseInt(w.slice(0, -1), 16);
    if (/^[01]+b$/.test(w)) return parseInt(w.slice(0, -1), 2);
    if (/^[0-7]+[oq]$/.test(w)) return parseInt(w.slice(0, -1), 8);
    if (/^[0-9]+d?$/.test(w)) return parseInt(w, 10);
    return null;
}

function tokenize(text, line) {
    const tokens = [];
    let i = 0;
    while (i < text.length) {
        const c = text[i];
        if (/\s/.test(c)) {
            i++;
        } else if (c === "'" || c === '"') {
            // En MASM, la comilla doblada dentro del texto es una comilla: 'it''s'.
            let end = i + 1;
            let v = '';
            for (;;) {
                const next = text.indexOf(c, end);
                if (next < 0) throw err.syntax(line, text.slice(i));
                v += text.slice(end, next);
                if (text[next + 1] === c) {
                    v += c;
                    end = next + 2;
                } else {
                    end = next + 1;
                    break;
                }
            }
            tokens.push({ t: 'str', v });
            i = end;
        } else if (/[0-9]/.test(c)) {
            const m = /^[0-9][0-9a-zA-Z]*/.exec(text.slice(i))[0];
            const value = parseNumber(m);
            if (value === null) throw err.syntax(line, m);
            tokens.push({ t: 'num', v: value });
            i += m.length;
        } else if (/[A-Za-z_@?$.]/.test(c)) {
            const m = /^[A-Za-z_@?$.][A-Za-z0-9_@?$]*/.exec(text.slice(i))[0];
            tokens.push({ t: 'id', v: m });
            i += m.length;
        } else if ('[]()+-*/:'.includes(c)) {
            tokens.push({ t: 'p', v: c });
            i++;
        } else {
            throw err.syntax(line, c);
        }
    }
    return tokens;
}

// ---------------------------------------------------------------- expresiones

/**
 * Evalúa una expresión de operando como combinación lineal: constante + registros (dentro de corchetes) +
 * a lo sumo un símbolo de datos (su dirección) o una etiqueta. `mapa[bx][si]`, `[bx + si + 2 * 4]`,
 * `msg + 1`, `offset nombre`, `0 * 16 + 14`, `'0'`.
 */
class Expr {
    constructor(tokens, ctx, line) {
        this.tk = tokens;
        this.pos = 0;
        this.ctx = ctx;
        this.line = line;
        this.brackets = false;
        this.offset = false;
        this.ptr = 0;
        this.seg = null;
    }

    peek(v) {
        const t = this.tk[this.pos];
        return t && (v === undefined || (t.t !== 'str' && String(t.v).toLowerCase() === v)) ? t : null;
    }

    parse() {
        // Prefijos: byte ptr / word ptr, offset, short, segmento con ':'.
        for (;;) {
            const a = this.peek();
            const b = this.tk[this.pos + 1];
            if (!a || a.t !== 'id') break;
            const w = a.v.toLowerCase();
            if ((w === 'byte' || w === 'word') && b && b.t === 'id' && b.v.toLowerCase() === 'ptr') {
                this.ptr = w === 'byte' ? 8 : 16;
                this.pos += 2;
            } else if (w === 'offset') {
                this.offset = true;
                this.pos++;
            } else if (w === 'short' || w === 'near') {
                this.pos++;
            } else if (SREG.includes(w) && b && b.t === 'p' && b.v === ':') {
                this.seg = w;
                this.pos += 2;
            } else {
                break;
            }
        }
        const value = this.sum();
        if (this.pos < this.tk.length) throw err.operator(this.line);
        return value;
    }

    sum() {
        let acc = this.product();
        for (;;) {
            if (this.peek('+')) {
                this.pos++;
                acc = add(acc, this.product(), 1, this.line);
            } else if (this.peek('-')) {
                this.pos++;
                acc = add(acc, this.product(), -1, this.line);
            } else if (this.peek('[')) {
                // `mapa[2][3]` = mapa + 2 + 3
                acc = add(acc, this.product(), 1, this.line);
            } else {
                return acc;
            }
        }
    }

    product() {
        let acc = this.unary();
        for (;;) {
            if (this.peek('*') || this.peek('/')) {
                const op = this.tk[this.pos++].v;
                const rhs = this.unary();
                if (acc.regs.length || rhs.regs.length || acc.sym || rhs.sym) throw err.operator(this.line);
                acc = { c: op === '*' ? acc.c * rhs.c : Math.trunc(acc.c / rhs.c), regs: [], sym: null };
            } else {
                return acc;
            }
        }
    }

    unary() {
        if (this.peek('-')) {
            this.pos++;
            const v = this.unary();
            if (v.regs.length || v.sym) throw err.operator(this.line);
            return { c: -v.c, regs: [], sym: null };
        }
        if (this.peek('+')) {
            this.pos++;
            return this.unary();
        }
        return this.atom();
    }

    atom() {
        const t = this.tk[this.pos++];
        if (!t) throw err.operator(this.line);
        if (t.t === 'num') return { c: t.v, regs: [], sym: null };
        if (t.t === 'str') {
            if (t.v.length === 1) return { c: t.v.charCodeAt(0), regs: [], sym: null };
            if (t.v.length === 2) return { c: (t.v.charCodeAt(0) << 8) | t.v.charCodeAt(1), regs: [], sym: null };
            throw err.operands(this.line);
        }
        if (t.t === 'p' && (t.v === '(' || t.v === '[')) {
            if (t.v === '[') this.brackets = true;
            const inner = this.sum();
            const close = this.tk[this.pos++];
            if (!close || close.v !== (t.v === '(' ? ')' : ']')) throw err.syntax(this.line, t.v);
            return inner;
        }
        if (t.t === 'id') {
            const w = t.v.toLowerCase();
            if (REG16.includes(w) || REG8.includes(w) || SREG.includes(w)) return { c: 0, regs: [w], sym: null };
            if (REG32.includes(w)) throw err.cpu(this.line);
            if (w === '@data') return { c: 0, regs: [], sym: { kind: 'segment', name: '@data' } };
            const sym = this.ctx.lookup(w, this.line, t.v);
            if (sym.kind === 'equ') return { c: sym.value, regs: [], sym: null };
            return { c: sym.kind === 'label' && sym.address === undefined ? 0 : (sym.offset ?? sym.address ?? 0), regs: [], sym };
        }
        throw err.syntax(this.line, t.v);
    }
}

function add(a, b, sign, line) {
    if (sign < 0 && (b.regs.length || b.sym)) throw err.operator(line);
    if (a.sym && b.sym) throw err.operator(line);
    return { c: a.c + sign * b.c, regs: [...a.regs, ...b.regs], sym: a.sym ?? b.sym };
}

// ---------------------------------------------------------------- operandos

/** Analiza un operando: registro, inmediato o memoria. `ctx` resuelve símbolos (o los adivina en la 1.ª pasada). */
function parseOperand(text, ctx, line) {
    const tokens = tokenize(text, line);
    if (!tokens.length) throw err.operands(line);
    const ex = new Expr(tokens, ctx, line);
    const v = ex.parse();

    // Un registro solo.
    if (v.regs.length === 1 && !ex.brackets && !v.sym && v.c === 0 && tokens.length === 1) {
        const r = v.regs[0];
        if (SREG.includes(r)) return { k: 'sreg', r, size: 16 };
        return { k: 'reg', r, size: REG16.includes(r) ? 16 : 8 };
    }
    if (v.regs.length && !ex.brackets) throw err.operands(line);

    const dataSym = v.sym && v.sym.kind === 'data';
    if (ex.offset || (!ex.brackets && !dataSym)) {
        // Inmediato: número, constante, offset de una variable o dirección de una etiqueta.
        if (v.regs.length) throw err.operands(line);
        return { k: 'imm', v: v.c, sym: v.sym, size: 0, label: v.sym && (v.sym.kind === 'label' || v.sym.kind === 'proc') ? v.sym : null };
    }

    // Memoria.
    let base = null;
    let index = null;
    for (const r of v.regs) {
        if (r === 'bx' || r === 'bp') {
            if (base) throw err.indexReg(line);
            base = r;
        } else if (r === 'si' || r === 'di') {
            if (index) throw err.indexReg(line);
            index = r;
        } else {
            throw err.indexReg(line);
        }
    }
    const size = ex.ptr || (dataSym ? v.sym.size : 0);
    return { k: 'mem', base, index, disp: v.c, seg: ex.seg, size, sym: v.sym };
}

// ---------------------------------------------------------------- tamaños (como un 8086 de verdad)

function modrmBytes(op) {
    if (op.k !== 'mem') return 0;
    if (!op.base && !op.index) return 2;
    const d = op.disp;
    if (d === 0 && !(op.base === 'bp' && !op.index)) return 0;
    return d >= -128 && d <= 127 ? 1 : 2;
}

function immBytes(size, value, signExt) {
    if (size === 8) return 1;
    return signExt && value >= -128 && value <= 127 ? 1 : 2;
}

function instructionSize(ins) {
    const [a, b] = ins.ops;
    const pre = (ins.prefix ? 1 : 0) + ins.ops.filter((o) => o.k === 'mem' && o.seg).length;
    const m = ins.m;
    let n;
    if (NOARGS.includes(m)) n = 1;
    else if (m === 'int') n = a.v === 3 ? 1 : 2;
    else if (m === 'ret' || m === 'retn') n = a ? 3 : 1;
    else if (m === 'call') n = a.k === 'imm' ? 3 : 2 + modrmBytes(a);
    else if (m === 'jmp') n = a.k === 'imm' ? (ins.short ? 2 : 3) : 2 + modrmBytes(a);
    else if (JCC[m] || LOOPS.includes(m)) n = 2;
    else if (m === 'push' || m === 'pop') n = a.k === 'mem' ? 2 + modrmBytes(a) : 1;
    else if (m === 'inc' || m === 'dec') n = a.k === 'reg' && a.size === 16 ? 1 : 2 + modrmBytes(a);
    else if (['neg', 'not', 'mul', 'imul', 'div', 'idiv'].includes(m)) n = 2 + modrmBytes(a);
    else if (SHIFTS.includes(m)) n = 2 + modrmBytes(a);
    else if (m === 'lea') n = 2 + modrmBytes(b);
    else if (m === 'xchg') n = a.k === 'reg' && b.k === 'reg' && a.size === 16 && (a.r === 'ax' || b.r === 'ax') ? 1 : 2 + modrmBytes(a.k === 'mem' ? a : b);
    else if (m === 'mov') {
        if (a.k === 'reg' && b.k === 'imm') n = 1 + (a.size === 8 ? 1 : 2);
        else if (a.k === 'mem' && b.k === 'imm') n = 2 + modrmBytes(a) + (ins.size === 8 ? 1 : 2);
        else if ((a.k === 'reg' && (a.r === 'al' || a.r === 'ax') && b.k === 'mem' && !b.base && !b.index)
            || (b.k === 'reg' && (b.r === 'al' || b.r === 'ax') && a.k === 'mem' && !a.base && !a.index)) n = 3;
        else n = 2 + modrmBytes(a.k === 'mem' ? a : b);
    } else {
        // add adc sub sbb cmp and or xor test
        if (b.k === 'imm') {
            const acc = a.k === 'reg' && (a.r === 'al' || a.r === 'ax');
            if (acc) n = 1 + (a.size === 8 ? 1 : 2);
            else n = 2 + modrmBytes(a) + immBytes(ins.size, b.v, m !== 'test');
        } else {
            n = 2 + modrmBytes(a.k === 'mem' ? a : b);
        }
    }
    return n + pre;
}

// ---------------------------------------------------------------- validación de operandos

function sizeOf(op) {
    if (op.k === 'reg' || op.k === 'sreg') return op.size;
    if (op.k === 'mem') return op.size;
    return 0;
}

function checkOperands(ins, line) {
    const { m, ops } = ins;
    const [a, b] = ops;
    const need = (n) => {
        if (ops.length !== n) throw err.operands(line);
    };
    if (NOARGS.includes(m)) return need(0);
    if (m === 'int') {
        need(1);
        if (a.k !== 'imm') throw err.operands(line);
        return;
    }
    if (m === 'ret' || m === 'retn') {
        if (ops.length > 1 || (a && a.k !== 'imm')) throw err.operands(line);
        return;
    }
    if (JCC[m] || LOOPS.includes(m) || m === 'jmp' || m === 'call') {
        need(1);
        if ((JCC[m] || LOOPS.includes(m)) && (a.k !== 'imm' || !a.label)) throw err.operands(line);
        if (a.k === 'reg' && a.size !== 16) throw err.operands(line);
        return;
    }
    if (m === 'push' || m === 'pop') {
        need(1);
        if (a.k === 'imm') throw err.cpu(line);
        if (a.k === 'reg' && a.size !== 16) throw err.operands(line);
        if (a.k === 'mem' && a.size === 8) throw err.operands(line);
        if (m === 'pop' && a.k === 'sreg' && a.r === 'cs') throw err.operands(line);
        ins.size = 16;
        return;
    }
    if (ONE.includes(m)) {
        need(1);
        if (a.k === 'imm' || a.k === 'sreg') throw err.operands(line);
        if (a.k === 'mem' && !a.size) throw err.mustSize(line);
        ins.size = sizeOf(a);
        return;
    }
    if (SHIFTS.includes(m)) {
        need(2);
        if (a.k === 'imm' || a.k === 'sreg') throw err.operands(line);
        if (a.k === 'mem' && !a.size) throw err.mustSize(line);
        if (b.k === 'imm') {
            if (b.v !== 1) throw err.cpu(line);
        } else if (!(b.k === 'reg' && b.r === 'cl')) {
            throw err.operands(line);
        }
        ins.size = sizeOf(a);
        return;
    }
    // Dos operandos.
    need(2);
    if (m === 'lea') {
        if (a.k !== 'reg' || a.size !== 16 || b.k !== 'mem') throw err.operands(line);
        ins.size = 16;
        return;
    }
    if (a.k === 'imm') throw err.operands(line);
    if (a.k === 'mem' && b.k === 'mem') {
        if (a.size && b.size && a.size !== b.size) throw err.size(line, a.size / 8, b.size / 8);
        throw err.operands(line);
    }
    if (a.k === 'sreg' || b.k === 'sreg') {
        if (m !== 'mov') throw err.operands(line);
        if (a.k === 'sreg' && (b.k === 'imm' || b.k === 'sreg' || a.r === 'cs')) throw err.operands(line);
        const other = a.k === 'sreg' ? b : a;
        if (other.k === 'reg' && other.size !== 16) throw err.size(line, sizeOf(a) / 8, sizeOf(b) / 8);
        ins.size = 16;
        return;
    }
    if (m === 'xchg' && b.k === 'imm') throw err.operands(line);
    const sa = sizeOf(a);
    const sb = sizeOf(b);
    if (sa && sb && sa !== sb) throw err.size(line, sa / 8, sb / 8);
    const size = sa || sb;
    if (!size) throw err.mustSize(line);
    if (b.k === 'imm' && !b.label && !b.sym) {
        const max = size === 8 ? 0xff : 0xffff;
        const min = size === 8 ? -0x80 : -0x8000;
        if (b.v > max || b.v < min) throw err.operands(line);
    }
    if (b.k === 'imm' && b.sym && b.sym.kind === 'segment' && size !== 16) throw err.operands(line);
    if (b.k === 'imm' && b.sym && b.sym.kind === 'data' && size !== 16) throw err.operands(line);
    ins.size = size;
}

// ---------------------------------------------------------------- macros

function expandMacros(lines) {
    const macros = new Map();
    const out = [];
    // 1) Sacar las definiciones.
    const body = [];
    for (let i = 0; i < lines.length; i++) {
        const { text, line } = lines[i];
        const m = /^\s*([A-Za-z_][A-Za-z0-9_]*)\s+macro\b(.*)$/i.exec(text);
        if (m) {
            const name = m[1].toLowerCase();
            const params = m[2].split(',').map((p) => p.trim().toLowerCase()).filter(Boolean);
            const def = { name, params, lines: [], locals: [], line };
            let j = i + 1;
            for (; j < lines.length; j++) {
                if (/^\s*endm\b/i.test(lines[j].text)) break;
                const loc = /^\s*local\s+(.*)$/i.exec(lines[j].text);
                if (loc) def.locals.push(...loc[1].split(',').map((s) => s.trim().toLowerCase()).filter(Boolean));
                else def.lines.push(lines[j].text);
            }
            if (j === lines.length) throw err.nesting(line, m[1]);
            if (macros.has(name)) throw err.already(line, m[1]);
            macros.set(name, def);
            i = j;
            continue;
        }
        body.push(lines[i]);
    }
    // 2) Expandir los usos (una macro puede usar otras).
    let counter = 0;
    const expand = (entry, depth) => {
        const m = /^\s*(?:([A-Za-z_][A-Za-z0-9_]*):\s*)?([A-Za-z_][A-Za-z0-9_]*)(?:\s+(.*))?$/.exec(entry.text);
        const def = m && macros.get(m[2].toLowerCase());
        if (!def) {
            out.push(entry);
            return;
        }
        if (depth > 20) throw err.nesting(entry.line, def.name);
        if (m[1]) out.push({ text: `${m[1]}:`, line: entry.line });
        const args = m[3] ? splitTop(m[3]).map((a) => a.replace(/^<(.*)>$/, '$1')) : [];
        const map = new Map();
        def.params.forEach((p, i) => map.set(p, args[i] ?? ''));
        def.locals.forEach((l) => map.set(l, `??${(counter++).toString(16).toUpperCase().padStart(4, '0')}`));
        for (const raw of def.lines) {
            const text = raw.replace(/'[^']*'|"[^"]*"|[A-Za-z_?][A-Za-z0-9_?]*/g, (w) =>
                w[0] === "'" || w[0] === '"' ? w : (map.has(w.toLowerCase()) ? map.get(w.toLowerCase()) : w));
            expand({ text: stripComment(text), line: entry.line, macro: def.name }, depth + 1);
        }
    };
    for (const entry of body) expand(entry, 0);
    return out;
}

// ---------------------------------------------------------------- ensamblar

/**
 * @returns {{ instructions, byAddress, data: Uint8Array, symbols, entry, stackSize, codeSize, lines }}
 * @throws {AsmError}
 */
export function assemble(source) {
    const raw = source.replace(/\r\n?/g, '\n').split('\n');
    let lines = raw.map((text, i) => ({ text: stripComment(text), line: i + 1 }));
    lines = expandMacros(lines);

    // Primera vuelta: qué es cada nombre (datos, etiquetas, procedimientos, constantes).
    const symbols = new Map();
    const define = (name, info, line) => {
        const key = name.toLowerCase();
        if (RESERVED.has(key)) throw err.syntax(line, name);
        if (symbols.has(key)) throw err.already(line, name);
        symbols.set(key, { name, line, ...info });
    };

    const statements = [];
    let section = null;
    let stackSize = 0x400;
    let entryName = null;
    let ended = false;
    const procs = [];
    const data = [];

    for (const { text, line } of lines) {
        let rest = text.trim();
        if (!rest || ended) continue;
        // Directivas de segmento.
        const dir = /^(\.[a-z0-9]+)\b\s*(.*)$/i.exec(rest);
        if (dir) {
            const d = dir[1].toLowerCase();
            if (d === '.data') section = 'data';
            else if (d === '.code') section = 'code';
            else if (d === '.stack') stackSize = dir[2].trim() ? evalConst(dir[2], symbols, line) : 0x400;
            else if (d === '.model' || d === '.8086' || d === '.186' || d === '.286' || d === '.startup') { /* nada */ }
            else if (['.386', '.486', '.586', '.686'].includes(d)) throw err.cpu(line);
            else throw err.syntax(line, dir[1]);
            continue;
        }
        if (/^end\b/i.test(rest)) {
            const m = /^end\s+([A-Za-z_][A-Za-z0-9_]*)?\s*$/i.exec(rest);
            entryName = m && m[1] ? m[1] : null;
            ended = true;
            continue;
        }
        // Etiqueta "nombre:" (puede haber instrucción en la misma línea).
        const label = /^([A-Za-z_?][A-Za-z0-9_?]*)\s*:(?!:)\s*(.*)$/.exec(rest);
        if (label && !SREG.includes(label[1].toLowerCase())) {
            define(label[1], { kind: 'label' }, line);
            statements.push({ type: 'label', name: label[1].toLowerCase(), line, section });
            rest = label[2].trim();
            if (!rest) continue;
        }
        const words = rest.split(/\s+/);
        const first = words[0].toLowerCase();
        const second = (words[1] ?? '').toLowerCase();
        // nombre proc / nombre endp
        if (second === 'proc') {
            define(words[0], { kind: 'proc' }, line);
            procs.push({ name: words[0], line });
            statements.push({ type: 'label', name: first, line, section });
            continue;
        }
        if (second === 'endp') {
            const open = procs.pop();
            if (!open || open.name.toLowerCase() !== first) throw err.nesting(line, words[0]);
            continue;
        }
        // nombre equ valor  /  nombre = valor
        const eq = /^([A-Za-z_][A-Za-z0-9_]*)\s+(?:equ\s+|=\s*)(.+)$/i.exec(rest);
        if (eq) {
            define(eq[1], { kind: 'equ', value: evalConst(eq[2], symbols, line) }, line);
            continue;
        }
        // Datos: [nombre] db|dw ...
        let dname = null;
        let dtype = null;
        let ditems = null;
        if (first === 'db' || first === 'dw') {
            dtype = first;
            ditems = rest.slice(words[0].length);
        } else if (second === 'db' || second === 'dw') {
            dname = words[0];
            dtype = second;
            ditems = rest.slice(rest.toLowerCase().indexOf(second, words[0].length) + 2);
        }
        if (dtype) {
            if (dname) define(dname, { kind: 'data', size: dtype === 'db' ? 8 : 16 }, line);
            statements.push({ type: 'data', name: dname?.toLowerCase(), dtype, items: ditems.trim(), line, section });
            continue;
        }
        if (second === 'dd' || first === 'dd') throw err.cpu(line);
        // Instrucción.
        statements.push({ type: 'ins', text: rest, line, section });
    }
    const lastLine = raw.length;
    if (procs.length) throw err.nesting(procs[procs.length - 1].line, procs[procs.length - 1].name);
    if (!ended) throw err.noEnd(lastLine);

    // Datos: cada variable recibe su dirección (offset en el segmento de datos) y se arma la imagen.
    const lookup = (name, line, shown = name) => {
        const s = symbols.get(name);
        if (!s) throw err.undefined(line, shown);
        return s;
    };
    const ctx = { lookup };
    for (const st of statements) {
        if (st.type !== 'data') continue;
        if (st.section === 'code') {
            // Variables dentro de .code: se permiten, pero acá se guardan con los datos (no ejecutamos código máquina).
        }
        const offset = data.length;
        if (st.name) symbols.get(st.name).offset = offset;
        emitData(st, data, ctx);
    }

    // Código: direcciones con los tamaños reales; los saltos hacia adelante se suponen largos (como MASM).
    const instructions = [];
    let address = 0;
    for (const st of statements) {
        if (st.type === 'label') {
            if (st.section !== 'data') symbols.get(st.name).address = address;
            else symbols.get(st.name).offset = data.length;
            continue;
        }
        if (st.type !== 'ins') continue;
        if (st.section !== 'code') throw err.syntax(st.line, st.text.split(/\s+/)[0]);
        const ins = parseInstruction(st.text, ctx, st.line, symbols, address);
        ins.address = address;
        ins.length = instructionSize(ins);
        address += ins.length;
        instructions.push(ins);
    }
    const codeSize = address;

    // Segunda vuelta: ahora todas las etiquetas tienen dirección; se resuelven los saltos y se valida el rango.
    for (const ins of instructions) {
        for (const op of ins.ops) {
            if (op.k === 'imm' && op.label) op.v = op.label.address;
        }
        if (JCC[ins.m] || LOOPS.includes(ins.m)) {
            const target = ins.ops[0].v;
            const rel = target - (ins.address + ins.length);
            if (rel > 127) throw err.range(ins.line, rel - 127);
            if (rel < -128) throw err.range(ins.line, -128 - rel);
        }
    }

    let entry = 0;
    if (entryName) {
        const s = symbols.get(entryName.toLowerCase());
        if (!s || s.address === undefined) throw err.undefined(lastLine, entryName);
        entry = s.address;
    }
    const byAddress = new Map(instructions.map((ins, i) => [ins.address, i]));
    return { instructions, byAddress, data: Uint8Array.from(data), symbols, entry, stackSize, codeSize, lines: raw };
}

function evalConst(text, symbols, line) {
    const ctx = {
        lookup: (name, _line, shown = name) => {
            const s = symbols.get(name);
            if (!s) throw err.undefined(line, shown);
            if (s.kind !== 'equ') throw err.operands(line);
            return s;
        },
    };
    const ex = new Expr(tokenize(text, line), ctx, line);
    const v = ex.parse();
    if (v.regs.length || v.sym) throw err.operands(line);
    return v.c;
}

function emitData(st, out, ctx) {
    const word = st.dtype === 'dw';
    const push = (v) => {
        if (word) out.push(v & 0xff, (v >> 8) & 0xff);
        else out.push(v & 0xff);
    };
    const items = splitTop(st.items);
    if (!items.length || items.some((i) => i === '')) throw err.syntax(st.line, st.items || st.dtype);
    const emitItem = (item) => {
        const dup = /^(.+?)\s+dup\s*\((.*)\)\s*$/i.exec(item);
        if (dup) {
            const n = evalItem(dup[1], ctx, st.line);
            const inner = splitTop(dup[2]);
            for (let i = 0; i < n; i++) inner.forEach(emitItem);
            return;
        }
        if (item === '?') return push(0);
        const str = /^(['"])(.*)\1$/.exec(item);
        if (str && (!word || str[2].length !== 2)) {
            if (word && str[2].length > 2) throw err.operands(st.line);
            for (const ch of str[2].replaceAll(str[1] + str[1], str[1])) push(ch.charCodeAt(0) & 0xff);
            return;
        }
        const v = evalItem(item, ctx, st.line, word);
        if (!word && (v > 255 || v < -128)) throw err.operands(st.line);
        push(v);
    };
    items.forEach(emitItem);
}

function evalItem(text, ctx, line, allowOffset = false) {
    const ex = new Expr(tokenize(text, line), ctx, line);
    const v = ex.parse();
    if (v.regs.length) throw err.operands(line);
    if (v.sym && !(allowOffset && v.sym.kind === 'data')) throw err.operands(line);
    return v.c;
}

function parseInstruction(text, ctx, line, symbols, address) {
    let rest = text;
    let prefix = null;
    let m = rest.split(/\s+/)[0].toLowerCase();
    if (PREFIXES.includes(m)) {
        prefix = m === 'repz' ? 'repe' : m === 'repnz' ? 'repne' : m;
        rest = rest.slice(m.length).trim();
        m = rest.split(/\s+/)[0].toLowerCase();
        if (!['movsb', 'movsw', 'lodsb', 'lodsw', 'stosb', 'stosw', 'cmpsb', 'cmpsw', 'scasb', 'scasw'].includes(m)) {
            throw err.syntax(line, m);
        }
    }
    if (PRE186.includes(m)) throw err.cpu(line);
    if (!MNEMONICS.has(m)) throw err.syntax(line, rest.split(/\s+/)[0]);
    const operandText = rest.slice(m.length).trim();
    // En la primera pasada, las etiquetas de más adelante todavía no tienen dirección.
    const ops = operandText ? splitTop(operandText).map((o) => {
        if (o === '') throw err.operands(line);
        return parseOperand(o, ctx, line);
    }) : [];
    const ins = { m: m === 'retn' ? 'ret' : m === 'sal' ? 'shl' : m === 'xlatb' ? 'xlat' : m, ops, line, prefix, text: text.trim() };
    if (JCC[m]) ins.cond = JCC[m];
    // Un JMP hacia atrás cercano entra en 2 bytes (corto); hacia adelante MASM lo deja de 3.
    if (m === 'jmp' && ops[0]?.k === 'imm' && ops[0].label && ops[0].label.address !== undefined) {
        const rel = ops[0].label.address - (address + 2);
        ins.short = rel >= -128 && rel <= 127;
    }
    if (/^\s*short\b/i.test(operandText)) ins.short = true;
    checkOperands(ins, line);
    return ins;
}

export const JUMP_CONDITIONS = JCC;
