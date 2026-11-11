# RAMA R03 · El Teatro del Titiritero: clases, módulos y closures

```meta
tipo: tronco
posicion: 3
```

## R03-N01 · Clases: el molde de los títeres

```meta
tipo: tema
padre: R02-N07
precio: 10
criatura: skeleton
temas: poo.clases
```

### Crónica

Detrás de la Avenida hay un teatrito de madera con cortinas rojas: el **Teatro del Titiritero**. Lo maneja **Hilván**, un titiritero joven, de dedos larguísimos, que tiene cien títeres y los hace uno por uno, a mano: le pinta la cara, le cose la ropa, le ata los hilos. Tarda una semana por títere.

—Si todos los títeres tienen cara, ropa e hilos —dice {mentor}—, no hace falta empezar de cero cada vez. Se hace un **molde**, y del molde salen todos los que quieras, cada uno con lo suyo. En JavaScript, el molde se llama **clase**.

### Objetivos

- Escribir una clase con `class`, su `constructor` y sus métodos.
- Crear objetos (instancias) con `new`.
- Usar `this` adentro de la clase para hablar del objeto.
- Entender que cada instancia tiene sus propios datos y comparte los métodos.

### Antes de empezar

- R01-N06 y R01-N07: objetos y funciones (y el `this` de un método).

### Explicación

#### Una clase
```javascript
class Titere {
  constructor(nombre, color) {
    this.nombre = nombre;   // cada títere, con su nombre
    this.color = color;
    this.energia = 3;
  }

  saludar() {
    return `${this.nombre} hace una reverencia`;
  }
}

const payaso = new Titere('Payaso', 'rojo');
const bailarina = new Titere('Bailarina', 'blanco');
console.log(payaso.saludar());
```
- El `constructor` corre una vez, al hacer `new`, y arma el objeto.
- `this` es **el objeto que se está usando**: en `payaso.saludar()`, `this` es `payaso`.
- Los métodos se escriben sin `function` y sin coma entre uno y otro.

#### Instancias
`payaso` y `bailarina` son **instancias** de `Titere`: cada uno tiene sus datos (`nombre`, `color`, `energia`), pero los dos usan el mismo método `saludar`.
```javascript
payaso instanceof Titere;   // true
```

#### Métodos que cambian el objeto
```javascript
bailar() {
  if (this.energia === 0) return `${this.nombre} está cansado`;
  this.energia--;
  return `${this.nombre} baila`;
}
```

### Código de ejemplo

```javascript
class Titere {
  constructor(nombre, color) {
    this.nombre = nombre;
    this.color = color;
    this.energia = 2;
  }

  saludar() {
    return `${this.nombre} (${this.color}) hace una reverencia`;
  }

  bailar() {
    if (this.energia === 0) return `${this.nombre} está cansado`;
    this.energia--;
    return `${this.nombre} baila`;
  }
}

const payaso = new Titere('Payaso', 'rojo');
const bailarina = new Titere('Bailarina', 'blanco');

console.log(payaso.saludar());
console.log(bailarina.bailar(), '·', bailarina.bailar(), '·', bailarina.bailar());
console.log(payaso.energia, bailarina.energia);
console.log(payaso);
console.log(payaso instanceof Titere);
```

### Salida esperada

```
Payaso (rojo) hace una reverencia
Bailarina baila · Bailarina baila · Bailarina está cansado
2 0
Titere { nombre: 'Payaso', color: 'rojo', energia: 2 }
true
```

### ¿Para qué sirve?

Los personajes de un juego, los productos de una tienda, los usuarios de una aplicación: cuando hay muchas cosas del mismo tipo, cada una con sus datos y con las mismas acciones, una clase las ordena. Muchos frameworks y bibliotecas de JavaScript se usan creando y extendiendo clases.

### Errores habituales

**Esqueleto: olvidarse el `this`.** Adentro de un método, `nombre` (sin `this.`) busca una variable que no existe: `ReferenceError: nombre is not defined`.

**Goblin: olvidarse el `new`.** `Titere('Payaso')` da `TypeError: Class constructor Titere cannot be invoked without 'new'`.

**Slime: comas entre métodos.** En una clase no van comas (en un objeto, sí).

### Micro-misión R03-N01-P1 · El primer molde

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván
carta: class | class Titere { constructor(nombre) { this.nombre = nombre; } } · new Titere('Payaso')
recompensa: xp 10, oro 10
```

#### Escena
Hilván le muestra a Nima su mesa de trabajo, llena de cabezas de madera a medio pintar. —Quiero un molde —dice—. Que cada títere salga con su nombre.

#### Gheco sugiere
Una **clase** es un **molde**: dice cómo es y qué sabe hacer una cosa (un títere, un globo), y con él se fabrican todos los que quieras. Cada uno que sale del molde es un **objeto**, con sus propios datos.

El `constructor` es lo que corre **al fabricar** cada uno: recibe los datos y los guarda. Adentro, `this` quiere decir «este objeto que se está fabricando»:

```js
class Globo {
    constructor(color) {
        this.color = color;
    }
}
const rojo = new Globo('rojo');
console.log(rojo.color);   // rojo
```

`this.color = color` guarda el dato que llegó en una propiedad del objeto. Por costumbre, el nombre de una clase empieza con mayúscula.

#### Desafío
Completá el constructor para que cada títere guarde su nombre.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {

  }
}

const payaso = new Titere('Payaso');
const caballito = new Titere('Caballito');
console.log(payaso.nombre, '·', caballito.nombre);
```

#### Salida esperada
```
Payaso · Caballito
```

#### Solución
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
}

const payaso = new Titere('Payaso');
const caballito = new Titere('Caballito');
console.log(payaso.nombre, '·', caballito.nombre);
```

#### Al superarla
De un solo molde de madera salen dos títeres, cada uno con su nombre pintado en la espalda. Hilván los mira, incrédulo. —¿Así de fácil?

#### Imagen
- Un taller de títeres detrás de un teatrito de madera con cortinas rojas, con un molde de madera abierto y dos títeres recién salidos.
- Hilván (titiritero joven y delgado, dedos larguísimos, chaleco de terciopelo violeta abotonado, camisa de mangas largas, hilos dorados enredados en los dedos) sostiene los títeres; Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) mira el molde; Gheco en su hombro.

### Micro-misión R03-N01-P2 · La reverencia

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván
carta: Métodos | adentro de la clase: saludar() { return … this.nombre … } · se llama con obj.saludar()
recompensa: xp 10, oro 10
```

#### Escena
Los títeres ya tienen nombre, pero no saben hacer nada. Hilván quiere que todos sepan hacer la reverencia de entrada.

#### Gheco sugiere
Un **método** es una función que vive adentro de la clase: algo que **sabe hacer** cada objeto. Se escribe sin la palabra `function`, y adentro usa `this` para llegar a los datos de ese objeto:

```js
class Globo {
    constructor(color) { this.color = color; }
    inflar() {
        return `El globo ${this.color} se infla`;
    }
}
console.log(new Globo('azul').inflar());   // El globo azul se infla
```

`return` **devuelve** el texto (no lo muestra): por eso se muestra afuera con `console.log`.

#### Desafío
Agregale a la clase el método `saludar`.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }

  // agregá saludar() acá
}

const payaso = new Titere('Payaso');
const bailarina = new Titere('Bailarina');
console.log(payaso.saludar());
console.log(bailarina.saludar());
```

#### Salida esperada
```
Payaso hace una reverencia
Bailarina hace una reverencia
```

#### Solución
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }

  saludar() {
    return `${this.nombre} hace una reverencia`;
  }
}

const payaso = new Titere('Payaso');
const bailarina = new Titere('Bailarina');
console.log(payaso.saludar());
console.log(bailarina.saludar());
```

#### Al superarla
Los dos títeres se inclinan a la vez, cada uno diciendo su nombre. El público imaginario de Hilván aplaude (es Gheco, solo).

#### Imagen
- Dos títeres de madera sobre el escenario de un teatrito inclinándose en una reverencia, con las cortinas rojas abiertas.
- Gheco solo, en la primera fila de bancos vacíos, aplaudiendo.

### Micro-misión R03-N01-P3 · La energía de cada uno

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván
carta: Estado propio | cada instancia tiene sus datos · un método puede cambiarlos con this.x--
recompensa: xp 10, oro 10
```

#### Escena
Los títeres se cansan: cada uno tiene 2 de energía y cada baile gasta 1. Cuando no tienen más, dicen que están cansados.

#### Gheco sugiere
Cada objeto tiene **sus propios datos**: si uno cambia, los otros no se enteran. Un método puede leer y cambiar los datos de su objeto con `this`:

```js
flotar() {
    if (this.aire === 0) return 'se desinfló';
    this.aire--;
    return 'flota';
}
```

`this.aire--` le resta uno al aire **de ese** globo. Con `return` el método termina ahí: lo que está abajo ya no corre.

#### Desafío
Completá `bailar` para que cada títere gaste **su** energía.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
    this.energia = 2;
  }

  bailar() {

  }
}

const payaso = new Titere('Payaso');
const bailarina = new Titere('Bailarina');
console.log(payaso.bailar());
console.log(payaso.bailar());
console.log(payaso.bailar());
console.log(bailarina.bailar());
```

#### Salida esperada
```
Payaso baila
Payaso baila
Payaso está cansado
Bailarina baila
```

#### Solución
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
    this.energia = 2;
  }

  bailar() {
    if (this.energia === 0) return `${this.nombre} está cansado`;
    this.energia--;
    return `${this.nombre} baila`;
  }
}

const payaso = new Titere('Payaso');
const bailarina = new Titere('Bailarina');
console.log(payaso.bailar());
console.log(payaso.bailar());
console.log(payaso.bailar());
console.log(bailarina.bailar());
```

#### Al superarla
El payaso se desploma en el escenario, agotado; la bailarina sigue fresca. Hilván se ríe: —Igual que los de verdad.

#### Imagen
- Un títere de payaso desparramado y cansado sobre el escenario, y una bailarina de madera en puntas de pie al lado.
- Hilván se ríe con los hilos en las manos; Nima también.

### Micro-misión R03-N01-P4 · El molde sin new

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván
criatura: goblin
carta: new | una clase se usa con new Clase(…) · sin new: Class constructor cannot be invoked without 'new'
recompensa: xp 10, oro 10
```

#### Escena
Un goblin se coló en el taller y escribió la creación del títere sin `new`. El programa explota con un error rojo.

#### Gheco sugiere
A una clase no se la llama como a una función: para fabricar un objeto se pone **`new`** adelante:

```js
const verde = new Globo('verde');
```

Sin `new`, JavaScript se niega y lo dice en el error. Leelo, buscá la línea que crea el títere y fijate qué le falta.

#### Desafío
Arreglá la línea que crea el títere.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
}

const caballito = Titere('Caballito');
console.log(caballito.nombre);
```

#### Salida esperada
```
Caballito
```

#### Solución
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
}

const caballito = new Titere('Caballito');
console.log(caballito.nombre);
```

#### Al superarla
El caballito sale del molde y relincha (o algo parecido: es de madera). El goblin se esconde en el baúl de los disfraces.

#### Imagen
- Un baúl de disfraces abierto en el taller de títeres, con un goblin chiquito (sin armas, chaleco a rayas) asomando la cabeza.
- Un caballito de madera recién hecho; Nima lo sostiene.

### Micro-misión R03-N01-P5 · La compañía entera

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván
carta: Instancias en un arreglo | const lista = nombres.map((n) => new Titere(n)) · después, recorrer y llamar métodos
recompensa: xp 15, monedas 5
```

#### Escena
Hilván quiere armar toda la compañía de una vez: tiene la lista de nombres y quiere un títere por cada uno, todos saludando al público.

#### Gheco sugiere
`map` (de R01) transforma cada elemento de un arreglo en otra cosa. Sirve también para fabricar un objeto por cada dato:

```js
const colores = ['rojo', 'azul'];
const globos = colores.map((c) => new Globo(c));
```

`globos` queda con dos objetos `Globo`. Después se recorre con `for…of` y a cada uno se le pide su método.

#### Desafío
Creá la compañía y que cada títere salude.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }

  saludar() {
    return `${this.nombre} hace una reverencia`;
  }
}

const nombres = ['Payaso', 'Bailarina', 'Caballito', 'Dragoncito'];
const compania = ___;

```

#### Salida esperada
```
Payaso hace una reverencia
Bailarina hace una reverencia
Caballito hace una reverencia
Dragoncito hace una reverencia
```

#### Solución
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }

  saludar() {
    return `${this.nombre} hace una reverencia`;
  }
}

const nombres = ['Payaso', 'Bailarina', 'Caballito', 'Dragoncito'];
const compania = nombres.map((nombre) => new Titere(nombre));

for (const titere of compania) {
  console.log(titere.saludar());
}
```

#### Al superarla
Cuatro títeres en fila sobre el escenario, haciendo la reverencia uno detrás del otro. Hilván ya no tarda una semana: tarda un renglón.

#### Imagen
- Cuatro títeres de madera en fila sobre el escenario (un payaso, una bailarina, un caballito y un dragoncito), con luces de candilejas.
- Hilván, emocionado, maneja los hilos de los cuatro a la vez.

### Micro-misión R03-N01-P6 · La función de esta noche

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván, Lumina
carta: Métodos que reciben otros | actuar(compañero) { … this.nombre … compañero.nombre … } · un objeto habla con otro
recompensa: xp 15, monedas 5
```

