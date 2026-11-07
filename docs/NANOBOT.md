# D122 · El nanobot del héroe (a revisar, sin programar)

Idea del docente, conversada el 2026-11-06. **Estado:** diseño para discutir. No se programa ninguna fase sin su OK.

**La idea en una frase:** cada héroe recibe un nanobot vacío que despierta con lo que el alumno aprende. Después, el alumno lo programa para que explore un mapa, junte recursos y pelee.

## 1. Lo que ya quedó decidido

| Tema | Decisión |
|---|---|
| Cuántos | **Un solo bot**, nunca un enjambre. Lo «neuronal» es que ese bot evoluciona. |
| Quién evoluciona | El bot: atributos, ítems, armas y mejoras. El héroe sigue siendo su dueño, con la misma historia y las mismas escenas. |
| Imagen | **La montura pasa a ser el nanobot.** Se aprovechan sus 5 niveles y se adapta lo que falte. |
| Por lenguaje | **Un bot fijo por lenguaje**, porque se programa distinto en cada uno. |
| Inglés y HTML | **Bot automático**, que no se programa: explora y pelea con métodos fijos. Los bots programables heredan esa misma base. |
| Mejoras | Mismo flujo que hoy con el héroe (oro y nivel de jugador); lo aprendido da capacidades. Más adelante, **lo que se equipa se ve en el bot**. |
| Guía | **El Profe** se lo entrega y guía el lado del juego. |
| Java | Sin Ejecutor en el juego: un simulador propio. El curso sigue usando Java real. |
| Exploración | Dos formas (§ 3 bis): **programada**, cuando el alumno la manda, 30 minutos como mucho, y se ve al volver; y **a mano**, en vivo, salto por salto. |
| Mapa | **Mosaico** limitado en ancho y alto, para explorar y para batallas simples. |
| Movimiento | **8 direcciones.** Personajes, monstruos y mascotas llevan su hoja de lados, por coherencia. |
| Cartas | **Las cartas del Grimorio habilitan las piezas del bot** (§ 5). Sin la micro-misión, ese bot no tiene esa pieza. |
| Vista | Repetición **de cerca, con la cámara siguiendo al bot**. Se le da una oportunidad antes de decidir si se recorta. |
| Orden | Despertar → atributos en el bot → mapa en Python → prueba con alumnos → estructuras. |
| A futuro | Mezclar cartas de distintos lenguajes (§ 9). Se tiene presente, no se hace ahora. |

Las referencias que mostró el docente (dos tácticos por casillas) son de género. El mapa, el arte y las reglas son propios.

## 2. El despertar

| Etapa | Cuándo | Qué cambia en el bot |
|---|---|---|
| 0. Vacío | Al entrar al curso, se lo da el Profe | Apagado y en gris |
| 1. Corazón | Al repartir los atributos («Tomá el control») | Le late una luz en el pecho; ojos cerrados y quieto |
| 2. Ojos | Aprende a imprimir | Abre los ojos, parpadea y mira para los costados; puede «hablar» |
| 3. Oídos | Aprende a leer datos | Recibe órdenes |
| 4. Criterio | Aprende condicionales | Interpreta órdenes y decide, pero todavía sin moverse |
| 5. Movimiento | Aprende bucles | **Se mueve y se abren las exploraciones** |

Lo apagado, la luz y los ojos se hacen con CSS sobre la imagen, con la posición guardada por imagen. Se retoca con Stitch solo lo que no quede bien.

### Una corrección a lo que dije antes
Yo había dicho que las etapas salían directo de los temas de [cursos/temas.md](../cursos/temas.md). **Revisé el código y no alcanza**, por tres motivos:
- Las cartas del Grimorio salen de cada micro-misión (`card_title`), con título libre.
- Los temas están marcados por nodo, no por micro-misión.
- Hay huecos: JavaScript no tiene `prog.entrada` y la demostración de C# no llega a `prog.bucles`.

