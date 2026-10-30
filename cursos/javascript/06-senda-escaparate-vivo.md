# RAMA S01 · Senda del Escaparate Vivo: páginas de los Talleres que reaccionan

```meta
tipo: senda
posicion: 6
```

## S01-N01 · El menú que se abre

```meta
tipo: tema
padre: R02-N07
precio: 3
moneda: comodin
criatura: orc
temas: js.dom, js.eventos
usa: html.estructura, css.selectores
```

### Crónica

Con la Avenida encendida, por la Feria entra un carro tirado por un burro, cargado de vitrales envueltos en papel. Lo maneja un chico flaco que viene corriendo al lado del burro, porque nunca camina: **Teo**, el aprendiz de los **Talleres de los Vitrales**.

—¡Me manda **Tesela**! —grita, sin aire—. En los Talleres hacemos las páginas más lindas del mundo: colores, cajas y letras. Pero son **vidrio quieto**. Tocás un botón y no pasa nada. Tesela dice que acá ustedes saben hacer que las cosas **reaccionen**. —Abre el carro: es un **escaparate** entero, lleno de páginas—. ¿Me ayudás a que cobren vida?

### Objetivos

- Abrir y cerrar un menú cambiando una clase con `classList.toggle`.
- Avisar a los lectores de pantalla si el menú está abierto, con `aria-expanded`.
- Cerrar el menú con la tecla Escape y al tocar afuera, con `closest`.
- Armar pestañas que muestran un panel y esconden los demás con `hidden`.

### Antes de empezar

- La Avenida de los Faroles (R02): seleccionar elementos, eventos y delegación.
- Si hiciste el curso de HTML y CSS, vas a reconocer las páginas de los Talleres. Si no, no importa: el HTML ya viene armado.

### Explicación

#### El reparto del trabajo
En los Talleres se aprende que cada lengua hace lo suyo:
- **HTML** dice qué hay (un botón, un menú);
- **CSS** dice cómo se ve (y cómo se ve **abierto**: `.abierto { display: block }`);
- **JavaScript** solo **cambia la clase**. No pinta nada él mismo.

```javascript
const boton = document.querySelector('#menu-boton');
const menu = document.querySelector('#menu');
boton.addEventListener('click', () => {
  menu.classList.toggle('abierto');      // la pone si no está, la saca si está
});
```
`toggle` devuelve `true` si la clase quedó puesta: sirve para saber en qué estado quedó.

#### Que también lo sepa quien no ve
Un lector de pantalla no ve la clase: lee los atributos `aria-*`. El botón de un menú lleva `aria-expanded`, que dice `"true"` o `"false"`:
```javascript
const abierto = menu.classList.toggle('abierto');
boton.setAttribute('aria-expanded', String(abierto));
```

#### Cerrar con Escape y al tocar afuera
```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') menu.classList.remove('abierto');
});
document.addEventListener('click', (e) => {
  if (!e.target.closest('#menu, #menu-boton')) menu.classList.remove('abierto');
});
```
`closest(selector)` sube desde el elemento tocado hasta encontrar uno que cumpla el selector, o devuelve `null`: si devuelve `null`, el click fue **afuera**.

#### Pestañas con `hidden`
El atributo `hidden` esconde un elemento sin CSS. `panel.hidden = true` lo esconde y `false` lo muestra.

### Código de ejemplo

```javascript
document.body.innerHTML = `
  <button id="menu-boton" aria-expanded="false">Menú</button>
  <nav id="menu"><a href="#">Vitrales</a> <a href="#">Talleres</a></nav>`;

const boton = document.querySelector('#menu-boton');
const menu = document.querySelector('#menu');

function alternar() {
  const abierto = menu.classList.toggle('abierto');
  boton.setAttribute('aria-expanded', String(abierto));
  console.log(`Menú ${abierto ? 'abierto' : 'cerrado'} · aria-expanded=${boton.getAttribute('aria-expanded')}`);
}

boton.addEventListener('click', alternar);
boton.click();
boton.click();
console.log('closest desde un enlace:', document.querySelector('a').closest('#menu')?.id);
console.log('closest desde el botón:', boton.closest('#menu'));
```

### Salida esperada

```
Menú abierto · aria-expanded=true
Menú cerrado · aria-expanded=false
closest desde un enlace: menu
closest desde el botón: null
```

### ¿Para qué sirve?

Casi todas las páginas del mundo tienen un menú que se abre en el celular, pestañas, acordeones y ventanitas. Todos funcionan igual: JavaScript cambia una clase o un atributo, y el CSS hace el resto.

### Errores habituales

**Orco: el botón que no está.** Si el `<script>` corre antes de que exista el botón, `querySelector` da `null` y `null.addEventListener` rompe todo. En la caja la página ya está cargada; en tus páginas, poné el script al final o con `defer`.

**Ogro: cerrar al tocar el propio botón.** Si el click en el documento cierra el menú y el click en el botón lo abre, los dos pasan con el mismo click: se abre y se cierra en el mismo instante. Por eso el `closest` mira también el botón.

**Goblin: `aria-expanded` con un booleano.** Los atributos siempre son texto: `setAttribute('aria-expanded', true)` guarda `"true"`, pero leerlo devuelve el texto `"true"`, no el booleano. Compará con `=== 'true'`.

### Micro-misión S01-N01-P1 · El botón de las tres rayas

```meta
lugar: El escaparate de los Talleres, en la Avenida
personajes: Nima, Gheco, Teo
carta: classList.toggle | boton.addEventListener('click', () => menu.classList.toggle('abierto'))
recompensa: xp 10, oro 10
```

#### Escena
La primera página del escaparate es la de los Talleres. Arriba tiene un botón con tres rayas, pero el menú no aparece nunca. —El CSS ya sabe cómo se ve abierto —dice Teo—. Le falta alguien que le avise.

#### Gheco sugiere
Al hacer click en `#menu-boton`, alterná la clase `abierto` del `#menu`.

