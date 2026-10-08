// Cómo se compara una salida con la esperada, igual que en el servidor (LocalCodeRunner::normalize). Lo
// usan el «Coincide» del ejecutor (ejemplos y micro-misiones) y la corrección asistida (cases.js).

// Lo que no se ve pero cambia el texto: el BOM, los espacios de ancho cero, el guion opcional y los controles.
const INVISIBLE = /[\uFEFF\u200B-\u200D\u2060\u00AD\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g;
// Los espacios «raros» (el duro de Windows, los finos) cuentan como un espacio común.
const ODD_SPACES = /[\u00A0\u2000-\u200A\u202F\u205F\u3000]/g;

/**
 * Sin \r de Windows, sin caracteres invisibles, con los espacios raros como espacios, las tildes en una sola
 * forma (NFC), sin espacios al final de cada línea ni líneas vacías en las puntas. La sangría sí cuenta.
 */
export function normalize(text) {
    return String(text ?? '')
        .normalize('NFC')
        .replace(/\r\n?/g, '\n')
        .replace(INVISIBLE, '')
        .replace(ODD_SPACES, ' ')
        .replace(/[ \t]+$/gm, '')
        .replace(/^\n+|\n+$/g, '');
}

const NAMES = {
    ' ': 'un espacio',
    '\t': 'un tabulador',
    '\u2013': 'un guion medio (–)',
    '\u2014': 'una raya (—)',
    '\u2018': 'una comilla tipográfica',
    '\u2019': 'una comilla tipográfica',
    '\u201C': 'una comilla tipográfica',
    '\u201D': 'una comilla tipográfica',
    '\uFFFD': 'un carácter roto (�, problema de codificación)',
};

function describe(char) {
    if (char === undefined) return 'el final de la línea';
    const code = char.codePointAt(0);
    const name = NAMES[char] ?? `«${char}»`;

    return code > 126 ? `${name} (U+${code.toString(16).toUpperCase().padStart(4, '0')})` : name;
}

/**
 * La primera diferencia, en palabras, para que el alumno vea qué no coincide (sobre todo lo que en pantalla
 * se ve igual). null si coinciden.
 */
export function describeDifference(expected, got) {
    const want = normalize(expected).split('\n');
    const have = normalize(got).split('\n');
    for (let i = 0; i < Math.max(want.length, have.length); i++) {
        const a = want[i];
        const b = have[i];
        if (a === b) continue;
        if (b === undefined) return `Falta la línea ${i + 1}: «${a}».`;
        if (a === undefined) return `Sobra la línea ${i + 1}: «${b}».`;
        const ca = Array.from(a);
        const cb = Array.from(b);
        let col = 0;
        while (col < ca.length && ca[col] === cb[col]) col++;
        const where = col ? `después de «${ca.slice(0, col).join('')}»` : 'al principio';

        return `En la línea ${i + 1}, ${where}: se esperaba ${describe(ca[col])} y tu salida tiene ${describe(cb[col])}.`;
    }

    return null;
}
