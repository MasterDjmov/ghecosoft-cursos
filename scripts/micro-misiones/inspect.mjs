#!/usr/bin/env node
// Corre el inspector de HTML y CSS (D102, resources/js/runners/inspector.js) en Chrome sin ventana, que es donde lo
// corre el alumno: así la salida esperada de cada micro-misión sale del mismo código, nunca a mano. No hace falta
// el servidor: el inspector solo usa DOMParser, que ya está en una pestaña vacía.
//
//   node scripts/micro-misiones/inspect.mjs casos.json salida.json
//   casos.json: [{ "name": "...", "code": "<!DOCTYPE html>…", "checks": "h1\nimg @alt" }, …]
//   salida.json: { "name": "informe", … }
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import WebSocket from 'ws';

const [casesFile, outFile] = process.argv.slice(2);
if (!casesFile || !outFile) {
    console.error('Uso: node inspect.mjs casos.json salida.json');
    process.exit(2);
}
const here = path.dirname(fileURLToPath(import.meta.url));
const source = fs.readFileSync(path.join(here, '../../resources/js/runners/inspector.js'), 'utf8').replace(/^export /gm, '');
const cases = JSON.parse(fs.readFileSync(casesFile, 'utf8'));
const CHROME = process.env.CHROME ?? '/usr/bin/google-chrome';
const PORT = 19322 + Math.floor(Math.random() * 100);
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'ghecosoft-inspector-'));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, '--no-first-run', 'about:blank'], { stdio: 'ignore' });
process.on('exit', () => {
    chrome.kill();
    fs.rmSync(profile, { recursive: true, force: true });
});

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

const expression = `(() => { ${source}; const cases = ${JSON.stringify(cases)};
    return Object.fromEntries(cases.map((c) => [c.name, inspect(c.code, c.checks)])); })()`;
const r = await send('Runtime.evaluate', { expression, returnByValue: true });
if (r.result?.exceptionDetails) {
    console.error(r.result.exceptionDetails.exception?.description ?? 'error en Chrome');
    process.exit(1);
}
fs.writeFileSync(outFile, JSON.stringify(r.result.result.value, null, 1));
process.exit(0);
