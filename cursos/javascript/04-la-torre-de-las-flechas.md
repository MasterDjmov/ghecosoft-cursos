# RAMA R04 · La Torre de las Flechas: lo asincrónico

```meta
tipo: tronco
posicion: 4
```

## R04-N01 · Lo que pasa después

```meta
tipo: tema
padre: R03-N07
precio: 10
criatura: troll
temas: conc.async
```

### Crónica

En la punta norte de la Feria se levanta la **Torre de las Flechas**: una torre alta y finita, con una galería arriba desde donde salen las **flechas de luz**, los mensajes de la Feria. Las atiende **Saeta**, una arquera mensajera vieja, de pelo blanco atado en un rodete, que lleva cuarenta años soltando flechas que vuelan hasta el Puerto de los Mensajeros y vuelven con la respuesta.

Nima sube los quinientos escalones y le cuenta su problema: ella también mandaba flechas desde el Valle, pero nunca le llegó una respuesta.

—Porque soltabas la flecha y te ibas —le dice Saeta, sin mirarla—. O peor: te quedabas parada esperando, sin hacer nada más. Las dos cosas están mal. Una flecha se suelta, se **sigue con lo demás**, y cuando la respuesta llega, se la atiende.

—En JavaScript se dice **asincrónico** —agrega {mentor}.

### Objetivos

- Entender que JavaScript hace **una cosa por vez**, y que lo que tarda (un temporizador, un pedido) se atiende **después**.
- Predecir el orden de la salida con `setTimeout`, incluso con 0 ms.
- Usar callbacks: funciones que se llaman cuando algo termina.
- Ver por qué los callbacks anidados se vuelven difíciles de leer (y por qué existen las promesas).

### Antes de empezar

- R01-N07 (funciones y callbacks) y R03-N05 (closures).

### Explicación

#### Una cosa por vez
JavaScript tiene **un solo hilo**: ejecuta tu programa de arriba abajo, sin interrupciones. Lo que tiene que esperar (un temporizador, una respuesta del servidor, un click) **no frena** el programa: queda anotado en una fila, y se atiende cuando el programa principal termina y el momento llega.
```javascript
console.log('1. Suelto la flecha');
setTimeout(() => console.log('3. Llegó la respuesta'), 1000);
console.log('2. Sigo con lo mío');
```

#### Hasta con 0
```javascript
setTimeout(() => console.log('después'), 0);
console.log('antes');
```
Muestra `antes` y después `después`: el temporizador va a la fila, aunque sea de 0 ms.

#### Callbacks
```javascript
function mandarFlecha(destino, alLlegar) {
  setTimeout(() => alLlegar(`Respuesta de ${destino}`), 1000);
}
mandarFlecha('el Puerto', (respuesta) => console.log(respuesta));
```

#### La pirámide
Si cada respuesta pide otra flecha, los callbacks quedan uno adentro del otro y el código se corre a la derecha hasta volverse ilegible. Las **promesas** (el próximo nodo) arreglan eso.

> **En la plataforma.** El reloj de la caja es de la Feria: un `setTimeout` de 3 segundos se cumple en un instante, pero en el orden de verdad. En el Tablero ves el reloj y cuántos temporizadores se dispararon.

### Código de ejemplo

```javascript
console.log('Nima suelta la flecha');
setTimeout(() => console.log('(a los 2 s) Llega la respuesta del Puerto'), 2000);
setTimeout(() => console.log('(a los 0 s, pero después) Saeta anota la salida'), 0);
console.log('Nima sigue practicando');

function mandarFlecha(destino, alLlegar) {
  setTimeout(() => alLlegar(`Respuesta de ${destino}`), 1000);
}
mandarFlecha('las Forjas', (respuesta) => console.log('(a los 1 s)', respuesta));
console.log('Fin del programa principal');
```

### Salida esperada

```
Nima suelta la flecha
Nima sigue practicando
Fin del programa principal
(a los 0 s, pero después) Saeta anota la salida
(a los 1 s) Respuesta de las Forjas
(a los 2 s) Llega la respuesta del Puerto
```

### ¿Para qué sirve?

En la web casi todo llega después: la respuesta de un servidor, un archivo que se lee, el click de una persona, el próximo cuadro de un juego. Si el programa se quedara parado esperando, la página se congelaría. Entender el orden de lo asincrónico es la diferencia entre un programa que anda y uno que «a veces» anda.

### Errores habituales

**Troll: usar el resultado antes de que llegue.**
```javascript
let respuesta;
setTimeout(() => (respuesta = 'ok'), 1000);
console.log(respuesta);   // undefined: todavía no llegó
```
Lo que depende de la respuesta va **adentro** del callback (o después de un `await`).

**Troll: esperar con un bucle.** Un `while` que espera a que algo cambie congela todo (y en la caja se corta). Nunca se espera con un bucle.

### Micro-misión R04-N01-P1 · El orden de las flechas

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta
carta: setTimeout | el programa no espera · lo del setTimeout sale después, aunque esté escrito antes
recompensa: xp 10, oro 10
```

#### Escena
Saeta le pide a Nima que anote, en orden, todo lo que pasa en la galería durante un envío. Nima escribe el programa, pero los renglones salen en otro orden del que esperaba.

#### Gheco sugiere
`setTimeout(función, ms)` (el de la Clase 0) **no frena** el programa: anota la función para dentro de tantos milisegundos y el programa sigue con la línea de abajo. Por eso, lo que está afuera de un `setTimeout` sale primero.

Entre varios `setTimeout`, sale primero **el de menos milisegundos**, sin importar en qué orden están escritos:

```js
setTimeout(() => console.log('B'), 2000);
setTimeout(() => console.log('A'), 500);
// sale A y después B
```

La consigna pide no mover las líneas: tocá solo los números.

#### Desafío
Hacé que la salida sea: `Sale la flecha`, `Saeta anota`, `Responden las Forjas`, `Responde el Puerto`.

#### Código inicial
```javascript
console.log('Sale la flecha');
setTimeout(() => console.log('Responde el Puerto'), 1000);
setTimeout(() => console.log('Responden las Forjas'), 3000);
console.log('Saeta anota');
```

#### Salida esperada
```
Sale la flecha
Saeta anota
Responden las Forjas
Responde el Puerto
```

#### Solución
```javascript
console.log('Sale la flecha');
setTimeout(() => console.log('Responde el Puerto'), 3000);
setTimeout(() => console.log('Responden las Forjas'), 1000);
console.log('Saeta anota');
```

#### Al superarla
Saeta mira la libreta de Nima y asiente, apenas. —Sale, se anota, y después llegan. En ese orden. Siempre.

#### Imagen
- La galería abierta en lo alto de una torre finita de feria, de noche, con flechas de luz amarilla saliendo hacia el horizonte.
- Saeta (arquera mensajera vieja, pelo blanco en un rodete, capa gris cerrada, guantes de cuero gastados, carcaj lleno de flechas de luz) mira el horizonte; Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) anota en una libreta; Gheco en su hombro.

### Micro-misión R04-N01-P2 · Cero no es ya

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta
carta: setTimeout(…, 0) | igual va a la fila · sale después de todo el programa principal
recompensa: xp 10, oro 10
```

#### Escena
Bruno subió a la Torre y dice que con 0 milisegundos la flecha sale «ya». Saeta le pide a Nima que le muestre que no.

#### Gheco sugiere
Un `setTimeout` de **0** milisegundos no corre «ya»: corre **apenas termine** todo lo que el programa está haciendo ahora. JavaScript hace una cosa por vez: primero termina el programa entero, de arriba abajo, y recién después atiende lo que quedó anotado para más tarde.

Ejecutá y fijate en qué lugar sale cada mensaje.

#### Desafío
Agregá `console.log('Fin')` al final del programa, y observá: la flecha de 0 sale última igual.

#### Código inicial
```javascript
console.log('Bruno cuenta: 3, 2, 1...');
setTimeout(() => console.log('¡Flecha de 0 ms!'), 0);
console.log('Bruno se da vuelta');
```

#### Salida esperada
```
Bruno cuenta: 3, 2, 1...
Bruno se da vuelta
Fin
¡Flecha de 0 ms!
```

#### Solución
```javascript
console.log('Bruno cuenta: 3, 2, 1...');
setTimeout(() => console.log('¡Flecha de 0 ms!'), 0);
console.log('Bruno se da vuelta');
console.log('Fin');
```

#### Al superarla
—Pero yo puse cero —protesta Bruno. —Y cero es «cuando termines» —dice Saeta—, no «ya».

#### Imagen
- Bruno (chico de 12, gorra al revés, chaleco rojo) con cara de sorpresa en la galería de la torre, mirando una flecha de luz que sale tarde.
- Saeta, de brazos cruzados, con una media sonrisa.

### Micro-misión R04-N01-P3 · El troll de la respuesta

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta
criatura: troll
carta: Usar lo que llega | lo que depende de la respuesta va adentro del callback · afuera, todavía no llegó
recompensa: xp 10, oro 10
```

#### Escena
Un troll se coló en la galería y cambió el código: ahora, apenas sale la flecha, el programa muestra la respuesta… y dice *undefined*.

#### Gheco sugiere
Si una variable se llena adentro de un `setTimeout`, **todavía está vacía** en la línea de abajo: esa línea corre enseguida, y el `setTimeout` mucho después.

```js
let premio;
setTimeout(() => { premio = 'oso'; }, 1000);
console.log(premio);   // undefined: todavía no llegó
```

Lo que usa el dato tiene que ir **adentro** de la función que se ejecuta cuando llega.

#### Desafío
Que se vea `Respuesta: ¡Recibido, Nima!`.

#### Código inicial
```javascript
let respuesta;
setTimeout(() => {
  respuesta = '¡Recibido, Nima!';
}, 2000);
console.log('Respuesta:', respuesta);
```

#### Salida esperada
```
Respuesta: ¡Recibido, Nima!
```

#### Solución
```javascript
let respuesta;
setTimeout(() => {
  respuesta = '¡Recibido, Nima!';
  console.log('Respuesta:', respuesta);
}, 2000);
```

#### Al superarla
La respuesta aparece cuando tiene que aparecer: ni antes ni después. El troll se va gruñendo escaleras abajo (son quinientos escalones: va a tardar).

#### Imagen
- Un troll chiquito y gruñón de feria (sin armas) bajando por una escalera caracol interminable de una torre.
- Arriba, Nima lee un papelito de luz que acaba de llegar; Saeta asiente.

### Micro-misión R04-N01-P4 · La flecha con callback

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta
carta: Callbacks | function mandar(destino, alLlegar) { … alLlegar(respuesta) … } · se le pasa qué hacer cuando llegue
recompensa: xp 10, oro 10
```

#### Escena
Saeta le enseña su técnica: la flecha lleva atada una instrucción de qué hacer cuando vuelva.

#### Gheco sugiere
Un **callback** es una función que le pasás a otra para que **la llame cuando termine**. Así, el que espera dice qué hacer con el resultado:

```js
function cocinar(plato, alTerminar) {
    setTimeout(() => alTerminar(`${plato} listo`), 1000);
}
cocinar('Pochoclo', (aviso) => console.log(aviso));
```

A los 1000 ms, `cocinar` llama a `alTerminar` con el texto, y se muestra `Pochoclo listo`. Fijate en la consigna qué texto tiene que recibir el callback.

#### Desafío
Completá `mandarFlecha`.

#### Código inicial
```javascript
function mandarFlecha(destino, alLlegar) {

}

mandarFlecha('el Puerto', (respuesta) => console.log(respuesta));
console.log('La flecha ya salió');
```

#### Salida esperada
```
La flecha ya salió
Respuesta de el Puerto
```

#### Solución
```javascript
function mandarFlecha(destino, alLlegar) {
  setTimeout(() => alLlegar(`Respuesta de ${destino}`), 1000);
}

mandarFlecha('el Puerto', (respuesta) => console.log(respuesta));
console.log('La flecha ya salió');
```

#### Al superarla
La flecha sale con un hilito de luz atado. Al volver, el hilito sabe solo qué hacer: lleva la respuesta a la mano de Nima.

#### Imagen
- Una flecha de luz amarilla con un hilito brillante atado, volviendo hacia la galería de la torre.
- Nima estira la mano para recibirla; Saeta mira con aprobación.

### Micro-misión R04-N01-P5 · La pirámide de flechas

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta
criatura: troll
carta: Callbacks anidados | cada paso adentro del anterior · funciona, pero se corre a la derecha (por eso existen las promesas)
recompensa: xp 15, monedas 5
```

#### Escena
Saeta tiene que mandar tres flechas en cadena: primero al Valle, cuando vuelva al Puerto, y cuando vuelva a las Forjas. Cada una sale recién cuando llega la anterior.

#### Gheco sugiere
Para hacer cosas **en orden** con callbacks, la segunda se pide **adentro** del callback de la primera, y la tercera adentro del de la segunda:

```js
cocinar('Pan', (r1) => {
    console.log(r1);
    cocinar('Torta', (r2) => {
        console.log(r2);
    });
});
```

Cada nivel se corre un poco a la derecha, y con muchos se forma una **pirámide** difícil de leer. Lo que va al final (`Las tres volvieron`) tiene que estar en el nivel de más adentro.

#### Desafío
Mandá las tres en cadena para que salgan, en orden, las tres respuestas y al final `Las tres volvieron`.

#### Código inicial
```javascript
function mandarFlecha(destino, alLlegar) {
  setTimeout(() => alLlegar(`Respuesta del ${destino}`), 1000);
}

mandarFlecha('Valle', (r1) => {
  console.log(r1);
  // mandá al Puerto, y adentro, a las Forjas

});
```

#### Salida esperada
```
Respuesta del Valle
Respuesta del Puerto
Respuesta del lado de las Forjas
Las tres volvieron
```

#### Solución
```javascript
function mandarFlecha(destino, alLlegar) {
  setTimeout(() => alLlegar(`Respuesta del ${destino}`), 1000);
}

mandarFlecha('Valle', (r1) => {
  console.log(r1);
  mandarFlecha('Puerto', (r2) => {
    console.log(r2);
    mandarFlecha('lado de las Forjas', (r3) => {
      console.log(r3);
      console.log('Las tres volvieron');
    });
  });
});
```

#### Al superarla
Las tres flechas vuelven en orden, pero el papel donde Nima anotó el plan quedó en forma de escalera. Saeta se ríe: —Así lo hacíamos antes. Mañana te muestro las promesas.

#### Imagen
- Una hoja de papel con anotaciones escalonadas hacia la derecha como una pirámide (sin texto legible), sobre la baranda de la galería de la torre.
- Tres flechas de luz llegando una detrás de otra; Saeta y Nima las miran.

### Micro-misión R04-N01-P6 · La galería no se congela

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta, Lumina
carta: No bloquear | mientras la flecha viaja, la página sigue respondiendo · lo largo se hace con temporizadores, nunca con un while
recompensa: xp 15, monedas 5
```

#### Escena
Lumina quiere ver una cosa: si mientras la flecha viaja (3 segundos) la galería sigue atendiendo. Pone un botón para tocar la campana, y quiere que la campana suene aunque la flecha esté en camino.

#### Gheco sugiere
Mientras un `setTimeout` espera, la página **sigue andando**: los otros botones responden, se puede escribir, nada se congela. Esa es la gracia de no frenar el programa.

En el evento del botón, primero cambiá el cartel y después dejá anotado, con `setTimeout`, el cambio de cuando vuelve la flecha. La campana ya tiene su propio evento: no la toques.

#### Desafío
Completá el evento de *Soltar*. (La comprobación suelta, toca la campana a los 1 s y espera hasta los 3 s.)

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; text-align: center; }
  button { font-size: 18px; margin: 4px; padding: 6px 14px; }
  #cartel { font-size: 22px; color: #ffd400; }
</style>
<button id="soltar">Soltar flecha</button> <button id="campana">🔔 Campana</button>
<p id="cartel">Galería tranquila</p>
<ul id="campanadas"></ul>
```

#### Eventos
```
click #soltar
esperar 1000
click #campana
esperar 2000
```

#### Estado
```
#cartel
#campanadas li
```

#### Código inicial
```javascript
const cartel = document.querySelector('#cartel');

document.querySelector('#campana').addEventListener('click', () => {
  const li = document.createElement('li');
  li.textContent = `Campanada a los ${performance.now()} ms (cartel: ${cartel.textContent})`;
  document.querySelector('#campanadas').append(li);
});

