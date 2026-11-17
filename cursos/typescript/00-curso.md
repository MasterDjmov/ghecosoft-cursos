# CURSO

```meta
slug: typescript
titulo: TypeScript: El Mirador de las Constelaciones
lenguaje: typescript
nivel: intermedio
descripcion_corta: TypeScript: JavaScript con tipos que se revisan antes de ejecutar. De las primeras medidas a un juego entero tipado.
precio_raiz: 10
dias_abono: 30
destacado: no
proximamente: si
publicado: no
micromisiones_completan: si
```

### Descripción

Aprendé **TypeScript**: es JavaScript con **tipos**. Antes de ejecutar, un programa llamado **compilador** revisa que cada dato tenga la forma que dijiste. Si algo no encaja, te avisa en qué línea y por qué, **antes** de que el programa se rompa delante de alguien. Lo usan casi todos los proyectos grandes de la web.

Conviene saber **JavaScript** antes, por ejemplo con el curso de la Feria de las Luces, pero no es obligatorio. Cada tema se explica antes de usarse.

En el Mirador de las Constelaciones, un observatorio de latón y vapor en la cima de la montaña, **cada pieza lleva grabada su medida antes de montarse**. Si una pieza no encaja en su ranura, el mecanismo se traba antes de girar. Esa es la lengua del Mirador: **medir antes de armar**.

Cada tema es un **nodo** del árbol. En cada uno leés la explicación, probás el ejemplo y resolvés las **micro-misiones**, que se comprueban solas. TypeScript corre acá mismo, en tu navegador:
- primero, el **compilador** revisa los tipos y te explica cada error en castellano;
- si todo encaja, el programa corre en la misma **caja** que JavaScript, sin internet, con su reloj, su almacenamiento y su servidor de mentira.

Las micro-misiones más difíciles te dan **estrellas de latón** para abrir el siguiente nodo. Cada rama termina con un **jefe**, que junta todo lo que aprendiste.

> Qué hace falta: nada para empezar. Para tus propios proyectos, **Node.js** y TypeScript (`npm install -D typescript`), en Windows y en Linux. Se explica en la Clase 0.

### Temario

- Qué es TypeScript, el compilador, la inferencia y cómo leer un error
- Tipos básicos, arreglos y tuplas; `any`, `unknown`, `void` y `never`
- La forma de los datos: `interface` y `type`, propiedades opcionales y `readonly`
- Funciones tipadas: parámetros, retorno, opcionales, rest, tipos de función y sobrecarga
- Clases tipadas, `private` contra `#`, `abstract`, `implements`, enums, `as const` y genéricos
- Uniones, narrowing, uniones discriminadas y exhaustividad con `never`
- Utility types (`Partial`, `Pick`, `Omit`, `Record`) y módulos con `import type`
- Errores tipados, `Promise<T>`, el DOM tipado, `strictNullChecks`, decoradores y `tsconfig.json`
- El mismo juego en JavaScript y en TypeScript: *Junta las Gemas* tipado

# DICCIONARIO

