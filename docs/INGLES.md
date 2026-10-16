# Crónicas en Inglés (D106, fase 1 hecha: para probar)

Dos cursos **extra de inglés**, **Primaria (desde los 6 años)** y **Secundaria**, con **una historia unificada nueva**: Ada, la aprendiz del Profe, pasa a la Lengua Común (el inglés) las crónicas de todas las regiones, con su mascota Eco, y se cruza con todos los personajes: héroes, líderes, criaturas y monturas. La historia está en [historias/ingles.md](historias/ingles.md). Todo se **comprueba solo**: el docente no corrige nada, porque los chicos tienen clases presenciales; esto es para leer y ejercitar por su cuenta.

Prototipo aprobado por el docente (2026-10-13): <https://claude.ai/artifact/MdJTGV9nVpuU94x5oCESEM>. Los botones de escuchar usan la voz del navegador; que suene robótica en algunas compus por ahora no molesta.

---

## 1. Lo que se decidió

- **Público:** primaria desde los 6 años; después, secundaria.
- **Corrección:** toda automática, en el navegador del alumno. No hay prácticas que corrija el docente.
- **Elegir qué leer:** el alumno entra a una **biblioteca** de episodios, agrupados por mundo, y elige cuál **leer** o **practicar**. Cada episodio muestra su avance.
- **La escritura tiene que ir creciendo:** no todo es arrastrar. Cada episodio termina escribiendo, y cuanto más avanza el curso, más se escribe (§ 4).
- **Escenas:** se reusan las de los cursos (no tienen texto). Si la progresión del inglés pide algo que no está, **se arman escenas o tramos de historia nuevos con los mismos personajes** (el docente dio libertad, 2026-10-13).
- **Voz:** la del navegador (Web Speech API), en inglés y en español. Sin costo ni servidor.

## 2. Cómo se ve (lo del prototipo)

- **Biblioteca:** mundos → episodios. Cada tarjeta tiene la escena de portada, el título en español y en inglés, el avance («2 de 4») y dos botones: **Leer** (la crónica entera con «Escuchar todo») y **Practicar**.
- **Misión:** la escena a la izquierda y, debajo, la historia en inglés. **Cada palabra se toca y se escucha.** Hay botones para escuchar en inglés y en español, para ver la traducción y para cambiar la velocidad, más las palabras nuevas con su audio. A la derecha va el desafío y la **pista de Gheco**.
- **Errores = criaturas del bestiario**, como en los cursos de programación:

| Criatura | Error de inglés |
|---|---|
| Slime | ortografía (una letra mal: «¡Casi!») |
| Orco | falta o sobra el artículo (a / an / the) |
| Ogro | orden de las palabras |
| Goblin | verbo que no concuerda (she draw, I is) |
| Esqueleto | palabra que no existe o no es la pedida |
| Troll | (más adelante) la pregunta mal armada: falta do/does |

- **Premio:** XP, oro y una **carta del grimorio** (la palabra o la regla, en inglés y en español). Al terminar el episodio: el resumen de cartas y «Leer la crónica completa».

## 3. Niveles y orden

El orden lo manda la **gramática**, no la historia: una crónica traducida tal cual es demasiado difícil para un chico de 6. La historia de cada mundo se **reescribe en inglés graduado** para el nivel que toca. Los nombres, los lugares y lo que pasa son los mismos.

| Nivel | Para | Inglés | Qué se aprende (resumen) |
|---|---|---|---|
| 1 | Primaria, 6–7 años | pre-A1 | saludos, *this is*, colores, números 1–10, objetos del taller, partes del cuerpo |
| 2 | Primaria, 8–9 | A1 | *to be*, *a / an*, plurales, *there is / are*, *in / on / under*, *can* |
| 3 | Primaria, 10–12 | A1+ | presente simple, presente continuo, posesivos, imperativos, preguntas con *do* |
| 4 | Secundaria 1–2 | A2 | pasado simple, *going to*, comparativos, contables e incontables |
| 5 | Secundaria 3–4 | A2+ / B1 | presente perfecto, *will*, modales, primer condicional |
| 6 | Secundaria 5–6 | B1 | segundo condicional, voz pasiva, estilo indirecto, **inglés técnico** (*function*, *loop*, *tag*, *error*), el puente a los cursos de programación |

**Elegir sin perder el orden:** dentro de un nivel, el alumno elige libremente qué episodio y de qué mundo. El nivel siguiente se abre al terminar una cantidad de episodios del nivel actual (por ejemplo, 4 de 5). Así puede elegir, y la gramática igual avanza en orden. Dentro de un episodio, las misiones se juegan en orden.

