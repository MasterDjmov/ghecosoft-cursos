# CURSO

```meta
slug: html
titulo: HTML y CSS: Los Talleres de los Vitrales
lenguaje: html
nivel: desde_cero
descripcion_corta: HTML, CSS y Tailwind desde cero: páginas que se ven bien en el celular y en la compu.
precio_raiz: 10
dias_abono: 30
destacado: no
proximamente: si
publicado: no
```

### Descripción

Aprendé a armar **páginas web desde cero**: primero la estructura con **HTML**, después el diseño a mano con **CSS** y al final la herramienta profesional, **Tailwind CSS**. No hace falta saber programar ni instalar nada para empezar: escribís en la plataforma y **ves tu página dibujada al lado**, en tamaño celular y en tamaño compu.

Todo se piensa **primero para el celular** (*mobile first*): si se ve bien en la pantalla chica, después se agranda. El curso termina con un proyecto grande: **reproducir esta misma plataforma, GhecoSoft-Code**, con su cabecera, su portal de acceso, la grilla de cursos y el Hall of Fame.

En los Talleres de los Vitrales las páginas son **vitrales**: primero se arma el **plomo** (HTML, la estructura), después se eligen los **vidrios de colores** (CSS) y al final llegan las **plantillas del gremio** (Tailwind) para trabajar rápido. Cada tema es un **nodo** del árbol: leés la explicación, probás el ejemplo y resolvés las **misiones**; al aprobarlas ganás cristales para abrir el siguiente. Cada rama termina con un **jefe**.

> Qué hace falta: un navegador (Chrome o Firefox) y la plataforma. Para practicar fuera de la plataforma, un editor como **VS Code**; desde la rama de Tailwind, si querés compilar en tu compu, **Node.js 20 o más nuevo**.

### Temario

- La estructura de una página: etiquetas, textos, enlaces, imágenes y listas
- HTML semántico y accesible, formularios con validación del navegador y tablas
- CSS: selectores, cascada, especificidad, variables y el modelo de caja
- Flexbox, Grid y diseño adaptable: celular primero, `@media`, `sticky` y `clamp()`
- Tailwind CSS: utilidades, flex y grid, prefijos de pantalla, estados y transiciones
- Tema propio, componentes reutilizables y una guía de estilo
- Proyecto: la plataforma GhecoSoft-Code completa, en celular y en compu

# DICCIONARIO

