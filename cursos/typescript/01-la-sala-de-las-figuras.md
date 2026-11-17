# RAMA R01 · La Sala de las Figuras: los tipos

```meta
tipo: tronco
posicion: 1
```

## R01-N01 · Tipos básicos y arreglos

```meta
tipo: tema
padre: R00-N01
precio: 10
criatura: goblin
temas: cal.tipos, prog.variables, col.listas
```

### Crónica

La **Sala de las Figuras** es el taller de Astrea: estantes de madera llenos de piezas de vidrio, lentes, bielas y engranajes, cada uno en su cajón. Cada cajón tiene grabado qué acepta: *solo números*, *solo textos*, *solo encendido o apagado*.

—Una pieza suelta es fácil de medir —dice {mentor}—. Lo difícil es un **estante** lleno. Si el cajón dice *números*, todo lo que entra tiene que ser un número. Uno solo que no lo sea, y el estante entero se traba.

### Objetivos

- Usar los tipos básicos: `string`, `number` y `boolean`.
- Anotar un arreglo: `number[]` o `Array<number>`.
- Ver cómo el compilador revisa cada cosa que entra al arreglo (`push`).
- Leer el error `TS2345`: un argumento de otro tipo.

### Antes de empezar

- La Clase 0: anotar un tipo, la inferencia y leer un error.
- De JavaScript: arreglos, `push`, `length` y `for…of`.

### Explicación

#### Los tres tipos básicos
```typescript
const nombre: string = 'lente';   // textos
const medida: number = 4.5;       // números: enteros y con decimales, todos son number
const encendida: boolean = true;  // true o false
```

#### Arreglos con tipo
Un arreglo lleva el tipo de **lo que guarda**, seguido de `[]`:

```typescript
const medidas: number[] = [12, 4, 7];
const nombres: string[] = ['lente', 'biela'];
```

Hay otra forma de escribir lo mismo, que vas a ver mucho más adelante con los genéricos: `Array<number>`. Las dos son iguales.

Si el arreglo empieza con valores, TypeScript lo **deduce**: `const medidas = [12, 4, 7]` ya es `number[]`.

#### El compilador revisa lo que entra
```typescript
const medidas: number[] = [12, 4, 7];
medidas.push(9);        // ✓
medidas.push('nueve');  // ✗ TS2345
```

`TS2345` quiere decir: *le pasaste a una función (acá, `push`) un valor de otro tipo que el que pide*.

#### Lo que sale también tiene tipo
Como `medidas` es `number[]`, cada elemento es un `number`: `medidas[0] * 2` está bien, y `medidas[0].toUpperCase()` es un error (los números no tienen `toUpperCase`).

### Código de ejemplo

```typescript
const piezas: string[] = ['lente', 'biela', 'engranaje'];
const medidas: number[] = [4, 12, 7];
const encendidas: Array<boolean> = [true, false, true];

piezas.push('resorte');
medidas.push(3);

let total = 0;
for (const m of medidas) total += m;

console.log(`${piezas.length} piezas: ${piezas.join(', ')}`);
console.log(`Medida total: ${total} mm`);
console.log(`Encendidas: ${encendidas.filter((e) => e).length}`);
```

### Salida esperada

```
4 piezas: lente, biela, engranaje, resorte
Medida total: 26 mm
Encendidas: 2
```

### ¿Para qué sirve?

Casi todos los programas trabajan con listas: los productos de un carrito, los jugadores de una partida, las notas de un curso. Con el tipo en el arreglo, el compilador se asegura de que nunca se mezcle un dato de otra clase, y de que lo que sacás de la lista se use bien.

### Errores habituales

**Goblin: un valor de otro tipo en el arreglo (TS2322 o TS2345).**
```
Línea 2: No se puede asignar un argumento de tipo "string" al parámetro de tipo "number". (TS2345)
```
Revisá qué tipo guarda el arreglo y qué le estás metiendo.

**Esqueleto: un método que ese tipo no tiene (TS2339).** `medidas[0].toUpperCase()` da *La propiedad 'toUpperCase' no existe en el tipo 'number'*. Los textos y los números tienen métodos distintos.

**El arreglo vacío.** `const lista = [];` queda con un tipo que no sirve para nada. Anotalo: `const lista: string[] = [];`.

### Micro-misión R01-N01-P1 · El estante de las medidas

```meta
lugar: La Sala de las Figuras
personajes: Rigel, Gheco, Astrea
carta: Arreglo con tipo | const medidas: number[] = [12, 4]; · el tipo de lo que guarda, y [] · también Array<number>
recompensa: xp 10, oro 10
```

#### Escena
El primer estante de la sala tiene grabado *solo medidas*. Rigel tiene que anotarlo en su libreta con la medida correcta.

#### Gheco sugiere
Un arreglo se anota con el tipo de **cada cosa que guarda** y `[]` al final:

```ts
const pesos: number[] = [3, 8];
```

Se lee: «`pesos` es un arreglo de números».

#### Desafío
Completá el tipo del arreglo `medidas`.

#### Pasos
1. Buscá el `___` después de `medidas:`.
2. Cambialo por `number[]` (un arreglo de números).
3. Tocá **Ejecutar**. Tiene que salir `3 piezas en el estante`.

#### Código inicial
```typescript
const medidas: ___ = [12, 4, 7];
console.log(`${medidas.length} piezas en el estante`);
```

#### Salida esperada
```
3 piezas en el estante
```

#### Solución
```typescript
const medidas: number[] = [12, 4, 7];
console.log(`${medidas.length} piezas en el estante`);
```

#### Al superarla
El estante se ilumina desde adentro, un cajón por vez. Astrea asiente sin decir nada.

#### Imagen
- Un taller de observatorio steampunk con estantes de madera llenos de piezas de vidrio, lentes y engranajes de latón, cada una en su cajón con una placa grabada (sin letras).
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón en la frente, camisa azul, chaleco de cuero marrón cerrado) anota en una libreta.
- Astrea (lechuza grande gris azulada con anteojos de latón y chaleco azul) mira desde lo alto del estante; Gheco en el hombro de Rigel.

### Micro-misión R01-N01-P2 · El goblin del cajón

```meta
lugar: La Sala de las Figuras
personajes: Rigel, Gheco
criatura: goblin
carta: TS2345 | un argumento de otro tipo · push solo acepta lo que guarda el arreglo
recompensa: xp 10, oro 10
```

#### Escena
Un **goblin** quiere meter el número 7 en el cajón de los nombres. El cajón se trabó y no deja guardar nada más.

#### Gheco sugiere
`push` agrega al final del arreglo, pero solo acepta el tipo que el arreglo guarda. En un `string[]`, todo lo que entra tiene que ser texto. Si no, el compilador avisa con `TS2345`: el argumento de `push` es de otro tipo.

#### Desafío
Ejecutá, leé el error y guardá la pieza `'biela'` en lugar del 7.

#### Pasos
1. Tocá **Ejecutar** y leé el error: está en la línea 2.
2. Cambiá `nombres.push(7);` por `nombres.push('biela');`.
3. Tocá **Ejecutar**. Tiene que salir `lente, engranaje, biela`.

#### Código inicial
```typescript
const nombres: string[] = ['lente', 'engranaje'];
nombres.push(7);
console.log(nombres.join(', '));
```

#### Salida esperada
```
lente, engranaje, biela
```

#### Solución
```typescript
const nombres: string[] = ['lente', 'engranaje'];
nombres.push('biela');
console.log(nombres.join(', '));
```

#### Al superarla
El cajón se destraba con un *clic*. El goblin se va refunfuñando, con el 7 abajo del brazo.

#### Imagen
- Un cajón de madera de un taller steampunk, abierto, con piezas de vidrio y una biela de latón adentro.
- Un goblin chiquito con un engranaje en la espalda intenta meter un número de latón grande en el cajón.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) lo aparta con el calibre; Gheco señala el cajón.

### Micro-misión R01-N01-P3 · Las lámparas del telescopio

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco
carta: Array<T> | Array<boolean> es lo mismo que boolean[] · filter((e) => e) se queda con los true
recompensa: xp 10, oro 10
```

#### Escena
El telescopio mayor tiene una fila de lámparas: algunas prendidas, otras apagadas. Rigel quiere contar cuántas andan.

#### Gheco sugiere
`Array<boolean>` es otra forma de escribir `boolean[]`: un arreglo de `true` y `false`. Las dos son iguales; la de los `<>` la vas a usar mucho más adelante.

`filter((e) => e)` se queda solo con los elementos que valen `true`.

#### Desafío
Completá el tipo de lo que guarda el arreglo.

#### Pasos
1. Buscá el `___` adentro de `Array<___>`.
2. Cambialo por `boolean`.
3. Tocá **Ejecutar**. Tiene que salir `Lámparas prendidas: 2 de 3`.

#### Código inicial
```typescript
const lamparas: Array<___> = [true, false, true];
const prendidas = lamparas.filter((e) => e).length;
console.log(`Lámparas prendidas: ${prendidas} de ${lamparas.length}`);
```

#### Salida esperada
```
Lámparas prendidas: 2 de 3
```

#### Solución
```typescript
const lamparas: Array<boolean> = [true, false, true];
const prendidas = lamparas.filter((e) => e).length;
console.log(`Lámparas prendidas: ${prendidas} de ${lamparas.length}`);
```

#### Al superarla
Rigel cambia la lámpara apagada por una nueva. Las tres brillan sobre el ocular del telescopio.

#### Imagen
- Un telescopio enorme de latón con una fila de tres lámparas de vidrio en el costado, dos encendidas y una apagada.
- Rigel (chico flaco con pecas, antiparras de latón, camisa azul, guantes sin dedos) cambia la lámpara apagada.
- Gheco sentado sobre el tubo del telescopio.

### Micro-misión R01-N01-P4 · Probar el cajón

```meta
lugar: La Sala de las Figuras
personajes: Rigel, Gheco, Astrea
criatura: goblin
carta: Hacer que falle | micro-misión de tipo Compilador · lo que se compara son los errores · TS2345 en la línea 2
recompensa: xp 15, monedas 5
```

#### Escena
Astrea quiere que Rigel compruebe que el cajón de las vueltas está bien medido: que rechace lo que no es un número.

#### Gheco sugiere
Esta es una micro-misión de tipo **Compilador**, como la de la Clase 0: no se ejecuta; lo que se compara son los errores. Para superarla, el compilador tiene que decir exactamente:

```
TS2345 en la línea 2
```

`'4'` (con comillas) es un texto, y no entra en un `number[]`.

#### Desafío
Hacé que el compilador frene en la línea 2: metele al arreglo el texto `'4'` en lugar del número `4`.

#### Pasos
1. Buscá la línea 2: `vueltas.push(4);`.
2. Poné el 4 entre comillas: `vueltas.push('4');`.
3. Tocá **Ejecutar**. Tiene que salir `TS2345 en la línea 2`.

#### Compilador
sí

#### Código inicial
```typescript
const vueltas: number[] = [1, 2, 3];
vueltas.push(4);
console.log(vueltas);
```

#### Salida esperada
```
TS2345 en la línea 2
```

#### Solución
```typescript
const vueltas: number[] = [1, 2, 3];
vueltas.push('4');
console.log(vueltas);
```

#### Al superarla
El cajón ni se abre. —Bien medido —dice Astrea—. Un cajón que dice que no es tan útil como uno que dice que sí.

#### Imagen
- Primer plano de un cajón de latón con una placa grabada que se niega a abrirse; una pieza de vidrio rebota en el borde.
- La mano de Rigel (guante de cuero sin dedos) con el calibre de latón.
- Astrea (lechuza con anteojos de latón) observa desde atrás.

### Micro-misión R01-N01-P5 · El inventario de Rigel

```meta
lugar: La Sala de las Figuras
personajes: Rigel, Gheco, Astrea
criatura: goblin
carta: Sumar un arreglo | let total: number = 0 · for (const m of medidas) total += m · el total empieza en 0, no en 'recompensa: xp 15, monedas 5
recompensa: xp 15, monedas 5
```

#### Escena
Para pedir piezas nuevas, Rigel suma las medidas de todo lo que hay en el estante. Pero empezó la cuenta con un texto, y el compilador no deja seguir.

#### Gheco sugiere
Para sumar todo un arreglo, se arranca un total en **cero** y se le suma cada elemento con `for…of`:

```ts
let total: number = 0;
for (const m of medidas) total += m;
```

El total tiene que ser `number` y empezar en `0`, no en `'0'` (eso sería un texto).

#### Desafío
Arreglá la línea del total para que el programa sume las medidas.

#### Pasos
1. Tocá **Ejecutar** y leé el error de la línea 2.
2. Cambiá `'0'` por `0`: queda `let total: number = 0;`.
3. Tocá **Ejecutar**. Tiene que salir `Total: 23 mm en 3 piezas`.

#### Código inicial
```typescript
const medidas: number[] = [12, 4, 7];
let total: number = '0';
for (const m of medidas) total += m;
console.log(`Total: ${total} mm en ${medidas.length} piezas`);
```

#### Salida esperada
```
Total: 23 mm en 3 piezas
```

#### Solución
```typescript
const medidas: number[] = [12, 4, 7];
let total: number = 0;
for (const m of medidas) total += m;
console.log(`Total: ${total} mm en ${medidas.length} piezas`);
```

#### Al superarla
Astrea revisa la cuenta con su compás y le da a Rigel una **estrella de latón**. —Ahora sí: 23 milímetros. Ni uno más.

#### Imagen
- Una mesa de trabajo de latón con piezas de vidrio ordenadas por tamaño y una libreta con una suma (sin números legibles).
- Rigel (chico flaco con pecas, pelo castaño revuelto, antiparras de latón, chaleco marrón) mide una pieza con el calibre.
- Astrea (lechuza con anteojos de latón y chaleco azul de cartógrafa) le alcanza una ficha de latón con una estrella; Gheco en la mesa.

## R01-N02 · Tuplas

```meta
tipo: tema
padre: R01-N01
precio: 10
criatura: orc
temas: cal.tipos, col.listas
```

### Crónica

En un cajón aparte, Astrea guarda las **coordenadas** de las estrellas: siempre dos números, primero la distancia y después la altura. Rigel las anotó en una lista común y las mezcló: puso la altura primero, y en una agregó un tercer número.

—Una coordenada no es una lista cualquiera —dice {mentor}—. Tiene **exactamente** dos lugares, y cada lugar significa algo. En el Mirador eso se llama **tupla**.

### Objetivos

- Anotar una tupla: un arreglo de largo fijo con un tipo por posición (`[string, number]`).
- Leer cada posición con `[0]` y `[1]`, y desarmarla con `const [a, b] = …`.
- Reconocer los errores de una tupla: el orden equivocado y la posición que no existe.
- Hacer una lista de tuplas: `[string, number][]`.

### Antes de empezar

- R01-N01: tipos básicos y arreglos.
- De JavaScript: desestructuración de arreglos (`const [a, b] = lista`).

### Explicación

#### Un arreglo de largo fijo
En JavaScript, un arreglo es un arreglo: puede tener cualquier largo y cualquier cosa adentro. En TypeScript, una **tupla** dice cuántos lugares tiene y qué va en cada uno:

```typescript
const punto: [number, number] = [3, 4];
const pieza: [string, number] = ['lente', 4];   // primero el nombre, después la medida
```

#### Lo que revisa el compilador
```typescript
const pieza: [string, number] = [4, 'lente'];   // ✗ TS2322: el orden está al revés
const punto: [number, number] = [3, 4, 5];      // ✗ TS2322: sobra un lugar
console.log(punto[2]);                          // ✗ TS2493: la tupla no tiene la posición 2
```

#### Leer y desarmar
```typescript
const [nombre, medida] = pieza;   // nombre es string, medida es number
console.log(`${nombre} mide ${medida} mm`);
```

#### Una lista de tuplas
```typescript
const estrellas: [string, number][] = [['Rigel', 860], ['Vega', 25]];
for (const [nombre, distancia] of estrellas) console.log(nombre, distancia);
```

### Código de ejemplo

```typescript
const punto: [number, number] = [3, 4];
const pieza: [string, number] = ['lente', 4];

