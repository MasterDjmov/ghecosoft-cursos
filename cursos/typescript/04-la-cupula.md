# RAMA R04 · La Cúpula: errores, lo asincrónico, la página y la configuración

```meta
tipo: tronco
posicion: 4
```

## R04-N01 · Errores tipados

```meta
tipo: tema
padre: R03-N08
precio: 10
criatura: troll
temas: err.excepciones, cal.tipos
```

### Crónica

La **Cúpula** del Mirador es la parte más alta: un domo de latón que se abre en gajos para dejar ver el cielo. Sus motores fallan seguido: a veces se traba un gajo, a veces falta vapor, a veces el viento es demasiado fuerte. Hasta ahora, cada falla hacía sonar la misma campana, y nadie sabía qué pasaba.

—Una falla sin nombre no se arregla —dice {mentor}—. Cada falla tiene que decir **qué** es y traer sus datos. Y quien la ataja tiene que preguntar qué falla le llegó antes de tocarla.

### Objetivos

- Crear errores propios con datos extra: `class GajoTrabado extends Error`.
- Atajar en un `catch` sabiendo que el error es `unknown`, y preguntar con `instanceof`.
- Usar el patrón `Result<T>`: devolver el error en vez de lanzarlo, con una unión discriminada.

### Antes de empezar

- R02-N03 (herencia) y R03-N02 (uniones discriminadas).
- De JavaScript: `throw`, `try`/`catch` y `finally`.

### Explicación

#### Un error con nombre y datos
```typescript
class GajoTrabado extends Error {
  constructor(public readonly gajo: number) {
    super(`El gajo ${gajo} está trabado`);
    this.name = 'GajoTrabado';
  }
}

throw new GajoTrabado(3);
```

#### El catch recibe un unknown
En JavaScript se puede lanzar **cualquier cosa** (`throw 'hola'`, `throw 42`). Por eso, en un `catch`, el error es `unknown`, y hay que preguntar antes de usarlo:

```typescript
try {
  abrirGajo(3);
} catch (error) {
  if (error instanceof GajoTrabado) console.log(`Revisar el gajo ${error.gajo}`);
  else if (error instanceof Error) console.log(error.message);
  else console.log('Falla desconocida');
}
```

Es más seguro que `(error as Error).message`, que usamos en R01: si lo que llegó no era un `Error`, el `as` mentía.

#### Result<T>: devolver en vez de lanzar
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function leerPresion(texto: string): Result<number> {
  const n = Number(texto);
  return Number.isNaN(n) ? { ok: false, error: `«${texto}» no es un número` } : { ok: true, valor: n };
}

const r = leerPresion('40');
if (r.ok) console.log(r.valor);   // TypeScript no deja leer r.valor sin preguntar r.ok
```

Con un `throw`, es fácil olvidarse el `catch`. Con `Result`, el compilador **obliga** a mirar si salió bien antes de usar el valor.

### Código de ejemplo

```typescript
class GajoTrabado extends Error {
  constructor(public readonly gajo: number) {
    super(`El gajo ${gajo} está trabado`);
    this.name = 'GajoTrabado';
  }
}

function abrirGajo(n: number): string {
  if (n === 3) throw new GajoTrabado(n);
  return `gajo ${n} abierto`;
}

type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function leerPresion(texto: string): Result<number> {
  const n = Number(texto);
  return Number.isNaN(n) ? { ok: false, error: `«${texto}» no es un número` } : { ok: true, valor: n };
}

for (const g of [1, 3]) {
  try {
    console.log(abrirGajo(g));
  } catch (error) {
    if (error instanceof GajoTrabado) console.log(`Revisar el gajo ${error.gajo}`);
  }
}
for (const t of ['40', 'mucha']) {
  const r = leerPresion(t);
  console.log(r.ok ? `Presión ${r.valor}` : `Error: ${r.error}`);
}
```

### Salida esperada

```
gajo 1 abierto
Revisar el gajo 3
Presión 40
Error: «mucha» no es un número
```

### ¿Para qué sirve?

En un programa de verdad hay muchas clases de fallas: falta un archivo, la red no responde, un dato viene mal. Con errores propios, cada una dice qué es y trae sus datos, y quien la ataja puede reaccionar distinto a cada una. `Result` es muy usado para los errores que **se esperan** (un dato mal escrito), y `throw` para los que no.

### Errores habituales

**Goblin: usar el error sin preguntar (TS18046).** *"error" es de tipo "unknown"*. Preguntá con `instanceof`.

**Esqueleto: leer el valor de un Result sin mirar ok (TS2339).** *La propiedad 'valor' no existe en el tipo '{ ok: false; error: string; }'*: puede haber salido mal.

**Olvidarse el super.** En la clase del error, `super(mensaje)` va antes de usar `this`.

### Micro-misión R04-N01-P1 · La falla con nombre

```meta
lugar: La Cúpula
personajes: Rigel, Gheco
criatura: troll
carta: Error propio | class GajoTrabado extends Error · public readonly gajo: number · super(mensaje) · this.name
recompensa: xp 10, oro 10
```

#### Escena
Un gajo de la Cúpula no se abre. Rigel quiere que la falla diga **cuál** gajo es, en lugar de hacer sonar la campana de siempre.

#### Gheco sugiere
Un error propio es una clase que hereda de `Error`. En el constructor se llama a `super` con el mensaje, y se pueden guardar datos extra:

```ts
class GajoTrabado extends Error {
  constructor(public readonly gajo: number) {
    super(`El gajo ${gajo} está trabado`);
    this.name = 'GajoTrabado';
  }
}
```

#### Desafío
Completá el `super` con el mensaje.

#### Pasos
1. Buscá el `___` en el constructor.
2. Cambialo por ``super(`El gajo ${gajo} está trabado`);``.
3. Tocá **Ejecutar**. Tiene que salir `GajoTrabado: El gajo 3 está trabado`.

#### Código inicial
```typescript
class GajoTrabado extends Error {
  constructor(public readonly gajo: number) {
    ___
    this.name = 'GajoTrabado';
  }
}

const falla = new GajoTrabado(3);
console.log(`${falla.name}: ${falla.message}`);
```

#### Salida esperada
```
GajoTrabado: El gajo 3 está trabado
```

#### Solución
```typescript
class GajoTrabado extends Error {
  constructor(public readonly gajo: number) {
    super(`El gajo ${gajo} está trabado`);
    this.name = 'GajoTrabado';
  }
}

const falla = new GajoTrabado(3);
console.log(`${falla.name}: ${falla.message}`);
```

#### Al superarla
En el tablero de la Cúpula se enciende una lucecita sobre el gajo 3. Por fin se sabe cuál es.

#### Imagen
- La cúpula de latón de un observatorio steampunk, abierta en gajos, con uno de ellos trabado y una lucecita roja encima.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco de cuero marrón cerrado) señala el gajo.
- Gheco sobre una viga.

### Micro-misión R04-N01-P2 · Atajar sin adivinar

```meta
lugar: La Cúpula
personajes: Rigel, Gheco
criatura: troll
carta: catch con unknown | catch (error): error es unknown · if (error instanceof GajoTrabado) deja usar error.gajo
recompensa: xp 10, oro 10
```

#### Escena
Rigel intenta abrir los gajos de a uno. Cuando uno falla, quiere saber cuál para ir a revisarlo.

#### Gheco sugiere
En el `catch`, el error es `unknown`: podría ser cualquier cosa. Con `instanceof` se pregunta qué es, y adentro del `if` se pueden usar sus datos.

#### Desafío
Completá la pregunta del `catch`.

#### Pasos
1. Buscá el `___` en el `if` del `catch`.
2. Cambialo por `error instanceof GajoTrabado`.
3. Tocá **Ejecutar**. Tiene que salir `gajo 1 abierto`, `Revisar el gajo 3` y `gajo 5 abierto`.

#### Código inicial
```typescript
class GajoTrabado extends Error {
  constructor(public readonly gajo: number) {
    super(`El gajo ${gajo} está trabado`);
  }
}

function abrirGajo(n: number): string {
  if (n === 3) throw new GajoTrabado(n);
  return `gajo ${n} abierto`;
}

for (const g of [1, 3, 5]) {
  try {
    console.log(abrirGajo(g));
  } catch (error) {
    if (___) console.log(`Revisar el gajo ${error.gajo}`);
  }
}
```

#### Salida esperada
```
gajo 1 abierto
Revisar el gajo 3
gajo 5 abierto
```

#### Solución
```typescript
class GajoTrabado extends Error {
  constructor(public readonly gajo: number) {
    super(`El gajo ${gajo} está trabado`);
  }
}

function abrirGajo(n: number): string {
  if (n === 3) throw new GajoTrabado(n);
  return `gajo ${n} abierto`;
}

for (const g of [1, 3, 5]) {
  try {
    console.log(abrirGajo(g));
  } catch (error) {
    if (error instanceof GajoTrabado) console.log(`Revisar el gajo ${error.gajo}`);
  }
}
```

#### Al superarla
Los gajos 1 y 5 se abren; el 3 queda marcado para revisar. La Cúpula ya no se traba entera por un gajo.

#### Imagen
- La cúpula con dos gajos abiertos mostrando el cielo y uno cerrado con una cinta de aviso.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) anota en una libreta.
- Gheco colgado de la cinta.

### Micro-misión R04-N01-P3 · Cualquier cosa puede caer

```meta
lugar: La Cúpula
personajes: Rigel, Gheco
criatura: troll
carta: Preguntar de lo particular a lo general | instanceof GajoTrabado · instanceof Error · lo demás es desconocido
recompensa: xp 10, oro 10
```

#### Escena
Por los caños de la Cúpula caen fallas de todo tipo: gajos trabados, errores comunes y hasta un tornillo suelto (alguien hizo `throw` de un texto).

#### Gheco sugiere
Se pregunta de lo más particular a lo más general:
1. `error instanceof GajoTrabado`;
2. `error instanceof Error` (cualquier error común);
3. lo que queda: algo que no es un error (`String(error)` lo muestra igual).

#### Desafío
Completá la segunda pregunta.

#### Pasos
1. Buscá el `___` en el `else if`.
2. Cambialo por `error instanceof Error`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
class GajoTrabado extends Error {
  constructor(public readonly gajo: number) {
    super(`El gajo ${gajo} está trabado`);
  }
}

function describir(error: unknown): string {
  if (error instanceof GajoTrabado) return `gajo ${error.gajo}`;
  else if (___) return `error: ${error.message}`;
  return `algo raro: ${String(error)}`;
}

const caidas: unknown[] = [new GajoTrabado(2), new Error('falta vapor'), 'tornillo'];
for (const c of caidas) console.log(describir(c));
```

#### Salida esperada
```
gajo 2
error: falta vapor
algo raro: tornillo
```

#### Solución
```typescript
class GajoTrabado extends Error {
  constructor(public readonly gajo: number) {
    super(`El gajo ${gajo} está trabado`);
  }
}

function describir(error: unknown): string {
  if (error instanceof GajoTrabado) return `gajo ${error.gajo}`;
  else if (error instanceof Error) return `error: ${error.message}`;
  return `algo raro: ${String(error)}`;
}

const caidas: unknown[] = [new GajoTrabado(2), new Error('falta vapor'), 'tornillo'];
for (const c of caidas) console.log(describir(c));
```

#### Al superarla
Cada falla cae en su canasto: los gajos, los errores comunes y el tornillo suelto, que Rigel se guarda en el bolsillo.

#### Imagen
- Tres canastos de latón al pie de un caño, cada uno recibiendo una cosa distinta: una pieza rota, una nube de vapor y un tornillo.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) se guarda el tornillo.
- Gheco dentro de un canasto.

### Micro-misión R04-N01-P4 · Devolver en vez de lanzar

```meta
lugar: Las calderas del Mirador
personajes: Rigel, Gheco, Astrea
carta: Result<T> | { ok: true; valor: T } | { ok: false; error: string } · no se puede leer valor sin mirar ok
recompensa: xp 10, oro 10
```

#### Escena
La fogonera anota la presión en un papelito, y a veces escribe palabras en vez de números. Astrea no quiere que eso haga sonar ninguna campana: quiere una respuesta que diga si salió bien o mal.

#### Gheco sugiere
`Result<T>` es una unión discriminada por `ok`:

```ts
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
```

Quien la usa tiene que mirar `r.ok` antes de leer `r.valor`: el compilador no lo deja de otra manera.

#### Desafío
Completá los dos `return`.

#### Pasos
1. El primer `___` (cuando no es número): ``{ ok: false, error: `«${texto}» no es un número` }``.
2. El segundo `___`: `{ ok: true, valor: n }`.
3. Tocá **Ejecutar**. Tiene que salir `Presión 40` y `Error: «mucha» no es un número`.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function leerPresion(texto: string): Result<number> {
  const n = Number(texto);
  if (Number.isNaN(n)) return ___;
  return ___;
}

for (const t of ['40', 'mucha']) {
  const r = leerPresion(t);
  console.log(r.ok ? `Presión ${r.valor}` : `Error: ${r.error}`);
}
```

#### Salida esperada
```
Presión 40
Error: «mucha» no es un número
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function leerPresion(texto: string): Result<number> {
  const n = Number(texto);
  if (Number.isNaN(n)) return { ok: false, error: `«${texto}» no es un número` };
  return { ok: true, valor: n };
}

for (const t of ['40', 'mucha']) {
  const r = leerPresion(t);
  console.log(r.ok ? `Presión ${r.valor}` : `Error: ${r.error}`);
}
```

#### Al superarla
Los papelitos con palabras vuelven a la fogonera con una nota amable. Ninguna campana suena.

#### Imagen
- Papelitos de anotación saliendo de una ranura: unos con un sello verde y otros devueltos con una notita.
- Astrea (lechuza grande gris azulada con anteojos de latón y chaleco azul) lee uno.
- Rigel (chico flaco con pecas, antiparras de latón) separa los papelitos; Gheco sobre la ranura.

### Micro-misión R04-N01-P5 · El valor que no se mira

```meta
lugar: Las calderas del Mirador
personajes: Rigel, Gheco
criatura: skeleton
carta: Mirar ok antes del valor | r.valor sin preguntar es TS2339 · if (r.ok) achica el tipo
recompensa: xp 15, monedas 5
```

#### Escena
Rigel usa el resultado sin mirar si salió bien. Un **esqueleto** se mete en el valor que puede no estar.

#### Gheco sugiere
Si salió mal, el resultado no tiene `valor`: por eso el compilador no deja leerlo sin preguntar (`TS2339`). Adentro de `if (r.ok)`, ya se puede.

#### Desafío
Mostrá el valor solo si salió bien y, si no, el error.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá la última línea por ``console.log(r.ok ? `Vueltas: ${r.valor * 2}` : r.error);``.
3. Tocá **Ejecutar**. Tiene que salir `Vueltas: 14`.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function contar(texto: string): Result<number> {
  const n = Number.parseInt(texto, 10);
  return Number.isNaN(n) ? { ok: false, error: 'no se pudo contar' } : { ok: true, valor: n };
}

const r = contar('7 vueltas');
console.log(`Vueltas: ${r.valor * 2}`);
```

#### Salida esperada
```
Vueltas: 14
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function contar(texto: string): Result<number> {
  const n = Number.parseInt(texto, 10);
  return Number.isNaN(n) ? { ok: false, error: 'no se pudo contar' } : { ok: true, valor: n };
}

const r = contar('7 vueltas');
console.log(r.ok ? `Vueltas: ${r.valor * 2}` : r.error);
```

#### Al superarla
El esqueleto se queda sin hueco: Rigel ya no usa nada sin mirar antes.

#### Imagen
- Un contador de vueltas de latón con una ventanita de «bien» y otra de «mal» (sin letras legibles).
- Un esqueleto de alambre chiquito expulsado de la ventanita.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mira la ventanita correcta; Gheco señala.

### Micro-misión R04-N01-P6 · El parte de la Cúpula

```meta
lugar: La Cúpula
personajes: Rigel, Gheco, Astrea
carta: Todo junto | errores propios para lo inesperado · Result para lo que se espera · finally para cerrar siempre
recompensa: xp 15, monedas 5
```

#### Escena
Al terminar la noche, Rigel cierra la Cúpula gajo por gajo. Algunos gajos se traban, y la lectura del viento a veces llega mal escrita. Astrea quiere un parte con todo, y que la Cúpula quede cerrada pase lo que pase.

#### Gheco sugiere
- `cerrarGajo` lanza un `GajoTrabado` si el gajo no cierra.
- `leerViento` devuelve un `Result<number>`.
- `finally` se ejecuta siempre, haya error o no.

#### Desafío
Completá el `catch` y el `finally`.

#### Pasos
1. El primer `___`: ``if (error instanceof GajoTrabado) parte.push(`trabado el ${error.gajo}`);``.
2. El segundo `___`: `parte.push('cúpula asegurada');`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
class GajoTrabado extends Error {
  constructor(public readonly gajo: number) {
    super(`El gajo ${gajo} está trabado`);
  }
}

type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function cerrarGajo(n: number): void {
  if (n === 2) throw new GajoTrabado(n);
}

function leerViento(texto: string): Result<number> {
  const n = Number(texto);
  return Number.isNaN(n) ? { ok: false, error: 'viento ilegible' } : { ok: true, valor: n };
}

const parte: string[] = [];
try {
  for (const g of [1, 2, 3]) cerrarGajo(g);
} catch (error) {
  ___
} finally {
  ___
}
const viento = leerViento('fuerte');
parte.push(viento.ok ? `viento ${viento.valor}` : viento.error);
console.log(parte.join(' · '));
```

#### Salida esperada
```
trabado el 2 · cúpula asegurada · viento ilegible
```

#### Solución
```typescript
class GajoTrabado extends Error {
  constructor(public readonly gajo: number) {
    super(`El gajo ${gajo} está trabado`);
  }
}

type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function cerrarGajo(n: number): void {
  if (n === 2) throw new GajoTrabado(n);
}

function leerViento(texto: string): Result<number> {
  const n = Number(texto);
  return Number.isNaN(n) ? { ok: false, error: 'viento ilegible' } : { ok: true, valor: n };
}

const parte: string[] = [];
try {
  for (const g of [1, 2, 3]) cerrarGajo(g);
} catch (error) {
  if (error instanceof GajoTrabado) parte.push(`trabado el ${error.gajo}`);
} finally {
  parte.push('cúpula asegurada');
}
const viento = leerViento('fuerte');
parte.push(viento.ok ? `viento ${viento.valor}` : viento.error);
console.log(parte.join(' · '));
```

#### Al superarla
La Cúpula queda cerrada y el parte, completo. Astrea le da a Rigel una **estrella de latón**.

#### Imagen
- La cúpula de latón cerrada al amanecer, con un gajo con cinta de aviso.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sostiene el parte; Gheco bostezando.

## R04-N02 · Promesas tipadas

```meta
tipo: tema
padre: R04-N01
precio: 10
criatura: troll
temas: conc.async, cal.tipos
```

### Crónica

Los motores de la Cúpula son lentos: cuando Rigel les pide que abran un gajo, contestan **un rato después**. Rigel quiere seguir con lo suyo mientras tanto, pero un **troll** de latón insiste en usar la respuesta antes de que llegue.

—Una respuesta que todavía no llegó tiene forma igual —dice {mentor}—. En el Mirador se escribe `Promise<T>`: la promesa de un `T`. Y hasta que no la esperás, no tenés el `T`.

### Objetivos

- Anotar una función `async` con lo que devuelve: `Promise<number>`.
- Ver cómo `await` «desenvuelve» el tipo: de `Promise<number>` a `number`.
- Leer el error de usar una promesa como si fuera el valor.
- Tipar `Promise.all` y conocer `Awaited<T>`.

### Antes de empezar

- R04-N01: errores tipados.
- De JavaScript: promesas, `async`/`await`, `setTimeout` y `Promise.all` (en el curso de JavaScript, R03).

### Explicación

#### La promesa de un número
```typescript
function esperar(ms: number): Promise<void> {
  return new Promise((listo) => setTimeout(listo, ms));
}

