# C++ · El arco de Bron (borrador 1, a revisar)

El curso de C++, **«La Ciudadela de los Artífices»**, con **Bron** como protagonista fijo (JUEGO.md § 1) y **Tesla** como mentor. Lo que manda en los contenidos es lo que piden las cátedras: el **apunte de Programación I de la UNLaR** (Camargo, pp. 70–88: clases, `new` y `delete`, herencia con su tabla de accesos, `this`, sobrecarga y operadores amigos) y **Programación II de la UTN** (C++ + STL, unidad 2, y Qt, unidad 3). Los de la UNLaR llegan hasta clases (R02); los de la UTN siguen hasta Qt (R06).

**Linux y Windows siempre:** el docente trabaja en Linux y los alumnos, en Windows. Cada «Cómo compilarlo», cada instalación y cada comando se da en las dos versiones. La UTN usa **VS Code** y **Qt Creator**; la UNLaR, **Code::Blocks**, **ZinjaI** y **VS Code**.

---

## 1. El arco

Bron es un **mecánico** de 24 años, grandote y bonachón, con una llave inglesa cian al hombro. Arregla todo **a mano, pieza por pieza**: si hacen falta cien engranajes, lima cien engranajes. Una noche cruza un vitral que se enciende como un portal y despierta al pie de la cuesta de la Ciudadela, con la llave en la mano. En la Ciudadela aprende lo contrario de lo que sabe: a **dibujar el plano una vez** (una clase, una plantilla) y que las piezas salgan solas.

**Las criaturas** son los errores de C++ (el diccionario del curso ya las define):
- **slimes** por la sintaxis;
- **goblins** por los tipos y las conversiones que pierden datos;
- **esqueletos** por los nombres que no existen o no se enlazan (`was not declared`, `undefined reference`);
- **orcos** por los índices fuera de rango y los iteradores que ya no valen;
- **ogros** por la lógica y el comportamiento indefinido;
- **trolls** por la vida de los objetos mal manejada (`new` sin `delete`, referencias colgantes, dos dueños).

**El objeto que cambia con él** es su **llave inglesa** (como la espada de Kira o la ganzúa de Zed):
- **en la Clase 0**, Bron intenta arreglar a mano el portón de engranajes de la Ciudadela, fuerza la llave en un diente y la **mella**: **la Llave Mellada**;
- **al vencer a la Quimera** (R02), Tesla le muestra que no hace falta una llave por cada tuerca: le arma una que **se ajusta** sola (como un constructor con parámetros): **la Llave Ajustable**;
- **al final**, Bron dibuja el plano de su propia llave, una que sirve para **cualquier** tuerca de la Ciudadela, como una plantilla: **la Llave Universal**.

**El hilo del portal:** según Tesla (`story.portal_piece`), el Vidriero le pidió «unas bisagras que pudieran abrir algo que no era una puerta», y Tesla nunca supo para qué. En la Ciudadela, Bron sigue ese encargo:
- en el Taller hay un **pedido de bisagras** firmado con un vitral;
- en los Planos, el **plano de las bisagras**, con una medida que no cierra con ninguna puerta;
- en el Bestiario, el Mímico copió la bisagra (y no sabe abrir nada con ella);
- en la Gran Biblioteca, el catálogo: la bisagra era una **plantilla**, hecha para cualquier marco;
- en el Laberinto, el Minotauro custodia **el Engranaje del Portal**;
- en los Vitrales, el último vitral muestra el **balcón de los cuatro portales** (una espiral, un engranaje, un vitral y un arco de fuego): el engranaje es el que Bron tiene en la mano.

Es el mismo marco que Zed ve vacío en la Torre del Arquitecto (Java) y que Kira mide en las Forjas (C). Los hilos se cruzan, pero los protagonistas **no viajan juntos**: a Bron le llegan las cartas de Ferrum, quemadas en una esquina (las de C llegan quemadas por lo mismo: Ferrum las lee demasiado cerca del horno).

### El tono: que sea divertido

Cada crónica tiene **un chiste o una escena cómica** antes de la lección, y los errores dan risa antes de dar miedo. Los chistes que vuelven:

- **«¿Y esto para qué me sirve?»** Es la frase de Bron, y la dice en cada nodo. Tesla siempre tiene la respuesta (es la sección «¿Para qué sirve?»), pero a veces se la contesta Lima antes, y Bron se ofende. En la Encrucijada, un aprendiz nuevo le pregunta lo mismo a Bron, y Bron contesta sin pensar.
- **Lima lima lo repetido.** Cada vez que ve dos piezas iguales hechas a mano (o dos funciones copiadas), saca su lima de relojero. Bron esconde las piezas repetidas detrás de la espalda.
- **«¿Y la prueba?»** La Maestra Artífice aparece cuando alguien dice «ya anda». Nadie la vio sonreír, hasta que las pruebas de Bron pasan todas en verde (R05-N03): sonríe medio segundo y Lima jura que fue un tic.
- **El guiso de Oto.** Oto cocina para toda la Ciudadela con recetas exactas; el día que improvisa (un comportamiento indefinido), el guiso sale violeta y nadie sabe por qué. Bron, que también cocina, es el único que se lo come.
- **Los chistes malos de Bron.** Tesla gruñe con cada uno; el día que se ríe, es porque el chiste era de punteros.
- **Las cartas de Ferrum** llegan quemadas en una esquina, siempre en la parte más importante.

