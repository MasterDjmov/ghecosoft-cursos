# PHP · El arco de Nilo (borrador 1, a revisar)

El curso de PHP, **«El Puerto de los Mensajeros»**, con **Nilo** como protagonista fijo (JUEGO.md § 1) y **Elefa** como mentora. Los contenidos no cambian: este documento le pone historia a lo que el curso ya enseña (cinco ramas: el Muelle, el Astillero, la Oficina de Correos, la Bodega y el Faro, y cuatro Sendas) y prepara lo que hace falta para las micro-misiones y sus escenas.

**Linux y Windows siempre:** el docente trabaja en Linux y los alumnos, en Windows (XAMPP). Cada instalación y cada comando se da en las dos versiones.

---

## 1. El arco

Nilo es un **mensajero** de 17 años de un pueblo de la costa: charlatán, optimista, rápido… y distraído. Corre sin anotar nada y se olvida de todo entre un pedido y el siguiente. Una noche de tormenta se le vuela una carta del bolso; la persigue por la costa hasta un **faro abandonado**, entra detrás de ella y la escalera lo deja en otro lugar: en lo alto del **Faro del Portal Oculto**, con la lámpara apagada, frente al **Puerto de los Mensajeros**.

En el Puerto aprende lo que le falta: a **recordar**. Es la lección de PHP: cada pedido que llega al servidor llega **solo**, sin memoria del anterior (HTTP no recuerda nada), y para atender bien hay que anotar: variables, sesiones, cookies y, al final, la base de datos. Nilo es, literalmente, un servidor sin estado; Elefa, que tiene **memoria de elefanta**, es lo contrario.

**Las criaturas** son los errores de PHP (el diccionario del curso ya las define):
- **slimes** por la sintaxis (`Parse error`, el `$` o el `;` que falta);
- **goblins** por los tipos que PHP convierte solo (`"10 manzanas"` → `10`) o rechaza (`TypeError`);
- **esqueletos** por los nombres que no existen (`Undefined variable`, la clase que el autoload no encuentra);
- **orcos** por las claves que no están (`Undefined array key`, el campo del formulario que nadie completó);
- **ogros** por la lógica, sobre todo `==` en vez de `===`;
- **trolls** por `null` y `false` donde se esperaba algo (`on null`, la consulta que no encontró nada);
- **dragones**, los jefes: un problema grande hecho de problemas chicos.

**El objeto que cambia con él** es su **bolso cruzado de cuero** (como la llave de Bron o la ganzúa de Zed):
- **en la Clase 0**, la tormenta le rompe la costura y las cartas se le caen por el agujero sin que se dé cuenta: **el Bolso Roto** (lo que entra, se pierde, como un pedido sin sesión);
- **al vencer a la Gorgona** (R03, después de sesiones y cookies), Iara le cose un bolsillo con su nombre bordado, donde guarda lo que tiene que recordar: **el Bolso Remendado**;
- **al final**, después de la Bodega y el Faro, Elefa le da el morral de los correos mayores, con un compartimiento numerado para cada pedido: nada se pierde y todo se encuentra: **el Morral del Correo Mayor**.

