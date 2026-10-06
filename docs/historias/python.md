# Python · El arco de Mia (borrador 1, a revisar)

Nivel 1 y 2 del método de [../JUEGO.md](../JUEGO.md) § 10: **el arco** y **los capítulos** (un párrafo por nodo). La planilla de continuidad y las micro-misiones se escriben **después de que el docente apruebe esto**.

Personajes y aspecto: [PROTAGONISTAS.md](PROTAGONISTAS.md). El contenido técnico de cada nodo (explicaciones, prácticas, pruebas) **no cambia**: cambia la historia que lo envuelve y el corte en micro-misiones.

---

## 1. El arco

**Mia** es una aprendiz de maga que leyó todos los libros de su escuela y nunca se animó a lanzar un hechizo sin entenderlo entero. Una noche, leyendo, ve abrirse en la pared una **espiral de luz verde**, la toca y despierta en **el Valle de la Serpiente**. Tiene en la mano un **pergamino en blanco** que no es suyo. **Gheco** aparece sobre su hombro y **Ofidia**, la guardiana del Valle, le explica la regla del lugar: acá la magia **no se recita, se escribe**, y el Intérprete hace realidad lo que está escrito, línea por línea.

**Lo que busca:**
- Al principio, **entender** cómo funciona este mundo, como siempre.
- Desde el primer error, **entender quién dejó el pergamino**: tiene una marca de agua que no logra leer, y en el Valle aparecen notas de alguien que escribía la lengua con una claridad perfecta, firmadas con un dibujito de un vitral.

**El peligro del Valle:** las **runas torcidas**. Son siglos de hechizos mal escritos por aprendices que se volvieron criaturas:
- **slimes** por la sintaxis rota;
- **goblins** por mezclar tipos;
- **esqueletos** por nombres sin cuerpo;
- **orcos** por pedir lo que no está;
- **trolls** por las listas compartidas;
- **ogros** por la lógica equivocada.

Donde se acumulan, nace algo grande: un jefe.

**Cómo cambia:** de **leer sin animarse** a **escribir, probar y leer el error**. Ofidia no le da respuestas: le da problemas. El cambio se ve en su túnica:
- **al llegar**, las runas bordadas están apagadas;
- **en cada rama** se enciende una parte;
- **en la rama 2** aparecen los cubos de datos sobre sus manos, cuando aprende a crear objetos.

**Los tres actos**, uno por rama, siempre hacia arriba en el mapa (del río a la cima):

| Acto | Rama | Lugar | Qué aprende Mia (como persona) | Jefe |
|---|---|---|---|---|
| I | R01 Fundamentos | La **Aldea del Script**, el río, los puentes y las **Terrazas de las Funciones** | Que se aprende **escribiendo**: probar, equivocarse, leer el traceback | **La Hidra de las Mil Runas**, en el Paso que sube al Bastión |
| II | R02 Objetos y errores | **El Bastión de las Escamas**, que guarda la **Gran Biblioteca** | Que el error **no es el enemigo**: se lo espera, se lo atrapa y se lo maneja | **El Archivista Corrupto**, que borra las notas del viajero |
| III | R03 Iteración y calidad | **La Torre del Reloj**, en la **Gran Ciudadela de Ofidia** | Que hacerlo **bien** es medir, probar y elegir lo claro | **El Gólem del Reloj**, en la cima |

**El final:** Mia vence al Gólem y el reloj del Valle vuelve a andar. En la **Encrucijada**, Ofidia le cuenta lo que vio hace mucho (su pieza del portal):

> «Hace mucho cruzó el Valle un viajero con las manos manchadas de plomo. Me preguntó cuál era la lengua más clara del mundo, la que cualquiera pudiera leer. Le dije que la mía. Sonrió y siguió camino hacia las Forjas.»

Mia levanta el pergamino, ya lleno, contra la luz del reloj, y por fin se lee la marca de agua: **un vitral, y debajo, «para quien llegue»**. Ella no vuelve a casa todavía. El árbol nunca termina: el viajero siguió hacia las Forjas, y desde la Encrucijada salen las Sendas.

**La compañía en el Valle:**
- **Mia.**
- **Gheco**, que da las pistas.
- **Tilo** (nuevo), un chico de la Aldea que se suma en el capítulo 5. Es práctico y siempre pregunta «¿y eso para qué sirve?»: toma el lugar que tenía Bron.
- **Kira, Zed y Bron no viajan con ella.** Solo se los anticipa: en la Posada, alguien cuenta de «una espadachina de pelo corto que bajó hacia las Forjas».

