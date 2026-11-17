#!/usr/bin/env node
// Prueba del compilador de TypeScript del navegador (D115, fase 5) con Node: el mismo ts-compile.js que usa el worker,
// con el compilador y los .d.ts de node_modules. Revisa errores de tipos (con su línea), el JavaScript que sale,
// las líneas del source map y los módulos. Uso: node scripts/ts-micro/probar-compilador.mjs
import { ts, libs, MAIN } from './compilador.mjs';
import { compile } from '../../resources/js/runners/ts-compile.js';
import { explainTypeErrors } from '../../resources/js/runners/ts-errors.js';

let fails = 0;
const check = (name, got, want) => {
    const ok = JSON.stringify(got) === JSON.stringify(want);
    if (!ok) fails++;
    console.log(`${ok ? '✓' : '✗'} ${name}${ok ? '' : `\n    dio:      ${JSON.stringify(got)}\n    esperaba: ${JSON.stringify(want)}`}`);
};
const codes = (r) => r.diagnostics.map((d) => `${d.code}@${d.line}`);

let started = Date.now();
let r = compile(ts, libs, { [MAIN]: 'let nivel: number = 4;\nconsole.log(nivel);\n' });
check('un programa bien tipado compila', codes(r), []);
check('y sale JavaScript sin tipos', r.js['main.js'].trim(), 'let nivel = 4;\nconsole.log(nivel);');
console.log(`  (primera compilación con los .d.ts: ${Date.now() - started} ms)`);

started = Date.now();
r = compile(ts, libs, { [MAIN]: 'const nombre: string = "Rigel";\nlet nivel: number = 4;\nnivel = "cinco";\n' });
check('TS2322 en la línea 3', codes(r), ['TS2322@3']);
check('el mensaje viene en español', r.diagnostics[0].message, "El tipo 'string' no se puede asignar al tipo 'number'.");
console.log(`  (segunda compilación, con los .d.ts en memoria: ${Date.now() - started} ms)`);

r = compile(ts, libs, { [MAIN]: 'function medir(x) {\n  return x * 2;\n}\n' });
check('strict: el parámetro sin tipo es un error (TS7006)', codes(r), ['TS7006@1']);

r = compile(ts, libs, { [MAIN]: 'const lista = [1, 2, 3];\nconst cuarto = lista.find((n) => n > 5);\nconsole.log(cuarto.toFixed(1));\n' });
check('strictNullChecks: «posiblemente undefined» (TS18048)', codes(r), ['TS18048@3']);

r = compile(ts, libs, { [MAIN]: 'const lienzo = document.querySelector("canvas")!;\nconst ctx = lienzo.getContext("2d");\nconsole.log([1, 2].toSorted(), Object.groupBy([1], (n) => n));\n' });
check('el DOM y el JavaScript más nuevo están tipados', codes(r), []);

r = compile(ts, libs, { [MAIN]: 'interface Gema { x: number; valor: number }\n\ntype Forma = "estrella" | "luna";\n\nconst g: Gema = { x: 1, valor: 5 };\nconsole.log(g.valor);\nthrow new Error("se rompió");\n' });
check('el source map devuelve la línea del TypeScript', r.maps['main.js'][r.js['main.js'].split('\n').findIndex((l) => l.includes('throw')) + 1], 7);

r = compile(ts, libs, {
    [MAIN]: 'import { Vec2, sumar } from "./vec2.js";\nconst a: Vec2 = { x: 1, y: 2 };\nconsole.log(sumar(a, a));\n',
    'vec2.ts': 'export interface Vec2 { x: number; y: number }\nexport const sumar = (a: Vec2, b: Vec2): Vec2 => ({ x: a.x + b.x, y: a.y + b.y });\n',
});
check('los módulos se importan con ./vec2.js', [codes(r), Object.keys(r.js).sort()], [[], ['main.js', 'vec2.js']]);
check('y el import queda igual en el JavaScript', r.js['main.js'].includes('from "./vec2.js"'), true);

r = compile(ts, libs, { 'main.ts': 'import { Vec2 } from "./vec2.js";\nconst a: Vec2 = { x: 1, y: "2" };\n', 'vec2.ts': 'export interface Vec2 { x: number; y: number }\n' });
check('el error en un objeto apunta a la propiedad', codes(r), ['TS2322@2']);

r = compile(ts, libs, { [MAIN]: 'const espera = (ms: number) => new Promise((listo) => setTimeout(listo, ms));\nawait espera(10);\n' });
check('el await suelto anda (cada archivo es un módulo)', codes(r), []);

r = compile(ts, libs, { [MAIN]: 'let x = ;\n' });
check('un error de escritura (TS1109)', codes(r), ['TS1109@1']);

r = compile(ts, libs, { [MAIN]: 'const lista: number[] = [1, 2];\nconst x: number = lista[5];\n' }, { noUncheckedIndexedAccess: true });
check('el tsconfig de la consigna suma opciones (noUncheckedIndexedAccess)', codes(r), ['TS2322@2']);

r = compile(ts, libs, { [MAIN]: 'let nivel: number = 1;\nnivel = null;\n' }, { strict: false });
check('y también las puede apagar (strict: false)', codes(r), []);

r = compile(ts, libs, { [MAIN]: 'const x = 1;\n' }, { noExisto: true });
check('una opción que no existe es un error de la configuración', r.diagnostics.map((d) => [d.code, d.line]), [['TS5023', null]]);

r = compile(ts, libs, {
    [MAIN]: 'import { brillo } from "./estrellas.js";\nconst b: number = brillo("Vega");\n',
    'estrellas.d.ts': 'export function brillo(nombre: string): number;\n',
});
check('un .d.ts describe un .js sin tipos (y no genera JavaScript)', [codes(r), Object.keys(r.js).sort()], [[], ['main.js']]);

r = compile(ts, libs, { [MAIN]: 'import { brillo } from "./estrellas.js";\nbrillo(3);\n', 'estrellas.d.ts': 'export function brillo(nombre: string): number;\n' });
check('y el compilador revisa las llamadas contra el .d.ts', codes(r), ['TS2345@2']);

const text = explainTypeErrors(compile(ts, libs, { [MAIN]: 'let nivel: number = 4;\nnivel = "cinco";\n' }).diagnostics);
check('la explicación nombra la línea, la criatura y el código', [text.includes('Línea 2'), text.includes('Goblin'), text.includes('TS2322')], [true, true, true]);
console.log(`\n${text}\n`);

console.log(fails ? `\n${fails} con problemas` : '\nTodo bien');
process.exit(fails ? 1 : 0);
