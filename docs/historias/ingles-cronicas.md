# Crónicas en Inglés · el Valle, el Imperio y Mis Crónicas — propuesta 2 (2026-10-29), aprobada el 2026-10-29

Junta lo que falta para cerrar los dos cursos de inglés: los ajustes al Valle ([ingles-valle.md](ingles-valle.md)) y al Imperio ([ingles-imperio.md](ingles-imperio.md)) para que no repitan lo que ya enseñan las 5 temporadas cargadas, y el libro de inglés en Mis Crónicas, que hoy está vacío.

## 1. El Valle (temporada 6): qué cambia

Comparado con los `### Objetivos` de las temporadas 1 a 5, en **Secundaria no se repite nada** (presente perfecto, *must / should / have to* y el presente perfecto continuo son nuevos). En **Primaria se repiten tres cosas**:

| Dónde | Propuesta del 2026-10-21 | Ya se vio en | Cambio |
|---|---|---|---|
| Episodio 2 · Baldo's Market | los días de la semana | Talleres (R01-N04) y Puerto (R03-N05) | **los plurales**: *one apple, two apples*, *a box, two boxes*, *a fish, two fish* (Baldo cuenta su mercadería) |
| Episodio 3 · The Bridge of Judgement | el clima | Puerto (R03-N07) | **cómo se siente**: *happy, sad, angry, scared, tired*; *Are you scared? Yes, I am. / No, I'm not.* (el Guardián grita y Eco tiembla) |
| Rama · The Tower Kitchen | días + presente simple | los días, otra vez | **qué tan seguido**: *always, sometimes, never* (*The cook always sings. She never sleeps.*) |

Lo demás de Primaria es nuevo: los animales, la rutina, el **presente simple** con *he / she* y sus preguntas y negativos, la hora en punto y la hora y media.

## 2. El Imperio (temporada 7, final de los dos cursos): qué cambia

**Las escenas:** Java ya tiene las 326 (2026-10-28), así que el tronco y las ramas pueden usar escenas de R03 a R05. Las 4 escenas del final (`IMPERIO-FIN-1` a `4`) siguen siendo necesarias, porque el Gran Borrón no está en Java.

| Dónde | Propuesta del 2026-10-21 | Ya se vio en | Cambio |
|---|---|---|---|
| Primaria · episodio 3 · The Interrogation | *What's your name? How old are you?* | Talleres (R01-N03) | **de dónde sos**: países y nacionalidades: *Where are you from? I'm from… He's Argentinian.* |
| Primaria · rama · The Academy Archive | los ordinales y los cumpleaños | los ordinales, en el Gólem (R05-N02) | **solo las fechas**: *When is your birthday? It's on the fifth of May.* (los ordinales, como repaso) |
| Secundaria · rama · The Mould Workshop | oraciones de relativo | Gólem (R05-N02, N03) | ***wish* + pasado**: *I wish I had a sword. I wish the mould worked.* (va con el segundo condicional) |
| Secundaria · rama · The Academy Archive | *used to* | Gólem (R05-N06) | **órdenes en estilo indirecto**: *The instructor told him to wait. She asked him not to run.* |

Las preguntas en estilo indirecto del episodio 4 (*The clerk asked what he was carrying*) no repiten la nota formal del Puerto (R03-N12, *Could you tell me where…?*): allá eran pedidos amables y acá se cuenta lo que otro preguntó.

## 3. Mis Crónicas de inglés

### Qué tiene hoy y qué le falta
El libro de cada curso de inglés está **vacío**: no tiene bienvenida, ni crónicas de los nodos, ni cierres. Además, el Diccionario de los dos cursos no define al héroe ni a la región. Por eso, donde la plataforma dice «el héroe» en un curso de inglés, hoy sale **Kira** (el valor general), y la región sale sin traducir.

### Lo que propongo
- **Quién habla:** Ada, con su retrato, en todas las páginas (hoy el libro pone el retrato del mentor, que en inglés es el Profe). Es un cambio chico de código: el libro usa a la narradora del curso si el Diccionario la define (`story.narrator`), y si no, al mentor como hasta ahora. Sirve para cualquier curso (D39).
- **El Diccionario de los dos cursos:** `hero.name` = Ada y `story.narrator` = Ada (sin `world.region`: el inglés no es un reino de la enciclopedia).
- **La crónica de cada nodo** (`### Crónica`): la portada de cada episodio ya está narrada por Ada, así que la crónica **no la repite**. Es una **entrada corta de su diario**, que se escribe al terminar el día: qué pasó al final del episodio, qué aprendió y una frase en inglés.
  - **Primaria (Ada de 11):** en español y en presente, 2 o 3 líneas, con la frase del día en inglés y en negrita.
  - **Secundaria (Ada de 15):** **en inglés**, con el tiempo verbal de esa temporada (es lectura extra al nivel del alumno), y la traducción en cursiva debajo. Así se cumple la regla del tiempo (ingles.md § 3 bis): Ada recuerda.
- **Los cierres:**
  - **Bienvenida** (`story.course_intro`): cómo empieza el libro.
  - **Cierre de rama** (`story.branch_completed`): uno solo para todas las ramas, con Eco.
  - **Epílogo** (`story.course_completed`): el final con la carta, que se escribe junto con el Imperio.
  - **Frases de aliento** (`story.locked_hints`).
