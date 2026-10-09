# RAMA R04 · El Gran Ventanal: la plataforma GhecoSoft-Code

```meta
tipo: tronco
posicion: 4
```

## R04-N01 · El marco: navegación

```meta
tipo: tema
padre: R03-N08
precio: 10
criatura: troll
temas: css.posicion
usa: css.frameworks, css.temas, html.semantica
```

### Crónica

El Gremio le encarga a {mentor} el trabajo más grande de los Talleres: **el gran ventanal**, la plataforma **GhecoSoft-Code**, la misma por la que se aprende en todos los mundos. {mentor} se lo pasa a Iris. Despliega el boceto —uno para la ventana de la cabaña y otro para el castillo— y le da un consejo:

—No empieces por el vidrio más lindo. Empezá por el **marco**: arriba, abajo y cómo se llega a cada parte.

Iris empieza por el marco. No tira ningún boceto en toda la mañana. Teo se preocupa y le pregunta si se siente bien.

### Objetivos

Armar el esqueleto de la página definitiva: cabecera fija con marca y estadísticas, menú principal **solo en la computadora**, barra inferior **solo en el celular**, pie, y el enlace de salto accesible.

### Antes de empezar

- Todo lo de las Plantillas del Gremio: el kit de «Componentes» es la base visual.
- El esqueleto semántico de «HTML semántico»: es el mismo, ahora con diseño.

### Explicación

#### El proyecto crece en cinco pasos
| Nodo | Agrega |
|---|---|
| **El marco: navegación** | cabecera, menú, barra inferior, pie |
| El panel central: hero y acceso | hero con la ilustración + login |
| Los vidrios de las rutas | grilla de cursos y filtros |
| El Hall of Fame | podio + lista en el celular / tabla en la compu |
| Jefe final: el Dragón de los Talleres | bóveda de tokens, revisión final y accesibilidad |

El CSS del tema es el del kit de «Componentes», con una animación más. Todas las etapas comparten el mismo tema: en la plataforma va en el bloque `<style type="text/tailwindcss">` de cada página.

#### La cabecera
- `sticky top-0 z-40 bg-fondo/85 backdrop-blur`: queda pegada y deja ver, borroso, lo que pasa por detrás.
- Contenedor: `mx-auto max-w-7xl px-4` (igual en el `main` y el pie: todo alineado).
- **Marca**: el logo de Gheco con la etiqueta `LV.14` encima (`relative` en el logo + `absolute -bottom-1.5 left-1/2 -translate-x-1/2` en la etiqueta), y "SYSTEM ONLINE" con el punto que late (`animate-latido`). La etiqueta de nivel solo se ve en el celular (`lg:hidden`): en la computadora el nivel va en la barra de la derecha.
- **Estadísticas**: en el celular, una sola pastilla `⚡ 1.450 · 🔥 12`; desde `lg`, la racha se separa en "🔥 12 días", aparece el avatar, y desde `xl` la barrita de nivel. Es el mismo dato mostrado según el espacio.
- **Menú**: `hidden lg:flex`. El enlace actual lleva `aria-current="page"` y un estilo de pastilla. `whitespace-nowrap` evita que un enlace se parta en dos líneas; y las etiquetas largas se acortan entre `lg` y `xl` ("Top 10" → "Top 10 alumnos").

#### La barra inferior (el menú del celular)
`fixed inset-x-0 bottom-0 lg:hidden` + `pb-20 lg:pb-0` en el `body` para que no tape el final. La sección activa tiene recuadro y color. Los íconos llevan `aria-hidden="true"`: el lector de pantalla lee solo el texto ("Arena"), no "espadas cruzadas Arena".

#### El enlace de salto
`sr-only focus:not-sr-only focus:fixed …`: invisible, pero al apretar Tab aparece arriba a la izquierda. Probalo.

#### El ejemplo


#### Cómo se ve el ejemplo

Tocá *Celular* y *Compu* en la vista previa: . Celular: cabecera con el logo y su `LV.14`, la pastilla de estadísticas, un recuadro punteado (lugar de las próximas secciones), el pie apilado y la barra de 4 secciones abajo con "Arena" marcada. Computadora: menú en la cabecera con "Top 10 alumnos" resaltado, nivel, ESC, racha y avatar; sin barra inferior; pie en 3 columnas.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GhecoSoft-Code · Etapa: Navegación</title>
    <meta name="description" content="Aprendé a programar avanzando por tu árbol de habilidades: C++, SDL3, OpenGL, WebAssembly y más.">
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <!-- pb-20: lugar para la barra inferior del celular; desde lg no hay barra -->
  <body class="pb-20 lg:pb-0">
    <!-- SECCION:salto -->
    <!-- Enlace de salto: invisible hasta que recibe el foco con Tab -->
    <a href="#contenido" class="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 focus:rounded-lg focus:bg-neon focus:px-4 focus:py-2 focus:text-fondo">Saltar al contenido</a>
    <!-- /SECCION:salto -->

    <!-- SECCION:cabecera -->
    <!-- ===== CABECERA ===== -->
    <header class="sticky top-0 z-40 border-b border-borde bg-fondo/85 backdrop-blur">
      <div class="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3">
        <!-- Marca: logo con su nivel + nombre + estado -->
        <a href="#" class="flex items-center gap-3">
          <span class="relative shrink-0">
            <img src="/img/cursos/html/gheco-logo.webp" alt="" width="44" height="44" class="size-11 rounded-xl ring-1 ring-neon/50">
            <span class="absolute -bottom-1.5 left-1/2 -translate-x-1/2 rounded bg-violet-600 px-1 font-mono text-[9px] leading-tight font-bold text-white lg:hidden">LV.14</span>
          </span>
          <span>
            <span class="block font-display text-lg leading-tight font-bold whitespace-nowrap">GhecoSoft <span class="text-neon">-Code</span></span>
            <span class="flex items-center gap-1.5 font-mono text-[10px] tracking-widest text-slate-400 uppercase">
              <span class="size-1.5 animate-latido rounded-full bg-emerald-400"></span> System online
            </span>
          </span>
        </a>

        <!-- Menu principal: solo desde lg (en el celular esta la barra de abajo) -->
        <nav aria-label="Principal" class="hidden items-center gap-1 text-sm whitespace-nowrap lg:flex">
          <a href="#rutas" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Cursos</a>
          <a href="#rutas" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Rutas</a>
          <a href="#fama" aria-current="page" class="rounded-lg border border-neon/50 bg-neon/10 px-3 py-2 text-neon">🏆 Top 10<span class="hidden xl:inline"> alumnos</span></a>
          <a href="#" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Skill Tree</a>
          <a href="#boveda" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Bóveda<span class="hidden xl:inline"> de tokens</span></a>
        </nav>

        <!-- Estadisticas del jugador -->
        <div class="flex items-center gap-2 font-mono text-xs whitespace-nowrap">
          <span class="hidden items-center gap-2 rounded-lg border border-borde px-2.5 py-1.5 xl:flex">
            LVL 14
            <span class="h-1.5 w-12 overflow-hidden rounded-full bg-borde"><span class="block h-full w-2/3 bg-violet-500"></span></span>
          </span>
          <span class="rounded-lg border border-borde px-2.5 py-1.5"><span class="text-neon">⚡ 1.450</span><span class="hidden lg:inline"> ESC</span><span class="lg:hidden"> · <span class="text-fuego">🔥 12</span></span></span>
          <span class="hidden rounded-lg border border-fuego/40 px-2.5 py-1.5 text-fuego lg:inline">🔥 12 días</span>
          <img src="/img/cursos/html/heroe-avatar.webp" alt="Tu perfil" width="36" height="36" class="hidden size-9 rounded-full border-2 border-neon object-cover lg:block">
        </div>
      </div>
    </header>
    <!-- /SECCION:cabecera -->

    <main id="contenido" class="mx-auto max-w-7xl space-y-16 px-4 py-6 lg:space-y-24 lg:py-10">
      <!-- Lo que falta se agrega en las proximas etapas del proyecto -->
      <p class="rounded-xl border border-dashed border-borde p-6 text-center font-mono text-sm text-slate-500">Próximas secciones: prácticas siguientes del proyecto (hasta la 22).</p>



    </main>

    <!-- SECCION:pie -->
    <!-- ===== PIE ===== -->
    <footer class="border-t border-borde">
      <div class="mx-auto grid max-w-7xl gap-6 px-4 py-8 text-sm md:grid-cols-[2fr_1fr_1fr] md:items-center">
        <div class="flex items-center gap-3">
          <img src="/img/cursos/html/gheco-logo.webp" alt="" width="36" height="36" class="size-9 rounded-lg">
          <p><span class="font-display font-bold">GhecoSoft-Code Platform</span><br><span class="text-xs text-slate-500">Formación avanzada en bajo nivel, motores de videojuegos y compilación real.</span></p>
        </div>
        <ul class="space-y-1 font-mono text-xs text-slate-400">
          <li><span class="text-emerald-400">●</span> Cloud Compiler Clang 18: online</li>
          <li><span class="text-emerald-400">●</span> GCC 14 / Emscripten: 99.98% uptime</li>
        </ul>
        <p class="font-mono text-xs text-slate-500 md:text-right">© 2026 GhecoSoft-Code.<br>Obsidian Design Protocol v4.2</p>
      </div>
    </footer>
    <!-- /SECCION:pie -->

    <!-- SECCION:barra -->
    <!-- ===== BARRA INFERIOR (solo celular y tablet) ===== -->
    <nav aria-label="Secciones" class="fixed inset-x-0 bottom-0 z-40 border-t border-borde bg-panel/95 backdrop-blur lg:hidden">
      <div class="mx-auto flex max-w-lg">
        <a href="#rutas" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">🗺</span>Campañas</a>
        <a href="#" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">📖</span>Lecciones</a>
        <a href="#fama" aria-current="page" class="my-1 flex flex-1 flex-col items-center gap-0.5 rounded-xl border border-neon/50 bg-neon/10 py-1 text-[11px] text-neon"><span aria-hidden="true" class="text-lg">⚔</span>Arena</a>
        <a href="#" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">🌳</span>Árbol</a>
      </div>
    </nav>
    <!-- /SECCION:barra -->
  </body>
</html>
```

### ¿Para qué sirve?

Toda aplicación web tiene este marco: una cabecera con la marca y el usuario, un menú, y en el celular una barra abajo, al alcance del pulgar (como Instagram o Mercado Libre). Armarlo bien —accesible, que no tape contenido, que se adapte— es lo primero que se hace en cualquier proyecto.

### Errores habituales

**Troll: la cabecera queda debajo del contenido** al hacer scroll: falta `z-40` (o algo de adentro tiene un `z` mayor).

**Ogro: el menú se parte en dos líneas** entre 1024 y 1280 px. Medí en DevTools a 1024: acortá etiquetas, usá `whitespace-nowrap` o mostrá el menú desde `xl`.

**Troll: los enlaces `#seccion` quedan tapados por la cabecera fija.** Las secciones llevan `scroll-mt-24` (margen al hacer scroll hasta ellas).

### Prueba del sello

#### ¿Por qué el menú principal y la barra inferior son dos `nav` distintos? ¿Cómo los distingue un lector de pantalla?

Porque son dos menús distintos: uno se ve solo en la compu (arriba) y el otro solo en el celular (abajo). El lector de pantalla los distingue por su nombre: cada `nav` lleva un `aria-label` distinto ("Principal", "Secciones").

#### ¿Para qué sirve `pb-20 lg:pb-0` en el `body`?

Deja lugar abajo para la barra fija del celular, así no tapa el final de la página. Desde `lg` la barra no existe, entonces el relleno vuelve a cero.

#### ¿Por qué los íconos de la barra llevan `aria-hidden="true"`?

Para que el lector de pantalla lea solo el texto ("Arena") y no la descripción del ícono ("espadas cruzadas Arena"). El ícono es decoración; el texto es la información.

### Misión R04-N01-M1 · El menú desplegable

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

En el celular, armá un botón **☰** que abra el menú **sin JavaScript** (con `details` y `summary`), y que se oculte desde `lg`, donde el menú ya se ve completo.

#### Criterio de aprobación

- Usa `details`/`summary`, sin JavaScript.
- El botón tiene un texto accesible (por ejemplo, `aria-label` o un texto `sr-only`).
- Desde `lg` el desplegable se oculta (`lg:hidden`).

#### Cómo debe quedar

celular: capturas/R04-N01-M1-celular.webp
compu: capturas/R04-N01-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El menú desplegable</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>Menú desplegable sin JavaScript</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <header class="border-b border-borde">
      <div class="flex items-center justify-between px-4 py-3">
        <a href="#" class="flex items-center gap-2 font-display font-bold"><img src="/img/cursos/html/gheco-logo.webp" alt="" width="36" height="36" class="size-9 rounded-lg"> GhecoSoft</a>
        <!-- details/summary: se abre y se cierra sin JavaScript. Solo en el celular -->
        <details class="group relative lg:hidden">
          <summary class="btn btn-secundario cursor-pointer list-none px-3 py-2" aria-label="Abrir menú"><span class="group-open:hidden" aria-hidden="true">☰</span><span class="hidden group-open:inline" aria-hidden="true">✕</span></summary>
          <nav aria-label="Principal (celular)" class="absolute right-0 z-50 mt-2 w-56 rounded-xl border border-borde bg-panel p-2 shadow-xl">
            <a href="#" class="block rounded-lg px-3 py-2 hover:bg-neon/10">Cursos</a>
            <a href="#" class="block rounded-lg px-3 py-2 hover:bg-neon/10">Rutas</a>
            <a href="#" aria-current="page" class="block rounded-lg bg-neon/10 px-3 py-2 text-neon">Top 10</a>
            <a href="#" class="block rounded-lg px-3 py-2 hover:bg-neon/10">Bóveda</a>
          </nav>
        </details>
        <nav aria-label="Principal" class="hidden gap-4 lg:flex"><a href="#">Cursos</a><a href="#">Rutas</a><a href="#" class="text-neon">Top 10</a><a href="#">Bóveda</a></nav>
      </div>
    </header>
    <main class="p-4 text-slate-400">Tocá ☰ (en el celular).</main>
  </body>
</html>
```


### Misión R04-N01-M2 · La barra con indicador

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá una barra inferior de **5 secciones** donde la activa tenga una **rayita arriba**, hecha con un pseudo-elemento (`before:`).

#### Criterio de aprobación

- Cinco secciones del mismo ancho.
- La activa lleva `aria-current="page"` y la rayita sale de `before:` (sin un elemento extra en el HTML).

#### Cómo debe quedar

celular: capturas/R04-N01-M2-celular.webp
compu: capturas/R04-N01-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La barra con indicador</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>Barra inferior con indicador</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <body class="min-h-screen pb-20">
    <main class="p-4 text-slate-400">La sección activa tiene una rayita arriba.</main>
    <nav aria-label="Secciones" class="fixed inset-x-0 bottom-0 flex border-t border-borde bg-panel text-[11px]">
      <a href="#" class="flex flex-1 flex-col items-center py-2 text-slate-400"><span aria-hidden="true" class="text-lg">🗺</span>Campañas</a>
      <a href="#" class="flex flex-1 flex-col items-center py-2 text-slate-400"><span aria-hidden="true" class="text-lg">📖</span>Lecciones</a>
      <!-- before: un pseudo-elemento: la rayita de arriba -->
      <a href="#" aria-current="page" class="relative flex flex-1 flex-col items-center py-2 text-neon before:absolute before:top-0 before:h-0.5 before:w-10 before:rounded-full before:bg-neon"><span aria-hidden="true" class="text-lg">⚔</span>Arena</a>
      <a href="#" class="flex flex-1 flex-col items-center py-2 text-slate-400"><span aria-hidden="true" class="text-lg">🌳</span>Árbol</a>
      <a href="#" class="flex flex-1 flex-col items-center py-2 text-slate-400"><span aria-hidden="true" class="text-lg">👤</span>Perfil</a>
    </nav>
  </body>
</html>
```


### Encargo R04-N01-E1 · El armazón del delivery

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Una app de delivery necesita su armazón: cabecera con el logo y el carrito, menú en la compu y barra inferior en el celular.

#### Criterio de aprobación

- Cabecera con logo y carrito.
- Menú visible solo en la compu y barra inferior solo en el celular.
- La barra no tapa el final de la página.

#### Cómo debe quedar

celular: capturas/R04-N01-E1-celular.webp
compu: capturas/R04-N01-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El armazón del delivery</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>App de delivery</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <body class="min-h-screen bg-white pb-20 text-slate-800 lg:pb-0">
    <header class="sticky top-0 border-b bg-white/90 backdrop-blur">
      <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <a href="#" class="text-xl font-black text-red-600">Pedí<span class="text-slate-800">Ya</span></a>
        <nav aria-label="Principal" class="hidden gap-6 lg:flex"><a href="#">Restaurantes</a><a href="#">Mercados</a><a href="#">Farmacias</a></nav>
        <a href="#" class="rounded-full bg-red-600 px-4 py-1.5 text-sm font-semibold text-white">🛒 3</a>
      </div>
    </header>
    <main class="mx-auto max-w-6xl p-4">Contenido</main>
    <nav aria-label="Secciones" class="fixed inset-x-0 bottom-0 flex border-t bg-white text-xs lg:hidden">
      <a href="#" aria-current="page" class="flex flex-1 flex-col items-center py-2 text-red-600"><span aria-hidden="true">🏠</span>Inicio</a>
      <a href="#" class="flex flex-1 flex-col items-center py-2"><span aria-hidden="true">🔍</span>Buscar</a>
      <a href="#" class="flex flex-1 flex-col items-center py-2"><span aria-hidden="true">📦</span>Pedidos</a>
    </nav>
  </body>
