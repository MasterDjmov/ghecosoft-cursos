# Java · El arco de Zed (borrador 1, a revisar)

Nivel 1 y 2 del método de [../JUEGO.md](../JUEGO.md) § 10: **el arco** y **los capítulos** (un párrafo corto por nodo). La planilla de continuidad y las micro-misiones se escriben **después de que el docente apruebe esto**, como en Python ([python.md](python.md)).

Personajes y aspecto: [PERSONAJES.md](PERSONAJES.md). El contenido técnico de cada nodo **no cambia**: cambia la historia que lo envuelve y el corte en micro-misiones. Las crónicas actuales del curso ya son buenas y se conservan casi enteras (el lugar, los aduaneros, la Academia, los Archivos y, en las Sendas, la Bóveda y el Palacio): se reescriben para que las viva **Zed**, en tercera persona, como pasó con Mia.

**Borrador 2 (2026-10-07):** el docente decidió que **manda el programa de la cátedra** (Paradigmas y Lenguajes III, unidades 1 a 3): el camino obligatorio lo cubre entero y lleva al examen; SQL y Swing pasan a ser Sendas optativas. Las decisiones están en § 3 y la estructura nueva, en § 2.

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
| IV | R04 Streams, patrones y concurrencia (U2) | **Las Corrientes del Imperio**: el río y los canales que mueven la capital | Que **no se hace todo solo**: se delega, se reparte y se confía en recetas probadas | **El Leviatán de los Datos**, en la represa |
| V | R05 Eficiencia, SOLID y Spring (U3 y U2) | **La Torre del Arquitecto**, donde Kaffa dibuja los planos del Imperio | Que se construye **para otros**: código que otro puede leer, cambiar y usar | **El Dragón del Imperio**, en la cima de la Torre |

**El misterio:** en cada distrito, Zed encuentra un rastro del mismo viajero:
- en la Aduana, un registro viejísimo de alguien que **declaró una sola cosa**: «un vitral»;
- en la Academia, un molde que nadie sabe usar, con la firma del vitral;
- en los Archivos, la ficha del viajero, que el Espectro Nulo convierte en `null`;
- en las Corrientes, una barcaza encallada en la represa: el viajero mandó por el río **un vitral para la ventana más alta de la Torre**, y nunca llegó.

**El final:** Zed vence al Dragón y sube a lo más alto de la Torre del Arquitecto, con el vitral que rescató del río. Hay una ventana que nunca se abrió, con un marco esperando un vidrio. **La llave entra.** El vitral se enciende y muestra, por un instante, un balcón con cuatro portales: una espiral, un engranaje, **un vitral** y un arco de fuego. En el marco está grabado *«para quien llegue»*. Kaffa le cuenta lo que sabe (su pieza del portal):

> «Trató de explicarme qué estaba construyendo y no pude ponerlo en ninguna clase. Es lo único que nunca supe ordenar: algo que no es de ningún lugar, porque es de todos.»

Zed no vuelve al Puerto todavía. Desde la Encrucijada de los Denarios salen las Sendas, y el vitral le mostró que el camino sigue.

**La compañía en el Imperio:**
- **Zed.**
- **Gheco**, que da las pistas (aparece sobre el hombro de Zed en la Aduana, sin explicar de dónde salió).
- **Nadia** (nueva), la aduanera que lo atrapa en la Clase 0. Es joven, estricta y cumple cada regla; lo vigila «hasta que aprenda», y termina siendo su compañera. Es el contrapunto de Zed: ella pregunta **«¿qué dice el reglamento?»**, él **«¿y si probamos por acá?»**. Los dos tienen razón a medias.
- **Kira, Mia y Bron no viajan con él.** Solo se los anticipa: en los Archivos hay una ficha recién llegada del Valle sobre «una aprendiz de maga que encontró notas con un vitral», y en el puerto del río un barquero comenta que una espadachina bajó hacia las Forjas.

**Personajes del Imperio:**
- **Kaffa:** el Arquitecto Imperial, el mentor.
- **Nadia:** la aduanera, compañera de Zed.
- **El Escriba Jefe de la Aduana**, **el instructor de la Academia** y **el Archivista Mayor**: secundarios que ya están en las crónicas.
- **El Barquero de la Represa:** en las Corrientes.
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

**R03-N08 · Jefe: el Espectro Nulo** — *La sala vacía.* Se lo vence diseñando para que el `null` no tenga dónde esconderse. La ficha del viajero vuelve entera: **mandó algo por el río** hacia la Torre del Arquitecto, y nunca llegó. Consigue: el ítem épico, **la Linterna del Espectro**. Gancho: desde los Archivos se oye el río que cruza la capital.