| clave | singular | plural | género | descripción | historia | ámbito |
|---|---|---|---|---|---|---|
| coin.course | estrella de latón | estrellas de latón | f | La moneda del Mirador: una ficha de latón estampada con una estrella, la que da el Gran Planisferio cuando una pieza encaja. Se gana superando las micro-misiones que vienen de una misión y abre los nodos del curso. | | curso |
| mentor.name | Astrea | | f | La Lechuza Cartógrafa: le pone nombre y figura a cada estrella del Mirador. | Astrea es una lechuza grande, más alta que una persona, de plumas gris azuladas. Usa anteojos de varias lentes de latón que se acomodan con una ruedita, un chaleco de cartógrafa con mapas enrollados en los bolsillos y un compás de bronce con el que mide las constelaciones. Habla poco y despacio, y repite siempre lo mismo: **nada brilla sin su forma**. | curso |
| world.region | Mirador de las Constelaciones | | m | La región del mundo cuya lengua arcana es TypeScript. | | curso |
| story.course_intro | Bienvenido al Mirador | | m | | Cuando el vitral del balcón se movió por primera vez, en la Ciudadela de los Artífices todos los engranajes dieron **un solo golpe al mismo tiempo**. Tesla, el Artífice Mayor, entendió enseguida: **el Gran Planisferio del Mirador quería volver a andar**. Lo habían construido él y el Vidriero hace muchos años. Le dio un plano a su aprendiz, **Rigel**, y lo mandó montaña arriba, en un ascensor de vapor abandonado.<br><br>Rigel llegó a {mundo}: cúpulas de latón, telescopios que se mueven con engranajes y caños que silban vapor. Soy {mentor}, la Lechuza Cartógrafa. Acá hablamos **TypeScript**: la lengua de lo que se mide antes de armarse. Rigel tiene manos rápidas, pero arma todo a ojo, y en el Mirador una pieza mal medida traba el cielo entero. Cada tema que domine pone a girar una parte del Planisferio; las micro-misiones más difíciles le dan estrellas de latón para abrir el siguiente. | curso |
| story.branch_completed | ¡La sala gira! | | f | | {mentor} acomoda sus anteojos con la ruedita y mira la sala: todas las piezas encajan y el mecanismo gira sin un solo chirrido. —Medido dos veces, armado una —dice Rigel, y por primera vez no le explota nada. | curso |
| story.course_completed | ¡Dominaste la lengua del Mirador! | | f | | Rigel ajusta la última pieza con el **Calibre del Vidriero** y suelta la palanca. El **Gran Planisferio** arranca: las constelaciones giran, se acomodan y, en el balcón del portal, el vitral **se queda quieto en la figura correcta**, por primera vez. {mentor} se saca los anteojos. —Llegaste armando a ojo. Te vas midiendo antes de tocar una sola pieza. | curso |
| story.portal_piece | El plano del portal | | m | La pieza del misterio del portal que se lee al terminar este curso (Mis Crónicas). | En el Atlas del Vidriero, Rigel encontró **el plano entero del portal**, con todas sus figuras medidas y numeradas. Todas menos una: en su lugar hay un hueco con la forma exacta de la pieza que falta y una nota con la letra del Vidriero, que dice que esa pieza no se mide: se construye en otro lado. | curso |
| beast.slime | slime | slimes | m | Nace de los errores de escritura: una llave sin cerrar, un `:` de más, una anotación mal escrita. | Los slimes del Mirador son de aceite de máquina: se meten entre los engranajes cuando una llave queda sin cerrar o una anotación está mal escrita. El compilador los ve antes que nadie y avisa con la línea. Son débiles, pero hasta que no los limpiás, nada gira. | curso |
| beast.goblin | goblin | goblins | m | Nace de los tipos que no encajan: `TS2322`, un texto donde va un número. | Los goblins del Mirador llevan engranajes en la espalda y quieren meter piezas donde no van: un texto en la ranura de un número, un número donde va un booleano. En JavaScript se salían con la suya; en TypeScript el compilador los frena con `TS2322` antes de que el mecanismo arranque. | curso |
| beast.skeleton | esqueleto | esqueletos | m | Nace de lo que no existe: `TS2339` (la propiedad no está), `TS2304` (el nombre no está). | Los esqueletos del Mirador son de alambre: nombres mal escritos, propiedades que el tipo no tiene, piezas que faltan en un objeto. TypeScript los descubre al compilar, con el nombre exacto de lo que no encontró. | curso |
| beast.orc | orco | orcos | m | Nace de los límites: lo que «capaz que no está», `null` y `undefined` (`TS18048`). | Los orcos atacan donde una pieza podría faltar: el resultado de un `find` que no encontró nada, un elemento que no está en la página, una propiedad opcional. TypeScript obliga a preguntar antes de usar. | curso |
| beast.ogre | ogro | ogros | m | Nace de la lógica y de las reglas: un caso que falta en un `switch`, un `as` que miente, una `const` que se quiere cambiar. | El ogro del Mirador es el que miente con un `as` («confiá en mí, es un número») o se olvida de un caso. TypeScript lo atrapa con `never` y con las reglas de `readonly`, `private` y `abstract`. | curso |
| beast.troll | troll | trolls | m | Nace del tiempo: una `Promise<T>` sin `await`, el tipo de lo que todavía no llegó. | El troll vive en lo asincrónico. Quiere usar una promesa como si ya fuera el valor. TypeScript le pone tipo a lo que va a llegar (`Promise<T>`) y no deja usarlo hasta esperarlo. | curso |
| beast.dragon | dragón | dragones | m | Guardián de los jefes: un modelo grande hecho de tipos chicos. | Un dragón del Mirador es un autómata enorme de latón y vidrio, armado con piezas del Planisferio mal medidas. No se vence de un golpe: se mide pieza por pieza, se tipa cada una y recién entonces cae. | curso |

