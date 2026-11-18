# RAMA S02 · Senda del Correo Neumático: un cliente tipado del Puerto

```meta
tipo: senda
posicion: 7
```

## S02-N01 · El cliente del Correo

```meta
tipo: tema
padre: R04-N03
precio: 3
moneda: comodin
criatura: troll
temas: web.api-rest
usa: web.http, conc.async, err.validacion, err.opcionales, poo.genericos, cal.tipos
```

### Crónica

Por el tubo neumático de la Cúpula llega una cápsula con un sello de lacre violeta. Es de **Elefa**, la Capitana del Puerto: *«Rigel: el Correo Neumático une el Mirador con el Puerto, pero cada vez que algo sale mal, tu tablero se queda colgado. Una cápsula perdida, una que llega rota, una que trae otra cosa. Nima dice que vos sabés tipar. ¿Nos armás un **cliente** que no se trague nada?»*

Nima está en la Cúpula, apoyada en la baranda. —En la Feria hice la ventanilla del Palomar —dice—. Andaba, pero cada respuesta rara era una sorpresa. Con tipos, las sorpresas se ven antes.

### Objetivos

- Leer el mensaje de error que manda el Puerto (un `404` con su `error`).
- Atrapar una cápsula rota (un JSON cortado o un texto suelto).
- Escribir un `pedir<T>` genérico que recibe el guardia de lo que espera.
- Armar guardias de listas a partir de guardias de uno (`listaDe`).
- Pedir varias cosas a la vez con `Promise.all`, cada una con su tipo.

### Antes de empezar

- La Cúpula (R04): `Result<T>` (R04-N01), promesas (R04-N02) y `fetch` con guardias (R04-N03).
- Si hiciste la Senda del Palomar en JavaScript, es el mismo Puerto.

### Explicación

#### Tres cosas que pueden salir mal
| Qué pasó | Qué llega | Cómo se ve |
|---|---|---|
| el Puerto dice que no (`404`, `422`, `500`) | `respuesta.ok` es `false`, con `{ error: '…' }` | se devuelve el `error` del Puerto |
| la cápsula llegó rota | `respuesta.json()` **lanza** un `SyntaxError` | `try`/`catch` alrededor de `json()` |
| llegó otra cosa | el JSON está bien, pero no tiene la forma | el guardia dice que no |

#### Un `pedir<T>` para todo
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

async function pedir<T>(url: string, guardia: (x: unknown) => x is T): Promise<Result<T>> {
  const respuesta = await fetch(url);
  let datos: unknown;
  try {
    datos = await respuesta.json();
  } catch {
    return { ok: false, error: 'La cápsula llegó rota' };
  }
  if (!respuesta.ok) return { ok: false, error: errorDe(datos, respuesta.status) };
  if (!guardia(datos)) return { ok: false, error: 'El Puerto mandó otra forma' };
  return { ok: true, valor: datos };
}
```

El que llama le pasa **el guardia**: `pedir('/puerto/clima', esClima)` devuelve `Result<Clima>`. El tipo sale del guardia.

#### Guardias que fabrican guardias
```typescript
function listaDe<T>(guardia: (x: unknown) => x is T): (x: unknown) => x is T[] {
  return (x: unknown): x is T[] => Array.isArray(x) && x.every(guardia);
}
pedir('/puerto/heroes', listaDe(esHeroe));   // Result<Heroe[]>
```

#### Varias cápsulas a la vez
```typescript
const [puestos, clima] = await Promise.all([pedir('/puerto/puestos', listaDe(esPuesto)), pedir('/puerto/clima', esClima)]);
```
Las dos viajan juntas, y cada una conserva su tipo: `puestos` es `Result<Puesto[]>` y `clima`, `Result<Clima>`.

> **En la caja**, el Puerto es de mentira y contesta, entre otras, `/puerto/hola`, `/puerto/puestos`, `/puerto/puestos/2`, `/puerto/heroes`, `/puerto/clima`, `/puerto/roto` (un JSON cortado) y `/puerto/texto` (texto, no JSON).

### Código de ejemplo

```typescript
const roto = await fetch('/puerto/roto');
try {
  await roto.json();
} catch (e) {
  console.log('Rota:', e instanceof SyntaxError);
}
const perdido = await fetch('/puerto/puestos/9');
console.log(perdido.ok, perdido.status);
```

### Salida esperada

```
Rota: true
false 404
```

### ¿Para qué sirve?

Toda aplicación que habla con un servidor (el homebanking, el campus, una app de delivery) tiene que mostrar algo útil cuando la red falla o el servidor contesta raro. Un cliente que devuelve `Result` obliga a pensar en esos casos, y el compilador no te deja olvidarlos.

### Errores habituales

**Troll: leer la respuesta sin mirar `ok`.** Un `404` también trae JSON. Si no se mira `respuesta.ok`, el programa cree que llegó un puesto.

**Esqueleto: `json()` sin `try`.** Si la cápsula llega rota, `json()` lanza un error y el programa se corta.

**Goblin: `as Puesto` en vez de un guardia.** Le promete al compilador algo que nadie revisó.

### Micro-misión S02-N01-P1 · El puesto que no existe

```meta
lugar: La Cúpula, junto al tubo neumático
personajes: Rigel, Gheco, Nima
criatura: skeleton
carta: El error del Puerto | si !respuesta.ok, el Puerto manda { error } · 'error' in datos y typeof · si no, el número del estado
recompensa: xp 10, oro 10
```

#### Escena
Rigel le pide al Puerto el puesto número 2 y el número 9. El 9 no existe: el Puerto contesta `404` con un mensaje que explica qué pasó.

#### Gheco sugiere
Lo que llega es `unknown`. Para leer su `error`, se pregunta por partes: ¿es un objeto?, ¿no es `null`?, ¿tiene `error`?, ¿es un texto? Con `'error' in datos`, TypeScript ya deja escribir `datos.error`.

#### Desafío
Completá la pregunta en `errorDe`.

#### Pasos
1. Buscá el `___` en `errorDe`.
2. Cambialo por `if (typeof datos === 'object' && datos !== null && 'error' in datos && typeof datos.error === 'string') return datos.error;`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
interface Puesto { id: number; nombre: string; precio: number; abierto: boolean }

function esPuesto(x: unknown): x is Puesto {
  return typeof x === 'object' && x !== null && 'nombre' in x && typeof x.nombre === 'string' && 'precio' in x && typeof x.precio === 'number';
}

function errorDe(datos: unknown, estado: number): string {
  ___
  return `El Puerto contestó ${estado}`;
}

async function pedirPuesto(id: number): Promise<Result<Puesto>> {
  const respuesta = await fetch(`/puerto/puestos/${id}`);
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok) return { ok: false, error: errorDe(datos, respuesta.status) };
  return esPuesto(datos) ? { ok: true, valor: datos } : { ok: false, error: 'El Puerto mandó otra forma' };
}

for (const id of [2, 9]) {
  const r = await pedirPuesto(id);
  console.log(r.ok ? `${r.valor.nombre}: ${r.valor.precio} estrella(s)` : `✗ ${r.error}`);
}
```

#### Salida esperada
```
Pan con miel: 1 estrella(s)
✗ No hay ningún puesto con el número 9.
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
interface Puesto { id: number; nombre: string; precio: number; abierto: boolean }

function esPuesto(x: unknown): x is Puesto {
  return typeof x === 'object' && x !== null && 'nombre' in x && typeof x.nombre === 'string' && 'precio' in x && typeof x.precio === 'number';
}

function errorDe(datos: unknown, estado: number): string {
  if (typeof datos === 'object' && datos !== null && 'error' in datos && typeof datos.error === 'string') return datos.error;
  return `El Puerto contestó ${estado}`;
}

async function pedirPuesto(id: number): Promise<Result<Puesto>> {
  const respuesta = await fetch(`/puerto/puestos/${id}`);
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok) return { ok: false, error: errorDe(datos, respuesta.status) };
  return esPuesto(datos) ? { ok: true, valor: datos } : { ok: false, error: 'El Puerto mandó otra forma' };
}

for (const id of [2, 9]) {
  const r = await pedirPuesto(id);
  console.log(r.ok ? `${r.valor.nombre}: ${r.valor.precio} estrella(s)` : `✗ ${r.error}`);
}
```

#### Al superarla
El tablero muestra el mensaje del Puerto en vez de quedarse colgado. Nima asiente: —Eso es lo que la gente necesita leer.

#### Imagen
- Un tubo neumático de latón que baja del techo de la cúpula, con una cápsula abierta y un papelito con una cruz roja.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas, arco verde a la espalda) lee el papelito.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) escribe en el tablero; Gheco espía adentro del tubo.

### Micro-misión S02-N01-P2 · La cápsula rota

```meta
lugar: La Cúpula, junto al tubo neumático
personajes: Rigel, Gheco, Nima
criatura: troll
carta: try alrededor de json() | una cápsula cortada o con texto hace que json() lance · catch devuelve un Result con el error
recompensa: xp 10, oro 10
```

#### Escena
Por el tubo llegan tres cápsulas: una sana, una **cortada a la mitad** y una que trae **texto suelto**, no JSON. El tablero se cae con la segunda.

#### Gheco sugiere
`respuesta.json()` lanza un error si lo que llegó no es JSON completo. Envuelto en `try`, el `catch` devuelve un `Result` con el problema, y el programa sigue con la cápsula siguiente.

#### Desafío
Completá el `catch`.

#### Pasos
1. Tocá **Ejecutar**: se corta con la segunda cápsula.
2. En el `___` del `catch`, escribí `return { ok: false, error: 'La cápsula llegó rota' };`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

async function leerCapsula(url: string): Promise<Result<unknown>> {
  const respuesta = await fetch(url);
  try {
    return { ok: true, valor: await respuesta.json() };
  } catch {
    ___
  }
}

for (const url of ['/puerto/hola', '/puerto/roto', '/puerto/texto']) {
  const r = await leerCapsula(url);
  console.log(`${url}: ${r.ok ? 'llegó bien' : `✗ ${r.error}`}`);
}
```

#### Salida esperada
```
/puerto/hola: llegó bien
/puerto/roto: ✗ La cápsula llegó rota
/puerto/texto: ✗ La cápsula llegó rota
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

async function leerCapsula(url: string): Promise<Result<unknown>> {
  const respuesta = await fetch(url);
  try {
    return { ok: true, valor: await respuesta.json() };
  } catch {
    return { ok: false, error: 'La cápsula llegó rota' };
  }
}