#### Escena
Lumina viene a ver el ensayo. En la obra, cada títere le pasa una flor al que sigue. Hilván quiere un método `pasarFlor(otro)`.

#### Gheco sugiere
Un método puede recibir **otro objeto** como dato, y usar los datos de los dos: los suyos con `this` y los del otro con el nombre que le pusiste.

```js
chocar(otro) {
    return `${this.color} choca con ${otro.color}`;
}
```

Para que cada uno se relacione con **el que sigue**, conviene el `for` clásico con índice: `arreglo[i]` es el actual y `arreglo[i + 1]` el siguiente. El último no tiene siguiente: fijate hasta dónde tiene que llegar `i`.

#### Desafío
Completá el método y el recorrido: cada títere le pasa la flor al que sigue (el último no se la pasa a nadie).

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }

  pasarFlor(otro) {

  }
}

const compania = ['Payaso', 'Bailarina', 'Caballito'].map((n) => new Titere(n));

for (let i = 0; i < compania.length - 1; i++) {
  console.log(___);
}
```

#### Salida esperada
```
Payaso le pasa la flor a Bailarina
Bailarina le pasa la flor a Caballito
```

#### Solución
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }

  pasarFlor(otro) {
    return `${this.nombre} le pasa la flor a ${otro.nombre}`;
  }
}

const compania = ['Payaso', 'Bailarina', 'Caballito'].map((n) => new Titere(n));

for (let i = 0; i < compania.length - 1; i++) {
  console.log(compania[i].pasarFlor(compania[i + 1]));
}
```

#### Al superarla
La flor de papel viaja de mano de madera en mano de madera hasta el caballito, que se la come. Lumina se ríe por primera vez en toda la noche.

#### Imagen
- Tres títeres en el escenario pasándose una flor de papel amarilla, el último (un caballito) mordiéndola.
- Lumina (luciérnaga enorme, alas de vidrio, luz amarilla en el pecho) mira desde un palco; Hilván maneja los hilos.

## R03-N02 · Lo privado, los getters y lo static

```meta
tipo: tema
padre: R03-N01
precio: 10
criatura: ogre
temas: poo.encapsulamiento, poo.static
```

### Crónica

Los títeres de Hilván tienen un problema: cualquiera que pasa por el teatro les cambia la energía, los hilos o el nombre. Bruno le puso energía 1000 al payaso para que bailara toda la noche, y el payaso se rompió.

—Hay cosas de un títere que no se tocan desde afuera —dice {mentor}—. En JavaScript, lo privado se marca con un **#**. Y si alguien quiere ver o cambiar algo, que pase por una puerta que controle el títere.

### Objetivos

- Proteger datos con campos privados `#campo`.
- Exponer valores con `get` y controlar los cambios con `set`.
- Usar campos y métodos `static`, que son de la clase y no de cada instancia.
- Declarar campos con un valor inicial afuera del constructor.

### Antes de empezar

- R03-N01: clases.

### Explicación

#### Campos privados
```javascript
class Titere {
  #energia = 3;          // privado: solo se usa adentro de la clase

  bailar() {
    this.#energia--;
  }
}
const t = new Titere();
t.#energia = 1000;       // SyntaxError: no se puede ni escribir afuera
```
El `#` es parte del nombre. Lo privado es **de verdad**: desde afuera no se ve ni se cambia.

#### get y set
```javascript
class Titere {
  #energia = 3;
  get energia() {             // se lee como propiedad: t.energia
    return this.#energia;
  }
  set energia(valor) {        // se escribe como propiedad: t.energia = 2
    if (valor < 0 || valor > 5) return;   // controla
    this.#energia = valor;
  }
}
```

#### static
```javascript
class Titere {
  static creados = 0;              // de la clase: uno solo para todos
  constructor() {
    Titere.creados++;
  }
  static deMadera(nombre) {        // se llama con Titere.deMadera('x')
    return new Titere(nombre);
  }
}
```

### Código de ejemplo

```javascript
class Titere {
  static creados = 0;
  #energia = 3;

  constructor(nombre) {
    this.nombre = nombre;
    Titere.creados++;
  }

  get energia() {
    return this.#energia;
  }

  set energia(valor) {
    if (valor < 0 || valor > 5) {
      console.log(`(${valor} no es una energía válida)`);
      return;
    }
    this.#energia = valor;
  }
}

const payaso = new Titere('Payaso');
new Titere('Bailarina');

payaso.energia = 1000;
payaso.energia = 5;
console.log(payaso.nombre, payaso.energia);
console.log('Títeres creados:', Titere.creados);
console.log(payaso);
```

### Salida esperada

```
(1000 no es una energía válida)
Payaso 5
Títeres creados: 2
Titere { nombre: 'Payaso' }
```

### ¿Para qué sirve?

Para que un objeto se cuide solo: que nadie le ponga una vida negativa, un precio con letras o un saldo inventado. Las clases de las bibliotecas que vas a usar esconden sus detalles así, y exponen solo lo que se puede usar.

### Errores habituales

**Slime: usar `#campo` sin declararlo.** `this.#vida = 3` en el constructor, sin `#vida;` arriba, da `Private field '#vida' must be declared in an enclosing class`.

**Ogro: el getter que se llama a sí mismo.** `get energia() { return this.energia; }` se llama sin fin (`Maximum call stack size exceeded`). Adentro, usá el privado: `this.#energia`.

**Esqueleto: llamar lo static desde una instancia.** `payaso.creados` da `undefined`: es `Titere.creados`.

### Micro-misión R03-N02-P1 · Los hilos no se tocan

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván
carta: #privado | #energia = 3; arriba de la clase · this.#energia adentro · desde afuera no se ve
recompensa: xp 10, oro 10
```

#### Escena
Hilván quiere que la energía de los títeres sea **privada**: que solo el títere la cambie cuando baila.

#### Gheco sugiere
Un campo **privado** es un dato que solo puede tocar la propia clase, desde sus métodos. De afuera no se ve ni se cambia. Se marca con `#` adelante y se declara arriba, en el cuerpo de la clase:

```js
class Alcancia {
    #monedas = 0;
    guardar() {
        this.#monedas++;
    }
}
```

El `#` es parte del nombre: se escribe **siempre**, también al usarlo (`this.#monedas`). Cambialo en todos los lugares donde aparece.

#### Desafío
Cambiá `energia` por el campo privado `#energia` en toda la clase.

#### Código inicial
```javascript
class Titere {
  energia = 3;

  constructor(nombre) {
    this.nombre = nombre;
  }

  bailar() {
    this.energia--;
    return `${this.nombre} baila (le queda ${this.energia})`;
  }
}

const payaso = new Titere('Payaso');
console.log(payaso.bailar());
console.log(payaso);
```

#### Salida esperada
```
Payaso baila (le queda 2)
Titere { nombre: 'Payaso' }
```

#### Solución
```javascript
class Titere {
  #energia = 3;

  constructor(nombre) {
    this.nombre = nombre;
  }

  bailar() {
    this.#energia--;
    return `${this.nombre} baila (le queda ${this.#energia})`;
  }
}

const payaso = new Titere('Payaso');
console.log(payaso.bailar());
console.log(payaso);
```

#### Al superarla
La energía desaparece de la etiqueta del payaso: ahora vive adentro, donde nadie la ve. Bruno busca por todos lados cómo cambiarla. No puede.

#### Imagen
- Un títere de payaso con una cajita cerrada con candado dorado en el pecho, de donde salen los hilos.
- Bruno (gorra al revés, chaleco rojo) intenta abrir la cajita sin éxito; Hilván lo mira con los brazos cruzados.

### Micro-misión R03-N02-P2 · La puerta de la energía

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván
carta: get | get energia() { return this.#energia; } · se lee como propiedad: titere.energia
recompensa: xp 10, oro 10
```

#### Escena
Ahora nadie ve la energía, ni siquiera Hilván. Quiere poder **leerla** desde afuera, pero sin que se pueda cambiar.

#### Gheco sugiere
Un **getter** es un método que se lee **como si fuera una propiedad**, sin paréntesis. Sirve para dejar **ver** un dato privado sin dejar cambiarlo:

```js
get monedas() {
    return this.#monedas;
}
// afuera:
console.log(alcancia.monedas);   // sin ()
```

Se escribe con `get` adelante del nombre.

#### Desafío
Agregá el getter `energia`.

#### Código inicial
```javascript
class Titere {
  #energia = 3;

  constructor(nombre) {
    this.nombre = nombre;
  }

  // agregá el getter acá

  bailar() {
    this.#energia--;
  }
}

const payaso = new Titere('Payaso');
payaso.bailar();
console.log('Energía:', payaso.energia);
```

#### Salida esperada
```
Energía: 2
```

#### Solución
```javascript
class Titere {
  #energia = 3;

  constructor(nombre) {
    this.nombre = nombre;
  }

  get energia() {
    return this.#energia;
  }

  bailar() {
    this.#energia--;
  }
}

const payaso = new Titere('Payaso');
payaso.bailar();
console.log('Energía:', payaso.energia);
```

#### Al superarla
Hilván ve la energía de cada títere en un relojito de madera, pero el relojito no tiene perilla: solo se mira.

#### Imagen
- Un relojito de madera con una aguja colgado del cuello de un títere, sin números legibles.
- Hilván lo mira de cerca con una lupa; Gheco espía el relojito.

### Micro-misión R03-N02-P3 · El set que controla

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván, Bruno
carta: set | set energia(v) { if (no vale) return; this.#energia = v; } · se escribe: titere.energia = 2
recompensa: xp 10, oro 10
```

#### Escena
Hilván quiere poder **recargar** la energía de un títere, pero entre 0 y 5. Nada de los 1000 de Bruno.

#### Gheco sugiere
Un **setter** es lo contrario: corre cuando alguien **asigna** con `=`, y recibe el valor nuevo. Así la clase puede **controlar** qué se acepta:

```js
set monedas(valor) {
    if (valor > 100) return;   // no entra
    this.#monedas = valor;
}
// afuera:
alcancia.monedas = 500;   // no hace nada
```

Con `return` se sale sin cambiar nada. `||` quiere decir «o»: alcanza con que se cumpla una de las dos condiciones.

#### Desafío
Agregá el setter con su control.

#### Código inicial
```javascript
class Titere {
  #energia = 3;

  get energia() {
    return this.#energia;
  }

  // agregá el setter acá
}

const payaso = new Titere();
payaso.energia = 1000;
console.log(payaso.energia);
payaso.energia = 5;
console.log(payaso.energia);
payaso.energia = -2;
console.log(payaso.energia);
```

#### Salida esperada
```
3
5
5
```

#### Solución
```javascript
class Titere {
  #energia = 3;

  get energia() {
    return this.#energia;
  }

  set energia(valor) {
    if (valor < 0 || valor > 5) return;
    this.#energia = valor;
  }
}

const payaso = new Titere();
payaso.energia = 1000;
console.log(payaso.energia);
payaso.energia = 5;
console.log(payaso.energia);
payaso.energia = -2;
console.log(payaso.energia);
```

#### Al superarla
Bruno prueba con 1000, con 999, con -1. Nada: el payaso se queda en 5, contento y entero.

#### Imagen
- Un títere de payaso sano y sonriente con una perilla dorada en la espalda que tiene un tope.
- Bruno gira la perilla con fuerza y no pasa nada; Tati se ríe atrás.

### Micro-misión R03-N02-P4 · El ogro del espejo

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco
criatura: ogre
carta: El getter que se llama a sí mismo | get x() { return this.x; } no termina nunca · adentro, usá el privado: this.#x
recompensa: xp 10, oro 10
```

#### Escena
Un ogro escribió un getter para el nombre, y el programa explota: `Cannot set property nombre … which has only a getter`. El constructor quiere guardar el nombre en el mismo lugar que ocupa el getter. Y aunque pudiera, el getter se leería a sí mismo sin fin, como dos espejos enfrentados.

#### Gheco sugiere
Una clase no puede tener **un getter y un dato con el mismo nombre**: `nombre` ya es el getter, así que `this.nombre = nombre` en el constructor quiere guardar en un lugar que solo se puede leer. De ahí el error `which has only a getter` («que solo tiene getter»).

Y hay otra trampa: si el getter `nombre` hace `return this.nombre`, leer `this.nombre` vuelve a ejecutar el getter, que vuelve a leer… sin fin (`Maximum call stack size exceeded`).

La salida para las dos es guardar el dato con **otro nombre**: un campo privado con `#`, que el constructor llena y el getter lee.

`texto.toUpperCase()` devuelve el texto **en mayúsculas**: `'Pipo'.toUpperCase()` da `'PIPO'`.

#### Desafío
Arreglá la clase para que el getter devuelva el nombre sin llamarse a sí mismo.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }

  get nombre() {
    return this.nombre.toUpperCase();
  }
}

console.log(new Titere('Payaso').nombre);
```

#### Salida esperada
```
PAYASO
```

#### Solución
```javascript
class Titere {
  #nombre;

  constructor(nombre) {
    this.#nombre = nombre;
  }

  get nombre() {
    return this.#nombre.toUpperCase();
  }
}

console.log(new Titere('Payaso').nombre);
```

#### Al superarla
El reflejo infinito se corta y el nombre aparece, en mayúsculas, como en un cartel de teatro: *PAYASO*.

#### Imagen
- Dos espejos de camarín enfrentados con un títere reflejado infinitas veces, y uno de los espejos con una grieta que corta el reflejo.
- Un ogro torpe de feria (sin armas) mareado en el medio; Nima lo saca de ahí de un brazo.

### Micro-misión R03-N02-P5 · Cuántos salieron del molde

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván
carta: static | static creados = 0; · es de la clase, uno solo · Titere.creados++ en el constructor
recompensa: xp 15, monedas 5
```

