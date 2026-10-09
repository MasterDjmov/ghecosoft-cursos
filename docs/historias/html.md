# HTML y CSS · El arco de Iris (borrador 1, a revisar)

El curso de HTML y CSS, **«Los Talleres de los Vitrales»**, con **Iris** como protagonista fija (JUEGO.md § 1) y **Tesela**, la Vitralista, como mentora. No hay cátedra detrás: el curso es propio y termina con un proyecto grande, **reproducir esta misma plataforma** (GhecoSoft-Code) en celular y en compu. Quedan los **25 nodos** de hoy (decidido 2026-10-08); se suman las micro-misiones, Linux y Windows y lo del juego.

**Linux y Windows siempre:** el docente trabaja en Linux y los alumnos, en Windows. Todo se puede hacer en la plataforma, pero cada vez que se trabaja afuera (VS Code, la extensión Live Server, las herramientas del navegador, Node.js para Tailwind) se dan los pasos en las dos.

---

## 1. El arco

Iris tiene 16 años y dibuja vitrales en una **capilla abandonada** de su mundo. Entre los escombros encuentra un **fragmento de vidrio de colores**, apoya la mano y el vidrio se abre como un portal. Despierta en el balcón de los Talleres, con el fragmento en la mano. Quiere que todo quede **hermoso desde el primer trazo**: tira bocetos, arranca por el color y se frustra. En los Talleres aprende que **todo vitral empieza chico** y que **primero va el plomo y después el color**.

**Las criaturas** son los errores de HTML y CSS (ya están en el diccionario del curso):
- **slimes** por las etiquetas mal cerradas o mal anidadas;
- **goblins** por los valores de CSS inválidos, que el navegador ignora en silencio;
- **esqueletos** por lo que no existe (clases, rutas, enlaces);
- **orcos** por los desbordes en el celular;
- **ogros** por la cascada y la especificidad;
- **trolls** por las capas que se pisan (`position`, `z-index`);
- **dragones** en los jefes grandes.

**El objeto que cambia con ella** es su **fragmento de vidrio** (como la espada de Kira y la llave de Bron):
- **en la Clase 0**, Iris quiere colgar el fragmento en la ventana del taller, sin plomo, y se cae y **se astilla en una punta**: **el Fragmento Astillado**. Tesela: «Un vidrio sin plomo es un vidrio en el piso»;
- **al vencer al Slime** (R01), Tesela le enseña a **emplomarlo**: **el Fragmento Emplomado**, que ya se sostiene solo;
- **al final**, Iris arma **su propio vitral** con el fragmento en el centro, empezando por la ventanita de la cabaña: **el Vitral de Iris**.

**El hilo del portal:** el Vidriero fue **el maestro de Tesela** y desapareció sin terminar su último trabajo (`story.portal_piece`). En los Talleres, Iris lo sigue:
- en la Clase 0, al fondo del taller hay **una puerta con candado** que nadie abre: el taller viejo del Vidriero;
- en R01, entre los bocetos tirados, Iris encuentra **un boceto de un vitral redondo** con la firma del Vidriero;
- en R02, en el armario de los vidrios, **un vidrio de un color que no está en ninguna paleta**, el mismo color que el fragmento de Iris;
- en R03, en el cofre del Gremio, **una plantilla del Vidriero** con la inscripción «para quien llegue»;
- en R04, Tesela abre por fin el taller viejo: en la mesa hay **un marco vacío** con un hueco del tamaño exacto del fragmento. Tesela reconoce el plomo: es del Vidriero. Es el mismo marco que Kira encontró en las Forjas (la Matriz del Marco), que Bron vio en la Ciudadela (las bisagras) y que Zed vio en la Torre del Arquitecto. **Iris no lo arma:** solo lo anticipa. Lo que hace moverse a un vitral se aprende en la **Feria de las Luces** (el curso de JavaScript).

Los protagonistas **no viajan juntos**; los de otros cursos solo se nombran o pasan de visita (Tesla ya pasa por el taller en R02-N02, Kaffa encarga en R02-N04, Ofidia en R03-N04).

