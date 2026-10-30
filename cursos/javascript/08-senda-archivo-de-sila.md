# RAMA S03 · Senda del Archivo de Sila: buscar, ordenar y contar datos

```meta
tipo: senda
posicion: 8
```

## S03-N01 · Buscar en el Archivo

```meta
tipo: tema
padre: R01-N08
precio: 3
moneda: comodin
criatura: orc
temas: col.listas, func.orden-superior
usa: js.fundamentos, func.lambdas
```

### Crónica

Una paloma blanca aterriza en el puesto de tiro con un paquete atado a la pata: un rollo de papeles y una carta con letra apretada. Es de **Sila**, la archivista del Valle de la Serpiente:

*«Nima: no sé si esto te llega. Anoche pasó por el Valle una niebla espesa y desordenó el Archivo entero. Las fichas de todos los héroes están mezcladas, repetidas, algunas mojadas. Mia dice que en la Feria hablan una lengua rápida para estas cosas. Te mando las fichas en JSON, como las guardamos acá. Si las podés ordenar, te espero.»*

Nima desenrolla el paquete: cientos de fichas. La primera de arriba es la suya.

### Objetivos

- Encontrar **un** elemento con `find` y su posición con `findIndex`.
- Quedarse con **varios** con `filter`.
- Preguntar «¿alguno?» con `some` y «¿todos?» con `every`.
- Buscar sin que importen las mayúsculas ni los acentos.

### Antes de empezar

- Los Puestos de Juegos (R01), sobre todo arreglos con `map`, `filter` y `reduce` (R01-N05) y objetos (R01-N06).
- Si hiciste el curso de Python, es lo mismo que buscar en una lista de diccionarios. Si no, no importa.

### Explicación

#### Las fichas
Cada ficha es un objeto, y el Archivo es un arreglo de fichas:
```javascript
const FICHAS = [
  { id: 1, heroe: 'Mia', region: 'Valle', nivel: 5 },
  { id: 2, heroe: 'Kira', region: 'Forjas', nivel: 6 },
  // …
];
```

#### Uno, varios, alguno, todos
| Método | Pregunta | Devuelve |
|---|---|---|
| `find(f)` | ¿cuál es el primero que cumple? | la ficha, o `undefined` |
| `findIndex(f)` | ¿en qué lugar está? | la posición, o `-1` |
| `filter(f)` | ¿cuáles cumplen? | un arreglo (puede estar vacío) |
| `some(f)` | ¿alguno cumple? | `true` / `false` |
| `every(f)` | ¿todos cumplen? | `true` / `false` |

```javascript
const nima = FICHAS.find((f) => f.heroe === 'Nima');
const delValle = FICHAS.filter((f) => f.region === 'Valle');
const hayNovatos = FICHAS.some((f) => f.nivel === 1);
```

#### Cuando no está
`find` devuelve `undefined` si no encuentra nada, y `undefined.nivel` rompe el programa. Con `?.` y `??` se pregunta sin romper:
```javascript
const zed = FICHAS.find((f) => f.heroe === 'Zed');
console.log(zed?.nivel ?? 'no está en el Archivo');
```

#### Sin mayúsculas ni acentos
```javascript
const limpio = (texto) => texto.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase();
limpio('Tizón');   // 'tizon'
```
`normalize('NFD')` separa la letra de su acento (la `ó` pasa a `o` + `´`), y el `replace` saca los acentos.

### Código de ejemplo

```javascript
const FICHAS = [
  { id: 1, heroe: 'Mia', region: 'Valle', nivel: 5 },
  { id: 2, heroe: 'Kira', region: 'Forjas', nivel: 6 },
  { id: 3, heroe: 'Nilo', region: 'Puerto', nivel: 4 },
  { id: 4, heroe: 'Nima', region: 'Valle', nivel: 4 },
];

console.log(FICHAS.find((f) => f.nivel > 4).heroe);
console.log(FICHAS.findIndex((f) => f.heroe === 'Nilo'));
console.log(FICHAS.filter((f) => f.region === 'Valle').map((f) => f.heroe));
console.log(FICHAS.some((f) => f.nivel > 5), FICHAS.every((f) => f.nivel > 5));
console.log(FICHAS.find((f) => f.heroe === 'Zed')?.nivel ?? 'no está');
```

### Salida esperada

```
Mia
2
[ 'Mia', 'Nima' ]
true false
no está
```

### ¿Para qué sirve?

Buscar un alumno por su DNI, los productos de una categoría, saber si alguna tarea está vencida o si todas están entregadas: cada buscador de una página es un `find` o un `filter`. Sacar los acentos es lo que hace que «tizon» encuentre a «Tizón».

### Errores habituales

**Orco: usar lo que `find` no encontró.** `FICHAS.find(…).nivel` rompe si no hay ninguno. Preguntá con `?.`.

**Ogro: `filter` cuando querías uno.** `filter` siempre devuelve un **arreglo**, aunque encuentre uno solo: `filter(…).nivel` da `undefined`. Para uno, `find`.

**Goblin: `=` en vez de `===`.** `find((f) => f.heroe = 'Nima')` no compara: **cambia** el nombre de la primera ficha y la devuelve.

### Micro-misión S03-N01-P1 · La ficha de arriba

```meta
lugar: El puesto de tiro, con el paquete del Valle
personajes: Nima, Gheco
carta: find | const ficha = FICHAS.find((f) => f.heroe === 'Nima')
recompensa: xp 10, oro 10
```

#### Escena
La ficha de arriba es la de Nima, pero Gheco quiere ver si la encuentra **buscando**, no mirando.

#### Gheco sugiere
Usá `find` para encontrar la ficha de `Nima` y mostrá `Nima: nivel 4, inventario: soga, brújula, pan`.

#### Desafío
Mostrá la ficha de Nima.

#### Código inicial
```javascript
const FICHAS = [
  { id: 9, heroe: 'Sila', region: 'Valle', nivel: 7 },
  { id: 2, heroe: 'Kira', region: 'Forjas', nivel: 6 },
  { id: 4, heroe: 'Nima', region: 'Valle', nivel: 4, inventario: ['soga', 'brújula', 'pan'] },
  { id: 3, heroe: 'Nilo', region: 'Puerto', nivel: 4 },
];

const ficha = FICHAS[0];
console.log(`${ficha.heroe}: nivel ${ficha.nivel}`);
```

#### Salida esperada
```
Nima: nivel 4, inventario: soga, brújula, pan
```

#### Solución
```javascript
const FICHAS = [
  { id: 9, heroe: 'Sila', region: 'Valle', nivel: 7 },
  { id: 2, heroe: 'Kira', region: 'Forjas', nivel: 6 },
  { id: 4, heroe: 'Nima', region: 'Valle', nivel: 4, inventario: ['soga', 'brújula', 'pan'] },
  { id: 3, heroe: 'Nilo', region: 'Puerto', nivel: 4 },
];

const ficha = FICHAS.find((f) => f.heroe === 'Nima');
console.log(`${ficha.heroe}: nivel ${ficha.nivel}, inventario: ${ficha.inventario.join(', ')}`);
```

#### Al superarla
*Nima: nivel 4, inventario: soga, brújula, pan.* —Ya no tengo el pan —dice Nima—. Me lo comí en las Forjas.

#### Imagen
- Una paloma blanca con un rollo de papeles atado a la pata, posada en el mostrador del puesto de tiro de la Feria, de noche.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) desenrolla una ficha de papel con un sello verde del Valle.

### Micro-misión S03-N01-P2 · Los del Valle

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco
carta: filter | FICHAS.filter((f) => f.region === 'Valle').map((f) => f.heroe)
recompensa: xp 10, oro 10
```

#### Escena
Sila quiere saber, antes que nada, quiénes son del **Valle**: son los primeros que tiene que volver a guardar.

#### Gheco sugiere
Quedate con las fichas del Valle con `filter`, y mostrá sus nombres separados por coma y cuántas son.

#### Desafío
`Del Valle (3): Sila, Nima, Mia`.

#### Código inicial
```javascript
const FICHAS = [
  { id: 9, heroe: 'Sila', region: 'Valle', nivel: 7 },
  { id: 2, heroe: 'Kira', region: 'Forjas', nivel: 6 },
  { id: 4, heroe: 'Nima', region: 'Valle', nivel: 4 },
  { id: 3, heroe: 'Nilo', region: 'Puerto', nivel: 4 },
  { id: 6, heroe: 'Tesela', region: 'Talleres', nivel: 9 },
  { id: 1, heroe: 'Mia', region: 'Valle', nivel: 5 },
];

