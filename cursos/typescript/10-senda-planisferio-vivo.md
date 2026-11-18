# RAMA S05 · Senda del Planisferio Vivo: el juego crece

```meta
tipo: senda
posicion: 10
```

## S05-N01 · Niveles

```meta
tipo: tema
padre: R05-N05
precio: 3
moneda: comodin
criatura: orc
temas: juegos.estados
usa: juegos.bucle, juegos.colisiones, cal.tipos, js.canvas
```

### Crónica

Desde que el Planisferio anda, los chicos de la Feria suben al Mirador los domingos para ver las constelaciones girar. Nima tiene una idea: —¿Y si proyectamos el juego del Vidriero en la cúpula? Pero más grande: con **niveles**, más enemigos y Fuelle ayudando al héroe.

Fuelle, el zorro mecánico, sopla una nubecita de vapor y mueve la cola de engranajes. Le encanta la idea.

—Un juego que crece —dice Gheco— tiene que tener su configuración en un solo lugar, y bien medida. Si no, cada nivel nuevo rompe algo.

### Objetivos

- Describir los niveles en una lista de configuración con `satisfies`.
- Generar las gemas de cada nivel a partir de su configuración.
- Pasar de nivel cuidando el índice con `noUncheckedIndexedAccess`.
- Ver el cambio de nivel en el lienzo.
- Calcular la dificultad con un `Record`.

### Antes de empezar

- El Atlas del Vidriero (R05), sobre todo el juego tipado (R05-N03 y N04).
- `satisfies` (R03-N05) y las opciones estrictas (R04-N06).

### Explicación

#### La configuración, en un solo lugar
```typescript
interface Nivel { nombre: string; gemas: number; velocidad: number }

const NIVELES = [
  { nombre: 'La Lira', gemas: 3, velocidad: 20 },
  { nombre: 'Orión', gemas: 5, velocidad: 35 },
] satisfies readonly Nivel[];
```
`satisfies` revisa que cada nivel tenga la forma de `Nivel` (sin campos de más, sin campos que falten), pero deja que TypeScript recuerde los valores exactos.

#### Pasar de nivel sin salirse
Con `noUncheckedIndexedAccess`, `NIVELES[i]` es `Nivel | undefined`: si `i` se pasó del último, no hay nivel. El compilador obliga a preguntar.

### Código de ejemplo

```typescript
interface Nivel { nombre: string; gemas: number }
const NIVELES = [{ nombre: 'La Lira', gemas: 3 }, { nombre: 'Orión', gemas: 5 }] satisfies readonly Nivel[];
console.log(NIVELES.map((n) => `${n.nombre}: ${n.gemas}`).join(' · '));
console.log(NIVELES.reduce((total, n) => total + n.gemas, 0));
```

### Salida esperada

```
La Lira: 3 · Orión: 5
8
```

### ¿Para qué sirve?

Los juegos de verdad separan **los datos** (niveles, enemigos, premios) **del motor** (el bucle, las colisiones). Así, los diseñadores agregan niveles sin tocar el código, y el compilador revisa que cada nivel esté bien escrito.

### Errores habituales

**Orco: el nivel que no existe.** Después del último nivel, `NIVELES[i]` es `undefined`. Hay que decidir qué pasa: ¿ganó?, ¿vuelve al primero?

**Goblin: un campo mal escrito en la configuración.** `gemass: 3` no compila con `satisfies`: te sugiere `gemas`.

**Ogro: números sueltos por el código.** Si la velocidad de cada nivel está escrita en el bucle, cambiarla obliga a buscarla. En la configuración, se cambia en un solo lugar.

### Micro-misión S05-N01-P1 · El nivel mal escrito

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Nima
criatura: goblin
carta: satisfies en la configuración | cada nivel con la forma de Nivel · gemass no existe: el compilador sugiere gemas (TS2561)
recompensa: xp 10, oro 10
```

#### Escena
Nima escribe los niveles del juego, uno por constelación. En el tercero se le escapó una letra.

#### Gheco sugiere
`satisfies readonly Nivel[]` revisa cada nivel. Leé el error: te dice qué campo no existe y cuál quisiste escribir.

#### Desafío
Corregí el campo mal escrito.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `gemass` por `gemas`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Nivel {
  nombre: string;
  gemas: number;
  velocidad: number;
}

const NIVELES = [
  { nombre: 'La Lira', gemas: 3, velocidad: 20 },
  { nombre: 'Orión', gemas: 5, velocidad: 35 },
  { nombre: 'El Dragón', gemass: 8, velocidad: 50 },
] satisfies readonly Nivel[];

NIVELES.forEach((n, i) => console.log(`Nivel ${i + 1} · ${n.nombre}: ${n.gemas} gemas, goblins a ${n.velocidad}`));
```

#### Salida esperada
```
Nivel 1 · La Lira: 3 gemas, goblins a 20
Nivel 2 · Orión: 5 gemas, goblins a 35
Nivel 3 · El Dragón: 8 gemas, goblins a 50
```

#### Solución
```typescript
interface Nivel {
  nombre: string;
  gemas: number;
  velocidad: number;
}

const NIVELES = [
  { nombre: 'La Lira', gemas: 3, velocidad: 20 },
  { nombre: 'Orión', gemas: 5, velocidad: 35 },
  { nombre: 'El Dragón', gemas: 8, velocidad: 50 },
] satisfies readonly Nivel[];

NIVELES.forEach((n, i) => console.log(`Nivel ${i + 1} · ${n.nombre}: ${n.gemas} gemas, goblins a ${n.velocidad}`));
```

#### Al superarla
Los tres niveles aparecen en la cúpula, cada uno con su constelación. Fuelle mueve la cola.

#### Imagen
- La cúpula del Planisferio por dentro, con tres constelaciones proyectadas en el techo como niveles de un juego.
- Un goblin chiquito con un engranaje en la espalda agregando una letra de más en un cartel.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas, arco verde) señala el techo; Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) corrige el cartel; Fuelle (zorro mecánico de latón con cola de engranajes) mueve la cola; Gheco sobre Fuelle.

### Micro-misión S05-N01-P2 · Las gemas de cada nivel

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco
carta: Generar desde la configuración | Array.from({ length: n.gemas }, (_, i) => …) · una gema por cada una · repartidas a lo ancho
recompensa: xp 10, oro 10
```

#### Escena
Cada nivel dice cuántas gemas tiene. Rigel escribe la función que las **fabrica**, repartidas a lo ancho del lienzo.

#### Gheco sugiere
`Array.from({ length: n }, (_, i) => …)` arma una lista de `n` elementos, llamando a la función con cada posición `i`. Para repartirlas: `x = 20 + i * 40`.

#### Desafío
Completá `gemasDe`.

#### Pasos
1. Buscá el `___` en `gemasDe`.
2. Cambialo por `return Array.from({ length: n.gemas }, (_, i) => ({ x: 20 + i * 40, y: 76, lado: 8 }));`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Caja { x: number; y: number; lado: number }
interface Nivel { nombre: string; gemas: number }

function gemasDe(n: Nivel): Caja[] {
  ___
}

for (const n of [{ nombre: 'La Lira', gemas: 3 }, { nombre: 'Orión', gemas: 5 }]) {
  console.log(`${n.nombre}: ${gemasDe(n).map((g) => g.x).join(', ')}`);
}
```

#### Salida esperada
```
La Lira: 20, 60, 100
Orión: 20, 60, 100, 140, 180
```

#### Solución
```typescript
interface Caja { x: number; y: number; lado: number }
interface Nivel { nombre: string; gemas: number }

function gemasDe(n: Nivel): Caja[] {
  return Array.from({ length: n.gemas }, (_, i) => ({ x: 20 + i * 40, y: 76, lado: 8 }));
}

for (const n of [{ nombre: 'La Lira', gemas: 3 }, { nombre: 'Orión', gemas: 5 }]) {
  console.log(`${n.nombre}: ${gemasDe(n).map((g) => g.x).join(', ')}`);
}
```

#### Al superarla
Las gemas aparecen en fila, a la misma distancia una de la otra, como cuentas de un collar.

#### Imagen
- Una fila de gemas celestes flotando a la misma distancia sobre el lienzo de vidrio de la cúpula.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mide la distancia con el calibre.
- Gheco salta de gema en gema.

### Micro-misión S05-N01-P3 · Después del último nivel

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Nima
criatura: orc
carta: noUncheckedIndexedAccess | NIVELES[i] puede ser undefined · si no hay nivel, ganaste el juego · el compilador obliga a preguntar
recompensa: xp 10, oro 10
```

#### Escena
Nima juega los tres niveles seguidos y, al terminar el último, el juego se cuelga: busca un **cuarto nivel** que no existe.

#### Gheco sugiere
Mirá el `tsconfig`: `noUncheckedIndexedAccess`. Con esa opción, `NIVELES[i]` puede ser `undefined`, y el compilador no te deja usarlo sin preguntar. Si no hay nivel, el juego terminó.

#### Desafío
Agregá la pregunta.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el `___`, escribí `if (!n) return '¡Ganaste todo el Planisferio!';`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### tsconfig
```json
{ "noUncheckedIndexedAccess": true }
```

#### Código inicial
```typescript
interface Nivel { nombre: string; gemas: number }
const NIVELES: readonly Nivel[] = [
  { nombre: 'La Lira', gemas: 3 },
  { nombre: 'Orión', gemas: 5 },
  { nombre: 'El Dragón', gemas: 8 },
];

function anunciar(indice: number): string {
  const n = NIVELES[indice];
  ___
  return `Nivel ${indice + 1}: ${n.nombre} (${n.gemas} gemas)`;
}

for (let i = 0; i <= 3; i++) console.log(anunciar(i));
```

#### Salida esperada
```
Nivel 1: La Lira (3 gemas)
Nivel 2: Orión (5 gemas)
Nivel 3: El Dragón (8 gemas)
¡Ganaste todo el Planisferio!
```

#### Solución
```typescript
interface Nivel { nombre: string; gemas: number }
const NIVELES: readonly Nivel[] = [
  { nombre: 'La Lira', gemas: 3 },
  { nombre: 'Orión', gemas: 5 },
  { nombre: 'El Dragón', gemas: 8 },
];

function anunciar(indice: number): string {
  const n = NIVELES[indice];
  if (!n) return '¡Ganaste todo el Planisferio!';
  return `Nivel ${indice + 1}: ${n.nombre} (${n.gemas} gemas)`;
}

for (let i = 0; i <= 3; i++) console.log(anunciar(i));
```

#### Al superarla
Después del último nivel, en la cúpula aparecen fuegos artificiales de luz. Nima grita de alegría y Fuelle da vueltas persiguiéndose la cola.

#### Imagen
- La cúpula del Planisferio con fuegos artificiales de luz dorada y estrellas girando.
- Un orco de cuerda chiquito buscando una puerta que no existe al final de un pasillo.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) festeja con los brazos arriba; Fuelle (zorro mecánico de latón) da vueltas; Rigel (chico flaco con pecas, antiparras de latón) sonríe; Gheco tira papelitos.

### Micro-misión S05-N01-P4 · El nivel siguiente

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Fuelle
carta: Cambiar de nivel en el bucle | al juntar todas, indice++ y gemas del nivel nuevo · el cartel muestra el nivel · si no hay más, ganaste
recompensa: xp 15, monedas 5
```

