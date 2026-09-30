# RAMA S04 · Senda del Escaparate: HTML y CSS

```meta
tipo: senda
posicion: 9
```

## S04-N01 · HTML: la estructura de una página

```meta
tipo: tema
padre: R01-N10
precio: 3
moneda: comodin
criatura: slime
ejecutable: no
temas: html.estructura, html.texto, html.semantica
```

### Crónica

Frente al Muelle de las Primeras Cartas hay una calle de tiendas con vidrieras: el **Escaparate del Puerto**. Algunas vidrieras están tan bien armadas que la gente se para a mirar; otras son un montón de cosas tiradas, sin cartel, sin precio, con la puerta escondida.

—Todo lo que tus programas de PHP respondan al navegador va a ser **HTML** —dice {mentor}—. Antes de que llegues a la Oficina de Correos, vení a aprender a armar una vidriera como la gente: con su cartel, sus secciones, sus puertas a las otras tiendas y una etiqueta en cada cosa. Es un camino optativo, {heroe}, pero el que lo recorre después arma páginas que da gusto mirar.

### Objetivos

- Entender qué es HTML: etiquetas, elementos y atributos.
- Armar el esqueleto correcto de una página (`<!DOCTYPE>`, `<head>`, `<body>`).
- Organizar el contenido con títulos, párrafos y etiquetas con significado (`header`, `nav`, `main`, `footer`…).
- Enlazar páginas entre sí y poner imágenes con rutas relativas y texto alternativo.

### Antes de empezar

- La rama del Muelle de las Primeras Cartas (R01). No hace falta saber nada de páginas web.
- Un editor de texto (el mismo que usás para PHP) y un navegador.

### Explicación

#### Etiquetas, elementos y atributos
HTML no es un lenguaje de programación: es un lenguaje para **marcar** qué es cada parte
de un texto. Una **etiqueta** abre y cierra un **elemento**; los **atributos** van en la
etiqueta de apertura:
```html
<a href="menu.html">Ver la carta</a>
<!-- etiqueta <a>, atributo href, contenido "Ver la carta" -->
<img src="img/ancla.svg" alt="Un ancla dorada">
```
Algunas etiquetas no tienen contenido ni cierre (`<img>`, `<br>`, `<meta>`, `<input>`).
Los elementos se **anidan** como cajas dentro de cajas, y se cierran en orden inverso:
`<p><strong>Hoy</strong> abrimos</p>`, nunca `<p><strong>Hoy</p></strong>`.

#### El esqueleto de toda página
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bodegón del Puerto</title>
</head>
<body>
    ... lo que se ve ...
</body>
</html>
```
| Parte | Para qué |
|---|---|
| `<!DOCTYPE html>` | avisa que es HTML moderno |
| `lang="es"` | el idioma: lo usan los lectores de pantalla y los buscadores |
| `<meta charset="utf-8">` | que las tildes y la ñ se vean bien |
| `<meta name="viewport" …>` | que en el celular no se vea achicada |
| `<title>` | el texto de la pestaña y de los resultados de Google |

#### Títulos, párrafos y énfasis
`<h1>` a `<h6>` son títulos por **importancia**, no por tamaño: una página tiene **un**
`<h1>` (de qué trata) y los demás bajan de a uno, sin saltear (`h2` dentro del `h1`,
`h3` dentro de un `h2`). `<p>` es un párrafo; `<strong>` marca algo importante y `<em>`
algo enfatizado. Los espacios y saltos de línea del código **no** cuentan: el navegador
los junta en uno solo.

#### Etiquetas con significado
| Etiqueta | Es |
|---|---|
| `<header>` | la cabecera (logo, título) |
| `<nav>` | el menú de navegación |
| `<main>` | el contenido principal (uno por página) |
| `<section>` | una parte con su propio título |
| `<article>` | algo que se entiende solo (una noticia, una tarjeta) |
| `<aside>` | algo al costado (publicidad, datos extra) |
| `<footer>` | el pie (contacto, derechos) |

Se ven igual que un `<div>` (una caja sin significado), pero los buscadores y los
lectores de pantalla entienden la página.

#### Enlaces e imágenes
```html
<a href="contacto.html">Contacto</a>                    <!-- en la misma carpeta -->
<a href="paginas/historia.html">Nuestra historia</a>    <!-- en una subcarpeta -->
<a href="../index.html">Volver al inicio</a>            <!-- una carpeta arriba -->
<a href="https://es.wikipedia.org/wiki/Puerto" target="_blank" rel="noopener">Wikipedia</a>
<a href="#reservas">Ir a las reservas</a>              <!-- a un id de la misma página -->
<img src="img/ancla.svg" alt="Ancla dorada, el logo del bodegón" width="64" height="64">
```
Las rutas **relativas** (sin `http`) funcionan igual en tu compu y en el hosting. El
`alt` describe la imagen para quien no la ve; si la imagen es solo decoración,
`alt=""`. `width` y `height` evitan que la página "salte" mientras carga.

#### Caracteres especiales
`<`, `>` y `&` tienen significado en HTML: para mostrarlos se escriben `&lt;`, `&gt;` y
`&amp;`. Es exactamente lo que hace `htmlspecialchars` en PHP.

#### Mirar y validar
Abrí el archivo con doble clic o, mejor, servilo con `php -S localhost:8000` en la
carpeta. F12 → **Elementos** muestra el árbol que armó el navegador (si cerraste mal
una etiqueta, lo vas a ver). El validador oficial, `validator.w3.org`, te marca cada
error.

### Código de ejemplo

La portada del **Bodegón del Puerto**, con su logo, menú, secciones y pie. El logo es un
archivo SVG (una imagen hecha de texto: se abre con el editor).

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bodegón del Puerto</title>
</head>
<body>
    <header>
        <img src="img/ancla.svg" alt="Ancla dorada, el logo del bodegón" width="64" height="64">
        <h1>Bodegón del Puerto</h1>
        <p>Pescado fresco frente al muelle desde 1952</p>
    </header>

    <nav>
        <a href="index.html">Inicio</a>
        <a href="carta.html">La carta</a>
        <a href="#donde">Dónde estamos</a>
    </nav>

    <main>
        <section>
            <h2>Hoy en la pizarra</h2>
            <p>Llegó la <strong>merluza</strong> de la madrugada: a la romana o a la plancha.</p>
            <p>Los jueves, <em>cazuela de mariscos</em> para compartir.</p>
        </section>

        <section id="donde">
            <h2>Dónde estamos</h2>
            <p>Muelle 3, al lado de la Torre de Elefa. Abrimos de martes a domingo.</p>
            <p>Precios en pesos &amp; con IVA incluido. Menores de 12 años &lt;mitad de precio&gt;.</p>
        </section>
    </main>

    <footer>
        <p>Bodegón del Puerto · <a href="https://es.wikipedia.org/wiki/Merluza" target="_blank" rel="noopener">¿Qué es la merluza?</a></p>
    </footer>
</body>
</html>
```

`carta.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La carta · Bodegón del Puerto</title>
</head>
<body>
    <header>
        <h1>La carta</h1>
    </header>
    <nav>
        <a href="index.html">Inicio</a>
        <a href="carta.html">La carta</a>
    </nav>
    <main>
        <p>Rabas, empanadas de pescado, merluza, cazuela de mariscos y flan casero.</p>
    </main>
</body>
</html>
```

`img/ancla.svg`
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="12" r="6" fill="none" stroke="#c9a227" stroke-width="4"/>
  <line x1="32" y1="18" x2="32" y2="56" stroke="#c9a227" stroke-width="4"/>
  <line x1="20" y1="28" x2="44" y2="28" stroke="#c9a227" stroke-width="4"/>
  <path d="M10 40 Q32 70 54 40" fill="none" stroke="#c9a227" stroke-width="4"/>
</svg>
```

Corré `php -S localhost:8000` en la carpeta del proyecto y abrí
`http://localhost:8000`. Probá los enlaces, mirá el árbol en F12 → Elementos y pasá la
página por el validador.

### ¿Para qué sirve?

Todo lo que se ve en la web es HTML: las páginas que vas a generar con PHP, los correos con formato, las plantillas de Blade o de WordPress. Una estructura correcta hace que la página funcione en cualquier pantalla, que los buscadores la entiendan y que la pueda usar también una persona ciega con su lector de pantalla.

### Errores habituales

**Slime: la etiqueta sin cerrar.** Un `<strong>` sin `</strong>` deja en negrita todo lo
que sigue. En F12 → Elementos se ve dónde empezó.

**Esqueleto: la imagen rota.** La ruta del `src` no coincide con el archivo: mayúsculas
(`Ancla.svg` ≠ `ancla.svg`, en el hosting importa), carpeta equivocada o `\` en lugar de
`/`.

**Esqueleto: el enlace que lleva a "no encontrado".** Igual que la imagen: la ruta
relativa se cuenta **desde la página donde está el enlace**. Desde `paginas/historia.html`,
el inicio es `../index.html`.

**Ogro: títulos por tamaño.** Usar `<h3>` porque "se ve más chico" rompe el orden de la
página. El tamaño se cambia con CSS; el título se elige por importancia.

**Slime: las tildes rotas (`BodegÃ³n`).** Falta `<meta charset="utf-8">` o el archivo no
está guardado en UTF-8.

**Orco: la imagen sin `alt`.** Quien no la ve no sabe qué hay. Siempre `alt`, vacío si es
decoración.

### Misión S04-N01-M1 · La ficha del barco

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá `index.html`, la **ficha del barco Albatros & Cía**, con el esqueleto completo
(idioma español, UTF-8, viewport y el título `Albatros · Ficha`) y esta estructura:

- un `<header>` con el `<h1>` `Albatros & Cía` (el `&` bien escrito);
- un `<main>` con un `<article>` que tiene tres `<section>`, cada una con su `<h2>`:
  **Datos** (eslora de **32,5 m**, en `<strong>`, y el año de botadura), **Historia**
  (dos párrafos, con alguna palabra en `<em>`) y **Carga** (un párrafo que diga que
  lleva `menos de 500 t`, escrito con el signo `<`: `&lt; 500 t`);
- un `<footer>` con un enlace externo a `https://es.wikipedia.org/wiki/Barco` que se abra
  en otra pestaña de forma segura.

Entregá la carpeta en un zip.

#### Criterio de aprobación

- El esqueleto está completo y hay un solo `<h1>`.
- Los títulos siguen el orden (`h1` → `h2`) y las etiquetas con significado están donde corresponde.
- Los caracteres especiales se escriben con `&amp;` y `&lt;`, y el enlace externo lleva `target="_blank"` y `rel="noopener"`.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Albatros · Ficha</title>
</head>
<body>
    <header>
        <h1>Albatros &amp; Cía</h1>
    </header>
    <main>
        <article>
            <section>
                <h2>Datos</h2>
                <p>Eslora: <strong>32,5 m</strong>. Botado en 1987 en el astillero del Puerto.</p>
            </section>
            <section>
                <h2>Historia</h2>
                <p>Empezó llevando pasajeros a Colonia y hoy es el barco de carga más <em>confiable</em> del muelle.</p>
                <p>En 2004 sobrevivió a la gran tormenta sin perder un solo cajón.</p>
            </section>
            <section>
                <h2>Carga</h2>
                <p>Lleva &lt; 500 t por viaje: cajones de fruta, correo y alguna que otra gallina.</p>
            </section>
        </article>
    </main>
    <footer>
        <p><a href="https://es.wikipedia.org/wiki/Barco" target="_blank" rel="noopener">¿Qué es un barco?</a></p>
    </footer>