</html>
```

## R04-N02 · El panel central: hero y acceso

```meta
tipo: tema
padre: R04-N01
precio: 10
criatura: troll
temas: css.posicion
usa: html.formularios, css.frameworks
```

### Crónica

El panel central del ventanal es el que todos miran primero: la figura del aprendiz con su buzo de circuitos, la promesa del taller y, al costado, la puerta de entrada.

—El texto tiene que leerse **sobre** la ilustración, sin taparla —dice {mentor}—. Son tres capas de vidrio, una encima de la otra. Pensalas en orden.

Nora pasa la mano por el panel. —¿Qué dice la figura? —Iris ya le había escrito el nombre.

### Objetivos

Construir el **hero** (texto sobre una ilustración de fondo con degradé) y el **portal de acceso** (formulario de login), que en el celular van uno abajo del otro y en la computadora en dos columnas.

### Antes de empezar

- Etapa 18. Formularios («Formularios»), estados de los campos («Estados y transiciones»), imágenes con `srcset` («Texto, enlaces e imágenes»).

### Explicación

#### La tarjeta del hero
`overflow-hidden rounded-3xl border bg-panel lg:grid lg:grid-cols-[1.5fr_1fr]`: una sola caja con bordes redondeados; desde `lg`, dos columnas (texto más ancho que el login). `overflow-hidden` recorta la imagen en las esquinas redondeadas.

#### Texto sobre una imagen: las capas
```
┌──────────────── div relative isolate ──────────────────┐
│ img absolute -z-10 (la ilustración, a la derecha)      │  capa del fondo
│ div absolute inset-0 -z-10 (degradé)                    │  capa del medio
│ etiqueta, h1, párrafo, botones (normales)               │  capa de arriba
└──────────────────────────────────────────────────────────┘
```
- `isolate` crea un "grupo de capas" propio: los `-z-10` quedan detrás del texto pero
  **adentro** de la tarjeta (sin `isolate`, se irían detrás del fondo de la página).
- La imagen: `absolute top-0 right-0 h-full w-auto max-w-none object-cover`: ocupa todo el alto y se pega a la derecha.
- El degradé hace legible el texto. **Mobile first**: en el celular va de abajo hacia arriba (`bg-linear-to-t`), porque el texto está abajo y el personaje arriba; desde `lg`, de izquierda a derecha (`lg:bg-linear-to-r`), porque el texto va a la izquierda.
- `justify-end` + `min-h-[36rem]` en el celular: el texto baja y deja ver al personaje arriba, como en esta plataforma.
- La ilustración es **decorativa** (`alt=""`): lo importante está en el texto. Usa `srcset` con dos tamaños (448 y 896 px).

#### El portal (login)
El formulario del 04 con el kit del 17: etiquetas `etiqueta-mono`, campos con `focus:ring`, error con `peer` + `user-invalid`, "¿Olvidaste tu contraseña?" alineado con su etiqueta (`flex items-baseline justify-between`), un divisor "o seguí con tu email" hecho con dos líneas `h-px flex-1` y una tarjeta de **misión en curso**. `accent-cyan-400` pinta la casilla nativa con el color del tema.

#### Botones del hero
En el celular, "Continuar campaña" ocupa el resto (`flex-1`) y el segundo dice solo "Top 10"; desde `sm`, cada uno mide lo suyo y el segundo dice "Ver leaderboard".

#### Cómo se ve el ejemplo

Tocá *Celular* y *Compu* en la vista previa: . Celular: el aprendiz arriba, que se funde hacia abajo con el texto, los dos botones en una fila y el portal debajo. Computadora: el texto a la izquierda con el personaje detrás y a la derecha, y el portal en su columna con borde a la izquierda.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GhecoSoft-Code · Etapa: Hero y login</title>
    <meta name="description" content="Aprendé a programar avanzando por tu árbol de habilidades: C++, SDL3, OpenGL, WebAssembly y más.">
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <!-- pb-20: lugar para la barra inferior del celular; desde lg no hay barra -->
  <body class="pb-20 lg:pb-0">
    <!-- SECCION:salto -->
    <!-- Enlace de salto: invisible hasta que recibe el foco con Tab -->
    <a href="#contenido" class="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 focus:rounded-lg focus:bg-neon focus:px-4 focus:py-2 focus:text-fondo">Saltar al contenido</a>
    <!-- /SECCION:salto -->

    <!-- SECCION:cabecera -->
    <!-- ===== CABECERA ===== -->
    <header class="sticky top-0 z-40 border-b border-borde bg-fondo/85 backdrop-blur">
      <div class="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3">
        <!-- Marca: logo con su nivel + nombre + estado -->
        <a href="#" class="flex items-center gap-3">
          <span class="relative shrink-0">
            <img src="/img/cursos/html/gheco-logo.webp" alt="" width="44" height="44" class="size-11 rounded-xl ring-1 ring-neon/50">
            <span class="absolute -bottom-1.5 left-1/2 -translate-x-1/2 rounded bg-violet-600 px-1 font-mono text-[9px] leading-tight font-bold text-white lg:hidden">LV.14</span>
          </span>
          <span>
            <span class="block font-display text-lg leading-tight font-bold whitespace-nowrap">GhecoSoft <span class="text-neon">-Code</span></span>
            <span class="flex items-center gap-1.5 font-mono text-[10px] tracking-widest text-slate-400 uppercase">
              <span class="size-1.5 animate-latido rounded-full bg-emerald-400"></span> System online
            </span>
          </span>
        </a>

        <!-- Menu principal: solo desde lg (en el celular esta la barra de abajo) -->
        <nav aria-label="Principal" class="hidden items-center gap-1 text-sm whitespace-nowrap lg:flex">
          <a href="#rutas" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Cursos</a>
          <a href="#rutas" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Rutas</a>
          <a href="#fama" aria-current="page" class="rounded-lg border border-neon/50 bg-neon/10 px-3 py-2 text-neon">🏆 Top 10<span class="hidden xl:inline"> alumnos</span></a>
          <a href="#" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Skill Tree</a>
          <a href="#boveda" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Bóveda<span class="hidden xl:inline"> de tokens</span></a>
        </nav>

        <!-- Estadisticas del jugador -->
        <div class="flex items-center gap-2 font-mono text-xs whitespace-nowrap">
          <span class="hidden items-center gap-2 rounded-lg border border-borde px-2.5 py-1.5 xl:flex">
            LVL 14
            <span class="h-1.5 w-12 overflow-hidden rounded-full bg-borde"><span class="block h-full w-2/3 bg-violet-500"></span></span>
          </span>
          <span class="rounded-lg border border-borde px-2.5 py-1.5"><span class="text-neon">⚡ 1.450</span><span class="hidden lg:inline"> ESC</span><span class="lg:hidden"> · <span class="text-fuego">🔥 12</span></span></span>
          <span class="hidden rounded-lg border border-fuego/40 px-2.5 py-1.5 text-fuego lg:inline">🔥 12 días</span>
          <img src="/img/cursos/html/heroe-avatar.webp" alt="Tu perfil" width="36" height="36" class="hidden size-9 rounded-full border-2 border-neon object-cover lg:block">
        </div>
      </div>
    </header>
    <!-- /SECCION:cabecera -->

    <main id="contenido" class="mx-auto max-w-7xl space-y-16 px-4 py-6 lg:space-y-24 lg:py-10">
      <!-- Lo que falta se agrega en las proximas etapas del proyecto -->
      <p class="rounded-xl border border-dashed border-borde p-6 text-center font-mono text-sm text-slate-500">Próximas secciones: prácticas siguientes del proyecto (hasta la 22).</p>
      <!-- SECCION:hero -->
      <!-- ===== HERO + LOGIN ===== -->
      <section aria-labelledby="titulo-hero" class="overflow-hidden rounded-3xl border border-borde bg-panel lg:grid lg:grid-cols-[1.5fr_1fr]">
        <!-- Lado izquierdo: ilustracion de fondo + texto -->
        <div class="fondo-cuadricula relative isolate flex min-h-[36rem] flex-col justify-end p-6 sm:min-h-[30rem] sm:p-10 lg:min-h-[34rem]">
          <img src="/img/cursos/html/heroe-448.webp" srcset="/img/cursos/html/heroe-448.webp 448w, /img/cursos/html/heroe-896.webp 896w" sizes="(min-width: 64rem) 30rem, 70vw" alt="" width="448" height="600" class="absolute top-0 right-0 -z-10 h-full w-auto max-w-none object-cover opacity-80">
          <!-- Degrade para que el texto se lea sobre la imagen -->
          <div class="absolute inset-0 -z-10 bg-linear-to-t from-panel from-30% via-panel/70 to-transparent lg:bg-linear-to-r lg:via-panel/70 lg:to-transparent"></div>

          <p class="etiqueta-mono inline-flex w-fit items-center gap-2 rounded-full border border-neon/40 bg-fondo/60 px-3 py-1 text-[10px] text-neon">
            <span class="size-1.5 animate-latido rounded-full bg-neon"></span> Plataforma de cursos <span class="hidden sm:inline">· Temporada 04</span>
          </p>
          <h1 id="titulo-hero" class="mt-4 max-w-xl text-3xl leading-tight font-bold sm:text-4xl lg:text-5xl">
            Aprendé a programar avanzando por tu <span class="texto-neon text-neon">árbol de habilidades</span>.
          </h1>
          <p class="mt-3 max-w-lg text-slate-300 lg:text-lg">
            Compilá algoritmos reales, desbloqueá nodos tecnológicos de bajo nivel (C++, SDL3, OpenGL, WASM) y competí por el rango Supremo del salón de la fama.
          </p>
          <div class="mt-6 flex gap-3">
            <a href="#rutas" class="btn btn-primario flex-1 sm:flex-none">▷ Continuar campaña</a>
            <a href="#fama" class="btn btn-secundario"><span class="sm:hidden">Top 10</span><span class="hidden sm:inline">Ver leaderboard <span class="ml-1 rounded bg-neon/10 px-1.5 text-xs">Top 10</span></span></a>
          </div>
        </div>

        <!-- Lado derecho: el portal (login). En el celular va debajo -->
        <div class="border-t border-borde bg-fondo/40 p-6 sm:p-10 lg:border-t-0 lg:border-l">
          <p class="etiqueta-mono text-center text-[10px] text-slate-500">Portal del desarrollador</p>
          <h2 class="mt-2 text-center text-2xl font-bold">Entrá a tu cuenta</h2>
          <p class="mt-1 text-center text-sm text-slate-400">Ingresá tu usuario y contraseña para retomar tu entrenamiento.</p>

          <form action="#" method="post" class="mt-6 space-y-4">
            <button type="button" class="btn w-full border border-borde bg-panel py-2.5 text-sm text-slate-200 hover:border-neon/60">🔑 Entrar con llave de acceso (Passkey)</button>
            <p class="flex items-center gap-3 font-mono text-[10px] tracking-widest text-slate-500 uppercase" aria-hidden="true">
              <span class="h-px flex-1 bg-borde"></span> o seguí con tu email <span class="h-px flex-1 bg-borde"></span>
            </p>
            <div class="space-y-1">
              <label for="usuario" class="etiqueta-mono block text-[10px] text-slate-400">Usuario o email</label>
              <input id="usuario" name="usuario" type="text" autocomplete="username" required placeholder="cliente" class="peer w-full rounded-lg border border-borde bg-fondo px-3 py-2.5 placeholder:text-slate-600 focus:border-neon focus:ring-2 focus:ring-neon/30 focus:outline-none user-invalid:border-rose-400">
              <p class="hidden text-xs text-rose-400 peer-user-invalid:block">Completá tu usuario o email.</p>
            </div>
            <div class="space-y-1">
              <div class="flex items-baseline justify-between">
                <label for="clave" class="etiqueta-mono text-[10px] text-slate-400">Contraseña</label>
                <a href="#" class="text-xs text-neon hover:underline">¿Olvidaste tu contraseña?</a>
              </div>
              <input id="clave" name="clave" type="password" autocomplete="current-password" required minlength="8" class="w-full rounded-lg border border-borde bg-fondo px-3 py-2.5 focus:border-neon focus:ring-2 focus:ring-neon/30 focus:outline-none">
            </div>
            <label class="flex items-center gap-2 text-sm text-slate-300">
              <input type="checkbox" name="recordarme" checked class="size-4 accent-cyan-400"> Recordarme en esta terminal
            </label>
            <button type="submit" class="btn btn-primario w-full tracking-wider uppercase">Entrar a la terminal →</button>
          </form>
          <p class="mt-4 text-center text-sm text-slate-400">¿No tenés cuenta aún? <a href="#" class="font-semibold text-neon hover:underline">Registrate gratis</a></p>

          <!-- Mision en curso -->
          <div class="mt-6 flex items-center gap-3 rounded-xl border border-borde bg-panel p-3">
            <span class="size-2 shrink-0 rounded-full bg-emerald-400"></span>
            <p class="min-w-0 flex-1 text-xs">
              <span class="etiqueta-mono block text-[10px] text-neon">Misión en curso</span>
              <span class="block truncate text-slate-300">04-C++ Moderno: Smart Pointers</span>
            </p>
            <span class="rounded-md bg-neon/10 px-2 py-1 font-mono text-xs text-neon">75%</span>
          </div>
        </div>
      </section>
      <!-- /SECCION:hero -->



    </main>

    <!-- SECCION:pie -->
    <!-- ===== PIE ===== -->
    <footer class="border-t border-borde">
      <div class="mx-auto grid max-w-7xl gap-6 px-4 py-8 text-sm md:grid-cols-[2fr_1fr_1fr] md:items-center">
        <div class="flex items-center gap-3">
          <img src="/img/cursos/html/gheco-logo.webp" alt="" width="36" height="36" class="size-9 rounded-lg">
          <p><span class="font-display font-bold">GhecoSoft-Code Platform</span><br><span class="text-xs text-slate-500">Formación avanzada en bajo nivel, motores de videojuegos y compilación real.</span></p>
        </div>
        <ul class="space-y-1 font-mono text-xs text-slate-400">
          <li><span class="text-emerald-400">●</span> Cloud Compiler Clang 18: online</li>
          <li><span class="text-emerald-400">●</span> GCC 14 / Emscripten: 99.98% uptime</li>
        </ul>
        <p class="font-mono text-xs text-slate-500 md:text-right">© 2026 GhecoSoft-Code.<br>Obsidian Design Protocol v4.2</p>
      </div>
    </footer>
    <!-- /SECCION:pie -->

    <!-- SECCION:barra -->
    <!-- ===== BARRA INFERIOR (solo celular y tablet) ===== -->
    <nav aria-label="Secciones" class="fixed inset-x-0 bottom-0 z-40 border-t border-borde bg-panel/95 backdrop-blur lg:hidden">
      <div class="mx-auto flex max-w-lg">
        <a href="#rutas" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">🗺</span>Campañas</a>
        <a href="#" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">📖</span>Lecciones</a>
        <a href="#fama" aria-current="page" class="my-1 flex flex-1 flex-col items-center gap-0.5 rounded-xl border border-neon/50 bg-neon/10 py-1 text-[11px] text-neon"><span aria-hidden="true" class="text-lg">⚔</span>Arena</a>
        <a href="#" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">🌳</span>Árbol</a>
      </div>
    </nav>
    <!-- /SECCION:barra -->
  </body>
</html>
```

### ¿Para qué sirve?

El "hero" es la primera pantalla de cualquier sitio: la de una película, un juego, una tienda. Poner texto legible sobre una imagen, sin que una cosa tape a la otra, es una de las tareas de diseño más pedidas. Y el login es la puerta de entrada de casi todas las aplicaciones.

### Errores habituales

**Troll: la imagen tapa el texto**: falta `-z-10` en la imagen y el degradé, o falta `isolate` en el contenedor (la imagen desaparece detrás del fondo de la página).

**Orco: la imagen se sale de la tarjeta**: falta `overflow-hidden` en la tarjeta.

**Ogro: el texto no se lee** sobre la parte clara de la ilustración: reforzá el degradé (`from-30%`, `via-panel/70`).

**Ogro: "Continuar campaña" en tres líneas**: el botón de al lado es demasiado largo para el celular. Acortalo en el celular o usá `whitespace-nowrap` (el componente `btn` ya lo trae).

### Prueba del sello

#### ¿Para qué sirve `isolate` en el contenedor del hero?

Crea un grupo de capas propio: la imagen y el degradé con `-z-10` quedan detrás del texto pero **adentro** de la tarjeta. Sin `isolate` se irían detrás del fondo de la página y desaparecerían.

#### ¿Por qué el degradé cambia de dirección en `lg`?

Porque cambia dónde está el texto: en el celular el texto va abajo y el personaje arriba, así que el degradé sube desde abajo (`bg-linear-to-t`); en la compu el texto va a la izquierda, así que el degradé va de izquierda a derecha (`lg:bg-linear-to-r`).

#### ¿Por qué la ilustración lleva `alt=""` y la de la misión 2 no?

Porque la ilustración del hero es **decorativa**: todo lo importante está en el texto. En la misión 2, la imagen de Gheco es parte del contenido, así que necesita un `alt` que la describa.

### Misión R04-N02-M1 · El registro

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá la página **"Creá tu cuenta"** con el estilo del portal: un alias con patrón (`pattern`), el email y la ruta inicial elegida con **chips** que se marcan con `has-checked:`.

#### Criterio de aprobación

- Cada campo tiene su `label`; el alias tiene `pattern` y el email `type="email"`.
- La ruta se elige con radios reales, escondidos con `sr-only`, y el chip elegido se marca con `has-checked:`.

#### Cómo debe quedar

celular: capturas/R04-N02-M1-celular.webp
compu: capturas/R04-N02-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El registro</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>Registro con el estilo de la plataforma</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <body class="fondo-cuadricula grid min-h-screen place-items-center p-4">
    <main class="tarjeta w-full max-w-md p-6 sm:p-8">
      <h1 class="text-center text-2xl font-bold">Creá tu cuenta</h1>
      <form action="#" method="post" class="mt-6 space-y-4">
        <div class="space-y-1">
          <label for="alias" class="etiqueta-mono block text-[10px] text-slate-400">Alias</label>
          <input id="alias" name="alias" type="text" required minlength="3" pattern="[A-Za-z0-9_]+" class="peer w-full rounded-lg border border-borde bg-fondo px-3 py-2.5 focus:border-neon focus:ring-2 focus:ring-neon/30 focus:outline-none user-invalid:border-rose-400">
          <p class="hidden text-xs text-rose-400 peer-user-invalid:block">Mínimo 3 letras, números o _.</p>
        </div>
        <div class="space-y-1">
          <label for="email" class="etiqueta-mono block text-[10px] text-slate-400">Email</label>
          <input id="email" name="email" type="email" autocomplete="email" required class="peer w-full rounded-lg border border-borde bg-fondo px-3 py-2.5 focus:border-neon focus:ring-2 focus:ring-neon/30 focus:outline-none user-invalid:border-rose-400">
          <p class="hidden text-xs text-rose-400 peer-user-invalid:block">Revisá el email.</p>
        </div>
        <fieldset class="space-y-2">
          <legend class="etiqueta-mono text-[10px] text-slate-400">Ruta inicial</legend>
          <div class="grid grid-cols-3 gap-2">
            <label class="chip cursor-pointer text-center has-checked:border-neon has-checked:bg-neon has-checked:text-fondo"><input type="radio" name="ruta" class="sr-only" checked> C++</label>
            <label class="chip cursor-pointer text-center has-checked:border-neon has-checked:bg-neon has-checked:text-fondo"><input type="radio" name="ruta" class="sr-only"> Web</label>
            <label class="chip cursor-pointer text-center has-checked:border-neon has-checked:bg-neon has-checked:text-fondo"><input type="radio" name="ruta" class="sr-only"> Python</label>
          </div>
        </fieldset>
        <button type="submit" class="btn btn-primario w-full">Crear cuenta</button>
      </form>
    </main>
  </body>
</html>
```


### Misión R04-N02-M2 · El hero con la mascota

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá un hero donde la imagen de **Gheco** (`/img/cursos/html/gheco-512.webp`) va **arriba** en el celular y **a la derecha** en la compu (`lg:order-2`).

#### Criterio de aprobación

- En *Celular* la imagen va arriba; en *Compu*, a la derecha del texto.
- El cambio se hace con `order` (no repitiendo la imagen).
- La imagen tiene un `alt` que la describe.

#### Cómo debe quedar

celular: capturas/R04-N02-M2-celular.webp
compu: capturas/R04-N02-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El hero con la mascota</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>Hero con la mascota</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <body class="p-4">
    <!-- En el celular la imagen va arriba; desde lg, a la derecha (order) -->
    <section aria-labelledby="t" class="tarjeta mx-auto grid max-w-5xl items-center gap-6 lg:grid-cols-2">
      <img src="/img/cursos/html/gheco-512.webp" alt="Gheco, el gecko de GhecoSoft, señalando hacia arriba" width="512" height="512" class="mx-auto w-48 rounded-full shadow-brillo sm:w-64 lg:order-2 lg:w-80">
      <div>
        <h1 id="t" class="text-3xl font-bold lg:text-5xl">Conocé a <span class="texto-neon text-neon">Gheco</span></h1>
        <p class="mt-3 text-slate-400">Tu guía en cada nodo del árbol de habilidades.</p>
        <a href="#" class="btn btn-primario mt-6">Empezar</a>
      </div>
    </section>
  </body>
</html>
```


### Encargo R04-N02-E1 · El hero del gimnasio

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Un gimnasio quiere su hero con un formulario "Quiero mi clase", apilado en el celular y en dos columnas en la compu.

#### Criterio de aprobación

- Apilado en *Celular*, dos columnas en *Compu*.
- El formulario tiene sus `label`.

#### Cómo debe quedar

celular: capturas/R04-N02-E1-celular.webp
compu: capturas/R04-N02-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El hero del gimnasio</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>Gimnasio Faro</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <body class="bg-zinc-950 text-zinc-100">
    <section aria-labelledby="t" class="mx-auto grid max-w-6xl gap-6 p-4 lg:grid-cols-[1.4fr_1fr] lg:items-center lg:py-16">
      <div>
        <p class="text-sm font-bold tracking-widest text-lime-400 uppercase">Primera clase gratis</p>
        <h1 id="t" class="mt-2 text-4xl font-black lg:text-6xl">Entrená en el Gimnasio Faro</h1>
        <p class="mt-3 text-zinc-400">Musculación, funcional y natación, de 6 a 23.</p>
      </div>
      <form action="#" method="post" class="space-y-3 rounded-2xl bg-zinc-900 p-6">
        <label for="nombre" class="block text-sm">Nombre</label>
        <input id="nombre" name="nombre" type="text" required autocomplete="name" class="w-full rounded-lg bg-zinc-800 px-3 py-2 focus:ring-2 focus:ring-lime-400 focus:outline-none">
        <label for="tel" class="block text-sm">Teléfono</label>
        <input id="tel" name="tel" type="tel" required autocomplete="tel" class="w-full rounded-lg bg-zinc-800 px-3 py-2 focus:ring-2 focus:ring-lime-400 focus:outline-none">
        <button type="submit" class="w-full rounded-lg bg-lime-400 py-3 font-bold text-zinc-950 hover:bg-lime-300">Quiero mi clase</button>
      </form>
    </section>
  </body>