**Propuesta:** marcar a mano qué micro-misión despierta cada capacidad, curso por curso (por ejemplo, `capacidad: ojos`). Así el momento es exacto y hasta se le puede poner una escena. En JavaScript, «leer datos» sería su equivalente, como un `prompt`. C# recién se mueve cuando el curso llegue a bucles.

## 3. Cómo se programa, y por qué nada corre mientras el alumno no está

Las aclaraciones del docente simplifican lo que yo veía como el mayor problema. Como la exploración no se ve en vivo, **se calcula toda de una vez, al mandarla**:

1. El alumno escribe el programa en el editor de siempre, con el ejecutor de su lenguaje, y lo prueba gratis en **el Patio**, un mapa de práctica sin premios.
2. Al mandarlo, su programa corre en **su navegador**, contra el mapa de esa expedición. Tarda segundos y sale una **lista de órdenes**.
3. El navegador manda solo esa lista. **El servidor nunca recibe ni ejecuta código**: repite las órdenes con la misma semilla y decide el resultado.
4. El bot «está afuera» 5, 15 o 30 minutos, igual que hoy. Sin cron: se resuelve cuando el alumno vuelve a mirar.
5. Al volver, ve **la repetición** en el mosaico: por dónde fue, qué juntó y cómo peleó.

Esto cambia lo que dije antes: tampoco hace falta guardar reglas para «mientras no estás». La **carta activa** es el mismo programa corrido varias vueltas, todas calculadas al salir.

### El programa del alumno
Imprime órdenes y lee respuestas, nada más. Por eso vale para cualquier lenguaje:

```python
while True:
    print("MIRAR N")
    veo = input()          # "libre", "pared", "recurso" o "enemigo"
    if veo == "recurso":
        print("N")
        print("JUNTAR")
    elif veo == "enemigo":
        print("ATACAR N")
    else:
        print("E")
```

| Órdenes | Para qué |
|---|---|
| `N`, `NE`, `E`, `SE`, `S`, `SO`, `O`, `NO` | Moverse (gasta energía) |
| `MIRAR <dirección>`, `VIDA`, `ENERGIA` | Preguntar: son las únicas que contestan |
| `JUNTAR`, `ATACAR <dirección>`, `DEFENDER`, `HUIR`, `POCION`, `VOLVER` | Actuar |

Un principiante puede escribir solo `for i in range(5): print("N")`. Funciona igual, pero el bot avanza a ciegas.

### El punto técnico que hay que probar
Los ejecutores actuales reciben toda la entrada antes de arrancar; no pueden esperar la respuesta del mapa en medio del programa. **Propuesta:** correrlo varias veces, y en cada una pasarle todas las respuestas que ya tuvo, hasta que pida una nueva. Las variables y el `while True` funcionan normalmente, sin que el alumno tenga que saber nada de esto. Hay tres riesgos:

| Riesgo | Qué hacer |
|---|---|
| Cuando se acaba la entrada, un `scanf` en C no corta: el `while` sigue para siempre | El ejecutor del juego corta el programa al pedir más de lo que hay. Hay que adaptarlo en cada lenguaje. |
| Tiempo: decenas de corridas en WebAssembly | Medirlo. C, C++ y C# compilan una vez y repiten. PHP es el que más me preocupa. |
| `random` o la hora hacen que cada corrida dé distinto | Semilla fija en el juego, y si aun así difiere, un mensaje claro. |

**Primero, un prototipo en Python** por fuera de la plataforma. Si esto no anda, el plan B es correr una vez por turno y guardar la memoria con una orden, algo más incómodo para el alumno.

### Trampas
Alguien con conocimientos podría falsear la lista de órdenes o espiar el mapa desde el navegador. El servidor valida cada orden y que el bot tenga esa capacidad, y el botín tiene el mismo tope que hoy. Lo máximo que se gana es una ruta perfecta, y solo da premios de juego: **nunca monedas del curso ni aperturas**.

## 3 bis. Jugar a mano, comandos y tutoriales (pedido del docente, 2026-11-06)

