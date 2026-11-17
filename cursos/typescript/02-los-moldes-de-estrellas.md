# RAMA R02 · Los Moldes de Estrellas: clases, enums y genéricos

```meta
tipo: tronco
posicion: 2
```

## R02-N01 · Clases tipadas

```meta
tipo: tema
padre: R01-N07
precio: 10
criatura: skeleton
temas: poo.clases, cal.tipos
```

### Crónica

Detrás de la Sala de las Figuras está **la fundición**: hornos chiquitos, crisoles de vidrio derretido y una pared llena de **moldes** de bronce. Ahí trabaja **Don Péndulo**, un relojero viejísimo, de barba blanca y delantal de cuero, que conoció al Vidriero.

—Una pieza se mide —le dice a Rigel—, pero mil piezas iguales se **funden en un molde**. El molde dice qué forma tiene cada una y qué sabe hacer. Lo hacés una vez, y después sacás todas las que quieras.

—En JavaScript ya lo conocés —agrega {mentor}—: es una `class`. En el Mirador, además, el molde lleva la medida de cada parte.

### Objetivos

- Escribir una clase con propiedades tipadas, constructor y métodos.
- Usar el atajo del constructor: `constructor(public x: number)`.
- Usar una clase como tipo: `const p: Vec2 = new Vec2(1, 2)`.
- Leer los errores de una clase: la propiedad que no existe (`TS2339`) y la que no tiene valor (`TS2564`).

### Antes de empezar

- R01 entera: tipos, funciones tipadas e `interface`.
- De JavaScript: `class`, `constructor`, `this` y `new`.

### Explicación

#### El molde con sus medidas
```typescript
class Estrella {
  nombre: string;
  brillo: number;

  constructor(nombre: string, brillo: number) {
    this.nombre = nombre;
    this.brillo = brillo;
  }

  describir(): string {
    return `${this.nombre} brilla ${this.brillo}`;
  }
}

const vega = new Estrella('Vega', 9);
console.log(vega.describir());
```

En TypeScript, las propiedades se **declaran** arriba, con su tipo. Si declarás una y no le das valor ni en la declaración ni en el constructor, el compilador avisa (`TS2564`).

#### El atajo del constructor
Escribir cada propiedad tres veces (declararla, recibirla y asignarla) cansa. TypeScript tiene un atajo:

```typescript
class Vec2 {
  constructor(public x: number, public y: number) {}
}
```

El `public` adelante del parámetro hace las tres cosas de una vez: declara la propiedad, la recibe y la guarda.

#### La clase también es un tipo
```typescript
function sumar(a: Vec2, b: Vec2): Vec2 {
  return new Vec2(a.x + b.x, a.y + b.y);
}
```

### Código de ejemplo

```typescript
class Vec2 {
  constructor(public x: number = 0, public y: number = 0) {}

  sumar(otro: Vec2): Vec2 {
    return new Vec2(this.x + otro.x, this.y + otro.y);
  }

  toString(): string {
    return `(${this.x}, ${this.y})`;
  }
}

class Estrella {
  constructor(public nombre: string, public posicion: Vec2) {}

  mover(paso: Vec2): void {
    this.posicion = this.posicion.sumar(paso);
  }
}

const vega = new Estrella('Vega', new Vec2(1, 2));
vega.mover(new Vec2(3, 1));
console.log(`${vega.nombre} está en ${vega.posicion}`);
```

### Salida esperada

```
Vega está en (4, 3)
```

### ¿Para qué sirve?

Las clases son moldes para crear muchos objetos con la misma forma y el mismo comportamiento: los enemigos de un juego, los productos de una tienda, las cuentas de un banco. Con los tipos, el compilador revisa que cada objeto se use bien en todo el programa.

### Errores habituales

**Esqueleto: una propiedad que la clase no tiene (TS2339).** *La propiedad 'brillo' no existe en el tipo 'Estrella'*. Revisá el nombre o declarala en la clase.

**Esqueleto: una propiedad sin valor (TS2564).** *La propiedad "brillo" no tiene inicializador y no está asignada de forma definitiva en el constructor*. Dale un valor al declararla o en el constructor.

**Esqueleto: los argumentos de new (TS2554).** `new Vec2(1)` cuando el constructor pide dos da *Se esperaban 2 argumentos*. Si uno puede faltar, dale un valor por defecto.

### Micro-misión R02-N01-P1 · El primer molde

```meta
lugar: La fundición
personajes: Rigel, Gheco, Don Péndulo
carta: Clase tipada | nombre: string; arriba · el constructor guarda con this. · los métodos con su tipo de retorno
recompensa: xp 10, oro 10
```

#### Escena
Don Péndulo le alcanza a Rigel un molde de bronce a medio grabar. —Completale lo que devuelve el método, que el molde no sabe qué entregar.

#### Gheco sugiere
En una clase de TypeScript, las propiedades se declaran arriba con su tipo, el constructor les da valor con `this.`, y cada método dice qué devuelve:

```ts
class Lampara {
  watts: number;
  constructor(watts: number) {
    this.watts = watts;
  }
  describir(): string {
    return `${this.watts} W`;
  }
}
```

#### Desafío
Completá el tipo de lo que devuelve `describir`.

#### Pasos
1. Buscá el `___` después de `describir()`.
2. Cambialo por `string` (devuelve un texto).
3. Tocá **Ejecutar**. Tiene que salir `Vega brilla 9`.

#### Código inicial
```typescript
class Estrella {
  nombre: string;
  brillo: number;

  constructor(nombre: string, brillo: number) {
    this.nombre = nombre;
    this.brillo = brillo;
  }

  describir(): ___ {
    return `${this.nombre} brilla ${this.brillo}`;
  }
}

const vega = new Estrella('Vega', 9);
console.log(vega.describir());
```

#### Salida esperada
```
Vega brilla 9
```

#### Solución
```typescript
class Estrella {
  nombre: string;
  brillo: number;

  constructor(nombre: string, brillo: number) {
    this.nombre = nombre;
    this.brillo = brillo;
  }

  describir(): string {
    return `${this.nombre} brilla ${this.brillo}`;
  }
}

const vega = new Estrella('Vega', 9);
console.log(vega.describir());
```

#### Al superarla
Rigel vierte vidrio derretido en el molde. Cuando se enfría, sale una estrellita perfecta. Don Péndulo la mira contra la luz: —Así se hacía antes. Así se hace siempre.

#### Imagen
- Una fundición de observatorio steampunk con hornos chiquitos, crisoles de vidrio derretido y una pared llena de moldes de bronce.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón bajadas sobre los ojos, camisa azul, chaleco de cuero marrón cerrado, guantes sin dedos) vierte vidrio en un molde.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa de relojero en un ojo) mira; Gheco sobre un estante.

### Micro-misión R02-N01-P2 · La propiedad sin valor

```meta
lugar: La fundición
personajes: Rigel, Gheco
criatura: skeleton
carta: TS2564 | una propiedad declarada sin valor · dásela al declararla o en el constructor
recompensa: xp 10, oro 10
```

#### Escena
Un molde tiene grabado *brillo*, pero nadie le puso cuánto. Un **esqueleto** de alambre duerme en el hueco vacío.

#### Gheco sugiere
En modo estricto, toda propiedad declarada tiene que tener valor: o al declararla (`brillo: number = 1;`) o en el constructor. Si no, el compilador avisa con `TS2564`.

#### Desafío
Asigná el brillo en el constructor.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el constructor, debajo de `this.nombre = nombre;`, escribí `this.brillo = brillo;`.
3. Tocá **Ejecutar**. Tiene que salir `Sirio: 10`.

#### Código inicial
```typescript
class Estrella {
  nombre: string;
  brillo: number;

  constructor(nombre: string, brillo: number) {
    this.nombre = nombre;
  }
}

const sirio = new Estrella('Sirio', 10);
console.log(`${sirio.nombre}: ${sirio.brillo}`);
```

#### Salida esperada
```
Sirio: 10
```

#### Solución
```typescript
class Estrella {
  nombre: string;
  brillo: number;

  constructor(nombre: string, brillo: number) {
    this.nombre = nombre;
    this.brillo = brillo;
  }
}

const sirio = new Estrella('Sirio', 10);
console.log(`${sirio.nombre}: ${sirio.brillo}`);
```

#### Al superarla
La estrella sale del molde y se enciende: brillo 10. El esqueleto se despierta encandilado y se va.

#### Imagen
- Una estrellita de vidrio recién salida de un molde de bronce, encendida y muy brillante.
- Un esqueleto de alambre chiquito tapándose los ojos.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sostiene la estrella con una pinza; Gheco mira.

### Micro-misión R02-N01-P3 · El atajo de Don Péndulo

```meta
lugar: La fundición
personajes: Rigel, Gheco, Don Péndulo
carta: Atajo del constructor | constructor(public x: number, public y: number) {} · declara, recibe y guarda de una vez
recompensa: xp 10, oro 10
```

#### Escena
Don Péndulo ve a Rigel escribir cada propiedad tres veces y se ríe. —Hay un atajo, muchacho. Mirá.

#### Gheco sugiere
Con `public` adelante de un parámetro del constructor, TypeScript declara la propiedad, la recibe y la guarda, todo de una vez:

```ts
class Vec2 {
  constructor(public x: number, public y: number) {}
}
```

Las llaves del constructor quedan vacías.

#### Desafío
Agregale `public` a los dos parámetros del constructor.

#### Pasos
1. Buscá `constructor(x: number, y: number)`.
2. Agregale `public` adelante de cada uno: `constructor(public x: number, public y: number)`.
3. Tocá **Ejecutar**. Tiene que salir `Posición: (3, 4)`.

#### Código inicial
```typescript
class Vec2 {
  constructor(x: number, y: number) {}
}

const p = new Vec2(3, 4);
console.log(`Posición: (${p.x}, ${p.y})`);
```

#### Salida esperada
```
Posición: (3, 4)
```

#### Solución
```typescript
class Vec2 {
  constructor(public x: number, public y: number) {}
}

const p = new Vec2(3, 4);
console.log(`Posición: (${p.x}, ${p.y})`);
```

#### Al superarla
—Tres líneas en una —dice Don Péndulo—. El Vidriero lo escribía así. Era un vago para las cosas aburridas, y un genio para las difíciles.

#### Imagen
- Una mesa de relojero llena de herramientas finas, con un plano dibujado a mano.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa en un ojo) señala el plano con un destornillador.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) toma nota; Gheco sobre la mesa.

### Micro-misión R02-N01-P4 · Sumar posiciones

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco
carta: Método que devuelve otra instancia | sumar(otro: Vec2): Vec2 · la clase como tipo · new Vec2(…) adentro
recompensa: xp 10, oro 10
```

#### Escena
Para mover una estrella del Planisferio, Rigel suma su posición con el paso que tiene que dar.

#### Gheco sugiere
Una clase también es un **tipo**: un método puede recibir otro `Vec2` y devolver un `Vec2` nuevo.

```ts
sumar(otro: Vec2): Vec2 {
  return new Vec2(this.x + otro.x, this.y + otro.y);
}
```

#### Desafío
Completá el `return` de `sumar`.

#### Pasos
1. Buscá el `___` en `sumar`.
2. Cambialo por `new Vec2(this.x + otro.x, this.y + otro.y)`.
3. Tocá **Ejecutar**. Tiene que salir `Vega pasa de (1, 2) a (4, 3)`.

#### Código inicial
```typescript
class Vec2 {
  constructor(public x: number, public y: number) {}

  sumar(otro: Vec2): Vec2 {
    return ___;
  }
}

const antes = new Vec2(1, 2);
const despues = antes.sumar(new Vec2(3, 1));
console.log(`Vega pasa de (${antes.x}, ${antes.y}) a (${despues.x}, ${despues.y})`);
```

#### Salida esperada
```
Vega pasa de (1, 2) a (4, 3)
```

#### Solución
```typescript
class Vec2 {
  constructor(public x: number, public y: number) {}

  sumar(otro: Vec2): Vec2 {
    return new Vec2(this.x + otro.x, this.y + otro.y);
  }
}

const antes = new Vec2(1, 2);
const despues = antes.sumar(new Vec2(3, 1));
console.log(`Vega pasa de (${antes.x}, ${antes.y}) a (${despues.x}, ${despues.y})`);
```

#### Al superarla
El brazo de latón de Vega se desliza y la estrella se acomoda en su lugar nuevo con un *clic*.

#### Imagen
- Un brazo articulado de latón del planetario mecánico moviendo una estrella de vidrio a una nueva posición, con una estela de luz.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) gira una manivela.
- Gheco viaja montado en la estrella.

### Micro-misión R02-N01-P5 · La estrella que se mueve

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco, Don Péndulo
carta: Clases que usan clases | una propiedad de tipo Vec2 · un método void que cambia el estado · toString() para mostrar
recompensa: xp 15, monedas 5
```

#### Escena
Don Péndulo quiere ver una estrella moverse dos veces seguidas por el Planisferio, y que cada paso se anote.

#### Gheco sugiere
Una propiedad puede ser de tipo **otra clase**: `posicion: Vec2`. Y un método `void` puede cambiarla:

```ts
mover(paso: Vec2): void {
  this.posicion = this.posicion.sumar(paso);
}
```

`toString()` dice cómo se muestra el objeto en un texto: `${vega.posicion}` usa el `toString()` de `Vec2`.

#### Desafío
Completá el método `mover`.

#### Pasos
1. Buscá el `___` adentro de `mover`.
2. Cambialo por `this.posicion = this.posicion.sumar(paso);`.
3. Tocá **Ejecutar**. Tienen que salir `Vega está en (4, 3)` y `Vega está en (4, 5)`.

#### Código inicial
```typescript
class Vec2 {
  constructor(public x: number = 0, public y: number = 0) {}

  sumar(otro: Vec2): Vec2 {
    return new Vec2(this.x + otro.x, this.y + otro.y);
  }

  toString(): string {
    return `(${this.x}, ${this.y})`;
  }
}

class Estrella {
  constructor(public nombre: string, public posicion: Vec2) {}

  mover(paso: Vec2): void {
    ___
  }
}

const vega = new Estrella('Vega', new Vec2(1, 2));
vega.mover(new Vec2(3, 1));
console.log(`${vega.nombre} está en ${vega.posicion}`);
vega.mover(new Vec2(0, 2));
console.log(`${vega.nombre} está en ${vega.posicion}`);
```

#### Salida esperada
```
Vega está en (4, 3)
Vega está en (4, 5)
```

#### Solución
```typescript
class Vec2 {
  constructor(public x: number = 0, public y: number = 0) {}

  sumar(otro: Vec2): Vec2 {
    return new Vec2(this.x + otro.x, this.y + otro.y);
  }

  toString(): string {
    return `(${this.x}, ${this.y})`;
  }
}

class Estrella {
  constructor(public nombre: string, public posicion: Vec2) {}

  mover(paso: Vec2): void {
    this.posicion = this.posicion.sumar(paso);
  }
}

const vega = new Estrella('Vega', new Vec2(1, 2));
vega.mover(new Vec2(3, 1));
console.log(`${vega.nombre} está en ${vega.posicion}`);
vega.mover(new Vec2(0, 2));
console.log(`${vega.nombre} está en ${vega.posicion}`);
```

#### Al superarla
Vega recorre el Planisferio, paso a paso, dejando un rastro de luz. Don Péndulo aplaude despacio, con sus manos de relojero.

#### Imagen
- Una estrella de vidrio recorriendo el planetario mecánico, con un rastro de luz en forma de escalón.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) anota en una libreta.
- Don Péndulo (relojero viejo de barba blanca y delantal de cuero) aplaude; Gheco persigue la estrella.

### Micro-misión R02-N01-P6 · El taller de faroles

```meta
lugar: La fundición
personajes: Rigel, Gheco, Don Péndulo
carta: Un arreglo de instancias | Farol[] · cada uno con sus datos · un método que calcula · el total con un for…of
recompensa: xp 15, monedas 5
```

#### Escena
Don Péndulo le encarga a Rigel tres faroles para la escalera del Mirador. Quiere saber cuánta luz dan entre todos.

#### Gheco sugiere
Una clase sirve como tipo de un arreglo: `Farol[]` es una lista de faroles. Cada farol sabe calcular su propia luz con un método, y el total se suma con un `for…of`.

#### Desafío
Completá el método `luz` (las lámparas por los watts de cada una) y el tipo del arreglo.

#### Pasos
1. En `luz`, el `___` es `this.lamparas * this.watts`.
2. En el arreglo, el `___` es `Farol[]`.
3. Tocá **Ejecutar**. Tiene que salir `Luz total: 90 W en 3 faroles`.

#### Código inicial
```typescript
class Farol {
  constructor(public lamparas: number, public watts: number) {}

  luz(): number {
    return ___;
  }
}

const escalera: ___ = [new Farol(2, 10), new Farol(3, 15), new Farol(1, 25)];

let total = 0;
for (const f of escalera) total += f.luz();
console.log(`Luz total: ${total} W en ${escalera.length} faroles`);
```

#### Salida esperada
```
Luz total: 90 W en 3 faroles
```