**Personajes del Valle:**
- **Ofidia:** la guardiana, la mentora.
- **Baldo:** el mercader de la Aldea.
- **La Copista:** en la Aldea.
- **El Ermitaño del Bestiario.**
- **Sila:** la Archivera de la Gran Biblioteca.
- **Maese Horas:** el relojero de la Torre.
- **La Guardiana de la Arena** y **el Consejo del Reino:** en las Sendas.

---

## 2. Los capítulos

Formato de cada capítulo: **lugar** · qué pasa · lo que **consigue** (carta del grimorio o ítem de la historia) · el **gancho** al siguiente.

### Acto I — El Valle bajo (R01)

**R00-N01 · Clase 0 · Hola, Python** — *La orilla del río, junto a la Aldea del Script.*
Mia despierta con el pergamino en blanco. Gheco se presenta y Ofidia emerge del río y le explica la regla del Valle. Primeros conjuros:
- `print` para que el pergamino «hable»;
- una variable para su nombre;
- `input` para escuchar.
Su primer slime nace de una comilla sin cerrar, y Gheco le enseña a **leer el traceback de abajo hacia arriba**.
- **Consigue:** el Pergamino en blanco (su grimorio) y las cartas `print`, `variables`, `input`.
- **Gancho:** Ofidia le dice que en la Aldea hay alguien que la puede ayudar a conseguir lo que necesita.

**R01-N01 · Tipos de datos y conversiones** — *El mercado de la Aldea del Script.*
Baldo, el mercader, le anota tres precios en un papel («12», «3.5», «7»). Mia los «suma» y le da 123.57, y aparece un goblin. Aprende que el texto no es un número y a convertir.
- **Consigue:** su **primera bolsa de oro** (se abre el oro del jugador) y las cartas `int/float/str`, `conversiones`.
- **Gancho:** para salir de la Aldea hay que cruzar el Puente del Juicio.

**R01-N02 · Operadores** — *El Puente del Juicio, sobre el río.*
El puente solo deja pasar a quien sabe **calcular** su daño, **comparar** y **combinar** condiciones: «nivel 5 o más, con llave o con magia, y sin maldición».
- **Consigue:** la carta `operadores` y la Llave del Puente (un ítem de la historia).
- **Gancho:** del otro lado está la Casa de los Copistas, donde un pedido de ayuda espera hace días.

**R01-N03 · Strings: el texto** — *La Casa de los Copistas.*
La Copista tiene los carteles del Valle escritos en runas desordenadas: espacios de más, mayúsculas mezcladas, mensajes al revés. Mia los ordena. En un cartel viejo aparece por primera vez **la firma del vitral**, en una nota escrita con una claridad perfecta.
- **Consigue:** las cartas `strings`, `métodos de texto`, `f-strings con formato`.
- **Gancho:** la Copista no sabe quién la escribió, pero la nota dice «el camino a las Terrazas cruza el Laberinto».

**R01-N04 · Decidir y repetir** — *El Laberinto de las Siete Salas, en las colinas.*
En cada sala hay que **decidir** (trampa, cofre, jefe) y **repetir** hasta encontrar la salida. Es la primera vez que Mia escribe un plan sin leerlo antes en ningún libro.
- **Consigue:** las cartas `if/elif/else`, `while`, `for`, `match`, y la **Espiral de Junco** (ítem: +2 vueltas en las expediciones).
- **Gancho:** sale de noche, agotada, frente a la Posada de la Serpiente.

**R01-N05 · Listas y tuplas** — *La Posada de la Serpiente.*
En la Posada conoce a **Tilo**, un chico de la Aldea que quiere llegar a las Terrazas y no sabe leer las runas. Se suma a la compañía. Hay que llevar la cuenta de quién viaja, qué hay en la mochila y el mapa del camino.
- **Consigue:** las cartas `listas`, `tuplas`, `desempaquetado` y el **Morral de la Posada** (ítem: +4 lugares en la mochila).
- **Se abre:** las **expediciones** (el Profe aparece con su tablero y explica los establos y el mapa).
- **Gancho:** alguien en la Posada habla de «una espadachina de pelo corto que bajó hacia las Forjas». En el camino hay un ermitaño que conoce todas las criaturas.

