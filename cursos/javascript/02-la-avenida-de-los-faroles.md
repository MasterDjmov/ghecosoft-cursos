# RAMA R02 · La Avenida de los Faroles: la página y los eventos

```meta
tipo: tronco
posicion: 2
```

## R02-N01 · La página: seleccionar y cambiar

```meta
tipo: tema
padre: R01-N08
precio: 10
criatura: orc
temas: js.dom
```

### Crónica

La **Avenida de los Faroles** es la calle principal de la Feria: cientos de faroles de vidrio, carteles, vidrieras y guirnaldas. De noche la recorre **Lucio**, el farolero, un viejo flaco con una escalera al hombro y una vara con una mecha. Prende los faroles de a uno, a mano, y a la madrugada todavía le faltan la mitad.

—La Avenida es una **página** —dice {mentor}—. Cada farol, cada cartel, cada vidriera es un **elemento**. JavaScript los puede encontrar por su nombre y cambiarlos todos, sin subir la escalera.

### Objetivos

- Entender qué es el DOM: la página como un árbol de elementos que JavaScript puede leer y cambiar.
- Encontrar elementos con `querySelector` y `querySelectorAll`.
- Cambiar su texto (`textContent`), sus clases (`classList`), su estilo (`style`) y sus atributos (`setAttribute`).

### Antes de empezar

- La Clase 0 (cambiaste un cartel) y los Puestos de Juegos (R01).

### Explicación

#### El DOM
Cuando el navegador lee el HTML, arma en memoria un **árbol de elementos**: el DOM (*Document Object Model*). JavaScript lo ve en la variable `document`. Si cambiás el DOM, la página cambia en el momento, sin recargar.

#### Encontrar elementos
```javascript
const titulo = document.querySelector('h1');          // el primero que coincide
const cartel = document.querySelector('#cartel');     // por id
const farol = document.querySelector('.farol');       // por clase (el primero)
const faroles = document.querySelectorAll('.farol');  // todos (una lista)
```
Los selectores son los mismos de CSS: `#id`, `.clase`, `etiqueta`, `nav a`, `[data-x]`. Si no encuentra nada, `querySelector` devuelve `null` (un orco que espera).

`querySelectorAll` devuelve una lista que se recorre con `for…of` o con `.forEach(…)`.

#### Cambiar
```javascript
cartel.textContent = 'Abierto';             // el texto
farol.classList.add('prendido');            // agrega una clase
farol.classList.remove('roto');             // la saca
farol.classList.toggle('prendido');         // la pone si no está, la saca si está
farol.style.backgroundColor = 'gold';       // un estilo (en camelCase)
imagen.setAttribute('alt', 'Un farol');     // un atributo
```
Conviene cambiar **clases** antes que estilos: el aspecto queda en el CSS y JavaScript solo dice «este está prendido».

### Código de ejemplo

```javascript
// Este ejemplo crea su propia avenida (en las micro-misiones, la página ya viene armada).
document.body.innerHTML = `
  <h1 id="cartel">Avenida a oscuras</h1>
  <span class="farol"></span><span class="farol"></span><span class="farol roto"></span>
`;

const cartel = document.querySelector('#cartel');
const faroles = document.querySelectorAll('.farol');
console.log('Faroles:', faroles.length);

for (const farol of faroles) {
  if (!farol.classList.contains('roto')) farol.classList.add('prendido');
}
cartel.textContent = 'Avenida encendida';

console.log(cartel.textContent);
console.log([...faroles].map((f) => f.className));
console.log(document.querySelector('#no-existe'));
```

### Salida esperada

```
Faroles: 3
Avenida encendida
[ 'farol prendido', 'farol prendido', 'farol roto' ]
null
```

### ¿Para qué sirve?

Todo lo que se mueve en una página web pasa por acá: un menú que se abre, un carrito que suma, un mensaje de error en un formulario. Los frameworks como React lo hacen por vos, pero por debajo hacen exactamente esto.

### Errores habituales

**Orco: el elemento no está.** `document.querySelector('#carteI')` (con I mayúscula) da `null`, y la línea siguiente explota con `Cannot set properties of null (setting 'textContent')`. Revisá el selector.

**Slime: olvidarse el `#` o el `.`.** `querySelector('cartel')` busca una **etiqueta** `<cartel>`, no el id.

**Ogro: tratar la lista como un elemento.** `querySelectorAll('.farol').classList` da `undefined`: es una lista; hay que recorrerla.

**Ogro: `innerHTML` con datos de afuera.** Mete HTML de verdad en la página. Con texto que escribió alguien, usá `textContent` (más seguro).

### Micro-misión R02-N01-P1 · El primer cartel de la Avenida

```meta
lugar: La Avenida de los Faroles
personajes: Nima, Gheco, Lucio
carta: querySelector | document.querySelector('#id') · .textContent = 'texto' cambia lo que dice
recompensa: xp 10, oro 10
```

#### Escena
Lucio, el farolero, saluda a Nima con la vara. —El cartel de la Avenida dice *Cerrada* desde que se fue el Vidriero. ¿Me lo cambiás?

#### Gheco sugiere
`document.querySelector('#avenida')` encuentra el cartel por su id. Después, `.textContent = '…'`.