### Comandos del Grimorio
Vida, energía y bonos se usan **desde el código**. Para los bots programables **nada se usa solo**: si el programa no toma la poción, el bot no la toma. Es la forma de obligar a usar lo aprendido. Solo los bots de HTML e inglés lo hacen automático.

```python
if vida() < 10 and pociones() > 0:
    tomar_pocion()
```

- **Los comandos son cartas del Grimorio:** `vida()`, `energia()`, `pociones()`, `celulas()`, `bonos()`, `mirar()`, `mover()`, `atacar()`, `tomar_pocion()`, `recargar()`, `usar_bono()`, `radar()` y los demás salen con su pieza (§ 5). En la plataforma, el Grimorio sumaría una sección «Comandos del bot».
- **Llevan paréntesis:** en todos los lenguajes tiene que preguntar en ese momento, y una variable no se actualizaría sola. Si alguien escribe `if vida < 10`, el prototipo le explica el error.
- **Devuelven datos reales de cada carta:** `radar()` es una lista, `donde()` una tupla y `analizar()` un diccionario.
- **Por debajo son `print` e `input`:** hay un ejemplo que lo muestra. Cada lenguaje llevará su propia versión de los comandos; solo está hecha la de Python.
- **Solo en el juego:** el curso sigue igual, sin desafíos con comandos falsos.

### A mano
Click en la casilla vecina y **el bot salta como una ficha**, sin saber qué hay: la niebla solo deja ver las casillas que ya pisó o miró.

- **Monstruo:** el bot queda frente a él y no se puede saltar hasta resolverlo. El alumno programa la pelea en ese momento y la ejecuta: puede curarse, proponer un `while` o huir, y puede salir mal.
- **Cofre:** se abre con código en ese momento, si tiene la carta.
- **Recursos:** se juntan solos al caer.
- **Errores:** no cortan la exploración; se corrige y se vuelve a ejecutar.
- **Espiar cuesta:** `mirar()` y `analizar()` gastan 1 de energía y `radar()` 2, para no perder la sorpresa.
- **`input()` le pregunta al jugador** con una ventanita.

**Cómo cuenta (decidido para probar, 2026-11-06):** gasta una de las 6 expediciones del día, sin espera porque se está jugando, con los mismos topes de premio. Salir no devuelve la expedición, para que no se pueda reintentar el mapa. Para que la niebla no se pueda espiar desde el navegador, el servidor manda solo lo revelado; eso significa un pedido al servidor por salto. Todo esto todavía **no está hecho ni probado en un servidor**: el prototipo calcula todo en el navegador.

### Del mapa del mundo al mosaico
Se sigue usando **el mapa de cada mundo con sus puntos**, el de las expediciones de hoy (`config('game.…places')`: lugar, posición, nodo, nivel y criaturas). El alumno avanza por los puntos, y cada uno se abre igual que ahora: al completar su nodo o, si viene de otro curso, al llegar a su nivel de jugador.

Tocar un punto abre su mosaico. Las criaturas y el nivel salen de ese lugar, así que el mapa se pone más difícil a medida que se avanza. **Propuesta:** los tutoriales son los primeros puntos. Hay que dibujar en 8 direcciones todas las criaturas que aparecen en los lugares de cada mundo.

### Tocar para ver
Tocar un monstruo, cofre, árbol, roca, agua o recurso **que ya se vio** abre su ficha. El monstruo muestra vida, cuánto pega, cuántos son y cuánto pega el bot, para calcular antes de entrar. Una casilla vecina con niebla o vacía salta directo. Lo que no se vio no muestra nada. Por ahora los grupos son de 1 enemigo; varios en un grupo queda para más adelante, porque hoy la pelea es de a uno.

### Tutoriales: una serie de mapas chiquitos
Idea del docente: **cada mapa enseña un solo detalle** y orienta qué escribir según lo que el Grimorio ya tiene. Son de 3 × 3, guiados por pasos, y usan código real de lo aprendido. No dan premios grandes.