**R01-N06 · Diccionarios y conjuntos** — *La Ermita del Bestiario.*
El Ermitaño le entrega el **Bestiario**: cada criatura tiene su página, con su vida, su ataque y sus debilidades. Mia aprende a buscar por nombre, contar y cruzar listas de debilidades.
- **Consigue:** las cartas `diccionarios`, `conjuntos`, `Counter`, y **el Bestiario** en su inventario (se abre la ficha de criaturas).
- **Gancho:** el Ermitaño advierte que bajo el próximo puente vive un troll.

**R01-N07 · Referencias, mutabilidad y copias** — *Bajo el puente viejo: la Cueva del Troll.*
Antes de entrar, Mia anota la lista de la compañía «por las dudas». Cuando Tilo cae en una trampa y lo tacha de la lista, descubre con horror que su anotación **también** lo perdió: no eran dos listas, eran **dos nombres para la misma lista**. Es el punto medio del acto. Mia, que creía que leer alcanzaba, entiende que hay que **probar** para saber.
- **Consigue:** las cartas `alias`, `copy/deepcopy` y el **Espejo del Troll** (ítem raro).
- **Gancho:** Tilo está lastimado, y en las Terrazas dicen que hay un hechizo de curación que se escribe una sola vez.

**R01-N08 · Funciones** — *Las Terrazas de las Funciones, primer nivel.*
Mia está cansada de escribir runa por runa el mismo hechizo de curación para Tilo. Ofidia le muestra el truco antiguo: escribirlo **una vez**, ponerle un **nombre** e invocarlo diciendo a quién y cuánto curar.
- **Consigue:** las cartas `def`, `parámetros`, `return`, y **Pociones de Curación** (las primeras del inventario).
- **Gancho:** más arriba, en las Terrazas, hay una cueva donde las palabras solo existen adentro.

**R01-N09 · Alcance, funciones como objetos y recursión** — *La Cueva de los Ecos, en las Terrazas.*
Cada palabra pronunciada en una cámara **solo existe en esa cámara**. Mia descubre que sus conjuros se pueden guardar y pasar de mano en mano. Tilo encuentra un cofre que tiene cofres adentro, que tienen más cofres…
- **Consigue:** las cartas `alcance`, `lambda`, `recursión` y el **Cofre de los Ecos** (ítem).
- **Gancho:** el pergamino de Mia ya es tan largo que se enrolla solo. En la cima de las Terrazas está la Casa de los Tomos.

**R01-N10 · Módulos y paquetes** — *La Casa de los Tomos, en la cima de las Terrazas.*
Cada saber tiene su **tomo** (un módulo) y los de un mismo tema comparten **estante** (un paquete). Mia ordena su pergamino en tomos. En el estante más viejo encuentra un módulo **firmado con el vitral**: el más claro que vio.
- **Consigue:** las cartas `import`, `módulos`, `paquetes` y el **Estante Portátil** (ítem: ordena el inventario).
- **Gancho:** desde la Casa se ve el Paso que sube al Bastión, tapado por algo enorme que se mueve.

**R01-N11 · Jefe: la Hidra de las Mil Runas** — *El Paso de la Hidra.*
Todas las runas torcidas del Valle bajo se juntaron en la Hidra: cada hechizo mal escrito le hace crecer dos cabezas. Mia la vence con lo que aprendió en el acto: **dividir** el problema en funciones chicas y módulos, y **probar** cada parte.
- **Consigue:** el ítem raro del jefe y la **primera parte de la túnica encendida**.
- **Gancho:** el Paso se abre al Bastión de las Escamas, que guarda la Gran Biblioteca.

### Acto II — La Gran Biblioteca (R02)

**R02-N01 · Clases y objetos** — *La Sala de los Moldes, en la Biblioteca.*
Sila, la Archivera, le muestra que los guardianes no escriben cada criatura por separado: tienen **moldes**. De un molde de «orco» salen mil orcos, cada uno con su vida.
- **Mia hace su primer objeto:** por primera vez, **los cubos de datos aparecen sobre sus manos**.
- **Consigue:** las cartas `class`, `__init__`, `métodos`.
- **Gancho:** Sila le cuenta que alguien está mezclando los registros de la Biblioteca.

