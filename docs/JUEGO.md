# El juego: el jugador, los protagonistas y las micro-misiones (D84, a revisar)

Conversado con el docente entre el 2026-10-04 y el 2026-10-06, a partir de [FICHA-HEROE.md](FICHA-HEROE.md) (D83, que esto reemplaza) y de las ideas de `docs/GeminisIA/` (Tanoth, MapleStory, Lineage 2, MUD). **Estado:** diseño cerrado en lo grande, sin programar. Falta definir el combate, el mapa de cada mundo y cómo corre Java para el alumno (§ 11).

**El problema:** el alumno entrega código, pero no ve qué gana con eso, y los cursos largos (Java, C, C++) lo frenan con explicaciones enormes. **La idea:**
- **Cortar la explicación en micro-misiones cortas**, con historia, que se comprueban solas y lo hacen avanzar rápido.
- **Una capa de juego** (atributos, oro, inventario, monturas, expediciones) que crece con lo que aprende.
- **Una historia sin saltos en cada curso**, con un protagonista propio.

## 1. El jugador y los protagonistas

El Mundo del Código **vive en la mente de quien programa** (el prólogo). El alumno es **esa mente**: el jugador que mueve a los protagonistas.

- **El Alfa crea al jugador**, no a un personaje:
  - la intro animada (el prólogo en 6 tomas, con música opcional): la que armó el docente con Stitch en `publicidad/logos cursos/introduccion novela/` (`intro.html` + `assets/`). Se pasa a una vista propia (sin el Tailwind por CDN, imágenes en webp, música comprimida y con botón). Se ve al crear la cuenta y **se vuelve a ver desde *Mis Crónicas → Prólogo***;
  - Gheco lo recibe en el **Balcón de los Portales**;
  - elige su **apodo**;
  - **el Profe** le muestra el lado del juego: el grimorio, el inventario, los establos y las expediciones.
  - Lo hace cualquiera que se registra, sin pagar. **Los que ya cursan lo completan** la primera vez que entran después del cambio, como una actualización de juego: la plataforma los lleva y les marca en rojo lo que falta.
- **Cada curso tiene su protagonista fijo**, y la historia es la de ese personaje (fichas en [historias/PERSONAJES.md](historias/PERSONAJES.md)):

  | Curso | Protagonista |
  |---|---|
  | Python | **Mia** |
  | Java | **Zed** |
  | C | **Kira** |
  | C++ | **Bron** |
  | PHP | **Nilo** (nuevo) |
  | HTML y CSS | **Iris** (nueva) |

- **Al empezar un curso** («Tomá el control de {heroe}»):
  - el alumno elige el **aspecto** del protagonista entre sus 6 variantes (solo cosmético, sin bonos);
  - le **reparte 24 puntos** entre **Fuerza, Destreza, Inteligencia y Suerte**, cada uno entre 4 y 12. Lo reparte él, sin test. Queda fijo salvo con un **Pergamino del Reinicio**.
  - Vida (HP) y Maná (MP) se calculan de los atributos.
  - Cada protagonista tiene su ficha.
- **`{heroe}` en los textos es el protagonista del curso** (Kira en C, Mia en Python). Como el personaje es siempre el mismo, no hacen falta marcas de género. Gheco le puede hablar al jugador por su apodo cuando conviene. Las imágenes muestran siempre al protagonista real.
- **Mia, Bron y Zed dejan de ser compañeros fijos de todos los cursos** (`companion.theory|uses|errors`):
  - la teoría corta y los errores los toma **Gheco**;
  - los protagonistas se cruzan en otros mundos solo como **anticipo** (una silueta, un rumor), nunca de modo que haga falta haber cursado el otro curso;
  - se juntan en las **incursiones** (§ 9).
- **Solo los cursos base tienen protagonista.** Los accesorios (SDL3, SFML, OpenGL, Laravel, Spring…) se abren por lo aprendido y dan misiones especiales.

## 2. Lo común del jugador

- **Oro**, una moneda de juego aparte de la del curso. Pasa por el `Ledger` como todo saldo.
- **Inventario** con una solapa por lenguaje y una de **comunes** (los ítems que sirven en todos).
- **Monturas.**
- **Nivel del jugador:** crece con el XP de todos sus protagonistas. Empezar un segundo curso también acerca la próxima montura.
- **El grimorio** (§ 4).

## 3. Cómo se dicta: el nodo, las micro-misiones y las prácticas

El **nodo se mantiene**, igual que el árbol, las monedas del curso y el abono. Lo que cambia es su interior:

1. **La explicación larga se corta en micro-misiones** (de 3 a 6 por nodo, de 2 a 5 minutos cada una). Cada una enseña **una sola cosa** y tiene 4 partes, más su imagen:
   1. **Narrativa** (diálogo tipo MUD): dónde está el protagonista, quién le habla y qué necesita.
   2. **La pista de Gheco** («loot intelectual»): el concepto mínimo, con un ejemplo.
   3. **El desafío**: completar o escribir un código corto que el alumno ejecuta.
   4. **La recompensa y el efecto en la historia**: XP, oro, la carta del grimorio, a veces un ítem, y lo que cambia en la escena (el guardián se corre, la antorcha se enciende).
