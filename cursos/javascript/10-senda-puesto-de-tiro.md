# RAMA S05 · Senda del Puesto de Tiro: un juego de puntería en canvas

```meta
tipo: senda
posicion: 10
```

## S05-N01 · Blancos y puntería

```meta
tipo: tema
padre: R05-N07
precio: 3
moneda: comodin
criatura: orc
temas: juegos.entrada, juegos.colisiones
usa: js.canvas, js.eventos
```

### Crónica

Con el vitral en movimiento y el Dragón en el cielo, la Feria vuelve a abrir todos sus puestos. Bruno y Tati corren hasta Nima con una idea: **el puesto de tiro**, el primero que ella visitó cuando llegó, el de los blancos que aparecían cuando querían. —¡Hagámoslo de nuevo, pero **en el lienzo**! —dice Tati—. Un juego de verdad, con puntos, tiempo y niveles. Y que vos no ganes siempre.

Nima se ríe. Hace mucho que no se ríe así. A lo lejos, entre los faroles, brilla una luz amarilla que salta: **Destello**, su ciervo de luz, que solo aparece cuando ella lo llama.

### Objetivos

- Dibujar un blanco de anillos con `arc`.
- Pasar un click a coordenadas del lienzo con `getBoundingClientRect`.
- Saber si un tiro dio adentro con la distancia (`Math.hypot`), y sumar puntos según el anillo.
- Manejar varios blancos en un arreglo y sacar los que caen.

### Antes de empezar

- El Taller del Vidriero (R05): el lienzo, el bucle del juego, el teclado y las colisiones.

### Explicación

#### Un blanco de anillos
Se dibuja de afuera hacia adentro: el círculo grande primero, el chico encima.
```javascript
function circulo(x, y, radio, color) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, radio, 0, Math.PI * 2);
  ctx.fill();
}
circulo(150, 75, 30, '#e53935');
circulo(150, 75, 20, '#ffffff');
circulo(150, 75, 10, '#e53935');
```

#### Dónde tocó
El evento del mouse trae `clientX` y `clientY`: dónde tocó **en la ventana**. Para saber dónde tocó **en el lienzo**, se resta la esquina del lienzo:
```javascript
lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  const x = e.clientX - caja.left;
  const y = e.clientY - caja.top;
});
```

#### ¿Adentro?
Un punto está adentro de un círculo si su **distancia** al centro es menor o igual que el radio. `Math.hypot(dx, dy)` es la distancia (Pitágoras: la raíz de `dx² + dy²`):
```javascript
const distancia = Math.hypot(x - blanco.x, y - blanco.y);
const adentro = distancia <= blanco.radio;
```

> **En la caja**, el evento `click #lienzo 120 80` toca el lienzo en el punto (120, 80), contando desde su esquina de arriba a la izquierda.

### Código de ejemplo

```javascript
const blanco = { x: 150, y: 75, radio: 30 };
for (const [x, y] of [[150, 75], [165, 75], [170, 95], [200, 75]]) {
  const distancia = Math.hypot(x - blanco.x, y - blanco.y);
  console.log(`(${x}, ${y}) está a ${distancia.toFixed(1)}: ${distancia <= blanco.radio ? 'adentro' : 'afuera'}`);
}
```

### Salida esperada

```
(150, 75) está a 0.0: adentro
(165, 75) está a 15.0: adentro
(170, 95) está a 28.3: adentro
(200, 75) está a 50.0: afuera
```

### ¿Para qué sirve?

Saber dónde tocó alguien en un lienzo sirve para todo lo que se dibuja: juegos, mapas, editores de imágenes, gráficos que muestran un dato al tocarlos. La distancia entre dos puntos aparece en cualquier juego: un disparo, un enemigo que te ve, una moneda que se junta.

### Errores habituales

**Orco: usar `clientX` directo.** Es la posición en la ventana, no en el lienzo: si el lienzo no está pegado a la esquina, todos los tiros dan corridos.

**Ogro: comparar `x` e `y` por separado.** `Math.abs(dx) <= radio && Math.abs(dy) <= radio` es un **cuadrado**: las esquinas cuentan como adentro.

**Ogro: dibujar el chico primero.** El grande lo tapa.

### Micro-misión S05-N01-P1 · El blanco de Bruno

```meta
lugar: El puesto de tiro de la Feria
personajes: Nima, Gheco, Bruno
carta: Anillos | circulo(x, y, 30, rojo) · circulo(x, y, 20, blanco) · circulo(x, y, 10, rojo)
recompensa: xp 10, oro 10
```

#### Escena
Bruno pinta el primer blanco del juego en el lienzo del puesto, pero solo le sale un círculo rojo. —Los de verdad tienen anillos —dice Tati.

#### Gheco sugiere
Esta Senda arma un puesto de tiro con el lienzo de R05. Lo primero: cuando algo se dibuja muchas veces, conviene una **función** que lo haga (como la `circulo` que ya viene), y llamarla con distintos datos.

El orden importa: lo que se dibuja después queda **encima**. Para que se vean los tres anillos, va primero el más grande.

#### Desafío
Con la función `circulo`, tres anillos con centro en el medio del lienzo (150, 75): radio 30 rojo (`#e53935`), encima radio 20 blanco (`#ffffff`) y encima radio 10 rojo.

El blanco de tres anillos.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');

function circulo(x, y, radio, color) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, radio, 0, Math.PI * 2);
  ctx.fill();
}

circulo(150, 75, 30, '#e53935');
```

#### Salida esperada
```
── Estado ──
lienzo: arc(150, 75, 30, 0, 6.28)
lienzo: fill() #e53935
lienzo: arc(150, 75, 20, 0, 6.28)
lienzo: fill() #ffffff
lienzo: arc(150, 75, 10, 0, 6.28)
lienzo: fill() #e53935
```

#### Solución
```javascript
const ctx = document.querySelector('#lienzo').getContext('2d');

function circulo(x, y, radio, color) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, radio, 0, Math.PI * 2);
  ctx.fill();
}

circulo(150, 75, 30, '#e53935');
circulo(150, 75, 20, '#ffffff');
circulo(150, 75, 10, '#e53935');
```

#### Al superarla
Un blanco de verdad, rojo y blanco, en el centro del lienzo. Bruno le saca una foto con los ojos.

#### Imagen
- Un puesto de tiro de feria de noche, con un lienzo enmarcado en madera donde brilla un blanco rojo y blanco de tres anillos.
- Bruno (12 años, pelo rizado, gorra al revés, chaleco rojo) con un pincel; Tati (11, dos colitas, delantal amarillo) aplaude; Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) mira sonriendo.

### Micro-misión S05-N01-P2 · Dónde cayó la flecha

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Tati
carta: Coordenadas | const caja = lienzo.getBoundingClientRect() · x = e.clientX - caja.left
recompensa: xp 10, oro 10
```

#### Escena
Tati toca el lienzo para tirar. El juego anota el tiro… en un lugar que no es donde tocó.

#### Gheco sugiere
El click trae dónde cayó, pero medido desde la esquina de la **ventana** (`evento.clientX` y `evento.clientY`), no del lienzo.

`lienzo.getBoundingClientRect()` da la caja del lienzo en la ventana: `left` es cuánto está corrido a la derecha y `top`, hacia abajo. Restando, queda el punto **dentro** del lienzo:

```js
const caja = lienzo.getBoundingClientRect();
const x = evento.clientX - caja.left;
```

`Math.round` lo redondea para mostrarlo.

#### Desafío
En cada click, `#tiro` muestra en qué punto **del lienzo** cayó, redondeado: `Tiro en (120, 80)`.

Tati tira en el punto (120, 80) del lienzo.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f6efe3; font-family: system-ui, sans-serif; padding: 40px 30px; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; display: block; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
<p id="tiro">Tocá el lienzo</p>
```

#### Eventos
```
click #lienzo 120 80
```

#### Estado
```
#tiro
```

#### Código inicial
```javascript
const lienzo = document.querySelector('#lienzo');
const tiro = document.querySelector('#tiro');

lienzo.addEventListener('click', (e) => {
  tiro.textContent = `Tiro en (${e.clientX}, ${e.clientY})`;
});
```

#### Salida esperada
```
── Estado ──
#tiro: Tiro en (120, 80)
```

#### Solución
```javascript
const lienzo = document.querySelector('#lienzo');
const tiro = document.querySelector('#tiro');

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  const x = Math.round(e.clientX - caja.left);
  const y = Math.round(e.clientY - caja.top);
  tiro.textContent = `Tiro en (${x}, ${y})`;
});
```

#### Al superarla
*Tiro en (120, 80)*: justo donde tocó. Antes decía (150, 120): el juego contaba desde la esquina de la ventana, no del lienzo.

#### Imagen
- Una flecha de luz clavada en un punto del lienzo, con dos reglas de madera que marcan la distancia a la esquina de arriba.
- Tati señala la flecha con el dedo, contenta.

### Micro-misión S05-N01-P3 · ¿Adentro o afuera?

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Bruno
carta: Math.hypot | Math.hypot(x - blanco.x, y - blanco.y) <= blanco.radio
recompensa: xp 10, oro 10
```

#### Escena
Bruno tira tres veces y discute cada tiro: —¡Ese entró! —No, rozó. Hace falta un juez.

#### Gheco sugiere
Un tiro cae adentro de un círculo si su **distancia al centro** es menor o igual que el radio. La distancia entre dos puntos es `Math.hypot(dx, dy)` (R05-N04), con las diferencias en `x` y en `y`.

Para la cuenta, dos variables afuera del evento: los tiros y los aciertos. El tiro de la «esquina» está a exactamente 30… y 30 es menor **o igual** que 30.

