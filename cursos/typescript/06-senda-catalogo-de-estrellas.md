# RAMA S01 · Senda del Catálogo de Estrellas: buscar, ordenar y contar datos

```meta
tipo: senda
posicion: 6
```

## S01-N01 · Buscar en el Catálogo

```meta
tipo: tema
padre: R02-N07
precio: 3
moneda: comodin
criatura: skeleton
temas: alg.busqueda, col.arrays
usa: cal.tipos, func.orden-superior, poo.genericos
```

### Crónica

Una tarde llega al Mirador **Nima**, con su trenza negra y el arco verde a la espalda. Trae una caja de fichas de cartón: *—Sila me mandó esto desde el Archivo de la Feria. Es el **Catálogo de Estrellas** del Vidriero: todas las estrellas que midió, una por ficha. Se le mezclaron con la mudanza.*

Rigel abre la caja. Cada ficha tiene un nombre, una constelación, un brillo, una distancia y un tipo de estrella. En una de ellas, con letra chiquita, dice **Rigel**.

—Te pusieron el nombre de una estrella —se ríe Nima—. Bueno, vamos a ordenar esto. En la Feria lo hacíamos sin tipos y siempre se colaba alguna ficha rota.

### Objetivos

- Describir cada ficha con una `interface` y los tipos de estrella con una unión.
- Buscar una ficha con `find` y manejar el `undefined` cuando no está.
- Quedarse con varias con `filter`, y preguntar con `some` y `every`.
- Armar un buscador con filtros opcionales y uno genérico con `keyof`.

### Antes de empezar

- Los Moldes de Estrellas (R02), sobre todo los genéricos y `keyof` (R02-N06 y R02-N07).
- Si hiciste la Senda del Archivo de Sila en JavaScript, es lo mismo, pero ahora el compilador cuida cada campo.

### Explicación

#### La forma de una ficha
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';

interface Estrella {
  nombre: string;
  constelacion: string;
  brillo: number;      // de 1 a 10
  distancia: number;   // en años luz
  tipo: Tipo;
}
```

#### Buscar una: `find`
```typescript
const vega = catalogo.find((e) => e.nombre === 'Vega');   // Estrella | undefined
console.log(vega?.distancia ?? 'no está');
```
`find` devuelve la primera que cumple, o `undefined` si ninguna cumple. TypeScript lo sabe, y te obliga a preguntar antes de usarla.

#### Quedarse con varias: `filter`
```typescript
const enanas = catalogo.filter((e) => e.tipo === 'enana');   // Estrella[]
```

#### Preguntar por todas: `some` y `every`
- `some`: ¿hay **alguna** que cumpla? → `boolean`.
- `every`: ¿cumplen **todas**? → `boolean`.

#### Un buscador genérico
```typescript
function buscarPor<K extends keyof Estrella>(campo: K, valor: Estrella[K]): Estrella[] {
  return catalogo.filter((e) => e[campo] === valor);
}
buscarPor('tipo', 'gigante');   // ✓
buscarPor('brillo', 'mucho');   // ✗ el brillo es un número
```

### Código de ejemplo

```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; constelacion: string; brillo: number; distancia: number; tipo: Tipo }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', constelacion: 'Can Mayor', brillo: 10, distancia: 9, tipo: 'enana' },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7, distancia: 860, tipo: 'supergigante' },
  { nombre: 'Arturo', constelacion: 'Boyero', brillo: 9, distancia: 37, tipo: 'gigante' },
];

console.log(catalogo.find((e) => e.nombre === 'Rigel')?.constelacion);
console.log(catalogo.filter((e) => e.brillo >= 9).length);
console.log(catalogo.some((e) => e.tipo === 'enana'), catalogo.every((e) => e.distancia < 100));
```

### Salida esperada

```
Orión
2
true false
```

### ¿Para qué sirve?

Buscar en una lista es lo que más hace un programa: el catálogo de una tienda, los alumnos de un curso, los mensajes de un chat. Con los campos tipados, un error de tipeo en el nombre de un campo o en un valor se ve antes de ejecutar.

### Errores habituales

**Esqueleto: usar lo que `find` no encontró.** `catalogo.find(...).nombre` no compila (TS18048): puede ser `undefined`. Se pregunta con `?.` o con un `if`.

**Goblin: un tipo de estrella mal escrito.** `'enano'` no es un `Tipo` (TS2345 o TS2322).

**Ogro: `filter` cuando querías uno solo.** `filter` devuelve siempre un arreglo, aunque tenga uno o ninguno.

### Micro-misión S01-N01-P1 · La ficha de Vega

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Nima
criatura: skeleton
carta: find tipado | catalogo.find((e) => …) da Estrella | undefined · ?. y ?? para lo que no está
recompensa: xp 10, oro 10
```

#### Escena
Nima pide la ficha de **Vega**, la estrella más brillante de la Lira. Rigel la busca en el catálogo. Después, Gheco pide una que no existe: **Polar del Sur**.

#### Gheco sugiere
`find` devuelve la ficha o `undefined`. Con `?.` se pide la distancia solo si la encontró, y con `??` se dice qué mostrar si no.

#### Desafío
Completá la búsqueda en `distanciaDe`.

#### Pasos
1. Buscá el `___` en `distanciaDe`.
2. Cambialo por `catalogo.find((e) => e.nombre === nombre)?.distancia ?? 'no está en el catálogo'`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; constelacion: string; brillo: number; distancia: number; tipo: Tipo }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', constelacion: 'Can Mayor', brillo: 10, distancia: 9, tipo: 'enana' },
  { nombre: 'Vega', constelacion: 'Lira', brillo: 8, distancia: 25, tipo: 'enana' },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7, distancia: 860, tipo: 'supergigante' },
];

function distanciaDe(nombre: string): number | string {
  return ___;
}

console.log(`Vega: ${distanciaDe('Vega')}`);
console.log(`Polar del Sur: ${distanciaDe('Polar del Sur')}`);
```

#### Salida esperada
```
Vega: 25
Polar del Sur: no está en el catálogo
```

#### Solución
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; constelacion: string; brillo: number; distancia: number; tipo: Tipo }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', constelacion: 'Can Mayor', brillo: 10, distancia: 9, tipo: 'enana' },
  { nombre: 'Vega', constelacion: 'Lira', brillo: 8, distancia: 25, tipo: 'enana' },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7, distancia: 860, tipo: 'supergigante' },
];

function distanciaDe(nombre: string): number | string {
  return catalogo.find((e) => e.nombre === nombre)?.distancia ?? 'no está en el catálogo';
}

console.log(`Vega: ${distanciaDe('Vega')}`);
console.log(`Polar del Sur: ${distanciaDe('Polar del Sur')}`);
```

#### Al superarla
La ficha de Vega aparece arriba de la pila. Gheco se queda buscando la Polar del Sur debajo de la mesa.

#### Imagen
- Una biblioteca steampunk con estantes de latón y una caja de fichas de cartón abierta sobre la mesa.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) levanta una ficha.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas, arco verde a la espalda) mira por encima del hombro; Gheco revuelve debajo de la mesa.

### Micro-misión S01-N01-P2 · La enana mal escrita

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Nima
criatura: goblin
carta: filter con una unión | porTipo(tipo: Tipo) · 'enano' no es un Tipo · el compilador lo marca
recompensa: xp 10, oro 10
```

#### Escena
Nima quiere separar las estrellas **enanas**. Lo escribió rápido, como en la Feria, y el compilador del Mirador se queja.

#### Gheco sugiere
`porTipo` solo acepta un `Tipo`: `'enana'`, `'gigante'` o `'supergigante'`. Leé el error y corregí la palabra.

#### Desafío
Corregí el tipo mal escrito.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `'enano'` por `'enana'`.
3. Tocá **Ejecutar**. Tiene que salir `Enanas: Sirio, Vega`.

#### Código inicial
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; constelacion: string; brillo: number; distancia: number; tipo: Tipo }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', constelacion: 'Can Mayor', brillo: 10, distancia: 9, tipo: 'enana' },
  { nombre: 'Vega', constelacion: 'Lira', brillo: 8, distancia: 25, tipo: 'enana' },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7, distancia: 860, tipo: 'supergigante' },
  { nombre: 'Arturo', constelacion: 'Boyero', brillo: 9, distancia: 37, tipo: 'gigante' },
];

function porTipo(tipo: Tipo): Estrella[] {
  return catalogo.filter((e) => e.tipo === tipo);
}

const enanas = porTipo('enano');
console.log(`Enanas: ${enanas.map((e) => e.nombre).join(', ')}`);
```

#### Salida esperada
```
Enanas: Sirio, Vega
```

#### Solución
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; constelacion: string; brillo: number; distancia: number; tipo: Tipo }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', constelacion: 'Can Mayor', brillo: 10, distancia: 9, tipo: 'enana' },
  { nombre: 'Vega', constelacion: 'Lira', brillo: 8, distancia: 25, tipo: 'enana' },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7, distancia: 860, tipo: 'supergigante' },
  { nombre: 'Arturo', constelacion: 'Boyero', brillo: 9, distancia: 37, tipo: 'gigante' },
];

function porTipo(tipo: Tipo): Estrella[] {
  return catalogo.filter((e) => e.tipo === tipo);
}

const enanas = porTipo('enana');
console.log(`Enanas: ${enanas.map((e) => e.nombre).join(', ')}`);
```

#### Al superarla
Nima se ríe: —En la Feria, ese error me dejaba la lista vacía y yo no sabía por qué. Acá te lo dice antes.

#### Imagen
- Dos pilas de fichas en la mesa de la biblioteca, una con estrellas chiquitas dibujadas.
- Un goblin chiquito con un engranaje en la espalda escapando con una letra «o».
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) se ríe; Rigel (chico flaco con pecas, antiparras de latón) corrige con un lápiz; Gheco persigue al goblin.

### Micro-misión S01-N01-P3 · ¿Alguna? ¿Todas?

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Astrea
carta: some y every | some: ¿hay alguna? · every: ¿cumplen todas? · las dos dan boolean
recompensa: xp 10, oro 10
```

