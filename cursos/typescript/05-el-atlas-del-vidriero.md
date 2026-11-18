# RAMA R05 · El Atlas del Vidriero: el mismo juego, ahora medido

```meta
tipo: tronco
posicion: 5
```

## R05-N01 · JavaScript contra TypeScript

```meta
tipo: tema
padre: R04-N09
precio: 10
criatura: goblin
temas: js.typescript, cal.tipos, cal.depuracion
```

### Crónica

En lo más alto de la Cúpula, detrás de una puerta que nunca se abría, Rigel encuentra el taller del Vidriero. En el centro hay un libro enorme encuadernado en latón: **el Atlas del Vidriero**. En la primera página, el Vidriero escribió el mismo programa dos veces, una al lado de la otra: a la izquierda, en la lengua de la Feria; a la derecha, en la del Mirador. Abajo, una nota: *los mismos tres errores. Mirá cuándo aparece cada uno.*

—Esto lo escribió para quien llegara hasta acá —dice {mentor}—. Para que entiendas, de una vez, para qué sirvió todo lo que mediste.

### Objetivos

- Ver el mismo programa con los mismos tres errores en JavaScript y en TypeScript, y cuándo aparece cada uno.
- Arreglar los tres errores clásicos: un nombre mal escrito, un dato que falta y un valor que puede no estar.
- Saber cómo se pasa un proyecto de JavaScript a TypeScript de a poco.

### Antes de empezar

- Todo el Mirador (R01 a R04).

### Explicación

#### Los tres errores del Atlas
| Error | En JavaScript | En TypeScript |
|---|---|---|
| un nombre mal escrito (`poderAtake` en vez de `poderAtaque`) | corre y da `NaN`, sin avisar | no compila: `TS2551`, y sugiere el nombre correcto |
| un dato que falta (`experiencia` sin valor inicial) | corre y da `NaN` | no compila: `TS2741`, falta la propiedad |
| un valor que puede no estar (`buscarEnemigo` no encuentra nada) | explota recién al llegar a esa línea | no compila: `TS18048`, posiblemente `undefined` |

En JavaScript, los tres errores aparecen **jugando** (o no aparecen nunca y el juego hace cualquier cosa). En TypeScript, aparecen **escribiendo**.

#### Pasar un proyecto de JavaScript a TypeScript
No hace falta reescribir todo de una vez. Un camino habitual:
1. Agregar TypeScript al proyecto (`npm install -D typescript`, `npx tsc --init`) con `"allowJs": true`: los `.js` siguen funcionando junto a los `.ts`.
2. Prender `"checkJs": true` (o poner `// @ts-check` arriba de un `.js`): TypeScript revisa también los `.js`, usando lo que pueda deducir y los comentarios JSDoc (`/** @param {number} x */`).
3. Renombrar los archivos de a uno a `.ts` y anotar los tipos, empezando por los datos (las `interface`).
4. Cuando no quede ningún `.js`, sacar `allowJs`.

> El paso 2 no está en el material de base (FullCursos): se agregó porque es como se migran los proyectos de verdad.

### Código de ejemplo

```typescript
interface Personaje {
  nombre: string;
  vida: number;
  poderAtaque: number;
  experiencia: number;
}

function crearHeroe(nombre: string): Personaje {
  return { nombre, vida: 100, poderAtaque: 12, experiencia: 0 };
}

function calcularDanio(p: Personaje, multiplicador: number): number {
  return p.poderAtaque * multiplicador;
}

const enemigos: Personaje[] = [crearHeroe('Goblin')];
function buscarEnemigo(nombre: string): Personaje | undefined {
  return enemigos.find((e) => e.nombre === nombre);
}

const rigel = crearHeroe('Rigel');
rigel.experiencia += 50;
const dragon = buscarEnemigo('Dragón');
console.log(calcularDanio(rigel, 2), rigel.experiencia, dragon?.vida ?? 'no hay dragón');
```

### Salida esperada

```
24 50 no hay dragón
```

### ¿Para qué sirve?

Para entender, con un ejemplo, qué se gana con TypeScript: los errores más comunes de JavaScript aparecen antes de ejecutar, con el lugar exacto y, muchas veces, con la solución sugerida. Y para saber cómo empezar a usarlo en un proyecto que ya existe.

### Errores habituales

**Esqueleto: el nombre mal escrito (TS2551).** *La propiedad "poderAtake" no existe en el tipo "Personaje". ¿Quería decir "poderAtaque"?* (Si el nombre no se parece a ninguno, el error es `TS2339`, sin sugerencia.)

**Esqueleto: el dato que falta (TS2741).** El objeto que devuelve `crearHeroe` tiene que tener todo lo que pide `Personaje`.

**Orco: lo que puede no estar (TS18048).** `find` puede no encontrar nada: preguntá o usá `?.`.

### Micro-misión R05-N01-P1 · El nombre mal escrito

```meta
lugar: El taller del Vidriero
personajes: Rigel, Gheco, Astrea
criatura: skeleton
carta: Error 1 del Atlas | en JS: NaN sin aviso · en TS: TS2551 y la sugerencia · usá el nombre de la interface
recompensa: xp 10, oro 10
```

#### Escena
Rigel copia la primera página del Atlas en TypeScript. El compilador frena enseguida en el cálculo del daño, y hasta sugiere la solución.

#### Gheco sugiere
En JavaScript, `p.poderAtake` daría `undefined`, y `undefined * 2` da `NaN`: el programa seguiría como si nada. En TypeScript, la `interface` dice que la propiedad se llama `poderAtaque`, y el compilador lo avisa (`TS2551`) con la sugerencia.

#### Desafío
Corregí el nombre de la propiedad.

#### Pasos
1. Tocá **Ejecutar** y leé el error: sugiere el nombre correcto.
2. Cambiá `p.poderAtake` por `p.poderAtaque`.
3. Tocá **Ejecutar**. Tiene que salir `Daño: 24`.

#### Código inicial
```typescript
interface Personaje {
  nombre: string;
  poderAtaque: number;
}

function calcularDanio(p: Personaje, multiplicador: number): number {
  return p.poderAtake * multiplicador;
}

console.log(`Daño: ${calcularDanio({ nombre: 'Rigel', poderAtaque: 12 }, 2)}`);
```

#### Salida esperada
```
Daño: 24
```

#### Solución
```typescript
interface Personaje {
  nombre: string;
  poderAtaque: number;
}

function calcularDanio(p: Personaje, multiplicador: number): number {
  return p.poderAtaque * multiplicador;
}

console.log(`Daño: ${calcularDanio({ nombre: 'Rigel', poderAtaque: 12 }, 2)}`);
```

#### Al superarla
En el margen del Atlas, al lado del error, aparece una marca de tinta: *visto antes de jugar*.

#### Imagen
- Un libro enorme encuadernado en latón abierto sobre un atril, con dos columnas de escritura y una marca de tinta en el margen (sin texto legible).
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco de cuero marrón cerrado) escribe en una libreta.
- Astrea (lechuza grande gris azulada con anteojos de latón y chaleco azul) mira por encima; Gheco sobre el atril.

### Micro-misión R05-N01-P2 · El dato que falta

```meta
lugar: El taller del Vidriero
personajes: Rigel, Gheco
criatura: skeleton
carta: Error 2 del Atlas | en JS: el dato sin valor da NaN · en TS: TS2741, falta la propiedad · la interface obliga a darla
recompensa: xp 10, oro 10
```

#### Escena
La segunda página del Atlas: el héroe se crea sin experiencia, y después se le suma. En JavaScript daba `NaN`.

#### Gheco sugiere
La `interface` pide `experiencia`. Si `crearHeroe` devuelve un objeto sin ella, el compilador avisa (`TS2741`). En JavaScript, la suma `undefined + 50` daba `NaN`.

#### Desafío
Agregá la experiencia inicial al héroe.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el objeto de `crearHeroe`, agregá `, experiencia: 0`.
3. Tocá **Ejecutar**. Tiene que salir `Rigel tiene 50 de experiencia`.

#### Código inicial
```typescript
interface Personaje {
  nombre: string;
  vida: number;
  experiencia: number;
}

function crearHeroe(nombre: string): Personaje {
  return { nombre, vida: 100 };
}

const rigel = crearHeroe('Rigel');
rigel.experiencia += 50;
console.log(`${rigel.nombre} tiene ${rigel.experiencia} de experiencia`);
```

#### Salida esperada
```
Rigel tiene 50 de experiencia
```

#### Solución
```typescript
interface Personaje {
  nombre: string;
  vida: number;
  experiencia: number;
}

function crearHeroe(nombre: string): Personaje {
  return { nombre, vida: 100, experiencia: 0 };
}

const rigel = crearHeroe('Rigel');
rigel.experiencia += 50;
console.log(`${rigel.nombre} tiene ${rigel.experiencia} de experiencia`);
```

#### Al superarla
Otra marca en el margen del Atlas. El Vidriero había dibujado al lado un `NaN` tachado.

#### Imagen
- Una página del Atlas con un símbolo tachado dibujado en el margen.
- Rigel (chico flaco con pecas, antiparras de latón) completa una ficha con la pluma.
- Gheco señalando el dibujo.

### Micro-misión R05-N01-P3 · El dragón que no estaba

```meta
lugar: El taller del Vidriero
personajes: Rigel, Gheco
criatura: orc
carta: Error 3 del Atlas | en JS: explota recién al llegar · en TS: TS18048 antes de ejecutar · preguntá o ?.
recompensa: xp 10, oro 10
```

#### Escena
La tercera página: el programa busca un dragón que no está en la lista. En JavaScript, explotaba en medio del juego.

#### Gheco sugiere
`buscarEnemigo` devuelve `Personaje | undefined`. Usar `dragon.vida` sin preguntar da `TS18048`. Con `?.` y `??` se da un valor si no está.

#### Desafío
Protegé la línea con `?.` y `??`.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `dragon.vida` por `dragon?.vida ?? 'no hay dragón'`.
3. Tocá **Ejecutar**. Tiene que salir `Vida del dragón: no hay dragón`.

#### Código inicial
```typescript
interface Personaje {
  nombre: string;
  vida: number;
}

const enemigos: Personaje[] = [{ nombre: 'Goblin', vida: 20 }];

function buscarEnemigo(nombre: string): Personaje | undefined {
  return enemigos.find((e) => e.nombre === nombre);
}

const dragon = buscarEnemigo('Dragón');
console.log(`Vida del dragón: ${dragon.vida}`);
```

#### Salida esperada
```
Vida del dragón: no hay dragón
```

#### Solución
```typescript
interface Personaje {
  nombre: string;
  vida: number;
}

const enemigos: Personaje[] = [{ nombre: 'Goblin', vida: 20 }];

function buscarEnemigo(nombre: string): Personaje | undefined {
  return enemigos.find((e) => e.nombre === nombre);
}

const dragon = buscarEnemigo('Dragón');
console.log(`Vida del dragón: ${dragon?.vida ?? 'no hay dragón'}`);
```

#### Al superarla
La tercera marca. Abajo de todo, el Vidriero escribió: *los tres, antes de jugar*.

#### Imagen
- La página del Atlas con tres marcas de tinta alineadas en el margen y una frase al pie (sin letras legibles).
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sonríe.
- Gheco hace la cuenta con tres dedos.

### Micro-misión R05-N01-P4 · Los tres a la vez

```meta
lugar: El taller del Vidriero
personajes: Rigel, Gheco, Astrea
criatura: goblin
carta: Hacer que el compilador los encuentre | micro-misión de tipo Compilador · dale tipos al JS y mirá los errores · TS2551 y TS18048
recompensa: xp 10, oro 10
```