#### Desafío
Hacé que el cartel diga `Avenida de los Faroles`.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; text-align: center; padding: 24px; }
  h1 { border: 3px solid #ffd400; border-radius: 10px; display: inline-block; padding: 8px 24px; }
</style>
<h1 id="avenida">Cerrada</h1>
```

#### Estado
```
#avenida
```

#### Código inicial
```javascript
const cartel = ___;
cartel.textContent = ___;
```

#### Salida esperada
```
── Estado ──
#avenida: Avenida de los Faroles
```

#### Solución
```javascript
const cartel = document.querySelector('#avenida');
cartel.textContent = 'Avenida de los Faroles';
```

#### Al superarla
Las letras del cartel se encienden de una en una. Lucio se saca la gorra. —Treinta años esperé ver eso de nuevo.

#### Imagen
- La entrada de una avenida de feria nocturna con un gran cartel de madera con borde de foquitos amarillos (sin letras legibles) y una fila de faroles de vidrio apagados.
- Lucio (farolero viejo y flaco, gorra de lana, abrigo largo abotonado, escalera al hombro y una vara con mecha) mira el cartel; Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas, arco verde) a su lado; Gheco en su hombro.

### Micro-misión R02-N01-P2 · Prender sin escalera

```meta
lugar: La Avenida de los Faroles
personajes: Nima, Gheco, Lucio
carta: classList | el.classList.add('x') agrega una clase · remove la saca · el CSS hace el resto
recompensa: xp 10, oro 10
```

#### Escena
Lucio sube la escalera para el primer farol y le duele la rodilla. Nima le pide que se quede abajo: ella lo prende desde el código.

#### Gheco sugiere
El CSS de la página ya dice cómo se ve un farol con la clase `prendido`. Solo hay que agregársela: `farol.classList.add('prendido')`.

#### Desafío
Prendé el farol `#primero`.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; text-align: center; padding: 24px; }
  .farol { display: inline-block; width: 50px; height: 50px; border-radius: 50%; background: #333; margin: 8px; }
  .farol.prendido { background: #ffd400; box-shadow: 0 0 24px #ffd400; }
</style>
<span class="farol" id="primero"></span><span class="farol"></span><span class="farol"></span>
```

#### Estado
```
.farol @class
```

#### Código inicial
```javascript
const farol = document.querySelector('#primero');
```

#### Salida esperada
```
── Estado ──
.farol @class: farol prendido
.farol @class: farol
.farol @class: farol
```

#### Solución
```javascript
const farol = document.querySelector('#primero');
farol.classList.add('prendido');
```

#### Al superarla
El primer farol se enciende sin que nadie suba. Lucio baja la escalera y la apoya contra la pared, por primera vez en años.

#### Imagen
- Una fila de tres faroles de vidrio de feria sobre postes, el primero prendido con luz amarilla y los otros apagados.
- Lucio, apoyado en su escalera, mira asombrado; Nima con la mano levantada, como si hubiera tirado una flecha invisible.

### Micro-misión R02-N01-P3 · Toda la fila

```meta
lugar: La Avenida de los Faroles
personajes: Nima, Gheco, Lucio
carta: querySelectorAll | devuelve todos · se recorre con for…of o con .forEach((el) => …)
recompensa: xp 10, oro 10
```

#### Escena
—Uno está bien —dice Lucio—. Pero la Avenida tiene cientos.

#### Gheco sugiere
`document.querySelectorAll('.farol')` trae todos. Recorrelos y agregale `prendido` a cada uno.

#### Desafío
Prendé **todos** los faroles.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; text-align: center; padding: 24px; }
  .farol { display: inline-block; width: 40px; height: 40px; border-radius: 50%; background: #333; margin: 6px; }
  .farol.prendido { background: #ffd400; box-shadow: 0 0 20px #ffd400; }
</style>
<span class="farol"></span><span class="farol"></span><span class="farol"></span><span class="farol"></span><span class="farol"></span>
```

#### Estado
```
.farol.prendido #
```

#### Código inicial
```javascript
const faroles = document.querySelectorAll('.farol');

```

#### Salida esperada
```
── Estado ──
.farol.prendido #: 5
```

#### Solución
```javascript
const faroles = document.querySelectorAll('.farol');

for (const farol of faroles) {
  farol.classList.add('prendido');
}
```

#### Al superarla
Una ola de luz corre por la Avenida, de punta a punta. La gente de la Feria sale de los puestos a mirar.

#### Imagen
- Una avenida de feria nocturna larga con todos los faroles prendidos en fila hasta perderse de vista, gente mirando desde los puestos.
- Nima y Lucio en el medio de la calle; Gheco salta de alegría.

### Micro-misión R02-N01-P4 · Los faroles rotos

```meta
lugar: La Avenida de los Faroles
personajes: Nima, Gheco, Lucio
carta: Clases y decisiones | el.classList.contains('x') pregunta · toggle la pone o la saca
recompensa: xp 10, oro 10
```

#### Escena
Algunos faroles están rotos: si les llega luz, revientan el vidrio. Hay que prender solo los sanos.

#### Gheco sugiere
`farol.classList.contains('roto')` devuelve `true` si está roto. Prendé solo los que **no** lo están.

#### Desafío
Prendé los faroles que no tienen la clase `roto`.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; text-align: center; padding: 24px; }
  .farol { display: inline-block; width: 40px; height: 40px; border-radius: 50%; background: #333; margin: 6px; }
  .farol.roto { background: #552222; }
  .farol.prendido { background: #ffd400; box-shadow: 0 0 20px #ffd400; }
</style>
<span class="farol"></span><span class="farol roto"></span><span class="farol"></span><span class="farol roto"></span><span class="farol"></span>
```

#### Estado
```
.farol @class
```

#### Código inicial
```javascript
const faroles = document.querySelectorAll('.farol');

for (const farol of faroles) {
  farol.classList.add('prendido');
}
```

#### Salida esperada
```
── Estado ──
.farol @class: farol prendido
.farol @class: farol roto
.farol @class: farol prendido
.farol @class: farol roto
.farol @class: farol prendido
```

#### Solución
```javascript
const faroles = document.querySelectorAll('.farol');

for (const farol of faroles) {
  if (!farol.classList.contains('roto')) {
    farol.classList.add('prendido');
  }
}
```

#### Al superarla
Los faroles rotos se quedan quietos, a oscuras. Lucio les pone una cinta roja: mañana se arreglan.

#### Imagen
- Una fila de faroles de feria, algunos prendidos y otros con el vidrio rajado y una cinta roja atada.
- Lucio ata una cinta roja a un farol roto; Nima sostiene la escalera.

### Micro-misión R02-N01-P5 · El color de cada puesto

```meta
lugar: La Avenida de los Faroles
personajes: Nima, Gheco, Lucio
carta: style y atributos | el.style.color = 'gold' · camelCase: backgroundColor · el.setAttribute('title', '…')
recompensa: xp 15, monedas 5
```

#### Escena
Cada puesto de la Avenida tiene su color. Lucio quiere que la vidriera del puesto de pan tenga el fondo color miel y un cartelito que aparezca al pasar el mouse.

#### Gheco sugiere
`vidriera.style.backgroundColor = 'goldenrod'` cambia el fondo, y `vidriera.setAttribute('title', 'Pan con miel')` pone el cartelito.

#### Desafío
Dale a `#pan` el fondo `goldenrod` y el `title` `Pan con miel`.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  .vidriera { width: 160px; height: 90px; border: 3px solid #f5f0e0; border-radius: 8px; display: inline-block; margin: 6px; }
</style>
<div class="vidriera" id="pan"></div><div class="vidriera" id="premios"></div>
```

#### Estado
```
estilo #pan { background-color }
#pan @title
```

#### Código inicial
```javascript
const vidriera = document.querySelector('#pan');

```

#### Salida esperada
```
── Estado ──
estilo #pan { background-color }: rgb(218, 165, 32)
#pan @title: Pan con miel
```

#### Solución
```javascript
const vidriera = document.querySelector('#pan');
vidriera.style.backgroundColor = 'goldenrod';
vidriera.setAttribute('title', 'Pan con miel');
```

#### Al superarla
La vidriera del pan se pone color miel y Doña Mirta, desde adentro, saluda con el cucharón.

#### Imagen
- Una vidriera de feria con fondo color miel y panes dorados, al lado de otra vidriera apagada.
- Doña Mirta (petisa, delantal floreado) saluda desde adentro con un cucharón; Nima y Lucio miran desde la calle.

### Micro-misión R02-N01-P6 · El orco del selector

```meta
lugar: La Avenida de los Faroles
personajes: Nima, Gheco, Lucio
criatura: orc
carta: null | querySelector da null si no encuentra · ?. evita que explote · revisá # y .
recompensa: xp 15, monedas 5
```

#### Escena
Lucio escribió un programa para prender el farol de la fuente, pero explota con un error rojo y no prende nada. Un orco se ríe detrás de la fuente.

#### Gheco sugiere
Leé el error: `Cannot read properties of null`. El selector no encontró nada. ¿Es un id o una clase?

#### Desafío
Arreglá el selector para que el farol de la fuente se prenda.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; text-align: center; padding: 24px; }
  .farol { display: inline-block; width: 50px; height: 50px; border-radius: 50%; background: #333; }
  .farol.prendido { background: #ffd400; box-shadow: 0 0 24px #ffd400; }
</style>
<p>La fuente</p>
<span class="farol" id="fuente"></span>
```

#### Estado
```
#fuente @class
```

#### Código inicial
```javascript
const farol = document.querySelector('.fuente');
farol.classList.add('prendido');
```

#### Salida esperada
```
── Estado ──
#fuente @class: farol prendido
```

#### Solución
```javascript
const farol = document.querySelector('#fuente');
farol.classList.add('prendido');
```

#### Al superarla
El farol de la fuente se prende y el orco sale corriendo con la cara tapada. El agua de la fuente brilla amarilla.

#### Imagen
- Una fuente de piedra en una plaza de feria nocturna, con un farol prendido que se refleja amarillo en el agua.
- Un orco chiquito y torpe de feria (sin armas) huye tapándose los ojos; Nima y Lucio, satisfechos.

## R02-N02 · Crear y borrar elementos

```meta
tipo: tema
padre: R02-N01
precio: 10
criatura: orc
temas: js.dom
```

### Crónica

En la mitad de la Avenida hay un gran **tablero de anuncios** vacío: antes, ahí se colgaban los avisos de la Feria (quién ganó, qué puesto abre, qué se perdió). Desde que se fue el Vidriero, nadie colgó nada más.

—No alcanza con cambiar lo que hay —dice {mentor}—. A veces hay que **crear** cosas nuevas en la página, y a veces, sacarlas.

### Objetivos

- Crear elementos con `document.createElement` y agregarlos con `append` y `prepend`.
- Sacarlos con `remove()`.
- Armar una lista en la página a partir de un arreglo.
- Saber la diferencia entre `textContent` e `innerHTML`.

### Antes de empezar

- R02-N01: seleccionar y cambiar elementos.

### Explicación

#### Crear y agregar
```javascript
const aviso = document.createElement('li');   // un <li> nuevo, todavía fuera de la página
aviso.textContent = 'Abre la calesita';
aviso.classList.add('aviso');
lista.append(aviso);                           // ahora sí: al final de la lista
lista.prepend(otro);                           // o al principio
```

#### Sacar
```javascript
document.querySelector('.vencido').remove();
```

#### De un arreglo a la página
```javascript
const avisos = ['Gana Nima', 'Abre la calesita'];
for (const texto of avisos) {
  const li = document.createElement('li');
  li.textContent = texto;
  lista.append(li);
}
```

#### textContent contra innerHTML
- `el.textContent = '<b>hola</b>'` muestra los símbolos tal cual: es **texto**.
- `el.innerHTML = '<b>hola</b>'` lo interpreta como **HTML**.

Con datos que escribió alguien (un nombre, un comentario), usá siempre `textContent`. Si usás `innerHTML`, esa persona puede meter HTML en tu página (así empiezan muchos ataques).

### Código de ejemplo

```javascript
document.body.innerHTML = '<ul id="tablero"><li class="vencido">Se perdió un gato</li></ul>';
const tablero = document.querySelector('#tablero');

const avisos = ['Gana Nima en el tiro', 'Abre la calesita'];
for (const texto of avisos) {
  const li = document.createElement('li');
  li.textContent = texto;
  tablero.append(li);
}

document.querySelector('.vencido').remove();

const urgente = document.createElement('li');
urgente.textContent = '¡Fuegos a las 22!';
tablero.prepend(urgente);

console.log([...tablero.children].map((li) => li.textContent));
```

### Salida esperada

```
[ '¡Fuegos a las 22!', 'Gana Nima en el tiro', 'Abre la calesita' ]
```

### ¿Para qué sirve?

Cada vez que una página muestra datos que no estaban al cargar (los mensajes nuevos de un chat, los resultados de una búsqueda, los productos de un carrito), hay JavaScript creando elementos.

### Errores habituales

**Ogro: crear y no agregar.** `createElement` crea el elemento, pero hasta que no hacés `append`, no está en la página.

**Ogro: usar `innerHTML +=` en un bucle.** Rehace toda la lista en cada vuelta (y borra los eventos que tenían). Mejor `createElement` + `append`.

**Troll: `innerHTML` con texto de afuera.** Lo que escriba alguien se vuelve HTML de tu página.

### Micro-misión R02-N02-P1 · El primer aviso

```meta
lugar: El tablero de anuncios
personajes: Nima, Gheco, Lucio
carta: createElement | const li = document.createElement('li') · li.textContent = '…' · lista.append(li)
recompensa: xp 10, oro 10
```

#### Escena
Lucio le alcanza a Nima un papel en blanco y un clavo. —El primer aviso en treinta años. Que sea bueno.

#### Gheco sugiere
Creá un `li`, ponele el texto y agregalo a la lista `#avisos` con `append`.

#### Desafío
Agregá un aviso que diga `Volvió la luz a la Avenida`.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #2b1d10; color: #3b2a14; padding: 24px; }
  ul { background: #c9a36b; border: 6px solid #6b4a24; padding: 16px 32px; min-height: 80px; }
  li { background: #fff8e0; margin: 6px 0; padding: 6px; list-style: none; }
</style>
<ul id="avisos"></ul>
```

#### Estado
```
#avisos li
```

#### Código inicial
```javascript
const avisos = document.querySelector('#avisos');

```

#### Salida esperada
```
── Estado ──
#avisos li: Volvió la luz a la Avenida
```

#### Solución
```javascript
const avisos = document.querySelector('#avisos');

const aviso = document.createElement('li');
aviso.textContent = 'Volvió la luz a la Avenida';
avisos.append(aviso);
```

#### Al superarla
El papel queda clavado en el centro del tablero. En cinco minutos, ya hay diez personas leyéndolo.

#### Imagen
- Un gran tablero de corcho de feria con marco de madera tallada, vacío salvo por un papel clavado en el centro (sin texto legible).
- Nima clava el papel con un clavo de bronce; Lucio sostiene el farol para que vea; gente de feria se acerca a leer.

### Micro-misión R02-N02-P2 · Todos los avisos

```meta
lugar: El tablero de anuncios
personajes: Nima, Gheco, Lucio
carta: De un arreglo a la página | for (const x of lista) { crear, llenar, append }
recompensa: xp 10, oro 10
```

#### Escena
Llegan los avisos atrasados de toda la semana. Lucio los trae en un arreglo.

#### Gheco sugiere
Recorré `nuevos` y, por cada texto, creá un `li` y agregalo.

#### Desafío
Colgá los tres avisos, en orden.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #2b1d10; color: #3b2a14; padding: 24px; }
  ul { background: #c9a36b; border: 6px solid #6b4a24; padding: 16px 32px; min-height: 80px; }
  li { background: #fff8e0; margin: 6px 0; padding: 6px; list-style: none; }
</style>
<ul id="avisos"></ul>
```

#### Estado
```
li #
li
```

#### Código inicial
```javascript
const avisos = document.querySelector('#avisos');
const nuevos = ['Abre la calesita', 'Gana Nima en el tiro', 'Se perdió un globo rojo'];

```

#### Salida esperada
```
── Estado ──
li #: 3
li: Abre la calesita
li: Gana Nima en el tiro
li: Se perdió un globo rojo
```

#### Solución
```javascript
const avisos = document.querySelector('#avisos');
const nuevos = ['Abre la calesita', 'Gana Nima en el tiro', 'Se perdió un globo rojo'];

for (const texto of nuevos) {
  const li = document.createElement('li');
  li.textContent = texto;
  avisos.append(li);
}
```

#### Al superarla
El tablero se llena. Alguien encuentra el globo rojo esa misma noche, gracias al aviso.

#### Imagen
- El tablero de anuncios de la feria lleno de papeles clavados de colores (sin texto legible), con un globo rojo atado a una esquina.
- Un nene recupera su globo rojo; Nima y Lucio sonríen.

### Micro-misión R02-N02-P3 · El aviso vencido

```meta
lugar: El tablero de anuncios
personajes: Nima, Gheco, Lucio
carta: remove | el.remove() saca el elemento de la página
recompensa: xp 10, oro 10
```

#### Escena
Entre los avisos hay uno viejísimo, amarillento: *El Vidriero atiende de 9 a 12*. Lucio lo mira un rato y le pide a Nima que lo saque.

#### Gheco sugiere
Encontralo por su clase `vencido` y usá `.remove()`.

#### Desafío
Sacá el aviso vencido del tablero.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #2b1d10; color: #3b2a14; padding: 24px; }
  ul { background: #c9a36b; border: 6px solid #6b4a24; padding: 16px 32px; }
  li { background: #fff8e0; margin: 6px 0; padding: 6px; list-style: none; }
  .vencido { background: #d8c48f; }
</style>
<ul id="avisos">
  <li>Abre la calesita</li>
  <li class="vencido">El Vidriero atiende de 9 a 12</li>
  <li>Gana Nima en el tiro</li>
</ul>
```

#### Estado
```
li #
.vencido #
```

#### Código inicial
```javascript
// Sacá el aviso vencido

```

#### Salida esperada
```
── Estado ──
li #: 2
.vencido #: 0
```

#### Solución
```javascript
// Sacá el aviso vencido
document.querySelector('.vencido').remove();
```

#### Al superarla
Lucio dobla el aviso viejo y se lo guarda en el bolsillo del abrigo. No dice nada, pero Nima ve que le tiembla la mano.

#### Imagen
- Primer plano de un papel amarillento y gastado (sin texto legible) en las manos viejas de Lucio, que lo dobla con cuidado.
- Atrás, el tablero de anuncios con un hueco donde estaba el papel; Nima mira a Lucio.

### Micro-misión R02-N02-P4 · El más reciente arriba

```meta
lugar: El tablero de anuncios
personajes: Nima, Gheco
carta: prepend | lista.prepend(el) agrega al principio · append, al final
recompensa: xp 10, oro 10
```

#### Escena
Bengala trae un aviso urgente: los fuegos se adelantan. Tiene que ir **arriba de todo**, no al final.

#### Gheco sugiere
`prepend` agrega al principio de la lista.

#### Desafío
Agregá `¡Los fuegos se adelantan!` al principio del tablero.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #2b1d10; color: #3b2a14; padding: 24px; }
  ul { background: #c9a36b; border: 6px solid #6b4a24; padding: 16px 32px; }
  li { background: #fff8e0; margin: 6px 0; padding: 6px; list-style: none; }
  .urgente { background: #ffb3a0; font-weight: bold; }
</style>
<ul id="avisos">
  <li>Abre la calesita</li>
  <li>Gana Nima en el tiro</li>
</ul>
```

#### Estado
```
li
li.urgente #
```

#### Código inicial
```javascript
const avisos = document.querySelector('#avisos');
const urgente = document.createElement('li');
urgente.textContent = '¡Los fuegos se adelantan!';
urgente.classList.add('urgente');
avisos.append(urgente);
```

#### Salida esperada
```
── Estado ──
li: ¡Los fuegos se adelantan!
li: Abre la calesita
li: Gana Nima en el tiro
li.urgente #: 1
```

#### Solución
```javascript
const avisos = document.querySelector('#avisos');
const urgente = document.createElement('li');
urgente.textContent = '¡Los fuegos se adelantan!';
urgente.classList.add('urgente');
avisos.prepend(urgente);
```

#### Al superarla
El aviso rojo queda arriba de todo y la gente corre a la explanada. Bengala llega justo.

#### Imagen
- El tablero de anuncios con un papel rojo de urgencia arriba de todo (sin texto legible) y gente corriendo hacia la explanada.
- Bengala (antiparras de cuero, delantal grueso) corre con cohetes bajo el brazo.

### Micro-misión R02-N02-P5 · La lista de ganadores

```meta
lugar: El tablero de anuncios
personajes: Nima, Gheco, Lucio
carta: Elementos con datos | crear · textContent con template literal · clase según una condición
recompensa: xp 15, monedas 5
```

#### Escena
Lucio quiere colgar la lista de ganadores de la noche, con sus puntos, y marcar en dorado a los que hicieron más de 20.

#### Gheco sugiere
Por cada ganador, un `li` con el texto `` `${g.nombre}: ${g.puntos}` ``. Si `g.puntos > 20`, agregale la clase `oro`.

#### Desafío
Armá la lista de ganadores en `#ganadores`.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #2b1d10; color: #3b2a14; padding: 24px; }
  ol { background: #c9a36b; border: 6px solid #6b4a24; padding: 16px 40px; }
  li { background: #fff8e0; margin: 6px 0; padding: 6px; }
  .oro { background: #ffd400; font-weight: bold; }
</style>
<ol id="ganadores"></ol>
```

#### Estado
```
#ganadores li
.oro #
```

#### Código inicial
```javascript
const lista = document.querySelector('#ganadores');
const ganadores = [
  { nombre: 'Nima', puntos: 24 },
  { nombre: 'Bruno', puntos: 18 },
  { nombre: 'Tati', puntos: 21 },
];

```

#### Salida esperada
```
── Estado ──
#ganadores li: Nima: 24
#ganadores li: Bruno: 18
#ganadores li: Tati: 21
.oro #: 2
```

#### Solución
```javascript
const lista = document.querySelector('#ganadores');
const ganadores = [
  { nombre: 'Nima', puntos: 24 },
  { nombre: 'Bruno', puntos: 18 },
  { nombre: 'Tati', puntos: 21 },
];

for (const g of ganadores) {
  const li = document.createElement('li');
  li.textContent = `${g.nombre}: ${g.puntos}`;
  if (g.puntos > 20) li.classList.add('oro');
  lista.append(li);
}
```

#### Al superarla
Tati ve su nombre en dorado y grita tan fuerte que se prende un farol más. Bruno dice que la próxima le gana.

#### Imagen
- Una lista de ganadores clavada en el tablero, con dos renglones resaltados en dorado (sin texto legible).
- Tati (dos colitas, delantal amarillo) salta de alegría; Bruno (gorra al revés, chaleco rojo) cruzado de brazos.

### Micro-misión R02-N02-P6 · El aviso con trampa

```meta
lugar: El tablero de anuncios
personajes: Nima, Gheco, Lucio
criatura: troll
carta: textContent contra innerHTML | textContent pone texto · innerHTML interpreta HTML · lo que escribe alguien, siempre como texto
recompensa: xp 15, monedas 5
```

#### Escena
Alguien dejó en el buzón un aviso raro, lleno de símbolos `<` y `>`. Cuando Lucio lo cuelga, en el tablero aparece un botón falso que dice *Ganaste 100 fichas*. Es una trampa de un troll.

#### Gheco sugiere
`innerHTML` convierte el texto en HTML de verdad. Con `textContent`, se ve tal cual, con los símbolos, y no hay botón.

#### Desafío
Colgá el aviso como **texto**, para que no aparezca ningún botón.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #2b1d10; color: #3b2a14; padding: 24px; }
  ul { background: #c9a36b; border: 6px solid #6b4a24; padding: 16px 32px; }
  li { background: #fff8e0; margin: 6px 0; padding: 6px; list-style: none; }
</style>
<ul id="avisos"></ul>
```

#### Estado
```
button #
#avisos li
```

#### Código inicial
```javascript
const delBuzon = 'Hola <button>Ganaste 100 fichas</button>';
const li = document.createElement('li');
li.innerHTML = delBuzon;
document.querySelector('#avisos').append(li);
```

#### Salida esperada
```
── Estado ──
button #: 0
#avisos li: Hola <button>Ganaste 100 fichas</button>
```

#### Solución
```javascript
const delBuzon = 'Hola <button>Ganaste 100 fichas</button>';
const li = document.createElement('li');
li.textContent = delBuzon;
document.querySelector('#avisos').append(li);
```

#### Al superarla
El aviso queda colgado con todos sus símbolos a la vista, y el botón falso no aparece. El troll del buzón se va, gruñendo. —Lo que escribe otro, siempre como texto —anota Lucio en su libreta.

#### Imagen
- Un buzón de madera de feria con un troll chiquito y gruñón (sin armas) asomando por la ranura con cara de travieso.
- Lucio y Nima leen un papel lleno de garabatos de símbolos; Gheco señala al troll.

## R02-N03 · Eventos: nada pasa hasta que algo pasa

```meta
tipo: tema
padre: R02-N02
precio: 10
criatura: skeleton
temas: js.eventos
```

### Crónica

Lucio lleva a Nima hasta el centro de la Avenida, donde hay un **carrusel de títeres** detenido: caballitos, payasos y una bailarina, todos quietos.

—Estos no se mueven con un programa que corre de arriba abajo —dice {mentor}—. Se mueven **cuando** alguien hace algo: cuando tocan la manija, cuando pasan por al lado, cuando aplauden. A eso le decimos **eventos**. Es la lengua de la Feria.

### Objetivos

- Escuchar eventos con `addEventListener`.
- Usar los eventos más comunes: `click`, `dblclick`, `mouseover`, `mouseout`.
- Leer el objeto del evento: `event.target`.
- Entender que el código del evento corre **después**, cuando pasa.
- Dejar de escuchar con `removeEventListener` y la opción `{ once: true }`.

### Antes de empezar

- R02-N02: crear y cambiar elementos.

### Explicación

#### Escuchar
```javascript
boton.addEventListener('click', () => {
  console.log('¡Me tocaron!');
});
```
La función queda **esperando**: no corre ahora, corre cada vez que alguien hace click. El programa sigue con lo que viene abajo.

#### Los eventos más comunes
| Evento | Cuándo pasa |
|---|---|
| `click` | un click (o un toque en el celular) |
| `dblclick` | doble click |
| `mouseover` / `mouseout` | el mouse entra / sale |
| `keydown` / `keyup` | se aprieta / suelta una tecla |
| `input` | cambia lo que hay escrito en un campo |
| `submit` | se envía un formulario |

#### El objeto del evento
La función recibe un **evento** con los datos de lo que pasó:
```javascript
boton.addEventListener('click', (evento) => {
  console.log(evento.type);          // 'click'
  console.log(evento.target.id);     // el elemento que se tocó
});
```

#### Una sola vez, o dejar de escuchar
```javascript
boton.addEventListener('click', premio, { once: true });   // solo la primera vez
boton.removeEventListener('click', premio);                 // deja de escuchar (hace falta la misma función)
```

> **En la plataforma.** Al ejecutar, la caja hace los eventos de la consigna (por ejemplo, *click #palanca*) y comprueba cómo quedó la página. Después la página sigue viva: probá tocarla vos.

### Código de ejemplo

```javascript
document.body.innerHTML = '<button id="manija">Girar</button><p id="vueltas">0</p>';
const manija = document.querySelector('#manija');
const vueltas = document.querySelector('#vueltas');
let cuenta = 0;

manija.addEventListener('click', (evento) => {
  cuenta++;
  vueltas.textContent = cuenta;
  console.log(`Vuelta ${cuenta} (evento ${evento.type} en #${evento.target.id})`);
});

console.log('El carrusel espera...');
manija.click();
manija.click();
console.log('Vueltas:', vueltas.textContent);
```

### Salida esperada

```
El carrusel espera...
Vuelta 1 (evento click en #manija)
Vuelta 2 (evento click en #manija)
Vueltas: 2
```

### ¿Para qué sirve?

Es la diferencia entre una página que se lee y una que se usa. Todo lo que reacciona a una persona (botones, menús, juegos, formularios) se escribe con eventos.

### Errores habituales

**Ogro: llamar la función en vez de pasarla.** `boton.addEventListener('click', prender())` ejecuta `prender` **ahora** y le pasa el resultado (`undefined`). Va sin paréntesis: `addEventListener('click', prender)`.

**Esqueleto: el nombre del evento mal escrito.** `'onclick'` o `'Click'` no existen para `addEventListener`: es `'click'`. No da error: simplemente nunca pasa.

**Orco: escuchar algo que todavía no está.** Si el elemento se crea después, el `querySelector` da `null`.

### Micro-misión R02-N03-P1 · La manija del carrusel

```meta
lugar: El carrusel de títeres
personajes: Nima, Gheco, Lucio
carta: addEventListener | el.addEventListener('click', () => { … }) · corre CUANDO hacen click
recompensa: xp 10, oro 10
```

#### Escena
El carrusel de títeres tiene una manija de bronce. Lucio dice que, cuando la tocaban, la bailarina se ponía a girar.

#### Gheco sugiere
Escuchá el `click` de `#manija` y, adentro, agregale la clase `girando` a `#bailarina`.

#### Desafío
Hacé que la bailarina gire al tocar la manija.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; text-align: center; padding: 24px; }
  #bailarina { font-size: 48px; display: inline-block; }
  #bailarina.girando { animation: giro 1s linear infinite; }
  @keyframes giro { to { transform: rotate(360deg); } }
  button { font-size: 18px; padding: 6px 16px; }
</style>
<p id="bailarina">💃</p>
<button id="manija">Manija</button>
```

#### Eventos
```
click #manija
```

#### Estado
```
#bailarina @class
```

#### Código inicial
```javascript
const manija = document.querySelector('#manija');
const bailarina = document.querySelector('#bailarina');

```

#### Salida esperada
```
── Estado ──
#bailarina @class: girando
```

#### Solución
```javascript
const manija = document.querySelector('#manija');
const bailarina = document.querySelector('#bailarina');

manija.addEventListener('click', () => {
  bailarina.classList.add('girando');
});
```

#### Al superarla
La bailarina de madera se pone a girar en puntas de pie, despacio primero, más rápido después. Lucio aplaude con los ojos húmedos.

#### Imagen
- Un carrusel de títeres de madera pintada en el centro de la avenida, con una bailarina girando y una manija de bronce.
- Nima toca la manija; Lucio aplaude; Gheco gira sobre sí mismo imitando a la bailarina.

### Micro-misión R02-N03-P2 · Contar las vueltas

```meta
lugar: El carrusel de títeres
personajes: Nima, Gheco, Lucio
carta: Estado y eventos | una variable afuera guarda la cuenta · el evento la cambia y la muestra
recompensa: xp 10, oro 10
```

#### Escena
Lucio quiere saber cuántas veces tocan la manija en toda la noche.

#### Gheco sugiere
Una variable `let vueltas = 0` **afuera** del evento. Adentro, sumale uno y mostrala en `#cuenta`.

#### Desafío
Cada click en la manija suma una vuelta y la muestra.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; text-align: center; padding: 24px; }
  #cuenta { font-size: 40px; color: #ffd400; }
</style>
<p>Vueltas: <span id="cuenta">0</span></p>
<button id="manija">Manija</button>
```

#### Eventos
```
click #manija
click #manija
click #manija
```

#### Estado
```
#cuenta
```

#### Código inicial
```javascript
const manija = document.querySelector('#manija');
const cuenta = document.querySelector('#cuenta');

```

#### Salida esperada
```
── Estado ──
#cuenta: 3
```

#### Solución
```javascript
const manija = document.querySelector('#manija');
const cuenta = document.querySelector('#cuenta');
let vueltas = 0;

manija.addEventListener('click', () => {
  vueltas++;
  cuenta.textContent = vueltas;
});
```

#### Al superarla
Tres vueltas, tres números que suben. Lucio dice que a la madrugada van a ser mil.

#### Imagen
- Un contador de feria de números de madera giratorios encima del carrusel de títeres.
- Lucio mira el contador con un reloj de bolsillo en la mano; Nima gira la manija.

### Micro-misión R02-N03-P3 · ¿Quién tocó?

```meta
lugar: El carrusel de títeres
personajes: Nima, Gheco
carta: event.target | (evento) => { evento.target } · el elemento donde pasó · evento.target.id, .textContent
recompensa: xp 10, oro 10
```

#### Escena
El carrusel tiene tres títeres y una sola función para todos: cuando tocan uno, tiene que decir cuál fue.

#### Gheco sugiere
La función recibe el `evento`. `evento.target.textContent` es el texto del botón que tocaron. Mostralo en `#ultimo`.

#### Desafío
Escuchá el click de cada títere y mostrá en `#ultimo` el nombre del que tocaron.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; text-align: center; padding: 24px; }
  button { font-size: 18px; margin: 4px; padding: 6px 14px; }
</style>
<button class="titere">Payaso</button><button class="titere">Caballito</button><button class="titere">Bailarina</button>
<p>Último: <strong id="ultimo">nadie</strong></p>
```

#### Eventos
```
click .titere:nth-child(2)
click .titere:nth-child(1)
```

#### Estado
```
#ultimo
```

#### Código inicial
```javascript
const ultimo = document.querySelector('#ultimo');

for (const titere of document.querySelectorAll('.titere')) {
  titere.addEventListener('click', (evento) => {

  });
}
```

#### Salida esperada
```
── Estado ──
! click .titere:nth-child(1): no hay ningún elemento «.titere:nth-child(1)»
#ultimo: Payaso
```

#### Solución
```javascript
const ultimo = document.querySelector('#ultimo');

for (const titere of document.querySelectorAll('.titere')) {
  titere.addEventListener('click', (evento) => {
    ultimo.textContent = evento.target.textContent;
  });
}
```

#### Al superarla
Cada títere que tocan saluda y el cartelito dice su nombre. El payaso se ofende un poco por no haber sido el último.

#### Imagen
- Tres títeres de madera colgados de hilos: un payaso, un caballito y una bailarina, con un cartelito debajo.
- Nima toca al payaso con la punta de una flecha de punta redonda; Gheco se ríe.

### Micro-misión R02-N03-P4 · El esqueleto de los paréntesis

```meta
lugar: El carrusel de títeres
personajes: Nima, Gheco, Lucio
criatura: skeleton
carta: Pasar, no llamar | addEventListener('click', prender) · sin () · con (), se ejecuta ya
recompensa: xp 10, oro 10
```

#### Escena
Lucio escribió que el farol del carrusel se prenda al tocar el botón. Pero se prende **solo**, apenas carga la página, sin que nadie toque nada. Un esqueleto se esconde en un paréntesis.

#### Gheco sugiere
`addEventListener('click', prender())` **llama** a `prender` en el momento. Pasala sin paréntesis: `addEventListener('click', prender)`.

#### Desafío
Arreglalo para que el farol se prenda **recién** al tocar el botón. (La comprobación mira cómo está antes del click y después.)

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; text-align: center; padding: 24px; }
  .farol { display: inline-block; width: 50px; height: 50px; border-radius: 50%; background: #333; }
  .farol.prendido { background: #ffd400; box-shadow: 0 0 24px #ffd400; }
</style>
<span class="farol" id="farol"></span>
<p id="estado">apagado</p>
<button id="boton">Prender</button>
```

#### Eventos
```
esperar 500
click #boton
```

#### Estado
```
#estado
```

#### Código inicial
```javascript
const farol = document.querySelector('#farol');
const estado = document.querySelector('#estado');

function prender() {
  farol.classList.add('prendido');
  estado.textContent = `prendido a los ${performance.now()} ms`;
}

document.querySelector('#boton').addEventListener('click', prender());
```

#### Salida esperada
```
── Estado ──
#estado: prendido a los 500 ms
```

#### Solución
```javascript
const farol = document.querySelector('#farol');
const estado = document.querySelector('#estado');

function prender() {
  farol.classList.add('prendido');
  estado.textContent = `prendido a los ${performance.now()} ms`;
}

document.querySelector('#boton').addEventListener('click', prender);
```

#### Al superarla
El farol se queda apagado hasta que tocan el botón, a los 500 milisegundos. —Ahora sí espera —dice Lucio.

#### Imagen
- Un esqueleto de feria chiquito y flaco (sin armas, con un moño de papel) sentado dentro de un paréntesis gigante de madera.
- Nima lo saca del paréntesis con la punta del arco; Lucio mira con la vara de farolero en la mano.

### Micro-misión R02-N03-P5 · Pasar por al lado

```meta
lugar: El carrusel de títeres
personajes: Nima, Gheco, Lucio
carta: mouseover y mouseout | el mouse entra · el mouse sale · un evento para cada cosa
recompensa: xp 15, monedas 5
```

#### Escena
Los faroles viejos de la Avenida se prendían solos cuando alguien pasaba por abajo, y se apagaban cuando se iba. Lucio quiere recuperar eso.

#### Gheco sugiere
`mouseover` agrega la clase `prendido` y `mouseout` la saca. Dos eventos, dos funciones.

#### Desafío
El farol se prende cuando el mouse pasa por encima y se apaga cuando sale. (La comprobación pasa y sale, y vuelve a pasar.)

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; text-align: center; padding: 24px; }
  .farol { display: inline-block; width: 80px; height: 80px; border-radius: 50%; background: #333; transition: background .3s; }
  .farol.prendido { background: #ffd400; box-shadow: 0 0 30px #ffd400; }
</style>
<span class="farol" id="farol"></span>
<p>Pasá el mouse por el farol</p>
```

#### Eventos
```
pasar #farol
salir #farol
pasar #farol
```

#### Estado
```
#farol @class
```

#### Código inicial
```javascript
const farol = document.querySelector('#farol');

```

#### Salida esperada
```
── Estado ──
#farol @class: farol prendido
```

#### Solución
```javascript
const farol = document.querySelector('#farol');

farol.addEventListener('mouseover', () => farol.classList.add('prendido'));
farol.addEventListener('mouseout', () => farol.classList.remove('prendido'));
```

#### Al superarla
Nima pasa la mano por debajo del farol y se prende; la saca y se apaga. Lo hace veinte veces seguidas, riéndose. Lucio, también.

#### Imagen
- Un farol de vidrio que se prende al pasar una mano por debajo, en una calle de feria nocturna.
- Nima pasa la mano enguantada debajo del farol; Lucio ríe; Gheco mira para arriba.

### Micro-misión R02-N03-P6 · El premio de una sola vez

```meta
lugar: El carrusel de títeres
personajes: Nima, Gheco, Lumina
carta: { once: true } | addEventListener('click', f, { once: true }) · escucha una sola vez y se olvida
recompensa: xp 15, monedas 5
```

#### Escena
Lumina dejó un cofre en el carrusel con un premio. El cofre da **una** ficha de luz, una sola vez. Bruno ya lo tocó diez veces para ver si da más.

#### Gheco sugiere
Con `{ once: true }` como tercer argumento, la función corre solo la primera vez.

#### Desafío
Agregá `{ once: true }` para que el cofre dé una sola ficha aunque lo toquen tres veces.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; text-align: center; padding: 24px; }
  #fichas { font-size: 40px; color: #ffd400; }
</style>
<button id="cofre">🎁 Cofre</button>
<p>Fichas de luz: <span id="fichas">0</span></p>
```

#### Eventos
```
click #cofre
click #cofre
click #cofre
```

#### Estado
```
#fichas
```

#### Código inicial
```javascript
const fichas = document.querySelector('#fichas');
let total = 0;

document.querySelector('#cofre').addEventListener('click', () => {
  total++;
  fichas.textContent = total;
});
```

#### Salida esperada
```
── Estado ──
#fichas: 1
```

#### Solución
```javascript
const fichas = document.querySelector('#fichas');
let total = 0;

document.querySelector('#cofre').addEventListener('click', () => {
  total++;
  fichas.textContent = total;
}, { once: true });
```

#### Al superarla
El cofre se abre, da su ficha y se cierra para siempre. Bruno lo sigue tocando un rato más, por las dudas. Nada.

#### Imagen
- Un cofrecito de madera con herrajes dorados abierto en el borde del carrusel, con una ficha de luz amarilla flotando arriba.
- Bruno (gorra al revés, chaleco rojo) golpea la tapa con insistencia; Lumina (luciérnaga enorme con alas de vidrio) lo mira con paciencia.

## R02-N04 · Teclado y formularios

```meta
tipo: tema
padre: R02-N03
precio: 10
criatura: goblin
temas: js.eventos, js.formularios
```

### Crónica

En la esquina de la Avenida está la **boletería** de la Feria: una ventanita donde se anota quién entra, cuántas fichas compra y con qué juego empieza. La atiende Tati, que no da abasto: la gente le grita los datos, ella los anota mal, y cuando alguien aprieta *Enter* en el formulario, la página se recarga y se pierde todo.

—Un formulario también habla con eventos —dice {mentor}—. Uno cuando escriben, otro cuando apretan una tecla y otro cuando lo envían. Y al enviarlo, el navegador recarga la página… salvo que le digas que no.

### Objetivos

- Leer lo que hay en un campo con `.value` (y saber que siempre es texto).
- Reaccionar mientras se escribe con el evento `input`.
- Reaccionar a las teclas con `keydown` y `event.key`.
- Manejar el envío con `submit` y `event.preventDefault()`.
- Validar los datos antes de usarlos y mostrar un mensaje de error.

### Antes de empezar

- R02-N03: eventos.

### Explicación

#### Lo que hay escrito
```javascript
const campo = document.querySelector('#nombre');
console.log(campo.value);           // siempre un texto, aunque sea un número
const fichas = Number(document.querySelector('#fichas').value);
```

#### Mientras escriben
```javascript
campo.addEventListener('input', () => {
  saludo.textContent = `Hola, ${campo.value}`;
});
```

#### Las teclas
```javascript
document.addEventListener('keydown', (evento) => {
  if (evento.key === 'Enter') { … }
  if (evento.key === 'ArrowUp') { … }
});
```
`evento.key` dice qué tecla: `'a'`, `'Enter'`, `'Escape'`, `'ArrowLeft'`, `' '` (la barra espaciadora).

#### El envío
```javascript
formulario.addEventListener('submit', (evento) => {
  evento.preventDefault();          // que no recargue la página
  // leer, validar, mostrar
});
```
El `submit` pasa al tocar el botón del formulario **o** al apretar Enter en un campo. Por eso conviene escuchar el `submit` del formulario y no el `click` del botón.

#### Validar
Antes de usar un dato, revisá que tenga sentido: que no esté vacío (`.trim() === ''`), que sea un número (`Number.isNaN`), que esté en un rango. Si no, mostrá un mensaje y cortá con `return`.

### Código de ejemplo

```javascript
document.body.innerHTML = `
  <form><input id="nombre"><input id="fichas"><button>Entrar</button></form>
  <p id="mensaje"></p>`;

const formulario = document.querySelector('form');
const mensaje = document.querySelector('#mensaje');

formulario.addEventListener('submit', (evento) => {
  evento.preventDefault();
  const nombre = document.querySelector('#nombre').value.trim();
  const fichas = Number(document.querySelector('#fichas').value);
  if (nombre === '' || Number.isNaN(fichas)) {
    mensaje.textContent = 'Faltan datos';
    return;
  }
  mensaje.textContent = `${nombre} entra con ${fichas} fichas`;
});

document.querySelector('#nombre').value = 'Nima';
document.querySelector('#fichas').value = '5';
formulario.requestSubmit();
console.log(mensaje.textContent);
```

### Salida esperada

```
Nima entra con 5 fichas
```

### ¿Para qué sirve?

Iniciar sesión, buscar, comprar, comentar, registrarse: todo pasa por un formulario. Validar en el navegador le avisa enseguida a la persona qué le falta (pero el servidor siempre tiene que volver a validar, como en el Puerto de Elefa).

### Errores habituales

**Goblin: sumar lo que viene de un campo.** `campo.value + 1` da `'51'`. Convertí con `Number`.

**Ogro: olvidar el `preventDefault()`.** La página se recarga y todo lo que escribiste se pierde. (En la caja, la página no se recarga, pero te avisa en el Tablero.)

**Ogro: escuchar el `click` del botón.** Si la persona aprieta Enter, el `click` no pasa: escuchá el `submit`.

**Esqueleto: `evento.key` con otra mayúscula.** Es `'Enter'`, no `'enter'`; y las flechas son `'ArrowUp'`, `'ArrowDown'`…

### Micro-misión R02-N04-P1 · El saludo de la boletería

```meta
lugar: La boletería
personajes: Nima, Gheco, Tati
carta: input y value | campo.value es lo que hay escrito · el evento 'input' pasa con cada letra
recompensa: xp 10, oro 10
```

#### Escena
Tati quiere que, mientras alguien escribe su nombre, el cartelito de la boletería lo salude.

#### Gheco sugiere
Escuchá el `input` del campo y, adentro, poné en `#saludo` el texto `` `¡Hola, ${campo.value}!` ``.

#### Desafío
El saludo se actualiza mientras se escribe.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  input { font-size: 18px; padding: 4px 8px; }
  #saludo { font-size: 24px; color: #ffd400; }
</style>
<label>Tu nombre: <input id="nombre"></label>
<p id="saludo">¡Hola!</p>
```

#### Eventos
```
escribir #nombre Nima
```

#### Estado
```
#saludo
```

#### Código inicial
```javascript
const campo = document.querySelector('#nombre');
const saludo = document.querySelector('#saludo');

```

#### Salida esperada
```
── Estado ──
#saludo: ¡Hola, Nima!
```

#### Solución
```javascript
const campo = document.querySelector('#nombre');
const saludo = document.querySelector('#saludo');

campo.addEventListener('input', () => {
  saludo.textContent = `¡Hola, ${campo.value}!`;
});
```

#### Al superarla
—¡Hola, Nima! —dice el cartelito, letra por letra. Tati se ríe: ya no tiene que gritarle a nadie.

#### Imagen
- La ventanita de una boletería de feria de madera, con un cartelito luminoso arriba y una fila de gente.
- Tati (chica de 11, dos colitas, delantal amarillo) adentro de la boletería; Nima escribe en una tablita.

### Micro-misión R02-N04-P2 · Que no se recargue

```meta
lugar: La boletería
personajes: Nima, Gheco, Tati
carta: submit | form.addEventListener('submit', (e) => { e.preventDefault(); … }) · también pasa con Enter
recompensa: xp 10, oro 10
```

#### Escena
Cuando alguien aprieta *Anotar*, la boletería se «recarga» y se borra todo. Tati está desesperada.

#### Gheco sugiere
Escuchá el `submit` del formulario y empezá con `evento.preventDefault()`. Después, agregá el nombre a la lista `#entraron`.

#### Desafío
Cada envío agrega un `li` con el nombre, sin recargar.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  input, button { font-size: 18px; padding: 4px 8px; }
</style>
<form id="boleteria"><input id="nombre"><button>Anotar</button></form>
<ul id="entraron"></ul>
```

#### Eventos
```
escribir #nombre Nima
enviar #boleteria
escribir #nombre Bruno
enviar #boleteria
```

#### Estado
```
#entraron li
```

#### Código inicial
```javascript
const formulario = document.querySelector('#boleteria');
const campo = document.querySelector('#nombre');
const lista = document.querySelector('#entraron');

```

#### Salida esperada
```
── Estado ──
#entraron li: Nima
#entraron li: Bruno
```

#### Solución
```javascript
const formulario = document.querySelector('#boleteria');
const campo = document.querySelector('#nombre');
const lista = document.querySelector('#entraron');

formulario.addEventListener('submit', (evento) => {
  evento.preventDefault();
  const li = document.createElement('li');
  li.textContent = campo.value;
  lista.append(li);
});
```

#### Al superarla
Los nombres se van anotando uno debajo del otro y nadie se pierde. Tati le pone un sello a cada uno.

#### Imagen
- Una libreta de boletería abierta con renglones anotados (sin texto legible) y un sello de goma.
- Tati sella la libreta; atrás, una fila de gente de feria con entradas en la mano.

### Micro-misión R02-N04-P3 · Las fichas que se suman

```meta
lugar: La boletería
personajes: Nima, Gheco, Tati
criatura: goblin
carta: value es texto | Number(campo.value) antes de sumar · el Goblin vuelve con '5' + 3
recompensa: xp 10, oro 10
```

#### Escena
Nima compra 5 fichas y después 3 más. La boletería dice que tiene **53**. El Goblin de la Coerción espía desde la fila.

#### Gheco sugiere
Lo que viene de un campo es texto. Convertilo con `Number` antes de sumarlo al total.

#### Desafío
Arreglá la suma para que el total dé 8.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  input, button { font-size: 18px; padding: 4px 8px; }
  #total { color: #ffd400; font-size: 28px; }
</style>
<form id="compra"><input id="cantidad"><button>Comprar</button></form>
<p>Total: <span id="total">0</span> fichas</p>
```

#### Eventos
```
escribir #cantidad 5
enviar #compra
escribir #cantidad 3
enviar #compra
```

#### Estado
```
#total
```

#### Código inicial
```javascript
let total = 0;
const campo = document.querySelector('#cantidad');

document.querySelector('#compra').addEventListener('submit', (evento) => {
  evento.preventDefault();
  total = total + campo.value;
  document.querySelector('#total').textContent = total;
});
```

#### Salida esperada
```
── Estado ──
#total: 8
```

#### Solución
```javascript
let total = 0;
const campo = document.querySelector('#cantidad');

document.querySelector('#compra').addEventListener('submit', (evento) => {
  evento.preventDefault();
  total = total + Number(campo.value);
  document.querySelector('#total').textContent = total;
});
```

#### Al superarla
—Ocho —lee Tati—. Ni cincuenta y tres, ni cero tres. Ocho. —El Goblin se va de la fila, aburrido.

#### Imagen
- Un mostrador de boletería con una pila de ocho fichas de bronce y un cartel con un número tachado.
- El Goblin de la Coerción (orejas puntiagudas, chaleco a rayas, galera) se aleja de la fila con las manos en los bolsillos; Nima cuenta sus fichas.

### Micro-misión R02-N04-P4 · El formulario que avisa

```meta
lugar: La boletería
personajes: Nima, Gheco, Tati
carta: Validar | .trim() === '' → vacío · Number.isNaN → no es número · mostrá el error y cortá con return
recompensa: xp 10, oro 10
```

#### Escena
Algunos llegan sin decir el nombre, otros ponen «muchas» en las fichas. Tati quiere que la boletería les avise en vez de anotar cualquier cosa.

#### Gheco sugiere
En el `submit`, revisá primero: si el nombre está vacío, mostrá `Falta el nombre`; si las fichas no son un número, `Las fichas tienen que ser un número`. Si está todo bien, `Entra ${nombre} con ${fichas} fichas`.

#### Desafío
Completá la validación. La comprobación prueba un envío vacío, uno con letras y uno bien.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  input, button { font-size: 18px; padding: 4px 8px; margin: 2px; }
  #mensaje { font-size: 20px; }
</style>
<form id="entrada"><input id="nombre" placeholder="nombre"><input id="fichas" placeholder="fichas"><button>Entrar</button></form>
<p id="mensaje"></p>
<ul id="registro"></ul>
```

#### Eventos
```
enviar #entrada
escribir #nombre Bruno
escribir #fichas muchas
enviar #entrada
escribir #fichas 4
enviar #entrada
```

#### Estado
```
#registro li
```

#### Código inicial
```javascript
const mensaje = document.querySelector('#mensaje');
const registro = document.querySelector('#registro');

function avisar(texto) {
  mensaje.textContent = texto;
  const li = document.createElement('li');
  li.textContent = texto;
  registro.append(li);
}

document.querySelector('#entrada').addEventListener('submit', (evento) => {
  evento.preventDefault();
  const nombre = document.querySelector('#nombre').value.trim();
  const fichas = Number(document.querySelector('#fichas').value);
  // validá y avisá con avisar(…)

});
```

#### Salida esperada
```
── Estado ──
#registro li: Falta el nombre
#registro li: Las fichas tienen que ser un número
#registro li: Entra Bruno con 4 fichas
```

#### Solución
```javascript
const mensaje = document.querySelector('#mensaje');
const registro = document.querySelector('#registro');

function avisar(texto) {
  mensaje.textContent = texto;
  const li = document.createElement('li');
  li.textContent = texto;
  registro.append(li);
}

document.querySelector('#entrada').addEventListener('submit', (evento) => {
  evento.preventDefault();
  const nombre = document.querySelector('#nombre').value.trim();
  const fichas = Number(document.querySelector('#fichas').value);
  if (nombre === '') {
    avisar('Falta el nombre');
    return;
  }
  if (Number.isNaN(fichas)) {
    avisar('Las fichas tienen que ser un número');
    return;
  }
  avisar(`Entra ${nombre} con ${fichas} fichas`);
});
```

#### Al superarla
La fila avanza rápido: cada uno sabe enseguida qué le falta. Tati por fin tiene tiempo de comerse un pan con miel.

#### Imagen
- Una boletería de feria con un cartelito luminoso que muestra un ícono de advertencia amarillo (sin texto).
- Tati come un pan con miel adentro; Bruno, en la ventanita, completa una tablita con cara de culpa.

### Micro-misión R02-N04-P5 · Las flechas del teclado

```meta
lugar: La boletería
personajes: Nima, Gheco, Tati
carta: keydown | document.addEventListener('keydown', (e) => …) · e.key es 'ArrowUp', 'Enter', 'a'…
recompensa: xp 15, monedas 5
```

#### Escena
Al lado de la boletería hay una mira de tiro que se mueve con las flechas del teclado. Tati quiere que la flecha derecha la mueva 10 píxeles y la izquierda la devuelva.

#### Gheco sugiere
Escuchá `keydown` en `document`. Si `evento.key === 'ArrowRight'`, sumá 10 a `x`; si es `'ArrowLeft'`, restá 10. Después mostralo en `#posicion`.

#### Desafío
La posición cambia con las flechas. (La comprobación aprieta tres veces la derecha y una la izquierda.)

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  #pista { position: relative; height: 40px; background: #1a2238; border-radius: 6px; }
  #mira { position: absolute; top: 8px; width: 24px; height: 24px; border-radius: 50%; border: 3px solid #ffd400; }
</style>
<div id="pista"><div id="mira"></div></div>
<p>x = <span id="posicion">0</span></p>
```

#### Eventos
```
tecla ArrowRight
tecla ArrowRight
tecla ArrowRight
tecla ArrowLeft
```

#### Estado
```
#posicion
estilo #mira { left }
```

#### Código inicial
```javascript
const mira = document.querySelector('#mira');
const posicion = document.querySelector('#posicion');
let x = 0;

function dibujar() {
  mira.style.left = `${x}px`;
  posicion.textContent = x;
}
dibujar();

```

#### Salida esperada
```
── Estado ──
#posicion: 20
estilo #mira { left }: 20px
```

#### Solución
```javascript
const mira = document.querySelector('#mira');
const posicion = document.querySelector('#posicion');
let x = 0;

function dibujar() {
  mira.style.left = `${x}px`;
  posicion.textContent = x;
}
dibujar();

document.addEventListener('keydown', (evento) => {
  if (evento.key === 'ArrowRight') x += 10;
  if (evento.key === 'ArrowLeft') x -= 10;
  dibujar();
});
```

#### Al superarla
La mira se desliza por la pista de un lado a otro. Nima la prueba y ya no puede parar: es como apuntar, pero con los dedos.

#### Imagen
- Una mira redonda amarilla deslizándose por un riel de madera al lado de una boletería de feria.
- Nima apoya los dedos en un teclado viejo de bronce con flechas; Tati mira por encima de su hombro.

### Micro-misión R02-N04-P6 · Enter para disparar

```meta
lugar: La boletería
personajes: Nima, Gheco, Tati, Lumina
carta: Teclas y estado | una variable guarda si está lista · Enter dispara · Escape cancela
recompensa: xp 15, monedas 5
```

#### Escena
Para el tiro con teclado, Lumina inventó una regla: la barra espaciadora **tensa** el arco, Enter **dispara** (solo si está tenso) y Escape lo **destensa**.

#### Gheco sugiere
Guardá `let tenso = false;`. En el `keydown`: si es `' '`, `tenso = true`; si es `'Escape'`, `tenso = false`; si es `'Enter'` y `tenso`, sumá un disparo y destensá.

#### Desafío
Contá los disparos válidos en `#disparos`. (La comprobación aprieta: Enter, espacio, Enter, espacio, Escape, Enter, espacio, Enter.)

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; text-align: center; }
  #disparos { font-size: 40px; color: #ffd400; }
</style>
<p>Espacio: tensar · Enter: disparar · Escape: soltar</p>
<p>Disparos: <span id="disparos">0</span></p>
```

#### Eventos
```
tecla Enter
tecla espacio
tecla Enter
tecla espacio
tecla Escape
tecla Enter
tecla espacio
tecla Enter
```

#### Estado
```
#disparos
```

#### Código inicial
```javascript
const disparos = document.querySelector('#disparos');
let tenso = false;
let total = 0;

document.addEventListener('keydown', (evento) => {

});
```

#### Salida esperada
```
── Estado ──
#disparos: 2
```

#### Solución
```javascript
const disparos = document.querySelector('#disparos');
let tenso = false;
let total = 0;

document.addEventListener('keydown', (evento) => {
  if (evento.key === ' ') tenso = true;
  if (evento.key === 'Escape') tenso = false;
  if (evento.key === 'Enter' && tenso) {
    total++;
    tenso = false;
    disparos.textContent = total;
  }
});
```

#### Al superarla
Dos disparos válidos, y los dos al centro. Lumina asiente: —Tensar, esperar, soltar. En ese orden.

#### Imagen
- Un blanco de paja con dos flechas clavadas en el centro, en una galería de tiro de feria.
- Nima con el arco tenso, concentrada; Lumina (luciérnaga enorme, alas de vidrio) mira desde arriba.

## R02-N05 · Delegación y data-*

```meta
tipo: tema
padre: R02-N04
precio: 10
criatura: ogre
temas: js.eventos, js.dom
```

### Crónica

La **galería de los cien faroles** es un pasillo con faroles de colores colgados del techo, cada uno con su número. Lucio quiere que cada uno se prenda al tocarlo, pero escribir cien `addEventListener`, uno por farol, le parece una locura. Y encima, cada noche cuelgan faroles nuevos.

—No hace falta escuchar a cada uno —dice {mentor}—. Los eventos **suben**: si tocás un farol, el toque llega también al techo del que cuelga. Escuchá el techo, y preguntá qué farol fue.

### Objetivos

- Entender que los eventos «burbujean»: suben del elemento a sus padres.
- Escuchar una sola vez en el contenedor (**delegación**) y usar `event.target` y `closest`.
- Guardar datos en el HTML con atributos `data-*` y leerlos con `dataset`.
- Que la delegación funcione también con los elementos que se agregan después.

### Antes de empezar

- R02-N03 y R02-N04: eventos.

### Explicación

#### Los eventos suben
Un click en un `<li>` es también un click en su `<ul>`, en el `<body>` y en el `document`. Por eso alcanza con escuchar **arriba**:
```javascript
galeria.addEventListener('click', (evento) => {
  const farol = evento.target.closest('.farol');
  if (!farol) return;              // tocaron otra cosa del contenedor
  farol.classList.toggle('prendido');
});
```
`closest('.farol')` sube desde lo que tocaron hasta encontrar un `.farol` (por si tocaron algo de adentro, como un ícono).

#### Datos en el HTML: data-*
```html
<li class="farol" data-color="rojo" data-precio="3">Farol 1</li>
```
```javascript
farol.dataset.color;    // 'rojo'
farol.dataset.precio;   // '3' (texto, como todo lo del HTML)
farol.dataset.vendido = 'si';   // crea data-vendido="si"
```

#### Lo nuevo también funciona
Como el que escucha es el contenedor, los faroles que agregues después con `append` reaccionan igual, sin escribir nada más.

#### Frenar la subida
`evento.stopPropagation()` corta el viaje para arriba. Se usa poco: casi siempre la delegación es lo que querés.

### Código de ejemplo

```javascript
document.body.innerHTML = `
  <ul id="galeria">
    <li class="farol" data-color="rojo">1</li>
    <li class="farol" data-color="verde">2</li>
  </ul>`;
const galeria = document.querySelector('#galeria');

galeria.addEventListener('click', (evento) => {
  const farol = evento.target.closest('.farol');
  if (!farol) return;
  farol.classList.toggle('prendido');
  console.log(`Farol ${farol.textContent} (${farol.dataset.color}):`, farol.classList.contains('prendido') ? 'prendido' : 'apagado');
});

const nuevo = document.createElement('li');
nuevo.className = 'farol';
nuevo.dataset.color = 'azul';
nuevo.textContent = '3';
galeria.append(nuevo);

document.querySelectorAll('.farol')[1].click();
nuevo.click();
nuevo.click();
```

### Salida esperada

```
Farol 2 (verde): prendido
Farol 3 (azul): prendido
Farol 3 (azul): apagado
```

### ¿Para qué sirve?

Listas largas, tablas, menús, tableros de juego: un solo evento en el contenedor reemplaza cientos. Es más rápido, más corto y funciona con lo que se agrega después (los mensajes nuevos de un chat, los productos que cargan al bajar).

### Errores habituales

**Ogro: usar `evento.target` sin `closest`.** Si el farol tiene un ícono adentro y tocan el ícono, `target` es el ícono, no el farol.

**Orco: no cortar cuando tocaron otra cosa.** Sin el `if (!farol) return;`, un click en el espacio entre faroles da `null` y explota.

**Goblin: `dataset` es texto.** `farol.dataset.precio + 1` da `'31'`. Convertí con `Number`.

### Micro-misión R02-N05-P1 · Un solo oído

```meta
lugar: La galería de los cien faroles
personajes: Nima, Gheco, Lucio
carta: Delegación | contenedor.addEventListener('click', (e) => { const x = e.target.closest('.farol'); … })
recompensa: xp 10, oro 10
```

#### Escena
Lucio cuelga los faroles de la galería en un solo riel. Nima le propone escuchar el riel, no cada farol.

#### Gheco sugiere
Escuchá el `click` de `#galeria`. Adentro, `evento.target.closest('.farol')` te da el farol tocado; si es `null`, `return`.

#### Desafío
Cada farol tocado alterna la clase `prendido`. (La comprobación toca el 1, el 3 y otra vez el 1.)

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  #galeria { display: flex; gap: 10px; list-style: none; padding: 0; }
  .farol { width: 50px; height: 50px; border-radius: 50%; background: #333; display: grid; place-items: center; cursor: pointer; }
  .farol.prendido { background: #ffd400; color: #0b1020; }
</style>
<ul id="galeria">
  <li class="farol" id="f1">1</li><li class="farol" id="f2">2</li><li class="farol" id="f3">3</li><li class="farol" id="f4">4</li>
</ul>
```

#### Eventos
```
click #f1
click #f3
click #f1
```

#### Estado
```
.farol.prendido
```

#### Código inicial
```javascript
const galeria = document.querySelector('#galeria');

```

#### Salida esperada
```
── Estado ──
.farol.prendido: 3
```

#### Solución
```javascript
const galeria = document.querySelector('#galeria');

galeria.addEventListener('click', (evento) => {
  const farol = evento.target.closest('.farol');
  if (!farol) return;
  farol.classList.toggle('prendido');
});
```

#### Al superarla
Un solo hilo de luz recorre el riel, y cada farol que tocan responde. Lucio se rasca la cabeza: —Y yo que iba a atar cien hilos.

#### Imagen
- Un pasillo de feria con un riel de bronce en el techo del que cuelgan faroles de colores numerados, algunos prendidos.
- Lucio mira el riel con la boca abierta; Nima toca un farol con la punta del arco.

### Micro-misión R02-N05-P2 · Los colores escondidos

```meta
lugar: La galería de los cien faroles
personajes: Nima, Gheco, Lucio
carta: dataset | data-color="rojo" en el HTML · el.dataset.color en JS · siempre texto
recompensa: xp 10, oro 10
```

#### Escena
Cada farol tiene escondido su color en un atributo `data-color`. Lucio quiere que, al tocarlo, el cartel diga de qué color es.

#### Gheco sugiere
Con delegación, encontrá el farol y leé `farol.dataset.color`. Mostralo en `#cartel`.

#### Desafío
El cartel muestra `Farol rojo`, `Farol verde`, etc., según el que tocaron.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  #galeria { display: flex; gap: 10px; list-style: none; padding: 0; }
  .farol { width: 50px; height: 50px; border-radius: 50%; background: #333; cursor: pointer; }
</style>
<ul id="galeria">
  <li class="farol" id="f1" data-color="rojo"></li><li class="farol" id="f2" data-color="verde"></li><li class="farol" id="f3" data-color="violeta"></li>
</ul>
<p id="cartel">Tocá un farol</p>
```

#### Eventos
```
click #f3
```

#### Estado
```
#cartel
```

#### Código inicial
```javascript
const galeria = document.querySelector('#galeria');
const cartel = document.querySelector('#cartel');

```

#### Salida esperada
```
── Estado ──
#cartel: Farol violeta
```

#### Solución
```javascript
const galeria = document.querySelector('#galeria');
const cartel = document.querySelector('#cartel');

galeria.addEventListener('click', (evento) => {
  const farol = evento.target.closest('.farol');
  if (!farol) return;
  cartel.textContent = `Farol ${farol.dataset.color}`;
});
```

#### Al superarla
—Violeta —lee Lucio—. Ese lo pintó el Vidriero. Decía que era el color de las cosas que todavía no pasaron.

#### Imagen
- Primer plano de un farol de vidrio violeta con dibujos finos de estrellas, colgado en la galería.
- Lucio lo mira con nostalgia; Nima lee el cartel.

### Micro-misión R02-N05-P3 · Los que llegan después

```meta
lugar: La galería de los cien faroles
personajes: Nima, Gheco, Lucio
carta: Lo nuevo funciona | con delegación, lo que agregás con append ya reacciona · sin tocar el evento
recompensa: xp 10, oro 10
```

#### Escena
Esta noche llegaron faroles nuevos. Lucio los cuelga con un botón *Colgar farol*. Con el código viejo (un evento por farol), los nuevos no reaccionaban.

#### Gheco sugiere
Cambiá los eventos de cada farol por uno solo en `#galeria`. Así los nuevos también se prenden.

#### Desafío
Que los faroles agregados con el botón también se prendan al tocarlos.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  #galeria { display: flex; gap: 10px; list-style: none; padding: 0; flex-wrap: wrap; }
  .farol { width: 40px; height: 40px; border-radius: 50%; background: #333; cursor: pointer; }
  .farol.prendido { background: #ffd400; }
</style>
<button id="colgar">Colgar farol</button>
<ul id="galeria"><li class="farol"></li></ul>
```

#### Eventos
```
click #colgar
click #colgar
click #galeria li:nth-child(3)
click #galeria li:nth-child(1)
```

#### Estado
```
.farol #
.farol.prendido #
```

#### Código inicial
```javascript
const galeria = document.querySelector('#galeria');

for (const farol of document.querySelectorAll('.farol')) {
  farol.addEventListener('click', () => farol.classList.toggle('prendido'));
}

document.querySelector('#colgar').addEventListener('click', () => {
  const farol = document.createElement('li');
  farol.className = 'farol';
  galeria.append(farol);
});
```

#### Salida esperada
```
── Estado ──
.farol #: 3
.farol.prendido #: 2
```

#### Solución
```javascript
const galeria = document.querySelector('#galeria');

galeria.addEventListener('click', (evento) => {
  const farol = evento.target.closest('.farol');
  if (farol) farol.classList.toggle('prendido');
});

document.querySelector('#colgar').addEventListener('click', () => {
  const farol = document.createElement('li');
  farol.className = 'farol';
  galeria.append(farol);
});
```

#### Al superarla
El farol recién colgado se prende al primer toque. Lucio cuelga diez más, nada más que para probarlo.

#### Imagen
- Lucio subido a su escalera colgando un farol nuevo en el riel de bronce de la galería, con varios faroles prendidos.
- Nima toca el farol nuevo desde abajo y se prende; Gheco aplaude.

### Micro-misión R02-N05-P4 · El ogro del ícono

```meta
lugar: La galería de los cien faroles
personajes: Nima, Gheco
criatura: ogre
carta: closest | e.target puede ser lo de adentro (un ícono) · e.target.closest('.farol') sube hasta el farol
recompensa: xp 10, oro 10
```

#### Escena
Los faroles de lujo tienen una estrellita adentro. Cuando tocan la estrellita, en vez de prenderse el farol, se «prende» la estrellita. Un ogro tocó el código.

#### Gheco sugiere
`evento.target` es lo que tocaron (la estrellita). Usá `evento.target.closest('.farol')` para subir hasta el farol.

#### Desafío
Arreglalo para que, aunque toquen la estrellita, se prenda el farol.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  #galeria { display: flex; gap: 10px; list-style: none; padding: 0; }
  .farol { width: 50px; height: 50px; border-radius: 50%; background: #333; display: grid; place-items: center; }
  .prendido { background: #ffd400; }
</style>
<ul id="galeria">
  <li class="farol" id="lujo"><span class="estrella">★</span></li><li class="farol"><span class="estrella">★</span></li>
</ul>
```

#### Eventos
```
click #lujo .estrella
```

#### Estado
```
#lujo @class
.estrella @class
```

#### Código inicial
```javascript
document.querySelector('#galeria').addEventListener('click', (evento) => {
  evento.target.classList.toggle('prendido');
});
```

#### Salida esperada
```
── Estado ──
#lujo @class: farol prendido
.estrella @class: estrella
.estrella @class: estrella
```

#### Solución
```javascript
document.querySelector('#galeria').addEventListener('click', (evento) => {
  const farol = evento.target.closest('.farol');
  if (farol) farol.classList.toggle('prendido');
});
```

#### Al superarla
El farol de lujo se prende entero, con la estrellita adentro brillando. El ogro se va a buscar otro código para romper.

#### Imagen
- Un farol de vidrio con una estrella dorada adentro, prendido, colgado en la galería de feria.
- Un ogro de feria torpe (sin armas, delantal de rayas) se aleja rascándose la cabeza; Nima sonríe.

### Micro-misión R02-N05-P5 · La cuenta de la galería

```meta
lugar: La galería de los cien faroles
personajes: Nima, Gheco, Lucio
carta: dataset y cuentas | Number(farol.dataset.precio) · sumá al prenderlo y restá al apagarlo
recompensa: xp 15, monedas 5
```

#### Escena
Cada farol gasta aceite: el precio por noche está en `data-precio`. Lucio quiere saber cuánto gasta la galería con los faroles que están prendidos.

#### Gheco sugiere
Con delegación, alterná la clase. Después recalculá el total: recorré los `.farol.prendido` y sumá `Number(farol.dataset.precio)`.

#### Desafío
Mostrá en `#gasto` el total de los faroles prendidos. (La comprobación prende el 1 y el 3, y después apaga el 1.)

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  #galeria { display: flex; gap: 10px; list-style: none; padding: 0; }
  .farol { width: 50px; height: 50px; border-radius: 50%; background: #333; display: grid; place-items: center; }
  .farol.prendido { background: #ffd400; color: #0b1020; }
</style>
<ul id="galeria">
  <li class="farol" id="f1" data-precio="2">2</li><li class="farol" id="f2" data-precio="5">5</li><li class="farol" id="f3" data-precio="3">3</li>
</ul>
<p>Gasto: <span id="gasto">0</span> fichas por noche</p>
```

#### Eventos
```
click #f1
click #f3
click #f1
```

#### Estado
```
#gasto
```

#### Código inicial
```javascript
const galeria = document.querySelector('#galeria');
const gasto = document.querySelector('#gasto');

function recalcular() {
  // sumá el precio de los faroles prendidos

}

galeria.addEventListener('click', (evento) => {
  const farol = evento.target.closest('.farol');
  if (!farol) return;
  farol.classList.toggle('prendido');
  recalcular();
});
```

#### Salida esperada
```
── Estado ──
#gasto: 3
```

#### Solución
```javascript
const galeria = document.querySelector('#galeria');
const gasto = document.querySelector('#gasto');

function recalcular() {
  let total = 0;
  for (const farol of document.querySelectorAll('.farol.prendido')) {
    total += Number(farol.dataset.precio);
  }
  gasto.textContent = total;
}

galeria.addEventListener('click', (evento) => {
  const farol = evento.target.closest('.farol');
  if (!farol) return;
  farol.classList.toggle('prendido');
  recalcular();
});
```

#### Al superarla
Tres fichas por noche. Lucio respira: con eso le alcanza el aceite hasta fin de mes.

#### Imagen
- Una lata de aceite de farolero y una libreta de cuentas sobre un banco, bajo la galería de faroles.
- Lucio hace cuentas con un lápiz; Nima le muestra el resultado.

### Micro-misión R02-N05-P6 · El menú de los puestos

```meta
lugar: La galería de los cien faroles
personajes: Nima, Gheco, Lucio, Lumina
carta: Pestañas | botones con data-puesto · delegación · mostrar uno (hidden = false) y esconder el resto
recompensa: xp 15, monedas 5
```

#### Escena
Lumina quiere un menú en la entrada de la galería: tres botones (Tiro, Pan, Fuegos) y tres carteles, uno por puesto. Al tocar un botón, se muestra solo su cartel.

#### Gheco sugiere
Cada botón tiene `data-puesto`. Con delegación en `#menu`, leé ese dato, recorré los `.cartel` y poné `cartel.hidden = cartel.id !== puesto`.

#### Desafío
Que se vea solo el cartel del botón tocado. (La comprobación toca *Pan* y después *Fuegos*.)

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  button { font-size: 16px; padding: 6px 14px; margin: 2px; }
  .cartel { border: 2px solid #ffd400; border-radius: 8px; padding: 12px; margin-top: 10px; }
</style>
<nav id="menu">
  <button data-puesto="tiro">Tiro</button><button data-puesto="pan">Pan</button><button data-puesto="fuegos">Fuegos</button>
</nav>
<div class="cartel" id="tiro">El puesto de tiro de Bruno y Tati</div>
<div class="cartel" id="pan" hidden>El pan con miel de Doña Mirta</div>
<div class="cartel" id="fuegos" hidden>Los fuegos de Bengala</div>
```

#### Eventos
```
click [data-puesto=pan]
click [data-puesto=fuegos]
```

#### Estado
```
.cartel @hidden
```

#### Código inicial
```javascript
const menu = document.querySelector('#menu');

```

#### Salida esperada
```
── Estado ──
.cartel @hidden: sí
.cartel @hidden: sí
.cartel @hidden: no
```

#### Solución
```javascript
const menu = document.querySelector('#menu');

menu.addEventListener('click', (evento) => {
  const boton = evento.target.closest('[data-puesto]');
  if (!boton) return;
  for (const cartel of document.querySelectorAll('.cartel')) {
    cartel.hidden = cartel.id !== boton.dataset.puesto;
  }
});
```

#### Al superarla
El menú de la galería funciona con un solo evento. Lumina lo mira un rato y dice, más para sí misma: —Así funcionaba el taller del Vidriero. Un solo oído para todo.

#### Imagen
- Un menú de madera con tres botones de bronce en la entrada de una galería de faroles, y tres carteles colgados, uno solo iluminado.
- Lumina (luciérnaga enorme, alas de vidrio) mira hacia el fondo oscuro de la Avenida; Nima y Lucio prueban los botones.

## R02-N06 · JSON y localStorage: que la Feria recuerde

```meta
tipo: tema
padre: R02-N05
precio: 10
criatura: troll
temas: arch.json, js.almacenamiento
```

### Crónica

Cada amanecer, la Feria se apaga y cuando vuelve la noche **no se acuerda de nada**: los puntajes, los faroles prendidos, los nombres de la boletería, todo vuelve a cero. Bruno llora todas las noches porque pierde su récord.

—La página se olvida cuando se cierra —dice {mentor}—. Pero el navegador tiene un **cajón** donde guardar cosas: `localStorage`. Solo guarda texto, así que para guardar objetos y listas los pasamos a **JSON**.

### Objetivos

- Pasar objetos y arreglos a texto con `JSON.stringify` y volver con `JSON.parse`.
- Guardar y leer en `localStorage` (`setItem`, `getItem`, `removeItem`).
- Cargar lo guardado al empezar, con un valor por defecto si no hay nada.
- Saber la diferencia entre `localStorage` y `sessionStorage`.
- Atajar un JSON roto con `try`/`catch`.

### Antes de empezar

- R01-N06 (objetos) y R02-N04 (formularios).

### Explicación

#### JSON
JSON es una forma de escribir datos como **texto**, muy parecida a los objetos de JavaScript:
```javascript
const record = { nombre: 'Bruno', puntos: 18 };
const texto = JSON.stringify(record);   // '{"nombre":"Bruno","puntos":18}'
const deVuelta = JSON.parse(texto);     // un objeto de nuevo
```
En JSON las claves y los textos van **siempre** con comillas dobles.

#### localStorage
```javascript
localStorage.setItem('record', JSON.stringify(record));
const guardado = localStorage.getItem('record');           // texto, o null si no hay
const record = guardado ? JSON.parse(guardado) : { puntos: 0 };
localStorage.removeItem('record');
```
- Guarda **solo texto**. Un número vuelve como texto: convertí con `Number`.
- Queda guardado aunque cierres el navegador, pero **solo en esa compu y ese navegador**.
- `sessionStorage` es igual, pero se borra al cerrar la pestaña.

> **En la plataforma.** La caja usa un `localStorage` de mentira: empieza vacío (o con lo que trae la consigna, como si fuera tu segunda visita) y se borra al terminar. Miralo en el **Tablero**.

#### JSON roto
Si el texto guardado se rompió, `JSON.parse` tira un `SyntaxError`. Atajalo:
```javascript
let datos;
try {
  datos = JSON.parse(localStorage.getItem('datos'));
} catch {
  datos = null;
}
```

### Código de ejemplo

```javascript
const record = { nombre: 'Bruno', puntos: 18, premios: ['silbato'] };
const texto = JSON.stringify(record);
console.log(texto, typeof texto);

localStorage.setItem('record', texto);
localStorage.setItem('visitas', 3);
console.log(typeof localStorage.getItem('visitas'));

const leido = JSON.parse(localStorage.getItem('record'));
console.log(leido.premios[0], leido.puntos + 1);

console.log(localStorage.getItem('nada') ?? 'no hay nada guardado');

try {
  JSON.parse('{nombre: Bruno}');
} catch (error) {
  console.log('JSON roto:', error.name);
}
```

### Salida esperada

```
{"nombre":"Bruno","puntos":18,"premios":["silbato"]} string
string
silbato 19
no hay nada guardado
JSON roto: SyntaxError
```

### ¿Para qué sirve?

El tema oscuro que elegiste, el carrito que dejaste a medias, el récord de un juego, un borrador que no se pierde: todo eso vive en el navegador. Y JSON es el idioma con el que hablan los servidores y las APIs: lo vas a ver de nuevo en la Torre de las Flechas.

### Errores habituales

**Goblin: guardar un objeto sin `stringify`.** `localStorage.setItem('record', record)` guarda el texto `'[object Object]'`.

**Goblin: leer un número sin convertir.** `localStorage.getItem('visitas') + 1` da `'31'`.

**Troll: `JSON.parse(null)` cuando no hay nada guardado.** Da `null` (no explota), y la línea siguiente sí: `Cannot read properties of null`. Poné un valor por defecto.

**Slime: JSON con comillas simples o sin comillas en las claves.** `{'a': 1}` o `{a: 1}` no son JSON válido.

### Micro-misión R02-N06-P1 · El objeto hecho texto

```meta
lugar: El puesto de tiro, al amanecer
personajes: Nima, Gheco, Bruno
carta: JSON | JSON.stringify(obj) → texto · JSON.parse(texto) → objeto · en JSON, comillas dobles
recompensa: xp 10, oro 10
```

#### Escena
Bruno quiere guardar su récord en un papel para no perderlo. Pero el récord es un objeto, y en un papel solo entra texto.

#### Gheco sugiere
`JSON.stringify(record)` lo pasa a texto. `JSON.parse(texto)` lo vuelve a armar.

#### Desafío
Pasá el récord a texto, mostralo, y después volvelo a objeto para mostrar los puntos.

#### Código inicial
```javascript
const record = { nombre: 'Bruno', puntos: 18 };

const texto = ___;
console.log(texto);

const deVuelta = ___;
console.log(deVuelta.puntos);
```

#### Salida esperada
```
{"nombre":"Bruno","puntos":18}
18
```

#### Solución
```javascript
const record = { nombre: 'Bruno', puntos: 18 };

const texto = JSON.stringify(record);
console.log(texto);

const deVuelta = JSON.parse(texto);
console.log(deVuelta.puntos);
```

#### Al superarla
Bruno copia el texto raro, lleno de llaves y comillas, en un papelito, y lo dobla en cuatro. —Ahora no se me olvida más.

#### Imagen
- Un papelito doblado con llaves y comillas dibujadas (sin texto legible) sobre el mostrador del puesto de tiro, con la luz del amanecer.
- Bruno (gorra al revés, chaleco rojo) guarda el papelito en el bolsillo; Nima bosteza.

### Micro-misión R02-N06-P2 · El cajón del navegador

```meta
lugar: El puesto de tiro, al amanecer
personajes: Nima, Gheco, Bruno
carta: localStorage | setItem('clave', texto) guarda · getItem('clave') lee (o da null) · solo texto
recompensa: xp 10, oro 10
```

#### Escena
Lumina le muestra a Bruno el cajón del navegador, donde las cosas no se borran al amanecer.

#### Gheco sugiere
`localStorage.setItem('record', JSON.stringify(record))` guarda el récord. Mirá el **Tablero** después de ejecutar.

#### Desafío
Guardá el récord en `localStorage` con la clave `record`.

#### Estado
```
local record
```

#### Código inicial
```javascript
const record = { nombre: 'Bruno', puntos: 18 };

```

#### Salida esperada
```
── Estado ──
local record: {"nombre":"Bruno","puntos":18}
```

#### Solución
```javascript
const record = { nombre: 'Bruno', puntos: 18 };

localStorage.setItem('record', JSON.stringify(record));
```

#### Al superarla
El récord de Bruno queda en el cajón. Él abre y cierra el Tablero diez veces, para estar seguro.

#### Imagen
- Un cajón de madera con cerradura dorada que brilla, flotando en el aire de la feria al amanecer, con un papelito adentro.
- Bruno guarda el papelito; Lumina (luciérnaga enorme, alas de vidrio) sostiene la llave.

### Micro-misión R02-N06-P3 · La segunda noche

```meta
lugar: El puesto de tiro, de noche
personajes: Nima, Gheco, Bruno
carta: Cargar al empezar | getItem · si hay, JSON.parse · si no (null), un valor por defecto
recompensa: xp 10, oro 10
```

#### Escena
Vuelve la noche. Es la segunda visita de Bruno a la página: el récord ya está guardado de ayer. Hay que leerlo y mostrarlo.

#### Gheco sugiere
`localStorage.getItem('record')` da el texto. Si no es `null`, `JSON.parse`; si es `null`, usá `{ nombre: 'nadie', puntos: 0 }`.

#### Desafío
Mostrá en `#record` el récord guardado, como `Bruno: 18`.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; text-align: center; }
  #record { font-size: 32px; color: #ffd400; }
</style>
<p>Récord de la noche</p>
<p id="record">-</p>
```

#### Almacenamiento
```
local record = {"nombre":"Bruno","puntos":18}
```

#### Estado
```
#record
```

#### Código inicial
```javascript
const guardado = localStorage.getItem('record');
const record = ___;

document.querySelector('#record').textContent = `${record.nombre}: ${record.puntos}`;
```

#### Salida esperada
```
── Estado ──
#record: Bruno: 18
```

#### Solución
```javascript
const guardado = localStorage.getItem('record');
const record = guardado ? JSON.parse(guardado) : { nombre: 'nadie', puntos: 0 };

document.querySelector('#record').textContent = `${record.nombre}: ${record.puntos}`;
```

#### Al superarla
—¡Está! ¡Se acordó! —grita Bruno—. Dieciocho. —Y se pone a practicar para superarlo.

#### Imagen
- El cartel del puesto de tiro de noche con un récord iluminado en dorado (sin números legibles).
- Bruno salta de alegría señalando el cartel; Tati pone los ojos en blanco.

### Micro-misión R02-N06-P4 · Las visitas de la Feria

```meta
lugar: La boletería
personajes: Nima, Gheco, Tati
carta: Números guardados | Number(localStorage.getItem('x') ?? 0) · sumá · volvé a guardar
recompensa: xp 10, oro 10
```

#### Escena
Tati quiere que la boletería cuente cuántas veces abrió la página cada visitante. Es la cuarta visita de Nima.

#### Gheco sugiere
Leé `visitas`, convertí con `Number` (si no hay nada, 0), sumale 1, guardalo de nuevo y mostralo.

#### Desafío
Mostrá `Visita número 4` y dejá guardado `4`.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; text-align: center; }
</style>
<p id="visitas"></p>
```

#### Almacenamiento
```
local visitas = 3
```

#### Estado
```
#visitas
local visitas
```

#### Código inicial
```javascript
let visitas = localStorage.getItem('visitas') + 1;
localStorage.setItem('visitas', visitas);
document.querySelector('#visitas').textContent = `Visita número ${visitas}`;
```

#### Salida esperada
```
── Estado ──
#visitas: Visita número 4
local visitas: 4
```

#### Solución
```javascript
let visitas = Number(localStorage.getItem('visitas') ?? 0) + 1;
localStorage.setItem('visitas', visitas);
document.querySelector('#visitas').textContent = `Visita número ${visitas}`;
```

#### Al superarla
*Visita número 4*. Antes decía *Visita número 31*: el Goblin se había colado en el cajón.

#### Imagen
- Un contador de visitas de madera con números giratorios en la boletería (sin números legibles).
- Tati lo limpia con un trapo; Nima entra por cuarta vez, saludando.

### Micro-misión R02-N06-P5 · La lista que no se borra

```meta
lugar: El tablero de anuncios
personajes: Nima, Gheco, Lucio
carta: Guardar una lista | cargar (o []) · agregar · dibujar · JSON.stringify y setItem después de cada cambio
recompensa: xp 15, monedas 5
```

#### Escena
Lucio quiere que el tablero de anuncios se acuerde de los avisos de la noche anterior, y guarde los nuevos.

#### Gheco sugiere
Al empezar, cargá el arreglo de avisos (o `[]`). Dibujalos. En el `submit`, agregá el nuevo al arreglo, guardalo con `setItem` y volvé a dibujar.

#### Desafío
Completá `guardar` y el `submit`. La consigna ya trae dos avisos guardados de ayer; la comprobación agrega uno.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #2b1d10; color: #3b2a14; padding: 24px; }
  ul { background: #c9a36b; border: 6px solid #6b4a24; padding: 16px 32px; }
  li { background: #fff8e0; margin: 6px 0; padding: 6px; list-style: none; }
  input, button { font-size: 16px; padding: 4px 8px; }
</style>
<form id="nuevo"><input id="texto"><button>Colgar</button></form>
<ul id="avisos"></ul>
```

#### Almacenamiento
```
local avisos = ["Abre la calesita","Gana Nima"]
```

#### Eventos
```
escribir #texto Fuegos a las 22
enviar #nuevo
```

#### Estado
```
#avisos li
local avisos
```

#### Código inicial
```javascript
const lista = document.querySelector('#avisos');
const avisos = JSON.parse(localStorage.getItem('avisos') ?? '[]');

function dibujar() {
  lista.replaceChildren();
  for (const texto of avisos) {
    const li = document.createElement('li');
    li.textContent = texto;
    lista.append(li);
  }
}

function guardar() {

}

document.querySelector('#nuevo').addEventListener('submit', (evento) => {
  evento.preventDefault();

});

dibujar();
```

#### Salida esperada
```
── Estado ──
#avisos li: Abre la calesita
#avisos li: Gana Nima
#avisos li: Fuegos a las 22
local avisos: ["Abre la calesita","Gana Nima","Fuegos a las 22"]
```

#### Solución
```javascript
const lista = document.querySelector('#avisos');
const avisos = JSON.parse(localStorage.getItem('avisos') ?? '[]');

function dibujar() {
  lista.replaceChildren();
  for (const texto of avisos) {
    const li = document.createElement('li');
    li.textContent = texto;
    lista.append(li);
  }
}

function guardar() {
  localStorage.setItem('avisos', JSON.stringify(avisos));
}

document.querySelector('#nuevo').addEventListener('submit', (evento) => {
  evento.preventDefault();
  avisos.push(document.querySelector('#texto').value);
  guardar();
  dibujar();
});

dibujar();
```

#### Al superarla
Esa noche, el tablero amanece con todos los avisos de ayer en su lugar, y uno nuevo. Lucio lo toca con la punta de la vara, por las dudas.

#### Imagen
- El tablero de anuncios de la feria lleno de papeles, a la luz del amanecer y después de noche, como en dos mitades.
- Lucio toca un papel con la vara de farolero; Nima y Gheco miran satisfechos.

### Micro-misión R02-N06-P6 · El cajón roto

```meta
lugar: El puesto de tiro
personajes: Nima, Gheco, Bruno
criatura: troll
carta: try/catch con JSON | try { JSON.parse(…) } catch { valor por defecto } · un dato roto no rompe la página
recompensa: xp 15, monedas 5
```

#### Escena
Un troll metió la mano en el cajón de Bruno y le rompió el récord: ahora el texto guardado no es JSON. La página entera explota y no se ve ni el cartel.

#### Gheco sugiere
Envolvé el `JSON.parse` en `try`/`catch`. Si falla, usá el récord por defecto y avisá en la consola.

#### Desafío
Que la página no explote: si el récord está roto, mostrá `nadie: 0` y escribí `Récord roto, empiezo de cero` en la consola.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; text-align: center; }
  #record { font-size: 32px; color: #ffd400; }
</style>
<p id="record">-</p>
```

#### Almacenamiento
```
local record = {"nombre":"Bruno","puntos":1
```

#### Estado
```
#record
```

#### Código inicial
```javascript
const record = JSON.parse(localStorage.getItem('record'));

document.querySelector('#record').textContent = `${record.nombre}: ${record.puntos}`;
```

#### Salida esperada
```
Récord roto, empiezo de cero
── Estado ──
#record: nadie: 0
```

#### Solución
```javascript
let record;
try {
  record = JSON.parse(localStorage.getItem('record'));
} catch {
  console.log('Récord roto, empiezo de cero');
  record = { nombre: 'nadie', puntos: 0 };
}

document.querySelector('#record').textContent = `${record.nombre}: ${record.puntos}`;
```

#### Al superarla
El cartel vuelve a prenderse, aunque diga *nadie: 0*. —Mejor empezar de cero que no tener cartel —dice Bruno, y se pone a tirar para recuperar su récord. El troll, al ver que no rompió nada, se va.

#### Imagen
- Un cajón de madera abierto con un papel roto y rasgado adentro, y un troll chiquito y gruñón de feria (sin armas) huyendo.
- Bruno, con el arco de feria en la mano, listo para tirar de nuevo; Nima le da una palmada en el hombro.

## R02-N07 · Jefe: el Fantasma Undefined

```meta
tipo: jefe
padre: R02-N06
precio: 10
criatura: dragon
insignia: Farol del Fantasma
insignia_descripcion: Venciste al Fantasma Undefined: tu página reacciona, valida y recuerda.
usa: js.dom, js.eventos, js.almacenamiento, arch.json
```

### Crónica

Al fondo de la Avenida, donde termina la luz, vive el **Fantasma Undefined**: una sábana vieja y transparente que flota entre los faroles y les **borra el nombre**. Donde pasa, los carteles dicen *undefined*, las listas quedan vacías y los faroles se apagan solos. Dicen que antes era el ayudante del Vidriero y que se quedó esperando que volviera.

—No lo vas a espantar con flechas —dice {mentor}—. Lo espantás con una página que **no se olvida**: que sabe lo que tiene, lo muestra bien, valida lo que le dan y lo guarda.

### Objetivos

- Integrar todo lo de la rama: seleccionar, crear, eventos, formularios, delegación y `localStorage`.
- Armar una pequeña aplicación de página: cargar, dibujar, escuchar, guardar.
- No dejar que ningún `undefined` llegue a la pantalla.

### Antes de empezar

- Todos los nodos de la Avenida de los Faroles (R02-N01 a R02-N06).

### Explicación

#### La forma de toda aplicación de página
1. **Estado**: los datos (un arreglo de faroles, por ejemplo), cargados de `localStorage` o con un valor por defecto.
2. **Dibujar**: una función que borra lo que hay y lo vuelve a dibujar a partir del estado.
3. **Escuchar**: eventos (formulario, delegación) que **cambian el estado**, guardan y vuelven a dibujar.
4. **Guardar**: después de cada cambio, `localStorage.setItem(…, JSON.stringify(estado))`.

Nunca cambies la página «a mano» en un evento: cambiá el estado y llamá a `dibujar()`. Así la página siempre muestra lo que hay.

#### Cómo nace un undefined
- Leer una propiedad que no existe (`farol.nombr`).
- Una función sin `return`.
- Un índice fuera del arreglo.
- Un dato de un formulario que no se validó.

### Micro-misión R02-N07-P1 · Los nombres borrados

```meta
lugar: El fondo de la Avenida
personajes: Nima, Gheco, el Fantasma Undefined
criatura: skeleton
carta: Fantasma 1 | una propiedad mal escrita da undefined · ?? pone un nombre por defecto
recompensa: xp 15, monedas 3
```

#### Escena
El Fantasma pasó por la fila de faroles y los carteles dicen *undefined*. Nima mira el código: alguien escribió mal una propiedad, y a un farol le falta el nombre.

#### Gheco sugiere
Revisá el nombre de la propiedad (`nombre`). Y para el farol que no tiene, usá `?? 'sin nombre'`.

#### Desafío
Que ningún cartel diga `undefined`.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  li { color: #ffd400; }
</style>
<ul id="faroles"></ul>
```

#### Estado
```
#faroles li
```

#### Código inicial
```javascript
const faroles = [{ nombre: 'Fuente' }, { nombre: 'Calesita' }, {}];
const lista = document.querySelector('#faroles');

for (const farol of faroles) {
  const li = document.createElement('li');
  li.textContent = `Farol de la ${farol.nombr}`;
  lista.append(li);
}
```

#### Salida esperada
```
── Estado ──
#faroles li: Farol de la Fuente
#faroles li: Farol de la Calesita
#faroles li: Farol de la sin nombre
```

#### Solución
```javascript
const faroles = [{ nombre: 'Fuente' }, { nombre: 'Calesita' }, {}];
const lista = document.querySelector('#faroles');

for (const farol of faroles) {
  const li = document.createElement('li');
  li.textContent = `Farol de la ${farol.nombre ?? 'sin nombre'}`;
  lista.append(li);
}
```

#### Al superarla
Los carteles recuperan sus nombres. El Fantasma, desde lejos, se estremece: no le gusta que le arreglen las cosas.

#### Imagen
- Una fila de faroles de feria con carteles debajo; el último cartel en blanco, y una sábana transparente flotando entre los faroles.
- El Fantasma Undefined (sábana vieja, transparente y celeste, con dos ojos huecos y tristes, sin boca, flotando) se aleja; Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) lo mira con el arco bajo.

### Micro-misión R02-N07-P2 · Los faroles que se apagan solos

```meta
lugar: El fondo de la Avenida
personajes: Nima, Gheco, el Fantasma Undefined
criatura: troll
carta: Fantasma 2 | estado + dibujar() · el evento cambia el estado, guarda y redibuja
recompensa: xp 15, monedas 3
```

#### Escena
Cada vez que Nima prende un farol, el Fantasma lo apaga, porque la página no **recuerda** cuáles están prendidos. Hay que guardar el estado.

#### Gheco sugiere
Guardá los números de los faroles prendidos en un arreglo `prendidos`. En el click (con delegación), agregá o sacá el número, guardá en `localStorage` y llamá a `dibujar()`.

#### Desafío
Completá el evento. La consigna trae guardado que el farol 2 ya estaba prendido; la comprobación prende el 4 y apaga el 2.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  #fila { display: flex; gap: 10px; }
  .farol { width: 44px; height: 44px; border-radius: 50%; background: #333; display: grid; place-items: center; cursor: pointer; }
  .farol.prendido { background: #ffd400; color: #0b1020; }
</style>
<div id="fila">
  <div class="farol" data-n="1">1</div><div class="farol" data-n="2">2</div><div class="farol" data-n="3">3</div><div class="farol" data-n="4">4</div>
</div>
```

#### Almacenamiento
```
local prendidos = [2]
```

#### Eventos
```
click [data-n="4"]
click [data-n="2"]
```

#### Estado
```
.farol.prendido
local prendidos
```

#### Código inicial
```javascript
let prendidos = JSON.parse(localStorage.getItem('prendidos') ?? '[]');

function dibujar() {
  for (const farol of document.querySelectorAll('.farol')) {
    farol.classList.toggle('prendido', prendidos.includes(Number(farol.dataset.n)));
  }
}

document.querySelector('#fila').addEventListener('click', (evento) => {
  const farol = evento.target.closest('.farol');
  if (!farol) return;
  const n = Number(farol.dataset.n);
  // si está prendido, sacalo; si no, agregalo. Después guardá y dibujá.

});

dibujar();
```

#### Salida esperada
```
── Estado ──
.farol.prendido: 4
local prendidos: [4]
```

#### Solución
```javascript
let prendidos = JSON.parse(localStorage.getItem('prendidos') ?? '[]');

function dibujar() {
  for (const farol of document.querySelectorAll('.farol')) {
    farol.classList.toggle('prendido', prendidos.includes(Number(farol.dataset.n)));
  }
}

document.querySelector('#fila').addEventListener('click', (evento) => {
  const farol = evento.target.closest('.farol');
  if (!farol) return;
  const n = Number(farol.dataset.n);
  if (prendidos.includes(n)) {
    prendidos = prendidos.filter((x) => x !== n);
  } else {
    prendidos.push(n);
  }
  localStorage.setItem('prendidos', JSON.stringify(prendidos));
  dibujar();
});

dibujar();
```

#### Al superarla
El Fantasma apaga un farol… y la página lo vuelve a dibujar prendido, porque se acuerda. Lo intenta tres veces. Se cansa.

#### Imagen
- Cuatro faroles de feria en fila; el Fantasma Undefined (sábana transparente celeste con ojos huecos) sopla uno, que sigue prendido.
- Nima, de brazos cruzados, sonríe; Gheco le saca la lengua al Fantasma.

### Micro-misión R02-N07-P3 · La Avenida que recuerda

```meta
lugar: El fondo de la Avenida
personajes: Nima, Gheco, Lucio, Lumina, el Fantasma Undefined
criatura: dragon
carta: El jefe | cargar · dibujar · validar el formulario · delegación para borrar · guardar después de cada cambio
recompensa: xp 30, oro 30, monedas 4
item: Farol del Fantasma
```

#### Escena
La última pelea: el Fantasma quiere borrar el **registro de faroles** de Lucio, la lista con el nombre de cada farol de la Avenida y sus horas de aceite. Nima tiene que armar la página entera: que cargue lo guardado, que deje agregar faroles validando los datos, que deje borrarlos con un botón ✕ y que **nunca** muestre un `undefined`.

#### Gheco sugiere
Seguí la forma de toda aplicación: estado (`faroles`, cargado o `[]`), `dibujar()`, `guardar()`, el `submit` que valida (nombre no vacío, horas número mayor que 0) y la delegación en la lista para los botones `.borrar` (con `data-i`, el índice).

#### Desafío
Completá `agregar` (con su validación) y el evento de borrar. La consigna trae guardado un farol; la comprobación intenta uno sin nombre, uno con horas que no son número, agrega dos bien y borra el primero. Al final:
- en la lista quedan `Calesita · 6 h` y `Fuente · 3 h`;
- el mensaje dice `Farol agregado: Fuente`;
- el total dice `Total: 9 h`.

#### Página
```html
<style>
  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
  input, button { font-size: 16px; padding: 4px 8px; margin: 2px; }
  li { margin: 4px 0; }
  .borrar { background: #552222; color: #fff; border: 0; border-radius: 4px; cursor: pointer; }
  #mensaje { color: #ffd400; }
</style>
<h1>Registro de faroles</h1>
<form id="nuevo"><input id="nombre" placeholder="nombre"><input id="horas" placeholder="horas"><button>Agregar</button></form>
<p id="mensaje"></p>
<ul id="lista"></ul>
<p id="total"></p>
```

#### Almacenamiento
```
local faroles = [{"nombre":"Entrada","horas":4}]
```

#### Eventos
```
escribir #horas 2
enviar #nuevo
escribir #nombre Calesita
escribir #horas mucho
enviar #nuevo
escribir #horas 6
enviar #nuevo
escribir #nombre Fuente
escribir #horas 3
enviar #nuevo
click #lista li:first-child .borrar
```

#### Estado
```
#lista li
#mensaje
#total
local faroles
```

#### Código inicial
```javascript
const lista = document.querySelector('#lista');
const mensaje = document.querySelector('#mensaje');
const total = document.querySelector('#total');
const faroles = JSON.parse(localStorage.getItem('faroles') ?? '[]');

function guardar() {
  localStorage.setItem('faroles', JSON.stringify(faroles));
}

function dibujar() {
  lista.replaceChildren();
  faroles.forEach((farol, i) => {
    const li = document.createElement('li');
    li.textContent = `${farol.nombre} · ${farol.horas} h `;
    const boton = document.createElement('button');
    boton.className = 'borrar';
    boton.dataset.i = i;
    boton.textContent = '✕';
    li.append(boton);
    lista.append(li);
  });
  total.textContent = `Total: ${faroles.reduce((suma, f) => suma + f.horas, 0)} h`;
}

function agregar(nombre, horas) {
  // validá: nombre vacío → 'Falta el nombre'; horas no número o <= 0 → 'Las horas tienen que ser un número mayor que 0'
  // si está bien: agregalo, guardá, dibujá y mostrá 'Farol agregado: …'

}

document.querySelector('#nuevo').addEventListener('submit', (evento) => {
  evento.preventDefault();
  agregar(document.querySelector('#nombre').value.trim(), Number(document.querySelector('#horas').value));
});

lista.addEventListener('click', (evento) => {
  // si tocaron un .borrar: sacá ese farol (splice), guardá y dibujá

});

dibujar();
```

#### Salida esperada
```
── Estado ──
#lista li: Calesita · 6 h ✕
#lista li: Fuente · 3 h ✕
#mensaje: Farol agregado: Fuente
#total: Total: 9 h
local faroles: [{"nombre":"Calesita","horas":6},{"nombre":"Fuente","horas":3}]
```

#### Solución
```javascript
const lista = document.querySelector('#lista');
const mensaje = document.querySelector('#mensaje');
const total = document.querySelector('#total');
const faroles = JSON.parse(localStorage.getItem('faroles') ?? '[]');

function guardar() {
  localStorage.setItem('faroles', JSON.stringify(faroles));
}

function dibujar() {
  lista.replaceChildren();
  faroles.forEach((farol, i) => {
    const li = document.createElement('li');
    li.textContent = `${farol.nombre} · ${farol.horas} h `;
    const boton = document.createElement('button');
    boton.className = 'borrar';
    boton.dataset.i = i;
    boton.textContent = '✕';
    li.append(boton);
    lista.append(li);
  });
  total.textContent = `Total: ${faroles.reduce((suma, f) => suma + f.horas, 0)} h`;
}

function agregar(nombre, horas) {
  if (nombre === '') {
    mensaje.textContent = 'Falta el nombre';
    return;
  }
  if (Number.isNaN(horas) || horas <= 0) {
    mensaje.textContent = 'Las horas tienen que ser un número mayor que 0';
    return;
  }
  faroles.push({ nombre, horas });
  guardar();
  dibujar();
  mensaje.textContent = `Farol agregado: ${nombre}`;
}

document.querySelector('#nuevo').addEventListener('submit', (evento) => {
  evento.preventDefault();
  agregar(document.querySelector('#nombre').value.trim(), Number(document.querySelector('#horas').value));
});

lista.addEventListener('click', (evento) => {
  const boton = evento.target.closest('.borrar');
  if (!boton) return;
  faroles.splice(Number(boton.dataset.i), 1);
  guardar();
  dibujar();
});

dibujar();
```

#### Al superarla
El registro de Lucio queda en pie, completo, sin un solo *undefined*. El Fantasma flota frente a la lista un largo rato, leyendo los nombres. Después se pliega solo, despacio, y se queda colgado de un farol como un pañuelo viejo. Cuando Nima lo toca, se vuelve un farolito de vidrio celeste que no quema: **el Farol del Fantasma**.

—Esperaba que alguien se acordara de los nombres —dice Lucio, en voz baja—. Igual que yo.

{mentor} abre las alas, y por primera vez en treinta años toda la Avenida de los Faroles queda prendida de punta a punta. Al fondo, en lo más oscuro, el taller del Vidriero tiene una ventana encendida.

#### Imagen
- Toda la avenida de la feria iluminada de punta a punta, y al fondo un taller viejo con una sola ventana encendida.
- Nima (trenza negra con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas, arco verde) sostiene un farolito de vidrio celeste; Lucio (farolero viejo, gorra de lana, abrigo largo) a su lado, emocionado.
- Lumina (luciérnaga enorme con alas de vidrio y luz amarilla en el pecho) con las alas abiertas sobre la avenida.