#### Desafío
El blanco tiene centro en (150, 75) y radio 30. En cada click, `#resultado` dice `¡Adentro!` si el tiro cayó a 30 o menos del centro, o `Afuera` si no; `#aciertos` lleva la cuenta, como `1 de 3`.

Bruno tira en (160, 70), (20, 20) y (175, 100), justo en la «esquina» del blanco.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f6efe3; font-family: system-ui, sans-serif; padding: 20px; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; display: block; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
<p><span id="resultado"></span> · <span id="aciertos">0 de 0</span></p>
```

#### Eventos
```
click #lienzo 160 70
click #lienzo 20 20
click #lienzo 175 100
```

#### Estado
```
#resultado
#aciertos
```

#### Código inicial
```javascript
const lienzo = document.querySelector('#lienzo');
const blanco = { x: 150, y: 75, radio: 30 };
let tiros = 0;
let aciertos = 0;

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  const x = e.clientX - caja.left;
  const y = e.clientY - caja.top;
  tiros++;
  const adentro = Math.abs(x - blanco.x) <= blanco.radio;
  if (adentro) aciertos++;
  document.querySelector('#resultado').textContent = adentro ? '¡Adentro!' : 'Afuera';
  document.querySelector('#aciertos').textContent = `${aciertos} de ${tiros}`;
});
```

#### Salida esperada
```
── Estado ──
#resultado: Afuera
#aciertos: 1 de 3
```

#### Solución
```javascript
const lienzo = document.querySelector('#lienzo');
const blanco = { x: 150, y: 75, radio: 30 };
let tiros = 0;
let aciertos = 0;

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  const x = e.clientX - caja.left;
  const y = e.clientY - caja.top;
  tiros++;
  const adentro = Math.hypot(x - blanco.x, y - blanco.y) <= blanco.radio;
  if (adentro) aciertos++;
  document.querySelector('#resultado').textContent = adentro ? '¡Adentro!' : 'Afuera';
  document.querySelector('#aciertos').textContent = `${aciertos} de ${tiros}`;
});
```

#### Al superarla
El juez del lienzo no discute: uno adentro y dos afuera. El de la esquina, también afuera: un blanco es redondo, no cuadrado. Bruno acepta, de mala gana.

#### Imagen
- Un blanco con dos flechas de luz clavadas adentro y una afuera, en el borde del lienzo.
- Bruno con los brazos cruzados; Gheco con una gorrita de juez.

### Micro-misión S05-N01-P4 · Cada anillo vale distinto

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Tati
carta: Puntos por anillo | distancia <= 10 → 10 · <= 20 → 5 · <= 30 → 2 · si no, 0
recompensa: xp 15, monedas 5
```

#### Escena
—En el puesto de verdad —dice Tati—, el centro vale más. Diez puntos el rojo chico, cinco el blanco, dos el rojo grande.

#### Gheco sugiere
Con varios premios según la distancia, los `if` van **del más chico al más grande**, y cada uno corta con `return`:

```js
function notaDe(error) {
    if (error <= 1) return 'excelente';
    if (error <= 5) return 'bien';
    return 'a practicar';
}
```

Si el primero no se cumple, ya se sabe que es mayor, y se pregunta el siguiente. El evento ya está armado: solo hay que cambiar la función.

#### Desafío
`puntosDe(distancia)`: 10 puntos hasta 10 del centro, 5 hasta 20, 2 hasta 30, y 0 más lejos. En cada tiro, `#puntos` muestra el total y `#ultimo` lo del último tiro (`+5`).

Cuatro tiros: (150, 75), (165, 75), (175, 75) y (200, 75).

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f6efe3; font-family: system-ui, sans-serif; padding: 20px; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; display: block; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
<p>Puntos: <span id="puntos">0</span> <span id="ultimo"></span></p>
```

#### Eventos
```
click #lienzo 150 75
click #lienzo 165 75
click #lienzo 175 75
click #lienzo 200 75
```

#### Estado
```
#puntos
#ultimo
```

#### Código inicial
```javascript
const lienzo = document.querySelector('#lienzo');
const blanco = { x: 150, y: 75 };
let puntos = 0;

function puntosDe(distancia) {
  return distancia <= 30 ? 10 : 0;
}

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  const distancia = Math.hypot(e.clientX - caja.left - blanco.x, e.clientY - caja.top - blanco.y);
  const ganados = puntosDe(distancia);
  puntos += ganados;
  document.querySelector('#puntos').textContent = puntos;
  document.querySelector('#ultimo').textContent = `+${ganados}`;
});
```

#### Salida esperada
```
── Estado ──
#puntos: 17
#ultimo: +0
```

#### Solución
```javascript
const lienzo = document.querySelector('#lienzo');
const blanco = { x: 150, y: 75 };
let puntos = 0;

function puntosDe(distancia) {
  if (distancia <= 10) return 10;
  if (distancia <= 20) return 5;
  if (distancia <= 30) return 2;
  return 0;
}

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  const distancia = Math.hypot(e.clientX - caja.left - blanco.x, e.clientY - caja.top - blanco.y);
  const ganados = puntosDe(distancia);
  puntos += ganados;
  document.querySelector('#puntos').textContent = puntos;
  document.querySelector('#ultimo').textContent = `+${ganados}`;
});
```

#### Al superarla
Diez, cinco, dos y cero: diecisiete. Tati anota el número en la pizarra del puesto, con tiza. —El primer récord del juego.

#### Imagen
- Un blanco con números pintados en cada anillo (sin números legibles) y una pizarra al costado con un número escrito en tiza.
- Tati escribe en la pizarra en puntas de pie.

### Micro-misión S05-N01-P5 · Tres patitos

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Bruno, Tati
carta: Varios blancos | blancos = blancos.filter((b) => !acertado(b)) · después, volver a dibujar
recompensa: xp 15, monedas 5
```

#### Escena
Bruno trae los patitos de lata del puesto viejo: tres, en fila. —Cada uno que le pegás, se cae.

#### Gheco sugiere
Es el `filter` de R05-N04: el arreglo de blancos se queda con los que **no** recibieron el tiro (los que están a más de su radio del punto). Después, dibujar todo de nuevo: borrar con `clearRect` y un círculo por cada blanco que quedó.

Una función `dibujar()` que se llame al empezar y después de cada tiro mantiene la pantalla igual a lo que dice el arreglo.

`lienzo.width` y `lienzo.height` son el **ancho y el alto** del lienzo. Para borrar todo: `ctx.clearRect(0, 0, lienzo.width, lienzo.height)` limpia el rectángulo que va desde la esquina hasta el otro extremo.

#### Desafío
En cada click, los blancos a los que se les pegó desaparecen: se vuelve a dibujar el lienzo con un círculo amarillo por cada blanco que queda, y `#quedan` dice `Quedan N`.

Tiros en (60, 75), (240, 80) y (10, 10).

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f6efe3; font-family: system-ui, sans-serif; padding: 20px; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; display: block; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
<p id="quedan">Quedan 3</p>
```

#### Eventos
```
click #lienzo 60 75
click #lienzo 240 80
click #lienzo 10 10
```

#### Estado
```
#quedan
lienzo
```

#### Código inicial
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
let blancos = [{ x: 60, y: 75 }, { x: 150, y: 75 }, { x: 240, y: 75 }];
const RADIO = 20;

function dibujar() {
  ctx.fillStyle = '#ffd400';
  for (const b of blancos) {
    ctx.beginPath();
    ctx.arc(b.x, b.y, RADIO, 0, Math.PI * 2);
    ctx.fill();
  }
}

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  const x = e.clientX - caja.left;
  const y = e.clientY - caja.top;

  dibujar();
});
dibujar();
```

#### Salida esperada
```
── Estado ──
#quedan: Quedan 1
lienzo: clearRect(0, 0, 300, 150)
lienzo: arc(60, 75, 20, 0, 6.28)
lienzo: fill() #ffd400
lienzo: arc(150, 75, 20, 0, 6.28)
lienzo: fill() #ffd400
lienzo: arc(240, 75, 20, 0, 6.28)
lienzo: fill() #ffd400
lienzo: clearRect(0, 0, 300, 150)
lienzo: arc(150, 75, 20, 0, 6.28)
lienzo: fill() #ffd400
lienzo: arc(240, 75, 20, 0, 6.28)
lienzo: fill() #ffd400
lienzo: clearRect(0, 0, 300, 150)
lienzo: arc(150, 75, 20, 0, 6.28)
lienzo: fill() #ffd400
lienzo: clearRect(0, 0, 300, 150)
lienzo: arc(150, 75, 20, 0, 6.28)
lienzo: fill() #ffd400
```

#### Solución
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
let blancos = [{ x: 60, y: 75 }, { x: 150, y: 75 }, { x: 240, y: 75 }];
const RADIO = 20;

