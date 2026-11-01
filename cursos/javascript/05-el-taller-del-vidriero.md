# RAMA R05 · El Taller del Vidriero: canvas y el juego

```meta
tipo: tronco
posicion: 5
```

## R05-N01 · Dibujar en el lienzo

```meta
tipo: tema
padre: R04-N08
precio: 10
criatura: slime
temas: js.canvas
```

### Crónica

Con tres ventanas encendidas, el **taller del Vidriero** ya no está a oscuras. Lucio le da a Nima la llave, oxidada, que guardó treinta años. Adentro hay mesas llenas de vidrios de colores, herramientas finísimas, planos enrollados y, en el fondo, tapado con una lona, **un marco de vitral vacío**, idéntico al del balcón del portal.

Sobre una mesa hay un cuadro de vidrio liso, en blanco, con un marco de bronce. —Es su **lienzo** —dice {mentor}—. El Vidriero dibujaba ahí antes de cortar el vidrio: líneas, círculos, colores. Con JavaScript se dibuja igual: píxel por píxel, en un `<canvas>`.

### Objetivos

- Obtener el contexto 2D de un `<canvas>` con `getContext('2d')`.
- Entender las coordenadas: el (0, 0) está arriba a la izquierda y la *y* crece hacia abajo.
- Dibujar rectángulos (`fillRect`, `strokeRect`), círculos (`arc`), líneas (`moveTo`, `lineTo`) y texto (`fillText`).
- Elegir colores con `fillStyle` y `strokeStyle`, y borrar con `clearRect`.

### Antes de empezar

- R02 (la página) y R01-N04 (bucles).

### Explicación

#### El lienzo y su pincel
```html
<canvas id="lienzo" width="300" height="150"></canvas>
```
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');   // el «pincel» para dibujar en 2D
```

#### Las coordenadas
El punto (0, 0) es la **esquina de arriba a la izquierda**. La *x* crece hacia la derecha y la *y* **hacia abajo**. Un lienzo de 300 × 150 va de (0, 0) a (300, 150).

#### Rectángulos y color
```javascript
ctx.fillStyle = '#ffd400';          // el color de relleno
ctx.fillRect(10, 20, 50, 30);       // x, y, ancho, alto
ctx.strokeStyle = 'white';
ctx.strokeRect(70, 20, 50, 30);     // solo el borde
ctx.clearRect(0, 0, 300, 150);      // borrar (todo el lienzo)
```

#### Círculos, líneas y texto
```javascript
ctx.beginPath();
ctx.arc(150, 75, 20, 0, Math.PI * 2);   // centro x, centro y, radio, ángulo inicial, ángulo final
ctx.fill();

ctx.beginPath();
ctx.moveTo(0, 0);
ctx.lineTo(300, 150);
ctx.stroke();

ctx.fillText('Hola', 10, 140);
```
Cada figura nueva empieza con `beginPath()`.

> **En la plataforma.** El lienzo se ve arriba de la Salida. Para comprobar, la caja anota **lo que dibujaste** (cada `fillRect`, `arc`, `fill` con su color): en el Estado aparece como `lienzo: fillRect(10, 20, 50, 30) #ffd400`.

### Código de ejemplo

```javascript
document.body.innerHTML = '<canvas width="300" height="150"></canvas>';
const ctx = document.querySelector('canvas').getContext('2d');

ctx.fillStyle = '#0b1020';
ctx.fillRect(0, 0, 300, 150);

ctx.fillStyle = '#ffd400';
ctx.fillRect(20, 20, 60, 60);

ctx.strokeStyle = '#4fc3f7';
ctx.lineWidth = 4;
ctx.strokeRect(100, 20, 60, 60);

ctx.fillStyle = '#e53935';
ctx.beginPath();
ctx.arc(220, 50, 30, 0, Math.PI * 2);
ctx.fill();

console.log('Ancho:', ctx.canvas.width, '· Alto:', ctx.canvas.height);
console.log('Último color de relleno:', ctx.fillStyle);
```

### Salida esperada

```
Ancho: 300 · Alto: 150
Último color de relleno: #e53935
```

### ¿Para qué sirve?

Canvas es donde se dibujan los juegos del navegador, los gráficos, los editores de imágenes y las animaciones. No tiene elementos como el DOM: es una superficie donde vos decidís cada píxel, cuadro por cuadro.

### Errores habituales

**Slime: `getContext('2D')` con mayúscula.** Da `null`. Es `'2d'`.

**Ogro: la *y* al revés.** Para dibujar algo «más arriba», la *y* tiene que ser **más chica**.

**Ogro: olvidarse el `beginPath()`.** Los círculos nuevos se suman al camino anterior y se dibujan todos juntos, con el último color.

**Orco: el tamaño con CSS.** Si cambiás el tamaño del canvas con CSS y no con `width`/`height`, el dibujo se estira. El tamaño de dibujo va en los atributos.

### Micro-misión R05-N01-P1 · El primer vidrio

```meta
lugar: El taller del Vidriero
personajes: Nima, Gheco, Lucio
carta: fillRect | const ctx = canvas.getContext('2d') · ctx.fillStyle = 'color' · ctx.fillRect(x, y, ancho, alto)
recompensa: xp 10, oro 10
```

#### Escena
Lucio le muestra a Nima cómo trabajaba el Vidriero: primero dibujaba cada vidrio en el lienzo, del tamaño justo. Nima prueba con un vidrio amarillo.

#### Gheco sugiere
Un `<canvas>` (*lienzo*) es un rectángulo de la página donde el programa **dibuja** con órdenes, como con un pincel. Para dibujar se le pide el **contexto 2D**: el pincel.

```js
const ctx = document.querySelector('#hoja').getContext('2d');
ctx.fillStyle = '#e53935';         // el color de relleno: rojo
ctx.fillRect(10, 20, 60, 40);      // un rectángulo relleno
```

`fillRect(x, y, ancho, alto)`: los dos primeros números dicen **dónde** va la esquina de arriba a la izquierda y los otros dos, **qué tamaño** tiene. Primero se elige el color y después se dibuja: el color queda puesto para lo que siga.

Los colores se escriben en hexadecimal: `#` y seis cifras (rojo, verde y azul).

#### Desafío
Dibujá un cuadrado amarillo (`#ffd400`) en (50, 25), de 100 × 100.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="150"></canvas>
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');

```

#### Salida esperada
```
── Estado ──
lienzo: fillRect(50, 25, 100, 100) #ffd400
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
ctx.fillStyle = '#ffd400';
ctx.fillRect(50, 25, 100, 100);
```

#### Al superarla
Un cuadrado amarillo aparece en el lienzo. Lucio le pasa la mano por encima, como si fuera un vidrio de verdad. —Así empezaba siempre.

#### Imagen
- El interior de un taller de vidriero abandonado, con mesas llenas de vidrios de colores, herramientas finas y planos enrollados, iluminado por faroles.
- Un lienzo de vidrio liso con marco de bronce sobre una mesa, con un cuadrado amarillo dibujado.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) dibuja con el dedo; Lucio (farolero viejo, gorra de lana) mira emocionado.

### Micro-misión R05-N01-P2 · Dónde está el cero

```meta
lugar: El taller del Vidriero
personajes: Nima, Gheco
carta: Coordenadas | (0, 0) es arriba a la izquierda · x crece a la derecha · y crece hacia ABAJO
recompensa: xp 10, oro 10
```

#### Escena
En el plano del Vidriero, las cuatro esquinas del lienzo tienen un vidrito rojo de 20 × 20. Nima tiene que ubicarlos en un lienzo de 200 × 150.

#### Gheco sugiere
En el lienzo, el punto `(0, 0)` es la esquina de **arriba a la izquierda**. La `x` crece hacia la derecha y la `y` crece **hacia abajo** (al revés que en matemática).

Como `fillRect` ubica la esquina de arriba a la izquierda del rectángulo, para que uno quede pegado al borde derecho hay que **restarle su ancho** al ancho del lienzo:

```js
// lienzo de 300 de ancho, cuadrado de 50: pegado a la derecha
ctx.fillRect(300 - 50, 0, 50, 50);
```

Con el borde de abajo pasa lo mismo, con el alto.

#### Desafío
Completá las cuatro esquinas en este orden: arriba a la izquierda, arriba a la derecha, abajo a la izquierda, abajo a la derecha.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="150"></canvas>
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
ctx.fillStyle = '#e53935';
ctx.fillRect(0, 0, 20, 20);
ctx.fillRect(___, ___, 20, 20);
ctx.fillRect(___, ___, 20, 20);
ctx.fillRect(___, ___, 20, 20);
```

#### Salida esperada
```
── Estado ──
lienzo: fillRect(0, 0, 20, 20) #e53935
lienzo: fillRect(180, 0, 20, 20) #e53935
lienzo: fillRect(0, 130, 20, 20) #e53935
lienzo: fillRect(180, 130, 20, 20) #e53935
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
ctx.fillStyle = '#e53935';
ctx.fillRect(0, 0, 20, 20);
ctx.fillRect(180, 0, 20, 20);
ctx.fillRect(0, 130, 20, 20);
ctx.fillRect(180, 130, 20, 20);
```

#### Al superarla
Los cuatro vidrios rojos marcan las esquinas, como en el plano. Gheco se sienta en el medio, exactamente en (100, 75), y no se mueve.

#### Imagen
- Un lienzo de vidrio con marco de bronce con cuatro vidritos rojos en las esquinas, sobre un plano enrollado.
- Gheco (gecko de luz cian con antiparras) sentado en el centro del lienzo.

### Micro-misión R05-N01-P3 · Los círculos del rosetón

```meta
lugar: El taller del Vidriero
personajes: Nima, Gheco, Lucio
carta: arc | ctx.beginPath(); ctx.arc(x, y, radio, 0, Math.PI * 2); ctx.fill(); · cada figura, con su beginPath
recompensa: xp 10, oro 10
```

#### Escena
En el centro del marco del vitral va un rosetón: un círculo grande violeta y, encima, uno chico amarillo.

#### Gheco sugiere
Un círculo se dibuja en tres pasos:

1. `ctx.beginPath()` empieza una figura nueva (si no, se mezcla con la anterior);
2. `ctx.arc(x, y, radio, 0, Math.PI * 2)` marca el círculo: el **centro**, el **radio**, y de dónde a dónde va la vuelta (de 0 a `Math.PI * 2` es la vuelta entera);
3. `ctx.fill()` lo rellena con el color del `fillStyle`.

```js
ctx.beginPath();
ctx.fillStyle = '#43a047';
ctx.arc(60, 60, 30, 0, Math.PI * 2);
ctx.fill();
```

Lo que se dibuja después queda **encima**: el orden importa.

#### Desafío
Dibujá los dos círculos: el grande `#7e57c2`, de radio 50 con centro en (100, 75), y encima el chico `#ffd400`, de radio 20 en el mismo centro.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="150"></canvas>
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');

```

#### Salida esperada
```
── Estado ──
lienzo: arc(100, 75, 50, 0, 6.28)
lienzo: fill() #7e57c2
lienzo: arc(100, 75, 20, 0, 6.28)
lienzo: fill() #ffd400
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');

ctx.beginPath();
ctx.fillStyle = '#7e57c2';
ctx.arc(100, 75, 50, 0, Math.PI * 2);
ctx.fill();

ctx.beginPath();
ctx.fillStyle = '#ffd400';
ctx.arc(100, 75, 20, 0, Math.PI * 2);
ctx.fill();
```

#### Al superarla
El rosetón brilla en el lienzo: violeta afuera, amarillo adentro. Lucio dice que el Vidriero lo dibujaba igual, sin compás, de memoria.

#### Imagen
- Un rosetón circular dibujado en el lienzo de vidrio: un círculo violeta grande con uno amarillo adentro, como un ojo.
- Lucio lo mira con nostalgia; Nima sostiene un pincel de luz.

### Micro-misión R05-N01-P4 · El slime del 2D

```meta
lugar: El taller del Vidriero
personajes: Nima, Gheco
criatura: slime
carta: getContext('2d') | con minúscula · con '2D' devuelve null y la línea siguiente explota
recompensa: xp 10, oro 10
```

#### Escena
Un slime se metió en el tintero del Vidriero y cambió una letra: ahora el pincel no aparece y el programa explota con `Cannot set properties of null`.

#### Gheco sugiere
Si `getContext` recibe un nombre que no conoce, no da error: devuelve `null`. Y después, en la primera línea que usa el pincel, salta `Cannot read properties of null`.

El nombre del contexto es exacto, con mayúsculas y minúsculas: revisalo letra por letra.

#### Desafío
Arreglá el programa para que dibuje el vidrio verde.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="150"></canvas>
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2D');
ctx.fillStyle = '#43a047';
ctx.fillRect(40, 40, 120, 70);
```

#### Salida esperada
```
── Estado ──
lienzo: fillRect(40, 40, 120, 70) #43a047
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
ctx.fillStyle = '#43a047';
ctx.fillRect(40, 40, 120, 70);
```

#### Al superarla
El vidrio verde aparece y el slime sale del tintero, manchado de tinta, ofendido.

#### Imagen
- Un tintero de vidrio volcado sobre una mesa de taller con un slime verde chiquito saliendo, manchado de tinta.
- En el lienzo de al lado, un rectángulo verde recién dibujado; Gheco limpia el tintero.

### Micro-misión R05-N01-P5 · La fila de vidrios

```meta
lugar: El taller del Vidriero
personajes: Nima, Gheco, Lucio
carta: Dibujar con bucles | un for que cambia la x en cada vuelta · un arreglo de colores
recompensa: xp 15, monedas 5
```

#### Escena
El borde de abajo del vitral es una fila de vidrios de colores, todos del mismo tamaño, separados por un poquito.

#### Gheco sugiere
Para dibujar varias cosas en fila, la posición se calcula con el **índice** (la posición en el arreglo: 0, 1, 2…): el primero va en el punto de partida y cada uno se corre un paso más.

```js
for (let i = 0; i < 4; i++) {
    ctx.fillRect(5 + i * 25, 10, 20, 20);   // x: 5, 30, 55, 80
}
```

El paso (25) es el ancho del cuadrado más el espacio entre uno y otro. `forEach((color, i) => …)` da a la vez el elemento y su índice.

#### Desafío
Dibujá un vidrio por color, en fila: cada uno de 30 × 30, a la altura `y = 100`; el primero en `x = 10` y cada uno 40 píxeles más a la derecha que el anterior.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="210" height="150"></canvas>
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const colores = ['#e53935', '#fb8c00', '#ffd400', '#43a047', '#1e88e5'];

```

#### Salida esperada
```
── Estado ──
lienzo: fillRect(10, 100, 30, 30) #e53935
lienzo: fillRect(50, 100, 30, 30) #fb8c00
lienzo: fillRect(90, 100, 30, 30) #ffd400
lienzo: fillRect(130, 100, 30, 30) #43a047
lienzo: fillRect(170, 100, 30, 30) #1e88e5
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const colores = ['#e53935', '#fb8c00', '#ffd400', '#43a047', '#1e88e5'];

colores.forEach((color, i) => {
  ctx.fillStyle = color;
  ctx.fillRect(10 + i * 40, 100, 30, 30);
});
```

#### Al superarla
Cinco vidrios de colores en fila, como un arco iris cortado en pedacitos. Lucio los cuenta dos veces.

#### Imagen
- Una fila de vidrios de colores (rojo, naranja, amarillo, verde, azul) dibujados en el lienzo de bronce.
- Lucio los cuenta con el dedo; Gheco salta de vidrio en vidrio.

### Micro-misión R05-N01-P6 · El boceto del vitral

```meta
lugar: El taller del Vidriero
personajes: Nima, Gheco, Lumina
carta: Todo junto | fondo con fillRect · figuras con arc · líneas con moveTo/lineTo y stroke · texto con fillText
recompensa: xp 15, monedas 5
```

#### Escena
Entre los planos, Lumina encuentra un boceto a medio hacer del vitral del portal: un fondo azul noche, un sol amarillo en el centro, cuatro rayos y la firma del Vidriero abajo. Le pide a Nima que lo pase al lienzo.

#### Gheco sugiere
Para las **líneas**:

- `ctx.strokeStyle` es el color del trazo y `ctx.lineWidth`, su grosor;
- `ctx.beginPath()`, `ctx.moveTo(x, y)` (apoyar el lápiz sin dibujar), `ctx.lineTo(x, y)` (marcar la línea hasta ahí) y `ctx.stroke()` (pasar la tinta).

Para el **texto**: `ctx.fillText('Hola', x, y)`, con el color del `fillStyle`.

El `for` que ya viene recorre los puntos de punta de cada rayo: cada rayo sale del centro del sol.

#### Desafío
Dibujá el boceto en este orden:
1. Fondo `#0d1b3d` en todo el lienzo.
2. Sol `#ffd400`: círculo de radio 25 en (100, 70).
3. Rayos `#ffd400`, de 4 de ancho: líneas del centro a (100, 10), (100, 130), (40, 70) y (160, 70).
4. Texto `#ffffff` `'V.'` en (180, 140).

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="150"></canvas>
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');