#### Escena
Astrea revisa el catálogo antes de guardarlo. Tiene dos preguntas: ¿hay **alguna** estrella a menos de 10 años luz? ¿Tienen **todas** un brillo válido (entre 1 y 10)?

#### Gheco sugiere
- `catalogo.some((e) => e.distancia < 10)`: alcanza con una.
- `catalogo.every((e) => e.brillo >= 1 && e.brillo <= 10)`: tienen que cumplir todas.

#### Desafío
Completá las dos preguntas.

#### Pasos
1. El primer `___`: `catalogo.some((e) => e.distancia < 10)`.
2. El segundo `___`: `catalogo.every((e) => e.brillo >= 1 && e.brillo <= 10)`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; constelacion: string; brillo: number; distancia: number; tipo: Tipo }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', constelacion: 'Can Mayor', brillo: 10, distancia: 9, tipo: 'enana' },
  { nombre: 'Vega', constelacion: 'Lira', brillo: 8, distancia: 25, tipo: 'enana' },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7, distancia: 860, tipo: 'supergigante' },
  { nombre: 'Betelgeuse', constelacion: 'Orión', brillo: 12, distancia: 550, tipo: 'supergigante' },
];

const hayCercana: boolean = ___;
const brillosBien: boolean = ___;

console.log(`¿Alguna a menos de 10 años luz? ${hayCercana}`);
console.log(`¿Todos los brillos entre 1 y 10? ${brillosBien}`);
```

#### Salida esperada
```
¿Alguna a menos de 10 años luz? true
¿Todos los brillos entre 1 y 10? false
```

#### Solución
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; constelacion: string; brillo: number; distancia: number; tipo: Tipo }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', constelacion: 'Can Mayor', brillo: 10, distancia: 9, tipo: 'enana' },
  { nombre: 'Vega', constelacion: 'Lira', brillo: 8, distancia: 25, tipo: 'enana' },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7, distancia: 860, tipo: 'supergigante' },
  { nombre: 'Betelgeuse', constelacion: 'Orión', brillo: 12, distancia: 550, tipo: 'supergigante' },
];

const hayCercana: boolean = catalogo.some((e) => e.distancia < 10);
const brillosBien: boolean = catalogo.every((e) => e.brillo >= 1 && e.brillo <= 10);

console.log(`¿Alguna a menos de 10 años luz? ${hayCercana}`);
console.log(`¿Todos los brillos entre 1 y 10? ${brillosBien}`);
```

#### Al superarla
Astrea encuentra la ficha rota: Betelgeuse dice brillo 12. —El tipo dice que es un número, pero no dice cuál —explica—. Eso lo revisa tu programa.

#### Imagen
- Astrea (lechuza con anteojos de latón y chaleco azul) sostiene una ficha con un borde rojo.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mira la ficha con el calibre.
- Gheco sobre la caja de fichas.

### Micro-misión S01-N01-P4 · El buscador con filtros

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Nima
carta: Filtros opcionales | interface Filtro { tipo?: Tipo; brilloMinimo?: number } · si el filtro no está, no filtra · === undefined
recompensa: xp 15, monedas 5
```

#### Escena
Nima quiere un buscador como el del Archivo de Sila: elegir el tipo, el brillo mínimo, o los dos, o ninguno.

#### Gheco sugiere
Cada campo del `Filtro` es opcional. Una estrella pasa si, **para cada filtro**, o el filtro no está, o lo cumple:

```ts
(f.tipo === undefined || e.tipo === f.tipo) && (f.brilloMinimo === undefined || e.brillo >= f.brilloMinimo)
```

#### Desafío
Completá la condición del `filter`.

#### Pasos
1. Buscá el `___` en `buscar`.
2. Cambialo por `(f.tipo === undefined || e.tipo === f.tipo) && (f.brilloMinimo === undefined || e.brillo >= f.brilloMinimo)`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; constelacion: string; brillo: number; distancia: number; tipo: Tipo }
interface Filtro { tipo?: Tipo; brilloMinimo?: number }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', constelacion: 'Can Mayor', brillo: 10, distancia: 9, tipo: 'enana' },
  { nombre: 'Vega', constelacion: 'Lira', brillo: 8, distancia: 25, tipo: 'enana' },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7, distancia: 860, tipo: 'supergigante' },
  { nombre: 'Arturo', constelacion: 'Boyero', brillo: 9, distancia: 37, tipo: 'gigante' },
  { nombre: 'Aldebarán', constelacion: 'Tauro', brillo: 5, distancia: 65, tipo: 'gigante' },
];

function buscar(f: Filtro): string {
  return catalogo.filter((e) => ___).map((e) => e.nombre).join(', ') || '(ninguna)';
}

console.log(buscar({ tipo: 'gigante' }));
console.log(buscar({ brilloMinimo: 8 }));
console.log(buscar({ tipo: 'enana', brilloMinimo: 9 }));
console.log(buscar({ tipo: 'supergigante', brilloMinimo: 9 }));
console.log(buscar({}));
```

#### Salida esperada
```
Arturo, Aldebarán
Sirio, Vega, Arturo
Sirio
(ninguna)
Sirio, Vega, Rigel, Arturo, Aldebarán
```

#### Solución
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; constelacion: string; brillo: number; distancia: number; tipo: Tipo }
interface Filtro { tipo?: Tipo; brilloMinimo?: number }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', constelacion: 'Can Mayor', brillo: 10, distancia: 9, tipo: 'enana' },
  { nombre: 'Vega', constelacion: 'Lira', brillo: 8, distancia: 25, tipo: 'enana' },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7, distancia: 860, tipo: 'supergigante' },
  { nombre: 'Arturo', constelacion: 'Boyero', brillo: 9, distancia: 37, tipo: 'gigante' },
  { nombre: 'Aldebarán', constelacion: 'Tauro', brillo: 5, distancia: 65, tipo: 'gigante' },
];

function buscar(f: Filtro): string {
  return catalogo.filter((e) => (f.tipo === undefined || e.tipo === f.tipo) && (f.brilloMinimo === undefined || e.brillo >= f.brilloMinimo)).map((e) => e.nombre).join(', ') || '(ninguna)';
}

console.log(buscar({ tipo: 'gigante' }));
console.log(buscar({ brilloMinimo: 8 }));
console.log(buscar({ tipo: 'enana', brilloMinimo: 9 }));
console.log(buscar({ tipo: 'supergigante', brilloMinimo: 9 }));
console.log(buscar({}));
```

#### Al superarla
El buscador anda con cualquier combinación. Nima aplaude: —Ese es el del Archivo, pero sin miedo a escribir mal un campo.

#### Imagen
- Una máquina buscadora de latón con dos perillas (una con estrellas de tamaños, otra con un número de brillo) y una ranura que saca fichas.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) gira una perilla; Rigel (chico flaco con pecas, antiparras de latón) recibe las fichas.
- Gheco sentado sobre la máquina.

### Micro-misión S01-N01-P5 · Buscar por cualquier campo

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Astrea
carta: Buscador genérico | buscarPor<K extends keyof Estrella>(campo: K, valor: Estrella[K]) · el valor tiene el tipo del campo
recompensa: xp 15, monedas 5
```

#### Escena
Astrea quiere buscar por **cualquier** campo: por constelación, por tipo, por brillo. Rigel arma un solo buscador que sirva para todos, y que no deje buscar un brillo con letras.

#### Gheco sugiere
`K extends keyof Estrella` es el nombre de un campo. `Estrella[K]` es el tipo de ese campo: si `K` es `'brillo'`, el valor tiene que ser un `number`.

#### Desafío
Completá la firma de `buscarPor`.

#### Pasos
1. Buscá el `___` en la firma.
2. Cambialo por `function buscarPor<K extends keyof Estrella>(campo: K, valor: Estrella[K]): Estrella[]`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; constelacion: string; brillo: number; distancia: number; tipo: Tipo }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', constelacion: 'Can Mayor', brillo: 10, distancia: 9, tipo: 'enana' },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7, distancia: 860, tipo: 'supergigante' },
  { nombre: 'Betelgeuse', constelacion: 'Orión', brillo: 6, distancia: 550, tipo: 'supergigante' },
  { nombre: 'Arturo', constelacion: 'Boyero', brillo: 9, distancia: 37, tipo: 'gigante' },
];

___ {
  return catalogo.filter((e) => e[campo] === valor);
}

const nombres = (lista: Estrella[]) => lista.map((e) => e.nombre).join(', ');
console.log(`Orión: ${nombres(buscarPor('constelacion', 'Orión'))}`);
console.log(`Gigantes: ${nombres(buscarPor('tipo', 'gigante'))}`);
console.log(`Brillo 10: ${nombres(buscarPor('brillo', 10))}`);
```

#### Salida esperada
```
Orión: Rigel, Betelgeuse
Gigantes: Arturo
Brillo 10: Sirio
```

#### Solución
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; constelacion: string; brillo: number; distancia: number; tipo: Tipo }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', constelacion: 'Can Mayor', brillo: 10, distancia: 9, tipo: 'enana' },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7, distancia: 860, tipo: 'supergigante' },
  { nombre: 'Betelgeuse', constelacion: 'Orión', brillo: 6, distancia: 550, tipo: 'supergigante' },
  { nombre: 'Arturo', constelacion: 'Boyero', brillo: 9, distancia: 37, tipo: 'gigante' },
];

function buscarPor<K extends keyof Estrella>(campo: K, valor: Estrella[K]): Estrella[] {
  return catalogo.filter((e) => e[campo] === valor);
}

const nombres = (lista: Estrella[]) => lista.map((e) => e.nombre).join(', ');
console.log(`Orión: ${nombres(buscarPor('constelacion', 'Orión'))}`);
console.log(`Gigantes: ${nombres(buscarPor('tipo', 'gigante'))}`);
console.log(`Brillo 10: ${nombres(buscarPor('brillo', 10))}`);
```

