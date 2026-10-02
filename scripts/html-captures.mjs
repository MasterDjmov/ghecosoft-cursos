#!/usr/bin/env node
// «Así tiene que quedar» (D77): genera las capturas de cada práctica de HTML y CSS a partir de su solución de
// referencia —celular (390 px) y compu (1280 px), página completa, en WebP— y escribe la parte
// «#### Cómo debe quedar» en el .md. Tailwind se compila igual que en la vista previa del alumno
// (resources/js/runners/html.js), así lo que se compara es lo mismo que se ve.
//
//   node scripts/html-captures.mjs cursos/html [--only=R02] [--force]
//
// Necesita Google Chrome (o la variable CHROME). Las imágenes /img/… se sirven desde public/.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { compile } from 'tailwindcss';
import WebSocket from 'ws';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const folder = path.resolve(args.find((a) => !a.startsWith('--')) ?? 'cursos/html');
const only = (args.find((a) => a.startsWith('--only=')) ?? '').slice(7);
const force = args.includes('--force');
const CHROME = process.env.CHROME ?? '/usr/bin/google-chrome';
const PORT = 17890 + Math.floor(Math.random() * 100);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ── Tailwind, como en runners/tailwind.js ──────────────────────────────────────────────────────────
const twDir = path.join(ROOT, 'node_modules/tailwindcss');
const SHEETS = Object.fromEntries(['index', 'theme', 'preflight', 'utilities'].flatMap((name) => {
    const css = fs.readFileSync(path.join(twDir, `${name}.css`), 'utf8');
    return [[`tailwindcss/${name}`, css], [`tailwindcss/${name}.css`, css], ...(name === 'index' ? [['tailwindcss', css]] : [])];
}));
const TAILWIND_BLOCK = /<style\b[^>]*type\s*=\s*["']text\/tailwindcss["'][^>]*>([\s\S]*?)<\/style>/gi;

async function render(html) {
    const blocks = [...html.matchAll(TAILWIND_BLOCK)];
    if (blocks.length === 0) return html;
    const compiler = await compile(blocks.map((b) => b[1]).join('\n'), {
        base: '/',
        loadStylesheet: async (id) => ({ path: id, base: '/', content: SHEETS[id] ?? (() => { throw new Error(`no se puede importar ${id}`); })() }),
    });
    const classes = new Set();
    for (const m of html.matchAll(/\bclass\s*=\s*(["'])([\s\S]*?)\1/gi)) m[2].split(/\s+/).filter(Boolean).forEach((c) => classes.add(c));
    const css = compiler.build([...classes]);
    let first = true;
    return html.replace(TAILWIND_BLOCK, () => (first ? ((first = false), `<style>${css}</style>`) : ''));
}

// ── Las prácticas de los .md ───────────────────────────────────────────────────────────────────────
function practices(file) {
    const text = fs.readFileSync(file, 'utf8');
    const found = [];
    const re = /^### (?:Misión|Encargo|Práctica|Desafío) ([A-Z0-9-]+) · .*$/gm;
    let m;
    const heads = [];
    while ((m = re.exec(text))) heads.push({ code: m[1], start: m.index });
    heads.forEach((h, i) => {
        const end = i + 1 < heads.length ? heads[i + 1].start : text.search(/^## /m) > h.start ? text.slice(h.start).search(/^## /m) + h.start : text.length;
        const body = text.slice(h.start, end === -1 ? text.length : end);
        const sol = body.match(/#### Solución de referencia\s+(`{3,4})html\n([\s\S]*?)\n\1/);
        if (sol) found.push({ code: h.code, solution: sol[2] });
    });
    return found;
}

function writeReferences(file, code, mobile, desktop) {
    let text = fs.readFileSync(file, 'utf8');
    const head = new RegExp(`^### (?:Misión|Encargo|Práctica|Desafío) ${code} · .*$`, 'm');
    const start = text.search(head);
    const bodyStart = text.indexOf('\n', start) + 1;
    const next = text.slice(bodyStart).search(/^#{2,3} /m);
    const end = next === -1 ? text.length : bodyStart + next;
    let block = text.slice(start, end);
    const part = `#### Cómo debe quedar\n\ncelular: ${mobile}\ncompu: ${desktop}\n\n`;
    block = /#### Cómo debe quedar\n[\s\S]*?(?=####|$)/.test(block)
        ? block.replace(/#### Cómo debe quedar\n[\s\S]*?(?=####|$)/, part)
        : block.replace(/#### Código inicial/, part + '#### Código inicial');
    fs.writeFileSync(file, text.slice(0, start) + block + text.slice(end));
}

// ── Servidor (public/ + la página a capturar) y Chrome ────────────────────────────────────────────
const pages = new Map();
const server = http.createServer((req, res) => {
    const url = decodeURIComponent(req.url.split('?')[0]);
    if (pages.has(url)) return res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }).end(pages.get(url));
    const file = path.join(ROOT, 'public', url);
    if (!file.startsWith(path.join(ROOT, 'public')) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) return res.writeHead(404).end();
    const types = { '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml' };
    res.writeHead(200, { 'content-type': types[path.extname(file)] ?? 'application/octet-stream' }).end(fs.readFileSync(file));
});
await new Promise((r) => server.listen(PORT, '127.0.0.1', r));

const profile = fs.mkdtempSync(path.join(process.env.TMPDIR ?? '/tmp', 'capturas-'));
const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`, '--no-first-run', '--hide-scrollbars', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
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
const evalv = async (expression) => (await page('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true })).result.result?.value;
await page('Page.enable');

async function shot(url, width, height) {
    await page('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: width < 600 });
    await page('Page.navigate', { url });
    // Que carguen las fuentes y las imágenes (las lazy, también).
    await evalv(`new Promise((r) => { const ok = () => Promise.all([document.fonts.ready, ...[...document.images].map((i) => i.complete ? 0 : new Promise((d) => { i.onload = i.onerror = d; }))]).then(r); document.readyState === 'complete' ? ok() : addEventListener('load', ok); setTimeout(r, 8000); })`);
    await sleep(300);
    const full = Math.min(8000, Math.max(height, await evalv('Math.ceil(document.documentElement.scrollHeight)')));
    await page('Emulation.setDeviceMetricsOverride', { width, height: full, deviceScaleFactor: 1, mobile: width < 600 });
    await sleep(300);
    const { result } = await page('Page.captureScreenshot', { format: 'webp', quality: 80, captureBeyondViewport: true });
    return Buffer.from(result.data, 'base64');
}

// ── A trabajar ─────────────────────────────────────────────────────────────────────────────────────
const outDir = path.join(folder, 'capturas');
fs.mkdirSync(outDir, { recursive: true });
let made = 0;
let skipped = 0;
let failed = 0;
for (const file of fs.readdirSync(folder).filter((f) => f.endsWith('.md')).sort()) {
    for (const p of practices(path.join(folder, file))) {
        if (only && !p.code.startsWith(only)) continue;
        const mobile = `capturas/${p.code}-celular.webp`;
        const desktop = `capturas/${p.code}-compu.webp`;
        if (!force && fs.existsSync(path.join(folder, mobile)) && fs.existsSync(path.join(folder, desktop))) {
            writeReferences(path.join(folder, file), p.code, mobile, desktop);
            skipped++;
            continue;
        }
        try {
            const html = (await render(p.solution)).replace(/\sloading="lazy"/g, '');
            pages.set(`/__captura/${p.code}.html`, html);
            const url = `http://127.0.0.1:${PORT}/__captura/${p.code}.html`;
            fs.writeFileSync(path.join(folder, mobile), await shot(url, 390, 844));
            fs.writeFileSync(path.join(folder, desktop), await shot(url, 1280, 800));
            writeReferences(path.join(folder, file), p.code, mobile, desktop);
            made++;
            console.log(`  ✓ ${p.code}`);
        } catch (e) {
            failed++;
            console.log(`  ✗ ${p.code}: ${e.message}`);
        }
    }
}

browser.close();
chrome.kill();
await new Promise((r) => (chrome.exitCode !== null ? r() : chrome.once('exit', r)));
server.close();
try {
    fs.rmSync(profile, { recursive: true, force: true });
} catch {
    // Chrome a veces termina de escribir su perfil después de cerrarse: queda en la carpeta temporal.
}
console.log(`Listo: ${made} nuevas, ${skipped} ya estaban${failed ? `, ${failed} con error` : ''}.`);
process.exit(failed ? 1 : 0);
