# RAMA R03 · El Telescopio: uniones, tipos útiles y módulos

```meta
tipo: tronco
posicion: 3
```

## R03-N01 · Uniones y narrowing

```meta
tipo: tema
padre: R02-N08
precio: 10
criatura: goblin
temas: cal.tipos, prog.condicionales
```

### Crónica

El Telescopio Mayor tiene un problema: lo que ve por el ocular no siempre es lo mismo. A veces es una estrella, a veces un cometa, a veces una nube, a veces nada. Antes de anotarlo, hay que saber **qué** es.

—Mirá antes de anotar —dice {mentor}—. Una cosa que puede ser varias se llama **unión**. Y cada pregunta que le hacés la va achicando, hasta que sabés exactamente qué es.

### Objetivos

- Usar uniones (`number | string`, `Estrella | Cometa`) y entender por qué no se pueden usar sin preguntar.
- Estrechar (*narrowing*) con `typeof`, `instanceof`, `in`, `Array.isArray` y comparando con `null`.
- Ver cómo TypeScript sabe el tipo adentro de cada rama de un `if`.

### Antes de empezar

- R01-N03 (`unknown` y `typeof`) y R01-N06 (uniones).
- R02-N03 (`instanceof`).

### Explicación

#### Una unión no se usa sin preguntar
```typescript
function mostrar(m: number | string): string {
  return m.toFixed(1);   // ✗ TS2339: los textos no tienen toFixed
}
```

En una unión, solo se puede usar lo que tienen **todos** los tipos. Para lo demás, hay que preguntar.

#### Las preguntas que achican el tipo
```typescript
if (typeof m === 'number') { … }        // primitivos: number, string, boolean…
if (x instanceof Cometa) { … }          // clases
if ('cola' in x) { … }                  // objetos: ¿tiene esa propiedad?
if (Array.isArray(x)) { … }             // ¿es un arreglo?
if (x !== null) { … }                   // ¿no es null?
```

Adentro de cada rama, TypeScript ya sabe el tipo. Y en el `else`, sabe que es **lo otro**.

#### Un valor o una lista de valores
Un patrón muy común: aceptar una cosa o varias.

```typescript
function nombres(n: string | string[]): string {
  return Array.isArray(n) ? n.join(', ') : n;
}
```

### Código de ejemplo

```typescript
type Estrella = { nombre: string; brillo: number };
type Cometa = { nombre: string; cola: number };

function describir(cosa: Estrella | Cometa | null): string {
  if (cosa === null) return 'nada';
  if ('cola' in cosa) return `cometa ${cosa.nombre} (cola de ${cosa.cola} km)`;
  return `estrella ${cosa.nombre} (brillo ${cosa.brillo})`;
}

function aTexto(m: number | string): string {
  return typeof m === 'number' ? m.toFixed(1) : m.trim();
}

function nombres(n: string | string[]): string {
  return Array.isArray(n) ? n.join(', ') : n;
}

console.log(describir({ nombre: 'Halley', cola: 100 }));
console.log(describir({ nombre: 'Vega', brillo: 9 }));
console.log(describir(null));
console.log(aTexto(4), aTexto('  12 mm '), nombres(['Vega', 'Sirio']), nombres('Rigel'));
```

### Salida esperada

```
cometa Halley (cola de 100 km)
estrella Vega (brillo 9)
nada
4.0 12 mm Vega, Sirio Rigel
```

### ¿Para qué sirve?

Los datos de verdad vienen de varias formas: una respuesta que puede traer un resultado o un error, un campo que puede estar vacío, un parámetro que acepta uno o muchos. Las uniones lo dicen, y el narrowing obliga a tratar cada caso. Así no se usa un error como si fuera un resultado.

### Errores habituales

**Goblin: usar algo que no tienen todos (TS2339).** *La propiedad 'toFixed' no existe en el tipo 'string | number'*. Preguntá antes con `typeof`.

**Orco: no descartar null (TS18047).** *"x" es posiblemente "null"*. Preguntá `if (x !== null)` o `if (x)`.

**`typeof null` es `'object'`.** Por una herencia vieja de JavaScript, `typeof null === 'object'`. Para null, compará directo: `x === null`.

### Micro-misión R03-N01-P1 · El número o el texto

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco
criatura: goblin
carta: Narrowing con typeof | en una unión solo vale lo de todos · if (typeof m === 'number') achica el tipo · el else es lo otro
recompensa: xp 10, oro 10
```

#### Escena
El telescopio manda las medidas a veces como número y a veces como texto con espacios. Rigel quiere mostrarlas prolijas.

#### Gheco sugiere
En una unión (`number | string`), solo se puede usar lo que tienen **los dos** tipos. `toFixed` es solo de los números; `trim` (saca los espacios de las puntas), solo de los textos.

Con `typeof` se pregunta, y en cada rama el tipo ya está achicado:

```ts
typeof m === 'number' ? m.toFixed(1) : m.trim()
```

#### Desafío
Completá la pregunta.

#### Pasos
1. Buscá el `___` antes del `?`.
2. Cambialo por `typeof m === 'number'`.
3. Tocá **Ejecutar**. Tiene que salir `4.0 | 12 mm`.

#### Código inicial
```typescript
function aTexto(m: number | string): string {
  return ___ ? m.toFixed(1) : m.trim();
}

console.log(`${aTexto(4)} | ${aTexto('  12 mm ')}`);
```

#### Salida esperada
```
4.0 | 12 mm
```

#### Solución
```typescript
function aTexto(m: number | string): string {
  return typeof m === 'number' ? m.toFixed(1) : m.trim();
}

console.log(`${aTexto(4)} | ${aTexto('  12 mm ')}`);
```

#### Al superarla
Las medidas aparecen en la pizarra del telescopio, todas alineadas.

#### Imagen
- Un observatorio steampunk con el Telescopio Mayor de latón y una pizarra a su lado con medidas alineadas (sin números legibles).
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco de cuero marrón cerrado) escribe en la pizarra.
- Gheco sobre el tubo del telescopio.

### Micro-misión R03-N01-P2 · ¿Tiene cola?

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: Narrowing con in | if ('cola' in cosa) · pregunta si el objeto tiene esa propiedad · sirve con type e interface
recompensa: xp 10, oro 10
```

#### Escena
Por el ocular pasa algo brillante. ¿Estrella o cometa? Astrea le enseña a Rigel la pregunta más rápida: ¿tiene cola?

#### Gheco sugiere
Con `in` se pregunta si un objeto **tiene** una propiedad:

```ts
if ('cola' in cosa) { … }   // acá cosa es Cometa
```

Sirve para objetos que no tienen una clase detrás (los que se describen con `type` o `interface`), donde `instanceof` no anda.

#### Desafío
Completá la pregunta del `if`.

#### Pasos
1. Buscá el `___` en el `if`.
2. Cambialo por `'cola' in cosa`.
3. Tocá **Ejecutar**. Tiene que salir `cometa Halley` y `estrella Vega`.

#### Código inicial
```typescript
type Estrella = { nombre: string; brillo: number };
type Cometa = { nombre: string; cola: number };

function queEs(cosa: Estrella | Cometa): string {
  if (___) return `cometa ${cosa.nombre}`;
  return `estrella ${cosa.nombre}`;
}

console.log(queEs({ nombre: 'Halley', cola: 100 }));
console.log(queEs({ nombre: 'Vega', brillo: 9 }));
```

#### Salida esperada
```
cometa Halley
estrella Vega
```

#### Solución
```typescript
type Estrella = { nombre: string; brillo: number };
type Cometa = { nombre: string; cola: number };

function queEs(cosa: Estrella | Cometa): string {
  if ('cola' in cosa) return `cometa ${cosa.nombre}`;
  return `estrella ${cosa.nombre}`;
}

console.log(queEs({ nombre: 'Halley', cola: 100 }));
console.log(queEs({ nombre: 'Vega', brillo: 9 }));
```

#### Al superarla
Un cometa cruza el ocular dejando su cola de luz. Rigel lo anota con la letra temblorosa de la emoción.

#### Imagen
- El ocular de un telescopio de latón mostrando un cometa con cola larga cruzando el cielo estrellado.
- Rigel (chico flaco con pecas, antiparras de latón subidas, chaleco marrón) mira emocionado.
- Astrea (lechuza grande gris azulada con anteojos de latón y chaleco azul) señala con el ala; Gheco en el hombro de Rigel.

### Micro-misión R03-N01-P3 · Nada en el ocular

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco
criatura: orc
carta: Descartar null | Estrella | null · if (cosa === null) return … · después, TypeScript sabe que no es null
recompensa: xp 10, oro 10
```

#### Escena
A veces el telescopio no ve nada y manda `null`. Un **orco** espera ese momento para romper el programa.

#### Gheco sugiere
Si un valor puede ser `null`, hay que descartarlo antes de usarlo. Una forma prolija es salir temprano:

```ts
if (cosa === null) return 'nada';
// de acá para abajo, cosa no es null
```

#### Desafío
Agregá la línea que descarta el `null`.

#### Pasos
1. Tocá **Ejecutar** y leé el error (`TS18047`).
2. En el `___`, escribí `if (cosa === null) return 'nada';`.
3. Tocá **Ejecutar**. Tiene que salir `Vega` y `nada`.

#### Código inicial
```typescript
type Estrella = { nombre: string; brillo: number };

function ver(cosa: Estrella | null): string {
  ___
  return cosa.nombre;
}

console.log(ver({ nombre: 'Vega', brillo: 9 }));
console.log(ver(null));
```

#### Salida esperada
```
Vega
nada
```

#### Solución
```typescript
type Estrella = { nombre: string; brillo: number };

function ver(cosa: Estrella | null): string {
  if (cosa === null) return 'nada';
  return cosa.nombre;
}

console.log(ver({ nombre: 'Vega', brillo: 9 }));
console.log(ver(null));
```

#### Al superarla
Cuando el ocular queda vacío, el telescopio anota *nada* y sigue tranquilo. El orco se aburre y se va.

#### Imagen
- El ocular de un telescopio de latón mostrando un cielo nublado, sin estrellas.
- Un orco chiquito bostezando al pie del telescopio.
- Rigel (chico flaco con pecas, antiparras de latón) anota en la libreta; Gheco mira el cielo.

### Micro-misión R03-N01-P4 · Una o muchas

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco
carta: Array.isArray | string | string[] · Array.isArray(n) achica a string[] · el else es string
recompensa: xp 10, oro 10
```

#### Escena
Astrea pide a veces una estrella y a veces una lista. Rigel quiere una sola función que acepte las dos cosas.

#### Gheco sugiere
`Array.isArray(n)` pregunta si `n` es un arreglo. En la rama del sí, `n` es `string[]`; en la del no, es `string`.

```ts
Array.isArray(n) ? n.join(', ') : n
```

#### Desafío
Completá la pregunta.

#### Pasos
1. Buscá el `___` antes del `?`.
2. Cambialo por `Array.isArray(n)`.
3. Tocá **Ejecutar**. Tiene que salir `Vega, Sirio` y `Rigel`.

#### Código inicial
```typescript
function nombres(n: string | string[]): string {
  return ___ ? n.join(', ') : n;
}

console.log(nombres(['Vega', 'Sirio']));
console.log(nombres('Rigel'));
```

#### Salida esperada
```
Vega, Sirio
Rigel
```

#### Solución
```typescript
function nombres(n: string | string[]): string {
  return Array.isArray(n) ? n.join(', ') : n;
}

console.log(nombres(['Vega', 'Sirio']));
console.log(nombres('Rigel'));
```

#### Al superarla
La función acepta lo que le den. Astrea la prueba con una estrella y con diez: anda con las dos.

#### Imagen
- Una tarjeta suelta y un mazo de tarjetas de estrellas entrando en la misma ranura de una máquina de latón.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mete el mazo.
- Gheco sobre la máquina.

### Micro-misión R03-N01-P5 · El instrumento correcto

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: Narrowing con instanceof | clases distintas en una unión · if (x instanceof Lente) deja usar lo de Lente
recompensa: xp 15, monedas 5
```

#### Escena
En la mesa hay lentes y filtros mezclados. Los lentes se enfocan; los filtros se tiñen. Rigel tiene que tratar a cada uno como corresponde.

#### Gheco sugiere
Cuando la unión es de **clases**, se pregunta con `instanceof`:

```ts
if (p instanceof Lente) return p.enfocar();
return p.tenir();   // acá p es Filtro
```

#### Desafío
Completá la pregunta del `if`.

#### Pasos
1. Buscá el `___` en el `if`.
2. Cambialo por `p instanceof Lente`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
class Lente {
  constructor(public aumento: number) {}
  enfocar(): string { return `lente enfocado a ${this.aumento}x`; }
}

class Filtro {
  constructor(public color: string) {}
  tenir(): string { return `filtro ${this.color}`; }
}

function usar(p: Lente | Filtro): string {
  if (___) return p.enfocar();
  return p.tenir();
}

for (const p of [new Lente(30), new Filtro('azul'), new Lente(8)]) console.log(usar(p));
```

#### Salida esperada
```
lente enfocado a 30x
filtro azul
lente enfocado a 8x
```

#### Solución
```typescript
class Lente {
  constructor(public aumento: number) {}
  enfocar(): string { return `lente enfocado a ${this.aumento}x`; }
}

class Filtro {
  constructor(public color: string) {}
  tenir(): string { return `filtro ${this.color}`; }
}

function usar(p: Lente | Filtro): string {
  if (p instanceof Lente) return p.enfocar();
  return p.tenir();
}

for (const p of [new Lente(30), new Filtro('azul'), new Lente(8)]) console.log(usar(p));
```

#### Al superarla
Cada pieza va a su lugar: los lentes al ocular, el filtro azul delante. El cielo se ve más nítido.

#### Imagen
- Una mesa con lentes de latón y un filtro de vidrio azul ordenados en dos grupos.
- Astrea (lechuza con anteojos de latón) coloca el filtro azul delante del telescopio.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) monta un lente; Gheco detrás del filtro, teñido de azul.

### Micro-misión R03-N01-P6 · El informe de la noche

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: Todas las preguntas | null primero · in para el cometa · lo que queda es estrella · un for…of sobre una lista con de todo
recompensa: xp 15, monedas 5
```

#### Escena
Al terminar la noche, Rigel arma el informe de todo lo que pasó por el ocular: estrellas, cometas y momentos de nada.

#### Gheco sugiere
Se pregunta de lo más simple a lo más complicado: primero el `null`, después lo que tiene `cola`, y lo que queda es una estrella. Después de cada `return`, el tipo se achica solo.

#### Desafío
Completá las dos preguntas de `describir`.

#### Pasos
1. El primer `___`: `if (cosa === null) return 'nada';`.
2. El segundo `___`: `'cola' in cosa`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Estrella = { nombre: string; brillo: number };
type Cometa = { nombre: string; cola: number };

function describir(cosa: Estrella | Cometa | null): string {
  ___
  if (___) return `cometa ${cosa.nombre} (cola de ${cosa.cola} km)`;
  return `estrella ${cosa.nombre} (brillo ${cosa.brillo})`;
}

const noche: (Estrella | Cometa | null)[] = [
  { nombre: 'Vega', brillo: 9 },
  null,
  { nombre: 'Halley', cola: 100 },
];
for (const cosa of noche) console.log(describir(cosa));
```

#### Salida esperada
```
estrella Vega (brillo 9)
nada
cometa Halley (cola de 100 km)
```

#### Solución
```typescript
type Estrella = { nombre: string; brillo: number };
type Cometa = { nombre: string; cola: number };

function describir(cosa: Estrella | Cometa | null): string {
  if (cosa === null) return 'nada';
  if ('cola' in cosa) return `cometa ${cosa.nombre} (cola de ${cosa.cola} km)`;
  return `estrella ${cosa.nombre} (brillo ${cosa.brillo})`;
}

const noche: (Estrella | Cometa | null)[] = [
  { nombre: 'Vega', brillo: 9 },
  null,
  { nombre: 'Halley', cola: 100 },
];
for (const cosa of noche) console.log(describir(cosa));
```

#### Al superarla
Astrea lee el informe completo y le da a Rigel una **estrella de latón**. —Una noche bien mirada vale más que diez noches de suerte.

#### Imagen
- Un informe de observación sobre la mesa del telescopio, con dibujitos de una estrella, una nube y un cometa.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sonríe cansado; Gheco dormido sobre el informe.

## R03-N02 · Uniones discriminadas

```meta
tipo: tema
padre: R03-N01
precio: 10
criatura: ogre
temas: cal.tipos, prog.condicionales
```

### Crónica

Astrea le da a Rigel las **tarjetas de las figuras**: círculos, cuadrados y triángulos de luz que el Planisferio dibuja entre las estrellas. Cada tarjeta empieza con una palabra grande: *círculo*, *cuadrado*, *triángulo*. Esa palabra dice qué más tiene la tarjeta.

