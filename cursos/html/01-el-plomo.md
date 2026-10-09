# RAMA R01 · El Plomo: la estructura (HTML)

```meta
tipo: tronco
posicion: 1
```

## R01-N01 · Texto, enlaces e imágenes

```meta
tipo: tema
padre: R00-N01
precio: 10
criatura: skeleton
temas: html.texto, html.listas-tablas
usa: html.estructura
```

### Crónica

—Llevá un diario del taller, Iris —le pide {mentor}, y le da un cuaderno en blanco—: lo que aprendés, los pasos de cada trabajo, un dibujo de la mascota y los caminos hacia otros talleres.

Iris tarda una hora en elegir la letra del título. Arranca tres veces la primera hoja. {mentor} junta las hojas arrancadas en un canasto y les escribe un número con tiza: «Boceto 1, 2, 3».

Nora, la vitralista más vieja del taller, pasa la mano por el diario. Nora no ve: lee los vitrales tocando el plomo. —¿Y qué hay en el dibujo de la mascota? —pregunta. El dibujo no dice nada. Para Nora, no existe.

{mentor} señala los ventanales del fondo: uno da al Valle de la Serpiente, otro al Puerto de los Mensajeros. —Un vitral también **conecta**. Cada ventana da a otra. —Entre los bocetos viejos del canasto, Iris encuentra uno que no es suyo: **un vitral redondo**, firmado por alguien que se hacía llamar el Vidriero.

### Objetivos

Usar listas (con y sin orden, de definiciones), enlaces (externos, relativos e internos), imágenes accesibles y algunas etiquetas de texto más.

### Antes de empezar

- Esqueleto de una página, títulos y párrafos («Clase 0 · Hola, HTML»).

### Explicación

#### Listas
| Etiqueta | Qué es |
|---|---|
| `<ul>` + `<li>` | lista sin orden (viñetas): ingredientes, características |
| `<ol>` + `<li>` | lista **ordenada** (números): pasos, rankings |
| `<dl>` + `<dt>` + `<dd>` | lista de definiciones: término y explicación |

Adentro de `ul`/`ol` solo van `li`. Un menú de navegación también es una lista (lo vamos a ver en 03).

#### Enlaces: `<a href="...">`
| `href` | Lleva a |
|---|---|
| `https://sitio.com` | otro sitio (**absoluto**) |
| `../01-Hola-HTML/index.html` | otro archivo del proyecto (**relativo**: `..` = carpeta de arriba) |
| `#glosario` | el elemento con `id="glosario"` de esta página |
| `mailto:...` / `tel:...` | abrir el correo / llamar (muy útil en el celular) |

`target="_blank"` abre otra pestaña: agregá `rel="noopener"` (seguridad) y **avisalo en el texto** del enlace. El texto del enlace tiene que decir adónde lleva: "Ver la documentación", nunca "clic acá" (los lectores de pantalla listan los enlaces por su texto).

#### Imágenes: `<img>`
```html
<img src="../img/gheco-logo.webp" alt="Gheco, el gecko mascota del taller…" width="96" height="96">
```
- `src`: la ruta. `alt`: **qué muestra**, para quien no la ve (y si no carga). Si la imagen es solo decorativa: `alt=""`.
- `width`/`height`: el navegador reserva el lugar antes de cargarla (la página no "salta").
- Formatos: `.jpg` (fotos e ilustraciones), `.png` (con transparencia), `.svg` (dibujos vectoriales: nítidos en cualquier tamaño), **`.webp`** (como jpg/png pero mucho más liviano: las imágenes del curso pesan 150–180 KB en jpg y 6–60 KB en webp).

#### Imágenes que se adaptan: `srcset`, `sizes`, `figure`
```html
<figure>
  <img src="../img/heroe-448.webp"
       srcset="../img/heroe-448.webp 448w, ../img/heroe-896.webp 896w"
       sizes="240px"
       alt="…" width="240" height="321" loading="lazy">
  <figcaption>Epígrafe</figcaption>
</figure>
```
- `srcset`: la lista de archivos con su ancho real (`448w`). `sizes`: qué ancho va a ocupar en pantalla (acá, 240 px). Con eso, **el navegador elige** el archivo: una pantalla común baja el chico; una de alta densidad (la mayoría de los celulares), el grande para que se vea nítido. Mobile first también es no hacer bajar de más.
- `width`/`height` también fijan el tamaño mientras no haya CSS: con `width="448"`, en un celular de 390 px la imagen **se sale de la pantalla** (en «Responsive: celular primero» aprendemos `max-width: 100%`).
- `loading="lazy"`: la imagen se descarga recién cuando se acerca a la vista.
- `figure` + `figcaption`: imagen con epígrafe.

#### Más texto
`<code>` (código), `<small>` (letra chica, notas), `<hr>` (separador temático), `<time datetime="2026-10-01">` (una fecha que las máquinas entienden), `<br>` (salto de línea dentro de un párrafo; no lo uses para separar bloques).

#### El ejemplo

Diario con imagen, listas, los tres tipos de enlace, glosario y pie.

#### Cómo se ve el ejemplo

El título, el logo de Gheco (el gecko celeste con anteojos), la ilustración del aprendiz con su epígrafe, una lista con viñetas, una numerada del 1 al 3, enlaces azules subrayados (morados si ya se visitaron), el glosario con las definiciones sangradas y una línea separadora. "Ir al glosario" baja hasta esa sección.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Diario del Taller</title>
  </head>
  <body>
    <h1>Diario del Taller</h1>

    <!-- Imagen: src = ruta al archivo, alt = descripcion para quien no la ve -->
    <img src="/img/cursos/html/gheco-logo.webp" alt="Gheco, el gecko mascota del taller, con anteojos de realidad aumentada" width="96" height="96">

    <!-- figure + figcaption: una imagen con su epigrafe.
         srcset: el navegador elige el archivo segun el ancho de la pantalla -->
    <figure>
      <img src="/img/cursos/html/heroe-448.webp"
           srcset="/img/cursos/html/heroe-448.webp 448w, /img/cursos/html/heroe-896.webp 896w"
           sizes="240px"
           alt="Ilustración de un joven con buzo negro de circuitos neón, sobre una grilla futurista"
           width="240" height="321" loading="lazy">
      <figcaption>El aprendiz del taller, con el buzo de GhecoSoft.</figcaption>
    </figure>

    <h2>Lo que aprendí hoy</h2>
    <!-- Lista sin orden (vinetas) -->
    <ul>
      <li>Las etiquetas se abren y se cierran.</li>
      <li>El <code>head</code> no se ve.</li>
      <li>Un solo <code>h1</code> por página.</li>
    </ul>

    <h2>Pasos para templar el vidrio</h2>
    <!-- Lista ordenada (numeros) -->
    <ol>
      <li>Calentar el horno.</li>
      <li>Meter el vidrio.</li>
      <li>Esperar <strong>sin abrir</strong>.</li>
    </ol>

    <h2>Enlaces</h2>
    <p>
      <!-- Enlace a otro sitio: se abre en otra pestana y se avisa -->
      Documentación oficial en
      <a href="https://developer.mozilla.org/es/docs/Web/HTML" target="_blank" rel="noopener">MDN (se abre en otra pestaña)</a>.
    </p>
    <p>
      <!-- Enlace relativo: a otro archivo del proyecto -->
      Volver a la <a href="../01-Hola-HTML/index.html">práctica 01</a>.
    </p>
    <p>
      <!-- Enlace interno: a un id de esta misma pagina -->
      Ir al <a href="#glosario">glosario</a>.
    </p>

    <h2 id="glosario">Glosario</h2>
    <dl>
      <dt>Plomo</dt>
      <dd>La estructura del vitral (el HTML).</dd>
      <dt>Vidrio</dt>
      <dd>El color y la forma (el CSS).</dd>
    </dl>

    <hr>
    <p><small>Escrito por Iris · <time datetime="2026-10-01">1 de octubre de 2026</time></small></p>
  </body>
