// La pantalla de la calculadora (D120): simple o para programar. La cuenta está en calculator-core.js.
import { BASES, evalProgrammer, evalSimple, groupBinary, toBase } from './calculator-core.js';
import { copyText, instanceStore } from './copy.js';

const WIDTHS = [8, 16, 32, 64];
const MAX_HISTORY = 30;

export function calculatorTool(user) {
    const store = instanceStore(user, 'calculadora');
    // Fuera de lo que mira Alpine: escribirlo mientras se dibuja volvería a dibujar.
    let lastLive = null;

    return {
        mode: 'simple',
        input: '',
        base: 10,
        width: 16,
        history: [],
        error: '',
        copied: '',
        fresh: false,
        widths: WIDTHS,
        basesInOrder: [16, 10, 8, 2],
        baseNames: { 16: 'HEX', 10: 'DEC', 8: 'OCT', 2: 'BIN' },

        init() {
            const saved = store.load();
            this.mode = saved.mode === 'programmer' ? 'programmer' : 'simple';
            this.input = typeof saved.input === 'string' ? saved.input.slice(0, 500) : '';
            this.base = BASES[saved.base] ? Number(saved.base) : 10;
            this.width = WIDTHS.includes(saved.width) ? saved.width : 16;
            this.history = Array.isArray(saved.history) ? saved.history.filter((row) => typeof row?.expr === 'string' && typeof row?.result === 'string').slice(0, MAX_HISTORY) : [];
            ['mode', 'input', 'base', 'width', 'history'].forEach((field) => this.$watch(field, () => this.persist()));
            this.focusInput();
        },

        persist() {
            store.save({ mode: this.mode, input: this.input, base: this.base, width: this.width, history: this.history });
        },

        focusInput() {
            // En el celular, enfocar abriría el teclado arriba de los botones.
            if (window.matchMedia('(pointer: fine)').matches) this.$nextTick(() => this.$refs.input?.focus());
        },

        /** El valor en vivo de la de programar; con una cuenta a medio escribir, el último que dio bien. */
        get live() {
            const result = evalProgrammer(this.input, this.base, this.width);
            if (!result.error) lastLive = result;
            return { ...(lastLive ?? evalProgrammer('', this.base, this.width)), error: result.error };
        },

        rows() {
            const { value } = this.live;
            return this.basesInOrder.map((base) => ({ base, name: this.baseNames[base], text: base === 2 ? groupBinary(value, this.width) : toBase(value, base), copy: toBase(value, base) }));
        },

        get signedText() {
            return String(this.live.signed).replace('-', '−');
        },

        get isNegative() {
            return this.live.signed < 0n;
        },

        /** El carácter de ese valor, si es uno de los imprimibles de ASCII. */
        get charText() {
            const { value } = this.live;
            return value >= 32n && value <= 126n ? String.fromCharCode(Number(value)) : '';
        },

        /** Los bits, de a 16 por fila y de a 4 por grupo; el de más peso, primero. */
        bitRows() {
            const { value } = this.live;
            const rows = [];
            for (let top = this.width - 1; top >= 0; top -= 16) {
                const low = Math.max(0, top - 15);
                const nibbles = [];
                for (let start = top; start >= low; start -= 4) {
                    const bits = [];
                    for (let bit = start; bit > start - 4 && bit >= low; bit--) bits.push({ index: bit, on: Boolean((value >> BigInt(bit)) & 1n) });
                    nibbles.push(bits);
                }
                rows.push({ top, low, nibbles });
            }
            return rows;
        },

        flip(bit) {
            this.setValue(this.live.value ^ (1n << BigInt(bit)));
        },

        setValue(value) {
            this.input = toBase(BigInt.asUintN(this.width, value), this.base);
            this.error = '';
            this.fresh = true;
        },

        setMode(mode) {
            this.mode = mode;
            this.input = '';
            this.error = '';
            this.fresh = false;
            this.focusInput();
        },

        /** Cambiar de base lleva lo que hay escrito a la base nueva. */
        setBase(base) {
            const result = evalProgrammer(this.input, this.base, this.width);
            this.base = base;
            this.error = '';
            if (!result.error && this.input.trim() !== '') {
                this.input = toBase(result.value, base);
                this.fresh = true;
            } else if (result.error) {
                this.input = '';
            }
            this.focusInput();
        },

        digitEnabled(digit) {
            return parseInt(digit, 16) < this.base;
        },

        /** Lo que empieza una cuenta nueva reemplaza al resultado; un operador sigue desde él. */
        press(text, startsNew = false) {
            if (this.fresh && startsNew) this.input = '';
            const field = this.$refs.input;
            const [from, to] = field && document.activeElement === field ? [field.selectionStart, field.selectionEnd] : [this.input.length, this.input.length];
            this.input = this.input.slice(0, from) + text + this.input.slice(to);
            this.fresh = false;
            this.error = '';
            this.$nextTick(() => {
                this.focusInput();
                field?.setSelectionRange(from + text.length, from + text.length);
            });
        },

        backspace() {
            this.input = this.fresh ? '' : this.input.slice(0, -1);
            this.fresh = false;
            this.error = '';
            this.focusInput();
        },

        clear() {
            this.input = '';
            this.error = '';
            this.fresh = false;
            this.focusInput();
        },

        square() {
            this.press('²');
        },

        addHistory(expr, result) {
            if (expr !== result) this.history = [{ expr, result }, ...this.history].slice(0, MAX_HISTORY);
        },

        equals() {
            if (this.input.trim() === '') return;
            if (this.mode === 'simple') {
                const result = evalSimple(this.input);
                if (result.error) {
                    this.error = result.error;
                    return;
                }
                this.addHistory(this.input, result.text);
                this.input = result.text;
            } else {
                const result = evalProgrammer(this.input, this.base, this.width);
                if (result.error) {
                    this.error = result.error;
                    return;
                }
                const text = toBase(result.value, this.base);
                this.addHistory(`${this.input} (${this.baseNames[this.base]})`, `${text} (${this.baseNames[this.base]})`);
                this.input = text;
            }
            this.error = '';
            this.fresh = true;
            this.focusInput();
        },

        /** Con el teclado: Enter calcula, Escape borra (no cierra la ventana) y un número nuevo reemplaza al resultado. */
        onKey(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                this.equals();
            } else if (event.key === 'Escape') {
                event.preventDefault();
                this.clear();
            } else if (this.fresh && event.key.length === 1 && !event.ctrlKey && !event.metaKey) {
                if (/[0-9a-fA-F(,.√]/.test(event.key)) this.input = '';
                this.fresh = false;
            } else if (event.key === 'Backspace') {
                this.fresh = false;
            }
            if (this.error && event.key.length === 1) this.error = '';
        },

        reuse(row) {
            this.input = row.result.replace(/ \((HEX|DEC|OCT|BIN)\)$/, '');
            const named = row.result.match(/\((HEX|DEC|OCT|BIN)\)$/);
            if (named) {
                this.mode = 'programmer';
                this.base = Number(this.basesInOrder.find((base) => this.baseNames[base] === named[1]));
            }
            this.fresh = true;
            this.error = '';
            this.focusInput();
        },

        clearHistory() {
            this.history = [];
        },

        async copy(text) {
            if (await copyText(text)) {
                this.copied = text;
                clearTimeout(this._copiedTimer);
                this._copiedTimer = setTimeout(() => (this.copied = ''), 1500);
            }
        },

        copyInput() {
            if (this.input !== '') this.copy(this.input);
        },
    };
}