**El hilo del portal** (`story.portal_piece`): veinte años atrás llegaron al Puerto, la misma noche de tormenta en que se apagó el Faro, **dos envíos sin remitente** sellados con lacre de **vidrio de colores**, los dos con la misma etiqueta: *«para quien llegue»*. Uno era un paquete y se lo robó un ladrón de techos (es el que encuentra **Zed** en Java, con la llave de plomo adentro); el otro era un mensaje, y Elefa lo guardó. Nilo sigue el rastro:
- en el Muelle, el **libro de cartas sin entregar** tiene una sola línea que nunca se tachó: *«1 mensaje, para quien llegue. Retenido por la Capitana»*;
- en el Astillero, el plano de **una barcaza hecha para llevar un solo vidrio enorme**, encargada por alguien con las manos manchadas de plomo (es la barcaza que encalla en el río del Imperio, en Java);
- en la Oficina de Correos, el registro del robo: *«paquete para quien llegue, robado del Albatros por un ladrón de techos»*; Elefa le cuenta que eran dos y que el otro lo tiene ella;
- en la Bodega, la ficha de esa noche: los dos envíos llegaron **la misma noche en que se apagó el Faro**, y nadie volvió a prenderlo;
- en el Faro, Nilo descubre que **la lente de la lámpara es un vitral** con plomo de las Forjas: el faro por el que llegó es un portal. Al prenderlo, Elefa le entrega el mensaje (su pieza del portal). Cuando Nilo rompe el sello, el vidrio muestra un instante el **balcón de los cuatro portales**: una espiral, un engranaje, un vitral y un arco de fuego.

Es el mismo misterio que Kira mide en las Forjas, Bron sigue en la Ciudadela y Zed abre en el Imperio. Los hilos se cruzan, pero **los protagonistas no viajan juntos**: de Zed, en el Puerto, solo se habla (el ladrón de techos del que todos tienen una anécdota y nadie sabe adónde fue).

### El tono: que sea divertido

Cada crónica tiene **un chiste o una escena cómica** antes de la lección. Los que vuelven:

- **«¿Y vos quién sos?»** Nilo se olvida de todos entre un pedido y el siguiente, como HTTP. Cada mañana le pregunta a Elefa cómo se llama, y ella contesta: «Elefa. Como ayer.» En R03-N04 (sesiones y cookies) Iara le da una **galletita con su nombre estampado** («una cookie, para que te acuerdes») y al otro día Nilo saluda: «¡Buen día, Elefa!». Elefa casi deja caer el bastón.
- **«¿Lo anotaste?»** Es la frase de Iara, y se la dice en cada nodo. Nilo contesta «lo tengo acá» y se toca la cabeza; Iara le muestra el agujero del bolso.
- **Pico, la gaviota ladrona.** Todo lo que se deja sin validar, sin escapar o sin cerrar, Pico se lo lleva: la carta sin sello, el formulario sin revisar, la contraseña escrita en un papel. Nilo, que ama a las gaviotas, la defiende siempre.
- **La campana de la torre.** Cada pedido nuevo es una campanada. Cuando el sistema de Nilo anda solo, la campana suena tres veces (`story.branch_completed`); cuando algo explota, suena sin parar y Fermín se tapa los oídos.
- **Las cartas al destinatario equivocado.** Nilo compara con `==`: le entrega la carta de «Olmo» a «olmo», la del 01 al 1, y la de «0» a nadie. El ogro se ríe; Elefa solo dice «tres iguales, Nilo».
- **Nilo silba** cuando algo le sale bien y deja de silbar cuando ve un orco. Los barcos ya saben: si el mensajero no silba, algo anda mal.

### Los personajes

Las fichas completas están en [PERSONAJES.md](PERSONAJES.md) (§ El Puerto de los Mensajeros); las que dicen *(falta la imagen)* se generan en Stitch con los pedidos de § 5.

- **Nilo** (protagonista, imágenes completas, y su montura **Gran Apex**).
- **Gheco**, que da las pistas.
- **Elefa**, la Capitana del Puerto: la mentora. Una elefanta enorme con armadura gris y violeta y un **bastón coronado por un sello de lacre**, con el que sella cada respuesta antes de que salga. Nunca se olvida de nada. Su regla: «Ningún mensaje se queda sin respuesta, y ninguna respuesta sale sin revisar.» (imágenes completas).
- **Iara** *(nueva)*: la escribiente de la Oficina de Correos, 16 años, con una libreta atada a la muñeca y un lápiz detrás de la oreja. Anota todo. Es el contrapunto de Nilo: él dice **«¡ningún mensaje se queda sin respuesta!»**; ella, **«¿lo anotaste?»**. Reemplaza a Kira en los ejemplos.
- **Fermín, el Bodeguero** *(nuevo)*: el anciano de la Bodega, bajo la torre. Encuentra cualquier ficha entre millones sin mirar, y escribe sus preguntas en una libreta de consultas (SQL). Desconfía de los pedidos «raros» desde el día de la inyección (R04-N05).
- **Marea, la farera** *(nueva)*: la guardiana del Faro (R05). No carga nada ni atiende a nadie: a cada barco le mira la bandera y le señala una dársena (el router). Cuidó el Faro apagado veinte años, esperando que alguien supiera prenderlo.
- **Pico** *(nuevo)*: la gaviota ladrona del Puerto.

