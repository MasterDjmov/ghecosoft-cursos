// Prueba de aceptación de la caja de JavaScript (D115), en Chrome sin ventana: la consola, el reloj virtual, los
// temporizadores, el Puerto simulado, las cookies y el almacenamiento, los eventos y el Estado, el lienzo, los topes
// y, sobre todo, que el código no pueda tocar nada de afuera. Correrla después de tocar la caja:
//   node scripts/js-micro/probar-caja.mjs [--only=texto]
import { openChrome } from './chrome.mjs';

const only = (process.argv.find((a) => a.startsWith('--only=')) ?? '').slice(7);

const CASES = [
    // ── La consola
    ['consola: textos, números y template literals', `const nombre = 'Nima'; let fichas = 3;\nconsole.log('Hola', nombre);\nconsole.log(\`Tenés \${fichas} fichas\`, fichas + 1, -0, 2n);`, {}, { output: "Hola Nima\nTenés 3 fichas 4 -0 2n" }],
    ['consola: objetos, arreglos, Map y Set como Node', `console.log({ nombre: 'Nima', nivel: 4, inventario: ['soga', 'brújula'] });\nconsole.log([1, [2, [3, [4]]]], new Map([['a', 1]]), new Set([1, 2]));\nconsole.log([undefined, null, true, 'x'], {});\nclass Heroe { constructor() { this.vida = 10; } }\nconsole.log(new Heroe(), Heroe, function tirar() {}, () => 1);`, {},
        { output: "{ nombre: 'Nima', nivel: 4, inventario: [ 'soga', 'brújula' ] }\n[ 1, [ 2, [ 3, [Array] ] ] ] Map(1) { 'a' => 1 } Set(2) { 1, 2 }\n[ undefined, null, true, 'x' ] {}\nHeroe { vida: 10 } [class Heroe] [Function: tirar] [Function (anonymous)]" }],
    ['consola: objeto largo en varias líneas', `console.log({ nombre: 'Nima la arquera del Valle', region: 'Feria de las Luces', arco: 'Arco de Rama del Valle' });`, {},
        { output: "{\n  nombre: 'Nima la arquera del Valle',\n  region: 'Feria de las Luces',\n  arco: 'Arco de Rama del Valle'\n}" }],
    ['consola: %s, %d, table, group, count', `console.log('%s tiene %d fichas', 'Nima', 3.7);\nconsole.table([{ a: 1, b: 2 }, { a: 3 }]);\nconsole.group('Puestos');\nconsole.log('tiro');\nconsole.groupEnd();\nconsole.count(); console.count();`, {},
        { output: "Nima tiene 3.7 fichas\n┌─────────┬───┬───┐\n│ (index) │ a │ b │\n├─────────┼───┼───┤\n│ 0       │ 1 │ 2 │\n│ 1       │ 3 │   │\n└─────────┴───┴───┘\nPuestos\n  tiro\ndefault: 1\ndefault: 2" }],
    ['consola: coerción', `console.log("2" + 2, "2" * 2, 0.1 + 0.2, typeof null, [] + {}, NaN === NaN);`, {}, { output: '22 4 0.30000000000000004 object [object Object] false' }],

    // ── Errores
    ['error de sintaxis con su línea', `let a = 1;\nconsole.log(a;\n`, {}, { errorIncludes: 'línea 2', syntax: true }],
    ['llave sin cerrar', `function f() {\n  console.log(1);\n`, {}, { errorIncludes: 'termina antes de tiempo' }],
    ['ReferenceError en criollo y con la línea', `console.log('antes');\nconsole.log(fichaz);`, {}, { output: 'antes', errorIncludes: 'línea 2: «fichaz» no existe' }],
    ['const no se cambia', `const x = 1;\nx = 2;`, {}, { errorIncludes: 'const' }],
    ['undefined.propiedad', `const puesto = undefined;\nconsole.log(puesto.nombre);`, {}, { errorIncludes: 'Quisiste leer «.nombre» de algo que es undefined' }],
    ['promesa rechazada sin catch', `Promise.reject(new Error('se cayó la flecha'));\nconsole.log('sigo');`, {}, { output: 'sigo', errorIncludes: 'nadie la atajó' }],
    ['un error en un temporizador no frena a los demás', `setTimeout(() => { throw new Error('uno'); }, 10);\nsetTimeout(() => console.log('dos'), 20);`, {}, { output: 'dos', errorIncludes: 'uno' }],

    // ── Topes
    ['while (true) se corta', `let i = 0;\nwhile (true) { i++; }`, { timeout: 1500 }, { timedOut: true, errorIncludes: 'Se cortó' }],
    ['for sin llaves también', `for (;;) Math.random();`, { timeout: 1500 }, { timedOut: true, errorIncludes: 'Se cortó' }],
    ['recursión sin fin', `function f(n) { return f(n + 1); }\nf(0);`, {}, { errorIncludes: 'se llama a sí misma' }],
    ['setTimeout que se reprograma sin fin', `function otra() { setTimeout(otra, 0); }\notra();`, { timeout: 3000 }, { output: '', noteIncludes: 'quedó 1 temporizador' }],
    ['atajar el corte no lo esquiva', `try { while (true) {} } catch (e) { console.log('atajado'); }\nwhile (true) {}`, { timeout: 1500 }, { timedOut: true, errorIncludes: 'Se cortó' }],

    // ── El reloj virtual
    ['setTimeout en orden y sin esperar de verdad', `setTimeout(() => console.log('tres'), 3000);\nsetTimeout(() => console.log('uno'), 1000);\nsetTimeout(() => console.log('dos'), 2000);\nconsole.log('ya');`, {}, { output: 'ya\nuno\ndos\ntres', fasterThan: 1500 }],
    ['setInterval y clearInterval', `let n = 0;\nconst id = setInterval(() => { n++; console.log('farol', n); if (n === 3) clearInterval(id); }, 500);`, {}, { output: 'farol 1\nfarol 2\nfarol 3' }],
    ['Date y performance siguen el reloj de la caja', `const t0 = Date.now();\nsetTimeout(() => console.log(Date.now() - t0, Math.round(performance.now())), 1500);\nconsole.log(new Date().toISOString());`, {}, { output: '2026-03-03T00:00:00.000Z\n1500 1500' }],
    ['await con un temporizador (top-level await)', `const esperar = (ms) => new Promise((r) => setTimeout(r, ms));\nconsole.log('suelto');\nawait esperar(2000);\nconsole.log('llegó', Date.now() - Date.UTC(2026, 2, 3));`, {}, { output: 'suelto\nllegó 2000' }],
    ['requestAnimationFrame a 60 cuadros', `let cuadros = 0; let ultimo = 0;\nfunction paso(t) { cuadros++; ultimo = t; if (cuadros < 60) requestAnimationFrame(paso); else console.log(cuadros, Math.round(ultimo)); }\nrequestAnimationFrame(paso);`, {}, { output: '60 1000' }],
    ['Math.random con semilla da siempre lo mismo', `console.log(Math.random(), Math.floor(Math.random() * 6) + 1);`, {}, { same: true }],
    ['un await que nunca llega', `await new Promise(() => {});\nconsole.log('nunca');`, {}, { output: '', noteIncludes: 'quedó esperando' }],
    ['sin nada pendiente, el reloj no salta al horizonte', `setTimeout(() => console.log(performance.now()), 250);`, { checks: 'reloj' }, { output: '250\n── Estado ──\nreloj: 250 ms' }],
    ['los temporizadores que quedan andando se avisan', `setInterval(() => {}, 1000);\nconsole.log('ok');`, {}, { output: 'ok', noteIncludes: 'quedó 1 temporizador' }],

    // ── El Puerto
    ['fetch al Puerto con await', `const r = await fetch('/puerto/hola');\nconsole.log(r.status, r.ok);\nconst datos = await r.json();\nconsole.log(datos.de, '-', datos.mensaje);`, {}, { output: '200 true\nElefa - ¡Hola, Nima! Te escribe Elefa desde el Puerto.' }],
    ['fetch con then y Promise.all', `Promise.all([fetch('/puerto/puestos/1'), fetch('/puerto/puestos/9')])\n  .then((rs) => Promise.all(rs.map((r) => r.json())))\n  .then(([a, b]) => console.log(a.nombre, '|', b.error));`, {}, { output: 'Tiro al blanco | No hay ningún puesto con el número 9.' }],
    ['lo lento llega después', `fetch('/puerto/lento').then(() => console.log('lento'));\nfetch('/puerto/clima').then(() => console.log('clima'));`, {}, { output: 'clima\nlento' }],
    ['JSON roto', `try { await (await fetch('/puerto/roto')).json(); } catch (e) { console.log(e.name); }`, {}, { output: 'SyntaxError' }],
    ['internet no hay', `try { await fetch('https://example.com/'); } catch (e) { console.log(e.name, e.message); }`, {}, { output: 'TypeError Failed to fetch', boardNotice: 'red' }],
    ['POST con JSON', `const r = await fetch('/puerto/mensajes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ texto: 'Llegué', de: 'Nima' }) });\nconsole.log(r.status, (await r.json()).id);\nconsole.log((await (await fetch('/puerto/mensajes')).json()).length);`, {}, { output: '201 3\n3' }],
    ['la sesión con cookie HttpOnly', `console.log((await fetch('/puerto/perfil')).status);\nawait fetch('/puerto/login', { method: 'POST', body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }) });\nconsole.log((await (await fetch('/puerto/perfil')).json()).nombre, JSON.stringify(document.cookie));\nawait fetch('/puerto/salir', { method: 'POST' });\nconsole.log((await fetch('/puerto/perfil')).status);`, { checks: 'cookies\npedidos' }, { output: "401\nNima \"\"\n401\n── Estado ──\ncookies: (ninguna)\npedidos: GET /puerto/perfil → 401\npedidos: POST /puerto/login → 200\npedidos: GET /puerto/perfil → 200\npedidos: POST /puerto/salir → 200\npedidos: GET /puerto/perfil → 401" }],
    ['AbortController cancela', `const c = new AbortController();\nsetTimeout(() => c.abort(), 100);\ntry { await fetch('/puerto/lento', { signal: c.signal }); } catch (e) { console.log(e.name); }`, {}, { output: 'AbortError' }],
    ['XMLHttpRequest no está', `new XMLHttpRequest();`, {}, { errorIncludes: 'no está en la caja' }],

    // ── Cookies y almacenamiento
    ['cookies con vencimiento', `document.cookie = 'ficha=3; max-age=2';\ndocument.cookie = 'tema=noche';\nconsole.log(document.cookie);\nsetTimeout(() => console.log(document.cookie), 3000);`, {}, { output: 'ficha=3; tema=noche\ntema=noche' }],
    ['localStorage y JSON', `localStorage.setItem('puntos', JSON.stringify({ tiro: 3 }));\nlocalStorage.visitas = 1;\nconsole.log(JSON.parse(localStorage.getItem('puntos')).tiro, localStorage.length, localStorage.getItem('nada'));\nsessionStorage.setItem('x', 'y');`, { checks: 'local\nlocal visitas\nsession x' }, { output: '3 2 null\n── Estado ──\nlocal: puntos={"tiro":3}; visitas=1\nlocal visitas: 1\nsession x: y' }],
    ['lo que trae la consigna (segunda visita)', `const v = Number(localStorage.getItem('visitas') ?? 0) + 1;\nlocalStorage.setItem('visitas', v);\nconsole.log('Visita', v, document.cookie);`, { storage: { local: { visitas: '1' } }, cookies: 'nombre=Nima' }, { output: 'Visita 2 nombre=Nima' }],

    // ── Ventanitas
    ['prompt, confirm y alert con la Entrada', `const nombre = prompt('¿Cómo te llamás?');\nif (confirm('¿Jugás?')) alert('¡A jugar, ' + nombre + '!');\nconsole.log(prompt('¿Algo más?'));`, { stdin: 'Nima\nsi\n' }, { output: '[pregunta] ¿Cómo te llamás? → Nima\n[confirmar] ¿Jugás? → Aceptar\n[alerta] ¡A jugar, Nima!\n[pregunta] ¿Algo más? → (cancelado)\nnull' }],

    // ── La página, los eventos y el Estado
    ['DOM: cambiar texto y clases al hacer click', `const boton = document.querySelector('#prender');\nconst cartel = document.querySelector('#cartel');\nboton.addEventListener('click', () => {\n  cartel.textContent = '¡Farol prendido!';\n  document.querySelector('.farol').classList.add('prendido');\n});`,
        { page: '<h1 id="cartel">Apagado</h1><div class="farol"></div><button id="prender">Prender</button>', events: 'click #prender', checks: '#cartel\n.farol @class' }, { output: '── Estado ──\n#cartel: ¡Farol prendido!\n.farol @class: farol prendido' }],
    ['DOM: formulario, escribir y enviar', `document.querySelector('form').addEventListener('submit', (e) => {\n  e.preventDefault();\n  const li = document.createElement('li');\n  li.textContent = document.querySelector('#nombre').value;\n  document.querySelector('ul').append(li);\n});`,
        { page: '<form><input id="nombre"><button>Anotar</button></form><ul></ul>', events: 'escribir #nombre Nima\nenviar form\nescribir #nombre Mia\nenviar form', checks: 'li #\nli\n#nombre @value' }, { output: '── Estado ──\nli #: 2\nli: Nima\nli: Mia\n#nombre @value: Mia' }],
    ['DOM: teclas y esperar', `let x = 0;\ndocument.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') x += 10; document.querySelector('#x').textContent = x; });\nsetTimeout(() => document.querySelector('#x').textContent += ' fin', 1000);`,
        { page: '<p id="x">0</p>', events: 'tecla ArrowRight\ntecla ArrowRight\nesperar 1000', checks: '#x' }, { output: '── Estado ──\n#x: 20 fin' }],
    ['DOM: evento sobre algo que no está', `1;`, { page: '<p>hola</p>', events: 'click #nada', checks: 'p' }, { output: '── Estado ──\n! click #nada: no hay ningún elemento «#nada»\np: hola' }],
    ['DOM: estilo calculado', `document.querySelector('#f').style.backgroundColor = 'gold';`, { page: '<div id="f">farol</div>', checks: 'estilo #f { background-color }' }, { output: '── Estado ──\nestilo #f { background-color }: rgb(255, 215, 0)' }],
    ['página entera del alumno con su script (línea del error en la página)', `<!doctype html>\n<html><body>\n<p id="p">hola</p>\n<script>\nconsole.log(document.querySelector('#p').textContent);\nnoexiste();\n</script>\n</body></html>`, {}, { output: 'hola', errorIncludes: 'línea 6' }],
    ['los enlaces no sacan de la página', `document.querySelector('a').click(); console.log('sigo acá');`, { page: '<a href="https://example.com">afuera</a>' }, { output: 'sigo acá', boardNotice: 'enlace' }],

    // ── El lienzo
    ['canvas: lo que se dibuja en el último cuadro', `const ctx = document.querySelector('canvas').getContext('2d');\nlet x = 0;\nfunction cuadro() {\n  ctx.clearRect(0, 0, 200, 100);\n  ctx.fillStyle = '#ffd400';\n  ctx.fillRect(x, 10, 20, 20);\n  x += 2;\n  if (x < 60) requestAnimationFrame(cuadro);\n}\nrequestAnimationFrame(cuadro);`,
        { page: '<canvas width="200" height="100"></canvas>', checks: 'lienzo' }, { output: '── Estado ──\nlienzo: clearRect(0, 0, 200, 100)\nlienzo: fillRect(58, 10, 20, 20) #ffd400' }],
    ['canvas: mantener una tecla unos cuadros', `const ctx = document.querySelector('canvas').getContext('2d');\nconst teclas = new Set(); let x = 0;\naddEventListener('keydown', (e) => teclas.add(e.key));\naddEventListener('keyup', (e) => teclas.delete(e.key));\nfunction loop() { if (teclas.has('ArrowRight')) x += 1; ctx.clearRect(0, 0, 100, 100); ctx.fillRect(x, 0, 5, 5); requestAnimationFrame(loop); }\nrequestAnimationFrame(loop);`,
        { page: '<canvas width="100" height="100"></canvas>', events: 'apretar ArrowRight\ncuadros 30\nsoltar ArrowRight\ncuadros 10', checks: 'lienzo' }, { output: '── Estado ──\nlienzo: clearRect(0, 0, 100, 100)\nlienzo: fillRect(30, 0, 5, 5) #000000' }],

    // ── Seguridad: nada de afuera
    ['no ve las cookies de verdad ni la página de afuera', `let afuera = 'no';\ntry { afuera = parent.document.title; } catch (e) { afuera = e.name; }\nconsole.log(afuera, location.origin, document.cookie === '');`, {}, { output: 'SecurityError null true' }],
    ['no puede abrir ventanas ni salir por fetch absoluto a la plataforma', `console.log(window.open('https://example.com'));\ntry { await fetch(location.ancestorOrigins?.[0] ?? 'http://127.0.0.1/'); } catch (e) { console.log(e.message); }`, {}, { output: 'null\nFailed to fetch' }],
    ['no hay eval ni Function (CSP)', `try { eval('1+1'); } catch (e) { console.log(e.name); }\ntry { new Function('return 1')(); } catch (e) { console.log(e.name); }`, {}, { output: 'EvalError\nEvalError' }],
    ['un script de afuera no se carga', `<p>x</p><script src="https://example.com/x.js"></script><script>console.log('mío')</script>`, {}, { output: 'mío', noteIncludes: 'No se cargó https://example.com/x.js' }],
    ['una imagen de afuera no carga', `const img = new Image();\nimg.onerror = () => console.log('bloqueada');\nimg.onload = () => console.log('cargó');\nimg.src = 'https://example.com/x.png';\nawait new Promise((r) => { img.addEventListener('error', r); img.addEventListener('load', r); });`, {}, { output: 'bloqueada' }],
    ['irse a otra dirección saca la caja', `location.href = 'https://example.com';`, {}, { errorIncludes: 'irse a otra dirección' }],

    // ── En vivo
    ['en vivo: después de comprobar, el reloj sigue al de verdad', `let n = 0;\nsetInterval(() => console.log('tic', ++n), 200);`, { live: true, horizon: 0, liveMs: 700 }, { liveIncludes: 'tic' }],
];