#### Solución
```typescript
class Farol {
  constructor(public lamparas: number, public watts: number) {}

  luz(): number {
    return this.lamparas * this.watts;
  }
}

const escalera: Farol[] = [new Farol(2, 10), new Farol(3, 15), new Farol(1, 25)];

let total = 0;
for (const f of escalera) total += f.luz();
console.log(`Luz total: ${total} W en ${escalera.length} faroles`);
```

#### Al superarla
La escalera del Mirador se ilumina de abajo hacia arriba. Don Péndulo le da a Rigel una **estrella de latón**, sacada de un bolsillo del delantal.

#### Imagen
- Una escalera de caracol de latón dentro del observatorio, iluminada por tres faroles de vidrio de distinto tamaño.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) cuelga el último farol.
- Don Péndulo (relojero viejo de barba blanca) le da una ficha de latón con una estrella; Gheco en la baranda.

## R02-N02 · private, readonly y #privado

```meta
tipo: tema
padre: R02-N01
precio: 10
criatura: ogre
temas: poo.encapsulamiento, cal.tipos
```

### Crónica

En la fundición, los crisoles tienen una tapa con candado: el vidrio derretido no se toca con la mano. Pero un **ogro** consiguió meter los dedos en uno y ahora el molde de Rigel tiene una mancha.

—Hay partes de un molde que nadie de afuera tiene que tocar —dice Don Péndulo—. Algunas se cierran con una **advertencia** escrita. Otras, con un **candado de verdad**.

### Objetivos

- Proteger propiedades con `private` y `readonly`, y leer sus errores (`TS2341`, `TS2540`).
- Conocer `protected`: lo usan la clase y las que heredan.
- Diferenciar `private` (lo revisa el compilador) de `#privado` (lo protege JavaScript al ejecutar).
- Usar un `get` para mostrar algo sin dejar cambiarlo.

### Antes de empezar

- R02-N01: clases tipadas.
- De JavaScript: campos `#privados` y `get`.

### Explicación

#### private y readonly
```typescript
class Caldera {
  private presion: number = 0;
  readonly numero: string;

  constructor(numero: string) {
    this.numero = numero;
  }

  cargar(cantidad: number): void {
    this.presion = Math.min(100, this.presion + cantidad);
  }

  get lectura(): number {
    return this.presion;
  }
}

const c = new Caldera('C-1');
c.presion = 500;   // ✗ TS2341: presion es private
c.numero = 'C-2';  // ✗ TS2540: numero es readonly
console.log(c.lectura);  // ✓ el get deja leer, no cambiar
```

- `private`: solo se usa **adentro** de la clase.
- `protected`: adentro de la clase **y** de las que heredan (R02-N03).
- `public`: desde cualquier lado (es lo que pasa si no ponés nada).
- `readonly`: se asigna al crear y después no se cambia.

#### La advertencia y el candado
`private` y `readonly` los revisa **el compilador**. En el JavaScript que corre desaparecen: si alguien usa tu clase desde JavaScript, puede tocar `presion` igual.

`#presion` es **privado de verdad**: lo protege JavaScript mientras el programa corre. TypeScript también lo revisa:

```typescript
class Cofre {
  #abierto = false;
  abrir(): void { this.#abierto = true; }
}
```

> Regla práctica: `private` alcanza casi siempre. Si tu clase la va a usar código que no es TypeScript, usá `#`.

### Código de ejemplo

```typescript
class Caldera {
  #presion = 0;

  constructor(public readonly numero: string, private maxima: number) {}

  cargar(cantidad: number): void {
    this.#presion = Math.min(this.maxima, this.#presion + cantidad);
  }

  get lectura(): string {
    return `${this.numero}: ${this.#presion} de ${this.maxima}`;
  }
}

const caldera = new Caldera('C-1', 80);
caldera.cargar(50);
caldera.cargar(50);
console.log(caldera.lectura);
```

### Salida esperada

```
C-1: 80 de 80
```

### ¿Para qué sirve?

Si cualquiera puede cambiar el estado de un objeto desde afuera, nadie puede asegurar que esté bien: una caldera con presión 500, un saldo negativo, una vida de -20. Con `private` y `readonly`, el único camino para cambiar el estado son los métodos de la clase, que revisan las reglas.

### Errores habituales

**Ogro: tocar algo privado desde afuera (TS2341).** *La propiedad 'presion' es privada y solo se puede acceder a ella en la clase 'Caldera'*. Usá un método de la clase.

**Ogro: cambiar algo readonly (TS2540).** Solo se asigna al declarar o en el constructor.

**Ogro: el #privado desde afuera (TS18013).** *No se puede acceder a la propiedad "#presion" fuera de la clase "Caldera" porque tiene un identificador privado*.

### Micro-misión R02-N02-P1 · El crisol cerrado

```meta
lugar: La fundición
personajes: Rigel, Gheco
criatura: ogre
carta: private | private temperatura: number · solo adentro de la clase · desde afuera es TS2341
recompensa: xp 10, oro 10
```

#### Escena
Un **ogro** quiere meter la mano en el crisol y subirle la temperatura a mil grados. Rigel le pone una tapa.

#### Gheco sugiere
`private` adelante de una propiedad hace que solo se pueda usar **adentro** de la clase. Desde afuera, el compilador avisa con `TS2341`. Para cambiarla, hay un método de la clase que revisa las reglas.

#### Desafío
Marcá `temperatura` como `private` y cambiá la línea del ogro por una llamada a `calentar(200)`.

#### Pasos
1. Agregale `private` adelante: `private temperatura: number = 20;`.
2. Tocá **Ejecutar**: la línea del ogro da `TS2341`.
3. Cambiá `crisol.temperatura = 1000;` por `crisol.calentar(200);`.
4. Tocá **Ejecutar**. Tiene que salir `El crisol está a 220 grados`.

#### Código inicial
```typescript
class Crisol {
  temperatura: number = 20;

  calentar(grados: number): void {
    this.temperatura = Math.min(900, this.temperatura + grados);
  }

  lectura(): string {
    return `El crisol está a ${this.temperatura} grados`;
  }
}

const crisol = new Crisol();
crisol.temperatura = 1000;
console.log(crisol.lectura());
```

#### Salida esperada
```
El crisol está a 220 grados
```

#### Solución
```typescript
class Crisol {
  private temperatura: number = 20;

  calentar(grados: number): void {
    this.temperatura = Math.min(900, this.temperatura + grados);
  }

  lectura(): string {
    return `El crisol está a ${this.temperatura} grados`;
  }
}

const crisol = new Crisol();
crisol.calentar(200);
console.log(crisol.lectura());
```

#### Al superarla
La tapa del crisol se cierra con un *clanc*. El ogro se sopla los dedos, ofendido.

#### Imagen
- Un crisol de vidrio derretido con una tapa de bronce y un candado chiquito, sobre un horno pequeño.
- Un ogro chiquito soplándose los dedos.
- Rigel (chico flaco con pecas, antiparras de latón bajadas, guantes sin dedos) cierra la tapa; Gheco mira.

### Micro-misión R02-N02-P2 · El número de la caldera

```meta
lugar: Las calderas del Mirador
personajes: Rigel, Gheco
criatura: ogre
carta: readonly en el constructor | constructor(public readonly numero: string) · se pone al crear · cambiarlo es TS2540
recompensa: xp 10, oro 10
```

#### Escena
Cada caldera tiene su número pintado. Alguien quiso repintar la C-1 como C-9 para confundir a la fogonera.

#### Gheco sugiere
`readonly` también se puede usar en el atajo del constructor:

```ts
constructor(public readonly numero: string) {}
```

Se asigna al crear la caldera, y después no se puede cambiar (`TS2540`).

#### Desafío
Agregale `readonly` al número y borrá la línea que lo repinta.

#### Pasos
1. Cambiá `public numero` por `public readonly numero`.
2. Tocá **Ejecutar**: la línea `caldera.numero = 'C-9';` da `TS2540`.
3. Borrá esa línea.
4. Tocá **Ejecutar**. Tiene que salir `Caldera C-1 lista`.

#### Código inicial
```typescript
class Caldera {
  constructor(public numero: string) {}
}

const caldera = new Caldera('C-1');
caldera.numero = 'C-9';
console.log(`Caldera ${caldera.numero} lista`);
```

#### Salida esperada
```
Caldera C-1 lista
```

#### Solución
```typescript
class Caldera {
  constructor(public readonly numero: string) {}
}

const caldera = new Caldera('C-1');
console.log(`Caldera ${caldera.numero} lista`);
```

#### Al superarla
La pintura nueva se escurre y vuelve a aparecer el número de siempre: C-1.

#### Imagen
- Una caldera de cobre con un número pintado en una placa (sin números legibles) y un pincel abandonado al lado.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) limpia la placa con un trapo.
- Gheco sentado sobre la caldera.

### Micro-misión R02-N02-P3 · Mirar sin tocar

```meta
lugar: Las calderas del Mirador
personajes: Rigel, Gheco
carta: get | get lectura(): number { return this.presion; } · se usa sin paréntesis · deja leer, no cambiar
recompensa: xp 10, oro 10
```

#### Escena
La fogonera necesita ver la presión de la caldera desde lejos, pero sin poder cambiarla. Rigel le pone un visor.

#### Gheco sugiere
Un `get` es un método que se usa **como si fuera una propiedad**, sin paréntesis:

```ts
get lectura(): number {
  return this.presion;
}
```

`caldera.lectura` devuelve la presión, pero no deja asignarle nada. La presión de verdad sigue siendo `private`.

#### Desafío
Completá el `get` para que devuelva la presión.

#### Pasos
1. Buscá el `___` adentro de `get lectura()`.
2. Cambialo por `return this.presion;`.
3. Tocá **Ejecutar**. Tiene que salir `Presión: 70`.

#### Código inicial
```typescript
class Caldera {
  private presion: number = 0;

  cargar(cantidad: number): void {
    this.presion = Math.min(100, this.presion + cantidad);
  }

  get lectura(): number {
    ___
  }
}

const caldera = new Caldera();
caldera.cargar(40);
caldera.cargar(30);
console.log(`Presión: ${caldera.lectura}`);
```

#### Salida esperada
```
Presión: 70
```

#### Solución
```typescript
class Caldera {
  private presion: number = 0;

  cargar(cantidad: number): void {
    this.presion = Math.min(100, this.presion + cantidad);
  }

  get lectura(): number {
    return this.presion;
  }
}

const caldera = new Caldera();
caldera.cargar(40);
caldera.cargar(30);
console.log(`Presión: ${caldera.lectura}`);
```

#### Al superarla
En el visor de vidrio aparece la aguja, quieta en el 70. La fogonera saluda desde lejos con la pala.

#### Imagen
- Un visor redondo de vidrio montado en un caño largo, que muestra la aguja de una caldera lejana.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) ajusta el visor.
- Al fondo, una fogonera con delantal de cuero y una pala saluda; Gheco en el caño.

### Micro-misión R02-N02-P4 · El candado de verdad

```meta
lugar: El cofre de Astrea
personajes: Rigel, Gheco, Astrea
carta: #privado | #abierto = false · privado de verdad, también al ejecutar · desde afuera es TS18013
recompensa: xp 10, oro 10
```

#### Escena
Astrea guarda los planos del Vidriero en un cofre. No le alcanza con una advertencia: quiere un candado de verdad.

#### Gheco sugiere
`private` lo revisa el compilador, pero en el JavaScript que corre desaparece. Un campo con `#` es privado **de verdad**: JavaScript no deja tocarlo desde afuera, ni siquiera al ejecutar.

```ts
class Cofre {
  #abierto = false;
}
```

Adentro de la clase se usa como `this.#abierto`.

#### Desafío
Completá el método `abrir`, que pone `#abierto` en `true`.

#### Pasos
1. Buscá el `___` adentro de `abrir`.
2. Cambialo por `this.#abierto = true;`.
3. Tocá **Ejecutar**. Tiene que salir `¿Abierto? false` y después `¿Abierto? true`.

#### Código inicial
```typescript
class Cofre {
  #abierto = false;

  abrir(): void {
    ___
  }

  estaAbierto(): boolean {
    return this.#abierto;
  }
}

const cofre = new Cofre();
console.log(`¿Abierto? ${cofre.estaAbierto()}`);
cofre.abrir();
console.log(`¿Abierto? ${cofre.estaAbierto()}`);
```

#### Salida esperada
```
¿Abierto? false
¿Abierto? true
```

#### Solución
```typescript
class Cofre {
  #abierto = false;

  abrir(): void {
    this.#abierto = true;
  }

  estaAbierto(): boolean {
    return this.#abierto;
  }
}

const cofre = new Cofre();
console.log(`¿Abierto? ${cofre.estaAbierto()}`);
cofre.abrir();
console.log(`¿Abierto? ${cofre.estaAbierto()}`);
```

#### Al superarla
El cofre se abre. Adentro hay planos enrollados con la letra apretada del Vidriero. Astrea lo vuelve a cerrar enseguida: —Todavía no.

#### Imagen
- Un cofre de latón con un candado intrincado, abierto, con planos enrollados adentro.
- Astrea (lechuza grande gris azulada con anteojos de latón y chaleco azul) cierra la tapa con un ala.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) espía por encima; Gheco sobre el cofre.

### Micro-misión R02-N02-P5 · La caldera segura

```meta
lugar: Las calderas del Mirador
personajes: Rigel, Gheco
carta: Todo junto | readonly en el constructor · #presion privado de verdad · private maxima · get para leer
recompensa: xp 15, monedas 5
```

#### Escena
Rigel arma la caldera definitiva del Mirador: con número que no se cambia, una presión que nadie puede tocar y un tope que solo ella conoce.

#### Gheco sugiere
Todo lo de este nodo en una clase:
- `public readonly numero`: se ve, pero no se cambia;
- `private maxima`: el tope, solo para la clase;
- `#presion`: privada de verdad;
- `get lectura`: para mirar sin tocar.

#### Desafío
Completá `cargar` para que la presión nunca pase de la máxima.

#### Pasos
1. Buscá el `___` adentro de `cargar`.
2. Cambialo por `this.#presion = Math.min(this.maxima, this.#presion + cantidad);`.
3. Tocá **Ejecutar**. Tiene que salir `C-1: 80 de 80`.

#### Código inicial
```typescript
class Caldera {
  #presion = 0;

  constructor(public readonly numero: string, private maxima: number) {}

  cargar(cantidad: number): void {
    ___
  }

  get lectura(): string {
    return `${this.numero}: ${this.#presion} de ${this.maxima}`;
  }
}

const caldera = new Caldera('C-1', 80);
caldera.cargar(50);
caldera.cargar(50);
console.log(caldera.lectura);
```

#### Salida esperada
```
C-1: 80 de 80
```

#### Solución
```typescript
class Caldera {
  #presion = 0;

  constructor(public readonly numero: string, private maxima: number) {}

  cargar(cantidad: number): void {
    this.#presion = Math.min(this.maxima, this.#presion + cantidad);
  }

  get lectura(): string {
    return `${this.numero}: ${this.#presion} de ${this.maxima}`;
  }
}

const caldera = new Caldera('C-1', 80);
caldera.cargar(50);
caldera.cargar(50);
console.log(caldera.lectura);
```

#### Al superarla
La caldera llega a 80 y se queda ahí, ronroneando tranquila, por más que el ogro le eche carbón.

#### Imagen
- Una caldera de cobre nueva y brillante, con un manómetro que se detiene en una marca roja (sin números legibles).
- Un ogro chiquito echándole carbón con una pala, frustrado.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) cruzado de brazos, satisfecho; Gheco en la caldera.

### Micro-misión R02-N02-P6 · El contador de vueltas

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco, Astrea
carta: Estado protegido | private vueltas · un método que avanza · un get que informa · nadie lo cambia desde afuera
recompensa: xp 15, monedas 5
```

#### Escena
Astrea quiere un contador de vueltas para el Planisferio, que nadie pueda adelantar a mano.

#### Gheco sugiere
La propiedad `vueltas` es `private`: solo cambia con `girar()`. Para leerla desde afuera hay un `get`.

#### Desafío
Completá la propiedad privada y el `get`.

#### Pasos
1. El primer `___` declara la propiedad: `private vueltas: number = 0;`.
2. El segundo `___` es lo que devuelve el `get`: `return this.vueltas;`.
3. Tocá **Ejecutar**. Tiene que salir `El Planisferio dio 3 vueltas`.

#### Código inicial
```typescript
class Contador {
  ___

  girar(): void {
    this.vueltas++;
  }

  get total(): number {
    ___
  }
}

const contador = new Contador();
contador.girar();
contador.girar();
contador.girar();
console.log(`El Planisferio dio ${contador.total} vueltas`);
```

#### Salida esperada
```
El Planisferio dio 3 vueltas
```

#### Solución
```typescript
class Contador {
  private vueltas: number = 0;

  girar(): void {
    this.vueltas++;
  }

  get total(): number {
    return this.vueltas;
  }
}

const contador = new Contador();
contador.girar();
contador.girar();
contador.girar();
console.log(`El Planisferio dio ${contador.total} vueltas`);
```

#### Al superarla
El contador marca tres. Astrea lo sella con lacre: —Ahora nadie hace trampa. —Y le da una **estrella de latón**.