—No hace falta preguntar si tiene radio o lado —dice {mentor}—. La primera palabra ya lo dice todo. En el Mirador se llama **etiqueta**.

### Objetivos

- Armar una unión discriminada: varios tipos con un campo en común (`tipo`) que tiene un valor distinto en cada uno.
- Usar un `switch` sobre ese campo: en cada `case`, TypeScript sabe exactamente qué forma tiene.
- Ver qué pasa si se escribe mal un `case`.

### Antes de empezar

- R03-N01: narrowing.
- R01-N06: uniones de opciones.

### Explicación

#### El campo que discrimina
```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
type Figura = Circulo | Cuadrado;
```

Todos tienen `tipo`, pero cada uno con un **valor fijo distinto**. Con mirar `tipo`, TypeScript sabe cuál es:

```typescript
function area(f: Figura): number {
  switch (f.tipo) {
    case 'circulo':
      return Math.PI * f.radio ** 2;   // acá f es Circulo
    case 'cuadrado':
      return f.lado ** 2;              // acá f es Cuadrado
  }
}
```

Es la forma más clara de manejar datos que vienen de varias formas: mensajes, eventos, respuestas de un servidor.

### Código de ejemplo

```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
type Triangulo = { tipo: 'triangulo'; base: number; alto: number };
type Figura = Circulo | Cuadrado | Triangulo;

function area(f: Figura): number {
  switch (f.tipo) {
    case 'circulo':
      return Math.PI * f.radio ** 2;
    case 'cuadrado':
      return f.lado ** 2;
    case 'triangulo':
      return (f.base * f.alto) / 2;
  }
}

const figuras: Figura[] = [
  { tipo: 'cuadrado', lado: 3 },
  { tipo: 'triangulo', base: 4, alto: 5 },
  { tipo: 'circulo', radio: 1 },
];
for (const f of figuras) console.log(f.tipo, area(f).toFixed(2));
```

### Salida esperada

```
cuadrado 9.00
triangulo 10.00
circulo 3.14
```

### ¿Para qué sirve?

Es el patrón más usado de TypeScript para datos con varias formas: el estado de un pedido (`pendiente`, `enviado` con fecha, `cancelado` con motivo), los mensajes de un chat, las acciones de un juego. Cada forma lleva solo lo que necesita, y el compilador no deja leer lo que no tiene.

### Errores habituales

**Esqueleto: leer lo que esa forma no tiene (TS2339).** En el `case 'cuadrado'`, `f.radio` da error: los cuadrados no tienen radio.

**Goblin: un case que no existe (TS2678).** Escribir `case 'circlo':` da error: esa etiqueta no está en la unión.

**Ogro: olvidarse un caso.** Si falta un `case`, la función puede no devolver nada. En el próximo nodo vas a ver cómo hacer que el compilador lo avise siempre.

### Micro-misión R03-N02-P1 · La etiqueta de la tarjeta

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco, Astrea
carta: Unión discriminada | un campo tipo con un valor fijo distinto en cada forma · type Figura = Circulo | Cuadrado
recompensa: xp 10, oro 10
```

#### Escena
Rigel escribe las tarjetas de las figuras. A la del cuadrado le falta la etiqueta.

#### Gheco sugiere
En una unión discriminada, cada forma tiene el **mismo campo** (`tipo`) con un **valor fijo** distinto:

```ts
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
```

#### Desafío
Completá el campo `tipo` del cuadrado.

#### Pasos
1. Buscá el `___` en `type Cuadrado`.
2. Cambialo por `tipo: 'cuadrado';`.
3. Tocá **Ejecutar**. Tiene que salir `circulo y cuadrado`.

#### Código inicial
```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { ___ lado: number };
type Figura = Circulo | Cuadrado;

const a: Figura = { tipo: 'circulo', radio: 2 };
const b: Figura = { tipo: 'cuadrado', lado: 3 };
console.log(`${a.tipo} y ${b.tipo}`);
```

#### Salida esperada
```
circulo y cuadrado
```

#### Solución
```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
type Figura = Circulo | Cuadrado;

const a: Figura = { tipo: 'circulo', radio: 2 };
const b: Figura = { tipo: 'cuadrado', lado: 3 };
console.log(`${a.tipo} y ${b.tipo}`);
```

#### Al superarla
Las dos tarjetas quedan con su palabra grande arriba. Astrea las apila en el Planisferio.

#### Imagen
- Dos tarjetas de latón con una figura de luz grabada (un círculo y un cuadrado) y una palabra grande arriba (sin letras legibles).
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) graba una tarjeta.
- Astrea (lechuza con anteojos de latón) apila las tarjetas; Gheco mira.

### Micro-misión R03-N02-P2 · El switch de las figuras

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco
carta: switch sobre la etiqueta | switch (f.tipo) · en cada case f tiene su forma · f.lado solo en el cuadrado
recompensa: xp 10, oro 10
```

#### Escena
El Planisferio tiene que saber cuánta luz necesita cada figura: depende de su área.

#### Gheco sugiere
Un `switch` sobre el campo que discrimina hace el resto: en cada `case`, TypeScript sabe la forma exacta.

```ts
switch (f.tipo) {
  case 'circulo':
    return Math.PI * f.radio ** 2;   // f es Circulo
  …
}
```

`**` es la potencia: `3 ** 2` es 9.

#### Desafío
Completá el caso del cuadrado.

#### Pasos
1. Buscá el `___` en el `switch`.
2. Cambialo por `case 'cuadrado':` y, en el renglón de abajo, `return f.lado ** 2;`.
3. Tocá **Ejecutar**. Tiene que salir `9.00 3.14`.

#### Código inicial
```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
type Figura = Circulo | Cuadrado;

function area(f: Figura): number {
  switch (f.tipo) {
    case 'circulo':
      return Math.PI * f.radio ** 2;
    ___
  }
}

console.log(area({ tipo: 'cuadrado', lado: 3 }).toFixed(2), area({ tipo: 'circulo', radio: 1 }).toFixed(2));
```

#### Salida esperada
```
9.00 3.14
```

#### Solución
```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
type Figura = Circulo | Cuadrado;

function area(f: Figura): number {
  switch (f.tipo) {
    case 'circulo':
      return Math.PI * f.radio ** 2;
    case 'cuadrado':
      return f.lado ** 2;
  }
}

console.log(area({ tipo: 'cuadrado', lado: 3 }).toFixed(2), area({ tipo: 'circulo', radio: 1 }).toFixed(2));
```

#### Al superarla
Entre las estrellas aparece un cuadrado de luz, y al lado un círculo, cada uno con su brillo justo.

#### Imagen
- Un cuadrado y un círculo dibujados con líneas de luz entre las estrellas del planetario mecánico.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) gira una perilla.
- Gheco dentro del círculo de luz.

### Micro-misión R03-N02-P3 · La propiedad equivocada

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco
criatura: skeleton
carta: Cada forma tiene lo suyo | en el case del cuadrado no hay radio · TS2339 · usá lo de esa forma
recompensa: xp 10, oro 10
```

#### Escena
Rigel copió la línea del círculo en el caso del cuadrado. Un **esqueleto** se metió en el radio que el cuadrado no tiene.

#### Gheco sugiere
Adentro del `case 'cuadrado'`, `f` es un `Cuadrado`: no tiene `radio`, y el compilador lo avisa (`TS2339`). Cada caso usa lo de **su** forma.

#### Desafío
Cambiá `f.radio` por `f.lado` en el caso del cuadrado.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el `case 'cuadrado'`, cambiá `f.radio` por `f.lado`.
3. Tocá **Ejecutar**. Tiene que salir `Perímetro del cuadrado: 12`.

#### Código inicial
```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
type Figura = Circulo | Cuadrado;

function perimetro(f: Figura): number {
  switch (f.tipo) {
    case 'circulo':
      return 2 * Math.PI * f.radio;
    case 'cuadrado':
      return 4 * f.radio;
  }
}

console.log(`Perímetro del cuadrado: ${perimetro({ tipo: 'cuadrado', lado: 3 })}`);
```

#### Salida esperada
```
Perímetro del cuadrado: 12
```

#### Solución
```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
type Figura = Circulo | Cuadrado;

function perimetro(f: Figura): number {
  switch (f.tipo) {
    case 'circulo':
      return 2 * Math.PI * f.radio;
    case 'cuadrado':
      return 4 * f.lado;
  }
}

console.log(`Perímetro del cuadrado: ${perimetro({ tipo: 'cuadrado', lado: 3 })}`);
```

#### Al superarla
El esqueleto se queda sin radio que agarrar y se cae del Planisferio.

#### Imagen
- Un cuadrado de luz entre las estrellas y un esqueleto de alambre chiquito cayendo desde una de sus esquinas.
- Rigel (chico flaco con pecas, antiparras de latón) corrige un plano.
- Gheco señala al esqueleto.

### Micro-misión R03-N02-P4 · El triángulo nuevo

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco, Astrea
carta: Sumar una forma | un type nuevo con su etiqueta · se agrega a la unión · un case nuevo en el switch
recompensa: xp 10, oro 10
```

#### Escena
Astrea quiere sumar triángulos al cielo. Rigel tiene que agregar la forma nueva y enseñarle al Planisferio su área.

#### Gheco sugiere
Para sumar una forma: un `type` nuevo con su etiqueta, sumarlo a la unión, y un `case` nuevo en el `switch`. El área del triángulo es base por alto, dividido 2.

#### Desafío
Agregá el triángulo a la unión y su caso.

#### Pasos
1. En `type Figura`, el `___` es `| Triangulo`.
2. En el `switch`, el `___` es `case 'triangulo':` y, abajo, `return (f.base * f.alto) / 2;`.
3. Tocá **Ejecutar**. Tiene que salir `Área del triángulo: 10`.

#### Código inicial
```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
type Triangulo = { tipo: 'triangulo'; base: number; alto: number };
type Figura = Circulo | Cuadrado ___;

function area(f: Figura): number {
  switch (f.tipo) {
    case 'circulo':
      return Math.PI * f.radio ** 2;
    case 'cuadrado':
      return f.lado ** 2;
    ___
  }
}

console.log(`Área del triángulo: ${area({ tipo: 'triangulo', base: 4, alto: 5 })}`);
```

#### Salida esperada
```
Área del triángulo: 10
```

#### Solución
```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
type Triangulo = { tipo: 'triangulo'; base: number; alto: number };
type Figura = Circulo | Cuadrado | Triangulo;

function area(f: Figura): number {
  switch (f.tipo) {
    case 'circulo':
      return Math.PI * f.radio ** 2;
    case 'cuadrado':
      return f.lado ** 2;
    case 'triangulo':
      return (f.base * f.alto) / 2;
  }
}

console.log(`Área del triángulo: ${area({ tipo: 'triangulo', base: 4, alto: 5 })}`);
```

#### Al superarla
El primer triángulo de luz se enciende entre tres estrellas. Astrea lo bautiza: *el Triángulo de Rigel*.

#### Imagen
- Un triángulo de luz uniendo tres estrellas en el planetario mecánico.
- Astrea (lechuza con anteojos de latón y chaleco azul) lo mira emocionada.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sonrojado; Gheco en un vértice.

### Micro-misión R03-N02-P5 · Los mensajes del Planisferio

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco
carta: Discriminadas para mensajes | type Mensaje con tipo 'gira' | 'traba' | 'alerta' · cada uno con sus datos · un switch para mostrar
recompensa: xp 15, monedas 5
```

#### Escena
El Planisferio manda mensajes de tres clases: que giró unos grados, que se trabó por algún motivo, o una alerta con su nivel. Rigel tiene que mostrarlos.

#### Gheco sugiere
Las uniones discriminadas son ideales para **mensajes**: cada clase de mensaje trae solo los datos que necesita.

```ts
type Mensaje =
  | { tipo: 'gira'; grados: number }
  | { tipo: 'traba'; motivo: string }
  | { tipo: 'alerta'; nivel: number };
```

#### Desafío
Completá el caso de la alerta.

#### Pasos
1. Buscá el `___` en el `switch`.
2. Cambialo por `case 'alerta':` y, abajo, ``return `¡Alerta nivel ${m.nivel}!`;``.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Mensaje =
  | { tipo: 'gira'; grados: number }
  | { tipo: 'traba'; motivo: string }
  | { tipo: 'alerta'; nivel: number };

function mostrar(m: Mensaje): string {
  switch (m.tipo) {
    case 'gira':
      return `Giró ${m.grados}°`;
    case 'traba':
      return `Se trabó: ${m.motivo}`;
    ___
  }
}

const mensajes: Mensaje[] = [
  { tipo: 'gira', grados: 45 },
  { tipo: 'alerta', nivel: 2 },
  { tipo: 'traba', motivo: 'falta aceite' },
];
for (const m of mensajes) console.log(mostrar(m));
```

#### Salida esperada
```
Giró 45°
¡Alerta nivel 2!
Se trabó: falta aceite
```

#### Solución
```typescript
type Mensaje =
  | { tipo: 'gira'; grados: number }
  | { tipo: 'traba'; motivo: string }
  | { tipo: 'alerta'; nivel: number };

function mostrar(m: Mensaje): string {
  switch (m.tipo) {
    case 'gira':
      return `Giró ${m.grados}°`;
    case 'traba':
      return `Se trabó: ${m.motivo}`;
    case 'alerta':
      return `¡Alerta nivel ${m.nivel}!`;
  }
}

const mensajes: Mensaje[] = [
  { tipo: 'gira', grados: 45 },
  { tipo: 'alerta', nivel: 2 },
  { tipo: 'traba', motivo: 'falta aceite' },
];
for (const m of mensajes) console.log(mostrar(m));
```

#### Al superarla
Los mensajes aparecen en orden en la pantallita del Planisferio. Rigel le pone aceite antes de que se trabe de verdad.

#### Imagen
- Una pantallita de vidrio con tres renglones de luz (sin letras legibles) en el panel del planetario mecánico.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) aceita un engranaje con el aceitero.
- Gheco leyendo la pantallita.

### Micro-misión R03-N02-P6 · El estado del pedido

```meta
lugar: El ascensor de vapor
personajes: Rigel, Gheco, Astrea
carta: Estados con datos | pendiente · enviado con piso · cancelado con motivo · cada estado lleva solo lo suyo
recompensa: xp 15, monedas 5
```

#### Escena
Los pedidos de piezas a la Ciudadela pasan por estados: pendiente, enviado (en qué piso va el ascensor) o cancelado (por qué). Astrea quiere ver el estado de cada uno.

#### Gheco sugiere
Un estado con datos es una unión discriminada: el `enviado` tiene `piso`, el `cancelado` tiene `motivo`, y el `pendiente` no tiene nada más. Así nunca se lee un `piso` de un pedido cancelado.

#### Desafío
Completá el tipo del estado `enviado` y su caso.

#### Pasos
1. En la unión, el `___` es `| { estado: 'enviado'; piso: number }`.
2. En el `switch`, el `___` es `case 'enviado':` y, abajo, ``return `${p.pieza}: en el piso ${p.piso}`;``.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Pedido = { pieza: string } & (
  | { estado: 'pendiente' }
  ___
  | { estado: 'cancelado'; motivo: string }
);

function verEstado(p: Pedido): string {
  switch (p.estado) {
    case 'pendiente':
      return `${p.pieza}: pendiente`;
    ___
    case 'cancelado':
      return `${p.pieza}: cancelado (${p.motivo})`;
  }
}

const pedidos: Pedido[] = [
  { pieza: 'ocular', estado: 'enviado', piso: 4 },
  { pieza: 'biela', estado: 'pendiente' },
  { pieza: 'resorte', estado: 'cancelado', motivo: 'no hay stock' },
];
for (const p of pedidos) console.log(verEstado(p));
```

#### Salida esperada
```
ocular: en el piso 4
biela: pendiente
resorte: cancelado (no hay stock)
```

#### Solución
```typescript
type Pedido = { pieza: string } & (
  | { estado: 'pendiente' }
  | { estado: 'enviado'; piso: number }
  | { estado: 'cancelado'; motivo: string }
);

function verEstado(p: Pedido): string {
  switch (p.estado) {
    case 'pendiente':
      return `${p.pieza}: pendiente`;
    case 'enviado':
      return `${p.pieza}: en el piso ${p.piso}`;
    case 'cancelado':
      return `${p.pieza}: cancelado (${p.motivo})`;
  }
}