#### Escena
Rigel prueba el cambio de nivel en el lienzo: el héroe junta las tres gemas de la Lira y aparecen las del nivel siguiente.

#### Gheco sugiere
En cada cuadro, después de juntar, se pregunta si quedan gemas. Si no quedan, se pasa al nivel siguiente: `cargar(indice + 1)`. Falta esa línea.

#### Desafío
Completá el cambio de nivel.

#### Pasos
1. Buscá el `___` en `cuadro`.
2. Cambialo por `if (gemas.length === 0) cargar(indice + 1);`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f2c14e; font-family: monospace; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1326; border: 6px solid #8d6e3f; }
</style>
<p id="nivel"></p>
<canvas id="lienzo" width="240" height="160"></canvas>
```

#### Eventos
```
apretar ArrowRight
cuadros 90
soltar ArrowRight
```

#### Estado
```
#nivel
lienzo
```

#### Código inicial
```typescript
interface Caja { x: number; y: number; lado: number }
interface Nivel { nombre: string; gemas: number }

const NIVELES = [
  { nombre: 'La Lira', gemas: 3 },
  { nombre: 'Orión', gemas: 5 },
] satisfies readonly Nivel[];

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}
const chocan = (a: Caja, b: Caja) => a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;

const ctx = obtenerElemento<HTMLCanvasElement>('#lienzo').getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;
const cartel = obtenerElemento<HTMLParagraphElement>('#nivel');

const heroe = { x: 0, y: 74, lado: 12, velocidad: 120 };
let indice = 0;
let gemas: Caja[] = [];

function cargar(i: number): void {
  indice = i;
  const n: Nivel | undefined = NIVELES[i];
  if (!n) {
    cartel.textContent = '¡Ganaste!';
    gemas = [];
    return;
  }
  heroe.x = 0;
  gemas = Array.from({ length: n.gemas }, (_, k) => ({ x: 40 + k * 40, y: 76, lado: 8 }));
  cartel.textContent = `Nivel ${i + 1}: ${n.nombre}`;
}

const teclas = new Set<string>();
addEventListener('keydown', (e: KeyboardEvent) => teclas.add(e.key));
addEventListener('keyup', (e: KeyboardEvent) => teclas.delete(e.key));

let antes: number | null = null;
function cuadro(ahora: number): void {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (teclas.has('ArrowRight')) heroe.x = Math.min(heroe.x + heroe.velocidad * dt, 240 - heroe.lado);
  gemas = gemas.filter((g) => !chocan(heroe, g));
  ___
  pincel.clearRect(0, 0, 240, 160);
  pincel.fillStyle = '#4fc3f7';
  for (const g of gemas) pincel.fillRect(g.x, g.y, g.lado, g.lado);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(Math.round(heroe.x), heroe.y, heroe.lado, heroe.lado);
  requestAnimationFrame(cuadro);
}
cargar(0);
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#nivel: Nivel 2: Orión
lienzo: clearRect(0, 0, 240, 160)
lienzo: fillRect(120, 76, 8, 8) #4fc3f7
lienzo: fillRect(160, 76, 8, 8) #4fc3f7
lienzo: fillRect(200, 76, 8, 8) #4fc3f7
lienzo: fillRect(70, 74, 12, 12) #f2c14e
```

#### Solución
```typescript
interface Caja { x: number; y: number; lado: number }
interface Nivel { nombre: string; gemas: number }

const NIVELES = [
  { nombre: 'La Lira', gemas: 3 },
  { nombre: 'Orión', gemas: 5 },
] satisfies readonly Nivel[];

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}
const chocan = (a: Caja, b: Caja) => a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;

const ctx = obtenerElemento<HTMLCanvasElement>('#lienzo').getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;
const cartel = obtenerElemento<HTMLParagraphElement>('#nivel');

const heroe = { x: 0, y: 74, lado: 12, velocidad: 120 };
let indice = 0;
let gemas: Caja[] = [];

function cargar(i: number): void {
  indice = i;
  const n: Nivel | undefined = NIVELES[i];
  if (!n) {
    cartel.textContent = '¡Ganaste!';
    gemas = [];
    return;
  }
  heroe.x = 0;
  gemas = Array.from({ length: n.gemas }, (_, k) => ({ x: 40 + k * 40, y: 76, lado: 8 }));
  cartel.textContent = `Nivel ${i + 1}: ${n.nombre}`;
}

const teclas = new Set<string>();
addEventListener('keydown', (e: KeyboardEvent) => teclas.add(e.key));
addEventListener('keyup', (e: KeyboardEvent) => teclas.delete(e.key));

let antes: number | null = null;
function cuadro(ahora: number): void {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (teclas.has('ArrowRight')) heroe.x = Math.min(heroe.x + heroe.velocidad * dt, 240 - heroe.lado);
  gemas = gemas.filter((g) => !chocan(heroe, g));
  if (gemas.length === 0) cargar(indice + 1);
  pincel.clearRect(0, 0, 240, 160);
  pincel.fillStyle = '#4fc3f7';
  for (const g of gemas) pincel.fillRect(g.x, g.y, g.lado, g.lado);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(Math.round(heroe.x), heroe.y, heroe.lado, heroe.lado);
  requestAnimationFrame(cuadro);
}
cargar(0);
requestAnimationFrame(cuadro);
```

#### Al superarla
Con la tercera gema, el héroe vuelve al principio y aparecen cinco gemas nuevas: Orión. Fuelle ladra con un silbidito de vapor.

#### Imagen
- El lienzo de vidrio de la cúpula con un cartel de nivel encendido y una fila de cinco gemas celestes.
- Fuelle (zorro mecánico de latón con cola de engranajes) suelta un silbidito de vapor.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) aprieta una tecla de flecha de bronce; Gheco cuenta las gemas.

### Micro-misión S05-N01-P5 · La dificultad

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Nima
carta: Record<Dificultad, …> | 'fácil' | 'normal' | 'difícil' · cada una con su multiplicador · nada de números sueltos
recompensa: xp 15, monedas 5
```

#### Escena
Los chicos de la Feria son de todas las edades. Nima pide tres dificultades: en **fácil** los goblins van a la mitad de velocidad y hay 5 vidas; en **difícil**, al doble y con 2 vidas.

#### Gheco sugiere
Un `Record<Dificultad, Ajuste>` guarda cada ajuste. Para calcular la velocidad de un nivel: `nivel.velocidad * AJUSTES[d].velocidad`.

#### Desafío
Completá la cuenta de la velocidad.

#### Pasos
1. Buscá el `___` en `preparar`.
2. Cambialo por `nivel.velocidad * AJUSTES[d].velocidad`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Dificultad = 'fácil' | 'normal' | 'difícil';
interface Ajuste { velocidad: number; vidas: number }

const AJUSTES: Record<Dificultad, Ajuste> = {
  fácil: { velocidad: 0.5, vidas: 5 },
  normal: { velocidad: 1, vidas: 3 },
  difícil: { velocidad: 2, vidas: 2 },
};

function preparar(nivel: { velocidad: number }, d: Dificultad): string {
  const velocidad = ___;
  return `${d}: goblins a ${velocidad}, ${AJUSTES[d].vidas} vidas`;
}

const orion = { nombre: 'Orión', velocidad: 36 };
for (const d of ['fácil', 'normal', 'difícil'] as const) console.log(preparar(orion, d));
```

#### Salida esperada
```
fácil: goblins a 18, 5 vidas
normal: goblins a 36, 3 vidas
difícil: goblins a 72, 2 vidas
```

#### Solución
```typescript
type Dificultad = 'fácil' | 'normal' | 'difícil';
interface Ajuste { velocidad: number; vidas: number }

const AJUSTES: Record<Dificultad, Ajuste> = {
  fácil: { velocidad: 0.5, vidas: 5 },
  normal: { velocidad: 1, vidas: 3 },
  difícil: { velocidad: 2, vidas: 2 },
};

function preparar(nivel: { velocidad: number }, d: Dificultad): string {
  const velocidad = nivel.velocidad * AJUSTES[d].velocidad;
  return `${d}: goblins a ${velocidad}, ${AJUSTES[d].vidas} vidas`;
}

const orion = { nombre: 'Orión', velocidad: 36 };
for (const d of ['fácil', 'normal', 'difícil'] as const) console.log(preparar(orion, d));
```

#### Al superarla
El domingo, una nena de seis años juega en fácil y llega a Orión. Un chico de quince juega en difícil y pierde enseguida, y vuelve a la fila para probar de nuevo.

#### Imagen
- Tres palancas de bronce con un caracol, un zorro y un halcón grabados.
- Una fila de chicos y chicas de distintas edades esperando para jugar, con ropa de abrigo.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro) ayuda a una nena a elegir la palanca del caracol; Rigel (chico flaco con pecas, antiparras de latón) ajusta las palancas; Gheco en la fila.

## S05-N02 · Enemigos con clases

```meta
tipo: tema
padre: S05-N01
precio: 10
criatura: goblin
temas: poo.polimorfismo
usa: poo.abstractas, poo.herencia, juegos.ia, js.canvas, cal.tipos
```

### Crónica

Con un solo tipo de goblin, el juego se vuelve aburrido rápido. Nima propone más enemigos, inspirados en las criaturas de cuerda del Mirador: el **goblin** que persigue, el **murciélago** que vuela en zigzag y la **torreta** que se queda quieta y gira.

—Cada uno se mueve distinto —dice Gheco—, pero para el juego son todos **enemigos**. El bucle no tiene que saber cuál es cuál: le dice a cada uno que se mueva, y cada uno sabe cómo.

### Objetivos

- Escribir una clase base abstracta `Enemigo` con un método abstracto `mover`.
- Escribir enemigos distintos que la extienden con `override` (o la implementan).
- Recorrer una lista de enemigos sin saber de qué clase es cada uno (polimorfismo).
- Fabricar enemigos con una función que usa un `switch` con `never`.
- Dibujar cada enemigo con su propio color en el lienzo.

### Antes de empezar

- Herencia, `abstract` y `override` (R02-N03).
- El modelo tipado del juego (R05-N02).

### Explicación

#### La clase base
```typescript
abstract class Enemigo {
  constructor(public x: number, public y: number, readonly lado = 12) {}
  abstract mover(dt: number, objetivo: { x: number; y: number }): void;
  abstract readonly color: string;
}
```
No se puede hacer `new Enemigo(…)`: es un molde incompleto. Cada clase hija completa `mover` y `color`.

#### Cada uno a su manera
```typescript
class Goblin extends Enemigo {
  readonly color = '#7cb342';
  mover(dt: number, objetivo: { x: number; y: number }): void { /* persigue */ }
}
```

#### Polimorfismo
```typescript
const enemigos: Enemigo[] = [new Goblin(10, 10), new Murcielago(50, 40), new Torreta(100, 80)];
for (const e of enemigos) e.mover(dt, heroe);   // cada uno a su manera
```

### Código de ejemplo

```typescript
abstract class Criatura {
  abstract sonido(): string;
  presentarse(): string { return `Hago ${this.sonido()}`; }
}
class Goblin extends Criatura { sonido() { return 'clic-clac'; } }
class Murcielago extends Criatura { sonido() { return 'fiu-fiu'; } }
for (const c of [new Goblin(), new Murcielago()]) console.log(c.presentarse());
```

### Salida esperada

```
Hago clic-clac
Hago fiu-fiu
```

### ¿Para qué sirve?

Así se escriben los juegos (y muchos programas): una lista de cosas distintas que responden al mismo mensaje. Agregar un enemigo nuevo es escribir **una clase nueva**, sin tocar el bucle.

### Errores habituales

**Goblin: olvidarse de completar el método abstracto.** La clase hija no compila (TS2515) hasta que lo escribe.

**Ogro: un `if` por cada tipo de enemigo en el bucle.** Cada enemigo nuevo obliga a tocarlo. Mejor que cada uno sepa moverse.

**Esqueleto: `new` de la clase abstracta.** TS2511: no se puede crear una instancia de una clase abstracta.

### Micro-misión S05-N02-P1 · El goblin que persigue

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Nima
criatura: goblin
carta: Completar lo abstracto | class Goblin extends Enemigo · mover persigue con la dirección normalizada · color propio
recompensa: xp 10, oro 10
```