</html>
```

### ¿Para qué sirve?

Los enlaces son la "web" de la web: lo que une una página con otra. Las listas están en todos lados (menús, ingredientes, pasos de un trámite) y las imágenes bien hechas cargan rápido en el celular y se pueden "leer" con un lector de pantalla. Un texto alternativo bien escrito también ayuda a que la página aparezca en los buscadores.

### Errores habituales

**Esqueleto: imagen que no aparece** (ruta mal escrita): se ve el texto del `alt` o un ícono roto. En DevTools → pestaña *Red* aparece en rojo con `404`. Las rutas distinguen mayúsculas: `Gheco-logo.webp` ≠ `gheco-logo.webp`.

**Slime: imagen sin `alt`**:
```
6:2  error  <img> is missing required "alt" attribute  wcag/h37
```
**Slime: algo que no es `li` dentro de una lista**:
```
11:6  error  <p> element is not permitted as content under <ul>  element-permitted-content
```
**Ogro: `id` repetido**: el enlace `#glosario` va al primero. El validador avisa `Duplicate ID`.

### Prueba del sello

#### ¿Qué diferencia hay entre una ruta absoluta y una relativa? ¿Qué significa `..`?

Una ruta **absoluta** es la dirección completa (`https://sitio.com/img/foto.webp`) y funciona desde cualquier lado. Una **relativa** se cuenta desde donde está la página: `img/foto.webp` busca la carpeta `img` al lado de la página. `..` significa "subí una carpeta": `../img/foto.webp` sale de la carpeta actual y entra a `img`.

#### ¿Qué tiene que decir el `alt`? ¿Cuándo va vacío?

Tiene que decir **lo que la imagen aporta**, como si se la contaras a alguien por teléfono: "Gheco señalando el mapa", no "imagen". Va vacío (`alt=""`) cuando la imagen es solo decorativa: así el lector de pantalla la saltea en lugar de leer el nombre del archivo.

#### ¿Por qué "clic acá" es un mal texto para un enlace?

Porque fuera de contexto no dice nada. Quien usa lector de pantalla suele pedir la lista de enlaces de la página, y diez "clic acá" son inútiles. El texto del enlace tiene que decir **adónde lleva**: "Ver el horario de las clases".

### Misión R01-N01-M1 · La receta de la poción

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Escribí la receta de una poción del taller:

1. Un título y una imagen de la poción (podés usar `/img/cursos/html/gheco-logo.webp`) con su `alt`.
2. La lista de ingredientes con `ul`.
3. Los pasos, en orden, con `ol`.

#### Criterio de aprobación

- La imagen tiene un `alt` que describe lo que muestra.
- Los ingredientes están en una lista `ul` y los pasos en una `ol`.
- Cada elemento de lista es un `li` dentro de su lista.
- El HTML está completo y bien cerrado.

#### Cómo debe quedar

celular: capturas/R01-N01-M1-celular.webp
compu: capturas/R01-N01-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La receta de la poción</title>
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
    <title>Poción de vida</title>
  </head>
  <body>
    <h1>Poción de vida</h1>
    <img src="/img/cursos/html/gheco-logo.webp" alt="Gheco, el gecko que prepara la poción" width="64" height="64">
    <h2>Ingredientes</h2>
    <ul>
      <li>2 hojas de menta</li>
      <li>1 gota de rocío</li>
      <li>Agua del manantial</li>
    </ul>
    <h2>Preparación</h2>
    <ol>
      <li>Hervir el agua.</li>
      <li>Agregar la menta.</li>
      <li>Al final, la gota de rocío.</li>
    </ol>
  </body>
</html>
```


### Misión R01-N01-M2 · El índice con saltos

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá una página del bestiario con un índice que salte a cada criatura:

1. Arriba, una lista de enlaces internos (`href="#slime"`, `href="#goblin"`…).
2. Una sección para cada criatura, con su `id` y un párrafo.
3. Al final de cada sección, un enlace "Volver arriba".

#### Criterio de aprobación

- Cada enlace del índice lleva a una sección que existe (el `href="#x"` coincide con un `id="x"`).
- Hay al menos tres criaturas con su sección.
- Funciona el "Volver arriba".
- Los textos de los enlaces dicen adónde llevan.

#### Cómo debe quedar

celular: capturas/R01-N01-M2-celular.webp
compu: capturas/R01-N01-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El índice con saltos</title>
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
    <title>Índice con saltos</title>
  </head>
  <body>
    <h1>Bestiario</h1>
    <ul>
      <li><a href="#slime">Slime</a></li>
      <li><a href="#goblin">Goblin</a></li>
    </ul>
    <h2 id="slime">Slime</h2>
    <p>Nace de etiquetas mal cerradas.</p>
    <h2 id="goblin">Goblin</h2>
    <p>Nace de valores de CSS inválidos.</p>
    <p><a href="#">Volver arriba</a></p>
  </body>
</html>
```


### Encargo R01-N01-E1 · La página de contacto

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Un comercio del barrio quiere su página de contacto: un teléfono que se pueda tocar para llamar (`tel:`), un correo que abra el programa de correo (`mailto:`) y un enlace al mapa que se abra en otra pestaña.

#### Criterio de aprobación

- El teléfono usa `href="tel:…"` y el correo `href="mailto:…"`.
- El enlace al mapa abre en otra pestaña (`target="_blank"` con `rel="noopener"`).
- Los textos de los enlaces dicen qué hacen.

#### Cómo debe quedar

celular: capturas/R01-N01-E1-celular.webp
compu: capturas/R01-N01-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La página de contacto</title>
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
    <title>Contacto del taller</title>
  </head>
  <body>
    <h1>Taller de Tesela</h1>
    <ul>
      <li>Teléfono: <a href="tel:+543804123456">380 412-3456</a></li>
      <li>Correo: <a href="mailto:taller@ejemplo.com">taller@ejemplo.com</a></li>
      <li>Mapa: <a href="https://www.openstreetmap.org" target="_blank" rel="noopener">ver en OpenStreetMap (otra pestaña)</a></li>
    </ul>
    <p><small>Abierto de lunes a viernes.</small></p>
  </body>
