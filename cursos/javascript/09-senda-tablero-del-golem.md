# RAMA S04 · Senda del Tablero del Gólem: un emulador chiquito en JavaScript

```meta
tipo: senda
posicion: 9
```

## S04-N01 · Las palancas del Gólem

```meta
tipo: tema
padre: R03-N07
precio: 3
moneda: comodin
criatura: goblin
temas: maq.registros, maq.numeracion
usa: poo.clases, poo.encapsulamiento
```

### Crónica

Después de que Ébano recupera sus hilos, el Teatro queda en silencio. Entonces, desde abajo, por las chimeneas que van de la Feria a las Forjas, sube una luz cian que se mete en el escenario y toma forma: una chica que flota, con el pelo dorado moviéndose como en el agua.

—Soy **Nova** —dice—. Vivo adentro de **Axón**, el Gólem de Bronce, debajo de las Forjas. Hace tiempo, una flecha de luz bajó por las chimeneas y me despertó. —Mira el arco de Nima—. Era tuya, ¿no? —Nima se pone colorada—. No vine a quejarme. Vine a pedirte algo: cada vez que pruebo una orden nueva, el Gólem entero se mueve, y si me equivoco, se cae una pared. ¿Me armás un **tablero de práctica**, uno de mentira, en tu lengua? Así pruebo sin romper nada.

### Objetivos

- Representar las palancas del Gólem (los **registros** `AX`, `BX`, `CX`, `DX`) con una clase.
- Mostrar números en **hexadecimal**, con cuatro cifras: `002A`.
- Respetar los 16 bits: un registro va de 0 a 65535 y **da la vuelta** al pasarse.
- Leer y escribir las mitades de un registro (`AH` y `AL`) con operaciones de bits, y avisar con un error si la palanca no existe.

### Antes de empezar

- El Teatro del Titiritero (R03): clases, campos privados y errores.
- Si hiciste el curso de Ensamblador, vas a reconocer el tablero de Nova. Si no, no importa: acá se explica todo lo que hace falta.

### Explicación

#### Las palancas
Adentro del Gólem hay cuatro palancas grandes, los **registros**: `AX`, `BX`, `CX` y `DX`. Cada una guarda un número de **16 bits**: de 0 a 65535.
```javascript
class Tablero {
  constructor() {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
  }
  mov(registro, valor) {
    this.registros[registro] = valor;
  }
}
```

#### En hexadecimal
El tablero del Gólem muestra los números en **base 16** (hexadecimal): las cifras van de `0` a `9` y después de `A` a `F`. Así, 16 bits entran justo en **cuatro** cifras:
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');
hex(42);      // '002A'
hex(65535);   // 'FFFF'
parseInt('2A', 16);   // 42: de vuelta a número
```

#### Dar la vuelta
Si `AX` vale `FFFF` (65535) y se le suma 1, no pasa a 65536: **da la vuelta** a `0000`, como un cuentakilómetros. Con `& 0xFFFF` («y» de bits) nos quedamos con los 16 bits de abajo:
```javascript
(65535 + 1) & 0xFFFF;   // 0
```

#### Las mitades
Cada palanca tiene dos mitades de 8 bits: `AH` (la alta) y `AL` (la baja). Si `AX` es `1234`, `AH` es `12` y `AL` es `34`:
```javascript
const ax = 0x1234;
const ah = ax >> 8;      // 0x12: corre los bits 8 lugares a la derecha
const al = ax & 0xFF;    // 0x34: se queda con los 8 de abajo
```

### Código de ejemplo

```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

console.log(hex(42), hex(255), hex(65535));
console.log(parseInt('FF', 16), 0x2A);
console.log(hex((65535 + 1) & 0xFFFF));
const ax = 0x1234;
console.log(hex(ax >> 8), hex(ax & 0xFF));
```

### Salida esperada

```
002A 00FF FFFF
255 42
0000
0012 0034
```

### ¿Para qué sirve?

Un **emulador** es un programa que hace de otra máquina: así se juega en la compu a las consolas viejas, y así se prueban programas para aparatos que todavía no existen. Los colores de las páginas (`#FFD400`), los permisos de los archivos y las direcciones de memoria se escriben en hexadecimal.

### Errores habituales

**Goblin: el hexadecimal como texto.** `'FF' + 1` da `'FF1'`. Para hacer cuentas, primero `parseInt('FF', 16)`.

**Goblin: olvidarse los 16 bits.** Un registro que llega a 70000 no existe en el Gólem. Siempre `& 0xFFFF`.

**Esqueleto: `ax` en minúsculas.** Las claves del objeto son `AX`, `BX`…: `registros['ax']` es `undefined`.

### Micro-misión S04-N01-P1 · Las cuatro cifras

```meta
lugar: El Teatro del Titiritero, de noche
personajes: Nima, Gheco, Nova
carta: Hexadecimal | n.toString(16).toUpperCase().padStart(4, '0')
recompensa: xp 10, oro 10
```

#### Escena
Nova dibuja en el aire el tablero del Gólem: cuatro palancas con cuatro cifras cada una. —El Gólem cuenta en dieciséis, no en diez. Mi palanca grande vale cuarenta y dos, y en el tablero dice **002A**.

#### Gheco sugiere
Completá `hex(n)`: pasá a base 16, en mayúsculas y con ceros adelante hasta tener cuatro cifras.

#### Desafío
`AX=002A BX=00FF CX=FFFF DX=0000`.

#### Código inicial
```javascript
function hex(n) {
  return String(n);
}

const registros = { AX: 42, BX: 255, CX: 65535, DX: 0 };
console.log(Object.entries(registros).map(([r, v]) => `${r}=${hex(v)}`).join(' '));
```

#### Salida esperada
```
AX=002A BX=00FF CX=FFFF DX=0000
```

#### Solución
```javascript
function hex(n) {
  return n.toString(16).toUpperCase().padStart(4, '0');
}

const registros = { AX: 42, BX: 255, CX: 65535, DX: 0 };
console.log(Object.entries(registros).map(([r, v]) => `${r}=${hex(v)}`).join(' '));
```

#### Al superarla
Las cuatro cifras aparecen en el aire, en cian, como en el pecho del Gólem. Nova aplaude. —¡Así! ¡Así me veo por dentro!

#### Imagen
- Nova (chica de unos 15 años que flota, pelo rubio dorado que se mueve como en el agua, ojos cian brillantes, capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada) dibuja en el aire un tablero de cuatro palancas con cifras de luz cian.
- Nima y Gheco la miran en el escenario vacío del Teatro de títeres.

### Micro-misión S04-N01-P2 · El tablero de práctica

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Nova
carta: La clase | class Tablero { constructor() { this.registros = { AX: 0, … } } mov(r, v) { … } mostrar() { … } }
recompensa: xp 10, oro 10
```

#### Escena
—Una palanca sola no me sirve —dice Nova—. Necesito las cuatro juntas, que se puedan mover y mirar.

#### Gheco sugiere
Completá la clase `Tablero`: `mov(registro, valor)` pone el valor, y `mostrar()` devuelve las cuatro palancas en hexadecimal, separadas por espacios.

#### Desafío
Después de `mov('AX', 5)` y `mov('DX', 4096)`: `AX=0005 BX=0000 CX=0000 DX=1000`.

#### Código inicial
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

class Tablero {
  constructor() {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
  }

  mov(registro, valor) {}

  mostrar() {
    return '';
  }
}

const tablero = new Tablero();
tablero.mov('AX', 5);
tablero.mov('DX', 4096);
console.log(tablero.mostrar());
```

#### Salida esperada
```
AX=0005 BX=0000 CX=0000 DX=1000
```

#### Solución
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

class Tablero {
  constructor() {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
  }

  mov(registro, valor) {
    this.registros[registro] = valor;
  }

  mostrar() {
    return Object.entries(this.registros).map(([r, v]) => `${r}=${hex(v)}`).join(' ');
  }
}

const tablero = new Tablero();
tablero.mov('AX', 5);
tablero.mov('DX', 4096);
console.log(tablero.mostrar());
```

#### Al superarla
Nova mueve la palanca `DX` de mentira y se queda mirando. —Cuatro mil noventa y seis, y en el tablero dice **1000**. Qué número redondo.

#### Imagen
- Un tablero de madera y bronce en miniatura, como un juguete, con cuatro palancas numeradas y cifras de luz cian encima.
- Nova mueve una palanca con un dedo, maravillada.

### Micro-misión S04-N01-P3 · El cuentakilómetros

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Nova, Axón (por la chimenea)
carta: 16 bits | this.registros[r] = (this.registros[r] + valor) & 0xFFFF
recompensa: xp 10, oro 10
```

#### Escena
Desde la chimenea llega la voz grave de **Axón**: *«Yo no adivino. Una palanca llega hasta FFFF. Si se pasa, vuelve a cero.»* Nova prueba en el tablero de práctica: `FFFF + 1`… y la palanca marca `10000`, cinco cifras.

#### Gheco sugiere
Agregale a `Tablero` el método `add(registro, valor)`, que suma y se queda con 16 bits (`& 0xFFFF`). Arreglá también `mov`.

#### Desafío
`AX` en `FFFF` más 1 da `0000`; `BX` en 70000 queda en `1170`.

#### Código inicial
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

class Tablero {
  constructor() {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
  }

  mov(registro, valor) {
    this.registros[registro] = valor;
  }

  add(registro, valor) {
    this.registros[registro] = this.registros[registro] + valor;
  }

  mostrar() {
    return Object.entries(this.registros).map(([r, v]) => `${r}=${hex(v)}`).join(' ');
  }
}

const tablero = new Tablero();
tablero.mov('AX', 0xFFFF);
tablero.add('AX', 1);
tablero.mov('BX', 70000);
tablero.mov('CX', 10);
tablero.add('CX', 5);
console.log(tablero.mostrar());
```

#### Salida esperada
```
AX=0000 BX=1170 CX=000F DX=0000
```

#### Solución
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

class Tablero {
  constructor() {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
  }

  mov(registro, valor) {
    this.registros[registro] = valor & 0xFFFF;
  }

  add(registro, valor) {
    this.registros[registro] = (this.registros[registro] + valor) & 0xFFFF;
  }

  mostrar() {
    return Object.entries(this.registros).map(([r, v]) => `${r}=${hex(v)}`).join(' ');
  }
}

const tablero = new Tablero();
tablero.mov('AX', 0xFFFF);
tablero.add('AX', 1);
tablero.mov('BX', 70000);
tablero.mov('CX', 10);
tablero.add('CX', 5);
console.log(tablero.mostrar());
```

#### Al superarla
`FFFF` más uno, `0000`. La palanca da la vuelta, como la de verdad. Por la chimenea sube un *«Correcto»* seco. Nova sonríe: es lo más parecido a un elogio que dice Axón.

#### Imagen
- Un cuentakilómetros de bronce con cuatro ruedas de cifras que vuelven todas a cero al mismo tiempo.
- Por una chimenea de la Feria asoma un resplandor de bronce y la sombra de un ojo redondo de cristal (Axón, lejos, abajo).

