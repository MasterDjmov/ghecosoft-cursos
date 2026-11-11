// Abre Chrome sin ventana con el ejecutor de C# cargado, para correr código igual que en la plataforma:
// sirve resources/js y public/toolchains/csharp (scripts/build-csharp-toolchain.sh).
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import WebSocket from 'ws';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const CHROME = process.env.CHROME ?? '/usr/bin/google-chrome';

const PAGE = `<!doctype html><html><head><meta charset="utf-8"><script type="module">
import { runCsharp } from '/resources/js/runners/csharp.js';
window.correr = (code, options = {}) => runCsharp(code, options);
window.listo = true;
</script></head><body></body></html>`;

const TYPES = { '.js': 'text/javascript', '.mjs': 'text/javascript', '.wasm': 'application/wasm', '.json': 'application/json' };

export async function openChrome() {
    const port = 18100 + Math.floor(Math.random() * 100);
    const server = http.createServer((req, res) => {
        const url = decodeURIComponent(req.url.split('?')[0]);
        if (url === '/') return res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }).end(PAGE);
        // Sin Vite: sql.js (de la Bóveda) es CommonJS, se envuelve como módulo; el .wasm se sirve de node_modules.
        if (url === '/__sqljs.js') {
            const text = fs.readFileSync(path.join(ROOT, 'node_modules/sql.js/dist/sql-wasm.js'), 'utf8');
            return res.writeHead(200, { 'content-type': 'text/javascript' }).end(`var module = { exports: {} }; var exports = module.exports;\n${text}\nexport default module.exports;`);
        }
        if (url === '/__sqljs-url.js') return res.writeHead(200, { 'content-type': 'text/javascript' }).end("export default '/node_modules/sql.js/dist/sql-wasm.wasm';");
        if (url === '/node_modules/sql.js/dist/sql-wasm.wasm') return res.writeHead(200, { 'content-type': 'application/wasm' }).end(fs.readFileSync(path.join(ROOT, url)));
        const file = url.startsWith('/toolchains/') ? path.join(ROOT, 'public', url) : path.join(ROOT, url);
        const allowed = url.startsWith('/toolchains/csharp/') || url.startsWith('/resources/js/');
        if (!allowed || !fs.existsSync(file) || fs.statSync(file).isDirectory()) return res.writeHead(404).end();
        let body = fs.readFileSync(file);
        if (url.endsWith('.js') && url.startsWith('/resources/js/')) {
            body = String(body).replace("'sql.js/dist/sql-wasm.js'", "'/__sqljs.js'").replace("'sql.js/dist/sql-wasm.wasm?url'", "'/__sqljs-url.js'");
        }
        res.writeHead(200, { 'content-type': TYPES[path.extname(file)] ?? 'application/octet-stream' }).end(body);
    });
    await new Promise((r) => server.listen(port, '127.0.0.1', r));

    const profile = fs.mkdtempSync(path.join(process.env.TMPDIR ?? '/tmp', 'csharp-'));
    const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`, '--no-first-run', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
    const wsUrl = await new Promise((resolve, reject) => {
        chrome.stderr.on('data', (d) => { const m = String(d).match(/ws:\/\/[^\s]+/); if (m) resolve(m[0]); });
        setTimeout(() => reject(new Error('Chrome no arrancó')), 15000);
    });
    const browser = new WebSocket(wsUrl, { perMessageDeflate: false });
    await new Promise((r) => browser.on('open', r));
    let id = 0;
    const pending = new Map();
    browser.on('message', (m) => { const d = JSON.parse(m); if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); } });
    const send = (method, params = {}, sessionId) => new Promise((r) => { const i = ++id; pending.set(i, r); browser.send(JSON.stringify({ id: i, method, params, sessionId })); });
    const { result: { targetId } } = await send('Target.createTarget', { url: 'about:blank' });
    const { result: { sessionId } } = await send('Target.attachToTarget', { targetId, flatten: true });
    const page = (method, params) => send(method, params, sessionId);
    const evaluate = async (expression) => {
        const answer = await page('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
        if (answer.result?.exceptionDetails) throw new Error(answer.result.exceptionDetails.exception?.description ?? 'error en Chrome');
        return answer.result.result?.value;
    };
    await page('Page.enable');
    await page('Page.navigate', { url: `http://127.0.0.1:${port}/` });
    for (let i = 0; i < 100 && !(await evaluate('window.listo === true')); i++) await new Promise((r) => setTimeout(r, 100));

    return {
        run: (code, options = {}) => evaluate(`window.correr(${JSON.stringify(code)}, ${JSON.stringify(options)})`),
        close: () => { browser.close(); chrome.kill(); server.close(); },
    };
}