</html>
```

## R01-N02 · HTML semántico

```meta
tipo: tema
padre: R01-N01
precio: 10
criatura: skeleton
temas: html.semantica
usa: html.texto
```

### Crónica

El Gremio le encargó a {mentor} un ventanal enorme, y el boceto tiene zonas: la cornisa, el panel central, los paneles de los costados, el zócalo.

Iris ya eligió los colores de las cuatro. {mentor} le saca el lápiz de la mano. —Antes de pensar en colores, **nombrá cada zona**.

Nora recorre el boceto con los dedos, de arriba abajo. —No encuentro el menú —dice—. Ni el contenido. Para mí son cajas, todas iguales. —Iris escribe el nombre de cada zona sobre el plomo, y Nora las encuentra al instante, una por una, con una sonrisa. —Ahora sí. El que no ve el vitral se guía por esos nombres.

### Objetivos

Organizar una página con etiquetas **semánticas** (`header`, `nav`, `main`, `section`, `article`, `aside`, `footer`) y dejar armado el **esqueleto** de la plataforma que vamos a diseñar en todo el curso.

### Antes de empezar

- Títulos, listas, enlaces e imágenes (de «Clase 0 · Hola, HTML» a «Texto, enlaces e imágenes»).

### Explicación

#### ¿Por qué no todo con `<div>`?
`<div>` es una caja **sin significado**. Las etiquetas semánticas dicen **qué rol** cumple cada parte. Lo aprovechan:
- los **lectores de pantalla**: permiten saltar directo a "navegación" o "contenido principal" (se llaman *landmarks*, puntos de referencia);
- los **buscadores** (Google entiende mejor la página);
- **vos**: el código se lee solo.

| Etiqueta | Rol | En la plataforma |
|---|---|---|
| `<header>` | cabecera (del sitio o de una sección) | logo + menú |
| `<nav>` | navegación principal | Cursos, Top 10, Bóveda |
| `<main>` | contenido principal (**uno** por página) | todo lo del medio |
| `<section>` | parte temática **con título** | Hero, Rutas, Hall of Fame |
| `<article>` | algo que se entiende solo | cada tarjeta de curso |
| `<aside>` | contenido secundario o relacionado | la Bóveda de tokens |
| `<footer>` | pie | derechos, estado del sistema |

Regla práctica: si tiene un título y es una parte de la página → `section`; si lo podrías publicar suelto → `article`; si es solo para agrupar y dar estilo → `div`.

#### Nombres accesibles
- `aria-label="Principal"` le da nombre a un `nav` (útil si hay más de uno: el de arriba y el de abajo en el celular).
- `aria-labelledby="titulo-rutas"` dice "esta sección se llama como el título con ese `id`".
- **Enlace de salto**: `<a href="#contenido">Saltar al contenido</a>` al principio deja ir directo al `main` sin recorrer todo el menú (en 22 lo escondemos hasta que recibe el foco).

#### El ejemplo

El esqueleto de **GhecoSoft-Code**, esta misma plataforma, sin nada de diseño: cabecera, navegación, hero, rutas (dos tarjetas), Hall of Fame, bóveda y pie. Lo vamos a ir vistiendo hasta el nodo «Jefe final: el Dragón de los Talleres».

#### Cómo se ve el ejemplo

Todo en una columna, letra con serifa, enlaces azules: así se ve la estructura pura. Con DevTools → pestaña *Accesibilidad* (o una extensión de *landmarks*) se ven las zonas: banner, navigation, main, region, complementary, contentinfo.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GhecoSoft-Code · Esqueleto</title>
  </head>
  <body>
    <!-- Enlace para saltear el menu con el teclado o un lector de pantalla -->
    <a href="#contenido">Saltar al contenido</a>

    <!-- header: la cabecera del sitio (logo + navegacion) -->
    <header>
      <a href="#">
        <img src="/img/cursos/html/gheco-logo.webp" alt="" width="40" height="40">
        GhecoSoft-Code
      </a>
      <!-- nav: el bloque de navegacion principal. aria-label lo nombra -->
      <nav aria-label="Principal">
        <ul>
          <li><a href="#rutas">Cursos</a></li>
          <li><a href="#fama">Top 10</a></li>
          <li><a href="#tokens">Bóveda de tokens</a></li>
        </ul>
      </nav>
    </header>

    <!-- main: el contenido principal, UNO por pagina -->
    <main id="contenido">
      <!-- section: una parte tematica, con su titulo -->
      <section aria-labelledby="titulo-hero">
        <p>Plataforma de cursos · Temporada 04</p>
        <h1 id="titulo-hero">Aprendé a programar avanzando por tu árbol de habilidades.</h1>
        <p>Compilá algoritmos reales, desbloqueá nodos tecnológicos y competí por el rango Supremo.</p>
        <a href="#rutas">Explorar cursos</a>
      </section>

      <section id="rutas" aria-labelledby="titulo-rutas">
        <h2 id="titulo-rutas">Rutas de entrenamiento</h2>
        <!-- article: algo que tiene sentido por si solo (una tarjeta, una noticia) -->
        <article>
          <h3>C++ Moderno y Videojuegos</h3>
          <p>Gestión de memoria, RAII y punteros inteligentes.</p>
          <p>Progreso: 18 de 24 nodos</p>
        </article>
        <article>
          <h3>Motores gráficos con SDL3</h3>
          <p>Ventanas, eventos y game loops.</p>
          <p>Progreso: 10 de 22 nodos</p>
        </article>
      </section>

      <section id="fama" aria-labelledby="titulo-fama">
        <h2 id="titulo-fama">Hall of Fame</h2>
        <ol>
          <li>@NeoCoder_X — 14.850 XP</li>
          <li>@DevValkyrie — 13.200 XP</li>
          <li>@GlitchHunter — 12.450 XP</li>
        </ol>
      </section>

      <!-- aside: contenido relacionado pero secundario -->
      <aside id="tokens" aria-labelledby="titulo-tokens">
        <h2 id="titulo-tokens">Bóveda de tokens</h2>
        <p>Cada módulo completado acuña una moneda en tu inventario.</p>
      </aside>
    </main>

    <!-- footer: el pie del sitio -->
    <footer>
      <p>© 2026 GhecoSoft-Code. Formación en bajo nivel, motores de videojuegos y compilación real.</p>
    </footer>
  </body>
</html>
```

### ¿Para qué sirve?

Los lectores de pantalla, que usan las personas ciegas, saltan de zona en zona usando estas etiquetas: "ir al menú", "ir al contenido". Los buscadores también las leen para entender qué es lo importante de tu página. Y en un equipo, el que abre tu archivo entiende enseguida dónde está cada cosa.

### Errores habituales

**Ogro: "divitis"** — todo con `div`: funciona, pero el lector de pantalla no encuentra nada.

**Ogro: dos `main`**: solo puede haber uno visible.

**Ogro: `section` sin título**: si no tiene título, probablemente es un `div`.

**Esqueleto: `aria-labelledby` que apunta a un `id` que no existe**: el validador avisa y la sección queda sin nombre.