#### Al superarla
Rigel prueba `buscarPor('brillo', 'mucho')` y el compilador lo frena enseguida. Astrea asiente: —Un buscador para todo, y ninguna búsqueda imposible.

#### Imagen
- Un fichero de latón con cajones rotulados con íconos (estrella, constelación, número).
- Astrea (lechuza con anteojos de latón y chaleco azul) abre un cajón con el ala.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sostiene tres fichas; Gheco asoma de un cajón.

## S01-N02 · Ordenar el Catálogo

```meta
tipo: tema
padre: S01-N01
precio: 10
criatura: orc
temas: alg.ordenamiento
usa: col.arrays, poo.genericos, cal.tipos
```

### Crónica

Las fichas ya se encuentran, pero siguen en desorden. Nima quiere verlas de la más brillante a la menos brillante. Astrea prefiere por nombre, como en un diccionario. Y Don Péndulo, que sube a la biblioteca con su lupa, pide por distancia: *—El Vidriero siempre las tenía de la más cercana a la más lejana. Decía que así se entendía el cielo.*

### Objetivos

- Ordenar con `sort` y una función que compara.
- Ordenar texto con `localeCompare` (acentos y mayúsculas).
- Ordenar sin cambiar la lista original: `toSorted` y los arreglos `readonly`.
- Escribir un `ordenarPor` genérico y ordenar por dos criterios.

### Antes de empezar

- S01-N01: el catálogo y sus tipos.

### Explicación

#### La función que compara
```typescript
lista.sort((a, b) => a.brillo - b.brillo);   // de menor a mayor
lista.sort((a, b) => b.brillo - a.brillo);   // de mayor a menor
```
Si da negativo, `a` va antes; si da positivo, va después; si da 0, quedan como estaban.

#### Ordenar palabras
`'Á'` y `'a'` no se ordenan bien con `<`. Para texto se usa `a.nombre.localeCompare(b.nombre, 'es')`.

#### `sort` cambia la lista
`sort` **reordena el arreglo original**. Si la lista es `readonly`, TypeScript no deja usarlo. `toSorted` devuelve una lista nueva y deja la original como estaba.

#### Un `ordenarPor` para cualquier lista
```typescript
function ordenarPor<T, K extends keyof T>(lista: readonly T[], campo: K): T[] {
  return lista.toSorted((a, b) => (a[campo] < b[campo] ? -1 : a[campo] > b[campo] ? 1 : 0));
}
```

### Código de ejemplo

```typescript
const brillos: readonly number[] = [7, 10, 5, 9];
const ordenados = brillos.toSorted((a, b) => b - a);
console.log(ordenados.join(' '), '·', brillos.join(' '));
console.log(['Vega', 'Aldebarán', 'arturo'].toSorted((a, b) => a.localeCompare(b, 'es')).join(', '));
```

### Salida esperada

```
10 9 7 5 · 7 10 5 9
Aldebarán, arturo, Vega
```

### ¿Para qué sirve?

Toda tabla que ves en una página (precios, posiciones de un ranking, archivos) tiene un orden. Saber ordenar sin romper la lista original evita errores que aparecen lejos de donde se cometieron.

### Errores habituales

**Orco: el orden al revés.** `a - b` es de menor a mayor; `b - a`, de mayor a menor.

**Goblin: ordenar números como texto.** `[10, 9, 5].sort()` da `[10, 5, 9]`: sin función, `sort` compara como texto.

**Ogro: `sort` que cambia la lista de otro.** Si la lista es compartida, otro lugar del programa la ve cambiada. Con `readonly` y `toSorted`, no pasa.

### Micro-misión S01-N02-P1 · Las tres más brillantes

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Nima
carta: sort con comparador | (a, b) => b.brillo - a.brillo · de mayor a menor · slice(0, 3) se queda con las primeras
recompensa: xp 10, oro 10
```

#### Escena
Nima quiere las tres estrellas más brillantes del catálogo para pintarlas en su arco.

#### Gheco sugiere
`b.brillo - a.brillo` ordena de mayor a menor. Después, `slice(0, 3)` se queda con las tres primeras.

#### Desafío
Completá la función que compara.

#### Pasos
1. Buscá el `___` en el `sort`.
2. Cambialo por `(a, b) => b.brillo - a.brillo`.
3. Tocá **Ejecutar**. Tiene que salir `Sirio (10), Arturo (9), Vega (8)`.

#### Código inicial
```typescript
interface Estrella { nombre: string; brillo: number }

const catalogo: Estrella[] = [
  { nombre: 'Rigel', brillo: 7 },
  { nombre: 'Sirio', brillo: 10 },
  { nombre: 'Aldebarán', brillo: 5 },
  { nombre: 'Vega', brillo: 8 },
  { nombre: 'Arturo', brillo: 9 },
];

const top = catalogo.sort(___).slice(0, 3);
console.log(top.map((e) => `${e.nombre} (${e.brillo})`).join(', '));
```

#### Salida esperada
```
Sirio (10), Arturo (9), Vega (8)
```

#### Solución
```typescript
interface Estrella { nombre: string; brillo: number }

const catalogo: Estrella[] = [
  { nombre: 'Rigel', brillo: 7 },
  { nombre: 'Sirio', brillo: 10 },
  { nombre: 'Aldebarán', brillo: 5 },
  { nombre: 'Vega', brillo: 8 },
  { nombre: 'Arturo', brillo: 9 },
];

const top = catalogo.sort((a, b) => b.brillo - a.brillo).slice(0, 3);
console.log(top.map((e) => `${e.nombre} (${e.brillo})`).join(', '));
```

#### Al superarla
Nima pinta tres estrellas en su arco: Sirio, Arturo y Vega.

#### Imagen
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) pinta tres estrellas doradas en su arco verde.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sostiene tres fichas en abanico.
- Gheco mira la pintura muy de cerca.

### Micro-misión S01-N02-P2 · Como en el diccionario

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Astrea
criatura: orc
carta: Ordenar texto | a.localeCompare(b, 'es') · acentos y mayúsculas en su lugar · sort() solo no sirve
recompensa: xp 10, oro 10
```

#### Escena
Astrea ordena por nombre con `sort()` sin nada, y la **Á** de Ámbar queda al final, después de Vega. Además, una ficha escrita en minúscula se va al fondo.

#### Gheco sugiere
`sort()` sin función compara los códigos de las letras: las mayúsculas van antes que las minúsculas, y las letras con acento, al final. `localeCompare(…, 'es')` ordena como un diccionario en español.

#### Desafío
Ordená con `localeCompare`.

#### Pasos
1. Tocá **Ejecutar** y mirá el orden.
2. Cambiá `nombres.toSorted()` por `nombres.toSorted((a, b) => a.localeCompare(b, 'es'))`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
const nombres: readonly string[] = ['Vega', 'Ámbar', 'sirio', 'Arturo', 'Rigel'];
console.log(nombres.toSorted().join(', '));
```

#### Salida esperada
```
Ámbar, Arturo, Rigel, sirio, Vega
```

#### Solución
```typescript
const nombres: readonly string[] = ['Vega', 'Ámbar', 'sirio', 'Arturo', 'Rigel'];
console.log(nombres.toSorted((a, b) => a.localeCompare(b, 'es')).join(', '));
```

#### Al superarla
Ámbar vuelve a su lugar, al principio. Astrea guarda las fichas en el fichero, de la A a la Z.

#### Imagen
- Un fichero de latón con letras grabadas en los cajones, de la A a la Z.
- Un orco chiquito de cuerda que había metido una ficha con «Á» en el último cajón.
- Astrea (lechuza con anteojos de latón y chaleco azul) la saca con el ala; Rigel (chico flaco con pecas, antiparras de latón) y Gheco miran.

### Micro-misión S01-N02-P3 · La lista que no se toca

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Don Péndulo
criatura: ogre
carta: readonly y toSorted | sort cambia la lista · en un readonly no existe (TS2339) · toSorted da una lista nueva
recompensa: xp 10, oro 10
```

#### Escena
Don Péndulo guarda el catálogo **original** del Vidriero, en el orden en que él lo escribió. Lo marcó `readonly` para que nadie lo cambie. Rigel quiere una copia ordenada por distancia.

#### Gheco sugiere
`sort` cambia el arreglo; por eso no existe en un `readonly`. `toSorted` hace lo mismo pero devuelve una lista nueva, y deja la original intacta.

#### Desafío
Ordená sin tocar el catálogo original.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `catalogo.sort(` por `catalogo.toSorted(`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Estrella { nombre: string; distancia: number }

const catalogo: readonly Estrella[] = [
  { nombre: 'Rigel', distancia: 860 },
  { nombre: 'Sirio', distancia: 9 },
  { nombre: 'Arturo', distancia: 37 },
];

const porDistancia = catalogo.sort((a, b) => a.distancia - b.distancia);
console.log(`Ordenado: ${porDistancia.map((e) => e.nombre).join(', ')}`);
console.log(`Original: ${catalogo.map((e) => e.nombre).join(', ')}`);
```

#### Salida esperada
```
Ordenado: Sirio, Arturo, Rigel
Original: Rigel, Sirio, Arturo
```

#### Solución
```typescript
interface Estrella { nombre: string; distancia: number }