for (const url of ['/puerto/hola', '/puerto/roto', '/puerto/texto']) {
  const r = await leerCapsula(url);
  console.log(`${url}: ${r.ok ? 'llegó bien' : `✗ ${r.error}`}`);
}
```

#### Al superarla
Las cápsulas rotas van a un canasto. El tablero sigue andando, y Gheco se pone a armar un rompecabezas con los pedazos.

#### Imagen
- Tres cápsulas de latón sobre la mesa: una sana, una partida al medio y una con un papel arrugado saliendo.
- Un troll de cuerda chiquito mordiendo la cápsula partida.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) tira la cápsula rota a un canasto; Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) se ríe; Gheco junta pedazos.

### Micro-misión S02-N01-P3 · Un pedir para todo

```meta
lugar: La Cúpula, junto al tubo neumático
personajes: Rigel, Gheco, Astrea
carta: pedir<T> genérico | recibe el guardia (x: unknown) => x is T · devuelve Result<T> · el tipo sale del guardia
recompensa: xp 10, oro 10
```

#### Escena
Astrea quiere el clima del Puerto para saber si esta noche se ven las estrellas. Rigel arma un solo `pedir` que sirve para cualquier cápsula: le pasa el guardia de lo que espera.

#### Gheco sugiere
`pedir<T>` hace los tres controles: que el Puerto diga que sí, que la cápsula no esté rota, y que tenga la forma. Falta el último: si el guardia dice que no, se devuelve un error.

#### Desafío
Completá el control de la forma.

#### Pasos
1. Buscá el `___` en `pedir`.
2. Cambialo por `if (!guardia(datos)) return { ok: false, error: 'El Puerto mandó otra forma' };`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
interface Clima { noche: boolean; viento: string; temperatura: number }

function esClima(x: unknown): x is Clima {
  return typeof x === 'object' && x !== null && 'noche' in x && typeof x.noche === 'boolean' && 'temperatura' in x && typeof x.temperatura === 'number';
}

async function pedir<T>(url: string, guardia: (x: unknown) => x is T): Promise<Result<T>> {
  const respuesta = await fetch(url);
  let datos: unknown;
  try {
    datos = await respuesta.json();
  } catch {
    return { ok: false, error: 'La cápsula llegó rota' };
  }
  if (!respuesta.ok) return { ok: false, error: `El Puerto contestó ${respuesta.status}` };
  ___
  return { ok: true, valor: datos };
}

const clima = await pedir('/puerto/clima', esClima);
console.log(clima.ok ? `Noche: ${clima.valor.noche} · ${clima.valor.temperatura} grados` : `✗ ${clima.error}`);

const trampa = await pedir('/puerto/hola', esClima);
console.log(trampa.ok ? 'Llegó un clima' : `✗ ${trampa.error}`);
```

#### Salida esperada
```
Noche: true · 18 grados
✗ El Puerto mandó otra forma
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
interface Clima { noche: boolean; viento: string; temperatura: number }

function esClima(x: unknown): x is Clima {
  return typeof x === 'object' && x !== null && 'noche' in x && typeof x.noche === 'boolean' && 'temperatura' in x && typeof x.temperatura === 'number';
}

async function pedir<T>(url: string, guardia: (x: unknown) => x is T): Promise<Result<T>> {
  const respuesta = await fetch(url);
  let datos: unknown;
  try {
    datos = await respuesta.json();
  } catch {
    return { ok: false, error: 'La cápsula llegó rota' };
  }
  if (!respuesta.ok) return { ok: false, error: `El Puerto contestó ${respuesta.status}` };
  if (!guardia(datos)) return { ok: false, error: 'El Puerto mandó otra forma' };
  return { ok: true, valor: datos };
}

const clima = await pedir('/puerto/clima', esClima);
console.log(clima.ok ? `Noche: ${clima.valor.noche} · ${clima.valor.temperatura} grados` : `✗ ${clima.error}`);

const trampa = await pedir('/puerto/hola', esClima);
console.log(trampa.ok ? 'Llegó un clima' : `✗ ${trampa.error}`);
```

#### Al superarla
Astrea mira el clima: noche clara, viento suave. —Esta noche abrimos la Cúpula —dice.

#### Imagen
- Un barómetro de latón con una aguja en «despejado» al lado del tubo neumático.
- Astrea (lechuza con anteojos de latón y chaleco azul) lee el barómetro.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mete una cápsula en el tubo; Gheco sopla adentro del tubo.

### Micro-misión S02-N01-P4 · Guardias de listas

```meta
lugar: La Cúpula, junto al tubo neumático
personajes: Rigel, Gheco, Nima
carta: Guardias que fabrican guardias | listaDe<T>(guardia) devuelve (x: unknown) => x is T[] · Array.isArray y every
recompensa: xp 15, monedas 5
```

#### Escena
Nima quiere la lista de héroes del Puerto, para ver si aparece su nombre. Ya existe `esHeroe`, que revisa **uno**. Rigel arma una función que, a partir de ese guardia, fabrica el guardia de **una lista**.

#### Gheco sugiere
`listaDe` recibe un guardia y devuelve otro: uno que pregunta si es un arreglo y si **todos** sus elementos pasan el primero.

#### Desafío
Completá el `return` de `listaDe`.

#### Pasos
1. Buscá el `___` en `listaDe`.
2. Cambialo por `return (x: unknown): x is T[] => Array.isArray(x) && x.every(guardia);`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
interface Heroe { nombre: string; region: string; nivel: number }

function esHeroe(x: unknown): x is Heroe {
  return typeof x === 'object' && x !== null && 'nombre' in x && typeof x.nombre === 'string' && 'nivel' in x && typeof x.nivel === 'number';
}

function listaDe<T>(guardia: (x: unknown) => x is T): (x: unknown) => x is T[] {
  ___
}

async function pedir<T>(url: string, guardia: (x: unknown) => x is T): Promise<Result<T>> {
  const respuesta = await fetch(url);
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok) return { ok: false, error: `El Puerto contestó ${respuesta.status}` };
  return guardia(datos) ? { ok: true, valor: datos } : { ok: false, error: 'El Puerto mandó otra forma' };
}

const heroes = await pedir('/puerto/heroes', listaDe(esHeroe));
if (heroes.ok) console.log(heroes.valor.map((h) => `${h.nombre} (${h.nivel})`).join(', '));

const noEsLista = await pedir('/puerto/clima', listaDe(esHeroe));
if (!noEsLista.ok) console.log(`✗ ${noEsLista.error}`);
```

#### Salida esperada
```
Mia (5), Kira (6), Nilo (4), Nima (1)
✗ El Puerto mandó otra forma
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
interface Heroe { nombre: string; region: string; nivel: number }

function esHeroe(x: unknown): x is Heroe {
  return typeof x === 'object' && x !== null && 'nombre' in x && typeof x.nombre === 'string' && 'nivel' in x && typeof x.nivel === 'number';
}

function listaDe<T>(guardia: (x: unknown) => x is T): (x: unknown) => x is T[] {
  return (x: unknown): x is T[] => Array.isArray(x) && x.every(guardia);
}

async function pedir<T>(url: string, guardia: (x: unknown) => x is T): Promise<Result<T>> {
  const respuesta = await fetch(url);
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok) return { ok: false, error: `El Puerto contestó ${respuesta.status}` };
  return guardia(datos) ? { ok: true, valor: datos } : { ok: false, error: 'El Puerto mandó otra forma' };
}

const heroes = await pedir('/puerto/heroes', listaDe(esHeroe));
if (heroes.ok) console.log(heroes.valor.map((h) => `${h.nombre} (${h.nivel})`).join(', '));

const noEsLista = await pedir('/puerto/clima', listaDe(esHeroe));
if (!noEsLista.ok) console.log(`✗ ${noEsLista.error}`);
```

#### Al superarla
Nima encuentra su nombre en la lista: nivel 1. —Eso es de cuando salí de la Feria —protesta—. Hay que actualizarlo.

#### Imagen
- Un rollo de papel largo saliendo del tubo neumático con una lista de nombres (sin texto legible) y cuatro retratitos.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro) señala uno de los retratos, ofendida.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) se aguanta la risa; Gheco enrollado en el papel.

### Micro-misión S02-N01-P5 · Dos cápsulas a la vez

```meta
lugar: La Cúpula, junto al tubo neumático
personajes: Rigel, Gheco, Astrea
carta: Promise.all tipado | [puestos, clima] = await Promise.all([...]) · viajan juntas · cada una con su tipo
recompensa: xp 15, monedas 5
```

#### Escena
Antes de bajar a la Feria a comprar aceite, Rigel quiere saber qué puestos están abiertos **y** qué tiempo hace. Manda las dos cápsulas juntas por el tubo.

#### Gheco sugiere
`Promise.all` espera a las dos a la vez. Como le pasás un arreglo con dos promesas distintas, TypeScript sabe que el resultado es una tupla: la primera es `Result<Puesto[]>` y la segunda `Result<Clima>`.

#### Desafío
Completá la línea del `Promise.all`.

#### Pasos
1. Buscá el `___`.
2. Cambialo por `await Promise.all([pedir('/puerto/puestos', listaDe(esPuesto)), pedir('/puerto/clima', esClima)])`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
interface Puesto { id: number; nombre: string; abierto: boolean }
interface Clima { temperatura: number; viento: string }

const esPuesto = (x: unknown): x is Puesto =>
  typeof x === 'object' && x !== null && 'nombre' in x && typeof x.nombre === 'string' && 'abierto' in x && typeof x.abierto === 'boolean';
const esClima = (x: unknown): x is Clima =>
  typeof x === 'object' && x !== null && 'temperatura' in x && typeof x.temperatura === 'number' && 'viento' in x && typeof x.viento === 'string';
const listaDe = <T,>(guardia: (x: unknown) => x is T) => (x: unknown): x is T[] => Array.isArray(x) && x.every(guardia);

async function pedir<T>(url: string, guardia: (x: unknown) => x is T): Promise<Result<T>> {
  const respuesta = await fetch(url);
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok) return { ok: false, error: `El Puerto contestó ${respuesta.status}` };
  return guardia(datos) ? { ok: true, valor: datos } : { ok: false, error: 'El Puerto mandó otra forma' };
}

const [puestos, clima] = ___;

if (puestos.ok && clima.ok) {
  console.log(`Abiertos: ${puestos.valor.filter((p) => p.abierto).map((p) => p.nombre).join(', ')}`);
  console.log(`Afuera: ${clima.valor.temperatura} grados, viento ${clima.valor.viento}`);
}
```

