# CURSO

```meta
slug: javascript
titulo: JavaScript: La Feria de las Luces
lenguaje: javascript
nivel: desde_cero
descripcion_corta: JavaScript desde cero: la lengua del navegador, de la consola a páginas que reaccionan, pedidos a un servidor y juegos en canvas.
precio_raiz: 10
dias_abono: 30
destacado: si
proximamente: no
publicado: si
micromisiones_completan: si
```

### Descripción

Aprendé **JavaScript desde cero**. No hace falta saber programar: cada tema se explica antes de usarse. Es el lenguaje que corre en todos los navegadores. Con él una página **reacciona**: a un click, a una tecla o a la respuesta de un servidor. También se hacen juegos que corren en cualquier compu, sin instalar nada.

En la Feria de las Luces **nada pasa hasta que algo pasa**: un farol se prende cuando alguien pasa por abajo y un títere baila cuando suena la música. Esa es la lengua de la Feria: **reaccionar**.

Cada tema es un **nodo** del árbol. En cada uno leés la explicación, probás el ejemplo y resolvés las **micro-misiones**, que se comprueban solas. JavaScript corre acá mismo, en tu navegador, dentro de una **caja**:
- no tiene internet ni ve tu sesión;
- el reloj, las cookies, el almacenamiento y el servidor (el **Puerto de Elefa**) son de mentira;
- debajo del editor hay un **tablero** donde ves todo eso.

Las micro-misiones más difíciles te dan **fichas de la Feria** para abrir el siguiente nodo. Cada rama termina con un **jefe**, que junta todo lo que aprendiste.

> Qué hace falta: nada para empezar. Para tus propios proyectos, un navegador (Chrome, Firefox o Edge) y un editor de texto. **Node.js** es opcional: sirve para correr JavaScript desde la terminal, en Windows y en Linux.

### Temario

- Primeros programas: la consola, valores, variables y template literals
- Tipos y la coerción del Goblin: `==` contra `===`, `NaN`, `undefined` y `null`
- Decisiones, `??` y `?.`, bucles, `for…of` y `for…in`
- Arreglos con `map`, `filter` y `reduce`; objetos, desestructuración y spread
- Funciones: flecha, `this`, parámetros rest y closures
- La página (el DOM): seleccionar, crear y cambiar elementos
- Eventos: clicks, teclado, formularios y delegación; JSON y `localStorage`
- Clases, campos privados, herencia, polimorfismo y módulos
- Lo asincrónico: temporizadores, promesas, `async`/`await` y `fetch` contra un servidor
- Errores propios, iteradores y generadores
- Canvas: el bucle del juego, el teclado, las colisiones, las oleadas y un juego completo

# DICCIONARIO

