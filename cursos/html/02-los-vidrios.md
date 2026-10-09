# RAMA R02 · Los Vidrios de colores: CSS

```meta
tipo: tronco
posicion: 2
```

## R02-N01 · Primeros vidrios: CSS

```meta
tipo: tema
padre: R01-N05
precio: 10
criatura: ogre
temas: css.selectores
usa: html.semantica
```

### Crónica

El esqueleto de plomo está listo. {mentor} abre el armario de los vidrios: azul noche, cian neón, ámbar. Iris quiere usar todos en la primera hora, como Teo, que ya está pintando un vitral de once colores.

—Ahora sí, el color —dice {mentor}—. Pero cuidado: cuando dos vidrios quieren el mismo hueco, **uno gana**. Hay que saber cuál, o vas a pelear toda la tarde contra un ogro que no ves.

En el fondo del armario, detrás de los frascos, Iris encuentra un vidrio de un color que no está en ninguna paleta del taller. Lo pone al lado de su fragmento: es exactamente el mismo.

### Objetivos

Enlazar una hoja de estilos, usar selectores, entender la **cascada**, la
**especificidad** y la **herencia**, y trabajar con colores, letras, unidades y variables.

### Antes de empezar

- HTML semántico («HTML semántico»).

### Explicación

#### Dónde va el CSS
```html
<link rel="stylesheet" href="estilos.css">   <!-- en el head: la forma normal en un proyecto -->
<style> ... </style>                          <!-- en el head: para una sola página -->
<p style="color: red">                        <!-- en línea: evitalo -->
```
En la plataforma cada página es **un solo archivo**, así que el CSS va en un `<style>` dentro del `head`. En un proyecto de verdad va en un archivo aparte (`estilos.css`) enlazado con `<link>`: así varias páginas comparten los mismos estilos.

#### Una regla
```css
selector {
  propiedad: valor;
}
```
| Selector | Elige | Ejemplo |
|---|---|---|
| `p` | todos los elementos `p` | `p { color: white; }` |
| `.aviso` | los que tienen `class="aviso"` (pueden ser muchos) | |
| `#especial` | el que tiene `id="especial"` (uno solo) | |
| `.caja p` | los `p` que están **dentro** de `.caja` | |
| `h1, h2` | los dos | |
| `a:hover`, `a:focus-visible` | un **estado**: mouse encima, foco con teclado | |
| `:root` | la raíz del documento (`html`) | para variables |

Un elemento puede tener varias clases: `class="aviso aviso-final"`.

#### ¿Quién gana? (la cascada)
Cuando varias reglas le dan un valor a la misma propiedad:
1. Gana la más **específica**: `#id` > `.clase` (y `:hover`) > `elemento`.
2. Con la misma especificidad, gana **la que está más abajo**.
3. `!important` le gana a todo: es un parche, evitalo.

#### Herencia
Algunas propiedades (color, letra, `line-height`) **pasan a los hijos**. Otras (bordes, márgenes, fondo) no. Pero si el hijo tiene **su propia regla**, gana esa: en el ejemplo, el párrafo de adentro de la caja no es gris porque la regla `p` le da otro color.

#### Valores
- **Colores**: `#22d3ee` (hexadecimal), `rgb(34 211 238)`, `rgb(34 211 238 / 50%)` (con transparencia), nombres (`crimson`).
- **Letras**: `font-family: system-ui, "Segoe UI", sans-serif;` es una **lista**: usa la primera que tenga el sistema. Siempre terminá en una genérica (`sans-serif`, `serif`, `monospace`).
- **Unidades**: `px` (fijo), **`rem`** (relativo al tamaño de letra del usuario: si agranda la letra en el sistema, todo crece; usalo para letras y espacios), `em` (relativo al padre), `%`.
- **Variables**: `--neon: #22d3ee;` en `:root` y `color: var(--neon);`. Cambiar el tema = cambiar las variables.

#### Cómo se ve el ejemplo

Fondo azul noche, letra clara, la etiqueta "PLATAFORMA DE CURSOS" en una píldora con borde cian, "árbol de habilidades" en cian. Los cuatro párrafos de prueba salen blanco, ámbar, rojo y verde. La caja con borde izquierdo cian tiene texto gris monoespaciado y un párrafo en cursiva que **no** es gris. Tocá *Celular* y *Compu* en la vista previa: .

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Primeros vidrios: CSS</title>
    <style>
      /* 06 - CSS basico: selectores, cascada, colores, letras y variables */

      /* Variables (custom properties): se definen una vez y se reutilizan */
      :root {
        --fondo: #0b1220;
        --texto: #e2e8f0;
        --apagado: #94a3b8;
        --neon: #22d3ee;
        --peligro: #f87171;
        --letra-codigo: ui-monospace, "JetBrains Mono", Consolas, monospace;
      }

      /* Selector de ELEMENTO: todos los body */
      body {
        background-color: var(--fondo);
        color: var(--texto); /* se hereda a todo lo de adentro */
        font-family: system-ui, "Segoe UI", Roboto, sans-serif;
        font-size: 1rem; /* rem = tamano de la letra raiz (normalmente 16px) */
        line-height: 1.5;
        margin: 0;
        padding: 1.25rem;
      }

      h1 {
        font-size: 1.75rem;
        line-height: 1.2;
      }

      h2 {
        color: var(--neon);
        font-size: 1.125rem;
        margin-top: 2rem;
      }

      code {
        font-family: var(--letra-codigo);
        color: var(--neon);
      }

      /* Selector de CLASE: los elementos con class="etiqueta" */
      .etiqueta {
        display: inline-block;
        font-family: var(--letra-codigo);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--neon);
        border: 1px solid var(--neon);
        border-radius: 999px;
        padding: 0.25rem 0.75rem;
      }

      .destacado {
        color: var(--neon);
      }

      /* --- Cascada y especificidad --- */
      p {
        color: var(--texto);
      }

      .aviso {
        color: #fbbf24; /* amarillo: clase > elemento */
      }

      #especial {
        color: var(--peligro); /* rojo: id > clase */
      }

      .aviso-final {
        color: #a3e635; /* verde: misma fuerza que .aviso, pero esta mas abajo */
      }

      /* Herencia: color y letra pasan a los hijos... salvo que tengan su propia regla */
      .caja-heredada {
        color: var(--apagado);
        font-family: var(--letra-codigo);
        border-left: 3px solid var(--neon);
        padding-left: 1rem;
      }

      /* Pseudoclases: estados */
      a {
        color: var(--neon);
      }

      a:hover,
      a:focus-visible {
        color: var(--fondo);
        background-color: var(--neon);
      }

      /* Selector DESCENDIENTE: solo los p que estan DENTRO de .caja-heredada */
      .caja-heredada p {
        font-style: italic;
      }
    </style>
  </head>
  <body>
    <main>
      <p class="etiqueta">Plataforma de cursos</p>
      <h1>Aprendé a programar avanzando por tu <span class="destacado">árbol de habilidades</span>.</h1>
      <p>Compilá algoritmos reales y desbloqueá nodos tecnológicos de bajo nivel.</p>

      <h2>¿Quién gana?</h2>
      <p>Párrafo común: lo pinta la regla de <code>p</code>.</p>
      <p class="aviso">Con clase: la regla de <code>.aviso</code> le gana a la de <code>p</code>.</p>
      <p class="aviso" id="especial">Con id: la regla de <code>#especial</code> le gana a la clase.</p>
      <p class="aviso aviso-final">Dos reglas con la misma fuerza: gana la que está <strong>más abajo</strong> en el CSS.</p>

      <h2>Herencia</h2>
      <div class="caja-heredada">
        El color gris y la letra los <strong>heredé</strong> de la caja que me contiene.
        <p>Este párrafo NO es gris: la regla de <code>p</code> le pone su propio color.</p>
      </div>

      <p><a href="#">Un enlace</a> que cambia al pasar el mouse.</p>
    </main>
  </body>
</html>
```

### ¿Para qué sirve?

Con el mismo HTML, el CSS cambia todo: el modo oscuro de una app, los colores de una marca, la versión para imprimir de una factura. Las **variables** son la forma en que las empresas cambian la paleta entera de un sitio tocando una sola línea. Y entender la especificidad es lo que separa a quien "pelea con el CSS" de quien lo maneja.

### Errores habituales

En CSS, un error **no rompe nada**: la regla se ignora en silencio. Abrí DevTools →
*Elementos* → panel *Estilos*: las propiedades inválidas aparecen **tachadas** con un ícono de advertencia, y las que perdieron contra otra regla, tachadas sin ícono.

**Goblin: valor inválido**: `font-size: 20 px;` (espacio), `color: #22d3e;` (5 dígitos), `colour: red;`. Se ignoran.

**Slime: falta un `;` o una `}`**: se pierde esa regla **y la siguiente**.

**Esqueleto: la clase no coincide**: `.Aviso` ≠ `class="aviso"`; o la ruta del `<link>` está mal (DevTools → *Red*: `estilos.css` en rojo).

**Ogro de la Cascada: "puse el estilo y no se aplica"**: otra regla más específica gana. Mirá en DevTools cuál está tachada.

### Prueba del sello

#### `.aviso` y `#especial` le dan color al mismo párrafo: ¿cuál gana? ¿Y si son dos clases?

Gana `#especial`: un id pesa más que cualquier cantidad de clases. Si son **dos clases** con la misma especificidad, gana la regla que aparece **después** en el CSS.

#### ¿Por qué conviene `rem` para el tamaño de letra?

Porque `rem` se mide desde el tamaño de letra que eligió la persona en su navegador. Si alguien agranda la letra para leer mejor, todo lo que está en `rem` crece con ella; lo que está en `px` queda fijo.

#### ¿Qué ventaja tienen las variables CSS?

Que un valor se escribe **una sola vez** (`--neon: #22d3ee;`) y se usa en todos lados con `var(--neon)`. Para cambiar el tema alcanza con cambiar las variables, y hasta se pueden pisar en una parte de la página.

### Micro-misión R02-N01-P1 · El primer vidrio

```meta
lugar: El armario de los vidrios
personajes: Iris, Tesela
carta: Una regla de CSS | selector { propiedad: valor; } · h1 { color: #22d3ee; }
recompensa: xp 10, oro 10
```

#### Escena
El esqueleto de plomo está listo. {mentor} abre el armario de los vidrios: azul noche, cian neón, ámbar. —Ahora sí, el color. Empezá por uno solo.

#### Gheco sugiere
Una regla dice **a quién** (el selector), **qué** (la propiedad) y **cómo** (el valor): `h1 { color: #22d3ee; }`. El CSS va en el `<style>`; el **Inspector** lee tus reglas tal como las escribiste (no mide cómo quedó dibujado): mirá en la vista previa que se vea como querés.

#### Desafío
Escribí en el `style` una regla para que el `h1` sea de color `#22d3ee`.

#### Código inicial
```html
<style>

</style>
<h1>Los Talleres de los Vitrales</h1>
```

#### Inspector
```
css h1 { color }
```

#### Salida esperada
```
css h1 { color }: #22d3ee
```

#### Solución
```html
<style>
  h1 { color: #22d3ee; }
</style>
<h1>Los Talleres de los Vitrales</h1>
```

#### Al superarla
El título se tiñe de cian, como un vidrio a contraluz. Iris lo mira diez segundos sin respirar.

#### Imagen
- Un armario abierto lleno de vidrios de colores ordenados por tono; sobre la mesa, un título de plomo que brilla en cian.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) sostiene un vidrio cian.
- Tesela (22, pelo corto iridiscente violeta y cian, monóculo de cristal tallado, sobretodo largo negro con fragmentos de vidrio de colores cosidos) abre el armario.

### Micro-misión R02-N01-P2 · Un vidrio para el aviso

```meta
lugar: El armario de los vidrios
personajes: Iris, Teo
carta: Clases | class="aviso" en el HTML · .aviso { … } en el CSS · el punto quiere decir «clase»
recompensa: xp 10, oro 10
```

#### Escena
Teo quiere pintar de ámbar **todos** los párrafos. Iris solo quiere el aviso.

#### Gheco sugiere
Una **clase** marca algunos elementos: `class="aviso"` en el HTML y `.aviso { … }` en el CSS (con punto). Así no se pinta todo.

#### Desafío
Ponele `class="aviso"` al segundo párrafo y escribí la regla `.aviso` con `background-color: #f59e0b`.

#### Código inicial
```html
<style>

</style>
<p>Encargos de toda la semana.</p>
<p>Mañana el taller abre tarde.</p>
```

#### Inspector
```
p @class
css .aviso { background-color }
```

#### Salida esperada
```
p @class: (no tiene)
p @class: aviso
css .aviso { background-color }: #f59e0b
```

#### Solución
```html
<style>
  .aviso { background-color: #f59e0b; }
</style>
<p>Encargos de toda la semana.</p>
<p class="aviso">Mañana el taller abre tarde.</p>
```

#### Al superarla
Solo el aviso se pone ámbar. Teo pinta igual todos sus párrafos, de once colores distintos.

#### Imagen
- Dos placas de vidrio en una pared; una sola brilla en ámbar.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) cuelga la ámbar.
- Teo (15, flaco, pelo negro enrulado con purpurina, pecas, delantal manchado de todos los colores, cinturón con frascos de vidrio molido) con las manos manchadas de pintura.

### Micro-misión R02-N01-P3 · Una sola vez, en el body

```meta
lugar: El armario de los vidrios
personajes: Iris, Tesela, Gheco
carta: Herencia | el color y la letra pasan de padres a hijos · body { color: … } alcanza para toda la página
recompensa: xp 10, oro 10
```

#### Escena
Iris pintó de gris claro cada cosa, una por una: el párrafo, la lista, el título chico. {mentor} cuenta las reglas en voz alta. Son tres para lo mismo.

#### Gheco sugiere
El `color` y la letra se **heredan**: si se lo ponés al `body`, todo lo de adentro lo toma, salvo lo que tenga su propia regla.

#### Desafío
Poné `color: #e2e8f0` una sola vez en `body` y borrá las tres reglas de `h2`, `p` y `li`.

#### Código inicial
```html
<style>
  body { background-color: #0f172a; }
  h2 { color: #e2e8f0; }
  p { color: #e2e8f0; }
  li { color: #e2e8f0; }
</style>
<h2>Vidrios del día</h2>
<p>Lo que hay en el armario:</p>
<ul><li>Azul noche</li><li>Cian neón</li></ul>
```

#### Inspector
```
css body { color }
css h2 { color }
css p { color }
css li { color }
```

#### Salida esperada
```
css body { color }: #e2e8f0
css h2 { color }: (no hay)
css p { color }: (no hay)
css li { color }: (no hay)
```

#### Solución
```html
<style>
  body { background-color: #0f172a; color: #e2e8f0; }
</style>
<h2>Vidrios del día</h2>
<p>Lo que hay en el armario:</p>
<ul><li>Azul noche</li><li>Cian neón</li></ul>
```

#### Al superarla
Tres reglas menos y todo se ve igual. Gheco sopla el polvo de las reglas borradas.

#### Imagen
- Un vitral oscuro con todo el texto gris claro.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) borra con un trapo tres líneas de una pizarra.
- Gheco (gecko de luz con antiparras) sopla el polvo.

### Micro-misión R02-N01-P4 · El color que no está en ninguna paleta

```meta
lugar: El armario de los vidrios
personajes: Iris, Tesela
carta: Variables | :root { --nombre: valor; } · se usa con var(--nombre) · cambiás el valor una vez y cambia en todos lados
recompensa: xp 10, oro 10
```

#### Escena
En el fondo del armario, detrás de los frascos, Iris encuentra un vidrio de un color que no está en ninguna paleta del taller. Lo pone al lado de su fragmento: es exactamente el mismo. Quiere guardarlo con un nombre.

#### Gheco sugiere
Una **variable** guarda un valor con nombre: `:root { --vidrio-misterio: #7c3aed; }`, y se usa con `var(--vidrio-misterio)`.

#### Desafío
Creá en `:root` la variable `--vidrio-misterio` con `#7c3aed`, y usala como `border-color` de `.fragmento`.

#### Código inicial
```html
<style>
  .fragmento { border: 4px solid; border-color: #7c3aed; padding: 1rem; }
</style>
<p class="fragmento">El fragmento de Iris</p>
```

#### Inspector
```
css :root { --vidrio-misterio }
css .fragmento { border-color }
```

#### Salida esperada
```
css :root { --vidrio-misterio }: #7c3aed
css .fragmento { border-color }: var(--vidrio-misterio)
```

#### Solución
```html
<style>
  :root { --vidrio-misterio: #7c3aed; }
  .fragmento { border: 4px solid; border-color: var(--vidrio-misterio); padding: 1rem; }
</style>
<p class="fragmento">El fragmento de Iris</p>
```

#### Al superarla
Iris le muestra el vidrio a {mentor}. Ella lo mira mucho rato, sin el monóculo. No dice nada. Lo guarda en el mismo bolsillo del sobretodo donde guardó el boceto del Vidriero.

#### Imagen
- Dos vidrios violetas idénticos sobre una mesa, uno con plomo y otro suelto.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) los compara.
- Tesela (22, pelo corto iridiscente violeta y cian, monóculo de cristal tallado, sobretodo largo negro con fragmentos de vidrio de colores cosidos) los mira sin el monóculo, pensativa.

### Misión R02-N01-M1 · Tu propio tema

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Partí de la página del ejemplo (ya está en el editor) y creá **un tema distinto** —otros colores de fondo, texto y acento— cambiando **solo** las variables de `:root`. El resto del CSS no se toca.

#### Criterio de aprobación

- Cambió los valores de las variables en `:root`.
- No modificó ninguna otra regla del CSS ni el HTML.
- El texto se lee bien sobre el fondo nuevo (buen contraste).

#### Cómo debe quedar