#### Escena
Hilván quiere llevar la cuenta de cuántos títeres salieron del molde desde que lo tiene. La cuenta es del **molde**, no de cada títere.

#### Gheco sugiere
Un campo **`static`** es de la **clase**, no de cada objeto: hay uno solo, compartido. Sirve, por ejemplo, para contar cuántos se fabricaron:

```js
class Globo {
    static vendidos = 0;
    constructor() {
        Globo.vendidos++;
    }
}
```

Se usa con el nombre de la clase adelante (`Globo.vendidos`), no con `this`.

#### Desafío
Contá los títeres creados con un campo `static`.

#### Código inicial
```javascript
class Titere {
  // un contador de la clase

  constructor(nombre) {
    this.nombre = nombre;

  }
}

['Payaso', 'Bailarina', 'Caballito'].forEach((n) => new Titere(n));
console.log('Salieron del molde:', Titere.creados);
```

#### Salida esperada
```
Salieron del molde: 3
```

#### Solución
```javascript
class Titere {
  static creados = 0;

  constructor(nombre) {
    this.nombre = nombre;
    Titere.creados++;
  }
}

['Payaso', 'Bailarina', 'Caballito'].forEach((n) => new Titere(n));
console.log('Salieron del molde:', Titere.creados);
```

#### Al superarla
Hilván talla tres rayitas en el costado del molde. Va a necesitar más espacio.

#### Imagen
- Un molde de madera grande con rayitas talladas en el costado, sobre la mesa de trabajo del titiritero.
- Hilván talla una rayita con una gubia; tres títeres nuevos sentados en fila al lado.

### Micro-misión R03-N02-P6 · La caja de la recaudación

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván, Lumina
carta: Todo junto | #privado para lo que no se toca · get para leer · un método que valida para cambiar · static para lo de todos
recompensa: xp 15, monedas 5
```

#### Escena
Lumina le regala a Hilván una caja para juntar las fichas de las funciones. Tiene que cuidarse sola: que nadie saque más de lo que hay ni ponga fichas negativas, y que se pueda ver el total.

#### Gheco sugiere
Juntá lo del nodo: un campo privado para el dato, un **getter** para verlo y métodos que lo cambian **solo si se puede**.

Un método puede devolver `true` o `false` para avisar si pudo hacer lo que le pidieron:

```js
gastar(n) {
    if (n > this.#saldo) return false;   // no alcanza
    this.#saldo -= n;
    return true;
}
```

`-=` resta y guarda (`a -= 3` es `a = a - 3`).

#### Desafío
Completá la caja.

#### Código inicial
```javascript
class Caja {
  #fichas = 0;

  get total() {

  }

  poner(n) {

  }

  sacar(n) {

  }
}

const caja = new Caja();
caja.poner(10);
caja.poner(-5);
console.log('Total:', caja.total);
console.log('¿Saca 4?', caja.sacar(4));
console.log('¿Saca 20?', caja.sacar(20));
console.log('Total:', caja.total);
```

#### Salida esperada
```
Total: 10
¿Saca 4? true
¿Saca 20? false
Total: 6
```

#### Solución
```javascript
class Caja {
  #fichas = 0;

  get total() {
    return this.#fichas;
  }

  poner(n) {
    if (n > 0) this.#fichas += n;
  }

  sacar(n) {
    if (n > this.#fichas) return false;
    this.#fichas -= n;
    return true;
  }
}

const caja = new Caja();
caja.poner(10);
caja.poner(-5);
console.log('Total:', caja.total);
console.log('¿Saca 4?', caja.sacar(4));
console.log('¿Saca 20?', caja.sacar(20));
console.log('Total:', caja.total);
```

#### Al superarla
La caja se cierra con un clic y se queda en el escritorio de Hilván. Esa noche, por primera vez, las cuentas del teatro cierran.

#### Imagen
- Una caja de madera con herrajes de bronce y una ranura para fichas, sobre el escritorio del titiritero.
- Lumina la entrega; Hilván la recibe con las dos manos.

## R03-N03 · Herencia: extends y super

```meta
tipo: tema
padre: R03-N02
precio: 10
criatura: ogre
temas: poo.herencia
```

### Crónica

Hilván quiere sumar títeres especiales a la compañía: un **dragoncito** que además de saludar escupe chispas, y una **arquera** de madera (idea de Nima, claro) que además de saludar dispara flechas de corcho. No quiere copiar todo el molde de nuevo.

—Un molde puede **heredar** de otro —dice {mentor}—. El dragoncito es un títere, con todo lo que tiene un títere, y algo más.

### Objetivos

- Crear una clase que herede de otra con `extends`.
- Llamar al constructor del padre con `super(…)`.
- Agregar métodos nuevos y **reemplazar** (sobrescribir) los del padre.
- Usar el método del padre desde la hija con `super.metodo()`.

### Antes de empezar

- R03-N01 y R03-N02: clases y campos.

### Explicación

#### extends y super
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
  saludar() {
    return `${this.nombre} hace una reverencia`;
  }
}

class Dragoncito extends Titere {
  constructor(nombre, chispas) {
    super(nombre);            // primero, el constructor del padre
    this.chispas = chispas;
  }
  escupir() {                 // un método nuevo
    return `${this.nombre} escupe ${this.chispas} chispas`;
  }
}
```
- `Dragoncito` tiene todo lo de `Titere` (el `nombre`, `saludar()`) y lo suyo.
- En el constructor de la hija, `super(…)` va **antes** de usar `this`.

#### Sobrescribir
```javascript
class Dragoncito extends Titere {
  saludar() {                                  // reemplaza al del padre
    return `${super.saludar()} y ruge`;        // usa el del padre y agrega
  }
}
```

#### La cadena
```javascript
const d = new Dragoncito('Chispín', 3);
d instanceof Dragoncito;   // true
d instanceof Titere;       // true: un dragoncito también es un títere
```

### Código de ejemplo

```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
  saludar() {
    return `${this.nombre} hace una reverencia`;
  }
}

class Dragoncito extends Titere {
  constructor(nombre, chispas) {
    super(nombre);
    this.chispas = chispas;
  }
  saludar() {
    return `${super.saludar()} y ruge`;
  }
  escupir() {
    return `${this.nombre} escupe ${this.chispas} chispas`;
  }
}

const payaso = new Titere('Payaso');
const chispin = new Dragoncito('Chispín', 3);
console.log(payaso.saludar());
console.log(chispin.saludar());
console.log(chispin.escupir());
console.log(chispin instanceof Titere, payaso instanceof Dragoncito);
console.log(chispin);
```

### Salida esperada

```
Payaso hace una reverencia
Chispín hace una reverencia y ruge
Chispín escupe 3 chispas
true false
Dragoncito { nombre: 'Chispín', chispas: 3 }
```

### ¿Para qué sirve?

Un enemigo común y uno jefe, un usuario y un administrador, un botón y un botón con ícono: cuando algo «es un» otro algo, con cosas de más, la herencia evita copiar código. (Igual, no abuses: muchas veces alcanza con objetos que tienen otros objetos adentro.)

### Errores habituales

**Esqueleto: usar `this` antes de `super`.** `Must call super constructor in derived class before accessing 'this'`.

**Ogro: olvidar `super` en el constructor de la hija.** Si la hija tiene constructor, tiene que llamar a `super(…)`. (Si no tiene constructor, se usa el del padre solo.)

**Ogro: sobrescribir sin querer.** Si la hija tiene un método con el mismo nombre, el del padre ya no se usa (salvo con `super.metodo()`).

### Micro-misión R03-N03-P1 · El dragoncito

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván
carta: extends | class Hija extends Padre { … } · la hija tiene todo lo del padre
recompensa: xp 10, oro 10
```

#### Escena
Hilván talla un dragoncito y quiere que sea un títere más: con nombre y con reverencia, sin escribir todo de nuevo.

#### Gheco sugiere
La **herencia** hace un molde nuevo **a partir de otro**: la clase hija tiene todo lo del padre (sus datos y sus métodos) y después le podés agregar o cambiar cosas. Se escribe con `extends`:

```js
class GloboGigante extends Globo {}
```

Aunque las llaves estén vacías, un `GloboGigante` ya sabe hacer todo lo que sabe un `Globo`.

`objeto instanceof Clase` pregunta si el objeto **se fabricó con ese molde** (o con una hija suya): da `true` o `false`.

#### Desafío
Declará la clase `Dragoncito` que herede de `Titere`.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
  saludar() {
    return `${this.nombre} hace una reverencia`;
  }
}

// declará Dragoncito acá


const chispin = new Dragoncito('Chispín');
console.log(chispin.saludar());
console.log(chispin instanceof Titere);
```

#### Salida esperada
```
Chispín hace una reverencia
true
```

#### Solución
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
  saludar() {
    return `${this.nombre} hace una reverencia`;
  }
}

class Dragoncito extends Titere {}

const chispin = new Dragoncito('Chispín');
console.log(chispin.saludar());
console.log(chispin instanceof Titere);
```

#### Al superarla
Chispín, el dragoncito de madera verde, hace su primera reverencia. La cola le queda un poco torcida.

#### Imagen
- Un títere de dragoncito de madera verde con alitas de tela, haciendo una reverencia en el escenario.
- Hilván le acomoda la cola; Nima y Gheco miran.

### Micro-misión R03-N03-P2 · Las chispas del dragoncito

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván
carta: super | constructor(nombre, chispas) { super(nombre); this.chispas = chispas; } · super va primero
recompensa: xp 10, oro 10
```

#### Escena
El dragoncito necesita algo que los otros títeres no tienen: cuántas chispas escupe.

#### Gheco sugiere
Si la hija necesita **datos propios**, escribe su propio `constructor`. Adentro, lo **primero** es `super(…)`: llama al constructor del padre para que guarde lo suyo. Después, la hija guarda lo nuevo:

```js
class GloboGigante extends Globo {
    constructor(color, metros) {
        super(color);          // el padre guarda el color
        this.metros = metros;  // la hija guarda lo suyo
    }
}
```

Los métodos nuevos se agregan como en cualquier clase.

#### Desafío
Completá el constructor y el método `escupir`.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
}

class Dragoncito extends Titere {
  constructor(nombre, chispas) {

  }

  escupir() {

  }
}

const chispin = new Dragoncito('Chispín', 3);
console.log(chispin.escupir());
```

#### Salida esperada
```
Chispín escupe 3 chispas
```

#### Solución
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
}

class Dragoncito extends Titere {
  constructor(nombre, chispas) {
    super(nombre);
    this.chispas = chispas;
  }

  escupir() {
    return `${this.nombre} escupe ${this.chispas} chispas`;
  }
}

const chispin = new Dragoncito('Chispín', 3);
console.log(chispin.escupir());
```

#### Al superarla
Tres chispas amarillas salen de la boca de madera de Chispín. Hilván, por las dudas, aleja las cortinas.

#### Imagen
- El títere de dragoncito verde escupiendo tres chispitas amarillas en el escenario.
- Hilván corre las cortinas rojas para que no se prendan; Gheco se esconde atrás de Nima.

### Micro-misión R03-N03-P3 · El esqueleto antes de super

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco
criatura: skeleton
carta: super primero | en la hija, this se puede usar recién después de super(…)
recompensa: xp 10, oro 10
```

#### Escena
Hilván hizo la arquera de madera, pero el programa explota: `Must call super constructor in derived class before accessing 'this'`.

#### Gheco sugiere
En el constructor de una hija, `this` **no existe** hasta que se llama a `super(…)`: el objeto lo fabrica el padre. Por eso usar `this` antes de `super` da error.

Leé el mensaje y mirá el orden de las líneas en el constructor.

#### Desafío
Arreglá el constructor de `Arquera`.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
}

class Arquera extends Titere {
  constructor(nombre, flechas) {
    this.flechas = flechas;
    super(nombre);
  }
}

const arquera = new Arquera('Mini Nima', 5);
console.log(arquera.nombre, arquera.flechas);
```

#### Salida esperada
```
Mini Nima 5
```

#### Solución
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
}

class Arquera extends Titere {
  constructor(nombre, flechas) {
    super(nombre);
    this.flechas = flechas;
  }
}

const arquera = new Arquera('Mini Nima', 5);
console.log(arquera.nombre, arquera.flechas);
```

#### Al superarla
La arquera de madera se para en el escenario con su arquito de mimbre. Tiene una trenza de lana negra con un hilo amarillo. Nima se pone colorada.

#### Imagen
- Un títere de madera de arquera con trenza de lana negra atada con un hilo amarillo y un arquito de mimbre, parado en el escenario.
- Nima, colorada, se tapa la cara; Hilván sonríe orgulloso.

### Micro-misión R03-N03-P4 · Cada uno saluda a su manera

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván
carta: Sobrescribir | la hija vuelve a escribir saludar() · super.saludar() usa el del padre
recompensa: xp 10, oro 10
```

#### Escena
Los títeres comunes hacen la reverencia, pero el dragoncito tiene que hacer la reverencia **y rugir**.

#### Gheco sugiere
La hija puede **volver a escribir** un método del padre con el mismo nombre: así cambia lo que hace (eso se llama **sobrescribir**). Y si quiere usar lo que hacía el padre y **agregarle** algo, lo llama con `super.metodo()`:

```js
inflar() {
    return `${super.inflar()} hasta el techo`;
}
```

El texto del padre queda adelante y la hija le agrega lo suyo.

#### Desafío
Sobrescribí `saludar` en el dragoncito usando el del padre.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
  saludar() {
    return `${this.nombre} hace una reverencia`;
  }
}

class Dragoncito extends Titere {
  // sobrescribí saludar
}

console.log(new Titere('Payaso').saludar());
console.log(new Dragoncito('Chispín').saludar());
```

#### Salida esperada
```
Payaso hace una reverencia
Chispín hace una reverencia y ruge
```

#### Solución
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
  saludar() {
    return `${this.nombre} hace una reverencia`;
  }
}

class Dragoncito extends Titere {
  saludar() {
    return `${super.saludar()} y ruge`;
  }
}

console.log(new Titere('Payaso').saludar());
console.log(new Dragoncito('Chispín').saludar());
```

#### Al superarla
—¡Grrr! —ruge Chispín después de la reverencia. Es un rugido de madera, chiquito, pero el público (Gheco) se asusta igual.

#### Imagen
- El dragoncito de madera rugiendo en el escenario con la boca abierta, al lado del payaso haciendo la reverencia.
- Gheco, en la primera fila, saltando del susto.

### Micro-misión R03-N03-P5 · La arquera de madera

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván
carta: Herencia completa | extends · super(…) en el constructor · métodos nuevos · el estado de la hija
recompensa: xp 15, monedas 5
```

#### Escena
La arquera de madera tiene que disparar flechas de corcho: empieza con algunas, y cuando se queda sin, avisa.

#### Gheco sugiere
Ahora va la clase entera: el `extends`, el `constructor` con `super` primero y el método. En el método, revisá primero el caso en que **no se puede** (no quedan flechas) y cortá con `return`; si no, restá y devolvé el texto.

Fijate en la consigna el texto exacto de los dos casos y **cuándo** se resta: el número que se muestra es el que queda después.

#### Desafío
Escribí la clase `Arquera` completa.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
}

// escribí Arquera acá


const mini = new Arquera('Mini Nima', 2);
console.log(mini.disparar());
console.log(mini.disparar());
console.log(mini.disparar());
```

#### Salida esperada
```
Mini Nima dispara (quedan 1)
Mini Nima dispara (quedan 0)
Mini Nima no tiene flechas
```

#### Solución
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
}

class Arquera extends Titere {
  constructor(nombre, flechas) {
    super(nombre);
    this.flechas = flechas;
  }

  disparar() {
    if (this.flechas === 0) return `${this.nombre} no tiene flechas`;
    this.flechas--;
    return `${this.nombre} dispara (quedan ${this.flechas})`;
  }
}

const mini = new Arquera('Mini Nima', 2);
console.log(mini.disparar());
console.log(mini.disparar());
console.log(mini.disparar());
```

#### Al superarla
Dos corchos vuelan por el teatro y uno le pega a Bruno en la gorra. Desde ese día, la arquera de madera es la estrella de la compañía.

#### Imagen
- El títere de arquera de madera disparando un corcho con su arquito, y un corcho volando hacia la gorra de Bruno en el público.
- Bruno (gorra al revés, chaleco rojo) se agarra la gorra; Nima y Hilván se ríen.

### Micro-misión R03-N03-P6 · Tres generaciones

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Hilván, Lumina
carta: Cadena de herencia | C extends B extends A · super.metodo() va subiendo · instanceof es verdad para todos los de arriba
recompensa: xp 15, monedas 5
```

#### Escena
Lumina pide un títere especial para el final de la función: un **dragón mayor**, que es un dragoncito que además vuela. Hilván duda: ¿se puede heredar de algo que ya heredó?

#### Gheco sugiere
La herencia puede tener **varias generaciones**: una clase hereda de otra que a su vez hereda de otra. `super.metodo()` siempre llama al de la clase de **arriba inmediata**, que puede usar el suyo de más arriba:

```js
class A { decir() { return 'a'; } }
class B extends A { decir() { return `${super.decir()}b`; } }
class C extends B { decir() { return `${super.decir()}c`; } }
console.log(new C().decir());   // abc
```

Cada generación agrega su parte a lo que ya traía.

#### Desafío
Escribí `DragonMayor` para que salude con las tres cosas.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
  saludar() {
    return `${this.nombre} hace una reverencia`;
  }
}

class Dragoncito extends Titere {
  saludar() {
    return `${super.saludar()} y ruge`;
  }
}

// escribí DragonMayor acá


const mayor = new DragonMayor('Brasa');
console.log(mayor.saludar());
console.log(mayor instanceof Dragoncito, mayor instanceof Titere);
```

#### Salida esperada
```
Brasa hace una reverencia y ruge y vuela
true true
```

#### Solución
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
  saludar() {
    return `${this.nombre} hace una reverencia`;
  }
}

class Dragoncito extends Titere {
  saludar() {
    return `${super.saludar()} y ruge`;
  }
}

class DragonMayor extends Dragoncito {
  saludar() {
    return `${super.saludar()} y vuela`;
  }
}

const mayor = new DragonMayor('Brasa');
console.log(mayor.saludar());
console.log(mayor instanceof Dragoncito, mayor instanceof Titere);
```

#### Al superarla
Brasa, el dragón mayor, hace la reverencia, ruge y levanta vuelo colgado de seis hilos a la vez. Lumina vuela a su lado durante toda la escena final.

#### Imagen
- Un gran títere de dragón rojo de madera y tela volando sobre el escenario colgado de muchos hilos dorados.
- Lumina (luciérnaga enorme, alas de vidrio) vuela al lado; Hilván, arriba en la pasarela, maneja los hilos con las dos manos.

## R03-N04 · Polimorfismo: cada títere a su manera

```meta
tipo: tema
padre: R03-N03
precio: 10
criatura: ogre
temas: poo.polimorfismo, poo.abstractas
```

### Crónica

Llega la noche del estreno. Hilván tiene una compañía mezclada: payasos, bailarinas, dragoncitos y la arquera. Su guion dice solamente *«todos actúan»*, una y otra vez, y él no quiere preguntar a cada rato qué tipo de títere es cada uno para saber qué hacer.

—No preguntes qué es —dice {mentor}—. Pedile a cada uno que **actúe**, y que cada uno lo haga a su manera. Esa es la gracia de los moldes.

### Objetivos

- Recorrer objetos de clases distintas y llamar al mismo método en todos (**polimorfismo**).
- Escribir una clase «abstracta»: un molde que no se usa solo, con un método que cada hija tiene que escribir.
- Usar `instanceof` cuando de verdad hace falta saber la clase.
- Darle a una clase su propio `toString()`.

### Antes de empezar

- R03-N03: herencia.

### Explicación

#### El mismo pedido, distintas respuestas
```javascript
const compania = [new Payaso('Pipo'), new Bailarina('Lola'), new Dragoncito('Chispín')];
for (const titere of compania) {
  console.log(titere.actuar());   // cada clase tiene su propio actuar()
}
```
El código de afuera no sabe ni le importa qué títere es cada uno: solo sabe que todos tienen `actuar()`.

#### Un molde que no se usa solo
JavaScript no tiene `abstract`, pero se simula:
```javascript
class Titere {
  constructor(nombre) {
    if (new.target === Titere) throw new Error('Titere es un molde: usá una de sus hijas');
    this.nombre = nombre;
  }
  actuar() {
    throw new Error(`${this.constructor.name} tiene que escribir actuar()`);
  }
}
```
- `new.target` es la clase que se usó con `new`.
- Si una hija se olvida de escribir `actuar()`, el error lo dice.

#### instanceof y toString
```javascript
if (titere instanceof Dragoncito) { … }   // solo cuando hace falta algo especial
class Titere {
  toString() { return `Títere ${this.nombre}`; }
}
`${payaso}`;   // usa toString(): 'Títere Pipo'
```

### Código de ejemplo

```javascript
class Titere {
  constructor(nombre) {
    if (new.target === Titere) throw new Error('Titere es un molde');
    this.nombre = nombre;
  }
  actuar() {
    throw new Error(`${this.constructor.name} tiene que escribir actuar()`);
  }
  toString() {
    return `${this.constructor.name} ${this.nombre}`;
  }
}

class Payaso extends Titere {
  actuar() { return 'se cae y se levanta'; }
}
class Bailarina extends Titere {
  actuar() { return 'gira en puntas de pie'; }
}
class Dragoncito extends Titere {
  actuar() { return 'escupe chispas'; }
}

const compania = [new Payaso('Pipo'), new Bailarina('Lola'), new Dragoncito('Chispín')];
for (const titere of compania) {
  console.log(`${titere}: ${titere.actuar()}`);
}

try {
  new Titere('Nadie');
} catch (error) {
  console.log('No se puede:', error.message);
}
```

### Salida esperada

```
Payaso Pipo: se cae y se levanta
Bailarina Lola: gira en puntas de pie
Dragoncito Chispín: escupe chispas
No se puede: Titere es un molde
```

### ¿Para qué sirve?

En un juego, todos los enemigos «se mueven», cada uno a su manera; en una tienda, todos los medios de pago «cobran»; en un editor, todas las herramientas «dibujan». Con polimorfismo, el código principal no se llena de `if` que preguntan qué es cada cosa.

### Errores habituales

**Ogro: llenarse de `if (x instanceof …)`.** Si el código pregunta la clase de cada uno para decidir qué hacer, ese comportamiento tendría que estar **en** cada clase.

**Ogro: la hija que se olvida del método.** Sin el error del molde, usa el del padre y hace cualquier cosa sin avisar.

**Esqueleto: el nombre del método distinto en una hija.** Si una clase escribe `actua()` en vez de `actuar()`, llamar a `actuar()` usa el del padre (o da `is not a function`).

### Micro-misión R03-N04-P1 · Todos actúan

```meta
lugar: El escenario del estreno
personajes: Nima, Gheco, Hilván
carta: Polimorfismo | la misma llamada, titere.actuar(), hace algo distinto según la clase de cada uno
recompensa: xp 10, oro 10
```

#### Escena
Hilván ya tiene las clases de su compañía, cada una con su `actuar()`. Falta el guion: recorrer la compañía y que cada uno actúe.

#### Gheco sugiere
**Polimorfismo** quiere decir «muchas formas»: objetos de clases distintas que tienen un método **con el mismo nombre**, y cada uno lo hace a su manera.

La gracia es que el que los usa no necesita preguntar qué es cada uno: le pide lo mismo a todos y cada uno responde lo suyo.

```js
for (const animal of granja) {
    console.log(animal.hablar());   // muu, beee, guau…
}
```

No hace falta ningún `if` para saber de qué clase es.

#### Desafío
Hacé que actúe toda la compañía.

#### Código inicial
```javascript
class Payaso {
  constructor(nombre) { this.nombre = nombre; }
  actuar() { return `${this.nombre} se cae y se levanta`; }
}
class Bailarina {
  constructor(nombre) { this.nombre = nombre; }
  actuar() { return `${this.nombre} gira en puntas de pie`; }
}

const compania = [new Payaso('Pipo'), new Bailarina('Lola'), new Payaso('Pepa')];

```

#### Salida esperada
```
Pipo se cae y se levanta
Lola gira en puntas de pie
Pepa se cae y se levanta
```

#### Solución
```javascript
class Payaso {
  constructor(nombre) { this.nombre = nombre; }
  actuar() { return `${this.nombre} se cae y se levanta`; }
}
class Bailarina {
  constructor(nombre) { this.nombre = nombre; }
  actuar() { return `${this.nombre} gira en puntas de pie`; }
}

const compania = [new Payaso('Pipo'), new Bailarina('Lola'), new Payaso('Pepa')];

for (const titere of compania) {
  console.log(titere.actuar());
}
```

#### Al superarla
Se abre el telón y la compañía actúa en fila, cada uno con su número. Hilván no mueve un dedo de más.

#### Imagen
- Un teatrito de títeres con el telón rojo abierto y tres títeres actuando a la vez: dos payasos y una bailarina.
- Hilván, detrás, con los hilos de los tres en una sola mano.

### Micro-misión R03-N04-P2 · El dragoncito se suma

```meta
lugar: El escenario del estreno
personajes: Nima, Gheco, Hilván
carta: Sumar una clase | una clase nueva con su actuar() · el recorrido no cambia
recompensa: xp 10, oro 10
```

#### Escena
Chispín, el dragoncito, quiere entrar en la obra. Hilván tiene miedo de tener que cambiar todo el guion.

#### Gheco sugiere
Esa es la ventaja del polimorfismo: para sumar un personaje nuevo, alcanza con escribir su clase con **el mismo método**. El recorrido que los hace actuar **no se toca**.

Escribí la clase nueva con su constructor y su método, y agregá el objeto al arreglo (al final, como pide la consigna).

#### Desafío
Agregá la clase `Dragoncito` y sumá a Chispín al final de la compañía.

#### Código inicial
```javascript
class Payaso {
  constructor(nombre) { this.nombre = nombre; }
  actuar() { return `${this.nombre} se cae y se levanta`; }
}

// escribí Dragoncito acá

const compania = [new Payaso('Pipo')];

for (const titere of compania) {
  console.log(titere.actuar());
}
```

#### Salida esperada
```
Pipo se cae y se levanta
Chispín escupe chispas
```