async function abrirGajo(n: number): Promise<string> {
  await esperar(500);
  return `gajo ${n} abierto`;
}
```

Una función `async` **siempre** devuelve una promesa: si adentro hace `return 'texto'`, afuera es un `Promise<string>`.

#### await desenvuelve
```typescript
const promesa = abrirGajo(1);       // Promise<string>
const texto = await abrirGajo(1);   // string
promesa.toUpperCase();              // ✗ TS2551: es una promesa, todavía no es un texto
```

#### Varias a la vez
```typescript
const [a, b] = await Promise.all([abrirGajo(1), medirViento()]);   // [string, number]
```

`Promise.all` mantiene el tipo de **cada** lugar.

> `Awaited<T>` es el tipo que queda después de esperar: `Awaited<Promise<string>>` es `string`. Sirve con `ReturnType`: `Awaited<ReturnType<typeof abrirGajo>>`.

### Código de ejemplo

```typescript
function esperar(ms: number): Promise<void> {
  return new Promise((listo) => setTimeout(listo, ms));
}

async function abrirGajo(n: number): Promise<string> {
  await esperar(500);
  return `gajo ${n} abierto`;
}

async function medirViento(): Promise<number> {
  await esperar(300);
  return 12;
}

type Apertura = Awaited<ReturnType<typeof abrirGajo>>;

const [gajo, viento] = await Promise.all([abrirGajo(1), medirViento()]);
const resumen: Apertura = gajo;
console.log(`${resumen} con viento ${viento} a los ${performance.now()} ms`);
```

### Salida esperada

```
gajo 1 abierto con viento 12 a los 500 ms
```

### ¿Para qué sirve?

Casi todo lo que habla con afuera es asincrónico: un servidor, un archivo, una base de datos. `Promise<T>` dice qué va a llegar, y el compilador no deja usarlo antes de esperarlo: así se vence al troll más común de JavaScript, el `await` olvidado.

### Errores habituales

**Troll: usar la promesa como si fuera el valor (TS2551 o TS2339).** *La propiedad 'toUpperCase' no existe en el tipo 'Promise<string>'*: falta el `await`.

**Troll: await fuera de una función async (TS1308).** El `await` va en funciones `async` (o suelto, al nivel de arriba de un módulo, como en la caja).

**Ogro: prometer otro tipo (TS2322).** Si la función dice `Promise<number>` y devuelve un texto, el compilador avisa.

### Micro-misión R04-N02-P1 · La promesa del motor

```meta
lugar: La Cúpula
personajes: Rigel, Gheco
carta: Promise<T> | async function abrir(): Promise<string> · siempre devuelve una promesa · T es lo que va a llegar
recompensa: xp 10, oro 10
```

#### Escena
El motor del gajo 1 tarda medio segundo en contestar. Rigel anota en la firma qué va a contestar.

#### Gheco sugiere
Una función `async` devuelve una **promesa** de lo que hace `return`. Si devuelve un texto, la firma dice `Promise<string>`:

```ts
async function abrirGajo(n: number): Promise<string> { … }
```

#### Desafío
Completá el tipo de lo que devuelve `abrirGajo`.

#### Pasos
1. Buscá el `___` después de los paréntesis de `abrirGajo`.
2. Cambialo por `Promise<string>`.
3. Tocá **Ejecutar**. Tiene que salir `gajo 1 abierto a los 500 ms`.

#### Código inicial
```typescript
function esperar(ms: number): Promise<void> {
  return new Promise((listo) => setTimeout(listo, ms));
}

async function abrirGajo(n: number): ___ {
  await esperar(500);
  return `gajo ${n} abierto`;
}

const texto = await abrirGajo(1);
console.log(`${texto} a los ${performance.now()} ms`);
```

#### Salida esperada
```
gajo 1 abierto a los 500 ms
```

#### Solución
```typescript
function esperar(ms: number): Promise<void> {
  return new Promise((listo) => setTimeout(listo, ms));
}

async function abrirGajo(n: number): Promise<string> {
  await esperar(500);
  return `gajo ${n} abierto`;
}

const texto = await abrirGajo(1);
console.log(`${texto} a los ${performance.now()} ms`);
```

#### Al superarla
Medio segundo después, el gajo 1 se abre con un silbido de vapor.

#### Imagen
- Un motor de vapor de latón al pie de un gajo de la cúpula, soltando vapor mientras el gajo empieza a abrirse.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) espera con los brazos cruzados.
- Gheco con un relojito de bolsillo.

### Micro-misión R04-N02-P2 · El troll impaciente

```meta
lugar: La Cúpula
personajes: Rigel, Gheco
criatura: troll
carta: Falta el await | una Promise<string> no es un string · toUpperCase no existe en la promesa · await la desenvuelve
recompensa: xp 10, oro 10
```

#### Escena
Un **troll** de latón quiere gritar la respuesta del motor antes de que llegue. El compilador no lo deja.

#### Gheco sugiere
Sin `await`, lo que tenés es la **promesa**, no el texto: `Promise<string>` no tiene `toUpperCase`, y el compilador avisa. Con `await`, el tipo pasa a ser `string`.

#### Desafío
Agregá el `await`.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `const respuesta = abrirGajo(2);` por `const respuesta = await abrirGajo(2);`.
3. Tocá **Ejecutar**. Tiene que salir `GAJO 2 ABIERTO`.

#### Código inicial
```typescript
function esperar(ms: number): Promise<void> {
  return new Promise((listo) => setTimeout(listo, ms));
}

async function abrirGajo(n: number): Promise<string> {
  await esperar(500);
  return `gajo ${n} abierto`;
}

const respuesta = abrirGajo(2);
console.log(respuesta.toUpperCase());
```

#### Salida esperada
```
GAJO 2 ABIERTO
```

#### Solución
```typescript
function esperar(ms: number): Promise<void> {
  return new Promise((listo) => setTimeout(listo, ms));
}

async function abrirGajo(n: number): Promise<string> {
  await esperar(500);
  return `gajo ${n} abierto`;
}

const respuesta = await abrirGajo(2);
console.log(respuesta.toUpperCase());
```

#### Al superarla
El troll se queda con la boca abierta: Rigel gritó la respuesta justo cuando llegó.

#### Imagen
- Un troll chiquito de latón con la boca abierta, al lado de un motor de vapor.
- Rigel (chico flaco con pecas, antiparras de latón) grita con las manos alrededor de la boca.
- Gheco tapándose los oídos.

### Micro-misión R04-N02-P3 · Lo que no se prometió

```meta
lugar: La Cúpula
personajes: Rigel, Gheco
criatura: ogre
carta: Promise<number> devuelve number | return de otro tipo es TS2322 · la promesa dice qué va a llegar
recompensa: xp 10, oro 10
```

#### Escena
El medidor de viento prometió un número, pero devuelve un texto. El **ogro** del motor se ríe.

#### Gheco sugiere
Si la firma dice `Promise<number>`, el `return` tiene que ser un número. Si devolvés otra cosa, el compilador avisa (`TS2322`), aunque la función sea `async`.

#### Desafío
Devolvé el número 12 en lugar del texto.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `return '12 km/h';` por `return 12;`.
3. Tocá **Ejecutar**. Tiene que salir `Viento: 12 km/h, el doble de ayer (6)`.

#### Código inicial
```typescript
async function medirViento(): Promise<number> {
  return '12 km/h';
}

const viento = await medirViento();
console.log(`Viento: ${viento} km/h, el doble de ayer (${viento / 2})`);
```

#### Salida esperada
```
Viento: 12 km/h, el doble de ayer (6)
```

#### Solución
```typescript
async function medirViento(): Promise<number> {
  return 12;
}

const viento = await medirViento();
console.log(`Viento: ${viento} km/h, el doble de ayer (${viento / 2})`);
```

#### Al superarla
El medidor devuelve el número limpio y Rigel puede hacer cuentas con él.

#### Imagen
- Un anemómetro de latón con cazoletas girando en lo alto de la cúpula.
- Un ogro chiquito con un cartelito de papel en la mano.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) lee el anemómetro; Gheco agarrado de una cazoleta.

### Micro-misión R04-N02-P4 · Todo a la vez

```meta
lugar: La Cúpula
personajes: Rigel, Gheco, Astrea
carta: Promise.all tipado | await Promise.all([a(), b()]) · cada lugar conserva su tipo · tardan lo que la más lenta
recompensa: xp 15, monedas 5
```

#### Escena
Astrea no quiere esperar al motor y después al viento: que se pidan las dos cosas a la vez.

#### Gheco sugiere
`Promise.all` espera varias promesas **a la vez**, y lo que devuelve es una tupla con el tipo de cada una:

```ts
const [gajo, viento] = await Promise.all([abrirGajo(1), medirViento()]);
// gajo: string, viento: number
```

Tarda lo que tarda la más lenta, no la suma.

#### Desafío
Completá el `Promise.all`.

#### Pasos
1. Buscá el `___` después de `await`.
2. Cambialo por `Promise.all([abrirGajo(1), medirViento()])`.
3. Tocá **Ejecutar**. Tiene que salir `gajo 1 abierto · viento 12 · a los 500 ms`.

#### Código inicial
```typescript
function esperar(ms: number): Promise<void> {
  return new Promise((listo) => setTimeout(listo, ms));
}

async function abrirGajo(n: number): Promise<string> {
  await esperar(500);
  return `gajo ${n} abierto`;
}

async function medirViento(): Promise<number> {
  await esperar(300);
  return 12;
}

const [gajo, viento] = await ___;
console.log(`${gajo} · viento ${viento} · a los ${performance.now()} ms`);
```

#### Salida esperada
```
gajo 1 abierto · viento 12 · a los 500 ms
```

#### Solución
```typescript
function esperar(ms: number): Promise<void> {
  return new Promise((listo) => setTimeout(listo, ms));
}

async function abrirGajo(n: number): Promise<string> {
  await esperar(500);
  return `gajo ${n} abierto`;
}

async function medirViento(): Promise<number> {
  await esperar(300);
  return 12;
}

const [gajo, viento] = await Promise.all([abrirGajo(1), medirViento()]);
console.log(`${gajo} · viento ${viento} · a los ${performance.now()} ms`);
```

#### Al superarla
El gajo se abre y el viento se mide al mismo tiempo. Astrea mira el reloj: medio segundo, ni uno más.

#### Imagen
- La cúpula con un gajo abriéndose y el anemómetro girando a la vez, con dos relojitos marcando lo mismo.
- Astrea (lechuza con anteojos de latón y chaleco azul) consulta un reloj de bolsillo.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) tira de dos palancas; Gheco sobre una de ellas.

### Micro-misión R04-N02-P5 · Lo que queda después de esperar

```meta
lugar: La Cúpula
personajes: Rigel, Gheco
carta: Awaited<T> | Awaited<ReturnType<typeof f>> · el tipo de lo que llega, sin la promesa
recompensa: xp 15, monedas 5
```

#### Escena
Rigel guarda los partes de los motores en una lista. Quiere que el tipo de la lista salga de la función, sin escribirlo a mano.

#### Gheco sugiere
`ReturnType<typeof leerMotor>` da `Promise<{ … }>`. Para el tipo de lo que **llega**, se envuelve con `Awaited`:

```ts
type Parte = Awaited<ReturnType<typeof leerMotor>>;
```

#### Desafío
Completá el tipo `Parte`.

#### Pasos
1. Buscá el `___` después de `type Parte =`.
2. Cambialo por `Awaited<ReturnType<typeof leerMotor>>`.
3. Tocá **Ejecutar**. Tiene que salir `motor 1: 40 · motor 2: 55`.

#### Código inicial
```typescript
async function leerMotor(n: number) {
  return { motor: n, presion: 25 + n * 15 };
}

type Parte = ___;

const partes: Parte[] = [];
for (const n of [1, 2]) partes.push(await leerMotor(n));
console.log(partes.map((p) => `motor ${p.motor}: ${p.presion}`).join(' · '));
```

#### Salida esperada
```
motor 1: 40 · motor 2: 55
```

#### Solución
```typescript
async function leerMotor(n: number) {
  return { motor: n, presion: 25 + n * 15 };
}

type Parte = Awaited<ReturnType<typeof leerMotor>>;

const partes: Parte[] = [];
for (const n of [1, 2]) partes.push(await leerMotor(n));
console.log(partes.map((p) => `motor ${p.motor}: ${p.presion}`).join(' · '));
```

#### Al superarla
Los partes de los motores quedan en fila, cada uno con su forma. Astrea le da a Rigel una **estrella de latón**.

#### Imagen
- Dos motores de vapor de latón con sus manómetros, y una libreta con dos partes anotados.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) anota en la libreta.
- Astrea (lechuza con anteojos de latón) le da una ficha con una estrella; Gheco sobre un motor.

## R04-N03 · fetch tipado: el tubo al Puerto

```meta
tipo: tema
padre: R04-N02
precio: 10
criatura: troll
temas: web.http, conc.async, err.validacion
```

### Crónica

Desde la Cúpula baja un **tubo neumático** que llega hasta el Puerto de los Mensajeros, donde Elefa atiende los pedidos de todo el mundo. Rigel le pide al Puerto la lista de puestos de la Feria, para saber dónde comprar aceite. Lo que vuelve por el tubo es una cápsula sin etiqueta.

—Lo que llega del Puerto no trae medida —dice {mentor}—. Para el compilador es `any`: lo deja pasar todo. Vos no lo dejes. Revisá la cápsula antes de abrirla.

### Objetivos

- Pedir datos al Puerto con `fetch` y tipar lo que devuelve la función: `Promise<Puesto[]>`.
- Saber que `respuesta.json()` devuelve `any`, y por qué hay que tratarlo como `unknown`.
- Validar la respuesta con un guardia antes de usarla.
- Revisar `respuesta.ok` y devolver un `Result`.

### Antes de empezar

- R04-N01 (`Result<T>`) y R04-N02 (promesas tipadas).
- R03-N03: guardias propios.
- De JavaScript: `fetch` y el Puerto de Elefa (en el curso de JavaScript, R03).

### Explicación

#### Lo que vuelve por el tubo
```typescript
const respuesta = await fetch('/puerto/puestos');   // Response
const datos = await respuesta.json();               // any: el compilador no sabe qué llegó
```

`json()` devuelve `any` porque TypeScript no puede saber qué manda el servidor. Lo más peligroso es usarlo directo. Hay dos caminos:
- **`as Puesto[]`**: le decís al compilador «confiá en mí». Si el servidor mandó otra cosa, explota más adelante.
- **guardarlo como `unknown` y validarlo** con un guardia: lo seguro.

#### Validar antes de abrir
```typescript
type Puesto = { id: number; nombre: string; precio: number; abierto: boolean };

function esPuesto(x: unknown): x is Puesto { … }

async function pedirPuestos(): Promise<Puesto[]> {
  const respuesta = await fetch('/puerto/puestos');
  const datos: unknown = await respuesta.json();
  if (!Array.isArray(datos) || !datos.every(esPuesto)) throw new Error('El Puerto mandó otra cosa');
  return datos;
}
```

`datos.every(esPuesto)` revisa cada elemento con el guardia: si todos pasan, TypeScript sabe que es un `Puesto[]`.

#### Cuando el Puerto contesta mal
`respuesta.ok` es `true` si el código está entre 200 y 299. Si no, conviene devolver un `Result` con el error, en vez de intentar leer un puesto que no llegó.

> En la caja, el Puerto es de mentira: contesta `/puerto/puestos`, `/puerto/puestos/1`, `/puerto/heroes`, `/puerto/clima` y otros, con una demora, sin salir a internet.

### Código de ejemplo

```typescript
type Clima = { noche: boolean; viento: string; temperatura: number };

function esClima(x: unknown): x is Clima {
  return typeof x === 'object' && x !== null
    && 'noche' in x && typeof x.noche === 'boolean'
    && 'viento' in x && typeof x.viento === 'string'
    && 'temperatura' in x && typeof x.temperatura === 'number';
}

async function pedirClima(): Promise<Clima> {
  const respuesta = await fetch('/puerto/clima');
  const datos: unknown = await respuesta.json();
  if (!esClima(datos)) throw new Error('El Puerto mandó otra cosa');
  return datos;
}

const clima = await pedirClima();
console.log(`¿Noche? ${clima.noche} · viento ${clima.viento} · ${clima.temperatura}°`);
```

### Salida esperada

```
¿Noche? true · viento suave · 18°
```

### ¿Para qué sirve?

Las respuestas de los servidores son la puerta de entrada de los errores: un campo que cambió de nombre, un número que llega como texto, un error en lugar de un dato. Validar lo que llega (con guardias o con bibliotecas como Zod) hace que el problema aparezca **en la puerta**, con un mensaje claro, y no tres pantallas más adelante.

### Errores habituales

**Troll: confiar en el any.** `const puestos = await respuesta.json(); puestos[0].nombr` compila (es `any`) y da `undefined`. Guardalo como `unknown` y validalo.

**Troll: no mirar respuesta.ok.** Si el Puerto contesta 404, el JSON es un error, no un puesto.

**El as que miente.** `as Puesto[]` no revisa nada: es una promesa tuya al compilador. Usalo solo si de verdad sabés qué llega.

### Micro-misión R04-N03-P1 · La primera cápsula

```meta
lugar: El tubo neumático
personajes: Rigel, Gheco
carta: fetch con su tipo | async function pedirClima(): Promise<Clima> · lo que llega se guarda como unknown · se valida con un guardia
recompensa: xp 10, oro 10
```

#### Escena
Rigel manda por el tubo un pedido al Puerto: ¿qué clima hay esta noche? La cápsula vuelve sin etiqueta.

#### Gheco sugiere
`respuesta.json()` devuelve algo sin medida. Se guarda como `unknown`:

```ts
const datos: unknown = await respuesta.json();
```

y se valida con un guardia antes de devolverlo. Así la función puede prometer `Promise<Clima>` de verdad.

#### Desafío
Completá la línea que lee el JSON como `unknown`.

#### Pasos
1. Buscá el `___` en `pedirClima`.
2. Cambialo por `const datos: unknown = await respuesta.json();`.
3. Tocá **Ejecutar**. Tiene que salir `Esta noche: viento suave, 18°`.

#### Código inicial
```typescript
type Clima = { viento: string; temperatura: number };

