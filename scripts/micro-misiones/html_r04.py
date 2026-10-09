from html_r01 import IRIS, TESELA, TEO, NORA, GHECO
from genhtml import m
from html_r03 import tw, THEME, BTN, PRIMARIO

CATEDRAL = "La Gran Catedral de los Vitrales"
VIDRIERO = "El taller del Vidriero"
DRAGON = "el Dragón de los Talleres (un dragón de plomo y vidrio con escamas como teselas de colores y una lupa enorme en la garra)"

NODOS = [
    {
        "titulo": "R04-N01 · El marco: navegación",
        "misiones": [
            tw(id="R04-N01-P1", titulo="La cornisa que no se va",
               lugar=CATEDRAL, personajes="Iris, Tesela",
               carta="sticky con clases | sticky top-0 z-10 · queda arriba al bajar y por encima del resto",
               recompensa="xp 10, oro 10",
               escena="""
                   El Gremio le encarga a {mentor} **el gran ventanal**: la plataforma **GhecoSoft-Code**, la misma por la que se aprende en todos los mundos. {mentor} se lo pasa a Iris. —Empezá por el **marco**: arriba, abajo y cómo se llega a cada parte.
               """,
               sugiere="`sticky top-0` la deja pegada arriba al bajar, y `z-10` la pone por encima de lo que pasa por debajo.",
               desafio="Agregale al `header` las clases `sticky top-0 z-10`, al principio.",
               inicial='''
                   <header class="bg-slate-950/90 p-4 text-slate-100">GhecoSoft-Code</header>
                   <main class="h-[200rem] p-4">El gran ventanal…</main>
               ''',
               inspector='''
                   header @class
               ''',
               solucion='''
                   <header class="sticky top-0 z-10 bg-slate-950/90 p-4 text-slate-100">GhecoSoft-Code</header>
                   <main class="h-[200rem] p-4">El gran ventanal…</main>
               ''',
               al_superar="La cornisa acompaña al bajar. Iris no tira ningún boceto en toda la mañana. Teo se preocupa y le pregunta si se siente bien.",
               imagen=["Una catedral gótica enorme con un ventanal en obra, andamios y una cornisa ya colocada.",
                       IRIS + " en un andamio.", TEO + " abajo, preocupado."]),
            tw(id="R04-N01-P2", titulo="La barra de la cabaña",
               lugar=CATEDRAL, personajes="Iris, Gheco",
               carta="fixed | fixed inset-x-0 bottom-0 · una barra pegada abajo · md:hidden la saca en el castillo",
               recompensa="xp 10, oro 10",
               escena="""
                   En la cabaña, el menú va abajo, al alcance del pulgar. En el castillo no hace falta: ya está arriba.
               """,
               sugiere="`fixed inset-x-0 bottom-0` la pega abajo de todo, de lado a lado; `md:hidden` la esconde desde la ventana mediana.",
               desafio="Dale al `nav` de abajo las clases `fixed inset-x-0 bottom-0 md:hidden`, al principio.",
               inicial='''
                   <nav class="flex justify-around bg-slate-900 p-3 text-slate-100">
                     <a href="#">Inicio</a>
                     <a href="#">Árbol</a>
                     <a href="#">Liga</a>
                   </nav>
               ''',
               inspector='''
                   nav @class
               ''',
               solucion='''
                   <nav class="fixed inset-x-0 bottom-0 md:hidden flex justify-around bg-slate-900 p-3 text-slate-100">
                     <a href="#">Inicio</a>
                     <a href="#">Árbol</a>
                     <a href="#">Liga</a>
                   </nav>
               ''',
               al_superar="En *Celular* la barra queda abajo; en *Compu* desaparece. Gheco se acuesta encima, como en una hamaca.",
               imagen=["Una ventanita de cabaña con una barra de vidrio pegada abajo.",
                       GHECO + " acostado sobre la barra.", IRIS + " mira."]),
            tw(id="R04-N01-P3", titulo="El atajo escondido",
               lugar=CATEDRAL, personajes="Iris, Nora",
               carta="sr-only | lo lee el lector de pantalla pero no se ve · focus:not-sr-only lo muestra al llegar con el teclado",
               recompensa="xp 10, oro 10",
               escena="""
                   Nora pide el atajo de siempre, «Saltar al contenido». Teo dice que queda feo arriba de todo.
               """,
               sugiere="`sr-only` lo esconde a la vista pero no al lector de pantalla; `focus:not-sr-only` lo muestra cuando se llega con el teclado.",
               desafio="Dale al enlace de salto las clases `sr-only focus:not-sr-only`.",
               inicial='''
                   <a href="#contenido">Saltar al contenido</a>
                   <header class="p-4">GhecoSoft-Code</header>
                   <main id="contenido" class="p-4">El gran ventanal…</main>
               ''',
               inspector='''
                   a[href="#contenido"] @class
               ''',
               solucion='''
                   <a href="#contenido" class="sr-only focus:not-sr-only">Saltar al contenido</a>
                   <header class="p-4">GhecoSoft-Code</header>
                   <main id="contenido" class="p-4">El gran ventanal…</main>
               ''',
               al_superar="Teo no lo ve. Nora aprieta Tab y aparece. Los dos contentos.",
               imagen=["Un ventanal con un cartel de atajo que aparece solo cuando alguien se acerca con un bastón.",
                       NORA + " con su bastón de vidrio.", TEO + " no lo ve y se encoge de hombros."]),
            tw(id="R04-N01-P4", titulo="Dos menús con nombre",
               lugar=CATEDRAL, personajes="Iris, Nora",
               carta="aria-label | le pone nombre a lo que no tiene texto visible · dos nav: «Principal» y «Atajos»",
               recompensa="xp 10, oro 10",
               escena="""
                   El ventanal tiene dos menús: el de arriba y la barra de abajo. Nora los encuentra a los dos, pero se llaman igual: «navegación».
               """,
               sugiere="Si hay dos `nav`, cada uno necesita un nombre: `aria-label=\"Principal\"` y `aria-label=\"Atajos\"`.",
               desafio="Ponele `aria-label=\"Principal\"` al primer `nav` y `aria-label=\"Atajos\"` al segundo.",
               inicial='''
                   <nav class="hidden md:flex gap-4 p-4"><a href="#">Cursos</a><a href="#">Liga</a></nav>
                   <nav class="flex gap-4 p-4 md:hidden"><a href="#">Inicio</a><a href="#">Árbol</a></nav>
               ''',
               inspector='''
                   nav @aria-label
               ''',
               solucion='''
                   <nav aria-label="Principal" class="hidden md:flex gap-4 p-4"><a href="#">Cursos</a><a href="#">Liga</a></nav>
                   <nav aria-label="Atajos" class="flex gap-4 p-4 md:hidden"><a href="#">Inicio</a><a href="#">Árbol</a></nav>
               ''',
               al_superar="—Navegación principal. Navegación de atajos —lee Nora—. Ahora sí sé cuál es cuál.",
               imagen=["Dos menús de vidrio, uno arriba y uno abajo, cada uno con su placa grabada.",
                       NORA + " toca las placas.", IRIS + " las grabó."]),
        ],
    },
    {
        "titulo": "R04-N02 · El panel central: hero y acceso",
        "misiones": [
            tw(id="R04-N02-P1", titulo="Tres capas de vidrio",
               lugar=CATEDRAL, personajes="Iris, Tesela",
               carta="Capas | relative en el padre · absolute inset-0 en la capa · la imagen ocupa todo el panel",
               recompensa="xp 10, oro 10",
               escena="""
                   El panel central lleva la figura del aprendiz de fondo y el texto encima. —Son tres capas de vidrio, una encima de la otra —dice {mentor}—. Pensalas en orden.
               """,
               sugiere="El panel lleva `relative`; la imagen, `absolute inset-0 h-full w-full object-cover`: ocupa todo el panel, de fondo.",
               desafio="Agregale `relative` al `section`, y a la imagen `absolute inset-0 h-full w-full object-cover`.",
               inicial='''
                   <section class="h-80 overflow-hidden rounded-xl">
                     <img src="/img/cursos/html/heroe-896.webp" alt="" class="">
                     <h1 class="p-6 text-3xl font-bold text-white">Aprendé a programar</h1>
                   </section>
               ''',
               inspector='''
                   section @class
                   img @class
               ''',
               solucion='''
                   <section class="relative h-80 overflow-hidden rounded-xl">
                     <img src="/img/cursos/html/heroe-896.webp" alt="" class="absolute inset-0 h-full w-full object-cover">
                     <h1 class="p-6 text-3xl font-bold text-white">Aprendé a programar</h1>
                   </section>
               ''',
               al_superar="La figura llena el panel de fondo. El título queda… tapado. Iris ya sabe por qué.",
               imagen=["Un panel de vitral con una figura de fondo y un título encima a medio ver.",
                       IRIS + " acomoda capas de vidrio.", TESELA + " observa."]),
            tw(id="R04-N02-P2", titulo="El texto, encima y legible",
               lugar=CATEDRAL, personajes="Iris, Nora",
               carta="Velo y orden | un velo absolute inset-0 bg-slate-950/60 · el texto con relative queda arriba",
               recompensa="xp 10, oro 10",
               escena="""
                   El título quedó debajo de la imagen. Y aunque lo subas, sobre la figura no se lee.
               """,
               sugiere="Un velo oscuro (`absolute inset-0 bg-slate-950/60`) entre la imagen y el texto, y el texto con `relative` para que quede arriba.",
               desafio="Al `div` del velo dale `absolute inset-0 bg-slate-950/60`, y agregale `relative` al principio de las clases del `h1`.",
               inicial='''
                   <section class="relative h-80 overflow-hidden rounded-xl">
                     <img src="/img/cursos/html/heroe-896.webp" alt="" class="absolute inset-0 h-full w-full object-cover">
                     <div></div>
                     <h1 class="p-6 text-3xl font-bold text-white">Aprendé a programar</h1>
                   </section>
               ''',
               inspector='''
                   section > div @class
                   h1 @class
               ''',
               solucion='''
                   <section class="relative h-80 overflow-hidden rounded-xl">
                     <img src="/img/cursos/html/heroe-896.webp" alt="" class="absolute inset-0 h-full w-full object-cover">
                     <div class="absolute inset-0 bg-slate-950/60"></div>
                     <h1 class="relative p-6 text-3xl font-bold text-white">Aprendé a programar</h1>
                   </section>
               ''',
               al_superar="El título se lee sobre la figura. Nora pasa la mano por el panel: —¿Y qué dice la figura? —Iris ya le había puesto `alt=\"\"`: es decoración. —Bien —dice Nora—. Entonces no me la leas.",
               imagen=["Un panel de vitral con una figura oscurecida de fondo y un título blanco bien legible encima.",
                       NORA + " pasa la mano por el panel.", IRIS + " al lado."]),
            tw(id="R04-N02-P3", titulo="La puerta de entrada",
               lugar=CATEDRAL, personajes="Iris, Gheco",
               carta="autocomplete | autocomplete=\"username\" y \"current-password\" · el navegador completa la clave guardada",
               recompensa="xp 10, oro 10",
               escena="""
                   Al costado del panel va el portal de acceso. Gheco se olvida su clave tres veces por día.
               """,
               sugiere="`autocomplete=\"username\"` y `autocomplete=\"current-password\"` le dicen al navegador qué es cada campo, para completarlo solo.",
               desafio="Agregale `autocomplete=\"username\"` al usuario y `autocomplete=\"current-password\"` a la clave.",
               inicial='''
                   <form class="flex flex-col gap-2 rounded-xl bg-slate-900 p-4 text-slate-100">
                     <label for="usuario">Usuario</label>
                     <input id="usuario" name="usuario" required class="rounded border border-slate-600 bg-slate-950 p-2">
                     <label for="clave">Contraseña</label>
                     <input id="clave" name="clave" type="password" required class="rounded border border-slate-600 bg-slate-950 p-2">
                   </form>
               ''',
               inspector='''
                   input @autocomplete
               ''',
               solucion='''
                   <form class="flex flex-col gap-2 rounded-xl bg-slate-900 p-4 text-slate-100">
                     <label for="usuario">Usuario</label>
                     <input id="usuario" name="usuario" autocomplete="username" required class="rounded border border-slate-600 bg-slate-950 p-2">
                     <label for="clave">Contraseña</label>
                     <input id="clave" name="clave" type="password" autocomplete="current-password" required class="rounded border border-slate-600 bg-slate-950 p-2">
                   </form>
               ''',
               al_superar="El navegador le ofrece a Gheco su clave guardada. Gheco finge que se la acordaba.",
               imagen=["Un portal de acceso de vidrio con dos campos que se completan solos.",
                       GHECO + " silba disimulando.", IRIS + " se ríe."]),
            tw(antes=(THEME, BTN, PRIMARIO), id="R04-N02-P4", titulo="Los dos botones del hero",
               lugar=CATEDRAL, personajes="Iris, Tesela",
               carta="Botón principal y secundario | uno lleno (btn-primario) y uno con borde · el más importante, más fuerte",
               recompensa="xp 10, oro 10",
               escena="""
                   El hero tiene dos botones: «Empezá gratis» y «Ver los cursos». —No pueden gritar los dos —dice {mentor}—. Uno manda; el otro acompaña.
               """,
               sugiere="El principal, lleno: `btn btn-primario`. El secundario, solo con borde: `btn border border-neon text-neon`.",
               desafio="Dale a «Empezá gratis» las clases `btn btn-primario`, y a «Ver los cursos», `btn border border-neon text-neon`.",
               inicial='''
                   <div class="flex gap-3">
                     <a href="#" class="btn">Empezá gratis</a>
                     <a href="#cursos" class="btn">Ver los cursos</a>
                   </div>
               ''',
               inspector='''
                   a @class
               ''',
               solucion='''
                   <div class="flex gap-3">
                     <a href="#" class="btn btn-primario">Empezá gratis</a>
                     <a href="#cursos" class="btn border border-neon text-neon">Ver los cursos</a>
                   </div>
               ''',
               al_superar="Un botón brilla, el otro acompaña. {mentor} mira el panel central entero desde la cabaña y desde el castillo. No dice nada. Eso, en {mentor}, es mucho.",
               imagen=["Dos botones de vidrio: uno cian lleno y otro con borde cian.",
                       TESELA + " mira el panel desde lejos.", IRIS + " espera."]),
        ],
    },
    {
        "titulo": "R04-N03 · Los vidrios de las rutas",
        "misiones": [
            tw(id="R04-N03-P1", titulo="La sección con su título",
               lugar=CATEDRAL, personajes="Iris, Nora",
               carta="aria-labelledby | la section toma el nombre de su título · section aria-labelledby=\"id-del-h2\"",
               recompensa="xp 10, oro 10",
               escena="""
                   Debajo del panel central van los vidrios de las rutas: ocho cursos. Nora quiere saber cómo se llama esa zona cuando llega.
               """,
               sugiere="Con `id` en el `h2` y `aria-labelledby` con ese id en la `section`, la sección se llama como su título.",
               desafio="Ponele `id=\"rutas-titulo\"` al `h2` y `aria-labelledby=\"rutas-titulo\"` a la `section`.",
               inicial='''
                   <section class="p-4">
                     <h2 class="text-2xl font-bold">Elegí tu ruta</h2>
                   </section>
               ''',
               inspector='''
                   section @aria-labelledby
                   h2 @id
               ''',
               solucion='''
                   <section aria-labelledby="rutas-titulo" class="p-4">
                     <h2 id="rutas-titulo" class="text-2xl font-bold">Elegí tu ruta</h2>
                   </section>
               ''',
               al_superar="—Región: Elegí tu ruta —lee Nora—. Me gusta. Suena a que puedo elegir.",
               imagen=["Una franja de vitral con un título grabado en una placa.",
                       NORA + " toca la placa.", IRIS + " al lado."]),
            tw(id="R04-N03-P2", titulo="De a uno, de a dos, de a cuatro",
               lugar=CATEDRAL, personajes="Iris, Teo",
               carta="Varios prefijos | grid gap-4 sm:grid-cols-2 lg:grid-cols-4 · una clase por tamaño de ventana",
               recompensa="xp 10, oro 10",
               escena="""
                   En la cabaña, los vidrios de las rutas van de a uno; en una ventana mediana, de a dos; en el castillo, de a cuatro. Teo propone un noveno color.
               """,
               sugiere="Se suman prefijos: `sm:grid-cols-2` desde la ventana chica-mediana y `lg:grid-cols-4` desde la grande.",
               desafio="Dale a la grilla las clases `grid gap-4 sm:grid-cols-2 lg:grid-cols-4`, en ese orden.",
               inicial='''
                   <div>
                     <article class="rounded-xl bg-emerald-500/20 p-4">Python</article>
                     <article class="rounded-xl bg-amber-500/20 p-4">Java</article>
                     <article class="rounded-xl bg-orange-500/20 p-4">C</article>
                     <article class="rounded-xl bg-violet-500/20 p-4">C++</article>
                   </div>
               ''',
               inspector='''
                   body > div @class
               ''',
               solucion='''
                   <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                     <article class="rounded-xl bg-emerald-500/20 p-4">Python</article>
                     <article class="rounded-xl bg-amber-500/20 p-4">Java</article>
                     <article class="rounded-xl bg-orange-500/20 p-4">C</article>
                     <article class="rounded-xl bg-violet-500/20 p-4">C++</article>
                   </div>
               ''',
               al_superar="Los vidrios se acomodan solos en cada ventana. Nadie le contesta a Teo lo del noveno color.",
               imagen=["Cuatro vidrios de colores (verde, oro, naranja, violeta) acomodados en fila en un ventanal.",
                       TEO + " sostiene un vidrio rosa que nadie pidió.", IRIS + " sonríe."]),
            tw(id="R04-N03-P3", titulo="Los filtros que empujan la pared",
               lugar=CATEDRAL, personajes="Iris, Tesela",
               criatura="orco",
               carta="Filtros que no desbordan | flex gap-2 overflow-x-auto · se deslizan adentro, no empujan la página",
               recompensa="xp 10, oro 10",
               escena="""
                   —Y cuidado con los filtros de arriba —advierte {mentor}—: son justo el escondite favorito del orco. No pueden empujar la pared hacia afuera.
               """,
               sugiere="`overflow-x-auto` en la fila de filtros: si no entran, se deslizan **adentro** de su fila, sin empujar la página.",
               desafio="Agregale `overflow-x-auto` al final de las clases de la fila de filtros.",
               inicial='''
                   <div class="flex gap-2">
                     <button type="button" class="shrink-0 rounded-full border px-3 py-1">Todos</button>
                     <button type="button" class="shrink-0 rounded-full border px-3 py-1">Desde cero</button>
                     <button type="button" class="shrink-0 rounded-full border px-3 py-1">Con juegos</button>
                     <button type="button" class="shrink-0 rounded-full border px-3 py-1">Para la facultad</button>
                     <button type="button" class="shrink-0 rounded-full border px-3 py-1">Próximamente</button>
                   </div>
               ''',
               inspector='''
                   body > div @class
               ''',
               solucion='''
                   <div class="flex gap-2 overflow-x-auto">
                     <button type="button" class="shrink-0 rounded-full border px-3 py-1">Todos</button>
                     <button type="button" class="shrink-0 rounded-full border px-3 py-1">Desde cero</button>
                     <button type="button" class="shrink-0 rounded-full border px-3 py-1">Con juegos</button>
                     <button type="button" class="shrink-0 rounded-full border px-3 py-1">Para la facultad</button>
                     <button type="button" class="shrink-0 rounded-full border px-3 py-1">Próximamente</button>
                   </div>
               ''',
               al_superar="En la cabaña, los filtros se deslizan con el dedo y la pared no se mueve. Un orquito que se había escondido ahí se va, desilusionado.",
               imagen=["Una fila de botones redondos que se desliza dentro de su marco en una ventanita.",
                       "Un orco chiquito se va desilusionado.", IRIS + " con el espejito."]),
            tw(id="R04-N03-P4", titulo="Las imágenes que esperan",
               lugar=CATEDRAL, personajes="Iris, Gheco",
               carta="loading=\"lazy\" | la imagen se baja recién cuando se acerca a la pantalla · ahorra datos en el celular",
               recompensa="xp 10, oro 10",
               escena="""
                   Cada vidrio de ruta tiene su imagen, y en el celular se bajan las ocho de golpe, aunque estén muy abajo.
               """,
               sugiere="`loading=\"lazy\"` en una imagen: el navegador la baja recién cuando se acerca a la pantalla.",
               desafio="Agregale `loading=\"lazy\"` a las dos imágenes.",
               inicial='''
                   <article class="rounded-xl p-4"><img src="/img/cursos/html/gheco-512.webp" alt="" width="128" height="128"> Python</article>
                   <article class="rounded-xl p-4"><img src="/img/cursos/html/vitral.webp" alt="" width="128" height="128"> HTML y CSS</article>
               ''',
               inspector='''
                   img @loading
               ''',
               solucion='''
                   <article class="rounded-xl p-4"><img src="/img/cursos/html/gheco-512.webp" alt="" width="128" height="128" loading="lazy"> Python</article>
                   <article class="rounded-xl p-4"><img src="/img/cursos/html/vitral.webp" alt="" width="128" height="128" loading="lazy"> HTML y CSS</article>
               ''',
               al_superar="Las imágenes esperan su turno. Gheco también: se pone en la fila, detrás de la última.",
               imagen=["Una fila de vitrales que se encienden de a uno a medida que alguien camina.",
                       GHECO + " espera en la fila.", IRIS + " camina."]),
        ],
    },
    {
        "titulo": "R04-N04 · El Hall of Fame",
        "misiones": [
            tw(id="R04-N04-P1", titulo="El podio imponente",
               lugar=CATEDRAL, personajes="Iris, Teo",
               carta="El podio con clases | grid grid-cols-3 items-end gap-2 · el del medio, más alto",
               recompensa="xp 10, oro 10",
               escena="""
                   En lo más alto del ventanal van los campeones de la **Liga Obsidiana**. Teo ya está practicando la pose del primer puesto.
               """,
               sugiere="`grid grid-cols-3 items-end gap-2`: tres columnas, apoyadas abajo, con espacio entre ellas.",
               desafio="Dale al `ol` del podio las clases `grid grid-cols-3 items-end gap-2`, en ese orden.",
               inicial='''
                   <ol>
                     <li class="h-24 bg-slate-400/40 text-center">2 · Nadia</li>
                     <li class="h-32 bg-amber-400/60 text-center">1 · Iris</li>
                     <li class="h-16 bg-orange-700/40 text-center">3 · Teo</li>
                   </ol>
               ''',
               inspector='''
                   ol @class
               ''',
               solucion='''
                   <ol class="grid grid-cols-3 items-end gap-2">
                     <li class="h-24 bg-slate-400/40 text-center">2 · Nadia</li>
                     <li class="h-32 bg-amber-400/60 text-center">1 · Iris</li>
                     <li class="h-16 bg-orange-700/40 text-center">3 · Teo</li>
                   </ol>
               ''',
               al_superar="El podio se para sobre el piso. Teo está tercero y dice que el podio está mal.",
               imagen=["Un podio de vidrio de tres escalones, dorado en el medio.",
                       TEO + " en el tercer escalón, protestando.", IRIS + " se ríe."]),
            tw(id="R04-N04-P2", titulo="Dos formas para los mismos datos",
               lugar=CATEDRAL, personajes="Iris, Tesela",
               carta="Lista o tabla | md:hidden en la lista · hidden md:table en la tabla · los mismos datos, dos formas",
               recompensa="xp 10, oro 10",
               escena="""
                   La tabla de diez filas no entra en la cabaña. —Los mismos datos pueden tener **dos formas** —dice {mentor}.
               """,
               sugiere="En la cabaña, la lista (`md:hidden`); en el castillo, la tabla (`hidden md:table`). Una se ve, la otra no.",
               desafio="Dale `md:hidden` al `ol`, y `hidden md:table` a la `table`.",
               inicial='''
                   <ol>
                     <li>Nadia · 120 puntos</li>
                     <li>Iris · 95 puntos</li>
                   </ol>
                   <table>
                     <thead><tr><th scope="col">Aprendiz</th><th scope="col">Puntos</th></tr></thead>
                     <tbody><tr><td>Nadia</td><td>120</td></tr><tr><td>Iris</td><td>95</td></tr></tbody>
                   </table>
               ''',
               inspector='''
                   ol @class
                   table @class
               ''',
               solucion='''
                   <ol class="md:hidden">
                     <li>Nadia · 120 puntos</li>
                     <li>Iris · 95 puntos</li>
                   </ol>
                   <table class="hidden md:table">
                     <thead><tr><th scope="col">Aprendiz</th><th scope="col">Puntos</th></tr></thead>
                     <tbody><tr><td>Nadia</td><td>120</td></tr><tr><td>Iris</td><td>95</td></tr></tbody>
                   </table>
               ''',
               al_superar="En la cabaña, una lista prolija; en el castillo, la tabla. {mentor}, más bajito: —Cuando termines, quiero pedirte algo para mí.",
               imagen=["Una ventanita con una lista y un ventanal con una tabla, con los mismos nombres.",
                       TESELA + " habla en voz baja.", IRIS + " escucha."]),
            tw(id="R04-N04-P3", titulo="El título que no se ve pero se oye",
               lugar=CATEDRAL, personajes="Iris, Nora",
               carta="caption sr-only | el título de la tabla para el lector de pantalla, sin ocupar lugar en la página",
               recompensa="xp 10, oro 10",
               escena="""
                   El diseño del ventanal no lleva título encima de la tabla: ya hay uno grande arriba. Pero Nora necesita saber de qué es la tabla.
               """,
               sugiere="Un `caption` con la clase `sr-only`: no se ve, pero el lector de pantalla lo lee.",
               desafio="Agregá como primer elemento de la tabla un `caption` con la clase `sr-only` que diga **Liga Obsidiana: los diez mejores**.",
               inicial='''
                   <table>
                     <thead><tr><th scope="col">Aprendiz</th><th scope="col">Puntos</th></tr></thead>
                     <tbody><tr><td>Nadia</td><td>120</td></tr></tbody>
                   </table>
               ''',
               inspector='''
                   caption
                   caption @class
               ''',
               solucion='''
                   <table>
                     <caption class="sr-only">Liga Obsidiana: los diez mejores</caption>
                     <thead><tr><th scope="col">Aprendiz</th><th scope="col">Puntos</th></tr></thead>
                     <tbody><tr><td>Nadia</td><td>120</td></tr></tbody>
                   </table>
               ''',
               al_superar="Nora toca la tabla: —Liga Obsidiana, los diez mejores. —Teo no está. Nadie se lo dice.",
               imagen=["Una tabla de vidrio con un título que solo brilla para quien la toca.",
                       NORA + " toca la tabla.", IRIS + " sonríe."]),
            tw(id="R04-N04-P4", titulo="El vitral de las líderes",
               lugar=CATEDRAL, personajes="Iris, Tesela",
               carta="Listas con sentido | una lista de personas es un <ul> · cada una en su <li>, con su retrato y su nombre",
               recompensa="xp 10, oro 10",
               escena="""
                   —Siempre quise un vitral con todas las líderes del mundo juntas —le dice {mentor}. Iris ya empezó: falta una.
               """,
               sugiere="Cada líder es un `li` de la lista. Copiá uno y cambiale el nombre.",
               desafio="Agregá al final de la lista un `li` que diga **Tesela**.",
               inicial='''
                   <ul class="grid grid-cols-2 gap-4 md:grid-cols-4">
                     <li>Ofidia</li>
                     <li>Maese Ferrum</li>
                     <li>Tesla</li>
                     <li>Kaffa</li>
                   </ul>
               ''',
               inspector='''
                   ul li #
                   ul li:last-child
               ''',
               solucion='''
                   <ul class="grid grid-cols-2 gap-4 md:grid-cols-4">
                     <li>Ofidia</li>
                     <li>Maese Ferrum</li>
                     <li>Tesla</li>
                     <li>Kaffa</li>
                     <li>Tesela</li>
                   </ul>
               ''',
               al_superar="{mentor} se ve en el vitral, al lado de Tesla y de su viejo maestro Ferrum. Se saca el monóculo y no lo limpia: se lo queda mirando un rato largo.",
               imagen=["Un vitral con cinco retratos de líderes, uno al lado del otro.",
                       TESELA + " se mira en el vitral, emocionada, con el monóculo en la mano.", IRIS + " al lado."]),
        ],
    },
    {
        "titulo": "R04-N05 · Jefe final: el Dragón de los Talleres",
        "misiones": [
            tw(id="R04-N05-P1", titulo="La imagen sin nombre",
               lugar=CATEDRAL, personajes="Iris, Tesela",
               criatura="dragon",
               carta="Inspección: alt | toda imagen con contenido tiene alt · alt=\"\" solo si es decoración",
               recompensa="xp 15, oro 15",
               escena="""
                   Iris coloca el último vidrio y da un paso atrás. Entonces aparece el **Dragón de los Talleres**, de plomo y vidrio, con una lupa en la garra. —Inspección final —gruñe—. Si encuentro un solo error, el ventanal es mío.
                   —Revisá como revisaría él —dice {mentor}—. **Celular, teclado y validador.**
               """,
               sugiere="Toda imagen que dice algo lleva `alt` con lo que muestra.",
               desafio="Agregale a la imagen de Gheco `alt=\"Gheco señala las monedas de maestría\"`.",
               inicial='''
                   <section class="p-4">
                     <h2 class="text-2xl font-bold">La Bóveda</h2>
                     <img src="/img/cursos/html/gheco-512.webp" width="160" height="160">
                   </section>
               ''',
               inspector='''
                   img @alt
               ''',
               solucion='''
                   <section class="p-4">
                     <h2 class="text-2xl font-bold">La Bóveda</h2>
                     <img src="/img/cursos/html/gheco-512.webp" alt="Gheco señala las monedas de maestría" width="160" height="160">
                   </section>
               ''',
               al_superar="El dragón acerca la lupa a la imagen. Lee el `alt`. Gruñe y sigue buscando.",
               imagen=["Un ventanal enorme terminado en una catedral; un dragón de plomo y vidrio lo inspecciona con una lupa.",
                       DRAGON, IRIS + " lo mira, tranquila."]),
            tw(id="R04-N05-P2", titulo="El botón sin voz",
               lugar=CATEDRAL, personajes="Iris, Nora",
               criatura="dragon",
               carta="Botones con nombre | un botón de solo ícono necesita aria-label · si no, el lector dice «botón» y nada más",
               recompensa="xp 15, oro 15",
               escena="""
                   El dragón encuentra un botón con un ícono de tres rayitas. Nora llega con el teclado: «Botón». Nada más.
               """,
               sugiere="Un botón que solo tiene un ícono necesita un nombre: `aria-label=\"Abrir el menú\"`.",
               desafio="Agregale al botón `aria-label=\"Abrir el menú\"`.",
               inicial='''
                   <button type="button" class="rounded-lg p-2 text-2xl">☰</button>
               ''',
               inspector='''
                   button @aria-label
               ''',
               solucion='''
                   <button type="button" aria-label="Abrir el menú" class="rounded-lg p-2 text-2xl">☰</button>
               ''',
               al_superar="—Botón: abrir el menú —lee Nora. El dragón tacha algo en su libreta, enojado.",
               imagen=["Un botón de vidrio con un ícono de tres rayas que se ilumina.",
                       NORA + " con la mano en el teclado.", DRAGON + " tacha en una libreta."]),
            tw(id="R04-N05-P3", titulo="El menú que se parte",
               lugar=VIDRIERO, personajes="Iris, Tesela",
               criatura="dragon",
               carta="whitespace-nowrap | el texto no se corta en dos renglones · para los enlaces del menú",
               recompensa="xp 15, oro 15",
               item="Marco Vacío",
               escena="""
                   El dragón agranda la ventana justo hasta 1024 píxeles, con una sonrisa: el menú se parte en dos renglones. «Mis cursos» queda «Mis» arriba y «cursos» abajo.
               """,
               sugiere="`whitespace-nowrap` en cada enlace del menú: el texto no se corta en dos renglones.",
               desafio="Agregale `whitespace-nowrap` a los dos enlaces del menú.",
               inicial='''
                   <nav class="flex gap-4">
                     <a href="#" class="">Mis cursos</a>
                     <a href="#" class="">Liga Obsidiana</a>
                   </nav>
               ''',
               inspector='''
                   nav a @class
               ''',
               solucion='''
                   <nav class="flex gap-4">
                     <a href="#" class="whitespace-nowrap">Mis cursos</a>
                     <a href="#" class="whitespace-nowrap">Liga Obsidiana</a>
                   </nav>
               ''',
               al_superar="El menú queda entero. El dragón, furioso, golpea con la cola la puerta del candado del fondo del taller, y la puerta cede. {mentor} se queda quieta. Saca una llave vieja que ya no hace falta y entra: es el taller de su maestro, el Vidriero. En la mesa hay **un marco de plomo redondo y vacío**, con un hueco del tamaño exacto del fragmento de Iris. {mentor} reconoce el plomo. **El Marco Vacío.**",
               imagen=["Un taller viejo y polvoriento con una puerta forzada; sobre la mesa, un marco de plomo redondo y vacío.",
                       TESELA + " entra despacio, con una llave vieja en la mano.", IRIS + " detrás, con su fragmento emplomado."]),
            m(id="R04-N05-P4", titulo="El Vitral de Iris",
               lugar=VIDRIERO, personajes="Iris, Tesela, Teo, Nora",
               criatura="dragon",
               carta="La inspección final | lang, title y description · celular, teclado y validador · todo vitral empieza chico",
               recompensa="xp 25, oro 30",
               item="Vitral de Iris",
               escena="""
                   El dragón vuelve para la última pasada: la cabecera de la página. Busca el idioma y la descripción que leen los buscadores.
               """,
               sugiere="`<html lang=\"es\">` dice el idioma, y `<meta name=\"description\" content=\"…\">` es el resumen que muestran los buscadores.",
               desafio="Ponele `lang=\"es\"` al `html` y agregá en el `head` un `meta` de `description` con **Aprendé a programar avanzando por tu árbol de habilidades.**",
               inicial='''
                   <!DOCTYPE html>
                   <html>
                     <head>
                       <meta charset="utf-8">
                       <meta name="viewport" content="width=device-width, initial-scale=1">
                       <title>GhecoSoft-Code</title>
                     </head>
                     <body>
                       <h1>GhecoSoft-Code</h1>
                     </body>
                   </html>
               ''',
               inspector='''
                   html @lang
                   meta[name="description"] @content
                   title
               ''',
               solucion='''
                   <!DOCTYPE html>
                   <html lang="es">
                     <head>
                       <meta charset="utf-8">
                       <meta name="viewport" content="width=device-width, initial-scale=1">
                       <title>GhecoSoft-Code</title>
                       <meta name="description" content="Aprendé a programar avanzando por tu árbol de habilidades.">
                     </head>
                     <body>
                       <h1>GhecoSoft-Code</h1>
                     </body>
                   </html>
               ''',
               al_superar="El dragón no encuentra nada. Se va volando, ofendido. Iris no pone su fragmento en el marco del Vidriero: arma su propio vitral, chiquito, empezando por la ventanita de la cabaña, con el fragmento en el centro. **El Vitral de Iris.** Teo aplaude. Nora pasa la mano por el plomo y asiente. {mentor} le muestra el canasto: —Boceto 214. Ese fue el primero que colgaste.",
               imagen=["Una ventanita de cabaña con un vitral redondo chico que brilla como un sol, con un fragmento iridiscente en el centro.",
                       IRIS + " lo cuelga.", TESELA + " sostiene un canasto lleno de bocetos.",
                       TEO + " aplaude.", NORA + " toca el plomo y sonríe."]),
        ],
    },
]