</body>
</html>
```

### Misión S04-N01-M2 · Las tres puertas

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá un sitio de tres páginas para la **Torre del Puerto** con esta estructura de
carpetas:
```
index.html
paginas/historia.html
paginas/contacto.html
img/torre.svg
```
Las tres páginas tienen el mismo `<nav>` con enlaces a las tres (con las rutas
relativas correctas **desde cada una**) y un solo `<h1>`. La portada muestra el dibujo
`img/torre.svg` (hacelo vos: un rectángulo y un triángulo alcanzan) con su `alt`, y
también se ve en `historia.html` (ojo con la ruta). `contacto.html` tiene un enlace
`Volver arriba` que lleva a un `id` al principio de la misma página. Ningún enlace ni
imagen puede quedar roto. Entregá la carpeta en un zip.

#### Criterio de aprobación

- Los tres menús llevan a las tres páginas desde cualquier lugar (rutas relativas bien contadas).
- Las imágenes cargan en las dos páginas y tienen `alt`.
- El enlace interno usa `#` y un `id`.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Torre del Puerto</title>
</head>
<body>
    <nav>
        <a href="index.html">Inicio</a>
        <a href="paginas/historia.html">Historia</a>
        <a href="paginas/contacto.html">Contacto</a>
    </nav>
    <main>
        <h1>Torre del Puerto</h1>
        <img src="img/torre.svg" alt="Dibujo de la Torre del Puerto" width="80" height="120">
        <p>Desde acá Elefa ve llegar cada barco.</p>
    </main>
</body>
</html>
```

`paginas/historia.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Historia · Torre del Puerto</title>
</head>
<body>
    <nav>
        <a href="../index.html">Inicio</a>
        <a href="historia.html">Historia</a>
        <a href="contacto.html">Contacto</a>
    </nav>
    <main>
        <h1>Historia de la torre</h1>
        <img src="../img/torre.svg" alt="La torre, tal como se construyó en 1890" width="80" height="120">
        <p>La construyeron en 1890 con piedras del mismo muelle.</p>
    </main>
</body>
</html>
```

`paginas/contacto.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Contacto · Torre del Puerto</title>
</head>
<body id="arriba">
    <nav>
        <a href="../index.html">Inicio</a>
        <a href="historia.html">Historia</a>
        <a href="contacto.html">Contacto</a>
    </nav>
    <main>
        <h1>Contacto</h1>
        <p>Escribinos a torre@puerto.test o subí los 214 escalones.</p>
        <p><a href="#arriba">Volver arriba</a></p>
    </main>
</body>
</html>
```

`img/torre.svg`
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 120" width="80" height="120">
  <polygon points="40,5 70,35 10,35" fill="#b3261e"/>
  <rect x="18" y="35" width="44" height="80" fill="#e8e0c8" stroke="#555" stroke-width="2"/>
  <rect x="34" y="85" width="12" height="30" fill="#555"/>
</svg>
```

### Misión S04-N01-M3 · La noticia del diario

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

El diario del Puerto publica la noticia **"Llegó el ferry nuevo"**. Armá `index.html`
con la noticia como un `<article>`:

- un `<header>` propio del artículo con el `<h1>` y la fecha en un
  `<time datetime="2026-10-03">3 de octubre de 2026</time>`;
- tres párrafos;
- una cita del capitán en `<blockquote>`, y quién la dijo en `<cite>`;
- una `<figure>` con la imagen (`img/ferry.svg`, hecha por vos) y su `<figcaption>`;
- al costado, un `<aside>` con **Datos del ferry** (un `<h2>` y dos párrafos).

Entregá la carpeta en un zip.

#### Criterio de aprobación

- La fecha usa `<time>` con el atributo `datetime` en formato AAAA-MM-DD.
- La cita, la figura y el aside usan sus etiquetas.
- La imagen carga y tiene `alt`.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Llegó el ferry nuevo · Diario del Puerto</title>
</head>
<body>
    <main>
        <article>
            <header>
                <h1>Llegó el ferry nuevo</h1>
                <p>Publicado el <time datetime="2026-10-03">3 de octubre de 2026</time></p>
            </header>
            <p>A las siete de la mañana, entre bocinazos y gaviotas, amarró en el muelle 2 el <em>Estrella del Sur</em>.</p>
            <p>Lleva hasta 400 pasajeros y 60 autos, y va a cubrir el cruce a Colonia tres veces por día.</p>
            <p>La primera salida con pasajeros será el lunes a las 8:30.</p>
            <blockquote>
                <p>Es el barco más estable que manejé en mi vida.</p>
                <cite>Capitana Nora Alvear</cite>
            </blockquote>
            <figure>
                <img src="img/ferry.svg" alt="El ferry Estrella del Sur amarrado en el muelle 2" width="160" height="80">
                <figcaption>El Estrella del Sur en su primera mañana en el Puerto.</figcaption>
            </figure>
        </article>
        <aside>
            <h2>Datos del ferry</h2>
            <p>Eslora: 54,2 m. Velocidad: 22 nudos.</p>
            <p>Construido en Vigo en 2025.</p>
        </aside>
    </main>
</body>
</html>
```

`img/ferry.svg`
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 80" width="160" height="80">
  <rect x="0" y="60" width="160" height="20" fill="#2a6f97"/>
  <polygon points="10,45 150,45 135,65 25,65" fill="#f2f2f2" stroke="#333" stroke-width="2"/>
  <rect x="45" y="25" width="70" height="20" fill="#f2f2f2" stroke="#333" stroke-width="2"/>
  <rect x="70" y="10" width="10" height="15" fill="#b3261e"/>
</svg>
```

### Encargo S04-N01-E1 · La página del capitán

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Armá tu **página personal de capitán o capitana** (inventá el personaje). Dos páginas:
`index.html` y `bitacora.html`, más un retrato en `img/retrato.svg`. Tienen que tener:

- el esqueleto completo, un solo `<h1>` por página y títulos en orden;
- `<header>`, `<nav>` (con enlaces entre las dos páginas), `<main>` y `<footer>` en las dos;
- en `index.html`: el retrato con `alt`, una presentación con `<strong>` y `<em>`, y un
  enlace a la sección `#viajes` de `bitacora.html` (`bitacora.html#viajes`);
- en `bitacora.html`: dos `<article>` (dos viajes), cada uno con su `<h2>` y su
  `<time datetime="…">`, dentro de una `<section id="viajes">`;
- en el pie de las dos, un enlace externo seguro.

Entregá la carpeta en un zip.

#### Criterio de aprobación

- Las dos páginas tienen el esqueleto y la estructura pedida, sin enlaces ni imágenes rotas.
- El enlace a `bitacora.html#viajes` lleva a la sección.
- Los viajes usan `<article>` y `<time>` con `datetime`.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Capitana Marga Rulos</title>
</head>
<body>
    <header>
        <img src="img/retrato.svg" alt="Retrato de la capitana Marga Rulos con su gorra" width="96" height="96">
        <h1>Capitana Marga Rulos</h1>
    </header>
    <nav>
        <a href="index.html">Inicio</a>
        <a href="bitacora.html">Bitácora</a>
    </nav>
    <main>
        <section>
            <h2>Quién soy</h2>
            <p>Navego desde los quince años y tengo el récord de <strong>cruces sin demora</strong> del Puerto.</p>
            <p>Me gusta el mar <em>picado</em>, el mate amargo y los faros.</p>
            <p><a href="bitacora.html#viajes">Leé mis últimos viajes</a></p>
        </section>
    </main>
    <footer>
        <p><a href="https://es.wikipedia.org/wiki/Capit%C3%A1n_de_barco" target="_blank" rel="noopener">¿Qué hace una capitana?</a></p>
    </footer>
</body>
</html>
```

`bitacora.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bitácora · Capitana Marga Rulos</title>
</head>
<body>
    <header>
        <h1>Bitácora</h1>
    </header>
    <nav>
        <a href="index.html">Inicio</a>
        <a href="bitacora.html">Bitácora</a>
    </nav>
    <main>
        <section id="viajes">
            <article>
                <h2>A Colonia con niebla</h2>
                <p><time datetime="2026-09-12">12 de septiembre</time>: salimos con niebla cerrada y llegamos a horario.</p>
            </article>
            <article>
                <h2>La noche de la tormenta</h2>
                <p><time datetime="2026-09-20">20 de septiembre</time>: olas de tres metros, ningún pasajero mareado.</p>
            </article>
        </section>
    </main>
    <footer>
        <p><a href="https://es.wikipedia.org/wiki/Bit%C3%A1cora" target="_blank" rel="noopener">¿Qué es una bitácora?</a></p>
    </footer>
</body>
</html>
```

`img/retrato.svg`
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96">
  <circle cx="48" cy="56" r="28" fill="#f1c27d"/>
  <rect x="22" y="18" width="52" height="16" rx="4" fill="#1d3557"/>
  <rect x="16" y="32" width="64" height="6" fill="#1d3557"/>
  <circle cx="38" cy="54" r="3" fill="#333"/>
  <circle cx="58" cy="54" r="3" fill="#333"/>
  <path d="M38 68 Q48 76 58 68" fill="none" stroke="#333" stroke-width="3"/>
</svg>
```

### Prueba del sello

#### ¿Cuántos `<h1>` tiene que tener una página?

Uno: el título de lo que trata la página. Los demás títulos bajan de a uno (`h2`, `h3`…).

#### ¿Para qué sirve el atributo `alt` de una imagen?

Describe la imagen para quien no la ve (lectores de pantalla, imagen que no cargó, buscadores). Si es solo decoración, va vacío.

#### Desde `paginas/historia.html`, ¿cómo se enlaza `index.html`, que está una carpeta arriba?

Con `../index.html`: las rutas relativas se cuentan desde la página donde está el enlace.

#### ¿Cómo se muestra el signo `<` en una página?

Escribiendo `&lt;` (como hace `htmlspecialchars` en PHP), porque `<` abre una etiqueta.

#### ¿Qué diferencia hay entre `<section>` y `<div>`?

Se ven igual, pero `<section>` dice que es una parte del contenido con su propio título; `<div>` es una caja sin significado.

### Soluciones (docente)

Contenido nuevo, pedido por el docente como camino optativo antes de la Oficina de Correos. Se verifica abriendo cada página en un navegador real (Chromium): un solo `<h1>`, `lang="es"`, todas las imágenes cargan y tienen `alt`, todos los enlaces locales responden, y la estructura pedida (etiquetas, `datetime`, `rel="noopener"`). Para corregir: descomprimir, `php -S localhost:8000` en la carpeta y recorrer; el validador `validator.w3.org` ayuda a encontrar cierres mal hechos.

## S04-N02 · Listas, tablas y formularios

```meta
tipo: tema
padre: S04-N01
precio: 10
criatura: orc
ejecutable: no
temas: html.listas-tablas, html.formularios
```

### Crónica

En la vidriera de la ferretería del Puerto todo está en orden: una lista de lo que hay, una tabla de precios con su encabezado, y en la puerta un formulario para encargar lo que falta. El dueño dice que desde que ordenó la vidriera vende el doble, y que los encargos le llegan completos.

—Las listas y las tablas ordenan los datos; los formularios los piden —dice {mentor}—. Y un formulario bien hecho, {heroe}, es la mitad del trabajo de PHP: cada campo con su nombre, su etiqueta y sus límites. Lo que armes acá es lo que vas a recibir en `$_POST` en la Oficina de Correos.

### Objetivos

- Ordenar contenido con listas (`ul`, `ol`, `dl`) y listas anidadas.
- Armar tablas accesibles con encabezados, pie y celdas combinadas.
- Construir formularios con etiquetas asociadas, tipos de campo y validación del navegador.
- Entender qué manda un formulario (`name`, `value`, `method`).

### Antes de empezar

- El nodo anterior (estructura de una página).

### Explicación

#### Listas
```html
<ul>                         <!-- sin orden: viñetas -->
    <li>Soga</li>
    <li>Boyas
        <ul><li>naranjas</li><li>blancas</li></ul>     <!-- anidada: va DENTRO del li -->
    </li>
</ul>
<ol>                         <!-- con orden: pasos numerados -->
    <li>Soltar amarras</li>
    <li>Encender el motor</li>
</ol>
<dl>                         <!-- de definiciones: término y descripción -->
    <dt>Eslora</dt><dd>El largo del barco.</dd>
    <dt>Calado</dt><dd>Cuánto se hunde bajo el agua.</dd>
</dl>
```
Un menú de navegación también es una lista: `<nav><ul><li><a>…</a></li></ul></nav>`.

#### Tablas
Las tablas son para **datos en filas y columnas** (horarios, precios), no para acomodar
la página.
```html
<table>
    <caption>Salidas del ferry</caption>          <!-- el título de la tabla -->
    <thead>
        <tr><th scope="col">Hora</th><th scope="col">Destino</th><th scope="col">Lugares</th></tr>
    </thead>
    <tbody>
        <tr><td>08:30</td><td>Colonia</td><td>120</td></tr>
        <tr><td>13:00</td><td colspan="2">Cancelado por viento</td></tr>   <!-- ocupa 2 columnas -->
    </tbody>
    <tfoot>
        <tr><th scope="row" colspan="2">Total</th><td>120</td></tr>
    </tfoot>
</table>
```
`<th>` es una celda de encabezado; `scope="col"` o `scope="row"` dice qué encabeza (los
lectores de pantalla lo leen al pasar por cada dato). `rowspan` combina filas.