#### Escena
Astrea le pide a Rigel una prueba: tomar el programa de la izquierda del Atlas (el de JavaScript, sin tipos), darle tipos, y ver con sus propios ojos qué encuentra el compilador.

#### Gheco sugiere
Esta micro-misión es de tipo **Compilador**: no se ejecuta, se comparan los errores. El código no tiene tipos, así que el compilador no puede encontrar nada (solo avisa que los parámetros no tienen tipo).

Cuando le des los tipos, va a encontrar los dos errores escondidos: el nombre mal escrito (`TS2551`, línea 7) y el valor que puede no estar (`TS18048`, línea 13).

#### Desafío
Anotá los parámetros con `Personaje` y `string`.

#### Pasos
1. Cambiá `function calcularDanio(p, multiplicador)` por `function calcularDanio(p: Personaje, multiplicador: number)`.
2. Cambiá `function buscarEnemigo(nombre)` por `function buscarEnemigo(nombre: string)`.
3. Tocá **Ejecutar**. Tienen que salir `TS2551 en la línea 7` y `TS18048 en la línea 13`.

#### Compilador
sí

#### Código inicial
```typescript
interface Personaje {
  nombre: string;
  poderAtaque: number;
}

function calcularDanio(p, multiplicador) {
  return p.poderAtake * multiplicador;
}

const enemigos: Personaje[] = [{ nombre: 'Goblin', poderAtaque: 5 }];
function buscarEnemigo(nombre) {
  const e = enemigos.find((x) => x.nombre === nombre);
  return e.poderAtaque;
}
```

#### Salida esperada
```
TS2551 en la línea 7
TS18048 en la línea 13
```

#### Solución
```typescript
interface Personaje {
  nombre: string;
  poderAtaque: number;
}

function calcularDanio(p: Personaje, multiplicador: number) {
  return p.poderAtake * multiplicador;
}

const enemigos: Personaje[] = [{ nombre: 'Goblin', poderAtaque: 5 }];
function buscarEnemigo(nombre: string) {
  const e = enemigos.find((x) => x.nombre === nombre);
  return e.poderAtaque;
}
```

#### Al superarla
Con los tipos puestos, el compilador encuentra los dos errores que el código sin tipos escondía. Astrea asiente: —Eso es lo que da medir.

#### Imagen
- Dos hojas de papel lado a lado: una sin marcas y otra con dos errores marcados con círculos de luz (sin texto legible).
- Astrea (lechuza con anteojos de latón y chaleco azul) señala los círculos con el compás.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) asiente; Gheco sobre las hojas.

### Micro-misión R05-N01-P5 · Migrar de a poco

```meta
lugar: El taller del Vidriero
personajes: Rigel, Gheco
carta: Migrar | primero los datos (interface) · después las funciones · el compilador te guía por los errores
recompensa: xp 15, monedas 5
```

#### Escena
En el Atlas hay un programa de la Feria que el Vidriero nunca pasó a la lengua del Mirador: el marcador de un puesto de tiro. Rigel lo pasa, empezando por los datos.

#### Gheco sugiere
Para pasar un programa de JavaScript a TypeScript, conviene empezar por los **datos**: escribir la `interface` y anotar con ella las funciones. Después, el compilador va marcando lo que falta.

#### Desafío
Completá la `interface` del tiro y anotá el parámetro de `puntos`.

#### Pasos
1. En la `interface`, el `___` es `jugador: string; distancia: number;`.
2. En `puntos(t)`, cambiá `t` por `t: Tiro` y agregá `: number` después de los paréntesis.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Tiro {
  ___
}

function puntos(t) {
  if (t.distancia <= 5) return 10;
  if (t.distancia <= 15) return 5;
  return 1;
}

const tiros: Tiro[] = [
  { jugador: 'Nima', distancia: 3 },
  { jugador: 'Rigel', distancia: 12 },
  { jugador: 'Gheco', distancia: 40 },
];
for (const t of tiros) console.log(`${t.jugador}: ${puntos(t)}`);
```

#### Salida esperada
```
Nima: 10
Rigel: 5
Gheco: 1
```

#### Solución
```typescript
interface Tiro {
  jugador: string; distancia: number;
}

function puntos(t: Tiro): number {
  if (t.distancia <= 5) return 10;
  if (t.distancia <= 15) return 5;
  return 1;
}

const tiros: Tiro[] = [
  { jugador: 'Nima', distancia: 3 },
  { jugador: 'Rigel', distancia: 12 },
  { jugador: 'Gheco', distancia: 40 },
];
for (const t of tiros) console.log(`${t.jugador}: ${puntos(t)}`);
```

#### Al superarla
El marcador de la Feria queda escrito en la lengua del Mirador. Rigel le guarda una copia a Nima.

#### Imagen
- Una página del Atlas con un dibujo de un puesto de tiro de feria y un marcador, a la derecha una versión prolija con fichas técnicas.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) copia con la pluma.
- Gheco con una flechita de juguete.

### Micro-misión R05-N01-P6 · Revisar sin renombrar

```meta
lugar: El taller del Vidriero
personajes: Rigel, Gheco, Astrea
carta: Revisar un .js | checkJs revisa los .js con lo que deduce y con JSDoc · un .js con su .d.ts se usa con tipos · paso a paso
recompensa: xp 15, monedas 5
```

#### Escena
Algunos programas del Vidriero son muy grandes para pasarlos de una vez. Astrea le muestra a Rigel cómo usar uno tal como está, en JavaScript, describiéndolo con una etiqueta.

#### Gheco sugiere
En el tablero está `marcador.js` (el código viejo, sin tipos) y `marcador.d.ts` (su descripción). Así el programa viejo se usa desde TypeScript sin reescribirlo: el compilador revisa cada llamada contra el `.d.ts`.

En un proyecto, `"allowJs": true` y `"checkJs": true` hacen algo parecido con todos los `.js`.

#### Desafío
Completá la llamada con un número (el compilador revisa contra el `.d.ts`).

#### Pasos
1. Tocá **Ejecutar** y leé el error: `sumar` pide un número.
2. Cambiá `marcador.sumar('diez')` por `marcador.sumar(10)`.
3. Tocá **Ejecutar**. Tiene que salir `Total: 15`.

#### Archivos
marcador.js
```javascript
export function crearMarcador() {
  let total = 0;
  return {
    sumar(puntos) {
      total += puntos;
    },
    get total() {
      return total;
    },
  };
}
```

marcador.d.ts
```typescript
export interface Marcador {
  sumar(puntos: number): void;
  readonly total: number;
}
export function crearMarcador(): Marcador;
```

#### Código inicial
```typescript
import { crearMarcador } from './marcador.js';

const marcador = crearMarcador();
marcador.sumar(5);
marcador.sumar('diez');
console.log(`Total: ${marcador.total}`);
```

#### Salida esperada
```
Total: 15
```

#### Solución
```typescript
import { crearMarcador } from './marcador.js';

const marcador = crearMarcador();
marcador.sumar(5);
marcador.sumar(10);
console.log(`Total: ${marcador.total}`);
```

#### Al superarla
El marcador viejo funciona con la etiqueta nueva. Astrea le da a Rigel una **estrella de latón**: —No hace falta tirar lo viejo para medirlo.

#### Imagen
- Un marcador mecánico viejo de la Feria, con una etiqueta de cartulina nueva atada con hilo.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) ajusta la etiqueta; Gheco sobre el marcador.

## R05-N02 · El modelo tipado del juego

```meta
tipo: tema
padre: R05-N01
precio: 10
criatura: dragon
temas: poo.clases, poo.herencia, poo.genericos, cal.tipos
```

### Crónica

En la segunda parte del Atlas, el Vidriero dejó los planos de un juego: *Junta las Gemas*, el mismo que Nima jugaba en la Feria. Pero estos planos son distintos: cada pieza tiene su ficha, sus medidas, sus reglas. Antes de construir el juego, el Vidriero midió **el modelo**: qué es un héroe, qué es un goblin, qué es una gema.

—Primero el modelo —dice {mentor}—. Si el modelo está bien medido, el juego se arma solo.

### Objetivos

- Armar el modelo de un juego con todo lo del curso: `interface`, clases, `abstract`, uniones discriminadas y genéricos.
- Usar una `interface` (`Posicionable`) que cumplen cosas distintas.
- Usar un genérico con restricción que conserva el tipo (`entidadesVivas<T extends Entidad>`).

### Antes de empezar

- R02 (clases, herencia y genéricos) y R03 (uniones discriminadas).

### Explicación

#### Las piezas del modelo
```typescript
interface Posicionable { x: number; y: number }

class Vec2 implements Posicionable { … }        // una posición con métodos

abstract class Entidad {                         // lo común a todos los que viven y pelean
  protected vida: number;
  constructor(public readonly nombre: string, public posicion: Vec2, protected readonly vidaMaxima: number) {
    this.vida = vidaMaxima;
  }
  abstract describir(): string;
}

class Heroe extends Entidad { … }
class Goblin extends Entidad { … }

type TipoGoblin =
  | { variante: 'normal'; vidaBase: 15 }
  | { variante: 'fuerte'; vidaBase: 30 };

interface Gema extends Posicionable { recolectada: boolean }
```

Una `Gema` no es una clase: es un objeto con `x`, `y` y `recolectada`. Igual cumple `Posicionable`, y por eso `Vec2.distanciaA` acepta una gema.

#### Un genérico que conserva el tipo
```typescript
function entidadesVivas<T extends Entidad>(entidades: T[]): T[] {
  return entidades.filter((e) => e.estaVivo());
}
```

Si le pasás `Goblin[]`, devuelve `Goblin[]` (no `Entidad[]`): podés seguir usando lo propio de los goblins.

### Código de ejemplo

```typescript
interface Posicionable {
  x: number;
  y: number;
}

class Vec2 implements Posicionable {
  constructor(public x: number = 0, public y: number = 0) {}
  distanciaA(otro: Posicionable): number {
    return Math.hypot(this.x - otro.x, this.y - otro.y);
  }
}

interface Gema extends Posicionable {
  recolectada: boolean;
}

const rigel = new Vec2(0, 0);
const gemas: Gema[] = [{ x: 3, y: 4, recolectada: false }, { x: 6, y: 8, recolectada: true }];
for (const g of gemas) console.log(rigel.distanciaA(g), g.recolectada);
```

### Salida esperada

```
5 false
10 true
```

### ¿Para qué sirve?

En todo programa grande, lo primero es el **modelo**: qué cosas existen y cómo son. En TypeScript, el modelo es código que el compilador revisa: si cambia una pieza, avisa en todos los lugares que la usan. Así se puede cambiar el juego sin miedo.

### Errores habituales

**Ogro: crear una Entidad (TS2511).** Es `abstract`: se crean héroes y goblins.

**Esqueleto: una variante que no existe (TS2322).** `{ variante: 'gigante', vidaBase: 50 }` no es un `TipoGoblin`.

**Ogro: tocar la vida desde afuera (TS2445).** `vida` es `protected`: se lee con `vidaActual` y se cambia con `recibirDanio`.

### Micro-misión R05-N02-P1 · Lo que tiene posición

```meta
lugar: El taller del Vidriero
personajes: Rigel, Gheco
carta: implements | class Vec2 implements Posicionable · cualquier cosa con x e y cumple Posicionable · distanciaA acepta una gema
recompensa: xp 10, oro 10
```

#### Escena
La primera ficha del modelo: todo lo que está en el mapa tiene posición. Rigel completa la clase de las posiciones.

#### Gheco sugiere
`Vec2 implements Posicionable` promete tener `x` e `y`. Y `distanciaA(otro: Posicionable)` acepta **cualquier** cosa con `x` e `y`: otro `Vec2`, una gema, lo que sea.

`Math.hypot(dx, dy)` es la distancia en línea recta.

#### Desafío
Completá el `return` de `distanciaA`.

#### Pasos
1. Buscá el `___` en `distanciaA`.
2. Cambialo por `Math.hypot(this.x - otro.x, this.y - otro.y)`.
3. Tocá **Ejecutar**. Tiene que salir `Distancia a la gema: 5`.

#### Código inicial
```typescript
interface Posicionable {
  x: number;
  y: number;
}

