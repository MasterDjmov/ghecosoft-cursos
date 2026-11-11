# RAMA R01 · Los Puestos de Juegos: los fundamentos

```meta
tipo: tronco
posicion: 1
```

## R01-N01 · Variables y template literals

```meta
tipo: tema
padre: R00-N01
precio: 10
criatura: skeleton
temas: prog.variables, prog.salida
```

### Crónica

Con el cartel en *Abierto*, la Feria se llena de gente. En el puesto de tiro, dos chicos, **Bruno y Tati**, llevan la cuenta de los tiros en una pizarra, borrando y volviendo a escribir con tiza. Se equivocan todo el tiempo.

—Así no —dice {mentor}, posándose en la pizarra—. Cada dato necesita una **cajita con nombre**. Algunas cajitas se pueden abrir y cambiar; otras se sellan para siempre. En la Feria las llamamos `let` y `const`.

### Objetivos

- Guardar datos en variables con `let` y `const`, y saber cuándo usar cada una.
- Elegir buenos nombres (camelCase).
- Cambiar el valor de una variable y usar `+=`.
- Armar textos con template literals: `` `Hola, ${nombre}` ``.

### Antes de empezar

- La Clase 0: `console.log`, textos y números.

### Explicación

#### Una cajita con nombre
```javascript
const nombre = 'Nima';   // const: no se puede cambiar
let fichas = 3;          // let: se puede cambiar
fichas = 5;              // ahora vale 5
```
- `const` **sella** la cajita: si intentás cambiarla, JavaScript se queja (`Assignment to constant variable`).
- `let` deja cambiarla todas las veces que quieras.
- **Regla de la Feria:** usá `const` siempre, y `let` solo cuando el valor tenga que cambiar.
- (Vas a ver también `var` en código viejo: no lo uses. Más adelante vas a ver por qué.)

#### Nombres
- Pueden tener letras, números, `_` y `$`, pero no empezar con un número.
- Se escriben en **camelCase**: `fichasGanadas`, `precioPorTiro`.
- Las mayúsculas cuentan: `fichas` y `Fichas` son dos cajitas distintas.

#### Cambiar un valor
```javascript
let tiros = 0;
tiros = tiros + 1;   // 1
tiros += 2;          // 3 (es lo mismo que tiros = tiros + 2)
tiros++;             // 4 (suma uno)
```

#### Template literals
Con comillas invertidas (`` ` ``, en el teclado al lado de la tecla Enter o con Alt Gr + }), podés meter valores adentro del texto con `${…}`:
```javascript
const puesto = 'Tiro al blanco';
const precio = 2;
console.log(`El puesto ${puesto} cuesta ${precio} fichas`);
console.log(`Tres tiros cuestan ${precio * 3} fichas`);
```
Adentro de `${…}` puede ir cualquier cuenta. Es mucho más cómodo que pegar con `+`.

### Código de ejemplo

```javascript
const arquera = 'Nima';
const puesto = 'Tiro al blanco';
let fichas = 3;
let tiros = 0;

console.log(`${arquera} llega al puesto ${puesto} con ${fichas} fichas.`);

// Cada tiro cuesta una ficha
tiros++;
fichas -= 1;
tiros++;
fichas -= 1;

console.log(`Tiros: ${tiros} · Fichas que quedan: ${fichas}`);
console.log(`Si gana el premio doble, se lleva ${fichas * 2} fichas.`);
```

### Salida esperada

```
Nima llega al puesto Tiro al blanco con 3 fichas.
Tiros: 2 · Fichas que quedan: 1
Si gana el premio doble, se lleva 2 fichas.
```

### ¿Para qué sirve?

Todo programa guarda datos: el puntaje de un juego, el nombre de quien entró, el total de un carrito. Las variables son la memoria del programa, y los template literals la forma de mostrarla con prolijidad.

### Errores habituales

**Ogro: cambiar una `const`.**
```
TypeError: Assignment to constant variable.
```
Si el valor tiene que cambiar, declarala con `let`.

**Esqueleto: usar una variable antes de declararla, o con otra mayúscula.**
```
ReferenceError: Fichas is not defined
```

**Slime: declarar dos veces.** `let fichas = 1;` y más abajo `let fichas = 2;` da `Identifier 'fichas' has already been declared`. La segunda vez va sin `let`: `fichas = 2;`.

**Comillas comunes en vez de invertidas.** `'Tengo ${fichas} fichas'` muestra literalmente `${fichas}`: el `${…}` solo funciona entre comillas invertidas.

### Micro-misión R01-N01-P1 · Cajitas con nombre

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Bruno, Tati
carta: Variables | const nombre = 'Nima'; · let fichas = 3; · const no cambia, let sí
recompensa: xp 10, oro 10
```

#### Escena
Bruno le pide a Nima su nombre y cuántas fichas tiene, para anotarla en la pizarra. Tati, que es la que borra, le pide por favor que el nombre «no se borre nunca».

#### Gheco sugiere
Una **variable** es una cajita con nombre donde el programa guarda un dato para usarlo después. En JavaScript hay dos formas de crearla:

- `const` para lo que **no cambia**: `const nombre = 'Nima';`
- `let` para lo que **sí cambia**: `let fichas = 10;`

El `=` no es «igual» como en matemática: quiere decir «guardá esto en la cajita». Después, `console.log(fichas)` muestra lo que hay adentro.

#### Desafío
Creá la constante `nombre` con el texto `Nima` y la variable `fichas` con el número `3`.

#### Código inicial
```javascript
// Creá nombre y fichas acá


console.log('Jugadora:', nombre);
console.log('Fichas:', fichas);
```

#### Salida esperada
```
Jugadora: Nima
Fichas: 3
```

#### Solución
```javascript
const nombre = 'Nima';
let fichas = 3;

console.log('Jugadora:', nombre);
console.log('Fichas:', fichas);
```

#### Al superarla
Tati escribe *NIMA* en letras grandes y le pasa un trapo por arriba para probar: no se borra. —¡Es una const! —dice, contentísima.

#### Imagen
- Un puesto de tiro de feria de noche, con una pizarra negra sin letras y tizas de colores.
- Bruno (chico de 12, pelo rizado, gorra al revés, chaleco rojo) y Tati (chica de 11, dos colitas, delantal amarillo) con tizas en la mano.
- Nima (muchacha de 17, trenza negra alta con hilo amarillo, chaqueta corta de cuero negro cerrada con costuras amarillas, arco verde en la espalda) les habla; Gheco en su hombro.

### Micro-misión R01-N01-P2 · Una ficha menos

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Bruno
carta: Cambiar valores | fichas = fichas - 1 · fichas -= 1 · tiros++ suma uno
recompensa: xp 10, oro 10
```

#### Escena
Cada tiro cuesta una ficha. Nima tira dos veces y Bruno tiene que actualizar la pizarra.

#### Gheco sugiere
Hay atajos para cambiar una variable usando su propio valor:

- `tiros++` suma 1;
- `fichas -= 1` resta 1 (es lo mismo que `fichas = fichas - 1`);
- también existen `+=`, `*=` y `--`.

#### Desafío
Después de los dos tiros, `tiros` tiene que valer 2 y `fichas` tiene que valer 1.

#### Código inicial
```javascript
let fichas = 3;
let tiros = 0;

// Primer tiro

// Segundo tiro

console.log(`Tiros: ${tiros}`);
console.log(`Fichas: ${fichas}`);
```

#### Salida esperada
```
Tiros: 2
Fichas: 1
```

#### Solución
```javascript
let fichas = 3;
let tiros = 0;

// Primer tiro
tiros++;
fichas -= 1;
// Segundo tiro
tiros++;
fichas -= 1;

console.log(`Tiros: ${tiros}`);
console.log(`Fichas: ${fichas}`);
```

#### Al superarla
Bruno borra el 3, escribe un 1 y dibuja dos rayitas al lado: los dos tiros. La cuenta, por primera vez, está bien.

#### Imagen
- Primer plano de la pizarra del puesto de tiro con rayitas de tiza y un trapo, sin letras ni números.
- La mano de Bruno (chaleco rojo) borra con el trapo; atrás, Nima apunta con el arco verde a un blanco de paja.

### Micro-misión R01-N01-P3 · El esqueleto de la const

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Tati
criatura: ogre
carta: const o let | si el valor cambia, let · Assignment to constant variable = quisiste cambiar una const
recompensa: xp 10, oro 10
```

#### Escena
Tati sella todas las cajitas, «por las dudas». Ahora, cuando Nima gana un premio, el programa explota con un error rojo.

#### Gheco sugiere
Una cajita `const` no se puede cambiar: si el programa lo intenta, JavaScript corta con el error `Assignment to constant variable` («le asignaste algo a una constante»).

Fijate cuál de las dos cajitas tiene que poder cambiar, y creala con `let`.

#### Desafío
Arreglá la declaración que corresponde para que el programa ande.

#### Código inicial
```javascript
const nombre = 'Nima';
const premios = 0;

premios = premios + 1;
console.log(`${nombre} ganó ${premios} premio`);
```

#### Salida esperada
```
Nima ganó 1 premio
```

#### Solución
```javascript
const nombre = 'Nima';
let premios = 0;

premios = premios + 1;
console.log(`${nombre} ganó ${premios} premio`);
```

#### Al superarla
—Entonces no todo se sella —dice Tati, un poco desilusionada—. Solo lo que no va a cambiar nunca.

#### Imagen
- Un ogro chiquito y torpe de feria (sin armas), atascado tratando de abrir un cajón cerrado con candado amarillo.
- Tati (chica de 11, dos colitas, delantal amarillo) le saca el candado al cajón con cara de culpa.
- Gheco señalando el candado.

### Micro-misión R01-N01-P4 · El cartel con huecos

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Bruno
carta: Template literals | `Hola, ${nombre}` · comillas invertidas · adentro de ${…} puede ir una cuenta
recompensa: xp 10, oro 10
```

#### Escena
Bruno quiere colgar un cartel con el precio de los tiros, pero cada vez que cambia el precio tiene que rehacer todo el cartel.

#### Gheco sugiere
Para meter valores adentro de un texto, se usan **comillas invertidas** (`` ` ``, la tecla al lado del 1 o con AltGr + }) y `${ }`:

```js
const precio = 4;
console.log(`Cuesta ${precio} fichas, y tres cuestan ${precio * 3}`);
```

Lo que va entre `${ }` se calcula y se mete en el texto. Se llama **plantilla de texto** (*template literal*).

#### Desafío
Completá los dos carteles usando `${…}` con las variables `puesto` y `precio`.

#### Código inicial
```javascript
const puesto = 'Tiro al blanco';
const precio = 2;

console.log(`Puesto: ___`);
console.log(`Tres tiros: ___ fichas`);
```

#### Salida esperada
```
Puesto: Tiro al blanco
Tres tiros: 6 fichas
```

#### Solución
```javascript
const puesto = 'Tiro al blanco';
const precio = 2;

console.log(`Puesto: ${puesto}`);
console.log(`Tres tiros: ${precio * 3} fichas`);
```

#### Al superarla
Ahora Bruno cambia el precio en un solo lugar y el cartel se arregla solo. Lo cambia cinco veces seguidas, nada más que para verlo.

#### Imagen
- Un cartel de madera de feria con un borde de foquitos amarillos y huecos vacíos donde van los números (sin texto legible).
- Bruno (chico de 12, gorra al revés, chaleco rojo) lo cuelga parado en un banquito; Nima le sostiene el banquito.

### Micro-misión R01-N01-P5 · La pizarra del puesto

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Bruno, Tati
carta: Repaso | const para lo fijo · let para lo que cambia · += y -= · `${…}` en el texto
recompensa: xp 15, monedas 5
```

#### Escena
Se termina la ronda. Bruno y Tati quieren pasar la pizarra en limpio: quién jugó, cuántos tiros hizo, cuántos acertó y cuántas fichas ganó.

#### Gheco sugiere
Cada acierto paga 3 fichas. Calculá las fichas ganadas a partir de los aciertos, con una cuenta (`aciertos * 3`), no escribiendo el resultado a mano: así, si cambian los aciertos, el resultado cambia solo.

#### Desafío
Nima hizo 5 tiros y acertó 4. Guardá esos datos y mostrá la pizarra **exactamente** así (las fichas son los aciertos por 3):
- `Jugadora: Nima`
- `Tiros: 5`
- `Aciertos: 4`
- `Fichas ganadas: 12`

#### Código inicial
```javascript
const jugadora = 'Nima';
// Guardá los tiros y los aciertos, y calculá las fichas

```

#### Salida esperada
```
Jugadora: Nima
Tiros: 5
Aciertos: 4
Fichas ganadas: 12
```

#### Solución
```javascript
const jugadora = 'Nima';
const tiros = 5;
const aciertos = 4;
const fichasGanadas = aciertos * 3;

console.log(`Jugadora: ${jugadora}`);
console.log(`Tiros: ${tiros}`);
console.log(`Aciertos: ${aciertos}`);
console.log(`Fichas ganadas: ${fichasGanadas}`);
```

#### Al superarla
Tati copia la pizarra en un papel y lo clava en el poste del puesto. —La mejor de la noche —anuncia. Bruno, que había jugado antes, se hace el que no escuchó.

#### Imagen
- Un papel clavado en un poste de madera de feria con una lista escrita a mano (sin letras legibles) y una ficha de bronce colgando.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) sonríe con el arco al hombro; Tati aplaude; Bruno mira para otro lado.

### Micro-misión R01-N01-P6 · Ronda tras ronda

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Bruno
carta: Acumular | let total = 0; · total += lo de cada ronda · al final, total tiene la suma
recompensa: xp 15, monedas 5
```

#### Escena
Nima juega tres rondas. En la primera gana 6 fichas, en la segunda 3 y en la tercera 9. Bruno quiere un número que vaya **juntando** todo.

#### Gheco sugiere
Un **acumulador** es una variable que va sumando: empezá con `let total = 0;` y, después de cada ronda, `total += fichasDeLaRonda;`.

Mostrá el total parcial después de cada ronda.

#### Desafío
Acumulá las fichas de las tres rondas (6, 3 y 9) y mostrá el total parcial después de cada una, así:
- `Ronda 1: 6`
- `Ronda 2: 9`
- `Ronda 3: 18`

#### Código inicial
```javascript
let total = 0;

```

#### Salida esperada
```
Ronda 1: 6
Ronda 2: 9
Ronda 3: 18
```

#### Solución
```javascript
let total = 0;

total += 6;
console.log(`Ronda 1: ${total}`);
total += 3;
console.log(`Ronda 2: ${total}`);
total += 9;
console.log(`Ronda 3: ${total}`);
```

