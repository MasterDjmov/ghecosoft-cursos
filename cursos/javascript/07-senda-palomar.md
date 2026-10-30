# RAMA S02 · Senda del Palomar: una página que habla con el Puerto

```meta
tipo: senda
posicion: 7
```

## S02-N01 · La ventanilla del Palomar

```meta
tipo: tema
padre: R04-N08
precio: 3
moneda: comodin
criatura: troll
temas: js.fetch, web.api-rest
usa: web.http, js.dom
```

### Crónica

Después de vencer al Troll, llega una flecha de luz con un sello de lacre violeta. Es de **Elefa**, la Capitana del Puerto: *«En el Puerto tenemos un **Palomar**: palomas que llevan mensajes a todas las regiones. Nilo escribió la parte de adentro, la que guarda y contesta. Pero no hay **ventanilla**: la gente de la Feria no tiene dónde leer los mensajes ni dónde escribirlos. Vos sabés tirar flechas al Puerto. ¿Nos armás la ventanilla?»*

Nilo espera del otro lado con su bufanda violeta. Arriba, en un poste, una gaviota mira todo con un ojo: **Pico**, la ladrona del Puerto.

### Objetivos

- Pedir una lista al Puerto con `fetch` y dibujarla en la página.
- Mostrar los estados de la espera: cargando, vacío, error.
- Escribir lo que llega con `textContent`, nunca con `innerHTML`, para que nadie meta código en la página.
- Pedir un elemento por su número (`/puerto/mensajes/2`) y manejar el 404.

### Antes de empezar

- La Torre de las Flechas (R04), sobre todo `fetch` (R04-N04) y los errores propios (R04-N06).
- Si hiciste el curso de PHP, esto es **el otro lado** de la API que escribió Nilo. Si no, no importa: el Puerto ya está andando.

### Explicación

#### Las direcciones del Palomar
| Pedido | Qué hace | Contesta |
|---|---|---|
| `GET /puerto/mensajes` | la lista | `200` con un arreglo |
| `GET /puerto/mensajes/2` | uno solo | `200`, o `404` si no está |
| `POST /puerto/mensajes` | uno nuevo | `201`, o `422` si falta el texto |
| `PATCH /puerto/mensajes/2` | corregir el texto | `200` |
| `DELETE /puerto/mensajes/2` | borrarlo | `204` (sin cuerpo) |

Así se arma casi toda API: **un sustantivo** (`mensajes`) y el **método** dice qué hacer. En el curso de PHP, Nilo la escribe del lado del servidor.

#### Pedir y dibujar
```javascript
const respuesta = await fetch('/puerto/mensajes');
if (!respuesta.ok) throw new Error(`El Palomar contestó ${respuesta.status}`);
const mensajes = await respuesta.json();
for (const m of mensajes) {
  const li = document.createElement('li');
  li.textContent = `${m.de}: ${m.texto}`;
  lista.append(li);
}
```

#### Los tres estados de la espera
Mientras la flecha viaja, la página tiene que decir algo: **cargando** al empezar, **vacío** si llegó una lista sin nada, **error** si falló. Una página que no dice nada parece rota.

#### `textContent`, no `innerHTML`
Lo que llega del servidor lo escribió **otra persona**. Si alguien manda `<img src=x onerror="robar()">` y lo ponés con `innerHTML`, la página **ejecuta** su código. Con `textContent` se ve tal cual, como texto. A esto se lo llama **XSS** (inyección de código en la página), y es la misma idea que la inyección SQL del curso de PHP.

> **En la caja**, el Puerto es de mentira y cada ejecución arranca con los mismos dos mensajes (de Sila y de Tizón). Con `?falla=1` contesta como si estuviera cerrado, y con `?demora=2000` tarda lo que digas.

### Código de ejemplo

```javascript
const lista = await (await fetch('/puerto/mensajes')).json();
console.log(`Hay ${lista.length} mensajes:`);
for (const m of lista) console.log(`- #${m.id} ${m.de}: ${m.texto}`);

const uno = await fetch('/puerto/mensajes/9');
console.log('El 9:', uno.status, (await uno.json()).error);

const cerrado = await fetch('/puerto/mensajes?falla=1');
console.log('Con tormenta:', cerrado.status, cerrado.ok);
```

### Salida esperada

```
Hay 2 mensajes:
- #1 Sila: ¿Dónde estás, Nima? Tu ficha sigue en el Archivo.
- #2 Tizón: Vi pasar las luces por las Forjas. Iban al norte.
El 9: 404 No hay ningún mensaje con el número 9.
Con tormenta: 503 false
```

### ¿Para qué sirve?

Una página con un servidor detrás es casi toda la web: el chat, la tienda, el campus virtual, la lista de tareas que se guarda en la nube. El servidor guarda y decide; la página pide, muestra y avisa.

### Errores habituales

**Troll: dibujar antes de que llegue.** Sin `await`, `respuesta.json()` es una promesa y el `for` no tiene qué recorrer.

**Troll: creer que un 404 es un error de `fetch`.** `fetch` solo falla si no hay red. Un 404 o un 500 **llegan bien**: hay que mirar `respuesta.ok` o `respuesta.status`.

**Goblin: `innerHTML` con lo que mandó otro.** Es la puerta de entrada de Pico.

### Micro-misión S02-N01-P1 · Los mensajes en la ventanilla

```meta
lugar: El Palomar del Puerto, la ventanilla
personajes: Nima, Gheco, Nilo
carta: Lista | const mensajes = await (await fetch('/puerto/mensajes')).json() · li.textContent = `${m.de}: ${m.texto}`
recompensa: xp 10, oro 10
```

#### Escena
La ventanilla del Palomar es un mostrador de madera con un pizarrón vacío. Del otro lado, los mensajes ya esperan en los casilleros. —Pedímelos —dice Nilo— y yo te los tiro.

#### Gheco sugiere
Pedí `/puerto/mensajes` y agregá un `<li>` por mensaje a `#mensajes`, con `de: texto`.