celular: capturas/R02-N01-M1-celular.webp
compu: capturas/R02-N01-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Primeros vidrios: CSS</title>
    <style>
      /* 06 - CSS basico: selectores, cascada, colores, letras y variables */

      /* Variables (custom properties): se definen una vez y se reutilizan */
      :root {
        --fondo: #0b1220;
        --texto: #e2e8f0;
        --apagado: #94a3b8;
        --neon: #22d3ee;
        --peligro: #f87171;
        --letra-codigo: ui-monospace, "JetBrains Mono", Consolas, monospace;
      }

      /* Selector de ELEMENTO: todos los body */
      body {
        background-color: var(--fondo);
        color: var(--texto); /* se hereda a todo lo de adentro */
        font-family: system-ui, "Segoe UI", Roboto, sans-serif;
        font-size: 1rem; /* rem = tamano de la letra raiz (normalmente 16px) */
        line-height: 1.5;
        margin: 0;
        padding: 1.25rem;
      }

      h1 {
        font-size: 1.75rem;
        line-height: 1.2;
      }

      h2 {
        color: var(--neon);
        font-size: 1.125rem;
        margin-top: 2rem;
      }

      code {
        font-family: var(--letra-codigo);
        color: var(--neon);
      }

      /* Selector de CLASE: los elementos con class="etiqueta" */
      .etiqueta {
        display: inline-block;
        font-family: var(--letra-codigo);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--neon);
        border: 1px solid var(--neon);
        border-radius: 999px;
        padding: 0.25rem 0.75rem;
      }

      .destacado {
        color: var(--neon);
      }

      /* --- Cascada y especificidad --- */
      p {
        color: var(--texto);
      }

      .aviso {
        color: #fbbf24; /* amarillo: clase > elemento */
      }

      #especial {
        color: var(--peligro); /* rojo: id > clase */
      }

      .aviso-final {
        color: #a3e635; /* verde: misma fuerza que .aviso, pero esta mas abajo */
      }

      /* Herencia: color y letra pasan a los hijos... salvo que tengan su propia regla */
      .caja-heredada {
        color: var(--apagado);
        font-family: var(--letra-codigo);
        border-left: 3px solid var(--neon);
        padding-left: 1rem;
      }

      /* Pseudoclases: estados */
      a {
        color: var(--neon);
      }

      a:hover,
      a:focus-visible {
        color: var(--fondo);
        background-color: var(--neon);
      }

      /* Selector DESCENDIENTE: solo los p que estan DENTRO de .caja-heredada */
      .caja-heredada p {
        font-style: italic;
      }
    </style>
  </head>
  <body>
    <main>
      <p class="etiqueta">Plataforma de cursos</p>
      <h1>Aprendé a programar avanzando por tu <span class="destacado">árbol de habilidades</span>.</h1>
      <p>Compilá algoritmos reales y desbloqueá nodos tecnológicos de bajo nivel.</p>

      <h2>¿Quién gana?</h2>
      <p>Párrafo común: lo pinta la regla de <code>p</code>.</p>
      <p class="aviso">Con clase: la regla de <code>.aviso</code> le gana a la de <code>p</code>.</p>
      <p class="aviso" id="especial">Con id: la regla de <code>#especial</code> le gana a la clase.</p>
      <p class="aviso aviso-final">Dos reglas con la misma fuerza: gana la que está <strong>más abajo</strong> en el CSS.</p>

      <h2>Herencia</h2>
      <div class="caja-heredada">
        El color gris y la letra los <strong>heredé</strong> de la caja que me contiene.
        <p>Este párrafo NO es gris: la regla de <code>p</code> le pone su propio color.</p>
      </div>

      <p><a href="#">Un enlace</a> que cambia al pasar el mouse.</p>
    </main>
  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Tema propio con variables</title>
    <style>
      /* Cambiar el tema = cambiar solo las variables */
      :root {
        --fondo: #1a0b20;
        --texto: #f5e9ff;
        --acento: #e879f9;
      }
      body {
        background: var(--fondo);
        color: var(--texto);
        font-family: system-ui, sans-serif;
        padding: 1.25rem;
      }
      h1,
      a {
        color: var(--acento);
      }
    </style>
  </head>
  <body>
    <h1>Tema Amatista</h1>
    <p>Mismo HTML, otras variables. <a href="#">Un enlace</a>.</p>
  </body>
</html>
```


### Misión R02-N01-M2 · Ganale a la especificidad

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

En el código inicial, el párrafo con clase `verde` sale **rojo**: la regla `#tablero p` le gana. Lográ que sea verde **sin usar `!important`** y sin borrar la regla `#tablero p`. Escribí en un comentario por qué tu regla gana.

#### Criterio de aprobación

- El párrafo `.verde` se ve verde y el otro sigue rojo.
- No usa `!important` ni estilos en línea (`style="…"`).
- Explica en un comentario por qué su selector gana (la especificidad).

#### Cómo debe quedar

celular: capturas/R02-N01-M2-celular.webp
compu: capturas/R02-N01-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Ganale a la especificidad</title>
    <style>
      body {
        font-family: system-ui, sans-serif;
        padding: 1.25rem;
      }
      #tablero p {
        color: crimson;
      }
      .verde {
        color: green;
      }
    </style>
  </head>
  <body>
    <div id="tablero">
      <p>Rojo por la regla #tablero p.</p>
      <p class="verde">Este tendría que ser verde.</p>
    </div>
  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Ganale a la especificidad</title>
    <style>
      body {
        font-family: system-ui, sans-serif;
        padding: 1.25rem;
      }
      /* Esta regla (id + elemento) le gana a la de abajo aunque este antes */
      #tablero p {
        color: crimson;
      }
      /* Solo una clase: pierde contra #tablero p */
      .verde {
        color: green;
      }
      /* Solucion correcta: subir la especificidad de forma pareja, sin !important */
      #tablero .verde {
        color: green;
      }
    </style>
  </head>
  <body>
    <div id="tablero">
      <p>Rojo por la regla #tablero p.</p>
      <p class="verde">Verde gracias a #tablero .verde.</p>
    </div>
  </body>
</html>
```


### Encargo R02-N01-E1 · La carta del café

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Un café quiere su carta: fondo crema, letra con serifa, la lista de productos con el precio en negrita y una línea punteada entre ítem e ítem.

#### Criterio de aprobación

- Fondo crema y una fuente con serifa.
- Los precios en negrita.
- Una línea punteada entre los productos (`border-bottom: 1px dotted …`).

#### Cómo debe quedar

celular: capturas/R02-N01-E1-celular.webp
compu: capturas/R02-N01-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La carta del café</title>
    <style>

    </style>
  </head>
  <body>

  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Café del Puerto</title>
    <style>
      :root {
        --cafe: #4b2e1e;
        --crema: #f6ecd9;
      }
      body {
        background: var(--crema);
        color: var(--cafe);
        font-family: Georgia, "Times New Roman", serif;
        padding: 1.25rem;
      }
      h1 {
        text-align: center;
        letter-spacing: 0.05em;
      }
      .precio {
        font-weight: bold;
        margin-left: 0.5rem;
      }
      li {
        border-bottom: 1px dashed var(--cafe);
        padding: 0.5rem 0;
        list-style: none;
      }
    </style>
  </head>
  <body>
    <h1>Café del Puerto</h1>
    <ul>
      <li>Café con leche <span class="precio">$2500</span></li>
      <li>Medialunas (3) <span class="precio">$2100</span></li>
      <li>Tostado <span class="precio">$4200</span></li>
    </ul>
  </body>
</html>
```

## R02-N02 · El modelo de caja

```meta
tipo: tema
padre: R02-N01
precio: 10
criatura: orc
temas: css.caja
usa: css.selectores
```

### Crónica

Cada vidrio del vitral va dentro de un marco, y entre marco y marco hay un espacio. Iris mide a ojo y los vidrios se le salen del marco.

Justo pasa por el taller **Tesla**, el Artífice de la Ciudadela, a buscar un encargo. Mira el trabajo de Iris y se ríe: —Igual que Tesela cuando éramos aprendices de Ferrum. —{mentor} lo mira por encima del monóculo y Tesla se pone serio de golpe. Saca su cinta métrica—. Todo es una **caja**, Iris: contenido, relleno, borde y espacio afuera. **Medí las cuatro.**

### Objetivos

Entender el **modelo de caja** (contenido, `padding`, `border`, `margin`), usar `box-sizing: border-box`, limitar anchos con `max-width`, conocer `display` y armar la **tarjeta de curso** de la plataforma con su barra de progreso.

### Antes de empezar

- Selectores, variables y unidades («Primeros vidrios: CSS»).

### Explicación

#### Las cuatro capas
```
┌──────────── margin (afuera, transparente) ────────────┐
│ ┌────────── border ──────────────────────────────────┐ │
│ │ ┌──────── padding (adentro, con el fondo) ───────┐ │ │
│ │ │              contenido (width × height)         │ │ │
│ │ └─────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```
- Atajos: `padding: 10px` (los 4 lados), `10px 20px` (arriba/abajo, costados), `10px 20px 5px 0` (arriba, derecha, abajo, izquierda: como las agujas del reloj).
- **`box-sizing: border-box`**: el `width` **incluye** padding y borde. Sin esto, una caja de `width: 100%` con padding mide **más** que la pantalla. Se pone para todo al principio de cada hoja de estilos (`*, *::before, *::after`).
- **`max-width`**: "como mucho este ancho, pero achicate si no entra". Clave para el celular: con `width: 400px` la caja se sale de una pantalla de 390.
- `margin: 0 auto` centra horizontalmente una caja con ancho.
- Los navegadores ponen **márgenes de fábrica** a `body`, `p`, `h1`…: en las tarjetas se controlan a mano.

#### Bordes y sombras
`border-radius: 0.75rem` redondea; `999px` hace una píldora. `box-shadow: x y difuminado color`; se pueden poner varias separadas por comas (el brillo neón de las tarjetas es una sombra de 1 px de color cian).

#### `display`
| Valor | Comportamiento | Ejemplos de fábrica |
|---|---|---|
| `block` | ocupa todo el ancho, empieza en una línea nueva | `div`, `p`, `h1`, `section` |
| `inline` | fluye con el texto; **ignora** `width`/`height` y el margen vertical | `span`, `a`, `strong` |
| `inline-block` | fluye con el texto pero respeta tamaño y padding | chips, etiquetas |
| `none` | no se muestra (ni ocupa lugar) | |

(`flex` y `grid` en 08–09.)

#### Barra de progreso
Una caja (`.barra`, fondo oscuro, `overflow: hidden`) con otra adentro (`.barra-relleno`) de `width: 75%`. Para el lector de pantalla: `role="progressbar"` y `aria-valuenow="75"`. Existe `<progress>`, pero casi no se puede estilizar igual en todos los navegadores.

#### El ejemplo

Caja de demostración, tarjeta del curso de C++ (igual a la de esta plataforma) y ejemplos de `display`.

**Probalo con DevTools**: seleccioná la tarjeta → pestaña *Calculado*: aparece el diagrama de caja con los números reales de cada capa.

#### Cómo se ve el ejemplo

Tocá *Celular* y *Compu* en la vista previa: la caja punteada cian, la tarjeta oscura con borde sutil y brillo, "MOD-04" con la etiqueta verde "Activo", la barra al 75 % y "+350 XP" en cian; abajo, el span con fondo rojizo y la chip con borde redondeado.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Modelo de caja: la tarjeta de curso</title>
    <style>
      /* 07 - Modelo de caja */
      :root {
        --fondo: #0b1220;
        --panel: #111a2e;
        --borde: #1f2a44;
        --texto: #e2e8f0;
        --apagado: #94a3b8;
        --neon: #22d3ee;
        --verde: #4ade80;
        --mono: ui-monospace, "JetBrains Mono", Consolas, monospace;
      }

      /* Con border-box, width INCLUYE padding y borde (mucho mas facil de calcular) */
      *,
      *::before,
      *::after {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        padding: 1.25rem;
        background: var(--fondo);
        color: var(--texto);
        font-family: system-ui, "Segoe UI", Roboto, sans-serif;
        line-height: 1.5;
      }

      h2 {
        margin-top: 2.5rem;
        color: var(--neon);
        font-size: 1.125rem;
      }

      /* --- La caja de demostracion --- */
      .demo {
        width: 220px;
        padding: 20px; /* espacio ADENTRO, entre contenido y borde */
        border: 4px dashed var(--neon); /* el borde */
        margin: 24px 0; /* espacio AFUERA: arriba/abajo 24, costados 0 */
        background: var(--panel); /* el fondo cubre contenido + padding */
        font-family: var(--mono);
        text-align: center;
      }

      /* --- Tarjeta --- */
      .tarjeta {
        max-width: 22rem; /* nunca mas ancha que esto, pero se achica si no entra */
        padding: 1.25rem;
        background: var(--panel);
        border: 1px solid var(--borde);
        border-radius: 0.75rem;
        /* sombra: x  y  difuminado  color */
        box-shadow: 0 0 0 1px rgb(34 211 238 / 25%), 0 10px 30px rgb(0 0 0 / 40%);
      }

      /* Los p traen margen de fabrica: lo controlamos nosotros */
      .tarjeta p,
      .tarjeta h3 {
        margin: 0 0 0.75rem;
      }

      .modulo {
        font-family: var(--mono);
        font-size: 0.75rem;
        color: var(--apagado);
      }

      .estado {
        display: inline-block;
        margin-left: 0.5rem;
        padding: 0.125rem 0.5rem;
        border-radius: 0.25rem;
        background: rgb(74 222 128 / 15%);
        color: var(--verde);
      }

      .tarjeta-titulo {
        font-size: 1.125rem;
      }

      .tarjeta-texto {
        color: var(--apagado);
        font-size: 0.875rem;
      }

      .progreso-texto {
        font-size: 0.75rem;
        color: var(--apagado);
      }

      .barra {
        height: 0.5rem;
        margin-bottom: 1rem;
        background: var(--borde);
        border-radius: 999px;
        overflow: hidden; /* que el relleno no se salga de las puntas redondeadas */
      }

      .barra-relleno {
        height: 100%;
        background: var(--neon);
      }

      .tarjeta .xp {
        margin: 0;
        font-family: var(--mono);
        font-weight: bold;
        color: var(--neon);
      }

      /* --- display --- */
      .en-linea {
        padding: 4px; /* en inline, el padding vertical NO empuja las lineas */
        background: rgb(248 113 113 / 30%);
      }

      .chip {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border: 1px solid var(--neon);
        border-radius: 999px;
      }
    </style>
  </head>
  <body>
    <main>
      <h1>El modelo de caja</h1>

      <!-- Caja de demostracion: contenido + padding + borde + margen -->
      <div class="demo">contenido</div>

      <h2>Una tarjeta de curso</h2>
      <article class="tarjeta">
        <p class="modulo">MOD-04 <span class="estado">Activo</span></p>
        <h3 class="tarjeta-titulo">C++ Moderno &amp; Videojuegos</h3>
        <p class="tarjeta-texto">Gestión de memoria, RAII, punteros inteligentes y conceptos de C++20.</p>
        <p class="progreso-texto">Progreso de nodos: 18 / 24</p>
        <!-- Barra de progreso: una caja dentro de otra, con ancho en % -->
        <div class="barra" role="progressbar" aria-label="Progreso del curso" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
          <div class="barra-relleno" style="width: 75%"></div>
        </div>
        <p class="xp">+350 XP</p>
      </article>

      <h2>block, inline e inline-block</h2>
      <p>
        Un <span class="en-linea">span (inline)</span> fluye con el texto; una
        <span class="chip">chip (inline-block)</span> fluye pero acepta padding y alto.
      </p>
    </main>
  </body>