| Mapa | Enseña | Código que escribe | Hecho en el prototipo |
|---|---|---|---|
| Moverse | Saltar con click, niebla, paredes, energía, recursos | Ninguno | Sí |
| El cofre | Abrir cofres | `print(caja)`, `clave = input()`, `abrir(clave)` | Sí |
| La pelea | Tocar para ver datos, calcular, atacar | `for` o `while` con `atacar()` | Sí |
| Curarse | Las pociones no se usan solas | `if vida() < 20: tomar_pocion()` | Sí |
| Defenderse | El escudo, con su carta | `defender()` y `atacar()` en un `while` | Sí |
| Energía, Radar, Mapa y otros | Una pieza cada uno | Según su carta | Falta |

**Propuesta:**
- **Cada mapa se abre con su carta.** Los primeros aparecen juntos al llegar a `while`, porque el bot recién ahí se mueve (§ 2). Los demás aparecen cuando el alumno consigue esa pieza, con un aviso: «Tenés una pieza nueva, probala».
- **Son los primeros puntos del mapa del mundo** y no gastan expediciones del día.
- **Las cerraduras van por nivel**, según la carta: con `print` e `input`, copiar la clave; con `Listas`, sumar una pista.
- **Premio chico, una sola vez** (aprobado): un poco de oro y una poción al terminar la serie, por `Ledger` e `Inventory`.
- **Nadie llega a un mapa real sin saber qué escribir** (pedido del docente): los cuatro primeros (moverse, cofre, pelea, curarse) son obligatorios antes del primer punto real.
- **El editor nunca queda en blanco en un mapa real:** ante un cofre o un monstruo aparece un código sugerido, que se puede cambiar (ya está en el prototipo). Falta sumar las cartas del Grimorio al lado del editor, para tocarlas e insertar el comando.

## 4. Cómo aprende a defenderse

El docente pidió ayuda con esto. Propuesta: **sabe pelear desde el principio, pero cuanto más aprende, mejor decide**.

| Sabe | Cómo pelea |
|---|---|
| Solo moverse | Si tropieza con algo, ataca solo hasta que uno caiga (como el combate de hoy) |
| Condicionales | Decide: `si vida < 30, HUIR` o `POCION` |
| Bucles | Sostiene una estrategia: ataca mientras convenga, defiende mientras se cura |
| Registros y arrays | Anota a cada enemigo: qué es, cuánto pega y cuánta vida le queda |
| Funciones | Guarda una rutina de combate para reutilizarla |

Los golpes, críticos y esquivas usan las fórmulas de `Expeditions::simulate`, con los mismos cuatro atributos. Primera versión: los monstruos están quietos en su casilla y la pelea es entre casillas vecinas, con las barras de siempre. Rodear o posicionarse queda para más adelante.

### Pociones, botín y tamaño del mapa (propuesta, a revisar)

Consulta del docente: cómo se resuelven las pociones de vida y de energía, y que la duración de la exploración cambie el mapa.

**De dónde salen las pociones:**
- **Se llevan del inventario.** Son las mismas de hoy: tienda, taller y botín. Salen de la mochila solo si el bot las toma; las que no usa siguen ahí.
- **Se encuentran en el mapa.** En una casilla, en un cofre o al caer un monstruo. Ocupan lugar en la carga: el bot puede tomarla ahora o guardarla, y una poción ocupa el lugar de un cristal.
- **Lo que sobra vuelve a casa,** con el mismo reparto del botín (entero, la mitad o nada, según cómo terminó).

**Energía:** hoy las pociones solo curan (`items.heal`). Propuesta: un solo ítem nuevo para todos los mundos, la **Célula de energía**, con una columna `energy`. Lleva una sola imagen y va bien con un bot. Las pociones temáticas de cada mundo siguen curando.