#### Desafío
Que se vean los mensajes del Palomar.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  h1 { font-size: 20px; color: #c7a4ff; }
  li { background: #1c335a; margin: 6px 0; padding: 8px; border-radius: 6px; list-style: none; }
</style>
<h1>🕊 El Palomar del Puerto</h1>
<ul id="mensajes"></ul>
```

#### Estado
```
#mensajes li
pedidos
```

#### Código inicial
```javascript
const lista = document.querySelector('#mensajes');

```

#### Salida esperada
```
── Estado ──
#mensajes li: Sila: ¿Dónde estás, Nima? Tu ficha sigue en el Archivo.
#mensajes li: Tizón: Vi pasar las luces por las Forjas. Iban al norte.
pedidos: GET /puerto/mensajes → 200
```

#### Solución
```javascript
const lista = document.querySelector('#mensajes');
const respuesta = await fetch('/puerto/mensajes');
const mensajes = await respuesta.json();
for (const m of mensajes) {
  const li = document.createElement('li');
  li.textContent = `${m.de}: ${m.texto}`;
  lista.append(li);
}
```

#### Al superarla
Los dos mensajes aparecen en el pizarrón. Nima lee el de Sila y se queda callada. —Ya le contesté —dice, bajito—. Esta vez espero.

#### Imagen
- La ventanilla de un palomar en un puerto de noche: un mostrador de madera, un pizarrón con dos mensajes de luz, y palomas blancas en casilleros detrás.
- Nilo (muchacho de 17, gorra de mensajero azul noche, bufanda violeta larga, bolso cruzado de cuero) del otro lado del mostrador; arriba, en un poste, una gaviota de ojo pícaro.

### Micro-misión S02-N01-P2 · Cargando, vacío o lleno

```meta
lugar: El Palomar del Puerto, la ventanilla
personajes: Nima, Gheco, Nilo
carta: Estados | estado.textContent = 'Cargando…' · después: lista.length ? `${n} mensajes` : 'No hay mensajes'
recompensa: xp 10, oro 10
```

#### Escena
—La gente se queda mirando el pizarrón vacío y se va —dice Nilo—. No sabe si el Palomar está roto o si las palomas todavía vuelan.

#### Gheco sugiere
Antes de pedir, poné `Cargando…` en `#estado`. Cuando llegue, si la lista está vacía poné `No hay mensajes`; si no, `2 mensajes en el Palomar` (con el número que sea).

#### Desafío
Que el Palomar diga en qué anda.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  #estado { color: #c7a4ff; font-style: italic; }
  li { background: #1c335a; margin: 6px 0; padding: 8px; list-style: none; }
</style>
<p id="estado"></p>
<ul id="mensajes"></ul>
```

#### Estado
```
#estado
#mensajes li #
```

#### Código inicial
```javascript
const estado = document.querySelector('#estado');
const lista = document.querySelector('#mensajes');

const mensajes = await (await fetch('/puerto/mensajes')).json();
for (const m of mensajes) {
  const li = document.createElement('li');
  li.textContent = `${m.de}: ${m.texto}`;
  lista.append(li);
}
```

#### Salida esperada
```
── Estado ──
#estado: 2 mensajes en el Palomar
#mensajes li #: 2
```

#### Solución
```javascript
const estado = document.querySelector('#estado');
const lista = document.querySelector('#mensajes');

estado.textContent = 'Cargando…';
const mensajes = await (await fetch('/puerto/mensajes')).json();
for (const m of mensajes) {
  const li = document.createElement('li');
  li.textContent = `${m.de}: ${m.texto}`;
  lista.append(li);
}
estado.textContent = mensajes.length ? `${mensajes.length} mensajes en el Palomar` : 'No hay mensajes';
```

#### Al superarla
*Cargando…*, y enseguida *2 mensajes en el Palomar*. Un pescador que pasaba se queda a leer.

#### Imagen
- El pizarrón de la ventanilla con un cartelito de luz violeta que dice que las palomas están volando (sin texto legible).
- Un pescador con gorro de lana se acerca a leer.

### Micro-misión S02-N01-P3 · La trampa de Pico

```meta
lugar: El Palomar del Puerto, la ventanilla
personajes: Nima, Gheco, Nilo, Pico
carta: textContent | li.textContent = … (se ve tal cual) · li.innerHTML = … (se ejecuta)
recompensa: xp 10, oro 10
```

#### Escena
Pico baja del poste y deja un mensaje en el Palomar. No es un mensaje: es **una etiqueta**, `<b>`, y la ventanilla la dibuja en negrita. —Si puede meter una negrita —dice Nilo, pálido—, puede meter cualquier cosa.

#### Gheco sugiere
El código de la ventanilla escribe con `innerHTML`. Cambialo para que el mensaje de Pico se vea **tal cual**, con sus `<` y `>`.

#### Desafío
Que no aparezca ningún `<b>` en la lista.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  li { background: #1c335a; margin: 6px 0; padding: 8px; list-style: none; }
</style>
<ul id="mensajes"></ul>
```

#### Estado
```
#mensajes li
#mensajes b #
```

#### Código inicial
```javascript
// Pico deja su «mensaje» (esto no lo cambies: es lo que hizo Pico).
await fetch('/puerto/mensajes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ de: 'Pico', texto: '<b>¡Todo esto es mío!</b>' }),
});

const lista = document.querySelector('#mensajes');
const mensajes = await (await fetch('/puerto/mensajes')).json();
for (const m of mensajes) {
  lista.innerHTML += `<li>${m.de}: ${m.texto}</li>`;
}
```

#### Salida esperada
```
── Estado ──
#mensajes li: Sila: ¿Dónde estás, Nima? Tu ficha sigue en el Archivo.
#mensajes li: Tizón: Vi pasar las luces por las Forjas. Iban al norte.
#mensajes li: Pico: <b>¡Todo esto es mío!</b>
#mensajes b #: 0
```

#### Solución
```javascript
// Pico deja su «mensaje» (esto no lo cambies: es lo que hizo Pico).
await fetch('/puerto/mensajes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ de: 'Pico', texto: '<b>¡Todo esto es mío!</b>' }),
});

const lista = document.querySelector('#mensajes');
const mensajes = await (await fetch('/puerto/mensajes')).json();
for (const m of mensajes) {
  const li = document.createElement('li');
  li.textContent = `${m.de}: ${m.texto}`;
  lista.append(li);
}
```

#### Al superarla
El mensaje de Pico aparece con sus `<b>` a la vista, como letras sueltas. No puede hacer nada. Pico grazna, ofendida, y vuelve al poste.

#### Imagen
- Una gaviota de ojo pícaro (Pico) con un pico lleno de letras de madera que no encajan en el pizarrón.
- Nilo, pálido, se seca la frente; Nima cruza los brazos.

### Micro-misión S02-N01-P4 · Cerrado por tormenta

```meta
lugar: El Palomar del Puerto, en una tormenta
personajes: Nima, Gheco, Nilo
carta: res.ok | if (!respuesta.ok) { const { error } = await respuesta.json(); … }
recompensa: xp 15, monedas 5
```

#### Escena
Se larga una tormenta en el Puerto y Elefa cierra el Palomar: las palomas no salen con viento. La ventanilla sigue mostrando *Cargando…* para siempre.

#### Gheco sugiere
Si la respuesta no es `ok`, leé el `error` que manda el Puerto y mostrá `El Palomar no atiende (503): …` en `#estado`, con la clase `error`. Si es `ok`, dibujá la lista como siempre.

#### Desafío
Pedí la lista con `?falla=1` (la tormenta).

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  .error { color: #ff8a80; font-weight: bold; }
</style>
<p id="estado">Cargando…</p>
<ul id="mensajes"></ul>
```

#### Estado
```
#estado
#estado @class
#mensajes li #
```

#### Código inicial
```javascript
const estado = document.querySelector('#estado');
const lista = document.querySelector('#mensajes');

const respuesta = await fetch('/puerto/mensajes?falla=1');
const mensajes = await respuesta.json();
for (const m of mensajes) {
  const li = document.createElement('li');
  li.textContent = `${m.de}: ${m.texto}`;
  lista.append(li);
}
estado.textContent = `${mensajes.length} mensajes`;
```

#### Salida esperada
```
── Estado ──
#estado: El Palomar no atiende (503): El Puerto está cerrado por tormenta.
#estado @class: error
#mensajes li #: 0
```

#### Solución
```javascript
const estado = document.querySelector('#estado');
const lista = document.querySelector('#mensajes');

const respuesta = await fetch('/puerto/mensajes?falla=1');
if (!respuesta.ok) {
  const { error } = await respuesta.json();
  estado.textContent = `El Palomar no atiende (${respuesta.status}): ${error}`;
  estado.classList.add('error');
} else {
  const mensajes = await respuesta.json();
  for (const m of mensajes) {
    const li = document.createElement('li');
    li.textContent = `${m.de}: ${m.texto}`;
    lista.append(li);
  }
  estado.textContent = `${mensajes.length} mensajes`;
}
```

#### Al superarla
La ventanilla avisa en rojo que el Palomar está cerrado por la tormenta. La gente se va a su casa en vez de esperar mojándose.

#### Imagen
- El puerto bajo una tormenta, con olas altas; el palomar con las ventanitas cerradas y un cartel rojo de luz en la ventanilla.
- Nilo con la capucha puesta y la bufanda volando; las palomas resguardadas adentro.

### Micro-misión S02-N01-P5 · Buscar por número

```meta
lugar: El Palomar del Puerto, la ventanilla
personajes: Nima, Gheco, Nilo
carta: Por número | fetch(`/puerto/mensajes/${n}`) · 404 → el error del Puerto
recompensa: xp 15, monedas 5
```

#### Escena
Una señora quiere ver **solo** el mensaje número 2, el de su hijo Tizón. Otro pide el 9, que no existe.

#### Gheco sugiere
En el `submit` del formulario (con `preventDefault`), pedí `/puerto/mensajes/` con el número escrito. Si está, mostrá `#2 Tizón: …` en `#resultado`; si no, el `error` que manda el Puerto.

#### Desafío
Buscan el 2 y después el 9.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  input { width: 60px; }
</style>
<form id="buscar">
  <label>Mensaje número <input id="numero" type="number" min="1"></label>
  <button>Buscar</button>
</form>
<p id="resultado"></p>
```

#### Eventos
```
escribir #numero 2
enviar #buscar
esperar 500
escribir #numero 9
enviar #buscar
```

#### Estado
```
#resultado
pedidos
```

#### Código inicial
```javascript
const form = document.querySelector('#buscar');
const numero = document.querySelector('#numero');
const resultado = document.querySelector('#resultado');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

});
```

#### Salida esperada
```
── Estado ──
#resultado: No hay ningún mensaje con el número 9.
pedidos: GET /puerto/mensajes/2 → 200
pedidos: GET /puerto/mensajes/9 → 404
```

#### Solución
```javascript
const form = document.querySelector('#buscar');
const numero = document.querySelector('#numero');
const resultado = document.querySelector('#resultado');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const respuesta = await fetch(`/puerto/mensajes/${numero.value}`);
  const datos = await respuesta.json();
  resultado.textContent = respuesta.ok ? `#${datos.id} ${datos.de}: ${datos.texto}` : datos.error;
});
```

#### Al superarla
La señora lee el mensaje de su hijo y se lo guarda de memoria. El que pidió el 9 se entera de que no existe, en vez de esperar una paloma que nunca iba a salir.

#### Imagen
- Una señora mayor con chal, en la ventanilla, leyendo emocionada un mensaje en el pizarrón.
- Detrás, un muchacho se rasca la cabeza frente a un casillero vacío con el número 9.

## S02-N02 · Escribir al Palomar

```meta
tipo: tema
padre: S02-N01
precio: 10
criatura: goblin
temas: js.formularios, web.api-rest
usa: js.fetch, arch.json
```

### Crónica

Ya se pueden leer los mensajes, pero la gente quiere **escribir**. Iara, la escribiente del Puerto, llega con su libreta atada a la muñeca. —Cada mensaje que entra tiene que llegar **bien**: con su remitente, su texto y una sola vez. Si llega mal, Pico se lo lleva. ¿Lo anotaste?

### Objetivos

- Mandar datos al Puerto con `POST` y un cuerpo en JSON.
- Mandar lo que se escribe en un formulario, y agregar a la lista lo que contestó el Puerto.
- Mostrar el error de validación del servidor (`422`).
- Evitar que un doble click mande dos veces, y pasar un formulario a JSON con `FormData`.

### Antes de empezar

- S02-N01 (la ventanilla).

### Explicación

#### Un POST con JSON
```javascript
const respuesta = await fetch('/puerto/mensajes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ de: 'Nima', texto: 'Llegué a la Feria.' }),
});
const creado = await respuesta.json();   // { id: 3, de: 'Nima', texto: '…' }
```
- `method` dice qué hacer;
- `headers` avisa en qué idioma va el cuerpo;
- `body` es **texto**: un objeto se pasa con `JSON.stringify`.

#### Lo que contesta el servidor manda
El Puerto le pone el número (`id`) al mensaje nuevo. Por eso se agrega a la lista **lo que contestó**, no lo que se mandó.

#### El 422
Si al Puerto le falta algo, contesta `422` con un `error`. La página lo muestra **tal cual**: la regla la pone el servidor.

#### Un solo envío
```javascript
boton.disabled = true;
try {
  await fetch(…);
} finally {
  boton.disabled = false;   // pase lo que pase, se vuelve a habilitar
}
```

#### De formulario a JSON
```javascript
const datos = Object.fromEntries(new FormData(form));  // { de: 'Iara', texto: '…' }
```
`FormData` junta los campos que tienen `name`.

### Código de ejemplo

```javascript
async function escribir(datos) {
  const respuesta = await fetch('/puerto/mensajes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos),
  });
  return { estado: respuesta.status, cuerpo: await respuesta.json() };
}

