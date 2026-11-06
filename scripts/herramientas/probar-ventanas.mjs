// Prueba de aceptación de las ventanas de Herramientas (D120), en Chrome sin ventana y contra la plataforma local:
//   php artisan serve --port=8123   (con los assets compilados)
//   node scripts/herramientas/probar-ventanas.mjs [carpeta-para-capturas]
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import WebSocket from 'ws';

const BASE = process.env.BASE ?? 'http://127.0.0.1:8123';
const SHOTS = process.argv[2] ?? null;
const profile = fs.mkdtempSync(path.join(process.env.TMPDIR ?? '/tmp', 'ventanas-'));
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

const boxes = 'document.querySelectorAll("[data-test=tool-window]")';
const count = () => js(`${boxes}.length`);
const frameDoc = (n) => `${boxes}[${n}].querySelector("iframe").contentDocument`;
const frameReady = (n, test) => until(`${frameDoc(n)}?.querySelector("[data-test=${test}]")?._x_dataStack?.length > 0`);
const inFrame = (n, selector) => `${frameDoc(n)}.querySelector(${JSON.stringify(selector)})`;
const clickIn = (n, selector) => js(`${inFrame(n, selector)}.click()`);
const textIn = (n, selector) => js(`${inFrame(n, selector)}.textContent.trim()`);
const type = async (n, text) => {
    await js(`(() => { const f = ${inFrame(n, '[data-test=calc-input]')}; f.value = ${JSON.stringify(text)}; f.dispatchEvent(new Event('input', { bubbles: true })); })()`);
    await sleep(60);
};
const calcValue = (n) => js(`${inFrame(n, '[data-test=calc-input]')}.value`);
const key = (n, name) => js(`${inFrame(n, '[data-test=calc-input]')}.dispatchEvent(new KeyboardEvent('keydown', { key: ${JSON.stringify(name)}, bubbles: true, cancelable: true }))`);
const buttonIn = (n, keys, label) => js(`[...${inFrame(n, `[data-test=${keys}]`)}.querySelectorAll('button')].find((b) => b.textContent.trim() === ${JSON.stringify(label)}).click()`);
const barButton = (n, label) => js(`${boxes}[${n}].querySelector('button[aria-label="${label}"]')?.click() ?? 'none'`);
const zOf = (n) => js(`Number(${boxes}[${n}].style.zIndex)`);