class Vec2 implements Posicionable {
  constructor(public x: number = 0, public y: number = 0) {}

  distanciaA(otro: Posicionable): number {
    return ___;
  }
}

const rigel = new Vec2(0, 0);
console.log(`Distancia a la gema: ${rigel.distanciaA({ x: 3, y: 4 })}`);
```

#### Salida esperada
```
Distancia a la gema: 5
```

#### Solución
```typescript
interface Posicionable {
  x: number;
  y: number;
}

class Vec2 implements Posicionable {
  constructor(public x: number = 0, public y: number = 0) {}

  distanciaA(otro: Posicionable): number {
    return Math.hypot(this.x - otro.x, this.y - otro.y);
  }
}

const rigel = new Vec2(0, 0);
console.log(`Distancia a la gema: ${rigel.distanciaA({ x: 3, y: 4 })}`);
```

#### Al superarla
En el plano del Atlas, una línea de luz une a Rigel con la primera gema: 5 pasos.

#### Imagen
- Un plano del Atlas con una cuadrícula, un punto para el héroe y una gema, unidos por una línea de luz.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) mide con el calibre.
- Gheco sobre el plano.

### Micro-misión R05-N02-P2 · Lo común a todos

```meta
lugar: El taller del Vidriero
personajes: Rigel, Gheco
carta: abstract Entidad | lo común en la clase abstracta · protected vida · cada uno completa describir()
recompensa: xp 10, oro 10
```

#### Escena
Héroes y goblins comparten mucho: nombre, posición, vida. El Vidriero lo puso todo en una ficha común, que no se usa sola.

#### Gheco sugiere
`Entidad` es `abstract`: tiene lo común (vida, recibir daño) y un hueco, `describir()`, que cada uno completa. `vida` es `protected`: la usan la clase y las que heredan.

#### Desafío
Completá el `describir()` del héroe.

#### Pasos
1. Buscá el `___` en la clase `Heroe`.
2. Cambialo por ``return `${this.nombre}: ${this.vida}/${this.vidaMaxima}`;``.
3. Tocá **Ejecutar**. Tiene que salir `Rigel: 70/100`.

#### Código inicial
```typescript
class Vec2 {
  constructor(public x: number = 0, public y: number = 0) {}
}

abstract class Entidad {
  protected vida: number;

  constructor(public readonly nombre: string, public posicion: Vec2, protected readonly vidaMaxima: number) {
    this.vida = vidaMaxima;
  }

  recibirDanio(cantidad: number): void {
    this.vida = Math.max(0, this.vida - cantidad);
  }

  abstract describir(): string;
}

class Heroe extends Entidad {
  constructor(posicion: Vec2) {
    super('Rigel', posicion, 100);
  }

  describir(): string {
    ___
  }
}

const rigel = new Heroe(new Vec2(0, 0));
rigel.recibirDanio(30);
console.log(rigel.describir());
```

#### Salida esperada
```
Rigel: 70/100
```

#### Solución
```typescript
class Vec2 {
  constructor(public x: number = 0, public y: number = 0) {}
}

abstract class Entidad {
  protected vida: number;

  constructor(public readonly nombre: string, public posicion: Vec2, protected readonly vidaMaxima: number) {
    this.vida = vidaMaxima;
  }

  recibirDanio(cantidad: number): void {
    this.vida = Math.max(0, this.vida - cantidad);
  }

  abstract describir(): string;
}

class Heroe extends Entidad {
  constructor(posicion: Vec2) {
    super('Rigel', posicion, 100);
  }

  describir(): string {
    return `${this.nombre}: ${this.vida}/${this.vidaMaxima}`;
  }
}

const rigel = new Heroe(new Vec2(0, 0));
rigel.recibirDanio(30);
console.log(rigel.describir());
```

#### Al superarla
La ficha del héroe queda completa en el Atlas, con su barra de vida dibujada.

#### Imagen
- Una ficha del Atlas con el dibujo de un héroe y una barra de vida a dos tercios.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) se mira en la ficha, divertido.
- Gheco dibujado en un rincón de la ficha.

### Micro-misión R05-N02-P3 · Las dos clases de goblin

```meta
lugar: El taller del Vidriero
personajes: Rigel, Gheco
criatura: goblin
carta: Variantes discriminadas | { variante: 'normal'; vidaBase: 15 } | { variante: 'fuerte'; vidaBase: 30 } · una que no existe es TS2322
recompensa: xp 10, oro 10
```

#### Escena
El Atlas describe dos clases de goblin: el normal y el fuerte. Un goblin se coló en los planos como *gigante*, que no existe.

#### Gheco sugiere
`TipoGoblin` es una unión discriminada por `variante`, y cada variante tiene su vida fija (`15` o `30`, como tipos literales). Una variante que no está, o una vida que no corresponde, da `TS2322`.

#### Desafío
Cambiá el goblin gigante por uno fuerte.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `{ variante: 'gigante', vidaBase: 50 }` por `{ variante: 'fuerte', vidaBase: 30 }`.
3. Tocá **Ejecutar**. Tiene que salir `Goblin normal: 15 · Goblin fuerte: 30`.

#### Código inicial
```typescript
type TipoGoblin =
  | { variante: 'normal'; vidaBase: 15 }
  | { variante: 'fuerte'; vidaBase: 30 };

const goblins: TipoGoblin[] = [
  { variante: 'normal', vidaBase: 15 },
  { variante: 'gigante', vidaBase: 50 },
];
console.log(goblins.map((g) => `Goblin ${g.variante}: ${g.vidaBase}`).join(' · '));
```

#### Salida esperada
```
Goblin normal: 15 · Goblin fuerte: 30
```

#### Solución
```typescript
type TipoGoblin =
  | { variante: 'normal'; vidaBase: 15 }
  | { variante: 'fuerte'; vidaBase: 30 };

const goblins: TipoGoblin[] = [
  { variante: 'normal', vidaBase: 15 },
  { variante: 'fuerte', vidaBase: 30 },
];
console.log(goblins.map((g) => `Goblin ${g.variante}: ${g.vidaBase}`).join(' · '));
```

#### Al superarla
El goblin gigante se encoge hasta su tamaño de verdad y se va refunfuñando del plano.

#### Imagen
- Una página del Atlas con dibujos de dos goblins, uno chico y uno fuerte, y un tercero encogiéndose.
- Un goblin chiquito con un engranaje en la espalda escapando de la página.
- Rigel (chico flaco con pecas, antiparras de latón) borra el dibujo del gigante; Gheco se ríe.

### Micro-misión R05-N02-P4 · Los que siguen en pie

```meta
lugar: El taller del Vidriero
personajes: Rigel, Gheco, Astrea
carta: Genérico que conserva el tipo | function entidadesVivas<T extends Entidad>(entidades: T[]): T[] · con Goblin[] devuelve Goblin[]
recompensa: xp 15, monedas 5
```

#### Escena
Después de cada pelea, el juego tiene que saber quiénes siguen en pie. Astrea quiere una sola máquina para héroes, goblins o todos juntos.

#### Gheco sugiere
Con un genérico con restricción, la función acepta cualquier lista de entidades y devuelve **el mismo tipo** de lista:

```ts
function entidadesVivas<T extends Entidad>(entidades: T[]): T[] {
  return entidades.filter((e) => e.estaVivo());
}
```

#### Desafío
Completá la firma genérica.

#### Pasos
1. Buscá el `___` en la firma de `entidadesVivas`.
2. Cambialo por `<T extends Entidad>(entidades: T[]): T[]`.
3. Tocá **Ejecutar**. Tiene que salir `En pie: Goblin fuerte`.

#### Código inicial
```typescript
abstract class Entidad {
  protected vida: number;
  constructor(public readonly nombre: string, vidaMaxima: number) {
    this.vida = vidaMaxima;
  }
  recibirDanio(cantidad: number): void {
    this.vida = Math.max(0, this.vida - cantidad);
  }
  estaVivo(): boolean {
    return this.vida > 0;
  }
}

class Goblin extends Entidad {}

function entidadesVivas___ {
  return entidades.filter((e) => e.estaVivo());
}

const goblins: Goblin[] = [new Goblin('Goblin normal', 15), new Goblin('Goblin fuerte', 30)];
for (const g of goblins) g.recibirDanio(20);
const enPie: Goblin[] = entidadesVivas(goblins);
console.log(`En pie: ${enPie.map((g) => g.nombre).join(', ')}`);
```

#### Salida esperada
```
En pie: Goblin fuerte
```

#### Solución
```typescript
abstract class Entidad {
  protected vida: number;
  constructor(public readonly nombre: string, vidaMaxima: number) {
    this.vida = vidaMaxima;
  }
  recibirDanio(cantidad: number): void {
    this.vida = Math.max(0, this.vida - cantidad);
  }
  estaVivo(): boolean {
    return this.vida > 0;
  }
}

class Goblin extends Entidad {}

function entidadesVivas<T extends Entidad>(entidades: T[]): T[] {
  return entidades.filter((e) => e.estaVivo());
}

const goblins: Goblin[] = [new Goblin('Goblin normal', 15), new Goblin('Goblin fuerte', 30)];
for (const g of goblins) g.recibirDanio(20);
const enPie: Goblin[] = entidadesVivas(goblins);
console.log(`En pie: ${enPie.map((g) => g.nombre).join(', ')}`);
```

#### Al superarla
En el Atlas, el goblin normal queda tachado y el fuerte sigue en pie. Astrea anota: *vencerlo cuesta dos golpes*.

#### Imagen
- Una página del Atlas con dos goblins dibujados, uno tachado y otro de pie.
- Astrea (lechuza con anteojos de latón y chaleco azul) anota con la pluma.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mira; Gheco señala al de pie.

### Micro-misión R05-N02-P5 · El modelo completo

```meta
lugar: El taller del Vidriero
personajes: Rigel, Gheco, Astrea
carta: Todo el modelo | Vec2 implements Posicionable · Entidad abstracta · Heroe y Goblin · TipoGoblin discriminado · Gema como interface
recompensa: xp 15, monedas 5
```

#### Escena
Rigel arma el modelo entero del Atlas y lo prueba: un héroe, dos goblins y dos gemas.

#### Gheco sugiere
Todo junto. El goblin recibe su `TipoGoblin` y arma su nombre y su vida a partir de él:

```ts
super(`Goblin ${tipo.variante}`, posicion, tipo.vidaBase);
```

#### Desafío
Completá el constructor del goblin.

#### Pasos
1. Buscá el `___` en el constructor de `Goblin`.
2. Cambialo por ``super(`Goblin ${tipo.variante}`, posicion, tipo.vidaBase);``.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Posicionable {
  x: number;
  y: number;
}

class Vec2 implements Posicionable {
  constructor(public x: number = 0, public y: number = 0) {}
  distanciaA(otro: Posicionable): number {
    return Math.hypot(this.x - otro.x, this.y - otro.y);
  }
  toString(): string {
    return `(${this.x}, ${this.y})`;
  }
}

abstract class Entidad {
  protected vida: number;
  constructor(public readonly nombre: string, public posicion: Vec2, protected readonly vidaMaxima: number) {
    this.vida = vidaMaxima;
  }
  describir(): string {
    return `${this.nombre}: ${this.vida}/${this.vidaMaxima} en ${this.posicion}`;
  }
}

class Heroe extends Entidad {
  constructor(posicion: Vec2) {
    super('Rigel', posicion, 100);
  }
}

type TipoGoblin =
  | { variante: 'normal'; vidaBase: 15 }
  | { variante: 'fuerte'; vidaBase: 30 };

class Goblin extends Entidad {
  constructor(posicion: Vec2, tipo: TipoGoblin) {
    ___
  }
}

interface Gema extends Posicionable {
  recolectada: boolean;
}

const rigel = new Heroe(new Vec2(0, 0));
const goblins = [new Goblin(new Vec2(10, 10), { variante: 'normal', vidaBase: 15 }), new Goblin(new Vec2(20, 5), { variante: 'fuerte', vidaBase: 30 })];
const gemas: Gema[] = [{ x: 3, y: 4, recolectada: false }, { x: 6, y: 8, recolectada: false }];

console.log(rigel.describir());
for (const g of goblins) console.log(g.describir());
console.log(`Gema más cercana a ${rigel.posicion.distanciaA(gemas[0]!)} pasos`);
```