</html>
```

### ¿Para qué sirve?

Cada botón, tarjeta, foto y párrafo de una página es una caja. Cuando algo "se sale", "queda pegado" o "no está centrado", el problema casi siempre está en una de sus cuatro medidas. El inspector del navegador te las dibuja en colores: es la herramienta que más vas a usar para arreglar diseños.

### Errores habituales

**Orco del Desborde: caja más ancha que la pantalla.** `width: 400px` (o `100%` + padding sin `border-box`): aparece scroll horizontal en el celular. Usá `max-width` y `border-box`.

**Ogro: el `width` en un `span` no hace nada** (es `inline`). Usá `inline-block` o `block`.

**Ogro: márgenes que "se juntan"**: dos márgenes verticales seguidos no se suman, se usa el mayor (*margin collapse*). Si molesta, usá `padding` o `gap` («Flexbox»).

**Ogro: la barra se sale de las puntas redondeadas**: falta `overflow: hidden` en el contenedor.

### Prueba del sello

#### ¿Qué diferencia hay entre `padding` y `margin`? ¿Cuál se pinta con el fondo?

El `padding` es el relleno **de adentro**, entre el contenido y el borde: se pinta con el fondo de la caja. El `margin` es el espacio **de afuera**, entre esta caja y las vecinas: es transparente.

#### ¿Qué cambia `box-sizing: border-box`?

Hace que el `width` incluya el relleno y el borde. Sin él, una caja de `width: 300px` con `padding: 20px` mide en realidad 340 px y se sale de su lugar; con `border-box` mide 300 px justos.

#### ¿Por qué `max-width` es mejor que `width` para el celular?

Porque `width: 600px` mide siempre 600 px, aunque la pantalla tenga 390: aparece el scroll de costado. `max-width: 600px` dice "como mucho 600": en la compu mide eso y en el celular se achica al ancho que haya.

### Micro-misión R02-N02-P1 · Aire adentro del marco

```meta
lugar: El taller de Tesela
personajes: Iris, Tesla
carta: padding | el relleno: el aire entre el contenido y el borde · padding: 1rem
recompensa: xp 10, oro 10
```

#### Escena
Iris mide a ojo y el texto queda pegado al plomo. Justo pasa por el taller **Tesla**, el Artífice de la Ciudadela, y se ríe: —Igual que Tesela cuando éramos aprendices de Ferrum. —{mentor} lo mira por encima del monóculo y Tesla se pone serio de golpe.

#### Gheco sugiere
Todo es una **caja**: contenido, relleno (`padding`), borde y margen. El `padding` es el aire **adentro** del borde.

#### Desafío
Dale a `.vidrio` un `padding` de `1rem`.

#### Código inicial
```html
<style>
  .vidrio { border: 2px solid #22d3ee; }
</style>
<p class="vidrio">Vidrio cian, con su plomo.</p>
```

#### Inspector
```
css .vidrio { padding }
```

#### Salida esperada
```
css .vidrio { padding }: 1rem
```

#### Solución
```html
<style>
  .vidrio { border: 2px solid #22d3ee; padding: 1rem; }
</style>
<p class="vidrio">Vidrio cian, con su plomo.</p>
```

#### Al superarla
El texto respira. Tesla saca su cinta métrica: —Medí las cuatro capas. Siempre las cuatro.

#### Imagen
- Un vidrio cian con su marco de plomo y un espacio de aire entre el texto y el marco.
- Tesla (muchacho delgado de pelo negro azulado en punta, visor cian, traje azul ajustado con líneas de luz cian y engranajes de bronce en los hombros) con una cinta métrica de bronce.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) mide.

### Micro-misión R02-N02-P2 · El plomo alrededor

```meta
lugar: El taller de Tesela
personajes: Iris, Tesla
carta: border | border: grosor estilo color · border: 2px solid #22d3ee
recompensa: xp 10, oro 10
```

#### Escena
—Sin plomo, un vidrio es un vidrio en el piso —le recuerda Tesla, que lo escuchó mil veces de Ferrum.

#### Gheco sugiere
`border` lleva tres cosas: el grosor, el estilo (`solid`, `dashed`…) y el color, en ese orden.

#### Desafío
Ponele a `.vidrio` un `border` de `3px solid #f59e0b`.

#### Código inicial
```html
<style>
  .vidrio { padding: 1rem; }
</style>
<p class="vidrio">Vidrio ámbar.</p>
```

#### Inspector
```
css .vidrio { border }
```

#### Salida esperada
```
css .vidrio { border }: 3px solid #f59e0b
```

#### Solución
```html
<style>
  .vidrio { padding: 1rem; border: 3px solid #f59e0b; }
</style>
<p class="vidrio">Vidrio ámbar.</p>
```

#### Al superarla
Un marco ámbar rodea el vidrio. Tesla asiente, guarda la cinta y se va con su encargo bajo el brazo.

#### Imagen
- Un vidrio con un marco grueso de color ámbar.
- Tesla (muchacho delgado de pelo negro azulado en punta, visor cian, traje azul ajustado con líneas de luz cian y engranajes de bronce en los hombros) se va con un paquete bajo el brazo.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) lo saluda.

### Micro-misión R02-N02-P3 · El ancho que no cierra

```meta
lugar: El taller de Tesela
personajes: Iris, Gheco
carta: box-sizing | border-box: el ancho incluye relleno y borde · * { box-sizing: border-box; }
recompensa: xp 10, oro 10
```

#### Escena
Iris le dio `width: 200px` al vidrio, pero mide 232. Le sumó el relleno y el borde por su cuenta.

#### Gheco sugiere
Con `box-sizing: border-box`, el `width` **incluye** el relleno y el borde. Se pone una vez para todo: `* { box-sizing: border-box; }`.

#### Desafío
Agregá una regla para `*` con `box-sizing: border-box`.

#### Código inicial
```html
<style>
  .vidrio { width: 200px; padding: 1rem; border: 0; background-color: #22d3ee; }
</style>
<p class="vidrio">200 px, ni uno más.</p>
```

#### Inspector
```
css * { box-sizing }
```

#### Salida esperada
```
css * { box-sizing }: border-box
```

#### Solución
```html
<style>
  * { box-sizing: border-box; }
  .vidrio { width: 200px; padding: 1rem; border: 0; background-color: #22d3ee; }
</style>
<p class="vidrio">200 px, ni uno más.</p>
```

#### Al superarla
El vidrio mide 200 justo. Gheco lo mide dos veces, por las dudas, como haría Tizón.

#### Imagen
- Un vidrio cian con una regla de medir al lado que marca exactamente 200.
- Gheco (gecko de luz con antiparras) con una cinta métrica.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) satisfecha.

### Micro-misión R02-N02-P4 · Esquinas pulidas

```meta
lugar: El taller de Tesela
personajes: Iris, Tesela
carta: Bordes y sombras | border-radius redondea las esquinas · box-shadow: x y desenfoque color
recompensa: xp 10, oro 10
```

#### Escena
—Las esquinas en punta se rompen primero —dice {mentor}, y le alcanza una lima de pulir.

#### Gheco sugiere
`border-radius` redondea las esquinas (`12px`, o `9999px` para una píldora).

#### Desafío
Dale a `.tarjeta` un `border-radius` de `12px`.

#### Código inicial
```html
<style>
  .tarjeta { padding: 1rem; background-color: #1e293b; color: #e2e8f0; }
</style>
<div class="tarjeta">Encargo: ventana para el Valle</div>
```

#### Inspector
```
css .tarjeta { border-radius }
```

#### Salida esperada
```
css .tarjeta { border-radius }: 12px
```

#### Solución
```html
<style>
  .tarjeta { padding: 1rem; background-color: #1e293b; color: #e2e8f0; border-radius: 12px; }
</style>
<div class="tarjeta">Encargo: ventana para el Valle</div>
```

#### Al superarla
Las esquinas quedan suaves. {mentor} pasa el dedo y no se corta.

#### Imagen
- Una tarjeta de vidrio azul oscuro con las esquinas redondeadas.
- Tesela (22, pelo corto iridiscente violeta y cian, monóculo de cristal tallado, sobretodo largo negro con fragmentos de vidrio de colores cosidos) pasa el dedo por una esquina.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) con una lima de pulir.

### Misión R02-N02-M1 · La tarjeta de SDL3

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Partí del ejemplo y agregá la tarjeta del curso de **SDL3** con acento **violeta**. Reutilizá las mismas clases de la tarjeta de C++ y cambiá **solo** la variable `--neon` en esa tarjeta (por ejemplo, con un `style="--neon: #a78bfa"` o una clase propia).

#### Criterio de aprobación

- La tarjeta de SDL3 usa las mismas clases que la de C++.
- El violeta sale de pisar la variable `--neon` solo en esa tarjeta, no de reglas nuevas para cada parte.
- La tarjeta de C++ sigue cian.

#### Cómo debe quedar

celular: capturas/R02-N02-M1-celular.webp
compu: capturas/R02-N02-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Modelo de caja: la tarjeta de curso</title>
    <style>
      /* 07 - Modelo de caja */
      :root {
        --fondo: #0b1220;
        --panel: #111a2e;
        --borde: #1f2a44;
        --texto: #e2e8f0;
        --apagado: #94a3b8;
        --neon: #22d3ee;
        --verde: #4ade80;
        --mono: ui-monospace, "JetBrains Mono", Consolas, monospace;
      }

      /* Con border-box, width INCLUYE padding y borde (mucho mas facil de calcular) */
      *,
      *::before,
      *::after {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        padding: 1.25rem;
        background: var(--fondo);
        color: var(--texto);
        font-family: system-ui, "Segoe UI", Roboto, sans-serif;
        line-height: 1.5;
      }

      h2 {
        margin-top: 2.5rem;
        color: var(--neon);
        font-size: 1.125rem;
      }

      /* --- La caja de demostracion --- */
      .demo {
        width: 220px;
        padding: 20px; /* espacio ADENTRO, entre contenido y borde */
        border: 4px dashed var(--neon); /* el borde */
        margin: 24px 0; /* espacio AFUERA: arriba/abajo 24, costados 0 */
        background: var(--panel); /* el fondo cubre contenido + padding */
        font-family: var(--mono);
        text-align: center;
      }

      /* --- Tarjeta --- */
      .tarjeta {
        max-width: 22rem; /* nunca mas ancha que esto, pero se achica si no entra */
        padding: 1.25rem;
        background: var(--panel);
        border: 1px solid var(--borde);
        border-radius: 0.75rem;
        /* sombra: x  y  difuminado  color */
        box-shadow: 0 0 0 1px rgb(34 211 238 / 25%), 0 10px 30px rgb(0 0 0 / 40%);
      }

      /* Los p traen margen de fabrica: lo controlamos nosotros */
      .tarjeta p,
      .tarjeta h3 {
        margin: 0 0 0.75rem;
      }

      .modulo {
        font-family: var(--mono);
        font-size: 0.75rem;
        color: var(--apagado);
      }

      .estado {
        display: inline-block;
        margin-left: 0.5rem;
        padding: 0.125rem 0.5rem;
        border-radius: 0.25rem;
        background: rgb(74 222 128 / 15%);
        color: var(--verde);
      }

      .tarjeta-titulo {
        font-size: 1.125rem;
      }

      .tarjeta-texto {
        color: var(--apagado);
        font-size: 0.875rem;
      }

      .progreso-texto {
        font-size: 0.75rem;
        color: var(--apagado);
      }

      .barra {
        height: 0.5rem;
        margin-bottom: 1rem;
        background: var(--borde);
        border-radius: 999px;
        overflow: hidden; /* que el relleno no se salga de las puntas redondeadas */
      }

      .barra-relleno {
        height: 100%;
        background: var(--neon);
      }

      .tarjeta .xp {
        margin: 0;
        font-family: var(--mono);
        font-weight: bold;
        color: var(--neon);
      }

      /* --- display --- */
      .en-linea {
        padding: 4px; /* en inline, el padding vertical NO empuja las lineas */
        background: rgb(248 113 113 / 30%);
      }

      .chip {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border: 1px solid var(--neon);
        border-radius: 999px;
      }
    </style>
  </head>
  <body>
    <main>
      <h1>El modelo de caja</h1>

      <!-- Caja de demostracion: contenido + padding + borde + margen -->
      <div class="demo">contenido</div>

      <h2>Una tarjeta de curso</h2>
      <article class="tarjeta">
        <p class="modulo">MOD-04 <span class="estado">Activo</span></p>
        <h3 class="tarjeta-titulo">C++ Moderno &amp; Videojuegos</h3>
        <p class="tarjeta-texto">Gestión de memoria, RAII, punteros inteligentes y conceptos de C++20.</p>
        <p class="progreso-texto">Progreso de nodos: 18 / 24</p>
        <!-- Barra de progreso: una caja dentro de otra, con ancho en % -->
        <div class="barra" role="progressbar" aria-label="Progreso del curso" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
          <div class="barra-relleno" style="width: 75%"></div>
        </div>
        <p class="xp">+350 XP</p>
      </article>

      <h2>block, inline e inline-block</h2>
      <p>
        Un <span class="en-linea">span (inline)</span> fluye con el texto; una
        <span class="chip">chip (inline-block)</span> fluye pero acepta padding y alto.
      </p>
    </main>
  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Tarjeta SDL3</title>
    <style>
      /* 07 - Modelo de caja */
      :root {
        --fondo: #0b1220;
        --panel: #111a2e;
        --borde: #1f2a44;
        --texto: #e2e8f0;
        --apagado: #94a3b8;
        --neon: #22d3ee;
        --verde: #4ade80;
        --mono: ui-monospace, "JetBrains Mono", Consolas, monospace;
      }

      /* Con border-box, width INCLUYE padding y borde (mucho mas facil de calcular) */
      *,
      *::before,
      *::after {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        padding: 1.25rem;
        background: var(--fondo);
        color: var(--texto);
        font-family: system-ui, "Segoe UI", Roboto, sans-serif;
        line-height: 1.5;
      }

      h2 {
        margin-top: 2.5rem;
        color: var(--neon);
        font-size: 1.125rem;
      }

      /* --- La caja de demostracion --- */
      .demo {
        width: 220px;
        padding: 20px; /* espacio ADENTRO, entre contenido y borde */
        border: 4px dashed var(--neon); /* el borde */
        margin: 24px 0; /* espacio AFUERA: arriba/abajo 24, costados 0 */
        background: var(--panel); /* el fondo cubre contenido + padding */
        font-family: var(--mono);
        text-align: center;
      }

      /* --- Tarjeta --- */
      .tarjeta {
        max-width: 22rem; /* nunca mas ancha que esto, pero se achica si no entra */
        padding: 1.25rem;
        background: var(--panel);
        border: 1px solid var(--borde);
        border-radius: 0.75rem;
        /* sombra: x  y  difuminado  color */
        box-shadow: 0 0 0 1px rgb(34 211 238 / 25%), 0 10px 30px rgb(0 0 0 / 40%);
      }

      /* Los p traen margen de fabrica: lo controlamos nosotros */
      .tarjeta p,
      .tarjeta h3 {
        margin: 0 0 0.75rem;
      }

      .modulo {
        font-family: var(--mono);
        font-size: 0.75rem;
        color: var(--apagado);
      }

      .estado {
        display: inline-block;
        margin-left: 0.5rem;
        padding: 0.125rem 0.5rem;
        border-radius: 0.25rem;
        background: rgb(74 222 128 / 15%);
        color: var(--verde);
      }

      .tarjeta-titulo {
        font-size: 1.125rem;
      }

      .tarjeta-texto {
        color: var(--apagado);
        font-size: 0.875rem;
      }

      .progreso-texto {
        font-size: 0.75rem;
        color: var(--apagado);
      }

      .barra {
        height: 0.5rem;
        margin-bottom: 1rem;
        background: var(--borde);
        border-radius: 999px;
        overflow: hidden; /* que el relleno no se salga de las puntas redondeadas */
      }

      .barra-relleno {
        height: 100%;
        background: var(--neon);
      }

      .tarjeta .xp {
        margin: 0;
        font-family: var(--mono);
        font-weight: bold;
        color: var(--neon);
      }

      /* --- display --- */
      .en-linea {
        padding: 4px; /* en inline, el padding vertical NO empuja las lineas */
        background: rgb(248 113 113 / 30%);
      }

      .chip {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border: 1px solid var(--neon);
        border-radius: 999px;
      }
    </style>
    <style>
      /* Reutiliza la tarjeta y cambia solo el color de acento */
      .violeta {
        --neon: #a78bfa;
      }
    </style>
  </head>
  <body>
    <article class="tarjeta violeta">
      <p class="modulo">MOD-06</p>
      <h3 class="tarjeta-titulo">SDL3 &amp; Game Loops</h3>
      <p class="tarjeta-texto">Renderizado acelerado, eventos y ventanas en tiempo real.</p>
      <p class="progreso-texto">Progreso de nodos: 10 / 22</p>
      <div class="barra" role="progressbar" aria-label="Progreso del curso" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100">
        <div class="barra-relleno" style="width: 45%"></div>
      </div>
      <p class="xp">+420 XP</p>
    </article>
  </body>
</html>
```


### Misión R02-N02-M2 · La caja centrada

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá una caja con un texto que en el celular ocupe **todo el ancho** y en la compu mida **como mucho 30 rem**, centrada en la pantalla. Mirala en *Celular* y en *Compu*.

#### Criterio de aprobación

- Usa `max-width: 30rem` (no `width`).
- Se centra con `margin-inline: auto` (o `margin: 0 auto`).
- En el celular no aparece scroll de costado.

#### Cómo debe quedar

celular: capturas/R02-N02-M2-celular.webp
compu: capturas/R02-N02-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La caja centrada</title>
    <style>

    </style>
  </head>
  <body>

  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Centrar una caja</title>
    <style>
      body {
        margin: 0;
        padding: 1rem;
        font-family: system-ui, sans-serif;
      }
      .centrada {
        box-sizing: border-box;
        max-width: 30rem; /* ancho maximo */
        margin: 2rem auto; /* auto a los costados = centrada */
        padding: 1.5rem;
        border: 2px solid #22d3ee;
        border-radius: 1rem;
      }
    </style>
  </head>
  <body>
    <div class="centrada">
      <p>Estoy centrada con <code>margin: auto</code>. En el celular ocupo todo el ancho; en la computadora, como mucho 30rem.</p>
    </div>
  </body>
</html>
```


### Encargo R02-N02-E1 · El ticket del almacén

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Un almacén quiere su ticket: papel blanco centrado de **20 rem como máximo**, un borde superior grueso, sombra, y líneas punteadas entre los productos.

#### Criterio de aprobación

- El papel mide como mucho 20 rem y está centrado.
- Tiene borde superior grueso y sombra (`box-shadow`).
- Líneas punteadas entre productos.

#### Cómo debe quedar

celular: capturas/R02-N02-E1-celular.webp
compu: capturas/R02-N02-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El ticket del almacén</title>
    <style>

    </style>
  </head>
  <body>

  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Ticket de compra</title>
    <style>
      * {
        box-sizing: border-box;
      }
      body {
        margin: 0;
        padding: 1rem;
        background: #e5e7eb;
        font-family: ui-monospace, Consolas, monospace;
      }
      .ticket {
        max-width: 20rem;
        margin: 0 auto;
        padding: 1rem 1.25rem;
        background: white;
        border-top: 6px solid #111827;
        box-shadow: 0 4px 12px rgb(0 0 0 / 15%);
      }
      .ticket h1 {
        margin: 0 0 1rem;
        font-size: 1.125rem;
        text-align: center;
      }
      .linea {
        margin: 0;
        padding: 0.25rem 0;
        border-bottom: 1px dashed #9ca3af;
      }
      .total {
        margin: 0.75rem 0 0;
        font-weight: bold;
      }
    </style>
  </head>
  <body>
    <div class="ticket">
      <h1>Almacén del Muelle</h1>
      <p class="linea">Yerba 1kg ........ $3200</p>
      <p class="linea">Pan ............... $1200</p>
      <p class="total">TOTAL ............. $4400</p>
    </div>
  </body>