function dibujar() {
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#ffd400';
  for (const b of blancos) {
    ctx.beginPath();
    ctx.arc(b.x, b.y, RADIO, 0, Math.PI * 2);
    ctx.fill();
  }
}

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  const x = e.clientX - caja.left;
  const y = e.clientY - caja.top;
  blancos = blancos.filter((b) => Math.hypot(x - b.x, y - b.y) > RADIO);
  document.querySelector('#quedan').textContent = `Quedan ${blancos.length}`;
  dibujar();
});
dibujar();
```

#### Al superarla
Dos patitos caen, el del medio queda solo. El tercer tiro, al aire. Bruno: —¡Ese no vale, me empujó Tati!

#### Imagen
- Tres patitos de lata amarillos en fila sobre el lienzo: dos caídos de espaldas, uno parado en el medio.
- Bruno y Tati se empujan riéndose.

## S05-N02 · Blancos que se mueven

```meta
tipo: tema
padre: S05-N01
precio: 10
criatura: troll
temas: juegos.bucle, juegos.colisiones
usa: js.canvas
```

### Crónica

Nima le pega a todo lo que está quieto: en el puesto de tiro, ya no hay juego. —En la Feria los blancos **se mueven** —le recuerda {mentor}—. Fue lo primero que aprendiste acá. —Bruno y Tati ponen los patitos en una cinta que gira, y empiezan a aparecer blancos de los costados, cada vez más rápido.

### Objetivos

- Mover un blanco cuadro por cuadro con `requestAnimationFrame`.
- Hacerlo rebotar en los bordes del lienzo.
- Hacer aparecer blancos nuevos cada tanto, en lugares al azar.
- Pegarle a un blanco que se mueve, y contar los que se escapan.

### Antes de empezar

- S05-N01 y el bucle del juego (R05-N02).

### Explicación

#### El bucle, otra vez
Cada cuadro hace lo mismo: **mover**, **borrar** y **dibujar**.
```javascript
function cuadro() {
  for (const b of blancos) b.x += b.vx;      // mover
  ctx.clearRect(0, 0, ANCHO, ALTO);          // borrar
  for (const b of blancos) circulo(b);       // dibujar
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```
En la caja, como en un navegador, hay 60 cuadros por segundo: un blanco que se mueve 2 por cuadro recorre 120 en un segundo.

#### Rebotar
```javascript
if (b.x + b.radio > ANCHO || b.x - b.radio < 0) b.vx = -b.vx;
```

#### Que aparezcan
```javascript
setInterval(() => {
  blancos.push({ x: 0, y: 20 + Math.random() * 110, vx: 3, radio: 15 });
}, 1000);
```
`Math.random()` da un número entre 0 y 1: por `110` y más `20`, entre 20 y 130. (En la caja el azar se repite igual en cada ejecución, así se puede comprobar.)

#### Los que se escapan
El que pasó del borde ya no se ve: se lo saca del arreglo, si no, el juego sigue moviendo blancos invisibles para siempre.
```javascript
const antes = blancos.length;
blancos = blancos.filter((b) => b.x - b.radio <= ANCHO);
escapados += antes - blancos.length;
```

### Código de ejemplo

```javascript
let blanco = { x: 280, vx: 4, radio: 15 };
const ANCHO = 300;
const recorrido = [];
for (let cuadro = 0; cuadro < 6; cuadro++) {
  blanco.x += blanco.vx;
  if (blanco.x + blanco.radio > ANCHO || blanco.x - blanco.radio < 0) blanco.vx = -blanco.vx;
  recorrido.push(blanco.x);
}
console.log('x:', recorrido.join(' → '));
console.log('Al azar, entre 20 y 130:', [1, 2, 3].map(() => 20 + Math.random() * 110).every((y) => y >= 20 && y <= 130));
```

### Salida esperada

```
x: 284 → 288 → 284 → 280 → 276 → 272
Al azar, entre 20 y 130: true
```

### ¿Para qué sirve?

Mover, borrar y dibujar es lo que hacen todos los juegos y animaciones. Sacar lo que ya no se ve (balas, enemigos, partículas) es lo que hace que un juego no se ponga cada vez más lento.

### Errores habituales

**Troll: tirarle a donde estaba.** El blanco se mueve: hay que comparar el tiro con su posición **ahora**, no con la del principio.

**Ogro: el rebote que se traba.** Si el blanco ya pasó el borde y solo se le da vuelta la velocidad, puede quedar del otro lado, temblando. Para que no pase, alcanza con que la velocidad lo lleve hacia adentro.

**Troll: los blancos invisibles.** Si no se sacan los que se fueron, el arreglo crece sin parar.

### Micro-misión S05-N02-P1 · El patito que cruza

```meta
lugar: El puesto de tiro, la cinta que gira
personajes: Nima, Gheco, Bruno
carta: Mover | function cuadro() { b.x += 2; ctx.clearRect(…); dibujar(b); requestAnimationFrame(cuadro); }
recompensa: xp 10, oro 10
```

#### Escena
Bruno pone en marcha la cinta y el primer patito cruza… o tendría que cruzar: está quieto.

#### Gheco sugiere
Es el bucle de R05-N02: en cada cuadro, **mover, borrar, dibujar** y pedir el siguiente con `requestAnimationFrame(cuadro)`. Ya hay una función que dibuja el patito: usala.

Si el patito queda dibujado varias veces (la estela), te falta el borrado o está después del dibujo.

#### Desafío
En cada cuadro, el patito avanza 2 a la derecha, se borra el lienzo y se lo dibuja.

En un segundo (60 cuadros), el patito llega a x = 120.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
```

#### Eventos
```
cuadros 60
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
const patito = { x: 0, y: 75, radio: 15 };

function dibujar() {
  ctx.fillStyle = '#ffd400';
  ctx.beginPath();
  ctx.arc(patito.x, patito.y, patito.radio, 0, Math.PI * 2);
  ctx.fill();
}

function cuadro() {
  dibujar();
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 300, 150)
lienzo: arc(120, 75, 15, 0, 6.28)
lienzo: fill() #ffd400
```

#### Solución
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
const patito = { x: 0, y: 75, radio: 15 };

function dibujar() {
  ctx.fillStyle = '#ffd400';
  ctx.beginPath();
  ctx.arc(patito.x, patito.y, patito.radio, 0, Math.PI * 2);
  ctx.fill();
}

function cuadro() {
  patito.x += 2;
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  dibujar();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
El patito cruza el lienzo, suave. Bruno lo sigue con el dedo y se olvida de tirar.

#### Imagen
- Un patito de lata amarillo deslizándose sobre una cinta de madera, con una estela de movimiento.
- Bruno lo sigue con el dedo, hipnotizado.

### Micro-misión S05-N02-P2 · El que rebota

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Tati
carta: Rebote | if (b.x + b.radio > ANCHO || b.x - b.radio < 0) b.vx = -b.vx
recompensa: xp 10, oro 10
```

#### Escena
El patito llega al borde y sigue de largo, fuera del lienzo. Tati lo espera del otro lado, pero no vuelve.

#### Gheco sugiere
El rebote de R05-N02: guardá la velocidad en el objeto (`vx`), sumala a la posición en cada cuadro y, al tocar un borde, dale vuelta el signo (`vx = -vx`).

Un círculo toca el borde derecho cuando su centro **más el radio** pasa el ancho del lienzo (`lienzo.width`), y el izquierdo cuando su centro **menos el radio** es menor que 0.

#### Desafío
El patito empieza con velocidad `vx` en 4, y cuando toca un borde (con su radio), la velocidad se da vuelta.

Después de 50 cuadros, el patito ya rebotó en la derecha y va volviendo.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
```

#### Eventos
```
cuadros 50
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
const patito = { x: 150, y: 75, vx: 4, radio: 15 };

function cuadro() {
  patito.x += patito.vx;
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#ffd400';
  ctx.beginPath();
  ctx.arc(patito.x, patito.y, patito.radio, 0, Math.PI * 2);
  ctx.fill();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 300, 150)
lienzo: arc(222, 75, 15, 0, 6.28)
lienzo: fill() #ffd400
```

#### Solución
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
const patito = { x: 150, y: 75, vx: 4, radio: 15 };

function cuadro() {
  patito.x += patito.vx;
  if (patito.x + patito.radio > lienzo.width || patito.x - patito.radio < 0) patito.vx = -patito.vx;
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#ffd400';
  ctx.beginPath();
  ctx.arc(patito.x, patito.y, patito.radio, 0, Math.PI * 2);
  ctx.fill();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
El patito toca el borde y vuelve, como una pelota. Tati lo espera de este lado y lo saluda cada vez que pasa.

#### Imagen
- Un patito de lata que rebota contra el borde de madera del lienzo, con una chispita amarilla en el choque.
- Tati lo saluda con la mano.

### Micro-misión S05-N02-P3 · Uno por segundo

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Bruno
carta: Aparecer | setInterval(() => blancos.push({ x: 0, y: 20 + Math.random() * 110, vx: 3 }), 1000)
recompensa: xp 10, oro 10
```

#### Escena
—Uno solo es aburrido —dice Bruno—. Que salgan de a uno, cada segundo, cada uno a otra altura.

#### Gheco sugiere
Para que aparezcan cosas cada tanto, un `setInterval` (Senda del Escaparate) agrega un objeto nuevo al arreglo; y el bucle de cuadros mueve y dibuja **todos** los que haya.

`Math.random()` da un número al azar entre 0 y 1 (sin llegar a 1). Para un número entre 20 y 130, se lo estira y se lo corre:

```js
const alto = 50 + Math.random() * 100;   // entre 50 y 150
```

#### Desafío
Cada 1000 ms aparece un blanco nuevo en `x = 0`, a una altura al azar entre 20 y 130, con `vx` en 3. `#blancos` muestra cuántos hay.

A los 3,5 segundos hay 3 blancos.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f6efe3; font-family: system-ui, sans-serif; padding: 20px; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; display: block; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
<p>Blancos: <span id="blancos">0</span></p>
```

#### Eventos
```
esperar 3500
```

#### Estado
```
#blancos
```

#### Código inicial
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
const blancos = [];

function cuadro() {
  for (const b of blancos) b.x += b.vx;
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#ffd400';
  for (const b of blancos) {
    ctx.beginPath();
    ctx.arc(b.x, b.y, 15, 0, Math.PI * 2);
    ctx.fill();
  }
  document.querySelector('#blancos').textContent = blancos.length;
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#blancos: 3
```

#### Solución
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
const blancos = [];

setInterval(() => {
  blancos.push({ x: 0, y: 20 + Math.random() * 110, vx: 3 });
}, 1000);

function cuadro() {
  for (const b of blancos) b.x += b.vx;
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#ffd400';
  for (const b of blancos) {
    ctx.beginPath();
    ctx.arc(b.x, b.y, 15, 0, Math.PI * 2);
    ctx.fill();
  }
  document.querySelector('#blancos').textContent = blancos.length;
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
Los patitos salen de a uno, cada uno a su altura, como los blancos del primer día. Nima los mira y no tira todavía: espera.

#### Imagen
- Tres patitos de lata a distintas alturas cruzando el lienzo en diagonal escalonada.
- Nima, con el arco bajo, mira con calma.

### Micro-misión S05-N02-P4 · Tirarle al que se mueve

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Lumina
carta: Ahora | Math.hypot(x - patito.x, y - patito.y) <= patito.radio (la posición de este momento)
recompensa: xp 15, monedas 5
```

#### Escena
Nima espera el momento. El patito pasa por el medio, y ella tira justo cuando está ahí. El juego dice *Afuera*. —El juego sigue mirando dónde estaba al principio —dice {mentor}.

#### Gheco sugiere
Si el blanco se mueve, hay que comparar el tiro con dónde está **en el momento del click**: el objeto ya tiene su posición actualizada en cada cuadro, así que alcanza con leerla en el evento.

Para frenarlo, su velocidad pasa a 0: el bucle sigue sumando, pero suma nada.

#### Desafío
En el click, se compara con la posición **actual** del patito: si le pegaste, se frena (`vx = 0`) y `#resultado` dice `¡Le pegaste en x = 120!` (redondeado).

A los 40 cuadros, el patito va por x = 120: Nima tira ahí.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f6efe3; font-family: system-ui, sans-serif; padding: 20px; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; display: block; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
<p id="resultado"></p>
```

#### Eventos
```
cuadros 40
click #lienzo 120 75
cuadros 10
```

#### Estado
```
#resultado
lienzo
```

#### Código inicial
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
const patito = { x: 0, y: 75, vx: 3, radio: 20 };
const inicio = { ...patito };

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  const x = e.clientX - caja.left;
  const y = e.clientY - caja.top;
  const acierto = Math.hypot(x - inicio.x, y - inicio.y) <= patito.radio;
  document.querySelector('#resultado').textContent = acierto ? `¡Le pegaste en x = ${Math.round(patito.x)}!` : 'Afuera';
});

function cuadro() {
  patito.x += patito.vx;
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#ffd400';
  ctx.beginPath();
  ctx.arc(patito.x, patito.y, patito.radio, 0, Math.PI * 2);
  ctx.fill();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#resultado: ¡Le pegaste en x = 120!
lienzo: clearRect(0, 0, 300, 150)
lienzo: arc(120, 75, 20, 0, 6.28)
lienzo: fill() #ffd400
```

#### Solución
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
const patito = { x: 0, y: 75, vx: 3, radio: 20 };

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  const x = e.clientX - caja.left;
  const y = e.clientY - caja.top;
  const acierto = Math.hypot(x - patito.x, y - patito.y) <= patito.radio;
  if (acierto) patito.vx = 0;
  document.querySelector('#resultado').textContent = acierto ? `¡Le pegaste en x = ${Math.round(patito.x)}!` : 'Afuera';
});

function cuadro() {
  patito.x += patito.vx;
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#ffd400';
  ctx.beginPath();
  ctx.arc(patito.x, patito.y, patito.radio, 0, Math.PI * 2);
  ctx.fill();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
*¡Le pegaste!* El patito se queda quieto donde lo alcanzó la flecha. {mentor} enciende su farolito. —Tiraste en el momento justo. Ni antes ni después.

#### Imagen
- Un patito de lata frenado en el medio del lienzo con una flecha de luz clavada, y una estela que se apaga detrás.
- Lumina, la luciérnaga gigante con alas de vidrio, enciende su farolito; Nima baja el arco, tranquila.

### Micro-misión S05-N02-P5 · Los que se escapan

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Tati
carta: Sacar los que salen | const antes = blancos.length · blancos = blancos.filter((b) => b.x - RADIO <= ANCHO) · escapados += antes - blancos.length
recompensa: xp 15, monedas 5
```

#### Escena
Tati se queda mirando la cuenta de blancos: 10, 20, 50… y el juego cada vez más lento. Los patitos que se fueron por el borde siguen ahí, invisibles, moviéndose para siempre.

#### Gheco sugiere
En cada cuadro, después de mover, se separan los que ya **salieron enteros**: el centro menos el radio pasó el ancho del lienzo. Se pueden contar con la diferencia de largos antes y después del `filter` (R05-N04):

```js
const antes = autos.length;
autos = autos.filter((a) => a.x - RADIO <= lienzo.width);
fuera += antes - autos.length;
```

Sacarlos importa: si no, el arreglo crece sin fin y el juego se pone lento.

#### Desafío
En cada cuadro, los patitos que ya salieron enteros por el borde derecho se sacan y se cuentan como `escapados`. Se muestran los dos números: los que hay y los que se escaparon.

A los 5 segundos, con un patito nuevo cada medio segundo que cruza en poco más de un segundo.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f6efe3; font-family: system-ui, sans-serif; padding: 20px; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; display: block; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
<p>En el lienzo: <span id="blancos">0</span> · Se escaparon: <span id="escapados">0</span></p>
```

#### Eventos
```
esperar 5000
```

#### Estado
```
#blancos
#escapados
```

#### Código inicial
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
const RADIO = 15;
let blancos = [];
let escapados = 0;

setInterval(() => blancos.push({ x: -RADIO, y: 75, vx: 5 }), 500);

function cuadro() {
  for (const b of blancos) b.x += b.vx;

  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#ffd400';
  for (const b of blancos) {
    ctx.beginPath();
    ctx.arc(b.x, b.y, RADIO, 0, Math.PI * 2);
    ctx.fill();
  }
  document.querySelector('#blancos').textContent = blancos.length;
  document.querySelector('#escapados').textContent = escapados;
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#blancos: 3
#escapados: 7
```

#### Solución
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
const RADIO = 15;
let blancos = [];
let escapados = 0;

setInterval(() => blancos.push({ x: -RADIO, y: 75, vx: 5 }), 500);

function cuadro() {
  for (const b of blancos) b.x += b.vx;
  const antes = blancos.length;
  blancos = blancos.filter((b) => b.x - RADIO <= lienzo.width);
  escapados += antes - blancos.length;
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#ffd400';
  for (const b of blancos) {
    ctx.beginPath();
    ctx.arc(b.x, b.y, RADIO, 0, Math.PI * 2);
    ctx.fill();
  }
  document.querySelector('#blancos').textContent = blancos.length;
  document.querySelector('#escapados').textContent = escapados;
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
En el lienzo quedan solo los que se ven, y la cuenta de los que se escaparon sube. Tati la mira con los ojos entrecerrados. —Eso es para que Nima no se agrande.

#### Imagen
- Patitos de lata que salen por el borde derecho del lienzo y caen en un canasto de madera.
- Tati cuenta los patitos del canasto con los dedos.

## S05-N03 · La ronda: tiempo, combos y niveles

```meta
tipo: tema
padre: S05-N02
precio: 10
criatura: ogre
temas: juegos.estados, juegos.bucle
usa: js.canvas, js.eventos
```

### Crónica

Ya hay blancos que se mueven, que aparecen y que se escapan. Pero un juego necesita **reglas**: cuánto dura una ronda, cuánto vale cada tiro, cuándo se pone difícil. Bruno y Tati las discuten a los gritos. Nima los deja discutir y escribe las reglas en la pizarra del puesto.

### Objetivos

- Llevar una cuenta regresiva y terminar la ronda al llegar a cero.
- Premiar los aciertos seguidos con un **combo** que se corta al errar.
- Dibujar los puntos y el tiempo en el lienzo, en cada cuadro.
- Subir de nivel cada tantos puntos, y llamar a Destello con una tecla para duplicar los puntos un rato.

### Antes de empezar

- S05-N02 (blancos que se mueven).

### Explicación

#### La cuenta regresiva
```javascript
let tiempo = 10;
const reloj = setInterval(() => {
  tiempo--;
  if (tiempo === 0) {
    clearInterval(reloj);
    terminar();
  }
}, 1000);
```

#### El combo
```javascript
if (acierto) {
  combo++;
  puntos += 10 * combo;   // 10, 20, 30…
} else {
  combo = 0;
}
```

#### Lo que se ve encima: el HUD
El texto de los puntos y el tiempo (el **HUD**, como en los juegos) se dibuja **en cada cuadro**, después del `clearRect`; si no, el borrado se lo lleva.
```javascript
ctx.fillStyle = 'white';
ctx.font = '14px monospace';
ctx.fillText(`Puntos: ${puntos}`, 10, 20);
```

#### Niveles
```javascript
const nivel = 1 + Math.floor(puntos / 50);     // 0-49: 1, 50-99: 2…
const velocidad = 2 * 1.5 ** (nivel - 1);      // cada nivel, un 50 % más rápido
```

#### Destello
El ciervo de luz de Nima aparece **una vez por ronda**, cuando ella lo llama (la tecla `d`), y durante 3 segundos todos los puntos valen el doble:
```javascript
setTimeout(() => (destello = false), 3000);
```

### Código de ejemplo

```javascript
let puntos = 0;
let combo = 0;
for (const acierto of [true, true, false, true]) {
  if (acierto) {
    combo++;
    puntos += 10 * combo;
  } else {
    combo = 0;
  }
  console.log(`${acierto ? 'acierto' : 'error  '} · combo ${combo} · puntos ${puntos}`);
}
for (const p of [0, 49, 50, 120]) {
  const nivel = 1 + Math.floor(p / 50);
  console.log(`${p} puntos → nivel ${nivel}, velocidad ${(2 * 1.5 ** (nivel - 1)).toFixed(2)}`);
}
```

### Salida esperada

```
acierto · combo 1 · puntos 10
acierto · combo 2 · puntos 30
error   · combo 0 · puntos 30
acierto · combo 1 · puntos 40
0 puntos → nivel 1, velocidad 2.00
49 puntos → nivel 1, velocidad 2.00
50 puntos → nivel 2, velocidad 3.00
120 puntos → nivel 3, velocidad 4.50
```

### ¿Para qué sirve?

Todos los juegos tienen reglas así: tiempo, combos, niveles, poderes que duran un rato. Son números que cambian según lo que pasa, y que hay que mostrar siempre en pantalla.

### Errores habituales

**Troll: el reloj que sigue después del fin.** Si no se cancela, `tiempo` pasa a -1, -2… y la ronda no termina nunca.

**Ogro: el HUD dibujado una sola vez.** El `clearRect` del primer cuadro lo borra.

**Ogro: Destello infinito.** Si la tecla se puede apretar siempre, el doble de puntos dura toda la ronda. Una vez por ronda, con una variable que lo anote.

### Micro-misión S05-N03-P1 · Diez segundos

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Tati
carta: Cuenta regresiva | setInterval(() => { tiempo--; if (tiempo === 0) { clearInterval(reloj); … } }, 1000)
recompensa: xp 10, oro 10
```

#### Escena
Tati pone un reloj de arena de diez segundos en el mostrador. —¡Ronda! —grita. Pero el reloj del juego sigue contando para abajo: -1, -2, -3…

#### Gheco sugiere
Una cuenta regresiva es un `setInterval` de 1000 ms que resta uno y muestra. Cuando llega a cero, **se frena a sí mismo** con `clearInterval` (por eso se guarda el número en una variable) y muestra el aviso final.

Si no se frena, sigue para siempre: −1, −2…

#### Desafío
La ronda dura 10 segundos: `#tiempo` muestra los que quedan, y al llegar a cero dice `¡Tiempo!` y el reloj se frena.

A los 12 segundos la ronda ya terminó y no queda ningún temporizador.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f6efe3; font-family: system-ui, sans-serif; padding: 20px; font-size: 22px; }
</style>
<p id="tiempo">10</p>
```

#### Eventos
```
esperar 12000
```

#### Estado
```
#tiempo
temporizadores
```

#### Código inicial
```javascript
let tiempo = 10;
const pantalla = document.querySelector('#tiempo');

const reloj = setInterval(() => {
  tiempo--;
  pantalla.textContent = tiempo;
}, 1000);
```

#### Salida esperada
```
── Estado ──
#tiempo: ¡Tiempo!
temporizadores: 0
```

#### Solución
```javascript
let tiempo = 10;
const pantalla = document.querySelector('#tiempo');

const reloj = setInterval(() => {
  tiempo--;
  pantalla.textContent = tiempo;
  if (tiempo === 0) {
    clearInterval(reloj);
    pantalla.textContent = '¡Tiempo!';
  }
}, 1000);
```

#### Al superarla
Diez, nueve, ocho… *¡Tiempo!* Y ahí se queda. Tati da vuelta el reloj de arena, satisfecha.

#### Imagen
- Un reloj de arena de madera y vidrio sobre el mostrador del puesto, con la arena terminando de caer.
- Tati, con las manos en la cintura, satisfecha.

### Micro-misión S05-N03-P2 · El combo de Bruno

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Bruno
carta: Combo | acierto: combo++, puntos += 10 * combo · error: combo = 0
recompensa: xp 10, oro 10
```

#### Escena
Bruno quiere que el que acierta seguido gane más: el primero 10, el segundo 20, el tercero 30. Y que un error lo corte.

#### Gheco sugiere
Un **combo** es un contador que sube con cada acierto seguido y vuelve a 0 con un error. Los puntos de cada acierto dependen del combo: 10 por el combo.

Pensá el orden adentro del acierto: primero sube el combo y después se suman los puntos con el combo nuevo. Si no, el primer acierto vale 0.

#### Desafío
Cada acierto seguido sube el combo y vale 10 por el combo (el primero 10, el segundo 20…); un error corta el combo a 0. Cada tiro se muestra como `✓ x1 → 10`.

La ronda de Bruno: acierto, acierto, error, acierto, acierto, acierto.

#### Código inicial
```javascript
let puntos = 0;
let combo = 0;

function tiro(acierto) {
  if (acierto) puntos += 10;
  console.log(`${acierto ? '✓' : '✗'} x${combo} → ${puntos}`);
}

for (const acierto of [true, true, false, true, true, true]) tiro(acierto);
console.log(`Total: ${puntos}`);
```

#### Salida esperada
```
✓ x1 → 10
✓ x2 → 30
✗ x0 → 30
✓ x1 → 40
✓ x2 → 60
✓ x3 → 90
Total: 90
```

#### Solución
```javascript
let puntos = 0;
let combo = 0;

function tiro(acierto) {
  if (acierto) {
    combo++;
    puntos += 10 * combo;
  } else {
    combo = 0;
  }
  console.log(`${acierto ? '✓' : '✗'} x${combo} → ${puntos}`);
}

for (const acierto of [true, true, false, true, true, true]) tiro(acierto);
console.log(`Total: ${puntos}`);
```

#### Al superarla
Noventa puntos. Bruno hace la cuenta con los dedos y no le da. —¿Noventa? —Gheco le muestra los renglones uno por uno.

#### Imagen
- Una fila de flechas de luz en un blanco, tres juntas al final, con chispas cada vez más grandes.
- Bruno cuenta con los dedos, confundido; Gheco le señala la cuenta.

### Micro-misión S05-N03-P3 · Los números en el lienzo

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Tati
carta: HUD | en cada cuadro, después de clearRect: ctx.fillText(`Puntos: ${puntos}`, 10, 20)
recompensa: xp 10, oro 10
```

#### Escena
Tati escribió los puntos en el lienzo, arriba a la izquierda, como en los juegos. Pero apenas empieza la ronda, desaparecen.

#### Gheco sugiere
El `clearRect` del bucle **borra todo** lo del lienzo en cada cuadro, también el texto. Lo que se dibuja una sola vez al empezar dura un cuadro y desaparece.

Todo lo que se tiene que ver siempre (los puntos, el tiempo) se dibuja **adentro** del cuadro, después de borrar. `ctx.fillText(texto, x, y)` (R05-N01) dibuja texto; la `y` es la línea de abajo de las letras.

#### Desafío
Los números se dibujan **en el lienzo**, en cada cuadro: `Puntos: N` en (10, 20) y `Tiempo: N` en (220, 20).

Nima acierta al blanco del medio y pasan dos cuadros.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
```

#### Eventos
```
click #lienzo 150 75
cuadros 2
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
let puntos = 0;
const tiempo = 10;

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  if (Math.hypot(e.clientX - caja.left - 150, e.clientY - caja.top - 75) <= 20) puntos += 10;
});

ctx.fillStyle = 'white';
ctx.font = '14px monospace';
ctx.fillText(`Puntos: ${puntos}`, 10, 20);
ctx.fillText(`Tiempo: ${tiempo}`, 220, 20);

function cuadro() {
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#ffd400';
  ctx.beginPath();
  ctx.arc(150, 75, 20, 0, Math.PI * 2);
  ctx.fill();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 300, 150)
lienzo: arc(150, 75, 20, 0, 6.28)
lienzo: fill() #ffd400
lienzo: fillText('Puntos: 10', 10, 20) #ffffff
lienzo: fillText('Tiempo: 10', 220, 20) #ffffff
```

#### Solución
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
let puntos = 0;
const tiempo = 10;

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  if (Math.hypot(e.clientX - caja.left - 150, e.clientY - caja.top - 75) <= 20) puntos += 10;
});

function cuadro() {
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#ffd400';
  ctx.beginPath();
  ctx.arc(150, 75, 20, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = 'white';
  ctx.font = '14px monospace';
  ctx.fillText(`Puntos: ${puntos}`, 10, 20);
  ctx.fillText(`Tiempo: ${tiempo}`, 220, 20);
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
Los puntos y el tiempo quedan arriba, firmes, y cambian en el momento en que Nima acierta. Tati: —Ahora sí parece un juego de verdad.

#### Imagen
- El lienzo del puesto con números blancos arriba a la izquierda y a la derecha, sobre un blanco amarillo.
- Tati señala los números, orgullosa.

### Micro-misión S05-N03-P4 · Más difícil cada vez

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Bruno
carta: Niveles | nivel = 1 + Math.floor(puntos / 50) · velocidad = 2 * 1.5 ** (nivel - 1)
recompensa: xp 15, monedas 5
```

#### Escena
Nima ya no falla. Bruno pide que el juego **se ponga más difícil** a medida que suma puntos: cada cincuenta, los patitos van más rápido.

#### Gheco sugiere
Dos cuentas que hacen falta:

- `Math.floor(n)` redondea **para abajo**: `Math.floor(120 / 50)` da 2. Sirve para «uno más cada tantos»;
- `**` (R05-N05) es la potencia: algo que se multiplica por 1,5 en cada nivel es `inicial * 1.5 ** (nivel - 1)` (en el nivel 1, la potencia da 1).

Para ver si las fórmulas andan, probá con los puntos de la consigna y compará con la salida esperada.

#### Desafío
El nivel empieza en 1 y sube uno cada 50 puntos enteros. La velocidad es 2 en el nivel 1, y en cada nivel es 1,5 veces la del anterior. Se muestra con un decimal: `0 → nivel 1, velocidad 2.0`.

Para 0, 40, 50, 120 y 260 puntos.

#### Código inicial
```javascript
function nivelDe(puntos) {
  return puntos / 50;
}

function velocidadDe(nivel) {
  return 2 * nivel;
}

for (const puntos of [0, 40, 50, 120, 260]) {
  const nivel = nivelDe(puntos);
  console.log(`${puntos} → nivel ${nivel}, velocidad ${velocidadDe(nivel).toFixed(1)}`);
}
```

#### Salida esperada
```
0 → nivel 1, velocidad 2.0
40 → nivel 1, velocidad 2.0
50 → nivel 2, velocidad 3.0
120 → nivel 3, velocidad 4.5
260 → nivel 6, velocidad 15.2
```

#### Solución
```javascript
function nivelDe(puntos) {
  return 1 + Math.floor(puntos / 50);
}

function velocidadDe(nivel) {
  return 2 * 1.5 ** (nivel - 1);
}

for (const puntos of [0, 40, 50, 120, 260]) {
  const nivel = nivelDe(puntos);
  console.log(`${puntos} → nivel ${nivel}, velocidad ${velocidadDe(nivel).toFixed(1)}`);
}
```

#### Al superarla
En el nivel 6 los patitos van a más de quince por cuadro. Bruno sonríe con maldad. —Ahí te quiero ver.

#### Imagen
- Una escalera de patitos de lata cada vez más chicos y rápidos, con estelas más largas.
- Bruno se frota las manos; Nima levanta una ceja.

### Micro-misión S05-N03-P5 · ¡Destello!

```meta
lugar: El puesto de tiro, de noche
personajes: Nima, Gheco, Destello
carta: Una vez por ronda | tecla d: if (!usado) { usado = true; destello = true; setTimeout(() => destello = false, 3000) }
recompensa: xp 15, monedas 5
```

#### Escena
Nima silba bajito y entre los faroles aparece **Destello**, su ciervo de luz amarilla. Mientras está en el puesto, todo brilla el doble. Pero se cansa rápido: viene una sola vez por noche.

#### Gheco sugiere
Un **poder** que dura un rato se arma con dos variables: una que dice si está **activo** y otra que dice si **ya se usó**. Al llamarlo: si ya se usó, no hace nada; si no, se activa, se marca como usado, y un `setTimeout` (R04-N01) lo apaga a los 3 segundos.

Mientras está activo, el acierto vale el doble. Una función `mostrar()` que elija el texto según las dos variables sirve después de cada cambio.

#### Desafío
Con la tecla `d`, si Destello todavía no vino, viene: mientras está, cada acierto vale 20 en vez de 10, y se va a los 3 segundos. Viene una sola vez. `#destello` dice `Destello está acá`, `Destello ya vino` o `Llamá a Destello con D`.

Un acierto, llama a Destello, otro acierto, pasan 3,5 segundos, otro acierto, lo vuelve a llamar (no viene) y un último acierto.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f6efe3; font-family: system-ui, sans-serif; padding: 20px; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; display: block; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
<p>Puntos: <span id="puntos">0</span> · <span id="destello">Llamá a Destello con D</span></p>
```

#### Eventos
```
click #lienzo 150 75
tecla d
click #lienzo 150 75
esperar 3500
click #lienzo 150 75
tecla d
click #lienzo 150 75
```

#### Estado
```
#puntos
#destello
temporizadores
```

#### Código inicial
```javascript
const lienzo = document.querySelector('#lienzo');
let puntos = 0;
let destello = false;

function mostrar() {
  document.querySelector('#puntos').textContent = puntos;
  document.querySelector('#destello').textContent = destello ? 'Destello está acá' : 'Llamá a Destello con D';
}

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  if (Math.hypot(e.clientX - caja.left - 150, e.clientY - caja.top - 75) <= 20) puntos += destello ? 20 : 10;
  mostrar();
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'd') {
    destello = true;
    mostrar();
  }
});
```

#### Salida esperada
```
── Estado ──
#puntos: 50
#destello: Destello ya vino
temporizadores: 0
```

#### Solución
```javascript
const lienzo = document.querySelector('#lienzo');
let puntos = 0;
let destello = false;
let usado = false;

