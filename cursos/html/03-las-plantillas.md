# RAMA R03 · Las Plantillas del Gremio: Tailwind

```meta
tipo: tronco
posicion: 3
```

## R03-N01 · Hola, Tailwind

```meta
tipo: tema
padre: R02-N06
precio: 10
criatura: skeleton
temas: css.frameworks
usa: css.caja, css.flexbox
```

### Crónica

Tardás una tarde entera en cortar los vidrios de una sola tarjeta. Entonces {mentor} abre un cofre con cientos de **plantillas** ya cortadas, cada una para una sola cosa: esta da el borde redondeado, esta el color cian, esta el relleno.

—Son las plantillas del Gremio, {heroe}. Con ellas armás lo mismo en minutos. Pero te las doy recién ahora, **porque ya sabés cortar a mano**: si una plantilla falla, vas a saber por qué.

### Objetivos

Instalar y usar **Tailwind CSS v4**: entender la idea de **clases utilitarias**, compilar el CSS con el CLI (también en modo "vigilar") y rehacer la tarjeta del 07 sin escribir CSS.

### Antes de empezar

- Todo lo de los Vidrios: el modelo de caja, Flexbox, Grid y el diseño adaptable. Tailwind **no reemplaza** saber CSS: cada clase es una propiedad de CSS.

### Explicación

#### La idea
En vez de inventar una clase (`.tarjeta`) y escribir su CSS, se combinan **clases chicas que hacen una sola cosa**:
```html
<article class="max-w-sm rounded-xl border border-slate-800 bg-slate-900 p-5">
```
| Clase | CSS que genera |
|---|---|
| `p-5` | `padding: 1.25rem` (la escala es de a 0.25 rem: `p-1` = 0.25 rem, `p-4` = 1 rem) |
| `rounded-xl` | `border-radius: 0.75rem` |
| `bg-slate-900` | `background-color` gris azulado oscuro |
| `text-cyan-400` | `color` cian (los números van de 50, muy claro, a 950, muy oscuro) |
| `max-w-sm` | `max-width: 24rem` |
| `w-3/4` | `width: 75%` |

Ventajas: no hay que inventar nombres, no hay CSS que crece sin control, cada cosa se cambia en el mismo HTML. Desventaja: el HTML queda largo (en 17 vemos cómo organizarlo).

#### El ciclo de trabajo

**En la plataforma** no hay que instalar nada. Escribís el CSS de Tailwind dentro de un bloque especial en el `head`, y la vista previa lo compila sola cada vez que cambiás algo:
```html
<style type="text/tailwindcss">
  @import "tailwindcss";
</style>
```
Tailwind **revisa las clases que usaste** en la página y genera el CSS **solo de esas**.

**En tu compu**, para un proyecto de verdad, se usa el CLI con Node.js (20 o más nuevo). El CSS de entrada va en un archivo aparte, `entrada.css`, y el CLI genera `salida.css`, que es el que se enlaza en el HTML:
```
entrada.css  ──(el CLI de Tailwind lee los .html)──▶  salida.css  ◀── <link> del HTML
```
```bash
npm install tailwindcss @tailwindcss/cli                    # una vez, en el proyecto
npx @tailwindcss/cli -i entrada.css -o salida.css            # compilar una vez
npx @tailwindcss/cli -i entrada.css -o salida.css --watch    # vigilar: recompila al guardar
```
Lo que escribas en el bloque de la plataforma es exactamente lo que va en `entrada.css`.

#### Recomendado: la extensión de VS Code
*Tailwind CSS IntelliSense* autocompleta las clases y muestra el CSS de cada una al pasar el mouse.

#### Cómo se ve el ejemplo

Tocá *Celular* y *Compu* en la vista previa: la misma tarjeta de el nodo «El modelo de caja», igual en cada detalle. Si la página se ve **sin estilos** (letra con serifa, fondo blanco), falta el bloque de Tailwind.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Hola, Tailwind</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-slate-950 text-slate-200 p-5">
    <main class="space-y-8">
      <h1 class="text-3xl font-bold">Hola, Tailwind</h1>

      <!-- La MISMA tarjeta de la practica 07, sin escribir CSS: solo clases -->
      <article class="max-w-sm rounded-xl border border-slate-800 bg-slate-900 p-5 shadow-lg">
        <p class="font-mono text-xs text-slate-400">
          MOD-04
          <span class="ml-2 rounded bg-green-400/15 px-2 py-0.5 text-green-400">Activo</span>
        </p>
        <h2 class="mt-3 text-lg font-semibold">C++ Moderno &amp; Videojuegos</h2>
        <p class="mt-2 text-sm text-slate-400">Gestión de memoria, RAII, punteros inteligentes y C++20.</p>
        <p class="mt-3 text-xs text-slate-400">Progreso de nodos: 18 / 24</p>
        <div class="mt-2 h-2 overflow-hidden rounded-full bg-slate-800" role="progressbar" aria-label="Progreso del curso" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
          <div class="h-full w-3/4 bg-cyan-400"></div>
        </div>
        <p class="mt-4 font-mono font-bold text-cyan-400">+350 XP</p>
      </article>

      <p class="text-sm text-slate-400">
        Cada clase hace <strong class="text-slate-200">una sola cosa</strong>:
        <code class="font-mono text-cyan-400">p-5</code> = padding,
        <code class="font-mono text-cyan-400">rounded-xl</code> = bordes redondeados,
        <code class="font-mono text-cyan-400">text-cyan-400</code> = color de letra.
      </p>
    </main>
  </body>
</html>
```

### ¿Para qué sirve?

Tailwind es uno de los frameworks de CSS más usados del mundo: lo vas a encontrar en startups, en plantillas de Laravel y en muchísimos proyectos de React. Esta misma plataforma está hecha con Tailwind. Saber leer sus clases te permite meterte en cualquiera de esos proyectos desde el primer día.

### Errores habituales

**Esqueleto: la página sin estilos.** En la plataforma: falta el bloque `<style type="text/tailwindcss">` o, adentro, `@import "tailwindcss";`. En tu compu: no se compiló, o el `<link>` apunta a `entrada.css` en vez de `salida.css`.

**Esqueleto: una clase que "no existe"** (`text-cyan-450`, `padding-4`): no da error, simplemente no genera nada. IntelliSense la marca.

**Ogro: agregué una clase y no cambia nada.** En la plataforma se recompila sola; en tu compu, sin `--watch`, hay que volver a compilar.

**Esqueleto: clases armadas por partes** (`"text-" + color + "-400"` desde JavaScript): el CLI busca clases **completas** en el texto de los archivos; si nunca aparecen escritas enteras, no las genera.

### Prueba del sello

#### ¿Qué es una clase utilitaria?

Una clase chica que hace **una sola cosa**: `p-5` pone un relleno, `rounded-xl` redondea, `text-cyan-400` pinta el texto. En lugar de inventar una clase (`.tarjeta`) y escribir su CSS, se combinan varias de estas en el HTML.

#### ¿Por qué el CSS que genera Tailwind pesa tan poco aunque tenga miles de clases?

Porque Tailwind **revisa las clases que usaste** en tus archivos y genera el CSS **solo de esas**. Si usaste 40 clases, el CSS tiene 40 reglas, no miles.

#### ¿Qué pasa si escribís una clase que no existe?

Nada: no da error, simplemente no genera ningún estilo (un esqueleto). Por eso conviene la extensión *Tailwind CSS IntelliSense*, que las autocompleta y avisa.

### Misión R03-N01-M1 · La tarjeta violeta

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Rehacé con clases de Tailwind la tarjeta del curso de **SDL3**: borde y acento **violeta**, y una barra de progreso al **45 %**. Para un valor que no está en la escala se usan corchetes: `w-[45%]`.

#### Criterio de aprobación

- No hay CSS escrito a mano: solo clases de Tailwind.
- Borde y acento violeta (`border-violet-…`, `bg-violet-…`).
- La barra mide 45 % con un valor a medida (`w-[45%]`).

#### Cómo debe quedar

celular: capturas/R03-N01-M1-celular.webp
compu: capturas/R03-N01-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La tarjeta violeta</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Tarjeta SDL3 con Tailwind</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-slate-950 p-5 text-slate-200">
    <article class="max-w-sm rounded-xl border border-violet-900 bg-slate-900 p-5">
      <p class="font-mono text-xs text-slate-400">MOD-06</p>
      <h1 class="mt-3 text-lg font-semibold">SDL3 &amp; Game Loops</h1>
      <p class="mt-2 text-sm text-slate-400">Renderizado acelerado y eventos en tiempo real.</p>
      <div class="mt-4 h-2 overflow-hidden rounded-full bg-slate-800" role="progressbar" aria-label="Progreso del curso" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100">
        <div class="h-full w-[45%] bg-violet-400"></div>
      </div>
      <p class="mt-4 font-mono font-bold text-violet-400">+420 XP</p>
    </article>
  </body>
</html>
```


### Misión R03-N01-M2 · Los botones

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá los dos botones de la plataforma: **"Continuar campaña"**, con fondo cian, y **"Nodos"**, solo con borde. Mirá «Cómo debería verse».

#### Criterio de aprobación

- "Continuar campaña" tiene fondo cian y texto oscuro; "Nodos", borde y fondo transparente.
- Los dos tienen el mismo alto, relleno y esquinas redondeadas.
- Solo clases de Tailwind.

#### Cómo debe quedar

celular: capturas/R03-N01-M2-celular.webp
compu: capturas/R03-N01-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Los botones</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Botones con Tailwind</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-slate-950 p-5">
    <a href="#" class="inline-block rounded-lg bg-cyan-400 px-5 py-3 font-semibold text-slate-950">▷ Continuar campaña</a>
    <a href="#" class="ml-2 inline-block rounded-lg border border-slate-700 px-5 py-3 font-semibold text-cyan-400">Nodos</a>
  </body>
</html>
```


### Encargo R03-N01-E1 · Los avisos del sistema

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Un sistema de turnos necesita tres avisos: **éxito** (verde), **advertencia** (ámbar) y **error** (rojo), cada uno con un borde izquierdo grueso de su color.

#### Criterio de aprobación

- Tres avisos con su color y un borde izquierdo grueso (`border-l-4`).
- El texto se lee bien sobre el fondo de cada uno.

#### Cómo debe quedar

celular: capturas/R03-N01-E1-celular.webp
compu: capturas/R03-N01-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Los avisos del sistema</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Avisos de un sistema</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="space-y-3 bg-white p-5">
    <p class="rounded-md border-l-4 border-green-500 bg-green-50 p-4 text-green-800">✔ Pago acreditado.</p>
    <p class="rounded-md border-l-4 border-amber-500 bg-amber-50 p-4 text-amber-800">⚠ Tu suscripción vence en 3 días.</p>
    <p class="rounded-md border-l-4 border-red-500 bg-red-50 p-4 text-red-800">✘ No se pudo enviar el formulario.</p>
  </body>
</html>
```

## R03-N02 · Las utilidades

```meta
tipo: tema
padre: R03-N01
precio: 10
criatura: goblin
temas: css.frameworks, css.caja
usa: css.frameworks
```

### Crónica

El cofre de plantillas tiene cajones: uno para los espacios, otro para las letras, otro para los colores y los brillos. Zed quiere usarlas todas a la vez y arma una tarjeta que parece un árbol de Navidad.

—Conocé los **cajones** y su **escala** —lo frena {mentor}—. Las plantillas sueltas no sirven si no sabés dónde buscarlas.

### Objetivos

Conocer las familias de utilidades más usadas (espaciado, tamaños, tipografía, color con transparencia, bordes, anillos, sombras, degradés), su escala y los valores a medida con corchetes.

### Antes de empezar

- Hola, Tailwind («Hola, Tailwind»). Las propiedades de CSS de 06–07.

### Explicación

#### Espacios y tamaños (escala de a 0.25 rem)
| Clase | CSS |
|---|---|
| `p-4`, `px-3`, `py-1.5`, `pt-2` | padding (todos, horizontal, vertical, arriba) |
| `m-4`, `mt-3`, `mx-auto`, `-mt-2` | margin (con `-` adelante: negativo) |
| `w-64`, `w-full`, `w-1/2`, `max-w-sm`, `min-h-screen` | anchos y altos |
| `size-10` | ancho **y** alto a la vez |
| `space-y-4` | espacio vertical entre los hijos |

`4` = 1 rem (16 px). `1` = 0.25 rem. `0.5` y `1.5` también existen.

#### Tipografía
`text-xs` … `text-6xl` (tamaño), `font-bold`/`font-extrabold`, `font-mono`, `uppercase`, `tracking-widest` (separación entre letras), `leading-tight` / `leading-relaxed` (interlineado), `line-through`, `antialiased` (letra más fina en fondos oscuros).

#### Colores
- Paleta: `slate`, `cyan`, `sky`, `amber`, `emerald`, `violet`… con tonos `50` a `950`.
- Se usan con un prefijo: `text-`, `bg-`, `border-`, `ring-`, `shadow-`, `from-`/`to-`.
- **Transparencia** con `/`: `bg-cyan-400/10` = cian al 10 %. Es el truco de todo el diseño "neón": fondos casi transparentes con borde y texto del mismo color.

#### Bordes, anillos y sombras
| Clase | Efecto |
|---|---|
| `border`, `border-2`, `border-l-4` + `border-cyan-400/40` | borde |
| `rounded`, `rounded-xl`, `rounded-full` | esquinas |
| `ring-2 ring-amber-400 ring-offset-4 ring-offset-slate-950` | anillo por fuera, con separación |
| `shadow-lg shadow-cyan-500/20` | sombra **con color**: el brillo de las tarjetas |

#### Degradés
`bg-linear-to-r from-cyan-300 to-sky-500` (de izquierda a derecha; `via-` agrega un color en el medio). Para un **texto** con degradé: `bg-clip-text text-transparent`.

#### Valores a medida
Si la escala no tiene lo que buscás: corchetes. `bg-[#1b1530]`, `text-[15px]`, `w-[45%]`, `grid-cols-[1fr_1.2fr_1fr]` (los espacios se escriben `_`). Usalos poco: si un valor se repite, va al **tema** («Tema propio»).

#### Posición (repaso de 10)
`relative` en el padre, `absolute -bottom-2 left-1/2 -translate-x-1/2` en el hijo: pegado abajo y centrado (`-translate-x-1/2` lo corre la mitad de su propio ancho hacia la izquierda). Se usa en la misión 1.

#### El ejemplo

Cinco muestras: título con degradé, espaciado, píldora "SYSTEM ONLINE", tarjeta con brillo, anillo dorado, valores a medida y la pastilla de estadísticas de la cabecera.

#### Cómo se ve el ejemplo