#### Escena
Rigel escribe el molde de todos los enemigos y el primero de ellos: el goblin, que persigue al héroe.

#### Gheco sugiere
El goblin avanza hacia el objetivo con la dirección dividida por su largo (como en el Atlas). Falta el `mover` del goblin.

#### Desafío
Completá el `mover` del goblin.

#### Pasos
1. Buscá el `___` adentro de `mover`.
2. Cambialo por `if (largo > 0) { this.x += (dx / largo) * this.velocidad * dt; this.y += (dy / largo) * this.velocidad * dt; }`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Punto { x: number; y: number }

abstract class Enemigo {
  constructor(public x: number, public y: number) {}
  abstract readonly color: string;
  abstract mover(dt: number, objetivo: Punto): void;
}

class Goblin extends Enemigo {
  readonly color = '#7cb342';
  velocidad = 25;
  mover(dt: number, objetivo: Punto): void {
    const dx = objetivo.x - this.x;
    const dy = objetivo.y - this.y;
    const largo = Math.hypot(dx, dy);
    ___
  }
}

const goblin = new Goblin(70, 60);
goblin.mover(1, { x: 100, y: 100 });
console.log(`Goblin en (${goblin.x}, ${goblin.y}), color ${goblin.color}`);
```

#### Salida esperada
```
Goblin en (85, 80), color #7cb342
```

#### Solución
```typescript
interface Punto { x: number; y: number }

abstract class Enemigo {
  constructor(public x: number, public y: number) {}
  abstract readonly color: string;
  abstract mover(dt: number, objetivo: Punto): void;
}

class Goblin extends Enemigo {
  readonly color = '#7cb342';
  velocidad = 25;
  mover(dt: number, objetivo: Punto): void {
    const dx = objetivo.x - this.x;
    const dy = objetivo.y - this.y;
    const largo = Math.hypot(dx, dy);
    if (largo > 0) { this.x += (dx / largo) * this.velocidad * dt; this.y += (dy / largo) * this.velocidad * dt; }
  }
}

const goblin = new Goblin(70, 60);
goblin.mover(1, { x: 100, y: 100 });
console.log(`Goblin en (${goblin.x}, ${goblin.y}), color ${goblin.color}`);
```

#### Al superarla
El goblin verde da su primer paso en la cúpula, exactamente 25 de largo, derecho hacia el héroe.

#### Imagen
- Un molde de bronce vacío con forma de criatura, y al lado un goblin de cuerda verde recién salido del molde.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) le da cuerda al goblin.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) mira; Gheco se esconde detrás del molde.

### Micro-misión S05-N02-P2 · El murciélago en zigzag

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco
carta: Otra forma de moverse | class Murcielago extends Enemigo · avanza en x y oscila en y con Math.sin · su propio tiempo
recompensa: xp 10, oro 10
```

#### Escena
El murciélago de cuerda no persigue: vuela de izquierda a derecha subiendo y bajando, como una ola.

#### Gheco sugiere
El murciélago lleva su propio reloj (`t`). En cada `mover`, suma `dt` al reloj, avanza en `x` y calcula `y` con un seno alrededor de su altura base: `this.y = this.base + Math.sin(this.t * 2) * 20`.

#### Desafío
Completá la línea de la altura.

#### Pasos
1. Buscá el `___` en `mover`.
2. Cambialo por `this.y = this.base + Math.sin(this.t * 2) * 20;`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Punto { x: number; y: number }

abstract class Enemigo {
  constructor(public x: number, public y: number) {}
  abstract readonly color: string;
  abstract mover(dt: number, objetivo: Punto): void;
}

class Murcielago extends Enemigo {
  readonly color = '#9575cd';
  private t = 0;
  private readonly base: number;
  constructor(x: number, y: number) {
    super(x, y);
    this.base = y;
  }
  mover(dt: number): void {
    this.t += dt;
    this.x += 30 * dt;
    ___
  }
}

const murcielago = new Murcielago(0, 80);
for (let i = 0; i < 4; i++) {
  murcielago.mover(0.5);
  console.log(`(${murcielago.x}, ${Math.round(murcielago.y)})`);
}
```

#### Salida esperada
```
(15, 97)
(30, 98)
(45, 83)
(60, 65)
```

#### Solución
```typescript
interface Punto { x: number; y: number }

abstract class Enemigo {
  constructor(public x: number, public y: number) {}
  abstract readonly color: string;
  abstract mover(dt: number, objetivo: Punto): void;
}

class Murcielago extends Enemigo {
  readonly color = '#9575cd';
  private t = 0;
  private readonly base: number;
  constructor(x: number, y: number) {
    super(x, y);
    this.base = y;
  }
  mover(dt: number): void {
    this.t += dt;
    this.x += 30 * dt;
    this.y = this.base + Math.sin(this.t * 2) * 20;
  }
}

const murcielago = new Murcielago(0, 80);
for (let i = 0; i < 4; i++) {
  murcielago.mover(0.5);
  console.log(`(${murcielago.x}, ${Math.round(murcielago.y)})`);
}
```

#### Al superarla
El murciélago violeta cruza la cúpula haciendo olas. Su `mover` no usa el objetivo, y está bien: puede tener menos parámetros que el del molde.

#### Imagen
- Un murciélago mecánico violeta con alas de tela y varillas de latón, volando en una línea ondulada punteada.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) dibuja la ola en una pizarra.
- Gheco imita el vuelo con los brazos abiertos.

### Micro-misión S05-N02-P3 · Todos se mueven

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Nima
carta: Polimorfismo | una lista Enemigo[] · e.mover(dt, heroe) en cada uno · cada clase a su manera · instanceof para contar
recompensa: xp 10, oro 10
```

#### Escena
Ya hay tres clases de enemigos. Rigel los pone a todos en una sola lista y el bucle les dice a todos que se muevan, sin preguntar cuál es cuál.

#### Gheco sugiere
`for (const e of enemigos) e.mover(1, heroe);`: cada uno usa su propio `mover`. Para contar los de una clase, `instanceof`.

#### Desafío
Completá el recorrido que mueve a todos.

#### Pasos
1. Buscá el `___`.
2. Cambialo por `for (const e of enemigos) e.mover(1, heroe);`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Punto { x: number; y: number }

abstract class Enemigo {
  constructor(public x: number, public y: number) {}
  abstract readonly nombre: string;
  abstract mover(dt: number, objetivo: Punto): void;
}

class Goblin extends Enemigo {
  readonly nombre = 'goblin';
  mover(dt: number, o: Punto): void {
    this.x += Math.sign(o.x - this.x) * 10 * dt;
    this.y += Math.sign(o.y - this.y) * 10 * dt;
  }
}

class Murcielago extends Enemigo {
  readonly nombre = 'murciélago';
  mover(dt: number): void {
    this.x += 30 * dt;
  }
}

class Torreta extends Enemigo {
  readonly nombre = 'torreta';
  mover(): void {}
}

const heroe = { x: 100, y: 100 };
const enemigos: Enemigo[] = [new Goblin(50, 50), new Murcielago(0, 20), new Torreta(200, 150), new Goblin(120, 130)];

___

for (const e of enemigos) console.log(`${e.nombre}: (${e.x}, ${e.y})`);
console.log(`Goblins: ${enemigos.filter((e) => e instanceof Goblin).length}`);
```

#### Salida esperada
```
goblin: (60, 60)
murciélago: (30, 20)
torreta: (200, 150)
goblin: (110, 120)
Goblins: 2
```

#### Solución
```typescript
interface Punto { x: number; y: number }

abstract class Enemigo {
  constructor(public x: number, public y: number) {}
  abstract readonly nombre: string;
  abstract mover(dt: number, objetivo: Punto): void;
}

class Goblin extends Enemigo {
  readonly nombre = 'goblin';
  mover(dt: number, o: Punto): void {
    this.x += Math.sign(o.x - this.x) * 10 * dt;
    this.y += Math.sign(o.y - this.y) * 10 * dt;
  }
}

class Murcielago extends Enemigo {
  readonly nombre = 'murciélago';
  mover(dt: number): void {
    this.x += 30 * dt;
  }
}

class Torreta extends Enemigo {
  readonly nombre = 'torreta';
  mover(): void {}
}

const heroe = { x: 100, y: 100 };
const enemigos: Enemigo[] = [new Goblin(50, 50), new Murcielago(0, 20), new Torreta(200, 150), new Goblin(120, 130)];

for (const e of enemigos) e.mover(1, heroe);

for (const e of enemigos) console.log(`${e.nombre}: (${e.x}, ${e.y})`);
console.log(`Goblins: ${enemigos.filter((e) => e instanceof Goblin).length}`);
```

#### Al superarla
Los cuatro enemigos se mueven a la vez, cada uno a su manera. La torreta, quieta como siempre, ni se entera.

#### Imagen
- Cuatro criaturas de cuerda en la cúpula (dos goblins verdes, un murciélago violeta y una torreta de latón quieta) moviéndose en direcciones distintas.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro) dirige como una directora de orquesta.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) anota posiciones; Gheco sentado sobre la torreta.

### Micro-misión S05-N02-P4 · La fábrica de enemigos

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco
criatura: ogre
carta: Fábrica con never | crearEnemigo(tipo: TipoEnemigo, x, y) · un case por tipo · el never avisa si falta uno
recompensa: xp 15, monedas 5
```