// 1. fondo
// 2. sol
// 3. rayos
ctx.strokeStyle = '#ffd400';
ctx.lineWidth = 4;
for (const [x, y] of [[100, 10], [100, 130], [40, 70], [160, 70]]) {

}
// 4. la firma
```

#### Salida esperada
```
── Estado ──
lienzo: fillRect(0, 0, 200, 150) #0d1b3d
lienzo: arc(100, 70, 25, 0, 6.28)
lienzo: fill() #ffd400
lienzo: moveTo(100, 70)
lienzo: lineTo(100, 10)
lienzo: stroke() #ffd400
lienzo: moveTo(100, 70)
lienzo: lineTo(100, 130)
lienzo: stroke() #ffd400
lienzo: moveTo(100, 70)
lienzo: lineTo(40, 70)
lienzo: stroke() #ffd400
lienzo: moveTo(100, 70)
lienzo: lineTo(160, 70)
lienzo: stroke() #ffd400
lienzo: fillText('V.', 180, 140) #ffffff
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');

ctx.fillStyle = '#0d1b3d';
ctx.fillRect(0, 0, 200, 150);

ctx.fillStyle = '#ffd400';
ctx.beginPath();
ctx.arc(100, 70, 25, 0, Math.PI * 2);
ctx.fill();

ctx.strokeStyle = '#ffd400';
ctx.lineWidth = 4;
for (const [x, y] of [[100, 10], [100, 130], [40, 70], [160, 70]]) {
  ctx.beginPath();
  ctx.moveTo(100, 70);
  ctx.lineTo(x, y);
  ctx.stroke();
}

ctx.fillStyle = '#ffffff';
ctx.fillText('V.', 180, 140);
```

#### Al superarla
El boceto del Vidriero queda en el lienzo, completo. Lumina se queda mirando la firma, *V.*, mucho rato. —Este es el sol del vitral —dice—. Pero en el vitral de verdad, el sol **gira**.

#### Imagen
- Un boceto de vitral en el lienzo de bronce: fondo azul noche, un sol amarillo con cuatro rayos y una firma chiquita en una esquina (una sola letra V).
- Lumina (luciérnaga enorme, alas de vidrio) lo mira de cerca; Nima a su lado con el pincel de luz.

## R05-N02 · El bucle del juego

```meta
tipo: tema
padre: R05-N01
precio: 10
criatura: troll
temas: js.canvas, juegos.bucle
```

### Crónica

El marco vacío del fondo del taller tiene un mecanismo: engranajes de bronce, un péndulo y un tambor con agujeros. Lucio dice que el Vidriero lo hacía girar y, mientras giraba, el vitral cambiaba **sesenta veces por segundo**: dibujaba, borraba y volvía a dibujar, un poquito movido cada vez.

—Eso es una **animación** —dice {mentor}—. No se mueve nada: se dibuja de nuevo, una y otra vez, muy rápido. En la Feria lo llamamos el **bucle del juego**.

### Objetivos

- Animar con `requestAnimationFrame`: una función que se vuelve a pedir a sí misma en cada cuadro.
- Seguir la receta de cada cuadro: **actualizar** el estado, **borrar** y **dibujar**.
- Usar el tiempo entre cuadros (*delta time*) para que la velocidad no dependa de la compu.
- Hacer rebotar algo en los bordes.

### Antes de empezar

- R05-N01: dibujar en el lienzo.

### Explicación

#### requestAnimationFrame
```javascript
function cuadro(ahora) {          // ahora: los milisegundos desde que empezó la página
  // actualizar, borrar, dibujar
  requestAnimationFrame(cuadro);  // pedir el próximo cuadro
}
requestAnimationFrame(cuadro);
```
El navegador llama a `cuadro` unas 60 veces por segundo, justo antes de pintar la pantalla.

#### Actualizar, borrar, dibujar
```javascript
let x = 0;
function cuadro() {
  x += 2;                                   // 1. actualizar
  ctx.clearRect(0, 0, ancho, alto);         // 2. borrar
  ctx.fillRect(x, 50, 20, 20);              // 3. dibujar
  requestAnimationFrame(cuadro);
}
```
Sin el `clearRect`, el cuadrado deja una estela.

#### Delta time
Una compu rápida puede dar 120 cuadros por segundo y una lenta 30. Si sumás «2 por cuadro», en una va el doble de rápido. Por eso se mueve **por segundo**:
```javascript
let antes = 0;
function cuadro(ahora) {
  const dt = (ahora - antes) / 1000;   // segundos desde el cuadro anterior
  antes = ahora;
  x += velocidad * dt;                  // velocidad en píxeles por segundo
  …
}
```

#### Rebotar
```javascript
if (x < 0 || x + lado > ancho) vx = -vx;
```

> **En la plataforma.** En la caja, el reloj es de la Feria: 60 cuadros por segundo exactos, siempre iguales. La comprobación corre la animación un rato (por ejemplo, `cuadros 30`) y revisa lo que quedó dibujado en el **último cuadro**.

### Código de ejemplo

```javascript
document.body.innerHTML = '<canvas width="300" height="100"></canvas>';
const ctx = document.querySelector('canvas').getContext('2d');
let x = 0;
let antes = 0;
const velocidad = 120;   // píxeles por segundo
let cuadros = 0;

function cuadro(ahora) {
  const dt = (ahora - antes) / 1000;
  antes = ahora;
  x += velocidad * dt;
  ctx.clearRect(0, 0, 300, 100);
  ctx.fillRect(x, 40, 20, 20);
  cuadros++;
  if (ahora < 1000) requestAnimationFrame(cuadro);
  else console.log(`En 1 segundo: ${cuadros} cuadros, x = ${Math.round(x)}`);
}
requestAnimationFrame((t) => {
  antes = t;
  requestAnimationFrame(cuadro);
});
```

### Salida esperada

```
En 1 segundo: 59 cuadros, x = 118
```

### ¿Para qué sirve?

Todo juego del navegador, toda animación de canvas, todo gráfico que se mueve funciona con este bucle. Los motores de juego (Phaser, Godot, Unity) hacen lo mismo por dentro: actualizar, dibujar, repetir.

### Errores habituales

**Troll: el bucle con `while`.** Un `while (true)` para animar congela la página: nunca le deja pintar. Siempre `requestAnimationFrame`.

**Ogro: olvidarse el `clearRect`.** El dibujo deja estela.

**Troll: llamar `requestAnimationFrame(cuadro())`.** Con paréntesis se llama ya, y después le pasa `undefined`.

**Ogro: moverse por cuadro y no por segundo.** En otra compu el juego va más rápido o más lento.

### Micro-misión R05-N02-P1 · El vidrio que se mueve

```meta
lugar: El mecanismo del vitral
personajes: Nima, Gheco, Lucio
carta: requestAnimationFrame | function cuadro() { … requestAnimationFrame(cuadro); } · actualizar, borrar, dibujar
recompensa: xp 10, oro 10
```

#### Escena
Nima da vuelta la manivela del mecanismo y un vidrio amarillo empieza a correr por el riel del marco.

#### Gheco sugiere
Una **animación** es una serie de dibujos (*cuadros*) que cambian un poquito cada vez, tan rápido que el ojo ve movimiento.

`requestAnimationFrame(funcion)` le pide al navegador que llame a la función **antes del próximo cuadro** (unas 60 veces por segundo). Si la función, al final, se pide a sí misma otra vez, queda un **bucle del juego**:

```js
let y = 0;
function cuadro() {
    y += 1;                              // 1. cambiar
    ctx.clearRect(0, 0, 100, 100);       // 2. borrar todo
    ctx.fillRect(40, y, 10, 10);         // 3. dibujar
    requestAnimationFrame(cuadro);       // 4. pedir el próximo
}
requestAnimationFrame(cuadro);
```

`clearRect(x, y, ancho, alto)` borra esa parte del lienzo; con el tamaño entero, lo deja limpio.

#### Desafío
Completá `cuadro`: en cada cuadro, el vidrio avanza 2 píxeles a la derecha y se dibuja de 20 × 20 a la altura 40. (La comprobación corre 30 cuadros.)

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="100"></canvas>
```

#### Eventos
```
cuadros 30
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
ctx.fillStyle = '#ffd400';
let x = 0;

function cuadro() {

}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 200, 100)
lienzo: fillRect(60, 40, 20, 20) #ffd400
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
ctx.fillStyle = '#ffd400';
let x = 0;

function cuadro() {
  x += 2;
  ctx.clearRect(0, 0, 200, 100);
  ctx.fillRect(x, 40, 20, 20);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
El vidrio amarillo corre por el riel, suave. Lucio aplaude con la gorra en la mano. —¡Se mueve! Treinta años quieto, y se mueve.

#### Imagen
- Un mecanismo de bronce con engranajes, un péndulo y un riel, con un vidrio amarillo deslizándose por el riel.
- Nima gira una manivela; Lucio aplaude con la gorra en la mano.

### Micro-misión R05-N02-P2 · La estela

```meta
lugar: El mecanismo del vitral
personajes: Nima, Gheco
criatura: ogre
carta: clearRect | sin borrar, cada cuadro se dibuja encima del anterior y queda una estela
recompensa: xp 10, oro 10
```

#### Escena
Un ogro movió una línea del mecanismo y ahora el vidrio deja una estela larguísima: el lienzo se llena de amarillo.

#### Gheco sugiere
El lienzo **no se borra solo**: cada dibujo queda pintado encima del anterior. Si en cada cuadro dibujás el vidrio un poco más allá sin borrar, quedan todos los anteriores a la vista, y se ve una **estela**.

Por eso cada cuadro empieza borrando todo con `clearRect` y recién después dibuja. Fijate en el orden.

#### Desafío
Agregá el `clearRect` antes de dibujar.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="100"></canvas>
```

#### Eventos
```
cuadros 20
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
ctx.fillStyle = '#ffd400';
let x = 0;

function cuadro() {
  x += 3;
  ctx.fillRect(x, 40, 20, 20);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 200, 100)
lienzo: fillRect(60, 40, 20, 20) #ffd400
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
ctx.fillStyle = '#ffd400';
let x = 0;

function cuadro() {
  x += 3;
  ctx.clearRect(0, 0, 200, 100);
  ctx.fillRect(x, 40, 20, 20);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
La estela desaparece y queda un solo vidrio, limpio, corriendo. El ogro se lleva su balde de pintura amarilla.

#### Imagen
- Un lienzo de vidrio manchado con una estela amarilla larga, y al lado el mismo lienzo limpio con un solo vidrio.
- Un ogro torpe de feria (sin armas) se va con un balde de pintura amarilla; Nima limpia con un trapo.

### Micro-misión R05-N02-P3 · Por segundo, no por cuadro

```meta
lugar: El mecanismo del vitral
personajes: Nima, Gheco, Lucio
carta: Delta time | dt = (ahora - antes) / 1000 · x += velocidad * dt · velocidad en píxeles por segundo
recompensa: xp 10, oro 10
```

#### Escena
Lucio dice que el Vidriero tenía una regla: el vidrio cruza el riel en **un segundo exacto**, sin importar si la manivela gira rápido o lento.

#### Gheco sugiere
No todas las pantallas dibujan los mismos cuadros por segundo: si el vidrio avanza 2 píxeles **por cuadro**, en una pantalla rápida corre más. Para que vaya igual en todas, se mueve según el **tiempo** que pasó.

La función del cuadro recibe la hora en milisegundos (`ahora`). La diferencia con la del cuadro anterior, pasada a **segundos**, se llama `dt` (*delta de tiempo*):

```js
const dt = (ahora - antes) / 1000;
```

Y la distancia es velocidad por tiempo: si la velocidad está en píxeles **por segundo**, en ese cuadro se avanza `velocidad * dt`.

#### Desafío
Completá el cálculo. (La comprobación corre 60 cuadros: un segundo.)

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="160" height="60"></canvas>
<p id="x" style="color:#fff;font-family:monospace"></p>
```

#### Eventos
```
cuadros 60
```

#### Estado
```
#x
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const velocidad = 120;
let x = 0;
let antes = null;

function cuadro(ahora) {
  if (antes === null) antes = ahora;
  const dt = ___;
  antes = ahora;
  x += ___;
  ctx.clearRect(0, 0, 160, 60);
  ctx.fillRect(x, 20, 20, 20);
  document.querySelector('#x').textContent = `x = ${Math.round(x)}`;
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#x: x = 118
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const velocidad = 120;
let x = 0;
let antes = null;

function cuadro(ahora) {
  if (antes === null) antes = ahora;
  const dt = (ahora - antes) / 1000;
  antes = ahora;
  x += velocidad * dt;
  ctx.clearRect(0, 0, 160, 60);
  ctx.fillRect(x, 20, 20, 20);
  document.querySelector('#x').textContent = `x = ${Math.round(x)}`;
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
El vidrio llega a 118 píxeles en un segundo (el primer cuadro solo mide el tiempo). Lucio lo cronometra con su reloj de bolsillo y asiente.

#### Imagen
- Un reloj de bolsillo abierto al lado del riel del mecanismo, con el vidrio amarillo llegando al final.
- Lucio sostiene el reloj; Nima gira la manivela.

### Micro-misión R05-N02-P4 · El rebote

```meta
lugar: El mecanismo del vitral
personajes: Nima, Gheco, Lucio
carta: Rebotar | si se pasa del borde, la velocidad cambia de signo: vx = -vx
recompensa: xp 10, oro 10
```

#### Escena
El vidrio llega al final del riel y se escapa del marco. El Vidriero lo hacía rebotar: ida y vuelta, sin parar.

#### Gheco sugiere
Para que algo **rebote**, se guarda su velocidad en una variable que puede ser positiva (va a la derecha) o negativa (va a la izquierda). Al tocar un borde, se le **da vuelta el signo**:

```js
vx = -vx;   // si era 4, pasa a -4; si era -4, pasa a 4
```

Pensá cuándo toca cada borde: el izquierdo cuando su `x` es menor que 0, y el derecho cuando su **lado derecho** (`x` más su ancho) pasa el ancho del lienzo.

#### Desafío
Que el vidrio rebote en los dos bordes. (La comprobación corre 70 cuadros.)

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="60"></canvas>
```

#### Eventos
```
cuadros 70
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
ctx.fillStyle = '#4fc3f7';
let x = 0;
let vx = 4;

function cuadro() {
  x += vx;
  // rebotá en los bordes

  ctx.clearRect(0, 0, 200, 60);
  ctx.fillRect(x, 20, 20, 20);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 200, 60)
lienzo: fillRect(88, 20, 20, 20) #4fc3f7
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
ctx.fillStyle = '#4fc3f7';
let x = 0;
let vx = 4;

function cuadro() {
  x += vx;
  if (x < 0 || x + 20 > 200) vx = -vx;
  ctx.clearRect(0, 0, 200, 60);
  ctx.fillRect(x, 20, 20, 20);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
El vidrio va, toca el borde, vuelve. Va, toca, vuelve. Gheco lo sigue con la cabeza hasta marearse.

#### Imagen
- Un vidrio celeste rebotando en los bordes de un marco de bronce, con flechitas de movimiento dibujadas como estela suave.
- Gheco mareado, con los ojos en espiral, sobre el marco.

### Micro-misión R05-N02-P5 · El vidrio que da vueltas

```meta
lugar: El mecanismo del vitral
personajes: Nima, Gheco, Lucio
carta: Movimiento en dos ejes | x e y con su propia velocidad · rebota en los cuatro bordes
recompensa: xp 15, monedas 5
```

#### Escena
Algunos vidrios del vitral no van solo de lado: van en diagonal, rebotando en las cuatro paredes del marco.

#### Gheco sugiere
Para moverse en diagonal se usan **dos** velocidades: `vx` para el costado y `vy` para arriba y abajo. Cada una se revisa con sus bordes y rebota por su cuenta:

- los bordes izquierdo y derecho dan vuelta `vx`;
- los de arriba y abajo dan vuelta `vy`.

Se pueden declarar varias variables en una línea, separadas por comas: `let a = 1, b = 2;`.

#### Desafío
Hacé rebotar el vidrio en los cuatro bordes. (La comprobación corre 40 cuadros.)

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="160" height="100"></canvas>
```

