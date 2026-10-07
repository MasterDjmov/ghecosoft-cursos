# Python · Acto I (R01): la planilla de continuidad y las micro-misiones

Nivel 3 y 4 del método ([../JUEGO.md](../JUEGO.md) § 10) para **la Clase 0 y la rama 1** del arco de Mia ([python.md](python.md)). Personajes y aspecto: [PERSONAJES.md](PERSONAJES.md).

**Estado:**
- La planilla (§ 2) cubre la Clase 0 y los 11 nodos.
- Las micro-misiones completas (§ 3) están escritas para **todo el Acto I**: la Clase 0 y los nodos 1 a 11 (70 en total).
- **Regla de largo:** una sola cosa por micro-misión, escena de 2 a 4 líneas, la pista justa. Si un tema necesita más, se agrega **otra micro-misión corta**, nunca una más larga. Ninguna usa temas de nodos posteriores.
- Las salidas esperadas de los nodos 2 a 11 salen de **ejecutar cada solución**, no de escribirlas a mano. El generador también comprueba que el código inicial **no** dé ya la salida esperada.
- Cuando esté programado, el texto final va al `.md` del curso.

**Cuántos nodos tiene cada acto:**

| Acto | Nodos |
|---|---|
| Acto I (R01) | Clase 0 + 11 nodos (10 temas y el jefe) |
| Acto II (R02) | 5 nodos (4 temas y el jefe) |
| Acto III (R03) | 8 nodos (6 temas, el jefe y la Encrucijada) |
| Sendas | 4 nodos cada una |

---

## 1. El formato de una micro-misión

Va **dentro del nodo**, antes de las prácticas que corrige el docente:

````
### Micro-misión R01-N01-P2 · Sumar números, no letras

```meta
lugar: El Mercado de la Aldea del Script
personajes: Mia, Gheco, Baldo
carta: Conversiones | int("12") → 12 · float("3.5") → 3.5 · str(7) → "7"
recompensa: xp 10, oro 15
item: Bolsa de cuero
imagen: R01-N01-P2
```

#### Escena          (narrativa y diálogo, con {heroe} y {mentor})
#### Gheco sugiere   (el concepto mínimo, con un ejemplo)
#### Desafío         (qué hacer + el código inicial)
#### Entrada         (opcional: lo que se «tipea»)
#### Salida esperada (con esto se comprueba sola)
#### Solución        (oculta, como las del docente)
#### Al superarla    (lo que cambia en la escena y el gancho)
#### Imagen          (el pedido para generarla)
````

**Imágenes:**
- Se llaman por el ID de la micro-misión (`R01-N01-P2.webp`).
- Van en `cursos/python/escenas/`, como las capturas de HTML.
- **También se suben o se cambian** desde una sección nueva, **Admin → Historia → Escenas**, con una pestaña por curso: la lista de todas las micro-misiones con su imagen, el pedido para generarla y un botón para subirla.
- Mientras no haya imagen, se muestra la del lugar o el fondo del mundo.

**La carta del grimorio** se escribe en la misma micro-misión (`carta: título | sintaxis`) y se agrupa en el grimorio por el tema del nodo (`temas:` de [cursos/temas.md](../../cursos/temas.md)).

**Estilo de todas las imágenes:** anime/cómic *cyber-arcana*, 16:9 (1376×768), de noche, con luz propia. Valle verde con cascadas y serpientes de piedra, auroras cian en el cielo, código holográfico flotando. Los personajes, siempre con su aspecto fijo de [PERSONAJES.md](PERSONAJES.md).

---

## 2. La planilla de continuidad (Clase 0 y Acto I)

**Qué lleva Mia encima:** empieza con la túnica de runas apagadas y el pergamino en blanco; cada fila suma lo que consigue.

| ID | Lugar | Quiénes | Qué aprende | Qué pasa / qué cambia | Lleva / consigue |
|---|---|---|---|---|---|
| **R00-N01** | Orilla del río, junto a la Aldea | Mia, Gheco, Ofidia | | Mia despierta | Pergamino en blanco |
| P1 | ídem | ídem | `print` | El pergamino escribe su primera frase | carta *print* |
| P2 | ídem | ídem | variables, reasignar | Ofidia le da 5 escamas | carta *variables* |
| P3 | ídem | ídem | f-strings, comentarios | El pergamino arma su ficha | carta *f-strings* |
| P4 | ídem | ídem | `input` | Ofidia le pregunta qué busca | carta *input* |
| P5 | ídem | + un slime | traceback, indentación | Primer slime, derretido. Ofidia la manda al Mercado | carta *leer el error* |
| *M1–M3, E1* | | | *(prácticas del docente)* | | |
| **R01-N01** | El Mercado de la Aldea | + Baldo | | | |
| P1 | ídem | ídem | `type()`, los 5 tipos | Baldo le anota tres precios en un papel | carta *tipos* |
| P2 | ídem | ídem | `int()`, `float()` | Suma letras («123.57»), aparece un goblin; convierte y lo vence | **Bolsa de cuero** (se abre el oro), carta *conversiones* |
| P3 | ídem | ídem | float inexacto, `round()` | El vuelto de Baldo no da justo | carta *round* |
| P4 | ídem | ídem | verdadero/falso, `bool()` | Baldo revisa bolsas vacías y llenas | carta *truthy/falsy* |
| P5 | ídem | ídem | formato de números | Arma el cartel del puesto de Baldo. Él le marca el camino al Puente | carta *formato* |
| **R01-N02 · Operadores** | | | | | |
| P1 | El Puente del Juicio | Mia, Gheco, el Guardián del Puente | Aritméticos | Los golpes que hacen falta |  |
| P2 | El Puente del Juicio | Mia, Gheco, el Guardián del Puente | Asignación aumentada | La cuenta de la energía |  |
| P3 | El Puente del Juicio | Mia, Gheco, el Guardián del Puente | Comparación | ¿Quién es más fuerte? |  |
| P4 | El Puente del Juicio | Mia, Gheco, el Guardián del Puente | Lógicos | La regla del puente |  |
| P5 | El Puente del Juicio | Mia, Gheco, el Guardián del Puente | Pertenencia e identidad | La llave del puente | Llave del Puente |
| **R01-N03 · Strings: el texto** | | | | | |
| P1 | La Casa de los Copistas | Mia, Gheco, la Copista | Crear textos | El cartel que no se entiende |  |
| P2 | La Casa de los Copistas | Mia, Gheco, la Copista | Índices y cortes | El mensaje al revés |  |
| P3 | La Casa de los Copistas | Mia, Gheco, la Copista | Textos inmutables | La tinta que no se borra |  |
| P4 | La Casa de los Copistas | Mia, Gheco, la Copista | Métodos de texto | Ordenar los carteles |  |
| P5 | La Casa de los Copistas | Mia, Gheco, la Copista | Alinear | La firma del vitral | se abre: la primera nota del viajero en el grimorio |
| **R01-N04 · Decidir y repetir** | | | | | |
| P1 | El Laberinto de las Siete Salas | Mia, Gheco | if / elif / else | Sala 1: trampa o cofre |  |
| P2 | El Laberinto de las Siete Salas | Mia, Gheco | while | Sala 2: hasta ver la luz |  |
| P3 | El Laberinto de las Siete Salas | Mia, Gheco | for y range | Salas 3 y 4: contar las losas |  |
| P4 | El Laberinto de las Siete Salas | Mia, Gheco | break y continue | Sala 5: el jefe y la salida |  |
| P5 | El Laberinto de las Siete Salas | Mia, Gheco | match / case | Sala 6: la puerta de los comandos |  |
| P6 | El Laberinto de las Siete Salas | Mia, Gheco | Azar reproducible | Sala 7: los dados de la salida | Espiral de Junco · se abre: el primer ítem que sirve en el juego: la Espiral de Junco |
| **R01-N05 · Listas y tuplas** | | | | | |
| P1 | La Posada de la Serpiente | Mia, Gheco | Listas | Lo que hay en la mochila |  |
| P2 | La Posada de la Serpiente | Mia, Gheco, Tilo | Agregar a una lista | Tilo se suma |  |
| P3 | La Posada de la Serpiente | Mia, Gheco, Tilo | Sacar de una lista | Sacar lo que sobra |  |
| P4 | La Posada de la Serpiente | Mia, Gheco, Tilo | Ordenar | El orden de la guardia |  |
| P5 | La Posada de la Serpiente | Mia, Gheco, Tilo | Recorrer | Pasar lista |  |
| P6 | La Posada de la Serpiente | Mia, Gheco, Tilo | Comprehension | Provisiones para el doble | Morral de la Posada |
| P7 | La Posada de la Serpiente | Mia, Gheco, Tilo | Listas anidadas | El mapa del camino |  |
| P8 | La Posada de la Serpiente | Mia, Gheco, Tilo, el Profe | Tuplas | Coordenadas que no cambian | se abre: las expediciones del jugador |
| **R01-N06 · Diccionarios y conjuntos** | | | | | |
| P1 | La Ermita del Bestiario | Mia, Gheco, Tilo, el Ermitaño | Diccionarios | La página del slime |  |
| P2 | La Ermita del Bestiario | Mia, Gheco, Tilo, el Ermitaño | get | La página que falta |  |
| P3 | La Ermita del Bestiario | Mia, Gheco, Tilo, el Ermitaño | Modificar un diccionario | Anotar lo que viste |  |
| P4 | La Ermita del Bestiario | Mia, Gheco, Tilo, el Ermitaño | Recorrer un diccionario | Leer el Bestiario entero |  |
| P5 | La Ermita del Bestiario | Mia, Gheco, Tilo, el Ermitaño | Contar con un diccionario | Contar las huellas |  |
| P6 | La Ermita del Bestiario | Mia, Gheco, Tilo, el Ermitaño | Counter | El contador del Ermitaño |  |
| P7 | La Ermita del Bestiario | Mia, Gheco, Tilo, el Ermitaño | Conjuntos | Sin repetir |  |
| P8 | La Ermita del Bestiario | Mia, Gheco, Tilo, el Ermitaño | Operaciones de conjuntos | Las debilidades en común | El Bestiario · se abre: la ficha de criaturas del Bestiario en el inventario |
| **R01-N07 · Referencias, mutabilidad y copias** | | | | | |
| P1 | La Cueva del Troll | Mia, Gheco, Tilo | Alias | La anotación de respaldo |  |
| P2 | La Cueva del Troll | Mia, Gheco, Tilo | Reasignar | Reasignar no es modificar |  |
| P3 | La Cueva del Troll | Mia, Gheco, Tilo | == frente a is | ¿El mismo o igual? |  |
| P4 | La Cueva del Troll | Mia, Gheco, Tilo | Copia superficial | La copia que no alcanza |  |
| P5 | La Cueva del Troll | Mia, Gheco, Tilo | Copia profunda | Copiar hasta el fondo | Espejo del Troll |
| **R01-N08 · Funciones** | | | | | |
| P1 | Las Terrazas de las Funciones | Mia, Gheco, Tilo, Ofidia | def | El hechizo con nombre |  |
| P2 | Las Terrazas de las Funciones | Mia, Gheco, Tilo, Ofidia | Parámetros | A quién y cuánto |  |
| P3 | Las Terrazas de las Funciones | Mia, Gheco, Tilo, Ofidia | return | El hechizo que devuelve |  |
| P4 | Las Terrazas de las Funciones | Mia, Gheco, Tilo, Ofidia | Valores por defecto | Por defecto, una poción chica |  |
| P5 | Las Terrazas de las Funciones | Mia, Gheco, Tilo, Ofidia | Devolver varios | Dos resultados |  |
| P6 | Las Terrazas de las Funciones | Mia, Gheco, Tilo, Ofidia | *args | Tantas pociones como quieras |  |
| P7 | Las Terrazas de las Funciones | Mia, Gheco, Tilo, Ofidia | Default mutable | La bolsa que nadie vació | Pociones de Curación |
| **R01-N09 · Alcance, funciones como objetos y recursión** | | | | | |
| P1 | La Cueva de los Ecos | Mia, Gheco, Tilo | Alcance local | Lo que se dice adentro |  |
| P2 | La Cueva de los Ecos | Mia, Gheco, Tilo | global | El contador de la cueva |  |
| P3 | La Cueva de los Ecos | Mia, Gheco, Tilo | Funciones como valores | El grimorio de conjuros |  |
| P4 | La Cueva de los Ecos | Mia, Gheco, Tilo | lambda | Hechizos de una línea |  |
| P5 | La Cueva de los Ecos | Mia, Gheco, Tilo | Recursión | Cofres dentro de cofres | Cofre de los Ecos |
| **R01-N10 · Módulos y paquetes** | | | | | |
| P1 | La Casa de los Tomos | Mia, Gheco, Tilo, la Copista | import | El tomo de los números |  |
| P2 | La Casa de los Tomos | Mia, Gheco, Tilo, la Copista | from … import | Traer solo lo que usás |  |
| P3 | La Casa de los Tomos | Mia, Gheco, Tilo, la Copista | datetime | El calendario del viaje |  |
| P4 | La Casa de los Tomos | Mia, Gheco, Tilo, la Copista | Decimal | El vuelto exacto |  |
| P5 | La Casa de los Tomos | Mia, Gheco, Tilo, la Copista | namedtuple | Fichas con nombre | Estante Portátil |
| P6 | La Casa de los Tomos | Mia, Gheco, Tilo, la Copista | __name__ | El tomo firmado | se abre: la segunda nota del viajero en el grimorio |
| **R01-N11 · Jefe: la Hidra de las Mil Runas** | | | | | |
| P1 | El Paso de la Hidra | Mia, Gheco, Tilo | Leer un NameError | La cabeza del esqueleto |  |
| P2 | El Paso de la Hidra | Mia, Gheco, Tilo | Leer un TypeError | La cabeza del goblin |  |
| P3 | El Paso de la Hidra | Mia, Gheco, Tilo | Leer un IndexError | La cabeza del orco |  |
| P4 | El Paso de la Hidra | Mia, Gheco, Tilo | Errores de lógica | La cabeza del ogro |  |
| P5 | El Paso de la Hidra | Mia, Gheco, Tilo, Ofidia | Dividir para vencer | La cabeza central |  |

> En la Casa de los Tomos (nodo 10) está **la Copista**, que se mudó a cuidar los tomos. Sila aparece recién en la Gran Biblioteca (Acto II).

---

## 3. Las micro-misiones

### Clase 0 · Hola, Python

#### Micro-misión R00-N01-P1 · El pergamino habla

```meta
lugar: Orilla del río, junto a la Aldea del Script
personajes: Mia, Gheco, Ofidia
carta: print | print("texto") · print(a, b, sep=" | ")
recompensa: xp 10
imagen: R00-N01-P1
```

**Escena.**
Abrís los ojos. Pasto húmedo, el ruido de una cascada y un cielo verde que se mueve como agua. En tu mano hay un **pergamino en blanco** que no es tuyo. El río tiembla y se abre. Del agua sale caminando una mujer alta, de pelo verde larguísimo, con un vestido hecho de escamas esmeralda y una corona de serpientes que se mueven despacio. No se moja.

—Te estaba esperando —dice, con una voz tranquila que suena como el río—. Soy **{mentor}**, la guardiana de este Valle. Acá la magia **no se recita, {heroe}: se escribe**. Lo que escribas en ese pergamino, el **Intérprete** lo hace realidad.

Te quedás quieta. Hay mil preguntas en tu cabeza y ninguna respuesta en el pergamino. Algo cian parpadea sobre tu hombro: un **gecko de luz**, con antiparras de aviador, que te saluda con la cola.

—¡Hola! Soy **Gheco**. No te asustes: en este Valle todos empezamos igual. Lo primero es que el pergamino **hable**. Decile quién sos.

**Gheco sugiere.**
`print(...)` muestra en pantalla lo que le pasás. El texto va **entre comillas**: sin comillas, Python cree que es el nombre de algo.

```python
print("Hola, Valle")
```

**Desafío.** Hacé que el pergamino diga exactamente: `Me llamo Mia y vengo de muy lejos.`

```python
# Escribí abajo tu primer conjuro

```

**Salida esperada.**
```
Me llamo Mia y vengo de muy lejos.
```

**Solución.** `print("Me llamo Mia y vengo de muy lejos.")`

**Al superarla.** Las letras aparecen solas en el pergamino, en tinta verde que brilla. {mentor} asiente despacio.
—Escribiste, y pasó. Así funciona todo acá.