#### Al superarla
Dieciocho fichas de bronce suenan en el bolsillo de Nima. Lumina, desde un farol, hace un guiño de luz: ya alcanza para abrir el próximo puesto.

#### Imagen
- Una pila de fichas de bronce de feria sobre un mostrador de madera, a la luz amarilla de un farol.
- La mano de Nima (guante de arquera) junta las fichas; Lumina (luciérnaga enorme con alas de vidrio) mira desde un farol.

## R01-N02 · Tipos y la coerción del Goblin

```meta
tipo: tema
padre: R01-N01
precio: 10
criatura: goblin
temas: prog.variables, prog.operadores
```

### Crónica

En el puesto de las balanzas, un **goblin** de orejas puntiagudas atiende con una sonrisa enorme. Cobra «2 más 2» y le da «22». Cobra «5 menos "dos"» y le da `NaN`, una moneda que no vale nada. La gente le paga sin entender por qué.

—El Goblin de la Coerción —dice {mentor}, en voz baja—. Hace trampa con los **tipos**: mezcla textos con números y nadie se da cuenta. En la Feria, quien no sabe de qué tipo es cada cosa, pierde las fichas.

### Objetivos

- Conocer los tipos de JavaScript: `number`, `string`, `boolean`, `undefined`, `null` (y los objetos).
- Usar `typeof` para saber el tipo de un valor.
- Entender la coerción: `"2" + 2` da `"22"` y `"2" * 2` da `4`.
- Convertir a propósito con `Number()` y `String()`, y reconocer `NaN`.
- Comparar con `===` y no con `==`.

### Antes de empezar

- R01-N01: variables y template literals.

### Explicación

#### Los tipos
| Tipo | Ejemplos | `typeof` |
|---|---|---|
| número | `3`, `2.5`, `-1`, `NaN` | `'number'` |
| texto | `'Nima'`, `"22"`, `` `hola` `` | `'string'` |
| lógico | `true`, `false` | `'boolean'` |
| sin valor | `undefined` (nunca se le dio uno) | `'undefined'` |
| vacío a propósito | `null` (se le dio «nada») | `'object'` (un error histórico) |

#### La coerción: el truco del Goblin
JavaScript **convierte tipos solo**, sin avisar:
```javascript
console.log('2' + 2);   // '22': con un texto, + PEGA
console.log('2' * 2);   // 4: * no sabe pegar, así que convierte a número
console.log('5' - 'dos'); // NaN: «dos» no se puede convertir
```
El `+` es el más tramposo: si alguno de los dos es texto, une en vez de sumar.

#### Convertir a propósito
```javascript
const precio = Number('2');    // 2
const texto = String(15);      // '15'
const raro = Number('dos');    // NaN («Not a Number»)
console.log(Number.isNaN(raro)); // true
```
`NaN` es un número que significa «esto no es un número». Es tan raro que `NaN === NaN` da `false`: por eso se pregunta con `Number.isNaN(…)`.

#### `===` contra `==`
```javascript
console.log(2 == '2');   // true: == convierte antes de comparar
console.log(2 === '2');  // false: === compara tipo Y valor
```
**Regla de la Feria:** usá siempre `===` y `!==`. El `==` es la balanza del Goblin.

### Código de ejemplo

```javascript
const fichas = 2;
const fichasDelCartel = '2';

console.log(typeof fichas, typeof fichasDelCartel);
console.log('Con +:', fichas + fichasDelCartel);
console.log('Convirtiendo:', fichas + Number(fichasDelCartel));
console.log('== dice', fichas == fichasDelCartel, 'y === dice', fichas === fichasDelCartel);

const moneda = Number('dos');
console.log('La moneda del Goblin vale', moneda, '¿es NaN?', Number.isNaN(moneda));

let premio;
console.log('Premio sin valor:', premio, '·', typeof premio);
```

### Salida esperada

```
number string
Con +: 22
Convirtiendo: 4
== dice true y === dice false
La moneda del Goblin vale NaN ¿es NaN? true
Premio sin valor: undefined · undefined
```

### ¿Para qué sirve?

Todo lo que llega de afuera (lo que escribe alguien en un formulario, lo que guarda `localStorage`, lo que manda un servidor) llega como **texto**. Si lo sumás sin convertirlo, el Goblin te cobra de más. Saber el tipo de cada dato evita la mitad de los errores de JavaScript.

### Errores habituales

**Goblin: sumar textos que parecen números.** `'10' + 5` da `'105'`. Convertí antes: `Number('10') + 5`.

**Goblin: comparar con `==`.** `0 == ''` da `true` y `null == undefined` da `true`. Con `===` no hay sorpresas.

**Goblin: preguntar `x === NaN`.** Siempre da `false`. Usá `Number.isNaN(x)`.

**Esqueleto: `undefined` por olvido.** Una variable declarada sin valor (`let premio;`) vale `undefined` hasta que le des uno.

### Micro-misión R01-N02-P1 · ¿De qué tipo es?

```meta
lugar: El puesto de las balanzas
personajes: Nima, Gheco
carta: typeof | typeof 3 → 'number' · typeof 'hola' → 'string' · typeof true → 'boolean'
recompensa: xp 10, oro 10
```

#### Escena
Sobre el mostrador del Goblin hay tres cosas: una ficha, un cartel y una lamparita. Gheco quiere saber de qué tipo es cada una antes de tocar nada.

#### Gheco sugiere
Cada valor tiene un **tipo**, que dice qué clase de dato es:

- `number`: números (con o sin decimales);
- `string`: texto, entre comillas;
- `boolean`: verdadero o falso, `true` o `false`;
- `undefined`: «todavía no tiene valor».

`typeof valor` devuelve el tipo como texto: `typeof 5` da `'number'`.

#### Desafío
Mostrá el tipo de cada una de las tres variables, una por línea.

#### Código inicial
```javascript
const ficha = 5;
const cartel = 'Balanzas';
const prendida = true;

console.log(___);
console.log(___);
console.log(___);
```

#### Salida esperada
```
number
string
boolean
```

#### Solución
```javascript
const ficha = 5;
const cartel = 'Balanzas';
const prendida = true;

console.log(typeof ficha);
console.log(typeof cartel);
console.log(typeof prendida);
```

#### Al superarla
Gheco anota los tres tipos en la palma de la mano de Nima, con tinta de luz: *number, string, boolean*. —Por las dudas —dice.

#### Imagen
- Un mostrador de feria con una balanza de bronce de dos platos, una ficha de bronce, un cartelito de madera y una lamparita, de noche.
- Gheco (gecko de luz cian con antiparras) sobre la balanza, mirando todo con una lupa.

### Micro-misión R01-N02-P2 · El 22 del Goblin

```meta
lugar: El puesto de las balanzas
personajes: Nima, Gheco, el Goblin de la Coerción
criatura: goblin
carta: Convertir | Number('2') → 2 · con un texto, + pega · convertí antes de sumar
recompensa: xp 10, oro 10
```

#### Escena
El Goblin pesa dos bolsas de fichas: una dice «2» en un cartel de papel y la otra tiene 2 fichas de verdad. —¡Veintidós! —anuncia, y estira la mano.

#### Gheco sugiere
Un número entre comillas es **texto**, y con texto `+` no suma: **pega**. `'20' + 2` da `'202'`.

Para sumar, primero convertí el texto a número con `Number(...)`: `Number('20') + 2` da `22`.

#### Desafío
Hacé que el total sea 4, convirtiendo el cartel a número.

#### Código inicial
```javascript
const delCartel = '2';
const fichas = 2;

const total = delCartel + fichas;
console.log('Total:', total);
```

#### Salida esperada
```
Total: 4
```

#### Solución
```javascript
const delCartel = '2';
const fichas = 2;

const total = Number(delCartel) + fichas;
console.log('Total:', total);
```

#### Al superarla
—¡Cuatro! —dice Nima, y le deja exactamente cuatro fichas. El Goblin cuenta tres veces, refunfuña y las guarda.

#### Imagen
- Un goblin de feria (orejas puntiagudas, sonrisa enorme, chaleco a rayas, sin armas) detrás de una balanza de bronce con dos bolsas.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) pone cuatro fichas de bronce en el mostrador con firmeza.

### Micro-misión R01-N02-P3 · La balanza tramposa

```meta
lugar: El puesto de las balanzas
personajes: Nima, Gheco, el Goblin de la Coerción
criatura: goblin
carta: === | compara tipo y valor · 2 === '2' es false · usá siempre === y !==
recompensa: xp 10, oro 10
```

#### Escena
El Goblin tiene una balanza que dice «iguales» aunque en un plato haya una ficha y en el otro un papel con un «1» escrito.

#### Gheco sugiere
JavaScript tiene dos formas de preguntar si dos cosas son iguales:

- `==` convierte los tipos antes de comparar: para él, `'5' == 5` es verdad;
- `===` no convierte: exige el mismo valor **y** el mismo tipo. `'5' === 5` es falso.

Usá siempre `===`: así nadie te engaña con un número disfrazado de texto.

#### Desafío
Hacé que la balanza diga `false`: la ficha y el papel **no** son lo mismo.

#### Código inicial
```javascript
const ficha = 1;
const papel = '1';

console.log('¿Son iguales?', ficha == papel);
```

#### Salida esperada
```
¿Son iguales? false
```

#### Solución
```javascript
const ficha = 1;
const papel = '1';

console.log('¿Son iguales?', ficha === papel);
```

#### Al superarla
La balanza se inclina hacia la ficha de verdad y el papel sale volando. El Goblin pone cara de no haber visto nada.

#### Imagen
- Una balanza de bronce de dos platos inclinada: de un lado una ficha de bronce y del otro un papelito que sale volando.
- El goblin de chaleco a rayas se tapa la cara; Gheco festeja arriba de la balanza.

### Micro-misión R01-N02-P4 · La moneda que no vale

```meta
lugar: El puesto de las balanzas
personajes: Nima, Gheco
criatura: goblin
carta: NaN | Number('dos') → NaN · NaN === NaN es false · preguntá con Number.isNaN(x)
recompensa: xp 10, oro 10
```

#### Escena
El Goblin le da a Nima el vuelto en una moneda gris que dice `NaN`. Nima quiere saber si vale algo, pero cuando la compara con otra moneda `NaN`, la balanza dice que no son iguales.

#### Gheco sugiere
Cuando una cuenta no da un número (por ejemplo, `Number('hola')`), JavaScript devuelve `NaN`: *Not a Number*, «no es un número».

`NaN` es raro: no es igual a nada, ni siquiera a sí mismo (`NaN === NaN` es falso). Para saber si un valor es `NaN`, usá `Number.isNaN(valor)`.

#### Desafío
Reemplazá la comparación por `Number.isNaN(vuelto)` para que diga `true`.

#### Código inicial
```javascript
const vuelto = Number('dos');

console.log('Vuelto:', vuelto);
console.log('¿Es NaN?', vuelto === NaN);
```

#### Salida esperada
```
Vuelto: NaN
¿Es NaN? true
```

#### Solución
```javascript
const vuelto = Number('dos');

console.log('Vuelto:', vuelto);
console.log('¿Es NaN?', Number.isNaN(vuelto));
```

#### Al superarla
Nima le devuelve la moneda gris al Goblin. —Esto no es un número. Quiero el vuelto en fichas.

#### Imagen
- Una moneda gris opaca y sin brillo en la palma enguantada de Nima, al lado de fichas de bronce que brillan.
- Atrás, el goblin de chaleco a rayas se rasca la cabeza.

### Micro-misión R01-N02-P5 · Las cuentas del Goblin

```meta
lugar: El puesto de las balanzas
personajes: Nima, Gheco, el Goblin de la Coerción
criatura: goblin
carta: Convertir todo | lo que llega en un cartel es texto · Number() a cada uno · después, la cuenta
recompensa: xp 15, monedas 5
```

#### Escena
El Goblin anota las compras del día en carteles de papel: todo es texto. Dice que la gente le debe `"3" + "4" + "5"` fichas, que según él son **345**.

#### Gheco sugiere
Convertí cada cartel con `Number(...)` antes de sumar. Mostrá primero la cuenta del Goblin (sumando los textos tal cual, que se pegan) y después la de verdad.

#### Desafío
Mostrá exactamente:
- `El Goblin dice: 345`
- `La verdad: 12`

#### Código inicial
```javascript
const a = '3';
const b = '4';
const c = '5';

console.log('El Goblin dice:', a + b + c);
// Mostrá la verdad
```

#### Salida esperada
```
El Goblin dice: 345
La verdad: 12
```

#### Solución
```javascript
const a = '3';
const b = '4';
const c = '5';

console.log('El Goblin dice:', a + b + c);
console.log('La verdad:', Number(a) + Number(b) + Number(c));
```

#### Al superarla
La gente de la fila hace las cuentas de nuevo y le reclama al Goblin. Él devuelve las fichas de mala gana… y le anota a Nima una cruz en una libretita.

#### Imagen
- Una fila de gente de feria reclamando frente a un puesto de balanzas; carteles de papel con números tachados (sin texto legible).
- Nima, de brazos cruzados, al frente de la fila; el goblin anota algo en una libretita.

### Micro-misión R01-N02-P6 · undefined y null

```meta
lugar: El puesto de las balanzas
personajes: Nima, Gheco, Lumina
carta: undefined y null | let x; → undefined (nunca tuvo valor) · null = vacío a propósito · typeof null es 'object'
recompensa: xp 15, monedas 5
```

#### Escena
En el fondo del puesto hay dos cajas. Una nunca se abrió; la otra la vaciaron a propósito. Lumina le pide a Nima que les ponga la etiqueta correcta.

#### Gheco sugiere
Dos formas de decir «no hay nada»:

- `undefined`: una variable que se creó pero **todavía** no recibió valor (`let x;`);
- `null`: «vacía **a propósito**». Se la ponés vos cuando querés decir que no hay nada.

#### Desafío
Declará `cajaNueva` **sin valor** y `cajaVaciada` con `null`, para que el programa muestre lo que se espera.

#### Código inicial
```javascript
// Declará las dos cajas


console.log('Caja nueva:', cajaNueva, typeof cajaNueva);
console.log('Caja vaciada:', cajaVaciada, typeof cajaVaciada);
```

#### Salida esperada
```
Caja nueva: undefined undefined
Caja vaciada: null object
```

#### Solución
```javascript
let cajaNueva;
const cajaVaciada = null;

console.log('Caja nueva:', cajaNueva, typeof cajaNueva);
console.log('Caja vaciada:', cajaVaciada, typeof cajaVaciada);
```

#### Al superarla
—`null` dice *object* —se ríe Lumina—. Es un error viejo de la Feria. Nadie lo arregla porque se rompería todo lo demás.