function esClima(x: unknown): x is Clima {
  return typeof x === 'object' && x !== null
    && 'viento' in x && typeof x.viento === 'string'
    && 'temperatura' in x && typeof x.temperatura === 'number';
}

async function pedirClima(): Promise<Clima> {
  const respuesta = await fetch('/puerto/clima');
  ___
  if (!esClima(datos)) throw new Error('El Puerto mandó otra cosa');
  return datos;
}

const clima = await pedirClima();
console.log(`Esta noche: viento ${clima.viento}, ${clima.temperatura}°`);
```

#### Salida esperada
```
Esta noche: viento suave, 18°
```

#### Solución
```typescript
type Clima = { viento: string; temperatura: number };

function esClima(x: unknown): x is Clima {
  return typeof x === 'object' && x !== null
    && 'viento' in x && typeof x.viento === 'string'
    && 'temperatura' in x && typeof x.temperatura === 'number';
}

async function pedirClima(): Promise<Clima> {
  const respuesta = await fetch('/puerto/clima');
  const datos: unknown = await respuesta.json();
  if (!esClima(datos)) throw new Error('El Puerto mandó otra cosa');
  return datos;
}

const clima = await pedirClima();
console.log(`Esta noche: viento ${clima.viento}, ${clima.temperatura}°`);
```

#### Al superarla
La cápsula se abre: viento suave, 18 grados. Una buena noche para abrir la Cúpula.

#### Imagen
- Un tubo neumático de latón que baja por la ladera de la montaña hasta un puerto lejano, con una cápsula llegando.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) abre la cápsula.
- Gheco asomado al tubo.

### Micro-misión R04-N03-P2 · La lista de puestos

```meta
lugar: El tubo neumático
personajes: Rigel, Gheco
carta: Validar una lista | Array.isArray(datos) && datos.every(esPuesto) · si todos pasan, es Puesto[]
recompensa: xp 10, oro 10
```

#### Escena
Rigel pide al Puerto la lista de puestos de la Feria, para saber cuáles están abiertos y comprar aceite.

#### Gheco sugiere
Para una lista, se revisa que sea un arreglo y que **cada** elemento pase el guardia:

```ts
if (!Array.isArray(datos) || !datos.every(esPuesto)) throw new Error('…');
```

`every` con un guardia le dice a TypeScript que todo el arreglo es de ese tipo.

#### Desafío
Completá la validación.

#### Pasos
1. Buscá el `___` en el `if`.
2. Cambialo por `!Array.isArray(datos) || !datos.every(esPuesto)`.
3. Tocá **Ejecutar**. Tiene que salir `Abiertos: Tiro al blanco, Pan con miel, Títeres de luz`.

#### Código inicial
```typescript
type Puesto = { id: number; nombre: string; abierto: boolean };

function esPuesto(x: unknown): x is Puesto {
  return typeof x === 'object' && x !== null
    && 'id' in x && typeof x.id === 'number'
    && 'nombre' in x && typeof x.nombre === 'string'
    && 'abierto' in x && typeof x.abierto === 'boolean';
}

async function pedirPuestos(): Promise<Puesto[]> {
  const respuesta = await fetch('/puerto/puestos');
  const datos: unknown = await respuesta.json();
  if (___) throw new Error('El Puerto mandó otra cosa');
  return datos;
}

const puestos = await pedirPuestos();
console.log(`Abiertos: ${puestos.filter((p) => p.abierto).map((p) => p.nombre).join(', ')}`);
```

#### Salida esperada
```
Abiertos: Tiro al blanco, Pan con miel, Títeres de luz
```

#### Solución
```typescript
type Puesto = { id: number; nombre: string; abierto: boolean };

function esPuesto(x: unknown): x is Puesto {
  return typeof x === 'object' && x !== null
    && 'id' in x && typeof x.id === 'number'
    && 'nombre' in x && typeof x.nombre === 'string'
    && 'abierto' in x && typeof x.abierto === 'boolean';
}

async function pedirPuestos(): Promise<Puesto[]> {
  const respuesta = await fetch('/puerto/puestos');
  const datos: unknown = await respuesta.json();
  if (!Array.isArray(datos) || !datos.every(esPuesto)) throw new Error('El Puerto mandó otra cosa');
  return datos;
}

const puestos = await pedirPuestos();
console.log(`Abiertos: ${puestos.filter((p) => p.abierto).map((p) => p.nombre).join(', ')}`);
```

#### Al superarla
Tres puestos abiertos. Rigel anota el de Pan con miel para la vuelta.

#### Imagen
- Una cápsula abierta con un rollo de papel con una lista de puestos de feria dibujados (sin letras legibles).
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) lee el rollo con una sonrisa.
- Gheco relamiéndose.

### Micro-misión R04-N03-P3 · El nombre que no llegó

```meta
lugar: El tubo neumático
personajes: Rigel, Gheco
criatura: troll
carta: El any esconde errores | json() devuelve any · un nombre mal escrito compila y da undefined · con unknown y un tipo, el compilador lo encuentra
recompensa: xp 10, oro 10
```

#### Escena
Rigel usa la respuesta directo, sin tipo. El programa compila, pero muestra *undefined*: escribió mal el nombre de una propiedad, y nadie le avisó.

#### Gheco sugiere
Como `json()` devuelve `any`, el compilador no revisa nada: `heroe.nombr` compila y da `undefined`. Si le das un tipo a lo que llega, el compilador encuentra el error.

#### Desafío
Dale el tipo `Heroe[]` a la lista y arreglá lo que aparece.

#### Pasos
1. Tocá **Ejecutar**: sale `undefined`.
2. Cambiá `const heroes = await respuesta.json();` por `const heroes: Heroe[] = await respuesta.json();`.
3. Ejecutá: ahora el compilador marca `nombr`. Cambialo por `nombre`.
4. Tocá **Ejecutar**. Tiene que salir `Primera heroína del Puerto: Mia`.

#### Código inicial
```typescript
type Heroe = { nombre: string; region: string; nivel: number };

const respuesta = await fetch('/puerto/heroes');
const heroes = await respuesta.json();
console.log(`Primera heroína del Puerto: ${heroes[0].nombr}`);
```

#### Salida esperada
```
Primera heroína del Puerto: Mia
```

#### Solución
```typescript
type Heroe = { nombre: string; region: string; nivel: number };

const respuesta = await fetch('/puerto/heroes');
const heroes: Heroe[] = await respuesta.json();
console.log(`Primera heroína del Puerto: ${heroes[0].nombre}`);
```

#### Al superarla
El nombre aparece. Gheco aclara: —Ojo: poner el tipo así es confiar en el Puerto. Lo más seguro es el guardia, como antes.

#### Imagen
- Un rollo de papel con retratitos de héroes saliendo de una cápsula (sin letras legibles).
- Un troll chiquito de latón escondiendo una letra arrancada.
- Rigel (chico flaco con pecas, antiparras de latón) corrige con la pluma; Gheco levanta un dedo.

### Micro-misión R04-N03-P4 · El puesto que no existe

```meta
lugar: El tubo neumático
personajes: Rigel, Gheco, Astrea
carta: respuesta.ok y Result | si no es ok, el JSON es un error · se devuelve { ok: false, error } · si es ok, el dato
recompensa: xp 15, monedas 5
```

#### Escena
Astrea le pide a Rigel el puesto número 9. El Puerto contesta con un error: no hay ningún puesto 9.

#### Gheco sugiere
`respuesta.ok` es `true` si salió bien (código 200 a 299). Si no, lo que llega es un error del Puerto (`{ error: '…' }`), y conviene devolverlo en un `Result`.

#### Desafío
Completá la pregunta por `respuesta.ok`.

#### Pasos
1. Buscá el `___` en el primer `if`.
2. Cambialo por `!respuesta.ok`.
3. Tocá **Ejecutar**. Tiene que salir `Puesto 2: Pan con miel` y `No hay ningún puesto con el número 9.`

#### Código inicial
```typescript
type Puesto = { id: number; nombre: string };
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

async function pedirPuesto(id: number): Promise<Result<Puesto>> {
  const respuesta = await fetch(`/puerto/puestos/${id}`);
  const datos = await respuesta.json();
  if (___) return { ok: false, error: String(datos.error) };
  return { ok: true, valor: datos as Puesto };
}

for (const id of [2, 9]) {
  const r = await pedirPuesto(id);
  console.log(r.ok ? `Puesto ${r.valor.id}: ${r.valor.nombre}` : r.error);
}
```

#### Salida esperada
```
Puesto 2: Pan con miel
No hay ningún puesto con el número 9.
```

#### Solución
```typescript
type Puesto = { id: number; nombre: string };
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

async function pedirPuesto(id: number): Promise<Result<Puesto>> {
  const respuesta = await fetch(`/puerto/puestos/${id}`);
  const datos = await respuesta.json();
  if (!respuesta.ok) return { ok: false, error: String(datos.error) };
  return { ok: true, valor: datos as Puesto };
}

for (const id of [2, 9]) {
  const r = await pedirPuesto(id);
  console.log(r.ok ? `Puesto ${r.valor.id}: ${r.valor.nombre}` : r.error);
}
```

#### Al superarla
El error del Puerto llega con su explicación, sin romper nada. Astrea asiente: —Elefa siempre contesta, aunque sea para decir que no.

#### Imagen
- Dos cápsulas abiertas: una con un dibujo de un puesto de pan con miel, otra con una nota de disculpa sellada con lacre.
- Astrea (lechuza con anteojos de latón y chaleco azul) lee la nota.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sostiene la otra cápsula; Gheco mira.

### Micro-misión R04-N03-P5 · El pedido seguro

```meta
lugar: El tubo neumático
personajes: Rigel, Gheco, Astrea
carta: Todo junto | un pedir<T> genérico con un guardia · Result para el error · nada de any sin revisar
recompensa: xp 15, monedas 5
```

#### Escena
Rigel arma una sola máquina para todos los pedidos al Puerto: recibe la dirección y el guardia, y devuelve un `Result`. Sirve para el clima, los puestos, lo que sea.

#### Gheco sugiere
Un genérico con un guardia como parámetro:

```ts
async function pedir<T>(ruta: string, esValido: (x: unknown) => x is T): Promise<Result<T>> { … }
```

`esValido` es un guardia: el tipo de función `(x: unknown) => x is T`.

#### Desafío
Completá el tipo del parámetro `esValido`.

#### Pasos
1. Buscá el `___` después de `esValido:`.
2. Cambialo por `(x: unknown) => x is T`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
type Clima = { viento: string; temperatura: number };

function esClima(x: unknown): x is Clima {
  return typeof x === 'object' && x !== null
    && 'viento' in x && typeof x.viento === 'string'
    && 'temperatura' in x && typeof x.temperatura === 'number';
}

async function pedir<T>(ruta: string, esValido: ___): Promise<Result<T>> {
  const respuesta = await fetch(ruta);
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok) return { ok: false, error: `el Puerto contestó ${respuesta.status}` };
  if (!esValido(datos)) return { ok: false, error: 'el Puerto mandó otra cosa' };
  return { ok: true, valor: datos };
}

const clima = await pedir('/puerto/clima', esClima);
console.log(clima.ok ? `Viento ${clima.valor.viento}` : clima.error);
const roto = await pedir('/puerto/hola', esClima);
console.log(roto.ok ? `Viento ${roto.valor.viento}` : roto.error);
```

#### Salida esperada
```
Viento suave
el Puerto mandó otra cosa
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
type Clima = { viento: string; temperatura: number };

function esClima(x: unknown): x is Clima {
  return typeof x === 'object' && x !== null
    && 'viento' in x && typeof x.viento === 'string'
    && 'temperatura' in x && typeof x.temperatura === 'number';
}

async function pedir<T>(ruta: string, esValido: (x: unknown) => x is T): Promise<Result<T>> {
  const respuesta = await fetch(ruta);
  const datos: unknown = await respuesta.json();
  if (!respuesta.ok) return { ok: false, error: `el Puerto contestó ${respuesta.status}` };
  if (!esValido(datos)) return { ok: false, error: 'el Puerto mandó otra cosa' };
  return { ok: true, valor: datos };
}

const clima = await pedir('/puerto/clima', esClima);
console.log(clima.ok ? `Viento ${clima.valor.viento}` : clima.error);
const roto = await pedir('/puerto/hola', esClima);
console.log(roto.ok ? `Viento ${roto.valor.viento}` : roto.error);
```

#### Al superarla
La máquina de pedidos queda atornillada junto al tubo. Astrea le da a Rigel una **estrella de latón**: —Ni Elefa podría mandarte algo que no revises.

#### Imagen
- Una máquina de latón junto al tubo neumático, con una ranura de entrada y dos bandejas de salida (aceptado y rechazado).
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) atornilla la máquina; Gheco sobre el tubo.

## R04-N04 · La página tipada

```meta
tipo: tema
padre: R04-N03
precio: 10
criatura: orc
temas: js.dom, js.eventos, cal.tipos
```

### Crónica

En la Cúpula hay un **tablero de control**: perillas, botones y cartelitos de luz para manejar los gajos desde abajo. Rigel lo conecta a su programa, pero el compilador se queja de todo: que el botón podría no estar, que el cartel no se sabe qué es, que la perilla no tiene número.

—El tablero es una página —dice {mentor}—. Y el compilador no la ve: no sabe qué elementos hay ni de qué clase son. Tenés que decírselo, y preguntar si están.

### Objetivos

- Entender por qué `querySelector` devuelve `Element | null` y preguntar antes de usarlo.
- Decir qué elemento es con el genérico: `querySelector<HTMLInputElement>('#perilla')`.
- Tipar los eventos: `MouseEvent`, `KeyboardEvent`, `SubmitEvent`.
- Leer `value` de un `input` (que siempre es texto) y convertirlo.

### Antes de empezar

- De JavaScript: la página (el DOM) y los eventos (en el curso de JavaScript, R02).
- R03-N01: descartar `null`.

### Explicación

#### El elemento que podría no estar
```typescript
const cartel = document.querySelector('#cartel');   // Element | null
cartel.textContent = 'Abierto';                     // ✗ TS18047: cartel es posiblemente null
```

`querySelector` devuelve `null` si no encuentra nada. TypeScript obliga a preguntar:

```typescript
if (cartel) cartel.textContent = 'Abierto';
```

#### Decir qué elemento es
`Element` es muy general: no sabe que un `input` tiene `value`. Con el genérico, se dice qué es:

```typescript
const perilla = document.querySelector<HTMLInputElement>('#perilla');
const boton = document.querySelector<HTMLButtonElement>('#abrir');
```

Algunos ya los sabe solo: `document.querySelector('input')` es `HTMLInputElement | null`, porque la etiqueta lo dice.

#### Eventos con tipo
```typescript
boton?.addEventListener('click', (e: MouseEvent) => { … });
document.addEventListener('keydown', (e: KeyboardEvent) => { if (e.key === 'Enter') … });
```

Adentro de `addEventListener('click', …)`, TypeScript ya sabe que el evento es un `MouseEvent`: anotarlo es opcional.

#### value siempre es texto
`perilla.value` es un `string`, aunque el `input` sea de números: hay que convertir con `Number(…)` o usar `perilla.valueAsNumber`.

### Código de ejemplo

```typescript
const perilla = document.querySelector<HTMLInputElement>('#perilla');
const cartel = document.querySelector<HTMLParagraphElement>('#cartel');

if (perilla && cartel) {
  const grados = Number(perilla.value);
  cartel.textContent = `Gajos abiertos a ${grados * 2}°`;
} else {
  console.log('Acá no hay tablero: este ejemplo necesita su página (probalo en las micro-misiones).');
}
```

### Salida esperada

```
Acá no hay tablero: este ejemplo necesita su página (probalo en las micro-misiones).
```

### ¿Para qué sirve?

En JavaScript, la mitad de los errores de una página son elementos que no están (`null`), propiedades que ese elemento no tiene y valores que llegan como texto. TypeScript los marca todos antes de abrir la página.

### Errores habituales

**Orco: usar un elemento sin preguntar (TS18047).** *"cartel" es posiblemente "null"*. Preguntá con `if (cartel)` o usá `?.`.

**Esqueleto: una propiedad que Element no tiene (TS2339).** *La propiedad 'value' no existe en el tipo 'Element'*. Decí qué elemento es: `querySelector<HTMLInputElement>(…)`.

**Goblin: el value es texto.** `perilla.value + 10` pega en vez de sumar. Convertí con `Number(perilla.value)`.

**Orco: la pregunta que no llega a la función.** Si preguntás `if (!cartel) throw …` afuera, adentro de una `function` declarada más abajo TypeScript igual dice que `cartel` puede ser `null`. Usá una función flecha en una `const`, creada después de la pregunta.

### Micro-misión R04-N04-P1 · El cartel que podría no estar

```meta
lugar: El tablero de la Cúpula
personajes: Rigel, Gheco
criatura: orc
carta: Element | null | querySelector puede no encontrar nada · if (cartel) antes de usarlo · si no, TS18047
recompensa: xp 10, oro 10
```

#### Escena
Rigel quiere que el cartel del tablero diga *Cúpula abierta*. El compilador no lo deja: el cartel podría no estar.

#### Gheco sugiere
`querySelector` devuelve `null` si no encuentra el elemento. Por eso el compilador obliga a preguntar:

```ts
if (cartel) cartel.textContent = 'Cúpula abierta';
```

#### Desafío
Agregá la pregunta antes de usar el cartel.

#### Pasos
1. Tocá **Ejecutar** y leé el error (`TS18047`).
2. Cambiá `cartel.textContent = 'Cúpula abierta';` por `if (cartel) cartel.textContent = 'Cúpula abierta';`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1326; color: #e8d9b0; padding: 24px; }
  #cartel { font-size: 24px; color: #f2c14e; }
</style>
<p id="cartel">Cúpula cerrada</p>
```

#### Estado
```
#cartel
```

#### Código inicial
```typescript
const cartel = document.querySelector('#cartel');
cartel.textContent = 'Cúpula abierta';
```

#### Salida esperada
```
── Estado ──
#cartel: Cúpula abierta
```

#### Solución
```typescript
const cartel = document.querySelector('#cartel');
if (cartel) cartel.textContent = 'Cúpula abierta';
```

#### Al superarla
El cartel de luz del tablero cambia a *Cúpula abierta*, y los gajos empiezan a moverse.

#### Imagen
- Un tablero de control de latón con un cartel de luz ámbar encendido, botones y perillas, al pie de la cúpula.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) frente al tablero.
- Gheco sobre el cartel.

### Micro-misión R04-N04-P2 · La perilla de los grados

```meta
lugar: El tablero de la Cúpula
personajes: Rigel, Gheco
criatura: skeleton
carta: querySelector<T> | querySelector<HTMLInputElement>('#perilla') · ahora sabe que tiene value · value es texto: Number(…)
recompensa: xp 10, oro 10
```

#### Escena
La perilla del tablero dice cuántos grados abrir. Rigel la lee, pero el compilador dice que un `Element` no tiene `value`.

#### Gheco sugiere
`querySelector('#perilla')` devuelve un `Element`: el compilador no sabe que es un `input`. Con el genérico se lo decís:

```ts
const perilla = document.querySelector<HTMLInputElement>('#perilla');
```

Y `perilla.value` es **texto**: para hacer cuentas, `Number(perilla.value)`.

#### Desafío
Decí que la perilla es un `HTMLInputElement`.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `document.querySelector('#perilla')` por `document.querySelector<HTMLInputElement>('#perilla')`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1326; color: #e8d9b0; padding: 24px; }
  #cartel { font-size: 24px; color: #f2c14e; }
</style>
<label>Grados <input id="perilla" type="number" value="15"></label>
<p id="cartel">—</p>
```