#### Salida esperada
```
Rigel: 100/100 en (0, 0)
Goblin normal: 15/15 en (10, 10)
Goblin fuerte: 30/30 en (20, 5)
Gema más cercana a 5 pasos
```

#### Solución
```typescript
interface Posicionable {
  x: number;
  y: number;
}

class Vec2 implements Posicionable {
  constructor(public x: number = 0, public y: number = 0) {}
  distanciaA(otro: Posicionable): number {
    return Math.hypot(this.x - otro.x, this.y - otro.y);
  }
  toString(): string {
    return `(${this.x}, ${this.y})`;
  }
}

abstract class Entidad {
  protected vida: number;
  constructor(public readonly nombre: string, public posicion: Vec2, protected readonly vidaMaxima: number) {
    this.vida = vidaMaxima;
  }
  describir(): string {
    return `${this.nombre}: ${this.vida}/${this.vidaMaxima} en ${this.posicion}`;
  }
}

class Heroe extends Entidad {
  constructor(posicion: Vec2) {
    super('Rigel', posicion, 100);
  }
}

type TipoGoblin =
  | { variante: 'normal'; vidaBase: 15 }
  | { variante: 'fuerte'; vidaBase: 30 };

class Goblin extends Entidad {
  constructor(posicion: Vec2, tipo: TipoGoblin) {
    super(`Goblin ${tipo.variante}`, posicion, tipo.vidaBase);
  }
}

interface Gema extends Posicionable {
  recolectada: boolean;
}

const rigel = new Heroe(new Vec2(0, 0));
const goblins = [new Goblin(new Vec2(10, 10), { variante: 'normal', vidaBase: 15 }), new Goblin(new Vec2(20, 5), { variante: 'fuerte', vidaBase: 30 })];
const gemas: Gema[] = [{ x: 3, y: 4, recolectada: false }, { x: 6, y: 8, recolectada: false }];

console.log(rigel.describir());
for (const g of goblins) console.log(g.describir());
console.log(`Gema más cercana a ${rigel.posicion.distanciaA(gemas[0]!)} pasos`);
```

#### Al superarla
El modelo del Atlas queda medido de punta a punta. Astrea le da a Rigel una **estrella de latón**: —Ahora sí, a construir el juego.

#### Imagen
- Una doble página del Atlas con el modelo completo del juego: un héroe, dos goblins y dos gemas, unidos por flechas de luz.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) cierra el Atlas con cuidado; Gheco sobre la tapa.

## R05-N03 · Junta las Gemas tipado: el escenario

```meta
tipo: tema
padre: R05-N02
precio: 10
criatura: orc
temas: juegos.bucle, juegos.colisiones, cal.tipos
```

### Crónica

Con el modelo medido, Rigel abre la tercera parte del Atlas: la construcción del juego. El Vidriero lo armó sobre el lienzo de la Cúpula, pieza por pieza: primero el escenario, después el héroe, después las gemas. Al lado de cada pieza dejó una nota con una regla del Mirador.

—Es el mismo juego que Nima jugaba en la Feria —dice {mentor}—. Pero cada pieza tiene su medida. Mirá cuánto más fácil es cambiarlo sin romper nada.

### Objetivos

- Buscar los elementos de la página con una función genérica que corta si falta alguno: `obtenerElemento<T extends Element>`.
- Describir el estado del juego con una unión de opciones: `'jugando' | 'ganado' | 'perdido'`.
- Escribir los choques entre cajas con un tipo común (`Caja`).
- Mover al héroe con el teclado y juntar gemas.

### Antes de empezar

- R05-N02: el modelo del juego.
- R04-N04 y R04-N05: la página y el lienzo tipados.

### Explicación

#### Buscar o cortar
En lugar de preguntar por cada elemento, una función genérica busca y corta si falta:

```typescript
function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const lienzo = obtenerElemento<HTMLCanvasElement>('#lienzo');   // nunca null
```

#### El estado, sin errores de tipeo
```typescript
type EstadoJuego = 'jugando' | 'ganado' | 'perdido';
let estado: EstadoJuego = 'jugando';
estado = 'ganadoo';   // ✗ TS2322: en JavaScript, este error dejaba el juego sin pantalla de victoria
```

#### Todo lo que choca es una caja
```typescript
interface Caja { x: number; y: number; lado: number }

function chocan(a: Caja, b: Caja): boolean {
  return a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;
}
```

El héroe, las gemas y los goblins tienen más cosas, pero todos cumplen `Caja`: la misma función sirve para todos.

### Código de ejemplo

```typescript
interface Caja {
  x: number;
  y: number;
  lado: number;
}

function chocan(a: Caja, b: Caja): boolean {
  return a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;
}

type EstadoJuego = 'jugando' | 'ganado' | 'perdido';

const heroe = { x: 10, y: 10, lado: 12, vidas: 3 };
const gema = { x: 18, y: 14, lado: 8 };
let estado: EstadoJuego = 'jugando';
if (chocan(heroe, gema)) estado = 'ganado';
console.log(chocan(heroe, gema), estado);
```

### Salida esperada

```
true ganado
```

### ¿Para qué sirve?

Así se arman los juegos de verdad (y cualquier programa con interfaz): pocas funciones chicas, cada una con su tipo, que se combinan. Cuando el juego crece, el compilador te avisa en qué lugar se rompió algo.

### Errores habituales

**Orco: un elemento que falta.** Con `obtenerElemento`, el error dice **cuál** falta, en vez de un `null` misterioso más adelante.

**Goblin: el estado mal escrito (TS2322).** *El tipo '"ganadoo"' no se puede asignar al tipo 'EstadoJuego'*.

**Ogro: el héroe que se sale del lienzo.** `Math.max(0, Math.min(x, ancho - lado))` lo deja adentro.

### Micro-misión R05-N03-P1 · Buscar o cortar

```meta
lugar: El lienzo de la Cúpula
personajes: Rigel, Gheco
carta: obtenerElemento<T extends Element> | busca con querySelector<T> · si no está, throw con el selector · nunca devuelve null
recompensa: xp 10, oro 10
```

#### Escena
El juego del Atlas busca cuatro elementos en la página. En lugar de preguntar por cada uno, el Vidriero escribió una sola función que busca o corta.

#### Gheco sugiere
Una función genérica con restricción: `T extends Element` (cualquier elemento de la página). Busca con `querySelector<T>`, y si no encuentra nada, lanza un error que dice qué selector falta. Así nunca devuelve `null`.

#### Desafío
Completá la línea que corta si no encontró el elemento.

#### Pasos
1. Buscá el `___` en `obtenerElemento`.
2. Cambialo por ``if (!el) throw new Error(`Falta ${selector} en la página`);``.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f2c14e; font-family: monospace; display: grid; place-items: center; height: 100vh; }
</style>
<p>Gemas: <span id="gemas">0</span> de <span id="meta">?</span></p>
```

#### Estado
```
#meta
```

#### Código inicial
```typescript
function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  ___
  return el;
}

const meta = obtenerElemento<HTMLSpanElement>('#meta');
meta.textContent = '10';
```

#### Salida esperada
```
── Estado ──
#meta: 10
```

#### Solución
```typescript
function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const meta = obtenerElemento<HTMLSpanElement>('#meta');
meta.textContent = '10';
```

#### Al superarla
El marcador del juego aparece en la pared de la Cúpula: *Gemas: 0 de 10*.

#### Imagen
- La pared de la cúpula con un marcador de latón encendido (sin números legibles) sobre el lienzo de vidrio ahumado.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) lee el Atlas abierto.
- Gheco sobre el marcador.

### Micro-misión R05-N03-P2 · La victoria que no llegaba

```meta
lugar: El lienzo de la Cúpula
personajes: Rigel, Gheco
criatura: goblin
carta: Estado con unión de opciones | type EstadoJuego = 'jugando' | 'ganado' | 'perdido' · un estado mal escrito es TS2322
recompensa: xp 10, oro 10
```

#### Escena
En la versión de la Feria del juego, la pantalla de victoria nunca aparecía. El Vidriero anotó por qué en el margen del Atlas: un estado mal escrito.

#### Gheco sugiere
En JavaScript, `estado = 'ganadoo'` corre sin aviso, y la pregunta `estado === 'ganado'` nunca da verdadero. Con el tipo `EstadoJuego`, el compilador encuentra el error al escribirlo.

#### Desafío
Corregí el estado mal escrito.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `'ganadoo'` por `'ganado'`.
3. Tocá **Ejecutar**. Tiene que salir `¡Juntaste las 10 gemas!`.

#### Código inicial
```typescript
type EstadoJuego = 'jugando' | 'ganado' | 'perdido';

let estado: EstadoJuego = 'jugando';
const gemas = 10;
if (gemas === 10) estado = 'ganadoo';

console.log(estado === 'ganado' ? '¡Juntaste las 10 gemas!' : 'Seguí jugando');
```

#### Salida esperada
```
¡Juntaste las 10 gemas!
```

#### Solución
```typescript
type EstadoJuego = 'jugando' | 'ganado' | 'perdido';

let estado: EstadoJuego = 'jugando';
const gemas = 10;
if (gemas === 10) estado = 'ganado';

console.log(estado === 'ganado' ? '¡Juntaste las 10 gemas!' : 'Seguí jugando');
```

#### Al superarla
La pantalla de victoria se enciende por primera vez desde que existe el juego. El Vidriero la había esperado mucho tiempo.

#### Imagen
- El lienzo de vidrio ahumado con fuegos artificiales de luz y gemas brillando.
- Un goblin chiquito con un engranaje en la espalda escondiendo una letra «o» de más.
- Rigel (chico flaco con pecas, antiparras de latón) festeja con los brazos arriba; Gheco salta.

### Micro-misión R05-N03-P3 · Todo lo que choca

```meta
lugar: El lienzo de la Cúpula
personajes: Rigel, Gheco
carta: Un tipo común | interface Caja { x; y; lado } · héroe, gemas y goblins la cumplen · chocan(a: Caja, b: Caja)
recompensa: xp 10, oro 10
```

#### Escena
Para saber si el héroe toca una gema o un goblin, el juego compara sus cajas. Rigel escribe la función de los choques.

#### Gheco sugiere
Dos cajas chocan si se pisan en `x` y también en `y`:

```ts
a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y
```

Como los parámetros son `Caja`, sirve para el héroe, las gemas y los goblins: todos tienen `x`, `y` y `lado`.

#### Desafío
Completá el `return` de `chocan`.

#### Pasos
1. Buscá el `___` en `chocan`.
2. Cambialo por `a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y`.
3. Tocá **Ejecutar**. Tiene que salir `gema: true · goblin: false`.

#### Código inicial
```typescript
interface Caja {
  x: number;
  y: number;
  lado: number;
}