</html>
```

## R04-N03 · Los vidrios de las rutas

```meta
tipo: tema
padre: R04-N02
precio: 10
criatura: orc
temas: css.grid
usa: css.frameworks, html.formularios
```

### Crónica

Debajo del panel central van los vidrios de las rutas: ocho cursos, cada uno con su color. El violeta de los Artífices, el verde del Valle, el oro del Imperio. En la cabaña tienen que verse de a uno; en el castillo, de a cuatro.

Teo propone un noveno color «para que quede más alegre». —Y cuidado con los filtros de arriba —advierte {mentor}—: son justo el escondite favorito del orco. No pueden empujar la pared hacia afuera.

### Objetivos

Armar la sección de **cursos**: encabezado con título y filtros, y una grilla de tarjetas que pasa de 1 a 2 a 4 columnas, con todas las tarjetas de la misma altura y los botones alineados abajo.

### Antes de empezar

- Etapa 19. Grid responsive («Responsive con Tailwind»), filtros con `has-checked` («Estados y transiciones»), tarjeta del kit («Componentes»).

### Explicación

#### El encabezado
`flex flex-wrap items-end justify-between`: en la computadora, título a la izquierda y filtros a la derecha; en el celular, los filtros bajan solos (`flex-wrap`).

Los filtros en el celular **no** pasan de línea: van en una fila con **scroll horizontal propio** (`overflow-x-auto` en el contenedor, `shrink-0` en cada chip). En `lg` vuelven a acomodarse en varias líneas (`lg:flex-wrap lg:overflow-visible`).

#### Dos trampas reales que aparecieron al armar esta sección
Al mirar la página en el celular, apareció scroll horizontal. Dos culpables:

1. **Un `fieldset` no se achica.** Por defecto tiene `min-width: min-content`: mide lo que miden todos los chips juntos, aunque tenga `overflow-x-auto`. Solución: `w-full min-w-0`.
2. **Los radios `sr-only` se escapan.** `sr-only` usa `position: absolute`, que se ubica respecto del primer ancestro **posicionado**. Como el `fieldset` no lo era, los radios quedaban fuera del recorte del scroll y estiraban la página. Solución: `relative` en el `fieldset`.

#### La grilla y las tarjetas
- `grid gap-4 sm:grid-cols-2 lg:grid-cols-4`.
- En una fila de la grilla, todas las celdas miden lo mismo de alto. Para que el progreso y el botón queden **siempre abajo** aunque una descripción sea más larga: la tarjeta es `flex flex-col` y el bloque de progreso lleva `mt-auto` (empuja todo lo de abajo hacia el fondo).
- La tarjeta activa (C++) se distingue con `border-neon/60 shadow-brillo` y botón primario; las demás, botón secundario.
- Cada curso tiene su color (violeta, esmeralda, oro…) en la etiqueta, el contador y la barra; el XP siempre en cian.

#### Cómo se ve el ejemplo

Tocá *Celular* y *Compu* en la vista previa: . Celular: el título con "DIRECTORIO CURRICULAR · 23 módulos", los filtros en una fila que se desliza y las ocho tarjetas una abajo de la otra. Computadora: filtros a la derecha del título y dos filas de cuatro tarjetas, con las barras y los botones alineados. Igual a la sección de esta plataforma.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GhecoSoft-Code · Etapa: Rutas de entrenamiento</title>
    <meta name="description" content="Aprendé a programar avanzando por tu árbol de habilidades: C++, SDL3, OpenGL, WebAssembly y más.">
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <!-- pb-20: lugar para la barra inferior del celular; desde lg no hay barra -->
  <body class="pb-20 lg:pb-0">
    <!-- SECCION:salto -->
    <!-- Enlace de salto: invisible hasta que recibe el foco con Tab -->
    <a href="#contenido" class="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 focus:rounded-lg focus:bg-neon focus:px-4 focus:py-2 focus:text-fondo">Saltar al contenido</a>
    <!-- /SECCION:salto -->

    <!-- SECCION:cabecera -->
    <!-- ===== CABECERA ===== -->
    <header class="sticky top-0 z-40 border-b border-borde bg-fondo/85 backdrop-blur">
      <div class="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3">
        <!-- Marca: logo con su nivel + nombre + estado -->
        <a href="#" class="flex items-center gap-3">
          <span class="relative shrink-0">
            <img src="/img/cursos/html/gheco-logo.webp" alt="" width="44" height="44" class="size-11 rounded-xl ring-1 ring-neon/50">
            <span class="absolute -bottom-1.5 left-1/2 -translate-x-1/2 rounded bg-violet-600 px-1 font-mono text-[9px] leading-tight font-bold text-white lg:hidden">LV.14</span>
          </span>
          <span>
            <span class="block font-display text-lg leading-tight font-bold whitespace-nowrap">GhecoSoft <span class="text-neon">-Code</span></span>
            <span class="flex items-center gap-1.5 font-mono text-[10px] tracking-widest text-slate-400 uppercase">
              <span class="size-1.5 animate-latido rounded-full bg-emerald-400"></span> System online
            </span>
          </span>
        </a>

        <!-- Menu principal: solo desde lg (en el celular esta la barra de abajo) -->
        <nav aria-label="Principal" class="hidden items-center gap-1 text-sm whitespace-nowrap lg:flex">
          <a href="#rutas" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Cursos</a>
          <a href="#rutas" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Rutas</a>
          <a href="#fama" aria-current="page" class="rounded-lg border border-neon/50 bg-neon/10 px-3 py-2 text-neon">🏆 Top 10<span class="hidden xl:inline"> alumnos</span></a>
          <a href="#" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Skill Tree</a>
          <a href="#boveda" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Bóveda<span class="hidden xl:inline"> de tokens</span></a>
        </nav>

        <!-- Estadisticas del jugador -->
        <div class="flex items-center gap-2 font-mono text-xs whitespace-nowrap">
          <span class="hidden items-center gap-2 rounded-lg border border-borde px-2.5 py-1.5 xl:flex">
            LVL 14
            <span class="h-1.5 w-12 overflow-hidden rounded-full bg-borde"><span class="block h-full w-2/3 bg-violet-500"></span></span>
          </span>
          <span class="rounded-lg border border-borde px-2.5 py-1.5"><span class="text-neon">⚡ 1.450</span><span class="hidden lg:inline"> ESC</span><span class="lg:hidden"> · <span class="text-fuego">🔥 12</span></span></span>
          <span class="hidden rounded-lg border border-fuego/40 px-2.5 py-1.5 text-fuego lg:inline">🔥 12 días</span>
          <img src="/img/cursos/html/heroe-avatar.webp" alt="Tu perfil" width="36" height="36" class="hidden size-9 rounded-full border-2 border-neon object-cover lg:block">
        </div>
      </div>
    </header>
    <!-- /SECCION:cabecera -->

    <main id="contenido" class="mx-auto max-w-7xl space-y-16 px-4 py-6 lg:space-y-24 lg:py-10">
      <!-- Lo que falta se agrega en las proximas etapas del proyecto -->
      <p class="rounded-xl border border-dashed border-borde p-6 text-center font-mono text-sm text-slate-500">Próximas secciones: prácticas siguientes del proyecto (hasta la 22).</p>
      <!-- SECCION:hero -->
      <!-- ===== HERO + LOGIN ===== -->
      <section aria-labelledby="titulo-hero" class="overflow-hidden rounded-3xl border border-borde bg-panel lg:grid lg:grid-cols-[1.5fr_1fr]">
        <!-- Lado izquierdo: ilustracion de fondo + texto -->
        <div class="fondo-cuadricula relative isolate flex min-h-[36rem] flex-col justify-end p-6 sm:min-h-[30rem] sm:p-10 lg:min-h-[34rem]">
          <img src="/img/cursos/html/heroe-448.webp" srcset="/img/cursos/html/heroe-448.webp 448w, /img/cursos/html/heroe-896.webp 896w" sizes="(min-width: 64rem) 30rem, 70vw" alt="" width="448" height="600" class="absolute top-0 right-0 -z-10 h-full w-auto max-w-none object-cover opacity-80">
          <!-- Degrade para que el texto se lea sobre la imagen -->
          <div class="absolute inset-0 -z-10 bg-linear-to-t from-panel from-30% via-panel/70 to-transparent lg:bg-linear-to-r lg:via-panel/70 lg:to-transparent"></div>

          <p class="etiqueta-mono inline-flex w-fit items-center gap-2 rounded-full border border-neon/40 bg-fondo/60 px-3 py-1 text-[10px] text-neon">
            <span class="size-1.5 animate-latido rounded-full bg-neon"></span> Plataforma de cursos <span class="hidden sm:inline">· Temporada 04</span>
          </p>
          <h1 id="titulo-hero" class="mt-4 max-w-xl text-3xl leading-tight font-bold sm:text-4xl lg:text-5xl">
            Aprendé a programar avanzando por tu <span class="texto-neon text-neon">árbol de habilidades</span>.
          </h1>
          <p class="mt-3 max-w-lg text-slate-300 lg:text-lg">
            Compilá algoritmos reales, desbloqueá nodos tecnológicos de bajo nivel (C++, SDL3, OpenGL, WASM) y competí por el rango Supremo del salón de la fama.
          </p>
          <div class="mt-6 flex gap-3">
            <a href="#rutas" class="btn btn-primario flex-1 sm:flex-none">▷ Continuar campaña</a>
            <a href="#fama" class="btn btn-secundario"><span class="sm:hidden">Top 10</span><span class="hidden sm:inline">Ver leaderboard <span class="ml-1 rounded bg-neon/10 px-1.5 text-xs">Top 10</span></span></a>
          </div>
        </div>

        <!-- Lado derecho: el portal (login). En el celular va debajo -->
        <div class="border-t border-borde bg-fondo/40 p-6 sm:p-10 lg:border-t-0 lg:border-l">
          <p class="etiqueta-mono text-center text-[10px] text-slate-500">Portal del desarrollador</p>
          <h2 class="mt-2 text-center text-2xl font-bold">Entrá a tu cuenta</h2>
          <p class="mt-1 text-center text-sm text-slate-400">Ingresá tu usuario y contraseña para retomar tu entrenamiento.</p>

          <form action="#" method="post" class="mt-6 space-y-4">
            <button type="button" class="btn w-full border border-borde bg-panel py-2.5 text-sm text-slate-200 hover:border-neon/60">🔑 Entrar con llave de acceso (Passkey)</button>
            <p class="flex items-center gap-3 font-mono text-[10px] tracking-widest text-slate-500 uppercase" aria-hidden="true">
              <span class="h-px flex-1 bg-borde"></span> o seguí con tu email <span class="h-px flex-1 bg-borde"></span>
            </p>
            <div class="space-y-1">
              <label for="usuario" class="etiqueta-mono block text-[10px] text-slate-400">Usuario o email</label>
              <input id="usuario" name="usuario" type="text" autocomplete="username" required placeholder="cliente" class="peer w-full rounded-lg border border-borde bg-fondo px-3 py-2.5 placeholder:text-slate-600 focus:border-neon focus:ring-2 focus:ring-neon/30 focus:outline-none user-invalid:border-rose-400">
              <p class="hidden text-xs text-rose-400 peer-user-invalid:block">Completá tu usuario o email.</p>
            </div>
            <div class="space-y-1">
              <div class="flex items-baseline justify-between">
                <label for="clave" class="etiqueta-mono text-[10px] text-slate-400">Contraseña</label>
                <a href="#" class="text-xs text-neon hover:underline">¿Olvidaste tu contraseña?</a>
              </div>
              <input id="clave" name="clave" type="password" autocomplete="current-password" required minlength="8" class="w-full rounded-lg border border-borde bg-fondo px-3 py-2.5 focus:border-neon focus:ring-2 focus:ring-neon/30 focus:outline-none">
            </div>
            <label class="flex items-center gap-2 text-sm text-slate-300">
              <input type="checkbox" name="recordarme" checked class="size-4 accent-cyan-400"> Recordarme en esta terminal
            </label>
            <button type="submit" class="btn btn-primario w-full tracking-wider uppercase">Entrar a la terminal →</button>
          </form>
          <p class="mt-4 text-center text-sm text-slate-400">¿No tenés cuenta aún? <a href="#" class="font-semibold text-neon hover:underline">Registrate gratis</a></p>

          <!-- Mision en curso -->
          <div class="mt-6 flex items-center gap-3 rounded-xl border border-borde bg-panel p-3">
            <span class="size-2 shrink-0 rounded-full bg-emerald-400"></span>
            <p class="min-w-0 flex-1 text-xs">
              <span class="etiqueta-mono block text-[10px] text-neon">Misión en curso</span>
              <span class="block truncate text-slate-300">04-C++ Moderno: Smart Pointers</span>
            </p>
            <span class="rounded-md bg-neon/10 px-2 py-1 font-mono text-xs text-neon">75%</span>
          </div>
        </div>
      </section>
      <!-- /SECCION:hero -->

      <!-- SECCION:rutas -->
      <!-- ===== RUTAS DE ENTRENAMIENTO ===== -->
      <section id="rutas" aria-labelledby="titulo-rutas" class="scroll-mt-24">
        <div class="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p class="flex items-center gap-2">
              <span class="etiqueta-mono rounded border border-neon/40 px-2 py-0.5 text-[10px] text-neon">Directorio curricular</span>
              <span class="font-mono text-xs text-slate-500">23 módulos</span>
            </p>
            <h2 id="titulo-rutas" class="mt-2 text-2xl font-bold lg:text-3xl">Rutas de Entrenamiento</h2>
          </div>
          <!-- Filtros: radios escondidos (sr-only) + has-checked -->
          <fieldset class="relative flex w-full min-w-0 gap-2 overflow-x-auto pb-1 lg:w-auto lg:flex-wrap lg:overflow-visible">
            <legend class="sr-only">Filtrar rutas</legend>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only" checked> Todos (23)</label>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only"> Bajo nivel / C++</label>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only"> Gráficos &amp; Shaders</label>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only"> Desarrollo web</label>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only"> Backend &amp; Cloud</label>
          </fieldset>
        </div>

        <!-- 1 columna → 2 (sm) → 4 (lg) -->
        <div class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <article class="tarjeta flex flex-col gap-3 border-neon/60 shadow-brillo">
            <div class="flex items-center justify-between"><span class="rounded bg-neon/10 px-2 py-0.5 font-mono text-xs text-neon">MOD-04</span><span class="font-mono text-xs text-emerald-400">Core activo</span></div>
            <h3 class="text-lg font-bold">C++ Moderno &amp; Videojuegos</h3>
            <p class="text-sm text-slate-400">Gestión de memoria, RAII, Smart Pointers, conceptos de C++20 y ciclo de vida de motores.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-neon">18 / 24</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de C++ Moderno" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-3/4 rounded-full bg-neon"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+350 XP <span class="text-xs text-slate-500">| Intermedio</span></span><a href="#" class="btn btn-primario px-3 py-1 text-xs">Continuar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-violet-400/10 px-2 py-0.5 font-mono text-xs text-violet-300">MOD-06</span><span class="font-mono text-xs text-slate-500">Pipeline 2D/3D</span></div>
            <h3 class="text-lg font-bold">SDL3 &amp; Game Loops</h3>
            <p class="text-sm text-slate-400">Renderizado acelerado por hardware, buffers de audio y gestión de ventanas en tiempo real.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-violet-300">10 / 22</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de SDL3" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[45%] rounded-full bg-violet-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+420 XP <span class="text-xs text-slate-500">| Avanzado</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-emerald-400/10 px-2 py-0.5 font-mono text-xs text-emerald-300">MOD-10</span><span class="font-mono text-xs text-slate-500">Shader pipeline</span></div>
            <h3 class="text-lg font-bold">OpenGL 4.6 &amp; GLSL</h3>
            <p class="text-sm text-slate-400">Vertex y fragment shaders, texturas, transformaciones e iluminación Phong.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-emerald-300">3 / 16</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de OpenGL" aria-valuenow="19" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[19%] rounded-full bg-emerald-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+500 XP <span class="text-xs text-slate-500">| Experto</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-oro/10 px-2 py-0.5 font-mono text-xs text-oro">MOD-13</span><span class="font-mono text-xs text-slate-500">Bajo nivel web</span></div>
            <h3 class="text-lg font-bold">WebAssembly &amp; Emscripten</h3>
            <p class="text-sm text-slate-400">Compilación nativa de C/C++ directo al navegador con velocidad cercana al metal.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-oro">5 / 19</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de WebAssembly" aria-valuenow="26" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[26%] rounded-full bg-oro"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+380 XP <span class="text-xs text-slate-500">| Avanzado</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-fuego/10 px-2 py-0.5 font-mono text-xs text-fuego">MOD-17</span><span class="font-mono text-xs text-slate-500">Data &amp; scripting</span></div>
            <h3 class="text-lg font-bold">Python &amp; Algoritmos</h3>
            <p class="text-sm text-slate-400">Estructuras de datos, resolución algorítmica y automatización de procesos.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-fuego">14 / 20</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de Python" aria-valuenow="70" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[70%] rounded-full bg-fuego"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+290 XP <span class="text-xs text-slate-500">| Inicial</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-rose-400/10 px-2 py-0.5 font-mono text-xs text-rose-300">MOD-20</span><span class="font-mono text-xs text-slate-500">Enterprise core</span></div>
            <h3 class="text-lg font-bold">Spring Boot &amp; Java Cloud</h3>
            <p class="text-sm text-slate-400">Arquitectura en capas, JPA, endpoints REST seguros y contenedores Docker.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-rose-300">16 / 24</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de Spring Boot" aria-valuenow="66" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-2/3 rounded-full bg-rose-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+310 XP <span class="text-xs text-slate-500">| Avanzado</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-sky-400/10 px-2 py-0.5 font-mono text-xs text-sky-300">MOD-23</span><span class="font-mono text-xs text-slate-500">Tipado estricto</span></div>
            <h3 class="text-lg font-bold">TypeScript Pro</h3>
            <p class="text-sm text-slate-400">Genéricos avanzados, decoradores, tipos condicionales y diseño de bibliotecas.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-sky-300">12 / 16</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de TypeScript" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-3/4 rounded-full bg-sky-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+290 XP <span class="text-xs text-slate-500">| Intermedio</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-pink-400/10 px-2 py-0.5 font-mono text-xs text-pink-300">MOD-16</span><span class="font-mono text-xs text-slate-500">Game dev web</span></div>
            <h3 class="text-lg font-bold">Phaser Engine &amp; JS</h3>
            <p class="text-sm text-slate-400">Física arcade, spritesheets, colisiones y publicación web de minijuegos.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-pink-300">8 / 15</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de Phaser" aria-valuenow="53" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[53%] rounded-full bg-pink-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+260 XP <span class="text-xs text-slate-500">| Inicial</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>
        </div>
      </section>
      <!-- /SECCION:rutas -->


    </main>

    <!-- SECCION:pie -->
    <!-- ===== PIE ===== -->
    <footer class="border-t border-borde">
      <div class="mx-auto grid max-w-7xl gap-6 px-4 py-8 text-sm md:grid-cols-[2fr_1fr_1fr] md:items-center">
        <div class="flex items-center gap-3">
          <img src="/img/cursos/html/gheco-logo.webp" alt="" width="36" height="36" class="size-9 rounded-lg">
          <p><span class="font-display font-bold">GhecoSoft-Code Platform</span><br><span class="text-xs text-slate-500">Formación avanzada en bajo nivel, motores de videojuegos y compilación real.</span></p>
        </div>
        <ul class="space-y-1 font-mono text-xs text-slate-400">
          <li><span class="text-emerald-400">●</span> Cloud Compiler Clang 18: online</li>
          <li><span class="text-emerald-400">●</span> GCC 14 / Emscripten: 99.98% uptime</li>
        </ul>
        <p class="font-mono text-xs text-slate-500 md:text-right">© 2026 GhecoSoft-Code.<br>Obsidian Design Protocol v4.2</p>
      </div>
    </footer>
    <!-- /SECCION:pie -->

    <!-- SECCION:barra -->
    <!-- ===== BARRA INFERIOR (solo celular y tablet) ===== -->
    <nav aria-label="Secciones" class="fixed inset-x-0 bottom-0 z-40 border-t border-borde bg-panel/95 backdrop-blur lg:hidden">
      <div class="mx-auto flex max-w-lg">
        <a href="#rutas" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">🗺</span>Campañas</a>
        <a href="#" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">📖</span>Lecciones</a>
        <a href="#fama" aria-current="page" class="my-1 flex flex-1 flex-col items-center gap-0.5 rounded-xl border border-neon/50 bg-neon/10 py-1 text-[11px] text-neon"><span aria-hidden="true" class="text-lg">⚔</span>Arena</a>
        <a href="#" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">🌳</span>Árbol</a>
      </div>
    </nav>
    <!-- /SECCION:barra -->
  </body>
</html>
```

### ¿Para qué sirve?

Los catálogos con filtros están en todas las tiendas online, los servicios de streaming y las plataformas de cursos. Las dos trampas de este nodo —el `fieldset` que no se achica y los radios que se escapan— son problemas reales que aparecieron al armar esta misma página.

### Errores habituales

**Orco del Desborde: `fieldset` que no se achica** y **radios `sr-only` que se escapan** (ver arriba). El detector imprime qué elemento llega más allá del borde:
```
FALLO 22-Proyecto-Plataforma: scroll horizontal a 390px:
  <fieldset class="flex gap-2 overflow-x-auto pb-1 lg:flex-wrap lg:overflow-vis"> llega a 426px
```
**Ogro: botones desalineados** entre tarjetas: falta `flex flex-col` en la tarjeta o `mt-auto` en el bloque de abajo.