| clave | singular | plural | género | descripción | historia | ámbito |
|---|---|---|---|---|---|---|
| coin.course | ficha | fichas | f | La moneda de la Feria: la ficha de bronce de los puestos de juegos. Se gana superando las micro-misiones que vienen de una misión y abre los nodos del curso. | | curso |
| mentor.name | Lumina | | f | La Reina de las Luciérnagas: la que prende cada farol de la Feria. | Lumina es una luciérnaga enorme, del tamaño de una persona, con alas de vidrio y una luz amarilla en el pecho. Prende cada farol de la Feria de las Luces, la feria nocturna que nunca cierra, y lleva siempre un farolito que no se apaga nunca. Habla poco y despacio, y espera: sabe que **nada pasa hasta que algo pasa**. | curso |
| world.region | Feria de las Luces | | f | La región del mundo cuya lengua arcana es JavaScript. | | curso |
| story.course_intro | Bienvenida a la Feria | | f | | Nima era la mejor arquera del Valle de la Serpiente: le acertaba a todo lo que estaba quieto. Una noche vio **luces que se movían solas** cruzando el cielo hacia el norte, más allá de las Forjas. Tomó su arco, la soga, la brújula y un pan, y las siguió. En el borde de las Forjas encontró un **carrusel abandonado**; cuando se subió, el carrusel giró y la dejó en la **Feria de las Luces**, en {mundo}: farolitos, calesitas, fuegos artificiales y títeres de luz.<br><br>Soy {mentor}, la Reina de las Luciérnagas. Acá hablamos **JavaScript**: la lengua de lo que reacciona. Nima tiene buena puntería, pero en la Feria los blancos se mueven, aparecen y desaparecen, y la flecha tiene que salir **en el momento justo**. Cada tema que domine le prende un farol nuevo; las micro-misiones más difíciles le dan fichas para abrir el siguiente. | curso |
| story.branch_completed | ¡Avenida encendida! | | f | | {mentor} abre las alas y todos los faroles de la avenida se prenden a la vez, uno detrás de otro, como una ola. —Esta parte de la Feria ya reacciona sola. —Nima guarda el arco, y por primera vez no tiene apuro. | curso |
| story.course_completed | ¡Dominaste la lengua de la Feria! | | f | | Nima tensa el **Arco del Vitral** y suelta la última flecha de luz. En el balcón del Vidriero, el vitral del portal **se mueve por primera vez**: los vidrios giran, se acomodan y dibujan una imagen. {mentor} se queda mirándola mucho rato. —Llegaste tirando antes de que el blanco apareciera. Te vas sabiendo esperar sin quedarte quieta. —Esa noche, Nima le escribe por fin a Sila, y esta vez espera la respuesta. | curso |
| story.portal_piece | Lo que mostró el vitral | | f | La pieza del misterio del portal que se lee al terminar este curso (Mis Crónicas). | Cuando el vitral se movió, no mostró el Mundo del Código: mostró **otro lugar**, un cielo lleno de estrellas atadas con hilos de luz, cada una en su figura. Abajo, en un rincón, una firma chiquita en vidrio de colores: la del Vidriero. Nima la copió en su libreta antes de que la imagen se borrara. | curso |
| beast.slime | slime | slimes | m | Nace de los errores de sintaxis: `SyntaxError`, y no se ejecuta nada. | Los slimes brotan de las llaves sin cerrar, los paréntesis de más, las comillas perdidas y las comas que sobran. JavaScript los ve antes de ejecutar y avisa con `SyntaxError` y la línea. Son débiles, pero hasta que no los eliminás el programa no arranca. | curso |
| beast.goblin | goblin | goblins | m | Nace de los tipos que se mezclan: la coerción, `"2" + 2`, `==` contra `===`, `NaN`. | Los goblins de la Feria son los más tramposos del mundo: JavaScript convierte tipos sin avisar. `"2" + 2` da `"22"`, `"2" * 2` da `4`, `[] + {}` da `"[object Object]"` y `NaN` no es igual ni a sí mismo. Se los vence comparando con `===` y convirtiendo a propósito, con `Number()` y `String()`. | curso |
| beast.skeleton | esqueleto | esqueletos | m | Nace de lo que no existe: `ReferenceError`, `undefined`, `x is not a function`. | Los esqueletos son nombres sin cuerpo: una variable mal escrita (`ReferenceError: fichaz is not defined`), una propiedad que no está y vale `undefined`, una función que en realidad no es una función. En JavaScript las mayúsculas cuentan: `nombre` no es `Nombre`. | curso |
| beast.orc | orco | orcos | m | Nace de los límites: posiciones que no están en el arreglo, elementos que no están en la página (`null`). | Los orcos atacan donde terminan las cosas: el índice 10 de un arreglo de 10 (da `undefined`, sin avisar), un `querySelector` que no encontró nada y devolvió `null`. El problema aparece después, lejos de donde nació. | curso |
| beast.ogre | ogro | ogros | m | Nace de los errores de lógica: el programa corre, pero hace otra cosa. | El ogro es el más traicionero: no hay ningún error rojo y el resultado está mal. Sus trucos favoritos en la Feria son el `this` perdido en una función, el `if` que siempre da verdadero porque tiene un `=` en vez de `===` y el `var` que se comparte entre todas las vueltas de un bucle. | curso |
| beast.troll | troll | trolls | m | Nace del tiempo: promesas que nadie espera, respuestas que llegan en otro orden, `undefined` de lo que todavía no llegó. | El troll vive en lo asincrónico. Usa el resultado de un `fetch` antes de que llegue, se olvida de un `await`, deja una promesa rechazada sin `catch` y mezcla respuestas que llegan en cualquier orden. Solo lo vence quien aprende a esperar sin quedarse quieto. | curso |
| beast.dragon | dragón | dragones | m | Guardián de los jefes: un programa grande hecho de piezas chicas. | Un dragón no se vence de un golpe. Se lo divide en funciones, eventos y promesas; se vence cada pieza y recién entonces cae. | curso |