#### Escena
Los niveles se escriben con texto: «goblin», «murciélago», «torreta». Rigel arma una **fábrica** que convierte cada palabra en su enemigo. Nima agregó un tipo nuevo, el **topo**, y la fábrica no lo conoce.

#### Gheco sugiere
El `never` del `default` encuentra el tipo que falta. Ya existe la clase `Topo`: agregá su `case`.

#### Desafío
Agregá el caso del topo.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el `___`, escribí `case 'topo': return new Topo(x, y);`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
abstract class Enemigo {
  constructor(public x: number, public y: number) {}
  abstract readonly nombre: string;
}
class Goblin extends Enemigo { readonly nombre = 'goblin'; }
class Murcielago extends Enemigo { readonly nombre = 'murciélago'; }
class Torreta extends Enemigo { readonly nombre = 'torreta'; }
class Topo extends Enemigo { readonly nombre = 'topo'; }

type TipoEnemigo = 'goblin' | 'murciélago' | 'torreta' | 'topo';

function crearEnemigo(tipo: TipoEnemigo, x: number, y: number): Enemigo {
  switch (tipo) {
    case 'goblin': return new Goblin(x, y);
    case 'murciélago': return new Murcielago(x, y);
    case 'torreta': return new Torreta(x, y);
    ___
    default: {
      const nunca: never = tipo;
      return nunca;
    }
  }
}

const nivel: [TipoEnemigo, number, number][] = [['goblin', 10, 10], ['topo', 120, 140], ['torreta', 200, 30]];
const enemigos = nivel.map(([tipo, x, y]) => crearEnemigo(tipo, x, y));
console.log(enemigos.map((e) => `${e.nombre} en (${e.x}, ${e.y})`).join('\n'));
```

#### Salida esperada
```
goblin en (10, 10)
topo en (120, 140)
torreta en (200, 30)
```

#### Solución
```typescript
abstract class Enemigo {
  constructor(public x: number, public y: number) {}
  abstract readonly nombre: string;
}
class Goblin extends Enemigo { readonly nombre = 'goblin'; }
class Murcielago extends Enemigo { readonly nombre = 'murciélago'; }
class Torreta extends Enemigo { readonly nombre = 'torreta'; }
class Topo extends Enemigo { readonly nombre = 'topo'; }

type TipoEnemigo = 'goblin' | 'murciélago' | 'torreta' | 'topo';

function crearEnemigo(tipo: TipoEnemigo, x: number, y: number): Enemigo {
  switch (tipo) {
    case 'goblin': return new Goblin(x, y);
    case 'murciélago': return new Murcielago(x, y);
    case 'torreta': return new Torreta(x, y);
    case 'topo': return new Topo(x, y);
    default: {
      const nunca: never = tipo;
      return nunca;
    }
  }
}

const nivel: [TipoEnemigo, number, number][] = [['goblin', 10, 10], ['topo', 120, 140], ['torreta', 200, 30]];
const enemigos = nivel.map(([tipo, x, y]) => crearEnemigo(tipo, x, y));
console.log(enemigos.map((e) => `${e.nombre} en (${e.x}, ${e.y})`).join('\n'));
```

#### Al superarla
El topo de cuerda asoma por un agujero del lienzo. Los chicos de la Feria gritan de sorpresa el domingo siguiente.

#### Imagen
- Una máquina fabricante de bronce con una cinta que saca criaturas de cuerda (un goblin, un topo, una torreta).
- Un ogro de cuerda chiquito tapando la salida del topo.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) aprieta un botón de la máquina; Gheco saluda al topo.

### Micro-misión S05-N02-P5 · Cada uno con su color

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Fuelle
carta: dibujar polimórfico | cada enemigo tiene su color · el bucle dibuja a todos con el mismo código · el lienzo muestra la verdad
recompensa: xp 15, monedas 5
```

#### Escena
Rigel pone los enemigos en el lienzo. El bucle los mueve y los dibuja a todos con el mismo código: cada uno con su color.

#### Gheco sugiere
Para dibujar, se usa el color de cada enemigo: `pincel.fillStyle = e.color;` y después el cuadrado. Falta esa línea del color.

#### Desafío
Completá la línea del color.

#### Pasos
1. Buscá el `___` en el bucle de dibujo.
2. Cambialo por `pincel.fillStyle = e.color;`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1326; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="240" height="160"></canvas>
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
interface Punto { x: number; y: number }

abstract class Enemigo {
  readonly lado = 12;
  constructor(public x: number, public y: number) {}
  abstract readonly color: string;
  abstract mover(dt: number, objetivo: Punto): void;
}

class Goblin extends Enemigo {
  readonly color = '#7cb342';
  mover(dt: number, o: Punto): void {
    const dx = o.x - this.x, dy = o.y - this.y, largo = Math.hypot(dx, dy);
    if (largo > 0) { this.x += (dx / largo) * 25 * dt; this.y += (dy / largo) * 25 * dt; }
  }
}

class Murcielago extends Enemigo {
  readonly color = '#9575cd';
  mover(dt: number): void {
    this.x = (this.x + 40 * dt) % 240;
  }
}

class Torreta extends Enemigo {
  readonly color = '#b0855a';
  mover(): void {}
}

const lienzo = document.querySelector<HTMLCanvasElement>('#lienzo');
const ctx = lienzo?.getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;

const heroe = { x: 114, y: 74, lado: 12 };
const enemigos: Enemigo[] = [new Goblin(10, 10), new Murcielago(0, 120), new Torreta(200, 20)];

let antes: number | null = null;
function cuadro(ahora: number): void {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  pincel.clearRect(0, 0, 240, 160);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(heroe.x, heroe.y, heroe.lado, heroe.lado);
  for (const e of enemigos) {
    e.mover(dt, heroe);
    ___
    pincel.fillRect(Math.round(e.x), Math.round(e.y), e.lado, e.lado);
  }
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 240, 160)
lienzo: fillRect(114, 74, 12, 12) #f2c14e
lienzo: fillRect(31, 23, 12, 12) #7cb342
lienzo: fillRect(39, 120, 12, 12) #9575cd
lienzo: fillRect(200, 20, 12, 12) #b0855a
```

#### Solución
```typescript
interface Punto { x: number; y: number }

abstract class Enemigo {
  readonly lado = 12;
  constructor(public x: number, public y: number) {}
  abstract readonly color: string;
  abstract mover(dt: number, objetivo: Punto): void;
}

class Goblin extends Enemigo {
  readonly color = '#7cb342';
  mover(dt: number, o: Punto): void {
    const dx = o.x - this.x, dy = o.y - this.y, largo = Math.hypot(dx, dy);
    if (largo > 0) { this.x += (dx / largo) * 25 * dt; this.y += (dy / largo) * 25 * dt; }
  }
}

class Murcielago extends Enemigo {
  readonly color = '#9575cd';
  mover(dt: number): void {
    this.x = (this.x + 40 * dt) % 240;
  }
}

class Torreta extends Enemigo {
  readonly color = '#b0855a';
  mover(): void {}
}

const lienzo = document.querySelector<HTMLCanvasElement>('#lienzo');
const ctx = lienzo?.getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;

const heroe = { x: 114, y: 74, lado: 12 };
const enemigos: Enemigo[] = [new Goblin(10, 10), new Murcielago(0, 120), new Torreta(200, 20)];

let antes: number | null = null;
function cuadro(ahora: number): void {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  pincel.clearRect(0, 0, 240, 160);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(heroe.x, heroe.y, heroe.lado, heroe.lado);
  for (const e of enemigos) {
    e.mover(dt, heroe);
    pincel.fillStyle = e.color;
    pincel.fillRect(Math.round(e.x), Math.round(e.y), e.lado, e.lado);
  }
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
En la cúpula se ven los tres enemigos con sus colores: el goblin verde que se acerca, el murciélago violeta que cruza y la torreta marrón, quieta. Fuelle les gruñe con un silbido.

#### Imagen
- El lienzo de vidrio de la cúpula con un cuadrado dorado en el centro y tres cuadrados de colores (verde, violeta, marrón).
- Fuelle (zorro mecánico de latón con cola de engranajes) gruñe soltando vapor.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) pinta con un pincel de latón; Gheco elige colores de una paleta.

## S05-N03 · Partículas y Fuelle

```meta
tipo: tema
padre: S05-N02
precio: 10
criatura: troll
temas: juegos.fisica
usa: poo.genericos, poo.clases, juegos.bucle, juegos.colisiones, js.canvas
```

### Crónica

Nima dice que al juego le falta **brillo**: cuando el héroe junta una gema, tendría que saltar una lluvia de chispas. Y Fuelle quiere jugar: que el zorro mecánico **siga al héroe** por la cúpula y lo ayude a juntar las gemas que quedan cerca.

—Las chispas son muchas y viven poco —dice Gheco—. Si se crea una nueva cada vez, el juego se pone lento. Mejor reusarlas.

### Objetivos

- Mover partículas con velocidad, gravedad y un tiempo de vida.
- Reusar objetos con una clase genérica `Pool<T>`.
- Hacer que Fuelle siga al héroe con suavidad (interpolación).
- Juntar gemas en un radio alrededor de Fuelle.
- Verlo todo en el lienzo.

### Antes de empezar

- S05-N01 y S05-N02.
- Clases genéricas (R02-N06).

### Explicación

#### Una partícula
```typescript
interface Particula { x: number; y: number; vx: number; vy: number; vida: number }

function actualizar(p: Particula, dt: number): void {
  p.vy += 200 * dt;      // la gravedad la tira para abajo
  p.x += p.vx * dt;
  p.y += p.vy * dt;
  p.vida -= dt;          // cuando llega a 0, desaparece
}
```

#### Reusar en vez de crear
```typescript
class Pool<T> {
  private libres: T[] = [];
  constructor(private readonly crear: () => T) {}
  tomar(): T { return this.libres.pop() ?? this.crear(); }
  devolver(x: T): void { this.libres.push(x); }
}
```

#### Seguir con suavidad
```typescript
fuelle.x += (heroe.x - fuelle.x) * 0.1;   // se acerca un 10% de lo que falta
```
Cuanto más lejos está, más rápido va; cuando está cerca, casi no se mueve. Se llama **interpolación**.

### Código de ejemplo

```typescript
let x = 0;
const objetivo = 100;
const pasos: number[] = [];
for (let i = 0; i < 4; i++) {
  x += (objetivo - x) * 0.5;
  pasos.push(x);
}
console.log(pasos.join(' → '));
```

### Salida esperada

```
50 → 75 → 87.5 → 93.75
```

### ¿Para qué sirve?

Las chispas, el humo, la lluvia y las explosiones de todos los juegos son partículas. Reusar objetos (un *pool*) es una técnica clásica para que un programa no se trabe. Y la interpolación está en todas las cámaras que siguen a un personaje.

### Errores habituales

**Troll: partículas que nunca mueren.** Si no se descuentan ni se quitan, se acumulan hasta que el juego se arrastra.