**Los ejemplos y las prácticas** usan hoy a Kira (≈ 250 menciones) y a Bron (≈ 90). Kira pasa a **Iara**: tiene cuatro letras y queda en el mismo lugar del abecedario que Kira entre los otros nombres de los ejemplos (Ana, Beto, Carla… Lía, Olmo), así los listados ordenados no cambian. Bron pasa a **Nilo** (el protagonista): ahí sí puede cambiar algún orden, así que las salidas se rehacen ejecutando el código (`php artisan app:course-tests cursos/php --fill`) y se revisan a mano las que el texto explica.

**Las crónicas pasan a tercera persona con Nilo** («Elefa le muestra a Nilo…»), como las de Kira, Bron y Zed. Las que hoy nombran a Kira y a Bron (R04-N07, la transferencia que se cortó) pasan a gente del Puerto.

### Los jefes

Los nombres ya están en las crónicas del curso; se suman lo que dejan y su ficha.

| Rama | Jefe | Ítem que deja |
|---|---|---|
| R01 | la Sirena de los Tipos Débiles | **la Caracola de la Sirena** (accesorio raro: «escuchá bien qué tipo es») |
| R02 | el Gólem del Astillero | **el Martillo del Carpintero de Moldes** (arma rara) |
| R03 | la Gorgona de los Formularios | **el Bolso Remendado** (épico, historia) |
| R04 | la Serpiente Marina de las Tablas | **la Llave de la Bodega** (épico) y la ficha de la noche de la tormenta (historia) |
| R05 | el Dragón del Faro | **el Morral del Correo Mayor** (legendario) |
| S01 | el Campeón Eterno | (Senda) |
| S02 | el Grifo de los Registros | (Senda) |
| S03 | la Orca de los Mensajes | (Senda) |
| S04 | el Hipocampo de las Vidrieras | (Senda) |

**La segunda vida del Puerto** (`Item::SECOND_LIFE`, como el Amuleto del Traceback o el del Catch): **el Salvavidas del `finally`**, que se gana en R02-N09 (excepciones). Cuando algo revienta, el salvavidas lo mantiene a flote y Nilo vuelve a la orilla.

---

## 2. Los capítulos (crónicas y micro-misiones)

**Clase 0 · Hola, PHP** — *El Faro del Portal Oculto.* Nilo sale corriendo detrás de su carta por la escalera del faro abandonado y aparece en lo alto de otro faro, con la lámpara apagada y la carta en la mano: en blanco, salvo un sello de vidrio que se borra. Baja por el **Sendero de las Cartas Perdidas** (sobres viejos enganchados en los arbustos, gaviotas) hasta el Puerto. La campana de la torre suena; en el mostrador, un papel que dice *«¿Hay alguien?»*. Elefa le pide que conteste. Nilo contesta… y a la campanada siguiente ya se olvidó de cómo se llamaba ella. Gancho: el bolso roto.

### Acto I — El Muelle de las Primeras Cartas (R01)