**R02-N02 · Herencia y polimorfismo** — *El Ala de Estrategia.*
El mapa de batalla muestra héroes, enemigos y torres: todos reciben daño y juegan su turno, cada uno a su manera.
- **Consigue:** las cartas `herencia`, `polimorfismo`, `dataclass`.
- **Gancho:** los registros dañados vienen del sótano.

**R02-N03 · Excepciones y archivos** — *El Sótano húmedo.*
Pergaminos rotos, húmedos o que no están. Un aprendiz intentó leer uno que no existía y el hechizo le explotó en la cara. Mia aprende a **esperar el error y atraparlo**. Es el cambio del acto: el error deja de darle miedo.
- **Consigue:** las cartas `try/except`, `raise`, `with` y el **Amuleto del Traceback** (ítem: una segunda vida en las expediciones).
- **Gancho:** en el sótano encuentra **notas del viajero del vitral, a medio borrar**.

**R02-N04 · JSON y CSV: guardar la partida** — *El Archivo.*
El archivista guarda las crónicas de cada aventurero en dos formatos, el JSON y el CSV. Mia copia las notas del viajero en ambos, para que no se pierdan.
- **Consigue:** las cartas `json`, `csv`.
- **Gancho:** las copias empiezan a cambiar solas: alguien las está corrompiendo desde la Bóveda.

**R02-N05 · Jefe: el Archivista Corrupto** — *La Bóveda.*
El Archivista Corrupto mezcla los registros, borra campos y cambia números por palabras. Quiere borrar las notas del viajero, porque la corrupción se come la claridad. Mia lo vence con archivos que **validan lo que leen** y no se rompen.
- **Consigue:** el ítem raro, la **segunda parte de la túnica encendida** y las **notas del viajero**, que ahora puede leer enteras en su grimorio. Dicen que buscaba «la lengua más clara» para escribir **instrucciones que cualquiera pudiera seguir**.
- **Gancho:** las notas terminan con «la Torre del Reloj guarda el tiempo del Valle; yo le debo una pieza».

### Acto III — La Torre del Reloj (R03)

**R03-N01 · Iteradores y generadores** — *Primer piso de la Torre, en la Gran Ciudadela de Ofidia.*
De un portal no paran de salir enemigos: nadie sabe cuántos son. Mia aprende a pedir **uno por vez**, sin cargarlos todos.
- **Consigue:** las cartas `iteradores`, `yield`, `itertools`.
- **Gancho:** **Maese Horas**, el relojero, le dice que el gran reloj atrasa desde que se perdió una pieza.

**R03-N02 · Programación funcional e itertools** — *Segundo piso.*
Maese Horas ordena cientos de piezas sin tocarlas: «agrupalas», «quedate con las doradas», «ordenalas».
- **Consigue:** las cartas `map/filter`, `sorted(key=)`, `groupby`.
- **Gancho:** entre las piezas hay una de **plomo y vidrio de colores** que no es de ningún reloj.

**R03-N03 · Closures y decoradores** — *Tercer piso.*
Los relojeros no desarman los relojes para mejorarlos: les ponen **encima** una pieza nueva.
- **Consigue:** las cartas `closure`, `decoradores`, `lru_cache`.
- **Gancho:** la pieza de vidrio encaja en un decorador del gran reloj: es la que el viajero arregló hace mucho.

**R03-N04 · Anotaciones de tipos y pruebas** — *Cuarto piso: el Gremio de Artífices.*
Planos que dicen **qué clase** de pieza va, y que se **prueban** antes de montar.
- **Consigue:** las cartas `type hints`, `assert/pruebas` y el **Escudo de las Aserciones** (ítem).
- **Gancho:** arriba se escucha el ruido de una cocina con mil cosas al fuego.

**R03-N05 · asyncio: esperar sin frenar** — *Quinto piso: la cocina.*
La cocinera prepara el banquete sola, con muchas esperas a la vez.
- **Consigue:** las cartas `async/await`, `gather`.
- **Gancho:** el gran reloj se para del todo, y algo despierta en la cima.

**R03-N06 · Rendimiento: medir antes de optimizar** — *Último piso.*
Los aprendices discuten por qué atrasa el reloj. Mia, que antes habría leído todos los manuales, **mide**. En cinco minutos encuentra la culpable.
- **Consigue:** las cartas `timeit`, `estructuras adecuadas` y el **Reloj de Arena** (ítem: termina una expedición al instante, una vez).
- **Gancho:** la pieza culpable es el corazón del Gólem.