#### Imagen
- Un contador mecánico de latón con rodillos numerados (sin números legibles), sellado con lacre azul.
- Astrea (lechuza con anteojos de latón y chaleco azul) aplica el sello con su compás.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) recibe una ficha con una estrella; Gheco aplaude.

## R02-N03 · Herencia: abstract, implements y override

```meta
tipo: tema
padre: R02-N02
precio: 10
criatura: ogre
temas: poo.herencia, poo.interfaces, poo.polimorfismo
```

### Crónica

En la pared de la fundición hay un molde distinto: no tiene fondo. Es la **forma general** de todos los instrumentos del Mirador: un nombre, un estado y un hueco que dice *acá va lo que sabe hacer cada uno*. Rigel quiere fundir una pieza con él y el vidrio se le escurre por abajo.

—Ese molde no es para fundir —dice Don Péndulo—. Es para **hacer otros moldes**. Cada instrumento lo completa a su manera.

### Objetivos

- Escribir una clase `abstract` con métodos `abstract`, y completarla en las clases que heredan.
- Usar `implements` para prometer que una clase cumple una `interface`.
- Marcar con `override` el método que reemplaza al de la clase de arriba.
- Usar `protected` y estrechar con `instanceof`.

### Antes de empezar

- R02-N01 y R02-N02.
- De JavaScript: `extends` y `super`.

### Explicación

#### El molde sin fondo: abstract
```typescript
abstract class Instrumento {
  constructor(public readonly nombre: string) {}

  abstract medir(): number;   // sin cuerpo: cada uno lo completa

  informe(): string {
    return `${this.nombre}: ${this.medir()}`;
  }
}

class Termometro extends Instrumento {
  medir(): number { return 21; }
}
```

- `new Instrumento('x')` da `TS2511`: un molde abstracto no se usa directo.
- Si `Termometro` no escribe `medir()`, da `TS2515`.

#### Prometer una forma: implements
```typescript
interface Calibrable {
  calibrar(): void;
}

class Barometro extends Instrumento implements Calibrable {
  medir(): number { return 1013; }
  calibrar(): void { console.log('Barómetro en cero'); }
}
```

Una clase puede **heredar de una sola** clase, pero **cumplir varias** interfaces: `implements A, B`.

#### Reemplazar un método: override
Si una clase escribe un método que **ya existía** (con cuerpo) en la de arriba, en el Mirador se marca con `override`:

```typescript
class Sextante extends Instrumento {
  medir(): number { return 45; }
  override informe(): string {
    return `${super.informe()} grados`;
  }
}
```

Sin `override`, el compilador avisa (`TS4114`). Así, si alguien cambia el nombre del método de arriba, te enterás. (Los métodos `abstract` no llevan `override`: se completan, no se reemplazan.)

#### protected e instanceof
- `protected`: lo usan la clase y las que heredan, pero no desde afuera.
- `if (x instanceof Barometro)`: adentro del `if`, TypeScript sabe que `x` es un `Barometro` y deja usar `calibrar()`.

### Código de ejemplo

```typescript
abstract class Instrumento {
  constructor(public readonly nombre: string) {}

  abstract medir(): number;

  informe(): string {
    return `${this.nombre}: ${this.medir()}`;
  }
}

interface Calibrable {
  calibrar(): string;
}

class Termometro extends Instrumento {
  medir(): number {
    return 21;
  }
}

class Barometro extends Instrumento implements Calibrable {
  medir(): number {
    return 1013;
  }
  calibrar(): string {
    return `${this.nombre} en cero`;
  }
}

class Sextante extends Instrumento {
  medir(): number {
    return 45;
  }
  override informe(): string {
    return `${super.informe()} grados`;
  }
}

const mesa: Instrumento[] = [new Termometro('termómetro'), new Barometro('barómetro'), new Sextante('sextante')];
for (const i of mesa) {
  console.log(i.informe());
  if (i instanceof Barometro) console.log(`  ${i.calibrar()}`);
}
```

### Salida esperada

```
termómetro: 21
barómetro: 1013
  barómetro en cero
sextante: 45 grados
```

### ¿Para qué sirve?

Cuando muchas clases comparten casi todo pero cada una hace una parte a su manera (los enemigos de un juego, los medios de pago de una tienda), la clase abstracta tiene lo común y obliga a cada una a completar lo suyo. El compilador avisa si alguna se olvida, antes de ejecutar.

### Errores habituales

**Ogro: crear un molde abstracto (TS2511).** *No se puede crear una instancia de una clase abstracta*. Creá una de las clases que heredan.

**Esqueleto: falta completar un método abstracto (TS2515).** La clase que hereda tiene que escribir todos los `abstract`.

**Esqueleto: implements incompleto (TS2420).** *La clase 'X' implementa la interfaz 'Y' de forma incorrecta*: le falta algo de la interface.

**Ogro: reemplazar sin override (TS4114).** *Este miembro debe tener un modificador "override"…*. Agregalo adelante del método.

### Micro-misión R02-N03-P1 · El molde sin fondo

```meta
lugar: La fundición
personajes: Rigel, Gheco, Don Péndulo
carta: abstract | abstract class · abstract medir(): number; sin cuerpo · cada clase que hereda lo completa
recompensa: xp 10, oro 10
```

#### Escena
Don Péndulo le muestra a Rigel el molde sin fondo. —Completalo para un termómetro. El molde general no sabe medir; el termómetro sí.

#### Gheco sugiere
Una clase `abstract` es un molde general: tiene lo común y deja **huecos** (`abstract medir(): number;`, sin cuerpo). Cada clase que hereda (`extends`) completa los huecos:

```ts
class Termometro extends Instrumento {
  medir(): number { return 21; }
}
```

#### Desafío
Completá el método `medir` del termómetro, que devuelve `21`.

#### Pasos
1. Buscá el `___` adentro de `Termometro`.
2. Cambialo por `medir(): number { return 21; }`.
3. Tocá **Ejecutar**. Tiene que salir `termómetro: 21`.

#### Código inicial
```typescript
abstract class Instrumento {
  constructor(public readonly nombre: string) {}

  abstract medir(): number;

  informe(): string {
    return `${this.nombre}: ${this.medir()}`;
  }
}

class Termometro extends Instrumento {
  ___
}

console.log(new Termometro('termómetro').informe());
```

#### Salida esperada
```
termómetro: 21
```

#### Solución
```typescript
abstract class Instrumento {
  constructor(public readonly nombre: string) {}

  abstract medir(): number;

  informe(): string {
    return `${this.nombre}: ${this.medir()}`;
  }
}

class Termometro extends Instrumento {
  medir(): number { return 21; }
}

console.log(new Termometro('termómetro').informe());
```

#### Al superarla
El termómetro sale del molde, completo. Su aguja sube hasta el 21 y se queda ahí.

#### Imagen
- Un molde de bronce sin fondo colgado en la pared de la fundición, y debajo un termómetro de vidrio y latón recién fundido.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sostiene el termómetro.
- Don Péndulo (relojero viejo de barba blanca, delantal de cuero) asiente; Gheco sobre el molde.

### Micro-misión R02-N03-P2 · Fundir el molde general

```meta
lugar: La fundición
personajes: Rigel, Gheco
criatura: ogre
carta: TS2511 | una clase abstract no se crea con new · se crea una de las que heredan
recompensa: xp 10, oro 10
```

#### Escena
Un **ogro** insiste en fundir el molde sin fondo: vierte vidrio y el vidrio se escurre por abajo.

#### Gheco sugiere
`new Instrumento(…)` da `TS2511`: un molde abstracto no se usa directo. Se crea una de las clases que lo completan, como `Barometro`.

#### Desafío
Cambiá el `new Instrumento` por un `new Barometro`.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `new Instrumento('barómetro')` por `new Barometro('barómetro')`.
3. Tocá **Ejecutar**. Tiene que salir `barómetro: 1013`.

#### Código inicial
```typescript
abstract class Instrumento {
  constructor(public readonly nombre: string) {}
  abstract medir(): number;
  informe(): string {
    return `${this.nombre}: ${this.medir()}`;
  }
}

class Barometro extends Instrumento {
  medir(): number { return 1013; }
}

const aparato = new Instrumento('barómetro');
console.log(aparato.informe());
```

#### Salida esperada
```
barómetro: 1013
```

#### Solución
```typescript
abstract class Instrumento {
  constructor(public readonly nombre: string) {}
  abstract medir(): number;
  informe(): string {
    return `${this.nombre}: ${this.medir()}`;
  }
}

class Barometro extends Instrumento {
  medir(): number { return 1013; }
}

const aparato = new Barometro('barómetro');
console.log(aparato.informe());
```

#### Al superarla
El vidrio por fin se queda en el molde del barómetro. El ogro se limpia las manos y se va a buscar otro molde que romper.

#### Imagen
- Un charco de vidrio derretido en el piso, debajo de un molde sin fondo, y al lado un barómetro de latón perfecto.
- Un ogro chiquito con las manos manchadas de vidrio.
- Rigel (chico flaco con pecas, antiparras de latón bajadas) sostiene el barómetro; Gheco esquiva el charco.

### Micro-misión R02-N03-P3 · La promesa del barómetro

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: implements | class Barometro extends Instrumento implements Calibrable · promete cumplir la interface · si falta algo, TS2420
recompensa: xp 10, oro 10
```

#### Escena
Astrea solo deja montar en el telescopio instrumentos que se puedan **calibrar**. El barómetro de Rigel tiene que prometerlo.

#### Gheco sugiere
`implements` promete que una clase cumple una `interface`. Si le falta algo, el compilador avisa:

```ts
class Barometro extends Instrumento implements Calibrable { … }
```

Una clase hereda de una sola, pero puede cumplir varias interfaces.

#### Desafío
Agregá `implements Calibrable` a la clase y escribile el método `calibrar`.

#### Pasos
1. Después de `extends Instrumento`, agregá ` implements Calibrable`.
2. Ejecutá: da `TS2420`, falta `calibrar`. En el `___`, escribí `calibrar(): string { return `${this.nombre} en cero`; }` (con comillas invertidas adentro del return).
3. Tocá **Ejecutar**. Tiene que salir `barómetro en cero`.

#### Código inicial
```typescript
abstract class Instrumento {
  constructor(public readonly nombre: string) {}
  abstract medir(): number;
}

interface Calibrable {
  calibrar(): string;
}

class Barometro extends Instrumento {
  medir(): number { return 1013; }
  ___
}

const b: Calibrable = new Barometro('barómetro');
console.log(b.calibrar());
```

#### Salida esperada
```
barómetro en cero
```

#### Solución
```typescript
abstract class Instrumento {
  constructor(public readonly nombre: string) {}
  abstract medir(): number;
}

interface Calibrable {
  calibrar(): string;
}

class Barometro extends Instrumento implements Calibrable {
  medir(): number { return 1013; }
  calibrar(): string { return `${this.nombre} en cero`; }
}

const b: Calibrable = new Barometro('barómetro');
console.log(b.calibrar());
```

#### Al superarla
La aguja del barómetro vuelve a cero con un tic. Astrea lo monta en el telescopio, al lado del ocular.

#### Imagen
- Un barómetro redondo de latón montado al costado de un telescopio enorme, con la aguja en cero.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) ajusta un tornillo.
- Astrea (lechuza con anteojos de latón y chaleco azul) observa con el compás en la mano; Gheco sobre el telescopio.

### Micro-misión R02-N03-P4 · El informe del sextante

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco
criatura: ogre
carta: override | reemplazar un método con cuerpo de la clase de arriba · se marca con override · sin él, TS4114 · super.informe() usa el de arriba
recompensa: xp 10, oro 10
```

#### Escena
El sextante mide ángulos, y su informe tiene que decir *grados* al final. Rigel reemplaza el informe general, pero el compilador se queja.

#### Gheco sugiere
Cuando una clase escribe un método que **ya tenía cuerpo** en la de arriba, lo **reemplaza**. En el Mirador eso se marca con `override`:

```ts
override informe(): string {
  return `${super.informe()} grados`;
}
```

`super.informe()` llama al informe de la clase de arriba. Sin `override`, el compilador avisa con `TS4114`.

#### Desafío
Agregá `override` al método `informe` del sextante.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Adelante de `informe(): string` (en `Sextante`), escribí `override `.
3. Tocá **Ejecutar**. Tiene que salir `sextante: 45 grados`.

#### Código inicial
```typescript
abstract class Instrumento {
  constructor(public readonly nombre: string) {}
  abstract medir(): number;
  informe(): string {
    return `${this.nombre}: ${this.medir()}`;
  }
}

class Sextante extends Instrumento {
  medir(): number { return 45; }
  informe(): string {
    return `${super.informe()} grados`;
  }
}

console.log(new Sextante('sextante').informe());
```

#### Salida esperada
```
sextante: 45 grados
```

#### Solución
```typescript
abstract class Instrumento {
  constructor(public readonly nombre: string) {}
  abstract medir(): number;
  informe(): string {
    return `${this.nombre}: ${this.medir()}`;
  }
}

class Sextante extends Instrumento {
  medir(): number { return 45; }
  override informe(): string {
    return `${super.informe()} grados`;
  }
}

console.log(new Sextante('sextante').informe());
```

#### Al superarla
El sextante apunta a una estrella y su arco marca 45. En la tarjeta del informe, al final, dice *grados*.

#### Imagen
- Un sextante de latón apuntando a una estrella por la abertura de la cúpula.
- Rigel (chico flaco con pecas, antiparras de latón subidas, chaleco marrón) mira por la mira del sextante.
- Gheco sobre el arco del sextante.

### Micro-misión R02-N03-P5 · La mesa de instrumentos

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: Polimorfismo e instanceof | Instrumento[] con distintos instrumentos · cada uno mide a su manera · if (i instanceof Barometro) deja usar calibrar
recompensa: xp 15, monedas 5
```

#### Escena
Astrea pone todos los instrumentos en la mesa y pide un informe de cada uno. Los que se pueden calibrar, además, se calibran.

#### Gheco sugiere
Un `Instrumento[]` puede tener termómetros, barómetros y sextantes: cada uno responde `informe()` a su manera. Para usar algo que solo tiene uno de ellos, se pregunta con `instanceof`:

```ts
if (i instanceof Barometro) console.log(i.calibrar());
```

Adentro del `if`, TypeScript sabe que `i` es un `Barometro`.

#### Desafío
Completá la pregunta del `if`.

#### Pasos
1. Buscá el `___` en el `if`.
2. Cambialo por `i instanceof Barometro`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
abstract class Instrumento {
  constructor(public readonly nombre: string) {}
  abstract medir(): number;
  informe(): string {
    return `${this.nombre}: ${this.medir()}`;
  }
}

class Termometro extends Instrumento {
  medir(): number { return 21; }
}

class Barometro extends Instrumento {
  medir(): number { return 1013; }
  calibrar(): string { return `${this.nombre} en cero`; }
}

const mesa: Instrumento[] = [new Termometro('termómetro'), new Barometro('barómetro')];
for (const i of mesa) {
  console.log(i.informe());
  if (___) console.log(`  ${i.calibrar()}`);
}
```

#### Salida esperada
```
termómetro: 21
barómetro: 1013
  barómetro en cero
```

#### Solución
```typescript
abstract class Instrumento {
  constructor(public readonly nombre: string) {}
  abstract medir(): number;
  informe(): string {
    return `${this.nombre}: ${this.medir()}`;
  }
}

class Termometro extends Instrumento {
  medir(): number { return 21; }
}

class Barometro extends Instrumento {
  medir(): number { return 1013; }
  calibrar(): string { return `${this.nombre} en cero`; }
}

const mesa: Instrumento[] = [new Termometro('termómetro'), new Barometro('barómetro')];
for (const i of mesa) {
  console.log(i.informe());
  if (i instanceof Barometro) console.log(`  ${i.calibrar()}`);
}
```

#### Al superarla
Cada instrumento da su medida en orden. Astrea las anota todas en su mapa.

#### Imagen
- Una mesa de latón con un termómetro, un barómetro y un sextante alineados, cada uno con una tarjetita.
- Astrea (lechuza con anteojos de latón y chaleco azul) anota con una pluma.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) calibra el barómetro; Gheco en la mesa.

### Micro-misión R02-N03-P6 · La familia de los instrumentos

```meta
lugar: La fundición
personajes: Rigel, Gheco, Don Péndulo
carta: protected | protected unidad · lo usan la clase y las que heredan · desde afuera no
recompensa: xp 15, monedas 5
```

#### Escena
Don Péndulo quiere que cada instrumento sepa su unidad (grados, milímetros…), que la usen los instrumentos para escribir su informe, pero que nadie la cambie desde afuera.

#### Gheco sugiere
`protected` está entre `private` y `public`: lo usan la clase **y las que heredan**, pero no desde afuera.

```ts
constructor(public readonly nombre: string, protected unidad: string) {}
```

La clase de abajo pasa la unidad con `super(nombre, 'grados')`.

#### Desafío
Marcá `unidad` como `protected` y completá el `super` del termómetro.

#### Pasos
1. En el constructor de `Instrumento`, el primer `___` es `protected`.
2. En `Termometro`, el segundo `___` es `super(nombre, 'grados')`.
3. Tocá **Ejecutar**. Tiene que salir `termómetro: 21 grados`.