function mostrar() {
  document.querySelector('#puntos').textContent = puntos;
  document.querySelector('#destello').textContent = destello ? 'Destello está acá' : usado ? 'Destello ya vino' : 'Llamá a Destello con D';
}

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  if (Math.hypot(e.clientX - caja.left - 150, e.clientY - caja.top - 75) <= 20) puntos += destello ? 20 : 10;
  mostrar();
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'd' && !usado) {
    usado = true;
    destello = true;
    setTimeout(() => {
      destello = false;
      mostrar();
    }, 3000);
    mostrar();
  }
});
```

#### Al superarla
Destello aparece, todo brilla el doble durante tres segundos, y se va trotando entre los faroles. La segunda vez que Nima silba, solo se ve una lucecita lejos: ya vino esta noche.

#### Imagen
- Destello, un ciervo de luz amarilla, entra trotando al puesto de tiro de noche y todo el lienzo brilla dorado.
- Nima silba con dos dedos; Bruno y Tati miran con la boca abierta.

## S05-N04 · Jefe: el Gran Pato de Hojalata

```meta
tipo: jefe
padre: S05-N03
precio: 10
criatura: dragon
insignia: Tiradora de la Feria
insignia_descripcion: Armaste el Puesto de Tiro en canvas: blancos que se mueven, puntos, tiempo, niveles, Destello y el Gran Pato de Hojalata.
temas: juegos.estados, juegos.guardado
usa: js.canvas, js.eventos, js.almacenamiento, juegos.colisiones
```

### Crónica

El juego está casi listo cuando, del fondo del depósito del puesto, sale rodando algo enorme: el **Gran Pato de Hojalata**, el blanco más grande que tuvo la Feria. Tiene un corazón a cuerda y cinco abolladuras de los cinco tiros que lo voltearon una vez, hace treinta años. Nadie lo volvió a voltear desde entonces.

—Dicen que el último que lo volteó —dice Tati— fue el **Vidriero**. —Bruno le da cuerda. El Pato abre el pico de lata, grazna como una trompeta y empieza a cruzar el lienzo.

### Objetivos

- Ordenar el juego en **estados** (`inicio`, `jugando`, `fin`) y que cada tecla y cada cuadro hagan lo suyo según el estado.
- Guardar una tabla de récords (los tres mejores) en `localStorage`, como JSON.
- Armar un enemigo con **vida**, una barra que la muestra y daño por cada tiro.
- Pausar el juego con una tecla, y juntar todo en una partida completa contra el Pato.

### Antes de empezar

- Todo el Puesto de Tiro (S05-N01 a N03), JSON y `localStorage` (R02-N06) y Junta las Gemas (R05-N06).

### Explicación

#### Los estados del juego
Un juego no hace siempre lo mismo: en la pantalla de inicio espera una tecla, jugando mueve y cuenta, y al final muestra los puntos. Una variable `estado` dice en cuál está:
```javascript
let estado = 'inicio';
document.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && estado !== 'jugando') empezar();
});
function cuadro() {
  if (estado === 'jugando') mover();
  dibujar();
  requestAnimationFrame(cuadro);
}
```

#### La tabla de récords
```javascript
const tabla = JSON.parse(localStorage.getItem('tiro') ?? '[]');
tabla.push({ nombre: 'Nima', puntos: 50 });
tabla.sort((a, b) => b.puntos - a.puntos);
localStorage.setItem('tiro', JSON.stringify(tabla.slice(0, 3)));
```

#### Un enemigo con vida
```javascript
const pato = { x: 40, y: 60, vx: 2, vida: 5 };
ctx.fillRect(10, 10, pato.vida * 20, 8);   // la barra: 20 por cada vida
```

#### Pausa
Con `pausa = !pausa` se alterna. En pausa el bucle **sigue** (para dibujar el cartel), pero no mueve nada.

### Código de ejemplo

```javascript
localStorage.setItem('tiro', JSON.stringify([{ nombre: 'Bruno', puntos: 40 }]));