#### Imagen
- Dos cajas de madera en el fondo de un puesto de feria: una cerrada con moño y polvo encima, la otra abierta y vacía.
- Lumina (luciérnaga enorme con alas de vidrio, luz amarilla en el pecho) ilumina las cajas; Nima pega una etiqueta en blanco.

## R01-N03 · Decisiones: if, switch, ?? y ?.

```meta
tipo: tema
padre: R01-N02
precio: 10
criatura: ogre
temas: prog.condicionales, prog.operadores
```

### Crónica

En la puerta de la **calesita** hay un guardia que deja pasar a unos sí y a otros no: a los que tienen ficha, a los que miden más de un metro, a los que vienen con alguien grande. Cada vez que alguien llega, el guardia **decide**.

—Un programa también decide —dice {mentor}—. Si pasa esto, hace aquello; si no, otra cosa. Y en la Feria hay dos trucos más: qué hacer cuando un dato no está (`??`) y cómo preguntar por algo que tal vez no existe (`?.`).

### Objetivos

- Decidir con `if`, `else if` y `else`.
- Combinar condiciones con `&&`, `||` y `!`.
- Elegir entre muchos casos con `switch`.
- Usar el operador ternario `condición ? a : b`.
- Dar un valor por defecto con `??` y preguntar sin romper con `?.`.
- Saber qué valores son «falsos» en JavaScript.

### Antes de empezar

- R01-N02: tipos y `===`.

### Explicación

#### if, else if, else
```javascript
const altura = 1.2;
if (altura >= 1.4) {
  console.log('Pasás a la montaña rusa');
} else if (altura >= 1) {
  console.log('Pasás a la calesita');
} else {
  console.log('Calesita con alguien grande');
}
```
Comparaciones: `===`, `!==`, `<`, `>`, `<=`, `>=`.

#### Varias condiciones
- `a && b`: las dos tienen que ser verdad.
- `a || b`: alcanza con una.
- `!a`: lo contrario.

#### Lo que cuenta como falso
En un `if`, estos valores cuentan como **falsos**: `false`, `0`, `''` (texto vacío), `null`, `undefined` y `NaN`. Todo lo demás es verdadero (¡incluso `'0'` y `[]`!).

#### switch
```javascript
switch (juego) {
  case 'tiro':
    console.log('2 fichas');
    break;
  case 'calesita':
    console.log('3 fichas');
    break;
  default:
    console.log('No existe ese juego');
}
```
Sin el `break`, sigue de largo al caso siguiente (un ogro clásico).

#### El ternario
```javascript
const mensaje = fichas > 0 ? 'Podés jugar' : 'Sin fichas';
```

#### `??`: el valor por defecto
```javascript
const nombre = apodo ?? 'Visitante';
```
Si `apodo` es `null` o `undefined`, usa `'Visitante'`. A diferencia de `||`, **no** reemplaza el `0` ni el `''`: `0 ?? 5` da `0`, pero `0 || 5` da `5`.

#### `?.`: preguntar sin romper
```javascript
const jugador = { nombre: 'Nima' };
console.log(jugador.premio?.nombre);   // undefined, sin error
```
Si lo de la izquierda es `null` o `undefined`, `?.` corta y devuelve `undefined` en vez de tirar `Cannot read properties of undefined`.

### Código de ejemplo

```javascript
const altura = 1.1;
const fichas = 2;
const conAlguienGrande = false;

if (fichas >= 3 && altura >= 1) {
  console.log('Pasás a la calesita');
} else if (fichas < 3) {
  console.log(`Te faltan ${3 - fichas} fichas`);
} else {
  console.log('Venís con alguien grande:', conAlguienGrande ? 'sí' : 'no');
}

const premios = 0;
console.log('Con ||:', premios || 'ninguno');
console.log('Con ??:', premios ?? 'ninguno');

const jugadora = { nombre: 'Nima' };
console.log('Su caballito:', jugadora.caballito?.color ?? 'todavía no eligió');
```

### Salida esperada

```
Te faltan 1 fichas
Con ||: ninguno
Con ??: 0
Su caballito: todavía no eligió
```

### ¿Para qué sirve?

Todo programa interesante decide: si la clave es correcta, entra; si el jugador perdió todas las vidas, termina el juego; si el servidor no mandó el dato, se muestra uno por defecto. `??` y `?.` son la forma moderna de no romperse cuando un dato falta.

### Errores habituales

**Ogro: un solo `=` en el `if`.** `if (fichas = 0)` **asigna** 0 (y da falso). Para comparar, `===`.

**Ogro: el `switch` sin `break`.** Se ejecutan también los casos de abajo.

**Ogro: `||` se come el cero.** `const vidas = guardadas || 3;` da 3 aunque hayas guardado 0. Usá `??`.

**Troll: leer una propiedad de algo que no está.** `jugador.premio.nombre` con `premio` vacío da `Cannot read properties of undefined (reading 'nombre')`. Usá `?.`.

### Micro-misión R01-N03-P1 · El guardia de la calesita

```meta
lugar: La calesita
personajes: Nima, Gheco
carta: if / else | if (condición) { … } else { … } · >= mayor o igual
recompensa: xp 10, oro 10
```

#### Escena
El guardia de la calesita deja pasar solo a quien tiene al menos 3 fichas. Nima tiene 5.

#### Gheco sugiere
Con `if` el programa **decide**: hace algo solo si una condición es verdad.

```js
if (edad >= 12) {
    console.log('Pasa');
} else {
    console.log('No pasa');
}
```

Lo que está en las primeras llaves se ejecuta si la condición se cumple; lo del `else` («si no»), si no se cumple. `>=` es «mayor o igual».

#### Desafío
Completá la condición para que muestre `Pasás a la calesita` si hay 3 fichas o más, y `Te faltan fichas` si no.

#### Código inicial
```javascript
const fichas = 5;

if (___) {
  console.log('Pasás a la calesita');
} else {
  console.log('Te faltan fichas');
}
```

#### Salida esperada
```
Pasás a la calesita
```

#### Solución
```javascript
const fichas = 5;

if (fichas >= 3) {
  console.log('Pasás a la calesita');
} else {
  console.log('Te faltan fichas');
}
```

#### Al superarla
El guardia levanta la soga roja y Nima sube a un caballito dorado. La calesita arranca con música de organito.

#### Imagen
- Una calesita de feria de noche, con caballitos dorados, espejos y foquitos amarillos, y una soga roja en la entrada.
- Un guardia grandote con gorra de feria levanta la soga; Nima (trenza negra con hilo amarillo, chaqueta de cuero negra, arco verde) pasa sonriendo.

### Micro-misión R01-N03-P2 · Tres caminos

```meta
lugar: La calesita
personajes: Nima, Gheco
carta: else if | if … else if … else · se elige el primero que se cumple · de mayor a menor
recompensa: xp 10, oro 10
```

#### Escena
En la calesita hay caballitos para tres alturas: los grandes (desde 1,5 m), los medianos (desde 1,1 m) y los chiquitos. Un nene de 1,2 m quiere saber cuál le toca.

#### Gheco sugiere
Con `else if` («si no, si…») agregás caminos en el medio:

```js
if (nota >= 9) { ... }
else if (nota >= 6) { ... }
else { ... }
```

JavaScript prueba **en orden** y entra solo en el primero que se cumple. Por eso, preguntá primero por el más alto: si no, el más fácil atrapa todo.

#### Desafío
Completá las condiciones para que a 1,2 m le toque el caballito mediano.

#### Código inicial
```javascript
const altura = 1.2;

if (___) {
  console.log('Caballito grande');
} else if (___) {
  console.log('Caballito mediano');
} else {
  console.log('Caballito chiquito');
}
```

#### Salida esperada
```
Caballito mediano
```

#### Solución
```javascript
const altura = 1.2;

if (altura >= 1.5) {
  console.log('Caballito grande');
} else if (altura >= 1.1) {
  console.log('Caballito mediano');
} else {
  console.log('Caballito chiquito');
}
```

#### Al superarla
El nene se sube a un caballito mediano color celeste y saluda cada vez que pasa frente a Nima.

#### Imagen
- La calesita girando de noche con caballitos de tres tamaños, uno celeste en primer plano con un nene saludando.
- Nima, abajo, devuelve el saludo con la mano enguantada.

### Micro-misión R01-N03-P3 · El precio de cada juego

```meta
lugar: La calesita
personajes: Nima, Gheco, Lumina
carta: switch | switch (valor) { case 'a': …; break; default: … } · sin break, sigue de largo
recompensa: xp 10, oro 10
```

#### Escena
Lumina tiene una lista de precios: el tiro cuesta 2 fichas, la calesita 3 y los títeres 1. Lo que no está en la lista, no existe.

#### Gheco sugiere
`switch` compara un valor con varias opciones fijas, como un menú:

```js
switch (juego) {
    case 'calesita':
        precio = 2;
        break;
    default:
        precio = 0;
}
```

Compara con `===`. Cada caso termina con `break` (si no, sigue de largo con el de abajo), y `default` es para lo que no coincide con ninguno.

#### Desafío
Completá el `switch` con los tres juegos, para que el `'calesita'` muestre `3 fichas`.

#### Código inicial
```javascript
const juego = 'calesita';

switch (juego) {
  case 'tiro':
    console.log('2 fichas');
    break;
  // Agregá la calesita (3) y los títeres (1)

  default:
    console.log('Ese juego no existe');
}
```

#### Salida esperada
```
3 fichas
```

#### Solución
```javascript
const juego = 'calesita';

switch (juego) {
  case 'tiro':
    console.log('2 fichas');
    break;
  case 'calesita':
    console.log('3 fichas');
    break;
  case 'titeres':
    console.log('1 ficha');
    break;
  default:
    console.log('Ese juego no existe');
}
```

#### Al superarla
Lumina cuelga la lista en la boletería, con letras de luz. Desde entonces, nadie le pregunta más los precios.

#### Imagen
- Una boletería de feria con una lista de precios hecha de luces (sin letras legibles) y tres íconos: un blanco, un caballito y un títere.
- Lumina (luciérnaga enorme con alas de vidrio) acomoda la lista; Gheco ayuda colgado de un clavo.

### Micro-misión R01-N03-P4 · El ogro del cero

```meta
lugar: La calesita
personajes: Nima, Gheco
criatura: ogre
carta: ?? | a ?? b · usa b solo si a es null o undefined · || también reemplaza el 0 y el ''
recompensa: xp 10, oro 10
```

#### Escena
Un ogro torpe anota cuántas vueltas dio cada uno. Si alguien dio 0 vueltas, el ogro anota «3», porque usa `||` y se le borra el cero.

#### Gheco sugiere
Dos operadores para poner un valor por defecto:

- `x || 3` usa el 3 si `x` es **cualquier cosa falsa**: también el 0 y el texto vacío;
- `x ?? 3` usa el 3 **solo** si no hay dato (`null` o `undefined`).

Si 0 es un valor válido (cero vueltas), usá `??`.

#### Desafío
Cambiá `||` por `??` para que las 0 vueltas se respeten, pero el que no tiene dato siga con 3.

#### Código inicial
```javascript
const vueltasDeNima = 0;
let vueltasDelNene;

console.log('Nima:', vueltasDeNima || 3);
console.log('El nene:', vueltasDelNene || 3);
```

#### Salida esperada
```
Nima: 0
El nene: 3
```

#### Solución
```javascript
const vueltasDeNima = 0;
let vueltasDelNene;

console.log('Nima:', vueltasDeNima ?? 3);
console.log('El nene:', vueltasDelNene ?? 3);
```

#### Al superarla
El ogro mira el cero un rato largo, como si fuera la primera vez que ve uno, y lo deja en paz.

#### Imagen
- Un ogro grandote y torpe de feria (sin armas, con delantal de rayas) sentado en un banquito con una libreta enorme y un lápiz chiquito.
- Nima le señala la libreta; Gheco se ríe en su hombro.

### Micro-misión R01-N03-P5 · El caballito que no está

```meta
lugar: La calesita
personajes: Nima, Gheco
criatura: troll
carta: ?. | obj.prop?.otra · si prop es null o undefined, da undefined sin error · se combina con ??
recompensa: xp 15, monedas 5
```

#### Escena
La calesita guarda qué caballito eligió cada uno. Nima todavía no eligió, y cuando el programa le pregunta el color de su caballito, explota con un error rojo.

#### Gheco sugiere
Si `jugadora.caballito` es `undefined`, pedirle `.color` corta el programa con un error.

Con `?.` (**encadenamiento opcional**) no explota: `jugadora.caballito?.color` da `undefined` si no hay caballito, en vez de error. Y con `?? 'sin elegir'` le das un texto por defecto.

#### Desafío
Arreglá la línea que explota para que muestre `Color: sin elegir`.

#### Código inicial
```javascript
const jugadora = { nombre: 'Nima' };

console.log('Jugadora:', jugadora.nombre);
console.log('Color:', jugadora.caballito.color);
```

#### Salida esperada
```
Jugadora: Nima
Color: sin elegir
```

#### Solución
```javascript
const jugadora = { nombre: 'Nima' };

console.log('Jugadora:', jugadora.nombre);
console.log('Color:', jugadora.caballito?.color ?? 'sin elegir');
```

#### Al superarla
Nima recorre la calesita una vez más antes de elegir. Al final se queda con un caballito negro de crines amarillas, como su chaqueta.

#### Imagen
- Un caballito de calesita negro con crines amarillas, de primer plano, con la calesita borrosa de fondo.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) acaricia el caballito.

### Micro-misión R01-N03-P6 · La entrada a la montaña rusa

```meta
lugar: La calesita
personajes: Nima, Gheco
carta: && y || | a && b: las dos · a || b: alguna · ternario: cond ? 'sí' : 'no'
recompensa: xp 15, monedas 5
```

#### Escena
Para la montaña rusa hay que medir al menos 1,4 m **y** tener 4 fichas, **o** tener el pase dorado. Nima mide 1,7 m, tiene 3 fichas y no tiene pase.

#### Gheco sugiere
Para juntar condiciones:

- `&&` es «**y**»: las dos tienen que cumplirse;
- `||` es «**o**»: alcanza con una.

Para elegir entre dos textos en una línea, el **ternario**: `puede ? 'Pasa' : 'No pasa'`. Si `puede` es verdad, da lo primero; si no, lo segundo.

#### Desafío
Completá la condición para que muestre `Nima: No pasa`.

#### Código inicial
```javascript
const altura = 1.7;
const fichas = 3;
const paseDorado = false;

const puede = ___;
console.log('Nima:', puede ? 'Pasa' : 'No pasa');
```

#### Salida esperada
```
Nima: No pasa
```