document.querySelector('#soltar').addEventListener('click', () => {

});
```

#### Salida esperada
```
── Estado ──
#cartel: Flecha de vuelta
#campanadas li: Campanada a los 1000 ms (cartel: Flecha en camino)
```

#### Solución
```javascript
const cartel = document.querySelector('#cartel');

document.querySelector('#campana').addEventListener('click', () => {
  const li = document.createElement('li');
  li.textContent = `Campanada a los ${performance.now()} ms (cartel: ${cartel.textContent})`;
  document.querySelector('#campanadas').append(li);
});

document.querySelector('#soltar').addEventListener('click', () => {
  cartel.textContent = 'Flecha en camino';
  setTimeout(() => {
    cartel.textContent = 'Flecha de vuelta';
  }, 3000);
});
```

#### Al superarla
La campana suena con la flecha todavía en el aire, y la flecha vuelve igual, a su hora. Lumina sonríe. —Esperar sin quedarse quieta —le dice a Nima—. Eso es lo que viniste a aprender.

#### Imagen
- La galería de la torre de noche con una campana de bronce sonando y una flecha de luz lejos, en el cielo.
- Nima toca la campana mirando la flecha; Lumina (luciérnaga enorme, alas de vidrio) y Saeta miran.

## R04-N02 · Promesas: la flecha que promete volver

```meta
tipo: tema
padre: R04-N01
precio: 10
criatura: troll
temas: conc.async, js.fetch
```

### Crónica

A la mañana siguiente, Saeta le muestra a Nima una flecha distinta: tiene la punta envuelta en un papel sellado con un dibujo de luz. —Esta es una flecha **prometida** —le dice—. Cuando la soltás, te da algo en la mano: una promesa. Todavía no sabés qué va a traer, pero sabés que **algo** va a traer: o la respuesta, o la noticia de que se perdió.

### Objetivos

- Entender qué es una promesa: un valor que va a llegar (o un error que va a llegar).
- Usar `.then()`, `.catch()` y `.finally()`.
- Encadenar `then` para hacer pasos en orden, sin pirámide.
- Crear promesas con `new Promise((resolve, reject) => …)`.
- Conocer `Promise.resolve` y `Promise.reject`.

### Antes de empezar

- R04-N01: lo asincrónico y los callbacks.

### Explicación

#### Una promesa
Una promesa está en uno de tres estados: **pendiente**, **cumplida** (con un valor) o **rechazada** (con un error).
```javascript
const flecha = new Promise((resolve, reject) => {
  setTimeout(() => resolve('¡Llegué!'), 1000);   // se cumple
  // o: reject(new Error('Se perdió la flecha'))  // se rechaza
});
```

#### then, catch, finally
```javascript
flecha
  .then((respuesta) => console.log(respuesta))   // si se cumplió
  .catch((error) => console.log(error.message))  // si se rechazó
  .finally(() => console.log('Saeta anota'));    // siempre, al final
```

#### Encadenar
Lo que devuelve un `then` pasa al siguiente. Si devuelve **otra promesa**, el siguiente espera a que se cumpla:
```javascript
mandar('Valle')
  .then((r1) => { console.log(r1); return mandar('Puerto'); })
  .then((r2) => { console.log(r2); return mandar('Forjas'); })
  .then((r3) => console.log(r3))
  .catch((error) => console.log('Una se perdió:', error.message));
```
Un solo `catch` al final ataja el error de **cualquier** paso.

#### Atajos
```javascript
Promise.resolve(5);                  // una promesa ya cumplida con 5
Promise.reject(new Error('No'));     // una ya rechazada
```

### Código de ejemplo

```javascript
function mandar(destino, ms) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (destino === 'la Niebla') reject(new Error(`La flecha a ${destino} se perdió`));
      else resolve(`Respuesta de ${destino}`);
    }, ms);
  });
}

const promesa = mandar('el Puerto', 1000);
console.log('¿Qué es?', promesa instanceof Promise);

promesa
  .then((r) => {
    console.log(r);
    return mandar('la Niebla', 500);
  })
  .then((r) => console.log('Esto no se ve:', r))
  .catch((error) => console.log('Error:', error.message))
  .finally(() => console.log('Saeta anota el viaje'));
```

### Salida esperada

```
¿Qué es? true
Respuesta de el Puerto
Error: La flecha a la Niebla se perdió
Saeta anota el viaje
```

### ¿Para qué sirve?

Todo lo asincrónico moderno devuelve promesas: `fetch`, leer archivos, la cámara, la ubicación, las bases de datos del navegador. Saber encadenarlas y atajar sus errores es saber trabajar con la web.

### Errores habituales

**Troll: olvidarse el `return` en un `then`.** El siguiente `then` no espera la flecha nueva: recibe `undefined`.

**Troll: la promesa rechazada sin `catch`.** En la caja aparece como *Una promesa falló y nadie la atajó*. Poné siempre un `catch` al final de la cadena.

**Ogro: rechazar con un texto.** `reject('se perdió')` funciona, pero lo correcto es `reject(new Error('se perdió'))`: así trae el mensaje y la línea.

### Micro-misión R04-N02-P1 · La flecha prometida

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta
carta: then | promesa.then((valor) => …) · corre cuando la promesa se cumple
recompensa: xp 10, oro 10
```

#### Escena
Saeta le da a Nima una flecha prometida. Al soltarla, a Nima le queda en la mano el papel sellado: la promesa.

#### Gheco sugiere
Una **promesa** (`Promise`) es un objeto que representa un resultado que **todavía no llegó**: «te prometo un valor para más tarde». Con `.then` decís qué hacer **cuando llegue**:

```js
pedido.then((comida) => console.log('Llegó:', comida));
```

La función del `then` recibe el valor que trae la promesa. Es como el callback, pero se escribe afuera, después.

#### Desafío
Usá `.then` para mostrar la respuesta.

#### Código inicial
```javascript
const flecha = new Promise((resolve) => {
  setTimeout(() => resolve('El Puerto dice: ¡Hola, Feria!'), 1500);
});

console.log('La flecha salió');
// mostrá la respuesta cuando llegue

```

#### Salida esperada
```
La flecha salió
El Puerto dice: ¡Hola, Feria!
```

#### Solución
```javascript
const flecha = new Promise((resolve) => {
  setTimeout(() => resolve('El Puerto dice: ¡Hola, Feria!'), 1500);
});

console.log('La flecha salió');
flecha.then((respuesta) => console.log(respuesta));
```

#### Al superarla
El papel sellado se ilumina en la mano de Nima y aparece el mensaje del Puerto, letra por letra.

#### Imagen
- Un papelito sellado con un dibujo de luz amarilla brillando en la palma enguantada de Nima.
- Atrás, en el cielo, una flecha de luz volviendo hacia la torre.

### Micro-misión R04-N02-P2 · La flecha que se pierde

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta
carta: catch y finally | .catch((error) => …) si se rechazó · .finally(() => …) siempre
recompensa: xp 10, oro 10
```

#### Escena
Hay niebla. Saeta suelta una flecha que se pierde: la promesa se **rechaza**. Hay que avisar del error, y anotar el viaje igual.

#### Gheco sugiere
Una promesa puede salir **bien** (se *cumple*) o **mal** (se *rechaza*, con un error). Se le pueden encadenar tres cosas:

- `.then(…)` corre si salió bien;
- `.catch((error) => …)` corre si salió mal; `error.message` es el texto del error;
- `.finally(() => …)` corre **siempre**, salga bien o mal.

```js
pedido
    .then((c) => console.log(c))
    .catch((error) => console.log('Falló:', error.message))
    .finally(() => console.log('Mesa limpia'));
```

#### Desafío
Completá la cadena.

#### Código inicial
```javascript
const flecha = new Promise((resolve, reject) => {
  setTimeout(() => reject(new Error('niebla en el camino')), 1000);
});

flecha
  .then((r) => console.log('Llegó:', r))

```

#### Salida esperada
```
Se perdió: niebla en el camino
Saeta anota el viaje
```

#### Solución
```javascript
const flecha = new Promise((resolve, reject) => {
  setTimeout(() => reject(new Error('niebla en el camino')), 1000);
});

flecha
  .then((r) => console.log('Llegó:', r))
  .catch((error) => console.log('Se perdió:', error.message))
  .finally(() => console.log('Saeta anota el viaje'));
```

#### Al superarla
—Perder una flecha no es lo peor —dice Saeta—. Lo peor es no enterarse.

#### Imagen
- Una niebla espesa alrededor de la torre de flechas, con una flecha de luz apagándose en la bruma.
- Saeta anota en un libro grande de cuero; Nima mira la niebla.

### Micro-misión R04-N02-P3 · Hacer promesas

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta
carta: new Promise | new Promise((resolve, reject) => { … resolve(valor) … reject(error) … }) · una función que la devuelve
recompensa: xp 10, oro 10
```

#### Escena
Saeta le pide a Nima que haga su propia función de mandar flechas: si el destino es `'la Niebla'`, la flecha se pierde; si no, vuelve a los 1000 ms.

#### Gheco sugiere
Para **crear** una promesa se usa `new Promise`, que recibe una función con dos botones: `resolve` (cumplir, con el valor) y `reject` (rechazar, con un error):

```js
function tirarDado() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (Math.random() < 0.1) reject(new Error('Se cayó de la mesa'));
            else resolve(4);
        }, 500);
    });
}
```

La función **devuelve** la promesa con `return`: así quien la llama puede ponerle `.then`.

#### Desafío
Completá `mandar`.

#### Código inicial
```javascript
function mandar(destino) {

}

mandar('el Puerto').then((r) => console.log(r));
mandar('la Niebla').catch((e) => console.log(e.message));
```

#### Salida esperada
```
Respuesta de el Puerto
La flecha a la Niebla se perdió
```

#### Solución
```javascript
function mandar(destino) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (destino === 'la Niebla') reject(new Error(`La flecha a ${destino} se perdió`));
      else resolve(`Respuesta de ${destino}`);
    }, 1000);
  });
}

mandar('el Puerto').then((r) => console.log(r));
mandar('la Niebla').catch((e) => console.log(e.message));
```

#### Al superarla
Nima suelta su primera flecha prometida, hecha por ella. Vuelve. La de la niebla no, pero ella se entera.

#### Imagen
- Nima soltando una flecha de luz desde la galería de la torre, con el arco tenso, concentrada.
- Saeta detrás, con las manos en la espalda, aprobando.

### Micro-misión R04-N02-P4 · Sin pirámide

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta
carta: Encadenar | .then((r) => { …; return otraPromesa; }).then(…) · cada paso espera al anterior · return es clave
recompensa: xp 10, oro 10
```

#### Escena
Las mismas tres flechas en cadena de ayer (Valle, Puerto, Forjas), pero ahora con promesas: en fila, sin escalera.

#### Gheco sugiere
Si adentro de un `then` **devolvés** otra promesa, el `then` siguiente espera a esa. Así se hacen cosas en orden **sin pirámide**: todo queda a la misma altura.

```js
cocinar('Pan')
    .then((r1) => {
        console.log(r1);
        return cocinar('Torta');
    })
    .then((r2) => console.log(r2));
```

Lo del final va en un último `then`.

#### Desafío
Encadená las tres para que salgan en orden y al final `Las tres volvieron`.

#### Código inicial
```javascript
function mandar(destino) {
  return new Promise((resolve) => setTimeout(() => resolve(`Respuesta de ${destino}`), 1000));
}

mandar('el Valle')
  .then((r1) => {
    console.log(r1);

  })

```

#### Salida esperada
```
Respuesta de el Valle
Respuesta de el Puerto
Respuesta de las Forjas
Las tres volvieron
```

#### Solución
```javascript
function mandar(destino) {
  return new Promise((resolve) => setTimeout(() => resolve(`Respuesta de ${destino}`), 1000));
}

mandar('el Valle')
  .then((r1) => {
    console.log(r1);
    return mandar('el Puerto');
  })
  .then((r2) => {
    console.log(r2);
    return mandar('las Forjas');
  })
  .then((r3) => {
    console.log(r3);
    console.log('Las tres volvieron');
  });
```

#### Al superarla
El papel del plan, esta vez, queda derecho: un paso debajo del otro. Saeta lo cuelga en la pared, al lado del de la pirámide. —Antes y después —dice.

#### Imagen
- Dos papeles colgados en una pared de piedra de la torre: uno escalonado como pirámide y otro con renglones derechos (sin texto legible).
- Saeta los señala con la punta de una flecha; Nima sonríe.

### Micro-misión R04-N02-P5 · El troll del return

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco
criatura: troll
carta: Sin return no espera | si un then no devuelve la promesa, el siguiente sigue sin esperarla
recompensa: xp 15, monedas 5
```

#### Escena
Un troll borró un `return`. Ahora la segunda respuesta llega **después** del mensaje final, y el siguiente `then` recibe `undefined`.

#### Gheco sugiere
Si un `then` llama a otra promesa pero **no la devuelve** con `return`, el `then` siguiente no la espera: arranca enseguida, con `undefined`.

Revisá cada `then` de la cadena: el que pide la próxima tiene que tener `return` adelante.

#### Desafío
Arreglalo para que salga: `Respuesta de el Valle`, `Respuesta de el Puerto`, `Fin del viaje`.

#### Código inicial
```javascript
function mandar(destino) {
  return new Promise((resolve) => setTimeout(() => resolve(`Respuesta de ${destino}`), 1000));
}

mandar('el Valle')
  .then((r1) => {
    console.log(r1);
    mandar('el Puerto');
  })
  .then((r2) => {
    console.log(r2);
    console.log('Fin del viaje');
  });
```

#### Salida esperada
```
Respuesta de el Valle
Respuesta de el Puerto
Fin del viaje
```

#### Solución
```javascript
function mandar(destino) {
  return new Promise((resolve) => setTimeout(() => resolve(`Respuesta de ${destino}`), 1000));
}

mandar('el Valle')
  .then((r1) => {
    console.log(r1);
    return mandar('el Puerto');
  })
  .then((r2) => {
    console.log(r2);
    console.log('Fin del viaje');
  });
```

#### Al superarla
Las dos flechas vuelven en orden. El troll se esconde en el carcaj vacío de Saeta, que lo sacude para afuera sin mirarlo.

#### Imagen
- Un carcaj de cuero gastado sacudido boca abajo, con un troll chiquito y gruñón (sin armas) cayendo de adentro.
- Saeta (pelo blanco en rodete, capa gris) sacude el carcaj con indiferencia; Nima se ríe.

### Micro-misión R04-N02-P6 · La flecha de la Reina

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta, Lumina
carta: Todo junto | una función que devuelve promesas · then encadenados · un solo catch · finally
recompensa: xp 15, monedas 5
```

#### Escena
Lumina tiene que mandar una invitación al Puerto, a las Forjas y a la Niebla (aunque sabe que la de la Niebla se pierde). Quiere un solo `catch` y que al final, pase lo que pase, se apague el farol de la galería.

#### Gheco sugiere
En una cadena de `then`, si cualquier paso sale mal, se **saltan** todos los `then` que siguen y se va directo al `catch`. Por eso alcanza con **un solo `catch`** al final para toda la cadena.

Encadená los pasos con `return` (como en R04-N02-P4), y al final el `catch` y el `finally`. Fijate en la consigna qué tiene que mostrar cada uno.

#### Desafío
Completá la cadena.

#### Código inicial
```javascript
function mandar(destino) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (destino === 'la Niebla') reject(new Error(`La invitación a ${destino} se perdió`));
      else resolve(`${destino} acepta la invitación`);
    }, 1000);
  });
}

mandar('el Puerto')

```

#### Salida esperada
```
el Puerto acepta la invitación
las Forjas acepta la invitación
Error: La invitación a la Niebla se perdió
Se apaga el farol de la galería
```

#### Solución
```javascript
function mandar(destino) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (destino === 'la Niebla') reject(new Error(`La invitación a ${destino} se perdió`));
      else resolve(`${destino} acepta la invitación`);
    }, 1000);
  });
}

mandar('el Puerto')
  .then((r) => {
    console.log(r);
    return mandar('las Forjas');
  })
  .then((r) => {
    console.log(r);
    return mandar('la Niebla');
  })
  .then((r) => console.log(r))
  .catch((error) => console.log('Error:', error.message))
  .finally(() => console.log('Se apaga el farol de la galería'));