### El tono: que sea divertido

Cada crónica tiene **un chiste o una escena cómica** antes de la lección. Los que vuelven a lo largo del curso:

- **Los bocetos de Iris.** Tira cada boceto que no le sale perfecto. Tesela los junta en un canasto y les pone número: «Boceto 1, boceto 2… boceto 214». Al final del curso, el canasto es el muestrario del primer vitral que Iris colgó.
- **La cabaña y el castillo.** Iris siempre revisa primero en el castillo (la compu), y en la ventanita de la cabaña (el celular) algo se rompe. Tesela no dice nada: le alcanza un **espejito de bolsillo** cada vez. A la mitad del curso, Iris ya lo saca sola.
- **Teo y los colores.** Teo, el otro aprendiz, quiere usar **todos los colores a la vez**: sus vitrales parecen árboles de Navidad. Cuando por fin hace uno de dos colores, le sale precioso y no lo puede creer.
- **Nora lee con las manos.** Nora no ve; lee los vitrales tocando el plomo. Cada vez que algo no tiene nombre (un `alt` vacío, un botón sin texto, un `div` donde va un `nav`), Nora lo encuentra en dos segundos y lo dice en voz alta, con una sonrisa.
- **El monóculo de Tesela.** Cuando algo está bien, Tesela se saca el monóculo y lo limpia. Iris tarda medio curso en entender que es un elogio.
- **La vendedora de vidrios.** Ámbar vende «vidrios casi sin burbujas»; siempre tienen una.

### Los personajes

Las fichas completas van en [PERSONAJES.md](PERSONAJES.md) (§ Los Talleres de los Vitrales); las que digan *(falta la imagen)* aparecen en *Admin → Historia → Personajes* para generarlas.

- **Iris** (imágenes completas).
- **Tesela**, la Vitralista, la mentora (tiene imagen; le falta la ficha completa en PERSONAJES.md). Aprendiz de Ferrum junto con Tesla; alumna del Vidriero.
- **Gheco**, que da las pistas.
- **Teo** *(nuevo, a confirmar)*: aprendiz de 15, apurado, desordenado, quiere usar todos los colores. Es el contrapunto de Iris: ella quiere que quede **perfecto** antes de mostrarlo; él lo muestra **antes de terminarlo**. Toma el lugar de Zed en las crónicas.
- **Nora** *(nueva, a confirmar)*: vitralista de 30, ciega, que lee los vitrales tocando el plomo. Es la que enseña la **accesibilidad** sin decir la palabra. Toma el lugar de Mia en las crónicas («Mia lee con los ojos cerrados» pasa a ser Nora, que de verdad no ve).
- **Ámbar** *(nueva, a confirmar)*: vendedora ambulante de vidrios de colores; atiende la tienda de los Talleres (como Chispa en las Forjas y Oto en la Ciudadela).
- **El Vidriero**: no aparece. Solo su obra, su firma y su taller cerrado (NOVELA-GRAFICA.md: «solo su sombra, sus manos o su obra»).

**Los ejemplos y las prácticas** usan poco a otros protagonistas (Kira 8 veces, Zed 3, Mia 2): las presentaciones de Kira («Soy Kira y este es mi primer vitral», «@Kira») pasan a ser de **Iris**, y lo demás, de Teo y Nora. Las capturas «Así tiene que quedar» se rehacen con `node scripts/html-captures.mjs cursos/html --force`.

**Las crónicas pasan a tercera persona con Iris** («Tesela le da el plomo a Iris…»), como las de Zed, Kira y Bron.

### Los jefes (todos tienen nombre; faltan sus fichas)

Hoy los jefes son criaturas del bestiario. Se les da un aspecto propio, como al Gólem de Escoria o a la Quimera:

| Rama | Jefe | Qué deja |
|---|---|---|
| R01 | el Slime de las Etiquetas Huérfanas | **el Fragmento Emplomado** (Tesela le emploma el fragmento) |
| R02 | el Ogro de la Cascada | **el Monóculo de Cristal** (épico: una copia del de Tesela) |
| R03 | el Orco del Desborde | **la Plantilla del Vidriero** (historia: «para quien llegue») |
| R04 | el Dragón de los Talleres | **el Vitral de Iris** (legendario) y **el Marco Vacío** (historia) |

- **El Slime de las Etiquetas Huérfanas:** un slime de **vidrio derretido**, translúcido y de colores, con etiquetas sin cerrar (`<p>`, `<li>`, `</div>`) flotando adentro como burbujas.
- **El Ogro de la Cascada:** un ogro gordo hecho de **capas de vidrios superpuestos** de colores que se tapan unos a otros; lleva un mazo con un `!important` grabado (que no le sirve de nada).
- **El Orco del Desborde:** un orco tan ancho que **no entra en el marco**: medio cuerpo afuera del vitral, estirando los brazos para correr las paredes.
- **El Dragón de los Talleres:** un dragón de **plomo y vidrio** con escamas como teselas de colores, que mira cada detalle con una lupa en la garra.

**La segunda vida de los Talleres** (`Item::SECOND_LIFE`, como el Amuleto del Traceback, el de la Campana, el del Volcado y el del Catch): **el Amuleto del Validador**, que se gana en R01-N05 (el jefe de las etiquetas). Cuando algo se rompe, el validador marca dónde y el vitral se arregla.

---

## 2. Cómo se comprueban solas las micro-misiones: el inspector (D102, decidido 2026-10-08)

En los otros cursos se compara **lo que imprime** el programa. Una página no imprime: se dibuja, en una caja (`iframe sandbox=""`) que la plataforma **no puede mirar por dentro**, y eso no se afloja (D76).

Por eso cada micro-misión de HTML trae una lista de **qué revisar**, y la plataforma lee el código del alumno **sin ejecutarlo** (con `DOMParser`, que no corre scripts ni carga imágenes) y arma un **informe** de texto. El informe se compara con el esperado igual que una salida, y el servidor lo valida igual (`NodeStep::accepts`). Ejemplo:

```
h1: Los Talleres de los Vitrales
img[alt]: Vitral de la entrada
nav a: 3
.tarjeta { padding: 1rem }
button.class: bg-amber-500 hover:bg-amber-600
```

- **HTML:** qué etiquetas hay, su texto, sus atributos (`alt`, `href`, `type`, `required`…) y cuántas hay. El texto se normaliza (espacios juntos).
- **CSS:** las reglas escritas en `<style>` (selector, propiedad y valor), con un lector propio y simple, igual en todos los navegadores: sin comentarios, propiedades en minúscula, espacios juntos. **No** mide cómo quedó dibujado.
- **Tailwind:** qué clases tiene cada elemento (en el orden en que están escritas).
- **Lo visual** («¿quedó lindo?») lo sigue mirando el alumno en la vista previa con las capturas «Así tiene que quedar», y lo corrige el docente en las prácticas.

El alumno ve el informe en la pestaña **Inspector**, con lo que encontró y lo que se esperaba, renglón por renglón (como el aviso de «qué difiere» de las otras micro-misiones).

**Lo que hay que programar:**
1. Una columna `checks` en `node_steps` (texto: un pedido por renglón) y la sección `#### Inspector` en el formato de las micro-misiones (FORMATO-CURSO.md e importador).
2. `resources/js/runners/inspector.js`: arma el informe desde el código y los pedidos. Lo usa el `codeRunner` cuando el lenguaje es HTML y la micro-misión tiene `checks`.
3. `scripts/micro-misiones/genhtml.py` + `browser-check.mjs`: la salida esperada se saca corriendo el inspector **en Chrome** con la solución de referencia (como gencpp.py), y se rechaza la micro-misión si el código inicial ya da el informe esperado.
4. Tests: el inspector no ejecuta nada (un `<script>` o un `onerror` en el código del alumno no corre), el servidor acepta solo el informe esperado.

---