</html>
```

## R02-N03 · Flexbox

```meta
tipo: tema
padre: R02-N02
precio: 10
criatura: orc
temas: css.flexbox
usa: css.caja
```

### Crónica

En el borde de arriba del ventanal van el escudo a la izquierda y los trofeos a la derecha; abajo, cuatro botones iguales. Iris lo intenta con márgenes «a ojo» y en cada pantalla queda distinto. Va por el boceto 61.

—Dejá de empujar los vidrios con el dedo —dice {mentor}, y le da una regla que se estira—. Esta es la **regla flexible**: le decís cómo repartir el espacio y ella se acomoda sola.

### Objetivos

Acomodar elementos en **una dirección** (fila o columna) con Flexbox: separar, alinear, repartir espacio, dejar que algo crezca y pasar a otra línea. Con piezas reales de la versión celular de la plataforma.

### Antes de empezar

- Modelo de caja y `display` («El modelo de caja»).

### Explicación

`display: flex` en el **contenedor** pone a sus **hijos** en una línea (el **eje principal**). El otro eje es el **cruzado**.

| En el contenedor | Qué hace | Valores |
|---|---|---|
| `flex-direction` | dirección del eje principal | `row` (por defecto), `column` |
| `justify-content` | reparte en el eje **principal** | `flex-start`, `center`, `space-between`, `space-around`, `flex-end` |
| `align-items` | alinea en el eje **cruzado** | `stretch` (por defecto), `center`, `flex-start`, `flex-end` |
| `gap` | espacio **entre** hijos | `0.75rem` |
| `flex-wrap: wrap` | si no entran, siguen en otra línea | |

| En un hijo | Qué hace |
|---|---|
| `flex: 1` | crece y ocupa el espacio que sobra (varios con `flex: 1` = partes iguales) |
| `flex-shrink: 0` | no se achica aunque falte lugar (avatares, íconos) |
| `min-width: 0` | permite que un texto largo se achique y se corte |
| `flex: 1 1 12rem` | crece, se achica, y su tamaño base es 12 rem (columnas que se acomodan solas) |

**Recetas de la plataforma:**
| Pieza | Receta |
|---|---|
| barra superior | `justify-content: space-between` + `align-items: center` |
| botón que ocupa el resto | `flex: 1` en ese botón |
| fila del ranking | avatar `flex-shrink: 0`, nombre `flex: 1; min-width: 0` |
| centrar algo en los dos ejes | `justify-content: center` + `align-items: center` |
| filtros (chips) | `flex-wrap: wrap` + `gap` |
| barra inferior | cada enlace `flex: 1` |

`gap` reemplaza a los márgenes entre hijos: no se duplica en los bordes y no tiene
*margin collapse*.

#### El ejemplo

Barra superior, botones, tres filas del ranking (una con un nombre larguísimo), chips y barra inferior.

**Probalo con DevTools**: al lado de un elemento con `display: flex` aparece la etiqueta `flex`; al tocarla, dibuja los ejes y los espacios.

#### Cómo se ve el ejemplo

Tocá *Celular* y *Compu* en la vista previa: igual que la parte de arriba y la de abajo de esta plataforma (versión celular). El nombre largo termina en `…` sin empujar los puntos. Los chips ocupan tres líneas en el celular y una sola en la computadora.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Flexbox: piezas de la plataforma</title>
    <style>
      /* 08 - Flexbox */
      :root {
        --fondo: #0b1220;
        --panel: #111a2e;
        --borde: #1f2a44;
        --texto: #e2e8f0;
        --apagado: #94a3b8;
        --neon: #22d3ee;
        --mono: ui-monospace, "JetBrains Mono", Consolas, monospace;
      }

      *,
      *::before,
      *::after {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        background: var(--fondo);
        color: var(--texto);
        font-family: system-ui, "Segoe UI", Roboto, sans-serif;
        line-height: 1.5;
      }

      a {
        color: inherit;
        text-decoration: none;
      }

      .neon {
        color: var(--neon);
      }

      main {
        padding: 1.25rem;
        display: flex;
        flex-direction: column; /* uno abajo del otro... */
        gap: 1.5rem; /* ...con espacio parejo entre cada bloque */
      }

      /* 1) Barra superior */
      .barra-superior {
        display: flex; /* los hijos se ponen en fila */
        justify-content: space-between; /* extremos separados (eje principal) */
        align-items: center; /* centrados en vertical (eje cruzado) */
        padding: 0.75rem 1.25rem;
        border-bottom: 1px solid var(--borde);
      }

      .marca {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 800;
      }

      .stats {
        display: flex;
        gap: 0.75rem;
        margin: 0;
        padding: 0.25rem 0.75rem;
        border: 1px solid var(--borde);
        border-radius: 0.5rem;
        font-family: var(--mono);
        font-size: 0.875rem;
      }

      /* 2) Botones */
      .acciones {
        display: flex;
        gap: 0.75rem;
      }

      .boton {
        padding: 0.875rem 1rem;
        border-radius: 0.5rem;
        font-weight: 600;
        text-align: center;
      }

      .boton-principal {
        flex: 1; /* crece y ocupa todo el espacio que sobra */
        background: var(--neon);
        color: var(--fondo);
      }

      .boton-secundario {
        border: 1px solid var(--borde);
        color: var(--neon);
      }

      /* 3) Ranking */
      .ranking {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin: 0;
        padding: 0;
        list-style: none;
      }

      .fila {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1rem;
        background: var(--panel);
        border: 1px solid var(--borde);
        border-radius: 0.75rem;
      }

      .puesto {
        width: 1.5rem;
        color: var(--apagado);
        font-family: var(--mono);
      }

      .avatar {
        display: flex;
        align-items: center;
        justify-content: center; /* centrar en los dos ejes */
        width: 2.25rem;
        height: 2.25rem;
        flex-shrink: 0; /* que no se achique aunque el nombre sea largo */
        border-radius: 0.5rem;
        background: var(--borde);
      }

      .nombre {
        flex: 1;
        min-width: 0; /* permite que el texto largo se corte en vez de empujar */
        display: flex;
        flex-direction: column;
        font-weight: 600;
      }

      /* La elipsis funciona en una caja de texto comun, no en un contenedor flex */
      .alias {
        overflow: hidden;
        text-overflow: ellipsis; /* ... al final */
        white-space: nowrap;
      }

      .nombre small,
      .puntos small {
        color: var(--apagado);
        font-weight: 400;
        font-size: 0.7rem;
      }

      .puntos {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        font-family: var(--mono);
      }

      /* 4) Chips */
      .chips {
        display: flex;
        flex-wrap: wrap; /* si no entran, siguen en otra linea */
        gap: 0.5rem;
        margin: 0;
        padding: 0;
        list-style: none;
      }

      .chips li {
        padding: 0.25rem 0.75rem;
        border: 1px solid var(--borde);
        border-radius: 0.375rem;
        font-size: 0.8rem;
      }

      .chips li:first-child {
        background: var(--neon);
        color: var(--fondo);
      }

      /* 5) Barra inferior */
      .barra-inferior {
        display: flex;
        border-top: 1px solid var(--borde);
        background: var(--panel);
      }

      .barra-inferior a {
        flex: 1; /* las cuatro partes iguales */
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.125rem;
        padding: 0.5rem 0;
        font-size: 0.75rem;
        color: var(--apagado);
      }

      .barra-inferior a[aria-current="page"] {
        color: var(--neon);
      }

      .marca img {
        border-radius: 0.5rem;
      }
    </style>
  </head>
  <body>
    <!-- 1) Barra superior: logo a la izquierda, estadisticas a la derecha -->
    <header class="barra-superior">
      <a class="marca" href="#">
        <img src="/img/cursos/html/gheco-logo.webp" alt="" width="36" height="36">
        <span>GhecoSoft <span class="neon">-Code</span></span>
      </a>
      <p class="stats">
        <span>⚡ 1.450</span>
        <span>🔥 12</span>
      </p>
    </header>

    <main>
      <!-- 2) Botones: uno crece, el otro mide lo que necesita -->
      <div class="acciones">
        <a class="boton boton-principal" href="#">▷ Continuar campaña</a>
        <a class="boton boton-secundario" href="#">Nodos</a>
      </div>

      <!-- 3) Fila del ranking: puesto, avatar, nombre (crece), puntos -->
      <ol class="ranking">
        <li class="fila">
          <span class="puesto">4</span>
          <span class="avatar">⚡</span>
          <span class="nombre"><span class="alias">@ZeroByte_Arg</span> <small>C++ · ▲ +1</small></span>
          <span class="puntos">10.900 <small>XP</small></span>
        </li>
        <li class="fila">
          <span class="puesto">5</span>
          <span class="avatar">🧙</span>
          <span class="nombre"><span class="alias">@PixelSage</span> <small>SDL3 · ▲ +3</small></span>
          <span class="puntos">9.850 <small>XP</small></span>
        </li>
        <li class="fila">
          <span class="puesto">6</span>
          <span class="avatar">🦊</span>
          <span class="nombre"><span class="alias">@CodeKitsune_con_un_nombre_larguisimo</span> <small>OpenGL · ▼ -2</small></span>
          <span class="puntos">8.920 <small>XP</small></span>
        </li>
      </ol>

      <!-- 4) Chips que pasan a otra linea si no entran -->
      <ul class="chips">
        <li>Todos (23)</li>
        <li>Bajo nivel / C++</li>
        <li>Gráficos &amp; Shaders</li>
        <li>Desarrollo Web</li>
        <li>Backend &amp; Cloud</li>
      </ul>
    </main>

    <!-- 5) Barra inferior del celular: cuatro partes iguales -->
    <nav class="barra-inferior" aria-label="Secciones">
      <a href="#"><span aria-hidden="true">🗺</span>Campañas</a>
      <a href="#"><span aria-hidden="true">📖</span>Lecciones</a>
      <a href="#" aria-current="page"><span aria-hidden="true">⚔</span>Arena</a>
      <a href="#"><span aria-hidden="true">🌳</span>Árbol</a>
    </nav>
  </body>
</html>
```

### ¿Para qué sirve?

Las barras de navegación, las filas de un chat, una tarjeta con foto y texto, los botones de un formulario, los íconos de una app: casi todo lo que va "uno al lado del otro" se arma con flexbox. Es, por lejos, la herramienta de diseño más usada de CSS. Y es la misma que usa React Native para armar las pantallas de las apps de celular.

### Errores habituales

**Ogro: `justify-content: center` no centra en vertical.** En una fila, `justify` trabaja en horizontal: para vertical, `align-items`.

**Ogro: `flex` en el hijo en vez del padre.** `display: flex` va en el
**contenedor**.

**Orco del Desborde: un texto largo empuja todo fuera de la pantalla.** Falta `min-width: 0` en el elemento que crece (por defecto un hijo flex no se achica más que su contenido).

**Ogro: la elipsis (`…`) no aparece.** `text-overflow: ellipsis` necesita una caja de texto común con `overflow: hidden` y `white-space: nowrap`; no funciona directo sobre un contenedor flex.

### Prueba del sello

#### ¿Qué diferencia hay entre `justify-content` y `align-items`?

`justify-content` reparte los hijos sobre el **eje principal** (a lo largo de la fila, si es `row`). `align-items` los alinea sobre el **eje cruzado** (de arriba a abajo, en una fila).

#### ¿Cómo hacés que cuatro botones midan lo mismo?

Poniéndolos en un contenedor con `display: flex` y dándole `flex: 1` a cada botón: el espacio se reparte en partes iguales.

#### ¿Por qué un nombre largo puede romper una fila flex y cómo se evita?

Porque un hijo flex no se achica por debajo del largo de su texto: empuja a los demás y se sale. Se evita con `min-width: 0` en ese hijo (y `overflow: hidden; text-overflow: ellipsis; white-space: nowrap` para cortarlo con `…`).

### Micro-misión R02-N03-P1 · La regla que se estira

```meta
lugar: La cornisa del ventanal
personajes: Iris, Tesela
carta: display: flex | los hijos se ponen en fila · el contenedor reparte el espacio
recompensa: xp 10, oro 10
```

#### Escena
En la cornisa del ventanal van el escudo y los trofeos, uno al lado del otro. Iris los empuja con márgenes «a ojo». Va por el boceto 61.
—Dejá de empujar los vidrios con el dedo —dice {mentor}, y le da una regla que se estira.

#### Gheco sugiere
Con `display: flex` en el **contenedor**, sus hijos se ponen en fila y se reparten el espacio solos.

#### Desafío
Poné `display: flex` en `.cornisa`.

#### Código inicial
```html
<style>
  .cornisa { padding: 1rem; background-color: #0f172a; color: #e2e8f0; }
</style>
<header class="cornisa">
  <span>Escudo</span>
  <span>Trofeos</span>
</header>
```

#### Inspector
```
css .cornisa { display }
```

#### Salida esperada
```
css .cornisa { display }: flex
```

#### Solución
```html
<style>
  .cornisa { display: flex; padding: 1rem; background-color: #0f172a; color: #e2e8f0; }
</style>
<header class="cornisa">
  <span>Escudo</span>
  <span>Trofeos</span>
</header>
```

#### Al superarla
Los dos vidrios se acomodan en fila, solos. Iris tira el boceto 61 al canasto, sin pena.

#### Imagen
- Una cornisa de vitral con dos piezas acomodándose solas en una fila.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) sostiene una regla de bronce que se estira.
- Tesela (22, pelo corto iridiscente violeta y cian, monóculo de cristal tallado, sobretodo largo negro con fragmentos de vidrio de colores cosidos) al lado.

### Micro-misión R02-N03-P2 · Uno a cada punta

```meta
lugar: La cornisa del ventanal
personajes: Iris, Gheco
carta: justify-content | reparte en el eje principal · space-between: uno a cada punta · center: al medio
recompensa: xp 10, oro 10
```

#### Escena
El escudo va a la izquierda y los trofeos a la derecha, bien a la punta.

#### Gheco sugiere
`justify-content` reparte en la dirección de la fila: `space-between` deja el primero en una punta y el último en la otra.

#### Desafío
Agregale a `.cornisa` un `justify-content: space-between`.

#### Código inicial
```html
<style>
  .cornisa { display: flex; padding: 1rem; background-color: #0f172a; color: #e2e8f0; }
</style>
<header class="cornisa">
  <span>Escudo</span>
  <span>Trofeos</span>
</header>
```

#### Inspector
```
css .cornisa { justify-content }
```

#### Salida esperada
```
css .cornisa { justify-content }: space-between
```

#### Solución
```html
<style>
  .cornisa { display: flex; justify-content: space-between; padding: 1rem; background-color: #0f172a; color: #e2e8f0; }
</style>
<header class="cornisa">
  <span>Escudo</span>
  <span>Trofeos</span>
</header>
```

#### Al superarla
El escudo y los trofeos se van cada uno a su punta. Gheco se sienta en el medio, que quedó libre.

#### Imagen
- Una cornisa con un escudo a la izquierda y trofeos a la derecha.
- Gheco (gecko de luz con antiparras) sentado en el medio.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) mira desde abajo.

### Micro-misión R02-N03-P3 · Centrados y con aire

```meta
lugar: La cornisa del ventanal
personajes: Iris, Teo
carta: align-items y gap | align-items: center los centra en el otro eje · gap: espacio entre los hijos
recompensa: xp 10, oro 10
```

#### Escena
Abajo van cuatro botones. Teo los separó con márgenes de distinto tamaño, y además el escudo, que es más alto, deja los botones torcidos.

#### Gheco sugiere
`align-items: center` los centra en el otro eje (el vertical, en una fila), y `gap` deja el mismo espacio entre todos.

#### Desafío
En `.botones`, poné `align-items: center` y `gap: 1rem`.

#### Código inicial
```html
<style>
  .botones { display: flex; }
  .botones a { padding: 0.5rem 1rem; background-color: #22d3ee; color: #0f172a; }
</style>
<nav class="botones">
  <a href="#">Taller</a>
  <a href="#">Encargos</a>
  <a href="#">Liga</a>
  <a href="#">Contacto</a>
</nav>
```

#### Inspector
```
css .botones { align-items }
css .botones { gap }
```

#### Salida esperada
```
css .botones { align-items }: center
css .botones { gap }: 1rem
```

#### Solución
```html
<style>
  .botones { display: flex; align-items: center; gap: 1rem; }
  .botones a { padding: 0.5rem 1rem; background-color: #22d3ee; color: #0f172a; }
</style>
<nav class="botones">
  <a href="#">Taller</a>
  <a href="#">Encargos</a>
  <a href="#">Liga</a>
  <a href="#">Contacto</a>
</nav>
```

#### Al superarla
Los cuatro botones quedan parejos. Teo los mide con la mano y, por primera vez, da igual.

#### Imagen
- Cuatro botones de vidrio cian en fila, a la misma distancia.
- Teo (15, flaco, pelo negro enrulado con purpurina, pecas, delantal manchado de todos los colores, cinturón con frascos de vidrio molido) los mide con la palma.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) sonríe.

### Micro-misión R02-N03-P4 · Cuatro botones iguales

```meta
lugar: La cornisa del ventanal
personajes: Iris, Tesela
carta: flex: 1 | cada hijo con flex: 1 ocupa la misma parte del espacio que sobra
recompensa: xp 10, oro 10
```

#### Escena
—Iguales —dice {mentor}—. No «parecidos»: iguales. Que ocupen todo el ancho, repartido.

#### Gheco sugiere
`flex: 1` en **cada hijo** hace que se repartan el espacio en partes iguales.

#### Desafío
Escribí una regla para `.botones a` con `flex: 1`.