- **N01 · Variables, tipos y conversiones** — *Los cajones del muelle.* Un estibador mete «12 kilos y medio» en el cajón *peso*; Nilo lo lee como 12 y el goblin se lleva el medio kilo.
- **N02 · Operadores** — *La balanza de dos platos.* Nilo entrega la carta del 01 al 1 (`==`); Elefa: «tres iguales, Nilo».
- **N03 · Textos** — *Los casilleros del correo.* Iara aparece por primera vez, limpiando las direcciones que Nilo copió con espacios de más. «¿Lo anotaste?»
- **N04 · Entrada por teclado** — *La ventanilla de encomiendas.* Un cliente contesta «doce kilos»; Nilo lo anota tal cual y la balanza explota en slimes.
- **N05 · Decisiones** — *El cruce de los tres muelles.* Nilo hace de guardia del farol y manda el carro de pescado a la torre.
- **N06 · Bucles** — *La fila de barcos al amanecer.* Nilo descarga cajones hasta que no queda ninguno… y sigue descargando el aire (el bucle que no termina).
- **N07 · Arrays** — *La bodega del tercer muelle.* Cajones en fila y cajones con etiqueta; Pico se roba la etiqueta *sal* y aparece un orco.
- **N08 · Funciones** — *Las oficinas de la torre.* Cada tarea tiene su oficina; Nilo deja de explicar lo mismo diez veces.
- **N09 · include y require** — *El estante de los tomos.* En el libro de cartas sin entregar, la línea que nunca se tachó: *«1 mensaje, para quien llegue»*.
- **N10 · Jefe: la Sirena de los Tipos Débiles** — *La roca de la Sirena.* Canta que «"10" es 10» y que «el cero es nada»; Nilo la vence comparando con `===` y declarando los tipos. Consigue: **la Caracola de la Sirena**.

### Acto II — El Astillero de los Moldes (R02)

- **N01 · Clases y objetos** — *Los moldes de los barcos.* Con un molde salen cien botes; Nilo pinta el suyo de violeta.
- **N02 · Encapsulamiento** — *El timón que dice «Solo el capitán».* Pico gira el timón y el barco encalla.
- **N03 · Static y fábricas** — *La pizarra de la puerta.*
- **N04 · Herencia** — *El árbol de las embarcaciones.*
- **N05 · Abstractas y polimorfismo** — *«Terminá tu pieza».*
- **N06 · Interfaces** — *Las tres reglas de la aduana del Astillero.*
- **N07 · Traits y composición** — *El bote que tiene un motor.* En el cajón de planos viejos, **la barcaza hecha para llevar un solo vidrio**.
- **N08 · Enums y fechas** — *El despacho de pasajes.* «pagado», «Pagada», «PAG»: Iara pierde la paciencia.
- **N09 · Excepciones** — *La grúa trabada en la tormenta.* Nilo cae al agua y lo salva **el Salvavidas del `finally`**.
- **N10 · Namespaces y Composer** — *Los dos timones.*
- **N11 · Jefe: el Gólem del Astillero** — *Los moldes viejos.* Consigue: **el Martillo del Carpintero de Moldes**.

### Acto III — La Oficina de Correos (R03)

- **N01 · Cómo funciona la web** — *Los tubos de bronce.* Cada cilindro que cae es un pedido; cada uno llega solo, sin saber nada del anterior. Nilo se siente comprendido.
- **N02 · GET** y **N03 · POST y validación** — *Las ventanillas.* El formulario que dice «bastante» en el peso.
- **N04 · Sesiones y cookies** — *La fonda sin memoria.* Nilo es el mozo y les pregunta a todos qué querían. Iara le da la galletita con su nombre. Al otro día: «¡Buen día, Elefa!».
- **N05 · Seguridad** — *El tablero que decía «envíos gratis».* Pico se roba un formulario sin la firma de la torre (CSRF).
- **N06 · Login** — *La puerta de la sala de archivos.* La lista de contraseñas en un papel, y Pico.
- **N07 · Subir archivos** — *El retrato que era una trampa.* En el registro de robos: *«paquete para quien llegue, robado del Albatros por un ladrón de techos»*. Elefa: «Eran dos. El otro lo guardé yo.»
- **N08 · Plantillas** — *Los veinte carteles.*
- **N09 · Jefe: la Gorgona de los Formularios** — *El último piso.* Iara le cose el bolso a Nilo: **el Bolso Remendado**.