const pedidos: Pedido[] = [
  { pieza: 'ocular', estado: 'enviado', piso: 4 },
  { pieza: 'biela', estado: 'pendiente' },
  { pieza: 'resorte', estado: 'cancelado', motivo: 'no hay stock' },
];
for (const p of pedidos) console.log(verEstado(p));
```

#### Al superarla
Astrea cuelga el tablero de pedidos junto al ascensor. Le da a Rigel una **estrella de latón**: —El ocular ya viene subiendo.

#### Imagen
- Un tablero de pedidos de latón junto al ascensor de vapor, con tres fichas en tres columnas.
- Astrea (lechuza con anteojos de latón y chaleco azul) cuelga el tablero.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) recibe una ficha con una estrella; Gheco viaja en el ascensor.

## R03-N03 · never y los guardias propios

```meta
tipo: tema
padre: R03-N02
precio: 10
criatura: ogre
temas: cal.tipos, err.validacion
```

### Crónica

Una noche, Astrea agrega una figura nueva al Planisferio: el **rombo**. Nadie le avisa a la máquina de las áreas, que sigue igual. Cuando le llega el primer rombo, la máquina no devuelve nada, y el Planisferio dibuja un agujero negro en el cielo.

—Una máquina tiene que **quejarse** si le falta un caso —dice {mentor}—. Y hay otra cosa: lo que llega de afuera no trae etiqueta. Para eso hacen falta **guardias** que revisen cada pieza en la puerta.

### Objetivos

- Usar `never` para que el compilador avise si a un `switch` le falta un caso (exhaustividad).
- Escribir un **guardia propio** (*type guard*): una función `(x: unknown): x is Estrella` que revisa un dato y le dice al compilador qué es.
- Validar datos que llegan como `unknown` antes de usarlos.

### Antes de empezar

- R03-N02: uniones discriminadas.
- R01-N03: `unknown` y `never`.

### Explicación

#### El caso que falta
```typescript
function area(f: Figura): number {
  switch (f.tipo) {
    case 'circulo': return …;
    case 'cuadrado': return …;
    default: {
      const nunca: never = f;   // si llegó acá, es una forma que nadie atendió
      throw new Error(`Figura desconocida: ${JSON.stringify(nunca)}`);
    }
  }
}
```

Si el `switch` atiende **todas** las formas, en el `default` no queda nada: `f` es `never` y la línea compila. Si mañana alguien agrega `Rombo` a la unión y no su `case`, en el `default` queda un `Rombo`, que no se puede guardar en un `never`: el compilador avisa **dónde** falta el caso (`TS2322`). El olvido se vuelve un error de compilación.

#### Guardias propios
Lo que llega de afuera (un `JSON.parse`, el `localStorage`, un servidor) es `unknown`. Un **guardia** es una función que lo revisa y, si devuelve `true`, le dice al compilador qué es:

```typescript
type Estrella = { nombre: string; brillo: number };

function esEstrella(x: unknown): x is Estrella {
  return typeof x === 'object' && x !== null
    && 'nombre' in x && typeof x.nombre === 'string'
    && 'brillo' in x && typeof x.brillo === 'number';
}

const dato: unknown = JSON.parse('{"nombre":"Vega","brillo":9}');
if (esEstrella(dato)) console.log(dato.brillo);   // acá dato es Estrella
```

`x is Estrella` en el lugar del tipo de retorno es la promesa del guardia: «si digo `true`, es una `Estrella`».

> Ojo: el compilador **confía** en el guardia. Si el guardia revisa mal, el error aparece al ejecutar. Revisá cada propiedad que vas a usar.

### Código de ejemplo

```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
type Figura = Circulo | Cuadrado;

function area(f: Figura): number {
  switch (f.tipo) {
    case 'circulo':
      return Math.PI * f.radio ** 2;
    case 'cuadrado':
      return f.lado ** 2;
    default: {
      const nunca: never = f;
      throw new Error(`Figura desconocida: ${JSON.stringify(nunca)}`);
    }
  }
}

type Estrella = { nombre: string; brillo: number };

function esEstrella(x: unknown): x is Estrella {
  return typeof x === 'object' && x !== null
    && 'nombre' in x && typeof x.nombre === 'string'
    && 'brillo' in x && typeof x.brillo === 'number';
}

const llegadas: unknown[] = [JSON.parse('{"nombre":"Vega","brillo":9}'), 'ruido', { nombre: 'Sirio' }];
console.log(area({ tipo: 'cuadrado', lado: 2 }));
for (const d of llegadas) console.log(esEstrella(d) ? `${d.nombre}: ${d.brillo}` : 'descartado');
```

### Salida esperada

```
4
Vega: 9
descartado
descartado
```

### ¿Para qué sirve?

`never` hace que agregar un caso nuevo sea seguro: el compilador te lleva de la mano por todos los lugares que hay que actualizar. Los guardias son la puerta de entrada de los datos de afuera: todo lo que llega de un servidor, de un archivo o del usuario pasa por uno antes de usarse.

### Errores habituales

**Ogro: el caso que falta (TS2322 con never).** *El tipo '{ tipo: "rombo"; … }' no se puede asignar al tipo 'never'*: te dice qué forma no atendiste.

**Goblin: el guardia que no revisa todo.** Si `esEstrella` no revisa `brillo` y devuelve `true`, el compilador te cree, y `dato.brillo` explota al ejecutar.

**Orco: olvidarse de que null es un object.** `typeof null === 'object'`: por eso el guardia pregunta también `x !== null`.

### Micro-misión R03-N03-P1 · La máquina que se queja

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco
criatura: ogre
carta: Exhaustividad | default: { const nunca: never = f; … } · si están todos los casos, compila · si falta uno, TS2322
recompensa: xp 10, oro 10
```

#### Escena
Rigel le pone a la máquina de las áreas una alarma: si alguna vez le llega una figura que no conoce, que se queje **antes** de ejecutar.

#### Gheco sugiere
En el `default` de un `switch` que atiende todas las formas, no queda ninguna: `f` es `never`. Por eso esta línea compila:

```ts
const nunca: never = f;
```

Si un día falta un caso, en el `default` queda esa forma, y el compilador avisa.

#### Desafío
Completá la línea del `default`.

#### Pasos
1. Buscá el `___` adentro del `default`.
2. Cambialo por `const nunca: never = f;`.
3. Tocá **Ejecutar**. Tiene que salir `4 3.14`.

#### Código inicial
```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
type Figura = Circulo | Cuadrado;

function area(f: Figura): number {
  switch (f.tipo) {
    case 'circulo':
      return Math.PI * f.radio ** 2;
    case 'cuadrado':
      return f.lado ** 2;
    default: {
      ___
      throw new Error(`Figura desconocida: ${JSON.stringify(nunca)}`);
    }
  }
}

console.log(area({ tipo: 'cuadrado', lado: 2 }), area({ tipo: 'circulo', radio: 1 }).toFixed(2));
```

#### Salida esperada
```
4 3.14
```

#### Solución
```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
type Figura = Circulo | Cuadrado;

function area(f: Figura): number {
  switch (f.tipo) {
    case 'circulo':
      return Math.PI * f.radio ** 2;
    case 'cuadrado':
      return f.lado ** 2;
    default: {
      const nunca: never = f;
      throw new Error(`Figura desconocida: ${JSON.stringify(nunca)}`);
    }
  }
}

console.log(area({ tipo: 'cuadrado', lado: 2 }), area({ tipo: 'circulo', radio: 1 }).toFixed(2));
```

#### Al superarla
La alarma queda montada en la máquina, en silencio. Por ahora no hay de qué quejarse.

#### Imagen
- Una máquina de áreas de latón con una campana de alarma nueva atornillada arriba, quieta.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) ajusta la campana.
- Gheco sentado sobre la campana.

### Micro-misión R03-N03-P2 · Llega el rombo

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco, Astrea
criatura: ogre
carta: El compilador te guía | se agrega Rombo a la unión · el never avisa dónde falta el caso · se agrega el case
recompensa: xp 10, oro 10
```

#### Escena
Astrea agrega el **rombo** a las figuras. Esta vez, la alarma de Rigel suena antes de que el Planisferio dibuje un agujero negro.

#### Gheco sugiere
Al agregar `Rombo` a la unión, el `default` ya no queda vacío: queda el rombo, y `const nunca: never = f` da `TS2322`, diciendo qué forma falta. Para arreglarlo, se agrega su `case`. El área del rombo es diagonal mayor por diagonal menor, dividido 2.

#### Desafío
Agregá el caso del rombo.

#### Pasos
1. Tocá **Ejecutar** y leé el error: dice qué forma no está atendida.
2. En el `___`, escribí `case 'rombo':` y, abajo, `return (f.mayor * f.menor) / 2;`.
3. Tocá **Ejecutar**. Tiene que salir `Área del rombo: 12`.

#### Código inicial
```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
type Rombo = { tipo: 'rombo'; mayor: number; menor: number };
type Figura = Circulo | Cuadrado | Rombo;

function area(f: Figura): number {
  switch (f.tipo) {
    case 'circulo':
      return Math.PI * f.radio ** 2;
    case 'cuadrado':
      return f.lado ** 2;
    ___
    default: {
      const nunca: never = f;
      throw new Error(`Figura desconocida: ${JSON.stringify(nunca)}`);
    }
  }
}

console.log(`Área del rombo: ${area({ tipo: 'rombo', mayor: 6, menor: 4 })}`);
```

#### Salida esperada
```
Área del rombo: 12
```

#### Solución
```typescript
type Circulo = { tipo: 'circulo'; radio: number };
type Cuadrado = { tipo: 'cuadrado'; lado: number };
type Rombo = { tipo: 'rombo'; mayor: number; menor: number };
type Figura = Circulo | Cuadrado | Rombo;

function area(f: Figura): number {
  switch (f.tipo) {
    case 'circulo':
      return Math.PI * f.radio ** 2;
    case 'cuadrado':
      return f.lado ** 2;
    case 'rombo':
      return (f.mayor * f.menor) / 2;
    default: {
      const nunca: never = f;
      throw new Error(`Figura desconocida: ${JSON.stringify(nunca)}`);
    }
  }
}

console.log(`Área del rombo: ${area({ tipo: 'rombo', mayor: 6, menor: 4 })}`);
```

#### Al superarla
Un rombo de luz aparece entre cuatro estrellas, sin agujeros negros. Astrea asiente: —Así se agrega algo nuevo sin miedo.

#### Imagen
- Un rombo de luz entre cuatro estrellas del planetario mecánico, y la campana de alarma vibrando apenas.
- Astrea (lechuza con anteojos de latón y chaleco azul) mira el rombo.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) apaga la campana; Gheco aplaude.

### Micro-misión R03-N03-P3 · El guardia de la puerta

```meta
lugar: El ascensor de vapor
personajes: Rigel, Gheco
carta: Guardia propio | function esNumero(x: unknown): x is number · si devuelve true, el compilador sabe el tipo
recompensa: xp 10, oro 10
```

#### Escena
Del ascensor llegan cajas sin etiqueta. Rigel pone un guardia en la puerta: solo pasan las que son medidas (números).

#### Gheco sugiere
Un **guardia** es una función que revisa un `unknown` y, en el lugar del tipo de retorno, promete qué es si devuelve `true`:

```ts
function esNumero(x: unknown): x is number {
  return typeof x === 'number';
}
```

Después, `if (esNumero(dato))` achica el tipo igual que un `typeof`.

#### Desafío
Completá el tipo de retorno del guardia.

#### Pasos
1. Buscá el `___` después de los paréntesis de `esNumero`.
2. Cambialo por `x is number`.
3. Tocá **Ejecutar**. Tiene que salir `Suma de las medidas: 16`.

#### Código inicial
```typescript
function esNumero(x: unknown): ___ {
  return typeof x === 'number';
}

const cajas: unknown[] = [12, 'lente', 4, null, true];
let suma = 0;
for (const c of cajas) if (esNumero(c)) suma += c;
console.log(`Suma de las medidas: ${suma}`);
```

#### Salida esperada
```
Suma de las medidas: 16
```

#### Solución
```typescript
function esNumero(x: unknown): x is number {
  return typeof x === 'number';
}

const cajas: unknown[] = [12, 'lente', 4, null, true];
let suma = 0;
for (const c of cajas) if (esNumero(c)) suma += c;
console.log(`Suma de las medidas: ${suma}`);
```

#### Al superarla
El guardia deja pasar dos cajas y manda las otras tres de vuelta abajo.

#### Imagen
- Un autómata guardia chiquito de latón en la puerta del ascensor, separando cajas en dos pilas.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) lo observa con los brazos cruzados.
- Gheco sobre una caja.

### Micro-misión R03-N03-P4 · El guardia de las estrellas

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco, Astrea
carta: Guardia de un objeto | typeof x === 'object' && x !== null · 'nombre' in x && typeof x.nombre === 'string' · revisá cada propiedad que vas a usar
recompensa: xp 10, oro 10
```

#### Escena
Llegan fichas de estrellas en texto, desde la Ciudadela. Algunas están incompletas. Astrea solo quiere las que tienen nombre **y** brillo.

#### Gheco sugiere
Para un objeto, el guardia revisa todo:
- que sea un objeto y no `null`;
- que tenga cada propiedad (`in`) y que sea del tipo correcto (`typeof`).

```ts
return typeof x === 'object' && x !== null
  && 'nombre' in x && typeof x.nombre === 'string'
  && 'brillo' in x && typeof x.brillo === 'number';
```

`JSON.parse` convierte un texto con formato JSON en un valor; lo que devuelve no tiene tipo seguro.

#### Desafío
Completá la revisión del brillo.

#### Pasos
1. Buscá el `___` al final del `return`.
2. Cambialo por `'brillo' in x && typeof x.brillo === 'number'`.
3. Tocá **Ejecutar**. Tiene que salir `Vega: 9` y dos `descartada`.

#### Código inicial
```typescript
type Estrella = { nombre: string; brillo: number };

function esEstrella(x: unknown): x is Estrella {
  return typeof x === 'object' && x !== null
    && 'nombre' in x && typeof x.nombre === 'string'
    && ___;
}

const fichas = ['{"nombre":"Vega","brillo":9}', '{"nombre":"Sirio"}', '"ruido"'];
for (const f of fichas) {
  const dato: unknown = JSON.parse(f);
  console.log(esEstrella(dato) ? `${dato.nombre}: ${dato.brillo}` : 'descartada');
}
```

#### Salida esperada
```
Vega: 9
descartada
descartada
```

#### Solución
```typescript
type Estrella = { nombre: string; brillo: number };

function esEstrella(x: unknown): x is Estrella {
  return typeof x === 'object' && x !== null
    && 'nombre' in x && typeof x.nombre === 'string'
    && 'brillo' in x && typeof x.brillo === 'number';
}

const fichas = ['{"nombre":"Vega","brillo":9}', '{"nombre":"Sirio"}', '"ruido"'];
for (const f of fichas) {
  const dato: unknown = JSON.parse(f);
  console.log(esEstrella(dato) ? `${dato.nombre}: ${dato.brillo}` : 'descartada');
}
```

#### Al superarla
Solo la ficha de Vega entra al catálogo. Astrea le escribe a la Ciudadela pidiendo que manden la de Sirio completa.

#### Imagen
- Tres fichas de papel saliendo de un tubo neumático de latón: una aceptada con un sello, dos rechazadas.
- Astrea (lechuza con anteojos de latón) sella la ficha aceptada.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) separa las rechazadas; Gheco mira.

### Micro-misión R03-N03-P5 · El guardia que mentía

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco
criatura: goblin
carta: El compilador confía en el guardia | si el guardia no revisa algo, el error aparece al ejecutar · revisá todo lo que se usa
recompensa: xp 15, monedas 5
```

#### Escena
Un goblin escribió un guardia perezoso: solo revisa el nombre. El programa compila… y al ejecutar muestra *undefined* donde debería ir el brillo.

#### Gheco sugiere
El compilador **confía** en el guardia: si dice `true`, cree que es una `Estrella`. Si el guardia no revisa el brillo, una ficha sin brillo pasa igual. El arreglo es que el guardia revise **todo** lo que después se usa.

#### Desafío
Agregale al guardia la revisión del brillo.

#### Pasos
1. Tocá **Ejecutar**: sale `Sirio: undefined`, que está mal.
2. Al final del `return`, antes del `;`, agregá `&& 'brillo' in x && typeof x.brillo === 'number'`.
3. Tocá **Ejecutar**. Tiene que salir `Vega: 9` y `descartada`.

#### Código inicial
```typescript
type Estrella = { nombre: string; brillo: number };

function esEstrella(x: unknown): x is Estrella {
  return typeof x === 'object' && x !== null
    && 'nombre' in x && typeof x.nombre === 'string';
}

for (const f of ['{"nombre":"Vega","brillo":9}', '{"nombre":"Sirio"}']) {
  const dato: unknown = JSON.parse(f);
  console.log(esEstrella(dato) ? `${dato.nombre}: ${dato.brillo}` : 'descartada');
}
```

#### Salida esperada
```
Vega: 9
descartada
```

#### Solución
```typescript
type Estrella = { nombre: string; brillo: number };