### Prueba del sello

#### ¿Qué gana una persona ciega con `nav` y `main` en lugar de `div`?

Puede **saltar directo** al menú o al contenido principal con un atajo, en lugar de escuchar la página entera desde el principio. Para su lector de pantalla un `div` no dice nada; un `nav` dice "esto es navegación".

#### ¿Cuándo `section`, cuándo `article` y cuándo `div`?

`article` es algo que tiene sentido **solo**, aunque lo saques de la página (una entrada de blog, una tarjeta de producto). `section` es una **parte temática** de la página, con su título. `div` es una caja **sin significado**, solo para agrupar y darle estilo.

#### ¿Para qué sirve el enlace "Saltar al contenido"?

Para que quien navega con el teclado o con un lector de pantalla no tenga que recorrer todo el menú en cada página: con un solo `Tab` + `Enter` llega directo al `main`.

### Misión R01-N02-M1 · El blog del taller

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá el blog de los Talleres con etiquetas semánticas:

1. Un `header` con el nombre del blog y un `nav` con tres enlaces.
2. Un `main` con dos `article`, cada uno con su título y su fecha en un `time` (con el atributo `datetime`).
3. Un `aside` "Sobre la autora".
4. Un `footer` al final.

#### Criterio de aprobación

- Usa `header`, `nav`, `main`, `article`, `aside` y `footer`, cada uno en su lugar.
- Cada `article` tiene su título y un `time` con `datetime` válido (`2026-10-02`).
- No hay `div` donde corresponde una etiqueta semántica.

#### Cómo debe quedar

celular: capturas/R01-N02-M1-celular.webp
compu: capturas/R01-N02-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El blog del taller</title>
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
    <title>Blog del Taller</title>
  </head>
  <body>
    <header>
      <p>Blog del Taller</p>
      <nav aria-label="Principal">
        <ul>
          <li><a href="#">Inicio</a></li>
          <li><a href="#">Archivo</a></li>
        </ul>
      </nav>
    </header>
    <main>
      <h1>Últimas entradas</h1>
      <article>
        <h2>Cómo cortar vidrio sin romperlo</h2>
        <p><time datetime="2026-09-30">30 de septiembre</time></p>
        <p>Primero se marca, después se golpea suave.</p>
      </article>
      <article>
        <h2>El plomo perfecto</h2>
        <p><time datetime="2026-09-28">28 de septiembre</time></p>
        <p>Ni muy grueso ni muy fino.</p>
      </article>
    </main>
    <aside aria-labelledby="titulo-autora">
      <h2 id="titulo-autora">Sobre la autora</h2>
      <p>Tesela, vitralista desde hace 300 años.</p>
    </aside>
    <footer>
      <p>© 2026 Blog del Taller</p>
    </footer>
  </body>
</html>
```


### Misión R01-N02-M2 · El perfil del jugador

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá el perfil de un jugador como un `article` independiente:

1. Su propio `header` con el avatar (con `alt`), el nombre y el nivel.
2. Una `section` de logros, con su título y una lista.
3. Un `footer` con la fecha en que se unió.

#### Criterio de aprobación

- El perfil es un `article` con `header`, `section` y `footer` propios.
- La `section` de logros tiene un título.
- El avatar tiene `alt`.

#### Cómo debe quedar

celular: capturas/R01-N02-M2-celular.webp
compu: capturas/R01-N02-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El perfil del jugador</title>
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
    <title>Perfil de jugador</title>
  </head>
  <body>
    <main>
      <article aria-labelledby="nombre">
        <header>
          <img src="/img/cursos/html/heroe-avatar.webp" alt="Avatar de Iris" width="96" height="96">
          <h1 id="nombre">@Iris</h1>
          <p>Nivel 14 · Espadachina</p>
        </header>
        <section aria-labelledby="titulo-logros">
          <h2 id="titulo-logros">Logros</h2>
          <ul>
            <li>Rey Slime vencido</li>
            <li>10 gemas en una partida</li>
          </ul>
        </section>
        <footer>
          <p>Miembro desde 2026</p>
        </footer>
      </article>
    </main>
  </body>
</html>
```


### Encargo R01-N02-E1 · La página del restaurante

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Un restaurante quiere su página: un enlace "Saltar al contenido" al principio, un menú de navegación, las secciones "Menú" y "Reservas" y un pie con la dirección.

#### Criterio de aprobación

- El primer enlace de la página salta al `main` (`href="#contenido"` con su `id`).
- Hay `nav`, `main` con dos `section` con título, y `footer` con la dirección (idealmente en un `address`).

#### Cómo debe quedar

celular: capturas/R01-N02-E1-celular.webp
compu: capturas/R01-N02-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La página del restaurante</title>
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
    <title>Restaurante El Puerto</title>
  </head>
  <body>
    <a href="#contenido">Saltar al contenido</a>
    <header>
      <p>Restaurante El Puerto</p>
      <nav aria-label="Principal">
        <ul>
          <li><a href="#menu">Menú</a></li>
          <li><a href="#reservas">Reservas</a></li>
        </ul>
      </nav>
    </header>
    <main id="contenido">
      <h1>Cocina de mar desde 1990</h1>
      <section id="menu" aria-labelledby="titulo-menu">
        <h2 id="titulo-menu">Menú</h2>
        <ul>
          <li>Rabas — $9000</li>
          <li>Merluza a la romana — $12000</li>
        </ul>
      </section>
      <section id="reservas" aria-labelledby="titulo-reservas">
        <h2 id="titulo-reservas">Reservas</h2>
        <p>Llamá al <a href="tel:+543804000000">380 400-0000</a>.</p>
      </section>
    </main>
    <footer>
      <p>Av. Costanera 123</p>
    </footer>
  </body>
</html>
```

## R01-N03 · Formularios

```meta
tipo: tema
padre: R01-N02
precio: 10
criatura: goblin
temas: html.formularios
usa: html.semantica
```

### Crónica

A la entrada del portal hay una terminal que pide nombre y contraseña. Teo la deja vacía y aprieta «Entrar», tres veces, cada vez más fuerte. La terminal le contesta sola que falta completar un campo.

—¡Está rota! —No está rota —se ríe {mentor}—. El navegador ya sabe validar. Solo hay que pedírselo bien.

Y cuando el formulario está completo, le explica a Iris, el mensaje viaja al Puerto de los Mensajeros: ahí Elefa lo recibe y lo contesta. —Nosotros armamos la ventanilla; ellos, la respuesta.

### Objetivos

Armar formularios accesibles (cada campo con su `label`), elegir el tipo de campo correcto y usar la validación que trae el navegador.

### Antes de empezar

- Estructura semántica («HTML semántico»).

### Explicación

#### La estructura
```html
<form action="/login" method="post">
  <label for="usuario">Usuario</label>
  <input id="usuario" name="usuario" type="text" required>
  <button type="submit">Entrar</button>