#### Estado
```
#cartel
```

#### Código inicial
```typescript
const perilla = document.querySelector('#perilla');
const cartel = document.querySelector('#cartel');

if (perilla && cartel) {
  cartel.textContent = `Gajos a ${Number(perilla.value) * 2}°`;
}
```

#### Salida esperada
```
── Estado ──
#cartel: Gajos a 30°
```

#### Solución
```typescript
const perilla = document.querySelector<HTMLInputElement>('#perilla');
const cartel = document.querySelector('#cartel');

if (perilla && cartel) {
  cartel.textContent = `Gajos a ${Number(perilla.value) * 2}°`;
}
```

#### Al superarla
La perilla marca 15 y los gajos se abren a 30 grados, como dice el cartel.

#### Imagen
- Una perilla de latón con una escala grabada (sin números legibles) y un cartel de luz al lado.
- Un esqueleto de alambre chiquito saliendo despedido de la perilla.
- Rigel (chico flaco con pecas, antiparras de latón, guantes sin dedos) gira la perilla; Gheco mira.

### Micro-misión R04-N04-P3 · El botón de abrir

```meta
lugar: El tablero de la Cúpula
personajes: Rigel, Gheco
carta: Eventos tipados | boton?.addEventListener('click', …) · el ?. por si no está · adentro, el evento ya tiene tipo
recompensa: xp 10, oro 10
```

#### Escena
El botón grande del tablero tiene que abrir un gajo por cada vez que lo tocan, y el cartel tiene que contar cuántos van.

#### Gheco sugiere
`boton?.addEventListener(…)`: el `?.` hace que, si el botón no está, no pase nada (en vez de romper).

Adentro, el cartel puede no estar: también se pregunta.

#### Desafío
Completá lo que pasa en cada click: sumar un gajo y mostrarlo.

#### Pasos
1. Buscá el `___` adentro del evento.
2. Cambialo por `abiertos++;` y, en el renglón de abajo, ``if (cartel) cartel.textContent = `Gajos abiertos: ${abiertos}`;``.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1326; color: #e8d9b0; padding: 24px; }
  #cartel { font-size: 24px; color: #f2c14e; }
</style>
<button id="abrir">Abrir un gajo</button>
<p id="cartel">Gajos abiertos: 0</p>
```

#### Eventos
```
click #abrir
click #abrir
click #abrir
```

#### Estado
```
#cartel
```

#### Código inicial
```typescript
const boton = document.querySelector<HTMLButtonElement>('#abrir');
const cartel = document.querySelector('#cartel');
let abiertos = 0;

boton?.addEventListener('click', () => {
  ___
});
```

#### Salida esperada
```
── Estado ──
#cartel: Gajos abiertos: 3
```

#### Solución
```typescript
const boton = document.querySelector<HTMLButtonElement>('#abrir');
const cartel = document.querySelector('#cartel');
let abiertos = 0;

boton?.addEventListener('click', () => {
  abiertos++;
  if (cartel) cartel.textContent = `Gajos abiertos: ${abiertos}`;
});
```

#### Al superarla
Tres clicks, tres gajos. El cielo se ve por una franja ancha de la Cúpula.

#### Imagen
- Un botón grande de latón con una tapa protectora levantada, en el tablero de control, y la cúpula abriéndose arriba.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) aprieta el botón.
- Gheco contando con los dedos.

### Micro-misión R04-N04-P4 · La tecla de emergencia

```meta
lugar: El tablero de la Cúpula
personajes: Rigel, Gheco
carta: KeyboardEvent | document.addEventListener('keydown', (e: KeyboardEvent) => …) · e.key dice qué tecla · Escape cierra
recompensa: xp 10, oro 10
```

#### Escena
Si se acerca una tormenta, la Cúpula tiene que cerrarse con una sola tecla: Escape.

#### Gheco sugiere
`keydown` recibe un `KeyboardEvent`, que tiene `key`: el nombre de la tecla (`'Escape'`, `'Enter'`, `'a'`…).

```ts
document.addEventListener('keydown', (e: KeyboardEvent) => {
  if (e.key === 'Escape') { … }
});
```

#### Desafío
Completá la pregunta por la tecla.

#### Pasos
1. Buscá el `___` en el `if`.
2. Cambialo por `e.key === 'Escape'`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1326; color: #e8d9b0; padding: 24px; }
  #cartel { font-size: 24px; color: #f2c14e; }
</style>
<p id="cartel">Cúpula abierta</p>
```

#### Eventos
```
tecla a
tecla Escape
```

#### Estado
```
#cartel
```

#### Código inicial
```typescript
const cartel = document.querySelector('#cartel');

document.addEventListener('keydown', (e: KeyboardEvent) => {
  if (___ && cartel) cartel.textContent = 'Cúpula cerrada por tormenta';
});
```

#### Salida esperada
```
── Estado ──
#cartel: Cúpula cerrada por tormenta
```

#### Solución
```typescript
const cartel = document.querySelector('#cartel');

document.addEventListener('keydown', (e: KeyboardEvent) => {
  if (e.key === 'Escape' && cartel) cartel.textContent = 'Cúpula cerrada por tormenta';
});
```

#### Al superarla
La primera tecla no hace nada; con Escape, todos los gajos se cierran de golpe. Afuera empiezan a caer las primeras gotas.

#### Imagen
- La cúpula de latón cerrándose rápido mientras se ven nubes de tormenta por la última rendija.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) aprieta una tecla grande de bronce.
- Gheco con un paraguitas.

### Micro-misión R04-N04-P5 · El formulario de pedidos

```meta
lugar: El tablero de la Cúpula
personajes: Rigel, Gheco, Astrea
carta: SubmitEvent | form?.addEventListener('submit', (e: SubmitEvent) => { e.preventDefault(); … }) · los input con su tipo · value es texto
recompensa: xp 15, monedas 5
```

#### Escena
Astrea quiere pedir piezas desde el tablero: escribe la pieza y la cantidad, y aprieta *Pedir*. El tablero tiene que anotar el pedido sin recargar la página.

#### Gheco sugiere
El envío de un formulario es un `SubmitEvent`. Con `e.preventDefault()` no se recarga la página. Cada `input` se busca con su tipo (`HTMLInputElement`), y `value` es texto: la cantidad se convierte con `Number`.

#### Desafío
Completá el tipo de los dos `input`.

#### Pasos
1. En los dos `querySelector` de los `input`, el `___` es `<HTMLInputElement>`.
2. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1326; color: #e8d9b0; padding: 24px; }
  #pedido { font-size: 20px; color: #f2c14e; }
</style>
<form id="pedir">
  <input id="pieza" placeholder="Pieza">
  <input id="cantidad" type="number" placeholder="Cantidad">
  <button>Pedir</button>
</form>
<p id="pedido">—</p>
```

#### Eventos
```
escribir #pieza lente
escribir #cantidad 3
enviar #pedir
```

#### Estado
```
#pedido
```

#### Código inicial
```typescript
const form = document.querySelector<HTMLFormElement>('#pedir');
const pieza = document.querySelector___('#pieza');
const cantidad = document.querySelector___('#cantidad');
const pedido = document.querySelector('#pedido');

form?.addEventListener('submit', (e: SubmitEvent) => {
  e.preventDefault();
  if (!pieza || !cantidad || !pedido) return;
  const n = Number(cantidad.value);
  pedido.textContent = `Pedido: ${n} × ${pieza.value} (${n * 2} estrellas)`;
});
```

#### Salida esperada
```
── Estado ──
#pedido: Pedido: 3 × lente (6 estrellas)
```

#### Solución
```typescript
const form = document.querySelector<HTMLFormElement>('#pedir');
const pieza = document.querySelector<HTMLInputElement>('#pieza');
const cantidad = document.querySelector<HTMLInputElement>('#cantidad');
const pedido = document.querySelector('#pedido');

form?.addEventListener('submit', (e: SubmitEvent) => {
  e.preventDefault();
  if (!pieza || !cantidad || !pedido) return;
  const n = Number(cantidad.value);
  pedido.textContent = `Pedido: ${n} × ${pieza.value} (${n * 2} estrellas)`;
});
```

#### Al superarla
El pedido aparece en el cartel y sale por el tubo hacia la Ciudadela. Astrea le da a Rigel una **estrella de latón**.

#### Imagen
- Un formulario de latón con dos casilleros y un botón en el tablero de control, y un cartel de luz con el pedido.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mira el cartel; Gheco junto al tubo neumático.

### Micro-misión R04-N04-P6 · El tablero completo

```meta
lugar: El tablero de la Cúpula
personajes: Rigel, Gheco, Astrea
carta: Todo junto | preguntar una vez y cortar si falta · function no ve esa pregunta: una flecha en una const sí · eventos de click y teclado
recompensa: xp 15, monedas 5
```

#### Escena
Rigel termina el tablero: dos botones para abrir y cerrar gajos, el cartel que cuenta, y la tecla Escape que cierra todo.

#### Gheco sugiere
Para no preguntar por cada elemento en cada evento, se pregunta una sola vez al principio y se corta si falta alguno:

```ts
if (!abrir || !cerrar || !cartel) throw new Error('Falta un control del tablero');
```

Después de esa línea, TypeScript sabe que los tres están… **salvo** adentro de una función escrita con `function`: esas se pueden llamar desde cualquier lado (hasta antes de la pregunta), y TypeScript no se arriesga. Una función flecha guardada en una `const`, creada **después** de la pregunta, sí lo sabe:

```ts
const mostrar = (): void => { … };
```

#### Desafío
Agregá la línea que corta si falta algún control, y pasá `mostrar` a una función flecha.

#### Pasos
1. En el `___`, escribí `if (!abrir || !cerrar || !cartel) throw new Error('Falta un control del tablero');`.
2. Ejecutá: adentro de `function mostrar` todavía dice que `cartel` puede ser `null`.
3. Cambiá `function mostrar(): void {` por `const mostrar = (): void => {`, y la `}` que la cierra por `};`.
4. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1326; color: #e8d9b0; padding: 24px; }
  #cartel { font-size: 24px; color: #f2c14e; }
</style>
<button id="abrir">Abrir</button>
<button id="cerrar">Cerrar</button>
<p id="cartel">Gajos abiertos: 0</p>
```

#### Eventos
```
click #abrir
click #abrir
click #abrir
click #cerrar
tecla Escape
click #abrir
```

#### Estado
```
#cartel
```

#### Código inicial
```typescript
const abrir = document.querySelector<HTMLButtonElement>('#abrir');
const cerrar = document.querySelector<HTMLButtonElement>('#cerrar');
const cartel = document.querySelector<HTMLParagraphElement>('#cartel');
let abiertos = 0;

___

function mostrar(): void {
  cartel.textContent = `Gajos abiertos: ${abiertos}`;
}

abrir.addEventListener('click', () => {
  abiertos = Math.min(8, abiertos + 1);
  mostrar();
});
cerrar.addEventListener('click', () => {
  abiertos = Math.max(0, abiertos - 1);
  mostrar();
});
document.addEventListener('keydown', (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    abiertos = 0;
    mostrar();
  }
});
```

#### Salida esperada
```
── Estado ──
#cartel: Gajos abiertos: 1
```

#### Solución
```typescript
const abrir = document.querySelector<HTMLButtonElement>('#abrir');
const cerrar = document.querySelector<HTMLButtonElement>('#cerrar');
const cartel = document.querySelector<HTMLParagraphElement>('#cartel');
let abiertos = 0;

if (!abrir || !cerrar || !cartel) throw new Error('Falta un control del tablero');

const mostrar = (): void => {
  cartel.textContent = `Gajos abiertos: ${abiertos}`;
};

abrir.addEventListener('click', () => {
  abiertos = Math.min(8, abiertos + 1);
  mostrar();
});
cerrar.addEventListener('click', () => {
  abiertos = Math.max(0, abiertos - 1);
  mostrar();
});
document.addEventListener('keydown', (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    abiertos = 0;
    mostrar();
  }
});
```

#### Al superarla
El tablero queda completo: abre, cierra y se cierra entero con Escape. Astrea le da a Rigel una **estrella de latón**.

#### Imagen
- El tablero de control de latón completo, con dos botones, un cartel de luz y una tecla de emergencia, y la cúpula arriba con un gajo abierto.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sonríe; Gheco sobre la tecla de emergencia.

## R04-N05 · El lienzo y el bucle tipados

```meta
tipo: tema
padre: R04-N04
precio: 10
criatura: orc
temas: juegos.bucle, cal.tipos
```

### Crónica

En el tablero de la Cúpula hay una pantalla de vidrio ahumado: el **lienzo**, donde el Mirador dibuja el recorrido de las estrellas. Rigel quiere animar ahí una estrella que cruce el cielo. Cuando empieza, el compilador le avisa algo raro: que el pincel podría no existir.

—El lienzo siempre está —dice {mentor}—, pero el compilador no lo sabe. Preguntá una vez, guardá la respuesta con su medida, y después dibujá tranquilo.

### Objetivos

- Pedir el lienzo con su tipo (`HTMLCanvasElement`) y el pincel (`getContext('2d')`), que puede ser `null`.
- Describir el estado del juego con una `interface`.
- Tipar el bucle de `requestAnimationFrame`: el tiempo es un `number` (`DOMHighResTimeStamp`).
- Esquivar la trampa de las funciones: la pregunta de afuera no llega adentro de una `function`.

### Antes de empezar

- R04-N04: la página tipada.
- De JavaScript: el lienzo y el bucle del juego (en el curso de JavaScript, R05).

### Explicación

#### El pincel que podría no estar
```typescript
const lienzo = document.querySelector<HTMLCanvasElement>('#lienzo');
if (!lienzo) throw new Error('Falta el lienzo');
const ctx = lienzo.getContext('2d');   // CanvasRenderingContext2D | null
if (!ctx) throw new Error('Este navegador no dibuja en 2D');
```

#### El estado del juego, con su forma
```typescript
interface Estrella {
  x: number;
  y: number;
  vx: number;
  radio: number;
}
```

Si mañana agregás `vy`, el compilador te avisa en cada lugar donde se crea una estrella sin ella.

#### La trampa de las funciones
```typescript
if (!ctx) throw new Error('…');

function cuadro(ahora: number): void {
  ctx.fillRect(0, 0, 10, 10);   // ✗ TS18047: acá adentro, ctx puede ser null
}
```

Una `function` se puede llamar desde cualquier lado, así que TypeScript no se fija en lo que preguntaste afuera. Dos salidas:
- guardar el pincel en una constante nueva, con el tipo ya sin `null`: `const pincel: CanvasRenderingContext2D = ctx;`;
- o usar una función flecha en una `const`, creada después de la pregunta.

### Código de ejemplo

```typescript
interface Estrella {
  x: number;
  vx: number;
}

const estrella: Estrella = { x: 0, vx: 60 };
let antes = 0;

function avanzar(e: Estrella, dt: number): void {
  e.x += e.vx * dt;
}

for (const ahora of [0, 500, 1000]) {
  avanzar(estrella, (ahora - antes) / 1000);
  antes = ahora;
  console.log(`a los ${ahora} ms: x = ${estrella.x}`);
}
```

### Salida esperada

```
a los 0 ms: x = 0
a los 500 ms: x = 30
a los 1000 ms: x = 60
```

### ¿Para qué sirve?

Los juegos tienen mucho estado (posiciones, velocidades, vidas, puntos) que cambia sesenta veces por segundo. Con el estado descrito en interfaces, un error de tipeo en una propiedad aparece al compilar, y no como una estrella que desaparece de la pantalla sin explicación.

### Errores habituales

**Orco: el pincel sin preguntar (TS18047).** *"ctx" es posiblemente "null"*. Preguntá una vez con `if (!ctx) throw …`.

**Orco: la pregunta que no llega a la función.** Adentro de una `function`, la pregunta de afuera no cuenta: guardá el pincel en una constante con su tipo, o usá una flecha.

**Esqueleto: un estado incompleto (TS2741).** Si la `interface` pide `vx`, toda estrella nueva tiene que tenerla.

### Micro-misión R04-N05-P1 · El primer trazo

```meta
lugar: El tablero de la Cúpula
personajes: Rigel, Gheco
criatura: orc
carta: getContext tipado | querySelector<HTMLCanvasElement> · getContext('2d') puede ser null · if (!ctx) throw …
recompensa: xp 10, oro 10
```

#### Escena
Rigel quiere dibujar una estrella en el lienzo del tablero. El compilador no lo deja: el pincel podría no existir.

#### Gheco sugiere
`getContext('2d')` devuelve el pincel **o** `null` (si el navegador no dibuja en 2D). Se pregunta una vez:

```ts
const ctx = lienzo.getContext('2d');
if (!ctx) throw new Error('Este navegador no dibuja en 2D');
```

Después, `ctx` ya es un `CanvasRenderingContext2D`.

#### Desafío
Agregá la pregunta por el pincel.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el `___`, escribí `if (!ctx) throw new Error('Este navegador no dibuja en 2D');`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1326; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="100"></canvas>
```

#### Estado
```
lienzo
```

#### Código inicial
```typescript
const lienzo = document.querySelector<HTMLCanvasElement>('#lienzo');
if (!lienzo) throw new Error('Falta el lienzo');
const ctx = lienzo.getContext('2d');
___
ctx.fillStyle = '#f2c14e';
ctx.fillRect(90, 40, 20, 20);
```

#### Salida esperada
```
── Estado ──
lienzo: fillRect(90, 40, 20, 20) #f2c14e
```

#### Solución
```typescript
const lienzo = document.querySelector<HTMLCanvasElement>('#lienzo');
if (!lienzo) throw new Error('Falta el lienzo');
const ctx = lienzo.getContext('2d');
if (!ctx) throw new Error('Este navegador no dibuja en 2D');
ctx.fillStyle = '#f2c14e';
ctx.fillRect(90, 40, 20, 20);
```

#### Al superarla
Un cuadradito dorado aparece en el centro del vidrio ahumado: la primera estrella del lienzo.

#### Imagen
- Una pantalla de vidrio ahumado enmarcada en latón, en el tablero de control, con un punto dorado brillando en el centro.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) sostiene un pincel de luz.
- Gheco sobre el marco.

### Micro-misión R04-N05-P2 · La ficha de la estrella

```meta
lugar: El tablero de la Cúpula
personajes: Rigel, Gheco
carta: Estado con interface | interface Estrella { x: number; y: number; lado: number } · todo lo que se dibuja sale de ahí
recompensa: xp 10, oro 10
```

#### Escena
Para animar la estrella, Rigel necesita guardar dónde está y qué tamaño tiene. Lo escribe en una ficha.

#### Gheco sugiere
El estado del juego se describe con una `interface`. Todo lo que se dibuja sale de ahí:

```ts
ctx.fillRect(e.x, e.y, e.lado, e.lado);
```

#### Desafío
Completá la `interface` con las tres propiedades.

#### Pasos
1. Buscá el `___` adentro de `interface Estrella`.
2. Cambialo por `x: number; y: number; lado: number;`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1326; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="100"></canvas>
```