function guardar(nombre, puntos) {
  const tabla = JSON.parse(localStorage.getItem('tiro') ?? '[]');
  tabla.push({ nombre, puntos });
  tabla.sort((a, b) => b.puntos - a.puntos);
  localStorage.setItem('tiro', JSON.stringify(tabla.slice(0, 3)));
}

guardar('Tati', 35);
guardar('Nima', 50);
guardar('Teo', 5);
console.log(JSON.parse(localStorage.getItem('tiro')).map((r) => `${r.nombre} ${r.puntos}`).join(' · '));
```

### Salida esperada

```
Nima 50 · Bruno 40 · Tati 35
```

### ¿Para qué sirve?

Los estados ordenan cualquier programa que «cambia de modo»: un juego, un formulario de varios pasos, un reproductor de música (parado, sonando, en pausa). La tabla de récords es el mismo `JSON` + `localStorage` que guarda las preferencias de cualquier página.

### Errores habituales

**Ogro: Enter en el medio de la partida.** Si Enter siempre empieza, apretarlo jugando reinicia todo. Mirá el estado.

**Ogro: la vida negativa.** Si el Pato recibe un tiro con vida 0, queda en -1 y la barra se dibuja para el otro lado. Al llegar a 0, se termina.

**Goblin: `JSON.parse` de `null`.** Sin récords guardados, `getItem` da `null`; el `?? '[]'` lo evita.

### Micro-misión S05-N04-P1 · Inicio, jugando, fin

```meta
lugar: El puesto de tiro, la pantalla del juego
personajes: Nima, Gheco, Tati
carta: Estados | let estado = 'inicio' · Enter: empezar() · al terminar el tiempo: estado = 'fin'
recompensa: xp 10, oro 10
```

#### Escena
Tati quiere una pantalla de inicio como en los juegos de verdad: *Apretá Enter para empezar*. Y al final, los puntos.

#### Gheco sugiere
Los **estados** del juego (R05-N06): un texto que dice en qué momento está, y cada parte del programa lo mira antes de actuar.

- la tecla Enter solo arranca si el estado **no** es `'jugando'`: así no se puede empezar dos veces;
- al arrancar, se cambia el estado y un `setTimeout` deja anotado el final de la ronda.

Una función por cambio (`empezar`, `terminar`) que cambie el estado **y** el cartel deja todo en un solo lugar.

#### Desafío
Con `estado` en `inicio`, `#pantalla` dice `Apretá Enter para empezar`. Enter (solo si no se está jugando) pasa a `jugando`, dice `¡A jugar!` y arranca una ronda de 5 segundos; al terminar, pasa a `fin` y dice `Fin de la ronda · Enter para jugar otra vez`.

