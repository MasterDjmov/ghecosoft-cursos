// El tablero del Gólem (D110): una ejecución que se puede mirar por dentro. Corre por tandas (sin trabar la
// página), avanza de a una orden, espera las teclas que pide el programa y arma lo que dibuja el tablero.
// Todo es del navegador del alumno.

import { assemble, describeError, stateReport, LIMIT } from './index.js';
import { Machine, FLAG_BITS, hex } from './machine.js';

export const REGISTER_ORDER = ['ax', 'bx', 'cx', 'dx', 'si', 'di', 'bp', 'sp', 'cs', 'ds', 'ss', 'es', 'ip'];
export const FLAG_ORDER = ['zf', 'sf', 'cf', 'of', 'pf', 'af', 'df', 'if', 'tf'];
const CGA = ['#000000', '#1d4ed8', '#16a34a', '#0891b2', '#b91c1c', '#9333ea', '#a16207', '#cbd5e1',
    '#64748b', '#60a5fa', '#4ade80', '#22d3ee', '#f87171', '#e879f9', '#fde047', '#ffffff'];

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
        this.lastChanges = { regs: new Set(), flags: new Set(), mem: new Set() };
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

    /** Una orden. Devuelve 'ok', 'halt' o 'input'. */
    step() {
        const r = this.machine.step(true);
        this.lastChanges = this.machine.changes ?? this.lastChanges;
        return r;
    }

    /**
     * Corre hasta terminar, pedir una tecla, que lo paren o pasarse del límite (el bucle infinito).
     * @param onTick se llama entre tandas, para redibujar
     */
    async runToEnd(onTick = () => {}) {
        this.stopped = false;
        let done = 0;
        for (;;) {
            const r = this.machine.run(20_000);
            done += 20_000;
            if (r !== 'ok') return r;
            if (this.stopped) return 'stopped';
            if (done >= LIMIT) return 'loop';
            onTick();
            await new Promise((resolve) => setTimeout(resolve, 0));
        }
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
        const ch = atFin ? { regs: new Set(), flags: new Set(), mem: new Set() } : this.lastChanges;
        const registers = REGISTER_ORDER.map((r) => ({
            name: r.toUpperCase(),
            value: hex(m.get(r), 4),
            high: r.length === 2 && 'abcd'.includes(r[0]) && r[1] === 'x' ? hex(m.get(`${r[0]}h`), 2) : null,
            low: r.length === 2 && 'abcd'.includes(r[0]) && r[1] === 'x' ? hex(m.get(`${r[0]}l`), 2) : null,
            changed: ch.regs.has(r),
        }));
        const flags = FLAG_ORDER.map((f) => ({ name: f.toUpperCase(), value: m.flag(f), changed: ch.flags.has(f) }));
        return {
            registers,
            flags,
            memory: this.memory(m, ch),
            stack: this.stack(m),
            screenHtml: this.screenHtml(),
            line: this.currentLine(),
            steps: this.machine.steps,
            atFin,
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
                cells.push({ value: hex(v, 2), char: v >= 32 && v < 127 ? String.fromCharCode(v) : '·', changed: ch.mem.has(phys), name: this.variables.get(off) ?? null });
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