2. **Las micro-misiones se comprueban solas, en el navegador del alumno.** Se compara su salida con la esperada, y opcionalmente con las pruebas (D73).
   - Lo que se comprueba en el navegador se puede trampear, así que **solo dan premios de juego**: XP del protagonista, oro, cartas e ítems.
   - **Nunca dan monedas del curso, nunca abren nodos y no cuentan para el CV.**
   - Es la única corrección automática de la plataforma.
3. **Las prácticas del nodo** (M1, M2…, encargos) **las sigue corrigiendo el docente.** Son las que pagan monedas del curso, abren nodos y valen para el CV, como hoy.
   - Con las micro-misiones el alumno llega mejor preparado, así que se pueden **achicar las obligatorias** (por ejemplo, 2) y el resto pasa a ser optativo con botín.
4. **El error se vuelve monstruo:** una **tabla fija por lenguaje**, sin IA, convierte el error nativo en la criatura del bestiario. Gheco lo explica en palabras del juego, con la pista justa:
   - `SyntaxError` → Slime;
   - `NameError` → Esqueleto;
   - `IndexError`/`KeyError` → Orco.

**Imágenes:** una por micro-misión **cuando la haya**; si no, la del sector o el fondo del mundo. Se nombran por su ID y van en la carpeta del curso, como las capturas de HTML.

**Formato:** las micro-misiones se escriben en el `.md` del curso, en un bloque nuevo dentro del nodo. Se agrega al importador y a [FORMATO-CURSO.md](FORMATO-CURSO.md) cuando se programe.

## 4. El grimorio

Cada tema de [cursos/temas.md](../cursos/temas.md) que el alumno aprende es una **carta**: nombre, sintaxis, un ejemplo y «Copiar».
- Hay una solapa por lenguaje, y adentro, acordeones por grupo (Entrada y salida, Control, Datos…).
- La carta aparece al **superar la micro-misión que la enseña**.
- Es la «memoria externa» del alumno: si en el capítulo 10 se olvidó la sintaxis, la consulta ahí.

## 5. La prueba gratis: Clase 0 y primer nodo

Sin abono, el alumno puede:
- **leer y jugar las micro-misiones de la Clase 0 y del primer nodo** del camino principal;
- **quedarse con los premios de juego.** Esto cambia la D71: hoy la prueba no deja ningún registro, y esto sí lo deja.

Las **prácticas que corrige el docente siguen pidiendo el abono**. Al pagar, todo sigue como hoy: las monedas del curso abren nodos y lo ya ganado jugando no se repite. No hay abono por el curso entero.

## 6. La economía del oro (primer borrador, se ajusta con la simulación)

El freno no es solo el precio: también hay un **nivel mínimo** y un **tope diario de expediciones**. Así nadie compra la montura n5 en dos semanas.

| Fuente | Oro |
|---|---|
| Micro-misión (una sola vez) | 10–30 |
| Práctica aprobada por el docente | 25 |
| Jefe de rama | 200 |
| Expedición corta / media / larga (5 / 15 / 30 min) | ~15 / ~40 / ~80 |
| **Tope:** 6 expediciones por día | |

Un alumno constante junta unos **3.000–4.000 de oro por mes**. El tope es **por cantidad, no por tiempo**: la montura ahorra espera, pero no multiplica el oro.

**Monturas:** se compra la especie (12, en `publicidad/logos cursos/monturas/`) en n1 y se mejora. La especie es cosmética; el nivel es el efecto.

| Nivel | Reduce el tiempo | Precio | Nivel mínimo | Se llega más o menos al |
|---|---|---|---|---|
| n1 | 10% | 300 | 3 | 1.ª semana |
| n2 | 20% | 1.500 | 8 | 1.er mes |
| n3 | 30% | 4.000 | 15 | 2.º–3.er mes |
| n4 | 40% | 8.000 | 22 | 4.º mes |
| n5 | 50% | 15.000 | 30 | 6.º mes o más |

**Atributos con oro:** cada punto extra cuesta **100 × el valor actual** (subir de 10 a 11 cuesta 1.000). El alumno elige entre montura y atributos. Las pociones y las reparaciones también gastan oro.

## 7. Los ítems y el botín

**Regla que no se rompe:** un ítem **nunca limita ni amplía lo que el alumno puede escribir**. Nada de «+3 variables» ni «más lugares en el vector»: el curso deja usar todo lo aprendido. Los ítems **solo afectan al juego**, y el concepto vive en el **nombre y la metáfora**:
- el Bucle de Cobre suma vueltas a la expedición;
- la Bolsa de Malloc da más lugares en la mochila;
- el Amuleto NULL salva de una caída;
- el Cetro `->` sirve en las incursiones.

