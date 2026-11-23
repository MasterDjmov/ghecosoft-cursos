// Prueba del menú lateral plegable, en Chrome sin ventana y contra la plataforma local:
//   php artisan serve --port=8123   (con los assets compilados)
//   node scripts/menu/probar.mjs [carpeta-para-capturas]
// Entra como admin y como alumno (cliente), pliega el menú, revisa que queden los íconos y que se recuerde al recargar.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import WebSocket from 'ws';

const BASE = process.env.BASE ?? 'http://127.0.0.1:8123';
const SHOTS = process.argv[2] ?? null;
const profile = fs.mkdtempSync(path.join(process.env.TMPDIR ?? '/tmp', 'menu-'));
const chrome = spawn(process.env.CHROME ?? '/usr/bin/google-chrome', ['--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`, '--no-first-run', '--window-size=1400,950', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
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
await page('Page.enable');
await send('Browser.grantPermissions', { origin: BASE, permissions: ['clipboardReadWrite', 'clipboardSanitizedWrite'] });

const errors = [];
await page('Runtime.enable');
browser.on('message', (m) => {
    const d = JSON.parse(m);
    if (d.method === 'Runtime.exceptionThrown') errors.push(d.params.exceptionDetails.exception?.description ?? d.params.exceptionDetails.text);
});

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const js = async (expression) => {
    const answer = await page('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (answer.result?.exceptionDetails) throw new Error(`${expression}\n${answer.result.exceptionDetails.exception?.description}`);
    return answer.result.result?.value;
};
const until = async (expression, ms = 15000) => {
    const end = Date.now() + ms;
    while (Date.now() < end) {
        if (await js(expression).catch(() => false)) return;
        await sleep(100);
    }
    throw new Error(`No se cumplió: ${expression}`);
};
const go = async (url) => {
    await page('Page.navigate', { url: BASE + url });
    await sleep(300);
    await until('document.readyState === "complete"');
    await sleep(500);
};
const shot = async (name) => {
    if (!SHOTS) return;
    await sleep(250);
    const { result } = await page('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(SHOTS, `${name}.png`), Buffer.from(result.data, 'base64'));
};


let fails = 0;
const check = (name, got, want = true) => {
    const ok = JSON.stringify(got) === JSON.stringify(want);
    if (!ok) fails++;
    console.log(`${ok ? '✓' : '✗'} ${name}${ok ? '' : `: dio ${JSON.stringify(got)}, se esperaba ${JSON.stringify(want)}`}`);
};


const login = async (user, pass) => {
    await go('/login');
    await js(`(() => { const set = (s, v) => { const f = document.querySelector(s); f.value = v; f.dispatchEvent(new Event('input', { bubbles: true })); }; set('input[name=username], input[type=text], input[name=email]', '${user}'); set('input[type=password]', '${pass}'); document.querySelector('form button[type=submit]').click(); })()`);
    await until('!location.pathname.includes("login")');
};
const sidebar = 'document.querySelector("ui-sidebar")';
const visibleItems = `[...${sidebar}.querySelectorAll("[data-flux-sidebar-item]")].filter((e) => e.offsetParent).length`;

try {
    for (const [user, pass] of [['admin', 'admin123'], ['cliente', 'cliente123']]) {
        await login(user, pass);
        await go('/');
        await js('localStorage.removeItem("flux-sidebar-collapsed-desktop")');
        await go('/');
        const open = await js(`${sidebar}.getBoundingClientRect().width`);
        const items = await js(visibleItems);
        check(`${user}: abierto mide 256 px`, open, 256);
        await shot(`${user}-abierto`);
        await js(`${sidebar}.querySelector("[data-flux-sidebar-collapse] button").click()`);
        await sleep(400);
        check(`${user}: plegado mide 56 px`, await js(`${sidebar}.getBoundingClientRect().width`), 56);
        check(`${user}: plegado quedan los mismos íconos`, await js(visibleItems), items);
        check(`${user}: plegado no se ven los títulos de los grupos`, await js(`[...${sidebar}.querySelectorAll("[data-flux-sidebar-group] > .truncate")].some((e) => e.offsetParent)`), false);
        await shot(`${user}-plegado`);
        await go('/');
        check(`${user}: al recargar sigue plegado`, await js(`${sidebar}.getBoundingClientRect().width`), 56);
        await js('localStorage.removeItem("flux-sidebar-collapsed-desktop")');
        await go('/logout').catch(() => {});
        await js('document.querySelector("form[action$=logout] button")?.click()').catch(() => {});
        await page('Network.clearBrowserCookies').catch(() => {});
        await send('Storage.clearCookies', {});
    }
    check('sin errores de JavaScript', errors, []);
} finally {
    browser.close();
    chrome.kill();
    try { fs.rmSync(profile, { recursive: true, force: true }); } catch {}
}
process.exit(fails ? 1 : 0);