#### Código inicial
```html
<style>
  .botones { display: flex; gap: 1rem; }
</style>
<nav class="botones">
  <a href="#">Taller</a>
  <a href="#">Encargos</a>
  <a href="#">Liga</a>
  <a href="#">Contacto</a>
</nav>
```

#### Inspector
```
css .botones a { flex }
```

#### Salida esperada
```
css .botones a { flex }: 1
```

#### Solución
```html
<style>
  .botones { display: flex; gap: 1rem; }
  .botones a { flex: 1; }
</style>
<nav class="botones">
  <a href="#">Taller</a>
  <a href="#">Encargos</a>
  <a href="#">Liga</a>
  <a href="#">Contacto</a>
</nav>
```

#### Al superarla
Los cuatro botones se estiran hasta ocupar la fila, del mismo ancho. {mentor} no dice nada; sigue con su vitral.

#### Imagen
- Una franja de vitral con cuatro paneles exactamente iguales.
- Tesela (22, pelo corto iridiscente violeta y cian, monóculo de cristal tallado, sobretodo largo negro con fragmentos de vidrio de colores cosidos) trabaja en su propio vitral.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) compara los paneles.

### Misión R02-N03-M1 · La tarjeta de perfil

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá una tarjeta de perfil en una sola fila: un avatar redondo a la izquierda, el nombre y el nivel en el medio (que ocupen el espacio que sobra) y un botón "Seguir" a la derecha.

#### Criterio de aprobación

- El contenedor usa `display: flex` con `align-items: center` y `gap`.
- El bloque del medio tiene `flex: 1` (y `min-width: 0`).
- El avatar no se achica (`flex-shrink: 0`) y es redondo (`border-radius: 50%`).

#### Cómo debe quedar

celular: capturas/R02-N03-M1-celular.webp
compu: capturas/R02-N03-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La tarjeta de perfil</title>
    <style>

    </style>
  </head>
  <body>

  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Tarjeta de perfil con flex</title>
    <style>
      * {
        box-sizing: border-box;
      }
      body {
        margin: 0;
        padding: 1.25rem;
        background: #0b1220;
        color: #e2e8f0;
        font-family: system-ui, sans-serif;
      }
      .perfil {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        border: 1px solid #1f2a44;
        border-radius: 0.75rem;
      }
      .perfil img {
        flex-shrink: 0;
        border-radius: 50%;
        background: #111a2e;
      }
      .datos {
        flex: 1;
      }
      .datos h1 {
        margin: 0;
        font-size: 1.125rem;
      }
      .datos p {
        margin: 0;
        color: #94a3b8;
      }
      .seguir {
        padding: 0.5rem 1rem;
        border-radius: 999px;
        background: #22d3ee;
        color: #0b1220;
        font-weight: 600;
        text-decoration: none;
      }
    </style>
  </head>
  <body>
    <div class="perfil">
      <img src="/img/cursos/html/heroe-avatar.webp" alt="" width="56" height="56">
      <div class="datos">
        <h1>@Iris</h1>
        <p>Nivel 14 · Espadachina</p>
      </div>
      <a class="seguir" href="#">Seguir</a>
    </div>
  </body>
</html>
```


### Misión R02-N03-M2 · Centrado total

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Poné un cartel **en el centro exacto de la ventana**, en los dos ejes. Pista: el `body` tiene que medir al menos todo el alto (`min-height: 100vh`).

#### Criterio de aprobación

- El cartel queda centrado horizontal y verticalmente, en celular y en compu.
- Usa flexbox (`justify-content: center` y `align-items: center`), no márgenes calculados a mano.

#### Cómo debe quedar

celular: capturas/R02-N03-M2-celular.webp
compu: capturas/R02-N03-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Centrado total</title>
    <style>

    </style>
  </head>
  <body>

  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Centrado total</title>
    <style>
      body {
        margin: 0;
        min-height: 100vh; /* alto de toda la ventana */
        display: flex;
        justify-content: center;
        align-items: center;
        background: #0b1220;
        color: #e2e8f0;
        font-family: system-ui, sans-serif;
      }
      .cartel {
        padding: 2rem;
        border: 2px solid #22d3ee;
        border-radius: 1rem;
        text-align: center;
      }
    </style>
  </head>
  <body>
    <div class="cartel">
      <p>Cargando el Taller…</p>
    </div>
  </body>
</html>
```


### Encargo R02-N03-E1 · El pie de la ferretería

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Una ferretería quiere un pie de página con tres columnas (dirección, horarios, contacto) que en el celular queden una abajo de la otra **sin media queries**: con `flex-wrap: wrap` y `flex: 1 1 12rem`.

#### Criterio de aprobación

- No usa `@media`.
- Usa `flex-wrap: wrap` y un tamaño base en cada columna (`flex: 1 1 12rem`).
- En *Celular* las columnas se apilan; en *Compu* quedan en una fila.

#### Cómo debe quedar

celular: capturas/R02-N03-E1-celular.webp
compu: capturas/R02-N03-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El pie de la ferretería</title>
    <style>

    </style>
  </head>
  <body>

  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Pie de página con flex-wrap</title>
    <style>
      * {
        box-sizing: border-box;
      }
      body {
        margin: 0;
        font-family: system-ui, sans-serif;
      }
      footer {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 1rem 2rem;
        padding: 1.5rem;
        background: #111827;
        color: #d1d5db;
      }
      footer section {
        flex: 1 1 12rem; /* crece, se achica, base 12rem: 1 columna en el celular, 3 en la PC */
      }
      footer h2 {
        margin: 0 0 0.5rem;
        font-size: 1rem;
        color: white;
      }
      footer p {
        margin: 0;
      }
    </style>
  </head>
  <body>
    <footer>
      <section aria-labelledby="pie-1">
        <h2 id="pie-1">Ferretería Central</h2>
        <p>Desde 1985</p>
      </section>
      <section aria-labelledby="pie-2">
        <h2 id="pie-2">Horario</h2>
        <p>Lunes a sábado, 8 a 20</p>
      </section>
      <section aria-labelledby="pie-3">
        <h2 id="pie-3">Contacto</h2>
        <p>380 400-1111</p>
      </section>
    </footer>
  </body>
</html>
```

## R02-N04 · Grid

```meta
tipo: tema
padre: R02-N03
precio: 10
criatura: orc
temas: css.grid
usa: css.flexbox
```

### Crónica

Llega un mensajero del Imperio de las Clases: **Kaffa**, el Arquitecto Imperial, encarga doce vitrales para su catedral. «Todos iguales, alineados en filas y columnas perfectas», dice la carta. Y abajo, el podio de los campeones: el del medio, más alto. Teo propone hacer el del medio de otro color. Nadie le contesta.

—Con la regla flexible hacés filas, Iris —dice {mentor}—, pero no **cuadrículas**. Para Kaffa, que no tolera un vidrio torcido, desplegamos la **malla**.

### Objetivos

Armar layouts en **dos dimensiones** con CSS Grid: columnas fijas y fraccionarias, grillas que deciden solas cuántas columnas entran, celdas que ocupan varias columnas y layouts dibujados con áreas.

### Antes de empezar

- Flexbox («Flexbox»).

### Explicación

`display: grid` en el contenedor + `grid-template-columns` define las columnas. Los hijos se van ubicando en orden, celda por celda.

| Propiedad | Ejemplo | Resultado |
|---|---|---|
| `grid-template-columns` | `1fr 1fr` | dos columnas iguales (`fr` = fracción del espacio libre) |
| | `12rem 1fr` | una fija y otra que ocupa el resto |
| | `repeat(4, 1fr)` | cuatro iguales |
| | `repeat(auto-fit, minmax(14rem, 1fr))` | **tantas columnas de al menos 14 rem como entren** |
| `gap` | `1rem` | espacio entre filas y columnas |
| `align-items` / `justify-items` | `end` / `center` | alinear dentro de cada celda |
| `place-items: center` | | centrar en los dos ejes (atajo) |
| `grid-column: span 2` (en un hijo) | | ocupa dos columnas |
| `grid-column-start: 4` (en un hijo) | | empieza en la columna 4 |
| `grid-template-areas` | `"cabecera cabecera" "menu contenido"` | dibujar el layout con nombres (misión 2) |

#### ¿Flex o Grid?
- **Flex**: una sola dirección; el contenido manda (barras, filas, botones).
- **Grid**: filas **y** columnas; el layout manda (grillas de tarjetas, páginas). Se combinan: la grilla de cursos es Grid y cada tarjeta adentro usa Flex.

#### `auto-fit` y sus límites
`repeat(auto-fit, minmax(14rem, 1fr))` es responsive **sin media queries**: 1 columna en el celular, 5 en una pantalla ancha. Pero no elige *cuántas* querés: en la captura de escritorio la sexta tarjeta queda sola en su fila. Para decidir exactamente "1 en el celular, 2 en la tablet, 4 en la computadora" hacen falta **media queries** («Responsive: celular primero»).

#### El ejemplo

Grilla de 6 cursos con `auto-fit`, dos tarjetas en dos columnas y el podio del Hall of Fame (tres columnas apoyadas abajo, la del medio más alta y con brillo dorado).

#### Cómo se ve el ejemplo

Celular: cursos en una columna, dos tarjetas lado a lado y el podio 2–1–3 con el primero más alto. Escritorio: cinco cursos por fila y el sexto solo, y el podio estirado a todo el ancho.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Grid: cursos y podio</title>
    <style>
      /* 09 - Grid */
      :root {
        --fondo: #0b1220;
        --panel: #111a2e;
        --borde: #1f2a44;
        --texto: #e2e8f0;
        --apagado: #94a3b8;
        --neon: #22d3ee;
        --oro: #fbbf24;
        --plata: #cbd5e1;
        --bronce: #d97742;
        --mono: ui-monospace, "JetBrains Mono", Consolas, monospace;
      }

      *,
      *::before,
      *::after {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        padding: 1.25rem;
        background: var(--fondo);
        color: var(--texto);
        font-family: system-ui, "Segoe UI", Roboto, sans-serif;
      }

      h1 {
        font-size: 1.5rem;
      }

      .subtitulo {
        margin-top: 2.5rem;
        color: var(--neon);
        font-size: 1.125rem;
      }

      .curso {
        padding: 1rem;
        background: var(--panel);
        border: 1px solid var(--borde);
        border-radius: 0.75rem;
      }

      .curso h2 {
        margin: 0.25rem 0;
        font-size: 1rem;
      }

      .curso p {
        margin: 0;
        color: var(--apagado);
        font-size: 0.8rem;
      }

      .mod {
        font-family: var(--mono);
      }

      /* 1) auto-fit + minmax: tantas columnas de al menos 14rem como entren */
      .grilla-cursos {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
        gap: 1rem;
      }

      /* 2) Dos columnas iguales: 1fr = una fraccion del espacio libre */
      .dos-columnas {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
      }

      /* 3) Podio */
      .podio {
        display: grid;
        grid-template-columns: 1fr 1.2fr 1fr; /* el del medio, un poco mas ancho */
        align-items: end; /* todos apoyados abajo */
        gap: 0.5rem;
        margin: 0;
        padding: 0;
        list-style: none;
      }

      .lugar {
        display: grid;
        justify-items: center; /* centra cada pieza en su celda */
        gap: 0.375rem;
        padding: 1rem 0.5rem;
        background: var(--panel);
        border: 2px solid var(--borde);
        border-radius: 0.75rem;
        font-size: 0.8rem;
        text-align: center;
      }

      .lugar strong {
        font-family: var(--mono);
        color: var(--neon);
      }

      .primero {
        padding-block: 2rem; /* padding arriba y abajo: mas alto */
        border-color: var(--oro);
        box-shadow: 0 0 24px rgb(251 191 36 / 30%);
      }

      .primero strong {
        color: var(--oro);
      }

      .segundo {
        border-color: var(--plata);
      }

      .tercero {
        border-color: var(--bronce);
      }

      .medalla {
        display: grid;
        place-items: center; /* centrado en los dos ejes en una linea */
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        background: var(--borde);
        font-weight: bold;
      }

      .primero .medalla {
        background: var(--oro);
        color: var(--fondo);
      }
    </style>
  </head>
  <body>
    <main>
      <h1>Rutas de entrenamiento</h1>
      <!-- 1) Grilla que decide sola cuantas columnas entran -->
      <section class="grilla-cursos" aria-label="Cursos">
        <article class="curso"><p class="mod">MOD-04</p><h2>C++ Moderno</h2><p>18 / 24 nodos</p></article>
        <article class="curso"><p class="mod">MOD-06</p><h2>SDL3 &amp; Game Loops</h2><p>10 / 22 nodos</p></article>
        <article class="curso"><p class="mod">MOD-10</p><h2>OpenGL 4.6</h2><p>3 / 16 nodos</p></article>
        <article class="curso"><p class="mod">MOD-13</p><h2>WebAssembly</h2><p>5 / 19 nodos</p></article>
        <article class="curso"><p class="mod">MOD-17</p><h2>Python</h2><p>14 / 20 nodos</p></article>
        <article class="curso"><p class="mod">MOD-20</p><h2>Spring Boot</h2><p>16 / 24 nodos</p></article>
      </section>

      <!-- 2) Dos columnas fijas: las tarjetas chicas de la version celular -->
      <h2 class="subtitulo">Más rutas</h2>
      <div class="dos-columnas">
        <article class="curso chico"><p class="mod">MOD-23</p><h2>TypeScript Pro</h2></article>
        <article class="curso chico"><p class="mod">MOD-20</p><h2>Spring Boot Cloud</h2></article>
      </div>

      <!-- 3) Podio: tres columnas, el del medio mas alto -->
      <h2 class="subtitulo">Hall of Fame</h2>
      <ol class="podio">
        <li class="lugar segundo"><span class="medalla">2</span>@DevValkyrie<strong>13.200 XP</strong></li>
        <li class="lugar primero"><span class="medalla">1</span>@NeoCoder_X<strong>14.850 XP</strong></li>
        <li class="lugar tercero"><span class="medalla">3</span>@GlitchHunter<strong>12.450 XP</strong></li>
      </ol>
    </main>
  </body>
</html>
```

### ¿Para qué sirve?

Las galerías de fotos, los catálogos de una tienda, un tablero de estadísticas, un calendario, el diseño general de una página (cabecera, menú, contenido, pie): todo lo que tiene filas **y** columnas se arma con grid. Con una sola línea (`repeat(auto-fill, minmax(…))`) la grilla se acomoda sola a cualquier pantalla.

### Errores habituales

**Orco del Desborde: `minmax(20rem, 1fr)` en el celular.** Si la columna mínima es más ancha que la pantalla (390 px ≈ 24 rem menos los márgenes), se sale. Usá mínimos chicos o `minmax(min(20rem, 100%), 1fr)`.

**Ogro: `grid-template-columns` en el hijo.** Va en el **contenedor**.

**Ogro: áreas mal dibujadas.** En `grid-template-areas` cada fila tiene que tener la misma cantidad de nombres y cada área tiene que ser un rectángulo; si no, DevTools tacha la propiedad.

### Prueba del sello

#### ¿Qué es `1fr`? ¿Qué hace `repeat(3, 1fr)`?

`fr` es una **fracción del espacio libre**. `repeat(3, 1fr)` arma tres columnas que se reparten el ancho en partes iguales; `1fr 2fr` haría la segunda el doble de ancha.

#### ¿Qué ventaja y qué límite tiene `auto-fit` con `minmax`?

La ventaja: la grilla pone **tantas columnas como entren** sin escribir media queries (`repeat(auto-fit, minmax(12rem, 1fr))`). El límite: no podés elegir exactamente cuántas columnas querés en cada pantalla; para eso se usan media queries.

#### ¿Cuándo usarías Flex y cuándo Grid?

Flex para **una dirección**: una fila o una columna de cosas (una barra, los botones, una tarjeta por dentro). Grid para **dos dimensiones**: filas y columnas a la vez (una galería, un tablero, el esqueleto de la página).

### Micro-misión R02-N04-P1 · Doce vitrales para Kaffa

```meta
lugar: La mesa de los encargos de Kaffa
personajes: Iris, Tesela
carta: display: grid | una malla de filas y columnas · grid-template-columns: repeat(3, 1fr)
recompensa: xp 10, oro 10
```

#### Escena
Llega una carta de **Kaffa**, el Arquitecto Imperial: «Doce vitrales iguales, alineados en filas y columnas perfectas». Teo propone hacer uno de otro color. Nadie le contesta.
—Con la regla flexible hacés filas —dice {mentor}—, pero no **cuadrículas**. Para Kaffa, la **malla**.

#### Gheco sugiere
`display: grid` arma una malla, y `grid-template-columns: repeat(3, 1fr)` hace tres columnas iguales (`1fr` es «una parte»).

#### Desafío
En `.vitrales`, poné `display: grid` y `grid-template-columns: repeat(3, 1fr)`.

#### Código inicial
```html
<style>
  .vitrales div { padding: 1rem; background-color: #7c3aed; color: #fff; }
</style>
<div class="vitrales">
  <div>1</div><div>2</div><div>3</div>
  <div>4</div><div>5</div><div>6</div>
</div>
```

#### Inspector
```
css .vitrales { display }
css .vitrales { grid-template-columns }
```

#### Salida esperada
```
css .vitrales { display }: grid
css .vitrales { grid-template-columns }: repeat(3, 1fr)
```

#### Solución
```html
<style>
  .vitrales { display: grid; grid-template-columns: repeat(3, 1fr); }
  .vitrales div { padding: 1rem; background-color: #7c3aed; color: #fff; }
</style>
<div class="vitrales">
  <div>1</div><div>2</div><div>3</div>
  <div>4</div><div>5</div><div>6</div>
</div>
```

#### Al superarla
Los vitrales se ordenan en filas de tres. Kaffa no los vio todavía, pero Iris ya se imagina su cara.