const catalogo: readonly Estrella[] = [
  { nombre: 'Rigel', distancia: 860 },
  { nombre: 'Sirio', distancia: 9 },
  { nombre: 'Arturo', distancia: 37 },
];

const porDistancia = catalogo.toSorted((a, b) => a.distancia - b.distancia);
console.log(`Ordenado: ${porDistancia.map((e) => e.nombre).join(', ')}`);
console.log(`Original: ${catalogo.map((e) => e.nombre).join(', ')}`);
```

#### Al superarla
Don Péndulo sonríe debajo de la barba: —Así lo tenía el Vidriero. Y el original, como él lo dejó.

#### Imagen
- Un libro antiguo con candado de latón (el catálogo original) junto a una pila de fichas nueva y ordenada.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa de relojero en un ojo) cuida el libro.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) acomoda la pila nueva; Gheco sobre el candado.

### Micro-misión S01-N02-P4 · Ordenar por cualquier campo

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Astrea
carta: ordenarPor genérico | <T, K extends keyof T> · compara a[campo] con b[campo] · sentido 'asc' | 'desc'
recompensa: xp 15, monedas 5
```

#### Escena
Cada uno quiere un orden distinto. Rigel arma una sola función que ordena **cualquier lista por cualquier campo**, para un lado o para el otro.

#### Gheco sugiere
`K extends keyof T`: el campo tiene que existir en lo que se ordena. Para comparar: si `a[campo] < b[campo]`, va `-1`; si es mayor, `1`; si son iguales, `0`. Para el sentido contrario, se da vuelta el signo.

#### Desafío
Completá la línea que compara.

#### Pasos
1. Buscá el `___` en `ordenarPor`.
2. Cambialo por `const orden = a[campo] < b[campo] ? -1 : a[campo] > b[campo] ? 1 : 0;`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Estrella { nombre: string; brillo: number; distancia: number }

function ordenarPor<T, K extends keyof T>(lista: readonly T[], campo: K, sentido: 'asc' | 'desc' = 'asc'): T[] {
  return lista.toSorted((a, b) => {
    ___
    return sentido === 'asc' ? orden : -orden;
  });
}

const catalogo: readonly Estrella[] = [
  { nombre: 'Vega', brillo: 8, distancia: 25 },
  { nombre: 'Arturo', brillo: 9, distancia: 37 },
  { nombre: 'Rigel', brillo: 7, distancia: 860 },
];
const nombres = (l: Estrella[]) => l.map((e) => e.nombre).join(', ');

console.log(nombres(ordenarPor(catalogo, 'nombre')));
console.log(nombres(ordenarPor(catalogo, 'brillo', 'desc')));
console.log(nombres(ordenarPor(catalogo, 'distancia')));
```

#### Salida esperada
```
Arturo, Rigel, Vega
Arturo, Vega, Rigel
Vega, Arturo, Rigel
```

#### Solución
```typescript
interface Estrella { nombre: string; brillo: number; distancia: number }

function ordenarPor<T, K extends keyof T>(lista: readonly T[], campo: K, sentido: 'asc' | 'desc' = 'asc'): T[] {
  return lista.toSorted((a, b) => {
    const orden = a[campo] < b[campo] ? -1 : a[campo] > b[campo] ? 1 : 0;
    return sentido === 'asc' ? orden : -orden;
  });
}

const catalogo: readonly Estrella[] = [
  { nombre: 'Vega', brillo: 8, distancia: 25 },
  { nombre: 'Arturo', brillo: 9, distancia: 37 },
  { nombre: 'Rigel', brillo: 7, distancia: 860 },
];
const nombres = (l: Estrella[]) => l.map((e) => e.nombre).join(', ');

console.log(nombres(ordenarPor(catalogo, 'nombre')));
console.log(nombres(ordenarPor(catalogo, 'brillo', 'desc')));
console.log(nombres(ordenarPor(catalogo, 'distancia')));
```

#### Al superarla
Rigel prueba `ordenarPor(catalogo, 'color')` y el compilador dice que ese campo no existe. Astrea anota la función en el Atlas: le va a servir para cualquier lista del Mirador.

#### Imagen
- Una máquina de latón con una palanca de sentido (flecha arriba, flecha abajo) y un selector con íconos de campos.
- Astrea (lechuza con anteojos de latón y chaleco azul) anota en un cuaderno.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mueve la palanca; Gheco montado en la palanca.

### Micro-misión S01-N02-P5 · Dos criterios

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Don Péndulo
carta: Ordenar por dos criterios | primero el tipo (con un Record de orden) · si empatan, el brillo · el || pasa al segundo
recompensa: xp 15, monedas 5
```

#### Escena
Don Péndulo quiere el catálogo como lo tenía el Vidriero: primero las enanas, después las gigantes, después las supergigantes; y adentro de cada grupo, de la más brillante a la menos.

#### Gheco sugiere
- Un `Record<Tipo, number>` dice en qué lugar va cada tipo: `{ enana: 1, gigante: 2, supergigante: 3 }`.
- Si dos estrellas tienen el mismo tipo, la resta da `0`, y `||` pasa al segundo criterio:

```ts
ORDEN[a.tipo] - ORDEN[b.tipo] || b.brillo - a.brillo
```

#### Desafío
Completá la función que compara.

#### Pasos
1. Buscá el `___` en el `toSorted`.
2. Cambialo por `ORDEN[a.tipo] - ORDEN[b.tipo] || b.brillo - a.brillo`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; brillo: number; tipo: Tipo }

const ORDEN: Record<Tipo, number> = { enana: 1, gigante: 2, supergigante: 3 };

const catalogo: readonly Estrella[] = [
  { nombre: 'Rigel', brillo: 7, tipo: 'supergigante' },
  { nombre: 'Vega', brillo: 8, tipo: 'enana' },
  { nombre: 'Aldebarán', brillo: 5, tipo: 'gigante' },
  { nombre: 'Sirio', brillo: 10, tipo: 'enana' },
  { nombre: 'Betelgeuse', brillo: 6, tipo: 'supergigante' },
  { nombre: 'Arturo', brillo: 9, tipo: 'gigante' },
];

const ordenado = catalogo.toSorted((a, b) => ___);
for (const e of ordenado) console.log(`${e.tipo.padEnd(12)} ${e.brillo} ${e.nombre}`);
```

#### Salida esperada
```
enana        10 Sirio
enana        8 Vega
gigante      9 Arturo
gigante      5 Aldebarán
supergigante 7 Rigel
supergigante 6 Betelgeuse
```

#### Solución
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; brillo: number; tipo: Tipo }

const ORDEN: Record<Tipo, number> = { enana: 1, gigante: 2, supergigante: 3 };

const catalogo: readonly Estrella[] = [
  { nombre: 'Rigel', brillo: 7, tipo: 'supergigante' },
  { nombre: 'Vega', brillo: 8, tipo: 'enana' },
  { nombre: 'Aldebarán', brillo: 5, tipo: 'gigante' },
  { nombre: 'Sirio', brillo: 10, tipo: 'enana' },
  { nombre: 'Betelgeuse', brillo: 6, tipo: 'supergigante' },
  { nombre: 'Arturo', brillo: 9, tipo: 'gigante' },
];

const ordenado = catalogo.toSorted((a, b) => ORDEN[a.tipo] - ORDEN[b.tipo] || b.brillo - a.brillo);
for (const e of ordenado) console.log(`${e.tipo.padEnd(12)} ${e.brillo} ${e.nombre}`);
```

#### Al superarla
Don Péndulo pasa el dedo por la lista y asiente despacio. —Igualito. Así lo leía él, de noche, en voz alta.

#### Imagen
- Tres cajones de latón de tamaños distintos (chico, mediano, grande), cada uno con fichas ordenadas adentro.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa en un ojo) lee una ficha con la lupa.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) le alcanza otra; Gheco duerme en el cajón chico.

## S01-N03 · Agrupar y contar

```meta
tipo: tema
padre: S01-N02
precio: 10
criatura: troll
temas: col.mapas
usa: col.arrays, func.orden-superior, poo.genericos, cal.tipos
```

### Crónica

Astrea quiere un **resumen** del catálogo para el Atlas: cuántas estrellas hay de cada tipo, la distancia promedio, y qué estrellas tiene cada constelación. Nima se acuerda de que en la Feria Sila hacía eso con planillas de papel, y tardaba una semana.

—Con `reduce` y un `Map` se hace en un rato —dice Gheco—. Y con tipos, sin perder ningún grupo.

### Objetivos

- Contar por grupo con un `Record<Tipo, number>`.
- Acumular con `reduce` (sumas y promedios).
- Agrupar con un `Map<string, Estrella[]>`.
- Escribir un `agruparPor` genérico y encontrar la más brillante de cada grupo.

### Antes de empezar

- S01-N01 y S01-N02.
- `Record` (R03-N04) y los genéricos (R02-N06).

### Explicación

#### Contar con un `Record`
```typescript
const cuenta: Record<Tipo, number> = { enana: 0, gigante: 0, supergigante: 0 };
for (const e of catalogo) cuenta[e.tipo]++;
```
Si te olvidás de un tipo al crear el objeto, el compilador avisa: el `Record` exige todos.

#### Acumular con `reduce`
```typescript
const total = catalogo.reduce((suma, e) => suma + e.distancia, 0);
```
El segundo argumento (`0`) es el valor inicial, y le da el tipo a `suma`.

#### Agrupar con un `Map`
```typescript
const porConstelacion = new Map<string, Estrella[]>();
for (const e of catalogo) {
  const grupo = porConstelacion.get(e.constelacion) ?? [];
  grupo.push(e);
  porConstelacion.set(e.constelacion, grupo);
}
```