try {
    // Entrar
    await go('/login');
    await js(`(() => { const set = (s, v) => { const f = document.querySelector(s); f.value = v; f.dispatchEvent(new Event('input', { bubbles: true })); }; set('input[name=username], input[type=text], input[name=email]', 'admin'); set('input[type=password]', 'admin123'); document.querySelector('form button[type=submit]').click(); })()`);
    await until('!location.pathname.includes("login")');
    await go('/mundos');

    // Abrir: el menú trae la que está, el + abre otra, hasta el tope
    await js('document.querySelector("[data-test=menu-calculator]").click()');
    check('el menú abre una calculadora', await count(), 1);
    await js('document.querySelector("[data-test=menu-calculator]").click()');
    check('el menú otra vez no abre otra', await count(), 1);
    const plus = 'document.querySelector("[data-test=menu-calculator]").closest(".group").querySelector("[data-tool-new]")';
    await js(`${plus}.click()`);
    await js(`${plus}.click()`);
    await js(`${plus}.click()`);
    check('hasta 3 calculadoras', await count(), 3);
    check('numeradas', await js(`[...${boxes}].map((b) => b.getAttribute('aria-label'))`), ['Calculadora', 'Calculadora 2', 'Calculadora 3']);
    await js('document.querySelector("[data-test=menu-ascii]").click()');
    check('más la tabla', await count(), 4);
    await js('document.querySelector("[data-test=menu-c]").closest(".group").querySelector("[data-tool-window]").click()');
    check('y una de práctica, sin reemplazar a las otras', await count(), 5);
    await frameReady(0, 'calculator-tool');
    await frameReady(1, 'calculator-tool');
    await frameReady(3, 'ascii-tool');

    // Siempre arriba y solo con la cruz
    check('la calculadora no tiene «Abrir como página»', await js(`${boxes}[0].querySelector('button[aria-label="Abrir como página"]') === null`));
    check('la de práctica sí', await js(`${boxes}[4].querySelector('button[aria-label="Abrir como página"]') !== null`));
    check('la última abierta va adelante', (await zOf(4)) > (await zOf(0)));
    const bar0 = await js(`(() => { const r = ${boxes}[0].querySelector('span').getBoundingClientRect(); return { x: r.x + 5, y: r.y + 5 }; })()`);
    await js(`${boxes}[0].dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, cancelable: true }))`);
    check('tocarla la trae adelante', (await zOf(0)) > (await zOf(4)));
    await js(`${frameDoc(3)}.defaultView.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))`);
    check('tocar adentro también', (await zOf(3)) > (await zOf(0)));
    check('por encima de la página', (await zOf(0)) >= 1000);

    // Moverla
    await js(`${boxes}[0].dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))`);
    const before = await js(`${boxes}[0].getBoundingClientRect().x`);
    await page('Input.dispatchMouseEvent', { type: 'mousePressed', x: bar0.x, y: bar0.y, button: 'left', buttons: 1, clickCount: 1 });
    await page('Input.dispatchMouseEvent', { type: 'mouseMoved', x: bar0.x - 150, y: bar0.y - 40, button: 'left', buttons: 1 });
    await page('Input.dispatchMouseEvent', { type: 'mouseReleased', x: bar0.x - 150, y: bar0.y - 40, button: 'left', buttons: 0, clickCount: 1 });
    check('se mueve arrastrando la barra', Math.round((await js(`${boxes}[0].getBoundingClientRect().x`)) - before), -150);

    // Calculadora simple
    await type(0, '2+3×4');
    await key(0, 'Enter');
    await sleep(60);
    check('2+3×4 = 14', await calcValue(0), '14');
    await key(0, 'Escape');
    await sleep(60);
    check('Esc borra y no cierra', [await calcValue(0), await count()], ['', 5]);
    await type(0, '0,1+0,2');
    await js(`${inFrame(0, '[data-test=calc-equals]')}.click()`);
    await sleep(60);
    check('0,1+0,2 = 0,3', await calcValue(0), '0,3');
    await buttonIn(0, 'calc-keys-simple', '+');
    await buttonIn(0, 'calc-keys-simple', '1');
    await js(`${inFrame(0, '[data-test=calc-equals]')}.click()`);
    await sleep(60);
    check('un operador sigue desde el resultado', await calcValue(0), '1,3');
    await buttonIn(0, 'calc-keys-simple', '7');
    await sleep(60);
    check('un número empieza una cuenta nueva', await calcValue(0), '7');
    await type(0, '1/0');
    await js(`${inFrame(0, '[data-test=calc-equals]')}.click()`);
    await sleep(60);
    check('dividir por cero avisa', await textIn(0, '[data-test=calc-error]'), 'No se puede dividir por cero.');
    await type(0, '123');
    await js(`${inFrame(0, '[data-test=calc-equals]')}.click()`);
    await sleep(60);
    check('cada ventana tiene lo suyo', await calcValue(1), '');

    // Programador
    await clickIn(1, '[data-test=calc-programmer]');
    await sleep(100);
    await clickIn(1, '[data-test=calc-base-16]');
    await clickIn(1, '[data-test=calc-width-8]');
    await sleep(60);
    await type(1, 'FF');
    await sleep(60);
    check('FF en las cuatro bases', [await textIn(1, '[data-test=calc-value-16]'), await textIn(1, '[data-test=calc-value-10]'), await textIn(1, '[data-test=calc-value-8]'), await textIn(1, '[data-test=calc-value-2]')], ['FF', '255', '377', '1111 1111']);
    check('con signo', await textIn(1, '[data-test=calc-signed]'), '−1');
    await clickIn(1, '[data-test=calc-bit-7]');
    await sleep(60);
    check('tocar un bit lo cambia', await calcValue(1), '7F');
    await clickIn(1, '[data-test=calc-twos]');
    await sleep(60);
    check('complemento a dos', await calcValue(1), '81');
    await type(1, '41');
    await sleep(60);
    check('muestra el carácter', await textIn(1, '[data-test=calc-char]'), 'A');
    await clickIn(1, '[data-test=calc-base-2]');
    await sleep(60);
    check('cambiar de base convierte', await calcValue(1), '1000001');
    check('en binario no se puede tocar el 7', await js(`[...${inFrame(1, '[data-test=calc-keys-programmer]')}.querySelectorAll('button')].find((b) => b.textContent.trim() === '7').disabled`));
    await clickIn(1, '[data-test=calc-base-10]');
    await sleep(40);
    await type(1, '256');
    await sleep(60);
    check('avisa si no entra', await js(`${inFrame(1, '[data-test=calc-overflow]')}.style.display !== 'none'`));
    await clickIn(1, '[data-test=calc-width-64]');
    await sleep(60);
    check('64 bits: 4 filas', await js(`${inFrame(1, '[data-test=calc-bit-63]')} !== null && ${inFrame(1, '[data-test=calc-bit-0]')} !== null`));
    await type(1, '-1');
    await sleep(60);
    check('64 bits exactos', await textIn(1, '[data-test=calc-value-16]'), 'FFFFFFFFFFFFFFFF');
    await type(1, '10+');
    await sleep(60);
    await js(`${inFrame(1, '[data-test=calc-equals-programmer]')}.click()`);
    await sleep(60);
    check('la cuenta sin terminar avisa', await textIn(1, '[data-test=calc-error]'), 'La cuenta quedó sin terminar.');

    // Tabla
    await clickIn(3, '[data-test=ascii-ascii-65]');
    await sleep(150);
    check('tocar A la copia', await textIn(3, '[data-test=ascii-copied]'), 'Copiado: A');
    await page('Page.bringToFront');
    await js(`${boxes}[3].querySelector("iframe").focus()`);
    const clip = await js(`${frameDoc(3)}.defaultView.navigator.clipboard.readText().catch((e) => 'ERROR ' + e.message)`);
    check('quedó en el portapapeles', clip, 'A');
    await clickIn(3, '[data-test=ascii-ascii-10]');
    await sleep(150);
    check('el salto de línea se copia como \\n', await textIn(3, '[data-test=ascii-copied]'), 'Copiado: \\n');
    await js(`(() => { const s = ${inFrame(3, '[data-test=ascii-copy-as]')}; s.value = 'hex'; s.dispatchEvent(new Event('change', { bubbles: true })); })()`);
    await sleep(60);
    await clickIn(3, '[data-test=ascii-ascii-65]');
    await sleep(150);
    check('copiar en HEX', await textIn(3, '[data-test=ascii-copied]'), 'Copiado: 0x41');
    await js(`(() => { const s = ${inFrame(3, '[data-test=ascii-copy-as]')}; s.value = 'symbol'; s.dispatchEvent(new Event('change', { bubbles: true })); })()`);
    await sleep(60);
    await clickIn(3, '[data-test=ascii-tab-windows]');
    await sleep(120);
    check('Windows: ñ es 164', await textIn(3, '[data-test=ascii-windows-164] span'), 'ñ');
    await clickIn(3, '[data-test=ascii-tab-unicode]');
    await sleep(200);
    check('Unicode: ñ es 241', await textIn(3, '[data-test=ascii-unicode-241] span'), 'ñ');
    await clickIn(3, '[data-test=ascii-tab-dos]');
    await sleep(120);
    check('DOS: 184 es ╕', await textIn(3, '[data-test=ascii-dos-184] span'), '╕');
    await js(`(() => { const s = ${inFrame(3, '[data-test=ascii-search]')}; s.value = 'ñ'; s.dispatchEvent(new Event('input', { bubbles: true })); })()`);
    await sleep(150);
    check('buscar ñ la muestra en las tres', await js(`${frameDoc(3)}.querySelectorAll('[data-test^="ascii-windows-"], [data-test^="ascii-dos-"], [data-test^="ascii-unicode-"]').length`), 3);
    await js(`(() => { const s = ${inFrame(3, '[data-test=ascii-search]')}; s.value = ''; s.dispatchEvent(new Event('input', { bubbles: true })); })()`);
    await clickIn(3, '[data-test=ascii-tab-ascii]');
    await sleep(150);

    // Achicar y seguir navegando sin perder nada
    await barButton(2, 'Achicar');
    check('achicada queda solo la barra', await js(`${boxes}[2].getBoundingClientRect().height`), 44);
    await js(`${frameDoc(0)}.defaultView.__marca = 'sigue';`);
    await js(`window.Livewire.navigate('/mochila')`);
    await until('location.pathname === "/mochila"');
    await sleep(700);
    check('al navegar siguen las 5', await count(), 5);
    check('sin recargarse', await js(`${frameDoc(0)}.defaultView.__marca`), 'sigue');
    await shot('todas');

    // Recargar: se recuerdan, con lo que tenían (vuelven en el orden en que estaban adelante)
    await go('/mundos');
    await until(`${boxes}.length === 5`);
    const named = (label) => js(`[...${boxes}].findIndex((b) => b.getAttribute('aria-label') === ${JSON.stringify(label)})`);
    const first = await named('Calculadora');
    await frameReady(first, 'calculator-tool');
    await sleep(300);
    check('al recargar se recuerda lo escrito', await calcValue(first), '123');
    check('y la achicada sigue achicada', await js(`${boxes}[${await named('Calculadora 3')}].getBoundingClientRect().height`), 44);

    // Cerrar con la cruz
    const key0 = await js(`Object.keys(localStorage).filter((k) => k.startsWith('tool-instance:')).length`);
    await barButton(first, 'Cerrar');
    check('la cruz la cierra', await count(), 4);
    check('y olvida lo suyo', await js(`Object.keys(localStorage).filter((k) => k.startsWith('tool-instance:')).length`), key0 - 1);
    await js(`${plus}.click()`);
    await sleep(100);
    check('la nueva toma el número libre', await named('Calculadora') >= 0);

    if (SHOTS) {
        // Capturas: cada una suelta y como página, de compu y de celular
        for (const n of [...Array(await count()).keys()].reverse()) await barButton(n, 'Cerrar');
        await js(`${plus}.click()`);
        await frameReady(0, 'calculator-tool');
        await shot('calc-simple');
        await clickIn(0, '[data-test=calc-programmer]');
        await sleep(100);
        await clickIn(0, '[data-test=calc-base-16]');
        await type(0, '41');
        await shot('calc-programador');
        await clickIn(0, '[data-test=calc-width-64]');
        await shot('calc-64');
        await barButton(0, 'Cerrar');
        await js('document.querySelector("[data-test=menu-ascii]").click()');
        await frameReady(0, 'ascii-tool');
        await clickIn(0, '[data-test=ascii-ascii-65]');
        await shot('ascii');
        await clickIn(0, '[data-test=ascii-tab-windows]');
        await js(`${inFrame(0, '[data-test=ascii-help]')}.open = true`);
        await shot('ascii-windows');
        await clickIn(0, '[data-test=ascii-tab-unicode]');
        await js(`${inFrame(0, '[data-test=ascii-help]')}.open = true`);
        await shot('ascii-unicode');
        await barButton(0, 'Cerrar');
        await go('/herramientas/tabla-ascii');
        await shot('ascii-pagina');
        await go('/herramientas/calculadora');
        await shot('calc-pagina');
        await page('Emulation.setDeviceMetricsOverride', { width: 390, height: 800, deviceScaleFactor: 1, mobile: true });
        await go('/mundos');
        await js('document.querySelector("[data-test=menu-calculator]").click()');
        await frameReady(0, 'calculator-tool');
        await shot('celular-calc');
        await barButton(0, 'Achicar');
        await js('document.querySelector("[data-test=menu-ascii]").click()');
        await frameReady(1, 'ascii-tool');
        await shot('celular-ascii');
    }

    check('sin errores de JavaScript', errors, []);
} catch (e) {
    fails++;
    console.log(`✗ ${e.message}`);
} finally {
    browser.close();
    chrome.kill();
    await sleep(500);
    fs.rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
}

console.log(fails ? `\n${fails} fallaron` : '\nTodo bien.');
process.exit(fails ? 1 : 0);