const delValle = FICHAS.find((f) => f.region === 'Valle');
console.log(`Del Valle: ${delValle.heroe}`);
```

#### Salida esperada
```
Del Valle (3): Sila, Nima, Mia
```

#### Solución
```javascript
const FICHAS = [
  { id: 9, heroe: 'Sila', region: 'Valle', nivel: 7 },
  { id: 2, heroe: 'Kira', region: 'Forjas', nivel: 6 },
  { id: 4, heroe: 'Nima', region: 'Valle', nivel: 4 },
  { id: 3, heroe: 'Nilo', region: 'Puerto', nivel: 4 },
  { id: 6, heroe: 'Tesela', region: 'Talleres', nivel: 9 },
  { id: 1, heroe: 'Mia', region: 'Valle', nivel: 5 },
];

const delValle = FICHAS.filter((f) => f.region === 'Valle');
console.log(`Del Valle (${delValle.length}): ${delValle.map((f) => f.heroe).join(', ')}`);
```

#### Al superarla
Tres fichas del Valle, separadas del montón. Gheco las apila con la cola.

#### Imagen
- Tres fichas de papel con el sello verde del Valle apiladas aparte, sobre un mostrador lleno de fichas mezcladas.
- Gheco, el geco, empuja la pila con la cola.

### Micro-misión S03-N01-P3 · ¿Alguno? ¿Todos?

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Bruno
carta: some y every | FICHAS.some((f) => …) · FICHAS.every((f) => …)
recompensa: xp 10, oro 10
```

#### Escena
Bruno se arrima a mirar. —¿Hay alguno de nivel 1, como yo? ¿Y todos tienen región?

#### Gheco sugiere
Respondé las dos preguntas con `some` y `every`, y una tercera: ¿todos tienen nivel mayor que 0?

#### Desafío
Tres renglones: `¿Alguno de nivel 1? sí`, `¿Todos con región? no` y `¿Todos con nivel? sí`.

#### Código inicial
```javascript
const FICHAS = [
  { id: 7, heroe: 'Teo', region: 'Talleres', nivel: 1 },
  { id: 2, heroe: 'Kira', region: 'Forjas', nivel: 6 },
  { id: 12, heroe: '???', nivel: 3 },
  { id: 4, heroe: 'Nima', region: 'Valle', nivel: 4 },
];

const siNo = (respuesta) => (respuesta ? 'sí' : 'no');
console.log(`¿Alguno de nivel 1? ${siNo(FICHAS[0].nivel === 1)}`);
```

#### Salida esperada
```
¿Alguno de nivel 1? sí
¿Todos con región? no
¿Todos con nivel? sí
```

#### Solución
```javascript
const FICHAS = [
  { id: 7, heroe: 'Teo', region: 'Talleres', nivel: 1 },
  { id: 2, heroe: 'Kira', region: 'Forjas', nivel: 6 },
  { id: 12, heroe: '???', nivel: 3 },
  { id: 4, heroe: 'Nima', region: 'Valle', nivel: 4 },
];

const siNo = (respuesta) => (respuesta ? 'sí' : 'no');
console.log(`¿Alguno de nivel 1? ${siNo(FICHAS.some((f) => f.nivel === 1))}`);
console.log(`¿Todos con región? ${siNo(FICHAS.every((f) => f.region !== undefined))}`);
console.log(`¿Todos con nivel? ${siNo(FICHAS.every((f) => f.nivel > 0))}`);
```

#### Al superarla
Hay uno de nivel 1 (Teo, el de los Talleres), y una ficha **sin región**: la 12, la de los signos de pregunta. Bruno la mira de cerca. —¿Quién es ese?

#### Imagen
- Una ficha de papel manchada con signos de pregunta en lugar del nombre, sin sello de región, iluminada por un farol.
- Bruno (12 años, pelo rizado, gorra al revés, chaleco rojo) la mira con lupa.

### Micro-misión S03-N01-P4 · El que no está

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco
carta: ?. y ?? | FICHAS.find(…)?.nivel ?? 'no está en el Archivo'
recompensa: xp 15, monedas 5
```

#### Escena
La carta de Sila pide tres fichas: la de Kira, la de **Zed** y la de Iara. Nima busca la de Zed y el programa explota.

#### Gheco sugiere
Escribí `nivelDe(nombre)`, que devuelve el nivel o `'no está en el Archivo'`, sin romper. Usá `?.` y `??`.

#### Desafío
Que muestre las tres, aunque una falte.

#### Código inicial
```javascript
const FICHAS = [
  { id: 2, heroe: 'Kira', region: 'Forjas', nivel: 6 },
  { id: 8, heroe: 'Iara', region: 'Puerto', nivel: 3 },
  { id: 4, heroe: 'Nima', region: 'Valle', nivel: 4 },
];

function nivelDe(nombre) {
  return FICHAS.find((f) => f.heroe === nombre).nivel;
}

for (const nombre of ['Kira', 'Zed', 'Iara']) {
  console.log(`${nombre}: ${nivelDe(nombre)}`);
}
```

#### Salida esperada
```
Kira: 6
Zed: no está en el Archivo
Iara: 3
```

#### Solución
```javascript
const FICHAS = [
  { id: 2, heroe: 'Kira', region: 'Forjas', nivel: 6 },
  { id: 8, heroe: 'Iara', region: 'Puerto', nivel: 3 },
  { id: 4, heroe: 'Nima', region: 'Valle', nivel: 4 },
];

function nivelDe(nombre) {
  return FICHAS.find((f) => f.heroe === nombre)?.nivel ?? 'no está en el Archivo';
}

for (const nombre of ['Kira', 'Zed', 'Iara']) {
  console.log(`${nombre}: ${nivelDe(nombre)}`);
}
```

#### Al superarla
*Zed: no está en el Archivo.* Nima anota al margen de la carta: *«Zed no es del Valle. ¿Del Imperio, quizás?»*

#### Imagen
- Un casillero vacío en un archivo de madera, con una telaraña, iluminado por un farol de la Feria.
- Nima anota algo al margen de una carta, pensativa.

### Micro-misión S03-N01-P5 · Tizon, sin acento

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Tati
carta: Sin acentos | texto.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase()
recompensa: xp 15, monedas 5
```

#### Escena
Tati quiere ayudar a buscar, pero escribe todo en minúsculas y sin acentos: `tizon`, `brujula`. Y así no encuentra nada.

#### Gheco sugiere
Escribí `limpio(texto)`, que saca acentos y mayúsculas, y `buscar(texto)`, que devuelve los nombres de las fichas cuyo `heroe` **contiene** lo buscado (los dos pasados por `limpio`).

#### Desafío
Que `tizon` encuentre a Tizón y `ni` encuentre a Nilo y a Nima.

#### Código inicial
```javascript
const FICHAS = [
  { id: 5, heroe: 'Tizón', region: 'Forjas', nivel: 2 },
  { id: 3, heroe: 'Nilo', region: 'Puerto', nivel: 4 },
  { id: 4, heroe: 'Nima', region: 'Valle', nivel: 4 },
  { id: 10, heroe: 'Ámbar', region: 'Talleres', nivel: 2 },
];

function buscar(texto) {
  return FICHAS.filter((f) => f.heroe.includes(texto)).map((f) => f.heroe);
}

for (const texto of ['tizon', 'ni', 'AMBAR', 'zed']) {
  console.log(`«${texto}» → ${buscar(texto).join(', ') || '(nada)'}`);
}
```

#### Salida esperada
```
«tizon» → Tizón
«ni» → Nilo, Nima
«AMBAR» → Ámbar
«zed» → (nada)
```

#### Solución
```javascript
const FICHAS = [
  { id: 5, heroe: 'Tizón', region: 'Forjas', nivel: 2 },
  { id: 3, heroe: 'Nilo', region: 'Puerto', nivel: 4 },
  { id: 4, heroe: 'Nima', region: 'Valle', nivel: 4 },
  { id: 10, heroe: 'Ámbar', region: 'Talleres', nivel: 2 },
];

const limpio = (texto) => texto.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase();

function buscar(texto) {
  return FICHAS.filter((f) => limpio(f.heroe).includes(limpio(texto))).map((f) => f.heroe);
}

for (const texto of ['tizon', 'ni', 'AMBAR', 'zed']) {
  console.log(`«${texto}» → ${buscar(texto).join(', ') || '(nada)'}`);
}
```