## R00-N01 · Clase 0 · Hola, JavaScript

```meta
tipo: raiz
criatura: slime
temas: prog.entorno, prog.salida
```

### Crónica

Una noche, desde la orilla del río del Valle, Nima ve **luces que se mueven solas** cruzando el cielo hacia el norte. Ella le acierta a todo lo que está quieto, pero esas luces no se quedan quietas nunca. Toma el arco, la soga, la brújula y un pan, y las sigue: cruza las Forjas, donde Tizón la ve pasar preguntando por las luces, y en el borde, entre chimeneas apagadas, encuentra un **carrusel abandonado**. Se sube a un caballito de madera. El carrusel gira solo, cada vez más rápido… y la deja en otro lugar.

Música de organito, olor a pan con miel, farolitos de colores colgados de todas partes: la **Feria de las Luces**. Pero los faroles de la entrada están apagados, y el cartel dice *Cerrado*.

Nima ve un blanco de paja en un puesto de tiro y tira, rápido, como siempre. La flecha se clava en la madera vacía: el blanco **todavía no había aparecido**. Aparece un segundo después, se ríe y se esconde.

—Acá no alcanza con apuntar —dice una voz suave. Es una luciérnaga enorme, del tamaño de una persona, con alas de vidrio y una luz amarilla en el pecho—. Soy {mentor}. En la Feria **nada pasa hasta que algo pasa**. Para que algo pase, hay que decirlo en nuestra lengua: JavaScript. Empecemos por lo más simple: saludar a la Feria.

### Objetivos

- Saber qué es JavaScript y dónde corre: en el navegador, en la caja de la plataforma y en Node.
- Mostrar texto y números con `console.log`.
- Escribir comentarios.
- Reconocer un error de sintaxis (`SyntaxError`) y leer su línea.
- Ver por primera vez las dos cosas que hacen especial a JavaScript: cambiar una página y **reaccionar** (a un click o al paso del tiempo).

### Antes de empezar

Nada: este es el primer nodo. Solo necesitás una compu y ganas.

### Explicación

#### Qué es JavaScript
JavaScript es **el lenguaje de los navegadores**. Todas las páginas que reaccionan (un botón que abre un menú, un mapa que se mueve, un juego en el navegador) lo usan. Es un lenguaje **interpretado**: escribís el programa en texto y el navegador lo lee y lo ejecuta de arriba hacia abajo, sin compilar aparte.

No tiene nada que ver con Java, salvo el nombre (fue una movida de marketing de 1995).

