# Mis Crónicas — el libro de la historia (D80, a revisar)

Conversado con el docente el 2026-10-02. **Estado:** diseño, sin programar.

La historia de cada curso hoy está desparramada: la bienvenida en la página del curso, una crónica en cada nodo, el final al terminarlo. **Mis Crónicas** la junta en un **libro que se va abriendo** a medida que el alumno aprueba: lo que todavía no desbloqueó se ve, pero no se lee, y lo invita a seguir. Lo nuevo late en el menú para que lo encuentre.

## 1. La metáfora (el prólogo)

El Mundo del Código **no está en ningún mapa: vive en la mente de quien programa**. Cada lenguaje es un **portal** a una región distinta; aprender uno abre la puerta al siguiente, y lo que se aprende en uno sirve en todos: **el árbol nunca termina y todo se conecta**. Es una metáfora de aliento: aprender a programar no es llegar a un final, es seguir abriendo puertas.

Borrador del prólogo (lo ve todo el que se registra, aunque no haya pagado ningún curso; se edita en el Diccionario):

> **Prólogo · El mundo que vive en tu mente**
>
> Hay un mundo que no aparece en ningún mapa, {heroe}. No está al otro lado del mar ni detrás de las montañas: está **adentro de la cabeza de quien programa**. Se enciende la primera vez que alguien escribe una instrucción y la ve cobrar vida en la pantalla.
>
> Lo llaman **el Mundo del Código**. Sus regiones no se recorren a pie: se llega a ellas por **portales**, y cada portal es una lengua. Algunos huelen a bosque y a serpiente; otros, a hierro recién forjado; otros brillan como vidrio de colores. Nadie los conoce todos. Nadie terminó nunca de recorrerlo, porque cada puerta que se abre deja ver otras dos.
>
> Por eso, en este mundo, lo que aprendés no se pierde: **cada rama que crece en tu árbol se toca con otra**. Lo que te enseñe una región te va a servir en la siguiente, y en la otra, y en la que todavía no existe.
>
> Esta noche, un portal se abrió para vos. Del otro lado te espera **Gheco**, un gecko de escamas cian que conoce todos los caminos porque trepa por las paredes entre un mundo y otro. —Tranquila, tranquilo —te dice—. Nadie llega sabiendo. **Se llega aprendiendo.**

## 2. Qué tiene el libro

1. **Prólogo**: el de arriba. Abierto para todos.
2. **Un libro por curso** (solo los cursos que el alumno empezó, o cuya Clase 0 probó), con un capítulo por **rama**:
   - la **bienvenida** de la líder (`story.course_intro`), abierta al empezar el curso;
   - la **crónica de cada nodo**, en el orden del árbol, abierta al **completar** ese nodo;
   - el **jefe** de la rama: su crónica, al vencerlo;
   - el cierre de la rama (`story.branch_completed`);
   - el **epílogo** del curso (`story.course_completed`), al terminarlo.
   Las Sendas optativas van al final, como capítulos aparte.
3. **El portal** (el hilo del misterio): una página especial con **una pieza por curso terminado**. Cada líder sabe algo del Vidriero y del portal-vitral; al terminar su curso, lo cuenta. Se muestra como «Pieza 2 de 6», con el vitral del portal que se va armando por partes.

Todo el texto **ya existe** salvo el prólogo, las piezas del portal y las frases de aliento: no hay que reescribir ningún curso.

## 3. Lo bloqueado y las frases de aliento

- Lo que falta desbloquear se ve como una **viñeta en silueta**, con su título (sin el texto) y lo que falta: «Completá *Operadores y expresiones* para seguir leyendo».
- Debajo, una **frase de aliento al azar** de una lista que el docente edita en el Diccionario (`story.locked_hints`, una por línea). Para empezar:
  - «La historia no se escribe sola: la escribís vos, misión a misión.»
  - «¿Qué habrá del otro lado de esta puerta?»
  - «{mentor} te está esperando unas páginas más adelante.»
  - «Cada hoja que aprobás es una página más de tu historia.»
  - «Kira tampoco sabía cómo seguía. Por eso siguió.»
- **Nunca se adelanta la trama:** el servidor no manda el texto de lo bloqueado (con test).

## 4. Lo nuevo late

- En el menú del alumno, **Mis Crónicas** con un **punto que late** cuando hay algo desbloqueado que todavía no leyó, y el número de páginas nuevas.
- Se guarda cuántas páginas desbloqueadas ya vio (`users.chronicles_seen`); si hoy tiene más, hay novedad. Al abrir el libro, se pone al día. Se calcula en cada request, sin cron.
- Al completar un nodo, el aviso de arriba («¡Completaste este nodo!») suma: «Se desbloqueó una página nueva de tus Crónicas».

## 5. Las imágenes

- Sin imágenes nuevas ya se ve bien: cada capítulo usa el **fondo del mundo** (D74), y cada página muestra el retrato de quien habla (la líder, la compañía, la criatura o el jefe).
- **Opcional:** una **ilustración por rama** (unas 30 entre todos los cursos), que el docente genera con Stitch o con IA y sube en el editor del curso. Si no hay, el fondo del mundo.

## 6. Las piezas del portal (borrador, una por curso)

Van en el Diccionario de cada curso (`story.portal_piece`) y se leen al terminarlo:

- **Ofidia (Python):** «Hace mucho cruzó el Valle un viajero con las manos manchadas de plomo. Me preguntó cuál era la lengua más clara del mundo, la que cualquiera pudiera leer. Le dije que la mía. Sonrió y siguió camino hacia las Forjas.»
- **Maese Ferrum (C):** «Me encargó el plomo para un vitral enorme, más grande que cualquier ventana que yo hubiera visto. Pagó por adelantado y nunca me dijo para qué era. Tenía la misma mirada que tiene Tesela cuando sueña.»
- **Tesla (C++):** «Me pidió un mecanismo raro: unas bisagras que pudieran abrir algo que no era una puerta. Las dibujé en un plano y nunca supe si las usó. Hasta que vi tu portal.»
- **Kaffa (Java):** «Trató de explicarme qué estaba construyendo y no pude ponerlo en ninguna clase. Es lo único que nunca supe ordenar: algo que no es de ningún lugar, porque es de todos.»
- **Elefa (PHP):** «Un día llegó al Puerto un mensaje sin remitente, sellado con un sello de vidrio de colores. Decía solamente: *para quien llegue*. Lo guardé veinte años. Creo que ahora es tuyo.»
- **Tesela (HTML y CSS):** «Ese portal es un vitral, y el plomo lo trabajó mi maestro, el Vidriero. Desapareció antes de terminarlo: le falta lo que hace moverse. Eso se aprende en la Feria de las Luces.»

Cada curso nuevo trae su pieza: la cuenta («Pieza N de M») se ajusta sola con los cursos publicados.

## 7. Dónde se ve

- **Menú del alumno → Mis Crónicas** (con el punto que late).
- **En su CV**: «Crónicas: 34 páginas desbloqueadas · 2 piezas del portal».
- El docente ve el libro de un alumno desde su ficha, igual que su árbol.

## 8. Etapas

1. El libro (prólogo + un libro por curso con lo que ya está escrito), lo bloqueado con sus frases y el punto que late en el menú.
2. El portal (las piezas) y el CV.
3. Las ilustraciones por rama.