function chocan(a: Caja, b: Caja): boolean {
  return ___;
}

const heroe = { x: 10, y: 10, lado: 12, vidas: 3 };
const gema = { x: 18, y: 14, lado: 8, recolectada: false };
const goblin = { x: 60, y: 40, lado: 12, vida: 15 };
console.log(`gema: ${chocan(heroe, gema)} · goblin: ${chocan(heroe, goblin)}`);
```

#### Salida esperada
```
gema: true · goblin: false
```

#### Solución
```typescript
interface Caja {
  x: number;
  y: number;
  lado: number;
}

function chocan(a: Caja, b: Caja): boolean {
  return a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;
}

const heroe = { x: 10, y: 10, lado: 12, vidas: 3 };
const gema = { x: 18, y: 14, lado: 8, recolectada: false };
const goblin = { x: 60, y: 40, lado: 12, vida: 15 };
console.log(`gema: ${chocan(heroe, gema)} · goblin: ${chocan(heroe, goblin)}`);
```

#### Al superarla
En el Atlas, las cajas del héroe y de la gema se superponen con un destello. La del goblin queda lejos.

#### Imagen
- Una página del Atlas con tres cuadrados dibujados: dos superpuestos con un destello y uno lejos.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mide con el calibre.
- Gheco sobre el cuadrado lejano.

### Micro-misión R05-N03-P4 · El héroe se mueve

```meta
lugar: El lienzo de la Cúpula
personajes: Rigel, Gheco
carta: Mover con dt y límites | Set<string> de teclas · dx según la flecha · Math.max(0, Math.min(x, ancho - lado))
recompensa: xp 15, monedas 5
```

#### Escena
Rigel pone al héroe en el lienzo y lo hace caminar con las flechas, sin que se salga por los bordes.

#### Gheco sugiere
En cada cuadro: se mira qué flechas están apretadas, se avanza `velocidad * dt` y se deja la posición entre 0 y el borde menos el lado:

```ts
heroe.x = Math.max(0, Math.min(heroe.x + dx * heroe.velocidad * dt, 240 - heroe.lado));
```

#### Desafío
Completá la línea que mueve al héroe en `x`.

#### Pasos
1. Buscá el `___` en `moverHeroe`.
2. Cambialo por `heroe.x = Math.max(0, Math.min(heroe.x + dx * heroe.velocidad * dt, 240 - heroe.lado));`.
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
apretar ArrowRight
cuadros 120
soltar ArrowRight
```

#### Estado
```
lienzo
```

#### Código inicial
```typescript
interface Heroe {
  x: number;
  y: number;
  lado: number;
  velocidad: number;
}

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const ctx = obtenerElemento<HTMLCanvasElement>('#lienzo').getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;

const heroe: Heroe = { x: 20, y: 74, lado: 12, velocidad: 120 };
const teclas = new Set<string>();
addEventListener('keydown', (e: KeyboardEvent) => teclas.add(e.key));
addEventListener('keyup', (e: KeyboardEvent) => teclas.delete(e.key));

function moverHeroe(dt: number): void {
  let dx = 0;
  if (teclas.has('ArrowRight')) dx += 1;
  if (teclas.has('ArrowLeft')) dx -= 1;
  ___
}

let antes: number | null = null;
function cuadro(ahora: number): void {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  moverHeroe(dt);
  pincel.clearRect(0, 0, 240, 160);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(Math.round(heroe.x), heroe.y, heroe.lado, heroe.lado);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 240, 160)
lienzo: fillRect(228, 74, 12, 12) #f2c14e
```

#### Solución
```typescript
interface Heroe {
  x: number;
  y: number;
  lado: number;
  velocidad: number;
}

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const ctx = obtenerElemento<HTMLCanvasElement>('#lienzo').getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;

const heroe: Heroe = { x: 20, y: 74, lado: 12, velocidad: 120 };
const teclas = new Set<string>();
addEventListener('keydown', (e: KeyboardEvent) => teclas.add(e.key));
addEventListener('keyup', (e: KeyboardEvent) => teclas.delete(e.key));

function moverHeroe(dt: number): void {
  let dx = 0;
  if (teclas.has('ArrowRight')) dx += 1;
  if (teclas.has('ArrowLeft')) dx -= 1;
  heroe.x = Math.max(0, Math.min(heroe.x + dx * heroe.velocidad * dt, 240 - heroe.lado));
}

let antes: number | null = null;
function cuadro(ahora: number): void {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  moverHeroe(dt);
  pincel.clearRect(0, 0, 240, 160);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(Math.round(heroe.x), heroe.y, heroe.lado, heroe.lado);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
El héroe cruza el lienzo y se frena justo en el borde, sin salirse.

#### Imagen
- El lienzo de vidrio ahumado con un cuadrado dorado (el héroe) apoyado contra el borde derecho.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) aprieta una tecla de flecha de bronce.
- Gheco mirando el borde.

### Micro-misión R05-N03-P5 · Juntar gemas

```meta
lugar: El lienzo de la Cúpula
personajes: Rigel, Gheco, Astrea
carta: filter con tipo | gemas = gemas.filter((g) => !chocan(heroe, g)) · las que tocó se cuentan · el marcador muestra cuántas
recompensa: xp 15, monedas 5
```

#### Escena
Hay tres gemas en el camino del héroe. Cuando las toca, desaparecen y el marcador suma.

#### Gheco sugiere
En cada cuadro: se cuentan las gemas que el héroe toca y se dejan solo las que **no** toca:

```ts
const antes = gemas.length;
gemas = gemas.filter((g) => !chocan(heroe, g));
juntadas += antes - gemas.length;
```

#### Desafío
Completá la línea del `filter`.

#### Pasos
1. Buscá el `___` en `juntarGemas`.
2. Cambialo por `gemas = gemas.filter((g) => !chocan(heroe, g));`.
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
cuadros 90
soltar ArrowRight
```

#### Estado
```
#gemas
lienzo
```

#### Código inicial
```typescript
interface Caja {
  x: number;
  y: number;
  lado: number;
}

function chocan(a: Caja, b: Caja): boolean {
  return a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;
}

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const ctx = obtenerElemento<HTMLCanvasElement>('#lienzo').getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;
const marcador = obtenerElemento<HTMLSpanElement>('#gemas');

const heroe = { x: 10, y: 74, lado: 12, velocidad: 120 };
let gemas: Caja[] = [{ x: 60, y: 76, lado: 8 }, { x: 120, y: 76, lado: 8 }, { x: 200, y: 20, lado: 8 }];
let juntadas = 0;
const teclas = new Set<string>();
addEventListener('keydown', (e: KeyboardEvent) => teclas.add(e.key));
addEventListener('keyup', (e: KeyboardEvent) => teclas.delete(e.key));

function juntarGemas(): void {
  const antes = gemas.length;
  ___
  juntadas += antes - gemas.length;
  marcador.textContent = String(juntadas);
}

let antes: number | null = null;
function cuadro(ahora: number): void {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (teclas.has('ArrowRight')) heroe.x = Math.min(heroe.x + heroe.velocidad * dt, 240 - heroe.lado);
  juntarGemas();
  pincel.clearRect(0, 0, 240, 160);
  pincel.fillStyle = '#4fc3f7';
  for (const g of gemas) pincel.fillRect(g.x, g.y, g.lado, g.lado);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(Math.round(heroe.x), heroe.y, heroe.lado, heroe.lado);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#gemas: 2
lienzo: clearRect(0, 0, 240, 160)
lienzo: fillRect(200, 20, 8, 8) #4fc3f7
lienzo: fillRect(188, 74, 12, 12) #f2c14e
```

#### Solución
```typescript
interface Caja {
  x: number;
  y: number;
  lado: number;
}

function chocan(a: Caja, b: Caja): boolean {
  return a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;
}

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const ctx = obtenerElemento<HTMLCanvasElement>('#lienzo').getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;
const marcador = obtenerElemento<HTMLSpanElement>('#gemas');

const heroe = { x: 10, y: 74, lado: 12, velocidad: 120 };
let gemas: Caja[] = [{ x: 60, y: 76, lado: 8 }, { x: 120, y: 76, lado: 8 }, { x: 200, y: 20, lado: 8 }];
let juntadas = 0;
const teclas = new Set<string>();
addEventListener('keydown', (e: KeyboardEvent) => teclas.add(e.key));
addEventListener('keyup', (e: KeyboardEvent) => teclas.delete(e.key));

function juntarGemas(): void {
  const antes = gemas.length;
  gemas = gemas.filter((g) => !chocan(heroe, g));
  juntadas += antes - gemas.length;
  marcador.textContent = String(juntadas);
}

let antes: number | null = null;
function cuadro(ahora: number): void {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (teclas.has('ArrowRight')) heroe.x = Math.min(heroe.x + heroe.velocidad * dt, 240 - heroe.lado);
  juntarGemas();
  pincel.clearRect(0, 0, 240, 160);
  pincel.fillStyle = '#4fc3f7';
  for (const g of gemas) pincel.fillRect(g.x, g.y, g.lado, g.lado);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(Math.round(heroe.x), heroe.y, heroe.lado, heroe.lado);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
Dos gemas desaparecen en el camino del héroe; la tercera, arriba, espera. Astrea le da a Rigel una **estrella de latón**.

#### Imagen
- El lienzo de vidrio ahumado con el héroe dorado y una sola gema celeste arriba, y el marcador encendido.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sonríe; Gheco junto a la gema que queda.

## R05-N04 · Junta las Gemas tipado: los goblins

```meta
tipo: tema
padre: R05-N03
precio: 10
criatura: goblin
temas: juegos.bucle, juegos.colisiones, poo.genericos, cal.tipos
```

### Crónica

La cuarta parte del Atlas está manchada de tinta, como si el Vidriero la hubiera escrito apurado. Son los **goblins** del juego: persiguen al héroe, le sacan vidas, y el héroe se defiende con un golpe. Al final de la página, dos dibujos: una pantalla de victoria y una de derrota.

—Lo más difícil del juego son las reglas —dice {mentor}—. Cuándo pierde una vida, cuándo gana, cuándo termina. Con tipos, cada regla dice exactamente qué pasa.

### Objetivos

- Hacer que los goblins persigan al héroe (normalizar la dirección).
- Sacar vidas con un tiempo de invulnerabilidad.
- Atacar a los goblins cercanos y quedarse con los vivos.
- Decidir el fin del juego con una unión de estados y `never`, y guardar el récord con su tipo.

### Antes de empezar

- R05-N03: el escenario del juego.
- R03-N03 (`never`) y R04-N06 (lo que puede no estar).

### Explicación

#### Perseguir
```typescript
const dx = heroe.x - goblin.x;
const dy = heroe.y - goblin.y;
const largo = Math.hypot(dx, dy);
if (largo > 0) {
  goblin.x += (dx / largo) * goblin.velocidad * dt;
  goblin.y += (dy / largo) * goblin.velocidad * dt;
}
```

Dividir por el largo deja la dirección con largo 1: el goblin avanza siempre a su velocidad, esté lejos o cerca.

#### Un golpe, y un respiro
```typescript
if (ahora > heroe.invulnerableHasta) {
  heroe.vidas--;
  heroe.invulnerableHasta = ahora + 1000;   // un segundo sin recibir otro golpe
}
```

#### El mensaje de cada final
```typescript
type EstadoJuego = 'jugando' | 'ganado' | 'perdido';