#### Estado
```
lienzo
```

#### Código inicial
```typescript
interface Estrella {
  ___
}

const lienzo = document.querySelector<HTMLCanvasElement>('#lienzo');
const ctx = lienzo?.getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');

const vega: Estrella = { x: 30, y: 20, lado: 12 };
ctx.fillStyle = '#f2c14e';
ctx.fillRect(vega.x, vega.y, vega.lado, vega.lado);
```

#### Salida esperada
```
── Estado ──
lienzo: fillRect(30, 20, 12, 12) #f2c14e
```

#### Solución
```typescript
interface Estrella {
  x: number; y: number; lado: number;
}

const lienzo = document.querySelector<HTMLCanvasElement>('#lienzo');
const ctx = lienzo?.getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');

const vega: Estrella = { x: 30, y: 20, lado: 12 };
ctx.fillStyle = '#f2c14e';
ctx.fillRect(vega.x, vega.y, vega.lado, vega.lado);
```

#### Al superarla
Vega aparece arriba a la izquierda del lienzo, en el lugar que dice su ficha.

#### Imagen
- El lienzo de vidrio ahumado con una estrella cuadrada dorada arriba a la izquierda y una ficha de cartulina al lado.
- Rigel (chico flaco con pecas, antiparras de latón) anota la ficha.
- Gheco señala la estrella.

### Micro-misión R04-N05-P3 · La estrella que cruza

```meta
lugar: El tablero de la Cúpula
personajes: Rigel, Gheco
carta: Bucle tipado | function cuadro(ahora: number): void · requestAnimationFrame(cuadro) · dt = (ahora - antes) / 1000
recompensa: xp 10, oro 10
```

#### Escena
Rigel quiere que Vega cruce el lienzo de izquierda a derecha, a 60 píxeles por segundo.

#### Gheco sugiere
`requestAnimationFrame` llama a la función de cada cuadro con el **tiempo** en milisegundos (un `number`). Con la diferencia entre dos cuadros se calcula cuánto avanzar:

```ts
const dt = (ahora - antes) / 1000;   // segundos
e.x += e.vx * dt;
```

Acá el pincel se guarda en una constante con su tipo (`pincel`), para usarlo adentro de la función sin problemas.

#### Desafío
Completá el tipo del parámetro `ahora`.

#### Pasos
1. Buscá el `___` en `function cuadro(ahora: ___)`.
2. Cambialo por `number`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1326; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="100"></canvas>
```

#### Eventos
```
cuadros 60
```

#### Estado
```
lienzo
```

#### Código inicial
```typescript
interface Estrella {
  x: number;
  y: number;
  vx: number;
}

const ctx = document.querySelector<HTMLCanvasElement>('#lienzo')?.getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;

const vega: Estrella = { x: 0, y: 40, vx: 60 };
let antes = 0;

function cuadro(ahora: ___): void {
  const dt = (ahora - antes) / 1000;
  antes = ahora;
  vega.x += vega.vx * dt;
  pincel.clearRect(0, 0, 200, 100);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(Math.round(vega.x), vega.y, 12, 12);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame((ahora) => {
  antes = ahora;
  requestAnimationFrame(cuadro);
});
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 200, 100)
lienzo: fillRect(59, 40, 12, 12) #f2c14e
```

#### Solución
```typescript
interface Estrella {
  x: number;
  y: number;
  vx: number;
}

const ctx = document.querySelector<HTMLCanvasElement>('#lienzo')?.getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;

const vega: Estrella = { x: 0, y: 40, vx: 60 };
let antes = 0;

function cuadro(ahora: number): void {
  const dt = (ahora - antes) / 1000;
  antes = ahora;
  vega.x += vega.vx * dt;
  pincel.clearRect(0, 0, 200, 100);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(Math.round(vega.x), vega.y, 12, 12);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame((ahora) => {
  antes = ahora;
  requestAnimationFrame(cuadro);
});
```

#### Al superarla
Vega cruza el lienzo despacito, dejando atrás un rastro que se borra en cada cuadro.

#### Imagen
- El lienzo de vidrio ahumado con una estrella dorada a mitad de camino y una estela tenue detrás.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) la sigue con la mirada.
- Gheco corriendo al lado del marco, como si la persiguiera.

### Micro-misión R04-N05-P4 · El pincel que se perdió

```meta
lugar: El tablero de la Cúpula
personajes: Rigel, Gheco
criatura: orc
carta: La trampa de las funciones | la pregunta de afuera no llega adentro de una function · const pincel: CanvasRenderingContext2D = ctx;
recompensa: xp 15, monedas 5
```

#### Escena
Rigel preguntó por el pincel afuera, pero adentro de la función del cuadro el compilador insiste en que podría ser `null`. Un **orco** se esconde en el pincel.

#### Gheco sugiere
Una `function` se puede llamar desde cualquier lado, así que TypeScript no usa lo que preguntaste afuera. La solución: guardar el pincel en una **constante nueva** con el tipo ya sin `null`, justo después de preguntar:

```ts
const pincel: CanvasRenderingContext2D = ctx;
```

Y adentro de la función usar `pincel`.

#### Desafío
Agregá la constante `pincel` y usala en la función.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el `___`, escribí `const pincel: CanvasRenderingContext2D = ctx;`.
3. Adentro de `cuadro`, cambiá los tres `ctx.` por `pincel.`.
4. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1326; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="100"></canvas>
```

#### Eventos
```
cuadros 30
```

#### Estado
```
lienzo
```

#### Código inicial
```typescript
const ctx = document.querySelector<HTMLCanvasElement>('#lienzo')?.getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
___

let x = 0;
function cuadro(): void {
  x += 2;
  ctx.clearRect(0, 0, 200, 100);
  ctx.fillStyle = '#f2c14e';
  ctx.fillRect(x, 44, 12, 12);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 200, 100)
lienzo: fillRect(60, 44, 12, 12) #f2c14e
```

#### Solución
```typescript
const ctx = document.querySelector<HTMLCanvasElement>('#lienzo')?.getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;

let x = 0;
function cuadro(): void {
  x += 2;
  pincel.clearRect(0, 0, 200, 100);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(x, 44, 12, 12);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
El pincel vuelve a la mano de Rigel y el orco se cae del tablero.

#### Imagen
- Un pincel de luz flotando sobre el lienzo y un orco chiquito cayéndose del tablero de control.
- Rigel (chico flaco con pecas, antiparras de latón, guantes sin dedos) atrapa el pincel.
- Gheco aplaude.

### Micro-misión R04-N05-P5 · Guiar la estrella

```meta
lugar: El tablero de la Cúpula
personajes: Rigel, Gheco, Astrea
carta: Teclado y estado tipados | Set<string> de teclas apretadas · interface del estado · el pincel con su tipo · el bucle mueve según las teclas
recompensa: xp 15, monedas 5
```

#### Escena
Astrea quiere guiar una estrella por el lienzo con las flechas del teclado, para mostrarle a Rigel por dónde pasa el cometa de esta noche.

#### Gheco sugiere
Las teclas apretadas se guardan en un `Set<string>`: `keydown` las agrega y `keyup` las saca. En cada cuadro, si está la flecha derecha, la estrella avanza.

#### Desafío
Completá las dos líneas del teclado.

#### Pasos
1. El primer `___` (en `keydown`): `teclas.add(e.key);`.
2. El segundo `___` (en `keyup`): `teclas.delete(e.key);`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1326; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="100"></canvas>
```

#### Eventos
```
apretar ArrowRight
cuadros 20
soltar ArrowRight
cuadros 10
```

#### Estado
```
lienzo
```

#### Código inicial
```typescript
interface Estrella {
  x: number;
  y: number;
  paso: number;
}

const ctx = document.querySelector<HTMLCanvasElement>('#lienzo')?.getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;

const cometa: Estrella = { x: 10, y: 44, paso: 3 };
const teclas = new Set<string>();

document.addEventListener('keydown', (e: KeyboardEvent) => {
  ___
});
document.addEventListener('keyup', (e: KeyboardEvent) => {
  ___
});

function cuadro(): void {
  if (teclas.has('ArrowRight')) cometa.x += cometa.paso;
  pincel.clearRect(0, 0, 200, 100);
  pincel.fillStyle = '#9ad1ff';
  pincel.fillRect(cometa.x, cometa.y, 12, 12);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 200, 100)
lienzo: fillRect(70, 44, 12, 12) #9ad1ff
```

#### Solución
```typescript
interface Estrella {
  x: number;
  y: number;
  paso: number;
}

const ctx = document.querySelector<HTMLCanvasElement>('#lienzo')?.getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;

const cometa: Estrella = { x: 10, y: 44, paso: 3 };
const teclas = new Set<string>();

document.addEventListener('keydown', (e: KeyboardEvent) => {
  teclas.add(e.key);
});
document.addEventListener('keyup', (e: KeyboardEvent) => {
  teclas.delete(e.key);
});

function cuadro(): void {
  if (teclas.has('ArrowRight')) cometa.x += cometa.paso;
  pincel.clearRect(0, 0, 200, 100);
  pincel.fillStyle = '#9ad1ff';
  pincel.fillRect(cometa.x, cometa.y, 12, 12);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
El cometa avanza mientras la flecha está apretada y se detiene al soltarla. Astrea le da a Rigel una **estrella de latón**: —Por ahí va a pasar esta noche.

#### Imagen
- El lienzo de vidrio ahumado con un cometa celeste a mitad de camino, y una tecla de flecha de latón en el tablero.
- Astrea (lechuza con anteojos de latón y chaleco azul) aprieta la tecla con un ala.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) recibe una ficha con una estrella; Gheco mira el cometa.

## R04-N06 · null en serio: strictNullChecks, ! y las opciones estrictas

```meta
tipo: tema
padre: R04-N05
precio: 10
criatura: orc
temas: cal.tipos, err.validacion
```

### Crónica

En la Cúpula, Rigel encuentra un tablero viejo, de antes del Vidriero, con una perilla oxidada que dice *revisar lo que falta*. Está apagada. Con la perilla apagada, nada avisa cuando una pieza no está, y las cosas se rompen de noche, en silencio.

—Esa perilla es `strictNullChecks` —dice {mentor}—. Viene prendida con `strict`, y es la que más errores ataja. Hay otras perillas más finas que podés prender. Y hay un atajo, el signo `!`, que es como taparla con la mano: usalo poco.

> Las opciones `noUncheckedIndexedAccess` y `exactOptionalPropertyTypes` no están en el material de base (FullCursos): se agregaron porque cada vez más proyectos las prenden.

### Objetivos

- Entender qué hace `strictNullChecks` y qué pasa sin él.
- Usar `?.` y `??`, y conocer el `!` (*non-null assertion*) y su peligro.
- Usar `!:` en una propiedad que se asigna más tarde (*definite assignment*).
- Conocer `noUncheckedIndexedAccess` (lo que sale de un arreglo o de un índice puede no estar) y `exactOptionalPropertyTypes`.

### Antes de empezar

- R03-N01 (descartar `null`), R04-N04 (la página) y R04-N05 (el lienzo).

### Explicación

#### Con la perilla prendida y apagada
Con `strictNullChecks` (que viene con `strict`), `null` y `undefined` **no** entran en cualquier tipo: hay que decirlo (`string | null`) y preguntar antes de usar. Sin la perilla, `let nombre: string = null` compila, y el error aparece al ejecutar.

> En las micro-misiones, la sección **tsconfig** (debajo del editor, en el tablero) dice si alguna perilla está distinta en esa micro-misión.

#### El signo ! : «confiá en mí»
```typescript
const lienzo = document.querySelector('#lienzo')!;   // le dice al compilador: no es null
```

`!` **no revisa nada**: solo calla al compilador. Si te equivocás, el error aparece al ejecutar, como en JavaScript. Usalo solo cuando estés **seguro** (por ejemplo, un elemento que vos mismo pusiste en la página).

#### Asignada más tarde: !:
```typescript
class Telescopio {
  objetivo!: string;          // se asigna en preparar(), no en el constructor
  preparar(): void { this.objetivo = 'Vega'; }
}
```

#### Perillas más finas
- **`noUncheckedIndexedAccess`**: lo que sale de `lista[i]` o de `registro[clave]` es `T | undefined`, porque ese lugar podría no existir. Obliga a usar `??` o preguntar.
- **`exactOptionalPropertyTypes`**: una propiedad opcional (`estrella?: string`) se **omite**: no se le puede poner `undefined` a mano.

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

### Código de ejemplo

```typescript
const catalogo = new Map<string, number>([['Vega', 25]]);

const vega = catalogo.get('Vega') ?? 0;
const polar = catalogo.get('Polar') ?? 0;

const nombres: string[] = ['Vega', 'Sirio'];
const tercera = nombres[5] ?? 'ninguna';

console.log(vega, polar, tercera);
```

### Salida esperada

```
25 0 ninguna
```

### ¿Para qué sirve?

El error más común de JavaScript es *Cannot read properties of undefined*. `strictNullChecks` lo ataja casi siempre, y las perillas finas atajan lo que queda: un índice que no existe o una clave que no está. El `!` es útil, pero cada uno es un lugar donde el compilador ya no te cuida.

### Errores habituales

**Orco: lo que puede no estar (TS18047 o TS18048).** Preguntá, o usá `?.` y `??`.

**Orco: el ! que mintió.** `mapa.get('Polar')!.toFixed(1)` compila y explota al ejecutar si no está. Cambialo por `?? 0`.

**Orco: con noUncheckedIndexedAccess, el índice (TS18048).** *"x" es posiblemente "undefined"*: ese lugar del arreglo podría no existir.

**Orco: undefined en una opcional (TS2375).** Con `exactOptionalPropertyTypes`, no pongas la propiedad en lugar de ponerle `undefined`.

### Micro-misión R04-N06-P1 · Sin la perilla

```meta
lugar: La Cúpula
personajes: Rigel, Gheco
criatura: orc
carta: strictNullChecks apagado | null entra en cualquier tipo · el error aparece al ejecutar · ?. y ?? protegen igual
recompensa: xp 10, oro 10
```

#### Escena
En el tablero viejo, la perilla de *revisar lo que falta* está apagada. El programa compila, pero explota al buscar una estrella que no está. Un **orco** se ríe.

#### Gheco sugiere
En esta micro-misión, la sección **tsconfig** apaga `strictNullChecks`. Por eso el compilador no avisa que `find` puede devolver `undefined`, y el programa explota al ejecutar.

Aunque la perilla esté apagada, `?.` y `??` protegen igual:

```ts
encontrada?.toUpperCase() ?? 'SIN ESTRELLA'
```

#### Desafío
Protegé la línea con `?.` y `??`.

#### Pasos
1. Tocá **Ejecutar**: compila y explota al ejecutar.
2. Cambiá `encontrada.toUpperCase()` por `encontrada?.toUpperCase() ?? 'SIN ESTRELLA'`.
3. Tocá **Ejecutar**. Tiene que salir `SIN ESTRELLA`.

#### tsconfig
```json
{ "strictNullChecks": false }
```

#### Código inicial
```typescript
const estrellas: string[] = ['Vega', 'Sirio'];
const encontrada = estrellas.find((e) => e === 'Polar');
console.log(encontrada.toUpperCase());
```

#### Salida esperada
```
SIN ESTRELLA
```

#### Solución
```typescript
const estrellas: string[] = ['Vega', 'Sirio'];
const encontrada = estrellas.find((e) => e === 'Polar');
console.log(encontrada?.toUpperCase() ?? 'SIN ESTRELLA');
```

#### Al superarla
Rigel prende la perilla oxidada, que cruje. —Prendida para siempre —dice.

#### Imagen
- Un tablero viejo y oxidado con una perilla grande apagada, y al lado el tablero nuevo brillante.
- Un orco chiquito riéndose detrás del tablero viejo.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) gira la perilla; Gheco mira.

### Micro-misión R04-N06-P2 · El signo que mintió

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco
criatura: orc
carta: El ! no revisa nada | mapa.get('Polar')! calla al compilador · si no estaba, explota al ejecutar · mejor ?? 0
recompensa: xp 10, oro 10
```

#### Escena
Rigel usó el signo `!` para que el compilador dejara de quejarse. Compiló… y explotó: Polar no estaba en el catálogo.

#### Gheco sugiere
`!` le dice al compilador «no es `undefined`, confiá». Pero **no revisa nada**: si te equivocás, explota al ejecutar. Acá, `get` devuelve `undefined` porque Polar no está.

Lo seguro es dar un valor si no está: `?? 0`.

#### Desafío
Cambiá el `!` por `?? 0`.

#### Pasos
1. Tocá **Ejecutar**: explota al ejecutar.
2. Cambiá `catalogo.get('Polar')!` por `(catalogo.get('Polar') ?? 0)`.
3. Tocá **Ejecutar**. Tiene que salir `Polar: 0.0 años luz`.

#### Código inicial
```typescript
const catalogo = new Map<string, number>([['Vega', 25]]);
const distancia = catalogo.get('Polar')!;
console.log(`Polar: ${distancia.toFixed(1)} años luz`);
```

#### Salida esperada
```
Polar: 0.0 años luz
```

#### Solución
```typescript
const catalogo = new Map<string, number>([['Vega', 25]]);
const distancia = (catalogo.get('Polar') ?? 0);
console.log(`Polar: ${distancia.toFixed(1)} años luz`);
```

#### Al superarla
Rigel tacha el signo `!` de su libreta con dos rayas. —Solo cuando esté seguro de verdad.

#### Imagen
- Una libreta abierta con un signo de exclamación enorme tachado con dos rayas.
- Rigel (chico flaco con pecas, antiparras de latón) con el lápiz en la mano.
- Gheco asintiendo.

### Micro-misión R04-N06-P3 · Asignada más tarde

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco
carta: Definite assignment | objetivo!: string · se asigna en otro método, no en el constructor · sin el !, TS2564
recompensa: xp 10, oro 10
```

#### Escena
El telescopio no sabe su objetivo cuando se construye: lo recibe después, cuando alguien lo prepara. El compilador se queja de que la propiedad no tiene valor.

#### Gheco sugiere
`objetivo!: string` le dice al compilador: «esta propiedad se va a asignar antes de usarse, aunque no sea en el constructor». Es un `!` también: usalo solo si lo vas a asignar seguro.

#### Desafío
Agregá el `!` a la propiedad.

#### Pasos
1. Tocá **Ejecutar** y leé el error (`TS2564`).
2. Cambiá `objetivo: string;` por `objetivo!: string;`.
3. Tocá **Ejecutar**. Tiene que salir `Apuntando a Vega`.

#### Código inicial
```typescript
class Telescopio {
  objetivo: string;

  preparar(estrella: string): void {
    this.objetivo = estrella;
  }

  apuntar(): string {
    return `Apuntando a ${this.objetivo}`;
  }
}

const t = new Telescopio();
t.preparar('Vega');
console.log(t.apuntar());
```

#### Salida esperada
```
Apuntando a Vega
```

#### Solución
```typescript
class Telescopio {
  objetivo!: string;

  preparar(estrella: string): void {
    this.objetivo = estrella;
  }

  apuntar(): string {
    return `Apuntando a ${this.objetivo}`;
  }
}

const t = new Telescopio();
t.preparar('Vega');
console.log(t.apuntar());
```

#### Al superarla
El telescopio gira hacia Vega. Antes de prepararlo no sabía dónde mirar; ahora sí.

#### Imagen
- El telescopio de latón girando hacia una estrella brillante por la cúpula abierta.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) ajusta la mira.
- Gheco sobre el tubo.

### Micro-misión R04-N06-P4 · El casillero que no existe

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco
criatura: orc
carta: noUncheckedIndexedAccess | lista[5] es T | undefined · obliga a usar ?? o preguntar · sin esa opción, el error aparece al ejecutar
recompensa: xp 10, oro 10
```

#### Escena
Rigel pide la sexta estrella de una lista de tres. Con la perilla fina de los índices prendida, el compilador lo frena antes de ejecutar.

#### Gheco sugiere
Con `noUncheckedIndexedAccess` (prendida en el **tsconfig** de esta micro-misión), lo que sale de `lista[i]` es `string | undefined`: ese lugar podría no existir. Hay que dar un valor si falta:

```ts
const sexta = lista[5] ?? 'ninguna';
```

#### Desafío
Agregá `?? 'ninguna'` a la lectura.

#### Pasos
1. Tocá **Ejecutar** y leé el error (`TS18048`).
2. Cambiá `const sexta = lista[5];` por `const sexta = lista[5] ?? 'ninguna';`.
3. Tocá **Ejecutar**. Tiene que salir `Sexta: NINGUNA`.

#### tsconfig
```json
{ "noUncheckedIndexedAccess": true }
```

#### Código inicial
```typescript
const lista: string[] = ['Vega', 'Sirio', 'Altair'];
const sexta = lista[5];
console.log(`Sexta: ${sexta.toUpperCase()}`);
```

#### Salida esperada
```
Sexta: NINGUNA
```

#### Solución
```typescript
const lista: string[] = ['Vega', 'Sirio', 'Altair'];
const sexta = lista[5] ?? 'ninguna';
console.log(`Sexta: ${sexta.toUpperCase()}`);
```

#### Al superarla
El casillero vacío ya no rompe nada. Rigel decide prender esa perilla en todos sus proyectos.

#### Imagen
- Un fichero de seis casilleros con tres ocupados por fichas de estrellas y tres vacíos, uno de ellos iluminado.
- Un orco chiquito asomado a un casillero vacío.
- Rigel (chico flaco con pecas, antiparras de latón) cierra el casillero; Gheco mira.

### Micro-misión R04-N06-P5 · La propiedad que se omite

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco
criatura: orc
carta: exactOptionalPropertyTypes | una opcional se omite · ponerle undefined es TS2375 · sacá la propiedad
recompensa: xp 15, monedas 5
```

#### Escena
Rigel registra una pieza sin estrella y le escribe `estrella: undefined`. Con la perilla de las opcionales prendida, el compilador no lo acepta.

#### Gheco sugiere
Con `exactOptionalPropertyTypes` (prendida en el **tsconfig** de esta micro-misión), una propiedad opcional (`estrella?: string`) significa «puede **no estar**», no «puede ser `undefined`». Si no hay estrella, la propiedad no se pone.

#### Desafío
Sacá la propiedad `estrella` del objeto.

#### Pasos
1. Tocá **Ejecutar** y leé el error (`TS2375`).
2. Cambiá `{ nombre: 'biela', estrella: undefined }` por `{ nombre: 'biela' }`.
3. Tocá **Ejecutar**. Tiene que salir `biela → cualquiera`.

#### tsconfig
```json
{ "exactOptionalPropertyTypes": true }
```

#### Código inicial
```typescript
interface Pieza {
  nombre: string;
  estrella?: string;
}

const biela: Pieza = { nombre: 'biela', estrella: undefined };
console.log(`${biela.nombre} → ${biela.estrella ?? 'cualquiera'}`);
```

#### Salida esperada
```
biela → cualquiera
```

#### Solución
```typescript
interface Pieza {
  nombre: string;
  estrella?: string;
}

const biela: Pieza = { nombre: 'biela' };
console.log(`${biela.nombre} → ${biela.estrella ?? 'cualquiera'}`);
```

#### Al superarla
La ficha de la biela queda limpia, sin un casillero de más.

#### Imagen
- Una ficha técnica de cartulina con un casillero borrado con goma.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sopla los restos de goma.
- Gheco estornuda.

### Micro-misión R04-N06-P6 · El registro con todas las perillas

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco, Astrea
carta: Todo junto | noUncheckedIndexedAccess en un registro · registro[clave] ?? 0 · ?. para lo opcional · nada de !
recompensa: xp 15, monedas 5
```

#### Escena
Astrea prende todas las perillas finas y le pide a Rigel el registro de las distancias. Algunas estrellas no están anotadas.

#### Gheco sugiere
Con `noUncheckedIndexedAccess`, `registro[nombre]` es `number | undefined`, aunque el registro sea un `Record<string, number>`: esa clave podría no estar.

#### Desafío
Completá la lectura del registro.

#### Pasos
1. Buscá el `___` en el `map`.
2. Cambialo por `registro[nombre] ?? 0`.
3. Tocá **Ejecutar**. Tiene que salir `Vega: 25 · Polar: 0 · Sirio: 9`.

#### tsconfig
```json
{ "noUncheckedIndexedAccess": true, "exactOptionalPropertyTypes": true }
```

#### Código inicial
```typescript
const registro: Record<string, number> = { Vega: 25, Sirio: 9 };
const pedidas = ['Vega', 'Polar', 'Sirio'];

const lineas = pedidas.map((nombre) => {
  const distancia: number = ___;
  return `${nombre}: ${distancia}`;
});
console.log(lineas.join(' · '));
```

#### Salida esperada
```
Vega: 25 · Polar: 0 · Sirio: 9
```

#### Solución
```typescript
const registro: Record<string, number> = { Vega: 25, Sirio: 9 };
const pedidas = ['Vega', 'Polar', 'Sirio'];

const lineas = pedidas.map((nombre) => {
  const distancia: number = registro[nombre] ?? 0;
  return `${nombre}: ${distancia}`;
});
console.log(lineas.join(' · '));
```

#### Al superarla
El registro sale completo, con un cero donde falta el dato. Astrea le da a Rigel una **estrella de latón**: —Las perillas prendidas no molestan: cuidan.

#### Imagen
- Un tablero con varias perillas de latón prendidas, todas con una lucecita verde.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) revisa el registro; Gheco sobre las perillas.