### Acto IV — La Bodega del Puerto (R04)

- **N01 · Bases de datos** — *La escalera de piedra.* Fermín aparece por primera vez: encuentra cualquier ficha sin mirar. Nilo le pregunta cómo se acuerda de todo; Fermín: «No me acuerdo. Lo anoto bien.»
- **N02 · Consultas** y **N03 · JOIN** — *Las preguntas de Fermín* y *las trescientas fichas de la Gaviota*.
- **N04 · PDO** — *El montacargas.* Por primera vez, la Oficina y la Bodega se hablan.
- **N05 · Consultas preparadas** — *El pedido «Gaviota' OR '1'='1».* Fermín deja de copiar pedidos tal cual.
- **N06 · Un ABM** — *El inventario de repuestos.*
- **N07 · Transacciones** — *La transferencia que se cortó.* Los sellos salieron de la cuenta del Astillero y nunca llegaron a la de la fonda. En la ficha de esa noche, veinte años atrás: los dos envíos y el Faro que se apagó.
- **N08 · Repositorios y login con base** — *Las cuarenta consultas parecidas.*
- **N09 · Jefe: la Serpiente Marina de las Tablas** — *El sótano inundado.* Consigue: **la Llave de la Bodega**.

### Acto V — El Faro (R05)

- **N01 · MVC y router** — *La cúpula del Faro.* Marea, la farera, aparece por primera vez: a cada barco le señala una dársena. Le cuenta a Nilo que el Faro está apagado desde la noche de la tormenta.
- **N02 · Closures y generadores** — *El tablero de palancas y la cinta de cajones.*
- **N03 · API REST** — *Los mensajes de las máquinas.*
- **N04 · PHPUnit** — *El banco de pruebas de la lámpara.*
- **N05 · Errores y logs** — *El libro de guardia.* Nilo empieza a anotar todo. Iara no lo puede creer.
- **N06 · Subir a un hosting** — *Llevar la luz a la costa.* Nilo descubre que la lente de la lámpara es **un vitral**.
- **N07 · Jefe final: el Dragón del Faro** — *La noche de la tormenta.* Con el Dragón vencido, la lámpara se prende. Elefa le da **el Morral del Correo Mayor** y el mensaje que guardó veinte años; al romper el sello, el balcón de los cuatro portales.
- **N08 · La Encrucijada de los Sellos** — *La fuente con forma de sello.* Elefa cuenta su pieza del portal. A la mañana, Nilo la saluda por su nombre sin pensarlo. Gheco señala las Sendas.

### Las Sendas

- **S01 · La Arena del Puerto** (RPG por turnos): el maestro de armas, el reloj de arena gigante y **el Campeón Eterno**.
- **S02 · El Bastión de Laravel** (antes «la Ciudadela de Laravel», que se confundía con la de C++): la fortaleza de piedra clara. Jefe: **el Grifo de los Registros**. Es la última Senda que se trabaja (decisión del docente).
- **S03 · El Palomar** (JavaScript con `fetch`): las palomas mensajeras y **la Orca de los Mensajes** (antes «el Leviatán», que se confundía con el de Java).
- **S04 · El Escaparate** (HTML y CSS): la calle de las vidrieras y **el Hipocampo de las Vidrieras**. Es la Senda que lleva a los Talleres de Tesela.

### Las micro-misiones