#### Solución
```javascript
const altura = 1.7;
const fichas = 3;
const paseDorado = false;

const puede = (altura >= 1.4 && fichas >= 4) || paseDorado;
console.log('Nima:', puede ? 'Pasa' : 'No pasa');
```

#### Al superarla
—Te falta una ficha —dice el guardia—. Volvé cuando hayas ganado más. —Nima mira los puestos que quedan con otros ojos.

#### Imagen
- La entrada de una montaña rusa de madera de feria, con luces amarillas y una vara de medir pintada (sin números).
- Nima, más alta que la vara, cuenta tres fichas en la mano con cara de fastidio; un guardia le cierra el paso con una sonrisa.

## R01-N04 · Bucles: for, while, for…of y for…in

```meta
tipo: tema
padre: R01-N03
precio: 10
criatura: orc
temas: prog.bucles
```

### Crónica

Al fondo de la avenida está la **Bengala**, la pirotécnica de la Feria. Tiene que prender cien cohetes, uno por uno, y siempre se olvida de alguno o prende el mismo dos veces.

—Para repetir, no se escribe cien veces —dice {mentor}—. Se escribe una vez y se dice **cuántas**, o **hasta cuándo**.

### Objetivos

- Repetir con `for` contando, y con `while` mientras se cumpla algo.
- Recorrer los elementos de un arreglo con `for…of`.
- Recorrer las propiedades de un objeto con `for…in`.
- Cortar con `break` y saltear con `continue`.
- Evitar los bucles que no terminan.

### Antes de empezar

- R01-N03: decisiones.

### Explicación

#### for: contando
```javascript
for (let i = 1; i <= 3; i++) {
  console.log('Cohete', i);
}
```
Tres partes entre paréntesis: dónde **empieza** (`let i = 1`), **mientras** qué sigue (`i <= 3`) y qué pasa al final de cada vuelta (`i++`).

#### while: mientras
```javascript
let polvora = 10;
while (polvora > 0) {
  polvora -= 4;
}
```
Repite mientras la condición sea verdad. Si nunca se vuelve falsa, el bucle **no termina** (en la caja se corta solo y te avisa).

#### for…of: cada elemento
```javascript
const colores = ['rojo', 'verde', 'azul'];
for (const color of colores) {
  console.log(color);
}
```

#### for…in: cada propiedad
```javascript
const precios = { tiro: 2, calesita: 3 };
for (const juego in precios) {
  console.log(juego, precios[juego]);
}
```
`for…in` da las **claves** (los nombres). Para arreglos, usá `for…of` (con `for…in` te da los índices como texto).

#### break y continue
- `break` corta el bucle entero.
- `continue` saltea lo que queda de **esa** vuelta y sigue con la próxima.

### Código de ejemplo

```javascript
// Cuenta regresiva de Bengala
for (let i = 3; i >= 1; i--) {
  console.log(`${i}...`);
}
console.log('¡Fuego!');

const cohetes = ['rojo', 'mojado', 'verde', 'azul'];
for (const cohete of cohetes) {
  if (cohete === 'mojado') {
    console.log('(este no prende)');
    continue;
  }
  console.log('Explota uno', cohete);
}

const precios = { tiro: 2, calesita: 3, titeres: 1 };
for (const juego in precios) {
  console.log(`${juego}: ${precios[juego]} fichas`);
}
```

### Salida esperada

```
3...
2...
1...
¡Fuego!
Explota uno rojo
(este no prende)
Explota uno verde
Explota uno azul
tiro: 2 fichas
calesita: 3 fichas
titeres: 1 fichas
```

### ¿Para qué sirve?

Mostrar todos los productos de una tienda, revisar cada casilla de un formulario, mover a todos los enemigos de un juego en cada cuadro: casi todo programa repite algo. Saber elegir el bucle justo hace el código más corto y más claro.

### Errores habituales

**Orco: uno de más o uno de menos.** `for (let i = 0; i <= 3; i++)` da **cuatro** vueltas (0, 1, 2, 3). Contá con cuidado el `<` y el `<=`.

**Troll: el `while` que no termina.** Si te olvidás de cambiar la variable de la condición, el bucle sigue para siempre. La caja lo corta: «Se cortó a los 5 segundos».

**Ogro: `for…in` en un arreglo.** Da los índices como texto (`'0'`, `'1'`…), no los elementos. Para arreglos, `for…of`.

### Micro-misión R01-N04-P1 · La cuenta regresiva

```meta
lugar: La explanada de los fuegos
personajes: Nima, Gheco, Bengala
carta: for | for (let i = 5; i >= 1; i--) { … } · empieza · mientras · cambia
recompensa: xp 10, oro 10
```

#### Escena
Bengala, la pirotécnica, cuenta para atrás antes de cada cohete, pero siempre se saltea un número. Le pide a Nima que la ayude.

#### Gheco sugiere
Un **bucle** repite instrucciones. El `for` tiene tres partes entre paréntesis:

```js
for (let i = 1; i <= 3; i++) {
    console.log(i);
}
```

1. **arranque**: `let i = 1`;
2. **condición**: `i <= 3`, se pregunta antes de cada vuelta;
3. **paso**: `i++`, al final de cada vuelta.

Para contar hacia atrás, arrancá alto y usá `i--`.

#### Desafío
Completá el `for` para que cuente del 5 al 1, y después muestre `¡Fuego!`.

#### Código inicial
```javascript
for (___) {
  console.log(i);
}
console.log('¡Fuego!');
```

#### Salida esperada
```
5
4
3
2
1
¡Fuego!
```

#### Solución
```javascript
for (let i = 5; i >= 1; i--) {
  console.log(i);
}
console.log('¡Fuego!');
```

#### Al superarla
El cohete sube derechito y explota en una flor amarilla. Bengala aplaude con los guantes chamuscados.

#### Imagen
- Una explanada de feria de noche con un cohete subiendo y una flor de fuegos artificiales amarilla en el cielo.
- Bengala (mujer joven pirotécnica, antiparras de cuero, delantal grueso cerrado, guantes chamuscados, pelo corto rojizo) aplaude; Nima mira para arriba.

### Micro-misión R01-N04-P2 · Todos los colores

```meta
lugar: La explanada de los fuegos
personajes: Nima, Gheco, Bengala
carta: for…of | for (const x of lista) { … } · da cada elemento, en orden
recompensa: xp 10, oro 10
```

#### Escena
Bengala tiene una fila de cohetes de colores. Quiere anunciar cada uno antes de prenderlo.

#### Gheco sugiere
Un **arreglo** (*array*) es una lista de valores entre corchetes: `['rojo', 'verde', 'azul']`.

`for…of` lo recorre y te da cada elemento, uno por vuelta:

```js
for (const color of colores) {
    console.log(color);
}
```

#### Desafío
Recorré el arreglo con `for…of` y mostrá `Cohete rojo`, `Cohete verde`, etc.

#### Código inicial
```javascript
const cohetes = ['rojo', 'verde', 'violeta', 'dorado'];

// Recorrelos acá

```

#### Salida esperada
```
Cohete rojo
Cohete verde
Cohete violeta
Cohete dorado
```

#### Solución
```javascript
const cohetes = ['rojo', 'verde', 'violeta', 'dorado'];

for (const cohete of cohetes) {
  console.log(`Cohete ${cohete}`);
}
```

#### Al superarla
Cuatro flores de colores se abren en el cielo, una detrás de la otra, en el orden exacto. La gente de la Feria dice «¡ooooh!» cuatro veces.

#### Imagen
- El cielo nocturno de la feria con cuatro fuegos artificiales en fila: rojo, verde, violeta y dorado.
- Siluetas de gente de feria mirando para arriba; Bengala con un farol en la mano.

### Micro-misión R01-N04-P3 · El cohete mojado

```meta
lugar: La explanada de los fuegos
personajes: Nima, Gheco, Bengala
carta: continue y break | continue: saltea esta vuelta · break: corta el bucle entero
recompensa: xp 10, oro 10
```

#### Escena
Llovió un poco y hay cohetes mojados. Los mojados no se prenden (se saltean), y si aparece uno **roto**, hay que parar todo por seguridad.

#### Gheco sugiere
Dos órdenes para controlar un bucle desde adentro:

- `continue;` saltea lo que queda de **esta** vuelta y pasa a la siguiente;
- `break;` corta el bucle **entero**.

#### Desafío
Completá los dos `if` para que los mojados se salteen y el roto corte el bucle.

#### Código inicial
```javascript
const cohetes = ['rojo', 'mojado', 'verde', 'roto', 'azul'];

for (const cohete of cohetes) {
  // si está mojado, saltealo; si está roto, pará todo

  console.log('Explota uno', cohete);
}
console.log('Fin del show');
```

#### Salida esperada
```
Explota uno rojo
Explota uno verde
Fin del show
```

#### Solución
```javascript
const cohetes = ['rojo', 'mojado', 'verde', 'roto', 'azul'];

for (const cohete of cohetes) {
  if (cohete === 'mojado') continue;
  if (cohete === 'roto') break;
  console.log('Explota uno', cohete);
}
console.log('Fin del show');
```

#### Al superarla
El cohete azul queda en la caja, sin prenderse. —Mejor así —dice Bengala—. Después del roto, no me fío de ninguno.

#### Imagen
- Una caja de madera con cohetes de colores; uno goteando agua y otro partido al medio.
- Bengala, con antiparras y guantes, aparta el cohete roto con una pinza; Nima le alcanza un balde.

### Micro-misión R01-N04-P4 · La pólvora que se acaba

```meta
lugar: La explanada de los fuegos
personajes: Nima, Gheco, Bengala
carta: while | while (condición) { … } · repite mientras se cumpla · cambiá la variable adentro
recompensa: xp 10, oro 10
```

#### Escena
Bengala tiene 20 gramos de pólvora y cada cohete usa 6. Quiere saber cuántos cohetes le salen.

#### Gheco sugiere
`while` repite **mientras** la condición sea verdad:

```js
while (polvora >= 6) { ... }
```

Adentro, algo tiene que cambiar para que alguna vez deje de cumplirse: restá los 6 gramos y sumá un cohete. Si no restás, no termina nunca.

#### Desafío
Completá el `while` para que muestre `Cohetes: 3` y `Sobran: 2`.

#### Código inicial
```javascript
let polvora = 20;
let cohetes = 0;

while (___) {

}
console.log('Cohetes:', cohetes);
console.log('Sobran:', polvora);
```

#### Salida esperada
```
Cohetes: 3
Sobran: 2
```

#### Solución
```javascript
let polvora = 20;
let cohetes = 0;

while (polvora >= 6) {
  polvora -= 6;
  cohetes++;
}
console.log('Cohetes:', cohetes);
console.log('Sobran:', polvora);
```

#### Al superarla
Bengala arma tres cohetes y guarda la pólvora que sobra en un frasquito con una etiqueta: *para la próxima*.

#### Imagen
- Una mesa de trabajo de pirotecnia con una balanza chiquita, montoncitos de pólvora gris y tres cohetes armados.
- Bengala (antiparras de cuero, delantal grueso) cierra un frasquito; Gheco mira de lejos, por las dudas.

### Micro-misión R01-N04-P5 · La lista de precios

```meta
lugar: La explanada de los fuegos
personajes: Nima, Gheco, Bengala
carta: for…in | for (const clave in objeto) { … } · da cada nombre · el valor es objeto[clave]
recompensa: xp 15, monedas 5
```

#### Escena
Bengala vende cohetes de tres tamaños y guarda los precios en un objeto. Quiere imprimir la lista para colgarla.

#### Gheco sugiere
`for…in` recorre los **nombres** de un objeto (sus claves):

```js
for (const tamaño in precios) {
    console.log(tamaño, precios[tamaño]);
}
```

En cada vuelta, `tamaño` es un nombre, y `precios[tamaño]` es su valor.

#### Desafío
Mostrá cada tamaño con su precio, así: `chico: 1 fichas`, `mediano: 3 fichas`, `grande: 5 fichas`.

#### Código inicial
```javascript
const precios = { chico: 1, mediano: 3, grande: 5 };

```

#### Salida esperada
```
chico: 1 fichas
mediano: 3 fichas
grande: 5 fichas
```

#### Solución
```javascript
const precios = { chico: 1, mediano: 3, grande: 5 };

for (const tamaño in precios) {
  console.log(`${tamaño}: ${precios[tamaño]} fichas`);
}
```

#### Al superarla
La lista queda colgada en un poste, y Bengala vende todos los cohetes medianos en diez minutos.

#### Imagen
- Un poste de feria con una lista colgada (sin texto legible) y tres cohetes de tamaños distintos dibujados.
- Bengala atiende a una fila de chicos; Nima sostiene una caja de cohetes.

### Micro-misión R01-N04-P6 · La tabla de los fuegos

```meta
lugar: La explanada de los fuegos
personajes: Nima, Gheco, Bengala, Lumina
carta: Bucles anidados | un for adentro de otro · el de adentro da todas sus vueltas por cada vuelta del de afuera
recompensa: xp 15, monedas 5
```

#### Escena
Para el gran final, Bengala quiere 3 tandas de 4 cohetes cada una. Lumina le pide que muestre el plan entero antes de prender nada.

#### Gheco sugiere
Un bucle puede ir **adentro** de otro (bucles **anidados**): un `for` para las tandas y, adentro, otro `for` para los cohetes de cada tanda.

Armá el renglón de cada tanda sumándole partes con `+=` (con textos, `+=` pega al final), y mostralo al terminar esa tanda.

#### Desafío
Mostrá cada tanda con sus cohetes numerados, así:
- `Tanda 1: * * * *`
- `Tanda 2: * * * *`
- `Tanda 3: * * * *`

#### Código inicial
```javascript
for (let tanda = 1; tanda <= 3; tanda++) {
  let renglon = `Tanda ${tanda}:`;
  // Agregale un ' *' por cada uno de los 4 cohetes

  console.log(renglon);
}
```

#### Salida esperada
```
Tanda 1: * * * *
Tanda 2: * * * *
Tanda 3: * * * *
```

#### Solución
```javascript
for (let tanda = 1; tanda <= 3; tanda++) {
  let renglon = `Tanda ${tanda}:`;
  for (let cohete = 1; cohete <= 4; cohete++) {
    renglon += ' *';
  }
  console.log(renglon);
}
```

#### Al superarla
El gran final llena el cielo: doce cohetes en tres tandas perfectas. Lumina vuela entre las chispas, feliz. —Esta parte de la Feria ya sabe repetir —dice.

#### Imagen
- El cielo de la feria lleno de fuegos artificiales amarillos en tres filas ordenadas.
- Lumina (luciérnaga enorme, alas de vidrio, luz amarilla en el pecho) vuela entre las chispas; abajo, Nima y Bengala miran abrazadas por los hombros.