#### Dónde corre
- **Acá, en la plataforma:** cada editor tiene el botón **Ejecutar**. Tu código corre en tu navegador, dentro de una **caja**: no tiene internet, no ve tu sesión y todo lo que toca (el reloj, las cookies, el almacenamiento, el servidor) es de mentira. Debajo del editor está la **Salida** y el **Tablero**, donde ves lo que guarda y lo que pide.
- **En cualquier navegador:** apretá **F12** (o *Ctrl + Mayús + J*) y elegí la pestaña **Consola**. Ahí podés escribir JavaScript y verlo andar. Es lo mismo en Windows y en Linux.
- **En la terminal, con Node.js** (opcional, para más adelante):
  - **Windows:** bajá el instalador LTS de *nodejs.org* y dejá todo como viene.
  - **Linux (Ubuntu, Debian):** `sudo apt install nodejs`.
  - Después, en una terminal: `node -v` tiene que responder la versión (por ejemplo `v20.18.0`), y `node hola.js` ejecuta un archivo.

#### Tu primer programa
```javascript
console.log('¡Hola, Feria!');
```
`console.log(…)` **muestra** lo que le pasás entre paréntesis. El texto va entre comillas: simples (`'…'`), dobles (`"…"`) o invertidas (`` `…` ``), las tres sirven. Al final de cada instrucción va un punto y coma `;` (JavaScript casi siempre lo adivina si falta, pero conviene ponerlo).

#### Mostrar varias cosas
```javascript
console.log('Fichas:', 3 + 4);   // Fichas: 7
console.log(10 / 4);             // 2.5
```
Con comas, `console.log` muestra varios valores separados por un espacio. Los números van **sin** comillas y se pueden hacer cuentas: `+`, `-`, `*`, `/`. El decimal se escribe con **punto**: `2.5`.

#### Comentarios
```javascript
// Esto es un comentario de una línea: JavaScript no lo ejecuta.
/* Y esto, uno
   de varias líneas. */
```
Sirven para explicar el código… y para «apagar» una línea sin borrarla.

#### Cuando algo sale mal
Si falta una comilla, una llave o un paréntesis, el programa **no arranca**: aparece un `SyntaxError` (un slime) con la línea donde JavaScript se dio cuenta. Mirá esa línea **y la anterior**. En la plataforma, la línea con problemas queda marcada en el editor.

#### Nada pasa hasta que algo pasa
Lo especial de JavaScript es que **reacciona**. Dos ejemplos que vas a ver a fondo más adelante:
- `setTimeout(() => console.log('¡Ya!'), 2000);` muestra *¡Ya!* **dentro de 2 segundos**, y mientras tanto el programa sigue con lo que viene abajo.
- `boton.addEventListener('click', …)` hace algo **cuando** alguien toca un botón.

En la caja, el reloj es de la Feria: 2 segundos pasan en un instante, pero el orden es el de verdad.

> **Si venís de otro lenguaje.** No hay `main`: el programa corre de arriba abajo. Las variables se declaran con `let` y `const` (lo ves en el próximo nodo) y no llevan tipo. El `+` también une textos, y ahí empiezan las trampas del Goblin.

### Código de ejemplo

```javascript
// Clase 0 de la Feria: mostrar texto y números con console.log.
console.log('=== Feria de las Luces ===');
console.log('Cartel de la entrada:', 'Cerrado');
console.log('Faroles apagados:', 12);
console.log('Fichas para la calesita:', 2 * 3);

/* El blanco del puesto de tiro aparece dentro de 1 segundo.
   Mientras tanto, el programa sigue. */
setTimeout(() => console.log('¡Apareció el blanco!'), 1000);
console.log('Nima espera con el arco tenso...');
```

### Salida esperada

```
=== Feria de las Luces ===
Cartel de la entrada: Cerrado
Faroles apagados: 12
Fichas para la calesita: 6
Nima espera con el arco tenso...
¡Apareció el blanco!
```

### ¿Para qué sirve?

`console.log` es la herramienta más usada de quien programa en JavaScript: para ver qué vale algo, si una parte del código se ejecutó y en qué orden pasan las cosas. Y el orden importa: en la web casi todo llega **después** (un click, una respuesta del servidor, el próximo cuadro de una animación).

### Errores habituales