**Ogro: el compañero que salta al lugar del héroe.** Sin interpolación, se mueve a los tirones.

**Goblin: devolver al pool algo que se sigue usando.** El mismo objeto termina en dos lugares a la vez.

### Micro-misión S05-N03-P1 · Las chispas

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Nima
carta: Partículas | velocidad, gravedad y vida · actualizar cada una · filter se queda con las vivas
recompensa: xp 10, oro 10
```

#### Escena
Rigel arma las primeras chispas: salen disparadas, caen por la gravedad y se apagan cuando se les termina la vida.

#### Gheco sugiere
Después de actualizar todas, se dejan solo las que tienen vida: `chispas.filter((p) => p.vida > 0)`.

#### Desafío
Completá la línea que se queda con las vivas.

#### Pasos
1. Buscá el `___`.
2. Cambialo por `chispas = chispas.filter((p) => p.vida > 0);`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Particula { x: number; y: number; vx: number; vy: number; vida: number }

function actualizar(p: Particula, dt: number): void {
  p.vy += 200 * dt;
  p.x += p.vx * dt;
  p.y += p.vy * dt;
  p.vida -= dt;
}

let chispas: Particula[] = [
  { x: 100, y: 100, vx: 40, vy: -80, vida: 0.5 },
  { x: 100, y: 100, vx: -40, vy: -60, vida: 0.3 },
  { x: 100, y: 100, vx: 0, vy: -100, vida: 0.2 },
];

for (let paso = 1; paso <= 3; paso++) {
  for (const p of chispas) actualizar(p, 0.1);
  ___
  console.log(`Paso ${paso}: ${chispas.length} chispas`);
}
const primera = chispas[0];
if (primera) console.log(`La última está en (${primera.x.toFixed(0)}, ${primera.y.toFixed(0)})`);
```

#### Salida esperada
```
Paso 1: 3 chispas
Paso 2: 2 chispas
Paso 3: 1 chispas
La última está en (112, 88)
```

#### Solución
```typescript
interface Particula { x: number; y: number; vx: number; vy: number; vida: number }

function actualizar(p: Particula, dt: number): void {
  p.vy += 200 * dt;
  p.x += p.vx * dt;
  p.y += p.vy * dt;
  p.vida -= dt;
}

let chispas: Particula[] = [
  { x: 100, y: 100, vx: 40, vy: -80, vida: 0.5 },
  { x: 100, y: 100, vx: -40, vy: -60, vida: 0.3 },
  { x: 100, y: 100, vx: 0, vy: -100, vida: 0.2 },
];

for (let paso = 1; paso <= 3; paso++) {
  for (const p of chispas) actualizar(p, 0.1);
  chispas = chispas.filter((p) => p.vida > 0);
  console.log(`Paso ${paso}: ${chispas.length} chispas`);
}
const primera = chispas[0];
if (primera) console.log(`La última está en (${primera.x.toFixed(0)}, ${primera.y.toFixed(0)})`);
```

#### Al superarla
Las chispas saltan, caen y se apagan una por una. Nima aplaude como si fueran fuegos artificiales.

#### Imagen
- Una lluvia de chispas doradas saltando en arco desde una gema, con las de abajo apagándose.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) aplaude.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mira con las antiparras puestas; Gheco atrapa una chispa.

### Micro-misión S05-N03-P2 · Reusar las chispas

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco
criatura: troll
carta: Pool<T> genérico | tomar(): la libre o una nueva · devolver(x): vuelve a la pila · se crean pocas
recompensa: xp 10, oro 10
```

#### Escena
Con muchas gemas, el juego crea cientos de chispas y se pone lento. Rigel arma un **pool**: una pila de chispas apagadas que se vuelven a usar.

#### Gheco sugiere
`tomar` saca una chispa libre de la pila con `pop()`; si no hay ninguna, crea una nueva con `this.crear()`. El `??` hace las dos cosas en una línea.

#### Desafío
Completá `tomar`.

#### Pasos
1. Buscá el `___` en `tomar`.
2. Cambialo por `return this.libres.pop() ?? this.crear();`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
class Pool<T> {
  private libres: T[] = [];
  creadas = 0;

  constructor(private readonly fabricar: () => T) {}

  private crear(): T {
    this.creadas++;
    return this.fabricar();
  }

  tomar(): T {
    ___
  }

  devolver(x: T): void {
    this.libres.push(x);
  }
}

interface Chispa { x: number; y: number; vida: number }
const pool = new Pool<Chispa>(() => ({ x: 0, y: 0, vida: 0 }));

for (let gema = 1; gema <= 5; gema++) {
  const usadas = [pool.tomar(), pool.tomar(), pool.tomar()];
  for (const c of usadas) pool.devolver(c);
}
console.log(`Se usaron 15 chispas y se crearon solo ${pool.creadas}`);
```

#### Salida esperada
```
Se usaron 15 chispas y se crearon solo 3
```

#### Solución
```typescript
class Pool<T> {
  private libres: T[] = [];
  creadas = 0;

  constructor(private readonly fabricar: () => T) {}

  private crear(): T {
    this.creadas++;
    return this.fabricar();
  }

  tomar(): T {
    return this.libres.pop() ?? this.crear();
  }

  devolver(x: T): void {
    this.libres.push(x);
  }
}

interface Chispa { x: number; y: number; vida: number }
const pool = new Pool<Chispa>(() => ({ x: 0, y: 0, vida: 0 }));

for (let gema = 1; gema <= 5; gema++) {
  const usadas = [pool.tomar(), pool.tomar(), pool.tomar()];
  for (const c of usadas) pool.devolver(c);
}
console.log(`Se usaron 15 chispas y se crearon solo ${pool.creadas}`);
```

#### Al superarla
Tres chispas hacen el trabajo de quince. El juego vuelve a andar suave, y el troll de cuerda que se colgaba de las chispas se cae de aburrimiento.

#### Imagen
- Un frasco de vidrio con tres chispas apagadas adentro y una tapa de latón con una palanca.
- Un troll de cuerda chiquito dormido al lado del frasco.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) saca una chispa del frasco; Gheco devuelve otra.

### Micro-misión S05-N03-P3 · Fuelle sigue al héroe

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Fuelle
criatura: ogre
carta: Interpolación | fuelle.x += (objetivo.x - fuelle.x) * k · se acerca una parte de lo que falta · llega suave
recompensa: xp 10, oro 10
```

#### Escena
Fuelle quiere seguir al héroe por el lienzo. La primera vez, Rigel lo puso **en el mismo lugar** que el héroe, y Fuelle saltaba de golpe. Ahora lo hace acercarse de a poco.

#### Gheco sugiere
En cada cuadro, Fuelle avanza una parte (`k`) de lo que le falta. Para que no quede encima del héroe, el objetivo está 16 pasos atrás.

#### Desafío
Completá la línea de la `x` de Fuelle.

#### Pasos
1. Buscá el `___` en `seguir`.
2. Cambialo por `fuelle.x += (objetivo.x - 16 - fuelle.x) * k;`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Punto { x: number; y: number }

function seguir(fuelle: Punto, objetivo: Punto, k: number): void {
  ___
  fuelle.y += (objetivo.y - fuelle.y) * k;
}

const heroe = { x: 116, y: 80 };
const fuelle = { x: 0, y: 80 };
const recorrido: number[] = [];
for (let i = 0; i < 5; i++) {
  seguir(fuelle, heroe, 0.5);
  recorrido.push(fuelle.x);
}
console.log(recorrido.join(' → '));
```

#### Salida esperada
```
50 → 75 → 87.5 → 93.75 → 96.875
```

#### Solución
```typescript
interface Punto { x: number; y: number }

function seguir(fuelle: Punto, objetivo: Punto, k: number): void {
  fuelle.x += (objetivo.x - 16 - fuelle.x) * k;
  fuelle.y += (objetivo.y - fuelle.y) * k;
}

const heroe = { x: 116, y: 80 };
const fuelle = { x: 0, y: 80 };
const recorrido: number[] = [];
for (let i = 0; i < 5; i++) {
  seguir(fuelle, heroe, 0.5);
  recorrido.push(fuelle.x);
}
console.log(recorrido.join(' → '));
```

#### Al superarla
Fuelle corre hacia el héroe, rápido al principio y cada vez más despacio, y se sienta justo detrás. Mueve la cola de engranajes, contento.

#### Imagen
- Una línea de huellas mecánicas en el piso de la cúpula, cada vez más juntas, que terminan detrás del héroe.
- Fuelle (zorro mecánico de latón con cola de engranajes) sentado detrás de un cuadrado dorado.
- Un ogro de cuerda chiquito que intentaba hacer saltar a Fuelle; Rigel (chico flaco con pecas, antiparras de latón) acaricia a Fuelle; Gheco sobre la cola.

### Micro-misión S05-N03-P4 · Fuelle ayuda

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Fuelle, Nima
carta: Juntar en un radio | Math.hypot(g.x - fuelle.x, g.y - fuelle.y) < radio · las cercanas se juntan · el resto queda
recompensa: xp 15, monedas 5
```

#### Escena
Nima le enseña un truco a Fuelle: **olfatear** gemas. Las que están a menos de 30 pasos, Fuelle las junta para el héroe.

#### Gheco sugiere
Una gema está cerca si la distancia entre ella y Fuelle (con `Math.hypot`) es menor que el radio. Se separan las cercanas de las lejanas.

#### Desafío
Completá la pregunta de quién está cerca.

#### Pasos
1. Buscá el `___` en `cerca`.
2. Cambialo por `return Math.hypot(g.x - fuelle.x, g.y - fuelle.y) < radio;`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Punto { x: number; y: number }
interface Gema extends Punto { nombre: string }

function cerca(g: Punto, fuelle: Punto, radio: number): boolean {
  ___
}

const fuelle = { x: 100, y: 80 };
let gemas: Gema[] = [
  { nombre: 'Vega', x: 110, y: 90 },
  { nombre: 'Sirio', x: 200, y: 20 },
  { nombre: 'Rigel', x: 80, y: 60 },
  { nombre: 'Arturo', x: 140, y: 80 },
];

const olfateadas = gemas.filter((g) => cerca(g, fuelle, 30));
gemas = gemas.filter((g) => !cerca(g, fuelle, 30));
console.log(`Fuelle juntó: ${olfateadas.map((g) => g.nombre).join(', ')}`);
console.log(`Quedan: ${gemas.map((g) => g.nombre).join(', ')}`);
```

#### Salida esperada
```
Fuelle juntó: Vega, Rigel
Quedan: Sirio, Arturo
```

