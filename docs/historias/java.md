# Java · El arco de Zed (borrador 1, a revisar)

Nivel 1 y 2 del método de [../JUEGO.md](../JUEGO.md) § 10: **el arco** y **los capítulos** (un párrafo corto por nodo). La planilla de continuidad y las micro-misiones se escriben **después de que el docente apruebe esto**, como en Python ([python.md](python.md)).

Personajes y aspecto: [PERSONAJES.md](PERSONAJES.md). El contenido técnico de cada nodo **no cambia**: cambia la historia que lo envuelve y el corte en micro-misiones. Las crónicas actuales del curso ya son buenas y se conservan casi enteras (el lugar, los aduaneros, la Academia, los Archivos, la Bóveda, el Palacio): se reescriben para que las viva **Zed**, en tercera persona, como pasó con Mia.

Antes de seguir hay **cuatro decisiones** que son del docente (§ 3).

---

## 1. El arco

**Zed** es un ladrón de techos del **Puerto de los Mensajeros**: 18 años, pelo blanco plateado, un visor rojo y una ganzúa que abre cualquier cerradura del Puerto. Su regla es la contraria a la del Imperio: **«Siempre hay otra puerta.»**

Una noche roba de un barco un paquete sin remitente. Adentro hay una **llave de plomo y vidrios de colores** con una etiqueta: *«para quien llegue»*. Cuando la toca, un vitral del depósito se enciende como un portal, y Zed despierta del otro lado: frente a la muralla del **Imperio de las Clases**, en la fila de la **Aduana del Compilador**, con la llave en la mano y sin ningún papel.

**Lo que busca:**
- Al principio, **colarse** y **volver**: el portal se apagó y su ganzúa no abre nada en el Imperio (acá las cerraduras se abren con **tipos** y **contratos**, no con trucos).
- Desde que lo atrapan, **saber qué abre la llave**. La llave no entra en ninguna cerradura del Imperio, pero en cada distrito aparecen marcas del mismo vitral: alguien pasó por acá, hace mucho, y dejó cosas «para quien llegue».

**El peligro del Imperio:** las mismas criaturas de todo el Mundo del Código, con la forma que toman en Java:
- **slimes** por la sintaxis (`';' expected`);
- **goblins** por los tipos que no encajan;
- **esqueletos** por los nombres que no existen (`cannot find symbol`);
- **orcos** por los índices fuera de rango;
- **trolls** por las referencias y el `null`;
- **ogros** por la lógica (y el `==` entre textos).

**Cómo cambia:** de **buscar atajos** a **diseñar bien**. Zed no deja de ser pícaro: descubre que la mejor forma de abrir una puerta es entender cómo está hecha, y que una regla clara (un tipo, un contrato, una restricción) es lo que hace que una puerta sea **confiable**. El cambio se ve en su ganzúa:
- **al llegar**, la ganzúa no le sirve para nada;
- **en la rama 2** (interfaces), Kaffa le enseña que en el Imperio las puertas se abren con **contratos**, y la ganzúa empieza a cambiar de forma: le crecen dientes de llave;
- **al final**, la ganzúa es una **llave maestra** que él mismo diseñó.

**Los cinco actos**, uno por rama, siempre hacia el centro de la capital:

| Acto | Rama | Lugar | Qué aprende Zed (como persona) | Jefe |
|---|---|---|---|---|
| I | R01 Fundamentos | **La Aduana del Compilador**, en la muralla | Que **declarar** no es rendirse: es que no haya sorpresas | **El Centinela de la Aduana** |
| II | R02 Objetos | **La Academia de los Moldes** | Que un objeto **cuida lo suyo** (él, que abría cofres ajenos) | **La Quimera de las Mil Herencias** |
| III | R03 Colecciones y errores | **Los Archivos Imperiales** | Que **los errores se escuchan**: no se esconden ni se esquivan | **El Espectro Nulo**, que borra los registros del viajero |
| IV | R04 Bases de datos | **La Bóveda Imperial** | Que algunas cosas pasan **enteras o nada** | **El Liche de las Tablas Huérfanas** |
| V | R05 Ventanas | **El Palacio de las Ventanas**, en la cima | Que se construye **para otros**: una ventana la usa cualquiera | **El Dragón del Imperio** |

