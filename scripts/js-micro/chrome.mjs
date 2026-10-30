// Abre Chrome sin ventana con la caja de JavaScript (D115) cargada, para correr código igual que en la plataforma:
// las pruebas de la caja (probar-caja.mjs) y las del curso (probar.mjs). Sirve resources/js/runners/ y acorn.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import WebSocket from 'ws';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const CHROME = process.env.CHROME ?? '/usr/bin/google-chrome';

const PAGE = `<!doctype html><html><head><meta charset="utf-8">
<script type="importmap">{"imports": {"acorn": "/node_modules/acorn/dist/acorn.mjs"}}</script>
<script type="module">
import { execute } from '/resources/js/runners/js-caja.js';
const world = await (await fetch('/resources/js/runners/js-sandbox/world.js')).text();
window.correr = (code, options = {}) => {
    let live = '';
    const container = options.live ? document.getElementById('vivo') : null;
    return execute(world, code, { ...options, container, onLive: (out) => (live += out) })
        .then((r) => ({ ...r, liveOutput: () => live }));
};
window.listo = true;
</script></head><body><div id="vivo" style="width:600px;height:400px"></div></body></html>`;

export async function openChrome() {
    const port = 17990 + Math.floor(Math.random() * 100);
    const server = http.createServer((req, res) => {
        const url = decodeURIComponent(req.url.split('?')[0]);
        if (url === '/') return res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }).end(PAGE);
        const file = path.join(ROOT, url);
        const allowed = ['resources/js/runners', 'node_modules/acorn', 'public/img'].some((dir) => file.startsWith(path.join(ROOT, dir)));
        if (!allowed || !fs.existsSync(file) || fs.statSync(file).isDirectory()) return res.writeHead(404).end();
        const type = file.endsWith('.js') || file.endsWith('.mjs') ? 'text/javascript' : 'application/octet-stream';
        res.writeHead(200, { 'content-type': type }).end(fs.readFileSync(file));
    });
    await new Promise((r) => server.listen(port, '127.0.0.1', r));

    const profile = fs.mkdtempSync(path.join(process.env.TMPDIR ?? '/tmp', 'caja-js-'));
    const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`, '--no-first-run', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
    const wsUrl = await new Promise((resolve, reject) => {
        chrome.stderr.on('data', (d) => { const m = String(d).match(/ws:\/\/[^\s]+/); if (m) resolve(m[0]); });
        setTimeout(() => reject(new Error('Chrome no arrancó')), 15000);
    });
    const browser = new WebSocket(wsUrl);
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
    for (let i = 0; i < 100 && !(await evaluate('window.listo === true').catch(() => false)); i++) await new Promise((r) => setTimeout(r, 100));

    return {
        /** Corre el código en la caja y devuelve el resultado (como runJavaScript). */
        run: (code, options = {}) => evaluate(`window.correr(${JSON.stringify(code)}, ${JSON.stringify(options)}).then(async (r) => {
            if (${Boolean(options.live)}) await new Promise((d) => setTimeout(d, ${options.liveMs ?? 600}));
            return { ...r, live: r.liveOutput() };
        })`),
        evaluate,
        async close() {
            browser.close();
            chrome.kill();
            await new Promise((r) => (chrome.exitCode !== null ? r() : chrome.once('exit', r)));
            server.close();
            try {
                fs.rmSync(profile, { recursive: true, force: true });
            } catch {
                // Chrome a veces termina de escribir su perfil después de cerrarse.
            }
        },
    };
}