#### Eventos
```
cuadros 40
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
ctx.fillStyle = '#ab47bc';
const lado = 16;
let x = 10, y = 10, vx = 5, vy = 4;

function cuadro() {

  ctx.clearRect(0, 0, 160, 100);
  ctx.fillRect(x, y, lado, lado);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 160, 100)
lienzo: fillRect(80, 2, 16, 16) #ab47bc
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
ctx.fillStyle = '#ab47bc';
const lado = 16;
let x = 10, y = 10, vx = 5, vy = 4;

function cuadro() {
  x += vx;
  y += vy;
  if (x < 0 || x + lado > 160) vx = -vx;
  if (y < 0 || y + lado > 100) vy = -vy;
  ctx.clearRect(0, 0, 160, 100);
  ctx.fillRect(x, y, lado, lado);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
El vidrio violeta rebota en diagonal por todo el marco, como una pelota encerrada. Lucio se ríe: el Vidriero le decía *el inquieto*.

#### Imagen
- Un vidrio violeta rebotando en diagonal dentro de un marco de bronce, con una línea punteada que muestra su recorrido en zigzag.
- Lucio se ríe con la mano en la panza; Nima sigue el vidrio con la mirada.

### Micro-misión R05-N02-P6 · El sol que late

```meta
lugar: El mecanismo del vitral
personajes: Nima, Gheco, Lumina
carta: Animar con el tiempo | Math.sin(ahora / 300) va de -1 a 1 · sirve para latir, oscilar, respirar
recompensa: xp 15, monedas 5
```

#### Escena
Lumina se acuerda: el sol del vitral no estaba quieto, **latía**, como un corazón. Se agrandaba y se achicaba, despacio.

#### Gheco sugiere
`Math.sin` (el seno de matemática) da un número que **sube y baja** entre −1 y 1, una y otra vez, de forma suave. Por eso sirve para todo lo que late, se balancea o respira.

```js
const alto = 30 + 10 * Math.sin(ahora / 500);   // va de 20 a 40 y vuelve
```

- el número de adelante (30) es el tamaño del medio;
- el que multiplica (10) es cuánto se agranda y se achica;
- el que divide a `ahora` (500) es la velocidad: más grande, más lento.

#### Desafío
Hacé latir el sol: en cada cuadro, su radio es `20 + 5 * Math.sin(ahora / 300)`, con centro en (80, 50). (La comprobación corre 45 cuadros.)

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0d1b3d; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="160" height="100"></canvas>
```

#### Eventos
```
cuadros 45
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
ctx.fillStyle = '#ffd400';

function cuadro(ahora) {
  const radio = ___;
  ctx.clearRect(0, 0, 160, 100);
  ctx.beginPath();
  ctx.arc(80, 50, radio, 0, Math.PI * 2);
  ctx.fill();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 160, 100)
lienzo: arc(80, 50, 22.99, 0, 6.28)
lienzo: fill() #ffd400
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
ctx.fillStyle = '#ffd400';

function cuadro(ahora) {
  const radio = 20 + 5 * Math.sin(ahora / 300);
  ctx.clearRect(0, 0, 160, 100);
  ctx.beginPath();
  ctx.arc(80, 50, radio, 0, Math.PI * 2);
  ctx.fill();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
El sol del lienzo late, despacio, como respirando. Lumina se apoya en la mesa y se queda mirándolo. —Así estaba —dice, bajito—. Así estaba el día que se fue.

#### Imagen
- Un sol amarillo dibujado en el lienzo de vidrio, con anillos suaves alrededor que muestran que late.
- Lumina (luciérnaga enorme, alas de vidrio) apoyada en la mesa del taller, mirándolo en silencio; Nima a su lado.

## R05-N03 · El teclado del juego

```meta
tipo: tema
padre: R05-N02
precio: 10
criatura: orc
temas: juegos.entrada, js.eventos
```

### Crónica

Debajo de una lona, Nima encuentra un juguete del Vidriero: un tablero de vidrio con una luciérnaga de cristal adentro, que se movía con cuatro palancas. Las palancas están rotas, pero el dibujo de cómo funcionaba sigue en la tapa.

—En un juego, el teclado no se escucha como en un formulario —dice {mentor}—. No importa **cuándo** apretaste: importa **qué teclas están apretadas ahora**, en cada cuadro.

### Objetivos

- Guardar el **estado** del teclado en un `Set` con `keydown` y `keyup`.
- Mover un personaje en el bucle según las teclas apretadas, con *delta time*.
- Normalizar la diagonal para que no vaya más rápido.
- No salirse de la pantalla (limitar con `Math.max` y `Math.min`).
- Evitar que las flechas muevan la página (`preventDefault`).

### Antes de empezar

- R05-N02 (el bucle) y R02-N04 (las teclas).

### Explicación

#### El estado del teclado
```javascript
const teclas = new Set();
addEventListener('keydown', (e) => teclas.add(e.key));
addEventListener('keyup', (e) => teclas.delete(e.key));
```
En el bucle, se pregunta: `if (teclas.has('ArrowRight')) …`. Así, mientras la tecla esté apretada, se mueve en **cada** cuadro, suave.

#### Mover con delta time
```javascript
let dx = 0, dy = 0;
if (teclas.has('ArrowRight')) dx += 1;
if (teclas.has('ArrowLeft')) dx -= 1;
if (teclas.has('ArrowDown')) dy += 1;
if (teclas.has('ArrowUp')) dy -= 1;
x += dx * velocidad * dt;
y += dy * velocidad * dt;
```

#### La diagonal
Con dos flechas a la vez, `dx = 1` y `dy = 1`: se mueve 1,41 veces más rápido (Pitágoras). Se arregla dividiendo por el largo:
```javascript
if (dx !== 0 && dy !== 0) {
  dx /= Math.SQRT2;
  dy /= Math.SQRT2;
}
```

#### Los bordes
```javascript
x = Math.max(0, Math.min(x, ancho - lado));
```

> **En la plataforma.** Para probar, la comprobación usa `apretar ArrowRight`, `cuadros 30` y `soltar ArrowRight`: mantiene la tecla durante 30 cuadros. En vivo, hacé click en la página y usá el teclado.

### Código de ejemplo

```javascript
document.body.innerHTML = '<canvas width="200" height="200"></canvas>';
const ctx = document.querySelector('canvas').getContext('2d');
const teclas = new Set();
addEventListener('keydown', (e) => teclas.add(e.key));
addEventListener('keyup', (e) => teclas.delete(e.key));

const luz = { x: 90, y: 90, lado: 20, velocidad: 60 };

function mover(dt) {
  let dx = 0, dy = 0;
  if (teclas.has('ArrowRight')) dx += 1;
  if (teclas.has('ArrowDown')) dy += 1;
  if (dx !== 0 && dy !== 0) {
    dx /= Math.SQRT2;
    dy /= Math.SQRT2;
  }
  luz.x = Math.min(luz.x + dx * luz.velocidad * dt, 200 - luz.lado);
  luz.y = Math.min(luz.y + dy * luz.velocidad * dt, 200 - luz.lado);
}

teclas.add('ArrowRight');
teclas.add('ArrowDown');
for (let i = 0; i < 60; i++) mover(1 / 60);
console.log('Diagonal 1 s:', Math.round(luz.x), Math.round(luz.y));