console.log(await escribir({ de: 'Nima', texto: 'Llegué a la Feria.' }));
console.log(await escribir({ de: 'Pico' }));
const lista = await (await fetch('/puerto/mensajes')).json();
console.log('Ahora hay', lista.length, 'mensajes');
```

### Salida esperada

```
{ estado: 201, cuerpo: { id: 3, de: 'Nima', texto: 'Llegué a la Feria.' } }
{ estado: 422, cuerpo: { error: 'Falta el texto del mensaje.' } }
Ahora hay 3 mensajes
```

### ¿Para qué sirve?

Comentar, registrarse, mandar un mensaje, subir una tarea, comprar: todo es un `POST`. Que el botón no mande dos veces evita las compras duplicadas; mostrar el error del servidor evita que alguien quede esperando sin saber qué pasó.

### Errores habituales

**Goblin: mandar el objeto sin `JSON.stringify`.** `body: { texto: 'hola' }` se manda como el texto `"[object Object]"`.

**Esqueleto: olvidarse el `Content-Type`.** Muchos servidores no entienden el cuerpo si no saben que es JSON.

**Ogro: agregar lo que se mandó.** Sin el `id` que pone el servidor, después no se lo puede borrar ni corregir.

**Troll: el botón que queda apagado.** Si el pedido falla y no hay `finally`, el botón no se vuelve a habilitar nunca.

### Micro-misión S02-N02-P1 · La primera paloma de Nima

```meta
lugar: El Palomar del Puerto, la ventanilla
personajes: Nima, Gheco, Iara
carta: POST | fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(datos) })
recompensa: xp 10, oro 10
```

#### Escena
Iara le pasa a Nima un formulario de papel. —Remitente, texto. Y después me decís qué número le tocó, que lo anoto.

#### Gheco sugiere
Mandá un `POST` a `/puerto/mensajes` con `{ de: 'Nima', texto: 'La ventanilla ya funciona.' }` y mostrá `Mensaje 3 guardado` (con el `id` que contestó el Puerto) en `#aviso`.

#### Desafío
Que el mensaje llegue al Palomar.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
</style>
<p id="aviso"></p>
```

#### Estado
```
#aviso
pedidos
```

#### Código inicial
```javascript
const aviso = document.querySelector('#aviso');
const respuesta = await fetch('/puerto/mensajes', {
  method: 'POST',
  body: { de: 'Nima', texto: 'La ventanilla ya funciona.' },
});

```

#### Salida esperada
```
── Estado ──
#aviso: Mensaje 3 guardado
pedidos: POST /puerto/mensajes → 201
```

#### Solución
```javascript
const aviso = document.querySelector('#aviso');
const respuesta = await fetch('/puerto/mensajes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ de: 'Nima', texto: 'La ventanilla ya funciona.' }),
});
const creado = await respuesta.json();
aviso.textContent = `Mensaje ${creado.id} guardado`;
```

#### Al superarla
*Mensaje 3 guardado*. Iara lo anota en la libreta. —Número tres. ¿Ves que no era tan difícil anotar?

#### Imagen
- Una paloma blanca sale volando del palomar con un sobre de lacre violeta atado a la pata.
- Iara (16 años, libreta atada a la muñeca, lápiz detrás de la oreja, abrigo cerrado) anota; Nima mira cómo se va la paloma.

### Micro-misión S02-N02-P2 · El formulario de la ventanilla

```meta
lugar: El Palomar del Puerto, la ventanilla
personajes: Nima, Gheco, Iara
carta: Formulario → POST | submit → fetch POST → li con lo que contestó → reset()
recompensa: xp 10, oro 10
```

#### Escena
Ahora le toca a la gente de la Feria. Iara pone un formulario de verdad en la ventanilla.

#### Gheco sugiere
En el `submit`, mandá el `POST` con los dos campos. Agregá a `#mensajes` un `<li>` con **lo que contestó** el Puerto (`#id de: texto`) y limpiá el formulario.

#### Desafío
Bengala manda un mensaje.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  label { display: block; margin: 4px 0; }
</style>
<form id="escribir">
  <label>De <input id="de"></label>
  <label>Texto <input id="texto"></label>
  <button>Mandar</button>
</form>
<ul id="mensajes"></ul>
```

#### Eventos
```
escribir #de Bengala
escribir #texto Esta noche hay fuegos en la explanada.
enviar #escribir
```

#### Estado
```
#mensajes li
#de @value
pedidos
```

#### Código inicial
```javascript
const form = document.querySelector('#escribir');
const de = document.querySelector('#de');
const texto = document.querySelector('#texto');
const lista = document.querySelector('#mensajes');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const li = document.createElement('li');
  li.textContent = `${de.value}: ${texto.value}`;
  lista.append(li);
});
```

#### Salida esperada
```
── Estado ──
#mensajes li: #3 Bengala: Esta noche hay fuegos en la explanada.
#de @value: (vacío)
pedidos: POST /puerto/mensajes → 201
```

#### Solución
```javascript
const form = document.querySelector('#escribir');
const de = document.querySelector('#de');
const texto = document.querySelector('#texto');
const lista = document.querySelector('#mensajes');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const respuesta = await fetch('/puerto/mensajes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ de: de.value, texto: texto.value }),
  });
  const m = await respuesta.json();
  const li = document.createElement('li');
  li.textContent = `#${m.id} ${m.de}: ${m.texto}`;
  lista.append(li);
  form.reset();
});
```

#### Al superarla
El mensaje de Bengala aparece con su número: *#3*. Iara lo anota. Esa noche, la explanada se llena de gente del Puerto.

#### Imagen
- Bengala (pirotécnica joven, antiparras de cuero, delantal grueso cerrado, pelo corto rojizo) escribe en la ventanilla.
- Al fondo, sobre el mar, fuegos artificiales de colores.

### Micro-misión S02-N02-P3 · Lo que dice el Puerto

```meta
lugar: El Palomar del Puerto, la ventanilla
personajes: Nima, Gheco, Iara
carta: 422 | if (!respuesta.ok) error.textContent = (await respuesta.json()).error
recompensa: xp 10, oro 10
```

#### Escena
Un chico manda un mensaje sin texto, solo con su nombre. La ventanilla agrega a la lista un mensaje que dice *undefined*.

#### Gheco sugiere
Si el Puerto contesta algo que no es `ok`, mostrá su `error` en `#error` y **no** agregues nada a la lista. Si está bien, borrá el error.

#### Desafío
Bruno manda uno sin texto y después lo completa.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  #error { color: #ff8a80; }
</style>
<form id="escribir">
  <input id="de" value="Bruno"> <input id="texto"> <button>Mandar</button>
</form>
<p id="error"></p>
<ul id="mensajes"></ul>
```

#### Eventos
```
enviar #escribir
esperar 500
escribir #texto ¡Hoy le gané al Goblin!
enviar #escribir
```

#### Estado
```
#error
#mensajes li
```

#### Código inicial
```javascript
const form = document.querySelector('#escribir');
const lista = document.querySelector('#mensajes');
const error = document.querySelector('#error');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const respuesta = await fetch('/puerto/mensajes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ de: form.de.value, texto: form.texto.value }),
  });
  const m = await respuesta.json();
  const li = document.createElement('li');
  li.textContent = `#${m.id} ${m.de}: ${m.texto}`;
  lista.append(li);
});
```

#### Salida esperada
```
── Estado ──
#error: (vacío)
#mensajes li: #3 Bruno: ¡Hoy le gané al Goblin!
```

#### Solución
```javascript
const form = document.querySelector('#escribir');
const lista = document.querySelector('#mensajes');
const error = document.querySelector('#error');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const respuesta = await fetch('/puerto/mensajes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ de: form.de.value, texto: form.texto.value }),
  });
  const m = await respuesta.json();
  if (!respuesta.ok) {
    error.textContent = m.error;
    return;
  }
  error.textContent = '';
  const li = document.createElement('li');
  li.textContent = `#${m.id} ${m.de}: ${m.texto}`;
  lista.append(li);
});
```

#### Al superarla
Primero aparece *Falta el texto del mensaje.*, y ningún *undefined*. Bruno lo completa y su mensaje sale con el número 3. —¡Lo vi! —grita Tati desde la Feria.

#### Imagen
- Bruno (12 años, pelo rizado, gorra al revés, chaleco rojo) escribe orgulloso en la ventanilla.
- Un cartelito rojo de luz se apaga al lado del formulario.

### Micro-misión S02-N02-P4 · El doble click de Tati

```meta
lugar: El Palomar del Puerto, la ventanilla
personajes: Nima, Gheco, Iara, Tati
carta: Un solo envío | boton.disabled = true · try { await fetch(…) } finally { boton.disabled = false }
recompensa: xp 15, monedas 5
```

#### Escena
Tati toca el botón dos veces seguidas, por las dudas. Al Palomar llegan **dos** mensajes iguales, e Iara tiene que anotarlos dos veces. —¿Lo anotaste? ¡Dos veces lo anoté!

#### Gheco sugiere
Al empezar el envío, deshabilitá el botón; al terminar (pase lo que pase), habilitalo de nuevo con `finally`. Un botón deshabilitado no envía el formulario.

#### Desafío
Tati toca dos veces seguidas: tiene que salir **un solo** `POST`, y el botón tiene que quedar habilitado al final.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  button:disabled { opacity: .4; }
</style>
<form id="escribir">
  <input id="de" value="Tati"> <input id="texto" value="Bruno hizo trampa">
  <button id="mandar">Mandar</button>
</form>
<ul id="mensajes"></ul>
```