## R00-N01 · Clase 0 · Hola, TypeScript

```meta
tipo: raiz
criatura: goblin
temas: js.typescript, cal.tipos, prog.salida
```

### Crónica

El ascensor de vapor sube la montaña dando sacudidas, entre nubes y silbidos. Arriba, Rigel ve las cúpulas de latón del **Mirador de las Constelaciones** brillando bajo las estrellas. Lleva en la mano el **Calibre de Aprendiz**, un regalo de Tesla, y en la mochila el plano del **Gran Planisferio**.

Adentro, todo está parado. En el centro, un planetario mecánico del tamaño de una sala: cada estrella es una pieza de vidrio en un brazo de latón. Rigel ve una pieza suelta en el piso, la levanta y la mete a la fuerza en el primer hueco que encuentra. El mecanismo hace *clac*, chilla y escupe vapor por todos lados.

—En el Mirador nada se arma a ojo —dice una voz grave. Es una lechuza enorme, con anteojos de latón de varias lentes—. Soy {mentor}. Acá cada pieza lleva grabada su **medida**, y el Planisferio revisa la medida antes de girar. Si no encaja, se traba antes de romperse. Esa revisión tiene nombre: **TypeScript**. Empecemos por lo más simple.

### Objetivos

- Saber qué es TypeScript: JavaScript con tipos que se revisan **antes** de ejecutar.
- Entender qué hace el **compilador**: revisa los tipos y pasa el código a JavaScript.
- Anotar el tipo de una variable (`: string`, `: number`, `: boolean`) y aprovechar la **inferencia**.
- Leer un error de tipos: la línea, el mensaje y el código (`TS2322`).
- Instalar TypeScript en tu compu, en Windows y en Linux.

### Antes de empezar

- Conviene saber lo básico de JavaScript: `console.log`, variables con `let` y `const`, y template literals (`` `Hola, ${nombre}` ``). Si no lo sabés, la Clase 0 y R01-N01 del curso de JavaScript lo explican.

### Explicación

#### Qué es TypeScript
**TypeScript es JavaScript con tipos.** Escribís el mismo JavaScript de siempre, pero podés decir de qué **tipo** es cada dato:

```typescript
const nombre: string = 'Rigel';   // un texto
let nivel: number = 1;            // un número
let aprendiz: boolean = true;     // verdadero o falso
```

Lo que va después de los dos puntos (`: string`) es la **anotación de tipo**: la medida grabada en la pieza.

#### El compilador revisa antes de ejecutar
El navegador no entiende TypeScript, solo JavaScript. Por eso hay un paso más, el **compilador** (`tsc`):
1. **revisa** que cada dato encaje con su tipo;
2. si todo encaja, **pasa** el código a JavaScript, borrando los tipos;
3. ese JavaScript es el que corre.

```typescript
let nivel: number = 1;
nivel = 'dos';   // ✗ el compilador frena acá
```

En JavaScript, `nivel = 'dos'` se ejecuta sin quejarse y el problema aparece más tarde, lejos de donde nació. En TypeScript **no se ejecuta nada** hasta que lo arregles.

> Los tipos solo existen antes de ejecutar. En el JavaScript que corre no queda ninguno: `const nombre: string = 'Rigel'` pasa a ser `const nombre = 'Rigel'`.