### Código de ejemplo

```typescript
type Tipo = 'enana' | 'gigante';
const tipos: Tipo[] = ['enana', 'gigante', 'enana'];
const cuenta: Record<Tipo, number> = { enana: 0, gigante: 0 };
for (const t of tipos) cuenta[t]++;
console.log(cuenta);
console.log([9, 25, 37].reduce((suma, d) => suma + d, 0));
```

### Salida esperada

```
{ enana: 2, gigante: 1 }
71
```

### ¿Para qué sirve?

Los informes, los tableros con números y los gráficos salen de agrupar y contar. Es lo que hace una planilla de cálculo, pero con tu propio programa.

### Errores habituales

**Troll: `reduce` sin valor inicial.** En una lista vacía explota, y el tipo del acumulador queda mal. Siempre se le da el valor inicial.

**Esqueleto: un grupo que no existe todavía.** `mapa.get(clave)` puede dar `undefined`: `?? []` arranca uno nuevo.

**Goblin: el `Record` incompleto.** Si falta un tipo al crearlo, TS2741 te dice cuál.

### Micro-misión S01-N03-P1 · Cuántas de cada tipo

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Astrea
carta: Contar con Record | Record<Tipo, number> con todos en 0 · cuenta[e.tipo]++ · no se pierde ningún tipo
recompensa: xp 10, oro 10
```

#### Escena
Astrea quiere saber cuántas estrellas hay de cada tipo.

#### Gheco sugiere
El `Record<Tipo, number>` arranca con todos los tipos en 0. Para cada estrella, se suma uno en su tipo: `cuenta[e.tipo]++`.

#### Desafío
Completá la línea que cuenta.

#### Pasos
1. Buscá el `___` adentro del `for`.
2. Cambialo por `cuenta[e.tipo]++;`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; tipo: Tipo }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', tipo: 'enana' },
  { nombre: 'Vega', tipo: 'enana' },
  { nombre: 'Rigel', tipo: 'supergigante' },
  { nombre: 'Arturo', tipo: 'gigante' },
  { nombre: 'Betelgeuse', tipo: 'supergigante' },
  { nombre: 'Proción', tipo: 'enana' },
];

const cuenta: Record<Tipo, number> = { enana: 0, gigante: 0, supergigante: 0 };
for (const e of catalogo) {
  ___
}

for (const [tipo, cantidad] of Object.entries(cuenta)) console.log(`${tipo}: ${cantidad}`);
```

#### Salida esperada
```
enana: 3
gigante: 1
supergigante: 2
```

#### Solución
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; tipo: Tipo }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', tipo: 'enana' },
  { nombre: 'Vega', tipo: 'enana' },
  { nombre: 'Rigel', tipo: 'supergigante' },
  { nombre: 'Arturo', tipo: 'gigante' },
  { nombre: 'Betelgeuse', tipo: 'supergigante' },
  { nombre: 'Proción', tipo: 'enana' },
];

const cuenta: Record<Tipo, number> = { enana: 0, gigante: 0, supergigante: 0 };
for (const e of catalogo) {
  cuenta[e.tipo]++;
}

for (const [tipo, cantidad] of Object.entries(cuenta)) console.log(`${tipo}: ${cantidad}`);
```

#### Al superarla
Astrea escribe los tres números en el Atlas, con letra prolija.

#### Imagen
- Tres frascos de vidrio con estrellitas adentro (muchas, una, dos), con etiquetas de latón.
- Astrea (lechuza con anteojos de latón y chaleco azul) escribe en el Atlas.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) pone una estrellita en un frasco; Gheco cuenta con los dedos.

### Micro-misión S01-N03-P2 · El promedio de las distancias

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Nima
criatura: troll
carta: reduce con valor inicial | lista.reduce((suma, e) => suma + e.distancia, 0) · sin el 0, una lista vacía explota
recompensa: xp 10, oro 10
```

#### Escena
Nima pregunta qué tan lejos están, en promedio, las estrellas de cada caja. Una de las cajas está **vacía**.

#### Gheco sugiere
`reduce` con valor inicial `0` suma las distancias; en una lista vacía da `0` sin explotar. Para el promedio, se divide por la cantidad, pero solo si hay alguna.

#### Desafío
Completá la suma con `reduce`.

#### Pasos
1. Buscá el `___` en `promedio`.
2. Cambialo por `lista.reduce((suma, e) => suma + e.distancia, 0)`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Estrella { nombre: string; distancia: number }

function promedio(lista: Estrella[]): string {
  const total: number = ___;
  return lista.length === 0 ? 'caja vacía' : `${(total / lista.length).toFixed(1)} años luz`;
}

const cercanas: Estrella[] = [{ nombre: 'Sirio', distancia: 9 }, { nombre: 'Vega', distancia: 25 }, { nombre: 'Arturo', distancia: 37 }];
const lejanas: Estrella[] = [{ nombre: 'Rigel', distancia: 860 }, { nombre: 'Betelgeuse', distancia: 550 }];
const perdidas: Estrella[] = [];

console.log(`Cercanas: ${promedio(cercanas)}`);
console.log(`Lejanas: ${promedio(lejanas)}`);
console.log(`Perdidas: ${promedio(perdidas)}`);
```

#### Salida esperada
```
Cercanas: 23.7 años luz
Lejanas: 705.0 años luz
Perdidas: caja vacía
```

#### Solución
```typescript
interface Estrella { nombre: string; distancia: number }

function promedio(lista: Estrella[]): string {
  const total: number = lista.reduce((suma, e) => suma + e.distancia, 0);
  return lista.length === 0 ? 'caja vacía' : `${(total / lista.length).toFixed(1)} años luz`;
}

const cercanas: Estrella[] = [{ nombre: 'Sirio', distancia: 9 }, { nombre: 'Vega', distancia: 25 }, { nombre: 'Arturo', distancia: 37 }];
const lejanas: Estrella[] = [{ nombre: 'Rigel', distancia: 860 }, { nombre: 'Betelgeuse', distancia: 550 }];
const perdidas: Estrella[] = [];

console.log(`Cercanas: ${promedio(cercanas)}`);
console.log(`Lejanas: ${promedio(lejanas)}`);
console.log(`Perdidas: ${promedio(perdidas)}`);
```

#### Al superarla
Nima silba: —¡Setecientos años luz! La luz que vemos de Rigel salió antes de que existiera la Feria.

#### Imagen
- Tres cajas de fichas: una llena de estrellas cercanas, una con dos estrellas lejanas, una vacía con telarañas.
- Un troll de cuerda dormido adentro de la caja vacía.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) mira la caja vacía; Rigel (chico flaco con pecas, antiparras de latón) hace la cuenta; Gheco tapa la caja del troll.

### Micro-misión S01-N03-P3 · Las constelaciones

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Astrea
carta: Agrupar con Map | Map<string, Estrella[]> · get(clave) ?? [] · push y set
recompensa: xp 10, oro 10
```

#### Escena
Astrea quiere ver qué estrellas tiene cada constelación, en el orden en que aparecen.

#### Gheco sugiere
Para cada estrella: se busca su grupo en el `Map` (o se arranca uno vacío con `?? []`), se agrega la estrella, y se guarda el grupo.

#### Desafío
Completá la línea que busca el grupo.

#### Pasos
1. Buscá el `___` en el `for`.
2. Cambialo por `const grupo = porConstelacion.get(e.constelacion) ?? [];`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Estrella { nombre: string; constelacion: string }

const catalogo: Estrella[] = [
  { nombre: 'Rigel', constelacion: 'Orión' },
  { nombre: 'Vega', constelacion: 'Lira' },
  { nombre: 'Betelgeuse', constelacion: 'Orión' },
  { nombre: 'Aldebarán', constelacion: 'Tauro' },
  { nombre: 'Bellatrix', constelacion: 'Orión' },
  { nombre: 'Sheliak', constelacion: 'Lira' },
];

const porConstelacion = new Map<string, Estrella[]>();
for (const e of catalogo) {
  ___
  grupo.push(e);
  porConstelacion.set(e.constelacion, grupo);
}

for (const [constelacion, estrellas] of porConstelacion) {
  console.log(`${constelacion}: ${estrellas.map((e) => e.nombre).join(', ')}`);
}
```

#### Salida esperada
```
Orión: Rigel, Betelgeuse, Bellatrix
Lira: Vega, Sheliak
Tauro: Aldebarán
```

#### Solución
```typescript
interface Estrella { nombre: string; constelacion: string }

const catalogo: Estrella[] = [
  { nombre: 'Rigel', constelacion: 'Orión' },
  { nombre: 'Vega', constelacion: 'Lira' },
  { nombre: 'Betelgeuse', constelacion: 'Orión' },
  { nombre: 'Aldebarán', constelacion: 'Tauro' },
  { nombre: 'Bellatrix', constelacion: 'Orión' },
  { nombre: 'Sheliak', constelacion: 'Lira' },
];

const porConstelacion = new Map<string, Estrella[]>();
for (const e of catalogo) {
  const grupo = porConstelacion.get(e.constelacion) ?? [];
  grupo.push(e);
  porConstelacion.set(e.constelacion, grupo);
}

for (const [constelacion, estrellas] of porConstelacion) {
  console.log(`${constelacion}: ${estrellas.map((e) => e.nombre).join(', ')}`);
}
```

#### Al superarla
Sobre la mesa quedan tres montoncitos. Astrea los une con hilos de latón: son las constelaciones.

#### Imagen
- Tres montoncitos de fichas unidas con hilos de latón en forma de constelación.
- Astrea (lechuza con anteojos de latón y chaleco azul) tiende un hilo con el pico.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sostiene la ficha de Rigel con una sonrisa; Gheco enredado en un hilo.

### Micro-misión S01-N03-P4 · Agrupar cualquier cosa

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Nima
carta: agruparPor genérico | <T, K> · clave: (x: T) => K · devuelve Map<K, T[]> · sirve para estrellas y para flechas
recompensa: xp 15, monedas 5
```