**El misterio:** en cada distrito, Zed encuentra un rastro del mismo viajero:
- en la Aduana, un registro viejísimo de alguien que **declaró una sola cosa**: «un vitral»;
- en la Academia, un molde que nadie sabe usar, con la firma del vitral;
- en los Archivos, la ficha del viajero, que el Espectro Nulo convierte en `null`;
- en la Bóveda, el pago del viajero, una transacción que nunca terminó: pagó con un vitral para la ventana más alta del Palacio.

**El final:** Zed vence al Dragón y sube a la torre del Palacio. Hay una ventana de vitral que nunca se abrió. **La llave entra.** El vitral se enciende y muestra, por un instante, un balcón con cuatro portales: una espiral, un engranaje, **un vitral** y un arco de fuego. En el marco está grabado *«para quien llegue»*. Kaffa le cuenta lo que sabe (su pieza del portal):

> «Trató de explicarme qué estaba construyendo y no pude ponerlo en ninguna clase. Es lo único que nunca supe ordenar: algo que no es de ningún lugar, porque es de todos.»

Zed no vuelve al Puerto todavía. Desde la Encrucijada de los Denarios salen las Sendas, y el vitral le mostró que el camino sigue.

**La compañía en el Imperio:**
- **Zed.**
- **Gheco**, que da las pistas (aparece sobre el hombro de Zed en la Aduana, sin explicar de dónde salió).
- **Nadia** (nueva), la aduanera que lo atrapa en la Clase 0. Es joven, estricta y cumple cada regla; lo vigila «hasta que aprenda», y termina siendo su compañera. Es el contrapunto de Zed: ella pregunta **«¿qué dice el reglamento?»**, él **«¿y si probamos por acá?»**. Los dos tienen razón a medias.
- **Kira, Mia y Bron no viajan con él.** Solo se los anticipa: en los Archivos hay una ficha recién llegada del Valle sobre «una aprendiz de maga que encontró notas con un vitral», y en la Bóveda alguien comenta que una espadachina bajó hacia las Forjas.

**Personajes del Imperio:**
- **Kaffa:** el Arquitecto Imperial, el mentor.
- **Nadia:** la aduanera, compañera de Zed.
- **El Escriba Jefe de la Aduana**, **el instructor de la Academia** y **el Archivista Mayor**: secundarios que ya están en las crónicas.
- **La Oráculo de las Tablas:** en la Bóveda.
- **El Tribunal Imperial:** en el examen final.

---

## 2. Los capítulos

Formato: **lugar** · qué pasa · lo que **consigue** (carta del grimorio o ítem) · el **gancho** al siguiente. Se apoyan en las crónicas que ya tiene el curso.

### Clase 0 · Hola, Java — *El depósito del Puerto y la fila de la Aduana*
Zed roba el paquete, toca la llave y cruza el portal. En la fila de la Aduana, Nadia le pide sus papeles; él intenta colarse por una ventana y la Aduana lo frena: **no deja pasar nada que no esté declarado**. Kaffa lo mira y, en lugar de echarlo, le da una tarea: escribir su primer programa.
- **Consigue:** las primeras cartas (`main`, `System.out.println`, compilar y ejecutar) y la **Llave del Vitral** (ítem de historia).
- **Gancho:** Kaffa: «Pasás la Aduana como todos. Declarando.»

### Acto I — La Aduana del Compilador (R01)

**R01-N01 · Variables, tipos y conversiones** — *La balanza de los cajones.* Zed quiere meter de contrabando «un poco de todo» en un cajón. La Aduana no lo deja: cada cajón tiene **tipo**. Consigue: cartas `int`, `double`, `String`, `boolean`, casteo. Gancho: dos guardias discuten una cuenta.

**R01-N02 · Operadores y expresiones** — *El patio de la Aduana.* Los guardias calculan distinto el peaje de una caravana. Zed se da cuenta de que el orden de las operaciones decide quién paga de más. Consigue: cartas operadores, precedencia, `%`, `++`. Gancho: la oficina de sellos está tapada de nombres mal escritos.