#### Solución
```javascript
class Payaso {
  constructor(nombre) { this.nombre = nombre; }
  actuar() { return `${this.nombre} se cae y se levanta`; }
}

class Dragoncito {
  constructor(nombre) { this.nombre = nombre; }
  actuar() { return `${this.nombre} escupe chispas`; }
}

const compania = [new Payaso('Pipo'), new Dragoncito('Chispín')];

for (const titere of compania) {
  console.log(titere.actuar());
}
```

#### Al superarla
Chispín entra en escena, escupe sus chispas y el público imaginario enloquece. El guion de Hilván no cambió ni una coma.

#### Imagen
- El dragoncito verde de madera escupiendo chispas amarillas al lado de un payaso en el escenario del teatrito.
- Hilván, sorprendido, mira el guion en sus manos (un papel sin texto legible).

### Micro-misión R03-N04-P3 · El molde que no se usa solo

```meta
lugar: El escenario del estreno
personajes: Nima, Gheco, Hilván
carta: Clase abstracta | if (new.target === Titere) throw new Error(…) · el molde solo sirve para heredar
recompensa: xp 10, oro 10
```

#### Escena
Bruno sacó del depósito un títere **sin nada**: sin cara, sin ropa, solo el molde. Lo mandó a escena y el público no entendió nada.

#### Gheco sugiere
Algunos moldes son solo **de base**: no tiene sentido fabricar uno «genérico», solo sus hijas. Para impedirlo, el constructor puede revisar **con qué clase** lo llamaron: `new.target` es la clase que se usó en el `new`.

```js
constructor() {
    if (new.target === Figura) throw new Error('Usá una figura concreta');
}
```

`throw` **lanza** un error y corta. Si el `new` fue de una hija, `new.target` es la hija y sigue de largo.

El `try`/`catch` (R02) atrapa el error que lanza el `throw`, y `error.message` es **el texto** que le pusiste en `new Error('…')`.

#### Desafío
Hacé que `new Titere(…)` tire el error y que las hijas sigan andando.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {

    this.nombre = nombre;
  }
}

class Payaso extends Titere {}

console.log(new Payaso('Pipo').nombre);
try {
  new Titere('Nadie');
  console.log('Salió un títere vacío');
} catch (error) {
  console.log('No se puede:', error.message);
}
```

#### Salida esperada
```
Pipo
No se puede: Titere es un molde
```

#### Solución
```javascript
class Titere {
  constructor(nombre) {
    if (new.target === Titere) throw new Error('Titere es un molde');
    this.nombre = nombre;
  }
}

class Payaso extends Titere {}

console.log(new Payaso('Pipo').nombre);
try {
  new Titere('Nadie');
  console.log('Salió un títere vacío');
} catch (error) {
  console.log('No se puede:', error.message);
}
```

#### Al superarla
El molde vuelve al depósito con un cartel: *no sale a escena*. Bruno lo mira con cariño: le parecía simpático.

#### Imagen
- Un molde de títere de madera lisa, sin cara ni ropa, en un estante del depósito con un cartelito colgado (sin texto legible).
- Bruno (gorra al revés, chaleco rojo) lo acaricia; Hilván cierra la puerta del depósito.

### Micro-misión R03-N04-P4 · La hija olvidadiza

```meta
lugar: El escenario del estreno
personajes: Nima, Gheco, Hilván
criatura: ogre
carta: Método obligatorio | el molde tira un error en actuar() · la hija que no lo escribe, se delata
recompensa: xp 10, oro 10
```

#### Escena
Hilván agregó una `Bailarina`, pero escribió `actua()` en vez de `actuar()`. En escena, la bailarina tira un error rojo. Un ogro aplaude.

#### Gheco sugiere
El molde trae un `actuar()` que lanza un error a propósito: es la forma de exigirle a cada hija que escriba **el suyo**. Si la hija lo escribe con el mismo nombre, el suyo **tapa** al del molde y no hay error.

El error aparece cuando la hija se olvida o lo escribe con **otro nombre**: comparalo letra por letra con el del molde.

#### Desafío
Corregí la bailarina para que actúe.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) { this.nombre = nombre; }
  actuar() {
    throw new Error(`${this.constructor.name} tiene que escribir actuar()`);
  }
}

class Payaso extends Titere {
  actuar() { return `${this.nombre} se cae y se levanta`; }
}
class Bailarina extends Titere {
  actua() { return `${this.nombre} gira en puntas de pie`; }
}

for (const titere of [new Payaso('Pipo'), new Bailarina('Lola')]) {
  console.log(titere.actuar());
}
```

#### Salida esperada
```
Pipo se cae y se levanta
Lola gira en puntas de pie
```

#### Solución
```javascript
class Titere {
  constructor(nombre) { this.nombre = nombre; }
  actuar() {
    throw new Error(`${this.constructor.name} tiene que escribir actuar()`);
  }
}

class Payaso extends Titere {
  actuar() { return `${this.nombre} se cae y se levanta`; }
}
class Bailarina extends Titere {
  actuar() { return `${this.nombre} gira en puntas de pie`; }
}

for (const titere of [new Payaso('Pipo'), new Bailarina('Lola')]) {
  console.log(titere.actuar());
}
```

#### Al superarla
Lola gira en puntas de pie y el ogro deja de aplaudir. Se va, ofendido, a buscar otra obra que arruinar.

#### Imagen
- Una bailarina de madera girando en el escenario con un tutú de tela blanca.
- Un ogro torpe de feria (sin armas, delantal de rayas) se va del teatro con los brazos cruzados; Nima lo mira irse.

### Micro-misión R03-N04-P5 · El cartel de cada uno

```meta
lugar: El escenario del estreno
personajes: Nima, Gheco, Hilván
carta: toString | toString() { return … } · se usa solo en `${obj}` y al unir con textos · this.constructor.name es el nombre de la clase
recompensa: xp 15, monedas 5
```

#### Escena
Para el programa de mano, Hilván quiere que cada títere se presente con su clase y su nombre: *Payaso Pipo*, *Bailarina Lola*.

#### Gheco sugiere
`toString()` es un método especial: JavaScript lo usa solo cuando necesita **convertir un objeto en texto**, por ejemplo adentro de un `${…}`. Si una clase no lo tiene, el objeto se ve como `[object Object]`.

`this.constructor.name` es el **nombre de la clase** del objeto, como texto:

```js
class Globo {
    toString() { return `Soy un ${this.constructor.name}`; }
}
class GloboGigante extends Globo {}
console.log(`${new GloboGigante()}`);   // Soy un GloboGigante
```

Se escribe una vez en el padre y cada hija dice su propio nombre.

#### Desafío
Agregá el `toString` para que el programa de mano salga bien.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) { this.nombre = nombre; }
}
class Payaso extends Titere {}
class Bailarina extends Titere {}

const compania = [new Payaso('Pipo'), new Bailarina('Lola')];
console.log(`Programa: ${compania.join(' y ')}`);
```

#### Salida esperada
```
Programa: Payaso Pipo y Bailarina Lola
```

#### Solución
```javascript
class Titere {
  constructor(nombre) { this.nombre = nombre; }
  toString() {
    return `${this.constructor.name} ${this.nombre}`;
  }
}
class Payaso extends Titere {}
class Bailarina extends Titere {}

const compania = [new Payaso('Pipo'), new Bailarina('Lola')];
console.log(`Programa: ${compania.join(' y ')}`);
```

#### Al superarla
El programa de mano se imprime solo, con cada títere en su renglón. Antes decía *[object Object] y [object Object]*.

#### Imagen
- Un programa de mano de teatro de papel con dibujitos de títeres (sin texto legible), apilado en una mesita de la entrada.
- Tati reparte los programas; gente de feria entra al teatro.

### Micro-misión R03-N04-P6 · El final de la obra

```meta
lugar: El escenario del estreno
personajes: Nima, Gheco, Hilván, Lumina
carta: Polimorfismo e instanceof | todos actúan igual · instanceof solo para el caso especial
recompensa: xp 15, monedas 5
```

#### Escena
En el final, todos actúan, y además **los dragones** hacen una reverencia extra, porque son los únicos que pueden volar hasta el palco de Lumina.

#### Gheco sugiere
A veces sí hace falta saber de qué clase es un objeto, para algo que solo hacen algunos. `instanceof` lo pregunta, y devuelve `true` o `false`:

```js
if (animal instanceof Vaca) {
    console.log('da leche');
}
```

Vale también para las hijas: un `GloboGigante` es `instanceof Globo`. Primero que todos actúen; el agregado va después, solo para los que corresponde.

#### Desafío
Completá el final de la obra.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) { this.nombre = nombre; }
}
class Payaso extends Titere {
  actuar() { return `${this.nombre} se cae y se levanta`; }
}
class Dragoncito extends Titere {
  actuar() { return `${this.nombre} escupe chispas`; }
}

const compania = [new Payaso('Pipo'), new Dragoncito('Chispín'), new Payaso('Pepa'), new Dragoncito('Brasa')];

for (const titere of compania) {

}
```

#### Salida esperada
```
Pipo se cae y se levanta
Chispín escupe chispas
Chispín vuela hasta el palco
Pepa se cae y se levanta
Brasa escupe chispas
Brasa vuela hasta el palco
```

#### Solución
```javascript
class Titere {
  constructor(nombre) { this.nombre = nombre; }
}
class Payaso extends Titere {
  actuar() { return `${this.nombre} se cae y se levanta`; }
}
class Dragoncito extends Titere {
  actuar() { return `${this.nombre} escupe chispas`; }
}

const compania = [new Payaso('Pipo'), new Dragoncito('Chispín'), new Payaso('Pepa'), new Dragoncito('Brasa')];

for (const titere of compania) {
  console.log(titere.actuar());
  if (titere instanceof Dragoncito) {
    console.log(`${titere.nombre} vuela hasta el palco`);
  }
}
```

#### Al superarla
Los dos dragones vuelan hasta el palco y le hacen una reverencia a Lumina. Ella los saluda con la luz del pecho, y el teatro entero se pone amarillo.

#### Imagen
- Dos títeres de dragón (uno verde chico y uno rojo grande) volando hacia un palco iluminado por la luz amarilla de Lumina, sobre un teatrito lleno de gente.
- Abajo, los payasos de madera saludan; Hilván en la pasarela, emocionado.

## R03-N05 · Closures: funciones que recuerdan

```meta
tipo: tema
padre: R03-N04
precio: 10
criatura: troll
temas: func.closures, prog.alcance
```

### Crónica

Entre bastidores, Nima encuentra una cajita de música vieja. Cada vez que le dan cuerda, toca **una nota más** que la vez anterior. Nadie le guarda la cuenta: la cajita **se acuerda** sola. Hilván dice que la hizo el Vidriero.

—Las funciones de JavaScript pueden hacer lo mismo —dice {mentor}—. Una función que nace adentro de otra se lleva consigo lo que había alrededor, y lo recuerda aunque la otra ya haya terminado. Se llama **closure**.

### Objetivos

- Entender el alcance de bloque de `let` y `const`, y el de función de `var`.
- Crear funciones que recuerdan variables (closures): contadores, fábricas de funciones.
- Usar un closure para tener datos privados sin clases.
- Reconocer el error clásico de `var` en un bucle con `setTimeout`.

### Antes de empezar

- R01-N07: funciones.

### Explicación

#### Alcance
```javascript
if (true) {
  let adentro = 1;
}
console.log(adentro);   // ReferenceError: let y const viven solo en su bloque { }
```
`var` (el viejo) ignora los bloques: vive en toda la función. Por eso se usa `let`.

#### Un closure
```javascript
function crearCajita() {
  let notas = 0;              // queda guardado
  return () => {
    notas++;
    return `Suena ${notas} nota(s)`;
  };
}
const cajita = crearCajita();
cajita();   // 'Suena 1 nota(s)'
cajita();   // 'Suena 2 nota(s)'
```
`crearCajita` ya terminó, pero la flecha que devolvió **se acuerda** de `notas`. Nadie más puede tocar `notas`: es privada.

#### Fábricas de funciones
```javascript
const multiplicarPor = (n) => (x) => x * n;
const doble = multiplicarPor(2);
const triple = multiplicarPor(3);
```

#### El troll de var
```javascript
for (var i = 1; i <= 3; i++) {
  setTimeout(() => console.log(i), 100);   // 4, 4, 4: hay un solo i para todas las vueltas
}
for (let j = 1; j <= 3; j++) {
  setTimeout(() => console.log(j), 100);   // 1, 2, 3: un j nuevo en cada vuelta
}
```

### Código de ejemplo

```javascript
function crearCajita(nombre) {
  let notas = 0;
  return () => {
    notas++;
    return `${nombre}: ${'♪'.repeat(notas)}`;
  };
}

const cajita = crearCajita('Cajita del Vidriero');
console.log(cajita());
console.log(cajita());
const otra = crearCajita('Cajita nueva');
console.log(otra());
console.log(cajita());

const multiplicarPor = (n) => (x) => x * n;
const doble = multiplicarPor(2);
console.log(doble(5), multiplicarPor(10)(3));

for (var i = 1; i <= 3; i++) setTimeout(() => console.log('var:', i), 10);
for (let j = 1; j <= 3; j++) setTimeout(() => console.log('let:', j), 20);
```

### Salida esperada

```
Cajita del Vidriero: ♪
Cajita del Vidriero: ♪♪
Cajita nueva: ♪
Cajita del Vidriero: ♪♪♪
10 30
var: 4
var: 4
var: 4
let: 1
let: 2
let: 3
```

### ¿Para qué sirve?