**Slime: comillas sin cerrar.**
```
SyntaxError: Unterminated string constant
```
Toda comilla que abre un texto tiene que cerrarse, y con la **misma** comilla: `'hola"` no sirve.

**Slime: paréntesis sin cerrar.**
```
SyntaxError: Unexpected token
```
Contá los paréntesis: cada `(` necesita su `)`.

**Esqueleto: una mayúscula de más.** `Console.log('hola')` da `ReferenceError: Console is not defined`. JavaScript distingue mayúsculas: es `console`, todo en minúscula.

**Goblin: número entre comillas.** `console.log('3' + 4)` muestra `34`, no `7`: con un texto, el `+` **pega** en vez de sumar.

### Micro-misión R00-N01-P1 · El primer farol

```meta
lugar: La entrada de la Feria
personajes: Nima, Gheco, Lumina
carta: Mostrar texto | console.log('texto'); · el texto va entre comillas · cada instrucción termina con ;
recompensa: xp 10, oro 10
```

#### Escena
Nima baja del carrusel. Sobre su hombro se enciende un gecko de luz con antiparras: **Gheco**.
—Lumina dice que la Feria entiende JavaScript —le susurra—. Si la saludás bien, se prende el primer farol.

#### Gheco sugiere
En JavaScript, para mostrar algo en la **consola** (el recuadro donde aparecen los mensajes del programa, la Salida) se usa:

```js
console.log('Hola');
```

Muestra **Hola**. `console.log` es una **función**: una orden con nombre que hace un trabajo, y lo que querés mostrar va entre sus paréntesis. El texto va entre comillas: las comillas no se ven, solo marcan dónde empieza y dónde termina. La línea termina con `;`.

Tocá **Ejecutar** (o Ctrl+Enter): JavaScript corre acá mismo, en tu navegador.

#### Desafío
Completá la instrucción para que Nima salude a la Feria.

#### Código inicial
```javascript
___('¡Hola, Feria!');
```

#### Salida esperada
```
¡Hola, Feria!
```

#### Solución
```javascript
console.log('¡Hola, Feria!');
```

#### Al superarla
Sobre la entrada, un farolito de papel amarillo se prende solo, tiembla y se queda encendido. Lumina inclina la cabeza: —Así empieza todo.

#### Imagen
- La entrada de una feria nocturna con un arco de madera lleno de farolitos de papel apagados y uno solo encendido, amarillo.
- Nima (muchacha de 17, alta y atlética, piel morena, ojos ámbar, pelo negro largo en una trenza alta atada con un hilo amarillo, chaqueta corta de cuero negro cerrada hasta el cuello con costuras amarillas que brillan, guante de arquera, botas altas con luz amarilla en la suela, arco de madera verde y carcaj en la espalda) mira el farol encendido.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre su hombro.

### Micro-misión R00-N01-P2 · Un slime en el carrusel

```meta
lugar: El carrusel abandonado
personajes: Nima, Gheco
criatura: slime
carta: Error de sintaxis | SyntaxError · el programa no arranca · el mensaje dice la línea · comillas y paréntesis siempre de a pares
recompensa: xp 10, oro 10
```

#### Escena
En el caballito de madera donde llegó Nima hay algo verde y blando: un **slime**, una gota de baba que se alimenta de las comillas que nadie cierra. Gheco señala el mensaje que dejó en el editor: `SyntaxError`.

#### Gheco sugiere
Si algo está mal escrito, JavaScript no ejecuta y muestra un error con el **número de línea** donde se dio cuenta.

Un error muy común: un texto que no se cierra. Toda comilla que abre un texto tiene que cerrarse con **la misma** comilla: `'hola'` o `"hola"`, pero no `'hola"`.

#### Desafío
Arreglá el programa para que ande.

#### Código inicial
```javascript
console.log('Nima llegó a la Feria);
```

#### Salida esperada
```
Nima llegó a la Feria
```

#### Solución
```javascript
console.log('Nima llegó a la Feria');
```