| Fuente | Qué da | Seguro o al azar |
|---|---|---|
| Micro-misión de la historia | El ítem de esa escena y su carta | **100%, siempre igual**: es la historia lineal |
| Jefe de rama | Un ítem raro del mundo; a veces un Pergamino del Reinicio | El raro es seguro; el pergamino, al 25% |
| Expedición | Siempre **oro y materiales**; ítem: común 20%, raro 5%, épico 1% (los legendarios, solo de jefes) | Al azar, con **contador de mala suerte**: a las 15 expediciones sin raro, cae uno |

Las rarezas usan marco **gris, azul, violeta y dorado**. El catálogo de cada lenguaje sale de su temario, en el orden en que se aprende: los ítems de punteros no aparecen antes que los punteros.

## 8. Expediciones, mapa y combate

- **Cada mundo tiene su mapa** (`mapa.jpeg` en `mundos_cursos/<líder>/`), con lugares. **Cada lugar se abre al terminar su sector** del curso y tiene un nivel de monstruos.
- Como en Tanoth, de los lugares abiertos salen **3 expediciones al azar** (corta, media y larga).
  - Se elige una y corre el **temporizador**.
  - Al volver, **el servidor calcula la pelea** con los atributos, el equipo y la montura.
  - Da oro, materiales y a veces un ítem.
- **Sin código del alumno:** no se puede trampear, no depende del ejecutor de cada lenguaje y no corre nada del alumno en el servidor (solo la cuenta del juego). Las «rutinas aprobadas» de la D83 quedan para más adelante.
- **Pendiente** (§ 11): las fórmulas del combate, qué pasa al perder, cómo se usan HP y MP, y los lugares de cada mapa (salen de la historia de cada curso).

## 9. Incursiones (más adelante)

Jefes fuera de los árboles que se vencen **juntando protagonistas de varios cursos**, como un proyecto real de varios lenguajes. Ahí brillan ítems como el **Cetro del Operador Flecha** (`->`: usar el ítem de otro protagonista sin pasarlo a la mochila) o la **Gema del Puntero Genérico** (`void*`).

## 10. Cómo se escribe la historia de un curso (sin saltos)

De lo grande a lo chico, y **no se escribe un nivel hasta que el docente aprueba el anterior**:

1. **El arco** (1–2 páginas): de dónde viene el protagonista, qué busca, qué misterio lo empuja, cómo cambia y cómo termina; cada rama es un acto.
2. **Los capítulos:** cada nodo, con lugar del mapa, personajes, lo que aprende, lo que consigue y el gancho al siguiente.
3. **La planilla de continuidad:** para cada escena, lugar, quién está, qué lleva encima y qué cambió.
4. **Las micro-misiones** con sus 4 partes y el **pedido de imagen** de cada una, con las descripciones fijas de los personajes de [historias/PERSONAJES.md](historias/PERSONAJES.md).

Orden de los cursos: **Python** (prueba piloto: [historias/python.md](historias/python.md)), **Java**, **C y C++** (los que tienen alumnos frenados), después PHP y HTML.

## 11. Lo que falta definir

- ~~Java para el alumno~~: resuelto con el **ejecutor local en su compu** (D85, *Herramientas → Ejecutor de Java*). Queda investigar Java en el navegador (licencias y peso) para no depender de instalar nada.
- **C y C++ para el alumno:** habilitar el Clang en WebAssembly que ya usa el docente, con el aviso de ~20 MB de descarga.
- **El combate:** fórmulas, derrota, HP y MP, pociones.
- **El mapa de cada mundo:** los lugares, por sector.

## 12. Etapas

1. **El jugador:** la intro animada, el Alfa (apodo, Gheco, el Profe) y el panel del jugador vacío (oro, nivel, inventario, grimorio). Obligatorio para todos.
2. **Los protagonistas:** «Tomá el control» (aspecto + 24 puntos), su ficha, HP y MP, y `{heroe}` por curso. **Mis personajes**: la galería con las fichas completas ([historias/PERSONAJES.md](historias/PERSONAJES.md) § 5), que salen del Diccionario.
3. **Las micro-misiones:** el formato ([historias/python-r01.md](historias/python-r01.md) § 1), el importador, *Admin → Historia → Escenas* (las imágenes por curso, con su pedido), la vista de las 4 partes, la comprobación en el navegador, la recompensa, el grimorio y los errores como monstruos. **Python, rama 1**, como prueba piloto con alumnos reales.
4. **El oro, los ítems y el botín** de micro-misiones y jefes; la tienda de atributos.
5. **Expediciones:** el mapa, el temporizador, las monturas y el combate.
6. **Java, C y C++** con sus historias y su ejecución para el alumno.
7. **Incursiones.**