Cada vez que pasás una función a un evento, a un `setTimeout` o a un `fetch`, esa función usa variables de afuera: es un closure. Entenderlos explica muchos errores raros (sobre todo con `var`) y permite guardar estado privado sin clases.

### Errores habituales

**Troll: `var` en un bucle con algo que corre después.** Todas las funciones ven el último valor. Usá `let`.

**Esqueleto: usar una variable fuera de su bloque.** `ReferenceError: x is not defined`.

**Ogro: creer que cada llamada a la fábrica comparte el estado.** Cada vez que llamás a `crearCajita()` nace un `notas` **nuevo**.

### Micro-misión R03-N05-P1 · La cajita que recuerda

```meta
lugar: Entre bastidores
personajes: Nima, Gheco, Hilván
carta: Closure | una función devuelve otra · la de adentro recuerda las variables de la de afuera
recompensa: xp 10, oro 10
```

#### Escena
Nima quiere hacer una cajita como la del Vidriero: cada vez que le dan cuerda, suma una vuelta.

#### Gheco sugiere
Una función puede **devolver otra función**. Y la de adentro **recuerda** las variables de la de afuera, aunque la de afuera ya haya terminado. Eso se llama **closure** (*clausura*): la función se lleva su «mochila» de variables.

```js
function crearMarcador() {
    let goles = 0;
    return () => {
        goles++;
        return goles;
    };
}
const marcador = crearMarcador();
console.log(marcador());   // 1
console.log(marcador());   // 2
```

`goles` no se ve desde afuera: solo la flecha devuelta puede tocarla.

#### Desafío
Completá `crearCajita`.

#### Código inicial
```javascript
function crearCajita() {

}

const cajita = crearCajita();
console.log(cajita());
console.log(cajita());
console.log(cajita());
```

#### Salida esperada
```
Vuelta 1
Vuelta 2
Vuelta 3
```

#### Solución
```javascript
function crearCajita() {
  let vueltas = 0;
  return () => {
    vueltas++;
    return `Vuelta ${vueltas}`;
  };
}

const cajita = crearCajita();
console.log(cajita());
console.log(cajita());
console.log(cajita());
```

#### Al superarla
La cajita de Nima toca una nota, después dos, después tres. Hilván la escucha con los ojos cerrados. —Igual a la del Vidriero.

#### Imagen
- Una cajita de música de madera con una manivela y un cilindro dorado, abierta entre bastidores de un teatro.
- Nima le da cuerda; Hilván escucha con los ojos cerrados; Gheco baila arriba de la tapa.

### Micro-misión R03-N05-P2 · Dos cajitas

```meta
lugar: Entre bastidores
personajes: Nima, Gheco
carta: Cada closure, lo suyo | cada vez que llamás a la fábrica nace un estado nuevo
recompensa: xp 10, oro 10
```

#### Escena
Hilván quiere dos cajitas, una para cada lado del escenario. ¿Se van a pisar la cuenta?

#### Gheco sugiere
Cada llamada a la función de afuera crea **variables nuevas**. Así, cada función devuelta tiene **su propia** mochila, y no comparte la cuenta con las otras:

```js
const local = crearMarcador();
const visitante = crearMarcador();
local();       // 1
visitante();   // 1 (su cuenta es aparte)
```

Fijate el orden de los resultados de la consigna para saber cuántas veces llamar a cada una.

#### Desafío
Mostrá que cada cajita lleva su cuenta: `Vuelta 1`, `Vuelta 2`, `Vuelta 1`, `Vuelta 3`.

#### Código inicial
```javascript
function crearCajita() {
  let vueltas = 0;
  return () => {
    vueltas++;
    return `Vuelta ${vueltas}`;
  };
}

const izquierda = ___;
const derecha = ___;
console.log(izquierda());
console.log(izquierda());
console.log(derecha());
console.log(izquierda());
```

#### Salida esperada
```
Vuelta 1
Vuelta 2
Vuelta 1
Vuelta 3
```

#### Solución
```javascript
function crearCajita() {
  let vueltas = 0;
  return () => {
    vueltas++;
    return `Vuelta ${vueltas}`;
  };
}

const izquierda = crearCajita();
const derecha = crearCajita();
console.log(izquierda());
console.log(izquierda());
console.log(derecha());
console.log(izquierda());
```

#### Al superarla
Las dos cajitas tocan cada una su canción, sin mezclarse. El público oye un dúo.

#### Imagen
- Dos cajitas de música iguales a cada lado de un escenario de títeres, cada una con notas musicales de distinto color saliendo.
- Hilván en el medio, dirigiendo con una batuta.

### Micro-misión R03-N05-P3 · La fábrica de precios

```meta
lugar: Entre bastidores
personajes: Nima, Gheco, Hilván
carta: Fábrica de funciones | const conRecargo = (pct) => (precio) => precio + precio * pct / 100
recompensa: xp 10, oro 10
```

#### Escena
Las entradas del teatro tienen recargos distintos según el día: 10% los sábados, 50% en el estreno.

#### Gheco sugiere
Con un closure se arman **fábricas de funciones**: le das un dato y te devuelve una función ya preparada con ese dato.

```js
const multiplicarPor = (n) => (x) => x * n;
const doble = multiplicarPor(2);
console.log(doble(7));   // 14
```

Son dos flechas seguidas: la primera recibe `n` y devuelve la segunda, que recibe `x` y recuerda `n`. Pensá qué cuenta da un recargo de un porcentaje: el precio, más el precio por el porcentaje dividido 100.

#### Desafío
Escribí `conRecargo` para que las dos entradas den 11 y 15.

#### Código inicial
```javascript
const conRecargo = ___;

const sabado = conRecargo(10);
const estreno = conRecargo(50);
console.log('Sábado:', sabado(10));
console.log('Estreno:', estreno(10));
```

#### Salida esperada
```
Sábado: 11
Estreno: 15
```

#### Solución
```javascript
const conRecargo = (pct) => (precio) => precio + (precio * pct) / 100;

const sabado = conRecargo(10);
const estreno = conRecargo(50);
console.log('Sábado:', sabado(10));
console.log('Estreno:', estreno(10));
```

#### Al superarla
Tati pega en la boletería del teatro las dos tarifas. Nadie protesta: el estreno es el estreno.

#### Imagen
- La boletería chiquita del teatro de títeres con dos carteles de precios (sin números legibles).
- Tati (dos colitas, delantal amarillo) los pega con cinta; Hilván controla.

### Micro-misión R03-N05-P4 · El troll del var

```meta
lugar: Entre bastidores
personajes: Nima, Gheco
criatura: troll
carta: var y let | var: una sola variable para todo el bucle · let: una nueva en cada vuelta · importa con lo que corre después
recompensa: xp 10, oro 10
```

#### Escena
Hilván programó que cada títere salga a escena con un segundo de diferencia: el 1, el 2 y el 3. Pero salen tres títeres que dicen todos *4*. Un troll se ríe en el foso.

#### Gheco sugiere
`var` es la forma vieja de crear variables, y tiene una trampa: en un bucle, **hay una sola** variable para todas las vueltas. Las funciones que se ejecutan después (con `setTimeout`) ven todas la misma, con el valor del final.

Con `let` se crea **una variable nueva por vuelta**, y cada función recuerda la suya. Por eso, hoy se usan `let` y `const`, nunca `var`.

#### Desafío
Arreglá el bucle para que salgan el 1, el 2 y el 3.

#### Código inicial
```javascript
for (var i = 1; i <= 3; i++) {
  setTimeout(() => console.log(`Sale el títere ${i}`), i * 1000);
}
```

#### Salida esperada
```
Sale el títere 1
Sale el títere 2
Sale el títere 3
```

#### Solución
```javascript
for (let i = 1; i <= 3; i++) {
  setTimeout(() => console.log(`Sale el títere ${i}`), i * 1000);
}
```

#### Al superarla
Uno, dos, tres: los títeres salen en orden, con un segundo justo entre uno y otro. El troll del foso se queda sin chiste.

#### Imagen
- Tres títeres saliendo a escena uno detrás del otro, con números de madera colgados del cuello (sin números legibles).
- Un troll chiquito y gruñón (sin armas) asoma del foso de la orquesta con cara de fastidio; Nima lo señala.

### Micro-misión R03-N05-P5 · El secreto sin clases

```meta
lugar: Entre bastidores
personajes: Nima, Gheco, Hilván
carta: Privado con closures | function crear() { let secreto; return { leer() {…}, cambiar(v) {…} }; } · nadie toca el secreto
recompensa: xp 15, monedas 5
```

#### Escena
Hilván guarda el final de la obra en secreto. Quiere un objeto que lo deje **leer** y **cambiar** (con una clave), pero que nadie pueda ver la variable.

#### Gheco sugiere
Un closure puede devolver un **objeto con varios métodos** que comparten la misma variable escondida. Es otra forma de tener un dato privado, sin clases:

```js
function crearCandado(clave) {
    let abierto = false;
    return {
        estado() { return abierto; },
        abrir(intento) { if (intento === clave) abierto = true; },
    };
}
```

Los métodos ven la variable y los datos que recibió la función; nadie de afuera puede cambiarlos directamente.

#### Desafío
Completá `crearSecreto`.

#### Código inicial
```javascript
function crearSecreto(inicial, clave) {

}

const guion = crearSecreto('El dragón se va volando', 'hilos');
console.log(guion.leer());
guion.cambiar('El payaso gana', 'adivino');
console.log(guion.leer());
guion.cambiar('Todos bailan', 'hilos');
console.log(guion.leer());
console.log(guion.final);
```

#### Salida esperada
```
El dragón se va volando
El dragón se va volando
Todos bailan
undefined
```

#### Solución
```javascript
function crearSecreto(inicial, clave) {
  let final = inicial;
  return {
    leer() {
      return final;
    },
    cambiar(nuevo, intento) {
      if (intento === clave) final = nuevo;
    },
  };
}

const guion = crearSecreto('El dragón se va volando', 'hilos');
console.log(guion.leer());
guion.cambiar('El payaso gana', 'adivino');
console.log(guion.leer());
guion.cambiar('Todos bailan', 'hilos');
console.log(guion.leer());
console.log(guion.final);
```

#### Al superarla
El final de la obra queda guardado donde nadie lo ve. Bruno pregunta tres veces cómo termina. Nadie le dice.

#### Imagen
- Un guion de teatro atado con un hilo dorado y un nudo, adentro de un cofrecito de bastidores.
- Hilván se lleva un dedo a los labios; Bruno (gorra al revés) intenta espiar.

### Micro-misión R03-N05-P6 · El contador de aplausos

```meta
lugar: Entre bastidores
personajes: Nima, Gheco, Hilván, Lumina
carta: Closures y eventos | cada botón con su función · la función recuerda su propio contador
recompensa: xp 15, monedas 5
```

#### Escena
Lumina quiere medir qué títere aplauden más. Cada botón de la página tiene que contar **sus** aplausos.

#### Gheco sugiere
Los closures sirven mucho con eventos: si una función recibe un elemento, crea su variable y le pone un `addEventListener`, cada elemento queda con **su propia cuenta**.

```js
function contarToques(tecla) {
    let toques = 0;
    tecla.addEventListener('click', () => {
        toques++;
        tecla.textContent = toques;
    });
}
```

Después se llama a la función una vez por cada botón (con `for…of`, o con `forEach`, que hace lo mismo).

#### Desafío
Cada botón cuenta sus aplausos. (La comprobación aplaude dos veces a Pipo y una a Lola.)

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #2a0e14; color: #f5f0e0; padding: 24px; }
  button { font-size: 18px; margin: 4px; padding: 8px 16px; }
</style>
<button class="aplauso" data-nombre="Pipo">Pipo</button>
<button class="aplauso" data-nombre="Lola">Lola</button>
<button class="aplauso" data-nombre="Chispín">Chispín</button>
```

#### Eventos
```
click [data-nombre=Pipo]
click [data-nombre=Pipo]
click [data-nombre=Lola]
```

#### Estado
```
.aplauso
```

#### Código inicial
```javascript
function contarAplausos(boton) {

}

document.querySelectorAll('.aplauso').forEach(contarAplausos);
```

#### Salida esperada
```
── Estado ──
.aplauso: Pipo: 2
.aplauso: Lola: 1
.aplauso: Chispín
```

#### Solución
```javascript
function contarAplausos(boton) {
  let aplausos = 0;
  boton.addEventListener('click', () => {
    aplausos++;
    boton.textContent = `${boton.dataset.nombre}: ${aplausos}`;
  });
}