### Micro-misión S04-N01-P4 · Las dos mitades

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Nova
carta: AH y AL | alta: valor >> 8 · baja: valor & 0xFF · juntar: (alta << 8) | baja
recompensa: xp 15, monedas 5
```

#### Escena
—Cada palanca grande tiene dos mitades —explica Nova—: la de arriba y la de abajo. A veces el Gólem mueve una sola. Si `AX` es `1234`, la de arriba, `AH`, es `12`.

#### Gheco sugiere
Completá `leer(nombre)`: con `AX`, `BX`… devuelve el registro entero; con `AH`, `BL`… la mitad (la letra del medio dice cuál palanca, la última, si es `H` o `L`). Completá también `poner(nombre, valor)`, que cambia una mitad sin tocar la otra.

#### Desafío
Con `AX = 1234`: `AH=0012 AL=0034`; después de poner `AL` en `FF`, `AX=12FF`.

#### Código inicial
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

class Tablero {
  constructor() {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
  }

  leer(nombre) {
    return this.registros[nombre];
  }

  poner(nombre, valor) {
    this.registros[nombre] = valor & 0xFFFF;
  }
}

const tablero = new Tablero();
tablero.poner('AX', 0x1234);
console.log(`AH=${hex(tablero.leer('AH'))} AL=${hex(tablero.leer('AL'))}`);
tablero.poner('AL', 0xFF);
console.log(`AX=${hex(tablero.leer('AX'))}`);
```

#### Salida esperada
```
AH=0012 AL=0034
AX=12FF
```

#### Solución
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

class Tablero {
  constructor() {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
  }

  leer(nombre) {
    if (nombre.endsWith('X')) return this.registros[nombre];
    const entero = this.registros[`${nombre[0]}X`];
    return nombre.endsWith('H') ? entero >> 8 : entero & 0xFF;
  }

  poner(nombre, valor) {
    if (nombre.endsWith('X')) {
      this.registros[nombre] = valor & 0xFFFF;
      return;
    }
    const registro = `${nombre[0]}X`;
    const alta = nombre.endsWith('H') ? valor & 0xFF : this.registros[registro] >> 8;
    const baja = nombre.endsWith('L') ? valor & 0xFF : this.registros[registro] & 0xFF;
    this.registros[registro] = (alta << 8) | baja;
  }
}

const tablero = new Tablero();
tablero.poner('AX', 0x1234);
console.log(`AH=${hex(tablero.leer('AH'))} AL=${hex(tablero.leer('AL'))}`);
tablero.poner('AL', 0xFF);
console.log(`AX=${hex(tablero.leer('AX'))}`);
```

#### Al superarla
La mitad de abajo cambia y la de arriba queda quieta. Nova mueve la mitad `AL` de su palanca de verdad, abajo en las Forjas, y en la Feria se oye un *clic* lejano, chiquito.

#### Imagen
- Una palanca de bronce partida en dos mitades que se mueven por separado, cada una con dos cifras de luz cian.
- Nova, concentrada, mueve solo la mitad de abajo.

### Micro-misión S04-N01-P5 · La palanca que no existe

```meta
lugar: El Teatro del Titiritero
personajes: Nima, Gheco, Nova
carta: throw | if (!(nombre in this.registros)) throw new Error(`no hay palanca «${nombre}»`)
recompensa: xp 15, monedas 5
```

#### Escena
Nova se emociona y prueba una palanca que se inventó: `EX`. El tablero de práctica la crea como si nada, y ahora tiene **cinco** palancas. —En el Gólem eso no pasa —dice Nova—. Si pido una palanca que no hay, el Gólem se traba.

#### Gheco sugiere
Que `mov` tire un `Error` con `no hay palanca «EX»` si el registro no es uno de los cuatro. Atrapalo con `try`/`catch` y mostrá `Nova: no hay palanca «EX»`.

#### Desafío
La palanca `BX` se mueve; la `EX` avisa, y el tablero sigue con cuatro.

#### Código inicial
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

class Tablero {
  constructor() {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
  }

  mov(registro, valor) {
    this.registros[registro] = valor & 0xFFFF;
  }

  mostrar() {
    return Object.entries(this.registros).map(([r, v]) => `${r}=${hex(v)}`).join(' ');
  }
}

const tablero = new Tablero();
for (const [registro, valor] of [['BX', 7], ['EX', 3]]) {
  tablero.mov(registro, valor);
}
console.log(tablero.mostrar());
```

#### Salida esperada
```
Nova: no hay palanca «EX»
AX=0000 BX=0007 CX=0000 DX=0000
```

#### Solución
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

class Tablero {
  constructor() {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
  }

  mov(registro, valor) {
    if (!(registro in this.registros)) throw new Error(`no hay palanca «${registro}»`);
    this.registros[registro] = valor & 0xFFFF;
  }

  mostrar() {
    return Object.entries(this.registros).map(([r, v]) => `${r}=${hex(v)}`).join(' ');
  }
}

const tablero = new Tablero();
for (const [registro, valor] of [['BX', 7], ['EX', 3]]) {
  try {
    tablero.mov(registro, valor);
  } catch (error) {
    console.log(`Nova: ${error.message}`);
  }
}
console.log(tablero.mostrar());
```

#### Al superarla
*Nova: no hay palanca «EX».* El tablero sigue con sus cuatro palancas, como el Gólem. —Gracias —dice Nova—. Prefiero que me avise a que invente.

#### Imagen
- Un tablero de cuatro palancas con un hueco vacío donde alguien intentó poner una quinta, y un cartelito de aviso rojo.
- Nova, con la mano en la boca, sonriendo.

## S04-N02 · Las órdenes escritas

```meta
tipo: tema
padre: S04-N01
precio: 10
criatura: slime
temas: maq.registros, prog.cadenas
usa: poo.clases, prog.condicionales
```

### Crónica

Nova no le habla al Gólem moviendo palancas a mano: le **escribe órdenes**, una por renglón, en la lengua del Gólem. `MOV AX, 5`. `ADD AX, BX`. El tablero de práctica todavía no sabe leer.

—Tiene que entender lo que escribo —dice Nova—, como lo entiende Axón. Si escribo `mov ax,5` en minúsculas y sin espacio, también.

### Objetivos

- Desarmar una orden escrita (`MOV AX, 5`) en sus partes con `split` y una expresión regular.
- Saber si un operando es un registro, un número decimal o uno hexadecimal (`0Fh`).
- Ejecutar órdenes con un `switch`: `MOV`, `ADD`, `SUB`, `INC` y `DEC`.
- Correr un programa entero (con comentarios y renglones vacíos) y avisar los errores con su número de línea.

### Antes de empezar

- S04-N01 (las palancas).

### Explicación

#### Desarmar una orden
```javascript
const renglon = '  mov ax,5  ; la palanca grande';
const sinComentario = renglon.split(';')[0].trim();          // 'mov ax,5'
const [op, destino, fuente] = sinComentario.toUpperCase().split(/[\s,]+/);
// op = 'MOV', destino = 'AX', fuente = '5'
```
`/[\s,]+/` corta donde haya uno o más espacios **o** comas, así `mov ax,5` y `MOV AX, 5` dan lo mismo.

#### ¿Qué es cada operando?
| Escrito | Es | Vale |
|---|---|---|
| `BX` | un registro | lo que tenga `BX` |
| `25` | un número decimal | 25 |
| `0FH` | un número hexadecimal (termina en `H`) | 15 |

```javascript
if (operando in registros) return registros[operando];
if (/^[0-9A-F]+H$/.test(operando)) return parseInt(operando.slice(0, -1), 16);
```

#### Un `switch` por orden
```javascript
switch (op) {
  case 'MOV': poner(destino, valor(fuente)); break;
  case 'ADD': poner(destino, registros[destino] + valor(fuente)); break;
  case 'INC': poner(destino, registros[destino] + 1); break;
  default: throw new Error(`no conozco «${op}»`);
}
```

#### El número de línea
Los errores del tablero, como los de cualquier lenguaje, dicen **en qué renglón** están: así se encuentran. Se cuenta desde 1 (el renglón 0 no existe para las personas).

### Código de ejemplo

```javascript
for (const renglon of ['MOV AX, 5', '  mov bx,0Fh ; quince', 'inc   cx', '; solo un comentario']) {
  const limpio = renglon.split(';')[0].trim();
  if (limpio === '') {
    console.log('(renglón vacío)');
    continue;
  }
  const [op, destino, fuente] = limpio.toUpperCase().split(/[\s,]+/);
  console.log({ op, destino, fuente });
}
console.log(parseInt('0F', 16), /^[0-9A-F]+H$/.test('0FH'), /^[0-9A-F]+H$/.test('AX'));
```

### Salida esperada

```
{ op: 'MOV', destino: 'AX', fuente: '5' }
{ op: 'MOV', destino: 'BX', fuente: '0FH' }
{ op: 'INC', destino: 'CX', fuente: undefined }
(renglón vacío)
15 true false
```

### ¿Para qué sirve?

Leer un texto y entender sus partes es lo que hace todo lenguaje de programación con tu código: JavaScript, Python y el ensamblador del Gólem empiezan igual, cortando el texto en pedazos. También lo hacen las calculadoras, los comandos de un juego y los archivos de configuración.

### Errores habituales

**Slime: el `break` olvidado.** Sin `break`, el `switch` sigue ejecutando el `case` de abajo: un `MOV` termina haciendo también un `ADD`.

**Goblin: `'5'` que no es `5`.** Lo que sale de `split` es texto. Hay que convertirlo antes de sumar.

**Ogro: contar las líneas desde 0.** El error dice «línea 2» y el problema está en la 3.

### Micro-misión S04-N02-P1 · Desarmar la orden

```meta
lugar: Las chimeneas entre la Feria y las Forjas
personajes: Nima, Gheco, Nova
carta: split | renglon.split(';')[0].trim().toUpperCase().split(/[\s,]+/)
recompensa: xp 10, oro 10
```

#### Escena
Nova escribe tres órdenes en la pared de la chimenea, con hollín, cada una de una forma distinta. El tablero tiene que entender las tres igual.

#### Gheco sugiere
Completá `desarmar(renglon)`: sacá el comentario, los espacios de los costados y pasá a mayúsculas. Cortá en `op`, `destino` y `fuente`, y devolvé un objeto con esas tres claves.

#### Desafío
Las tres órdenes, desarmadas.

#### Código inicial
```javascript
function desarmar(renglon) {
  const [op, destino, fuente] = renglon.split(' ');
  return { op, destino, fuente };
}

for (const renglon of ['MOV AX, 5', 'add bx,ax', '  sub   cx , 2   ; dos menos']) {
  console.log(desarmar(renglon));
}
```

#### Salida esperada
```
{ op: 'MOV', destino: 'AX', fuente: '5' }
{ op: 'ADD', destino: 'BX', fuente: 'AX' }
{ op: 'SUB', destino: 'CX', fuente: '2' }
```

#### Solución
```javascript
function desarmar(renglon) {
  const limpio = renglon.split(';')[0].trim().toUpperCase();
  const [op, destino, fuente] = limpio.split(/[\s,]+/);
  return { op, destino, fuente };
}

