from genhtml import m

BALCON = "El balcón de los Talleres"
TALLER = "El taller de Tesela"
RIOS = "Los ríos de plomo"
VENTANILLA = "La ventanilla del portal"
LIGA = "La entrada de los Talleres"
PANADERIA = "La panadería del Gremio"
VER = "Tu página se dibuja sola al lado mientras escribís; el **Inspector**, debajo, lee tu código (sin ejecutarlo) y te muestra qué encontró."
IRIS = "Iris (16, delgada, trenza larga castaño claro con mechones rojo, ámbar y azul, anteojos redondos, delantal de cuero marrón con lápices y vidrios en los bolsillos, botas con luz cian)"
TESELA = "Tesela (22, pelo corto iridiscente violeta y cian, monóculo de cristal tallado, sobretodo largo negro con fragmentos de vidrio de colores cosidos)"
TEO = "Teo (15, flaco, pelo negro enrulado con purpurina, pecas, delantal manchado de todos los colores, cinturón con frascos de vidrio molido)"
NORA = "Nora (30, ciega, alta, piel oscura, trenzas finas con un broche de vidrio, túnica gris perla, guantes sin dedos, bastón de vidrio)"
GHECO = "Gheco (gecko de luz con antiparras)"
SLIME = "el Slime de las Etiquetas Huérfanas (un slime gordo de vidrio derretido verde y rosa, con etiquetas sin cerrar flotando adentro como burbujas)"