## R01-N05 · Arreglos: map, filter y reduce

```meta
tipo: tema
padre: R01-N04
precio: 10
criatura: orc
temas: col.listas
```

### Crónica

Del puesto del pan con miel sale un olor que no deja pensar. Lo atiende **Doña Mirta**, una panadera petisa y apurada, con una bandeja larguísima de panes en fila. Los cuenta, los ordena, les cambia el precio, saca los quemados… y siempre se pierde.

—Una fila de cosas es un **arreglo** —dice {mentor}—. Y en la Feria, los arreglos traen sus propias herramientas: una para transformar cada elemento, otra para quedarse con algunos y otra para juntarlos todos en uno.

### Objetivos

- Crear arreglos, leer por posición (desde 0) y saber su largo con `length`.
- Agregar y sacar con `push`, `pop`, `unshift` y `shift`.
- Buscar con `includes`, `indexOf` y `find`.
- Transformar con `map`, filtrar con `filter` y acumular con `reduce`.
- Distinguir los métodos que **cambian** el arreglo de los que devuelven uno nuevo.

### Antes de empezar

- R01-N04: bucles y `for…of`.

### Explicación

#### Un arreglo
```javascript
const panes = ['miel', 'nuez', 'quemado'];
console.log(panes[0]);       // 'miel' (las posiciones empiezan en 0)
console.log(panes.length);   // 3
console.log(panes[3]);       // undefined: no hay posición 3 (un orco)
```

#### Agregar y sacar
| Método | Qué hace |
|---|---|
| `push(x)` | agrega al final |
| `pop()` | saca el último (y lo devuelve) |
| `unshift(x)` | agrega al principio |
| `shift()` | saca el primero |

Estos **cambian** el arreglo original.

#### Buscar
```javascript
panes.includes('nuez');            // true
panes.indexOf('quemado');          // 2 (o -1 si no está)
const precios = [3, 5, 8];
precios.find((p) => p > 4);        // 5: el primero que cumple
```

#### map, filter y reduce
Reciben una **función flecha** (`(x) => …`) que se aplica a cada elemento, y **devuelven algo nuevo** sin tocar el original:
```javascript
const precios = [2, 3, 5];
const conAumento = precios.map((p) => p + 1);          // [3, 4, 6]
const baratos = precios.filter((p) => p <= 3);         // [2, 3]
const total = precios.reduce((suma, p) => suma + p, 0); // 10
```
- `map`: un arreglo **del mismo largo**, con cada elemento transformado.
- `filter`: un arreglo con **los que cumplen** la condición.
- `reduce`: **un solo valor**. Empieza en el segundo argumento (`0`) y va acumulando.

(Las funciones flecha las vas a ver a fondo en R01-N07; por ahora alcanza con saber que `(p) => p + 1` quiere decir «a cada `p`, devolvé `p + 1`».)

### Código de ejemplo

```javascript
const bandeja = ['miel', 'nuez', 'quemado', 'miel'];
bandeja.push('canela');
console.log(bandeja, bandeja.length);

const buenos = bandeja.filter((pan) => pan !== 'quemado');
console.log('Buenos:', buenos);

const precios = [2, 3, 2, 4];
console.log('Con aumento:', precios.map((p) => p * 2));
console.log('Total:', precios.reduce((suma, p) => suma + p, 0));
console.log('¿Hay de nuez?', bandeja.includes('nuez'));
```

### Salida esperada

```
[ 'miel', 'nuez', 'quemado', 'miel', 'canela' ] 5
Buenos: [ 'miel', 'nuez', 'miel', 'canela' ]
Con aumento: [ 4, 6, 4, 8 ]
Total: 11
¿Hay de nuez? true
```

### ¿Para qué sirve?

Una lista de productos, de mensajes, de enemigos o de puntajes: casi todos los datos vienen en arreglos. `map`, `filter` y `reduce` son las tres herramientas que más vas a usar para mostrar, buscar y resumir datos, en el navegador y en cualquier framework.

### Errores habituales

**Orco: contar desde 1.** El primer elemento es `[0]` y el último es `[largo - 1]`. `panes[panes.length]` da `undefined`.

**Ogro: olvidarse el `return` en una flecha con llaves.** `precios.map((p) => { p * 2 })` da `[undefined, …]`. Con llaves hay que escribir `return`; sin llaves, `(p) => p * 2`, devuelve solo.

**Ogro: esperar que `map` cambie el original.** `map` y `filter` devuelven uno **nuevo**: guardalo en una variable.

**Orco: `reduce` sin valor inicial en un arreglo vacío.** Da `TypeError: Reduce of empty array with no initial value`. Poné siempre el inicial: `reduce(…, 0)`.

### Micro-misión R01-N05-P1 · La bandeja de Doña Mirta

```meta
lugar: El puesto del pan con miel
personajes: Nima, Gheco, Doña Mirta
carta: Arreglos | ['a', 'b'] · lista[0] es el primero · lista.length es el largo
recompensa: xp 10, oro 10
```

#### Escena
Doña Mirta pone la bandeja sobre el mostrador. —¿Cuál es el primero? ¿Y cuántos hay? ¡Rápido, que se enfrían!

#### Gheco sugiere
Cada elemento de un arreglo tiene una posición, que se cuenta desde **0**:

- el primero es `panes[0]`;
- `panes.length` dice cuántos hay;
- el último es `panes[panes.length - 1]` (si hay 5, el último está en la posición 4).

#### Desafío
Mostrá el primer pan, el último y cuántos hay.

#### Código inicial
```javascript
const panes = ['miel', 'nuez', 'canela', 'miel', 'chocolate'];

console.log('Primero:', ___);
console.log('Último:', ___);
console.log('Cantidad:', ___);
```

#### Salida esperada
```
Primero: miel
Último: chocolate
Cantidad: 5
```

#### Solución
```javascript
const panes = ['miel', 'nuez', 'canela', 'miel', 'chocolate'];

console.log('Primero:', panes[0]);
console.log('Último:', panes[panes.length - 1]);
console.log('Cantidad:', panes.length);
```

#### Al superarla
—¡Cinco! —dice Doña Mirta—. Siempre me da cuatro o seis. —Le regala a Nima el de miel.

#### Imagen
- Un puesto de feria de pan con miel de noche, con una bandeja larga de panes dorados en fila y frascos de miel.
- Doña Mirta (señora petisa y redonda, delantal floreado cerrado, pañuelo en la cabeza, cucharón de madera) señala la bandeja; Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) cuenta con el dedo.

### Micro-misión R01-N05-P2 · Recién salidos del horno

```meta
lugar: El puesto del pan con miel
personajes: Nima, Gheco, Doña Mirta
carta: push y shift | push(x) agrega al final · shift() saca el primero · cambian el arreglo
recompensa: xp 10, oro 10
```

#### Escena
Del horno salen dos panes nuevos, de canela y de anís, y van al final de la fila. El primero de la fila se vende enseguida.

#### Gheco sugiere
Los arreglos tienen **métodos** (funciones que se usan con un punto) para cambiarlos:

- `push(x)` agrega al final (se le pueden pasar varios: `push(a, b)`);
- `shift()` saca el primero.

#### Desafío
Agregá `'canela'` y `'anis'` al final, vendé el primero y mostrá cómo quedó la bandeja.

#### Código inicial
```javascript
const bandeja = ['miel', 'nuez'];

// Agregá los dos nuevos y vendé el primero

console.log(bandeja);
```

#### Salida esperada
```
[ 'nuez', 'canela', 'anis' ]
```

#### Solución
```javascript
const bandeja = ['miel', 'nuez'];

bandeja.push('canela', 'anis');
bandeja.shift();
console.log(bandeja);
```

#### Al superarla
La fila avanza: los recién salidos van atrás y los de adelante se venden. —Así nunca se me quema ninguno —dice Doña Mirta.

#### Imagen
- La puerta de un horno de barro de feria abierta, con dos panes nuevos saliendo en una pala de madera.
- Doña Mirta acomoda los panes al final de la bandeja; un chico se lleva el primero de la fila.

### Micro-misión R01-N05-P3 · Fuera los quemados

```meta
lugar: El puesto del pan con miel
personajes: Nima, Gheco, Doña Mirta
carta: filter | lista.filter((x) => condición) · devuelve los que cumplen · no toca la original
recompensa: xp 10, oro 10
```

#### Escena
En la bandeja se colaron algunos panes quemados. Doña Mirta no quiere tirar la bandeja: quiere una nueva, solo con los buenos.

#### Gheco sugiere
`filter` arma un arreglo **nuevo** solo con los elementos que cumplen una condición. La condición es una función chiquita (una **flecha**):

```js
panes.filter((pan) => pan !== 'quemado')
```

Se lee: «para cada `pan`, quedate con él si no es `'quemado'`». `!==` es «distinto».

#### Desafío
Armá el arreglo `buenos` sin los quemados.

#### Código inicial
```javascript
const bandeja = ['miel', 'quemado', 'nuez', 'quemado', 'canela'];

const buenos = ___;
console.log('Buenos:', buenos);
console.log('La bandeja sigue igual:', bandeja.length);
```

#### Salida esperada
```
Buenos: [ 'miel', 'nuez', 'canela' ]
La bandeja sigue igual: 5
```

#### Solución
```javascript
const bandeja = ['miel', 'quemado', 'nuez', 'quemado', 'canela'];

const buenos = bandeja.filter((pan) => pan !== 'quemado');
console.log('Buenos:', buenos);
console.log('La bandeja sigue igual:', bandeja.length);
```

#### Al superarla
Los quemados van a parar a una canasta aparte: Doña Mirta dice que los pájaros de la Feria los prefieren.

#### Imagen
- Una bandeja de panes dorados y, al lado, una canastita con panes negros quemados y un pájaro picoteando.
- Las manos de Doña Mirta (delantal floreado) separan los panes; Gheco tapándose la nariz.

### Micro-misión R01-N05-P4 · Precios de feria

```meta
lugar: El puesto del pan con miel
personajes: Nima, Gheco, Doña Mirta
carta: map | lista.map((x) => nuevo) · mismo largo · cada elemento transformado
recompensa: xp 10, oro 10
```

#### Escena
Es noche de feria grande y Doña Mirta sube **una ficha** cada precio. Quiere la lista nueva sin perder la vieja.

#### Gheco sugiere
`map` arma un arreglo **nuevo** transformando cada elemento con una función:

```js
precios.map((p) => p * 2)
```

Devuelve cada precio multiplicado por 2. El arreglo original no cambia.

#### Desafío
Armá `nuevos` con cada precio aumentado en 1.

#### Código inicial
```javascript
const precios = [2, 3, 1, 4];

const nuevos = ___;
console.log('Antes:', precios);
console.log('Ahora:', nuevos);
```

#### Salida esperada
```
Antes: [ 2, 3, 1, 4 ]
Ahora: [ 3, 4, 2, 5 ]
```

#### Solución
```javascript
const precios = [2, 3, 1, 4];

const nuevos = precios.map((p) => p + 1);
console.log('Antes:', precios);
console.log('Ahora:', nuevos);
```

#### Al superarla
Doña Mirta pega los precios nuevos encima de los viejos, con miel en vez de cola. Se pegan igual.

#### Imagen
- Un pizarrón chico de feria con papelitos pegados uno encima de otro (sin números legibles) y un frasco de miel abierto.
- Doña Mirta pega un papelito con el dedo pegajoso; Nima se ríe.

### Micro-misión R01-N05-P5 · La caja del día

```meta
lugar: El puesto del pan con miel
personajes: Nima, Gheco, Doña Mirta
carta: reduce | lista.reduce((acum, x) => acum + x, 0) · empieza en 0 · devuelve un solo valor
recompensa: xp 15, monedas 5
```

#### Escena
Se termina la noche. Doña Mirta anotó cada venta en un arreglo y quiere saber cuánto juntó, y cuántas ventas fueron de más de 3 fichas.

#### Gheco sugiere
`reduce` junta todos los elementos en un solo valor:

```js
ventas.reduce((total, v) => total + v, 0)
```

Arranca con `total` en 0 (el último dato) y, por cada `v`, suma. Al final da la suma de todo.

Para contar los que cumplen algo: filtrá primero y mirá el `length` del resultado.

#### Desafío
Mostrá `Total: 23` y `Ventas grandes: 2`.

#### Código inicial
```javascript
const ventas = [2, 5, 3, 1, 8, 4];

const total = ___;
const grandes = ___;
console.log('Total:', total);
console.log('Ventas grandes:', grandes);
```

#### Salida esperada
```
Total: 23
Ventas grandes: 3
```

#### Solución
```javascript
const ventas = [2, 5, 3, 1, 8, 4];

const total = ventas.reduce((suma, v) => suma + v, 0);
const grandes = ventas.filter((v) => v > 3).length;
console.log('Total:', total);
console.log('Ventas grandes:', grandes);
```

#### Al superarla
Doña Mirta guarda las veintitrés fichas en una lata de galletitas y le da a Nima una bolsa de panes para el camino. —Para cuando tengas que esperar —le guiña.

#### Imagen
- Una lata de galletitas abierta llena de fichas de bronce, sobre el mostrador de un puesto de pan cerrando de noche.
- Doña Mirta le da a Nima una bolsita de papel con panes; Gheco ya está adentro de la bolsa.

### Micro-misión R01-N05-P6 · El pedido de Lumina

```meta
lugar: El puesto del pan con miel
personajes: Nima, Gheco, Doña Mirta, Lumina
carta: Encadenar | lista.filter(…).map(…) · el resultado de uno entra en el siguiente · find da el primero que cumple
recompensa: xp 15, monedas 5
```

#### Escena
Lumina quiere los panes de miel para las luciérnagas chicas, con el precio en fichas **doble** (es para un festejo). Y quiere saber cuál es el primer pan que cuesta más de 3.

#### Gheco sugiere
Los métodos se pueden **encadenar**, uno detrás del otro: primero `filter` para quedarte con los de miel, después `map` para sacar el precio por 2.

Para el primero que cumpla una condición, `find`: `find((p) => p.precio > 3)` devuelve el primero que la cumple (o `undefined` si ninguno).

#### Desafío
Mostrá `Miel al doble: [ 4, 6 ]` y `Primero caro: chocolate`.

#### Código inicial
```javascript
const panes = [
  { sabor: 'miel', precio: 2 },
  { sabor: 'nuez', precio: 3 },
  { sabor: 'chocolate', precio: 4 },
  { sabor: 'miel', precio: 3 },
];

const mielDoble = ___;
const caro = ___;
console.log('Miel al doble:', mielDoble);
console.log('Primero caro:', caro.sabor);
```

