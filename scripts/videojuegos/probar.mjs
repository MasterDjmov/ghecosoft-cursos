// Prueba del prototipo de juegos con SDL3 (D126, fase 1), en Chrome sin ventana y contra la plataforma local:
//   php artisan serve --port=8123   (con los assets compilados)
//   node scripts/videojuegos/probar.mjs [carpeta-para-capturas]
// Entra como admin a Herramientas → Juegos con SDL3, compila el Pong, mira el menú, juega con el teclado (la pelota se
// mueve, la paleta sube con W) y con un joystick simulado (la cruz baja la paleta), lo cierra, y prueba que un error
// de compilación se muestre y que un bucle sin pausas (el Bucle Eterno) se corte solo.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import WebSocket from 'ws';

const BASE = process.env.BASE ?? 'http://127.0.0.1:8123';
const SHOTS = process.argv[2] ?? null;
const profile = fs.mkdtempSync(path.join(process.env.TMPDIR ?? '/tmp', 'videojuegos-'));
const chrome = spawn(process.env.CHROME ?? '/usr/bin/google-chrome', ['--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`, '--no-first-run', '--window-size=1400,1100', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
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
        await sleep(150);
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
    const { result } = await page('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(SHOTS, `${name}.png`), Buffer.from(result.data, 'base64'));
};

let fails = 0;
const check = (name, got, want = true) => {
    const ok = JSON.stringify(got) === JSON.stringify(want);
    if (!ok) fails++;
    console.log(`${ok ? '✓' : '✗'} ${name}${ok ? '' : `: dio ${JSON.stringify(got)}, se esperaba ${JSON.stringify(want)}`}`);
};

const runner = 'Alpine.$data(document.querySelector("[data-test=game-tool]"))';

/**
 * Lo que se ve en el lienzo del juego (una captura de la pantalla, recortada): dónde hay amarillo (la pelota o los
 * títulos) y dónde está lo blanco de la franja izquierda (la paleta del jugador 1), en píxeles del juego (640 × 480).
 */
async function look() {
    const rect = await js('(() => { const r = document.querySelector("[data-test=game-canvas]").getBoundingClientRect(); return { x: r.x, y: r.y + scrollY, w: r.width, h: r.height }; })()');
    await js(`scrollTo(0, ${Math.max(0, rect.y - 40)})`);
    await sleep(100);
    // El recorte va en coordenadas del documento (no de lo que se ve).
    const answer = await page('Page.captureScreenshot', { format: 'png', clip: { x: rect.x, y: rect.y, width: rect.w, height: rect.h, scale: 640 / rect.w } });
    if (!answer.result) throw new Error(`No se pudo capturar el juego: ${JSON.stringify(answer.error)}`);
    const { result } = answer;
    return js(`(async () => {
        const image = new Image();
        image.src = 'data:image/png;base64,${result.data}';
        await image.decode();
        const c = new OffscreenCanvas(640, 480);
        const g = c.getContext('2d');
        g.drawImage(image, 0, 0, 640, 480);
        const px = g.getImageData(0, 0, 640, 480).data;
        const box = (test, x0, x1) => {
            let b = null;
            for (let y = 0; y < 480; y++) for (let x = x0; x < x1; x++) {
                const i = (y * 640 + x) * 4;
                if (test(px[i], px[i + 1], px[i + 2])) b = b ? { x0: Math.min(b.x0, x), y0: Math.min(b.y0, y), x1: Math.max(b.x1, x), y1: Math.max(b.y1, y) } : { x0: x, y0: y, x1: x, y1: y };
            }
            return b;
        };
        return {
            yellow: box((r, g, b) => r > 220 && g > 170 && g < 240 && b < 140, 0, 640),
            paddle: box((r, g, b) => r > 230 && g > 230 && b > 230, 0, 60),
        };
    })()`);
}

const key = async (code, type, text = '') => {
    const keyName = { KeyW: 'w', KeyS: 's', Digit1: '1', Digit2: '2', Numpad1: '1', Enter: 'Enter', Escape: 'Escape' }[code] ?? code;
    const vk = { KeyW: 87, KeyS: 83, Digit1: 49, Digit2: 50, Numpad1: 97, Enter: 13, Escape: 27 }[code];
    await page('Input.dispatchKeyEvent', { type, code, key: keyName, text: type === 'keyDown' ? text : undefined, windowsVirtualKeyCode: vk });
};

try {
    await go('/login');
    await until('document.querySelector("input[type=password]")');
    await js(`(() => { const set = (s, v) => { const f = document.querySelector(s); f.value = v; f.dispatchEvent(new Event('input', { bubbles: true })); }; set('input[name=username], input[type=text], input[name=email]', 'admin'); set('input[type=password]', 'admin123'); document.querySelector('form button[type=submit]').click(); })()`);
    await until('!location.pathname.includes("login")');

    await go('/herramientas/arcadia');
    await until(`${runner}?.editor`);
    check('el editor trae el Pong', await js(`${runner}.code.includes('La Cancha de las Paletas')`));
    check('el botón dice Jugar', await js('[...document.querySelectorAll("button")].some((b) => b.textContent.trim() === "Jugar")'));

    // Un joystick de mentira, para probar la cruz sin tener uno enchufado: arranca suelto.
    await js(`(() => {
        window.fakePad = { index: 0, id: 'Control de prueba (STANDARD GAMEPAD)', connected: true, mapping: 'standard', axes: [0, 0, 0, 0], buttons: Array.from({ length: 17 }, () => ({ pressed: false, value: 0 })) };
        navigator.getGamepads = () => [window.fakePad];
    })()`);

    const started = Date.now();
    await js(`void ${runner}.run()`);
    await until(`${runner}.gamePlaying || ${runner}.error`, 240000);
    console.log(`  (compilar y arrancar: ${((Date.now() - started) / 1000).toFixed(1)} s)`);
    check('el juego arrancó', await js(`${runner}.gamePlaying`));
    await until(`${runner}.gameTitle !== ''`, 5000).catch(() => {});
    check('la ventana se llama como en SDL_CreateWindow', await js(`${runner}.gameTitle`), 'La Cancha de las Paletas');
    check('ve el joystick', await js(`${runner}.gamePads`), 1);
    await sleep(800);
    let seen = await look();
    await shot('1-menu');
    check('el menú muestra el título en amarillo', Boolean(seen.yellow && seen.yellow.y0 > 100 && seen.yellow.y1 < 200));

    // Teclado: el 1 del teclado numérico (y el de arriba, y Enter) empieza contra la compu. Se hace clic en el juego,
    // como el alumno.
    await page('Input.dispatchMouseEvent', { type: 'mousePressed', x: 700, y: 300, button: 'left', clickCount: 1 });
    await page('Input.dispatchMouseEvent', { type: 'mouseReleased', x: 700, y: 300, button: 'left', clickCount: 1 });
    check('el clic deja el juego listo para el teclado', await js('document.activeElement?.dataset.test'), 'game-canvas');
    check('y abajo lo dice', await js(`${runner}.status`), '🎮 El teclado está en el juego (ESC vuelve al menú)');
    await key('Numpad1', 'keyDown', '1');
    await key('Numpad1', 'keyUp');
    await sleep(300);
    const a = await look();
    await sleep(300);
    const b = await look();
    await shot('2-jugando');
    check('hay una pelota chica', Boolean(a.yellow && a.yellow.x1 - a.yellow.x0 < 20));
    check('la pelota se mueve', Boolean(a.yellow && b.yellow && (a.yellow.x0 !== b.yellow.x0 || a.yellow.y0 !== b.yellow.y0)));

    const before = b.paddle;
    await key('KeyW', 'keyDown', 'w');
    await sleep(400);
    await key('KeyW', 'keyUp');
    const up = (await look()).paddle;
    check('con W la paleta sube', Boolean(before && up && up.y0 < before.y0 - 40));

    await js('fakePad.buttons[13] = { pressed: true, value: 1 }');
    await sleep(500);
    await js('fakePad.buttons[13] = { pressed: false, value: 0 }');
    const down = (await look()).paddle;
    check('con la cruz del joystick la paleta baja', Boolean(up && down && down.y0 > up.y0 + 40));

    // Escape vuelve al menú.
    await key('Escape', 'keyDown');
    await key('Escape', 'keyUp');
    await sleep(300);
    seen = await look();
    check('ESC vuelve al menú', Boolean(seen.yellow && seen.yellow.y0 > 100 && seen.yellow.y1 < 200));

    await js(`${runner}.gameStop()`);
    await until(`! ${runner}.gamePlaying`, 5000);
    check('Cerrar el juego le manda SDL_EVENT_QUIT y termina solo', await js(`${runner}.status`), 'El juego terminó (devolvió 0).');

    // Un error de compilación se muestra con el renglón.
    await js(`${runner}.editor.setDoc('#include <SDL3/SDL.h>\\nint main(void) {\\n    SDL_Init(SDL_INIT_VIDEO)\\n    return 0;\\n}\\n')`);
    await js(`void ${runner}.run()`);
    await until(`! ${runner}.running`, 60000);
    check('si no compila, lo dice', await js(`${runner}.status`), 'No compila.');
    check('y muestra el error del compilador', await js(`/main.c:3/.test(${runner}.output)`));
    await shot('3-no-compila');

    // El Bucle Eterno: un while que nunca cede se corta solo.
    await js(`${runner}.editor.setDoc('#include <SDL3/SDL.h>\\nint main(void) {\\n    SDL_Window *v = SDL_CreateWindow("Eterno", 320, 240, 0);\\n    (void)v;\\n    volatile int n = 0;\\n    while (1) { n++; }\\n    return 0;\\n}\\n')`);
    await js(`void ${runner}.run()`);
    await until(`${runner}.gamePlaying`, 60000);
    await until(`! ${runner}.gamePlaying`, 10000);
    check('un bucle sin pausas se corta solo', await js(`${runner}.status`), 'Se colgó (el Bucle Eterno)');
    await shot('4-bucle-eterno');

    // printf y SDL_Log salen abajo.
    await js(`${runner}.editor.setDoc('#include <stdio.h>\\n#include <SDL3/SDL.h>\\nint main(void) {\\n    printf("hola %d\\\\n", 3);\\n    SDL_Log("chau");\\n    return 0;\\n}\\n')`);
    await js(`void ${runner}.run()`);
    await until(`${runner}.status.startsWith('El juego terminó')`, 60000);
    check('printf y SDL_Log se ven en la salida', await js(`${runner}.output.trim()`), 'hola 3\nchau');

    check('sin errores de JavaScript en la página', errors, []);
} catch (e) {
    fails++;
    console.log(`✗ ${e.message}`);
    await shot('error');
} finally {
    chrome.kill();
    await sleep(500);
    try { fs.rmSync(profile, { recursive: true, force: true }); } catch { /* Chrome todavía la está soltando */ }
}

console.log(fails ? `\n${fails} con problemas` : '\nTodo bien');
process.exit(fails ? 1 : 0);