#### Código inicial
```typescript
abstract class Instrumento {
  constructor(public readonly nombre: string, ___ unidad: string) {}
  abstract medir(): number;
  informe(): string {
    return `${this.nombre}: ${this.medir()} ${this.unidad}`;
  }
}

class Termometro extends Instrumento {
  constructor(nombre: string) {
    ___;
  }
  medir(): number { return 21; }
}

console.log(new Termometro('termómetro').informe());
```

#### Salida esperada
```
termómetro: 21 grados
```

#### Solución
```typescript
abstract class Instrumento {
  constructor(public readonly nombre: string, protected unidad: string) {}
  abstract medir(): number;
  informe(): string {
    return `${this.nombre}: ${this.medir()} ${this.unidad}`;
  }
}

class Termometro extends Instrumento {
  constructor(nombre: string) {
    super(nombre, 'grados');
  }
  medir(): number { return 21; }
}

console.log(new Termometro('termómetro').informe());
```

#### Al superarla
Don Péndulo graba *grados* en el costado del termómetro. —La familia ya sabe hablar. —Le da a Rigel una **estrella de latón**.

#### Imagen
- Una pared de la fundición con varios instrumentos de latón colgados en fila, como un árbol genealógico, unidos por líneas de bronce.
- Don Péndulo (relojero viejo de barba blanca, delantal de cuero) graba una inscripción en un termómetro.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) recibe una ficha con una estrella; Gheco mira.

## R02-N04 · static y set: lo del molde y lo que se valida

```meta
tipo: tema
padre: R02-N03
precio: 10
criatura: skeleton
temas: poo.clases, poo.encapsulamiento
```

### Crónica

En la pared de la fundición, sobre los moldes, hay un contador de bronce que marca cuántas estrellas se fundieron desde que el Mirador existe. No es de ninguna estrella: es **del molde**. Y al lado, una perilla de brillo que no deja pasar del 10, por más que la fuercen.

—El contador es del molde, no de cada pieza —dice Don Péndulo—. Y la perilla revisa lo que le das antes de aceptarlo. Las dos cosas las vas a necesitar para pelear con la Mantícora.

> Este nodo no está en el material de base (FullCursos): se agregó porque `static` y `set` se usan en casi todas las clases de los proyectos.

### Objetivos

- Usar miembros `static`: datos y métodos que son de la **clase**, no de cada objeto.
- Leer el error `TS2576`: un `static` usado desde un objeto.
- Escribir un `set` que **valida** lo que recibe, junto a su `get`.

### Antes de empezar

- R02-N01 a R02-N03: clases, `private`, `get` y herencia.

### Explicación

#### Lo que es del molde: static
```typescript
class Estrella {
  static fundidas = 0;       // una sola, para todas las estrellas

  constructor(public nombre: string) {
    Estrella.fundidas++;     // se usa con el nombre de la clase
  }

  static desdeTexto(texto: string): Estrella {
    return new Estrella(texto.trim());
  }
}

new Estrella('Vega');
const sirio = Estrella.desdeTexto('  Sirio ');
console.log(Estrella.fundidas);   // 2
console.log(sirio.fundidas);      // ✗ TS2576: es del molde, no de cada estrella
```

Un método `static` que crea objetos (como `desdeTexto`) se llama **fábrica**.

#### Validar lo que entra: set
Un `set` se usa como una propiedad, pero ejecuta código cuando le asignan algo:

```typescript
class Perilla {
  #brillo = 5;

  get brillo(): number {
    return this.#brillo;
  }

  set brillo(valor: number) {
    this.#brillo = Math.max(0, Math.min(10, valor));   // nunca menos de 0 ni más de 10
  }
}

const p = new Perilla();
p.brillo = 50;           // pasa por el set
console.log(p.brillo);   // 10
```

### Código de ejemplo

```typescript
class Estrella {
  static fundidas = 0;
  static readonly MAXIMO = 10;
  #brillo = 0;

  constructor(public nombre: string, brillo: number) {
    this.brillo = brillo;
    Estrella.fundidas++;
  }

  get brillo(): number {
    return this.#brillo;
  }

  set brillo(valor: number) {
    this.#brillo = Math.max(0, Math.min(Estrella.MAXIMO, valor));
  }
}

const vega = new Estrella('Vega', 9);
const sirio = new Estrella('Sirio', 50);
sirio.brillo = sirio.brillo - 3;
console.log(`${vega.nombre}: ${vega.brillo} · ${sirio.nombre}: ${sirio.brillo}`);
console.log(`Fundidas: ${Estrella.fundidas}`);
```

### Salida esperada

```
Vega: 9 · Sirio: 7
Fundidas: 2
```

### ¿Para qué sirve?

`static` sirve para lo que comparten todos los objetos de una clase: un contador, una constante, una fábrica que los crea desde un texto o un archivo. El `set` asegura que una propiedad nunca quede con un valor inválido, venga de donde venga.

### Errores habituales

**Esqueleto: un static usado desde un objeto (TS2576).** *La propiedad "fundidas" no existe en el tipo "Estrella". ¿Pretendía acceder al miembro estático "Estrella.fundidas"?* Usalo con el nombre de la clase.

**Ogro: un get sin set.** Si una propiedad solo tiene `get`, asignarle algo da `TS2540` (es de solo lectura). Si querés poder cambiarla, escribile el `set`.

**Troll: el set que se llama a sí mismo.** `set brillo(v) { this.brillo = v; }` se llama a sí mismo sin fin. El valor de verdad se guarda en otra propiedad (`#brillo`).

### Micro-misión R02-N04-P1 · El contador de la fundición

```meta
lugar: La fundición
personajes: Rigel, Gheco, Don Péndulo
carta: static | static fundidas = 0 · es de la clase, una sola para todas · se usa como Estrella.fundidas
recompensa: xp 10, oro 10
```

#### Escena
Don Péndulo le pide a Rigel que el molde lleve la cuenta de cuántas estrellas fundió. La cuenta no es de ninguna estrella: es del molde.

#### Gheco sugiere
Una propiedad `static` es **de la clase**: hay una sola, compartida por todos los objetos. Se usa con el nombre de la clase:

```ts
class Molde {
  static usos = 0;
}
Molde.usos++;
```

#### Desafío
Declará el contador `static`.

#### Pasos
1. Buscá el `___` adentro de la clase.
2. Cambialo por `static fundidas = 0;`.
3. Tocá **Ejecutar**. Tiene que salir `El molde fundió 3 estrellas`.

#### Código inicial
```typescript
class Estrella {
  ___

  constructor(public nombre: string) {
    Estrella.fundidas++;
  }
}

new Estrella('Vega');
new Estrella('Sirio');
new Estrella('Altair');
console.log(`El molde fundió ${Estrella.fundidas} estrellas`);
```

#### Salida esperada
```
El molde fundió 3 estrellas
```

#### Solución
```typescript
class Estrella {
  static fundidas = 0;

  constructor(public nombre: string) {
    Estrella.fundidas++;
  }
}

new Estrella('Vega');
new Estrella('Sirio');
new Estrella('Altair');
console.log(`El molde fundió ${Estrella.fundidas} estrellas`);
```

#### Al superarla
El contador de bronce de la pared avanza tres casillas: *clic, clic, clic*.

#### Imagen
- Un contador mecánico de bronce con rodillos, montado sobre la pared de moldes de la fundición (sin números legibles).
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) saca tres estrellitas del molde.
- Don Péndulo (relojero viejo de barba blanca, delantal de cuero) mira el contador; Gheco sobre él.

### Micro-misión R02-N04-P2 · El contador equivocado

```meta
lugar: La fundición
personajes: Rigel, Gheco
criatura: skeleton
carta: TS2576 | un static no se pide a un objeto · se pide a la clase: Estrella.fundidas
recompensa: xp 10, oro 10
```

#### Escena
Rigel le pregunta a una estrella cuántas se fundieron. La estrella no sabe: esa cuenta es del molde. Un **esqueleto** se ríe en el hueco del contador.

#### Gheco sugiere
`vega.fundidas` da `TS2576`: el compilador te avisa que es un miembro **estático** y te sugiere cómo usarlo: `Estrella.fundidas`.

#### Desafío
Pedile la cuenta a la clase, no a la estrella.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `vega.fundidas` por `Estrella.fundidas`.
3. Tocá **Ejecutar**. Tiene que salir `Fundidas: 2`.

#### Código inicial
```typescript
class Estrella {
  static fundidas = 0;

  constructor(public nombre: string) {
    Estrella.fundidas++;
  }
}

const vega = new Estrella('Vega');
new Estrella('Sirio');
console.log(`Fundidas: ${vega.fundidas}`);
```

#### Salida esperada
```
Fundidas: 2
```

#### Solución
```typescript
class Estrella {
  static fundidas = 0;

  constructor(public nombre: string) {
    Estrella.fundidas++;
  }
}

const vega = new Estrella('Vega');
new Estrella('Sirio');
console.log(`Fundidas: ${Estrella.fundidas}`);
```

#### Al superarla
Rigel le pregunta al molde, y el molde contesta. El esqueleto se queda sin chiste.

#### Imagen
- Una estrellita de vidrio encogiéndose de hombros frente al contador de bronce de la pared.
- Un esqueleto de alambre chiquito riéndose en el hueco del contador.
- Rigel (chico flaco con pecas, antiparras de latón) se rasca la cabeza; Gheco señala el contador.

### Micro-misión R02-N04-P3 · La fábrica de estrellas

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco, Astrea
carta: Método static | static desdeTexto(texto: string): Estrella · crea objetos · se llama con Estrella.desdeTexto(…)
recompensa: xp 10, oro 10
```

#### Escena
Astrea tiene las estrellas anotadas en tarjetas: *Vega:9*, *Sirio:10*. Rigel quiere un método que arme una estrella a partir de cada tarjeta.

#### Gheco sugiere
Un método `static` también es de la clase. Uno que **crea** objetos se llama **fábrica**:

```ts
static desdeTexto(texto: string): Estrella {
  const [nombre, brillo] = texto.split(':');
  return new Estrella(nombre, Number(brillo));
}
```

Se llama con el nombre de la clase: `Estrella.desdeTexto('Vega:9')`.

#### Desafío
Completá el `return` de la fábrica.

#### Pasos
1. Buscá el `___` en `desdeTexto`.
2. Cambialo por `new Estrella(nombre, Number(brillo))`.
3. Tocá **Ejecutar**. Tiene que salir `Vega brilla 9` y `Sirio brilla 10`.

#### Código inicial
```typescript
class Estrella {
  constructor(public nombre: string, public brillo: number) {}

  static desdeTexto(texto: string): Estrella {
    const [nombre, brillo] = texto.split(':');
    return ___;
  }
}

for (const tarjeta of ['Vega:9', 'Sirio:10']) {
  const e = Estrella.desdeTexto(tarjeta);
  console.log(`${e.nombre} brilla ${e.brillo}`);
}
```

#### Salida esperada
```
Vega brilla 9
Sirio brilla 10
```

#### Solución
```typescript
class Estrella {
  constructor(public nombre: string, public brillo: number) {}

  static desdeTexto(texto: string): Estrella {
    const [nombre, brillo] = texto.split(':');
    return new Estrella(nombre, Number(brillo));
  }
}

for (const tarjeta of ['Vega:9', 'Sirio:10']) {
  const e = Estrella.desdeTexto(tarjeta);
  console.log(`${e.nombre} brilla ${e.brillo}`);
}
```

#### Al superarla
De cada tarjeta sale una estrella encendida. Astrea las cuelga del techo de la sala.

#### Imagen
- Tarjetas de cartulina entrando en una máquina de latón y estrellitas de vidrio encendidas saliendo por el otro lado.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mete una tarjeta.
- Astrea (lechuza con anteojos de latón y chaleco azul) cuelga una estrella; Gheco sobre la máquina.

### Micro-misión R02-N04-P4 · La perilla que no se pasa

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco
carta: set | set brillo(valor: number) { … } · se usa como propiedad · valida antes de guardar · Math.max y Math.min ponen los topes
recompensa: xp 10, oro 10
```

#### Escena
La lámpara del telescopio tiene una perilla de brillo. Si alguien la fuerza más allá del 10, la lámpara se quema.

#### Gheco sugiere
Un `set` se usa como si fuera una propiedad (`lampara.brillo = 50`), pero ejecuta código antes de guardar. Así se valida:

```ts
set brillo(valor: number) {
  this.#brillo = Math.max(0, Math.min(10, valor));
}
```

`Math.min(10, valor)` no deja pasar de 10, y `Math.max(0, …)` no deja bajar de 0.

#### Desafío
Completá el `set` para que el brillo quede entre 0 y 10.

#### Pasos
1. Buscá el `___` adentro del `set`.
2. Cambialo por `this.#brillo = Math.max(0, Math.min(10, valor));`.
3. Tocá **Ejecutar**. Tiene que salir `10 0 7`.

#### Código inicial
```typescript
class Lampara {
  #brillo = 5;

  get brillo(): number {
    return this.#brillo;
  }

  set brillo(valor: number) {
    ___
  }
}

const lampara = new Lampara();
lampara.brillo = 50;
const alto = lampara.brillo;
lampara.brillo = -3;
const bajo = lampara.brillo;
lampara.brillo = 7;
console.log(alto, bajo, lampara.brillo);
```

#### Salida esperada
```
10 0 7
```

#### Solución
```typescript
class Lampara {
  #brillo = 5;

  get brillo(): number {
    return this.#brillo;
  }

  set brillo(valor: number) {
    this.#brillo = Math.max(0, Math.min(10, valor));
  }
}

const lampara = new Lampara();
lampara.brillo = 50;
const alto = lampara.brillo;
lampara.brillo = -3;
const bajo = lampara.brillo;
lampara.brillo = 7;
console.log(alto, bajo, lampara.brillo);
```

#### Al superarla
La perilla gira hasta el tope y se detiene. La lámpara brilla fuerte, pero sin quemarse.

#### Imagen
- Una lámpara de latón montada en el telescopio con una perilla de brillo que tiene un tope marcado (sin números legibles).
- Rigel (chico flaco con pecas, antiparras de latón con el lente azul bajado) gira la perilla.
- Gheco protegiéndose del brillo con la cola.

### Micro-misión R02-N04-P5 · El tope del molde

```meta
lugar: La fundición
personajes: Rigel, Gheco, Don Péndulo
carta: static readonly | static readonly MAXIMO = 10 · una constante de la clase · el set la usa como Estrella.MAXIMO
recompensa: xp 15, monedas 5
```

#### Escena
Don Péndulo quiere que el tope del brillo esté escrito **una sola vez**, en el molde, y que todas las estrellas lo respeten.

#### Gheco sugiere
`static readonly` es una **constante de la clase**: está una vez y no se cambia.

```ts
static readonly MAXIMO = 10;
```

El `set` la usa con el nombre de la clase: `Estrella.MAXIMO`. Si mañana el tope es 12, se cambia en un solo lugar.

#### Desafío
Completá la constante y el `set`.

#### Pasos
1. El primer `___` declara la constante: `static readonly MAXIMO = 10;`.
2. El segundo `___` es el cuerpo del `set`: `this.#brillo = Math.max(0, Math.min(Estrella.MAXIMO, valor));`.
3. Tocá **Ejecutar**. Tiene que salir `Vega: 9 · Sirio: 7`.

#### Código inicial
```typescript
class Estrella {
  ___
  #brillo = 0;

  constructor(public nombre: string, brillo: number) {
    this.brillo = brillo;
  }

  get brillo(): number {
    return this.#brillo;
  }

  set brillo(valor: number) {
    ___
  }
}

const vega = new Estrella('Vega', 9);
const sirio = new Estrella('Sirio', 50);
sirio.brillo = sirio.brillo - 3;
console.log(`${vega.nombre}: ${vega.brillo} · ${sirio.nombre}: ${sirio.brillo}`);
```

#### Salida esperada
```
Vega: 9 · Sirio: 7
```

#### Solución
```typescript
class Estrella {
  static readonly MAXIMO = 10;
  #brillo = 0;

  constructor(public nombre: string, brillo: number) {
    this.brillo = brillo;
  }

  get brillo(): number {
    return this.#brillo;
  }

  set brillo(valor: number) {
    this.#brillo = Math.max(0, Math.min(Estrella.MAXIMO, valor));
  }
}

const vega = new Estrella('Vega', 9);
const sirio = new Estrella('Sirio', 50);
sirio.brillo = sirio.brillo - 3;
console.log(`${vega.nombre}: ${vega.brillo} · ${sirio.nombre}: ${sirio.brillo}`);
```

#### Al superarla
Don Péndulo graba el número en el borde del molde, una sola vez. —Lo que se escribe una vez no se equivoca dos.

#### Imagen
- El borde de un molde de bronce con una inscripción grabada (sin letras legibles) y dos estrellitas de vidrio recién salidas.
- Don Péndulo (relojero viejo de barba blanca) graba con un buril.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mira; Gheco sobre el molde.

### Micro-misión R02-N04-P6 · El registro de la fundición

```meta
lugar: La fundición
personajes: Rigel, Gheco, Don Péndulo
carta: Todo junto | static para contar · fábrica static · set que valida · get para leer
recompensa: xp 15, monedas 5
```

