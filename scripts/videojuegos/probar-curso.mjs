// Prueba las micro-misiones de juego de un curso (D126, fase 4) con el mismo robot de Arcadia que usa el alumno, en
// Chrome sin ventana y contra la plataforma local (php artisan serve --port=8123, con los assets compilados):
//   node scripts/videojuegos/probar-curso.mjs cursos/videojuegos [--only=R01] [--fill] [--force]
// Corre la «Solución» de cada micro-misión con sus «Eventos» y su «Estado» y la compara con la «Salida esperada»; con
// --fill escribe la que falte (o la que cambió, con --force). Avisa si el «Código inicial» ya da la salida (se
// resolvería sin hacer nada) o si no compila (tiene que compilar: el alumno lo juega antes de tocarlo).
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import WebSocket from 'ws';

const args = process.argv.slice(2);
const folder = path.resolve(args.find((a) => !a.startsWith('--')) ?? 'cursos/videojuegos');
const only = (args.find((a) => a.startsWith('--only=')) ?? '').slice(7);
const fill = args.includes('--fill');
const force = args.includes('--force');
const BASE = process.env.BASE ?? 'http://127.0.0.1:8123';

const FIELD = { 'solución': 'solution', 'código inicial': 'starter', eventos: 'events', estado: 'state', 'salida esperada': 'expected' };

