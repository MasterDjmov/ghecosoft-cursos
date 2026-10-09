from genhtml import m
from html_r01 import IRIS, TESELA, TEO, NORA, GHECO

ARMARIO = "El armario de los vidrios"
TALLER = "El taller de Tesela"
CORNISA = "La cornisa del ventanal"
KAFFA = "La mesa de los encargos de Kaffa"
CABANA = "La cabaña y el castillo"
MURO = "El muro de encargos"
TESLA = "Tesla (muchacho delgado de pelo negro azulado en punta, visor cian, traje azul ajustado con líneas de luz cian y engranajes de bronce en los hombros)"
OGRO = "el Ogro de la Cascada (un ogro gordo hecho de capas de vidrios de colores superpuestos que se tapan unos a otros, con un mazo que tiene grabado !important)"
CSS = "El CSS va en el `<style>`; el **Inspector** lee tus reglas tal como las escribiste (no mide cómo quedó dibujado): mirá en la vista previa que se vea como querés."

NODOS = [
    {
        "titulo": "R02-N01 · Primeros vidrios: CSS",
        "misiones": [
            m(id="R02-N01-P1", titulo="El primer vidrio",
              lugar=ARMARIO, personajes="Iris, Tesela",
              carta="Una regla de CSS | selector { propiedad: valor; } · h1 { color: #22d3ee; }",
              recompensa="xp 10, oro 10",
              escena="""
                  El esqueleto de plomo está listo. {mentor} abre el armario de los vidrios: azul noche, cian neón, ámbar. —Ahora sí, el color. Empezá por uno solo.
              """,
              sugiere="Una regla dice **a quién** (el selector), **qué** (la propiedad) y **cómo** (el valor): `h1 { color: #22d3ee; }`. " + CSS,
              desafio="Escribí en el `style` una regla para que el `h1` sea de color `#22d3ee`.",
              inicial='''
                  <style>

                  </style>
                  <h1>Los Talleres de los Vitrales</h1>
              ''',
              inspector='''
                  css h1 { color }
              ''',
              solucion='''
                  <style>
                    h1 { color: #22d3ee; }
                  </style>
                  <h1>Los Talleres de los Vitrales</h1>
              ''',
              al_superar="El título se tiñe de cian, como un vidrio a contraluz. Iris lo mira diez segundos sin respirar.",
              imagen=["Un armario abierto lleno de vidrios de colores ordenados por tono; sobre la mesa, un título de plomo que brilla en cian.",
                      IRIS + " sostiene un vidrio cian.", TESELA + " abre el armario."]),
            m(id="R02-N01-P2", titulo="Un vidrio para el aviso",
              lugar=ARMARIO, personajes="Iris, Teo",
              carta="Clases | class=\"aviso\" en el HTML · .aviso { … } en el CSS · el punto quiere decir «clase»",
              recompensa="xp 10, oro 10",
              escena="""
                  Teo quiere pintar de ámbar **todos** los párrafos. Iris solo quiere el aviso.
              """,
              sugiere="Una **clase** marca algunos elementos: `class=\"aviso\"` en el HTML y `.aviso { … }` en el CSS (con punto). Así no se pinta todo.",
              desafio="Ponele `class=\"aviso\"` al segundo párrafo y escribí la regla `.aviso` con `background-color: #f59e0b`.",
              inicial='''
                  <style>

                  </style>
                  <p>Encargos de toda la semana.</p>
                  <p>Mañana el taller abre tarde.</p>
              ''',
              inspector='''
                  p @class
                  css .aviso { background-color }
              ''',
              solucion='''
                  <style>
                    .aviso { background-color: #f59e0b; }
                  </style>
                  <p>Encargos de toda la semana.</p>
                  <p class="aviso">Mañana el taller abre tarde.</p>
              ''',
              al_superar="Solo el aviso se pone ámbar. Teo pinta igual todos sus párrafos, de once colores distintos.",
              imagen=["Dos placas de vidrio en una pared; una sola brilla en ámbar.",
                      IRIS + " cuelga la ámbar.", TEO + " con las manos manchadas de pintura."]),
            m(id="R02-N01-P3", titulo="Una sola vez, en el body",
              lugar=ARMARIO, personajes="Iris, Tesela, Gheco",
              carta="Herencia | el color y la letra pasan de padres a hijos · body { color: … } alcanza para toda la página",
              recompensa="xp 10, oro 10",
              escena="""
                  Iris pintó de gris claro cada cosa, una por una: el párrafo, la lista, el título chico. {mentor} cuenta las reglas en voz alta. Son tres para lo mismo.
              """,
              sugiere="El `color` y la letra se **heredan**: si se lo ponés al `body`, todo lo de adentro lo toma, salvo lo que tenga su propia regla.",
              desafio="Poné `color: #e2e8f0` una sola vez en `body` y borrá las tres reglas de `h2`, `p` y `li`.",
              inicial='''
                  <style>
                    body { background-color: #0f172a; }
                    h2 { color: #e2e8f0; }
                    p { color: #e2e8f0; }
                    li { color: #e2e8f0; }
                  </style>
                  <h2>Vidrios del día</h2>
                  <p>Lo que hay en el armario:</p>
                  <ul><li>Azul noche</li><li>Cian neón</li></ul>
              ''',
              inspector='''
                  css body { color }
                  css h2 { color }
                  css p { color }
                  css li { color }
              ''',
              solucion='''
                  <style>
                    body { background-color: #0f172a; color: #e2e8f0; }
                  </style>
                  <h2>Vidrios del día</h2>
                  <p>Lo que hay en el armario:</p>
                  <ul><li>Azul noche</li><li>Cian neón</li></ul>
              ''',
              al_superar="Tres reglas menos y todo se ve igual. Gheco sopla el polvo de las reglas borradas.",
              imagen=["Un vitral oscuro con todo el texto gris claro.",
                      IRIS + " borra con un trapo tres líneas de una pizarra.", GHECO + " sopla el polvo."]),
            m(id="R02-N01-P4", titulo="El color que no está en ninguna paleta",
              lugar=ARMARIO, personajes="Iris, Tesela",
              carta="Variables | :root { --nombre: valor; } · se usa con var(--nombre) · cambiás el valor una vez y cambia en todos lados",
              recompensa="xp 10, oro 10",
              escena="""
                  En el fondo del armario, detrás de los frascos, Iris encuentra un vidrio de un color que no está en ninguna paleta del taller. Lo pone al lado de su fragmento: es exactamente el mismo. Quiere guardarlo con un nombre.
              """,
              sugiere="Una **variable** guarda un valor con nombre: `:root { --vidrio-misterio: #7c3aed; }`, y se usa con `var(--vidrio-misterio)`.",
              desafio="Creá en `:root` la variable `--vidrio-misterio` con `#7c3aed`, y usala como `border-color` de `.fragmento`.",
              inicial='''
                  <style>
                    .fragmento { border: 4px solid; border-color: #7c3aed; padding: 1rem; }
                  </style>
                  <p class="fragmento">El fragmento de Iris</p>
              ''',
              inspector='''
                  css :root { --vidrio-misterio }
                  css .fragmento { border-color }
              ''',
              solucion='''
                  <style>
                    :root { --vidrio-misterio: #7c3aed; }
                    .fragmento { border: 4px solid; border-color: var(--vidrio-misterio); padding: 1rem; }
                  </style>
                  <p class="fragmento">El fragmento de Iris</p>
              ''',
              al_superar="Iris le muestra el vidrio a {mentor}. Ella lo mira mucho rato, sin el monóculo. No dice nada. Lo guarda en el mismo bolsillo del sobretodo donde guardó el boceto del Vidriero.",
              imagen=["Dos vidrios violetas idénticos sobre una mesa, uno con plomo y otro suelto.",
                      IRIS + " los compara.", TESELA + " los mira sin el monóculo, pensativa."]),
        ],
    },
    {
        "titulo": "R02-N02 · El modelo de caja",
        "misiones": [
            m(id="R02-N02-P1", titulo="Aire adentro del marco",
              lugar=TALLER, personajes="Iris, Tesla",
              carta="padding | el relleno: el aire entre el contenido y el borde · padding: 1rem",
              recompensa="xp 10, oro 10",
              escena="""
                  Iris mide a ojo y el texto queda pegado al plomo. Justo pasa por el taller **Tesla**, el Artífice de la Ciudadela, y se ríe: —Igual que Tesela cuando éramos aprendices de Ferrum. —{mentor} lo mira por encima del monóculo y Tesla se pone serio de golpe.
              """,
              sugiere="Todo es una **caja**: contenido, relleno (`padding`), borde y margen. El `padding` es el aire **adentro** del borde.",
              desafio="Dale a `.vidrio` un `padding` de `1rem`.",
              inicial='''
                  <style>
                    .vidrio { border: 2px solid #22d3ee; }
                  </style>
                  <p class="vidrio">Vidrio cian, con su plomo.</p>
              ''',
              inspector='''
                  css .vidrio { padding }
              ''',
              solucion='''
                  <style>
                    .vidrio { border: 2px solid #22d3ee; padding: 1rem; }
                  </style>
                  <p class="vidrio">Vidrio cian, con su plomo.</p>
              ''',
              al_superar="El texto respira. Tesla saca su cinta métrica: —Medí las cuatro capas. Siempre las cuatro.",
              imagen=["Un vidrio cian con su marco de plomo y un espacio de aire entre el texto y el marco.",
                      TESLA + " con una cinta métrica de bronce.", IRIS + " mide."]),
            m(id="R02-N02-P2", titulo="El plomo alrededor",
              lugar=TALLER, personajes="Iris, Tesla",
              carta="border | border: grosor estilo color · border: 2px solid #22d3ee",
              recompensa="xp 10, oro 10",
              escena="""
                  —Sin plomo, un vidrio es un vidrio en el piso —le recuerda Tesla, que lo escuchó mil veces de Ferrum.
              """,
              sugiere="`border` lleva tres cosas: el grosor, el estilo (`solid`, `dashed`…) y el color, en ese orden.",
              desafio="Ponele a `.vidrio` un `border` de `3px solid #f59e0b`.",
              inicial='''
                  <style>
                    .vidrio { padding: 1rem; }
                  </style>
                  <p class="vidrio">Vidrio ámbar.</p>
              ''',
              inspector='''
                  css .vidrio { border }
              ''',
              solucion='''
                  <style>
                    .vidrio { padding: 1rem; border: 3px solid #f59e0b; }
                  </style>
                  <p class="vidrio">Vidrio ámbar.</p>
              ''',
              al_superar="Un marco ámbar rodea el vidrio. Tesla asiente, guarda la cinta y se va con su encargo bajo el brazo.",
              imagen=["Un vidrio con un marco grueso de color ámbar.",
                      TESLA + " se va con un paquete bajo el brazo.", IRIS + " lo saluda."]),
            m(id="R02-N02-P3", titulo="El ancho que no cierra",
              lugar=TALLER, personajes="Iris, Gheco",
              carta="box-sizing | border-box: el ancho incluye relleno y borde · * { box-sizing: border-box; }",
              recompensa="xp 10, oro 10",
              escena="""
                  Iris le dio `width: 200px` al vidrio, pero mide 232. Le sumó el relleno y el borde por su cuenta.
              """,
              sugiere="Con `box-sizing: border-box`, el `width` **incluye** el relleno y el borde. Se pone una vez para todo: `* { box-sizing: border-box; }`.",
              desafio="Agregá una regla para `*` con `box-sizing: border-box`.",
              inicial='''
                  <style>
                    .vidrio { width: 200px; padding: 1rem; border: 0; background-color: #22d3ee; }
                  </style>
                  <p class="vidrio">200 px, ni uno más.</p>
              ''',
              inspector='''
                  css * { box-sizing }
              ''',
              solucion='''
                  <style>
                    * { box-sizing: border-box; }
                    .vidrio { width: 200px; padding: 1rem; border: 0; background-color: #22d3ee; }
                  </style>
                  <p class="vidrio">200 px, ni uno más.</p>
              ''',
              al_superar="El vidrio mide 200 justo. Gheco lo mide dos veces, por las dudas, como haría Tizón.",
              imagen=["Un vidrio cian con una regla de medir al lado que marca exactamente 200.",
                      GHECO + " con una cinta métrica.", IRIS + " satisfecha."]),
            m(id="R02-N02-P4", titulo="Esquinas pulidas",
              lugar=TALLER, personajes="Iris, Tesela",
              carta="Bordes y sombras | border-radius redondea las esquinas · box-shadow: x y desenfoque color",
              recompensa="xp 10, oro 10",
              escena="""
                  —Las esquinas en punta se rompen primero —dice {mentor}, y le alcanza una lima de pulir.
              """,
              sugiere="`border-radius` redondea las esquinas (`12px`, o `9999px` para una píldora).",
              desafio="Dale a `.tarjeta` un `border-radius` de `12px`.",
              inicial='''
                  <style>
                    .tarjeta { padding: 1rem; background-color: #1e293b; color: #e2e8f0; }
                  </style>
                  <div class="tarjeta">Encargo: ventana para el Valle</div>
              ''',
              inspector='''
                  css .tarjeta { border-radius }
              ''',
              solucion='''
                  <style>
                    .tarjeta { padding: 1rem; background-color: #1e293b; color: #e2e8f0; border-radius: 12px; }
                  </style>
                  <div class="tarjeta">Encargo: ventana para el Valle</div>
              ''',
              al_superar="Las esquinas quedan suaves. {mentor} pasa el dedo y no se corta.",
              imagen=["Una tarjeta de vidrio azul oscuro con las esquinas redondeadas.",
                      TESELA + " pasa el dedo por una esquina.", IRIS + " con una lima de pulir."]),
        ],
    },
    {
        "titulo": "R02-N03 · Flexbox",
        "misiones": [
            m(id="R02-N03-P1", titulo="La regla que se estira",
              lugar=CORNISA, personajes="Iris, Tesela",
              carta="display: flex | los hijos se ponen en fila · el contenedor reparte el espacio",
              recompensa="xp 10, oro 10",
              escena="""
                  En la cornisa del ventanal van el escudo y los trofeos, uno al lado del otro. Iris los empuja con márgenes «a ojo». Va por el boceto 61.
                  —Dejá de empujar los vidrios con el dedo —dice {mentor}, y le da una regla que se estira.
              """,
              sugiere="Con `display: flex` en el **contenedor**, sus hijos se ponen en fila y se reparten el espacio solos.",
              desafio="Poné `display: flex` en `.cornisa`.",
              inicial='''
                  <style>
                    .cornisa { padding: 1rem; background-color: #0f172a; color: #e2e8f0; }
                  </style>
                  <header class="cornisa">
                    <span>Escudo</span>
                    <span>Trofeos</span>
                  </header>
              ''',
              inspector='''
                  css .cornisa { display }
              ''',
              solucion='''
                  <style>
                    .cornisa { display: flex; padding: 1rem; background-color: #0f172a; color: #e2e8f0; }
                  </style>
                  <header class="cornisa">
                    <span>Escudo</span>
                    <span>Trofeos</span>
                  </header>
              ''',
              al_superar="Los dos vidrios se acomodan en fila, solos. Iris tira el boceto 61 al canasto, sin pena.",
              imagen=["Una cornisa de vitral con dos piezas acomodándose solas en una fila.",
                      IRIS + " sostiene una regla de bronce que se estira.", TESELA + " al lado."]),
            m(id="R02-N03-P2", titulo="Uno a cada punta",
              lugar=CORNISA, personajes="Iris, Gheco",
              carta="justify-content | reparte en el eje principal · space-between: uno a cada punta · center: al medio",
              recompensa="xp 10, oro 10",
              escena="""
                  El escudo va a la izquierda y los trofeos a la derecha, bien a la punta.
              """,
              sugiere="`justify-content` reparte en la dirección de la fila: `space-between` deja el primero en una punta y el último en la otra.",
              desafio="Agregale a `.cornisa` un `justify-content: space-between`.",
              inicial='''
                  <style>
                    .cornisa { display: flex; padding: 1rem; background-color: #0f172a; color: #e2e8f0; }
                  </style>
                  <header class="cornisa">
                    <span>Escudo</span>
                    <span>Trofeos</span>
                  </header>
              ''',
              inspector='''
                  css .cornisa { justify-content }
              ''',
              solucion='''
                  <style>
                    .cornisa { display: flex; justify-content: space-between; padding: 1rem; background-color: #0f172a; color: #e2e8f0; }
                  </style>
                  <header class="cornisa">
                    <span>Escudo</span>
                    <span>Trofeos</span>
                  </header>
              ''',
              al_superar="El escudo y los trofeos se van cada uno a su punta. Gheco se sienta en el medio, que quedó libre.",
              imagen=["Una cornisa con un escudo a la izquierda y trofeos a la derecha.",
                      GHECO + " sentado en el medio.", IRIS + " mira desde abajo."]),
            m(id="R02-N03-P3", titulo="Centrados y con aire",
              lugar=CORNISA, personajes="Iris, Teo",
              carta="align-items y gap | align-items: center los centra en el otro eje · gap: espacio entre los hijos",
              recompensa="xp 10, oro 10",
              escena="""
                  Abajo van cuatro botones. Teo los separó con márgenes de distinto tamaño, y además el escudo, que es más alto, deja los botones torcidos.
              """,
              sugiere="`align-items: center` los centra en el otro eje (el vertical, en una fila), y `gap` deja el mismo espacio entre todos.",
              desafio="En `.botones`, poné `align-items: center` y `gap: 1rem`.",
              inicial='''
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
              ''',
              inspector='''
                  css .botones { align-items }
                  css .botones { gap }
              ''',
              solucion='''
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
              ''',
              al_superar="Los cuatro botones quedan parejos. Teo los mide con la mano y, por primera vez, da igual.",
              imagen=["Cuatro botones de vidrio cian en fila, a la misma distancia.",
                      TEO + " los mide con la palma.", IRIS + " sonríe."]),
            m(id="R02-N03-P4", titulo="Cuatro botones iguales",
              lugar=CORNISA, personajes="Iris, Tesela",
              carta="flex: 1 | cada hijo con flex: 1 ocupa la misma parte del espacio que sobra",
              recompensa="xp 10, oro 10",
              escena="""
                  —Iguales —dice {mentor}—. No «parecidos»: iguales. Que ocupen todo el ancho, repartido.
              """,
              sugiere="`flex: 1` en **cada hijo** hace que se repartan el espacio en partes iguales.",
              desafio="Escribí una regla para `.botones a` con `flex: 1`.",
              inicial='''
                  <style>
                    .botones { display: flex; gap: 1rem; }
                  </style>
                  <nav class="botones">
                    <a href="#">Taller</a>
                    <a href="#">Encargos</a>
                    <a href="#">Liga</a>
                    <a href="#">Contacto</a>
                  </nav>
              ''',
              inspector='''
                  css .botones a { flex }
              ''',
              solucion='''
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
              ''',
              al_superar="Los cuatro botones se estiran hasta ocupar la fila, del mismo ancho. {mentor} no dice nada; sigue con su vitral.",
              imagen=["Una franja de vitral con cuatro paneles exactamente iguales.",
                      TESELA + " trabaja en su propio vitral.", IRIS + " compara los paneles."]),
        ],
    },
    {
        "titulo": "R02-N04 · Grid",
        "misiones": [
            m(id="R02-N04-P1", titulo="Doce vitrales para Kaffa",
              lugar=KAFFA, personajes="Iris, Tesela",
              carta="display: grid | una malla de filas y columnas · grid-template-columns: repeat(3, 1fr)",
              recompensa="xp 10, oro 10",
              escena="""
                  Llega una carta de **Kaffa**, el Arquitecto Imperial: «Doce vitrales iguales, alineados en filas y columnas perfectas». Teo propone hacer uno de otro color. Nadie le contesta.
                  —Con la regla flexible hacés filas —dice {mentor}—, pero no **cuadrículas**. Para Kaffa, la **malla**.
              """,
              sugiere="`display: grid` arma una malla, y `grid-template-columns: repeat(3, 1fr)` hace tres columnas iguales (`1fr` es «una parte»).",
              desafio="En `.vitrales`, poné `display: grid` y `grid-template-columns: repeat(3, 1fr)`.",
              inicial='''
                  <style>
                    .vitrales div { padding: 1rem; background-color: #7c3aed; color: #fff; }
                  </style>
                  <div class="vitrales">
                    <div>1</div><div>2</div><div>3</div>
                    <div>4</div><div>5</div><div>6</div>
                  </div>
              ''',
              inspector='''
                  css .vitrales { display }
                  css .vitrales { grid-template-columns }
              ''',
              solucion='''
                  <style>
                    .vitrales { display: grid; grid-template-columns: repeat(3, 1fr); }
                    .vitrales div { padding: 1rem; background-color: #7c3aed; color: #fff; }
                  </style>
                  <div class="vitrales">
                    <div>1</div><div>2</div><div>3</div>
                    <div>4</div><div>5</div><div>6</div>
                  </div>
              ''',
              al_superar="Los vitrales se ordenan en filas de tres. Kaffa no los vio todavía, pero Iris ya se imagina su cara.",
              imagen=["Una pared con vitrales violetas acomodados en una cuadrícula perfecta de tres columnas.",
                      IRIS + " los mira.", TESELA + " con la carta de Kaffa en la mano."]),
            m(id="R02-N04-P2", titulo="El plomo entre vitral y vitral",
              lugar=KAFFA, personajes="Iris, Gheco",
              carta="gap en grid | gap: el espacio entre filas y columnas · sin márgenes en cada hijo",
              recompensa="xp 10, oro 10",
              escena="""
                  Los vitrales quedaron pegados unos con otros. Kaffa pidió una franja de plomo pareja entre todos.
              """,
              sugiere="En una malla, `gap` deja el mismo espacio entre filas y entre columnas, sin tocar los hijos.",
              desafio="Agregale a `.vitrales` un `gap` de `0.75rem`.",
              inicial='''
                  <style>
                    .vitrales { display: grid; grid-template-columns: repeat(3, 1fr); }
                    .vitrales div { padding: 1rem; background-color: #7c3aed; color: #fff; }
                  </style>
                  <div class="vitrales">
                    <div>1</div><div>2</div><div>3</div>
                    <div>4</div><div>5</div><div>6</div>
                  </div>
              ''',
              inspector='''
                  css .vitrales { gap }
              ''',
              solucion='''
                  <style>
                    .vitrales { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; }
                    .vitrales div { padding: 1rem; background-color: #7c3aed; color: #fff; }
                  </style>
                  <div class="vitrales">
                    <div>1</div><div>2</div><div>3</div>
                    <div>4</div><div>5</div><div>6</div>
                  </div>
              ''',
              al_superar="Una franja de plomo pareja separa cada vitral. Gheco camina por las franjas como por un laberinto.",
              imagen=["Una cuadrícula de vitrales violetas separados por franjas de plomo iguales.",
                      GHECO + " camina por las franjas.", IRIS + " sonríe."]),
            m(id="R02-N04-P3", titulo="Tantas columnas como entren",
              lugar=KAFFA, personajes="Iris, Tesela",
              carta="auto-fit y minmax | repeat(auto-fit, minmax(10rem, 1fr)) · entran las columnas que quepan, sin @media",
              recompensa="xp 10, oro 10",
              escena="""
                  —En la catedral de Kaffa hay ventanas anchas y angostas —dice {mentor}—. No le vamos a hacer una malla para cada una.
              """,
              sugiere="`repeat(auto-fit, minmax(10rem, 1fr))`: cada columna mide al menos `10rem`, y entran todas las que quepan.",
              desafio="Cambiá el `grid-template-columns` de `.vitrales` por `repeat(auto-fit, minmax(10rem, 1fr))`.",
              inicial='''
                  <style>
                    .vitrales { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; }
                    .vitrales div { padding: 1rem; background-color: #7c3aed; color: #fff; }
                  </style>
                  <div class="vitrales">
                    <div>1</div><div>2</div><div>3</div>
                    <div>4</div><div>5</div><div>6</div>
                  </div>
              ''',
              inspector='''
                  css .vitrales { grid-template-columns }
              ''',
              solucion='''
                  <style>
                    .vitrales { display: grid; grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr)); gap: 0.75rem; }
                    .vitrales div { padding: 1rem; background-color: #7c3aed; color: #fff; }
                  </style>
                  <div class="vitrales">
                    <div>1</div><div>2</div><div>3</div>
                    <div>4</div><div>5</div><div>6</div>
                  </div>
              ''',
              al_superar="En *Celular* se ven de a dos; en *Compu*, de a seis. La misma malla. {mentor} asiente una sola vez.",
              imagen=["Dos ventanas, una angosta y una ancha, con la misma cuadrícula de vitrales acomodada distinto.",
                      IRIS + " compara las dos.", TESELA + " asiente."]),
            m(id="R02-N04-P4", titulo="El podio de los campeones",
              lugar=KAFFA, personajes="Iris, Teo",
              carta="align-items: end | en la malla, alinea los hijos abajo · el podio: el del medio más alto",
              recompensa="xp 10, oro 10",
              escena="""
                  Abajo del encargo va el podio: tres escalones, el del medio más alto. Pero en la malla los tres quedan colgando de arriba.
              """,
              sugiere="`align-items: end` en la malla apoya a todos los hijos **abajo**, como escalones sobre el piso.",
              desafio="Agregale `align-items: end` a `.podio`.",
              inicial='''
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
              ''',
              inspector='''
                  css .podio { align-items }
              ''',
              solucion='''
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
              ''',
              al_superar="Los tres escalones se apoyan en el piso. Teo se sube al del medio para la foto.",
              imagen=["Un podio dorado de tres escalones, el del medio más alto.",
                      TEO + " subido al escalón del medio, haciendo pose.", IRIS + " se ríe."]),
        ],
    },
    {
        "titulo": "R02-N05 · Responsive: celular primero",
        "misiones": [
            m(id="R02-N05-P1", titulo="La ventanita de la cabaña",
              lugar=CABANA, personajes="Iris, Tesela",
              carta="viewport | <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> · sin esto el celular achica la página de escritorio",
              recompensa="xp 10, oro 10",
              escena="""
                  El **Ogro de la Cascada** desafía al taller: el mismo vitral tiene que verse bien en la ventanita de una cabaña **y** en el ventanal del castillo. Iris prueba primero en el castillo, como siempre. {mentor} no dice nada: le alcanza un **espejito de bolsillo**. En el espejito, todo se ve diminuto.
              """,
              sugiere="Sin la etiqueta `<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">`, el celular muestra la versión de compu achicada.",
              desafio="Agregá en el `head` la etiqueta `meta` del viewport con `width=device-width, initial-scale=1`.",
              inicial='''
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
              ''',
              inspector='''
                  meta[name="viewport"] @content
              ''',
              solucion='''
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
              ''',
              al_superar="En el espejito, el vitral se ve de su tamaño. {mentor} le deja el espejito en la mesa.",
              imagen=["Una cabaña chiquita y un castillo enorme, uno al lado del otro, con el mismo vitral.",
                      IRIS + " mira un espejito de bolsillo.", TESELA + " se lo alcanza."]),
            m(id="R02-N05-P2", titulo="Agrandar es fácil",
              lugar=CABANA, personajes="Iris, Tesela",
              carta="@media | celular primero: el CSS de base es el chico · @media (min-width: 768px) { … } agrega lo de la pantalla grande",
              recompensa="xp 10, oro 10",
              escena="""
                  —Empezá por la ventana **chica** —le dice {mentor}—. Agrandar es fácil; achicar algo grande, casi imposible.
              """,
              sugiere="El CSS de base es para el celular. Lo de pantallas grandes se **agrega** adentro de `@media (min-width: 768px) { … }`.",
              desafio="Agregá un `@media (min-width: 768px)` que ponga `.grilla` con `grid-template-columns: repeat(2, 1fr)`.",
              inicial='''
                  <style>
                    .grilla { display: grid; gap: 1rem; }
                    .grilla div { padding: 1rem; background-color: #22d3ee; }
                  </style>
                  <div class="grilla">
                    <div>Cabaña</div>
                    <div>Castillo</div>
                  </div>
              ''',
              inspector='''
                  css .grilla { grid-template-columns }
                  css @media (min-width: 768px) | .grilla { grid-template-columns }
              ''',
              solucion='''
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
              ''',
              al_superar="En *Celular*, uno debajo del otro; en *Compu*, de a dos. Iris lo prueba primero en el espejito. Sin que nadie se lo diga.",
              imagen=["Un vitral que en la cabaña tiene sus piezas apiladas y en el castillo, lado a lado.",
                      IRIS + " con el espejito en la mano.", TESELA + " sonríe apenas."]),
            m(id="R02-N05-P3", titulo="La imagen que no entra",
              lugar=CABANA, personajes="Iris, Gheco",
              criatura="orco",
              carta="Imágenes flexibles | img { max-width: 100%; height: auto; } · nunca más ancha que su caja",
              recompensa="xp 10, oro 10",
              escena="""
                  En la ventanita de la cabaña, la imagen del vitral es más ancha que la pared y aparece una barra para arrastrar de costado. Por la rendija asoma un **orco**.
              """,
              sugiere="`max-width: 100%` hace que la imagen nunca sea más ancha que su caja, y `height: auto` mantiene la proporción.",
              desafio="Escribí una regla para `img` con `max-width: 100%` y `height: auto`.",
              inicial='''
                  <style>

                  </style>
                  <img src="/img/cursos/html/heroe-896.webp" alt="El aprendiz con su buzo de circuitos" width="896" height="896">
              ''',
              inspector='''
                  css img { max-width }
                  css img { height }
              ''',
              solucion='''
                  <style>
                    img { max-width: 100%; height: auto; }
                  </style>
                  <img src="/img/cursos/html/heroe-896.webp" alt="El aprendiz con su buzo de circuitos" width="896" height="896">
              ''',
              al_superar="La imagen se achica hasta entrar en la pared. El orco se queda sin rendija y se va gruñendo.",
              imagen=["Una ventanita de cabaña con una imagen que se achica para entrar; un orco se aleja gruñendo.",
                      IRIS + " con el espejito.", GHECO + " lo señala."]),
            m(id="R02-N05-P4", titulo="La cornisa que acompaña",
              lugar=CABANA, personajes="Iris, Nora",
              carta="position: sticky | se queda pegado al borde al bajar · top: 0 dice dónde se pega",
              recompensa="xp 10, oro 10",
              escena="""
                  El vitral de la cabaña es largo, y al bajar se pierde el menú. Nora, que lo recorre de arriba abajo, no sabe cómo volver.
              """,
              sugiere="`position: sticky` con `top: 0` deja el elemento en su lugar hasta que llega arriba, y ahí se queda pegado mientras bajás.",
              desafio="Poné `position: sticky` y `top: 0` en `header`.",
              inicial='''
                  <style>
                    header { background-color: #0f172a; color: #e2e8f0; padding: 1rem; }
                    main { height: 2000px; }
                  </style>
                  <header>Taller · Encargos · Liga</header>
                  <main><p>Un vitral muy largo…</p></main>
              ''',
              inspector='''
                  css header { position }
                  css header { top }
              ''',
              solucion='''
                  <style>
                    header { position: sticky; top: 0; background-color: #0f172a; color: #e2e8f0; padding: 1rem; }
                    main { height: 2000px; }
                  </style>
                  <header>Taller · Encargos · Liga</header>
                  <main><p>Un vitral muy largo…</p></main>
              ''',
              al_superar="Nora baja hasta el final y el menú la acompaña. —Así no me pierdo nunca.",
              imagen=["Un vitral largo con una franja de arriba que se queda fija mientras el resto baja.",
                      NORA + " recorre el vitral con la mano.", IRIS + " al lado."]),
        ],
    },
    {
        "titulo": "R02-N06 · Jefe: el Ogro de la Cascada",
        "misiones": [
            m(id="R02-N06-P1", titulo="El aviso de Ofidia",
              lugar=MURO, personajes="Iris, Tesela",
              criatura="ogro",
              carta="Especificidad | id > clase > etiqueta · #muro .aviso le gana a #muro p",
              recompensa="xp 15, oro 15",
              escena="""
                  El Ogro de la Cascada se metió de noche en el **muro de encargos**. El aviso de Ofidia no se ve ámbar: otra regla le gana.
                  —Ninguna regla está borrada —dice {mentor}—. Otras les ganan. Sin `!important` y sin tocar el HTML: entendé **quién le gana a quién**.
              """,
              sugiere="Gana el selector más **específico**: cuenta primero los `#id`, después las `.clases`, después las etiquetas. `#muro p` tiene un id y una etiqueta; `#muro .aviso`, un id y una clase: gana.",
              desafio="Cambiá el selector de la regla ámbar de `.aviso` a `#muro .aviso`.",
              inicial='''
                  <style>
                    #muro p { color: #94a3b8; }
                    .aviso { color: #f59e0b; }
                  </style>
                  <section id="muro">
                    <p>Encargo de Kaffa: doce vitrales.</p>
                    <p class="aviso">Aviso de Ofidia: el río crece.</p>
                  </section>
              ''',
              inspector='''
                  css .aviso { color }
                  css #muro .aviso { color }
              ''',
              solucion='''
                  <style>
                    #muro p { color: #94a3b8; }
                    #muro .aviso { color: #f59e0b; }
                  </style>
                  <section id="muro">
                    <p>Encargo de Kaffa: doce vitrales.</p>
                    <p class="aviso">Aviso de Ofidia: el río crece.</p>
                  </section>
              ''',
              al_superar="El aviso de Ofidia se enciende en ámbar. Al ogro se le descascara la primera capa.",
              imagen=["Un muro de carteles pegados unos encima de otros; uno se enciende en ámbar.",
                      OGRO + " pierde una capa de vidrio.", IRIS + " frente al muro."]),
            m(id="R02-N06-P2", titulo="El encargo destacado",
              lugar=MURO, personajes="Iris, Gheco",
              criatura="ogro",
              carta="Dos clases | .encargo.destacado (pegadas) = un elemento con las dos clases · le gana a .encargo",
              recompensa="xp 15, oro 15",
              escena="""
                  El encargo destacado de Kaffa parece uno más: el borde dorado no aparece.
              """,
              sugiere="`.encargo.destacado` (con las dos clases **pegadas**) apunta al elemento que tiene las dos, y es más específico que `.encargo` solo.",
              desafio="Cambiá el selector `.destacado` por `.encargo.destacado`.",
              inicial='''
                  <style>
                    .destacado { border-color: #fbbf24; }
                    .encargo { border: 3px solid #334155; padding: 1rem; }
                  </style>
                  <article class="encargo">Ventana para el Valle</article>
                  <article class="encargo destacado">Doce vitrales para Kaffa</article>
              ''',
              inspector='''
                  css .destacado { border-color }
                  css .encargo.destacado { border-color }
              ''',
              solucion='''
                  <style>
                    .encargo.destacado { border-color: #fbbf24; }
                    .encargo { border: 3px solid #334155; padding: 1rem; }
                  </style>
                  <article class="encargo">Ventana para el Valle</article>
                  <article class="encargo destacado">Doce vitrales para Kaffa</article>
              ''',
              al_superar="El borde dorado vuelve. Otra capa del ogro se cae al piso y se hace añicos.",
              imagen=["Un cartel con borde dorado que vuelve a brillar en un muro de encargos.",
                      OGRO + " más flaco.", GHECO + " barre los vidrios."]),
            m(id="R02-N06-P3", titulo="El mazo que no sirve",
              lugar=MURO, personajes="Iris, Tesela",
              criatura="ogro",
              carta="Sin !important | !important gana a todo y después nada le gana a él · se resuelve con un selector más específico",
              recompensa="xp 15, oro 15",
              escena="""
                  El título del muro perdió su color: el ogro le pegó con su mazo, que tiene grabado `!important`. Teo propone pegarle con otro `!important` más grande.
              """,
              sugiere="`!important` le gana a todo… y después nada le gana a él. Sacalo, y para que gane el cian usá un selector más específico.",
              desafio="Sacá el `!important` de `.titulo`, y escribí `.muro .titulo` con `color: #22d3ee`.",
              inicial='''
                  <style>
                    .titulo { color: #64748b !important; }
                  </style>
                  <section class="muro">
                    <h2 class="titulo">Muro de encargos</h2>
                  </section>
              ''',
              inspector='''
                  css .titulo { color }
                  css .muro .titulo { color }
              ''',
              solucion='''
                  <style>
                    .titulo { color: #64748b; }
                    .muro .titulo { color: #22d3ee; }
                  </style>
                  <section class="muro">
                    <h2 class="titulo">Muro de encargos</h2>
                  </section>
              ''',
              al_superar="El título se pone cian. El ogro mira su mazo y se lo esconde atrás de la espalda.",
              imagen=["Un título de vitral que recupera su color cian.",
                      OGRO + " esconde el mazo atrás de la espalda.", TESELA + " se cruza de brazos."]),
            m(id="R02-N06-P4", titulo="El último gana",
              lugar=MURO, personajes="Iris, Tesela, Teo",
              criatura="ogro",
              carta="El orden | con la misma especificidad, gana la regla que viene después",
              recompensa="xp 20, oro 25",
              item="Monóculo de Cristal",
              escena="""
                  Los botones del muro tienen el fondo oscuro y el texto no se ve. Hay dos reglas para `.boton`, iguales de específicas.
              """,
              sugiere="Si dos reglas son igual de específicas, gana **la que viene después**. Mirá el orden.",
              desafio="Borrá la segunda regla de `.boton` (la del fondo `#1e293b`), así gana la cian.",
              inicial='''
                  <style>
                    .boton { background: #22d3ee; color: #0f172a; padding: 0.5rem 1rem; }
                    .boton { background: #1e293b; }
                  </style>
                  <a class="boton" href="#">Ver encargos</a>
              ''',
              inspector='''
                  css .boton { background }
              ''',
              solucion='''
                  <style>
                    .boton { background: #22d3ee; color: #0f172a; padding: 0.5rem 1rem; }
                  </style>
                  <a class="boton" href="#">Ver encargos</a>
              ''',
              al_superar="El ogro se descascara capa por capa hasta desaparecer. {mentor} se saca el monóculo y lo limpia con la manga, despacio. Iris no entiende por qué. Al día siguiente, en su mesa, hay un monóculo de cristal tallado igual al de {mentor}: **el Monóculo de Cristal**.",
              imagen=["Un muro de encargos ordenado y luminoso; en el piso, una pila de capas de vidrio rotas.",
                      TESELA + " limpia su monóculo con la manga.", IRIS + " la mira sin entender.", TEO + " aplaude."]),
        ],
    },
]