#### Cómo se lee un error
```
Línea 2: El tipo 'string' no se puede asignar al tipo 'number'.
  Goblin: el valor no encaja con el tipo de la variable. (TS2322)
```
- **Línea 2:** dónde lo vio.
- **El mensaje:** qué no encaja (un `string` donde va un `number`).
- **TS2322:** el número del error. Sirve para buscarlo en internet: todos los programadores del mundo lo conocen por ese número.

#### La inferencia: no hace falta anotar todo
Si la variable empieza con un valor, TypeScript **deduce** el tipo solo:

```typescript
let vida = 100;     // TypeScript ya sabe que es number
vida = 'cien';      // ✗ TS2322, igual que si lo hubieras anotado
```

Anotá cuando el tipo no se ve a simple vista; cuando se ve, dejá que TypeScript lo deduzca.

#### Dónde corre
- **Acá, en la plataforma:** cada editor tiene el botón **Ejecutar**. La primera vez baja el compilador (unos segundos); después es instantáneo. Si hay errores de tipos, el programa no corre y te los explica. Si no hay, corre en la **caja**, igual que JavaScript.
- **En tu compu**, con **Node.js** (el mismo de JavaScript):
  - **Windows:** instalá Node LTS desde *nodejs.org*.
  - **Linux (Ubuntu, Debian):** `sudo apt install nodejs npm`.
  - Después, en una carpeta de tu proyecto: `npm install -D typescript` y `npx tsc --init` (crea el archivo de configuración, `tsconfig.json`).
  - `npx tsc` compila todos los `.ts` a `.js`, y `node archivo.js` los ejecuta. Es igual en Windows y en Linux.
- **El modo estricto:** en la plataforma, TypeScript corre siempre en modo **estricto** (`"strict": true`), que es el que recomienda todo el mundo. `tsc --init` también lo deja prendido.

### Código de ejemplo

```typescript
const nombre: string = 'Rigel';
let nivel: number = 1;
const aprendiz: boolean = true;

console.log(`Hola, ${nombre}. Nivel ${nivel}.`);

nivel = nivel + 1;
console.log(`Ahora es nivel ${nivel}.`);

// Inferencia: TypeScript deduce que vueltas es un number.
let vueltas = 3;
vueltas += 2;
console.log(vueltas, typeof vueltas, aprendiz);
```

### Salida esperada

```
Hola, Rigel. Nivel 1.
Ahora es nivel 2.
5 number true
```

### ¿Para qué sirve?

Los errores de tipos (un texto donde va un número, una propiedad mal escrita) son de los más comunes en JavaScript, y aparecen recién cuando alguien usa el programa. TypeScript los encuentra **mientras escribís**. Por eso lo usan casi todos los proyectos grandes de la web.

### Errores habituales

**Goblin: un tipo que no encaja (TS2322).**
```
Línea 2: El tipo 'string' no se puede asignar al tipo 'number'. (TS2322)
```
Revisá qué tipo le diste a la variable y qué le estás guardando. `'5'` (entre comillas) es un texto; `5` es un número.

**Esqueleto: la variable sin valor (TS2454).** `let mana: number;` y después `console.log(mana)` da *La variable 'mana' se usa antes de asignarla* (TS2454). Dale un valor al declararla.

**Slime: la anotación mal escrita.** `let nivel: Number = 1` funciona, pero el tipo es `number`, en minúscula. `let nivel: numero = 1` da `TS2552`: *No se encuentra el nombre "numero". ¿Quería decir "number"?*

### Micro-misión R00-N01-P1 · La primera medida

```meta
lugar: La entrada del Mirador
personajes: Rigel, Gheco, Astrea
carta: Anotar un tipo | const nombre: string = 'Rigel'; · lo de después de : es el tipo · string, number, boolean
recompensa: xp 10, oro 10
```

#### Escena
Junto a la puerta del Mirador hay una placa de latón con un hueco vacío. Sobre el hombro de Rigel se enciende un gecko de luz con antiparras: **Gheco**.
—La placa pide tu nombre —le susurra—, pero con su medida grabada.