</form>
```
- `action`: adónde se envían los datos (un servidor: PHP/Laravel, Spring…). Acá `#` porque todavía no hay servidor.
- `method`: `get` (los datos van en la URL: búsquedas) o `post` (van ocultos: login, registro).
- `name`: el nombre con el que llega cada dato al servidor. Sin `name`, el campo **no se envía**.
- **`label` siempre.** `for` = el `id` del campo. Tocar el texto enfoca el campo (zona táctil más grande en el celular) y el lector de pantalla dice qué hay que escribir. El `placeholder` es solo un ejemplo: **no reemplaza** al label (desaparece al escribir).

#### Tipos de campo
| `type` | Para | En el celular |
|---|---|---|
| `text`, `password` | texto, contraseña oculta | teclado común |
| `email` | correo (valida el formato) | teclado con `@` |
| `number` (+ `min`/`max`) | números | teclado numérico |
| `tel` | teléfono | teclado de teléfono |
| `search` | búsqueda | botón "buscar" |
| `date`, `time` | fecha, hora | selector nativo |
| `checkbox` | sí/no, varias opciones | |
| `radio` (mismo `name`) | **una** opción entre varias | |

Más: `<select>` + `<option>` (lista desplegable), `<textarea>` (texto largo), `<fieldset>` + `<legend>` (agrupar campos con un título; obligatorio para grupos de `radio`).

#### Validación del navegador
`required`, `minlength`/`maxlength`, `min`/`max`, `pattern="[A-Za-z0-9_]+"` (un patrón de caracteres permitidos). Si algo no cumple, el navegador **no envía** el formulario y muestra un mensaje en el campo. Es una ayuda: el servidor **siempre** tiene que volver a validar.

`autocomplete="username"`, `"current-password"`, `"email"`, `"tel"` permiten que el celular complete los datos guardados.

#### Botones
`<button type="submit">` envía, `type="reset"` borra, `type="button"` no hace nada (se usa con JavaScript). Poné siempre el `type`.

#### El ejemplo

El login de la plataforma (como en esta plataforma) y un formulario de registro con casi todos los tipos de campo.

#### Cómo se ve el ejemplo

Campos con su texto arriba, casillas y botones del sistema (sin diseño todavía). Tocar "Entrar a la terminal" vacío muestra un globo del navegador sobre el usuario pidiendo completarlo (el texto exacto depende del idioma del navegador, por ejemplo "Completa este campo"). Un alias con espacios avisa que no coincide con el formato.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Formularios del portal</title>
  </head>
  <body>
    <main>
      <h1>Portal del desarrollador</h1>

      <!-- 1) Login: action = adonde se envia, method = como -->
      <section aria-labelledby="titulo-login">
        <h2 id="titulo-login">Entrá a tu cuenta</h2>
        <form action="#" method="post">
          <!-- label + for = id: tocar el texto enfoca el campo, y el lector lo anuncia -->
          <p>
            <label for="usuario">Usuario o email</label><br>
            <input id="usuario" name="usuario" type="text" autocomplete="username" required>
          </p>
          <p>
            <label for="clave">Contraseña</label><br>
            <input id="clave" name="clave" type="password" autocomplete="current-password" required minlength="8">
          </p>
          <p>
            <!-- checkbox: label que ENVUELVE al input (otra forma valida) -->
            <label><input type="checkbox" name="recordarme" checked> Recordarme en esta terminal</label>
          </p>
          <button type="submit">Entrar a la terminal</button>
          <p><a href="#registro">¿No tenés cuenta? Registrate gratis</a></p>
        </form>
      </section>

      <!-- 2) Registro: mas tipos de campo y validaciones del navegador -->
      <section id="registro" aria-labelledby="titulo-registro">
        <h2 id="titulo-registro">Crear cuenta</h2>
        <form action="#" method="post">
          <fieldset>
            <legend>Datos personales</legend>
            <p>
              <label for="alias">Alias (3 a 15 letras o números)</label><br>
              <input id="alias" name="alias" type="text" required minlength="3" maxlength="15" pattern="[A-Za-z0-9_]+" placeholder="NeoCoder_X">
            </p>
            <p>
              <label for="email">Email</label><br>
              <input id="email" name="email" type="email" autocomplete="email" required>
            </p>
            <p>
              <label for="edad">Edad</label><br>
              <input id="edad" name="edad" type="number" min="10" max="99">
            </p>
          </fieldset>

          <fieldset>
            <legend>Ruta inicial</legend>
            <!-- radio: mismo name = solo se puede elegir uno -->
            <label><input type="radio" name="ruta" value="cpp" checked> C++</label>
            <label><input type="radio" name="ruta" value="web"> Web</label>
            <label><input type="radio" name="ruta" value="python"> Python</label>
          </fieldset>

          <p>
            <label for="nivel">Nivel</label><br>
            <select id="nivel" name="nivel">
              <option value="inicial">Inicial</option>
              <option value="intermedio" selected>Intermedio</option>
              <option value="avanzado">Avanzado</option>
            </select>
          </p>
          <p>
            <label for="objetivo">¿Qué querés aprender?</label><br>
            <textarea id="objetivo" name="objetivo" rows="3" cols="30"></textarea>
          </p>
          <button type="submit">Crear cuenta</button>
          <button type="reset">Borrar todo</button>
        </form>
      </section>
    </main>
  </body>
</html>
```

### ¿Para qué sirve?

Todo lo que se completa en internet es un formulario: el login, el buscador, la compra con tarjeta, la encuesta, el turno del médico. Un formulario bien hecho se usa rápido con el teclado, muestra el teclado numérico en el celular cuando hace falta y avisa los errores antes de enviar. En el curso de PHP vas a ver el otro lado: cómo el servidor recibe esos datos.

### Errores habituales

**Esqueleto: `label` que apunta a un `id` que no existe**: tocar el texto no hace nada y el lector de pantalla anuncia "campo de texto" sin nombre.

**Ogro: falta `name`**: el campo se ve, pero el dato no llega al servidor.

**Slime: botón sin `type`**:
```
9:2  error  <button> is missing recommended "type" attribute  no-implicit-button-type
```
**Ogro: varios checkbox con el mismo nombre**:
```
21:47  error  Duplicate form control name "temas"  form-dup-name
```
Para enviar **varios** valores se usa `name="temas[]"` (así lo entienden PHP y Laravel).

### Prueba del sello

#### ¿Por qué el `placeholder` no reemplaza al `label`?

Porque el `placeholder` **desaparece** apenas empezás a escribir, y entonces ya no sabés qué iba en ese campo. Además, muchos lectores de pantalla no lo leen y su gris suele tener poco contraste. El `label` queda siempre a la vista y, si lo tocás, pone el cursor en su campo.

#### ¿Qué diferencia hay entre `get` y `post`?

Con `get` los datos viajan **en la dirección** (`buscar?q=slime`): sirve para búsquedas, que se pueden guardar o compartir. Con `post` viajan **dentro del pedido**, sin verse en la barra: es para lo que cambia algo o es privado (un login, un formulario de compra).

#### Si el navegador ya valida, ¿por qué hay que validar también en el servidor?

Porque la validación del navegador **se puede saltear**: cualquiera puede borrar el `required` con el inspector o mandar datos sin usar tu página. Lo del navegador es una ayuda para quien completa; la seguridad está en el servidor.

### Misión R01-N03-M1 · El buscador

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá el buscador del bestiario: un formulario con `method="get"`, un campo de tipo `search` con su `label` y un botón "Buscar".

#### Criterio de aprobación

- El formulario usa `method="get"`.
- El campo es `type="search"`, tiene `name` y un `label` conectado (`for` igual al `id`).
- Hay un botón de envío con un texto claro.

#### Cómo debe quedar

celular: capturas/R01-N03-M1-celular.webp
compu: capturas/R01-N03-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El buscador</title>
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
    <title>Buscar cursos</title>
  </head>
  <body>
    <main>
      <h1>Buscar cursos</h1>
      <form action="#" method="get" role="search">
        <label for="q">Buscar</label>
        <input id="q" name="q" type="search" placeholder="Ej.: OpenGL">
        <button type="submit">Buscar</button>
      </form>
    </main>
  </body>
</html>
```