#### Salida esperada
```
Abiertos: Tiro al blanco, Pan con miel, Títeres de luz
Afuera: 18 grados, viento suave
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
interface Puesto { id: number; nombre: string; abierto: boolean }
interface Clima { temperatura: number; viento: string }

const esPuesto = (x: unknown): x is Puesto =>
  typeof x === 'object' && x !== null && 'nombre' in x && typeof x.nombre === 'string' && 'abierto' in x && typeof x.abierto === 'boolean';
const esClima = (x: unknown): x is Clima =>
  typeof x === 'object' && x !== null && 'temperatura' in x && typeof x.temperatura === 'number' && 'viento' in x && typeof x.viento === 'string';
const listaDe = <T,>(guardia: (x: unknown) => x is T) => (x: unknown): x is T[] => Array.isArray(x) && x.every(guardia);

async function pedir<T>(url: string, guardia: (x: unknown) => x is T): Promise<Result<T>> {
  const respuesta = await fetch(url);
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok) return { ok: false, error: `El Puerto contestó ${respuesta.status}` };
  return guardia(datos) ? { ok: true, valor: datos } : { ok: false, error: 'El Puerto mandó otra forma' };
}

const [puestos, clima] = await Promise.all([pedir('/puerto/puestos', listaDe(esPuesto)), pedir('/puerto/clima', esClima)]);

if (puestos.ok && clima.ok) {
  console.log(`Abiertos: ${puestos.valor.filter((p) => p.abierto).map((p) => p.nombre).join(', ')}`);
  console.log(`Afuera: ${clima.valor.temperatura} grados, viento ${clima.valor.viento}`);
}
```

#### Al superarla
Las dos cápsulas vuelven casi juntas. Astrea le da a Rigel una **estrella de latón** y una lista: aceite, tornillos y pan con miel.

#### Imagen
- Dos cápsulas de latón saliendo juntas del tubo neumático, con una nubecita de vapor.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) abre las dos cápsulas a la vez; Gheco atrapa la nubecita.

## S02-N02 · Mandar cápsulas

```meta
tipo: tema
padre: S02-N01
precio: 10
criatura: goblin
temas: web.api-rest
usa: web.http, conc.async, cal.tipos, poo.genericos
```

### Crónica

Elefa contesta por el tubo: *«¡Ahora sí! Ya leés todo lo que mandamos. Ahora quiero que también **escribas**: el Mirador tiene que poder dejar mensajes en el Palomar, corregirlos y borrarlos.»*

Nima le explica a Rigel cómo es el Palomar del Puerto: un mensaje tiene un número (`id`), quién lo manda (`de`) y el `texto`. El número lo pone el Puerto, nunca quien escribe.

### Objetivos

- Mandar un mensaje con `POST` y tipar lo que se manda: `Omit<Mensaje, 'id'>`.
- Leer el `422` (datos que el Puerto no acepta) y devolverlo como `Result`.
- Corregir con `PATCH` usando `Pick`.
- Borrar con `DELETE` y entender el `204` (sin cuerpo).

### Antes de empezar

- S02-N01: el cliente del Correo.
- Los tipos útiles (R03-N04): `Partial`, `Pick`, `Omit`.

### Explicación

#### Lo que se manda no es lo que se guarda
```typescript
interface Mensaje { id: number; de: string; texto: string }
type NuevoMensaje = Omit<Mensaje, 'id'>;          // { de: string; texto: string }
type Correccion = Pick<Mensaje, 'texto'>;         // { texto: string }
```
Si alguien intenta mandar un `id`, el compilador avisa: el número lo pone el Puerto.

#### Los métodos del Palomar
| Pedido | Qué hace | Contesta |
|---|---|---|
| `POST /puerto/mensajes` | uno nuevo | `201` con el mensaje, o `422` si falta el texto |
| `PATCH /puerto/mensajes/1` | corrige el texto | `200` con el mensaje corregido |
| `DELETE /puerto/mensajes/1` | lo borra | `204`, **sin cuerpo** |

#### Mandar con `fetch`
```typescript
await fetch('/puerto/mensajes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(nuevo),
});
```

#### El `204` no trae nada
Con `204`, `respuesta.json()` falla: no hay nada que leer. Se pregunta por el estado antes.

> **En la caja**, cada ejecución arranca con dos mensajes: el 1 (de Sila) y el 2 (de Tizón). El siguiente que se mande va a ser el 3.

### Código de ejemplo

```typescript
const r = await fetch('/puerto/mensajes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ de: 'Rigel', texto: 'Hola desde el Mirador' }),
});
console.log(r.status, await r.json());
```

### Salida esperada

```
201 { id: 3, de: 'Rigel', texto: 'Hola desde el Mirador' }
```

### ¿Para qué sirve?

Casi toda aplicación crea, cambia y borra cosas en un servidor: un posteo, un carrito, una tarea. Tipar lo que se manda (distinto de lo que se recibe) evita mandar campos que el servidor no espera o se olvida de los que sí.

### Errores habituales

**Goblin: mandar el `id`.** Con `Omit<Mensaje, 'id'>`, el compilador lo marca.

**Troll: el `body` sin `JSON.stringify`.** Se manda `[object Object]` y el Puerto no entiende.

**Esqueleto: leer el cuerpo de un `204`.** No hay cuerpo: `json()` lanza un error.

### Micro-misión S02-N02-P1 · La primera cápsula

```meta
lugar: La Cúpula, junto al tubo neumático
personajes: Rigel, Gheco, Nima
carta: POST tipado | crear(m: NuevoMensaje): Promise<Mensaje> · method, headers y body con JSON.stringify
recompensa: xp 10, oro 10
```

#### Escena
Rigel escribe su primer mensaje para el Palomar: avisarle a Elefa que el Correo ya anda.

#### Gheco sugiere
Para mandar, `fetch` lleva un segundo argumento con el método, el tipo de contenido y el cuerpo, pasado a texto con `JSON.stringify`.

#### Desafío
Completá las opciones del `fetch`.

#### Pasos
1. Buscá el `___` en `crear`.
2. Cambialo por `{ method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(m) }`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Mensaje { id: number; de: string; texto: string }
type NuevoMensaje = Omit<Mensaje, 'id'>;

const esMensaje = (x: unknown): x is Mensaje =>
  typeof x === 'object' && x !== null && 'id' in x && typeof x.id === 'number' && 'texto' in x && typeof x.texto === 'string' && 'de' in x && typeof x.de === 'string';

async function crear(m: NuevoMensaje): Promise<Mensaje> {
  const respuesta = await fetch('/puerto/mensajes', ___);
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok || !esMensaje(datos)) throw new Error(`El Palomar contestó ${respuesta.status}`);
  return datos;
}

const nuevo = await crear({ de: 'Rigel', texto: 'El Correo del Mirador ya anda.' });
console.log(`#${nuevo.id} ${nuevo.de}: ${nuevo.texto}`);
```

#### Salida esperada
```
#3 Rigel: El Correo del Mirador ya anda.
```

#### Solución
```typescript
interface Mensaje { id: number; de: string; texto: string }
type NuevoMensaje = Omit<Mensaje, 'id'>;

const esMensaje = (x: unknown): x is Mensaje =>
  typeof x === 'object' && x !== null && 'id' in x && typeof x.id === 'number' && 'texto' in x && typeof x.texto === 'string' && 'de' in x && typeof x.de === 'string';

async function crear(m: NuevoMensaje): Promise<Mensaje> {
  const respuesta = await fetch('/puerto/mensajes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(m) });
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok || !esMensaje(datos)) throw new Error(`El Palomar contestó ${respuesta.status}`);
  return datos;
}

const nuevo = await crear({ de: 'Rigel', texto: 'El Correo del Mirador ya anda.' });
console.log(`#${nuevo.id} ${nuevo.de}: ${nuevo.texto}`);
```

#### Al superarla
La cápsula sale con un silbido. Al rato vuelve otra con el número 3 y un dibujito de Elefa sonriendo.

#### Imagen
- Una cápsula de latón entrando al tubo neumático con un silbido de vapor.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) suelta la cápsula.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) mira por la ventana hacia el Puerto; Gheco se tapa las orejas.

### Micro-misión S02-N02-P2 · El número lo pone el Puerto

```meta
lugar: La Cúpula, junto al tubo neumático
personajes: Rigel, Gheco, Nima
criatura: goblin
carta: Omit en lo que se manda | NuevoMensaje = Omit<Mensaje, 'id'> · mandar un id es TS2353 · el Puerto numera
recompensa: xp 10, oro 10
```

#### Escena
Gheco quiere que su mensaje sea el número 99, que le gusta más. Lo escribió en la cápsula, y el compilador no lo deja salir.

#### Gheco sugiere
(Un poco avergonzado.) `NuevoMensaje` no tiene `id`: un objeto escrito ahí mismo no puede traer campos de más. Sacá el `id: 99,` y dejá que el Puerto ponga el número.

#### Desafío
Sacá el `id` del mensaje.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Borrá `id: 99, ` del objeto que se manda.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Mensaje { id: number; de: string; texto: string }
type NuevoMensaje = Omit<Mensaje, 'id'>;

async function crear(m: NuevoMensaje): Promise<number> {
  const respuesta = await fetch('/puerto/mensajes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(m) });
  const datos: unknown = await respuesta.json();
  return typeof datos === 'object' && datos !== null && 'id' in datos && typeof datos.id === 'number' ? datos.id : -1;
}

const numero = await crear({ id: 99, de: 'Gheco', texto: '¡Quiero el 99!' });
console.log(`El Puerto le puso el número ${numero}`);
```

#### Salida esperada
```
El Puerto le puso el número 3
```

#### Solución
```typescript
interface Mensaje { id: number; de: string; texto: string }
type NuevoMensaje = Omit<Mensaje, 'id'>;

async function crear(m: NuevoMensaje): Promise<number> {
  const respuesta = await fetch('/puerto/mensajes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(m) });
  const datos: unknown = await respuesta.json();
  return typeof datos === 'object' && datos !== null && 'id' in datos && typeof datos.id === 'number' ? datos.id : -1;
}

const numero = await crear({ de: 'Gheco', texto: '¡Quiero el 99!' });
console.log(`El Puerto le puso el número ${numero}`);
```

#### Al superarla
El mensaje de Gheco sale con el número 3. Gheco se cruza de brazos, pero Nima le promete que algún día va a llegar al 99.

#### Imagen
- Una cápsula con un «99» tachado y un «3» escrito al lado.
- Un goblin chiquito con un engranaje en la espalda escapando con el «99».
- Gheco cruzado de brazos sobre la cápsula; Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) le acaricia la cabeza; Rigel (chico flaco con pecas, antiparras de latón) sonríe.

### Micro-misión S02-N02-P3 · El mensaje vacío

```meta
lugar: La Cúpula, junto al tubo neumático
personajes: Rigel, Gheco, Astrea
criatura: troll
carta: El 422 como Result | si !respuesta.ok, se devuelve el error del Puerto · el que llama decide qué mostrar
recompensa: xp 10, oro 10
```

#### Escena
Astrea manda una cápsula sin texto, para probar. El Puerto contesta `422`: falta el texto. Rigel quiere que `crear` devuelva ese error en un `Result`, en vez de explotar.

#### Gheco sugiere
Si `respuesta.ok` es `false`, se devuelve `{ ok: false, error: … }` con el mensaje del Puerto (para eso está `errorDe`).