#### Formularios
```html
<form action="reservar.php" method="post">
    <label for="nombre">Nombre</label>
    <input id="nombre" name="nombre" required maxlength="40">

    <label for="personas">Personas</label>
    <input id="personas" name="personas" type="number" min="1" max="12" value="2">

    <fieldset>
        <legend>Turno</legend>
        <label><input type="radio" name="turno" value="mediodia" checked> Mediodía</label>
        <label><input type="radio" name="turno" value="noche"> Noche</label>
    </fieldset>

    <label><input type="checkbox" name="terraza" value="si"> En la terraza</label>

    <label for="plato">Plato</label>
    <select id="plato" name="plato">
        <option value="">Elegí…</option>
        <option value="merluza">Merluza</option>
    </select>

    <label for="notas">Notas</label>
    <textarea id="notas" name="notas" rows="3"></textarea>

    <button type="submit">Reservar</button>
</form>
```
| Pieza | Para qué |
|---|---|
| `name` | la clave con la que llega el dato (`$_POST['nombre']`); sin `name`, no se manda |
| `<label for="id">` | asocia el texto al campo: tocar el texto enfoca el campo (y lo lee el lector de pantalla) |
| `type` | `text`, `email`, `number`, `date`, `password`, `tel`, `checkbox`, `radio`… |
| `required`, `min`, `max`, `maxlength`, `pattern` | validación del navegador, antes de mandar |
| `method` | `get` (los datos van en la URL: búsquedas) o `post` (en el cuerpo: todo lo que guarda) |

Los `radio` con el **mismo** `name` forman un grupo (se elige uno). Un `checkbox` sin
marcar **no se manda**. La validación del navegador es una ayuda para el usuario, no
una protección: PHP siempre vuelve a validar.

### Código de ejemplo

La página de **reservas del bodegón**: la carta en una tabla, la lista de lo que incluye
el menú del día y el formulario de reserva. `gracias.html` es la página a la que va el
formulario (con `method="get"` se ven los datos en la URL: probalo).

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Reservas · Bodegón del Puerto</title>
</head>
<body>
    <main>
        <h1>Reservá tu mesa</h1>

        <section>
            <h2>El menú del día incluye</h2>
            <ol>
                <li>Entrada: rabas o empanada</li>
                <li>Principal
                    <ul>
                        <li>Merluza a la romana</li>
                        <li>Cazuela de mariscos (con recargo)</li>
                    </ul>
                </li>
                <li>Postre: flan casero</li>
            </ol>
        </section>

        <section>
            <h2>Precios</h2>
            <table>
                <caption>La carta de hoy</caption>
                <thead>
                    <tr><th scope="col">Plato</th><th scope="col">Precio</th></tr>
                </thead>
                <tbody>
                    <tr><td>Menú del día</td><td>$ 12.500</td></tr>
                    <tr><td>Recargo por cazuela</td><td>$ 3.000</td></tr>
                </tbody>
                <tfoot>
                    <tr><td colspan="2">Precios con IVA incluido</td></tr>
                </tfoot>
            </table>
        </section>

        <section>
            <h2>Tus datos</h2>
            <form action="gracias.html" method="get">
                <label for="nombre">Nombre</label>
                <input id="nombre" name="nombre" required maxlength="40">

                <label for="personas">Personas</label>
                <input id="personas" name="personas" type="number" min="1" max="12" value="2" required>

                <label for="dia">Día</label>
                <input id="dia" name="dia" type="date" required>

                <fieldset>
                    <legend>Turno</legend>
                    <label><input type="radio" name="turno" value="mediodia" checked> Mediodía</label>
                    <label><input type="radio" name="turno" value="noche"> Noche</label>
                </fieldset>

                <label><input type="checkbox" name="terraza" value="si"> En la terraza</label>

                <button type="submit">Reservar</button>
            </form>
        </section>
    </main>
</body>
</html>
```

`gracias.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>¡Gracias! · Bodegón del Puerto</title>
</head>
<body>
    <main>
        <h1>¡Reserva recibida!</h1>
        <p>Mirá la barra de direcciones: ahí están los datos que mandó el formulario.</p>
        <p><a href="index.html">Volver</a></p>
    </main>
</body>
</html>
```

Probá mandar el formulario vacío (el navegador no te deja), con 20 personas (tampoco) y
bien completo: en `gracias.html` mirá la URL. ¿Aparece `terraza` si no la marcaste?

### ¿Para qué sirve?

Casi toda la información de la web está en listas y tablas, y casi toda la interacción pasa por formularios. Un formulario con `label`, `name` y límites bien puestos es más cómodo para el usuario, funciona en el celular (con el teclado numérico o el calendario) y le llega a PHP con los datos ordenados.

### Errores habituales

**Orco: el campo sin `name`.** Se ve, se completa… y no se manda. En PHP,
`Undefined array key`.

**Orco: el `radio` suelto.** Si cada opción tiene un `name` distinto, se pueden marcar
todas. Un grupo comparte el `name`.

**Esqueleto: el `label` que no se asocia.** El `for` tiene que ser igual al `id` del
campo (o el campo va adentro del `label`).

**Ogro: la tabla para acomodar la página.** Las tablas son para datos. Para acomodar,
CSS (lo ves en los próximos nodos).

**Slime: la lista anidada afuera del `li`.** `<ul><li>A</li><ul>…</ul></ul>` es
inválido: la sublista va **adentro** del `<li>`.

**Troll: confiar en `required`.** Cualquiera saltea la validación del navegador (F12 o
`curl`). PHP valida siempre de nuevo.

### Misión S04-N02-M1 · Los horarios del ferry

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá `index.html` con la tabla de **horarios del ferry a Colonia**:

| Salida | Barco | Lugares libres |
|---|---|---|
| 08:30 | Estrella del Sur | 120 |
| 13:00 | Gaviota | 45 |
| 17:45 | *(cancelado por viento: ocupa las columnas de barco y lugares)* | |
| 21:00 | Estrella del Sur | 210 |

con `caption` (`Ferry a Colonia · sábado`), `thead` con `th scope="col"`, la hora de
cada fila como `th scope="row"`, la fila cancelada con `colspan="2"` y un `tfoot` con
`Total de lugares` y `375`. Debajo, una lista `dl` que explique **Salida**, **Lugares
libres** y **Cancelado**. Entregá la carpeta en un zip.

#### Criterio de aprobación

- La tabla tiene `caption`, `thead`, `tbody` y `tfoot`, con `scope` en los encabezados.
- La fila cancelada combina dos columnas con `colspan`.
- Las definiciones van en una `dl` con `dt` y `dd`.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Horarios del ferry</title>
</head>
<body>
    <main>
        <h1>Horarios del ferry</h1>
        <table>
            <caption>Ferry a Colonia · sábado</caption>
            <thead>
                <tr><th scope="col">Salida</th><th scope="col">Barco</th><th scope="col">Lugares libres</th></tr>
            </thead>
            <tbody>
                <tr><th scope="row">08:30</th><td>Estrella del Sur</td><td>120</td></tr>
                <tr><th scope="row">13:00</th><td>Gaviota</td><td>45</td></tr>
                <tr><th scope="row">17:45</th><td colspan="2">Cancelado por viento</td></tr>
                <tr><th scope="row">21:00</th><td>Estrella del Sur</td><td>210</td></tr>
            </tbody>
            <tfoot>
                <tr><th scope="row" colspan="2">Total de lugares</th><td>375</td></tr>
            </tfoot>
        </table>
        <dl>
            <dt>Salida</dt>
            <dd>La hora en que el ferry suelta amarras (hay que estar 30 minutos antes).</dd>
            <dt>Lugares libres</dt>
            <dd>Pasajes que todavía se pueden comprar.</dd>
            <dt>Cancelado</dt>
            <dd>El viaje no sale; el pasaje se cambia sin cargo.</dd>
        </dl>
    </main>
</body>
</html>
```

### Misión S04-N02-M2 · La inscripción a la regata

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá el formulario de **inscripción a la regata del Puerto** (`index.html`, que manda
por `get` a `gracias.html`). Cada campo con su `<label>` asociado:

- `barco`: texto obligatorio, hasta 30 letras;
- `email`: de tipo correo, obligatorio;
- `tripulantes`: número de 1 a 8, obligatorio;
- `categoria`: un `<select>` obligatorio con `vela`, `remo` y `motor` (y una primera
  opción vacía `Elegí…`);
- `fecha_nacimiento` del capitán: fecha, obligatoria;
- `reglamento`: casilla obligatoria (`Leí el reglamento`).

Entregá la carpeta en un zip.

#### Criterio de aprobación

- Cada campo tiene `name` y un `label` asociado por `for`/`id`.
- El navegador no deja mandar el formulario incompleto ni con 9 tripulantes.
- Completo, llega a `gracias.html` con los datos en la URL.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Inscripción a la regata</title>
</head>
<body>
    <main>
        <h1>Inscripción a la regata</h1>
        <form action="gracias.html" method="get">
            <p>
                <label for="barco">Nombre del barco</label>
                <input id="barco" name="barco" required maxlength="30">
            </p>
            <p>
                <label for="email">Correo</label>
                <input id="email" name="email" type="email" required>
            </p>
            <p>
                <label for="tripulantes">Tripulantes</label>
                <input id="tripulantes" name="tripulantes" type="number" min="1" max="8" required>
            </p>
            <p>
                <label for="categoria">Categoría</label>
                <select id="categoria" name="categoria" required>
                    <option value="">Elegí…</option>
                    <option value="vela">Vela</option>
                    <option value="remo">Remo</option>
                    <option value="motor">Motor</option>
                </select>
            </p>
            <p>
                <label for="fecha_nacimiento">Nacimiento del capitán</label>
                <input id="fecha_nacimiento" name="fecha_nacimiento" type="date" required>
            </p>
            <p>
                <input id="reglamento" name="reglamento" type="checkbox" value="si" required>
                <label for="reglamento">Leí el reglamento</label>
            </p>
            <button type="submit">Inscribirme</button>
        </form>
    </main>
</body>
</html>
```

`gracias.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>¡Inscripto!</title>
</head>
<body>
    <main>
        <h1>¡Inscripción recibida!</h1>
        <p><a href="index.html">Inscribir otro barco</a></p>
    </main>
</body>
</html>
```

### Misión S04-N02-M3 · La receta de la abuela del muelle

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá `index.html` con la receta de la **cazuela de mariscos**:

- un `<h1>` con el nombre y una `dl` con **Porciones** (4), **Tiempo** (50 minutos) y
  **Dificultad** (media);
- los **ingredientes** en una lista sin orden, con una sublista **dentro** de
  "Mariscos" (mejillones, calamar, langostinos);
- los **pasos** en una lista **ordenada** de al menos cinco pasos;
- un **consejo** final en un `<aside>`.

Entregá la carpeta en un zip.

#### Criterio de aprobación

- Ingredientes en `ul` con una sublista bien anidada (dentro del `li`).
- Pasos en `ol` (al menos cinco) y datos en `dl`.
- Un solo `<h1>` y títulos `<h2>` para cada parte.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Cazuela de mariscos</title>
</head>
<body>
    <main>
        <h1>Cazuela de mariscos</h1>
        <dl>
            <dt>Porciones</dt><dd>4</dd>
            <dt>Tiempo</dt><dd>50 minutos</dd>
            <dt>Dificultad</dt><dd>media</dd>
        </dl>

        <h2>Ingredientes</h2>
        <ul>
            <li>1 cebolla y 1 morrón</li>
            <li>2 tomates</li>
            <li>Mariscos
                <ul>
                    <li>500 g de mejillones</li>
                    <li>1 calamar en anillos</li>
                    <li>300 g de langostinos</li>
                </ul>
            </li>
            <li>1 vaso de vino blanco</li>
        </ul>

        <h2>Pasos</h2>
        <ol>
            <li>Picar la cebolla y el morrón.</li>
            <li>Rehogarlos en la cazuela con aceite.</li>
            <li>Agregar el tomate y cocinar 10 minutos.</li>
            <li>Sumar el calamar y el vino; cocinar 15 minutos.</li>
            <li>Agregar mejillones y langostinos, tapar y cocinar 8 minutos más.</li>
        </ol>

        <aside>
            <h2>Consejo</h2>
            <p>Tirá los mejillones que no se abrieron: no están buenos.</p>
        </aside>
    </main>
</body>
</html>
```