**Comandos:** `tomar_pocion()`, `recargar()`, `usar_bono()`, y las preguntas `pociones()`, `celulas()` y `bonos()`, porque el programa no puede adivinar lo que encontró en el camino. Ya están en el prototipo, con un **Bono de fuerza** de ensayo (+6 de daño por 3 golpes). Las pociones, las células y el bono se dibujan con íconos provisorios.

**Según la duración:**

| | Corta (5 min) | Media (15 min) | Larga (30 min) |
|---|---|---|---|
| Mapa | 8 × 8 | 10 × 10 | 12 × 12 |
| Energía del bot | 64 | 80 | 96 |
| Monstruos | 3 o 4 | 5 o 6 | 7 a 9 |
| Recursos | 6 | 8 | 10 |
| Cofres | 1 | 2 | 3 |
| Pociones que puede llevar | 2 | 3 | 4 |
| Oro en total (el de hoy) | 15 | 40 | 80 |

Todos los números son un primer tiro, sin balancear.

**Para darle más recorrido:**
- **Lejos es mejor y más peligroso:** cerca de la salida hay slimes y recursos comunes; en los bordes, monstruos fuertes y cofres mejores. La energía obliga a decidir hasta dónde ir.
- **Cada expedición tiene su mapa:** tipo y lugar de los monstruos salen de la semilla de esa expedición. El servidor lo repite igual, sin cron.

**Límites de economía:**
- El oro total no sube: se reparte por el mapa, siempre por `Ledger`.
- Los ítems, por `Inventory`.
- Se mantienen las 6 expediciones por día, las probabilidades de botín (20, 5 y 1 %) y el contador de mala suerte. Hay más monstruos, así que el botín se sortea **por expedición, no por monstruo**; si no, las largas darían mucho más que hoy.
- Solo premios de juego: nunca monedas del curso ni aperturas.

**Bots automáticos (HTML, inglés):** toman las pociones solos, como el combate de hoy. Los programables, nunca (§ 3 bis).

## 5. Las cartas habilitan piezas

Pedido del docente: el diseño usa **las cartas del Grimorio**. Cada carta que importa le da al bot una **pieza**, y la pieza suma órdenes. Sin superar esa micro-misión, ese bot no la tiene. El aprendizaje es incremental: la ayuda del editor muestra solo las órdenes que ya tiene.

| Carta (Python) | Micro-misión | Pieza | Qué suma |
|---|---|---|---|
| `print` | R00-N01-P1 | Voz | Dice lo que imprimís |
| `input` | R00-N01-P4 | Antena | `MIRAR`, `VIDA`, `ENERGIA` |
| `if / elif / else` | R01-N04-P1 | Criterio | `ATACAR`, `POCION`, `HUIR` |
| `while` | R01-N04-P2 | Motor | Moverse, `JUNTAR`, `VOLVER`: salen las exploraciones |
| `Listas` | R01-N05-P1 | Radar y mochila | `RADAR` (las 8 casillas de una vez) y carga 8 cosas en lugar de 3 |
| `Listas anidadas` | R01-N05-P7 | Mapa interno | `MAPA` (lo explorado, en filas y columnas) |
| `Tuplas` | R01-N05-P8 | GPS | `DONDE` (fila y columna) |
| `Diccionarios` | R01-N06-P1 | Escáner | `ANALIZAR <dirección>` (nombre, vida y ataque) |
| `try / except` | R02-N03-P1 | Escudo | `DEFENDER` |
| `Archivos` | R02-N03-P4 | Caja negra | `GUARDAR`, `RECORDAR`: de una exploración a la otra |

Falta decidir qué dan `Funciones` (rutinas guardadas), `deque` (lista de tareas) y `Clase y objeto`, que no están en el prototipo. Solo unas pocas cartas dan pieza: Python tiene 129 entre los tres módulos del tronco, y el resto sigue siendo de consulta.