for (const renglon of ['MOV AX, 5', 'add bx,ax', '  sub   cx , 2   ; dos menos']) {
  console.log(desarmar(renglon));
}
```

#### Al superarla
Las tres órdenes quedan en sus tres partes, prolijas. Nova las lee en voz alta, como si fueran poesía. —*Mov. A equis. Cinco.*

#### Imagen
- La pared de ladrillo de una chimenea con tres órdenes escritas en hollín, cada una con distinta letra, y cada orden partida en tres piezas de luz cian.
- Nova, flotando, lee en voz alta; Nima sostiene un farol.

### Micro-misión S04-N02-P2 · ¿Registro o número?

```meta
lugar: Las chimeneas
personajes: Nima, Gheco, Nova
carta: valor() | in registros → su valor · /^[0-9A-F]+H$/ → parseInt(…, 16) · /^\d+$/ → Number
recompensa: xp 10, oro 10
```

#### Escena
—Cuando escribo `ADD AX, BX` —explica Nova—, quiero sumar **lo que tiene** `BX`. Pero cuando escribo `ADD AX, 10h`, quiero sumar dieciséis. Y si escribo `ADD AX, BANANA`, el Gólem me mira raro.

#### Gheco sugiere
Completá `valor(operando, registros)`: si es un registro, su valor; si termina en `H`, hexadecimal; si son solo dígitos, decimal; si no, tirá un `Error` con `no entiendo «BANANA»`.

#### Desafío
Los cuatro operandos.

#### Código inicial
```javascript
const registros = { AX: 3, BX: 40, CX: 0, DX: 0 };

function valor(operando, registros) {
  return Number(operando);
}

for (const operando of ['BX', '10H', '25', 'BANANA']) {
  try {
    console.log(`${operando} → ${valor(operando, registros)}`);
  } catch (error) {
    console.log(`${operando} → ${error.message}`);
  }
}
```

#### Salida esperada
```
BX → 40
10H → 16
25 → 25
BANANA → no entiendo «BANANA»
```

#### Solución
```javascript
const registros = { AX: 3, BX: 40, CX: 0, DX: 0 };

function valor(operando, registros) {
  if (operando in registros) return registros[operando];
  if (/^[0-9A-F]+H$/.test(operando)) return parseInt(operando.slice(0, -1), 16);
  if (/^\d+$/.test(operando)) return Number(operando);
  throw new Error(`no entiendo «${operando}»`);
}

for (const operando of ['BX', '10H', '25', 'BANANA']) {
  try {
    console.log(`${operando} → ${valor(operando, registros)}`);
  } catch (error) {
    console.log(`${operando} → ${error.message}`);
  }
}
```

#### Al superarla
`BX` vale 40, `10H` vale 16, `25` vale 25, y `BANANA` no se entiende. Gheco se ríe tanto que se cae del farol.

#### Imagen
- Cuatro carteles de madera colgados en la chimenea: uno con una palanca, uno con cifras hexadecimales, uno con cifras comunes y uno con una banana dibujada tachada.
- Gheco cae de un farol, muerto de risa.

### Micro-misión S04-N02-P3 · Las cinco órdenes

```meta
lugar: Las chimeneas
personajes: Nima, Gheco, Nova
carta: switch | case 'MOV': … break; case 'ADD': … break; case 'INC': … break; …
recompensa: xp 10, oro 10
```

#### Escena
Ya entiende las partes. Ahora tiene que **hacer** lo que dicen: las cinco órdenes que Nova aprendió primero.

#### Gheco sugiere
Completá `ejecutar(renglon)` con un `switch` sobre `op`: `MOV` pone, `ADD` suma, `SUB` resta, `INC` suma uno y `DEC` resta uno. Siempre con 16 bits.

#### Desafío
Después de las seis órdenes: `AX=0007 BX=0003 CX=FFFF DX=0010`.

#### Código inicial
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');
const registros = { AX: 0, BX: 0, CX: 0, DX: 0 };

function desarmar(renglon) {
  const [op, destino, fuente] = renglon.split(';')[0].trim().toUpperCase().split(/[\s,]+/);
  return { op, destino, fuente };
}

function valor(operando) {
  if (operando in registros) return registros[operando];
  if (/^[0-9A-F]+H$/.test(operando)) return parseInt(operando.slice(0, -1), 16);
  return Number(operando);
}

function poner(registro, n) {
  registros[registro] = n & 0xFFFF;
}

function ejecutar(renglon) {
  const { op, destino, fuente } = desarmar(renglon);
  switch (op) {
    case 'MOV':
      poner(destino, valor(fuente));
  }
}

for (const renglon of ['MOV AX, 5', 'MOV BX, 3', 'ADD AX, 2', 'DEC CX', 'MOV DX, 10h', 'SUB AX, 0']) ejecutar(renglon);
console.log(Object.entries(registros).map(([r, v]) => `${r}=${hex(v)}`).join(' '));
```

#### Salida esperada
```
AX=0007 BX=0003 CX=FFFF DX=0010
```

#### Solución
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');
const registros = { AX: 0, BX: 0, CX: 0, DX: 0 };

function desarmar(renglon) {
  const [op, destino, fuente] = renglon.split(';')[0].trim().toUpperCase().split(/[\s,]+/);
  return { op, destino, fuente };
}

function valor(operando) {
  if (operando in registros) return registros[operando];
  if (/^[0-9A-F]+H$/.test(operando)) return parseInt(operando.slice(0, -1), 16);
  return Number(operando);
}

function poner(registro, n) {
  registros[registro] = n & 0xFFFF;
}

function ejecutar(renglon) {
  const { op, destino, fuente } = desarmar(renglon);
  switch (op) {
    case 'MOV':
      poner(destino, valor(fuente));
      break;
    case 'ADD':
      poner(destino, registros[destino] + valor(fuente));
      break;
    case 'SUB':
      poner(destino, registros[destino] - valor(fuente));
      break;
    case 'INC':
      poner(destino, registros[destino] + 1);
      break;
    case 'DEC':
      poner(destino, registros[destino] - 1);
      break;
  }
}

for (const renglon of ['MOV AX, 5', 'MOV BX, 3', 'ADD AX, 2', 'DEC CX', 'MOV DX, 10h', 'SUB AX, 0']) ejecutar(renglon);
console.log(Object.entries(registros).map(([r, v]) => `${r}=${hex(v)}`).join(' '));
```

#### Al superarla
`DEC CX` con `CX` en cero da `FFFF`: la palanca dio la vuelta para atrás. Nova abre los ojos grandes. —¡Eso me pasó la primera semana! Creí que me había roto.

#### Imagen
- Cinco engranajes de bronce con las palabras de las órdenes talladas, girando en una cadena, uno detrás del otro.
- Nova, sorprendida, señala una palanca que dio la vuelta.

### Micro-misión S04-N02-P4 · El primer programa

```meta
lugar: Las chimeneas
personajes: Nima, Gheco, Nova
carta: Programa | texto.split('\n') · saltear vacíos y comentarios · ejecutar cada renglón
recompensa: xp 15, monedas 5
```

#### Escena
Nova escribe su primer **programa**: varios renglones, con comentarios para acordarse qué hace cada uno, y renglones vacíos para que respire.

#### Gheco sugiere
Completá `correr(programa)`: cortá el texto en renglones, salteá los vacíos y los que son solo comentario, y ejecutá los demás. Contá cuántas órdenes se ejecutaron.

#### Desafío
`4 órdenes · AX=000A BX=0005 CX=0000 DX=0000`.

#### Código inicial
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');
const registros = { AX: 0, BX: 0, CX: 0, DX: 0 };

function ejecutar(renglon) {
  const [op, destino, fuente] = renglon.split(';')[0].trim().toUpperCase().split(/[\s,]+/);
  const valor = (o) => (o in registros ? registros[o] : Number(o));
  switch (op) {
    case 'MOV': registros[destino] = valor(fuente) & 0xFFFF; break;
    case 'ADD': registros[destino] = (registros[destino] + valor(fuente)) & 0xFFFF; break;
    default: throw new Error(`no conozco «${op}»`);
  }
}

function correr(programa) {
  let ordenes = 0;
  for (const renglon of programa.split('\n')) {
    ejecutar(renglon);
    ordenes++;
  }
  return ordenes;
}

const programa = `
; mi primer programa
MOV BX, 5     ; la palanca chica

MOV AX, BX
ADD AX, BX    ; el doble
ADD CX, 0
`;
const ordenes = correr(programa);
console.log(`${ordenes} órdenes · ${Object.entries(registros).map(([r, v]) => `${r}=${hex(v)}`).join(' ')}`);
```

#### Salida esperada
```
4 órdenes · AX=000A BX=0005 CX=0000 DX=0000
```

#### Solución
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');
const registros = { AX: 0, BX: 0, CX: 0, DX: 0 };

function ejecutar(renglon) {
  const [op, destino, fuente] = renglon.split(';')[0].trim().toUpperCase().split(/[\s,]+/);
  const valor = (o) => (o in registros ? registros[o] : Number(o));
  switch (op) {
    case 'MOV': registros[destino] = valor(fuente) & 0xFFFF; break;
    case 'ADD': registros[destino] = (registros[destino] + valor(fuente)) & 0xFFFF; break;
    default: throw new Error(`no conozco «${op}»`);
  }
}

function correr(programa) {
  let ordenes = 0;
  for (const renglon of programa.split('\n')) {
    if (renglon.split(';')[0].trim() === '') continue;
    ejecutar(renglon);
    ordenes++;
  }
  return ordenes;
}

const programa = `
; mi primer programa
MOV BX, 5     ; la palanca chica

MOV AX, BX
ADD AX, BX    ; el doble
ADD CX, 0
`;
const ordenes = correr(programa);
console.log(`${ordenes} órdenes · ${Object.entries(registros).map(([r, v]) => `${r}=${hex(v)}`).join(' ')}`);
```

#### Al superarla
El programa corre de punta a punta. `AX` termina en `000A`: diez, el doble de cinco. Nova lee el resultado tres veces. —Lo escribí yo. Y lo hizo.

#### Imagen
- Un pergamino largo con un programa de pocos renglones escrito a mano, con comentarios al costado, y las palancas del tablero moviéndose solas.
- Nova abraza el pergamino.

### Micro-misión S04-N02-P5 · La línea del error

```meta
lugar: Las chimeneas
personajes: Nima, Gheco, Nova, Axón (por la chimenea)
carta: Línea | programa.split('\n').forEach((renglon, i) => … `Línea ${i + 1}: …`)
recompensa: xp 15, monedas 5
```

#### Escena
Nova escribe una orden que todavía no existe en el tablero: `MUL`. El tablero dice *no conozco «MUL»*. —¿Pero dónde? —pregunta Nova—. El programa tiene veinte renglones. —Por la chimenea sube la voz de Axón: *«Línea 4.»*

#### Gheco sugiere
En `correr`, atrapá el error de cada renglón y volvé a tirarlo con el número de línea adelante: `Línea 4: no conozco «MUL»`. Las líneas se cuentan desde 1, **incluidos** los renglones vacíos. El programa se frena en el error.

#### Desafío
El error con su línea, y las palancas como quedaron hasta ahí.

#### Código inicial
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');
const registros = { AX: 0, BX: 0, CX: 0, DX: 0 };

function ejecutar(renglon) {
  const [op, destino, fuente] = renglon.split(';')[0].trim().toUpperCase().split(/[\s,]+/);
  const valor = (o) => (o in registros ? registros[o] : Number(o));
  switch (op) {
    case 'MOV': registros[destino] = valor(fuente) & 0xFFFF; break;
    case 'ADD': registros[destino] = (registros[destino] + valor(fuente)) & 0xFFFF; break;
    default: throw new Error(`no conozco «${op}»`);
  }
}

function correr(programa) {
  for (const renglon of programa.split('\n')) {
    if (renglon.split(';')[0].trim() === '') continue;
    ejecutar(renglon);
  }
}

const programa = `MOV AX, 3
ADD AX, 4

MUL AX, 2
MOV BX, 9`;
try {
  correr(programa);
} catch (error) {
  console.log(error.message);
}
console.log(Object.entries(registros).map(([r, v]) => `${r}=${hex(v)}`).join(' '));
```