| clave | singular | plural | género | descripción | historia | ámbito |
|---|---|---|---|---|---|---|
| coin.course | cristal | cristales | m | La moneda de los Talleres: un vidrio de color tallado, listo para su vitral. Se gana aprobando misiones obligatorias y abre los nodos del curso. | | curso |
| mentor.name | Tesela | | f | La Vitralista: maestra de los Talleres de los Vitrales, por los que se asoma todo el mundo. | Tesela aprendió a fundir el plomo en las Forjas de Hierro, con Maese Ferrum, junto a otro aprendiz que soñaba con engranajes: Tesla. Cuando terminaron, Tesla subió a la montaña a fundar la Ciudadela de los Artífices y Tesela eligió el vidrio. Hoy sus vitrales están en las catedrales del Imperio, en las ventanas del Valle y en cada mensaje que despacha el Puerto. Lleva un monóculo de cristal tallado y una sola regla: **todo vitral empieza chico; si se ve bien en la ventana de una cabaña, después se agranda al ventanal del castillo**. | curso |
| world.region | Talleres de los Vitrales | | m | La región del mundo donde se fabrican los vitrales: las páginas web. Su lengua es HTML, con CSS para los colores. | | curso |
| story.course_intro | Bienvenida a los Talleres | | f | | El portal te deja en un balcón de piedra, {heroe}. Abajo, ríos de plomo fundido corren hacia los hornos; arriba, ventanales enormes de vidrio de colores reparten la luz por toda la ciudad. Cada uno es una ventana a otro lugar del mundo.<br><br>Soy {mentor}, la Vitralista. Acá se fabrican los vitrales por los que se asoma todo el mundo: las **páginas web**. Primero vas a aprender el **plomo**, la estructura; después, los **vidrios de colores**; y al final, las **plantillas del gremio**, para trabajar rápido.<br><br>Una sola regla: **todo vitral empieza chico**. Cada tema que domines te abre un taller nuevo; cada misión aprobada te da cristales para abrir el siguiente. | curso |
| story.branch_completed | ¡Taller terminado! | | m | | {mentor} levanta tu vitral contra la luz y lo mira despacio, desde la cabaña y desde el castillo. —Esto ya se sostiene solo, {heroe}. Colgalo. | curso |
| story.course_completed | ¡El gran ventanal está terminado! | | m | | {mentor} se queda mirando tu ventanal un largo rato. —¿Sabés a qué se parece? Al portal por el que llegaste. Ese portal es un vitral, {heroe}, y el plomo lo trabajó mi maestro, el Vidriero, antes de desaparecer. Lo que hiciste está quieto: brilla, pero no se mueve. Lo que hace moverse a un vitral se aprende en la **Feria de las Luces**. Cuando estés lista o listo, ahí te espero. | curso |
| beast.slime | slime | slimes | m | Nace de las etiquetas mal cerradas o mal anidadas: las marca el validador. | Los slimes brotan de un `</p>` que nadie escribió, de un `<strong>` que se cierra afuera de su párrafo, de una lista sin su `<ul>`. El navegador los perdona y "adivina" qué quisiste decir… y casi siempre adivina mal. El validador los encuentra todos. | curso |
| beast.goblin | goblin | goblins | m | Nace de los valores de CSS inválidos: el navegador los ignora en silencio. | Los goblins viven en los detalles: `20 px` con un espacio, `colour` en vez de `color`, un color de cinco dígitos. El navegador no avisa: simplemente ignora la regla. En el inspector aparecen **tachados**, con un triangulito amarillo. | curso |
| beast.skeleton | esqueleto | esqueletos | m | Nace de lo que no existe: clases, rutas de imágenes o enlaces que no apuntan a nada. | Los esqueletos son nombres sin cuerpo: `class="Aviso"` cuando la regla dice `.aviso`, una imagen que se busca en la carpeta equivocada, un enlace a `#contacto` cuando la sección se llama `#contactos`. En la pestaña *Red* del inspector aparecen en rojo. | curso |
| beast.orc | orco | orcos | m | Nace de los desbordes: algo más ancho que la pantalla y aparece el scroll horizontal. | Los orcos atacan en el celular: una imagen de 1200 px, una tabla que no entra, un texto larguísimo sin cortes. La página entera se puede arrastrar de costado y todo se ve corrido. | curso |
| beast.ogre | ogro | ogros | m | Nace de la cascada y la especificidad: la regla está, pero otra le gana. | El ogro es el más frustrante: escribís el estilo, guardás, recargás… y no pasa nada. No es que esté mal escrito: hay otra regla más específica, o que viene después, que le gana. En el inspector, la tuya aparece tachada sin triangulito. | curso |
| beast.troll | troll | trolls | m | Nace de las capas que se pisan: `position`, `z-index` y los elementos fijos que tapan contenido. | El troll se esconde detrás de las cosas: una barra fija que tapa el último renglón, un menú que queda por debajo de una imagen, un botón que no se puede tocar porque otra caja invisible está encima. | curso |
| beast.dragon | dragón | dragones | m | Guardián de los jefes: una página grande hecha de piezas chicas. | Un dragón no se vence de un golpe. Se lo divide en piezas —el marco, el panel central, las tarjetas, la tabla—, se arma cada una y recién entonces cae. | curso |

## R00-N01 · Clase 0 · Hola, HTML

```meta
tipo: raiz
criatura: slime
temas: html.estructura, herr.navegador
```

### Crónica

Cruzás el portal y aparecés en un balcón de piedra, sobre una ciudad de ventanales que brillan. Abajo, ríos de **plomo fundido** bajan hacia los hornos. Una mujer con un monóculo de cristal te espera con una varilla gris en la mano: es **{mentor}**, la Vitralista.

—¿Vidrios de colores? Todavía no, {heroe} —te dice, y te da el plomo—. Primero la **estructura**. Un vitral sin plomo es un montón de vidrios rotos en el piso. Este plomo lo funden en las Forjas de Hierro, las de Maese Ferrum: sin su metal no habría ni un vitral en todo el mundo.

### Objetivos

Escribir una página HTML completa y válida, entender sus partes (`head` y `body`), abrirla en el navegador y revisarla con el inspector y el validador.

### Antes de empezar

Nada: escribís en la plataforma y tu página se dibuja al lado. Para practicar también en tu compu alcanza con un editor de texto (VS Code, por ejemplo) y un navegador (Chrome o Firefox).

### Explicación