```

#### Al superarla
Dos invitaciones aceptadas, una perdida en la niebla. Lumina no parece sorprendida. —A la Niebla nunca le llega nada —dice—. Algún día vamos a saber por qué.

#### Imagen
- La galería de la torre con el farol apagándose y, a lo lejos, un banco de niebla espesa y oscura en el horizonte.
- Lumina (luciérnaga enorme, alas de vidrio) mira la niebla; Nima y Saeta a su lado.

## R04-N03 · async y await

```meta
tipo: tema
padre: R04-N02
precio: 10
criatura: troll
temas: conc.async
```

### Crónica

Saeta le da a Nima su arco viejo de mensajera: un arco con una muesca en el medio, donde se apoya la mano para **esperar** la flecha de vuelta sin soltar el arco. —Con este no tenés que escribir *then, then, then* —le dice—. Esperás, y cuando llega, seguís. Como si fuera derecho.

### Objetivos

- Escribir funciones `async` y esperar promesas con `await`.
- Atajar errores con `try`/`catch` (y `finally`) en código asincrónico.
- Saber que una función `async` siempre devuelve una promesa.
- Usar `await` en el nivel principal del programa (en módulos).
- No esperar de más: lo que no depende de lo anterior puede salir junto.

### Antes de empezar

- R04-N02: promesas.

### Explicación

#### async y await
```javascript
async function viaje() {
  const r1 = await mandar('el Valle');    // espera, sin congelar la página
  console.log(r1);
  const r2 = await mandar('el Puerto');
  console.log(r2);
}
viaje();
```
Se lee de arriba abajo, como si fuera normal, pero **no frena** al resto: mientras espera, la página sigue.

#### Errores
```javascript
async function viaje() {
  try {
    const r = await mandar('la Niebla');
    console.log(r);
  } catch (error) {
    console.log('Se perdió:', error.message);
  } finally {
    console.log('Saeta anota');
  }
}
```

#### Siempre devuelve una promesa
```javascript
async function doble(n) { return n * 2; }
doble(4);                       // una Promise, no 8
doble(4).then(console.log);     // 8
const x = await doble(4);       // 8 (en el nivel principal de un módulo, o adentro de otra async)
```

> **En la plataforma.** Tu código corre como un módulo: podés usar `await` directamente, afuera de una función.

#### No esperar de más
```javascript
const a = await mandar('el Valle');    // 1 s
const b = await mandar('el Puerto');   // 1 s más: 2 s en total
```
Si no dependen una de la otra, soltalas juntas y esperá las dos (lo vas a ver en *Varias flechas a la vez*).

### Código de ejemplo

```javascript
function mandar(destino) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (destino === 'la Niebla') reject(new Error(`se perdió la flecha a ${destino}`));
      else resolve(`Respuesta de ${destino}`);
    }, 1000);
  });
}

async function viaje(destinos) {
  for (const destino of destinos) {
    try {
      const respuesta = await mandar(destino);
      console.log(`${performance.now()} ms · ${respuesta}`);
    } catch (error) {
      console.log(`${performance.now()} ms · Error: ${error.message}`);
    }
  }
  return 'viaje terminado';
}

const resultado = viaje(['el Valle', 'la Niebla', 'el Puerto']);
console.log('¿Qué devolvió?', resultado instanceof Promise);
console.log(await resultado);
```

### Salida esperada

```
¿Qué devolvió? true
1000 ms · Respuesta de el Valle
2000 ms · Error: se perdió la flecha a la Niebla
3000 ms · Respuesta de el Puerto
viaje terminado
```

### ¿Para qué sirve?

Es la forma en que se escribe el código asincrónico hoy: pedidos al servidor, bases de datos, archivos. Se lee como un programa común, y los errores se atajan con el mismo `try`/`catch` de siempre.

### Errores habituales

**Troll: olvidarse el `await`.** `const r = mandar('el Valle'); console.log(r);` muestra `Promise { … }`, no la respuesta.

**Slime: `await` en una función que no es `async`.** `SyntaxError: await is only valid in async functions…`. Agregá `async` a la función.

**Troll: el `catch` que falta.** Un `await` de una promesa rechazada sin `try` tira el error; si nadie lo ataja, se pierde.

**Troll: `await` adentro de `forEach`.** `forEach` no espera: usá `for…of`.

### Micro-misión R04-N03-P1 · Esperar sin then

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta
carta: await | const r = await promesa · solo adentro de async (o en el nivel principal de un módulo)
recompensa: xp 10, oro 10
```

#### Escena
Nima prueba el arco de la muesca: suelta, espera y sigue, sin escribir `then`.

#### Gheco sugiere
`await` es otra forma de esperar una promesa, más fácil de leer que `then`: **frena esa parte del programa** hasta que la promesa llegue, y da su valor:

```js
const comida = await cocinar('Pan');
console.log(comida);
```

Se lee de arriba abajo, como si no hubiera espera. En esta caja se puede usar `await` suelto, en el programa principal.

#### Desafío
Esperá la respuesta con `await` y mostrala.

#### Código inicial
```javascript
function mandar(destino) {
  return new Promise((resolve) => setTimeout(() => resolve(`Respuesta de ${destino}`), 1000));
}

console.log('Suelto');
const respuesta = ___;
console.log(respuesta);
console.log('Sigo');
```

#### Salida esperada
```
Suelto
Respuesta de el Puerto
Sigo
```

#### Solución
```javascript
function mandar(destino) {
  return new Promise((resolve) => setTimeout(() => resolve(`Respuesta de ${destino}`), 1000));
}

console.log('Suelto');
const respuesta = await mandar('el Puerto');
console.log(respuesta);
console.log('Sigo');
```

#### Al superarla
La mano de Nima descansa en la muesca del arco. La flecha vuelve y ella, sin moverse, ya sabe qué hacer después.

#### Imagen
- Un arco viejo de mensajera con una muesca de madera pulida en el medio, en las manos de Nima.
- Saeta mira de cerca cómo lo sostiene; atrás, una flecha de luz volviendo.

### Micro-misión R04-N03-P2 · La función que espera

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta
carta: async function | async function f() { const r = await …; } · se llama como cualquier función
recompensa: xp 10, oro 10
```

#### Escena
Saeta quiere una función `viaje()` que mande dos flechas en orden y muestre las dos respuestas.

#### Gheco sugiere
Adentro de una función, `await` solo se puede usar si la función está marcada como **`async`** (asíncrona):

```js
async function almuerzo() {
    const entrada = await cocinar('Sopa');
    console.log(entrada);
    const plato = await cocinar('Fideos');
    console.log(plato);
}
almuerzo();
```

Cada `await` espera al anterior: salen en orden. Después hay que **llamarla**, como cualquier función.

#### Desafío
Escribí `viaje`.

#### Código inicial
```javascript
function mandar(destino) {
  return new Promise((resolve) => setTimeout(() => resolve(`Respuesta de ${destino}`), 1000));
}

// escribí viaje acá


viaje();
```

#### Salida esperada
```
Respuesta de el Valle
Respuesta de el Puerto
```

#### Solución
```javascript
function mandar(destino) {
  return new Promise((resolve) => setTimeout(() => resolve(`Respuesta de ${destino}`), 1000));
}

async function viaje() {
  const r1 = await mandar('el Valle');
  console.log(r1);
  const r2 = await mandar('el Puerto');
  console.log(r2);
}

viaje();
```

#### Al superarla
Dos flechas, una detrás de la otra, sin pirámide ni cadena de `then`. Saeta lo lee en voz alta, como si fuera un cuento.

#### Imagen
- Saeta leyendo en voz alta un papel con renglones derechos (sin texto legible) en la galería de la torre.
- Nima escucha; Gheco cabecea de sueño.

### Micro-misión R04-N03-P3 · try y catch en las alturas

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta
carta: try/catch con await | try { await … } catch (e) { … } finally { … } · como en el código común
recompensa: xp 10, oro 10
```

#### Escena
Hay niebla otra vez. La flecha a la Niebla se pierde, y el programa explota con una promesa rechazada que nadie atajó.

#### Gheco sugiere
Con `await`, una promesa rechazada se comporta como un error común: corta el programa. Se ataja con el `try`/`catch` de R02, y el `finally` corre siempre:

```js
try {
    const comida = await cocinar('Suflé');
    console.log(comida);
} catch (error) {
    console.log('Se quemó:', error.message);
} finally {
    console.log('Apagar el horno');
}
```

#### Desafío
Atajá el error.

#### Código inicial
```javascript
function mandar(destino) {
  return new Promise((resolve, reject) => {
    setTimeout(() => reject(new Error(`niebla rumbo a ${destino}`)), 1000);
  });
}

const respuesta = await mandar('la Niebla');
console.log(respuesta);
```

#### Salida esperada
```
Se perdió: niebla rumbo a la Niebla
Saeta anota
```

#### Solución
```javascript
function mandar(destino) {
  return new Promise((resolve, reject) => {
    setTimeout(() => reject(new Error(`niebla rumbo a ${destino}`)), 1000);
  });
}

try {
  const respuesta = await mandar('la Niebla');
  console.log(respuesta);
} catch (error) {
  console.log('Se perdió:', error.message);
} finally {
  console.log('Saeta anota');
}
```

#### Al superarla
El error ya no explota: queda anotado prolijamente en el libro de Saeta, con fecha y hora.

#### Imagen
- El libro grande de cuero de Saeta abierto sobre un atril, con una página de anotaciones (sin texto legible) y una pluma.
- Saeta escribe; afuera, niebla.

### Micro-misión R04-N03-P4 · El troll del await que falta

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco
criatura: troll
carta: Sin await | sin await tenés la promesa, no la respuesta · Promise { … } en la salida es la pista
recompensa: xp 10, oro 10
```

#### Escena
Un troll sacó un `await`. Ahora el programa muestra `Promise { … }` en vez de la respuesta del Puerto.

#### Gheco sugiere
Sin `await`, la variable no guarda el **resultado**: guarda **la promesa**, que todavía no tiene nada. Por eso se ve `Promise { … }` en vez de la respuesta.

Buscá la línea que llama a la función que devuelve una promesa y fijate qué le falta adelante.

#### Desafío
Que se vea la respuesta.

#### Código inicial
```javascript
function mandar(destino) {
  return new Promise((resolve) => setTimeout(() => resolve(`Respuesta de ${destino}`), 1000));
}

async function viaje() {
  const respuesta = mandar('el Puerto');
  console.log(respuesta);
}

viaje();
```

#### Salida esperada
```
Respuesta de el Puerto
```

#### Solución
```javascript
function mandar(destino) {
  return new Promise((resolve) => setTimeout(() => resolve(`Respuesta de ${destino}`), 1000));
}

async function viaje() {
  const respuesta = await mandar('el Puerto');
  console.log(respuesta);
}

viaje();
```

#### Al superarla
La respuesta aparece en lugar del papel sellado. El troll se lleva el papel sellado de recuerdo.

#### Imagen
- Un troll chiquito y gruñón de feria (sin armas) llevándose un papelito sellado bajo el brazo, por la escalera de la torre.
- Nima lee una respuesta de luz; Gheco le saca la lengua al troll.

### Micro-misión R04-N03-P5 · El forEach que no espera

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta
criatura: troll
carta: for…of con await | forEach no espera las promesas · for (const x of lista) { await … } sí
recompensa: xp 15, monedas 5
```

#### Escena
Saeta tiene que mandar flechas a tres destinos, **una por vez**, y anotar *Todas volvieron* al final. Con `forEach`, el *Todas volvieron* sale antes que las respuestas.

#### Gheco sugiere
`forEach` llama a su función para cada elemento **sin esperar** a ninguno, aunque la función tenga `await` adentro. Por eso lo que está después del `forEach` sale antes que las respuestas.

El `for…of` sí respeta el `await`: no pasa al siguiente hasta que vuelve el anterior.

```js
for (const plato of menu) {
    console.log(await cocinar(plato));
}
```

#### Desafío
Que las tres respuestas salgan antes que `Todas volvieron`.

#### Código inicial
```javascript
function mandar(destino) {
  return new Promise((resolve) => setTimeout(() => resolve(`Respuesta de ${destino}`), 1000));
}

const destinos = ['el Valle', 'el Puerto', 'las Forjas'];
destinos.forEach(async (destino) => {
  console.log(await mandar(destino));
});
console.log('Todas volvieron');
```

#### Salida esperada
```
Respuesta de el Valle
Respuesta de el Puerto
Respuesta de las Forjas
Todas volvieron
```

#### Solución
```javascript
function mandar(destino) {
  return new Promise((resolve) => setTimeout(() => resolve(`Respuesta de ${destino}`), 1000));
}

const destinos = ['el Valle', 'el Puerto', 'las Forjas'];
for (const destino of destinos) {
  console.log(await mandar(destino));
}
console.log('Todas volvieron');
```

#### Al superarla
Una por una, las flechas vuelven. Recién después Saeta escribe *Todas volvieron*, y esta vez es verdad.

#### Imagen
- Tres flechas de luz llegando una detrás de otra a la galería, con un reloj de arena grande en la baranda.
- Saeta anota; Nima cuenta con los dedos.

### Micro-misión R04-N03-P6 · La carta a Sila (borrador)

```meta
lugar: La Torre de las Flechas
personajes: Nima, Gheco, Saeta, Lumina
carta: async con valor | una async devuelve una promesa con su return · se espera con await desde afuera
recompensa: xp 15, monedas 5
```

#### Escena
Nima quiere escribirle a Sila, en el Valle, pero no se anima. Lumina le propone empezar con un borrador: una función que arme la carta **esperando** las noticias de la Feria y del Puerto, y la devuelva.

#### Gheco sugiere
Una función `async` siempre **devuelve una promesa**, aunque adentro hagas `return` de un texto común. Por eso, quien la llama tiene que esperar con `await` para tener el texto:

```js
async function pedirPostre() {
    const p = await cocinar('Flan');
    return `De postre: ${p}`;
}
const postre = await pedirPostre();
```

Esperá cada noticia, armá la carta con un *template literal* y devolvela. Copiá el texto de la consigna con cuidado: cada coma y cada punto cuentan.

#### Desafío
Completá `armarCarta` para que devuelva `Querida Sila: en la Feria hay faroles nuevos y en el Puerto llegaron barcos. Nima.`

#### Código inicial
```javascript
const NOTICIAS = { 'la Feria': 'hay faroles nuevos', 'el Puerto': 'llegaron barcos' };
function noticias(lugar) {
  return new Promise((resolve) => setTimeout(() => resolve(NOTICIAS[lugar]), 1000));
}

async function armarCarta() {

}

const carta = await armarCarta();
console.log(carta);
```

#### Salida esperada
```
Querida Sila: en la Feria hay faroles nuevos y en el Puerto llegaron barcos. Nima.
```

#### Solución
```javascript
const NOTICIAS = { 'la Feria': 'hay faroles nuevos', 'el Puerto': 'llegaron barcos' };
function noticias(lugar) {
  return new Promise((resolve) => setTimeout(() => resolve(NOTICIAS[lugar]), 1000));
}

async function armarCarta() {
  const feria = await noticias('la Feria');
  const puerto = await noticias('el Puerto');
  return `Querida Sila: en la Feria ${feria} y en el Puerto ${puerto}. Nima.`;
}

const carta = await armarCarta();
console.log(carta);
```

#### Al superarla
Nima lee el borrador tres veces. No lo manda. Lo dobla y lo guarda en el carcaj, al lado de los papelitos viejos. —Todavía no —dice. Lumina no insiste.

#### Imagen
- Una carta doblada de papel amarillento guardada entre las flechas de un carcaj de cuero.
- Nima, sentada en el borde de la galería de la torre, mira hacia el sur, donde está el Valle; Lumina a su lado.

## R04-N04 · fetch: una flecha al Puerto

```meta
tipo: tema
padre: R04-N03
precio: 10
criatura: troll
temas: js.fetch, web.http, arch.json
```

### Crónica

Saeta lleva a Nima hasta el arco más grande de la galería, apuntado al sur, al **Puerto de los Mensajeros**. —Las flechas de este arco no llevan papeles —le dice—. Llevan **pedidos**: «dame la lista de puestos», «guardá este mensaje», «¿quién soy?». Del otro lado las recibe el muelle de Elefa, y las contesta.