### Prueba del sello

#### ¿Por qué un `fieldset` con `overflow-x-auto` puede igual desbordar la página?

Porque un `fieldset` tiene, de fábrica, `min-width: min-content`: mide lo que miden todos los chips juntos, y su scroll nunca se activa. Se arregla con `w-full min-w-0`.

#### ¿Qué hace `mt-auto` dentro de una tarjeta `flex flex-col`?

Usa todo el espacio libre como margen de arriba: empuja ese bloque (y todo lo que sigue) **hasta el fondo** de la tarjeta. Así el progreso y el botón quedan alineados aunque las descripciones tengan distinto largo.

#### ¿Cómo se filtra con CSS sin JavaScript? ¿Qué limitación tiene frente a JavaScript?

Con radios y `:has()`: el contenedor es `group` y cada tarjeta que no es de la categoría tiene `group-has-[#f-graf:checked]:hidden`. La limitación: cada filtro hay que escribirlo a mano en el HTML; no se puede buscar por texto, combinar filtros libremente ni traer datos nuevos. Eso es lo que hace JavaScript.

### Misión R04-N03-M1 · El curso bloqueado

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Armá una tarjeta de curso **bloqueada**: apagada (`opacity-60 grayscale`), con un candado y un **botón desactivado** en vez de un enlace.

#### Criterio de aprobación

- La tarjeta se ve apagada (`opacity-60 grayscale`) y tiene un candado.
- Usa un `button` con `disabled` (no un enlace) y el texto dice por qué está bloqueada.

#### Cómo debe quedar

celular: capturas/R04-N03-M1-celular.webp
compu: capturas/R04-N03-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El curso bloqueado</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>Tarjeta bloqueada</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <body class="p-4">
    <div class="grid max-w-3xl gap-4 sm:grid-cols-2">
      <article class="tarjeta flex flex-col gap-3">
        <div class="flex items-center justify-between"><span class="rounded bg-neon/10 px-2 py-0.5 font-mono text-xs text-neon">MOD-04</span><span class="font-mono text-xs text-emerald-400">Disponible</span></div>
        <h1 class="text-lg font-bold">C++ Moderno</h1>
        <a href="#" class="btn btn-primario mt-auto px-3 py-1 text-xs">Continuar</a>
      </article>
      <!-- Bloqueada: apagada, con candado, y el boton no es un enlace -->
      <article class="tarjeta relative flex flex-col gap-3 opacity-60 grayscale">
        <div class="flex items-center justify-between"><span class="rounded bg-borde px-2 py-0.5 font-mono text-xs text-slate-400">MOD-30</span><span class="font-mono text-xs text-slate-400">🔒 Bloqueado</span></div>
        <h2 class="text-lg font-bold">Vulkan &amp; Ray Tracing</h2>
        <p class="text-sm text-slate-400">Se desbloquea al completar OpenGL 4.6.</p>
        <button type="button" disabled class="btn btn-secundario mt-auto cursor-not-allowed px-3 py-1 text-xs">Requiere MOD-10</button>
      </article>
    </div>
  </body>