Aprietan otra tecla (no pasa nada), Enter, y esperan 6 segundos.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f6efe3; font-family: system-ui, sans-serif; padding: 20px; font-size: 20px; }
</style>
<p id="pantalla"></p>
<p>Estado: <span id="estado"></span></p>
```

#### Eventos
```
tecla x
tecla Enter
esperar 6000
```

#### Estado
```
#pantalla
#estado
temporizadores
```

#### Código inicial
```javascript
let estado = 'inicio';
const pantalla = document.querySelector('#pantalla');

function mostrar(texto) {
  pantalla.textContent = texto;
  document.querySelector('#estado').textContent = estado;
}

function empezar() {
  estado = 'jugando';
  mostrar('¡A jugar!');
}

document.addEventListener('keydown', () => empezar());
mostrar('Apretá Enter para empezar');
```

#### Salida esperada
```
── Estado ──
#pantalla: Fin de la ronda · Enter para jugar otra vez
#estado: fin
temporizadores: 0
```

#### Solución
```javascript
let estado = 'inicio';
const pantalla = document.querySelector('#pantalla');

function mostrar(texto) {
  pantalla.textContent = texto;
  document.querySelector('#estado').textContent = estado;
}

function empezar() {
  estado = 'jugando';
  mostrar('¡A jugar!');
  setTimeout(() => {
    estado = 'fin';
    mostrar('Fin de la ronda · Enter para jugar otra vez');
  }, 5000);
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && estado !== 'jugando') empezar();
});
mostrar('Apretá Enter para empezar');
```

#### Al superarla
Inicio, ronda, fin. Y otra vez. Tati juega cinco rondas seguidas sin tirar ni una flecha, solo para ver las pantallas.

#### Imagen
- El lienzo del puesto con un cartel de luz de pantalla de inicio, estilo juego de feria antiguo (sin texto legible).
- Tati aprieta una tecla grande de madera, emocionada.

### Micro-misión S05-N04-P2 · La tabla de los mejores

```meta
lugar: El puesto de tiro, la pizarra de récords
personajes: Nima, Gheco, Bruno, Tati
carta: Top 3 | JSON.parse(localStorage.getItem('tiro') ?? '[]') · push · sort · slice(0, 3) · JSON.stringify
recompensa: xp 10, oro 10
```

#### Escena
La pizarra del puesto ya tiene dos récords: Bruno 40, Tati 35. Bruno quiere que el juego guarde **los tres mejores**, con su nombre, y que la pizarra se dibuje sola.

#### Gheco sugiere
Una **tabla de récords** es un arreglo de objetos guardado en `localStorage` como JSON (R02-N06). Cada partida: leer (o `[]` si no hay), agregar con `push`, ordenar de mayor a menor (Senda del Archivo), cortar con `slice(0, 3)` y guardar.

Para dibujarla, `replaceChildren()` vacía la lista, y después un `<li>` por récord (R02-N02).

#### Desafío
`guardar(nombre, puntos)` lee la tabla guardada (clave `tiro`), agrega el nuevo, ordena de mayor a menor, deja los tres primeros y la vuelve a guardar. `dibujarTabla()` pone un `<li>` por récord en `#records`: `Nima — 50`.