#### Al superarla
Tati escribe `tizon`, sin acento y en minúsculas, y aparece Tizón. Escribe `AMBAR`, gritando, y aparece Ámbar. —¡El buscador me entiende!

#### Imagen
- Tati (11 años, dos colitas, delantal amarillo) escribe en una pizarrita con tiza, y las fichas de papel se acomodan solas.
- Una ficha con un acento de madera que se despega y sale volando.

## S03-N02 · Ordenar las fichas

```meta
tipo: tema
padre: S03-N01
precio: 10
criatura: goblin
temas: alg.ordenamiento, func.orden-superior
usa: col.listas, prog.cadenas
```

### Crónica

Las fichas ya se encuentran, pero siguen **revueltas**. Sila las guardaba en orden: por nivel en un cajón, por nombre en otro. Nima prueba con `sort()`, el que ordena solo, y el Goblin de la Coerción, que se había colado en el paquete, se ríe desde adentro: el nivel 10 quedó antes que el 9.

### Objetivos

- Entender por qué `sort()` sin nada ordena **como texto**, y ordenar números con `(a, b) => a - b`.
- Ordenar nombres en castellano (con Ñ y acentos) con `localeCompare`.
- Ordenar por dos criterios: nivel y, si empatan, nombre.
- Ordenar sin cambiar el original (`toSorted`) y quedarse con los primeros (`slice`).

### Antes de empezar

- S03-N01 (buscar en el Archivo).

### Explicación

#### La trampa del `sort`
```javascript
[10, 9, 1].sort();   // [1, 10, 9]: ¡los compara como textos!
```
Sin nada, `sort` convierte todo a texto y compara letra por letra: `'10'` va antes que `'9'` porque `'1'` va antes que `'9'`. Es el Goblin otra vez.

#### La función que compara
`sort` recibe una función que compara **dos** elementos, `a` y `b`, y devuelve:
- un número **negativo** si `a` va antes;
- **positivo** si `b` va antes;
- **0** si da igual.
```javascript
numeros.sort((a, b) => a - b);                     // de menor a mayor
FICHAS.sort((a, b) => b.nivel - a.nivel);          // nivel, de mayor a menor
```

#### Los nombres
`'Ñandú' < 'Oso'` da `false`: la Ñ está muy lejos en la tabla de caracteres. Para ordenar como en el diccionario:
```javascript
FICHAS.sort((a, b) => a.heroe.localeCompare(b.heroe, 'es'));
```

#### Dos criterios
```javascript
FICHAS.sort((a, b) => b.nivel - a.nivel || a.heroe.localeCompare(b.heroe, 'es'));
```
Si la resta da 0 (empate), el `||` pasa al segundo criterio.

#### Sin tocar el original
`sort` **cambia** el arreglo. `toSorted` devuelve uno nuevo y deja el original como estaba.

### Código de ejemplo

```javascript
console.log([10, 9, 1, 25].sort());
console.log([10, 9, 1, 25].sort((a, b) => a - b));

const nombres = ['Oso', 'Ñandú', 'Ámbar', 'Nilo'];
console.log([...nombres].sort());
console.log(nombres.toSorted((a, b) => a.localeCompare(b, 'es')));
console.log('El original:', nombres);
```

### Salida esperada

```
[ 1, 10, 25, 9 ]
[ 1, 9, 10, 25 ]
[ 'Nilo', 'Oso', 'Ámbar', 'Ñandú' ]
[ 'Ámbar', 'Nilo', 'Ñandú', 'Oso' ]
El original: [ 'Oso', 'Ñandú', 'Ámbar', 'Nilo' ]
```

### ¿Para qué sirve?

Las tablas que se ordenan tocando la columna, el ranking de un juego, los precios de menor a mayor, la lista de alumnos por apellido. Ordenar bien los nombres en castellano es lo que hace que «Ñoño» no quede después de «Zorro».

### Errores habituales

**Goblin: `sort()` con números.** Siempre pasale la función.

**Ogro: el `sort` que cambió el original.** Si después usás el arreglo «de antes», ya no está. Usá `toSorted` o copiá con `[...arreglo]`.

**Ogro: devolver `true` o `false`.** `(a, b) => a > b` no sirve: `sort` necesita un número negativo, cero o positivo.

### Micro-misión S03-N02-P1 · El 10 antes que el 9

```meta
lugar: El puesto de tiro, el cajón de los niveles
personajes: Nima, Gheco, el Goblin de la Coerción
carta: Números | niveles.sort((a, b) => a - b)
recompensa: xp 10, oro 10
```

#### Escena
El Goblin asoma la cabeza entre las fichas, con la galera torcida. —¡Ordenado! —dice, y señala: `1, 10, 2, 9`.

#### Gheco sugiere
Pasale a `sort` la función que compara números: de menor a mayor.

#### Desafío
`Niveles: 1, 2, 4, 9, 10`.

#### Código inicial
```javascript
const niveles = [9, 1, 10, 4, 2];
niveles.sort();
console.log(`Niveles: ${niveles.join(', ')}`);
```

#### Salida esperada
```
Niveles: 1, 2, 4, 9, 10
```

#### Solución
```javascript
const niveles = [9, 1, 10, 4, 2];
niveles.sort((a, b) => a - b);
console.log(`Niveles: ${niveles.join(', ')}`);
```

#### Al superarla
El 10 vuelve al final, donde va. El Goblin se cala la galera, ofendido, y se esconde otra vez en el paquete.

#### Imagen
- Un goblin de orejas puntiagudas, galera y chaleco a rayas asoma entre fichas de papel con números, sonriendo pícaro.
- Cinco fichas con números en fila, acomodadas por tamaño.

### Micro-misión S03-N02-P2 · Ñandú y Ámbar

```meta
lugar: El puesto de tiro, el cajón de los nombres
personajes: Nima, Gheco
carta: localeCompare | nombres.sort((a, b) => a.localeCompare(b, 'es'))
recompensa: xp 10, oro 10
```

#### Escena
En el cajón de los nombres, Ámbar (la del carrito de los Talleres) quedó al final, después de Teo. Y el Ñandú de las Forjas, después de todos.

#### Gheco sugiere
Ordená los nombres con `localeCompare` en castellano.

#### Desafío
Que Ámbar quede primero y Ñandú entre Nima y Teo.

#### Código inicial
```javascript
const nombres = ['Teo', 'Ñandú', 'Ámbar', 'Nima', 'Kira', 'Elefa'];
nombres.sort();
console.log(nombres.join(' · '));
```

#### Salida esperada
```
Ámbar · Elefa · Kira · Nima · Ñandú · Teo
```

#### Solución
```javascript
const nombres = ['Teo', 'Ñandú', 'Ámbar', 'Nima', 'Kira', 'Elefa'];
nombres.sort((a, b) => a.localeCompare(b, 'es'));
console.log(nombres.join(' · '));
```

#### Al superarla
*Ámbar · Elefa · Kira · Nima · Ñandú · Teo.* Como en el diccionario del Valle.

#### Imagen
- Un cajón de madera con separadores de letras talladas, incluida una Ñ, y fichas acomodadas en orden.
- Gheco sostiene la ficha de la Ñ con orgullo.

### Micro-misión S03-N02-P3 · El cajón de los niveles

```meta
lugar: El puesto de tiro, el cajón de los niveles
personajes: Nima, Gheco
carta: Dos criterios | (a, b) => b.nivel - a.nivel || a.heroe.localeCompare(b.heroe, 'es')
recompensa: xp 10, oro 10
```

#### Escena
Sila guarda las fichas del nivel más alto al más bajo. Y si dos tienen el mismo nivel, por nombre.

#### Gheco sugiere
Ordená por nivel de mayor a menor y, si empatan, por nombre. Mostrá cada una como `7 · Sila`.

#### Desafío
Nilo y Nima tienen nivel 4: tiene que quedar primero Nilo.

#### Código inicial
```javascript
const FICHAS = [
  { heroe: 'Nima', nivel: 4 },
  { heroe: 'Teo', nivel: 1 },
  { heroe: 'Sila', nivel: 7 },
  { heroe: 'Nilo', nivel: 4 },
  { heroe: 'Kira', nivel: 6 },
  { heroe: 'Iara', nivel: 3 },
];

FICHAS.sort((a, b) => b.nivel - a.nivel);
for (const f of FICHAS) console.log(`${f.nivel} · ${f.heroe}`);
```

