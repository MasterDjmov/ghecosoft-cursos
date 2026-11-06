// La cuenta de la calculadora (D120), sin pantalla: un analizador propio, nunca eval. La simple usa números con coma;
// la de programar, enteros exactos (BigInt) en la base elegida, con la misma prioridad de operadores que C.

const MAX_LENGTH = 500;
const MAX_SHIFT = 4096n;

class CalcError extends Error {}

export const BASES = { 16: 'hexadecimal', 10: 'decimal', 8: 'octal', 2: 'binario' };

/** Sin el ruido de los números con coma: 0,1 + 0,2 da 0,3. */
export function formatSimple(value) {
    return String(Number(value.toPrecision(14))).replace('.', ',');
}

function parseSimple(source) {
    const text = source.replace(/\s+/g, '').replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-').replace(/,/g, '.').toLowerCase();
    let at = 0;
    const peek = () => text[at];
    const accept = (token) => (text.startsWith(token, at) ? ((at += token.length), true) : false);

    function primary() {
        if (accept('(')) {
            const inner = sum();
            if (!accept(')')) throw new CalcError('Falta cerrar un paréntesis.');
            return inner;
        }
        if (accept('π')) return Math.PI;
        const number = text.slice(at).match(/^(\d+\.?\d*|\.\d+)/);
        if (!number) throw new CalcError(at >= text.length ? 'La cuenta quedó sin terminar.' : `No entiendo «${peek()}».`);
        at += number[0].length;
        return Number(number[0]);
    }

    // `percentOf`: 200 + 10% suma el 10 % de 200; solo, 10% es 0,1.
    function postfix() {
        let value = primary();
        let percentOf = null;
        for (;;) {
            if (accept('²')) {
                value *= value;
                percentOf = null;
            } else if (accept('%')) {
                percentOf = value;
                value /= 100;
            } else {
                return { value, percentOf };
            }
        }
    }

    function factor() {
        if (accept('-')) return { value: -factor().value, percentOf: null };
        if (accept('+')) return factor();
        if (accept('√')) {
            const inside = factor().value;
            if (inside < 0) throw new CalcError('No hay raíz cuadrada de un número negativo.');
            return { value: Math.sqrt(inside), percentOf: null };
        }
        return postfix();
    }

    function term() {
        let left = factor();
        for (;;) {
            if (accept('*')) left = { value: left.value * factor().value, percentOf: null };
            else if (accept('/')) left = { value: divide(left.value, factor().value), percentOf: null };
            else if (accept('mod')) {
                const right = factor().value;
                if (right === 0) throw new CalcError('No se puede dividir por cero.');
                left = { value: left.value % right, percentOf: null };
            } else if (peek() === '(' || peek() === '√' || peek() === 'π') left = { value: left.value * factor().value, percentOf: null };
            else return left;
        }
    }

    function sum() {
        let total = term().value;
        for (;;) {
            if (accept('+')) {
                const right = term();
                total += right.percentOf === null ? right.value : (total * right.percentOf) / 100;
            } else if (accept('-')) {
                const right = term();
                total -= right.percentOf === null ? right.value : (total * right.percentOf) / 100;
            } else return total;
        }
    }

    const result = sum();
    if (at < text.length) throw new CalcError(peek() === ')' ? 'Sobra un paréntesis.' : `No entiendo «${peek()}».`);
    return result;
}

function divide(a, b) {
    if (b === 0) throw new CalcError('No se puede dividir por cero.');
    return a / b;
}

/** @returns {{value: number, text: string}|{error: string}} */
export function evalSimple(source) {
    if (source.length > MAX_LENGTH) return { error: 'La cuenta es demasiado larga.' };
    try {
        const value = parseSimple(source);
        if (!Number.isFinite(value)) return { error: 'El resultado es demasiado grande.' };
        return { value, text: formatSimple(value) };
    } catch (e) {
        if (e instanceof CalcError || e instanceof RangeError) return { error: e instanceof CalcError ? e.message : 'La cuenta es demasiado larga.' };
        throw e;
    }
}

const DIGITS = { 16: /^[0-9a-f]+/i, 10: /^[0-9]+/, 8: /^[0-7]+/, 2: /^[01]+/ };

function literal(digits, base) {
    const prefix = { 16: '0x', 8: '0o', 2: '0b' }[base];
    return BigInt(prefix ? prefix + digits : digits);
}