#### ¿Qué es HTML?
**HTML** describe **qué es** cada parte de una página: "esto es un título", "esto es un párrafo". No dice cómo se ve: de eso se encarga CSS («Primeros vidrios: CSS»). Se escribe con
**etiquetas**:
```html
<p>Un párrafo</p>         <!-- apertura, contenido, cierre -->
<meta charset="utf-8">    <!-- etiqueta "vacía": no tiene contenido ni cierre -->
```
Dentro de la apertura van los **atributos**: `nombre="valor"` (`lang="es"`).

#### El esqueleto
| Parte | Para qué |
|---|---|
| `<!DOCTYPE html>` | "esto es HTML moderno" (siempre la primera línea) |
| `<html lang="es">` | la raíz; `lang` le dice al lector de pantalla en qué idioma leer |
| `<head>` | datos para el navegador: no se ven |
| `<meta charset="utf-8">` | permite tildes y eñes |
| `<meta name="viewport" ...>` | **clave para el celular**: sin esto, se ve la versión de escritorio achicada |
| `<title>` | el texto de la pestaña |
| `<body>` | todo lo que se ve |

#### Primeras etiquetas de texto
| Etiqueta | Qué es |
|---|---|
| `<h1>` … `<h6>` | títulos, del más importante al menos. Un solo `h1` por página, sin saltear niveles |
| `<p>` | párrafo |
| `<strong>` | texto **importante** (se ve en negrita) |
| `<em>` | texto con *énfasis* (se ve en cursiva) |
| `<!-- ... -->` | comentario: no se ve |

**Anidar bien:** lo que se abre adentro se cierra adentro. `<p><strong>bien</strong></p>`, no `<p><strong>mal</p></strong>`.