teclas.delete('ArrowDown');
for (let i = 0; i < 120; i++) mover(1 / 60);
console.log('Derecha 2 s más:', Math.round(luz.x), Math.round(luz.y), '(tocó el borde)');
```

### Salida esperada

```
Diagonal 1 s: 132 132
Derecha 2 s más: 180 132 (tocó el borde)
```

### ¿Para qué sirve?

Así se controlan los personajes de todos los juegos: el estado de las teclas (o del joystick, o de la pantalla táctil) se lee en cada cuadro. Es la diferencia entre un personaje que se mueve suave y uno que se mueve a saltitos.

### Errores habituales

**Ogro: mover en el `keydown`.** Se mueve a saltitos y con la demora de repetición del teclado. Guardá el estado y mové en el bucle.

**Ogro: la diagonal rápida.** Sin normalizar, en diagonal se va 1,41 veces más rápido.

**Orco: salirse de la pantalla.** Sin limitar, el personaje desaparece por un costado.

**Esqueleto: `e.key` con otra mayúscula.** Es `'ArrowUp'`, no `'arrowup'`. Y las letras cambian con Mayúsculas: `'w'` no es `'W'`.

### Micro-misión R05-N03-P1 · Las teclas apretadas

```meta
lugar: El juguete del Vidriero
personajes: Nima, Gheco, Lucio
carta: Estado del teclado | const teclas = new Set() · keydown → add(e.key) · keyup → delete(e.key)
recompensa: xp 10, oro 10
```

#### Escena
Para arreglar el juguete, primero hay que saber qué palancas están apretadas en cada momento.

#### Gheco sugiere
En un juego, `keydown` no alcanza: lo que importa es qué teclas están **apretadas ahora**, y puede haber varias a la vez. Se guardan en un **`Set`** (*conjunto*): una colección sin repetidos.

```js
const apretadas = new Set();
apretadas.add('a');       // la agrega (si ya estaba, no la repite)
apretadas.delete('a');    // la saca
apretadas.has('a');       // ¿está? true o false
```

`keydown` pasa al **apretar** y `keyup`, al **soltar**. Para mostrar un `Set`, se pasa a arreglo con `[...conjunto]` y se une con `join(' ')`.

#### Desafío
Completá los dos eventos. (La comprobación aprieta la flecha derecha, después la de arriba, y suelta la derecha.)

#### Página
```html
<style>
  body { font-family: monospace; background: #1a1206; color: #ffd400; padding: 24px; font-size: 20px; }
</style>
<p>Teclas apretadas: <span id="teclas">(ninguna)</span></p>
```

#### Eventos
```
apretar ArrowRight
apretar ArrowUp
soltar ArrowRight
```

#### Estado
```
#teclas
```

#### Código inicial
```javascript
const teclas = new Set();
const mostrar = () => (document.querySelector('#teclas').textContent = [...teclas].join(' ') || '(ninguna)');

addEventListener('keydown', (e) => {

  mostrar();
});
addEventListener('keyup', (e) => {

  mostrar();
});
```

#### Salida esperada
```
── Estado ──
#teclas: ArrowUp
```

#### Solución
```javascript
const teclas = new Set();
const mostrar = () => (document.querySelector('#teclas').textContent = [...teclas].join(' ') || '(ninguna)');

addEventListener('keydown', (e) => {
  teclas.add(e.key);
  mostrar();
});
addEventListener('keyup', (e) => {
  teclas.delete(e.key);
  mostrar();
});
```

#### Al superarla
En el cartel aparece solo `ArrowUp`: la derecha ya se soltó. Lucio dice que así sabía el Vidriero qué palancas tocaba su ayudante.

#### Imagen
- Un tablero de vidrio con cuatro palancas de bronce rotas y un dibujo de flechas en la tapa.
- Nima aprieta dos palancas a la vez; Lucio lee el cartel.

### Micro-misión R05-N03-P2 · La luciérnaga de cristal

```meta
lugar: El juguete del Vidriero
personajes: Nima, Gheco, Lucio
carta: Mover en el bucle | if (teclas.has('ArrowRight')) x += velocidad * dt · cada cuadro, mientras esté apretada
recompensa: xp 10, oro 10
```

#### Escena
Con las palancas arregladas, la luciérnaga de cristal tiene que moverse a la derecha mientras se aprieta la flecha.

#### Gheco sugiere
La idea es separar las dos cosas: los eventos del teclado **solo anotan** qué teclas están apretadas, y el bucle del juego, en cada cuadro, **pregunta** y mueve.

```js
if (apretadas.has('ArrowUp')) {
    nave.y -= nave.velocidad * dt;
}
```

Así el movimiento es parejo mientras la tecla esté apretada, y no depende de cada cuántos milisegundos repite la tecla la compu.

#### Desafío
Mové la luciérnaga a la derecha con la flecha. (La comprobación la mantiene 1 segundo: 60 cuadros.)

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="100"></canvas>
```

#### Eventos
```
apretar ArrowRight
cuadros 60
soltar ArrowRight
cuadros 10
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const teclas = new Set();
addEventListener('keydown', (e) => teclas.add(e.key));
addEventListener('keyup', (e) => teclas.delete(e.key));

const luz = { x: 20, y: 40, velocidad: 60 };
let antes = null;

function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;

  ctx.clearRect(0, 0, 200, 100);
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(Math.round(luz.x), luz.y, 16, 16);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 200, 100)
lienzo: fillRect(79, 40, 16, 16) #ffd400
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const teclas = new Set();
addEventListener('keydown', (e) => teclas.add(e.key));
addEventListener('keyup', (e) => teclas.delete(e.key));

const luz = { x: 20, y: 40, velocidad: 60 };
let antes = null;

function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (teclas.has('ArrowRight')) luz.x += luz.velocidad * dt;
  ctx.clearRect(0, 0, 200, 100);
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(Math.round(luz.x), luz.y, 16, 16);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
La luciérnaga de cristal se desliza a la derecha mientras Nima aprieta, y se queda quieta cuando suelta. Lucio aplaude. —¡Funciona como antes!

#### Imagen
- Una luciérnaga de cristal amarilla deslizándose dentro de un tablero de vidrio, con el reflejo de un farol.
- Nima aprieta una palanca; Lucio aplaude.

### Micro-misión R05-N03-P3 · Las cuatro direcciones

```meta
lugar: El juguete del Vidriero
personajes: Nima, Gheco
carta: dx y dy | sumar 1 o -1 según las teclas · x += dx * velocidad * dt · y += dy * velocidad * dt
recompensa: xp 10, oro 10
```

#### Escena
Ahora las cuatro palancas: arriba, abajo, izquierda y derecha.

#### Gheco sugiere
Una forma prolija de las cuatro flechas: calcular una **dirección** en cada eje, que vale `-1`, `0` o `1`, y mover con ella:

```js
let dx = 0;
if (apretadas.has('ArrowLeft')) dx -= 1;
if (apretadas.has('ArrowRight')) dx += 1;
nave.x += dx * nave.velocidad * dt;
```

Si están apretadas las dos, se anulan y da 0: no se mueve. Con `dy` se hace lo mismo para arriba y abajo (recordá que la `y` crece hacia abajo).

#### Desafío
Mové en las cuatro direcciones. (La comprobación va medio segundo a la izquierda y medio segundo hacia arriba.)

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="200"></canvas>
```

#### Eventos
```
apretar ArrowLeft
cuadros 30
soltar ArrowLeft
apretar ArrowUp
cuadros 30
soltar ArrowUp
cuadros 2
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const teclas = new Set();
addEventListener('keydown', (e) => teclas.add(e.key));
addEventListener('keyup', (e) => teclas.delete(e.key));

const luz = { x: 100, y: 100, velocidad: 60 };
let antes = null;

function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  let dx = 0;
  let dy = 0;
  // sumá o restá según las cuatro flechas

  luz.x += dx * luz.velocidad * dt;
  luz.y += dy * luz.velocidad * dt;
  ctx.clearRect(0, 0, 200, 200);
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(Math.round(luz.x), Math.round(luz.y), 16, 16);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 200, 200)
lienzo: fillRect(71, 70, 16, 16) #ffd400
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const teclas = new Set();
addEventListener('keydown', (e) => teclas.add(e.key));
addEventListener('keyup', (e) => teclas.delete(e.key));

const luz = { x: 100, y: 100, velocidad: 60 };
let antes = null;

function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  let dx = 0;
  let dy = 0;
  if (teclas.has('ArrowRight')) dx += 1;
  if (teclas.has('ArrowLeft')) dx -= 1;
  if (teclas.has('ArrowDown')) dy += 1;
  if (teclas.has('ArrowUp')) dy -= 1;
  luz.x += dx * luz.velocidad * dt;
  luz.y += dy * luz.velocidad * dt;
  ctx.clearRect(0, 0, 200, 200);
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(Math.round(luz.x), Math.round(luz.y), 16, 16);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
La luciérnaga de cristal va adonde Nima quiere: a la izquierda, arriba, en cualquier dirección. Gheco intenta atraparla y no puede.

#### Imagen
- La luciérnaga de cristal moviéndose en el tablero de vidrio, con flechas de bronce en las cuatro direcciones.
- Gheco persiguiéndola por el borde del tablero.

### Micro-misión R05-N03-P4 · El orco del borde

```meta
lugar: El juguete del Vidriero
personajes: Nima, Gheco
criatura: orc
carta: Limitar | x = Math.max(0, Math.min(x, ancho - lado)) · nunca menos que 0 ni más que el borde
recompensa: xp 10, oro 10
```

#### Escena
Un orco empujó la luciérnaga hasta el borde y la hizo desaparecer por el costado del tablero.

#### Gheco sugiere
Para que un número no se salga de un rango se usan dos funciones:

- `Math.max(a, b)` da el **más grande** de los dos: `Math.max(0, x)` nunca deja que `x` baje de 0;
- `Math.min(a, b)` da el **más chico**: `Math.min(x, 100)` nunca deja que pase de 100.

```js
x = Math.max(0, Math.min(x, 100));   // queda entre 0 y 100
```

El tope derecho es el ancho del lienzo **menos el tamaño** de la luciérnaga: su `x` es el lado izquierdo.

#### Desafío
Que la luciérnaga no se salga por la derecha. (La comprobación aprieta la derecha 3 segundos.)

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="60"></canvas>
```

#### Eventos
```
apretar ArrowRight
cuadros 180
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const teclas = new Set();
addEventListener('keydown', (e) => teclas.add(e.key));
addEventListener('keyup', (e) => teclas.delete(e.key));

const luz = { x: 20, y: 20, velocidad: 90 };
let antes = null;

function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (teclas.has('ArrowRight')) luz.x += luz.velocidad * dt;
  // que no se salga

  ctx.clearRect(0, 0, 200, 60);
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(Math.round(luz.x), luz.y, 16, 16);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 200, 60)
lienzo: fillRect(184, 20, 16, 16) #ffd400
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const teclas = new Set();
addEventListener('keydown', (e) => teclas.add(e.key));
addEventListener('keyup', (e) => teclas.delete(e.key));

const luz = { x: 20, y: 20, velocidad: 90 };
let antes = null;

function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (teclas.has('ArrowRight')) luz.x += luz.velocidad * dt;
  luz.x = Math.max(0, Math.min(luz.x, 200 - 16));
  ctx.clearRect(0, 0, 200, 60);
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(Math.round(luz.x), luz.y, 16, 16);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
La luciérnaga llega al borde y se queda ahí, apoyada contra el vidrio. El orco empuja y empuja, pero no pasa.

#### Imagen
- La luciérnaga de cristal apoyada contra el borde derecho del tablero de vidrio.
- Un orco chiquito y torpe de feria (sin armas) empujando del otro lado del vidrio, sin éxito.

### Micro-misión R05-N03-P5 · La diagonal tramposa

```meta
lugar: El juguete del Vidriero
personajes: Nima, Gheco, Lucio
carta: Normalizar | con dx y dy a la vez, dividí los dos por Math.SQRT2 · la velocidad queda igual en todas las direcciones
recompensa: xp 15, monedas 5
```

#### Escena
Bruno descubrió que, apretando dos flechas, la luciérnaga va más rápido. Para el torneo, eso es trampa.

#### Gheco sugiere
Con dos flechas a la vez, se suma un paso entero de costado y otro entero hacia abajo: la diagonal es **más larga** que un paso (por el teorema de Pitágoras, mide `√2`, cerca de 1,41). Por eso va más rápido.

Para que la diagonal mida lo mismo que un paso recto, cuando `dx` y `dy` son los dos distintos de 0 se dividen por `√2`. En JavaScript, `√2` ya viene escrito como `Math.SQRT2`.

#### Desafío
Normalizá la diagonal. (La comprobación aprieta derecha y abajo durante 1 segundo.)

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="200"></canvas>
```

#### Eventos
```
apretar ArrowRight
apretar ArrowDown
cuadros 61
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const teclas = new Set();
addEventListener('keydown', (e) => teclas.add(e.key));
addEventListener('keyup', (e) => teclas.delete(e.key));

const luz = { x: 20, y: 20, velocidad: 60 };
let antes = null;

function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  let dx = 0;
  let dy = 0;
  if (teclas.has('ArrowRight')) dx += 1;
  if (teclas.has('ArrowLeft')) dx -= 1;
  if (teclas.has('ArrowDown')) dy += 1;
  if (teclas.has('ArrowUp')) dy -= 1;
  // normalizá la diagonal

  luz.x += dx * luz.velocidad * dt;
  luz.y += dy * luz.velocidad * dt;
  ctx.clearRect(0, 0, 200, 200);
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(Math.round(luz.x), Math.round(luz.y), 16, 16);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 200, 200)
lienzo: fillRect(62, 62, 16, 16) #ffd400
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const teclas = new Set();
addEventListener('keydown', (e) => teclas.add(e.key));
addEventListener('keyup', (e) => teclas.delete(e.key));

const luz = { x: 20, y: 20, velocidad: 60 };
let antes = null;

function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  let dx = 0;
  let dy = 0;
  if (teclas.has('ArrowRight')) dx += 1;
  if (teclas.has('ArrowLeft')) dx -= 1;
  if (teclas.has('ArrowDown')) dy += 1;
  if (teclas.has('ArrowUp')) dy -= 1;
  if (dx !== 0 && dy !== 0) {
    dx /= Math.SQRT2;
    dy /= Math.SQRT2;
  }
  luz.x += dx * luz.velocidad * dt;
  luz.y += dy * luz.velocidad * dt;
  ctx.clearRect(0, 0, 200, 200);
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(Math.round(luz.x), Math.round(luz.y), 16, 16);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
En diagonal, la luciérnaga ya no corre más que en línea recta. Bruno pierde su ventaja y protesta. Lucio le dice que el Vidriero también le había ganado así una vez.

#### Imagen
- La luciérnaga de cristal moviéndose en diagonal por el tablero, con una regla de bronce al lado midiendo.
- Bruno (gorra al revés, chaleco rojo) protesta; Lucio se ríe.

### Micro-misión R05-N03-P6 · Que la página no se mueva

```meta
lugar: El juguete del Vidriero
personajes: Nima, Gheco, Lumina
carta: preventDefault con teclas | las flechas y la barra mueven la página · en el juego, e.preventDefault() lo evita
recompensa: xp 15, monedas 5
```

#### Escena
Lumina prueba el juguete en una página larga y, cada vez que aprieta una flecha, además de moverse la luciérnaga, se mueve toda la página. Es incómodo.

#### Gheco sugiere
Algunas teclas tienen un trabajo **de fábrica** en el navegador: las flechas y la barra espaciadora mueven la página hacia arriba o abajo. Como en el `submit` de R02, `evento.preventDefault()` lo impide.

Pero solo hay que impedirlo con las teclas **del juego**: si lo hacés con todas, no se puede escribir nada. Un arreglo con las teclas del juego e `includes` (de R01) sirven para preguntar si es una de esas.

#### Desafío
Evitá que las flechas y la barra muevan la página. (La comprobación aprieta derecha, la barra y la letra *a*.)

#### Página
```html
<style>
  body { font-family: monospace; background: #1a1206; color: #ffd400; padding: 24px; font-size: 18px; height: 3000px; }
</style>
<p>Evitadas: <span id="evitadas">0</span></p>
```

#### Eventos
```
tecla ArrowRight
tecla espacio
tecla a
```

#### Estado
```
#evitadas
```

#### Código inicial
```javascript
const DEL_JUEGO = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '];
let evitadas = 0;

addEventListener('keydown', (e) => {

});
```

#### Salida esperada
```
── Estado ──
#evitadas: 2
```

#### Solución
```javascript
const DEL_JUEGO = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '];
let evitadas = 0;

addEventListener('keydown', (e) => {
  if (DEL_JUEGO.includes(e.key)) {
    e.preventDefault();
    evitadas++;
    document.querySelector('#evitadas').textContent = evitadas;
  }
});
```

#### Al superarla
La página se queda quieta y la luciérnaga se mueve sola. Lumina juega diez minutos seguidos sin decir nada. Después se ríe: —Me ganó un juguete.

#### Imagen
- Lumina (luciérnaga enorme, alas de vidrio) jugando con el tablero de vidrio, concentrada, con la luciérnaga de cristal adentro.
- Nima y Gheco la miran divertidos.

## R05-N04 · Colisiones: cuando dos cosas se tocan

```meta
tipo: tema
padre: R05-N03
precio: 10
criatura: orc
temas: juegos.colisiones
```

### Crónica

En un cajón del taller, Nima encuentra un **tablero de gemas**: una caja de vidrio con gemas de colores sueltas adentro. Según el plano de la tapa, la luciérnaga de cristal tenía que **juntarlas**: cada vez que tocaba una, la gema desaparecía y sonaba una campanita.

—Para saber si dos cosas se tocan —dice {mentor}—, no hace falta mirar cada píxel. Alcanza con comparar sus **cajas**.

### Objetivos

- Detectar si dos rectángulos se superponen (colisión AABB).
- Detectar si dos círculos se tocan (por la distancia entre centros).
- Sacar de un arreglo lo que se tocó (juntar gemas) y sumar puntos.
- Hacer la colisión en el bucle, cuadro por cuadro.

### Antes de empezar

- R05-N03: el teclado del juego.

### Explicación

#### Dos rectángulos
Cada cosa tiene su caja: `{ x, y, ancho, alto }`. Dos cajas se tocan si se superponen en las dos direcciones:
```javascript
function chocan(a, b) {
  return a.x < b.x + b.ancho && a.x + a.ancho > b.x
      && a.y < b.y + b.alto && a.y + a.alto > b.y;
}
```
Se lee: «a empieza antes de que termine b, y termina después de que empieza b», en *x* y en *y*.

#### Dos círculos
```javascript
function tocan(c1, c2) {
  const distancia = Math.hypot(c1.x - c2.x, c1.y - c2.y);
  return distancia < c1.radio + c2.radio;
}
```

#### Juntar
```javascript
gemas = gemas.filter((gema) => {
  if (chocan(jugador, gema)) {
    puntos++;
    return false;   // la saca
  }
  return true;      // la deja
});
```

### Código de ejemplo

```javascript
function chocan(a, b) {
  return a.x < b.x + b.ancho && a.x + a.ancho > b.x && a.y < b.y + b.alto && a.y + a.alto > b.y;
}

const luz = { x: 50, y: 50, ancho: 20, alto: 20 };
const gemas = [
  { color: 'roja', x: 60, y: 60, ancho: 10, alto: 10 },
  { color: 'verde', x: 70, y: 50, ancho: 10, alto: 10 },
  { color: 'azul', x: 150, y: 20, ancho: 10, alto: 10 },
];

for (const gema of gemas) {
  console.log(gema.color, chocan(luz, gema) ? 'toca' : 'no toca');
}

let puntos = 0;
const quedan = gemas.filter((gema) => {
  if (chocan(luz, gema)) {
    puntos++;
    return false;
  }
  return true;
});
console.log('Puntos:', puntos, '· Quedan:', quedan.map((g) => g.color));
console.log('Distancia:', Math.hypot(3, 4));
```

### Salida esperada

```
roja toca
verde no toca
azul no toca
Puntos: 1 · Quedan: [ 'verde', 'azul' ]
Distancia: 5
```

### ¿Para qué sirve?

Agarrar monedas, chocar con un enemigo, pisar el piso, que una bala pegue: todo juego es, en el fondo, un montón de preguntas de «¿se tocan?» en cada cuadro. Y no solo en juegos: arrastrar y soltar en una página usa la misma cuenta.

### Errores habituales

**Orco: `<=` en vez de `<`.** Con `<=`, dos cajas que solo se rozan por el borde cuentan como choque.

**Ogro: comparar solo una dirección.** Si comparás solo la *x*, dos cosas en la misma columna pero lejos en altura «chocan».

**Ogro: sacar elementos de un arreglo mientras se recorre con `for`.** Se saltea el siguiente. Usá `filter`.

### Micro-misión R05-N04-P1 · ¿Se tocan?

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco, Lucio
carta: Colisión AABB | a.x < b.x + b.ancho && a.x + a.ancho > b.x && lo mismo con y y alto
recompensa: xp 10, oro 10
```

#### Escena
Según el plano, una gema se junta cuando la caja de la luciérnaga se superpone con la de la gema. Nima tiene que escribir la regla.

#### Gheco sugiere
Dos rectángulos se **tocan** cuando se pisan en el costado **y** también en la altura. En el costado se pisan si cada uno empieza antes de que termine el otro:

```js
const pisanEnX = a.x < b.x + b.ancho && a.x + a.ancho > b.x;
```

- `a.x < b.x + b.ancho`: `a` empieza antes de que termine `b`;
- `a.x + a.ancho > b.x`: `a` termina después de que empieza `b`.

Con la `y` y el alto es igual. Chocan si se cumplen las cuatro comparaciones, unidas con `&&`. Esto se llama colisión de cajas (en inglés, *AABB*).

#### Desafío
Escribí `chocan`.

#### Código inicial
```javascript
function chocan(a, b) {

}

const luz = { x: 50, y: 50, ancho: 20, alto: 20 };
console.log(chocan(luz, { x: 60, y: 60, ancho: 10, alto: 10 }));
console.log(chocan(luz, { x: 70, y: 50, ancho: 10, alto: 10 }));
console.log(chocan(luz, { x: 55, y: 100, ancho: 10, alto: 10 }));
console.log(chocan(luz, { x: 40, y: 40, ancho: 40, alto: 40 }));
```

#### Salida esperada
```
true
false
false
true
```

#### Solución
```javascript
function chocan(a, b) {
  return a.x < b.x + b.ancho && a.x + a.ancho > b.x && a.y < b.y + b.alto && a.y + a.alto > b.y;
}

const luz = { x: 50, y: 50, ancho: 20, alto: 20 };
console.log(chocan(luz, { x: 60, y: 60, ancho: 10, alto: 10 }));
console.log(chocan(luz, { x: 70, y: 50, ancho: 10, alto: 10 }));
console.log(chocan(luz, { x: 55, y: 100, ancho: 10, alto: 10 }));
console.log(chocan(luz, { x: 40, y: 40, ancho: 40, alto: 40 }));
```

#### Al superarla
`true, false, false, true`: la segunda gema solo roza el borde, y no cuenta. Lucio dice que el Vidriero era así de exigente.

#### Imagen
- Una caja de vidrio con gemas de colores y una luciérnaga de cristal, con rectángulos de luz dibujados alrededor de cada cosa.
- Nima los compara con una regla; Lucio mira con una lupa.

### Micro-misión R05-N04-P2 · El orco del borde

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco
criatura: orc
carta: < y no <= | dos cajas que se rozan por el borde no chocan · con <= sí, y eso es un error
recompensa: xp 10, oro 10
```

#### Escena
Un orco cambió los `<` por `<=` y ahora la luciérnaga junta gemas que apenas la rozan, de lejos.

#### Gheco sugiere
Si dos rectángulos están **pegados**, borde con borde (uno termina en 70 y el otro empieza en 70), ¿se tocan? Con `<` y `>` no: `70 < 70` es falso. Con `<=` y `>=` sí, porque `70 <= 70` es verdadero.

En el juego, rozar no cuenta. Compará las comparaciones del código con las de R05-N04-P1.

#### Desafío
Arreglá `chocan` para que la gema que solo roza no cuente.

#### Código inicial
```javascript
function chocan(a, b) {
  return a.x <= b.x + b.ancho && a.x + a.ancho >= b.x && a.y <= b.y + b.alto && a.y + a.alto >= b.y;
}

const luz = { x: 50, y: 50, ancho: 20, alto: 20 };
console.log('Roza:', chocan(luz, { x: 70, y: 50, ancho: 10, alto: 10 }));
console.log('Adentro:', chocan(luz, { x: 55, y: 55, ancho: 10, alto: 10 }));
```

#### Salida esperada
```
Roza: false
Adentro: true
```

#### Solución
```javascript
function chocan(a, b) {
  return a.x < b.x + b.ancho && a.x + a.ancho > b.x && a.y < b.y + b.alto && a.y + a.alto > b.y;
}

const luz = { x: 50, y: 50, ancho: 20, alto: 20 };
console.log('Roza:', chocan(luz, { x: 70, y: 50, ancho: 10, alto: 10 }));
console.log('Adentro:', chocan(luz, { x: 55, y: 55, ancho: 10, alto: 10 }));
```

#### Al superarla
La gema que solo rozaba se queda en su lugar. El orco se queda sin gema robada.

#### Imagen
- Dos gemas de colores en el tablero de vidrio, una tocando apenas el borde de la luciérnaga de cristal.
- Un orco chiquito de feria (sin armas) con las manos vacías y cara de fastidio.

### Micro-misión R05-N04-P3 · Círculos de luz

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco, Lucio
carta: Círculos | Math.hypot(dx, dy) es la distancia · se tocan si la distancia es menor que la suma de los radios
recompensa: xp 10, oro 10
```

#### Escena
Las gemas redondas no tienen esquinas. Para ellas, el plano dice: se tocan si están más cerca que la suma de sus radios.

#### Gheco sugiere
Con **círculos** es más fácil: se tocan si la distancia entre los **centros** es menor que la suma de los **dos radios**.

`Math.hypot(dx, dy)` calcula esa distancia (es Pitágoras: la raíz de `dx² + dy²`), donde `dx` y `dy` son las diferencias entre las `x` y entre las `y` de los centros:

```js
const distancia = Math.hypot(p.x - q.x, p.y - q.y);
```

#### Desafío
Escribí `tocan`.

#### Código inicial
```javascript
function tocan(a, b) {

}

const luz = { x: 100, y: 100, radio: 10 };
console.log(tocan(luz, { x: 115, y: 100, radio: 6 }));
console.log(tocan(luz, { x: 100, y: 130, radio: 6 }));
console.log(tocan(luz, { x: 108, y: 106, radio: 1 }));
```

#### Salida esperada
```
true
false
true
```

#### Solución
```javascript
function tocan(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y) < a.radio + b.radio;
}

const luz = { x: 100, y: 100, radio: 10 };
console.log(tocan(luz, { x: 115, y: 100, radio: 6 }));
console.log(tocan(luz, { x: 100, y: 130, radio: 6 }));
console.log(tocan(luz, { x: 108, y: 106, radio: 1 }));
```

#### Al superarla
Las gemas redondas también tienen su regla. Lucio guarda el compás del Vidriero, que ya no hace falta.

#### Imagen
- Gemas redondas en el tablero de vidrio con círculos de luz alrededor, una tocando la luciérnaga de cristal.
- Lucio guarda un compás de bronce en un estuche.

### Micro-misión R05-N04-P4 · Juntar las gemas

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco, Lucio
carta: Juntar con filter | gemas = gemas.filter((g) => { if (chocan(…)) { puntos++; return false; } return true; })
recompensa: xp 10, oro 10
```

#### Escena
La luciérnaga recorre el tablero: en cada posición, junta las gemas que toca.

#### Gheco sugiere
`filter` (de R01) arma un arreglo **nuevo** con los que cumplen: sirve para **sacar** las gemas que se juntaron, quedándote con las que **no** chocan.

Y la cuenta de puntos se puede hacer comparando largos: lo que había antes menos lo que quedó es cuántas se juntaron.

```js
const antes = frutas.length;
frutas = frutas.filter((f) => !f.comida);
const comidas = antes - frutas.length;
```

Para volver a asignar el arreglo, tiene que estar declarado con `let`.

#### Desafío
Completá `juntar`.

#### Código inicial
```javascript
function chocan(a, b) {
  return a.x < b.x + b.ancho && a.x + a.ancho > b.x && a.y < b.y + b.alto && a.y + a.alto > b.y;
}

const luz = { x: 0, y: 0, ancho: 20, alto: 20 };
let gemas = [
  { x: 25, y: 5, ancho: 8, alto: 8 },
  { x: 60, y: 5, ancho: 8, alto: 8 },
  { x: 95, y: 5, ancho: 8, alto: 8 },
];
let puntos = 0;

function juntar() {

}

for (const x of [0, 20, 40, 60, 80]) {
  luz.x = x;
  juntar();
  console.log(`x = ${x}: ${puntos} puntos, quedan ${gemas.length}`);
}
```

#### Salida esperada
```
x = 0: 0 puntos, quedan 3
x = 20: 1 puntos, quedan 2
x = 40: 1 puntos, quedan 2
x = 60: 2 puntos, quedan 1
x = 80: 3 puntos, quedan 0
```

#### Solución
```javascript
function chocan(a, b) {
  return a.x < b.x + b.ancho && a.x + a.ancho > b.x && a.y < b.y + b.alto && a.y + a.alto > b.y;
}

const luz = { x: 0, y: 0, ancho: 20, alto: 20 };
let gemas = [
  { x: 25, y: 5, ancho: 8, alto: 8 },
  { x: 60, y: 5, ancho: 8, alto: 8 },
  { x: 95, y: 5, ancho: 8, alto: 8 },
];
let puntos = 0;

function juntar() {
  gemas = gemas.filter((gema) => {
    if (chocan(luz, gema)) {
      puntos++;
      return false;
    }
    return true;
  });
}

for (const x of [0, 20, 40, 60, 80]) {
  luz.x = x;
  juntar();
  console.log(`x = ${x}: ${puntos} puntos, quedan ${gemas.length}`);
}
```

#### Al superarla
Tilín, tilín, tilín: las tres campanitas suenan, una por gema. El tablero queda vacío.

#### Imagen
- La luciérnaga de cristal recorriendo el tablero de vidrio y gemas desapareciendo con un destello.
- Lucio sonríe; tres campanitas de bronce cuelgan del borde de la caja.

### Micro-misión R05-N04-P5 · Las gemas en el lienzo

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco, Lucio
carta: Colisión en el bucle | mover · juntar · dibujar lo que queda · mostrar los puntos
recompensa: xp 15, monedas 5
```

#### Escena
Ahora en el lienzo: la luciérnaga se mueve con la flecha derecha, y en cada cuadro junta las gemas que toca.

#### Gheco sugiere
En el bucle del juego, el orden de cada cuadro es siempre el mismo:

1. **mover** (lo que dicen las teclas);
2. **revisar** choques y reglas (juntar);
3. **borrar y dibujar** cómo quedó todo;
4. **mostrar** los números en la página;
5. pedir el próximo cuadro.

Si dibujás antes de juntar, en ese cuadro se ve una gema que ya no está.

#### Desafío
Completá `cuadro`. (La comprobación mantiene la derecha 1 segundo.)

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #ffd400; font-family: monospace; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<p>Puntos: <span id="puntos">0</span></p>
<canvas id="lienzo" width="200" height="60"></canvas>
```

#### Eventos
```
apretar ArrowRight
cuadros 61
soltar ArrowRight
```

#### Estado
```
#puntos
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const teclas = new Set();
addEventListener('keydown', (e) => teclas.add(e.key));
addEventListener('keyup', (e) => teclas.delete(e.key));

const chocan = (a, b) => a.x < b.x + b.ancho && a.x + a.ancho > b.x && a.y < b.y + b.alto && a.y + a.alto > b.y;
const luz = { x: 0, y: 20, ancho: 16, alto: 16 };
let gemas = [40, 100, 160].map((x) => ({ x, y: 24, ancho: 8, alto: 8 }));
let puntos = 0;
let antes = null;

function juntar() {
  gemas = gemas.filter((g) => (chocan(luz, g) ? (puntos++, false) : true));
}

function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (teclas.has('ArrowRight')) luz.x += 120 * dt;
  // juntar, borrar, dibujar las gemas que quedan (#4fc3f7) y la luz (#ffd400), mostrar los puntos

  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#puntos: 2
lienzo: clearRect(0, 0, 200, 60)
lienzo: fillRect(160, 24, 8, 8) #4fc3f7
lienzo: fillRect(120, 20, 16, 16) #ffd400
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const teclas = new Set();
addEventListener('keydown', (e) => teclas.add(e.key));
addEventListener('keyup', (e) => teclas.delete(e.key));

const chocan = (a, b) => a.x < b.x + b.ancho && a.x + a.ancho > b.x && a.y < b.y + b.alto && a.y + a.alto > b.y;
const luz = { x: 0, y: 20, ancho: 16, alto: 16 };
let gemas = [40, 100, 160].map((x) => ({ x, y: 24, ancho: 8, alto: 8 }));
let puntos = 0;
let antes = null;

function juntar() {
  gemas = gemas.filter((g) => (chocan(luz, g) ? (puntos++, false) : true));
}

function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (teclas.has('ArrowRight')) luz.x += 120 * dt;
  juntar();
  ctx.clearRect(0, 0, 200, 60);
  ctx.fillStyle = '#4fc3f7';
  for (const g of gemas) ctx.fillRect(g.x, g.y, g.ancho, g.alto);
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(Math.round(luz.x), luz.y, luz.ancho, luz.alto);
  document.querySelector('#puntos').textContent = puntos;
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
En un segundo, la luciérnaga cruza el tablero y se lleva dos gemas. La tercera, la más lejana, la espera.

#### Imagen
- El lienzo del taller con la luciérnaga amarilla avanzando por una fila de gemas celestes, una desapareciendo en un destello.
- Nima con la mano en una palanca; Gheco cuenta con los dedos.

### Micro-misión R05-N04-P6 · El cofre de las gemas

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco, Lumina
carta: Colisión con varios tipos | cada gema con su valor · chocar con una trampa resta
recompensa: xp 15, monedas 5
```

#### Escena
Lumina mezcla en el cofre gemas de distinto valor y algunas **trampas** (vidrios rotos) que restan puntos. Quiere una función que, para una posición, diga cuánto se gana.

#### Gheco sugiere
Cuando cada cosa vale distinto, ya no alcanza con contar: hay que **sumar el valor** de cada una que se toca. Una forma es recorrer y repartir en dos: las que se tocan suman, las que no se quedan.

```js
let ganado = 0;
cosas = cosas.filter((c) => {
    if (!toca(c)) return true;    // se queda
    ganado += c.valor;
    return false;                 // se va
});
```

Una trampa con valor negativo **resta** sola, sin ningún `if` especial.

#### Desafío
Completá `juntar` para que devuelva lo ganado en cada paso.

#### Código inicial
```javascript
const chocan = (a, b) => a.x < b.x + b.ancho && a.x + a.ancho > b.x && a.y < b.y + b.alto && a.y + a.alto > b.y;
let cosas = [
  { nombre: 'rubí', valor: 5, x: 10, y: 0, ancho: 6, alto: 6 },
  { nombre: 'vidrio roto', valor: -3, x: 30, y: 0, ancho: 6, alto: 6 },
  { nombre: 'zafiro', valor: 3, x: 34, y: 0, ancho: 6, alto: 6 },
  { nombre: 'esmeralda', valor: 4, x: 80, y: 0, ancho: 6, alto: 6 },
];

function juntar(luz) {

}

console.log(juntar({ x: 5, y: 0, ancho: 10, alto: 10 }));
console.log(juntar({ x: 28, y: 0, ancho: 10, alto: 10 }));
console.log(juntar({ x: 50, y: 0, ancho: 10, alto: 10 }));
console.log('Quedan:', cosas.map((c) => c.nombre));
```

#### Salida esperada
```
5
0
0
Quedan: [ 'esmeralda' ]
```

#### Solución
```javascript
const chocan = (a, b) => a.x < b.x + b.ancho && a.x + a.ancho > b.x && a.y < b.y + b.alto && a.y + a.alto > b.y;
let cosas = [
  { nombre: 'rubí', valor: 5, x: 10, y: 0, ancho: 6, alto: 6 },
  { nombre: 'vidrio roto', valor: -3, x: 30, y: 0, ancho: 6, alto: 6 },
  { nombre: 'zafiro', valor: 3, x: 34, y: 0, ancho: 6, alto: 6 },
  { nombre: 'esmeralda', valor: 4, x: 80, y: 0, ancho: 6, alto: 6 },
];

function juntar(luz) {
  let ganado = 0;
  cosas = cosas.filter((cosa) => {
    if (chocan(luz, cosa)) {
      ganado += cosa.valor;
      return false;
    }
    return true;
  });
  return ganado;
}

console.log(juntar({ x: 5, y: 0, ancho: 10, alto: 10 }));
console.log(juntar({ x: 28, y: 0, ancho: 10, alto: 10 }));
console.log(juntar({ x: 50, y: 0, ancho: 10, alto: 10 }));
console.log('Quedan:', cosas.map((c) => c.nombre));
```

#### Al superarla
El rubí suma cinco; el vidrio roto y el zafiro, juntos, apenas cero. Lumina guarda la esmeralda que quedó: —Esa —dice— la vamos a necesitar al final.

#### Imagen
- Un cofre abierto con gemas de colores (un rubí, un zafiro, una esmeralda) y un vidrio roto filoso.
- Lumina (luciérnaga enorme, alas de vidrio) sostiene la esmeralda a la luz; Nima la mira.

## R05-N05 · Enemigos: perseguir y esquivar

```meta
tipo: tema
padre: R05-N04
precio: 10
criatura: goblin
temas: juegos.ia
```

### Crónica

En el tablero de gemas hay también unas figuritas negras: **sombras**. Según el plano, perseguían a la luciérnaga por todo el tablero, y si la tocaban le sacaban una vida. Y salían por **oleadas**: primero una, después dos, después cuatro.

—Un enemigo no piensa —dice {mentor}—: en cada cuadro da un pasito hacia donde está su presa. Con eso alcanza para que parezca que te persigue.

### Objetivos

- Mover un enemigo hacia el jugador: el vector dirección, normalizado.
- Detectar el choque con el jugador y restar vidas, con un tiempo de invulnerabilidad (*cooldown*).
- Lanzar oleadas de enemigos cada vez más grandes.
- Organizar a los enemigos con una clase (`Sombra`) y un arreglo.

### Antes de empezar

- R05-N04 (colisiones) y R03-N01 (clases).

### Explicación

#### Perseguir
```javascript
const dx = jugador.x - enemigo.x;
const dy = jugador.y - enemigo.y;
const largo = Math.hypot(dx, dy);
if (largo > 0) {
  enemigo.x += (dx / largo) * enemigo.velocidad * dt;
  enemigo.y += (dy / largo) * enemigo.velocidad * dt;
}
```
Dividir por el largo da una dirección de largo 1: así el enemigo va a la misma velocidad, esté lejos o cerca.

#### Cooldown
Si el enemigo toca al jugador en 60 cuadros seguidos, le sacaría 60 vidas. Por eso, después de un golpe, el jugador queda un ratito invulnerable:
```javascript
if (chocan(jugador, enemigo) && ahora > jugador.invulnerableHasta) {
  jugador.vidas--;
  jugador.invulnerableHasta = ahora + 1000;   // un segundo
}
```

#### Oleadas
```javascript
let oleada = 1;
function lanzarOleada() {
  for (let i = 0; i < 2 ** (oleada - 1); i++) enemigos.push(new Sombra(…));
  oleada++;
}
```
Cuando no queda ninguno (`enemigos.length === 0`), se lanza la siguiente.

### Código de ejemplo

```javascript
class Sombra {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.velocidad = 30;
  }
  perseguir(objetivo, dt) {
    const dx = objetivo.x - this.x;
    const dy = objetivo.y - this.y;
    const largo = Math.hypot(dx, dy);
    if (largo > 0) {
      this.x += (dx / largo) * this.velocidad * dt;
      this.y += (dy / largo) * this.velocidad * dt;
    }
  }
}

const luz = { x: 100, y: 100 };
const sombra = new Sombra(0, 100);
for (let i = 0; i < 60; i++) sombra.perseguir(luz, 1 / 60);
console.log('Después de 1 s:', Math.round(sombra.x), Math.round(sombra.y));

const otra = new Sombra(100, 0);
for (let i = 0; i < 120; i++) otra.perseguir(luz, 1 / 60);
console.log('Después de 2 s:', Math.round(otra.x), Math.round(otra.y));

const oleadas = [1, 2, 3, 4].map((n) => 2 ** (n - 1));
console.log('Sombras por oleada:', oleadas);
```

### Salida esperada

```
Después de 1 s: 30 100
Después de 2 s: 100 60
Sombras por oleada: [ 1, 2, 4, 8 ]
```

### ¿Para qué sirve?

Casi todos los enemigos de los juegos sencillos hacen esto: ir hacia el jugador, a veces con un poco de azar. Y la idea del *cooldown* (un tiempo de espera después de una acción) aparece en todos lados: disparos, poderes, botones que no se pueden apretar dos veces seguidas.

### Errores habituales

**Goblin: no normalizar.** Sin dividir por el largo, el enemigo va rapidísimo cuando está lejos y lento cuando está cerca.

**Troll: dividir por cero.** Si el enemigo ya está encima (`largo === 0`), `dx / largo` da `NaN` y el enemigo desaparece. Preguntá antes.

**Ogro: el golpe que se repite.** Sin *cooldown*, un toque saca todas las vidas en un segundo.

### Micro-misión R05-N05-P1 · La sombra que persigue

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco, Lucio
carta: Perseguir | dx, dy hacia el objetivo · dividir por Math.hypot(dx, dy) · multiplicar por velocidad * dt
recompensa: xp 10, oro 10
```

#### Escena
Una sombra aparece en una esquina del tablero y empieza a ir hacia la luciérnaga.

#### Gheco sugiere
Para que algo **persiga** a otro, en cada cuadro se mueve un poquito hacia donde está el otro:

1. la **diferencia** en cada eje: `dx = objetivo.x - enemigo.x` (y lo mismo con `y`). Si es positiva, el objetivo está a la derecha;
2. la **distancia** entre los dos, con `Math.hypot(dx, dy)`;
3. dividir `dx` y `dy` por la distancia da una **dirección de largo 1**, y eso por la velocidad y por `dt` es cuánto avanza.

Si la distancia es 0 (ya llegó), no se mueve: dividir por 0 rompe todo.

#### Desafío
Escribí `perseguir`.

#### Código inicial
```javascript
const luz = { x: 100, y: 100 };
const sombra = { x: 0, y: 0, velocidad: 50 };

function perseguir(enemigo, objetivo, dt) {

}

for (let i = 0; i < 60; i++) perseguir(sombra, luz, 1 / 60);
console.log(Math.round(sombra.x), Math.round(sombra.y));
for (let i = 0; i < 300; i++) perseguir(sombra, luz, 1 / 60);
console.log(Math.round(sombra.x), Math.round(sombra.y));
```

#### Salida esperada
```
35 35
100 100
```

#### Solución
```javascript
const luz = { x: 100, y: 100 };
const sombra = { x: 0, y: 0, velocidad: 50 };

function perseguir(enemigo, objetivo, dt) {
  const dx = objetivo.x - enemigo.x;
  const dy = objetivo.y - enemigo.y;
  const largo = Math.hypot(dx, dy);
  if (largo > 1) {
    enemigo.x += (dx / largo) * enemigo.velocidad * dt;
    enemigo.y += (dy / largo) * enemigo.velocidad * dt;
  }
}

for (let i = 0; i < 60; i++) perseguir(sombra, luz, 1 / 60);
console.log(Math.round(sombra.x), Math.round(sombra.y));
for (let i = 0; i < 300; i++) perseguir(sombra, luz, 1 / 60);
console.log(Math.round(sombra.x), Math.round(sombra.y));
```

#### Al superarla
La sombra avanza en diagonal, sin desviarse, hasta quedar pegada a la luciérnaga. Lucio se estremece: —Así era. No paraba nunca.

#### Imagen
- Una figurita negra de sombra avanzando en diagonal por el tablero de vidrio hacia la luciérnaga de cristal amarilla.
- Lucio se abraza a sí mismo con un escalofrío; Nima mira concentrada.

### Micro-misión R05-N05-P2 · El goblin que corre de más

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco
criatura: goblin
carta: Normalizar | sin dividir por el largo, la velocidad depende de la distancia
recompensa: xp 10, oro 10
```

#### Escena
Un goblin se disfrazó de sombra y corre rapidísimo cuando está lejos. Hace trampa: no normaliza.

#### Gheco sugiere
Si se mueve con `dx * velocidad` directamente, corre **más rápido cuanto más lejos está**: `dx` es la distancia entera, no una dirección. De lejos salta, de cerca casi no se mueve.

Para que vaya siempre a la misma velocidad, hay que **normalizar**: dividir `dx` y `dy` por la distancia, así la dirección mide 1 y solo la velocidad dice cuánto avanza.

#### Desafío
Arreglá `perseguir` para que en 1 segundo avance 40 píxeles, esté lejos o cerca.

#### Código inicial
```javascript
function perseguir(enemigo, objetivo, dt) {
  const dx = objetivo.x - enemigo.x;
  const dy = objetivo.y - enemigo.y;
  enemigo.x += dx * enemigo.velocidad * dt;
  enemigo.y += dy * enemigo.velocidad * dt;
}

const lejos = { x: 0, y: 0, velocidad: 40 };
perseguir(lejos, { x: 300, y: 400 }, 1);
console.log('Avanzó:', Math.round(Math.hypot(lejos.x, lejos.y)));
```

#### Salida esperada
```
Avanzó: 40
```

#### Solución
```javascript
function perseguir(enemigo, objetivo, dt) {
  const dx = objetivo.x - enemigo.x;
  const dy = objetivo.y - enemigo.y;
  const largo = Math.hypot(dx, dy);
  if (largo === 0) return;
  enemigo.x += (dx / largo) * enemigo.velocidad * dt;
  enemigo.y += (dy / largo) * enemigo.velocidad * dt;
}

const lejos = { x: 0, y: 0, velocidad: 40 };
perseguir(lejos, { x: 300, y: 400 }, 1);
console.log('Avanzó:', Math.round(Math.hypot(lejos.x, lejos.y)));
```

#### Al superarla
El goblin disfrazado avanza lo justo, ni un paso más. Se saca el disfraz y se va, aburrido.

#### Imagen
- Un goblin de feria (orejas puntiagudas, chaleco a rayas, sin armas) sacándose un disfraz de sombra negra.
- Nima y Gheco lo miran con los brazos cruzados.

### Micro-misión R05-N05-P3 · Tres vidas

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco, Lucio
carta: Cooldown | después de un golpe, invulnerable un rato: if (ahora > invulnerableHasta) { vidas--; invulnerableHasta = ahora + 1000; }
recompensa: xp 10, oro 10
```

#### Escena
La luciérnaga tiene 3 vidas. Si una sombra la toca, pierde una… y queda un segundo brillando, intocable.

#### Gheco sugiere
Si un choque quitara una vida **en cada cuadro**, con una sola tocada se perderían todas en un instante. Por eso, después de un golpe, la luciérnaga queda **invulnerable** un rato.

Se guarda **hasta cuándo** es invulnerable (en milisegundos). Un golpe solo cuenta si `ahora` ya pasó ese momento; y si cuenta, se resta la vida y se corre el momento un segundo más allá.

```js
if (ahora > escudo.hasta) {
    // cuenta el golpe… y el escudo dura hasta ahora + 1000
}
```

#### Desafío
Completá `golpear`. (La sombra la toca en los milisegundos 0, 500, 1200, 1300 y 2500.)

#### Código inicial
```javascript
const luz = { vidas: 3, invulnerableHasta: -1 };

function golpear(ahora) {

}

for (const t of [0, 500, 1200, 1300, 2500]) {
  golpear(t);
  console.log(`${t} ms: ${luz.vidas} vidas`);
}
```

#### Salida esperada
```
0 ms: 2 vidas
500 ms: 2 vidas
1200 ms: 1 vidas
1300 ms: 1 vidas
2500 ms: 0 vidas
```

#### Solución
```javascript
const luz = { vidas: 3, invulnerableHasta: -1 };

function golpear(ahora) {
  if (ahora > luz.invulnerableHasta) {
    luz.vidas--;
    luz.invulnerableHasta = ahora + 1000;
  }
}

for (const t of [0, 500, 1200, 1300, 2500]) {
  golpear(t);
  console.log(`${t} ms: ${luz.vidas} vidas`);
}
```

#### Al superarla
La luciérnaga parpadea después de cada golpe, y los toques seguidos no la lastiman. Le queda una vida: justo.

#### Imagen
- La luciérnaga de cristal parpadeando con un halo blanco protector mientras una sombra negra rebota contra ella.
- Lucio contiene la respiración; Nima aprieta una palanca.

### Micro-misión R05-N05-P4 · Las oleadas

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco, Lucio
carta: Oleadas | cuando no quedan enemigos, la siguiente oleada · cada una más grande: 2 ** (n - 1)
recompensa: xp 10, oro 10
```

#### Escena
Cuando la luciérnaga se libra de todas las sombras, sale una oleada nueva, el doble de grande.

#### Gheco sugiere
`**` es la **potencia**: `2 ** 3` es `2 × 2 × 2 = 8`. Sirve para lo que se **duplica** cada vez: 1, 2, 4, 8… es `2 ** 0`, `2 ** 1`, `2 ** 2`, `2 ** 3`.

Para agregar varias a un arreglo, un `for` que cuente hasta esa cantidad y haga `push` en cada vuelta. Pensá qué número de oleada da 1 sombra en la primera y cómo sigue. Después de lanzar una, la cuenta de oleadas sube.

#### Desafío
Completá `lanzarOleada`.

#### Código inicial
```javascript
let oleada = 1;
let sombras = [];

function lanzarOleada() {

}

for (let ronda = 1; ronda <= 4; ronda++) {
  if (sombras.length === 0) lanzarOleada();
  console.log(`Ronda ${ronda}: ${sombras.length} sombras`);
  sombras = [];   // la luciérnaga las vence a todas
}
```

#### Salida esperada
```
Ronda 1: 1 sombras
Ronda 2: 2 sombras
Ronda 3: 4 sombras
Ronda 4: 8 sombras
```

#### Solución
```javascript
let oleada = 1;
let sombras = [];

function lanzarOleada() {
  for (let i = 0; i < 2 ** (oleada - 1); i++) {
    sombras.push({ x: 0, y: i * 10 });
  }
  oleada++;
}

for (let ronda = 1; ronda <= 4; ronda++) {
  if (sombras.length === 0) lanzarOleada();
  console.log(`Ronda ${ronda}: ${sombras.length} sombras`);
  sombras = [];   // la luciérnaga las vence a todas
}
```

#### Al superarla
Una, dos, cuatro, ocho sombras. Lucio cierra los ojos en la cuarta oleada. Nima no.

#### Imagen
- Oleadas de sombras negras cada vez más numerosas entrando por los bordes del tablero de vidrio.
- Nima, concentrada, con las manos en las palancas; Lucio con los ojos cerrados.

### Micro-misión R05-N05-P5 · La clase Sombra

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco
carta: Enemigos con clase | class Sombra { perseguir(obj, dt) { … } dibujar(ctx) { … } } · un arreglo de sombras
recompensa: xp 15, monedas 5
```

#### Escena
Con tantas sombras, Nima prefiere hacer un molde: cada sombra sabe perseguir y dibujarse.

#### Gheco sugiere
Es pasar lo que ya hiciste a una **clase** (R03): los datos de cada sombra en el `constructor`, y lo que sabe hacer en métodos, usando `this` en vez del nombre de la variable.

`Math.round(n)` **redondea** al entero más cercano: los píxeles del lienzo son enteros, y así el dibujo queda nítido.

#### Desafío
Completá la clase: `perseguir` como en R05-N05-P2, y `dibujar` con un cuadrado `#311b92` de 10 × 10 en su posición redondeada. (La comprobación corre 60 cuadros con dos sombras.)

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="200" height="200"></canvas>
```

#### Eventos
```
cuadros 61
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');

class Sombra {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.velocidad = 40;
  }
  perseguir(objetivo, dt) {

  }
  dibujar(ctx) {

  }
}