## 3. Los capítulos (crónicas y micro-misiones)

Cada nodo: de 3 a 5 micro-misiones (≈ 100 en total), cada una con su escena, la pista de Gheco, el desafío, lo que pasa al superarla y lo que revisa el inspector. A diferencia de C, los textos pueden llevar tildes: el inspector corre siempre en el navegador y no hace falta pegar nada desde la compu.

**Clase 0 · Hola, HTML** — *El balcón de los Talleres.* Iris despierta con el fragmento en la mano. Quiere colgarlo en la ventana del taller, sin plomo, y el vidrio se cae y **se astilla** (el Fragmento Astillado). Tesela le da una varilla de plomo: «Primero la estructura». Al fondo, una puerta con candado. Consigue: cartas `<!DOCTYPE>`, `<html>`, `<head>`, `<body>`, `<h1>`, `<p>`. Gancho: Teo entra corriendo con un vitral de doce colores, y se le cae.

### Acto I — El Plomo (R01)

- **N01 · Texto, enlaces e imágenes** — *El diario del taller.* Tesela le da a Iris un cuaderno en blanco; Iris tarda una hora en elegir la letra del título. Nora le pregunta qué hay en el dibujo de la mascota, y el dibujo no tiene `alt`. Entre los bocetos tirados, **un boceto de un vitral redondo** firmado por el Vidriero.
- **N02 · HTML semántico** — *El ventanal del Gremio.* Nora recorre el boceto con los dedos y no encuentra el menú: es un `div`. Iris lo nombra (`nav`) y Nora lo encuentra al instante.
- **N03 · Formularios** — *La ventanilla del portal.* Teo deja el formulario vacío y aprieta «Entrar»: el navegador le contesta solo. El mensaje viaja al Puerto, donde lo recibe Elefa (anticipo de PHP).
- **N04 · Tablas** — *La Liga Obsidiana.* El Slime desarmó la tabla de posiciones; Nora la lee en voz alta para ver si se entiende.
- **N05 · Jefe: el Slime de las Etiquetas Huérfanas** — *El escaparate derretido.* La panadería del Gremio amanece derretida. Iris cierra cada etiqueta y el slime se queda sin comida. Tesela le emploma el fragmento: **el Fragmento Emplomado**. Consigue también **el Amuleto del Validador**. Gancho: el plomo del fragmento no es de los Talleres.

### Acto II — Los Vidrios (R02)

- **N01 · Primeros vidrios: CSS** — *El armario de los vidrios.* Iris quiere todos los colores en la primera hora (como Teo). En el fondo del armario, **un vidrio de un color que no está en ninguna paleta**: el del fragmento.
- **N02 · El modelo de caja** — *Las cuatro medidas.* Tesla pasa por el taller y se ríe: «Igual que Tesela cuando éramos aprendices de Ferrum».
- **N03 · Flexbox** — *La regla que se estira.* Iris empuja los vidrios con el dedo; Tesela le da la regla flexible.
- **N04 · Grid** — *Los doce vitrales de Kaffa.* El Arquitecto Imperial no tolera un vidrio torcido.
- **N05 · Responsive: celular primero** — *La cabaña y el castillo.* El Ogro desafía al taller; Tesela le alcanza a Iris el espejito de bolsillo por primera vez.
- **N06 · Jefe: el Ogro de la Cascada** — *El muro de encargos.* Ninguna regla está borrada: otras les ganan. Iris lo vence entendiendo quién le gana a quién. Tesela se saca el monóculo y lo limpia (Iris no entiende). Consigue: **el Monóculo de Cristal**.

### Acto III — Las Plantillas (R03)