#### Desafío
Completá el control de `respuesta.ok`.

#### Pasos
1. Buscá el `___` en `crear`.
2. Cambialo por `if (!respuesta.ok) return { ok: false, error: errorDe(datos, respuesta.status) };`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
interface Mensaje { id: number; de: string; texto: string }
type NuevoMensaje = Omit<Mensaje, 'id'>;

const esMensaje = (x: unknown): x is Mensaje =>
  typeof x === 'object' && x !== null && 'id' in x && typeof x.id === 'number' && 'texto' in x && typeof x.texto === 'string';

function errorDe(datos: unknown, estado: number): string {
  if (typeof datos === 'object' && datos !== null && 'error' in datos && typeof datos.error === 'string') return datos.error;
  return `El Puerto contestó ${estado}`;
}

async function crear(m: NuevoMensaje): Promise<Result<Mensaje>> {
  const respuesta = await fetch('/puerto/mensajes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(m) });
  const datos: unknown = await respuesta.json();
  ___
  return esMensaje(datos) ? { ok: true, valor: datos } : { ok: false, error: 'El Puerto mandó otra forma' };
}

for (const texto of ['', 'Esta noche se abre la Cúpula.']) {
  const r = await crear({ de: 'Astrea', texto });
  console.log(r.ok ? `✓ #${r.valor.id}: ${r.valor.texto}` : `✗ ${r.error}`);
}
```

#### Salida esperada
```
✗ Falta el texto del mensaje.
✓ #3: Esta noche se abre la Cúpula.
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
interface Mensaje { id: number; de: string; texto: string }
type NuevoMensaje = Omit<Mensaje, 'id'>;

const esMensaje = (x: unknown): x is Mensaje =>
  typeof x === 'object' && x !== null && 'id' in x && typeof x.id === 'number' && 'texto' in x && typeof x.texto === 'string';

function errorDe(datos: unknown, estado: number): string {
  if (typeof datos === 'object' && datos !== null && 'error' in datos && typeof datos.error === 'string') return datos.error;
  return `El Puerto contestó ${estado}`;
}

async function crear(m: NuevoMensaje): Promise<Result<Mensaje>> {
  const respuesta = await fetch('/puerto/mensajes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(m) });
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok) return { ok: false, error: errorDe(datos, respuesta.status) };
  return esMensaje(datos) ? { ok: true, valor: datos } : { ok: false, error: 'El Puerto mandó otra forma' };
}

for (const texto of ['', 'Esta noche se abre la Cúpula.']) {
  const r = await crear({ de: 'Astrea', texto });
  console.log(r.ok ? `✓ #${r.valor.id}: ${r.valor.texto}` : `✗ ${r.error}`);
}
```

#### Al superarla
La cápsula vacía vuelve con una nota amable del Puerto. La segunda sale bien. Astrea anota: *«Un error explicado vale más que un tablero colgado.»*

#### Imagen
- Una cápsula vacía devuelta por el tubo con una nota que tiene un signo de pregunta.
- Un troll de cuerda dormido adentro de la cápsula vacía.
- Astrea (lechuza con anteojos de latón y chaleco azul) escribe en un cuaderno; Rigel (chico flaco con pecas, antiparras de latón) sostiene la nota; Gheco despierta al troll.

### Micro-misión S02-N02-P4 · Corregir sin pisar

```meta
lugar: La Cúpula, junto al tubo neumático
personajes: Rigel, Gheco, Nima
carta: PATCH con Pick | Correccion = Pick<Mensaje, 'texto'> · method: 'PATCH' a /puerto/mensajes/:id · el resto queda igual
recompensa: xp 15, monedas 5
```

#### Escena
Sila, desde el Archivo, dejó un mensaje que ya no sirve: pregunta dónde está Nima. Nima le pide a Rigel que lo **corrija**, sin cambiar quién lo mandó.

#### Gheco sugiere
`PATCH` cambia solo lo que se manda. `Correccion` es `Pick<Mensaje, 'texto'>`: solo deja mandar el texto, así nadie cambia quién lo escribió.

#### Desafío
Completá el método del pedido.

#### Pasos
1. Buscá el `___` en `corregir`.
2. Cambialo por `'PATCH'`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Mensaje { id: number; de: string; texto: string }
type Correccion = Pick<Mensaje, 'texto'>;

const esMensaje = (x: unknown): x is Mensaje =>
  typeof x === 'object' && x !== null && 'id' in x && typeof x.id === 'number' && 'texto' in x && typeof x.texto === 'string' && 'de' in x && typeof x.de === 'string';

async function corregir(id: number, cambio: Correccion): Promise<Mensaje> {
  const respuesta = await fetch(`/puerto/mensajes/${id}`, {
    method: ___,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(cambio),
  });
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok || !esMensaje(datos)) throw new Error(`El Palomar contestó ${respuesta.status}`);
  return datos;
}

const corregido = await corregir(1, { texto: 'Nima está en el Mirador, ayudando a Rigel.' });
console.log(`#${corregido.id} ${corregido.de}: ${corregido.texto}`);
```

#### Salida esperada
```
#1 Sila: Nima está en el Mirador, ayudando a Rigel.
```

#### Solución
```typescript
interface Mensaje { id: number; de: string; texto: string }
type Correccion = Pick<Mensaje, 'texto'>;

const esMensaje = (x: unknown): x is Mensaje =>
  typeof x === 'object' && x !== null && 'id' in x && typeof x.id === 'number' && 'texto' in x && typeof x.texto === 'string' && 'de' in x && typeof x.de === 'string';

async function corregir(id: number, cambio: Correccion): Promise<Mensaje> {
  const respuesta = await fetch(`/puerto/mensajes/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(cambio),
  });
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok || !esMensaje(datos)) throw new Error(`El Palomar contestó ${respuesta.status}`);
  return datos;
}

const corregido = await corregir(1, { texto: 'Nima está en el Mirador, ayudando a Rigel.' });
console.log(`#${corregido.id} ${corregido.de}: ${corregido.texto}`);
```

#### Al superarla
El mensaje de Sila se corrige, y sigue firmado por ella. Nima respira tranquila: en la Feria ya saben dónde está.

#### Imagen
- Un mensaje en papel con una línea tachada y otra escrita encima, con la firma intacta abajo.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) sonríe aliviada.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sopla la tinta; Gheco sostiene el papel.

### Micro-misión S02-N02-P5 · Borrar no trae nada

```meta
lugar: La Cúpula, junto al tubo neumático
personajes: Rigel, Gheco, Nima
criatura: skeleton
carta: DELETE y 204 | el 204 no tiene cuerpo · preguntar respuesta.status === 204 antes de json() · Result<null>
recompensa: xp 15, monedas 5
```

#### Escena
Tizón mandó un mensaje viejo que ya no hace falta: las luces que vio iban al Mirador, y ya llegaron. Rigel lo **borra**, y el tablero se cae: el Puerto contestó sin cuerpo.

#### Gheco sugiere
`DELETE` contesta `204`: todo bien, pero **sin nada adentro**. Si se llama a `json()`, falla. Se pregunta por el estado antes de leer.

#### Desafío
Agregá el control del `204`.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el `___`, escribí `if (respuesta.status === 204) return { ok: true, valor: null };`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

async function borrar(id: number): Promise<Result<null>> {
  const respuesta = await fetch(`/puerto/mensajes/${id}`, { method: 'DELETE' });
  ___
  const datos: unknown = await respuesta.json();
  const error = typeof datos === 'object' && datos !== null && 'error' in datos && typeof datos.error === 'string' ? datos.error : `El Palomar contestó ${respuesta.status}`;
  return { ok: false, error };
}

for (const id of [2, 2]) {
  const r = await borrar(id);
  console.log(r.ok ? `Borrado el ${id}` : `✗ ${r.error}`);
}
const quedan: unknown = await (await fetch('/puerto/mensajes')).json();
console.log(`Quedan: ${Array.isArray(quedan) ? quedan.length : '?'}`);
```

#### Salida esperada
```
Borrado el 2
✗ No hay ningún mensaje con el número 2.
Quedan: 1
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

async function borrar(id: number): Promise<Result<null>> {
  const respuesta = await fetch(`/puerto/mensajes/${id}`, { method: 'DELETE' });
  if (respuesta.status === 204) return { ok: true, valor: null };
  const datos: unknown = await respuesta.json();
  const error = typeof datos === 'object' && datos !== null && 'error' in datos && typeof datos.error === 'string' ? datos.error : `El Palomar contestó ${respuesta.status}`;
  return { ok: false, error };
}

for (const id of [2, 2]) {
  const r = await borrar(id);
  console.log(r.ok ? `Borrado el ${id}` : `✗ ${r.error}`);
}
const quedan: unknown = await (await fetch('/puerto/mensajes')).json();
console.log(`Quedan: ${Array.isArray(quedan) ? quedan.length : '?'}`);
```

#### Al superarla
El mensaje de Tizón desaparece del Palomar. La segunda vez, el Puerto avisa que ya no está. Elefa manda una cápsula con un solo dibujo: un pulgar arriba.

#### Imagen
- Una cápsula vacía y abierta volviendo por el tubo, con un pulgar dibujado en un papelito.
- Un esqueleto de alambre chiquito buscando adentro de la cápsula vacía.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) y Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) chocan los cinco; Gheco mira adentro del tubo.

## S02-N03 · Esperas, reintentos y páginas

```meta
tipo: tema
padre: S02-N02
precio: 10
criatura: troll
temas: conc.async
usa: web.http, web.api-rest, poo.genericos, err.excepciones, js.dom, js.formularios
```

### Crónica

Una noche de marea alta, el Correo se pone lento. Algunas cápsulas tardan una eternidad, otras vuelven vacías y hay que mandarlas de nuevo, y el registro de fichas de la Feria llega **de a pedazos**. Elefa se disculpa: *«La marea está brava. El Puerto contesta, pero a su tiempo.»*

—Un buen cliente sabe esperar —dice {mentor}—, y también sabe cuándo dejar de esperar.

### Objetivos

- Ponerle un tope de tiempo a una promesa con `Promise.race`.
- Reintentar un pedido que falla, con un genérico y `await` adentro del `try`.
- Juntar una lista que llega por páginas.
- Mostrar en la página el estado de la espera con una unión: cargando, listo o error.
- Mandar un mensaje desde un formulario y ver la lista actualizada.

### Antes de empezar

- S02-N01 y S02-N02.
- Promesas (R04-N02) y la página tipada (R04-N04).

### Explicación

#### Un tope de tiempo
```typescript
function conTope<T>(promesa: Promise<T>, ms: number): Promise<T> {
  const vencer = new Promise<never>((_, rechazar) => setTimeout(() => rechazar(new Error(`Tardó más de ${ms} ms`)), ms));
  return Promise.race([promesa, vencer]);
}
```
`Promise.race` se queda con la que termina primero. La de vencer es `Promise<never>`: nunca da un valor, solo puede fallar. Por eso la carrera sigue siendo `Promise<T>`.

#### Reintentar
```typescript
async function reintentar<T>(fn: () => Promise<T>, veces: number): Promise<T> { … }
```
Adentro del `try` tiene que ir `return await fn()`. Sin el `await`, la promesa sale del `try` antes de fallar y el `catch` no la ve.

#### Lo que llega de a páginas
`/puerto/fichas?pagina=1` devuelve `{ pagina, porPagina, total, datos }`. Se piden páginas hasta tener `total`.

#### Los estados de la espera, tipados
```typescript
type Carga<T> =
  | { estado: 'cargando' }
  | { estado: 'listo'; datos: T }
  | { estado: 'error'; mensaje: string };
```
Con un `switch` sobre `estado`, el compilador no te deja usar `datos` mientras se está cargando.

> **En la caja**, `/puerto/lento` tarda 3 segundos, `/puerto/error` siempre contesta `500` y `/puerto/fichas` tiene 12 fichas, de a 5 por página. El reloj de la caja es de mentira: las esperas no tardan de verdad.

### Código de ejemplo

```typescript
const rapida = new Promise<string>((ok) => setTimeout(() => ok('liebre'), 100));
const lenta = new Promise<string>((ok) => setTimeout(() => ok('tortuga'), 900));
console.log(await Promise.race([rapida, lenta]));
```

### Salida esperada

```
liebre
```

### ¿Para qué sirve?

Las redes fallan, y los servidores a veces tardan. Las aplicaciones buenas ponen topes, reintentan con cuidado y le muestran a la persona qué está pasando. Es la diferencia entre una pantalla en blanco y un cartel que dice «Cargando…».

### Errores habituales

**Troll: esperar para siempre.** Sin un tope, un pedido que no vuelve deja la página colgada.

**Esqueleto: `return fn()` sin `await` en el `try`.** El error se escapa del `catch` y no se reintenta.

**Ogro: pedir solo la primera página.** El resto de los datos nunca llega.

### Micro-misión S02-N03-P1 · No esperar para siempre

```meta
lugar: La Cúpula, junto al tubo neumático
personajes: Rigel, Gheco, Astrea
criatura: troll
carta: Tope con Promise.race | una Promise<never> que falla después de ms · race se queda con la primera · conTope<T>
recompensa: xp 10, oro 10
```

#### Escena
Con la marea alta, una cápsula al Puerto tarda tres segundos en volver. Astrea no quiere que el tablero se quede esperando más de uno.

#### Gheco sugiere
Se arma una promesa que **falla** después de `ms` milisegundos, y se hace correr contra la del pedido. La que termina primero gana. Como la de vencer nunca devuelve un valor, es `Promise<never>`.

#### Desafío
Completá la promesa que vence.

#### Pasos
1. Buscá el `___` en `conTope`.
2. Cambialo por ``const vencer = new Promise<never>((_, rechazar) => setTimeout(() => rechazar(new Error(`Tardó más de ${ms} ms`)), ms));``.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
function conTope<T>(promesa: Promise<T>, ms: number): Promise<T> {
  ___
  return Promise.race([promesa, vencer]);
}

for (const url of ['/puerto/hola', '/puerto/lento']) {
  try {
    const respuesta = await conTope(fetch(url), 1000);
    console.log(`${url}: llegó (${respuesta.status})`);
  } catch (e) {
    console.log(`${url}: ✗ ${e instanceof Error ? e.message : e}`);
  }
}
```

#### Salida esperada
```
/puerto/hola: llegó (200)
/puerto/lento: ✗ Tardó más de 1000 ms
```

#### Solución
```typescript
function conTope<T>(promesa: Promise<T>, ms: number): Promise<T> {
  const vencer = new Promise<never>((_, rechazar) => setTimeout(() => rechazar(new Error(`Tardó más de ${ms} ms`)), ms));
  return Promise.race([promesa, vencer]);
}

for (const url of ['/puerto/hola', '/puerto/lento']) {
  try {
    const respuesta = await conTope(fetch(url), 1000);
    console.log(`${url}: llegó (${respuesta.status})`);
  } catch (e) {
    console.log(`${url}: ✗ ${e instanceof Error ? e.message : e}`);
  }
}
```

#### Al superarla
Un relojito de arena de latón aparece al lado del tubo. Cuando se termina la arena, el tablero deja de esperar y avisa.

#### Imagen
- Un reloj de arena de latón junto al tubo neumático, con la arena casi terminada.
- Un troll de cuerda muy lento empujando una cápsula por el tubo.
- Astrea (lechuza con anteojos de latón y chaleco azul) da vuelta el reloj; Rigel (chico flaco con pecas, antiparras de latón) mira; Gheco cuenta los granos.

### Micro-misión S02-N03-P2 · Otra vez, por las dudas

```meta
lugar: La Cúpula, junto al tubo neumático
personajes: Rigel, Gheco, Nima
criatura: skeleton
carta: reintentar<T> | return await fn() adentro del try · sin el await, el catch no ve el error · después de las veces, se rinde
recompensa: xp 10, oro 10
```

#### Escena
Algunas cápsulas vuelven vacías por la marea. Nima propone mandarlas de nuevo, hasta tres veces. Rigel escribe `reintentar`, pero no reintenta nada: el error se escapa.

#### Gheco sugiere
`return fn()` devuelve la promesa **sin esperarla**: sale del `try` antes de fallar, y el `catch` no la atrapa. Con `return await fn()`, el error pasa por el `catch` y se reintenta.

#### Desafío
Agregá el `await` que falta.

#### Pasos
1. Tocá **Ejecutar**: se rinde en el primer intento.
2. Cambiá `return fn();` por `return await fn();`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
async function reintentar<T>(fn: () => Promise<T>, veces: number): Promise<T> {
  let ultimo: unknown;
  for (let i = 1; i <= veces; i++) {
    try {
      return fn();
    } catch (e) {
      ultimo = e;
      console.log(`Intento ${i}: ${e instanceof Error ? e.message : e}`);
    }
  }
  throw ultimo;
}

let vueltas = 0;
async function capsulaConMarea(): Promise<string> {
  vueltas++;
  if (vueltas < 3) throw new Error('volvió vacía');
  return 'llegó la cápsula';
}

try {
  console.log(`Resultado: ${await reintentar(capsulaConMarea, 3)}`);
} catch (e) {
  console.log(`Se rindió: ${e instanceof Error ? e.message : e}`);
}
```

#### Salida esperada
```
Intento 1: volvió vacía
Intento 2: volvió vacía
Resultado: llegó la cápsula
```

#### Solución
```typescript
async function reintentar<T>(fn: () => Promise<T>, veces: number): Promise<T> {
  let ultimo: unknown;
  for (let i = 1; i <= veces; i++) {
    try {
      return await fn();
    } catch (e) {
      ultimo = e;
      console.log(`Intento ${i}: ${e instanceof Error ? e.message : e}`);
    }
  }
  throw ultimo;
}

let vueltas = 0;
async function capsulaConMarea(): Promise<string> {
  vueltas++;
  if (vueltas < 3) throw new Error('volvió vacía');
  return 'llegó la cápsula';
}

try {
  console.log(`Resultado: ${await reintentar(capsulaConMarea, 3)}`);
} catch (e) {
  console.log(`Se rindió: ${e instanceof Error ? e.message : e}`);
}
```

#### Al superarla
A la tercera, la cápsula llega llena. Nima se ríe: —En la Feria decimos «la tercera es la vencida».

#### Imagen
- Tres cápsulas en fila: dos vacías y una llena con un papel enrollado.
- Un esqueleto de alambre chiquito sosteniendo las dos vacías.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro) levanta tres dedos; Rigel (chico flaco con pecas, antiparras de latón) abre la cápsula llena; Gheco aplaude.