document.querySelectorAll('.aplauso').forEach(contarAplausos);
```

#### Al superarla
Pipo gana por un aplauso. Lumina se los anota en el ala, con luz. —Las cosas que se recuerdan solas —dice— son las que mejor funcionan.

#### Imagen
- Tres botones de bronce grandes en el borde del escenario, cada uno con un títere pintado, y manos del público aplaudiendo.
- Lumina (luciérnaga enorme, alas de vidrio) anota con luz en su ala; Hilván festeja con Pipo, el payaso.

## R03-N06 · Módulos: import y export

```meta
tipo: tema
padre: R03-N05
precio: 10
criatura: skeleton
temas: js.modulos, prog.modulos
```

### Crónica

El taller de Hilván es un caos: los moldes, los hilos, las pinturas y los guiones están todos en una sola mesa enorme. Cuando busca algo, tarda horas.

—Un programa grande no se escribe en un solo archivo —dice {mentor}—. Se separa en **módulos**: cada archivo con lo suyo, y cada uno dice qué **exporta** para que los demás lo **importen**.

### Objetivos

- Exportar con `export` (con nombre) y `export default` (el principal).
- Importar con `import { … } from './archivo.js'`, con un nombre default y con `* as`.
- Renombrar al importar con `as`.
- Saber que cada módulo tiene su propio alcance y corre una sola vez.

### Antes de empezar

- R03-N01 a R03-N05: clases y closures.

### Explicación

#### Exportar
```javascript
// hilos.js
export const LARGO = 30;
export function atar(titere) { … }
export default class Titere { … }   // uno solo por archivo
```

#### Importar
```javascript
// main.js
import Titere, { LARGO, atar } from './hilos.js';   // el default, y los con nombre entre llaves
import { atar as anudar } from './hilos.js';         // con otro nombre
import * as hilos from './hilos.js';                 // todo junto: hilos.LARGO, hilos.atar
```
- La ruta empieza con `./` y lleva `.js`.
- Lo que no se exporta queda **privado** del archivo.
- En el navegador, el archivo principal se carga con `<script type="module" src="main.js">`. En Node, con la extensión `.mjs` o `"type": "module"` en el `package.json`.

> **En la plataforma.** Las micro-misiones de este nodo traen otros archivos (arriba de la Salida, en «otro archivo»). Tu código es el principal y los importa con `./nombre.js`.

### Código de ejemplo

Este ejemplo es un solo archivo: los módulos los vas a usar en las micro-misiones, que traen sus otros archivos. Muestra cómo se ve cada parte:

```javascript
// Así se vería hilos.js:
//   export const LARGO = 30;
//   export function atar(nombre) { return `${nombre} queda atado con ${LARGO} cm de hilo`; }
//   export default class Titere { constructor(n) { this.nombre = n; } }
//
// Y main.js:
//   import Titere, { atar } from './hilos.js';

const LARGO = 30;
function atar(nombre) {
  return `${nombre} queda atado con ${LARGO} cm de hilo`;
}
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
}

const pipo = new Titere('Pipo');
console.log(atar(pipo.nombre));
```

### Salida esperada

```
Pipo queda atado con 30 cm de hilo
```

### ¿Para qué sirve?

Todo proyecto real de JavaScript está hecho de módulos: los tuyos y los de las bibliotecas que instalás con npm. React, Vue, los juegos en canvas y Node usan `import` y `export` en cada archivo.

### Errores habituales

**Esqueleto: importar algo que no se exporta.** `The requested module './hilos.js' does not provide an export named 'atr'`. Revisá el nombre (y que tenga `export`).

**Esqueleto: la ruta sin `./` o sin `.js`.** `import { atar } from 'hilos'` busca un paquete, no tu archivo.

**Ogro: llaves de más o de menos.** El default se importa **sin** llaves; los con nombre, **con** llaves.

### Micro-misión R03-N06-P1 · El cajón de los hilos

```meta
lugar: El taller ordenado
personajes: Nima, Gheco, Hilván
carta: import con nombre | import { atar } from './hilos.js' · la ruta con ./ y .js
recompensa: xp 10, oro 10
```

#### Escena
Hilván puso todo lo de los hilos en un cajón aparte: `hilos.js`. Ahora quiere usar `atar` desde el escenario.

#### Gheco sugiere
Un programa grande se reparte en **módulos**: archivos separados, cada uno con lo suyo. Un archivo **exporta** lo que quiere compartir (`export`), y otro lo **importa** para usarlo:

```js
import { sumar } from './cuentas.js';
console.log(sumar(2, 3));
```

- entre llaves va el **nombre exacto** de lo que el otro archivo exporta;
- después de `from`, el archivo, entre comillas y con `./` adelante (quiere decir «en esta misma carpeta»).

Los archivos de esta micro-misión están arriba de la Salida: abrilos para ver qué exportan.

#### Desafío
Importá `atar` y usala con los dos títeres.

#### Archivos
hilos.js
```javascript
export function atar(nombre) {
  return `${nombre} queda atado`;
}
```

#### Código inicial
```javascript
// importá atar acá

console.log(atar('Pipo'));
console.log(atar('Lola'));
```

#### Salida esperada
```
Pipo queda atado
Lola queda atado
```

#### Solución
```javascript
import { atar } from './hilos.js';

console.log(atar('Pipo'));
console.log(atar('Lola'));
```

#### Al superarla
Del cajón de los hilos sale justo lo que hacía falta, sin revolver nada más. Hilván suspira de alivio.

#### Imagen
- Un mueble de taller con cajones etiquetados con dibujos (un ovillo, un pincel, una cabeza de madera), uno abierto con hilos dorados.
- Hilván saca un ovillo; Nima sostiene un títere para atar.

### Micro-misión R03-N06-P2 · El molde principal

```meta
lugar: El taller ordenado
personajes: Nima, Gheco, Hilván
carta: export default | import Titere from './titere.js' · sin llaves · uno solo por archivo
recompensa: xp 10, oro 10
```

#### Escena
El molde de los títeres está en `titere.js`, exportado como **lo principal** del archivo.

#### Gheco sugiere
Un archivo puede tener **una** exportación principal, marcada con `export default`. Esa se importa **sin llaves**, y le podés poner el nombre que quieras:

```js
import Globo from './globo.js';
```

Las otras (las que se exportan con `export` a secas) van con llaves y con su nombre exacto.

#### Desafío
Importá la clase y creá a Chispín.

#### Archivos
titere.js
```javascript
export default class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
  saludar() {
    return `${this.nombre} hace una reverencia`;
  }
}
```

#### Código inicial
```javascript
// importá el molde

const chispin = new Titere('Chispín');
console.log(chispin.saludar());
```

#### Salida esperada
```
Chispín hace una reverencia
```

#### Solución
```javascript
import Titere from './titere.js';

const chispin = new Titere('Chispín');
console.log(chispin.saludar());
```

#### Al superarla
El molde principal sale de su estante y Chispín sale del molde. El taller ya no parece un depósito.

#### Imagen
- El molde de madera grande sobre un estante propio, con una luz encima, en un taller ordenado.
- Chispín, el dragoncito verde, sale del molde; Hilván aplaude.

### Micro-misión R03-N06-P3 · Exportar lo tuyo

```meta
lugar: El taller ordenado
personajes: Nima, Gheco, Hilván
carta: export | export const / export function · el otro archivo lo importa con ese nombre
recompensa: xp 10, oro 10
```

#### Escena
La boletería del teatro quedó repartida en dos cajones: `precios.js` sabe cuánto cuesta la entrada, y `boleteria.js` cobra (y para eso, importa el precio del otro cajón). `precios.js` también guarda un secreto que no exporta.

#### Gheco sugiere
Solo se puede importar lo que el otro archivo **exporta**: lo que no tiene `export` queda privado del archivo, y nadie de afuera lo ve.

Si necesitás cosas de dos archivos, va un `import` por cada uno:

```js
import { IVA } from './impuestos.js';
import { facturar } from './caja.js';
```

Abrí cada archivo y fijate qué exporta.

#### Desafío
Importá `PRECIO` de `precios.js` y `cobrar` de `boleteria.js`, y cobrá 3 entradas.

#### Archivos
precios.js
```javascript
export const PRECIO = 4;
const SECRETO = 'no se exporta';
```

boleteria.js
```javascript
import { PRECIO } from './precios.js';

export function cobrar(cantidad) {
  return `${cantidad} entradas: ${cantidad * PRECIO} fichas`;
}
```

#### Código inicial
```javascript
// importá PRECIO y cobrar

console.log('Precio:', PRECIO);
console.log(cobrar(3));
```

#### Salida esperada
```
Precio: 4
3 entradas: 12 fichas
```

#### Solución
```javascript
import { PRECIO } from './precios.js';
import { cobrar } from './boleteria.js';

console.log('Precio:', PRECIO);
console.log(cobrar(3));
```

#### Al superarla
Los dos cajones trabajan juntos: uno sabe el precio, el otro cobra. Y el secreto de `precios.js` sigue siendo secreto.

#### Imagen
- Dos cajones de madera conectados por un hilo dorado, uno con fichas y otro con entradas de papel.
- Tati cobra en la boletería del teatro; Hilván controla.

### Micro-misión R03-N06-P4 · El esqueleto del import

```meta
lugar: El taller ordenado
personajes: Nima, Gheco
criatura: skeleton
carta: Nombres exactos | lo que importás con { } tiene que llamarse igual que lo exportado · si no: does not provide an export named
recompensa: xp 10, oro 10
```

#### Escena
Un esqueleto cambió una letra del import y ahora el programa no arranca: `does not provide an export named 'pintr'`.

#### Gheco sugiere
Si importás con llaves un nombre que el archivo **no exporta**, aparece un error que dice que ese nombre no existe en el módulo.

El nombre entre llaves tiene que ser **idéntico** al del `export`, con mayúsculas y todo. Abrí el archivo y compará.

#### Desafío
Arreglá el import.

#### Archivos
pinturas.js
```javascript
export function pintar(titere, color) {
  return `${titere} queda ${color}`;
}
```

#### Código inicial
```javascript
import { pintr } from './pinturas.js';

console.log(pintr('Pipo', 'rojo'));
```

#### Salida esperada
```
Pipo queda rojo
```

#### Solución
```javascript
import { pintar } from './pinturas.js';

console.log(pintar('Pipo', 'rojo'));
```

#### Al superarla
Pipo queda rojo, como corresponde. El esqueleto se lleva el pincel equivocado.

#### Imagen
- Un estante de frascos de pintura de colores en el taller de títeres, y un payaso de madera recién pintado de rojo.
- Un esqueleto chiquito de feria (sin armas, moño de papel) se va con un pincel seco.

### Micro-misión R03-N06-P5 · Todo el cajón

```meta
lugar: El taller ordenado
personajes: Nima, Gheco, Hilván
carta: import * as | import * as hilos from './hilos.js' · hilos.atar, hilos.LARGO · as también renombra uno
recompensa: xp 15, monedas 5
```

#### Escena
Hilván quiere usar todo lo del cajón de hilos, y además tiene una función propia que también se llama `atar`. No quiere que se peleen los nombres.

#### Gheco sugiere
`import * as nombre from '…'` trae **todo** lo que exporta un archivo, junto, bajo un solo nombre. Después se usa cada cosa con un punto:

```js
import * as cuentas from './cuentas.js';
cuentas.sumar(2, 3);
cuentas.PI;
```

Sirve también para que no choquen nombres: si tu archivo ya tiene una función `sumar`, la importada es `cuentas.sumar` y las dos conviven.

#### Desafío
Importá todo `hilos.js` como `hilos` y mostrá las dos formas de atar.

#### Archivos
hilos.js
```javascript
export const LARGO = 30;
export function atar(nombre) {
  return `${nombre} queda atado con ${LARGO} cm`;
}
```

#### Código inicial
```javascript
// importá todo el cajón como hilos

function atar(nombre) {
  return `${nombre} queda atado con un moño`;
}

console.log(hilos.atar('Pipo'));
console.log(atar('Lola'));
console.log('Largo:', hilos.LARGO);
```

#### Salida esperada
```
Pipo queda atado con 30 cm
Lola queda atado con un moño
Largo: 30
```

#### Solución
```javascript
import * as hilos from './hilos.js';

function atar(nombre) {
  return `${nombre} queda atado con un moño`;
}

console.log(hilos.atar('Pipo'));
console.log(atar('Lola'));
console.log('Largo:', hilos.LARGO);
```

#### Al superarla
Dos formas de atar, sin pelearse: la del cajón y la de Hilván. Lola queda con un moño enorme.

#### Imagen
- Un títere de bailarina con un moño enorme en la cabeza, al lado de un payaso atado con hilos dorados.
- Hilván se ríe del moño; Gheco se enreda en un ovillo.

### Micro-misión R03-N06-P6 · La compañía en módulos

```meta
lugar: El taller ordenado
personajes: Nima, Gheco, Hilván, Lumina
carta: Módulos que se importan entre sí | cada archivo importa lo que necesita · el principal arma todo
recompensa: xp 15, monedas 5
```

#### Escena
Lumina ayuda a Hilván a ordenar la compañía entera: el molde en `titere.js`, cada personaje en su archivo, y el escenario (tu archivo) que arma la función.

#### Gheco sugiere
Un módulo también puede importar de otros: cada archivo importa solo lo que usa. Vos solo tenés que importar las clases que vas a fabricar (fijate si se exportan con `default`, así sabés si van con llaves o sin), armar el arreglo con un objeto de cada una y recorrerlo como en R03-N04.

#### Desafío
Importá `Payaso` y `Dragoncito` y hacé actuar a Pipo y a Chispín.

#### Archivos
titere.js
```javascript
export default class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
}
```

payaso.js
```javascript
import Titere from './titere.js';

export default class Payaso extends Titere {
  actuar() {
    return `${this.nombre} se cae y se levanta`;
  }
}
```

dragoncito.js
```javascript
import Titere from './titere.js';

export default class Dragoncito extends Titere {
  actuar() {
    return `${this.nombre} escupe chispas`;
  }
}
```

#### Código inicial
```javascript
// importá las dos clases

const compania = [new Payaso('Pipo'), new Dragoncito('Chispín')];
for (const titere of compania) {
  console.log(titere.actuar());
}
```

#### Salida esperada
```
Pipo se cae y se levanta
Chispín escupe chispas
```

#### Solución
```javascript
import Payaso from './payaso.js';
import Dragoncito from './dragoncito.js';