Del otro lado, en el Puerto, un muchacho de gorra azul y bufanda violeta atrapa la primera flecha en el aire: **Nilo**, el mensajero. Lee el pedido, corre a la torre de Elefa, y la respuesta vuelve en otra flecha.

### Objetivos

- Pedir datos a un servidor con `fetch(url)` y leerlos con `await respuesta.json()`.
- Revisar `respuesta.ok` y `respuesta.status` antes de usar los datos.
- Mandar datos con `POST`: `method`, `headers` y `body: JSON.stringify(…)`.
- Distinguir un error de red (`fetch` rechaza) de un error del servidor (la respuesta llega con 404 o 500).
- Atajar un JSON roto.

### Antes de empezar

- R04-N03 (`async`/`await`) y R02-N06 (JSON).

### Explicación

#### Pedir
```javascript
const respuesta = await fetch('/puerto/puestos');
const puestos = await respuesta.json();     // también es una promesa
```
`fetch` devuelve una promesa con la **respuesta**; `.json()` devuelve otra promesa con los **datos**.

#### ¿Salió bien?
```javascript
if (!respuesta.ok) {                         // ok es true si el status es 200 a 299
  console.log('El Puerto contestó', respuesta.status);   // 404, 500…
}
```
**Ojo:** un 404 o un 500 **no** rechazan la promesa: la respuesta llega igual, con el error adentro. `fetch` rechaza solo si la flecha no pudo salir (sin red).

#### Mandar
```javascript
const respuesta = await fetch('/puerto/mensajes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ de: 'Nima', texto: 'Llegué a la Feria' }),
});
```

#### Los códigos más comunes
| Código | Quiere decir |
|---|---|
| 200 | todo bien |
| 201 | creado (después de un POST) |
| 401 | no iniciaste sesión |
| 404 | eso no existe |
| 422 | los datos que mandaste están mal |
| 500 | se rompió algo en el servidor |

> **En la plataforma.** La caja no tiene internet: `fetch('/puerto/…')` lo contesta el **Puerto de Elefa simulado**. Algunas direcciones: `/puerto/hola`, `/puerto/puestos`, `/puerto/puestos/1`, `/puerto/heroes`, `/puerto/clima`, `/puerto/mensajes` (GET y POST), `/puerto/lento`, `/puerto/error`, `/puerto/roto`. En el **Tablero** ves cada pedido, su respuesta y cuánto tardó.

### Código de ejemplo

```javascript
const respuesta = await fetch('/puerto/puestos');
console.log('Status:', respuesta.status, '· ok:', respuesta.ok);
const puestos = await respuesta.json();
console.log(puestos.map((p) => p.nombre));

const noExiste = await fetch('/puerto/puestos/99');
console.log('Status:', noExiste.status, '·', (await noExiste.json()).error);

const enviado = await fetch('/puerto/mensajes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ de: 'Nima', texto: 'Llegué a la Feria' }),
});
console.log('Status:', enviado.status, '·', await enviado.json());

try {
  await fetch('https://internet.de.verdad/');
} catch (error) {
  console.log('Sin red:', error.message);
}
```

### Salida esperada

```
Status: 200 · ok: true
[ 'Tiro al blanco', 'Pan con miel', 'La calesita', 'Títeres de luz' ]
Status: 404 · No hay ningún puesto con el número 99.
Status: 201 · { id: 3, de: 'Nima', texto: 'Llegué a la Feria' }
Sin red: Failed to fetch
```

### ¿Para qué sirve?

Es como una página habla con un servidor: el clima, los mensajes de un chat, los productos de una tienda, guardar lo que escribiste. Es el cruce con PHP: en el curso del Puerto, Nilo escribe el **otro lado** (la API que contesta); acá escribís el lado que pregunta.

### Errores habituales

**Troll: usar la respuesta sin `.json()`.** `respuesta.nombre` da `undefined`: primero `const datos = await respuesta.json()`.

**Troll: creer que un 404 cae en el `catch`.** No cae: revisá `respuesta.ok`.

**Goblin: mandar el objeto sin `JSON.stringify`.** El servidor recibe `[object Object]`.

**Slime: un JSON roto.** `await respuesta.json()` tira `SyntaxError`: atajalo con `try`.

### Micro-misión R04-N04-P1 · La primera flecha al Puerto

```meta
lugar: El arco del sur
personajes: Nima, Gheco, Saeta, Nilo
carta: fetch | const r = await fetch('/puerto/hola') · const datos = await r.json()
recompensa: xp 10, oro 10
```

#### Escena
Nima tensa el arco grande y suelta su primera flecha-pedido al Puerto: `/puerto/hola`. Del otro lado, Nilo la atrapa.

#### Gheco sugiere
`fetch` le **pide algo a un servidor** por internet, con su dirección. Acá no sale a internet: le pide al **Puerto**, un servidor simulado de la Feria.

Son dos esperas:

1. `await fetch('/direccion')` espera la **respuesta** (que llegó, con qué código);
2. `await respuesta.json()` espera el **contenido**, y lo arma como objeto (el `JSON.parse` de R02, pero esperando).

```js
const respuesta = await fetch('/puerto/clima');
const clima = await respuesta.json();
console.log(clima);
```

Mostrá primero el objeto entero para ver qué propiedades trae.

#### Desafío
Pedile el saludo al Puerto y mostralo como `Elefa: ¡Hola, Nima! …`.

#### Código inicial
```javascript
const respuesta = ___;
const datos = ___;
console.log(`${datos.de}: ${datos.mensaje}`);
```

#### Salida esperada
```
Elefa: ¡Hola, Nima! Te escribe Elefa desde el Puerto.
```

#### Solución
```javascript
const respuesta = await fetch('/puerto/hola');
const datos = await respuesta.json();
console.log(`${datos.de}: ${datos.mensaje}`);
```

#### Al superarla
La flecha vuelve con la respuesta de Elefa. Es la primera vez en su vida que a Nima le contesta alguien desde lejos.

#### Imagen
- Un muelle de puerto de noche con barcos y faroles violetas; un muchacho atrapando en el aire una flecha de luz amarilla que llega desde el norte.
- Nilo (muchacho de 17, gorra de mensajero azul noche, bufanda violeta larga, chaqueta corta de lona con bolsillos, bolso cruzado de cuero con sobres de lacre violeta) atrapa la flecha, sonriendo.

### Micro-misión R04-N04-P2 · La lista de puestos

```meta
lugar: El arco del sur
personajes: Nima, Gheco, Nilo
carta: Datos de un fetch | lo que llega es un arreglo u objeto común · se usa con map, filter, for…of
recompensa: xp 10, oro 10
```

#### Escena
Elefa guarda en el Puerto la lista oficial de puestos de la Feria. Nima quiere saber cuáles están abiertos esta noche.

#### Gheco sugiere
Si el Puerto devuelve un **arreglo** de objetos, se trabaja como en R01:

- `filter` se queda con los que cumplen algo;
- `map` transforma cada uno (por ejemplo, en solo su nombre).

```js
const baratos = juegos.filter((j) => j.precio < 5).map((j) => j.nombre);
```

Se pueden encadenar: el `map` trabaja sobre lo que dejó el `filter`.

#### Desafío
Mostrá los nombres de los puestos abiertos.

#### Código inicial
```javascript
const puestos = await (await fetch('/puerto/puestos')).json();

```

#### Salida esperada
```
Abiertos: [ 'Tiro al blanco', 'Pan con miel', 'Títeres de luz' ]
```

#### Solución
```javascript
const puestos = await (await fetch('/puerto/puestos')).json();

const abiertos = puestos.filter((p) => p.abierto).map((p) => p.nombre);
console.log('Abiertos:', abiertos);
```

#### Al superarla
—¿La calesita cerrada? —se sorprende Nima—. Mañana voy a ver qué le pasa.

#### Imagen
- Un pergamino largo de luz con una lista de puestos (sin texto legible) llegando atado a una flecha a la galería de la torre.
- Nima lo desenrolla; Gheco señala uno con la colita.

### Micro-misión R04-N04-P3 · El puesto que no existe

```meta
lugar: El arco del sur
personajes: Nima, Gheco, Nilo
criatura: troll
carta: respuesta.ok | un 404 llega como respuesta, no como error · revisá ok o status antes de usar los datos
recompensa: xp 10, oro 10
```

#### Escena
Nima pide el puesto número 9. El Puerto contesta, pero con un 404. El programa muestra *undefined cuesta undefined fichas* y sigue como si nada.

#### Gheco sugiere
Que llegue una respuesta no quiere decir que haya salido bien: el servidor puede contestar «no existe» o «no podés». Eso lo dice el **código de estado**:

- `respuesta.status` es el número: `200` está bien, `404` es «no encontrado»;
- `respuesta.ok` es `true` si salió bien (entre 200 y 299) y `false` si no.

```js
if (!respuesta.ok) {
    console.log('Error', respuesta.status);
}
```

Cuando sale mal, el Puerto igual manda un JSON, con una propiedad `error` que explica qué pasó.

#### Desafío
Manejá la respuesta de error.

#### Código inicial
```javascript
const respuesta = await fetch('/puerto/puestos/9');
const datos = await respuesta.json();
console.log(`${datos.nombre} cuesta ${datos.precio} fichas`);
```

#### Salida esperada
```
No se pudo (404): No hay ningún puesto con el número 9.
```

#### Solución
```javascript
const respuesta = await fetch('/puerto/puestos/9');
const datos = await respuesta.json();
if (!respuesta.ok) {
  console.log(`No se pudo (${respuesta.status}): ${datos.error}`);
} else {
  console.log(`${datos.nombre} cuesta ${datos.precio} fichas`);
}
```

#### Al superarla
Del otro lado, Nilo se rasca la cabeza: —¿El puesto 9? Acá no hay nada con ese número. —Ahora el programa lo dice claro.

#### Imagen
- Nilo en el muelle mirando un cuaderno de registros vacío en una página, con una flecha de luz en la otra mano.
- Detrás, Elefa (elefanta enorme con armadura y un bastón coronado por un sello de lacre) niega con la trompa.

### Micro-misión R04-N04-P4 · Un mensaje para el Puerto

```meta
lugar: El arco del sur
personajes: Nima, Gheco, Nilo, Elefa
carta: POST | fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(datos) })
recompensa: xp 10, oro 10
```

#### Escena
Nima quiere dejar un mensaje en el tablero del Puerto: *De Nima: saludos desde la Feria*.

#### Gheco sugiere
Hasta ahora `fetch` **pedía** (eso se llama `GET`). Para **mandar** datos se usa `POST`, y se le pasa un segundo dato con las opciones:

```js
await fetch('/puerto/pedidos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ plato: 'Pan', cantidad: 2 }),
});
```

- `method` dice qué se hace;
- `headers` avisa que lo que va es JSON;
- `body` es lo que se manda, pasado a texto.

Cuando guarda algo nuevo, el Puerto contesta con el código `201` (*creado*) y devuelve lo guardado con su `id` (su número).

#### Desafío
Mandá el mensaje y mostrá el status y el `id` que le dio el Puerto.

#### Código inicial
```javascript
const respuesta = await fetch('/puerto/mensajes', {

});
const guardado = await respuesta.json();
console.log('Status:', respuesta.status);
console.log('Mensaje número', guardado.id, '·', guardado.texto);
```

#### Salida esperada
```
Status: 201
Mensaje número 3 · Saludos desde la Feria
```

#### Solución
```javascript
const respuesta = await fetch('/puerto/mensajes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ de: 'Nima', texto: 'Saludos desde la Feria' }),
});
const guardado = await respuesta.json();
console.log('Status:', respuesta.status);
console.log('Mensaje número', guardado.id, '·', guardado.texto);
```

#### Al superarla
En el Puerto, Elefa clava el mensaje de Nima en el tablero del muelle con su sello. —Mensaje número tres —dice—. Bienvenida, arquera.

#### Imagen
- El tablero de mensajes del muelle del Puerto con un papel nuevo sellado con lacre violeta.
- Elefa (elefanta enorme con armadura) sella el papel; Nilo silba al lado.

### Micro-misión R04-N04-P5 · El mensaje vacío

```meta
lugar: El arco del sur
personajes: Nima, Gheco, Nilo, Elefa
carta: Errores del servidor | 422: los datos están mal · el servidor valida y contesta qué falta · mostralo
recompensa: xp 15, monedas 5
```

#### Escena
Bruno mandó un mensaje sin texto, y el Puerto lo rechazó con un 422. El programa de Bruno muestra *Mensaje número undefined*. Elefa no deja pasar nada sin revisar.

#### Gheco sugiere
Un servidor puede **rechazar** lo que le mandás si no está bien: un dato vacío, un número que no es. Contesta con un código de error (acá, `422`: «no puedo procesar esto») y explica en `error` qué falló.

En la función: hacé el `POST`, leé el JSON y, según `respuesta.ok`, devolvé un texto u otro. Fijate en la consigna el texto exacto de cada caso.

#### Desafío
Completá `enviar` y probala con un mensaje vacío y uno bueno.

#### Código inicial
```javascript
async function enviar(texto) {

}

console.log(await enviar(''));
console.log(await enviar('Bruno estuvo acá'));
```

#### Salida esperada
```
Rechazado: Falta el texto del mensaje.
Guardado con número 3
```

#### Solución
```javascript
async function enviar(texto) {
  const respuesta = await fetch('/puerto/mensajes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ de: 'Bruno', texto }),
  });
  const datos = await respuesta.json();
  if (!respuesta.ok) return `Rechazado: ${datos.error}`;
  return `Guardado con número ${datos.id}`;
}

console.log(await enviar(''));
console.log(await enviar('Bruno estuvo acá'));
```

#### Al superarla
El primer mensaje vuelve rebotado con una nota de Elefa: *falta el texto*. El segundo se queda en el tablero. Bruno lo festeja como un gol.

#### Imagen
- Una flecha de luz rebotando contra un sello rojo de rechazo en el muelle del Puerto, y otra clavada en el tablero.
- Bruno (gorra al revés, chaleco rojo) festeja en la galería de la torre; Saeta pone los ojos en blanco.

### Micro-misión R04-N04-P6 · El JSON roto del Puerto

```meta
lugar: El arco del sur
personajes: Nima, Gheco, Nilo
criatura: slime
carta: Todo lo que puede fallar | sin red: fetch rechaza · error del servidor: ok es false · JSON roto: .json() rechaza
recompensa: xp 15, monedas 5
```

#### Escena
Una flecha llegó mojada: el papel del Puerto está cortado por la mitad (`/puerto/roto`). Otra fue a una dirección que no es el Puerto. Nima quiere una función que nunca explote y diga qué pasó.

#### Gheco sugiere
Con `fetch` pueden salir mal **dos cosas distintas**:

- el servidor contesta, pero con error: `respuesta.ok` es `false` (no lanza nada, hay que mirarlo);
- algo se rompe: no hay conexión, o lo que llegó no es JSON válido y `respuesta.json()` **lanza** un error. Eso se ataja con `try`/`catch`.

`error.name` es el **tipo** de error (`SyntaxError`, `TypeError`…). Adentro del `try`, devolvé lo que corresponde en cada caso; en el `catch`, el aviso del error.

#### Desafío
Completá `pedir` y probala con las cuatro direcciones.

#### Código inicial
```javascript
async function pedir(url) {

}

console.log(await pedir('/puerto/clima'));
console.log(await pedir('/puerto/error'));
console.log(await pedir('/puerto/roto'));
console.log(await pedir('https://otro.lugar/'));
```

#### Salida esperada
```
{ noche: true, viento: 'suave', temperatura: 18, luciernagas: 120 }
Error 500
Falló: SyntaxError
Falló: TypeError
```

#### Solución
```javascript
async function pedir(url) {
  try {
    const respuesta = await fetch(url);
    if (!respuesta.ok) return `Error ${respuesta.status}`;
    return await respuesta.json();
  } catch (error) {
    return `Falló: ${error.name}`;
  }
}

console.log(await pedir('/puerto/clima'));
console.log(await pedir('/puerto/error'));
console.log(await pedir('/puerto/roto'));
console.log(await pedir('https://otro.lugar/'));
```

#### Al superarla
Cuatro flechas, cuatro respuestas distintas, y ninguna explota. Nilo, del otro lado, escribe en su libreta: *la arquera de la Feria pregunta bien*.