function esEstrella(x: unknown): x is Estrella {
  return typeof x === 'object' && x !== null
    && 'nombre' in x && typeof x.nombre === 'string'
    && 'brillo' in x && typeof x.brillo === 'number';
}

for (const f of ['{"nombre":"Vega","brillo":9}', '{"nombre":"Sirio"}']) {
  const dato: unknown = JSON.parse(f);
  console.log(esEstrella(dato) ? `${dato.nombre}: ${dato.brillo}` : 'descartada');
}
```

#### Al superarla
El guardia nuevo ya no deja pasar fichas incompletas. El goblin busca otro trabajo.

#### Imagen
- Un autómata guardia de latón con una lupa grande, revisando una ficha de papel con atención.
- Un goblin chiquito con un engranaje en la espalda se va con un cartel de «despedido» (sin letras legibles).
- Rigel (chico flaco con pecas, antiparras de latón) ajusta la lupa del guardia; Gheco mira.

### Micro-misión R03-N03-P6 · La puerta del Mirador

```meta
lugar: El ascensor de vapor
personajes: Rigel, Gheco, Astrea
carta: Guardia + discriminada + never | lo que llega pasa por el guardia · después se atiende con un switch exhaustivo
recompensa: xp 15, monedas 5
```

#### Escena
Por el ascensor llegan pedidos en texto de la Ciudadela. Rigel arma la puerta completa: un guardia revisa cada pedido y una máquina exhaustiva lo atiende.

#### Gheco sugiere
Los dos patrones juntos:
1. el **guardia** `esPedido` revisa que el dato tenga `tipo` con un valor conocido;
2. el **switch** con `never` atiende cada tipo, y avisaría si faltara uno.

`['subir', 'bajar'].includes(x.tipo)` pregunta si `x.tipo` es uno de esos.

#### Desafío
Completá el caso de `bajar` en el `switch`.

#### Pasos
1. Buscá el `___` en el `switch`.
2. Cambialo por `case 'bajar':` y, abajo, ``return `Baja ${p.pisos} pisos`;``.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Pedido = { tipo: 'subir'; pisos: number } | { tipo: 'bajar'; pisos: number };

function esPedido(x: unknown): x is Pedido {
  return typeof x === 'object' && x !== null
    && 'tipo' in x && typeof x.tipo === 'string' && ['subir', 'bajar'].includes(x.tipo)
    && 'pisos' in x && typeof x.pisos === 'number';
}

function atender(p: Pedido): string {
  switch (p.tipo) {
    case 'subir':
      return `Sube ${p.pisos} pisos`;
    ___
    default: {
      const nunca: never = p;
      throw new Error(`Pedido desconocido: ${JSON.stringify(nunca)}`);
    }
  }
}

for (const texto of ['{"tipo":"subir","pisos":3}', '{"tipo":"volar","pisos":1}', '{"tipo":"bajar","pisos":2}']) {
  const dato: unknown = JSON.parse(texto);
  console.log(esPedido(dato) ? atender(dato) : 'Pedido rechazado');
}
```

#### Salida esperada
```
Sube 3 pisos
Pedido rechazado
Baja 2 pisos
```

#### Solución
```typescript
type Pedido = { tipo: 'subir'; pisos: number } | { tipo: 'bajar'; pisos: number };

function esPedido(x: unknown): x is Pedido {
  return typeof x === 'object' && x !== null
    && 'tipo' in x && typeof x.tipo === 'string' && ['subir', 'bajar'].includes(x.tipo)
    && 'pisos' in x && typeof x.pisos === 'number';
}

function atender(p: Pedido): string {
  switch (p.tipo) {
    case 'subir':
      return `Sube ${p.pisos} pisos`;
    case 'bajar':
      return `Baja ${p.pisos} pisos`;
    default: {
      const nunca: never = p;
      throw new Error(`Pedido desconocido: ${JSON.stringify(nunca)}`);
    }
  }
}

for (const texto of ['{"tipo":"subir","pisos":3}', '{"tipo":"volar","pisos":1}', '{"tipo":"bajar","pisos":2}']) {
  const dato: unknown = JSON.parse(texto);
  console.log(esPedido(dato) ? atender(dato) : 'Pedido rechazado');
}
```

#### Al superarla
El ascensor sube, se niega a volar y baja. Astrea le da a Rigel una **estrella de latón**: —La puerta está segura.

#### Imagen
- El ascensor de vapor con un panel de control nuevo, un guardia de latón chiquito en la puerta y un papel rechazado volando.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sonríe; Gheco en el ascensor.

## R03-N04 · Tipos útiles: Partial, Pick, Omit, Record

```meta
tipo: tema
padre: R03-N03
precio: 10
criatura: skeleton
temas: cal.tipos, poo.genericos
```

### Crónica

En un cajón del Telescopio, Rigel encuentra un juego de **plantillas transparentes** del Vidriero. Se apoyan sobre una ficha técnica y la transforman: una tapa todo menos el número de serie, otra deja ver solo el nombre y la medida, otra marca todo como «puede faltar».

—Son las plantillas de los tipos —dice {mentor}—. No hace falta escribir una ficha nueva cada vez: se transforma la que ya tenés.

### Objetivos

- Usar los **tipos útiles** (*utility types*) que trae TypeScript:
  - `Partial<T>`: todo opcional;
  - `Required<T>`: nada opcional;
  - `Readonly<T>`: todo de solo lectura;
  - `Pick<T, 'a' | 'b'>`: solo esas propiedades;
  - `Omit<T, 'a'>`: todas menos esa;
  - `Record<K, V>`: un objeto con todas las claves de `K`, cada una con un `V`.
- Leer el error de un nombre que no existe en `Pick` u `Omit` (`TS2344`).

### Antes de empezar

- R01-N05 (`interface`), R02-N06 y R02-N07 (genéricos y `keyof`).

### Explicación

#### Transformar una ficha
```typescript
interface Estrella {
  id: string;
  nombre: string;
  brillo: number;
  distancia: number;
}

type Cambios = Partial<Estrella>;             // todas opcionales: para actualizar solo algunas
type Resumen = Pick<Estrella, 'nombre' | 'brillo'>;   // solo nombre y brillo
type Nueva = Omit<Estrella, 'id'>;            // todo menos el id (lo pone el sistema)
type Fija = Readonly<Estrella>;               // nada se puede cambiar
```

#### Actualizar solo algunas cosas
```typescript
function actualizar(e: Estrella, cambios: Partial<Estrella>): Estrella {
  return { ...e, ...cambios };
}
actualizar(vega, { brillo: 8 });   // no hace falta pasar todo
```

#### Un objeto con todas las claves
```typescript
type Turno = 'noche' | 'madrugada';
const encargados: Record<Turno, string> = {
  noche: 'Rigel',
  madrugada: 'Astrea',
};   // si falta una clave, TS2741
```

`Record` es como la firma de índice de R01-N08, pero con las claves **exactas**: ni de más ni de menos.

### Código de ejemplo

```typescript
interface Estrella {
  id: string;
  nombre: string;
  brillo: number;
  distancia: number;
}

function actualizar(e: Estrella, cambios: Partial<Estrella>): Estrella {
  return { ...e, ...cambios };
}

function resumen(e: Estrella): Pick<Estrella, 'nombre' | 'brillo'> {
  return { nombre: e.nombre, brillo: e.brillo };
}

let siguiente = 1;
function registrar(datos: Omit<Estrella, 'id'>): Estrella {
  return { id: `e-${siguiente++}`, ...datos };
}

type Turno = 'noche' | 'madrugada';
const encargados: Record<Turno, string> = { noche: 'Rigel', madrugada: 'Astrea' };

const vega = registrar({ nombre: 'Vega', brillo: 9, distancia: 25 });
const vegaMas = actualizar(vega, { brillo: 10 });
console.log(vega.id, resumen(vegaMas));
console.log(`Esta noche mira ${encargados.noche}`);
```

### Salida esperada

```
e-1 { nombre: 'Vega', brillo: 10 }
Esta noche mira Rigel
```

### ¿Para qué sirve?

En un programa de verdad, la misma «cosa» aparece de varias formas: el usuario completo, el usuario sin la contraseña para mostrarlo, los datos para crearlo (sin id) y los cambios para actualizarlo (todo opcional). Los tipos útiles los sacan de una sola ficha, y si la ficha cambia, cambian todos.

### Errores habituales

**Esqueleto: un nombre que no existe en Pick u Omit (TS2344).** *El tipo '"brilo"' no cumple la restricción …*, seguido de los nombres que valen.

**Esqueleto: falta una clave en un Record (TS2741).** `Record<Turno, string>` pide **todas** las claves de `Turno`.

**Goblin: usar Partial para crear.** `Partial` sirve para **cambios**. Para crear, usá el tipo completo (o `Omit` de lo que pone el sistema).

### Micro-misión R03-N04-P1 · Cambiar solo el brillo

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco, Astrea
carta: Partial<T> | todas las propiedades opcionales · para actualizar solo algunas · { ...e, ...cambios }
recompensa: xp 10, oro 10
```

#### Escena
Esta noche Vega brilla un poco menos. Astrea quiere actualizar solo el brillo, sin reescribir toda la ficha.

#### Gheco sugiere
`Partial<Estrella>` es la misma ficha con **todo opcional**: sirve para pasar solo lo que cambia.

```ts
function actualizar(e: Estrella, cambios: Partial<Estrella>): Estrella {
  return { ...e, ...cambios };
}
```

`{ ...e, ...cambios }` copia la ficha y le pisa encima los cambios.

#### Desafío
Completá el tipo de los cambios.

#### Pasos
1. Buscá el `___` después de `cambios:`.
2. Cambialo por `Partial<Estrella>`.
3. Tocá **Ejecutar**. Tiene que salir `Vega: brillo 8, a 25 años luz`.

#### Código inicial
```typescript
interface Estrella {
  nombre: string;
  brillo: number;
  distancia: number;
}

function actualizar(e: Estrella, cambios: ___): Estrella {
  return { ...e, ...cambios };
}

const vega: Estrella = { nombre: 'Vega', brillo: 9, distancia: 25 };
const nueva = actualizar(vega, { brillo: 8 });
console.log(`${nueva.nombre}: brillo ${nueva.brillo}, a ${nueva.distancia} años luz`);
```

#### Salida esperada
```
Vega: brillo 8, a 25 años luz
```

#### Solución
```typescript
interface Estrella {
  nombre: string;
  brillo: number;
  distancia: number;
}

function actualizar(e: Estrella, cambios: Partial<Estrella>): Estrella {
  return { ...e, ...cambios };
}

const vega: Estrella = { nombre: 'Vega', brillo: 9, distancia: 25 };
const nueva = actualizar(vega, { brillo: 8 });
console.log(`${nueva.nombre}: brillo ${nueva.brillo}, a ${nueva.distancia} años luz`);
```

#### Al superarla
Astrea apoya la plantilla transparente sobre la ficha y corrige solo un número.

#### Imagen
- Una ficha técnica de estrella con una plantilla transparente encima que deja ver un solo renglón resaltado.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) sostiene la plantilla.
- Astrea (lechuza con anteojos de latón y chaleco azul) corrige con una pluma; Gheco mira.

### Micro-misión R03-N04-P2 · La tarjeta chica

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco
carta: Pick<T, …> | Pick<Estrella, 'nombre' | 'brillo'> · solo esas propiedades · las demás no están
recompensa: xp 10, oro 10
```

#### Escena
Para la pared del Mirador, Rigel hace tarjetas chicas con solo el nombre y el brillo de cada estrella.

#### Gheco sugiere
`Pick` se queda con **algunas** propiedades:

```ts
type Tarjeta = Pick<Estrella, 'nombre' | 'brillo'>;
```

Las propiedades van como una unión de textos.

#### Desafío
Completá el tipo `Tarjeta`.

#### Pasos
1. Buscá el `___` después de `type Tarjeta =`.
2. Cambialo por `Pick<Estrella, 'nombre' | 'brillo'>`.
3. Tocá **Ejecutar**. Tiene que salir `Sirio ★10`.

#### Código inicial
```typescript
interface Estrella {
  nombre: string;
  brillo: number;
  distancia: number;
}

type Tarjeta = ___;

function tarjeta(e: Estrella): Tarjeta {
  return { nombre: e.nombre, brillo: e.brillo };
}

const t = tarjeta({ nombre: 'Sirio', brillo: 10, distancia: 9 });
console.log(`${t.nombre} ★${t.brillo}`);
```

#### Salida esperada
```
Sirio ★10
```

#### Solución
```typescript
interface Estrella {
  nombre: string;
  brillo: number;
  distancia: number;
}

type Tarjeta = Pick<Estrella, 'nombre' | 'brillo'>;

function tarjeta(e: Estrella): Tarjeta {
  return { nombre: e.nombre, brillo: e.brillo };
}

const t = tarjeta({ nombre: 'Sirio', brillo: 10, distancia: 9 });
console.log(`${t.nombre} ★${t.brillo}`);
```

#### Al superarla
La tarjeta de Sirio queda colgada en la pared, chiquita y clara.

#### Imagen
- Una pared de madera con tarjetitas de estrellas colgadas, cada una con una estrella dibujada y un número de brillo (sin texto legible).
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) cuelga una tarjeta.
- Gheco colgado de otra tarjeta.

### Micro-misión R03-N04-P3 · Sin el número de serie

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco
carta: Omit<T, …> | todas menos esas · para crear sin lo que pone el sistema · Omit<Estrella, 'id'>
recompensa: xp 10, oro 10
```

#### Escena
Cuando se registra una estrella nueva, el número de serie lo pone el catálogo, no quien la registra.

#### Gheco sugiere
`Omit` es lo contrario de `Pick`: **todas menos** las que nombrás.

```ts
function registrar(datos: Omit<Estrella, 'id'>): Estrella { … }
```

Quien llama pasa todo menos el `id`; la función lo agrega.

#### Desafío
Completá el tipo de `datos`.

#### Pasos
1. Buscá el `___` después de `datos:`.
2. Cambialo por `Omit<Estrella, 'id'>`.
3. Tocá **Ejecutar**. Tiene que salir `e-1: Vega` y `e-2: Altair`.

#### Código inicial
```typescript
interface Estrella {
  id: string;
  nombre: string;
  brillo: number;
}

let siguiente = 1;
function registrar(datos: ___): Estrella {
  return { id: `e-${siguiente++}`, ...datos };
}

for (const e of [registrar({ nombre: 'Vega', brillo: 9 }), registrar({ nombre: 'Altair', brillo: 8 })]) {
  console.log(`${e.id}: ${e.nombre}`);
}
```

#### Salida esperada
```
e-1: Vega
e-2: Altair
```

#### Solución
```typescript
interface Estrella {
  id: string;
  nombre: string;
  brillo: number;
}

let siguiente = 1;
function registrar(datos: Omit<Estrella, 'id'>): Estrella {
  return { id: `e-${siguiente++}`, ...datos };
}

for (const e of [registrar({ nombre: 'Vega', brillo: 9 }), registrar({ nombre: 'Altair', brillo: 8 })]) {
  console.log(`${e.id}: ${e.nombre}`);
}
```

#### Al superarla
El catálogo pone los números de serie solo, en orden. Nadie se equivoca de número.

#### Imagen
- Una máquina de latón que estampa números de serie en fichas de estrellas que pasan por una cinta.
- Rigel (chico flaco con pecas, antiparras de latón) pone las fichas en la cinta.
- Gheco sentado sobre el sello.

### Micro-misión R03-N04-P4 · La plantilla que no existe

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco
criatura: skeleton
carta: TS2344 | Pick y Omit solo aceptan nombres que existen · el mensaje dice cuál no cumple
recompensa: xp 10, oro 10
```

#### Escena
Rigel pidió una plantilla con *brilo* y *nombre*. Un **esqueleto** se mete en la letra que falta.

#### Gheco sugiere
`Pick` y `Omit` solo aceptan nombres de propiedades que existen (`keyof`). Si uno está mal escrito, da `TS2344` y dice cuál.

#### Desafío
Corregí el nombre de la propiedad.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `'brilo'` por `'brillo'`.
3. Tocá **Ejecutar**. Tiene que salir `Vega ★9`.

#### Código inicial
```typescript
interface Estrella {
  nombre: string;
  brillo: number;
  distancia: number;
}

type Tarjeta = Pick<Estrella, 'nombre' | 'brilo'>;
const t: Tarjeta = { nombre: 'Vega', brillo: 9 };
console.log(`${t.nombre} ★${t.brillo}`);
```

#### Salida esperada
```
Vega ★9
```