#### Escena
Nima quiere agrupar las flechas de su carcaj por color, igual que las estrellas por constelación. Rigel generaliza: una función que agrupa **cualquier lista** por **cualquier clave**.

#### Gheco sugiere
`T` es lo que se agrupa y `K`, el tipo de la clave. La función `clave` dice, para cada elemento, en qué grupo va. El resultado es un `Map<K, T[]>`.

#### Desafío
Completá la firma de `agruparPor`.

#### Pasos
1. Buscá el `___` en la firma.
2. Cambialo por `function agruparPor<T, K>(lista: readonly T[], clave: (x: T) => K): Map<K, T[]>`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
___ {
  const grupos = new Map<K, T[]>();
  for (const x of lista) {
    const k = clave(x);
    const grupo = grupos.get(k) ?? [];
    grupo.push(x);
    grupos.set(k, grupo);
  }
  return grupos;
}

interface Estrella { nombre: string; brillo: number }
interface Flecha { color: 'roja' | 'verde' | 'azul'; largo: number }

const estrellas: Estrella[] = [{ nombre: 'Sirio', brillo: 10 }, { nombre: 'Rigel', brillo: 7 }, { nombre: 'Arturo', brillo: 9 }];
const flechas: Flecha[] = [{ color: 'roja', largo: 70 }, { color: 'verde', largo: 75 }, { color: 'roja', largo: 72 }];

const porBrillo = agruparPor(estrellas, (e) => (e.brillo >= 9 ? 'brillantes' : 'tenues'));
const porColor = agruparPor(flechas, (f) => f.color);

for (const [k, v] of porBrillo) console.log(`${k}: ${v.map((e) => e.nombre).join(', ')}`);
for (const [k, v] of porColor) console.log(`${k}: ${v.length} flechas`);
```

#### Salida esperada
```
brillantes: Sirio, Arturo
tenues: Rigel
roja: 2 flechas
verde: 1 flechas
```

#### Solución
```typescript
function agruparPor<T, K>(lista: readonly T[], clave: (x: T) => K): Map<K, T[]> {
  const grupos = new Map<K, T[]>();
  for (const x of lista) {
    const k = clave(x);
    const grupo = grupos.get(k) ?? [];
    grupo.push(x);
    grupos.set(k, grupo);
  }
  return grupos;
}

interface Estrella { nombre: string; brillo: number }
interface Flecha { color: 'roja' | 'verde' | 'azul'; largo: number }

const estrellas: Estrella[] = [{ nombre: 'Sirio', brillo: 10 }, { nombre: 'Rigel', brillo: 7 }, { nombre: 'Arturo', brillo: 9 }];
const flechas: Flecha[] = [{ color: 'roja', largo: 70 }, { color: 'verde', largo: 75 }, { color: 'roja', largo: 72 }];

const porBrillo = agruparPor(estrellas, (e) => (e.brillo >= 9 ? 'brillantes' : 'tenues'));
const porColor = agruparPor(flechas, (f) => f.color);

for (const [k, v] of porBrillo) console.log(`${k}: ${v.map((e) => e.nombre).join(', ')}`);
for (const [k, v] of porColor) console.log(`${k}: ${v.length} flechas`);
```

#### Al superarla
Nima ordena su carcaj por colores. —La voy a llevar a la Feria —dice—. Sila la va a querer para el Archivo.

#### Imagen
- Un carcaj abierto con flechas agrupadas por color (rojas, verdes) al lado de fichas de estrellas en dos montones.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) separa flechas.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) separa fichas; Gheco con una flecha en la mano como si fuera una lanza.

### Micro-misión S01-N03-P5 · La reina de cada constelación

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Astrea
carta: Agrupar y elegir | agruparPor por constelación · en cada grupo, reduce se queda con la de más brillo
recompensa: xp 15, monedas 5
```

#### Escena
En los mapas del Vidriero, cada constelación tiene su estrella principal, la más brillante, dibujada más grande. Astrea quiere esa lista para el Atlas.

#### Gheco sugiere
Primero se agrupa por constelación. Después, en cada grupo, `reduce` compara de a dos y se queda con la más brillante:

```ts
grupo.reduce((mejor, e) => (e.brillo > mejor.brillo ? e : mejor))
```

Acá no hace falta valor inicial: ningún grupo está vacío (si existe, tiene al menos una).

#### Desafío
Completá el `reduce`.

#### Pasos
1. Buscá el `___` en el `for`.
2. Cambialo por `grupo.reduce((mejor, e) => (e.brillo > mejor.brillo ? e : mejor))`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
function agruparPor<T, K>(lista: readonly T[], clave: (x: T) => K): Map<K, T[]> {
  const grupos = new Map<K, T[]>();
  for (const x of lista) {
    const grupo = grupos.get(clave(x)) ?? [];
    grupo.push(x);
    grupos.set(clave(x), grupo);
  }
  return grupos;
}

interface Estrella { nombre: string; constelacion: string; brillo: number }

const catalogo: Estrella[] = [
  { nombre: 'Betelgeuse', constelacion: 'Orión', brillo: 6 },
  { nombre: 'Vega', constelacion: 'Lira', brillo: 8 },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7 },
  { nombre: 'Sheliak', constelacion: 'Lira', brillo: 3 },
  { nombre: 'Bellatrix', constelacion: 'Orión', brillo: 5 },
  { nombre: 'Aldebarán', constelacion: 'Tauro', brillo: 5 },
];

for (const [constelacion, grupo] of agruparPor(catalogo, (e) => e.constelacion)) {
  const reina: Estrella = ___;
  console.log(`${constelacion}: ${reina.nombre} (${reina.brillo})`);
}
```

#### Salida esperada
```
Orión: Rigel (7)
Lira: Vega (8)
Tauro: Aldebarán (5)
```

#### Solución
```typescript
function agruparPor<T, K>(lista: readonly T[], clave: (x: T) => K): Map<K, T[]> {
  const grupos = new Map<K, T[]>();
  for (const x of lista) {
    const grupo = grupos.get(clave(x)) ?? [];
    grupo.push(x);
    grupos.set(clave(x), grupo);
  }
  return grupos;
}

interface Estrella { nombre: string; constelacion: string; brillo: number }

const catalogo: Estrella[] = [
  { nombre: 'Betelgeuse', constelacion: 'Orión', brillo: 6 },
  { nombre: 'Vega', constelacion: 'Lira', brillo: 8 },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7 },
  { nombre: 'Sheliak', constelacion: 'Lira', brillo: 3 },
  { nombre: 'Bellatrix', constelacion: 'Orión', brillo: 5 },
  { nombre: 'Aldebarán', constelacion: 'Tauro', brillo: 5 },
];

for (const [constelacion, grupo] of agruparPor(catalogo, (e) => e.constelacion)) {
  const reina: Estrella = grupo.reduce((mejor, e) => (e.brillo > mejor.brillo ? e : mejor));
  console.log(`${constelacion}: ${reina.nombre} (${reina.brillo})`);
}
```

#### Al superarla
Rigel es la reina de Orión. Gheco no para de repetirlo en voz alta, y Rigel se pone colorado.

#### Imagen
- Un mapa del cielo en papel antiguo con tres constelaciones dibujadas y una estrella más grande en cada una.
- Astrea (lechuza con anteojos de latón y chaleco azul) dibuja con una pluma.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) colorado de vergüenza; Gheco señala la estrella grande de Orión y se ríe.

## S01-N04 · Jefe: la Polilla de Bronce

```meta
tipo: jefe
padre: S01-N03
precio: 10
criatura: dragon
insignia: Sello del Catálogo
insignia_descripcion: Salvaste el Catálogo de Estrellas de la Polilla de Bronce: buscar, ordenar, agrupar y mostrar datos, con sus tipos.
usa: alg.busqueda, alg.ordenamiento, col.mapas, poo.genericos, err.validacion, js.dom, js.formularios
```

### Crónica

Esa noche, en la biblioteca, se oye un aleteo metálico. De adentro de la caja de fichas sale una **polilla de bronce** del tamaño de un gato, con alas de engranajes. Es un autómata viejo del Vidriero que se quedó encerrado: **se alimenta de fichas**. Mastica algunas, mezcla otras y deja pedazos sueltos por todas partes.

—¡La Polilla de Bronce! —dice Don Péndulo—. El Vidriero la hizo para limpiar el polvo de los estantes, pero se le descompuso el apetito.

Nima tensa el arco, pero Astrea la frena: —Con flechas no. Si el catálogo queda en orden, la Polilla no tiene nada que comer.

### Objetivos

- Repasar toda la Senda: buscar, filtrar, ordenar, agrupar.
- Paginar una lista con un genérico.
- Limpiar datos rotos con un guardia de tipo.
- Mostrar el catálogo en una página que busca mientras se escribe.

### Antes de empezar

- Toda la Senda del Catálogo (S01-N01 a N03).
- Los guardias propios (R03-N03) y la página tipada (R04-N04).

### Explicación

#### Paginar
```typescript
interface Pagina<T> { datos: T[]; pagina: number; paginas: number }