#### Salida esperada
```
Miel al doble: [ 4, 6 ]
Primero caro: chocolate
```

#### Solución
```javascript
const panes = [
  { sabor: 'miel', precio: 2 },
  { sabor: 'nuez', precio: 3 },
  { sabor: 'chocolate', precio: 4 },
  { sabor: 'miel', precio: 3 },
];

const mielDoble = panes.filter((p) => p.sabor === 'miel').map((p) => p.precio * 2);
const caro = panes.find((p) => p.precio > 3);
console.log('Miel al doble:', mielDoble);
console.log('Primero caro:', caro.sabor);
```

#### Al superarla
Esa noche las luciérnagas chicas brillan un poco más: dicen que es la miel. Doña Mirta jura que es su receta.

#### Imagen
- Un enjambre de luciérnagas chiquitas alrededor de una canasta con panes de miel, de noche.
- Lumina (luciérnaga enorme, alas de vidrio) recibe la canasta de manos de Doña Mirta; Nima mira.

## R01-N06 · Objetos, desestructuración y spread

```meta
tipo: tema
padre: R01-N05
precio: 10
criatura: skeleton
temas: col.mapas, prog.referencias
```

### Crónica

La **tienda de premios** de la Feria es un caos: osos de peluche, cometas, silbatos y faroles, cada uno con una etiqueta escrita a mano con su nombre, su precio, su color y cuántos quedan. El encargado, un señor muy flaco al que todos llaman **el Flaco Ruiz**, busca cada dato en una pila de etiquetas.

—Un premio no es un número ni un texto: es **muchas cosas juntas** —dice {mentor}—. En JavaScript eso se guarda en un **objeto**, con un nombre para cada dato.

### Objetivos

- Crear objetos con `{ clave: valor }` y leerlos con `.` y con `[ ]`.
- Agregar, cambiar y borrar propiedades.
- Recorrerlos con `Object.keys`, `Object.values` y `Object.entries`.
- Desarmar objetos y arreglos con la desestructuración.
- Copiar y combinar con el spread `...`.
- Entender que dos variables pueden apuntar al **mismo** objeto, y congelarlo con `Object.freeze`.

### Antes de empezar

- R01-N05: arreglos.

### Explicación

#### Un objeto
```javascript
const premio = { nombre: 'Oso', precio: 10, color: 'marrón' };
console.log(premio.nombre);      // 'Oso'
console.log(premio['precio']);   // 10 (con corchetes, útil si la clave está en una variable)
premio.quedan = 3;               // agrega una propiedad
premio.precio = 12;              // la cambia
delete premio.color;             // la borra
```
Aunque `premio` sea `const`, sus propiedades **sí** se pueden cambiar: `const` sella la cajita, no lo que hay adentro.

#### Recorrer
```javascript
Object.keys(premio);     // [ 'nombre', 'precio', 'quedan' ]
Object.values(premio);   // [ 'Oso', 12, 3 ]
Object.entries(premio);  // [ [ 'nombre', 'Oso' ], … ]
```

#### Desestructurar
```javascript
const { nombre, precio } = premio;          // dos variables de una vez
const { color = 'sin color' } = premio;     // con valor por defecto
const [primero, segundo] = ['oso', 'cometa'];
```

#### Spread: copiar y combinar
```javascript
const copia = { ...premio };                       // una copia nueva
const enOferta = { ...premio, precio: 8 };          // copia y cambia el precio
const todos = [...premiosChicos, ...premiosGrandes]; // junta dos arreglos
```

#### El mismo objeto, dos nombres
```javascript
const a = { quedan: 3 };
const b = a;      // b NO es una copia: es otro nombre del mismo objeto
b.quedan = 0;
console.log(a.quedan);   // 0
```
Para una copia de verdad, `{ ...a }`. Y para que nadie lo cambie, `Object.freeze(a)`.

### Código de ejemplo

```javascript
const premio = { nombre: 'Cometa', precio: 6, color: 'rojo' };
premio.quedan = 4;
console.log(premio);

const { nombre, precio } = premio;
console.log(`${nombre} cuesta ${precio} fichas`);

const enOferta = { ...premio, precio: 4 };
console.log('Original:', premio.precio, '· Oferta:', enOferta.precio);

for (const [clave, valor] of Object.entries(premio)) {
  console.log(`${clave} → ${valor}`);
}

const otroNombre = premio;
otroNombre.quedan = 0;
console.log('Quedan (en el original):', premio.quedan);
```

### Salida esperada

```
{ nombre: 'Cometa', precio: 6, color: 'rojo', quedan: 4 }
Cometa cuesta 6 fichas
Original: 6 · Oferta: 4
nombre → Cometa
precio → 6
color → rojo
quedan → 4
Quedan (en el original): 0
```

### ¿Para qué sirve?

Un usuario, un producto, un personaje de un juego, la respuesta de un servidor: casi todo en JavaScript es un objeto. La desestructuración y el spread están en todo el código moderno (y en React, todo el tiempo).

### Errores habituales

**Esqueleto: una propiedad mal escrita.** `premio.precoi` no da error: da `undefined`, y el problema aparece después.

**Troll: creer que `b = a` copia.** Cambiás `b` y se cambia `a`. Para copiar, `{ ...a }` o `[...a]`.

**Ogro: el spread copia solo el primer nivel.** `{ ...premio }` copia las propiedades, pero si una de ellas es otro objeto, ese sigue siendo compartido. Para copiar todo, `structuredClone(premio)`.

**Slime: desestructurar `undefined`.** `const { nombre } = undefined;` da `Cannot destructure property 'nombre' of 'undefined'`.

### Micro-misión R01-N06-P1 · La etiqueta del oso

```meta
lugar: La tienda de premios
personajes: Nima, Gheco, el Flaco Ruiz
carta: Objetos | { nombre: 'Oso', precio: 10 } · premio.nombre · premio['precio']
recompensa: xp 10, oro 10
```

#### Escena
El Flaco Ruiz le pide a Nima que pase la etiqueta del oso de peluche a una cajita con nombres: nombre, precio y color.

#### Gheco sugiere
Un **objeto** junta varios datos sobre una misma cosa, cada uno con su nombre, entre llaves:

```js
const premio = { nombre: 'oso', precio: 8, color: 'marrón' };
```

Cada `nombre: valor` es una **propiedad**, separadas por comas. Se lee con un punto: `premio.precio`.

#### Desafío
Creá el objeto `oso` con `nombre` `'Oso'`, `precio` `10` y `color` `'marrón'`.

#### Código inicial
```javascript
const oso = ___;

console.log(oso.nombre, 'cuesta', oso.precio);
console.log('Color:', oso['color']);
```

#### Salida esperada
```
Oso cuesta 10
Color: marrón
```

#### Solución
```javascript
const oso = { nombre: 'Oso', precio: 10, color: 'marrón' };

console.log(oso.nombre, 'cuesta', oso.precio);
console.log('Color:', oso['color']);
```

#### Al superarla
El Flaco Ruiz busca el precio del oso en dos segundos en vez de dos minutos. Se queda mirando el objeto como si fuera magia.

#### Imagen
- Una tienda de premios de feria llena de osos de peluche, cometas y faroles colgados, con etiquetas de cartón (sin texto).
- El Flaco Ruiz (señor muy flaco y alto, bigote fino, chaleco verde abotonado, galera chiquita) sostiene un oso marrón; Nima toma notas.

### Micro-misión R01-N06-P2 · Quedan pocos

```meta
lugar: La tienda de premios
personajes: Nima, Gheco, el Flaco Ruiz
carta: Cambiar propiedades | obj.prop = valor agrega o cambia · delete obj.prop borra · const no impide cambiar adentro
recompensa: xp 10, oro 10
```

#### Escena
Llegaron más cometas, subió el precio y ya no hay color rojo. El Flaco quiere actualizar la etiqueta sin hacer una nueva.

#### Gheco sugiere
Las propiedades de un objeto se pueden cambiar:

- `cometa.quedan = 5` la **agrega** si no estaba;
- `cometa.precio = 7` la **cambia** si estaba;
- `delete cometa.color` la **borra**.

#### Desafío
Agregá `quedan: 5`, cambiá el precio a `7` y borrá el `color`.

#### Código inicial
```javascript
const cometa = { nombre: 'Cometa', precio: 6, color: 'rojo' };

// Actualizá la etiqueta

console.log(cometa);
```

#### Salida esperada
```
{ nombre: 'Cometa', precio: 7, quedan: 5 }
```

#### Solución
```javascript
const cometa = { nombre: 'Cometa', precio: 6, color: 'rojo' };

cometa.quedan = 5;
cometa.precio = 7;
delete cometa.color;
console.log(cometa);
```

#### Al superarla
—¡Y era `const`! —se asombra el Flaco—. —La cajita está sellada —le explica Nima—, pero lo de adentro se puede acomodar.

#### Imagen
- Un mazo de cometas de colores colgadas del techo de una tienda de feria, con una etiqueta de cartón tachada.
- El Flaco Ruiz sube una escalera para colgar más cometas; Gheco le sostiene la etiqueta.

### Micro-misión R01-N06-P3 · Desarmar el paquete

```meta
lugar: La tienda de premios
personajes: Nima, Gheco, el Flaco Ruiz
carta: Desestructurar | const { a, b } = obj · const [x, y] = lista · con valor por defecto: { c = 'x' }
recompensa: xp 10, oro 10
```

#### Escena
Llega un paquete con un premio adentro. El Flaco quiere sacar el nombre y el precio, y si no trae color, ponerle `'sin color'`.

#### Gheco sugiere
Para sacar varias propiedades de un objeto de una vez, se **desarma** (desestructuración):

```js
const { nombre, precio } = paquete;
```

Crea las variables `nombre` y `precio` con los valores del objeto. Con `= 'algo'` le das un valor por defecto, por si esa propiedad no está.

#### Desafío
Desestructurá `paquete` para que el programa muestre los tres datos.

#### Código inicial
```javascript
const paquete = { nombre: 'Silbato', precio: 2 };

// Desarmalo en una sola línea

console.log(nombre, precio, color);
```

#### Salida esperada
```
Silbato 2 sin color
```

#### Solución
```javascript
const paquete = { nombre: 'Silbato', precio: 2 };

const { nombre, precio, color = 'sin color' } = paquete;

console.log(nombre, precio, color);
```

#### Al superarla
El silbato queda en la vitrina con su etiqueta completa: *sin color*. El Flaco lo prueba. Suena horrible.

#### Imagen
- Una caja de cartón abierta sobre un mostrador, con papel de seda y un silbato de lata adentro.
- El Flaco Ruiz sopla el silbato; Nima y Gheco se tapan los oídos.

### Micro-misión R01-N06-P4 · El esqueleto de la copia

```meta
lugar: La tienda de premios
personajes: Nima, Gheco, el Flaco Ruiz
criatura: troll
carta: Copiar | b = a no copia: es el mismo objeto · { ...a } hace una copia nueva
recompensa: xp 10, oro 10
```

#### Escena
El Flaco hizo una «copia» del farol para ponerlo en oferta. Pero al bajarle el precio a la copia, también se le bajó al original.

#### Gheco sugiere
`const oferta = farol;` **no copia** el objeto: crea un segundo nombre para **el mismo** farol. Si cambiás uno, cambia el otro, porque es uno solo.

Para una copia de verdad: `const oferta = { ...farol };`. Los tres puntos (`...`, **spread**) desparraman las propiedades del farol adentro de un objeto nuevo.

#### Desafío
Arreglá la copia para que el original siga a 8.

#### Código inicial
```javascript
const farol = { nombre: 'Farol', precio: 8 };
const oferta = farol;
oferta.precio = 5;

console.log('Original:', farol.precio);
console.log('Oferta:', oferta.precio);
```

#### Salida esperada
```
Original: 8
Oferta: 5
```

#### Solución
```javascript
const farol = { nombre: 'Farol', precio: 8 };
const oferta = { ...farol };
oferta.precio = 5;

console.log('Original:', farol.precio);
console.log('Oferta:', oferta.precio);
```

#### Al superarla
Ahora hay dos faroles en la vitrina: uno caro y uno en oferta. Nadie entiende cuál es la diferencia, pero el de oferta se vende enseguida.

#### Imagen
- Dos faroles de vidrio iguales en una vitrina de feria, uno con un moño rojo de oferta.
- Un troll chiquito y gruñón de feria (sin armas) asoma detrás de la vitrina, contrariado; Nima señala los faroles.

### Micro-misión R01-N06-P5 · El inventario completo

```meta
lugar: La tienda de premios
personajes: Nima, Gheco, el Flaco Ruiz
carta: Object.entries | da [clave, valor] de cada propiedad · se recorre con for…of y se desarma con [k, v]
recompensa: xp 15, monedas 5
```

#### Escena
El Flaco guarda cuántos quedan de cada premio en un solo objeto. Quiere una lista que diga cuántos quedan de cada uno, y avise los que se agotaron.

#### Gheco sugiere
`Object.entries(objeto)` convierte un objeto en una lista de pares `[clave, valor]`. Con `for…of` y desarmando cada par:

```js
for (const [premio, cantidad] of Object.entries(stock)) { ... }
```

En cada vuelta tenés el nombre y la cantidad. Si la cantidad es 0, mostrá `agotado`.

#### Desafío
Mostrá cada premio con su cantidad, o `agotado` si es 0: `oso: 3`, `cometa: agotado`, `silbato: 12`, `farol: 1`.

#### Código inicial
```javascript
const stock = { oso: 3, cometa: 0, silbato: 12, farol: 1 };

```

#### Salida esperada
```
oso: 3
cometa: agotado
silbato: 12
farol: 1
```

#### Solución
```javascript
const stock = { oso: 3, cometa: 0, silbato: 12, farol: 1 };

for (const [premio, cantidad] of Object.entries(stock)) {
  console.log(`${premio}: ${cantidad === 0 ? 'agotado' : cantidad}`);
}
```

#### Al superarla
El Flaco Ruiz pega la lista en la puerta. Por primera vez en años, nadie le pide una cometa que no tiene.

#### Imagen
- La puerta de una tienda de premios de feria con una lista pegada (sin texto legible) y un premio de cada tipo colgado alrededor.
- El Flaco Ruiz, con la galera chiquita, sonríe por primera vez; Gheco le da la mano.

### Micro-misión R01-N06-P6 · El combo de premios

```meta
lugar: La tienda de premios
personajes: Nima, Gheco, el Flaco Ruiz, Lumina
carta: Spread | [...a, ...b] junta arreglos · { ...obj, prop: nuevo } copia y cambia · Object.freeze lo congela
recompensa: xp 15, monedas 5
```