function parseProgrammer(source, base) {
    const text = source.replace(/\s+/g, '').replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-');
    let at = 0;
    const accept = (token) => (text.slice(at, at + token.length).toLowerCase() === token ? ((at += token.length), true) : false);

    function primary() {
        if (accept('(')) {
            const inner = or();
            if (!accept(')')) throw new CalcError('Falta cerrar un paréntesis.');
            return inner;
        }
        const char = text.slice(at).match(/^'([\s\S])'/u);
        if (char) {
            at += char[0].length;
            return BigInt(char[1].codePointAt(0));
        }
        const rest = text.slice(at);
        // Con prefijo se puede escribir en otra base; 0b y 0o no valen en hexadecimal, donde b es un dígito.
        const prefixed = rest.match(/^0x([0-9a-f]+)/i) ?? (base !== 16 ? rest.match(/^0b([01]+)/i) ?? rest.match(/^0o([0-7]+)/i) : null);
        if (prefixed) {
            at += prefixed[0].length;
            return BigInt(prefixed[0].toLowerCase());
        }
        const digits = rest.match(DIGITS[base]);
        if (digits) {
            at += digits[0].length;
            if (/^[0-9a-f]/i.test(text.slice(at)) && !/^mod/i.test(text.slice(at))) throw new CalcError(`«${text[at]}» no existe en ${BASES[base]}.`);
            return literal(digits[0], base);
        }
        if (at >= text.length) throw new CalcError('La cuenta quedó sin terminar.');
        throw new CalcError(/^[0-9a-f]/i.test(text[at]) ? `«${text[at]}» no existe en ${BASES[base]}.` : `No entiendo «${text[at]}».`);
    }

    function unary() {
        if (accept('~')) return ~unary();
        if (accept('-')) return -unary();
        if (accept('+')) return unary();
        return primary();
    }

    function term() {
        let left = unary();
        for (;;) {
            if (accept('*')) left *= unary();
            else if (accept('/') || accept('÷')) {
                const right = unary();
                if (right === 0n) throw new CalcError('No se puede dividir por cero.');
                left /= right;
            } else if (accept('mod') || accept('%')) {
                const right = unary();
                if (right === 0n) throw new CalcError('No se puede dividir por cero.');
                left %= right;
            } else return left;
        }
    }

    function additive() {
        let left = term();
        for (;;) {
            if (accept('+')) left += term();
            else if (accept('-')) left -= term();
            else return left;
        }
    }

    function shift() {
        let left = additive();
        for (;;) {
            const leftShift = accept('<<');
            if (!leftShift && !accept('>>')) return left;
            const right = additive();
            if (right < 0n || right > MAX_SHIFT) throw new CalcError('Ese corrimiento no se puede hacer.');
            left = leftShift ? left << right : left >> right;
        }
    }

    function and() {
        let left = shift();
        while (accept('&')) left &= shift();
        return left;
    }

    function xor() {
        let left = and();
        while (accept('^')) left ^= and();
        return left;
    }

    function or() {
        let left = xor();
        while (accept('|')) left |= xor();
        return left;
    }

    const result = or();
    if (at < text.length) throw new CalcError(text[at] === ')' ? 'Sobra un paréntesis.' : `No entiendo «${text[at]}».`);
    return result;
}

/**
 * La cuenta se hace sin tope y se recorta al ancho recién al final, como un registro.
 * @returns {{value: bigint, signed: bigint, overflow: boolean}|{error: string}}
 */
export function evalProgrammer(source, base, width) {
    if (source.length > MAX_LENGTH) return { error: 'La cuenta es demasiado larga.' };
    const bits = BigInt(width);
    try {
        const raw = source.trim() === '' ? 0n : parseProgrammer(source, base);
        return {
            value: BigInt.asUintN(width, raw),
            signed: BigInt.asIntN(width, raw),
            overflow: raw >= 1n << bits || raw < -(1n << (bits - 1n)),
        };
    } catch (e) {
        if (e instanceof CalcError) return { error: e.message };
        if (e instanceof RangeError) return { error: 'El número es demasiado grande.' };
        throw e;
    }
}

export function toBase(value, base) {
    return value.toString(base).toUpperCase();
}

/** 1010 0001, de a cuatro desde la derecha. */
export function groupBinary(value, width) {
    return value.toString(2).padStart(width, '0').replace(/(.{4})(?=.)/g, '$1 ');
}