### Micro-misión S02-N03-P3 · Las fichas de a pedazos

```meta
lugar: La Cúpula, junto al tubo neumático
personajes: Rigel, Gheco, Nima
criatura: ogre
carta: Páginas | Pagina<T> con total y datos · pedir mientras juntas.length < total · pagina++ en cada vuelta
recompensa: xp 10, oro 10
```

#### Escena
Nima quiere contar todas las fichas de la Feria que guarda el Puerto. El Puerto las manda **de a cinco**: hay que ir pidiendo páginas hasta tenerlas todas.

#### Gheco sugiere
Cada página dice cuántas fichas hay en total. Se pide la página 1, después la 2, y así, **mientras** lo que se juntó sea menos que el total.

#### Desafío
Completá la condición del `while`.

#### Pasos
1. Buscá el `___` en el `while`.
2. Cambialo por `juntas.length < total`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Ficha { id: number; puesto: string; valor: number }
interface Pagina<T> { pagina: number; porPagina: number; total: number; datos: T[] }

function esPagina(x: unknown): x is Pagina<Ficha> {
  return typeof x === 'object' && x !== null && 'total' in x && typeof x.total === 'number' && 'datos' in x && Array.isArray(x.datos);
}

async function todasLasFichas(): Promise<Ficha[]> {
  const juntas: Ficha[] = [];
  let pagina = 1;
  let total = Infinity;
  while (___) {
    const datos: unknown = await (await fetch(`/puerto/fichas?pagina=${pagina}`)).json();
    if (!esPagina(datos)) throw new Error('El Puerto mandó otra forma');
    console.log(`Página ${datos.pagina}: ${datos.datos.length} fichas`);
    juntas.push(...datos.datos);
    total = datos.total;
    pagina++;
  }
  return juntas;
}

const fichas = await todasLasFichas();
console.log(`Total: ${fichas.length} fichas, ${fichas.reduce((suma, f) => suma + f.valor, 0)} de valor`);
```

#### Salida esperada
```
Página 1: 5 fichas
Página 2: 5 fichas
Página 3: 2 fichas
Total: 12 fichas, 24 de valor
```

#### Solución
```typescript
interface Ficha { id: number; puesto: string; valor: number }
interface Pagina<T> { pagina: number; porPagina: number; total: number; datos: T[] }

function esPagina(x: unknown): x is Pagina<Ficha> {
  return typeof x === 'object' && x !== null && 'total' in x && typeof x.total === 'number' && 'datos' in x && Array.isArray(x.datos);
}

async function todasLasFichas(): Promise<Ficha[]> {
  const juntas: Ficha[] = [];
  let pagina = 1;
  let total = Infinity;
  while (juntas.length < total) {
    const datos: unknown = await (await fetch(`/puerto/fichas?pagina=${pagina}`)).json();
    if (!esPagina(datos)) throw new Error('El Puerto mandó otra forma');
    console.log(`Página ${datos.pagina}: ${datos.datos.length} fichas`);
    juntas.push(...datos.datos);
    total = datos.total;
    pagina++;
  }
  return juntas;
}