#### Salida esperada
```
Línea 4: no conozco «MUL»
AX=0007 BX=0000 CX=0000 DX=0000
```

#### Solución
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');
const registros = { AX: 0, BX: 0, CX: 0, DX: 0 };

function ejecutar(renglon) {
  const [op, destino, fuente] = renglon.split(';')[0].trim().toUpperCase().split(/[\s,]+/);
  const valor = (o) => (o in registros ? registros[o] : Number(o));
  switch (op) {
    case 'MOV': registros[destino] = valor(fuente) & 0xFFFF; break;
    case 'ADD': registros[destino] = (registros[destino] + valor(fuente)) & 0xFFFF; break;
    default: throw new Error(`no conozco «${op}»`);
  }
}

function correr(programa) {
  programa.split('\n').forEach((renglon, i) => {
    if (renglon.split(';')[0].trim() === '') return;
    try {
      ejecutar(renglon);
    } catch (error) {
      throw new Error(`Línea ${i + 1}: ${error.message}`);
    }
  });
}

const programa = `MOV AX, 3
ADD AX, 4

MUL AX, 2
MOV BX, 9`;
try {
  correr(programa);
} catch (error) {
  console.log(error.message);
}
console.log(Object.entries(registros).map(([r, v]) => `${r}=${hex(v)}`).join(' '));
```

#### Al superarla
*Línea 4: no conozco «MUL».* Nova encuentra el renglón enseguida. `BX` quedó en cero: el programa se frenó donde tenía que frenarse. —Como Axón —dice—. Exacto y sin adivinar.

#### Imagen
- Un pergamino con un programa donde un renglón brilla en rojo, con un número 4 grande al costado.
- Por la chimenea asoma la sombra del ojo de cristal de Axón; Nova apunta al renglón rojo.

## S04-N03 · Banderas y saltos

```meta
tipo: tema
padre: S04-N02
precio: 10
criatura: orc
temas: maq.banderas, maq.saltos
usa: poo.clases, prog.bucles
```

### Crónica

El tablero ya entiende órdenes, pero solo sabe ir **para adelante**, de arriba hacia abajo. —El Gólem sabe **volver** —dice Nova—: repetir un pedazo hasta que una palanca llegue a cero. Para eso tiene **interruptores**, las banderas, que se prenden solos según cómo salió la última cuenta.

### Objetivos

- Prender la bandera **ZF** (cero) cuando una cuenta da 0.
- Leer las **etiquetas** de un programa (`bucle:`) antes de correrlo.
- Llevar la cuenta de la orden que sigue (el **IP**) y saltar con `JMP`, `JZ` y `JNZ`.
- Comparar con `CMP` sin cambiar los registros, y cortar un programa que no termina con un **tope de pasos**.

### Antes de empezar

- S04-N02 (las órdenes escritas) y los bucles (R01-N04).

### Explicación

#### La bandera del cero
Después de `ADD`, `SUB`, `INC` o `DEC`, el Gólem prende **ZF** si el resultado dio 0, y la apaga si no. `MOV` no la toca.
```javascript
this.zf = this.registros[destino] === 0;
```

#### El IP: dónde va
Para poder saltar, el `for` no alcanza: hace falta un número que diga **cuál orden sigue**. Se llama **IP** (*instruction pointer*, el puntero de instrucción):
```javascript
while (this.ip < this.lineas.length) {
  const orden = this.lineas[this.ip];
  this.ip++;               // por defecto, la siguiente…
  // …salvo que la orden sea un salto, que cambia this.ip
}
```

#### Las etiquetas
Una etiqueta (`bucle:`) no es una orden: es un **nombre** para un lugar del programa. Antes de correr, se recorre todo el texto y se anota a qué orden apunta cada una:
```javascript
if (limpio.endsWith(':')) {
  this.etiquetas[limpio.slice(0, -1)] = this.lineas.length;   // la orden que viene
  continue;
}
```

#### Los saltos
| Orden | Salta si… |
|---|---|
| `JMP etiqueta` | siempre |
| `JZ` o `JE` | ZF está prendida (dio cero, o eran iguales) |
| `JNZ` o `JNE` | ZF está apagada |

`CMP AX, 7` resta sin guardar el resultado: solo prende o apaga ZF. Después de un `CMP`, `JE` salta si eran iguales.

#### El tope
`bucle: JMP bucle` no termina nunca. Como la caja con su tope de vueltas, el tablero cuenta los pasos y se frena a los 1000.

### Código de ejemplo

```javascript
const programa = ['MOV CX, 3', 'bucle:', 'DEC CX', 'JNZ bucle', 'MOV AX, 1'];
const lineas = [];
const etiquetas = {};
for (const renglon of programa) {
  if (renglon.endsWith(':')) etiquetas[renglon.slice(0, -1)] = lineas.length;
  else lineas.push(renglon);
}
console.log(lineas);
console.log(etiquetas);

let cx = 3;
let vueltas = 0;
do {
  cx--;
  vueltas++;
} while (cx !== 0);
console.log(`Dio ${vueltas} vueltas; ZF quedó prendida: ${cx === 0}`);
```

### Salida esperada

```
[ 'MOV CX, 3', 'DEC CX', 'JNZ bucle', 'MOV AX, 1' ]
{ bucle: 1 }
Dio 3 vueltas; ZF quedó prendida: true
```

### ¿Para qué sirve?

Así funcionan por dentro **todos** los `if`, `while` y `for` de todos los lenguajes: al final, la máquina compara, prende una bandera y salta. Entender el IP es entender qué hace un depurador cuando avanza «paso a paso».

### Errores habituales

**Orco: saltar a una etiqueta que no existe.** `this.etiquetas['BUCEL']` es `undefined`, y `this.ip = undefined` hace que el `while` termine sin avisar. Revisá que exista y tirá un error si no.

**Ogro: la etiqueta contada como orden.** Si `bucle:` entra en `lineas`, todos los saltos caen una orden más abajo.

**Troll: el bucle sin fin.** Un `JNZ` sobre un registro que nunca llega a cero da vueltas para siempre. Para eso está el tope.

### Micro-misión S04-N03-P1 · El interruptor del cero

```meta
lugar: El tablero de práctica, en la Feria
personajes: Nima, Gheco, Nova
carta: ZF | this.zf = this.registros[destino] === 0 (en ADD, SUB, INC, DEC; MOV no)
recompensa: xp 10, oro 10
```

#### Escena
Nova pone un interruptor nuevo en el tablero de práctica, con una Z pintada. —Se prende solo cuando una cuenta da cero. Es el que más uso.

#### Gheco sugiere
En `Maquina`, el método `cuenta(destino, n)` guarda el resultado con 16 bits. Hacé que también actualice `this.zf`. `MOV` usa `poner`, que no toca la bandera.

#### Desafío
Mostrá `CX` y `ZF` después de cada orden.

#### Código inicial
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

class Maquina {
  constructor() {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
    this.zf = false;
  }

  poner(destino, n) {
    this.registros[destino] = n & 0xFFFF;
  }

  cuenta(destino, n) {
    this.registros[destino] = n & 0xFFFF;
  }

  ejecutar(renglon) {
    const [op, destino, fuente] = renglon.toUpperCase().split(/[\s,]+/);
    const valor = (o) => (o in this.registros ? this.registros[o] : Number(o));
    if (op === 'MOV') this.poner(destino, valor(fuente));
    if (op === 'DEC') this.cuenta(destino, this.registros[destino] - 1);
    if (op === 'ADD') this.cuenta(destino, this.registros[destino] + valor(fuente));
  }
}

const m = new Maquina();
for (const renglon of ['MOV CX, 2', 'DEC CX', 'DEC CX', 'MOV CX, 0', 'ADD CX, 1', 'ADD CX, 0FFFFh']) {
  m.ejecutar(renglon);
  console.log(`${renglon.padEnd(15)} CX=${hex(m.registros.CX)} ZF=${m.zf ? 1 : 0}`);
}
```

#### Salida esperada
```
MOV CX, 2       CX=0002 ZF=0
DEC CX          CX=0001 ZF=0
DEC CX          CX=0000 ZF=1
MOV CX, 0       CX=0000 ZF=1
ADD CX, 1       CX=0001 ZF=0
ADD CX, 0FFFFh  CX=0000 ZF=1
```

#### Solución
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

class Maquina {
  constructor() {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
    this.zf = false;
  }

  poner(destino, n) {
    this.registros[destino] = n & 0xFFFF;
  }

  cuenta(destino, n) {
    this.registros[destino] = n & 0xFFFF;
    this.zf = this.registros[destino] === 0;
  }

  ejecutar(renglon) {
    const [op, destino, fuente] = renglon.toUpperCase().split(/[\s,]+/);
    const valor = (o) => (o in this.registros ? this.registros[o] : /^[0-9A-F]+H$/.test(o) ? parseInt(o.slice(0, -1), 16) : Number(o));
    if (op === 'MOV') this.poner(destino, valor(fuente));
    if (op === 'DEC') this.cuenta(destino, this.registros[destino] - 1);
    if (op === 'ADD') this.cuenta(destino, this.registros[destino] + valor(fuente));
  }
}

const m = new Maquina();
for (const renglon of ['MOV CX, 2', 'DEC CX', 'DEC CX', 'MOV CX, 0', 'ADD CX, 1', 'ADD CX, 0FFFFh']) {
  m.ejecutar(renglon);
  console.log(`${renglon.padEnd(15)} CX=${hex(m.registros.CX)} ZF=${m.zf ? 1 : 0}`);
}
```

#### Al superarla
El interruptor se prende cuando `CX` llega a cero, y también cuando `0001 + FFFF` da la vuelta a `0000`. Nova lo mira prenderse y apagarse como quien mira una luciérnaga.

#### Imagen
- Un interruptor de bronce con una Z pintada, encendido con una luz cian, en el tablero de práctica.
- Nova lo mira de cerca con los ojos brillantes; una luciérnaga pasa volando al lado.

### Micro-misión S04-N03-P2 · Los nombres de los lugares

```meta
lugar: El tablero de práctica
personajes: Nima, Gheco, Nova
carta: Etiquetas | if (limpio.endsWith(':')) etiquetas[nombre] = lineas.length
recompensa: xp 10, oro 10
```

#### Escena
Nova le pone nombre a los lugares de su programa, como las paradas de un recorrido: `inicio:`, `bucle:`, `fin:`. —No son órdenes —aclara—. Son carteles.

#### Gheco sugiere
Completá `leer(texto)`: devuelve `lineas` (solo las órdenes, sin comentarios ni vacíos, en mayúsculas) y `etiquetas` (cada nombre, en mayúsculas, con la posición de la orden que viene después).

#### Desafío
`4 órdenes` y las etiquetas `{"INICIO":0,"BUCLE":1,"FIN":3}`.

#### Código inicial
```javascript
function leer(texto) {
  const lineas = [];
  const etiquetas = {};
  for (const renglon of texto.split('\n')) {
    const limpio = renglon.split(';')[0].trim().toUpperCase();
    if (limpio === '') continue;
    lineas.push(limpio);
  }
  return { lineas, etiquetas };
}