**Imagen.**
- Plano general: la orilla de un río en un valle verde, de noche, con auroras cian.
- Mia, sentada en el pasto, recién despierta, con su túnica violeta de runas **apagadas** y un pergamino en las manos donde brilla una línea de texto verde.
- Del río sale Ofidia: mujer alta, pelo verde larguísimo, vestido de escamas esmeralda con el símbolo de Python en el pecho, corona de serpientes; serena.
- Gheco flota sobre el hombro de Mia.

---

#### Micro-misión R00-N01-P2 · Lo que se anota no se olvida

```meta
lugar: Orilla del río, junto a la Aldea del Script
personajes: Mia, Gheco, Ofidia
carta: Variables | nombre = valor · escamas = escamas + 5
recompensa: xp 10
imagen: R00-N01-P2
```

**Escena.**
{mentor} se arrodilla junto a vos, se arranca **cinco escamas brillantes** del vestido y las deja en el pasto.
—Son tuyas. En el Valle, lo que querés recordar lo anotás con un **nombre**. Anotá quién sos y cuántas escamas tenías antes… y cuántas tenés ahora.

**Gheco sugiere.**
Una **variable** es un nombre que apunta a un valor: `escamas = 0`. El `=` no significa «es igual»: significa «que `escamas` apunte a esto». Para sumarle, calculás con el valor viejo y lo volvés a guardar: `escamas = escamas + 5`.

**Desafío.** Completá la línea que falta para que Mia pase de 0 a 5 escamas.

```python
nombre = "Mia"
escamas = 0
print(nombre, "tiene", escamas, "escamas")

escamas = ___
print(nombre, "tiene", escamas, "escamas")
```

**Salida esperada.**
```
Mia tiene 0 escamas
Mia tiene 5 escamas
```

**Solución.** `escamas = escamas + 5`

**Al superarla.** Las cinco escamas se elevan y se pegan al borde del pergamino, como un sello.
—Ahora el pergamino sabe cuántas tenés —dice Gheco—. Y no se va a olvidar.

**Imagen.**
- Primer plano de las manos de Mia sosteniendo el pergamino.
- Cinco escamas esmeralda flotan hacia él, dejando una estela de luz.
- En el pergamino brilla `escamas = escamas + 5`.
- Gheco, al lado, aplaudiendo con las patitas.

---

#### Micro-misión R00-N01-P3 · La ficha del pergamino

```meta
lugar: Orilla del río, junto a la Aldea del Script
personajes: Mia, Gheco, Ofidia
carta: f-strings | f"Tenés {oro} monedas" · # un comentario
recompensa: xp 10
imagen: R00-N01-P3
```

**Escena.**
—Cada aprendiz del Valle tiene su ficha —dice {mentor}—. Una sola línea que diga quién es, qué tiene y cuánto le falta. Para romper el primer sello del Valle hacen falta **10 escamas**.

**Gheco sugiere.**
Con una `f` antes de las comillas, lo que pongas entre `{ }` se **calcula** y se mete en el texto: `f"Te faltan {10 - escamas}"`. Y lo que va después de `#` es un **comentario**: Python lo ignora, es para quien lee.

**Desafío.** Armá la ficha en una sola línea con un f-string.

```python
nombre = "Mia"
escamas = 5
# La ficha: nombre, clase, escamas y cuántas faltan para 10
print(f"___")
```

**Salida esperada.**
```
Mia - aprendiz de maga - 5 escamas - le faltan 5 para romper el primer sello
```

**Solución.**
```python
print(f"{nombre} - aprendiz de maga - {escamas} escamas - le faltan {10 - escamas} para romper el primer sello")
```

**Al superarla.** En la tapa del pergamino aparece tu ficha, como el título de un libro. Gheco la lee en voz alta, orgulloso, como si fuera suya.

**Imagen.**
- El pergamino abierto, flotando frente a Mia.
- En su borde superior, una línea dorada con la ficha, como un título.
- Mia la mira con curiosidad, ajustándose los anteojos.
- Ofidia, de fondo, desenfocada, sonríe.

---

#### Micro-misión R00-N01-P4 · La pregunta de Ofidia

```meta
lugar: Orilla del río, junto a la Aldea del Script
personajes: Mia, Gheco, Ofidia
carta: input | respuesta = input("¿Pregunta? ") · siempre devuelve texto
recompensa: xp 10
imagen: R00-N01-P4
```

**Escena.**
{mentor} se inclina hasta quedar a tu altura. Las serpientes de su corona también te miran.
—Todos los que cruzan el portal buscan algo, {heroe}. ¿Vos qué venís a buscar?
Querés contestar, pero el pergamino solo habla, no escucha. Todavía.

**Gheco sugiere.**
`input("pregunta ")` muestra la pregunta, espera a que alguien escriba y guarda lo que escribió. **Siempre devuelve texto.** En la plataforma, lo que se «tipea» va en la pestaña **Entrada**.

**Desafío.** Que el pergamino le pregunte a Mia y le conteste con lo que ella responda.

```python
deseo = input("¿Qué venís a buscar? ")
print(f"___")
```

**Entrada.**
```
entender cómo funciona todo
```

**Salida esperada.**
```
¿Qué venís a buscar? Buscás entender cómo funciona todo. Acá eso se consigue escribiendo.
```

**Solución.** `print(f"Buscás {deseo}. Acá eso se consigue escribiendo.")`

**Al superarla.** {mentor} se ríe, un sonido como de hojas secas.
—Entender. Igual que el último que pasó por acá. Él tampoco se quedaba quieto hasta saber cómo funcionaba algo.
No te dice quién era. Todavía.

**Imagen.**
- Ofidia, inclinada a la altura de Mia, mirándola a los ojos; las serpientes de su corona, curiosas.
- Entre ellas, el pergamino muestra un signo de pregunta de luz verde.
- Mia, un poco intimidada pero firme.
- Al fondo, las primeras casas de la Aldea del Script, con faroles verdes.

---

#### Micro-misión R00-N01-P5 · El primer slime

```meta
lugar: Orilla del río, junto a la Aldea del Script
personajes: Mia, Gheco, Ofidia, un slime
criatura: slime
carta: Leer el error | el traceback se lee de abajo hacia arriba: la última línea dice QUÉ pasó; la de arriba, DÓNDE
recompensa: xp 15
imagen: R00-N01-P5
```

**Escena.**
Estás tan entusiasmada que escribís rápido, sin mirar. El pergamino tiembla, se mancha… y de la mancha cae al pasto **un slime**: una gota verde y temblorosa, con dos ojitos, que te muestra la lengua.

—¡Un slime! —grita Gheco—. Nacen de los hechizos mal escritos. Tranquila: son débiles, pero no se van hasta que encontrás qué escribiste mal.

**Gheco sugiere.**
Cuando algo falla, Python muestra un **traceback**. Leelo **de abajo hacia arriba**:
- la última línea dice **qué** pasó (`SyntaxError`, `IndentationError`…);
- la de arriba marca **dónde** (la línea).

Y ojo: los espacios al principio de la línea **significan algo** en Python. Uno de más, sin motivo, es un error.

**Desafío.** Ejecutalo tal como está, leé el error y corregilo. Hay **dos** errores: cuando arregles el primero, aparece el segundo.

```python
print("Las escamas brillan)
  print("El slime se derrite")
```

**Salida esperada.**
```
Las escamas brillan
El slime se derrite
```

**Solución.** Cerrar las comillas de la primera línea y sacar los dos espacios del principio de la segunda.

**Al superarla.** El slime se derrite en un charquito que se evapora con olor a menta.
{mentor} te mira con algo parecido al orgullo.
—Escribiste, te equivocaste y **leíste el error**. La mayoría tarda semanas en aprender eso. Ahora andá a la Aldea: en el Mercado vas a conseguir lo que necesitás para el camino.

**Imagen.**
- Escena de acción cómica: un slime verde translúcido, con ojos grandes, salta frente a Mia.
- Del pergamino sale una línea roja de error, con `SyntaxError` escrito en runas.
- Mia retrocede un paso, sorprendida.
- Gheco, en el aire, señala la línea del error con una pantalla holográfica.

> Después vienen las prácticas que corrige el docente (**M1** La ficha de personaje, **M2** La bolsa de oro, **M3** Cazar al slime, **E1** El ticket de la panadería), sin cambios.

---

### R01-N01 · Tipos de datos y conversiones

#### Micro-misión R01-N01-P1 · El papel del mercader

```meta
lugar: El Mercado de la Aldea del Script
personajes: Mia, Gheco, Baldo
carta: Los 5 tipos | int 12 · float 3.5 · str "7" · bool True · None · type(valor)
recompensa: xp 10
imagen: R01-N01-P1
```

**Escena.**
El Mercado de la Aldea es un enredo de toldos verdes, faroles y serpientes de piedra que hacen de columnas. Detrás de un puesto lleno de cajitas brillantes, un hombrecito de orejas puntiagudas y antiparras en la frente se frota las manos.
—¡Una cara nueva! **Baldo**, para servirte. Para el camino vas a necesitar una bolsa, una cantimplora y una capa. Te anoto los precios.
Te da un papelito: `"12"`, `"3.5"`, `"7"`.

Gheco entrecierra los ojos.
—Antes de sumar nada… ¿de qué **tipo** es cada cosa?

**Gheco sugiere.**
Cada valor tiene un **tipo**:
- `int`: enteros;
- `float`: con decimales;
- `str`: texto, entre comillas;
- `bool`: `True` o `False`;
- `None`: nada.

`type(valor)` te dice cuál es.

**Desafío.** Mostrá el tipo de cada uno de estos cinco valores, uno por línea.

```python
print(type(12))
print(type(3.5))
print(type(___))
print(type(True))
print(type(___))
```

**Salida esperada.**
```
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
<class 'NoneType'>
```

**Solución.** `type("7")` y `type(None)`.

**Al superarla.** Ves que los números del papel tienen **comillas**: no son números, son texto. Baldo se rasca la oreja, incómodo.

**Imagen.**
- El Mercado de la Aldea de noche: toldos verdes, faroles, columnas con forma de serpiente.
- Baldo detrás de su puesto, con una caja de gemas.
- Mia sostiene un papelito con tres números entre comillas, que brillan en rojo.
- Gheco, con una lupa holográfica sobre el papel.

---

#### Micro-misión R01-N01-P2 · Sumar números, no letras

```meta
lugar: El Mercado de la Aldea del Script
personajes: Mia, Gheco, Baldo, un goblin
criatura: goblin
carta: Conversiones | int("12") → 12 · float("3.5") → 3.5 · str(7) → "7"
recompensa: xp 15, oro 15
item: Bolsa de cuero
imagen: R01-N01-P2
```

**Escena.**
Sumás los tres precios como vienen y el pergamino dice `123.57`. Baldo abre grande los ojos, demasiado contento.
—¡Ciento veintitrés con cincuenta y siete! Justo, justo.
Y debajo del puesto, algo se ríe: un **goblin** verde y flaco, con los bolsillos llenos de escamas ajenas.
—¡Te estaban cobrando de más! —grita Gheco—. Los goblins nacen de **mezclar tipos**: sumaste **letras**, no números.

**Gheco sugiere.**
Para usar un texto como número, **convertilo**: `int("12")` da `12` y `float("3.5")` da `3.5`. Con `+`, dos textos se **pegan** (`"12" + "7"` da `"127"`), y dos números se **suman**.

**Desafío.** Convertí los precios antes de sumar.

```python
a = "12"
b = "3.5"
c = "7"
print(a + b + c)          # lo que te quería cobrar
total = ___
print(f"Total: {total}")
```

**Salida esperada.**
```
123.57
Total: 22.5
```

**Solución.** `total = int(a) + float(b) + int(c)`

**Al superarla.** El goblin suelta las escamas y sale corriendo entre los toldos. Baldo, colorado, te cobra lo justo y te regala una **bolsa de cuero** «por las molestias».
—Para que guardes tu oro, que en este mercado no falta quien se lo quiera llevar.

**Se abre:** el **oro** del jugador (la bolsa de cuero en el inventario).

**Imagen.**
- Un goblin flaco y verde huye entre los toldos, con escamas que se le caen de los bolsillos.
- En el pergamino de Mia, `int("12") + float("3.5")` brilla en verde.
- Baldo, avergonzado, le entrega una bolsa de cuero.
- Gheco, triunfante, con los brazos en alto.

---

#### Micro-misión R01-N01-P3 · El vuelto que no da justo

```meta
lugar: El Mercado de la Aldea del Script
personajes: Mia, Gheco, Baldo
carta: Decimales | 0.1 + 0.2 → 0.30000000000000004 · round(x, 2)
recompensa: xp 10, oro 10
imagen: R01-N01-P3
```

**Escena.**
Baldo te da el vuelto en dos monedas: una de 0.1 y otra de 0.2. Le pedís al pergamino que confirme que son 0.3, y el pergamino, muy serio, dice que **no**.
—¿Me estás estafando otra vez? —le preguntás.
—¡Esta vez no, lo juro por mis orejas!

**Gheco sugiere.**
Los `float` no son exactos: `0.1 + 0.2` da `0.30000000000000004`. No es un error de Python: así se guardan los decimales en la máquina. Para comparar o mostrar, **redondeá**: `round(x, 2)`.

**Desafío.** Mostrá el vuelto tal cual y después compará el vuelto **redondeado** con 0.3.

```python
vuelto = 0.1 + 0.2
print(vuelto)
print(___ == 0.3)
```

**Salida esperada.**
```
0.30000000000000004
True
```

**Solución.** `print(round(vuelto, 2) == 0.3)`

**Al superarla.** Baldo respira aliviado.
—Ves que soy honesto… a veces. —Y te agrega 10 de oro de propina, por la paciencia.

**Imagen.**
- Primer plano de dos monedas brillantes sobre el mostrador de Baldo.
- Sobre ellas flota el número `0.30000000000000004`, partido en dos por una grieta de luz.
- Mia lo mira con el ceño fruncido; Baldo, con las manos en alto, inocente.

---

#### Micro-misión R01-N01-P4 · ¿Hay algo en la bolsa?

```meta
lugar: El Mercado de la Aldea del Script
personajes: Mia, Gheco, Baldo
carta: Verdadero y falso | bool("") → False · bool("0") → True · 0, None y "" son falsos
recompensa: xp 10, oro 10
imagen: R01-N01-P4
```

**Escena.**
Baldo vacía sobre el mostrador cuatro bolsitas que le dejaron otros viajeros: una con una nota en blanco, otra con un papel que dice «0», una con cero monedas y otra que nadie sabe qué tiene.
—¿Cuáles tienen **algo**? —te pregunta—. Las vacías las tiro.

**Gheco sugiere.**
`bool(valor)` dice si Python lo considera verdadero o falso. Son **falsos**: `0`, `0.0`, el texto vacío `""` y `None` (y las colecciones vacías, que vas a ver más adelante). **Todo lo demás es verdadero**, ¡aunque sea el texto `"0"`!

**Desafío.** Mostrá en una línea qué bolsas tienen algo.

```python
print(bool(""), bool("0"), bool(___), bool(None))
```

**Salida esperada.**
```
False True False False
```

**Solución.** `bool(0)`

**Al superarla.** Baldo está por tirar la del papel «0», y lo frenás: **tiene algo**. Adentro, doblado, hay un dibujito: **un vitral pequeño, en tinta**. Baldo se encoge de hombros.
—Lo dejó un viajero hace muchísimo. Nunca volvió a buscarlo.
Lo guardás en el pergamino.

**Imagen.**
- Cuatro bolsitas de tela sobre el mostrador, cada una con una etiqueta de luz: `False`, `True`, `False`, `False`.
- Mia sostiene la bolsa marcada `True` y saca un papel con un vitral dibujado en tinta.
- Gheco, intrigado, se asoma por encima.

---

#### Micro-misión R01-N01-P5 · El cartel del puesto

```meta
lugar: El Mercado de la Aldea del Script
personajes: Mia, Gheco, Baldo
carta: Formato de números | f"{x:,.2f}" → 15,230.50 · f"{n:03}" → 007 · f"{p:.0%}" → 15%
recompensa: xp 15, oro 15
imagen: R01-N01-P5
```

**Escena.**
—Ya que sabés tanto —dice Baldo—, haceme un cartel nuevo. Que se lea lo que hay en la caja, el número de mi puesto y el descuento de hoy. **Prolijo**, que los clientes desconfían de los números feos.

**Gheco sugiere.**
En un f-string, después de `:` va el **formato**:
- `{x:,.2f}`: separador de miles y 2 decimales;
- `{n:03}`: rellena con ceros hasta 3 cifras;
- `{p:.0%}`: lo muestra como porcentaje.

**Desafío.**
Completá los tres `___` con el formato justo para que el cartel quede prolijo.

```python
caja = 15230.5
puesto = 7
descuento = 0.15
print(f"Escamas en la caja: {caja:___}")
print(f"Puesto N.º {puesto:___}")
print(f"Descuento: {descuento:___}")
```