#### Escena
Al final del día, Don Péndulo pide el registro: cuántas estrellas se fundieron y con qué brillo quedó cada una, sabiendo que algunas tarjetas pedían brillos imposibles.

#### Gheco sugiere
Todo lo del nodo: la fábrica `static desdeTexto` arma cada estrella, el constructor suma al contador `static`, y el `set` deja el brillo entre 0 y 10.

#### Desafío
Completá el constructor: guardá el brillo (pasando por el `set`) y sumá al contador.

#### Pasos
1. El primer `___`: `this.brillo = brillo;` (pasa por el `set`).
2. El segundo `___`: `Estrella.fundidas++;`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
class Estrella {
  static fundidas = 0;
  #brillo = 0;

  constructor(public nombre: string, brillo: number) {
    ___
    ___
  }

  static desdeTexto(texto: string): Estrella {
    const [nombre, brillo] = texto.split(':');
    return new Estrella(nombre, Number(brillo));
  }

  get brillo(): number {
    return this.#brillo;
  }

  set brillo(valor: number) {
    this.#brillo = Math.max(0, Math.min(10, valor));
  }
}

for (const tarjeta of ['Vega:9', 'Sirio:40', 'Polar:-2']) {
  const e = Estrella.desdeTexto(tarjeta);
  console.log(`${e.nombre}: ${e.brillo}`);
}
console.log(`Fundidas: ${Estrella.fundidas}`);
```

#### Salida esperada
```
Vega: 9
Sirio: 10
Polar: 0
Fundidas: 3
```

#### Solución
```typescript
class Estrella {
  static fundidas = 0;
  #brillo = 0;

  constructor(public nombre: string, brillo: number) {
    this.brillo = brillo;
    Estrella.fundidas++;
  }

  static desdeTexto(texto: string): Estrella {
    const [nombre, brillo] = texto.split(':');
    return new Estrella(nombre, Number(brillo));
  }

  get brillo(): number {
    return this.#brillo;
  }

  set brillo(valor: number) {
    this.#brillo = Math.max(0, Math.min(10, valor));
  }
}

for (const tarjeta of ['Vega:9', 'Sirio:40', 'Polar:-2']) {
  const e = Estrella.desdeTexto(tarjeta);
  console.log(`${e.nombre}: ${e.brillo}`);
}
console.log(`Fundidas: ${Estrella.fundidas}`);
```

#### Al superarla
Don Péndulo firma el registro y le da a Rigel una **estrella de latón**. —Hasta las tarjetas mal escritas salieron bien. Eso es un buen molde.

#### Imagen
- Un libro de registro abierto sobre la mesa de la fundición, con tres estrellitas de vidrio de distinto brillo al lado.
- Don Péndulo (relojero viejo de barba blanca, delantal de cuero) firma con una pluma.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) recibe una ficha con una estrella; Gheco sobre el libro.

## R02-N05 · enum y as const

```meta
tipo: tema
padre: R02-N04
precio: 10
criatura: goblin
temas: cal.tipos, poo.clases
```

### Crónica

En la fundición, cada molde tiene una chapa con su **tipo**: *lente*, *engranaje*, *biela*. Rigel ve que alguien escribió *engranage* con g en una chapa nueva, y ese molde quedó afuera de todas las listas.

—Para que nadie escriba mal un tipo, el Mirador tiene **listas con nombre** —dice {mentor}—. Se escriben una vez y después se eligen, nunca se tipean.

### Objetivos

- Usar un `enum` numérico (`Direccion.Norte`, que vale `0`) y uno de texto (`TipoPieza.Lente = 'lente'`).
- Recorrer las opciones de un `switch` con un `enum`.
- Leer el error de asignar un texto suelto a un `enum` (`TS2322`).
- Usar `as const` con un objeto o un arreglo, y sacar de ahí un tipo.

### Antes de empezar

- R01-N06: uniones de opciones (`'parado' | 'girando'`).
- R02-N04: miembros `static`.

### Explicación

#### enum numérico
```typescript
enum Direccion {
  Norte,   // 0
  Sur,     // 1
  Este,    // 2
  Oeste,   // 3
}
console.log(Direccion.Norte, Direccion[0]);   // 0 'Norte'
```

Cada opción vale un número desde 0. Se puede ir y volver: `Direccion[0]` da `'Norte'`.

#### enum de texto
```typescript
enum TipoPieza {
  Lente = 'lente',
  Engranaje = 'engranaje',
  Biela = 'biela',
}
let tipo: TipoPieza = TipoPieza.Lente;
tipo = 'lente';   // ✗ TS2322: hay que usar TipoPieza.Lente
```

Los de texto se leen mejor al mostrarlos o guardarlos. Son los más usados.

#### as const: la alternativa sin enum
Mucho código de TypeScript moderno no usa `enum`: usa un objeto común con `as const`, que congela los valores:

```typescript
const Estado = {
  Parado: 'parado',
  Girando: 'girando',
} as const;
type Estado = typeof Estado[keyof typeof Estado];   // 'parado' | 'girando'
```

Esa última línea parece un trabalenguas. Se lee de adentro hacia afuera:
- `typeof Estado`: el tipo del objeto;
- `keyof typeof Estado`: sus claves (`'Parado' | 'Girando'`);
- `typeof Estado[…]`: los valores de esas claves.

`as const` también sirve con arreglos: `const MODOS = ['parado', 'girando'] as const;` y `type Modo = typeof MODOS[number];`.

> ¿enum o as const? Los dos andan. `as const` es JavaScript común (sin nada propio de TypeScript), y por eso hoy es el más elegido. Vas a ver los dos en proyectos reales.

### Código de ejemplo

```typescript
enum TipoPieza {
  Lente = 'lente',
  Engranaje = 'engranaje',
  Biela = 'biela',
}

function horasDeTrabajo(tipo: TipoPieza): number {
  switch (tipo) {
    case TipoPieza.Lente:
      return 3;
    case TipoPieza.Engranaje:
      return 5;
    case TipoPieza.Biela:
      return 2;
  }
}

const MODOS = ['parado', 'girando', 'trabado'] as const;
type Modo = typeof MODOS[number];
const modo: Modo = 'girando';

console.log(TipoPieza.Engranaje, horasDeTrabajo(TipoPieza.Engranaje));
console.log(MODOS.join(' / '), '→', modo);
```

### Salida esperada

```
engranaje 5
parado / girando / trabado → girando
```

### ¿Para qué sirve?

Cada vez que un dato tiene un conjunto fijo de valores (los estados de un pedido, los tipos de enemigo, las direcciones), un `enum` o un `as const` evita los errores de tipeo y deja que el editor te sugiera las opciones.

### Errores habituales

**Goblin: un texto suelto donde va un enum (TS2322).** *El tipo '"lente"' no se puede asignar al tipo 'TipoPieza'*. Usá `TipoPieza.Lente`.

**Ogro: cambiar algo as const (TS2540).** Con `as const`, los valores son de solo lectura.

**El enum numérico que acepta cualquier número.** Ojo: en versiones viejas de TypeScript, un `enum` numérico aceptaba cualquier número. Preferí los de texto.

### Micro-misión R02-N05-P1 · Los cuatro rumbos

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco
carta: enum numérico | enum Direccion { Norte, Sur, Este, Oeste } · valen 0, 1, 2, 3 · Direccion[0] da 'Norte'
recompensa: xp 10, oro 10
```

#### Escena
El telescopio gira hacia cuatro rumbos. Rigel quiere nombrarlos en vez de acordarse de qué número es cada uno.

#### Gheco sugiere
Un `enum` es una **lista con nombre**. En uno numérico, cada opción vale un número desde 0:

```ts
enum Direccion { Norte, Sur, Este, Oeste }
```

`Direccion.Este` vale `2`, y `Direccion[2]` da `'Este'`.

#### Desafío
Completá el `enum` con los cuatro rumbos, en ese orden.

#### Pasos
1. Buscá el `___` adentro de `enum Direccion`.
2. Cambialo por `Norte, Sur, Este, Oeste`.
3. Tocá **Ejecutar**. Tiene que salir `Este vale 2` y `El 3 es Oeste`.

#### Código inicial
```typescript
enum Direccion {
  ___
}

console.log(`Este vale ${Direccion.Este}`);
console.log(`El 3 es ${Direccion[3]}`);
```

#### Salida esperada
```
Este vale 2
El 3 es Oeste
```

#### Solución
```typescript
enum Direccion {
  Norte, Sur, Este, Oeste
}

console.log(`Este vale ${Direccion.Este}`);
console.log(`El 3 es ${Direccion[3]}`);
```

#### Al superarla
Rigel graba los cuatro nombres en el aro del telescopio. Ya no tiene que contar con los dedos.

#### Imagen
- El aro giratorio de un telescopio de latón con cuatro marcas grabadas en los rumbos (sin letras legibles).
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) graba una marca.
- Gheco sobre el aro.

### Micro-misión R02-N05-P2 · Las chapas de los moldes

```meta
lugar: La fundición
personajes: Rigel, Gheco, Don Péndulo
carta: enum de texto | Lente = 'lente' · cada opción con su texto · se usa TipoPieza.Lente
recompensa: xp 10, oro 10
```

#### Escena
Don Péndulo quiere chapas nuevas para los moldes, con el tipo escrito una sola vez y bien.

#### Gheco sugiere
En un `enum` de texto, cada opción tiene su valor:

```ts
enum Color { Rojo = 'rojo', Azul = 'azul' }
```

Al mostrarlo sale el texto: `Color.Azul` es `'azul'`.

#### Desafío
Completá la opción que falta: `Biela = 'biela'`.

#### Pasos
1. Buscá el `___` adentro del `enum`.
2. Cambialo por `Biela = 'biela',`.
3. Tocá **Ejecutar**. Tiene que salir `lente, engranaje, biela`.

#### Código inicial
```typescript
enum TipoPieza {
  Lente = 'lente',
  Engranaje = 'engranaje',
  ___
}

console.log([TipoPieza.Lente, TipoPieza.Engranaje, TipoPieza.Biela].join(', '));
```

#### Salida esperada
```
lente, engranaje, biela
```

#### Solución
```typescript
enum TipoPieza {
  Lente = 'lente',
  Engranaje = 'engranaje',
  Biela = 'biela',
}

console.log([TipoPieza.Lente, TipoPieza.Engranaje, TipoPieza.Biela].join(', '));
```

#### Al superarla
Las chapas nuevas brillan en cada molde, todas bien escritas.

#### Imagen
- Tres chapas de latón grabadas colgadas de tres moldes de bronce (sin letras legibles).
- Don Péndulo (relojero viejo de barba blanca) atornilla una chapa.
- Rigel (chico flaco con pecas, antiparras de latón) le alcanza los tornillos; Gheco mira.

### Micro-misión R02-N05-P3 · La chapa mal escrita

```meta
lugar: La fundición
personajes: Rigel, Gheco
criatura: goblin
carta: TS2322 con un enum | un texto suelto no es un TipoPieza · se usa TipoPieza.Engranaje
recompensa: xp 10, oro 10
```

#### Escena
Un goblin escribió *engranaje* a mano en una chapa. El compilador no la acepta.

#### Gheco sugiere
Una variable de tipo `TipoPieza` solo acepta las opciones del `enum`, escritas con su nombre: `TipoPieza.Engranaje`. Un texto suelto da `TS2322`, aunque tenga las mismas letras.

#### Desafío
Cambiá el texto suelto por la opción del `enum`.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `'engranaje'` por `TipoPieza.Engranaje`.
3. Tocá **Ejecutar**. Tiene que salir `Molde: engranaje`.

#### Código inicial
```typescript
enum TipoPieza {
  Lente = 'lente',
  Engranaje = 'engranaje',
}

const tipo: TipoPieza = 'engranaje';
console.log(`Molde: ${tipo}`);
```

#### Salida esperada
```
Molde: engranaje
```

#### Solución
```typescript
enum TipoPieza {
  Lente = 'lente',
  Engranaje = 'engranaje',
}

const tipo: TipoPieza = TipoPieza.Engranaje;
console.log(`Molde: ${tipo}`);
```

#### Al superarla
La chapa escrita a mano se cae sola. En su lugar aparece la chapa oficial.

#### Imagen
- Una chapa de cartón escrita a mano cayéndose de un molde, y una chapa de latón oficial en su lugar.
- Un goblin chiquito con un engranaje en la espalda y un lápiz en la mano.
- Rigel (chico flaco con pecas, antiparras de latón) atornilla la chapa oficial; Gheco se ríe.

### Micro-misión R02-N05-P4 · El estado sin enum

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco, Astrea
carta: as const | const Estado = { … } as const · type Estado = typeof Estado[keyof typeof Estado] · JavaScript común
recompensa: xp 10, oro 10
```

#### Escena
Astrea prefiere los estados del Planisferio en un objeto común, que también entiende cualquier programa de JavaScript.

#### Gheco sugiere
Un objeto con `as const` queda congelado: sus valores son exactamente esos textos. De ahí se saca el tipo:

```ts
type Estado = typeof Estado[keyof typeof Estado];
```

Se lee de adentro hacia afuera: el tipo del objeto (`typeof Estado`), sus claves (`keyof`), y los valores de esas claves. Da `'parado' | 'girando'`.

#### Desafío
Completá el `as const` del objeto.

#### Pasos
1. Buscá el `___` después de la llave que cierra el objeto.
2. Cambialo por `as const`.
3. Tocá **Ejecutar**. Tiene que salir `Nuevo estado: girando`.

#### Código inicial
```typescript
const Estado = {
  Parado: 'parado',
  Girando: 'girando',
} ___;
type Estado = typeof Estado[keyof typeof Estado];

function cambiar(estado: Estado): void {
  console.log(`Nuevo estado: ${estado}`);
}

cambiar(Estado.Girando);
```

#### Salida esperada
```
Nuevo estado: girando
```

#### Solución
```typescript
const Estado = {
  Parado: 'parado',
  Girando: 'girando',
} as const;
type Estado = typeof Estado[keyof typeof Estado];

function cambiar(estado: Estado): void {
  console.log(`Nuevo estado: ${estado}`);
}

cambiar(Estado.Girando);
```

#### Al superarla
El Planisferio cambia de estado y lo anuncia con una campanita.

#### Imagen
- Un tablero de estados de latón junto al planetario mecánico, con una luz encendida en una de dos posiciones.
- Astrea (lechuza con anteojos de latón y chaleco azul) toca una campanita.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mueve una perilla; Gheco mira.

### Micro-misión R02-N05-P5 · Las horas de cada molde

```meta
lugar: La fundición
personajes: Rigel, Gheco, Don Péndulo
carta: switch con enum | case TipoPieza.Lente: return 3; · un caso por opción · la función devuelve number
recompensa: xp 15, monedas 5
```

#### Escena
Don Péndulo quiere saber cuántas horas lleva fundir cada tipo de pieza, para organizar el turno de la noche.

#### Gheco sugiere
Un `switch` con un `enum` tiene un `case` por opción:

```ts
switch (tipo) {
  case TipoPieza.Lente:
    return 3;
  …
}
```

Si están todas las opciones, TypeScript sabe que la función siempre devuelve un número.

#### Desafío
Completá el caso que falta: la biela lleva 2 horas.

#### Pasos
1. Buscá el `___` en el `switch`.
2. Cambialo por `case TipoPieza.Biela:` y, en el renglón de abajo, `return 2;`.
3. Tocá **Ejecutar**. Tiene que salir `Turno de la noche: 10 horas`.

#### Código inicial
```typescript
enum TipoPieza {
  Lente = 'lente',
  Engranaje = 'engranaje',
  Biela = 'biela',
}

function horas(tipo: TipoPieza): number {
  switch (tipo) {
    case TipoPieza.Lente:
      return 3;
    case TipoPieza.Engranaje:
      return 5;
    ___
  }
}

const turno: TipoPieza[] = [TipoPieza.Lente, TipoPieza.Engranaje, TipoPieza.Biela];
let total = 0;
for (const t of turno) total += horas(t);
console.log(`Turno de la noche: ${total} horas`);
```

#### Salida esperada
```
Turno de la noche: 10 horas
```

#### Solución
```typescript
enum TipoPieza {
  Lente = 'lente',
  Engranaje = 'engranaje',
  Biela = 'biela',
}

function horas(tipo: TipoPieza): number {
  switch (tipo) {
    case TipoPieza.Lente:
      return 3;
    case TipoPieza.Engranaje:
      return 5;
    case TipoPieza.Biela:
      return 2;
  }
}

const turno: TipoPieza[] = [TipoPieza.Lente, TipoPieza.Engranaje, TipoPieza.Biela];
let total = 0;
for (const t of turno) total += horas(t);
console.log(`Turno de la noche: ${total} horas`);
```

#### Al superarla
Don Péndulo anota el turno en la pizarra: diez horas. —Una noche larga, pero ordenada.

#### Imagen
- Una pizarra con un turno de trabajo dibujado con rayitas (sin números legibles) y un reloj de pared grande.
- Don Péndulo (relojero viejo de barba blanca) anota con tiza.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) se arremanga; Gheco sobre el reloj.

### Micro-misión R02-N05-P6 · Las posiciones de la palanca

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco, Astrea
carta: Arreglo as const | const MODOS = ['parado', 'girando'] as const · type Modo = typeof MODOS[number] · se puede recorrer
recompensa: xp 15, monedas 5
```