function paginar<T>(lista: readonly T[], pagina: number, porPagina: number): Pagina<T> {
  const paginas = Math.max(1, Math.ceil(lista.length / porPagina));
  return { datos: lista.slice((pagina - 1) * porPagina, pagina * porPagina), pagina, paginas };
}
```

#### Las trampas de la Polilla (y la verdad)
| La Polilla dice… | La verdad |
|---|---|
| "todas las fichas tienen sus datos" | lo que llega de afuera es `unknown` hasta que pasa un guardia |
| "la página 0 existe" | las páginas arrancan en 1 y no pasan de la última |
| "ordená la original, total no importa" | `toSorted` deja la original como estaba |
| "buscá con mayúsculas exactas" | se compara en minúsculas: `toLowerCase()` |

### Micro-misión S01-N04-P1 · Las fichas por páginas

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Nima, la Polilla de Bronce
criatura: orc
carta: Trampa 1 | paginar<T> · slice((pagina - 1) * porPagina, pagina * porPagina) · Math.ceil para contar las páginas
recompensa: xp 15, monedas 3
```

#### Escena
La Polilla se come las fichas que quedan sueltas. Rigel decide mostrarlas de a pocas, por páginas, y guardar el resto en la caja.

#### Gheco sugiere
La página `p` arranca en `(p - 1) * porPagina` y termina antes de `p * porPagina`. La cantidad de páginas es `Math.ceil(total / porPagina)`.

#### Desafío
Completá el `slice` de `paginar`.

#### Pasos
1. Buscá el `___` en `paginar`.
2. Cambialo por `lista.slice((pagina - 1) * porPagina, pagina * porPagina)`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Pagina<T> {
  datos: T[];
  pagina: number;
  paginas: number;
}

function paginar<T>(lista: readonly T[], pagina: number, porPagina: number): Pagina<T> {
  const paginas = Math.max(1, Math.ceil(lista.length / porPagina));
  return { datos: ___, pagina, paginas };
}

const nombres = ['Sirio', 'Vega', 'Rigel', 'Arturo', 'Betelgeuse', 'Aldebarán', 'Proción'];
for (const p of [1, 2, 3]) {
  const pag = paginar(nombres, p, 3);
  console.log(`Página ${pag.pagina} de ${pag.paginas}: ${pag.datos.join(', ')}`);
}
```

#### Salida esperada
```
Página 1 de 3: Sirio, Vega, Rigel
Página 2 de 3: Arturo, Betelgeuse, Aldebarán
Página 3 de 3: Proción
```

#### Solución
```typescript
interface Pagina<T> {
  datos: T[];
  pagina: number;
  paginas: number;
}

function paginar<T>(lista: readonly T[], pagina: number, porPagina: number): Pagina<T> {
  const paginas = Math.max(1, Math.ceil(lista.length / porPagina));
  return { datos: lista.slice((pagina - 1) * porPagina, pagina * porPagina), pagina, paginas };
}

const nombres = ['Sirio', 'Vega', 'Rigel', 'Arturo', 'Betelgeuse', 'Aldebarán', 'Proción'];
for (const p of [1, 2, 3]) {
  const pag = paginar(nombres, p, 3);
  console.log(`Página ${pag.pagina} de ${pag.paginas}: ${pag.datos.join(', ')}`);
}
```

#### Al superarla
Las fichas quedan en tres sobres de latón, bien cerrados. La Polilla da vueltas alrededor, sin poder abrirlos.

#### Imagen
- Una polilla mecánica de bronce del tamaño de un gato, con alas de engranajes, revoloteando sobre la mesa.
- Tres sobres de latón cerrados con fichas adentro.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) cierra un sobre; Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) lo cubre; Gheco se esconde debajo de un sobre.

### Micro-misión S01-N04-P2 · Las fichas mordidas

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Astrea, la Polilla de Bronce
criatura: skeleton
carta: Trampa 2 | lo que llega es unknown · esEstrella(x): x is Estrella · filter(esEstrella) da Estrella[]
recompensa: xp 15, monedas 3
```

#### Escena
La Polilla mordió algunas fichas: a una le falta el nombre, otra tiene el brillo escrito con letras, otra es solo un pedazo de papel. Astrea las pasó a un texto JSON, y hay que separar las sanas de las rotas.

#### Gheco sugiere
`JSON.parse` devuelve `unknown` (con el `as unknown[]` que ya está puesto). Un guardia `esEstrella(x): x is Estrella` revisa cada campo. Usado en `filter`, la lista que sale ya es `Estrella[]`.

#### Desafío
Completá el guardia.

#### Pasos
1. Buscá el `___` en `esEstrella`.
2. Cambialo por `typeof f.nombre === 'string' && typeof f.brillo === 'number'`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Estrella { nombre: string; brillo: number }

function esEstrella(x: unknown): x is Estrella {
  if (typeof x !== 'object' || x === null) return false;
  const f = x as Record<string, unknown>;
  return ___;
}

const texto = '[{"nombre":"Vega","brillo":8},{"brillo":7},{"nombre":"Sirio","brillo":"mucho"},"papelito",{"nombre":"Arturo","brillo":9}]';
const fichas = JSON.parse(texto) as unknown[];

const sanas: Estrella[] = fichas.filter(esEstrella);
console.log(`Sanas: ${sanas.map((e) => e.nombre).join(', ')}`);
console.log(`Mordidas: ${fichas.length - sanas.length}`);
```

#### Salida esperada
```
Sanas: Vega, Arturo
Mordidas: 3
```

#### Solución
```typescript
interface Estrella { nombre: string; brillo: number }

function esEstrella(x: unknown): x is Estrella {
  if (typeof x !== 'object' || x === null) return false;
  const f = x as Record<string, unknown>;
  return typeof f.nombre === 'string' && typeof f.brillo === 'number';
}

const texto = '[{"nombre":"Vega","brillo":8},{"brillo":7},{"nombre":"Sirio","brillo":"mucho"},"papelito",{"nombre":"Arturo","brillo":9}]';
const fichas = JSON.parse(texto) as unknown[];

const sanas: Estrella[] = fichas.filter(esEstrella);
console.log(`Sanas: ${sanas.map((e) => e.nombre).join(', ')}`);
console.log(`Mordidas: ${fichas.length - sanas.length}`);
```

#### Al superarla
Las tres fichas mordidas van a una lata para reparar. La Polilla intenta comerse la lata y se rompe un diente.

#### Imagen
- Una lata de latón con fichas mordidas adentro y una polilla mecánica de bronce mordiendo el borde.
- Un esqueleto de alambre chiquito armado con pedazos de fichas.
- Astrea (lechuza con anteojos de latón y chaleco azul) separa fichas; Rigel (chico flaco con pecas, antiparras de latón) tapa la lata; Gheco se ríe del diente roto.

### Micro-misión S01-N04-P3 · El resumen del Atlas

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Astrea, la Polilla de Bronce
criatura: troll
carta: Trampa 3 | Record<Tipo, Resumen> · contar y quedarse con la más brillante en una sola pasada · nada se pierde
recompensa: xp 15, monedas 3
```

#### Escena
La Polilla escupe hojas en blanco sobre el Atlas: quiere tapar el resumen. Rigel lo arma de nuevo, en una sola pasada: para cada tipo, cuántas hay y cuál es la más brillante.

#### Gheco sugiere
El `Record<Tipo, Resumen>` arranca con los tres tipos. Para cada estrella, se suma una a su tipo y, si brilla más que la guardada, se cambia:

```ts
const r = resumen[e.tipo];
r.cantidad++;
if (e.brillo > r.brillo) { r.brillo = e.brillo; r.masBrillante = e.nombre; }
```

#### Desafío
Completá la línea que cambia la más brillante.

#### Pasos
1. Buscá el `___` en el `for`.
2. Cambialo por `if (e.brillo > r.brillo) { r.brillo = e.brillo; r.masBrillante = e.nombre; }`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; brillo: number; tipo: Tipo }
interface Resumen { cantidad: number; masBrillante: string; brillo: number }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', brillo: 10, tipo: 'enana' },
  { nombre: 'Vega', brillo: 8, tipo: 'enana' },
  { nombre: 'Rigel', brillo: 7, tipo: 'supergigante' },
  { nombre: 'Arturo', brillo: 9, tipo: 'gigante' },
  { nombre: 'Betelgeuse', brillo: 6, tipo: 'supergigante' },
];

const vacio = (): Resumen => ({ cantidad: 0, masBrillante: '-', brillo: 0 });
const resumen: Record<Tipo, Resumen> = { enana: vacio(), gigante: vacio(), supergigante: vacio() };

for (const e of catalogo) {
  const r = resumen[e.tipo];
  r.cantidad++;
  ___
}

for (const [tipo, r] of Object.entries(resumen)) {
  console.log(`${tipo}: ${r.cantidad}, la más brillante es ${r.masBrillante}`);
}
```

#### Salida esperada
```
enana: 2, la más brillante es Sirio
gigante: 1, la más brillante es Arturo
supergigante: 2, la más brillante es Rigel
```

#### Solución
```typescript
type Tipo = 'enana' | 'gigante' | 'supergigante';
interface Estrella { nombre: string; brillo: number; tipo: Tipo }
interface Resumen { cantidad: number; masBrillante: string; brillo: number }

const catalogo: Estrella[] = [
  { nombre: 'Sirio', brillo: 10, tipo: 'enana' },
  { nombre: 'Vega', brillo: 8, tipo: 'enana' },
  { nombre: 'Rigel', brillo: 7, tipo: 'supergigante' },
  { nombre: 'Arturo', brillo: 9, tipo: 'gigante' },
  { nombre: 'Betelgeuse', brillo: 6, tipo: 'supergigante' },
];

const vacio = (): Resumen => ({ cantidad: 0, masBrillante: '-', brillo: 0 });
const resumen: Record<Tipo, Resumen> = { enana: vacio(), gigante: vacio(), supergigante: vacio() };

