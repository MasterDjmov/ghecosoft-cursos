// Prueba de la calculadora y de la tabla de caracteres (D120), sin navegador. Correrla después de tocar resources/js/tools/:
//   node scripts/herramientas/probar.mjs
import { evalProgrammer, evalSimple, groupBinary, toBase } from '../../resources/js/tools/calculator-core.js';
import { forms, search, sectionsOf, TABLES, uPlus, utf8Bytes } from '../../resources/js/tools/ascii-data.js';

let fails = 0;
const same = (name, got, want) => {
    if (JSON.stringify(got) !== JSON.stringify(want)) {
        fails++;
        console.log(`✗ ${name}: dio ${JSON.stringify(got)}, se esperaba ${JSON.stringify(want)}`);
    }
};

const simple = [
    ['2+2', '4'], ['0,1+0,2', '0,3'], ['0.1+0.2', '0,3'], ['2+3×4', '14'], ['(2+3)*4', '20'], ['10÷4', '2,5'], ['7 mod 3', '1'], ['-3²', '-9'], ['(-3)²', '9'],
    ['√9', '3'], ['2√9', '6'], ['2(3+1)', '8'], ['50%', '0,5'], ['200+10%', '220'], ['200-10%', '180'], ['200×10%', '20'], ['1−1', '0'], ['1/3', '0,33333333333333'], ['π', '3,1415926535898'], ['1,5+1,5', '3'], ['--2', '2'],
];
for (const [input, want] of simple) same(`simple ${input}`, evalSimple(input).text ?? evalSimple(input).error, want);
for (const [input, want] of [['1/0', 'No se puede dividir por cero.'], ['5 mod 0', 'No se puede dividir por cero.'], ['√-1', 'No hay raíz cuadrada de un número negativo.'], ['(2', 'Falta cerrar un paréntesis.'], ['2)', 'Sobra un paréntesis.'], ['2+', 'La cuenta quedó sin terminar.'], ['alert(1)', 'No entiendo «a».']]) {
    same(`simple error ${input}`, evalSimple(input).error, want);
}

const prog = (input, base, width) => {
    const r = evalProgrammer(input, base, width);
    return r.error ?? `${toBase(r.value, 16)}${r.overflow ? '!' : ''}`;
};
const programmer = [
    ['FF', 16, 8, 'FF'], ['ff', 16, 8, 'FF'], ['255', 10, 8, 'FF'], ['377', 8, 8, 'FF'], ['11111111', 2, 8, 'FF'], ['0x41', 10, 16, '41'], ['0b101', 10, 16, '5'], ["'A'", 10, 16, '41'],
    ['~0', 10, 8, 'FF'], ['-1', 10, 16, 'FFFF'], ['-1', 10, 64, 'FFFFFFFFFFFFFFFF'], ['1<<4', 10, 16, '10'], ['1<<8', 10, 8, '0!'], ['256', 10, 8, '0!'], ['255', 10, 8, 'FF'], ['-128', 10, 8, '80'], ['-129', 10, 8, '7F!'],
    ['F0&3C', 16, 8, '30'], ['F0|0F', 16, 8, 'FF'], ['FF^0F', 16, 8, 'F0'], ['10 mod 3', 10, 8, '1'], ['AD mod 10', 16, 16, 'D'], ['10%3', 10, 8, '1'], ['7/2', 10, 8, '3'], ['-7/2', 10, 8, 'FD'], ['255/2', 10, 8, '7F'],
    ['1+2<<1', 10, 8, '6'], ['6&3|8', 10, 8, 'A'], ['2*(3+4)', 10, 8, 'E'], ['', 10, 8, '0'], ['FFFFFFFFFFFFFFFF', 16, 64, 'FFFFFFFFFFFFFFFF'], ['B0', 16, 8, 'B0'],
];
for (const [input, base, width, want] of programmer) same(`programador ${input} (base ${base}, ${width} bits)`, prog(input, base, width), want);
for (const [input, base, want] of [['9', 8, '«9» no existe en octal.'], ['2', 2, '«2» no existe en binario.'], ['A', 10, '«A» no existe en decimal.'], ['12A', 10, '«A» no existe en decimal.'], ['1/0', 10, 'No se puede dividir por cero.'], ['1<<99999', 10, 'Ese corrimiento no se puede hacer.'], ['(1', 10, 'Falta cerrar un paréntesis.'], ['$', 10, 'No entiendo «$».']]) {
    same(`programador error ${input}`, prog(input, base, 16), want);
}
same('con signo', String(evalProgrammer('FF', 16, 8).signed), '-1');
same('sin desborde con 64 bits', evalProgrammer('1<<63', 10, 64).overflow, false);
same('bits agrupados', groupBinary(0x41n, 8), '0100 0001');

