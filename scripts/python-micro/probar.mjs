// D111: corre con Pyodide (el mismo Python del navegador del alumno) la solución de cada micro-misión de Python
// que vino de una misión (las que tienen «antes:» en el meta; con --todas, todas) y la compara con su salida
// esperada, igual que el navegador (compare.js). También revisa que el código inicial NO dé ya la salida esperada.
//
//   (una vez) npm i --prefix /tmp/pyo pyodide@0.29.5
//   PYODIDE_DIR=/tmp/pyo/node_modules/pyodide node scripts/python-micro/probar.mjs cursos/python/0*.md [--todas]
//
// La entrada y la salida se manejan como en resources/js/workers/python.worker.js: stdout y stderr juntos, la
// entrada por líneas (sin la última vacía) y variables limpias en cada ejecución.
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { normalize, describeDifference } from '../../resources/js/runners/compare.js';

const dir = process.env.PYODIDE_DIR;
if (!dir) {
    console.error('Falta PYODIDE_DIR (la carpeta del paquete pyodide de npm).');
    process.exit(2);
}
const { loadPyodide } = await import(pathToFileURL(path.join(dir, 'pyodide.mjs')).href);
const pyodide = await loadPyodide({ indexURL: dir + path.sep });

const all = process.argv.includes('--todas');
const files = process.argv.slice(2).filter((arg) => !arg.startsWith('--'));

function section(block, name) {
    const m = block.match(new RegExp(`^#### ${name}\\n([\\s\\S]*?)(?=^#### |(?![\\s\\S]))`, 'm'));
    return m ? m[1] : null;
}

function fence(body) {
    const m = body?.match(/```[a-z]*\n([\s\S]*?)\n```/);
    return m ? m[1] : null;
}

async function run(code, stdin) {
    let output = '';
    const decoder = new TextDecoder();
    const write = (buffer) => {
        output += decoder.decode(buffer, { stream: true });
        return buffer.length;
    };
    pyodide.setStdout({ write });
    pyodide.setStderr({ write });
    const lines = String(stdin ?? '').split('\n');
    if (lines.at(-1) === '') lines.pop();
    pyodide.setStdin({ stdin: () => (lines.length ? lines.shift() : null) });
    await pyodide.loadPackagesFromImports(code);
    const globals = pyodide.globals.get('dict')();
    globals.set('__name__', '__main__');
    let error = null;
    try {
        await pyodide.runPythonAsync(code, { globals });
    } catch (e) {
        error = String(e.message).split('\n').slice(-3).join('\n');
    } finally {
        globals.destroy();
        pyodide.runPython('import sys\nsys.stdout.flush()\nsys.stderr.flush()');
    }
    return { output, error };
}

let ok = 0;
const bad = [];
for (const file of files) {
    const text = fs.readFileSync(file, 'utf8');
    for (const block of text.split(/^(?=### )/m)) {
        const head = block.match(/^### Micro-misión (\S+) · (.*)/);
        if (!head) continue;
        const meta = block.match(/```meta\n([\s\S]*?)```/)?.[1] ?? '';
        if (!all && !/^antes:/m.test(meta)) continue;
        const solution = fence(section(block, 'Solución'));
        const expected = fence(section(block, 'Salida esperada'));
        if (!solution || expected === null) continue;
        const stdin = fence(section(block, 'Entrada'));
        const result = await run(solution, stdin);
        const diff = describeDifference(expected, result.output);
        if (result.error || diff) {
            bad.push(`${head[1]} · ${head[2]}\n    ${result.error ?? diff}`);
            continue;
        }
        const starter = fence(section(block, 'Código inicial'));
        if (starter && normalize((await run(starter, stdin)).output) === normalize(expected)) {
            bad.push(`${head[1]} · ${head[2]}\n    el código inicial ya da la salida esperada`);
            continue;
        }
        ok++;
    }
}
console.log(`${ok} bien, ${bad.length} mal`);
for (const line of bad) console.log('  ' + line);
process.exit(bad.length ? 1 : 0);