const [x, y] = punto;
console.log(`Punto en (${x}, ${y})`);
console.log(`${pieza[0]} mide ${pieza[1]} mm`);

const estrellas: [string, number][] = [
  ['Rigel', 860],
  ['Vega', 25],
];
for (const [nombre, distancia] of estrellas) {
  console.log(`${nombre}: ${distancia} años luz`);
}
```

### Salida esperada

```
Punto en (3, 4)
lente mide 4 mm
Rigel: 860 años luz
Vega: 25 años luz
```

### ¿Para qué sirve?

Para datos chicos que siempre van juntos y en el mismo orden: una coordenada (x, y), un par clave y valor, un nombre con su puntaje. Con la tupla, el compilador se asegura de que nadie invierta el orden ni se olvide un lugar.

### Errores habituales

**Goblin: el orden al revés (TS2322).** `const pieza: [string, number] = [4, 'lente']` da *El tipo 'number' no se puede asignar al tipo 'string'*. El primer lugar es el texto.

**Orco: una posición que no existe (TS2493).** En `[number, number]`, `punto[2]` da *El tipo de tupla "[number, number]" de longitud "2" no tiene ningún elemento en el índice "2"*.

**El arreglo común no es una tupla.** `const punto = [3, 4]` queda como `number[]` (largo libre). Para una tupla hay que anotarla.

### Micro-misión R01-N02-P1 · La coordenada de Rigel

```meta
lugar: El cajón de las coordenadas
personajes: Rigel, Gheco
carta: Tupla | const punto: [number, number] = [3, 4]; · largo fijo · un tipo por posición
recompensa: xp 10, oro 10
```

#### Escena
Astrea le pide a Rigel que anote la coordenada de su primera estrella: distancia 3, altura 4.

#### Gheco sugiere
Una **tupla** es un arreglo de **largo fijo**, con un tipo para cada lugar. Se anota con los tipos entre corchetes:

```ts
const par: [number, number] = [1, 2];
```

#### Desafío
Completá el tipo de `punto`: dos números.

#### Pasos
1. Buscá el `___` después de `punto:`.
2. Cambialo por `[number, number]`.
3. Tocá **Ejecutar**. Tiene que salir `Estrella en (3, 4)`.

#### Código inicial
```typescript
const punto: ___ = [3, 4];
console.log(`Estrella en (${punto[0]}, ${punto[1]})`);
```

#### Salida esperada
```
Estrella en (3, 4)
```

#### Solución
```typescript
const punto: [number, number] = [3, 4];
console.log(`Estrella en (${punto[0]}, ${punto[1]})`);
```

#### Al superarla
En el mapa de Astrea aparece un puntito de luz, exactamente en el (3, 4).

#### Imagen
- Un mapa de estrellas grabado en un disco de bronce, con una cuadrícula y un punto de luz encendido.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) señala el punto con el calibre.
- Gheco sobre el borde del disco.

### Micro-misión R01-N02-P2 · El orden al revés

```meta
lugar: El cajón de las coordenadas
personajes: Rigel, Gheco
criatura: goblin
carta: El orden importa | [string, number] · primero el texto, después el número · al revés es TS2322
recompensa: xp 10, oro 10
```

#### Escena
Un goblin dio vuelta la etiqueta de una pieza: puso la medida donde va el nombre.

#### Gheco sugiere
En una tupla, **cada lugar tiene su tipo**. En `[string, number]`, el primero es un texto y el segundo un número. Si se invierten, el compilador frena con `TS2322`.

#### Desafío
Arreglá el orden de los valores de `pieza`.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `[4, 'lente']` por `['lente', 4]`.
3. Tocá **Ejecutar**. Tiene que salir `lente mide 4 mm`.

#### Código inicial
```typescript
const pieza: [string, number] = [4, 'lente'];
console.log(`${pieza[0]} mide ${pieza[1]} mm`);
```

#### Salida esperada
```
lente mide 4 mm
```

#### Solución
```typescript
const pieza: [string, number] = ['lente', 4];
console.log(`${pieza[0]} mide ${pieza[1]} mm`);
```

#### Al superarla
La etiqueta queda derecha y el goblin se va a buscar otra cosa para dar vuelta.

#### Imagen
- Una etiqueta de latón colgada de una pieza de vidrio, dada vuelta.
- Un goblin chiquito con un engranaje en la espalda escapa riéndose.
- Rigel (chico flaco con pecas, antiparras de latón) endereza la etiqueta; Gheco lo ayuda.

### Micro-misión R01-N02-P3 · El lugar que sobra

```meta
lugar: El cajón de las coordenadas
personajes: Rigel, Gheco
criatura: orc
carta: Largo fijo | [number, number] tiene dos lugares · uno de más es TS2322 · leer el [2] es TS2493
recompensa: xp 10, oro 10
```

#### Escena
En una coordenada, Rigel anotó tres números. Un **orco** se esconde en el lugar que sobra.

#### Gheco sugiere
Una tupla `[number, number]` tiene **exactamente dos** lugares. Con tres, el compilador frena. Y si se lee `punto[2]`, también: esa posición no existe.

#### Desafío
Sacale el número que sobra al final y dejá de leer la posición 2.

#### Pasos
1. En la primera línea, cambiá `[5, 2, 9]` por `[5, 2]`.
2. En el `console.log`, borrá `, ${punto[2]}` (la tercera posición).
3. Tocá **Ejecutar**. Tiene que salir `Estrella en (5, 2)`.

#### Código inicial
```typescript
const punto: [number, number] = [5, 2, 9];
console.log(`Estrella en (${punto[0]}, ${punto[1]}, ${punto[2]})`);
```

#### Salida esperada
```
Estrella en (5, 2)
```

#### Solución
```typescript
const punto: [number, number] = [5, 2];
console.log(`Estrella en (${punto[0]}, ${punto[1]})`);
```

#### Al superarla
El orco se queda sin lugar donde esconderse y sale corriendo del cajón.

#### Imagen
- Un cajón de latón con dos ranuras ocupadas por cristales y una tercera ranura improvisada de donde asoma un orco chiquito.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) saca el cristal que sobra.
- Gheco señala al orco.

### Micro-misión R01-N02-P4 · Desarmar la pieza

```meta
lugar: La Sala de las Figuras
personajes: Rigel, Gheco
carta: Desarmar una tupla | const [nombre, medida] = pieza; · cada variable toma el tipo de su lugar
recompensa: xp 15, monedas 5
```

#### Escena
Rigel quiere los dos datos de la pieza en dos variables con nombre, para no andar con `[0]` y `[1]`.

#### Gheco sugiere
Una tupla se puede **desarmar** en variables, como cualquier arreglo:

```ts
const [nombre, medida] = pieza;
```

`nombre` queda como `string` y `medida` como `number`, cada una con el tipo de su lugar.

#### Desafío
Desarmá `pieza` en `nombre` y `medida`.

#### Pasos
1. Buscá el `___` en la segunda línea.
2. Cambialo por `[nombre, medida]`.
3. Tocá **Ejecutar**. Tiene que salir `biela: 12 mm, el doble son 24`.

#### Código inicial
```typescript
const pieza: [string, number] = ['biela', 12];
const ___ = pieza;
console.log(`${nombre}: ${medida} mm, el doble son ${medida * 2}`);
```

#### Salida esperada
```
biela: 12 mm, el doble son 24
```

#### Solución
```typescript
const pieza: [string, number] = ['biela', 12];
const [nombre, medida] = pieza;
console.log(`${nombre}: ${medida} mm, el doble son ${medida * 2}`);
```

#### Al superarla
Rigel separa la biela de su etiqueta y la deja en la mesa, lista para montar.

#### Imagen
- Una biela de latón sobre una mesa de trabajo y, al lado, su etiqueta de latón suelta.
- Rigel (chico flaco con pecas, antiparras de latón, guantes sin dedos) la mira con la lupa de las antiparras bajada.
- Gheco sobre la mesa.

### Micro-misión R01-N02-P5 · El catálogo de estrellas

```meta
lugar: El cajón de las coordenadas
personajes: Rigel, Gheco, Astrea
carta: Lista de tuplas | [string, number][] · for (const [nombre, distancia] of lista) · cada vuelta desarma una tuprecompensa: xp 15, monedas 5
recompensa: xp 15, monedas 5
```

#### Escena
Astrea le confía a Rigel el catálogo de estrellas: un nombre y una distancia cada una. Quiere saber cuál es la más lejana.

#### Gheco sugiere
Una **lista de tuplas** se anota con el tipo de la tupla y `[]` al final:

```ts
const lista: [string, number][] = [['a', 1], ['b', 2]];
```

En el `for…of`, cada vuelta se puede desarmar directamente:

```ts
for (const [nombre, distancia] of lista) { … }
```

#### Desafío
Completá el tipo de `catalogo` y el `for…of` que busca la más lejana.

#### Pasos
1. El primer `___` es el tipo: `[string, number][]`.
2. El segundo `___` desarma cada tupla: `[nombre, distancia]`.
3. Tocá **Ejecutar**. Tiene que salir `La más lejana: Rigel (860 años luz)`.

#### Código inicial
```typescript
const catalogo: ___ = [
  ['Vega', 25],
  ['Rigel', 860],
  ['Sirio', 9],
];

let lejana = '';
let maxima = 0;
for (const ___ of catalogo) {
  if (distancia > maxima) {
    maxima = distancia;
    lejana = nombre;
  }
}
console.log(`La más lejana: ${lejana} (${maxima} años luz)`);
```

#### Salida esperada
```
La más lejana: Rigel (860 años luz)
```

#### Solución
```typescript
const catalogo: [string, number][] = [
  ['Vega', 25],
  ['Rigel', 860],
  ['Sirio', 9],
];