Como en C++ (`scripts/micro-misiones/gencpp.py`): unas **4 por nodo** en el tronco y 3 en las Sendas, que se comprueban solas con PHP en WebAssembly en el navegador (D68), con su `#### Imagen` escrito desde esta historia. Cada `#### Imagen` nombra solo a personajes con ficha y referencia en Stitch (Nilo, Elefa, Iara, Fermín, Marea, Pico, Gheco y los jefes), y traduce los números y las letras a algo visual (lecciones de ESCENAS.md).

---

## 3. Los lugares (el mapa de las expediciones)

El mapa que hay (`mundos_cursos/elefa/mapa.jpeg`) es lindo pero no cuadra con el curso: tiene una «Gran Ciudadela Imperial de Elefa» (se confunde con el Imperio de Java), un «Bastión de los Daemons», «Almacenes de Sesionnes» y un «Canal de las Servictor Web» con letras mal escritas. El de los extras de Nilo (*La Costa de los Faros*) tiene el Faro del Portal Oculto y el Sendero de las Cartas Perdidas, que sí entran en la historia (la Clase 0). Se rehace en Stitch con este recorrido, de abajo a la izquierda hacia el Faro, como el de la Ciudadela:

| Lugar | Nodo | Qué se ve |
|---|---|---|
| El Sendero de las Cartas Perdidas | R00-N01 | camino de la costa con sobres viejos enganchados en los arbustos |
| El Muelle de las Primeras Cartas | R01-N01 | muelles de madera, cajones con etiquetas, grúas |
| El Cruce de los Tres Muelles | R01-N05 | el guardia del farol y los carros |
| La Roca de la Sirena | R01-N10 | una roca con algas en la boca del puerto |
| El Astillero de los Moldes | R02-N01 | galpones con moldes de barcos colgados y cascos a medio armar |
| La Grúa de la Tormenta | R02-N09 | la grúa del muelle 2 y el agua revuelta |
| La Torre de la Campana | R03-N01 | la Oficina de Correos, con tubos de bronce y la campana en lo alto |
| La Fonda del Puerto | R03-N04 | la fonda sin memoria |
| La Bodega del Puerto | R04-N01 | galerías de piedra bajo la torre, estanterías de fichas |
| El Sótano Inundado | R04-N09 | donde se filtra el mar; la Serpiente |
| El Faro | R05-N01 | en la punta del muelle más largo, el faro apagado (el mismo por el que llegó Nilo) |
| La Encrucijada de los Sellos | R05-N08 | la plaza con la fuente con forma de sello; los caminos a la Arena, el Bastión, el Palomar y el Escaparate |

---

**Dónde está cada lugar en el mapa nuevo** (en %, para `config('game.protagonists.php.expeditions.places')`): Sendero 15,92 · Muelle 21,82 · Cruce 40,85 · Roca de la Sirena 12,48 · Grúa 45,46 · Astillero 56,55 · Torre 50,26 · Fonda 64,70 · Bodega 64,92 · Sótano 77,84 · Encrucijada 78,58 · Faro 92,13.

## 4. Lo que hay que construir (por etapas, cada una con el OK del docente)