function mensaje(e: EstadoJuego): string {
  switch (e) {
    case 'jugando': return '';
    case 'ganado': return '¡Juntaste las gemas!';
    case 'perdido': return 'Los goblins te ganaron · R para reiniciar';
    default: {
      const nunca: never = e;
      return nunca;
    }
  }
}
```

#### El récord
`localStorage` guarda texto: `Number(localStorage.getItem('record') ?? 0)` lo convierte, y si no hay nada, empieza en 0.

### Código de ejemplo

```typescript
const heroe = { x: 100, y: 100, vidas: 3, invulnerableHasta: -1 };
const goblin = { x: 70, y: 60, velocidad: 25 };

const dx = heroe.x - goblin.x;
const dy = heroe.y - goblin.y;
const largo = Math.hypot(dx, dy);
goblin.x += (dx / largo) * goblin.velocidad;
goblin.y += (dy / largo) * goblin.velocidad;

for (const ahora of [0, 500, 1200]) {
  if (ahora > heroe.invulnerableHasta) {
    heroe.vidas--;
    heroe.invulnerableHasta = ahora + 1000;
  }
}
console.log(goblin.x, goblin.y, heroe.vidas);
```

### Salida esperada

```
85 80 1
```

### ¿Para qué sirve?

Las reglas de un juego (o de cualquier sistema: un banco, una tienda) son lo que más cambia. Con los estados como unión y el `never`, agregar una regla nueva (por ejemplo, un estado `'pausa'`) hace que el compilador te muestre todos los lugares que hay que actualizar.

### Errores habituales

**Ogro: perder todas las vidas de un golpe.** Sin el tiempo de invulnerabilidad, un goblin encima del héroe le saca una vida en **cada cuadro**.

**Goblin: el récord como texto.** `localStorage.getItem` devuelve `string | null`: sin `Number(…)`, `9 > '12'` compara mal.

**Ogro: el estado que falta en el switch.** Con `never`, el compilador avisa si se agrega un estado y no su mensaje.

### Micro-misión R05-N04-P1 · El goblin que persigue

```meta
lugar: El lienzo de la Cúpula
personajes: Rigel, Gheco
criatura: goblin
carta: Perseguir | dx y dy hacia el héroe · dividir por el largo · avanza a su velocidad · if (largo > 0) para no dividir por cero
recompensa: xp 10, oro 10
```

#### Escena
El primer goblin del Atlas camina hacia el héroe, a su velocidad, sin importar lo lejos que esté.

#### Gheco sugiere
La dirección hacia el héroe es `(dx, dy)`. Dividida por su largo, tiene largo 1: así el goblin avanza siempre lo mismo por segundo. Si el largo es 0 (ya está encima), no se mueve.

#### Desafío
Completá las dos líneas que mueven al goblin.

#### Pasos
1. El primer `___`: `goblin.x += (dx / largo) * goblin.velocidad * dt;`.
2. El segundo `___`: `goblin.y += (dy / largo) * goblin.velocidad * dt;`.
3. Tocá **Ejecutar**. Tiene que salir `Goblin en (85, 80)`.

#### Código inicial
```typescript
interface Goblin {
  x: number;
  y: number;
  velocidad: number;
}

function perseguir(goblin: Goblin, objetivo: { x: number; y: number }, dt: number): void {
  const dx = objetivo.x - goblin.x;
  const dy = objetivo.y - goblin.y;
  const largo = Math.hypot(dx, dy);
  if (largo > 0) {
    ___
    ___
  }
}

const goblin: Goblin = { x: 70, y: 60, velocidad: 25 };
perseguir(goblin, { x: 100, y: 100 }, 1);
console.log(`Goblin en (${goblin.x}, ${goblin.y})`);
```

#### Salida esperada
```
Goblin en (85, 80)
```

#### Solución
```typescript
interface Goblin {
  x: number;
  y: number;
  velocidad: number;
}

function perseguir(goblin: Goblin, objetivo: { x: number; y: number }, dt: number): void {
  const dx = objetivo.x - goblin.x;
  const dy = objetivo.y - goblin.y;
  const largo = Math.hypot(dx, dy);
  if (largo > 0) {
    goblin.x += (dx / largo) * goblin.velocidad * dt;
    goblin.y += (dy / largo) * goblin.velocidad * dt;
  }
}

const goblin: Goblin = { x: 70, y: 60, velocidad: 25 };
perseguir(goblin, { x: 100, y: 100 }, 1);
console.log(`Goblin en (${goblin.x}, ${goblin.y})`);
```

#### Al superarla
El goblin del Atlas da su primer paso hacia el héroe: exactamente 25 de largo.

#### Imagen
- Una página del Atlas con un goblin dibujado avanzando por una línea punteada hacia el héroe.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) mide el paso con el calibre.
- Gheco siguiendo la línea punteada.

### Micro-misión R05-N04-P2 · Un golpe y un respiro

```meta
lugar: El lienzo de la Cúpula
personajes: Rigel, Gheco
criatura: ogre
carta: Invulnerabilidad | if (ahora > heroe.invulnerableHasta) · resta una vida · invulnerableHasta = ahora + 1000
recompensa: xp 10, oro 10
```

#### Escena
En la versión de la Feria, un goblin encima del héroe le sacaba todas las vidas en un instante. El Vidriero anotó la solución: un segundo de respiro después de cada golpe.

#### Gheco sugiere
Después de un golpe, el héroe queda **invulnerable** un segundo: solo puede perder otra vida si `ahora` ya pasó ese momento.

#### Desafío
Completá la función `golpear`.

#### Pasos
1. Buscá el `___` adentro del `if`.
2. Cambialo por `heroe.vidas--;` y, en el renglón de abajo, `heroe.invulnerableHasta = ahora + 1000;`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Heroe {
  vidas: number;
  invulnerableHasta: number;
}

function golpear(heroe: Heroe, ahora: number): void {
  if (ahora > heroe.invulnerableHasta) {
    ___
  }
}

const heroe: Heroe = { vidas: 3, invulnerableHasta: -1 };
for (const ahora of [0, 300, 900, 1100, 2500]) {
  golpear(heroe, ahora);
  console.log(`${ahora} ms: ${heroe.vidas} vidas`);
}
```

#### Salida esperada
```
0 ms: 2 vidas
300 ms: 2 vidas
900 ms: 2 vidas
1100 ms: 1 vidas
2500 ms: 0 vidas
```

#### Solución
```typescript
interface Heroe {
  vidas: number;
  invulnerableHasta: number;
}

function golpear(heroe: Heroe, ahora: number): void {
  if (ahora > heroe.invulnerableHasta) {
    heroe.vidas--;
    heroe.invulnerableHasta = ahora + 1000;
  }
}

const heroe: Heroe = { vidas: 3, invulnerableHasta: -1 };
for (const ahora of [0, 300, 900, 1100, 2500]) {
  golpear(heroe, ahora);
  console.log(`${ahora} ms: ${heroe.vidas} vidas`);
}
```

#### Al superarla
Los golpes llegan de a uno, con un respiro entre medio. El juego se vuelve justo.

#### Imagen
- Una página del Atlas con una línea de tiempo y tres corazones, uno de ellos brillando como un escudo.
- Un ogro chiquito con un mazo esperando que pase el escudo.
- Rigel (chico flaco con pecas, antiparras de latón) cuenta con un relojito; Gheco mira.

### Micro-misión R05-N04-P3 · El golpe del héroe

```meta
lugar: El lienzo de la Cúpula
personajes: Rigel, Gheco
carta: Atacar a los cercanos | los goblins a menos de 20 pierden vida · entidadesVivas<T> se queda con los que siguen · el tipo se conserva
recompensa: xp 10, oro 10
```

#### Escena
El héroe tiene un golpe: le saca 10 de vida a todos los goblins que están cerca (a menos de 20 pasos). Los que quedan sin vida desaparecen.

#### Gheco sugiere
- `Math.hypot(g.x - heroe.x, g.y - heroe.y) < 20`: el goblin está cerca.
- Después, `vivos(goblins)` se queda con los que tienen vida. Es genérico: devuelve `Goblin[]`.

#### Desafío
Completá la pregunta de quién está cerca.

#### Pasos
1. Buscá el `___` en el `if`.
2. Cambialo por `Math.hypot(g.x - heroe.x, g.y - heroe.y) < 20`.
3. Tocá **Ejecutar**. Tiene que salir `Quedan: lejano (15), fuerte (20)`.

#### Código inicial
```typescript
interface Goblin {
  nombre: string;
  x: number;
  y: number;
  vida: number;
}

function vivos<T extends { vida: number }>(lista: T[]): T[] {
  return lista.filter((e) => e.vida > 0);
}

const heroe = { x: 100, y: 100 };
let goblins: Goblin[] = [
  { nombre: 'cercano', x: 110, y: 100, vida: 10 },
  { nombre: 'lejano', x: 10, y: 10, vida: 15 },
  { nombre: 'fuerte', x: 95, y: 105, vida: 30 },
];

for (const g of goblins) {
  if (___) g.vida -= 10;
}
goblins = vivos(goblins);
console.log(`Quedan: ${goblins.map((g) => `${g.nombre} (${g.vida})`).join(', ')}`);
```

#### Salida esperada
```
Quedan: lejano (15), fuerte (20)
```

#### Solución
```typescript
interface Goblin {
  nombre: string;
  x: number;
  y: number;
  vida: number;
}

function vivos<T extends { vida: number }>(lista: T[]): T[] {
  return lista.filter((e) => e.vida > 0);
}

const heroe = { x: 100, y: 100 };
let goblins: Goblin[] = [
  { nombre: 'cercano', x: 110, y: 100, vida: 10 },
  { nombre: 'lejano', x: 10, y: 10, vida: 15 },
  { nombre: 'fuerte', x: 95, y: 105, vida: 30 },
];

for (const g of goblins) {
  if (Math.hypot(g.x - heroe.x, g.y - heroe.y) < 20) g.vida -= 10;
}
goblins = vivos(goblins);
console.log(`Quedan: ${goblins.map((g) => `${g.nombre} (${g.vida})`).join(', ')}`);
```

#### Al superarla
El goblin cercano se desarma con el golpe; el fuerte se tambalea.

#### Imagen
- Una página del Atlas con un círculo de golpe alrededor del héroe y un goblin desarmándose adentro.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) dibuja el círculo con el compás.
- Gheco haciendo de goblin con cara de susto.

### Micro-misión R05-N04-P4 · Los dos finales

```meta
lugar: El lienzo de la Cúpula
personajes: Rigel, Gheco, Astrea
criatura: ogre
carta: Estados con never | type EstadoJuego = 'jugando' | 'ganado' | 'perdido' | 'pausa' · el never avisa qué mensaje falta
recompensa: xp 15, monedas 5
```

#### Escena
Astrea agrega un estado nuevo al juego: la **pausa**. La máquina de los mensajes, que tenía su alarma `never`, se queja enseguida: falta el mensaje de la pausa.

#### Gheco sugiere
Al agregar `'pausa'` a la unión, el `default` con `never` deja de compilar: el compilador te dice que falta ese caso. Se agrega su `case`.

#### Desafío
Agregá el mensaje de la pausa.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el `___`, escribí `case 'pausa':` y, abajo, `return 'En pausa · P para seguir';`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type EstadoJuego = 'jugando' | 'ganado' | 'perdido' | 'pausa';

function mensaje(e: EstadoJuego): string {
  switch (e) {
    case 'jugando':
      return '';
    case 'ganado':
      return '¡Juntaste las gemas!';
    case 'perdido':
      return 'Los goblins te ganaron · R para reiniciar';
    ___
    default: {
      const nunca: never = e;
      return nunca;
    }
  }
}

const estados: EstadoJuego[] = ['ganado', 'pausa', 'perdido'];
for (const e of estados) console.log(mensaje(e));
```

#### Salida esperada
```
¡Juntaste las gemas!
En pausa · P para seguir
Los goblins te ganaron · R para reiniciar
```

#### Solución
```typescript
type EstadoJuego = 'jugando' | 'ganado' | 'perdido' | 'pausa';