for (const e of catalogo) {
  const r = resumen[e.tipo];
  r.cantidad++;
  if (e.brillo > r.brillo) { r.brillo = e.brillo; r.masBrillante = e.nombre; }
}

for (const [tipo, r] of Object.entries(resumen)) {
  console.log(`${tipo}: ${r.cantidad}, la más brillante es ${r.masBrillante}`);
}
```

#### Al superarla
El resumen queda escrito en el Atlas, con tinta que la Polilla no puede borrar.

#### Imagen
- El Atlas abierto con una tabla de tres renglones escrita con tinta dorada.
- La polilla mecánica de bronce escupiendo hojas en blanco que rebotan contra el libro.
- Astrea (lechuza con anteojos de latón y chaleco azul) sostiene el libro; Rigel (chico flaco con pecas, antiparras de latón) escribe; Gheco se tapa la cabeza.

### Micro-misión S01-N04-P4 · El catálogo en la pared

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Nima, la Polilla de Bronce
carta: Trampa 4 | la lista en la página · createElement('li') y textContent · ordenada con toSorted, sin tocar la original
recompensa: xp 15, monedas 5
```

#### Escena
Para que la Polilla no lo encuentre en la caja, Rigel pasa el catálogo a la pared de la biblioteca, en una lista ordenada de la más brillante a la menos.

#### Gheco sugiere
Para cada estrella de la lista ordenada: se crea un `li`, se le pone el texto con `textContent`, y se agrega a la lista con `append`.

#### Desafío
Completá las dos líneas que arman cada `li`.

#### Pasos
1. El primer `___`: `const li = document.createElement('li');`.
2. El segundo `___`: ``li.textContent = `${e.nombre} · brillo ${e.brillo}`;``.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: Georgia, serif; background: #1a1206; color: #e8d9b0; padding: 20px; }
  h1 { color: #f2c14e; font-size: 20px; }
  li { padding: 4px 0; border-bottom: 1px dashed #8d6e3f; }
</style>
<h1>Catálogo de Estrellas</h1>
<ol id="lista"></ol>
```

#### Estado
```
li #
```

#### Código inicial
```typescript
interface Estrella { nombre: string; brillo: number }

const catalogo: readonly Estrella[] = [
  { nombre: 'Rigel', brillo: 7 },
  { nombre: 'Sirio', brillo: 10 },
  { nombre: 'Vega', brillo: 8 },
  { nombre: 'Arturo', brillo: 9 },
];

const lista = document.querySelector<HTMLOListElement>('#lista');
if (!lista) throw new Error('Falta #lista en la página');

for (const e of catalogo.toSorted((a, b) => b.brillo - a.brillo)) {
  ___
  ___
  lista.append(li);
}
```

#### Salida esperada
```
── Estado ──
li #: 4
```

#### Solución
```typescript
interface Estrella { nombre: string; brillo: number }

const catalogo: readonly Estrella[] = [
  { nombre: 'Rigel', brillo: 7 },
  { nombre: 'Sirio', brillo: 10 },
  { nombre: 'Vega', brillo: 8 },
  { nombre: 'Arturo', brillo: 9 },
];

const lista = document.querySelector<HTMLOListElement>('#lista');
if (!lista) throw new Error('Falta #lista en la página');

for (const e of catalogo.toSorted((a, b) => b.brillo - a.brillo)) {
  const li = document.createElement('li');
  li.textContent = `${e.nombre} · brillo ${e.brillo}`;
  lista.append(li);
}
```

#### Al superarla
El catálogo brilla en la pared, escrito con letras de luz. La Polilla se golpea contra la pared y cae aturdida.

#### Imagen
- Una pared de la biblioteca con una lista luminosa de nombres de estrellas (sin texto legible).
- La polilla mecánica de bronce aturdida en el piso, con estrellitas girando sobre la cabeza.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro) baja el arco sin haber disparado; Rigel (chico flaco con pecas, antiparras de latón) y Gheco festejan.

### Micro-misión S01-N04-P5 · Jefe: la Polilla se queda sin cena

```meta
lugar: La biblioteca del Mirador
personajes: Rigel, Gheco, Nima, Astrea, Don Péndulo, la Polilla de Bronce
carta: El catálogo completo | escribir en el buscador · filtrar en minúsculas · ordenar · mostrar con textContent · contar lo que se ve
recompensa: xp 50, oro 50, monedas 1
```

#### Escena
La Polilla se despierta furiosa y va derecho a la pared. Rigel termina el catálogo: un **buscador** que filtra mientras se escribe, muestra las estrellas ordenadas y cuenta cuántas encontró. Si el catálogo se puede buscar, ya no hay fichas sueltas para comer.

#### Gheco sugiere
Junta toda la Senda. Cada vez que se escribe en `#buscar` (el evento `input`):
1. Se pasa lo escrito a minúsculas.
2. Se filtran las estrellas cuyo nombre o constelación (también en minúsculas) lo **incluye**.
3. Se ordenan por brillo y se dibuja la lista.
4. Se escribe la cuenta en `#cuenta`.

Falta el paso 2.

#### Desafío
Completá el filtro del buscador.

#### Pasos
1. Buscá el `___` en `mostrar`.
2. Cambialo por `e.nombre.toLowerCase().includes(texto) || e.constelacion.toLowerCase().includes(texto)`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: Georgia, serif; background: #1a1206; color: #e8d9b0; padding: 20px; }
  input { font-size: 16px; padding: 6px; background: #2a1d0b; color: #f2c14e; border: 2px solid #8d6e3f; }
  li { padding: 4px 0; }
  #cuenta { color: #f2c14e; }
</style>
<label>Buscar: <input id="buscar"></label>
<p id="cuenta"></p>
<ul id="lista"></ul>
```

#### Eventos
```
escribir #buscar orión
```

#### Estado
```
#cuenta
li #
```

#### Código inicial
```typescript
interface Estrella { nombre: string; constelacion: string; brillo: number }

const catalogo: readonly Estrella[] = [
  { nombre: 'Sirio', constelacion: 'Can Mayor', brillo: 10 },
  { nombre: 'Betelgeuse', constelacion: 'Orión', brillo: 6 },
  { nombre: 'Vega', constelacion: 'Lira', brillo: 8 },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7 },
  { nombre: 'Bellatrix', constelacion: 'Orión', brillo: 5 },
  { nombre: 'Arturo', constelacion: 'Boyero', brillo: 9 },
];

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const buscar = obtenerElemento<HTMLInputElement>('#buscar');
const cuenta = obtenerElemento<HTMLParagraphElement>('#cuenta');
const lista = obtenerElemento<HTMLUListElement>('#lista');

function mostrar(): void {
  const texto = buscar.value.trim().toLowerCase();
  const encontradas = catalogo
    .filter((e) => ___)
    .toSorted((a, b) => b.brillo - a.brillo);

  lista.replaceChildren();
  for (const e of encontradas) {
    const li = document.createElement('li');
    li.textContent = `${e.nombre} (${e.constelacion}) · brillo ${e.brillo}`;
    lista.append(li);
  }
  cuenta.textContent = `${encontradas.length} de ${catalogo.length} estrellas`;
}

buscar.addEventListener('input', mostrar);
mostrar();
```

#### Salida esperada
```
── Estado ──
#cuenta: 3 de 6 estrellas
li #: 3
```

#### Solución
```typescript
interface Estrella { nombre: string; constelacion: string; brillo: number }

const catalogo: readonly Estrella[] = [
  { nombre: 'Sirio', constelacion: 'Can Mayor', brillo: 10 },
  { nombre: 'Betelgeuse', constelacion: 'Orión', brillo: 6 },
  { nombre: 'Vega', constelacion: 'Lira', brillo: 8 },
  { nombre: 'Rigel', constelacion: 'Orión', brillo: 7 },
  { nombre: 'Bellatrix', constelacion: 'Orión', brillo: 5 },
  { nombre: 'Arturo', constelacion: 'Boyero', brillo: 9 },
];

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const buscar = obtenerElemento<HTMLInputElement>('#buscar');
const cuenta = obtenerElemento<HTMLParagraphElement>('#cuenta');
const lista = obtenerElemento<HTMLUListElement>('#lista');

function mostrar(): void {
  const texto = buscar.value.trim().toLowerCase();
  const encontradas = catalogo
    .filter((e) => e.nombre.toLowerCase().includes(texto) || e.constelacion.toLowerCase().includes(texto))
    .toSorted((a, b) => b.brillo - a.brillo);

  lista.replaceChildren();
  for (const e of encontradas) {
    const li = document.createElement('li');
    li.textContent = `${e.nombre} (${e.constelacion}) · brillo ${e.brillo}`;
    lista.append(li);
  }
  cuenta.textContent = `${encontradas.length} de ${catalogo.length} estrellas`;
}

buscar.addEventListener('input', mostrar);
mostrar();
```

#### Al superarla
La Polilla de Bronce aterriza sobre el buscador, prueba a morder las letras de luz y no puede. Da dos vueltas, cansada, y se queda quieta en un estante. Don Péndulo le cambia un engranaje del apetito con un destornillador chiquito: desde esa noche, la Polilla solo come polvo.

Nima se lleva una copia del buscador para el Archivo de Sila. Astrea le pone a Rigel el **Sello del Catálogo** en la tapa del Atlas.

#### Imagen
- La biblioteca del Mirador ordenada, con un buscador de latón y letras de luz en la pared.
- La polilla mecánica de bronce, tranquila, quitando el polvo de un estante.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) recibe un sello de lacre dorado de Astrea (lechuza con anteojos de latón y chaleco azul); Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) aplaude; Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa en un ojo) guarda el destornillador; Gheco sobre la polilla.