### Encargo S04-N02-E1 · La encuesta del puerto

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

La torre quiere saber qué opinan los visitantes. Armá `index.html` con una **encuesta**
que manda por `get` a `gracias.html`:

- `visita`: grupo de `radio` con `primera` y `habitual` (una marcada de entrada), dentro
  de un `fieldset` con su `legend`;
- `servicios`: **casillas** para `ferry`, `bodegon` y `torre`, con el **mismo** `name`
  `servicios[]` (así PHP las recibe como array);
- `puntaje`: número de 1 a 10;
- `barrio`: un `<select>` con cuatro opciones;
- `comentario`: `textarea` de hasta 300 letras (opcional);
- botón **Mandar** y botón para **Borrar todo** (`type="reset"`).

En `gracias.html` agregá una nota que explique cómo llegan las casillas a PHP. Entregá
la carpeta en un zip.

#### Criterio de aprobación

- Los radios forman un grupo y las casillas usan `servicios[]`.
- Todos los campos tienen `label` (los grupos, `fieldset` y `legend`).
- Al mandar, la URL lleva `servicios[]` una vez por cada casilla marcada.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Encuesta del Puerto</title>
</head>
<body>
    <main>
        <h1>¿Qué te pareció el Puerto?</h1>
        <form action="gracias.html" method="get">
            <fieldset>
                <legend>¿Es tu primera visita?</legend>
                <label><input type="radio" name="visita" value="primera" checked> Sí, la primera</label>
                <label><input type="radio" name="visita" value="habitual"> No, vengo seguido</label>
            </fieldset>

            <fieldset>
                <legend>¿Qué usaste?</legend>
                <label><input type="checkbox" name="servicios[]" value="ferry"> Ferry</label>
                <label><input type="checkbox" name="servicios[]" value="bodegon"> Bodegón</label>
                <label><input type="checkbox" name="servicios[]" value="torre"> Visita a la torre</label>
            </fieldset>

            <p>
                <label for="puntaje">Puntaje (1 a 10)</label>
                <input id="puntaje" name="puntaje" type="number" min="1" max="10" required>
            </p>
            <p>
                <label for="barrio">¿De dónde venís?</label>
                <select id="barrio" name="barrio">
                    <option value="centro">Centro</option>
                    <option value="costa">La Costa</option>
                    <option value="alto">Barrio Alto</option>
                    <option value="afuera">De otra ciudad</option>
                </select>
            </p>
            <p>
                <label for="comentario">Comentario (opcional)</label>
                <textarea id="comentario" name="comentario" maxlength="300" rows="4"></textarea>
            </p>
            <button type="submit">Mandar</button>
            <button type="reset">Borrar todo</button>
        </form>
    </main>
</body>
</html>
```

`gracias.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>¡Gracias por opinar!</title>
</head>
<body>
    <main>
        <h1>¡Gracias por opinar!</h1>
        <p>Las casillas llegan a PHP como un array: <code>$_GET['servicios']</code> vale, por ejemplo, <code>['ferry', 'torre']</code>. Si no marcaste ninguna, la clave no existe.</p>
        <p><a href="index.html">Volver</a></p>
    </main>
</body>
</html>
```

### Prueba del sello

#### ¿Qué pasa con un campo de formulario que no tiene `name`?

No se manda: el servidor nunca lo recibe.

#### ¿Cómo se hace para que varios `radio` sean un solo grupo?

Dándoles el mismo `name`: así solo se puede elegir uno.

#### ¿Para qué sirve `<th scope="col">`?

Marca la celda como encabezado de su columna, para que los lectores de pantalla la anuncien junto a cada dato.

#### ¿Dónde va una lista anidada?

Dentro del `<li>` al que pertenece, nunca suelta entre dos `<li>`.

#### Si el formulario tiene `required`, ¿PHP puede confiar en que el dato llegó?

No: la validación del navegador se puede saltear. PHP tiene que validar siempre.

### Soluciones (docente)

Contenido nuevo. Se verifica en Chromium: estructura de listas y tablas (`caption`, `scope`, `colspan`, anidado), cada campo con `name` y `label` asociado, la validación del navegador (`checkValidity`) vacío y completo, y el envío real del formulario (los datos llegan en la URL de `gracias.html`). Para corregir, probar el formulario vacío, con valores fuera de rango y completo.

## S04-N03 · CSS: selectores, colores y cajas

```meta
tipo: tema
padre: S04-N02
precio: 10
criatura: ogre
ejecutable: no
temas: css.selectores, css.caja
usa: html.estructura
```

### Crónica

La vidriera de la ferretería ya está ordenada, pero es gris: todo del mismo tamaño, pegado a los bordes, sin un color que llame la atención. En la tienda de al lado, la de las velas, un letrero rojo con letras claras y un marco de madera hace que todos entren.

—El HTML dice **qué** es cada cosa; el **CSS** dice **cómo se ve** —dice {mentor}—. Los colores, las letras, los márgenes, los marcos. Y como una buena tienda, {heroe}, se decide en un solo lugar: si mañana cambiás el rojo del letrero, cambia en todas las vidrieras a la vez.

### Objetivos

- Conectar una hoja de estilos y escribir reglas de CSS.
- Elegir elementos con selectores (etiqueta, clase, id, descendiente, estados).
- Entender la cascada y la especificidad: qué regla gana.
- Usar colores, variables, tipografía y unidades.
- Manejar el modelo de caja: `margin`, `border`, `padding`, `width` y `box-sizing`.

### Antes de empezar

- Los nodos de HTML de esta senda.

### Explicación

#### Una hoja de estilos para todas las páginas
```html
<link rel="stylesheet" href="css/estilos.css">     <!-- en el <head> de cada página -->
```
```css
/* css/estilos.css: una regla = selector { propiedad: valor; } */
h1 {
    color: #0b3d5c;
    font-size: 2rem;
}
```
Con un archivo aparte, todas las páginas comparten el diseño. (Existen también
`<style>` en el `<head>` y el atributo `style="…"`, pero mezclan el diseño con el
contenido: mejor evitarlos.)

#### Selectores
| Selector | Elige |
|---|---|
| `p` | todos los párrafos |
| `.precio` | los elementos con `class="precio"` (un elemento puede tener varias clases) |
| `#reservas` | el elemento con `id="reservas"` (único en la página) |
| `nav a` | los `a` que están **dentro** de un `nav` |
| `ul > li` | los `li` **hijos directos** de un `ul` |
| `li + li` | cada `li` que viene justo después de otro `li` |
| `a:hover` | un enlace mientras el mouse está encima |
| `tr:nth-child(even)` | las filas pares |
| `li:first-child` | el primer `li` de su lista |
| `h1, h2` | los dos |

#### La cascada: qué regla gana
Si dos reglas cambian lo mismo, gana la **más específica**: un id le gana a una clase y
una clase le gana a una etiqueta (`#menu a` > `.menu a` > `nav a`). Si empatan, gana la
**última** que aparece en el archivo. Algunas propiedades (el color, la letra) se
**heredan**: si ponés `color` en el `body`, todo el texto lo toma salvo que otra regla
diga lo contrario. Para ver qué regla ganó y cuáles quedaron tachadas: F12 → Elementos
→ Estilos.

#### Colores, variables y letras
```css
:root {                          /* variables: se definen una vez y se usan en todo el sitio */
    --mar: #0b3d5c;
    --arena: #f4e9d8;
    --faro: #e63946;
}
body {
    background-color: var(--arena);
    color: var(--mar);
    font-family: Georgia, 'Times New Roman', serif;   /* la primera que tenga la compu */
    font-size: 1rem;                                   /* 1rem = el tamaño base (16px) */
    line-height: 1.5;
}
a { color: var(--faro); }
a:hover { text-decoration: none; }
```
Los colores se escriben como `#0b3d5c` (hexadecimal), `rgb(11 61 92)` o por nombre
(`white`). Las **unidades**: `px` (fijos), `rem` (relativos al tamaño base: respetan si
el usuario agranda la letra), `%` (del contenedor) y `vw`/`vh` (de la pantalla).

#### El modelo de caja
Todo elemento es una **caja**: contenido, relleno (`padding`), borde (`border`) y
margen (`margin`, el espacio de afuera).
```
margin → border → padding → contenido
```
```css
.tarjeta {
    width: 280px;
    padding: 16px;
    border: 2px solid var(--mar);
    border-radius: 8px;            /* esquinas redondeadas */
    margin: 0 auto;                /* arriba/abajo 0, a los costados automático: centra */
    box-sizing: border-box;        /* el width INCLUYE padding y borde */
}
```
Sin `box-sizing: border-box`, esa tarjeta mediría 280 + 32 + 4 = **316 px**: por eso casi
todos los sitios empiezan con `*, *::before, *::after { box-sizing: border-box; }`.

`display` dice cómo se acomoda la caja: `block` (ocupa todo el ancho, uno abajo del
otro: `p`, `h1`, `div`), `inline` (en la línea del texto: `a`, `strong`; no toma
`width`), `inline-block` (en la línea, pero con ancho y alto) y `none` (no se ve).

### Código de ejemplo

La portada del bodegón, ahora con estilo: variables de color, letra, una cabecera
oscura, el menú y tarjetas con el modelo de caja.

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bodegón del Puerto</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <header class="cabecera">
        <h1>Bodegón del Puerto</h1>
        <nav>
            <a href="index.html" class="activo">Inicio</a>
            <a href="#pizarra">La pizarra</a>
        </nav>
    </header>
    <main>
        <section id="pizarra">
            <h2>Hoy en la pizarra</h2>
            <article class="tarjeta">
                <h3>Merluza a la romana</h3>
                <p class="precio">$ 9.500</p>
            </article>
            <article class="tarjeta destacada">
                <h3>Cazuela de mariscos</h3>
                <p class="precio">$ 14.750</p>
            </article>
        </section>
    </main>
</body>
</html>
```

`css/estilos.css`
```css
*, *::before, *::after {
    box-sizing: border-box;
}

:root {
    --mar: #0b3d5c;
    --arena: #f4e9d8;
    --faro: #e63946;
}

body {
    margin: 0;
    background-color: var(--arena);
    color: var(--mar);
    font-family: Georgia, 'Times New Roman', serif;
    line-height: 1.5;
}

.cabecera {
    background-color: var(--mar);
    color: white;
    padding: 16px 24px;
}

.cabecera h1 {
    margin: 0;
    font-size: 2rem;
}

nav a {
    color: white;
    margin-right: 16px;
}

nav a.activo {
    font-weight: bold;
    text-decoration: none;
    border-bottom: 3px solid var(--faro);
}

main {
    padding: 24px;
}

.tarjeta {
    width: 280px;
    padding: 16px;
    margin: 0 0 16px;
    background-color: white;
    border: 2px solid var(--mar);
    border-radius: 8px;
}

.tarjeta h3 {
    margin-top: 0;
}

.precio {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
}

.destacada {
    border-color: var(--faro);
}