#### Imagen
- Cuatro flechas de luz en la galería: una entera, una con una cruz roja, una con el papel roto y mojado, y una que nunca salió.
- Nima las ordena en la baranda; un slime verde chiquito se escurre del papel mojado.

## R04-N05 · Varias flechas a la vez

```meta
tipo: tema
padre: R04-N04
precio: 10
criatura: troll
temas: conc.async, js.fetch
```

### Crónica

La víspera de la Gran Noche de la Feria, Lumina necesita confirmar a la vez el clima, la lista de puestos y los héroes invitados. Si Saeta manda las flechas de a una, esperando cada respuesta, tarda una eternidad.

—No hace falta esperar una para soltar la otra —dice Saeta, y tensa tres flechas a la vez en el mismo arco—. Salen juntas, y esperás a que vuelvan todas.

### Objetivos

- Esperar varias promesas a la vez con `Promise.all`.
- Saber qué pasa si una falla, y usar `Promise.allSettled` para tener todas las respuestas igual.
- Quedarse con la primera que llegue con `Promise.race`.
- Ponerle un tiempo máximo a un pedido con `AbortController` (o `AbortSignal.timeout`).

### Antes de empezar

- R04-N03 y R04-N04: `async`/`await` y `fetch`.

### Explicación

#### Juntas
```javascript
const [clima, puestos] = await Promise.all([pedir('/puerto/clima'), pedir('/puerto/puestos')]);
```
Salen al mismo tiempo y tardan lo que tarde **la más lenta**, no la suma.

#### Si una falla
`Promise.all` se rechaza apenas **una** falla. Si querés todas las respuestas, buenas y malas:
```javascript
const resultados = await Promise.allSettled(promesas);
// [{ status: 'fulfilled', value: … }, { status: 'rejected', reason: Error }]
```

#### La primera que llega
```javascript
const primera = await Promise.race([flechaA, flechaB]);
```

#### Un tiempo máximo
```javascript
const respuesta = await fetch('/puerto/lento', { signal: AbortSignal.timeout(1000) });
// si tarda más de 1 s, se cancela: TimeoutError
```
Con `const control = new AbortController()` y `control.abort()` la cancelás vos cuando quieras (por ejemplo, si la persona tocó *Cancelar*).

### Código de ejemplo

```javascript
const pedir = async (url) => (await fetch(url)).json();

let inicio = performance.now();
await pedir('/puerto/clima');
await pedir('/puerto/puestos');
console.log('De a una:', performance.now() - inicio, 'ms');

inicio = performance.now();
const [clima, puestos] = await Promise.all([pedir('/puerto/clima'), pedir('/puerto/puestos')]);
console.log('Juntas:', performance.now() - inicio, 'ms ·', clima.temperatura, 'grados ·', puestos.length, 'puestos');

const resultados = await Promise.allSettled([pedir('/puerto/hola'), pedir('/puerto/roto')]);
console.log(resultados.map((r) => r.status));

try {
  await fetch('/puerto/lento', { signal: AbortSignal.timeout(1000) });
} catch (error) {
  console.log('Cancelado:', error.name);
}
```

### Salida esperada

```
De a una: 600 ms
Juntas: 400 ms · 18 grados · 4 puestos
[ 'fulfilled', 'rejected' ]
Cancelado: TimeoutError
```

### ¿Para qué sirve?

Una página que carga el perfil, los mensajes y las notificaciones a la vez abre mucho más rápido que una que los pide de a uno. Y ponerle un tiempo máximo a un pedido evita que la página quede «cargando» para siempre.

### Errores habituales

**Troll: esperar de a una lo que no depende.** Dos `await` seguidos que no se necesitan entre sí tardan el doble.

**Troll: `Promise.all` con una que falla.** Se pierden también las respuestas buenas. Si necesitás todas, `allSettled`.

**Ogro: el orden.** `Promise.all` devuelve los resultados **en el orden de la lista**, no en el orden en que llegaron.

### Micro-misión R04-N05-P1 · Tres flechas en un arco

```meta
lugar: La galería de la Torre
personajes: Nima, Gheco, Saeta
carta: Promise.all | await Promise.all([p1, p2, p3]) · salen juntas · los resultados en el orden de la lista
recompensa: xp 10, oro 10
```

#### Escena
Saeta le enseña a Nima a tensar tres flechas a la vez: el clima, los puestos y los héroes.

#### Gheco sugiere
Si varias cosas **no dependen** una de otra, no hace falta pedirlas de a una: `Promise.all([…])` recibe un arreglo de promesas, espera **a todas juntas** y da un arreglo con los resultados, **en el mismo orden**:

```js
const [pan, torta] = await Promise.all([cocinar('Pan'), cocinar('Torta')]);
```

El `[pan, torta] =` es la desestructuración de R01: saca cada resultado del arreglo con su nombre.

#### Desafío
Pedí las tres cosas juntas y mostrá la temperatura, cuántos puestos y cuántos héroes hay.

#### Código inicial
```javascript
const pedir = async (url) => (await fetch(url)).json();

const [clima, puestos, heroes] = ___;
console.log(`${clima.temperatura} grados · ${puestos.length} puestos · ${heroes.length} héroes`);
console.log('Tardó', performance.now(), 'ms');
```

#### Salida esperada
```
18 grados · 4 puestos · 4 héroes
Tardó 500 ms
```

#### Solución
```javascript
const pedir = async (url) => (await fetch(url)).json();

const [clima, puestos, heroes] = await Promise.all([pedir('/puerto/clima'), pedir('/puerto/puestos'), pedir('/puerto/heroes')]);
console.log(`${clima.temperatura} grados · ${puestos.length} puestos · ${heroes.length} héroes`);
console.log('Tardó', performance.now(), 'ms');
```

#### Al superarla
Tres flechas salen del mismo arco y vuelven casi juntas. Saeta no dice nada, pero le da a Nima una palmada en la espalda, que en ella es muchísimo.

#### Imagen
- Un arco tensado con tres flechas de luz a la vez, desde la galería de la torre, apuntando al sur.
- Saeta le acomoda los dedos a Nima en la cuerda; Gheco cuenta las flechas.

### Micro-misión R04-N05-P2 · De a una tarda más

```meta
lugar: La galería de la Torre
personajes: Nima, Gheco, Saeta
carta: No esperar de más | dos await seguidos suman los tiempos · juntas, tarda lo de la más lenta
recompensa: xp 10, oro 10
```

#### Escena
Bruno escribió el pedido de los héroes y de los puestos con dos `await` seguidos. Tarda casi un segundo. Saeta dice que se puede en la mitad.

#### Gheco sugiere
Con dos `await` seguidos, la segunda pregunta **no sale** hasta que vuelve la primera: el tiempo total es la **suma**. Con `Promise.all`, salen las dos a la vez y se espera solo a la más lenta.

`performance.now()` da los milisegundos desde que empezó el programa: sirve para ver cuánto se tardó.

#### Desafío
Que tarde lo de la más lenta (500 ms) y no la suma.

#### Código inicial
```javascript
const pedir = async (url) => (await fetch(url)).json();

const heroes = await pedir('/puerto/heroes');
const puestos = await pedir('/puerto/puestos');
console.log(heroes.length, puestos.length);
console.log('Tardó', performance.now(), 'ms');
```

#### Salida esperada
```
4 4
Tardó 500 ms
```

#### Solución
```javascript
const pedir = async (url) => (await fetch(url)).json();

const [heroes, puestos] = await Promise.all([pedir('/puerto/heroes'), pedir('/puerto/puestos')]);
console.log(heroes.length, puestos.length);
console.log('Tardó', performance.now(), 'ms');
```

#### Al superarla
—¿Quinientos? —dice Bruno, mirando el reloj—. Era novecientos. —Se queda pensando en todo el tiempo que perdió esperando de a una.

#### Imagen
- Un reloj de arena grande en la galería de la torre con la mitad de la arena cayendo.
- Bruno mira el reloj con la boca abierta; Saeta a su lado, tranquila.

### Micro-misión R04-N05-P3 · Las que vuelven y las que no

```meta
lugar: La galería de la Torre
personajes: Nima, Gheco, Saeta
carta: Promise.allSettled | espera todas aunque alguna falle · cada una: { status, value } o { status, reason }
recompensa: xp 10, oro 10
```

#### Escena
Lumina mandó cuatro invitaciones. Una dirección no existe y otra contesta roto. Con `Promise.all`, el error de una tira abajo todo. Lumina quiere saber cuáles volvieron y cuáles no.

#### Gheco sugiere
`Promise.all` tiene una debilidad: si **una sola** falla, falla todo, y se pierden los resultados de las que sí volvieron.

`Promise.allSettled([…])` espera a todas, salgan bien o mal, y da un arreglo con un objeto por cada una:

- `status` es `'fulfilled'` (cumplida) o `'rejected'` (rechazada);
- si se cumplió, el valor está en `value`; si se rechazó, el error está en `reason`.

```js
for (const r of resultados) {
    if (r.status === 'fulfilled') console.log(r.value);
}
```

#### Desafío
Mostrá el resultado de cada invitación.

#### Código inicial
```javascript
async function invitar(url) {
  const respuesta = await fetch(url);
  if (!respuesta.ok) throw new Error(`${url} contestó ${respuesta.status}`);
  return `${url} acepta`;
}

const urls = ['/puerto/hola', '/puerto/nada', '/puerto/clima', '/puerto/error'];
const resultados = ___;

```

#### Salida esperada
```
Volvió: /puerto/hola acepta
No volvió: /puerto/nada contestó 404
Volvió: /puerto/clima acepta
No volvió: /puerto/error contestó 500
```

#### Solución
```javascript
async function invitar(url) {
  const respuesta = await fetch(url);
  if (!respuesta.ok) throw new Error(`${url} contestó ${respuesta.status}`);
  return `${url} acepta`;
}

const urls = ['/puerto/hola', '/puerto/nada', '/puerto/clima', '/puerto/error'];
const resultados = await Promise.allSettled(urls.map(invitar));

for (const r of resultados) {
  if (r.status === 'fulfilled') console.log('Volvió:', r.value);
  else console.log('No volvió:', r.reason.message);
}
```

#### Al superarla
Dos invitaciones aceptadas y dos rebotadas, cada una con su motivo. Lumina anota a las que faltan para mandarles otra flecha mañana.

#### Imagen
- Cuatro flechas de luz en la baranda: dos con lazos dorados y dos con un sello rojo.
- Lumina (luciérnaga enorme, alas de vidrio) las revisa una por una.

### Micro-misión R04-N05-P4 · La flecha lenta

```meta
lugar: La galería de la Torre
personajes: Nima, Gheco, Saeta
criatura: troll
carta: Tiempo máximo | fetch(url, { signal: AbortSignal.timeout(ms) }) · si tarda más, se cancela con TimeoutError
recompensa: xp 10, oro 10
```

#### Escena
El pedido `/puerto/lento` tarda 3 segundos (la marea estaba alta). La galería no puede esperar tanto: después de 2 segundos, hay que darlo por perdido y avisar.

#### Gheco sugiere
Un pedido puede tardar demasiado. Se lo puede **cancelar** solo con una señal de tiempo, que va en las opciones del `fetch`:

```js
await fetch('/puerto/algo', { signal: AbortSignal.timeout(3000) });
```

Si a los 3000 ms no volvió, el `fetch` se cancela y **lanza** un error cuyo `error.name` es `'TimeoutError'`. Atajalo con `try`/`catch` y preguntá por ese nombre.

#### Desafío
Cancelá el pedido a los 2 segundos y avisalo.

#### Código inicial
```javascript
try {
  const respuesta = await fetch('/puerto/lento');
  console.log((await respuesta.json()).mensaje);
} catch (error) {

}
console.log('Pasaron', performance.now(), 'ms');
```

#### Salida esperada
```
La flecha tardó demasiado
Pasaron 2000 ms
```

#### Solución
```javascript
try {
  const respuesta = await fetch('/puerto/lento', { signal: AbortSignal.timeout(2000) });
  console.log((await respuesta.json()).mensaje);
} catch (error) {
  if (error.name === 'TimeoutError') console.log('La flecha tardó demasiado');
}
console.log('Pasaron', performance.now(), 'ms');
```

#### Al superarla
A los dos segundos, Saeta corta el hilo de la flecha lenta. —Mejor saber que no llega —dice— que esperar para siempre.

#### Imagen
- Saeta cortando con un cuchillito un hilo de luz atado a una flecha lejana, en la galería de la torre.
- Un troll chiquito y gruñón (sin armas) se cae de la flecha lenta, en el aire.

### Micro-misión R04-N05-P5 · La primera que llega

```meta
lugar: La galería de la Torre
personajes: Nima, Gheco, Saeta
carta: Promise.race | await Promise.race([p1, p2]) · gana la primera que termine (bien o mal)
recompensa: xp 15, monedas 5
```

#### Escena
Saeta propone una carrera: Nima y Bruno mandan flechas al Puerto a la vez. Gana la primera que vuelva.

#### Gheco sugiere
`Promise.race([…])` (*carrera*) larga todas las promesas y da el valor de **la primera que termina**. Las demás siguen, pero ya no importan.

Para probarla, hace falta una función que devuelva una promesa que se cumple a tantos milisegundos, con un valor:

```js
const corredor = (nombre, ms) => new Promise((resolve) => setTimeout(() => resolve(nombre), ms));
```

Fijate quién tiene que ganar y con cuántos milisegundos tira cada uno.

#### Desafío
Mostrá `Ganó Nima`.

#### Código inicial
```javascript
const flecha = (quien, ms) => new Promise((resolve) => setTimeout(() => resolve(quien), ms));

const ganadora = ___;
console.log(`Ganó ${ganadora}`);
```

#### Salida esperada
```
Ganó Nima
```

#### Solución
```javascript
const flecha = (quien, ms) => new Promise((resolve) => setTimeout(() => resolve(quien), ms));

const ganadora = await Promise.race([flecha('Bruno', 900), flecha('Nima', 600)]);
console.log(`Ganó ${ganadora}`);
```

#### Al superarla
La flecha de Nima vuelve primero. Bruno dice que el viento estaba a favor de ella. Saeta dice que no había viento.

#### Imagen
- Dos flechas de luz de colores distintos volando en paralelo hacia el sur, una adelante.
- Nima y Bruno en la baranda de la galería, mirándolas con los arcos en la mano.

### Micro-misión R04-N05-P6 · El botón de cancelar

```meta
lugar: La galería de la Torre
personajes: Nima, Gheco, Saeta, Lumina
carta: AbortController | const control = new AbortController() · fetch(url, { signal: control.signal }) · control.abort() cancela
recompensa: xp 15, monedas 5
```

#### Escena
Lumina quiere un botón *Cancelar* en la galería: si alguien se arrepiente de un pedido lento, lo corta.

#### Gheco sugiere
Para cancelar **cuando quieras** (con un botón, por ejemplo), se usa un `AbortController`, que tiene dos partes:

- `control.signal`, la señal que va en las opciones del `fetch`;
- `control.abort()`, que cancela.

```js
const control = new AbortController();
fetch('/puerto/algo', { signal: control.signal });
// más tarde:
control.abort();
```

Al cancelar, el `fetch` lanza un error con `name` igual a `'AbortError'`. El controlador tiene que estar en una variable **afuera** de los dos eventos, así el segundo botón lo encuentra. La función del evento puede ser `async` para usar `await` adentro.

#### Desafío
Completá los dos botones. (La comprobación pide, espera 1 s y cancela.)

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; text-align: center; }
  button { font-size: 18px; margin: 4px; padding: 6px 14px; }
  #estado { font-size: 22px; color: #ffd400; }
</style>
<button id="pedir">Pedir al Puerto</button> <button id="cancelar">Cancelar</button>
<p id="estado">Listo</p>
```

#### Eventos
```
click #pedir
esperar 1000
click #cancelar
esperar 3000
```

#### Estado
```
#estado
pedidos
```

#### Código inicial
```javascript
const estado = document.querySelector('#estado');
let control = null;

document.querySelector('#pedir').addEventListener('click', async () => {

});

document.querySelector('#cancelar').addEventListener('click', () => {

});
```

#### Salida esperada
```
── Estado ──
#estado: Cancelado
pedidos: GET /puerto/lento → cancelado
```

#### Solución
```javascript
const estado = document.querySelector('#estado');
let control = null;