#### Eventos
```
click #mandar
click #mandar
```

#### Estado
```
pedidos
#mandar @disabled
#mensajes li #
```

#### Código inicial
```javascript
const form = document.querySelector('#escribir');
const boton = document.querySelector('#mandar');
const lista = document.querySelector('#mensajes');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const respuesta = await fetch('/puerto/mensajes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ de: form.de.value, texto: form.texto.value }),
  });
  const m = await respuesta.json();
  const li = document.createElement('li');
  li.textContent = `#${m.id} ${m.de}: ${m.texto}`;
  lista.append(li);
});
```

#### Salida esperada
```
── Estado ──
pedidos: POST /puerto/mensajes → 201
#mandar @disabled: no
#mensajes li #: 1
```

#### Solución
```javascript
const form = document.querySelector('#escribir');
const boton = document.querySelector('#mandar');
const lista = document.querySelector('#mensajes');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  boton.disabled = true;
  try {
    const respuesta = await fetch('/puerto/mensajes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ de: form.de.value, texto: form.texto.value }),
    });
    const m = await respuesta.json();
    const li = document.createElement('li');
    li.textContent = `#${m.id} ${m.de}: ${m.texto}`;
    lista.append(li);
  } finally {
    boton.disabled = false;
  }
});
```

#### Al superarla
Una sola paloma, un solo renglón en la libreta de Iara. Tati toca el botón diez veces más, por las dudas, y el botón la ignora hasta que la paloma sale.

#### Imagen
- Tati (11 años, dos colitas, delantal amarillo) aprieta con los dos dedos un botón de bronce apagado.
- Iara, con la libreta, suspira aliviada.

### Micro-misión S02-N02-P5 · Todo el formulario de una vez

```meta
lugar: El Palomar del Puerto, la ventanilla
personajes: Nima, Gheco, Iara
carta: FormData | const datos = Object.fromEntries(new FormData(form))
recompensa: xp 15, monedas 5
```

#### Escena
El Puerto ahora recibe más datos: además del remitente y el texto, la **región** de donde escribe cada uno. Iara está harta de leer campo por campo. —¿No hay una forma de mandar todo junto?

#### Gheco sugiere
Con `Object.fromEntries(new FormData(form))` tenés un objeto con todos los campos que tienen `name`. Mandalo al **eco** del Puerto (`POST /puerto/eco`, que contesta lo que recibió) y mostrá en `#recibido` lo que contestó, como JSON (`JSON.stringify(datos.recibido)`).

#### Desafío
Lucio manda su mensaje desde la Feria.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  label { display: block; margin: 4px 0; }
  #recibido { font-family: monospace; }
</style>
<form id="escribir">
  <label>De <input name="de"></label>
  <label>Región
    <select name="region"><option>Valle</option><option>Forjas</option><option>Feria</option></select>
  </label>
  <label>Texto <input name="texto"></label>
  <button>Mandar</button>
</form>
<p id="recibido"></p>
```

#### Eventos
```
escribir [name=de] Lucio
elegir [name=region] Feria
escribir [name=texto] Los faroles ya se prenden solos.
enviar #escribir
```

#### Estado
```
#recibido
pedidos
```

#### Código inicial
```javascript
const form = document.querySelector('#escribir');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const datos = { de: form.de.value };

});
```

#### Salida esperada
```
── Estado ──
#recibido: {"de":"Lucio","region":"Feria","texto":"Los faroles ya se prenden solos."}
pedidos: POST /puerto/eco → 200
```

#### Solución
```javascript
const form = document.querySelector('#escribir');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const datos = Object.fromEntries(new FormData(form));
  const respuesta = await fetch('/puerto/eco', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos),
  });
  const eco = await respuesta.json();
  document.querySelector('#recibido').textContent = JSON.stringify(eco.recibido);
});
```

#### Al superarla
El eco del Puerto devuelve los tres campos, completos y en orden. Iara cierra la libreta por primera vez en el día.

#### Imagen
- Lucio, el farolero, escribe en la ventanilla con su vara de mecha apoyada al lado.
- El formulario de papel se dobla solo y vuela como una paloma.

## S02-N03 · Corregir y borrar

```meta
tipo: tema
padre: S02-N02
precio: 10
criatura: ogre
temas: web.api-rest, js.fetch
usa: js.dom, js.eventos
```

### Crónica

Con la ventanilla abierta, el Palomar se llena de mensajes. Algunos tienen errores («Llegó el *barko*»), otros ya no sirven, y Pico deja uno nuevo cada noche. Elefa manda una orden: *«Que cada mensaje se pueda **corregir** y **borrar** desde la ventanilla. Y que nunca, nunca, se borre uno que no era.»*

### Objetivos

- Borrar con `DELETE` y corregir con `PATCH`.
- Poner un botón de borrar en cada mensaje, con delegación y `data-id`.
- Sacar un mensaje de la lista **antes** de que conteste el Puerto, y devolverlo si falla.
- Juntar todo en una función `pedir(metodo, ruta, datos)` que maneje JSON y errores.

### Antes de empezar

- S02-N02 (escribir al Palomar) y la delegación de R02-N05.

### Explicación

#### Los otros dos métodos
```javascript
await fetch('/puerto/mensajes/2', { method: 'DELETE' });                 // 204: sin cuerpo
await fetch('/puerto/mensajes/2', {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ texto: 'Llegó el barco.' }),
});
```
`204 No Content` quiere decir «hecho, y no tengo nada que decir»: **no** se llama a `.json()`, porque no hay cuerpo.

#### El número va en el elemento
Cada `<li>` lleva su número en `data-id`, y su botón adentro. Con delegación, un solo escuchador sirve para todos:
```javascript
lista.addEventListener('click', async (e) => {
  const boton = e.target.closest('.borrar');
  if (!boton) return;
  const li = boton.closest('li');
  await fetch(`/puerto/mensajes/${li.dataset.id}`, { method: 'DELETE' });
  li.remove();
});
```

#### Primero la página, después el Puerto
Esperar al servidor para sacar un renglón hace que la página se sienta lenta. Se puede sacar **enseguida** y, si el Puerto contesta mal, volver a ponerlo en su lugar. A esto se lo llama **actualización optimista**.

#### Una función para todos los pedidos
```javascript
async function pedir(metodo, ruta, datos) {
  const opciones = { method: metodo };
  if (datos !== undefined) {
    opciones.headers = { 'Content-Type': 'application/json' };
    opciones.body = JSON.stringify(datos);
  }
  const respuesta = await fetch(ruta, opciones);
  const cuerpo = respuesta.status === 204 ? null : await respuesta.json();
  if (!respuesta.ok) throw new Error(cuerpo?.error ?? `El Puerto contestó ${respuesta.status}`);
  return cuerpo;
}
```

### Código de ejemplo

```javascript
const borrado = await fetch('/puerto/mensajes/2', { method: 'DELETE' });
console.log('DELETE del 2:', borrado.status, borrado.ok);

const corregido = await fetch('/puerto/mensajes/1', {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ texto: 'Estoy en la Feria, Sila.' }),
});
console.log('PATCH del 1:', await corregido.json());

const otraVez = await fetch('/puerto/mensajes/2', { method: 'DELETE' });
console.log('Otra vez el 2:', otraVez.status);
console.log('Quedan:', (await (await fetch('/puerto/mensajes')).json()).length);
```

### Salida esperada

```
DELETE del 2: 204 true
PATCH del 1: { id: 1, de: 'Sila', texto: 'Estoy en la Feria, Sila.' }
Otra vez el 2: 404
Quedan: 1
```

### ¿Para qué sirve?

Editar un comentario, borrar una foto, cambiar el estado de una tarea a «hecha»: todo es `PATCH` y `DELETE`. La actualización optimista es lo que hace que una app se sienta rápida aunque el servidor esté lejos.

### Errores habituales

**Troll: `.json()` en un 204.** No hay cuerpo y `json()` rompe con *Unexpected end of JSON input*.

**Ogro: borrar el que no era.** Si el número sale de la posición en la lista y no del `data-id`, después de borrar uno todos los demás se corren y se borra otro.

**Ogro: el optimista que no vuelve.** Si se saca el renglón antes de tiempo y el Puerto falla, hay que devolverlo **en el mismo lugar**, no al final.

### Micro-misión S02-N03-P1 · Borrar el de Pico

```meta
lugar: El Palomar del Puerto, la ventanilla
personajes: Nima, Gheco, Nilo, Pico
carta: DELETE | await fetch(`/puerto/mensajes/${id}`, { method: 'DELETE' }) · 204
recompensa: xp 10, oro 10
```

#### Escena
Pico volvió a dejar un mensaje: el número 3. Nilo, que defiende a las gaviotas, suspira. —Está bien. Ese se va.

#### Gheco sugiere
Borrá el mensaje 3 con `DELETE` y, si el Puerto contestó bien, volvé a pedir la lista y dibujala en `#mensajes`.