.destacada .precio {
    color: var(--faro);
}
```

Abrilo, pasá el mouse por el menú y abrí F12 → Elementos → Estilos sobre una tarjeta:
vas a ver el dibujo del modelo de caja con sus medidas, y en la destacada, la regla
`border-color` que le ganó a la de `.tarjeta`.

### ¿Para qué sirve?

Con CSS una misma página puede verse como un diario, como una tienda o como una app. Las variables y las clases reutilizables hacen que un sitio entero cambie de color en una línea, y entender la cascada y el modelo de caja es lo que separa "pelearse con el CSS" de decidir cómo se ve cada cosa.

### Errores habituales

**Ogro: la regla que "no hace nada".** Otra regla más específica le gana. Mirala en F12
→ Estilos: aparece tachada. Subí la especificidad con una clase o revisá el orden.

**Esqueleto: el CSS que no carga.** La ruta del `<link>` está mal (se cuenta desde la
página, como las imágenes). En F12 → Red aparece en rojo.

**Troll: la caja más ancha de lo que dijiste.** Sin `box-sizing: border-box`, el
`padding` y el borde se **suman** al `width`.

**Slime: el punto y coma que falta.** `color: red font-size: 2rem;` anula las dos
propiedades. Cada declaración termina en `;`.

**Ogro: `.clase` con espacio.** `nav .activo` (un `.activo` dentro de `nav`) no es lo
mismo que `nav.activo` (un `nav` que tiene la clase `activo`).

**Goblin: `width` en un `a`.** Los elementos `inline` ignoran `width` y `height`: cambiá
el `display` a `inline-block` o `block`.

### Misión S04-N03-M1 · La tarjeta del barco

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá `index.html` y `css/estilos.css` con la **tarjeta del barco** Albatros (un
`<article class="tarjeta">` con un `<h1>`, una foto `img/albatros.svg`, un párrafo y un
`<p class="precio">` con el pasaje). Estilos:

- la tarjeta mide **exactamente 280 px de ancho** en total (con `padding` de 16 px y
  borde de 2 px), tiene las esquinas redondeadas (8 px) y está **centrada** en la página;
- la imagen ocupa todo el ancho de adentro de la tarjeta (`width: 100%`) y es `block`;
- el título es del color `#0b3d5c` y el precio mide `1.5rem`, en negrita.

Entregá la carpeta en un zip.

#### Criterio de aprobación

- La tarjeta mide 280 px de punta a punta (con `box-sizing: border-box`) y queda centrada.
- La imagen se adapta al ancho de la tarjeta.
- Los colores y tamaños salen del CSS, no de atributos `style`.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Albatros</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <main>
        <article class="tarjeta">
            <h1>Albatros</h1>
            <img src="img/albatros.svg" alt="El Albatros navegando">
            <p>Carguero de 32,5 m que cruza a Colonia todos los días.</p>
            <p class="precio">$ 18.000</p>
        </article>
    </main>
</body>
</html>
```

`css/estilos.css`
```css
*, *::before, *::after {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 24px 0;
    font-family: Georgia, serif;
}

.tarjeta {
    width: 280px;
    margin: 0 auto;
    padding: 16px;
    border: 2px solid #0b3d5c;
    border-radius: 8px;
}

.tarjeta h1 {
    margin-top: 0;
    font-size: 1.5rem;
    color: #0b3d5c;
}

.tarjeta img {
    display: block;
    width: 100%;
    height: auto;
}

.precio {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0;
}
```

`img/albatros.svg`
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 120" width="240" height="120">
  <rect width="240" height="120" fill="#a8dadc"/>
  <rect y="90" width="240" height="30" fill="#1d3557"/>
  <polygon points="30,80 210,80 190,100 50,100" fill="#f1faee" stroke="#1d3557" stroke-width="2"/>
  <rect x="90" y="55" width="60" height="25" fill="#e63946"/>
</svg>
```

### Misión S04-N03-M2 · Los colores del puerto

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Definí la **paleta del Puerto** como variables en `:root`: `--mar` (`#0b3d5c`),
`--arena` (`#f4e9d8`) y `--faro` (`#e63946`), y usala en `index.html` (una cabecera
con un menú de tres enlaces, dos párrafos con enlaces y un botón):

- el fondo de la página es arena y el texto, mar;
- la cabecera tiene fondo mar y texto blanco, y sus enlaces también son blancos;
- los enlaces del contenido son color faro y **pierden el subrayado al pasar el mouse**;
- el botón (`<a class="boton">`) es un `inline-block` con fondo faro, texto blanco,
  `padding` de 8 px arriba y abajo y 16 px a los costados, y bordes totalmente
  redondeados (`border-radius: 999px`).

Ningún color puede estar escrito fuera de `:root`. Entregá la carpeta en un zip.

#### Criterio de aprobación

- Los tres colores son variables y todas las reglas usan `var(...)`.
- Los enlaces de la cabecera y los del contenido tienen colores distintos (selectores por lugar).
- El `:hover` quita el subrayado y el botón tiene su caja completa.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Los colores del Puerto</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <header>
        <h1>Puerto de los Mensajeros</h1>
        <nav>
            <a href="#muelle">Muelle</a>
            <a href="#torre">Torre</a>
            <a href="#faro">Faro</a>
        </nav>
    </header>
    <main>
        <p id="muelle">Del <a href="#torre">muelle</a> salen los ferrys a Colonia.</p>
        <p id="torre">Desde la <a href="#faro">torre</a> se ve todo el puerto.</p>
        <p id="faro"><a href="#muelle" class="boton">Comprá tu pasaje</a></p>
    </main>
</body>
</html>
```

`css/estilos.css`
```css
:root {
    --mar: #0b3d5c;
    --arena: #f4e9d8;
    --faro: #e63946;
    --blanco: #ffffff;
}

body {
    margin: 0;
    background-color: var(--arena);
    color: var(--mar);
    font-family: Georgia, serif;
}

header {
    background-color: var(--mar);
    color: var(--blanco);
    padding: 16px;
}

header a {
    color: var(--blanco);
    margin-right: 12px;
}

main {
    padding: 16px;
}

main a {
    color: var(--faro);
}

main a:hover {
    text-decoration: none;
}

main a.boton {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 999px;
    background-color: var(--faro);
    color: var(--blanco);
    text-decoration: none;
}
```

### Misión S04-N03-M3 · El menú con estados

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá el menú de la Torre como una **lista** dentro de un `<nav class="menu">` (cinco
enlaces, el de la página actual con la clase `activo`) y dale estilo **solo con
selectores**, sin agregar más clases:

- la lista sin viñetas ni `padding`, y cada `li` en `inline-block`;
- entre un `li` y el siguiente, un separador: `border-left: 1px solid` y
  `padding-left: 12px` (el primero no tiene: usá `li + li`);
- los enlaces sin subrayado; al pasar el mouse, fondo `#f4e9d8`;
- el activo en negrita y con un borde inferior de 3 px color `#e63946`.

Entregá la carpeta en un zip.

#### Criterio de aprobación

- Los separadores salen de `li + li` (el primero no lo tiene).
- El estado activo y el `:hover` se ven como se pide.
- No hay clases agregadas en los `li` ni atributos `style`.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Menú de la Torre</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <nav class="menu">
        <ul>
            <li><a href="#" class="activo">Inicio</a></li>
            <li><a href="#">Horarios</a></li>
            <li><a href="#">Barcos</a></li>
            <li><a href="#">Tarifas</a></li>
            <li><a href="#">Contacto</a></li>
        </ul>
    </nav>
    <main>
        <h1>Torre del Puerto</h1>
    </main>
</body>
</html>
```

`css/estilos.css`
```css
.menu ul {
    list-style: none;
    margin: 0;
    padding: 0;
}

.menu li {
    display: inline-block;
}

.menu li + li {
    border-left: 1px solid #0b3d5c;
    padding-left: 12px;
    margin-left: 8px;
}

.menu a {
    color: #0b3d5c;
    text-decoration: none;
    padding: 4px 6px;
}

.menu a:hover {
    background-color: #f4e9d8;
}

.menu a.activo {
    font-weight: bold;
    border-bottom: 3px solid #e63946;
}
```

### Encargo S04-N03-E1 · La tabla con estilo

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Tomá la tabla de **horarios del ferry** (la de la misión S04-N02-M1 o una parecida,
con `caption`, `thead`, `tbody` y `tfoot`) y dale estilo en `css/estilos.css`:

- bordes simples entre celdas (`border-collapse: collapse` y `1px solid`);
- encabezados (`thead th`) con fondo `#0b3d5c` y texto blanco;
- filas **pares** del cuerpo con fondo `#f4e9d8` (`:nth-child(even)`);
- los números (una clase `numero` en esas celdas) alineados a la derecha;
- el `caption` en negrita y a la izquierda, y el `tfoot` en negrita;
- `padding` de 6 px arriba y abajo y 12 px a los costados en todas las celdas.

Entregá la carpeta en un zip.

#### Criterio de aprobación

- Las filas pares se pintan con `:nth-child(even)`, sin clases en cada fila.
- Los números quedan a la derecha y los encabezados con sus colores.
- La tabla tiene sus bordes simples.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Horarios del ferry</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <main>
        <h1>Horarios del ferry</h1>
        <table>
            <caption>Ferry a Colonia · sábado</caption>
            <thead>
                <tr><th scope="col">Salida</th><th scope="col">Barco</th><th scope="col">Lugares libres</th></tr>
            </thead>
            <tbody>
                <tr><th scope="row">08:30</th><td>Estrella del Sur</td><td class="numero">120</td></tr>
                <tr><th scope="row">13:00</th><td>Gaviota</td><td class="numero">45</td></tr>
                <tr><th scope="row">17:45</th><td colspan="2">Cancelado por viento</td></tr>
                <tr><th scope="row">21:00</th><td>Estrella del Sur</td><td class="numero">210</td></tr>
            </tbody>
            <tfoot>
                <tr><th scope="row" colspan="2">Total de lugares</th><td class="numero">375</td></tr>
            </tfoot>
        </table>
    </main>
</body>
</html>
```

`css/estilos.css`
```css
body {
    font-family: Georgia, serif;
    color: #0b3d5c;
}

table {
    border-collapse: collapse;
}

caption {
    font-weight: bold;
    text-align: left;
    padding-bottom: 8px;
}

th, td {
    border: 1px solid #0b3d5c;
    padding: 6px 12px;
    text-align: left;
}

thead th {
    background-color: #0b3d5c;
    color: #ffffff;
}

tbody tr:nth-child(even) {
    background-color: #f4e9d8;
}

.numero {
    text-align: right;
}

tfoot {
    font-weight: bold;
}
```

### Prueba del sello

#### Si `nav a { color: white; }` y `.activo { color: red; }`, ¿de qué color queda `<a class="activo">` dentro del `nav`?

Rojo: una clase es más específica que cualquier combinación de etiquetas, así que `.activo` le gana a `nav a` aunque aparezca antes en el archivo.

#### ¿Qué hace `box-sizing: border-box`?

Hace que el `width` incluya el `padding` y el borde, así la caja mide exactamente lo que dice.

#### ¿Para qué sirven las variables de CSS (`--mar`)?

Para definir un valor una sola vez (un color, un tamaño) y usarlo en todo el sitio con `var(--mar)`: se cambia en un lugar.

#### ¿Qué diferencia hay entre `margin` y `padding`?

El `padding` es el espacio de adentro, entre el contenido y el borde (toma el fondo); el `margin` es el espacio de afuera, entre la caja y las demás.

#### ¿Por qué conviene `rem` en lugar de `px` para el tamaño de la letra?

Porque `rem` es relativo al tamaño base del navegador: si el usuario agranda la letra, la página la respeta.

### Soluciones (docente)

Contenido nuevo. Se verifica en Chromium midiendo los **estilos computados** (colores, bordes, tamaños, `text-align`, el `:hover` pasando el mouse) y las **cajas reales** (la tarjeta mide 280 px y queda centrada). Para corregir, F12 → Elementos → Estilos muestra qué regla ganó y el dibujo del modelo de caja.

## S04-N04 · Flexbox, grid y diseño adaptable

```meta
tipo: tema
padre: S04-N03
precio: 10
criatura: troll
ejecutable: no
temas: css.flexbox, css.grid, css.responsive
```

### Crónica

Llega la temporada de cruceros y el Escaparate se llena de gente que mira las vidrieras… desde el celular. Las tiendas que se ven bien en la pantalla grande de la oficina se deforman en la mano de un turista: columnas aplastadas, textos cortados, botones que no se pueden tocar.

—Una vidriera tiene que acomodarse al que mira —dice {mentor}—. Para eso están **flexbox** y **grid**: le decís al navegador cómo repartir el espacio y él lo acomoda en cualquier pantalla. Y con las **consultas de medios**, {heroe}, cambiás el diseño cuando la pantalla es chica. Pensá primero en el celular.

### Objetivos

- Acomodar elementos en fila o en columna con flexbox.
- Armar grillas con CSS grid, incluidas las que se adaptan solas (`auto-fill`, `minmax`).
- Diseñar pensando primero en el celular y agrandar con `@media`.
- Evitar que la página se salga de la pantalla (imágenes y anchos flexibles).

### Antes de empezar

- El nodo anterior (CSS: selectores, colores y cajas).

### Explicación

#### Flexbox: una fila (o una columna) que se reparte
```css
.cabecera {
    display: flex;                   /* los hijos directos se ponen en fila */
    justify-content: space-between;  /* reparte a lo largo: uno a cada punta */
    align-items: center;             /* los centra en el alto */
    gap: 16px;                       /* espacio entre hijos */
    flex-wrap: wrap;                 /* si no entran, pasan a la línea de abajo */
}
.cabecera nav { display: flex; gap: 12px; }
```
| Propiedad | Valores útiles |
|---|---|
| `flex-direction` | `row` (fila, por defecto), `column` |
| `justify-content` | `flex-start`, `center`, `space-between`, `flex-end` |
| `align-items` | `stretch` (por defecto: todos del mismo alto), `center`, `flex-start` |
| `flex` (en un hijo) | `1` (toma el espacio que sobra); `1 1 220px` (crece, se achica, arranca en 220 px) |
| `order` (en un hijo) | cambia el orden visual sin tocar el HTML |

#### Grid: filas y columnas a la vez
```css
.grilla {
    display: grid;
    grid-template-columns: repeat(3, 1fr);          /* tres columnas iguales */
    gap: 16px;
}
.galeria {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));   /* entran las que entren */
}
```
`fr` es una **fracción** del espacio libre. Con `repeat(auto-fill, minmax(200px, 1fr))`
la grilla pone tantas columnas de al menos 200 px como entren, y las estira para llenar:
se adapta a cualquier pantalla **sin** `@media`.

Para diseñar una página entera, las **áreas** tienen nombre:
```css
.pagina {
    display: grid;
    grid-template-columns: 200px 1fr;
    grid-template-areas:
        "cabecera cabecera"
        "menu     contenido"
        "pie      pie";
}
header { grid-area: cabecera; }
nav    { grid-area: menu; }
```

#### Primero el celular
Más de la mitad de las visitas llegan desde un teléfono. Se escribe primero el diseño
**de una columna** (el del celular) y después, con una **consulta de medios**, se
agrega lo que cambia en pantallas más anchas:
```css
.pagina { display: grid; gap: 16px; }              /* celular: una columna */