document.querySelector('#pedir').addEventListener('click', async () => {
  control = new AbortController();
  estado.textContent = 'Esperando…';
  try {
    const respuesta = await fetch('/puerto/lento', { signal: control.signal });
    estado.textContent = (await respuesta.json()).mensaje;
  } catch (error) {
    if (error.name === 'AbortError') estado.textContent = 'Cancelado';
  }
});

document.querySelector('#cancelar').addEventListener('click', () => {
  control?.abort();
});
```

#### Al superarla
La flecha lenta vuelve sola a la galería, plegada, sin llegar al Puerto. Lumina asiente. —Saber soltar —dice— también es saber cancelar.

#### Imagen
- Una flecha de luz plegándose en el aire y volviendo hacia la galería, y un botón de bronce grande con una cruz.
- Lumina toca el botón con una pata; Nima y Saeta miran.

## R04-N06 · Errores propios

```meta
tipo: tema
padre: R04-N05
precio: 10
criatura: ogre
temas: err.excepciones
```

### Crónica

En el libro de Saeta, los errores están todos anotados igual: *se perdió*. Pero no es lo mismo una flecha que se perdió en la niebla, una que llegó a una dirección equivocada o una que volvió rota. Cada una se arregla distinto.

—Si todos los errores se llaman igual, no sabés qué hacer con cada uno —dice {mentor}—. Ponele nombre a los tuyos.

### Objetivos

- Lanzar errores con `throw new Error(…)`.
- Crear clases de error propias con `extends Error`, con su nombre y sus datos.
- Distinguirlos en el `catch` con `instanceof`.
- Volver a lanzar (`throw error`) lo que no sabés manejar.
- Usar `finally` para lo que tiene que pasar siempre.

### Antes de empezar

- R03-N03 (herencia) y R04-N03 (`try`/`catch` con `await`).

### Explicación

#### Lanzar
```javascript
function apuntar(distancia) {
  if (distancia > 500) throw new Error('Demasiado lejos');
  return 'en el blanco';
}
```

#### Errores con nombre
```javascript
class FlechaPerdida extends Error {
  constructor(destino) {
    super(`La flecha a ${destino} se perdió`);
    this.name = 'FlechaPerdida';
    this.destino = destino;
  }
}
throw new FlechaPerdida('la Niebla');
```

#### Distinguirlos
```javascript
try {
  …
} catch (error) {
  if (error instanceof FlechaPerdida) {
    console.log('Mandar otra a', error.destino);
  } else {
    throw error;   // lo que no sé manejar, que siga para arriba
  }
} finally {
  console.log('Saeta anota');
}
```

### Código de ejemplo

```javascript
class FlechaPerdida extends Error {
  constructor(destino) {
    super(`La flecha a ${destino} se perdió`);
    this.name = 'FlechaPerdida';
    this.destino = destino;
  }
}
class DireccionEquivocada extends Error {
  name = 'DireccionEquivocada';
}

function mandar(destino) {
  if (destino === 'la Niebla') throw new FlechaPerdida(destino);
  if (!destino.startsWith('el ')) throw new DireccionEquivocada(`No conozco «${destino}»`);
  return `Llegó a ${destino}`;
}

for (const destino of ['el Puerto', 'la Niebla', 'Marte']) {
  try {
    console.log(mandar(destino));
  } catch (error) {
    if (error instanceof FlechaPerdida) console.log(`${error.name}: reintentar a ${error.destino}`);
    else console.log(`${error.name}: ${error.message}`);
  } finally {
    console.log('  (Saeta anota)');
  }
}
```

### Salida esperada

```
Llegó a el Puerto
  (Saeta anota)
FlechaPerdida: reintentar a la Niebla
  (Saeta anota)
DireccionEquivocada: No conozco «Marte»
  (Saeta anota)
```

### ¿Para qué sirve?

En una aplicación de verdad, no es lo mismo «la clave es incorrecta» que «se cortó internet» o «el servidor se cayó»: a la persona se le muestra algo distinto, y a veces se reintenta. Los errores con nombre hacen que el código que los ataja sea claro.

### Errores habituales

**Ogro: el `catch` que se traga todo.** Un `catch` vacío esconde los errores que no esperabas. Si no sabés qué hacer con uno, volvé a lanzarlo.

**Ogro: lanzar textos.** `throw 'se perdió'` funciona, pero pierde la línea y el nombre. Siempre `throw new Error(…)` (o una clase tuya).

**Esqueleto: olvidarse `this.name`.** El error se muestra como `Error`, no como `FlechaPerdida`.

### Micro-misión R04-N06-P1 · Demasiado lejos

```meta
lugar: El libro de Saeta
personajes: Nima, Gheco, Saeta
carta: throw | throw new Error('mensaje') corta la función · el que llama lo ataja con try/catch
recompensa: xp 10, oro 10
```

#### Escena
El arco de Nima llega hasta 500 pasos. Saeta quiere que la función de apuntar **se queje** si le piden más.

#### Gheco sugiere
Tus propias funciones también pueden **lanzar errores**, cuando les piden algo que no se puede. `throw` corta la función ahí mismo y manda el error hacia afuera:

```js
function dividir(a, b) {
    if (b === 0) throw new Error('No se divide por cero');
    return a / b;
}
```

El texto del `new Error(…)` es el que después se lee en `error.message`, en el `catch`.

#### Desafío
Completá `apuntar`.

#### Código inicial
```javascript
function apuntar(distancia) {

  return `Blanco a ${distancia} pasos`;
}

for (const d of [100, 800, 450]) {
  try {
    console.log(apuntar(d));
  } catch (error) {
    console.log(`${d}: ${error.message}`);
  }
}
```

#### Salida esperada
```
Blanco a 100 pasos
800: Demasiado lejos
Blanco a 450 pasos
```

#### Solución
```javascript
function apuntar(distancia) {
  if (distancia > 500) throw new Error('Demasiado lejos');
  return `Blanco a ${distancia} pasos`;
}

for (const d of [100, 800, 450]) {
  try {
    console.log(apuntar(d));
  } catch (error) {
    console.log(`${d}: ${error.message}`);
  }
}
```

#### Al superarla
El arco de Nima ya no intenta lo imposible. Avisa, y ella apunta a otro lado.

#### Imagen
- Un campo de tiro con blancos a distintas distancias, uno muy lejos, casi en el horizonte.
- Nima baja el arco frente al blanco lejano; Saeta niega con la cabeza.

### Micro-misión R04-N06-P2 · Ponerle nombre

```meta
lugar: El libro de Saeta
personajes: Nima, Gheco, Saeta
carta: Error propio | class X extends Error { constructor(…) { super(mensaje); this.name = 'X'; } }
recompensa: xp 10, oro 10
```

#### Escena
Saeta quiere que las flechas perdidas tengan su propio nombre en el libro: *FlechaPerdida*, con el destino adentro.

#### Gheco sugiere
Se puede crear un **tipo de error propio**, con una clase que hereda de `Error` (el `extends` de R03). Así el error lleva un nombre que dice qué pasó y los datos que hagan falta:

```js
class SinStock extends Error {
    constructor(producto) {
        super(`No queda ${producto}`);   // el mensaje
        this.name = 'SinStock';
        this.producto = producto;
    }
}
```

El `super(…)` recibe el mensaje; `this.name` es el nombre que se ve en el error.

#### Desafío
Escribí la clase.

#### Código inicial
```javascript
// escribí FlechaPerdida acá


try {
  throw new FlechaPerdida('la Niebla');
} catch (error) {
  console.log(error.name, '·', error.message, '·', error.destino);
  console.log(error instanceof Error);
}
```

#### Salida esperada
```
FlechaPerdida · La flecha a la Niebla se perdió · la Niebla
true
```

#### Solución
```javascript
class FlechaPerdida extends Error {
  constructor(destino) {
    super(`La flecha a ${destino} se perdió`);
    this.name = 'FlechaPerdida';
    this.destino = destino;
  }
}

try {
  throw new FlechaPerdida('la Niebla');
} catch (error) {
  console.log(error.name, '·', error.message, '·', error.destino);
  console.log(error instanceof Error);
}
```

#### Al superarla
En el libro de Saeta aparece una columna nueva: *tipo de error*. La primera fila dice *FlechaPerdida · la Niebla*.

#### Imagen
- El libro grande de cuero de Saeta con una columna nueva dibujada a mano (sin texto legible).
- Saeta escribe con una pluma; Nima le dicta.

### Micro-misión R04-N06-P3 · Cada error, su arreglo

```meta
lugar: El libro de Saeta
personajes: Nima, Gheco, Saeta
carta: instanceof en el catch | if (error instanceof FlechaPerdida) … else if … · cada uno se maneja distinto
recompensa: xp 10, oro 10
```

#### Escena
Las flechas perdidas se reintentan; las que van a una dirección equivocada se tiran. Saeta quiere que el programa lo decida solo.

#### Gheco sugiere
Con errores de distintos tipos, el `catch` puede preguntar **cuál llegó** con `instanceof` (de R03) y hacer algo distinto para cada uno:

```js
catch (error) {
    if (error instanceof SinStock) {
        console.log('Pedir más', error.producto);
    } else if (error instanceof PrecioMal) {
        console.log('Revisar', error.message);
    }
}
```

Fijate en la consigna el texto de cada caso y qué dato del error usa.

#### Desafío
Completá el `catch`.

#### Código inicial
```javascript
class FlechaPerdida extends Error {
  constructor(destino) {
    super(`se perdió rumbo a ${destino}`);
    this.name = 'FlechaPerdida';
    this.destino = destino;
  }
}
class DireccionEquivocada extends Error {
  name = 'DireccionEquivocada';
}

function mandar(destino) {
  if (destino === 'la Niebla') throw new FlechaPerdida(destino);
  if (destino === 'Marte') throw new DireccionEquivocada('Marte no existe');
  return `Llegó a ${destino}`;
}

for (const destino of ['el Puerto', 'la Niebla', 'Marte']) {
  try {
    console.log(mandar(destino));
  } catch (error) {

  }
}
```

#### Salida esperada
```
Llegó a el Puerto
Reintentar a la Niebla
Descartar: Marte no existe
```

#### Solución
```javascript
class FlechaPerdida extends Error {
  constructor(destino) {
    super(`se perdió rumbo a ${destino}`);
    this.name = 'FlechaPerdida';
    this.destino = destino;
  }
}
class DireccionEquivocada extends Error {
  name = 'DireccionEquivocada';
}

function mandar(destino) {
  if (destino === 'la Niebla') throw new FlechaPerdida(destino);
  if (destino === 'Marte') throw new DireccionEquivocada('Marte no existe');
  return `Llegó a ${destino}`;
}

for (const destino of ['el Puerto', 'la Niebla', 'Marte']) {
  try {
    console.log(mandar(destino));
  } catch (error) {
    if (error instanceof FlechaPerdida) console.log(`Reintentar a ${error.destino}`);
    else if (error instanceof DireccionEquivocada) console.log(`Descartar: ${error.message}`);
  }
}
```

#### Al superarla
Saeta separa el carcaj de reintentos del cesto de descartes. Por primera vez, no tira flechas buenas.

#### Imagen
- Un carcaj con un cartelito de reintento y un cesto de mimbre con flechas descartadas, en la galería de la torre.
- Saeta acomoda flechas; Gheco duerme en el cesto.

### Micro-misión R04-N06-P4 · El ogro que se traga todo

```meta
lugar: El libro de Saeta
personajes: Nima, Gheco
criatura: ogre
carta: Volver a lanzar | catch { if (lo conozco) …; else throw error; } · un catch vacío esconde los errores de verdad
recompensa: xp 10, oro 10
```

#### Escena
Un ogro escribió un `catch` que se traga todo. Ahora, cuando hay un error de verdad (un nombre mal escrito en el código), el programa no dice nada y no se entiende qué pasa.

#### Gheco sugiere
Un `catch` que ataja **todo** y no avisa también esconde los errores que no esperabas, como una variable mal escrita: el programa no anda y no se sabe por qué.

Lo sano es manejar solo los errores que conocés, y a los demás **volver a lanzarlos** para que se vean:

```js
catch (error) {
    if (error instanceof SinStock) { … }
    else throw error;
}
```

Cuando aparezca el error escondido, leelo: dice qué nombre no existe y en qué línea.

#### Desafío
Hacé que el error escondido aparezca, y después arreglalo (está en `mandar`: `destno`).

#### Código inicial
```javascript
class FlechaPerdida extends Error {}

function mandar(destino) {
  if (destino === 'la Niebla') throw new FlechaPerdida('niebla');
  return `Llegó a ${destno}`;
}

try {
  console.log(mandar('el Puerto'));
} catch (error) {
  // el ogro se lo traga todo
}
console.log('Fin');
```

#### Salida esperada
```
Llegó a el Puerto
Fin
```

#### Solución
```javascript
class FlechaPerdida extends Error {}

function mandar(destino) {
  if (destino === 'la Niebla') throw new FlechaPerdida('niebla');
  return `Llegó a ${destino}`;
}

try {
  console.log(mandar('el Puerto'));
} catch (error) {
  if (error instanceof FlechaPerdida) console.log('Se perdió en la niebla');
  else throw error;
}
console.log('Fin');
```

#### Al superarla
El esqueleto escondido sale a la luz (*destno no existe*), Nima lo arregla, y la flecha llega al Puerto. El ogro se queda sin escondite.

#### Imagen
- Un ogro torpe de feria (sin armas) con la boca llena de papelitos de error, sorprendido.
- Nima saca un papelito de su boca con dos dedos; Gheco se ríe.

### Micro-misión R04-N06-P5 · Reintentar

```meta
lugar: El libro de Saeta
personajes: Nima, Gheco, Saeta
carta: Reintentos | un for con try adentro · break si salió bien · si se acaban los intentos, lanzar el último error
recompensa: xp 15, monedas 5
```

#### Escena
Las flechas a la Torre de los Vientos se pierden muchas veces, pero tarde o temprano llegan. Saeta las manda hasta 3 veces antes de rendirse.

#### Gheco sugiere
**Reintentar** es probar otra vez si algo falló. Se hace con un `for` que cuenta los intentos, y adentro un `try`:

- si sale bien, `return` con el resultado: la función termina y no hay más vueltas;
- si falla, el `catch` avisa y el `for` sigue con el próximo intento.

Si el `for` termina sin que ningún intento haya salido bien, recién ahí, abajo del `for`, la función se rinde con un `throw`. Fijate en la consigna el texto exacto del aviso de cada intento.

#### Desafío
Completá la función. (La flecha de prueba se pierde en los intentos 1 y 2, y llega en el 3.)

#### Código inicial
```javascript
function mandar(destino, intento) {
  return new Promise((resolve, reject) => {
    setTimeout(() => (intento < 3 ? reject(new Error('viento')) : resolve(`Llegó a ${destino}`)), 500);
  });
}

async function mandarConReintentos(destino) {

}

console.log(await mandarConReintentos('la Torre de los Vientos'));
```

#### Salida esperada
```
Intento 1 falló: viento
Intento 2 falló: viento
Llegó a la Torre de los Vientos
```

#### Solución
```javascript
function mandar(destino, intento) {
  return new Promise((resolve, reject) => {
    setTimeout(() => (intento < 3 ? reject(new Error('viento')) : resolve(`Llegó a ${destino}`)), 500);
  });
}

async function mandarConReintentos(destino) {
  for (let intento = 1; intento <= 3; intento++) {
    try {
      return await mandar(destino, intento);
    } catch (error) {
      console.log(`Intento ${intento} falló: ${error.message}`);
    }
  }
  throw new Error('Se rindió');
}