function mensaje(e: EstadoJuego): string {
  switch (e) {
    case 'jugando':
      return '';
    case 'ganado':
      return '¡Juntaste las gemas!';
    case 'perdido':
      return 'Los goblins te ganaron · R para reiniciar';
    case 'pausa':
      return 'En pausa · P para seguir';
    default: {
      const nunca: never = e;
      return nunca;
    }
  }
}

const estados: EstadoJuego[] = ['ganado', 'pausa', 'perdido'];
for (const e of estados) console.log(mensaje(e));
```

#### Al superarla
El juego aprende a esperar. Astrea sonríe: —Un estado nuevo, y el compilador te llevó de la mano al único lugar que había que tocar.

#### Imagen
- El lienzo de vidrio ahumado con un cartel de pausa en el medio y el juego congelado detrás.
- Astrea (lechuza con anteojos de latón y chaleco azul) aprieta una tecla de pausa.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) se estira; Gheco duerme una siesta.

### Micro-misión R05-N04-P5 · El récord del Mirador

```meta
lugar: El lienzo de la Cúpula
personajes: Rigel, Gheco
carta: El récord tipado | Number(localStorage.getItem('record') ?? 0) · getItem da string | null · se guarda con String(…)
recompensa: xp 15, monedas 5
```

#### Escena
El juego guarda el récord de gemas en la memoria de la Cúpula. El Vidriero había dejado anotado un 12. Esta noche, Rigel juega tres partidas.

#### Gheco sugiere
`localStorage.getItem('record')` devuelve `string | null`. Para compararlo con un número, se convierte, y si no hay nada, se empieza en 0:

```ts
const record = Number(localStorage.getItem('record') ?? 0);
```

Para guardar, se pasa a texto: `localStorage.setItem('record', String(gemas))`.

#### Desafío
Completá la lectura del récord.

#### Pasos
1. Buscá el `___` en `terminar`.
2. Cambialo por `const record = Number(localStorage.getItem('record') ?? 0);`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Almacenamiento
```
local record = 12
```

#### Estado
```
local record
```

#### Código inicial
```typescript
function terminar(gemas: number): void {
  ___
  if (gemas > record) {
    localStorage.setItem('record', String(gemas));
    console.log(`${gemas}: ¡récord nuevo!`);
  } else {
    console.log(`${gemas}: el récord sigue en ${record}`);
  }
}

for (const partida of [9, 15, 14]) terminar(partida);
```

#### Salida esperada
```
9: el récord sigue en 12
15: ¡récord nuevo!
14: el récord sigue en 15
── Estado ──
local record: 15
```

#### Solución
```typescript
function terminar(gemas: number): void {
  const record = Number(localStorage.getItem('record') ?? 0);
  if (gemas > record) {
    localStorage.setItem('record', String(gemas));
    console.log(`${gemas}: ¡récord nuevo!`);
  } else {
    console.log(`${gemas}: el récord sigue en ${record}`);
  }
}

for (const partida of [9, 15, 14]) terminar(partida);
```

#### Al superarla
El récord del Vidriero cae: 15 gemas. Rigel no sabe si festejar o pedir perdón.

#### Imagen
- Una placa de récord de latón en la pared de la cúpula con un número nuevo grabado (sin números legibles).
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mira la placa con una mezcla de orgullo y vergüenza.
- Gheco aplaude.

## R05-N05 · Jefe: el Dragón de las Constelaciones Rotas

```meta
tipo: jefe
padre: R05-N04
precio: 10
criatura: dragon
insignia: Calibre del Vidriero
insignia_descripcion: Venciste al Dragón de las Constelaciones Rotas y pusiste en marcha el Planisferio: armás un programa grande con tipos chicos.
usa: cal.tipos, poo.genericos, poo.interfaces, poo.herencia, juegos.bucle, juegos.colisiones, js.dom
```

### Crónica

Rigel cierra el Atlas y sube a la sala del **Gran Planisferio**. Cada pieza ya está en su lugar, pero cuando tira de la palanca, las estrellas se sueltan de sus brazos de latón y se juntan en el aire. Forman un autómata enorme de vidrio y bronce, con alas de constelaciones mal armadas: **el Dragón de las Constelaciones Rotas**. Cada vez que respira, una estrella cambia de forma y el vitral del balcón tiembla.

—El Dragón está hecho de todos los errores que viste en el Mirador —dice {mentor}—. Un `any` por acá, un caso que falta por allá, un estado mal escrito. Vencelo pieza por pieza, como armaste el juego.

### Objetivos

- Integrar todo el curso: tipos, uniones, interfaces, clases, genéricos, la página y el lienzo.
- Reparar el modelo del juego y ponerlo a andar entero.

### Antes de empezar

- Todo el Atlas (R05-N01 a R05-N04) y, si dudás, el jefe de cada rama.

### Explicación

#### Cómo encarar al Dragón
1. **Leé el error entero**: dice el archivo, la línea y qué no encaja.
2. **Arreglá la medida, no el síntoma**: si un valor está mal, buscá dónde se decidió su tipo.
3. **Nunca un `any` ni un `!` para callar al compilador**: es justo por donde entra el Dragón.
4. **Ejecutá después de cada paso.**

#### Las trampas del Dragón (y la verdad)
| El Dragón dice… | La verdad |
|---|---|
| "con `any` anda igual" | `any` apaga las revisiones: `'3' + 1` da `'31'` |
| "ese caso nunca llega" | con `never`, el compilador te muestra el que falta |
| "una clase por cada bicho" | una clase base y un genérico sirven para todos |
| "el juego está listo" | está listo cuando compila sin errores **y** anda |

### Micro-misión R05-N05-P1 · La estrella sin forma

```meta
lugar: La sala del Planisferio
personajes: Rigel, Gheco, el Dragón de las Constelaciones Rotas
criatura: goblin
carta: Trampa 1 | any apaga las revisiones · '3' + 1 da '31' · con su tipo, el compilador avisa y Number(…) lo arregla
recompensa: xp 15, monedas 3
```

#### Escena
La primera estrella que suelta el Dragón es el contador de vidas del juego. El Dragón la dejó sin forma (`any`), y la vida que lee de la memoria llega como texto: el héroe termina con **31** vidas.

#### Gheco sugiere
Con `any`, el compilador no revisa nada. Cambiá `any` por `string`: el compilador te va a mostrar dónde se suma un texto con un número. Ahí, convertilo con `Number(...)`.

#### Desafío
Dale su tipo al valor leído y convertilo a número.

#### Pasos
1. Cambiá `const guardadas: any` por `const guardadas: string`.
2. Tocá **Ejecutar**: el compilador marca la línea de `vidas`.
3. Cambiá `const vidas: number = guardadas + 1;` por `const vidas: number = Number(guardadas) + 1;`.
4. Tocá **Ejecutar**. Tiene que salir `El héroe tiene 4 vidas`.

#### Código inicial
```typescript
// Lo que se lee de la memoria siempre llega como texto.
const guardadas: any = '3';
const vidas: number = guardadas + 1;
console.log(`El héroe tiene ${vidas} vidas`);
```

#### Salida esperada
```
El héroe tiene 4 vidas
```

#### Solución
```typescript
// Lo que se lee de la memoria siempre llega como texto.
const guardadas: string = '3';
const vidas: number = Number(guardadas) + 1;
console.log(`El héroe tiene ${vidas} vidas`);
```

#### Al superarla
La estrella toma su forma y vuelve a su brazo de latón con un clic. El Dragón pierde un pedazo del ala.

#### Imagen
- La sala del Planisferio con un autómata-dragón enorme de vidrio y bronce, con alas de constelaciones mal armadas.
- Una estrella de vidrio volviendo a un brazo de latón con un destello.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) apunta con el calibre; Gheco se agarra de su hombro.

### Micro-misión R05-N05-P2 · La figura que faltaba

```meta
lugar: La sala del Planisferio
personajes: Rigel, Gheco, el Dragón de las Constelaciones Rotas
criatura: ogre
carta: Trampa 2 | unión con discriminante tipo · el switch con never avisa el caso que falta · se agrega su case
recompensa: xp 15, monedas 3
```

#### Escena
El Dragón agregó una figura nueva al modelo, la **trampa**, y escondió su caso en la tabla de puntos. El Planisferio no sabe cuánto vale y se traba.

#### Gheco sugiere
`Entidad` es una unión con el campo `tipo`. El `default` con `never` deja de compilar si falta un caso. Leé el error: dice cuál falta. Una trampa resta 5 puntos.

#### Desafío
Agregá el caso de la trampa.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el `___`, escribí `case 'trampa':` y, abajo, `return -5;`.
3. Tocá **Ejecutar**. Tiene que salir `Puntos: 15`.

#### Código inicial
```typescript
interface Gema { tipo: 'gema'; valor: number }
interface Goblin { tipo: 'goblin'; vida: number }
interface Trampa { tipo: 'trampa'; x: number }
type Entidad = Gema | Goblin | Trampa;

function puntos(e: Entidad): number {
  switch (e.tipo) {
    case 'gema':
      return e.valor;
    case 'goblin':
      return 10;
    ___
    default: {
      const nunca: never = e;
      return nunca;
    }
  }
}

const tocadas: Entidad[] = [{ tipo: 'gema', valor: 5 }, { tipo: 'goblin', vida: 0 }, { tipo: 'gema', valor: 5 }, { tipo: 'trampa', x: 40 }];
console.log(`Puntos: ${tocadas.reduce((total, e) => total + puntos(e), 0)}`);
```

#### Salida esperada
```
Puntos: 15
```

#### Solución
```typescript
interface Gema { tipo: 'gema'; valor: number }
interface Goblin { tipo: 'goblin'; vida: number }
interface Trampa { tipo: 'trampa'; x: number }
type Entidad = Gema | Goblin | Trampa;

function puntos(e: Entidad): number {
  switch (e.tipo) {
    case 'gema':
      return e.valor;
    case 'goblin':
      return 10;
    case 'trampa':
      return -5;
    default: {
      const nunca: never = e;
      return nunca;
    }
  }
}

const tocadas: Entidad[] = [{ tipo: 'gema', valor: 5 }, { tipo: 'goblin', vida: 0 }, { tipo: 'gema', valor: 5 }, { tipo: 'trampa', x: 40 }];
console.log(`Puntos: ${tocadas.reduce((total, e) => total + puntos(e), 0)}`);
```

#### Al superarla
La tabla de puntos se completa y el Planisferio da un primer giro, chirriando. El Dragón ruge.

#### Imagen
- El Planisferio dando un giro, con una tabla de latón llena de casilleros encendidos.
- Un ogro chiquito con un engranaje en la espalda escapando con un casillero vacío.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) pone la última pieza; Gheco empuja.

### Micro-misión R05-N05-P3 · Lo que dice el compilador

```meta
lugar: La sala del Planisferio
personajes: Rigel, Gheco, Astrea
carta: Trampa 3 | leer los errores antes de ejecutar · cada código y su línea · son las constelaciones rotas del Dragón
recompensa: xp 15, monedas 3
```

#### Escena
El Dragón respira sobre el programa del Planisferio y lo llena de errores escondidos. Astrea saca el catalejo: —Antes de arreglar, contá cuántos son y dónde están.

#### Gheco sugiere
Esta misión no se ejecuta: el compilador revisa el código y muestra los errores. Leé el código buscando los tres:
- una propiedad mal escrita;
- un valor que no es del tipo que se pide;
- un método que la clase promete (por la interfaz) y no tiene.

Después, tocá **Ejecutar** y compará.

#### Desafío
Leé los tres errores y arreglá el más fácil: la propiedad mal escrita.

#### Pasos
1. Tocá **Ejecutar**: la salida son los errores, con su código y su línea (`TS2420`, `TS2345` y `TS2551`).
2. Cambiá `polar.nombr` por `polar.nombre`.
3. Tocá **Ejecutar**: quedan dos constelaciones rotas, `TS2420` y `TS2345`. Las vas a vencer con las próximas trampas.

#### Compilador
sí

#### Código inicial
```typescript
interface Dibujable {
  dibujar(): string;
}