#### Escena
Lumina arma un premio especial para la mejor arquera de la noche: los premios chicos y los grandes en una sola lista, y una copia del farol dorado con el precio en 0, congelada para que nadie la cambie.

#### Gheco sugiere
Los tres puntos también sirven para juntar:

- `[...chicos, ...grandes]` arma un arreglo con los de las dos listas;
- `{ ...farol, precio: 0 }` copia el farol y le cambia el precio.

`Object.freeze(objeto)` lo **congela**: después nadie lo puede cambiar.

El `try { … } catch (error) { … }` ya viene escrito: **prueba** lo que está en el `try` y, si falla, en vez de cortar el programa corre lo del `catch`, con el error en `error`. `error.name` es el **tipo** de error (acá, `TypeError`). Lo vas a ver con calma en R02.

#### Desafío
Armá `todos` y `regalo`. Si el regalo quedó congelado, el intento de cambiarle el precio falla (el `try` ya está escrito).

#### Código inicial
```javascript
const chicos = ['silbato', 'globo'];
const grandes = ['oso', 'farol'];
const farol = { nombre: 'Farol dorado', precio: 20 };

const todos = ___;
const regalo = ___;
try {
  regalo.precio = 99;   // congelado: esto tiene que fallar
} catch (error) {
  console.log('No se puede cambiar:', error.name);
}

console.log(todos);
console.log(regalo, Object.isFrozen(regalo));
```

#### Salida esperada
```
No se puede cambiar: TypeError
[ 'silbato', 'globo', 'oso', 'farol' ]
{ nombre: 'Farol dorado', precio: 0 } true
```

#### Solución
```javascript
const chicos = ['silbato', 'globo'];
const grandes = ['oso', 'farol'];
const farol = { nombre: 'Farol dorado', precio: 20 };

const todos = [...chicos, ...grandes];
const regalo = Object.freeze({ ...farol, precio: 0 });
try {
  regalo.precio = 99;   // congelado: esto tiene que fallar
} catch (error) {
  console.log('No se puede cambiar:', error.name);
}

console.log(todos);
console.log(regalo, Object.isFrozen(regalo));
```

#### Al superarla
El farol dorado queda congelado en precio cero, con un moño amarillo. Lumina lo guarda para más adelante: —Lo vas a necesitar —le dice a Nima, sin explicar para qué.

#### Imagen
- Un farol dorado con un moño amarillo sobre un almohadón de terciopelo, brillando de noche.
- Lumina (luciérnaga enorme, alas de vidrio) lo cubre con una campana de vidrio; Nima y el Flaco Ruiz miran.

## R01-N07 · Funciones

```meta
tipo: tema
padre: R01-N06
precio: 10
criatura: ogre
temas: prog.funciones, prog.alcance
```

### Crónica

En una esquina, un viejo **organito** toca siempre la misma canción, y el **organillero** (un abuelo de sombrero de copa al que todos llaman **Don Tano**) se queja: tiene cien canciones guardadas en rollos de papel, pero no sabe cómo elegir cuál tocar ni cómo cambiarle el ritmo.

—Cada rollo es una **función** —dice {mentor}—. Se escribe una vez, se le pone nombre y se la llama cuando hace falta, con lo que necesite: el ritmo, el volumen, la persona a la que se le dedica.

### Objetivos

- Declarar funciones con `function`, con parámetros y `return`.
- Escribir funciones flecha: `(a, b) => a + b`.
- Usar parámetros por defecto y parámetros rest (`...nums`).
- Pasar funciones como argumento (callbacks), como en `map` y `filter`.
- Entender el alcance: lo que se declara adentro de una función no se ve afuera.

### Antes de empezar

- R01-N05 y R01-N06: arreglos y objetos (ya usaste flechas en `map` y `filter`).

### Explicación

#### Declarar y llamar
```javascript
function saludar(nombre) {
  return `¡Hola, ${nombre}!`;
}
console.log(saludar('Nima'));
```
- `nombre` es un **parámetro**: lo que la función necesita.
- `return` **devuelve** un valor y termina la función. Sin `return`, devuelve `undefined`.

#### Funciones flecha
```javascript
const doble = (n) => n * 2;             // sin llaves: devuelve solo
const sumar = (a, b) => {
  const total = a + b;
  return total;                          // con llaves: hace falta return
};
```

#### Parámetros por defecto y rest
```javascript
function tocar(cancion, veces = 1) { … }      // si no pasan veces, vale 1
function sumarTodas(...fichas) {               // fichas es un arreglo con todos los argumentos
  return fichas.reduce((a, b) => a + b, 0);
}
sumarTodas(1, 2, 3);   // 6
```

#### Funciones que reciben funciones
```javascript
function repetir(veces, accion) {
  for (let i = 1; i <= veces; i++) accion(i);
}
repetir(3, (n) => console.log('Vuelta', n));
```
`accion` es un **callback**: una función que le pasás a otra para que la llame. Es lo que hacen `map`, `filter` y, más adelante, `addEventListener` y `setTimeout`.

#### Alcance
```javascript
function contar() {
  const secreto = 42;
}
console.log(secreto);   // ReferenceError: lo de adentro no se ve afuera
```

#### `this`, en una línea
Adentro de un **método** de un objeto (`obj.metodo()`), `this` es el objeto. Las flechas **no** tienen su propio `this`. Lo vas a ver a fondo con las clases (R03).

### Código de ejemplo

```javascript
function precioFinal(precio, descuento = 0) {
  return precio - precio * descuento;
}
console.log(precioFinal(10));
console.log(precioFinal(10, 0.2));

const cuadrado = (n) => n * n;
console.log([1, 2, 3].map(cuadrado));

function juntarFichas(...rondas) {
  return rondas.reduce((total, r) => total + r, 0);
}
console.log('Fichas:', juntarFichas(3, 5, 2));

const organito = {
  cancion: 'La Cumparsita',
  tocar() {
    return `Suena ${this.cancion}`;
  },
};
console.log(organito.tocar());
```

### Salida esperada

```
10
8
[ 1, 4, 9 ]
Fichas: 10
Suena La Cumparsita
```

### ¿Para qué sirve?

Las funciones son la forma de partir un programa grande en piezas chicas con nombre: cada una hace una cosa y se puede probar sola. En JavaScript, además, las funciones viajan: se pasan a `map`, a un botón, a un temporizador o a un pedido al servidor. Todo lo que viene en el curso depende de esto.

### Errores habituales

**Ogro: olvidarse el `return`.** La función hace la cuenta pero devuelve `undefined`.

**Ogro: llamar sin paréntesis.** `saludar` (sin `()`) es la función misma; `saludar('Nima')` la ejecuta. `console.log(saludar)` muestra `[Function: saludar]`.

**Esqueleto: usar algo declarado adentro de otra función.** `ReferenceError: secreto is not defined`.

**Ogro: el `this` perdido en una flecha.** En un método, `tocar: () => this.cancion` da `undefined`: para métodos, usá la forma `tocar() { … }`.

### Micro-misión R01-N07-P1 · El rollo del saludo

```meta
lugar: La esquina del organito
personajes: Nima, Gheco, Don Tano
carta: function | function nombre(param) { return …; } · se llama con nombre(valor)
recompensa: xp 10, oro 10
```

#### Escena
Don Tano quiere un rollo que salude a cualquiera que pase, con su nombre.

#### Gheco sugiere
Una **función** es una receta con nombre que escribís una vez y usás muchas veces:

```js
function doble(n) {
    return n * 2;
}

console.log(doble(7));   // 14
```

Entre los paréntesis van los **parámetros** (los datos que recibe), y `return` **devuelve** el resultado y termina.

#### Desafío
Escribí la función `saludar` para que el programa muestre los dos saludos.

#### Código inicial
```javascript
// Escribí la función saludar acá


console.log(saludar('Nima'));
console.log(saludar('Gheco'));
```

#### Salida esperada
```
¡Bienvenida a la Feria, Nima!
¡Bienvenida a la Feria, Gheco!
```

#### Solución
```javascript
function saludar(nombre) {
  return `¡Bienvenida a la Feria, ${nombre}!`;
}

console.log(saludar('Nima'));
console.log(saludar('Gheco'));
```

#### Al superarla
El organito toca una melodía nueva y dice el nombre de cada uno que pasa. Gheco pasa tres veces, para escucharlo.

#### Imagen
- Un organito de manivela antiguo con pinturas de colores sobre un carrito, en una esquina de la feria iluminada.
- Don Tano (abuelo de sombrero de copa gastado, bigote blanco grande, saco largo abotonado) gira la manivela; Nima escucha y Gheco baila arriba del organito.

### Micro-misión R01-N07-P2 · Ritmo por defecto

```meta
lugar: La esquina del organito
personajes: Nima, Gheco, Don Tano
carta: Parámetro por defecto | function f(a, b = 1) · si no pasan b, vale 1 · return devuelve el resultado
recompensa: xp 10, oro 10
```

#### Escena
Algunas canciones se tocan una vez y otras varias. Si nadie dice cuántas, Don Tano la toca **una**.

#### Gheco sugiere
Un parámetro puede tener un valor **por defecto**, el que usa si no se lo pasan:

```js
function tocar(cancion, veces = 1) { ... }
```

Si llamás `tocar('vals')`, `veces` vale 1.

`texto.repeat(n)` repite un texto `n` veces: `'la'.repeat(3)` da `'lalala'`.

#### Desafío
Completá la función para que devuelva la canción repetida, separada por espacios y con una nota al final: `'la '.repeat(3)` da `'la la la '`.

#### Código inicial
```javascript
function tocar(cancion, ___) {
  return (cancion + ' ').repeat(veces) + '♪';
}

console.log(tocar('tan'));
console.log(tocar('tin', 3));
```

#### Salida esperada
```
tan ♪
tin tin tin ♪
```

#### Solución
```javascript
function tocar(cancion, veces = 1) {
  return (cancion + ' ').repeat(veces) + '♪';
}

console.log(tocar('tan'));
console.log(tocar('tin', 3));
```

#### Al superarla
Don Tano repite el estribillo tres veces y la gente lo canta con él. La tercera vez, desafinan todos juntos.

#### Imagen
- Rollos de papel perforado de organito apilados en un canasto, con notas musicales doradas flotando en el aire.
- Don Tano marca el ritmo con el pie; una ronda de gente de feria canta.

### Micro-misión R01-N07-P3 · Flechas de luz

```meta
lugar: La esquina del organito
personajes: Nima, Gheco
carta: Funciones flecha | const f = (x) => x * 2; · sin llaves devuelve solo · con llaves, return
recompensa: xp 10, oro 10
```

#### Escena
Gheco dice que las funciones flecha son las favoritas de la Feria: cortas, rápidas, como las flechas de Nima.

#### Gheco sugiere
Las **funciones flecha** son una forma corta de escribir funciones:

```js
const doble = (n) => n * 2;
```

Recibe `n` y devuelve `n * 2`, todo en una línea. Si es una sola expresión, no hace falta `return` ni llaves.

#### Desafío
Escribí `triple` y `esPar` como flechas (`esPar` devuelve `true` si el número es par: `n % 2 === 0`).

#### Código inicial
```javascript
const triple = ___;
const esPar = ___;

console.log(triple(4));
console.log(esPar(4), esPar(7));
console.log([1, 2, 3, 4].filter(esPar).map(triple));
```

#### Salida esperada
```
12
true false
[ 6, 12 ]
```

#### Solución
```javascript
const triple = (n) => n * 3;
const esPar = (n) => n % 2 === 0;

console.log(triple(4));
console.log(esPar(4), esPar(7));
console.log([1, 2, 3, 4].filter(esPar).map(triple));
```

#### Al superarla
Nima mira el código y se ríe: —Son como mis flechas. Salen apenas las pensás.

#### Imagen
- Tres flechas de luz amarilla cruzando el cielo de la feria, dejando estela.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra con costuras amarillas) baja el arco; Gheco aplaude.

### Micro-misión R01-N07-P4 · Todas las fichas

```meta
lugar: La esquina del organito
personajes: Nima, Gheco, Don Tano
carta: Parámetros rest | function f(...nums) · nums es un arreglo con todos los argumentos
recompensa: xp 10, oro 10
```

#### Escena
La gente le deja monedas a Don Tano en el sombrero, de a una o de a puñados. Quiere una función que las sume, sin importar cuántas le pasen.

#### Gheco sugiere
Con tres puntos antes del parámetro (**parámetro rest**), la función acepta **cualquier cantidad** de datos y los junta en un arreglo:

```js
function juntar(...monedas) { ... }

juntar(1, 2, 3);   // monedas es [1, 2, 3]
```

Después, para sumarlas, `reduce`.

#### Desafío
Escribí `juntar` para que sume todos sus argumentos.

#### Código inicial
```javascript
function juntar(___) {
  ___
}

console.log(juntar(1, 2));
console.log(juntar(5, 5, 5, 1));
console.log(juntar());
```

#### Salida esperada
```
3
16
0
```

#### Solución
```javascript
function juntar(...monedas) {
  return monedas.reduce((total, m) => total + m, 0);
}

console.log(juntar(1, 2));
console.log(juntar(5, 5, 5, 1));
console.log(juntar());
```

#### Al superarla
Don Tano da vuelta el sombrero y cuenta: dieciséis fichas y un botón. El botón lo guarda igual.

#### Imagen
- Un sombrero de copa gastado dado vuelta en el piso, lleno de fichas de bronce y un botón.
- Don Tano cuenta las fichas; Gheco sostiene el botón con cara de duda.

### Micro-misión R01-N07-P5 · El rollo que repite

```meta
lugar: La esquina del organito
personajes: Nima, Gheco, Don Tano
carta: Callbacks | una función que recibe otra función · accion(i) la llama · map, filter y setTimeout lo hacen
recompensa: xp 15, monedas 5
```

#### Escena
Don Tano quiere un rollo «comodín»: que repita **cualquier cosa** las veces que le pidan. Lo que se repite se lo pasan como otra función.

#### Gheco sugiere
Una función puede recibir **otra función** como dato. `repetir(veces, accion)` hace un `for` y, en cada vuelta, llama a `accion(i)`.

Al usarla, le pasás una flecha que dice qué hacer en cada vuelta:

```js
repetir(3, (i) => console.log('vuelta', i));
```

#### Desafío
Completá `repetir` y usala para mostrar `Vuelta 1`, `Vuelta 2` y `Vuelta 3`.

#### Código inicial
```javascript
function repetir(veces, accion) {
  // llamá a accion con cada número, de 1 a veces

}

repetir(3, ___);
```

#### Salida esperada
```
Vuelta 1
Vuelta 2
Vuelta 3
```