#### Gheco sugiere
En TypeScript, después del nombre de la variable van **dos puntos** y el **tipo**:

```ts
const ciudad: string = 'Ciudadela';
```

`string` es el tipo de los **textos**. Otros tipos básicos: `number` (números) y `boolean` (`true` o `false`). Los tipos van en minúscula.

Tocá **Ejecutar**: primero el compilador revisa los tipos y, si encajan, el programa corre.

#### Desafío
Completá el tipo de `aprendiz` para que la placa lo acepte.

#### Pasos
1. Buscá el `___` después de `aprendiz:`.
2. Cambialo por `string`: el nombre es un texto.
3. Tocá **Ejecutar**. Tiene que salir `Bienvenido, Rigel`.

#### Código inicial
```typescript
const aprendiz: ___ = 'Rigel';
console.log(`Bienvenido, ${aprendiz}`);
```

#### Salida esperada
```
Bienvenido, Rigel
```

#### Solución
```typescript
const aprendiz: string = 'Rigel';
console.log(`Bienvenido, ${aprendiz}`);
```

#### Al superarla
La placa se ilumina y la puerta se abre con un silbido de vapor. Astrea, desde una viga, inclina la cabeza: —Así empieza todo.

#### Imagen
- La puerta de un observatorio steampunk de latón con remaches, de noche, y una placa de latón iluminada junto a ella; vapor saliendo de un caño.
- Rigel (chico de 16, flaco, pecas, pelo castaño claro revuelto, antiparras de latón con un lente azul subidas a la frente, camisa azul, chaleco de cuero marrón cerrado, cinturón de herramientas, mochila con un engranaje a la vista) toca la placa.
- Gheco (gecko de luz aguamarina, flaco, con antiparras) sobre su hombro; Astrea (lechuza grande gris azulada con anteojos de latón y chaleco azul) mira desde una viga.

### Micro-misión R00-N01-P2 · El goblin del ascensor

```meta
lugar: El ascensor de vapor
personajes: Rigel, Gheco
criatura: goblin
carta: Error de tipos | TS2322 · el programa no se ejecuta · el mensaje dice la línea y qué no encaja
recompensa: xp 10, oro 10
```

#### Escena
En el tablero del ascensor, un **goblin** con un engranaje en la espalda metió un papelito en la ranura de los pisos. El ascensor no se mueve. Gheco señala el mensaje del compilador: `TS2322`.

#### Gheco sugiere
Si un valor no encaja con el tipo de la variable, el compilador **no deja ejecutar** y muestra la línea y el problema:

```
Línea 2: El tipo 'string' no se puede asignar al tipo 'number'. (TS2322)
```

`'3'` (con comillas) es un texto; `3` (sin comillas) es un número. La variable `piso` es `number`: solo acepta números.

#### Desafío
Ejecutá, leé el error y arreglá la línea para que el ascensor vaya al piso 3.

#### Pasos
1. Tocá **Ejecutar** y leé el error: está en la línea 2.
2. En esa línea, sacale las comillas al `'3'`: queda `piso = 3;`.
3. Tocá **Ejecutar**. Tiene que salir `Piso 3`.

#### Código inicial
```typescript
let piso: number = 1;
piso = '3';
console.log(`Piso ${piso}`);
```

#### Salida esperada
```
Piso 3
```

#### Solución
```typescript
let piso: number = 1;
piso = 3;
console.log(`Piso ${piso}`);
```

#### Al superarla
El ascensor da una sacudida y sube. El goblin sale disparado por la rejilla con su papelito en la mano.

#### Imagen
- El interior de un ascensor de vapor de latón con una rejilla, palancas y un tablero de pisos con números grabados (sin texto legible).
- Rigel (chico flaco con pecas, pelo castaño revuelto, antiparras de latón en la frente, chaleco marrón, camisa azul) tira de una palanca.
- Un goblin chiquito con un engranaje en la espalda escapa por la rejilla; Gheco señala el tablero.

### Micro-misión R00-N01-P3 · La pieza que no entra