@media (min-width: 768px) {                         /* tablet y compu */
    .pagina { grid-template-columns: 200px 1fr; }
}
```
Sin la etiqueta `<meta name="viewport" content="width=device-width, initial-scale=1">`
el celular simula una pantalla de compu y achica todo: no la olvides.

#### Que nada se salga
```css
img { max-width: 100%; height: auto; }    /* las imágenes nunca más anchas que su caja */
```
Evitá los anchos fijos grandes (`width: 900px`): usá `max-width` y porcentajes. Para
probar, F12 → el ícono del celular (vista de dispositivo) y elegí un ancho de 375 px.

### Código de ejemplo

La **cartelera de salidas** adaptable: la cabecera en fila (y en columna en el
celular) y una grilla de tarjetas que pone tantas columnas como entren.

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Cartelera de salidas</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <header class="cabecera">
        <h1>Salidas de hoy</h1>
        <nav>
            <a href="#">Ferry</a>
            <a href="#">Cruceros</a>
            <a href="#">Carga</a>
        </nav>
    </header>
    <main class="grilla">
        <article class="tarjeta"><h2>08:30</h2><p>Estrella del Sur → Colonia</p></article>
        <article class="tarjeta"><h2>10:15</h2><p>Gaviota → Montevideo</p></article>
        <article class="tarjeta"><h2>13:00</h2><p>Albatros → Piriápolis</p></article>
        <article class="tarjeta"><h2>17:45</h2><p>Tritón → Colonia</p></article>
        <article class="tarjeta"><h2>21:00</h2><p>Estrella del Sur → Colonia</p></article>
    </main>
</body>
</html>
```

`css/estilos.css`
```css
*, *::before, *::after {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Georgia, serif;
    color: #0b3d5c;
    background-color: #f4e9d8;
}

.cabecera {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 16px;
    background-color: #0b3d5c;
    color: white;
}

.cabecera h1 {
    margin: 0;
}

.cabecera nav {
    display: flex;
    gap: 12px;
}

.cabecera a {
    color: white;
}

.grilla {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 16px;
    padding: 16px;
}

.tarjeta {
    background-color: white;
    border-radius: 8px;
    padding: 12px 16px;
}

.tarjeta h2 {
    margin: 0;
}

@media (min-width: 700px) {
    .cabecera {
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
}
```

Achicá y agrandá la ventana (o usá la vista de dispositivo de F12): con 1000 px de ancho
entran cuatro tarjetas por fila; en un celular, una. La cabecera pasa de fila a columna
en 700 px.

### ¿Para qué sirve?

Casi todos los diseños que ves en la web (menús, galerías, tiendas, paneles de administración) están hechos con flexbox y grid. Diseñar primero para el celular hace que tu página se vea bien donde más se la va a mirar, y las grillas que se adaptan solas te ahorran escribir un diseño para cada pantalla.

### Errores habituales

**Troll: `display: flex` en el lugar equivocado.** Flexbox acomoda a los **hijos
directos** del elemento que lo tiene. Si lo ponés en el `<nav>`, se acomodan los
enlaces; no el `<nav>` junto al título.

**Troll: la página que se sale de la pantalla.** Un ancho fijo (`width: 900px`) o una
imagen sin `max-width: 100%` hacen aparecer la barra de desplazamiento horizontal en el
celular.

**Ogro: el `@media` al revés.** Si escribís el diseño de compu primero y "arreglás" el
celular con `max-width`, terminás pisando reglas. Primero el celular, después
`min-width`.

**Esqueleto: el celular que muestra todo chiquito.** Falta la etiqueta `<meta
name="viewport">`.

**Ogro: `auto-fill` sin `minmax`.** `repeat(auto-fill, 1fr)` no sabe cuánto mide cada
columna. Dale un mínimo: `minmax(200px, 1fr)`.

### Misión S04-N04-M1 · La barra de navegación

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá la **barra de navegación** del Puerto (`<header class="barra">` con un logo, una
lista de cuatro enlaces y un botón `Comprar pasaje`). Con flexbox:

- en el **celular** (menos de 700 px), todo en **columna**: el logo arriba, los enlaces
  en una fila debajo (que pasan de línea si no entran) y el botón al final;
- desde **700 px**, todo en **una fila**: el logo a la izquierda, el botón a la
  derecha, los enlaces en el medio, todo centrado en el alto.

La página no se puede salir de la pantalla en 375 px. Entregá la carpeta en un zip.

#### Criterio de aprobación

- Flexbox en la barra y en la lista, con `gap`.
- Un `@media (min-width: 700px)` cambia de columna a fila.
- En 375 px no hay desplazamiento horizontal.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Puerto de los Mensajeros</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <header class="barra">
        <a href="#" class="logo">⚓ Puerto</a>
        <nav>
            <ul>
                <li><a href="#">Ferry</a></li>
                <li><a href="#">Cruceros</a></li>
                <li><a href="#">Bodegón</a></li>
                <li><a href="#">Torre</a></li>
            </ul>
        </nav>
        <a href="#" class="boton">Comprar pasaje</a>
    </header>
    <main>
        <h1>Bienvenidos al Puerto</h1>
    </main>
</body>
</html>
```

`css/estilos.css`
```css
*, *::before, *::after {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Georgia, serif;
}

.barra {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 12px 16px;
    background-color: #0b3d5c;
}

.barra a {
    color: white;
    text-decoration: none;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
}

.barra ul {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    list-style: none;
    margin: 0;
    padding: 0;
}

.barra .boton {
    align-self: flex-start;
    padding: 8px 16px;
    border-radius: 999px;
    background-color: #e63946;
}

main {
    padding: 16px;
}

@media (min-width: 700px) {
    .barra {
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }

    .barra .boton {
        align-self: center;
    }
}
```

### Misión S04-N04-M2 · La galería de barcos

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá una **galería** de ocho barcos (`<figure>` con una imagen SVG, la misma para todos
alcanza, y su `figcaption`) dentro de `<main class="galeria">`. Con **grid**, sin
ningún `@media`:

- columnas de **al menos 150 px** que se estiran para llenar el ancho
  (`auto-fill` y `minmax`), con `gap` de 12 px y 16 px de `padding` en la galería;
- las imágenes ocupan el ancho de su figura (`width: 100%`) y son cuadradas
  (`aspect-ratio: 1`);
- el texto de cada figura, centrado.

Con esos números, en una pantalla de 1000 px entran 6 por fila y en un celular de
375 px, 2. Entregá la carpeta en un zip.

#### Criterio de aprobación

- La grilla se adapta sola (con `repeat(auto-fill, minmax(150px, 1fr))`), sin `@media`.
- Las imágenes son cuadradas y del ancho de su figura.
- No hay desplazamiento horizontal en 375 px.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Galería de barcos</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <h1>Barcos del Puerto</h1>
    <main class="galeria">
        <figure><img src="img/barco.svg" alt="Albatros"><figcaption>Albatros</figcaption></figure>
        <figure><img src="img/barco.svg" alt="Gaviota"><figcaption>Gaviota</figcaption></figure>
        <figure><img src="img/barco.svg" alt="Estrella del Sur"><figcaption>Estrella del Sur</figcaption></figure>
        <figure><img src="img/barco.svg" alt="Tritón"><figcaption>Tritón</figcaption></figure>
        <figure><img src="img/barco.svg" alt="Tortuga"><figcaption>Tortuga</figcaption></figure>
        <figure><img src="img/barco.svg" alt="Gavilán"><figcaption>Gavilán</figcaption></figure>
        <figure><img src="img/barco.svg" alt="Petrel"><figcaption>Petrel</figcaption></figure>
        <figure><img src="img/barco.svg" alt="Delfín"><figcaption>Delfín</figcaption></figure>
    </main>
</body>
</html>
```

`css/estilos.css`
```css
*, *::before, *::after {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Georgia, serif;
}

h1 {
    margin: 16px;
}

.galeria {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 12px;
    padding: 16px;
}

.galeria figure {
    margin: 0;
    text-align: center;
}

.galeria img {
    display: block;
    width: 100%;
    aspect-ratio: 1;
    object-fit: cover;
    border-radius: 8px;
}
```

`img/barco.svg`
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect width="100" height="100" fill="#a8dadc"/>
  <rect y="70" width="100" height="30" fill="#1d3557"/>
  <polygon points="15,62 85,62 75,78 25,78" fill="#f1faee" stroke="#1d3557" stroke-width="2"/>
  <polygon points="50,20 50,60 75,60" fill="#e63946"/>
</svg>
```

### Misión S04-N04-M3 · La página con áreas

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá el diseño de la **página de la Torre** con **áreas de grid** en un
`<div class="pagina">` que contiene `<header>`, `<nav>`, `<main>`, `<aside>` y
`<footer>`:

- en el **celular**, una sola columna en este orden: cabecera, menú, contenido, aside,
  pie;
- desde **768 px**: tres columnas (`200px 1fr 220px`), la cabecera y el pie ocupan las
  tres, y en el medio van el menú a la izquierda, el contenido al centro y el aside a la
  derecha, **a la misma altura**.

Usá `grid-template-areas` con nombres en las dos versiones. Entregá la carpeta en un zip.

#### Criterio de aprobación

- Las áreas tienen nombre (`grid-area`) y el `@media` solo cambia las columnas y las áreas.
- En 768 px o más, menú, contenido y aside quedan lado a lado; en el celular, uno debajo del otro.
- No hay desplazamiento horizontal en 375 px.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La Torre del Puerto</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <div class="pagina">
        <header><h1>La Torre del Puerto</h1></header>
        <nav>
            <ul>
                <li><a href="#">Historia</a></li>
                <li><a href="#">Visitas</a></li>
                <li><a href="#">Contacto</a></li>
            </ul>
        </nav>
        <main>
            <h2>214 escalones</h2>
            <p>Desde arriba se ven los tres muelles, el faro y, en días claros, la costa de enfrente.</p>
        </main>
        <aside>
            <h2>Horarios</h2>
            <p>Martes a domingo, de 9 a 18.</p>
        </aside>
        <footer><p>Torre del Puerto · 1890</p></footer>
    </div>
</body>
</html>
```