**R01-N03 · Textos: String, equals y printf** — *La oficina de sellos.* Zed «falsifica» un sello que dice lo mismo que el original… y la Aduana lo rechaza: **dos textos iguales no siempre son el mismo texto** (`==` contra `equals`). Primer ogro. Consigue: cartas `equals`, métodos de `String`, `printf`. Gancho: el aduanero empieza a hacer preguntas.

**R01-N04 · Leer del teclado: Scanner, Math y Random** — *La ventanilla.* Nadia lo interroga con `Scanner`; Zed contesta «muchos» donde va un número y el programa explota. Ahora él tiene que escribir el interrogatorio. Consigue: cartas `Scanner`, `Math`, `Random`. Gancho: tres portones para tres tipos de viajeros.

**R01-N05 · Decisiones: if y switch** — *Los tres portones.* Zed escribe el guardia que manda a cada viajero a su portón. Consigue: cartas `if/else`, `switch`, operadores lógicos. Gancho: al atardecer hay que contar todo lo que entró.

**R01-N06 · Bucles: while, do y for** — *El cierre de la Aduana.* Contar carro por carro. Zed escribe un bucle que no termina y la Aduana queda trabada toda la noche. Consigue: cartas `while`, `do`, `for`, `break`. Gancho: en el depósito, un estante numerado y un mapa en cuadrículas.

**R01-N07 · Arrays y matrices** — *El depósito.* Estantes del 0 al 9 y un mapa de la frontera. Zed busca el registro más viejo y, en el último estante, encuentra la **primera marca del vitral**: un viajero que declaró una sola cosa, «un vitral». Consigue: cartas arrays, matrices, el orco del último índice. Gancho: el reglamento de mil páginas.

**R01-N08 · Métodos: dividir el trabajo** — *Los libritos de los aduaneros.* Zed entiende que nadie lee el reglamento entero: cada aduanero tiene su método. Consigue: cartas métodos, parámetros, `return`, sobrecarga. Gancho: al fondo del último pasillo, el Centinela.

**R01-N09 · Jefe: el Centinela de la Aduana** — *El trono de piedra.* Una armadura vacía que aprueba o rechaza a cada viajero. Zed intenta engañarlo y no puede: lo vence con **orden**, partiendo el problema en métodos. Consigue: el ítem raro, **el Sello de Entrada** (ya no es un colado: está declarado) y la ganzúa que empieza a cambiar. Gancho: Kaffa: «Ahora aprendé a hacer moldes.»

### Acto II — La Academia de los Moldes (R02)

**R02-N01 · Clases y objetos** — *Los talleres de moldes.* Zed hace su primer molde, `Viajero`, y deja de guardar datos en tres arrays sueltos. Consigue: cartas clase, objeto, atributos y métodos. Gancho: un soldado sale del molde sin espada.

**R02-N02 · Constructores, this y sobrecarga** — *La palanca del molde.* Consigue: cartas constructor, `this`, sobrecarga. Gancho: el cofre de la tesorería está abierto.

**R02-N03 · Encapsulamiento y miembros static** — *La tesorería.* El cofre está a la vista y Zed, por costumbre, mete la mano… y escribe «-500» en la etiqueta. Por primera vez **le toca arreglar lo que rompió**: encapsular para que nadie (ni él) deje el cofre en negativo. Es el cambio del acto. Consigue: cartas `private`, getters y setters, `static`. Gancho: dos tarjetas que señalan el mismo escudo.

**R02-N04 · Referencias, null y equals** — *El escudo abollado.* El primer troll. Consigue: cartas referencia, `null`, `equals`/`hashCode`. Gancho: un molde viejo con la palabra «Personaje».

**R02-N05 · Herencia: extends y super** — *El ala oeste.* Consigue: cartas `extends`, `super`, `@Override`. Gancho: el instructor grita «¡Ataquen!».

**R02-N06 · Polimorfismo y clases abstractas** — *El patio de armas.* Consigue: cartas polimorfismo, `abstract`. Gancho: la sala de los pactos.

**R02-N07 · Interfaces: contratos** — *La sala de los pactos.* Zed descubre por qué su ganzúa no sirve: en el Imperio **las puertas se abren con contratos**. Firma su primera interfaz y la ganzúa **echa dientes de llave**. Consigue: cartas `interface`, `implements`, `Comparable`. Gancho: un aprendiz quiere que el caballero herede de todo.

