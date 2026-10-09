from genhtml import m
from html_r01 import IRIS, TESELA, TEO, NORA, GHECO

COFRE = "El cofre del Gremio"
CAJONES = "Los cajones del cofre"
CABANA = "La cabaña y el castillo"
OFIDIA = "La mesa de los pergaminos de Ofidia"
TALLER = "El taller de Tesela"
MUESTRARIO = "El muestrario"
TABLON = "El tablón de encargos"
OFIDIA_IMG = "Ofidia (la líder del Valle de la Serpiente, con una túnica verde y una serpiente de luz enroscada en el brazo)"
ORCO = "el Orco del Desborde (un orco verde musgo tan ancho que no entra en el marco del vitral, con vidrios rotos clavados en la armadura, estirando los brazos)"
TW = "Con Tailwind, el **Inspector** mira las clases de cada elemento (en el orden en que las escribiste). La vista previa compila Tailwind sola."
THEME = "@theme {\n  --color-neon: #22d3ee;\n}"
BTN = "@utility btn {\n  @apply rounded-lg px-4 py-2 font-semibold;\n}"
PRIMARIO = "@utility btn-primario {\n  @apply bg-neon text-slate-950;\n}"
FONT = '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&display=swap" rel="stylesheet">'


def page(body, extra=()):
    """El bloque de Tailwind de la plataforma (con el CSS de más que haga falta) y el cuerpo, ya sin sangría."""
    import textwrap
    css = "\n".join(["@import \"tailwindcss\";", *extra])
    return '<style type="text/tailwindcss">\n' + textwrap.indent(css, "  ") + "\n</style>\n" + textwrap.dedent(body).strip("\n")


def tw(antes=(), despues=None, **kw):
    """antes: el CSS de más del bloque en el código inicial; despues: en la solución (si no, el mismo)."""
    kw["inicial"] = page(kw["inicial"], antes)
    kw["solucion"] = page(kw["solucion"], antes if despues is None else despues)
    return m(**kw)