Juegan Nima (50), Lucio (10) y Bengala (45).

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f6efe3; font-family: system-ui, sans-serif; padding: 20px; }
  ol { font-family: monospace; font-size: 18px; }
</style>
<h2>Los mejores</h2>
<ol id="records"></ol>
```

#### Almacenamiento
```
local tiro = [{"nombre":"Bruno","puntos":40},{"nombre":"Tati","puntos":35}]
```

#### Estado
```
#records li
local tiro
```

#### Código inicial
```javascript
function guardar(nombre, puntos) {
  const tabla = localStorage.getItem('tiro') ?? [];
  tabla.push({ nombre, puntos });
  localStorage.setItem('tiro', tabla);
}

function dibujarTabla() {
  const lista = document.querySelector('#records');
  lista.replaceChildren();
}

guardar('Nima', 50);
guardar('Lucio', 10);
guardar('Bengala', 45);
dibujarTabla();
```

#### Salida esperada
```
── Estado ──
#records li: Nima — 50
#records li: Bengala — 45
#records li: Bruno — 40
local tiro: [{"nombre":"Nima","puntos":50},{"nombre":"Bengala","puntos":45},{"nombre":"Bruno","puntos":40}]
```

#### Solución
```javascript
function guardar(nombre, puntos) {
  const tabla = JSON.parse(localStorage.getItem('tiro') ?? '[]');
  tabla.push({ nombre, puntos });
  tabla.sort((a, b) => b.puntos - a.puntos);
  localStorage.setItem('tiro', JSON.stringify(tabla.slice(0, 3)));
}

function dibujarTabla() {
  const lista = document.querySelector('#records');
  lista.replaceChildren(...JSON.parse(localStorage.getItem('tiro') ?? '[]').map((r) => {
    const li = document.createElement('li');
    li.textContent = `${r.nombre} — ${r.puntos}`;
    return li;
  }));
}

guardar('Nima', 50);
guardar('Lucio', 10);
guardar('Bengala', 45);
dibujarTabla();
```

#### Al superarla
*Nima 50, Bengala 45, Bruno 40.* Tati se quedó afuera del podio. Se cruza de brazos. —Mañana vuelvo.

#### Imagen
- Una pizarra de feria con tres renglones de récords escritos con tiza de colores (sin texto legible).
- Bengala (pirotécnica joven, antiparras de cuero, delantal cerrado, pelo corto rojizo) festeja; Tati, de brazos cruzados.

### Micro-misión S05-N04-P3 · Cinco abolladuras

```meta
lugar: El puesto de tiro, el Gran Pato
personajes: Nima, Gheco, Bruno, el Gran Pato de Hojalata
carta: Vida | acierto: pato.vida-- · ctx.fillRect(10, 10, pato.vida * 20, 8)
recompensa: xp 10, oro 10
```

#### Escena
El Gran Pato cruza el lienzo, despacio, graznando. Bruno le tira y la flecha rebota: un tiro no alcanza. —Cinco tiros —dice Bruno—. Uno por cada abolladura.

#### Gheco sugiere
Un enemigo con **vida** es un número que baja con cada golpe. Lo que lo muestra se calcula **a partir de** ese número: una barra cuyo ancho es la vida multiplicada por un tamaño fijo se achica sola con cada golpe.

El golpe se revisa en el click, con la posición del Pato en ese momento (S05-N02-P4), y la barra se dibuja en el cuadro, después de borrar.

#### Desafío
El Pato tiene `vida: 5`. Cada tiro que le pega (a 25 o menos de su centro, en el momento del tiro) le saca una. En cada cuadro se dibuja arriba la barra roja de vida, con `fillRect(10, 10, vida * 20, 8)`, y `#vida` muestra la vida.

Dos tiros que le pegan mientras cruza.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f6efe3; font-family: system-ui, sans-serif; padding: 20px; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; display: block; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
<p>Vida del Pato: <span id="vida">5</span></p>
```

#### Eventos
```
cuadros 20
click #lienzo 90 60
cuadros 10
click #lienzo 120 60
cuadros 1
```

#### Estado
```
#vida
lienzo
```

#### Código inicial
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
const pato = { x: 30, y: 60, vx: 3, vida: 5 };

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  const x = e.clientX - caja.left;
  const y = e.clientY - caja.top;

});

function cuadro() {
  pato.x += pato.vx;
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#b0bec5';
  ctx.beginPath();
  ctx.arc(pato.x, pato.y, 25, 0, Math.PI * 2);
  ctx.fill();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#vida: 3
lienzo: clearRect(0, 0, 300, 150)
lienzo: fillRect(10, 10, 60, 8) #e53935
lienzo: arc(123, 60, 25, 0, 6.28)
lienzo: fill() #b0bec5
```

#### Solución
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
const pato = { x: 30, y: 60, vx: 3, vida: 5 };

lienzo.addEventListener('click', (e) => {
  const caja = lienzo.getBoundingClientRect();
  const x = e.clientX - caja.left;
  const y = e.clientY - caja.top;
  if (pato.vida > 0 && Math.hypot(x - pato.x, y - pato.y) <= 25) pato.vida--;
  document.querySelector('#vida').textContent = pato.vida;
});