**R02-N08 · Composición, agregación y delegación** — *El taller de armaduras.* Consigue: cartas composición, agregación, delegación. Gancho: la pizarra con «arquero», «ARQERO» y «ARQUERO».

**R02-N09 · enum y record** — *El archivo de la Academia.* Consigue: cartas `enum`, `record`. Gancho: Kaffa desenrolla un plano.

**R02-N10 · Diagramas UML** — *La biblioteca de la Academia.* En los planos de Kaffa hay un molde que nadie supo completar, firmado con el vitral. Consigue: cartas clase, asociación, herencia en UML. Gancho: algo ruge en el sótano.

**R02-N11 · Jefe: la Quimera de las Mil Herencias** — *El sótano.* Se la vence **modelándola bien**. Consigue: el ítem raro, **los Guantes del Artesano**, y el título de **aprendiz de la Academia**. Gancho: los Archivos guardan el registro de todos los que cruzaron.

### Acto III — Los Archivos Imperiales (R03)

**R03-N01 · Paquetes, import y archivos .jar** — *Las salas de los Archivos.* Consigue: cartas `package`, `import`, `jar`. Gancho: un estante de 10 lugares con 14 pergaminos.

**R03-N02 · ArrayList y genéricos** — *El ala norte.* Consigue: cartas `ArrayList`, genéricos. Gancho: las fichas del ala sur.

**R03-N03 · Mapas y conjuntos: HashMap y HashSet** — *El ala sur.* Zed busca la ficha del viajero por su clave, «el Vidriero»… y la ficha existe, pero dice `null`. Consigue: cartas `HashMap`, `HashSet`. Gancho: esa noche, el edificio entero se apaga.

**R03-N04 · Excepciones** — *Las campanas.* Kaffa instala campanas; Zed, que antes esquivaba cualquier alarma, aprende a **escucharlas**: es el cambio del acto. Consigue: cartas `try/catch`, `throw`, excepciones propias y el **Amuleto de la Campana** (ítem: segunda vida en las expediciones, como el del Valle). Gancho: el archivista jefe se cansa de dar instrucciones largas.

**R03-N05 · Lambdas, clases anónimas y referencias a métodos** — *La tarjetita en la puerta.* Consigue: cartas lambda, `Comparator`, referencias a métodos. Gancho: el Tribunal de las Pruebas.

**R03-N06 · Pruebas con JUnit** — *El Tribunal de las Pruebas.* Consigue: cartas `@Test`, `assertEquals`. Gancho: la escriba del diario.

**R03-N07 · Depuración, logging y Javadoc** — *El diario de los errores.* Siguiendo el diario, Zed descubre quién borra los registros del viajero. Consigue: cartas depurador, `Logger`, Javadoc. Gancho: la sala donde los pergaminos desaparecen.

**R03-N08 · Jefe: el Espectro Nulo** — *La sala vacía.* Se lo vence diseñando para que el `null` no tenga dónde esconderse. La ficha del viajero vuelve entera: **pagó en la Bóveda** con algo que nadie supo tasar. Consigue: el ítem épico, **la Linterna del Espectro**. Gancho: la escalera de piedra que baja a la Bóveda.

### Acto IV — La Bóveda Imperial (R04)

**R04-N01 · Archivos de texto, CSV y .properties** — *El primer piso.* Consigue: cartas lectura y escritura de archivos, CSV, `.properties`. Gancho: tablas talladas en la pared.

**R04-N02 · SQL: tablas, restricciones y ABM** — *El segundo piso.* Consigue: cartas `CREATE TABLE`, `PRIMARY KEY`, `INSERT`/`UPDATE`/`DELETE`. Gancho: la Oráculo de las Tablas.

**R04-N03 · SQL: consultas, JOIN y vistas** — *El tercer piso.* La Oráculo cruza tablas para Zed: el pago del viajero está registrado, pero **sin destino**. Consigue: cartas `SELECT`, `JOIN`, `GROUP BY`, vistas. Gancho: tablas que reaccionan solas.

**R04-N04 · SQL: funciones, procedimientos, triggers y roles** — *El cuarto piso.* Consigue: cartas funciones, procedimientos, triggers, roles. Gancho: el tubo de bronce.