NODOS = [
    {
        "titulo": "R03-N01 · Hola, Tailwind",
        "misiones": [
            m(id="R03-N01-P1", titulo="Abrir el cofre",
              lugar=COFRE, personajes="Iris, Tesela",
              carta="Tailwind en la plataforma | <style type=\"text/tailwindcss\"> @import \"tailwindcss\"; </style> · genera el CSS de las clases que usaste",
              recompensa="xp 10, oro 10",
              escena="""
                  Iris tardó una tarde entera en cortar los vidrios de una sola tarjeta. Entonces {mentor} abre un cofre con cientos de **plantillas** ya cortadas.
                  —Te las doy recién ahora, **porque ya sabés cortar a mano**: si una plantilla falla, vas a saber por qué.
              """,
              sugiere="En la plataforma, Tailwind se activa con un bloque `<style type=\"text/tailwindcss\">` que adentro tiene `@import \"tailwindcss\";`. " + TW,
              desafio="Agregá arriba el bloque `style` de tipo `text/tailwindcss` con `@import \"tailwindcss\";` adentro.",
              inicial='''
                  <h1 class="text-cyan-400">El cofre del Gremio</h1>
              ''',
              inspector='''
                  style[type="text/tailwindcss"]
              ''',
              solucion='''
                  <style type="text/tailwindcss">
                    @import "tailwindcss";
                  </style>
                  <h1 class="text-cyan-400">El cofre del Gremio</h1>
              ''',
              al_superar="El título se pone cian sin escribir una sola regla. Teo ya tiene las dos manos adentro del cofre.",
              imagen=["Un cofre enorme abierto, lleno de plantillas de vidrio cortadas, en una plaza.",
                      TESELA + " levanta la tapa.", IRIS + " mira asombrada.", TEO + " mete las manos adentro."]),
            tw(id="R03-N01-P2", titulo="Una plantilla, una cosa",
               lugar=COFRE, personajes="Iris, Gheco",
               carta="Utilidades | cada clase hace una sola cosa · text-cyan-400 el color · font-bold la letra gruesa",
               recompensa="xp 10, oro 10",
               escena="""
                   Cada plantilla del cofre sirve para **una sola cosa**: esta da el color cian, esta la letra gruesa.
               """,
               sugiere="Con Tailwind, el estilo va en `class`: `text-cyan-400` es el color del texto y `font-bold`, la letra gruesa. " + TW,
               desafio="Dale al `h1` las clases `text-cyan-400 font-bold`, en ese orden.",
               inicial='''
                   <h1>Plantillas del Gremio</h1>
               ''',
               inspector='''
                   h1 @class
               ''',
               solucion='''
                   <h1 class="text-cyan-400 font-bold">Plantillas del Gremio</h1>
               ''',
               al_superar="Dos plantillas, dos cosas. Gheco se pone una de color en la cola, para probar.",
               imagen=["Dos plantillas de vidrio apoyadas sobre un título, una cian y una gruesa.",
                       IRIS + " las acomoda.", GHECO + " con la cola teñida de cian."]),
            tw(id="R03-N01-P3", titulo="La tarjeta en minutos",
               lugar=COFRE, personajes="Iris, Tesela",
               carta="Fondo y relleno | bg-slate-900 el fondo · p-4 el relleno (4 = 1rem)",
               recompensa="xp 10, oro 10",
               escena="""
                   —La tarjeta que te llevó una tarde —dice {mentor}—. Hacela de nuevo.
               """,
               sugiere="`bg-slate-900` pinta el fondo y `p-4` le da relleno (`4` son `1rem`). El color del texto, `text-slate-100`.",
               desafio="Dale al `div` las clases `bg-slate-900 p-4 text-slate-100`, en ese orden.",
               inicial='''
                   <div>Encargo: ventana para el Valle</div>
               ''',
               inspector='''
                   div @class
               ''',
               solucion='''
                   <div class="bg-slate-900 p-4 text-slate-100">Encargo: ventana para el Valle</div>
               ''',
               al_superar="Iris la arma en un minuto. Se queda mirando el reloj de arena, ofendida con su propia tarde.",
               imagen=["Una tarjeta de vidrio azul oscuro recién armada sobre una mesa, junto a un reloj de arena.",
                       IRIS + " mira el reloj de arena.", TESELA + " sonríe."]),
            tw(id="R03-N01-P4", titulo="Esquinas del cofre",
               lugar=COFRE, personajes="Iris, Teo",
               carta="rounded | rounded-lg, rounded-xl, rounded-full · lo mismo que border-radius, con nombre",
               recompensa="xp 10, oro 10",
               escena="""
                   Teo encuentra el cajón de las esquinas. —¿Y esta plantilla para qué es? —Para no cortarte —le contesta Iris.
               """,
               sugiere="`rounded-xl` redondea las esquinas, como `border-radius`. Se suma a las clases que ya tiene.",
               desafio="Agregale `rounded-xl` al final de las clases del `div`.",
               inicial='''
                   <div class="bg-slate-900 p-4 text-slate-100">Encargo: ventana para el Valle</div>
               ''',
               inspector='''
                   div @class
               ''',
               solucion='''
                   <div class="bg-slate-900 p-4 text-slate-100 rounded-xl">Encargo: ventana para el Valle</div>
               ''',
               al_superar="La tarjeta queda con esquinas suaves. Teo prueba `rounded-full` en todo y le sale una página de píldoras.",
               imagen=["Una tarjeta oscura con las esquinas redondeadas.",
                       TEO + " rodeado de vidrios redondos como píldoras.", IRIS + " se ríe."]),
        ],
    },
    {
        "titulo": "R03-N02 · Las utilidades",
        "misiones": [
            tw(id="R03-N02-P1", titulo="La escala de los espacios",
               lugar=CAJONES, personajes="Iris, Tesela",
               carta="La escala | p-1 = 0.25rem · p-4 = 1rem · mb-6 = 1.5rem · se cuenta de a 0.25rem",
               recompensa="xp 10, oro 10",
               escena="""
                   El cofre tiene cajones: uno para los espacios, otro para las letras, otro para los colores. —Conocé los **cajones** y su **escala** —dice {mentor}.
               """,
               sugiere="Los espacios van de a `0.25rem`: `mb-6` es un margen de abajo de `1.5rem`. Los nombres: `m` margen, `p` relleno; `t`, `b`, `x`, `y`… el lado.",
               desafio="Separá el título del párrafo: agregale `mb-6` al `h2`.",
               inicial='''
                   <h2 class="text-xl font-bold">Los cajones</h2>
                   <p>Espacios, letras y colores.</p>
               ''',
               inspector='''
                   h2 @class
               ''',
               solucion='''
                   <h2 class="text-xl font-bold mb-6">Los cajones</h2>
                   <p>Espacios, letras y colores.</p>
               ''',
               al_superar="El título se aleja del párrafo exactamente un cajón y medio. {mentor} cierra el cajón de los espacios.",
               imagen=["Un cofre con cajones etiquetados: espacios, letras, colores.",
                       TESELA + " abre un cajón.", IRIS + " mira la escala grabada en la madera."]),
            tw(id="R03-N02-P2", titulo="El cajón de las letras",
               lugar=CAJONES, personajes="Iris, Nora",
               carta="Tipografía | text-2xl el tamaño · font-semibold el grosor · tracking-wide el espacio entre letras",
               recompensa="xp 10, oro 10",
               escena="""
                   Nora pide que el título del encargo se lea de lejos: más grande y un poco más abierto.
               """,
               sugiere="`text-2xl` agranda la letra, `font-semibold` la engrosa y `tracking-wide` separa un poco las letras.",
               desafio="Dale al `h2` las clases `text-2xl font-semibold tracking-wide`, en ese orden.",
               inicial='''
                   <h2>Encargo de Nora</h2>
               ''',
               inspector='''
                   h2 @class
               ''',
               solucion='''
                   <h2 class="text-2xl font-semibold tracking-wide">Encargo de Nora</h2>
               ''',
               al_superar="Nora pide que se lo lean. —Encargo de Nora —lee Teo, de lejos, sin entrecerrar los ojos.",
               imagen=["Un título de vitral grande y abierto, legible de lejos.",
                       NORA + " escucha.", TEO + " lee desde el fondo del taller."]),
            tw(id="R03-N02-P3", titulo="Un vidrio apenas teñido",
               lugar=CAJONES, personajes="Iris, Gheco",
               carta="Opacidad | bg-cyan-400/20 = el cian al 20 % · el número después de la barra es la opacidad",
               recompensa="xp 10, oro 10",
               escena="""
                   Iris quiere un vidrio cian, pero apenas: que se vea lo de atrás.
               """,
               sugiere="Después de un color, `/20` le baja la opacidad al 20 %: `bg-cyan-400/20`.",
               desafio="Cambiá `bg-cyan-400` por `bg-cyan-400/20` en el `div`.",
               inicial='''
                   <div class="bg-cyan-400 p-4">Vidrio teñido</div>
               ''',
               inspector='''
                   div @class
               ''',
               solucion='''
                   <div class="bg-cyan-400/20 p-4">Vidrio teñido</div>
               ''',
               al_superar="El vidrio se vuelve casi transparente. Gheco se pone atrás y se lo ve, cian clarito.",
               imagen=["Un vidrio cian muy claro, casi transparente; detrás se ve un gecko de luz.",
                       GHECO + " detrás del vidrio.", IRIS + " lo sostiene."]),
            tw(id="R03-N02-P4", titulo="El árbol de Navidad de Teo",
               lugar=CAJONES, personajes="Iris, Teo, Tesela",
               carta="Menos es más | cada clase tiene que tener una razón · si dos dicen lo mismo, gana una sola",
               recompensa="xp 10, oro 10",
               escena="""
                   Teo quiere usar todas las plantillas a la vez y arma una tarjeta que parece un árbol de Navidad. Le pone una estrella arriba.
                   —Las plantillas sueltas no sirven si no sabés para qué —lo frena {mentor}.
               """,
               sugiere="Si hay tres colores de fondo, gana uno y los otros sobran. Dejá solo lo que hace falta.",
               desafio="Dejá en la tarjeta solo estas clases, en este orden: `rounded-lg bg-slate-800 p-4 text-slate-100`.",
               inicial='''
                   <div class="tarjeta rounded-lg bg-red-500 bg-green-500 bg-slate-800 p-4 p-8 text-yellow-300 text-slate-100 animate-bounce">Encargo de Teo</div>
               ''',
               inspector='''
                   .tarjeta @class
               ''',
               solucion='''
                   <div class="tarjeta rounded-lg bg-slate-800 p-4 text-slate-100">Encargo de Teo</div>
               ''',
               al_superar="La tarjeta deja de saltar. Teo la mira un rato largo. —Es… linda —admite. Y le saca la estrella.",
               imagen=["Una tarjeta sobria y oscura al lado de una tarjeta de mil colores que salta.",
                       TEO + " le saca una estrella de la punta.", IRIS + " sonríe.", TESELA + " de brazos cruzados."]),
        ],
    },
    {
        "titulo": "R03-N03 · Flex y Grid con Tailwind",
        "misiones": [
            tw(id="R03-N03-P1", titulo="La cornisa, con plantillas",
               lugar=CABANA, personajes="Iris, Tesela",
               carta="flex con clases | flex = display: flex · justify-between = space-between · items-center = align-items: center",
               recompensa="xp 10, oro 10",
               escena="""
                   {mentor} le pide algo que parece imposible: rearmar la cornisa **sin escribir una sola regla de CSS**. —Todo lo de la regla flexible está en el cofre. Solo le cambiaron el nombre.
               """,
               sugiere="`flex` es `display: flex`, `justify-between` es `justify-content: space-between` e `items-center`, `align-items: center`.",
               desafio="Dale al `header` las clases `flex justify-between items-center`, en ese orden.",
               inicial='''
                   <header>
                     <span>Escudo</span>
                     <span>Trofeos</span>
                   </header>
               ''',
               inspector='''
                   header @class
               ''',
               solucion='''
                   <header class="flex justify-between items-center">
                     <span>Escudo</span>
                     <span>Trofeos</span>
                   </header>
               ''',
               al_superar="El escudo y los trofeos se van a sus puntas. Iris no abrió el `style` ni una vez.",
               imagen=["Una cornisa de vitral con un escudo a la izquierda y trofeos a la derecha.",
                       IRIS + " con plantillas en la mano.", TESELA + " mira."]),
            tw(id="R03-N03-P2", titulo="Los botones con su espacio",
               lugar=CABANA, personajes="Iris, Teo",
               carta="gap | gap-4 = 1rem entre los hijos · sirve en flex y en grid",
               recompensa="xp 10, oro 10",
               escena="""
                   Los cuatro botones están pegados. Teo les pone márgenes a mano, de a uno.
               """,
               sugiere="`gap-4` deja `1rem` entre todos los hijos, sin tocarlos.",
               desafio="Agregale `gap-4` a las clases del `nav`.",
               inicial='''
                   <nav class="flex">
                     <a href="#">Taller</a>
                     <a href="#">Encargos</a>
                     <a href="#">Liga</a>
                   </nav>
               ''',
               inspector='''
                   nav @class
               ''',
               solucion='''
                   <nav class="flex gap-4">
                     <a href="#">Taller</a>
                     <a href="#">Encargos</a>
                     <a href="#">Liga</a>
                   </nav>
               ''',
               al_superar="Los botones se separan parejo. Teo guarda sus márgenes en el bolsillo, por si algún día sirven.",
               imagen=["Tres botones de vidrio separados por espacios iguales.",
                       TEO + " guarda unas reglitas en el bolsillo.", IRIS + " al lado."]),
            tw(id="R03-N03-P3", titulo="La malla de dos",
               lugar=CABANA, personajes="Iris, Gheco",
               carta="grid con clases | grid grid-cols-2 = dos columnas iguales · gap-4 el espacio",
               recompensa="xp 10, oro 10",
               escena="""
                   Las tarjetas de la cabaña van de a dos, en malla.
               """,
               sugiere="`grid grid-cols-2` arma una malla de dos columnas iguales; `gap-4`, el espacio.",
               desafio="Dale al `div` de afuera las clases `grid grid-cols-2 gap-4`, en ese orden.",
               inicial='''
                   <div>
                     <div class="bg-cyan-400/20 p-4">Valle</div>
                     <div class="bg-cyan-400/20 p-4">Puerto</div>
                     <div class="bg-cyan-400/20 p-4">Forjas</div>
                     <div class="bg-cyan-400/20 p-4">Imperio</div>
                   </div>
               ''',
               inspector='''
                   body > div @class
               ''',
               solucion='''
                   <div class="grid grid-cols-2 gap-4">
                     <div class="bg-cyan-400/20 p-4">Valle</div>
                     <div class="bg-cyan-400/20 p-4">Puerto</div>
                     <div class="bg-cyan-400/20 p-4">Forjas</div>
                     <div class="bg-cyan-400/20 p-4">Imperio</div>
                   </div>
               ''',
               al_superar="Las cuatro tarjetas se ordenan de a dos. Gheco salta de una a otra, en diagonal.",
               imagen=["Cuatro vidrios cian en una malla de dos por dos.",
                       GHECO + " salta entre ellos.", IRIS + " mira."]),
            tw(id="R03-N03-P4", titulo="Una columna en la cabaña",
               lugar=CABANA, personajes="Iris, Tesela",
               carta="flex-col | flex flex-col = uno debajo del otro · gap-2 el espacio",
               recompensa="xp 10, oro 10",
               escena="""
                   En la ventanita de la cabaña, el formulario de acceso va en una sola columna: un campo debajo del otro.
               """,
               sugiere="`flex flex-col` pone los hijos **uno debajo del otro**; `gap-2` los separa un poco.",
               desafio="Dale al `form` las clases `flex flex-col gap-2`, en ese orden.",
               inicial='''
                   <form>
                     <label for="usuario">Usuario</label>
                     <input id="usuario" class="border p-2">
                     <button type="submit" class="bg-cyan-400 p-2">Entrar</button>
                   </form>
               ''',
               inspector='''
                   form @class
               ''',
               solucion='''
                   <form class="flex flex-col gap-2">
                     <label for="usuario">Usuario</label>
                     <input id="usuario" class="border p-2">
                     <button type="submit" class="bg-cyan-400 p-2">Entrar</button>
                   </form>
               ''',
               al_superar="El formulario cae en una columna prolija. {mentor} lo prueba en el espejito antes que en el castillo.",
               imagen=["Un formulario de vidrio en una sola columna, en una ventanita de cabaña.",
                       TESELA + " lo mira en un espejito.", IRIS + " al lado."]),
        ],
    },
    {
        "titulo": "R03-N04 · Responsive con Tailwind",
        "misiones": [
            tw(id="R03-N04-P1", titulo="Los pergaminos de Ofidia",
               lugar=OFIDIA, personajes="Iris, Tesela",
               carta="Prefijos | sin prefijo = la cabaña (celular) · md: desde 768 px · lg: desde 1024 px",
               recompensa="xp 10, oro 10",
               escena="""
                   Desde el Valle llega un encargo de **Ofidia**: una ventana para sus pergaminos, que se vea bien en el espejo de bolsillo de cada aldeano y en el gran salón. Iris saca el espejito antes de que {mentor} se lo alcance.
               """,
               sugiere="Lo que va **sin prefijo** es para la cabaña. `md:grid-cols-2` agrega, **desde** la ventana mediana, dos columnas.",
               desafio="Agregale `md:grid-cols-2` al final de las clases del `div` de afuera.",
               inicial='''
                   <div class="grid gap-4">
                     <div class="bg-emerald-400/20 p-4">Pergamino de los ríos</div>
                     <div class="bg-emerald-400/20 p-4">Pergamino de las cosechas</div>
                   </div>
               ''',
               inspector='''
                   body > div @class
               ''',
               solucion='''
                   <div class="grid gap-4 md:grid-cols-2">
                     <div class="bg-emerald-400/20 p-4">Pergamino de los ríos</div>
                     <div class="bg-emerald-400/20 p-4">Pergamino de las cosechas</div>
                   </div>
               ''',
               al_superar="En *Celular*, uno debajo del otro; en *Compu*, de a dos. Ofidia manda las gracias con una serpiente de luz que se enrosca en el marco.",
               imagen=["Una ventana con dos pergaminos verdes, en la cabaña uno debajo del otro y en el salón lado a lado.",
                       IRIS + " con el espejito.", OFIDIA_IMG + " en un vitral, saludando."]),
            tw(id="R03-N04-P2", titulo="El menú del castillo",
               lugar=OFIDIA, personajes="Iris, Gheco",
               carta="Esconder y mostrar | hidden = no se ve · md:flex = desde md se ve como flex",
               recompensa="xp 10, oro 10",
               escena="""
                   El menú largo no entra en la cabaña: en la cabaña va el menú de abajo, y el largo solo en el castillo.
               """,
               sugiere="`hidden` lo esconde; `md:flex` lo muestra (como flex) desde la ventana mediana.",
               desafio="Dale al `nav` las clases `hidden md:flex gap-4`, en ese orden.",
               inicial='''
                   <nav>
                     <a href="#">Taller</a>
                     <a href="#">Encargos</a>
                     <a href="#">Liga</a>
                     <a href="#">Contacto</a>
                   </nav>
               ''',
               inspector='''
                   nav @class
               ''',
               solucion='''
                   <nav class="hidden md:flex gap-4">
                     <a href="#">Taller</a>
                     <a href="#">Encargos</a>
                     <a href="#">Liga</a>
                     <a href="#">Contacto</a>
                   </nav>
               ''',
               al_superar="En *Celular* el menú desaparece; en *Compu*, vuelve. Gheco aparece y desaparece con él, para hacerse el mago.",
               imagen=["Un menú de vidrio que aparece en un ventanal grande y se esconde en una ventanita.",
                       GHECO + " haciendo de mago.", IRIS + " se ríe."]),
            tw(id="R03-N04-P3", titulo="El título que crece",
               lugar=OFIDIA, personajes="Iris, Nora",
               carta="Tamaños por pantalla | text-2xl md:text-4xl · en la cabaña chico, en el castillo grande",
               recompensa="xp 10, oro 10",
               escena="""
                   El título de los pergaminos es enorme en la cabaña y se parte en cuatro renglones.
               """,
               sugiere="Primero el tamaño de la cabaña (`text-2xl`), y con `md:text-4xl` crece en el castillo.",
               desafio="Dale al `h1` las clases `text-2xl md:text-4xl font-bold`, en ese orden.",
               inicial='''
                   <h1 class="text-5xl font-bold">Los pergaminos de Ofidia</h1>
               ''',
               inspector='''
                   h1 @class
               ''',
               solucion='''
                   <h1 class="text-2xl md:text-4xl font-bold">Los pergaminos de Ofidia</h1>
               ''',
               al_superar="El título entra en un renglón en la cabaña y crece en el castillo.",
               imagen=["Un título de vitral chico en una ventanita y grande en un ventanal.",
                       IRIS + " compara las dos ventanas.", NORA + " toca el marco."]),
            tw(id="R03-N04-P4", titulo="El contenedor del salón",
               lugar=OFIDIA, personajes="Iris, Tesela",
               carta="Contenedor | mx-auto centra · max-w-5xl pone un ancho máximo · px-4 deja aire a los costados",
               recompensa="xp 10, oro 10",
               escena="""
                   En el gran salón, el texto de los pergaminos se estira de pared a pared y no hay quien lo lea.
               """,
               sugiere="`max-w-5xl` le pone un ancho máximo, `mx-auto` lo centra y `px-4` deja aire a los costados en la cabaña.",
               desafio="Dale al `main` las clases `mx-auto max-w-5xl px-4`, en ese orden.",
               inicial='''
                   <main>
                     <p>Los pergaminos cuentan los ríos, las cosechas y las lunas del Valle.</p>
                   </main>
               ''',
               inspector='''
                   main @class
               ''',
               solucion='''
                   <main class="mx-auto max-w-5xl px-4">
                     <p>Los pergaminos cuentan los ríos, las cosechas y las lunas del Valle.</p>
                   </main>
               ''',
               al_superar="El texto se queda en el medio del salón, de un ancho que se lee. {mentor} se saca el monóculo, lo mira y se lo vuelve a poner. Todavía no.",
               imagen=["Un salón enorme con un pergamino centrado de ancho cómodo.",
                       TESELA + " con el monóculo en la mano.", IRIS + " espera."]),
        ],
    },
    {
        "titulo": "R03-N05 · Estados y transiciones",
        "misiones": [
            tw(id="R03-N05-P1", titulo="El vitral mudo",
               lugar=TALLER, personajes="Iris, Teo",
               carta="hover: | hover:bg-cyan-300 = ese fondo solo cuando el mouse está encima",
               recompensa="xp 10, oro 10",
               escena="""
                   Teo toca una tarjeta y no pasa nada. —¿Está rota? —No está rota —dice {mentor}—. Está **muda**.
               """,
               sugiere="`hover:` delante de una clase hace que se aplique **solo** cuando el mouse está encima: `hover:bg-cyan-300`.",
               desafio="Agregale `hover:bg-cyan-300` al final de las clases del botón.",
               inicial='''
                   <button type="button" class="rounded-lg bg-cyan-400 px-4 py-2">Ver encargo</button>
               ''',
               inspector='''
                   button @class
               ''',
               solucion='''
                   <button type="button" class="rounded-lg bg-cyan-400 px-4 py-2 hover:bg-cyan-300">Ver encargo</button>
               ''',
               al_superar="Teo pasa el mouse y el botón se aclara. Lo pasa cuarenta veces más.",
               imagen=["Un botón de vidrio cian que se aclara cuando se le acerca una mano.",
                       TEO + " pasa la mano una y otra vez.", IRIS + " lo mira."]),
            tw(id="R03-N05-P2", titulo="Para quien usa el teclado",
               lugar=TALLER, personajes="Iris, Nora",
               carta="focus-visible: | el anillo de foco cuando se llega con el teclado · focus-visible:ring-2",
               recompensa="xp 10, oro 10",
               escena="""
                   Nora recorre la tarjeta con el teclado, una tecla por vez, y no sabe dónde está parada: nada cambia.
               """,
               sugiere="`focus-visible:ring-2 focus-visible:ring-cyan-400` dibuja un anillo cuando llegás con el teclado (no con el mouse).",
               desafio="Agregale al botón `focus-visible:ring-2 focus-visible:ring-cyan-400`, al final.",
               inicial='''
                   <button type="button" class="rounded-lg bg-cyan-400 px-4 py-2 hover:bg-cyan-300">Ver encargo</button>
               ''',
               inspector='''
                   button @class
               ''',
               solucion='''
                   <button type="button" class="rounded-lg bg-cyan-400 px-4 py-2 hover:bg-cyan-300 focus-visible:ring-2 focus-visible:ring-cyan-400">Ver encargo</button>
               ''',
               al_superar="Nora aprieta Tab y el botón se enciende con un anillo. —Ahí estoy —dice.",
               imagen=["Un botón de vidrio rodeado de un anillo de luz cian.",
                       NORA + " con la mano sobre un teclado de vidrio.", IRIS + " al lado."]),
            tw(id="R03-N05-P3", titulo="Que se mueva suave",
               lugar=TALLER, personajes="Iris, Gheco",
               carta="transition | transition hace suave el cambio · hover:-translate-y-1 lo levanta un poquito",
               recompensa="xp 10, oro 10",
               escena="""
                   La tarjeta cambia de golpe, como un parpadeo. Iris la quiere suave, como la luz de la tarde.
               """,
               sugiere="`transition` suaviza los cambios, y `hover:-translate-y-1` levanta la tarjeta un poquito cuando el mouse pasa.",
               desafio="Agregale a la tarjeta `transition hover:-translate-y-1`, al final.",
               inicial='''
                   <article class="rounded-xl bg-slate-800 p-4 text-slate-100">Ventana para el Valle</article>
               ''',
               inspector='''
                   article @class
               ''',
               solucion='''
                   <article class="rounded-xl bg-slate-800 p-4 text-slate-100 transition hover:-translate-y-1">Ventana para el Valle</article>
               ''',
               al_superar="La tarjeta se levanta despacito cuando pasa el mouse. Gheco se sube arriba para que lo levante también.",
               imagen=["Una tarjeta de vidrio que se eleva suavemente.",
                       GHECO + " sentado arriba.", IRIS + " mira la luz."]),
            tw(id="R03-N05-P4", titulo="El vitral que se ilumina entero",
               lugar=TALLER, personajes="Iris, Tesela",
               carta="group | group en el padre · group-hover:… en un hijo · el hijo cambia cuando el mouse pasa por el padre",
               recompensa="xp 10, oro 10",
               escena="""
                   Cuando alguien se acerca a la tarjeta, Iris quiere que se encienda el **título** adentro, aunque el mouse no esté justo encima.
               """,
               sugiere="`group` en el padre, y `group-hover:text-cyan-400` en el hijo: el hijo cambia cuando el mouse pasa por **el padre**.",
               desafio="Agregale `group` al `article`, y `group-hover:text-cyan-400` al `h3`.",
               inicial='''
                   <article class="rounded-xl bg-slate-800 p-4">
                     <h3 class="font-bold text-slate-100">Ventana para el Valle</h3>
                     <p class="text-slate-400">Encargo de Ofidia</p>
                   </article>
               ''',
               inspector='''
                   article @class
                   h3 @class
               ''',
               solucion='''
                   <article class="group rounded-xl bg-slate-800 p-4">
                     <h3 class="font-bold text-slate-100 group-hover:text-cyan-400">Ventana para el Valle</h3>
                     <p class="text-slate-400">Encargo de Ofidia</p>
                   </article>
               ''',
               al_superar="El mouse roza la tarjeta y el título se enciende en cian. {mentor} se queda mirando un segundo de más.",
               imagen=["Una tarjeta de vidrio oscuro cuyo título se enciende en cian.",
                       TESELA + " la mira.", IRIS + " acerca la mano."]),
        ],
    },
    {
        "titulo": "R03-N06 · Tema propio",
        "misiones": [
            tw(antes=(), despues=(THEME,), id="R03-N06-P1", titulo="Los colores, en el cofre",
               lugar=COFRE, personajes="Iris, Tesela",
               carta="@theme | --color-neon: #22d3ee; crea text-neon, bg-neon, border-neon…",
               recompensa="xp 10, oro 10",
               escena="""
                   Iris copió `#22d3ee` en veinte lugares. Cuando el Gremio pide un cian «un poquito más claro», tiene que cambiar los veinte. Se le escapa uno. Teo lo encuentra y se ríe media hora.
                   —Grabá los colores **en el cofre** —le enseña {mentor}—. Una vez.
               """,
               sugiere="Adentro del bloque de Tailwind, `@theme { --color-neon: #22d3ee; }` crea las clases `text-neon`, `bg-neon`…",
               desafio="Agregá en el bloque un `@theme` con `--color-neon: #22d3ee;`, y cambiá la clase del `h1` a `text-neon`.",
               inicial='''
                   <h1 class="text-[#22d3ee]">GhecoSoft</h1>
               ''',
               inspector='''
                   css @theme { --color-neon }
                   h1 @class
               ''',
               solucion='''
                   <h1 class="text-neon">GhecoSoft</h1>
               ''',
               al_superar="El título usa el color por su nombre. Teo deja de reírse: ya no hay nada que encontrar.",
               imagen=["Un cofre con un frasco de color cian etiquetado «neón».",
                       IRIS + " escribe la etiqueta.", TESELA + " asiente."]),
            tw(antes=(THEME,), despues=(THEME.replace("#22d3ee", "#67e8f9"),), id="R03-N06-P2", titulo="Un cian un poquito más claro",
               lugar=COFRE, personajes="Iris, Teo",
               carta="Cambiar el tema | se cambia el valor en @theme y cambia en todos lados",
               recompensa="xp 10, oro 10",
               escena="""
                   El Gremio vuelve a pedir el cian «un poquito más claro». Teo prepara una lista para buscar los veinte lugares.
               """,
               sugiere="Con el color en el `@theme`, se cambia **una sola vez**: el valor de `--color-neon`.",
               desafio="Cambiá el valor de `--color-neon` a `#67e8f9`.",
               inicial='''
                   <h1 class="text-neon">GhecoSoft</h1>
                   <p class="text-neon">Aprendé a programar.</p>
               ''',
               inspector='''
                   css @theme { --color-neon }
               ''',
               solucion='''
                   <h1 class="text-neon">GhecoSoft</h1>
                   <p class="text-neon">Aprendé a programar.</p>
               ''',
               al_superar="Iris cambia un solo número y todo se aclara a la vez. Teo rompe su lista.",
               imagen=["Un vitral entero que cambia de cian a un cian más claro, todo a la vez.",
                       TEO + " rompe una lista de papel.", IRIS + " sonríe."]),
            tw(antes=(THEME,), despues=(THEME, "@layer base {\n  h2 { @apply font-bold text-neon; }\n}"), id="R03-N06-P3", titulo="Los títulos de fábrica",
               lugar=COFRE, personajes="Iris, Tesela",
               carta="@layer base | estilos de fábrica para etiquetas · h1 { @apply font-bold; }",
               recompensa="xp 10, oro 10",
               escena="""
                   Todos los títulos del taller van en negrita. Iris le pone `font-bold` a cada uno, de a uno.
               """,
               sugiere="`@layer base { h2 { @apply font-bold; } }` le da a **todos** los `h2` la letra gruesa, sin ponérsela a cada uno.",
               desafio="Agregá en el bloque un `@layer base` con `h2 { @apply font-bold text-neon; }`, y sacale las clases a los dos `h2`.",
               inicial='''
                   <h2 class="font-bold text-neon">Encargos</h2>
                   <h2 class="font-bold text-neon">Liga</h2>
               ''',
               inspector='''
                   css h2 { @apply }
                   h2 @class
               ''',
               solucion='''
                   <h2>Encargos</h2>
                   <h2>Liga</h2>
               ''',
               al_superar="Los títulos salen gruesos y cian de fábrica. Iris mira sus manos, sin saber qué hacer con el tiempo que le sobra.",
               imagen=["Una fila de títulos de vitral todos iguales, saliendo de un molde.",
                       IRIS + " con las manos vacías.", TESELA + " sonríe."]),
            tw(antes=(THEME,), despues=(THEME.replace("}", "  --font-display: \"Space Grotesk\", sans-serif;\n}"),), id="R03-N06-P4", titulo="La letra del taller",
               lugar=COFRE, personajes="Iris, Nora",
               carta="Fuentes | --font-display: \"Space Grotesk\", sans-serif; en @theme crea font-display",
               recompensa="xp 10, oro 10",
               escena="""
                   El taller tiene su propia letra para los títulos. Nora no la ve, pero la reconoce cuando se la leen: «suena moderna», dice.
               """,
               sugiere="En `@theme`, `--font-display: \"Space Grotesk\", sans-serif;` crea la clase `font-display`. El nombre de la fuente va entre comillas.",
               desafio="Agregá en el `@theme` la variable `--font-display` con `\"Space Grotesk\", sans-serif`.",
               inicial=FONT + '''
                   <h1 class="font-display text-neon">Los Talleres</h1>
               ''',
               inspector='''
                   css @theme { --font-display }
               ''',
               solucion=FONT + '''
                   <h1 class="font-display text-neon">Los Talleres</h1>
               ''',
               al_superar="El título toma la letra del taller. Nora pasa la mano y sonríe: —Moderna. Lo sabía.",
               imagen=["Un título de vitral con una letra moderna y geométrica.",
                       NORA + " sonríe.", IRIS + " lee en voz alta."]),
        ],
    },
    {
        "titulo": "R03-N07 · Componentes",
        "misiones": [
            tw(antes=(THEME,), despues=(THEME, BTN), id="R03-N07-P1", titulo="La pieza oficial",
               lugar=MUESTRARIO, personajes="Iris, Tesela",
               carta="@utility | @utility btn { @apply …; } · una pieza con nombre, se usa con class=\"btn\"",
               recompensa="xp 10, oro 10",
               escena="""
                   El **Orco del Desborde** asoma la cabeza por la puerta: la misma tarjeta, copiada treinta veces con treinta diferencias chiquitas. Cada copia mal hecha lo hace más fuerte.
                   {mentor} cuelga en la pared un **muestrario**: cada pieza una sola vez, la oficial.
               """,
               sugiere="`@utility btn { @apply rounded-lg px-4 py-2 font-semibold; }` crea la clase `btn`. Se escribe una vez y se usa en todos lados.",
               desafio="Agregá en el bloque `@utility btn { @apply rounded-lg px-4 py-2 font-semibold; }`, y dejale a los dos botones solo la clase `btn`.",
               inicial='''
                   <a class="rounded-lg px-4 py-2 font-semibold" href="#">Encargos</a>
                   <a class="rounded-md px-5 py-2 font-bold" href="#">Liga</a>
               ''',
               inspector='''
                   css @utility btn { @apply }
                   a @class
               ''',
               solucion='''
                   <a class="btn" href="#">Encargos</a>
                   <a class="btn" href="#">Liga</a>
               ''',
               al_superar="Los dos botones quedan idénticos. El orco pierde una de sus treinta copias y gruñe.",
               imagen=["Una pared con un muestrario de piezas de vitral, cada una una sola vez.",
                       TESELA + " cuelga una pieza.", IRIS + " al lado.", "En la puerta asoma un orco verde enorme."]),
            tw(antes=(THEME, BTN), despues=(THEME, BTN, PRIMARIO), id="R03-N07-P2", titulo="El botón principal",
               lugar=MUESTRARIO, personajes="Iris, Teo",
               carta="Variantes de componente | btn + btn-primario · la base y el color, por separado",
               recompensa="xp 10, oro 10",
               escena="""
                   Teo quiere que el botón de «Entrar» sea distinto: cian y llamativo. Pero sin copiar todo el botón.
               """,
               sugiere="Se combinan: `class=\"btn btn-primario\"`. La base en `btn` y el color en `btn-primario`, con su propio `@utility`.",
               desafio="Agregá `@utility btn-primario { @apply bg-neon text-slate-950; }` y ponele al enlace las clases `btn btn-primario`.",
               inicial='''
                   <a class="btn" href="#">Entrar</a>
               ''',
               inspector='''
                   css @utility btn-primario { @apply }
                   a @class
               ''',
               solucion='''
                   <a class="btn btn-primario" href="#">Entrar</a>
               ''',
               al_superar="El botón de Entrar brilla cian y sigue siendo un `btn`. Teo, por primera vez, no le agrega nada.",
               imagen=["Un botón de vidrio cian brillante al lado de botones grises iguales.",
                       TEO + " con las manos en los bolsillos, conteniéndose.", IRIS + " sonríe."]),
            tw(antes=(THEME, BTN, PRIMARIO), id="R03-N07-P3", titulo="Se combina con clases sueltas",
               lugar=MUESTRARIO, personajes="Iris, Tesela",
               carta="Componente + clases | btn btn-primario w-full sm:w-auto · el componente no impide ajustar",
               recompensa="xp 10, oro 10",
               escena="""
                   En la cabaña, el botón de Entrar tiene que ocupar todo el ancho; en el castillo, su ancho justo.
               """,
               sugiere="Un componente se combina con clases sueltas: `btn btn-primario w-full sm:w-auto`.",
               desafio="Agregale `w-full sm:w-auto` al final de las clases del enlace.",
               inicial='''
                   <a class="btn btn-primario" href="#">Entrar</a>
               ''',
               inspector='''
                   a @class
               ''',
               solucion='''
                   <a class="btn btn-primario w-full sm:w-auto" href="#">Entrar</a>
               ''',
               al_superar="En la cabaña, el botón se estira de lado a lado. En el castillo, vuelve a su tamaño.",
               imagen=["Un botón cian que en una ventanita ocupa todo el ancho y en un ventanal es chico.",
                       TESELA + " lo mira en el espejito.", IRIS + " al lado."]),
            tw(antes=(THEME,), despues=(THEME, "@utility chip {\n  @apply rounded-full px-3 py-1 text-xs;\n}"), id="R03-N07-P4", titulo="El chip del curso",
               lugar=MUESTRARIO, personajes="Iris, Gheco",
               carta="No todo es componente | si se usa una vez, clases sueltas · si se repite, @utility",
               recompensa="xp 10, oro 10",
               escena="""
                   Las tarjetas de los cursos llevan un chip con el lenguaje, y se repite en ocho tarjetas. Va al muestrario.
               """,
               sugiere="Lo que se repite va a un `@utility`. `@utility chip { @apply rounded-full px-3 py-1 text-xs; }`.",
               desafio="Agregá `@utility chip { @apply rounded-full px-3 py-1 text-xs; }` y ponele `chip` a los tres `span`.",
               inicial='''
                   <span class="rounded-full px-3 py-1 text-xs">Python</span>
                   <span class="rounded-full px-3 py-1 text-xs">Java</span>
                   <span class="rounded-full px-3 py-1 text-xs">C++</span>
               ''',
               inspector='''
                   css @utility chip { @apply }
                   span @class
               ''',
               solucion='''
                   <span class="chip">Python</span>
                   <span class="chip">Java</span>
                   <span class="chip">C++</span>
               ''',
               al_superar="Tres chips iguales. El muestrario ya tiene botones y chips. Iris le agrega una etiqueta prolija debajo de cada pieza.",
               imagen=["Un muestrario de vidrio con botones y chips redondos de colores, cada uno con su etiqueta.",
                       GHECO + " señala un chip.", IRIS + " escribe etiquetas."]),
        ],
    },
    {
        "titulo": "R03-N08 · Jefe: el Orco del Desborde",
        "misiones": [
            tw(id="R03-N08-P1", titulo="La imagen que estira la pared",
               lugar=TABLON, personajes="Iris, Tesela",
               criatura="orco",
               carta="Imágenes que entran | max-w-full h-auto · nunca más ancha que su caja",
               recompensa="xp 15, oro 15",
               escena="""
                   El Orco del Desborde entró al taller y estiró el **tablón de encargos** con sus manos enormes. En la ventanita de la cabaña todo se sale por el costado.
                   —Mirá la cabaña, no el castillo —dice {mentor}—. **En el celular, se ve todo.**
               """,
               sugiere="`max-w-full h-auto` hace que la imagen nunca sea más ancha que su caja.",
               desafio="Cambiá la clase `w-[900px]` de la imagen por `max-w-full h-auto`.",
               inicial='''
                   <img src="/img/cursos/html/heroe-896.webp" alt="El aprendiz con su buzo de circuitos" width="896" height="896" class="w-[900px]">
               ''',
               inspector='''
                   img @class
               ''',
               solucion='''
                   <img src="/img/cursos/html/heroe-896.webp" alt="El aprendiz con su buzo de circuitos" width="896" height="896" class="max-w-full h-auto">
               ''',
               al_superar="La imagen entra en la cabaña. El orco pierde un brazo de ancho.",
               imagen=["Un tablón de encargos de madera que se encoge para entrar en una ventanita.",
                       ORCO, IRIS + " con el espejito."]),
            tw(id="R03-N08-P2", titulo="La dirección larguísima",
               lugar=TABLON, personajes="Iris, Gheco",
               criatura="orco",
               carta="break-all | corta las palabras larguísimas (direcciones, códigos) donde haga falta",
               recompensa="xp 15, oro 15",
               escena="""
                   La dirección para seguir el encargo es una sola palabra larguísima, y empuja la pared.
               """,
               sugiere="`break-all` deja cortar una palabra larguísima en cualquier letra, para que entre.",
               desafio="Agregale `break-all` al párrafo de la dirección.",
               inicial='''
                   <p>Seguí tu encargo en: https://talleres-de-los-vitrales.example/encargos/ventanal-del-gran-castillo-de-la-montana</p>
               ''',
               inspector='''
                   p @class
               ''',
               solucion='''
                   <p class="break-all">Seguí tu encargo en: https://talleres-de-los-vitrales.example/encargos/ventanal-del-gran-castillo-de-la-montana</p>
               ''',
               al_superar="La dirección se corta en dos renglones y entra. El orco pierde el otro brazo de ancho.",
               imagen=["Un cartel con una dirección larguísima que se dobla en dos renglones.",
                       ORCO, GHECO + " dobla el cartel."]),
            tw(id="R03-N08-P3", titulo="La tabla que no entra",
               lugar=TABLON, personajes="Iris, Nora",
               criatura="orco",
               carta="overflow-x-auto | un contenedor que se desliza de costado · la tabla entera, sin romper la página",
               recompensa="xp 15, oro 15",
               escena="""
                   La tabla de encargos tiene seis columnas y en la cabaña no entra de ninguna forma.
               """,
               sugiere="Envolvé la tabla en un `div` con `overflow-x-auto`: la **tabla** se desliza de costado, no la página entera.",
               desafio="Envolvé la tabla en un `div` con la clase `overflow-x-auto`.",
               inicial='''
                   <table class="min-w-[40rem]">
                     <tr><th>Encargo</th><th>Cliente</th><th>Vidrios</th><th>Plomo</th><th>Entrega</th><th>Estado</th></tr>
                     <tr><td>Ventanal</td><td>Kaffa</td><td>12</td><td>8 kg</td><td>Lunes</td><td>En curso</td></tr>
                   </table>
               ''',
               inspector='''
                   div.overflow-x-auto > table #
               ''',
               solucion='''
                   <div class="overflow-x-auto">
                     <table class="min-w-[40rem]">
                       <tr><th>Encargo</th><th>Cliente</th><th>Vidrios</th><th>Plomo</th><th>Entrega</th><th>Estado</th></tr>
                       <tr><td>Ventanal</td><td>Kaffa</td><td>12</td><td>8 kg</td><td>Lunes</td><td>En curso</td></tr>
                     </table>
                   </div>
               ''',
               al_superar="La tabla se desliza sola, sin mover la página. Nora la recorre de punta a punta sin perderse.",
               imagen=["Una tabla de vidrio que se desliza de costado dentro de un marco, sin moverlo.",
                       ORCO + " encogido.", NORA + " recorre la tabla."]),
            tw(id="R03-N08-P4", titulo="El ancho fijo",
               lugar=TABLON, personajes="Iris, Tesela",
               criatura="orco",
               carta="Anchos que se adaptan | w-full max-w-xl · nunca un ancho fijo más grande que la cabaña",
               recompensa="xp 20, oro 25",
               item="Plantilla del Vidriero",
               escena="""
                   Queda la última trampa del orco: la tarjeta del tablón tiene un ancho fijo de 600 píxeles.
               """,
               sugiere="En vez de un ancho fijo, `w-full max-w-xl`: ocupa todo lo que hay, pero nunca más que `max-w-xl`.",
               desafio="Cambiá `w-[600px]` por `w-full max-w-xl` en la tarjeta.",
               inicial='''
                   <article class="w-[600px] rounded-xl bg-slate-800 p-4 text-slate-100">Tablón de encargos</article>
               ''',
               inspector='''
                   article @class
               ''',
               solucion='''
                   <article class="w-full max-w-xl rounded-xl bg-slate-800 p-4 text-slate-100">Tablón de encargos</article>
               ''',
               al_superar="El orco se queda sin lugar adonde estirarse y sale por la puerta, de costado. En el fondo del cofre, donde estaba sentado, queda una plantilla vieja que no es del Gremio: un vitral redondo, con la inscripción **«para quien llegue»**. Es la letra del Vidriero: **la Plantilla del Vidriero**.",
               imagen=["Un taller ordenado; un orco enorme sale por la puerta de costado.",
                       IRIS + " sostiene una plantilla vieja de un vitral redondo con una inscripción a mano.", TESELA + " la mira, pálida."]),
        ],
    },
]