### Misión R01-N03-M2 · La encuesta del gremio

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá una encuesta para los aprendices:

1. Un grupo de opciones `radio` obligatorio (¿qué taller te gustó más?), dentro de un `fieldset` con su `legend`.
2. Un grupo de `checkbox` (¿qué herramientas usaste?).
3. Un `textarea` de comentarios de **300 caracteres como máximo**.

#### Criterio de aprobación

- Los `radio` comparten el mismo `name`, están en un `fieldset` con `legend` y uno lleva `required`.
- Cada opción tiene su `label`.
- El `textarea` tiene `maxlength="300"` y su `label`.

#### Cómo debe quedar

celular: capturas/R01-N03-M2-celular.webp
compu: capturas/R01-N03-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La encuesta del gremio</title>
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
    <title>Encuesta de la temporada</title>
  </head>
  <body>
    <main>
      <h1>Encuesta de la temporada</h1>
      <form action="#" method="post">
        <fieldset>
          <legend>¿Qué te pareció el curso?</legend>
          <label><input type="radio" name="opinion" value="5" required> Excelente</label>
          <label><input type="radio" name="opinion" value="3"> Bien</label>
          <label><input type="radio" name="opinion" value="1"> Mejorable</label>
        </fieldset>
        <fieldset>
          <legend>¿Qué temas querés? (podés elegir varios)</legend>
          <label><input type="checkbox" name="temas[]" value="vulkan"> Vulkan</label>
          <label><input type="checkbox" name="temas[]" value="rust"> Rust</label>
          <label><input type="checkbox" name="temas[]" value="godot"> Godot</label>
        </fieldset>
        <p>
          <label for="comentario">Comentario</label><br>
          <textarea id="comentario" name="comentario" rows="4" maxlength="300"></textarea>
        </p>
        <button type="submit">Enviar</button>
      </form>
    </main>
  </body>
</html>
```


### Encargo R01-N03-E1 · Los turnos de la veterinaria

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Una veterinaria quiere un formulario para pedir turno: nombre, teléfono, fecha (desde hoy en adelante), hora (de 9 a 18, cada media hora) y la especie en un `select` obligatorio.

#### Criterio de aprobación

- Usa los tipos de campo correctos (`tel`, `date`, `time`).
- La hora tiene `min="09:00"`, `max="18:00"` y `step="1800"`.
- El `select` es `required` y su primera opción vacía pide elegir.
- Todos los campos tienen su `label`.

#### Cómo debe quedar

celular: capturas/R01-N03-E1-celular.webp
compu: capturas/R01-N03-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Los turnos de la veterinaria</title>
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
    <title>Pedir turno</title>
  </head>
  <body>
    <main>
      <h1>Pedir turno en la veterinaria</h1>
      <form action="#" method="post">
        <p>
          <label for="duenio">Nombre y apellido</label><br>
          <input id="duenio" name="duenio" type="text" autocomplete="name" required>
        </p>
        <p>
          <label for="telefono">Teléfono</label><br>
          <input id="telefono" name="telefono" type="tel" autocomplete="tel" required>
        </p>
        <p>
          <label for="fecha">Fecha</label><br>
          <input id="fecha" name="fecha" type="date" required min="2026-10-01">
        </p>
        <p>
          <label for="hora">Hora</label><br>
          <input id="hora" name="hora" type="time" min="09:00" max="18:00" step="1800" required>
        </p>
        <p>
          <label for="especie">Especie</label><br>
          <select id="especie" name="especie" required>
            <option value="">Elegí una opción</option>
            <option>Perro</option>
            <option>Gato</option>
            <option>Otro</option>
          </select>
        </p>
        <button type="submit">Reservar</button>
      </form>
    </main>
  </body>
</html>
```

## R01-N04 · Tablas

```meta
tipo: tema
padre: R01-N03
precio: 10
criatura: orc
temas: html.listas-tablas
usa: html.semantica
```

### Crónica

En la entrada de los Talleres cuelga la tabla de la **Liga Obsidiana**: puesto, aprendiz, especialidad, racha y puntos. Pero anoche el Slime de las Etiquetas Huérfanas desarmó las filas, y ahora nadie sabe de quién es cada número. Teo jura que él estaba primero.

—Volvé a armarla, Iris —le pide {mentor}—, **para que se entienda leyéndola en voz alta**.

Nora se ofrece a probarla. Pasa la mano fila por fila y lee: «Puesto 3, Teo, especialidad… colores, racha: dos días». Teo no estaba primero.

### Objetivos

Mostrar datos en filas y columnas con `table`, con encabezados accesibles, partes (`thead`, `tbody`, `tfoot`) y celdas combinadas.

### Antes de empezar

- Estructura semántica («HTML semántico»).

### Explicación

| Etiqueta | Qué es |
|---|---|
| `<table>` | la tabla |
| `<caption>` | su título (va primero) |
| `<thead>` / `<tbody>` / `<tfoot>` | encabezado, cuerpo, pie |
| `<tr>` | una fila (*table row*) |
| `<th>` | celda de **encabezado** |
| `<td>` | celda de **dato** |

- `scope="col"`: el `th` es el título de su **columna**. `scope="row"`: identifica su **fila**. Con eso, el lector de pantalla dice "Puntos, 9.850 XP" en vez de solo "9.850 XP".
- `colspan="4"`: una celda que ocupa 4 columnas (`rowspan` para filas).
- Las tablas son **para datos tabulares** (rankings, horarios, facturas), **nunca** para ubicar cosas en la página: eso es trabajo de CSS (de «Flexbox» a «Grid»).

#### Tablas en el celular
Una tabla de 5 columnas en 390 píxeles de ancho se aprieta o se sale de la pantalla. Soluciones: envolverla en una caja con scroll horizontal, o mostrar los mismos datos como **lista de tarjetas** en pantallas chicas. La plataforma de la imagen hace justamente eso: lista en el celular, tabla en la computadora (práctica 21).

#### El ejemplo

La tabla del Hall of Fame (puestos 4 a 10, recortada) con `caption`, encabezados con `scope`, pie con `colspan`.