#### Salida esperada
```
7 · Sila
6 · Kira
4 · Nilo
4 · Nima
3 · Iara
1 · Teo
```

#### Solución
```javascript
const FICHAS = [
  { heroe: 'Nima', nivel: 4 },
  { heroe: 'Teo', nivel: 1 },
  { heroe: 'Sila', nivel: 7 },
  { heroe: 'Nilo', nivel: 4 },
  { heroe: 'Kira', nivel: 6 },
  { heroe: 'Iara', nivel: 3 },
];

FICHAS.sort((a, b) => b.nivel - a.nivel || a.heroe.localeCompare(b.heroe, 'es'));
for (const f of FICHAS) console.log(`${f.nivel} · ${f.heroe}`);
```

#### Al superarla
El cajón queda como lo tenía Sila. Nima se ve a sí misma en el medio de la lista, justo después de Nilo. —Algún día lo paso.

#### Imagen
- Un cajón de archivo con fichas en escalera, de la más alta a la más baja, cada una con un número tallado.
- Nima señala su ficha, en el medio.

### Micro-misión S03-N02-P4 · El orden de llegada

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco
carta: toSorted | const porNombre = FICHAS.toSorted(…) · FICHAS queda igual
recompensa: xp 15, monedas 5
```

#### Escena
La carta de Sila tenía una posdata: *«No pierdas el orden en que te llegaron: es el orden en que la niebla las fue tirando, y quiero entender por dónde pasó.»* Nima ya había ordenado el arreglo con `sort`… y el orden de llegada se perdió.

#### Gheco sugiere
Usá `toSorted` para tener la lista **por nombre** sin tocar `FICHAS`. Mostrá las dos.

#### Desafío
`Por nombre: …` y `Como llegaron: …`, cada una en su renglón.

#### Código inicial
```javascript
const FICHAS = [
  { heroe: 'Tizón', nivel: 2 },
  { heroe: 'Mia', nivel: 5 },
  { heroe: 'Iara', nivel: 3 },
  { heroe: 'Kira', nivel: 6 },
];

const porNombre = FICHAS.sort((a, b) => a.heroe.localeCompare(b.heroe, 'es'));
console.log(`Por nombre: ${porNombre.map((f) => f.heroe).join(', ')}`);
console.log(`Como llegaron: ${FICHAS.map((f) => f.heroe).join(', ')}`);
```

#### Salida esperada
```
Por nombre: Iara, Kira, Mia, Tizón
Como llegaron: Tizón, Mia, Iara, Kira
```

#### Solución
```javascript
const FICHAS = [
  { heroe: 'Tizón', nivel: 2 },
  { heroe: 'Mia', nivel: 5 },
  { heroe: 'Iara', nivel: 3 },
  { heroe: 'Kira', nivel: 6 },
];

const porNombre = FICHAS.toSorted((a, b) => a.heroe.localeCompare(b.heroe, 'es'));
console.log(`Por nombre: ${porNombre.map((f) => f.heroe).join(', ')}`);
console.log(`Como llegaron: ${FICHAS.map((f) => f.heroe).join(', ')}`);
```

#### Al superarla
Las dos listas, una al lado de la otra. Mirando el orden de llegada, Nima lo ve: la niebla entró por las Forjas (Tizón), pasó por el Valle (Mia), el Puerto (Iara) y volvió a las Forjas (Kira). —Dio una vuelta —dice—. Como buscando algo.

#### Imagen
- Dos columnas de fichas de papel sobre el mostrador; sobre una, un mapa chiquito dibujado a mano con el recorrido de una niebla.
- Nima, con el ceño fruncido, sigue el recorrido con el dedo.

### Micro-misión S03-N02-P5 · Los tres primeros

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Bruno
carta: Podio | lista.toSorted(…).slice(0, 3).map((f, i) => `${i + 1}. …`)
recompensa: xp 15, monedas 5
```

#### Escena
Bruno quiere un **podio**, como en el puesto de tiro: los tres de nivel más alto del Archivo.

#### Gheco sugiere
Ordená de mayor a menor (sin cambiar el original), quedate con los tres primeros con `slice(0, 3)` y mostralos numerados: `1. Tesela (9)`.

#### Desafío
El podio del Archivo.

#### Código inicial
```javascript
const FICHAS = [
  { heroe: 'Nima', nivel: 4 },
  { heroe: 'Tesela', nivel: 9 },
  { heroe: 'Sila', nivel: 7 },
  { heroe: 'Teo', nivel: 1 },
  { heroe: 'Kira', nivel: 6 },
  { heroe: 'Mia', nivel: 5 },
];

const podio = FICHAS.slice(0, 3);
podio.forEach((f, i) => console.log(`${i + 1}. ${f.heroe} (${f.nivel})`));
```

#### Salida esperada
```
1. Tesela (9)
2. Sila (7)
3. Kira (6)
```

#### Solución
```javascript
const FICHAS = [
  { heroe: 'Nima', nivel: 4 },
  { heroe: 'Tesela', nivel: 9 },
  { heroe: 'Sila', nivel: 7 },
  { heroe: 'Teo', nivel: 1 },
  { heroe: 'Kira', nivel: 6 },
  { heroe: 'Mia', nivel: 5 },
];

const podio = FICHAS.toSorted((a, b) => b.nivel - a.nivel).slice(0, 3);
podio.forEach((f, i) => console.log(`${i + 1}. ${f.heroe} (${f.nivel})`));
```

#### Al superarla
*1. Tesela (9) · 2. Sila (7) · 3. Kira (6).* Bruno aplaude. —¡La archivista está segunda!

#### Imagen
- Un podio de madera de feria con tres fichas de papel en los escalones, con cintas de colores.
- Bruno aplaude con la gorra en la mano.

## S03-N03 · Agrupar y contar

```meta
tipo: tema
padre: S03-N02
precio: 10
criatura: ogre
temas: col.mapas, col.conjuntos, func.orden-superior
usa: col.listas
```

### Crónica

Ya están ordenadas. Ahora Sila necesita saber **cuántas** hay de cada región, para preparar los cajones. —En la Feria cuento las fichas del puesto de tiro de a una —dice Nima—. Con trescientas no termino nunca. —Gheco le muestra el `reduce` del puesto de Doña Mirta: el que junta todo en uno.

### Objetivos

- Contar por grupo con `reduce` y un objeto.
- Sacar los repetidos con `Set`.
- Agrupar en un objeto de listas, con `??=`.
- Calcular promedios por grupo y recorrer un objeto con `Object.entries`.

### Antes de empezar

- S03-N02 y `reduce` (R01-N05).

### Explicación

#### Contar con `reduce`
```javascript
const porRegion = FICHAS.reduce((cuenta, f) => {
  cuenta[f.region] = (cuenta[f.region] ?? 0) + 1;
  return cuenta;
}, {});
// { Valle: 3, Forjas: 2, Puerto: 2 }
```
El `{}` del final es el valor con el que arranca: un objeto vacío.

#### Sin repetidos
Un `Set` guarda cada valor **una sola vez**:
```javascript
const regiones = [...new Set(FICHAS.map((f) => f.region))];
```

#### Agrupar
```javascript
const grupos = {};
for (const f of FICHAS) {
  grupos[f.region] ??= [];        // si no hay lista, crearla
  grupos[f.region].push(f.heroe);
}
```

#### Recorrer un objeto
```javascript
for (const [region, cantidad] of Object.entries(porRegion)) {
  console.log(`${region}: ${cantidad}`);
}
```
`Object.entries` lo convierte en una lista de pares `[clave, valor]`, que se puede ordenar como cualquier arreglo.

### Código de ejemplo

```javascript
const FICHAS = [
  { heroe: 'Mia', region: 'Valle', nivel: 5 },
  { heroe: 'Kira', region: 'Forjas', nivel: 6 },
  { heroe: 'Nima', region: 'Valle', nivel: 4 },
  { heroe: 'Tizón', region: 'Forjas', nivel: 2 },
  { heroe: 'Sila', region: 'Valle', nivel: 7 },
];

const cuenta = FICHAS.reduce((c, f) => {
  c[f.region] = (c[f.region] ?? 0) + 1;
  return c;
}, {});
console.log(cuenta);
console.log([...new Set(FICHAS.map((f) => f.region))]);
console.log(Object.entries(cuenta));
```