function block(text) {
    const fenced = text.match(/^\s*(`{3,}|~{3,})[\w+-]*[ \t]*\n([\s\S]*?)\n[ \t]*\1\s*$/);
    return fenced ? fenced[2] : text.trim();
}

/** Las micro-misiones de juego del archivo: { code, fields: { solution, starter, events, state, expected } }. */
function missions(text) {
    const found = [];
    const re = /^### Micro-misión ([A-Z0-9-]+) · .*$/gm;
    const heads = [];
    let m;
    while ((m = re.exec(text))) heads.push({ code: m[1], start: m.index });
    for (const h of heads) {
        const lineEnd = text.indexOf('\n', h.start);
        const next = text.slice(lineEnd).search(/^#{2,3} /m);
        const body = text.slice(h.start, next === -1 ? text.length : lineEnd + next);
        const fields = {};
        for (const part of body.split(/^#### /m).slice(1)) {
            const newline = part.indexOf('\n');
            const title = part.slice(0, newline).trim().toLowerCase();
            if (FIELD[title]) fields[FIELD[title]] = block(part.slice(newline + 1).replace(/\n+$/, ''));
        }
        if ((fields.starter ?? '').includes('<SDL3/')) found.push({ code: h.code, fields });
    }
    return found;
}

const normalize = (t) => String(t ?? '').replace(/\r\n?/g, '\n').replace(/[ \t]+$/gm, '').replace(/^\n+|\n+$/g, '');
const lines = (t) => String(t ?? '').split('\n').map((l) => l.trim()).filter((l) => l && !l.startsWith('//'));

function writeExpected(file, code, output) {
    const text = fs.readFileSync(file, 'utf8');
    const start = text.indexOf(`### Micro-misión ${code} ·`);
    const lineEnd = text.indexOf('\n', start);
    const next = text.slice(lineEnd).search(/^#{2,3} /m);
    const end = next === -1 ? text.length : lineEnd + next;
    let body = text.slice(start, end);
    const section = `#### Salida esperada\n\`\`\`\n${output}\n\`\`\`\n\n`;
    const existing = /^#### Salida esperada\n[\s\S]*?(?=^#### |(?![\s\S]))/m;
    body = existing.test(body) ? body.replace(existing, section) : body.replace(/^#### Solución/m, `${section}#### Solución`);
    fs.writeFileSync(file, text.slice(0, start) + body + text.slice(end));
}

// ---------- Chrome
const profile = fs.mkdtempSync(path.join(process.env.TMPDIR ?? '/tmp', 'arcadia-curso-'));
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
const runner = 'Alpine.$data(document.querySelector("[data-test=game-tool]"))';

/** Corre el código con el robot: { output } o { error }. */
async function robot(code, events, state) {
    await js(`(() => { const r = ${runner}; r.gameStop(); r.editor.setDoc(${JSON.stringify(code)}); r.gameTest = ${JSON.stringify({ events: events ?? '', checks: lines(state) })}; })()`);
    await js(`(() => { window.robotError = null; ${runner}.gameCheck().catch((e) => { window.robotError = String(e?.stack ?? e); ${runner}.running = false; }); })()`);
    await sleep(100);
    try {
        await until(`! ${runner}.running`, Number(process.env.ESPERA ?? 120000));
    } catch {
        const stuck = await js(`({ status: ${runner}.status, output: ${runner}.output, fail: window.robotError })`);
        return { error: `no terminó (${stuck.status}) ${stuck.output} ${stuck.fail ?? ''}` };
    }
    const state2 = await js(`({ error: ${runner}.error, status: ${runner}.status, output: ${runner}.output, fail: window.robotError })`);
    if (state2.fail) return { error: `se rompió la prueba: ${state2.fail}` };
    return state2.error ? { error: `${state2.status}: ${state2.output}` } : { output: state2.output === '(sin salida)' ? '' : state2.output };
}

let ok = 0;
let bad = 0;
let filled = 0;
try {
    await page('Page.navigate', { url: `${BASE}/login` });
    await until('document.querySelector("input[type=password]")');
    await js(`(() => { const set = (s, v) => { const f = document.querySelector(s); f.value = v; f.dispatchEvent(new Event('input', { bubbles: true })); }; set('input[name=username], input[type=text], input[name=email]', 'admin'); set('input[type=password]', 'admin123'); document.querySelector('form button[type=submit]').click(); })()`);
    await until('!location.pathname.includes("login")');
    await page('Page.navigate', { url: `${BASE}/herramientas/arcadia` });
    await until(`${runner}?.editor`, 20000);

    const files = fs.statSync(folder).isFile() ? [folder] : fs.readdirSync(folder).filter((f) => f.endsWith('.md')).sort().map((f) => path.join(folder, f));
    for (const file of files) {
        for (const mission of missions(fs.readFileSync(file, 'utf8'))) {
            if (only && !mission.code.startsWith(only)) continue;
            const f = mission.fields;
            if (!f.solution) {
                console.log(`  ? ${mission.code}: no tiene «Solución»`);
                bad++;
                continue;
            }
            const result = await robot(f.solution, f.events, f.state);
            if (result.error) {
                console.log(`  ✗ ${mission.code}: la solución falla: ${result.error.slice(0, 600)}`);
                bad++;
                continue;
            }
            const output = normalize(result.output);
            if (!f.expected || (force && normalize(f.expected) !== output)) {
                if (fill) {
                    writeExpected(file, mission.code, output);
                    filled++;
                    console.log(`  ✎ ${mission.code}: salida esperada escrita`);
                } else {
                    console.log(`  ? ${mission.code}: falta la salida esperada (correr con --fill). Da:\n${output}`);
                    bad++;
                }
                continue;
            }
            if (normalize(f.expected) !== output) {
                console.log(`  ✗ ${mission.code}: la solución no da la salida esperada.\n    esperada: ${JSON.stringify(normalize(f.expected))}\n    da:       ${JSON.stringify(output)}`);
                bad++;
                continue;
            }
            const starter = await robot(f.starter, f.events, f.state);
            if (starter.error && /No compila|Compilador/.test(starter.error)) {
                console.log(`  ! ${mission.code}: el código inicial no compila (tiene que compilar: se juega antes de tocarlo)\n${starter.error.slice(0, 600)}`);
                bad++;
                continue;
            }
            if (!starter.error && normalize(starter.output) === output) {
                console.log(`  ! ${mission.code}: el código inicial ya da la salida esperada`);
                bad++;
                continue;
            }
            ok++;
            console.log(`  ✓ ${mission.code}`);
        }
    }
} finally {
    browser.close();
    chrome.kill();
}
console.log(`\n${ok} bien${filled ? `, ${filled} escritas` : ''}${bad ? `, ${bad} con problemas` : ''}.`);
process.exit(bad ? 1 : 0);