function cuadro() {
  pato.x += pato.vx;
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#e53935';
  ctx.fillRect(10, 10, pato.vida * 20, 8);
  ctx.fillStyle = '#b0bec5';
  ctx.beginPath();
  ctx.arc(pato.x, pato.y, 25, 0, Math.PI * 2);
  ctx.fill();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
Dos abolladuras nuevas en la hojalata, y la barra roja se achica. El Pato grazna, ofendido, y sigue cruzando.

#### Imagen
- Un pato de hojalata gigante, gris plateado, con una llave de cuerda en la espalda y abolladuras, cruzando el lienzo; arriba, una barra roja de vida achicándose.
- Bruno le da ánimo a Nima con el puño en alto.

### Micro-misión S05-N04-P4 · Pausa para respirar

```meta
lugar: El puesto de tiro, el Gran Pato
personajes: Nima, Gheco, Doña Mirta
carta: Pausa | tecla p: pausa = !pausa · if (!pausa) mover() · if (pausa) fillText('Pausa', …)
recompensa: xp 15, monedas 5
```

#### Escena
En el medio de la pelea, Doña Mirta llega con pan con miel recién hecho. Nima no puede dejar pasar un pan con miel. —¡Pausa! —grita. El Pato sigue cruzando, como si nada.

#### Gheco sugiere
Una **pausa** es una variable `true`/`false` que la tecla alterna con `!` (no): `pausa = !pausa` la da vuelta.

En el bucle, la pausa frena solo el **movimiento**: se sigue borrando y dibujando (si no, la pantalla se congela con lo último) y se sigue pidiendo el próximo cuadro. Lo que cambia es que, en pausa, no se suma la velocidad, y se dibuja el cartel.

#### Desafío
La tecla `p` pone y saca la pausa. En pausa, el bucle sigue dibujando pero el Pato no se mueve, y aparece `Pausa` escrito en (125, 80).

Pasan 10 cuadros, Nima aprieta `p` y pasan 30 más: el Pato tiene que seguir donde estaba.

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; display: grid; place-items: center; height: 100vh; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
```

#### Eventos
```
cuadros 10
tecla p
cuadros 30
```

#### Estado
```
lienzo
```

#### Código inicial
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
const pato = { x: 30, y: 60, vx: 3 };
let pausa = false;

document.addEventListener('keydown', (e) => {
  if (e.key === 'p') pausa = true;
});

function cuadro() {
  pato.x += pato.vx;
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#b0bec5';
  ctx.beginPath();
  ctx.arc(pato.x, pato.y, 25, 0, Math.PI * 2);
  ctx.fill();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
lienzo: clearRect(0, 0, 300, 150)
lienzo: arc(60, 60, 25, 0, 6.28)
lienzo: fill() #b0bec5
lienzo: fillText('Pausa', 125, 80) #ffffff
```

#### Solución
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
const pato = { x: 30, y: 60, vx: 3 };
let pausa = false;

document.addEventListener('keydown', (e) => {
  if (e.key === 'p') pausa = !pausa;
});

function cuadro() {
  if (!pausa) pato.x += pato.vx;
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#b0bec5';
  ctx.beginPath();
  ctx.arc(pato.x, pato.y, 25, 0, Math.PI * 2);
  ctx.fill();
  if (pausa) {
    ctx.fillStyle = 'white';
    ctx.fillText('Pausa', 125, 80);
  }
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Al superarla
El Pato se queda quieto en el aire, con una pata levantada, mientras Nima se come el pan con miel. Doña Mirta le deja otro al Pato, por las dudas.

#### Imagen
- El pato de hojalata congelado en el medio del lienzo con una pata levantada, y un cartel de pausa encima.
- Doña Mirta (petisa y redonda, delantal floreado cerrado, pañuelo en la cabeza) le da un pan con miel a Nima; otro pan quedó en el mostrador para el Pato.

### Micro-misión S05-N04-P5 · Jefe: el Gran Pato cae

```meta
lugar: El puesto de tiro, toda la Feria mirando
personajes: Nima, Gheco, Bruno, Tati, Destello, el Gran Pato de Hojalata, Lumina
carta: El juego completo | estados · bucle · vida y barra · tiempo · récord en localStorage
recompensa: xp 50, oro 50, monedas 1
```

#### Escena
Toda la Feria se junta alrededor del puesto: Lucio con su escalera, Bengala con las antiparras, Don Tano con el organito callado, por respeto. Bruno le da toda la cuerda al Gran Pato. —El Vidriero lo volteó en cinco tiros —dice Tati—. Nadie sabe cuánto tardó.

#### Gheco sugiere
Junta toda la Senda:

- los estados de S05-N04-P1, con Enter para arrancar;
- la vida y los golpes de S05-N04-P3;
- el tiempo de la partida: `performance.now()` (R04-N05) al empezar y al terminar; la resta da milisegundos, y dividida por 1000, segundos (`toFixed(1)` para un decimal);
- el récord de `localStorage`, pero acá gana el **más chico**. Si no hay nada guardado, `Infinity` (*infinito*) sirve de reserva: cualquier tiempo es menor.

#### Desafío
- `estado` empieza en `inicio`; Enter (si no se está jugando) arranca la partida: el Pato en `x = 40` con `vida: 5`, y se anota cuándo empezó (`performance.now()`);
- jugando, el Pato avanza 2 por cuadro; cada tiro a 25 o menos de su centro le saca una vida;
- con vida 0: `estado` pasa a `fin`, se calculan los segundos que tardó (con un decimal) y `#pantalla` dice `¡El Pato cayó en 0.8 s!`;
- el mejor tiempo (el más **chico**) se guarda con la clave `mejorTiempo`, y `#record` dice `Récord: …`;
- en cada cuadro se dibujan la barra de vida y el Pato.

La partida de Nima: Enter y cinco tiros mientras el Pato cruza. (El mejor tiempo guardado es de 2.5 s: el del Vidriero.)

#### Página
```html
<style>
  body { margin: 0; background: #1a1206; color: #f6efe3; font-family: system-ui, sans-serif; padding: 20px; }
  canvas { background: #0b1020; outline: 6px solid #8d6e3f; display: block; }
</style>
<canvas id="lienzo" width="300" height="150"></canvas>
<p id="pantalla">Apretá Enter para empezar</p>
<p id="record"></p>
```

#### Almacenamiento
```
local mejorTiempo = 2.5
```

#### Eventos
```
tecla Enter
cuadros 10
click #lienzo 60 60
cuadros 10
click #lienzo 80 60
cuadros 10
click #lienzo 100 60
cuadros 10
click #lienzo 120 60
cuadros 10
click #lienzo 140 60
cuadros 2
```

#### Estado
```
#pantalla
#record
local mejorTiempo
lienzo
```

#### Código inicial
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
let estado = 'inicio';
let pato = { x: 40, y: 60, vx: 2, vida: 5 };
let inicio = 0;

function dibujar() {
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#e53935';
  ctx.fillRect(10, 10, pato.vida * 20, 8);
  ctx.fillStyle = '#b0bec5';
  ctx.beginPath();
  ctx.arc(pato.x, pato.y, 25, 0, Math.PI * 2);
  ctx.fill();
}

function cuadro() {
  dibujar();
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(cuadro);
```

#### Salida esperada
```
── Estado ──
#pantalla: ¡El Pato cayó en 0.8 s!
#record: Récord: 0.8 s
local mejorTiempo: 0.8
lienzo: clearRect(0, 0, 300, 150)
lienzo: fillRect(10, 10, 0, 8) #e53935
lienzo: arc(140, 60, 25, 0, 6.28)
lienzo: fill() #b0bec5
```

#### Solución
```javascript
const lienzo = document.querySelector('#lienzo');
const ctx = lienzo.getContext('2d');
let estado = 'inicio';
let pato = { x: 40, y: 60, vx: 2, vida: 5 };
let inicio = 0;

const mejor = () => Number(localStorage.getItem('mejorTiempo') ?? Infinity);
const mostrarRecord = () => (document.querySelector('#record').textContent = `Récord: ${mejor()} s`);

function empezar() {
  estado = 'jugando';
  pato = { x: 40, y: 60, vx: 2, vida: 5 };
  inicio = performance.now();
  document.querySelector('#pantalla').textContent = '¡A jugar!';
}

function terminar() {
  estado = 'fin';
  const segundos = Number(((performance.now() - inicio) / 1000).toFixed(1));
  document.querySelector('#pantalla').textContent = `¡El Pato cayó en ${segundos} s!`;
  if (segundos < mejor()) localStorage.setItem('mejorTiempo', segundos);
  mostrarRecord();
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && estado !== 'jugando') empezar();
});

lienzo.addEventListener('click', (e) => {
  if (estado !== 'jugando') return;
  const caja = lienzo.getBoundingClientRect();
  const x = e.clientX - caja.left;
  const y = e.clientY - caja.top;
  if (Math.hypot(x - pato.x, y - pato.y) <= 25) pato.vida--;
  if (pato.vida === 0) terminar();
});

function dibujar() {
  ctx.clearRect(0, 0, lienzo.width, lienzo.height);
  ctx.fillStyle = '#e53935';
  ctx.fillRect(10, 10, pato.vida * 20, 8);
  ctx.fillStyle = '#b0bec5';
  ctx.beginPath();
  ctx.arc(pato.x, pato.y, 25, 0, Math.PI * 2);
  ctx.fill();
}

function cuadro() {
  if (estado === 'jugando') pato.x += pato.vx;
  dibujar();
  requestAnimationFrame(cuadro);
}

mostrarRecord();
requestAnimationFrame(cuadro);
```

#### Al superarla
Cinco tiros, cinco abolladuras nuevas, y el Gran Pato de Hojalata se da vuelta panza arriba con un graznido de trompeta que se oye en toda la Feria. En menos de un segundo: más rápido que el Vidriero.

La Feria estalla en aplausos. Destello entra trotando al puesto, se acerca al Pato y le apoya el hocico de luz en la hojalata; el corazón a cuerda hace *tic, tic, tic* y se queda quieto, dormido. Adentro del Pato, en el hueco de la cuerda, Bruno encuentra un papelito doblado, viejo, con la letra del Vidriero: *«Para quien lo voltee más rápido que yo: mirá las estrellas.»*

{mentor} lo lee por encima del hombro de Nima y apaga, despacio, su farolito. —Ya sabés adónde ir.

#### Imagen
- El pato de hojalata gigante dado vuelta panza arriba en el puesto de tiro, con la Feria entera aplaudiendo alrededor de noche (Lucio con su escalera, Bengala, Don Tano con su organito).
- Destello, el ciervo de luz amarilla, apoya el hocico en el pato; Bruno sostiene un papelito viejo doblado y Nima mira el cielo estrellado.
