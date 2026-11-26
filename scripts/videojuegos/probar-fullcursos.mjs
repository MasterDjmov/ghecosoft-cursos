// Prueba de los programas SDL3 de FullCursos en la web (D126, fase 3), en Chrome sin ventana y contra la plataforma local:
//   php artisan serve --port=8123   (con los assets compilados)
//   node scripts/videojuegos/probar-fullcursos.mjs [carpeta-para-capturas] [filtro]
// Carga cada main.c de 06-SDL3 y de 29-Juegos-SDL3 en Herramientas → Juegos con SDL3, lo compila, lo deja correr unos
// segundos (con Enter y Espacio para salir del menú) y revisa que compile, que no se corte, que dibuje y, si usa audio,
// que suene. Deja una captura de cada uno. Los que piden bibliotecas que la plataforma todavía no tiene se saltean.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import WebSocket from 'ws';

const BASE = process.env.BASE ?? 'http://127.0.0.1:8123';
const FULL = process.env.FULLCURSOS ?? '/home/djmov/Programas/Cursos/FullCursos';
const SHOTS = process.argv[2] ?? null;
const FILTER = process.argv[3] ?? '';
const SKIP = { '23-YAhoraQue': 'solo lectura' };

const programs = ['06-SDL3', '29-Juegos-SDL3'].flatMap((stage) => fs.readdirSync(path.join(FULL, stage))
    .filter((dir) => /^\d\d-/.test(dir) && fs.existsSync(path.join(FULL, stage, dir, 'main.c')))
    .map((dir) => ({ stage, dir, file: path.join(FULL, stage, dir, 'main.c') })))
    .filter((p) => p.dir.includes(FILTER) || p.stage.includes(FILTER) && FILTER);

const profile = fs.mkdtempSync(path.join(process.env.TMPDIR ?? '/tmp', 'fullcursos-'));
const chrome = spawn(process.env.CHROME ?? '/usr/bin/google-chrome', ['--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`, '--no-first-run', '--autoplay-policy=no-user-gesture-required', '--window-size=1400,1100', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
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
        if (await js(expression).catch(() => false)) return true;
        await sleep(150);
    }
    return false;
};
const runner = 'Alpine.$data(document.querySelector("[data-test=game-tool]"))';
const key = async (code, keyName, vk) => {
    await page('Input.dispatchKeyEvent', { type: 'keyDown', code, key: keyName, windowsVirtualKeyCode: vk });
    await sleep(60);
    await page('Input.dispatchKeyEvent', { type: 'keyUp', code, key: keyName, windowsVirtualKeyCode: vk });
};

/** ¿Cuántos colores distintos hay en el juego? (una pantalla negra o de un solo color: no dibujó nada) */
async function colors() {
    const rect = await js('(() => { const r = document.querySelector("[data-test=game-canvas]").getBoundingClientRect(); return { x: r.x, y: r.y + scrollY, w: r.width, h: r.height }; })()');
    await js(`scrollTo(0, ${Math.max(0, rect.y - 40)})`);
    await sleep(100);
    const shot = await page('Page.captureScreenshot', { format: 'png', clip: { x: rect.x, y: rect.y, width: rect.w, height: rect.h, scale: 320 / rect.w } });
    if (!shot.result) return { count: 0, data: null };
    const count = await js(`(async () => {
        const image = new Image();
        image.src = 'data:image/png;base64,${shot.result.data}';
        await image.decode();
        const c = new OffscreenCanvas(image.width, image.height);
        const g = c.getContext('2d');
        g.drawImage(image, 0, 0);
        const px = g.getImageData(0, 0, image.width, image.height).data;
        const seen = new Set();
        for (let i = 0; i < px.length; i += 16) seen.add((px[i] >> 4) << 8 | (px[i + 1] >> 4) << 4 | px[i + 2] >> 4);
        return seen.size;
    })()`);
    return { count, data: shot.result.data };
}