### Los personajes

Las fichas completas están en [PERSONAJES.md](PERSONAJES.md) (§ La Ciudadela de los Artífices); las que dicen *(falta la imagen)* aparecen en *Admin → Historia → Personajes* para generarlas.

- **Bron** (protagonista, imágenes completas).
- **Gheco**, que da las pistas.
- **Tesla**, el Artífice Mayor: el mentor. Fue aprendiz de Ferrum junto con Tesela. Rápido, curioso, odia repetir código.
- **Lima** (imágenes completas): aprendiz de relojera de 16 años, chiquita, con una **lima de relojero** en el bolsillo del delantal. Es el contrapunto de Bron: él dice **«¿y esto para qué me sirve?»**; ella, **«¿y si lo hacemos una sola vez?»**. Reemplaza a Kira en los ejemplos.
- **La Maestra Artífice** (imágenes completas): la **inspectora** de la Ciudadela. Nada sale de la Ciudadela sin pasar por sus pruebas. Lleva una tableta con tildes verdes y unos anteojos de soldar en la frente. Frase: «¿Y la prueba?».
- **Lyn** (imágenes completas): la mensajera de la Ciudadela, la más rápida de las torres; apuesta carreras contra todo lo que se mueve, incluidos los programas.
- **Oto** *(nuevo)*: el cocinero del comedor de los artífices, grandote, de recetas exactas.

**Los ejemplos y las prácticas** que hoy usan a Kira (≈ 490 menciones) pasan a **Lima**: tiene cuatro letras y queda en el mismo lugar del abecedario (entre Bron y Lyn), así los listados ordenados no cambian. Las salidas se rehacen ejecutando el código (`scripts/regen-salidas.py`).

**Las crónicas pasan a tercera persona con Bron** («Tesla le muestra a Bron…»), como las de Kira y Zed.

### Los jefes

| Rama | Jefe | Ítem que deja |
|---|---|---|
| R01 | el Autómata de Latón | **el Engranaje de Latón** (accesorio raro) |
| R02 | la Quimera de la Arena | **la Llave Ajustable** (arma rara) |
| R03 | el Mímico del Bestiario | **el Espejo del Mímico** (épico) |
| R04 | el Kraken de los Contenedores | **el Catálogo de Plantillas** (historia) y un épico |
| R05 | el Minotauro del Laberinto | **el Engranaje del Portal** (historia) |
| R06 | la Gárgola de los Vitrales (simulacro **TallerExpress**) | **la Llave Universal** (legendaria) |
| S01 | el Espectro de la Linterna | (Senda) |

**La segunda vida de la Ciudadela** (`Item::SECOND_LIFE`, como el Amuleto del Traceback, el de la Campana y el del Volcado): **el Amuleto del Catch**, que se gana en R05-N01 (excepciones). Cuando algo revienta, el amuleto lo **atrapa** y Bron vuelve a levantarse.

---

## 2. Los contenidos contra las cátedras

| Tema | Dónde |
|---|---|
| Clases, niveles de acceso, constructores y destructores, `inline`, `static` | R02-N01 a N03 |
| **`new` y `delete`** a mano, y **`this`** | R02-N02 (nuevo, 2026-10-08) |
| Sobrecarga de funciones | R01-N05 |
| Sobrecarga de operadores, **`friend`** y la clase `Complejo` del apunte | R02-N04 (nuevo: sección y misión M4) |
| Herencia, **tabla de accesos `public`/`protected`/`private`**, **herencia múltiple** | R02-N06 (nuevo) |
| Polimorfismo, clases abstractas, varios archivos | R02-N07 y N08 |
| Archivos de texto, **binarios con clases y acceso directo** | R03-N06 (nuevo: sección y misión M4) |
| STL: contenedores, iteradores (y los que se invalidan), algoritmos, functores y lambdas | R03 y R04 |
| **`forward_list`** y el idiom **erase-remove** | R04-N03 y N05 (nuevo) |
| **Qt** (UTN, unidad 3): ventanas, señales y slots, formularios, **tus clases detrás de una tabla**, dibujo y modelo-vista | R06 (obligatoria desde 2026-10-08) |
| El examen: **archivos con clases y herencia** + **un programa con Qt y clases** (sin bases de datos) | R06-N05, TallerExpress |