### Salida esperada

```
{ Valle: 3, Forjas: 2 }
[ 'Valle', 'Forjas' ]
[ [ 'Valle', 3 ], [ 'Forjas', 2 ] ]
```

### ¿Para qué sirve?

Las estadísticas de cualquier sistema son contar y agrupar: ventas por mes, alumnos por curso, votos por candidato, visitas por país. Es el mismo `reduce`, con más datos.

### Errores habituales

**Ogro: olvidarse el `return` del `reduce`.** La segunda vuelta recibe `undefined` y `undefined['Valle']` rompe.

**Ogro: olvidarse el valor inicial.** Sin el `{}`, el `reduce` arranca con la primera ficha como si fuera la cuenta.

**Goblin: `cuenta[region] + 1` sin el `?? 0`.** La primera vez es `undefined + 1`, que da `NaN`.

### Micro-misión S03-N03-P1 · Cuántas de cada región

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Doña Mirta
carta: Contar | FICHAS.reduce((c, f) => { c[f.region] = (c[f.region] ?? 0) + 1; return c; }, {})
recompensa: xp 10, oro 10
```

#### Escena
Doña Mirta se acerca con una bandeja de pan con miel. —Yo cuento los panes de cada horno así: un palito por pan, y a la noche sumo. —Es un `reduce` —dice Gheco.

#### Gheco sugiere
Contá cuántas fichas hay de cada región con `reduce`, y mostrá cada una en su renglón: `Valle: 3`.

#### Desafío
Las cuentas, en el orden en que aparecen las regiones.

#### Código inicial
```javascript
const FICHAS = [
  { heroe: 'Mia', region: 'Valle' },
  { heroe: 'Kira', region: 'Forjas' },
  { heroe: 'Nilo', region: 'Puerto' },
  { heroe: 'Nima', region: 'Valle' },
  { heroe: 'Tizón', region: 'Forjas' },
  { heroe: 'Iara', region: 'Puerto' },
  { heroe: 'Sila', region: 'Valle' },
];

const cuenta = FICHAS.reduce((c, f) => {
  c[f.region] = c[f.region] + 1;
  return c;
}, {});
for (const region in cuenta) console.log(`${region}: ${cuenta[region]}`);
```

#### Salida esperada
```
Valle: 3
Forjas: 2
Puerto: 2
```

#### Solución
```javascript
const FICHAS = [
  { heroe: 'Mia', region: 'Valle' },
  { heroe: 'Kira', region: 'Forjas' },
  { heroe: 'Nilo', region: 'Puerto' },
  { heroe: 'Nima', region: 'Valle' },
  { heroe: 'Tizón', region: 'Forjas' },
  { heroe: 'Iara', region: 'Puerto' },
  { heroe: 'Sila', region: 'Valle' },
];

const cuenta = FICHAS.reduce((c, f) => {
  c[f.region] = (c[f.region] ?? 0) + 1;
  return c;
}, {});
for (const region in cuenta) console.log(`${region}: ${cuenta[region]}`);
```

#### Al superarla
*Valle: 3, Forjas: 2, Puerto: 2.* Antes decía `NaN` en todas: el Goblin otra vez. Doña Mirta le deja un pan a Gheco.

#### Imagen
- Doña Mirta (petisa y redonda, delantal floreado cerrado, pañuelo en la cabeza) con una bandeja de panes, al lado de tres montoncitos de fichas.
- Gheco come un pan con miel, feliz.

### Micro-misión S03-N03-P2 · Las regiones, una vez

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco
carta: Set | [...new Set(lista)]
recompensa: xp 10, oro 10
```

#### Escena
Sila quiere un cartelito por cajón, y hay un cajón por región. Nima escribe los carteles… y le salen siete: tres del Valle.

#### Gheco sugiere
Sacá las regiones sin repetir con un `Set`, y mostrá cuántas son y cuáles.

#### Desafío
`4 regiones: Valle, Forjas, Puerto, Talleres`.

#### Código inicial
```javascript
const FICHAS = [
  { heroe: 'Mia', region: 'Valle' },
  { heroe: 'Kira', region: 'Forjas' },
  { heroe: 'Nilo', region: 'Puerto' },
  { heroe: 'Nima', region: 'Valle' },
  { heroe: 'Tesela', region: 'Talleres' },
  { heroe: 'Iara', region: 'Puerto' },
  { heroe: 'Sila', region: 'Valle' },
];

const regiones = FICHAS.map((f) => f.region);
console.log(`${regiones.length} regiones: ${regiones.join(', ')}`);
```

#### Salida esperada
```
4 regiones: Valle, Forjas, Puerto, Talleres
```

#### Solución
```javascript
const FICHAS = [
  { heroe: 'Mia', region: 'Valle' },
  { heroe: 'Kira', region: 'Forjas' },
  { heroe: 'Nilo', region: 'Puerto' },
  { heroe: 'Nima', region: 'Valle' },
  { heroe: 'Tesela', region: 'Talleres' },
  { heroe: 'Iara', region: 'Puerto' },
  { heroe: 'Sila', region: 'Valle' },
];

const regiones = [...new Set(FICHAS.map((f) => f.region))];
console.log(`${regiones.length} regiones: ${regiones.join(', ')}`);
```

#### Al superarla
Cuatro carteles, uno por cajón. Gheco tira los tres repetidos a la basura.

#### Imagen
- Cuatro cartelitos de madera colgados de cuatro cajones (con dibujos de una serpiente, un yunque, un ancla y un vitral).
- Gheco tira cartelitos repetidos a un canasto.

### Micro-misión S03-N03-P3 · Cada cual en su cajón

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco
carta: Agrupar | grupos[f.region] ??= [] · grupos[f.region].push(f.heroe)
recompensa: xp 10, oro 10
```

#### Escena
Ahora sí: hay que meter cada ficha en su cajón. Un cajón por región, con los nombres adentro.

#### Gheco sugiere
Armá un objeto con una lista de nombres por región (creala con `??=` la primera vez) y mostrá cada cajón: `Valle → Mia, Nima, Sila`.

#### Desafío
Los cuatro cajones.

#### Código inicial
```javascript
const FICHAS = [
  { heroe: 'Mia', region: 'Valle' },
  { heroe: 'Kira', region: 'Forjas' },
  { heroe: 'Nilo', region: 'Puerto' },
  { heroe: 'Nima', region: 'Valle' },
  { heroe: 'Tesela', region: 'Talleres' },
  { heroe: 'Iara', region: 'Puerto' },
  { heroe: 'Sila', region: 'Valle' },
];

const grupos = {};
for (const f of FICHAS) {
  grupos[f.region] = [f.heroe];
}
for (const [region, nombres] of Object.entries(grupos)) console.log(`${region} → ${nombres.join(', ')}`);
```

#### Salida esperada
```
Valle → Mia, Nima, Sila
Forjas → Kira
Puerto → Nilo, Iara
Talleres → Tesela
```

#### Solución
```javascript
const FICHAS = [
  { heroe: 'Mia', region: 'Valle' },
  { heroe: 'Kira', region: 'Forjas' },
  { heroe: 'Nilo', region: 'Puerto' },
  { heroe: 'Nima', region: 'Valle' },
  { heroe: 'Tesela', region: 'Talleres' },
  { heroe: 'Iara', region: 'Puerto' },
  { heroe: 'Sila', region: 'Valle' },
];

const grupos = {};
for (const f of FICHAS) {
  grupos[f.region] ??= [];
  grupos[f.region].push(f.heroe);
}
for (const [region, nombres] of Object.entries(grupos)) console.log(`${region} → ${nombres.join(', ')}`);
```

#### Al superarla
Cada ficha en su cajón. Con el código de antes, en cada cajón quedaba solo la **última**: las otras se pisaban.

#### Imagen
- Cuatro cajones de archivo abiertos, cada uno con su montoncito de fichas, ordenados.
- Nima cierra el último cajón con la cadera.

### Micro-misión S03-N03-P4 · El promedio de cada región

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Lumina
carta: Promedio | suma / cantidad · promedio.toFixed(1)
recompensa: xp 15, monedas 5
```

#### Escena
{mentor} se posa en el mostrador y mira los cajones. —¿Y cuál región tiene los héroes más avanzados? —Nima no sabe: un cajón tiene más fichas, pero eso no dice nada del nivel.