#### Solución
```typescript
interface Estrella {
  nombre: string;
  brillo: number;
  distancia: number;
}

type Tarjeta = Pick<Estrella, 'nombre' | 'brillo'>;
const t: Tarjeta = { nombre: 'Vega', brillo: 9 };
console.log(`${t.nombre} ★${t.brillo}`);
```

#### Al superarla
La plantilla se arma bien y el esqueleto se cae por el agujero de la letra.

#### Imagen
- Una plantilla transparente con un agujero mal recortado, y un esqueleto de alambre chiquito cayéndose por él.
- Rigel (chico flaco con pecas, antiparras de latón con la lupa bajada) recorta una plantilla nueva.
- Gheco mira la caída.

### Micro-misión R03-N04-P5 · Los turnos del Mirador

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: Record<K, V> | Record<Turno, string> · todas las claves de la unión · si falta una, TS2741
recompensa: xp 15, monedas 5
```

#### Escena
Astrea arma la planilla de turnos: quién mira el cielo en cada turno de la noche. No puede quedar ningún turno sin encargado.

#### Gheco sugiere
`Record<Turno, string>` es un objeto con **todas** las claves de `Turno`, cada una con un texto. Si falta una, el compilador avisa (`TS2741`).

#### Desafío
Completá el encargado del turno que falta.

#### Pasos
1. Tocá **Ejecutar** y leé el error: dice qué turno falta.
2. En el `___`, escribí `madrugada: 'Don Péndulo',`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Turno = 'atardecer' | 'noche' | 'madrugada';

const encargados: Record<Turno, string> = {
  atardecer: 'Astrea',
  noche: 'Rigel',
  ___
};

for (const turno of ['atardecer', 'noche', 'madrugada'] as const) {
  console.log(`${turno}: ${encargados[turno]}`);
}
```

#### Salida esperada
```
atardecer: Astrea
noche: Rigel
madrugada: Don Péndulo
```

#### Solución
```typescript
type Turno = 'atardecer' | 'noche' | 'madrugada';

const encargados: Record<Turno, string> = {
  atardecer: 'Astrea',
  noche: 'Rigel',
  madrugada: 'Don Péndulo',
};

for (const turno of ['atardecer', 'noche', 'madrugada'] as const) {
  console.log(`${turno}: ${encargados[turno]}`);
}
```

#### Al superarla
La planilla queda completa. Don Péndulo se entera de que le tocó la madrugada y suspira.

#### Imagen
- Una planilla de turnos de latón con tres casilleros y tres retratitos (sin letras legibles).
- Astrea (lechuza con anteojos de latón y chaleco azul) señala la planilla.
- Rigel (chico flaco con pecas, antiparras de latón) se ríe; al fondo, Don Péndulo (relojero viejo de barba blanca) suspira; Gheco en la planilla.

### Micro-misión R03-N04-P6 · El catálogo completo

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco, Astrea
carta: Todos los tipos útiles | Omit para registrar · Partial para actualizar · Readonly para lo publicado · Pick para la tarjeta
recompensa: xp 15, monedas 5
```

#### Escena
Rigel arma el catálogo entero: registrar estrellas nuevas, actualizarlas, publicar la ficha (que ya nadie toca) y mostrar la tarjeta chica.

#### Gheco sugiere
Todos los tipos útiles salen de la misma ficha `Estrella`. `Readonly<Estrella>` es la ficha publicada: nada se puede cambiar.

#### Desafío
Completá los cuatro tipos.

#### Pasos
1. En `registrar`: `Omit<Estrella, 'id'>`.
2. En `actualizar`: `Partial<Estrella>`.
3. En `publicar`, lo que devuelve: `Readonly<Estrella>`.
4. En `tarjeta`, lo que devuelve: `Pick<Estrella, 'nombre' | 'brillo'>`.
5. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Estrella {
  id: string;
  nombre: string;
  brillo: number;
}

let siguiente = 1;
function registrar(datos: ___): Estrella {
  return { id: `e-${siguiente++}`, ...datos };
}

function actualizar(e: Estrella, cambios: ___): Estrella {
  return { ...e, ...cambios };
}

function publicar(e: Estrella): ___ {
  return Object.freeze({ ...e });
}

function tarjeta(e: Estrella): ___ {
  return { nombre: e.nombre, brillo: e.brillo };
}

const vega = publicar(actualizar(registrar({ nombre: 'Vega', brillo: 9 }), { brillo: 10 }));
console.log(vega.id, tarjeta(vega));
```

#### Salida esperada
```
e-1 { nombre: 'Vega', brillo: 10 }
```

#### Solución
```typescript
interface Estrella {
  id: string;
  nombre: string;
  brillo: number;
}

let siguiente = 1;
function registrar(datos: Omit<Estrella, 'id'>): Estrella {
  return { id: `e-${siguiente++}`, ...datos };
}

function actualizar(e: Estrella, cambios: Partial<Estrella>): Estrella {
  return { ...e, ...cambios };
}

function publicar(e: Estrella): Readonly<Estrella> {
  return Object.freeze({ ...e });
}

function tarjeta(e: Estrella): Pick<Estrella, 'nombre' | 'brillo'> {
  return { nombre: e.nombre, brillo: e.brillo };
}

const vega = publicar(actualizar(registrar({ nombre: 'Vega', brillo: 9 }), { brillo: 10 }));
console.log(vega.id, tarjeta(vega));
```

#### Al superarla
El catálogo queda listo: una sola ficha, cuatro plantillas. Astrea le da a Rigel una **estrella de latón**.

#### Imagen
- Un catálogo de estrellas encuadernado en cuero, con cuatro plantillas transparentes de colores apoyadas al lado.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) ordena las plantillas; Gheco sobre el catálogo.

## R03-N05 · Tipos sacados de otros y satisfies

```meta
tipo: tema
padre: R03-N04
precio: 10
criatura: goblin
temas: cal.tipos, prog.funciones
```

### Crónica

En el cajón de las plantillas hay unas más raras: no transforman fichas, sino **máquinas**. Se apoyan sobre una máquina y copian qué recibe y qué entrega, sin abrirla. Y al fondo, una lupa con una inscripción: *revisá sin achicar*.

—Si una máquina ya existe, no vuelvas a escribir su forma a mano —dice {mentor}—. Copiala. Y si querés revisar una pieza sin perder sus detalles, usá la lupa.

> `NonNullable`, el `filter` con guardia y `satisfies` no están en el material de base (FullCursos): se agregaron porque se usan todo el tiempo.

### Objetivos

- Sacar tipos de una función que ya existe: `ReturnType<typeof f>` y `Parameters<typeof f>`.
- Sacar `null` y `undefined` de un tipo con `NonNullable<T>`, y filtrar una lista con un guardia.
- Hacer obligatorio todo con `Required<T>`.
- Revisar un objeto con `satisfies` sin perder lo que TypeScript deduce.

### Antes de empezar

- R03-N03 (guardias) y R03-N04 (tipos útiles).

### Explicación

#### Copiar la forma de una máquina
```typescript
function medir(nombre: string, brillo: number) {
  return { nombre, brillo, visible: brillo > 5 };
}

type Medicion = ReturnType<typeof medir>;      // { nombre: string; brillo: number; visible: boolean }
type Argumentos = Parameters<typeof medir>;    // [nombre: string, brillo: number]
```

Si mañana `medir` cambia, los tipos cambian solos.

#### Sacar el null
```typescript
type Lectura = number | null;
type Segura = NonNullable<Lectura>;   // number

const lecturas: Lectura[] = [12, null, 4];
const limpias = lecturas.filter((x): x is number => x !== null);   // number[]
```

El `filter` con un **guardia** (`(x): x is number => …`) le dice al compilador que lo que queda ya no tiene `null`.

#### Todo obligatorio
```typescript
interface Config { zoom?: number; filtro?: string }
function aplicar(c: Required<Config>): void { … }   // ahora no puede faltar nada
```

#### satisfies: revisar sin achicar
```typescript
type Color = 'rojo' | 'azul';
const paleta = { rojo: '#e53935', azul: '#1e88e5' } satisfies Record<Color, string>;
```

`satisfies` **revisa** que el objeto cumpla el tipo (que estén todos los colores y ninguno de más), pero el objeto **conserva** el tipo exacto que deduce TypeScript. Con `: Record<Color, string>` también se revisa, pero el tipo queda achicado a «cualquier color».

### Código de ejemplo

```typescript
function medir(nombre: string, brillo: number) {
  return { nombre, brillo, visible: brillo > 5 };
}

type Medicion = ReturnType<typeof medir>;
type Argumentos = Parameters<typeof medir>;

const pedidos: Argumentos[] = [['Vega', 9], ['Polar', 2]];
const resultados: Medicion[] = pedidos.map((args) => medir(...args));

const lecturas: (number | null)[] = [12, null, 4];
const limpias = lecturas.filter((x): x is number => x !== null);

type Color = 'rojo' | 'azul';
const paleta = { rojo: '#e53935', azul: '#1e88e5' } satisfies Record<Color, string>;

for (const r of resultados) console.log(r.nombre, r.visible);
console.log(limpias, paleta.azul);
```

### Salida esperada

```
Vega true
Polar false
[ 12, 4 ] #1e88e5
```

### ¿Para qué sirve?

En un proyecto grande, la misma forma se usa en muchos lugares. Sacarla de donde nace (una función, una constante) evita copias que se desincronizan. `satisfies` es ideal para las configuraciones: revisa que estén todas las claves sin perder los detalles.

### Errores habituales

**Goblin: la copia que no coincide (TS2322).** Si usás `ReturnType` y armás un objeto a mano con otro tipo en una propiedad, el compilador avisa.

**Orco: el filter sin guardia.** `lecturas.filter((x) => x !== null)` en versiones viejas de TypeScript seguía dando `(number | null)[]`. Con el guardia, siempre da `number[]`.

**Esqueleto: una clave de más con satisfies (TS2353).** *El literal de objeto solo puede especificar propiedades conocidas y 'verde' no existe en el tipo 'Record<Color, string>'*.

### Micro-misión R03-N05-P1 · Copiar lo que entrega

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco
carta: ReturnType | ReturnType<typeof medir> · el tipo de lo que devuelve una función que ya existe · cambia solo si la función cambia
recompensa: xp 10, oro 10
```

#### Escena
La máquina de medir devuelve un objeto con tres datos. Rigel necesita guardar varias mediciones y no quiere escribir la forma a mano.

#### Gheco sugiere
`ReturnType<typeof medir>` es el tipo de lo que devuelve `medir`. `typeof medir` es el tipo de la función (el `typeof` de los tipos, de R02-N07).

#### Desafío
Completá el tipo `Medicion`.

#### Pasos
1. Buscá el `___` después de `type Medicion =`.
2. Cambialo por `ReturnType<typeof medir>`.
3. Tocá **Ejecutar**. Tiene que salir `Vega visible: true · Polar visible: false`.

#### Código inicial
```typescript
function medir(nombre: string, brillo: number) {
  return { nombre, brillo, visible: brillo > 5 };
}

type Medicion = ___;

const noche: Medicion[] = [medir('Vega', 9), medir('Polar', 2)];
console.log(noche.map((m) => `${m.nombre} visible: ${m.visible}`).join(' · '));
```

#### Salida esperada
```
Vega visible: true · Polar visible: false
```

#### Solución
```typescript
function medir(nombre: string, brillo: number) {
  return { nombre, brillo, visible: brillo > 5 };
}

type Medicion = ReturnType<typeof medir>;

const noche: Medicion[] = [medir('Vega', 9), medir('Polar', 2)];
console.log(noche.map((m) => `${m.nombre} visible: ${m.visible}`).join(' · '));
```

#### Al superarla
Rigel apoya la plantilla sobre la máquina y la forma de lo que entrega queda dibujada sola.

#### Imagen
- Una plantilla transparente apoyada sobre una máquina de medir de latón, copiando su forma con líneas de luz.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) sostiene la plantilla.
- Gheco sobre la máquina.

### Micro-misión R03-N05-P2 · Copiar lo que recibe

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco
carta: Parameters | Parameters<typeof medir> · una tupla con los parámetros · medir(...args) los pasa todos
recompensa: xp 10, oro 10
```

#### Escena
Astrea deja una lista de pedidos de medición: cada uno con un nombre y un brillo, en el orden que pide la máquina.

#### Gheco sugiere
`Parameters<typeof medir>` es una **tupla** con los tipos de los parámetros: `[nombre: string, brillo: number]`. Con `...args` se pasan todos juntos:

```ts
medir(...args)
```

#### Desafío
Completá el tipo `Pedido`.

#### Pasos
1. Buscá el `___` después de `type Pedido =`.
2. Cambialo por `Parameters<typeof medir>`.
3. Tocá **Ejecutar**. Tiene que salir `Vega:9 Sirio:10`.

#### Código inicial
```typescript
function medir(nombre: string, brillo: number): string {
  return `${nombre}:${brillo}`;
}

type Pedido = ___;

const pedidos: Pedido[] = [['Vega', 9], ['Sirio', 10]];
console.log(pedidos.map((args) => medir(...args)).join(' '));
```

#### Salida esperada
```
Vega:9 Sirio:10
```

#### Solución
```typescript
function medir(nombre: string, brillo: number): string {
  return `${nombre}:${brillo}`;
}

type Pedido = Parameters<typeof medir>;

const pedidos: Pedido[] = [['Vega', 9], ['Sirio', 10]];
console.log(pedidos.map((args) => medir(...args)).join(' '));
```

#### Al superarla
Los pedidos entran a la máquina de a uno, cada uno con lo justo.

#### Imagen
- Una fila de tarjetitas de pedido entrando en la ranura de la máquina de medir de latón.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) acomoda las tarjetas.
- Gheco sobre la ranura.

### Micro-misión R03-N05-P3 · Las lecturas sin huecos

```meta
lugar: Las calderas del Mirador
personajes: Rigel, Gheco
criatura: orc
carta: filter con guardia | lecturas.filter((x): x is number => x !== null) · lo que queda es number[] · NonNullable<T> saca el null del tipo
recompensa: xp 10, oro 10
```

#### Escena
El manómetro mandó lecturas con huecos: algunas son `null`. Rigel necesita el promedio de las que sí hay. Un **orco** acecha en cada hueco.

#### Gheco sugiere
`filter` con un **guardia** saca los `null` y le avisa al compilador:

```ts
const limpias = lecturas.filter((x): x is number => x !== null);
```

`limpias` queda como `number[]`. El tipo `NonNullable<number | null>` es justamente `number`.

#### Desafío
Completá el guardia del `filter`.

#### Pasos
1. Buscá el `___` adentro del `filter`.
2. Cambialo por `(x): x is number => x !== null`.
3. Tocá **Ejecutar**. Tiene que salir `Promedio de 3 lecturas: 40`.

#### Código inicial
```typescript
type Lectura = number | null;
const lecturas: Lectura[] = [30, null, 50, null, 40];

const limpias: NonNullable<Lectura>[] = lecturas.filter(___);
const promedio = limpias.reduce((a, b) => a + b, 0) / limpias.length;
console.log(`Promedio de ${limpias.length} lecturas: ${promedio}`);
```

#### Salida esperada
```
Promedio de 3 lecturas: 40
```

#### Solución
```typescript
type Lectura = number | null;
const lecturas: Lectura[] = [30, null, 50, null, 40];

const limpias: NonNullable<Lectura>[] = lecturas.filter((x): x is number => x !== null);
const promedio = limpias.reduce((a, b) => a + b, 0) / limpias.length;
console.log(`Promedio de ${limpias.length} lecturas: ${promedio}`);
```

#### Al superarla
Los huecos quedan afuera del cálculo y los orcos, sin dónde esconderse.

#### Imagen
- Una tira de papel de un registrador de presión con algunas marcas y algunos huecos, pasando por un colador de latón.
- Un orco chiquito atrapado en el colador.
- Rigel (chico flaco con pecas, antiparras de latón) sostiene el colador; Gheco se ríe.

### Micro-misión R03-N05-P4 · La configuración completa

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: Required<T> | lo contrario de Partial · nada puede faltar · si falta algo, TS2741
recompensa: xp 10, oro 10
```

#### Escena
La configuración del telescopio tiene todo opcional para guardarla a medias. Pero para **encenderlo**, Astrea exige que esté completa.

#### Gheco sugiere
`Required<Config>` es la misma configuración con **todo obligatorio**. Si a la que le pasás le falta algo, el compilador avisa (`TS2741`).

#### Desafío
Agregá el filtro que falta en la configuración de encendido.

#### Pasos
1. Tocá **Ejecutar** y leé qué falta.
2. En el objeto de `encender`, agregá `, filtro: 'azul'`.
3. Tocá **Ejecutar**. Tiene que salir `Encendido: zoom 30, filtro azul`.

#### Código inicial
```typescript
interface Config {
  zoom?: number;
  filtro?: string;
}