`css/estilos.css`
```css
*, *::before, *::after {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Georgia, serif;
    color: #0b3d5c;
}

.pagina {
    display: grid;
    gap: 12px;
    padding: 12px;
    grid-template-areas:
        "cabecera"
        "menu"
        "contenido"
        "costado"
        "pie";
}

.pagina > * {
    padding: 12px;
    border-radius: 8px;
    background-color: #f4e9d8;
}

header { grid-area: cabecera; }
nav { grid-area: menu; }
main { grid-area: contenido; }
aside { grid-area: costado; }
footer { grid-area: pie; }

header h1, footer p {
    margin: 0;
}

@media (min-width: 768px) {
    .pagina {
        grid-template-columns: 200px 1fr 220px;
        grid-template-areas:
            "cabecera cabecera cabecera"
            "menu     contenido costado"
            "pie      pie       pie";
    }
}
```

### Encargo S04-N04-E1 · Las tarjetas de precios

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Armá las **tarifas del ferry** con tres tarjetas (`Ida`, `Ida y vuelta` y `Abono
mensual`) en un `<section class="planes">`, con flexbox:

- en pantallas anchas, las tres **en fila**, del **mismo alto** aunque tengan distinta
  cantidad de texto, y cada una con `flex: 1 1 220px`;
- la del medio (`class="plan destacado"`) tiene un borde de 3 px color `#e63946` y la
  etiqueta `Más elegida` (las otras, un borde del **mismo grosor** en un color suave:
  si no, los botones quedan desparejos por 2 px);
- en el **celular**, una debajo de otra y la **destacada primero** (con `order`, sin
  cambiar el HTML);
- el botón de cada tarjeta queda **siempre abajo**, aunque el texto sea corto (la
  tarjeta también es flex en columna, y el botón usa `margin-top: auto`).

Entregá la carpeta en un zip.

#### Criterio de aprobación

- Las tarjetas son del mismo alto en fila y sus botones quedan alineados abajo.
- En el celular la destacada aparece primero, con `order`.
- No hay desplazamiento horizontal en 375 px.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Tarifas del ferry</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <h1>Tarifas del ferry a Colonia</h1>
    <section class="planes">
        <article class="plan">
            <h2>Ida</h2>
            <p class="precio">$ 18.000</p>
            <p>Un viaje.</p>
            <a href="#" class="boton">Comprar</a>
        </article>
        <article class="plan destacado">
            <p class="etiqueta">Más elegida</p>
            <h2>Ida y vuelta</h2>
            <p class="precio">$ 32.000</p>
            <p>Dos viajes, con la vuelta abierta hasta 30 días. Incluye el café a bordo y prioridad para embarcar el auto.</p>
            <a href="#" class="boton">Comprar</a>
        </article>
        <article class="plan">
            <h2>Abono mensual</h2>
            <p class="precio">$ 190.000</p>
            <p>Viajes ilimitados durante 30 días.</p>
            <a href="#" class="boton">Comprar</a>
        </article>
    </section>
</body>
</html>
```

`css/estilos.css`
```css
*, *::before, *::after {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 16px;
    font-family: Georgia, serif;
    color: #0b3d5c;
}