#### Solución
```typescript
interface Punto { x: number; y: number }
interface Gema extends Punto { nombre: string }

function cerca(g: Punto, fuelle: Punto, radio: number): boolean {
  return Math.hypot(g.x - fuelle.x, g.y - fuelle.y) < radio;
}

const fuelle = { x: 100, y: 80 };
let gemas: Gema[] = [
  { nombre: 'Vega', x: 110, y: 90 },
  { nombre: 'Sirio', x: 200, y: 20 },
  { nombre: 'Rigel', x: 80, y: 60 },
  { nombre: 'Arturo', x: 140, y: 80 },
];

const olfateadas = gemas.filter((g) => cerca(g, fuelle, 30));
gemas = gemas.filter((g) => !cerca(g, fuelle, 30));
console.log(`Fuelle juntó: ${olfateadas.map((g) => g.nombre).join(', ')}`);
console.log(`Quedan: ${gemas.map((g) => g.nombre).join(', ')}`);
```

#### Al superarla
Fuelle vuelve con dos gemas en la boca, moviendo la cola. Arturo quedó un poquito lejos: a 40 pasos.

#### Imagen
- Un círculo de olfato dibujado alrededor de un zorro mecánico, con dos gemas adentro y dos afuera.
- Fuelle (zorro mecánico de latón con cola de engranajes) con dos gemas celestes en la boca.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) le da una palmadita; Rigel (chico flaco con pecas, antiparras de latón) mide el círculo con el calibre; Gheco señala la gema lejana.

### Micro-misión S05-N03-P5 · Chispas y compañía

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Fuelle
carta: Todo en el lienzo | el héroe se mueve · Fuelle lo sigue con interpolación · al juntar, salta una lluvia de chispas · el marcador cuenta
recompensa: xp 15, monedas 5
```

#### Escena
Rigel junta todo en el lienzo: el héroe camina, Fuelle lo sigue, y cada gema que se junta suelta chispas.

#### Gheco sugiere
Cuando el héroe junta una gema, se lanzan chispas desde ese lugar con `lanzarChispas(g.x, g.y)`. Falta esa llamada, adentro del `filter`.

#### Desafío
Completá la llamada a `lanzarChispas`.

#### Pasos
1. Buscá el `___` en `cuadro`.
2. Cambialo por `lanzarChispas(g.x, g.y);`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f2c14e; font-family: monospace; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1326; border: 6px solid #8d6e3f; }
</style>
<p>Gemas: <span id="gemas">0</span></p>
<canvas id="lienzo" width="240" height="160"></canvas>
```

#### Eventos
```
apretar ArrowRight
cuadros 80
soltar ArrowRight
cuadros 5
```

#### Estado
```
#gemas
lienzo
```

#### Código inicial
```typescript
interface Caja { x: number; y: number; lado: number }
interface Chispa { x: number; y: number; vx: number; vy: number; vida: number }

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}
const chocan = (a: Caja, b: Caja) => a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;

const ctx = obtenerElemento<HTMLCanvasElement>('#lienzo').getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;
const marcador = obtenerElemento<HTMLSpanElement>('#gemas');

const heroe: Caja = { x: 30, y: 74, lado: 12 };
const fuelle = { x: 10, y: 78, lado: 8 };
let gemas: Caja[] = [70, 110, 150].map((x) => ({ x, y: 76, lado: 8 }));
let chispas: Chispa[] = [];
let juntadas = 0;

function lanzarChispas(x: number, y: number): void {
  for (let i = 0; i < 6; i++) {
    const angulo = (i / 6) * Math.PI * 2;
    chispas.push({ x, y, vx: Math.cos(angulo) * 60, vy: Math.sin(angulo) * 60 - 40, vida: 0.4 });
  }
}

const teclas = new Set<string>();
addEventListener('keydown', (e: KeyboardEvent) => teclas.add(e.key));
addEventListener('keyup', (e: KeyboardEvent) => teclas.delete(e.key));

let antes: number | null = null;
function cuadro(ahora: number): void {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (teclas.has('ArrowRight')) heroe.x = Math.min(heroe.x + 120 * dt, 240 - heroe.lado);
  fuelle.x += (heroe.x - 16 - fuelle.x) * 0.1;
  gemas = gemas.filter((g) => {
    if (!chocan(heroe, g)) return true;
    juntadas++;
    ___
    return false;
  });
  for (const c of chispas) {
    c.vy += 200 * dt;
    c.x += c.vx * dt;
    c.y += c.vy * dt;
    c.vida -= dt;
  }
  chispas = chispas.filter((c) => c.vida > 0);
  marcador.textContent = String(juntadas);

  pincel.clearRect(0, 0, 240, 160);
  pincel.fillStyle = '#4fc3f7';
  for (const g of gemas) pincel.fillRect(g.x, g.y, g.lado, g.lado);
  pincel.fillStyle = '#ffd54f';
  for (const c of chispas) pincel.fillRect(Math.round(c.x), Math.round(c.y), 2, 2);
  pincel.fillStyle = '#b0855a';
  pincel.fillRect(Math.round(fuelle.x), fuelle.y, fuelle.lado, fuelle.lado);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(Math.round(heroe.x), heroe.y, heroe.lado, heroe.lado);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#gemas: 3
lienzo: clearRect(0, 0, 240, 160)
lienzo: fillRect(161, 78, 8, 8) #b0855a
lienzo: fillRect(188, 74, 12, 12) #f2c14e
```

#### Solución
```typescript
interface Caja { x: number; y: number; lado: number }
interface Chispa { x: number; y: number; vx: number; vy: number; vida: number }

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}
const chocan = (a: Caja, b: Caja) => a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;

const ctx = obtenerElemento<HTMLCanvasElement>('#lienzo').getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;
const marcador = obtenerElemento<HTMLSpanElement>('#gemas');

const heroe: Caja = { x: 30, y: 74, lado: 12 };
const fuelle = { x: 10, y: 78, lado: 8 };
let gemas: Caja[] = [70, 110, 150].map((x) => ({ x, y: 76, lado: 8 }));
let chispas: Chispa[] = [];
let juntadas = 0;

function lanzarChispas(x: number, y: number): void {
  for (let i = 0; i < 6; i++) {
    const angulo = (i / 6) * Math.PI * 2;
    chispas.push({ x, y, vx: Math.cos(angulo) * 60, vy: Math.sin(angulo) * 60 - 40, vida: 0.4 });
  }
}

const teclas = new Set<string>();
addEventListener('keydown', (e: KeyboardEvent) => teclas.add(e.key));
addEventListener('keyup', (e: KeyboardEvent) => teclas.delete(e.key));

let antes: number | null = null;
function cuadro(ahora: number): void {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (teclas.has('ArrowRight')) heroe.x = Math.min(heroe.x + 120 * dt, 240 - heroe.lado);
  fuelle.x += (heroe.x - 16 - fuelle.x) * 0.1;
  gemas = gemas.filter((g) => {
    if (!chocan(heroe, g)) return true;
    juntadas++;
    lanzarChispas(g.x, g.y);
    return false;
  });
  for (const c of chispas) {
    c.vy += 200 * dt;
    c.x += c.vx * dt;
    c.y += c.vy * dt;
    c.vida -= dt;
  }
  chispas = chispas.filter((c) => c.vida > 0);
  marcador.textContent = String(juntadas);

  pincel.clearRect(0, 0, 240, 160);
  pincel.fillStyle = '#4fc3f7';
  for (const g of gemas) pincel.fillRect(g.x, g.y, g.lado, g.lado);
  pincel.fillStyle = '#ffd54f';
  for (const c of chispas) pincel.fillRect(Math.round(c.x), Math.round(c.y), 2, 2);
  pincel.fillStyle = '#b0855a';
  pincel.fillRect(Math.round(fuelle.x), fuelle.y, fuelle.lado, fuelle.lado);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(Math.round(heroe.x), heroe.y, heroe.lado, heroe.lado);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
Cada gema estalla en chispas doradas, y Fuelle corre detrás del héroe, saltando entre las chispas. El domingo, los chicos de la Feria no quieren bajar del Mirador.

#### Imagen
- El lienzo de vidrio de la cúpula con un héroe dorado, un zorro de latón detrás y una lluvia de chispas doradas.
- Fuelle (zorro mecánico de latón con cola de engranajes) saltando entre chispas.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) juega con la tecla de flecha de bronce; Gheco con los ojos llenos de chispas.

## S05-N04 · Jefe: el Eclipse de Hierro

```meta
tipo: jefe
padre: S05-N03
precio: 10
criatura: dragon
insignia: Corona del Planisferio
insignia_descripcion: Venciste al Eclipse de Hierro y el Planisferio Vivo quedó abierto para todos: niveles, enemigos con clases, partículas, Fuelle y un jefe con fases.
usa: juegos.estados, juegos.ia, juegos.guardado, poo.abstractas, poo.genericos, err.validacion, js.canvas
```

### Crónica

Un domingo, mientras los chicos juegan, la cúpula se oscurece. Por encima del Planisferio pasa un disco enorme de hierro, con engranajes en el borde, que tapa las constelaciones una por una: **el Eclipse de Hierro**. Es una pieza vieja del Planisferio, la que el Vidriero usaba para mostrar los eclipses. Se soltó con los años y ahora gira sola, tapándolo todo.

—Si lo metemos en el juego —propone Nima—, lo vencemos jugando. Y de paso los chicos ven el eclipse.

Fuelle suelta un silbido de vapor decidido. Él también quiere pelear.

### Objetivos

- Integrar toda la Senda: niveles, enemigos con clases, partículas y Fuelle.
- Escribir un jefe con fases (una unión) que cambian según su vida.
- Ataques con tiempo de espera.
- Guardar la partida y cargarla con un validador.
- Una barra de vida y la pelea final en el lienzo.

### Antes de empezar

- Toda la Senda del Planisferio Vivo (S05-N01 a N03).

### Explicación

#### Las trampas del Eclipse (y la verdad)
| El Eclipse hace… | La verdad |
|---|---|
| cambia de forma cuando pierde vida | sus fases son una unión, calculadas por la vida |
| ataca sin parar | cada ataque tiene un tiempo de espera |
| borra la partida guardada | lo guardado se lee con un validador |
| tapa la barra de vida | la barra se calcula de la vida, siempre |

### Micro-misión S05-N04-P1 · Las fases del Eclipse

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Nima, el Eclipse de Hierro
criatura: ogre
carta: Trampa 1 | Fase = 'entero' | 'agrietado' | 'roto' · la fase sale de la vida · get fase() calcula
recompensa: xp 15, monedas 3
```

#### Escena
El Eclipse cambia cuando pierde vida: primero está **entero**, después **agrietado** (con menos de 60) y al final **roto** (con menos de 25). Rigel lo escribe como un enemigo más, con su fase calculada.

#### Gheco sugiere
La fase no se guarda: se **calcula** cada vez con un `get`. Así nunca queda una fase que no coincide con la vida.

#### Desafío
Completá el `get fase()`.

#### Pasos
1. Buscá el `___` en `fase`.
2. Cambialo por `return this.vida < 25 ? 'roto' : this.vida < 60 ? 'agrietado' : 'entero';`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Fase = 'entero' | 'agrietado' | 'roto';

abstract class Enemigo {
  constructor(public x: number, public y: number, public vida: number) {}
  abstract readonly nombre: string;
  recibir(golpe: number): void {
    this.vida = Math.max(0, this.vida - golpe);
  }
}