### Reglas
- **Una marca en la micro-misión:** una línea `pieza: radar` en el `meta` del curso. El alumno tiene la pieza si superó esa micro-misión; se calcula en cada request y no se guarda aparte.
- **Vale para cursos que todavía crecen:** en JavaScript y C#, la pieza aparece cuando el curso suma la micro-misión y el alumno la supera. Si se marca una micro-misión ya superada, la pieza aparece sola.
- **El lenguaje no se prohíbe, solo se limita la pieza.** Un alumno puede usar listas antes de tiempo, porque no se puede ni conviene impedirlo. Lo que no tiene es la orden `RADAR`.
- **Orden sin pieza:** el bot avisa cuál le falta y qué micro-misión la da, y vuelve con todo lo que tenía. No se castiga. El servidor lo vuelve a comprobar.
- **Cada bot, sus cartas:** las piezas de un lenguaje no pasan al bot de otro (la mezcla queda para § 9).

### Lo que dejó la prueba
- **Los comandos hacen más lenta la exploración programada:** como preguntar es gratis, «Se cuida solo» tardó 25 s en 588 corridas. A mano no se nota: una pelea son unas 12 corridas, 0,3 s. **Idea sin probar:** en Python, el simulador podría ir dentro del Web Worker y contestar en el momento, en una sola corrida, sin repetir nada. Hay que probarlo antes de la fase 3 y ver si los otros ejecutores lo permiten.
- **El Radar también resuelve la lentitud:** el programa con 8 `MIRAR` por turno tardó 619 corridas y 12,7 s; el de `RADAR`, 69 corridas y 0,9 s. Son programas parecidos, no idénticos. Aprender listas se siente como una mejora real.
- **La brújula y el mapa no coinciden:** en pantalla, `NE` sube una fila y `SE` avanza una columna, pero `mapa()` y `donde()` hablan en filas y columnas. **Decidido:** quedan los rombos y se explica con un dibujo al entregar esas cartas. El click evita gran parte del problema, porque a mano no hace falta la brújula. Es el punto más confuso que encontré, sin probarlo con alumnos.
- **Falta el cerebro:** el grafo donde se encenderían las piezas sigue siendo una idea; en el prototipo son una fila de cartas.

## 6. Los bots y sus imágenes

**Propuesta de un bot por lenguaje (se puede cambiar):**

| Curso | Bot | Por qué | Retoque |
|---|---|---|---|
| Python | Serphira | Es del Valle | Partir de **la imagen ya armada**, no de un diseño nuevo (decisión del 2026-11-06) |
| C | PixelShell | Lava y patas de hierro, las Forjas | Poco |
| C++ | Titán | Elefante de metal | Poco |
| Java | Draco-Bit | Dragón de plata | Medio |
| PHP | Gran Apex | Montura de los mensajeros del Puerto | Medio |
| JavaScript | Voltio | Neón, va con la Feria | Medio |
| C# | Archivald | Búho con antiparras | Medio |
| Ensamblador | CopperPug | Cobre y orugas: el más máquina | Poco |

Las demás especies no se tiran: siguen en inglés y en la Enciclopedia. **Folio** (inglés) y **Vitral** (HTML) son los bots automáticos, aprobados por ahora (§ 10).

**El trabajo de arte, sin dibujar nada antes de tiempo:**
- **Retoque:** las 5 imágenes de cada bot, con su aire de robot.
- **8 direcciones:** una hoja por nivel de cada bot, o sea **40 hojas** en total. Para Python alcanzan 5.
- **Monstruos:** primero los del Valle. Muchos ya tienen hoja; hay que revisar los que falten.
- **Mosaicos:** un juego de casillas por mundo (pasto, piedra, agua, recurso).
- **Limitaciones:**
  - Las imágenes y las hojas tienen fondo, así que hay que **recortarlas**. Lo pruebo con un personaje antes de hacer todas.
  - Las hojas son de 8 poses fijas, sin ciclo de caminata. El bot **gira y se desliza** con un saltito. Animar los pasos multiplica el trabajo por 4 o más, y queda para después.
  - El límite diario de Stitch compite con las escenas de JS que faltan.