## 4. La escritura, por escalones

Cada misión usa uno de estos tipos. Los primeros niveles usan más los de arriba, pero **todo episodio termina en un escalón de escritura**, y cada nivel sube un escalón el piso.

| Escalón | Tipo | Qué hace el alumno | Cómo se comprueba |
|---|---|---|---|
| E1 | **escuchar** | escucha una palabra y toca la correcta | igual a la palabra |
| E2 | **completar / ordenar** | arrastra o toca palabras a los huecos o arma la frase | cada hueco contra su respuesta |
| E3 | **letras** | arma la palabra tocando fichas de letras (también puede tipear) | igual, sin mayúsculas |
| E4 | **escribir la palabra** | tipea la palabra que falta en una frase (con audio de la frase) | igual; a una letra de distancia, «¡Casi!» (slime) |
| E5 | **escribir varias** | completa varias palabras: conjuga, pone el plural | cada una contra sus respuestas válidas |
| E6 | **dictado** | escucha la frase entera y la escribe | palabra por palabra; sin mayúsculas ni puntos; muestra cuáles ya están bien |
| E7 | **responder** | contesta una pregunta sobre la escena con su propia frase: *What color is the glass?* → *The glass is red.* | contra **patrones** con huecos libres: `My name is {nombre}`, `The glass is {color}`; varias respuestas válidas |
| E8 | **transformar** | pasa una frase a negativa, a pregunta o al pasado | contra las formas válidas |

Lo que no se puede comprobar solo (un texto libre largo) queda afuera: el curso es autocomprobado.

| Nivel | Escalones más usados | Cierre de cada episodio |
|---|---|---|
| 1 | E1, E2, E3 | E3 (letras) |
| 2 | E2, E3, E4 | E4 |
| 3 | E2, E4, E5 | E5 o E6 |
| 4 | E4, E5, E6 | E6 o E7 |
| 5–6 | E5, E6, E7, E8 | E7 u E8 |

## 4 bis. Hablar: «Decilo en voz alta» (opcional)

Pedido del docente (2026-10-13). El alumno escucha el modelo, toca el micrófono y dice la palabra o la frase. El **reconocimiento de voz del navegador** (Web Speech API, `SpeechRecognition`) devuelve lo que entendió, con hasta 5 alternativas, y `english.js` lo compara con lo esperado. Prueba suelta para evaluarlo antes de sumarlo: [prototipos/hablar.html](prototipos/hablar.html), que se abre en Chrome o Edge desde `http://localhost/larioja-aprende-cursos/docs/prototipos/hablar.html`. Tiene colores, frases del episodio 1 en Primaria y Secundaria, y una tabla de resultados para copiar.