#### Gheco sugiere
Para cada región juntá la **suma** de niveles y la **cantidad**. Después mostrá el promedio con un decimal (`toFixed(1)`): `Valle: 5.3`.

#### Desafío
Los promedios de las tres regiones.

#### Código inicial
```javascript
const FICHAS = [
  { heroe: 'Mia', region: 'Valle', nivel: 5 },
  { heroe: 'Kira', region: 'Forjas', nivel: 6 },
  { heroe: 'Nilo', region: 'Puerto', nivel: 4 },
  { heroe: 'Nima', region: 'Valle', nivel: 4 },
  { heroe: 'Tizón', region: 'Forjas', nivel: 2 },
  { heroe: 'Iara', region: 'Puerto', nivel: 3 },
  { heroe: 'Sila', region: 'Valle', nivel: 7 },
];

const datos = {};
for (const f of FICHAS) {
  datos[f.region] ??= { suma: 0, cantidad: 0 };

}
for (const [region, d] of Object.entries(datos)) console.log(`${region}: ${d.suma}`);
```

#### Salida esperada
```
Valle: 5.3
Forjas: 4.0
Puerto: 3.5
```

#### Solución
```javascript
const FICHAS = [
  { heroe: 'Mia', region: 'Valle', nivel: 5 },
  { heroe: 'Kira', region: 'Forjas', nivel: 6 },
  { heroe: 'Nilo', region: 'Puerto', nivel: 4 },
  { heroe: 'Nima', region: 'Valle', nivel: 4 },
  { heroe: 'Tizón', region: 'Forjas', nivel: 2 },
  { heroe: 'Iara', region: 'Puerto', nivel: 3 },
  { heroe: 'Sila', region: 'Valle', nivel: 7 },
];

const datos = {};
for (const f of FICHAS) {
  datos[f.region] ??= { suma: 0, cantidad: 0 };
  datos[f.region].suma += f.nivel;
  datos[f.region].cantidad++;
}
for (const [region, d] of Object.entries(datos)) console.log(`${region}: ${(d.suma / d.cantidad).toFixed(1)}`);
```

#### Al superarla
*Valle: 5.3 · Forjas: 4.0 · Puerto: 3.5.* {mentor} asiente. —El Valle tiene buenos maestros. Ofidia sabe esperar, como yo.

#### Imagen
- Tres cajones con una balanza de bronce encima de cada uno, inclinadas distinto.
- Lumina, la luciérnaga gigante con alas de vidrio, posada en el mostrador con su farolito.

### Micro-misión S03-N03-P5 · El cartel del Archivo

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco
carta: Ordenar entradas | Object.entries(cuenta).sort(([, a], [, b]) => b - a)
recompensa: xp 15, monedas 5
```

#### Escena
Para la puerta del Archivo, Sila quiere un cartel con las regiones de **la que más fichas tiene a la que menos**, y si empatan, por nombre.

#### Gheco sugiere
Contá por región, pasalo a pares con `Object.entries`, ordená por cantidad (de mayor a menor) y, si empatan, por nombre. Mostrá `Valle ··· 3`.

#### Desafío
El cartel ordenado.

#### Código inicial
```javascript
const FICHAS = [
  { heroe: 'Kira', region: 'Forjas' },
  { heroe: 'Nilo', region: 'Puerto' },
  { heroe: 'Mia', region: 'Valle' },
  { heroe: 'Tesela', region: 'Talleres' },
  { heroe: 'Nima', region: 'Valle' },
  { heroe: 'Tizón', region: 'Forjas' },
  { heroe: 'Iara', region: 'Puerto' },
  { heroe: 'Sila', region: 'Valle' },
];

const cuenta = FICHAS.reduce((c, f) => {
  c[f.region] = (c[f.region] ?? 0) + 1;
  return c;
}, {});
for (const [region, cantidad] of Object.entries(cuenta)) console.log(`${region} ··· ${cantidad}`);
```

#### Salida esperada
```
Valle ··· 3
Forjas ··· 2
Puerto ··· 2
Talleres ··· 1
```

#### Solución
```javascript
const FICHAS = [
  { heroe: 'Kira', region: 'Forjas' },
  { heroe: 'Nilo', region: 'Puerto' },
  { heroe: 'Mia', region: 'Valle' },
  { heroe: 'Tesela', region: 'Talleres' },
  { heroe: 'Nima', region: 'Valle' },
  { heroe: 'Tizón', region: 'Forjas' },
  { heroe: 'Iara', region: 'Puerto' },
  { heroe: 'Sila', region: 'Valle' },
];

const cuenta = FICHAS.reduce((c, f) => {
  c[f.region] = (c[f.region] ?? 0) + 1;
  return c;
}, {});
const cartel = Object.entries(cuenta).sort(([ra, a], [rb, b]) => b - a || ra.localeCompare(rb, 'es'));
for (const [region, cantidad] of cartel) console.log(`${region} ··· ${cantidad}`);
```

#### Al superarla
*Valle ··· 3, Forjas ··· 2, Puerto ··· 2, Talleres ··· 1.* Nima lo copia con su mejor letra para mandárselo a Sila.

#### Imagen
- Un cartel de madera pintado a mano con cuatro renglones y puntitos, colgado de un clavo.
- Nima lo pinta con un pincel finito, concentrada.

## S03-N04 · Jefe: el Ratón de la Niebla

```meta
tipo: jefe
padre: S03-N03
precio: 10
criatura: dragon
insignia: Archivista de la Feria
insignia_descripcion: Ordenaste el Archivo de Sila: buscaste, ordenaste, contaste y limpiaste las fichas que desordenó la niebla.
temas: arch.json, err.validacion
usa: col.listas, col.mapas, col.conjuntos, alg.ordenamiento
```

### Crónica

Cuando Nima ya cree que terminó, del fondo del paquete sale un **ratón** gris, mojado y con los bigotes llenos de gotitas. Vino escondido desde el Valle, comiéndose las esquinas de las fichas. Tiene los ojos blancos como la niebla.

—Es el **Ratón de la Niebla** —dice Gheco—. Donde pasa, las fichas quedan **rotas**: nombres con espacios de más, niveles escritos como texto, regiones que faltan, fichas repetidas. —El ratón se sienta sobre la última pila y espera, como si supiera que nadie puede arreglar lo que rompió.

### Objetivos

- Limpiar datos: sacar espacios con `trim`, convertir con `Number` y poner valores por defecto.
- Sacar los repetidos por `id` con un `Map`.
- Separar los datos que sirven de los que no, con el motivo.
- Armar un informe en una tabla con `padEnd` y `padStart`, y en JSON con `JSON.stringify(datos, null, 2)`.

### Antes de empezar

- Todo el Archivo (S03-N01 a N03).

### Explicación

#### Los datos sucios
Los datos de verdad casi nunca llegan limpios:
```javascript
{ id: 4, heroe: '  Nima ', region: '', nivel: '4' }
```
Limpiar es **una función** que recibe una ficha sucia y devuelve una limpia:
```javascript
const limpiar = (f) => ({
  id: f.id,
  heroe: f.heroe.trim(),
  region: f.region?.trim() || 'Sin región',
  nivel: Number(f.nivel),
});
```
`||` (y no `??`) porque una región vacía `''` también tiene que pasar a `'Sin región'`.

#### Repetidos por `id`
Un `Map` guarda una ficha por clave. Si la clave se repite, pisa la anterior:
```javascript
const unicas = [...new Map(fichas.map((f) => [f.id, f])).values()];
```

#### ¿Sirve o no sirve?
```javascript
const motivo = (f) => (Number.isNaN(f.nivel) ? 'nivel ilegible' : f.heroe === '' ? 'sin nombre' : '');
```

#### Una tabla en la consola
```javascript
console.log('Sila'.padEnd(10, '.') + '7'.padStart(3));   // 'Sila......  7'
```

#### JSON para mandar
```javascript
JSON.stringify({ total: 3, fichas: [] }, null, 2);
```
El `2` es la sangría: el JSON sale en varios renglones, fácil de leer.

### Código de ejemplo

```javascript
const sucia = { id: 4, heroe: '  Nima ', region: '', nivel: '4' };
const limpia = {
  id: sucia.id,
  heroe: sucia.heroe.trim(),
  region: sucia.region?.trim() || 'Sin región',
  nivel: Number(sucia.nivel),
};
console.log(limpia);
console.log(Number('cuatro'), Number.isNaN(Number('cuatro')));
console.log('Sila'.padEnd(10, '.') + '7'.padStart(3));
console.log(JSON.stringify({ total: 1, fichas: [limpia.heroe] }, null, 2));
```

### Salida esperada

```
{ id: 4, heroe: 'Nima', region: 'Sin región', nivel: 4 }
NaN true
Sila......  7
{
  "total": 1,
  "fichas": [
    "Nima"
  ]
}
```

### ¿Para qué sirve?

Todo sistema que recibe datos de afuera (un formulario, un archivo Excel, otra API) tiene que limpiarlos antes de usarlos: espacios, números como texto, campos vacíos, filas repetidas. Es la mitad del trabajo con datos de verdad.

### Errores habituales

**Goblin: comparar `NaN` con `===`.** `NaN === NaN` es `false`. Se pregunta con `Number.isNaN`.

**Ogro: `??` donde iba `||`.** `'' ?? 'Sin región'` da `''`: el `??` solo reemplaza `null` y `undefined`.

**Ogro: sacar repetidos por nombre.** Dos héroes distintos pueden llamarse igual; lo que no se repite es el `id`.

### Micro-misión S03-N04-P1 · Las fichas mojadas

```meta
lugar: El puesto de tiro, con el Ratón de la Niebla
personajes: Nima, Gheco, el Ratón de la Niebla
carta: Limpiar | heroe.trim() · region?.trim() || 'Sin región' · Number(nivel)
recompensa: xp 10, oro 10
```

#### Escena
El Ratón mordió las primeras fichas: los nombres quedaron con espacios, las regiones vacías y los niveles escritos como texto.

#### Gheco sugiere
Escribí `limpiar(ficha)` y mostrá cada ficha limpia como `Nima | Sin región | 4 (number)`.

#### Desafío
Las tres fichas, limpias.

#### Código inicial
```javascript
const SUCIAS = [
  { id: 4, heroe: '  Nima ', region: '', nivel: '4' },
  { id: 2, heroe: 'Kira', region: ' Forjas', nivel: 6 },
  { id: 3, heroe: 'Nilo  ', nivel: '4' },
];