.planes {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.plan {
    display: flex;
    flex-direction: column;
    flex: 1 1 220px;
    padding: 16px;
    border: 3px solid #d9d2c3;
    border-radius: 8px;
}

.plan h2 {
    margin: 0;
}

.destacado {
    order: -1;
    border-color: #e63946;
}

.etiqueta {
    margin: 0;
    color: #e63946;
    font-weight: bold;
}

.precio {
    font-size: 1.5rem;
    font-weight: bold;
}

.boton {
    margin-top: auto;
    padding: 8px 16px;
    border-radius: 999px;
    background-color: #0b3d5c;
    color: white;
    text-align: center;
    text-decoration: none;
}

@media (min-width: 768px) {
    .planes {
        flex-direction: row;
    }

    .destacado {
        order: 0;
    }
}
```

### Prueba del sello

#### ¿A qué elementos acomoda `display: flex`?

A los hijos directos del elemento que lo tiene.

#### ¿Qué hace `grid-template-columns: repeat(auto-fill, minmax(200px, 1fr))`?

Pone tantas columnas de al menos 200 px como entren en el ancho disponible y las estira para llenarlo: la grilla se adapta sola.

#### ¿Qué significa "primero el celular"?

Escribir el diseño de una columna como base y agregar con `@media (min-width: …)` lo que cambia en pantallas más anchas.

#### ¿Para qué sirve `<meta name="viewport" content="width=device-width, initial-scale=1">`?

Para que el celular use su ancho real y no simule una pantalla de compu achicando todo.

#### ¿Cómo se manda el botón de una tarjeta al fondo aunque el texto sea corto?

Haciendo la tarjeta flex en columna y dándole al botón `margin-top: auto`, que toma todo el espacio libre de arriba.

### Soluciones (docente)

Contenido nuevo. Se verifica en Chromium con dos anchos de pantalla (375 px y 1000–1200 px): se miden las posiciones reales de cada caja (cuántas tarjetas entran por fila, qué queda al lado o debajo de qué, alturas iguales, el orden en el celular) y que no aparezca desplazamiento horizontal. Para corregir, F12 → vista de dispositivo, y achicar y agrandar la ventana.

## S04-N05 · Jefe del Escaparate: el Hipocampo de las Vidrieras

```meta
tipo: jefe
padre: S04-N04
precio: 10
criatura: dragon
ejecutable: no
insignia: Vidrierista del Puerto
insignia_descripcion: Venciste al Hipocampo de las Vidrieras: armaste sitios completos con HTML y CSS que se ven bien en cualquier pantalla.
usa: html.semantica, css.responsive, html.formularios
```

### Crónica

Una mañana, todas las vidrieras del Escaparate amanecen revueltas: letreros al revés, precios que se salen del vidrio, puertas que no llevan a ningún lado. En el reflejo de los vidrios se mueve el **Hipocampo de las Vidrieras**, un caballito de mar del tamaño de un bote, que se alimenta de las páginas desordenadas.

—Tiene una sola debilidad —dice {mentor}—: las páginas que están bien de punta a punta. Estructura con significado, un solo estilo para todo el sitio, enlaces que andan, formularios con sus etiquetas y un diseño que se acomoda al celular. Armá una vidriera así, {heroe}, y el Hipocampo se va a buscar comida a otro puerto.

### Objetivos

- Construir sitios completos de varias páginas con HTML semántico y una sola hoja de estilos.
- Combinar flexbox, grid, tablas y formularios en un diseño adaptable.
- Revisar un sitio como lo haría un cliente: enlaces, imágenes, celular y compu.

### Antes de empezar

- Toda la Senda del Escaparate.

### Explicación

#### Antes de escribir: el plano del sitio
Anotá las páginas y qué va en cada una, las partes que se repiten (cabecera, menú,
pie) y los colores y letras en variables. Así el CSS se escribe una vez y todas las
páginas lo comparten.

#### La lista del cliente
Antes de entregar, recorré el sitio como un cliente exigente:
- cada página tiene su `<title>`, un solo `<h1>` y `lang="es"`;
- todos los enlaces llevan a algún lado y todas las imágenes cargan y tienen `alt`;
- el menú marca la página actual;
- en 375 px (F12 → vista de dispositivo) no hay desplazamiento horizontal ni textos
  cortados, y en una pantalla grande el contenido no queda estirado de punta a punta
  (`max-width` y `margin: 0 auto`);
- los formularios tienen cada campo con su `label` y sus límites.

Cuando lleguen PHP y la Oficina de Correos, estas mismas páginas se van a convertir en
plantillas: la cabecera y el pie en un `include`, y la carta saliendo de la base de
datos.

### Misión S04-N05-M1 · El sitio del bodegón

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 40
```

#### Consigna

Armá el sitio completo del **Bodegón del Puerto**: `index.html`, `carta.html`,
`reservas.html`, **una sola** hoja `css/estilos.css` y el logo `img/logo.svg`.

- **Todas las páginas**: la misma cabecera (logo y nombre a la izquierda, menú a la
  derecha desde 768 px; uno debajo del otro en el celular), el enlace de la página
  actual con la clase `activo` (en negrita y con borde inferior color faro), el mismo
  pie, el contenido con un ancho máximo de 960 px centrado, y colores en variables.
- **Inicio**: una presentación con el `<h1>`, un párrafo y un botón a `reservas.html`;
  y **Destacados**, una grilla de tres tarjetas (plato, descripción, precio) que se
  adapta sola (`auto-fill` y `minmax(220px, 1fr)`).
- **La carta**: una tabla con `caption`, `thead` con fondo mar y texto blanco, filas
  pares pintadas, precios alineados a la derecha.
- **Reservas**: un formulario (`get` a `index.html`) con nombre, personas (1 a 12),
  día, turno (radios en un `fieldset`) y notas; cada campo con su `label`; los campos
  de texto ocupan todo el ancho disponible hasta 400 px.

Nada de atributos `style`. Entregá la carpeta en un zip.

#### Criterio de aprobación

- Las tres páginas comparten la hoja de estilos, la cabecera, el menú (con el activo correcto) y el pie.
- Sin enlaces ni imágenes rotas, un `<h1>` por página, y ningún desplazamiento horizontal en 375 px.
- La grilla, la tabla y el formulario cumplen lo pedido.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bodegón del Puerto</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <header class="cabecera">
        <a href="index.html" class="marca"><img src="img/logo.svg" alt="" width="40" height="40"> Bodegón del Puerto</a>
        <nav>
            <a href="index.html" class="activo">Inicio</a>
            <a href="carta.html">La carta</a>
            <a href="reservas.html">Reservas</a>
        </nav>
    </header>
    <main class="contenido">
        <section class="presentacion">
            <h1>Pescado fresco frente al muelle</h1>
            <p>Desde 1952, la merluza de la madrugada llega a tu mesa al mediodía.</p>
            <a href="reservas.html" class="boton">Reservá tu mesa</a>
        </section>
        <section>
            <h2>Destacados</h2>
            <div class="grilla">
                <article class="tarjeta">
                    <h3>Merluza a la romana</h3>
                    <p>Con papas fritas y limón.</p>
                    <p class="precio">$ 9.500</p>
                </article>
                <article class="tarjeta">
                    <h3>Cazuela de mariscos</h3>
                    <p>Para compartir, los jueves.</p>
                    <p class="precio">$ 14.750</p>
                </article>
                <article class="tarjeta">
                    <h3>Flan casero</h3>
                    <p>Con dulce de leche o crema.</p>
                    <p class="precio">$ 3.100</p>
                </article>
            </div>
        </section>
    </main>
    <footer class="pie">
        <p>Muelle 3 · martes a domingo de 12 a 23</p>
    </footer>
</body>
</html>
```

`carta.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La carta · Bodegón del Puerto</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <header class="cabecera">
        <a href="index.html" class="marca"><img src="img/logo.svg" alt="" width="40" height="40"> Bodegón del Puerto</a>
        <nav>
            <a href="index.html">Inicio</a>
            <a href="carta.html" class="activo">La carta</a>
            <a href="reservas.html">Reservas</a>
        </nav>
    </header>
    <main class="contenido">
        <h1>La carta</h1>
        <table>
            <caption>Precios con IVA incluido</caption>
            <thead>
                <tr><th scope="col">Plato</th><th scope="col">Precio</th></tr>
            </thead>
            <tbody>
                <tr><td>Rabas</td><td class="numero">$ 5.200</td></tr>
                <tr><td>Empanadas de pescado</td><td class="numero">$ 3.800</td></tr>
                <tr><td>Merluza a la romana</td><td class="numero">$ 9.500</td></tr>
                <tr><td>Cazuela de mariscos</td><td class="numero">$ 14.750</td></tr>
                <tr><td>Flan casero</td><td class="numero">$ 3.100</td></tr>
            </tbody>
        </table>
    </main>
    <footer class="pie">
        <p>Muelle 3 · martes a domingo de 12 a 23</p>
    </footer>
</body>
</html>
```

`reservas.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Reservas · Bodegón del Puerto</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <header class="cabecera">
        <a href="index.html" class="marca"><img src="img/logo.svg" alt="" width="40" height="40"> Bodegón del Puerto</a>
        <nav>
            <a href="index.html">Inicio</a>
            <a href="carta.html">La carta</a>
            <a href="reservas.html" class="activo">Reservas</a>
        </nav>
    </header>
    <main class="contenido">
        <h1>Reservá tu mesa</h1>
        <form class="formulario" action="index.html" method="get">
            <label for="nombre">Nombre</label>
            <input id="nombre" name="nombre" required maxlength="40">

            <label for="personas">Personas</label>
            <input id="personas" name="personas" type="number" min="1" max="12" value="2" required>

            <label for="dia">Día</label>
            <input id="dia" name="dia" type="date" required>

            <fieldset>
                <legend>Turno</legend>
                <label><input type="radio" name="turno" value="mediodia" checked> Mediodía</label>
                <label><input type="radio" name="turno" value="noche"> Noche</label>
            </fieldset>

            <label for="notas">Notas</label>
            <textarea id="notas" name="notas" rows="3" maxlength="300"></textarea>

            <button type="submit" class="boton">Reservar</button>
        </form>
    </main>
    <footer class="pie">
        <p>Muelle 3 · martes a domingo de 12 a 23</p>
    </footer>
</body>
</html>
```

`css/estilos.css`
```css
*, *::before, *::after {
    box-sizing: border-box;
}

:root {
    --mar: #0b3d5c;
    --arena: #f4e9d8;
    --faro: #e63946;
    --blanco: #ffffff;
}

body {
    margin: 0;
    background-color: var(--arena);
    color: var(--mar);
    font-family: Georgia, 'Times New Roman', serif;
    line-height: 1.5;
}

img {
    max-width: 100%;
    height: auto;
}

.cabecera {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 12px 16px;
    background-color: var(--mar);
}

.cabecera a {
    color: var(--blanco);
    text-decoration: none;
}

.marca {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 1.25rem;
    font-weight: bold;
}

.cabecera nav {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
}

.cabecera nav a.activo {
    font-weight: bold;
    border-bottom: 3px solid var(--faro);
}

.contenido {
    max-width: 960px;
    margin: 0 auto;
    padding: 16px;
}

.presentacion {
    padding: 24px 0;
}

.boton {
    display: inline-block;
    padding: 8px 16px;
    border: 0;
    border-radius: 999px;
    background-color: var(--faro);
    color: var(--blanco);
    font: inherit;
    text-decoration: none;
    cursor: pointer;
}

.grilla {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 16px;
}

.tarjeta {
    padding: 16px;
    border-radius: 8px;
    background-color: var(--blanco);
}

.tarjeta h3 {
    margin-top: 0;
}

.precio {
    font-size: 1.25rem;
    font-weight: bold;
    color: var(--faro);
    margin-bottom: 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    background-color: var(--blanco);
}

caption {
    text-align: left;
    font-weight: bold;
    padding-bottom: 8px;
}

th, td {
    padding: 6px 12px;
    border-bottom: 1px solid var(--arena);
    text-align: left;
}

thead th {
    background-color: var(--mar);
    color: var(--blanco);
}

tbody tr:nth-child(even) {
    background-color: var(--arena);
}

.numero {
    text-align: right;
}

.formulario {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.formulario input:not([type=radio]),
.formulario textarea {
    width: 100%;
    max-width: 400px;
    padding: 6px;
    font: inherit;
}

.formulario fieldset {
    max-width: 400px;
}

.formulario .boton {
    align-self: flex-start;
    margin-top: 8px;
}

.pie {
    padding: 16px;
    text-align: center;
    background-color: var(--mar);
    color: var(--blanco);
}

@media (min-width: 768px) {
    .cabecera {
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
}
```

`img/logo.svg`
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="32" r="30" fill="#e63946"/>
  <circle cx="32" cy="16" r="5" fill="none" stroke="#ffffff" stroke-width="3"/>
  <line x1="32" y1="21" x2="32" y2="52" stroke="#ffffff" stroke-width="3"/>
  <line x1="22" y1="30" x2="42" y2="30" stroke="#ffffff" stroke-width="3"/>
  <path d="M14 40 Q32 62 50 40" fill="none" stroke="#ffffff" stroke-width="3"/>
</svg>
```

### Misión S04-N05-M2 · La página de la regata

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 40
```

#### Consigna

Armá la **página de la Regata del Puerto** (`index.html` y `css/estilos.css`), una
sola página larga con un menú que lleva a cada sección:

- una **cabecera** con el nombre y un menú de anclas (`#categorias`, `#cronograma`,
  `#inscripcion`) que, desde 768 px, va en fila a la derecha;
- una **portada** (`section class="portada"`) de ancho completo con fondo mar, el
  `<h1>`, la fecha en un `<time datetime="2026-11-14">` y un botón a `#inscripcion`;
- **Categorías** (`id="categorias"`): tres tarjetas (vela, remo, motor) en una grilla de
  **tres columnas iguales desde 768 px** y una columna en el celular, las tres del mismo
  alto;
- **Cronograma** (`id="cronograma"`): una tabla con hora y actividad (con `caption` y
  encabezados), que en el celular no se salga de la pantalla;
- **Inscripción** (`id="inscripcion"`): el formulario (barco, correo, categoría y la
  casilla del reglamento), cada campo con su `label` y obligatorio;
- un **pie** con un enlace externo seguro.

El contenido de las secciones no pasa de 1000 px de ancho, centrado. Entregá la carpeta
en un zip.

#### Criterio de aprobación

- Cada ancla del menú lleva a una sección que existe.
- Las tarjetas son tres por fila (del mismo alto) desde 768 px y una en el celular.
- Nada se sale de la pantalla en 375 px y el formulario tiene todas sus etiquetas.

#### Solución de referencia

`index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Regata del Puerto 2026</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <header class="cabecera">
        <strong>Regata del Puerto</strong>
        <nav>
            <a href="#categorias">Categorías</a>
            <a href="#cronograma">Cronograma</a>
            <a href="#inscripcion">Inscripción</a>
        </nav>
    </header>

    <section class="portada">
        <div class="ancho">
            <h1>Regata del Puerto 2026</h1>
            <p>Sábado <time datetime="2026-11-14">14 de noviembre</time>, largada frente a la Torre.</p>
            <a href="#inscripcion" class="boton">Inscribí tu barco</a>
        </div>
    </section>

    <main>
        <section id="categorias" class="ancho">
            <h2>Categorías</h2>
            <div class="tarjetas">
                <article class="tarjeta">
                    <h3>Vela</h3>
                    <p>Veleros de hasta 12 metros. Recorrido de 8 millas alrededor de la boya del faro.</p>
                </article>
                <article class="tarjeta">
                    <h3>Remo</h3>
                    <p>Botes de dos a ocho remeros.</p>
                </article>
                <article class="tarjeta">
                    <h3>Motor</h3>
                    <p>Lanchas de hasta 40 caballos, con control de velocidad en la bahía.</p>
                </article>
            </div>
        </section>

        <section id="cronograma" class="ancho">
            <h2>Cronograma</h2>
            <div class="tabla">
                <table>
                    <caption>Sábado 14 de noviembre</caption>
                    <thead>
                        <tr><th scope="col">Hora</th><th scope="col">Actividad</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>08:00</td><td>Acreditación en el muelle 2</td></tr>
                        <tr><td>10:00</td><td>Largada de vela</td></tr>
                        <tr><td>11:30</td><td>Largada de remo</td></tr>
                        <tr><td>14:00</td><td>Largada de motor</td></tr>
                        <tr><td>18:00</td><td>Premiación en el Bodegón del Puerto</td></tr>
                    </tbody>
                </table>
            </div>
        </section>

        <section id="inscripcion" class="ancho">
            <h2>Inscripción</h2>
            <form class="formulario" action="index.html" method="get">
                <label for="barco">Nombre del barco</label>
                <input id="barco" name="barco" required maxlength="30">
                <label for="email">Correo</label>
                <input id="email" name="email" type="email" required>
                <label for="categoria">Categoría</label>
                <select id="categoria" name="categoria" required>
                    <option value="">Elegí…</option>
                    <option value="vela">Vela</option>
                    <option value="remo">Remo</option>
                    <option value="motor">Motor</option>
                </select>
                <p>
                    <input id="reglamento" name="reglamento" type="checkbox" value="si" required>
                    <label for="reglamento">Leí el reglamento</label>
                </p>
                <button type="submit" class="boton">Inscribirme</button>
            </form>
        </section>
    </main>

    <footer class="pie">
        <p>Organiza la Torre del Puerto · <a href="https://es.wikipedia.org/wiki/Regata" target="_blank" rel="noopener">¿Qué es una regata?</a></p>
    </footer>
</body>
</html>
```

`css/estilos.css`
```css
*, *::before, *::after {
    box-sizing: border-box;
}

:root {
    --mar: #0b3d5c;
    --arena: #f4e9d8;
    --faro: #e63946;
    --blanco: #ffffff;
}

html {
    scroll-behavior: smooth;
}

body {
    margin: 0;
    font-family: Georgia, 'Times New Roman', serif;
    color: var(--mar);
    background-color: var(--arena);
    line-height: 1.5;
}

.ancho {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 16px;
}

.cabecera {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 12px 16px;
    background-color: var(--blanco);
}

.cabecera nav {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
}

.cabecera a {
    color: var(--mar);
}

.portada {
    padding: 48px 0;
    background-color: var(--mar);
    color: var(--blanco);
}

.portada h1 {
    margin-top: 0;
    font-size: 2.25rem;
    line-height: 1.2;
}

.boton {
    display: inline-block;
    padding: 10px 20px;
    border: 0;
    border-radius: 999px;
    background-color: var(--faro);
    color: var(--blanco);
    font: inherit;
    text-decoration: none;
    cursor: pointer;
}

.tarjetas {
    display: grid;
    gap: 16px;
}

.tarjeta {
    padding: 16px;
    border-radius: 8px;
    background-color: var(--blanco);
}

.tarjeta h3 {
    margin-top: 0;
}

.tabla {
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    background-color: var(--blanco);
}

caption {
    text-align: left;
    font-weight: bold;
    padding-bottom: 8px;
}

th, td {
    padding: 6px 12px;
    text-align: left;
    border-bottom: 1px solid var(--arena);
}

thead th {
    background-color: var(--mar);
    color: var(--blanco);
}

.formulario {
    display: flex;
    flex-direction: column;
    gap: 6px;
    max-width: 400px;
}

.formulario input:not([type=checkbox]),
.formulario select {
    width: 100%;
    padding: 6px;
    font: inherit;
}

.formulario .boton {
    align-self: flex-start;
}

.pie {
    margin-top: 32px;
    padding: 16px;
    text-align: center;
    background-color: var(--mar);
    color: var(--blanco);
}

.pie a {
    color: var(--blanco);
}

@media (min-width: 768px) {
    .cabecera {
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }

    .tarjetas {
        grid-template-columns: repeat(3, 1fr);
    }
}
```

### Prueba del sello

#### ¿Por qué conviene una sola hoja de estilos para todo el sitio?

Porque el diseño se escribe una vez y todas las páginas lo comparten: un cambio (un color, una letra) se hace en un solo lugar.

#### ¿Cómo se consigue que el contenido no quede estirado en una pantalla muy ancha?

Con un ancho máximo (`max-width`) y `margin: 0 auto`, que lo centra.

#### ¿Qué hace un enlace con `href="#cronograma"`?

Lleva a la parte de la misma página que tiene `id="cronograma"`.

#### ¿Cómo se evita que una tabla ancha rompa la página en el celular?

Envolviéndola en una caja con `overflow-x: auto`: la tabla se desplaza sola, sin que se desplace toda la página.

#### ¿Qué partes de estas páginas se convertirían en un `include` de PHP?

Las que se repiten en todas: la cabecera con el menú y el pie.

### Soluciones (docente)

Contenido nuevo. Las dos soluciones se verifican en Chromium en 375 px y en 1000–1200 px: cada página con su `<h1>`, `lang`, enlaces e imágenes sanos; el menú con el activo correcto en cada página; la cabecera en fila o en columna según el ancho; la grilla y las tarjetas (cuántas por fila y del mismo alto); la tabla con sus colores; el formulario con todas sus etiquetas y su validación; las anclas que llevan a secciones que existen; y ningún desplazamiento horizontal.