## 7. Cómo encaja con lo que ya hay

Menos cambios de los que parecía:
- **Un bot por héroe:** `Hero` ya es uno por alumno y curso, con atributos y equipo. El bot puede **vivir en esa misma fila**, sumando solo su nivel, sin copiar datos.
- **Monturas:** hoy `Mount` es una por jugador. Pasan a ser un nivel por bot, con los mismos precios y niveles mínimos, y el mismo efecto de acortar el viaje. Los Establos se vuelven **el Taller del bot**.
- **Expediciones:** se reutilizan el límite diario, las tres ofertas, los tiempos, el Reloj de Arena y el botín por `Ledger` e `Inventory`. Cambia lo que pasa adentro.
- **Mapas de otros cursos:** quien explora un mundo ajeno va con el bot de su curso y lo programa en ese lenguaje.
- **Ejecutores:** se usan los del navegador. Para Java, un intérprete propio de un subconjunto: variables, `if`, bucles, `Scanner`, `println`, métodos y arrays. Si encuentra algo que no sabe, avisa con un mensaje claro. **Es la pieza más cara del proyecto**, y por eso va después de la prueba.
- **Fuera de esto:** el avance del curso, las monedas, las aperturas y las correcciones no dependen del bot.

**Reinicio:** el docente ya avisó a los alumnos, pero con este diseño **quizá no haga falta borrar casi nada**. Los atributos y el equipo siguen sirviendo, y solo cambian las monturas. Se decide en la fase 2, con la lista exacta a la vista. En ningún caso se tocan el avance, las monedas del curso, la XP o los abonos.

## 8. Fases

Cada una termina con la prueba del docente, y la siguiente arranca solo con su OK.

| Fase | Qué incluye | Si sale mal |
|---|---|---|
| **0. Prototipo** | Python corrido varias veces (§ 3), recorte de una imagen y 8 direcciones en un mosaico de prueba. Fuera de la plataforma. | No se tocó nada |
| **1. Despertar** | Ficha del bot, las etapas de § 2 en Python y la entrega del Profe. Solo visual. | Se oculta |
| **2. Atributos en el bot** | Monturas a bots, el Taller, textos, exploraciones desde bucles. Las expediciones siguen automáticas. | Decisión de reinicio |
| **3. Mapa en Python** | Mapa del mundo con sus puntos, mosaicos, modo a mano, tutoriales, fichas, comandos y primeras piezas; editor, Patio, servidor, repetición y peleas de § 4. Lo automático sigue en los otros lenguajes. | Queda solo en Python |
| **4. Prueba con alumnos** | **Se frena acá.** Si no entusiasma, no se sigue. | — |
| **5. Evolución** | Más piezas, cerebro (§ 5), carta activa. Las primeras piezas entran con el mapa, en la fase 3. | — |
| **6. Otros lenguajes** | Uno a la vez, con el intérprete de Java al final. | — |

Es **ambicioso, pero se puede hacer**, porque la fase 4 frena antes de lo más caro. Al sumar cada bot, recorrer [ALTA-DE-CURSOS-Y-PERSONAJES.md](ALTA-DE-CURSOS-Y-PERSONAJES.md).

### Resultados de la fase 0 (2026-11-06)
Prototipo en [scripts/nanobot-prototipo/](../scripts/nanobot-prototipo/): el despertar, las 8 direcciones y el mapa programable en Python. Probado en Chrome.