const luz = { x: 100, y: 100 };
const sombras = [new Sombra(0, 100), new Sombra(100, 0)];
let antes = null;

function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  ctx.clearRect(0, 0, 200, 200);
  for (const s of sombras) {
    s.perseguir(luz, dt);
    s.dibujar(ctx);
  }
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(luz.x, luz.y, 10, 10);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 200, 200)
lienzo: fillRect(40, 100, 10, 10) #311b92
lienzo: fillRect(100, 40, 10, 10) #311b92
lienzo: fillRect(100, 100, 10, 10) #ffd400
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');

class Sombra {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.velocidad = 40;
  }
  perseguir(objetivo, dt) {
    const dx = objetivo.x - this.x;
    const dy = objetivo.y - this.y;
    const largo = Math.hypot(dx, dy);
    if (largo > 0) {
      this.x += (dx / largo) * this.velocidad * dt;
      this.y += (dy / largo) * this.velocidad * dt;
    }
  }
  dibujar(ctx) {
    ctx.fillStyle = '#311b92';
    ctx.fillRect(Math.round(this.x), Math.round(this.y), 10, 10);
  }
}

const luz = { x: 100, y: 100 };
const sombras = [new Sombra(0, 100), new Sombra(100, 0)];
let antes = null;

function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  ctx.clearRect(0, 0, 200, 200);
  for (const s of sombras) {
    s.perseguir(luz, dt);
    s.dibujar(ctx);
  }
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(luz.x, luz.y, 10, 10);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
Dos sombras avanzan desde dos lados. Ahora, con el molde, podrían ser cien.