1. **Esta historia y las fichas** (este documento y PERSONAJES.md § El Puerto de los Mensajeros). Hecho y aprobado (2026-10-11).
2. **Las referencias en Stitch** (hechas 2026-10-11, proyecto `12272294721581088244`, ids en `REFS['php']`), y **el mapa nuevo** en `public/img/mundos/puerto/mapa.webp` (copia en `mundos_cursos/elefa/mapa_puerto.jpeg`). Pendiente: los circulares de la compañía nueva, si se quieren (la enciclopedia recorta el retrato del cuerpo entero): un proyecto de PHP con Nilo y Elefa (de sus imágenes), y Gheco, Iara, Fermín, Marea, Pico y los nueve jefes generados desde sus fichas con los pedidos de § 5. Se guardan en `publicidad/logos cursos/personajes/El Puerto de los Mensajeros/` (cuerpo entero y circular) y van a `REFS['php']` de `scripts/escenas/pendientes.py`.
3. **El curso** (hecho 2026-10-11): Iara y Nilo en los ejemplos (las salidas se revisaron con `app:course-tests` y con `scripts/regen-salidas.py cursos/php`, que ahora también corre PHP), las 63 crónicas en tercera persona con Nilo, Iara, Fermín, Marea y Pico, las pistas del portal en cada rama, el diccionario y los nombres nuevos (el Bastión de Laravel, la Orca de los Mensajes). El `lugar:` va en cada micro-misión (paso 5).
4. **Nilo jugable** (hecho 2026-10-11): `config('game.protagonists.php')` con sus 6 aspectos (`public/img/protagonistas/nilo/`, de la gorra al uniforme de gala), **el puesto de Fermín** (15 ítems del Puerto, 4 que solo se fabrican y 5 recetas), lo que gana Nilo en la historia (el Bolso Roto, la Caracola de la Sirena, el Martillo del Carpintero de Moldes, el Bolso Remendado, la Llave de la Bodega, la Ficha de la Noche de la Tormenta, el Morral del Correo Mayor y el Mensaje para quien llegue), **el Salvavidas del `finally`** como segunda vida (`Item::LIFEBUOY`) y las expediciones en el mapa nuevo, con sus 12 lugares. Faltan las imágenes de los ítems (sus pedidos ya están en *Admin → Juego → Ítems*).
5. **Las micro-misiones** (hechas 2026-10-11): **213**, una tanda por rama (`scripts/micro-misiones/php_r01.py` … `php_sendas_b.py`), generadas con `genphp.py` (PHP 8.3, sin avisos, sin reloj ni azar sin semilla, corridas dos veces) y verificadas **las 213 en Chrome** con el PHP del alumno (D105, `browser-check.mjs`). La Bodega usa PDO con SQLite en memoria (el mismo SQL que MariaDB); las pruebas, una `afirmar()` propia (PHPUnit no corre suelto en el navegador); el Bastión imita Laravel con PHP puro. Cada una trae su `#### Imagen` con los personajes de `REFS['php']`.
6. **Las escenas** en Stitch, de a una, como en C++. En curso: 6 de 213 (2026-10-11), sigue `R01-N01-P3`.

---

## 5. Pedidos para Stitch (referencias de personajes)

Cada pedido genera un **cuerpo entero 896×1200** sobre el fondo de grilla oscura de los demás personajes (el estilo de Nilo y Elefa: anime/cómic cyber-arcana, contorno marcado, luz violeta y cian). Después, el **circular 1024×1024** con el mismo personaje, sin nombre escrito. Todos llevan: *«Sin texto de ningún tipo: ni letras, ni números, ni carteles.»* Para que el estilo cuadre, se piden **seleccionando a Nilo y a Elefa como referencia de estilo** («no los modifiques; usalos solo para el estilo del dibujo»).