function limpiar(f) {
  return f;
}

for (const f of SUCIAS.map(limpiar)) {
  console.log(`${f.heroe} | ${f.region} | ${f.nivel} (${typeof f.nivel})`);
}
```

#### Salida esperada
```
Nima | Sin región | 4 (number)
Kira | Forjas | 6 (number)
Nilo | Sin región | 4 (number)
```

#### Solución
```javascript
const SUCIAS = [
  { id: 4, heroe: '  Nima ', region: '', nivel: '4' },
  { id: 2, heroe: 'Kira', region: ' Forjas', nivel: 6 },
  { id: 3, heroe: 'Nilo  ', nivel: '4' },
];

function limpiar(f) {
  return {
    id: f.id,
    heroe: f.heroe.trim(),
    region: f.region?.trim() || 'Sin región',
    nivel: Number(f.nivel),
  };
}

for (const f of SUCIAS.map(limpiar)) {
  console.log(`${f.heroe} | ${f.region} | ${f.nivel} (${typeof f.nivel})`);
}
```

#### Al superarla
Las tres fichas se secan, prolijas. El Ratón se sacude el agua de los bigotes, sorprendido.

#### Imagen
- Un ratón gris mojado, con bigotes llenos de gotitas y ojos blancos como niebla, sentado sobre una pila de fichas (dibujo tierno, no da miedo).
- Las fichas de arriba se secan con un brillo amarillo.

### Micro-misión S03-N04-P2 · Las repetidas

```meta
lugar: El puesto de tiro, con el Ratón de la Niebla
personajes: Nima, Gheco, el Ratón de la Niebla
carta: Map por id | [...new Map(fichas.map((f) => [f.id, f])).values()]
recompensa: xp 10, oro 10
```

#### Escena
El Ratón tiene otro truco: copia las fichas. La de Kira aparece tres veces, la de Mia dos.

#### Gheco sugiere
Sacá las repetidas por `id` con un `Map` (queda la **última** de cada `id`). Mostrá cuántas había, cuántas quedan y los nombres.

#### Desafío
`De 7 quedan 4: Mia, Kira, Nilo, Sila`.

#### Código inicial
```javascript
const FICHAS = [
  { id: 1, heroe: 'Mia' },
  { id: 2, heroe: 'Kira' },
  { id: 2, heroe: 'Kira' },
  { id: 3, heroe: 'Nilo' },
  { id: 1, heroe: 'Mia' },
  { id: 9, heroe: 'Sila' },
  { id: 2, heroe: 'Kira' },
];

const unicas = FICHAS;
console.log(`De ${FICHAS.length} quedan ${unicas.length}: ${unicas.map((f) => f.heroe).join(', ')}`);
```

#### Salida esperada
```
De 7 quedan 4: Mia, Kira, Nilo, Sila
```

#### Solución
```javascript
const FICHAS = [
  { id: 1, heroe: 'Mia' },
  { id: 2, heroe: 'Kira' },
  { id: 2, heroe: 'Kira' },
  { id: 3, heroe: 'Nilo' },
  { id: 1, heroe: 'Mia' },
  { id: 9, heroe: 'Sila' },
  { id: 2, heroe: 'Kira' },
];

const unicas = [...new Map(FICHAS.map((f) => [f.id, f])).values()];
console.log(`De ${FICHAS.length} quedan ${unicas.length}: ${unicas.map((f) => f.heroe).join(', ')}`);
```

#### Al superarla
Las copias se deshacen como niebla. El Ratón se rasca la oreja, cada vez más chiquito.

#### Imagen
- Fichas de papel repetidas que se deshacen en hilitos de niebla; quedan cuatro, firmes.
- El ratón gris se rasca la oreja, un poco más chico que antes.

### Micro-misión S03-N04-P3 · Las que no se pueden leer

```meta
lugar: El puesto de tiro, con el Ratón de la Niebla
personajes: Nima, Gheco, el Ratón de la Niebla
carta: Validar | Number.isNaN(f.nivel) ? 'nivel ilegible' : f.heroe === '' ? 'sin nombre' : ''
recompensa: xp 10, oro 10
```

#### Escena
Algunas fichas quedaron tan mojadas que no se leen: una dice nivel *«cua…»*, otra no tiene nombre. Sila prefiere saber cuáles son, antes que inventarles los datos.

#### Gheco sugiere
Escribí `motivo(ficha)`, que devuelve por qué una ficha no sirve (o `''` si sirve). Separá las que sirven de las que no y mostrá las dos listas, las que no con su motivo: `#12 (nivel ilegible)`.

#### Desafío
Dos renglones: `Sirven: …` y `No sirven: …`.

#### Código inicial
```javascript
const FICHAS = [
  { id: 1, heroe: 'Mia', nivel: 5 },
  { id: 12, heroe: 'Kira', nivel: Number('cua') },
  { id: 3, heroe: 'Nilo', nivel: 4 },
  { id: 14, heroe: '', nivel: 2 },
  { id: 9, heroe: 'Sila', nivel: 7 },
];

function motivo(f) {
  if (f.nivel === NaN) return 'nivel ilegible';
  return '';
}

const sirven = FICHAS.filter((f) => motivo(f) === '');
const noSirven = FICHAS.filter((f) => motivo(f) !== '');
console.log(`Sirven: ${sirven.map((f) => f.heroe).join(', ')}`);
console.log(`No sirven: ${noSirven.map((f) => `#${f.id} (${motivo(f)})`).join(', ')}`);
```

#### Salida esperada
```
Sirven: Mia, Nilo, Sila
No sirven: #12 (nivel ilegible), #14 (sin nombre)
```

#### Solución
```javascript
const FICHAS = [
  { id: 1, heroe: 'Mia', nivel: 5 },
  { id: 12, heroe: 'Kira', nivel: Number('cua') },
  { id: 3, heroe: 'Nilo', nivel: 4 },
  { id: 14, heroe: '', nivel: 2 },
  { id: 9, heroe: 'Sila', nivel: 7 },
];

function motivo(f) {
  if (Number.isNaN(f.nivel)) return 'nivel ilegible';
  if (f.heroe === '') return 'sin nombre';
  return '';
}

const sirven = FICHAS.filter((f) => motivo(f) === '');
const noSirven = FICHAS.filter((f) => motivo(f) !== '');
console.log(`Sirven: ${sirven.map((f) => f.heroe).join(', ')}`);
console.log(`No sirven: ${noSirven.map((f) => `#${f.id} (${motivo(f)})`).join(', ')}`);
```