#### Imagen
- El lienzo del taller con dos sombras violeta oscuro avanzando desde la izquierda y desde arriba hacia una luciérnaga amarilla en el centro.
- Gheco tapándose los ojos con una mano y espiando con la otra.

### Micro-misión R05-N05-P6 · Esquivar

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco, Lumina
carta: Juego completo chiquito | mover con el teclado · las sombras persiguen · chocar resta vidas con cooldown
recompensa: xp 15, monedas 5
```

#### Escena
Lumina quiere probar: la luciérnaga se mueve con las flechas, una sombra la persigue, y si la toca le saca una vida (con un segundo de invulnerabilidad).

#### Gheco sugiere
Es juntar tres cosas que ya hiciste en cada cuadro: mover, perseguir y revisar el choque con su tiempo de invulnerabilidad (R05-N05-P3). La condición del golpe tiene dos partes, unidas con `&&`: que se toquen **y** que ya haya pasado el tiempo.

Después de restar la vida, mostrá las vidas en la página.

#### Desafío
Completá la parte del choque. (En la comprobación, la luz se queda quieta 3 segundos y la sombra la alcanza.)

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #ffd400; font-family: monospace; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<p>Vidas: <span id="vidas">3</span></p>
<canvas id="lienzo" width="200" height="100"></canvas>
```

#### Eventos
```
cuadros 180
```

#### Estado
```
#vidas
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const chocan = (a, b) => a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;
const luz = { x: 150, y: 45, lado: 10, vidas: 3, invulnerableHasta: -1 };
const sombra = { x: 0, y: 45, lado: 10, velocidad: 100 };
let antes = null;

function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  const dx = luz.x - sombra.x;
  const dy = luz.y - sombra.y;
  const largo = Math.hypot(dx, dy);
  if (largo > 0) {
    sombra.x += (dx / largo) * sombra.velocidad * dt;
    sombra.y += (dy / largo) * sombra.velocidad * dt;
  }
  // el choque con cooldown

  document.querySelector('#vidas').textContent = luz.vidas;
  ctx.clearRect(0, 0, 200, 100);
  ctx.fillStyle = '#311b92';
  ctx.fillRect(Math.round(sombra.x), Math.round(sombra.y), 10, 10);
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(luz.x, luz.y, 10, 10);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#vidas: 1
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const chocan = (a, b) => a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;
const luz = { x: 150, y: 45, lado: 10, vidas: 3, invulnerableHasta: -1 };
const sombra = { x: 0, y: 45, lado: 10, velocidad: 100 };
let antes = null;

function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  const dx = luz.x - sombra.x;
  const dy = luz.y - sombra.y;
  const largo = Math.hypot(dx, dy);
  if (largo > 0) {
    sombra.x += (dx / largo) * sombra.velocidad * dt;
    sombra.y += (dy / largo) * sombra.velocidad * dt;
  }
  if (chocan(luz, sombra) && ahora > luz.invulnerableHasta) {
    luz.vidas--;
    luz.invulnerableHasta = ahora + 1000;
  }
  document.querySelector('#vidas').textContent = luz.vidas;
  ctx.clearRect(0, 0, 200, 100);
  ctx.fillStyle = '#311b92';
  ctx.fillRect(Math.round(sombra.x), Math.round(sombra.y), 10, 10);
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(luz.x, luz.y, 10, 10);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
La sombra alcanza a la luciérnaga quieta y le saca dos vidas en tres segundos: con el *cooldown*, ni una más. Lumina se ríe: —Ahora movete, que para eso tenés flechas.

#### Imagen
- Una sombra negra pegada a una luciérnaga amarilla que parpadea con un halo blanco, en el lienzo del taller.
- Lumina (luciérnaga enorme, alas de vidrio) se ríe; Nima con las manos en las palancas, lista para escapar.

## R05-N06 · Junta las Gemas: el juego completo

```meta
tipo: tema
padre: R05-N05
precio: 10
criatura: dragon
temas: juegos.estados, juegos.guardado, js.canvas
usa: juegos.bucle, juegos.entrada, juegos.colisiones, juegos.ia, js.almacenamiento
```

### Crónica

Con todas las piezas arregladas, Nima arma el juego entero del tablero, tal como estaba en el plano del Vidriero: **Junta las Gemas**. La luciérnaga junta gemas, las sombras la persiguen, y cuando junta todas, empieza otra ronda. Si pierde las tres vidas, se termina, y el récord queda guardado.

—El Vidriero no lo hizo para jugar —dice Lucio, bajito—. Lo hizo para practicar. Para aprender a mover cosas de vidrio, una por una, sin que se choquen.

### Objetivos

- Organizar un juego con **estados**: `'jugando'`, `'fin'`.
- Integrar todo: bucle, teclado, colisiones, enemigos, puntaje y vidas.
- Guardar el récord en `localStorage`.
- Reiniciar el juego sin recargar la página.

### Antes de empezar

- R05-N01 a R05-N05.

### Explicación

#### El estado del juego
```javascript
const juego = {
  estado: 'jugando',     // o 'fin'
  puntos: 0,
  record: Number(localStorage.getItem('record') ?? 0),
};
```
En cada cuadro, según el estado, se hace una cosa u otra:
```javascript
function cuadro(ahora) {
  if (juego.estado === 'jugando') actualizar(dt, ahora);
  dibujar();
  requestAnimationFrame(cuadro);
}
```

#### Terminar y guardar
```javascript
if (jugador.vidas === 0) {
  juego.estado = 'fin';
  if (juego.puntos > juego.record) {
    juego.record = juego.puntos;
    localStorage.setItem('record', juego.record);
  }
}
```

#### Reiniciar
Una función `reiniciar()` que vuelve todo a como empieza (y llama a la misma que arma la primera ronda).

#### Partir en funciones
El juego entero no entra en un solo `cuadro`. Se separa: `moverJugador`, `moverSombras`, `juntarGemas`, `revisarGolpes`, `dibujar`… Cada una hace una cosa.

### Código de ejemplo

```javascript
// La lógica de Junta las Gemas, sin dibujar: rondas simuladas.
const juego = { estado: 'jugando', puntos: 0, ronda: 1, vidas: 3, record: 7 };

function juntarTodas(cantidad) {
  juego.puntos += cantidad;
  juego.ronda++;
}
function perderVida() {
  juego.vidas--;
  if (juego.vidas === 0) {
    juego.estado = 'fin';
    if (juego.puntos > juego.record) juego.record = juego.puntos;
  }
}

juntarTodas(3);
perderVida();
juntarTodas(5);
perderVida();
perderVida();
console.log(juego);
```

### Salida esperada

```
{ estado: 'fin', puntos: 8, ronda: 3, vidas: 0, record: 8 }
```

### ¿Para qué sirve?

Es un juego completo, con todo lo que tienen los juegos de verdad: estados, puntaje, vidas, enemigos, récord. Lo podés copiar a un `index.html` en tu compu, abrirlo con doble click en el navegador, y compartirlo. Es el mismo *Junta las Gemas* que vas a reescribir con tipos en el curso de TypeScript.

### Errores habituales

**Ogro: seguir actualizando en el estado `'fin'`.** Las sombras siguen persiguiendo a una luciérnaga muerta. Revisá el estado antes de actualizar.

**Goblin: el récord como texto.** `localStorage` devuelve texto: `'10' > '9'` da `false`. Convertí con `Number`.

**Ogro: reiniciar a medias.** Si `reiniciar` se olvida de algo (las vidas, las sombras), la segunda partida arranca rota.

### Micro-misión R05-N06-P1 · Los estados del juego

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco, Lucio
carta: Estados | juego.estado = 'jugando' o 'fin' · cada cuadro hace lo que corresponde al estado
recompensa: xp 10, oro 10
```