#### Al superarla
El slime se escurre por las tablas del carrusel y desaparece. El caballito de madera, limpio, brilla un poco.

#### Imagen
- Un carrusel viejo de madera con caballitos despintados, de noche, iluminado por la luz amarilla de la feria al fondo.
- Nima (trenza negra alta con hilo amarillo, chaqueta de cuero negra con costuras amarillas, arco verde) mira con asco un slime verde chiquito sobre un caballito.
- Gheco (gecko de luz cian con antiparras) apunta al slime con su colita.

### Micro-misión R00-N01-P3 · Las cuentas del puesto

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco
carta: Números | 3 + 4 · 2 * 5 · 10 / 4 da 2.5 · console.log('Texto:', valor) muestra los dos
recompensa: xp 10, oro 10
```

#### Escena
El dueño del puesto de tiro duerme sobre el mostrador. En una pizarra dice: *3 tiros por ronda · 2 rondas*. Nima quiere saber cuántos tiros son y cuánto cuestan, si cada tiro vale 2 fichas.

#### Gheco sugiere
Los números van **sin** comillas, y JavaScript hace las cuentas: `console.log(3 * 2)` muestra `6`. Con comillas, `'3 * 2'` sería un texto y se mostraría tal cual.

Con una coma, `console.log` muestra varias cosas juntas, separadas por un espacio:

```js
console.log('Tiros:', 3 * 2);   // Tiros: 6
```

#### Desafío
Reemplazá los `___` por las cuentas: los tiros son 3 por ronda y 2 rondas; las fichas, 2 por tiro.

#### Código inicial
```javascript
console.log('Tiros:', ___);
console.log('Fichas:', ___);
```

#### Salida esperada
```
Tiros: 6
Fichas: 12
```

#### Solución
```javascript
console.log('Tiros:', 3 * 2);
console.log('Fichas:', 3 * 2 * 2);
```

#### Al superarla
El dueño abre un ojo, mira las cuentas y le alcanza a Nima un puñado de flechas de punta redonda. —Doce fichas. Pero la primera ronda va de regalo.

#### Imagen
- Un puesto de tiro al blanco de feria de noche, con blancos de paja pintados, flechas de punta redonda y una pizarra con rayas (sin letras ni números).
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra con costuras amarillas) cuenta con los dedos frente al mostrador.
- Gheco sentado sobre la pizarra.

### Micro-misión R00-N01-P4 · Notas en el carcaj

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco
carta: Comentarios | // una línea · /* varias líneas */ · JavaScript no los ejecuta · sirven para apagar una línea
recompensa: xp 10, oro 10
```

#### Escena
Nima anota todo en papelitos que guarda en el carcaj. Uno dice algo que ya no sirve: *el blanco está quieto*. En la Feria, eso es mentira.

#### Gheco sugiere
Un **comentario** es una nota para las personas que leen el código. JavaScript lo saltea: no se ejecuta.

Todo lo que va después de `//`, hasta el final de la línea, es comentario:

```js
// esto es una nota
console.log('esto sí se muestra');
```

#### Desafío
«Apagá» la línea que dice que el blanco está quieto, sin borrarla, para que el programa muestre solo las otras dos.

#### Código inicial
```javascript
console.log('El blanco aparece y desaparece');
console.log('El blanco está quieto');
console.log('Hay que tirar en el momento justo');
```

#### Salida esperada
```
El blanco aparece y desaparece
Hay que tirar en el momento justo
```

#### Solución
```javascript
console.log('El blanco aparece y desaparece');
// console.log('El blanco está quieto');
console.log('Hay que tirar en el momento justo');
```

#### Al superarla
Nima tacha el papelito viejo y lo guarda igual. —Para acordarme de que me equivoqué —dice.

#### Imagen
- Primer plano de un carcaj de cuero con flechas y papelitos enrollados atados con hilo amarillo, a la luz de un farol.
- Las manos de Nima (guante de arquera en la derecha, brazal de cuero en la izquierda) sacan un papelito.
- Gheco asomado al borde del carcaj.

