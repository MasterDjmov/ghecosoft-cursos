#!/usr/bin/env node
// Prueba las micro-misiones de C y C++ con el Clang del navegador (D98, D100), que es donde las corre el alumno:
// abre Chrome sin ventana, entra con el admin local, va a un nodo con un ejemplo ejecutable y le pasa cada caso
// al ejecutor del ejemplo (el componente codeRunner). Compara la salida con la que dio gcc o g++.
//
//   python3 scripts/micro-misiones/gencpp.py cpp_r01.py --json /tmp/casos.json
//   node scripts/micro-misiones/browser-check.mjs /tmp/casos.json --nodo=/cursos/cpp/nodos/123
//
// Necesita el servidor local (APP_URL, por defecto http://localhost:8000), el admin del seeder (admin/admin123)
// y Google Chrome (o la variable CHROME). El compilador se baja una vez y queda en la caché de PERFIL.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import WebSocket from 'ws';

const args = process.argv.slice(2);
const casesFile = args.find((a) => !a.startsWith('--'));
const nodePath = (args.find((a) => a.startsWith('--nodo=')) ?? '').slice(7);
const BASE = process.env.APP_URL ?? 'http://localhost:8000';
const CHROME = process.env.CHROME ?? '/usr/bin/google-chrome';
const PROFILE = process.env.PERFIL ?? path.join(os.tmpdir(), 'ghecosoft-clang-perfil');
const PORT = 19222 + Math.floor(Math.random() * 100);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

if (!casesFile || !nodePath) {
    console.error('Uso: node browser-check.mjs casos.json --nodo=/cursos/cpp/nodos/ID');
    process.exit(2);
}
const cases = JSON.parse(fs.readFileSync(casesFile, 'utf8'));

const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${PROFILE}`, '--no-first-run', 'about:blank'], { stdio: 'ignore' });
process.on('exit', () => chrome.kill());

let target;
for (let i = 0; i < 50 && !target; i++) {
    await sleep(200);
    try {
        target = (await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json()).find((t) => t.type === 'page');
    } catch {
        // Chrome todavía no abrió el puerto.
    }
}
const ws = new WebSocket(target.webSocketDebuggerUrl, { perMessageDeflate: false });
await new Promise((r) => ws.once('open', r));
let seq = 0;
const pending = new Map();
ws.on('message', (raw) => {
    const msg = JSON.parse(raw);
    if (msg.id && pending.has(msg.id)) {
        pending.get(msg.id)(msg);
        pending.delete(msg.id);
    }
});
const send = (method, params = {}) => new Promise((resolve) => {
    const id = ++seq;
    pending.set(id, resolve);
    ws.send(JSON.stringify({ id, method, params }));
});
const evaluate = async (expression) => {
    const r = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true, timeout: 600000 });
    if (r.result?.exceptionDetails) throw new Error(r.result.exceptionDetails.exception?.description ?? 'error en la página');
    return r.result?.result?.value;
};
const go = async (url) => {
    await send('Page.navigate', { url });
    for (let i = 0; i < 100; i++) {
        await sleep(200);
        if ((await evaluate('document.readyState')) === 'complete') return;
    }
};

await send('Page.enable');
await send('Runtime.enable');
await go(`${BASE}/login`);
if (await evaluate('!!document.querySelector("input[name=login]")')) {
    await evaluate(`(() => { const f = document.querySelector('input[name=login]').form;
        f.querySelector('input[name=login]').value = 'admin'; f.querySelector('input[name=password]').value = 'admin123'; f.submit(); })()`);
    await sleep(2500);
}
await go(BASE + nodePath);
for (let i = 0; i < 50; i++) {
    if (await evaluate('!!(window.Alpine && document.querySelector("[x-data^=codeRunner]"))')) break;
    await sleep(200);
}
console.log('Página:', await evaluate('document.title'));

let bad = 0;
for (const c of cases) {
    const output = await evaluate(`(async () => {
        const d = Alpine.$data(document.querySelector('[x-data^=codeRunner]'));
        d.code = ${JSON.stringify(c.code)};
        d.stdin = ${JSON.stringify(c.stdin)};
        await d.run();
        return d.output;
    })()`);
    // Si el compilador avisó algo, la salida trae su parte antes de «── Programa ──».
    const program = (output ?? '').includes('── Programa ──\n') ? output.split('── Programa ──\n')[1] : output ?? '';
    const ok = program.replace(/\n+$/, '') === c.expected.replace(/\n+$/, '');
    if (!ok) bad++;
    console.log(`${ok ? 'ok ' : 'MAL'} ${c.name}`);
    if (!ok) console.log(`   esperaba:\n${c.expected}\n   salió:\n${output}`);
}
console.log(`${cases.length - bad} de ${cases.length} iguales en el navegador`);
ws.close();
chrome.kill();
process.exit(bad ? 1 : 0);