---

## 3. Los capítulos (crónicas y micro-misiones)

**Clase 0 · Hola, C++** — *El portón de engranajes.* Bron despierta al pie de la cuesta, junto a un vitral apagado. El portón de la Ciudadela es una pared de engranajes trabados; Bron saca la llave y los arregla uno por uno, a mano. Al engranaje 47 la llave se traba en un diente y **se mella** (Llave Mellada). Tesla, que lo miraba desde arriba con el visor levantado, baja por una polea: el portón tenía un plano, y con el plano se arreglan los 200 engranajes de una vez. Le da su primer programa. Gancho: Bron pregunta por primera vez «¿y esto para qué me sirve?».

### Acto I — Los Cimientos (R01)

- **N01 · Variables, tipos y operadores** — *El almacén de piezas.* Bron guarda 3,75 kilos de tornillos en un cajón para enteros y le quedan 3: los otros 750 gramos se los llevó un goblin. Lima lo ve y se ríe por primera vez.
- **N02 · Entrada y salida** — *La ventanilla de pedidos.* Lyn pide «dos ruedas dentadas» y el `cin` lee solo «dos».
- **N03 · Decisiones** — *Las compuertas del canal.* Bron abre todas las compuertas «por las dudas» y el comedor de Oto se inunda.
- **N04 · Bucles** — *La cinta transportadora.* La cinta que no se detiene deja a Bron con mil tuercas en la falda; Lima saca la lima.
- **N05 · Funciones** — *Las herramientas con nombre.* Lima le pide que no escriba lo mismo tres veces; Bron lo escribe cuatro, para ver qué pasa (pasa la lima).
- **N06 · Referencias** — *La llave prestada.* Bron le presta su llave a Oto «por copia» y Oto ajusta una llave que no es la de Bron; con una referencia, ajusta la de verdad. En el depósito, un **pedido de bisagras** firmado con un vitral.
- **N07 · Vectores** — *El estante que crece.*
- **N08 · Azar y matemáticas** — *La rueda de la feria.* Lyn apuesta que la rueda cae en rojo; la semilla fija hace que caiga siempre igual y Lyn gana diez veces seguidas, hasta que Tesla se da cuenta.
- **N09 · Jefe: el Autómata de Latón** — *El patio de pruebas.* El autómata solo deja pasar a quien domina los cimientos; Bron lo vence partiendo el problema en funciones, no desarmándolo a mano. Consigue: **el Engranaje de Latón**.

### Acto II — Los Planos (R02)

- **N01 · Structs y clases** — *El archivo de planos.* Bron descubre que un plano no es una pieza: con un plano salen cien. Pregunta para qué le sirve y Tesla le muestra la torre del reloj: un plano, mil engranajes.
- **N02 · Constructores y destructores** (+ `new`, `delete` y `this`) — *El taller de autómatas.* Cada autómata nace en un estado válido y se apaga solo al final del turno; el que Bron armó con `new` sigue dando vueltas a la noche porque nadie hizo `delete`. Oto lo usa de batidora.
- **N03 · Encapsulamiento** — *La caja fuerte del tesoro.*
- **N04 · Operadores** (+ `friend` y `Complejo`) — *La mesa del cartógrafo.* La amistad la da la clase, no la pide la función: Lyn quiere ser amiga de la caja fuerte y la caja no la deja.
- **N05 · Composición** — *El autómata por piezas.* Un autómata **tiene** un motor; no **es** un motor.
- **N06 · Herencia** (+ la tabla de accesos y herencia múltiple) — *Las carpetas de los autómatas.* El autómata pato que vuela y nada.
- **N07 · Polimorfismo** — *El desfile de autómatas.*
- **N08 · Programas en varios archivos** — *Los talleres separados.* En el archivo, el **plano de las bisagras**, con una medida que no cierra con ninguna puerta de la Ciudadela.
- **N09 · Jefe: la Quimera de la Arena** — *La Arena.* Bron la vence sin preguntarle qué es en cada turno: cada forma responde por sí misma. Tesla le arregla la llave: **la Llave Ajustable**. Para los de la UNLaR, acá termina el camino de clases.

### Acto III — Los Talleres Modernos (R03)

- **N01 a N08** — *Los talleres nuevos de la Ciudadela:* `auto`, textos, diccionarios, `optional`, lambdas, archivos (+ binarios), punteros inteligentes y RAII. La Maestra Artífice aparece por primera vez en N08: revisa que cada objeto tenga un solo dueño. Oto descubre que su guiso tenía dos dueños (él y Bron) y que por eso se servía dos veces.
- **N09 · Jefe: el Mímico del Bestiario** — *El Bestiario revuelto.* El Mímico copió la bisagra del Vidriero y no sabe abrir nada con ella. Consigue: **el Espejo del Mímico**.