#### Imagen
- Una pared con vitrales violetas acomodados en una cuadrícula perfecta de tres columnas.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) los mira.
- Tesela (22, pelo corto iridiscente violeta y cian, monóculo de cristal tallado, sobretodo largo negro con fragmentos de vidrio de colores cosidos) con la carta de Kaffa en la mano.

### Micro-misión R02-N04-P2 · El plomo entre vitral y vitral

```meta
lugar: La mesa de los encargos de Kaffa
personajes: Iris, Gheco
carta: gap en grid | gap: el espacio entre filas y columnas · sin márgenes en cada hijo
recompensa: xp 10, oro 10
```

#### Escena
Los vitrales quedaron pegados unos con otros. Kaffa pidió una franja de plomo pareja entre todos.

#### Gheco sugiere
En una malla, `gap` deja el mismo espacio entre filas y entre columnas, sin tocar los hijos.

#### Desafío
Agregale a `.vitrales` un `gap` de `0.75rem`.

#### Código inicial
```html
<style>
  .vitrales { display: grid; grid-template-columns: repeat(3, 1fr); }
  .vitrales div { padding: 1rem; background-color: #7c3aed; color: #fff; }
</style>
<div class="vitrales">
  <div>1</div><div>2</div><div>3</div>
  <div>4</div><div>5</div><div>6</div>
</div>
```

#### Inspector
```
css .vitrales { gap }
```

#### Salida esperada
```
css .vitrales { gap }: 0.75rem
```

#### Solución
```html
<style>
  .vitrales { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; }
  .vitrales div { padding: 1rem; background-color: #7c3aed; color: #fff; }
</style>
<div class="vitrales">
  <div>1</div><div>2</div><div>3</div>
  <div>4</div><div>5</div><div>6</div>
</div>
```

#### Al superarla
Una franja de plomo pareja separa cada vitral. Gheco camina por las franjas como por un laberinto.

#### Imagen
- Una cuadrícula de vitrales violetas separados por franjas de plomo iguales.
- Gheco (gecko de luz con antiparras) camina por las franjas.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) sonríe.

### Micro-misión R02-N04-P3 · Tantas columnas como entren

```meta
lugar: La mesa de los encargos de Kaffa
personajes: Iris, Tesela
carta: auto-fit y minmax | repeat(auto-fit, minmax(10rem, 1fr)) · entran las columnas que quepan, sin @media
recompensa: xp 10, oro 10
```

#### Escena
—En la catedral de Kaffa hay ventanas anchas y angostas —dice {mentor}—. No le vamos a hacer una malla para cada una.

#### Gheco sugiere
`repeat(auto-fit, minmax(10rem, 1fr))`: cada columna mide al menos `10rem`, y entran todas las que quepan.

#### Desafío
Cambiá el `grid-template-columns` de `.vitrales` por `repeat(auto-fit, minmax(10rem, 1fr))`.

#### Código inicial
```html
<style>
  .vitrales { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; }
  .vitrales div { padding: 1rem; background-color: #7c3aed; color: #fff; }
</style>
<div class="vitrales">
  <div>1</div><div>2</div><div>3</div>
  <div>4</div><div>5</div><div>6</div>
</div>
```

#### Inspector
```
css .vitrales { grid-template-columns }
```

#### Salida esperada
```
css .vitrales { grid-template-columns }: repeat(auto-fit, minmax(10rem, 1fr))
```

#### Solución
```html
<style>
  .vitrales { display: grid; grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr)); gap: 0.75rem; }
  .vitrales div { padding: 1rem; background-color: #7c3aed; color: #fff; }
</style>
<div class="vitrales">
  <div>1</div><div>2</div><div>3</div>
  <div>4</div><div>5</div><div>6</div>
</div>
```

#### Al superarla
En *Celular* se ven de a dos; en *Compu*, de a seis. La misma malla. {mentor} asiente una sola vez.

#### Imagen
- Dos ventanas, una angosta y una ancha, con la misma cuadrícula de vitrales acomodada distinto.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) compara las dos.
- Tesela (22, pelo corto iridiscente violeta y cian, monóculo de cristal tallado, sobretodo largo negro con fragmentos de vidrio de colores cosidos) asiente.

### Micro-misión R02-N04-P4 · El podio de los campeones

```meta
lugar: La mesa de los encargos de Kaffa
personajes: Iris, Teo
carta: align-items: end | en la malla, alinea los hijos abajo · el podio: el del medio más alto
recompensa: xp 10, oro 10
```

#### Escena
Abajo del encargo va el podio: tres escalones, el del medio más alto. Pero en la malla los tres quedan colgando de arriba.

#### Gheco sugiere
`align-items: end` en la malla apoya a todos los hijos **abajo**, como escalones sobre el piso.

#### Desafío
Agregale `align-items: end` a `.podio`.

#### Código inicial
```html
<style>
  .podio { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; height: 10rem; }
  .podio div { background-color: #fbbf24; text-align: center; }
  .segundo { height: 6rem; }
  .primero { height: 9rem; }
  .tercero { height: 4rem; }
</style>
<div class="podio">
  <div class="segundo">2</div>
  <div class="primero">1</div>
  <div class="tercero">3</div>
</div>
```

#### Inspector
```
css .podio { align-items }
```

#### Salida esperada
```
css .podio { align-items }: end
```

#### Solución
```html
<style>
  .podio { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; height: 10rem; align-items: end; }
  .podio div { background-color: #fbbf24; text-align: center; }
  .segundo { height: 6rem; }
  .primero { height: 9rem; }
  .tercero { height: 4rem; }
</style>
<div class="podio">
  <div class="segundo">2</div>
  <div class="primero">1</div>
  <div class="tercero">3</div>
</div>
```

#### Al superarla
Los tres escalones se apoyan en el piso. Teo se sube al del medio para la foto.

#### Imagen
- Un podio dorado de tres escalones, el del medio más alto.
- Teo (15, flaco, pelo negro enrulado con purpurina, pecas, delantal manchado de todos los colores, cinturón con frascos de vidrio molido) subido al escalón del medio, haciendo pose.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) se ríe.

### Misión R02-N04-M1 · La galería de insignias

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá una galería de insignias **cuadradas** (`aspect-ratio: 1`) que se acomode sola con `repeat(auto-fill, minmax(…))`, y una insignia especial que ocupe **dos columnas**.

#### Criterio de aprobación

- La grilla usa `repeat(auto-fill, minmax(…, 1fr))`.
- Las insignias son cuadradas con `aspect-ratio: 1`.
- Una ocupa dos columnas (`grid-column: span 2`).

#### Cómo debe quedar

celular: capturas/R02-N04-M1-celular.webp
compu: capturas/R02-N04-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La galería de insignias</title>
    <style>

    </style>
  </head>
  <body>

  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Galería de insignias</title>
    <style>
      body {
        margin: 0;
        padding: 1.25rem;
        background: #0b1220;
        color: #e2e8f0;
        font-family: system-ui, sans-serif;
      }
      .insignias {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(6rem, 1fr));
        gap: 0.75rem;
        padding: 0;
        list-style: none;
      }
      .insignias li {
        display: grid;
        place-items: center;
        aspect-ratio: 1; /* cuadradas */
        border: 1px solid #1f2a44;
        border-radius: 1rem;
        font-size: 2rem;
      }
      /* Una insignia especial ocupa dos columnas */
      .insignias .grande {
        grid-column: span 2;
        aspect-ratio: auto;
        border-color: #fbbf24;
      }
    </style>
  </head>
  <body>
    <h1>Insignias</h1>
    <ul class="insignias">
      <li class="grande"><span aria-hidden="true">🏆</span> Campeona</li>
      <li><span role="img" aria-label="fuego">🔥</span></li>
      <li><span role="img" aria-label="rayo">⚡</span></li>
      <li><span role="img" aria-label="gema">💎</span></li>
      <li><span role="img" aria-label="espada">⚔️</span></li>
      <li><span role="img" aria-label="escudo">🛡️</span></li>
    </ul>
  </body>
</html>
```


### Misión R02-N04-M2 · El layout con áreas

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá el esqueleto de una página con **cabecera, menú lateral, contenido y pie**, usando `grid-template-areas` con nombres.

#### Criterio de aprobación

- Usa `grid-template-areas` y cada zona tiene su `grid-area`.
- Las cuatro zonas son etiquetas semánticas (`header`, `nav` o `aside`, `main`, `footer`).

#### Cómo debe quedar

celular: capturas/R02-N04-M2-celular.webp
compu: capturas/R02-N04-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El layout con áreas</title>
    <style>

    </style>
  </head>
  <body>

  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Layout con áreas</title>
    <style>
      * {
        box-sizing: border-box;
      }
      body {
        margin: 0;
        min-height: 100vh;
        display: grid;
        /* El "dibujo" del layout: cada palabra es un area */
        grid-template-areas:
          "cabecera cabecera"
          "menu     contenido"
          "pie      pie";
        grid-template-columns: 12rem 1fr;
        grid-template-rows: auto 1fr auto;
        font-family: system-ui, sans-serif;
      }
      header { grid-area: cabecera; background: #1e293b; color: white; padding: 1rem; }
      nav { grid-area: menu; background: #e2e8f0; padding: 1rem; }
      main { grid-area: contenido; padding: 1rem; }
      footer { grid-area: pie; background: #1e293b; color: white; padding: 1rem; }
    </style>
  </head>
  <body>
    <header>Cabecera</header>
    <nav aria-label="Lateral">Menú lateral</nav>
    <main>Contenido principal</main>
    <footer>Pie</footer>
  </body>
</html>
```


### Encargo R02-N04-E1 · El calendario de octubre

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Armá el calendario de **octubre de 2026**: 7 columnas con los encabezados L a D, el día 1 cae **jueves** (`grid-column-start: 4`) y el 12 está marcado como feriado.

#### Criterio de aprobación

- Siete columnas iguales con sus encabezados.
- El 1 arranca en la cuarta columna.
- El 12 se distingue como feriado.

#### Cómo debe quedar

celular: capturas/R02-N04-E1-celular.webp
compu: capturas/R02-N04-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El calendario de octubre</title>
    <style>

    </style>
  </head>
  <body>

  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Calendario de octubre</title>
    <style>
      body {
        margin: 0;
        padding: 1rem;
        font-family: system-ui, sans-serif;
      }
      .mes {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 4px;
        max-width: 28rem;
        padding: 0;
        list-style: none;
      }
      .mes li {
        padding: 0.5rem 0;
        text-align: center;
        background: #f1f5f9;
        border-radius: 0.375rem;
      }
      .mes .dia-semana {
        background: none;
        font-weight: bold;
      }
      /* Octubre de 2026 empieza en jueves: el 1 va en la columna 4 */
      .mes .primero {
        grid-column-start: 4;
      }
      .mes .feriado {
        background: #fecaca;
      }
    </style>
  </head>
  <body>
    <h1>Octubre 2026</h1>
    <ol class="mes">
      <li class="dia-semana">L</li><li class="dia-semana">M</li><li class="dia-semana">M</li><li class="dia-semana">J</li><li class="dia-semana">V</li><li class="dia-semana">S</li><li class="dia-semana">D</li>
      <li class="primero">1</li><li>2</li><li>3</li><li>4</li><li>5</li><li>6</li><li>7</li><li>8</li><li>9</li><li>10</li><li>11</li><li class="feriado">12</li><li>13</li><li>14</li><li>15</li><li>16</li><li>17</li><li>18</li><li>19</li><li>20</li><li>21</li><li>22</li><li>23</li><li>24</li><li>25</li><li>26</li><li>27</li><li>28</li><li>29</li><li>30</li><li>31</li>
    </ol>
  </body>