// Las tablas
same('las de control van juntas, después de las imprimibles', sectionsOf(TABLES.ascii).map((s) => s.items.length), [95, 33]);
same('128 en ASCII', TABLES.ascii.length, 128);
same('128 en Windows', TABLES.windows.length, 128);
same('128 en DOS', TABLES.dos.length, 128);
same('sin repetir en Unicode', TABLES.unicode.length, new Set(TABLES.unicode.map((e) => e.cp)).size === TABLES.unicode.length ? TABLES.unicode.length : -1);
const at = (table, code) => TABLES[table].find((e) => e.code === code);
same('ñ en 850', at('windows', 164).char, 'ñ');
same('ñ en 437', at('dos', 164).char, 'ñ');
same('ñ en Unicode', at('unicode', 241).char, 'ñ');
same('© solo en la 850', [at('windows', 184).char, at('dos', 184).char], ['©', '╕']);
same('tabla del 127', forms(at('ascii', 127)).hex, '0x7F');
same('A', forms(at('ascii', 65)), { symbol: 'A', dec: '65', hex: '0x41', oct: '101', bin: '01000001', code: '\\x41', html: '&#65;', utf8: '41' });
same('salto de línea', forms(at('ascii', 10)).symbol, '\\n');
same('ESC se copia en hexa', forms(at('ascii', 27)).symbol, '0x1B');
same('espacio', forms(at('ascii', 32)).symbol, ' ');
same('ñ de Windows', forms(at('windows', 164)), { symbol: 'ñ', dec: '164', hex: '0xA4', oct: '244', bin: '10100100', code: '\\xA4', html: '&#241;', utf8: 'C3 B1' });
same('ñ de Unicode', forms(at('unicode', 241)).code, '\\u00F1');
same('emoji', [forms(at('unicode', 0x1f680)).code, utf8Bytes(0x1f680), uPlus(0x1f680)], ['\\U0001F680', 'F0 9F 9A 80', 'U+1F680']);
const keys = (q) => search(q).map((e) => e.key);
same('buscar ñ', keys('ñ'), ['windows-164', 'dos-164', 'unicode-241']);
same('buscar A', keys('A'), ['ascii-65']);
same('buscar a no da A', keys('a'), ['ascii-97']);
same('buscar 41: decimal y hexa', keys('41'), ['ascii-41', 'ascii-65']);
same('buscar 0x41', keys('0x41'), ['ascii-65']);
same('buscar 41h', keys('41h'), ['ascii-65']);
same('buscar esc', keys('esc'), ['ascii-27']);
same('buscar arroba', keys('arroba'), ['ascii-64']);
same('buscar sin tilde', keys('flecha doble equivale'), ['unicode-8660']);
same('buscar U+00F1: el mismo carácter en cada tabla', keys('U+00F1'), ['windows-164', 'dos-164', 'unicode-241']);
same('fuera de la lista', keys('U+1F999'), ['unicode-129433']);
same('pegado fuera de la lista', keys('文'), ['unicode-25991']);
same('buscar espacio pegado', keys(' '), ['ascii-32']);
same('código imposible', keys('U+D800'), []);

if (fails) {
    console.log(`\n${fails} fallaron`);
    process.exit(1);
}
console.log('Todo bien.');