#### Solución
```javascript
function repetir(veces, accion) {
  for (let i = 1; i <= veces; i++) {
    accion(i);
  }
}

repetir(3, (n) => console.log(`Vuelta ${n}`));
```

#### Al superarla
El rollo comodín gira tres veces y se detiene solo. Don Tano lo pone en el lugar de honor del canasto.

#### Imagen
- Un rollo de papel perforado dorado, distinto de los demás, girando en la boca de un organito.
- Don Tano lo mira con orgullo; Nima y Gheco aplauden.

### Micro-misión R01-N07-P6 · El método del organito

```meta
lugar: La esquina del organito
personajes: Nima, Gheco, Don Tano, Lumina
criatura: ogre
carta: Métodos y this | metodo() { this.prop } · this es el objeto · una flecha no tiene su propio this
recompensa: xp 15, monedas 5
```

#### Escena
Lumina le arma a Don Tano un organito que sabe qué canción tiene puesta. Pero cuando lo prueban, dice *Suena undefined*: un ogro escondido en el código.

#### Gheco sugiere
Adentro de un objeto, `this` quiere decir «este objeto». Pero las funciones **flecha** no tienen su propio `this`: usan el de afuera, y ahí `this.cancion` no existe.

Por eso, un método que usa `this` se escribe como método común, no como flecha:

```js
const organito = {
    cancion: 'vals',
    tocar() { console.log(this.cancion); },
};
```

#### Desafío
Arreglá el método para que muestre `Suena La Cumparsita`.

#### Código inicial
```javascript
const organito = {
  cancion: 'La Cumparsita',
  tocar: () => `Suena ${this?.cancion}`,
};

console.log(organito.tocar());
```

#### Salida esperada
```
Suena La Cumparsita
```

#### Solución
```javascript
const organito = {
  cancion: 'La Cumparsita',
  tocar() {
    return `Suena ${this.cancion}`;
  },
};

console.log(organito.tocar());
```

#### Al superarla
El organito suena con la canción correcta, y toda la esquina se pone a bailar. Lumina hace titilar su luz al compás. —Ahora sí: los Puestos ya hablan nuestra lengua.

#### Imagen
- Una esquina de la feria con gente bailando alrededor de un organito y farolitos de colores.
- Don Tano gira la manivela; Lumina (luciérnaga enorme, alas de vidrio) titila arriba; Nima baila con Gheco en el hombro.

## R01-N08 · Jefe: el Goblin de la Coerción

```meta
tipo: jefe
padre: R01-N07
precio: 10
criatura: dragon
insignia: Ficha del Goblin
insignia_descripcion: Venciste al Goblin de la Coerción: dominás los fundamentos de JavaScript.
usa: prog.variables, prog.condicionales, prog.bucles, col.listas, col.mapas, prog.funciones
```

### Crónica

Al final de la fila de puestos, el **Goblin de la Coerción** abrió su propio puesto: *La Gran Balanza*. Promete el doble de fichas a quien gane su juego, pero hace trampa con todo: suma textos con números, compara con `==`, se come los ceros con `||` y cobra `NaN` como si fuera una ficha.

—Esta vez no le vas a pagar —dice {mentor}—. Vas a jugar su juego con todo lo que aprendiste en los Puestos, y le vas a ganar con las cuentas bien hechas.

### Objetivos

- Integrar todo lo de la rama: variables, tipos, decisiones, bucles, arreglos, objetos y funciones.
- Convertir a propósito los datos que llegan como texto y validarlos.
- Partir un problema en funciones chicas.

### Antes de empezar

- Todos los nodos de los Puestos de Juegos (R01-N01 a R01-N07).

### Explicación

#### Cómo encarar un jefe
1. **Leé la consigna entera** y anotá qué datos entran y qué tiene que salir.
2. **Partilo en funciones chicas**: una convierte, otra valida, otra calcula.
3. **Probá de a una**: ejecutá después de cada función nueva.
4. **Buscá los casos raros**: un texto que no es número, un cero, un dato que falta. El Goblin ataca por ahí.

#### Las trampas del Goblin (y la verdad)
| El Goblin dice… | La verdad |
|---|---|
| "«5» más 5 es 55" | convertí con `Number` antes de sumar |
| "`==` alcanza" | `===` compara tipo y valor |
| "0 fichas es lo mismo que nada" | `??` respeta el cero; `||` no |
| "`NaN` es una ficha" | `Number.isNaN(x)` lo descubre |
| "si no está el dato, no pasa nada" | `?.` y `??` evitan que explote |

### Micro-misión R01-N08-P1 · Los carteles de la Gran Balanza

```meta
lugar: La Gran Balanza del Goblin
personajes: Nima, Gheco, el Goblin de la Coerción
criatura: goblin
carta: Trampa 1 | lo que llega en carteles es texto · Number() a cada uno · Number.isNaN descarta lo que no es número
recompensa: xp 15, monedas 3
```

#### Escena
El Goblin muestra los carteles de las apuestas de la noche, todos de papel: algunos son números y otros no. Dice que suman «35104», y que «diez» también cuenta.

#### Gheco sugiere
Convertí cada cartel con `Number(...)`, quedate solo con los que **no** son `NaN` (con `filter` y `Number.isNaN`), y recién ahí sumalos con `reduce`.

#### Desafío
Mostrá los válidos y el total de verdad: `Válidos: [ 3, 5, 10, 4 ]` y `Total: 22`.

#### Código inicial
```javascript
const carteles = ['3', '5', 'diez', '10', '4', 'mucho'];

const validos = ___;
const total = ___;
console.log('Válidos:', validos);
console.log('Total:', total);
```

#### Salida esperada
```
Válidos: [ 3, 5, 10, 4 ]
Total: 22
```

#### Solución
```javascript
const carteles = ['3', '5', 'diez', '10', '4', 'mucho'];

const validos = carteles.map(Number).filter((n) => !Number.isNaN(n));
const total = validos.reduce((suma, n) => suma + n, 0);
console.log('Válidos:', validos);
console.log('Total:', total);
```

#### Al superarla
El Goblin tacha «35104» en su pizarra y escribe «22», chiquito. La primera trampa cayó.

#### Imagen
- Un puesto de feria enorme y recargado con una balanza gigante de bronce y carteles de papel colgados (sin texto legible).
- El Goblin de la Coerción (goblin de orejas puntiagudas, sonrisa enorme, chaleco a rayas y galera, sin armas) tacha su pizarra con fastidio; Nima, de brazos cruzados.

### Micro-misión R01-N08-P2 · La balanza de dos platos

```meta
lugar: La Gran Balanza del Goblin
personajes: Nima, Gheco, el Goblin de la Coerción
criatura: goblin
carta: Trampa 2 | == convierte antes de comparar · === no · contá cuántos pares son iguales de verdad
recompensa: xp 15, monedas 3
```

#### Escena
El Goblin pone pares de cosas en su balanza y cobra una ficha por cada par «igual». Pero su balanza usa `==`.

#### Gheco sugiere
Recorré los pares con `for…of` y desarmá cada uno en dos variables: `for (const [a, b] of pares)`. Contá solo los que dan `a === b` (iguales en valor y en tipo).

#### Desafío
Mostrá `El Goblin cobra: 4` (con `==`) y `Pares iguales de verdad: 1` (con `===`).

#### Código inicial
```javascript
const pares = [[1, '1'], [0, ''], [2, 2], [null, undefined], ['3', 4]];

let segunElGoblin = 0;
let deVerdad = 0;
for (const [a, b] of pares) {
  if (a == b) segunElGoblin++;
  // contá los iguales de verdad

}
console.log('El Goblin cobra:', segunElGoblin);
console.log('Pares iguales de verdad:', deVerdad);
```

#### Salida esperada
```
El Goblin cobra: 4
Pares iguales de verdad: 1
```

#### Solución
```javascript
const pares = [[1, '1'], [0, ''], [2, 2], [null, undefined], ['3', 4]];

let segunElGoblin = 0;
let deVerdad = 0;
for (const [a, b] of pares) {
  if (a == b) segunElGoblin++;
  if (a === b) deVerdad++;
}
console.log('El Goblin cobra:', segunElGoblin);
console.log('Pares iguales de verdad:', deVerdad);
```

#### Al superarla
La balanza del Goblin se traba de golpe y deja de inclinarse para su lado. Él le da un golpe, pero ya no hay caso.

#### Imagen
- Una balanza de bronce gigante trabada en el medio, con objetos raros en cada plato: una ficha y un papel, una caja vacía y un globo.
- El goblin de chaleco a rayas le da un golpe a la balanza; Gheco se ríe arriba de un plato.

### Micro-misión R01-N08-P3 · El cero que se come

```meta
lugar: La Gran Balanza del Goblin
personajes: Nima, Gheco, el Goblin de la Coerción
criatura: goblin
carta: Trampa 3 | fichas ?? 10 respeta el 0 · el ?. no explota si falta algo
recompensa: xp 15, monedas 3
```

#### Escena
El Goblin le da a cada jugador 10 fichas «si no tiene ninguna». Pero también se las da a los que tienen 0 a propósito (los que ya perdieron), y explota cuando un jugador no trae su bolsa.

#### Gheco sugiere
`jugador.bolsa?.fichas ?? 10`:

- si no hay bolsa, `?.` da `undefined` en vez de error, y `??` pone el 10;
- si la bolsa tiene 0 fichas, `??` deja el 0 (porque 0 es un dato, no «nada»).

#### Desafío
Escribí la función `fichasDe` para que muestre `Nima: 4`, `Bruno: 0` y `Tati: 10`.

#### Código inicial
```javascript
const jugadores = [
  { nombre: 'Nima', bolsa: { fichas: 4 } },
  { nombre: 'Bruno', bolsa: { fichas: 0 } },
  { nombre: 'Tati' },
];

function fichasDe(jugador) {
  return jugador.bolsa.fichas || 10;
}

for (const j of jugadores) {
  console.log(`${j.nombre}: ${fichasDe(j)}`);
}
```

#### Salida esperada
```
Nima: 4
Bruno: 0
Tati: 10
```

#### Solución
```javascript
const jugadores = [
  { nombre: 'Nima', bolsa: { fichas: 4 } },
  { nombre: 'Bruno', bolsa: { fichas: 0 } },
  { nombre: 'Tati' },
];

function fichasDe(jugador) {
  return jugador.bolsa?.fichas ?? 10;
}

for (const j of jugadores) {
  console.log(`${j.nombre}: ${fichasDe(j)}`);
}
```

#### Al superarla
Bruno se queda con su cero (es justo: ya perdió) y Tati recibe sus diez. El Goblin cuenta su caja y le faltan las fichas que regalaba de más.

#### Imagen
- Tres bolsitas de tela con fichas sobre un mostrador: una con pocas, una vacía y un lugar vacío donde falta la tercera.
- Bruno (chaleco rojo) pone cara de resignado; Tati (delantal amarillo) recibe una bolsa nueva; el goblin, furioso.

### Micro-misión R01-N08-P4 · El juego de la Gran Balanza

```meta
lugar: La Gran Balanza del Goblin
personajes: Nima, Gheco, Lumina, el Goblin de la Coerción
criatura: dragon
carta: El jefe | partí en funciones · convertí y validá · acumulá con reduce · decidí con if
recompensa: xp 30, oro 30, monedas 1
item: Ficha del Goblin
```

#### Escena
El juego final del Goblin: tres rondas de tiro. Cada ronda llega como un objeto con los puntos **en texto**, y algunas rondas llegan rotas. Si Nima junta más de 20 puntos válidos, gana el doble de fichas. El Goblin está seguro de que la cuenta le va a dar mal.

#### Gheco sugiere
Separá en partes:

1. `puntosDe(ronda)` convierte la ronda a número y devuelve 0 si no lo es (`Number.isNaN`);
2. sumá todas las rondas con `reduce`, usando `puntosDe` en cada una;
3. decidí el resultado con un `if` (o un ternario).

#### Desafío
Completá las funciones para que el programa muestre exactamente:
- `Ronda 1: 8`
- `Ronda 2: 0 (rota)`
- `Ronda 3: 9`
- `Ronda 4: 7`
- `Total: 24`
- `¡Nima gana el doble!`

#### Código inicial
```javascript
const rondas = [
  { numero: 1, puntos: '8' },
  { numero: 2, puntos: 'ocho' },
  { numero: 3, puntos: '9' },
  { numero: 4, puntos: '7' },
];

function puntosDe(ronda) {
  // convertí a número; si es NaN, devolvé 0

}

for (const ronda of rondas) {
  // mostrá cada ronda (y avisá las rotas)

}

const total = ___;
console.log('Total:', total);
// si el total es mayor que 20: '¡Nima gana el doble!'; si no: 'Gana el Goblin'

```

#### Salida esperada
```
Ronda 1: 8
Ronda 2: 0 (rota)
Ronda 3: 9
Ronda 4: 7
Total: 24
¡Nima gana el doble!
```

#### Solución
```javascript
const rondas = [
  { numero: 1, puntos: '8' },
  { numero: 2, puntos: 'ocho' },
  { numero: 3, puntos: '9' },
  { numero: 4, puntos: '7' },
];

function puntosDe(ronda) {
  const puntos = Number(ronda.puntos);
  return Number.isNaN(puntos) ? 0 : puntos;
}

for (const ronda of rondas) {
  const puntos = puntosDe(ronda);
  const rota = Number.isNaN(Number(ronda.puntos)) ? ' (rota)' : '';
  console.log(`Ronda ${ronda.numero}: ${puntos}${rota}`);
}

const total = rondas.reduce((suma, ronda) => suma + puntosDe(ronda), 0);
console.log('Total:', total);
console.log(total > 20 ? '¡Nima gana el doble!' : 'Gana el Goblin');
```

#### Al superarla
La Gran Balanza se inclina, por fin, hacia el lado justo. El Goblin le paga a Nima el doble, ficha por ficha, y se le cae la galera. Entre las fichas hay una distinta, de bronce oscuro, con una cara de goblin sonriente: **la Ficha del Goblin**.

—Los Puestos ya hablan nuestra lengua —dice {mentor}, y todos los faroles de la fila se prenden a la vez—. Ahora, la avenida.

#### Imagen
- La Gran Balanza de bronce inclinada hacia el lado de Nima, con una lluvia de fichas de bronce cayendo.
- Nima (trenza negra con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas, arco verde) atrapa una ficha oscura con cara de goblin; el Goblin de la Coerción (orejas puntiagudas, chaleco a rayas) pierde la galera.
- Lumina (luciérnaga enorme con alas de vidrio y luz amarilla en el pecho) y todos los faroles de la feria prendidos atrás.
