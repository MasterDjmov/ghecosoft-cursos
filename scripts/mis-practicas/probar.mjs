// Prueba de Bajar y Mis prácticas (D124), en Chrome sin ventana y contra la plataforma local:
//   php artisan serve --port=8123   (con los assets compilados)
//   node scripts/mis-practicas/probar.mjs [carpeta-para-capturas]
// Entra como admin, escribe en Practicar Python, baja el archivo, guarda, cambia el nombre, edita y vuelve a guardar,
// y la encuentra en Mis prácticas. Al final borra la práctica de prueba.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import WebSocket from 'ws';

const BASE = process.env.BASE ?? 'http://127.0.0.1:8123';
const SHOTS = process.argv[2] ?? null;
const profile = fs.mkdtempSync(path.join(process.env.TMPDIR ?? '/tmp', 'mispracticas-'));
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



const downloads = fs.mkdtempSync(path.join(process.env.TMPDIR ?? '/tmp', 'bajadas-'));
await send('Browser.setDownloadBehavior', { behavior: 'allow', downloadPath: downloads });
const runner = 'Alpine.$data(document.querySelector("[data-test=practice-tool]"))';
const setCode = (text) => js(`${runner}.editor.setDoc(${JSON.stringify(text)})`);
const getCode = () => js(`${runner}.code`);
const ready = 'typeof Alpine !== "undefined" && !!Alpine.$data(document.querySelector("[data-test=practice-tool]"))?.editor';

try {
    await go('/login');
    await js(`(() => { const set = (s, v) => { const f = document.querySelector(s); f.value = v; f.dispatchEvent(new Event('input', { bubbles: true })); }; set('input[name=username], input[type=text], input[name=email]', 'admin'); set('input[type=password]', 'admin123'); document.querySelector('form button[type=submit]').click(); })()`);
    await until('!location.pathname.includes("login")');
    await go('/herramientas/practicar/python');
    await until(ready);
    await setCode('print("prueba de mis prácticas")\n');
    await sleep(300);
    await js('document.querySelector("[data-test=code-download]").click()');
    await sleep(1500);
    const files = fs.readdirSync(downloads);
    check('Bajar deja practica.py', files, ['practica.py']);
    check('el archivo tiene lo escrito', files.length ? fs.readFileSync(path.join(downloads, files[0]), 'utf8') : '', 'print("prueba de mis prácticas")\n');
    await shot('1-practicar');

    await js('document.querySelector("[data-test=practice-save]").click()');
    await until('location.search.includes("practica=")', 10000);
    await until('!!document.querySelector("[data-test=saved-practice-header]") && ' + ready);
    const id = await js('new URLSearchParams(location.search).get("practica")');
    check('abre la guardada con su código', await getCode(), 'print("prueba de mis prácticas")\n');
    await js(`(() => { const i = document.querySelector('[data-test=saved-practice-title] input') ?? document.querySelector('[data-test=saved-practice-title]'); i.value = 'Prueba automática'; i.dispatchEvent(new Event('input', { bubbles: true })); i.dispatchEvent(new Event('blur', { bubbles: true })); i.dispatchEvent(new Event('change', { bubbles: true })); })()`);
    await sleep(800);
    await setCode('print("cambiado")\n');
    await sleep(300);
    check('marca los cambios sin guardar', await js('!!document.querySelector("[data-test=unsaved-dot]")?.offsetParent'));
    await js('document.querySelector("[data-test=practice-save]").click()');
    await sleep(1200);
    check('al guardar se va la marca', await js('!document.querySelector("[data-test=unsaved-dot]")?.offsetParent'));
    await shot('2-guardada');

    await go('/herramientas/mis-practicas');
    check('aparece en Mis prácticas con su nombre', await js(`!!document.querySelector('[data-test=saved-practice-${id}]')?.textContent.includes('Prueba automática')`));
    await shot('3-mis-practicas');
    await go(`/herramientas/practicar/python?practica=${id}`);
    await until(ready);
    check('al volver trae lo último guardado', await getCode(), 'print("cambiado")\n');

    await go('/herramientas/mis-practicas');
    await js(`window.confirm = () => true; document.querySelector('[data-test=saved-practice-${id}] [data-test=saved-practice-delete]').click()`);
    await sleep(1200);
    check('se borra', await js(`!document.querySelector('[data-test=saved-practice-${id}]')`));
    check('sin errores de JavaScript', errors, []);
} finally {
    browser.close();
    chrome.kill();
    try { fs.rmSync(profile, { recursive: true, force: true }); fs.rmSync(downloads, { recursive: true, force: true }); } catch {}
}
process.exit(fails ? 1 : 0);