### Acto IV — Las Corrientes del Imperio (R04, unidad 2)

Lo que hoy es la Senda de las Corrientes (S02) pasa al camino obligatorio, más un nodo nuevo de patrones.

**R04-N01 · Streams: datos que fluyen** *(hoy S02-N01)* — *El río de la capital.* Por el río bajan miles de barcazas con mercadería; nadie las descarga una por una: se **filtran**, se **transforman** y se **cuentan** mientras pasan. Consigue: cartas `stream()`, `filter`, `map`, `forEach`. Gancho: en los muelles, los recaudadores juntan todo en cajas.

**R04-N02 · Collectors y Optional** *(hoy S02-N02)* — *Los muelles.* Consigue: cartas `collect`, `Collectors.groupingBy`, `Optional`. Gancho: el registro del río dice que una barcaza con «un vitral» nunca llegó a destino.

**R04-N03 · Comparadores y el Java moderno** *(hoy S02-N03)* — *El orden de las barcazas.* Consigue: cartas `Comparator.comparing`, `thenComparing`, `var`, `record` y `switch` modernos. Gancho: los constructores de barcazas repiten siempre los mismos diseños.

**R04-N04 · Patrones de diseño: Singleton, Factory y Strategy** *(nuevo)* — *El astillero.* Los maestros del astillero no inventan cada barco: usan **recetas probadas**. Una sola capitanía para todo el río (Singleton), una fábrica que arma el barco justo según el pedido (Factory), y la ruta que se cambia según el clima sin tocar el barco (Strategy). Zed, que siempre improvisaba, descubre que una receta conocida es otro tipo de atajo. Consigue: cartas Singleton, Factory, Strategy. Gancho: el río se traba en la represa.

**R04-N05 · Concurrencia: Thread, Runnable, Executor y parallel streams** *(hoy S02-N04)* — *Las esclusas.* Una sola esclusa no da abasto; hay que abrir varias **a la vez** sin que las barcazas choquen. Es el cambio del acto: Zed, que siempre trabajó solo, aprende a **repartir el trabajo** y a cuidar lo compartido. Consigue: cartas `Thread`, `Runnable`, `ExecutorService`, `parallelStream()`, `synchronized`. Gancho: en la represa, algo enorme se mueve bajo el agua.

**R04-N06 · Jefe: el Leviatán de los Datos** *(hoy S02-N05)* — *La represa.* Un monstruo hecho de millones de registros que tapa el río. Se lo vence con streams, patrones y varias corrientes a la vez. Detrás de él, encallada, está **la barcaza del viajero**, y adentro, envuelto en lona, **un vitral**. Consigue: el ítem épico, **el Remo de las Corrientes**, y **el Vitral del Viajero** (ítem de historia). Gancho: el vitral tiene una etiqueta: «para la ventana más alta de la Torre del Arquitecto».

### Acto V — La Torre del Arquitecto (R05, unidad 3 y Spring)

La Torre de Kaffa, donde se dibujan los planos de todo el Imperio. Tres nodos nuevos y tres que hoy están en la Senda del Puerto de Spring (S03). El acto entero apunta al **examen final práctico** de la cátedra (el último, «BiblioExpress»: Java 17 o 21, Spring Boot 3, Lombok, Git y GitHub, en memoria, capas controller–service–model–dto, herencia o interfaces, validaciones, el patrón Strategy, `HashMap` y `HashSet`, y Postman con evidencias).

**R05-N01 · Eficiencia: Big O y medir tiempos** *(nuevo)* — *El primer piso: la sala de las balanzas del tiempo.* Dos aprendices discuten qué algoritmo es más rápido; Kaffa les da un reloj: «No discutan: **midan**. Y después, piensen cómo crece». Consigue: cartas O(1), O(n), O(n²), O(log n), `System.nanoTime()`. Gancho: un plano que nadie se anima a cambiar.

**R05-N02 · Principios SOLID** *(nuevo)* — *El segundo piso: los planos viejos.* Un plano tan enredado que cambiar una puerta tira una pared. Kaffa le muestra a Zed las cinco reglas de los planos que duran. Consigue: cartas S, O, L, I, D (una por principio). Gancho: Kaffa: «La última regla es la más importante: **no fabriques lo que usás; pedilo**».