function encender(c: Required<Config>): void {
  console.log(`Encendido: zoom ${c.zoom}, filtro ${c.filtro}`);
}

encender({ zoom: 30 });
```

#### Salida esperada
```
Encendido: zoom 30, filtro azul
```

#### Solución
```typescript
interface Config {
  zoom?: number;
  filtro?: string;
}

function encender(c: Required<Config>): void {
  console.log(`Encendido: zoom ${c.zoom}, filtro ${c.filtro}`);
}

encender({ zoom: 30, filtro: 'azul' });
```

#### Al superarla
El telescopio se enciende con el filtro azul puesto. Astrea mira por el ocular: —Ahora sí.

#### Imagen
- El panel de encendido del telescopio de latón con dos perillas ajustadas y una luz verde encendida.
- Astrea (lechuza con anteojos de latón y chaleco azul) mira por el ocular.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) ajusta el filtro azul; Gheco sobre el panel.

### Micro-misión R03-N05-P5 · La lupa que no achica

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco
criatura: skeleton
carta: satisfies | revisa que el objeto cumpla el tipo · conserva lo que deduce TypeScript · una clave de más es TS2353
recompensa: xp 15, monedas 5
```

#### Escena
La paleta de colores de los filtros tiene un color que no existe en la lista oficial: *verde*. Un **esqueleto** lo pintó a escondidas.

#### Gheco sugiere
`satisfies` **revisa** sin achicar: el objeto tiene que cumplir el tipo (todos los colores, ninguno de más), y conserva lo que TypeScript deduce de él.

```ts
const paleta = { … } satisfies Record<Color, string>;
```

Una clave de más da `TS2353`.

#### Desafío
Borrá el color que no está en la lista.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Borrá `verde: '#43a047',` del objeto.
3. Tocá **Ejecutar**. Tiene que salir `rojo #e53935 · azul #1e88e5`.

#### Código inicial
```typescript
type Color = 'rojo' | 'azul';

const paleta = {
  rojo: '#e53935',
  azul: '#1e88e5',
  verde: '#43a047',
} satisfies Record<Color, string>;

console.log(`rojo ${paleta.rojo} · azul ${paleta.azul}`);
```

#### Salida esperada
```
rojo #e53935 · azul #1e88e5
```

#### Solución
```typescript
type Color = 'rojo' | 'azul';

const paleta = {
  rojo: '#e53935',
  azul: '#1e88e5',
} satisfies Record<Color, string>;

console.log(`rojo ${paleta.rojo} · azul ${paleta.azul}`);
```

#### Al superarla
El filtro verde desaparece de la caja. El esqueleto se va con su pincel.

#### Imagen
- Una caja de filtros de vidrio de colores (rojo y azul) y un hueco donde había uno verde.
- Un esqueleto de alambre chiquito escapando con un pincel verde.
- Rigel (chico flaco con pecas, antiparras de latón con la lupa bajada) revisa la caja; Gheco mira.

### Micro-misión R03-N05-P6 · El informe de la máquina

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: Todo junto | Parameters para los pedidos · ReturnType para los resultados · filter con guardia para descartar
recompensa: xp 15, monedas 5
```

#### Escena
Astrea manda una tanda de pedidos de medición. Algunos vuelven vacíos (la estrella estaba tapada). Rigel arma el informe solo con los que volvieron.

#### Gheco sugiere
- `Parameters<typeof medir>` para los pedidos;
- `ReturnType<typeof medir>` es `{ … } | null`;
- `NonNullable<…>` y el `filter` con guardia para quedarte con los que volvieron.

#### Desafío
Completá el tipo `Medicion` y el guardia del `filter`.

#### Pasos
1. El primer `___`: `NonNullable<ReturnType<typeof medir>>`.
2. El segundo `___`: `(m): m is Medicion => m !== null`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
function medir(nombre: string, tapada: boolean) {
  return tapada ? null : { nombre, brillo: nombre.length };
}

type Pedido = Parameters<typeof medir>;
type Medicion = ___;

const pedidos: Pedido[] = [['Vega', false], ['Polar', true], ['Altair', false]];
const resultados = pedidos.map((args) => medir(...args)).filter(___);
for (const m of resultados) console.log(`${m.nombre}: ${m.brillo}`);
```

#### Salida esperada
```
Vega: 4
Altair: 6
```

#### Solución
```typescript
function medir(nombre: string, tapada: boolean) {
  return tapada ? null : { nombre, brillo: nombre.length };
}

type Pedido = Parameters<typeof medir>;
type Medicion = NonNullable<ReturnType<typeof medir>>;

const pedidos: Pedido[] = [['Vega', false], ['Polar', true], ['Altair', false]];
const resultados = pedidos.map((args) => medir(...args)).filter((m): m is Medicion => m !== null);
for (const m of resultados) console.log(`${m.nombre}: ${m.brillo}`);
```

#### Al superarla
El informe sale limpio, sin huecos. Astrea le da a Rigel una **estrella de latón**.

#### Imagen
- Un informe de observación con dos estrellas anotadas y un casillero tachado con una nube dibujada.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) guarda el informe; Gheco sobre la mesa.

## R03-N06 · Tipos que fabrican tipos

```meta
tipo: tema
padre: R03-N05
precio: 10
criatura: goblin
temas: cal.tipos, poo.genericos
```

### Crónica

En lo más alto del Telescopio, Rigel encuentra el taller secreto del Vidriero: una máquina que **fabrica plantillas**. Le das una ficha, le decís qué hacer con cada casillero, y saca una plantilla nueva. Al lado, un sello de palabras que arma nombres de eventos con prefijos.

—Así hizo el Vidriero todas las plantillas que usaste —dice {mentor}—. `Partial`, `Readonly`, `Record`… no son magia. Son tipos que recorren otros tipos.

> Este nodo no está en el material de base (FullCursos): se agregó porque explica cómo están hechos los tipos útiles y porque aparece en muchas bibliotecas.

### Objetivos

- Escribir un **mapped type**: `{ [K in keyof T]: … }`, que recorre las propiedades de un tipo.
- Usar los modificadores `?` y `readonly` en un mapped type (y armar tu propio `Partial`).
- Escribir **template literal types**: tipos de texto armados con `` `al${…}` `` y `Capitalize`.
- Renombrar las claves con `as`.

### Antes de empezar

- R02-N07 (`keyof`, `T[K]`) y R03-N04 (tipos útiles).

### Explicación

#### Recorrer las propiedades
```typescript
type Estrella = { nombre: string; brillo: number };

type Revisada = { [K in keyof Estrella]: boolean };
// { nombre: boolean; brillo: boolean }
```

`[K in keyof Estrella]` recorre cada nombre (`'nombre'`, después `'brillo'`). Lo que va después de los dos puntos es el tipo de cada propiedad nueva. Con `T[K]` se conserva el tipo original.

#### Tu propio Partial
```typescript
type Opcional<T> = { [K in keyof T]?: T[K] };
type SoloLectura<T> = { readonly [K in keyof T]: T[K] };
```

Así están hechos `Partial` y `Readonly`.

#### Tipos de texto armados
```typescript
type Accion = 'girar' | 'trabar';
type Evento = `al${Capitalize<Accion>}`;   // 'alGirar' | 'alTrabar'
```

`Capitalize` pasa la primera letra a mayúscula. También hay `Uppercase`, `Lowercase` y `Uncapitalize`.

#### Renombrar con as
```typescript
type Manejadores = { [A in Accion as `al${Capitalize<A>}`]: () => string };
// { alGirar: () => string; alTrabar: () => string }
```

### Código de ejemplo

```typescript
type Estrella = { nombre: string; brillo: number };
type Revisada = { [K in keyof Estrella]: boolean };
type Opcional<T> = { [K in keyof T]?: T[K] };

type Accion = 'girar' | 'trabar';
type Manejadores = { [A in Accion as `al${Capitalize<A>}`]: () => string };

const revisada: Revisada = { nombre: true, brillo: false };
const borrador: Opcional<Estrella> = { nombre: 'Vega' };
const manejadores: Manejadores = {
  alGirar: () => 'gira',
  alTrabar: () => 'se traba',
};

console.log(revisada, borrador);
console.log(manejadores.alGirar(), '/', manejadores.alTrabar());
```

### Salida esperada

```
{ nombre: true, brillo: false } { nombre: 'Vega' }
gira / se traba
```

### ¿Para qué sirve?

Con estos tipos se escriben reglas como «para cada campo del formulario, un mensaje de error» o «para cada acción, un evento `alAccion`» una sola vez. Si se agrega un campo o una acción, todo lo demás se actualiza solo. Muchas bibliotecas los usan; ahora vas a poder leer sus tipos.

### Errores habituales

**Goblin: un nombre de evento que no existe (TS2322).** *El tipo '"alFrenar"' no se puede asignar al tipo '"alGirar" | "alTrabar"'*.

**Esqueleto: falta un manejador (TS2741).** Si el mapped type pide uno por acción, tienen que estar todos.

**Leer de adentro hacia afuera.** Estos tipos parecen difíciles. Leelos por partes: qué se recorre (`in`), cómo se llama cada clave (`as`) y qué tipo tiene cada una (después de `:`).

### Micro-misión R03-N06-P1 · La lista de control

```meta
lugar: El taller secreto del Vidriero
personajes: Rigel, Gheco, Astrea
carta: Mapped type | { [K in keyof Estrella]: boolean } · recorre cada propiedad · le da un tipo nuevo
recompensa: xp 10, oro 10
```

#### Escena
Astrea quiere una lista de control para cada ficha de estrella: un tilde por cada dato revisado.

#### Gheco sugiere
Un **mapped type** recorre las propiedades de otro tipo:

```ts
type Revisada = { [K in keyof Estrella]: boolean };
```

Por cada nombre de `Estrella`, una propiedad del mismo nombre de tipo `boolean`.

#### Desafío
Completá el mapped type.

#### Pasos
1. Buscá el `___` adentro de las llaves de `Revisada`.
2. Cambialo por `[K in keyof Estrella]: boolean`.
3. Tocá **Ejecutar**. Tiene que salir `nombre: ✓ · brillo: ✗ · distancia: ✓`.

#### Código inicial
```typescript
type Estrella = { nombre: string; brillo: number; distancia: number };
type Revisada = { ___ };

const control: Revisada = { nombre: true, brillo: false, distancia: true };
console.log(Object.entries(control).map(([k, v]) => `${k}: ${v ? '✓' : '✗'}`).join(' · '));
```

#### Salida esperada
```
nombre: ✓ · brillo: ✗ · distancia: ✓
```

#### Solución
```typescript
type Estrella = { nombre: string; brillo: number; distancia: number };
type Revisada = { [K in keyof Estrella]: boolean };

const control: Revisada = { nombre: true, brillo: false, distancia: true };
console.log(Object.entries(control).map(([k, v]) => `${k}: ${v ? '✓' : '✗'}`).join(' · '));
```

#### Al superarla
La máquina de plantillas saca una lista de control con un casillero por cada dato. Astrea la usa esa misma noche.

#### Imagen
- Una máquina de latón en un taller escondido bajo la cúpula, sacando una plantilla de cartulina con casilleros.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) toma la plantilla.
- Astrea (lechuza con anteojos de latón y chaleco azul) mira asombrada; Gheco sobre la máquina.

### Micro-misión R03-N06-P2 · Tu propio Partial

```meta
lugar: El taller secreto del Vidriero
personajes: Rigel, Gheco
carta: Modificadores | { [K in keyof T]?: T[K] } · el ? hace todo opcional · T[K] conserva el tipo · así está hecho Partial
recompensa: xp 10, oro 10
```

#### Escena
Rigel quiere entender cómo funciona la plantilla `Partial`. La arma él mismo con la máquina del Vidriero.

#### Gheco sugiere
En un mapped type se pueden agregar modificadores. Con `?`, todas las propiedades quedan opcionales; con `T[K]`, cada una conserva su tipo:

```ts
type Opcional<T> = { [K in keyof T]?: T[K] };
```

Es exactamente lo que hace `Partial<T>`.

#### Desafío
Completá `Opcional<T>`.

#### Pasos
1. Buscá el `___` adentro de las llaves.
2. Cambialo por `[K in keyof T]?: T[K]`.
3. Tocá **Ejecutar**. Tiene que salir `Borrador: Vega (brillo sin medir)`.

#### Código inicial
```typescript
type Opcional<T> = { ___ };
type Estrella = { nombre: string; brillo: number };

const borrador: Opcional<Estrella> = { nombre: 'Vega' };
console.log(`Borrador: ${borrador.nombre} (brillo ${borrador.brillo ?? 'sin medir'})`);
```

#### Salida esperada
```
Borrador: Vega (brillo sin medir)
```

#### Solución
```typescript
type Opcional<T> = { [K in keyof T]?: T[K] };
type Estrella = { nombre: string; brillo: number };

const borrador: Opcional<Estrella> = { nombre: 'Vega' };
console.log(`Borrador: ${borrador.nombre} (brillo ${borrador.brillo ?? 'sin medir'})`);
```

#### Al superarla
La plantilla que salió es idéntica a la `Partial` del cajón. Rigel se ríe: —No era magia.

#### Imagen
- Dos plantillas transparentes idénticas superpuestas sobre una mesa.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) las compara contra la luz.
- Gheco haciendo un gesto de sorpresa.

### Micro-misión R03-N06-P3 · El sello de los eventos

```meta
lugar: El taller secreto del Vidriero
personajes: Rigel, Gheco
carta: Template literal type | `al${Capitalize<Accion>}` · arma tipos de texto · Capitalize pasa la primera a mayúscula
recompensa: xp 10, oro 10
```

#### Escena
El sello de palabras del Vidriero arma nombres de eventos: a *girar* le pone *al* adelante y la mayúscula en su lugar: *alGirar*.

#### Gheco sugiere
Los **template literal types** arman tipos de texto con la misma sintaxis de los template literals:

```ts
type Evento = `al${Capitalize<Accion>}`;
```

Con `Accion = 'girar' | 'trabar'`, da `'alGirar' | 'alTrabar'`.

#### Desafío
Completá el tipo `Evento`.

#### Pasos
1. Buscá el `___` después de `type Evento =`.
2. Cambialo por `` `al${Capitalize<Accion>}` ``.
3. Tocá **Ejecutar**. Tiene que salir `alGirar`.

#### Código inicial
```typescript
type Accion = 'girar' | 'trabar';
type Evento = ___;

const evento: Evento = 'alGirar';
console.log(evento);
```

#### Salida esperada
```
alGirar
```

#### Solución
```typescript
type Accion = 'girar' | 'trabar';
type Evento = `al${Capitalize<Accion>}`;

const evento: Evento = 'alGirar';
console.log(evento);
```

#### Al superarla
El sello estampa *alGirar* en una tarjeta. La letra sale perfecta.

#### Imagen
- Un sello de bronce con letras intercambiables estampando una palabra de luz sobre una tarjeta (sin letras legibles).
- Rigel (chico flaco con pecas, antiparras de latón) aprieta el sello.
- Gheco con tinta en la nariz.

### Micro-misión R03-N06-P4 · El evento que no existe

```meta
lugar: El taller secreto del Vidriero
personajes: Rigel, Gheco
criatura: goblin
carta: Un texto que no está en el tipo | 'alFrenar' no es 'alGirar' | 'alTrabar' · TS2322
recompensa: xp 15, monedas 5
```

#### Escena
Un goblin estampó *alFrenar*, un evento que el Planisferio no tiene.

#### Gheco sugiere
El tipo `Evento` solo acepta los textos que salen de `Accion`. `'alFrenar'` no está: da `TS2322`, y el mensaje muestra los que valen.

#### Desafío
Cambiá el evento por uno que exista: `'alTrabar'`.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `'alFrenar'` por `'alTrabar'`.
3. Tocá **Ejecutar**. Tiene que salir `Escuchando: alTrabar`.

#### Código inicial
```typescript
type Accion = 'girar' | 'trabar';
type Evento = `al${Capitalize<Accion>}`;

const evento: Evento = 'alFrenar';
console.log(`Escuchando: ${evento}`);
```

#### Salida esperada
```
Escuchando: alTrabar
```

#### Solución
```typescript
type Accion = 'girar' | 'trabar';
type Evento = `al${Capitalize<Accion>}`;

const evento: Evento = 'alTrabar';
console.log(`Escuchando: ${evento}`);
```

#### Al superarla
La tarjeta con el evento falso se borra sola. El goblin se queda con el sello manchado.

#### Imagen
- Una tarjeta de cartón cuya palabra se borra en humo, y al lado una tarjeta nueva bien estampada.
- Un goblin chiquito con un engranaje en la espalda y las manos manchadas de tinta.
- Rigel (chico flaco con pecas, antiparras de latón) estampa la tarjeta buena; Gheco mira.