</html>
```

## R02-N05 · Responsive: celular primero

```meta
tipo: tema
padre: R02-N04
precio: 10
criatura: troll
temas: css.responsive, css.posicion
usa: css.grid, css.flexbox
```

### Crónica

El **Ogro de la Cascada** golpea la puerta del taller con un desafío: el mismo vitral tiene que verse bien en la ventanita de una cabaña **y** en el ventanal del castillo. Si en alguno se rompe, el taller es suyo.

Iris prueba primero en el castillo, como siempre. Queda precioso. {mentor} no dice nada: le alcanza un **espejito de bolsillo**. En el espejito, la ventanita de la cabaña, todo está amontonado.

—Empezá por la ventana **chica** —le dice—. Agrandar es fácil; achicar algo grande, casi imposible.

### Objetivos

Diseñar **primero para el celular** y después agregar cambios para pantallas más grandes con **media queries** `min-width`. Usar posiciones `sticky` y `fixed`, tamaños fluidos con `clamp()` e imágenes que no se desbordan.

### Antes de empezar

- Flexbox («Flexbox») y Grid («Grid»).

### Explicación

#### Mobile first
1. Los estilos **sin** media query son los del **celular** (la base).
2. Cada `@media (min-width: X)` **agrega o cambia** algo a partir de ese ancho.

```css
.grilla { grid-template-columns: 1fr; }                   /* celular */
@media (min-width: 40rem) { .grilla { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 64rem) { .grilla { grid-template-columns: repeat(4, 1fr); } }
```
¿Por qué así y no al revés (`max-width`)? Porque el celular es lo más restrictivo y lo que más se usa: si funciona ahí, agrandar es sumar columnas. Y los estilos del celular no cargan con reglas de escritorio que después hay que "deshacer".

**Puntos de quiebre** (*breakpoints*) usados en el curso (los mismos de Tailwind): `40rem` (640 px, tablet), `48rem` (768 px), `64rem` (1024 px), `80rem` (1280 px).

#### Qué cambia en la plataforma
| Pieza | Celular | Computadora |
|---|---|---|
| menú | barra **fija abajo** (`position: fixed`) | menú arriba, en la cabecera |
| hero | texto y login uno abajo del otro | dos columnas (`1.4fr 1fr`) |
| cursos | 1 columna | 2 (tablet) → 4 |
| título | 1.75 rem | crece hasta 3.25 rem (`clamp`) |

#### Posiciones
| `position` | Comportamiento |
|---|---|
| `static` | normal (por defecto) |
| `relative` | normal, pero sirve de **referencia** para los `absolute` de adentro |
| `absolute` | sale del flujo y se ubica respecto del ancestro `relative` |
| `fixed` | fijo a la **ventana**: no se mueve con el scroll (barra inferior) |
| `sticky` | normal hasta que llega al borde, y ahí se queda pegado (cabecera) |

Se ubican con `top`/`right`/`bottom`/`left` o el atajo `inset`. `z-index` decide quién queda encima. Un elemento `fixed` **tapa** contenido: por eso el `body` lleva un `padding-bottom` igual al alto de la barra.

#### Más herramientas
- `clamp(1.75rem, 1rem + 3vw, 3.25rem)`: tamaño **fluido** con mínimo y máximo (`vw` = 1 % del ancho de la ventana).
- `img { max-width: 100%; height: auto; }`: ninguna imagen se sale de su caja.
- `max-width: 80rem; margin: 0 auto;` en el `main`: en pantallas enormes el contenido no se estira de lado a lado.

#### El ejemplo

La plataforma en miniatura. Abajo de todo, un indicador dice en qué tramo de ancho estás.

**Probalo**: DevTools → modo dispositivo (Ctrl+Shift+M) → arrastrá el borde: a 640, 768 y 1024 px cambian la grilla, el menú y el hero.

#### Cómo se ve el ejemplo

Tocá *Celular* y *Compu* en la vista previa: . Celular: cabecera pegada arriba, todo en una columna, barra de 4 íconos fija abajo (en la captura de página completa aparece a la altura de la pantalla, que es donde la ve el usuario) y "celular (menos de 40rem)". Escritorio: menú en la cabecera, sin barra inferior, hero en dos columnas, 4 cursos por fila y "pantalla grande (64rem o más)".

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Mobile first: de la cabaña al ventanal</title>
    <style>
      /* 10 - Responsive mobile first
         1) Primero se escriben los estilos del CELULAR (sin media query).
         2) Despues, con @media (min-width: ...), se AGREGA lo de pantallas mas grandes. */
      :root {
        --fondo: #0b1220;
        --panel: #111a2e;
        --borde: #1f2a44;
        --texto: #e2e8f0;
        --apagado: #94a3b8;
        --neon: #22d3ee;
        --alto-barra: 4rem;
      }

      *,
      *::before,
      *::after {
        box-sizing: border-box;
      }

      img {
        max-width: 100%; /* ninguna imagen mas ancha que su contenedor */
        height: auto;
      }

      body {
        margin: 0;
        background: var(--fondo);
        color: var(--texto);
        font-family: system-ui, "Segoe UI", Roboto, sans-serif;
        line-height: 1.5;
        /* Lugar para que la barra fija no tape el final de la pagina */
        padding-bottom: var(--alto-barra);
      }

      a {
        color: inherit;
        text-decoration: none;
      }

      .neon {
        color: var(--neon);
      }

      .apagado {
        color: var(--apagado);
      }

      /* ===== CELULAR (base) ===== */

      .cabecera {
        position: sticky; /* se queda pegada arriba al hacer scroll */
        top: 0;
        z-index: 10;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding: 0.75rem 1rem;
        background: rgb(11 18 32 / 90%);
        border-bottom: 1px solid var(--borde);
      }

      .marca {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 800;
      }

      .menu-superior {
        display: none; /* en el celular no hay lugar: se usa la barra de abajo */
      }

      .stats {
        margin: 0;
        font-size: 0.85rem;
      }

      main {
        width: 100%;
        max-width: 80rem; /* en pantallas enormes no se estira de mas */
        margin: 0 auto;
        padding: 1.25rem 1rem;
      }

      .hero {
        display: grid;
        gap: 1.5rem; /* una sola columna */
      }

      h1 {
        margin: 0 0 0.75rem;
        /* clamp(minimo, preferido, maximo): crece con la ventana pero con limites */
        font-size: clamp(1.75rem, 1rem + 3vw, 3.25rem);
        line-height: 1.15;
      }

      .panel-login,
      .tarjeta {
        padding: 1rem;
        background: var(--panel);
        border: 1px solid var(--borde);
        border-radius: 0.75rem;
      }

      .grilla {
        display: grid;
        grid-template-columns: 1fr; /* 1 columna en el celular */
        gap: 1rem;
      }

      .barra-inferior {
        position: fixed; /* fija a la ventana, no se mueve con el scroll */
        inset: auto 0 0 0; /* top right bottom left: pegada abajo, de lado a lado */
        z-index: 10;
        display: flex;
        height: var(--alto-barra);
        background: var(--panel);
        border-top: 1px solid var(--borde);
      }

      .barra-inferior a {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        color: var(--apagado);
      }

      .barra-inferior a[aria-current="page"] {
        color: var(--neon);
      }

      /* Muestra en que tramo estamos (solo para aprender) */
      .indicador::after {
        content: "celular (menos de 40rem)";
        color: var(--neon);
      }

      /* ===== TABLET: desde 40rem (640 px) ===== */
      @media (min-width: 40rem) {
        .grilla {
          grid-template-columns: repeat(2, 1fr);
        }

        .indicador::after {
          content: "tablet (40rem o más)";
        }
      }

      /* ===== COMPUTADORA CHICA: desde 48rem (768 px) ===== */
      @media (min-width: 48rem) {
        .menu-superior {
          display: flex;
          gap: 1.5rem;
        }

        .barra-inferior {
          display: none; /* ya hay menu arriba */
        }

        body {
          padding-bottom: 0;
        }

        .indicador::after {
          content: "computadora (48rem o más)";
        }
      }

      /* ===== COMPUTADORA: desde 64rem (1024 px) ===== */
      @media (min-width: 64rem) {
        .hero {
          grid-template-columns: 1.4fr 1fr; /* texto a la izquierda, login a la derecha */
          align-items: center;
        }

        .grilla {
          grid-template-columns: repeat(4, 1fr);
        }

        .indicador::after {
          content: "pantalla grande (64rem o más)";
        }
      }

      .marca img {
        border-radius: 0.5rem;
      }
    </style>
  </head>
  <body>
    <header class="cabecera">
      <a class="marca" href="#">
        <img src="/img/cursos/html/gheco-logo.webp" alt="" width="36" height="36">
        GhecoSoft <span class="neon">-Code</span>
      </a>
      <!-- Menu de arriba: escondido en el celular, visible desde 48rem -->
      <nav class="menu-superior" aria-label="Principal">
        <a href="#cursos">Cursos</a>
        <a href="#fama">Top 10</a>
        <a href="#">Bóveda</a>
      </nav>
      <p class="stats">⚡ 1.450 · 🔥 12</p>
    </header>

    <main>
      <section class="hero" aria-labelledby="titulo">
        <div>
          <h1 id="titulo">Aprendé a programar avanzando por tu <span class="neon">árbol de habilidades</span>.</h1>
          <p>Compilá algoritmos reales y competí por el rango Supremo.</p>
        </div>
        <!-- En el celular va debajo; en la computadora, a la derecha -->
        <div class="panel-login">
          <p><strong>Entrá a tu cuenta</strong></p>
          <p class="apagado">(el formulario completo está en el nodo «El panel central: hero y acceso»)</p>
        </div>
      </section>

      <section id="cursos" aria-labelledby="titulo-cursos">
        <h2 id="titulo-cursos">Rutas de entrenamiento</h2>
        <div class="grilla">
          <article class="tarjeta">C++ Moderno</article>
          <article class="tarjeta">SDL3 &amp; Game Loops</article>
          <article class="tarjeta">OpenGL 4.6</article>
          <article class="tarjeta">WebAssembly</article>
          <article class="tarjeta">Python</article>
          <article class="tarjeta">Spring Boot</article>
          <article class="tarjeta">TypeScript</article>
          <article class="tarjeta">Phaser</article>
        </div>
      </section>

      <section id="fama" aria-labelledby="titulo-fama">
        <h2 id="titulo-fama">Hall of Fame</h2>
        <p class="apagado">Ancho de la ventana: <span class="indicador"></span></p>
      </section>
    </main>

    <!-- Barra inferior: SOLO en el celular, fija abajo -->
    <nav class="barra-inferior" aria-label="Secciones">
      <a href="#cursos">🗺<span>Campañas</span></a>
      <a href="#">📖<span>Lecciones</span></a>
      <a href="#fama" aria-current="page">⚔<span>Arena</span></a>
      <a href="#">🌳<span>Árbol</span></a>
    </nav>
  </body>
</html>
```

### ¿Para qué sirve?

Más de la mitad de las visitas a cualquier sitio llegan desde un celular. Un diseño adaptable (*responsive*) es la diferencia entre una página que se usa y una que se cierra a los tres segundos. Las barras fijas, los menús que se pegan arriba y los títulos que crecen con la pantalla son parte del día a día de cualquier diseño web.

### Errores habituales

**Ogro: falta el `meta viewport`**: el celular simula una pantalla de ~980 px y aplica las media queries **de escritorio**.

**Troll: la barra fija tapa el final de la página**: falta el `padding-bottom` en el `body`.

**Ogro: media queries en desorden**: con `min-width`, van de la más chica a la más grande; si `64rem` está antes que `40rem`, la de 40 la pisa (misma especificidad, gana la de más abajo).

**Orco del Desborde: scroll horizontal en el celular**. En DevTools, buscá qué elemento es más ancho que la pantalla (suele ser una imagen, una tabla o un `width` fijo).

### Prueba del sello

#### ¿Qué significa *mobile first* y por qué se usa `min-width`?

Que el CSS **sin `@media`** es el del celular, y lo que se agrega para pantallas más grandes va en `@media (min-width: …)`: "desde este ancho en adelante". Es más fácil agregar columnas que quitarlas, y el celular carga solo lo que necesita.

#### ¿Qué diferencia hay entre `fixed` y `sticky`?

`fixed` saca la caja del flujo y la deja **siempre** en el mismo lugar de la ventana (puede tapar contenido). `sticky` se comporta normal hasta que llega a un borde al hacer scroll, y ahí **se pega** mientras su contenedor esté a la vista.

#### ¿Qué hace `clamp()`?

Da un valor que **crece con la pantalla pero con límites**: `clamp(1.5rem, 5vw, 3rem)` es 5 % del ancho, pero nunca menos de 1,5 rem ni más de 3 rem. Ideal para títulos.

### Micro-misión R02-N05-P1 · La ventanita de la cabaña

```meta
lugar: La cabaña y el castillo
personajes: Iris, Tesela
carta: viewport | <meta name="viewport" content="width=device-width, initial-scale=1"> · sin esto el celular achica la página de escritorio
recompensa: xp 10, oro 10
```

#### Escena
El **Ogro de la Cascada** desafía al taller: el mismo vitral tiene que verse bien en la ventanita de una cabaña **y** en el ventanal del castillo. Iris prueba primero en el castillo, como siempre. {mentor} no dice nada: le alcanza un **espejito de bolsillo**. En el espejito, todo se ve diminuto.

#### Gheco sugiere
Sin la etiqueta `<meta name="viewport" content="width=device-width, initial-scale=1">`, el celular muestra la versión de compu achicada.

#### Desafío
Agregá en el `head` la etiqueta `meta` del viewport con `width=device-width, initial-scale=1`.

#### Código inicial
```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <title>El vitral de la cabaña</title>
  </head>
  <body>
    <h1>Un vitral para todas las ventanas</h1>
  </body>
</html>
```

#### Inspector
```
meta[name="viewport"] @content
```

#### Salida esperada
```
meta[name="viewport"] @content: width=device-width, initial-scale=1
```

#### Solución
```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El vitral de la cabaña</title>
  </head>
  <body>
    <h1>Un vitral para todas las ventanas</h1>
  </body>
</html>
```

#### Al superarla
En el espejito, el vitral se ve de su tamaño. {mentor} le deja el espejito en la mesa.

#### Imagen
- Una cabaña chiquita y un castillo enorme, uno al lado del otro, con el mismo vitral.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) mira un espejito de bolsillo.
- Tesela (22, pelo corto iridiscente violeta y cian, monóculo de cristal tallado, sobretodo largo negro con fragmentos de vidrio de colores cosidos) se lo alcanza.

### Micro-misión R02-N05-P2 · Agrandar es fácil

```meta
lugar: La cabaña y el castillo
personajes: Iris, Tesela
carta: @media | celular primero: el CSS de base es el chico · @media (min-width: 768px) { … } agrega lo de la pantalla grande
recompensa: xp 10, oro 10
```

#### Escena
—Empezá por la ventana **chica** —le dice {mentor}—. Agrandar es fácil; achicar algo grande, casi imposible.

#### Gheco sugiere
El CSS de base es para el celular. Lo de pantallas grandes se **agrega** adentro de `@media (min-width: 768px) { … }`.

#### Desafío
Agregá un `@media (min-width: 768px)` que ponga `.grilla` con `grid-template-columns: repeat(2, 1fr)`.

#### Código inicial
```html
<style>
  .grilla { display: grid; gap: 1rem; }
  .grilla div { padding: 1rem; background-color: #22d3ee; }
</style>
<div class="grilla">
  <div>Cabaña</div>
  <div>Castillo</div>
</div>
```

#### Inspector
```
css .grilla { grid-template-columns }
css @media (min-width: 768px) | .grilla { grid-template-columns }
```

#### Salida esperada
```
css .grilla { grid-template-columns }: (no hay)
css @media (min-width: 768px) | .grilla { grid-template-columns }: repeat(2, 1fr)
```

#### Solución
```html
<style>
  .grilla { display: grid; gap: 1rem; }
  .grilla div { padding: 1rem; background-color: #22d3ee; }
  @media (min-width: 768px) {
    .grilla { grid-template-columns: repeat(2, 1fr); }
  }
</style>
<div class="grilla">
  <div>Cabaña</div>
  <div>Castillo</div>
</div>
```

#### Al superarla
En *Celular*, uno debajo del otro; en *Compu*, de a dos. Iris lo prueba primero en el espejito. Sin que nadie se lo diga.

#### Imagen
- Un vitral que en la cabaña tiene sus piezas apiladas y en el castillo, lado a lado.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) con el espejito en la mano.
- Tesela (22, pelo corto iridiscente violeta y cian, monóculo de cristal tallado, sobretodo largo negro con fragmentos de vidrio de colores cosidos) sonríe apenas.

### Micro-misión R02-N05-P3 · La imagen que no entra

```meta
lugar: La cabaña y el castillo
personajes: Iris, Gheco
criatura: orco
carta: Imágenes flexibles | img { max-width: 100%; height: auto; } · nunca más ancha que su caja
recompensa: xp 10, oro 10
```

#### Escena
En la ventanita de la cabaña, la imagen del vitral es más ancha que la pared y aparece una barra para arrastrar de costado. Por la rendija asoma un **orco**.

#### Gheco sugiere
`max-width: 100%` hace que la imagen nunca sea más ancha que su caja, y `height: auto` mantiene la proporción.

#### Desafío
Escribí una regla para `img` con `max-width: 100%` y `height: auto`.

#### Código inicial
```html
<style>

</style>
<img src="/img/cursos/html/heroe-896.webp" alt="El aprendiz con su buzo de circuitos" width="896" height="896">
```

#### Inspector
```
css img { max-width }
css img { height }
```

#### Salida esperada
```
css img { max-width }: 100%
css img { height }: auto
```

#### Solución
```html
<style>
  img { max-width: 100%; height: auto; }
</style>
<img src="/img/cursos/html/heroe-896.webp" alt="El aprendiz con su buzo de circuitos" width="896" height="896">
```

#### Al superarla
La imagen se achica hasta entrar en la pared. El orco se queda sin rendija y se va gruñendo.

#### Imagen
- Una ventanita de cabaña con una imagen que se achica para entrar; un orco se aleja gruñendo.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) con el espejito.
- Gheco (gecko de luz con antiparras) lo señala.

### Micro-misión R02-N05-P4 · La cornisa que acompaña

```meta
lugar: La cabaña y el castillo
personajes: Iris, Nora
carta: position: sticky | se queda pegado al borde al bajar · top: 0 dice dónde se pega
recompensa: xp 10, oro 10
```

#### Escena
El vitral de la cabaña es largo, y al bajar se pierde el menú. Nora, que lo recorre de arriba abajo, no sabe cómo volver.

#### Gheco sugiere
`position: sticky` con `top: 0` deja el elemento en su lugar hasta que llega arriba, y ahí se queda pegado mientras bajás.

#### Desafío
Poné `position: sticky` y `top: 0` en `header`.

#### Código inicial
```html
<style>
  header { background-color: #0f172a; color: #e2e8f0; padding: 1rem; }
  main { height: 2000px; }
</style>
<header>Taller · Encargos · Liga</header>
<main><p>Un vitral muy largo…</p></main>
```

#### Inspector
```
css header { position }
css header { top }
```

#### Salida esperada
```
css header { position }: sticky
css header { top }: 0
```

#### Solución
```html
<style>
  header { position: sticky; top: 0; background-color: #0f172a; color: #e2e8f0; padding: 1rem; }
  main { height: 2000px; }
</style>
<header>Taller · Encargos · Liga</header>
<main><p>Un vitral muy largo…</p></main>
```

#### Al superarla
Nora baja hasta el final y el menú la acompaña. —Así no me pierdo nunca.

#### Imagen
- Un vitral largo con una franja de arriba que se queda fija mientras el resto baja.
- Nora (30, ciega, alta, piel oscura, trenzas finas con un broche de vidrio, túnica gris perla, guantes sin dedos, bastón de vidrio) recorre el vitral con la mano.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) al lado.

### Misión R02-N05-M1 · La galería 1-2-3-6

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá una galería que tenga **1 columna** en el celular, **2** desde 30 rem, **3** desde 48 rem y **6** desde 80 rem. Escribí primero el CSS del celular y después las media queries con `min-width`.

#### Criterio de aprobación

- El CSS sin `@media` es el del celular (1 columna).
- Las media queries usan `min-width` y van de menor a mayor.
- En *Celular* hay una columna; en *Compu*, varias.

#### Cómo debe quedar

celular: capturas/R02-N05-M1-celular.webp
compu: capturas/R02-N05-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La galería 1-2-3-6</title>
    <style>

    </style>
  </head>
  <body>

  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Galería 1-2-3-6</title>
    <style>
      body {
        margin: 0;
        padding: 1rem;
        font-family: system-ui, sans-serif;
      }
      .galeria {
        display: grid;
        grid-template-columns: 1fr;
        gap: 0.5rem;
        padding: 0;
        list-style: none;
      }
      .galeria li {
        aspect-ratio: 4 / 3;
        display: grid;
        place-items: center;
        background: #e0f2fe;
        border-radius: 0.5rem;
      }
      @media (min-width: 30rem) {
        .galeria { grid-template-columns: repeat(2, 1fr); }
      }
      @media (min-width: 48rem) {
        .galeria { grid-template-columns: repeat(3, 1fr); }
      }
      @media (min-width: 80rem) {
        .galeria { grid-template-columns: repeat(6, 1fr); }
      }
    </style>
  </head>
  <body>
    <h1>Galería</h1>
    <ul class="galeria">
      <li>1</li><li>2</li><li>3</li><li>4</li><li>5</li><li>6</li>
    </ul>
  </body>
</html>
```


### Misión R02-N05-M2 · El menú lateral

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

En el celular, el menú es **una fila con scroll horizontal propio** (sin mover la página); desde 48 rem, pasa a ser **una columna a la izquierda** del contenido.

#### Criterio de aprobación

- En el celular el menú usa `overflow-x: auto` y la página no se mueve de costado.
- Desde 48 rem el menú queda en columna al costado del contenido.

#### Cómo debe quedar

celular: capturas/R02-N05-M2-celular.webp
compu: capturas/R02-N05-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El menú lateral</title>
    <style>

    </style>
  </head>
  <body>

  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Menú arriba en el celular, al costado en la computadora</title>
    <style>
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: system-ui, sans-serif;
      }
      .layout {
        display: grid;
        grid-template-columns: 1fr; /* celular: todo apilado */
      }
      nav {
        display: flex;
        gap: 1rem;
        overflow-x: auto; /* si no entran, scroll SOLO en el menu */
        padding: 1rem;
        background: #1e293b;
      }
      nav a {
        color: white;
        white-space: nowrap;
      }
      main {
        padding: 1rem;
      }
      @media (min-width: 48rem) {
        .layout {
          grid-template-columns: 14rem 1fr; /* computadora: menu a la izquierda */
          min-height: 100vh;
        }
        nav {
          flex-direction: column;
        }
      }
    </style>
  </head>
  <body>
    <div class="layout">
      <nav aria-label="Panel">
        <a href="#">Resumen</a>
        <a href="#">Mis cursos</a>
        <a href="#">Insignias</a>
        <a href="#">Configuración</a>
      </nav>
      <main>
        <h1>Panel del alumno</h1>
        <p>Achicá y agrandá la ventana.</p>
      </main>
    </div>
  </body>
</html>
```


### Encargo R02-N05-E1 · Los planes del gimnasio

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Un gimnasio quiere mostrar sus planes: apilados en el celular, tres columnas en la compu con el **plan destacado más alto**, y el título con `clamp()`.

#### Criterio de aprobación

- Apilados en *Celular*, tres columnas en *Compu*.
- El plan destacado se distingue y es más alto.
- El título usa `clamp()`.

#### Cómo debe quedar