**R05-N03 · Spring: el contenedor, IoC e inyección de dependencias** *(hoy S03-N01)* — *El tercer piso: el taller que arma solo.* En lugar de que cada pieza fabrique sus partes, un **contenedor** las crea y se las entrega. Consigue: cartas `@Component`, `@Service`, `@Autowired`, inyección por constructor, Maven. Gancho: desde la Torre se ve el Puerto, lejos.

**R05-N04 · Servicios REST con Spring MVC** *(hoy S03-N02)* — *El cuarto piso: la ventanilla de los mensajes.* La Torre responde pedidos de todo el Mundo del Código. Zed escribe el servicio que conecta el Imperio con **el Puerto**, su casa: por primera vez llega al Puerto **construyendo** y no robando. Consigue: cartas `@RestController`, `@GetMapping`, `@PostMapping`, `@RequestBody`, JSON, probar con Postman. Gancho: los mensajes del Puerto llegan con cualquier cosa adentro.

**R05-N05 · Capas, DTO, validaciones y Lombok** *(hoy S03-N03, más Lombok)* — *El quinto piso: las cuatro salas.* Kaffa separa el servicio en salas que no se pisan: controller, service, model, dto y el repositorio en memoria. Lo que entra y sale por la ventanilla es un **DTO**, nunca el modelo; lo que entra se **valida**; y Lombok escribe los getters, constructores y builders. Es el cambio del acto: Zed, que entraba por cualquier lado, ahora **diseña las puertas** de su propio servicio. Consigue: cartas DTO, `@Valid`, `@NotBlank`, `@ExceptionHandler`, `@Data`, `@Builder`, `@RequiredArgsConstructor`. Gancho: en la cima, el Tribunal deja un pliego sobre la mesa.

**R05-N06 · Jefe final: el Dragón del Imperio** *(nuevo, reemplaza al de Swing)* — *La cima de la Torre.* El pliego del Tribunal es **un simulacro del examen final, con el mismo formato, pensado para 180 minutos (pasarse no se penaliza)**, ambientado en el Imperio. Por ejemplo, **«AduanaExpress»**:
- **Mercancías** (`Caja`, `Barril`, heredan de `Mercancia`) y **viajeros** (`Mercader`, y `Peregrino`, con 50 % de descuento en los recargos);
- un **recargo por demora** con estrategia activa (`RecargoNormal`, `RecargoFeria`, `RecargoNocturno`: el patrón **Strategy**);
- **depurar pasaportes duplicados** en una sola pasada con `HashSet`, y buscar mercancías por código con `HashMap`;
- capas controller–service–model–dto, repositorio en memoria, Lombok, endpoints REST, colección de Postman y `EVIDENCIAS.md` en un repositorio de GitHub.

Se lo vence pieza por pieza. Consigue: el ítem épico, **la Llave Maestra** (su ganzúa, ya transformada) y su sello de arquitecto. Gancho: la ventana más alta.

**R05-N07 · La Encrucijada de los Denarios** *(hoy R05-N09)* — *La ventana más alta y la fuente.* Zed coloca el vitral del viajero en el marco vacío y la Llave del Vitral lo abre: muestra el balcón de los cuatro portales y *«para quien llegue»*. Kaffa cuenta su pieza del portal. Nadia se queda en la Aduana, como jefa de turno. Gheco señala las Sendas.

### Las Sendas (optativas, desde la Encrucijada)

- **S01 · La Bóveda Imperial** *(hoy R04)*: SQL con PostgreSQL, JDBC, DAO y transacciones; jefe, el Liche de las Tablas Huérfanas. Las micro-misiones de SQL corren en el navegador con SQLite.
- **S02 · El Palacio de las Ventanas** *(hoy R05-N01 a N08)*: Swing, layouts, tablas, MDI, SwingWorker y MVC; jefe, la Registración de Actas. Las micro-misiones son la lógica sin ventana.
- **S03 · El Arcade Imperial** *(hoy S01)*: un juego 2D con Swing.
- **S04 · El Puerto de Spring** *(hoy S03-N04 y N05)*: JPA con base de datos y el Kraken de los Servicios. Zed **vuelve al Puerto**, ahora a construir sus servicios.

**Wrapper y autoboxing** (U1): ya estaban en **R03-N02 · ArrayList y genéricos** (explicación, ejemplo y prueba del sello).

**Hecho (2026-10-07, D96):** el reordenamiento ya está en `cursos/java/` (archivos 04 a 09) y la migración `reorder_java_course_codes` renombra los códigos en la base. Los nodos nuevos ya están escritos (R04-N04 patrones, R05-N01 Big O, R05-N02 SOLID y R05-N06 el Dragón con «AduanaExpress»); Lombok ya estaba en R05-N05.