#### Desafío
Que quede la lista sin el mensaje de Pico.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  li { background: #1c335a; margin: 6px 0; padding: 8px; list-style: none; }
</style>
<ul id="mensajes"></ul>
```

#### Estado
```
#mensajes li
pedidos
```

#### Código inicial
```javascript
// Lo que dejó Pico (no lo cambies).
await fetch('/puerto/mensajes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ de: 'Pico', texto: '¡Las palomas son mías!' }),
});

const lista = document.querySelector('#mensajes');

const mensajes = await (await fetch('/puerto/mensajes')).json();
for (const m of mensajes) {
  const li = document.createElement('li');
  li.textContent = `#${m.id} ${m.de}: ${m.texto}`;
  lista.append(li);
}
```

#### Salida esperada
```
── Estado ──
#mensajes li: #1 Sila: ¿Dónde estás, Nima? Tu ficha sigue en el Archivo.
#mensajes li: #2 Tizón: Vi pasar las luces por las Forjas. Iban al norte.
pedidos: POST /puerto/mensajes → 201
pedidos: DELETE /puerto/mensajes/3 → 204
pedidos: GET /puerto/mensajes → 200
```

#### Solución
```javascript
// Lo que dejó Pico (no lo cambies).
await fetch('/puerto/mensajes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ de: 'Pico', texto: '¡Las palomas son mías!' }),
});

const lista = document.querySelector('#mensajes');

const borrado = await fetch('/puerto/mensajes/3', { method: 'DELETE' });
if (borrado.ok) {
  const mensajes = await (await fetch('/puerto/mensajes')).json();
  for (const m of mensajes) {
    const li = document.createElement('li');
    li.textContent = `#${m.id} ${m.de}: ${m.texto}`;
    lista.append(li);
  }
}
```

#### Al superarla
El mensaje de Pico desaparece del pizarrón. Pico mira desde el poste, con la cabeza ladeada, y se va a buscar pescado.

#### Imagen
- Una paloma blanca saca con el pico un sobre de un casillero y lo tira al mar; la gaviota mira ofendida desde el poste.
- Nilo, resignado, con la mano en la bufanda.

### Micro-misión S02-N03-P2 · Un botón en cada mensaje

```meta
lugar: El Palomar del Puerto, la ventanilla
personajes: Nima, Gheco, Iara
carta: Delegación | lista.addEventListener('click', e => { const li = e.target.closest('li') … li.dataset.id })
recompensa: xp 10, oro 10
```

#### Escena
—No puedo llamarte cada vez que hay que borrar uno —dice Iara—. Poné un botón en cada mensaje, y que borre **ese**.

#### Gheco sugiere
Cada `<li>` lleva `data-id` y un botón `.borrar`. Con un solo escuchador en la lista, borrá con `DELETE` el del `data-id` y, si salió bien, sacá el `<li>`.

#### Desafío
Iara borra el mensaje de Tizón (el segundo).

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  li { background: #1c335a; margin: 6px 0; padding: 8px; list-style: none; display: flex; justify-content: space-between; }
</style>
<ul id="mensajes"></ul>
```

#### Eventos
```
esperar 500
click #mensajes li:nth-child(2) .borrar
```

#### Estado
```
#mensajes li
pedidos
```

#### Código inicial
```javascript
const lista = document.querySelector('#mensajes');

const mensajes = await (await fetch('/puerto/mensajes')).json();
for (const m of mensajes) {
  const li = document.createElement('li');
  li.dataset.id = m.id;
  const texto = document.createElement('span');
  texto.textContent = `${m.de}: ${m.texto}`;
  const boton = document.createElement('button');
  boton.className = 'borrar';
  boton.textContent = '✕';
  li.append(texto, boton);
  lista.append(li);
}

```

#### Salida esperada
```
── Estado ──
#mensajes li: Sila: ¿Dónde estás, Nima? Tu ficha sigue en el Archivo.✕
pedidos: GET /puerto/mensajes → 200
pedidos: DELETE /puerto/mensajes/2 → 204
```

#### Solución
```javascript
const lista = document.querySelector('#mensajes');

const mensajes = await (await fetch('/puerto/mensajes')).json();
for (const m of mensajes) {
  const li = document.createElement('li');
  li.dataset.id = m.id;
  const texto = document.createElement('span');
  texto.textContent = `${m.de}: ${m.texto}`;
  const boton = document.createElement('button');
  boton.className = 'borrar';
  boton.textContent = '✕';
  li.append(texto, boton);
  lista.append(li);
}

lista.addEventListener('click', async (e) => {
  const boton = e.target.closest('.borrar');
  if (!boton) return;
  const li = boton.closest('li');
  const respuesta = await fetch(`/puerto/mensajes/${li.dataset.id}`, { method: 'DELETE' });
  if (respuesta.ok) li.remove();
});
```

#### Al superarla
Un toque en la cruz y el mensaje de Tizón se va, solo ese. Iara prueba con el lápiz, de lejos, por si muerde.

#### Imagen
- El pizarrón de la ventanilla con mensajes de luz, cada uno con una crucecita de bronce al costado; uno se desvanece en chispas.
- Iara toca la cruz con la punta del lápiz.

### Micro-misión S02-N03-P3 · El barko

```meta
lugar: El Palomar del Puerto, la ventanilla
personajes: Nima, Gheco, Iara, Nilo
carta: PATCH | fetch(`/puerto/mensajes/${id}`, { method: 'PATCH', headers, body: JSON.stringify({ texto }) })
recompensa: xp 10, oro 10
```

#### Escena
Nilo escribió apurado un aviso: *«Llegó el barko de las Forjas»*. Iara lo mira con la ceja levantada. —Corregilo, que lo lee todo el Puerto.

#### Gheco sugiere
Mandá un `PATCH` al mensaje 3 con el texto corregido y, con lo que contestó el Puerto, actualizá el `<li>` que tiene `data-id="3"`.

#### Desafío
Que en la lista diga `Llegó el barco de las Forjas`.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  li { background: #1c335a; margin: 6px 0; padding: 8px; list-style: none; }
</style>
<ul id="mensajes"></ul>
```

#### Estado
```
#mensajes li
pedidos
```

#### Código inicial
```javascript
// El aviso apurado de Nilo (no lo cambies).
await fetch('/puerto/mensajes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ de: 'Nilo', texto: 'Llegó el barko de las Forjas' }),
});

const lista = document.querySelector('#mensajes');
for (const m of await (await fetch('/puerto/mensajes')).json()) {
  const li = document.createElement('li');
  li.dataset.id = m.id;
  li.textContent = `${m.de}: ${m.texto}`;
  lista.append(li);
}

```

#### Salida esperada
```
── Estado ──
#mensajes li: Sila: ¿Dónde estás, Nima? Tu ficha sigue en el Archivo.
#mensajes li: Tizón: Vi pasar las luces por las Forjas. Iban al norte.
#mensajes li: Nilo: Llegó el barco de las Forjas
pedidos: POST /puerto/mensajes → 201
pedidos: GET /puerto/mensajes → 200
pedidos: PATCH /puerto/mensajes/3 → 200
```

#### Solución
```javascript
// El aviso apurado de Nilo (no lo cambies).
await fetch('/puerto/mensajes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ de: 'Nilo', texto: 'Llegó el barko de las Forjas' }),
});

const lista = document.querySelector('#mensajes');
for (const m of await (await fetch('/puerto/mensajes')).json()) {
  const li = document.createElement('li');
  li.dataset.id = m.id;
  li.textContent = `${m.de}: ${m.texto}`;
  lista.append(li);
}

const respuesta = await fetch('/puerto/mensajes/3', {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ texto: 'Llegó el barco de las Forjas' }),
});
const m = await respuesta.json();
lista.querySelector(`[data-id="${m.id}"]`).textContent = `${m.de}: ${m.texto}`;
```

#### Al superarla
El *barko* se vuelve *barco*. Nilo se pone colorado. —Lo escribí corriendo. —Iara: —¿Y lo anotaste bien? —No.

#### Imagen
- Un barco de las Forjas, con chimenea de hierro, entrando al puerto de noche.
- Nilo, colorado, se tapa la cara con la bufanda violeta; Iara le muestra la libreta.

### Micro-misión S02-N03-P4 · Volver a ponerlo

```meta
lugar: El Palomar del Puerto, la ventanilla
personajes: Nima, Gheco, Iara
carta: Optimista | const lugar = li.nextSibling · li.remove() · si falla: lista.insertBefore(li, lugar)
recompensa: xp 15, monedas 5
```

#### Escena
La ventanilla tarda en sacar los mensajes borrados: la gente toca la cruz, no pasa nada, y vuelve a tocar. Elefa quiere que se vayan **enseguida**. Pero si el Puerto no lo pudo borrar, que vuelva a aparecer, en su lugar.

#### Gheco sugiere
Al tocar la cruz, guardá el lugar (`li.nextSibling`) y sacá el `<li>` **antes** de pedir. Si el Puerto contesta mal, volvé a ponerlo con `lista.insertBefore(li, lugar)` y mostrá su `error` en `#error`.