**R04-N05 · JDBC: conectarse y consultar** — *El tubo de bronce.* Alguien esconde órdenes en un nombre: Zed, que de trampas sabe, la reconoce. Consigue: cartas `Connection`, `PreparedStatement`, inyección SQL. Gancho: los Mensajeros de cada tabla.

**R04-N06 · DAO: el ABM completo desde Java** — *Los Mensajeros.* Consigue: cartas DAO, ABM. Gancho: un tesorero pasa denarios de un cofre a otro y se apaga la antorcha.

**R04-N07 · Transacciones y CallableStatement** — *La tesorería de la Bóveda.* El pago del viajero era una transacción que **nunca terminó**: pagó con un vitral para la ventana más alta del Palacio, y el vitral nunca se colocó. Es el cambio del acto: enteras o nada. Consigue: cartas `commit`, `rollback`, `CallableStatement`. Gancho: las filas huérfanas alimentan a alguien.

**R04-N08 · Jefe: el Liche de las Tablas Huérfanas** — *El último piso.* Consigue: el ítem épico, **el Cofre Íntegro**, y el plano de la ventana más alta del Palacio. Gancho: arriba de todo, el Palacio de las Ventanas.

### Acto V — El Palacio de las Ventanas (R05)

**R05-N01 · La primera ventana: JFrame, componentes y eventos** — *La entrada del Palacio.* Consigue: cartas `JFrame`, `JButton`, `ActionListener`. Gancho: el salón de los vitrales.

**R05-N02 · Layouts: ordenar la ventana** — *El salón de los vitrales.* Hay vitrales de los Talleres de Tesela por todos lados (anticipo del curso de HTML y CSS). Consigue: cartas `BorderLayout`, `GridLayout`, `FlowLayout`. Gancho: la armería y sus formularios.

**R05-N03 · Componentes: listas, opciones y controles** — *La armería.* Consigue: cartas `JComboBox`, `JRadioButton`, `JCheckBox`. Gancho: la biblioteca del Palacio.

**R05-N04 · Tablas, árboles y diálogos** — *La biblioteca.* Consigue: cartas `JTable`, `TableModel`, `JTree`, `JOptionPane`. Gancho: el salón del trono, con muchas ventanas adentro.

**R05-N05 · MDI y menús** — *El salón del trono.* Consigue: cartas `JDesktopPane`, `JMenuBar`. Gancho: la ventana se congela.

**R05-N06 · SwingWorker: la base sin congelar la ventana** — *El registro de héroes.* Consigue: cartas `SwingWorker`, hilo de eventos. Gancho: el plano de cuatro salas.

**R05-N07 · MVC al estilo de la cátedra** — *La biblioteca, el plano entero.* Consigue: cartas modelo, vista, controlador, DAO. Gancho: el Tribunal se reúne en la cima.

**R05-N08 · Jefe final: el Dragón del Imperio** — *La cima del Palacio.* El examen de la Registración de Actas. Zed lo vence pieza por pieza. Consigue: el ítem épico, **la Llave Maestra** (su ganzúa, ya transformada) y su sello de arquitecto. Gancho: la ventana más alta.

**R05-N09 · La Encrucijada de los Denarios** — *La torre y la fuente.* La Llave del Vitral abre la ventana más alta: el vitral muestra el balcón de los cuatro portales y *«para quien llegue»*. Kaffa cuenta su pieza del portal. Nadia se queda en la Aduana, ahora como jefa de turno. Gheco señala las tres avenidas de las Sendas.

### Las Sendas (optativas)

- **S01 · Senda del Arcade Imperial** (Swing 2D): la sala de juegos de luces.
- **S02 · Senda de las Corrientes** (Java moderno): el río que corre rapidísimo.
- **S03 · Senda del Puerto de Spring** (servicios web): el puerto de barcos. Zed **vuelve al Puerto**, pero ahora a construir servicios, no a robarlos.

---

## 3. Decisiones que son del docente