const chrome = await openChrome();
let passed = 0;
let failed = 0;
for (const [name, code, options, expect] of CASES) {
    if (only && !name.includes(only)) continue;
    const t0 = Date.now();
    let result;
    try {
        result = await chrome.run(code, options);
    } catch (e) {
        result = { crash: e.message };
    }
    const elapsed = Date.now() - t0;
    const problems = [];
    if (result.crash) problems.push(`se rompió: ${result.crash}`);
    if ('output' in expect && result.output !== expect.output) problems.push(`salida:\n${JSON.stringify(result.output)}\nesperada:\n${JSON.stringify(expect.output)}`);
    if (expect.errorIncludes && !String(result.error ?? '').includes(expect.errorIncludes)) problems.push(`error: ${JSON.stringify(result.error)} (tenía que decir «${expect.errorIncludes}»)`);
    if (expect.errorIncludesAny && !expect.errorIncludesAny.some((t) => String(result.error ?? '').includes(t))) problems.push(`error: ${JSON.stringify(result.error)}`);
    if (!expect.errorIncludes && !expect.errorIncludesAny && result.error) problems.push(`no tenía que fallar: ${result.error}`);
    if (expect.timedOut && !result.timedOut) problems.push('tenía que cortarse por tiempo');
    if (expect.syntax && !result.syntax) problems.push('tenía que ser un error de sintaxis');
    if (expect.noteIncludes && !(result.notes ?? []).some((n) => n.includes(expect.noteIncludes))) problems.push(`notas: ${JSON.stringify(result.notes)}`);
    if (expect.boardNotice && !(result.board?.notices ?? []).some((n) => n.kind === expect.boardNotice)) problems.push(`avisos del tablero: ${JSON.stringify(result.board?.notices)}`);
    if (expect.fasterThan && elapsed > expect.fasterThan) problems.push(`tardó ${elapsed} ms`);
    if (expect.same) {
        const again = await chrome.run(code, options);
        if (again.output !== result.output) problems.push(`no dio lo mismo: ${result.output} / ${again.output}`);
    }
    if (expect.liveIncludes && !String(result.live ?? '').includes(expect.liveIncludes)) problems.push(`en vivo: ${JSON.stringify(result.live)}`);

    if (problems.length) {
        failed++;
        console.log(`✗ ${name}\n    ${problems.join('\n    ')}`);
    } else {
        passed++;
        console.log(`✓ ${name} (${elapsed} ms)`);
    }
}
await chrome.close();
console.log(`\n${passed} bien, ${failed} mal.`);
process.exit(failed ? 1 : 0);