### Micro-misión R00-N01-P5 · La flecha que se adelanta

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Lumina
carta: setTimeout | setTimeout(() => console.log('…'), 2000) · se ejecuta dentro de 2000 ms · mientras tanto, el programa sigue
recompensa: xp 15, monedas 4
```

#### Escena
Nima tira otra vez, y otra vez la flecha llega antes que el blanco. Lumina se posa en el mostrador.
—Tu flecha sale apenas la pensás. El blanco aparece dentro de dos segundos. Decile a tu flecha que **espere**.

#### Gheco sugiere
`setTimeout` deja una orden **para más tarde**:

```js
setTimeout(() => console.log('¡Ya!'), 2500);
```

Muestra `¡Ya!` dentro de 2500 **milisegundos** (milésimas de segundo: 2500 son 2,5 segundos). Lo que va antes de la coma, `() => …`, es la orden que espera.

Mirá el orden de la salida: lo que está dentro de un `setTimeout` sale **después**, aunque esté escrito antes. El resto del programa no se queda esperando.

#### Desafío
Hacé que *¡Suelta la flecha!* salga **después** de que aparezca el blanco: metela en un `setTimeout` de 2500 ms, igual que el blanco.

#### Código inicial
```javascript
console.log('Nima tensa el arco...');
setTimeout(() => console.log('¡Aparece el blanco!'), 2000);
console.log('¡Suelta la flecha!');
```

#### Salida esperada
```
Nima tensa el arco...
¡Aparece el blanco!
¡Suelta la flecha!
```

#### Solución
```javascript
console.log('Nima tensa el arco...');
setTimeout(() => console.log('¡Aparece el blanco!'), 2000);
setTimeout(() => console.log('¡Suelta la flecha!'), 2500);
```

#### Al superarla
El blanco aparece, se ríe… y la flecha le da justo en el centro. Por primera vez desde que llegó, Nima se ríe fuerte. —En el momento justo —dice Lumina.

#### Imagen
- Un blanco de paja redondo con cara pintada de payaso, saliendo de una trampilla en un puesto de feria, con una flecha clavada en el centro.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra con costuras amarillas, arco verde) acaba de soltar la cuerda y sonríe.
- Lumina (luciérnaga enorme, del tamaño de una persona, alas de vidrio, luz amarilla en el pecho, farolito en una pata) mira desde el mostrador.

### Micro-misión R00-N01-P6 · El cartel de la entrada

```meta
lugar: La entrada de la Feria
personajes: Nima, Gheco, Lumina
carta: Cambiar la página | document.querySelector('#id') busca un elemento · .textContent = '…' cambia su texto
recompensa: xp 15, monedas 3
```

#### Escena
Volviendo a la entrada, el cartel sigue diciendo *Cerrado*. Lumina sacude las alas.
—La Feria es una página, y JavaScript la puede cambiar. Ese cartel tiene un nombre: `cartel`.

#### Gheco sugiere
Arriba de la Salida está **la página**: el HTML donde corre tu código. Cada parte de la página es un **elemento** (un título, un botón, un párrafo).

```js
document.querySelector('#cartel').textContent = 'Abierto';
```

- `document.querySelector('#cartel')` busca el elemento cuyo `id` es `cartel` (el `#` quiere decir «id»);
- `.textContent = '…'` le cambia el texto.

