// Los caracteres de la tabla (D120), sin pantalla. Del 0 al 127 son iguales en todas las tablas; lo que cambia es la
// parte extendida: la página 850 (consola de Windows en español), la 437 (DOS y el Gólem 8086) y Unicode.

const CP850 = 'ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜø£Ø×ƒáíóúñÑªº¿®¬½¼¡«»░▒▓│┤ÁÂÀ©╣║╗╝¢¥┐└┴┬├─┼ãÃ╚╔╩╦╠═╬¤ðÐÊËÈıÍÎÏ┘┌█▄¦Ì▀ÓßÔÒõÕµþÞÚÛÙýÝ¯´\u00AD±‗¾¶§÷¸°¨·¹³²■\u00A0';
const CP437 = 'ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■\u00A0';

// Los caracteres de control: abreviatura, nombre y cómo se escriben en el código (si tienen forma corta).
const CONTROL = {
    0: ['NUL', 'carácter nulo', '\\0'], 1: ['SOH', 'inicio de encabezado'], 2: ['STX', 'inicio de texto'], 3: ['ETX', 'fin de texto'],
    4: ['EOT', 'fin de transmisión'], 5: ['ENQ', 'consulta'], 6: ['ACK', 'acuse de recibo'], 7: ['BEL', 'timbre', '\\a'],
    8: ['BS', 'retroceso', '\\b'], 9: ['HT', 'tabulador horizontal', '\\t'], 10: ['LF', 'salto de línea', '\\n'], 11: ['VT', 'tabulador vertical', '\\v'],
    12: ['FF', 'salto de página', '\\f'], 13: ['CR', 'retorno de carro', '\\r'], 14: ['SO', 'desactivar mayúsculas'], 15: ['SI', 'activar mayúsculas'],
    16: ['DLE', 'escape de enlace de datos'], 17: ['DC1', 'control de dispositivo 1'], 18: ['DC2', 'control de dispositivo 2'], 19: ['DC3', 'control de dispositivo 3'],
    20: ['DC4', 'control de dispositivo 4'], 21: ['NAK', 'acuse negativo'], 22: ['SYN', 'espera sincrónica'], 23: ['ETB', 'fin de bloque'],
    24: ['CAN', 'cancelar'], 25: ['EM', 'fin del medio'], 26: ['SUB', 'sustituir'], 27: ['ESC', 'escape'],
    28: ['FS', 'separador de archivos'], 29: ['GS', 'separador de grupos'], 30: ['RS', 'separador de registros'], 31: ['US', 'separador de unidades'],
    127: ['DEL', 'borrar'],
};

const PUNCTUATION = {
    ' ': 'espacio', '!': 'exclamación cierra', '"': 'comillas', '#': 'numeral', $: 'pesos dólar', '%': 'porcentaje', '&': 'ampersand', "'": 'apóstrofo comilla simple',
    '(': 'paréntesis abre', ')': 'paréntesis cierra', '*': 'asterisco', '+': 'más', ',': 'coma', '-': 'guion menos', '.': 'punto', '/': 'barra',
    ':': 'dos puntos', ';': 'punto y coma', '<': 'menor', '=': 'igual', '>': 'mayor', '?': 'pregunta cierra', '@': 'arroba', '[': 'corchete abre',
    '\\': 'barra invertida', ']': 'corchete cierra', '^': 'circunflejo', _: 'guion bajo', '`': 'acento grave', '{': 'llave abre', '|': 'barra vertical', '}': 'llave cierra', '~': 'virgulilla',
};

const named = (group, pairs) => ({ group, chars: pairs });
const range = (group, from, to) => ({ group, from, to });

