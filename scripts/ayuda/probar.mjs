// Prueba de aceptación de «Necesito ayuda» (D123), en Chrome sin ventana y contra la plataforma local:
//   php artisan serve --port=8123   (con los assets compilados)
//   NODE_URL=/cursos/python/nodos/1 node scripts/ayuda/probar.mjs [carpeta-para-capturas]
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import WebSocket from 'ws';

const BASE = process.env.BASE ?? 'http://127.0.0.1:8123';
const SHOTS = process.argv[2] ?? null;
const profile = fs.mkdtempSync(path.join(process.env.TMPDIR ?? '/tmp', 'ayuda-'));
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

try {
    await go('/login');
    await js(`(() => { const set = (s, v) => { const f = document.querySelector(s); f.value = v; f.dispatchEvent(new Event('input', { bubbles: true })); }; set('input[name=username], input[type=text], input[name=email]', 'admin'); set('input[type=password]', 'admin123'); document.querySelector('form button[type=submit]').click(); })()`);
    await until('!location.pathname.includes("login")');
    await go(process.env.NODE_URL);
    await until('document.querySelector("[data-test=step-help]")?._x_dataStack?.length > 0');
    const help = '[...document.querySelectorAll("[data-test=step-help]")].find((e) => e.offsetParent)';
    check('el botón de escuchar está', await js('!!document.querySelector("[data-test=step-read]")'));
    check('el panel arranca cerrado', await js(`${help}.querySelector("[data-test=step-help-panel]").offsetParent === null`));
    await js(`${help}.querySelector("[data-test=step-help-toggle]").click()`);
    await sleep(300);
    check('se abre el panel', await js(`${help}.querySelector("[data-test=step-help-panel]").offsetParent !== null`));
    await js(`${help}.scrollIntoView({ block: 'start' })`);
    await shot('1-panel');
    // ¿Dónde toco?
    await js(`[...${help}.querySelectorAll("[data-test=step-help-where] button")][0].click()`);
    await until('document.querySelectorAll(".cm-help-line").length > 0');
    check('marca renglones en el editor', await js('document.querySelectorAll(".cm-help-line").length'), 1);
    check('dice cuáles', await js(`${help}.querySelector("[data-test=step-help-where-text]").textContent.includes("renglón 1")`));
    // Comparemos: antes de ejecutar, el aviso
    check('comparar pide ejecutar primero', await js(`${help}.querySelector("[data-test=step-help-compare]").textContent.includes("Ejecutá tu programa")`));
    // Ejecutar algo mal
    await js(`(() => { const v = document.querySelector(".cm-editor").cmView?.view; return true; })()`);
    await js(`(() => { const root = document.querySelector("[data-test=step-current]"); const data = Alpine.$data(root.querySelector("[x-data^=codeRunner]")); data.editor.setDoc('print("Me llamo Mia y vengo de lejos.")'); data.run(); })()`);
    await until(`(() => { const d = Alpine.$data(document.querySelector("[data-test=step-current] [x-data^=codeRunner]")); return d.running === false && d.matches === false; })()`, 90000);
    await sleep(300);
    check('ahora se puede comparar', await js(`[...${help}.querySelectorAll("[data-test=step-help-compare] button")].some((b) => b.offsetParent)`));
    await js(`[...${help}.querySelectorAll("[data-test=step-help-compare] button")].find((b) => b.offsetParent).click()`);
    await sleep(300);
    check('la tabla compara las dos salidas', await js(`${help}.querySelector("[data-test=step-help-compare] table").innerText.includes("muy·lejos")`));
    await js(`${help}.querySelector('[data-test=step-help-compare]').scrollIntoView({ block: 'center' })`);
    await shot('2-comparar');
    // Mostrame una línea (staff: sin fallos previos)
    await js(`${help}.querySelector("[data-test=step-help-line-button]").click()`);
    await until(`${help}.querySelector("[data-test=step-help-solution]").offsetParent !== null`);
    check('con una sola línea que cambia, la solución completa', await js(`${help}.querySelector("[data-test=step-help-solution] pre").textContent`), 'print("Me llamo Mia y vengo de muy lejos.")');
    await js(`${help}.querySelector('[data-test=step-help-line]').scrollIntoView({ block: 'center' })`);
    await shot('3-linea');
    check('sin errores de JavaScript', errors, []);
} catch (e) {
    console.error(e);
    fails++;
} finally {
    browser.close();
    chrome.kill();
    process.exit(fails ? 1 : 0);
}