#### Desafío
Cambiá el texto del cartel por `Abierto`.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; text-align: center; padding-top: 40px; }
  h1 { display: inline-block; border: 4px solid #ffd400; border-radius: 12px; padding: 12px 32px; }
</style>
<h1 id="cartel">Cerrado</h1>
```

#### Estado
```
#cartel
```

#### Código inicial
```javascript
const cartel = document.querySelector('#cartel');
cartel.textContent = '___';
```

#### Salida esperada
```
── Estado ──
#cartel: Abierto
```

#### Solución
```javascript
const cartel = document.querySelector('#cartel');
cartel.textContent = 'Abierto';
```

#### Al superarla
Las letras del cartel se apagan y se vuelven a prender, distintas: *Abierto*. Del otro lado del arco, la música del organito suena más fuerte.

#### Imagen
- Un cartel de madera colgado en el arco de entrada de una feria nocturna, con el borde de foquitos amarillos, sin letras legibles.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra con costuras amarillas) mira el cartel desde abajo.
- Lumina vuela al lado del cartel con su farolito.

### Micro-misión R00-N01-P7 · Nada pasa hasta que algo pasa

```meta
lugar: La avenida de los faroles
personajes: Nima, Gheco, Lumina
carta: Reaccionar | boton.addEventListener('click', () => { … }) · lo de adentro se ejecuta CUANDO tocan el botón
recompensa: xp 15, monedas 3
```

#### Escena
La avenida principal está a oscuras. Al lado del primer farol hay una palanca de bronce.
—Los faroles de la Feria no se prenden solos —dice Lumina—. Esperan. Cuando alguien toca la palanca, reaccionan.

#### Gheco sugiere
Un programa de página no hace todo de una vez: deja cosas **esperando** a que pase algo, como un click. Eso es un **evento**.

```js
boton.addEventListener('click', () => {
    // esto corre recién cuando hacen click
});
```

Lo que está entre las llaves no se ejecuta ahora: se ejecuta cada vez que alguien hace click en el botón. Adentro, `farol.classList.add('prendido')` le pone al farol la clase que lo enciende.

Después de ejecutar, ¡tocá el botón en la página!

#### Desafío
Completá el código para que, al tocar **Prender**, el farol se prenda (que tenga la clase `prendido`) y el cartel diga `Farol prendido`.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; text-align: center; padding-top: 24px; }
  .farol { width: 60px; height: 60px; margin: 16px auto; border-radius: 50%; background: #333; transition: background .4s, box-shadow .4s; }
  .farol.prendido { background: #ffd400; box-shadow: 0 0 30px #ffd400; }
  button { font-size: 18px; padding: 8px 20px; }
</style>
<p id="cartel">La avenida está a oscuras</p>
<div class="farol"></div>
<button id="palanca">Prender</button>
```

#### Eventos
```
click #palanca
```

#### Estado
```
.farol @class
#cartel
```

#### Código inicial
```javascript
const farol = document.querySelector('.farol');
const cartel = document.querySelector('#cartel');
const palanca = document.querySelector('#palanca');

palanca.addEventListener('click', () => {
  // ¿Qué pasa cuando tocan la palanca?

});
```

#### Salida esperada
```
── Estado ──
.farol @class: farol prendido
#cartel: Farol prendido
```

#### Solución
```javascript
const farol = document.querySelector('.farol');
const cartel = document.querySelector('#cartel');
const palanca = document.querySelector('#palanca');

palanca.addEventListener('click', () => {
  farol.classList.add('prendido');
  cartel.textContent = 'Farol prendido';
});
```

#### Al superarla
El primer farol de la avenida se prende… y enseguida el siguiente, y el siguiente, como una ola de luz que corre hasta el fondo de la Feria. Al final, en lo más oscuro, se ve un taller con las ventanas rotas. —El taller del Vidriero —dice Lumina—. Pero eso es para más adelante.

#### Imagen
- Una avenida de feria nocturna con faroles de vidrio que se van encendiendo en fila, de cerca hacia lo lejos, y al fondo un taller oscuro con ventanas rotas.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra con costuras amarillas, arco verde en la espalda) tira de una palanca de bronce.
- Lumina (luciérnaga enorme con alas de vidrio y luz amarilla en el pecho) sobrevuela la fila de faroles; Gheco en el hombro de Nima.