#### Escena
El plano tiene dos pantallas: *jugando* y *fin del juego*. Nima tiene que hacer que el juego pase de una a otra cuando se acaban las vidas.

#### Gheco sugiere
Un juego pasa por **estados**: jugando, en pausa, terminado. Se guarda en una variable de texto (`'jugando'`, `'fin'`), y cada parte del juego mira el estado antes de actuar: si terminó, ya no se mueve ni se pierden vidas.

El cambio de estado va donde pasa lo que lo provoca: cuando se pierde la última vida, el juego pasa a terminado.

#### Desafío
Completá `perderVida`.

#### Código inicial
```javascript
const juego = { estado: 'jugando', vidas: 3 };

function perderVida() {

}

for (let i = 1; i <= 4; i++) {
  if (juego.estado === 'jugando') perderVida();
  console.log(`Golpe ${i}: ${juego.vidas} vidas · ${juego.estado}`);
}
```

#### Salida esperada
```
Golpe 1: 2 vidas · jugando
Golpe 2: 1 vidas · jugando
Golpe 3: 0 vidas · fin
Golpe 4: 0 vidas · fin
```

#### Solución
```javascript
const juego = { estado: 'jugando', vidas: 3 };

function perderVida() {
  juego.vidas--;
  if (juego.vidas === 0) juego.estado = 'fin';
}

for (let i = 1; i <= 4; i++) {
  if (juego.estado === 'jugando') perderVida();
  console.log(`Golpe ${i}: ${juego.vidas} vidas · ${juego.estado}`);
}
```

#### Al superarla
Al tercer golpe aparece la pantalla de fin. El cuarto golpe ya no hace nada: el juego terminó.

#### Imagen
- El tablero de vidrio con un cartel de vidrio grabado colgando encima (sin texto legible) y las sombras quietas.
- Lucio y Nima miran el tablero apagado.

### Micro-misión R05-N06-P2 · El récord del Vidriero

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco, Lucio
carta: Guardar el récord | Number(localStorage.getItem('record') ?? 0) · si los puntos lo superan, setItem
recompensa: xp 10, oro 10
```

#### Escena
Grabado en la tapa del tablero hay un récord: 12 gemas. Lucio dice que lo hizo el Vidriero. Nima quiere superarlo, y que quede guardado.

#### Gheco sugiere
El **récord** se guarda en `localStorage` (de R02), así sigue ahí al volver otro día:

- leer: `localStorage.getItem('clave')` da texto, o `null` si no hay. Con `?? 0` y `Number`, queda un número (0 si nunca se guardó);
- comparar con los puntos de la partida;
- si los supera, guardar el nuevo con `setItem`.

Fijate en la consigna el texto exacto de los dos casos.

#### Desafío
Completá `terminar`. (El récord guardado es 12.)

#### Almacenamiento
```
local record = 12
```

#### Estado
```
local record
```

#### Código inicial
```javascript
function terminar(puntos) {

}

terminar(9);
terminar(15);
terminar(14);
```

#### Salida esperada
```
9: Récord: 12
15: ¡Récord nuevo!
14: Récord: 15
── Estado ──
local record: 15
```

#### Solución
```javascript
function terminar(puntos) {
  const record = Number(localStorage.getItem('record') ?? 0);
  if (puntos > record) {
    localStorage.setItem('record', puntos);
    console.log(`${puntos}: ¡Récord nuevo!`);
  } else {
    console.log(`${puntos}: Récord: ${record}`);
  }
}

terminar(9);
terminar(15);
terminar(14);
```

#### Al superarla
Quince gemas. Nima graba su récord al lado del del Vidriero, en la tapa. Lucio no dice nada, pero sonríe.

#### Imagen
- La tapa de bronce del tablero de gemas con dos números grabados (sin números legibles), uno viejo y uno recién hecho.
- Nima graba con una punta fina; Lucio sonríe atrás.

### Micro-misión R05-N06-P3 · Volver a empezar

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco
criatura: ogre
carta: Reiniciar | una sola función que deja todo como al empezar · se usa al principio y al reiniciar
recompensa: xp 10, oro 10
```

#### Escena
Un ogro escribió el reinicio y se olvidó de las vidas: la segunda partida arranca con 0 vidas y termina enseguida.

#### Gheco sugiere
Para **volver a empezar** hay que dejar **todo** como al principio: cada dato que cambia durante la partida. Si queda uno sin reiniciar, la partida nueva arranca con algo de la vieja (con 0 vidas, por ejemplo).

Lo más seguro es que la misma función `reiniciar()` se use también para **empezar** la primera vez: así nunca hay dos listas distintas de valores iniciales. Comparala con lo que cambia en el resto del programa.

#### Desafío
Arreglá `reiniciar`.

#### Código inicial
```javascript
const juego = {};

function reiniciar() {
  juego.estado = 'jugando';
  juego.puntos = 0;
}

reiniciar();
juego.vidas = 3;
juego.ronda = 1;
console.log('Primera partida:', juego);

juego.vidas = 0;
juego.estado = 'fin';
juego.puntos = 9;
juego.ronda = 4;
reiniciar();
console.log('Segunda partida:', juego);
```

#### Salida esperada
```
Primera partida: { estado: 'jugando', puntos: 0, vidas: 3, ronda: 1 }
Segunda partida: { estado: 'jugando', puntos: 0, vidas: 3, ronda: 1 }
```

#### Solución
```javascript
const juego = {};

function reiniciar() {
  juego.estado = 'jugando';
  juego.puntos = 0;
  juego.vidas = 3;
  juego.ronda = 1;
}

reiniciar();
console.log('Primera partida:', juego);

juego.vidas = 0;
juego.estado = 'fin';
juego.puntos = 9;
juego.ronda = 4;
reiniciar();
console.log('Segunda partida:', juego);
```

#### Al superarla
La segunda partida arranca igual que la primera: tres vidas, ronda uno. El ogro se queda sin chiste.

#### Imagen
- El tablero de gemas reiniciándose: gemas que vuelven a su lugar con destellos y tres corazoncitos de vidrio que se encienden.
- Un ogro torpe de feria (sin armas) mirando confundido.

### Micro-misión R05-N06-P4 · Junta las Gemas

```meta
lugar: El tablero de gemas
personajes: Nima, Gheco, Lucio, Lumina
criatura: dragon
carta: El juego entero | estado · mover · perseguir · juntar · golpes con cooldown · rondas · fin y récord
recompensa: xp 30, monedas 10
```

#### Escena
Llegó la hora: el juego entero, como en el plano. Lumina, Lucio, Bruno y Tati se juntan alrededor del tablero.

#### Gheco sugiere
Las dos funciones que faltan usan lo de R05-N04 y R05-N05:

- **juntar** es el `filter` con su cuenta de puntos, y una pregunta al final: si el arreglo quedó vacío, ronda nueva;
- **revisar golpes**: `some` (*alguno*) devuelve `true` si **alguno** del arreglo cumple, ideal para «¿alguna sombra me toca?»; el golpe con su tiempo de invulnerabilidad es el de R05-N05-P3; y el final es el récord de R05-N06-P2.

```js
const hayMoscas = cosas.some((c) => c.tipo === 'mosca');
```

#### Desafío
Completá las dos funciones:
- `juntarGemas()`: saca las gemas que tocan a la luz y suma un punto por cada una; si no queda ninguna, `nuevaRonda()`.
- `revisarGolpes(ahora)`: si alguna sombra toca a la luz y ya pasó el tiempo de invulnerabilidad, resta una vida (con un segundo de *cooldown*); si las vidas llegan a 0, termina (estado `'fin'`) y guarda el récord si lo superó.

La comprobación juega: va a la derecha medio segundo (junta una gema), a la izquierda, y después se queda quieta hasta que las sombras la alcanzan.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #ffd400; font-family: monospace; display: grid; place-items: center; height: 100vh; text-align: center; }
  canvas { background: #0b1020; border: 6px solid #8d6e3f; }
</style>
<p>Puntos: <span id="puntos">0</span> · Vidas: <span id="vidas">3</span> · Ronda: <span id="ronda">1</span> · Récord: <span id="record">0</span></p>
<canvas id="lienzo" width="240" height="160"></canvas>
<p id="estado"></p>
```

#### Eventos
```
apretar ArrowRight
cuadros 30
soltar ArrowRight
apretar ArrowLeft
cuadros 20
soltar ArrowLeft
esperar 6000
```

#### Estado
```
#puntos
#vidas
#estado
local record
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const teclas = new Set();
addEventListener('keydown', (e) => teclas.add(e.key));
addEventListener('keyup', (e) => teclas.delete(e.key));
const chocan = (a, b) => a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;

const juego = { record: Number(localStorage.getItem('record') ?? 0) };
let luz, gemas, sombras;

function nuevaRonda() {
  gemas = [[60, 75], [200, 30], [200, 130]].map(([x, y]) => ({ x, y, lado: 8 }));
  sombras = Array.from({ length: juego.ronda }, (_, i) => ({ x: 0, y: 20 + i * 60, lado: 12, velocidad: 25 }));
  juego.ronda++;
}

function reiniciar() {
  Object.assign(juego, { estado: 'jugando', puntos: 0, vidas: 3, ronda: 1 });
  luz = { x: 20, y: 75, lado: 12, velocidad: 100, invulnerableHasta: -1 };
  nuevaRonda();
}

function moverLuz(dt) {
  let dx = 0, dy = 0;
  if (teclas.has('ArrowRight')) dx += 1;
  if (teclas.has('ArrowLeft')) dx -= 1;
  if (teclas.has('ArrowDown')) dy += 1;
  if (teclas.has('ArrowUp')) dy -= 1;
  if (dx && dy) { dx /= Math.SQRT2; dy /= Math.SQRT2; }
  luz.x = Math.max(0, Math.min(luz.x + dx * luz.velocidad * dt, 240 - luz.lado));
  luz.y = Math.max(0, Math.min(luz.y + dy * luz.velocidad * dt, 160 - luz.lado));
}

function moverSombras(dt) {
  for (const s of sombras) {
    const dx = luz.x - s.x, dy = luz.y - s.y, largo = Math.hypot(dx, dy);
    if (largo > 0) { s.x += (dx / largo) * s.velocidad * dt; s.y += (dy / largo) * s.velocidad * dt; }
  }
}

function juntarGemas() {

}

function revisarGolpes(ahora) {

}

function dibujar() {
  ctx.clearRect(0, 0, 240, 160);
  ctx.fillStyle = '#4fc3f7';
  for (const g of gemas) ctx.fillRect(g.x, g.y, g.lado, g.lado);
  ctx.fillStyle = '#311b92';
  for (const s of sombras) ctx.fillRect(Math.round(s.x), Math.round(s.y), s.lado, s.lado);
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(Math.round(luz.x), Math.round(luz.y), luz.lado, luz.lado);
  for (const [id, valor] of Object.entries({ puntos: juego.puntos, vidas: juego.vidas, ronda: juego.ronda - 1, record: juego.record })) {
    document.querySelector(`#${id}`).textContent = valor;
  }
  document.querySelector('#estado').textContent = juego.estado === 'fin' ? 'Fin del juego · tocá R para reiniciar' : '';
}

let antes = null;
function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (juego.estado === 'jugando') {
    moverLuz(dt);
    moverSombras(dt);
    juntarGemas();
    revisarGolpes(ahora);
  }
  dibujar();
  requestAnimationFrame(cuadro);
}

addEventListener('keydown', (e) => {
  if (e.key === 'r' && juego.estado === 'fin') reiniciar();
});
reiniciar();
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#puntos: 1
#vidas: 0
#estado: Fin del juego · tocá R para reiniciar
local record: 1
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');
const teclas = new Set();
addEventListener('keydown', (e) => teclas.add(e.key));
addEventListener('keyup', (e) => teclas.delete(e.key));
const chocan = (a, b) => a.x < b.x + b.lado && a.x + a.lado > b.x && a.y < b.y + b.lado && a.y + a.lado > b.y;

const juego = { record: Number(localStorage.getItem('record') ?? 0) };
let luz, gemas, sombras;

function nuevaRonda() {
  gemas = [[60, 75], [200, 30], [200, 130]].map(([x, y]) => ({ x, y, lado: 8 }));
  sombras = Array.from({ length: juego.ronda }, (_, i) => ({ x: 0, y: 20 + i * 60, lado: 12, velocidad: 25 }));
  juego.ronda++;
}

function reiniciar() {
  Object.assign(juego, { estado: 'jugando', puntos: 0, vidas: 3, ronda: 1 });
  luz = { x: 20, y: 75, lado: 12, velocidad: 100, invulnerableHasta: -1 };
  nuevaRonda();
}

function moverLuz(dt) {
  let dx = 0, dy = 0;
  if (teclas.has('ArrowRight')) dx += 1;
  if (teclas.has('ArrowLeft')) dx -= 1;
  if (teclas.has('ArrowDown')) dy += 1;
  if (teclas.has('ArrowUp')) dy -= 1;
  if (dx && dy) { dx /= Math.SQRT2; dy /= Math.SQRT2; }
  luz.x = Math.max(0, Math.min(luz.x + dx * luz.velocidad * dt, 240 - luz.lado));
  luz.y = Math.max(0, Math.min(luz.y + dy * luz.velocidad * dt, 160 - luz.lado));
}

function moverSombras(dt) {
  for (const s of sombras) {
    const dx = luz.x - s.x, dy = luz.y - s.y, largo = Math.hypot(dx, dy);
    if (largo > 0) { s.x += (dx / largo) * s.velocidad * dt; s.y += (dy / largo) * s.velocidad * dt; }
  }
}

function juntarGemas() {
  gemas = gemas.filter((g) => {
    if (chocan(luz, g)) {
      juego.puntos++;
      return false;
    }
    return true;
  });
  if (gemas.length === 0) nuevaRonda();
}

function revisarGolpes(ahora) {
  if (ahora <= luz.invulnerableHasta) return;
  if (sombras.some((s) => chocan(luz, s))) {
    juego.vidas--;
    luz.invulnerableHasta = ahora + 1000;
    if (juego.vidas === 0) {
      juego.estado = 'fin';
      if (juego.puntos > juego.record) {
        juego.record = juego.puntos;
        localStorage.setItem('record', juego.record);
      }
    }
  }
}

function dibujar() {
  ctx.clearRect(0, 0, 240, 160);
  ctx.fillStyle = '#4fc3f7';
  for (const g of gemas) ctx.fillRect(g.x, g.y, g.lado, g.lado);
  ctx.fillStyle = '#311b92';
  for (const s of sombras) ctx.fillRect(Math.round(s.x), Math.round(s.y), s.lado, s.lado);
  ctx.fillStyle = '#ffd400';
  ctx.fillRect(Math.round(luz.x), Math.round(luz.y), luz.lado, luz.lado);
  for (const [id, valor] of Object.entries({ puntos: juego.puntos, vidas: juego.vidas, ronda: juego.ronda - 1, record: juego.record })) {
    document.querySelector(`#${id}`).textContent = valor;
  }
  document.querySelector('#estado').textContent = juego.estado === 'fin' ? 'Fin del juego · tocá R para reiniciar' : '';
}

let antes = null;
function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (juego.estado === 'jugando') {
    moverLuz(dt);
    moverSombras(dt);
    juntarGemas();
    revisarGolpes(ahora);
  }
  dibujar();
  requestAnimationFrame(cuadro);
}