#### Herramientas
- **En la plataforma**: escribís y tu página se dibuja al lado, sola. Con *Celular* y *Compu* la ves en los dos tamaños; con el botón de pantalla completa, grande. Fuera de la plataforma: guardá el archivo como `index.html` y abrilo con doble clic.
- **Inspector (DevTools)**: clic derecho → *Inspeccionar* (o F12). Muestra el árbol de etiquetas. Con el ícono de celular (Ctrl+Shift+M) se ve la página **en tamaño celular**: lo vamos a usar todo el curso.
- **Validador**: revisa que el HTML esté bien escrito. Copiá tu código, abrí [validator.w3.org](https://validator.w3.org/#validate_by_input), pegalo en *Validate by Direct Input* y tocá *Check*. Si dice *No errors*, el plomo está bien soldado.

#### El ejemplo

Una página mínima con título y dos párrafos.

#### Cómo se ve el ejemplo

Pestaña "Mi primer vitral"; en la página, el título grande "¡Hola, Talleres!" y dos párrafos, con "HTML" en negrita y "qué es" en cursiva. Letra con serifa, fondo blanco: así se ve HTML **sin** CSS. El validador dice *No errors* si todo está bien.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <!-- head: datos PARA el navegador; no se ven en la pagina -->
    <meta charset="utf-8">
    <!-- Sin esta linea, el celular muestra la pagina "achicada" como si fuera de escritorio -->
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Mi primer vitral</title>
  </head>
  <body>
    <!-- body: lo que SI se ve -->
    <h1>¡Hola, Talleres!</h1>
    <p>Soy Kira y este es mi primer vitral escrito en <strong>HTML</strong>.</p>
    <p>El HTML describe <em>qué es</em> cada cosa: un título, un párrafo, un texto importante.</p>
  </body>
</html>
```

### ¿Para qué sirve?

Toda página que abrís —un diario, una tienda, esta misma plataforma— es un archivo HTML que el navegador dibuja. Las apps de los bancos, los correos que te llegan con colores y botones, las pantallas de muchos juegos: todo eso tiene HTML adentro. Y aunque después uses herramientas que lo escriben por vos, cuando algo se ve mal, el que entiende el HTML es el que lo arregla.

### Errores habituales

En HTML el navegador **no se queja**: intenta adivinar y sigue. Por eso se usa el validador.

**Slime: etiqueta sin cerrar** (`<p>Hola <strong>mundo</p>`):
```
5:10  error  Unclosed element '<strong>'                         close-order
5:23  error  End tag '</p>' seen but there were open elements    close-order
```
Y como el `<strong>` quedó abierto, **todo lo que sigue** sale en negrita.

**Slime: falta el idioma**:
```
2:2  error  <html> is missing required "lang" attribute   element-required-attributes
```
**Ogro: tildes rotas** (`Ã¡` en vez de `á`): falta `<meta charset="utf-8">`.

**Ogro: en el celular se ve todo diminuto**: falta el `meta viewport`.

### Prueba del sello

#### ¿Qué va en `head` y qué en `body`?

En el `head` van los datos **para el navegador**, que no se ven en la página: el `charset`, el `viewport`, el `title` de la pestaña y, más adelante, los estilos. En el `body` va **todo lo que se ve**: títulos, párrafos, imágenes, botones.

#### ¿Para qué sirve el `meta viewport`?

Le dice al celular que use su ancho real. Sin él, el celular hace de cuenta que es una pantalla de compu de unos 980 px y achica todo: la página se ve diminuta y hay que hacer zoom para leer.

#### ¿Por qué no hay que usar `h3` solo porque "se ve más chico"?

Porque los títulos dicen **qué importancia** tiene cada parte, no qué tamaño tiene. Un lector de pantalla y un buscador usan esa jerarquía para entender la página; saltar de `h1` a `h3` es como un índice al que le falta un nivel. El tamaño se cambia con CSS.

### Misión R00-N01-M1 · La presentación

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá una página que presente a {heroe} como aprendiz de los Talleres:

1. El esqueleto completo: `DOCTYPE`, `html` con `lang="es"`, `head` con `charset`, `viewport` y `title`.
2. Un `h1` con el nombre y un `h2` con su especialidad.
3. Dos párrafos que cuenten algo de su viaje, con al menos una palabra en `strong` y otra en `em`.

#### Criterio de aprobación

- Tiene el esqueleto completo: `<!DOCTYPE html>`, `lang="es"`, `charset`, `viewport` y `title`.
- Hay un solo `h1`, seguido de un `h2`.
- Hay dos párrafos, con al menos un `strong` y un `em`.
- Todas las etiquetas se cierran en orden (sin slimes).

#### Cómo debe quedar

celular: capturas/R00-N01-M1-celular.webp
compu: capturas/R00-N01-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La presentación</title>
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
    <title>Presentación de Kira</title>
  </head>
  <body>
    <h1>Kira</h1>
    <h2>Espadachina aprendiz</h2>
    <p>Llegué a Codexia por un portal. Ahora aprendo a <strong>escribir magia</strong>.</p>
    <p>Mi objetivo: <em>volver a casa</em>.</p>
  </body>
</html>
```


### Misión R00-N01-M2 · El manual del taller

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Escribí el índice de un "manual del taller" usando solo títulos y párrafos:

1. Un `h1` con el nombre del manual.
2. Dos `h2` (dos capítulos), cada uno con un párrafo.
3. Bajo el **primer** capítulo, dos `h3` (dos apartados), cada uno con su párrafo.

Sin saltear niveles: nunca un `h3` sin un `h2` arriba.

#### Criterio de aprobación

- Un `h1`, dos `h2` y dos `h3` dentro del primer capítulo.
- Ningún nivel salteado (no hay `h3` directamente bajo el `h1`).
- Cada título tiene al menos un párrafo debajo.
- El esqueleto está completo y las etiquetas, bien cerradas.

#### Cómo debe quedar

celular: capturas/R00-N01-M2-celular.webp
compu: capturas/R00-N01-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El manual del taller</title>
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
    <title>Jerarquía de títulos</title>
  </head>
  <body>
    <h1>Manual del Taller</h1>
    <h2>Capítulo 1: El plomo</h2>
    <h3>Cómo cortar el plomo</h3>
    <p>Con cuidado y en línea recta.</p>
    <h3>Cómo soldarlo</h3>
    <p>A fuego lento.</p>
    <h2>Capítulo 2: Los vidrios</h2>
    <p>Próximamente.</p>
  </body>
</html>
```


### Encargo R00-N01-E1 · El cartel de la panadería

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

El Gremio necesita el cartel de una panadería del barrio: el nombre (como título), el horario, el teléfono y una frase destacada ("¡Pan caliente a toda hora!"). Usá títulos, párrafos, `strong` y `em` donde corresponda.

#### Criterio de aprobación

- El nombre de la panadería es el único `h1`.
- Horario y teléfono están en párrafos.
- La frase destacada usa `strong` o `em`.
- El esqueleto está completo.

#### Cómo debe quedar

celular: capturas/R00-N01-E1-celular.webp
compu: capturas/R00-N01-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El cartel de la panadería</title>
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
    <title>Panadería La Ola</title>
  </head>
  <body>
    <h1>Panadería La Ola</h1>
    <p><strong>Horario:</strong> lunes a sábado, de 7 a 20.</p>
    <p><strong>Teléfono:</strong> 380 412-3456</p>
    <p><em>¡Pan caliente todas las mañanas!</em></p>
  </body>
</html>
```