Tocá *Celular* y *Compu* en la vista previa: "árbol de habilidades" en degradé cian → azul, las cajas de margen/padding, la píldora con el punto verde, la tarjeta con brillo cian, la de anillo dorado separado, la caja violeta y `⚡ 1.450 • 🔥 12`.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Utilidades de Tailwind</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-slate-950 p-5 text-slate-200 antialiased">
    <main class="space-y-10">

      <!-- Tipografia + degrade en el texto -->
      <section aria-labelledby="t1">
        <p id="t1" class="font-mono text-xs tracking-widest text-cyan-400 uppercase">1 · Tipografía</p>
        <h1 class="mt-2 text-3xl leading-tight font-extrabold">
          Aprendé avanzando por tu
          <span class="bg-linear-to-r from-cyan-300 to-sky-500 bg-clip-text text-transparent">árbol de habilidades</span>.
        </h1>
        <p class="mt-2 text-sm leading-relaxed text-slate-400">Texto chico, con más interlineado y color apagado.</p>
      </section>

      <!-- Espaciado y tamanos -->
      <section aria-labelledby="t2">
        <p id="t2" class="font-mono text-xs tracking-widest text-cyan-400 uppercase">2 · Espaciado</p>
        <div class="mt-3 inline-block bg-cyan-400/20">
          <div class="m-4 bg-cyan-400/40 p-4 font-mono text-sm">m-4 + p-4</div>
        </div>
        <div class="mt-3 flex gap-2">
          <span class="size-8 rounded bg-slate-700"></span>
          <span class="size-10 rounded bg-slate-600"></span>
          <span class="size-12 rounded bg-slate-500"></span>
        </div>
      </section>

      <!-- Colores con transparencia, bordes y anillos -->
      <section aria-labelledby="t3">
        <p id="t3" class="font-mono text-xs tracking-widest text-cyan-400 uppercase">3 · Color, bordes y sombras</p>
        <p class="mt-3 inline-flex items-center gap-2 rounded-full border border-cyan-400/40 bg-cyan-400/10 px-3 py-1 font-mono text-xs text-cyan-300">
          <span class="size-2 rounded-full bg-emerald-400"></span> SYSTEM ONLINE
        </p>
        <div class="mt-4 rounded-xl border border-cyan-400/60 bg-slate-900 p-4 shadow-lg shadow-cyan-500/20">Borde de color + sombra con color (brillo neón)</div>
        <div class="mt-4 rounded-xl bg-slate-900 p-4 ring-2 ring-amber-400 ring-offset-4 ring-offset-slate-950">Anillo dorado con separación (ring + ring-offset)</div>
      </section>

      <!-- Valores a medida -->
      <section aria-labelledby="t4">
        <p id="t4" class="font-mono text-xs tracking-widest text-cyan-400 uppercase">4 · Valores a medida</p>
        <p class="mt-3 rounded-lg bg-[#1b1530] p-4 text-[15px] text-[#c4b5fd]">Color y tamaño exactos con corchetes: <code>bg-[#1b1530]</code>, <code>text-[15px]</code></p>
      </section>

      <!-- Todo junto: la pastilla de estadisticas de la cabecera -->
      <section aria-labelledby="t5">
        <p id="t5" class="font-mono text-xs tracking-widest text-cyan-400 uppercase">5 · Todo junto</p>
        <p class="mt-3 inline-flex gap-3 rounded-lg border border-slate-800 bg-slate-900/80 px-3 py-1.5 font-mono text-sm">
          <span class="text-cyan-300">⚡ 1.450</span>
          <span class="text-slate-600" aria-hidden="true">•</span>
          <span class="text-orange-400">🔥 12</span>
        </p>
      </section>
    </main>
  </body>
</html>
```

### ¿Para qué sirve?

Las escalas de espacios y colores son lo que hace que un diseño se vea "prolijo": todo está a 4, 8, 16 o 24 px, nunca a 13. Los equipos de diseño trabajan con esas mismas escalas, así que lo que aprendés acá es el idioma con el que vas a hablar con cualquier diseñador.

### Errores habituales

**Goblin: dos clases de la misma familia** (`p-2 p-6`): no gana la última del atributo, gana la que Tailwind generó **más abajo** en el CSS. No mezcles: dejá una.

**Esqueleto: el degradé del texto no se ve**: falta `bg-clip-text` o `text-transparent`.

**Goblin: corchetes con espacios** (`grid-cols-[1fr 2fr]`): se corta la clase. Usá `_`.

### Prueba del sello

#### ¿Cuánto mide `p-4`? ¿Y `mt-0.5`?

La escala va de a 0,25 rem: `p-4` es 1 rem (16 px) de relleno en los cuatro lados y `mt-0.5` es 0,125 rem (2 px) de margen arriba.

#### ¿Qué significa `bg-cyan-400/10`?

Fondo del color cian 400 con **10 % de opacidad**: el número después de la barra es la transparencia.

#### ¿Cuándo conviene un valor con corchetes y cuándo no?

Los corchetes (`w-[45%]`, `bg-[#0e1626]`) sirven para un valor **puntual** que no está en la escala. Si el mismo valor se repite en muchos lugares, conviene agregarlo al tema (lo vas a ver en «Tema propio»).

### Misión R03-N02-M1 · La insignia de nivel

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá el avatar de la cabecera del celular: una imagen redonda con un **anillo cian** y la etiqueta **`LV.14`** pegada abajo, al centro (como en esta plataforma).

#### Criterio de aprobación

- El avatar es redondo y tiene un anillo cian (`ring-…`).
- La etiqueta `LV.14` queda superpuesta abajo al centro (posición `relative`/`absolute`).
- La imagen tiene `alt`.

#### Cómo debe quedar

celular: capturas/R03-N02-M1-celular.webp
compu: capturas/R03-N02-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La insignia de nivel</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Insignia de nivel</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-slate-950 p-5">
    <div class="relative inline-block">
      <img src="/img/cursos/html/gheco-logo.webp" alt="Avatar" width="64" height="64" class="rounded-xl bg-slate-900 p-2 ring-2 ring-cyan-400">
      <span class="absolute -bottom-2 left-1/2 -translate-x-1/2 rounded bg-violet-600 px-1.5 font-mono text-[10px] font-bold text-white">LV.14</span>
    </div>
  </body>
</html>
```


### Misión R03-N02-M2 · Títulos con degradé

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Escribí dos títulos con el texto en degradé: **"Hall of Fame"** en dorado y **"Liga Obsidiana"** con tres colores.

#### Criterio de aprobación

- El degradé está en el texto, no en el fondo (`bg-clip-text text-transparent`).
- "Liga Obsidiana" usa tres colores (`from-…`, `via-…`, `to-…`).

#### Cómo debe quedar

celular: capturas/R03-N02-M2-celular.webp
compu: capturas/R03-N02-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Títulos con degradé</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Títulos con degradé</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="space-y-4 bg-slate-950 p-5">
    <h1 class="bg-linear-to-r from-amber-300 to-orange-500 bg-clip-text text-4xl font-black text-transparent">Hall of Fame</h1>
    <h2 class="bg-linear-to-r from-fuchsia-400 via-violet-400 to-cyan-400 bg-clip-text text-2xl font-bold text-transparent">Liga Obsidiana</h2>
  </body>
</html>
```


### Encargo R03-N02-E1 · La etiqueta de oferta

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Una tienda quiere la tarjeta de un producto en oferta: una etiqueta **"-20 %"**, el precio viejo tachado y el precio nuevo, grande.

#### Criterio de aprobación

- La etiqueta "-20 %" se destaca.
- El precio viejo está tachado (`line-through`) y el nuevo es más grande.

#### Cómo debe quedar

celular: capturas/R03-N02-E1-celular.webp
compu: capturas/R03-N02-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La etiqueta de oferta</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Producto en oferta</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-stone-100 p-5">
    <article class="max-w-xs rounded-2xl bg-white p-5 shadow-md">
      <p class="inline-block rounded-full bg-red-600 px-3 py-0.5 text-xs font-bold tracking-wide text-white uppercase">-20 %</p>
      <h1 class="mt-3 text-xl font-semibold text-stone-800">Zapatillas Trail</h1>
      <p class="mt-1 text-sm text-stone-400 line-through">$80000</p>
      <p class="text-3xl font-extrabold text-stone-900">$64000</p>
    </article>
  </body>
</html>
```

## R03-N03 · Flex y Grid con Tailwind

```meta
tipo: tema
padre: R03-N02
precio: 10
criatura: orc
temas: css.frameworks, css.flexbox, css.grid
usa: css.flexbox, css.grid
```

### Crónica

Con las plantillas en la mano, {mentor} te pide algo que parece imposible: rearmar la pantalla de la cabaña —la versión celular de la plataforma— **sin escribir una sola regla de CSS**.

—Todo lo que aprendiste de la regla flexible y de la malla está en el cofre, {heroe}. Solo le cambiaron el nombre.

### Objetivos

Usar Flexbox y Grid con clases de Tailwind y rearmar la versión **celular** de la plataforma: cabecera, tarjetas de rutas, podio y filas del ranking.

### Antes de empezar

- Flexbox («Flexbox») y Grid («Grid») en CSS. Utilidades («Las utilidades»).

### Explicación

#### Equivalencias
| CSS (de «Flexbox» a «Grid») | Tailwind |
|---|---|
| `display: flex` | `flex` |
| `flex-direction: column` | `flex-col` |
| `justify-content: space-between` | `justify-between` |
| `align-items: center` | `items-center` |
| `gap: 0.75rem` | `gap-3` |
| `flex: 1` | `flex-1` |
| `flex-shrink: 0` | `shrink-0` |
| `min-width: 0` | `min-w-0` |
| `flex-wrap: wrap` | `flex-wrap` |
| `align-self: flex-end` | `self-end` |
| `overflow: hidden; text-overflow: ellipsis; white-space: nowrap` | `truncate` |
| `display: grid` | `grid` |
| `grid-template-columns: repeat(2, 1fr)` | `grid-cols-2` |
| columnas a medida | `grid-cols-[1fr_1.2fr_1fr]` |
| `grid-column: span 2` | `col-span-2` |
| `place-items: center` | `place-items-center` |
| `justify-items: center` | `justify-items-center` |

#### Recetas que se repiten
- **Ícono cuadrado centrado**: `grid size-12 shrink-0 place-items-center`.
- **Texto que crece y se corta**: `min-w-0 flex-1` en el contenedor y `truncate` en el texto.
- **Puntos alineados a la derecha en dos líneas**: `text-right` + un `span` con `block`.
- **Fila resaltada** (el usuario actual): mismo molde, con `border-cyan-400/60 bg-cyan-400/5`.

#### El ejemplo

La pantalla del celular de esta plataforma, recortada.

#### Cómo se ve el ejemplo

Tocá *Celular* y *Compu* en la vista previa: cabecera con el gecko y las estadísticas, el título con la píldora "23 módulos", dos tarjetas con su ícono cuadrado y XP en dorado (los títulos largos terminan en `…`), dos tarjetas chicas lado a lado, el podio 2-1-3 y dos filas del ranking (la de @GhecoDev resaltada en cian). En escritorio se ve todo estirado: todavía no hay responsive (eso es la 14).

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Flex y Grid con Tailwind</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-slate-950 text-slate-200 antialiased">
    <!-- Cabecera: flex + justify-between -->
    <header class="flex items-center justify-between border-b border-slate-800 px-4 py-3">
      <a href="#" class="flex items-center gap-2 font-extrabold">
        <img src="/img/cursos/html/gheco-logo.webp" alt="" width="36" height="36" class="rounded-lg ring-1 ring-cyan-400/40">
        <span>GhecoSoft <span class="text-cyan-400">-Code</span></span>
      </a>
      <p class="flex gap-3 rounded-lg border border-slate-800 px-3 py-1 font-mono text-sm">
        <span>⚡ 1.450</span><span>🔥 12</span>
      </p>
    </header>

    <main class="space-y-8 p-4">
      <!-- Lista de tarjetas: flex en columna con gap -->
      <section aria-labelledby="rutas" class="flex flex-col gap-3">
        <div class="flex items-center justify-between">
          <h2 id="rutas" class="text-lg font-bold">Rutas de Entrenamiento</h2>
          <span class="rounded-full border border-emerald-400/40 px-2 py-0.5 font-mono text-xs text-emerald-400">23 módulos</span>
        </div>
        <article class="flex items-center gap-3 rounded-xl border border-cyan-400/60 bg-slate-900 p-4">
          <span class="grid size-12 shrink-0 place-items-center rounded-lg border border-cyan-400 font-mono font-bold text-cyan-400">C++</span>
          <div class="min-w-0 flex-1">
            <p class="font-mono text-xs text-slate-400">04 · CORE</p>
            <h3 class="truncate font-semibold">C++ Moderno &amp; Videojuegos</h3>
          </div>
          <span class="font-mono text-sm font-bold text-amber-400">+350 XP</span>
        </article>
        <article class="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-900 p-4">
          <span class="grid size-12 shrink-0 place-items-center rounded-lg border border-violet-400 font-mono font-bold text-violet-300">SDL</span>
          <div class="min-w-0 flex-1">
            <p class="font-mono text-xs text-slate-400">06 · GRAPHICS</p>
            <h3 class="truncate font-semibold">Motores Gráficos con SDL3</h3>
          </div>
          <span class="font-mono text-sm font-bold text-amber-400">+420 XP</span>
        </article>
        <!-- Dos tarjetas chicas lado a lado: grid de 2 columnas -->
        <div class="grid grid-cols-2 gap-3">
          <article class="rounded-xl border border-slate-800 bg-slate-900 p-3">
            <p class="font-mono text-xs text-sky-400">TS · 23</p>
            <h3 class="mt-1 text-sm font-semibold">TypeScript Pro</h3>
          </article>
          <article class="rounded-xl border border-slate-800 bg-slate-900 p-3">
            <p class="font-mono text-xs text-red-400">JV · 20</p>
            <h3 class="mt-1 text-sm font-semibold">Spring Boot Cloud</h3>
          </article>
        </div>
      </section>

      <!-- Podio: grid de 3 columnas a medida, apoyadas abajo -->
      <section aria-labelledby="fama">
        <h2 id="fama" class="mb-4 text-lg font-bold">Hall of Fame</h2>
        <ol class="grid grid-cols-[1fr_1.2fr_1fr] items-end gap-2">
          <li class="grid justify-items-center gap-1 rounded-xl border-2 border-slate-300 bg-slate-900 px-1 py-4 text-xs">
            <span class="grid size-8 place-items-center rounded-full bg-slate-700 font-bold">2</span>
            @DevValkyrie<strong class="font-mono text-cyan-300">13.2k</strong>
          </li>
          <li class="grid justify-items-center gap-1 rounded-xl border-2 border-amber-400 bg-slate-900 px-1 py-7 text-xs shadow-lg shadow-amber-400/30">
            <span class="grid size-8 place-items-center rounded-full bg-amber-400 font-bold text-slate-950">1</span>
            @NeoCoder_X<strong class="font-mono text-amber-400">14.850</strong>
          </li>
          <li class="grid justify-items-center gap-1 rounded-xl border-2 border-orange-500 bg-slate-900 px-1 py-4 text-xs">
            <span class="grid size-8 place-items-center rounded-full bg-slate-700 font-bold">3</span>
            @GlitchHunter<strong class="font-mono text-cyan-300">12.4k</strong>
          </li>
        </ol>
      </section>

      <!-- Filas del ranking -->
      <ol class="space-y-2" start="4">
        <li class="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-900 px-4 py-3">
          <span class="w-5 font-mono text-slate-400">4</span>
          <span class="grid size-9 shrink-0 place-items-center rounded-lg bg-slate-800">⚡</span>
          <span class="min-w-0 flex-1">
            <span class="block truncate font-semibold">@ZeroByte_Arg</span>
            <span class="block text-xs text-slate-400">C++ · <span class="text-emerald-400">▲ +1</span></span>
          </span>
          <span class="text-right font-mono">10.900<span class="block text-xs text-slate-400">XP</span></span>
        </li>
        <li class="flex items-center gap-3 rounded-xl border border-cyan-400/60 bg-cyan-400/5 px-4 py-3">
          <span class="w-5 font-mono text-cyan-400">10</span>
          <span class="grid size-9 shrink-0 place-items-center rounded-lg bg-slate-800">🦎</span>
          <span class="min-w-0 flex-1">
            <span class="block truncate font-semibold text-cyan-300">@GhecoDev</span>
            <span class="block text-xs text-slate-400">TypeScript · <span class="text-emerald-400">▲ +4</span></span>
          </span>
          <span class="text-right font-mono text-cyan-300">6.400<span class="block text-xs text-slate-400">XP</span></span>
        </li>
      </ol>
    </main>
  </body>
</html>
```

### ¿Para qué sirve?

Las apps de chat, los tableros de estadísticas, las barras de navegación de los celulares y las grillas de productos se arman con flex y grid. Con Tailwind lo hacés directo en el HTML, que es como se trabaja hoy en la mayoría de los proyectos con React, Vue o Laravel.

### Errores habituales

**Ogro: `truncate` no corta.** El contenedor que crece necesita `min-w-0`.

**Ogro: `items-center` en el hijo.** Las clases de alineación van en el
**contenedor**; en el hijo se usa `self-*`.

**Ogro: `space-y-*` dentro de un `flex` en fila**: `space-y` separa en vertical; en filas va `gap-*` (que funciona en las dos direcciones).

### Prueba del sello

#### ¿Qué tres clases necesita una fila con un texto largo que se corta?

`flex-1` y `min-w-0` en el contenedor que crece (para que pueda achicarse) y `truncate` en el texto (que corta con `…`).

#### ¿Qué diferencia hay entre `space-y-2` y `gap-2`?

`space-y-2` pone un margen arriba de cada hijo menos el primero: funciona en cualquier contenedor, pero solo en vertical. `gap-2` es el espacio **entre** los hijos de un contenedor `flex` o `grid`, en las dos direcciones, y no se rompe si un hijo está oculto o la fila pasa a otra línea.

#### ¿Cómo hacés tres columnas donde la del medio es un 20 % más ancha?

Con columnas a medida: `grid grid-cols-[1fr_1.2fr_1fr]` (los guiones bajos son los espacios).

### Misión R03-N03-M1 · La barra inferior

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá la barra inferior de 4 secciones **pegada abajo de la ventana**, usando solo flex: `min-h-screen flex flex-col` en el `body` y `flex-1` en el `main`.

#### Criterio de aprobación

- La barra queda abajo aunque haya poco contenido, sin `position: fixed`.
- Las 4 secciones miden lo mismo (`flex-1` en cada una).
- Solo clases de Tailwind.

#### Cómo debe quedar

celular: capturas/R03-N03-M1-celular.webp
compu: capturas/R03-N03-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La barra inferior</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Barra inferior con Tailwind</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="flex min-h-screen flex-col bg-slate-950 text-slate-200">
    <main class="flex-1 p-4">Contenido</main>
    <nav aria-label="Secciones" class="flex border-t border-slate-800 bg-slate-900 text-xs">
      <a href="#" class="flex flex-1 flex-col items-center py-2 text-slate-400"><span aria-hidden="true">🗺</span>Campañas</a>
      <a href="#" class="flex flex-1 flex-col items-center py-2 text-slate-400"><span aria-hidden="true">📖</span>Lecciones</a>
      <a href="#" aria-current="page" class="flex flex-1 flex-col items-center py-2 text-cyan-400"><span aria-hidden="true">⚔</span>Arena</a>
      <a href="#" class="flex flex-1 flex-col items-center py-2 text-slate-400"><span aria-hidden="true">🌳</span>Árbol</a>
    </nav>
  </body>
</html>
```


### Misión R03-N03-M2 · El tablero

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá un tablero con **tres estadísticas** en una grilla de **2 columnas**, donde la primera ocupa las dos.

#### Criterio de aprobación

- Usa `grid grid-cols-2` y la primera estadística tiene `col-span-2`.
- Las tres tarjetas tienen el mismo estilo.

#### Cómo debe quedar

celular: capturas/R03-N03-M2-celular.webp
compu: capturas/R03-N03-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El tablero</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Tablero de estadísticas</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-slate-950 p-4 text-slate-200">
    <div class="grid grid-cols-2 gap-3">
      <div class="col-span-2 rounded-xl bg-slate-900 p-4">XP total<p class="font-mono text-3xl text-cyan-300">14.850</p></div>
      <div class="rounded-xl bg-slate-900 p-4">Racha<p class="font-mono text-2xl text-orange-400">45 días</p></div>
      <div class="rounded-xl bg-slate-900 p-4">Nodos<p class="font-mono text-2xl text-emerald-400">82</p></div>
    </div>
  </body>
</html>
```


### Encargo R03-N03-E1 · El chat de soporte

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Una tienda quiere un chat de soporte: los mensajes del cliente a la izquierda y los propios a la derecha (`self-start` / `self-end`), con un ancho máximo del 80 %.

#### Criterio de aprobación

- Los mensajes se alinean a cada lado con `self-start` y `self-end`.
- Ninguno ocupa más del 80 % (`max-w-[80%]`).

#### Cómo debe quedar

celular: capturas/R03-N03-E1-celular.webp
compu: capturas/R03-N03-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El chat de soporte</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Chat de soporte</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-gray-100 p-4">
    <ol class="mx-auto flex max-w-md flex-col gap-2">
      <li class="max-w-[80%] self-start rounded-2xl rounded-bl-none bg-white px-4 py-2 shadow">Hola, ¿en qué te ayudo?</li>
      <li class="max-w-[80%] self-end rounded-2xl rounded-br-none bg-green-600 px-4 py-2 text-white">No me llegó el pedido 1234.</li>
      <li class="max-w-[80%] self-start rounded-2xl rounded-bl-none bg-white px-4 py-2 shadow">Lo reviso y te aviso en 5 minutos.</li>
    </ol>
  </body>
</html>
```

## R03-N04 · Responsive con Tailwind

```meta
tipo: tema
padre: R03-N03
precio: 10
criatura: orc
temas: css.frameworks, css.responsive
usa: css.responsive
```

### Crónica

Desde el Valle de la Serpiente llega un encargo de **Ofidia**: quiere una ventana para mostrar sus pergaminos de datos, y la quiere ver bien en el espejo de bolsillo de cada aldeano y también en el gran salón.

{mentor} te muestra el truco más usado del cofre: un **prefijo** delante de cualquier plantilla. —`md:` significa "desde la ventana mediana en adelante", {heroe}. Lo que va sin prefijo es la cabaña. Lo demás, se agrega.

### Objetivos

Hacer layouts responsive con los prefijos `sm:`, `md:`, `lg:`, `xl:` y rehacer el nodo «Responsive: celular primero» (barra inferior en el celular, menú arriba en la computadora, grilla de 1→2→4 y hero de 1→2 columnas) solo con clases.

### Antes de empezar

- Mobile first con media queries («Responsive: celular primero»). Flex y Grid con Tailwind («Flex y Grid con Tailwind»).

### Explicación

#### Los prefijos
| Prefijo | Desde | Equivale a |
|---|---|---|
| (ninguno) | 0: **celular** | estilos base |
| `sm:` | 40rem (640 px) | `@media (min-width: 40rem)` |
| `md:` | 48rem (768 px) | |
| `lg:` | 64rem (1024 px) | |
| `xl:` | 80rem (1280 px) | |
| `2xl:` | 96rem (1536 px) | |

**`md:flex` NO significa "en tablets"**: significa "desde 48rem en adelante". Por eso se escribe primero lo del celular y después lo que cambia:
```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">   <!-- 1 → 2 → 4 -->
<nav class="hidden md:flex">                                   <!-- oculto → visible -->
<nav class="fixed bottom-0 md:hidden">                         <!-- visible → oculto -->
<h1 class="text-3xl sm:text-4xl lg:text-5xl">                  <!-- crece -->
<div class="flex flex-col sm:flex-row">                        <!-- apilado → en fila -->
```
Para un rango cerrado existe `max-*`: `md:max-lg:hidden` = oculto solo entre md y lg.

#### El contenedor
`mx-auto max-w-7xl px-4`: centrado, como mucho 80 rem, con margen a los costados en el celular. Se repite en la cabecera y en el `main` para que todo quede alineado.

#### Lo de siempre, con clases
`sticky top-0 z-10` (cabecera pegada), `fixed inset-x-0 bottom-0` (barra inferior), `pb-16 md:pb-0` (lugar para la barra solo cuando existe), `backdrop-blur` (desenfoca lo que pasa por detrás de la cabecera semitransparente).

#### El ejemplo

La misma página de el nodo «Responsive: celular primero». Abajo, un indicador muestra qué prefijo está activo.

#### Cómo se ve el ejemplo

Igual que el nodo «Responsive: celular primero»: celular con botones apilados, una columna y barra fija abajo; computadora con menú en la cabecera, hero en dos columnas, botones en fila y 4 cursos por fila.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Responsive con Tailwind</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <!-- pb-16 en el celular (lugar para la barra fija); md:pb-0 desde 48rem -->
  <body class="bg-slate-950 pb-16 text-slate-200 antialiased md:pb-0">
    <header class="sticky top-0 z-10 border-b border-slate-800 bg-slate-950/90 backdrop-blur">
      <div class="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3">
        <a href="#" class="flex items-center gap-2 font-extrabold">
          <img src="/img/cursos/html/gheco-logo.webp" alt="" width="36" height="36" class="rounded-lg ring-1 ring-cyan-400/40">
          <span>GhecoSoft <span class="text-cyan-400">-Code</span></span>
        </a>
        <!-- hidden = display:none; md:flex = desde 48rem, display:flex -->
        <nav aria-label="Principal" class="hidden gap-6 text-sm md:flex">
          <a href="#cursos" class="hover:text-cyan-400">Cursos</a>
          <a href="#" class="hover:text-cyan-400">Rutas</a>
          <a href="#" class="hover:text-cyan-400">Top 10</a>
          <a href="#" class="hover:text-cyan-400">Bóveda de tokens</a>
        </nav>
        <p class="font-mono text-sm">⚡ 1.450 <span class="hidden sm:inline">· 🔥 12</span></p>
      </div>
    </header>

    <main class="mx-auto max-w-7xl space-y-12 px-4 py-6 lg:py-12">
      <!-- Hero: 1 columna; desde lg, 2 columnas -->
      <section aria-labelledby="titulo" class="grid gap-6 lg:grid-cols-[1.4fr_1fr] lg:items-center">
        <div>
          <h1 id="titulo" class="text-3xl leading-tight font-extrabold sm:text-4xl lg:text-5xl">
            Aprendé a programar avanzando por tu <span class="text-cyan-400">árbol de habilidades</span>.
          </h1>
          <p class="mt-3 text-slate-400 lg:text-lg">Compilá algoritmos reales y competí por el rango Supremo.</p>
          <!-- Botones: apilados en el celular, en fila desde sm -->
          <div class="mt-6 flex flex-col gap-3 sm:flex-row">
            <a href="#" class="rounded-lg bg-cyan-400 px-5 py-3 text-center font-semibold text-slate-950">Explorar cursos →</a>
            <a href="#" class="rounded-lg border border-slate-700 px-5 py-3 text-center font-semibold text-cyan-400">Ver leaderboard</a>
          </div>
        </div>
        <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <p class="font-semibold">Entrá a tu cuenta</p>
          <p class="mt-1 text-sm text-slate-400">Formulario completo en el nodo «El panel central: hero y acceso».</p>
        </div>
      </section>

      <!-- Grilla: 1 → 2 (sm) → 4 (lg) columnas -->
      <section id="cursos" aria-labelledby="titulo-cursos">
        <h2 id="titulo-cursos" class="mb-4 text-xl font-bold lg:text-2xl">Rutas de entrenamiento</h2>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <article class="rounded-xl border border-cyan-400/60 bg-slate-900 p-4">C++ Moderno</article>
          <article class="rounded-xl border border-slate-800 bg-slate-900 p-4">SDL3 &amp; Game Loops</article>
          <article class="rounded-xl border border-slate-800 bg-slate-900 p-4">OpenGL 4.6</article>
          <article class="rounded-xl border border-slate-800 bg-slate-900 p-4">WebAssembly</article>
          <article class="rounded-xl border border-slate-800 bg-slate-900 p-4">Python</article>
          <article class="rounded-xl border border-slate-800 bg-slate-900 p-4">Spring Boot</article>
          <article class="rounded-xl border border-slate-800 bg-slate-900 p-4">TypeScript</article>
          <article class="rounded-xl border border-slate-800 bg-slate-900 p-4">Phaser</article>
        </div>
      </section>

      <p class="font-mono text-sm text-cyan-400">
        <span class="sm:hidden">celular (&lt; sm)</span>
        <span class="hidden sm:inline md:hidden">sm: 40rem o más</span>
        <span class="hidden md:inline lg:hidden">md: 48rem o más</span>
        <span class="hidden lg:inline">lg: 64rem o más</span>
      </p>
    </main>

    <!-- Barra inferior: fija y SOLO en el celular (md:hidden) -->
    <nav aria-label="Secciones" class="fixed inset-x-0 bottom-0 z-10 flex h-16 border-t border-slate-800 bg-slate-900 text-xs md:hidden">
      <a href="#cursos" class="flex flex-1 flex-col items-center justify-center text-slate-400"><span aria-hidden="true">🗺</span>Campañas</a>
      <a href="#" class="flex flex-1 flex-col items-center justify-center text-slate-400"><span aria-hidden="true">📖</span>Lecciones</a>
      <a href="#" aria-current="page" class="flex flex-1 flex-col items-center justify-center text-cyan-400"><span aria-hidden="true">⚔</span>Arena</a>
      <a href="#" class="flex flex-1 flex-col items-center justify-center text-slate-400"><span aria-hidden="true">🌳</span>Árbol</a>
    </nav>
  </body>
</html>
```

### ¿Para qué sirve?

En cualquier proyecto con Tailwind, el diseño adaptable se escribe así: una clase para el celular y otra con prefijo para pantallas más grandes, en la misma línea. Es muchísimo más rápido que mantener media queries en un archivo aparte, y se ve de un vistazo cómo cambia cada pieza.

### Errores habituales

**Ogro: pensar en "desktop first"**: `lg:hidden` en un elemento que solo querés en la computadora lo oculta **en la computadora**. Lo correcto: `hidden lg:block`.

**Ogro: prefijo sin la base**: `md:grid-cols-2` sin `grid`: no hay grilla a la que cambiarle las columnas.

**Troll: la barra fija tapa el final**: falta `pb-16` en el `body` (y `md:pb-0` para sacarlo cuando la barra desaparece).

**Orco del Desborde: algo con ancho fijo** (`w-[500px]`) se sale en el celular. Usá `w-full max-w-[500px]`.

### Prueba del sello

#### ¿Qué significa `md:` exactamente?

"Desde 48 rem (768 px) **en adelante**". No significa "en tablets": `md:flex` también se aplica en una pantalla de 1920 px.

#### ¿Cómo mostrás algo **solo** en el celular? ¿Y solo en la computadora?

Solo en el celular: visible y con `md:hidden`. Solo en la compu: `hidden md:block` (o `hidden md:flex`): oculto de entrada y visible desde `md`.

#### ¿Por qué el mismo `mx-auto max-w-7xl px-4` va en la cabecera y en el `main`?

Para que el contenido de las dos partes quede **alineado** con los mismos bordes: el mismo ancho máximo, centrado, y el mismo margen a los costados en el celular.

### Misión R03-N04-M1 · La fila adaptable

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá una fila del ranking que en el celular muestre **puesto, nombre y puntos**, y desde `md` se convierta en una grilla de **5 columnas** que suma la especialidad y la racha (como la tabla de la versión de compu de esta plataforma).

#### Criterio de aprobación

- En *Celular* se ven tres datos; en *Compu*, cinco columnas.
- Especialidad y racha aparecen solo desde `md` (`hidden md:block`).
- La grilla usa `md:grid md:grid-cols-5` (o columnas a medida).

#### Cómo debe quedar

celular: capturas/R03-N04-M1-celular.webp
compu: capturas/R03-N04-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La fila adaptable</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Fila del ranking adaptable</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-slate-950 p-4 text-slate-200">
    <!-- Celular: puesto, nombre y puntos. Desde md aparecen especialidad y racha -->
    <div class="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-900 px-4 py-3 md:grid md:grid-cols-[3rem_1fr_1fr_6rem_6rem]">
      <span class="font-mono text-cyan-400">#04</span>
      <span class="min-w-0 flex-1 truncate font-semibold">@ZeroByte_Arg</span>
      <span class="hidden text-slate-400 md:block">C++ Moderno / Memory Guru</span>
      <span class="hidden md:block">🔥 14d</span>
      <span class="text-right font-mono">10.900 XP</span>
    </div>
  </body>
</html>
```


### Misión R03-N04-M2 · El texto que crece

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Escribí un título que pase de `text-2xl` a `text-4xl` desde `sm` y a `text-6xl` desde `lg`, y un párrafo con el ancho de línea limitado en pantallas grandes.

#### Criterio de aprobación

- El título usa `text-2xl sm:text-4xl lg:text-6xl`.
- El párrafo tiene un ancho máximo (`max-w-prose` o similar).

#### Cómo debe quedar

celular: capturas/R03-N04-M2-celular.webp
compu: capturas/R03-N04-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El texto que crece</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Texto que crece</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-slate-950 p-4 text-slate-200 md:p-10">
    <h1 class="text-2xl font-black sm:text-4xl lg:text-6xl">Liga Obsidiana</h1>
    <p class="mt-2 text-sm text-slate-400 lg:max-w-xl lg:text-lg">El texto, el padding y el ancho de línea crecen con la pantalla.</p>
  </body>
</html>
```


### Encargo R03-N04-E1 · La portada de la inmobiliaria

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Una inmobiliaria quiere su portada: el título centrado en el celular y alineado a la izquierda desde `md`, y las propiedades en **1 → 2 → 3** columnas.

#### Criterio de aprobación

- El título usa `text-center md:text-left`.
- Las propiedades pasan de 1 a 2 y a 3 columnas con prefijos.

#### Cómo debe quedar

celular: capturas/R03-N04-E1-celular.webp
compu: capturas/R03-N04-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La portada de la inmobiliaria</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Inmobiliaria Costa</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-white text-slate-800">
    <main class="mx-auto max-w-6xl px-4 py-8">
      <h1 class="text-center text-3xl font-bold md:text-left md:text-5xl">Encontrá tu casa en la costa</h1>
      <div class="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <article class="rounded-xl border p-4"><h2 class="font-semibold">Casa 3 ambientes</h2><p class="text-slate-500">USD 85.000</p></article>
        <article class="rounded-xl border p-4"><h2 class="font-semibold">Depto. frente al mar</h2><p class="text-slate-500">USD 120.000</p></article>
        <article class="rounded-xl border p-4"><h2 class="font-semibold">Lote 600 m²</h2><p class="text-slate-500">USD 30.000</p></article>
      </div>
    </main>
  </body>
</html>
```

## R03-N05 · Estados y transiciones

```meta
tipo: tema
padre: R03-N04
precio: 10
criatura: troll
temas: css.animaciones, css.frameworks
usa: html.formularios
```

### Crónica

Un vitral vivo cambia con la luz: brilla cuando alguien se acerca y se oscurece cuando no se puede pasar. Zed toca una tarjeta y no pasa nada. —¿Está rota?

—No está rota —dice {mentor}—. Está **muda**. Toda pieza que se puede tocar tiene que responder, {heroe}: al mouse, al dedo y al teclado.

### Objetivos

Dar respuesta visual a la interacción con **variantes** de estado (`hover:`, `focus-visible:`, `active:`, `disabled:`), reaccionar al estado de un padre (`group`), de un hermano (`peer`) o de lo que hay adentro (`has-`), y animar los cambios con `transition`. Todo sin JavaScript.

### Antes de empezar

- Utilidades y responsive con Tailwind (de «Las utilidades» a «Responsive con Tailwind»). Formularios («Formularios»).

### Explicación

#### Variantes: "esta clase, solo cuando…"
| Variante | Cuándo se aplica |
|---|---|
| `hover:` | el mouse está encima (en el celular casi no existe: no dependas de él) |
| `focus-visible:` | tiene el foco **con teclado** (Tab): ¡imprescindible para la accesibilidad! |
| `focus:` | tiene el foco (también con clic o toque) |
| `active:` | se está apretando |
| `disabled:` | el elemento está desactivado |
| `user-invalid:` | el campo es inválido **después** de que la persona lo tocó |
| `placeholder:` | el texto de ayuda del campo |
| `open:` | un `details` está abierto |
| `aria-[current=page]:` | el elemento tiene `aria-current="page"` |
| `motion-reduce:` | la persona pidió en su sistema "reducir movimiento" |

Se combinan con los prefijos de tamaño: `md:hover:underline`.

#### Padre, hermano, contenido
| Técnica | Cómo | Ejemplo |
|---|---|---|
| **group** | `group` en el padre, `group-hover:` en los hijos | al pasar sobre la tarjeta, el título se pone cian |
| **peer** | `peer` en un elemento, `peer-checked:` / `peer-user-invalid:` en un **hermano que viene después** | mensaje de error debajo del campo; interruptor |
| **has** | `has-checked:` en el contenedor | la etiqueta del filtro se pinta si su radio está elegido |

`sr-only` esconde algo **a la vista** pero no al lector de pantalla: los radios de los filtros siguen existiendo (y se manejan con el teclado), solo que lo que se ve es la etiqueta.

#### Transiciones
`transition` anima los cambios de color, sombra, opacidad y movimiento (150 ms por defecto); `duration-300` lo hace más lento. `hover:-translate-y-1` levanta la tarjeta, `active:scale-95` la "aprieta". Con `motion-reduce:transition-none` se respeta a quien se marea con las animaciones.

#### El ejemplo

Botones, tarjeta con `group`, filtros con `has-checked`, campo de email con `user-invalid` y `peer`, y menú con `aria-current`.

**Probalo**: pasá el mouse, apretá Tab para recorrer con el teclado, escribí un email sin `@` y salí del campo, tocá los filtros.

#### Cómo se ve el ejemplo

La captura muestra el estado inicial. Interactuando: el botón brilla y se achica al apretarlo; la tarjeta sube, se ilumina su borde y aparece "Entrenar →"; el filtro elegido se pinta de cian; con un email inválido, el borde se pone rojo y aparece "Ese email no es válido."; con Tab, cada control muestra un contorno cian.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Estados y transiciones</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-slate-950 p-5 text-slate-200 antialiased">
    <main class="mx-auto max-w-3xl space-y-10">
      <!-- 1) Boton con hover, foco de teclado y "apretado" -->
      <section aria-labelledby="t1" class="space-y-3">
        <h2 id="t1" class="font-mono text-xs tracking-widest text-cyan-400 uppercase">1 · Botones</h2>
        <div class="flex flex-wrap gap-3">
          <button type="button" class="rounded-lg bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 hover:shadow-lg hover:shadow-cyan-400/40 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cyan-300 active:scale-95">Entrar a la terminal →</button>
          <button type="button" disabled class="rounded-lg bg-cyan-400 px-5 py-3 font-semibold text-slate-950 disabled:cursor-not-allowed disabled:opacity-40">Desactivado</button>
        </div>
      </section>

      <!-- 2) Tarjeta: al pasar sobre el PADRE (group) cambian los hijos -->
      <section aria-labelledby="t2" class="space-y-3">
        <h2 id="t2" class="font-mono text-xs tracking-widest text-cyan-400 uppercase">2 · Tarjeta con group-hover</h2>
        <a href="#" class="group block rounded-xl border border-slate-800 bg-slate-900 p-5 transition duration-300 hover:-translate-y-1 hover:border-cyan-400/60 hover:shadow-xl hover:shadow-cyan-500/10 motion-reduce:transition-none motion-reduce:hover:translate-y-0">
          <p class="font-mono text-xs text-slate-400">MOD-10</p>
          <h3 class="mt-1 font-semibold transition group-hover:text-cyan-300">OpenGL 4.6 &amp; GLSL</h3>
          <p class="mt-3 text-sm text-slate-400">Shaders, texturas e iluminación Phong.</p>
          <p class="mt-4 text-sm text-cyan-400 opacity-0 transition group-hover:opacity-100">Entrenar →</p>
        </a>
      </section>

      <!-- 3) Filtros sin JavaScript: radios escondidos + has-checked en la etiqueta -->
      <section aria-labelledby="t3" class="space-y-3">
        <h2 id="t3" class="font-mono text-xs tracking-widest text-cyan-400 uppercase">3 · Filtros (has-checked)</h2>
        <fieldset class="flex flex-wrap gap-2">
          <legend class="sr-only">Filtrar rutas</legend>
          <label class="cursor-pointer rounded-md border border-slate-700 px-3 py-1 text-sm transition has-checked:border-cyan-400 has-checked:bg-cyan-400 has-checked:text-slate-950 has-focus-visible:outline-2 has-focus-visible:outline-cyan-300">
            <input type="radio" name="filtro" class="sr-only" checked> Todos (23)
          </label>
          <label class="cursor-pointer rounded-md border border-slate-700 px-3 py-1 text-sm transition has-checked:border-cyan-400 has-checked:bg-cyan-400 has-checked:text-slate-950 has-focus-visible:outline-2 has-focus-visible:outline-cyan-300">
            <input type="radio" name="filtro" class="sr-only"> Bajo nivel / C++
          </label>
          <label class="cursor-pointer rounded-md border border-slate-700 px-3 py-1 text-sm transition has-checked:border-cyan-400 has-checked:bg-cyan-400 has-checked:text-slate-950 has-focus-visible:outline-2 has-focus-visible:outline-cyan-300">
            <input type="radio" name="filtro" class="sr-only"> Gráficos &amp; Shaders
          </label>
        </fieldset>
      </section>

      <!-- 4) Campo con foco y error (user-invalid: solo despues de que la persona escribio) -->
      <section aria-labelledby="t4" class="space-y-3">
        <h2 id="t4" class="font-mono text-xs tracking-widest text-cyan-400 uppercase">4 · Formularios</h2>
        <form action="#" class="max-w-sm space-y-1">
          <label for="email" class="block text-xs tracking-wider text-slate-400 uppercase">Email</label>
          <input id="email" type="email" required placeholder="kira@codexia.dev" class="peer w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 placeholder:text-slate-600 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/30 focus:outline-none user-invalid:border-red-400">
          <p class="hidden text-sm text-red-400 peer-user-invalid:block">Ese email no es válido.</p>
          <button type="submit" class="mt-2 rounded-lg border border-slate-700 px-4 py-2 text-sm hover:border-cyan-400">Suscribirme</button>
        </form>
      </section>

      <!-- 5) Menu: el enlace de la pagina actual se marca con aria-current -->
      <section aria-labelledby="t5" class="space-y-3">
        <h2 id="t5" class="font-mono text-xs tracking-widest text-cyan-400 uppercase">5 · Enlace actual</h2>
        <nav aria-label="Ejemplo" class="flex gap-2 text-sm">
          <a href="#" class="rounded-md px-3 py-1.5 text-slate-400 hover:text-slate-200">Cursos</a>
          <a href="#" aria-current="page" class="rounded-md px-3 py-1.5 text-slate-400 hover:text-slate-200 aria-[current=page]:bg-cyan-400/10 aria-[current=page]:text-cyan-300">Top 10</a>
          <a href="#" class="rounded-md px-3 py-1.5 text-slate-400 hover:text-slate-200">Bóveda</a>
        </nav>
      </section>
    </main>
  </body>
</html>
```

### ¿Para qué sirve?

Un botón que cambia al pasar el mouse, un campo que se marca en rojo cuando está mal, un interruptor de "recordarme": son los detalles que hacen que una página se sienta como una aplicación. Y el foco visible con el teclado no es un adorno: es lo que permite usar la página a quien no puede usar un mouse.

### Errores habituales

**Ogro: `peer` después del hermano.** `peer-*` solo funciona en elementos que vienen
**después** del que tiene `peer` (es una regla de CSS: `~`).

**Ogro: quitar el contorno de foco** (`outline-none`) sin poner otro: quien navega con teclado no sabe dónde está. Si sacás el de fábrica, poné `focus-visible:outline-*` o `focus:ring-*`.

**Ogro: el error aparece antes de escribir.** Con `invalid:` el campo vacío y obligatorio ya está en rojo al cargar la página; `user-invalid:` espera a que la persona lo use.

**Esqueleto: un filtro hecho con `display: none` en el radio**: deja de funcionar con el teclado y el lector de pantalla. Usá `sr-only`.

### Prueba del sello

#### ¿Qué diferencia hay entre `focus:` y `focus-visible:`?

`focus:` se aplica cada vez que el elemento tiene el foco, también al hacer clic con el mouse. `focus-visible:` solo cuando el foco llega **con el teclado** (Tab): ahí es donde hace falta ver dónde estás.

#### ¿Para qué sirven `group` y `peer`? ¿Qué limitación tiene `peer`?

`group` en un padre permite que sus hijos reaccionen al estado del padre (`group-hover:`). `peer` en un elemento permite que **un hermano** reaccione a su estado (`peer-checked:`). La limitación: `peer` solo funciona con hermanos que vienen **después** en el HTML.

#### ¿Por qué `sr-only` y no `hidden` para esconder un radio?

Porque `hidden` lo saca del todo: no se puede elegir con el teclado ni lo lee el lector de pantalla. `sr-only` lo esconde **solo a la vista**: sigue funcionando y accesible.

### Misión R03-N05-M1 · La fila con hover

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá una fila del ranking que, al pasar el mouse, **cambie el fondo**, pinte el puesto de cian y muestre una flecha que **se desliza**. Todo con transición.

#### Criterio de aprobación

- La fila es un `group` y sus partes reaccionan con `group-hover:`.
- Los cambios tienen `transition`.
- También responde al teclado (`focus-visible:` si es un enlace).

#### Cómo debe quedar

celular: capturas/R03-N05-M1-celular.webp
compu: capturas/R03-N05-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La fila con hover</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Fila con hover</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-slate-950 p-4 text-slate-200">
    <a href="#" class="group flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-900 px-4 py-3 transition hover:border-cyan-400/60 hover:bg-slate-800 focus-visible:outline-2 focus-visible:outline-cyan-300">
      <span class="font-mono text-slate-400 group-hover:text-cyan-400">4</span>
      <span class="flex-1 font-semibold">@ZeroByte_Arg</span>
      <span class="font-mono">10.900 XP</span>
      <span class="translate-x-0 text-cyan-400 opacity-0 transition group-hover:translate-x-1 group-hover:opacity-100" aria-hidden="true">→</span>
    </a>
  </body>
</html>
```


### Misión R03-N05-M2 · El interruptor

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá un **"Recordarme en esta terminal"** con forma de interruptor: un checkbox con `peer sr-only` y un `span` que dibuja el interruptor, con la bolita hecha con `after:`.

#### Criterio de aprobación

- El checkbox es real (`input type="checkbox"`), con `peer sr-only`, y tiene su `label`.
- El interruptor cambia con `peer-checked:` (color y posición de la bolita).
- Se puede usar con el teclado.

#### Cómo debe quedar

celular: capturas/R03-N05-M2-celular.webp
compu: capturas/R03-N05-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El interruptor</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Interruptor sin JavaScript</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-slate-950 p-4 text-slate-200">
    <label class="flex cursor-pointer items-center gap-3">
      <input type="checkbox" class="peer sr-only" checked>
      <!-- El "riel" y la "bolita" reaccionan al checkbox hermano (peer) -->
      <span class="relative h-6 w-11 rounded-full bg-slate-700 transition peer-checked:bg-cyan-400 peer-focus-visible:outline-2 peer-focus-visible:outline-cyan-300 after:absolute after:top-0.5 after:left-0.5 after:size-5 after:rounded-full after:bg-white after:transition peer-checked:after:translate-x-5"></span>
      Recordarme en esta terminal
    </label>
  </body>
</html>
```


### Encargo R03-N05-E1 · Las preguntas frecuentes

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Una tienda quiere sus preguntas frecuentes con `details` y `summary`: se abren y se cierran **sin JavaScript**, y la flecha gira con `group-open:rotate-180`.

#### Criterio de aprobación

- Usa `details`/`summary` (sin JavaScript).
- La flecha gira al abrir (`group-open:rotate-180`).

#### Cómo debe quedar

celular: capturas/R03-N05-E1-celular.webp
compu: capturas/R03-N05-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Las preguntas frecuentes</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
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
    <title>Preguntas frecuentes</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-white p-4 text-slate-800">
    <h1 class="mb-4 text-2xl font-bold">Preguntas frecuentes</h1>
    <!-- details/summary: se abre y cierra sin JavaScript; open: estiliza el estado abierto -->
    <details class="group rounded-lg border p-4 open:bg-slate-50">
      <summary class="flex cursor-pointer list-none justify-between font-semibold">
        ¿Hacen envíos?
        <span class="transition group-open:rotate-180" aria-hidden="true">▾</span>
      </summary>
      <p class="mt-2 text-slate-600">Sí, a todo el país en 48 horas.</p>
    </details>
    <details class="group mt-2 rounded-lg border p-4 open:bg-slate-50">
      <summary class="flex cursor-pointer list-none justify-between font-semibold">
        ¿Puedo devolver un producto?
        <span class="transition group-open:rotate-180" aria-hidden="true">▾</span>
      </summary>
      <p class="mt-2 text-slate-600">Dentro de los 30 días.</p>
    </details>
  </body>
</html>
```

## R03-N06 · Tema propio

```meta
tipo: tema
padre: R03-N05
precio: 10
criatura: skeleton
temas: css.temas
usa: css.frameworks, css.selectores
```

### Crónica

Cada taller tiene sus colores. Los de GhecoSoft son el azul noche, el cian neón y el oro de los campeones. Copiaste `#22d3ee` en veinte lugares y, cuando el Gremio pide un cian "un poquito más claro", tenés que cambiar los veinte.

—Grabá los colores **en el cofre**, {heroe} —te enseña {mentor}—. Una vez. Y que todo lo demás los use por su nombre.

### Objetivos

Definir la identidad visual del proyecto en un solo lugar con `@theme` (colores, fuentes, sombras, animaciones), poner estilos de fábrica con `@layer base` y crear utilidades propias con `@utility`.

### Antes de empezar

- Variables CSS («Primeros vidrios: CSS»). Utilidades y estados (de «Las utilidades» a «Estados y transiciones»).

### Explicación

#### `@theme`: los tokens del diseño
Dentro de `@theme` —en el bloque `<style type="text/tailwindcss">`, o en `entrada.css` en tu compu— cada variable con un nombre especial **genera clases**:

| Variable en `@theme` | Clases que crea |
|---|---|
| `--color-neon: #22d3ee;` | `text-neon`, `bg-neon`, `border-neon`, `bg-neon/10`, `shadow-neon/30`… |
| `--font-display: "Space Grotesk", …;` | `font-display` |
| `--font-mono: "JetBrains Mono", …;` | **reemplaza** a `font-mono` |
| `--shadow-brillo: …;` | `shadow-brillo` |
| `--animate-latido: latido 1.6s …;` + `@keyframes` | `animate-latido` |
| `--breakpoint-3xl: 120rem;` | el prefijo `3xl:` |

Ventajas: un cambio de color se hace en **un** lugar; los nombres hablan del proyecto (`bg-panel` en vez de `bg-[#0e1626]`); y como son **variables CSS**, se pueden pisar en una parte de la página (misión 1: otro tema con las mismas clases).

#### `@layer base`: estilos de fábrica
Para cosas que valen para **todas** las etiquetas de un tipo (el fondo del `body`, la letra de los títulos). Adentro, `@apply` permite usar clases de Tailwind:
```css
@layer base {
  body { @apply bg-fondo text-slate-200 antialiased; }
  h1, h2, h3 { @apply font-display; }
}
```
#### `@utility`: utilidades propias
Para un efecto que Tailwind no trae (el fondo cuadriculado de esta plataforma, un brillo en el texto). Se usan como cualquier clase y aceptan variantes: `hover:texto-neon`, `md:fondo-cuadricula`.

#### Fuentes
Se cargan con el `<link>` de Google Fonts en el `head` y se nombran en el tema, **con fuentes de reserva** al final: sin internet, la página igual se ve bien.

#### El ejemplo

Este tema es el que usa el proyecto (de «El marco: navegación» a «Jefe final: el Dragón de los Talleres»).

#### Cómo se ve el ejemplo

Tocá *Celular* y *Compu* en la vista previa: fondo azul muy oscuro con una cuadrícula cian tenue, la píldora con un punto verde que **late**, el título en Space Grotesk con "árbol de habilidades" brillando, cuatro muestras de color y la tarjeta con brillo neón.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Tema GhecoSoft</title>
    <!-- Fuentes de Google (si no hay internet, se usan las de reserva del tema) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&amp;family=Space+Grotesk:wght@500;700&amp;display=swap">
    <style type="text/tailwindcss">
      @import "tailwindcss";

      /* 1) TEMA: cada variable crea clases nuevas.
            --color-neon  ->  bg-neon, text-neon, border-neon, shadow-neon/30...
            --font-display -> font-display */
      @theme {
        --color-fondo: #070b16;
        --color-panel: #0e1626;
        --color-borde: #1d2a42;
        --color-neon: #22d3ee;
        --color-neon-suave: #67e8f9;
        --color-oro: #fbbf24;
        --color-fuego: #fb923c;

        --font-display: "Space Grotesk", system-ui, sans-serif;
        --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;

        --shadow-brillo: 0 0 0 1px rgb(34 211 238 / 35%), 0 0 24px rgb(34 211 238 / 25%);

        /* Animacion propia: animate-latido */
        --animate-latido: latido 1.6s ease-in-out infinite;
        @keyframes latido {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      }

      /* 2) BASE: estilos de fabrica para etiquetas (en vez de repetir clases en cada una) */
      @layer base {
        body {
          @apply bg-fondo font-sans text-slate-200 antialiased;
        }
        h1, h2, h3 {
          @apply font-display;
        }
      }

      /* 3) UTILIDADES PROPIAS: se usan como cualquier clase (y aceptan hover:, md:...) */
      @utility fondo-cuadricula {
        background-image:
          linear-gradient(rgb(34 211 238 / 6%) 1px, transparent 1px),
          linear-gradient(90deg, rgb(34 211 238 / 6%) 1px, transparent 1px);
        background-size: 32px 32px;
      }

      @utility texto-neon {
        text-shadow: 0 0 12px rgb(34 211 238 / 60%);
      }
    </style>
  </head>
  <body>
    <main class="fondo-cuadricula min-h-screen p-5 md:p-10">
      <div class="mx-auto max-w-3xl space-y-8">
        <p class="inline-flex items-center gap-2 rounded-full border border-neon/40 bg-neon/10 px-3 py-1 font-mono text-xs tracking-widest text-neon uppercase">
          <span class="size-2 animate-latido rounded-full bg-emerald-400"></span> Plataforma de cursos
        </p>

        <h1 class="text-4xl leading-tight font-bold md:text-5xl">
          Aprendé a programar avanzando por tu <span class="texto-neon text-neon">árbol de habilidades</span>.
        </h1>

        <!-- Tokens del tema: cada muestra usa una clase generada por @theme -->
        <section aria-labelledby="paleta">
          <h2 id="paleta" class="mb-3 text-lg font-bold">Paleta del tema</h2>
          <ul class="grid grid-cols-2 gap-3 font-mono text-xs sm:grid-cols-4">
            <li class="rounded-lg border border-borde bg-panel p-3">bg-panel</li>
            <li class="rounded-lg bg-neon p-3 text-fondo">bg-neon</li>
            <li class="rounded-lg bg-oro p-3 text-fondo">bg-oro</li>
            <li class="rounded-lg bg-fuego p-3 text-fondo">bg-fuego</li>
          </ul>
        </section>

        <article class="max-w-sm rounded-xl border border-borde bg-panel p-5 shadow-brillo">
          <p class="font-mono text-xs text-slate-400">MOD-04 · font-mono</p>
          <h3 class="mt-1 text-lg">C++ Moderno · font-display</h3>
          <p class="mt-2 text-sm text-slate-400">La sombra <code class="font-mono text-neon-suave">shadow-brillo</code> es un token del tema.</p>
        </article>
      </div>
    </main>
  </body>
</html>
```

### ¿Para qué sirve?

Las empresas definen su marca —colores, letras, sombras— en un solo lugar, el **sistema de diseño**, y todas sus páginas y apps lo usan. Cuando cambian el color de la marca, cambian una línea. Es exactamente lo que hace `@theme`, y la razón por la que existen los "modo oscuro" que se activan con un botón.

### Errores habituales

**Esqueleto: la clase del tema no existe.** El nombre tiene que empezar con el prefijo correcto: `--color-…` para colores, `--font-…` para letras. `--neon` a secas no crea ninguna clase.

**Ogro: `@apply` para todo.** Convertir cada componente en `.boton { @apply … }` es volver a escribir CSS con otra sintaxis y perder las ventajas de Tailwind. Usalo en la base y en casos puntuales («Componentes»).

**Ogro: las fuentes no cambian.** Sin internet, o con el `<link>` de Google Fonts mal escrito, se usan las de reserva. En DevTools → *Calculado* → `font-family` se ve cuál se está usando de verdad.

### Prueba del sello

#### ¿Qué clases crea `--color-oro: #fbbf24;`?

Todas las de color con el nombre `oro`: `text-oro`, `bg-oro`, `border-oro`, `ring-oro`, `from-oro`, `shadow-oro`… y con transparencia, como `bg-oro/20`.

#### ¿Para qué sirve `@layer base` y cuándo no conviene `@apply`?

`@layer base` define estilos de fábrica para **etiquetas** (el fondo del `body`, la letra de los títulos), sin repetir clases en cada una. `@apply` no conviene para convertir cada elemento en una clase propia: termina siendo escribir CSS de nuevo, con otra sintaxis.

#### ¿Por qué las fuentes del tema terminan en `system-ui, sans-serif`?

Son las fuentes **de reserva**: si no hay internet o Google Fonts tarda en cargar, la página usa la letra del sistema y se sigue viendo bien.

### Misión R03-N06-M1 · La Liga Amatista

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

En el editor ya está el tema de GhecoSoft. Pisá sus variables dentro de una clase **`.tema-amatista`** y mostrá una tarjeta violeta usando **las mismas clases** de siempre (`bg-panel`, `text-neon`…).

#### Criterio de aprobación

- La clase `.tema-amatista` redefine variables del tema (`--color-neon`, `--color-panel`…).
- La tarjeta violeta usa las mismas clases que una tarjeta normal.
- Fuera de `.tema-amatista` todo sigue cian.

#### Cómo debe quedar

celular: capturas/R03-N06-M1-celular.webp
compu: capturas/R03-N06-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La Liga Amatista</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";

      /* 1) TEMA: cada variable crea clases nuevas.
            --color-neon  ->  bg-neon, text-neon, border-neon, shadow-neon/30...
            --font-display -> font-display */
      @theme {
        --color-fondo: #070b16;
        --color-panel: #0e1626;
        --color-borde: #1d2a42;
        --color-neon: #22d3ee;
        --color-neon-suave: #67e8f9;
        --color-oro: #fbbf24;
        --color-fuego: #fb923c;

        --font-display: "Space Grotesk", system-ui, sans-serif;
        --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;

        --shadow-brillo: 0 0 0 1px rgb(34 211 238 / 35%), 0 0 24px rgb(34 211 238 / 25%);

        /* Animacion propia: animate-latido */
        --animate-latido: latido 1.6s ease-in-out infinite;
        @keyframes latido {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      }

      /* 2) BASE: estilos de fabrica para etiquetas (en vez de repetir clases en cada una) */
      @layer base {
        body {
          @apply bg-fondo font-sans text-slate-200 antialiased;
        }
        h1, h2, h3 {
          @apply font-display;
        }
      }

      /* 3) UTILIDADES PROPIAS: se usan como cualquier clase (y aceptan hover:, md:...) */
      @utility fondo-cuadricula {
        background-image:
          linear-gradient(rgb(34 211 238 / 6%) 1px, transparent 1px),
          linear-gradient(90deg, rgb(34 211 238 / 6%) 1px, transparent 1px);
        background-size: 32px 32px;
      }

      @utility texto-neon {
        text-shadow: 0 0 12px rgb(34 211 238 / 60%);
      }
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
    <title>Otro tema: Liga Amatista</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";

      /* 1) TEMA: cada variable crea clases nuevas.
            --color-neon  ->  bg-neon, text-neon, border-neon, shadow-neon/30...
            --font-display -> font-display */
      @theme {
        --color-fondo: #070b16;
        --color-panel: #0e1626;
        --color-borde: #1d2a42;
        --color-neon: #22d3ee;
        --color-neon-suave: #67e8f9;
        --color-oro: #fbbf24;
        --color-fuego: #fb923c;

        --font-display: "Space Grotesk", system-ui, sans-serif;
        --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;

        --shadow-brillo: 0 0 0 1px rgb(34 211 238 / 35%), 0 0 24px rgb(34 211 238 / 25%);

        /* Animacion propia: animate-latido */
        --animate-latido: latido 1.6s ease-in-out infinite;
        @keyframes latido {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      }

      /* 2) BASE: estilos de fabrica para etiquetas (en vez de repetir clases en cada una) */
      @layer base {
        body {
          @apply bg-fondo font-sans text-slate-200 antialiased;
        }
        h1, h2, h3 {
          @apply font-display;
        }
      }

      /* 3) UTILIDADES PROPIAS: se usan como cualquier clase (y aceptan hover:, md:...) */
      @utility fondo-cuadricula {
        background-image:
          linear-gradient(rgb(34 211 238 / 6%) 1px, transparent 1px),
          linear-gradient(90deg, rgb(34 211 238 / 6%) 1px, transparent 1px);
        background-size: 32px 32px;
      }

      @utility texto-neon {
        text-shadow: 0 0 12px rgb(34 211 238 / 60%);
      }
    </style>
    <!-- Los tokens del tema son variables CSS: se pueden pisar para una parte de la pagina -->
    <style>
      .tema-amatista {
        --color-neon: #c084fc;
        --color-neon-suave: #e9d5ff;
        --color-panel: #1a1027;
        --color-borde: #3b2357;
      }
    </style>
  </head>
  <body>
    <main class="tema-amatista p-5">
      <article class="max-w-sm rounded-xl border border-borde bg-panel p-5">
        <p class="font-mono text-xs text-neon-suave">MOD-23</p>
        <h1 class="mt-1 text-lg text-neon">TypeScript Pro</h1>
        <p class="mt-2 text-sm">Mismas clases, otros valores.</p>
      </article>
    </main>
  </body>
</html>
```


### Misión R03-N06-M2 · La utilidad en acción

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Usá las utilidades propias del tema: una palabra gigante que **brilla solo al pasar el mouse** (`hover:texto-neon`) sobre el fondo cuadriculado (`fondo-cuadricula`).

#### Criterio de aprobación

- Usa las utilidades del tema (`fondo-cuadricula`, `texto-neon`).
- El brillo aparece solo con `hover:`.

#### Cómo debe quedar

celular: capturas/R03-N06-M2-celular.webp
compu: capturas/R03-N06-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La utilidad en acción</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";

      /* 1) TEMA: cada variable crea clases nuevas.
            --color-neon  ->  bg-neon, text-neon, border-neon, shadow-neon/30...
            --font-display -> font-display */
      @theme {
        --color-fondo: #070b16;
        --color-panel: #0e1626;
        --color-borde: #1d2a42;
        --color-neon: #22d3ee;
        --color-neon-suave: #67e8f9;
        --color-oro: #fbbf24;
        --color-fuego: #fb923c;

        --font-display: "Space Grotesk", system-ui, sans-serif;
        --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;

        --shadow-brillo: 0 0 0 1px rgb(34 211 238 / 35%), 0 0 24px rgb(34 211 238 / 25%);

        /* Animacion propia: animate-latido */
        --animate-latido: latido 1.6s ease-in-out infinite;
        @keyframes latido {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      }

      /* 2) BASE: estilos de fabrica para etiquetas (en vez de repetir clases en cada una) */
      @layer base {
        body {
          @apply bg-fondo font-sans text-slate-200 antialiased;
        }
        h1, h2, h3 {
          @apply font-display;
        }
      }

      /* 3) UTILIDADES PROPIAS: se usan como cualquier clase (y aceptan hover:, md:...) */
      @utility fondo-cuadricula {
        background-image:
          linear-gradient(rgb(34 211 238 / 6%) 1px, transparent 1px),
          linear-gradient(90deg, rgb(34 211 238 / 6%) 1px, transparent 1px);
        background-size: 32px 32px;
      }

      @utility texto-neon {
        text-shadow: 0 0 12px rgb(34 211 238 / 60%);
      }
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
    <title>Utilidades del tema en acción</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";

      /* 1) TEMA: cada variable crea clases nuevas.
            --color-neon  ->  bg-neon, text-neon, border-neon, shadow-neon/30...
            --font-display -> font-display */
      @theme {
        --color-fondo: #070b16;
        --color-panel: #0e1626;
        --color-borde: #1d2a42;
        --color-neon: #22d3ee;
        --color-neon-suave: #67e8f9;
        --color-oro: #fbbf24;
        --color-fuego: #fb923c;

        --font-display: "Space Grotesk", system-ui, sans-serif;
        --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;

        --shadow-brillo: 0 0 0 1px rgb(34 211 238 / 35%), 0 0 24px rgb(34 211 238 / 25%);

        /* Animacion propia: animate-latido */
        --animate-latido: latido 1.6s ease-in-out infinite;
        @keyframes latido {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      }

      /* 2) BASE: estilos de fabrica para etiquetas (en vez de repetir clases en cada una) */
      @layer base {
        body {
          @apply bg-fondo font-sans text-slate-200 antialiased;
        }
        h1, h2, h3 {
          @apply font-display;
        }
      }

      /* 3) UTILIDADES PROPIAS: se usan como cualquier clase (y aceptan hover:, md:...) */
      @utility fondo-cuadricula {
        background-image:
          linear-gradient(rgb(34 211 238 / 6%) 1px, transparent 1px),
          linear-gradient(90deg, rgb(34 211 238 / 6%) 1px, transparent 1px);
        background-size: 32px 32px;
      }

      @utility texto-neon {
        text-shadow: 0 0 12px rgb(34 211 238 / 60%);
      }
    </style>
  </head>
  <body>
    <main class="fondo-cuadricula grid min-h-screen place-items-center p-5">
      <p class="font-display text-5xl font-bold text-neon hover:texto-neon">HOVER</p>
    </main>
  </body>
</html>
```


### Encargo R03-N06-E1 · La marca de la cafetería

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Una cafetería quiere su marca: crema, blanco y marrón, usando **los mismos tokens del tema** (`bg-fondo`, `text-neon`…) con otros valores.

#### Criterio de aprobación

- Cambia los valores de las variables del tema, no las clases del HTML.
- La paleta es crema, blanco y marrón.

#### Cómo debe quedar

celular: capturas/R03-N06-E1-celular.webp
compu: capturas/R03-N06-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La marca de la cafetería</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";

      /* 1) TEMA: cada variable crea clases nuevas.
            --color-neon  ->  bg-neon, text-neon, border-neon, shadow-neon/30...
            --font-display -> font-display */
      @theme {
        --color-fondo: #070b16;
        --color-panel: #0e1626;
        --color-borde: #1d2a42;
        --color-neon: #22d3ee;
        --color-neon-suave: #67e8f9;
        --color-oro: #fbbf24;
        --color-fuego: #fb923c;

        --font-display: "Space Grotesk", system-ui, sans-serif;
        --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;

        --shadow-brillo: 0 0 0 1px rgb(34 211 238 / 35%), 0 0 24px rgb(34 211 238 / 25%);

        /* Animacion propia: animate-latido */
        --animate-latido: latido 1.6s ease-in-out infinite;
        @keyframes latido {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      }

      /* 2) BASE: estilos de fabrica para etiquetas (en vez de repetir clases en cada una) */
      @layer base {
        body {
          @apply bg-fondo font-sans text-slate-200 antialiased;
        }
        h1, h2, h3 {
          @apply font-display;
        }
      }

      /* 3) UTILIDADES PROPIAS: se usan como cualquier clase (y aceptan hover:, md:...) */
      @utility fondo-cuadricula {
        background-image:
          linear-gradient(rgb(34 211 238 / 6%) 1px, transparent 1px),
          linear-gradient(90deg, rgb(34 211 238 / 6%) 1px, transparent 1px);
        background-size: 32px 32px;
      }

      @utility texto-neon {
        text-shadow: 0 0 12px rgb(34 211 238 / 60%);
      }
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
    <title>Marca de una cafetería</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";

      /* 1) TEMA: cada variable crea clases nuevas.
            --color-neon  ->  bg-neon, text-neon, border-neon, shadow-neon/30...
            --font-display -> font-display */
      @theme {
        --color-fondo: #070b16;
        --color-panel: #0e1626;
        --color-borde: #1d2a42;
        --color-neon: #22d3ee;
        --color-neon-suave: #67e8f9;
        --color-oro: #fbbf24;
        --color-fuego: #fb923c;

        --font-display: "Space Grotesk", system-ui, sans-serif;
        --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;

        --shadow-brillo: 0 0 0 1px rgb(34 211 238 / 35%), 0 0 24px rgb(34 211 238 / 25%);

        /* Animacion propia: animate-latido */
        --animate-latido: latido 1.6s ease-in-out infinite;
        @keyframes latido {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      }

      /* 2) BASE: estilos de fabrica para etiquetas (en vez de repetir clases en cada una) */
      @layer base {
        body {
          @apply bg-fondo font-sans text-slate-200 antialiased;
        }
        h1, h2, h3 {
          @apply font-display;
        }
      }

      /* 3) UTILIDADES PROPIAS: se usan como cualquier clase (y aceptan hover:, md:...) */
      @utility fondo-cuadricula {
        background-image:
          linear-gradient(rgb(34 211 238 / 6%) 1px, transparent 1px),
          linear-gradient(90deg, rgb(34 211 238 / 6%) 1px, transparent 1px);
        background-size: 32px 32px;
      }

      @utility texto-neon {
        text-shadow: 0 0 12px rgb(34 211 238 / 60%);
      }
    </style>
    <style>
      /* Paleta de la marca: se reutilizan las clases del tema con otros valores */
      .marca-cafe {
        --color-fondo: #f6ecd9;
        --color-panel: #ffffff;
        --color-borde: #e4d3b4;
        --color-neon: #7c4a2d;
      }
    </style>
  </head>
  <body>
    <main class="marca-cafe min-h-screen bg-fondo p-5 text-stone-800">
      <h1 class="text-3xl font-bold text-neon">Café del Puerto</h1>
      <article class="mt-4 max-w-xs rounded-xl border border-borde bg-panel p-4">
        <h2 class="font-semibold">Café con leche</h2>
        <p class="font-mono text-neon">$2500</p>
      </article>
    </main>
  </body>
</html>
```

## R03-N07 · Componentes

```meta
tipo: tema
padre: R03-N06
precio: 10
criatura: orc
temas: css.temas
usa: css.frameworks
```

### Crónica

El **Orco del Desborde** asoma la cabeza por la puerta: la misma tarjeta, copiada treinta veces con treinta diferencias chiquitas, y nadie sabe cuál es la buena. Cada copia mal hecha lo hace más fuerte.

{mentor} cuelga en la pared del taller un **muestrario**: cada pieza una sola vez, la oficial. —Desde hoy, {heroe}, se copia de acá.

### Objetivos

Organizar las piezas que se repiten: decidir cuándo repetir clases y cuándo crear un
**componente** con `@utility` + `@apply`, y armar la **guía de estilo** de GhecoSoft (botones, chips, avatares, tarjeta de curso, barras, campo, título de sección) que usa el proyecto.

### Antes de empezar

- Tema propio («Tema propio»). Estados («Estados y transiciones»).

### Explicación

#### El problema
Con Tailwind, una tarjeta tiene 10–15 clases. Si aparece en 30 lugares y hay que cambiar el borde, son 30 cambios. Hay tres soluciones, de la mejor a la peor:

1. **Que la pieza exista una sola vez en el código.** En un proyecto real, el HTML lo genera algo: un componente de React (en el Archipiélago de los Espejos, el curso de React Native), una plantilla de PHP/Blade (en el Puerto de Elefa, el curso de PHP), un `for` en JavaScript (en la Feria de las Luces, el curso de JavaScript). La tarjeta se escribe **una** vez y se repite con datos distintos.
2. **Un componente de CSS** para piezas chicas que se repiten **siempre iguales** (botones, chips):
   ```css
   @utility btn {
     @apply inline-flex items-center justify-center gap-2 rounded-lg px-5 py-3 font-semibold transition …;
   }
   @utility btn-primario {
     @apply bg-neon text-fondo hover:bg-neon-suave;
   }
   ```
   ```html
   <a class="btn btn-primario">Continuar</a>
   <a class="btn btn-primario w-full sm:w-auto">Entrar</a>   <!-- se combina con clases sueltas -->
   ```
   Con `@utility` (y no con una clase común) el componente acepta variantes (`md:btn`) y se ordena bien con las demás clases.
3. **Copiar y pegar** desde la guía de estilo, en una página estática como esta. Es lo que hacemos en el proyecto porque todavía no hay JavaScript ni servidor: por eso el muestrario es importante.

**No conviertas todo en componentes.** Si cada `div` tiene su `.algo { @apply … }`, volviste a escribir CSS con otra sintaxis.

#### Las piezas del kit
| Pieza | Clave del diseño |
|---|---|
| botón | `btn` + `btn-primario` / `btn-secundario` |
| chip / filtro | `chip`; el elegido con `bg-neon text-fondo` |
| píldora | `rounded-full border` + color al 40 % |
| avatar | `size-*` + `rounded-full` + `object-cover` (imagen) o iniciales centradas |
| tarjeta de curso | `tarjeta` + `shadow-brillo` si está activa |
| barra de progreso | caja `bg-borde` + relleno con `w-*` y el color del curso |
| campo | `focus:border-neon focus:ring-2 focus:ring-neon/30` |
| título de sección | etiqueta mono chica + título en `font-display` |

`object-cover` hace que una imagen llene su caja recortando lo que sobra, sin deformarse (avatares).

#### Cómo se ve el ejemplo

Tocá *Celular* y *Compu* en la vista previa: los tres botones, los chips y píldoras, los avatares (iniciales, el héroe y Gheco), la tarjeta de C++ igual a la de esta plataforma, tres barras de colores, el campo con su botón y el título de sección.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Kit de componentes GhecoSoft</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&amp;family=Space+Grotesk:wght@500;700&amp;display=swap">
    <style type="text/tailwindcss">
      @import "tailwindcss";

      /* 1) TEMA: cada variable crea clases nuevas.
            --color-neon  ->  bg-neon, text-neon, border-neon, shadow-neon/30...
            --font-display -> font-display */
      @theme {
        --color-fondo: #070b16;
        --color-panel: #0e1626;
        --color-borde: #1d2a42;
        --color-neon: #22d3ee;
        --color-neon-suave: #67e8f9;
        --color-oro: #fbbf24;
        --color-fuego: #fb923c;

        --font-display: "Space Grotesk", system-ui, sans-serif;
        --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;

        --shadow-brillo: 0 0 0 1px rgb(34 211 238 / 35%), 0 0 24px rgb(34 211 238 / 25%);

        /* Animacion propia: animate-latido */
        --animate-latido: latido 1.6s ease-in-out infinite;
        @keyframes latido {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      }

      /* 2) BASE: estilos de fabrica para etiquetas (en vez de repetir clases en cada una) */
      @layer base {
        body {
          @apply bg-fondo font-sans text-slate-200 antialiased;
        }
        h1, h2, h3 {
          @apply font-display;
        }
      }

      /* 3) UTILIDADES PROPIAS: se usan como cualquier clase (y aceptan hover:, md:...) */
      @utility fondo-cuadricula {
        background-image:
          linear-gradient(rgb(34 211 238 / 6%) 1px, transparent 1px),
          linear-gradient(90deg, rgb(34 211 238 / 6%) 1px, transparent 1px);
        background-size: 32px 32px;
      }

      @utility texto-neon {
        text-shadow: 0 0 12px rgb(34 211 238 / 60%);
      }

      /* 4) COMPONENTES: solo para piezas que se repiten MUCHO y siempre iguales.
            Se definen con @utility para que acepten variantes (hover:, md:...)
            y se puedan combinar con otras clases en el HTML. */
      @utility btn {
        @apply inline-flex items-center justify-center gap-2 rounded-lg px-5 py-3 font-semibold whitespace-nowrap transition
          focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-neon active:scale-95;
      }

      @utility btn-primario {
        @apply bg-neon text-fondo hover:bg-neon-suave hover:shadow-lg hover:shadow-neon/30;
      }

      @utility btn-secundario {
        @apply border border-borde text-neon hover:border-neon/60 hover:bg-neon/5;
      }

      @utility tarjeta {
        @apply rounded-xl border border-borde bg-panel p-5;
      }

      @utility chip {
        @apply rounded-md border border-borde px-3 py-1 text-sm transition;
      }

      @utility etiqueta-mono {
        @apply font-mono text-xs tracking-widest uppercase;
      }

      /* Respetar "reducir movimiento" del sistema: sin animaciones decorativas */
      @layer base {
        @media (prefers-reduced-motion: reduce) {
          *,
          *::before,
          *::after {
            animation: none !important;
            transition: none !important;
          }
        }
      }
    </style>
  </head>
  <body>
    <main class="mx-auto max-w-5xl space-y-12 p-5 md:p-10">
      <header>
        <p class="etiqueta-mono text-neon">Guía de estilo</p>
        <h1 class="mt-1 text-3xl font-bold">Kit de componentes</h1>
        <p class="mt-2 text-slate-400">Cada pieza que usa la plataforma, una sola vez, para copiar.</p>
      </header>

      <!-- Botones: componente (btn + variante) -->
      <section aria-labelledby="c-botones" class="space-y-3">
        <h2 id="c-botones" class="etiqueta-mono text-slate-400">Botones</h2>
        <div class="flex flex-wrap gap-3">
          <a href="#" class="btn btn-primario">▷ Continuar campaña</a>
          <a href="#" class="btn btn-secundario">Nodos</a>
          <!-- Un componente se puede ajustar con clases sueltas -->
          <a href="#" class="btn btn-primario w-full sm:w-auto">Entrar a la terminal →</a>
        </div>
      </section>

      <!-- Chips y pildoras -->
      <section aria-labelledby="c-chips" class="space-y-3">
        <h2 id="c-chips" class="etiqueta-mono text-slate-400">Chips, píldoras e insignias</h2>
        <div class="flex flex-wrap items-center gap-2">
          <span class="chip border-neon bg-neon text-fondo">Todos (23)</span>
          <span class="chip">Bajo nivel / C++</span>
          <span class="rounded-full border border-emerald-400/40 px-2 py-0.5 font-mono text-xs text-emerald-400">23 módulos</span>
          <span class="rounded bg-emerald-400/15 px-2 py-0.5 font-mono text-xs text-emerald-400">ACTIVO</span>
          <span class="rounded bg-violet-600 px-1.5 font-mono text-[10px] font-bold text-white">LV.14</span>
        </div>
      </section>

      <!-- Avatares -->
      <section aria-labelledby="c-avatares" class="space-y-3">
        <h2 id="c-avatares" class="etiqueta-mono text-slate-400">Avatares</h2>
        <div class="flex items-end gap-4">
          <span class="grid size-10 place-items-center rounded-lg bg-borde">🦊</span>
          <span class="grid size-14 place-items-center rounded-full border-2 border-slate-300 font-display font-bold text-slate-200">VAL</span>
          <span class="grid size-20 place-items-center rounded-full border-2 border-oro bg-oro/10 font-display text-xl font-bold text-oro shadow-lg shadow-oro/30">NEO</span>
          <img src="/img/cursos/html/heroe-avatar.webp" alt="Avatar de @GhecoDev" width="80" height="80" class="size-20 rounded-full border-2 border-neon object-cover shadow-brillo">
          <img src="/img/cursos/html/gheco-logo.webp" alt="Gheco, la mascota" width="56" height="56" class="size-14 rounded-xl ring-1 ring-neon/40">
        </div>
      </section>

      <!-- Tarjeta de curso: componente "tarjeta" + contenido propio -->
      <section aria-labelledby="c-tarjeta" class="space-y-3">
        <h2 id="c-tarjeta" class="etiqueta-mono text-slate-400">Tarjeta de curso</h2>
        <article class="tarjeta flex max-w-sm flex-col gap-3 border-neon/60 shadow-brillo">
          <div class="flex items-center justify-between">
            <span class="rounded bg-neon/10 px-2 py-0.5 font-mono text-xs text-neon">MOD-04</span>
            <span class="font-mono text-xs text-emerald-400">Core activo</span>
          </div>
          <h3 class="text-lg font-bold">04-C++ Moderno &amp; Videojuegos</h3>
          <p class="text-sm text-slate-400">Gestión de memoria, RAII, Smart Pointers y C++20.</p>
          <div>
            <div class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-neon">18 / 24</span></div>
            <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de C++ Moderno" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
              <div class="h-full w-3/4 rounded-full bg-neon"></div>
            </div>
          </div>
          <div class="flex items-center justify-between">
            <span class="font-mono text-sm text-neon">+350 XP <span class="text-slate-500">| Intermedio</span></span>
            <a href="#" class="btn btn-primario px-3 py-1 text-xs">Continuar</a>
          </div>
        </article>
      </section>

      <!-- Barras de progreso: cada curso con su color -->
      <section aria-labelledby="c-barras" class="space-y-3">
        <h2 id="c-barras" class="etiqueta-mono text-slate-400">Barras de progreso</h2>
        <div class="max-w-sm space-y-2">
          <div class="h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="SDL3" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[45%] bg-violet-400"></div></div>
          <div class="h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Python" aria-valuenow="70" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[70%] bg-oro"></div></div>
          <div class="h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Spring Boot" aria-valuenow="66" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-2/3 bg-rose-500"></div></div>
        </div>
      </section>

      <!-- Campo de formulario -->
      <section aria-labelledby="c-campo" class="space-y-3">
        <h2 id="c-campo" class="etiqueta-mono text-slate-400">Campo</h2>
        <form action="#" class="max-w-sm space-y-1">
          <label for="usuario" class="etiqueta-mono block text-slate-400">Usuario o email</label>
          <input id="usuario" type="text" class="w-full rounded-lg border border-borde bg-fondo px-3 py-2.5 placeholder:text-slate-600 focus:border-neon focus:ring-2 focus:ring-neon/30 focus:outline-none" placeholder="cliente">
          <button type="submit" class="btn btn-primario mt-3 w-full">Entrar</button>
        </form>
      </section>

      <!-- Titulo de seccion -->
      <section aria-labelledby="c-titulo" class="space-y-3">
        <h2 id="c-titulo" class="etiqueta-mono text-slate-400">Título de sección</h2>
        <div>
          <p class="etiqueta-mono inline-block rounded border border-neon/40 px-2 py-0.5 text-[10px] text-neon">Directorio curricular</p>
          <p class="mt-2 font-display text-2xl font-bold">Rutas de Entrenamiento Tecnológico</p>
        </div>
      </section>
    </main>
  </body>
</html>
```

### ¿Para qué sirve?

Las empresas tienen su **guía de estilo** (o *design system*): la página donde está cada botón, cada campo y cada tarjeta, la versión oficial. Diseñadores y programadores trabajan desde ahí. Y cuando el HTML lo genera un programa —PHP, Java, React—, cada pieza se escribe una sola vez y se repite con datos distintos.

### Errores habituales

**Ogro: `@apply` con una clase que no existe** (mal escrita, o un color que no está en el `@theme`): el CLI **se detiene** y no actualiza `salida.css`. Es de los pocos errores que sí avisan:
```
Error: Cannot apply unknown utility class `bg-neon`
```

**Ogro: componente que no se deja ajustar.** Si `btn` pone `px-5` y en el HTML agregás `px-3`, gana la que Tailwind ordenó después. Con `@utility` las clases sueltas del HTML se pueden sumar sin pelear (como en "Continuar", que achica el padding).

**Orco: la tarjeta copiada que se desvía.** Si se cambia en un lugar, cambiala en la guía primero.

### Prueba del sello

#### Nombrá las tres formas de evitar repetir una tarjeta. ¿Cuál es la mejor y por qué?

1) Que la pieza exista **una sola vez en el código** (una plantilla de PHP, un componente de React, un bucle en JavaScript); 2) un componente de CSS con `@utility` y `@apply`; 3) copiarla de la guía de estilo. La mejor es la primera: un cambio se hace en un lugar y todas las copias quedan iguales.

#### ¿Cuándo conviene un componente con `@apply` y cuándo no?

Conviene para piezas **chicas** que se repiten **siempre iguales**: botones, chips, campos. No conviene para todo: si cada `div` tiene su clase con `@apply`, volviste a escribir CSS con otra sintaxis.

#### ¿Para qué sirve una guía de estilo en una página estática?

Es la **fuente oficial** de cada pieza: como no hay un programa que genere el HTML, se copia de ahí y todas las páginas quedan iguales. También sirve para ver todas las piezas juntas y probar un cambio del tema de un vistazo.

### Misión R03-N07-M1 · Las alertas

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá tres avisos —éxito, advertencia y error— **reutilizando el componente `tarjeta`** del tema y cambiando solo los colores con clases sueltas.

#### Criterio de aprobación

- Los tres avisos usan la clase `tarjeta`.
- El color de cada uno sale de clases sueltas agregadas, no de componentes nuevos.

#### Cómo debe quedar

celular: capturas/R03-N07-M1-celular.webp
compu: capturas/R03-N07-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Las alertas</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";

      /* 1) TEMA: cada variable crea clases nuevas.
            --color-neon  ->  bg-neon, text-neon, border-neon, shadow-neon/30...
            --font-display -> font-display */
      @theme {
        --color-fondo: #070b16;
        --color-panel: #0e1626;
        --color-borde: #1d2a42;
        --color-neon: #22d3ee;
        --color-neon-suave: #67e8f9;
        --color-oro: #fbbf24;
        --color-fuego: #fb923c;

        --font-display: "Space Grotesk", system-ui, sans-serif;
        --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;

        --shadow-brillo: 0 0 0 1px rgb(34 211 238 / 35%), 0 0 24px rgb(34 211 238 / 25%);

        /* Animacion propia: animate-latido */
        --animate-latido: latido 1.6s ease-in-out infinite;
        @keyframes latido {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      }

      /* 2) BASE: estilos de fabrica para etiquetas (en vez de repetir clases en cada una) */
      @layer base {
        body {
          @apply bg-fondo font-sans text-slate-200 antialiased;
        }
        h1, h2, h3 {
          @apply font-display;
        }
      }

      /* 3) UTILIDADES PROPIAS: se usan como cualquier clase (y aceptan hover:, md:...) */
      @utility fondo-cuadricula {
        background-image:
          linear-gradient(rgb(34 211 238 / 6%) 1px, transparent 1px),
          linear-gradient(90deg, rgb(34 211 238 / 6%) 1px, transparent 1px);
        background-size: 32px 32px;
      }

      @utility texto-neon {
        text-shadow: 0 0 12px rgb(34 211 238 / 60%);
      }

      /* 4) COMPONENTES: solo para piezas que se repiten MUCHO y siempre iguales.
            Se definen con @utility para que acepten variantes (hover:, md:...)
            y se puedan combinar con otras clases en el HTML. */
      @utility btn {
        @apply inline-flex items-center justify-center gap-2 rounded-lg px-5 py-3 font-semibold whitespace-nowrap transition
          focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-neon active:scale-95;
      }

      @utility btn-primario {
        @apply bg-neon text-fondo hover:bg-neon-suave hover:shadow-lg hover:shadow-neon/30;
      }

      @utility btn-secundario {
        @apply border border-borde text-neon hover:border-neon/60 hover:bg-neon/5;
      }

      @utility tarjeta {
        @apply rounded-xl border border-borde bg-panel p-5;
      }

      @utility chip {
        @apply rounded-md border border-borde px-3 py-1 text-sm transition;
      }

      @utility etiqueta-mono {
        @apply font-mono text-xs tracking-widest uppercase;
      }

      /* Respetar "reducir movimiento" del sistema: sin animaciones decorativas */
      @layer base {
        @media (prefers-reduced-motion: reduce) {
          *,
          *::before,
          *::after {
            animation: none !important;
            transition: none !important;
          }
        }
      }
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
    <title>Componente alerta</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";

      /* 1) TEMA: cada variable crea clases nuevas.
            --color-neon  ->  bg-neon, text-neon, border-neon, shadow-neon/30...
            --font-display -> font-display */
      @theme {
        --color-fondo: #070b16;
        --color-panel: #0e1626;
        --color-borde: #1d2a42;
        --color-neon: #22d3ee;
        --color-neon-suave: #67e8f9;
        --color-oro: #fbbf24;
        --color-fuego: #fb923c;

        --font-display: "Space Grotesk", system-ui, sans-serif;
        --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;

        --shadow-brillo: 0 0 0 1px rgb(34 211 238 / 35%), 0 0 24px rgb(34 211 238 / 25%);

        /* Animacion propia: animate-latido */
        --animate-latido: latido 1.6s ease-in-out infinite;
        @keyframes latido {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      }

      /* 2) BASE: estilos de fabrica para etiquetas (en vez de repetir clases en cada una) */
      @layer base {
        body {
          @apply bg-fondo font-sans text-slate-200 antialiased;
        }
        h1, h2, h3 {
          @apply font-display;
        }
      }

      /* 3) UTILIDADES PROPIAS: se usan como cualquier clase (y aceptan hover:, md:...) */
      @utility fondo-cuadricula {
        background-image:
          linear-gradient(rgb(34 211 238 / 6%) 1px, transparent 1px),
          linear-gradient(90deg, rgb(34 211 238 / 6%) 1px, transparent 1px);
        background-size: 32px 32px;
      }

      @utility texto-neon {
        text-shadow: 0 0 12px rgb(34 211 238 / 60%);
      }

      /* 4) COMPONENTES: solo para piezas que se repiten MUCHO y siempre iguales.
            Se definen con @utility para que acepten variantes (hover:, md:...)
            y se puedan combinar con otras clases en el HTML. */
      @utility btn {
        @apply inline-flex items-center justify-center gap-2 rounded-lg px-5 py-3 font-semibold whitespace-nowrap transition
          focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-neon active:scale-95;
      }

      @utility btn-primario {
        @apply bg-neon text-fondo hover:bg-neon-suave hover:shadow-lg hover:shadow-neon/30;
      }

      @utility btn-secundario {
        @apply border border-borde text-neon hover:border-neon/60 hover:bg-neon/5;
      }

      @utility tarjeta {
        @apply rounded-xl border border-borde bg-panel p-5;
      }

      @utility chip {
        @apply rounded-md border border-borde px-3 py-1 text-sm transition;
      }

      @utility etiqueta-mono {
        @apply font-mono text-xs tracking-widest uppercase;
      }

      /* Respetar "reducir movimiento" del sistema: sin animaciones decorativas */
      @layer base {
        @media (prefers-reduced-motion: reduce) {
          *,
          *::before,
          *::after {
            animation: none !important;
            transition: none !important;
          }
        }
      }
    </style>
  </head>
  <body>
    <main class="space-y-3 p-5">
      <!-- Misma estructura, el color se cambia con clases sueltas -->
      <p class="tarjeta flex gap-3 border-emerald-400/40 py-3 text-emerald-300"><span aria-hidden="true">✔</span> Nodo desbloqueado: Smart Pointers.</p>
      <p class="tarjeta flex gap-3 border-oro/40 py-3 text-oro"><span aria-hidden="true">⚠</span> Tu racha se corta en 2 horas.</p>
      <p class="tarjeta flex gap-3 border-rose-400/40 py-3 text-rose-300"><span aria-hidden="true">✘</span> El compilador encontró 3 errores.</p>
    </main>
  </body>
</html>
```


### Misión R03-N07-M2 · Las tarjetas chicas

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá las dos tarjetas chicas de la versión celular de esta plataforma: **"TypeScript Pro"** y **"Spring Boot Cloud"**, usando las piezas del kit.

#### Criterio de aprobación

- Las dos tarjetas comparten la misma estructura y las mismas clases; solo cambian los datos y el color.
- Usan las piezas del kit (`tarjeta`, `chip`, barra de progreso).

#### Cómo debe quedar

celular: capturas/R03-N07-M2-celular.webp
compu: capturas/R03-N07-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Las tarjetas chicas</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";

      /* 1) TEMA: cada variable crea clases nuevas.
            --color-neon  ->  bg-neon, text-neon, border-neon, shadow-neon/30...
            --font-display -> font-display */
      @theme {
        --color-fondo: #070b16;
        --color-panel: #0e1626;
        --color-borde: #1d2a42;
        --color-neon: #22d3ee;
        --color-neon-suave: #67e8f9;
        --color-oro: #fbbf24;
        --color-fuego: #fb923c;

        --font-display: "Space Grotesk", system-ui, sans-serif;
        --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;

        --shadow-brillo: 0 0 0 1px rgb(34 211 238 / 35%), 0 0 24px rgb(34 211 238 / 25%);

        /* Animacion propia: animate-latido */
        --animate-latido: latido 1.6s ease-in-out infinite;
        @keyframes latido {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      }

      /* 2) BASE: estilos de fabrica para etiquetas (en vez de repetir clases en cada una) */
      @layer base {
        body {
          @apply bg-fondo font-sans text-slate-200 antialiased;
        }
        h1, h2, h3 {
          @apply font-display;
        }
      }

      /* 3) UTILIDADES PROPIAS: se usan como cualquier clase (y aceptan hover:, md:...) */
      @utility fondo-cuadricula {
        background-image:
          linear-gradient(rgb(34 211 238 / 6%) 1px, transparent 1px),
          linear-gradient(90deg, rgb(34 211 238 / 6%) 1px, transparent 1px);
        background-size: 32px 32px;
      }

      @utility texto-neon {
        text-shadow: 0 0 12px rgb(34 211 238 / 60%);
      }

      /* 4) COMPONENTES: solo para piezas que se repiten MUCHO y siempre iguales.
            Se definen con @utility para que acepten variantes (hover:, md:...)
            y se puedan combinar con otras clases en el HTML. */
      @utility btn {
        @apply inline-flex items-center justify-center gap-2 rounded-lg px-5 py-3 font-semibold whitespace-nowrap transition
          focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-neon active:scale-95;
      }

      @utility btn-primario {
        @apply bg-neon text-fondo hover:bg-neon-suave hover:shadow-lg hover:shadow-neon/30;
      }

      @utility btn-secundario {
        @apply border border-borde text-neon hover:border-neon/60 hover:bg-neon/5;
      }

      @utility tarjeta {
        @apply rounded-xl border border-borde bg-panel p-5;
      }

      @utility chip {
        @apply rounded-md border border-borde px-3 py-1 text-sm transition;
      }

      @utility etiqueta-mono {
        @apply font-mono text-xs tracking-widest uppercase;
      }

      /* Respetar "reducir movimiento" del sistema: sin animaciones decorativas */
      @layer base {
        @media (prefers-reduced-motion: reduce) {
          *,
          *::before,
          *::after {
            animation: none !important;
            transition: none !important;
          }
        }
      }
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
    <title>Tarjetas chicas</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";

      /* 1) TEMA: cada variable crea clases nuevas.
            --color-neon  ->  bg-neon, text-neon, border-neon, shadow-neon/30...
            --font-display -> font-display */
      @theme {
        --color-fondo: #070b16;
        --color-panel: #0e1626;
        --color-borde: #1d2a42;
        --color-neon: #22d3ee;
        --color-neon-suave: #67e8f9;
        --color-oro: #fbbf24;
        --color-fuego: #fb923c;

        --font-display: "Space Grotesk", system-ui, sans-serif;
        --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;

        --shadow-brillo: 0 0 0 1px rgb(34 211 238 / 35%), 0 0 24px rgb(34 211 238 / 25%);

        /* Animacion propia: animate-latido */
        --animate-latido: latido 1.6s ease-in-out infinite;
        @keyframes latido {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      }

      /* 2) BASE: estilos de fabrica para etiquetas (en vez de repetir clases en cada una) */
      @layer base {
        body {
          @apply bg-fondo font-sans text-slate-200 antialiased;
        }
        h1, h2, h3 {
          @apply font-display;
        }
      }

      /* 3) UTILIDADES PROPIAS: se usan como cualquier clase (y aceptan hover:, md:...) */
      @utility fondo-cuadricula {
        background-image:
          linear-gradient(rgb(34 211 238 / 6%) 1px, transparent 1px),
          linear-gradient(90deg, rgb(34 211 238 / 6%) 1px, transparent 1px);
        background-size: 32px 32px;
      }

      @utility texto-neon {
        text-shadow: 0 0 12px rgb(34 211 238 / 60%);
      }

      /* 4) COMPONENTES: solo para piezas que se repiten MUCHO y siempre iguales.
            Se definen con @utility para que acepten variantes (hover:, md:...)
            y se puedan combinar con otras clases en el HTML. */
      @utility btn {
        @apply inline-flex items-center justify-center gap-2 rounded-lg px-5 py-3 font-semibold whitespace-nowrap transition
          focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-neon active:scale-95;
      }

      @utility btn-primario {
        @apply bg-neon text-fondo hover:bg-neon-suave hover:shadow-lg hover:shadow-neon/30;
      }

      @utility btn-secundario {
        @apply border border-borde text-neon hover:border-neon/60 hover:bg-neon/5;
      }

      @utility tarjeta {
        @apply rounded-xl border border-borde bg-panel p-5;
      }

      @utility chip {
        @apply rounded-md border border-borde px-3 py-1 text-sm transition;
      }

      @utility etiqueta-mono {
        @apply font-mono text-xs tracking-widest uppercase;
      }

      /* Respetar "reducir movimiento" del sistema: sin animaciones decorativas */
      @layer base {
        @media (prefers-reduced-motion: reduce) {
          *,
          *::before,
          *::after {
            animation: none !important;
            transition: none !important;
          }
        }
      }
    </style>
  </head>
  <body>
    <main class="grid grid-cols-2 gap-3 p-5">
      <article class="tarjeta p-3">
        <p class="font-mono text-xs"><span class="rounded bg-sky-400/15 px-1 text-sky-300">TS</span> 23 · TYPE-SYS</p>
        <h1 class="mt-2 text-sm font-bold">TypeScript Pro</h1>
        <p class="mt-1 flex justify-between font-mono text-xs"><span class="text-neon">12 Nodos</span><span class="text-slate-400">+290 XP</span></p>
      </article>
      <article class="tarjeta p-3">
        <p class="font-mono text-xs"><span class="rounded bg-rose-400/15 px-1 text-rose-300">JV</span> 20 · SPRING</p>
        <h2 class="mt-2 text-sm font-bold">Spring Boot Cloud</h2>
        <p class="mt-1 flex justify-between font-mono text-xs"><span class="text-neon">16 Nodos</span><span class="text-slate-400">+310 XP</span></p>
      </article>
    </main>
  </body>
</html>
```


### Encargo R03-N07-E1 · El kit de la verdulería

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Una verdulería quiere su kit: los mismos componentes (botón, chip, tarjeta) con la marca de la tienda, **pisando las variables del tema** como en «Tema propio».

#### Criterio de aprobación

- Usa los mismos componentes del kit.
- La marca sale de pisar las variables del tema.

#### Cómo debe quedar

celular: capturas/R03-N07-E1-celular.webp
compu: capturas/R03-N07-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El kit de la verdulería</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";

      /* 1) TEMA: cada variable crea clases nuevas.
            --color-neon  ->  bg-neon, text-neon, border-neon, shadow-neon/30...
            --font-display -> font-display */
      @theme {
        --color-fondo: #070b16;
        --color-panel: #0e1626;
        --color-borde: #1d2a42;
        --color-neon: #22d3ee;
        --color-neon-suave: #67e8f9;
        --color-oro: #fbbf24;
        --color-fuego: #fb923c;

        --font-display: "Space Grotesk", system-ui, sans-serif;
        --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;

        --shadow-brillo: 0 0 0 1px rgb(34 211 238 / 35%), 0 0 24px rgb(34 211 238 / 25%);

        /* Animacion propia: animate-latido */
        --animate-latido: latido 1.6s ease-in-out infinite;
        @keyframes latido {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      }

      /* 2) BASE: estilos de fabrica para etiquetas (en vez de repetir clases en cada una) */
      @layer base {
        body {
          @apply bg-fondo font-sans text-slate-200 antialiased;
        }
        h1, h2, h3 {
          @apply font-display;
        }
      }

      /* 3) UTILIDADES PROPIAS: se usan como cualquier clase (y aceptan hover:, md:...) */
      @utility fondo-cuadricula {
        background-image:
          linear-gradient(rgb(34 211 238 / 6%) 1px, transparent 1px),
          linear-gradient(90deg, rgb(34 211 238 / 6%) 1px, transparent 1px);
        background-size: 32px 32px;
      }

      @utility texto-neon {
        text-shadow: 0 0 12px rgb(34 211 238 / 60%);
      }

      /* 4) COMPONENTES: solo para piezas que se repiten MUCHO y siempre iguales.
            Se definen con @utility para que acepten variantes (hover:, md:...)
            y se puedan combinar con otras clases en el HTML. */
      @utility btn {
        @apply inline-flex items-center justify-center gap-2 rounded-lg px-5 py-3 font-semibold whitespace-nowrap transition
          focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-neon active:scale-95;
      }

      @utility btn-primario {
        @apply bg-neon text-fondo hover:bg-neon-suave hover:shadow-lg hover:shadow-neon/30;
      }

      @utility btn-secundario {
        @apply border border-borde text-neon hover:border-neon/60 hover:bg-neon/5;
      }

      @utility tarjeta {
        @apply rounded-xl border border-borde bg-panel p-5;
      }

      @utility chip {
        @apply rounded-md border border-borde px-3 py-1 text-sm transition;
      }

      @utility etiqueta-mono {
        @apply font-mono text-xs tracking-widest uppercase;
      }

      /* Respetar "reducir movimiento" del sistema: sin animaciones decorativas */
      @layer base {
        @media (prefers-reduced-motion: reduce) {
          *,
          *::before,
          *::after {
            animation: none !important;
            transition: none !important;
          }
        }
      }
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
    <title>Kit de una tienda</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";

      /* 1) TEMA: cada variable crea clases nuevas.
            --color-neon  ->  bg-neon, text-neon, border-neon, shadow-neon/30...
            --font-display -> font-display */
      @theme {
        --color-fondo: #070b16;
        --color-panel: #0e1626;
        --color-borde: #1d2a42;
        --color-neon: #22d3ee;
        --color-neon-suave: #67e8f9;
        --color-oro: #fbbf24;
        --color-fuego: #fb923c;

        --font-display: "Space Grotesk", system-ui, sans-serif;
        --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;

        --shadow-brillo: 0 0 0 1px rgb(34 211 238 / 35%), 0 0 24px rgb(34 211 238 / 25%);

        /* Animacion propia: animate-latido */
        --animate-latido: latido 1.6s ease-in-out infinite;
        @keyframes latido {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      }

      /* 2) BASE: estilos de fabrica para etiquetas (en vez de repetir clases en cada una) */
      @layer base {
        body {
          @apply bg-fondo font-sans text-slate-200 antialiased;
        }
        h1, h2, h3 {
          @apply font-display;
        }
      }

      /* 3) UTILIDADES PROPIAS: se usan como cualquier clase (y aceptan hover:, md:...) */
      @utility fondo-cuadricula {
        background-image:
          linear-gradient(rgb(34 211 238 / 6%) 1px, transparent 1px),
          linear-gradient(90deg, rgb(34 211 238 / 6%) 1px, transparent 1px);
        background-size: 32px 32px;
      }

      @utility texto-neon {
        text-shadow: 0 0 12px rgb(34 211 238 / 60%);
      }

      /* 4) COMPONENTES: solo para piezas que se repiten MUCHO y siempre iguales.
            Se definen con @utility para que acepten variantes (hover:, md:...)
            y se puedan combinar con otras clases en el HTML. */
      @utility btn {
        @apply inline-flex items-center justify-center gap-2 rounded-lg px-5 py-3 font-semibold whitespace-nowrap transition
          focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-neon active:scale-95;
      }

      @utility btn-primario {
        @apply bg-neon text-fondo hover:bg-neon-suave hover:shadow-lg hover:shadow-neon/30;
      }

      @utility btn-secundario {
        @apply border border-borde text-neon hover:border-neon/60 hover:bg-neon/5;
      }

      @utility tarjeta {
        @apply rounded-xl border border-borde bg-panel p-5;
      }

      @utility chip {
        @apply rounded-md border border-borde px-3 py-1 text-sm transition;
      }

      @utility etiqueta-mono {
        @apply font-mono text-xs tracking-widest uppercase;
      }

      /* Respetar "reducir movimiento" del sistema: sin animaciones decorativas */
      @layer base {
        @media (prefers-reduced-motion: reduce) {
          *,
          *::before,
          *::after {
            animation: none !important;
            transition: none !important;
          }
        }
      }
    </style>
    <style>
      .marca-tienda {
        --color-fondo: #ffffff;
        --color-panel: #f8fafc;
        --color-borde: #e2e8f0;
        --color-neon: #16a34a;
        --color-neon-suave: #22c55e;
      }
    </style>
  </head>
  <body>
    <main class="marca-tienda min-h-screen space-y-4 bg-fondo p-5 text-slate-800">
      <h1 class="text-2xl font-bold">Verdulería Don Tito</h1>
      <div class="flex gap-2"><span class="chip border-neon bg-neon text-white">Frutas</span><span class="chip">Verduras</span></div>
      <article class="tarjeta max-w-xs">
        <h2 class="font-semibold">Manzana roja</h2>
        <p class="font-mono text-neon">$2200 / kg</p>
        <a href="#" class="btn btn-primario mt-3 w-full text-white">Agregar al carrito</a>
      </article>
    </main>
  </body>
</html>
```

## R03-N08 · Jefe: el Orco del Desborde

```meta
tipo: jefe
padre: R03-N07
precio: 10
criatura: dragon
insignia: Guardián del borde
insignia_descripcion: Venciste al Orco del Desborde: nada de tu página se sale de la pantalla.
usa: css.frameworks, css.responsive, css.flexbox, css.grid
```

### Crónica

El Orco del Desborde se cansó de mirar desde la puerta y entró al taller. Agarró el **tablón de encargos** y lo estiró con sus manos enormes: en la ventanita de la cabaña, ahora todo se sale por el costado. La cabecera, la imagen, una dirección larguísima, las tarjetas, la tabla. Para leer hay que arrastrar la página de un lado al otro.

—Mirá la cabaña, {heroe}, no el castillo —dice {mentor}—. En la compu el orco no se nota. **En el celular, se ve todo.**

### Objetivos

- Encontrar qué elemento hace aparecer el scroll horizontal en el celular.
- Corregir anchos fijos, imágenes, textos sin cortes, filas que no bajan de línea y tablas anchas.
- Lograr que la página se vea bien en celular **y** en compu.

### Antes de empezar

- Todos los nodos de las Plantillas del Gremio, sobre todo «Flex y Grid con Tailwind» y «Responsive con Tailwind».

### Explicación

#### Cómo cazar al orco
1. Mirá la página en **Celular**: si aparece una barra de scroll horizontal abajo, hay orco.
2. En tu navegador, con el inspector en modo celular, buscá el elemento que se sale: suele ser el que tiene un **ancho fijo** (`w-[600px]`) o algo que **no se achica**.
3. Arreglá de a uno y volvé a mirar.

#### Los cinco escondites del orco
| Escondite | Arreglo |
|---|---|
| Un ancho fijo (`w-[600px]`) | `w-full max-w-[600px]`: como mucho 600, pero se achica |
| Una imagen con `max-w-none` | `w-full h-auto`: nunca más ancha que su contenedor |
| Un texto sin espacios (una dirección web) | `break-all`: se puede cortar en cualquier letra |
| Una fila de tarjetas con `shrink-0` | una grilla: una columna en el celular, varias desde `sm` |
| Una tabla ancha | un contenedor con `overflow-x-auto`: la tabla se desplaza sola, la página no |

### ¿Para qué sirve?

"En mi celular la página se mueve para el costado" es uno de los reclamos más comunes en cualquier sitio web. Arreglarlo rápido —encontrar el elemento culpable y saber cuál de los cinco arreglos usar— es una habilidad que se usa todas las semanas.

### Errores habituales

El orco se esconde en cinco lugares a la vez. Y hay que tener cuidado con la trampa más común: ponerle `overflow-x-hidden` al `body`. Eso **esconde** el desborde, pero no lo arregla: lo que se salía queda cortado y no se puede leer.

### Prueba del sello

#### ¿Por qué `overflow-x-hidden` en el `body` no es un buen arreglo?

Porque esconde el síntoma, no el problema: lo que se salía de la pantalla queda cortado y nadie lo puede ver ni leer. Hay que encontrar el elemento que desborda y arreglarlo.

#### ¿Qué diferencia hay entre `w-[600px]` y `w-full max-w-[600px]`?

`w-[600px]` mide siempre 600 px, aunque la pantalla tenga 390. `w-full max-w-[600px]` ocupa todo el ancho disponible, pero nunca más de 600: en la compu mide 600 y en el celular se achica.

### Misión R03-N08-M1 · El tablón estirado

```meta
entrega: codigo
entorno: navegador
monedas: 12
xp: 40
```

#### Consigna

El Orco estiró el tablón del taller. Arreglalo para que **en *Celular* no haya scroll horizontal** y en *Compu* se siga viendo bien:

1. La cabecera, como mucho de 600 px, y el menú que baje de línea si no entra.
2. La imagen, nunca más ancha que la pantalla.
3. La dirección larga, que se corte.
4. Las tres tarjetas: una abajo de la otra en el celular, en fila desde `sm`.
5. La tabla, con su propio scroll horizontal.

No vale `overflow-x-hidden` en el `body`. Mirá «Cómo debería verse».

#### Criterio de aprobación

- En *Celular* la página no tiene scroll horizontal y todo el texto se puede leer.
- No usa `overflow-hidden` en el `body` ni en `main` para esconder el desborde.
- La tabla tiene scroll propio dentro de un contenedor con `overflow-x-auto`.
- En *Compu* se ve como en «Cómo debería verse».

#### Cómo debe quedar

celular: capturas/R03-N08-M1-celular.webp
compu: capturas/R03-N08-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El tablón del taller</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-slate-950 p-4 text-slate-200">
    <header class="flex w-[600px] items-center justify-between rounded-xl bg-slate-900 p-4">
      <h1 class="text-xl font-bold text-cyan-400">Tablón del taller</h1>
      <nav class="flex gap-6 text-sm">
        <a href="#">Inicio</a><a href="#">Encargos</a><a href="#">Galería</a><a href="#">Contacto</a>
      </nav>
    </header>
    <main class="mt-4 space-y-4">
      <img src="/img/cursos/html/heroe-896.webp" alt="Aprendiz del taller con un vitral en las manos" class="w-[896px] max-w-none rounded-xl">
      <p>Seguí tu encargo en: https://talleres-de-los-vitrales.example/encargos/ventanal-del-gran-castillo-de-la-montana</p>
      <div class="flex gap-4">
        <article class="w-64 shrink-0 rounded-xl bg-slate-900 p-4">Vitral del Valle</article>
        <article class="w-64 shrink-0 rounded-xl bg-slate-900 p-4">Ventanas de la Ciudadela</article>
        <article class="w-64 shrink-0 rounded-xl bg-slate-900 p-4">Escaparate del Puerto</article>
      </div>
      <table class="w-[640px] text-left text-sm">
        <caption class="text-left font-bold">Entregas de la semana</caption>
        <thead><tr><th scope="col">Encargo</th><th scope="col">Región</th><th scope="col">Vidrios</th><th scope="col">Plomo</th><th scope="col">Entrega</th></tr></thead>
        <tbody><tr><td>Ventanal</td><td>Valle de la Serpiente</td><td>48</td><td>12 kg</td><td>Lunes</td></tr><tr><td>Rosetón</td><td>Imperio de las Clases</td><td>96</td><td>20 kg</td><td>Jueves</td></tr></tbody>
      </table>
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
    <title>El tablón del taller</title>
    <style type="text/tailwindcss">
      @import "tailwindcss";
    </style>
  </head>
  <body class="bg-slate-950 p-4 text-slate-200">
    <!-- Como mucho 600 px, pero en el celular se achica; si no entra, el menú baja -->
    <header class="flex w-full max-w-[600px] flex-wrap items-center justify-between gap-2 rounded-xl bg-slate-900 p-4">
      <h1 class="text-xl font-bold text-cyan-400">Tablón del taller</h1>
      <nav class="flex flex-wrap gap-x-6 gap-y-1 text-sm">
        <a href="#">Inicio</a><a href="#">Encargos</a><a href="#">Galería</a><a href="#">Contacto</a>
      </nav>
    </header>
    <main class="mt-4 space-y-4">
      <!-- La imagen nunca más ancha que su contenedor -->
      <img src="/img/cursos/html/heroe-896.webp" alt="Aprendiz del taller con un vitral en las manos" class="h-auto w-full max-w-[896px] rounded-xl">
      <!-- Un texto sin espacios (una dirección) se puede cortar en cualquier letra -->
      <p class="break-all">Seguí tu encargo en: https://talleres-de-los-vitrales.example/encargos/ventanal-del-gran-castillo-de-la-montana</p>
      <!-- Una columna en el celular, tres desde sm -->
      <div class="grid gap-4 sm:grid-cols-3">
        <article class="rounded-xl bg-slate-900 p-4">Vitral del Valle</article>
        <article class="rounded-xl bg-slate-900 p-4">Ventanas de la Ciudadela</article>
        <article class="rounded-xl bg-slate-900 p-4">Escaparate del Puerto</article>
      </div>
      <!-- La tabla mantiene su ancho, pero con scroll propio: la página no se mueve -->
      <div class="overflow-x-auto">
        <table class="min-w-[640px] text-left text-sm">
          <caption class="text-left font-bold">Entregas de la semana</caption>
          <thead><tr><th scope="col">Encargo</th><th scope="col">Región</th><th scope="col">Vidrios</th><th scope="col">Plomo</th><th scope="col">Entrega</th></tr></thead>
          <tbody><tr><td>Ventanal</td><td>Valle de la Serpiente</td><td>48</td><td>12 kg</td><td>Lunes</td></tr><tr><td>Rosetón</td><td>Imperio de las Clases</td><td>96</td><td>20 kg</td><td>Jueves</td></tr></tbody>
        </table>
      </div>
    </main>
  </body>
</html>
```