```meta
lugar: El Gran Planisferio
personajes: Rigel, Gheco, Astrea
criatura: goblin
carta: El compilador frena | cambiá un número por un texto · el compilador da TS2322 y la línea · no se ejecuta nada
recompensa: xp 10, oro 10
```

#### Escena
Astrea le muestra a Rigel una ranura del Planisferio con la medida grabada: *número*.
—Quiero que lo veas con tus propios ojos. Meté una pieza que no encaje y mirá qué pasa.

#### Gheco sugiere
Esta micro-misión es distinta: **no ejecuta el programa**. Solo revisa los tipos, y lo que se compara son los **errores** del compilador. Para superarla, el código tiene que dar exactamente este error:

```
TS2322 en la línea 2
```

Si el código compila bien, sale `Compila sin errores`.

#### Desafío
Hacé que el compilador frene en la línea 2: guardá en `medida` el **texto** `'15'` en lugar del número `15`.

#### Pasos
1. Buscá la línea 2: `medida = 15;`.
2. Poné el número entre comillas: `medida = '15';`.
3. Tocá **Ejecutar**. Tiene que salir `TS2322 en la línea 2`.

#### Compilador
sí

#### Código inicial
```typescript
let medida: number = 12;
medida = 15;
console.log(medida);
```

#### Salida esperada
```
TS2322 en la línea 2
```

#### Solución
```typescript
let medida: number = 12;
medida = '15';
console.log(medida);
```

#### Al superarla
La pieza no entra, y el Planisferio ni se mueve: ni un chirrido, ni una chispa. —¿Ves? —dice Astrea—. Se trabó **antes** de romperse.

#### Imagen
- Un planetario mecánico gigante de latón en una sala con cúpula, con estrellas de vidrio en brazos articulados; una ranura iluminada con una medida grabada (sin letras).
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón, camisa azul) sostiene una pieza de vidrio que no entra en la ranura.
- Astrea (lechuza grande gris azulada con anteojos de latón de varias lentes y chaleco azul) observa con calma; Gheco en el hombro de Rigel.

### Micro-misión R00-N01-P4 · La medida que se deduce

```meta
lugar: La Sala de las Figuras
personajes: Rigel, Gheco
carta: Inferencia | let vueltas = 3; · TypeScript deduce number · no hace falta anotar si el valor ya lo dice
recompensa: xp 15, monedas 3
```

#### Escena
Rigel cuenta las vueltas que da una rueda dentada. Anotó `vueltas` sin tipo y teme que el compilador se queje.

#### Gheco sugiere
Si la variable empieza con un valor, TypeScript **deduce** el tipo solo. Se llama **inferencia**:

```ts
let vueltas = 3;      // TypeScript sabe que es number
vueltas = vueltas + 1;
```

`typeof` dice de qué tipo es un valor cuando el programa corre: `typeof vueltas` es `'number'`.

#### Desafío
Completá la línea para que `vueltas` sume una vuelta más.

#### Pasos
1. Buscá el `___` después de `vueltas =`.
2. Cambialo por `vueltas + 1`.
3. Tocá **Ejecutar**. Tiene que salir `4 number`.

#### Código inicial
```typescript
let vueltas = 3;
vueltas = ___;
console.log(vueltas, typeof vueltas);
```

#### Salida esperada
```
4 number
```

#### Solución
```typescript
let vueltas = 3;
vueltas = vueltas + 1;
console.log(vueltas, typeof vueltas);
```

#### Al superarla
La rueda dentada da su cuarta vuelta y encaja con un *clic* limpio.

#### Imagen
- Una rueda dentada grande de latón girando en una pared llena de engranajes, con vapor suave.
- Rigel (chico flaco con pecas, pelo castaño revuelto, antiparras de latón, chaleco marrón) cuenta las vueltas con los dedos.
- Gheco sentado en el eje de la rueda.

### Micro-misión R00-N01-P5 · La caldera vacía

```meta
lugar: Las calderas del Mirador
personajes: Rigel, Gheco
criatura: skeleton
carta: Usada antes de asignarla | TS2454 · let x: number; sin valor · dale el valor al declararla
recompensa: xp 15, monedas 3
```