## R04-N07 · Decoradores

```meta
tipo: tema
padre: R04-N06
precio: 10
criatura: ogre
temas: func.orden-superior, poo.clases
```

### Crónica

En la Cúpula, cada motor tiene pegadas unas **chapitas de bronce** con una arroba grabada: `@anunciar`, `@medir`, `@repetir`. Rigel pregunta qué son. Don Péndulo, que subió a ver la tormenta, se ríe.

—Son **decoradores** —dice—. Envuelven una máquina sin abrirla: antes y después de que haga lo suyo, hacen algo más. Anunciar que arranca, medir cuánto tardó, repetir si falla. La máquina ni se entera.

### Objetivos

- Entender qué es un decorador: una función que envuelve un método o una clase.
- Usar un decorador de método (`@anunciar`) y uno de clase (`@registrada`).
- Escribir la parte de adentro de un decorador: hacer algo y llamar al original.
- Usar una **fábrica de decoradores**, con parámetros: `@repetir(3)`.

### Antes de empezar

- R01-N06 (tipos de función) y R02 (clases y genéricos).
- De JavaScript: funciones que reciben y devuelven funciones.

### Explicación

#### Envolver sin abrir
Un **decorador de método** es una función que recibe el método original y un `context` (con el nombre del método, entre otras cosas), y devuelve el método que se va a usar en su lugar:

```typescript
function anunciar<T, A extends unknown[], R>(
  original: (this: T, ...args: A) => R,
  context: ClassMethodDecoratorContext<T, (this: T, ...args: A) => R>,
) {
  return function (this: T, ...args: A): R {
    console.log(`→ ${String(context.name)}`);   // algo antes
    return original.call(this, ...args);        // la máquina de siempre
  };
}

class Cupula {
  @anunciar
  abrir(gajo: number): string {
    return `gajo ${gajo} abierto`;
  }
}
```

La firma parece difícil, pero dice algo simple: «recibo un método que tiene un `this` (`T`), unos argumentos (`A`) y un resultado (`R`), y devuelvo otro método igual». Lo importante está adentro: hacer algo y llamar al original con `original.call(this, ...args)`.

> `@anunciar` arriba de `abrir` es lo mismo que escribir, a mano, `abrir = anunciar(abrir, contexto)`.

#### Decorador de clase
```typescript
const registro: string[] = [];
function registrada(_clase: unknown, context: ClassDecoratorContext) {
  registro.push(String(context.name));
}

@registrada
class Barometro {}
```

#### Con parámetros: una fábrica
```typescript
function repetir(veces: number) {
  return function <T, A extends unknown[]>(original: (this: T, ...args: A) => void, _context: ClassMethodDecoratorContext) {
    return function (this: T, ...args: A): void {
      for (let i = 0; i < veces; i++) original.call(this, ...args);
    };
  };
}
```

`@repetir(3)` llama a `repetir(3)`, que **devuelve** el decorador.

> Estos son los decoradores **estándar** de JavaScript, los que TypeScript trae desde la versión 5. Algunos frameworks viejos (Angular, NestJS) usan otros, los «experimentales», que se escriben distinto: si los ves, son parecidos pero no iguales.

### Código de ejemplo

```typescript
function anunciar<T, A extends unknown[], R>(
  original: (this: T, ...args: A) => R,
  context: ClassMethodDecoratorContext<T, (this: T, ...args: A) => R>,
) {
  return function (this: T, ...args: A): R {
    console.log(`→ ${String(context.name)}`);
    return original.call(this, ...args);
  };
}

const registro: string[] = [];
function registrada(_clase: unknown, context: ClassDecoratorContext) {
  registro.push(String(context.name));
}

@registrada
class Cupula {
  @anunciar
  abrir(gajo: number): string {
    return `gajo ${gajo} abierto`;
  }
}

console.log(new Cupula().abrir(2));
console.log('Registradas:', registro);
```

### Salida esperada

```
→ abrir
gajo 2 abierto
Registradas: [ 'Cupula' ]
```

### ¿Para qué sirve?

Muchos frameworks usan decoradores para marcar qué hace cada parte: una ruta de un servidor (`@Get('/usuarios')`), un componente, una propiedad que se guarda en la base. Y sirven para cosas que se repiten en muchos métodos: registrar en un log, medir tiempos, revisar permisos, reintentar.

### Errores habituales

**Ogro: olvidarse de llamar al original.** Si el decorador no hace `original.call(this, ...args)`, el método deja de hacer lo suyo.

**Ogro: perder el this.** `original(...args)` (sin `.call(this, …)`) llama al método sin su objeto: adentro, `this` es `undefined`.

**Esqueleto: la fábrica sin paréntesis.** Si `repetir` recibe parámetros, se usa `@repetir(3)`, no `@repetir`.

### Micro-misión R04-N07-P1 · La chapita de anunciar

```meta
lugar: La Cúpula
personajes: Rigel, Gheco, Don Péndulo
carta: Usar un decorador | @anunciar arriba del método · lo envuelve sin cambiarlo
recompensa: xp 10, oro 10
```

#### Escena
Don Péndulo le da a Rigel una chapita `@anunciar` para el motor de los gajos: que cada vez que arranque, lo anuncie.

#### Gheco sugiere
Un decorador se pone **arriba** del método, con una arroba:

```ts
@anunciar
abrir(gajo: number): string { … }
```

El decorador ya está escrito: solo hay que pegarlo.

#### Desafío
Poné el decorador arriba del método `abrir`.

#### Pasos
1. Buscá el `___` arriba de `abrir`.
2. Cambialo por `@anunciar`.
3. Tocá **Ejecutar**. Tiene que salir `→ abrir` y `gajo 2 abierto`.

#### Código inicial
```typescript
function anunciar<T, A extends unknown[], R>(
  original: (this: T, ...args: A) => R,
  context: ClassMethodDecoratorContext<T, (this: T, ...args: A) => R>,
) {
  return function (this: T, ...args: A): R {
    console.log(`→ ${String(context.name)}`);
    return original.call(this, ...args);
  };
}

class Cupula {
  ___
  abrir(gajo: number): string {
    return `gajo ${gajo} abierto`;
  }
}

console.log(new Cupula().abrir(2));
```

#### Salida esperada
```
→ abrir
gajo 2 abierto
```

#### Solución
```typescript
function anunciar<T, A extends unknown[], R>(
  original: (this: T, ...args: A) => R,
  context: ClassMethodDecoratorContext<T, (this: T, ...args: A) => R>,
) {
  return function (this: T, ...args: A): R {
    console.log(`→ ${String(context.name)}`);
    return original.call(this, ...args);
  };
}

class Cupula {
  @anunciar
  abrir(gajo: number): string {
    return `gajo ${gajo} abierto`;
  }
}

console.log(new Cupula().abrir(2));
```

#### Al superarla
El motor anuncia que arranca con un silbido, y el gajo se abre.

#### Imagen
- Un motor de vapor de latón con una chapita de bronce pegada que tiene una arroba grabada.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) pega la chapita.
- Don Péndulo (relojero viejo de barba blanca, delantal de cuero) mira con la lupa; Gheco sobre el motor.

### Micro-misión R04-N07-P2 · Lo de antes y lo de después

```meta
lugar: La Cúpula
personajes: Rigel, Gheco
criatura: ogre
carta: Adentro del decorador | algo antes · const resultado = original.call(this, ...args) · algo después · return resultado
recompensa: xp 10, oro 10
```

#### Escena
Rigel quiere un decorador que avise cuándo empieza y cuándo termina cada maniobra de la Cúpula.

#### Gheco sugiere
Adentro del decorador se puede hacer algo **antes** y algo **después** del original:

```ts
console.log('empieza');
const resultado = original.call(this, ...args);
console.log('termina');
return resultado;
```

`original.call(this, ...args)` llama al método de siempre, con su objeto (`this`) y sus argumentos.

#### Desafío
Completá la línea que llama al método original.

#### Pasos
1. Buscá el `___` adentro del decorador.
2. Cambialo por `const resultado = original.call(this, ...args);`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
function bitacora<T, A extends unknown[], R>(
  original: (this: T, ...args: A) => R,
  context: ClassMethodDecoratorContext<T, (this: T, ...args: A) => R>,
) {
  return function (this: T, ...args: A): R {
    console.log(`empieza ${String(context.name)}`);
    ___
    console.log(`termina ${String(context.name)}`);
    return resultado;
  };
}

class Cupula {
  @bitacora
  cerrar(): string {
    return 'cúpula cerrada';
  }
}

console.log(new Cupula().cerrar());
```

#### Salida esperada
```
empieza cerrar
termina cerrar
cúpula cerrada
```

#### Solución
```typescript
function bitacora<T, A extends unknown[], R>(
  original: (this: T, ...args: A) => R,
  context: ClassMethodDecoratorContext<T, (this: T, ...args: A) => R>,
) {
  return function (this: T, ...args: A): R {
    console.log(`empieza ${String(context.name)}`);
    const resultado = original.call(this, ...args);
    console.log(`termina ${String(context.name)}`);
    return resultado;
  };
}

class Cupula {
  @bitacora
  cerrar(): string {
    return 'cúpula cerrada';
  }
}

console.log(new Cupula().cerrar());
```

#### Al superarla
La bitácora de la Cúpula anota cada maniobra, de principio a fin.

#### Imagen
- Una bitácora de cuero abierta junto al tablero de la cúpula, con renglones de entrada y salida.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) escribe en ella.
- Gheco sostiene el tintero.

### Micro-misión R04-N07-P3 · El this perdido

```meta
lugar: La Cúpula
personajes: Rigel, Gheco
criatura: ogre
carta: original.call(this, …) | sin el call, el método pierde su objeto · this queda undefined · el error aparece al ejecutar
recompensa: xp 10, oro 10
```

#### Escena
Un **ogro** escribió un decorador apurado: llama al método original sin su objeto. Al ejecutar, el motor no encuentra su propio nombre.

#### Gheco sugiere
`original(...args)` llama al método **sin** su objeto: adentro, `this` es `undefined` y `this.nombre` explota. Con `original.call(this, ...args)` se lo pasa.

#### Desafío
Cambiá la llamada por una que pase el `this`.

#### Pasos
1. Tocá **Ejecutar**: explota al ejecutar.
2. Cambiá `return original(...args);` por `return original.call(this, ...args);`.
3. Tocá **Ejecutar**. Tiene que salir `→ arrancar` y `motor M-1 en marcha`.

#### Código inicial
```typescript
function anunciar<T, A extends unknown[], R>(
  original: (this: T, ...args: A) => R,
  context: ClassMethodDecoratorContext<T, (this: T, ...args: A) => R>,
) {
  return function (this: T, ...args: A): R {
    console.log(`→ ${String(context.name)}`);
    return (original as (...args: A) => R)(...args);
  };
}

class Motor {
  constructor(public nombre: string) {}

  @anunciar
  arrancar(): string {
    return `motor ${this.nombre} en marcha`;
  }
}

console.log(new Motor('M-1').arrancar());
```

#### Salida esperada
```
→ arrancar
motor M-1 en marcha
```

#### Solución
```typescript
function anunciar<T, A extends unknown[], R>(
  original: (this: T, ...args: A) => R,
  context: ClassMethodDecoratorContext<T, (this: T, ...args: A) => R>,
) {
  return function (this: T, ...args: A): R {
    console.log(`→ ${String(context.name)}`);
    return original.call(this, ...args);
  };
}

class Motor {
  constructor(public nombre: string) {}

  @anunciar
  arrancar(): string {
    return `motor ${this.nombre} en marcha`;
  }
}

console.log(new Motor('M-1').arrancar());
```

#### Al superarla
El motor recupera su nombre y arranca. El ogro se rasca la cabeza: no entiende qué pasó.

#### Imagen
- Un motor de vapor con su placa de nombre (sin letras legibles) arrancando, con humo blanco.
- Un ogro chiquito rascándose la cabeza.
- Rigel (chico flaco con pecas, antiparras de latón, guantes sin dedos) ajusta una pieza; Gheco mira.

### Micro-misión R04-N07-P4 · El registro de los instrumentos

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: Decorador de clase | @registrada arriba de class · recibe la clase y su context · context.name es el nombre de la clase
recompensa: xp 15, monedas 5
```

#### Escena
Astrea quiere una lista de todos los instrumentos del Mirador, sin tener que acordarse de anotarlos. Que cada clase se anote sola al crearse.