#### Escena
Astrea quiere que la palanca del Planisferio muestre todas sus posiciones en un cartel, y que el tipo `Modo` salga de esa misma lista, sin escribirla dos veces.

#### Gheco sugiere
Un arreglo con `as const` sirve para las dos cosas: **recorrerlo** (es un arreglo de verdad) y **sacar el tipo** de sus elementos:

```ts
const MODOS = ['parado', 'girando', 'trabado'] as const;
type Modo = typeof MODOS[number];   // 'parado' | 'girando' | 'trabado'
```

`[number]` quiere decir «cualquier elemento del arreglo».

#### Desafío
Completá el tipo `Modo`.

#### Pasos
1. Buscá el `___` después de `type Modo =`.
2. Cambialo por `typeof MODOS[number]`.
3. Tocá **Ejecutar**. Tiene que salir `Posiciones: parado / girando / trabado` y `Ahora: girando`.

#### Código inicial
```typescript
const MODOS = ['parado', 'girando', 'trabado'] as const;
type Modo = ___;

const actual: Modo = 'girando';
console.log(`Posiciones: ${MODOS.join(' / ')}`);
console.log(`Ahora: ${actual}`);
```

#### Salida esperada
```
Posiciones: parado / girando / trabado
Ahora: girando
```

#### Solución
```typescript
const MODOS = ['parado', 'girando', 'trabado'] as const;
type Modo = typeof MODOS[number];

const actual: Modo = 'girando';
console.log(`Posiciones: ${MODOS.join(' / ')}`);
console.log(`Ahora: ${actual}`);
```

#### Al superarla
El cartel de la palanca se escribe solo, a partir de la lista. Astrea le da a Rigel una **estrella de latón**: —Una sola lista, dos usos. Así me gusta.

#### Imagen
- Un cartel de latón junto a la palanca del planetario mecánico, con tres posiciones grabadas (sin letras legibles).
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sonríe; Gheco sobre la palanca.

## R02-N06 · Genéricos

```meta
tipo: tema
padre: R02-N05
precio: 10
criatura: goblin
temas: poo.genericos, col.listas, col.mapas
```

### Crónica

En el fondo de la fundición hay un molde raro: una caja de bronce con una ranura en la tapa que dice *T*. Rigel mete un engranaje y la caja se adapta: desde ese momento, solo acepta engranajes. Mete una lente en otra caja igual, y esa solo acepta lentes.

—Es el molde de los moldes —dice Don Péndulo—. No sabe de antemano qué va a guardar, pero en cuanto le decís qué, no se olvida más. El Vidriero los llamaba **genéricos**.

### Objetivos

- Escribir una función genérica: `function primero<T>(lista: T[]): T | undefined`.
- Entender por qué un genérico es mejor que `any`: **recuerda** el tipo.
- Escribir una clase genérica: `class Pila<T>`.
- Usar las clases genéricas de JavaScript con su tipo: `Map<string, number>` y `Set<string>`.

### Antes de empezar

- R01-N06: tipos de función.
- R02-N01 a R02-N05: clases.
- Ya lo usaste sin saberlo: `Array<number>` es un genérico.

### Explicación

#### Una función que sirve para cualquier tipo
```typescript
function primero<T>(lista: T[]): T | undefined {
  return lista[0];
}

const n = primero([3, 4]);          // T es number → n es number | undefined
const s = primero(['Vega', 'Sirio']); // T es string → s es string | undefined
```

`<T>` es un **parámetro de tipo**: un hueco que se llena en cada llamada, según lo que le pases. Lo podés llamar como quieras, pero por costumbre es `T`.

#### Por qué no any
```typescript
function primeroAny(lista: any[]): any { return lista[0]; }
const x = primeroAny([3, 4]);   // x es any: el compilador se olvidó de que era un número
```

Con `any`, lo que sale no tiene tipo. Con `<T>`, el compilador **recuerda** qué entró y te dice qué sale.

#### Una clase genérica
```typescript
class Pila<T> {
  private items: T[] = [];
  apilar(item: T): void { this.items.push(item); }
  desapilar(): T | undefined { return this.items.pop(); }
}

const pila = new Pila<number>();
pila.apilar(1);
pila.apilar('dos');   // ✗ TS2345: esta pila es de números
```

#### Los genéricos de JavaScript
```typescript
const stock = new Map<string, number>();   // claves de texto, valores numéricos
stock.set('lente', 3);
const vistas = new Set<string>();           // un conjunto de textos, sin repetidos
vistas.add('Vega');
```

### Código de ejemplo

```typescript
function primero<T>(lista: T[]): T | undefined {
  return lista[0];
}

class Pila<T> {
  private items: T[] = [];

  apilar(item: T): void {
    this.items.push(item);
  }

  desapilar(): T | undefined {
    return this.items.pop();
  }

  get tamano(): number {
    return this.items.length;
  }
}

const pila = new Pila<string>();
pila.apilar('lente');
pila.apilar('biela');

const stock = new Map<string, number>([['lente', 3]]);
stock.set('biela', 5);

console.log(primero([12, 4, 7]), primero(['Vega', 'Sirio']));
console.log(pila.desapilar(), pila.tamano);
console.log(stock.get('biela'), stock.size);
```

### Salida esperada

```
12 Vega
biela 1
5 2
```

### ¿Para qué sirve?

Las estructuras que guardan cosas (listas, pilas, colas, diccionarios, cachés) y las funciones que las recorren no dependen de **qué** guardan. Con genéricos se escriben una vez y sirven para todo, sin perder los tipos. Toda la biblioteca de TypeScript está hecha así: `Array<T>`, `Map<K, V>`, `Promise<T>`.

### Errores habituales

**Goblin: meter otro tipo en un genérico (TS2345).** Una `Pila<number>` no acepta textos.

**Usar any en vez de un genérico.** Compila, pero lo que sale pierde el tipo, y los errores vuelven a aparecer al ejecutar.

**Orco: lo que puede no estar.** `primero([])` devuelve `undefined`: por eso el tipo es `T | undefined`. Preguntá antes de usarlo, o usá `??`.

### Micro-misión R02-N06-P1 · La caja que se adapta

```meta
lugar: La fundición
personajes: Rigel, Gheco, Don Péndulo
carta: Función genérica | function primero<T>(lista: T[]): T | undefined · <T> se llena en cada llamada · recuerda el tipo
recompensa: xp 10, oro 10
```

#### Escena
Don Péndulo le pide a Rigel una máquina que saque la primera pieza de cualquier lista: de engranajes, de lentes, de lo que sea.

#### Gheco sugiere
Una función **genérica** tiene un parámetro de tipo entre `<>`:

```ts
function primero<T>(lista: T[]): T | undefined {
  return lista[0];
}
```

`T` se llena con lo que le pases: con `[1, 2]`, `T` es `number`; con `['a']`, es `string`.

#### Desafío
Agregá el parámetro de tipo `<T>` después del nombre de la función.

#### Pasos
1. Buscá el `___` entre `primero` y el paréntesis.
2. Cambialo por `<T>`.
3. Tocá **Ejecutar**. Tiene que salir `12 Vega`.

#### Código inicial
```typescript
function primero___(lista: T[]): T | undefined {
  return lista[0];
}

console.log(primero([12, 4, 7]), primero(['Vega', 'Sirio']));
```

#### Salida esperada
```
12 Vega
```

#### Solución
```typescript
function primero<T>(lista: T[]): T | undefined {
  return lista[0];
}

console.log(primero([12, 4, 7]), primero(['Vega', 'Sirio']));
```

#### Al superarla
La máquina saca un engranaje de una fila y una estrella de la otra. Es la misma máquina.

#### Imagen
- Una máquina de latón con una pinza que saca la primera pieza de dos filas distintas: una de engranajes y otra de estrellitas.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) mueve la palanca.
- Don Péndulo (relojero viejo de barba blanca, delantal de cuero) observa; Gheco sobre la pinza.

### Micro-misión R02-N06-P2 · El Camaleón vuelve

```meta
lugar: La fundición
personajes: Rigel, Gheco
criatura: goblin
carta: Genérico contra any | con any lo que sale pierde el tipo · con <T> el compilador recuerda · el error aparece antes
recompensa: xp 10, oro 10
```

#### Escena
Alguien dejó en la fundición una máquina con `any`. Saca la primera pieza bien, pero después el programa explota: trata un texto como si fuera un número.

#### Gheco sugiere
Con `any`, lo que sale de la función pierde el tipo, y el compilador no puede avisar nada. Si la hacés genérica, el compilador sabe que sale un `string` y te avisa que los textos no tienen `toFixed`.

#### Desafío
Hacé genérica la función y arreglá lo que aparece.

#### Pasos
1. Tocá **Ejecutar**: explota al ejecutar.
2. Cambiá la firma por `function primero<T>(lista: T[]): T | undefined {`.
3. Ejecutá: ahora el compilador avisa antes. Cambiá `nombre?.toFixed(1)` por `nombre?.toUpperCase()`.
4. Tocá **Ejecutar**. Tiene que salir `VEGA`.

#### Código inicial
```typescript
function primero(lista: any[]): any {
  return lista[0];
}

const nombre = primero(['Vega', 'Sirio']);
console.log(nombre?.toFixed(1));
```

#### Salida esperada
```
VEGA
```

#### Solución
```typescript
function primero<T>(lista: T[]): T | undefined {
  return lista[0];
}

const nombre = primero(['Vega', 'Sirio']);
console.log(nombre?.toUpperCase());
```

#### Al superarla
Rigel tira la máquina vieja al canasto de chatarra. —Que el Camaleón la busque ahí.

#### Imagen
- Un canasto de chatarra con una máquina vieja que cambia de color, y una máquina nueva de latón brillante en la mesa.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) se sacude las manos.
- Gheco asomado al canasto.

### Micro-misión R02-N06-P3 · La pila de bandejas

```meta
lugar: La fundición
personajes: Rigel, Gheco
carta: Clase genérica | class Pila<T> · private items: T[] · apilar(item: T) · desapilar(): T | undefined
recompensa: xp 10, oro 10
```

#### Escena
Las bandejas con piezas recién fundidas se apilan una arriba de otra. La última que entra es la primera que sale.

#### Gheco sugiere
Una clase también puede ser genérica. Cada vez que la creás, decís qué guarda:

```ts
class Pila<T> {
  private items: T[] = [];
  apilar(item: T): void { this.items.push(item); }
  desapilar(): T | undefined { return this.items.pop(); }
}

const bandejas = new Pila<string>();
```

#### Desafío
Completá el tipo de lo que devuelve `desapilar`.

#### Pasos
1. Buscá el `___` después de `desapilar()`.
2. Cambialo por `T | undefined` (si la pila está vacía, no hay nada).
3. Tocá **Ejecutar**. Tiene que salir `Sale: resorte · Quedan: 2`.

#### Código inicial
```typescript
class Pila<T> {
  private items: T[] = [];

  apilar(item: T): void {
    this.items.push(item);
  }

  desapilar(): ___ {
    return this.items.pop();
  }

  get tamano(): number {
    return this.items.length;
  }
}

const bandejas = new Pila<string>();
bandejas.apilar('lente');
bandejas.apilar('biela');
bandejas.apilar('resorte');
console.log(`Sale: ${bandejas.desapilar()} · Quedan: ${bandejas.tamano}`);
```

#### Salida esperada
```
Sale: resorte · Quedan: 2
```

#### Solución
```typescript
class Pila<T> {
  private items: T[] = [];

  apilar(item: T): void {
    this.items.push(item);
  }

  desapilar(): T | undefined {
    return this.items.pop();
  }

  get tamano(): number {
    return this.items.length;
  }
}

const bandejas = new Pila<string>();
bandejas.apilar('lente');
bandejas.apilar('biela');
bandejas.apilar('resorte');
console.log(`Sale: ${bandejas.desapilar()} · Quedan: ${bandejas.tamano}`);
```

#### Al superarla
Rigel saca la bandeja de arriba: la del resorte. Las otras dos esperan su turno.

#### Imagen
- Una pila de tres bandejas de latón con piezas, y la de arriba levantada.
- Rigel (chico flaco con pecas, antiparras de latón, guantes sin dedos) levanta la bandeja.
- Gheco sentado en la pila.

### Micro-misión R02-N06-P4 · La bandeja equivocada

```meta
lugar: La fundición
personajes: Rigel, Gheco
criatura: goblin
carta: Un genérico se fija al crearlo | new Pila<number>() solo acepta números · otro tipo es TS2345
recompensa: xp 10, oro 10
```

#### Escena
Un goblin quiere apilar una lente en la pila de las medidas, que es de números.

#### Gheco sugiere
`new Pila<number>()` fija `T` en `number` para esa pila: desde ahí, `apilar` solo acepta números. Lo demás da `TS2345`.

#### Desafío
Apilá la medida `4` en lugar de `'lente'`.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `medidas.apilar('lente');` por `medidas.apilar(4);`.
3. Tocá **Ejecutar**. Tiene que salir `Arriba: 4`.

#### Código inicial
```typescript
class Pila<T> {
  private items: T[] = [];
  apilar(item: T): void {
    this.items.push(item);
  }
  desapilar(): T | undefined {
    return this.items.pop();
  }
}

const medidas = new Pila<number>();
medidas.apilar(12);
medidas.apilar('lente');
console.log(`Arriba: ${medidas.desapilar()}`);
```

#### Salida esperada
```
Arriba: 4
```

#### Solución
```typescript
class Pila<T> {
  private items: T[] = [];
  apilar(item: T): void {
    this.items.push(item);
  }
  desapilar(): T | undefined {
    return this.items.pop();
  }
}

const medidas = new Pila<number>();
medidas.apilar(12);
medidas.apilar(4);
console.log(`Arriba: ${medidas.desapilar()}`);
```

#### Al superarla
La lente rebota en la pila de las medidas y cae en la mano del goblin, que se la lleva a otra parte.

#### Imagen
- Una pila de bandejas con medidas grabadas y una lente de vidrio rebotando en el borde.
- Un goblin chiquito con un engranaje en la espalda atajando la lente.
- Rigel (chico flaco con pecas, antiparras de latón) apila una pieza; Gheco mira.

### Micro-misión R02-N06-P5 · El stock de la fundición

```meta
lugar: La fundición
personajes: Rigel, Gheco, Don Péndulo
carta: Map<K, V> | new Map<string, number>() · set(clave, valor) · get(clave) puede ser undefined · ?? 0
recompensa: xp 15, monedas 5
```

#### Escena
Don Péndulo lleva el stock en un cuaderno: cuántas piezas hay de cada tipo. Rigel lo pasa a un `Map`.

#### Gheco sugiere
`Map` es una clase genérica de JavaScript con **dos** tipos: el de las claves y el de los valores.

```ts
const stock = new Map<string, number>();
stock.set('lente', 3);
stock.get('lente');   // number | undefined: puede no estar
```

Como `get` puede devolver `undefined`, se usa con `?? 0`.

#### Desafío
Completá los tipos del `Map`.

#### Pasos
1. Buscá el `___` adentro de `new Map<___>()`.
2. Cambialo por `string, number`.
3. Tocá **Ejecutar**. Tiene que salir `lente: 5 · tuerca: 0 · tipos: 2`.

#### Código inicial
```typescript
const stock = new Map<___>();
stock.set('lente', 3);
stock.set('biela', 1);
stock.set('lente', (stock.get('lente') ?? 0) + 2);

console.log(`lente: ${stock.get('lente')} · tuerca: ${stock.get('tuerca') ?? 0} · tipos: ${stock.size}`);
```

#### Salida esperada
```
lente: 5 · tuerca: 0 · tipos: 2
```

#### Solución
```typescript
const stock = new Map<string, number>();
stock.set('lente', 3);
stock.set('biela', 1);
stock.set('lente', (stock.get('lente') ?? 0) + 2);

console.log(`lente: ${stock.get('lente')} · tuerca: ${stock.get('tuerca') ?? 0} · tipos: ${stock.size}`);
```

#### Al superarla
Don Péndulo cierra su cuaderno viejo. —Cuarenta años con esto. Ya era hora.

#### Imagen
- Un cuaderno viejo de cuero cerrado y al lado un fichero nuevo de latón con cajoncitos (sin letras legibles).
- Don Péndulo (relojero viejo de barba blanca, delantal de cuero) cierra el cuaderno con nostalgia.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) ordena el fichero; Gheco sobre el cuaderno.

### Micro-misión R02-N06-P6 · Las estrellas vistas

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: Set<T> y genérico con dos tipos | new Set<string>() no repite · function emparejar<A, B>(a: A, b: B): [A, B]
recompensa: xp 15, monedas 5
```

#### Escena
Astrea anota las estrellas que vio esta noche, sin repetir, y las empareja con la hora de la última vista.

#### Gheco sugiere
`Set<string>` es un conjunto de textos: si agregás uno repetido, no lo guarda dos veces.

Un genérico puede tener **varios** parámetros de tipo:

```ts
function emparejar<A, B>(a: A, b: B): [A, B] {
  return [a, b];
}
```

`emparejar('Vega', 21)` devuelve un `[string, number]`.

#### Desafío
Completá el tipo del `Set` y los parámetros de tipo de `emparejar`.

#### Pasos
1. El primer `___` es `<string>` (en `new Set<string>()`).
2. El segundo `___` es `<A, B>` (después de `emparejar`).
3. Tocá **Ejecutar**. Tiene que salir `Vistas: 3` y `Vega a las 23`.

#### Código inicial
```typescript
const vistas = new Set___();
for (const e of ['Vega', 'Sirio', 'Vega', 'Altair']) vistas.add(e);

