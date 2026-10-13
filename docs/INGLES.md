# Crónicas en Inglés (D106, a revisar)

Un curso **extra de inglés** que recorre las historias de todos los mundos: el alumno lee y practica las crónicas de Iris, Kira, Bron, Zed, Nilo y Mia **en inglés**, con las mismas escenas. Es para **primaria (desde los 6 años)** y después **secundaria**. Todo se **comprueba solo**: el docente no corrige nada, porque los chicos tienen clases presenciales; esto es para leer y ejercitar por su cuenta.

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

## 5. El piloto: los Talleres de los Vitrales

Se usa HTML porque tiene **las 100 escenas**. Son **5 episodios de 4 misiones**, uno por nodo, con las 4 escenas de ese nodo (20 misiones). Se hacen dos versiones del mismo episodio: **Primaria (nivel 1)** y **Secundaria (nivel 4)**, para que el docente compare.

| Episodio | Escenas (HTML) | Qué pasa | Primaria (nivel 1) | Secundaria (nivel 4) |
|---|---|---|---|---|
| 1 · *Iris Arrives* | R00-N01-P1 a P4 | el balcón, el primer vitral, Teo rompe el suyo, el vidrio sin plomo | hello, this is, colores, a / an · cierre E3 | to be, presente simple, pasado irregular · cierre E6 |
| 2 · *The Workshop Diary* | R01-N01-P1 a P4 | el diario de los pasos, las ventanas a otros mundos, Nora, el boceto del Vidriero | números 1–10, *first / then*, objetos (book, pencil, basket) · cierre E3 | imperativos y secuencia (*first, then, finally*) · cierre E6 |
| 3 · *Nora's Window* | R01-N02-P1 a P4 | Nora no encuentra el menú, las zonas del ventanal | partes del cuerpo (hands, fingers), *top / middle / bottom* · cierre E3 | *there is / are*, preposiciones · cierre E7 |
| 4 · *The Gate Terminal* | R01-N03-P1 a P4 | la terminal del portal, Teo aprieta Entrar, la carta al Puerto | *What's your name? My name is…* · cierre E4 con su nombre (patrón) | preguntas, *can / can't* · cierre E7 |
| 5 · *The League Table* | R01-N04-P1 a P4 | la tabla de la Liga Obsidiana, Teo «estaba primero» | números, *first / second / third*, días de la semana · cierre E4 | comparativos y ordinales (*more points than*) · cierre E8 |

El episodio 1 ya está escrito en el prototipo, con 5 misiones (usa además la escena de Nora, R01-N01-P3). En el piloto queda en 4, y la de Nora pasa al episodio 2.

**Qué evalúa el docente con el piloto:** si un chico de 6 lo puede usar solo, si la escritura sube bien de escalón, cuánto tarda cada misión (la meta: 2 a 5 minutos) y si la voz alcanza.

## 6. Cómo entraría en la plataforma (fase propia, después del OK)

- **Curso nuevo `cursos/ingles/`** en el formato del importador. Un `lenguaje: ingles` que **no ejecuta nada**: un comprobador nuevo, `resources/js/runners/english.js`, compara respuestas como el inspector de HTML (D102). No corre código del alumno en ningún lado.
- **Formato de la misión de inglés** (FORMATO-CURSO § 6 bis, variante): en lugar de `Código inicial` / `Salida esperada`, `#### Inglés`, `#### Español`, `#### Palabras` y `#### Ejercicio` (tipo E1–E8, huecos, banco de palabras, respuestas válidas y patrones). `#### Imagen` puede **apuntar a una escena de otro curso** (`imagen: html/R01-N01-P2`), así no se copian archivos. Si una escena no existe, se genera en Stitch y queda en `cursos/ingles/escenas/`.
- **Vista biblioteca:** este curso se muestra como la biblioteca del prototipo, no como el árbol radial (es demasiado para un chico de 6). Mundos → episodios → misiones.
- **Lo que cambia de las reglas** (por eso D106): en un curso **autocomprobado**:
  - los nodos (episodios) **se abren al terminar las misiones** y no con monedas del curso, porque no hay prácticas ni monedas;
  - **no cuentan para el CV**: lo que se comprueba en el navegador se puede trampear;
  - el importador acepta **nodos sin prácticas obligatorias** en ese curso.

  Toda regla de acceso nueva va con su Policy y su test Pest, y se calcula en cada pedido, como siempre.
- **XP y oro**, por el `Ledger` de siempre, al jugador.

## 7. Lo que falta decidir

1. **¿Se cobra?** ¿Abono como los demás cursos, gratis, o incluido con otro curso?
2. **¿Uno o dos cursos?** Recomendación: **dos cursos que comparten las escenas**, *Crónicas en Inglés · Primaria* y *· Secundaria*, porque el texto y los ejercicios son distintos y así cada comisión tiene el suyo.
3. **Las cuentas de los de 6 años:** las crea el docente (como hoy, `StudentAccounts`), con la autorización de menores. ¿Entran con usuario y clave, o hace falta algo más simple (una clave de dibujitos)?
4. **¿Cuántos episodios abren el nivel siguiente?** (propuesta: 4 de 5).
5. **¿Va la protagonista del jugador** (Alfa, JUEGO.md) o el curso de inglés no tiene protagonista propio y se lee la historia de cada mundo tal cual?