#### Desafío
Que el click abra el menú (y otro click lo cierre).

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #f6efe3; color: #2b1d0e; }
  header { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: #2b1d0e; color: #f6efe3; }
  #menu-boton { font-size: 22px; background: none; color: inherit; border: 0; cursor: pointer; }
  #menu { display: none; flex-direction: column; background: #3b2a16; padding: 8px 16px; }
  #menu.abierto { display: flex; }
  #menu a { color: #ffd400; padding: 6px 0; }
</style>
<header><button id="menu-boton">☰</button> <strong>Talleres de los Vitrales</strong></header>
<nav id="menu"><a href="#">Vitrales</a><a href="#">El taller</a><a href="#">Pedidos</a></nav>
<main><p style="padding:16px">Bienvenidos a los Talleres.</p></main>
```

#### Eventos
```
click #menu-boton
```

#### Estado
```
#menu @class
```

#### Código inicial
```javascript
const boton = document.querySelector('#menu-boton');
const menu = document.querySelector('#menu');

```

#### Salida esperada
```
── Estado ──
#menu @class: abierto
```

#### Solución
```javascript
const boton = document.querySelector('#menu-boton');
const menu = document.querySelector('#menu');
boton.addEventListener('click', () => {
  menu.classList.toggle('abierto');
});
```

#### Al superarla
El menú baja como una persiana de vidrio. Teo lo abre y lo cierra veinte veces, riéndose.

#### Imagen
- Un escaparate de madera con vidrios en la Avenida de los Faroles, lleno de páginas de colores enmarcadas como vitrales.
- Teo (chico flaco con delantal de cuero manchado de pintura, siempre corriendo) toca un botón con tres rayas; Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) mira.

### Micro-misión S01-N01-P2 · Para los que leen sin ver

```meta
lugar: El escaparate de los Talleres
personajes: Nima, Gheco, Teo
carta: aria-expanded | const abierto = menu.classList.toggle('abierto') · boton.setAttribute('aria-expanded', String(abierto))
recompensa: xp 10, oro 10
```

#### Escena
—En los Talleres hay una regla —dice Teo—: **toda página es para todos**. Hay quien la escucha con un lector de pantalla, y el lector no ve si el menú bajó. Lo lee del botón.

#### Gheco sugiere
Guardá lo que devuelve `toggle` y ponelo en `aria-expanded` como texto.

#### Desafío
Después de dos clicks, el menú queda cerrado y `aria-expanded` en `false`. Mostrá en `#aviso` el estado: `Menú abierto` o `Menú cerrado`.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #f6efe3; color: #2b1d0e; }
  header { display: flex; gap: 12px; padding: 12px 16px; background: #2b1d0e; color: #f6efe3; }
  #menu-boton { font-size: 22px; background: none; color: inherit; border: 0; }
  #menu { display: none; background: #3b2a16; padding: 8px 16px; }
  #menu.abierto { display: block; }
  #menu a { color: #ffd400; margin-right: 12px; }
  #aviso { padding: 16px; font-style: italic; }
</style>
<header><button id="menu-boton" aria-expanded="false" aria-controls="menu">☰</button> <strong>Talleres</strong></header>
<nav id="menu"><a href="#">Vitrales</a><a href="#">Pedidos</a></nav>
<p id="aviso">Menú cerrado</p>
```

#### Eventos
```
click #menu-boton
click #menu-boton
```

#### Estado
```
#menu @class
#menu-boton @aria-expanded
#aviso
```

#### Código inicial
```javascript
const boton = document.querySelector('#menu-boton');
const menu = document.querySelector('#menu');
const aviso = document.querySelector('#aviso');
boton.addEventListener('click', () => {
  menu.classList.toggle('abierto');
  boton.setAttribute('aria-expanded', 'true');
  aviso.textContent = 'Menú abierto';
});
```

#### Salida esperada
```
── Estado ──
#menu @class: (vacío)
#menu-boton @aria-expanded: false
#aviso: Menú cerrado
```

#### Solución
```javascript
const boton = document.querySelector('#menu-boton');
const menu = document.querySelector('#menu');
const aviso = document.querySelector('#aviso');
boton.addEventListener('click', () => {
  const abierto = menu.classList.toggle('abierto');
  boton.setAttribute('aria-expanded', String(abierto));
  aviso.textContent = abierto ? 'Menú abierto' : 'Menú cerrado';
});
```

#### Al superarla
Teo cierra los ojos y le pide a Gheco que le lea el botón. —«Menú, contraído». —Ahora sí es una página de los Talleres.

#### Imagen
- Teo con los ojos tapados con una venda de tela, escuchando; Gheco, el geco, le lee el botón en voz alta.
- El botón de tres rayas brilla con una etiqueta de luz al costado (sin texto legible).

### Micro-misión S01-N01-P3 · La tecla de escape

```meta
lugar: El escaparate de los Talleres
personajes: Nima, Gheco, Teo
carta: Escape | document.addEventListener('keydown', (e) => { if (e.key === 'Escape') … })
recompensa: xp 10, oro 10
```

#### Escena
Teo abre el menú y quiere cerrarlo rápido, como cierra todo: con la tecla de escape. No pasa nada.

#### Gheco sugiere
Escuchá `keydown` en el `document`. Si la tecla es `Escape`, sacá la clase `abierto` y poné `aria-expanded` en `false`.

#### Desafío
Abrir con el botón y cerrar con Escape.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #f6efe3; }
  header { padding: 12px 16px; background: #2b1d0e; }
  #menu-boton { font-size: 22px; background: none; color: #f6efe3; border: 0; }
  #menu { display: none; background: #3b2a16; padding: 8px 16px; }
  #menu.abierto { display: block; }
  #menu a { color: #ffd400; margin-right: 12px; }
</style>
<header><button id="menu-boton" aria-expanded="false">☰</button></header>
<nav id="menu"><a href="#">Vitrales</a><a href="#">Pedidos</a></nav>
```

#### Eventos
```
click #menu-boton
tecla Escape
```

#### Estado
```
#menu @class
#menu-boton @aria-expanded
```

#### Código inicial
```javascript
const boton = document.querySelector('#menu-boton');
const menu = document.querySelector('#menu');
boton.addEventListener('click', () => {
  const abierto = menu.classList.toggle('abierto');
  boton.setAttribute('aria-expanded', String(abierto));
});

```

#### Salida esperada
```
── Estado ──
#menu @class: (vacío)
#menu-boton @aria-expanded: false
```

#### Solución
```javascript
const boton = document.querySelector('#menu-boton');
const menu = document.querySelector('#menu');
boton.addEventListener('click', () => {
  const abierto = menu.classList.toggle('abierto');
  boton.setAttribute('aria-expanded', String(abierto));
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    menu.classList.remove('abierto');
    boton.setAttribute('aria-expanded', 'false');
  }
});
```

#### Al superarla
*Escape* y el menú se va. Teo lo prueba con los ojos cerrados: ya no necesita buscar el botón.

#### Imagen
- Primer plano de un teclado de madera tallada con la tecla de escape iluminada en amarillo.
- Al fondo, el menú de vidrio que sube y se esconde.

### Micro-misión S01-N01-P4 · Tocar afuera

```meta
lugar: El escaparate de los Talleres
personajes: Nima, Gheco, Teo, Tesela (por carta)
carta: closest | if (!e.target.closest('#menu, #menu-boton')) cerrar()
recompensa: xp 15, monedas 5
```

#### Escena
Llega una carta de **Tesela**, con letra prolija: *«Un menú abierto no puede tapar la página. Si alguien toca afuera, se cierra solo.»* Teo la lee dos veces, corriendo en el lugar.

#### Gheco sugiere
Escuchá `click` en el `document`. Si el elemento tocado no está adentro del menú ni del botón (`closest` da `null`), cerrá el menú.

#### Desafío
Abrí el menú, tocá un enlace del menú (sigue abierto) y después tocá el `main` (se cierra). En `#veces` contá cuántas veces se cerró solo.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #f6efe3; }
  header { padding: 12px 16px; background: #2b1d0e; }
  #menu-boton { font-size: 22px; background: none; color: #f6efe3; border: 0; }
  #menu { display: none; background: #3b2a16; padding: 8px 16px; }
  #menu.abierto { display: block; }
  #menu a { color: #ffd400; margin-right: 12px; }
  main { padding: 16px; min-height: 120px; }
</style>
<header><button id="menu-boton" aria-expanded="false">☰</button></header>
<nav id="menu"><a href="#vitrales">Vitrales</a><a href="#pedidos">Pedidos</a></nav>
<main><p>Los vitrales de esta semana.</p><p>Se cerró solo <span id="veces">0</span> veces.</p></main>
```

#### Eventos
```
click #menu-boton
click #menu a
click main
```

#### Estado
```
#menu @class
#menu-boton @aria-expanded
#veces
```

#### Código inicial
```javascript
const boton = document.querySelector('#menu-boton');
const menu = document.querySelector('#menu');
const veces = document.querySelector('#veces');
let cerradas = 0;

boton.addEventListener('click', () => {
  const abierto = menu.classList.toggle('abierto');
  boton.setAttribute('aria-expanded', String(abierto));
});

document.addEventListener('click', () => {
  menu.classList.remove('abierto');
});
```

#### Salida esperada
```
── Estado ──
#menu @class: (vacío)
#menu-boton @aria-expanded: false
#veces: 1
```

#### Solución
```javascript
const boton = document.querySelector('#menu-boton');
const menu = document.querySelector('#menu');
const veces = document.querySelector('#veces');
let cerradas = 0;

boton.addEventListener('click', () => {
  const abierto = menu.classList.toggle('abierto');
  boton.setAttribute('aria-expanded', String(abierto));
});

document.addEventListener('click', (e) => {
  if (e.target.closest('#menu, #menu-boton')) return;
  if (!menu.classList.contains('abierto')) return;
  menu.classList.remove('abierto');
  boton.setAttribute('aria-expanded', 'false');
  cerradas++;
  veces.textContent = cerradas;
});
```

#### Al superarla
El menú se cierra cuando corresponde, y no cuando se lo toca. Teo dobla la carta de Tesela y se la guarda en el delantal: —Siempre tiene razón. Es insoportable.

#### Imagen
- Una carta de papel grueso con un sello de plomo de colores (el de los Talleres), abierta sobre el mostrador del escaparate, sin texto legible.
- Teo corre en el lugar mientras lee; Nima se ríe.

### Micro-misión S01-N01-P5 · Las pestañas del catálogo

```meta
lugar: El escaparate de los Talleres
personajes: Nima, Gheco, Teo
carta: hidden | panel.hidden = panel.id !== elegido · boton.dataset.panel
recompensa: xp 15, monedas 5
```

#### Escena
El catálogo de los Talleres tiene tres secciones apiladas, una debajo de otra, y nadie llega hasta la última. —Tesela quiere **pestañas** —dice Teo—: tres botones arriba y se ve una sola sección por vez.

#### Gheco sugiere
Cada botón tiene `data-panel` con el `id` de su sección. Al tocar uno, recorré los paneles y escondé (`hidden = true`) todos menos el elegido. Marcá el botón activo con `aria-selected="true"` y los otros con `"false"`.

#### Desafío
Tocar la pestaña «Precios» muestra solo esa sección.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #f6efe3; color: #2b1d0e; padding: 16px; }
  [role=tablist] { display: flex; gap: 4px; }
  [role=tab] { padding: 8px 14px; border: 2px solid #2b1d0e; background: #fff8ec; border-radius: 8px 8px 0 0; }
  [role=tab][aria-selected=true] { background: #2b1d0e; color: #ffd400; }
  section { border: 2px solid #2b1d0e; padding: 12px; background: #fff; }
</style>
<div role="tablist">
  <button role="tab" data-panel="vitrales" aria-selected="true">Vitrales</button>
  <button role="tab" data-panel="precios" aria-selected="false">Precios</button>
  <button role="tab" data-panel="taller" aria-selected="false">El taller</button>
</div>
<section id="vitrales">Rosetones, ventanas y lámparas.</section>
<section id="precios" hidden>Un rosetón: 12 sellos.</section>
<section id="taller" hidden>Abierto de noche, como la Feria.</section>
```

#### Eventos
```
click [data-panel=precios]
```

#### Estado
```
section @hidden
[role=tab] @aria-selected
```

#### Código inicial
```javascript
const pestanias = document.querySelectorAll('[role=tab]');
const paneles = document.querySelectorAll('section');

```

#### Salida esperada
```
── Estado ──
section @hidden: sí
section @hidden: no
section @hidden: sí
[role=tab] @aria-selected: false
[role=tab] @aria-selected: true
[role=tab] @aria-selected: false
```

#### Solución
```javascript
const pestanias = document.querySelectorAll('[role=tab]');
const paneles = document.querySelectorAll('section');

for (const pestania of pestanias) {
  pestania.addEventListener('click', () => {
    const elegido = pestania.dataset.panel;
    for (const panel of paneles) panel.hidden = panel.id !== elegido;
    for (const otra of pestanias) otra.setAttribute('aria-selected', String(otra === pestania));
  });
}
```

#### Al superarla
Tres pestañas, una sección por vez. Teo se pone a mirar los precios por primera vez. —¿Doce sellos? Tesela me paga en pan.

#### Imagen
- Un catálogo de vidrio con tres pestañas de colores arriba, como carpetas, y una sola página visible.
- Teo, sorprendido, lee la pestaña del medio.

## S01-N02 · La galería de vitrales

```meta
tipo: tema
padre: S01-N01
precio: 10
criatura: ogre
temas: js.dom, js.eventos
usa: html.multimedia
```

### Crónica

La segunda página del escaparate es la **galería**: cinco vitrales de Tesela en miniatura, en fila, y un marco grande vacío. —Cuando alguien toca uno —explica Teo—, tiene que verse grande en el marco. Y con flechas para pasar al siguiente, como en una feria de verdad. —Mira a Nima de reojo—. Tesela dice que la última vez que alguien lo intentó, el último vitral **no tenía siguiente** y la página se rompió.

### Objetivos

- Cambiar la imagen grande desde las miniaturas, con `src`, `alt` y `data-*`.
- Pasar al siguiente y al anterior **dando la vuelta** con el resto (`%`).
- Marcar la miniatura activa y mostrar el contador «2 / 5».
- Manejar la galería con el teclado y con un pase automático que se pausa.

### Antes de empezar

- S01-N01 (el menú que se abre) y la delegación de R02-N05.

### Explicación

#### Una galería es un índice
Toda la galería depende de **un solo número**: cuál se está mirando.
```javascript
const vitrales = ['rosa.png', 'sol.png', 'luna.png', 'faro.png', 'gema.png'];
let actual = 0;

function mostrar(n) {
  actual = n;
  grande.src = vitrales[actual];
  contador.textContent = `${actual + 1} / ${vitrales.length}`;
}
```
Las flechas solo cambian `actual` y llaman a `mostrar`.

#### Dar la vuelta con `%`
Al pasar del último (4) al siguiente, hay que volver al 0; al ir hacia atrás desde el 0, al último:
```javascript
const siguiente = (actual + 1) % vitrales.length;                  // 4 → 0
const anterior = (actual - 1 + vitrales.length) % vitrales.length; // 0 → 4
```
El `+ vitrales.length` evita el resto negativo: en JavaScript, `-1 % 5` da `-1`, no `4`.

#### Marcar la activa
```javascript
miniaturas.forEach((mini, i) => mini.classList.toggle('activa', i === actual));
```
`toggle(clase, condición)` la pone si la condición es verdadera y la saca si es falsa.

#### El pase automático
```javascript
let pase = setInterval(() => mostrar((actual + 1) % vitrales.length), 3000);
galeria.addEventListener('mouseenter', () => clearInterval(pase));
```
En la caja el reloj es de mentira: tres segundos pasan con `esperar 3000`.

### Código de ejemplo

```javascript
const vitrales = ['Rosa', 'Sol', 'Luna', 'Faro', 'Gema'];
let actual = 0;

const siguiente = () => (actual + 1) % vitrales.length;
const anterior = () => (actual - 1 + vitrales.length) % vitrales.length;

actual = 4;
console.log('Del último, siguiente:', vitrales[siguiente()]);
actual = 0;
console.log('Del primero, anterior:', vitrales[anterior()]);
console.log('Sin el arreglo de la vuelta:', -1 % vitrales.length);
console.log(`Contador: ${actual + 1} / ${vitrales.length}`);
```

### Salida esperada

```
Del último, siguiente: Rosa
Del primero, anterior: Gema
Sin el arreglo de la vuelta: -1
Contador: 1 / 5
```

### ¿Para qué sirve?

Galerías, carruseles de fotos, catálogos de tiendas, pasos de un formulario largo, diapositivas: todos son «un índice y una función que muestra». La cuenta del resto aparece en relojes, calendarios y juegos que dan la vuelta a la pantalla.

### Errores habituales

**Ogro: el siguiente del último.** `actual + 1` sin el resto llega a 5, y `vitrales[5]` es `undefined`: la imagen se rompe. Es el error de «uno de más».

**Ogro: el resto negativo.** `(0 - 1) % 5` da `-1`. Sumá el largo antes del resto.

**Orco: el `alt` olvidado.** Cambiar el `src` y no el `alt` deja una descripción vieja: quien usa un lector de pantalla escucha «Rosa» mirando la luna.

**Troll: dos intervalos.** Si el pase arranca cada vez que el mouse sale y nunca se cancela el anterior, se juntan dos, tres, cuatro intervalos y la galería pasa cada vez más rápido. Antes de crear uno nuevo, cancelá el viejo.

### Micro-misión S01-N02-P1 · El marco grande

```meta
lugar: La galería del escaparate
personajes: Nima, Gheco, Teo
carta: data-* y src | grande.src = mini.dataset.grande · grande.alt = mini.alt
recompensa: xp 10, oro 10
```

#### Escena
Cinco miniaturas en fila y el marco grande vacío. Teo toca la del sol y no pasa nada.

#### Gheco sugiere
Usá delegación en `#miniaturas`: con `closest('img')` encontrá la miniatura tocada y copiá su `data-grande` al `src` del `#grande`, y su `alt` al `alt`.

#### Desafío
Tocar la tercera miniatura (la luna) la muestra grande.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #1b1209; color: #f6efe3; padding: 16px; text-align: center; }
  #grande { width: 220px; height: 140px; background: #3b2a16; border: 6px solid #8d6e3f; object-fit: cover; }
  #miniaturas { display: flex; gap: 6px; justify-content: center; margin-top: 10px; }
  #miniaturas img { width: 48px; height: 48px; border: 3px solid transparent; cursor: pointer; background: #8d6e3f; }
</style>
<img id="grande" src="" alt="">
<div id="miniaturas">
  <img src="mini-rosa.png" data-grande="rosa.png" alt="Rosetón rosa">
  <img src="mini-sol.png" data-grande="sol.png" alt="Vitral del sol">
  <img src="mini-luna.png" data-grande="luna.png" alt="Vitral de la luna">
  <img src="mini-faro.png" data-grande="faro.png" alt="Vitral del faro">
  <img src="mini-gema.png" data-grande="gema.png" alt="Vitral de la gema">
</div>
```

#### Eventos
```
click #miniaturas img:nth-child(3)
```

#### Estado
```
#grande @src
#grande @alt
```

#### Código inicial
```javascript
const grande = document.querySelector('#grande');
const miniaturas = document.querySelector('#miniaturas');

```

#### Salida esperada
```
── Estado ──
#grande @src: luna.png
#grande @alt: Vitral de la luna
```

#### Solución
```javascript
const grande = document.querySelector('#grande');
const miniaturas = document.querySelector('#miniaturas');
miniaturas.addEventListener('click', (e) => {
  const mini = e.target.closest('img');
  if (!mini) return;
  grande.src = mini.dataset.grande;
  grande.alt = mini.alt;
});
```

#### Al superarla
La luna llena el marco. Teo se queda quieto (por primera vez en el día) mirándola.

#### Imagen
- Una galería de madera con un marco grande de bronce que muestra un vitral de una luna, y cinco vitrales en miniatura en fila debajo.
- Teo quieto, con la boca abierta.

### Micro-misión S01-N02-P2 · El que no tenía siguiente

```meta
lugar: La galería del escaparate
personajes: Nima, Gheco, Teo
carta: Dar la vuelta | (actual - 1 + total) % total · (actual + 1) % total
recompensa: xp 10, oro 10
```

#### Escena
Las flechas ya están, pero hacen lo de la última vez: desde el primer vitral, la flecha de «anterior» rompe la página. —Te dije —dice Teo, y se tapa la cara.

#### Gheco sugiere
Las dos flechas tienen que **dar la vuelta**: desde el primero, «anterior» va al último. Arreglá las dos cuentas y mostrá el contador `n / 5`.

#### Desafío
Desde el primero, tocá «anterior» y después dos veces «siguiente»: tiene que quedar el segundo vitral (`2 / 5`).

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #1b1209; color: #f6efe3; padding: 16px; text-align: center; }
  #nombre { font-size: 22px; margin: 12px; }
  button { font-size: 20px; padding: 4px 14px; }
</style>
<p id="nombre">Rosetón rosa</p>
<button id="anterior">◀</button> <span id="contador">1 / 5</span> <button id="siguiente">▶</button>
```

#### Eventos
```
click #anterior
click #siguiente
click #siguiente
```

#### Estado
```
#nombre
#contador
```

#### Código inicial
```javascript
const vitrales = ['Rosetón rosa', 'Vitral del sol', 'Vitral de la luna', 'Vitral del faro', 'Vitral de la gema'];
let actual = 0;

function mostrar() {
  document.querySelector('#nombre').textContent = vitrales[actual];
  document.querySelector('#contador').textContent = `${actual} / ${vitrales.length}`;
}

document.querySelector('#anterior').addEventListener('click', () => {
  actual = actual - 1;
  mostrar();
});
document.querySelector('#siguiente').addEventListener('click', () => {
  actual = actual + 1;
  mostrar();
});
```

#### Salida esperada
```
── Estado ──
#nombre: Vitral del sol
#contador: 2 / 5
```

#### Solución
```javascript
const vitrales = ['Rosetón rosa', 'Vitral del sol', 'Vitral de la luna', 'Vitral del faro', 'Vitral de la gema'];
let actual = 0;

function mostrar() {
  document.querySelector('#nombre').textContent = vitrales[actual];
  document.querySelector('#contador').textContent = `${actual + 1} / ${vitrales.length}`;
}

document.querySelector('#anterior').addEventListener('click', () => {
  actual = (actual - 1 + vitrales.length) % vitrales.length;
  mostrar();
});
document.querySelector('#siguiente').addEventListener('click', () => {
  actual = (actual + 1) % vitrales.length;
  mostrar();
});
```

#### Al superarla
La galería da la vuelta como una calesita: después de la gema vuelve la rosa. Teo destapa la cara. —¿Ya está? ¿No se rompe más?

#### Imagen
- Una galería circular de vitrales que gira como una calesita, con flechas de luz a los costados.
- Teo espía entre los dedos.

### Micro-misión S01-N02-P3 · La miniatura encendida

```meta
lugar: La galería del escaparate
personajes: Nima, Gheco, Teo
carta: toggle con condición | minis.forEach((m, i) => m.classList.toggle('activa', i === actual))
recompensa: xp 10, oro 10
```

#### Escena
—Falta que se note **cuál** estás mirando —dice Teo—. Tesela le pone un marco dorado a la miniatura del vitral que está en el marco grande.

#### Gheco sugiere
En `mostrar`, recorré las miniaturas y poné la clase `activa` solo en la del índice `actual`, con `toggle(clase, condición)`. Que tocar una miniatura también la muestre (su índice sale de `data-n`).

#### Desafío
Tocá «siguiente» y después la quinta miniatura: queda activa solo la quinta.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #1b1209; color: #f6efe3; padding: 16px; text-align: center; }
  #miniaturas { display: flex; gap: 6px; justify-content: center; margin: 10px; }
  #miniaturas button { width: 48px; height: 48px; border: 3px solid transparent; background: #8d6e3f; color: #fff; }
  #miniaturas .activa { border-color: #ffd400; }
</style>
<p id="nombre">Rosetón rosa</p>
<div id="miniaturas">
  <button data-n="0" class="activa">1</button><button data-n="1">2</button><button data-n="2">3</button><button data-n="3">4</button><button data-n="4">5</button>
</div>
<button id="siguiente">▶</button>
```

#### Eventos
```
click #siguiente
click [data-n="4"]
```

#### Estado
```
.activa #
.activa
#nombre
```

#### Código inicial
```javascript
const vitrales = ['Rosetón rosa', 'Vitral del sol', 'Vitral de la luna', 'Vitral del faro', 'Vitral de la gema'];
const minis = document.querySelectorAll('#miniaturas button');
let actual = 0;

function mostrar(n) {
  actual = n;
  document.querySelector('#nombre').textContent = vitrales[actual];
  minis[actual].classList.add('activa');
}

document.querySelector('#siguiente').addEventListener('click', () => mostrar((actual + 1) % vitrales.length));
```

#### Salida esperada
```
── Estado ──
.activa #: 1
.activa: 5
#nombre: Vitral de la gema
```

#### Solución
```javascript
const vitrales = ['Rosetón rosa', 'Vitral del sol', 'Vitral de la luna', 'Vitral del faro', 'Vitral de la gema'];
const minis = document.querySelectorAll('#miniaturas button');
let actual = 0;

function mostrar(n) {
  actual = n;
  document.querySelector('#nombre').textContent = vitrales[actual];
  minis.forEach((mini, i) => mini.classList.toggle('activa', i === actual));
}

document.querySelector('#siguiente').addEventListener('click', () => mostrar((actual + 1) % vitrales.length));
document.querySelector('#miniaturas').addEventListener('click', (e) => {
  const mini = e.target.closest('[data-n]');
  if (mini) mostrar(Number(mini.dataset.n));
});
```

#### Al superarla
Un solo marco dorado, siempre en la miniatura correcta. Antes, con el código de Teo, terminaban todas doradas.

#### Imagen
- Una fila de cinco vitrales en miniatura; solo el último tiene un marco dorado que brilla.
- Teo, avergonzado, sostiene un tarro de pintura dorada.

### Micro-misión S01-N02-P4 · Las flechas del teclado

```meta
lugar: La galería del escaparate
personajes: Nima, Gheco, Teo
carta: Flechas | if (e.key === 'ArrowRight') … else if (e.key === 'ArrowLeft') …
recompensa: xp 15, monedas 5
```

#### Escena
Un visitante de la Feria no puede usar el mouse: maneja todo con el teclado. Se queda frente a la galería sin poder pasar los vitrales.

#### Gheco sugiere
Escuchá `keydown` en el `document`: `ArrowRight` pasa al siguiente y `ArrowLeft` al anterior, dando la vuelta. Las demás teclas no hacen nada.

#### Desafío
Con `←`, `←`, `→`, `a` y `←`, tiene que quedar el cuarto vitral (`4 / 5`).

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #1b1209; color: #f6efe3; padding: 16px; text-align: center; }
  #nombre { font-size: 22px; }
</style>
<p id="nombre">Rosetón rosa</p>
<p id="contador">1 / 5</p>
<p><small>Usá las flechas ← y →</small></p>
```

#### Eventos
```
tecla ArrowLeft
tecla ArrowLeft
tecla ArrowRight
tecla a
tecla ArrowLeft
```

#### Estado
```
#nombre
#contador
```

#### Código inicial
```javascript
const vitrales = ['Rosetón rosa', 'Vitral del sol', 'Vitral de la luna', 'Vitral del faro', 'Vitral de la gema'];
let actual = 0;

function mostrar(n) {
  actual = (n + vitrales.length) % vitrales.length;
  document.querySelector('#nombre').textContent = vitrales[actual];
  document.querySelector('#contador').textContent = `${actual + 1} / ${vitrales.length}`;
}

```

#### Salida esperada
```
── Estado ──
#nombre: Vitral del faro
#contador: 4 / 5
```

#### Solución
```javascript
const vitrales = ['Rosetón rosa', 'Vitral del sol', 'Vitral de la luna', 'Vitral del faro', 'Vitral de la gema'];
let actual = 0;

function mostrar(n) {
  actual = (n + vitrales.length) % vitrales.length;
  document.querySelector('#nombre').textContent = vitrales[actual];
  document.querySelector('#contador').textContent = `${actual + 1} / ${vitrales.length}`;
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight') mostrar(actual + 1);
  else if (e.key === 'ArrowLeft') mostrar(actual - 1);
});
```

#### Al superarla
El visitante pasa los vitrales con las flechas, uno por uno, sin apuro. Al irse le deja a Teo una ficha de propina.

#### Imagen
- Un visitante mayor con bastón, frente a la galería, apoyando la mano sobre dos teclas de flecha de madera.
- Los vitrales pasan dentro del marco; Teo lo mira contento.

### Micro-misión S01-N02-P5 · El pase que espera

```meta
lugar: La galería del escaparate
personajes: Nima, Gheco, Teo
carta: Pausar | pase = setInterval(…, 3000) · mouseenter → clearInterval(pase) · mouseleave → arrancar()
recompensa: xp 15, monedas 5
```

#### Escena
Tesela quiere que la galería pase sola cada tres segundos, como el carrusel de la Feria. Pero que **se quede quieta** mientras alguien la mira con el mouse encima.

#### Gheco sugiere
Hacé una función `arrancar` que cancele el intervalo anterior y cree uno nuevo de 3000 ms. Llamala al empezar y en `mouseleave`; en `mouseenter`, cancelalo.

#### Desafío
Pasan 7 segundos (va por el tercero), el mouse entra y se queda 10 segundos (no cambia), sale y pasan 3 segundos más: queda el cuarto. Al final tiene que haber **un solo** temporizador esperando.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #1b1209; color: #f6efe3; padding: 16px; text-align: center; }
  #galeria { border: 6px solid #8d6e3f; padding: 24px; font-size: 22px; }
</style>
<div id="galeria"><span id="nombre">Rosetón rosa</span></div>
```

#### Eventos
```
esperar 7000
pasar #galeria
esperar 10000
salir #galeria
esperar 3000
```

#### Estado
```
#nombre
temporizadores
```

#### Código inicial
```javascript
const vitrales = ['Rosetón rosa', 'Vitral del sol', 'Vitral de la luna', 'Vitral del faro', 'Vitral de la gema'];
const galeria = document.querySelector('#galeria');
let actual = 0;
let pase = null;

function siguiente() {
  actual = (actual + 1) % vitrales.length;
  document.querySelector('#nombre').textContent = vitrales[actual];
}

function arrancar() {
  pase = setInterval(siguiente, 3000);
}

arrancar();
galeria.addEventListener('mouseleave', arrancar);
```

#### Salida esperada
```
── Estado ──
#nombre: Vitral del faro
temporizadores: 1
```

#### Solución
```javascript
const vitrales = ['Rosetón rosa', 'Vitral del sol', 'Vitral de la luna', 'Vitral del faro', 'Vitral de la gema'];
const galeria = document.querySelector('#galeria');
let actual = 0;
let pase = null;

function siguiente() {
  actual = (actual + 1) % vitrales.length;
  document.querySelector('#nombre').textContent = vitrales[actual];
}

function arrancar() {
  clearInterval(pase);
  pase = setInterval(siguiente, 3000);
}

arrancar();
galeria.addEventListener('mouseenter', () => clearInterval(pase));
galeria.addEventListener('mouseleave', arrancar);
```

#### Al superarla
La galería pasa sola y se queda quieta cuando alguien la mira. Teo, para probar, se queda con la mano encima diez minutos. —Sí. Espera. Como la Reina.

#### Imagen
- La galería de vitrales de noche, con un vitral grande quieto en el marco y una mano apoyada encima.
- Lumina, la luciérnaga gigante con alas de vidrio, mira desde un farol con su farolito encendido.

## S01-N03 · Los temas del escaparate

```meta
tipo: tema
padre: S01-N02
precio: 10
criatura: goblin
temas: css.temas, js.almacenamiento
usa: js.dom, js.eventos
```

### Crónica

De día, las páginas de los Talleres son de color crema y madera. Pero en la Feria es **siempre de noche**, y el escaparate encandila a todos los que pasan. Doña Mirta se tapa los ojos con el delantal. —¡Apaguen eso, que me quedo ciega!

—Tesela hace todas las páginas con **dos caras** —dice Teo—: una clara y una oscura. Solo hay que saber cuál mostrar. Y que la página **se acuerde** de la que eligió cada uno.

### Objetivos

- Cambiar el tema de la página con una clase en el `<body>`.
- Guardar el tema elegido en `localStorage` y aplicarlo al cargar.
- Cambiar variables de CSS desde JavaScript con `style.setProperty('--acento', color)`.
- Agrandar y achicar la letra con límites, y elegir entre varios temas con `data-tema`.

### Antes de empezar

- S01-N02 y JSON y `localStorage` (R02-N06).

### Explicación

#### Dos caras con una clase
El CSS tiene las dos versiones; JavaScript elige:
```css
body { background: #f6efe3; color: #2b1d0e; }
body.oscuro { background: #0b1020; color: #f6efe3; }
```
```javascript
const oscuro = document.body.classList.toggle('oscuro');
```

#### Que se acuerde
```javascript
localStorage.setItem('tema', oscuro ? 'oscuro' : 'claro');
// al cargar la página:
if (localStorage.getItem('tema') === 'oscuro') document.body.classList.add('oscuro');
```

#### Variables de CSS
Los Talleres pintan todo con **variables**: `var(--acento)`. Cambiando una sola variable cambia el color de toda la página:
```javascript
document.documentElement.style.setProperty('--acento', '#e53935');
getComputedStyle(document.documentElement).getPropertyValue('--acento'); // '#e53935'
```
`document.documentElement` es la etiqueta `<html>`: la variable vale para toda la página.

#### Varios temas
Con más de dos, en vez de clases conviene un atributo: `document.documentElement.dataset.tema = 'vitral'`, y en el CSS `[data-tema=vitral] { … }`.

### Código de ejemplo

```javascript
document.body.innerHTML = '<p>Hola</p>';

localStorage.setItem('tema', 'oscuro');
const guardado = localStorage.getItem('tema');
if (guardado === 'oscuro') document.body.classList.add('oscuro');
console.log('Clases del body:', document.body.className);

document.documentElement.style.setProperty('--acento', '#e53935');
console.log('Acento:', getComputedStyle(document.documentElement).getPropertyValue('--acento'));

let tamanio = Number(localStorage.getItem('letra') ?? 16);
tamanio = Math.min(24, tamanio + 10);
console.log('Letra (con tope):', tamanio);
```

### Salida esperada

```
Clases del body: oscuro
Acento: #e53935
Letra (con tope): 24
```

### ¿Para qué sirve?

El modo oscuro, el tamaño de letra para quien ve poco, los colores de una marca, la página que «se acuerda» de tus preferencias: todo es una clase o una variable de CSS, y un `localStorage` para no olvidarlo.

### Errores habituales

**Goblin: el número que es texto.** `localStorage` devuelve texto: `'16' + 2` da `'162'`. Convertí con `Number` antes de sumar.

**Ogro: el parpadeo.** Si el tema se aplica después de un rato (dentro de un `setTimeout`, o al final de un script largo), la página se ve un instante clara y después oscura. Aplicalo lo antes posible.

**Esqueleto: la variable sin los dos guiones.** `setProperty('acento', …)` no hace nada: las variables de CSS empiezan con `--`.

### Micro-misión S01-N03-P1 · La noche de Doña Mirta

```meta
lugar: El escaparate, de noche
personajes: Nima, Gheco, Teo, Doña Mirta
carta: Tema oscuro | const oscuro = document.body.classList.toggle('oscuro')
recompensa: xp 10, oro 10
```

#### Escena
Doña Mirta sigue con el delantal en la cara. Teo agrega un botón con una luna.

#### Gheco sugiere
Al tocar `#tema`, alterná la clase `oscuro` del `body` y cambiá el texto del botón: `☀ Claro` si quedó oscuro (para volver), `🌙 Oscuro` si quedó claro.

#### Desafío
Un click: la página queda oscura y el botón dice `☀ Claro`.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #f6efe3; color: #2b1d0e; padding: 16px; transition: background .3s; }
  body.oscuro { background: #0b1020; color: #f6efe3; }
  #tema { padding: 6px 12px; }
</style>
<button id="tema">🌙 Oscuro</button>
<h1>Talleres de los Vitrales</h1>
<p>Rosetones, ventanas y lámparas.</p>
```

#### Eventos
```
click #tema
```

#### Estado
```
body @class
#tema
```

#### Código inicial
```javascript
const boton = document.querySelector('#tema');

```

#### Salida esperada
```
── Estado ──
body @class: oscuro
#tema: ☀ Claro
```

#### Solución
```javascript
const boton = document.querySelector('#tema');
boton.addEventListener('click', () => {
  const oscuro = document.body.classList.toggle('oscuro');
  boton.textContent = oscuro ? '☀ Claro' : '🌙 Oscuro';
});
```

#### Al superarla
El escaparate se apaga suave, como un farol que baja la mecha. Doña Mirta se saca el delantal de la cara. —Ahora sí. Tomá, un pan con miel.

#### Imagen
- El escaparate de vitrales en modo oscuro, de noche, con colores profundos y un brillo suave.
- Doña Mirta (petisa y redonda, delantal floreado cerrado, pañuelo en la cabeza) le da un pan con miel a Teo.

### Micro-misión S01-N03-P2 · La página que se acuerda

```meta
lugar: El escaparate, de noche
personajes: Nima, Gheco, Doña Mirta
carta: Recordar | localStorage.setItem('tema', …) · al cargar: if (localStorage.getItem('tema') === 'oscuro') …
recompensa: xp 10, oro 10
```

#### Escena
A la noche siguiente, Doña Mirta vuelve a pasar… y el escaparate está claro otra vez. —¡Otra vez! ¿No se acuerda de nada esta página?

#### Gheco sugiere
Al cargar, si `localStorage` tiene `tema` en `oscuro`, poné la clase y el texto del botón. Al tocar el botón, guardá el tema nuevo.

#### Desafío
Doña Mirta ya lo había elegido oscuro: la página arranca oscura. Ella toca el botón dos veces (claro y otra vez oscuro), y queda guardado `oscuro`.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #f6efe3; color: #2b1d0e; padding: 16px; }
  body.oscuro { background: #0b1020; color: #f6efe3; }
</style>
<button id="tema">🌙 Oscuro</button>
<h1>Talleres de los Vitrales</h1>
```

#### Almacenamiento
```
local tema = oscuro
```

#### Eventos
```
click #tema
click #tema
```

#### Estado
```
body @class
#tema
local tema
```

#### Código inicial
```javascript
const boton = document.querySelector('#tema');

function poner(oscuro) {
  document.body.classList.toggle('oscuro', oscuro);
  boton.textContent = oscuro ? '☀ Claro' : '🌙 Oscuro';
}

boton.addEventListener('click', () => {
  poner(!document.body.classList.contains('oscuro'));
});
```

#### Salida esperada
```
── Estado ──
body @class: oscuro
#tema: ☀ Claro
local tema: oscuro
```

#### Solución
```javascript
const boton = document.querySelector('#tema');

function poner(oscuro) {
  document.body.classList.toggle('oscuro', oscuro);
  boton.textContent = oscuro ? '☀ Claro' : '🌙 Oscuro';
  localStorage.setItem('tema', oscuro ? 'oscuro' : 'claro');
}

poner(localStorage.getItem('tema') === 'oscuro');
boton.addEventListener('click', () => {
  poner(!document.body.classList.contains('oscuro'));
});
```

#### Al superarla
Doña Mirta pasa y el escaparate ya está oscuro, esperándola. —Así me gusta. Que se acuerden de una.

#### Imagen
- Doña Mirta pasa frente al escaparate oscuro con una canasta de panes, tranquila.
- Un cajoncito de madera con un papel guardado (el cajón del navegador), brillando suave, sin texto legible.

### Micro-misión S01-N03-P3 · El color de Tesela

```meta
lugar: El escaparate
personajes: Nima, Gheco, Teo
carta: Variables de CSS | document.documentElement.style.setProperty('--acento', color)
recompensa: xp 10, oro 10
```

#### Escena
Todas las páginas de Tesela usan **un** color de acento: los bordes, los títulos y los botones. —Si cambia esa variable, cambia todo —dice Teo—. Ella la elige con un frasquito de pintura.

#### Gheco sugiere
El `<input type="color">` avisa con `input`. Copiá su `value` a la variable `--acento` del `<html>`, y mostrá el color en `#codigo`.

#### Desafío
Elegir el rojo `#e53935` pinta toda la página.

#### Página
```html
<style>
  :root { --acento: #8d6e3f; }
  body { margin: 0; font-family: system-ui, sans-serif; background: #f6efe3; color: #2b1d0e; padding: 16px; }
  h1 { color: var(--acento); border-bottom: 4px solid var(--acento); }
  button { background: var(--acento); color: white; border: 0; padding: 8px 14px; }
</style>
<label>Color de acento <input id="color" type="color" value="#8d6e3f"></label> <code id="codigo">#8d6e3f</code>
<h1>Talleres de los Vitrales</h1>
<button>Pedir un vitral</button>
```

#### Eventos
```
elegir #color #e53935
```

#### Estado
```
estilo html { --acento }
#codigo
```

#### Código inicial
```javascript
const color = document.querySelector('#color');
const codigo = document.querySelector('#codigo');

```

#### Salida esperada
```
── Estado ──
estilo html { --acento }: #e53935
#codigo: #e53935
```

#### Solución
```javascript
const color = document.querySelector('#color');
const codigo = document.querySelector('#codigo');
color.addEventListener('input', () => {
  document.documentElement.style.setProperty('--acento', color.value);
  codigo.textContent = color.value;
});
```

#### Al superarla
Toda la página se vuelve roja de golpe: títulos, bordes y botones. Teo aplaude. —¡Como cuando se le cae el frasco a Tesela!

#### Imagen
- Una página de los Talleres pintada de rojo, con un frasquito de pintura roja derramado al costado.
- Teo aplaude saltando.

### Micro-misión S01-N03-P4 · La letra de Lucio

```meta
lugar: El escaparate
personajes: Nima, Gheco, Lucio
carta: Con límites | tamanio = Math.min(24, tamanio + 2) · Math.max(12, tamanio - 2)
recompensa: xp 15, monedas 5
```

#### Escena
Lucio, el farolero, se acerca al escaparate y entrecierra los ojos. —Lindo… pero no leo nada. Ya no tengo la vista de antes.

#### Gheco sugiere
Dos botones: `A+` suma 2 a la letra y `A−` resta 2, entre 12 y 24 como mucho. Ponela en `document.body.style.fontSize`, mostrala en `#tamanio` y guardala en `local letra`. Al cargar, leela (si no hay, 16).

#### Desafío
Lucio ya la había puesto en 20. Toca `A+` cuatro veces y `A−` una: queda en 22.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #0b1020; color: #f6efe3; padding: 16px; }
</style>
<button id="menos">A−</button> <span id="tamanio">16</span> px <button id="mas">A+</button>
<p>Los faroles de la Avenida se prenden de cerca hacia lo lejos.</p>
```

#### Almacenamiento
```
local letra = 20
```

#### Eventos
```
click #mas
click #mas
click #mas
click #mas
click #menos
```

#### Estado
```
#tamanio
estilo body { font-size }
local letra
```

#### Código inicial
```javascript
let tamanio = localStorage.getItem('letra') ?? 16;

function poner(nuevo) {
  tamanio = nuevo;
  document.body.style.fontSize = `${tamanio}px`;
  document.querySelector('#tamanio').textContent = tamanio;
  localStorage.setItem('letra', tamanio);
}

poner(tamanio);
document.querySelector('#mas').addEventListener('click', () => poner(tamanio + 2));
document.querySelector('#menos').addEventListener('click', () => poner(tamanio - 2));
```

#### Salida esperada
```
── Estado ──
#tamanio: 22
estilo body { font-size }: 22px
local letra: 22
```

#### Solución
```javascript
let tamanio = Number(localStorage.getItem('letra') ?? 16);

function poner(nuevo) {
  tamanio = Math.max(12, Math.min(24, nuevo));
  document.body.style.fontSize = `${tamanio}px`;
  document.querySelector('#tamanio').textContent = tamanio;
  localStorage.setItem('letra', tamanio);
}

poner(tamanio);
document.querySelector('#mas').addEventListener('click', () => poner(tamanio + 2));
document.querySelector('#menos').addEventListener('click', () => poner(tamanio - 2));
```

#### Al superarla
Con el código de antes, la letra de Lucio se iba a 202: el Goblin había pegado el 2 al 20. Ahora llega a 24, no pasa de ahí, y Lucio lee el cartel entero en voz alta.

#### Imagen
- Lucio (farolero viejo y flaco, gorra de lana, abrigo largo abotonado) lee de cerca un cartel con letras grandes, sonriendo.
- Un goblin chiquito de galera se escapa con un número 2 de madera bajo el brazo.

### Micro-misión S01-N03-P5 · Los tres vidrios

```meta
lugar: El escaparate
personajes: Nima, Gheco, Teo, Lumina
carta: data-tema | document.documentElement.dataset.tema = valor · [data-tema=vitral] { … }
recompensa: xp 15, monedas 5
```

#### Escena
—Tesela mandó un tercer tema —dice Teo—: **vitral**, todo con los colores del rosetón. Ya no alcanza con claro u oscuro. —{mentor} se posa arriba del escaparate a ver.

#### Gheco sugiere
Al cambiar el `<select id="elegir">`, poné su valor en `document.documentElement.dataset.tema` y guardalo en `local tema`. Al cargar, aplicá el guardado; si no hay ninguno o es uno que no existe, usá `claro`.

#### Desafío
Alguien había guardado `fucsia` (que no existe): arranca en `claro`. Después elige `vitral`.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; padding: 16px; }
  [data-tema=claro] body { background: #f6efe3; color: #2b1d0e; }
  [data-tema=oscuro] body { background: #0b1020; color: #f6efe3; }
  [data-tema=vitral] body { background: linear-gradient(135deg, #7b1fa2, #1565c0, #00897b); color: #fff; }
</style>
<label>Tema
  <select id="elegir">
    <option value="claro">Claro</option>
    <option value="oscuro">Oscuro</option>
    <option value="vitral">Vitral</option>
  </select>
</label>
<h1>Talleres de los Vitrales</h1>
```

#### Almacenamiento
```
local tema = fucsia
```

#### Eventos
```
elegir #elegir vitral
```

#### Estado
```
html @data-tema
#elegir @value
local tema
```

#### Código inicial
```javascript
const TEMAS = ['claro', 'oscuro', 'vitral'];
const elegir = document.querySelector('#elegir');

function poner(tema) {
  document.documentElement.dataset.tema = tema;
  elegir.value = tema;
}

poner(localStorage.getItem('tema'));
```

#### Salida esperada
```
── Estado ──
html @data-tema: vitral
#elegir @value: vitral
local tema: vitral
```

#### Solución
```javascript
const TEMAS = ['claro', 'oscuro', 'vitral'];
const elegir = document.querySelector('#elegir');

function poner(tema) {
  const valido = TEMAS.includes(tema) ? tema : 'claro';
  document.documentElement.dataset.tema = valido;
  elegir.value = valido;
  localStorage.setItem('tema', valido);
}

poner(localStorage.getItem('tema'));
elegir.addEventListener('change', () => poner(elegir.value));
```

#### Al superarla
El escaparate se llena de los colores del rosetón. {mentor} baja la luz de su farolito, como si no quisiera competir.

#### Imagen
- El escaparate con los colores de un rosetón (violeta, azul y verde) iluminando la Avenida de noche.
- Lumina, la luciérnaga gigante con alas de vidrio, posada arriba, con su luz amarilla bajita.

## S01-N04 · Jefe: la Polilla de los Formularios

```meta
tipo: jefe
padre: S01-N03
precio: 10
criatura: dragon
insignia: Vidriera Viva
insignia_descripcion: Le diste vida al Escaparate de los Talleres: menú, galería, temas y un formulario que avisa.
temas: js.formularios, err.validacion
usa: js.dom, js.eventos, html.formularios
```

### Crónica

La última página del escaparate es la más importante: el **formulario de pedidos** de los Talleres. Por ahí la gente encarga sus vitrales. Pero cada vez que alguien lo manda, llega a los Talleres **vacío**, o con un correo sin arroba, o con un mensaje de tres mil palabras.

Teo abre la caja de los pedidos y sale volando una **polilla** enorme, gris y peluda, atraída por la luz del escaparate. Tiene las alas llenas de letras que se comió. —¡La **Polilla de los Formularios**! —grita Teo—. Se come todo lo que se manda mal. Tesela dice que la única forma de echarla es que el formulario **avise antes**: que no deje mandar nada que esté mal.

### Objetivos

- Contar caracteres mientras se escribe, con el evento `input`.
- Mostrar el error de cada campo **en vivo**, al lado del campo, y marcarlo con `aria-invalid`.
- Deshabilitar el botón de enviar hasta que todo esté bien.
- Enviar sin recargar (`preventDefault`), agradecer y limpiar el formulario con `reset`.

### Antes de empezar

- Todo el Escaparate (S01-N01 a N03) y Teclado y formularios (R02-N04).

### Explicación

#### Cada campo, su regla
La validación se arma con funciones chiquitas: cada una recibe el valor y devuelve **el error** (un texto) o `''` si está bien.
```javascript
function errorNombre(valor) {
  if (valor.trim() === '') return 'Falta el nombre.';
  return '';
}
function errorCorreo(valor) {
  if (!valor.includes('@')) return 'El correo necesita una @.';
  return '';
}
```

#### En vivo
```javascript
campo.addEventListener('input', () => {
  const error = errorCorreo(campo.value);
  mensaje.textContent = error;
  campo.setAttribute('aria-invalid', String(error !== ''));
});
```
`aria-invalid` le avisa al lector de pantalla que el campo tiene un error.

#### El botón, solo si todo está bien
```javascript
enviar.disabled = errorNombre(nombre.value) !== '' || errorCorreo(correo.value) !== '';
```

#### Enviar sin recargar
```javascript
form.addEventListener('submit', (e) => {
  e.preventDefault();       // la página no se recarga
  gracias.textContent = `¡Gracias, ${nombre.value}!`;
  form.reset();             // vacía todos los campos
});
```

> **Siempre se valida dos veces.** Lo que valida JavaScript es para **ayudar** a quien escribe. Alguien con malas intenciones puede saltearlo, así que el servidor tiene que volver a validar. En PHP, eso lo hace Elefa en el Puerto.

### Código de ejemplo

```javascript
function errorCorreo(valor) {
  if (valor.trim() === '') return 'Falta el correo.';
  if (!valor.includes('@')) return 'El correo necesita una @.';
  if (valor.endsWith('@')) return 'Falta lo que va después de la @.';
  return '';
}

for (const prueba of ['', 'teo', 'teo@', 'teo@talleres']) {
  console.log(`«${prueba}» → ${errorCorreo(prueba) || 'bien'}`);
}
```

### Salida esperada

```
«» → Falta el correo.
«teo» → El correo necesita una @.
«teo@» → Falta lo que va después de la @.
«teo@talleres» → bien
```

### ¿Para qué sirve?

Todos los formularios de la web avisan así: el registro de una cuenta, una compra, un turno médico. Avisar al lado del campo, en el momento, es lo que hace que la gente los complete y no los abandone.

### Errores habituales

**Ogro: validar solo al enviar.** Si el error aparece recién al final, la persona ya se fue a otro campo y no sabe cuál está mal. Validá en `input` y mostrá el error al lado.

**Esqueleto: `form.reset` sin paréntesis.** `form.reset` es la función; `form.reset()` la ejecuta.

**Troll: el botón que nunca se habilita.** Si `disabled` se calcula una sola vez al cargar, queda deshabilitado para siempre. Hay que recalcularlo en cada `input`.

**Goblin: `trim` olvidado.** Un nombre de tres espacios no está vacío para `=== ''`. Con `.trim()` sí.

### Micro-misión S01-N04-P1 · Cuántas letras quedan

```meta
lugar: El escaparate, la caja de pedidos
personajes: Nima, Gheco, Teo, la Polilla
carta: Contador | mensaje.addEventListener('input', () => cuenta.textContent = `${mensaje.value.length} / 140`)
recompensa: xp 10, oro 10
```

#### Escena
La Polilla se come primero los mensajes larguísimos. —¡Que la gente vea cuánto le queda! —grita Teo, tapando la caja con el cuerpo.

#### Gheco sugiere
En cada `input` del `#mensaje`, mostrá en `#cuenta` cuántas letras lleva sobre 140. Si pasa de 140, agregale la clase `pasado` a `#cuenta` (y sacala si vuelve a estar bien).

#### Desafío
Escriben un pedido corto y después uno largo.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #f6efe3; color: #2b1d0e; padding: 16px; }
  textarea { width: 100%; height: 80px; }
  #cuenta.pasado { color: #c62828; font-weight: bold; }
</style>
<label for="mensaje">Tu pedido</label>
<textarea id="mensaje" maxlength="200"></textarea>
<p id="cuenta">0 / 140</p>
```

#### Eventos
```
escribir #mensaje Un rosetón azul para la cocina.
escribir #mensaje Quiero un vitral enorme con todos los colores del arco iris, una luna, un sol, tres estrellas, un faro, el mar, una gema, un dragón y a la Reina de las Luciérnagas volando.
```

#### Estado
```
#cuenta
#cuenta @class
```

#### Código inicial
```javascript
const mensaje = document.querySelector('#mensaje');
const cuenta = document.querySelector('#cuenta');

```

#### Salida esperada
```
── Estado ──
#cuenta: 172 / 140
#cuenta @class: pasado
```

#### Solución
```javascript
const mensaje = document.querySelector('#mensaje');
const cuenta = document.querySelector('#cuenta');
mensaje.addEventListener('input', () => {
  const largo = mensaje.value.length;
  cuenta.textContent = `${largo} / 140`;
  cuenta.classList.toggle('pasado', largo > 140);
});
```

#### Al superarla
El contador se pone rojo cuando el pedido se pasa. La Polilla se acerca al número, lo huele y se aleja: no hay nada para comer.

#### Imagen
- Una polilla gris enorme y peluda, con las alas llenas de letras que se comió, revoloteando sobre un formulario de madera (dibujo tierno, no da miedo).
- Un contador de números rojos al pie del formulario; Teo tapa la caja de pedidos con el cuerpo.

### Micro-misión S01-N04-P2 · El aviso al lado del campo

```meta
lugar: El escaparate, la caja de pedidos
personajes: Nima, Gheco, la Polilla
carta: Error en vivo | error.textContent = errorCorreo(campo.value) · campo.setAttribute('aria-invalid', …)
recompensa: xp 10, oro 10
```

#### Escena
La Polilla se lanza sobre un correo sin arroba. Nima la espanta con el arco y la Polilla da una vuelta y espera.

#### Gheco sugiere
Escribí `errorCorreo(valor)`: si está vacío, `Falta el correo.`; si no tiene `@`, `El correo necesita una @.`; si está bien, `''`. En cada `input` del correo, mostrá el error en `#error-correo` y poné `aria-invalid` en `true` o `false`.

#### Desafío
Escriben `teo` y después `teo@talleres`.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #f6efe3; color: #2b1d0e; padding: 16px; }
  input[aria-invalid=true] { border: 2px solid #c62828; }
  .error { color: #c62828; min-height: 1.2em; margin: 4px 0; }
</style>
<label for="correo">Tu correo</label>
<input id="correo" type="text">
<p class="error" id="error-correo"></p>
```

#### Eventos
```
escribir #correo teo
escribir #correo teo@talleres
```

#### Estado
```
#error-correo
#correo @aria-invalid
```

#### Código inicial
```javascript
const correo = document.querySelector('#correo');
const error = document.querySelector('#error-correo');

function errorCorreo(valor) {

}

```

#### Salida esperada
```
── Estado ──
#error-correo: (vacío)
#correo @aria-invalid: false
```

#### Solución
```javascript
const correo = document.querySelector('#correo');
const error = document.querySelector('#error-correo');

function errorCorreo(valor) {
  if (valor.trim() === '') return 'Falta el correo.';
  if (!valor.includes('@')) return 'El correo necesita una @.';
  return '';
}

correo.addEventListener('input', () => {
  const mensaje = errorCorreo(correo.value);
  error.textContent = mensaje;
  correo.setAttribute('aria-invalid', String(mensaje !== ''));
});
```

#### Al superarla
Mientras el correo no tiene arroba, un aviso rojo lo dice al lado. Cuando aparece la `@`, el aviso se borra. La Polilla da otra vuelta, sin hambre.

#### Imagen
- Un campo de formulario de madera con un borde rojo y un cartelito de aviso al lado, y la polilla girando alrededor sin poder comer.
- Nima con el arco bajo, vigilando.

### Micro-misión S01-N04-P3 · El botón que espera

```meta
lugar: El escaparate, la caja de pedidos
personajes: Nima, Gheco, Teo, la Polilla
carta: disabled | enviar.disabled = errores().length > 0
recompensa: xp 10, oro 10
```

#### Escena
—Si el formulario está mal —dice Teo—, que el botón **ni se pueda tocar**. Así la Polilla no tiene nada que comer.

#### Gheco sugiere
Escribí `errores()`, que devuelve la lista de errores de los dos campos (los vacíos no cuentan). Después de cada `input` en el formulario (con delegación, en el `form`), deshabilitá `#enviar` si hay alguno.

#### Desafío
Al empezar el botón está deshabilitado. Escriben el nombre (sigue deshabilitado) y después el correo: se habilita.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #f6efe3; color: #2b1d0e; padding: 16px; }
  label { display: block; margin-top: 8px; }
  button:disabled { opacity: .4; }
</style>
<form id="pedido">
  <label>Nombre <input id="nombre"></label>
  <label>Correo <input id="correo"></label>
  <button id="enviar">Enviar pedido</button>
</form>
<p id="estado"></p>
```

#### Eventos
```
escribir #nombre Doña Mirta
escribir #correo mirta@feria
```

#### Estado
```
#enviar @disabled
```

#### Código inicial
```javascript
const form = document.querySelector('#pedido');
const nombre = document.querySelector('#nombre');
const correo = document.querySelector('#correo');
const enviar = document.querySelector('#enviar');

function errores() {
  const lista = [];
  if (nombre.value.trim() === '') lista.push('Falta el nombre.');
  if (!correo.value.includes('@')) lista.push('El correo necesita una @.');
  return lista;
}

enviar.disabled = errores().length > 0;
```

#### Salida esperada
```
── Estado ──
#enviar @disabled: no
```

#### Solución
```javascript
const form = document.querySelector('#pedido');
const nombre = document.querySelector('#nombre');
const correo = document.querySelector('#correo');
const enviar = document.querySelector('#enviar');

function errores() {
  const lista = [];
  if (nombre.value.trim() === '') lista.push('Falta el nombre.');
  if (!correo.value.includes('@')) lista.push('El correo necesita una @.');
  return lista;
}

function revisar() {
  enviar.disabled = errores().length > 0;
}

revisar();
form.addEventListener('input', revisar);
```

#### Al superarla
El botón está apagado hasta que el pedido está completo, y se enciende recién al final. La Polilla se posa en el botón apagado y no encuentra nada.

#### Imagen
- Un botón de bronce apagado, opaco, con la polilla posada encima, confundida.
- Teo, con el dedo listo para tocar el botón, espera.

### Micro-misión S01-N04-P4 · El pedido llega entero

```meta
lugar: El escaparate, la caja de pedidos
personajes: Nima, Gheco, Teo
carta: submit | e.preventDefault() · gracias.textContent = … · form.reset()
recompensa: xp 15, monedas 5
```

#### Escena
Ahora sí: alguien completa el pedido y lo manda. Pero la página se recarga y el pedido se pierde en el camino. Teo se agarra la cabeza.

#### Gheco sugiere
En el `submit` del formulario, frená la recarga con `preventDefault`. Agregá el pedido como un `<li>` en `#pedidos` (`nombre: mensaje`), mostrá `¡Gracias, nombre!` en `#gracias` y limpiá el formulario con `reset()`.

#### Desafío
Doña Mirta manda un pedido.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #f6efe3; color: #2b1d0e; padding: 16px; }
  label { display: block; margin-top: 8px; }
  #gracias { color: #2e7d32; font-weight: bold; }
</style>
<form id="pedido">
  <label>Nombre <input id="nombre" name="nombre"></label>
  <label>Pedido <input id="mensaje" name="mensaje"></label>
  <button>Enviar pedido</button>
</form>
<p id="gracias"></p>
<ul id="pedidos"></ul>
```

#### Eventos
```
escribir #nombre Doña Mirta
escribir #mensaje Un vitral con un pan con miel
click #pedido button
```

#### Estado
```
#gracias
#pedidos li
#nombre @value
```

#### Código inicial
```javascript
const form = document.querySelector('#pedido');
const nombre = document.querySelector('#nombre');
const mensaje = document.querySelector('#mensaje');

form.addEventListener('submit', () => {
  document.querySelector('#gracias').textContent = 'Gracias';
});
```

#### Salida esperada
```
── Estado ──
#gracias: ¡Gracias, Doña Mirta!
#pedidos li: Doña Mirta: Un vitral con un pan con miel
#nombre @value: (vacío)
```

#### Solución
```javascript
const form = document.querySelector('#pedido');
const nombre = document.querySelector('#nombre');
const mensaje = document.querySelector('#mensaje');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const li = document.createElement('li');
  li.textContent = `${nombre.value}: ${mensaje.value}`;
  document.querySelector('#pedidos').append(li);
  document.querySelector('#gracias').textContent = `¡Gracias, ${nombre.value}!`;
  form.reset();
});
```

#### Al superarla
El pedido aparece en la lista, entero, con su nombre. El formulario queda limpio para el siguiente. Teo lo copia en un papel para llevárselo a Tesela, corriendo.

#### Imagen
- Una lista de pedidos escrita en vidrio en el escaparate, con el primer renglón brillante.
- Doña Mirta sonríe con su pedido hecho; Teo corre con un papel en la mano.

### Micro-misión S01-N04-P5 · Jefe: la Polilla se va

```meta
lugar: El escaparate, la caja de pedidos
personajes: Nima, Gheco, Teo, la Polilla, Lumina
carta: El formulario completo | errores en vivo · botón con disabled · submit con preventDefault · reset
recompensa: xp 50, oro 50, monedas 1
```

#### Escena
La Polilla junta fuerzas para su último ataque: se pone delante de toda la luz del escaparate, enorme, y espera el próximo pedido mal hecho. —Ahora o nunca —dice Teo—. Un formulario que avise **todo**.

#### Gheco sugiere
Juntá todo: `errores()` devuelve un objeto con el error de cada campo (`nombre`, `correo`, `mensaje`; `''` si está bien). En cada `input`, mostrá el error de cada campo en su `#error-…`, marcá `aria-invalid` y deshabilitá `#enviar` si hay alguno. Al enviar, `preventDefault`, agradecé y `reset()`; después del reset, volvé a revisar (el botón queda deshabilitado otra vez).

Las reglas: el nombre no puede estar vacío; el correo necesita una `@` y algo después; el mensaje, entre 10 y 140 letras.

#### Desafío
Escriben un correo sin arroba, lo corrigen, completan todo y lo mandan. Enseguida, Bengala empieza otro pedido con un correo a medias.

#### Página
```html
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #f6efe3; color: #2b1d0e; padding: 16px; }
  label { display: block; margin-top: 8px; }
  [aria-invalid=true] { border: 2px solid #c62828; }
  .error { color: #c62828; min-height: 1.1em; margin: 2px 0; font-size: 13px; }
  button:disabled { opacity: .4; }
  #gracias { color: #2e7d32; font-weight: bold; }
</style>
<form id="pedido" novalidate>
  <label>Nombre <input id="nombre"></label><p class="error" id="error-nombre"></p>
  <label>Correo <input id="correo"></label><p class="error" id="error-correo"></p>
  <label>Pedido <textarea id="mensaje"></textarea></label><p class="error" id="error-mensaje"></p>
  <button id="enviar">Enviar pedido</button>
</form>
<p id="gracias"></p>
```

#### Eventos
```
escribir #correo lucio.feria
escribir #correo lucio@feria
escribir #nombre Lucio
escribir #mensaje Un farol de vidrio amarillo
click #enviar
escribir #correo bengala@
```

#### Estado
```
#gracias
.error
[aria-invalid=true] #
#enviar @disabled
#nombre @value
```

#### Código inicial
```javascript
const form = document.querySelector('#pedido');
const campos = {
  nombre: document.querySelector('#nombre'),
  correo: document.querySelector('#correo'),
  mensaje: document.querySelector('#mensaje'),
};
const enviar = document.querySelector('#enviar');

function errores() {
  return {
    nombre: '',
    correo: '',
    mensaje: '',
  };
}

```

#### Salida esperada
```
── Estado ──
#gracias: ¡Gracias, Lucio! Tu pedido va para los Talleres.
.error: (vacío)
.error: Falta lo que va después de la @.
.error: (vacío)
[aria-invalid=true] #: 1
#enviar @disabled: sí
#nombre @value: (vacío)
```

#### Solución
```javascript
const form = document.querySelector('#pedido');
const campos = {
  nombre: document.querySelector('#nombre'),
  correo: document.querySelector('#correo'),
  mensaje: document.querySelector('#mensaje'),
};
const enviar = document.querySelector('#enviar');
let tocados = new Set();

function errores() {
  const correo = campos.correo.value.trim();
  const largo = campos.mensaje.value.trim().length;
  return {
    nombre: campos.nombre.value.trim() === '' ? 'Falta el nombre.' : '',
    correo: !correo.includes('@') ? 'El correo necesita una @.' : correo.endsWith('@') ? 'Falta lo que va después de la @.' : '',
    mensaje: largo < 10 ? 'El pedido necesita al menos 10 letras.' : largo > 140 ? 'El pedido se pasa de 140 letras.' : '',
  };
}

function revisar() {
  const lista = errores();
  for (const [nombre, error] of Object.entries(lista)) {
    const mostrar = tocados.has(nombre) ? error : '';
    document.querySelector(`#error-${nombre}`).textContent = mostrar;
    campos[nombre].setAttribute('aria-invalid', String(mostrar !== ''));
  }
  enviar.disabled = Object.values(lista).some((error) => error !== '');
}

form.addEventListener('input', (e) => {
  tocados.add(e.target.id);
  revisar();
});

form.addEventListener('submit', (e) => {
  e.preventDefault();
  document.querySelector('#gracias').textContent = `¡Gracias, ${campos.nombre.value}! Tu pedido va para los Talleres.`;
  form.reset();
  tocados = new Set();
  revisar();
});

revisar();
```

#### Al superarla
El pedido de Lucio sale entero, y el formulario queda limpio y con el botón apagado, esperando al siguiente. La Polilla ya no tiene nada que comer: da tres vueltas alrededor del escaparate, se posa en el farolito de {mentor} y se queda ahí, tranquila, mirando la luz.

—No era mala —dice {mentor}—. Tenía hambre y solo encontraba errores. —Teo llena el carro con las páginas vivas y sale corriendo hacia los Talleres. A la semana llega una carta de Tesela, de una sola línea: *«Ahora mis vitrales se mueven. Gracias, Nima.»*

#### Imagen
- La polilla gris y peluda posada en calma sobre el farolito de Lumina, iluminada en amarillo, con las alas ya sin letras.
- Teo se va corriendo con el carro lleno de vitrales que brillan y se mueven, y una carta con el sello de colores de los Talleres llega en una flecha de luz.