function emparejar___(a: A, b: B): [A, B] {
  return [a, b];
}

const [estrella, hora] = emparejar('Vega', 23);
console.log(`Vistas: ${vistas.size}`);
console.log(`${estrella} a las ${hora}`);
```

#### Salida esperada
```
Vistas: 3
Vega a las 23
```

#### Solución
```typescript
const vistas = new Set<string>();
for (const e of ['Vega', 'Sirio', 'Vega', 'Altair']) vistas.add(e);

function emparejar<A, B>(a: A, b: B): [A, B] {
  return [a, b];
}

const [estrella, hora] = emparejar('Vega', 23);
console.log(`Vistas: ${vistas.size}`);
console.log(`${estrella} a las ${hora}`);
```

#### Al superarla
Astrea cierra su libreta: tres estrellas, sin repetir. Le da a Rigel una **estrella de latón**.

#### Imagen
- Una libreta de observación abierta con tres estrellas dibujadas y la cúpula abierta al cielo detrás.
- Astrea (lechuza con anteojos de latón y chaleco azul) escribe con una pluma.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mira por el telescopio; Gheco sobre la libreta.

## R02-N07 · Restricciones, keyof y typeof

```meta
tipo: tema
padre: R02-N06
precio: 10
criatura: goblin
temas: poo.genericos, cal.tipos
```

### Crónica

La caja genérica tiene un problema: acepta **cualquier** cosa, hasta piezas que no tienen brillo. Y la máquina que elige la estrella más brillante necesita que todas tengan brillo.

—Un molde que sirve para todo está bien —dice Don Péndulo—, pero a veces hay que decir **qué mínimo** tiene que tener lo que entra. Y a veces necesitás los **nombres** de las partes, no las partes.

### Objetivos

- Restringir un genérico: `<T extends { brillo: number }>`.
- Usar `keyof T`: la unión de los nombres de las propiedades.
- Escribir `function leer<T, K extends keyof T>(obj: T, clave: K): T[K]`.
- Sacar el tipo de un valor con `typeof`.
- Darle un valor por defecto a un genérico: `<T = string>`.

### Antes de empezar

- R02-N06: genéricos.
- R02-N05: `typeof … [keyof typeof …]`, que ahora se explica de a una pieza.

### Explicación

#### Un mínimo: extends
```typescript
function masBrillante<T extends { brillo: number }>(lista: T[]): T {
  return lista.reduce((a, b) => (b.brillo > a.brillo ? b : a));
}
```

`T extends { brillo: number }` quiere decir: «cualquier tipo, siempre que tenga `brillo`». Adentro se puede usar `.brillo`, y lo que sale conserva todo lo demás (el nombre, la distancia…).

#### Los nombres de las partes: keyof
```typescript
type Estrella = { nombre: string; brillo: number };
type Parte = keyof Estrella;   // 'nombre' | 'brillo'
```

Con un genérico, sirve para leer una propiedad por su nombre sin perder el tipo:

```typescript
function leer<T, K extends keyof T>(obj: T, clave: K): T[K] {
  return obj[clave];
}
leer(vega, 'brillo');   // number
leer(vega, 'brilo');    // ✗ TS2345: no hay ninguna propiedad 'brilo'
```

`T[K]` es «el tipo de la propiedad `K` de `T`».

#### El tipo de un valor: typeof
```typescript
const config = { cupula: 'abierta', zoom: 30 };
type Config = typeof config;   // { cupula: string; zoom: number }
```

Ojo: este `typeof` es el de los **tipos** (va después de `type … =`). El otro, el de JavaScript, devuelve un texto (`'number'`) cuando el programa corre.

#### Un genérico por defecto
```typescript
class Etiqueta<T = string> {
  constructor(public valor: T) {}
}
```

### Código de ejemplo

```typescript
type Estrella = { nombre: string; brillo: number; distancia: number };

function masBrillante<T extends { brillo: number }>(lista: T[]): T {
  return lista.reduce((a, b) => (b.brillo > a.brillo ? b : a));
}

function leer<T, K extends keyof T>(obj: T, clave: K): T[K] {
  return obj[clave];
}

const cielo: Estrella[] = [
  { nombre: 'Vega', brillo: 9, distancia: 25 },
  { nombre: 'Sirio', brillo: 10, distancia: 9 },
];

const config = { cupula: 'abierta', zoom: 30 };
type Config = typeof config;
const otra: Config = { cupula: 'cerrada', zoom: 10 };

const mejor = masBrillante(cielo);
console.log(mejor.nombre, leer(mejor, 'distancia'));
console.log(otra.cupula, leer(config, 'zoom'));
```

### Salida esperada

```
Sirio 9
cerrada 30
```

### ¿Para qué sirve?

Las restricciones dejan escribir funciones genéricas que igual usan algo de lo que reciben (ordenar por fecha, buscar por id). `keyof` sirve para leer, ordenar o filtrar por el nombre de una propiedad sin escribir mal ese nombre. `typeof` evita escribir dos veces la forma de un objeto que ya existe.

### Errores habituales

**Goblin: algo que no cumple el mínimo (TS2345 o TS2353).** Si le pasás un objeto sin `brillo` a `masBrillante`, el compilador avisa qué falta.

**Esqueleto: un nombre de propiedad mal escrito (TS2345).** *No se puede asignar un argumento de tipo ""brilo"" al parámetro de tipo ""nombre" | "brillo" | "distancia""* (el compilador pone las comillas dobles dos veces): el mensaje te muestra los nombres que valen.

**Confundir los dos typeof.** `typeof x === 'number'` es de JavaScript (corre). `type T = typeof x` es de TypeScript (solo para el compilador).

### Micro-misión R02-N07-P1 · La más brillante

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: Restricción | <T extends { brillo: number }> · cualquier tipo que tenga brillo · lo que sale conserva todo lo demás
recompensa: xp 10, oro 10
```

#### Escena
Astrea quiere una máquina que elija la estrella más brillante de cualquier lista: de estrellas, de faroles, de lo que tenga brillo.

#### Gheco sugiere
Con `extends`, un genérico pide un **mínimo**:

```ts
function masBrillante<T extends { brillo: number }>(lista: T[]): T { … }
```

Adentro se puede usar `.brillo`. Y lo que sale es del mismo tipo que entró: si entraron estrellas, sale una estrella con su nombre.

#### Desafío
Completá la restricción del genérico.

#### Pasos
1. Buscá el `___` adentro de `<T ___>`.
2. Cambialo por `extends { brillo: number }`.
3. Tocá **Ejecutar**. Tiene que salir `La más brillante: Sirio`.

#### Código inicial
```typescript
function masBrillante<T ___>(lista: T[]): T {
  return lista.reduce((a, b) => (b.brillo > a.brillo ? b : a));
}

const cielo = [
  { nombre: 'Vega', brillo: 9 },
  { nombre: 'Sirio', brillo: 10 },
  { nombre: 'Altair', brillo: 8 },
];
console.log(`La más brillante: ${masBrillante(cielo).nombre}`);
```

#### Salida esperada
```
La más brillante: Sirio
```

#### Solución
```typescript
function masBrillante<T extends { brillo: number }>(lista: T[]): T {
  return lista.reduce((a, b) => (b.brillo > a.brillo ? b : a));
}

const cielo = [
  { nombre: 'Vega', brillo: 9 },
  { nombre: 'Sirio', brillo: 10 },
  { nombre: 'Altair', brillo: 8 },
];
console.log(`La más brillante: ${masBrillante(cielo).nombre}`);
```

#### Al superarla
El telescopio gira solo y apunta a Sirio. Astrea asiente: —La de siempre.

#### Imagen
- Un telescopio de latón girando hacia la estrella más brillante del cielo, con un haz de luz.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) suelta una palanca.
- Astrea (lechuza con anteojos de latón y chaleco azul) mira por el ocular; Gheco sobre el tubo.

### Micro-misión R02-N07-P2 · El farol sin brillo

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco
criatura: goblin
carta: No cumple el mínimo | algo sin la propiedad que pide el extends · el compilador avisa qué falta
recompensa: xp 10, oro 10
```

#### Escena
Un goblin coló en la lista un farol con *luz* en lugar de *brillo*. La máquina no lo acepta.

#### Gheco sugiere
Si algo de la lista no tiene lo que pide el `extends`, el compilador avisa y dice qué falta. El farol tiene `luz`, pero la máquina pide `brillo`.

#### Desafío
Cambiá `luz` por `brillo` en el farol.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el farol, cambiá `luz: 4` por `brillo: 4`.
3. Tocá **Ejecutar**. Tiene que salir `La más brillante: Vega`.

#### Código inicial
```typescript
function masBrillante<T extends { brillo: number }>(lista: T[]): T {
  return lista.reduce((a, b) => (b.brillo > a.brillo ? b : a));
}

console.log(`La más brillante: ${masBrillante([
  { nombre: 'Vega', brillo: 9 },
  { nombre: 'farol', luz: 4 },
]).nombre}`);
```

#### Salida esperada
```
La más brillante: Vega
```

#### Solución
```typescript
function masBrillante<T extends { brillo: number }>(lista: T[]): T {
  return lista.reduce((a, b) => (b.brillo > a.brillo ? b : a));
}

console.log(`La más brillante: ${masBrillante([
  { nombre: 'Vega', brillo: 9 },
  { nombre: 'farol', brillo: 4 },
]).nombre}`);
```

#### Al superarla
El farol entra en la lista con su brillo bien escrito. Pierde contra Vega, pero por lo menos juega.

#### Imagen
- Un farol de latón con una etiqueta corregida al lado de una estrella de vidrio mucho más brillante.
- Un goblin chiquito con un engranaje en la espalda escondiendo un lápiz.
- Rigel (chico flaco con pecas, antiparras de latón) corrige la etiqueta; Gheco mira.

### Micro-misión R02-N07-P3 · Leer por el nombre

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco, Astrea
carta: keyof | K extends keyof T · el nombre de una propiedad que existe · T[K] es su tipo
recompensa: xp 10, oro 10
```

#### Escena
Astrea quiere una máquina que lea cualquier dato de una ficha, diciéndole el nombre del dato.

#### Gheco sugiere
`keyof T` es la unión de los **nombres** de las propiedades de `T`:

```ts
type Estrella = { nombre: string; brillo: number };
// keyof Estrella es 'nombre' | 'brillo'
```

Con `K extends keyof T`, el segundo parámetro solo acepta nombres que existen, y `T[K]` es el tipo de esa propiedad.

#### Desafío
Completá el segundo parámetro de tipo.

#### Pasos
1. Buscá el `___` después de `<T, `.
2. Cambialo por `K extends keyof T`.
3. Tocá **Ejecutar**. Tiene que salir `Vega 25`.

#### Código inicial
```typescript
function leer<T, ___>(obj: T, clave: K): T[K] {
  return obj[clave];
}

const vega = { nombre: 'Vega', brillo: 9, distancia: 25 };
console.log(leer(vega, 'nombre'), leer(vega, 'distancia'));
```

#### Salida esperada
```
Vega 25
```

#### Solución
```typescript
function leer<T, K extends keyof T>(obj: T, clave: K): T[K] {
  return obj[clave];
}

const vega = { nombre: 'Vega', brillo: 9, distancia: 25 };
console.log(leer(vega, 'nombre'), leer(vega, 'distancia'));
```

#### Al superarla
La máquina lee la ficha y devuelve justo el dato pedido, con su tipo. Astrea la guarda junto al catálogo.

#### Imagen
- Una ficha de estrella de cartulina en una máquina lectora de latón que ilumina un solo renglón (sin letras legibles).
- Astrea (lechuza con anteojos de latón y chaleco azul) gira una perilla.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mira el resultado; Gheco sobre la máquina.

### Micro-misión R02-N07-P4 · El nombre mal escrito

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco
criatura: skeleton
carta: keyof atrapa los nombres mal escritos | 'brilo' no es una propiedad · el mensaje muestra los nombres que valen
recompensa: xp 10, oro 10
```

#### Escena
Rigel le pide a la máquina el *brilo* de Vega. Un **esqueleto** se mete en el hueco de la letra que falta.

#### Gheco sugiere
Con `K extends keyof T`, el compilador revisa que el nombre exista. Y el mensaje de error muestra **todos los nombres que valen**: es una buena manera de encontrar cuál quisiste escribir.

#### Desafío
Corregí el nombre de la propiedad.

#### Pasos
1. Tocá **Ejecutar** y leé el error: muestra los nombres que valen.
2. Cambiá `'brilo'` por `'brillo'`.
3. Tocá **Ejecutar**. Tiene que salir `Brillo de Vega: 9`.

#### Código inicial
```typescript
function leer<T, K extends keyof T>(obj: T, clave: K): T[K] {
  return obj[clave];
}

const vega = { nombre: 'Vega', brillo: 9 };
console.log(`Brillo de Vega: ${leer(vega, 'brilo')}`);
```

#### Salida esperada
```
Brillo de Vega: 9
```

#### Solución
```typescript
function leer<T, K extends keyof T>(obj: T, clave: K): T[K] {
  return obj[clave];
}

const vega = { nombre: 'Vega', brillo: 9 };
console.log(`Brillo de Vega: ${leer(vega, 'brillo')}`);
```

#### Al superarla
Con la letra en su lugar, el esqueleto se queda sin hueco y se desarma.

#### Imagen
- Una tarjeta con una palabra a la que le falta una letra y un esqueleto de alambre chiquito metido en el hueco.
- Rigel (chico flaco con pecas, antiparras de latón con la lupa bajada) completa la letra con una pluma.
- Gheco señala el hueco.

### Micro-misión R02-N07-P5 · La configuración de la cúpula

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: typeof en los tipos | type Config = typeof config · el tipo de un valor que ya existe · no se escribe dos veces
recompensa: xp 15, monedas 5
```

#### Escena
Astrea tiene la configuración de la cúpula escrita en un objeto. Rigel necesita otra igual para la cúpula chica, con la misma forma.

#### Gheco sugiere
`typeof` adentro de un tipo **saca el tipo de un valor** que ya existe:

```ts
const config = { cupula: 'abierta', zoom: 30 };
type Config = typeof config;   // { cupula: string; zoom: number }
```

Así no hay que escribir la forma dos veces.

#### Desafío
Completá el tipo `Config`.

#### Pasos
1. Buscá el `___` después de `type Config =`.
2. Cambialo por `typeof grande`.
3. Tocá **Ejecutar**. Tiene que salir `Grande: abierta (30x) · Chica: cerrada (10x)`.

#### Código inicial
```typescript
const grande = { cupula: 'abierta', zoom: 30 };
type Config = ___;

const chica: Config = { cupula: 'cerrada', zoom: 10 };

function describir(c: Config): string {
  return `${c.cupula} (${c.zoom}x)`;
}

console.log(`Grande: ${describir(grande)} · Chica: ${describir(chica)}`);
```

#### Salida esperada
```
Grande: abierta (30x) · Chica: cerrada (10x)
```

#### Solución
```typescript
const grande = { cupula: 'abierta', zoom: 30 };
type Config = typeof grande;

const chica: Config = { cupula: 'cerrada', zoom: 10 };

function describir(c: Config): string {
  return `${c.cupula} (${c.zoom}x)`;
}

console.log(`Grande: ${describir(grande)} · Chica: ${describir(chica)}`);
```

#### Al superarla
Las dos cúpulas quedan configuradas igual, cada una con sus valores.

#### Imagen
- Dos cúpulas de latón de distinto tamaño, una abierta y una cerrada, con paneles de control iguales.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) ajusta el panel de la chica.
- Astrea (lechuza con anteojos de latón) controla la grande; Gheco entre las dos.

### Micro-misión R02-N07-P6 · La etiqueta por defecto

```meta
lugar: La fundición
personajes: Rigel, Gheco, Don Péndulo
carta: Genérico por defecto | class Etiqueta<T = string> · si no decís el tipo, usa string · new Etiqueta<number>(4) lo cambia
recompensa: xp 15, monedas 5
```

#### Escena
Don Péndulo pone etiquetas en los moldes. Casi todas son de texto, pero algunas llevan un número.

#### Gheco sugiere
Un parámetro de tipo puede tener un valor **por defecto**:

```ts
class Etiqueta<T = string> {
  constructor(public valor: T) {}
}
```

Si no decís el tipo, usa el de por defecto o lo deduce del valor; `new Etiqueta<number>(4)` lo fija en `number`.

#### Desafío
Completá el genérico con su tipo por defecto.

#### Pasos
1. Buscá el `___` después de `class Etiqueta`.
2. Cambialo por `<T = string>`.
3. Tocá **Ejecutar**. Tiene que salir `lente · 4`.