NODOS = [
    {
        "titulo": "R00-N01 · Clase 0 · Hola, HTML",
        "misiones": [
            m(id="R00-N01-P1", titulo="El esqueleto del vitral",
              lugar=BALCON, personajes="Iris, Gheco, Tesela",
              carta="El esqueleto | <!DOCTYPE html> · <html lang=\"es\"> · <head> (no se ve) · <body> (todo lo que se ve)",
              recompensa="xp 10, oro 10",
              escena="""
                  Iris despierta en un balcón de piedra, con el fragmento de vidrio todavía en la mano. Sobre su hombro aparece un gecko de luz con antiparras: **Gheco**.
                  —Acá los vitrales se escriben —le dice—. Y todos empiezan igual: con su esqueleto.
              """,
              sugiere="Toda página empieza con `<!DOCTYPE html>` y tiene una raíz `<html lang=\"es\">` con dos partes: `<head>` (lo que no se ve) y `<body>` (lo que se ve). " + VER,
              desafio="Escribí la primera línea que falta, `<!DOCTYPE html>`, y poné `lang=\"es\"` en la etiqueta `html`.",
              inicial='''
                  <html>
                    <head>
                      <meta charset="utf-8">
                      <title>Mi primer vitral</title>
                    </head>
                    <body>
                      <p>Hola, Talleres.</p>
                    </body>
                  </html>
              ''',
              inspector='''
                  !doctype
                  html @lang
                  title
              ''',
              solucion='''
                  <!DOCTYPE html>
                  <html lang="es">
                    <head>
                      <meta charset="utf-8">
                      <title>Mi primer vitral</title>
                    </head>
                    <body>
                      <p>Hola, Talleres.</p>
                    </body>
                  </html>
              ''',
              al_superar="Una varilla de plomo se dobla sola y dibuja un marco en el aire. Gheco aplaude con la cola.",
              imagen=["Un balcón de piedra sobre una ciudad de ventanales de colores, al atardecer; abajo, ríos de plomo fundido plateado.",
                      IRIS + " mira un marco de plomo vacío dibujado en el aire.", GHECO + " sobre su hombro."]),
            m(id="R00-N01-P2", titulo="El título del vitral",
              lugar=BALCON, personajes="Iris, Tesela",
              carta="Títulos y párrafos | <h1> el título principal (uno por página) · <p> un párrafo",
              recompensa="xp 10, oro 10",
              escena="""
                  —Un vitral sin título es un vidrio más —dice {mentor}, y le alcanza una varilla de plomo—. Decí qué es, arriba de todo.
              """,
              sugiere="`<h1>…</h1>` es el título más importante de la página (uno solo). `<p>…</p>` es un párrafo. Lo que se abre, se cierra.",
              desafio="Agregá, arriba del párrafo, un `h1` que diga exactamente **¡Hola, Talleres!**",
              inicial='''
                  <!DOCTYPE html>
                  <html lang="es">
                    <head>
                      <meta charset="utf-8">
                      <title>Mi primer vitral</title>
                    </head>
                    <body>
                      <p>Soy Iris y este es mi primer vitral.</p>
                    </body>
                  </html>
              ''',
              inspector='''
                  h1
                  p
              ''',
              solucion='''
                  <!DOCTYPE html>
                  <html lang="es">
                    <head>
                      <meta charset="utf-8">
                      <title>Mi primer vitral</title>
                    </head>
                    <body>
                      <h1>¡Hola, Talleres!</h1>
                      <p>Soy Iris y este es mi primer vitral.</p>
                    </body>
                  </html>
              ''',
              al_superar="Las letras del título se encienden en el plomo. {mentor} lo mira de reojo y sigue con lo suyo.",
              imagen=["Un taller de vitralista con grandes ventanales; sobre la mesa, un vitral de plomo con un título que brilla.",
                      IRIS + " escribe con un lápiz de luz.", TESELA + " la mira de reojo."]),
            m(id="R00-N01-P3", titulo="Lo importante y lo dicho con énfasis",
              lugar=TALLER, personajes="Iris, Teo, Gheco",
              carta="strong y em | <strong> texto importante (negrita) · <em> énfasis (cursiva)",
              recompensa="xp 10, oro 10",
              escena="""
                  Teo entra corriendo con un vitral de doce colores. —¡Miren lo que…! —Se le desarma en las manos.
                  Iris quiere que en su párrafo **HTML** se note más que el resto, y que *qué es* suene distinto.
              """,
              sugiere="`<strong>` marca lo **importante** y `<em>` lo dicho con *énfasis*. Van adentro del párrafo: `<p>Hola <strong>mundo</strong></p>`.",
              desafio="En el párrafo, envolvé **HTML** con `strong` y **qué es** con `em`.",
              inicial='''
                  <h1>¡Hola, Talleres!</h1>
                  <p>Aprendo HTML: el plomo dice qué es cada parte.</p>
              ''',
              inspector='''
                  p strong
                  p em
              ''',
              solucion='''
                  <h1>¡Hola, Talleres!</h1>
                  <p>Aprendo <strong>HTML</strong>: el plomo dice <em>qué es</em> cada parte.</p>
              ''',
              al_superar="Teo junta los vidrios de su vitral desarmado y mira el párrafo de Iris. —¿Y el negrita no es un color? —No —dice Gheco—. Es una forma de decir «esto importa».",
              imagen=["Un taller de vitrales con vidrios rotos de muchos colores en el piso.",
                      TEO + " junta los vidrios con cara de susto.", IRIS + " escribe en un cuaderno."]),
            m(id="R00-N01-P4", titulo="Lo que se abre adentro, se cierra adentro",
              lugar=TALLER, personajes="Iris, Tesela, Gheco",
              criatura="slime",
              carta="Anidar bien | lo que se abre adentro se cierra adentro · <p><em>bien</em></p> · una etiqueta sin cerrar se come lo que sigue",
              recompensa="xp 10, oro 10",
              item="Fragmento Astillado",
              escena="""
                  Iris apoya el fragmento en una ventana vacía, sin plomo, para ver cómo queda. El vidrio resbala, cae y **se astilla en una punta**.
                  —Un vidrio sin plomo es un vidrio en el piso —dice {mentor}. Y señala el vitral de Iris: un **slime** se está comiendo un cierre mal puesto.
              """,
              sugiere="Las etiquetas se cierran en orden inverso: la última que abriste es la primera que cerrás. Si una queda abierta, el navegador «adivina» dónde termina… y casi siempre adivina mal: acá, el *énfasis* se contagia al párrafo de abajo.",
              desafio="El `em` de **plomo** quedó abierto y se contagia al párrafo de abajo: cerralo con `</em>` antes del `</p>`.",
              inicial='''
                  <h1>¡Hola, Talleres!</h1>
                  <p>Primero el <em>plomo</p>
                  <p>Después el color.</p>
              ''',
              inspector='''
                  em #
                  p em
              ''',
              solucion='''
                  <h1>¡Hola, Talleres!</h1>
                  <p>Primero el <em>plomo</em></p>
                  <p>Después el color.</p>
              ''',
              al_superar="El slime se queda sin comida y se escurre por una rendija. {mentor} junta el fragmento astillado y se lo devuelve: —Guardalo. Ya le vamos a encontrar su plomo. Al fondo del taller, Iris ve una puerta vieja con un candado enorme.",
              imagen=["Un taller de vitrales; en el piso, un fragmento de vidrio iridiscente con una punta astillada.",
                      TESELA + " lo levanta con cuidado.", IRIS + " mira apenada.",
                      "Al fondo, una puerta vieja con un candado enorme."]),
        ],
    },
    {
        "titulo": "R01-N01 · Texto, enlaces e imágenes",
        "misiones": [
            m(id="R01-N01-P1", titulo="Los pasos del trabajo",
              lugar=TALLER, personajes="Iris, Tesela",
              carta="Listas | <ul> con viñetas · <ol> numerada · cada elemento en un <li>",
              recompensa="xp 10, oro 10",
              escena="""
                  —Llevá un diario del taller —le pide {mentor}, y le da un cuaderno en blanco—. Lo primero: los pasos de cada trabajo, en orden.
              """,
              sugiere="`<ol>` es una lista **numerada** (el orden importa); `<ul>`, con viñetas. Cada elemento va en su `<li>`.",
              desafio="Convertí los tres pasos en una lista **numerada**: un `ol` con un `li` por paso.",
              inicial='''
                  <h2>Pasos de un vitral</h2>
                  <p>Dibujar el boceto</p>
                  <p>Soldar el plomo</p>
                  <p>Elegir los vidrios</p>
              ''',
              inspector='''
                  ol li #
                  ol li
              ''',
              solucion='''
                  <h2>Pasos de un vitral</h2>
                  <ol>
                    <li>Dibujar el boceto</li>
                    <li>Soldar el plomo</li>
                    <li>Elegir los vidrios</li>
                  </ol>
              ''',
              al_superar="{mentor} asiente. Iris arranca la hoja, la vuelve a escribir con mejor letra y tira la primera al canasto. {mentor} le escribe un número con tiza: «Boceto 1».",
              imagen=["Una mesa de taller con un cuaderno abierto y una lista numerada de tres pasos.",
                      IRIS + " escribe.", TESELA + " pone un papel en un canasto y le escribe un 1 con tiza."]),
            m(id="R01-N01-P2", titulo="Una ventana a otro taller",
              lugar=TALLER, personajes="Iris, Tesela, Gheco",
              carta="Enlaces | <a href=\"destino\">texto</a> · el texto dice adónde lleva (nunca «clic acá»)",
              recompensa="xp 10, oro 10",
              escena="""
                  {mentor} señala los ventanales del fondo: uno da al Valle de la Serpiente, otro al Puerto de los Mensajeros. —Un vitral también **conecta**. Cada ventana da a otra.
              """,
              sugiere="`<a href=\"…\">texto</a>` es un enlace: `href` dice adónde va y el texto dice qué hay ahí. «Clic acá» no le dice nada a nadie.",
              desafio="Convertí *Valle de la Serpiente* en un enlace a `valle.html`.",
              inicial='''
                  <h2>Caminos</h2>
                  <p>Desde el taller se ve el Valle de la Serpiente.</p>
              ''',
              inspector='''
                  a
                  a @href
              ''',
              solucion='''
                  <h2>Caminos</h2>
                  <p>Desde el taller se ve el <a href="valle.html">Valle de la Serpiente</a>.</p>
              ''',
              al_superar="El ventanal del Valle se ilumina de verde. Por un segundo, Iris escucha el río.",
              imagen=["Un ventanal enorme de taller que da a un valle verde con un río, brillando.",
                      IRIS + " lo señala.", GHECO + " cuelga del marco."]),
            m(id="R01-N01-P3", titulo="Lo que Nora no ve",
              lugar=TALLER, personajes="Iris, Nora",
              carta="Imágenes | <img src=\"ruta\" alt=\"qué muestra\"> · el alt es lo que lee quien no la ve · alt=\"\" si es solo decoración",
              recompensa="xp 10, oro 10",
              escena="""
                  Nora, la vitralista más vieja del taller, pasa la mano por el diario. Nora no ve: lee los vitrales tocando el plomo.
                  —¿Y qué hay en el dibujo de la mascota? —pregunta. El dibujo no dice nada. Para Nora, no existe.
              """,
              sugiere="`alt` describe lo que muestra la imagen, para quien no la ve (o si no carga). Sin `alt`, el lector de pantalla lee el nombre del archivo.",
              desafio="Agregale a la imagen un `alt` que diga exactamente **Gheco, el gecko celeste con anteojos**.",
              inicial='''
                  <h2>La mascota del taller</h2>
                  <img src="/img/personajes/gheco.webp" width="160" height="160">
              ''',
              inspector='''
                  img @alt
              ''',
              solucion='''
                  <h2>La mascota del taller</h2>
                  <img src="/img/personajes/gheco.webp" alt="Gheco, el gecko celeste con anteojos" width="160" height="160">
              ''',
              al_superar="Nora pasa los dedos por el dibujo y sonríe. —Un gecko con anteojos. Ahora sí lo veo.",
              imagen=["Un taller de vitrales con luz de tarde.",
                      NORA + " pasa los dedos por un cuaderno abierto con un dibujo de un gecko.", IRIS + " la mira."]),
            m(id="R01-N01-P4", titulo="El boceto del canasto",
              lugar=TALLER, personajes="Iris, Tesela",
              carta="figure y figcaption | <figure> agrupa una imagen con su epígrafe · <figcaption> es el epígrafe",
              recompensa="xp 10, oro 10",
              escena="""
                  Entre los bocetos viejos del canasto, Iris encuentra uno que no es suyo: **un vitral redondo**, firmado por alguien que se hacía llamar *el Vidriero*. Quiere pegarlo en el diario con su epígrafe.
              """,
              sugiere="`<figure>` agrupa una imagen con su epígrafe, y el epígrafe va en `<figcaption>`, adentro de la misma `figure`.",
              desafio="Envolvé la imagen y el epígrafe en un `figure`, y poné el epígrafe en un `figcaption` (en vez del `p`).",
              inicial='''
                  <img src="/img/cursos/html/vitral.webp" alt="Boceto de un vitral redondo" width="240" height="240">
                  <p>Boceto firmado por el Vidriero</p>
              ''',
              inspector='''
                  figure img @alt
                  figure figcaption
              ''',
              solucion='''
                  <figure>
                    <img src="/img/cursos/html/vitral.webp" alt="Boceto de un vitral redondo" width="240" height="240">
                    <figcaption>Boceto firmado por el Vidriero</figcaption>
                  </figure>
              ''',
              al_superar="Iris le muestra el boceto a {mentor}. Ella lo mira un segundo de más, lo dobla y se lo guarda en el sobretodo. —Ese no es para el diario.",
              imagen=["Un canasto lleno de papeles arrugados; arriba, un boceto viejo de un vitral redondo con una firma.",
                      IRIS + " lo sostiene.", TESELA + " lo mira, seria."]),
        ],
    },
    {
        "titulo": "R01-N02 · HTML semántico",
        "misiones": [
            m(id="R01-N02-P1", titulo="El menú que Nora no encuentra",
              lugar=RIOS, personajes="Iris, Nora, Tesela",
              carta="nav | <nav> agrupa los enlaces principales · el lector de pantalla lo anuncia como «navegación»",
              recompensa="xp 10, oro 10",
              escena="""
                  Nora recorre el boceto del ventanal con los dedos, de arriba abajo. —No encuentro el menú —dice—. Para mí son cajas, todas iguales.
              """,
              sugiere="`<div>` no dice nada. `<nav>` dice «acá está la navegación»: el lector de pantalla lo anuncia y deja saltar directo.",
              desafio="Cambiá el `div` de los enlaces por un `nav`.",
              inicial='''
                  <div>
                    <a href="#taller">Taller</a>
                    <a href="#encargos">Encargos</a>
                    <a href="#contacto">Contacto</a>
                  </div>
              ''',
              inspector='''
                  nav a #
                  div #
              ''',
              solucion='''
                  <nav>
                    <a href="#taller">Taller</a>
                    <a href="#encargos">Encargos</a>
                    <a href="#contacto">Contacto</a>
                  </nav>
              ''',
              al_superar="Nora encuentra el menú al instante. —Ahí está. Navegación, tres enlaces.",
              imagen=["Un boceto de ventanal sobre una mesa, dividido en zonas.",
                      NORA + " recorre el plomo con los dedos.", IRIS + " escribe una palabra sobre una zona."]),
            m(id="R01-N02-P2", titulo="Las zonas del ventanal",
              lugar=RIOS, personajes="Iris, Tesela",
              carta="Zonas de la página | <header> cornisa · <main> el contenido (uno solo) · <footer> zócalo",
              recompensa="xp 10, oro 10",
              escena="""
                  El ventanal del Gremio tiene zonas: la cornisa, el panel central y el zócalo. Iris ya eligió los colores de las tres. {mentor} le saca el lápiz de la mano. —Antes de los colores, **nombrá cada zona**.
              """,
              sugiere="`<header>` es la cabecera, `<main>` el contenido principal (uno por página) y `<footer>` el pie.",
              desafio="Cambiá los tres `div` por `header`, `main` y `footer`, en ese orden.",
              inicial='''
                  <div><h1>Los Talleres de los Vitrales</h1></div>
                  <div><p>Encargos de vitrales para todo el mundo.</p></div>
                  <div><p>Hecho con plomo de las Forjas.</p></div>
              ''',
              inspector='''
                  header h1
                  main p
                  footer p
              ''',
              solucion='''
                  <header><h1>Los Talleres de los Vitrales</h1></header>
                  <main><p>Encargos de vitrales para todo el mundo.</p></main>
                  <footer><p>Hecho con plomo de las Forjas.</p></footer>
              ''',
              al_superar="{mentor} le devuelve el lápiz. —Ahora sí, el color. —Iris ya no se acuerda de qué colores había elegido.",
              imagen=["Un ventanal gótico dividido en tres franjas de plomo: arriba, centro y abajo, con etiquetas escritas a mano.",
                      IRIS + " escribe los nombres.", TESELA + " sostiene el lápiz."]),
            m(id="R01-N02-P3", titulo="Una sección con nombre",
              lugar=RIOS, personajes="Iris, Nora",
              carta="section y article | <section> una parte con título propio · <article> algo que se entiende solo (una entrada, una tarjeta)",
              recompensa="xp 10, oro 10",
              escena="""
                  En el panel central van los encargos de la semana. Nora toca uno y pregunta: —¿Esto es una parte del ventanal, o se puede leer suelto?
              """,
              sugiere="`<article>` es algo que se entiende solo, aunque lo saques de la página (un encargo, una noticia). Lleva su propio título.",
              desafio="Envolvé cada encargo (su `h3` y su `p`) en un `article`.",
              inicial='''
                  <section>
                    <h2>Encargos de la semana</h2>
                    <h3>Ventanal de Kaffa</h3>
                    <p>Doce vitrales iguales para la catedral.</p>
                    <h3>Ventana de Ofidia</h3>
                    <p>Una ventana para los pergaminos del Valle.</p>
                  </section>
              ''',
              inspector='''
                  section article #
                  article h3
              ''',
              solucion='''
                  <section>
                    <h2>Encargos de la semana</h2>
                    <article>
                      <h3>Ventanal de Kaffa</h3>
                      <p>Doce vitrales iguales para la catedral.</p>
                    </article>
                    <article>
                      <h3>Ventana de Ofidia</h3>
                      <p>Una ventana para los pergaminos del Valle.</p>
                    </article>
                  </section>
              ''',
              al_superar="Nora pasa de un encargo al otro sin perderse. —Dos encargos. Ahora sé dónde empieza y dónde termina cada uno.",
              imagen=["Un panel de vitral con dos cuadros separados por plomo grueso, cada uno con su título.",
                      NORA + " toca uno de los cuadros.", IRIS + " sonríe."]),
            m(id="R01-N02-P4", titulo="Saltar al contenido",
              lugar=RIOS, personajes="Iris, Nora, Gheco",
              carta="Enlace de salto | <a href=\"#contenido\"> al principio · <main id=\"contenido\"> · el que usa teclado no recorre todo el menú",
              recompensa="xp 10, oro 10",
              escena="""
                  Nora usa el teclado para recorrer las páginas: cada vez tiene que pasar por todos los enlaces del menú antes de llegar a lo importante. —Veinte enlaces —suspira—. Todos los días.
              """,
              sugiere="Un `id` le pone nombre a un elemento, y `href=\"#ese-id\"` salta hasta él. Un enlace **«Saltar al contenido»** al principio le ahorra el menú a quien usa teclado.",
              desafio="Ponele `id=\"contenido\"` al `main`, para que el enlace de salto llegue.",
              inicial='''
                  <a href="#contenido">Saltar al contenido</a>
                  <nav>
                    <a href="#taller">Taller</a>
                    <a href="#encargos">Encargos</a>
                  </nav>
                  <main>
                    <h1>Los Talleres de los Vitrales</h1>
                  </main>
              ''',
              inspector='''
                  a[href="#contenido"]
                  main @id
              ''',
              solucion='''
                  <a href="#contenido">Saltar al contenido</a>
                  <nav>
                    <a href="#taller">Taller</a>
                    <a href="#encargos">Encargos</a>
                  </nav>
                  <main id="contenido">
                    <h1>Los Talleres de los Vitrales</h1>
                  </main>
              ''',
              al_superar="Nora aprieta una tecla y llega directo al título. Se ríe. —Me devolviste diez minutos por día.",
              imagen=["Un pasillo de taller con muchas puertas y un cartel de atajo brillante que salta directo a la última.",
                      NORA + " camina con su bastón de vidrio.", GHECO + " señala el atajo."]),
        ],
    },
    {
        "titulo": "R01-N03 · Formularios",
        "misiones": [
            m(id="R01-N03-P1", titulo="Cada campo con su nombre",
              lugar=VENTANILLA, personajes="Iris, Nora",
              carta="label | <label for=\"id\"> une el texto con su campo · tocar el texto enfoca el campo",
              recompensa="xp 10, oro 10",
              escena="""
                  A la entrada del portal hay una terminal que pide nombre y contraseña. Nora apoya la mano: —Hay dos cajas, pero ninguna dice qué es.
              """,
              sugiere="`<label for=\"usuario\">` se une al campo que tiene `id=\"usuario\"`: el lector de pantalla lo lee, y tocar el texto pone el cursor en el campo.",
              desafio="Agregá el `for` que falta en cada `label`, con el `id` de su campo.",
              inicial='''
                  <form>
                    <label>Usuario</label>
                    <input id="usuario" name="usuario">
                    <label>Contraseña</label>
                    <input id="clave" name="clave" type="password">
                  </form>
              ''',
              inspector='''
                  label @for
              ''',
              solucion='''
                  <form>
                    <label for="usuario">Usuario</label>
                    <input id="usuario" name="usuario">
                    <label for="clave">Contraseña</label>
                    <input id="clave" name="clave" type="password">
                  </form>
              ''',
              al_superar="—Usuario. Contraseña —lee Nora, tocando cada caja—. Ahora sí sé qué me piden.",
              imagen=["Una ventanilla de piedra con una terminal de vidrio que muestra dos campos con su nombre.",
                      NORA + " apoya la mano en la terminal.", IRIS + " al lado."]),
            m(id="R01-N03-P2", titulo="Teo aprieta Entrar",
              lugar=VENTANILLA, personajes="Iris, Teo, Tesela",
              carta="required | <input required> · el navegador no deja enviar el formulario con ese campo vacío",
              recompensa="xp 10, oro 10",
              escena="""
                  Teo deja la terminal vacía y aprieta «Entrar», tres veces, cada vez más fuerte. La terminal acepta todo. —¡Entré! —¿Con qué usuario? —pregunta {mentor}. Teo no sabe.
              """,
              sugiere="Con el atributo `required`, el navegador no deja enviar el formulario si ese campo está vacío, y le avisa solo al que lo llena.",
              desafio="Marcá los dos campos como obligatorios con `required`.",
              inicial='''
                  <form>
                    <label for="usuario">Usuario</label>
                    <input id="usuario" name="usuario">
                    <label for="clave">Contraseña</label>
                    <input id="clave" name="clave" type="password">
                    <button type="submit">Entrar</button>
                  </form>
              ''',
              inspector='''
                  input[required] #
              ''',
              solucion='''
                  <form>
                    <label for="usuario">Usuario</label>
                    <input id="usuario" name="usuario" required>
                    <label for="clave">Contraseña</label>
                    <input id="clave" name="clave" type="password" required>
                    <button type="submit">Entrar</button>
                  </form>
              ''',
              al_superar="Teo vuelve a apretar «Entrar». La terminal le muestra un globito: *Completá este campo*. —¡Está rota! —No está rota —se ríe {mentor}—. Ahora sabe pedir.",
              imagen=["Una terminal de vidrio con un globito de aviso sobre un campo vacío.",
                      TEO + " aprieta un botón con fuerza.", TESELA + " se ríe."]),
            m(id="R01-N03-P3", titulo="El tipo de cada campo",
              lugar=VENTANILLA, personajes="Iris, Gheco",
              carta="Tipos de campo | type=\"email\" · type=\"number\" con min y max · type=\"date\" · el celular muestra el teclado justo",
              recompensa="xp 10, oro 10",
              escena="""
                  El formulario de encargos pide el correo y cuántos vitrales. En el celular de un cliente, el campo del correo muestra el teclado de letras sin `@`, y en «cantidad» se puede escribir «muchos».
              """,
              sugiere="`type=\"email\"` pide un correo (y el celular muestra la `@`); `type=\"number\"` pide un número, y con `min` y `max` marca los límites.",
              desafio="Poné `type=\"email\"` en el correo y `type=\"number\"` con `min=\"1\"` y `max=\"12\"` en la cantidad.",
              inicial='''
                  <form>
                    <label for="correo">Correo</label>
                    <input id="correo" name="correo" required>
                    <label for="cantidad">Cantidad de vitrales</label>
                    <input id="cantidad" name="cantidad">
                  </form>
              ''',
              inspector='''
                  #correo @type
                  #cantidad @type
                  #cantidad @min
                  #cantidad @max
              ''',
              solucion='''
                  <form>
                    <label for="correo">Correo</label>
                    <input id="correo" name="correo" type="email" required>
                    <label for="cantidad">Cantidad de vitrales</label>
                    <input id="cantidad" name="cantidad" type="number" min="1" max="12">
                  </form>
              ''',
              al_superar="Gheco prueba escribir «muchos» en la cantidad. El campo no lo deja. Gheco se ofende un poco.",
              imagen=["Un formulario de vidrio con un campo de correo y un selector de números del 1 al 12.",
                      GHECO + " intenta escribir letras en el campo de números.", IRIS + " se ríe."]),
            m(id="R01-N03-P4", titulo="La carta al Puerto",
              lugar=VENTANILLA, personajes="Iris, Tesela",
              carta="Botones | <button type=\"submit\"> envía · type=\"button\" no envía · type=\"reset\" borra todo (casi nunca se usa)",
              recompensa="xp 10, oro 10",
              escena="""
                  Cuando el formulario está completo, le explica {mentor}, el mensaje viaja al Puerto de los Mensajeros: ahí Elefa lo recibe y lo contesta. —Nosotros armamos la ventanilla; ellos, la respuesta.
                  Pero el botón de enviar está escrito como un enlace.
              """,
              sugiere="Lo que **envía** un formulario es un `<button type=\"submit\">`, adentro del `form`. Un enlace lleva a otra página; no envía nada.",
              desafio="Cambiá el enlace por un `button` de tipo `submit` que diga **Enviar al Puerto**.",
              inicial='''
                  <form>
                    <label for="mensaje">Mensaje</label>
                    <textarea id="mensaje" name="mensaje" required></textarea>
                    <a href="#">Enviar al Puerto</a>
                  </form>
              ''',
              inspector='''
                  form button
                  form button @type
                  form a #
              ''',
              solucion='''
                  <form>
                    <label for="mensaje">Mensaje</label>
                    <textarea id="mensaje" name="mensaje" required></textarea>
                    <button type="submit">Enviar al Puerto</button>
                  </form>
              ''',
              al_superar="Un mensajero de papel sale volando por la ventanilla, rumbo al Puerto. —Elefa contesta rápido —dice {mentor}—. Ya vas a ver.",
              imagen=["Una ventanilla de piedra de la que sale volando un sobre de papel con alas, hacia un faro a lo lejos.",
                      IRIS + " lo mira irse.", TESELA + " con los brazos cruzados."]),
        ],
    },
    {
        "titulo": "R01-N04 · Tablas",
        "misiones": [
            m(id="R01-N04-P1", titulo="La tabla desarmada",
              lugar=LIGA, personajes="Iris, Teo",
              criatura="slime",
              carta="Tablas | <table> · <tr> una fila · <td> una celda · <th> una celda de encabezado",
              recompensa="xp 10, oro 10",
              escena="""
                  En la entrada de los Talleres cuelga la tabla de la **Liga Obsidiana**, pero anoche el Slime desarmó las filas y quedaron los datos sueltos. Teo jura que él estaba primero.
              """,
              sugiere="Una tabla es `<table>` con filas `<tr>`, y cada fila con sus celdas `<td>`. Una fila por aprendiz.",
              desafio="Armá la tabla: una fila `tr` por aprendiz, con dos celdas `td` (nombre y puntos).",
              inicial='''
                  <table>
                    Nadia 120
                    Teo 45
                  </table>
              ''',
              inspector='''
                  tr #
                  td
              ''',
              solucion='''
                  <table>
                    <tr><td>Nadia</td><td>120</td></tr>
                    <tr><td>Teo</td><td>45</td></tr>
                  </table>
              ''',
              al_superar="Los números vuelven a su lugar. Teo tenía 45 puntos. Teo dice que la tabla está mal.",
              imagen=["Un tablero de piedra en la entrada de un taller con una tabla de posiciones de vidrio.",
                      TEO + " señala su nombre, indignado.", IRIS + " acomoda las filas."]),
            m(id="R01-N04-P2", titulo="Para leerla en voz alta",
              lugar=LIGA, personajes="Iris, Nora",
              carta="Encabezados | <thead> con <th scope=\"col\"> · <tbody> con los datos · el lector dice «Puntos: 120» y no un número suelto",
              recompensa="xp 10, oro 10",
              escena="""
                  —Volvé a armarla —le pide {mentor}—, **para que se entienda leyéndola en voz alta**. Nora se ofrece a probarla: —¿120 qué? ¿Años?
              """,
              sugiere="La primera fila va en `<thead>` con celdas `<th scope=\"col\">` (los títulos de las columnas); los datos, en `<tbody>`.",
              desafio="Agregá un `thead` con una fila de dos `th` con `scope=\"col\"`: **Aprendiz** y **Puntos**. Los datos quedan en el `tbody`.",
              inicial='''
                  <table>
                    <tbody>
                      <tr><td>Nadia</td><td>120</td></tr>
                      <tr><td>Teo</td><td>45</td></tr>
                    </tbody>
                  </table>
              ''',
              inspector='''
                  thead th
                  thead th @scope
                  tbody tr #
              ''',
              solucion='''
                  <table>
                    <thead>
                      <tr><th scope="col">Aprendiz</th><th scope="col">Puntos</th></tr>
                    </thead>
                    <tbody>
                      <tr><td>Nadia</td><td>120</td></tr>
                      <tr><td>Teo</td><td>45</td></tr>
                    </tbody>
                  </table>
              ''',
              al_superar="Nora pasa la mano fila por fila: «Aprendiz: Teo. Puntos: 45». Teo no estaba primero.",
              imagen=["Una tabla de posiciones de vidrio con la fila de títulos más gruesa.",
                      NORA + " la recorre con la mano.", TEO + " detrás, con los brazos cruzados."]),
            m(id="R01-N04-P3", titulo="El título de la tabla",
              lugar=LIGA, personajes="Iris, Nora",
              carta="caption | <caption> es el título de la tabla · va primero, adentro de <table>",
              recompensa="xp 10, oro 10",
              escena="""
                  —¿Y de qué es esta tabla? —pregunta Nora—. Antes de los números, decime de qué se trata.
              """,
              sugiere="`<caption>` es el título de una tabla. Va como **primer** elemento adentro de `<table>`.",
              desafio="Agregá un `caption` que diga **Liga Obsidiana: la semana**.",
              inicial='''
                  <table>
                    <thead>
                      <tr><th scope="col">Aprendiz</th><th scope="col">Puntos</th></tr>
                    </thead>
                    <tbody>
                      <tr><td>Nadia</td><td>120</td></tr>
                    </tbody>
                  </table>
              ''',
              inspector='''
                  table caption
              ''',
              solucion='''
                  <table>
                    <caption>Liga Obsidiana: la semana</caption>
                    <thead>
                      <tr><th scope="col">Aprendiz</th><th scope="col">Puntos</th></tr>
                    </thead>
                    <tbody>
                      <tr><td>Nadia</td><td>120</td></tr>
                    </tbody>
                  </table>
              ''',
              al_superar="—Liga Obsidiana —lee Nora—. Ahora sé qué estoy tocando.",
              imagen=["Un cartel de piedra tallada sobre una tabla de vidrio, con el título grabado.",
                      NORA + " toca el título.", IRIS + " al lado."]),
            m(id="R01-N04-P4", titulo="Encabezados de fila",
              lugar=LIGA, personajes="Iris, Nora, Teo",
              carta="th de fila | <th scope=\"row\"> en la primera celda · el lector anuncia de quién es cada número",
              recompensa="xp 10, oro 10",
              escena="""
                  La tabla ahora tiene racha y puntos. Nora pregunta por la fila de Teo: —¿De quién es esta racha de dos días?
              """,
              sugiere="La primera celda de cada fila, si dice **de quién** es la fila, es un `<th scope=\"row\">`: así el lector anuncia «Teo, racha: 2 días».",
              desafio="Convertí la primera celda de cada fila del `tbody` en un `th` con `scope=\"row\"`.",
              inicial='''
                  <table>
                    <thead>
                      <tr><th scope="col">Aprendiz</th><th scope="col">Racha</th><th scope="col">Puntos</th></tr>
                    </thead>
                    <tbody>
                      <tr><td>Nadia</td><td>12 días</td><td>120</td></tr>
                      <tr><td>Teo</td><td>2 días</td><td>45</td></tr>
                    </tbody>
                  </table>
              ''',
              inspector='''
                  tbody th
                  tbody th @scope
                  tbody td #
              ''',
              solucion='''
                  <table>
                    <thead>
                      <tr><th scope="col">Aprendiz</th><th scope="col">Racha</th><th scope="col">Puntos</th></tr>
                    </thead>
                    <tbody>
                      <tr><th scope="row">Nadia</th><td>12 días</td><td>120</td></tr>
                      <tr><th scope="row">Teo</th><td>2 días</td><td>45</td></tr>
                    </tbody>
                  </table>
              ''',
              al_superar="«Teo, racha: dos días», lee Nora. Teo propone que la racha se cuente en horas.",
              imagen=["Una tabla de vidrio con la primera columna en vidrio más oscuro.",
                      NORA + " lee con la mano.", TEO + " protesta al fondo."]),
        ],
    },
    {
        "titulo": "R01-N05 · Jefe: el Slime de las Etiquetas Huérfanas",
        "misiones": [
            m(id="R01-N05-P1", titulo="El escaparate derretido",
              lugar=PANADERIA, personajes="Iris, Tesela",
              criatura="slime",
              carta="Cazar slimes | el navegador «adivina» las etiquetas mal cerradas · el validador las encuentra todas",
              recompensa="xp 15, oro 15",
              escena="""
                  El escaparate de la panadería del Gremio amaneció **derretido**: el título chorrea sobre el párrafo y todo sale en negrita. En el medio, temblando, está el **Slime de las Etiquetas Huérfanas**.
                  —Se alimenta de etiquetas sin cerrar —dice {mentor}—. **Cerralas todas** y se queda sin comida.
              """,
              sugiere="Un `<h2>` sin su `</h2>` se traga todo lo que viene después. Cerrá cada etiqueta antes de abrir la siguiente.",
              desafio="Cerrá el `h2` del título, para que el párrafo quede afuera.",
              inicial='''
                  <h2>Panadería del Gremio
                  <p>Pan de miel recién horneado.</p>
              ''',
              inspector='''
                  h2
                  body > p #
              ''',
              solucion='''
                  <h2>Panadería del Gremio</h2>
                  <p>Pan de miel recién horneado.</p>
              ''',
              al_superar="El título deja de chorrear. El slime pierde una burbuja y achica un poco.",
              imagen=["El escaparate de una panadería de vidrio derretido que chorrea letras.",
                      SLIME + " en la puerta.", IRIS + " frente a él."]),
            m(id="R01-N05-P2", titulo="La lista que se escapó",
              lugar=PANADERIA, personajes="Iris, Gheco",
              criatura="slime",
              carta="Listas bien armadas | cada <li> adentro de su <ul> u <ol> · un <li> suelto es un slime",
              recompensa="xp 15, oro 15",
              escena="""
                  La lista de panes se escapó de su caja: los `li` andan sueltos por el escaparate.
              """,
              sugiere="Un `<li>` siempre vive adentro de un `<ul>` o un `<ol>`. Suelto, el navegador no sabe de qué lista es.",
              desafio="Meté los tres `li` adentro de un `ul`.",
              inicial='''
                  <h2>Panes del día</h2>
                  <li>Pan de miel</li>
                  <li>Trenza de anís</li>
                  <li>Medialunas</li>
              ''',
              inspector='''
                  ul > li #
                  ul > li
              ''',
              solucion='''
                  <h2>Panes del día</h2>
                  <ul>
                    <li>Pan de miel</li>
                    <li>Trenza de anís</li>
                    <li>Medialunas</li>
                  </ul>
              ''',
              al_superar="La lista vuelve a su caja. El slime escupe tres burbujas con forma de `<li>` y se pone pálido.",
              imagen=["Tres panes de vidrio volviendo a ordenarse en una canasta.",
                      SLIME + " escupe burbujas.", GHECO + " lo señala."]),
            m(id="R01-N05-P3", titulo="Todo en negrita",
              lugar=PANADERIA, personajes="Iris, Tesela",
              criatura="slime",
              carta="Cierres en orden | el último que abriste es el primero que cerrás · <p><strong>…</strong></p>",
              recompensa="xp 15, oro 15",
              escena="""
                  Todo el escaparate sale en negrita, hasta el teléfono. Un `strong` quedó abierto y se comió el resto.
              """,
              sugiere="Buscá el `<strong>` que no tiene su `</strong>`, y cerralo donde termina lo importante, **adentro** de su párrafo.",
              desafio="Cerrá el `strong` justo después de **recién horneado**, adentro del primer párrafo.",
              inicial='''
                  <p>Pan de miel <strong>recién horneado</p>
                  <p>Teléfono: 4455-1020</p>
              ''',
              inspector='''
                  strong #
                  strong
                  p
              ''',
              solucion='''
                  <p>Pan de miel <strong>recién horneado</strong></p>
                  <p>Teléfono: 4455-1020</p>
              ''',
              item="Amuleto del Validador",
              al_superar="El teléfono vuelve a verse normal. El slime está casi transparente. {mentor} le cuelga a Iris un vidrio transparente al cuello: se pone rojo donde algo quedó mal cerrado. —**El Amuleto del Validador.** Con esto no se te escapa ninguno.",
              imagen=["Un escaparate con letras gruesas que vuelven a afinarse.",
                      SLIME + " casi transparente.", TESELA + " observa con el monóculo."]),
            m(id="R01-N05-P4", titulo="El fragmento emplomado",
              lugar=PANADERIA, personajes="Iris, Tesela, Gheco",
              criatura="slime",
              carta="Amuleto del Validador | validator.w3.org · *No errors* = el plomo está bien soldado",
              recompensa="xp 20, oro 25",
              item="Fragmento Emplomado",
              escena="""
                  Queda el último cierre: el `div` del escaparate nunca se cerró, y la nota del pie quedó atrapada adentro.
              """,
              sugiere="Cada `<div>` que abrís necesita su `</div>`. Contalos: tiene que haber tantos cierres como aperturas.",
              desafio="Cerrá el `div` del escaparate antes del `footer`, para que el pie quede afuera.",
              inicial='''
                  <div class="escaparate">
                    <h2>Panadería del Gremio</h2>
                    <p>Pan de miel recién horneado.</p>
                  <footer>Abierto de 7 a 13.</footer>
              ''',
              inspector='''
                  .escaparate footer #
                  body > footer
              ''',
              solucion='''
                  <div class="escaparate">
                    <h2>Panadería del Gremio</h2>
                    <p>Pan de miel recién horneado.</p>
                  </div>
                  <footer>Abierto de 7 a 13.</footer>
              ''',
              al_superar="El slime se encoge hasta ser una gotita y se va rodando. {mentor} le pide a Iris el fragmento astillado, lo rodea con una varilla de plomo y lo cuelga en la ventana: ahora se sostiene solo, **el Fragmento Emplomado**. Lo mira con el monóculo y frunce el ceño. —Este plomo no es de los Talleres.",
              imagen=["Una ventana de taller con un fragmento de vidrio iridiscente rodeado de plomo, proyectando rayos de colores.",
                      TESELA + " lo mira con el monóculo, frunciendo el ceño.", IRIS + " con un amuleto de vidrio al cuello.",
                      "Una gotita de slime se va rodando por el piso."]),
        ],
    },
]