### Acto IV — La Gran Biblioteca (R04)

- **N01 a N08** — *La biblioteca de la Ciudadela:* plantillas (Lima se emociona: una sola pieza para cualquier tuerca), iteradores (los que se invalidan son estantes que se mudaron), secuencias, mapas, algoritmos, functores, vistas y un contenedor propio.
- **N09 · Jefe: el Kraken de los Contenedores** — *Los sótanos inundados.* Consigue: **el Catálogo de Plantillas**: la bisagra del Vidriero era una plantilla, hecha para cualquier marco.

### Acto V — El Taller del Juego (R05)

- **N01 · Excepciones** — *La red del trapecio.* Bron se cae del andamio y lo ataja una red: **el Amuleto del Catch**.
- **N02 · Depuración** y **N03 · Pruebas y medición** — La Maestra Artífice sonríe medio segundo.
- **N04 y N05** — *Las piezas y el bucle de un juego.*
- **N06 · Jefe: el Minotauro del Laberinto** — Detrás del Minotauro, **el Engranaje del Portal**.

### Acto VI — Los Vitrales (R06)

- **N01 · Ventanas, señales y slots** — *El vitral que espera.* Bron aprieta todos los botones a la vez para ver qué pasa.
- **N02 · Formularios, menús y archivos** — *La oficina de inscripciones.*
- **N03 · Tu clase detrás de la ventana** — *La oficina de patentes.* El empleado suma con los dedos; Bron le escribe el plano primero.
- **N04 · Dibujar y modelo-vista** — *El reloj de la torre.*
- **N05 · Jefe final: la Gárgola de los Vitrales** (simulacro **TallerExpress**) — La Gárgola le toma el examen y Bron, que llegó arreglando 200 engranajes a mano, dibuja el plano de su llave: **la Llave Universal**. El último vitral muestra el balcón de los cuatro portales.
- **N06 · La Encrucijada de los Engranajes** — Tesla cuenta su pieza del portal. Un aprendiz nuevo le pregunta a Bron «¿y esto para qué me sirve?», y Bron contesta sin pensar. Gheco señala la Senda de **la Linterna Mágica** (SDL3).

---

## 4. Lo que hay que construir

**Hecho (2026-10-08, D100):**
1. **C++ para el alumno en el navegador (D100)**, con el encabezado precompilado.
2. **Qt obligatorio (R06)**, con el nodo nuevo «Tu clase detrás de la ventana» y el jefe final **TallerExpress** (consola con pruebas, la ventana y un simulacro con reloj). La migración `renumber_cpp_course_codes` pasa S02 a R06 y la Encrucijada a R06-N06.
3. **Lo que faltaba del apunte y de la STL** (§ 2).
4. **Linux y Windows** en todo el curso: la Clase 0 (ZinjaI, Code::Blocks 25.03 y VS Code con MSYS2), «Cómo compilarlo y ejecutarlo» en cada nodo, CMake, gdb, sanitizadores, Qt (Qt Creator) y SDL3.
5. **Lima** en los ejemplos (salidas rehechas con `scripts/regen-salidas.py`), **las crónicas en tercera persona** con Bron y las fichas de la Ciudadela.
6. **Bron jugable** (`config('game.protagonists.cpp')`, 6 aspectos en `public/img/protagonistas/bron/`) y los ítems de la Ciudadela en `app:game-items`, con el **Amuleto del Catch** como segunda vida (`Item::CATCH`).

7. **163 micro-misiones** (Clase 0 y R01 32, R02 28, R03 28, R04 28, R05 19, R06 16 y la Senda 12), generadas con `scripts/micro-misiones/gencpp.py` y probadas también con el Clang del navegador (`browser-check.mjs`). Las de Qt y SDL3 prueban la lógica sin ventana.

**Falta:**
- ~~El mapa de la Ciudadela~~ (hecho 2026-10-08: `public/img/mundos/ciudadela/mapa.webp` y sus 12 lugares en `config/game.php`, del Portón de Engranajes a la Torre de los Vitrales).
- ~~Las imágenes de los personajes~~ (hechas 2026-10-08: Lima, Lyn, Oto y los siete jefes).
- Las imágenes de los ítems y de las escenas de las 163 micro-misiones; la tienda y las recetas de la Ciudadela.

## 5. Lo que decidió el docente (2026-10-08)

- **Qt pasa al camino obligatorio** como rama nueva (R06), después del Taller del Juego; la Senda de SDL3 sigue optativa.
- **No hay parciales de C++ todavía** (el contenido es nuevo en la UTN), pero se sabe que piden «un programa que interactúe con Qt y clases», sin bases de datos: de ahí sale TallerExpress.
- **C++ corre en el navegador del alumno** (D100).
- **Lima** reemplaza a Kira en los ejemplos, y **la Maestra Artífice** es la inspectora de la Ciudadela.