#### Escena
Rigel quiere saber cuánta presión tiene la caldera, pero anotó la variable sin ponerle un valor. Un **esqueleto** de alambre se ríe detrás del manómetro.

#### Gheco sugiere
`let presion: number;` declara la variable con su tipo, pero **sin valor**. Si la usás antes de dárselo, el compilador avisa:

```
La variable 'presion' se usa antes de asignarla. (TS2454)
```

Lo más simple es darle el valor en la misma línea: `let presion: number = 40;`.

#### Desafío
Dale a `presion` el valor `40` al declararla.

#### Pasos
1. Buscá `let presion: number;`.
2. Antes del `;`, agregá ` = 40`: queda `let presion: number = 40;`.
3. Tocá **Ejecutar**. Tiene que salir `Presión: 40`.

#### Código inicial
```typescript
let presion: number;
console.log(`Presión: ${presion}`);
```

#### Salida esperada
```
Presión: 40
```

#### Solución
```typescript
let presion: number = 40;
console.log(`Presión: ${presion}`);
```

#### Al superarla
La aguja del manómetro sube hasta el 40 y la caldera ronronea. El esqueleto se desarma en un montoncito de alambre.

#### Imagen
- Una sala de calderas de cobre con caños, válvulas y un manómetro grande con la aguja subiendo (sin números legibles).
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón, guantes sin dedos) gira una válvula.
- Un esqueleto de alambre chiquito se desarma detrás del manómetro; Gheco lo señala.

### Micro-misión R00-N01-P6 · El ascensor de vapor

```meta
lugar: El ascensor de vapor
personajes: Rigel, Gheco, Astrea
criatura: goblin
carta: Cuentas con tipos | number * number da number · un texto en una cuenta es TS2362 · el tipo de la variable manda
recompensa: xp 15, monedas 4
```

#### Escena
Para bajar a buscar las piezas del Planisferio, Rigel tiene que calcular cuánto tarda el ascensor: 7 pisos, 3 segundos por piso. Pero alguien anotó los pisos como texto, y el compilador no deja hacer la cuenta.

#### Gheco sugiere
Una cuenta como `*` necesita **números** de los dos lados. Si uno es `string`, el compilador frena:

```
La parte izquierda de una operación aritmética debe ser de tipo "any", "number", "bigint" o un tipo de enumeración. (TS2362)
```

Arreglá el **tipo** y el **valor** juntos: `const pisos: number = 7;`.

#### Desafío
Arreglá la línea de `pisos` para que el programa calcule el tiempo.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En la primera línea, cambiá `string` por `number` y `'7'` por `7`: `const pisos: number = 7;`.
3. Tocá **Ejecutar**. Tiene que salir `El ascensor tarda 21 segundos`.

#### Código inicial
```typescript
const pisos: string = '7';
const segundosPorPiso: number = 3;
const total: number = pisos * segundosPorPiso;
console.log(`El ascensor tarda ${total} segundos`);
```

#### Salida esperada
```
El ascensor tarda 21 segundos
```

#### Solución
```typescript
const pisos: number = 7;
const segundosPorPiso: number = 3;
const total: number = pisos * segundosPorPiso;
console.log(`El ascensor tarda ${total} segundos`);
```

#### Al superarla
El ascensor baja exactamente en 21 segundos. Astrea anota algo en un mapa con su compás. —Mediste antes de bajar. Así se trabaja en el Mirador. —Le entrega a Rigel su primera **estrella de latón**.

#### Imagen
- Un ascensor de vapor de latón bajando por la ladera de una montaña de noche, con un cielo lleno de estrellas y las cúpulas del observatorio arriba.
- Rigel (chico flaco con pecas, pelo castaño revuelto, antiparras de latón, chaleco marrón, mochila con engranaje) mira hacia abajo por la rejilla con una ficha de latón con una estrella en la mano.
- Astrea (lechuza grande con anteojos de latón y chaleco azul de cartógrafa) vuela al lado; Gheco en el hombro de Rigel.