console.log(await mandarConReintentos('la Torre de los Vientos'));
```

#### Al superarla
A la tercera, la flecha llega. Saeta guarda el arco con un gruñido satisfecho. —Hay que saber insistir —dice—. Pero no para siempre.

#### Imagen
- Tres flechas de luz hacia una torre lejana entre ráfagas de viento: dos desviadas y una que llega.
- Saeta con la capa volando por el viento; Nima la sostiene del brazo.

### Micro-misión R04-N06-P6 · finally: el farol siempre se apaga

```meta
lugar: El libro de Saeta
personajes: Nima, Gheco, Saeta, Lumina
carta: finally | corre siempre: haya salido bien, mal, o con un return en el medio
recompensa: xp 15, monedas 5
```

#### Escena
Cada vez que sale una flecha, Saeta prende el farol de la galería; al terminar, **siempre** hay que apagarlo, salga bien o mal. Pero cuando hay un error, el farol queda prendido toda la noche.

#### Gheco sugiere
Lo que tiene que pasar **siempre**, salga bien o mal (apagar una luz, cerrar algo, sacar un «cargando»), va en el `finally`. Si lo ponés al final del `try`, no corre cuando hay error: el error salta directo al `catch` y lo que quedaba abajo se pierde.

Buscá dónde se apaga el farol y movelo al lugar que corre siempre.

#### Desafío
Que el farol quede apagado después de los dos envíos.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; text-align: center; }
  #farol { width: 60px; height: 60px; border-radius: 50%; background: #333; margin: 0 auto; }
  #farol.prendido { background: #ffd400; box-shadow: 0 0 30px #ffd400; }
</style>
<div id="farol"></div>
<ul id="registro"></ul>
```

#### Estado
```
#farol @class
#registro li
```

#### Código inicial
```javascript
const farol = document.querySelector('#farol');
const anotar = (t) => document.querySelector('#registro').insertAdjacentHTML('beforeend', `<li>${t}</li>`);

async function enviar(url) {
  farol.classList.add('prendido');
  try {
    const respuesta = await fetch(url);
    if (!respuesta.ok) throw new Error(`contestó ${respuesta.status}`);
    anotar(`${url}: bien`);
    farol.classList.remove('prendido');
  } catch (error) {
    anotar(`${url}: ${error.message}`);
  }
}

await enviar('/puerto/hola');
await enviar('/puerto/error');
```

#### Salida esperada
```
── Estado ──
#farol @class: (vacío)
#registro li: /puerto/hola: bien
#registro li: /puerto/error: contestó 500
```

#### Solución
```javascript
const farol = document.querySelector('#farol');
const anotar = (t) => document.querySelector('#registro').insertAdjacentHTML('beforeend', `<li>${t}</li>`);

async function enviar(url) {
  farol.classList.add('prendido');
  try {
    const respuesta = await fetch(url);
    if (!respuesta.ok) throw new Error(`contestó ${respuesta.status}`);
    anotar(`${url}: bien`);
  } catch (error) {
    anotar(`${url}: ${error.message}`);
  } finally {
    farol.classList.remove('prendido');
  }
}

await enviar('/puerto/hola');
await enviar('/puerto/error');
```

#### Al superarla
El farol de la galería se apaga solo después de cada envío, bueno o malo. Lumina, que cuida cada luz de la Feria, se lo agradece a Nima con una reverencia.

#### Imagen
- El farol de la galería de la torre apagándose suavemente después de que sale una flecha.
- Lumina (luciérnaga enorme, alas de vidrio) hace una reverencia; Nima se pone colorada.

## R04-N07 · Iteradores y generadores

```meta
tipo: tema
padre: R04-N06
precio: 10
criatura: orc
temas: func.iteradores
```

### Crónica

En el sótano de la Torre, Saeta guarda el **carcaj infinito**: un carcaj que nunca se vacía, porque no tiene las flechas guardadas: las **fabrica** una por una, recién cuando alguien saca la siguiente.

—Así funcionan los generadores —dice {mentor}—. No hacen toda la lista de una vez: te dan el próximo valor cuando lo pedís, y se acuerdan de dónde quedaron.

### Objetivos

- Entender qué recorre un `for…of`: cualquier cosa **iterable**.
- Escribir generadores con `function*` y `yield`.
- Pedir valores a mano con `.next()`.
- Hacer generadores infinitos y tomar solo los que hacen falta.
- Hacer que una clase propia se pueda recorrer con `for…of` (`[Symbol.iterator]`).

### Antes de empezar

- R01-N04 (bucles) y R03-N05 (closures).

### Explicación

#### Un generador
```javascript
function* carcaj() {
  yield 'flecha roja';
  yield 'flecha verde';
  yield 'flecha azul';
}
for (const flecha of carcaj()) console.log(flecha);
```
`yield` entrega un valor y **pausa** la función hasta que le pidan el próximo.

#### A mano
```javascript
const c = carcaj();
c.next();   // { value: 'flecha roja', done: false }
c.next();   // { value: 'flecha verde', done: false }
```

#### Infinito
```javascript
function* numerar() {
  let n = 1;
  while (true) yield n++;    // no se cuelga: solo avanza cuando le piden
}
```
Se usa con cuidado: con `break`, o tomando una cantidad.

#### Clases que se recorren
```javascript
class Carcaj {
  constructor(flechas) { this.flechas = flechas; }
  *[Symbol.iterator]() {
    for (const f of this.flechas) yield f;
  }
}
for (const f of new Carcaj(['a', 'b'])) …
[...new Carcaj(['a', 'b'])];   // también con spread
```

### Código de ejemplo

```javascript
function* numerarFlechas(prefijo) {
  let n = 1;
  while (true) {
    yield `${prefijo}-${n}`;
    n++;
  }
}

const carcaj = numerarFlechas('NIMA');
console.log(carcaj.next().value, carcaj.next().value);

for (const flecha of numerarFlechas('SAETA')) {
  if (flecha === 'SAETA-4') break;
  console.log(flecha);
}

class Ronda {
  constructor(...tiradores) {
    this.tiradores = tiradores;
  }
  *[Symbol.iterator]() {
    for (const t of this.tiradores) yield `turno de ${t}`;
  }
}
console.log([...new Ronda('Nima', 'Bruno', 'Tati')]);
```

### Salida esperada

```
NIMA-1 NIMA-2
SAETA-1
SAETA-2
SAETA-3
[ 'turno de Nima', 'turno de Bruno', 'turno de Tati' ]
```

### ¿Para qué sirve?

Para recorrer cosas grandes sin cargarlas enteras (los renglones de un archivo enorme, los resultados de una búsqueda página por página), para generar secuencias (identificadores, turnos, oleadas de enemigos) y para que tus propias estructuras se recorran con `for…of` como si fueran arreglos.

### Errores habituales

**Orco: el generador infinito sin corte.** `[...numerar()]` intenta hacer una lista infinita y no termina (en la caja se corta).

**Slime: olvidarse el `*`.** `function carcaj() { yield 1; }` da `SyntaxError`: `yield` solo va en un `function*`.

**Ogro: reusar un generador terminado.** Un generador se recorre una sola vez; para empezar de nuevo, llamá otra vez a la función.

### Micro-misión R04-N07-P1 · El carcaj de tres

```meta
lugar: El sótano de la Torre
personajes: Nima, Gheco, Saeta
carta: function* y yield | function* g() { yield a; yield b; } · for (const x of g()) los recorre
recompensa: xp 10, oro 10
```

#### Escena
Saeta le da a Nima un carcaj chiquito que fabrica tres flechas, de a una: roja, verde y azul.

#### Gheco sugiere
Un **generador** es una función que va entregando valores **de a uno**, cuando se los piden. Se escribe con un asterisco (`function*`), y cada `yield` (*entregar*) da un valor y deja la función **en pausa** hasta que pidan el próximo:

```js
function* semaforo() {
    yield 'verde';
    yield 'amarillo';
    yield 'rojo';
}
for (const luz of semaforo()) {
    console.log(luz);
}
```

El `for…of` pide uno por vuelta hasta que se terminan.

#### Desafío
Completá el generador.

#### Código inicial
```javascript
function* carcaj() {

}

for (const flecha of carcaj()) {
  console.log('Sale la flecha', flecha);
}
```

#### Salida esperada
```
Sale la flecha roja
Sale la flecha verde
Sale la flecha azul
```

#### Solución
```javascript
function* carcaj() {
  yield 'roja';
  yield 'verde';
  yield 'azul';
}

for (const flecha of carcaj()) {
  console.log('Sale la flecha', flecha);
}
```

#### Al superarla
Cada vez que Nima mete la mano, aparece una flecha nueva, de otro color. A la cuarta, el carcaj está vacío.

#### Imagen
- Un sótano de piedra con un carcaj de cuero que brilla por dentro, y tres flechas de colores (roja, verde y azul) saliendo de a una.
- Nima saca una flecha; Saeta sostiene un farol.

### Micro-misión R04-N07-P2 · De a una, a mano

```meta
lugar: El sótano de la Torre
personajes: Nima, Gheco, Saeta
carta: next() | const g = gen(); g.next() → { value, done } · done es true cuando se terminó
recompensa: xp 10, oro 10
```

#### Escena
Saeta quiere ver cómo funciona por dentro: sacar las flechas a mano, de a una, y ver cuándo se termina.

#### Gheco sugiere
Lo que devuelve un generador se puede pedir **a mano**, con `.next()`. Cada llamada da un objeto con dos datos:

- `value`: el valor entregado;
- `done`: `false` mientras quedan, y `true` cuando ya no hay más (y ahí `value` es `undefined`).

```js
const s = semaforo();
console.log(s.next());   // { value: 'verde', done: false }
```

Llamalo una vez más de las que hay `yield`, y mirá qué da la última.

#### Desafío
Mostrá los cuatro resultados de `next()`.

#### Código inicial
```javascript
function* carcaj() {
  yield 'roja';
  yield 'verde';
  yield 'azul';
}

const c = carcaj();

```

#### Salida esperada
```
{ value: 'roja', done: false }
{ value: 'verde', done: false }
{ value: 'azul', done: false }
{ value: undefined, done: true }
```

#### Solución
```javascript
function* carcaj() {
  yield 'roja';
  yield 'verde';
  yield 'azul';
}

const c = carcaj();
console.log(c.next());
console.log(c.next());
console.log(c.next());
console.log(c.next());
```

#### Al superarla
La cuarta vez, el carcaj contesta `done: true` y se queda quieto. Saeta lo cuelga en la pared.

#### Imagen
- Un carcaj de cuero vacío colgado de un clavo en la pared de piedra del sótano, con una etiqueta de cartón.
- Gheco asoma la cabeza adentro del carcaj para comprobar que no queda nada.

### Micro-misión R04-N07-P3 · El carcaj infinito

```meta
lugar: El sótano de la Torre
personajes: Nima, Gheco, Saeta
criatura: orc
carta: Generador infinito | while (true) yield … · no se cuelga: solo avanza cuando le piden · cortá con break
recompensa: xp 10, oro 10
```

#### Escena
El carcaj infinito de Saeta numera las flechas: 1, 2, 3… para siempre. Nima necesita solo las primeras 5.

#### Gheco sugiere
Como el generador se pausa en cada `yield`, puede tener un bucle **que no termina nunca** (`while (true)`) sin colgar el programa: solo da el próximo valor cuando se lo piden.

`n++` usa el valor de `n` y **después** le suma uno: `yield n++` entrega el actual y deja listo el siguiente.

Quien lo recorre es el que decide cuándo parar, con `break` (sale del `for…of`).

#### Desafío
Mostrá `Flecha 1` a `Flecha 5`.

#### Código inicial
```javascript
function* numerar() {

}

for (const n of numerar()) {

  console.log(`Flecha ${n}`);
}
```

#### Salida esperada
```
Flecha 1
Flecha 2
Flecha 3
Flecha 4
Flecha 5
```

#### Solución
```javascript
function* numerar() {
  let n = 1;
  while (true) yield n++;
}

for (const n of numerar()) {
  if (n > 5) break;
  console.log(`Flecha ${n}`);
}
```

#### Al superarla
El carcaj infinito da cinco flechas y espera, paciente, por si alguien quiere la sexta.

#### Imagen
- Un carcaj enorme y antiguo con flechas de luz numeradas brotando de adentro, en el sótano de la torre.
- Nima con cinco flechas en la mano; un orco chiquito de feria (sin armas) mira el carcaj con ganas de sacar más.

### Micro-misión R04-N07-P4 · Tomar las que hacen falta

```meta
lugar: El sótano de la Torre
personajes: Nima, Gheco, Saeta
carta: Generadores que reciben otros | function* tomar(n, gen) { for (const x of gen) { if (n-- <= 0) return; yield x; } }
recompensa: xp 10, oro 10
```

#### Escena
Saeta quiere una herramienta para sacar **N** flechas de cualquier carcaj, infinito o no.

#### Gheco sugiere
Un generador puede **recorrer a otro** y entregar solo algunos de sus valores. Adentro, un `for…of` sobre el otro, un `yield` por cada uno y una cuenta de cuántos van; `return` en un generador lo **termina**, aunque el otro siga teniendo.

`[...algo]` (el *spread* de R01) junta todo lo que entrega un generador en un arreglo. Pensá también qué pasa si piden cero.

#### Desafío
Completá `tomar` para que `[...tomar(3, numerar())]` dé `[ 1, 2, 3 ]`.

#### Código inicial
```javascript
function* numerar() {
  let n = 1;
  while (true) yield n++;
}

function* tomar(cantidad, carcaj) {

}

console.log([...tomar(3, numerar())]);
console.log([...tomar(10, ['a', 'b'])]);
```

#### Salida esperada
```
[ 1, 2, 3 ]
[ 'a', 'b' ]
```

#### Solución
```javascript
function* numerar() {
  let n = 1;
  while (true) yield n++;
}

function* tomar(cantidad, carcaj) {
  if (cantidad <= 0) return;
  for (const flecha of carcaj) {
    yield flecha;
    cantidad--;
    if (cantidad === 0) return;
  }
}

console.log([...tomar(3, numerar())]);
console.log([...tomar(10, ['a', 'b'])]);
```

#### Al superarla
—Sirve hasta con un carcaj común —se sorprende Saeta—. De dos flechas, te da las dos, y no se queja.

#### Imagen
- Una pinza de bronce sacando flechas de dos carcajes distintos, uno enorme y brillante y otro chiquito.
- Saeta sostiene la pinza; Nima cuenta.

### Micro-misión R04-N07-P5 · La ronda de tiradores

```meta
lugar: El sótano de la Torre
personajes: Nima, Gheco, Saeta
carta: [Symbol.iterator] | *[Symbol.iterator]() { for (…) yield … } en una clase · se recorre con for…of y con [...obj]
recompensa: xp 15, monedas 5
```

#### Escena
Para el torneo de tiro, Saeta arma una `Ronda` con los tiradores. Quiere recorrerla con `for…of` como si fuera un arreglo.

#### Gheco sugiere
El `for…of` puede recorrer un objeto propio si la clase le enseña **cómo**: con un método especial que se llama `[Symbol.iterator]`. Si se escribe con asterisco, es un generador, y lo que entrega con `yield` es lo que recorre el `for…of`:

```js
class Fila {
    constructor(...personas) { this.personas = personas; }
    *[Symbol.iterator]() {
        for (const p of this.personas) yield p.toUpperCase();
    }
}
for (const p of new Fila('ana', 'leo')) console.log(p);   // ANA, LEO
```

`...personas` en los parámetros junta todos los datos que lleguen en un arreglo.

#### Desafío
Hacé que la ronda se pueda recorrer.

#### Código inicial
```javascript
class Ronda {
  constructor(...tiradores) {
    this.tiradores = tiradores;
  }

}

const ronda = new Ronda('Nima', 'Bruno', 'Tati');
for (const turno of ronda) {
  console.log(turno);
}
console.log([...ronda].length);
```

#### Salida esperada
```
turno de Nima
turno de Bruno
turno de Tati
3
```

#### Solución
```javascript
class Ronda {
  constructor(...tiradores) {
    this.tiradores = tiradores;
  }

  *[Symbol.iterator]() {
    for (const t of this.tiradores) yield `turno de ${t}`;
  }
}

const ronda = new Ronda('Nima', 'Bruno', 'Tati');
for (const turno of ronda) {
  console.log(turno);
}
console.log([...ronda].length);
```

#### Al superarla
El torneo arranca: Nima, Bruno, Tati, en ronda. Saeta lleva la cuenta con la misma clase, sin un solo índice.

#### Imagen
- Tres tiradores en fila frente a blancos de paja en el campo de tiro de la torre: Nima, Bruno (gorra al revés) y Tati (dos colitas).
- Saeta da la señal con un banderín.

### Micro-misión R04-N07-P6 · Las oleadas de luciérnagas