const compania = [new Payaso('Pipo'), new Dragoncito('Chispín')];
for (const titere of compania) {
  console.log(titere.actuar());
}
```

#### Al superarla
El taller queda ordenado como una biblioteca: cada títere en su estante, cada cosa en su cajón. Lumina mira los estantes y se queda pensativa. —El taller del Vidriero estaba ordenado igual —dice—. Cada pieza del portal, en su cajón.

#### Imagen
- El taller de títeres perfectamente ordenado, con estantes por personaje y cajones con dibujos, a la luz de un farol.
- Lumina (luciérnaga enorme con alas de vidrio) mira los estantes pensativa; Hilván y Nima chocan las manos.

## R03-N07 · Jefe: el Títere sin Hilos

```meta
tipo: jefe
padre: R03-N06
precio: 10
criatura: dragon
insignia: Hilo de Oro
insignia_descripcion: Venciste al Títere sin Hilos: dominás las clases, los closures, los módulos y el this.
usa: poo.clases, poo.herencia, poo.polimorfismo, func.closures, js.eventos
```

### Crónica

La noche del estreno, uno de los títeres se suelta. Es el **Títere sin Hilos**: un muñeco grande, de madera oscura, que perdió sus hilos y ahora se mueve solo, sin saber quién es. Cuando alguien le pide que actúe, dice *undefined*; cuando suena la campana, se tropieza; cuando lo llaman, no sabe su nombre.

—Perdió su `this` —dice {mentor}—. Lo sacaron de su objeto y lo mandaron a otro lado: a un temporizador, a un botón. Y una función suelta no sabe de quién es. Hay que volver a atarlo.

### Objetivos

- Entender por qué `this` se pierde cuando un método se pasa suelto (a `setTimeout`, a `addEventListener`, a `map`).
- Atarlo de nuevo con una flecha, con `bind` o con un campo flecha en la clase.
- Integrar todo lo de la rama: clases, herencia, polimorfismo, closures y eventos.

### Antes de empezar

- Todos los nodos del Teatro del Titiritero (R03-N01 a R03-N06).

### Explicación

#### Cómo se pierde el this
```javascript
class Titere {
  constructor(nombre) { this.nombre = nombre; }
  actuar() { return `${this?.nombre} actúa`; }
}
const pipo = new Titere('Pipo');
const suelto = pipo.actuar;   // la función, sin su objeto
suelto();                     // this es undefined
```
`this` no es «el objeto donde escribí el método»: es **el objeto que está antes del punto al llamarlo**. Si se llama sin punto (porque lo pasaste a otra función), no hay `this`.

#### Tres formas de atarlo
```javascript
setTimeout(() => pipo.actuar(), 1000);       // 1. una flecha que lo llama con su punto
setTimeout(pipo.actuar.bind(pipo), 1000);    // 2. bind: una copia atada para siempre
class Titere {
  actuar = () => `${this.nombre} actúa`;     // 3. un campo flecha: cada instancia, atada
}
```

### Micro-misión R03-N07-P1 · El títere que no sabe su nombre

```meta
lugar: El escenario del estreno
personajes: Nima, Gheco, el Títere sin Hilos
criatura: ogre
carta: this perdido | pasar obj.metodo suelto pierde el this · () => obj.metodo() lo conserva
recompensa: xp 15, monedas 3
```

#### Escena
Hilván programó que Pipo actúe a los 2 segundos del telón. Pero a los 2 segundos aparece en escena el Títere sin Hilos y dice: *undefined actúa*.

#### Gheco sugiere
Cuando un método se pasa **suelto**, sin el objeto adelante, pierde su `this`: la función viaja sola y ya no sabe de quién es.

```js
setTimeout(globo.inflar, 1000);   // inflar corre sin su globo
```

La salida más simple es envolverlo en una flecha que lo llame **con** su objeto adelante:

```js
setTimeout(() => globo.inflar(), 1000);
```

Así lo que viaja es la flecha, y cuando corre, llama al método como corresponde.

#### Desafío
Que a los 2 segundos se vea `Pipo actúa`.

#### Código inicial
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
  actuar() {
    console.log(`${this?.nombre} actúa`);
  }
}

const pipo = new Titere('Pipo');
setTimeout(pipo.actuar, 2000);
```

#### Salida esperada
```
Pipo actúa
```

#### Solución
```javascript
class Titere {
  constructor(nombre) {
    this.nombre = nombre;
  }
  actuar() {
    console.log(`${this?.nombre} actúa`);
  }
}

const pipo = new Titere('Pipo');
setTimeout(() => pipo.actuar(), 2000);
```

#### Al superarla
A los dos segundos, Pipo sale a escena y se cae (como siempre). El Títere sin Hilos retrocede: algo se le volvió a atar.

#### Imagen
- Un gran títere de madera oscura, sin hilos, con la mirada perdida, en un costado del escenario; en el centro, el payaso Pipo cayéndose.
- Nima, entre bastidores, con un reloj de arena en la mano; Gheco señala al títere oscuro.

### Micro-misión R03-N07-P2 · La campana del telón

```meta
lugar: El escenario del estreno
personajes: Nima, Gheco, Hilván, el Títere sin Hilos
criatura: troll
carta: bind | metodo.bind(obj) devuelve una copia atada a obj · sirve para addEventListener
recompensa: xp 15, monedas 3
```

#### Escena
Cuando tocan la campana del telón, la bailarina tiene que girar y el cartel tiene que decir su nombre. Pero el método se pasó suelto al botón, y el cartel dice *undefined gira*.

#### Gheco sugiere
Otra forma de que un método no pierda su `this` es **atarlo**: `metodo.bind(objeto)` devuelve una copia de la función que **siempre** usa ese objeto como `this`, la llame quien la llame.

```js
const inflarRojo = rojo.inflar.bind(rojo);
boton.addEventListener('click', inflarRojo);
```

Pasa lo mismo con los eventos que con `setTimeout`: el método se pasa suelto.

#### Desafío
Que al tocar la campana el cartel diga `Lola gira`.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #2a0e14; color: #f5f0e0; text-align: center; padding: 24px; }
  #cartel { font-size: 24px; color: #ffd400; }
</style>
<button id="campana">🔔 Campana</button>
<p id="cartel">Telón cerrado</p>
```

#### Eventos
```
click #campana
```

#### Estado
```
#cartel
```

#### Código inicial
```javascript
class Bailarina {
  constructor(nombre) {
    this.nombre = nombre;
  }
  girar() {
    document.querySelector('#cartel').textContent = `${this.nombre} gira`;
  }
}

const lola = new Bailarina('Lola');
document.querySelector('#campana').addEventListener('click', lola.girar);
```

#### Salida esperada
```
── Estado ──
#cartel: Lola gira
```

#### Solución
```javascript
class Bailarina {
  constructor(nombre) {
    this.nombre = nombre;
  }
  girar() {
    document.querySelector('#cartel').textContent = `${this.nombre} gira`;
  }
}

const lola = new Bailarina('Lola');
document.querySelector('#campana').addEventListener('click', lola.girar.bind(lola));
```

#### Al superarla
La campana suena, el telón se abre y Lola gira. El Títere sin Hilos se tapa los oídos y retrocede otro paso.

#### Imagen
- Una campana de bronce colgada al costado de un escenario de títeres, con el telón rojo abriéndose y una bailarina girando.
- Hilván tira de la cuerda de la campana; el títere oscuro sin hilos se tapa los oídos.

### Micro-misión R03-N07-P3 · Volver a atarlo

```meta
lugar: El escenario del estreno
personajes: Nima, Gheco, Hilván, Lumina, el Títere sin Hilos
criatura: dragon
carta: El jefe | clases y herencia · campos flecha atados · closures que cuentan · polimorfismo · eventos
recompensa: xp 30, oro 30, monedas 4
item: Hilo de Oro
```

#### Escena
El Títere sin Hilos se planta en el centro del escenario. Para volver a atarlo, Nima tiene que armar la función entera: la compañía (un molde y sus hijas), un botón por títere que lo hace actuar **con su propio this**, un contador de actuaciones que recuerda solo, y un final en el que todos actúan juntos.

#### Gheco sugiere
Junta todo lo de R03:

- un **campo flecha** (`metodo = () => { … }`, escrito como campo de la clase) queda atado a su objeto: la flecha usa el `this` de donde se creó, aunque viaje suelta;
- las hijas solo cambian el dato que las diferencia;
- el contador es un **closure** como el de R03-N05;
- los botones se arman como en R02 (crear, `data-`, colgar) y cada uno escucha su `click`.

Andá por partes y ejecutá entre medio.

#### Desafío
Completá las hijas, `crearContador` y los botones. La comprobación toca *Pipo*, *Chispín* y después *Final*. Al final:
- el registro tiene `Pipo se cae y se levanta`, `Chispín escupe chispas`, después las dos otra vez (el final), y `Actuaciones: 4`;
- el Títere sin Hilos queda atado.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #2a0e14; color: #f5f0e0; padding: 24px; }
  button { font-size: 16px; margin: 3px; padding: 6px 12px; }
  #registro li { color: #ffd400; }
  #jefe { margin-top: 12px; }
  #jefe.atado { color: #8fe38f; }
</style>
<div id="botones"></div>
<button id="final">Final</button>
<ul id="registro"></ul>
<p id="jefe">El Títere sin Hilos anda suelto</p>
```

#### Eventos
```
click [data-nombre=Pipo]
click [data-nombre=Chispín]
click #final
```

#### Estado
```
#registro li
#jefe
#jefe @class
```

#### Código inicial
```javascript
const registro = document.querySelector('#registro');
const contar = crearContador();

class Titere {
  accion = 'hace algo';
  constructor(nombre) {
    this.nombre = nombre;
  }
  actuar = () => {
    const li = document.createElement('li');
    li.textContent = `${this.nombre} ${this.accion}`;
    registro.append(li);
    return contar();
  };
}

// Payaso: accion 'se cae y se levanta' · Dragoncito: accion 'escupe chispas'


function crearContador() {
  // devolvé una flecha que sume uno y devuelva el total

}

const compania = [new Payaso('Pipo'), new Dragoncito('Chispín')];

// un botón por títere en #botones, con data-nombre, que llame a titere.actuar (suelto)


document.querySelector('#final').addEventListener('click', () => {
  let total = 0;
  for (const titere of compania) total = titere.actuar();
  registro.insertAdjacentHTML('beforeend', `<li>Actuaciones: ${total}</li>`);
  const jefe = document.querySelector('#jefe');
  jefe.textContent = 'El Títere sin Hilos quedó atado';
  jefe.classList.add('atado');
});
```

#### Salida esperada
```
── Estado ──
#registro li: Pipo se cae y se levanta
#registro li: Chispín escupe chispas
#registro li: Pipo se cae y se levanta
#registro li: Chispín escupe chispas
#registro li: Actuaciones: 4
#jefe: El Títere sin Hilos quedó atado
#jefe @class: atado
```

#### Solución
```javascript
const registro = document.querySelector('#registro');
const contar = crearContador();

class Titere {
  accion = 'hace algo';
  constructor(nombre) {
    this.nombre = nombre;
  }
  actuar = () => {
    const li = document.createElement('li');
    li.textContent = `${this.nombre} ${this.accion}`;
    registro.append(li);
    return contar();
  };
}

class Payaso extends Titere {
  accion = 'se cae y se levanta';
}

class Dragoncito extends Titere {
  accion = 'escupe chispas';
}

function crearContador() {
  let total = 0;
  return () => {
    total++;
    return total;
  };
}

const compania = [new Payaso('Pipo'), new Dragoncito('Chispín')];

for (const titere of compania) {
  const boton = document.createElement('button');
  boton.dataset.nombre = titere.nombre;
  boton.textContent = titere.nombre;
  boton.addEventListener('click', titere.actuar);
  document.querySelector('#botones').append(boton);
}

document.querySelector('#final').addEventListener('click', () => {
  let total = 0;
  for (const titere of compania) total = titere.actuar();
  registro.insertAdjacentHTML('beforeend', `<li>Actuaciones: ${total}</li>`);
  const jefe = document.querySelector('#jefe');
  jefe.textContent = 'El Títere sin Hilos quedó atado';
  jefe.classList.add('atado');
});
```

#### Al superarla
Uno por uno, los títeres actúan atados a sí mismos, sin perderse. El Títere sin Hilos los mira desde el centro del escenario… y de a poco se le van atando hilos nuevos, de luz amarilla, que bajan del techo. Cuando el último nudo se cierra, el títere hace una reverencia perfecta y dice, por primera vez, su nombre: *Ébano*. Entre sus manos de madera queda un carretel con un hilo que brilla: **el Hilo de Oro**.

—Se había perdido de sí mismo —dice Hilván—. Como el Vidriero.

{mentor} apaga y prende su luz tres veces sobre el teatro: la señal de que el Teatro ya habla la lengua de la Feria. Al fondo de la Avenida, en el taller del Vidriero, se enciende una segunda ventana.

#### Imagen
- El gran títere de madera oscura haciendo una reverencia en el centro del escenario, con hilos nuevos de luz amarilla bajando del techo y atándolo.
- Nima (trenza negra con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas, arco verde) sostiene un carretel con un hilo dorado brillante; Hilván (chaleco de terciopelo violeta) emocionado a su lado.
- Lumina (luciérnaga enorme con alas de vidrio y luz amarilla en el pecho) sobre el teatro; la compañía de títeres alrededor.