// Unicode tiene más de 149.000 caracteres: acá van los que sirven para programar. Otro se busca por su código.
const UNICODE_GROUPS = [
    range('Latín: tildes, eñe y signos', 0xa1, 0xff),
    named('Puntuación', [['–', 'raya corta'], ['—', 'raya larga'], ['‘', 'comilla simple abre'], ['’', 'comilla simple cierra'], ['“', 'comilla doble abre'], ['”', 'comilla doble cierra'], ['•', 'viñeta'], ['…', 'puntos suspensivos'], ['‰', 'por mil'], ['′', 'prima minutos'], ['″', 'doble prima segundos']]),
    named('Monedas', [['€', 'euro'], ['£', 'libra'], ['¥', 'yen'], ['₿', 'bitcoin'], ['₩', 'won'], ['₹', 'rupia']]),
    named('Flechas', [['←', 'flecha izquierda'], ['↑', 'flecha arriba'], ['→', 'flecha derecha'], ['↓', 'flecha abajo'], ['↔', 'flecha doble horizontal'], ['↕', 'flecha doble vertical'], ['↖', 'flecha diagonal'], ['↗', 'flecha diagonal'], ['↘', 'flecha diagonal'], ['↙', 'flecha diagonal'], ['⇐', 'flecha doble izquierda'], ['⇒', 'flecha doble derecha implica'], ['⇔', 'flecha doble equivale'], ['↵', 'flecha enter retorno']]),
    named('Matemática', [['±', 'más menos'], ['×', 'por multiplicar'], ['÷', 'dividido'], ['−', 'menos'], ['√', 'raíz'], ['∞', 'infinito'], ['≈', 'aproximado'], ['≠', 'distinto'], ['≤', 'menor o igual'], ['≥', 'mayor o igual'], ['∑', 'sumatoria'], ['∏', 'productoria'], ['∫', 'integral'], ['∂', 'derivada parcial'], ['∅', 'conjunto vacío'], ['∈', 'pertenece'], ['∉', 'no pertenece'], ['∩', 'intersección'], ['∪', 'unión'], ['⊂', 'subconjunto'], ['∀', 'para todo'], ['∃', 'existe'], ['¬', 'negación'], ['∧', 'y lógico'], ['∨', 'o lógico'], ['⊕', 'xor']]),
    named('Griegas', [['α', 'alfa'], ['β', 'beta'], ['γ', 'gamma'], ['δ', 'delta'], ['ε', 'épsilon'], ['θ', 'theta'], ['λ', 'lambda'], ['μ', 'mu'], ['π', 'pi'], ['ρ', 'rho'], ['σ', 'sigma'], ['τ', 'tau'], ['φ', 'fi'], ['ω', 'omega'], ['Γ', 'gamma mayúscula'], ['Δ', 'delta mayúscula'], ['Θ', 'theta mayúscula'], ['Λ', 'lambda mayúscula'], ['Π', 'pi mayúscula'], ['Σ', 'sigma mayúscula'], ['Φ', 'fi mayúscula'], ['Ω', 'omega mayúscula']]),
    range('Cuadros y líneas', 0x2500, 0x257f),
    range('Bloques', 0x2580, 0x259f),
    range('Figuras', 0x25a0, 0x25ff),
    named('Símbolos', [['✓', 'tilde correcto'], ['✗', 'cruz incorrecto'], ['★', 'estrella llena'], ['☆', 'estrella vacía'], ['♥', 'corazón'], ['♦', 'diamante'], ['♣', 'trébol'], ['♠', 'pica'], ['♪', 'nota musical'], ['♫', 'notas musicales'], ['☀', 'sol'], ['☁', 'nube'], ['☂', 'paraguas'], ['☃', 'muñeco de nieve'], ['⚠', 'advertencia'], ['⚡', 'rayo'], ['©', 'copyright'], ['®', 'registrado'], ['™', 'marca']]),
    named('Emojis (ocupan 4 bytes)', [['😀', 'cara sonriente emoji'], ['😂', 'risa emoji'], ['🤔', 'pensando emoji'], ['👍', 'pulgar arriba emoji'], ['🎉', 'festejo emoji'], ['🔥', 'fuego emoji'], ['🚀', 'cohete emoji'], ['🐍', 'serpiente python emoji'], ['☕', 'café java emoji'], ['🐘', 'elefante php emoji']]),
];

const MARKS = { '́': 'con tilde', '̀': 'con acento grave', '̂': 'con circunflejo', '̈': 'con diéresis', '̃': 'con virgulilla', '̊': 'con anillo', '̧': 'con cedilla' };

const plain = (text) => text.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

function letterName(char) {
    if (char === 'ñ' || char === 'Ñ') return `eñe ${char === 'Ñ' ? 'mayúscula' : 'minúscula'}`;
    const [base, mark] = [...char.normalize('NFD')];
    return mark && MARKS[mark] ? `${base} ${MARKS[mark]}` : '';
}

function item(table, code, char, group, name = '') {
    const control = code < 32 || code === 127 ? CONTROL[code] : null;
    const cp = char.codePointAt(0);
    const label = control ? control[0] : cp === 0x20 ? 'SP' : cp === 0xa0 ? 'NBSP' : cp === 0xad ? 'SHY' : char;
    return { key: `${table}-${code}`, table, code, cp, char, group, label, wide: label.length > 1, name: control ? `${control[0]} ${control[1]}` : name || PUNCTUATION[char] || letterName(char), escape: control?.[2] ?? null };
}

function extended(table, chars, group) {
    return [...chars].map((char, i) => item(table, 128 + i, char, group));
}

function unicodeItems() {
    // Algunos están en dos grupos (× en Latín y en Matemática): se muestra en el primero, y se busca por los dos nombres.
    const lists = UNICODE_GROUPS.map(({ group, chars, from, to }) => ({
        group,
        list: chars ?? Array.from({ length: to - from + 1 }, (_, i) => [String.fromCodePoint(from + i), '']),
    }));
    const names = new Map();
    lists.forEach(({ list }) => list.forEach(([char, name]) => name && names.set(char, name)));
    const seen = new Set();

    return lists.flatMap(({ group, list }) => list.filter(([char]) => !seen.has(char) && seen.add(char))
        .map(([char]) => item('unicode', char.codePointAt(0), char, group, names.get(char) ?? '')));
}