class Eclipse extends Enemigo {
  readonly nombre = 'el Eclipse de Hierro';
  get fase(): Fase {
    ___
  }
}

const eclipse = new Eclipse(180, 40, 100);
for (const golpe of [0, 30, 20, 30]) {
  eclipse.recibir(golpe);
  console.log(`vida ${eclipse.vida}: ${eclipse.fase}`);
}
```

#### Salida esperada
```
vida 100: entero
vida 70: entero
vida 50: agrietado
vida 20: roto
```

#### Solución
```typescript
type Fase = 'entero' | 'agrietado' | 'roto';

abstract class Enemigo {
  constructor(public x: number, public y: number, public vida: number) {}
  abstract readonly nombre: string;
  recibir(golpe: number): void {
    this.vida = Math.max(0, this.vida - golpe);
  }
}

class Eclipse extends Enemigo {
  readonly nombre = 'el Eclipse de Hierro';
  get fase(): Fase {
    return this.vida < 25 ? 'roto' : this.vida < 60 ? 'agrietado' : 'entero';
  }
}

const eclipse = new Eclipse(180, 40, 100);
for (const golpe of [0, 30, 20, 30]) {
  eclipse.recibir(golpe);
  console.log(`vida ${eclipse.vida}: ${eclipse.fase}`);
}
```

#### Al superarla
En la cúpula, el disco de hierro se agrieta por primera vez. Los chicos de la Feria hacen «¡ooooh!».

#### Imagen
- Un disco enorme de hierro con engranajes en el borde, tapando parte de las constelaciones de la cúpula, con una grieta luminosa.
- Un ogro de cuerda chiquito intentando pegar la grieta con cinta.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas, arco verde) mira para arriba; Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) señala la grieta; Gheco se esconde detrás de Rigel.

### Micro-misión S05-N04-P2 · Un ataque, y a esperar

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, el Eclipse de Hierro
criatura: troll
carta: Trampa 2 | cada ataque tiene espera · espera -= dt en cada cuadro · ataca solo si llegó a 0, y vuelve a esperar · más rápido si está roto
recompensa: xp 15, monedas 3
```

#### Escena
El Eclipse lanza sombras sobre el lienzo. Si ataca en cada cuadro, nadie puede jugar. Rigel le pone un **tiempo de espera**: 1 segundo entre ataques (medio segundo si está roto, porque se enoja).

#### Gheco sugiere
En cada cuadro se descuenta `dt` de la espera. Si llegó a 0 o menos, ataca y la espera vuelve a empezar. Falta la pregunta.

#### Desafío
Completá la pregunta del ataque.

#### Pasos
1. Buscá el `___` en `actualizar`.
2. Cambialo por `if (this.espera <= 0) { this.ataques++; this.espera = this.roto ? 0.5 : 1; }`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
class Eclipse {
  espera = 1;
  ataques = 0;
  constructor(public roto: boolean) {}

  actualizar(dt: number): void {
    this.espera -= dt;
    ___
  }
}

for (const roto of [false, true]) {
  const eclipse = new Eclipse(roto);
  for (let i = 0; i < 30; i++) eclipse.actualizar(0.1);
  console.log(`${roto ? 'Roto' : 'Entero'}: ${eclipse.ataques} ataques en 3 segundos`);
}
```

#### Salida esperada
```
Entero: 2 ataques en 3 segundos
Roto: 4 ataques en 3 segundos
```

#### Solución
```typescript
class Eclipse {
  espera = 1;
  ataques = 0;
  constructor(public roto: boolean) {}

  actualizar(dt: number): void {
    this.espera -= dt;
    if (this.espera <= 0) { this.ataques++; this.espera = this.roto ? 0.5 : 1; }
  }
}

for (const roto of [false, true]) {
  const eclipse = new Eclipse(roto);
  for (let i = 0; i < 30; i++) eclipse.actualizar(0.1);
  console.log(`${roto ? 'Roto' : 'Entero'}: ${eclipse.ataques} ataques en 3 segundos`);
}
```

#### Al superarla
Las sombras del Eclipse caen con ritmo, y se pueden esquivar. Cuando se rompe, atacan más seguido: se pone emocionante.

#### Imagen
- Sombras con forma de disco cayendo sobre el lienzo de la cúpula a intervalos, con un reloj de arena de latón al costado.
- Un troll de cuerda chiquito dando vuelta el reloj de arena antes de tiempo.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) esquiva una sombra; Gheco le saca el reloj al troll.

### Micro-misión S05-N04-P3 · La partida guardada

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Nima, el Eclipse de Hierro
criatura: skeleton
carta: Trampa 3 | lo guardado es unknown · el guardia revisa nivel y récord · si está roto, partida nueva
recompensa: xp 15, monedas 3
```

#### Escena
El Eclipse pasó por encima de la memoria del Mirador y la dejó llena de garabatos: la partida guardada dice nivel **"muchos"**. Si el juego la carga sin revisar, se rompe.

#### Gheco sugiere
`esPartida` revisa que lo guardado sea un objeto con `nivel` y `record` numéricos. Falta la pregunta por los campos.

#### Desafío
Completá el guardia.

#### Pasos
1. Buscá el `___` en `esPartida`.
2. Cambialo por `'nivel' in x && typeof x.nivel === 'number' && 'record' in x && typeof x.record === 'number'`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Almacenamiento
```
local partida = {"nivel":"muchos","record":12}
```

#### Estado
```
local partida
```

#### Código inicial
```typescript
interface Partida { nivel: number; record: number }

function esPartida(x: unknown): x is Partida {
  return typeof x === 'object' && x !== null && ___;
}

function cargar(): Partida {
  try {
    const leido: unknown = JSON.parse(localStorage.getItem('partida') ?? 'null');
    return esPartida(leido) ? leido : { nivel: 1, record: 0 };
  } catch {
    return { nivel: 1, record: 0 };
  }
}

const guardar = (p: Partida) => localStorage.setItem('partida', JSON.stringify(p));

const primera = cargar();
console.log(`Arranca en el nivel ${primera.nivel} (récord ${primera.record})`);
guardar({ nivel: 3, record: 18 });
const segunda = cargar();
console.log(`Arranca en el nivel ${segunda.nivel} (récord ${segunda.record})`);
```

#### Salida esperada
```
Arranca en el nivel 1 (récord 0)
Arranca en el nivel 3 (récord 18)
── Estado ──
local partida: {"nivel":3,"record":18}
```

#### Solución
```typescript
interface Partida { nivel: number; record: number }

function esPartida(x: unknown): x is Partida {
  return typeof x === 'object' && x !== null && 'nivel' in x && typeof x.nivel === 'number' && 'record' in x && typeof x.record === 'number';
}

function cargar(): Partida {
  try {
    const leido: unknown = JSON.parse(localStorage.getItem('partida') ?? 'null');
    return esPartida(leido) ? leido : { nivel: 1, record: 0 };
  } catch {
    return { nivel: 1, record: 0 };
  }
}

const guardar = (p: Partida) => localStorage.setItem('partida', JSON.stringify(p));

const primera = cargar();
console.log(`Arranca en el nivel ${primera.nivel} (récord ${primera.record})`);
guardar({ nivel: 3, record: 18 });
const segunda = cargar();
console.log(`Arranca en el nivel ${segunda.nivel} (récord ${segunda.record})`);
```

#### Al superarla
El juego no se cae con los garabatos del Eclipse: arranca una partida nueva. Nima juega hasta el nivel 3 y la partida queda guardada, sana.

#### Imagen
- Una placa de memoria de latón con garabatos de sombra encima y una placa nueva, limpia, al lado.
- Un esqueleto de alambre chiquito dibujando garabatos con carbón.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) guarda la placa limpia; Rigel (chico flaco con pecas, antiparras de latón) borra los garabatos; Gheco persigue al esqueleto.

### Micro-misión S05-N04-P4 · La barra de vida

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Fuelle, el Eclipse de Hierro
carta: Trampa 4 | el ancho de la barra sale de la vida · `${vida / vidaMax * 100}%` · la barra nunca miente
recompensa: xp 15, monedas 3
```

#### Escena
Arriba de la cúpula, una barra de latón muestra cuánta vida le queda al Eclipse. El Eclipse intenta taparla, pero la barra se calcula siempre de la vida.

#### Gheco sugiere
El ancho de la barra es el porcentaje de vida: `vida / vidaMax * 100`, con `%`. Cada golpe la actualiza.

#### Desafío
Completá el ancho de la barra.

#### Pasos
1. Buscá el `___` en `pintar`.
2. Cambialo por ``barra.style.width = `${(eclipse.vida / eclipse.vidaMax) * 100}%`;``.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: Georgia, serif; background: #0b1326; color: #e8d9b0; padding: 20px; }
  #marco { width: 200px; height: 14px; border: 2px solid #8d6e3f; background: #2a1d0b; }
  #barra { height: 100%; width: 100%; background: #e57373; }
  button { margin-top: 10px; padding: 6px 12px; background: #8d6e3f; color: #fff7e0; border: 0; border-radius: 6px; }
</style>
<p id="fase"></p>
<div id="marco"><div id="barra"></div></div>
<button id="golpe">Fuelle muerde</button>
```

#### Eventos
```
click #golpe
click #golpe
click #golpe
```

#### Estado
```
#fase
estilo #barra { width }
```

#### Código inicial
```typescript
type Fase = 'entero' | 'agrietado' | 'roto';

class Eclipse {
  readonly vidaMax = 80;
  vida = 80;
  get fase(): Fase {
    return this.vida < 20 ? 'roto' : this.vida < 48 ? 'agrietado' : 'entero';
  }
  recibir(golpe: number): void {
    this.vida = Math.max(0, this.vida - golpe);
  }
}

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const eclipse = new Eclipse();
const barra = obtenerElemento<HTMLDivElement>('#barra');
const fase = obtenerElemento<HTMLParagraphElement>('#fase');

function pintar(): void {
  fase.textContent = `El Eclipse está ${eclipse.fase}`;
  ___
}

obtenerElemento<HTMLButtonElement>('#golpe').addEventListener('click', () => {
  eclipse.recibir(20);
  pintar();
});
pintar();
```

#### Salida esperada
```
── Estado ──
#fase: El Eclipse está agrietado
estilo #barra { width }: 50px
```

#### Solución
```typescript
type Fase = 'entero' | 'agrietado' | 'roto';

class Eclipse {
  readonly vidaMax = 80;
  vida = 80;
  get fase(): Fase {
    return this.vida < 20 ? 'roto' : this.vida < 48 ? 'agrietado' : 'entero';
  }
  recibir(golpe: number): void {
    this.vida = Math.max(0, this.vida - golpe);
  }
}

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const eclipse = new Eclipse();
const barra = obtenerElemento<HTMLDivElement>('#barra');
const fase = obtenerElemento<HTMLParagraphElement>('#fase');

function pintar(): void {
  fase.textContent = `El Eclipse está ${eclipse.fase}`;
  barra.style.width = `${(eclipse.vida / eclipse.vidaMax) * 100}%`;
}

obtenerElemento<HTMLButtonElement>('#golpe').addEventListener('click', () => {
  eclipse.recibir(20);
  pintar();
});
pintar();
```