addEventListener('keydown', (e) => {
  if (e.key === 'r' && juego.estado === 'fin') reiniciar();
});
reiniciar();
requestAnimationFrame(cuadro);
```

#### Al superarla
El tablero del Vidriero vuelve a funcionar después de treinta años. Bruno juega, Tati juega, Lucio juega (y pierde enseguida). Lumina mira las partidas desde arriba, sin decir nada, hasta que de golpe se da vuelta hacia el fondo del taller: debajo de la lona, el marco del vitral **vibra**.

—Ya está listo —dice—. Pero algo lo cuida.

#### Imagen
- El tablero de gemas funcionando con luces, gemas celestes, sombras violeta y la luciérnaga amarilla, rodeado de gente.
- Bruno y Tati se pelean por las palancas; Lucio se ríe; Lumina mira hacia el fondo del taller, donde una lona tapa algo grande que vibra.

## R05-N07 · Jefe final: el Dragón de los Fuegos Artificiales

```meta
tipo: jefe
padre: R05-N06
precio: 10
criatura: dragon
insignia: Arco del Vitral
insignia_descripcion: Venciste al Dragón de los Fuegos Artificiales y moviste el vitral: dominás la lengua de la Feria.
usa: js.canvas, juegos.bucle, juegos.colisiones, poo.clases, conc.async
```

### Crónica

Cuando Nima levanta la lona, el marco del vitral está entero, con todos sus vidrios… y enroscado alrededor, durmiendo, hay un **dragón hecho de fuegos artificiales**: un cuerpo largo de chispas de colores que se apagan y se prenden, y ojos de bengala. Es el **Dragón de los Fuegos Artificiales**, el que el Vidriero dejó cuidando el mecanismo.

Se despierta. Cada vez que respira, suelta una lluvia de chispas que, si tocan el vitral, lo rajan.

—No lo vas a vencer peleando —dice {mentor}—. Lo vas a vencer **haciendo lo que él cuida**: mover el vitral. Si el vitral se mueve, ya no tiene nada que cuidar.

Lucio le alcanza a Nima un arco que estaba colgado en la pared del taller, de vidrio de colores, con la cuerda de luz: **el Arco del Vitral**.

### Objetivos

- Integrar todo el curso: clases, arreglos, el bucle, el tiempo, colisiones, eventos y promesas.
- Usar `ctx.save`, `translate` y `rotate` para dibujar cosas que giran.
- Animar un sistema de partículas (las chispas del dragón).
- Mover el vitral.

### Antes de empezar

- Todo el curso. De verdad: todo.

### Explicación

#### Girar
```javascript
ctx.save();                    // guarda cómo estaba el pincel
ctx.translate(cx, cy);         // el (0, 0) pasa al centro
ctx.rotate(angulo);            // gira todo lo que se dibuje después (en radianes)
ctx.fillRect(-10, -40, 20, 40);
ctx.restore();                 // vuelve como estaba
```
Para que algo gire sobre su centro, primero se mueve el origen al centro y después se rota.

#### Partículas
Una chispa es un objeto con posición, velocidad y vida. En cada cuadro, todas se mueven, pierden vida, y las que llegan a 0 se borran:
```javascript
chispas = chispas.filter((c) => c.vida > 0);
for (const c of chispas) {
  c.x += c.vx * dt;
  c.y += c.vy * dt;
  c.vida -= dt;
}
```

### Micro-misión R05-N07-P1 · La lluvia de chispas

```meta
lugar: El fondo del taller
personajes: Nima, Gheco, el Dragón de los Fuegos Artificiales
criatura: dragon
carta: Partículas | cada chispa con x, y, vx, vy, vida · moverlas, gastarles vida y sacar las que se apagan
recompensa: xp 15, monedas 3
```

#### Escena
El dragón respira y suelta chispas. Nima tiene que entender cómo se mueven para poder esquivarlas: cada una sale con su velocidad y se apaga cuando se le termina la vida.

#### Gheco sugiere
Las **partículas** (chispas, humo, polvo) son muchas cosas chiquitas, cada una con su velocidad y su **vida**: cuánto tiempo le queda, en segundos.

En cada cuadro, a cada una:

- se la mueve con su velocidad (como en R05-N02: velocidad por `dt`, en cada eje);
- se le resta a su vida el tiempo que pasó.

Y al final se sacan, con `filter`, las que ya no tienen vida. `-=` resta y guarda.

#### Desafío
Completá `actualizar`.

#### Código inicial
```javascript
let chispas = [
  { x: 0, y: 0, vx: 10, vy: 0, vida: 1 },
  { x: 0, y: 0, vx: 0, vy: 20, vida: 2 },
  { x: 0, y: 0, vx: -5, vy: -5, vida: 0.5 },
];

function actualizar(dt) {

}

for (let paso = 1; paso <= 4; paso++) {
  actualizar(0.5);
  console.log(`${paso * 0.5} s:`, chispas.map((c) => `(${c.x}, ${c.y})`).join(' '));
}
```

#### Salida esperada
```
0.5 s: (5, 0) (0, 10)
1 s: (0, 20)
1.5 s: (0, 30)
2 s:
```

#### Solución
```javascript
let chispas = [
  { x: 0, y: 0, vx: 10, vy: 0, vida: 1 },
  { x: 0, y: 0, vx: 0, vy: 20, vida: 2 },
  { x: 0, y: 0, vx: -5, vy: -5, vida: 0.5 },
];

function actualizar(dt) {
  for (const c of chispas) {
    c.x += c.vx * dt;
    c.y += c.vy * dt;
    c.vida -= dt;
  }
  chispas = chispas.filter((c) => c.vida > 0);
}

for (let paso = 1; paso <= 4; paso++) {
  actualizar(0.5);
  console.log(`${paso * 0.5} s:`, chispas.map((c) => `(${c.x}, ${c.y})`).join(' '));
}
```

#### Al superarla
Nima ve el patrón: las chispas rápidas se apagan primero. Se acerca al vitral por el camino que dejan libre.

#### Imagen
- Un dragón largo hecho de fuegos artificiales de colores, con ojos de bengala, enroscado alrededor de un gran marco de vitral en el fondo de un taller, soltando una lluvia de chispas.
- Nima (trenza negra con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) avanza agachada entre las chispas; Gheco se cubre en su capucha.

### Micro-misión R05-N07-P2 · El sol que gira

```meta
lugar: El fondo del taller
personajes: Nima, Gheco, Lumina, el Dragón de los Fuegos Artificiales
carta: rotate | ctx.save(); ctx.translate(cx, cy); ctx.rotate(angulo); … dibujar alrededor del (0, 0) …; ctx.restore();
recompensa: xp 15, monedas 3
```

#### Escena
El mecanismo del vitral está trabado: el sol del centro tiene que **girar** para que todo se mueva. Lumina le muestra a Nima cómo dibujaba el Vidriero las cosas que giran.

#### Gheco sugiere
Para dibujar algo **girado**, en vez de calcular cada punta, se gira **el papel**:

- `ctx.save()` guarda cómo está el pincel ahora;
- `ctx.translate(x, y)` mueve el punto `(0, 0)` a ese lugar (el centro del giro);
- `ctx.rotate(angulo)` gira todo lo que se dibuje después, en **radianes** (`Math.PI` es media vuelta);
- `ctx.restore()` vuelve el pincel a como estaba en el `save`.

```js
ctx.save();
ctx.translate(50, 50);
ctx.rotate(Math.PI / 4);        // un octavo de vuelta
ctx.fillRect(-10, -10, 20, 20); // un rombo con centro en (50, 50)
ctx.restore();
```

Con un `rotate` adentro de un `for`, cada dibujo queda girado un poco más que el anterior.

#### Desafío
Completá el giro: en cada cuadro, trasladá al centro (100, 75), rotá `ahora / 1000` radianes y dibujá los cuatro rayos con `fillRect(-4, -60, 8, 30)`, girando de a `Math.PI / 2` entre uno y otro. Después restaurá y dibujá el sol encima. (La comprobación corre 30 cuadros.)

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0d1b3d; border: 8px solid #8d6e3f; border-radius: 50%; }
</style>
<canvas id="vitral" width="200" height="150"></canvas>
```

#### Eventos
```
cuadros 30
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#vitral').getContext('2d');

function cuadro(ahora) {
  ctx.clearRect(0, 0, 200, 150);
  ctx.fillStyle = '#ffb300';
  // guardá, trasladá al centro, rotá, dibujá los 4 rayos, restaurá

  ctx.fillStyle = '#ffd400';
  ctx.beginPath();
  ctx.arc(100, 75, 20, 0, Math.PI * 2);
  ctx.fill();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 200, 150)
lienzo: save()
lienzo: translate(100, 75)
lienzo: rotate(0.5)
lienzo: fillRect(-4, -60, 8, 30) #ffb300
lienzo: rotate(1.57)
lienzo: fillRect(-4, -60, 8, 30) #ffb300
lienzo: rotate(1.57)
lienzo: fillRect(-4, -60, 8, 30) #ffb300
lienzo: rotate(1.57)
lienzo: fillRect(-4, -60, 8, 30) #ffb300
lienzo: rotate(1.57)
lienzo: restore()
lienzo: arc(100, 75, 20, 0, 6.28)
lienzo: fill() #ffd400
```

#### Solución
```javascript
const ctx = document.querySelector('#vitral').getContext('2d');

function cuadro(ahora) {
  ctx.clearRect(0, 0, 200, 150);
  ctx.fillStyle = '#ffb300';
  ctx.save();
  ctx.translate(100, 75);
  ctx.rotate(ahora / 1000);
  for (let i = 0; i < 4; i++) {
    ctx.fillRect(-4, -60, 8, 30);
    ctx.rotate(Math.PI / 2);
  }
  ctx.restore();
  ctx.fillStyle = '#ffd400';
  ctx.beginPath();
  ctx.arc(100, 75, 20, 0, Math.PI * 2);
  ctx.fill();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
Los rayos del sol empiezan a girar, despacio. El dragón abre un ojo de bengala, desconfiado: algo que cuidaba se está moviendo.

#### Imagen
- El sol de un vitral circular con cuatro rayos dorados girando, de noche, en un marco de bronce.
- El dragón de fuegos artificiales abre un ojo de bengala; Lumina ilumina el vitral desde arriba.

### Micro-misión R05-N07-P3 · El vitral se mueve

```meta
lugar: El fondo del taller
personajes: Nima, Gheco, Lumina, Lucio, el Dragón de los Fuegos Artificiales
criatura: dragon
carta: El final | clases para los vidrios · el bucle con el tiempo · rotate · la flecha que espera (await) · el vitral se mueve
recompensa: xp 50, oro 50, monedas 1
item: Arco del Vitral
```

#### Escena
Es el momento. El vitral tiene un anillo de **vidrios de colores** que tienen que girar alrededor del sol, cada uno a su velocidad. Y el mecanismo solo arranca si la **flecha de luz** llega al centro: Nima tiene que tensar el Arco del Vitral, **esperar** (dos segundos: el dragón respira y se calma) y soltar. Cuando la flecha llega, el vitral se mueve.

#### Gheco sugiere
Junta lo del curso entero:

- `avanzar` es la velocidad por `dt` de R05-N02, pero sobre un **ángulo** en vez de una posición;
- `soltarFlecha` es una función `async` (R04): con `await` sobre la promesa `esperar`, se queda esperando sin congelar el juego, y después cambia el estado y el cartel (R02).

El bucle ya pregunta por `vitral.moviendo`: no hace falta tocarlo.

#### Desafío
Completá `avanzar` y `soltarFlecha`:
- `avanzar(dt)` suma `this.velocidad * dt` al ángulo del vidrio;
- `soltarFlecha()` espera 2000 ms (con la promesa `esperar`), y después pone `vitral.moviendo = true` y escribe `¡El vitral se mueve!` en `#cartel`.

La comprobación toca *Soltar la flecha*, espera 2 segundos y después deja correr el vitral 1 segundo.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #ffd400; font-family: system-ui, sans-serif; display: grid; place-items: center; height: 100vh; text-align: center; }
  canvas { background: #0d1b3d; border: 8px solid #8d6e3f; border-radius: 50%; }
  button { font-size: 18px; padding: 8px 18px; margin-top: 8px; }
</style>
<canvas id="vitral" width="220" height="220"></canvas>
<p id="cartel">El vitral está quieto</p>
<button id="soltar">Soltar la flecha</button>
```

#### Eventos
```
click #soltar
esperar 2000
cuadros 60
```

#### Estado
```
#cartel
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#vitral').getContext('2d');
const esperar = (ms) => new Promise((listo) => setTimeout(listo, ms));

class Vidrio {
  constructor(color, angulo, velocidad) {
    this.color = color;
    this.angulo = angulo;
    this.velocidad = velocidad;   // radianes por segundo
  }
  avanzar(dt) {

  }
  dibujar(ctx) {
    ctx.save();
    ctx.translate(110, 110);
    ctx.rotate(this.angulo);
    ctx.fillStyle = this.color;
    ctx.fillRect(60, -12, 30, 24);
    ctx.restore();
  }
}

const vitral = {
  moviendo: false,
  vidrios: [
    new Vidrio('#e53935', 0, 1),
    new Vidrio('#43a047', Math.PI / 2, 1),
    new Vidrio('#1e88e5', Math.PI, 1),
    new Vidrio('#ab47bc', (3 * Math.PI) / 2, 1),
  ],
};

async function soltarFlecha() {

}

let antes = null;
function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (vitral.moviendo) {
    for (const v of vitral.vidrios) v.avanzar(dt);
  }
  ctx.clearRect(0, 0, 220, 220);
  for (const v of vitral.vidrios) v.dibujar(ctx);
  ctx.fillStyle = '#ffd400';
  ctx.beginPath();
  ctx.arc(110, 110, 30, 0, Math.PI * 2);
  ctx.fill();
  requestAnimationFrame(cuadro);
}

document.querySelector('#soltar').addEventListener('click', soltarFlecha, { once: true });
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#cartel: ¡El vitral se mueve!
lienzo: clearRect(0, 0, 220, 220)
lienzo: save()
lienzo: translate(110, 110)
lienzo: rotate(1.02)
lienzo: fillRect(60, -12, 30, 24) #e53935
lienzo: restore()
lienzo: save()
lienzo: translate(110, 110)
lienzo: rotate(2.59)
lienzo: fillRect(60, -12, 30, 24) #43a047
lienzo: restore()
lienzo: save()
lienzo: translate(110, 110)
lienzo: rotate(4.16)
lienzo: fillRect(60, -12, 30, 24) #1e88e5
lienzo: restore()
lienzo: save()
lienzo: translate(110, 110)
lienzo: rotate(5.73)
lienzo: fillRect(60, -12, 30, 24) #ab47bc
lienzo: restore()
lienzo: arc(110, 110, 30, 0, 6.28)
lienzo: fill() #ffd400
```

#### Solución
```javascript
const ctx = document.querySelector('#vitral').getContext('2d');
const esperar = (ms) => new Promise((listo) => setTimeout(listo, ms));

class Vidrio {
  constructor(color, angulo, velocidad) {
    this.color = color;
    this.angulo = angulo;
    this.velocidad = velocidad;   // radianes por segundo
  }
  avanzar(dt) {
    this.angulo += this.velocidad * dt;
  }
  dibujar(ctx) {
    ctx.save();
    ctx.translate(110, 110);
    ctx.rotate(this.angulo);
    ctx.fillStyle = this.color;
    ctx.fillRect(60, -12, 30, 24);
    ctx.restore();
  }
}

const vitral = {
  moviendo: false,
  vidrios: [
    new Vidrio('#e53935', 0, 1),
    new Vidrio('#43a047', Math.PI / 2, 1),
    new Vidrio('#1e88e5', Math.PI, 1),
    new Vidrio('#ab47bc', (3 * Math.PI) / 2, 1),
  ],
};

async function soltarFlecha() {
  document.querySelector('#cartel').textContent = 'La flecha espera…';
  await esperar(2000);
  vitral.moviendo = true;
  document.querySelector('#cartel').textContent = '¡El vitral se mueve!';
}

let antes = null;
function cuadro(ahora) {
  const dt = antes === null ? 0 : (ahora - antes) / 1000;
  antes = ahora;
  if (vitral.moviendo) {
    for (const v of vitral.vidrios) v.avanzar(dt);
  }
  ctx.clearRect(0, 0, 220, 220);
  for (const v of vitral.vidrios) v.dibujar(ctx);
  ctx.fillStyle = '#ffd400';
  ctx.beginPath();
  ctx.arc(110, 110, 30, 0, Math.PI * 2);
  ctx.fill();
  requestAnimationFrame(cuadro);
}

document.querySelector('#soltar').addEventListener('click', soltarFlecha, { once: true });
requestAnimationFrame(cuadro);
```

#### Al superarla
Nima tensa el Arco del Vitral. Espera. El dragón respira una vez, dos, y se calma. Recién entonces, Nima suelta.

La flecha de luz cruza el taller sin apuro y entra justo en el centro del sol. El mecanismo hace *clic*. Y el vitral **se mueve**: los vidrios de colores empiezan a girar alrededor del sol, cada uno a su ritmo, y la luz que pasa a través de ellos pinta el taller de colores que cambian.

El Dragón de los Fuegos Artificiales se desenrosca despacio del marco. Ya no tiene nada que cuidar. Sube por la chimenea del taller y, en el cielo de la Feria, estalla en el fuego artificial más grande que nadie vio nunca. Toda la Feria sale a mirar.

En el balcón del portal, lejos, el otro vitral —el gemelo de este— también empieza a girar. Y por primera vez **muestra una imagen**: un cielo lleno de estrellas, atadas entre sí con hilos de luz, cada una en su figura.

—Ahí fue el Vidriero —dice {mentor}, en voz muy baja—. Al **Mirador de las Constelaciones**.

Nima mira la imagen hasta que se borra. Después saca del carcaj el borrador de la carta para Sila, lo termina, y lo suelta en una flecha de luz hacia el sur. Esta vez se queda esperando la respuesta, sin apuro.

#### Imagen
- Un gran vitral circular girando en el fondo del taller del Vidriero, con vidrios de colores alrededor de un sol dorado, y la luz de colores pintando el taller.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas que brillan) con el Arco del Vitral (un arco de vidrio de colores con cuerda de luz) recién disparado; Lucio, Lumina (luciérnaga enorme con alas de vidrio), Gheco, Bruno y Tati mirando maravillados.
- Por la chimenea, un dragón de fuegos artificiales sube hacia el cielo de la Feria.