**R03-N07 · Jefe: el Gólem del Reloj** — *La cima de la Torre.*
Oleadas de engranajes sin fin, y cada siete oleadas, el Gólem. Mia lo vence con todo lo que aprendió: generadores para las oleadas, pruebas y medir dónde está el problema.
- **Consigue:** el ítem épico, la **túnica encendida entera** y la **última carta**.
- **El reloj del Valle vuelve a andar.**

**R03-N08 · La Encrucijada** — *Los puentes al pie de la Ciudadela.*
Ofidia se enrosca al sol y le cuenta lo que vio (la pieza del portal). Mia levanta el pergamino, ya lleno, contra la luz del reloj, y se lee la marca de agua: **un vitral, y «para quien llegue»**. Tilo se queda en el Valle, como aprendiz de Ofidia. Gheco señala los caminos:
- las **Sendas** del Valle;
- el camino hacia **las Forjas**, por donde siguió el viajero.

### Las Sendas (optativas, después de la Encrucijada)

**S01 · La Senda de la Arena** (pygame) — *El Coliseo del Valle.*
La Guardiana de la Arena: acá los hechizos **se ven y se mueven**. Mia arma su primer juego y, en el jefe, construye «Junta las Gemas» entero.

**S02 · La Senda del Reino** (datos, IA, robótica) — *La oficina del Consejo, la Torre de los Estrategas y el Taller del Reino.*
Los magos del Reino no pelean: **responden preguntas**. Mia lee lo que cuentan las partidas, hace que un enemigo encuentre el camino (A*), arma rivales que aprenden y conecta un mando de Arduino.

---

## 3. Arreglos de continuidad respecto del curso actual

La historia de hoy tiene saltos que este arco corrige:
- **R01-N03** pasaba «en la Gran Biblioteca del Valle», y **R02** «llega» a la Gran Biblioteca: pasa a ser la **Casa de los Copistas**.
- **R01-N10** («la Biblioteca del Valle») pasa a ser la **Casa de los Tomos**.
- **R01-N05**: «Bron, Mia y Zed se sumaron» pasa a ser **Tilo se suma**. En R01-N07, quien cae es Tilo. En R01-N09, Tilo encuentra el cofre.
- **Los ejemplos y las prácticas** que usan a Kira, Zed y Bron como compañía pasan a usar a Mia, Tilo, Gheco y gente del Valle. Kira puede quedar como una viajera de paso.
- **La bienvenida** (`story.course_intro`) y el **epílogo** (`story.course_completed`) se reescriben con Mia, el pergamino y la marca de agua.

## 4. El mapa del Valle

El mapa que generó el docente (`mundos_cursos/ofidia/`) ya tiene la Aldea del Script, la Posada de la Serpiente, las Terrazas de las Funciones, el Bastión de las Escamas y la Gran Ciudadela de Ofidia. **Faltan**, para regenerarlo:
- el Mercado (en la Aldea);
- el Puente del Juicio;
- la Casa de los Copistas;
- el Laberinto de las Siete Salas;
- la Ermita del Bestiario;
- la Cueva del Troll (bajo un puente viejo);
- la Cueva de los Ecos y la Casa de los Tomos (en las Terrazas);
- el Paso de la Hidra;
- la Torre del Reloj (en la Ciudadela);
- la Encrucijada;
- el Coliseo de la Arena.

**Para las expediciones**, los lugares se abren por acto: el Valle bajo con R01, el Bastión con R02 y la Ciudadela con R03.

## 5. Personaje nuevo: Tilo (para generar)

- **Quién es:** chico de 14 años de la Aldea del Script, hijo de un balsero, que sueña con subir a las Terrazas. No sabe leer las runas, pero sabe todo del río.
- **Personalidad:** práctico, valiente de más, pregunta «¿y eso para qué sirve?».
- **Aspecto:**
  - piel trigueña, pelo castaño desordenado con alguna hoja enredada;
  - **pañuelo verde** al cuello (el verde del Valle);
  - chaleco de cuero sobre camisa oscura con vivos verdes neón, pantalón arremangado, descalzo o con sandalias;
  - una **pértiga de balsero** con un farol verde en la punta.
- **No es protagonista:** solo cuerpo entero y retrato circular, sin variantes.