let lejana = '';
let maxima = 0;
for (const [nombre, distancia] of catalogo) {
  if (distancia > maxima) {
    maxima = distancia;
    lejana = nombre;
  }
}
console.log(`La más lejana: ${lejana} (${maxima} años luz)`);
```

#### Al superarla
—Rigel —lee Astrea, y por primera vez se ríe—. Como vos. La más lejana y la más brillante del cielo de invierno. —Le da una **estrella de latón**.

#### Imagen
- Un catálogo de estrellas abierto: un libro grande con mapas de constelaciones y una estrella marcada con luz.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) lo lee sorprendido.
- Astrea (lechuza con anteojos de latón) sonríe a su lado; Gheco sobre el libro.

## R01-N03 · any, unknown, void y never

```meta
tipo: tema
padre: R01-N02
precio: 10
criatura: goblin
temas: cal.tipos, err.validacion
```

### Crónica

En la Sala hay un estante tapado con una lona. Rigel la levanta: adentro, piezas sin ninguna medida grabada. Una de ellas se mueve sola, cambia de color y se le escapa de la mano.

—No las toques así —dice {mentor}—. Esas son las piezas del **Camaleón**. No tienen medida, y por eso entran en cualquier ranura… y rompen lo que tocan. Hay cuatro medidas especiales que tenés que conocer, y una de ellas es la del Camaleón: `any`.

### Objetivos

- Entender `any`: apaga la revisión de tipos (y por eso es peligroso).
- Usar `unknown`: un valor que todavía no sabemos qué es, y que hay que **revisar** antes de usar (con `typeof`).
- Anotar `void`: una función que no devuelve nada.
- Anotar `never`: una función que nunca termina bien (siempre lanza un error).

### Antes de empezar

- R01-N01 y R01-N02.
- De JavaScript: `typeof`, funciones, `throw` y `try`/`catch`.

### Explicación

#### any: la pieza del Camaleón
`any` le dice al compilador «no revises esto». Todo vale:

```typescript
let pieza: any = 'lente';
pieza.toFixed(2);   // compila… y explota al ejecutar: los textos no tienen toFixed
```

Con `any` volvés a tener los problemas de JavaScript. Evitalo.

#### unknown: preguntá antes de usar
`unknown` también acepta cualquier cosa, pero **no deja usarla** hasta revisar qué es:

```typescript
const dato: unknown = 'engranaje';
console.log(dato.length);            // ✗ TS18046: dato es unknown
if (typeof dato === 'string') {
  console.log(dato.length);          // ✓ adentro del if, TypeScript sabe que es string
}
```

Eso de «adentro del `if` ya sabe el tipo» se llama **estrechar** el tipo (*narrowing*). Lo vas a usar todo el tiempo.

#### void: no devuelve nada
```typescript
function anunciar(texto: string): void {
  console.log(`📣 ${texto}`);
}
```

#### never: no termina nunca bien
```typescript
function trabar(motivo: string): never {
  throw new Error(motivo);
}
```

`never` es el tipo de lo que **nunca pasa**. Más adelante lo vas a usar para que el compilador avise si te olvidaste un caso.

#### El error en un catch
En un `catch (e)`, `e` es `unknown`: puede ser cualquier cosa. Para leer su mensaje, se le dice al compilador que es un `Error` con `as`: `(e as Error).message`. (Más adelante vas a ver una forma más segura.)

### Código de ejemplo

```typescript
const lecturas: unknown[] = ['lente', 12, true, 'biela', 30];

let textos = 0;
let suma = 0;
for (const dato of lecturas) {
  if (typeof dato === 'string') textos++;
  if (typeof dato === 'number') suma += dato;
}

function anunciar(texto: string): void {
  console.log(`[Mirador] ${texto}`);
}

function trabar(motivo: string): never {
  throw new Error(motivo);
}

anunciar(`Textos: ${textos} · Suma: ${suma}`);
try {
  trabar('falta una pieza');
} catch (e) {
  anunciar(`Se trabó: ${(e as Error).message}`);
}
```

### Salida esperada

```
[Mirador] Textos: 2 · Suma: 42
[Mirador] Se trabó: falta una pieza
```

### ¿Para qué sirve?

Los datos que vienen de afuera (lo que escribe alguien, una respuesta de un servidor, un archivo) no tienen tipo seguro. Con `unknown` el compilador te obliga a revisarlos antes de usarlos, y así no explota nada. `void` y `never` documentan qué hace una función, para quien la lea y para el compilador.

### Errores habituales

**Goblin: usar un unknown sin revisarlo (TS18046).** *"dato" es de tipo "unknown"*. Preguntá antes con `typeof`.

**El Camaleón: usar any para que «compile».** Compila, pero los errores vuelven a aparecer al ejecutar. Si no sabés el tipo, usá `unknown` y revisalo.

**Esqueleto: el catch sin as.** `e.message` en un `catch (e)` da `TS18046`, porque `e` es `unknown`. Usá `(e as Error).message`.

### Micro-misión R01-N03-P1 · La pieza del Camaleón

```meta
lugar: El estante tapado
personajes: Rigel, Gheco
criatura: goblin
carta: any | apaga la revisión · compila y explota al ejecutar · cambialo por el tipo de verdad
recompensa: xp 10, oro 10
```

#### Escena
Rigel agarra una pieza del estante tapado. El código compila, pero al ejecutar explota. Gheco mira la etiqueta: dice `any`.

#### Gheco sugiere
`any` le dice al compilador «no revises esto». Por eso `pieza.toFixed(2)` compila aunque `pieza` sea un texto, y explota recién al ejecutar (los textos no tienen `toFixed`).

Si le ponés el tipo de verdad, `string`, el compilador te avisa **antes**, y podés usar un método que los textos sí tienen: `toUpperCase()` (pasa a mayúsculas).

#### Desafío
Cambiá `any` por `string` y usá `toUpperCase()` en lugar de `toFixed(2)`.

#### Pasos
1. Tocá **Ejecutar**: explota al ejecutar, con un error de JavaScript.
2. Cambiá `any` por `string`. Ejecutá: ahora el compilador avisa antes (`TS2339`).
3. Cambiá `pieza.toFixed(2)` por `pieza.toUpperCase()`.
4. Tocá **Ejecutar**. Tiene que salir `LENTE`.

#### Código inicial
```typescript
let pieza: any = 'lente';
console.log(pieza.toFixed(2));
```

#### Salida esperada
```
LENTE
```

#### Solución
```typescript
let pieza: string = 'lente';
console.log(pieza.toUpperCase());
```

#### Al superarla
La pieza deja de cambiar de color y se queda quieta en la mano de Rigel, con su medida grabada: *texto*.

#### Imagen
- Un estante cubierto con una lona levantada y, adentro, piezas de vidrio que cambian de color como un camaleón.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sostiene una pieza que se queda quieta.
- Gheco con cara de alivio en su hombro.

### Micro-misión R01-N03-P2 · Preguntá antes de usar

```meta
lugar: El estante tapado
personajes: Rigel, Gheco
carta: unknown | acepta cualquier cosa · no se usa sin preguntar · if (typeof dato === 'string') { … }
recompensa: xp 10, oro 10
```

#### Escena
Llega una pieza en un sobre sin etiqueta: `unknown`. Rigel quiere saber cuánto mide su nombre, pero el compilador no lo deja.

#### Gheco sugiere
Un valor `unknown` no se puede usar hasta **revisar** qué es. Con `typeof` se pregunta:

```ts
if (typeof dato === 'string') {
  // acá adentro, dato es string
}
```

Adentro del `if`, TypeScript ya sabe que es un texto: eso se llama **estrechar** el tipo.

#### Desafío
Completá el `if` para que solo muestre el largo si `dato` es un texto.

#### Pasos
1. Buscá el `___` en el `if`.
2. Cambialo por `typeof dato === 'string'`.
3. Tocá **Ejecutar**. Tiene que salir `engranaje tiene 9 letras`.

#### Código inicial
```typescript
const dato: unknown = 'engranaje';
if (___) {
  console.log(`${dato} tiene ${dato.length} letras`);
}
```

#### Salida esperada
```
engranaje tiene 9 letras
```

#### Solución
```typescript
const dato: unknown = 'engranaje';
if (typeof dato === 'string') {
  console.log(`${dato} tiene ${dato.length} letras`);
}
```

#### Al superarla
Rigel abre el sobre: adentro, un engranaje con su nombre grabado. Ahora sí sabe qué es.

#### Imagen
- Un sobre de papel grueso sin etiqueta, abierto sobre una mesa de latón, con un engranaje adentro.
- Rigel (chico flaco con pecas, antiparras de latón con la lupa bajada) lo examina.
- Gheco asomado al sobre.

### Micro-misión R01-N03-P3 · La lectura del manómetro

```meta
lugar: Las calderas del Mirador
personajes: Rigel, Gheco
carta: Estrechar a number | typeof dato === 'number' · adentro del if se puede hacer cuentas
recompensa: xp 10, oro 10
```

#### Escena
El manómetro de la caldera manda su lectura como `unknown`. Rigel necesita el doble para saber el máximo seguro.

#### Gheco sugiere
Con `typeof lectura === 'number'`, adentro del `if` la lectura ya es un número y se puede multiplicar. Afuera del `if`, no.

#### Desafío
Completá qué tipo se pregunta en el `if`.

#### Pasos
1. Buscá el `___` después de `===`.
2. Cambialo por `'number'` (entre comillas: `typeof` devuelve un texto).
3. Tocá **Ejecutar**. Tiene que salir `Máximo seguro: 84`.

#### Código inicial
```typescript
const lectura: unknown = 42;
if (typeof lectura === ___) {
  console.log(`Máximo seguro: ${lectura * 2}`);
}
```

#### Salida esperada
```
Máximo seguro: 84
```

#### Solución
```typescript
const lectura: unknown = 42;
if (typeof lectura === 'number') {
  console.log(`Máximo seguro: ${lectura * 2}`);
}
```

#### Al superarla
La aguja del manómetro marca 42. Rigel pinta una raya roja en el 84: de ahí no se pasa.

#### Imagen
- Un manómetro grande de latón con una raya roja pintada en el borde (sin números legibles).
- Rigel (chico flaco con pecas, antiparras de latón, guantes sin dedos) pinta la raya con un pincel.
- Gheco sobre un caño de cobre.

### Micro-misión R01-N03-P4 · El anuncio que no devuelve nada

```meta
lugar: La Sala de las Figuras
personajes: Rigel, Gheco
carta: void | function anunciar(texto: string): void · la función hace algo, pero no devuelve nada
recompensa: xp 10, oro 10
```

#### Escena
Rigel arma un altavoz de latón para anunciar las piezas que llegan. El altavoz habla, pero no devuelve nada.

#### Gheco sugiere
En TypeScript, una función puede anotar **qué devuelve**, después de los paréntesis:

```ts
function anunciar(texto: string): void { … }
```

`texto: string` es el tipo del parámetro, y `: void` dice que **no devuelve nada**: solo hace algo (acá, mostrar).

#### Desafío
Completá el tipo de lo que devuelve `anunciar`.

#### Pasos
1. Buscá el `___` después de los paréntesis de `anunciar`.
2. Cambialo por `void`.
3. Tocá **Ejecutar**. Tienen que salir los dos anuncios.

#### Código inicial
```typescript
function anunciar(texto: string): ___ {
  console.log(`[Altavoz] ${texto}`);
}

anunciar('Llegó una lente');
anunciar('Llegó una biela');
```

#### Salida esperada
```
[Altavoz] Llegó una lente
[Altavoz] Llegó una biela
```

#### Solución
```typescript
function anunciar(texto: string): void {
  console.log(`[Altavoz] ${texto}`);
}

anunciar('Llegó una lente');
anunciar('Llegó una biela');
```

#### Al superarla
El altavoz retumba por toda la sala. Astrea se tapa las orejas de plumas: —Un poco más bajo, por favor.

#### Imagen
- Un altavoz de latón con forma de corneta, montado en la pared de un taller steampunk, con ondas de sonido dibujadas en el aire.
- Rigel (chico flaco con pecas, antiparras de latón) habla por un tubo.
- Astrea (lechuza con anteojos de latón) se tapa los penachos con las alas; Gheco se ríe.

### Micro-misión R01-N03-P5 · La palanca de emergencia

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco, Astrea
carta: never | function trabar(motivo: string): never · siempre lanza un error · nunca termina bien
recompensa: xp 15, monedas 5
```

#### Escena
El Planisferio tiene una palanca de emergencia: cuando algo anda mal, lo traba todo y avisa por qué. Nunca vuelve sola a su lugar.

#### Gheco sugiere
`never` es el tipo de una función que **nunca termina bien**: siempre lanza un error (`throw`). Es más fuerte que `void`: `void` termina sin devolver nada, `never` no termina.

En el `catch (e)`, `e` es `unknown`; para leer el mensaje se usa `(e as Error).message`.

#### Desafío
Completá el tipo de lo que devuelve `trabar`.

#### Pasos
1. Buscá el `___` después de los paréntesis de `trabar`.
2. Cambialo por `never`.
3. Tocá **Ejecutar**. Tiene que salir `Se trabó: falta una pieza`.

#### Código inicial
```typescript
function trabar(motivo: string): ___ {
  throw new Error(motivo);
}

try {
  trabar('falta una pieza');
} catch (e) {
  console.log(`Se trabó: ${(e as Error).message}`);
}
```

#### Salida esperada
```
Se trabó: falta una pieza
```

#### Solución
```typescript
function trabar(motivo: string): never {
  throw new Error(motivo);
}

try {
  trabar('falta una pieza');
} catch (e) {
  console.log(`Se trabó: ${(e as Error).message}`);
}
```

#### Al superarla
La palanca baja, el Planisferio se frena en seco y una campanita avisa: *falta una pieza*. —Mejor trabado que roto —dice Astrea.

#### Imagen
- Una palanca de emergencia roja y latón al pie de un planetario mecánico gigante, con una campanita.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) tira de la palanca.
- Astrea (lechuza con anteojos de latón) asiente; Gheco en el hombro de Rigel.

### Micro-misión R01-N03-P6 · El sobre de las lecturas

```meta
lugar: Las calderas del Mirador
personajes: Rigel, Gheco, Astrea
carta: unknown[] | un arreglo de cosas sin revisar · typeof en cada vuelta · contar textos y sumar númerrecompensa: xp 15, monedas 5
recompensa: xp 15, monedas 5
```

#### Escena
Llega un sobre con lecturas mezcladas: nombres de piezas, números de presión, y hasta un `true`. Astrea quiere saber cuántos nombres hay y cuánto suman los números.