</html>
```


### Misión R04-N03-M2 · Los filtros que filtran

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Hacé que los chips de filtro **oculten de verdad** las tarjetas, sin JavaScript: `group` en el contenedor y `group-has-[#f-graf:checked]:hidden` en cada tarjeta que **no** es de gráficos.

#### Criterio de aprobación

- Los filtros son radios reales con su `label`.
- Al elegir "Gráficos" se ocultan las demás tarjetas, sin JavaScript.
- En *Celular* los chips no desbordan la página.

#### Cómo debe quedar

celular: capturas/R04-N03-M2-celular.webp
compu: capturas/R04-N03-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Los filtros que filtran</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>Filtros que filtran sin JavaScript</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <body class="p-4">
    <!-- group en el contenedor: las tarjetas preguntan "¿el grupo TIENE tal radio marcado?" -->
    <div class="group mx-auto max-w-4xl space-y-4">
      <fieldset class="flex flex-wrap gap-2">
        <legend class="sr-only">Filtrar rutas</legend>
        <label class="chip cursor-pointer has-checked:bg-neon has-checked:text-fondo"><input id="f-todos" type="radio" name="f" class="sr-only" checked> Todos</label>
        <label class="chip cursor-pointer has-checked:bg-neon has-checked:text-fondo"><input id="f-bajo" type="radio" name="f" class="sr-only"> Bajo nivel</label>
        <label class="chip cursor-pointer has-checked:bg-neon has-checked:text-fondo"><input id="f-graf" type="radio" name="f" class="sr-only"> Gráficos</label>
        <label class="chip cursor-pointer has-checked:bg-neon has-checked:text-fondo"><input id="f-web" type="radio" name="f" class="sr-only"> Web</label>
      </fieldset>
      <div class="grid gap-3 sm:grid-cols-2">
        <article class="tarjeta group-has-[#f-graf:checked]:hidden group-has-[#f-web:checked]:hidden">C++ Moderno · bajo nivel</article>
        <article class="tarjeta group-has-[#f-bajo:checked]:hidden group-has-[#f-web:checked]:hidden">SDL3 · gráficos</article>
        <article class="tarjeta group-has-[#f-bajo:checked]:hidden group-has-[#f-web:checked]:hidden">OpenGL · gráficos</article>
        <article class="tarjeta group-has-[#f-graf:checked]:hidden group-has-[#f-bajo:checked]:hidden">TypeScript · web</article>
      </div>
    </div>
  </body>
</html>
```


### Encargo R04-N03-E1 · El catálogo de la librería

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Una librería quiere su catálogo: **1 → 2 → 3 → 4** columnas, y el precio **siempre al pie** de cada tarjeta aunque el título ocupe dos líneas.

#### Criterio de aprobación

- Pasa de 1 a 4 columnas con prefijos.
- El precio queda abajo en todas las tarjetas (`flex flex-col` + `mt-auto`).

#### Cómo debe quedar

celular: capturas/R04-N03-E1-celular.webp
compu: capturas/R04-N03-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El catálogo de la librería</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>Catálogo de una librería</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <body class="bg-amber-50 p-4 text-stone-800">
    <main class="mx-auto max-w-6xl">
      <h1 class="text-2xl font-bold lg:text-4xl">Librería El Faro</h1>
      <div class="mt-6 grid gap-4 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4">
        <article class="flex flex-col rounded-xl bg-white p-4 shadow-sm"><p class="text-xs text-stone-500">Novela</p><h2 class="font-semibold">Rayuela</h2><p class="mt-auto pt-3 font-bold">$18000</p></article>
        <article class="flex flex-col rounded-xl bg-white p-4 shadow-sm"><p class="text-xs text-stone-500">Ensayo</p><h2 class="font-semibold">Breve historia del tiempo, edición ilustrada y ampliada</h2><p class="mt-auto pt-3 font-bold">$25000</p></article>
        <article class="flex flex-col rounded-xl bg-white p-4 shadow-sm"><p class="text-xs text-stone-500">Infantil</p><h2 class="font-semibold">El Principito</h2><p class="mt-auto pt-3 font-bold">$9000</p></article>
        <article class="flex flex-col rounded-xl bg-white p-4 shadow-sm"><p class="text-xs text-stone-500">Poesía</p><h2 class="font-semibold">Veinte poemas de amor</h2><p class="mt-auto pt-3 font-bold">$11000</p></article>
      </div>
    </main>
  </body>
</html>
```

## R04-N04 · El Hall of Fame

```meta
tipo: tema
padre: R04-N03
precio: 10
criatura: orc
temas: html.listas-tablas, css.responsive
usa: css.grid, css.frameworks
```

### Crónica

En lo más alto del ventanal van los campeones de la **Liga Obsidiana**. El podio tiene que verse imponente en el castillo y entrar igual en la ventanita de la cabaña. Y la tabla de diez filas… en el celular no entra.

—Los mismos datos pueden tener **dos formas** —dice {mentor}. Y después, más bajito—: Cuando termines, quiero pedirte algo para mí. Siempre quise un vitral con todas las líderes del mundo juntas.

### Objetivos

Construir el **podio** (tres columnas que se adaptan de tamaño, el primero más alto) y mostrar los puestos 4 a 10 como **lista de filas en el celular** y como **tabla en la computadora**, con la fila del usuario resaltada.

### Antes de empezar

- Etapa 20. Tablas accesibles («Tablas»), Grid («Grid», «Flex y Grid con Tailwind»), responsive («Responsive con Tailwind»).

### Explicación

#### El podio
- `grid grid-cols-[1fr_1.15fr_1fr] items-end`: **siempre** tres columnas (también en el celular, como en esta plataforma), el centro un poco más ancho y todos apoyados abajo. El orden en el HTML es 2-1-3 para que se vea así.
- El 1.º es más alto por el padding (`pt-10 pb-6`) y por contenido extra; tiene borde dorado, sombra dorada y un degradé desde arriba (`bg-linear-to-b from-oro/15 to-panel`).
- La medalla y la corona salen por arriba del borde: `relative` en la tarjeta y `absolute -top-4` en la medalla.
- En el celular hay poco lugar: los nombres se cortan (`w-full truncate`) y las etiquetas de especialidad y la racha aparecen recién en `sm`/`lg` (`hidden sm:block`, `hidden lg:flex`). El avatar crece con `sm:size-16`/`sm:size-20`.

#### Lista o tabla
| | Celular (`md:hidden`) | Computadora (`hidden md:block`) |
|---|---|---|
| etiqueta | `<ol start="4">` | `<table>` con `caption`, `th scope` |
| columnas | puesto · avatar · nombre (y especialidad debajo) · puntos | rank · desarrollador · especialidad · tendencia · racha · puntos |

Los datos están **dos veces** en el HTML, pero el lector de pantalla lee **uno** solo: lo que tiene `display: none` no existe para él. La desventaja es mantener dos copias (en un proyecto real, las dos salen de los mismos datos con JavaScript o una plantilla del servidor). La alternativa —una sola tabla con scroll horizontal— es la misión 2.

- `divide-y divide-borde` en el `tbody`: una línea entre filas sin tocar cada `tr`.
- La fila del usuario: fondo `bg-neon/5`, texto cian y "(vos)".

#### Cómo se ve el ejemplo

Tocá *Celular* y *Compu* en la vista previa: . Celular: el título con el cierre de temporada, el podio de tres con el
1.º dorado y más alto, y siete filas (la de @GhecoDev con el logo de Gheco y borde cian). Computadora: el podio grande con especialidades y rachas, y la tabla de seis columnas.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GhecoSoft-Code · Etapa: Hall of Fame</title>
    <meta name="description" content="Aprendé a programar avanzando por tu árbol de habilidades: C++, SDL3, OpenGL, WebAssembly y más.">
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <!-- pb-20: lugar para la barra inferior del celular; desde lg no hay barra -->
  <body class="pb-20 lg:pb-0">
    <!-- SECCION:salto -->
    <!-- Enlace de salto: invisible hasta que recibe el foco con Tab -->
    <a href="#contenido" class="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 focus:rounded-lg focus:bg-neon focus:px-4 focus:py-2 focus:text-fondo">Saltar al contenido</a>
    <!-- /SECCION:salto -->

    <!-- SECCION:cabecera -->
    <!-- ===== CABECERA ===== -->
    <header class="sticky top-0 z-40 border-b border-borde bg-fondo/85 backdrop-blur">
      <div class="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3">
        <!-- Marca: logo con su nivel + nombre + estado -->
        <a href="#" class="flex items-center gap-3">
          <span class="relative shrink-0">
            <img src="/img/cursos/html/gheco-logo.webp" alt="" width="44" height="44" class="size-11 rounded-xl ring-1 ring-neon/50">
            <span class="absolute -bottom-1.5 left-1/2 -translate-x-1/2 rounded bg-violet-600 px-1 font-mono text-[9px] leading-tight font-bold text-white lg:hidden">LV.14</span>
          </span>
          <span>
            <span class="block font-display text-lg leading-tight font-bold whitespace-nowrap">GhecoSoft <span class="text-neon">-Code</span></span>
            <span class="flex items-center gap-1.5 font-mono text-[10px] tracking-widest text-slate-400 uppercase">
              <span class="size-1.5 animate-latido rounded-full bg-emerald-400"></span> System online
            </span>
          </span>
        </a>

        <!-- Menu principal: solo desde lg (en el celular esta la barra de abajo) -->
        <nav aria-label="Principal" class="hidden items-center gap-1 text-sm whitespace-nowrap lg:flex">
          <a href="#rutas" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Cursos</a>
          <a href="#rutas" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Rutas</a>
          <a href="#fama" aria-current="page" class="rounded-lg border border-neon/50 bg-neon/10 px-3 py-2 text-neon">🏆 Top 10<span class="hidden xl:inline"> alumnos</span></a>
          <a href="#" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Skill Tree</a>
          <a href="#boveda" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Bóveda<span class="hidden xl:inline"> de tokens</span></a>
        </nav>

        <!-- Estadisticas del jugador -->
        <div class="flex items-center gap-2 font-mono text-xs whitespace-nowrap">
          <span class="hidden items-center gap-2 rounded-lg border border-borde px-2.5 py-1.5 xl:flex">
            LVL 14
            <span class="h-1.5 w-12 overflow-hidden rounded-full bg-borde"><span class="block h-full w-2/3 bg-violet-500"></span></span>
          </span>
          <span class="rounded-lg border border-borde px-2.5 py-1.5"><span class="text-neon">⚡ 1.450</span><span class="hidden lg:inline"> ESC</span><span class="lg:hidden"> · <span class="text-fuego">🔥 12</span></span></span>
          <span class="hidden rounded-lg border border-fuego/40 px-2.5 py-1.5 text-fuego lg:inline">🔥 12 días</span>
          <img src="/img/cursos/html/heroe-avatar.webp" alt="Tu perfil" width="36" height="36" class="hidden size-9 rounded-full border-2 border-neon object-cover lg:block">
        </div>
      </div>
    </header>
    <!-- /SECCION:cabecera -->

    <main id="contenido" class="mx-auto max-w-7xl space-y-16 px-4 py-6 lg:space-y-24 lg:py-10">
      <!-- Lo que falta se agrega en las proximas etapas del proyecto -->
      <p class="rounded-xl border border-dashed border-borde p-6 text-center font-mono text-sm text-slate-500">Próximas secciones: prácticas siguientes del proyecto (hasta la 22).</p>
      <!-- SECCION:hero -->
      <!-- ===== HERO + LOGIN ===== -->
      <section aria-labelledby="titulo-hero" class="overflow-hidden rounded-3xl border border-borde bg-panel lg:grid lg:grid-cols-[1.5fr_1fr]">
        <!-- Lado izquierdo: ilustracion de fondo + texto -->
        <div class="fondo-cuadricula relative isolate flex min-h-[36rem] flex-col justify-end p-6 sm:min-h-[30rem] sm:p-10 lg:min-h-[34rem]">
          <img src="/img/cursos/html/heroe-448.webp" srcset="/img/cursos/html/heroe-448.webp 448w, /img/cursos/html/heroe-896.webp 896w" sizes="(min-width: 64rem) 30rem, 70vw" alt="" width="448" height="600" class="absolute top-0 right-0 -z-10 h-full w-auto max-w-none object-cover opacity-80">
          <!-- Degrade para que el texto se lea sobre la imagen -->
          <div class="absolute inset-0 -z-10 bg-linear-to-t from-panel from-30% via-panel/70 to-transparent lg:bg-linear-to-r lg:via-panel/70 lg:to-transparent"></div>

          <p class="etiqueta-mono inline-flex w-fit items-center gap-2 rounded-full border border-neon/40 bg-fondo/60 px-3 py-1 text-[10px] text-neon">
            <span class="size-1.5 animate-latido rounded-full bg-neon"></span> Plataforma de cursos <span class="hidden sm:inline">· Temporada 04</span>
          </p>
          <h1 id="titulo-hero" class="mt-4 max-w-xl text-3xl leading-tight font-bold sm:text-4xl lg:text-5xl">
            Aprendé a programar avanzando por tu <span class="texto-neon text-neon">árbol de habilidades</span>.
          </h1>
          <p class="mt-3 max-w-lg text-slate-300 lg:text-lg">
            Compilá algoritmos reales, desbloqueá nodos tecnológicos de bajo nivel (C++, SDL3, OpenGL, WASM) y competí por el rango Supremo del salón de la fama.
          </p>
          <div class="mt-6 flex gap-3">
            <a href="#rutas" class="btn btn-primario flex-1 sm:flex-none">▷ Continuar campaña</a>
            <a href="#fama" class="btn btn-secundario"><span class="sm:hidden">Top 10</span><span class="hidden sm:inline">Ver leaderboard <span class="ml-1 rounded bg-neon/10 px-1.5 text-xs">Top 10</span></span></a>
          </div>
        </div>

        <!-- Lado derecho: el portal (login). En el celular va debajo -->
        <div class="border-t border-borde bg-fondo/40 p-6 sm:p-10 lg:border-t-0 lg:border-l">
          <p class="etiqueta-mono text-center text-[10px] text-slate-500">Portal del desarrollador</p>
          <h2 class="mt-2 text-center text-2xl font-bold">Entrá a tu cuenta</h2>
          <p class="mt-1 text-center text-sm text-slate-400">Ingresá tu usuario y contraseña para retomar tu entrenamiento.</p>

          <form action="#" method="post" class="mt-6 space-y-4">
            <button type="button" class="btn w-full border border-borde bg-panel py-2.5 text-sm text-slate-200 hover:border-neon/60">🔑 Entrar con llave de acceso (Passkey)</button>
            <p class="flex items-center gap-3 font-mono text-[10px] tracking-widest text-slate-500 uppercase" aria-hidden="true">
              <span class="h-px flex-1 bg-borde"></span> o seguí con tu email <span class="h-px flex-1 bg-borde"></span>
            </p>
            <div class="space-y-1">
              <label for="usuario" class="etiqueta-mono block text-[10px] text-slate-400">Usuario o email</label>
              <input id="usuario" name="usuario" type="text" autocomplete="username" required placeholder="cliente" class="peer w-full rounded-lg border border-borde bg-fondo px-3 py-2.5 placeholder:text-slate-600 focus:border-neon focus:ring-2 focus:ring-neon/30 focus:outline-none user-invalid:border-rose-400">
              <p class="hidden text-xs text-rose-400 peer-user-invalid:block">Completá tu usuario o email.</p>
            </div>
            <div class="space-y-1">
              <div class="flex items-baseline justify-between">
                <label for="clave" class="etiqueta-mono text-[10px] text-slate-400">Contraseña</label>
                <a href="#" class="text-xs text-neon hover:underline">¿Olvidaste tu contraseña?</a>
              </div>
              <input id="clave" name="clave" type="password" autocomplete="current-password" required minlength="8" class="w-full rounded-lg border border-borde bg-fondo px-3 py-2.5 focus:border-neon focus:ring-2 focus:ring-neon/30 focus:outline-none">
            </div>
            <label class="flex items-center gap-2 text-sm text-slate-300">
              <input type="checkbox" name="recordarme" checked class="size-4 accent-cyan-400"> Recordarme en esta terminal
            </label>
            <button type="submit" class="btn btn-primario w-full tracking-wider uppercase">Entrar a la terminal →</button>
          </form>
          <p class="mt-4 text-center text-sm text-slate-400">¿No tenés cuenta aún? <a href="#" class="font-semibold text-neon hover:underline">Registrate gratis</a></p>

          <!-- Mision en curso -->
          <div class="mt-6 flex items-center gap-3 rounded-xl border border-borde bg-panel p-3">
            <span class="size-2 shrink-0 rounded-full bg-emerald-400"></span>
            <p class="min-w-0 flex-1 text-xs">
              <span class="etiqueta-mono block text-[10px] text-neon">Misión en curso</span>
              <span class="block truncate text-slate-300">04-C++ Moderno: Smart Pointers</span>
            </p>
            <span class="rounded-md bg-neon/10 px-2 py-1 font-mono text-xs text-neon">75%</span>
          </div>
        </div>
      </section>
      <!-- /SECCION:hero -->

      <!-- SECCION:rutas -->
      <!-- ===== RUTAS DE ENTRENAMIENTO ===== -->
      <section id="rutas" aria-labelledby="titulo-rutas" class="scroll-mt-24">
        <div class="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p class="flex items-center gap-2">
              <span class="etiqueta-mono rounded border border-neon/40 px-2 py-0.5 text-[10px] text-neon">Directorio curricular</span>
              <span class="font-mono text-xs text-slate-500">23 módulos</span>
            </p>
            <h2 id="titulo-rutas" class="mt-2 text-2xl font-bold lg:text-3xl">Rutas de Entrenamiento</h2>
          </div>
          <!-- Filtros: radios escondidos (sr-only) + has-checked -->
          <fieldset class="relative flex w-full min-w-0 gap-2 overflow-x-auto pb-1 lg:w-auto lg:flex-wrap lg:overflow-visible">
            <legend class="sr-only">Filtrar rutas</legend>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only" checked> Todos (23)</label>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only"> Bajo nivel / C++</label>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only"> Gráficos &amp; Shaders</label>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only"> Desarrollo web</label>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only"> Backend &amp; Cloud</label>
          </fieldset>
        </div>

        <!-- 1 columna → 2 (sm) → 4 (lg) -->
        <div class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <article class="tarjeta flex flex-col gap-3 border-neon/60 shadow-brillo">
            <div class="flex items-center justify-between"><span class="rounded bg-neon/10 px-2 py-0.5 font-mono text-xs text-neon">MOD-04</span><span class="font-mono text-xs text-emerald-400">Core activo</span></div>
            <h3 class="text-lg font-bold">C++ Moderno &amp; Videojuegos</h3>
            <p class="text-sm text-slate-400">Gestión de memoria, RAII, Smart Pointers, conceptos de C++20 y ciclo de vida de motores.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-neon">18 / 24</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de C++ Moderno" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-3/4 rounded-full bg-neon"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+350 XP <span class="text-xs text-slate-500">| Intermedio</span></span><a href="#" class="btn btn-primario px-3 py-1 text-xs">Continuar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-violet-400/10 px-2 py-0.5 font-mono text-xs text-violet-300">MOD-06</span><span class="font-mono text-xs text-slate-500">Pipeline 2D/3D</span></div>
            <h3 class="text-lg font-bold">SDL3 &amp; Game Loops</h3>
            <p class="text-sm text-slate-400">Renderizado acelerado por hardware, buffers de audio y gestión de ventanas en tiempo real.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-violet-300">10 / 22</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de SDL3" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[45%] rounded-full bg-violet-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+420 XP <span class="text-xs text-slate-500">| Avanzado</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-emerald-400/10 px-2 py-0.5 font-mono text-xs text-emerald-300">MOD-10</span><span class="font-mono text-xs text-slate-500">Shader pipeline</span></div>
            <h3 class="text-lg font-bold">OpenGL 4.6 &amp; GLSL</h3>
            <p class="text-sm text-slate-400">Vertex y fragment shaders, texturas, transformaciones e iluminación Phong.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-emerald-300">3 / 16</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de OpenGL" aria-valuenow="19" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[19%] rounded-full bg-emerald-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+500 XP <span class="text-xs text-slate-500">| Experto</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-oro/10 px-2 py-0.5 font-mono text-xs text-oro">MOD-13</span><span class="font-mono text-xs text-slate-500">Bajo nivel web</span></div>
            <h3 class="text-lg font-bold">WebAssembly &amp; Emscripten</h3>
            <p class="text-sm text-slate-400">Compilación nativa de C/C++ directo al navegador con velocidad cercana al metal.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-oro">5 / 19</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de WebAssembly" aria-valuenow="26" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[26%] rounded-full bg-oro"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+380 XP <span class="text-xs text-slate-500">| Avanzado</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-fuego/10 px-2 py-0.5 font-mono text-xs text-fuego">MOD-17</span><span class="font-mono text-xs text-slate-500">Data &amp; scripting</span></div>
            <h3 class="text-lg font-bold">Python &amp; Algoritmos</h3>
            <p class="text-sm text-slate-400">Estructuras de datos, resolución algorítmica y automatización de procesos.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-fuego">14 / 20</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de Python" aria-valuenow="70" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[70%] rounded-full bg-fuego"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+290 XP <span class="text-xs text-slate-500">| Inicial</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-rose-400/10 px-2 py-0.5 font-mono text-xs text-rose-300">MOD-20</span><span class="font-mono text-xs text-slate-500">Enterprise core</span></div>
            <h3 class="text-lg font-bold">Spring Boot &amp; Java Cloud</h3>
            <p class="text-sm text-slate-400">Arquitectura en capas, JPA, endpoints REST seguros y contenedores Docker.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-rose-300">16 / 24</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de Spring Boot" aria-valuenow="66" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-2/3 rounded-full bg-rose-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+310 XP <span class="text-xs text-slate-500">| Avanzado</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-sky-400/10 px-2 py-0.5 font-mono text-xs text-sky-300">MOD-23</span><span class="font-mono text-xs text-slate-500">Tipado estricto</span></div>
            <h3 class="text-lg font-bold">TypeScript Pro</h3>
            <p class="text-sm text-slate-400">Genéricos avanzados, decoradores, tipos condicionales y diseño de bibliotecas.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-sky-300">12 / 16</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de TypeScript" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-3/4 rounded-full bg-sky-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+290 XP <span class="text-xs text-slate-500">| Intermedio</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-pink-400/10 px-2 py-0.5 font-mono text-xs text-pink-300">MOD-16</span><span class="font-mono text-xs text-slate-500">Game dev web</span></div>
            <h3 class="text-lg font-bold">Phaser Engine &amp; JS</h3>
            <p class="text-sm text-slate-400">Física arcade, spritesheets, colisiones y publicación web de minijuegos.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-pink-300">8 / 15</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de Phaser" aria-valuenow="53" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[53%] rounded-full bg-pink-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+260 XP <span class="text-xs text-slate-500">| Inicial</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>
        </div>
      </section>
      <!-- /SECCION:rutas -->

      <!-- SECCION:fama -->
      <!-- ===== HALL OF FAME ===== -->
      <section id="fama" aria-labelledby="titulo-fama" class="scroll-mt-24">
        <div class="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p class="etiqueta-mono inline-block rounded border border-oro/40 px-2 py-0.5 text-[10px] text-oro">🏆 Hall of Fame · Temporada 04</p>
            <h2 id="titulo-fama" class="mt-2 text-2xl font-bold lg:text-3xl">Liga Obsidiana: Top 10 Alumnos</h2>
          </div>
          <p class="rounded-lg border border-borde px-3 py-1.5 font-mono text-xs text-slate-400">Cierre de temporada: <span class="text-neon">04d : 18h : 32m</span></p>
        </div>

        <!-- Podio: 3 columnas siempre; el 1.º mas alto y mas ancho -->
        <ol class="mt-10 grid grid-cols-[1fr_1.15fr_1fr] items-end gap-2 sm:gap-4 lg:gap-6">
          <li class="relative flex flex-col items-center gap-2 rounded-2xl border-2 border-slate-300/70 bg-panel px-1 pt-8 pb-4 text-center sm:px-4">
            <span class="absolute -top-4 grid size-8 place-items-center rounded-full border-2 border-slate-300 bg-fondo font-bold">2</span>
            <span class="grid size-12 place-items-center rounded-full border-2 border-neon/60 font-display font-bold text-neon sm:size-16 sm:text-lg">VAL</span>
            <span class="w-full truncate text-xs font-semibold sm:text-base">@DevValkyrie</span>
            <span class="font-mono text-[10px] text-slate-400">Cyber Wizard</span>
            <span class="rounded-full bg-neon/10 px-2 py-0.5 font-mono text-xs text-neon sm:text-sm">13.200 XP</span>
            <span class="hidden gap-1 text-[10px] lg:flex"><span class="rounded border border-borde px-1.5">OpenGL</span><span class="rounded border border-borde px-1.5">Rust</span></span>
            <span class="hidden text-xs text-fuego sm:block">🔥 Racha 28 días</span>
          </li>
          <li class="relative flex flex-col items-center gap-2 rounded-2xl border-2 border-oro bg-linear-to-b from-oro/15 to-panel px-1 pt-10 pb-6 text-center shadow-xl shadow-oro/20 sm:px-4 lg:pb-8">
            <span class="absolute -top-4 rounded-full bg-oro px-3 py-1 font-mono text-[10px] font-bold text-fondo uppercase"><span aria-hidden="true">👑</span> 1.º <span class="hidden sm:inline">lugar supremo</span></span>
            <span class="grid size-16 place-items-center rounded-full border-2 border-oro bg-oro/10 font-display text-lg font-bold text-oro shadow-lg shadow-oro/40 sm:size-20 sm:text-xl">NEO</span>
            <span class="w-full truncate text-sm font-bold sm:text-lg">@NeoCoder_X</span>
            <span class="font-mono text-[10px] text-oro">Gran Arquitecto Obsidian</span>
            <span class="rounded-full border border-oro/50 bg-oro/10 px-3 py-0.5 font-mono text-sm font-bold text-oro sm:text-base">14.850 XP</span>
            <span class="hidden gap-1 text-[10px] lg:flex"><span class="rounded border border-borde px-1.5">C++20</span><span class="rounded border border-borde px-1.5">SDL3 Engine</span></span>
            <span class="hidden text-xs text-fuego sm:block">🔥 Racha 45 días continuos</span>
          </li>
          <li class="relative flex flex-col items-center gap-2 rounded-2xl border-2 border-orange-500/80 bg-panel px-1 pt-8 pb-4 text-center sm:px-4">
            <span class="absolute -top-4 grid size-8 place-items-center rounded-full border-2 border-orange-500 bg-fondo font-bold">3</span>
            <span class="grid size-12 place-items-center rounded-full border-2 border-orange-500/70 font-display font-bold text-fuego sm:size-16 sm:text-lg">GLT</span>
            <span class="w-full truncate text-xs font-semibold sm:text-base">@GlitchHunter</span>
            <span class="font-mono text-[10px] text-slate-400">Kernel Master</span>
            <span class="rounded-full bg-fuego/10 px-2 py-0.5 font-mono text-xs text-fuego sm:text-sm">12.450 XP</span>
            <span class="hidden gap-1 text-[10px] lg:flex"><span class="rounded border border-borde px-1.5">WASM</span><span class="rounded border border-borde px-1.5">C++ Core</span></span>
            <span class="hidden text-xs text-fuego sm:block">🔥 Racha 19 días</span>
          </li>
        </ol>

        <!-- Puestos 4 a 10, CELULAR: lista de filas (oculta desde md) -->
        <ol start="4" class="mt-8 space-y-2 md:hidden">
          <li class="flex items-center gap-3 rounded-xl border border-borde bg-panel px-4 py-3"><span class="w-5 font-mono text-slate-400">4</span><span class="grid size-9 shrink-0 place-items-center rounded-lg bg-borde" aria-hidden="true">⚡</span><span class="min-w-0 flex-1"><span class="block truncate font-semibold">@ZeroByte_Arg</span><span class="block text-xs text-slate-400">C++ · <span class="text-emerald-400">▲ +1</span></span></span><span class="text-right font-mono">10.900<span class="block text-xs text-slate-500">XP</span></span></li>
          <li class="flex items-center gap-3 rounded-xl border border-borde bg-panel px-4 py-3"><span class="w-5 font-mono text-slate-400">5</span><span class="grid size-9 shrink-0 place-items-center rounded-lg bg-borde" aria-hidden="true">🧙</span><span class="min-w-0 flex-1"><span class="block truncate font-semibold">@PixelSage</span><span class="block text-xs text-slate-400">SDL3 · <span class="text-emerald-400">▲ +3</span></span></span><span class="text-right font-mono">9.850<span class="block text-xs text-slate-500">XP</span></span></li>
          <li class="flex items-center gap-3 rounded-xl border border-borde bg-panel px-4 py-3"><span class="w-5 font-mono text-slate-400">6</span><span class="grid size-9 shrink-0 place-items-center rounded-lg bg-borde" aria-hidden="true">🦊</span><span class="min-w-0 flex-1"><span class="block truncate font-semibold">@CodeKitsune</span><span class="block text-xs text-slate-400">OpenGL · <span class="text-rose-400">▼ −2</span></span></span><span class="text-right font-mono">8.920<span class="block text-xs text-slate-500">XP</span></span></li>
          <li class="flex items-center gap-3 rounded-xl border border-borde bg-panel px-4 py-3"><span class="w-5 font-mono text-slate-400">7</span><span class="grid size-9 shrink-0 place-items-center rounded-lg bg-borde" aria-hidden="true">⚔</span><span class="min-w-0 flex-1"><span class="block truncate font-semibold">@ByteSamurai</span><span class="block text-xs text-slate-400">WASM · <span class="text-slate-400">= 0</span></span></span><span class="text-right font-mono">8.100<span class="block text-xs text-slate-500">XP</span></span></li>
          <li class="flex items-center gap-3 rounded-xl border border-borde bg-panel px-4 py-3"><span class="w-5 font-mono text-slate-400">8</span><span class="grid size-9 shrink-0 place-items-center rounded-lg bg-borde" aria-hidden="true">🐍</span><span class="min-w-0 flex-1"><span class="block truncate font-semibold">@LaraBinary</span><span class="block text-xs text-slate-400">Python · <span class="text-emerald-400">▲ +1</span></span></span><span class="text-right font-mono">7.650<span class="block text-xs text-slate-500">XP</span></span></li>
          <li class="flex items-center gap-3 rounded-xl border border-borde bg-panel px-4 py-3"><span class="w-5 font-mono text-slate-400">9</span><span class="grid size-9 shrink-0 place-items-center rounded-lg bg-borde" aria-hidden="true">🕶</span><span class="min-w-0 flex-1"><span class="block truncate font-semibold">@MatrixWalker</span><span class="block text-xs text-slate-400">Java · <span class="text-rose-400">▼ −3</span></span></span><span class="text-right font-mono">6.980<span class="block text-xs text-slate-500">XP</span></span></li>
          <li class="flex items-center gap-3 rounded-xl border border-neon/60 bg-neon/5 px-4 py-3"><span class="w-5 font-mono text-neon">10</span><img src="/img/cursos/html/gheco-logo.webp" alt="" width="36" height="36" class="size-9 shrink-0 rounded-lg"><span class="min-w-0 flex-1"><span class="block truncate font-semibold text-neon">@GhecoDev <span class="text-xs font-normal text-slate-400">(vos)</span></span><span class="block text-xs text-slate-400">TypeScript · <span class="text-emerald-400">▲ +4</span></span></span><span class="text-right font-mono text-neon">6.400<span class="block text-xs text-slate-500">XP</span></span></li>
        </ol>

        <!-- Puestos 4 a 10, COMPUTADORA: tabla de verdad (visible desde md) -->
        <div class="mt-10 hidden overflow-hidden rounded-2xl border border-borde md:block">
          <table class="w-full text-left text-sm">
            <caption class="sr-only">Puestos 4 a 10 de la Liga Obsidiana</caption>
            <thead class="bg-panel font-mono text-[10px] tracking-widest text-slate-500 uppercase">
              <tr><th scope="col" class="px-5 py-3">Rank</th><th scope="col" class="px-5 py-3">Desarrollador</th><th scope="col" class="px-5 py-3">Rango y especialidad</th><th scope="col" class="px-5 py-3">Tendencia</th><th scope="col" class="px-5 py-3">Racha</th><th scope="col" class="px-5 py-3 text-right">Puntos</th></tr>
            </thead>
            <tbody class="divide-y divide-borde">
              <tr class="hover:bg-panel"><td class="px-5 py-3 font-mono text-neon">#04</td><th scope="row" class="px-5 py-3 font-semibold">@ZeroByte_Arg</th><td class="px-5 py-3 text-slate-400">C++ Moderno / Memory Guru</td><td class="px-5 py-3 text-emerald-400">▲ +1</td><td class="px-5 py-3 text-fuego">🔥 14d</td><td class="px-5 py-3 text-right font-mono">10.900 XP</td></tr>
              <tr class="hover:bg-panel"><td class="px-5 py-3 font-mono text-neon">#05</td><th scope="row" class="px-5 py-3 font-semibold">@PixelSage</th><td class="px-5 py-3 text-slate-400">SDL3 Engine / Game Loops</td><td class="px-5 py-3 text-emerald-400">▲ +3</td><td class="px-5 py-3 text-fuego">🔥 11d</td><td class="px-5 py-3 text-right font-mono">9.850 XP</td></tr>
              <tr class="hover:bg-panel"><td class="px-5 py-3 font-mono text-neon">#06</td><th scope="row" class="px-5 py-3 font-semibold">@CodeKitsune</th><td class="px-5 py-3 text-slate-400">OpenGL Shader Specialist</td><td class="px-5 py-3 text-rose-400">▼ −2</td><td class="px-5 py-3 text-fuego">🔥 8d</td><td class="px-5 py-3 text-right font-mono">8.920 XP</td></tr>
              <tr class="hover:bg-panel"><td class="px-5 py-3 font-mono text-neon">#07</td><th scope="row" class="px-5 py-3 font-semibold">@ByteSamurai</th><td class="px-5 py-3 text-slate-400">WebAssembly &amp; C Native</td><td class="px-5 py-3 text-slate-400">= 0</td><td class="px-5 py-3 text-fuego">🔥 18d</td><td class="px-5 py-3 text-right font-mono">8.100 XP</td></tr>
              <tr class="hover:bg-panel"><td class="px-5 py-3 font-mono text-neon">#08</td><th scope="row" class="px-5 py-3 font-semibold">@LaraBinary</th><td class="px-5 py-3 text-slate-400">Python Algorithms &amp; ML</td><td class="px-5 py-3 text-emerald-400">▲ +1</td><td class="px-5 py-3 text-fuego">🔥 15d</td><td class="px-5 py-3 text-right font-mono">7.650 XP</td></tr>
              <tr class="hover:bg-panel"><td class="px-5 py-3 font-mono text-neon">#09</td><th scope="row" class="px-5 py-3 font-semibold">@MatrixWalker</th><td class="px-5 py-3 text-slate-400">Java Spring Boot Cloud</td><td class="px-5 py-3 text-rose-400">▼ −3</td><td class="px-5 py-3 text-fuego">🔥 6d</td><td class="px-5 py-3 text-right font-mono">6.980 XP</td></tr>
              <tr class="bg-neon/5"><td class="px-5 py-3 font-mono text-neon">#10</td><th scope="row" class="px-5 py-3 font-semibold text-neon">@GhecoDev <span class="font-normal text-slate-400">(vos)</span></th><td class="px-5 py-3 text-slate-400">TypeScript Pro / Fullstack</td><td class="px-5 py-3 text-emerald-400">▲ +4</td><td class="px-5 py-3 text-fuego">🔥 9d</td><td class="px-5 py-3 text-right font-mono text-neon">6.400 XP</td></tr>
            </tbody>
          </table>
        </div>
      </section>
      <!-- /SECCION:fama -->

    </main>

    <!-- SECCION:pie -->
    <!-- ===== PIE ===== -->
    <footer class="border-t border-borde">
      <div class="mx-auto grid max-w-7xl gap-6 px-4 py-8 text-sm md:grid-cols-[2fr_1fr_1fr] md:items-center">
        <div class="flex items-center gap-3">
          <img src="/img/cursos/html/gheco-logo.webp" alt="" width="36" height="36" class="size-9 rounded-lg">
          <p><span class="font-display font-bold">GhecoSoft-Code Platform</span><br><span class="text-xs text-slate-500">Formación avanzada en bajo nivel, motores de videojuegos y compilación real.</span></p>
        </div>
        <ul class="space-y-1 font-mono text-xs text-slate-400">
          <li><span class="text-emerald-400">●</span> Cloud Compiler Clang 18: online</li>
          <li><span class="text-emerald-400">●</span> GCC 14 / Emscripten: 99.98% uptime</li>
        </ul>
        <p class="font-mono text-xs text-slate-500 md:text-right">© 2026 GhecoSoft-Code.<br>Obsidian Design Protocol v4.2</p>
      </div>
    </footer>
    <!-- /SECCION:pie -->

    <!-- SECCION:barra -->
    <!-- ===== BARRA INFERIOR (solo celular y tablet) ===== -->
    <nav aria-label="Secciones" class="fixed inset-x-0 bottom-0 z-40 border-t border-borde bg-panel/95 backdrop-blur lg:hidden">
      <div class="mx-auto flex max-w-lg">
        <a href="#rutas" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">🗺</span>Campañas</a>
        <a href="#" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">📖</span>Lecciones</a>
        <a href="#fama" aria-current="page" class="my-1 flex flex-1 flex-col items-center gap-0.5 rounded-xl border border-neon/50 bg-neon/10 py-1 text-[11px] text-neon"><span aria-hidden="true" class="text-lg">⚔</span>Arena</a>
        <a href="#" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">🌳</span>Árbol</a>
      </div>
    </nav>
    <!-- /SECCION:barra -->
  </body>
</html>
```

### ¿Para qué sirve?

Los rankings, las tablas de posiciones y los resultados de búsqueda tienen que funcionar en cualquier pantalla. Mostrar los mismos datos como tarjetas en el celular y como tabla en la compu es una técnica que usan los diarios deportivos, los bancos y las tiendas.

### Errores habituales

**Orco: el podio se sale en el celular**: un nombre largo o un `min-w` empujan la columna. `truncate` necesita un ancho (`w-full`) para cortar.

**Troll: la medalla queda cortada**: la tarjeta (o un padre) tiene `overflow-hidden`; o le falta espacio arriba a la lista (`mt-10`).

**Ogro: `hidden` y `md:table`**: para mostrar una tabla desde `md` se usa `hidden md:table` (o envolverla en un `div` con `hidden md:block`); con `md:block` en la propia tabla, sus columnas se desarman.

### Prueba del sello

#### ¿Por qué el orden del podio en el HTML es 2-1-3?

Porque la grilla acomoda las columnas en el orden del HTML: escribiendo 2-1-3, el segundo queda a la izquierda, el primero en el medio (la columna más ancha) y el tercero a la derecha, como un podio de verdad.

#### Si los datos están dos veces, ¿por qué el lector de pantalla no los lee dos veces?

Porque una de las dos copias está oculta con `display: none` (`md:hidden` o `hidden md:block`), y lo que tiene `display: none` no existe para el lector de pantalla.

#### ¿Qué ventaja y qué desventaja tiene la tabla con scroll frente a lista + tabla?

Ventaja: los datos están **una sola vez**, más fácil de mantener. Desventaja: en el celular hay que deslizar de costado para ver todas las columnas, que es más incómodo que una lista pensada para la pantalla chica.

### Misión R04-N04-M1 · Tu puesto a la vista

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

En una lista larga del ranking, hacé que **la fila del usuario** quede pegada abajo de la pantalla hasta que se llega a ella al hacer scroll (`sticky bottom-4`).

#### Criterio de aprobación

- La fila del usuario usa `sticky bottom-…` y se distingue de las demás.
- Al llegar a su lugar en la lista, queda en su posición.

#### Cómo debe quedar

celular: capturas/R04-N04-M1-celular.webp
compu: capturas/R04-N04-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Tu puesto a la vista</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>Tu puesto siempre a la vista</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <body class="pb-20">
    <main class="space-y-2 p-4">
      <p class="text-sm text-slate-400">Hacé scroll: tu fila queda pegada abajo hasta que llegás a ella.</p>
      <ol start="4" class="space-y-2">
        <li class="tarjeta py-3">4 · @ZeroByte_Arg</li><li class="tarjeta py-3">5 · @PixelSage</li><li class="tarjeta py-3">6 · @CodeKitsune</li>
        <li class="tarjeta py-3">7 · @ByteSamurai</li><li class="tarjeta py-3">8 · @LaraBinary</li><li class="tarjeta py-3">9 · @MatrixWalker</li>
        <li class="tarjeta py-3">11 · @NullPointer</li><li class="tarjeta py-3">12 · @SegFaultKid</li><li class="tarjeta py-3">13 · @HeapHero</li>
        <li class="tarjeta py-3">14 · @StackSmash</li><li class="tarjeta py-3">15 · @RustAcean</li>
        <!-- sticky bottom: se queda abajo mientras su lugar real no aparece en pantalla -->
        <li class="tarjeta sticky bottom-4 border-neon/60 bg-panel py-3 text-neon shadow-brillo">10 · @GhecoDev (vos) · 6.400 XP</li>
      </ol>
    </main>
  </body>
</html>
```


### Misión R04-N04-M2 · Una sola tabla

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Usá la tabla de la compu **también en el celular**, con scroll horizontal propio: `overflow-x-auto` en el contenedor y `min-w-[40rem]` en la tabla.

#### Criterio de aprobación

- La tabla tiene `caption` y encabezados con `scope`.
- En *Celular* la tabla se desliza sola; la página no tiene scroll horizontal.

#### Cómo debe quedar

celular: capturas/R04-N04-M2-celular.webp
compu: capturas/R04-N04-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Una sola tabla</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>Tabla con scroll horizontal</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <body class="p-4">
    <!-- La otra solucion: UNA sola tabla que en el celular se desliza de costado -->
    <div class="overflow-x-auto rounded-2xl border border-borde">
      <table class="w-full min-w-[40rem] text-left text-sm">
        <caption class="sr-only">Puestos 4 a 6</caption>
        <thead class="bg-panel font-mono text-[10px] tracking-widest text-slate-500 uppercase">
          <tr><th scope="col" class="px-4 py-3">Rank</th><th scope="col" class="px-4 py-3">Desarrollador</th><th scope="col" class="px-4 py-3">Especialidad</th><th scope="col" class="px-4 py-3">Racha</th><th scope="col" class="px-4 py-3 text-right">Puntos</th></tr>
        </thead>
        <tbody class="divide-y divide-borde">
          <tr><td class="px-4 py-3 font-mono text-neon">#04</td><th scope="row" class="px-4 py-3">@ZeroByte_Arg</th><td class="px-4 py-3 text-slate-400">C++ Moderno</td><td class="px-4 py-3 text-fuego">🔥 14d</td><td class="px-4 py-3 text-right font-mono">10.900</td></tr>
          <tr><td class="px-4 py-3 font-mono text-neon">#05</td><th scope="row" class="px-4 py-3">@PixelSage</th><td class="px-4 py-3 text-slate-400">SDL3 Engine</td><td class="px-4 py-3 text-fuego">🔥 11d</td><td class="px-4 py-3 text-right font-mono">9.850</td></tr>
          <tr><td class="px-4 py-3 font-mono text-neon">#06</td><th scope="row" class="px-4 py-3">@CodeKitsune</th><td class="px-4 py-3 text-slate-400">OpenGL</td><td class="px-4 py-3 text-fuego">🔥 8d</td><td class="px-4 py-3 text-right font-mono">8.920</td></tr>
        </tbody>
      </table>
    </div>
  </body>
</html>
```


### Encargo R04-N04-E1 · La tabla del torneo

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Una liga de fútbol quiere su tabla de posiciones: tarjetas en el celular y la tabla completa (PJ, G, E, P, Pts) en la compu.

#### Criterio de aprobación

- Tarjetas en *Celular* y tabla en *Compu*, con `md:hidden` / `hidden md:block`.
- La tabla tiene `caption` y `scope`.

#### Cómo debe quedar

celular: capturas/R04-N04-E1-celular.webp
compu: capturas/R04-N04-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La tabla del torneo</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>Torneo de fútbol</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <body class="bg-green-50 p-4 text-slate-800">
    <main class="mx-auto max-w-4xl">
      <h1 class="text-2xl font-bold">Liga Barrial · Fecha 12</h1>
      <!-- Celular: tarjetas -->
      <ol class="mt-4 space-y-2 md:hidden">
        <li class="flex justify-between rounded-lg bg-white p-3 shadow-sm"><span>1. Los Pumas</span><strong>28 pts</strong></li>
        <li class="flex justify-between rounded-lg bg-white p-3 shadow-sm"><span>2. Atlético Faro</span><strong>25 pts</strong></li>
        <li class="flex justify-between rounded-lg bg-white p-3 shadow-sm"><span>3. Deportivo Sur</span><strong>21 pts</strong></li>
      </ol>
      <!-- Computadora: tabla -->
      <table class="mt-4 hidden w-full overflow-hidden rounded-lg bg-white shadow-sm md:table">
        <caption class="sr-only">Tabla de posiciones</caption>
        <thead class="bg-green-700 text-left text-white"><tr><th scope="col" class="p-3">Equipo</th><th scope="col" class="p-3">PJ</th><th scope="col" class="p-3">G</th><th scope="col" class="p-3">E</th><th scope="col" class="p-3">P</th><th scope="col" class="p-3">Pts</th></tr></thead>
        <tbody class="divide-y">
          <tr><th scope="row" class="p-3 text-left">Los Pumas</th><td class="p-3">12</td><td class="p-3">9</td><td class="p-3">1</td><td class="p-3">2</td><td class="p-3 font-bold">28</td></tr>
          <tr><th scope="row" class="p-3 text-left">Atlético Faro</th><td class="p-3">12</td><td class="p-3">8</td><td class="p-3">1</td><td class="p-3">3</td><td class="p-3 font-bold">25</td></tr>
          <tr><th scope="row" class="p-3 text-left">Deportivo Sur</th><td class="p-3">12</td><td class="p-3">6</td><td class="p-3">3</td><td class="p-3">3</td><td class="p-3 font-bold">21</td></tr>
        </tbody>
      </table>
    </main>
  </body>
</html>
```


### Encargo R04-N04-E2 · La galería de las líderes

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

El pedido de {mentor}: un vitral con **las seis líderes del mundo**. Armá una galería con una tarjeta por líder —su retrato, su nombre, su región y su lengua— en **1 → 2 → 3** columnas. Los retratos están en `/img/cursos/html/lideres/`: `ofidia.webp`, `ferrum.webp`, `tesla.webp`, `kaffa.webp`, `elefa.webp` y `tesela.webp`.

| Líder | Región | Lengua |
|---|---|---|
| Ofidia | Valle de la Serpiente | Python |
| Maese Ferrum | Forjas de Hierro | C |
| Tesla | Ciudadela de los Artífices | C++ |
| Kaffa | Imperio de las Clases | Java |
| Elefa | Puerto de los Mensajeros | PHP |
| Tesela | Talleres de los Vitrales | HTML y CSS |

#### Criterio de aprobación

- Seis tarjetas iguales, una por líder, con retrato, nombre, región y lengua.
- Cada retrato tiene un `alt` con el nombre.
- La grilla pasa de 1 a 2 y a 3 columnas.

#### Cómo debe quedar

celular: capturas/R04-N04-E2-celular.webp
compu: capturas/R04-N04-E2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La galería de las líderes</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>La galería de las líderes</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <body class="min-h-screen p-4 sm:p-8">
    <main class="mx-auto max-w-6xl">
      <p class="etiqueta-mono text-neon">Hall of Fame</p>
      <h1 class="mt-1 font-display text-3xl font-bold text-white sm:text-4xl">La galería de las líderes</h1>
      <p class="mt-2 max-w-prose text-slate-400">Las maestras y maestros de cada región del Mundo del Código.</p>
      <ul class="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <li class="tarjeta flex flex-col items-center gap-3 p-5 text-center">
          <div class="rounded-full bg-linear-to-br from-emerald-400 to-teal-600 p-1">
            <img src="/img/cursos/html/lideres/ofidia.webp" alt="Retrato de Ofidia" width="112" height="112" loading="lazy" class="size-28 rounded-full object-cover">
          </div>
          <h3 class="font-display text-lg font-bold text-white">Ofidia</h3>
          <p class="text-sm text-slate-400">Valle de la Serpiente</p>
          <span class="chip">Python</span>
        </li>
        <li class="tarjeta flex flex-col items-center gap-3 p-5 text-center">
          <div class="rounded-full bg-linear-to-br from-orange-400 to-red-700 p-1">
            <img src="/img/cursos/html/lideres/ferrum.webp" alt="Retrato de Maese Ferrum" width="112" height="112" loading="lazy" class="size-28 rounded-full object-cover">
          </div>
          <h3 class="font-display text-lg font-bold text-white">Maese Ferrum</h3>
          <p class="text-sm text-slate-400">Forjas de Hierro</p>
          <span class="chip">C</span>
        </li>
        <li class="tarjeta flex flex-col items-center gap-3 p-5 text-center">
          <div class="rounded-full bg-linear-to-br from-sky-400 to-blue-700 p-1">
            <img src="/img/cursos/html/lideres/tesla.webp" alt="Retrato de Tesla" width="112" height="112" loading="lazy" class="size-28 rounded-full object-cover">
          </div>
          <h3 class="font-display text-lg font-bold text-white">Tesla</h3>
          <p class="text-sm text-slate-400">Ciudadela de los Artífices</p>
          <span class="chip">C++</span>
        </li>
        <li class="tarjeta flex flex-col items-center gap-3 p-5 text-center">
          <div class="rounded-full bg-linear-to-br from-amber-300 to-yellow-700 p-1">
            <img src="/img/cursos/html/lideres/kaffa.webp" alt="Retrato de Kaffa" width="112" height="112" loading="lazy" class="size-28 rounded-full object-cover">
          </div>
          <h3 class="font-display text-lg font-bold text-white">Kaffa</h3>
          <p class="text-sm text-slate-400">Imperio de las Clases</p>
          <span class="chip">Java</span>
        </li>
        <li class="tarjeta flex flex-col items-center gap-3 p-5 text-center">
          <div class="rounded-full bg-linear-to-br from-violet-400 to-purple-700 p-1">
            <img src="/img/cursos/html/lideres/elefa.webp" alt="Retrato de Elefa" width="112" height="112" loading="lazy" class="size-28 rounded-full object-cover">
          </div>
          <h3 class="font-display text-lg font-bold text-white">Elefa</h3>
          <p class="text-sm text-slate-400">Puerto de los Mensajeros</p>
          <span class="chip">PHP</span>
        </li>
        <li class="tarjeta flex flex-col items-center gap-3 p-5 text-center">
          <div class="rounded-full bg-linear-to-br from-cyan-300 to-fuchsia-500 p-1">
            <img src="/img/cursos/html/lideres/tesela.webp" alt="Retrato de Tesela" width="112" height="112" loading="lazy" class="size-28 rounded-full object-cover">
          </div>
          <h3 class="font-display text-lg font-bold text-white">Tesela</h3>
          <p class="text-sm text-slate-400">Talleres de los Vitrales</p>
          <span class="chip">HTML y CSS</span>
        </li>
      </ul>
    </main>
  </body>
</html>
```

## R04-N05 · Jefe final: el Dragón de los Talleres

```meta
tipo: jefe
padre: R04-N04
precio: 10
criatura: dragon
insignia: Maestro vitralista
insignia_descripcion: Venciste al Dragón de los Talleres: terminaste el gran ventanal, en el celular y en la compu.
temas: herr.navegador
usa: css.frameworks, css.temas, html.semantica, css.responsive
```

### Crónica

Falta el último vidrio: la **Bóveda**, donde brillan las monedas de maestría, con Gheco señalándolas. Iris lo coloca, da un paso atrás y mira el ventanal entero, desde la cabaña y desde el castillo.

Entonces aparece el **Dragón de los Talleres**, de plomo y vidrio, con una lupa enorme en la garra: el que vive en cada detalle que nadie revisó. Un menú que se parte, un botón sin foco, una imagen sin `alt`. —Inspección final —gruñe—. Si encuentro un solo error, el ventanal es mío.

—No te apures —dice {mentor}—. Revisá como revisaría él. **Celular, teclado y validador.**

El dragón no encuentra nada. Se va volando, ofendido. Esa noche, {mentor} saca una llave vieja y abre por fin la puerta del candado: el taller de su maestro, el Vidriero. En la mesa hay **un marco de plomo redondo y vacío**, con un hueco en el centro del tamaño exacto del fragmento de Iris. {mentor} reconoce el plomo. Iris no pone el fragmento en ese marco: arma su propio vitral, chiquito, empezando por la ventanita de la cabaña, con el fragmento en el centro. **El Vitral de Iris.** {mentor} le muestra el canasto: —Boceto 214. Ese fue el primero que colgaste.

### Objetivos

Terminar la página de **GhecoSoft-Code** igual a las imágenes de referencia (celular y computadora): agregar la bóveda de tokens y hacer la **revisión final** de accesibilidad, desbordes, rendimiento y validez. Y saber cómo publicarla.

### Antes de empezar

- Las cuatro etapas del Gran Ventanal: esta página es la misma, completa.

### Explicación

#### La bóveda de tokens
- Tarjeta de dos columnas desde `lg` (texto | monedas), apilada en el celular.
- Los datos "6 / 6" y "100%" son una lista de definiciones (`dl`/`dt`/`dd`): término y valor.
- **Las monedas** son `li` redondos con degradé (`bg-linear-to-br from-sky-400 to-blue-700`), borde claro y sombra de color. Flotan con la animación del tema (`animate-flotar`) y cada una arranca un poco después con un valor a medida: `[animation-delay:300ms]` (corchetes también para propiedades enteras).
- **Gheco** (`gheco-512.webp`) va detrás, abajo a la izquierda, semitransparente, con `loading="lazy"` porque está lejos del principio de la página.

#### Revisión final (la inspección del Dragón)
| Revisión | Cómo |
|---|---|
| HTML válido | Pegá el código en [validator.w3.org](https://validator.w3.org/#validate_by_input): tiene que decir *No errors* |
| Sin scroll horizontal | Mirá la vista *Celular* entera: no puede aparecer la barra de scroll de costado. En tu compu, probá también a 768 y 1024 px con el modo celular del inspector |
| Teclado | Tab desde el principio: aparece "Saltar al contenido", todo control tiene contorno de foco, los filtros se eligen con las flechas |
| Lector de pantalla | landmarks (banner, 2 navigation con nombre, main, contentinfo), títulos en orden h1 → h2 → h3, imágenes decorativas con `alt=""`, íconos con `aria-hidden`, tabla con `caption` y `scope`, barras con `role="progressbar"` |
| Imágenes | WebP (6–60 KB en vez de 150–180 KB), `srcset` en el héroe, `width`/`height` siempre, `lazy` en las de abajo |
| Movimiento | si el sistema pide "reducir movimiento", el tema apaga animaciones y transiciones (`@media (prefers-reduced-motion: reduce)`) |

En Chrome, DevTools → **Lighthouse** → "Analizar" da puntajes de rendimiento, accesibilidad y buenas prácticas, con la lista de lo que falta.

#### Publicar la página
1. Pasar el CSS de Tailwind a un archivo y compilarlo **minificado** (sin espacios ni comentarios), en tu compu:
   ```bash
   npx @tailwindcss/cli -i entrada.css -o salida.css --minify
   ```
2. Subir `index.html`, `salida.css` y las imágenes que usa (respetando las rutas) a cualquier hosting estático: GitHub Pages, Netlify, Cloudflare Pages o el servidor del instituto. No hace falta Node en el servidor: es HTML y CSS.

#### Lo que falta para que "funcione"
La página es **estática**: el login no entra a ningún lado y el ranking está escrito a mano. El paso siguiente es darle vida: con JavaScript (en la Feria de las Luces, el curso de JavaScript), como app con React Native (en el Archipiélago de los Espejos, el curso de React Native) o generada desde un servidor con PHP/Laravel (en el Puerto de Elefa, el curso de PHP) o Spring Boot (en el Imperio de Kaffa, el curso de Java), que llenan las mismas tarjetas y filas con datos reales.

#### El ejemplo

La página completa, con comentarios `<!-- SECCION:x -->` que marcan cada parte. Las etapas del Gran Ventanal salieron de este mismo archivo.

#### Cómo se ve el ejemplo

Cabecera, hero con el aprendiz, portal, ocho rutas, podio, ranking, bóveda con las seis monedas y Gheco, y pie. En el celular, la barra de 4 secciones abajo. Miralo en *Celular*, en *Compu* y en pantalla completa.

### Código de ejemplo

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GhecoSoft-Code · Plataforma de cursos</title>
    <meta name="description" content="Aprendé a programar avanzando por tu árbol de habilidades: C++, SDL3, OpenGL, WebAssembly y más.">
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <!-- pb-20: lugar para la barra inferior del celular; desde lg no hay barra -->
  <body class="pb-20 lg:pb-0">
    <!-- SECCION:salto -->
    <!-- Enlace de salto: invisible hasta que recibe el foco con Tab -->
    <a href="#contenido" class="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 focus:rounded-lg focus:bg-neon focus:px-4 focus:py-2 focus:text-fondo">Saltar al contenido</a>
    <!-- /SECCION:salto -->

    <!-- SECCION:cabecera -->
    <!-- ===== CABECERA ===== -->
    <header class="sticky top-0 z-40 border-b border-borde bg-fondo/85 backdrop-blur">
      <div class="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3">
        <!-- Marca: logo con su nivel + nombre + estado -->
        <a href="#" class="flex items-center gap-3">
          <span class="relative shrink-0">
            <img src="/img/cursos/html/gheco-logo.webp" alt="" width="44" height="44" class="size-11 rounded-xl ring-1 ring-neon/50">
            <span class="absolute -bottom-1.5 left-1/2 -translate-x-1/2 rounded bg-violet-600 px-1 font-mono text-[9px] leading-tight font-bold text-white lg:hidden">LV.14</span>
          </span>
          <span>
            <span class="block font-display text-lg leading-tight font-bold whitespace-nowrap">GhecoSoft <span class="text-neon">-Code</span></span>
            <span class="flex items-center gap-1.5 font-mono text-[10px] tracking-widest text-slate-400 uppercase">
              <span class="size-1.5 animate-latido rounded-full bg-emerald-400"></span> System online
            </span>
          </span>
        </a>

        <!-- Menu principal: solo desde lg (en el celular esta la barra de abajo) -->
        <nav aria-label="Principal" class="hidden items-center gap-1 text-sm whitespace-nowrap lg:flex">
          <a href="#rutas" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Cursos</a>
          <a href="#rutas" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Rutas</a>
          <a href="#fama" aria-current="page" class="rounded-lg border border-neon/50 bg-neon/10 px-3 py-2 text-neon">🏆 Top 10<span class="hidden xl:inline"> alumnos</span></a>
          <a href="#" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Skill Tree</a>
          <a href="#boveda" class="rounded-lg px-3 py-2 text-slate-300 hover:text-neon">Bóveda<span class="hidden xl:inline"> de tokens</span></a>
        </nav>

        <!-- Estadisticas del jugador -->
        <div class="flex items-center gap-2 font-mono text-xs whitespace-nowrap">
          <span class="hidden items-center gap-2 rounded-lg border border-borde px-2.5 py-1.5 xl:flex">
            LVL 14
            <span class="h-1.5 w-12 overflow-hidden rounded-full bg-borde"><span class="block h-full w-2/3 bg-violet-500"></span></span>
          </span>
          <span class="rounded-lg border border-borde px-2.5 py-1.5"><span class="text-neon">⚡ 1.450</span><span class="hidden lg:inline"> ESC</span><span class="lg:hidden"> · <span class="text-fuego">🔥 12</span></span></span>
          <span class="hidden rounded-lg border border-fuego/40 px-2.5 py-1.5 text-fuego lg:inline">🔥 12 días</span>
          <img src="/img/cursos/html/heroe-avatar.webp" alt="Tu perfil" width="36" height="36" class="hidden size-9 rounded-full border-2 border-neon object-cover lg:block">
        </div>
      </div>
    </header>
    <!-- /SECCION:cabecera -->

    <main id="contenido" class="mx-auto max-w-7xl space-y-16 px-4 py-6 lg:space-y-24 lg:py-10">
      <!-- SECCION:hero -->
      <!-- ===== HERO + LOGIN ===== -->
      <section aria-labelledby="titulo-hero" class="overflow-hidden rounded-3xl border border-borde bg-panel lg:grid lg:grid-cols-[1.5fr_1fr]">
        <!-- Lado izquierdo: ilustracion de fondo + texto -->
        <div class="fondo-cuadricula relative isolate flex min-h-[36rem] flex-col justify-end p-6 sm:min-h-[30rem] sm:p-10 lg:min-h-[34rem]">
          <img src="/img/cursos/html/heroe-448.webp" srcset="/img/cursos/html/heroe-448.webp 448w, /img/cursos/html/heroe-896.webp 896w" sizes="(min-width: 64rem) 30rem, 70vw" alt="" width="448" height="600" class="absolute top-0 right-0 -z-10 h-full w-auto max-w-none object-cover opacity-80">
          <!-- Degrade para que el texto se lea sobre la imagen -->
          <div class="absolute inset-0 -z-10 bg-linear-to-t from-panel from-30% via-panel/70 to-transparent lg:bg-linear-to-r lg:via-panel/70 lg:to-transparent"></div>

          <p class="etiqueta-mono inline-flex w-fit items-center gap-2 rounded-full border border-neon/40 bg-fondo/60 px-3 py-1 text-[10px] text-neon">
            <span class="size-1.5 animate-latido rounded-full bg-neon"></span> Plataforma de cursos <span class="hidden sm:inline">· Temporada 04</span>
          </p>
          <h1 id="titulo-hero" class="mt-4 max-w-xl text-3xl leading-tight font-bold sm:text-4xl lg:text-5xl">
            Aprendé a programar avanzando por tu <span class="texto-neon text-neon">árbol de habilidades</span>.
          </h1>
          <p class="mt-3 max-w-lg text-slate-300 lg:text-lg">
            Compilá algoritmos reales, desbloqueá nodos tecnológicos de bajo nivel (C++, SDL3, OpenGL, WASM) y competí por el rango Supremo del salón de la fama.
          </p>
          <div class="mt-6 flex gap-3">
            <a href="#rutas" class="btn btn-primario flex-1 sm:flex-none">▷ Continuar campaña</a>
            <a href="#fama" class="btn btn-secundario"><span class="sm:hidden">Top 10</span><span class="hidden sm:inline">Ver leaderboard <span class="ml-1 rounded bg-neon/10 px-1.5 text-xs">Top 10</span></span></a>
          </div>
        </div>

        <!-- Lado derecho: el portal (login). En el celular va debajo -->
        <div class="border-t border-borde bg-fondo/40 p-6 sm:p-10 lg:border-t-0 lg:border-l">
          <p class="etiqueta-mono text-center text-[10px] text-slate-500">Portal del desarrollador</p>
          <h2 class="mt-2 text-center text-2xl font-bold">Entrá a tu cuenta</h2>
          <p class="mt-1 text-center text-sm text-slate-400">Ingresá tu usuario y contraseña para retomar tu entrenamiento.</p>

          <form action="#" method="post" class="mt-6 space-y-4">
            <button type="button" class="btn w-full border border-borde bg-panel py-2.5 text-sm text-slate-200 hover:border-neon/60">🔑 Entrar con llave de acceso (Passkey)</button>
            <p class="flex items-center gap-3 font-mono text-[10px] tracking-widest text-slate-500 uppercase" aria-hidden="true">
              <span class="h-px flex-1 bg-borde"></span> o seguí con tu email <span class="h-px flex-1 bg-borde"></span>
            </p>
            <div class="space-y-1">
              <label for="usuario" class="etiqueta-mono block text-[10px] text-slate-400">Usuario o email</label>
              <input id="usuario" name="usuario" type="text" autocomplete="username" required placeholder="cliente" class="peer w-full rounded-lg border border-borde bg-fondo px-3 py-2.5 placeholder:text-slate-600 focus:border-neon focus:ring-2 focus:ring-neon/30 focus:outline-none user-invalid:border-rose-400">
              <p class="hidden text-xs text-rose-400 peer-user-invalid:block">Completá tu usuario o email.</p>
            </div>
            <div class="space-y-1">
              <div class="flex items-baseline justify-between">
                <label for="clave" class="etiqueta-mono text-[10px] text-slate-400">Contraseña</label>
                <a href="#" class="text-xs text-neon hover:underline">¿Olvidaste tu contraseña?</a>
              </div>
              <input id="clave" name="clave" type="password" autocomplete="current-password" required minlength="8" class="w-full rounded-lg border border-borde bg-fondo px-3 py-2.5 focus:border-neon focus:ring-2 focus:ring-neon/30 focus:outline-none">
            </div>
            <label class="flex items-center gap-2 text-sm text-slate-300">
              <input type="checkbox" name="recordarme" checked class="size-4 accent-cyan-400"> Recordarme en esta terminal
            </label>
            <button type="submit" class="btn btn-primario w-full tracking-wider uppercase">Entrar a la terminal →</button>
          </form>
          <p class="mt-4 text-center text-sm text-slate-400">¿No tenés cuenta aún? <a href="#" class="font-semibold text-neon hover:underline">Registrate gratis</a></p>

          <!-- Mision en curso -->
          <div class="mt-6 flex items-center gap-3 rounded-xl border border-borde bg-panel p-3">
            <span class="size-2 shrink-0 rounded-full bg-emerald-400"></span>
            <p class="min-w-0 flex-1 text-xs">
              <span class="etiqueta-mono block text-[10px] text-neon">Misión en curso</span>
              <span class="block truncate text-slate-300">04-C++ Moderno: Smart Pointers</span>
            </p>
            <span class="rounded-md bg-neon/10 px-2 py-1 font-mono text-xs text-neon">75%</span>
          </div>
        </div>
      </section>
      <!-- /SECCION:hero -->

      <!-- SECCION:rutas -->
      <!-- ===== RUTAS DE ENTRENAMIENTO ===== -->
      <section id="rutas" aria-labelledby="titulo-rutas" class="scroll-mt-24">
        <div class="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p class="flex items-center gap-2">
              <span class="etiqueta-mono rounded border border-neon/40 px-2 py-0.5 text-[10px] text-neon">Directorio curricular</span>
              <span class="font-mono text-xs text-slate-500">23 módulos</span>
            </p>
            <h2 id="titulo-rutas" class="mt-2 text-2xl font-bold lg:text-3xl">Rutas de Entrenamiento</h2>
          </div>
          <!-- Filtros: radios escondidos (sr-only) + has-checked -->
          <fieldset class="relative flex w-full min-w-0 gap-2 overflow-x-auto pb-1 lg:w-auto lg:flex-wrap lg:overflow-visible">
            <legend class="sr-only">Filtrar rutas</legend>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only" checked> Todos (23)</label>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only"> Bajo nivel / C++</label>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only"> Gráficos &amp; Shaders</label>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only"> Desarrollo web</label>
            <label class="chip shrink-0 cursor-pointer has-checked:border-neon has-checked:bg-neon has-checked:text-fondo has-focus-visible:outline-2 has-focus-visible:outline-neon"><input type="radio" name="filtro" class="sr-only"> Backend &amp; Cloud</label>
          </fieldset>
        </div>

        <!-- 1 columna → 2 (sm) → 4 (lg) -->
        <div class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <article class="tarjeta flex flex-col gap-3 border-neon/60 shadow-brillo">
            <div class="flex items-center justify-between"><span class="rounded bg-neon/10 px-2 py-0.5 font-mono text-xs text-neon">MOD-04</span><span class="font-mono text-xs text-emerald-400">Core activo</span></div>
            <h3 class="text-lg font-bold">C++ Moderno &amp; Videojuegos</h3>
            <p class="text-sm text-slate-400">Gestión de memoria, RAII, Smart Pointers, conceptos de C++20 y ciclo de vida de motores.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-neon">18 / 24</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de C++ Moderno" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-3/4 rounded-full bg-neon"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+350 XP <span class="text-xs text-slate-500">| Intermedio</span></span><a href="#" class="btn btn-primario px-3 py-1 text-xs">Continuar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-violet-400/10 px-2 py-0.5 font-mono text-xs text-violet-300">MOD-06</span><span class="font-mono text-xs text-slate-500">Pipeline 2D/3D</span></div>
            <h3 class="text-lg font-bold">SDL3 &amp; Game Loops</h3>
            <p class="text-sm text-slate-400">Renderizado acelerado por hardware, buffers de audio y gestión de ventanas en tiempo real.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-violet-300">10 / 22</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de SDL3" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[45%] rounded-full bg-violet-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+420 XP <span class="text-xs text-slate-500">| Avanzado</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-emerald-400/10 px-2 py-0.5 font-mono text-xs text-emerald-300">MOD-10</span><span class="font-mono text-xs text-slate-500">Shader pipeline</span></div>
            <h3 class="text-lg font-bold">OpenGL 4.6 &amp; GLSL</h3>
            <p class="text-sm text-slate-400">Vertex y fragment shaders, texturas, transformaciones e iluminación Phong.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-emerald-300">3 / 16</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de OpenGL" aria-valuenow="19" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[19%] rounded-full bg-emerald-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+500 XP <span class="text-xs text-slate-500">| Experto</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-oro/10 px-2 py-0.5 font-mono text-xs text-oro">MOD-13</span><span class="font-mono text-xs text-slate-500">Bajo nivel web</span></div>
            <h3 class="text-lg font-bold">WebAssembly &amp; Emscripten</h3>
            <p class="text-sm text-slate-400">Compilación nativa de C/C++ directo al navegador con velocidad cercana al metal.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-oro">5 / 19</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de WebAssembly" aria-valuenow="26" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[26%] rounded-full bg-oro"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+380 XP <span class="text-xs text-slate-500">| Avanzado</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-fuego/10 px-2 py-0.5 font-mono text-xs text-fuego">MOD-17</span><span class="font-mono text-xs text-slate-500">Data &amp; scripting</span></div>
            <h3 class="text-lg font-bold">Python &amp; Algoritmos</h3>
            <p class="text-sm text-slate-400">Estructuras de datos, resolución algorítmica y automatización de procesos.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-fuego">14 / 20</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de Python" aria-valuenow="70" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[70%] rounded-full bg-fuego"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+290 XP <span class="text-xs text-slate-500">| Inicial</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-rose-400/10 px-2 py-0.5 font-mono text-xs text-rose-300">MOD-20</span><span class="font-mono text-xs text-slate-500">Enterprise core</span></div>
            <h3 class="text-lg font-bold">Spring Boot &amp; Java Cloud</h3>
            <p class="text-sm text-slate-400">Arquitectura en capas, JPA, endpoints REST seguros y contenedores Docker.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-rose-300">16 / 24</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de Spring Boot" aria-valuenow="66" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-2/3 rounded-full bg-rose-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+310 XP <span class="text-xs text-slate-500">| Avanzado</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-sky-400/10 px-2 py-0.5 font-mono text-xs text-sky-300">MOD-23</span><span class="font-mono text-xs text-slate-500">Tipado estricto</span></div>
            <h3 class="text-lg font-bold">TypeScript Pro</h3>
            <p class="text-sm text-slate-400">Genéricos avanzados, decoradores, tipos condicionales y diseño de bibliotecas.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-sky-300">12 / 16</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de TypeScript" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-3/4 rounded-full bg-sky-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+290 XP <span class="text-xs text-slate-500">| Intermedio</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>

          <article class="tarjeta flex flex-col gap-3">
            <div class="flex items-center justify-between"><span class="rounded bg-pink-400/10 px-2 py-0.5 font-mono text-xs text-pink-300">MOD-16</span><span class="font-mono text-xs text-slate-500">Game dev web</span></div>
            <h3 class="text-lg font-bold">Phaser Engine &amp; JS</h3>
            <p class="text-sm text-slate-400">Física arcade, spritesheets, colisiones y publicación web de minijuegos.</p>
            <div class="mt-auto">
              <p class="flex justify-between text-xs text-slate-400"><span>Progreso de nodos</span><span class="font-mono text-pink-300">8 / 15</span></p>
              <div class="mt-1 h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso de Phaser" aria-valuenow="53" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-[53%] rounded-full bg-pink-400"></div></div>
            </div>
            <div class="flex items-center justify-between"><span class="font-mono text-sm text-neon">+260 XP <span class="text-xs text-slate-500">| Inicial</span></span><a href="#" class="btn btn-secundario px-3 py-1 text-xs">Entrenar</a></div>
          </article>
        </div>
      </section>
      <!-- /SECCION:rutas -->

      <!-- SECCION:fama -->
      <!-- ===== HALL OF FAME ===== -->
      <section id="fama" aria-labelledby="titulo-fama" class="scroll-mt-24">
        <div class="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p class="etiqueta-mono inline-block rounded border border-oro/40 px-2 py-0.5 text-[10px] text-oro">🏆 Hall of Fame · Temporada 04</p>
            <h2 id="titulo-fama" class="mt-2 text-2xl font-bold lg:text-3xl">Liga Obsidiana: Top 10 Alumnos</h2>
          </div>
          <p class="rounded-lg border border-borde px-3 py-1.5 font-mono text-xs text-slate-400">Cierre de temporada: <span class="text-neon">04d : 18h : 32m</span></p>
        </div>

        <!-- Podio: 3 columnas siempre; el 1.º mas alto y mas ancho -->
        <ol class="mt-10 grid grid-cols-[1fr_1.15fr_1fr] items-end gap-2 sm:gap-4 lg:gap-6">
          <li class="relative flex flex-col items-center gap-2 rounded-2xl border-2 border-slate-300/70 bg-panel px-1 pt-8 pb-4 text-center sm:px-4">
            <span class="absolute -top-4 grid size-8 place-items-center rounded-full border-2 border-slate-300 bg-fondo font-bold">2</span>
            <span class="grid size-12 place-items-center rounded-full border-2 border-neon/60 font-display font-bold text-neon sm:size-16 sm:text-lg">VAL</span>
            <span class="w-full truncate text-xs font-semibold sm:text-base">@DevValkyrie</span>
            <span class="font-mono text-[10px] text-slate-400">Cyber Wizard</span>
            <span class="rounded-full bg-neon/10 px-2 py-0.5 font-mono text-xs text-neon sm:text-sm">13.200 XP</span>
            <span class="hidden gap-1 text-[10px] lg:flex"><span class="rounded border border-borde px-1.5">OpenGL</span><span class="rounded border border-borde px-1.5">Rust</span></span>
            <span class="hidden text-xs text-fuego sm:block">🔥 Racha 28 días</span>
          </li>
          <li class="relative flex flex-col items-center gap-2 rounded-2xl border-2 border-oro bg-linear-to-b from-oro/15 to-panel px-1 pt-10 pb-6 text-center shadow-xl shadow-oro/20 sm:px-4 lg:pb-8">
            <span class="absolute -top-4 rounded-full bg-oro px-3 py-1 font-mono text-[10px] font-bold text-fondo uppercase"><span aria-hidden="true">👑</span> 1.º <span class="hidden sm:inline">lugar supremo</span></span>
            <span class="grid size-16 place-items-center rounded-full border-2 border-oro bg-oro/10 font-display text-lg font-bold text-oro shadow-lg shadow-oro/40 sm:size-20 sm:text-xl">NEO</span>
            <span class="w-full truncate text-sm font-bold sm:text-lg">@NeoCoder_X</span>
            <span class="font-mono text-[10px] text-oro">Gran Arquitecto Obsidian</span>
            <span class="rounded-full border border-oro/50 bg-oro/10 px-3 py-0.5 font-mono text-sm font-bold text-oro sm:text-base">14.850 XP</span>
            <span class="hidden gap-1 text-[10px] lg:flex"><span class="rounded border border-borde px-1.5">C++20</span><span class="rounded border border-borde px-1.5">SDL3 Engine</span></span>
            <span class="hidden text-xs text-fuego sm:block">🔥 Racha 45 días continuos</span>
          </li>
          <li class="relative flex flex-col items-center gap-2 rounded-2xl border-2 border-orange-500/80 bg-panel px-1 pt-8 pb-4 text-center sm:px-4">
            <span class="absolute -top-4 grid size-8 place-items-center rounded-full border-2 border-orange-500 bg-fondo font-bold">3</span>
            <span class="grid size-12 place-items-center rounded-full border-2 border-orange-500/70 font-display font-bold text-fuego sm:size-16 sm:text-lg">GLT</span>
            <span class="w-full truncate text-xs font-semibold sm:text-base">@GlitchHunter</span>
            <span class="font-mono text-[10px] text-slate-400">Kernel Master</span>
            <span class="rounded-full bg-fuego/10 px-2 py-0.5 font-mono text-xs text-fuego sm:text-sm">12.450 XP</span>
            <span class="hidden gap-1 text-[10px] lg:flex"><span class="rounded border border-borde px-1.5">WASM</span><span class="rounded border border-borde px-1.5">C++ Core</span></span>
            <span class="hidden text-xs text-fuego sm:block">🔥 Racha 19 días</span>
          </li>
        </ol>

        <!-- Puestos 4 a 10, CELULAR: lista de filas (oculta desde md) -->
        <ol start="4" class="mt-8 space-y-2 md:hidden">
          <li class="flex items-center gap-3 rounded-xl border border-borde bg-panel px-4 py-3"><span class="w-5 font-mono text-slate-400">4</span><span class="grid size-9 shrink-0 place-items-center rounded-lg bg-borde" aria-hidden="true">⚡</span><span class="min-w-0 flex-1"><span class="block truncate font-semibold">@ZeroByte_Arg</span><span class="block text-xs text-slate-400">C++ · <span class="text-emerald-400">▲ +1</span></span></span><span class="text-right font-mono">10.900<span class="block text-xs text-slate-500">XP</span></span></li>
          <li class="flex items-center gap-3 rounded-xl border border-borde bg-panel px-4 py-3"><span class="w-5 font-mono text-slate-400">5</span><span class="grid size-9 shrink-0 place-items-center rounded-lg bg-borde" aria-hidden="true">🧙</span><span class="min-w-0 flex-1"><span class="block truncate font-semibold">@PixelSage</span><span class="block text-xs text-slate-400">SDL3 · <span class="text-emerald-400">▲ +3</span></span></span><span class="text-right font-mono">9.850<span class="block text-xs text-slate-500">XP</span></span></li>
          <li class="flex items-center gap-3 rounded-xl border border-borde bg-panel px-4 py-3"><span class="w-5 font-mono text-slate-400">6</span><span class="grid size-9 shrink-0 place-items-center rounded-lg bg-borde" aria-hidden="true">🦊</span><span class="min-w-0 flex-1"><span class="block truncate font-semibold">@CodeKitsune</span><span class="block text-xs text-slate-400">OpenGL · <span class="text-rose-400">▼ −2</span></span></span><span class="text-right font-mono">8.920<span class="block text-xs text-slate-500">XP</span></span></li>
          <li class="flex items-center gap-3 rounded-xl border border-borde bg-panel px-4 py-3"><span class="w-5 font-mono text-slate-400">7</span><span class="grid size-9 shrink-0 place-items-center rounded-lg bg-borde" aria-hidden="true">⚔</span><span class="min-w-0 flex-1"><span class="block truncate font-semibold">@ByteSamurai</span><span class="block text-xs text-slate-400">WASM · <span class="text-slate-400">= 0</span></span></span><span class="text-right font-mono">8.100<span class="block text-xs text-slate-500">XP</span></span></li>
          <li class="flex items-center gap-3 rounded-xl border border-borde bg-panel px-4 py-3"><span class="w-5 font-mono text-slate-400">8</span><span class="grid size-9 shrink-0 place-items-center rounded-lg bg-borde" aria-hidden="true">🐍</span><span class="min-w-0 flex-1"><span class="block truncate font-semibold">@LaraBinary</span><span class="block text-xs text-slate-400">Python · <span class="text-emerald-400">▲ +1</span></span></span><span class="text-right font-mono">7.650<span class="block text-xs text-slate-500">XP</span></span></li>
          <li class="flex items-center gap-3 rounded-xl border border-borde bg-panel px-4 py-3"><span class="w-5 font-mono text-slate-400">9</span><span class="grid size-9 shrink-0 place-items-center rounded-lg bg-borde" aria-hidden="true">🕶</span><span class="min-w-0 flex-1"><span class="block truncate font-semibold">@MatrixWalker</span><span class="block text-xs text-slate-400">Java · <span class="text-rose-400">▼ −3</span></span></span><span class="text-right font-mono">6.980<span class="block text-xs text-slate-500">XP</span></span></li>
          <li class="flex items-center gap-3 rounded-xl border border-neon/60 bg-neon/5 px-4 py-3"><span class="w-5 font-mono text-neon">10</span><img src="/img/cursos/html/gheco-logo.webp" alt="" width="36" height="36" class="size-9 shrink-0 rounded-lg"><span class="min-w-0 flex-1"><span class="block truncate font-semibold text-neon">@GhecoDev <span class="text-xs font-normal text-slate-400">(vos)</span></span><span class="block text-xs text-slate-400">TypeScript · <span class="text-emerald-400">▲ +4</span></span></span><span class="text-right font-mono text-neon">6.400<span class="block text-xs text-slate-500">XP</span></span></li>
        </ol>

        <!-- Puestos 4 a 10, COMPUTADORA: tabla de verdad (visible desde md) -->
        <div class="mt-10 hidden overflow-hidden rounded-2xl border border-borde md:block">
          <table class="w-full text-left text-sm">
            <caption class="sr-only">Puestos 4 a 10 de la Liga Obsidiana</caption>
            <thead class="bg-panel font-mono text-[10px] tracking-widest text-slate-500 uppercase">
              <tr><th scope="col" class="px-5 py-3">Rank</th><th scope="col" class="px-5 py-3">Desarrollador</th><th scope="col" class="px-5 py-3">Rango y especialidad</th><th scope="col" class="px-5 py-3">Tendencia</th><th scope="col" class="px-5 py-3">Racha</th><th scope="col" class="px-5 py-3 text-right">Puntos</th></tr>
            </thead>
            <tbody class="divide-y divide-borde">
              <tr class="hover:bg-panel"><td class="px-5 py-3 font-mono text-neon">#04</td><th scope="row" class="px-5 py-3 font-semibold">@ZeroByte_Arg</th><td class="px-5 py-3 text-slate-400">C++ Moderno / Memory Guru</td><td class="px-5 py-3 text-emerald-400">▲ +1</td><td class="px-5 py-3 text-fuego">🔥 14d</td><td class="px-5 py-3 text-right font-mono">10.900 XP</td></tr>
              <tr class="hover:bg-panel"><td class="px-5 py-3 font-mono text-neon">#05</td><th scope="row" class="px-5 py-3 font-semibold">@PixelSage</th><td class="px-5 py-3 text-slate-400">SDL3 Engine / Game Loops</td><td class="px-5 py-3 text-emerald-400">▲ +3</td><td class="px-5 py-3 text-fuego">🔥 11d</td><td class="px-5 py-3 text-right font-mono">9.850 XP</td></tr>
              <tr class="hover:bg-panel"><td class="px-5 py-3 font-mono text-neon">#06</td><th scope="row" class="px-5 py-3 font-semibold">@CodeKitsune</th><td class="px-5 py-3 text-slate-400">OpenGL Shader Specialist</td><td class="px-5 py-3 text-rose-400">▼ −2</td><td class="px-5 py-3 text-fuego">🔥 8d</td><td class="px-5 py-3 text-right font-mono">8.920 XP</td></tr>
              <tr class="hover:bg-panel"><td class="px-5 py-3 font-mono text-neon">#07</td><th scope="row" class="px-5 py-3 font-semibold">@ByteSamurai</th><td class="px-5 py-3 text-slate-400">WebAssembly &amp; C Native</td><td class="px-5 py-3 text-slate-400">= 0</td><td class="px-5 py-3 text-fuego">🔥 18d</td><td class="px-5 py-3 text-right font-mono">8.100 XP</td></tr>
              <tr class="hover:bg-panel"><td class="px-5 py-3 font-mono text-neon">#08</td><th scope="row" class="px-5 py-3 font-semibold">@LaraBinary</th><td class="px-5 py-3 text-slate-400">Python Algorithms &amp; ML</td><td class="px-5 py-3 text-emerald-400">▲ +1</td><td class="px-5 py-3 text-fuego">🔥 15d</td><td class="px-5 py-3 text-right font-mono">7.650 XP</td></tr>
              <tr class="hover:bg-panel"><td class="px-5 py-3 font-mono text-neon">#09</td><th scope="row" class="px-5 py-3 font-semibold">@MatrixWalker</th><td class="px-5 py-3 text-slate-400">Java Spring Boot Cloud</td><td class="px-5 py-3 text-rose-400">▼ −3</td><td class="px-5 py-3 text-fuego">🔥 6d</td><td class="px-5 py-3 text-right font-mono">6.980 XP</td></tr>
              <tr class="bg-neon/5"><td class="px-5 py-3 font-mono text-neon">#10</td><th scope="row" class="px-5 py-3 font-semibold text-neon">@GhecoDev <span class="font-normal text-slate-400">(vos)</span></th><td class="px-5 py-3 text-slate-400">TypeScript Pro / Fullstack</td><td class="px-5 py-3 text-emerald-400">▲ +4</td><td class="px-5 py-3 text-fuego">🔥 9d</td><td class="px-5 py-3 text-right font-mono text-neon">6.400 XP</td></tr>
            </tbody>
          </table>
        </div>
      </section>
      <!-- /SECCION:fama -->

      <!-- SECCION:boveda -->
      <!-- ===== BOVEDA DE TOKENS ===== -->
      <section id="boveda" aria-labelledby="titulo-boveda" class="scroll-mt-24 overflow-hidden rounded-3xl border border-borde bg-panel lg:grid lg:grid-cols-2">
        <div class="p-6 sm:p-10">
          <p class="etiqueta-mono inline-flex items-center gap-2 rounded-full border border-oro/40 px-3 py-1 text-[10px] text-oro"><span class="size-1.5 rounded-full bg-oro"></span> Bóveda de coleccionables · Skill tokens</p>
          <h2 id="titulo-boveda" class="mt-4 text-2xl font-bold lg:text-3xl">Forjá tus Monedas de Maestría</h2>
          <p class="mt-3 text-slate-400">Cada módulo completado y nodo desbloqueado acuña una moneda en tu inventario. Dominá C++, JS, Rust, TS y Java para alcanzar el estatus de Arquitecto Obsidian.</p>
          <dl class="mt-6 flex gap-8 font-mono">
            <div><dt class="text-xs text-slate-500">Tokens principales</dt><dd class="text-2xl text-slate-100">6 / 6</dd></div>
            <div><dt class="text-xs text-slate-500">Trazabilidad en cadena</dt><dd class="text-2xl text-neon">100%</dd></div>
          </dl>
        </div>
        <!-- Monedas hechas con CSS + la mascota -->
        <div class="fondo-cuadricula relative flex min-h-64 items-center justify-center overflow-hidden border-t border-borde p-6 lg:border-t-0 lg:border-l">
          <img src="/img/cursos/html/gheco-512.webp" alt="Gheco, la mascota, señalando las monedas" width="512" height="512" loading="lazy" class="absolute bottom-0 left-0 size-36 rounded-full opacity-80 sm:size-48">
          <h3 class="sr-only">Monedas obtenidas</h3>
          <ul class="relative grid grid-cols-3 gap-4">
            <li class="grid size-16 animate-flotar place-items-center rounded-full border-4 border-sky-300 bg-linear-to-br from-sky-400 to-blue-700 font-display font-bold text-white shadow-lg shadow-sky-500/40 sm:size-20">C++</li>
            <li class="grid size-16 animate-flotar place-items-center rounded-full border-4 border-yellow-200 bg-linear-to-br from-yellow-300 to-amber-600 font-display font-bold text-fondo shadow-lg shadow-amber-500/40 [animation-delay:300ms] sm:size-20">JS</li>
            <li class="grid size-16 animate-flotar place-items-center rounded-full border-4 border-cyan-200 bg-linear-to-br from-cyan-400 to-blue-600 font-display font-bold text-white shadow-lg shadow-cyan-500/40 [animation-delay:600ms] sm:size-20">TS</li>
            <li class="grid size-16 animate-flotar place-items-center rounded-full border-4 border-orange-200 bg-linear-to-br from-orange-400 to-red-700 font-display font-bold text-white shadow-lg shadow-orange-500/40 [animation-delay:900ms] sm:size-20">Rust</li>
            <li class="grid size-16 animate-flotar place-items-center rounded-full border-4 border-rose-200 bg-linear-to-br from-rose-400 to-red-700 font-display font-bold text-white shadow-lg shadow-rose-500/40 [animation-delay:1200ms] sm:size-20">Java</li>
            <li class="grid size-16 animate-flotar place-items-center rounded-full border-4 border-emerald-200 bg-linear-to-br from-emerald-400 to-teal-700 font-display font-bold text-white shadow-lg shadow-emerald-500/40 [animation-delay:1500ms] sm:size-20">Py</li>
          </ul>
        </div>
      </section>
      <!-- /SECCION:boveda -->
    </main>

    <!-- SECCION:pie -->
    <!-- ===== PIE ===== -->
    <footer class="border-t border-borde">
      <div class="mx-auto grid max-w-7xl gap-6 px-4 py-8 text-sm md:grid-cols-[2fr_1fr_1fr] md:items-center">
        <div class="flex items-center gap-3">
          <img src="/img/cursos/html/gheco-logo.webp" alt="" width="36" height="36" class="size-9 rounded-lg">
          <p><span class="font-display font-bold">GhecoSoft-Code Platform</span><br><span class="text-xs text-slate-500">Formación avanzada en bajo nivel, motores de videojuegos y compilación real.</span></p>
        </div>
        <ul class="space-y-1 font-mono text-xs text-slate-400">
          <li><span class="text-emerald-400">●</span> Cloud Compiler Clang 18: online</li>
          <li><span class="text-emerald-400">●</span> GCC 14 / Emscripten: 99.98% uptime</li>
        </ul>
        <p class="font-mono text-xs text-slate-500 md:text-right">© 2026 GhecoSoft-Code.<br>Obsidian Design Protocol v4.2</p>
      </div>
    </footer>
    <!-- /SECCION:pie -->

    <!-- SECCION:barra -->
    <!-- ===== BARRA INFERIOR (solo celular y tablet) ===== -->
    <nav aria-label="Secciones" class="fixed inset-x-0 bottom-0 z-40 border-t border-borde bg-panel/95 backdrop-blur lg:hidden">
      <div class="mx-auto flex max-w-lg">
        <a href="#rutas" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">🗺</span>Campañas</a>
        <a href="#" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">📖</span>Lecciones</a>
        <a href="#fama" aria-current="page" class="my-1 flex flex-1 flex-col items-center gap-0.5 rounded-xl border border-neon/50 bg-neon/10 py-1 text-[11px] text-neon"><span aria-hidden="true" class="text-lg">⚔</span>Arena</a>
        <a href="#" class="flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] text-slate-400 hover:text-neon"><span aria-hidden="true" class="text-lg">🌳</span>Árbol</a>
      </div>
    </nav>
    <!-- /SECCION:barra -->
  </body>
</html>
```

### ¿Para qué sirve?

Ninguna página se da por terminada sin esta inspección: en cualquier empresa, antes de publicar, alguien la revisa en el celular, con el teclado y con herramientas como Lighthouse. Y publicar una página estática es gratis: GitHub Pages, Netlify o el hosting de tu escuela alcanzan. Este ventanal puede ser el primer proyecto de tu portafolio.

### Errores habituales

**Esqueleto: imagen lazy que "no carga"** en una captura de página completa o en una herramienta que no hace scroll: `loading="lazy"` espera a que la imagen se acerque a la vista. En el navegador funciona: bajá y aparece.

**Dragón: el detalle que nadie revisó.** Probá **siempre** en 390 px, con teclado y con el validador antes de dar algo por terminado. En este proyecto, esas tres revisiones encontraron: un `fieldset` que desbordaba, radios que se escapaban del scroll, un menú que se partía a 1280 px y un botón que se partía en tres líneas en el celular.

### Prueba del sello

#### ¿Qué cuatro revisiones hacés antes de dar por terminada una página?

Que el HTML sea **válido** (validador), que **no haya scroll horizontal** en el celular, que se pueda usar **con el teclado** (foco visible, saltar al contenido) y que sea **accesible** para un lector de pantalla (landmarks, títulos en orden, `alt`, tablas con `scope`). Y además, que las imágenes sean livianas.

#### ¿Por qué el CSS se compila con `--minify` para publicar?

Porque saca los espacios, los saltos de línea y los comentarios: el archivo pesa menos y la página carga más rápido, sobre todo en el celular.

#### ¿Qué le falta a esta página para ser una aplicación de verdad?

Datos y comportamiento: el login no entra a ningún lado y el ranking está escrito a mano. Para que funcione hace falta JavaScript (en la Feria de las Luces) o un servidor que arme la página con datos reales (como en el Puerto de Elefa, con PHP).

### Misión R04-N05-M1 · El árbol de habilidades

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Agregá una sección nueva: un **árbol de habilidades** con nodos completados, el actual (brillante) y los bloqueados, unidos por una **línea vertical** hecha con `before:`.

#### Criterio de aprobación

- Tres estados de nodo bien distintos: completado, actual (con brillo) y bloqueado.
- La línea que los une sale de `before:` (sin elementos extra).
- Es una lista (`ol`) y el estado se entiende también sin colores (texto o `aria-current`).

#### Cómo debe quedar

celular: capturas/R04-N05-M1-celular.webp
compu: capturas/R04-N05-M1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El árbol de habilidades</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>Árbol de habilidades</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
  <body class="fondo-cuadricula min-h-screen p-4">
    <section aria-labelledby="t" class="mx-auto max-w-3xl">
      <p class="etiqueta-mono text-neon">Skill Tree · C++</p>
      <h1 id="t" class="mt-1 text-2xl font-bold">Árbol de habilidades</h1>
      <!-- Cada nivel es una fila; la linea vertical une los niveles -->
      <ol class="relative mt-8 space-y-8 before:absolute before:inset-y-0 before:left-1/2 before:w-px before:bg-borde">
        <li class="relative flex justify-center"><span class="tarjeta border-emerald-400 py-2 text-emerald-300">✔ Punteros</span></li>
        <li class="relative flex justify-center gap-4"><span class="tarjeta border-emerald-400 py-2 text-emerald-300">✔ RAII</span><span class="tarjeta border-neon py-2 text-neon shadow-brillo">▶ Smart Pointers</span></li>
        <li class="relative flex justify-center gap-4"><span class="tarjeta py-2 text-slate-500">🔒 Move</span><span class="tarjeta py-2 text-slate-500">🔒 Templates</span><span class="tarjeta py-2 text-slate-500">🔒 Concepts</span></li>
      </ol>
    </section>
  </body>
</html>
```


### Misión R04-N05-M2 · El tema claro

```meta
entrega: codigo
entorno: navegador
monedas: 6
xp: 15
```

#### Consigna

Mostrá la tarjeta de curso en un **tema claro**, pisando **solo las variables del tema** (fondo, panel, borde, texto), sin cambiar las clases de la tarjeta.

#### Criterio de aprobación

- El tema claro sale de redefinir las variables del tema.
- La tarjeta usa las mismas clases que en el tema oscuro.
- El texto se lee bien sobre el fondo claro.

#### Cómo debe quedar

celular: capturas/R04-N05-M2-celular.webp
compu: capturas/R04-N05-M2-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>El tema claro</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>Tema claro</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
      /* Tema claro: mismos tokens, otros valores. El HTML no cambia */
      .tema-claro {
        --color-fondo: #f8fafc;
        --color-panel: #ffffff;
        --color-borde: #e2e8f0;
        --color-neon: #0891b2;
        --color-neon-suave: #0e7490;
        background: var(--color-fondo);
      }
    </style>
  </head>
  <body class="tema-claro min-h-screen p-4 text-slate-800">
    <article class="tarjeta mx-auto flex max-w-sm flex-col gap-3 border-neon/60">
      <div class="flex items-center justify-between"><span class="rounded bg-neon/10 px-2 py-0.5 font-mono text-xs text-neon">MOD-04</span><span class="font-mono text-xs text-emerald-600">Core activo</span></div>
      <h1 class="text-lg font-bold">C++ Moderno &amp; Videojuegos</h1>
      <div class="h-1.5 overflow-hidden rounded-full bg-borde" role="progressbar" aria-label="Progreso" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"><div class="h-full w-3/4 rounded-full bg-neon"></div></div>
      <a href="#" class="btn btn-primario text-white">Continuar</a>
    </article>
  </body>
</html>
```


### Encargo R04-N05-E1 · La academia de idiomas

```meta
obligatoria: no
entrega: codigo
entorno: navegador
monedas: 3
xp: 10
```

#### Consigna

Armá la misma estructura —cabecera, menú, barra inferior y grilla de tarjetas— para una **academia de idiomas**, con su propia paleta.

#### Criterio de aprobación

- Tiene cabecera, menú (compu), barra inferior (celular) y grilla de tarjetas.
- La paleta propia sale de las variables del tema.

#### Cómo debe quedar

celular: capturas/R04-N05-E1-celular.webp
compu: capturas/R04-N05-E1-compu.webp

#### Código inicial

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>La academia de idiomas</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
    <title>Academia de idiomas</title>
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

      /* 5) PROYECTO: las monedas de la boveda flotan (animate-flotar) */
      @theme {
        --animate-flotar: flotar 4s ease-in-out infinite;
        @keyframes flotar {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-6px); }
        }
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
      .marca-academia {
        --color-fondo: #fffbf5;
        --color-panel: #ffffff;
        --color-borde: #f1e4d3;
        --color-neon: #e11d48;
        --color-neon-suave: #f43f5e;
      }
    </style>
  </head>
  <body class="marca-academia min-h-screen bg-fondo pb-20 text-slate-800 lg:pb-0">
    <header class="sticky top-0 border-b border-borde bg-fondo/90 backdrop-blur">
      <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <a href="#" class="font-display text-xl font-bold">Lingua<span class="text-neon">Viva</span></a>
        <nav aria-label="Principal" class="hidden gap-6 lg:flex"><a href="#">Cursos</a><a href="#">Profesores</a><a href="#">Precios</a></nav>
        <a href="#" class="btn btn-primario px-4 py-2 text-sm text-white">Inscribirme</a>
      </div>
    </header>
    <main class="mx-auto max-w-6xl space-y-10 px-4 py-8">
      <h1 class="text-4xl font-bold lg:text-6xl">Hablá inglés en 6 meses</h1>
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <article class="tarjeta"><h2 class="font-bold">Inglés inicial</h2><p class="text-sm text-slate-500">Desde cero.</p></article>
        <article class="tarjeta"><h2 class="font-bold">Conversación</h2><p class="text-sm text-slate-500">Con nativos.</p></article>
        <article class="tarjeta"><h2 class="font-bold">Exámenes</h2><p class="text-sm text-slate-500">FCE, CAE.</p></article>
      </div>
    </main>
    <nav aria-label="Secciones" class="fixed inset-x-0 bottom-0 flex border-t border-borde bg-panel text-xs lg:hidden">
      <a href="#" aria-current="page" class="flex flex-1 flex-col items-center py-2 text-neon"><span aria-hidden="true">🏠</span>Inicio</a>
      <a href="#" class="flex flex-1 flex-col items-center py-2"><span aria-hidden="true">📚</span>Cursos</a>
      <a href="#" class="flex flex-1 flex-col items-center py-2"><span aria-hidden="true">👤</span>Mi cuenta</a>
    </nav>
  </body>
</html>
```