- **No es un escalón: es un extra.** Se ofrece al lado de cualquier misión de E1 a E7 que tenga una frase corta. **Nunca traba el avance:** sin micrófono, en un navegador que no lo tiene o después de 3 intentos fallidos, aparece «Pasar igual». Decirlo bien suma una estrella en pantalla (por ahora sin XP); el oro y la carta siguen saliendo de la misión escrita.
- **Cómo se comprueba** (con tolerancia, porque las voces de chicos se reconocen peor):
  - Se prueba **cada alternativa** que devuelve el reconocedor, no solo la primera.
  - Se normaliza: minúsculas, sin acentos ni signos; los números pasan a palabra (`2` → `two`); las palabras que **suenan igual** valen lo mismo (*red/read*, *two/too/to*, *blue/blew*, *four/for*, *see/sea*…).
  - **Una palabra sola:** vale si aparece entre lo que dijo («*it's red*» vale por *red*).
  - **Una frase:** distancia palabra por palabra. 0 es bien; hasta 1 palabra de cada 4 es «¡Casi!» (el slime).
  - **Con patrón** (`My name is {nombre}`): vale lo fijo más cualquier cosa en el hueco.
- **Dónde anda:** Chrome y Edge, en la compu y en Android; Safari, a medias; **Firefox, no** (el botón no aparece). Solo en páginas seguras (HTTPS o localhost); producción ya lo es. La plataforma manda `Permissions-Policy: microphone=(self)` (SecurityHeaders): el micrófono, solo para ella misma, nunca para los iframes del código del alumno ni para sitios ajenos.
- **Privacidad (menores):** Chrome manda el audio a Google para reconocerlo (Edge, a Microsoft), y necesita internet. La plataforma no guarda ni recibe audio, solo el texto del resultado. Se avisa en la autorización de menores que firman los padres, y el alumno puede apagarlo en su perfil. Si eso deja de cerrar, se cambia por un reconocedor que corre dentro de la compu (Whisper o Vosk en WebAssembly, 40–75 MB que se bajan una vez), y el ejercicio para el chico queda igual.
- **En el formato de la misión:** `hablar: si` en `#### Ejercicio` (usa la frase de `#### Inglés`) o `hablar: "The glass is red."` para otra frase. Con `patron:` como en E7.

## 5. El piloto: los Talleres de los Vitrales

Se usa HTML porque tiene **las 100 escenas**. Son **5 episodios de 4 misiones**, uno por nodo, con las 4 escenas de ese nodo (20 misiones). Se hacen dos versiones del mismo episodio: **Primaria (nivel 1)** y **Secundaria (nivel 4)**, para que el docente compare.

| Episodio | Escenas (HTML) | Qué pasa | Primaria (nivel 1) | Secundaria (nivel 4) |
|---|---|---|---|---|
| 1 · *Iris Arrives* | R00-N01-P1 a P4 | el balcón, el primer vitral, Teo rompe el suyo, el vidrio sin plomo | hello, this is, colores, a / an · cierre E3 | to be, presente simple, pasado irregular · cierre E6 |
| 2 · *The Workshop Diary* | R01-N01-P1 a P4 | el diario de los pasos, las ventanas a otros mundos, Nora, el boceto del Vidriero | números 1–10, *first / then*, objetos (book, pencil, basket) · cierre E3 | imperativos y secuencia (*first, then, finally*) · cierre E6 |
| 3 · *Nora's Window* | R01-N02-P1 a P4 | Nora no encuentra el menú, las zonas del ventanal | partes del cuerpo (hands, fingers), *top / middle / bottom* · cierre E3 | *there is / are*, preposiciones · cierre E7 |
| 4 · *The Gate Terminal* | R01-N03-P1 a P4 | la terminal del portal, Teo aprieta Entrar, la carta al Puerto | *What's your name? My name is…* · cierre E4 con su nombre (patrón) | preguntas, *can / can't* · cierre E7 |
| 5 · *The League Table* | R01-N04-P1 a P4 | la tabla de la Liga Obsidiana, Teo «estaba primero» | números, *first / second / third*, días de la semana · cierre E4 | comparativos y ordinales (*more points than*) · cierre E8 |

**Los textos y los ejercicios del piloto completo:** [historias/ingles-piloto.md](historias/ingles-piloto.md) (borrador 1, para revisar).

El episodio 1 ya está escrito en el prototipo, con 5 misiones (usa además la escena de Nora, R01-N01-P3). En el piloto queda en 4, y la de Nora pasa al episodio 2.

**Qué evalúa el docente con el piloto:** si un chico de 6 lo puede usar solo, si la escritura sube bien de escalón, cuánto tarda cada misión (la meta: 2 a 5 minutos) y si la voz alcanza.

## 6. En la plataforma (fase 1 hecha el 2026-10-13, para probar)

- **Dos cursos**, en el formato del importador: [cursos/ingles-primaria/](../cursos/ingles-primaria/) y [cursos/ingles-secundaria/](../cursos/ingles-secundaria/), con `lenguaje: english`. Los carga el seeder local (`EnglishCoursesSeeder`) y se importan como cualquier curso. Quedan **sin publicar**: el docente los publica cuando quiera abrirlos.
- **No se ejecuta nada.** `resources/js/runners/english.js` muestra la historia, lee con la voz del navegador y compara las respuestas, como el inspector de HTML (D102). Al resolver, el navegador avisa «superada» y el servidor da los premios de juego (`StepCompleter`).
- **La misión de inglés** (FORMATO-CURSO § 6 ter) usa `#### Inglés` (la historia), `#### Español`, `#### Palabras` («window = ventana», una por renglón), `#### Gheco sugiere` y `#### Ejercicio`. El ejercicio se escribe en líneas simples (`App\Support\EnglishExercise`):

  ```
  tipo: completar          leer, escuchar, completar, ordenar, letras, escribir, dictado, responder, transformar
  consigna: Pintá el vitral.
  banco: red, blue, yellow, green      (con «reusar: si» las fichas no se gastan)
  opciones: hello, girl, gecko         (escuchar)
  hablar: The glass is red.            (el extra de § 4 bis)
  - [#EF4444] {red}                    huecos {a|b}; {*nombre} y {*numero} son libres
  - three = 3                          escuchar: dice «three», se toca «3»
  - door | b, e                        letras: la palabra y letras de más
  - Question? => patrón || otro        responder y transformar
  ```

  El importador lo revisa (tipo, ítems, que la respuesta esté en el banco o en las opciones) y lo guarda armado. `imagen: html/R00-N01-P1` usa la escena de otro curso y `imagen: ingles/NUEVA-01`, las portadas de `cursos/ingles/escenas/`.
- **Cada episodio es un nodo** con 5 micro-misiones: la portada (`tipo: leer`, la escena nueva de Ada y Eco) y las 4 misiones. El episodio 1 es el raíz y se abre con el abono. Los otros cuatro cuelgan de él: al terminar el 1, el alumno **elige libremente** cuál sigue. Se abren sin monedas (precio 0).
- **La biblioteca:** en un curso de inglés, *Árbol* muestra la biblioteca (`livewire/student/library`): la portada de cada episodio, su avance y **Leer** / **Practicar**. El nodo muestra el episodio (`livewire/student/episode`), y con `?leer=1`, el episodio entero para leer y escuchar.
- **Las reglas que cambian, solo en un curso que se comprueba solo** (`Language::isSelfChecked`):
  - un nodo se completa con **todas sus micro-misiones superadas** (`TreeAccess::nodeWorkDone`), y al superar la última se completa (XP del nodo);
  - el importador acepta nodos **sin prácticas**;
  - **cuenta para el CV** como cualquier curso (`CvData`; cambiado el 2026-10-14): sus temas son los episodios terminados, incluido el primero.

  Los tests están en `tests/Feature/Student/EnglishCourseTest.php`.
- **Hecho después del piloto (2026-10-14):** las temporadas (§ 8, abren con el 75 % del tronco anterior); Ada jugable (niña en Primaria, `img/protagonistas/ada/`, y de 15 en Secundaria, `ada-15/`, 6 aspectos cada una, expediciones en los Talleres y la montura **Folio**, n1–n5) con **sus ítems** (`app:game-items`, 15 por curso, con la **Pluma de Eco** de segunda vida) y **el puesto de Ámbar**; **Eco como mascota** que crece con los episodios terminados (JUEGO.md § 11 ter); y **«hablar» da XP**: decir bien la frase da 3 de XP una sola vez por micro-misión (`StepCompleter::speak`).
- **Lo que falta:**
  - las temporadas que siguen (§ 8): Valle, Imperio y las de los cursos nuevos (Talleres, Forjas, Puerto y Ciudadela ya están, con sus ramas);
  - revisar los retratos en el Diccionario y en Mis Crónicas (historias/ingles.md § 7, pasos 3 y 5; la Enciclopedia ya tiene a Ada, Eco y el Borrón).

## 7. Lo que decidió el docente (2026-10-13)

1. **Se cobra como el resto:** abono de 30 días por curso.
2. **Dos cursos, Primaria y Secundaria,** que comparten escenas. Tienen **una historia unificada** para chicos (y su versión para secundaria) que usa a todos los personajes: héroes, líderes, criaturas y monturas ([historias/ingles.md](historias/ingles.md)).
3. **Las cuentas de los más chicos las crea el docente o el administrador** (`StudentAccounts`, como hoy).
4. **Para abrir el nivel siguiente**, para probar: 4 episodios de 5.
5. **Protagonista propio:** uno nuevo, distinto de todos, generado en Stitch y cargado como el resto en la enciclopedia, el diccionario, Mis Crónicas y el juego. La propuesta es Ada, con su mascota Eco ([historias/ingles.md](historias/ingles.md) § 2 y § 7).

## 8. Temporadas: el curso completo (propuesta del 2026-10-14, a revisar)

El docente pidió más que el piloto («5 capítulos de 5 misiones me los terminan en una hora») y que **salgan todos los personajes**: Kira, Zed, Mia, Bron, Nilo… en Primaria y en Secundaria, cada una a su nivel.

- **Una temporada por región**, con su héroe. En la biblioteca los episodios se agrupan por temporada.
- **Tronco y ramas:** unos 8 episodios de tronco con la gramática y 3 o 4 ramas cortas, optativas, con la gente del lugar (el carro de Chispa, el puesto de Fermín, Pico, el comedor de Oto…), que suman vocabulario, oro y botín.
- **La temporada siguiente se abre** con la mayor parte del tronco terminado (por ejemplo 6 de 8; reemplaza el «4 de 5» de § 7).
- **Los dos cursos recorren las seis regiones:** Primaria es el viaje de Ada niña, Secundaria el mismo viaje cuatro años después con inglés más difícil. Cambia lo de historias/ingles.md § 4 (Primaria con 3 regiones y Secundaria con las otras 3).

| Región | Primaria (A1 → A2) | Secundaria (A2 → B1) |
|---|---|---|
| Talleres · Iris | colores, números, *this is*, *to be*, útiles; ramas: más colores (Teo), *What color is it?* (Nora), comprar (Ámbar) | repaso de *to be*, presente simple, *there is/are*; ramas: adverbios de frecuencia (Teo), verbos de los sentidos (Nora), *some/any*, *much/many*, *I'd like* (Ámbar) |
| Puerto · Nilo | saludos, familia, *have got*, *in/on/under* | presente continuo, preguntas (*some/any* ya está en la rama de Ámbar: acá solo se repasa) |
| Forjas · Kira | cuerpo, ropa, *big/hot/heavy*, *can/can't* | pasado simple, comparativos y superlativos |
| Ciudadela · Bron | comida, la casa, números hasta 100, *I like* | futuro (*will* y *going to*), primer condicional |
| Valle · Mia | animales, rutina, presente simple, días y clima | presente perfecto, *must/should* |
| Imperio · Zed | presente continuo, *wh-questions*, meses, repaso | voz pasiva, segundo condicional, estilo indirecto; final con el Gran Borrón |

**Las escenas mandan el orden de trabajo:** C (161) y HTML (100) están completos; C++ (37) y PHP (41) a medias; Python (4) y Java (0) necesitan escenas nuevas en Stitch.

**Se trabaja por tandas**, como el piloto: una temporada escrita en un .md, el docente la revisa y se carga.

**El docente aprobó (2026-10-14)** el orden, la gramática y el tamaño, y empezar por las Forjas. Las Forjas pasan a ser la **temporada 2** (antes de Puerto) porque sus escenas están completas: [historias/ingles-forjas.md](historias/ingles-forjas.md). **Cargada el 2026-10-14** (12 episodios por curso con portadas propias; la regla de temporadas es `TreeAccess::startsSeason`). Después, el Puerto (temporada 3, [historias/ingles-puerto.md](historias/ingles-puerto.md)) y la Ciudadela con Bron (temporada 4, [historias/ingles-ciudadela.md](historias/ingles-ciudadela.md)), las dos cargadas el 2026-10-14.

### El programa nacional y el de La Rioja (analizado el 2026-10-14)

El docente pasó los documentos del [Programa Nacional de Fortalecimiento de la Enseñanza del Inglés](https://www.argentina.gob.ar/capital-humano/educacion/programas-educativos/programa-nacional-de-fortalecimiento-de-la-ensenanza) (2026): el análisis situacional y líneas de acción, y el cuadernillo *Promoting Interaction in the English Classroom*. Lo que sirve para las Crónicas:
- **No fijan temas por grado.** La base de contenidos son los **NAP de Lenguas Extranjeras**, alineados con el **Marco Común Europeo** (A1–B2); cada provincia arma su diseño.
- **La Rioja** tiene diseño provincial basado en los NAP: comunicativo, intercultural y plurilingüe; 2 horas cátedra por semana en primaria y 3 en secundaria; **tres recorridos**: A (desde 1.º grado), B (desde 4.º) y C (desde 7.º). Hay escuelas sin inglés y diferencias de nivel al pasar a secundaria.
- **El problema que marcan en La Rioja:** en la práctica domina la gramática con vocabulario, y no hay material actualizado (las públicas usan cuadernillos fotocopiados). Es el hueco que llenan las Crónicas.
- **Lo que piden:** enfoque comunicativo, oralidad, juego, evaluación formativa, recursos digitales, AICLE/CLIL y aprendizaje por proyectos y tareas.
- **Para las Crónicas:** cada episodio tiene un *para qué* comunicativo; cada temporada se puede empezar desde cero (su primer episodio repasa lo necesario), por los tres recorridos; la voz («Decilo en voz alta») y el audio en cada misión; Secundaria también sirve a quien empieza en 7.º.

### Los cursos que vienen (JavaScript, React Native, Laravel)

Cada curso nuevo trae su región, su héroe, su líder, su gente, sus jefes y sus criaturas, y **todos tienen su reparto en inglés**: una **temporada nueva** en Primaria y en Secundaria, con tronco y ramas, y la gramática según dónde caiga en el recorrido. Sus escenas se reusan en el inglés como las de los demás. **JavaScript (la Feria de las Luces) tiene un héroe nuevo**, no Bron (decidido el 2026-10-16): alguien acorde a la región que ya esté en la historia como personaje secundario (por ejemplo la arquera Nima, la maga Lía o la arquera de Java) o que se vincule con alguno. Su historia y su ficha se arman cuando se arme el curso, o antes si el inglés llega a su temporada. La lista completa de lo que hay que tocar al sumar un curso o un personaje (inglés incluido) está en [ALTA-DE-CURSOS-Y-PERSONAJES.md](ALTA-DE-CURSOS-Y-PERSONAJES.md).