#### Gheco sugiere
`unknown[]` es un arreglo donde **cada elemento** es `unknown`. En cada vuelta del `for…of` hay que preguntar qué es antes de usarlo:

```ts
if (typeof dato === 'string') textos++;
if (typeof dato === 'number') suma += dato;
```

#### Desafío
Completá las dos preguntas del `for…of`.

#### Pasos
1. El primer `___`: `typeof dato === 'string'`.
2. El segundo `___`: `typeof dato === 'number'`.
3. Tocá **Ejecutar**. Tiene que salir `Textos: 2 · Suma: 42`.

#### Código inicial
```typescript
const lecturas: unknown[] = ['lente', 12, true, 'biela', 30];

let textos = 0;
let suma = 0;
for (const dato of lecturas) {
  if (___) textos++;
  if (___) suma += dato;
}
console.log(`Textos: ${textos} · Suma: ${suma}`);
```

#### Salida esperada
```
Textos: 2 · Suma: 42
```

#### Solución
```typescript
const lecturas: unknown[] = ['lente', 12, true, 'biela', 30];

let textos = 0;
let suma = 0;
for (const dato of lecturas) {
  if (typeof dato === 'string') textos++;
  if (typeof dato === 'number') suma += dato;
}
console.log(`Textos: ${textos} · Suma: ${suma}`);
```

#### Al superarla
Astrea anota los números en su mapa. —Revisaste cada pieza antes de tocarla. El Camaleón no tiene nada que hacer con vos. —Y le da una **estrella de latón**.

#### Imagen
- Un sobre abierto sobre una mesa de calderas, con papelitos, tuercas y fichas desparramadas.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) los ordena en dos pilas.
- Astrea (lechuza con anteojos de latón) le da una ficha de latón con una estrella; Gheco en la mesa.

## R01-N04 · Funciones tipadas

```meta
tipo: tema
padre: R01-N03
precio: 10
criatura: goblin
temas: prog.funciones, cal.tipos
```

### Crónica

En el fondo de la Sala hay una fila de **máquinas de medir**: una calcula superficies, otra repara piezas, otra suma golpes de martillo. Cada máquina tiene grabado en la tapa qué recibe y qué devuelve: *dos números entran, un número sale*.

—Una función es una máquina —dice {mentor}—. Si le grabás qué recibe y qué devuelve, nadie la va a usar mal. Ni siquiera vos, dentro de un mes.

### Objetivos

- Anotar los parámetros y lo que devuelve una función: `function area(ancho: number, alto: number): number`.
- Leer el error `TS2345` en una llamada.
- Usar parámetros con valor por defecto (`= 10`), opcionales (`?`) y rest (`...golpes: number[]`).
- Anotar una función flecha.

### Antes de empezar

- R01-N03: `void` y `never`.
- De JavaScript: funciones, funciones flecha, parámetros por defecto, rest y `??`.

### Explicación

#### Lo que entra y lo que sale
```typescript
function area(ancho: number, alto: number): number {
  return ancho * alto;
}
```

Cada parámetro lleva su tipo, y después de los paréntesis va el tipo de lo que **devuelve**. Si la función devuelve algo de otro tipo, o la llamás con otra cosa, el compilador avisa:

```typescript
area(3, '4');   // ✗ TS2345: '4' es un texto
```

> Si no anotás lo que devuelve, TypeScript lo deduce. Igual conviene anotarlo: así el error aparece adentro de la función, donde está el problema.

#### Por defecto, opcional y rest
```typescript
function curar(vida: number, cantidad: number = 10): number { … }   // si no la pasan, vale 10
function saludar(nombre: string, titulo?: string): string { … }     // titulo puede faltar
function sumarGolpes(...golpes: number[]): number { … }              // todos los que lleguen
```

Un parámetro opcional (`titulo?: string`) puede valer `undefined`. Antes de usarlo, preguntá o usá `??`: `titulo ?? 'Aprendiz'`.

#### Funciones flecha
```typescript
const doble = (n: number): number => n * 2;
```

Adentro de un `map` o un `filter` no hace falta anotar: TypeScript ya sabe el tipo de cada elemento.

```typescript
const medidas: number[] = [1, 2, 3];
medidas.map((m) => m * 2);   // m ya es number
```

### Código de ejemplo

```typescript
function area(ancho: number, alto: number): number {
  return ancho * alto;
}

function curar(vida: number, cantidad: number = 10): number {
  return Math.min(100, vida + cantidad);
}

function saludar(nombre: string, titulo?: string): string {
  return `${titulo ?? 'Aprendiz'} ${nombre}`;
}

function sumarGolpes(...golpes: number[]): number {
  return golpes.reduce((total, g) => total + g, 0);
}

const doble = (n: number): number => n * 2;

console.log(area(3, 4), curar(80), curar(80, 30));
console.log(saludar('Rigel'), '|', saludar('Astrea', 'Cartógrafa'));
console.log(sumarGolpes(10, 15, 7), [1, 2, 3].map(doble));
```

### Salida esperada

```
12 90 100
Aprendiz Rigel | Cartógrafa Astrea
32 [ 2, 4, 6 ]
```

### ¿Para qué sirve?

Las funciones se usan desde muchos lugares, a veces por otras personas. Con los tipos en la firma, el compilador revisa **cada llamada**: nadie le puede pasar un texto a una función de números, y quien la usa sabe qué le va a devolver sin leer el código de adentro.

### Errores habituales

**Goblin: un argumento de otro tipo (TS2345).** `area(3, '4')` da *No se puede asignar un argumento de tipo "string" al parámetro de tipo "number"*.

**Esqueleto: la cantidad de argumentos (TS2554).** `area(3)` da *Se esperaban 2 argumentos, pero se obtuvieron 1*. Si uno puede faltar, hacelo opcional o dale un valor por defecto.

**Ogro: prometer que devuelve y no devolver (TS2366).** Si la función dice `: number` y hay un camino sin `return`, el compilador avisa.

**Ogro: el parámetro sin tipo (TS7006).** `function doble(n)` da *El parámetro 'n' tiene un tipo 'any' implícitamente*: en modo estricto, todo parámetro lleva su tipo.

### Micro-misión R01-N04-P1 · La máquina de superficies

```meta
lugar: Las máquinas de medir
personajes: Rigel, Gheco
carta: Función tipada | function area(ancho: number, alto: number): number · tipos en los parámetros · : number después de los ( )
recompensa: xp 10, oro 10
```

#### Escena
La primera máquina mide la superficie de una placa de vidrio: recibe el ancho y el alto, y devuelve cuántos centímetros cuadrados tiene. Pero no sabe qué hacer con ellos.

#### Gheco sugiere
En la firma, cada parámetro lleva su tipo, y después de los paréntesis va el tipo de lo que devuelve:

```ts
function area(ancho: number, alto: number): number {
  return ancho * alto;
}
```

`return` es lo que la máquina devuelve.

#### Desafío
Completá el `return` para que devuelva el ancho por el alto.

#### Pasos
1. Buscá el `___` después de `return`.
2. Cambialo por `ancho * alto`.
3. Tocá **Ejecutar**. Tiene que salir `La placa mide 12 cm²`.

#### Código inicial
```typescript
function area(ancho: number, alto: number): number {
  return ___;
}

console.log(`La placa mide ${area(3, 4)} cm²`);
```

#### Salida esperada
```
La placa mide 12 cm²
```

#### Solución
```typescript
function area(ancho: number, alto: number): number {
  return ancho * alto;
}

console.log(`La placa mide ${area(3, 4)} cm²`);
```

#### Al superarla
La máquina zumba, mide la placa y escupe un papelito: *12*. Rigel lo pega en la placa.

#### Imagen
- Una máquina de medir de latón con una tapa grabada y una placa de vidrio cuadrada en su bandeja.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco de cuero marrón cerrado) gira una manivela.
- Gheco sobre la tapa de la máquina.

### Micro-misión R01-N04-P2 · El goblin de la reparadora

```meta
lugar: Las máquinas de medir
personajes: Rigel, Gheco
criatura: goblin
carta: TS2345 en una llamada | el argumento no encaja con el parámetro · '20' es texto, 20 es número
recompensa: xp 10, oro 10
```

#### Escena
Un goblin le metió a la máquina reparadora un papelito con el número 20 escrito. La máquina se trabó.

#### Gheco sugiere
El compilador revisa **cada llamada** contra la firma de la función. `curar` pide un `number`; `'20'` es un texto. Por eso da `TS2345` en la línea de la llamada, no adentro de la función.

#### Desafío
Arreglá la llamada a `curar`.

#### Pasos
1. Tocá **Ejecutar** y leé el error: está en la línea 5.
2. Cambiá `curar('20')` por `curar(20)`.
3. Tocá **Ejecutar**. Tiene que salir `La pieza quedó al 70%`.

#### Código inicial
```typescript
function curar(estado: number): number {
  return Math.min(100, estado + 50);
}

console.log(`La pieza quedó al ${curar('20')}%`);
```

#### Salida esperada
```
La pieza quedó al 70%
```

#### Solución
```typescript
function curar(estado: number): number {
  return Math.min(100, estado + 50);
}

console.log(`La pieza quedó al ${curar(20)}%`);
```

#### Al superarla
La máquina escupe el papelito del goblin y repara la pieza hasta el 70%.

#### Imagen
- Una máquina reparadora de latón con brazos mecánicos y una pieza de vidrio rajada en la bandeja.
- Un goblin chiquito con un engranaje en la espalda se escapa con un papelito.
- Rigel (chico flaco con pecas, antiparras de latón, guantes sin dedos) destraba la máquina; Gheco ayuda.

### Micro-misión R01-N04-P3 · Lo que vale si no lo dicen

```meta
lugar: Las máquinas de medir
personajes: Rigel, Gheco
carta: Valor por defecto | cantidad: number = 10 · si no lo pasan, vale 10 · el tipo y el valor juntos
recompensa: xp 10, oro 10
```

#### Escena
La reparadora casi siempre arregla de a 10 puntos. Rigel quiere que, si no le dicen cuánto, use 10 sola.

#### Gheco sugiere
Un parámetro puede tener un **valor por defecto**, que se usa cuando no lo pasan:

```ts
function curar(estado: number, cantidad: number = 10): number { … }
```

`curar(80)` usa `cantidad = 10`; `curar(80, 30)` usa 30.

#### Desafío
Dale a `cantidad` el valor por defecto `10`.

#### Pasos
1. Buscá `cantidad: number` en la firma.
2. Agregale ` = 10`: queda `cantidad: number = 10`.
3. Tocá **Ejecutar**. Tiene que salir `90 100`.

#### Código inicial
```typescript
function curar(estado: number, cantidad: number): number {
  return Math.min(100, estado + cantidad);
}

console.log(curar(80), curar(80, 30));
```

#### Salida esperada
```
90 100
```

#### Solución
```typescript
function curar(estado: number, cantidad: number = 10): number {
  return Math.min(100, estado + cantidad);
}

console.log(curar(80), curar(80, 30));
```

#### Al superarla
La reparadora aprende su número favorito. Desde ahora, si nadie le dice nada, repara de a 10.

#### Imagen
- La máquina reparadora de latón con un dial que marca un número por defecto (sin números legibles).
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) ajusta el dial con un destornillador chiquito.
- Gheco sobre la máquina.

### Micro-misión R01-N04-P4 · El título que puede faltar

```meta
lugar: La entrada del Mirador
personajes: Rigel, Gheco, Astrea
carta: Parámetro opcional | titulo?: string · puede ser undefined · titulo ?? 'Aprendiz' da un valor si falta
recompensa: xp 10, oro 10
```

#### Escena
La placa de la entrada saluda a cada visitante con su título. Pero no todos tienen uno.

#### Gheco sugiere
Un parámetro con `?` es **opcional**: puede faltar. Si falta, vale `undefined`.

```ts
function saludar(nombre: string, titulo?: string): string { … }
```

Para usar un valor cuando falta, `??`: `titulo ?? 'Aprendiz'` da el título si hay, y `'Aprendiz'` si no.

#### Desafío
Hacé que `titulo` sea opcional.

#### Pasos
1. Buscá `titulo: string` en la firma.
2. Agregale `?` después del nombre: `titulo?: string`.
3. Tocá **Ejecutar**. Tiene que salir `Aprendiz Rigel | Cartógrafa Astrea`.

#### Código inicial
```typescript
function saludar(nombre: string, titulo: string): string {
  return `${titulo ?? 'Aprendiz'} ${nombre}`;
}

console.log(saludar('Rigel'), '|', saludar('Astrea', 'Cartógrafa'));
```

#### Salida esperada
```
Aprendiz Rigel | Cartógrafa Astrea
```

#### Solución
```typescript
function saludar(nombre: string, titulo?: string): string {
  return `${titulo ?? 'Aprendiz'} ${nombre}`;
}

console.log(saludar('Rigel'), '|', saludar('Astrea', 'Cartógrafa'));
```

#### Al superarla
La placa saluda: *Aprendiz Rigel*. Rigel infla el pecho. Astrea, al pasar, recibe su *Cartógrafa Astrea*.

#### Imagen
- La placa de latón iluminada junto a la puerta del observatorio, con dos líneas de luz (sin letras legibles).
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sonríe orgulloso frente a la placa.
- Astrea (lechuza con anteojos de latón y chaleco azul) pasa detrás; Gheco en el hombro de Rigel.

### Micro-misión R01-N04-P5 · Los golpes del martillo