#### Cómo se ve el ejemplo

Una tabla sin bordes (todavía sin CSS), con los encabezados en negrita y centrados, el título "Clasificación de la temporada 04" arriba y la fila del total abajo. En la captura de celular se ve apretada: es el problema que resolvemos más adelante.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Liga Obsidiana · Tabla</title>
  </head>
  <body>
    <main>
      <h1>Liga Obsidiana: Top 10</h1>

      <table>
        <!-- caption: el titulo de la tabla (lo lee el lector de pantalla) -->
        <caption>Clasificación de la temporada 04</caption>
        <thead>
          <tr>
            <!-- th con scope="col": encabezado de columna -->
            <th scope="col">Puesto</th>
            <th scope="col">Alumno</th>
            <th scope="col">Especialidad</th>
            <th scope="col">Racha</th>
            <th scope="col">Puntos</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>4</td>
            <!-- th con scope="row": el dato que identifica la fila -->
            <th scope="row">@ZeroByte_Arg</th>
            <td>C++ Moderno</td>
            <td>14 días</td>
            <td>10.900 XP</td>
          </tr>
          <tr>
            <td>5</td>
            <th scope="row">@PixelSage</th>
            <td>SDL3 Engine</td>
            <td>11 días</td>
            <td>9.850 XP</td>
          </tr>
          <tr>
            <td>6</td>
            <th scope="row">@CodeKitsune</th>
            <td>OpenGL Shaders</td>
            <td>8 días</td>
            <td>8.920 XP</td>
          </tr>
          <tr>
            <td>10</td>
            <th scope="row">@GhecoDev</th>
            <td>TypeScript Pro</td>
            <td>9 días</td>
            <td>6.400 XP</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <!-- colspan: una celda que ocupa varias columnas -->
            <td colspan="4">Total de la tabla</td>
            <td>36.070 XP</td>
          </tr>
        </tfoot>
      </table>

      <p>
        En el celular, una tabla de 5 columnas no entra: en el nodo «El Hall of Fame» la vamos a
        mostrar como <strong>lista</strong> en pantallas chicas y como
        <strong>tabla</strong> en pantallas grandes.
      </p>
    </main>
  </body>
</html>
```

### ¿Para qué sirve?

Horarios, facturas, comparaciones de precios, tablas de posiciones, resultados de un examen: todo dato que se lee **cruzando una fila con una columna** va en una tabla. Bien hecha, un lector de pantalla puede decir "Iris, racha: 12 días" en lugar de leer números sueltos.

### Errores habituales

**Slime: `td` fuera de un `tr`**: el navegador inventa filas y la tabla se desarma.

**Ogro: filas con distinta cantidad de celdas**: la tabla queda con huecos; revisá los `colspan`.

**Ogro: tabla para maquetar** (logo a la izquierda, menú a la derecha): el lector de pantalla anuncia "tabla de 1 fila y 2 columnas" y en el celular no se adapta.

**Orco: tabla ancha en el celular**: aparece scroll horizontal en toda la página.

### Prueba del sello

#### ¿Qué diferencia hay entre `th` y `td`? ¿Para qué sirve `scope`?

`th` es una celda de **encabezado** (dice qué es la columna o la fila) y `td` una celda de **dato**. `scope="col"` o `scope="row"` le dice al lector de pantalla si ese encabezado manda sobre la columna o sobre la fila, para leer cada dato con su nombre.

#### ¿Para qué **no** se usa una tabla?

Para **acomodar** cosas en la pantalla (columnas, menús, la estructura de la página). Eso se hace con CSS (flexbox y grid). La tabla es solo para datos que tienen filas y columnas de verdad.

#### ¿Qué problema tienen las tablas en el celular y cómo se puede resolver?

Una tabla con muchas columnas **no entra** en una pantalla chica y empuja toda la página de costado (un orco). Se resuelve poniéndola dentro de un contenedor con scroll horizontal propio, o mostrando los mismos datos como tarjetas en el celular (lo vas a hacer en el Hall of Fame).

### Misión R01-N04-M1 · El horario del taller

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá el horario semanal del taller: los días como encabezados de columna, la hora como encabezado de cada fila, y una actividad que dure **dos días** (una celda con `colspan="2"`).

#### Criterio de aprobación

- Tiene `caption` con el título de la tabla.
- Los días son `th` con `scope="col"` y las horas `th` con `scope="row"`.
- Una celda ocupa dos días con `colspan="2"`.

#### Cómo debe quedar

celular: capturas/R01-N04-M1-celular.webp
compu: capturas/R01-N04-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El horario del taller</title>
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
    <title>Horario de clases</title>
  </head>
  <body>
    <main>
      <h1>Horario del taller</h1>
      <table>
        <caption>Clases de la semana</caption>
        <thead>
          <tr>
            <th scope="col">Hora</th>
            <th scope="col">Lunes</th>
            <th scope="col">Miércoles</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">18:00</th>
            <td>HTML</td>
            <td>CSS</td>
          </tr>
          <tr>
            <th scope="row">20:00</th>
            <td colspan="2">Práctica libre</td>
          </tr>
        </tbody>
      </table>
    </main>
  </body>
</html>
```


### Misión R01-N04-M2 · Comparar planes

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá una tabla que compare el plan **Gratis** con el plan **Supremo**: las características en las filas y los planes en las columnas, con encabezados de fila y de columna.

#### Criterio de aprobación

- Tiene `caption`, `thead` y `tbody`.
- Hay encabezados de columna (`scope="col"`) y de fila (`scope="row"`).
- Leída en voz alta, cada dato se entiende con su característica y su plan.

#### Cómo debe quedar

celular: capturas/R01-N04-M2-celular.webp
compu: capturas/R01-N04-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Comparar planes</title>
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
    <title>Comparar planes</title>
  </head>
  <body>
    <main>
      <h1>Planes</h1>
      <table>
        <caption>Comparación de planes de la plataforma</caption>
        <thead>
          <tr>
            <th scope="col">Característica</th>
            <th scope="col">Gratis</th>
            <th scope="col">Supremo</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">Cursos</th>
            <td>3</td>
            <td>Todos</td>
          </tr>
          <tr>
            <th scope="row">Certificado</th>
            <td>No</td>
            <td>Sí</td>
          </tr>
        </tbody>
      </table>
    </main>
  </body>
</html>
```


### Encargo R01-N04-E1 · La factura

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Un almacén necesita una factura: productos, cantidad, precio unitario y subtotal, y el **total** al pie, en un `tfoot`.

#### Criterio de aprobación

- Usa `thead`, `tbody` y `tfoot`; el total va en el `tfoot`.
- Los encabezados son `th` con `scope`.

#### Cómo debe quedar

celular: capturas/R01-N04-E1-celular.webp
compu: capturas/R01-N04-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La factura</title>
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
    <title>Factura</title>
  </head>
  <body>
    <main>
      <h1>Factura N.º 0001-00001234</h1>
      <table>
        <caption>Detalle de la compra</caption>
        <thead>
          <tr>
            <th scope="col">Producto</th>
            <th scope="col">Cantidad</th>
            <th scope="col">Precio</th>
            <th scope="col">Subtotal</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">Teclado</th>
            <td>1</td>
            <td>$30000</td>
            <td>$30000</td>
          </tr>
          <tr>
            <th scope="row">Mouse</th>
            <td>2</td>
            <td>$12000</td>
            <td>$24000</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <th scope="row" colspan="3">Total</th>
            <td>$54000</td>
          </tr>
        </tfoot>
      </table>
    </main>
  </body>
</html>
```