- **N01 · Hola, Tailwind** — *El cofre del Gremio.* «Te lo doy ahora porque ya sabés cortar a mano».
- **N02 · Las utilidades** — *Los cajones del cofre.* Teo arma una tarjeta-árbol de Navidad.
- **N03 · Flex y Grid con Tailwind** — *La cabaña sin una regla de CSS.*
- **N04 · Responsive con Tailwind** — *Los pergaminos de Ofidia.* El prefijo `md:`.
- **N05 · Estados y transiciones** — *El vitral mudo.* Teo toca una tarjeta y no pasa nada; Nora la recorre con el teclado y tampoco.
- **N06 · Tema propio** — *Los colores en el cofre.* `#22d3ee` en veinte lugares.
- **N07 · Componentes** — *El muestrario.* El canasto de bocetos de Iris se vuelve el muestrario del taller.
- **N08 · Jefe: el Orco del Desborde** — *El tablón estirado.* En el castillo no se nota; en la cabaña, sí. Consigue: **la Plantilla del Vidriero**, con «para quien llegue».

### Acto IV — El Gran Ventanal (R04)

- **N01 a N04** — *El ventanal del Gremio:* el marco, el panel central, los vidrios de las rutas y el Hall of Fame (la plataforma GhecoSoft-Code). Tesela le pide a Iris un vitral con todas las líderes del mundo juntas.
- **N05 · Jefe final: el Dragón de los Talleres** — *La inspección final.* Celular, teclado y validador. Iris no tira ningún boceto. Tesela abre el taller viejo del Vidriero: **el Marco Vacío**, con un hueco del tamaño del fragmento. Iris arma su propio vitral, empezando por la ventanita de la cabaña: **el Vitral de Iris**. Tesela le muestra el canasto: «Boceto 214. Ese fue el primero que colgaste».

---

## 4. Lo que hay que construir

1. **El inspector** (§ 2) y su generador de micro-misiones.
2. **≈ 100 micro-misiones**, de la Clase 0 al Dragón, todas con la solución de referencia y comprobadas en Chrome.
3. **Iris jugable** (`config('game.protagonists.html')`, 6 aspectos en `public/img/protagonistas/iris/`, de las imágenes que ya están en `publicidad/logos cursos/personajes/Iris/`).
4. **Los ítems de los Talleres** en `app:game-items` (los de la historia, el Amuleto del Validador como segunda vida, `Item::VALIDATOR`), y después la tienda de Ámbar y las recetas.
5. **Las fichas** de Tesela (completa), Teo, Nora, Ámbar y los cuatro jefes en PERSONAJES.md.
6. **Las crónicas en tercera persona** con Iris, Teo y Nora en lugar de Zed y Mia; `story.course_intro`, `branch_completed` y `course_completed` reescritos.
7. **Linux y Windows**: VS Code, Live Server, las herramientas del navegador y Node.js para Tailwind, en la Clase 0 y donde se trabaja afuera.
8. **El mapa de los Talleres** (hecho 2026-10-08: `public/img/mundos/talleres/mapa.webp`). Sus 12 lugares van a `config('game.protagonists.html.expeditions')` cuando Iris sea jugable (x, y en % del mapa, ya revisados sobre la imagen):

   | Lugar | Nodo | x | y |
   |---|---|---|---|
   | El Balcón de los Talleres | R00-N01 | 14 | 77 |
   | El Taller de Tesela | R01-N01 | 33 | 81 |
   | Los Ríos de Plomo | R01-N02 | 28 | 59 |
   | La Ventanilla del Portal | R01-N03 | 47 | 74 |
   | La Panadería del Gremio | R01-N05 | 57 | 68 |
   | El Armario de los Vidrios | R02-N01 | 48 | 46 |
   | La Cabaña y el Castillo | R02-N05 | 61 | 34 |
   | El Muro de Encargos | R02-N06 | 66 | 59 |
   | El Cofre del Gremio | R03-N01 | 76 | 52 |
   | El Muestrario | R03-N07 | 87 | 46 |
   | La Gran Catedral de los Vitrales | R04-N01 | 78 | 23 |
   | El Taller del Vidriero | R04-N05 | 92 | 18 |

## 5. A confirmar con el docente

- Teo, Nora y Ámbar (nombres y aspecto).
- Los cuatro jefes con aspecto propio y lo que deja cada uno.
- El Amuleto del Validador como segunda vida.