```meta
lugar: Las máquinas de medir
personajes: Rigel, Gheco
carta: Rest tipado | ...golpes: number[] · todos los argumentos que lleguen, en un arreglo · reduce para sumar
recompensa: xp 15, monedas 5
```

#### Escena
El martillo neumático da muchos golpes seguidos, a veces tres, a veces siete. Rigel quiere una máquina que los sume, lleguen los que lleguen.

#### Gheco sugiere
Un parámetro **rest** (`...`) junta todos los argumentos que lleguen en un arreglo. Se anota con el tipo del arreglo:

```ts
function sumarGolpes(...golpes: number[]): number { … }
```

#### Desafío
Completá el tipo del parámetro rest.

#### Pasos
1. Buscá el `___` después de `...golpes:`.
2. Cambialo por `number[]`.
3. Tocá **Ejecutar**. Tiene que salir `32 en 3 golpes` y `5 en 1 golpes`.

#### Código inicial
```typescript
function sumarGolpes(...golpes: ___): string {
  const total = golpes.reduce((suma, g) => suma + g, 0);
  return `${total} en ${golpes.length} golpes`;
}

console.log(sumarGolpes(10, 15, 7));
console.log(sumarGolpes(5));
```

#### Salida esperada
```
32 en 3 golpes
5 en 1 golpes
```

#### Solución
```typescript
function sumarGolpes(...golpes: number[]): string {
  const total = golpes.reduce((suma, g) => suma + g, 0);
  return `${total} en ${golpes.length} golpes`;
}

console.log(sumarGolpes(10, 15, 7));
console.log(sumarGolpes(5));
```

#### Al superarla
El martillo da sus golpes, *pum, pum, pum*, y la máquina anota cada uno.

#### Imagen
- Un martillo neumático de latón golpeando una placa sobre un yunque, con vapor y chispas chiquitas.
- Rigel (chico flaco con pecas, antiparras de latón bajadas sobre los ojos, chaleco marrón) cuenta los golpes.
- Gheco tapándose los oídos.

### Micro-misión R01-N04-P6 · La cinta de las piezas

```meta
lugar: Las máquinas de medir
personajes: Rigel, Gheco, Astrea
carta: Flecha tipada | const doble = (n: number): number => n * 2 · en map y filter el tipo ya se sarecompensa: xp 15, monedas 5
recompensa: xp 15, monedas 5
```

#### Escena
Una cinta transporta piezas hacia el Planisferio. Antes de montarlas, cada medida se agranda al doble, y las chicas se descartan.

#### Gheco sugiere
Una función flecha se anota igual: el tipo de cada parámetro y, después de los paréntesis, lo que devuelve:

```ts
const doble = (n: number): number => n * 2;
const esGrande = (n: number): boolean => n > 10;
```

`map(doble)` le aplica `doble` a cada elemento y `filter(esGrande)` se queda con los que dan `true`.

#### Desafío
Completá las dos funciones flecha.

#### Pasos
1. En `doble`, el `___` es lo que devuelve: `n * 2`.
2. En `esGrande`, el `___` es el tipo que devuelve: `boolean`.
3. Tocá **Ejecutar**. Tiene que salir `Para el Planisferio: 24, 14, 20`.

#### Código inicial
```typescript
const doble = (n: number): number => ___;
const esGrande = (n: number): ___ => n > 10;

const medidas: number[] = [12, 4, 7, 10];
const listas = medidas.map(doble).filter(esGrande);
console.log(`Para el Planisferio: ${listas.join(', ')}`);
```

#### Salida esperada
```
Para el Planisferio: 24, 14, 20
```

#### Solución
```typescript
const doble = (n: number): number => n * 2;
const esGrande = (n: number): boolean => n > 10;

const medidas: number[] = [12, 4, 7, 10];
const listas = medidas.map(doble).filter(esGrande);
console.log(`Para el Planisferio: ${listas.join(', ')}`);
```

#### Al superarla
La cinta avanza, las piezas chicas caen a un canasto y las demás suben hasta el Planisferio. Astrea le da una **estrella de latón**.

#### Imagen
- Una cinta transportadora de latón que lleva piezas de vidrio hacia un planetario mecánico, con un canasto al costado para las piezas chicas.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) controla una palanca.
- Astrea (lechuza con anteojos de latón) le entrega una ficha con una estrella; Gheco montado en una pieza.

## R01-N05 · interface: la forma de los datos

```meta
tipo: tema
padre: R01-N04
precio: 10
criatura: skeleton
temas: poo.interfaces, cal.tipos
```

### Crónica

Astrea despliega sobre la mesa una lámina enorme: la **ficha técnica** de una pieza. Dice qué tiene que tener: un nombre, una medida y, a veces, la estrella para la que está hecha. No es una pieza: es la descripción de cómo tiene que ser **cualquier** pieza.

—Cuando todas las piezas siguen la misma ficha, el Planisferio sabe qué esperar de cada una —dice {mentor}—. Esa ficha se llama `interface`.

### Objetivos

- Describir la forma de un objeto con `interface`.
- Ver qué revisa el compilador: lo que falta (`TS2741`) y lo que sobra (`TS2353`).
- Usar propiedades opcionales (`?`) y de solo lectura (`readonly`).
- Extender una interface con `extends`.

### Antes de empezar

- R01-N04: funciones tipadas.
- De JavaScript: objetos, propiedades y arreglos de objetos.

### Explicación

#### La ficha técnica
```typescript
interface Pieza {
  nombre: string;
  medida: number;
}

const lente: Pieza = { nombre: 'lente', medida: 4 };
```

Una `interface` dice **qué propiedades** tiene un objeto y de qué tipo. No crea nada: solo existe para el compilador (en el JavaScript que corre, desaparece).

#### Lo que revisa
```typescript
const a: Pieza = { nombre: 'biela' };                       // ✗ TS2741: falta medida
const b: Pieza = { nombre: 'biela', medida: 12, color: 1 }; // ✗ TS2353: color no está en la ficha
console.log(lente.peso);                                    // ✗ TS2339: Pieza no tiene peso
```

#### Opcional y solo lectura
```typescript
interface Pieza {
  readonly id: string;   // no se puede cambiar después de crearla
  nombre: string;
  medida: number;
  estrella?: string;     // puede faltar
}
```

`pieza.id = 'otro'` da `TS2540`. Y `pieza.estrella` puede ser `undefined`: usá `??` o preguntá antes.

#### Extender
```typescript
interface Lente extends Pieza {
  aumento: number;
}
```

Un `Lente` tiene todo lo de `Pieza` **más** `aumento`.

### Código de ejemplo

```typescript
interface Pieza {
  readonly id: string;
  nombre: string;
  medida: number;
  estrella?: string;
}

interface Lente extends Pieza {
  aumento: number;
}

const biela: Pieza = { id: 'p-1', nombre: 'biela', medida: 12 };
const ocular: Lente = { id: 'p-2', nombre: 'ocular', medida: 4, estrella: 'Rigel', aumento: 30 };

function describir(p: Pieza): string {
  return `${p.nombre} (${p.medida} mm) para ${p.estrella ?? 'ninguna estrella'}`;
}

console.log(describir(biela));
console.log(describir(ocular), `· aumento ${ocular.aumento}x`);
```

### Salida esperada

```
biela (12 mm) para ninguna estrella
ocular (4 mm) para Rigel · aumento 30x
```

### ¿Para qué sirve?

Los programas de verdad pasan objetos de un lado a otro todo el tiempo: un usuario, un producto, un mensaje. Con una `interface`, cada parte del programa sabe exactamente qué tiene un objeto, el editor te sugiere las propiedades mientras escribís, y un nombre mal escrito se descubre antes de ejecutar.

### Errores habituales

**Esqueleto: falta una propiedad (TS2741).** *La propiedad "medida" falta en el tipo "{ nombre: string; }", pero es obligatoria en el tipo "Pieza"*. Agregala, o hacela opcional con `?` si de verdad puede faltar.

**Esqueleto: una propiedad que no está en la ficha (TS2353).** Casi siempre es un nombre mal escrito: `medidda` en vez de `medida`.

**Ogro: cambiar algo readonly (TS2540).** *No se puede asignar a "id" porque es una propiedad de solo lectura*.

**Orco: usar un opcional sin preguntar.** `p.estrella.toUpperCase()` da `TS18048`: *"p.estrella" es posiblemente "undefined"*.

### Micro-misión R01-N05-P1 · La ficha técnica

```meta
lugar: La mesa de Astrea
personajes: Rigel, Gheco, Astrea
carta: interface | interface Pieza { nombre: string; medida: number } · describe la forma de un objeto · no crea nada
recompensa: xp 10, oro 10
```

#### Escena
Astrea le pide a Rigel que escriba la ficha técnica de las piezas: qué tiene que tener cada una.

#### Gheco sugiere
Una `interface` describe la **forma** de un objeto: qué propiedades tiene y de qué tipo.

```ts
interface Estrella {
  nombre: string;
  distancia: number;
}
```

Después se usa como un tipo más: `const vega: Estrella = { nombre: 'Vega', distancia: 25 };`.

#### Desafío
Completá la ficha `Pieza` con sus dos propiedades.

#### Pasos
1. El primer `___` es el tipo de `nombre`: `string`.
2. El segundo `___` es el tipo de `medida`: `number`.
3. Tocá **Ejecutar**. Tiene que salir `lente: 4 mm`.

#### Código inicial
```typescript
interface Pieza {
  nombre: ___;
  medida: ___;
}

const lente: Pieza = { nombre: 'lente', medida: 4 };
console.log(`${lente.nombre}: ${lente.medida} mm`);
```

#### Salida esperada
```
lente: 4 mm
```

#### Solución
```typescript
interface Pieza {
  nombre: string;
  medida: number;
}

const lente: Pieza = { nombre: 'lente', medida: 4 };
console.log(`${lente.nombre}: ${lente.medida} mm`);
```

#### Al superarla
Astrea clava la ficha en la pared, con una chinche de bronce. Desde ahora, toda pieza nueva se compara con ella.

#### Imagen
- Una lámina técnica grande clavada en una pared de madera, con el dibujo de una pieza de vidrio y sus medidas (sin letras legibles).
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) la escribe con una pluma.
- Astrea (lechuza grande gris azulada con anteojos de latón y chaleco azul) sostiene la chinche; Gheco mira.

### Micro-misión R01-N05-P2 · La pieza incompleta

```meta
lugar: La mesa de Astrea
personajes: Rigel, Gheco
criatura: skeleton
carta: TS2741 | falta una propiedad que la interface pide · agregala o hacela opcional
recompensa: xp 10, oro 10
```

#### Escena
Llega una biela sin su medida anotada. Un **esqueleto** de alambre se esconde en el hueco donde debería estar el número.

#### Gheco sugiere
Si a un objeto le falta una propiedad que la `interface` pide, el compilador avisa con `TS2741` y dice **cuál** falta.

#### Desafío
Agregale a `biela` su medida: `12`.

#### Pasos
1. Tocá **Ejecutar** y leé qué propiedad falta.
2. En el objeto, después de `nombre: 'biela'`, agregá `, medida: 12`.
3. Tocá **Ejecutar**. Tiene que salir `biela: 12 mm`.

#### Código inicial
```typescript
interface Pieza {
  nombre: string;
  medida: number;
}

const biela: Pieza = { nombre: 'biela' };
console.log(`${biela.nombre}: ${biela.medida} mm`);
```

#### Salida esperada
```
biela: 12 mm
```

#### Solución
```typescript
interface Pieza {
  nombre: string;
  medida: number;
}

const biela: Pieza = { nombre: 'biela', medida: 12 };
console.log(`${biela.nombre}: ${biela.medida} mm`);
```

#### Al superarla
Con la medida anotada, el hueco se cierra y el esqueleto queda afuera, desarmado.

#### Imagen
- Una biela de latón sobre la mesa con una etiqueta a la que le falta un pedazo, y un esqueleto de alambre chiquito asomado por el hueco.
- Rigel (chico flaco con pecas, antiparras de latón) completa la etiqueta.
- Gheco señala al esqueleto.

### Micro-misión R01-N05-P3 · Para qué estrella

```meta
lugar: La mesa de Astrea
personajes: Rigel, Gheco
carta: Propiedad opcional | estrella?: string · puede faltar · p.estrella ?? 'ninguna' para usarla
recompensa: xp 10, oro 10
```

#### Escena
Algunas piezas se hacen para una estrella en particular; otras sirven para cualquiera. Rigel quiere que la ficha lo permita.

#### Gheco sugiere
Una propiedad con `?` es **opcional**: el objeto puede no tenerla. Si falta, vale `undefined`, y por eso hay que usarla con `??`:

```ts
`${p.estrella ?? 'cualquiera'}`
```

#### Desafío
Hacé opcional la propiedad `estrella` en la ficha.

#### Pasos
1. Tocá **Ejecutar**: la biela no tiene estrella y el compilador se queja.
2. En la `interface`, cambiá `estrella: string;` por `estrella?: string;`.
3. Tocá **Ejecutar**. Tiene que salir `ocular → Rigel` y `biela → cualquiera`.

#### Código inicial
```typescript
interface Pieza {
  nombre: string;
  estrella: string;
}

const piezas: Pieza[] = [
  { nombre: 'ocular', estrella: 'Rigel' },
  { nombre: 'biela' },
];
for (const p of piezas) console.log(`${p.nombre} → ${p.estrella ?? 'cualquiera'}`);
```

#### Salida esperada
```
ocular → Rigel
biela → cualquiera
```