celular: capturas/R02-N05-E1-celular.webp
compu: capturas/R02-N05-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Los planes del gimnasio</title>
    <style>

    </style>
  </head>
  <body>

  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Planes de un gimnasio</title>
    <style>
      * { box-sizing: border-box; }
      body {
        margin: 0;
        padding: 1rem;
        font-family: system-ui, sans-serif;
        background: #f8fafc;
      }
      h1 {
        text-align: center;
        font-size: clamp(1.5rem, 1rem + 2vw, 2.5rem);
      }
      .planes {
        display: grid;
        gap: 1rem;
        max-width: 64rem;
        margin: 0 auto;
      }
      .plan {
        padding: 1.5rem;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
      }
      .plan.destacado {
        border: 2px solid #16a34a;
      }
      .precio {
        font-size: 2rem;
        font-weight: bold;
      }
      @media (min-width: 48rem) {
        .planes {
          grid-template-columns: repeat(3, 1fr);
          align-items: center;
        }
        .plan.destacado {
          padding-block: 2.5rem;
        }
      }
    </style>
  </head>
  <body>
    <h1>Planes del Gimnasio Faro</h1>
    <div class="planes">
      <article class="plan"><h2>Básico</h2><p class="precio">$15000</p><p>Sala de musculación.</p></article>
      <article class="plan destacado"><h2>Completo</h2><p class="precio">$25000</p><p>Sala + clases.</p></article>
      <article class="plan"><h2>Libre</h2><p class="precio">$35000</p><p>Todo, todos los días.</p></article>
    </div>
  </body>
</html>
```

## R02-N06 · Jefe: el Ogro de la Cascada

```meta
tipo: jefe
padre: R02-N05
precio: 10
criatura: dragon
insignia: Domador de la Cascada
insignia_descripcion: Venciste al Ogro de la Cascada: sabés qué regla gana y por qué.
usa: css.selectores, css.caja
```

### Crónica

El Ogro de la Cascada perdió el desafío de las ventanas y se vengó: se metió de noche en el **muro de encargos** del taller. Ahora el aviso de Ofidia no se ve, el encargo destacado de Kaffa parece uno más, los botones tienen el texto invisible y el título perdió su color. El ogro está hecho de capas de vidrio que se tapan unas a otras, y lleva un mazo con un `!important` grabado.

—Y lo peor —dice {mentor}— es que **ninguna regla está borrada**. Están todas ahí. Simplemente, otras les ganan. Para echarlo, no se vale `!important` ni tocar el HTML: tenés que entender **quién le gana a quién**.

Cuando Iris termina, el ogro se descascara capa por capa hasta desaparecer. {mentor} se saca el monóculo y lo limpia con la manga, despacio. Iris no entiende por qué. Al día siguiente, en su mesa, hay un monóculo de cristal tallado igual al de {mentor}: **el Monóculo de Cristal**.

### Objetivos

- Encontrar con el inspector por qué una regla no se aplica (tachada con o sin triangulito).
- Arreglar conflictos de especificidad y de orden sin usar `!important`.
- Detectar los valores inválidos que el navegador ignora en silencio.

### Antes de empezar

- Todos los nodos de los Vidrios, sobre todo «Primeros vidrios: CSS» (especificidad) y «El modelo de caja».

### Explicación

#### Cómo se decide qué regla gana
1. **Importancia**: `!important` gana a todo (por eso no se usa: después nadie le puede ganar).
2. **Especificidad**: se cuenta como (ids, clases, elementos). `#muro p` es (1,0,1); `.aviso` es (0,1,0): gana el id, aunque esté antes.
3. **Orden**: con la misma especificidad, gana la que viene **después**.

#### Cómo encontrar al ogro
- Clic derecho → *Inspeccionar* sobre lo que se ve mal. En *Estilos* aparecen todas las reglas que le tocan.
- **Tachada con un triangulito amarillo**: el valor es inválido (un goblin: `2 px`, `colour`).
- **Tachada sin triangulito**: es válida, pero otra le gana (el ogro). Arriba está la ganadora.

#### Cómo ganarle bien
- **Bajar** la especificidad de la regla que gana de más (cambiar `#muro p` por `main p`) suele ser mejor que subir la de todas las demás.
- **Reordenar**: si las dos pesan lo mismo, la que tiene que ganar va después.

### ¿Para qué sirve?

"Puse el estilo y no se aplica" es el problema de CSS más común en cualquier trabajo. En un proyecto grande, con CSS de varias personas, saber leer la cascada en el inspector es lo que te ahorra horas y evita llenar todo de `!important`.

### Errores habituales

El ogro mezcla tres trucos: una regla con **id** que le gana a las clases, una regla que pierde **por el orden** y dos **goblins** (valores inválidos) que el navegador ignora en silencio. El inspector muestra los tres: aprendé a distinguir la tachadura con triangulito de la que no lo tiene.

### Prueba del sello

#### ¿Por qué `#muro p` le gana a `.aviso` aunque esté antes en el CSS?

Porque el orden solo desempata cuando la especificidad es igual. `#muro p` tiene un id (1,0,1) y `.aviso` solo una clase (0,1,0): gana el id esté donde esté.

#### ¿Por qué no conviene arreglarlo con `!important`?

Porque `!important` le gana a todo, y la próxima vez que algo tenga que ganarle a esa regla vas a necesitar otro `!important`. El CSS termina en una guerra que nadie entiende.

### Micro-misión R02-N06-P1 · El aviso de Ofidia

```meta
lugar: El muro de encargos
personajes: Iris, Tesela
criatura: ogro
carta: Especificidad | id > clase > etiqueta · #muro .aviso le gana a #muro p
recompensa: xp 15, oro 15
```

#### Escena
El Ogro de la Cascada se metió de noche en el **muro de encargos**. El aviso de Ofidia no se ve ámbar: otra regla le gana.
—Ninguna regla está borrada —dice {mentor}—. Otras les ganan. Sin `!important` y sin tocar el HTML: entendé **quién le gana a quién**.

#### Gheco sugiere
Gana el selector más **específico**: cuenta primero los `#id`, después las `.clases`, después las etiquetas. `#muro p` tiene un id y una etiqueta; `#muro .aviso`, un id y una clase: gana.

#### Desafío
Cambiá el selector de la regla ámbar de `.aviso` a `#muro .aviso`.

#### Código inicial
```html
<style>
  #muro p { color: #94a3b8; }
  .aviso { color: #f59e0b; }
</style>
<section id="muro">
  <p>Encargo de Kaffa: doce vitrales.</p>
  <p class="aviso">Aviso de Ofidia: el río crece.</p>
</section>
```

#### Inspector
```
css .aviso { color }
css #muro .aviso { color }
```

#### Salida esperada
```
css .aviso { color }: (no hay)
css #muro .aviso { color }: #f59e0b
```

#### Solución
```html
<style>
  #muro p { color: #94a3b8; }
  #muro .aviso { color: #f59e0b; }
</style>
<section id="muro">
  <p>Encargo de Kaffa: doce vitrales.</p>
  <p class="aviso">Aviso de Ofidia: el río crece.</p>
</section>
```

#### Al superarla
El aviso de Ofidia se enciende en ámbar. Al ogro se le descascara la primera capa.

#### Imagen
- Un muro de carteles pegados unos encima de otros; uno se enciende en ámbar.
- el Ogro de la Cascada (un ogro gordo hecho de capas de vidrios de colores superpuestos que se tapan unos a otros, con un mazo que tiene grabado !important) pierde una capa de vidrio.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) frente al muro.

### Micro-misión R02-N06-P2 · El encargo destacado

```meta
lugar: El muro de encargos
personajes: Iris, Gheco
criatura: ogro
carta: Dos clases | .encargo.destacado (pegadas) = un elemento con las dos clases · le gana a .encargo
recompensa: xp 15, oro 15
```

#### Escena
El encargo destacado de Kaffa parece uno más: el borde dorado no aparece.

#### Gheco sugiere
`.encargo.destacado` (con las dos clases **pegadas**) apunta al elemento que tiene las dos, y es más específico que `.encargo` solo.

#### Desafío
Cambiá el selector `.destacado` por `.encargo.destacado`.

#### Código inicial
```html
<style>
  .destacado { border-color: #fbbf24; }
  .encargo { border: 3px solid #334155; padding: 1rem; }
</style>
<article class="encargo">Ventana para el Valle</article>
<article class="encargo destacado">Doce vitrales para Kaffa</article>
```

#### Inspector
```
css .destacado { border-color }
css .encargo.destacado { border-color }
```

#### Salida esperada
```
css .destacado { border-color }: (no hay)
css .encargo.destacado { border-color }: #fbbf24
```

#### Solución
```html
<style>
  .encargo.destacado { border-color: #fbbf24; }
  .encargo { border: 3px solid #334155; padding: 1rem; }
</style>
<article class="encargo">Ventana para el Valle</article>
<article class="encargo destacado">Doce vitrales para Kaffa</article>
```

#### Al superarla
El borde dorado vuelve. Otra capa del ogro se cae al piso y se hace añicos.

#### Imagen
- Un cartel con borde dorado que vuelve a brillar en un muro de encargos.
- el Ogro de la Cascada (un ogro gordo hecho de capas de vidrios de colores superpuestos que se tapan unos a otros, con un mazo que tiene grabado !important) más flaco.
- Gheco (gecko de luz con antiparras) barre los vidrios.

### Micro-misión R02-N06-P3 · El mazo que no sirve

```meta
lugar: El muro de encargos
personajes: Iris, Tesela
criatura: ogro
carta: Sin !important | !important gana a todo y después nada le gana a él · se resuelve con un selector más específico
recompensa: xp 15, oro 15
```

#### Escena
El título del muro perdió su color: el ogro le pegó con su mazo, que tiene grabado `!important`. Teo propone pegarle con otro `!important` más grande.

#### Gheco sugiere
`!important` le gana a todo… y después nada le gana a él. Sacalo, y para que gane el cian usá un selector más específico.

#### Desafío
Sacá el `!important` de `.titulo`, y escribí `.muro .titulo` con `color: #22d3ee`.

#### Código inicial
```html
<style>
  .titulo { color: #64748b !important; }
</style>
<section class="muro">
  <h2 class="titulo">Muro de encargos</h2>
</section>
```

#### Inspector
```
css .titulo { color }
css .muro .titulo { color }
```

#### Salida esperada
```
css .titulo { color }: #64748b
css .muro .titulo { color }: #22d3ee
```

#### Solución
```html
<style>
  .titulo { color: #64748b; }
  .muro .titulo { color: #22d3ee; }
</style>
<section class="muro">
  <h2 class="titulo">Muro de encargos</h2>
</section>
```

#### Al superarla
El título se pone cian. El ogro mira su mazo y se lo esconde atrás de la espalda.

#### Imagen
- Un título de vitral que recupera su color cian.
- el Ogro de la Cascada (un ogro gordo hecho de capas de vidrios de colores superpuestos que se tapan unos a otros, con un mazo que tiene grabado !important) esconde el mazo atrás de la espalda.
- Tesela (22, pelo corto iridiscente violeta y cian, monóculo de cristal tallado, sobretodo largo negro con fragmentos de vidrio de colores cosidos) se cruza de brazos.

### Micro-misión R02-N06-P4 · El último gana

```meta
lugar: El muro de encargos
personajes: Iris, Tesela, Teo
criatura: ogro
carta: El orden | con la misma especificidad, gana la regla que viene después
recompensa: xp 20, oro 25
item: Monóculo de Cristal
```

#### Escena
Los botones del muro tienen el fondo oscuro y el texto no se ve. Hay dos reglas para `.boton`, iguales de específicas.

#### Gheco sugiere
Si dos reglas son igual de específicas, gana **la que viene después**. Mirá el orden.

#### Desafío
Borrá la segunda regla de `.boton` (la del fondo `#1e293b`), así gana la cian.

#### Código inicial
```html
<style>
  .boton { background: #22d3ee; color: #0f172a; padding: 0.5rem 1rem; }
  .boton { background: #1e293b; }
</style>
<a class="boton" href="#">Ver encargos</a>
```

#### Inspector
```
css .boton { background }
```

#### Salida esperada
```
css .boton { background }: #22d3ee
```

#### Solución
```html
<style>
  .boton { background: #22d3ee; color: #0f172a; padding: 0.5rem 1rem; }
</style>
<a class="boton" href="#">Ver encargos</a>
```

#### Al superarla
El ogro se descascara capa por capa hasta desaparecer. {mentor} se saca el monóculo y lo limpia con la manga, despacio. Iris no entiende por qué. Al día siguiente, en su mesa, hay un monóculo de cristal tallado igual al de {mentor}: **el Monóculo de Cristal**.

#### Imagen
- Un muro de encargos ordenado y luminoso; en el piso, una pila de capas de vidrio rotas.
- Tesela (22, pelo corto iridiscente violeta y cian, monóculo de cristal tallado, sobretodo largo negro con fragmentos de vidrio de colores cosidos) limpia su monóculo con la manga.
- Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian) la mira sin entender.
- Teo (15, flaco, pelo negro enrulado con purpurina, pecas, delantal manchado de todos los colores, cinturón con frascos de vidrio molido) aplaude.

### Misión R02-N06-M1 · El muro de encargos

```meta
entrega: codigo
entorno: navegador
monedas: 12
xp: 40
```

#### Consigna

Este es el muro que desordenó el Ogro. Arreglá **solo el CSS** (sin `!important`, sin estilos en línea y sin tocar el HTML) para que:

1. Los avisos ("¡Se entrega mañana!", "Encargo destacado") se vean **dorados y en negrita**.
2. El título del muro sea **cian**.
3. Las tarjetas tengan su **borde cian de 2 px**, y la destacada, **borde dorado**.
4. El texto de los botones sea **oscuro** sobre el cian.

Usá el inspector para ver qué regla gana en cada caso. Mirá «Cómo debería verse».

#### Criterio de aprobación

- Los cuatro puntos se ven como en «Cómo debería verse».
- No usa `!important` ni `style="…"`, y el HTML no cambió.
- Corrigió los dos valores inválidos (`2 px` y `colour`).

#### Cómo debe quedar

celular: capturas/R02-N06-M1-celular.webp
compu: capturas/R02-N06-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El muro de encargos</title>
    <style>
      :root {
        --fondo: #0b1020;
        --texto: #e2e8f0;
        --neon: #22d3ee;
        --oro: #fbbf24;
      }
      body {
        background: var(--fondo);
        color: var(--texto);
        font-family: system-ui, sans-serif;
        padding: 1.25rem;
      }
      #muro p {
        color: #94a3b8;
      }
      #muro a {
        color: white;
        text-decoration: none;
      }
      h2 {
        colour: var(--neon);
      }
      .aviso {
        color: var(--oro);
        font-weight: 700;
      }
      .destacada {
        border-color: var(--oro);
      }
      .tarjeta {
        border: 2 px solid var(--neon);
        border-radius: 0.75rem;
        padding: 1rem;
        margin-block: 1rem;
      }
      .tarjeta h3 {
        color: var(--neon);
        margin-top: 0;
      }
      .boton {
        display: inline-block;
        background: var(--neon);
        color: var(--fondo);
        padding: 0.5rem 1rem;
        border-radius: 999px;
        font-weight: 700;
      }
    </style>
  </head>
  <body>
    <main id="muro">
      <h2>Muro de encargos del taller</h2>
      <article class="tarjeta">
        <h3>Ventanal del Valle</h3>
        <p class="aviso">¡Se entrega mañana!</p>
        <p>Encargo de Ofidia: un ventanal para leer los pergaminos de datos del Valle de la Serpiente.</p>
        <a class="boton" href="#">Ver encargo</a>
      </article>
      <article class="tarjeta destacada">
        <h3>Vitrales de la catedral</h3>
        <p class="aviso">Encargo destacado</p>
        <p>Encargo de Kaffa: doce vitrales iguales para la catedral del Imperio de las Clases.</p>
        <a class="boton" href="#">Ver encargo</a>
      </article>
    </main>
  </body>
</html>
```

#### Solución de referencia

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El muro de encargos</title>
    <style>
      :root {
        --fondo: #0b1020;
        --texto: #e2e8f0;
        --neon: #22d3ee;
        --oro: #fbbf24;
      }
      body {
        background: var(--fondo);
        color: var(--texto);
        font-family: system-ui, sans-serif;
        padding: 1.25rem;
      }
      /* Un selector de elementos (0,0,2): las clases de abajo ahora le ganan */
      main p {
        color: #94a3b8;
      }
      main a {
        color: white;
        text-decoration: none;
      }
      h2 {
        color: var(--neon);
      }
      .aviso {
        color: var(--oro);
        font-weight: 700;
      }
      .tarjeta {
        border: 2px solid var(--neon);
        border-radius: 0.75rem;
        padding: 1rem;
        margin-block: 1rem;
      }
      .tarjeta h3 {
        color: var(--neon);
        margin-top: 0;
      }
      /* Después de .tarjeta: misma especificidad, gana la que viene después */
      .destacada {
        border-color: var(--oro);
      }
      .boton {
        display: inline-block;
        background: var(--neon);
        color: var(--fondo);
        padding: 0.5rem 1rem;
        border-radius: 999px;
        font-weight: 700;
      }
    </style>
  </head>
  <body>
    <main id="muro">
      <h2>Muro de encargos del taller</h2>
      <article class="tarjeta">
        <h3>Ventanal del Valle</h3>
        <p class="aviso">¡Se entrega mañana!</p>
        <p>Encargo de Ofidia: un ventanal para leer los pergaminos de datos del Valle de la Serpiente.</p>
        <a class="boton" href="#">Ver encargo</a>
      </article>
      <article class="tarjeta destacada">
        <h3>Vitrales de la catedral</h3>
        <p class="aviso">Encargo destacado</p>
        <p>Encargo de Kaffa: doce vitrales iguales para la catedral del Imperio de las Clases.</p>
        <a class="boton" href="#">Ver encargo</a>
      </article>
    </main>
  </body>
</html>
```