class Estrella implements Dibujable {
  constructor(public nombre: string, public brillo: number) {}
}

const polar = new Estrella('Polar', 'mucho');
console.log(polar.nombr);
```

#### Salida esperada
```
TS2420 en la línea 5
TS2345 en la línea 9
```

#### Solución
```typescript
interface Dibujable {
  dibujar(): string;
}

class Estrella implements Dibujable {
  constructor(public nombre: string, public brillo: number) {}
}

const polar = new Estrella('Polar', 'mucho');
console.log(polar.nombre);
```

#### Al superarla
Astrea anota los tres errores en el margen del Atlas. Cada uno es una constelación del Dragón que ya no puede esconderse.

#### Imagen
- Una página del programa del Planisferio con tres manchas de luz roja marcadas.
- Astrea (lechuza con anteojos de latón y chaleco azul) mira por el catalejo.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) cuenta con los dedos; Gheco señala una mancha.

### Micro-misión R05-N05-P4 · Un brazo para todas las piezas

```meta
lugar: La sala del Planisferio
personajes: Rigel, Gheco
carta: Trampa 4 | una clase base abstracta · un genérico con T extends Pieza · el mismo método para estrellas y planetas
recompensa: xp 15, monedas 3
```

#### Escena
El Dragón le grita a Rigel que necesita un brazo distinto para cada pieza del Planisferio. Rigel arma uno solo, genérico, que sirve para cualquier pieza.

#### Gheco sugiere
`la más brillante` de una lista sirve para estrellas y para planetas si es genérica: `T extends Pieza`. Así devuelve una `Estrella` si le pasás estrellas, y un `Planeta` si le pasás planetas, con sus propiedades.

#### Desafío
Completá la firma de la función genérica.

#### Pasos
1. Buscá el `___` en la firma.
2. Cambialo por `function masBrillante<T extends Pieza>(lista: T[]): T | undefined`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
abstract class Pieza {
  constructor(public nombre: string, public brillo: number) {}
  abstract describir(): string;
}

class Estrella extends Pieza {
  describir(): string {
    return `estrella ${this.nombre}`;
  }
}

class Planeta extends Pieza {
  constructor(nombre: string, brillo: number, public lunas: number) {
    super(nombre, brillo);
  }
  describir(): string {
    return `planeta ${this.nombre} con ${this.lunas} lunas`;
  }
}

___ {
  let mejor: T | undefined;
  for (const p of lista) if (!mejor || p.brillo > mejor.brillo) mejor = p;
  return mejor;
}

const estrellas = [new Estrella('Polar', 7), new Estrella('Vega', 9)];
const planetas = [new Planeta('Rojo', 4, 2), new Planeta('Anillado', 6, 82)];
console.log(masBrillante(estrellas)?.describir());
console.log(masBrillante(planetas)?.lunas);
console.log(masBrillante<Estrella>([])?.nombre ?? 'sin piezas');
```

#### Salida esperada
```
estrella Vega
82
sin piezas
```

#### Solución
```typescript
abstract class Pieza {
  constructor(public nombre: string, public brillo: number) {}
  abstract describir(): string;
}

class Estrella extends Pieza {
  describir(): string {
    return `estrella ${this.nombre}`;
  }
}

class Planeta extends Pieza {
  constructor(nombre: string, brillo: number, public lunas: number) {
    super(nombre, brillo);
  }
  describir(): string {
    return `planeta ${this.nombre} con ${this.lunas} lunas`;
  }
}

function masBrillante<T extends Pieza>(lista: T[]): T | undefined {
  let mejor: T | undefined;
  for (const p of lista) if (!mejor || p.brillo > mejor.brillo) mejor = p;
  return mejor;
}

const estrellas = [new Estrella('Polar', 7), new Estrella('Vega', 9)];
const planetas = [new Planeta('Rojo', 4, 2), new Planeta('Anillado', 6, 82)];
console.log(masBrillante(estrellas)?.describir());
console.log(masBrillante(planetas)?.lunas);
console.log(masBrillante<Estrella>([])?.nombre ?? 'sin piezas');
```

#### Al superarla
Un solo brazo de latón sostiene estrellas y planetas. Al Dragón se le caen las dos alas.

#### Imagen
- Un brazo mecánico de latón sosteniendo a la vez una estrella de vidrio y un planeta con anillos.
- El dragón de vidrio y bronce sin alas, más chico.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) ajusta el brazo con una llave; Gheco sobre el planeta.

### Micro-misión R05-N05-P5 · El Planisferio en marcha

```meta
lugar: La sala del Planisferio
personajes: Rigel, Gheco, Astrea, Fuelle, el Dragón de las Constelaciones Rotas
carta: El jefe | obtenerElemento · Caja y chocan · EstadoJuego · bucle con dt · el juego entero, tipado, compila y anda
recompensa: xp 20, monedas 5
```

#### Escena
Queda el corazón del Dragón: el juego del Planisferio. Rigel lo arma entero, con todas las piezas del Atlas: el héroe se mueve, junta las gemas de las constelaciones, y cuando junta todas, el estado pasa a **ganado**.

#### Gheco sugiere
Está casi todo. Falta la regla que decide el final: si no quedan gemas, el estado es `'ganado'`, y el cartel lo dice. Usá el tipo `EstadoJuego`: si lo escribís mal, el compilador te avisa.

#### Desafío
Completá la regla de la victoria.

#### Pasos
1. Buscá el `___` en `reglas`.
2. Cambialo por `if (gemas.length === 0) estado = 'ganado';`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f2c14e; font-family: monospace; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1326; border: 6px solid #8d6e3f; }
</style>
<p>Gemas: <span id="gemas">0</span> · <span id="estado">jugando</span></p>
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
#gemas
#estado
lienzo
```

#### Código inicial
```typescript
interface Caja {
  x: number;
  y: number;
  lado: number;
}
type EstadoJuego = 'jugando' | 'ganado' | 'perdido';

function chocan(a: Caja, b: Caja): boolean {
  return a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;
}

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const ctx = obtenerElemento<HTMLCanvasElement>('#lienzo').getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;
const marcador = obtenerElemento<HTMLSpanElement>('#gemas');
const cartel = obtenerElemento<HTMLSpanElement>('#estado');

const heroe = { x: 10, y: 74, lado: 12, velocidad: 120 };
let gemas: Caja[] = [40, 90, 140, 190].map((x) => ({ x, y: 76, lado: 8 }));
let juntadas = 0;
let estado: EstadoJuego = 'jugando';
const teclas = new Set<string>();
addEventListener('keydown', (e: KeyboardEvent) => teclas.add(e.key));
addEventListener('keyup', (e: KeyboardEvent) => teclas.delete(e.key));

function reglas(): void {
  const antes = gemas.length;
  gemas = gemas.filter((g) => !chocan(heroe, g));
  juntadas += antes - gemas.length;
  ___
}

function dibujar(): void {
  pincel.clearRect(0, 0, 240, 160);
  pincel.fillStyle = '#4fc3f7';
  for (const g of gemas) pincel.fillRect(g.x, g.y, g.lado, g.lado);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(Math.round(heroe.x), heroe.y, heroe.lado, heroe.lado);
  marcador.textContent = String(juntadas);
  cartel.textContent = estado === 'ganado' ? '¡El Planisferio anda!' : estado;
}

let antes: number | null = null;
function cuadro(ahora: number): void {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (estado === 'jugando') {
    if (teclas.has('ArrowRight')) heroe.x = Math.min(heroe.x + heroe.velocidad * dt, 240 - heroe.lado);
    if (teclas.has('ArrowLeft')) heroe.x = Math.max(heroe.x - heroe.velocidad * dt, 0);
    reglas();
  }
  dibujar();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#gemas: 4
#estado: ¡El Planisferio anda!
lienzo: clearRect(0, 0, 240, 160)
lienzo: fillRect(180, 74, 12, 12) #f2c14e
```

#### Solución
```typescript
interface Caja {
  x: number;
  y: number;
  lado: number;
}
type EstadoJuego = 'jugando' | 'ganado' | 'perdido';

function chocan(a: Caja, b: Caja): boolean {
  return a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;
}

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const ctx = obtenerElemento<HTMLCanvasElement>('#lienzo').getContext('2d');
if (!ctx) throw new Error('No hay dónde dibujar');
const pincel: CanvasRenderingContext2D = ctx;
const marcador = obtenerElemento<HTMLSpanElement>('#gemas');
const cartel = obtenerElemento<HTMLSpanElement>('#estado');

const heroe = { x: 10, y: 74, lado: 12, velocidad: 120 };
let gemas: Caja[] = [40, 90, 140, 190].map((x) => ({ x, y: 76, lado: 8 }));
let juntadas = 0;
let estado: EstadoJuego = 'jugando';
const teclas = new Set<string>();
addEventListener('keydown', (e: KeyboardEvent) => teclas.add(e.key));
addEventListener('keyup', (e: KeyboardEvent) => teclas.delete(e.key));

function reglas(): void {
  const antes = gemas.length;
  gemas = gemas.filter((g) => !chocan(heroe, g));
  juntadas += antes - gemas.length;
  if (gemas.length === 0) estado = 'ganado';
}

function dibujar(): void {
  pincel.clearRect(0, 0, 240, 160);
  pincel.fillStyle = '#4fc3f7';
  for (const g of gemas) pincel.fillRect(g.x, g.y, g.lado, g.lado);
  pincel.fillStyle = '#f2c14e';
  pincel.fillRect(Math.round(heroe.x), heroe.y, heroe.lado, heroe.lado);
  marcador.textContent = String(juntadas);
  cartel.textContent = estado === 'ganado' ? '¡El Planisferio anda!' : estado;
}

let antes: number | null = null;
function cuadro(ahora: number): void {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (estado === 'jugando') {
    if (teclas.has('ArrowRight')) heroe.x = Math.min(heroe.x + heroe.velocidad * dt, 240 - heroe.lado);
    if (teclas.has('ArrowLeft')) heroe.x = Math.max(heroe.x - heroe.velocidad * dt, 0);
    reglas();
  }
  dibujar();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
La última gema encaja y el Dragón se deshace en una lluvia de estrellas, que vuelven una por una a sus brazos de latón. El **Gran Planisferio** arranca: las constelaciones giran despacio sobre la sala, como cuando el Vidriero estaba ahí. Afuera, en el balcón, el vitral del portal deja de temblar y **se queda quieto en la figura correcta**, por primera vez.

En la última hoja del Atlas, Rigel encuentra el plano entero del portal, con todas sus figuras. Falta una sola. Al lado, con la letra apurada del Vidriero: *«La última figura no se mide desde acá.»*

Astrea guarda el catalejo. Fuelle sopla una nube de vapor contenta. Y Rigel guarda en el bolsillo **el Calibre del Vidriero**, que estaba escondido en el centro del Planisferio: el que mide el portal.

#### Imagen
- La sala del Gran Planisferio en marcha: constelaciones de vidrio girando en brazos de latón, con luz dorada.
- Por la ventana, el vitral del portal en el balcón, quieto y brillando.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) sostiene un calibre antiguo de latón; Astrea (lechuza con anteojos de latón y chaleco azul) y Fuelle (zorro mecánico de latón) a su lado; Gheco sobre el hombro de Rigel.