#### Solución
```typescript
interface Pieza {
  nombre: string;
  estrella?: string;
}

const piezas: Pieza[] = [
  { nombre: 'ocular', estrella: 'Rigel' },
  { nombre: 'biela' },
];
for (const p of piezas) console.log(`${p.nombre} → ${p.estrella ?? 'cualquiera'}`);
```

#### Al superarla
Rigel separa las piezas en dos cajas: las que tienen dueña y las que sirven para cualquier estrella.

#### Imagen
- Dos cajas de madera: una con piezas atadas con cintas que tienen una estrellita, otra con piezas sueltas.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) reparte las piezas.
- Gheco sentado en el borde de una caja.

### Micro-misión R01-N05-P4 · El número de serie

```meta
lugar: La mesa de Astrea
personajes: Rigel, Gheco
criatura: ogre
carta: readonly | readonly id: string · se pone al crear y no se cambia más · cambiarlo es TS2540
recompensa: xp 10, oro 10
```

#### Escena
Cada pieza tiene un número de serie grabado a fuego. Un **ogro** quiere cambiarlo para hacer pasar una pieza vieja por nueva.

#### Gheco sugiere
`readonly` marca una propiedad de **solo lectura**: se pone al crear el objeto y después no se puede cambiar. Si alguien lo intenta, el compilador avisa con `TS2540`.

#### Desafío
Marcá `id` como `readonly` y borrá la línea del ogro, que lo cambia.

#### Pasos
1. En la `interface`, cambiá `id: string;` por `readonly id: string;`.
2. Tocá **Ejecutar**: ahora la línea del ogro da `TS2540`.
3. Borrá la línea `ocular.id = 'p-999';`.
4. Tocá **Ejecutar**. Tiene que salir `p-7: ocular`.

#### Código inicial
```typescript
interface Pieza {
  id: string;
  nombre: string;
}

const ocular: Pieza = { id: 'p-7', nombre: 'ocular' };
ocular.id = 'p-999';
console.log(`${ocular.id}: ${ocular.nombre}`);
```

#### Salida esperada
```
p-7: ocular
```

#### Solución
```typescript
interface Pieza {
  readonly id: string;
  nombre: string;
}

const ocular: Pieza = { id: 'p-7', nombre: 'ocular' };
console.log(`${ocular.id}: ${ocular.nombre}`);
```

#### Al superarla
El ogro pasa el buril por el número, una y otra vez: no se borra. Se va gruñendo.

#### Imagen
- Una pieza de vidrio con un número de serie grabado en un aro de latón (sin números legibles).
- Un ogro chiquito con un buril que no logra rayar el aro.
- Rigel (chico flaco con pecas, antiparras de latón) cruzado de brazos; Gheco se ríe.

### Micro-misión R01-N05-P5 · El lente es una pieza

```meta
lugar: El Telescopio Mayor
personajes: Rigel, Gheco, Astrea
carta: extends | interface Lente extends Pieza { aumento: number } · tiene todo lo de Pieza y algo más
recompensa: xp 15, monedas 5
```

#### Escena
Los lentes son piezas, pero con algo más: el aumento. Astrea no quiere copiar toda la ficha de la pieza para escribir la del lente.

#### Gheco sugiere
Con `extends`, una `interface` toma todo lo de otra y le suma lo suyo:

```ts
interface Lente extends Pieza {
  aumento: number;
}
```

Un `Lente` tiene `nombre`, `medida` **y** `aumento`. Y sirve en cualquier lugar donde se pida una `Pieza`.

#### Desafío
Completá la `interface` del lente para que extienda a `Pieza`.

#### Pasos
1. Buscá el `___` después de `interface Lente`.
2. Cambialo por `extends Pieza`.
3. Tocá **Ejecutar**. Tiene que salir `ocular: 4 mm, aumento 30x`.

#### Código inicial
```typescript
interface Pieza {
  nombre: string;
  medida: number;
}

interface Lente ___ {
  aumento: number;
}

const ocular: Lente = { nombre: 'ocular', medida: 4, aumento: 30 };
console.log(`${ocular.nombre}: ${ocular.medida} mm, aumento ${ocular.aumento}x`);
```

#### Salida esperada
```
ocular: 4 mm, aumento 30x
```

#### Solución
```typescript
interface Pieza {
  nombre: string;
  medida: number;
}

interface Lente extends Pieza {
  aumento: number;
}

const ocular: Lente = { nombre: 'ocular', medida: 4, aumento: 30 };
console.log(`${ocular.nombre}: ${ocular.medida} mm, aumento ${ocular.aumento}x`);
```

#### Al superarla
Rigel monta el ocular en el telescopio. Por primera vez ve una estrella de cerca: tiembla un poco, como si respirara.

#### Imagen
- Un telescopio grande de latón con un ocular nuevo montado, apuntando a un cielo estrellado por la abertura de la cúpula.
- Rigel (chico flaco con pecas, antiparras de latón subidas a la frente, chaleco marrón) mira por el ocular.
- Astrea (lechuza con anteojos de latón) a su lado; Gheco sobre el tubo.

### Micro-misión R01-N05-P6 · El pedido de piezas

```meta
lugar: La mesa de Astrea
personajes: Rigel, Gheco, Astrea
carta: Arreglo de interfaces | Pieza[] · una función que recibe Pieza · la estrella opcional con recompensa: xp 15, monedas 5
recompensa: xp 15, monedas 5
```

#### Escena
Para el Planisferio faltan tres piezas. Rigel arma el pedido a la Ciudadela, con una función que describe cada una.

#### Gheco sugiere
Una `interface` se usa como cualquier tipo: en un arreglo (`Pieza[]`) y en los parámetros de una función.

```ts
function describir(p: Pieza): string { … }
```

Adentro, `p.` ya sabe qué propiedades hay.

#### Desafío
Completá la función `describir`: el nombre, la medida y la estrella (o `cualquiera`).

#### Pasos
1. El primer `___` es el tipo del parámetro: `Pieza`.
2. El segundo `___` es la estrella o `cualquiera`: `p.estrella ?? 'cualquiera'`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
interface Pieza {
  nombre: string;
  medida: number;
  estrella?: string;
}

const pedido: Pieza[] = [
  { nombre: 'ocular', medida: 4, estrella: 'Rigel' },
  { nombre: 'biela', medida: 12 },
  { nombre: 'resorte', medida: 3, estrella: 'Vega' },
];

function describir(p: ___): string {
  return `${p.nombre} de ${p.medida} mm para ${___}`;
}

for (const p of pedido) console.log(describir(p));
```

#### Salida esperada
```
ocular de 4 mm para Rigel
biela de 12 mm para cualquiera
resorte de 3 mm para Vega
```

#### Solución
```typescript
interface Pieza {
  nombre: string;
  medida: number;
  estrella?: string;
}

const pedido: Pieza[] = [
  { nombre: 'ocular', medida: 4, estrella: 'Rigel' },
  { nombre: 'biela', medida: 12 },
  { nombre: 'resorte', medida: 3, estrella: 'Vega' },
];

function describir(p: Pieza): string {
  return `${p.nombre} de ${p.medida} mm para ${p.estrella ?? 'cualquiera'}`;
}

for (const p of pedido) console.log(describir(p));
```

#### Al superarla
Astrea firma el pedido con su compás y lo manda por el ascensor. —Con fichas así, en la Ciudadela no se equivocan nunca. —Le da una **estrella de latón**.

#### Imagen
- Una hoja de pedido enrollada dentro de un tubo de latón, en el ascensor de vapor listo para bajar.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mete el tubo en el ascensor.
- Astrea (lechuza con anteojos de latón) le da una ficha con una estrella; Gheco en el ascensor.

## R01-N06 · type: uniones, alias y tipos de función

```meta
tipo: tema
padre: R01-N05
precio: 10
criatura: goblin
temas: cal.tipos, prog.funciones
```

### Crónica

Las palancas del Planisferio no aceptan cualquier posición: solo *parado*, *girando* o *trabado*. Rigel intentó ponerla en *a medias* y la palanca rebotó.

—Hay cosas que tienen pocas formas posibles —dice {mentor}—. Para nombrarlas, en el Mirador usamos `type`. Con `type` se le pone nombre a **cualquier** tipo: una forma de objeto, una lista cerrada de opciones o la firma de una máquina.

### Objetivos

- Ponerle nombre a un tipo con `type`.
- Hacer una **unión**: un valor que puede ser de varios tipos (`number | string`) o una lista cerrada de opciones (`'parado' | 'girando'`).
- Escribir el tipo de una función: `(a: number, b: number) => number`.
- Conocer la **sobrecarga**: varias firmas para la misma función.

### Antes de empezar

- R01-N05: `interface`.
- R01-N03: estrechar con `typeof`.

### Explicación

#### Un nombre para cualquier tipo
```typescript
type Punto = { x: number; y: number };   // como una interface
type Id = number;                         // un tipo básico con otro nombre
```

> `interface` y `type` se parecen mucho para describir objetos. La regla práctica: **`interface` para objetos, `type` para todo lo demás** (uniones, funciones, tuplas).

#### Uniones: esto **o** aquello
```typescript
type Medida = number | string;   // un número o un texto
let m: Medida = 12;
m = '12 mm';                     // ✓ también vale
```

Para usar una unión, se estrecha con `typeof`, como con `unknown`.

#### Una lista cerrada de opciones
```typescript
type Estado = 'parado' | 'girando' | 'trabado';
let palanca: Estado = 'parado';
palanca = 'a medias';   // ✗ TS2322: no es ninguna de las tres
```

Es como un menú: solo se puede elegir lo que está escrito.

#### El tipo de una función
```typescript
type Operacion = (a: number, b: number) => number;
const sumar: Operacion = (a, b) => a + b;   // a y b ya son number
```

Sirve para recibir funciones como parámetro (un *callback*):

```typescript
function aplicar(medidas: number[], cambio: (n: number) => number): number[] {
  return medidas.map(cambio);
}
```

#### Sobrecarga
A veces una función hace cosas distintas según lo que recibe. Se escriben **varias firmas** arriba y **una** implementación que las cubre a todas:

```typescript
function buscar(id: number): string;     // con un número, devuelve el nombre
function buscar(nombre: string): number; // con un nombre, devuelve el número
function buscar(valor: number | string): string | number { … }
```

Así TypeScript sabe que `buscar(1)` devuelve un `string` y `buscar('Vega')` un `number`.

### Código de ejemplo

```typescript
type Estado = 'parado' | 'girando' | 'trabado';
type Medida = number | string;
type Operacion = (a: number, b: number) => number;

let palanca: Estado = 'parado';
palanca = 'girando';

function enMilimetros(m: Medida): number {
  if (typeof m === 'number') return m;
  return Number.parseFloat(m);
}

const sumar: Operacion = (a, b) => a + b;

function aplicar(medidas: number[], cambio: (n: number) => number): number[] {
  return medidas.map(cambio);
}

console.log(palanca, enMilimetros(12), enMilimetros('4.5 mm'));
console.log(sumar(3, 4), aplicar([1, 2, 3], (n) => n * 10));
```

### Salida esperada

```
girando 12 4.5
7 [ 10, 20, 30 ]
```

### ¿Para qué sirve?

Muchos datos tienen pocas opciones posibles: el estado de un pedido, la dificultad de un juego, el rol de un usuario. Con una unión de opciones, el compilador no deja escribir una que no existe, y el editor te las sugiere. Los tipos de función documentan qué tipo de función esperás recibir.

### Errores habituales

**Goblin: una opción que no está en la lista (TS2322).** *El tipo '"a medias"' no se puede asignar al tipo 'Estado'*. Fijate cómo están escritas las opciones: las mayúsculas y los acentos cuentan.

**Goblin: usar una unión sin estrechar.** Con `m: number | string`, `m.toFixed(1)` da `TS2339`: un texto no tiene `toFixed`. Preguntá antes con `typeof`.

**Esqueleto: la sobrecarga que no coincide (TS2769).** Si llamás con algo que ninguna firma acepta, da *Ninguna sobrecarga coincide con esta llamada*.

### Micro-misión R01-N06-P1 · Un nombre para el punto

```meta
lugar: La Sala de las Figuras
personajes: Rigel, Gheco
carta: type | type Punto = { x: number; y: number }; · un nombre para un tipo · se usa como cualquier tipo
recompensa: xp 10, oro 10
```

#### Escena
Rigel escribe tantas veces `{ x: number; y: number }` en sus planos que le duele la mano. Gheco le propone ponerle un nombre.

#### Gheco sugiere
Con `type` se le pone **nombre** a un tipo, para no repetirlo:

```ts
type Punto = { x: number; y: number };
```

Después, `Punto` se usa como cualquier tipo: en variables, parámetros y arreglos.

#### Desafío
Completá el tipo `Punto`.

#### Pasos
1. Buscá el `___` después de `type Punto =`.
2. Cambialo por `{ x: number; y: number }`.
3. Tocá **Ejecutar**. Tiene que salir `De (1, 2) a (4, 6): 5 de distancia`.

#### Código inicial
```typescript
type Punto = ___;

function distancia(a: Punto, b: Punto): number {
  return Math.hypot(b.x - a.x, b.y - a.y);
}

const desde: Punto = { x: 1, y: 2 };
const hasta: Punto = { x: 4, y: 6 };
console.log(`De (${desde.x}, ${desde.y}) a (${hasta.x}, ${hasta.y}): ${distancia(desde, hasta)} de distancia`);
```

#### Salida esperada
```
De (1, 2) a (4, 6): 5 de distancia
```

#### Solución
```typescript
type Punto = { x: number; y: number };