const { lineas, etiquetas } = leer(`
inicio:
  MOV CX, 3
bucle:
  DEC CX      ; una menos
  JNZ bucle
fin:
  MOV AX, 1
`);
console.log(`${lineas.length} órdenes`);
console.log(JSON.stringify(etiquetas));
```

#### Salida esperada
```
4 órdenes
{"INICIO":0,"BUCLE":1,"FIN":3}
```

#### Solución
```javascript
function leer(texto) {
  const lineas = [];
  const etiquetas = {};
  for (const renglon of texto.split('\n')) {
    const limpio = renglon.split(';')[0].trim().toUpperCase();
    if (limpio === '') continue;
    if (limpio.endsWith(':')) {
      etiquetas[limpio.slice(0, -1)] = lineas.length;
      continue;
    }
    lineas.push(limpio);
  }
  return { lineas, etiquetas };
}

const { lineas, etiquetas } = leer(`
inicio:
  MOV CX, 3
bucle:
  DEC CX      ; una menos
  JNZ bucle
fin:
  MOV AX, 1
`);
console.log(`${lineas.length} órdenes`);
console.log(JSON.stringify(etiquetas));
```

#### Al superarla
Tres carteles, cada uno clavado donde va. Nova los acaricia como si fueran plantas.

#### Imagen
- Tres carteles de madera clavados entre los renglones de un pergamino largo, como paradas de un camino.
- Nova acaricia uno con la punta de los dedos.

### Micro-misión S04-N03-P3 · La primera vuelta

```meta
lugar: El tablero de práctica
personajes: Nima, Gheco, Nova
carta: IP y saltos | while (this.ip < lineas.length) { … this.ip++ … JNZ: if (!this.zf) this.ip = etiquetas[destino] }
recompensa: xp 10, oro 10
```

#### Escena
Llegó el momento: el primer programa que **vuelve**. Nova quiere sumar 5 + 4 + 3 + 2 + 1, sin escribir cinco `ADD`.

#### Gheco sugiere
En `correr`, usá `this.ip` para saber qué orden sigue. `JMP` salta siempre; `JNZ`, solo si ZF está apagada. Al saltar, `this.ip` pasa a la posición de la etiqueta.

#### Desafío
`AX=000F CX=0000`, en 16 pasos.

#### Código inicial
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

class Maquina {
  constructor(texto) {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
    this.zf = false;
    this.ip = 0;
    this.pasos = 0;
    this.lineas = [];
    this.etiquetas = {};
    for (const renglon of texto.split('\n')) {
      const limpio = renglon.split(';')[0].trim().toUpperCase();
      if (limpio === '') continue;
      if (limpio.endsWith(':')) this.etiquetas[limpio.slice(0, -1)] = this.lineas.length;
      else this.lineas.push(limpio.split(/[\s,]+/));
    }
  }

  valor(o) {
    return o in this.registros ? this.registros[o] : Number(o);
  }

  cuenta(destino, n) {
    this.registros[destino] = n & 0xFFFF;
    this.zf = this.registros[destino] === 0;
  }

  correr() {
    for (const [op, destino, fuente] of this.lineas) {
      this.pasos++;
      if (op === 'MOV') this.registros[destino] = this.valor(fuente) & 0xFFFF;
      else if (op === 'ADD') this.cuenta(destino, this.registros[destino] + this.valor(fuente));
      else if (op === 'DEC') this.cuenta(destino, this.registros[destino] - 1);
    }
  }
}

const m = new Maquina(`
  MOV CX, 5
bucle:
  ADD AX, CX
  DEC CX
  JNZ bucle
`);
m.correr();
console.log(`AX=${hex(m.registros.AX)} CX=${hex(m.registros.CX)}, en ${m.pasos} pasos`);
```

#### Salida esperada
```
AX=000F CX=0000, en 16 pasos
```

#### Solución
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

class Maquina {
  constructor(texto) {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
    this.zf = false;
    this.ip = 0;
    this.pasos = 0;
    this.lineas = [];
    this.etiquetas = {};
    for (const renglon of texto.split('\n')) {
      const limpio = renglon.split(';')[0].trim().toUpperCase();
      if (limpio === '') continue;
      if (limpio.endsWith(':')) this.etiquetas[limpio.slice(0, -1)] = this.lineas.length;
      else this.lineas.push(limpio.split(/[\s,]+/));
    }
  }

  valor(o) {
    return o in this.registros ? this.registros[o] : Number(o);
  }

  cuenta(destino, n) {
    this.registros[destino] = n & 0xFFFF;
    this.zf = this.registros[destino] === 0;
  }

  correr() {
    while (this.ip < this.lineas.length) {
      const [op, destino, fuente] = this.lineas[this.ip];
      this.ip++;
      this.pasos++;
      if (op === 'MOV') this.registros[destino] = this.valor(fuente) & 0xFFFF;
      else if (op === 'ADD') this.cuenta(destino, this.registros[destino] + this.valor(fuente));
      else if (op === 'DEC') this.cuenta(destino, this.registros[destino] - 1);
      else if (op === 'JMP') this.ip = this.etiquetas[destino];
      else if (op === 'JNZ' && !this.zf) this.ip = this.etiquetas[destino];
    }
  }
}

const m = new Maquina(`
  MOV CX, 5
bucle:
  ADD AX, CX
  DEC CX
  JNZ bucle
`);
m.correr();
console.log(`AX=${hex(m.registros.AX)} CX=${hex(m.registros.CX)}, en ${m.pasos} pasos`);
```

#### Al superarla
`000F`: quince, la suma de cinco, cuatro, tres, dos y uno, con tres órdenes que dieron cinco vueltas. Abajo, en las Forjas, Nova prueba el mismo programa en el Gólem de verdad, y por las chimeneas sube un ruido de engranajes que giran, se frenan y vuelven a girar. Cinco veces.

#### Imagen
- Un engranaje de bronce que gira en círculo con tres órdenes talladas, y una palanca que baja de cinco a cero.
- Nova, con los brazos abiertos, gira en el aire con el engranaje.

### Micro-misión S04-N03-P4 · ¿Son iguales?

```meta
lugar: El tablero de práctica
personajes: Nima, Gheco, Nova
carta: CMP | CMP AX, 7 → this.zf = ((a - b) & 0xFFFF) === 0 (no guarda) · JE salta si son iguales
recompensa: xp 15, monedas 5
```

#### Escena
Nova quiere que el Gólem **decida**: si la palanca grande vale siete, que prenda el ojo (`BX` en 1); si no, que lo deje apagado (`BX` en 2).

#### Gheco sugiere
Agregá `CMP`: resta sin guardar y solo actualiza ZF. Agregá `JE` (salta si ZF está prendida) y `JNE` (si está apagada). Probá el programa con `AX` en 7 y en 3.

#### Desafío
`Con AX=7: BX=0001` y `Con AX=3: BX=0002`.

#### Código inicial
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

class Maquina {
  constructor(texto, ax) {
    this.registros = { AX: ax, BX: 0, CX: 0, DX: 0 };
    this.zf = false;
    this.ip = 0;
    this.lineas = [];
    this.etiquetas = {};
    for (const renglon of texto.split('\n')) {
      const limpio = renglon.split(';')[0].trim().toUpperCase();
      if (limpio === '') continue;
      if (limpio.endsWith(':')) this.etiquetas[limpio.slice(0, -1)] = this.lineas.length;
      else this.lineas.push(limpio.split(/[\s,]+/));
    }
  }

  valor(o) {
    return o in this.registros ? this.registros[o] : Number(o);
  }

  correr() {
    while (this.ip < this.lineas.length) {
      const [op, destino, fuente] = this.lineas[this.ip];
      this.ip++;
      if (op === 'MOV') this.registros[destino] = this.valor(fuente) & 0xFFFF;
      else if (op === 'JMP') this.ip = this.etiquetas[destino];
    }
  }
}

const programa = `
  CMP AX, 7
  JE  iguales
  MOV BX, 2      ; distinto: el ojo apagado
  JMP fin
iguales:
  MOV BX, 1      ; igual: el ojo prendido
fin:
`;
for (const ax of [7, 3]) {
  const m = new Maquina(programa, ax);
  m.correr();
  console.log(`Con AX=${ax}: BX=${hex(m.registros.BX)}`);
}
```

#### Salida esperada
```
Con AX=7: BX=0001
Con AX=3: BX=0002
```

#### Solución
```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

class Maquina {
  constructor(texto, ax) {
    this.registros = { AX: ax, BX: 0, CX: 0, DX: 0 };
    this.zf = false;
    this.ip = 0;
    this.lineas = [];
    this.etiquetas = {};
    for (const renglon of texto.split('\n')) {
      const limpio = renglon.split(';')[0].trim().toUpperCase();
      if (limpio === '') continue;
      if (limpio.endsWith(':')) this.etiquetas[limpio.slice(0, -1)] = this.lineas.length;
      else this.lineas.push(limpio.split(/[\s,]+/));
    }
  }

  valor(o) {
    return o in this.registros ? this.registros[o] : Number(o);
  }

  correr() {
    while (this.ip < this.lineas.length) {
      const [op, destino, fuente] = this.lineas[this.ip];
      this.ip++;
      if (op === 'MOV') this.registros[destino] = this.valor(fuente) & 0xFFFF;
      else if (op === 'CMP') this.zf = ((this.valor(destino) - this.valor(fuente)) & 0xFFFF) === 0;
      else if (op === 'JMP') this.ip = this.etiquetas[destino];
      else if (op === 'JE' && this.zf) this.ip = this.etiquetas[destino];
      else if (op === 'JNE' && !this.zf) this.ip = this.etiquetas[destino];
    }
  }
}

const programa = `
  CMP AX, 7
  JE  iguales
  MOV BX, 2      ; distinto: el ojo apagado
  JMP fin
iguales:
  MOV BX, 1      ; igual: el ojo prendido
fin:
`;
for (const ax of [7, 3]) {
  const m = new Maquina(programa, ax);
  m.correr();
  console.log(`Con AX=${ax}: BX=${hex(m.registros.BX)}`);
}
```

#### Al superarla
Con siete, el ojo se prende; con tres, no. Nova se queda callada un rato. —Esto es un `if` —dice al fin—. Lo que ustedes escriben con `if`, por dentro, ¿es esto? —Gheco asiente. —Todo es esto.

#### Imagen
- El ojo redondo de cristal del Gólem, encendido en cian, reflejado en un tablero de práctica con dos caminos dibujados.
- Nova, pensativa, con la mano en el mentón.

### Micro-misión S04-N03-P5 · El tope de Axón

```meta
lugar: El tablero de práctica
personajes: Nima, Gheco, Nova, Axón
carta: Tope | if (++this.pasos > 1000) throw new Error('…más de 1000 pasos…')
recompensa: xp 15, monedas 5
```

#### Escena
Nova escribe sin querer un programa que no termina: el tablero se queda pensando y la pestaña de Nima se congela (la caja la corta con su propio tope). Por la chimenea, Axón: *«Yo cuento mis pasos. A los mil, me detengo y aviso.»*

#### Gheco sugiere
En `correr`, contá los pasos. Si pasan de 1000, tirá un `Error` con `Axón se detuvo: más de 1000 pasos. ¿Hay un salto que no termina?`. Atrapalo y mostralo. Si el salto va a una etiqueta que no existe, tirá `no hay ninguna etiqueta «…»`.

#### Desafío
Los dos programas, cada uno con su aviso.