#### Al superarla
Tres mordidas de Fuelle y la barra queda en un cuarto. El Eclipse, agrietado, tiembla en el techo de la cúpula.

#### Imagen
- Una barra de vida de latón en lo alto de la cúpula, casi vacía, con luz roja.
- Fuelle (zorro mecánico de latón con cola de engranajes) mordiendo el borde del disco de hierro.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) aprieta un botón grande; Gheco anima a Fuelle con banderitas.

### Micro-misión S05-N04-P5 · Jefe: el Planisferio Vivo

```meta
lugar: La cúpula del Planisferio
personajes: Rigel, Gheco, Nima, Fuelle, Astrea, el Eclipse de Hierro
carta: El juego completo | el héroe avanza · Fuelle lo sigue · cada contacto le saca vida al Eclipse con espera · al llegar a 0, chispas y victoria
recompensa: xp 50, oro 50, monedas 1
```

#### Escena
La pelea final. El Eclipse baja hasta el borde derecho del lienzo. El héroe corre hacia él con Fuelle detrás y se planta contra el disco: mientras lo toca, le saca vida, con un respiro entre golpe y golpe. Cuando el Eclipse llega a 0, estalla en chispas y el juego dice **¡Victoria!**

#### Gheco sugiere
Junta toda la Senda. Falta la regla de la victoria: cuando la vida del Eclipse llega a 0, el estado pasa a `'victoria'` y se lanzan chispas desde su centro.

#### Desafío
Completá la regla de la victoria.

#### Pasos
1. Buscá el `___` en `cuadro`.
2. Cambialo por `if (eclipse.vida === 0) { estado = 'victoria'; lanzarChispas(eclipse.x + 10, eclipse.y + 10); }`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f2c14e; font-family: monospace; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1326; border: 6px solid #8d6e3f; }
</style>
<p id="estado"></p>
<canvas id="lienzo" width="240" height="160"></canvas>
```

#### Eventos
```
apretar ArrowRight
cuadros 150
soltar ArrowRight
cuadros 5
```

#### Estado
```
#estado
lienzo
```

#### Código inicial
```typescript
interface Caja { x: number; y: number; lado: number }
interface Chispa { x: number; y: number; vx: number; vy: number; vida: number }
type Estado = 'peleando' | 'victoria';
type Fase = 'entero' | 'agrietado' | 'roto';

abstract class Enemigo implements Caja {
  constructor(public x: number, public y: number, public lado: number, public vida: number) {}
  recibir(golpe: number): void {
    this.vida = Math.max(0, this.vida - golpe);
  }
}

class Eclipse extends Enemigo {
  get fase(): Fase {
    return this.vida < 10 ? 'roto' : this.vida < 20 ? 'agrietado' : 'entero';
  }
}

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}
const chocan = (a: Caja, b: Caja) => a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;

const ctx = obtenerElemento<HTMLCanvasElement>('#lienzo').getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;
const cartel = obtenerElemento<HTMLParagraphElement>('#estado');

const heroe: Caja = { x: 10, y: 74, lado: 12 };
const fuelle = { x: 0, y: 78, lado: 8 };
const eclipse = new Eclipse(208, 70, 20, 30);
let chispas: Chispa[] = [];
let estado: Estado = 'peleando';
let respiro = 0;

function lanzarChispas(x: number, y: number): void {
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2;
    chispas.push({ x, y, vx: Math.cos(a) * 80, vy: Math.sin(a) * 80 - 40, vida: 0.6 });
  }
}

const teclas = new Set<string>();
addEventListener('keydown', (e: KeyboardEvent) => teclas.add(e.key));
addEventListener('keyup', (e: KeyboardEvent) => teclas.delete(e.key));

let antes: number | null = null;
function cuadro(ahora: number): void {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (estado === 'peleando') {
    if (teclas.has('ArrowRight')) heroe.x = Math.min(heroe.x + 120 * dt, eclipse.x - heroe.lado + 2);
    fuelle.x += (heroe.x - 16 - fuelle.x) * 0.1;
    respiro -= dt;
    if (chocan(heroe, eclipse) && respiro <= 0) {
      eclipse.recibir(10);
      respiro = 0.3;
    }
    ___
  }
  for (const c of chispas) {
    c.vy += 200 * dt;
    c.x += c.vx * dt;
    c.y += c.vy * dt;
    c.vida -= dt;
  }
  chispas = chispas.filter((c) => c.vida > 0);
  cartel.textContent = estado === 'victoria' ? '¡Victoria! El Planisferio brilla' : `El Eclipse está ${eclipse.fase} (${eclipse.vida})`;

  pincel.clearRect(0, 0, 240, 160);
  if (estado === 'peleando') {
    pincel.fillStyle = '#5d6470';
    pincel.fillRect(eclipse.x, eclipse.y, eclipse.lado, eclipse.lado);
  }
  pincel.fillStyle = '#ffd54f';
  for (const c of chispas) pincel.fillRect(Math.round(c.x), Math.round(c.y), 2, 2);
  pincel.fillStyle = '#b0855a';
  pincel.fillRect(Math.round(fuelle.x), fuelle.y, fuelle.lado, fuelle.lado);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(Math.round(heroe.x), heroe.y, heroe.lado, heroe.lado);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#estado: ¡Victoria! El Planisferio brilla
lienzo: clearRect(0, 0, 240, 160)
lienzo: fillRect(249, 80, 2, 2) #ffd54f
lienzo: fillRect(245, 95, 2, 2) #ffd54f
lienzo: fillRect(233, 107, 2, 2) #ffd54f
lienzo: fillRect(218, 111, 2, 2) #ffd54f
lienzo: fillRect(203, 107, 2, 2) #ffd54f
lienzo: fillRect(191, 95, 2, 2) #ffd54f
lienzo: fillRect(187, 80, 2, 2) #ffd54f
lienzo: fillRect(191, 65, 2, 2) #ffd54f
lienzo: fillRect(203, 53, 2, 2) #ffd54f
lienzo: fillRect(218, 49, 2, 2) #ffd54f
lienzo: fillRect(233, 53, 2, 2) #ffd54f
lienzo: fillRect(245, 65, 2, 2) #ffd54f
lienzo: fillRect(182, 78, 8, 8) #b0855a
lienzo: fillRect(198, 74, 12, 12) #f2c14e
```

#### Solución
```typescript
interface Caja { x: number; y: number; lado: number }
interface Chispa { x: number; y: number; vx: number; vy: number; vida: number }
type Estado = 'peleando' | 'victoria';
type Fase = 'entero' | 'agrietado' | 'roto';

abstract class Enemigo implements Caja {
  constructor(public x: number, public y: number, public lado: number, public vida: number) {}
  recibir(golpe: number): void {
    this.vida = Math.max(0, this.vida - golpe);
  }
}

class Eclipse extends Enemigo {
  get fase(): Fase {
    return this.vida < 10 ? 'roto' : this.vida < 20 ? 'agrietado' : 'entero';
  }
}

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}
const chocan = (a: Caja, b: Caja) => a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;

const ctx = obtenerElemento<HTMLCanvasElement>('#lienzo').getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;
const cartel = obtenerElemento<HTMLParagraphElement>('#estado');

const heroe: Caja = { x: 10, y: 74, lado: 12 };
const fuelle = { x: 0, y: 78, lado: 8 };
const eclipse = new Eclipse(208, 70, 20, 30);
let chispas: Chispa[] = [];
let estado: Estado = 'peleando';
let respiro = 0;

function lanzarChispas(x: number, y: number): void {
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2;
    chispas.push({ x, y, vx: Math.cos(a) * 80, vy: Math.sin(a) * 80 - 40, vida: 0.6 });
  }
}

const teclas = new Set<string>();
addEventListener('keydown', (e: KeyboardEvent) => teclas.add(e.key));
addEventListener('keyup', (e: KeyboardEvent) => teclas.delete(e.key));

let antes: number | null = null;
function cuadro(ahora: number): void {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (estado === 'peleando') {
    if (teclas.has('ArrowRight')) heroe.x = Math.min(heroe.x + 120 * dt, eclipse.x - heroe.lado + 2);
    fuelle.x += (heroe.x - 16 - fuelle.x) * 0.1;
    respiro -= dt;
    if (chocan(heroe, eclipse) && respiro <= 0) {
      eclipse.recibir(10);
      respiro = 0.3;
    }
    if (eclipse.vida === 0) { estado = 'victoria'; lanzarChispas(eclipse.x + 10, eclipse.y + 10); }
  }
  for (const c of chispas) {
    c.vy += 200 * dt;
    c.x += c.vx * dt;
    c.y += c.vy * dt;
    c.vida -= dt;
  }
  chispas = chispas.filter((c) => c.vida > 0);
  cartel.textContent = estado === 'victoria' ? '¡Victoria! El Planisferio brilla' : `El Eclipse está ${eclipse.fase} (${eclipse.vida})`;

  pincel.clearRect(0, 0, 240, 160);
  if (estado === 'peleando') {
    pincel.fillStyle = '#5d6470';
    pincel.fillRect(eclipse.x, eclipse.y, eclipse.lado, eclipse.lado);
  }
  pincel.fillStyle = '#ffd54f';
  for (const c of chispas) pincel.fillRect(Math.round(c.x), Math.round(c.y), 2, 2);
  pincel.fillStyle = '#b0855a';
  pincel.fillRect(Math.round(fuelle.x), fuelle.y, fuelle.lado, fuelle.lado);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(Math.round(heroe.x), heroe.y, heroe.lado, heroe.lado);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
Al tercer golpe, el Eclipse de Hierro estalla en una lluvia de chispas doradas. En la cúpula de verdad, el disco viejo deja de girar y se acomoda despacio en su lugar, en el borde del Planisferio, donde el Vidriero lo había puesto. Las constelaciones vuelven a brillar.

Los chicos de la Feria gritan y aplauden. Fuelle da tres vueltas persiguiéndose la cola. Astrea baja volando con una corona chiquita de latón, con una estrella en el medio: **la Corona del Planisferio**. Se la pone a Rigel, que se pone colorado, y después a Nima, y después a Fuelle, y al final a Gheco, que no se la quiere sacar nunca más.

Desde ese domingo, el **Planisferio Vivo** queda abierto para todos.

#### Imagen
- La cúpula del Planisferio con las constelaciones brillando otra vez y un disco de hierro quieto en el borde, con una lluvia de chispas doradas.
- Una multitud de chicos y chicas de la Feria con ropa de abrigo, aplaudiendo.
- Astrea (lechuza con anteojos de latón y chaleco azul) vuela con una corona chiquita de latón; Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) colorado; Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas, arco verde) se ríe; Fuelle (zorro mecánico de latón con cola de engranajes) da vueltas; Gheco con la corona puesta.