#### Gheco sugiere
Un **decorador de clase** va arriba de `class` y recibe la clase y un `context`. `context.name` es el nombre de la clase:

```ts
function registrada(_clase: unknown, context: ClassDecoratorContext) {
  registro.push(String(context.name));
}
```

El guion bajo en `_clase` dice «no la uso».

#### Desafío
Completá la línea del registro y decorá las dos clases.

#### Pasos
1. En el `___` de `registrada`, escribí `registro.push(String(context.name));`.
2. Arriba de las dos clases, cambiá los `___` por `@registrada`.
3. Tocá **Ejecutar**. Tiene que salir `Instrumentos: Termometro, Barometro`.

#### Código inicial
```typescript
const registro: string[] = [];

function registrada(_clase: unknown, context: ClassDecoratorContext) {
  ___
}

___
class Termometro {}

___
class Barometro {}

console.log(`Instrumentos: ${registro.join(', ')}`);
```

#### Salida esperada
```
Instrumentos: Termometro, Barometro
```

#### Solución
```typescript
const registro: string[] = [];

function registrada(_clase: unknown, context: ClassDecoratorContext) {
  registro.push(String(context.name));
}

@registrada
class Termometro {}

@registrada
class Barometro {}

console.log(`Instrumentos: ${registro.join(', ')}`);
```

#### Al superarla
El libro de inventario del Mirador se llena solo, a medida que se fabrican los instrumentos.

#### Imagen
- Un libro de inventario abierto con renglones que se escriben solos con tinta de luz.
- Astrea (lechuza con anteojos de latón y chaleco azul) mira el libro.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sostiene un termómetro y un barómetro; Gheco sobre el libro.

### Micro-misión R04-N07-P5 · Repetir hasta que salga

```meta
lugar: La Cúpula
personajes: Rigel, Gheco, Don Péndulo
carta: Fábrica de decoradores | function repetir(veces: number) { return function (original, context) { … } } · se usa @repetir(3)
recompensa: xp 15, monedas 5
```

#### Escena
Los gajos viejos a veces no cierran del todo. Don Péndulo propone empujarlos varias veces: tres para los viejos, una para los nuevos.

#### Gheco sugiere
Un decorador **con parámetros** es una función que **devuelve** un decorador:

```ts
function repetir(veces: number) {
  return function (original, context) { … };
}
```

Se usa con paréntesis: `@repetir(3)`.

#### Desafío
Completá el `for` adentro del decorador y decorá `empujar` con `@repetir(3)`.

#### Pasos
1. En el `___` del decorador: `for (let i = 0; i < veces; i++) original.call(this, ...args);`.
2. Arriba de `empujar`, el `___` es `@repetir(3)`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
function repetir(veces: number) {
  return function <T, A extends unknown[]>(original: (this: T, ...args: A) => void, _context: ClassMethodDecoratorContext) {
    return function (this: T, ...args: A): void {
      ___
    };
  };
}

class GajoViejo {
  constructor(public numero: number) {}

  ___
  empujar(): void {
    console.log(`empujo el gajo ${this.numero}`);
  }
}

new GajoViejo(4).empujar();
```

#### Salida esperada
```
empujo el gajo 4
empujo el gajo 4
empujo el gajo 4
```

#### Solución
```typescript
function repetir(veces: number) {
  return function <T, A extends unknown[]>(original: (this: T, ...args: A) => void, _context: ClassMethodDecoratorContext) {
    return function (this: T, ...args: A): void {
      for (let i = 0; i < veces; i++) original.call(this, ...args);
    };
  };
}

class GajoViejo {
  constructor(public numero: number) {}

  @repetir(3)
  empujar(): void {
    console.log(`empujo el gajo ${this.numero}`);
  }
}

new GajoViejo(4).empujar();
```

#### Al superarla
Al tercer empujón, el gajo viejo cierra con un *clonc* perfecto. Don Péndulo le da a Rigel una **estrella de latón**: —Al Vidriero le encantaban estas chapitas.

#### Imagen
- Un gajo viejo de la cúpula, con remaches oxidados, cerrándose al tercer empujón de un brazo mecánico.
- Don Péndulo (relojero viejo de barba blanca) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sonríe; Gheco cuenta tres con los dedos.

## R04-N08 · tsconfig.json y archivos .d.ts

```meta
tipo: tema
padre: R04-N07
precio: 10
criatura: skeleton
temas: cal.tipos, cal.build, js.modulos
```

### Crónica

En el sótano de la Cúpula está **la sala de calibración**: un panel enorme con decenas de perillas que ajustan cómo mide el Mirador. Y en un estante, cajas viejas de la Ciudadela, sin ninguna medida grabada, con una **etiqueta aparte** pegada en la tapa que describe qué hay adentro.

—Las perillas son el `tsconfig.json` —dice {mentor}—: cómo trabaja el compilador en tu proyecto. Y las cajas con etiqueta aparte son las bibliotecas escritas en JavaScript: el código no tiene tipos, pero alguien escribió en un archivo `.d.ts` qué tiene cada una.

> Los archivos `.d.ts` y `declare` no están en el material de base (FullCursos): se agregaron porque son la forma de usar desde TypeScript cualquier biblioteca de JavaScript.

### Objetivos

- Leer un `tsconfig.json`: las opciones principales (`strict`, `target`, `module`, `outDir`, `sourceMap`, `noEmitOnError`).
- Usar las opciones de calidad: `noImplicitReturns` y `noUnusedLocals`.
- Entender qué es un archivo `.d.ts`: los tipos de un código que está en JavaScript.
- Usar una biblioteca de JavaScript a través de su `.d.ts`, y leer el error de una biblioteca sin tipos (`TS2307`).

### Antes de empezar

- R03-N07 (módulos) y R04-N06 (las perillas finas).

### Explicación

#### El tsconfig.json
En un proyecto, `npx tsc --init` crea el `tsconfig.json`. Las opciones más usadas:

```json
{
  "compilerOptions": {
    "target": "ES2022",          // a qué JavaScript se pasa
    "module": "nodenext",        // cómo se escriben los módulos
    "strict": true,              // todas las revisiones estrictas (siempre prendido)
    "outDir": "dist",            // dónde van los .js
    "sourceMap": true,           // para que los errores digan la línea del .ts
    "noEmitOnError": true,       // si hay errores, no se genera ningún .js
    "noImplicitReturns": true,   // toda rama tiene que devolver algo
    "noUnusedLocals": true       // avisa si sobra una variable
  },
  "include": ["src"]
}
```

El `tsconfig.json` admite comentarios (`//`), a diferencia del JSON común.

> En la plataforma el compilador ya trabaja como con `"strict": true` y `"noEmitOnError": true`: si hay errores, el programa no corre. Algunas micro-misiones prenden otras perillas en su **tsconfig**.

#### Los .d.ts: la etiqueta de la caja
Muchas bibliotecas están escritas en JavaScript, sin tipos. Para usarlas desde TypeScript, existe un archivo **`.d.ts`** que solo **declara** sus tipos, sin código:

```typescript
// brujula.d.ts
export function rumbo(grados: number): string;
export const VERSION: string;
```

El JavaScript de verdad está en `brujula.js`. TypeScript lee el `.d.ts` y revisa cómo usás la biblioteca; al ejecutar, corre el `.js`.

- Si una biblioteca no tiene `.d.ts`, el compilador avisa: `TS2307` (*no se encuentra … ni sus declaraciones de tipos*).
- Para casi todas las bibliotecas populares, los `.d.ts` ya existen: vienen en el paquete o se instalan aparte (`npm install -D @types/nombre`).
- `declare` es la palabra para «esto existe, aunque no lo veas»: `declare const VERSION: string;`. En un `.d.ts` se sobreentiende.

### Código de ejemplo

```typescript
// En una micro-misión, rumbo vendría de brujula.js, descrito por brujula.d.ts.
function rumbo(grados: number): string {
  const nombres = ['norte', 'este', 'sur', 'oeste'];
  return nombres[Math.round(grados / 90) % 4] ?? 'norte';
}

console.log(rumbo(0), rumbo(95), rumbo(260));
```

### Salida esperada

```
norte este oeste
```

### ¿Para qué sirve?

Todo proyecto de TypeScript tiene su `tsconfig.json`, y conviene entender qué dice. Y casi todo proyecto usa bibliotecas de JavaScript: gracias a los `.d.ts`, también se usan con tipos, con sugerencias del editor y con el compilador revisando cada llamada.

### Errores habituales

**Ogro: una rama sin return (TS7030, con noImplicitReturns).** *No todas las rutas de acceso de código devuelven un valor*. Agregá el `return` que falta.

**Ogro: una variable que sobra (TS6133, con noUnusedLocals).** *Se declara "x", pero su valor no se lee nunca*. Borrala o usala.

**Esqueleto: una biblioteca sin tipos (TS2307).** *No se encuentra el módulo "./brujula.js" ni sus declaraciones de tipos correspondientes*. Hace falta su `.d.ts`.

### Micro-misión R04-N08-P1 · La perilla de los caminos

```meta
lugar: La sala de calibración
personajes: Rigel, Gheco
criatura: ogre
carta: noImplicitReturns | toda rama de una función tiene que devolver algo · si falta, TS7030 · agregá el return
recompensa: xp 10, oro 10
```

#### Escena
Rigel prende la perilla *todos los caminos devuelven*. Enseguida, la máquina que traduce los rumbos se queja: hay un caso en que no devuelve nada.

#### Gheco sugiere
Con `noImplicitReturns` (prendida en el **tsconfig** de esta micro-misión), si una función devuelve algo en un camino, tiene que devolver algo en **todos**. Si no, `TS7030`.

#### Desafío
Agregá el `return` del caso que falta.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el `___`, al final de la función, escribí `return 'sin rumbo';`.
3. Tocá **Ejecutar**. Tiene que salir `norte · sur · sin rumbo`.

#### tsconfig
```json
{ "noImplicitReturns": true }
```

#### Código inicial
```typescript
function rumbo(grados: number) {
  if (grados === 0) return 'norte';
  if (grados === 180) return 'sur';
  ___
}

console.log(`${rumbo(0)} · ${rumbo(180)} · ${rumbo(45)}`);
```

#### Salida esperada
```
norte · sur · sin rumbo
```

#### Solución
```typescript
function rumbo(grados: number) {
  if (grados === 0) return 'norte';
  if (grados === 180) return 'sur';
  return 'sin rumbo';
}

console.log(`${rumbo(0)} · ${rumbo(180)} · ${rumbo(45)}`);
```

#### Al superarla
La máquina de los rumbos ya no se queda callada con ningún ángulo.

#### Imagen
- Un panel enorme de calibración con decenas de perillas de latón, una de ellas recién prendida con una luz verde.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) gira la perilla.
- Gheco sobre el panel.

### Micro-misión R04-N08-P2 · La perilla de lo que sobra

```meta
lugar: La sala de calibración
personajes: Rigel, Gheco
criatura: ogre
carta: noUnusedLocals | una variable declarada y nunca usada es TS6133 · borrala
recompensa: xp 10, oro 10
```

#### Escena
Con la perilla *nada sobra* prendida, el compilador encuentra una variable que Rigel dejó de usar hace rato.

#### Gheco sugiere
Con `noUnusedLocals`, una variable que se declara y no se usa nunca da `TS6133`. Suele ser un resto de algo que se cambió: borrala.

#### Desafío
Borrá la variable que sobra.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Borrá la línea `const viejo = 'telescopio chico';`.
3. Tocá **Ejecutar**. Tiene que salir `Telescopio Mayor listo`.

#### tsconfig
```json
{ "noUnusedLocals": true }
```

#### Código inicial
```typescript
const viejo = 'telescopio chico';
const actual = 'Telescopio Mayor';
console.log(`${actual} listo`);
```

#### Salida esperada
```
Telescopio Mayor listo
```

#### Solución
```typescript
const actual = 'Telescopio Mayor';
console.log(`${actual} listo`);
```

#### Al superarla
Rigel tira a la basura la etiqueta vieja del telescopio chico. La mesa queda más ordenada.

#### Imagen
- Una etiqueta vieja cayendo en un canasto de papeles junto al panel de calibración.
- Rigel (chico flaco con pecas, antiparras de latón) se sacude las manos.
- Gheco dentro del canasto.

### Micro-misión R04-N08-P3 · La caja sin etiqueta

```meta
lugar: El estante de las cajas viejas
personajes: Rigel, Gheco
criatura: skeleton
carta: TS2307 | una biblioteca .js sin .d.ts · el compilador no sabe qué tiene · con un .d.ts que la describa, se usa con tipos
recompensa: xp 10, oro 10
```

#### Escena
Rigel abre una caja de la Ciudadela: la biblioteca `brujula.js`. El compilador no la quiere usar: no sabe qué hay adentro. Pero al lado hay otra caja, con la misma biblioteca **y** su etiqueta aparte.

#### Gheco sugiere
En el tablero hay dos archivos: `brujula.js` (el código, sin tipos) y `brujula.d.ts` (la etiqueta: solo dice qué tipos tiene). Si importás un módulo que no tiene tipos, el compilador avisa con `TS2307`.

Acá el problema es otro: la ruta está mal escrita. La biblioteca se llama `brujula`, no `brujulas`.

#### Desafío
Corregí la ruta del `import`.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `'./brujulas.js'` por `'./brujula.js'`.
3. Tocá **Ejecutar**. Tiene que salir `Rumbo: este`.

#### Archivos
brujula.js
```javascript
export function rumbo(grados) {
  const nombres = ['norte', 'este', 'sur', 'oeste'];
  return nombres[Math.round(grados / 90) % 4];
}
```

brujula.d.ts
```typescript
export function rumbo(grados: number): string;
```

#### Código inicial
```typescript
import { rumbo } from './brujulas.js';

console.log(`Rumbo: ${rumbo(95)}`);
```

#### Salida esperada
```
Rumbo: este
```

#### Solución
```typescript
import { rumbo } from './brujula.js';

console.log(`Rumbo: ${rumbo(95)}`);
```

#### Al superarla
La brújula de la Ciudadela gira y marca el este. Con su etiqueta, se usa como cualquier pieza del Mirador.

#### Imagen
- Una caja de madera abierta con una brújula de bronce adentro y una etiqueta de cartulina pegada en la tapa.
- Un esqueleto de alambre chiquito escondido en la caja vacía de al lado.
- Rigel (chico flaco con pecas, antiparras de latón) sostiene la brújula; Gheco lee la etiqueta.

### Micro-misión R04-N08-P4 · La etiqueta revisa

```meta
lugar: El estante de las cajas viejas
personajes: Rigel, Gheco
criatura: goblin
carta: El .d.ts revisa las llamadas | el código .js no tiene tipos · el .d.ts dice qué recibe y qué devuelve · el compilador revisa contra él
recompensa: xp 10, oro 10
```

#### Escena
Rigel le pasa a la brújula un texto en lugar de un número. El JavaScript de la brújula no se quejaría, pero la etiqueta sí.

#### Gheco sugiere
El `.d.ts` dice que `rumbo` recibe un `number`. Aunque el código de verdad esté en JavaScript, el compilador revisa cada llamada contra la etiqueta: `rumbo('noventa')` da `TS2345`.

#### Desafío
Pasale el número `270` en lugar del texto.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `rumbo('noventa')` por `rumbo(270)`.
3. Tocá **Ejecutar**. Tiene que salir `Rumbo: oeste`.

#### Archivos
brujula.js
```javascript
export function rumbo(grados) {
  const nombres = ['norte', 'este', 'sur', 'oeste'];
  return nombres[Math.round(grados / 90) % 4];
}
```

brujula.d.ts
```typescript
export function rumbo(grados: number): string;
```

#### Código inicial
```typescript
import { rumbo } from './brujula.js';

console.log(`Rumbo: ${rumbo('noventa')}`);
```

#### Salida esperada
```
Rumbo: oeste
```

#### Solución
```typescript
import { rumbo } from './brujula.js';

console.log(`Rumbo: ${rumbo(270)}`);
```

#### Al superarla
La brújula apunta al oeste. El goblin que quería darle un papelito se va con las manos vacías.

#### Imagen
- La brújula de bronce marcando el oeste, con la etiqueta de cartulina al lado.
- Un goblin chiquito con un engranaje en la espalda y un papelito arrugado.
- Rigel (chico flaco con pecas, antiparras de latón) gira la brújula; Gheco mira.

### Micro-misión R04-N08-P5 · Lo que existe aunque no lo veas

```meta
lugar: El estante de las cajas viejas
personajes: Rigel, Gheco, Astrea
carta: declare | declare const VERSION: string; · le dice al compilador que eso existe · lo pone otro archivo, en JavaScript
recompensa: xp 15, monedas 5
```

#### Escena
La caja de configuración de la Ciudadela (`config.js`) deja anotadas, al abrirse, la versión del Mirador y el nombre del observatorio. Rigel las quiere mostrar, pero el compilador dice que no existen.

#### Gheco sugiere
`config.js` (en el tablero) guarda `VERSION` y `OBSERVATORIO` en el objeto global (`globalThis`). Al ejecutar existen, pero el compilador no lo sabe: da `TS2304` (*no se encuentra el nombre*).

`declare` le dice al compilador «esto existe, confiá»:

```ts
declare const VERSION: string;
```

Es lo mismo que hace un `.d.ts`, pero adentro de tu archivo. Como el `!`, no revisa nada: usalo para cosas que de verdad existen.

`import './config.js';` (sin llaves) ejecuta el archivo sin traer nada: solo para que deje anotado lo suyo. Su `config.d.ts` solo le dice al compilador que el archivo existe.

#### Desafío
Declará las dos constantes.

#### Pasos
1. Tocá **Ejecutar** y leé los errores.
2. En el `___`, escribí `declare const VERSION: string;` y, en el renglón de abajo, `declare const OBSERVATORIO: string;`.
3. Tocá **Ejecutar**. Tiene que salir `Mirador de las Constelaciones, versión 6.0`.

#### Archivos
config.js
```javascript
globalThis.VERSION = '6.0';
globalThis.OBSERVATORIO = 'Mirador de las Constelaciones';
```

config.d.ts
```typescript
// Solo dice que config.js existe: no exporta nada.
export {};
```

#### Código inicial
```typescript
import './config.js';

___

console.log(`${OBSERVATORIO}, versión ${VERSION}`);
```

#### Salida esperada
```
Mirador de las Constelaciones, versión 6.0
```

#### Solución
```typescript
import './config.js';

declare const VERSION: string;
declare const OBSERVATORIO: string;

console.log(`${OBSERVATORIO}, versión ${VERSION}`);
```

#### Al superarla
El cartel de la entrada muestra la versión. Astrea asiente: —Lo que existe aunque no lo veas también se declara.

#### Imagen
- Una caja de configuración de la Ciudadela, abierta, con dos tarjetas de latón flotando hacia el cartel de la entrada del observatorio.
- Astrea (lechuza con anteojos de latón y chaleco azul) lee el cartel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sostiene la caja; Gheco sobre el cartel.

### Micro-misión R04-N08-P6 · La calibración completa

```meta
lugar: La sala de calibración
personajes: Rigel, Gheco, Astrea
carta: Todo junto | perillas estrictas en el tsconfig · una biblioteca .js con su .d.ts · cada camino devuelve · nada sobra
recompensa: xp 15, monedas 5
```