#### Código inicial
```javascript
class Maquina {
  constructor(texto) {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
    this.ip = 0;
    this.pasos = 0;
    this.lineas = [];
    this.etiquetas = {};
    for (const renglon of texto.split('\n')) {
      const limpio = renglon.split(';')[0].trim().toUpperCase();
      if (limpio === '') continue;
      if (limpio.endsWith(':')) this.etiquetas[limpio.slice(0, -1)] = this.lineas.length;
      else this.lineas.push(limpio.split(/[\s,]+/));
    }
  }

  saltar(etiqueta) {
    this.ip = this.etiquetas[etiqueta];
  }

  correr() {
    while (this.ip < this.lineas.length) {
      const [op, destino] = this.lineas[this.ip];
      this.ip++;
      if (op === 'INC') this.registros[destino] = (this.registros[destino] + 1) & 0xFFFF;
      else if (op === 'JMP') this.saltar(destino);
      if (this.pasos > 5) break;
    }
  }
}

for (const programa of ['siempre:\nINC AX\nJMP siempre', 'INC AX\nJMP sieempre']) {
  const m = new Maquina(programa);
  try {
    m.correr();
    console.log(`Terminó en ${m.pasos} pasos`);
  } catch (error) {
    console.log(error.message);
  }
}
```

#### Salida esperada
```
Axón se detuvo: más de 1000 pasos. ¿Hay un salto que no termina?
no hay ninguna etiqueta «SIEEMPRE»
```

#### Solución
```javascript
class Maquina {
  constructor(texto) {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
    this.ip = 0;
    this.pasos = 0;
    this.lineas = [];
    this.etiquetas = {};
    for (const renglon of texto.split('\n')) {
      const limpio = renglon.split(';')[0].trim().toUpperCase();
      if (limpio === '') continue;
      if (limpio.endsWith(':')) this.etiquetas[limpio.slice(0, -1)] = this.lineas.length;
      else this.lineas.push(limpio.split(/[\s,]+/));
    }
  }

  saltar(etiqueta) {
    if (!(etiqueta in this.etiquetas)) throw new Error(`no hay ninguna etiqueta «${etiqueta}»`);
    this.ip = this.etiquetas[etiqueta];
  }

  correr() {
    while (this.ip < this.lineas.length) {
      if (++this.pasos > 1000) throw new Error('Axón se detuvo: más de 1000 pasos. ¿Hay un salto que no termina?');
      const [op, destino] = this.lineas[this.ip];
      this.ip++;
      if (op === 'INC') this.registros[destino] = (this.registros[destino] + 1) & 0xFFFF;
      else if (op === 'JMP') this.saltar(destino);
    }
  }
}

for (const programa of ['siempre:\nINC AX\nJMP siempre', 'INC AX\nJMP sieempre']) {
  const m = new Maquina(programa);
  try {
    m.correr();
    console.log(`Terminó en ${m.pasos} pasos`);
  } catch (error) {
    console.log(error.message);
  }
}
```

#### Al superarla
El tablero ya no se congela: avisa. Y la etiqueta mal escrita, `SIEEMPRE`, también. Por la chimenea, Axón dice *«Correcto»*, y esta vez Nova jura que lo dijo un poco más suave.

#### Imagen
- Un contador de pasos de bronce con muchas cifras, frenado con una traba, y un cartelito de aviso al lado.
- Nova y Nima se miran contentas; por la chimenea brilla el ojo de Axón.

## S04-N04 · Jefe: la Herrumbre

```meta
tipo: jefe
padre: S04-N03
precio: 10
criatura: dragon
insignia: Maestra del Tablero
insignia_descripcion: Armaste el tablero de práctica de Nova: registros, órdenes, banderas, saltos y un paso a paso en la página.
temas: js.dom, js.modulos
usa: maq.registros, maq.saltos, js.eventos, poo.clases
```

### Crónica

Nova vuelve a la Feria más apagada que nunca. —Algo se mete en el Gólem. Una **herrumbre** roja que sube por las palancas y las traba. Cuando una palanca se traba, el Gólem se queda a mitad de un programa, y yo no sé **dónde** se quedó.

Gheco lo entiende enseguida. —Necesita **ver** el programa mientras corre. Orden por orden, con las palancas a la vista. Un **paso a paso**, como los depuradores de los programadores.

Nima abre el Taller de los Títeres y arma una mesa larga: ahí va a ir el tablero, ya no en la consola, sino **en la página**. La máquina que armaron entre las dos viene en un módulo aparte, `maquina.js`, listo para importar.

### Objetivos

- Importar la máquina de un módulo (`import { Maquina, hex } from './maquina.js'`).
- Dibujar el estado de la máquina en la página: registros, bandera ZF y la orden que sigue.
- Avanzar una orden por click, y frenar al terminar.
- Correr solo con un temporizador, pausar, reiniciar y mostrar los errores sin romper la página.

### Antes de empezar

- Todo el Tablero (S04-N01 a N03) y los módulos (R03-N06).

### Explicación

#### La máquina, en su módulo
`maquina.js` tiene todo lo que armaron en las tres paradas anteriores:
```javascript
import { Maquina, hex } from './maquina.js';
const m = new Maquina('MOV AX, 5\nINC AX');
m.paso();            // ejecuta UNA orden (la del ip) y avanza
m.registros.AX;      // 5
m.ip;                // 1: la que sigue
m.terminado;         // false: todavía queda una
m.lineas[m.ip];      // { numero: 2, texto: 'INC AX', … }
```

#### Dibujar desde el estado
La regla de oro de una página con datos: **el estado manda**. Hay una sola función, `dibujar()`, que lee la máquina y pone todo en la página. Cada botón cambia la máquina y llama a `dibujar()`:
```javascript
function dibujar() {
  for (const r of ['AX', 'BX', 'CX', 'DX']) document.querySelector(`#${r}`).textContent = hex(m.registros[r]);
  document.querySelectorAll('#programa li').forEach((li, i) => li.classList.toggle('actual', i === m.ip));
}
```

#### Correr solo
```javascript
const reloj = setInterval(() => {
  if (m.terminado) return clearInterval(reloj);
  m.paso();
  dibujar();
}, 500);
```

### Código de ejemplo

```javascript
const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');
const estado = { ip: 0, AX: 0 };
const ordenes = [() => (estado.AX = 5), () => (estado.AX += 1), () => (estado.AX *= 2)];

function dibujar() {
  console.log(`ip=${estado.ip} AX=${hex(estado.AX)}${estado.ip >= ordenes.length ? ' (fin)' : ''}`);
}

dibujar();
while (estado.ip < ordenes.length) {
  ordenes[estado.ip]();
  estado.ip++;
  dibujar();
}
```

### Salida esperada

```
ip=0 AX=0000
ip=1 AX=0005
ip=2 AX=0006
ip=3 AX=000C (fin)
```

### ¿Para qué sirve?

El paso a paso es la herramienta más importante para encontrar errores: las herramientas de desarrollador del navegador, los editores de código y el tablero del curso de Ensamblador funcionan así. Y «el estado manda, la página lo dibuja» es la idea central de React, Vue y todos los frameworks de interfaz.

### Errores habituales

**Ogro: cambiar la página sin cambiar la máquina.** Si un botón cambia el texto de `#AX` directamente, la página y la máquina dicen cosas distintas. Siempre: cambiar la máquina, después `dibujar()`.

**Troll: el intervalo que nadie para.** Si «Correr» se toca dos veces, arrancan dos intervalos y la máquina corre al doble. Cancelá el anterior antes de crear uno.

**Esqueleto: importar sin `./`.** `import … from 'maquina.js'` busca un paquete, no el archivo de al lado.

### Micro-misión S04-N04-P1 · El tablero en la página

```meta
lugar: El Taller de los Títeres, la mesa larga
personajes: Nima, Gheco, Nova
carta: dibujar() | import { Maquina, hex } from './maquina.js' · #AX.textContent = hex(m.registros.AX)
recompensa: xp 10, oro 10
```

#### Escena
La mesa larga ya tiene sus casilleros dibujados: cuatro palancas, el interruptor Z y el programa al costado. Falta que muestren lo que tiene la máquina.

#### Gheco sugiere
Importá `Maquina` y `hex` de `./maquina.js`. Escribí `dibujar()`: los cuatro registros en sus celdas (`#AX`, `#BX`…), `ZF` en `#ZF` (`1` o `0`), y el programa en `#programa`, un `<li>` por orden con su `texto`. Corré el programa entero con `m.correr()` y dibujá.