#### Código inicial
```typescript
class Etiqueta___ {
  constructor(public valor: T) {}

  mostrar(): string {
    return String(this.valor);
  }
}

const deTexto = new Etiqueta('lente');
const deNumero = new Etiqueta<number>(4);
console.log(`${deTexto.mostrar()} · ${deNumero.mostrar()}`);
```

#### Salida esperada
```
lente · 4
```

#### Solución
```typescript
class Etiqueta<T = string> {
  constructor(public valor: T) {}

  mostrar(): string {
    return String(this.valor);
  }
}

const deTexto = new Etiqueta('lente');
const deNumero = new Etiqueta<number>(4);
console.log(`${deTexto.mostrar()} · ${deNumero.mostrar()}`);
```

#### Al superarla
Las etiquetas quedan colgadas, de texto y de número. Don Péndulo le da a Rigel una **estrella de latón**: —Mañana viene la Mantícora. Descansá.

#### Imagen
- Moldes de bronce con etiquetas colgantes de cartulina, unas con palabras y otras con números (sin letras legibles).
- Don Péndulo (relojero viejo de barba blanca) cuelga una etiqueta con un hilo.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) recibe una ficha con una estrella; Gheco se columpia de una etiqueta.

## R02-N08 · Jefe: la Mantícora de las Mil Formas

```meta
tipo: jefe
padre: R02-N07
precio: 10
criatura: dragon
insignia: Molde de la Mantícora
insignia_descripcion: Venciste a la Mantícora de las Mil Formas: tus moldes sirven para cualquier pieza sin perder la medida.
usa: poo.clases, poo.herencia, poo.genericos, poo.encapsulamiento, cal.tipos
```

### Crónica

Una noche, los moldes de la fundición amanecen mezclados: engranajes con forma de lente, lentes que se doblan como resortes, cajas que aceptan cualquier cosa. En medio del desastre, un autómata de bronce con cuerpo de león, alas de vidrio y una cola llena de moldes: **la Mantícora de las Mil Formas**. Cada pieza que toca cambia de forma.

—Se alimenta de los moldes sin medida —dice Don Péndulo—. Mientras una caja acepte cualquier cosa, ella va a poder meter lo que quiera.

—Vas a necesitar todo lo de la fundición —agrega {mentor}—: clases, privacidad, herencia, enums y, sobre todo, genéricos.

### Objetivos

- Integrar todo lo de la rama: clases, `private`, `static`, `set`, herencia, `enum` y genéricos con restricciones.
- Cambiar `any` por genéricos que recuerdan el tipo.
- Partir el problema en clases chicas.

### Antes de empezar

- Todos los nodos de los Moldes de Estrellas (R02-N01 a R02-N07).

### Explicación

#### Cómo encarar un jefe
1. **Leé la consigna entera** y anotá qué entra y qué tiene que salir.
2. **Buscá los moldes sin medida**: `any`, propiedades públicas que no deberían serlo, textos sueltos donde va un `enum`.
3. **Arreglá de a uno** y ejecutá: el compilador te muestra lo que estaba escondido.

#### Las trampas de la Mantícora (y la verdad)
| La Mantícora dice… | La verdad |
|---|---|
| "una caja `any` sirve para todo" | una caja `<T>` sirve para todo **y** recuerda qué guarda |
| "cualquiera puede tocar el stock" | `private` y un método que valida |
| "el tipo de pieza se escribe a mano" | un `enum` evita los errores de tipeo |
| "todas las piezas miden igual" | cada clase completa su `abstract` a su manera |

### Micro-misión R02-N08-P1 · La caja de la Mantícora

```meta
lugar: La fundición
personajes: Rigel, Gheco, la Mantícora de las Mil Formas
criatura: goblin
carta: Trampa 1 | cambiá any por <T> · new Caja<number>() · el compilador encuentra lo que no es número
recompensa: xp 15, monedas 3
```

#### Escena
La Mantícora dejó una caja que acepta cualquier cosa. Adentro, entre las medidas, metió un texto. La suma da *16cinco*.

#### Gheco sugiere
Con `any`, la caja no recuerda qué guarda. Si la hacés genérica (`Caja<T>`) y la creás como `new Caja<number>()`, el compilador encuentra enseguida lo que no es un número.

#### Desafío
Hacé genérica la caja y arreglá lo que aparece.

#### Pasos
1. Tocá **Ejecutar**: da `Total: 16cinco`.
2. Cambiá `class Caja {` por `class Caja<T> {`, y los dos `any` por `T`.
3. Cambiá `new Caja()` por `new Caja<number>()`.
4. Ejecutá: el compilador marca `'cinco'`. Cambialo por `5`.
5. Tocá **Ejecutar**. Tiene que salir `Total: 21`.

#### Código inicial
```typescript
class Caja {
  private items: any[] = [];

  guardar(item: any): void {
    this.items.push(item);
  }

  todos(): any[] {
    return [...this.items];
  }
}

const medidas = new Caja();
medidas.guardar(12);
medidas.guardar(4);
medidas.guardar('cinco');

let total = 0;
for (const m of medidas.todos()) total += m;
console.log(`Total: ${total}`);
```

#### Salida esperada
```
Total: 21
```

#### Solución
```typescript
class Caja<T> {
  private items: T[] = [];

  guardar(item: T): void {
    this.items.push(item);
  }

  todos(): T[] {
    return [...this.items];
  }
}

const medidas = new Caja<number>();
medidas.guardar(12);
medidas.guardar(4);
medidas.guardar(5);

let total = 0;
for (const m of medidas.todos()) total += m;
console.log(`Total: ${total}`);
```

#### Al superarla
La caja se cierra con su medida grabada: *números*. La Mantícora pierde un molde de la cola.

#### Imagen
- Una caja de bronce con una ranura grabada que se cierra sobre unas medidas, y un papel con un garabato expulsado.
- La Mantícora de las Mil Formas (autómata de bronce con cuerpo de león, alas de vidrio y una cola cargada de moldes) retrocede.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) sostiene la caja; Gheco en su hombro.

### Micro-misión R02-N08-P2 · El stock abierto

```meta
lugar: La fundición
personajes: Rigel, Gheco, la Mantícora de las Mil Formas
criatura: ogre
carta: Trampa 2 | el stock private · un método que valida · nunca negativo
recompensa: xp 15, monedas 3
```

#### Escena
La Mantícora le restó al stock de lentes más de lo que había, y quedó en *-7*. Cualquiera podía tocar el número desde afuera.

#### Gheco sugiere
Si el stock es `private`, nadie lo cambia desde afuera: solo con `retirar`, que revisa que no quede negativo (`Math.max(0, …)`).

#### Desafío
Marcá el stock como `private` y cambiá la línea de la Mantícora por un `retirar(10)`.

#### Pasos
1. Cambiá `cantidad: number = 3;` por `private cantidad: number = 3;`.
2. Ejecutá: la línea `lentes.cantidad = -7;` da `TS2341`. Cambiala por `lentes.retirar(10);`.
3. Tocá **Ejecutar**. Tiene que salir `Lentes: 0`.

#### Código inicial
```typescript
class Stock {
  cantidad: number = 3;

  retirar(n: number): void {
    this.cantidad = Math.max(0, this.cantidad - n);
  }

  get total(): number {
    return this.cantidad;
  }
}

const lentes = new Stock();
lentes.cantidad = -7;
console.log(`Lentes: ${lentes.total}`);
```

#### Salida esperada
```
Lentes: 0
```

#### Solución
```typescript
class Stock {
  private cantidad: number = 3;

  retirar(n: number): void {
    this.cantidad = Math.max(0, this.cantidad - n);
  }

  get total(): number {
    return this.cantidad;
  }
}

const lentes = new Stock();
lentes.retirar(10);
console.log(`Lentes: ${lentes.total}`);
```

#### Al superarla
El contador de lentes vuelve a cero, que es lo que de verdad hay. La Mantícora pierde otro molde.

#### Imagen
- Un contador de stock de latón que marca cero, con un candado chiquito en la tapa.
- La Mantícora (autómata de bronce con cuerpo de león y cola de moldes) intenta abrir el candado con la cola.
- Rigel (chico flaco con pecas, antiparras de latón) cierra la tapa; Gheco mira.

### Micro-misión R02-N08-P3 · Las piezas que cambian de forma

```meta
lugar: La fundición
personajes: Rigel, Gheco, la Mantícora de las Mil Formas
criatura: ogre
carta: Trampa 3 | abstract para lo común · cada pieza completa su medida · un enum para el tipo
recompensa: xp 15, monedas 3
```

#### Escena
La Mantícora convenció a una lente de que era un engranaje. Si cada pieza dice su tipo con un `enum` y calcula su peso a su manera, no hay forma de confundirlas.

#### Gheco sugiere
- `Pieza` es `abstract`, con `abstract peso(): number`.
- Cada clase de abajo dice su tipo con el `enum` y completa su `peso`.
- La lente pesa su medida por 2; el engranaje, su medida por 5.

#### Desafío
Completá la clase `Engranaje`.

#### Pasos
1. En `Engranaje`, el primer `___` es el tipo: `readonly tipo = TipoPieza.Engranaje;`.
2. El segundo `___` es el peso: `peso(): number { return this.medida * 5; }`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
enum TipoPieza {
  Lente = 'lente',
  Engranaje = 'engranaje',
}

abstract class Pieza {
  abstract readonly tipo: TipoPieza;
  constructor(public medida: number) {}
  abstract peso(): number;
  describir(): string {
    return `${this.tipo} de ${this.medida} mm pesa ${this.peso()} g`;
  }
}

class Lente extends Pieza {
  readonly tipo = TipoPieza.Lente;
  peso(): number { return this.medida * 2; }
}

class Engranaje extends Pieza {
  ___
  ___
}

const piezas: Pieza[] = [new Lente(4), new Engranaje(12)];
for (const p of piezas) console.log(p.describir());
```

#### Salida esperada
```
lente de 4 mm pesa 8 g
engranaje de 12 mm pesa 60 g
```

#### Solución
```typescript
enum TipoPieza {
  Lente = 'lente',
  Engranaje = 'engranaje',
}

abstract class Pieza {
  abstract readonly tipo: TipoPieza;
  constructor(public medida: number) {}
  abstract peso(): number;
  describir(): string {
    return `${this.tipo} de ${this.medida} mm pesa ${this.peso()} g`;
  }
}

class Lente extends Pieza {
  readonly tipo = TipoPieza.Lente;
  peso(): number { return this.medida * 2; }
}

class Engranaje extends Pieza {
  readonly tipo = TipoPieza.Engranaje;
  peso(): number { return this.medida * 5; }
}

const piezas: Pieza[] = [new Lente(4), new Engranaje(12)];
for (const p of piezas) console.log(p.describir());
```

#### Al superarla
La lente vuelve a ser lente; el engranaje, engranaje. La Mantícora ruge: ya casi no le quedan moldes.

#### Imagen
- Una lente y un engranaje de latón sobre la mesa, cada uno con su chapa, recuperando su forma original.
- La Mantícora (autómata de bronce con cuerpo de león, alas de vidrio y cola de moldes casi vacía) ruge.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sostiene el calibre; Gheco detrás de él.

### Micro-misión R02-N08-P4 · La medida mínima

```meta
lugar: La fundición
personajes: Rigel, Gheco, la Mantícora de las Mil Formas
criatura: goblin
carta: Trampa 4 | <T extends { medida: number }> · promedio de cualquier lista que tenga medida · lo que no tiene medida no entra
recompensa: xp 15, monedas 3
```

#### Escena
La Mantícora quiere sacar el promedio de una lista donde metió un pedazo de cola sin medida. La máquina tiene que aceptar cualquier pieza, pero solo si tiene medida.

#### Gheco sugiere
Un genérico con restricción acepta cualquier tipo que cumpla el mínimo:

```ts
function promedio<T extends { medida: number }>(lista: T[]): number { … }
```

#### Desafío
Completá la restricción y el cálculo del promedio.

#### Pasos
1. El primer `___` es la restricción: `extends { medida: number }`.
2. El segundo `___` es la suma de las medidas: `lista.reduce((suma, p) => suma + p.medida, 0)`.
3. Tocá **Ejecutar**. Tiene que salir `Promedio: 6 mm`.

#### Código inicial
```typescript
function promedio<T ___>(lista: T[]): number {
  const total = ___;
  return total / lista.length;
}

const piezas = [
  { nombre: 'lente', medida: 4 },
  { nombre: 'biela', medida: 12 },
  { nombre: 'resorte', medida: 2 },
];
console.log(`Promedio: ${promedio(piezas)} mm`);
```

#### Salida esperada
```
Promedio: 6 mm
```

#### Solución
```typescript
function promedio<T extends { medida: number }>(lista: T[]): number {
  const total = lista.reduce((suma, p) => suma + p.medida, 0);
  return total / lista.length;
}

const piezas = [
  { nombre: 'lente', medida: 4 },
  { nombre: 'biela', medida: 12 },
  { nombre: 'resorte', medida: 2 },
];
console.log(`Promedio: ${promedio(piezas)} mm`);
```

#### Al superarla
El pedazo de cola de la Mantícora rebota de la máquina: no tiene medida. El promedio sale limpio.

#### Imagen
- Una máquina promediadora de latón con tres piezas en su bandeja y un pedazo de cola de bronce rebotando afuera.
- La Mantícora (autómata de bronce con cuerpo de león) recoge su pedazo de cola, furiosa.
- Rigel (chico flaco con pecas, antiparras de latón) lee el resultado; Gheco aplaude.

### Micro-misión R02-N08-P5 · La Mantícora cae

```meta
lugar: La fundición
personajes: Rigel, Gheco, Don Péndulo, Astrea, la Mantícora de las Mil Formas
criatura: dragon
carta: El jefe | clase genérica con dos tipos · Map privado · static para contar · un set que valida
recompensa: xp 20, monedas 5
```

#### Escena
Sin moldes donde esconderse, la Mantícora intenta un último truco: desordenar el **inventario** de la fundición. Rigel arma uno que no se puede desordenar: genérico, privado y con reglas.

#### Gheco sugiere
Todo lo de la rama:
- `Inventario<K, V>`: una clase genérica con **dos** tipos, como `Map`;
- el `Map` adentro es `private`;
- un `static` cuenta cuántos inventarios hay;
- `obtener` devuelve `V | undefined`.

#### Desafío
Completá los tres huecos del inventario.

#### Pasos
1. El primer `___` son los parámetros de tipo de la clase: `<K, V>`.
2. El segundo `___` es el `Map` privado: `private mapa = new Map<K, V>();`.
3. El tercer `___` es lo que devuelve `obtener`: `V | undefined`.
4. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
class Inventario___ {
  static creados = 0;
  ___

  constructor(public readonly nombre: string) {
    Inventario.creados++;
  }

  agregar(clave: K, valor: V): void {
    this.mapa.set(clave, valor);
  }

  obtener(clave: K): ___ {
    return this.mapa.get(clave);
  }

  get tamano(): number {
    return this.mapa.size;
  }
}

const stock = new Inventario<string, number>('stock');
stock.agregar('lente', 5);
stock.agregar('biela', 2);

const moldes = new Inventario<number, string>('moldes');
moldes.agregar(1, 'molde de estrella');

console.log(`${stock.nombre}: lente ${stock.obtener('lente')}, tuerca ${stock.obtener('tuerca') ?? 0} (${stock.tamano} tipos)`);
console.log(`${moldes.nombre}: ${moldes.obtener(1)}`);
console.log(`Inventarios: ${Inventario.creados}`);
```

#### Salida esperada
```
stock: lente 5, tuerca 0 (2 tipos)
moldes: molde de estrella
Inventarios: 2
```

#### Solución
```typescript
class Inventario<K, V> {
  static creados = 0;
  private mapa = new Map<K, V>();

  constructor(public readonly nombre: string) {
    Inventario.creados++;
  }

  agregar(clave: K, valor: V): void {
    this.mapa.set(clave, valor);
  }

  obtener(clave: K): V | undefined {
    return this.mapa.get(clave);
  }

  get tamano(): number {
    return this.mapa.size;
  }
}

const stock = new Inventario<string, number>('stock');
stock.agregar('lente', 5);
stock.agregar('biela', 2);

const moldes = new Inventario<number, string>('moldes');
moldes.agregar(1, 'molde de estrella');

console.log(`${stock.nombre}: lente ${stock.obtener('lente')}, tuerca ${stock.obtener('tuerca') ?? 0} (${stock.tamano} tipos)`);
console.log(`${moldes.nombre}: ${moldes.obtener(1)}`);
console.log(`Inventarios: ${Inventario.creados}`);
```

#### Al superarla
La Mantícora no encuentra un solo molde sin medida. Se queda quieta, y su cola cargada de moldes se suelta: caen al piso, uno por uno, y cada uno tiene ahora su medida grabada. Don Péndulo levanta el último y se lo da a Rigel: el **Molde de la Mantícora**. —Sirve para cualquier pieza —dice— y no se olvida nunca de cuál.

#### Imagen
- Una mantícora de bronce (cuerpo de león, alas de vidrio, cola larga) desarmándose en el piso de la fundición, con sus moldes cayendo ordenados.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) recibe un molde de bronce brillante.
- Don Péndulo (relojero viejo de barba blanca, delantal de cuero) se lo entrega; Astrea (lechuza con anteojos de latón) observa desde una viga; Gheco festeja.