function distancia(a: Punto, b: Punto): number {
  return Math.hypot(b.x - a.x, b.y - a.y);
}

const desde: Punto = { x: 1, y: 2 };
const hasta: Punto = { x: 4, y: 6 };
console.log(`De (${desde.x}, ${desde.y}) a (${hasta.x}, ${hasta.y}): ${distancia(desde, hasta)} de distancia`);
```

#### Al superarla
Rigel mide con el calibre entre las dos estrellas del plano: exactamente 5. Le guiña un ojo a Gheco.

#### Imagen
- Un plano de constelaciones sobre la mesa, con dos estrellas unidas por una línea de luz.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) mide la distancia con el calibre de latón.
- Gheco sobre el plano.

### Micro-misión R01-N06-P2 · La palanca de tres posiciones

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco
criatura: goblin
carta: Unión de opciones | type Estado = 'parado' | 'girando' | 'trabado' · solo esas · otra es TS2322
recompensa: xp 10, oro 10
```

#### Escena
Un goblin quiere poner la palanca del Planisferio en *a medias*. La palanca no tiene esa posición.

#### Gheco sugiere
Con `|` se hace una **unión**: el valor puede ser una cosa **o** la otra. Con textos entre comillas, es una lista cerrada de opciones:

```ts
type Estado = 'parado' | 'girando' | 'trabado';
```

Cualquier otro texto da `TS2322`.

#### Desafío
Poné la palanca en una posición que exista: `'girando'`.

#### Pasos
1. Tocá **Ejecutar** y leé el error de la línea 4.
2. Cambiá `'a medias'` por `'girando'`.
3. Tocá **Ejecutar**. Tiene que salir `La palanca está: girando`.

#### Código inicial
```typescript
type Estado = 'parado' | 'girando' | 'trabado';

let palanca: Estado = 'parado';
palanca = 'a medias';
console.log(`La palanca está: ${palanca}`);
```

#### Salida esperada
```
La palanca está: girando
```

#### Solución
```typescript
type Estado = 'parado' | 'girando' | 'trabado';

let palanca: Estado = 'parado';
palanca = 'girando';
console.log(`La palanca está: ${palanca}`);
```

#### Al superarla
La palanca cae en su muesca con un *clonc* firme. El goblin prueba empujarla a la mitad: no se queda.

#### Imagen
- Una palanca grande de latón con tres muescas grabadas, al pie de un planetario mecánico.
- Un goblin chiquito con un engranaje en la espalda colgado de la palanca.
- Rigel (chico flaco con pecas, antiparras de latón) la empuja hasta la muesca del medio; Gheco mira.

### Micro-misión R01-N06-P3 · Medidas de dos formas

```meta
lugar: La mesa de Astrea
personajes: Rigel, Gheco
carta: Unión de tipos | type Medida = number | string · estrechar con typeof · Number.parseFloat('4.5 mm') da 4.5
recompensa: xp 10, oro 10
```

#### Escena
Algunas medidas llegan como número (`12`) y otras como texto (`'4.5 mm'`). Rigel necesita todas en milímetros, como número.

#### Gheco sugiere
`type Medida = number | string` acepta las dos formas. Para usarla, se estrecha con `typeof`, como con `unknown`:

```ts
if (typeof m === 'number') return m;
return Number.parseFloat(m);   // acá m ya es string
```

`Number.parseFloat('4.5 mm')` lee el número del principio del texto: `4.5`.

#### Desafío
Completá el `if` que devuelve la medida cuando ya es un número.

#### Pasos
1. Buscá el `___` en el `if`.
2. Cambialo por `typeof m === 'number'`.
3. Tocá **Ejecutar**. Tiene que salir `12 4.5 7`.

#### Código inicial
```typescript
type Medida = number | string;

function enMilimetros(m: Medida): number {
  if (___) return m;
  return Number.parseFloat(m);
}

console.log(enMilimetros(12), enMilimetros('4.5 mm'), enMilimetros('7'));
```

#### Salida esperada
```
12 4.5 7
```

#### Solución
```typescript
type Medida = number | string;

function enMilimetros(m: Medida): number {
  if (typeof m === 'number') return m;
  return Number.parseFloat(m);
}

console.log(enMilimetros(12), enMilimetros('4.5 mm'), enMilimetros('7'));
```

#### Al superarla
Todas las medidas quedan en la misma columna, como números. Astrea las suma de un vistazo.

#### Imagen
- Una planilla de latón con dos columnas de etiquetas que se convierten en una sola columna de fichas (sin números legibles).
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) pasa las etiquetas de una columna a la otra.
- Gheco sobre la planilla.

### Micro-misión R01-N06-P4 · La máquina de operaciones

```meta
lugar: Las máquinas de medir
personajes: Rigel, Gheco
carta: Tipo de función | type Operacion = (a: number, b: number) => number · las flechas que lo usan ya saben los tipos
recompensa: xp 10, oro 10
```

#### Escena
Rigel arma una máquina con varias perillas: sumar, restar, multiplicar. Todas reciben dos números y devuelven uno.

#### Gheco sugiere
Una función también tiene tipo: qué recibe y qué devuelve, con una flecha `=>` en el medio:

```ts
type Operacion = (a: number, b: number) => number;
const restar: Operacion = (a, b) => a - b;
```

Como `restar` es una `Operacion`, `a` y `b` ya son `number` sin anotarlos.

#### Desafío
Completá el tipo `Operacion`.

#### Pasos
1. Buscá el `___` después de `type Operacion =`.
2. Cambialo por `(a: number, b: number) => number`.
3. Tocá **Ejecutar**. Tiene que salir `7 -1 12`.

#### Código inicial
```typescript
type Operacion = ___;

const sumar: Operacion = (a, b) => a + b;
const restar: Operacion = (a, b) => a - b;
const multiplicar: Operacion = (a, b) => a * b;

console.log(sumar(3, 4), restar(3, 4), multiplicar(3, 4));
```

#### Salida esperada
```
7 -1 12
```

#### Solución
```typescript
type Operacion = (a: number, b: number) => number;

const sumar: Operacion = (a, b) => a + b;
const restar: Operacion = (a, b) => a - b;
const multiplicar: Operacion = (a, b) => a * b;

console.log(sumar(3, 4), restar(3, 4), multiplicar(3, 4));
```

#### Al superarla
Las tres perillas giran a la vez y la máquina da tres resultados, uno por cada ventanita.

#### Imagen
- Una máquina de latón con tres perillas y tres ventanitas de vidrio con números de luz (sin números legibles).
- Rigel (chico flaco con pecas, antiparras de latón, guantes sin dedos) gira las perillas.
- Gheco dentro de una ventanita.

### Micro-misión R01-N06-P5 · El buscador del catálogo

```meta
lugar: El catálogo de estrellas
personajes: Rigel, Gheco, Astrea
carta: Sobrecarga | varias firmas arriba · una implementación que las cubre · buscar(1) da string, buscar('Vega') da number
recompensa: xp 15, monedas 5
```

#### Escena
Astrea busca estrellas de dos maneras: por número («¿cuál es la 2?») o por nombre («¿qué número tiene Vega?»). Rigel arma una sola máquina para las dos.

#### Gheco sugiere
La **sobrecarga** son varias firmas para la misma función, escritas arriba **sin cuerpo**:

```ts
function buscar(numero: number): string;
function buscar(nombre: string): number;
```

Abajo va **una** implementación, con un tipo que cubre los dos casos (`number | string`). Así, TypeScript sabe que `buscar(2)` devuelve un texto y `buscar('Vega')` un número.

#### Desafío
Completá la segunda firma: recibe un nombre (texto) y devuelve un número.

#### Pasos
1. Buscá la línea con `___`.
2. Cambiala por `function buscar(nombre: string): number;`.
3. Tocá **Ejecutar**. Tiene que salir `Vega 3`.

#### Código inicial
```typescript
const catalogo: string[] = ['Rigel', 'Vega', 'Sirio', 'Altair'];

function buscar(numero: number): string;
___
function buscar(valor: number | string): string | number {
  if (typeof valor === 'number') return catalogo[valor - 1] ?? 'ninguna';
  return catalogo.indexOf(valor) + 1;
}

console.log(buscar(2), buscar('Sirio'));
```

#### Salida esperada
```
Vega 3
```

#### Solución
```typescript
const catalogo: string[] = ['Rigel', 'Vega', 'Sirio', 'Altair'];

function buscar(numero: number): string;
function buscar(nombre: string): number;
function buscar(valor: number | string): string | number {
  if (typeof valor === 'number') return catalogo[valor - 1] ?? 'ninguna';
  return catalogo.indexOf(valor) + 1;
}

console.log(buscar(2), buscar('Sirio'));
```

#### Al superarla
Astrea gira la máquina hacia un lado y sale un nombre; hacia el otro, un número. —Una máquina, dos preguntas.

#### Imagen
- Un fichero giratorio de latón con tarjetas de estrellas, con una manivela de cada lado.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) gira una manivela.
- Astrea (lechuza con anteojos de latón) lee una tarjeta; Gheco sobre el fichero.

### Micro-misión R01-N06-P6 · El ajuste de la cinta

```meta
lugar: Las máquinas de medir
personajes: Rigel, Gheco, Astrea
carta: Callback tipado | cambio: (n: number) => number · la función que recibe otra función · map aplica el cambrecompensa: xp 15, monedas 5
recompensa: xp 15, monedas 5
```

#### Escena
La cinta de piezas necesita ajustes distintos según el día: a veces agranda, a veces achica. Rigel arma una máquina que recibe **el ajuste** como pieza intercambiable.

#### Gheco sugiere
Una función puede recibir **otra función** como parámetro (un *callback*). Se anota con el tipo de función:

```ts
function ajustar(medidas: number[], cambio: (n: number) => number): number[] {
  return medidas.map(cambio);
}
```

Al llamarla, le pasás la función que quieras: `ajustar(m, (n) => n + 1)`.

#### Desafío
Completá el tipo del parámetro `cambio`.

#### Pasos
1. Buscá el `___` después de `cambio:`.
2. Cambialo por `(n: number) => number`.
3. Tocá **Ejecutar**. Tiene que salir `Agrandadas: 24, 8, 14` y `Achicadas: 6, 2, 3.5`.

#### Código inicial
```typescript
function ajustar(medidas: number[], cambio: ___): number[] {
  return medidas.map(cambio);
}

const medidas: number[] = [12, 4, 7];
console.log(`Agrandadas: ${ajustar(medidas, (n) => n * 2).join(', ')}`);
console.log(`Achicadas: ${ajustar(medidas, (n) => n / 2).join(', ')}`);
```

#### Salida esperada
```
Agrandadas: 24, 8, 14
Achicadas: 6, 2, 3.5
```

#### Solución
```typescript
function ajustar(medidas: number[], cambio: (n: number) => number): number[] {
  return medidas.map(cambio);
}

const medidas: number[] = [12, 4, 7];
console.log(`Agrandadas: ${ajustar(medidas, (n) => n * 2).join(', ')}`);
console.log(`Achicadas: ${ajustar(medidas, (n) => n / 2).join(', ')}`);
```

#### Al superarla
Rigel cambia la pieza del ajuste como quien cambia una lente. La cinta obedece. Astrea le da una **estrella de latón**.

#### Imagen
- Una máquina de latón con un hueco donde se encastra una pieza intercambiable, y dos piezas distintas en la mesa.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) encastra una de las piezas.
- Astrea (lechuza con anteojos de latón) le da una ficha con una estrella; Gheco mira.

## R01-N07 · Jefe: el Camaleón Any

```meta
tipo: jefe
padre: R01-N06
precio: 10
criatura: dragon
insignia: Escama del Camaleón
insignia_descripcion: Venciste al Camaleón Any: medís cada pieza antes de montarla.
usa: cal.tipos, poo.interfaces, prog.funciones, col.listas
```

### Crónica

Una noche, Rigel encuentra la Sala de las Figuras revuelta. Las fichas técnicas dicen `any` donde antes decían `number`, las palancas aceptan cualquier posición y el Planisferio da cuentas absurdas: *4123 milímetros*.

Sobre el estante tapado, un autómata de latón cambia de color sin parar. Es el **Camaleón Any**: su cuerpo está hecho de piezas sin medida, y por eso entra en cualquier ranura y esconde todos los errores.

—Mientras todo diga `any`, el compilador no puede ver nada —dice {mentor}—. Vas a tener que devolverle su medida a cada pieza, una por una. Cuando ya no quede ningún `any`, el Camaleón no va a tener dónde esconderse.

### Objetivos

- Integrar todo lo de la rama: tipos básicos, arreglos, tuplas, `unknown`, funciones tipadas, `interface` y `type`.
- Reemplazar `any` por el tipo de verdad y arreglar los errores que aparecen.
- Revisar con `typeof` lo que llega sin tipo.

### Antes de empezar

- Todos los nodos de la Sala de las Figuras (R01-N01 a R01-N06).

### Explicación

#### Cómo encarar un jefe
1. **Leé la consigna entera** y anotá qué datos entran y qué tiene que salir.
2. **Buscá los `any`**: cada uno es un lugar donde el Camaleón esconde un error.
3. **Cambialos de a uno** por el tipo de verdad y ejecutá: el compilador te va a mostrar lo que estaba escondido.
4. **Arreglá lo que aparezca**, leyendo cada error con su línea.

