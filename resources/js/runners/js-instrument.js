// Prepara el código del alumno para la caja de JavaScript (D115): lo lee con acorn (sin ejecutarlo), avisa los
// errores de sintaxis en español con su línea, y le pone el tope de vueltas: __tick__() al principio de cada bucle y
// de cada función, para que un while (true) no congele la pestaña (como el tope de órdenes del 8086). Las líneas
// no cambian (nada agrega saltos de línea), así los errores de la caja apuntan a la línea que escribió el alumno.
// Lo usan el ejecutor del navegador (javascript.js) y las pruebas del curso con Node (scripts/js-micro/).
import { parse } from 'acorn';

const LOOPS = new Set(['ForStatement', 'ForInStatement', 'ForOfStatement', 'WhileStatement', 'DoWhileStatement']);
const FUNCTIONS = new Set(['FunctionDeclaration', 'FunctionExpression', 'ArrowFunctionExpression']);

/** Los mensajes de acorn más comunes, en criollo. */
const SYNTAX = [
    [/^Unterminated string constant/, 'Una comilla abre un texto y no lo cierra.'],
    [/^Unterminated template/, 'Un texto con comillas invertidas (`) no se cierra.'],
    [/^Unterminated regular expression/, 'Una expresión regular (/…/) no se cierra.'],
    [/^Unterminated comment/, 'Un comentario /* no se cierra con */.'],
    [/^Identifier '(.+)' has already been declared/, 'Ya declaraste «$1» antes: no se puede declarar dos veces con let, const o class.'],
    [/^Unexpected keyword '(.+)'/, 'La palabra «$1» no puede ir acá.'],
    [/^The keyword '(.+)' is reserved/, '«$1» es una palabra reservada de JavaScript: no se puede usar como nombre.'],
    [/^Cannot use keyword 'await' outside an async function/, 'await solo se puede usar adentro de una función async (o afuera de toda función).'],
    [/^'return' outside of function/, 'return solo puede ir adentro de una función.'],
    [/^Assigning to rvalue/, 'A la izquierda del = tiene que haber una variable o una propiedad.'],
    [/^Invalid left-hand side in/, 'A la izquierda tiene que haber una variable o una propiedad.'],
    [/^Unexpected character '(.+)'/, 'Hay un carácter que JavaScript no entiende: «$1».'],
    [/^Unsyntactic break/, 'break solo puede ir adentro de un bucle o de un switch.'],
    [/^Unsyntactic continue/, 'continue solo puede ir adentro de un bucle.'],
    [/^Missing initializer in const declaration/, 'Una const necesita su valor en el mismo renglón: const x = 1;'],
    [/^Complex binding patterns require an initialization value/, 'La desestructuración necesita un valor: const { a } = objeto;'],
    [/^Deleting local variable in strict mode/, 'delete sirve para propiedades (delete objeto.x), no para variables.'],
    [/^Octal literal in strict mode/, 'Un número no puede empezar con 0 (salvo 0x, 0b, 0o o el 0 solo).'],
    [/^Unexpected token/, 'Hay algo que sobra o que falta acá (un símbolo que no va en ese lugar).'],
];

function spanishSyntax(message, atEnd) {
    const clean = message.replace(/\s*\(\d+:\d+\)$/, '');
    if (atEnd && /^Unexpected token/.test(clean)) {
        return 'El código termina antes de tiempo: ¿falta cerrar una llave }, un paréntesis ) o un corchete ]?';
    }
    for (const [pattern, text] of SYNTAX) {
        const found = clean.match(pattern);
        if (found) return text.replace(/\$(\d)/g, (all, n) => found[Number(n)]);
    }
    return clean;
}

function walk(node, visit) {
    if (!node || typeof node.type !== 'string') return;
    visit(node);
    for (const key of Object.keys(node)) {
        if (key === 'loc') continue;
        const value = node[key];
        if (Array.isArray(value)) {
            for (const child of value) walk(child, visit);
        } else if (value && typeof value.type === 'string') {
            walk(value, visit);
        }
    }
}

/**
 * @returns {{code: string, error: null} | {code: null, error: {name: string, message: string, original: string, line: number, column: number}}}
 */
export function instrument(source, index = 0) {
    const code = String(source ?? '');
    let ast;
    try {
        ast = parse(code, { ecmaVersion: 'latest', sourceType: 'module', locations: true, allowHashBang: true });
    } catch (e) {
        const line = e.loc?.line ?? 1;
        const column = (e.loc?.column ?? 0) + 1;
        const atEnd = typeof e.pos === 'number' && code.slice(e.pos).trim() === '';
        return { code: null, error: { name: 'SyntaxError', message: spanishSyntax(e.message, atEnd), original: e.message.replace(/\s*\(\d+:\d+\)$/, ''), line, column } };
    }

    const edits = [];
    walk(ast, (node) => {
        if (LOOPS.has(node.type)) {
            const body = node.body;
            if (body.type === 'BlockStatement') {
                edits.push([body.start + 1, '__tick__();']);
            } else {
                edits.push([body.start, '{__tick__();']);
                edits.push([body.end, '}']);
            }
        } else if (FUNCTIONS.has(node.type) && node.body.type === 'BlockStatement') {
            edits.push([node.body.start + 1, '__tick__();']);
        }
    });

    // De atrás para adelante, así las posiciones siguen valiendo; a igual posición, el cierre «}» va primero.
    edits.sort((a, b) => b[0] - a[0] || (a[1] === '}' ? -1 : 1));
    let out = code;
    for (const [at, text] of edits) out = out.slice(0, at) + text + out.slice(at);
    // Un #! en la primera línea tiene que quedar primero.
    const bang = out.match(/^#![^\n]*/);
    out = bang ? `${bang[0]}\n__begin__(${index});${out.slice(bang[0].length + 1)}` : `__begin__(${index});${out}`;

    return { code: out, error: null };
}

/**
 * Si el alumno escribió una página entera (HTML con sus <script>), separa la página de los scripts: los scripts
 * van a la caja por separado (con su línea dentro de la página) y los de afuera (src=) no se cargan.
 *
 * @returns {{page: string|null, scripts: {code: string, offset: number}[], skipped: string[]}}
 */
export function splitPage(source) {
    const code = String(source ?? '');
    if (!/^\s*</.test(code)) return { page: null, scripts: [{ code, offset: 0 }], skipped: [] };
    const scripts = [];
    const skipped = [];
    const page = code.replace(/<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi, (all, attributes, body, at) => {
        const src = attributes.match(/\bsrc\s*=\s*["']?([^"'\s>]+)/i);
        if (src) {
            skipped.push(src[1]);
            return '';
        }
        if (/\btype\s*=\s*["']?(?!module|text\/javascript|application\/javascript)[^"'\s>]+/i.test(attributes)) return all;
        const start = at + all.indexOf('>') + 1;
        scripts.push({ code: body, offset: code.slice(0, start).split('\n').length - 1 });
        return '';
    });

    return { page, scripts, skipped };
}
