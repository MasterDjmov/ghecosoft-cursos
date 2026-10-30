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
`const` para lo que no cambia (el nombre) y `let` para lo que sí (las fichas). Después, `console.log` muestra lo que guardaste.

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
`tiros++` suma uno y `fichas -= 1` resta uno. Hacelo dos veces: una por cada tiro.

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
Leé el error: `Assignment to constant variable`. ¿Cuál de las dos cajitas tiene que poder cambiar?

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
Con comillas invertidas, `${precio}` mete el valor de la variable adentro del texto, y `${precio * 3}` mete el resultado de la cuenta.

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
Cada acierto paga 3 fichas. Calculá las fichas ganadas a partir de los aciertos, con una cuenta, no escribiendo el resultado a mano.

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
Empezá con `let total = 0;` y después de cada ronda hacé `total += …`. Mostrá el total parcial después de cada ronda.

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
`typeof valor` devuelve el tipo como texto. Mostralo con `console.log`.

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
El cartel es un **texto**. Convertilo con `Number(…)` antes de sumar.

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
`==` convierte antes de comparar; `===` no. Cambiá la comparación para que no la engañen.

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
`NaN` no es igual a nada, ni a sí mismo. Para saber si un valor es `NaN`, usá `Number.isNaN(valor)`.

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
Convertí cada cartel con `Number` antes de sumar. Mostrá primero la cuenta del Goblin y después la de verdad.

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
Una variable declarada sin valor vale `undefined`. Si querés decir «vacía a propósito», le das `null`.

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
`if (fichas >= 3) { … } else { … }`: lo de la primera llave se ejecuta si se cumple, lo del `else` si no.

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
Con `else if` agregás un camino en el medio. Preguntá primero por el más alto.

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
`switch` compara con `===` cada `case`. Terminá cada caso con `break`, y usá `default` para lo que no está.

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
`vueltas || 3` reemplaza también el 0. Con `vueltas ?? 3`, el 3 se usa **solo** si no hay dato (`null` o `undefined`).

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
`jugadora.caballito` es `undefined`, y no se le puede pedir `.color`. Con `jugadora.caballito?.color` no explota, y con `?? 'sin elegir'` le das un texto por defecto.

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
Armá la condición con `&&` y `||`, y usá el ternario `puede ? 'Pasa' : 'No pasa'` para mostrar el resultado.

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
`for (let i = 5; i >= 1; i--)` empieza en 5 y baja de a uno mientras `i` sea mayor o igual que 1.

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
`for (const cohete of cohetes)` te da cada elemento del arreglo, uno por vuelta.

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
Adentro del `for…of`, `if (cohete === 'mojado') continue;` lo saltea, y `if (cohete === 'roto') break;` corta todo.

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
`while (polvora >= 6)` repite mientras alcance. Adentro, restá los 6 gramos y sumá un cohete. ¡No te olvides de restar, o no termina nunca!

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
`for (const tamaño in precios)` te da cada nombre, y `precios[tamaño]` su precio.

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
Un `for` para las tandas y, adentro, otro `for` para los cohetes de cada tanda. Armá el renglón de cada tanda con `+=` y mostralo al final de esa vuelta.

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