const hex = (n, pad = 2) => n.toString(16).toUpperCase().padStart(pad, '0');

const asciiItems = Array.from({ length: 128 }, (_, code) => {
    const char = String.fromCharCode(code);
    const isLetter = /[a-z]/i.test(char);
    return item('ascii', code, char, code < 32 || code === 127 ? 'De control (0–31 y 127)' : 'Imprimibles (32–126)', isLetter ? `letra ${char} ${/[a-z]/.test(char) ? 'minúscula' : 'mayúscula'}` : /\d/.test(char) ? `dígito ${char}` : '');
}).sort((a, b) => (a.group === b.group ? a.code - b.code : a.group.startsWith('Imprimibles') ? -1 : 1)); // Lo más usado, primero.

export const TABLES = {
    ascii: asciiItems,
    windows: extended('windows', CP850, 'Extendido de Windows, página 850 (128–255)'),
    dos: extended('dos', CP437, 'Extendido de DOS, página 437 (128–255)'),
    unicode: unicodeItems(),
};

export const TABLE_LABELS = { ascii: 'ASCII', windows: 'Windows 850', dos: 'DOS 437', unicode: 'Unicode' };

export const uPlus = (cp) => `U+${hex(cp, 4)}`;

export function utf8Bytes(cp) {
    return [...new TextEncoder().encode(String.fromCodePoint(cp))].map((b) => hex(b)).join(' ');
}

function escapeOf(entry) {
    if (entry.escape) return entry.escape;
    if (entry.table !== 'unicode') return `\\x${hex(entry.code)}`;
    return entry.cp > 0xffff ? `\\U${hex(entry.cp, 8)}` : `\\u${hex(entry.cp, 4)}`;
}

/** Todas las formas de un carácter, en el orden en que se ofrecen para copiar. */
export function forms(entry) {
    const control = entry.table === 'ascii' && entry.label !== entry.char && entry.label !== 'SP';
    return {
        symbol: control ? (entry.escape ?? `0x${hex(entry.code)}`) : entry.char,
        dec: String(entry.code),
        hex: `0x${hex(entry.code)}`,
        oct: entry.code.toString(8),
        bin: entry.code.toString(2).padStart(8, '0'),
        code: escapeOf(entry),
        html: `&#${entry.cp};`,
        utf8: utf8Bytes(entry.cp),
    };
}

export const FORM_LABELS = { symbol: 'Símbolo', dec: 'DEC', hex: 'HEX', oct: 'OCT', bin: 'BIN', code: 'Código', html: 'HTML', utf8: 'UTF-8' };

function computed(cp) {
    if (cp > 0x10ffff || (cp >= 0xd800 && cp <= 0xdfff)) return [];
    return [item('unicode', cp, String.fromCodePoint(cp), 'Unicode, fuera de la lista')];
}

/**
 * Busca en todas las tablas: un carácter pegado (ñ), un número (41: como decimal y como hexa), 0x41, 41h, U+00F1 o
 * parte de un nombre (ESC, arroba, flecha).
 */
export function search(query, limit = 150) {
    const text = query.trim();
    if (text === '' && query === '') return [];
    const all = Object.values(TABLES).flat();
    const single = [...query].length === 1 ? query : [...text].length === 1 ? text : null;
    const uplus = text.match(/^u\+([0-9a-f]{1,6})$/i);
    const hexa = text.match(/^(?:0x|\\x)([0-9a-f]+)$/i) ?? text.match(/^([0-9a-f]+)h$/i);
    let found;

    if (uplus) {
        const cp = parseInt(uplus[1], 16);
        found = all.filter((entry) => entry.cp === cp);
        if (!found.length) found = computed(cp);
    } else if (hexa) {
        const code = parseInt(hexa[1], 16);
        found = all.filter((entry) => entry.code === code);
    } else if (/^\d+$/.test(text)) {
        const [dec, asHex] = [parseInt(text, 10), parseInt(text, 16)];
        found = all.filter((entry) => entry.code === dec || entry.code === asHex || (text.length === 1 && entry.char === text));
    } else if (single) {
        const cp = single.codePointAt(0);
        found = all.filter((entry) => entry.cp === cp);
        if (!found.length && cp > 127) found = computed(cp);
    } else {
        const wanted = plain(text);
        // ESC es ESC, aunque otro nombre diga «escape».
        const exact = all.filter((entry) => entry.wide && plain(entry.label) === wanted);
        found = exact.length ? exact : wanted.length < 2 ? [] : all.filter((entry) => plain(`${entry.name} ${entry.group}`).includes(wanted));
    }

    return found.slice(0, limit);
}

/** La tabla por secciones. */
export function sectionsOf(entries) {
    const sections = new Map();
    for (const entry of entries) {
        if (!sections.has(entry.group)) sections.set(entry.group, { title: entry.group, items: [] });
        sections.get(entry.group).items.push(entry);
    }
    return [...sections.values()];
}