const fichas = await todasLasFichas();
console.log(`Total: ${fichas.length} fichas, ${fichas.reduce((suma, f) => suma + f.valor, 0)} de valor`);
```

#### Al superarla
Las doce fichas quedan juntas en la mesa. Nima las cuenta dos veces, por las dudas.

#### Imagen
- Tres cápsulas abiertas con fichas de colores, la última con solo dos.
- Un ogro de cuerda que se quedó con la primera cápsula y no suelta las otras.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) cuenta fichas; Rigel (chico flaco con pecas, antiparras de latón) le alcanza la última cápsula; Gheco apila fichas.

### Micro-misión S02-N03-P4 · Cargando…

```meta
lugar: La Cúpula, el tablero de los héroes
personajes: Rigel, Gheco, Astrea
carta: Carga<T> en la página | 'cargando' | 'listo' con datos | 'error' con mensaje · el switch solo deja usar datos cuando está listo
recompensa: xp 15, monedas 5
```

#### Escena
Astrea quiere ver en la pared de la Cúpula la lista de héroes del Puerto. Mientras la cápsula viaja, la pared tiene que decir **Cargando…**; si algo falla, el error.

#### Gheco sugiere
`pintar` recibe un `Carga<Heroe[]>` y, según el estado, muestra el cartel y la lista. Falta el caso `'listo'`: un `li` por héroe y el cartel con la cantidad.

#### Desafío
Completá el caso `'listo'`.

#### Pasos
1. Buscá el `___` en `pintar`.
2. Cambialo por ``case 'listo': cartel.textContent = `${c.datos.length} héroes`; lista.replaceChildren(...c.datos.map(itemDe)); break;``.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: Georgia, serif; background: #0b1326; color: #e8d9b0; padding: 20px; }
  #cartel { color: #f2c14e; }
</style>
<p id="cartel"></p>
<ul id="lista"></ul>
```

#### Eventos
```
esperar 1000
```

#### Estado
```
#cartel
li #
```

#### Código inicial
```typescript
interface Heroe { nombre: string; region: string; nivel: number }
type Carga<T> = { estado: 'cargando' } | { estado: 'listo'; datos: T } | { estado: 'error'; mensaje: string };

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const cartel = obtenerElemento<HTMLParagraphElement>('#cartel');
const lista = obtenerElemento<HTMLUListElement>('#lista');

function itemDe(h: Heroe): HTMLLIElement {
  const li = document.createElement('li');
  li.textContent = `${h.nombre} · ${h.region} · nivel ${h.nivel}`;
  return li;
}

function pintar(c: Carga<Heroe[]>): void {
  switch (c.estado) {
    case 'cargando': cartel.textContent = 'Cargando…'; lista.replaceChildren(); break;
    ___
    case 'error': cartel.textContent = `✗ ${c.mensaje}`; lista.replaceChildren(); break;
  }
}

pintar({ estado: 'cargando' });
try {
  const respuesta = await fetch('/puerto/heroes');
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok || !Array.isArray(datos)) throw new Error(`El Puerto contestó ${respuesta.status}`);
  pintar({ estado: 'listo', datos: datos as Heroe[] });
} catch (e) {
  pintar({ estado: 'error', mensaje: e instanceof Error ? e.message : String(e) });
}
```

#### Salida esperada
```
── Estado ──
#cartel: 4 héroes
li #: 4
```

#### Solución
```typescript
interface Heroe { nombre: string; region: string; nivel: number }
type Carga<T> = { estado: 'cargando' } | { estado: 'listo'; datos: T } | { estado: 'error'; mensaje: string };

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const cartel = obtenerElemento<HTMLParagraphElement>('#cartel');
const lista = obtenerElemento<HTMLUListElement>('#lista');

function itemDe(h: Heroe): HTMLLIElement {
  const li = document.createElement('li');
  li.textContent = `${h.nombre} · ${h.region} · nivel ${h.nivel}`;
  return li;
}

function pintar(c: Carga<Heroe[]>): void {
  switch (c.estado) {
    case 'cargando': cartel.textContent = 'Cargando…'; lista.replaceChildren(); break;
    case 'listo': cartel.textContent = `${c.datos.length} héroes`; lista.replaceChildren(...c.datos.map(itemDe)); break;
    case 'error': cartel.textContent = `✗ ${c.mensaje}`; lista.replaceChildren(); break;
  }
}

pintar({ estado: 'cargando' });
try {
  const respuesta = await fetch('/puerto/heroes');
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok || !Array.isArray(datos)) throw new Error(`El Puerto contestó ${respuesta.status}`);
  pintar({ estado: 'listo', datos: datos as Heroe[] });
} catch (e) {
  pintar({ estado: 'error', mensaje: e instanceof Error ? e.message : String(e) });
}
```

#### Al superarla
La pared dice *Cargando…* un instante, y después aparecen los cuatro héroes. Astrea le da a Rigel una **estrella de latón**.

#### Imagen
- La pared de la cúpula con un cartel de latón que cambia de «reloj de arena» a una lista de cuatro retratitos.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mira la pared; Gheco imita a un reloj de arena.

### Micro-misión S02-N03-P5 · La ventanilla del Mirador

```meta
lugar: La Cúpula, la ventanilla del Correo
personajes: Rigel, Gheco, Nima
carta: Formulario que manda | submit con preventDefault · crear(...) devuelve Result · si sale bien, se vuelve a pintar la lista; si no, el aviso
recompensa: xp 15, monedas 5
```

#### Escena
Nima pide una **ventanilla** como la del Palomar de la Feria, pero en el Mirador: un campo para escribir, un botón, y la lista de mensajes que se actualiza sola.

#### Gheco sugiere
Al enviar el formulario: se evita que la página se recargue, se llama a `crear`, y según el `Result` se vuelve a pintar la lista o se muestra el aviso. Falta la llamada a `crear`.

#### Desafío
Completá la llamada a `crear` en el `submit`.

#### Pasos
1. Buscá el `___` en el `submit`.
2. Cambialo por `const r = await crear({ de: 'Rigel', texto: campo.value.trim() });`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: Georgia, serif; background: #1a1206; color: #e8d9b0; padding: 20px; }
  input { padding: 6px; background: #2a1d0b; color: #f2c14e; border: 2px solid #8d6e3f; }
  #aviso { color: #f2c14e; }
</style>
<form>
  <input id="texto" placeholder="Tu mensaje">
  <button>Mandar</button>
</form>
<p id="aviso"></p>
<ul id="lista"></ul>
```

#### Eventos
```
escribir #texto Hola desde el Mirador
enviar form
esperar 1500
```

#### Estado
```
#aviso
li #
#texto @value
```

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
interface Mensaje { id: number; de: string; texto: string }

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const formulario = obtenerElemento<HTMLFormElement>('form');
const campo = obtenerElemento<HTMLInputElement>('#texto');
const aviso = obtenerElemento<HTMLParagraphElement>('#aviso');
const lista = obtenerElemento<HTMLUListElement>('#lista');

async function crear(m: Omit<Mensaje, 'id'>): Promise<Result<Mensaje>> {
  const respuesta = await fetch('/puerto/mensajes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(m) });
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok) return { ok: false, error: `El Palomar contestó ${respuesta.status}` };
  return { ok: true, valor: datos as Mensaje };
}

async function pintarLista(): Promise<void> {
  const datos: unknown = await (await fetch('/puerto/mensajes')).json();
  const mensajes = Array.isArray(datos) ? (datos as Mensaje[]) : [];
  lista.replaceChildren(...mensajes.map((m) => {
    const li = document.createElement('li');
    li.textContent = `${m.de}: ${m.texto}`;
    return li;
  }));
}

formulario.addEventListener('submit', async (e: SubmitEvent) => {
  e.preventDefault();
  ___
  if (r.ok) {
    aviso.textContent = `Mandado: #${r.valor.id}`;
    campo.value = '';
    await pintarLista();
  } else {
    aviso.textContent = `✗ ${r.error}`;
  }
});

await pintarLista();
```

#### Salida esperada
```
── Estado ──
#aviso: Mandado: #3
li #: 3
#texto @value: (vacío)
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
interface Mensaje { id: number; de: string; texto: string }

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const formulario = obtenerElemento<HTMLFormElement>('form');
const campo = obtenerElemento<HTMLInputElement>('#texto');
const aviso = obtenerElemento<HTMLParagraphElement>('#aviso');
const lista = obtenerElemento<HTMLUListElement>('#lista');

async function crear(m: Omit<Mensaje, 'id'>): Promise<Result<Mensaje>> {
  const respuesta = await fetch('/puerto/mensajes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(m) });
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok) return { ok: false, error: `El Palomar contestó ${respuesta.status}` };
  return { ok: true, valor: datos as Mensaje };
}

async function pintarLista(): Promise<void> {
  const datos: unknown = await (await fetch('/puerto/mensajes')).json();
  const mensajes = Array.isArray(datos) ? (datos as Mensaje[]) : [];
  lista.replaceChildren(...mensajes.map((m) => {
    const li = document.createElement('li');
    li.textContent = `${m.de}: ${m.texto}`;
    return li;
  }));
}

formulario.addEventListener('submit', async (e: SubmitEvent) => {
  e.preventDefault();
  const r = await crear({ de: 'Rigel', texto: campo.value.trim() });
  if (r.ok) {
    aviso.textContent = `Mandado: #${r.valor.id}`;
    campo.value = '';
    await pintarLista();
  } else {
    aviso.textContent = `✗ ${r.error}`;
  }
});