```meta
lugar: El sótano de la Torre
personajes: Nima, Gheco, Saeta, Lumina
carta: Generadores con estado | el generador recuerda dónde quedó · cada yield puede calcular el próximo valor
recompensa: xp 15, monedas 5
```

#### Escena
Lumina organiza el vuelo de las luciérnagas para la Gran Noche: en cada oleada salen el doble que en la anterior, empezando con 1. Quiere ver las primeras 6 oleadas.

#### Gheco sugiere
Juntá lo del nodo: un generador infinito que va cambiando su número en cada vuelta, y un recorrido que lleva su propia cuenta y corta con `break`.

`*=` multiplica y guarda (`x *= 3` es `x = x * 3`). Pensá el orden adentro del `while`: primero se entrega el número que hay y después se cambia, así el primero que sale es el inicial.

#### Desafío
Mostrá `Oleada 1: 1` hasta `Oleada 6: 32`.

#### Código inicial
```javascript
function* oleadas() {

}

let numero = 1;
for (const cantidad of oleadas()) {

}
```

#### Salida esperada
```
Oleada 1: 1
Oleada 2: 2
Oleada 3: 4
Oleada 4: 8
Oleada 5: 16
Oleada 6: 32
```

#### Solución
```javascript
function* oleadas() {
  let cantidad = 1;
  while (true) {
    yield cantidad;
    cantidad *= 2;
  }
}

let numero = 1;
for (const cantidad of oleadas()) {
  console.log(`Oleada ${numero}: ${cantidad}`);
  if (numero === 6) break;
  numero++;
}
```

#### Al superarla
Seis oleadas de luciérnagas, cada una el doble que la anterior, suben desde el sótano y llenan la Torre de luz. Lumina vuela en el medio. —Para la Gran Noche —dice— vamos a necesitar todas.

#### Imagen
- Oleadas de luciérnagas cada vez más numerosas subiendo en espiral por el interior de una torre de piedra.
- Lumina (luciérnaga enorme, alas de vidrio, luz amarilla en el pecho) en el centro de la espiral; Nima y Saeta miran desde la escalera.

## R04-N08 · Jefe: el Troll de las Respuestas Cruzadas

```meta
tipo: jefe
padre: R04-N07
precio: 10
criatura: dragon
insignia: Flecha de Regreso
insignia_descripcion: Venciste al Troll de las Respuestas Cruzadas: sabés esperar sin quedarte quieta.
usa: conc.async, js.fetch, err.excepciones, web.sesiones
```

### Crónica

La noche anterior a la Gran Noche, las flechas empiezan a volver **cruzadas**: la respuesta del clima trae los puestos, la de los puestos trae un mensaje viejo, y el perfil de Nima dice que es Bruno. Abajo de la Torre, sentado sobre un montón de flechas robadas, ríe el **Troll de las Respuestas Cruzadas**: un troll gordo, de pelo enredado como un nido de hilos, que se mete en el medio del camino de las flechas y les cambia el orden.

—Las flechas no se cruzan solas —dice Saeta—. Se cruzan porque alguien las suelta sin esperar, o usa la respuesta de una para otra. Hoy le ganás con todo lo que aprendiste.

### Objetivos

- Integrar lo de la rama: promesas, `async`/`await`, `fetch`, `Promise.all`, errores propios y cancelación.
- Usar la sesión del Puerto: iniciar sesión, pedir el perfil y cerrar sesión, en orden.
- Que la respuesta vieja no pise a la nueva (la última búsqueda manda).

### Antes de empezar

- Todos los nodos de la Torre de las Flechas (R04-N01 a R04-N07).

### Explicación

#### Las trampas del Troll
| El Troll hace… | Cómo se le gana |
|---|---|
| usar la respuesta antes de que llegue | `await` antes de usarla |
| soltar de a una lo que puede ir junto | `Promise.all` |
| que un 404 parezca una respuesta buena | revisar `respuesta.ok` |
| que la búsqueda vieja llegue después y pise la nueva | cancelar la anterior (`AbortController`) o ignorar las respuestas viejas |
| pedir el perfil antes de iniciar sesión | `await` del login antes del perfil |

#### La sesión del Puerto
El Puerto simulado tiene sesión: `POST /puerto/login` con `{ usuario: 'nima', clave: 'luciernaga' }` guarda una **cookie HttpOnly** (JavaScript no la ve, pero viaja sola en los pedidos siguientes); `GET /puerto/perfil` contesta 401 si no hay sesión; `POST /puerto/salir` la borra. Mirala en el Tablero.

### Micro-misión R04-N08-P1 · El perfil cruzado

```meta
lugar: Al pie de la Torre
personajes: Nima, Gheco, el Troll de las Respuestas Cruzadas
criatura: troll
carta: Trampa 1 | el login se espera antes de pedir el perfil · la cookie de sesión viaja sola
recompensa: xp 15, monedas 3
```

#### Escena
El Troll soltó el login y el perfil a la vez. El perfil llega antes que el login y el Puerto contesta 401: *Primero iniciá sesión*.

#### Gheco sugiere
El servidor sabe **quién sos** por una **cookie**: un dato chiquito que te da al iniciar sesión y que el navegador le devuelve solo en cada pedido. Hasta que no inicies sesión, no la tenés, y el servidor no sabe quién pide.

Por eso el orden importa: el pedido que inicia la sesión tiene que **terminar** (con `await`) antes de pedir lo que necesita la sesión. Si salen los dos a la vez, el segundo llega sin cookie. Después de ejecutar, mirá las cookies en el **Tablero**.

#### Desafío
Que se vea `Sesión de Nima · 12 fichas` y que en las cookies quede la sesión.

#### Estado
```
cookies
```

#### Código inicial
```javascript
const login = fetch('/puerto/login', { method: 'POST', body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }) });
const perfil = await fetch('/puerto/perfil');
const datos = await perfil.json();
console.log(perfil.ok ? `Sesión de ${datos.nombre} · ${datos.fichas} fichas` : `Error: ${datos.error}`);
```

#### Salida esperada
```
Sesión de Nima · 12 fichas
── Estado ──
cookies: sesion=farol-7f3a (HttpOnly)
```

#### Solución
```javascript
await fetch('/puerto/login', { method: 'POST', body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }) });
const perfil = await fetch('/puerto/perfil');
const datos = await perfil.json();
console.log(perfil.ok ? `Sesión de ${datos.nombre} · ${datos.fichas} fichas` : `Error: ${datos.error}`);
```

#### Al superarla
El perfil llega con el nombre correcto. El Troll suelta una de las flechas robadas, enojado.

#### Imagen
- Al pie de una torre finita de noche, un troll gordo de pelo enredado como un nido de hilos (sin armas, con chaleco remendado) sentado sobre un montón de flechas de luz robadas.
- Nima (trenza negra con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas, arco verde) lo enfrenta con una flecha en la mano.

### Micro-misión R04-N08-P2 · La búsqueda vieja

```meta
lugar: Al pie de la Torre
personajes: Nima, Gheco, Saeta, el Troll de las Respuestas Cruzadas
criatura: troll
carta: Trampa 2 | al empezar una búsqueda nueva, cancelá la anterior · la última manda
recompensa: xp 15, monedas 3
```

#### Escena
En la galería hay un buscador de puestos. Nima busca el puesto 1 y enseguida el 2. Pero la respuesta del 1 llega **después** (el Troll la frenó) y pisa la del 2: el cartel dice *Tiro al blanco* aunque buscó el 2.

#### Gheco sugiere
Si se piden dos cosas seguidas y la primera es **más lenta**, puede volver **después** que la segunda y pisar el cartel con un dato viejo.

La salida: cada búsqueda nueva **cancela la anterior** con su `AbortController` (de R04-N05). Guardá el controlador en una variable afuera, y al empezar una búsqueda, cancelá el que había. `?.` (de R01) llama a `abort` solo si hay uno: la primera vez, no hay.

La cancelada lanza un `AbortError`: atajalo y no hagas nada con él.

#### Desafío
Que el cartel muestre el último puesto buscado. (La comprobación busca el 1 —que tarda 800 ms— y enseguida el 2 —que tarda 200 ms—.)

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; text-align: center; }
  button { font-size: 18px; margin: 4px; padding: 6px 14px; }
  #cartel { font-size: 22px; color: #ffd400; }
</style>
<button data-id="1" data-demora="800">Puesto 1</button> <button data-id="2" data-demora="200">Puesto 2</button>
<p id="cartel">Buscá un puesto</p>
```

#### Eventos
```
click [data-id="1"]
esperar 100
click [data-id="2"]
esperar 1000
```

#### Estado
```
#cartel
pedidos
```

#### Código inicial
```javascript
const cartel = document.querySelector('#cartel');
let anterior = null;

async function buscar(id, demora) {
  try {
    const respuesta = await fetch(`/puerto/puestos/${id}?demora=${demora}`);
    const puesto = await respuesta.json();
    cartel.textContent = puesto.nombre;
  } catch (error) {
    if (error.name !== 'AbortError') cartel.textContent = 'Error';
  }
}

document.addEventListener('click', (evento) => {
  const boton = evento.target.closest('[data-id]');
  if (boton) buscar(boton.dataset.id, boton.dataset.demora);
});
```

#### Salida esperada
```
── Estado ──
#cartel: Pan con miel
pedidos: GET /puerto/puestos/1?demora=800 → cancelado
pedidos: GET /puerto/puestos/2?demora=200 → 200
```

#### Solución
```javascript
const cartel = document.querySelector('#cartel');
let anterior = null;

async function buscar(id, demora) {
  anterior?.abort();
  const control = new AbortController();
  anterior = control;
  try {
    const respuesta = await fetch(`/puerto/puestos/${id}?demora=${demora}`, { signal: control.signal });
    const puesto = await respuesta.json();
    cartel.textContent = puesto.nombre;
  } catch (error) {
    if (error.name !== 'AbortError') cartel.textContent = 'Error';
  }
}

document.addEventListener('click', (evento) => {
  const boton = evento.target.closest('[data-id]');
  if (boton) buscar(boton.dataset.id, boton.dataset.demora);
});
```

#### Al superarla
La flecha vieja se pliega en el aire antes de llegar, y el cartel muestra *Pan con miel*, el puesto que Nima buscó último. El Troll pierde otra flecha.

#### Imagen
- Dos flechas de luz en el cielo: una plegándose y cayendo, otra llegando derecha a la galería de la torre.
- El troll de pelo enredado intenta atrapar la flecha que cae; Saeta lo mira desde arriba.

### Micro-misión R04-N08-P3 · La Gran Noche

```meta
lugar: Al pie de la Torre
personajes: Nima, Gheco, Saeta, Lumina, Nilo, el Troll de las Respuestas Cruzadas
criatura: dragon
carta: El jefe | login con await · varios pedidos juntos con Promise.all · errores propios · ok y status · finally · cerrar sesión
recompensa: xp 30, oro 30, monedas 4
item: Flecha de Regreso
```

#### Escena
La última pelea. Para preparar la Gran Noche, Nima tiene que hacer todo el envío en orden, sin que el Troll cruce nada:
1. iniciar sesión en el Puerto;
2. pedir **a la vez** el perfil, el clima y los puestos;
3. dejar un mensaje para Nilo;
4. y cerrar la sesión **siempre**, salga bien o mal.

Si algo falla, tiene que decir exactamente qué.

#### Gheco sugiere
Junta todo lo de R04:

- el **error propio** (R04-N06) ya está hecho, con el código de estado y el mensaje del Puerto;
- `pedir` hace el `fetch`, lee el JSON, revisa `ok` y **lanza** ese error si salió mal (R04-N04);
- los pasos en orden con `await`, y los que no dependen uno de otro, juntos con `Promise.all` (R04-N05);
- el `try`/`catch`/`finally`, con el cierre de sesión en el lugar que corre siempre.

Compará tu salida con la de la consigna línea por línea.

#### Desafío
Completá `pedir` y `granNoche` para que la salida sea:
- `Sesión iniciada`
- `Nima tiene 12 fichas · 18 grados · 3 puestos abiertos`
- `Mensaje 3 para Nilo`
- `Sesión cerrada`
- `Error del Puerto (401): Usuario o clave incorrectos.`
- `Sesión cerrada`

#### Estado
```
cookies
```

#### Código inicial
```javascript
class ErrorDelPuerto extends Error {
  constructor(status, mensaje) {
    super(mensaje);
    this.name = 'ErrorDelPuerto';
    this.status = status;
  }
}

async function pedir(url, opciones = {}) {
  // fetch; si no está ok, lanzá ErrorDelPuerto con el status y datos.error; si está ok, devolvé los datos

}

const comoJSON = (datos) => ({ method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(datos) });

async function granNoche(clave) {
  try {
    // 1. login (usuario 'nima' y la clave)
    // 2. perfil, clima y puestos a la vez
    // 3. el mensaje para Nilo (POST /puerto/mensajes con de: 'Nima', texto: 'Te espero en la Gran Noche')

  } catch (error) {
    if (error instanceof ErrorDelPuerto) console.log(`Error del Puerto (${error.status}): ${error.message}`);
    else throw error;
  } finally {
    // 4. cerrar la sesión siempre (POST /puerto/salir) y mostrar 'Sesión cerrada'

  }
}

await granNoche('luciernaga');
await granNoche('fuego');
```

#### Salida esperada
```
Sesión iniciada
Nima tiene 12 fichas · 18 grados · 3 puestos abiertos
Mensaje 3 para Nilo
Sesión cerrada
Error del Puerto (401): Usuario o clave incorrectos.
Sesión cerrada
── Estado ──
cookies: (ninguna)
```

#### Solución
```javascript
class ErrorDelPuerto extends Error {
  constructor(status, mensaje) {
    super(mensaje);
    this.name = 'ErrorDelPuerto';
    this.status = status;
  }
}

async function pedir(url, opciones = {}) {
  const respuesta = await fetch(url, opciones);
  const datos = await respuesta.json();
  if (!respuesta.ok) throw new ErrorDelPuerto(respuesta.status, datos.error);
  return datos;
}

const comoJSON = (datos) => ({ method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(datos) });

async function granNoche(clave) {
  try {
    await pedir('/puerto/login', comoJSON({ usuario: 'nima', clave }));
    console.log('Sesión iniciada');
    const [perfil, clima, puestos] = await Promise.all([pedir('/puerto/perfil'), pedir('/puerto/clima'), pedir('/puerto/puestos')]);
    const abiertos = puestos.filter((p) => p.abierto).length;
    console.log(`${perfil.nombre} tiene ${perfil.fichas} fichas · ${clima.temperatura} grados · ${abiertos} puestos abiertos`);
    const mensaje = await pedir('/puerto/mensajes', comoJSON({ de: 'Nima', texto: 'Te espero en la Gran Noche' }));
    console.log(`Mensaje ${mensaje.id} para Nilo`);
  } catch (error) {
    if (error instanceof ErrorDelPuerto) console.log(`Error del Puerto (${error.status}): ${error.message}`);
    else throw error;
  } finally {
    await pedir('/puerto/salir', { method: 'POST' });
    console.log('Sesión cerrada');
  }
}

await granNoche('luciernaga');
await granNoche('fuego');
```

#### Al superarla
Todas las flechas salen y vuelven en su orden, ninguna cruzada. El Troll de las Respuestas Cruzadas se queda sin nada que robar; se levanta del montón de flechas, se rasca el nido de hilos que tiene por pelo y se va caminando hacia la Niebla. Entre las flechas que deja hay una que brilla distinto: vuelve sola a la mano de quien la suelta. **La Flecha de Regreso**.

Esa noche, del Puerto llega una flecha que nadie pidió. Es de Nilo: *¡Ahí estaré! Y… ¿vos sos la arquera del Valle? Acá llegó hace mucho un papel con tu nombre.*

{mentor} prende la punta de la Torre, que se ve desde toda la Feria. Al fondo de la Avenida, en el taller del Vidriero, se enciende una tercera ventana.

#### Imagen
- La punta de una torre finita de feria iluminada como un faro amarillo, de noche, con flechas de luz saliendo ordenadas hacia el sur.
- Nima (trenza negra con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas, arco verde) atrapa una flecha que vuelve sola; Saeta (pelo blanco en rodete, capa gris) a su lado.
- Abajo, el troll de pelo enredado se aleja hacia un banco de niebla; arriba, Lumina (luciérnaga enorme con alas de vidrio) ilumina la torre.