### Micro-misión R03-N06-P5 · Un manejador por acción

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco, Astrea
carta: Renombrar con as | { [A in Accion as `al${Capitalize<A>}`]: () => string } · una clave por acción · si falta una, TS2741
recompensa: xp 15, monedas 5
```

#### Escena
Astrea quiere que el Planisferio tenga un manejador por cada acción. Si mañana se agrega una acción, que el compilador pida su manejador.

#### Gheco sugiere
En un mapped type, `as` **renombra** cada clave:

```ts
type Manejadores = { [A in Accion as `al${Capitalize<A>}`]: () => string };
```

Por cada acción, una clave `alAccion` con una función. Si falta alguna, `TS2741`.

#### Desafío
Agregá el manejador que falta.

#### Pasos
1. Tocá **Ejecutar** y leé qué falta.
2. En el `___`, escribí `alDetener: () => 'se detiene',`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Accion = 'girar' | 'trabar' | 'detener';
type Manejadores = { [A in Accion as `al${Capitalize<A>}`]: () => string };

const planisferio: Manejadores = {
  alGirar: () => 'gira',
  alTrabar: () => 'se traba',
  ___
};

for (const nombre of Object.keys(planisferio) as (keyof Manejadores)[]) {
  console.log(`${nombre}: ${planisferio[nombre]()}`);
}
```

#### Salida esperada
```
alGirar: gira
alTrabar: se traba
alDetener: se detiene
```

#### Solución
```typescript
type Accion = 'girar' | 'trabar' | 'detener';
type Manejadores = { [A in Accion as `al${Capitalize<A>}`]: () => string };

const planisferio: Manejadores = {
  alGirar: () => 'gira',
  alTrabar: () => 'se traba',
  alDetener: () => 'se detiene',
};

for (const nombre of Object.keys(planisferio) as (keyof Manejadores)[]) {
  console.log(`${nombre}: ${planisferio[nombre]()}`);
}
```

#### Al superarla
El Planisferio aprende su acción nueva sin que se olvide ninguna. Astrea le da a Rigel una **estrella de latón**: —El Vidriero estaría orgulloso.

#### Imagen
- El panel del planetario mecánico con tres palancas, cada una con su chapita grabada (sin letras legibles).
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) baja la tercera palanca; Gheco aplaude.

## R03-N07 · Módulos tipados

```meta
tipo: tema
padre: R03-N06
precio: 10
criatura: skeleton
temas: js.modulos, cal.tipos
```

### Crónica

El Telescopio es enorme, y sus planos ocupan un montón de láminas. Astrea las tiene separadas: una lámina para las lentes, otra para los motores, otra para las estrellas. Cada lámina dice qué **exporta** (lo que otras láminas pueden usar) y qué **importa** (lo que trae de otras).

—Un plano entero en una sola hoja no lo entiende nadie —dice {mentor}—. Se parte en archivos. Y los tipos viajan entre archivos igual que el código.

### Objetivos

- Exportar e importar clases, funciones **y tipos** entre archivos (`export`, `import`).
- Usar `import type` para traer solo un tipo.
- Escribir la ruta con `.js` (`'./vec2.js'`), aunque el archivo sea `vec2.ts`.
- Leer el error de importar algo que no existe (`TS2305`, o `TS2724` si hay un nombre parecido).

### Antes de empezar

- De JavaScript: módulos con `export` e `import` (en el curso de JavaScript, R03).
- R02: clases e interfaces.

### Explicación

#### Exportar tipos
```typescript
// vec2.ts
export class Vec2 {
  constructor(public x: number, public y: number) {}
}
export interface ConPosicion {
  posicion: Vec2;
}
```

Una `interface` o un `type` se exportan igual que una clase. No generan nada en el JavaScript: solo viajan para el compilador.

#### Importar
```typescript
// main.ts
import { Vec2 } from './vec2.js';
import type { ConPosicion } from './vec2.js';
```

- `import type` trae **solo** el tipo, y se borra entero al compilar. Deja claro que no se usa como valor.
- **La ruta lleva `.js`**, aunque el archivo se llame `vec2.ts`: es la ruta del archivo que va a existir cuando se compile. Es lo que pide el estándar de JavaScript y Node (`"module": "nodenext"`). Algunas herramientas aceptan `'./vec2'` sin extensión, pero en la caja (y en el navegador) no anda.

#### En las micro-misiones
Los otros archivos aparecen en el tablero, debajo del editor. Los podés leer, pero no cambiar: solo trabajás en `main.ts`.

### Código de ejemplo

```typescript
// En una micro-misión, vec2.ts es otro archivo; acá va todo junto para ver la idea.
class Vec2 {
  constructor(public x: number, public y: number) {}
  sumar(o: Vec2): Vec2 {
    return new Vec2(this.x + o.x, this.y + o.y);
  }
}

interface ConPosicion {
  posicion: Vec2;
}

function describir(e: ConPosicion): string {
  return `en (${e.posicion.x}, ${e.posicion.y})`;
}

const telescopio = { nombre: 'Mayor', posicion: new Vec2(3, 4).sumar(new Vec2(1, 1)) };
console.log(telescopio.nombre, describir(telescopio));
```

### Salida esperada

```
Mayor en (4, 5)
```

### ¿Para qué sirve?

Todo proyecto real se parte en archivos: uno por clase, uno para los tipos compartidos, uno para la configuración. TypeScript revisa los tipos **a través** de los archivos: si cambia una interface en un archivo, avisa en todos los que la usan.

### Errores habituales

**Esqueleto: importar algo que no se exporta (TS2305 o TS2724).** Si hay un nombre parecido, el compilador lo sugiere: *""./vec2.js"" no tiene ningún miembro exportado con el nombre "Vec". ¿Pretendía usar "Vec2"?* Revisá el nombre (y que el otro archivo lo tenga con `export`).

**Esqueleto: la ruta sin .js.** `from './vec2'` puede compilar, pero al ejecutar no encuentra el archivo. Escribí `'./vec2.js'`.

**Usar como valor algo traído con import type.** `import type { Vec2 }` y después `new Vec2(…)` da error: con `import type` solo se puede usar como tipo.

### Micro-misión R03-N07-P1 · Traer la lámina de las posiciones

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: import | import { Vec2 } from './vec2.js'; · la ruta lleva .js aunque el archivo sea .ts · el otro archivo está en el tablero
recompensa: xp 10, oro 10
```

#### Escena
Astrea le alcanza a Rigel la lámina de las posiciones (`vec2.ts`). Para usarla en su plano, tiene que importarla.

#### Gheco sugiere
El archivo `vec2.ts` está en el tablero, debajo del editor: exporta la clase `Vec2`. Para usarla en `main.ts`:

```ts
import { Vec2 } from './vec2.js';
```

La ruta lleva `.js`: es la del archivo que existe cuando se compila.

#### Desafío
Completá la primera línea con el `import`.

#### Pasos
1. Buscá el `___` en la primera línea.
2. Cambialo por `import { Vec2 } from './vec2.js';`.
3. Tocá **Ejecutar**. Tiene que salir `Telescopio en (4, 5)`.

#### Archivos
vec2.ts
```typescript
export class Vec2 {
  constructor(public x: number, public y: number) {}

  sumar(o: Vec2): Vec2 {
    return new Vec2(this.x + o.x, this.y + o.y);
  }
}
```

#### Código inicial
```typescript
___

const posicion = new Vec2(3, 4).sumar(new Vec2(1, 1));
console.log(`Telescopio en (${posicion.x}, ${posicion.y})`);
```

#### Salida esperada
```
Telescopio en (4, 5)
```

#### Solución
```typescript
import { Vec2 } from './vec2.js';

const posicion = new Vec2(3, 4).sumar(new Vec2(1, 1));
console.log(`Telescopio en (${posicion.x}, ${posicion.y})`);
```

#### Al superarla
Rigel une las dos láminas con un clip de bronce. El plano del telescopio empieza a tener sentido.

#### Imagen
- Dos láminas de plano unidas con un clip de bronce sobre la mesa del telescopio, con una flecha de luz de una a la otra.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) pone el clip.
- Astrea (lechuza con anteojos de latón y chaleco azul) asiente; Gheco sobre las láminas.

### Micro-misión R03-N07-P2 · El nombre que no está

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco
criatura: skeleton
carta: TS2724 | importar algo que el archivo no exporta · el compilador sugiere el nombre parecido · revisá el tablero
recompensa: xp 10, oro 10
```

#### Escena
Rigel importó `Vec` de la lámina, pero la lámina exporta otra cosa. Un **esqueleto** se ríe en el hueco.

#### Gheco sugiere
Si importás un nombre que el otro archivo no exporta, el compilador avisa (`TS2724` si hay uno parecido, y te lo sugiere; `TS2305` si no). Mirá en el tablero cómo se llama de verdad.

#### Desafío
Corregí el nombre importado y el que usás.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el `import`, cambiá `Vec` por `Vec2`.
3. En la tercera línea, cambiá `new Vec(` por `new Vec2(`.
4. Tocá **Ejecutar**. Tiene que salir `Lente en (2, 7)`.

#### Archivos
vec2.ts
```typescript
export class Vec2 {
  constructor(public x: number, public y: number) {}
}
```

#### Código inicial
```typescript
import { Vec } from './vec2.js';

const lente = new Vec(2, 7);
console.log(`Lente en (${lente.x}, ${lente.y})`);
```

#### Salida esperada
```
Lente en (2, 7)
```

#### Solución
```typescript
import { Vec2 } from './vec2.js';

const lente = new Vec2(2, 7);
console.log(`Lente en (${lente.x}, ${lente.y})`);
```

#### Al superarla
El esqueleto se queda sin chiste. El nombre bien escrito encaja en la lámina.

#### Imagen
- Una lámina de plano con un casillero de nombre corregido y un esqueleto de alambre chiquito saliendo de él.
- Rigel (chico flaco con pecas, antiparras de latón) corrige con una pluma.
- Gheco señala el tablero.

### Micro-misión R03-N07-P3 · Solo la forma

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco
carta: import type | import type { ConPosicion } from './vec2.js'; · trae solo el tipo · se borra al compilar
recompensa: xp 10, oro 10
```

#### Escena
De la lámina de las posiciones, Rigel solo necesita la ficha `ConPosicion`, no ninguna pieza. Astrea le enseña a pedir solo la forma.

#### Gheco sugiere
`import type` trae **solo un tipo**:

```ts
import type { ConPosicion } from './vec2.js';
```

Se borra entero al compilar, y deja claro que no se usa como valor.

#### Desafío
Completá la línea del `import type`.

#### Pasos
1. Buscá el `___` en la segunda línea.
2. Cambialo por `import type { ConPosicion } from './vec2.js';`.
3. Tocá **Ejecutar**. Tiene que salir `Ocular en (1, 2)`.

#### Archivos
vec2.ts
```typescript
export class Vec2 {
  constructor(public x: number, public y: number) {}
}

export interface ConPosicion {
  nombre: string;
  posicion: Vec2;
}
```

#### Código inicial
```typescript
import { Vec2 } from './vec2.js';
___

function describir(e: ConPosicion): string {
  return `${e.nombre} en (${e.posicion.x}, ${e.posicion.y})`;
}

console.log(describir({ nombre: 'Ocular', posicion: new Vec2(1, 2) }));
```

#### Salida esperada
```
Ocular en (1, 2)
```

#### Solución
```typescript
import { Vec2 } from './vec2.js';
import type { ConPosicion } from './vec2.js';

function describir(e: ConPosicion): string {
  return `${e.nombre} en (${e.posicion.x}, ${e.posicion.y})`;
}

console.log(describir({ nombre: 'Ocular', posicion: new Vec2(1, 2) }));
```

#### Al superarla
Rigel calca solo la ficha, sin traer ninguna pieza de la lámina.

#### Imagen
- Una hoja de calco sobre una lámina de plano, copiando solo una ficha con líneas punteadas.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) calca con un lápiz.
- Gheco sosteniendo la hoja.

### Micro-misión R03-N07-P4 · La ruta sin extensión

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco
criatura: skeleton
carta: La ruta lleva .js | './vec2' compila pero al ejecutar no se encuentra · './vec2.js' anda siempre
recompensa: xp 15, monedas 5
```

#### Escena
Rigel escribió la ruta sin la extensión. El compilador no se queja, pero al ejecutar, la caja no encuentra la lámina.

#### Gheco sugiere
`'./vec2'` (sin extensión) lo aceptan algunas herramientas, pero el navegador y Node buscan el archivo **exacto**. Después de compilar, el archivo se llama `vec2.js`, así que la ruta tiene que ser `'./vec2.js'`.

#### Desafío
Agregale `.js` a la ruta.

#### Pasos
1. Tocá **Ejecutar**: compila, pero falla al ejecutar.
2. Cambiá `'./vec2'` por `'./vec2.js'`.
3. Tocá **Ejecutar**. Tiene que salir `Motor en (0, 9)`.

#### Archivos
vec2.ts
```typescript
export class Vec2 {
  constructor(public x: number, public y: number) {}
}
```

#### Código inicial
```typescript
import { Vec2 } from './vec2';

const motor = new Vec2(0, 9);
console.log(`Motor en (${motor.x}, ${motor.y})`);
```

#### Salida esperada
```
Motor en (0, 9)
```

#### Solución
```typescript
import { Vec2 } from './vec2.js';

const motor = new Vec2(0, 9);
console.log(`Motor en (${motor.x}, ${motor.y})`);
```

#### Al superarla
La caja encuentra la lámina y el motor aparece en su lugar.

#### Imagen
- Un sobre con una dirección incompleta devuelto al remitente, y otro con la dirección completa entrando en un buzón de latón.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) completa la dirección.
- Gheco con el sobre devuelto en la mano.

### Micro-misión R03-N07-P5 · Las tres láminas

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: Varios archivos | lente.ts importa de vec2.ts · main.ts importa de los dos · import type para la interface
recompensa: xp 15, monedas 5
```

#### Escena
El plano completo del telescopio tiene tres láminas: posiciones, lentes y el plano principal. Las lentes usan las posiciones, y el principal usa las dos.

#### Gheco sugiere
Un archivo puede importar de otro que a su vez importa de un tercero: `lente.ts` importa `Vec2` de `vec2.ts`, y `main.ts` importa de los dos. El tablero muestra los dos archivos.

#### Desafío
Completá los dos `import` de `main.ts`.

#### Pasos
1. El primer `___`: `import { Vec2 } from './vec2.js';`.
2. El segundo `___`: `import { Lente } from './lente.js';`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Archivos
vec2.ts
```typescript
export class Vec2 {
  constructor(public x: number, public y: number) {}
}
```

lente.ts
```typescript
import { Vec2 } from './vec2.js';

export class Lente {
  constructor(public aumento: number, public posicion: Vec2) {}

  describir(): string {
    return `lente ${this.aumento}x en (${this.posicion.x}, ${this.posicion.y})`;
  }
}
```

#### Código inicial
```typescript
___
___

const lentes = [new Lente(30, new Vec2(0, 4)), new Lente(8, new Vec2(0, 1))];
for (const l of lentes) console.log(l.describir());
```

#### Salida esperada
```
lente 30x en (0, 4)
lente 8x en (0, 1)
```

#### Solución
```typescript
import { Vec2 } from './vec2.js';
import { Lente } from './lente.js';