#### Escena
Astrea prende todas las perillas de la sala de calibración y le pide a Rigel que arme el informe de rumbos con la brújula de la Ciudadela.

#### Gheco sugiere
En este **tsconfig** están prendidas `noImplicitReturns`, `noUnusedLocals` y `noUncheckedIndexedAccess`. Hay una variable que sobra y un camino sin `return`.

#### Desafío
Arreglá los dos errores.

#### Pasos
1. Tocá **Ejecutar** y leé los dos errores.
2. Borrá la línea `const sobrante = 0;`.
3. En el `___` de `describir`, escribí ``return `${grados}°: ${rumbo(grados)}`;``.
4. Tocá **Ejecutar** y compará con la salida esperada.

#### tsconfig
```json
{ "noImplicitReturns": true, "noUnusedLocals": true, "noUncheckedIndexedAccess": true }
```

#### Archivos
brujula.js
```javascript
export function rumbo(grados) {
  const nombres = ['norte', 'este', 'sur', 'oeste'];
  return nombres[Math.round(grados / 90) % 4];
}
```

brujula.d.ts
```typescript
export function rumbo(grados: number): string;
```

#### Código inicial
```typescript
import { rumbo } from './brujula.js';

const sobrante = 0;
const angulos: number[] = [0, 90, -1, 180];

function describir(grados: number) {
  if (grados < 0) return `${grados}°: inválido`;
  ___
}

for (const a of angulos) console.log(describir(a));
```

#### Salida esperada
```
0°: norte
90°: este
-1°: inválido
180°: sur
```

#### Solución
```typescript
import { rumbo } from './brujula.js';

const angulos: number[] = [0, 90, -1, 180];

function describir(grados: number) {
  if (grados < 0) return `${grados}°: inválido`;
  return `${grados}°: ${rumbo(grados)}`;
}

for (const a of angulos) console.log(describir(a));
```

#### Al superarla
Todas las perillas en verde, y el informe sale limpio. Astrea le da a Rigel una **estrella de latón**: —Ya sabés calibrar el Mirador.

#### Imagen
- El panel de calibración con todas las perillas en verde y un informe de rumbos impreso saliendo por una ranura.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) toma el informe; Gheco sobre el panel.

## R04-N09 · Jefe: el Espejismo Null

```meta
tipo: jefe
padre: R04-N08
precio: 10
criatura: dragon
insignia: Lente del Espejismo
insignia_descripcion: Venciste al Espejismo Null: ya no te engaña nada que no esté.
usa: cal.tipos, err.excepciones, conc.async, js.dom, err.validacion
```

### Crónica

Una noche sin luna, la Cúpula se llena de **reflejos**: en el tablero aparecen botones que no existen, el tubo trae respuestas que nunca se mandaron y el registro muestra estrellas que no están. En el centro de la sala flota un autómata de vidrio y latón, transparente, que cambia de forma: **el Espejismo Null**. Todo lo que toca parece estar… y no está.

—El Espejismo vive de lo que se usa sin preguntar —dice {mentor}—. Para vencerlo, preguntá por todo lo que puede faltar, y revisá todo lo que llega.

### Objetivos

- Integrar todo lo de la rama: errores tipados, `Result`, promesas, `fetch` con guardias, la página tipada, el lienzo y las opciones estrictas.
- No dejar ningún `null`, `undefined` ni respuesta sin revisar.

### Antes de empezar

- Todos los nodos de la Cúpula (R04-N01 a R04-N08).

### Explicación

#### Cómo encarar un jefe
1. **Leé la consigna entera** y marcá todo lo que puede faltar: elementos, respuestas, índices.
2. **Preguntá una vez y cortá**: `if (!x) throw …` al principio.
3. **Lo que llega de afuera, por un guardia.**
4. **Ejecutá después de cada paso.**

#### Las trampas del Espejismo (y la verdad)
| El Espejismo dice… | La verdad |
|---|---|
| "el botón está, siempre está" | `querySelector` puede dar `null`: preguntá |
| "lo que llega del Puerto es lo que pediste" | lo que llega es `unknown` hasta que pasa el guardia |
| "el tercer elemento existe" | con `noUncheckedIndexedAccess`, puede no existir |
| "poné un `!` y listo" | el `!` no revisa nada: el Espejismo entra por ahí |

### Micro-misión R04-N09-P1 · El botón que no estaba

```meta
lugar: El tablero de la Cúpula
personajes: Rigel, Gheco, el Espejismo Null
criatura: orc
carta: Trampa 1 | el ! no revisa · el botón con otro id da null al ejecutar · preguntá y usá el id correcto
recompensa: xp 15, monedas 3
```

#### Escena
El Espejismo puso un `!` en el programa del tablero: el compilador no se queja, pero al ejecutar explota. El botón que busca no existe: se llama distinto.

#### Gheco sugiere
`document.querySelector('#abrir-cupula')!` le dice al compilador que el botón está, pero no lo revisa. En la página el botón se llama `#abrir`. Sacá el `!`, preguntá, y usá el id correcto.

#### Desafío
Cambiá el `!` por una pregunta y corregí el id.

#### Pasos
1. Tocá **Ejecutar**: explota al ejecutar.
2. Cambiá `document.querySelector<HTMLButtonElement>('#abrir-cupula')!` por `document.querySelector<HTMLButtonElement>('#abrir')`.
3. En el `___`, escribí `if (!boton || !cartel) throw new Error('Falta un control');`.
4. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1326; color: #e8d9b0; padding: 24px; }
  #cartel { font-size: 22px; color: #f2c14e; }
</style>
<button id="abrir">Abrir la Cúpula</button>
<p id="cartel">Cúpula cerrada</p>
```

#### Eventos
```
click #abrir
```

#### Estado
```
#cartel
```

#### Código inicial
```typescript
const boton = document.querySelector<HTMLButtonElement>('#abrir-cupula')!;
const cartel = document.querySelector('#cartel');
___

boton.addEventListener('click', () => {
  cartel.textContent = 'Cúpula abierta';
});
```

#### Salida esperada
```
── Estado ──
#cartel: Cúpula abierta
```

#### Solución
```typescript
const boton = document.querySelector<HTMLButtonElement>('#abrir');
const cartel = document.querySelector('#cartel');
if (!boton || !cartel) throw new Error('Falta un control');

boton.addEventListener('click', () => {
  cartel.textContent = 'Cúpula abierta';
});
```

#### Al superarla
El reflejo del botón falso se deshace, y el de verdad abre la Cúpula.

#### Imagen
- Un tablero de control de latón con un botón de verdad y, al lado, el reflejo transparente de un botón que se deshace.
- El Espejismo Null (un autómata transparente de vidrio y latón que cambia de forma) se aleja.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) aprieta el botón; Gheco mira.

### Micro-misión R04-N09-P2 · La respuesta que nadie mandó

```meta
lugar: El tubo neumático
personajes: Rigel, Gheco, el Espejismo Null
criatura: troll
carta: Trampa 2 | lo que llega es unknown · el guardia revisa · Result con el error si no pasa
recompensa: xp 15, monedas 3
```

#### Escena
Por el tubo llegan dos cápsulas: una del Puerto, con la lista de héroes, y otra que el Espejismo hizo aparecer, con el saludo del Puerto disfrazado. Rigel tiene que reconocer cuál es de verdad.

#### Gheco sugiere
`pedirHeroes` usa un guardia: si lo que llega no es una lista de héroes, devuelve un `Result` con el error. Probá las dos rutas.

#### Desafío
Completá la validación de la lista.

#### Pasos
1. Buscá el `___` en el `if`.
2. Cambialo por `!Array.isArray(datos) || !datos.every(esHeroe)`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Heroe = { nombre: string; nivel: number };
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function esHeroe(x: unknown): x is Heroe {
  return typeof x === 'object' && x !== null
    && 'nombre' in x && typeof x.nombre === 'string'
    && 'nivel' in x && typeof x.nivel === 'number';
}

async function pedirHeroes(ruta: string): Promise<Result<Heroe[]>> {
  const respuesta = await fetch(ruta);
  const datos: unknown = await respuesta.json();
  if (___) return { ok: false, error: 'es un espejismo' };
  return { ok: true, valor: datos };
}

for (const ruta of ['/puerto/heroes', '/puerto/hola']) {
  const r = await pedirHeroes(ruta);
  console.log(r.ok ? `${r.valor.length} héroes, el primero ${r.valor[0]?.nombre}` : r.error);
}
```

#### Salida esperada
```
4 héroes, el primero Mia
es un espejismo
```

#### Solución
```typescript
type Heroe = { nombre: string; nivel: number };
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function esHeroe(x: unknown): x is Heroe {
  return typeof x === 'object' && x !== null
    && 'nombre' in x && typeof x.nombre === 'string'
    && 'nivel' in x && typeof x.nivel === 'number';
}

async function pedirHeroes(ruta: string): Promise<Result<Heroe[]>> {
  const respuesta = await fetch(ruta);
  const datos: unknown = await respuesta.json();
  if (!Array.isArray(datos) || !datos.every(esHeroe)) return { ok: false, error: 'es un espejismo' };
  return { ok: true, valor: datos };
}

for (const ruta of ['/puerto/heroes', '/puerto/hola']) {
  const r = await pedirHeroes(ruta);
  console.log(r.ok ? `${r.valor.length} héroes, el primero ${r.valor[0]?.nombre}` : r.error);
}
```

#### Al superarla
La cápsula falsa se evapora al abrirla. La de verdad trae los cuatro héroes del Puerto.

#### Imagen
- Dos cápsulas en la boca del tubo neumático: una real y otra transparente que se evapora en humo.
- El Espejismo Null (autómata transparente de vidrio y latón) retrocede.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) abre la cápsula real; Gheco sopla el humo.

### Micro-misión R04-N09-P3 · Las estrellas que no están

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco, el Espejismo Null
criatura: orc
carta: Trampa 3 | con noUncheckedIndexedAccess, cada índice puede faltar · ?? para el valor por defecto · ?. para seguir
recompensa: xp 15, monedas 3
```

#### Escena
El Espejismo agregó al pedido del catálogo estrellas que no existen. Con las perillas finas prendidas, el compilador ya las ve venir.

#### Gheco sugiere
Con `noUncheckedIndexedAccess` (en el **tsconfig**), `brillos[nombre]` es `number | undefined`, y `orden[i]` es `string | undefined`. Hay que dar un valor si falta.

#### Desafío
Completá las dos lecturas.

#### Pasos
1. El primer `___`: `orden[i] ?? 'nadie'`.
2. El segundo `___`: `brillos[nombre] ?? 0`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### tsconfig
```json
{ "noUncheckedIndexedAccess": true }
```

#### Código inicial
```typescript
const brillos: Record<string, number> = { Vega: 9, Sirio: 10 };
const orden: string[] = ['Sirio', 'Fantasma', 'Vega'];

for (let i = 0; i < 4; i++) {
  const nombre: string = ___;
  const brillo: number = ___;
  console.log(`${i + 1}. ${nombre}: ${brillo}`);
}
```

#### Salida esperada
```
1. Sirio: 10
2. Fantasma: 0
3. Vega: 9
4. nadie: 0
```

#### Solución
```typescript
const brillos: Record<string, number> = { Vega: 9, Sirio: 10 };
const orden: string[] = ['Sirio', 'Fantasma', 'Vega'];

for (let i = 0; i < 4; i++) {
  const nombre: string = orden[i] ?? 'nadie';
  const brillo: number = brillos[nombre] ?? 0;
  console.log(`${i + 1}. ${nombre}: ${brillo}`);
}
```

#### Al superarla
Las estrellas falsas del catálogo brillan con cero: se ve enseguida que no están.

#### Imagen
- Un catálogo de estrellas con algunas fichas transparentes y vacías entre las de verdad.
- El Espejismo Null (autómata transparente) desdibujándose.
- Rigel (chico flaco con pecas, antiparras de latón con la lupa bajada) revisa las fichas; Gheco señala una vacía.

### Micro-misión R04-N09-P4 · La falla que se esconde

```meta
lugar: La Cúpula
personajes: Rigel, Gheco, el Espejismo Null
criatura: troll
carta: Trampa 4 | async con try/catch · el error es unknown: instanceof · finally deja todo en orden
recompensa: xp 15, monedas 3
```

#### Escena
El Espejismo hace fallar el motor de un gajo cuando nadie mira. Rigel arma la maniobra de cierre para que, falle lo que falle, la Cúpula quede asegurada.

#### Gheco sugiere
En una función `async`, un error se ataja igual, con `try`/`catch`. El error es `unknown`: se pregunta con `instanceof`. Y `finally` se ejecuta siempre.

#### Desafío
Completá la pregunta del `catch`.

#### Pasos
1. Buscá el `___` en el `if` del `catch`.
2. Cambialo por `error instanceof GajoTrabado`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
class GajoTrabado extends Error {
  constructor(public readonly gajo: number) {
    super(`el gajo ${gajo} no responde`);
  }
}

const esperar = (ms: number): Promise<void> => new Promise((listo) => setTimeout(listo, ms));

async function cerrarGajo(n: number): Promise<void> {
  await esperar(200);
  if (n === 3) throw new GajoTrabado(n);
  console.log(`gajo ${n} cerrado`);
}

try {
  for (const g of [1, 2, 3, 4]) await cerrarGajo(g);
} catch (error) {
  if (___) console.log(`Espejismo en el gajo ${error.gajo}`);
} finally {
  console.log('Cúpula asegurada');
}
```

#### Salida esperada
```
gajo 1 cerrado
gajo 2 cerrado
Espejismo en el gajo 3
Cúpula asegurada
```

#### Solución
```typescript
class GajoTrabado extends Error {
  constructor(public readonly gajo: number) {
    super(`el gajo ${gajo} no responde`);
  }
}

const esperar = (ms: number): Promise<void> => new Promise((listo) => setTimeout(listo, ms));

async function cerrarGajo(n: number): Promise<void> {
  await esperar(200);
  if (n === 3) throw new GajoTrabado(n);
  console.log(`gajo ${n} cerrado`);
}

try {
  for (const g of [1, 2, 3, 4]) await cerrarGajo(g);
} catch (error) {
  if (error instanceof GajoTrabado) console.log(`Espejismo en el gajo ${error.gajo}`);
} finally {
  console.log('Cúpula asegurada');
}
```

#### Al superarla
El gajo 3 queda marcado, y la Cúpula, asegurada igual. El Espejismo pierde su último escondite.

#### Imagen
- La cúpula cerrándose gajo por gajo, con uno marcado con una cinta de aviso.
- El Espejismo Null (autómata transparente) casi invisible.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) baja una palanca; Gheco en su hombro.

### Micro-misión R04-N09-P5 · El Espejismo se disipa

```meta
lugar: El tablero de la Cúpula
personajes: Rigel, Gheco, Astrea, el Espejismo Null
criatura: dragon
carta: El jefe | elementos con su tipo y una pregunta · fetch con guardia y Result · async en un evento · el cartel muestra la verdad
recompensa: xp 20, monedas 5
item: Lente del Espejismo
```

#### Escena
Acorralado, el Espejismo se mete en el último lugar: el botón del tablero que pide el clima al Puerto. Si Rigel lo arma sin dejar nada sin revisar, el Espejismo no tiene dónde quedarse.

#### Gheco sugiere
Todo lo de la rama:
- los elementos con su tipo, preguntando una vez (y la función del evento como flecha, para que la pregunta llegue adentro);
- `pedirClima` revisa la respuesta con un guardia y devuelve un `Result`;
- el evento es `async`: espera la respuesta y muestra lo que corresponde.

#### Desafío
Completá la línea que muestra el resultado en el cartel.

#### Pasos
1. Buscá el `___` adentro del evento.
2. Cambialo por ``cartel.textContent = r.ok ? `Viento ${r.valor.viento}, ${r.valor.temperatura}°` : r.error;``.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1326; color: #e8d9b0; padding: 24px; }
  #cartel { font-size: 22px; color: #f2c14e; }
</style>
<button id="pedir">Pedir el clima</button>
<p id="cartel">—</p>
```

#### Eventos
```
click #pedir
esperar 1000
```

#### Estado
```
#cartel
```

#### Código inicial
```typescript
type Clima = { viento: string; temperatura: number };
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function esClima(x: unknown): x is Clima {
  return typeof x === 'object' && x !== null
    && 'viento' in x && typeof x.viento === 'string'
    && 'temperatura' in x && typeof x.temperatura === 'number';
}

async function pedirClima(): Promise<Result<Clima>> {
  const respuesta = await fetch('/puerto/clima');
  if (!respuesta.ok) return { ok: false, error: `el Puerto contestó ${respuesta.status}` };
  const datos: unknown = await respuesta.json();
  return esClima(datos) ? { ok: true, valor: datos } : { ok: false, error: 'es un espejismo' };
}

const boton = document.querySelector<HTMLButtonElement>('#pedir');
const cartel = document.querySelector<HTMLParagraphElement>('#cartel');
if (!boton || !cartel) throw new Error('Falta un control del tablero');

boton.addEventListener('click', async () => {
  cartel.textContent = 'Pidiendo…';
  const r = await pedirClima();
  ___
});
```

#### Salida esperada
```
── Estado ──
#cartel: Viento suave, 18°
```

#### Solución
```typescript
type Clima = { viento: string; temperatura: number };
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function esClima(x: unknown): x is Clima {
  return typeof x === 'object' && x !== null
    && 'viento' in x && typeof x.viento === 'string'
    && 'temperatura' in x && typeof x.temperatura === 'number';
}

async function pedirClima(): Promise<Result<Clima>> {
  const respuesta = await fetch('/puerto/clima');
  if (!respuesta.ok) return { ok: false, error: `el Puerto contestó ${respuesta.status}` };
  const datos: unknown = await respuesta.json();
  return esClima(datos) ? { ok: true, valor: datos } : { ok: false, error: 'es un espejismo' };
}

const boton = document.querySelector<HTMLButtonElement>('#pedir');
const cartel = document.querySelector<HTMLParagraphElement>('#cartel');
if (!boton || !cartel) throw new Error('Falta un control del tablero');

boton.addEventListener('click', async () => {
  cartel.textContent = 'Pidiendo…';
  const r = await pedirClima();
  cartel.textContent = r.ok ? `Viento ${r.valor.viento}, ${r.valor.temperatura}°` : r.error;
});
```

#### Al superarla
El cartel muestra el clima de verdad. Sin un solo lugar sin revisar, el Espejismo se vuelve transparente del todo y se disipa como vapor. En el piso queda un lente de vidrio claro. Astrea lo levanta y se lo da a Rigel: la **Lente del Espejismo**. —Con esto vas a ver siempre lo que de verdad está.

#### Imagen
- El tablero de control de la cúpula con el cartel de luz encendido, y un autómata transparente disipándose en vapor.
- Astrea (lechuza grande con anteojos de latón y chaleco azul) le da a Rigel un lente de vidrio claro.
- Rigel (chico flaco con pecas, pelo castaño revuelto, antiparras de latón, chaleco marrón) lo recibe; Gheco festeja.