**1. Cómo se comprueban solas las micro-misiones de Java.** El código Java del alumno no corre en el navegador; hoy corre con el **ejecutor local** (D85, *Herramientas → Ejecutor de Java*).
- **A. Ejecutor local desde la Clase 0 (lo que anda hoy, recomendado para empezar):** la Clase 0 incluye instalar el JDK y abrir el ejecutor, y desde ahí las micro-misiones se comprueban solas, igual que en Python. Contra: hay que instalar algo antes de la primera micro-misión, y quien prueba la Clase 0 gratis también.
- **B. Java en el navegador:** hay opciones (CheerpJ, TeaVM, un JDK en WebAssembly), pero pesan decenas de MB, y CheerpJ pide licencia paga para uso comercial. Habría que investigarlas antes de decidir (ya estaba anotado en JUEGO.md § 11).
- Mi recomendación: **empezar con A** y en paralelo investigar B; si B anda, se cambia sin tocar las micro-misiones.

**2. La rama 4 (SQL) y la rama 5 (Swing).**
- **SQL:** con el ejecutor local, las micro-misiones de SQL pedirían PostgreSQL instalado. Propongo correr el SQL de las micro-misiones **en el navegador con SQLite** (una base chiquita que viene armada, sin instalar nada), y dejar PostgreSQL para las prácticas que corrige el docente. Las diferencias de sintaxis son pocas en lo que se ve en micro-misiones (tablas, `SELECT`, `JOIN`).
- **Swing:** una ventana no se comprueba sola. Como en la Senda de la Arena de Python, las micro-misiones serían **la lógica** (el modelo de la tabla, los eventos como métodos, MVC sin ventana), y la ventana queda para las prácticas.

**3. Cuántas micro-misiones.** En Python fueron 5 o 6 por nodo. Java tiene **45 nodos** en el camino principal: con 5 por nodo serían unas 225. Propongo **3 o 4 por nodo** (unas 160): cada una sigue siendo una sola idea, pero los nodos de Java ya tienen mucha práctica que corrige el docente.

**4. Las crónicas actuales.** Hoy están escritas en segunda persona («Pasás la primera puerta…»). Propongo pasarlas a tercera persona con Zed, como se hizo con Mia, conservando los lugares y los secundarios.

---

## 4. Arreglos de continuidad respecto del curso actual

- **{heroe}** pasa a ser Zed en todo el curso (como Mia en Python).
- **R04-N07:** «pasando cien denarios del cofre de Kira al de Bron» pasa a «del cofre de Nadia al de Zed».
- **Ejemplos y prácticas** que usan a la compañía vieja (Kira, Mia, Bron) como personajes pasan a Zed, Nadia y gente del Imperio, con las salidas rehechas ejecutando el código, como en Python.
- **La bienvenida** (`story.course_intro`), **el cierre** (`story.course_completed`) y la ficha de Kaffa en el diccionario se reescriben con Zed, la llave y la ventana.
- **El mapa del Imperio** para las expediciones: hay que generarlo (la Aduana en la muralla, la Academia, los Archivos, la Bóveda bajo los Archivos, el Palacio en la cima, la Encrucijada y las tres avenidas de las Sendas).

## 5. Personajes nuevos (para generar)

**Nadia**, la aduanera (compañera de Zed). No es protagonista: cuerpo entero y retrato circular, sin variantes.
- **Quién es:** aduanera de la Aduana del Compilador, 19 años, la más joven del turno y la más estricta.
- **Personalidad:** prolija, seria, cumple cada regla y se la sabe de memoria; se ríe muy poco, y cuando lo hace es por algo que hizo Zed. Pregunta «¿qué dice el reglamento?».
- **Aspecto:**
  - piel morena, ojos oscuros y atentos, **pelo negro recogido en un rodete tirante**;
  - **uniforme de la Aduana**: chaqueta azul oscuro con botones de bronce y vivos dorados, cuello alto, guantes blancos;
  - un **sello de bronce** colgado del cinturón y una **libreta de registros** siempre abierta;
  - el dorado de las catedrales del Imperio.
- **Frase:** «Lo que no está declarado, no existe.»

**También tienen que estar en PERSONAJES.md** (algunos ya aparecen en las crónicas, sin ficha): **el Escriba Jefe de la Aduana**, **el instructor de la Academia**, **el Archivista Mayor**, **la Oráculo de las Tablas** y los jefes (**el Centinela**, **la Quimera**, **el Espectro Nulo**, **el Liche**, **el Dragón del Imperio**). Se fichan cuando se aprueben los capítulos, y solo los que hablen con Zed llevan imagen (la regla de Python).