#### Al superarla
Las fichas que no se pueden leer quedan aparte, con su motivo, para que Sila las rehaga. Ninguna se inventó. El Ratón ya es del tamaño de una nuez.

#### Imagen
- Dos montones de fichas: uno prolijo y otro chiquito, con etiquetas rojas atadas con hilo.
- El ratón, ahora del tamaño de una nuez, mira desde arriba de una ficha.

### Micro-misión S03-N04-P4 · La tabla para la puerta

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Don Tano
carta: Tabla | heroe.padEnd(10, '.') + String(nivel).padStart(3)
recompensa: xp 15, monedas 5
```

#### Escena
Don Tano, el del organito, se acerca a mirar. —En mis tiempos, las listas se escribían con puntitos, para que el ojo no se pierda. Así. —Y dibuja en el aire una fila de puntos.

#### Gheco sugiere
Mostrá una tabla: un título `HÉROE       NIVEL`, una línea de 15 guiones (`'-'.repeat(15)`) y una fila por ficha con el nombre completado con puntos hasta 10 letras y el nivel alineado a la derecha en 5.

#### Desafío
La tabla, ordenada por nivel de mayor a menor.

#### Código inicial
```javascript
const FICHAS = [
  { heroe: 'Mia', nivel: 5 },
  { heroe: 'Tesela', nivel: 9 },
  { heroe: 'Nilo', nivel: 4 },
  { heroe: 'Sila', nivel: 7 },
];

console.log('HÉROE       NIVEL');
for (const f of FICHAS) console.log(f.heroe + ' ' + f.nivel);
```

#### Salida esperada
```
HÉROE       NIVEL
---------------
Tesela....    9
Sila......    7
Mia.......    5
Nilo......    4
```

#### Solución
```javascript
const FICHAS = [
  { heroe: 'Mia', nivel: 5 },
  { heroe: 'Tesela', nivel: 9 },
  { heroe: 'Nilo', nivel: 4 },
  { heroe: 'Sila', nivel: 7 },
];

console.log('HÉROE       NIVEL');
console.log('-'.repeat(15));
for (const f of FICHAS.toSorted((a, b) => b.nivel - a.nivel)) {
  console.log(f.heroe.padEnd(10, '.') + String(f.nivel).padStart(5));
}
```

#### Al superarla
Una tabla prolija, con sus puntitos. Don Tano la mira y da vuelta la manija del organito, contento: suena un vals.

#### Imagen
- Don Tano (abuelo de sombrero de copa gastado, bigote blanco grande, saco largo abotonado) con su organito, mirando un papel con una tabla de puntitos.
- Nima sostiene el papel; notas musicales de luz salen del organito.

### Micro-misión S03-N04-P5 · Jefe: el informe para Sila

```meta
lugar: El puesto de tiro, de madrugada
personajes: Nima, Gheco, el Ratón de la Niebla, Lumina
carta: El Archivo completo | limpiar → sin repetidos → separar → ordenar → contar → JSON.stringify(informe, null, 2)
recompensa: xp 50, oro 50, monedas 1
```

#### Escena
Queda la última pila, la más mojada, y el Ratón está sentado encima. —Todo junto —dice {mentor}—. Lo que aprendiste en este paquete, de una vez.

#### Gheco sugiere
Armá el `informe` para Sila con las fichas sucias:
1. limpiá cada ficha (`trim`, `Number`, `'Sin región'`);
2. sacá las repetidas por `id`;
3. separá las que no sirven (nivel ilegible o sin nombre);
4. de las que sirven, ordená por nivel (de mayor a menor) y por nombre;
5. contá cuántas hay por región.

Mostralo con `JSON.stringify(informe, null, 2)`, con estas claves: `total`, `porRegion`, `fichas` (los nombres en orden) y `paraRehacer` (los `id` que no sirven).

#### Desafío
El informe completo.

#### Código inicial
```javascript
const SUCIAS = [
  { id: 4, heroe: '  Nima ', region: 'Valle', nivel: '4' },
  { id: 2, heroe: 'Kira', region: ' Forjas', nivel: 6 },
  { id: 9, heroe: 'Sila', region: 'Valle', nivel: '7' },
  { id: 2, heroe: 'Kira', region: 'Forjas', nivel: 6 },
  { id: 12, heroe: 'Tizón', region: 'Forjas', nivel: 'cua…' },
  { id: 3, heroe: 'Nilo', region: '', nivel: 4 },
  { id: 1, heroe: 'Mia ', region: 'Valle', nivel: 5 },
  { id: 15, heroe: 'El Vidriero', region: 'Mirador de las Constelaciones', nivel: '9' },
  { id: 14, heroe: '   ', region: 'Talleres', nivel: 2 },
];

const informe = {
  total: SUCIAS.length,
  porRegion: {},
  fichas: SUCIAS.map((f) => f.heroe),
  paraRehacer: [],
};

console.log(JSON.stringify(informe, null, 2));
```

#### Salida esperada
```
{
  "total": 6,
  "porRegion": {
    "Mirador de las Constelaciones": 1,
    "Valle": 3,
    "Forjas": 1,
    "Sin región": 1
  },
  "fichas": [
    "El Vidriero",
    "Sila",
    "Kira",
    "Mia",
    "Nilo",
    "Nima"
  ],
  "paraRehacer": [
    12,
    14
  ]
}
```

#### Solución
```javascript
const SUCIAS = [
  { id: 4, heroe: '  Nima ', region: 'Valle', nivel: '4' },
  { id: 2, heroe: 'Kira', region: ' Forjas', nivel: 6 },
  { id: 9, heroe: 'Sila', region: 'Valle', nivel: '7' },
  { id: 2, heroe: 'Kira', region: 'Forjas', nivel: 6 },
  { id: 12, heroe: 'Tizón', region: 'Forjas', nivel: 'cua…' },
  { id: 3, heroe: 'Nilo', region: '', nivel: 4 },
  { id: 1, heroe: 'Mia ', region: 'Valle', nivel: 5 },
  { id: 15, heroe: 'El Vidriero', region: 'Mirador de las Constelaciones', nivel: '9' },
  { id: 14, heroe: '   ', region: 'Talleres', nivel: 2 },
];

const limpiar = (f) => ({
  id: f.id,
  heroe: f.heroe.trim(),
  region: f.region?.trim() || 'Sin región',
  nivel: Number(f.nivel),
});
const motivo = (f) => (Number.isNaN(f.nivel) ? 'nivel ilegible' : f.heroe === '' ? 'sin nombre' : '');

const limpias = SUCIAS.map(limpiar);
const unicas = [...new Map(limpias.map((f) => [f.id, f])).values()];
const sirven = unicas
  .filter((f) => motivo(f) === '')
  .sort((a, b) => b.nivel - a.nivel || a.heroe.localeCompare(b.heroe, 'es'));

const informe = {
  total: sirven.length,
  porRegion: sirven.reduce((c, f) => {
    c[f.region] = (c[f.region] ?? 0) + 1;
    return c;
  }, {}),
  fichas: sirven.map((f) => f.heroe),
  paraRehacer: unicas.filter((f) => motivo(f) !== '').map((f) => f.id),
};

console.log(JSON.stringify(informe, null, 2));
```

#### Al superarla
El informe sale limpio, ordenado y contado. El Ratón de la Niebla se queda sin nada que romper: se sacude la última gota, los ojos se le ponen negros como los de cualquier ratón, y se mete en el bolsillo de Nima, calentito.

Pero hay una ficha que Nima no entiende: la 15. *El Vidriero, nivel 9, región: Mirador de las Constelaciones.* No es ninguna región que ella conozca. {mentor} la mira mucho rato y no dice nada; solo baja la luz del farolito.

Nima ata el informe a la pata de la paloma y escribe al pie: *«Sila: el Archivo está en orden. ¿Quién es el Vidriero? ¿Y dónde queda el Mirador?»*

#### Imagen
- Un ratoncito gris de ojos negros, ya seco y tranquilo, asomando del bolsillo de la chaqueta de Nima.
- Una ficha de papel brillante con una constelación dibujada en el borde, en la mano de Nima; la paloma blanca espera con el informe atado a la pata, y Lumina mira la ficha con la luz bajita.