**Salida esperada.**
```
Escamas en la caja: 15,230.50
Puesto N.º 007
Descuento: 15%
```

**Solución.** `,.2f`, `03` y `.0%`.

**Al superarla.** El cartel nuevo se ilumina sobre el puesto y se forma una fila de clientes. Baldo, feliz, te señala el camino.
—Para salir de la Aldea hay que cruzar **el Puente del Juicio**. El guardián no deja pasar a cualquiera: hay que saber **calcular**. Suerte, maguita.

**Imagen.**
- El puesto de Baldo con un cartel holográfico nuevo, prolijo, en verde y dorado.
- Una fila de aldeanos curiosos.
- Al fondo, entre la niebla, se ve un puente de piedra con una gran serpiente tallada: el Puente del Juicio.
- Mia, de espaldas, mirando hacia el puente, con su bolsa de cuero al cinturón.

> Después vienen las prácticas que corrige el docente (**M1** El tasador, **M2** La ficha con formato, **M3** ¿Qué tipo es?, **E1** El termómetro del herrero). Ajuste de historia: en M1 el tasador es Baldo.

---

### R01-N02 · Operadores

*El Puente del Juicio, sobre el río. Mia, Gheco y el Guardián del Puente: una serpiente de piedra enroscada en el arco, con ojos de musgo que se encienden cuando habla.*

#### Micro-misión R01-N02-P1 · Los golpes que hacen falta

```meta
lugar: El Puente del Juicio
personajes: Mia, Gheco, el Guardián del Puente
carta: Aritméticos | + - * / · // división entera · % resto · ** potencia
recompensa: xp 10, oro 10
imagen: R01-N02-P1
```

**Escena.**
El cartel de Baldo tenía razón: el puente es de piedra negra, y en el arco se enrosca una **serpiente tallada** tan grande como el río. Cuando ponés un pie encima, sus ojos de musgo se encienden.
—Nadie cruza sin saber **calcular** —retumba—. Primera pregunta, aprendiz: si cada golpe tuyo quita 7 de vida, ¿cuántos golpes **enteros** necesitás para un enemigo de 50? ¿Y cuánta vida le queda después?

**Gheco sugiere.**
`/` divide con decimales (`50 / 7` da `7.142…`). `//` da la **división entera** (cuántas veces entra) y `%` da **el resto** (lo que sobra). Son la pareja que más se usa para repartir y contar.

**Desafío.** Completá con los operadores que faltan.

```python
vida = 50
golpe = 7
print(f"Golpes enteros: {vida ___ golpe}")
print(f"Le queda: {vida ___ golpe}")
print(f"Golpes exactos: {vida / golpe:.2f}")
```

**Salida esperada.**
```
Golpes enteros: 7
Le queda: 1
Golpes exactos: 7.14
```

**Solución.** `vida // golpe` y `vida % golpe`.

**Al superarla.**
Se enciende la primera de las cinco runas talladas en la baranda del puente. El Guardián gruñe, que en piedra es lo más parecido a estar conforme.

**Imagen.**
- El Puente del Juicio de noche: piedra negra sobre un río que brilla verde, con una serpiente gigante tallada en el arco y ojos de musgo encendidos.
- Mia, chiquita frente a la escultura, con el pergamino abierto donde brillan `//` y `%`.
- Gheco flota a su lado contando con los dedos.
- En la baranda, cinco runas: la primera encendida.

---

#### Micro-misión R01-N02-P2 · La cuenta de la energía

```meta
lugar: El Puente del Juicio
personajes: Mia, Gheco, el Guardián del Puente
carta: Asignación aumentada | x += 3 · x -= 5 · x *= 2 · x //= 2 (es x = x + 3, etc.)
recompensa: xp 10, oro 10
imagen: R01-N02-P2
```

**Escena.**
—Segunda pregunta. —El Guardián entrecierra los ojos—. Tenés 20 de energía. Cruzar el primer tramo te cuesta 5. En el medio hay una fuente que te devuelve 3. Y si llegás al final, el puente **duplica** lo que te quede. ¿Con cuánto llegás?

**Gheco sugiere.**
Para cambiar una variable usando su propio valor hay atajos: `energia -= 5` es lo mismo que `energia = energia - 5`. También existen `+=`, `*=`, `//=` y `%=`.

**Desafío.** Escribí cada paso con un atajo y mostrá la energía después de cada uno.

```python
energia = 20
energia ___ 5
print(f"Primer tramo: {energia}")
energia ___ 3
print(f"La fuente: {energia}")
energia ___ 2
print(f"Al final: {energia}")
```

**Salida esperada.**
```
Primer tramo: 15
La fuente: 18
Al final: 36
```

**Solución.** `-=`, `+=` y `*=`.

**Al superarla.**
Se enciende la segunda runa. Del medio del puente brota, de verdad, una fuente chiquita de agua verde. Gheco mete la cola y se ríe porque le hace cosquillas.

**Imagen.**
- El medio del Puente del Juicio: una fuente pequeña de agua verde luminosa brota de la piedra.
- Gheco moja la cola en la fuente y se ríe.
- Mia anota en el pergamino `energia += 3`.
- Dos runas encendidas en la baranda.

---

#### Micro-misión R01-N02-P3 · ¿Quién es más fuerte?

```meta
lugar: El Puente del Juicio
personajes: Mia, Gheco, el Guardián del Puente
carta: Comparación | == != < > <= >= · encadenadas: 10 <= x < 20 · dan True o False
recompensa: xp 10, oro 10
imagen: R01-N02-P3
```

**Escena.**
—Tercera. —La voz del Guardián hace temblar el agua—. Tu fuerza es 12; la mía, 15. Decime sin miedo si sos más fuerte que yo. Decime si tu fuerza está entre 10 y 20, que es lo que pide el puente. Y decime si «Mia» y «mia» son el mismo nombre.

**Gheco sugiere.**
Las comparaciones **siempre** dan `True` o `False`. Se pueden encadenar como en matemática: `10 <= fuerza < 20`. Y ojo: `=` guarda un valor; `==` **pregunta** si son iguales. Las mayúsculas cuentan: `"Mia" == "mia"` es `False`.

**Desafío.** Escribí las tres comparaciones.

```python
fuerza_mia = 12
fuerza_guardian = 15
print(fuerza_mia ___ fuerza_guardian)
print(10 <= fuerza_mia ___ 20)
print("Mia" ___ "mia")
```

**Salida esperada.**
```
False
True
False
```

**Solución.** `>`, `<` y `==`.

**Al superarla.**
—No sos más fuerte que yo —dice el Guardián, y por primera vez suena divertido—. Pero no mentiste. Eso vale más.
Se enciende la tercera runa.

**Imagen.**
- Primer plano de la cabeza de piedra del Guardián, a centímetros de Mia.
- Entre los dos flotan tres resultados de luz: `False`, `True`, `False`.
- Mia sostiene la mirada, con las manos apretando el pergamino; Gheco se esconde detrás de su coleta.

---

#### Micro-misión R01-N02-P4 · La regla del puente

```meta
lugar: El Puente del Juicio
personajes: Mia, Gheco, el Guardián del Puente
carta: Lógicos | and · or · not · cortocircuito · valor por defecto: nombre or "Anónimo"
recompensa: xp 15, oro 15
imagen: R01-N02-P4
```

**Escena.**
En la piedra del arco aparece grabada la regla del puente:
*«Pasa quien tenga nivel 5 o más y una llave, **o** quien sea maga y no esté maldita.»*
Tenés nivel 3, no tenés llave, sos aprendiz de maga y, que sepas, no estás maldita.
—¿Y cómo te llamo? —agrega el Guardián—. No me dijiste tu título. Si no tenés, te llamo «Aprendiz».

**Gheco sugiere.**
`and` pide que se cumplan **las dos**; `or`, **alguna**; `not` da vuelta el valor. `and` se evalúa antes que `or`, pero los paréntesis lo hacen más claro. Y un truco: `titulo or "Aprendiz"` da `titulo` si tiene algo y, si está vacío, `"Aprendiz"`.

**Desafío.** Escribí la regla del puente con `and`, `or` y `not`, y el título con `or`.

```python
nivel = 3
tiene_llave = False
es_maga = True
maldita = False
titulo = ""
pasa = ___
print(f"¿Pasa? {pasa}")
print(f"Te llaman: {___}")
```

**Salida esperada.**
```
¿Pasa? True
Te llaman: Aprendiz
```

**Solución.** `pasa = (nivel >= 5 and tiene_llave) or (es_maga and not maldita)` y `titulo or 'Aprendiz'`.

**Al superarla.**
La cuarta runa se enciende con un brillo violeta, del mismo color que tu túnica. Por un segundo, **una de las runas apagadas de tu túnica parpadea**, como si te reconociera. Después se apaga.

**Imagen.**
- La regla del puente grabada en la piedra del arco, con `and`, `or` y `not` brillando.
- Mia mira sorprendida el borde de su túnica: una runa bordada parpadea en violeta.
- Cuatro runas encendidas en la baranda.

---

#### Micro-misión R01-N02-P5 · La llave del puente

```meta
lugar: El Puente del Juicio
personajes: Mia, Gheco, el Guardián del Puente
carta: Pertenencia e identidad | "x" in texto · x is None · precedencia: * antes que +
recompensa: xp 15, oro 20
item: Llave del Puente
imagen: R01-N02-P5
```

**Escena.**
—Última —dice el Guardián, y abre la boca de piedra. Adentro, sobre la lengua, hay una **llave verde**—. Es tuya si me decís tres cosas: si la palabra «serpiente» está en mi nombre, si de verdad **no** tenías llave (si tu llave era `None`) y cuánto da `2 + 3 * 4`, que los apurados siempre contestan mal.

**Gheco sugiere.**
`"serpiente" in texto` pregunta si un texto está **adentro** de otro. Para preguntar si algo es `None` se usa `is`: `llave is None`. Y la precedencia es la de la escuela: `*` antes que `+`. Si dudás, paréntesis.

**Desafío.** Completá las tres preguntas del Guardián.

```python
nombre = "Guardián del puente, la serpiente de piedra"
llave = None
print("serpiente" ___ nombre)
print(llave ___ None)
print(2 + 3 * 4, ___)
```

**Salida esperada.**
```
True
True
14 20
```

**Solución.** `in`, `is` y `(2 + 3) * 4`.

**Al superarla.**
Las cinco runas brillan a la vez. El Guardián deja caer la **Llave del Puente** en tu mano y se vuelve a quedar quieto, piedra otra vez.
Del otro lado del río, entre los faroles de la Aldea, hay una casa con la puerta abierta y montañas de carteles afuera: **la Casa de los Copistas**. Alguien adentro está gritando que nadie entiende lo que escribe.

**Imagen.**
- El Guardián de piedra con la boca abierta; sobre su lengua, una llave verde brillante.
- Mia estira la mano para tomarla.
- Las cinco runas de la baranda encendidas.
- Al fondo, cruzando el río, una casa con carteles amontonados en la puerta.

---

> Después vienen las prácticas que corrige el docente (**M1** El reloj de arena, **M2** El Puente del Juicio, **M3** Predicción, **E1** El calendario del escriba).

---

### R01-N03 · Strings: el texto

*La Casa de los Copistas, del otro lado del puente. Mia, Gheco y la Copista, rodeada de carteles que hablan solos.*

#### Micro-misión R01-N03-P1 · El cartel que no se entiende

```meta
lugar: La Casa de los Copistas
personajes: Mia, Gheco, la Copista
carta: Crear textos | "…" o '…' · \n salto de línea · \" comilla adentro · """varias líneas"""
recompensa: xp 10, oro 10
imagen: R01-N03-P1
```

**Escena.**
Adentro hay carteles por todos lados: colgados, apilados, pegados al techo. Una mujer alta de túnica lila, con el pelo negro recogido con horquillas, pasea entre ellos con una pluma en la mano.
—¡Por fin alguien que sabe runas! Soy **la Copista**. Me encargaron un cartel para la Posada y me sale todo en una sola línea, y con las comillas rotas. Tiene que decir *Se busca* arriba y, abajo, *"aprendiz" que sepa runas*, con las comillas.