#### Desafío
El tablero con la máquina al final del programa.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #0d1117; color: #c9d1d9; padding: 12px; display: flex; gap: 16px; }
  table { border-collapse: collapse; } td, th { border: 1px solid #30363d; padding: 4px 10px; font-family: monospace; }
  th { color: #3dd6f5; }
  ol { font-family: monospace; margin: 0; } li.actual { background: #3dd6f5; color: #0d1117; }
</style>
<table>
  <tr><th>AX</th><td id="AX"></td></tr><tr><th>BX</th><td id="BX"></td></tr>
  <tr><th>CX</th><td id="CX"></td></tr><tr><th>DX</th><td id="DX"></td></tr>
  <tr><th>ZF</th><td id="ZF"></td></tr>
</table>
<ol id="programa"></ol>
```

#### Archivos
maquina.js
```javascript
export const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

export class Maquina {
  constructor(texto) {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
    this.zf = false;
    this.ip = 0;
    this.pasos = 0;
    this.lineas = [];
    this.etiquetas = {};
    texto.split('\n').forEach((renglon, i) => {
      const limpio = renglon.split(';')[0].trim();
      if (limpio === '') return;
      if (limpio.endsWith(':')) {
        this.etiquetas[limpio.slice(0, -1).toUpperCase()] = this.lineas.length;
        return;
      }
      const [op, destino, fuente] = limpio.toUpperCase().split(/[\s,]+/);
      this.lineas.push({ numero: i + 1, texto: limpio, op, destino, fuente });
    });
  }

  get terminado() {
    return this.ip >= this.lineas.length;
  }

  valor(o) {
    if (o in this.registros) return this.registros[o];
    if (/^[0-9A-F]+H$/.test(o)) return parseInt(o.slice(0, -1), 16);
    if (/^\d+$/.test(o)) return Number(o);
    throw new Error(`no entiendo «${o}»`);
  }

  cuenta(destino, n) {
    if (!(destino in this.registros)) throw new Error(`no hay palanca «${destino}»`);
    this.registros[destino] = n & 0xFFFF;
    this.zf = this.registros[destino] === 0;
  }

  saltar(etiqueta) {
    if (!(etiqueta in this.etiquetas)) throw new Error(`no hay ninguna etiqueta «${etiqueta}»`);
    this.ip = this.etiquetas[etiqueta];
  }

  paso() {
    if (this.terminado) return;
    const { numero, op, destino, fuente } = this.lineas[this.ip];
    this.ip++;
    this.pasos++;
    try {
      switch (op) {
        case 'MOV':
          if (!(destino in this.registros)) throw new Error(`no hay palanca «${destino}»`);
          this.registros[destino] = this.valor(fuente) & 0xFFFF;
          break;
        case 'ADD': this.cuenta(destino, this.registros[destino] + this.valor(fuente)); break;
        case 'SUB': this.cuenta(destino, this.registros[destino] - this.valor(fuente)); break;
        case 'INC': this.cuenta(destino, this.registros[destino] + 1); break;
        case 'DEC': this.cuenta(destino, this.registros[destino] - 1); break;
        case 'CMP': this.zf = ((this.valor(destino) - this.valor(fuente)) & 0xFFFF) === 0; break;
        case 'JMP': this.saltar(destino); break;
        case 'JZ': case 'JE': if (this.zf) this.saltar(destino); break;
        case 'JNZ': case 'JNE': if (!this.zf) this.saltar(destino); break;
        default: throw new Error(`no conozco «${op}»`);
      }
    } catch (error) {
      this.ip--;
      throw new Error(`Línea ${numero}: ${error.message}`);
    }
  }

  correr(tope = 1000) {
    while (!this.terminado) {
      if (this.pasos >= tope) throw new Error(`Axón se detuvo: más de ${tope} pasos.`);
      this.paso();
    }
  }
}
```

#### Estado
```
td
#programa li
```

#### Código inicial
```javascript
const m = new Maquina(`MOV AX, 2
MOV CX, 3
ADD AX, CX
DEC CX`);

```

#### Salida esperada
```
── Estado ──
td: 0005
td: 0000
td: 0002
td: 0000
td: 0
#programa li: MOV AX, 2
#programa li: MOV CX, 3
#programa li: ADD AX, CX
#programa li: DEC CX
```

#### Solución
```javascript
import { Maquina, hex } from './maquina.js';

const m = new Maquina(`MOV AX, 2
MOV CX, 3
ADD AX, CX
DEC CX`);

function dibujar() {
  for (const r of ['AX', 'BX', 'CX', 'DX']) document.querySelector(`#${r}`).textContent = hex(m.registros[r]);
  document.querySelector('#ZF').textContent = m.zf ? '1' : '0';
  const lista = document.querySelector('#programa');
  lista.replaceChildren(...m.lineas.map((linea) => {
    const li = document.createElement('li');
    li.textContent = linea.texto;
    return li;
  }));
}

m.correr();
dibujar();
```

#### Al superarla
Las palancas aparecen en la mesa larga, con sus cifras: `AX=0005`, `CX=0002`. Nova las toca una por una, como quien reconoce su propia cara en un espejo.

#### Imagen
- Una mesa larga de madera en un taller de títeres, con un tablero dibujado: cuatro casilleros con cifras cian, un interruptor con una Z y un pergamino con renglones al costado.
- Nova toca los casilleros con la punta de los dedos; Nima y Gheco la miran.

### Micro-misión S04-N04-P2 · Un paso por click

```meta
lugar: El Taller de los Títeres, la mesa larga
personajes: Nima, Gheco, Nova
carta: Paso a paso | boton.addEventListener('click', () => { m.paso(); dibujar(); }) · li.classList.toggle('actual', i === m.ip)
recompensa: xp 10, oro 10
```

#### Escena
—Ahora quiero verlo **despacio** —pide Nova—. Una orden, y miro. Otra orden, y miro.

#### Gheco sugiere
Al empezar, dibujá sin correr nada. El botón `#paso` ejecuta **una** orden y vuelve a dibujar. En `dibujar`, marcá con la clase `actual` el `<li>` de la orden que sigue (`m.ip`).

#### Desafío
Dos pasos: `AX=0002`, `CX=0003`, y marcada la tercera orden.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #0d1117; color: #c9d1d9; padding: 12px; }
  td, th { border: 1px solid #30363d; padding: 4px 10px; font-family: monospace; }
  ol { font-family: monospace; } li.actual { background: #3dd6f5; color: #0d1117; }
</style>
<button id="paso">Paso ▶</button>
<table><tr><th>AX</th><td id="AX"></td><th>CX</th><td id="CX"></td></tr></table>
<ol id="programa"></ol>
```

#### Archivos
maquina.js
```javascript
export const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

export class Maquina {
  constructor(texto) {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
    this.zf = false;
    this.ip = 0;
    this.lineas = texto.split('\n').map((renglon) => renglon.trim()).filter(Boolean).map((texto) => {
      const [op, destino, fuente] = texto.toUpperCase().split(/[\s,]+/);
      return { texto, op, destino, fuente };
    });
  }

  get terminado() {
    return this.ip >= this.lineas.length;
  }

  paso() {
    if (this.terminado) return;
    const { op, destino, fuente } = this.lineas[this.ip++];
    const valor = fuente in this.registros ? this.registros[fuente] : Number(fuente);
    if (op === 'MOV') this.registros[destino] = valor & 0xFFFF;
    if (op === 'ADD') this.registros[destino] = (this.registros[destino] + valor) & 0xFFFF;
    if (op === 'DEC') this.registros[destino] = (this.registros[destino] - 1) & 0xFFFF;
    if (['ADD', 'DEC'].includes(op)) this.zf = this.registros[destino] === 0;
  }
}
```

#### Eventos
```
click #paso
click #paso
```

#### Estado
```
#AX
#CX
li.actual
```

#### Código inicial
```javascript
import { Maquina, hex } from './maquina.js';

const m = new Maquina(`MOV AX, 2
MOV CX, 3
ADD AX, CX
DEC CX`);

const lista = document.querySelector('#programa');
for (const linea of m.lineas) {
  const li = document.createElement('li');
  li.textContent = linea.texto;
  lista.append(li);
}

function dibujar() {
  document.querySelector('#AX').textContent = hex(m.registros.AX);
  document.querySelector('#CX').textContent = hex(m.registros.CX);
}

dibujar();
```

#### Salida esperada
```
── Estado ──
#AX: 0002
#CX: 0003
li.actual: ADD AX, CX
```

#### Solución
```javascript
import { Maquina, hex } from './maquina.js';

const m = new Maquina(`MOV AX, 2
MOV CX, 3
ADD AX, CX
DEC CX`);

const lista = document.querySelector('#programa');
for (const linea of m.lineas) {
  const li = document.createElement('li');
  li.textContent = linea.texto;
  lista.append(li);
}

function dibujar() {
  document.querySelector('#AX').textContent = hex(m.registros.AX);
  document.querySelector('#CX').textContent = hex(m.registros.CX);
  lista.querySelectorAll('li').forEach((li, i) => li.classList.toggle('actual', i === m.ip));
}

document.querySelector('#paso').addEventListener('click', () => {
  m.paso();
  dibujar();
});
dibujar();
```

#### Al superarla
Un click, una orden. La franja cian baja por el programa como el dedo de alguien que lee despacio. Nova se ríe: —¡Así pienso yo! De a una cosa.

#### Imagen
- Un pergamino con renglones de código donde una franja de luz cian ilumina un solo renglón, como un dedo que lee.
- Nova aprieta un botón de bronce grande, con una flecha, riéndose.

### Micro-misión S04-N04-P3 · El final del programa

```meta
lugar: El Taller de los Títeres, la mesa larga
personajes: Nima, Gheco, Nova
carta: terminado | if (m.terminado) { boton.disabled = true; estado.textContent = 'Fin del programa' }
recompensa: xp 10, oro 10
```

#### Escena
Nova sigue tocando «Paso» cuando el programa ya terminó, y no pasa nada. No sabe si se trabó o si terminó. —La herrumbre hace eso —dice—: te deja tocando y no avisa.

#### Gheco sugiere
En `dibujar`, si la máquina terminó, deshabilitá `#paso` y poné `Fin del programa` en `#estado`. Si no, `Sigue: la orden N` (con el número de la que sigue, contando desde 1).

#### Desafío
Seis clicks a un programa de tres órdenes.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #0d1117; color: #c9d1d9; padding: 12px; }
  #estado { color: #3dd6f5; }
</style>
<button id="paso">Paso ▶</button> <span id="estado"></span>
<p>AX = <span id="AX"></span></p>
```

#### Archivos
maquina.js
```javascript
export const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

export class Maquina {
  constructor(texto) {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
    this.ip = 0;
    this.lineas = texto.split('\n').map((renglon) => renglon.trim()).filter(Boolean).map((texto) => {
      const [op, destino, fuente] = texto.toUpperCase().split(/[\s,]+/);
      return { texto, op, destino, fuente };
    });
  }

  get terminado() {
    return this.ip >= this.lineas.length;
  }

  paso() {
    if (this.terminado) return;
    const { op, destino, fuente } = this.lineas[this.ip++];
    if (op === 'MOV') this.registros[destino] = Number(fuente) & 0xFFFF;
    if (op === 'INC') this.registros[destino] = (this.registros[destino] + 1) & 0xFFFF;
  }
}
```

#### Eventos
```
click #paso
click #paso
click #paso
click #paso
click #paso
click #paso
```

#### Estado
```
#AX
#estado
#paso @disabled
```

#### Código inicial
```javascript
import { Maquina, hex } from './maquina.js';

const m = new Maquina('MOV AX, 7\nINC AX\nINC AX');
const boton = document.querySelector('#paso');
const estado = document.querySelector('#estado');

function dibujar() {
  document.querySelector('#AX').textContent = hex(m.registros.AX);
}

boton.addEventListener('click', () => {
  m.paso();
  dibujar();
});
dibujar();
```

#### Salida esperada
```
── Estado ──
#AX: 0009
#estado: Fin del programa
#paso @disabled: sí
```

#### Solución
```javascript
import { Maquina, hex } from './maquina.js';

const m = new Maquina('MOV AX, 7\nINC AX\nINC AX');
const boton = document.querySelector('#paso');
const estado = document.querySelector('#estado');

function dibujar() {
  document.querySelector('#AX').textContent = hex(m.registros.AX);
  boton.disabled = m.terminado;
  estado.textContent = m.terminado ? 'Fin del programa' : `Sigue: la orden ${m.ip + 1}`;
}

boton.addEventListener('click', () => {
  m.paso();
  dibujar();
});
dibujar();
```

#### Al superarla
Al tercer click, el botón se apaga y dice *Fin del programa*. Los otros tres clicks no hacen nada, y está bien que no hagan nada. Nova suspira, aliviada. —Ahora sé cuándo termina.

#### Imagen
- Un botón de bronce apagado y una placa de luz que se enciende al lado, en el tablero de la mesa larga.
- Nova, aliviada, con la mano en el pecho.

### Micro-misión S04-N04-P4 · Correr y pausar

```meta
lugar: El Taller de los Títeres, la mesa larga
personajes: Nima, Gheco, Nova
carta: setInterval | reloj = setInterval(() => { if (m.terminado) parar(); else { m.paso(); dibujar(); } }, 500)
recompensa: xp 15, monedas 5
```

#### Escena
Con programas largos, Nova se cansa de tocar. —Que corra solo, despacito, una orden cada medio segundo. Y si veo algo raro, que pueda **pausar**.

#### Gheco sugiere
`#correr` arranca un intervalo de 500 ms que da un paso y dibuja (cancelá antes el que hubiera). `#pausa` lo cancela. Cuando termina, el intervalo se cancela solo.

#### Desafío
Corre 1,2 segundos, se pausa 3 segundos (no avanza), vuelve a correr hasta terminar. Al final no tiene que quedar ningún temporizador.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #0d1117; color: #c9d1d9; padding: 12px; }
</style>
<button id="correr">Correr ⏵</button> <button id="pausa">Pausa ⏸</button>
<p>AX = <span id="AX"></span> · orden <span id="ip"></span></p>
```

#### Archivos
maquina.js
```javascript
export const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

export class Maquina {
  constructor(texto) {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
    this.ip = 0;
    this.lineas = texto.split('\n').map((renglon) => renglon.trim()).filter(Boolean).map((texto) => {
      const [op, destino, fuente] = texto.toUpperCase().split(/[\s,]+/);
      return { texto, op, destino, fuente };
    });
  }

  get terminado() {
    return this.ip >= this.lineas.length;
  }

  paso() {
    if (this.terminado) return;
    const { op, destino, fuente } = this.lineas[this.ip++];
    if (op === 'MOV') this.registros[destino] = Number(fuente) & 0xFFFF;
    if (op === 'INC') this.registros[destino] = (this.registros[destino] + 1) & 0xFFFF;
  }
}
```

#### Eventos
```
click #correr
esperar 1200
click #pausa
esperar 3000
click #correr
esperar 5000
```

#### Estado
```
#AX
#ip
temporizadores
```

#### Código inicial
```javascript
import { Maquina, hex } from './maquina.js';

const m = new Maquina('MOV AX, 1\nINC AX\nINC AX\nINC AX\nINC AX\nINC AX');
let reloj = null;

function dibujar() {
  document.querySelector('#AX').textContent = hex(m.registros.AX);
  document.querySelector('#ip').textContent = m.terminado ? 'fin' : m.ip + 1;
}

document.querySelector('#correr').addEventListener('click', () => {
  reloj = setInterval(() => {
    m.paso();
    dibujar();
  }, 500);
});
dibujar();
```

#### Salida esperada
```
── Estado ──
#AX: 0006
#ip: fin
temporizadores: 0
```

#### Solución
```javascript
import { Maquina, hex } from './maquina.js';

const m = new Maquina('MOV AX, 1\nINC AX\nINC AX\nINC AX\nINC AX\nINC AX');
let reloj = null;

function dibujar() {
  document.querySelector('#AX').textContent = hex(m.registros.AX);
  document.querySelector('#ip').textContent = m.terminado ? 'fin' : m.ip + 1;
}

function parar() {
  clearInterval(reloj);
  reloj = null;
}

document.querySelector('#correr').addEventListener('click', () => {
  parar();
  reloj = setInterval(() => {
    if (m.terminado) {
      parar();
      return;
    }
    m.paso();
    dibujar();
  }, 500);
});
document.querySelector('#pausa').addEventListener('click', parar);
dibujar();
```

#### Al superarla
El programa corre despacio, se queda quieto mientras Nova piensa, y sigue cuando ella quiere. Al terminar, el reloj se apaga solo. Nova lo deja correr tres veces seguidas, mirando.

#### Imagen
- Un reloj de arena de bronce y cristal al lado del tablero, con la arena cian cayendo despacio.
- Nova con la mano levantada sobre un botón de pausa, atenta.

### Micro-misión S04-N04-P5 · Jefe: donde se trabó la Herrumbre

```meta
lugar: Las Forjas, adentro de Axón, con el tablero de la Feria
personajes: Nima, Gheco, Nova, Axón, la Herrumbre
carta: El paso a paso completo | dibujar() desde el estado · Paso · Correr/Pausa · Reiniciar · errores en #error sin romper
recompensa: xp 50, oro 50, monedas 1
```

#### Escena
Nima baja con Nova por las chimeneas hasta el pecho de Axón, con el tablero de la mesa larga bajo el brazo. Adentro, la **Herrumbre** es una mancha roja, viva, que se arrastra por las palancas y se come el bronce. El programa del Gólem se trabó en algún lado.

—Con el paso a paso —dice Gheco— vemos dónde se trabó.

#### Gheco sugiere
Juntá todo en el tablero:
- `dibujar()` muestra los cuatro registros, `ZF`, la orden actual (`li.actual`) y deshabilita `#paso` y `#correr` si terminó;
- `#paso` da un paso; `#correr` corre cada 300 ms; `#pausa` frena;
- `#reiniciar` frena y crea una máquina nueva con el mismo programa;
- si `paso()` tira un error (la Herrumbre), frená el reloj, mostrá el mensaje en `#error` y dejá todo como quedó, para que se vea **dónde** se trabó.

#### Desafío
Nova prueba los botones: corre un poco, pausa, reinicia y da un paso a mano. Después lo deja correr solo hasta que se traba: tiene que verse **dónde**.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #1a0f08; color: #f0d9b5; padding: 12px; }
  td, th { border: 1px solid #6b4a2a; padding: 3px 8px; font-family: monospace; }
  th { color: #3dd6f5; }
  ol { font-family: monospace; } li.actual { background: #3dd6f5; color: #1a0f08; }
  #error { color: #ff6b4a; font-weight: bold; }
</style>
<div>
  <button id="paso">Paso ▶</button> <button id="correr">Correr ⏵</button>
  <button id="pausa">Pausa ⏸</button> <button id="reiniciar">Reiniciar ⟲</button>
</div>
<table><tr><th>AX</th><td id="AX"></td><th>BX</th><td id="BX"></td><th>CX</th><td id="CX"></td><th>DX</th><td id="DX"></td><th>ZF</th><td id="ZF"></td></tr></table>
<ol id="programa"></ol>
<p id="error"></p>
```

#### Archivos
maquina.js
```javascript
export const hex = (n) => n.toString(16).toUpperCase().padStart(4, '0');

export class Maquina {
  constructor(texto) {
    this.registros = { AX: 0, BX: 0, CX: 0, DX: 0 };
    this.zf = false;
    this.ip = 0;
    this.pasos = 0;
    this.lineas = [];
    this.etiquetas = {};
    texto.split('\n').forEach((renglon, i) => {
      const limpio = renglon.split(';')[0].trim();
      if (limpio === '') return;
      if (limpio.endsWith(':')) {
        this.etiquetas[limpio.slice(0, -1).toUpperCase()] = this.lineas.length;
        return;
      }
      const [op, destino, fuente] = limpio.toUpperCase().split(/[\s,]+/);
      this.lineas.push({ numero: i + 1, texto: limpio, op, destino, fuente });
    });
  }

  get terminado() {
    return this.ip >= this.lineas.length;
  }

  valor(o) {
    if (o in this.registros) return this.registros[o];
    if (/^[0-9A-F]+H$/.test(o)) return parseInt(o.slice(0, -1), 16);
    if (/^\d+$/.test(o)) return Number(o);
    throw new Error(`no entiendo «${o}»`);
  }

  cuenta(destino, n) {
    if (!(destino in this.registros)) throw new Error(`no hay palanca «${destino}»`);
    this.registros[destino] = n & 0xFFFF;
    this.zf = this.registros[destino] === 0;
  }

  saltar(etiqueta) {
    if (!(etiqueta in this.etiquetas)) throw new Error(`no hay ninguna etiqueta «${etiqueta}»`);
    this.ip = this.etiquetas[etiqueta];
  }

  paso() {
    if (this.terminado) return;
    const { numero, op, destino, fuente } = this.lineas[this.ip];
    this.ip++;
    this.pasos++;
    try {
      switch (op) {
        case 'MOV':
          if (!(destino in this.registros)) throw new Error(`no hay palanca «${destino}»`);
          this.registros[destino] = this.valor(fuente) & 0xFFFF;
          break;
        case 'ADD': this.cuenta(destino, this.registros[destino] + this.valor(fuente)); break;
        case 'SUB': this.cuenta(destino, this.registros[destino] - this.valor(fuente)); break;
        case 'INC': this.cuenta(destino, this.registros[destino] + 1); break;
        case 'DEC': this.cuenta(destino, this.registros[destino] - 1); break;
        case 'CMP': this.zf = ((this.valor(destino) - this.valor(fuente)) & 0xFFFF) === 0; break;
        case 'JMP': this.saltar(destino); break;
        case 'JZ': case 'JE': if (this.zf) this.saltar(destino); break;
        case 'JNZ': case 'JNE': if (!this.zf) this.saltar(destino); break;
        default: throw new Error(`no conozco «${op}»`);
      }
    } catch (error) {
      this.ip--;
      throw new Error(`Línea ${numero}: ${error.message}`);
    }
  }
}
```

#### Eventos
```
click #correr
esperar 900
click #pausa
click #reiniciar
click #paso
click #correr
esperar 6000
```

#### Estado
```
#error
td
li.actual
#paso @disabled
temporizadores
```

#### Código inicial
```javascript
import { Maquina, hex } from './maquina.js';

const PROGRAMA = `MOV CX, 3      ; tres vueltas
MOV AX, 0
vuelta:
ADD AX, 0Ah    ; diez por vuelta
DEC CX
JNZ vuelta
MOV BX, AX
MOV EX, 1      ; acá se metió la Herrumbre
MOV DX, 1`;

let m = new Maquina(PROGRAMA);
let reloj = null;
const lista = document.querySelector('#programa');

function dibujar() {
  for (const r of ['AX', 'BX', 'CX', 'DX']) document.querySelector(`#${r}`).textContent = hex(m.registros[r]);
}

dibujar();
```

#### Salida esperada
```
── Estado ──
#error: Línea 8: no hay palanca «EX»
td: 001E
td: 001E
td: 0000
td: 0000
td: 1
li.actual: MOV EX, 1
#paso @disabled: no
temporizadores: 0
```

#### Solución
```javascript
import { Maquina, hex } from './maquina.js';

const PROGRAMA = `MOV CX, 3      ; tres vueltas
MOV AX, 0
vuelta:
ADD AX, 0Ah    ; diez por vuelta
DEC CX
JNZ vuelta
MOV BX, AX
MOV EX, 1      ; acá se metió la Herrumbre
MOV DX, 1`;

let m = new Maquina(PROGRAMA);
let reloj = null;
const lista = document.querySelector('#programa');
const error = document.querySelector('#error');

function dibujar() {
  for (const r of ['AX', 'BX', 'CX', 'DX']) document.querySelector(`#${r}`).textContent = hex(m.registros[r]);
  document.querySelector('#ZF').textContent = m.zf ? '1' : '0';
  lista.replaceChildren(...m.lineas.map((linea, i) => {
    const li = document.createElement('li');
    li.textContent = linea.texto;
    li.classList.toggle('actual', i === m.ip);
    return li;
  }));
  document.querySelector('#paso').disabled = m.terminado;
  document.querySelector('#correr').disabled = m.terminado;
}

function parar() {
  clearInterval(reloj);
  reloj = null;
}

function avanzar() {
  try {
    m.paso();
  } catch (e) {
    parar();
    error.textContent = e.message;
  }
  if (m.terminado) parar();
  dibujar();
}

document.querySelector('#paso').addEventListener('click', avanzar);
document.querySelector('#correr').addEventListener('click', () => {
  parar();
  reloj = setInterval(avanzar, 300);
});
document.querySelector('#pausa').addEventListener('click', parar);
document.querySelector('#reiniciar').addEventListener('click', () => {
  parar();
  m = new Maquina(PROGRAMA);
  error.textContent = '';
  dibujar();
});

dibujar();
```

#### Al superarla
El programa corre solo: tres vueltas, `AX` en `001E`, `BX` en `001E`… y se frena en seco. En rojo: *Línea 8: no hay palanca «EX»*. La franja cian quedó **justo ahí**, sobre la orden donde se metió la Herrumbre.

Nova la ve. Escribe la orden bien (`MOV DX, 1`), y la Herrumbre, que solo vive en lo que nadie mira, se seca y se cae en escamas al piso del Gólem. Axón mueve un dedo, después la mano entera, y abre el ojo de cristal.

*«Correcto»*, dice. Y después, por primera vez en siglos, dice otra palabra: *«Gracias.»*

Nova se lleva el tablero de práctica a su núcleo. —Lo voy a usar todos los días —le dice a Nima—. Y la próxima flecha que tires por las chimeneas… avisame antes.

#### Imagen
- Adentro del pecho del Gólem de Bronce: pasillos de palancas, y una mancha roja de herrumbre que se seca y cae en escamas.
- Nova (chica flotante de capa oscura con circuitos cian y pelo dorado) sostiene el tablero de práctica con una franja cian sobre un renglón; Nima apunta al renglón; el ojo de cristal de Axón, enorme, se enciende en cian al fondo.