await pintarLista();
```

#### Al superarla
El mensaje de Rigel aparece al final de la lista, debajo de los de Sila y Tizón. Nima se emociona: —Es la ventanilla de la Feria, pero en el cielo.

#### Imagen
- Una ventanilla de latón con un mostrador, un campo de texto y una lista de mensajes en papelitos colgados.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) apoyada en el mostrador.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) aprieta el botón de mandar; Gheco cuelga un papelito.

## S02-N04 · Jefe: el Autómata Falsificador

```meta
tipo: jefe
padre: S02-N03
precio: 10
criatura: dragon
insignia: Sello del Correo Neumático
insignia_descripcion: Venciste al Autómata Falsificador: un cliente tipado del Puerto que revisa todo, con la sesión cuidada de punta a punta.
temas: web.sesiones, web.auth
usa: web.api-rest, web.http, conc.async, err.validacion, web.seguridad
```

### Crónica

Una noche, las cápsulas empiezan a llegar **raras**. Una dice ser de Elefa, pero el sello está torcido. Otra trae un perfil que no tiene nombre. Nima baja al cuarto de máquinas del tubo y lo encuentra: un autómata flaco de latón, con brazos de pinza y un sello falso en la mano. Es **el Autómata Falsificador**: abre las cápsulas en el camino, cambia lo que dicen y las vuelve a cerrar.

—Quiere las **palomas** del Puerto —dice Nima—. Solo se mandan con sesión iniciada. Si consigue una sesión, manda mensajes en nombre de cualquiera.

Elefa le prestó a Nima su usuario del Palomar para ayudar desde el Mirador: `nima`, con la clave `luciernaga`.

### Objetivos

- Iniciar sesión con `POST /puerto/login` y devolver el resultado como `Result`.
- Describir la sesión con una unión: afuera o adentro.
- Entender por qué la cookie `HttpOnly` no se ve con `document.cookie`.
- Limitar los destinos de las palomas con una unión de regiones.
- No creer en ninguna cápsula sin pasarla por un guardia.

### Antes de empezar

- Toda la Senda del Correo (S02-N01 a N03).

### Explicación

#### Entrar y saber quién sos
```typescript
type Sesion = { estado: 'afuera' } | { estado: 'adentro'; nombre: string; fichas: number };
```
`/puerto/perfil` contesta `401` si no hay sesión, y el perfil si la hay.

#### La cookie que no se ve
El Puerto deja la sesión en una cookie `HttpOnly`: el navegador la manda sola en cada pedido, pero **JavaScript no la puede leer**. Si el Falsificador logra meter un script, no se la lleva.

#### Los destinos, tipados
```typescript
type Region = 'Valle' | 'Forjas' | 'Talleres' | 'Puerto';
```
El Puerto contesta `422` si el destino no existe. Con el tipo, el error se ve antes de mandar.

#### Las trampas del Falsificador (y la verdad)
| El Falsificador dice… | La verdad |
|---|---|
| "poné `as Perfil` y listo" | `as` no revisa: un guardia sí |
| "la sesión está en `document.cookie`" | es `HttpOnly`: hay que preguntarle al Puerto |
| "mandá la paloma a la Feria" | las palomas solo van a cuatro regiones |
| "dejá la sesión abierta, total…" | se sale con `POST /puerto/salir` |

> **En la caja**, el usuario es `nima` y la clave `luciernaga`. Las palomas van a `Valle`, `Forjas`, `Talleres` o `Puerto`, y la respuesta dice cuánto tarda en volar (`vuelo`, en milisegundos).

### Micro-misión S02-N04-P1 · Entrar al Palomar

```meta
lugar: El cuarto de máquinas del tubo neumático
personajes: Rigel, Gheco, Nima, el Autómata Falsificador
criatura: goblin
carta: Trampa 1 | POST /puerto/login con { usuario, clave } · 200 es adentro · 401 es la clave mala · Result<string>
recompensa: xp 15, monedas 3
```

#### Escena
El Falsificador probó claves toda la noche. Rigel arma la función que entra al Palomar con el usuario de Nima, y la prueba con una clave equivocada primero.

#### Gheco sugiere
El cuerpo del pedido lleva el usuario y la clave en JSON. Con `{ usuario, clave }` se arma el objeto con esos dos nombres.

#### Desafío
Completá el cuerpo del pedido.

#### Pasos
1. Buscá el `___` en `entrar`.
2. Cambialo por `JSON.stringify({ usuario, clave })`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

async function entrar(usuario: string, clave: string): Promise<Result<string>> {
  const respuesta = await fetch('/puerto/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: ___,
  });
  const datos: unknown = await respuesta.json();
  if (respuesta.ok && typeof datos === 'object' && datos !== null && 'usuario' in datos && typeof datos.usuario === 'string') {
    return { ok: true, valor: datos.usuario };
  }
  const error = typeof datos === 'object' && datos !== null && 'error' in datos && typeof datos.error === 'string' ? datos.error : `El Puerto contestó ${respuesta.status}`;
  return { ok: false, error };
}

for (const clave of ['engranaje', 'luciernaga']) {
  const r = await entrar('nima', clave);
  console.log(r.ok ? `Entró: ${r.valor}` : `✗ ${r.error}`);
}
```

#### Salida esperada
```
✗ Usuario o clave incorrectos.
Entró: nima
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

async function entrar(usuario: string, clave: string): Promise<Result<string>> {
  const respuesta = await fetch('/puerto/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ usuario, clave }),
  });
  const datos: unknown = await respuesta.json();
  if (respuesta.ok && typeof datos === 'object' && datos !== null && 'usuario' in datos && typeof datos.usuario === 'string') {
    return { ok: true, valor: datos.usuario };
  }
  const error = typeof datos === 'object' && datos !== null && 'error' in datos && typeof datos.error === 'string' ? datos.error : `El Puerto contestó ${respuesta.status}`;
  return { ok: false, error };
}

for (const clave of ['engranaje', 'luciernaga']) {
  const r = await entrar('nima', clave);
  console.log(r.ok ? `Entró: ${r.valor}` : `✗ ${r.error}`);
}
```

#### Al superarla
La puerta del Palomar se abre para Nima. El Falsificador, escondido entre los caños, anota algo con su pinza.

#### Imagen
- El cuarto de máquinas del tubo neumático: caños de latón, válvulas y vapor.
- Un autómata flaco de latón con brazos de pinza y un sello de lacre falso, escondido entre los caños.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas, arco verde) mira de reojo; Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) escribe en un tablero portátil; Gheco señala al autómata.

### Micro-misión S02-N04-P2 · ¿Adentro o afuera?

```meta
lugar: El cuarto de máquinas del tubo neumático
personajes: Rigel, Gheco, Nima, el Autómata Falsificador
criatura: skeleton
carta: Trampa 2 | Sesion = afuera | adentro con nombre y fichas · 401 es afuera · document.cookie no muestra la sesión HttpOnly
recompensa: xp 15, monedas 3
```

#### Escena
El Falsificador le susurra a Rigel: *«Para saber si hay sesión, mirá `document.cookie`»*. Rigel mira: está vacío. Pero la sesión **está**: la cookie es `HttpOnly`. Para saberlo, hay que preguntarle al Puerto.

#### Gheco sugiere
`quienSoy` pregunta a `/puerto/perfil`. Si contesta `401`, se está afuera. Falta esa línea.

#### Desafío
Completá el caso `401`.

#### Pasos
1. Buscá el `___` en `quienSoy`.
2. Cambialo por `if (respuesta.status === 401) return { estado: 'afuera' };`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Sesion = { estado: 'afuera' } | { estado: 'adentro'; nombre: string; fichas: number };

async function quienSoy(): Promise<Sesion> {
  const respuesta = await fetch('/puerto/perfil');
  ___
  const datos: unknown = await respuesta.json();
  if (typeof datos === 'object' && datos !== null && 'nombre' in datos && typeof datos.nombre === 'string' && 'fichas' in datos && typeof datos.fichas === 'number') {
    return { estado: 'adentro', nombre: datos.nombre, fichas: datos.fichas };
  }
  throw new Error('El Puerto mandó otra forma');
}

function describir(s: Sesion): string {
  return s.estado === 'adentro' ? `adentro: ${s.nombre} con ${s.fichas} fichas` : 'afuera';
}

console.log(describir(await quienSoy()));
await fetch('/puerto/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }) });
console.log(`document.cookie: ${JSON.stringify(document.cookie)}`);
console.log(describir(await quienSoy()));
```

#### Salida esperada
```
afuera
document.cookie: ""
adentro: Nima con 12 fichas
```

#### Solución
```typescript
type Sesion = { estado: 'afuera' } | { estado: 'adentro'; nombre: string; fichas: number };

async function quienSoy(): Promise<Sesion> {
  const respuesta = await fetch('/puerto/perfil');
  if (respuesta.status === 401) return { estado: 'afuera' };
  const datos: unknown = await respuesta.json();
  if (typeof datos === 'object' && datos !== null && 'nombre' in datos && typeof datos.nombre === 'string' && 'fichas' in datos && typeof datos.fichas === 'number') {
    return { estado: 'adentro', nombre: datos.nombre, fichas: datos.fichas };
  }
  throw new Error('El Puerto mandó otra forma');
}

function describir(s: Sesion): string {
  return s.estado === 'adentro' ? `adentro: ${s.nombre} con ${s.fichas} fichas` : 'afuera';
}

console.log(describir(await quienSoy()));
await fetch('/puerto/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }) });
console.log(`document.cookie: ${JSON.stringify(document.cookie)}`);
console.log(describir(await quienSoy()));
```

#### Al superarla
La sesión está, aunque no se vea. El Falsificador se rasca la cabeza de latón: la cookie que buscaba no se puede leer.

#### Imagen
- Una galletita de latón (la cookie) adentro de una caja de vidrio con candado, que el autómata no puede abrir.
- Un esqueleto de alambre chiquito intentando abrir el candado.
- El autómata flaco de latón con brazos de pinza, frustrado; Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) y Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) se miran cómplices; Gheco sentado sobre la caja.

### Micro-misión S02-N04-P3 · Una paloma a ninguna parte

```meta
lugar: El cuarto de máquinas del tubo neumático
personajes: Rigel, Gheco, Nima, el Autómata Falsificador
criatura: goblin
carta: Trampa 3 | type Region = 'Valle' | 'Forjas' | 'Talleres' | 'Puerto' · 'Feria' no es una Region (TS2345) · el error se ve antes de mandar
recompensa: xp 15, monedas 3
```

#### Escena
El Falsificador cambió el destino de la paloma de Nima: dice **Feria**, que no es una región del Palomar. La Feria está dentro de los Talleres.

#### Gheco sugiere
`mandarPaloma` solo acepta una `Region`. Leé el error del compilador y cambiá el destino por `'Talleres'`.

#### Desafío
Corregí el destino.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `'Feria'` por `'Talleres'`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Region = 'Valle' | 'Forjas' | 'Talleres' | 'Puerto';
interface Paloma { id: number; para: Region; texto: string; vuelo: number }

async function mandarPaloma(para: Region, texto: string): Promise<Paloma> {
  const respuesta = await fetch('/puerto/palomas', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ para, texto }) });
  if (!respuesta.ok) throw new Error(`El Palomar contestó ${respuesta.status}`);
  return (await respuesta.json()) as Paloma;
}

await fetch('/puerto/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }) });
const paloma = await mandarPaloma('Feria', 'Sila: estoy en el Mirador. Vuelvo pronto.');
console.log(`Paloma #${paloma.id} a ${paloma.para}: vuela ${paloma.vuelo} ms`);
```

#### Salida esperada
```
Paloma #1 a Talleres: vuela 3000 ms
```

#### Solución
```typescript
type Region = 'Valle' | 'Forjas' | 'Talleres' | 'Puerto';
interface Paloma { id: number; para: Region; texto: string; vuelo: number }

async function mandarPaloma(para: Region, texto: string): Promise<Paloma> {
  const respuesta = await fetch('/puerto/palomas', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ para, texto }) });
  if (!respuesta.ok) throw new Error(`El Palomar contestó ${respuesta.status}`);
  return (await respuesta.json()) as Paloma;
}