const lentes = [new Lente(30, new Vec2(0, 4)), new Lente(8, new Vec2(0, 1))];
for (const l of lentes) console.log(l.describir());
```

#### Al superarla
Las tres láminas quedan unidas en una carpeta de cuero. Astrea le da a Rigel una **estrella de latón**: —Ahora cualquiera puede leer tus planos.

#### Imagen
- Una carpeta de cuero con tres láminas de planos unidas por clips de bronce y flechas de luz entre ellas.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) cierra la carpeta; Gheco sobre ella.

## R03-N08 · Jefe: el Cerbero de las Uniones

```meta
tipo: jefe
padre: R03-N07
precio: 10
criatura: dragon
insignia: Collar del Cerbero
insignia_descripcion: Venciste al Cerbero de las Uniones: sabés qué es cada cosa antes de tocarla.
usa: cal.tipos, prog.condicionales, err.validacion, poo.genericos
```

### Crónica

Una madrugada, el Telescopio enloquece: apunta a cualquier lado y anota cosas sin sentido. En la cúpula, enroscado alrededor del tubo, hay un autómata de bronce con **tres cabezas de perro**: el **Cerbero de las Uniones**. Cada cabeza ladra un tipo distinto, y entre las tres confunden todo lo que entra.

—Cada cabeza dice que lo que entra es suyo —dice {mentor}—. Para pasar, tenés que saber, en cada momento, **cuál** de las tres tiene razón.

### Objetivos

- Integrar todo lo de la rama: narrowing, uniones discriminadas, `never`, guardias, tipos útiles y tipos fabricados.
- Tratar cada caso de una unión, sin olvidar ninguno.
- Validar lo que llega de afuera antes de usarlo.

### Antes de empezar

- Todos los nodos del Telescopio (R03-N01 a R03-N07).

### Explicación

#### Cómo encarar un jefe
1. **Leé la consigna entera** y anotá qué formas puede tener lo que entra.
2. **Preguntá antes de usar**: `typeof`, `in`, `instanceof`, la etiqueta o un guardia.
3. **Cerrá con `never`**: que el compilador avise si falta un caso.
4. **Ejecutá después de cada paso.**

#### Las trampas del Cerbero (y la verdad)
| El Cerbero dice… | La verdad |
|---|---|
| "si es una unión, usalo como quieras" | solo vale lo que tienen todos; para lo demás, preguntá |
| "con tres casos alcanza" | si mañana hay cuatro, `never` te avisa |
| "lo que llega de afuera ya viene bien" | pasa por un guardia antes de usarse |
| "para actualizar, mandá la ficha entera" | `Partial` para cambios, `Omit` para crear |

### Micro-misión R03-N08-P1 · La primera cabeza

```meta
lugar: La cúpula del Telescopio
personajes: Rigel, Gheco, el Cerbero de las Uniones
criatura: goblin
carta: Trampa 1 | number | string | string[] · typeof y Array.isArray · cada rama con lo suyo
recompensa: xp 15, monedas 3
```

#### Escena
La primera cabeza ladra medidas que llegan de tres formas: un número, un texto con milímetros o una lista de textos. Rigel tiene que convertirlas todas a un total.

#### Gheco sugiere
Tres formas, tres preguntas:
- `typeof m === 'number'`: ya es un número;
- `Array.isArray(m)`: es una lista de textos, se suma cada uno;
- lo que queda es un texto.

`Number.parseFloat` lee el número del principio de un texto.

#### Desafío
Completá las dos preguntas.

#### Pasos
1. El primer `___`: `typeof m === 'number'`.
2. El segundo `___`: `Array.isArray(m)`.
3. Tocá **Ejecutar**. Tiene que salir `Total: 25.5 mm`.

#### Código inicial
```typescript
type Medida = number | string | string[];

function aMilimetros(m: Medida): number {
  if (___) return m;
  if (___) return m.reduce((suma, t) => suma + Number.parseFloat(t), 0);
  return Number.parseFloat(m);
}

const medidas: Medida[] = [12, '4.5 mm', ['3 mm', '6 mm']];
let total = 0;
for (const m of medidas) total += aMilimetros(m);
console.log(`Total: ${total} mm`);
```

#### Salida esperada
```
Total: 25.5 mm
```

#### Solución
```typescript
type Medida = number | string | string[];

function aMilimetros(m: Medida): number {
  if (typeof m === 'number') return m;
  if (Array.isArray(m)) return m.reduce((suma, t) => suma + Number.parseFloat(t), 0);
  return Number.parseFloat(m);
}

const medidas: Medida[] = [12, '4.5 mm', ['3 mm', '6 mm']];
let total = 0;
for (const m of medidas) total += aMilimetros(m);
console.log(`Total: ${total} mm`);
```

#### Al superarla
La primera cabeza se queda callada, con la boca llena de medidas bien convertidas.

#### Imagen
- Un autómata de bronce con tres cabezas de perro enroscado en el tubo de un telescopio enorme, bajo la cúpula abierta; una de las cabezas cerrada y quieta.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) sostiene el calibre en alto.
- Gheco en su hombro.

### Micro-misión R03-N08-P2 · La segunda cabeza

```meta
lugar: La cúpula del Telescopio
personajes: Rigel, Gheco, el Cerbero de las Uniones
criatura: ogre
carta: Trampa 2 | unión discriminada con tres señales · switch exhaustivo con never · la cuarta señal no se escapa
recompensa: xp 15, monedas 3
```

#### Escena
La segunda cabeza manda señales de tres clases: *ladrido*, *gruñido* y *aullido*. Rigel tiene que traducirlas, y que el compilador avise si aparece una cuarta.

#### Gheco sugiere
Una unión discriminada con `tipo`, un `switch` con un `case` por señal, y el `default` con `never`.

#### Desafío
Completá el caso del aullido y la línea del `never`.

#### Pasos
1. El primer `___`: `case 'aullido':` y, abajo, ``return `aúlla ${s.segundos} segundos`;``.
2. El segundo `___`: `const nunca: never = s;`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Senal =
  | { tipo: 'ladrido'; veces: number }
  | { tipo: 'grunido'; fuerza: number }
  | { tipo: 'aullido'; segundos: number };

function traducir(s: Senal): string {
  switch (s.tipo) {
    case 'ladrido':
      return `ladra ${s.veces} veces`;
    case 'grunido':
      return `gruñe con fuerza ${s.fuerza}`;
    ___
    default: {
      ___
      throw new Error(`Señal desconocida: ${JSON.stringify(nunca)}`);
    }
  }
}

const senales: Senal[] = [{ tipo: 'ladrido', veces: 3 }, { tipo: 'aullido', segundos: 5 }, { tipo: 'grunido', fuerza: 8 }];
for (const s of senales) console.log(traducir(s));
```

#### Salida esperada
```
ladra 3 veces
aúlla 5 segundos
gruñe con fuerza 8
```

#### Solución
```typescript
type Senal =
  | { tipo: 'ladrido'; veces: number }
  | { tipo: 'grunido'; fuerza: number }
  | { tipo: 'aullido'; segundos: number };

function traducir(s: Senal): string {
  switch (s.tipo) {
    case 'ladrido':
      return `ladra ${s.veces} veces`;
    case 'grunido':
      return `gruñe con fuerza ${s.fuerza}`;
    case 'aullido':
      return `aúlla ${s.segundos} segundos`;
    default: {
      const nunca: never = s;
      throw new Error(`Señal desconocida: ${JSON.stringify(nunca)}`);
    }
  }
}

const senales: Senal[] = [{ tipo: 'ladrido', veces: 3 }, { tipo: 'aullido', segundos: 5 }, { tipo: 'grunido', fuerza: 8 }];
for (const s of senales) console.log(traducir(s));
```

#### Al superarla
La segunda cabeza no tiene ninguna señal que Rigel no entienda. Agacha las orejas de bronce.

#### Imagen
- El autómata de tres cabezas de perro con una segunda cabeza agachando las orejas.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) lee una libreta de traducciones.
- Gheco tapándose los oídos.

### Micro-misión R03-N08-P3 · La tercera cabeza

```meta
lugar: La cúpula del Telescopio
personajes: Rigel, Gheco, el Cerbero de las Uniones
criatura: goblin
carta: Trampa 3 | lo que llega es unknown · un guardia revisa cada propiedad · lo que no pasa, se descarta
recompensa: xp 15, monedas 3
```

#### Escena
La tercera cabeza escupe papelitos con estrellas en texto. Algunos están rotos, otros son basura. Rigel pone un guardia en la boca del Cerbero.

#### Gheco sugiere
`JSON.parse` devuelve algo sin tipo seguro: se guarda como `unknown` y pasa por un guardia. El guardia revisa que sea un objeto, que no sea `null`, y cada propiedad que se va a usar.

#### Desafío
Completá el tipo de retorno del guardia.

#### Pasos
1. Buscá el `___` después de los paréntesis de `esEstrella`.
2. Cambialo por `x is Estrella`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Estrella = { nombre: string; brillo: number };

function esEstrella(x: unknown): ___ {
  return typeof x === 'object' && x !== null
    && 'nombre' in x && typeof x.nombre === 'string'
    && 'brillo' in x && typeof x.brillo === 'number';
}

const papelitos = ['{"nombre":"Vega","brillo":9}', '{"nombre":3}', '{"nombre":"Altair","brillo":8}'];
for (const p of papelitos) {
  const dato: unknown = JSON.parse(p);
  console.log(esEstrella(dato) ? `${dato.nombre} ★${dato.brillo}` : 'basura');
}
```

#### Salida esperada
```
Vega ★9
basura
Altair ★8
```

#### Solución
```typescript
type Estrella = { nombre: string; brillo: number };

function esEstrella(x: unknown): x is Estrella {
  return typeof x === 'object' && x !== null
    && 'nombre' in x && typeof x.nombre === 'string'
    && 'brillo' in x && typeof x.brillo === 'number';
}

const papelitos = ['{"nombre":"Vega","brillo":9}', '{"nombre":3}', '{"nombre":"Altair","brillo":8}'];
for (const p of papelitos) {
  const dato: unknown = JSON.parse(p);
  console.log(esEstrella(dato) ? `${dato.nombre} ★${dato.brillo}` : 'basura');
}
```

#### Al superarla
El guardia separa los papelitos buenos de la basura. La tercera cabeza se queda sin nada que escupir.

#### Imagen
- Papelitos volando desde la boca de una cabeza de perro de bronce, y un guardia chiquito de latón separándolos en dos canastos.
- Rigel (chico flaco con pecas, antiparras de latón) junta los papelitos buenos.
- Gheco con un papelito pegado en la cara.

### Micro-misión R03-N08-P4 · El collar del Cerbero

```meta
lugar: La cúpula del Telescopio
personajes: Rigel, Gheco, el Cerbero de las Uniones
criatura: ogre
carta: Trampa 4 | Record con una entrada por cabeza · Partial para cambiar solo algo · Omit para crear sin id
recompensa: xp 15, monedas 3
```

#### Escena
Para atar al Cerbero, Rigel arma un collar con una placa para cada cabeza. Si falta una placa, la cabeza se escapa.

#### Gheco sugiere
`Record<Cabeza, Placa>` pide una placa por **cada** cabeza. Para cambiar solo algo de una placa, `Partial<Placa>`.

#### Desafío
Completá los tipos del collar y de los cambios.

#### Pasos
1. El primer `___`: `Record<Cabeza, Placa>`.
2. El segundo `___`: `Partial<Placa>`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Cabeza = 'izquierda' | 'centro' | 'derecha';
type Placa = { material: string; grabado: string };

const collar: ___ = {
  izquierda: { material: 'bronce', grabado: 'number' },
  centro: { material: 'bronce', grabado: 'string' },
  derecha: { material: 'bronce', grabado: 'boolean' },
};

function cambiar(cabeza: Cabeza, cambios: ___): void {
  collar[cabeza] = { ...collar[cabeza], ...cambios };
}

cambiar('centro', { material: 'latón' });
for (const c of ['izquierda', 'centro', 'derecha'] as const) {
  console.log(`${c}: ${collar[c].material} (${collar[c].grabado})`);
}
```

#### Salida esperada
```
izquierda: bronce (number)
centro: latón (string)
derecha: bronce (boolean)
```

#### Solución
```typescript
type Cabeza = 'izquierda' | 'centro' | 'derecha';
type Placa = { material: string; grabado: string };

const collar: Record<Cabeza, Placa> = {
  izquierda: { material: 'bronce', grabado: 'number' },
  centro: { material: 'bronce', grabado: 'string' },
  derecha: { material: 'bronce', grabado: 'boolean' },
};

function cambiar(cabeza: Cabeza, cambios: Partial<Placa>): void {
  collar[cabeza] = { ...collar[cabeza], ...cambios };
}

cambiar('centro', { material: 'latón' });
for (const c of ['izquierda', 'centro', 'derecha'] as const) {
  console.log(`${c}: ${collar[c].material} (${collar[c].grabado})`);
}
```

#### Al superarla
Las tres placas quedan en su lugar. El collar se cierra sobre los tres cuellos.

#### Imagen
- Un collar de bronce con tres placas grabadas, cerrándose sobre los tres cuellos del autómata de perro.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) ajusta el broche.
- Gheco sostiene una de las placas.

### Micro-misión R03-N08-P5 · El Cerbero cae

```meta
lugar: La cúpula del Telescopio
personajes: Rigel, Gheco, Astrea, el Cerbero de las Uniones
criatura: dragon
carta: El jefe | guardia para lo que llega · unión discriminada · switch exhaustivo · un manejador por cabeza con un mapped type
recompensa: xp 20, monedas 5
item: Collar del Cerbero
```

#### Escena
Con el collar puesto, el Cerbero intenta un último truco: mandar órdenes falsas al Telescopio. Rigel arma la defensa completa: un guardia en la entrada, un manejador para cada cabeza y nada sin atender.

#### Gheco sugiere
Todo lo de la rama:
- las órdenes llegan en texto: se parsean y pasan por el guardia `esOrden`;
- `Orden` es una unión discriminada por `cabeza`;
- `Manejadores` es un mapped type con un manejador por cabeza;
- el `switch` termina con `never`.

#### Desafío
Completá el mapped type de los manejadores.

#### Pasos
1. Buscá el `___` adentro de las llaves de `Manejadores`.
2. Cambialo por `[C in Cabeza]: (fuerza: number) => string`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Cabeza = 'izquierda' | 'centro' | 'derecha';
type Orden = { cabeza: Cabeza; fuerza: number };
type Manejadores = { ___ };

const CABEZAS: readonly string[] = ['izquierda', 'centro', 'derecha'];

function esOrden(x: unknown): x is Orden {
  return typeof x === 'object' && x !== null
    && 'cabeza' in x && typeof x.cabeza === 'string' && CABEZAS.includes(x.cabeza)
    && 'fuerza' in x && typeof x.fuerza === 'number';
}

const manejadores: Manejadores = {
  izquierda: (f) => `el telescopio gira ${f}° a la izquierda`,
  centro: (f) => `el telescopio sube ${f}°`,
  derecha: (f) => `el telescopio gira ${f}° a la derecha`,
};

function atender(o: Orden): string {
  switch (o.cabeza) {
    case 'izquierda':
    case 'centro':
    case 'derecha':
      return manejadores[o.cabeza](o.fuerza);
    default: {
      const nunca: never = o.cabeza;
      throw new Error(`Cabeza desconocida: ${nunca}`);
    }
  }
}

const ordenes = ['{"cabeza":"centro","fuerza":30}', '{"cabeza":"cola","fuerza":99}', '{"cabeza":"izquierda","fuerza":15}'];
for (const texto of ordenes) {
  const dato: unknown = JSON.parse(texto);
  console.log(esOrden(dato) ? atender(dato) : 'orden falsa: ignorada');
}
```

#### Salida esperada
```
el telescopio sube 30°
orden falsa: ignorada
el telescopio gira 15° a la izquierda
```

#### Solución
```typescript
type Cabeza = 'izquierda' | 'centro' | 'derecha';
type Orden = { cabeza: Cabeza; fuerza: number };
type Manejadores = { [C in Cabeza]: (fuerza: number) => string };

const CABEZAS: readonly string[] = ['izquierda', 'centro', 'derecha'];

function esOrden(x: unknown): x is Orden {
  return typeof x === 'object' && x !== null
    && 'cabeza' in x && typeof x.cabeza === 'string' && CABEZAS.includes(x.cabeza)
    && 'fuerza' in x && typeof x.fuerza === 'number';
}

const manejadores: Manejadores = {
  izquierda: (f) => `el telescopio gira ${f}° a la izquierda`,
  centro: (f) => `el telescopio sube ${f}°`,
  derecha: (f) => `el telescopio gira ${f}° a la derecha`,
};

function atender(o: Orden): string {
  switch (o.cabeza) {
    case 'izquierda':
    case 'centro':
    case 'derecha':
      return manejadores[o.cabeza](o.fuerza);
    default: {
      const nunca: never = o.cabeza;
      throw new Error(`Cabeza desconocida: ${nunca}`);
    }
  }
}

const ordenes = ['{"cabeza":"centro","fuerza":30}', '{"cabeza":"cola","fuerza":99}', '{"cabeza":"izquierda","fuerza":15}'];
for (const texto of ordenes) {
  const dato: unknown = JSON.parse(texto);
  console.log(esOrden(dato) ? atender(dato) : 'orden falsa: ignorada');
}
```

#### Al superarla
La orden falsa rebota en el guardia, y las verdaderas mueven el Telescopio como corresponde. El Cerbero, sin una sola cabeza que lo obedezca, se desenrosca del tubo y se queda dormido, con las tres cabezas juntas. Astrea le saca el collar y se lo da a Rigel: el **Collar del Cerbero**. —Ahora sabés qué es cada cosa antes de tocarla.

#### Imagen
- El autómata de bronce de tres cabezas de perro dormido enroscado al pie del telescopio, bajo la cúpula abierta con el cielo estrellado.
- Rigel (chico flaco con pecas, pelo castaño revuelto, antiparras de latón, chaleco marrón) recibe un collar de bronce con tres placas.
- Astrea (lechuza grande con anteojos de latón y chaleco azul) se lo entrega; Gheco acaricia una de las cabezas dormidas.