| Pregunta | Resultado |
|---|---|
| ¿Anda correr el programa varias veces? | **Sí, en Python:** `while True` con `input()` y variables funcionan sin cambios. |
| ¿Cuánto tarda en Python? | Unos 10 a 20 ms por corrida. 107 corridas, 1,2 s; 499 corridas, entre 17 y 21 s, porque cada corrida repite las anteriores: un programa que pregunta mucho se hace lento. Más los segundos de carga de la primera vez. Falta probar en computadoras lentas. |
| ¿Se cortan los programas con error? | Sí: bucle sin salida, error de sintaxis o de ejecución, y `input()` sin preguntar antes, cada uno con su mensaje. |
| ¿Sirven las hojas para 8 direcciones? | **Sí.** Sobre fondo magenta, Stitch dio las 8 en el orden pedido y `recortar.py` las separa solo. |
| ¿Salen estados y evoluciones? | **Sí.** La hoja apagada se editó a partir de la prendida; también salieron los niveles 3 y 5. |
| ¿Salen los mosaicos? | **Sí**, para el Valle, las Forjas y el Puerto. Falta que el agua y la lava empalmen entre casillas. |

**La vista:** se sumó una cámara que sigue al bot, dos acercamientos, zoom en las peleas y un botón para ampliar el mapa. Las imágenes actuales son chicas (bot de 133 × 150, casillas de 233 de ancho): el arte definitivo tiene que recortarse más grande para que no se vea borroso de cerca.

**Sin probar:** C, C++, C#, PHP y JavaScript corridos varias veces; la validación en el servidor; alumnos reales. **Defectos a corregir en el arte definitivo:** la hoja del bot muestra la luz del pecho también de espaldas, y los monstruos se dibujaron sin sus hojas oficiales.

## 9. A mediano o largo plazo: mezclar lenguajes

El docente imagina combinar cartas: un iterable, una herencia de Java, algo de ensamblador. Como todos los lenguajes hablan el mismo idioma de órdenes y respuestas, el diseño no lo cierra: una carta guardada podría ser una rutina en otro lenguaje que su bot aprendió. Por ahora solo hay que **guardar cada carta con su lenguaje** y no atar las órdenes a ninguno.

## 10. Decisiones del 2026-11-06

1. **HTML, CSS e inglés tienen bot automático:** usa la misma base que los demás, pero no se programa. Se reutilizan las expediciones automáticas de hoy. Propuesta de imagen: Vitral (HTML) y Folio (inglés).
2. **Los bots de § 6 quedan aprobados.**
3. **Mejorar el bot sigue el flujo de hoy.** Que lo equipado se vea en el bot queda para más adelante.
4. **Fase 0 aprobada:** prototipo para ver el diseño del bot, los movimientos y los escenarios antes de codificar.
5. **Opinión sobre el prototipo:**
   - El bot tiene que parecerse a lo ya armado: Serphira ya se rehízo desde sus 5 imágenes (2026-11-06, a la espera del OK del docente). Forma y colores de cada nivel, más ojo-lente, juntas y luz en el pecho; sin bases, círculos ni pantallas. Hojas en Stitch, proyecto `16828689365976730624`: `a2811ac7…` (n1), `27e36026…` (n2), `90963805…` (n3), `767186423…` (n4), `171787da…` (n5).
   - **Cómo sale para los otros bots:** Stitch confunde derecha e izquierda y a veces agrega figuras, así que se piden 5 vistas (frente, 3/4 frente, perfil, 3/4 espalda, espalda) y se espejan las demás con `scripts/nanobot-prototipo/armar-serphira.py`, que dice qué figura va en cada dirección. Hay que mirar cada hoja antes de armarla. El bot apagado sale en gris del nivel 1, sin gastar cuota. Lo espejado invierte también lo asimétrico (la montura o una marca de un solo lado).
   - El mapa en rombos queda.
   - Se suman las cartas como piezas (§ 5).
   - Las órdenes se entienden, porque se aprenden de a poco.
   - La repetición convence a medias: se le da una oportunidad, más grande y más cerca.
6. **Respuestas del 2026-11-06:**
   - El modo a mano se prueba como está propuesto en § 3 bis.
   - Los tutoriales son una serie de mapas, uno por detalle (§ 3 bis).
   - Mapa en rombos, con un dibujo para explicar `mapa()` y `donde()`.
   - Se usa el mapa de cada mundo con sus puntos para avanzar.
   - Vitral y Folio quedan como bots automáticos, por ahora.