await fetch('/puerto/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }) });
const paloma = await mandarPaloma('Talleres', 'Sila: estoy en el Mirador. Vuelvo pronto.');
console.log(`Paloma #${paloma.id} a ${paloma.para}: vuela ${paloma.vuelo} ms`);
```

#### Al superarla
La paloma de latón sale por la ventana rumbo a los Talleres, y de ahí a la Feria. El Falsificador se queda con el papelito de «Feria» en la pinza.

#### Imagen
- Una paloma mecánica de latón saliendo por una ventana redonda hacia un cielo nocturno.
- Un goblin chiquito con un engranaje en la espalda sosteniendo un cartelito tachado.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro) despide a la paloma; Rigel (chico flaco con pecas, antiparras de latón) cierra la ventana; Gheco saluda.

### Micro-misión S02-N04-P4 · La cápsula falsa

```meta
lugar: El cuarto de máquinas del tubo neumático
personajes: Rigel, Gheco, Nima, el Autómata Falsificador
criatura: ogre
carta: Trampa 4 | as Perfil no revisa · el guardia esPerfil sí · la cápsula falsa no pasa, la verdadera sí
recompensa: xp 15, monedas 3
```

#### Escena
El Falsificador cambió la dirección de una cápsula: en vez de traer el perfil, trae el eco de otra cosa. El programa la abre con `as Perfil` y explota al leer el nombre.

#### Gheco sugiere
`as Perfil` le dice al compilador «confiá», pero no revisa nada. Con el guardia `esPerfil`, la cápsula falsa se detecta y se avisa.

#### Desafío
Cambiá el `as` por el guardia.

#### Pasos
1. Tocá **Ejecutar**: explota al leer el nombre.
2. Cambiá `const perfil = (await respuesta.json()) as Perfil;` por `const perfil: unknown = await respuesta.json();`.
3. En el renglón de abajo, en el `___`, escribí `if (!esPerfil(perfil)) return '✗ Cápsula falsa: no es un perfil';`.
4. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Perfil { usuario: string; nombre: string; fichas: number }

function esPerfil(x: unknown): x is Perfil {
  return typeof x === 'object' && x !== null && 'nombre' in x && typeof x.nombre === 'string' && 'fichas' in x && typeof x.fichas === 'number';
}

async function leerPerfil(url: string, metodo: string): Promise<string> {
  const respuesta = await fetch(url, { method: metodo });
  const perfil = (await respuesta.json()) as Perfil;
  ___
  return `${perfil.nombre.toUpperCase()} · ${perfil.fichas} fichas`;
}

await fetch('/puerto/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }) });
console.log(await leerPerfil('/puerto/eco', 'POST'));
console.log(await leerPerfil('/puerto/perfil', 'GET'));
```

#### Salida esperada
```
✗ Cápsula falsa: no es un perfil
NIMA · 12 fichas
```

#### Solución
```typescript
interface Perfil { usuario: string; nombre: string; fichas: number }

function esPerfil(x: unknown): x is Perfil {
  return typeof x === 'object' && x !== null && 'nombre' in x && typeof x.nombre === 'string' && 'fichas' in x && typeof x.fichas === 'number';
}

async function leerPerfil(url: string, metodo: string): Promise<string> {
  const respuesta = await fetch(url, { method: metodo });
  const perfil: unknown = await respuesta.json();
  if (!esPerfil(perfil)) return '✗ Cápsula falsa: no es un perfil';
  return `${perfil.nombre.toUpperCase()} · ${perfil.fichas} fichas`;
}

await fetch('/puerto/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }) });
console.log(await leerPerfil('/puerto/eco', 'POST'));
console.log(await leerPerfil('/puerto/perfil', 'GET'));
```

#### Al superarla
La cápsula falsa queda marcada con una cruz roja. El sello torcido del Falsificador ya no engaña a nadie.

#### Imagen
- Dos cápsulas sobre la mesa: una con un sello de lacre torcido y una cruz roja, otra con el sello violeta de Elefa.
- Un ogro de cuerda que había traído la cápsula falsa, mirando para otro lado.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) compara los sellos con la lupa; Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) cruza los brazos; Gheco tapa la cápsula falsa.

### Micro-misión S02-N04-P5 · Jefe: el Falsificador sin sello

```meta
lugar: El cuarto de máquinas del tubo neumático
personajes: Rigel, Gheco, Nima, Elefa, el Autómata Falsificador
carta: La sesión completa | quienSoy → entrar → paloma → esperar el vuelo → salir → quienSoy · nada queda abierto
recompensa: xp 50, oro 50, monedas 1
```

#### Escena
El Falsificador tiene un último plan: esperar a que alguien deje la sesión abierta en el tablero del Mirador y mandar mil palomas en su nombre. —Hacé todo el recorrido —dice Elefa por el tubo—. Y al final, **cerrá la puerta**.

#### Gheco sugiere
Junta toda la Senda:
1. `quienSoy()`: afuera.
2. Entrar con el usuario de Nima.
3. Mandar una paloma a las Forjas, para Tizón.
4. Esperar el vuelo.
5. **Salir** con `POST /puerto/salir`.
6. `quienSoy()`: afuera otra vez.

Falta el paso 5.

#### Desafío
Agregá la salida.

#### Pasos
1. Buscá el `___`.
2. Cambialo por `await fetch('/puerto/salir', { method: 'POST' });`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Region = 'Valle' | 'Forjas' | 'Talleres' | 'Puerto';
type Sesion = { estado: 'afuera' } | { estado: 'adentro'; nombre: string };
interface Paloma { id: number; para: Region; vuelo: number }

const json = { 'Content-Type': 'application/json' };
const esperar = (ms: number) => new Promise<void>((listo) => setTimeout(listo, ms));

async function quienSoy(): Promise<Sesion> {
  const respuesta = await fetch('/puerto/perfil');
  if (respuesta.status === 401) return { estado: 'afuera' };
  const datos: unknown = await respuesta.json();
  if (typeof datos === 'object' && datos !== null && 'nombre' in datos && typeof datos.nombre === 'string') return { estado: 'adentro', nombre: datos.nombre };
  throw new Error('El Puerto mandó otra forma');
}

function esPaloma(x: unknown): x is Paloma {
  return typeof x === 'object' && x !== null && 'id' in x && typeof x.id === 'number' && 'vuelo' in x && typeof x.vuelo === 'number';
}

async function mandarPaloma(para: Region, texto: string): Promise<Paloma> {
  const respuesta = await fetch('/puerto/palomas', { method: 'POST', headers: json, body: JSON.stringify({ para, texto }) });
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok || !esPaloma(datos)) throw new Error(`El Palomar contestó ${respuesta.status}`);
  return datos;
}

const decir = (s: Sesion) => (s.estado === 'adentro' ? `adentro (${s.nombre})` : 'afuera');

console.log(`1. ${decir(await quienSoy())}`);
const entrada = await fetch('/puerto/login', { method: 'POST', headers: json, body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }) });
console.log(`2. login: ${entrada.status} · ${decir(await quienSoy())}`);
const paloma = await mandarPaloma('Forjas', 'Tizón: las luces llegaron al Mirador.');
console.log(`3. paloma #${paloma.id} a ${paloma.para}`);
await esperar(paloma.vuelo);
console.log(`4. llegó después de ${paloma.vuelo} ms`);
___
console.log(`5. ${decir(await quienSoy())}`);
```

#### Salida esperada
```
1. afuera
2. login: 200 · adentro (Nima)
3. paloma #1 a Forjas
4. llegó después de 2000 ms
5. afuera
```

#### Solución
```typescript
type Region = 'Valle' | 'Forjas' | 'Talleres' | 'Puerto';
type Sesion = { estado: 'afuera' } | { estado: 'adentro'; nombre: string };
interface Paloma { id: number; para: Region; vuelo: number }

const json = { 'Content-Type': 'application/json' };
const esperar = (ms: number) => new Promise<void>((listo) => setTimeout(listo, ms));

async function quienSoy(): Promise<Sesion> {
  const respuesta = await fetch('/puerto/perfil');
  if (respuesta.status === 401) return { estado: 'afuera' };
  const datos: unknown = await respuesta.json();
  if (typeof datos === 'object' && datos !== null && 'nombre' in datos && typeof datos.nombre === 'string') return { estado: 'adentro', nombre: datos.nombre };
  throw new Error('El Puerto mandó otra forma');
}

function esPaloma(x: unknown): x is Paloma {
  return typeof x === 'object' && x !== null && 'id' in x && typeof x.id === 'number' && 'vuelo' in x && typeof x.vuelo === 'number';
}

async function mandarPaloma(para: Region, texto: string): Promise<Paloma> {
  const respuesta = await fetch('/puerto/palomas', { method: 'POST', headers: json, body: JSON.stringify({ para, texto }) });
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok || !esPaloma(datos)) throw new Error(`El Palomar contestó ${respuesta.status}`);
  return datos;
}

const decir = (s: Sesion) => (s.estado === 'adentro' ? `adentro (${s.nombre})` : 'afuera');

console.log(`1. ${decir(await quienSoy())}`);
const entrada = await fetch('/puerto/login', { method: 'POST', headers: json, body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }) });
console.log(`2. login: ${entrada.status} · ${decir(await quienSoy())}`);
const paloma = await mandarPaloma('Forjas', 'Tizón: las luces llegaron al Mirador.');
console.log(`3. paloma #${paloma.id} a ${paloma.para}`);
await esperar(paloma.vuelo);
console.log(`4. llegó después de ${paloma.vuelo} ms`);
await fetch('/puerto/salir', { method: 'POST' });
console.log(`5. ${decir(await quienSoy())}`);
```

#### Al superarla
La paloma llega a las Forjas, la sesión se cierra, y el tablero del Mirador queda en blanco, sin ninguna puerta abierta. El Falsificador espera, espera… y se le cae el sello falso de la pinza. Sin sesión y sin cápsulas que engañen, no tiene nada que hacer.

Elefa sube al Mirador en persona, en el ascensor de carga, para llevárselo al Puerto: lo van a reprogramar para **clasificar** cápsulas, no para abrirlas. Antes de irse, le estampa a Rigel el **Sello del Correo Neumático**, violeta como el suyo.

#### Imagen
- El cuarto de máquinas del tubo neumático, tranquilo, con una paloma mecánica de latón volando por una ventana redonda.
- El autómata flaco de latón con brazos de pinza, desarmado y quieto, con su sello falso en el piso.
- Elefa (elefanta capitana con chaqueta de capitán abotonada y bastón) estampa un sello violeta en un papel que sostiene Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón); Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) aplaude; Gheco se prueba la pinza del autómata.