#### Desafío
La lista tiene un mensaje viejo, el número 7, que en el Puerto ya no existe. Iara intenta borrarlo (vuelve a su lugar, con el error) y después borra el de Sila (se va).

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  li { background: #1c335a; margin: 6px 0; padding: 8px; list-style: none; }
  #error { color: #ff8a80; }
</style>
<ul id="mensajes">
  <li data-id="1">Sila: ¿Dónde estás, Nima? <button class="borrar">✕</button></li>
  <li data-id="7">Pico: (un mensaje viejo) <button class="borrar">✕</button></li>
  <li data-id="2">Tizón: Vi pasar las luces. <button class="borrar">✕</button></li>
</ul>
<p id="error"></p>
```

#### Eventos
```
click [data-id="7"] .borrar
esperar 500
click [data-id="1"] .borrar
```

#### Estado
```
#mensajes li @data-id
#error
```

#### Código inicial
```javascript
const lista = document.querySelector('#mensajes');
const error = document.querySelector('#error');

lista.addEventListener('click', async (e) => {
  const boton = e.target.closest('.borrar');
  if (!boton) return;
  const li = boton.closest('li');
  li.remove();
  await fetch(`/puerto/mensajes/${li.dataset.id}`, { method: 'DELETE' });
});
```

#### Salida esperada
```
── Estado ──
#mensajes li @data-id: 7
#mensajes li @data-id: 2
#error: No hay ningún mensaje con el número 7.
```

#### Solución
```javascript
const lista = document.querySelector('#mensajes');
const error = document.querySelector('#error');

lista.addEventListener('click', async (e) => {
  const boton = e.target.closest('.borrar');
  if (!boton) return;
  const li = boton.closest('li');
  const lugar = li.nextSibling;
  li.remove();
  const respuesta = await fetch(`/puerto/mensajes/${li.dataset.id}`, { method: 'DELETE' });
  if (!respuesta.ok) {
    lista.insertBefore(li, lugar);
    error.textContent = (await respuesta.json()).error;
  }
});
```

#### Al superarla
El mensaje 7 se va y vuelve, en el medio, como estaba, con el aviso de que el Puerto no lo tiene. El de Sila se va y no vuelve. Iara anota, sin que nadie le diga: *«El 7 hay que borrarlo a mano.»*

#### Imagen
- Un mensaje de luz que vuelve a su lugar en el pizarrón como un vidrio que se reacomoda en un vitral.
- Iara anota en su libreta, conforme.

### Micro-misión S02-N03-P5 · Una sola función para el Puerto

```meta
lugar: El Palomar del Puerto, la torre de Elefa
personajes: Nima, Gheco, Elefa
carta: pedir() | async function pedir(metodo, ruta, datos) { … if (!respuesta.ok) throw new Error(cuerpo.error) … }
recompensa: xp 15, monedas 5
```

#### Escena
Elefa sube a Nima a la torre y le muestra el código de la ventanilla. —Mucho `fetch`, mucho `headers`, mucho `JSON.stringify`, repetido. En el Puerto, todo lo repetido se hace **una vez** y se usa muchas.

#### Gheco sugiere
Completá `pedir(metodo, ruta, datos)`: si hay `datos`, mandalos en JSON; si el estado es 204, devolvé `null`; si no es `ok`, tirá un `Error` con el `error` del Puerto. Después usala para crear, corregir, borrar y listar, y atrapá el error del final.

#### Desafío
Que la consola muestre lo que hizo cada pedido.

#### Código inicial
```javascript
async function pedir(metodo, ruta, datos) {
  const respuesta = await fetch(ruta, { method: metodo });
  return respuesta.json();
}

const nuevo = await pedir('POST', '/puerto/mensajes', { de: 'Elefa', texto: 'Palomar abierto de noche.' });
console.log('Creado:', nuevo.id);
const corregido = await pedir('PATCH', `/puerto/mensajes/${nuevo.id}`, { texto: 'Palomar abierto día y noche.' });
console.log('Corregido:', corregido.texto);
console.log('Borrado:', await pedir('DELETE', '/puerto/mensajes/1'));
console.log('Quedan:', (await pedir('GET', '/puerto/mensajes')).map((m) => m.de).join(', '));
try {
  await pedir('DELETE', '/puerto/mensajes/1');
} catch (error) {
  console.log('Error:', error.message);
}
```

#### Salida esperada
```
Creado: 3
Corregido: Palomar abierto día y noche.
Borrado: null
Quedan: Tizón, Elefa
Error: No hay ningún mensaje con el número 1.
```

#### Solución
```javascript
async function pedir(metodo, ruta, datos) {
  const opciones = { method: metodo };
  if (datos !== undefined) {
    opciones.headers = { 'Content-Type': 'application/json' };
    opciones.body = JSON.stringify(datos);
  }
  const respuesta = await fetch(ruta, opciones);
  const cuerpo = respuesta.status === 204 ? null : await respuesta.json();
  if (!respuesta.ok) throw new Error(cuerpo?.error ?? `El Puerto contestó ${respuesta.status}`);
  return cuerpo;
}

const nuevo = await pedir('POST', '/puerto/mensajes', { de: 'Elefa', texto: 'Palomar abierto de noche.' });
console.log('Creado:', nuevo.id);
const corregido = await pedir('PATCH', `/puerto/mensajes/${nuevo.id}`, { texto: 'Palomar abierto día y noche.' });
console.log('Corregido:', corregido.texto);
console.log('Borrado:', await pedir('DELETE', '/puerto/mensajes/1'));
console.log('Quedan:', (await pedir('GET', '/puerto/mensajes')).map((m) => m.de).join(', '));
try {
  await pedir('DELETE', '/puerto/mensajes/1');
} catch (error) {
  console.log('Error:', error.message);
}
```

#### Al superarla
Cinco pedidos y una sola función. Elefa asiente despacio con la trompa. —Así trabaja Nilo del otro lado. Ahora ustedes dos hablan igual.

#### Imagen
- La torre de Elefa, con una ventana redonda sobre el puerto; Elefa (elefanta capitana con chaqueta de capitán abotonada y bastón) mira un pergamino con código.
- Nima, al lado, sostiene una sola flecha de luz que se divide en cinco.

## S02-N04 · Jefe: Pico y la sesión

```meta
tipo: jefe
padre: S02-N03
precio: 10
criatura: dragon
insignia: Palomera del Puerto
insignia_descripcion: Armaste la ventanilla del Palomar: leer, escribir, corregir, borrar y mandar palomas con la sesión iniciada.
temas: web.sesiones, web.auth
usa: js.fetch, web.api-rest, web.seguridad
```

### Crónica

Lo último que falta es lo más delicado: **mandar palomas** a las otras regiones. Las palomas son pocas y valiosas, así que solo pueden mandarlas los del Puerto con **sesión iniciada**. Nima tiene su usuario: `nima`, con la clave `luciernaga`.

Esa noche, Pico no se queda en el poste. Baja a la ventanilla, se esconde detrás del mostrador y espera. —Quiere la **sesión** —dice Nilo—. Si se lleva la cookie de alguien, manda palomas en su nombre. Ya lo hizo una vez en el Puerto: le robó la contraseña a Fermín, que la tenía escrita en un papel.

### Objetivos

- Iniciar sesión con `POST /puerto/login` y entender la cookie que deja el Puerto.
- Saber por qué una cookie `HttpOnly` no se ve con `document.cookie` y aun así viaja en cada pedido.
- Manejar el `401` (sin sesión) y el `422` (datos que el Puerto no acepta).
- Hacer el recorrido completo: ver si hay sesión, entrar, mandar una paloma, esperarla y salir.

### Antes de empezar

- Todo el Palomar (S02-N01 a N03) y las cookies de la Torre de las Flechas (R04).

### Explicación

#### Cómo se entra
```javascript
const respuesta = await fetch('/puerto/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }),
});
```
Si la clave es correcta, el Puerto contesta `200` y deja una cookie: `sesion=…`. Desde ahí, **cada** pedido al Puerto la lleva solo: el Puerto sabe quién es.

#### La cookie que JavaScript no ve
La cookie de sesión viene marcada **`HttpOnly`**: el navegador la guarda y la manda, pero **JavaScript no la puede leer**. `document.cookie` no la muestra. Así, aunque Pico logre meter un script en la página, no se lleva la sesión. (En el curso de PHP, la marca la pone Nilo del lado del servidor.)

#### Los dos errores
| Estado | Quiere decir | La página |
|---|---|---|
| `401` | no hay sesión, o la clave estaba mal | muestra el formulario para entrar |
| `422` | los datos no sirven (un destino que no existe) | muestra el `error` que manda el Puerto |

#### Salir
`POST /puerto/salir` borra la cookie. Una sesión abierta en una compu compartida es una puerta abierta.

> **En la caja**, el usuario es `nima` y la clave `luciernaga`. Las palomas van a `Valle`, `Forjas`, `Talleres` o `Puerto`, y cada una avisa cuánto tarda en volar (`vuelo`, en milisegundos).

### Código de ejemplo

```javascript
const sinSesion = await fetch('/puerto/perfil');
console.log('Perfil sin sesión:', sinSesion.status);