- **Sin pieza del portal:** el curso de inglés vuelve a contar las historias de todos los mundos, no suma una pieza nueva. Además, si sumara una, cambiaría el «Pieza N de M» de los demás cursos.
- **Cuántos textos son:** 56 crónicas por curso con lo cargado hoy (112 en total) y 24 más con cada temporada nueva. Se escriben por temporada y se reimportan sin tocar el progreso.

### Muestra: los Talleres

**La bienvenida, Primaria.** *Mi libro de crónicas.* Hola, soy Ada. El Profe me dio este libro grande con las páginas en blanco, y una tarea: escribir en la Lengua Común las historias de todo el Mundo del Código. Eco me ayuda, aunque a veces repite todo dos veces. Y el Borrón… el Borrón se come las palabras. Por eso cada página que terminamos la guardo acá.

**La bienvenida, Secundaria.** *The Book, again.* Four years ago I wrote this book for the first time. The Borrón ate half of it. Now I am fifteen, and I am writing it again — with what I remember, with my old notes, and with everything I learned since then.
*Hace cuatro años escribí este libro por primera vez. El Borrón se comió la mitad. Ahora tengo quince, y lo vuelvo a escribir: con lo que recuerdo, con mis notas viejas y con todo lo que aprendí desde entonces.*

**El cierre de rama (los dos cursos).** Eco da tres vueltas sobre la página nueva y canta la última palabra que aprendió hasta quedarse sin voz. Una página más que el Borrón ya no se puede comer.

| Nodo | Primaria (Ada de 11) | Secundaria (Ada de 15) |
|---|---|---|
| R00-N01 · Iris llega | Hoy conocí a Eco. Salió de mi tintero, chiquito y negro, y lo primero que dijo fue **«Hello! Hello!»**. Ahora lo dice todo el tiempo. | *I was eleven, and my book was empty. That day a drop of ink became a bird.* — Tenía once años, y mi libro estaba vacío. Ese día una gota de tinta se volvió un pájaro. |
| R01-N01 · El diario del taller | El Borrón se comió los colores, pero los volvimos a pintar: **red, blue, yellow**. Se escapó al margen, riéndose. Mañana lo atrapo. | *First I chased it, then I lost it, and finally I painted every colour again.* — Primero lo perseguí, después lo perdí y al final pinté de nuevo cada color. |
| R01-N02 · El ventanal de Nora | Nora me hizo tocar el vitral con los ojos cerrados. Arriba estaba frío; abajo, tibio. **Top, middle, bottom.** | *There was a story in every line, Nora said. There were lines everywhere.* — Nora dijo que había una historia en cada línea. Había líneas por todas partes. |
| R01-N03 · La terminal del portal | ¡La terminal sabe mi nombre! Le escribí **«My name is Ada»** y me saludó. Eco quiso escribir el suyo y apretó todas las teclas. | *I couldn't read the terminal, but I could write my name. And it answered.* — No podía leer la terminal, pero podía escribir mi nombre. Y me contestó. |
| R01-N04 · La tabla de la Liga | Tesela me dio una llave de vidrio. **The first page is ready!** Eco está más orgulloso que yo. | *It was the first chapter of my life, and it was the most colourful one.* — Fue el primer capítulo de mi vida, y el más lleno de color. |
| R01-N05 · ¡Todos los colores! (rama) | Teo me tiró los frascos encima y ahora Eco es **pink and green**. Dice Teo que en una semana se le va. | *Teo always ran. He never walked. I usually laughed.* — Teo siempre corría. Nunca caminaba. Yo casi siempre me reía. |
| R01-N06 · Contame los colores (rama) | Nora no ve los colores, así que se los conté: **«It is red, like an apple.»** Eco lo repitió toda la tarde: *apple, apple*. | *Did it sound like glass? Did it feel cold? Nora always asked.* — ¿Sonaba a vidrio? ¿Se sentía frío? Nora siempre preguntaba. |
| R01-N07 · La carretilla de Ámbar (rama) | Le compré a Ámbar un vidrio **«almost no bubbles»**. Tenía una burbuja. Igual es mi preferido. | *I didn't need any glass, but I bought some ink. How much? Too much.* — No necesitaba vidrio, pero compré tinta. ¿Cuánto? Demasiado. |

## 4. Para decidir

1. **El Valle y el Imperio:** ¿van con los cambios de §§ 1 y 2? Siguen abiertas las preguntas de sus propuestas: el chiste de *snake / snack*, el de Eco declarando palabras en la Aduana y si el final con el Gran Borrón es el último episodio del tronco.
2. **Mis Crónicas:**
   - ¿Ada narra con su retrato?
   - ¿La crónica es una entrada de diario, en español en Primaria y en inglés con la traducción en Secundaria?
   - ¿Va sin pieza del portal?
3. **El orden:** primero las crónicas de las 5 temporadas cargadas (un commit por temporada) y después el Valle y el Imperio, cada uno con sus 24 portadas, sus crónicas y su deploy con `--cursos`.