- **Iara:** chica de 16 años, bajita (1,58 m) y delgada, piel morena, ojos negros grandes, pelo negro lacio largo atado en una cola baja con una cinta turquesa; lápiz detrás de la oreja. Blusa blanca arremangada, chaleco azul petróleo con muchos bolsillos con sobres, pollera larga gris, botas cortas con luz cian. Una libreta de cuero atada a la muñeca con un cordón. Expresión: ceja levantada, a punto de preguntar «¿lo anotaste?».
- **Fermín, el Bodeguero:** anciano de 80 años, bajo y encorvado, flaco, piel clara arrugada, barba blanca larga y prolija, anteojos redondos de marco de bronce en la punta de la nariz. Guardapolvo gris largo con manguitos negros, gorro de lana. En una mano un farol con luz cian; en la otra, una libreta cerrada. Expresión tranquila, de alguien que nunca se apura.
- **Marea, la farera:** mujer de 45 años, alta (1,78 m) y fuerte, piel curtida por el sol, pelo gris ondulado recogido con un pañuelo violeta, una cicatriz chica en el mentón. Impermeable largo amarillo oscuro de farera sobre ropa azul marino, botas de goma. Sostiene un **farol de señales** con dos vidrios (violeta y cian). Expresión serena y firme.
- **Pico:** una gaviota blanca y gris, regordeta y descarada, con el pico amarillo y una mancha violeta en una ala; lleva un sobre robado en el pico. Del tamaño de una gaviota real.
- **Gheco:** el gecko cian de la plataforma, chiquito (del tamaño de una mano), como en su imagen oficial.
- **La Sirena de los Tipos Débiles:** sirena de piel verde agua y escamas violetas, pelo largo de algas, sentada en una roca; los ojos brillan de dos colores distintos (uno cian, uno violeta), como si dijera dos cosas a la vez. Burbujas con símbolos que cambian de forma.
- **El Gólem del Astillero:** gigante hecho de tablas de barco, clavos torcidos, sogas y moldes de madera pegados a las apuradas; un timón en el pecho, un brazo más largo que el otro. Ojos de brasa violeta.
- **La Gorgona de los Formularios:** mujer-serpiente cuyo pelo son decenas de **cintas de papel y serpientes de pergamino** que se retuercen; ojos que brillan en violeta. Lleva una pluma de escribir enorme como lanza.
- **La Serpiente Marina de las Tablas:** serpiente marina enorme de escamas azul oscuro con **placas rectangulares en el lomo, como fichas ordenadas en filas y columnas** (sin letras), que brillan cian; sale del agua del sótano entre estanterías.
- **El Dragón del Faro:** dragón marino negro y violeta, con alas como velas rotas, el cuerpo hecho de olas y relámpagos, enroscado en el faro; ojos como lámparas cian.
- **El Campeón Eterno:** guerrero con armadura antigua y capa gastada, sin cara visible (dentro del casco solo hay luz y engranajes): un juego perfecto que aprende.
- **El Grifo de los Registros:** grifo de plumas blancas y cuerpo de león dorado, con un monóculo y páginas de libro entre las plumas de las alas.
- **La Orca de los Mensajes:** criatura marina enorme que traga palomas mensajeras en vuelo; boca llena de sobres.
- **El Hipocampo de las Vidrieras:** caballito de mar del tamaño de un caballo, de vidrio de colores, que se refleja deformado en las vidrieras.

**El mapa del Puerto:** *«Mapa ilustrado de fantasía, estilo pergamino como el de la referencia, del Puerto de los Mensajeros, de noche, con auroras violetas: abajo a la izquierda, un sendero de la costa con sobres en los arbustos; muelles de madera con cajones y grúas; una roca con algas en la boca del puerto; galpones de un astillero con cascos de barcos; en el centro, una torre alta con una campana y tubos de bronce; una fonda; una escalera que baja a galerías de piedra bajo la torre; a la derecha, en la punta del muelle más largo, un faro alto; una plaza con una fuente en forma de sello de lacre y cuatro caminos (una arena, una fortaleza de piedra clara, un palomar, una calle de vidrieras). Sin texto ni carteles.»* (los nombres los pone la plataforma, como en la Ciudadela).

---

## 6. Lo que decidió el docente (2026-10-11)

1. **Iara** es la compañera y reemplaza a Kira en los ejemplos; **Bron pasa a Nilo**. Solo hacía falta crear los personajes.
2. **El bolso** es el objeto que cambia (Roto → Remendado → Morral del Correo Mayor).
3. **El Faro** es el lugar por el que llega Nilo y el último de la historia, y **los dos envíos «para quien llegue»** lo atan con Zed y con Java («de 10 esa vinculación»).
4. Se renombran **el Bastión de Laravel** y **la Orca de los Mensajes** (los nombres se pueden cambiar si no alteran nada). **La Senda de Laravel se trabaja al último.**
5. **La tienda del Puerto** es el puesto de Fermín, en la Bodega.