await fetch('/puerto/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }),
});
console.log('document.cookie:', JSON.stringify(document.cookie));

const perfil = await (await fetch('/puerto/perfil')).json();
console.log('Perfil con sesión:', perfil.nombre, perfil.fichas);

await fetch('/puerto/salir', { method: 'POST' });
console.log('Después de salir:', (await fetch('/puerto/perfil')).status);
```

### Salida esperada

```
Perfil sin sesión: 401
document.cookie: ""
Perfil con sesión: Nima 12
Después de salir: 401
```

### ¿Para qué sirve?

Así funciona casi todo inicio de sesión en la web: el campus, el banco, el correo. La cookie `HttpOnly`, la clave que nunca se guarda en la página y el botón de **salir** son las primeras defensas contra los Picos de verdad.

### Errores habituales

**Goblin: guardar la clave en `localStorage`.** Cualquier script de la página la lee. La sesión la maneja el servidor con su cookie; la página no guarda claves nunca.

**Troll: creer que hay sesión porque se vio el «200» una vez.** La sesión puede vencer. Cada pedido puede contestar `401`, y la página tiene que saber volver al formulario.

**Esqueleto: buscar la sesión en `document.cookie`.** No está, y está bien que no esté. Para saber si hay sesión, se le pregunta al Puerto (`/puerto/perfil`).

### Micro-misión S02-N04-P1 · Entrar al Palomar

```meta
lugar: El Palomar del Puerto, la ventanilla de los del Puerto
personajes: Nima, Gheco, Nilo
carta: login | POST /puerto/login { usuario, clave } · 200 → la cookie viaja sola
recompensa: xp 10, oro 10
```

#### Escena
Nilo abre una puertita al costado de la ventanilla: la de los del Puerto. —Usuario y clave. Y no la digas en voz alta, que Pico escucha.

#### Gheco sugiere
En el `submit`, mandá `usuario` y `clave` a `/puerto/login`. Si contesta `ok`, mostrá `Hola, nima` (el `usuario` que contestó) en `#saludo`.

#### Desafío
Nima entra con su usuario.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  label { display: block; margin: 4px 0; }
</style>
<form id="entrar">
  <label>Usuario <input id="usuario"></label>
  <label>Clave <input id="clave" type="password"></label>
  <button>Entrar</button>
</form>
<p id="saludo"></p>
```

#### Eventos
```
escribir #usuario nima
escribir #clave luciernaga
enviar #entrar
```

#### Estado
```
#saludo
cookies
```

#### Código inicial
```javascript
const form = document.querySelector('#entrar');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

});
```

#### Salida esperada
```
── Estado ──
#saludo: Hola, nima
cookies: sesion=farol-7f3a (HttpOnly)
```

#### Solución
```javascript
const form = document.querySelector('#entrar');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const respuesta = await fetch('/puerto/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ usuario: form.usuario.value, clave: form.clave.value }),
  });
  const datos = await respuesta.json();
  if (respuesta.ok) document.querySelector('#saludo').textContent = `Hola, ${datos.usuario}`;
});
```

#### Al superarla
*Hola, nima*. En el Tablero aparece la cookie `sesion`, con un candadito: **HttpOnly**. Nilo le guiña un ojo. —Esa no te la saca nadie.

#### Imagen
- Una puertita de madera con candado de bronce al costado de la ventanilla del palomar, abierta, con luz cálida adentro.
- Nilo sostiene la puerta; Nima entra; en el mostrador, un frasco con una galletita estampada (la cookie).

### Micro-misión S02-N04-P2 · Lo que Pico no ve

```meta
lugar: El Palomar del Puerto, detrás del mostrador
personajes: Nima, Gheco, Pico
carta: HttpOnly | document.cookie no la muestra · fetch('/puerto/perfil') la manda igual
recompensa: xp 10, oro 10
```

#### Escena
Pico logró meter un script chiquito en la ventanilla, uno que lee `document.cookie` para robarse la sesión. Nima lo deja correr, tranquila.

#### Gheco sugiere
Después de entrar, mostrá en `#pico` lo que ve Pico: `Pico ve: «…»` con `document.cookie`. Después pedí `/puerto/perfil` (la cookie viaja sola) y mostrá `Nima tiene 12 fichas` en `#perfil`.

#### Desafío
Que se vea que Pico no ve nada, pero el Puerto sí sabe quién es Nima.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
</style>
<p id="pico"></p>
<p id="perfil"></p>
```

#### Estado
```
#pico
#perfil
```

#### Código inicial
```javascript
await fetch('/puerto/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }),
});

```

#### Salida esperada
```
── Estado ──
#pico: Pico ve: «»
#perfil: Nima tiene 12 fichas
```

#### Solución
```javascript
await fetch('/puerto/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }),
});

document.querySelector('#pico').textContent = `Pico ve: «${document.cookie}»`;
const perfil = await (await fetch('/puerto/perfil')).json();
document.querySelector('#perfil').textContent = `${perfil.nombre} tiene ${perfil.fichas} fichas`;
```

#### Al superarla
*Pico ve: «»*. Nada. Y aun así, el Puerto contesta con el perfil de Nima. Pico sacude la cabeza, como si tuviera agua en los oídos.

#### Imagen
- La gaviota Pico con un monóculo de vidrio, mirando un frasco de galletitas vacío, desconcertada.
- Atrás, una paloma se lleva la galletita estampada en el pico, a salvo.

### Micro-misión S02-N04-P3 · La clave equivocada

```meta
lugar: El Palomar del Puerto, la puertita
personajes: Nima, Gheco, Fermín
carta: 401 | if (respuesta.status === 401) error.textContent = datos.error
recompensa: xp 10, oro 10
```

#### Escena
Fermín, el bodeguero viejo, viene a probar la puertita. Se equivoca con la clave: escribe la de antes, la que le robó Pico.

#### Gheco sugiere
Si el login contesta `401`, mostrá el `error` del Puerto en `#error` y vaciá el campo de la clave. Si sale bien, borrá el error y saludá en `#saludo`.

#### Desafío
Primero con una clave equivocada, después con la buena.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  #error { color: #ff8a80; }
</style>
<form id="entrar">
  <input id="usuario" value="nima"> <input id="clave" type="password"> <button>Entrar</button>
</form>
<p id="error"></p>
<p id="saludo"></p>
```

#### Eventos
```
escribir #clave gaviota123
enviar #entrar
esperar 600
escribir #clave luciernaga
enviar #entrar
```

#### Estado
```
#error
#saludo
#clave @value
cookies
```

#### Código inicial
```javascript
const form = document.querySelector('#entrar');
const error = document.querySelector('#error');
const saludo = document.querySelector('#saludo');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const respuesta = await fetch('/puerto/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ usuario: form.usuario.value, clave: form.clave.value }),
  });
  const datos = await respuesta.json();
  saludo.textContent = `Hola, ${datos.usuario}`;
});
```

#### Salida esperada
```
── Estado ──
#error: (vacío)
#saludo: Hola, nima
#clave @value: (vacío)
cookies: sesion=farol-7f3a (HttpOnly)
```

#### Solución
```javascript
const form = document.querySelector('#entrar');
const error = document.querySelector('#error');
const saludo = document.querySelector('#saludo');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const respuesta = await fetch('/puerto/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ usuario: form.usuario.value, clave: form.clave.value }),
  });
  const datos = await respuesta.json();
  if (respuesta.status === 401) {
    error.textContent = datos.error;
    form.clave.value = '';
    return;
  }
  error.textContent = '';
  form.clave.value = '';
  saludo.textContent = `Hola, ${datos.usuario}`;
});
```

#### Al superarla
Con la clave vieja, *Usuario o clave incorrectos.*, y el campo queda vacío. Con la buena, entra. Fermín asiente. —Bien. Que nadie vea la clave, ni siquiera escrita en la pantalla.

#### Imagen
- Fermín (anciano bodeguero, delantal de cuero cerrado, anteojos redondos, libreta de consultas) frente a la puertita, que no abre.
- Un papelito viejo con una clave tachada, tirado en el piso, y la gaviota mirándolo de lejos.

### Micro-misión S02-N04-P4 · Una paloma para el Valle

```meta
lugar: El Palomar del Puerto, el techo de las palomas
personajes: Nima, Gheco, Nilo
carta: 401 y 422 | POST /puerto/palomas { para, texto } · 401: sin sesión · 422: destino que no existe
recompensa: xp 15, monedas 5
```

#### Escena
Nilo sube con Nima al techo del Palomar, donde duermen las palomas. —Cada una sabe ir a un lugar. Si le pedís uno que no conoce, no sale.

#### Gheco sugiere
Escribí `mandarPaloma(para, texto)`: manda el `POST` a `/puerto/palomas` y muestra en `#estado` `Salió la paloma 1 al Valle` si salió, `Primero iniciá sesión.` si contesta 401, o el `error` del Puerto si contesta otra cosa. Probala tres veces: sin sesión, después de entrar con un destino que no existe (`Niebla`) y con el Valle.