---

## 3. Lo que decidió el docente (2026-10-07)

1. **Micro-misiones con el ejecutor local desde la Clase 0.** La Clase 0 enseña a instalar el JDK y abrir el ejecutor (*Herramientas → Ejecutor de Java*); desde ahí se comprueban solas, como en Python. **Si no tiene el ejecutor abierto**, el alumno corre el código en su compu o en su IDE y **pega la salida**: si coincide con la esperada, la supera. Java en el navegador se investiga más adelante.
2. **SQL y Swing:** las micro-misiones de SQL corren en el navegador con **SQLite**; las de Swing son **la lógica sin ventana**. Las dos ramas pasan a ser Sendas (§ 2).
3. **3 o 4 micro-misiones por nodo**, siempre que el alumno termine sabiendo el tema: si un nodo necesita más para eso, lleva más.
4. **Las crónicas pasan a tercera persona con Zed**, como con Mia.
5. **Manda el programa de la cátedra:** el camino obligatorio cubre las unidades 1 a 3 y lleva al examen; lo demás es optativo. **El jefe final es un simulacro del examen** (formato del último, «BiblioExpress»), con Spring Boot 3 y Lombok.
6. **UML, JUnit, paquetes y .jar** quedan en el camino (son cortos y ayudan); si hace falta, se dan en clase.
7. **Spring en micro-misiones:** Java puro que imita la idea (un contenedor chiquito, inyectar por constructor, un controlador que devuelve el JSON, una estrategia elegida en tiempo de ejecución). Spring, Lombok, Git y Postman de verdad, en las prácticas que corrige el docente.

**En producción (revisado el 2026-10-07, solo lectura):** un solo alumno cursa Java, en la rama 1 (Clase 0, R01-N01 y R01-N02). Los nodos que se mueven (R04, R05, S02 y S03) no los abrió nadie: se pueden reordenar sin reiniciar a nadie.

**Lo que hay que resolver al programar:**
- **Mover nodos entre ramas** cambia sus códigos (S02-N01 pasa a R04-N01, R04 pasa a ser una Senda). Hoy nadie los cursó (ver arriba), pero el importador tiene que tratarlos como movidos y no como nuevos, para no dejar nodos viejos sueltos.
- **Los tres nodos nuevos** (patrones, Big O, SOLID), **Lombok** dentro de R05-N05 y el **jefe final** hay que escribirlos enteros: explicación, ejemplo, prácticas y prueba del sello, como los demás.

## 3 bis. El juego en el Imperio (hecho, 2026-10-07)

- **Zed** con sus 6 aspectos (`public/img/protagonistas/zed/`).
- **El mapa de expediciones** (`public/img/mundos/imperio/mapa.webp`): 12 lugares, de la Aduana (nivel 1) a la Torre del Arquitecto (nivel 13); se abren desde Decisiones (R01-N05). La Torre del Arquitecto se abre desde R05-N01.
- **El puesto de Baldo en el Imperio:** Baldo, el mercader ambulante (aparece en R01-N04), vende armas, ropa, accesorios y el **Café Fuerte** (la poción del Imperio). 16 ítems del Imperio en `app:game-items`, con su pedido de imagen, más la **Llave del Vitral** (historia).

## 4. Arreglos de continuidad respecto del curso actual

- **{heroe}** pasa a ser Zed en todo el curso (como Mia en Python).
- **R04-N07:** «pasando cien denarios del cofre de Kira al de Bron» pasa a «del cofre de Nadia al de Zed».
- **Ejemplos y prácticas:** hecho (2026-10-08). Kira pasó a **Nadia** y Bron a **Baldo** en todo el curso (Mia no aparecía), con las salidas rehechas ejecutando el código (259 ejemplos y salidas, 223 pruebas). Los protagonistas de otros cursos solo se cruzan como anticipo (JUEGO.md § 1); el hilo con los demás mundos es **el Vidriero**, el que hizo el portal-vitral de Kira (NOVELA-GRAFICA.md).
- **La bienvenida** (`story.course_intro`), **el cierre** (`story.course_completed`) y la ficha de Kaffa en el diccionario se reescriben con Zed, la llave y la ventana.
- **El mapa del Imperio** para las expediciones: hay que generarlo (la Aduana en la muralla, la Academia, los Archivos, el río con sus muelles, esclusas y la represa, la Torre del Arquitecto en el centro, la Encrucijada y los caminos a las Sendas: la Bóveda, el Palacio de las Ventanas, el Arcade y el Puerto).

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
