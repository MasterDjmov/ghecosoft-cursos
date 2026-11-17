// Prueba de TypeScript en Chrome sin ventana (D115, fase 5), contra la plataforma local:
//   php artisan serve --port=8123   (con los assets compilados y node scripts/build-typescript-toolchain.mjs)
//   node scripts/ts-micro/probar-navegador.mjs
// Usa los ejemplos de TypeScript de Herramientas → La caja de la Feria: uno que compila y corre en la caja, y otro
// con dos errores de tipos (que no se ejecuta y explica cada error con su línea).
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import WebSocket from 'ws';

const BASE = process.env.BASE ?? 'http://127.0.0.1:8123';
const profile = fs.mkdtempSync(path.join(process.env.TMPDIR ?? '/tmp', 'ts-'));
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
await page('Runtime.enable');
const errors = [];
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
        await sleep(150);
    }
    throw new Error(`No se cumplió: ${expression}`);
};
let fails = 0;
const check = (name, ok, detail = '') => {
    if (!ok) fails++;
    console.log(`${ok ? '✓' : '✗'} ${name}${ok ? '' : `\n    ${detail}`}`);
};
const runner = (key) => `Alpine.$data([...document.querySelectorAll('[data-test=js-tool]')].find((e) => e.closest('section') && e.closest('section').querySelector('[x-data]') && e.closest('section').getAttribute('x-show')?.includes("'${key}'")))`;

try {
    await page('Page.navigate', { url: `${BASE}/login` });
    await until('document.readyState === "complete"');
    await sleep(500);
    await js(`(() => { const set = (s, v) => { const f = document.querySelector(s); f.value = v; f.dispatchEvent(new Event('input', { bubbles: true })); }; set('input[name=username], input[type=text], input[name=email]', 'admin'); set('input[type=password]', 'admin123'); document.querySelector('form button[type=submit]').click(); })()`);
    await until('!location.pathname.includes("login")');
    await page('Page.navigate', { url: `${BASE}/herramientas/caja-de-la-feria` });
    await until('document.readyState === "complete" && window.Alpine');
    await sleep(800);

    // 1. El que compila: corre en la caja.
    const started = Date.now();
    await js(`${runner('tipos')}.run()`);
    await until(`${runner('tipos')}.running === false && ${runner('tipos')}.output !== ''`, 90000);
    const ok = await js(`${runner('tipos')}.output`);
    console.log(`  (primera vez, bajando el compilador: ${Date.now() - started} ms)`);
    check('el ejemplo bien tipado se ejecuta', ok.includes('Nivel 1: 2 piezas, 16 mm en total') && ok.includes('lente Rigel'), ok);
    check('sin error', (await js(`${runner('tipos')}.error`)) === false);

    // 2. El mismo, con un texto donde va un número: no se ejecuta.
    await js(`${runner('tipos')}.editor.setDoc(${runner('tipos')}.code.replace('let nivel: number = 1;', 'let nivel: number = "cinco";'))`);
    await sleep(200);
    const again = Date.now();
    await js(`${runner('tipos')}.run()`);
    await until(`${runner('tipos')}.running === false`, 30000);
    const bad = await js(`${runner('tipos')}.output`);
    console.log(`  (segunda vez, con el compilador en memoria: ${Date.now() - again} ms)`);
    check('TS2322 en la línea 16, en español y sin ejecutar', bad.includes('Línea 16') && bad.includes('TS2322') && bad.includes("no se puede asignar al tipo 'number'") && !bad.includes('Nivel'), bad);
    check('marca el error', (await js(`${runner('tipos')}.error`)) === true);

    // 3. Un error al ejecutar: la línea es la del TypeScript (no la del JavaScript que sale, que no tiene los tipos).
    await js(`${runner('tipos')}.editor.setDoc('interface Gema {\\n  valor: number;\\n}\\n\\ntype Forma = "luna" | "sol";\\n\\nconst gemas: Gema[] = [];\\nconsole.log(gemas[0].valor);\\n')`);
    await sleep(200);
    await js(`${runner('tipos')}.run()`);
    await until(`${runner('tipos')}.running === false`, 30000);
    const runtime = await js(`${runner('tipos')}.output`);
    check('el error al ejecutar dice la línea del TypeScript (8)', runtime.includes('línea 8') && runtime.includes('valor'), runtime);

    // 4. El de los dos errores.
    await js(`${runner('mirador')}.run()`);
    await until(`${runner('mirador')}.running === false && ${runner('mirador')}.output !== ''`, 30000);
    const two = await js(`${runner('mirador')}.output`);
    check('los dos errores, cada uno con su línea y su criatura', two.includes('2 piezas no encajan') && two.includes('Línea 10') && two.includes('TS2345') && two.includes('Línea 12') && two.includes('TS18047') && two.includes('Orco'), two);
    console.log(`\n${two}\n`);
    // 5. JavaScript sigue igual (comparte jsRun con TypeScript).
    await js(`${runner('consola')}.run()`);
    await until(`${runner('consola')}.running === false && ${runner('consola')}.output !== ''`, 30000);
    const plain = await js(`${runner('consola')}.output`);
    check('JavaScript sigue andando', plain.includes('Hola, Nima') && plain.includes('22 4'), plain);
    check('sin errores de JavaScript en la página', errors.length === 0, errors.join('\n'));
} catch (e) {
    console.error(e);
    fails++;
} finally {
    browser.close();
    chrome.kill();
    process.exit(fails ? 1 : 0);
}