#### Desafío
Que en `#historial` quede un `<li>` por cada intento, con lo que pasó.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
</style>
<p id="estado"></p>
<ul id="historial"></ul>
```

#### Estado
```
#historial li
pedidos
```

#### Código inicial
```javascript
const historial = document.querySelector('#historial');

function anotar(texto) {
  document.querySelector('#estado').textContent = texto;
  const li = document.createElement('li');
  li.textContent = texto;
  historial.append(li);
}

async function mandarPaloma(para, texto) {

}

async function entrar() {
  await fetch('/puerto/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }),
  });
}

await mandarPaloma('Valle', 'Hola, Sila.');
await entrar();
await mandarPaloma('Niebla', '¿Hay alguien?');
await mandarPaloma('Valle', 'Hola, Sila. Te escribo desde el Puerto.');
```

#### Salida esperada
```
── Estado ──
#historial li: Primero iniciá sesión.
#historial li: Las palomas no saben llegar a «Niebla». Destinos: Valle, Forjas, Talleres, Puerto.
#historial li: Salió la paloma 1 al Valle
pedidos: POST /puerto/palomas → 401
pedidos: POST /puerto/login → 200
pedidos: POST /puerto/palomas → 422
pedidos: POST /puerto/palomas → 201
```

#### Solución
```javascript
const historial = document.querySelector('#historial');

function anotar(texto) {
  document.querySelector('#estado').textContent = texto;
  const li = document.createElement('li');
  li.textContent = texto;
  historial.append(li);
}

async function mandarPaloma(para, texto) {
  const respuesta = await fetch('/puerto/palomas', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ para, texto }),
  });
  const datos = await respuesta.json();
  if (respuesta.ok) anotar(`Salió la paloma ${datos.id} al ${datos.para}`);
  else if (respuesta.status === 401) anotar('Primero iniciá sesión.');
  else anotar(datos.error);
}

async function entrar() {
  await fetch('/puerto/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }),
  });
}

await mandarPaloma('Valle', 'Hola, Sila.');
await entrar();
await mandarPaloma('Niebla', '¿Hay alguien?');
await mandarPaloma('Valle', 'Hola, Sila. Te escribo desde el Puerto.');
```

#### Al superarla
Sin sesión no sale ninguna. A la Niebla, ninguna paloma sabe llegar: se quedan quietas, con las plumas erizadas. Al Valle sale la primera, derecho, hacia el sur. Nilo la mira hasta que se pierde. —Las palomas tampoco van a la Niebla —dice bajito—. Nadie va.

#### Imagen
- El techo del palomar de noche, con una paloma blanca que sale volando hacia el sur sobre el mar, y otras quietas con las plumas erizadas mirando hacia una niebla espesa en el horizonte.
- Nilo y Nima, de espaldas, miran a la paloma irse.

### Micro-misión S02-N04-P5 · Jefe: Pico se queda sin nada

```meta
lugar: El Palomar del Puerto, la ventanilla de noche
personajes: Nima, Gheco, Nilo, Pico, Elefa
carta: La sesión completa | /perfil (¿hay sesión?) → login → palomas → esperar el vuelo → salir
recompensa: xp 50, oro 50, monedas 1
```

#### Escena
Pico tiene un plan: esperar a que alguien se olvide la sesión abierta en la ventanilla y mandar mil palomas a su nombre. —La ventanilla tiene que hacer **todo** bien —dice Elefa desde la torre—. Y cerrar la puerta al irse.

#### Gheco sugiere
1. Al empezar, preguntá `/puerto/perfil`. Si contesta `401`, mostrá el formulario (`#entrar` sin `hidden`) y `Entrá para mandar palomas` en `#estado`.
2. Al enviar el formulario, entrá. Si sale bien, escondé el formulario y mostrá el de la paloma (`#paloma`).
3. Al mandar la paloma, mostrá `Volando al Valle…` y esperá **lo que dice su `vuelo`** con un `setTimeout`. Ahí mostrá `La paloma llegó al Valle`.
4. Al llegar, salí (`POST /puerto/salir`) y volvé a mostrar el formulario de entrar.

#### Desafío
Nima entra, le manda una paloma a Sila, espera que llegue y sale. Al final no tiene que quedar ninguna cookie de sesión.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #10203a; color: #f3e9d2; padding: 16px; }
  form { margin: 8px 0; }
  #estado { color: #c7a4ff; }
</style>
<p id="estado">Un momento…</p>
<form id="entrar" hidden>
  <input id="usuario" placeholder="usuario"> <input id="clave" type="password" placeholder="clave"> <button>Entrar</button>
</form>
<form id="paloma" hidden>
  <select id="para"><option>Valle</option><option>Forjas</option><option>Talleres</option></select>
  <input id="texto" placeholder="mensaje"> <button>Mandar paloma</button>
</form>
```

#### Eventos
```
esperar 500
escribir #usuario nima
escribir #clave luciernaga
enviar #entrar
esperar 600
elegir #para Valle
escribir #texto Sila: llegué a la Feria. Estoy bien. Te escribo pronto.
enviar #paloma
esperar 2000
```

#### Estado
```
#estado
#entrar @hidden
#paloma @hidden
cookies
pedidos
```

#### Código inicial
```javascript
const estado = document.querySelector('#estado');
const entrar = document.querySelector('#entrar');
const paloma = document.querySelector('#paloma');

async function pedir(metodo, ruta, datos) {
  const opciones = { method: metodo };
  if (datos !== undefined) {
    opciones.headers = { 'Content-Type': 'application/json' };
    opciones.body = JSON.stringify(datos);
  }
  const respuesta = await fetch(ruta, opciones);
  return { estado: respuesta.status, datos: await respuesta.json() };
}

function mostrar(cual) {
  entrar.hidden = cual !== 'entrar';
  paloma.hidden = cual !== 'paloma';
}

```

#### Salida esperada
```
── Estado ──
#estado: La paloma llegó al Valle
#entrar @hidden: no
#paloma @hidden: sí
cookies: (ninguna)
pedidos: GET /puerto/perfil → 401
pedidos: POST /puerto/login → 200
pedidos: POST /puerto/palomas → 201
pedidos: POST /puerto/salir → 200
```

#### Solución
```javascript
const estado = document.querySelector('#estado');
const entrar = document.querySelector('#entrar');
const paloma = document.querySelector('#paloma');

async function pedir(metodo, ruta, datos) {
  const opciones = { method: metodo };
  if (datos !== undefined) {
    opciones.headers = { 'Content-Type': 'application/json' };
    opciones.body = JSON.stringify(datos);
  }
  const respuesta = await fetch(ruta, opciones);
  return { estado: respuesta.status, datos: await respuesta.json() };
}

function mostrar(cual) {
  entrar.hidden = cual !== 'entrar';
  paloma.hidden = cual !== 'paloma';
}

const esperar = (ms) => new Promise((listo) => setTimeout(listo, ms));

const perfil = await pedir('GET', '/puerto/perfil');
if (perfil.estado === 401) {
  mostrar('entrar');
  estado.textContent = 'Entrá para mandar palomas';
} else {
  mostrar('paloma');
  estado.textContent = `Hola, ${perfil.datos.nombre}`;
}

entrar.addEventListener('submit', async (e) => {
  e.preventDefault();
  const login = await pedir('POST', '/puerto/login', { usuario: entrar.usuario.value, clave: entrar.clave.value });
  entrar.clave.value = '';
  if (login.estado !== 200) {
    estado.textContent = login.datos.error;
    return;
  }
  mostrar('paloma');
  estado.textContent = `Hola, ${login.datos.usuario}`;
});

paloma.addEventListener('submit', async (e) => {
  e.preventDefault();
  const salida = await pedir('POST', '/puerto/palomas', { para: paloma.para.value, texto: paloma.texto.value });
  if (salida.estado !== 201) {
    estado.textContent = salida.estado === 401 ? 'Primero iniciá sesión.' : salida.datos.error;
    if (salida.estado === 401) mostrar('entrar');
    return;
  }
  estado.textContent = `Volando al ${salida.datos.para}…`;
  await esperar(salida.datos.vuelo);
  estado.textContent = `La paloma llegó al ${salida.datos.para}`;
  await pedir('POST', '/puerto/salir');
  mostrar('entrar');
});
```

#### Al superarla
La paloma sale hacia el Valle con la carta de Nima. Un segundo después, *La paloma llegó al Valle*, y la ventanilla se cierra sola: no queda ninguna sesión abierta. Pico salta al mostrador, revisa el frasco de las galletitas, el formulario y los casilleros… y no encuentra **nada**.

Por primera vez, Pico no se lleva nada del Puerto. Se queda un rato mirando a Nima y después, despacio, se posa en el hombro de Nilo. —¿Ves? —dice Nilo, feliz—. No es mala. Solo agarra lo que se deja tirado. —Elefa toca la campana de la torre tres veces.

En el Valle, esa misma noche, Sila encuentra un papelito en la ventana del Archivo: *«Estoy bien. Te escribo pronto.»* Es poco, pero es la primera noticia de Nima en años.

#### Imagen
- La ventanilla del palomar cerrada de noche, con una paloma que vuela lejos hacia el sur bajo la luna y la campana de la torre sonando.
- La gaviota Pico posada en el hombro de Nilo, tranquila; Nima sonríe; en la torre, Elefa con su bastón.