let fails = 0;
try {
    await page('Page.navigate', { url: `${BASE}/login` });
    await until('document.querySelector("input[type=password]")');
    await js(`(() => { const set = (s, v) => { const f = document.querySelector(s); f.value = v; f.dispatchEvent(new Event('input', { bubbles: true })); }; set('input[name=username], input[type=text], input[name=email]', 'admin'); set('input[type=password]', 'admin123'); document.querySelector('form button[type=submit]').click(); })()`);
    await until('!location.pathname.includes("login")');
    await page('Page.navigate', { url: `${BASE}/herramientas/arcadia` });
    await until(`${runner}?.editor`, 20000);

    for (const program of programs) {
        const name = `${program.stage}/${program.dir}`;
        if (SKIP[program.dir]) {
            console.log(`– ${name}: se saltea (${SKIP[program.dir]})`);
            continue;
        }
        const code = fs.readFileSync(program.file, 'utf8');
        const usesAudio = /SDL_PutAudioStreamData|MIX_Play/.test(code);
        await js(`window.sdlAudioChunks = 0; window.sdlFps = 0; ${runner}.editor.setDoc(${JSON.stringify(code)})`);
        await js(`void ${runner}.run()`);
        const started = await until(`${runner}.gamePlaying || (! ${runner}.running && ${runner}.status !== '' && ! ${runner}.status.startsWith('Compilando'))`, 180000);
        await sleep(1200);
        if (program.dir === '08-PongEnRed') {
            // Dos ventanas en la red de mentira: la primera es anfitrión (1) y la segunda, invitado (2).
            await js('document.querySelector("[data-test=game-canvas]").focus()');
            await key('Digit1', '1', 49);
            await js(`${runner}.gameSecondRun()`.replace('gameSecondRun()', 'gameSecondRun(), 0'));
            const second = await until('document.querySelectorAll("[data-test=game-canvas]").length === 2', 60000);
            await sleep(800);
            await js('document.querySelectorAll("[data-test=game-canvas]")[1].focus()');
            await key('Digit2', '2', 49 + 1);
            await sleep(3000);
            const output = await js(`${runner}.output`);
            const connected = /invitado conectado/.test(output);
            const both = await js(`${runner}.gamePlaying && ${runner}.gameSecond`);
            const ok = second && connected && both;
            if (!ok) fails++;
            if (process.env.SALIDA) console.log(output.trim().split('\n').slice(-10).map((l) => `    | ${l}`).join('\n'));
            console.log(`${ok ? '✓' : '✗'} ${name} (dos ventanas: ${second ? 'sí' : 'no'}, conectadas: ${connected ? 'sí' : 'no'})`);
            if (SHOTS) {
                const shot = await page('Page.captureScreenshot', { format: 'png' });
                fs.writeFileSync(path.join(SHOTS, `${program.stage}-${program.dir}.png`), Buffer.from(shot.result.data, 'base64'));
            }
            await js(`${runner}.gameStop()`);
            await sleep(2000);
            continue;
        }
        // Salir del menú, por si tiene: Enter, Espacio y 1.
        await js('document.querySelector("[data-test=game-canvas]")?.focus()');
        await key('Enter', 'Enter', 13);
        await key('Space', ' ', 32);
        await key('Digit1', '1', 49);
        await sleep(500);
        // Ya en la partida: saltar o disparar (así suenan los que solo suenan al hacer algo).
        // (dos tandas: un salto solo suena si arranca desde el piso)
        for (let round = 0; round < 2; round++) {
            for (const [code, name, vk] of [['Space', ' ', 32], ['KeyW', 'w', 87], ['ArrowUp', 'ArrowUp', 38]]) {
                await page('Input.dispatchKeyEvent', { type: 'keyDown', code, key: name, windowsVirtualKeyCode: vk });
                await sleep(250);
                await page('Input.dispatchKeyEvent', { type: 'keyUp', code, key: name, windowsVirtualKeyCode: vk });
            }
            await sleep(900);
        }
        await sleep(1500);
        const state = await js(`({ playing: ${runner}.gamePlaying, error: ${runner}.error, status: ${runner}.status, output: ${runner}.output })`);
        const seen = state.playing ? await colors() : { count: 0 };
        if (SHOTS && seen.data) fs.writeFileSync(path.join(SHOTS, `${program.stage}-${program.dir}.png`), Buffer.from(seen.data, 'base64'));
        const audio = await js('window.sdlAudioChunks ?? 0');
        const fps = await js('window.sdlFps ?? 0');
        const problems = [];
        if (!started) problems.push('no arrancó');
        if (state.error) problems.push(`${state.status}: ${(state.output ?? '').slice(-400)}`);
        if (!state.error && !state.playing && !/terminó \(devolvió 0\)/.test(state.status)) problems.push(`terminó solo: ${state.status}`);
        if (state.playing && seen.count < 2) problems.push('la pantalla está vacía');
        // Un juego con VSync tiene que ir a unos 60 cuadros por segundo (ni trabado ni a lo loco).
        if (state.playing && /SDL_SetRenderVSync\(\w+,\s*1\)/.test(code) && (fps < 45 || fps > 75)) problems.push(`va a ${fps} cuadros por segundo (con VSync tienen que ser unos 60)`);
        if (usesAudio && state.playing && audio === 0) problems.push('no sonó');
        if (process.env.SALIDA) console.log((state.output ?? '').trim().split('\n').slice(-12).map((l) => `    | ${l}`).join('\n'));
        if (problems.length) fails++;
        console.log(`${problems.length ? '✗' : '✓'} ${name}${state.playing ? ` (${seen.count} colores${usesAudio ? `, ${audio} sonidos` : ''}, ${fps} cuadros/s)` : ''}${problems.length ? ': ' + problems.join(' · ') : ''}`);
        await js(`${runner}.gameControl?.kill()`);
        await sleep(300);
    }
    if (errors.length) {
        fails++;
        console.log(`✗ errores de JavaScript en la página: ${errors.join(' | ')}`);
    }
} catch (e) {
    fails++;
    console.log(`✗ ${e.message}`);
} finally {
    chrome.kill();
    await sleep(500);
    try { fs.rmSync(profile, { recursive: true, force: true }); } catch { /* Chrome la está soltando */ }
}
console.log(fails ? `\n${fails} con problemas` : '\nTodo bien');
process.exit(fails ? 1 : 0);