#### Las trampas del Camaleón (y la verdad)
| El Camaleón dice… | La verdad |
|---|---|
| "con `any` compila todo" | compila, pero los errores aparecen al ejecutar |
| "`'12'` y `12` son lo mismo" | uno es texto y el otro número: `4 + '12'` da `'412'` |
| "una palanca acepta cualquier palabra" | una unión de opciones solo acepta las que están escritas |
| "lo que llega, se usa" | lo que llega sin tipo es `unknown`: se revisa con `typeof` |

### Micro-misión R01-N07-P1 · Las fichas del Camaleón

```meta
lugar: La Sala de las Figuras
personajes: Rigel, Gheco, el Camaleón Any
criatura: goblin
carta: Trampa 1 | cambiá any por el tipo de verdad · el compilador muestra el dato mal cargado · '12' no es 12
recompensa: xp 15, monedas 3
```

#### Escena
El Camaleón cambió la ficha técnica de las piezas: ahora todo es `any`. El total de las medidas da *4123 mm*, y nadie sabe por qué.

#### Gheco sugiere
Con `any`, el compilador no revisa nada. Una de las medidas quedó cargada como texto (`'12'`), y `4 + '12'` **pega** en vez de sumar: da `'412'`.

Si la ficha dice el tipo de verdad (`nombre: string; medida: number`), el compilador encuentra enseguida el dato mal cargado.

#### Desafío
Cambiá los dos `any` de la ficha por su tipo de verdad, y arreglá el dato que aparece mal.

#### Pasos
1. Tocá **Ejecutar**: da `Total: 4123 mm`, que está mal.
2. En la `interface`, cambiá `nombre: any;` por `nombre: string;` y `medida: any;` por `medida: number;`.
3. Ejecutá: el compilador marca la biela (`TS2322`). Cambiá `medida: '12'` por `medida: 12`.
4. Tocá **Ejecutar**. Tiene que salir `Total: 19 mm`.

#### Código inicial
```typescript
interface Pieza {
  nombre: any;
  medida: any;
}

const piezas: Pieza[] = [
  { nombre: 'ocular', medida: 4 },
  { nombre: 'biela', medida: '12' },
  { nombre: 'resorte', medida: 3 },
];

let total = 0;
for (const p of piezas) total += p.medida;
console.log(`Total: ${total} mm`);
```

#### Salida esperada
```
Total: 19 mm
```

#### Solución
```typescript
interface Pieza {
  nombre: string;
  medida: number;
}

const piezas: Pieza[] = [
  { nombre: 'ocular', medida: 4 },
  { nombre: 'biela', medida: 12 },
  { nombre: 'resorte', medida: 3 },
];

let total = 0;
for (const p of piezas) total += p.medida;
console.log(`Total: ${total} mm`);
```

#### Al superarla
La ficha técnica recupera su letra prolija. El Camaleón pierde una escama de color y se queda, por un momento, de un solo gris.

#### Imagen
- Una ficha técnica clavada en la pared, con manchas de colores cambiantes que se borran y vuelven a ser letras prolijas (sin texto legible).
- El Camaleón Any (un autómata de latón y vidrio con forma de camaleón, que cambia de color) se aferra al estante.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) corrige la ficha con una pluma; Gheco en su hombro.

### Micro-misión R01-N07-P2 · La caldera del Camaleón

```meta
lugar: Las calderas del Mirador
personajes: Rigel, Gheco, el Camaleón Any
criatura: goblin
carta: Trampa 2 | parámetros con any no protegen las llamadas · tipá la firma · el compilador encuentra la llamada mal hecha
recompensa: xp 15, monedas 3
```

#### Escena
El Camaleón metió la mano en la caldera: la función que suma la presión acepta cualquier cosa, y el manómetro marca *405*. Si sigue subiendo, explota.

#### Gheco sugiere
Una función con parámetros `any` acepta lo que sea, y nadie revisa las llamadas. Con la firma tipada (`(base: number, extra: number): number`), el compilador revisa cada llamada y encuentra la que está mal.

#### Desafío
Tipá la firma de `presion` y arreglá la llamada que aparece mal.

#### Pasos
1. En la firma, cambiá los tres `any`: `base: number`, `extra: number` y `: number` después de los paréntesis.
2. Ejecutá: la llamada da `TS2345`. Cambiá `'5'` por `5`.
3. Tocá **Ejecutar**. Tiene que salir `Presión: 45`.

#### Código inicial
```typescript
function presion(base: any, extra: any): any {
  return base + extra;
}

console.log(`Presión: ${presion(40, '5')}`);
```

#### Salida esperada
```
Presión: 45
```

#### Solución
```typescript
function presion(base: number, extra: number): number {
  return base + extra;
}

console.log(`Presión: ${presion(40, 5)}`);
```

#### Al superarla
La aguja del manómetro baja de golpe hasta el 45. La caldera deja de temblar. El Camaleón retira la mano quemada.

#### Imagen
- Una caldera de cobre con un manómetro cuya aguja baja de la zona roja a la normal (sin números legibles).
- El Camaleón Any (autómata de latón con forma de camaleón que cambia de color) retira una pata de la caldera.
- Rigel (chico flaco con pecas, antiparras de latón bajadas, guantes sin dedos) cierra una válvula; Gheco señala el manómetro.

### Micro-misión R01-N07-P3 · La palanca mal escrita

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco, el Camaleón Any
criatura: goblin
carta: Trampa 3 | una unión de opciones descubre lo mal escrito · 'girnado' no es 'girando'
recompensa: xp 15, monedas 3
```

#### Escena
Rigel pone la palanca del Planisferio en *girando*, pero el Planisferio sigue parado. El Camaleón le cambió la palanca por una que acepta cualquier palabra… y Rigel escribió mal la suya.

#### Gheco sugiere
Con `let modo: any`, cualquier texto vale, aunque esté mal escrito. Con el tipo `Modo`, una **unión de opciones**, el compilador solo acepta las que están en la lista, y descubre la que está mal escrita.

#### Desafío
Cambiá `any` por `Modo` y arreglá lo que aparece mal escrito.

#### Pasos
1. Tocá **Ejecutar**: dice `Sigue parado`, aunque la palanca está «en girando».
2. Cambiá `let modo: any` por `let modo: Modo`.
3. Ejecutá: el compilador marca `'girnado'` (`TS2322`). Corregilo: `'girando'`.
4. Tocá **Ejecutar**. Tiene que salir `El Planisferio gira`.

#### Código inicial
```typescript
type Modo = 'parado' | 'girando' | 'trabado';

let modo: any = 'parado';
modo = 'girnado';
console.log(modo === 'girando' ? 'El Planisferio gira' : 'Sigue parado');
```

#### Salida esperada
```
El Planisferio gira
```

#### Solución
```typescript
type Modo = 'parado' | 'girando' | 'trabado';

let modo: Modo = 'parado';
modo = 'girando';
console.log(modo === 'girando' ? 'El Planisferio gira' : 'Sigue parado');
```

#### Al superarla
El Planisferio arranca, despacio, y la primera constelación da media vuelta. El Camaleón pierde otra escama de color.

#### Imagen
- Un planetario mecánico gigante empezando a girar, con una constelación de vidrio moviéndose.
- El Camaleón Any (autómata de latón con forma de camaleón) se aferra a un brazo del planetario, perdiendo colores.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sostiene la palanca; Gheco festeja.

### Micro-misión R01-N07-P4 · Lo que trae el ascensor

```meta
lugar: El ascensor de vapor
personajes: Rigel, Gheco, el Camaleón Any
criatura: goblin
carta: Trampa 4 | lo que llega sin tipo es unknown · typeof number → se usa · typeof string → parseFloat · lo demás vale 0
recompensa: xp 15, monedas 3
```

#### Escena
El ascensor trae una caja de lecturas de la Ciudadela, mezcladas por el Camaleón: números, textos con milímetros, un `null` y hasta un `true`. Rigel necesita la suma, en milímetros.

#### Gheco sugiere
Lo que llega sin saber qué es se anota `unknown` y se revisa antes de usar:

```ts
if (typeof dato === 'number') return dato;
if (typeof dato === 'string') return Number.parseFloat(dato);
return 0;
```

Lo que no es ni número ni texto, no suma nada.

#### Desafío
Completá las dos preguntas de `aMilimetros`.

#### Pasos
1. El primer `___`: `typeof dato === 'number'`.
2. El segundo `___`: `typeof dato === 'string'`.
3. Tocá **Ejecutar**. Tiene que salir `Suma: 23.5 mm`.

#### Código inicial
```typescript
const lecturas: unknown[] = [12, '4.5 mm', null, '7', true];

function aMilimetros(dato: unknown): number {
  if (___) return dato;
  if (___) return Number.parseFloat(dato);
  return 0;
}

let suma = 0;
for (const dato of lecturas) suma += aMilimetros(dato);
console.log(`Suma: ${suma} mm`);
```

#### Salida esperada
```
Suma: 23.5 mm
```

#### Solución
```typescript
const lecturas: unknown[] = [12, '4.5 mm', null, '7', true];

function aMilimetros(dato: unknown): number {
  if (typeof dato === 'number') return dato;
  if (typeof dato === 'string') return Number.parseFloat(dato);
  return 0;
}

let suma = 0;
for (const dato of lecturas) suma += aMilimetros(dato);
console.log(`Suma: ${suma} mm`);
```

#### Al superarla
Rigel separa lo que sirve de lo que no. El `null` y el `true` vuelven a la caja; el Camaleón, sin trampas nuevas, retrocede.

#### Imagen
- Una caja de madera en el ascensor de vapor con papelitos, fichas, una tuerca y una lámpara apagada mezclados.
- El Camaleón Any (autómata de latón con forma de camaleón) retrocede, cada vez más gris.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) ordena el contenido; Gheco ayuda.

### Micro-misión R01-N07-P5 · El Camaleón cae

```meta
lugar: La Sala de las Figuras
personajes: Rigel, Gheco, Astrea, el Camaleón Any
criatura: dragon
carta: El jefe | interface con opcional · unión de tipos · callback tipado · cada pieza con su medida
recompensa: xp 20, monedas 5
```

#### Escena
Acorralado, el Camaleón se esconde en lo último que le queda: el informe del Planisferio. Si Rigel lo escribe con cada pieza bien medida, el Camaleón no va a tener dónde meterse.

#### Gheco sugiere
Todo lo de la rama junto:
- la ficha `Pieza` (una `interface`) con la estrella **opcional**;
- la medida que puede llegar como número o como texto (`Medida = number | string`);
- una función que recibe un **ajuste** (un callback `(n: number) => number`).

#### Desafío
Completá los tres huecos del informe.

#### Pasos
1. En la `interface`, el `___` hace opcional a la estrella: `estrella?: string;`.
2. En `aMilimetros`, el `___` pregunta si ya es número: `typeof m === 'number'`.
3. En `informe`, el `___` es el tipo del ajuste: `(n: number) => number`.
4. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Medida = number | string;

interface Pieza {
  nombre: string;
  medida: Medida;
  ___
}

function aMilimetros(m: Medida): number {
  if (___) return m;
  return Number.parseFloat(m);
}

function informe(piezas: Pieza[], ajuste: ___): void {
  let total = 0;
  for (const p of piezas) {
    const mm = ajuste(aMilimetros(p.medida));
    total += mm;
    console.log(`${p.nombre}: ${mm} mm (${p.estrella ?? 'cualquiera'})`);
  }
  console.log(`Total: ${total} mm`);
}

informe(
  [
    { nombre: 'ocular', medida: 4, estrella: 'Rigel' },
    { nombre: 'biela', medida: '12 mm' },
    { nombre: 'resorte', medida: '3.5', estrella: 'Vega' },
  ],
  (n) => n * 2,
);
```

#### Salida esperada
```
ocular: 8 mm (Rigel)
biela: 24 mm (cualquiera)
resorte: 7 mm (Vega)
Total: 39 mm
```

#### Solución
```typescript
type Medida = number | string;

interface Pieza {
  nombre: string;
  medida: Medida;
  estrella?: string;
}

function aMilimetros(m: Medida): number {
  if (typeof m === 'number') return m;
  return Number.parseFloat(m);
}

function informe(piezas: Pieza[], ajuste: (n: number) => number): void {
  let total = 0;
  for (const p of piezas) {
    const mm = ajuste(aMilimetros(p.medida));
    total += mm;
    console.log(`${p.nombre}: ${mm} mm (${p.estrella ?? 'cualquiera'})`);
  }
  console.log(`Total: ${total} mm`);
}

informe(
  [
    { nombre: 'ocular', medida: 4, estrella: 'Rigel' },
    { nombre: 'biela', medida: '12 mm' },
    { nombre: 'resorte', medida: '3.5', estrella: 'Vega' },
  ],
  (n) => n * 2,
);
```

#### Al superarla
Sin un solo `any` donde esconderse, el Camaleón se queda quieto, gris, y se desarma en un montón de piezas de vidrio, cada una con su medida grabada. Astrea las junta con cuidado. —Ahora sí sirven —dice, y le da a Rigel la **Escama del Camaleón**: una escama de vidrio que ya no cambia de color.

#### Imagen
- Un autómata de latón con forma de camaleón desarmándose en un montón de piezas de vidrio grises, en el piso de un taller steampunk.
- Rigel (chico flaco con pecas, pelo castaño revuelto, antiparras de latón, chaleco marrón) sostiene una escama de vidrio en la mano.
- Astrea (lechuza grande con anteojos de latón y chaleco azul) junta las piezas; Gheco festeja sobre una de ellas.