**Gheco sugiere.**
Dentro de un texto, la barra `\` anuncia un carácter especial: `\n` es un **salto de línea** y `\"` es una **comilla** que no cierra el texto. También podés escribir varias líneas entre triples comillas `"""…"""`.

**Desafío.** Arreglá el cartel con `\n` y `\"`.

```python
cartel = "Se busca: "aprendiz" que sepa runas"
print(cartel)
```

**Salida esperada.**
```
Se busca:
"aprendiz" que sepa runas
```

**Solución.** `cartel = "Se busca:\n\"aprendiz\" que sepa runas"`.

**Al superarla.**
El cartel se dobla solo en dos renglones prolijos. La Copista aplaude con la pluma.
—¡Eso! Ahora, el resto…

**Imagen.**
- Interior de la Casa de los Copistas: carteles colgados del techo, pilas de pergaminos, faroles verdes.
- La Copista, alta, túnica lila con cintas de texto holográfico flotando, pelo negro con horquillas, pluma en mano.
- Mia sostiene un cartel que se acomoda en dos renglones de luz.

---

#### Micro-misión R01-N03-P2 · El mensaje al revés

```meta
lugar: La Casa de los Copistas
personajes: Mia, Gheco, la Copista
carta: Índices y cortes | t[0] primero · t[-1] último · t[2:5] del 2 al 4 · t[::-1] al revés
recompensa: xp 10, oro 10
imagen: R01-N03-P2
```

**Escena.**
La Copista te pasa un papel viejo.
—Este llegó así. Todos los mensajes de la Aldea vienen al derecho, menos los de **un** cliente, que los escribe al revés para que no los lean los curiosos.
El papel dice: `otnirebaL le ne somev soN`.

**Gheco sugiere.**
Cada letra de un texto tiene una **posición**, y se empieza a contar desde **0**: `t[0]` es la primera y `t[-1]`, la última. `t[2:5]` corta de la 2 a la 4 (la 5 no entra). Y `t[::-1]` recorre todo hacia atrás: lo da vuelta.

**Desafío.** Mostrá la primera letra, la última y el mensaje al derecho.

```python
mensaje = "otnirebaL le ne somev soN"
print(mensaje[___], mensaje[___])
print(mensaje[___])
```

**Salida esperada.**
```
o N
Nos vemos en el Laberinto
```

**Solución.** `mensaje[0]`, `mensaje[-1]` y `mensaje[::-1]`.

**Al superarla.**
*Nos vemos en el Laberinto.* La Copista se encoge de hombros.
—Así firma ese cliente. Nunca le vi la cara: deja los pedidos por debajo de la puerta.

**Imagen.**
- Primer plano de un papel amarillento con letras al revés; sobre él, el mismo mensaje se da vuelta en el aire, letra por letra, en luz verde.
- La mano de Mia sostiene el papel; Gheco cuelga cabeza abajo de su brazo para leerlo «al derecho».

---

#### Micro-misión R01-N03-P3 · La tinta que no se borra

```meta
lugar: La Casa de los Copistas
personajes: Mia, Gheco, la Copista
carta: Textos inmutables | nombre.upper() da un texto NUEVO · para guardarlo: nombre = nombre.upper()
recompensa: xp 10, oro 10
imagen: R01-N03-P3
```

**Escena.**
—Los títulos van en mayúsculas —dice la Copista—. Pasá este a mayúsculas.
Escribís `titulo.upper()`, mostrás `titulo`… y sigue en minúsculas. Gheco suspira.

**Gheco sugiere.**
Los textos en Python **no se modifican**: son como tinta que no se borra. `titulo.upper()` no cambia `titulo`: **devuelve un texto nuevo**. Si lo querés guardar, reasignalo: `titulo = titulo.upper()`. Por eso `titulo[0] = "X"` da error.

**Desafío.** Hacé que el título quede guardado en mayúsculas.

```python
titulo = "casa de los copistas"
titulo.upper()
print(titulo)
```

**Salida esperada.**
```
CASA DE LOS COPISTAS
```

**Solución.** `titulo = titulo.upper()`.

**Al superarla.**
—Tinta que no se borra —repite la Copista, como si fuera un refrán—. Mi maestra decía que por eso se copia: el original no se toca nunca.

**Imagen.**
- Un letrero de madera sobre la puerta de la Casa, que pasa de minúsculas a mayúsculas: CASA DE LOS COPISTAS, en letras de luz.
- La Copista lo mira con aprobación; Mia, con el pergamino en alto.

---

#### Micro-misión R01-N03-P4 · Ordenar los carteles

```meta
lugar: La Casa de los Copistas
personajes: Mia, Gheco, la Copista
carta: Métodos de texto | strip() saca espacios de las puntas · lower() · upper() · title() · replace("a", "b")
recompensa: xp 15, oro 15
imagen: R01-N03-P4
```

**Escena.**
El cartel más feo de todos es el de una oficina de la Aldea: tiene espacios por todos lados y mayúsculas mezcladas, como si lo hubiera escrito un goblin.
`"   oFIcina de LAS runas   "`
—Necesito que quede *Oficina De Las Runas*, sin espacios en las puntas.

**Gheco sugiere.**
`strip()` saca los espacios de las puntas y `title()` pone en mayúscula la primera letra de cada palabra. Se pueden **encadenar**: `texto.strip().title()`.

**Desafío.** Limpiá el cartel encadenando los dos métodos. Los corchetes muestran dónde empieza y termina.

```python
cartel = "   oFIcina de LAS runas   "
limpio = cartel
print(f"[{limpio}]")
```

**Salida esperada.**
```
[Oficina De Las Runas]
```

**Solución.** `limpio = cartel.strip().title()`.

**Al superarla.**
Los carteles de toda la casa se acomodan solos, como si hubieran estado esperando que alguien les dijera cómo. Uno, viejísimo, cae de un estante a tus pies.

**Imagen.**
- Decenas de carteles que se ordenan solos en el aire de la Casa, letras que se acomodan.
- Uno muy viejo cae a los pies de Mia; la Copista se agacha a mirarlo.

---

#### Micro-misión R01-N03-P5 · La firma del vitral

```meta
lugar: La Casa de los Copistas
personajes: Mia, Gheco, la Copista
carta: Alinear | f"{t:<10}" izquierda · f"{t:>8}" derecha · f"{t:^12}" centro · len() cuenta letras (también ñ y tildes)
recompensa: xp 15, oro 15
imagen: R01-N03-P5
```

**Escena.**
El cartel viejo no es un cartel: es una **tabla de pedidos**, con tres columnas perfectas, escrita con una letra tan clara que da gusto leerla. Abajo, en una esquina, **el mismo vitral** del papelito de Baldo.
—Lo hizo un cliente hace muchísimos años —dice la Copista—. Me lo dejó como modelo: *«así se ordena un pedido»*. Nunca supe cómo lo hacía tan prolijo.
Gheco se frota las patas.
—Yo sí. Probemos.

**Gheco sugiere.**
En un f-string, después de `:` podés decir el **ancho** y la **alineación**: `{texto:<10}` ocupa 10 lugares a la izquierda; `{texto:>8}`, 8 a la derecha; `{texto:^12}`, centrado. Así las columnas quedan derechas. Y `len("ñandú")` da 5: la ñ y las tildes cuentan como una letra.

**Desafío.** Armá la tabla con las columnas alineadas: el pedido a la izquierda (10 lugares) y la cantidad a la derecha (5 lugares).

```python
print(f"{'Pedido'}|{'Cant.'}")
print(f"{'Tinta'}|{3}")
print(f"{'Pergamino'}|{12}")
print(len("ñandú"))
```

**Salida esperada.**
```
Pedido    |Cant.
Tinta     |    3
Pergamino |   12
5
```

**Solución.** `:<10` en la primera columna y `:>5` en la segunda.

**Al superarla.**
Tu tabla queda igual de derecha que la del viajero. Le mostrás a la Copista el papelito de Baldo: el mismo vitral. Ella abre grandes los ojos.
—Ese cliente decía siempre una cosa: que el camino a las Terrazas de las Funciones **cruza el Laberinto de las Siete Salas**. Y que quien no sabe decidir, no sale.
Te guarda el cartel viejo en el pergamino, como quien entrega una herencia.

**Se abre:** la **primera nota del viajero** en el grimorio (el cartel viejo con la firma del vitral).

**Imagen.**
- Un pergamino antiguo con una tabla de tres columnas perfectamente alineadas, letra clarísima; en la esquina inferior, un pequeño vitral dibujado en tinta.
- Mia sostiene al lado el papelito de Baldo con el mismo dibujo: los dos vitrales se iluminan a la vez.
- La Copista, sorprendida, con la mano en el pecho.

---

> Después vienen las prácticas que corrige el docente (**M1** El nombre del héroe, **M2** La runa espejo, **M3** La tabla de la compañía, **E1** Los correos del Gremio). Ajuste de historia: en M3 la tabla es de los clientes de la Copista, porque la compañía de Mia (Tilo) recién llega en el nodo 5.

---

### R01-N04 · Decidir y repetir

*El Laberinto de las Siete Salas, en las colinas detrás de la Aldea. Mia y Gheco, solos. Cada sala tiene una puerta de piedra con una runa que se enciende cuando el hechizo es correcto.*

#### Micro-misión R01-N04-P1 · Sala 1: trampa o cofre

```meta
lugar: El Laberinto de las Siete Salas
personajes: Mia, Gheco
carta: if / elif / else | se revisan en orden y corre SOLO el primero que se cumple · el bloque va indentado
recompensa: xp 10, oro 10
imagen: R01-N04-P1
```

**Escena.**
La primera sala es un cuadrado de piedra con tres baldosas brillantes en el piso. La runa de la puerta dice: *«Pisá la que te convenga.»*
Gheco olfatea.
—Si la baldosa tiene trampa, esquivala. Si no, y tiene un cofre, abrilo. Y si no hay nada… seguí caminando. Una sola decisión, Mia, en orden.

**Gheco sugiere.**
`if` pregunta; si se cumple, corre su bloque (las líneas con sangría debajo). `elif` es «si no, ¿y esto?», y `else` es «en cualquier otro caso». Python revisa en orden y ejecuta **solo el primero** que se cumple.

**Desafío.** Completá la decisión para la baldosa del medio, que no tiene trampa pero sí cofre.

```python
trampa = False
cofre = True
if trampa:
    print("¡Esquivás la trampa!")
___ cofre:
    print("Abrís el cofre: 15 de oro.")
___:
    print("Seguís caminando.")
```

**Salida esperada.**
```
Abrís el cofre: 15 de oro.
```

**Solución.** `elif cofre:` y `else:`.

**Al superarla.**
El cofre se abre con un chasquido y la puerta de la sala 1 se corre. Detrás, oscuridad total.

**Imagen.**
- Una sala cuadrada de piedra con tres baldosas brillantes; un cofre abierto sobre la del medio.
- Mia de pie al lado, con el pergamino donde brillan `if`, `elif` y `else` como tres caminos.
- Gheco ilumina la sala con su propio brillo cian.

---

#### Micro-misión R01-N04-P2 · Sala 2: hasta ver la luz

```meta
lugar: El Laberinto de las Siete Salas
personajes: Mia, Gheco
carta: while | repite MIENTRAS se cumpla · lo de adentro tiene que cambiar la condición (o no termina nunca)
recompensa: xp 10, oro 10
imagen: R01-N04-P2
```

**Escena.**
La segunda sala es un pasillo oscuro. No se ve el final. La runa dice: *«Avanzá mientras no veas la luz.»*
—No sabemos cuántos pasos son —dice Gheco—. Pero sí sabemos **cuándo frenar**.

**Gheco sugiere.**
`while condicion:` repite su bloque **mientras** la condición sea verdadera. Adentro algo tiene que cambiar para que alguna vez deje de cumplirse; si no, el bucle no termina nunca (y la plataforma lo corta a los 5 segundos).

**Desafío.** La luz aparece cuando la distancia llega a 0. Cada paso acorta 3 metros. Completá la condición y el paso.

```python
distancia = 12
pasos = 0
while ___:
    distancia ___ 3
    pasos += 1
    print(f"Paso {pasos}: faltan {distancia} m")
print("¡Se ve la luz!")
```

**Salida esperada.**
```
Paso 1: faltan 9 m
Paso 2: faltan 6 m
Paso 3: faltan 3 m
Paso 4: faltan 0 m
¡Se ve la luz!
```

**Solución.** `while distancia > 0:` y `distancia -= 3`.

**Al superarla.**
Al cuarto paso, una línea de luz verde aparece en el piso y marca la puerta de la sala 3.

**Imagen.**
- Un pasillo de piedra oscurísimo; Mia avanza con una mano en la pared.
- Gheco ilumina apenas un metro adelante.
- Al fondo, una línea de luz verde en el piso marca la salida.

---

#### Micro-misión R01-N04-P3 · Salas 3 y 4: contar las losas

```meta
lugar: El Laberinto de las Siete Salas
personajes: Mia, Gheco
carta: for y range | for x in secuencia: · range(5) → 0..4 · range(1, 6) → 1..5 · range(0, 10, 2) de 2 en 2
recompensa: xp 10, oro 10
imagen: R01-N04-P3
```

**Escena.**
La tercera sala tiene cinco losas numeradas y la runa dice: *«Pisá cada una, en orden, y decí su número.»* La cuarta tiene losas solo en los números pares hasta el 8.
—Acá sí sabemos cuántas son —dice Gheco—. Eso es trabajo para `for`.

**Gheco sugiere.**
`for x in range(1, 6):` repite **una vez por cada número** del 1 al 5 (el último no entra). `range(0, 9, 2)` va de 2 en 2: 0, 2, 4, 6, 8. Usá `for` cuando sabés cuántas vueltas hay, y `while` cuando no.

**Desafío.** Completá los dos `range`. En la sala 4, mostrá los números en una sola línea separados por espacio.

```python
for losa in range(___):
    print(f"Losa {losa}")
for losa in range(___):
    print(losa, end=" ")
print()
```

**Salida esperada.**
```
Losa 1
Losa 2
Losa 3
Losa 4
Losa 5
0 2 4 6 8 
```

**Solución.** `range(1, 6)` y `range(0, 9, 2)`.

**Al superarla.**
Las losas se encienden una tras otra, como teclas de un piano de piedra. Dos puertas se abren seguidas.

**Imagen.**
- Un piso de losas numeradas que se encienden en secuencia bajo los pies de Mia.
- Gheco salta de losa par en losa par.
- Números de luz flotan sobre cada losa.

---

#### Micro-misión R01-N04-P4 · Sala 5: el jefe y la salida

```meta
lugar: El Laberinto de las Siete Salas
personajes: Mia, Gheco
criatura: ogro
carta: break y continue | break corta el bucle · continue salta a la vuelta siguiente · for…else: el else corre si no hubo break
recompensa: xp 15, oro 15
imagen: R01-N04-P4
```

**Escena.**
La quinta sala tiene seis puertas numeradas. Gheco escucha detrás de cada una: la 2 y la 4 están vacías, y detrás de la 5 ronca un **ogro**. La runa dice: *«Revisá las puertas en orden. Las vacías, salteálas. Si llegás al ogro, no pelees: salí corriendo.»*
—Y si revisamos todas y no está… —susurra Gheco— mejor todavía.

**Gheco sugiere.**
Dentro de un bucle, `continue` **salta** directo a la vuelta siguiente, y `break` **corta** el bucle entero. Un `for` puede tener `else`: corre **solo si el bucle terminó sin `break`** («busqué en todos lados y no estaba»).

**Desafío.** Las vacías (2 y 4) se saltean con `continue`; en la del ogro (5), `break`. Completá.

```python
for puerta in range(1, 7):
    if puerta == 2 or puerta == 4:
        ___
    if puerta == 5:
        print(f"Puerta {puerta}: ¡el ogro! A correr.")
        ___
    print(f"Puerta {puerta}: un cofre")
else:
    print("No había ningún ogro.")
```

**Salida esperada.**
```
Puerta 1: un cofre
Puerta 3: un cofre
Puerta 5: ¡el ogro! A correr.
```

**Solución.** `continue` y `break`.

**Al superarla.**
Salís de la sala 5 sin hacer ruido, con el corazón en la garganta. El ogro ronca detrás de la puerta 5 y no se entera de nada. La puerta 6 queda sin abrir… y no importa.

**Imagen.**
- Seis puertas de piedra en semicírculo; detrás de la quinta, entreabierta, se ve la sombra de un ogro enorme dormido.
- Mia y Gheco en puntas de pie, alejándose con el dedo en los labios.

---

#### Micro-misión R01-N04-P5 · Sala 6: la puerta de los comandos

```meta
lugar: El Laberinto de las Siete Salas
personajes: Mia, Gheco
carta: match / case | match valor: case "a": … case "b" | "c": … case _: (cualquier otro)
recompensa: xp 15, oro 15
imagen: R01-N04-P5
```

**Escena.**
La sexta puerta no tiene picaporte: tiene una **boca de piedra** que espera una palabra. Al lado, grabado: *«norte», «sur», «este» u «oeste». Cualquier otra cosa: la boca se ríe.*
—Es como un menú —dice Gheco—. Para cada palabra, una respuesta.

**Gheco sugiere.**
`match` compara un valor contra varios casos y corre el primero que coincide. `case "este" | "oeste":` acepta cualquiera de los dos, y `case _:` es «cualquier otra cosa». Es más claro que una cadena larga de `elif`.

**Desafío.** La salida está al norte. Completá los casos.

```python
orden = input("¿Hacia dónde? ")
match orden:
    case "norte":
        print("La boca se abre: ¡la salida!")
    case "sur":
        print("Volvés por donde viniste.")
    case ___:
        print("Un muro. Probá otra dirección.")
    case ___:
        print("La boca se ríe de vos.")
```

**Entrada.**
```
norte
```

**Salida esperada.**
```
¿Hacia dónde? La boca se abre: ¡la salida!
```

**Solución.** `case "este" | "oeste":` y `case _:`.

**Al superarla.**
La boca de piedra se abre de par en par. Detrás, la última sala: una mesa redonda con **dos dados de hueso** y una runa más.

**Imagen.**
- Una enorme boca de piedra en la pared que se abre; adentro, luz.
- Cuatro direcciones grabadas alrededor como una rosa de los vientos; «norte» brilla.
- Mia de pie frente a ella; Gheco cubre la cabeza por las dudas.

---

#### Micro-misión R01-N04-P6 · Sala 7: los dados de la salida

```meta
lugar: El Laberinto de las Siete Salas
personajes: Mia, Gheco
carta: Azar reproducible | import random · random.seed(7) · random.randint(1, 6) · misma semilla → mismos números
recompensa: xp 15, oro 20
item: Espiral de Junco
imagen: R01-N04-P6
```

**Escena.**
En la mesa hay dos dados y una runa: *«Tirá tres veces. Si la suma pasa de 8, el Laberinto te deja salir.»*
—¿Y si sale poco? —preguntás.
Gheco señala un número diminuto grabado en el borde de la mesa: **7**.
—Pista: estos dados están **hechizados con una semilla**. Con la misma semilla, siempre sale lo mismo. Así se prueban los programas con azar.

**Gheco sugiere.**
`import random` trae la herramienta del azar. `random.randint(1, 6)` da un número entre 1 y 6 (los dos incluidos). Si antes llamás a `random.seed(7)`, la secuencia es **siempre la misma**: ideal para probar un programa.

**Desafío.** Fijá la semilla 7, tirá tres dados, mostralos y decí si salís.

```python
import random
___
dado1 = random.randint(1, 6)
dado2 = random.randint(1, 6)
dado3 = random.randint(1, 6)
suma = dado1 + dado2 + dado3
print(f"Tiradas: {dado1} {dado2} {dado3} - suma {suma}")
if suma > 8:
    print("¡Salís del Laberinto!")
else:
    print("Seguís adentro.")
```

**Salida esperada.**
```
Tiradas: 3 2 4 - suma 9
¡Salís del Laberinto!
```

**Solución.** `random.seed(7)`.

**Al superarla.**
Los dados se quedan quietos y el piso de la sala gira despacio, como una escalera de caracol. Te deja afuera, en la ladera, bajo las estrellas. En la mesa quedó, enrollado, un **junco con forma de espiral**: lo guardás.
Ya es de noche y estás agotada. Allá abajo, junto al puente viejo, se ven las luces de **la Posada de la Serpiente**.

**Se abre:** el primer ítem que sirve en el juego: la **Espiral de Junco** (+2 vueltas en las expediciones, cuando se abran).

**Imagen.**
- Una mesa redonda de piedra con dos dados de hueso; el número 7 grabado en el borde.
- El piso de la sala gira como una escalera de caracol de luz.
- Afuera, desde la ladera de noche, se ven las luces cálidas de la Posada de la Serpiente junto al río.
- Mia sostiene un junco enrollado en espiral; Gheco bosteza.

---

> Después vienen las prácticas que corrige el docente (**M1** El ritmo de la forja, **M2** Combate con pociones, **M3** El acertijo de la serpiente, **E1** El vuelto del cajero).

---

### R01-N05 · Listas y tuplas

*La Posada de la Serpiente, junto al puente viejo. Mia, Gheco y, desde la segunda micro-misión, **Tilo**. Al final aparece **el Profe**.*

#### Micro-misión R01-N05-P1 · Lo que hay en la mochila

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco
carta: Listas | [a, b, c] · lista[0] primero · lista[-1] último · len(lista)
recompensa: xp 10, oro 10
imagen: R01-N05-P1
```

**Escena.**
La Posada huele a pan y a río. Te sentás junto al fuego y vaciás la mochila sobre la mesa: el pergamino, la llave del puente y la espiral de junco.
—Anotalo —dice Gheco—. Un aventurero que no sabe qué lleva, no sabe qué puede hacer.

**Gheco sugiere.**
Una **lista** guarda varios valores en orden, entre corchetes: `["a", "b"]`. Se cuenta desde 0, igual que en los textos: `lista[0]` es el primero y `lista[-1]`, el último. `len(lista)` dice cuántos hay.

**Desafío.** Mostrá lo primero, lo último y cuántas cosas hay.

```python
mochila = ["pergamino", "llave del puente", "espiral de junco"]
print(mochila[___])
print(mochila[___])
print(len(___))
```

**Salida esperada.**
```
pergamino
espiral de junco
3
```

**Solución.** `mochila[0]`, `mochila[-1]` y `len(mochila)`.

**Al superarla.**
Un chico descalzo, con un farol verde en la punta de una pértiga, mira tu mochila desde la mesa de al lado. No deja de mirar el pergamino.

**Imagen.**
- Interior cálido de la Posada de la Serpiente: fuego, mesas de madera, faroles verdes.
- Sobre la mesa de Mia: un pergamino, una llave verde y un junco en espiral.
- En la mesa de al lado, Tilo (14, pelo castaño con una hoja enredada, pañuelo verde, pértiga con farol verde) mira con curiosidad.

---

#### Micro-misión R01-N05-P2 · Tilo se suma

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco, Tilo
carta: Agregar a una lista | lista.append(x) al final · lista.insert(0, x) al principio
recompensa: xp 10, oro 10
imagen: R01-N05-P2
```

**Escena.**
—Soy **Tilo** —dice el chico—. Sé todo del río, pero no sé leer las runas. Quiero subir a las Terrazas. ¿Me llevan?
Gheco te mira. Vos mirás la lista de la compañía, que hasta ahora tenía dos nombres.

**Gheco sugiere.**
`lista.append(x)` agrega `x` **al final**. La lista cambia ahí mismo: no hace falta volver a asignarla.

**Desafío.** Sumá a Tilo a la compañía.

```python
compania = ["Mia", "Gheco"]
___
print(compania)
print(f"Somos {len(compania)}")
```

**Salida esperada.**
```
['Mia', 'Gheco', 'Tilo']
Somos 3
```

**Solución.** `compania.append("Tilo")`.

**Al superarla.**
Tilo sonríe con toda la cara. —¿Y eso para qué sirve? —pregunta, señalando el pergamino. Es la primera de muchas veces que lo va a preguntar.

**Imagen.**
- Tilo, de pie, con la pértiga y el farol verde, extiende la mano a Mia.
- Sobre la mesa, el pergamino muestra una lista que crece: Mia, Gheco, Tilo.
- Gheco, sobre el hombro de Mia, desconfiado pero sonriendo.

---

#### Micro-misión R01-N05-P3 · Sacar lo que sobra

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco, Tilo
carta: Sacar de una lista | lista.remove(x) por valor · lista.pop() el último · x in lista para preguntar
recompensa: xp 10, oro 10
imagen: R01-N05-P3
```

**Escena.**
Tilo vacía su bolsa: un anzuelo, una piedra lisa, **otra piedra lisa** y un pan.
—Dos piedras no —dice Gheco—. Pesan.

**Gheco sugiere.**
`lista.remove(x)` saca **la primera** aparición de `x` (si no está, da error: preguntá antes con `x in lista`). `lista.pop()` saca y devuelve el último.

**Desafío.** Sacá una de las piedras y comé el pan (el último).

```python
bolsa = ["anzuelo", "piedra lisa", "piedra lisa", "pan"]
bolsa.___("piedra lisa")
comido = bolsa.___()
print(f"Te comés: {comido}")
print(bolsa)
```

**Salida esperada.**
```
Te comés: pan
['anzuelo', 'piedra lisa']
```

**Solución.** `remove` y `pop`.

**Al superarla.**
Tilo se guarda la piedra que queda. —Es para hacer sapito en el río —explica, muy serio.

**Imagen.**
- Primer plano de la mesa: un anzuelo, un pan y dos piedras lisas; una de ellas se desvanece en partículas.
- Tilo masticando el pan; Mia anotando en el pergamino.

---

#### Micro-misión R01-N05-P4 · El orden de la guardia

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco, Tilo
carta: Ordenar | lista.sort() cambia la lista · sorted(lista) devuelve una nueva · reverse=True al revés
recompensa: xp 10, oro 10
imagen: R01-N05-P4
```

**Escena.**
Para dormir tranquilos, alguien tiene que hacer guardia. Deciden ir por orden alfabético… pero Gheco quiere ver también el orden al revés, «por si acaso».

**Gheco sugiere.**
`sorted(lista)` devuelve una lista **nueva** ordenada y deja la original como estaba. `lista.sort()` la ordena **ahí mismo**. Las dos aceptan `reverse=True`.

**Desafío.** Mostrá la guardia en orden y al revés, sin cambiar la lista original.

```python
compania = ["Tilo", "Mia", "Gheco"]
print(___)
print(___)
print(compania)
```

**Salida esperada.**
```
['Gheco', 'Mia', 'Tilo']
['Tilo', 'Mia', 'Gheco']
['Tilo', 'Mia', 'Gheco']
```

**Solución.** `sorted(compania)` y `sorted(compania, reverse=True)`.

**Al superarla.**
Le toca a Gheco la primera guardia. Se duerme a los tres minutos.

**Imagen.**
- La Posada de noche, casi a oscuras; Gheco «de guardia» dormido sobre una silla, brillando suave.
- Mia y Tilo durmiendo en catres; sobre la mesa, el pergamino con la lista ordenada.

---

#### Micro-misión R01-N05-P5 · Pasar lista

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco, Tilo
carta: Recorrer | for x in lista: · for i, x in enumerate(lista, start=1): posición y valor
recompensa: xp 10, oro 10
imagen: R01-N05-P5
```

**Escena.**
—Antes de salir se pasa lista —dice Tilo—. Mi papá lo hace con los balseros: uno, dos, tres.

**Gheco sugiere.**
`for x in lista:` recorre los elementos de a uno. Si además querés el número de cada uno, `enumerate(lista, start=1)` te da la **posición y el valor** juntos.

**Desafío.** Pasá lista numerando desde 1.

```python
compania = ["Mia", "Gheco", "Tilo"]
for ___ in ___:
    print(f"{numero}. {nombre}: ¡presente!")
```

**Salida esperada.**
```
1. Mia: ¡presente!
2. Gheco: ¡presente!
3. Tilo: ¡presente!
```

**Solución.** `for numero, nombre in enumerate(compania, start=1):`.

**Al superarla.**
«¡Presente!», grita Gheco tan fuerte que despierta a medio salón.

**Imagen.**
- Amanecer en la puerta de la Posada: Mia, Tilo y Gheco en fila, como soldaditos.
- Números de luz (1, 2, 3) flotan sobre sus cabezas.

---

#### Micro-misión R01-N05-P6 · Provisiones para el doble

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco, Tilo
carta: Comprehension | [expresión for x in lista] · con filtro: [x for x in lista if condición]
recompensa: xp 15, oro 15
item: Morral de la Posada
imagen: R01-N05-P6
```

**Escena.**
El posadero les vende provisiones, pero el camino es largo: hace falta el **doble** de cada cosa. Y de paso, quedarse solo con lo que cueste menos de 5.

**Gheco sugiere.**
Una *comprehension* arma una lista nueva desde otra en una línea: `[p * 2 for p in cantidades]`. Con un `if` al final, filtra: `[p for p in precios if p < 5]`.

**Desafío.** Doblá las cantidades y filtrá los precios baratos.

```python
cantidades = [2, 1, 3]
precios = [3, 8, 4, 12]
dobles = ___
baratos = ___
print(dobles)
print(baratos)
```

**Salida esperada.**
```
[4, 2, 6]
[3, 4]
```

**Solución.** `[c * 2 for c in cantidades]` y `[p for p in precios if p < 5]`.

**Al superarla.**
El posadero, sorprendido por lo rápido de la cuenta, les regala un **morral** de cuero con muchos bolsillos.

**Imagen.**
- El mostrador de la Posada con bolsas de provisiones que se duplican en el aire.
- El posadero entrega un morral de cuero lleno de bolsillos a Mia.

---

#### Micro-misión R01-N05-P7 · El mapa del camino

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco, Tilo
carta: Listas anidadas | mapa[fila][columna] · una lista de filas, cada fila una lista
recompensa: xp 15, oro 15
imagen: R01-N05-P7
```

**Escena.**
Tilo dibuja en la mesa el camino a la Ermita como una grilla: `.` es camino y `#` es piedra. La ermita está en la última fila, a la derecha.

**Gheco sugiere.**
Una lista puede tener listas adentro: un **mapa** es una lista de filas. `mapa[1][2]` es la fila 1, columna 2 (siempre desde 0).

**Desafío.** Mostrá qué hay en la esquina de la ermita (última fila, última columna) y en la casilla del medio.

```python
mapa = [
    [".", "#", "."],
    [".", ".", "#"],
    ["#", ".", "E"],
]
print(mapa[___][___])
print(mapa[___][___])
```

**Salida esperada.**
```
E
.
```

**Solución.** `mapa[2][2]` (o `mapa[-1][-1]`) y `mapa[1][1]`.

**Al superarla.**
—E de Ermita —dice Tilo—. Ahí vive un viejo que sabe el nombre de todos los bichos.

**Imagen.**
- Una grilla de 3×3 dibujada con tiza sobre la mesa de la Posada; una casilla con una E brilla.
- Tilo con la tiza en la mano; Mia sigue el dedo de Tilo sobre la grilla.

---

#### Micro-misión R01-N05-P8 · Coordenadas que no cambian

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco, Tilo, el Profe
carta: Tuplas | (x, y) como una lista que no se cambia · desempaquetar: fila, col = posicion
recompensa: xp 15, oro 20
imagen: R01-N05-P8
```

**Escena.**
Un hombre de barba canosa y sobretodo negro con líneas cian se sienta a la mesa sin pedir permiso. Toma notas en una tableta de luz.
—Soy **el Profe**, el Cronista del Gremio. Anoto las hazañas de los aprendices. La ermita está fija en el mapa, chicos: anótenla como algo que **no cambia**.

**Gheco sugiere.**
Una **tupla** es como una lista, pero entre paréntesis y **no se puede modificar**: ideal para coordenadas. Se puede **desempaquetar**: `fila, col = (2, 2)` reparte cada valor en su variable.

**Desafío.** Guardá la ermita como tupla y desempaquetala.

```python
ermita = ___
fila, col = ___
print(f"Fila {fila}, columna {col}")
```

**Salida esperada.**
```
Fila 2, columna 2
```

**Solución.** `ermita = (2, 2)` y `fila, col = ermita`.

**Al superarla.**
El Profe asiente y les muestra su tablero: un mapa del Valle con lugares que se pueden **recorrer**.
—Mientras estudian, pueden mandar a explorar. Les explico cómo funcionan los establos y las expediciones.
Antes de irse, comenta al pasar que vio bajar hacia las Forjas a una espadachina de pelo corto, con un mechón cian.

**Se abre:** las **expediciones** del jugador (el Profe explica el mapa, el temporizador y los establos).

**Imagen.**
- El Profe (barba canosa, anteojos, sobretodo negro con líneas cian) sentado a la mesa con su tableta holográfica.
- Sobre la tableta, un mapa del Valle con puntos brillantes para explorar.
- Mia y Tilo inclinados para ver; Gheco, fascinado.

---

> Después vienen las prácticas que corrige el docente (**M1** La mochila, **M2** El ranking del torneo, **M3** El mapa de la mazmorra, **E1** Las notas de la escuela).

---

### R01-N06 · Diccionarios y conjuntos

*La Ermita del Bestiario, en el bosque de la colina. Mia, Gheco, Tilo y el Ermitaño, rodeado de libros y de un bicho de luz que nunca se queda quieto.*

#### Micro-misión R01-N06-P1 · La página del slime

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
carta: Diccionarios | {clave: valor} · d["clave"] lee · las claves no se repiten
recompensa: xp 10, oro 10
imagen: R01-N06-P1
```

**Escena.**
El Ermitaño los mira con un solo ojo; el otro es un monóculo de luz cian.
—¿Quieren el Bestiario? Primero lean una página. Cada criatura tiene sus datos con nombre: vida, ataque, debilidad.

**Gheco sugiere.**
Un **diccionario** guarda pares **clave: valor** entre llaves. Se lee por la clave, no por la posición: `slime["vida"]`.

**Desafío.** Mostrá la vida y la debilidad del slime.

```python
slime = {"vida": 10, "ataque": 2, "debilidad": "fuego"}
print(slime[___])
print(slime[___])
```

**Salida esperada.**
```
10
fuego
```

**Solución.** `slime["vida"]` y `slime["debilidad"]`.

**Al superarla.**
—Lee —gruñe el Ermitaño—. Bien. Una página no es un libro.

**Imagen.**
- Interior de una ermita de madera llena de libros y frascos; un bicho de luz revolotea.
- El Ermitaño (capa de musgo con capucha, barba gris, monóculo cian, bastón con orbe) sostiene un libro abierto en la página del slime.
- Mia, Tilo y Gheco leen por encima de su hombro.

---

#### Micro-misión R01-N06-P2 · La página que falta

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
criatura: orco
carta: get | d.get(clave) da None si no está · d.get(clave, "por defecto") · d[clave] da KeyError
recompensa: xp 10, oro 10
imagen: R01-N06-P2
```

**Escena.**
Tilo busca la página del **troll**, que es la que más miedo le da. El libro tiembla y no la encuentra: un orco chiquito asoma entre las hojas.

**Gheco sugiere.**
Pedir una clave que no existe con `d[clave]` da `KeyError` (el grito del orco). `d.get(clave, "algo")` devuelve el valor si está y, si no, lo que le digas.

**Desafío.** Buscá al troll sin que aparezca el orco.

```python
vida = {"slime": 10, "goblin": 15, "orco": 30}
print(vida["troll"])
```

**Salida esperada.**
```
No está anotado
```

**Solución.** `vida.get("troll", "No está anotado")`.

**Al superarla.**
—No está anotado porque nadie volvió para contarlo —dice el Ermitaño. Tilo traga saliva.

**Imagen.**
- Un orco diminuto asoma entre las páginas del Bestiario con la boca abierta, gritando KeyError.
- Tilo da un salto hacia atrás; Mia escribe `get` en el pergamino y el orco se esconde.

---

#### Micro-misión R01-N06-P3 · Anotar lo que viste

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
carta: Modificar un diccionario | d[clave] = valor agrega o cambia · del d[clave] borra
recompensa: xp 10, oro 10
imagen: R01-N06-P3
```

**Escena.**
Le contás al Ermitaño el goblin del mercado. Era más fuerte de lo que dice el libro: tenía 20 de vida, no 15. Y el murciélago de la cueva, que nadie anotó, tenía 8.

**Gheco sugiere.**
`d[clave] = valor` **cambia** el valor si la clave existe y la **agrega** si no.

**Desafío.** Corregí al goblin y agregá al murciélago.

```python
vida = {"slime": 10, "goblin": 15}
___
___
print(vida)
```

**Salida esperada.**
```
{'slime': 10, 'goblin': 20, 'murciélago': 8}
```

**Solución.** `vida["goblin"] = 20` y `vida["murciélago"] = 8`.

**Al superarla.**
El Ermitaño moja la pluma y lo anota él mismo, con letra temblorosa. —Nadie me había traído datos nuevos en años.

**Imagen.**
- El Ermitaño escribe en el Bestiario a la luz de su bastón; una página nueva muestra un murciélago.
- Gheco imita a un murciélago colgado de una viga.

---

#### Micro-misión R01-N06-P4 · Leer el Bestiario entero

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
carta: Recorrer un diccionario | for clave, valor in d.items(): · d.keys() · d.values()
recompensa: xp 10, oro 10
imagen: R01-N06-P4
```

**Escena.**
—Si lo van a llevar, sepan qué hay adentro —dice el Ermitaño—. Léanmelo en voz alta.

**Gheco sugiere.**
`d.items()` da los pares **clave y valor** juntos, para recorrerlos con un `for`.

**Desafío.** Mostrá cada criatura con su vida.

```python
vida = {"slime": 10, "goblin": 20, "murciélago": 8}
for ___ in ___:
    print(f"{nombre}: {v} de vida")
```

**Salida esperada.**
```
slime: 10 de vida
goblin: 20 de vida
murciélago: 8 de vida
```

**Solución.** `for nombre, v in vida.items():`.

**Al superarla.**
El bicho de luz se posa en el hombro de Gheco. Se miran. Se caen bien.

**Imagen.**
- Mia lee en voz alta el Bestiario; nombres de criaturas flotan en el aire como fantasmas de luz.
- El bicho de luz y Gheco, frente a frente, curiosos.

---

#### Micro-misión R01-N06-P5 · Contar las huellas

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
carta: Contar con un diccionario | cuenta[x] = cuenta.get(x, 0) + 1
recompensa: xp 15, oro 15
imagen: R01-N06-P5
```

**Escena.**
Afuera de la ermita hay huellas en el barro. Tilo, que sabe leer huellas aunque no runas, las va nombrando. El Ermitaño quiere saber **cuántas de cada una**.

**Gheco sugiere.**
El patrón para contar: un diccionario vacío y, por cada cosa, `cuenta[x] = cuenta.get(x, 0) + 1`. La primera vez `get` da 0.

**Desafío.** Completá la línea que cuenta.

```python
huellas = ["slime", "goblin", "slime", "slime", "goblin", "troll"]
cuenta = {}
for h in huellas:
    ___
print(cuenta)
```

**Salida esperada.**
```
{'slime': 3, 'goblin': 2, 'troll': 1}
```

**Solución.** `cuenta[h] = cuenta.get(h, 0) + 1`.

**Al superarla.**
Hay **una** huella de troll. Fresca. Tilo deja de sonreír.

**Imagen.**
- Barro con huellas de distintos tamaños; una enorme, de troll, en primer plano.
- Tilo agachado señalando las huellas; contadores de luz flotan sobre cada tipo.

---

#### Micro-misión R01-N06-P6 · El contador del Ermitaño

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
carta: Counter | from collections import Counter · Counter(lista) · .most_common(1)
recompensa: xp 10, oro 10
imagen: R01-N06-P6
```

**Escena.**
El Ermitaño se ríe por primera vez. —Eso que hicieron a mano ya existe hecho. Miren.

**Gheco sugiere.**
`Counter(lista)` cuenta todo de una vez y `.most_common(1)` da el más repetido, con su cantidad.

**Desafío.** Usá `Counter` para saber cuál huella aparece más.

```python
from collections import Counter
huellas = ["slime", "goblin", "slime", "slime", "goblin", "troll"]
cuenta = ___
print(cuenta.most_common(1))
```

**Salida esperada.**
```
[('slime', 3)]
```

**Solución.** `Counter(huellas)`.

**Al superarla.**
—Los slimes siempre ganan en cantidad —dice el Ermitaño—. Por eso hay que aprender a vencerlos rápido.

**Imagen.**
- El Ermitaño con el bastón en alto; del orbe sale un contador holográfico.
- Mia, admirada; Tilo, todavía mirando la huella del troll.

---

#### Micro-misión R01-N06-P7 · Sin repetir

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
carta: Conjuntos | set(lista) sin repetidos ni orden · {a, b} · x in conjunto es muy rápido
recompensa: xp 10, oro 10
imagen: R01-N06-P7
```

**Escena.**
—Para el índice del libro, cada criatura una sola vez —pide el Ermitaño.

**Gheco sugiere.**
Un **conjunto** (`set`) guarda cada valor **una sola vez** y sin orden. `set(lista)` saca los repetidos. Para mostrarlo prolijo, `sorted(conjunto)`.

**Desafío.** Armá el índice sin repetidos y en orden alfabético.

```python
huellas = ["slime", "goblin", "slime", "slime", "goblin", "troll"]
indice = ___
print(sorted(indice))
```

**Salida esperada.**
```
['goblin', 'slime', 'troll']
```

**Solución.** `set(huellas)`.

**Al superarla.**
El índice del Bestiario se escribe solo en la primera página.

**Imagen.**
- La primera página del Bestiario con un índice que se escribe solo, en tinta verde.
- El bicho de luz ilumina cada palabra a medida que aparece.

---

#### Micro-misión R01-N06-P8 · Las debilidades en común

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
carta: Operaciones de conjuntos | a & b los dos · a | b alguno · a - b solo el primero
recompensa: xp 15, oro 20
item: El Bestiario
imagen: R01-N06-P8
```

**Escena.**
—Última lección —dice el Ermitaño—. El troll es débil al fuego y a la luz. El goblin, a la luz y al agua. ¿Qué les sirve contra los dos?

**Gheco sugiere.**
`a & b` da lo que está **en los dos**; `a | b`, lo que está **en alguno**; `a - b`, lo que está en `a` pero **no** en `b`.

**Desafío.** Mostrá lo que sirve contra los dos y lo que sirve solo contra el troll.

```python
troll = {"fuego", "luz"}
goblin = {"luz", "agua"}
print(troll ___ goblin)
print(troll ___ goblin)
```

**Salida esperada.**
```
{'luz'}
{'fuego'}
```

**Solución.** `troll & goblin` y `troll - goblin`.

**Al superarla.**
El Ermitaño cierra el libro y te lo pone en las manos: **el Bestiario** es tuyo.
—La luz sirve contra los dos. Y la van a necesitar: el camino a las Terrazas pasa por **debajo del puente viejo**. Ahí vive el troll de la huella.

**Se abre:** la **ficha de criaturas** del Bestiario en el inventario.

**Imagen.**
- El Ermitaño entrega el Bestiario a Mia; el libro brilla al cambiar de manos.
- Dos círculos de luz se cruzan en el aire: en la intersección, la palabra «luz».
- Por la ventana, a lo lejos, se ve un puente viejo de piedra sobre el río.

---

> Después vienen las prácticas que corrige el docente (**M1** El bestiario, **M2** El reparto del botín, **M3** Las habilidades de la compañía, **E1** Las estadísticas del pregonero).

---

### R01-N07 · Referencias, mutabilidad y copias

*La Cueva del Troll, debajo del puente viejo. Mia, Gheco, Tilo y el troll, que no se ve pero se oye.*

#### Micro-misión R01-N07-P1 · La anotación de respaldo

```meta
lugar: La Cueva del Troll
personajes: Mia, Gheco, Tilo
criatura: troll
carta: Alias | b = a NO copia: son dos nombres para la MISMA lista · lo que cambia por uno, cambia por el otro
recompensa: xp 15, oro 15
imagen: R01-N07-P1
```

**Escena.**
Antes de entrar, anotás la compañía «por las dudas», en una segunda lista. Adentro, el piso cede y **Tilo cae** por un pozo. Lo sacás de la lista… y al mirar la de respaldo, **Tilo tampoco está**.
Desde la oscuridad, el troll se ríe.

**Gheco sugiere.**
`respaldo = compania` **no hace una copia**: da otro nombre a **la misma** lista. Lo que le hacés por un nombre, se ve por el otro. Ejecutalo y mirá.

**Desafío.** Ejecutá el código y completá lo que imprime el respaldo. Después, cambiá la segunda línea para que el respaldo sea una copia de verdad: `compania.copy()`.

```python
compania = ["Mia", "Gheco", "Tilo"]
respaldo = compania
compania.remove("Tilo")
print(compania)
print(respaldo)
```

**Salida esperada.**
```
['Mia', 'Gheco']
['Mia', 'Gheco', 'Tilo']
```

**Solución.** `respaldo = compania.copy()`.

**Al superarla.**
En el respaldo verdadero, Tilo sigue anotado. Y desde el fondo del pozo se escucha su voz: —¡Estoy bien! ¡Me raspé!
Te das cuenta de algo: **leíste** que `=` no copia, y aun así te equivocaste. Hasta que no lo **probaste**, no lo entendiste.

**Imagen.**
- Boca de una cueva bajo un puente viejo de piedra, oscura, con ojos amarillos al fondo.
- Mia, de rodillas al borde de un pozo, con el pergamino donde dos listas brillan unidas por un mismo hilo.
- Gheco ilumina el pozo; abajo, la mano de Tilo saludando.

---

#### Micro-misión R01-N07-P2 · Reasignar no es modificar

```meta
lugar: La Cueva del Troll
personajes: Mia, Gheco, Tilo
criatura: troll
carta: Reasignar | a = a + [x] crea una lista NUEVA (el alias no la ve) · a.append(x) cambia la MISMA
recompensa: xp 10, oro 10
imagen: R01-N07-P2
```

**Escena.**
Gheco quiere entender la trampa del troll. —¿Y si en lugar de `append` sumo con `+`?

**Gheco sugiere.**
`a.append(x)` **modifica** la lista. `a = a + [x]` arma una lista **nueva** y hace que `a` apunte a ella: el otro nombre sigue apuntando a la vieja.

**Desafío.** Completá: el primer resultado tiene que mostrar que `b` no cambió.

```python
a = ["llave"]
b = a
a = ___
print(a)
print(b)
```

**Salida esperada.**
```
['llave', 'bestiario']
['llave']
```

**Solución.** `a = a + ["bestiario"]`.

**Al superarla.**
—Entonces el troll no me engaña si sé si estoy **cambiando** algo o **apuntando** a otra cosa —dice Gheco, orgulloso de la frase.

**Imagen.**
- Dos etiquetas de luz con flechas: una apunta a una caja vieja, la otra a una caja nueva.
- Gheco explicándole a Tilo con gestos exagerados.

---

#### Micro-misión R01-N07-P3 · ¿El mismo o igual?

```meta
lugar: La Cueva del Troll
personajes: Mia, Gheco, Tilo
criatura: troll
carta: == frente a is | == ¿valen lo mismo? · is ¿son el MISMO objeto? · is solo para None
recompensa: xp 10, oro 10
imagen: R01-N07-P3
```

**Escena.**
En la cueva hay dos cofres idénticos. El troll susurra: «Son el mismo». Gheco no le cree.

**Gheco sugiere.**
`==` pregunta si **valen lo mismo**. `is` pregunta si son **el mismo objeto**. Dos listas iguales pueden ser objetos distintos. Para comparar valores usá siempre `==` (y `is` solo con `None`).

**Desafío.** Completá las dos comparaciones.

```python
cofre1 = ["oro", "gema"]
cofre2 = ["oro", "gema"]
print(cofre1 ___ cofre2)
print(cofre1 ___ cofre2)
```

**Salida esperada.**
```
True
False
```

**Solución.** `==` (True) e `is` (False).

**Al superarla.**
—Iguales, pero no el mismo —dice Tilo—. Como dos piedras lisas.

**Imagen.**
- Dos cofres idénticos uno al lado del otro, iluminados por Gheco.
- Sobre ellos, `==` brilla en verde y `is` en rojo.
- Unos ojos amarillos miran desde la oscuridad.

---

#### Micro-misión R01-N07-P4 · La copia que no alcanza

```meta
lugar: La Cueva del Troll
personajes: Mia, Gheco, Tilo
criatura: troll
carta: Copia superficial | lista.copy() copia la de afuera, pero las de ADENTRO siguen compartidas
recompensa: xp 15, oro 15
imagen: R01-N07-P4
```

**Escena.**
Copiás el mapa de la cueva antes de marcar el camino. Marcás una casilla en el original… y **la copia también aparece marcada**. El troll se ríe más fuerte.

**Gheco sugiere.**
`.copy()` copia **la lista de afuera**, pero si adentro hay listas (las filas del mapa), esas se **comparten**. Es una copia **superficial**.

**Desafío.** Ejecutalo y mirá cómo la copia también cambia. No hay que arreglar nada todavía: completá el `print` de la copia.

```python
mapa = [[".", "."], [".", "."]]
copia = mapa.copy()
mapa[0][0] = "X"
print(mapa)
```

**Salida esperada.**
```
[['X', '.'], ['.', '.']]
[['X', '.'], ['.', '.']]
```

**Solución.** `print(copia)`: también tiene la X.

**Al superarla.**
—Las filas son las mismas —dice Mia—. Necesito copiar **todo**, hasta el fondo.

**Imagen.**
- Dos mapas de piedra lado a lado; la misma X aparece en los dos a la vez, unida por un hilo de luz.
- Mia frunce el ceño, pensando.

---

#### Micro-misión R01-N07-P5 · Copiar hasta el fondo

```meta
lugar: La Cueva del Troll
personajes: Mia, Gheco, Tilo
criatura: troll
carta: Copia profunda | import copy · copy.deepcopy(x) copia todo, también lo de adentro
recompensa: xp 15, oro 20
item: Espejo del Troll
imagen: R01-N07-P5
```

**Escena.**
El troll sale de la sombra: enorme, con piel de piedra y musgo. Para vencerlo hay que cruzar marcando el camino **sin arruinar** el mapa de respaldo.

**Gheco sugiere.**
`copy.deepcopy(mapa)` copia la lista **y todo lo que tiene adentro**. Lo que cambies en el original ya no toca la copia.

**Desafío.** Usá `deepcopy` para que el respaldo quede limpio.

```python
import copy
mapa = [[".", "."], [".", "."]]
respaldo = mapa.copy()
mapa[0][0] = "X"
print(respaldo)
```

**Salida esperada.**
```
[['.', '.'], ['.', '.']]
```

**Solución.** `respaldo = copy.deepcopy(mapa)`.

**Al superarla.**
Con el mapa limpio encontrás la salida, y con la luz de Gheco (la debilidad del Bestiario) el troll retrocede hasta convertirse en piedra. Donde estaba, queda un **espejo** de bordes de musgo.
Tilo, raspado, se apoya en vos para caminar. —Dicen que en las Terrazas hay un hechizo de curación que se escribe **una sola vez** —dice, apretando los dientes.

**Imagen.**
- El troll (enorme, piel de piedra y musgo, ojos amarillos) se vuelve estatua bajo la luz cian de Gheco.
- En el suelo, un espejo con bordes de musgo refleja a Mia.
- Tilo, raspado, apoyado en el hombro de Mia.

---

> Después vienen las prácticas que corrige el docente (**M1** El bug del troll, **M2** El punto de guardado, **M3** Predicción, **E1** Las facturas de la herrería).

---

### R01-N08 · Funciones

*Las Terrazas de las Funciones, primer nivel. Mia, Gheco, Tilo (lastimado) y {mentor}, que los espera arriba de una escalera de cascadas.*

#### Micro-misión R01-N08-P1 · El hechizo con nombre

```meta
lugar: Las Terrazas de las Funciones
personajes: Mia, Gheco, Tilo, Ofidia
carta: def | def nombre(): define · nombre() la llama · se escribe UNA vez y se usa muchas
recompensa: xp 10, oro 10
imagen: R01-N08-P1
```

**Escena.**
Llegás a las Terrazas con Tilo colgado de tu hombro. {mentor} los espera junto a una cascada.
—Cansada de escribir runa por runa el mismo hechizo, ¿no? Escribilo **una vez**, ponele **nombre** y llamalo cuando quieras.

**Gheco sugiere.**
`def curar():` define una **función**: un bloque con nombre. No hace nada hasta que la **llamás** con `curar()`. Podés llamarla todas las veces que quieras.

**Desafío.** Definí `curar` y llamala dos veces.

```python
___
    print("Una luz verde cierra un raspón.")

curar()
curar()
```

**Salida esperada.**
```
Una luz verde cierra un raspón.
Una luz verde cierra un raspón.
```

**Solución.** `def curar():`.

**Al superarla.**
Dos raspones de Tilo se cierran. —Me quedan como diez —se queja, pero se le escapa una sonrisa.

**Imagen.**
- Terrazas verdes escalonadas con cascadas; Ofidia, de pie junto al agua, serena.
- Mia apoya la mano en el brazo de Tilo: una luz verde sale de su pergamino.
- Gheco hace de enfermero con una venda en la cola.

---

#### Micro-misión R01-N08-P2 · A quién y cuánto

```meta
lugar: Las Terrazas de las Funciones
personajes: Mia, Gheco, Tilo, Ofidia
carta: Parámetros | def curar(nombre, puntos): · se llama con curar("Tilo", 5) · cada llamada, sus valores
recompensa: xp 10, oro 10
imagen: R01-N08-P2
```

**Escena.**
—Un hechizo que siempre hace lo mismo sirve poco —dice {mentor}—. Decile **a quién** curar y **cuánto**.

**Gheco sugiere.**
Entre los paréntesis de `def` van los **parámetros**: nombres que reciben los valores que le pasás al llamar.

**Desafío.** Agregá los parámetros y curá a Tilo con 5 y a Gheco con 1.

```python
def curar(___):
    print(f"{nombre} recupera {puntos} de vida.")

curar("Tilo", 5)
curar("Gheco", 1)
```

**Salida esperada.**
```
Tilo recupera 5 de vida.
Gheco recupera 1 de vida.
```

**Solución.** `def curar(nombre, puntos):`.

**Al superarla.**
—¿Y a mí por qué? —pregunta Gheco. —Por las dudas —contesta Tilo.

**Imagen.**
- Dos haces de luz verde salen del pergamino: uno grande hacia Tilo, uno chiquito hacia Gheco.
- Ofidia observa, con las serpientes de su corona atentas.

---

#### Micro-misión R01-N08-P3 · El hechizo que devuelve

```meta
lugar: Las Terrazas de las Funciones
personajes: Mia, Gheco, Tilo, Ofidia
carta: return | return valor devuelve un resultado · sin return, la función devuelve None
recompensa: xp 15, oro 15
imagen: R01-N08-P3
```

**Escena.**
—Mostrar no alcanza —dice {mentor}—. Quiero que el hechizo me **dé** la vida nueva, para anotarla.

**Gheco sugiere.**
`return` **devuelve** un valor a quien llamó: `nueva = curar(4, 10)`. `print` solo muestra; `return` entrega. Sin `return`, la función devuelve `None`.

**Desafío.** Hacé que `curar` devuelva la vida nueva.

```python
def curar(vida, puntos):
    ___

vida_tilo = 4
vida_tilo = curar(vida_tilo, 10)
print(f"Tilo tiene {vida_tilo} de vida.")
```

**Salida esperada.**
```
Tilo tiene 14 de vida.
```

**Solución.** `return vida + puntos`.

**Al superarla.**
Tilo se para solo, por primera vez desde la cueva. Sin `return`, el pergamino había dicho «Tilo tiene None de vida», y Gheco casi se desmaya.

**Imagen.**
- Tilo de pie por sus propios medios, con la pértiga.
- Sobre el pergamino, un número que vuelve volando hacia Mia como una flecha de luz: `return 14`.

---

#### Micro-misión R01-N08-P4 · Por defecto, una poción chica

```meta
lugar: Las Terrazas de las Funciones
personajes: Mia, Gheco, Tilo, Ofidia
carta: Valores por defecto | def f(x, y=10): · f(1) usa 10 · f(1, y=25) por nombre
recompensa: xp 10, oro 10
imagen: R01-N08-P4
```

**Escena.**
—Casi siempre curás 10 —observa Gheco—. ¿Y si el 10 viniera solo, y solo lo decís cuando es otra cosa?

**Gheco sugiere.**
`def curar(vida, puntos=10):` hace que `puntos` valga 10 si no lo pasás. Y al llamar podés nombrar el argumento: `curar(4, puntos=25)`, que se lee mejor.

**Desafío.** Poné 10 por defecto y usá el nombre en la segunda llamada.

```python
def curar(vida, puntos___):
    return vida + puntos

print(curar(4))
print(curar(4, ___))
```

**Salida esperada.**
```
14
29
```

**Solución.** `puntos=10` y `puntos=25`.

**Al superarla.**
{mentor} asiente. —Ya escribís hechizos como los del Valle. Subamos.

**Imagen.**
- Ofidia sube por una escalera de piedra entre cascadas; Mia, Tilo y Gheco la siguen.
- En el aire, dos frascos de poción: uno chico (10) y uno grande (25).

---

#### Micro-misión R01-N08-P5 · Dos resultados

```meta
lugar: Las Terrazas de las Funciones
personajes: Mia, Gheco, Tilo, Ofidia
carta: Devolver varios | return a, b devuelve una tupla · se desempaqueta: x, y = f()
recompensa: xp 10, oro 10
imagen: R01-N08-P5
```

**Escena.**
En el segundo nivel, una fuente revisa a quien bebe y dice dos cosas: cuánta vida tiene y si está **en peligro** (menos de 10).

**Gheco sugiere.**
Una función puede devolver varios valores separados por coma: `return vida, vida < 10`. Llegan como una tupla, y la desempaquetás como en la Posada: `v, peligro = revisar(7)`.

**Desafío.** Devolvé los dos valores.

```python
def revisar(vida):
    return ___

v, peligro = revisar(7)
print(f"Vida {v}. ¿En peligro? {peligro}")
```

**Salida esperada.**
```
Vida 7. ¿En peligro? True
```

**Solución.** `return vida, vida < 10`.

**Al superarla.**
Tilo bebe. La fuente dice 14 y «no». Él insiste en que se siente en peligro igual.

**Imagen.**
- Una fuente de piedra con forma de serpiente que muestra dos números de luz sobre el agua.
- Tilo bebiendo con las manos; Gheco controlando el resultado.

---

#### Micro-misión R01-N08-P6 · Tantas pociones como quieras

```meta
lugar: Las Terrazas de las Funciones
personajes: Mia, Gheco, Tilo, Ofidia
carta: *args | def f(*valores): recibe cualquier cantidad · adentro, valores es una tupla
recompensa: xp 15, oro 15
imagen: R01-N08-P6
```

**Escena.**
—¿Y si quiero tomar dos pociones? ¿Y tres? —pregunta Tilo—. ¿Hay que escribir un hechizo para cada cantidad?

**Gheco sugiere.**
Con `*` antes del parámetro, la función acepta **cualquier cantidad** de valores: `def tomar(*pociones):`. Adentro, `pociones` es una tupla que podés recorrer.

**Desafío.** Completá el parámetro y el total.

```python
def tomar(___):
    total = 0
    for p in pociones:
        total += p
    return total

print(tomar(10))
print(tomar(10, 25, 5))
```

**Salida esperada.**
```
10
40
```

**Solución.** `def tomar(*pociones):`.

**Al superarla.**
—Tres juntas no —advierte {mentor}—. Dan hipo de magia. —Tilo ya las tomó.

**Imagen.**
- Tilo con tres frascos vacíos y un hipo que suelta burbujas verdes.
- Ofidia se tapa la boca para no reírse.

---

#### Micro-misión R01-N08-P7 · La bolsa que nadie vació

```meta
lugar: Las Terrazas de las Funciones
personajes: Mia, Gheco, Tilo, Ofidia
carta: Default mutable | NUNCA def f(x, bolsa=[]) · usar bolsa=None y adentro: if bolsa is None: bolsa = []
recompensa: xp 15, oro 20
item: Poción de Curación x3
imagen: R01-N08-P7
```

**Escena.**
{mentor} te da su hechizo para armar bolsas de pociones. Lo usás para Tilo y después para Gheco… y **la bolsa de Gheco aparece con la poción de Tilo adentro**.
—Ah —dice {mentor}—. La trampa más vieja del Valle.

**Gheco sugiere.**
El valor por defecto se crea **una sola vez**, cuando se define la función. Si es una lista, **todas las llamadas comparten la misma**. Usá `None` y creá la lista adentro.

**Desafío.** Arreglá la función para que cada bolsa sea nueva.

```python
def armar_bolsa(pocion, bolsa=[]):
    bolsa.append(pocion)
    return bolsa

print(armar_bolsa("vida"))
print(armar_bolsa("maná"))
```

**Salida esperada.**
```
['vida']
['maná']
```

**Solución.** `bolsa=None` y, adentro, `if bolsa is None: bolsa = []`.

**Al superarla.**
Cada uno con su bolsa, y en cada bolsa **pociones de curación** de verdad. Tilo, curado, salta en una pierna para demostrarlo.
{mentor} señala hacia arriba, donde las terrazas se meten en la montaña. —Ahí hay una cueva donde las palabras solo existen adentro. Cuidado con lo que gritan.

**Imagen.**
- Dos bolsas de cuero, cada una con su poción brillante; un hilo de luz que las unía se corta.
- Tilo saltando en una pierna, curado.
- Ofidia señala hacia la boca de una cueva en lo alto de las terrazas.

---

> Después vienen las prácticas que corrige el docente (**M1** La bolsa de dados, **M2** Formar la compañía, **M3** La bendición del templo, **E1** El precio del mercado).

---

### R01-N09 · Alcance, funciones como objetos y recursión

*La Cueva de los Ecos, entre las Terrazas. Mia, Gheco y Tilo. Cada cámara de la cueva devuelve las palabras, pero solo adentro.*

#### Micro-misión R01-N09-P1 · Lo que se dice adentro

```meta
lugar: La Cueva de los Ecos
personajes: Mia, Gheco, Tilo
criatura: esqueleto
carta: Alcance local | lo que se crea dentro de una función solo existe ahí · para sacarlo: return
recompensa: xp 10, oro 10
imagen: R01-N09-P1
```

**Escena.**
Tilo grita «¡HOLA!» dentro de la primera cámara y el eco responde. Afuera, le pide al eco que repita… y aparece un **esqueleto**: un nombre sin cuerpo.

**Gheco sugiere.**
Una variable creada **dentro** de una función es **local**: afuera no existe (por eso `NameError`). Si la necesitás afuera, **devolvela** con `return`.

**Desafío.** Hacé que la cámara devuelva el eco y guardalo afuera.

```python
def camara():
    eco = "¡HOLA! ¡hola! hola…"

camara()
print(eco)
```

**Salida esperada.**
```
¡HOLA! ¡hola! hola…
```

**Solución.** `return eco` adentro y `eco = camara()` afuera.

**Al superarla.**
El esqueleto se desarma en huesitos que se caen en las piedras. Tilo los junta de recuerdo; Gheco le dice que no.

**Imagen.**
- Una cámara redonda de piedra con ondas de sonido visibles rebotando en las paredes.
- Afuera, un esqueleto torpe hecho de letras sueltas se desarma.
- Tilo con las manos llenas de huesitos; Gheco negando con la cabeza.

---

#### Micro-misión R01-N09-P2 · El contador de la cueva

```meta
lugar: La Cueva de los Ecos
personajes: Mia, Gheco, Tilo
carta: global | para CAMBIAR una variable de afuera desde una función: global x · mejor: recibir y devolver
recompensa: xp 10, oro 10
imagen: R01-N09-P2
```

**Escena.**
Gheco quiere contar cuántas veces gritaron en la cueva. Escribe una función que suma 1… y el pergamino se queja.

**Gheco sugiere.**
Si una función **asigna** una variable, Python la toma como local, aunque exista afuera (`UnboundLocalError`). `global gritos` le avisa que es la de afuera. Funciona, pero se usa poco: casi siempre es mejor recibir el valor y devolverlo.

**Desafío.** Agregá la línea que falta.

```python
gritos = 0

def gritar():
    gritos += 1

gritar()
gritar()
print(f"Gritaron {gritos} veces")
```

**Salida esperada.**
```
Gritaron 2 veces
```

**Solución.** `global gritos` al principio de la función.

**Al superarla.**
—Funciona —dice Gheco—, pero ahora la cueva entera sabe cuánto gritamos. Prefiero que los secretos queden en su cámara.

**Imagen.**
- Gheco con un ábaco de piedra contando gritos; números de eco flotan.
- Tilo con las manos alrededor de la boca, gritando.

---

#### Micro-misión R01-N09-P3 · El grimorio de conjuros

```meta
lugar: La Cueva de los Ecos
personajes: Mia, Gheco, Tilo
carta: Funciones como valores | se guardan en variables y diccionarios · acciones["luz"]() la llama
recompensa: xp 15, oro 15
imagen: R01-N09-P3
```

**Escena.**
En una cámara hay un atril con un libro: cada página tiene un nombre y, al decirlo, el conjuro se lanza solo. Mia se da cuenta de que **sus** hechizos también se pueden guardar así.

**Gheco sugiere.**
Una función es un valor más: se puede guardar en un diccionario **sin paréntesis** (`"luz": luz`) y llamarla después con `acciones["luz"]()`. Es una tabla de acciones: reemplaza muchos `if`.

**Desafío.** Completá la tabla y llamá al conjuro que pide la orden.

```python
def luz():
    print("La cueva se ilumina.")

def calma():
    print("Los ecos se callan.")

acciones = {"luz": ___, "calma": ___}
orden = "luz"
acciones[orden]___
```

**Salida esperada.**
```
La cueva se ilumina.
```

**Solución.** `{"luz": luz, "calma": calma}` y `acciones[orden]()`.

**Al superarla.**
La cueva se ilumina y, por primera vez, ven el fondo: un pasillo que sube.

**Imagen.**
- Un atril de piedra con un libro abierto; de sus páginas salen conjuros como luciérnagas.
- La cueva iluminada de golpe; Mia con el pergamino en alto.

---

#### Micro-misión R01-N09-P4 · Hechizos de una línea

```meta
lugar: La Cueva de los Ecos
personajes: Mia, Gheco, Tilo
carta: lambda | lambda x: expresión · función chica sin nombre · típico en sorted(lista, key=lambda x: x[1])
recompensa: xp 15, oro 15
imagen: R01-N09-P4
```

**Escena.**
Para cruzar el pasillo hay que enfrentar a las criaturas de la menos a la más fuerte. Tilo tiene la lista de criaturas con su vida.

**Gheco sugiere.**
`lambda c: c[1]` es una función de una línea, sin nombre. `sorted(lista, key=...)` usa esa función para saber **por qué valor** ordenar: acá, por la vida (la posición 1 de cada tupla).

**Desafío.** Ordená por vida, de menor a mayor.

```python
criaturas = [("murciélago", 8), ("goblin", 20), ("slime", 10)]
for nombre, vida in sorted(criaturas, key=___):
    print(nombre, vida)
```

**Salida esperada.**
```
murciélago 8
slime 10
goblin 20
```

**Solución.** `key=lambda c: c[1]`.

**Al superarla.**
Murciélago, slime, goblin: uno por uno, cada vez más fácil porque cada vez saben más. Al final del pasillo hay un cofre.

**Imagen.**
- Un pasillo de piedra que sube; tres siluetas de criaturas en fila de menor a mayor.
- Al final, un cofre que brilla.

---

#### Micro-misión R01-N09-P5 · Cofres dentro de cofres

```meta
lugar: La Cueva de los Ecos
personajes: Mia, Gheco, Tilo
carta: Recursión | una función que se llama a sí misma · siempre con un caso que termina
recompensa: xp 15, oro 20
item: Cofre de los Ecos
imagen: R01-N09-P5
```

**Escena.**
Tilo abre el cofre: adentro hay monedas **y otro cofre**. Y adentro de ese, monedas y otro cofre más. —¿Cuántas monedas hay en total?

**Gheco sugiere.**
Una función **recursiva** se llama a sí misma con algo más chico: si encuentra otro cofre (una lista), se cuenta a sí misma adentro. `isinstance(x, list)` pregunta si `x` es una lista. El caso que termina: los números se suman y listo.

**Desafío.** Completá la llamada recursiva.

```python
def contar(cofre):
    total = 0
    for cosa in cofre:
        if isinstance(cosa, list):
            total += ___
        else:
            total += cosa
    return total

cofre = [5, [3, [2, 1]], 4]
print(contar(cofre))
```

**Salida esperada.**
```
15
```

**Solución.** `contar(cosa)`.

**Al superarla.**
Quince monedas. El cofre más chico, del tamaño de una nuez, se queda con vos: cuando lo acercás al oído, repite lo último que dijiste.
Tu pergamino, mientras tanto, se enrolla solo: ya es tan largo que no encontrás nada. Arriba de la cueva, en la cima de las Terrazas, está **la Casa de los Tomos**.

**Imagen.**
- Una serie de cofres uno dentro de otro, abiertos como muñecas rusas, con monedas brillando en cada uno.
- Mia sostiene el cofre más pequeño junto a su oreja.
- El pergamino de Mia, larguísimo, enrollado en el piso.

---

> Después vienen las prácticas que corrige el docente (**M1** El grimorio de Mia, **M2** Ordenar la compañía, **M3** Las cámaras de la cueva, **E1** El archivo del escriba).

---

### R01-N10 · Módulos y paquetes

*La Casa de los Tomos, en la cima de las Terrazas. Mia, Gheco, Tilo y la Copista, que se mudó a cuidar los tomos («para tener un rato de silencio»).*

#### Micro-misión R01-N10-P1 · El tomo de los números

```meta
lugar: La Casa de los Tomos
personajes: Mia, Gheco, Tilo, la Copista
carta: import | import math · math.sqrt(16) · math.ceil(2.1) → 3 · math.pi
recompensa: xp 10, oro 10
imagen: R01-N10-P1
```

**Escena.**
—¡Ustedes! —La Copista los recibe entre estantes que llegan al techo—. Acá cada saber tiene su **tomo**. No hace falta escribirlo todo de nuevo: se pide prestado.
Tilo quiere saber cuántos viajes de balsa necesita para 21 pasajeros si entran 5 por viaje.

**Gheco sugiere.**
`import math` trae el tomo de matemática. Se usa con un punto: `math.ceil(x)` redondea **hacia arriba**, `math.sqrt(x)` es la raíz.

**Desafío.** Calculá los viajes redondeando hacia arriba.

```python
___
pasajeros = 21
lugares = 5
print(math.ceil(pasajeros / lugares))
```

**Salida esperada.**
```
5
```

**Solución.** `import math`.

**Al superarla.**
—Cinco viajes —dice Tilo—. Mi papá siempre decía cuatro y dejaba a uno en la orilla.

**Imagen.**
- Una biblioteca circular en la cima de las terrazas: estantes altísimos, tomos con lomos de colores, una cúpula con estrellas.
- La Copista (túnica lila, horquillas) baja un tomo con el símbolo π.
- Tilo contando con los dedos.

---

#### Micro-misión R01-N10-P2 · Traer solo lo que usás

```meta
lugar: La Casa de los Tomos
personajes: Mia, Gheco, Tilo, la Copista
carta: from … import | from statistics import mean · import algo as alias
recompensa: xp 10, oro 10
imagen: R01-N10-P2
```

**Escena.**
—No hace falta bajar el tomo entero si querés una sola página —dice la Copista—. Quiero el promedio de las vidas del Bestiario.

**Gheco sugiere.**
`from statistics import mean` trae **solo** `mean`, y se usa sin el prefijo: `mean(lista)`.

**Desafío.** Traé `mean` y calculá el promedio.

```python
vidas = [10, 20, 8, 30]
print(mean(vidas))
```

**Salida esperada.**
```
17
```

**Solución.** `from statistics import mean`.

**Al superarla.**
La Copista anota «17» en una ficha y la guarda en el tomo del Bestiario. —Promedio de criaturas: diecisiete. Lindo número.

**Imagen.**
- Una sola página que sale volando de un tomo cerrado hacia las manos de Mia.
- La Copista anotando en una ficha.

---

#### Micro-misión R01-N10-P3 · El calendario del viaje

```meta
lugar: La Casa de los Tomos
personajes: Mia, Gheco, Tilo, la Copista
carta: datetime | from datetime import date, timedelta · date(2026, 10, 7) + timedelta(days=30) · .strftime("%d/%m/%Y")
recompensa: xp 15, oro 15
imagen: R01-N10-P3
```

**Escena.**
—Si salimos hoy, el 7 de octubre, y el viaje a la Gran Biblioteca dura 30 días… ¿qué día llegamos? —pregunta Mia.

**Gheco sugiere.**
`date(año, mes, día)` es una fecha y `timedelta(days=30)`, una duración: se pueden sumar. `.strftime("%d/%m/%Y")` la muestra como día/mes/año.

**Desafío.** Calculá la llegada y mostrala en formato argentino.

```python
from datetime import date, timedelta
salida = date(2026, 10, 7)
llegada = ___
print(llegada.strftime(___))
```

**Salida esperada.**
```
06/11/2026
```

**Solución.** `salida + timedelta(days=30)` y `"%d/%m/%Y"`.

**Al superarla.**
—Seis de noviembre —dice la Copista—. Si no se demoran en el Paso. —Y se queda callada, mirando por la ventana.

**Imagen.**
- Un calendario de piedra con días que pasan como hojas al viento.
- La Copista mira por la ventana con preocupación.

---

#### Micro-misión R01-N10-P4 · El vuelto exacto

```meta
lugar: La Casa de los Tomos
personajes: Mia, Gheco, Tilo, la Copista
carta: Decimal | from decimal import Decimal · Decimal("0.1") con comillas · cuentas de dinero exactas
recompensa: xp 10, oro 10
imagen: R01-N10-P4
```

**Escena.**
Te acordás del vuelto de Baldo: `0.1 + 0.2` no daba `0.3`. La Copista sonríe. —Para la plata hay un tomo especial.

**Gheco sugiere.**
`Decimal("0.1")` guarda el decimal **exacto** (escribilo entre comillas). Con `Decimal`, `0.1 + 0.2` da justo `0.3`.

**Desafío.** Rehacé la cuenta de Baldo con `Decimal`.

```python
a = 0.1
b = 0.2
print(a + b)
print(a + b == 0.3)
```

**Salida esperada.**
```
0.3
True
```

**Solución.** `from decimal import Decimal`, `Decimal("0.1")`, `Decimal("0.2")` y comparar con `Decimal("0.3")`.

**Al superarla.**
—La próxima vez que veas a Baldo, decíselo —ríe Gheco—. Va a tener que inventar otra excusa.

**Imagen.**
- Dos monedas que se suman en el aire dando un 0.3 perfecto, sin grietas.
- Gheco riéndose a carcajadas.

---

#### Micro-misión R01-N10-P5 · Fichas con nombre

```meta
lugar: La Casa de los Tomos
personajes: Mia, Gheco, Tilo, la Copista
carta: namedtuple | from collections import namedtuple · Criatura = namedtuple("Criatura", "nombre vida") · c.vida
recompensa: xp 10, oro 10
item: Estante Portátil
imagen: R01-N10-P5
```

**Escena.**
—Las tuplas son prolijas —dice la Copista—, pero `c[1]` no dice nada. ¿No sería mejor `c.vida`?

**Gheco sugiere.**
`namedtuple` crea un tipo de tupla con **nombres de campo**: `Criatura("slime", 10)` y después `c.nombre`, `c.vida`.

**Desafío.** Creá el tipo y mostrá los campos por su nombre.

```python
from collections import namedtuple
Criatura = ___
c = Criatura("slime", 10)
print(f"{c.nombre} tiene {c.vida} de vida")
```

**Salida esperada.**
```
slime tiene 10 de vida
```

**Solución.** `namedtuple("Criatura", "nombre vida")`.

**Al superarla.**
La Copista te deja ordenar tu pergamino en **tomos**: uno de textos, uno de listas, uno de hechizos. Por fin encontrás todo.

**Imagen.**
- El pergamino de Mia se separa en tres tomos pequeños que se acomodan en un estante portátil.
- La Copista aprueba con la cabeza.

---

#### Micro-misión R01-N10-P6 · El tomo firmado

```meta
lugar: La Casa de los Tomos
personajes: Mia, Gheco, Tilo, la Copista
carta: __name__ | if __name__ == "__main__": · lo de adentro corre solo si ejecutás ESE archivo, no si lo importan
recompensa: xp 15, oro 20
imagen: R01-N10-P6
```

**Escena.**
En el estante más alto, Tilo encuentra un tomo finito con **el vitral** en el lomo. Es un módulo, escrito con la letra clarísima del viajero. Termina con una línea que Mia no entiende: `if __name__ == "__main__":`.

**Gheco sugiere.**
Cada archivo tiene un nombre interno: `__name__`. Si lo **ejecutás**, vale `"__main__"`. Si otro archivo lo **importa**, vale el nombre del archivo. Por eso `if __name__ == "__main__":` separa «lo que hago si me ejecutan» de «lo que presto si me importan».

**Desafío.** Ejecutalo así como está: el pergamino es el archivo que se ejecuta. Completá la condición.

```python
def saludo():
    return "Para quien llegue."

if __name__ == ___:
    print(saludo())
```

**Salida esperada.**
```
Para quien llegue.
```

**Solución.** `"__main__"`.

**Al superarla.**
*Para quien llegue.* Es la misma frase que todavía no pudiste leer en la marca de agua de tu pergamino; lo sentís aunque no sepas por qué. Guardás el tomo en el grimorio: **la segunda nota del viajero**.
Por la ventana de la Casa se ve el **Paso** que sube al Bastión de las Escamas. Algo enorme se mueve ahí. Tiene muchas cabezas.

**Se abre:** la **segunda nota del viajero** en el grimorio.

**Imagen.**
- Un tomo finito con un vitral en el lomo, abierto en las manos de Mia; la última línea brilla.
- Por la ventana circular, a lo lejos, la silueta de una hidra de muchas cabezas sobre un paso de montaña.
- Tilo y Gheco pegados al vidrio.

---

> Después vienen las prácticas que corrige el docente (**M1** Tu propio módulo, **M2** El calendario de la aventura, **M3** Romper el círculo, **E1** El módulo de los comerciantes). Los módulos propios (varios archivos) se practican en M1, en la compu.

---

### R01-N11 · Jefe: la Hidra de las Mil Runas

*El Paso de la Hidra, entre las Terrazas y el Bastión. Mia, Gheco, Tilo y {mentor}, que mira desde lejos: este combate es de Mia. Cada cabeza de la Hidra es un error del Valle; cortarla con un hechizo mal escrito le hace crecer dos.*

#### Micro-misión R01-N11-P1 · La cabeza del esqueleto

```meta
lugar: El Paso de la Hidra
personajes: Mia, Gheco, Tilo
criatura: esqueleto
carta: Leer un NameError | «name 'x' is not defined»: una variable mal escrita o usada antes de crearla
recompensa: xp 15, oro 15
imagen: R01-N11-P1
```

**Escena.**
La primera cabeza de la Hidra tiene forma de calavera. Grita `NameError` y tu hechizo de luz se apaga.

**Gheco sugiere.**
Leé el error de abajo hacia arriba: dice **qué nombre** no existe. Casi siempre es una letra cambiada o una mayúscula.

**Desafío.** Encontrá el nombre mal escrito y corregilo.

```python
def ataque(fuerza, arma):
    return fuerza + arma

fuerza_mia = 12
arma_mia = 5
print(ataque(fuerza_mia, arma_Mia))
```

**Salida esperada.**
```
17
```

**Solución.** `arma_Mia` tenía una mayúscula: es `arma_mia`.

**Al superarla.**
La cabeza de calavera se deshace. La Hidra ruge con las que le quedan.

**Imagen.**
- La Hidra de las Mil Runas en el paso de montaña: cuerpo de serpiente gigante, cabezas distintas; una con forma de calavera grita «NameError».
- Mia, firme, con el pergamino en alto; Tilo detrás con la pértiga; Gheco ilumina.

---

#### Micro-misión R01-N11-P2 · La cabeza del goblin

```meta
lugar: El Paso de la Hidra
personajes: Mia, Gheco, Tilo
criatura: goblin
carta: Leer un TypeError | «can only concatenate str (not "int") to str»: mezclaste texto y número
recompensa: xp 15, oro 15
imagen: R01-N11-P2
```

**Escena.**
La segunda cabeza es verde y flaca, con sonrisa de goblin. Tu hechizo de daño explota en chispas: `TypeError`.

**Gheco sugiere.**
Un `TypeError` dice que mezclaste tipos que no se combinan, como texto y número con `+`. La solución más clara: un f-string.

**Desafío.** Arreglá el mensaje del daño.

```python
danio = 17
print("Le hacés " + danio + " de daño")
```

**Salida esperada.**
```
Le hacés 17 de daño
```

**Solución.** `print(f"Le hacés {danio} de daño")` (o `str(danio)`).

**Al superarla.**
La cabeza del goblin cae. Tilo grita de alegría y la Hidra lo mira; él se esconde detrás de vos.

**Imagen.**
- Una cabeza verde de la Hidra con sonrisa de goblin explota en chispas.
- Tilo festejando y escondiéndose a la vez.

---

#### Micro-misión R01-N11-P3 · La cabeza del orco

```meta
lugar: El Paso de la Hidra
personajes: Mia, Gheco, Tilo
criatura: orco
carta: Leer un IndexError | «list index out of range»: pediste una posición que no existe (se cuenta desde 0)
recompensa: xp 15, oro 15
imagen: R01-N11-P3
```

**Escena.**
La tercera cabeza tiene colmillos de orco. Para cortarla hay que golpear **cada** cabeza de una lista, pero tu bucle siempre se pasa de una.

**Gheco sugiere.**
Si una lista tiene 3 elementos, las posiciones son 0, 1 y 2. `range(len(lista) + 1)` se pasa. Lo más simple: recorrer la lista directamente, sin posiciones.

**Desafío.** Arreglá el bucle.

```python
cabezas = ["orco", "ogro", "hidra"]
for i in range(len(cabezas) + 1):
    print(f"Golpe a la cabeza {cabezas[i]}")
```

**Salida esperada.**
```
Golpe a la cabeza orco
Golpe a la cabeza ogro
Golpe a la cabeza hidra
```

**Solución.** `for cabeza in cabezas:` (o `range(len(cabezas))`).

**Al superarla.**
La cabeza de orco cae. Quedan dos: la del ogro y la central, la más grande.

**Imagen.**
- Una cabeza con colmillos de orco cae; las cabezas restantes se agitan.
- Mia corre entre las rocas del paso.

---

#### Micro-misión R01-N11-P4 · La cabeza del ogro

```meta
lugar: El Paso de la Hidra
personajes: Mia, Gheco, Tilo
criatura: ogro
carta: Errores de lógica | el programa corre sin errores… y da mal · se vencen probando con un caso que sabés calcular
recompensa: xp 20, oro 20
imagen: R01-N11-P4
```

**Escena.**
La cabeza del ogro no grita. Tu hechizo corre, no explota, no da error… y la cabeza no cae. El promedio de tus golpes da cualquier cosa.

**Gheco sugiere.**
Un **ogro** no deja traceback: el programa termina tranquilo y el resultado está mal. Se vence **probando**: con 10, 20 y 30, el promedio tiene que dar 20. ¿Da?

**Desafío.** Encontrá el error de lógica.

```python
golpes = [10, 20, 30]
promedio = sum(golpes) / len(golpes) + 1
print(f"Promedio: {promedio}")
```

**Salida esperada.**
```
Promedio: 20.0
```

**Solución.** Sobraba el `+ 1`: el promedio es `sum(golpes) / len(golpes)`.

**Al superarla.**
La cabeza del ogro se derrumba en silencio, como cayó cada uno de sus errores: sin avisar.

**Imagen.**
- Una cabeza de ogro de la Hidra se derrumba sin ruido.
- Mia, concentrada, comprueba una cuenta en el pergamino con el dedo.

---

#### Micro-misión R01-N11-P5 · La cabeza central

```meta
lugar: El Paso de la Hidra
personajes: Mia, Gheco, Tilo, Ofidia
criatura: dragón
carta: Dividir para vencer | un problema grande = funciones chicas, cada una probada
recompensa: xp 25, oro 30
imagen: R01-N11-P5
```

**Escena.**
Queda la cabeza central, la más grande. Cada vez que le pegás con un hechizo largo y enredado, le crecen dos. {mentor}, desde lejos, dice una sola frase:
—Dividí.

**Gheco sugiere.**
Un problema grande se vence **en partes**: una función que hace una sola cosa, otra que hace otra, y una que las junta. Cada parte se prueba sola.

**Desafío.** Completá las dos funciones chicas; la tercera ya las usa.

```python
def danio(fuerza, arma):
    ___

def sigue_viva(vida):
    ___

def combate(vida, fuerza, arma):
    turnos = 0
    while sigue_viva(vida):
        vida -= danio(fuerza, arma)
        turnos += 1
    return turnos

print(f"Cae en {combate(100, 12, 5)} turnos")
```

**Salida esperada.**
```
Cae en 6 turnos
```

**Solución.** `return fuerza + arma` y `return vida > 0`.

**Al superarla.**
Seis golpes limpios, uno detrás de otro. La Hidra cae y el Paso queda en silencio.
Mirás tu túnica: **las runas del borde, desde los pies hasta la cintura, brillan en violeta**. Ya no se apagan.
{mentor} se acerca despacio. —En el Valle bajo aprendiste lo más difícil: que se aprende **escribiendo**. Arriba está el Bastión de las Escamas, y adentro, la Gran Biblioteca. Ahí te esperan cosas que no vas a poder leer sin equivocarte.

**Imagen.**
- La cabeza central de la Hidra se desploma en el paso de montaña; polvo y runas que se apagan.
- Mia de pie, con la túnica encendida en violeta desde los pies hasta la cintura.
- Ofidia se acerca; Tilo y Gheco abrazados de alegría.
- Al fondo, el Bastión de las Escamas recortado contra la aurora.

---

> Después vienen las prácticas del jefe, que corrige el docente (**M1** La tienda del Valle, **M2** El informe de la batalla, **E1** La libreta del almacén). Al aprobarlas: la **primera parte de la túnica encendida**, el ítem raro del jefe y el Paso abierto hacia el Bastión de las Escamas.

---