## R01-N05 · Jefe: el Slime de las Etiquetas Huérfanas

```meta
tipo: jefe
padre: R01-N04
precio: 10
criatura: dragon
insignia: Soldador de plomo
insignia_descripcion: Venciste al Slime de las Etiquetas Huérfanas: tu HTML se sostiene solo.
usa: html.estructura, html.semantica, html.texto, html.formularios
```

### Crónica

Una mañana, el escaparate de la panadería del Gremio amanece **derretido**: los títulos chorrean sobre los párrafos, la lista se escapó de su caja y todo, hasta el teléfono, sale en negrita. En el medio, temblando, está el **Slime de las Etiquetas Huérfanas**, un slime de vidrio derretido, gordo de tanto comer cierres que nadie escribió.

Iris quiere arreglar primero lo que se ve más feo. —No lo vas a vencer así —dice {mentor}—. Se alimenta de etiquetas sin cerrar. **Cerralas todas**, de adentro hacia afuera, y se queda sin comida.

Cuando cae el último cierre, el slime se encoge hasta ser una gotita y se va rodando. {mentor} le pide a Iris el fragmento astillado, lo rodea con una varilla de plomo y lo cuelga en la ventana: ahora se sostiene solo, **el Fragmento Emplomado**. Lo mira de cerca con el monóculo y frunce el ceño. —Este plomo no es de los Talleres.

### Objetivos

- Encontrar y arreglar etiquetas sin cerrar, mal anidadas y fuera de su lugar.
- Usar el validador como el pergamino que dice dónde está cada slime.
- Corregir una página entera sin cambiar lo que dice: solo su estructura.

### Antes de empezar

- Todos los nodos del Plomo: «Clase 0 · Hola, HTML», «Texto, enlaces e imágenes», «HTML semántico», «Formularios» y «Tablas».

### Explicación

#### Cómo cazar slimes
1. **Validá primero.** Pegá el código en [validator.w3.org](https://validator.w3.org/#validate_by_input). Cada error dice la línea y qué encontró.
2. **Arreglá de arriba hacia abajo.** Un solo `<strong>` sin cerrar puede producir diez errores más abajo: arreglás el primero y los otros desaparecen.
3. **Mirá el árbol en el inspector.** El navegador "adivina" cómo cerrar lo que quedó abierto; en *Elementos* ves cómo lo armó él, y ahí se nota qué quedó adentro de qué.
4. **Revisá lo que no es error, pero está mal:** imágenes sin `alt`, `label` que no apuntan a su campo, un `li` suelto fuera de su lista, niveles de título salteados.

#### Lo que se abre adentro, se cierra adentro
```html
<p>Pan <strong>caliente</strong></p>   <!-- bien -->
<p>Pan <strong>caliente</p></strong>   <!-- slime: se cierran cruzados -->
```

### ¿Para qué sirve?

Arreglar el HTML de otro es una de las tareas más comunes del trabajo real: una página que alguien armó apurado, un correo que se ve roto en un celular, una plantilla vieja. Saber leer el árbol y el validador te ahorra horas.

### Errores habituales

Los slimes de este jefe son los de siempre, pero todos juntos: etiquetas sin cerrar, cierres cruzados, un `li` fuera de su `ul`, un `h3` sin `h2`, una imagen sin `alt` y un `label` que no apunta a ningún campo. El navegador no se queja de ninguno: **el validador sí**.

### Prueba del sello

#### ¿Por qué un solo `<strong>` sin cerrar puede poner en negrita toda la página?

Porque el navegador no sabe dónde terminaba: lo deja abierto hasta que encuentra algo que lo obliga a cerrarlo, y todo lo que está en el medio queda "adentro" del `strong`.

#### ¿Por qué hay que arreglar los errores del validador de arriba hacia abajo?

Porque un error al principio genera otros más abajo (el validador sigue confundido por lo que quedó abierto). Al arreglar el primero, muchos de los siguientes desaparecen solos.

### Misión R01-N05-M1 · El escaparate derretido

```meta
entrega: codigo
entorno: navegador
monedas: 12
xp: 40
```

#### Consigna

Este es el escaparate que derritió el Slime. **Arreglá la estructura sin cambiar los textos**:

1. Cerrá cada etiqueta en su lugar y en el orden correcto.
2. Poné cada `li` dentro de su lista y cada título en su nivel (sin saltear).
3. Agregá lo que falta: el `alt` de la imagen y el `for` del `label`.
4. Pasá el validador hasta que diga *No errors*.

#### Criterio de aprobación

- El validador no marca errores.
- Los textos son los mismos que en el código inicial.
- La página usa `header`, `main` y `footer`; los títulos van de `h1` a `h2` sin saltos.
- La imagen tiene `alt` y el `label` apunta a su campo.

#### Cómo debe quedar

celular: capturas/R01-N05-M1-celular.webp
compu: capturas/R01-N05-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Panadería del Gremio
  </head>
  <body>
    <header>
      <h1>Panadería del Gremio</h2>
      <p>Abierto de <strong>7 a 20 h</p></strong>
    </header>
    <main>
      <h3>Lo de hoy</h3>
      <img src="/img/cursos/html/gheco-logo.webp" width="64" height="64">
      <li>Pan de campo</li>
      <ul>
        <li>Medialunas
        <li>Facturas de dulce de leche</li>
      </ul>
      <h2>Pedidos</h2>
      <form>
        <label>Tu nombre</label>
        <input id="nombre" name="nombre">
        <button>Encargar</button>
      </form>
    <footer>
      <p>Teléfono: <a href="tel:+543804000000">3804 00-0000</a>
    </footer>
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
    <title>Panadería del Gremio</title>
  </head>
  <body>
    <header>
      <h1>Panadería del Gremio</h1>
      <p>Abierto de <strong>7 a 20 h</strong></p>
    </header>
    <main>
      <h2>Lo de hoy</h2>
      <img src="/img/cursos/html/gheco-logo.webp" width="64" height="64" alt="Gheco, la mascota de la panadería">
      <ul>
        <li>Pan de campo</li>
        <li>Medialunas</li>
        <li>Facturas de dulce de leche</li>
      </ul>
      <h2>Pedidos</h2>
      <form>
        <label for="nombre">Tu nombre</label>
        <input id="nombre" name="nombre">
        <button>Encargar</button>
      </form>
    </main>
    <footer>
      <p>Teléfono: <a href="tel:+543804000000">3804 00-0000</a></p>
    </footer>
  </body>
</html>
```
