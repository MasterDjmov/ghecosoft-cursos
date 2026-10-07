# Python · Acto I (R01): la planilla de continuidad y las micro-misiones

Nivel 3 y 4 del método ([../JUEGO.md](../JUEGO.md) § 10) para **la Clase 0 y la rama 1** del arco de Mia ([python.md](python.md)). Personajes y aspecto: [PERSONAJES.md](PERSONAJES.md).

**Estado:**
- La planilla (§ 2) cubre la Clase 0 y los 11 nodos.
- Las micro-misiones completas (§ 3) están escritas para la **Clase 0** y los **nodos 1 a 4** (26 en total).
- Faltan los nodos 5 a 11, siguiendo la planilla.
- Las salidas esperadas de los nodos 2 a 4 salen de **ejecutar cada solución**, no de escribirlas a mano. El generador también comprueba que el código inicial **no** dé ya la salida esperada.
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
| **R01-N02** | El Puente del Juicio | Mia, Gheco, el Guardián del Puente (una serpiente de piedra) | | | |
| P1 | ídem | ídem | aritméticos, `//`, `%` | Calcula su daño para la primera prueba | |
| P2 | ídem | ídem | asignación aumentada | Lleva la cuenta de los golpes | |
| P3 | ídem | ídem | comparaciones (también encadenadas) | Compara su fuerza con la del guardián | |
| P4 | ídem | ídem | `and`, `or`, `not`, cortocircuito | «Nivel 5 o más, con llave o magia, sin maldición» | |
| P5 | ídem | ídem | `in`, `is`, precedencia | El puente se abre | **Llave del Puente** |
| **R01-N03** | La Casa de los Copistas | + la Copista | | | |
| P1 | ídem | ídem | crear textos, escapes, multilínea | Carteles desordenados | |
| P2 | ídem | ídem | índices y cortes | Mensajes que solo se leen al revés | |
| P3 | ídem | ídem | inmutables, operar con textos | | |
| P4 | ídem | ídem | métodos, `split`/`join` | Ordena los carteles | |
| P5 | ídem | ídem | alinear, Unicode | En un cartel viejo aparece **la firma del vitral** | nota del viajero (1) |
| **R01-N04** | El Laberinto de las Siete Salas | Mia, Gheco | | | |
| P1 | ídem | ídem | `if`/`elif`/`else` | Sala 1: trampa o cofre | |
| P2 | ídem | ídem | `while` | Sala 2: avanzar hasta la luz | |
| P3 | ídem | ídem | `for` y `range` | Salas 3–4: contar losas | |
| P4 | ídem | ídem | `break`/`continue`, `for…else` | Sala 5: huir del jefe | |
| P5 | ídem | ídem | `match` | Sala 6: la puerta de los comandos | |
| P6 | ídem | ídem | `random` con semilla | Sala 7: los dados de la salida | **Espiral de Junco** |
| **R01-N05** | La Posada de la Serpiente | + **Tilo** | | Tilo se suma | |
| P1 | ídem | ídem | crear listas, índices | Anota quién viaja | |
| P2 | ídem | ídem | modificar, `sort`/`sorted` | La mochila | |
| P3 | ídem | ídem | recorrer, `enumerate` | | |
| P4 | ídem | ídem | comprehension | | |
| P5 | ídem | ídem | listas anidadas | El mapa del camino | |
| P6 | ídem | ídem | tuplas, desempaquetado, `match` con secuencias | Rumor: «una espadachina de pelo corto bajó a las Forjas». **Se abren las expediciones:** el Profe aparece con su tablero | **Morral de la Posada** |
| **R01-N06** | La Ermita del Bestiario | + el Ermitaño | | | |
| P1 | ídem | ídem | crear diccionarios, `get` | | **el Bestiario** (se abre la ficha de criaturas) |
| P2 | ídem | ídem | modificar, `setdefault` | | |
| P3 | ídem | ídem | recorrer | | |
| P4 | ídem | ídem | dict comprehension, anidados | | |
| P5 | ídem | ídem | contar, `Counter` | | |
| P6 | ídem | ídem | conjuntos | El Ermitaño advierte del troll | |
| **R01-N07** | La Cueva del Troll, bajo el puente viejo | Mia, Tilo, Gheco, el troll | | | |
| P1 | ídem | ídem | alias | **Punto medio:** Tilo cae y la anotación «de respaldo» también lo pierde | |
| P2 | ídem | ídem | reasignar no es modificar | | |
| P3 | ídem | ídem | `==` frente a `is` | | |
| P4 | ídem | ídem | copia superficial y su trampa | | |
| P5 | ídem | ídem | `deepcopy` | Vence al troll | **Espejo del Troll** |
| **R01-N08** | Las Terrazas de las Funciones | Mia, Tilo (lastimado), Gheco, Ofidia | | | |
| P1 | ídem | ídem | `def` y llamar | Cura a Tilo | |
| P2 | ídem | ídem | parámetros y `return` | | |
| P3 | ídem | ídem | por nombre, valores por defecto | | |
| P4 | ídem | ídem | devolver varios, `*args`/`**kwargs` | | |
| P5 | ídem | ídem | el default mutable | | |
| P6 | ídem | ídem | dividir en funciones chicas | Tilo se cura | **Pociones de Curación** |
| **R01-N09** | La Cueva de los Ecos | Mia, Tilo, Gheco | | | |
| P1 | ídem | ídem | alcance (LEGB), `global` | | |
| P2 | ídem | ídem | `nonlocal` | | |
| P3 | ídem | ídem | funciones como objetos, tabla de acciones | | |
| P4 | ídem | ídem | `lambda` | | |
| P5 | ídem | ídem | recursión | Cofres dentro de cofres | **Cofre de los Ecos** |
| **R01-N10** | La Casa de los Tomos | + la bibliotecaria de los Tomos | | | |
| P1 | ídem | ídem | `math`, `random` | | |
| P2 | ídem | ídem | `statistics`, `datetime` | | |
| P3 | ídem | ídem | `decimal`, `namedtuple` | | |
| P4 | ídem | ídem | módulos propios | | |
| P5 | ídem | ídem | paquetes | En el estante viejo, un **módulo firmado con el vitral**. Desde la Casa se ve algo enorme en el Paso | **Estante Portátil**, nota del viajero (2) |
| **R01-N11** | El Paso de la Hidra | Mia, Tilo, Gheco, Ofidia | | | |
| P1–P3 | ídem | ídem | repaso por partes: cada cabeza es un error del acto | Jefe: la Hidra | |
| (cierre) | ídem | ídem | | Vence: se enciende la **primera parte de la túnica**; el Paso se abre al Bastión | ítem raro |

> En el Acto I la bibliotecaria de la Casa de los Tomos **no es Sila** (Sila está en la Gran Biblioteca, Acto II). Si se quiere ahorrar un personaje, puede ser **la Copista**, que se mudó a cuidar los tomos.

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
Mia · aprendiz de maga · 5 escamas · le faltan 5 para romper el primer sello
```

**Solución.**
```python
print(f"{nombre} · aprendiz de maga · {escamas} escamas · le faltan {10 - escamas} para romper el primer sello")
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
a, b, c = "12", "3.5", "7"
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
carta: Métodos de texto | strip · lower/upper/title · replace · split → lista · " ".join(lista)
recompensa: xp 15, oro 15
imagen: R01-N03-P4
```

**Escena.**
El cartel más feo de todos es el de una oficina de la Aldea: tiene espacios por todos lados y mayúsculas mezcladas, como si lo hubiera escrito un goblin.
`"  oFIcina    DE   lAs    RUNAS  "`
—Necesito que quede *Oficina De Las Runas*, con un solo espacio entre palabras.

**Gheco sugiere.**
`split()` sin nada parte el texto en **palabras** y se come todos los espacios de más (te da una lista: las listas se ven en el nodo 5). `" ".join(palabras)` las vuelve a unir con un espacio. Y `.title()` pone la primera letra de cada palabra en mayúscula.

**Desafío.** Limpiá el cartel en una sola línea encadenando métodos.

```python
cartel = "  oFIcina    DE   lAs    RUNAS  "
limpio = cartel
print(limpio)
```

**Salida esperada.**
```
Oficina De Las Runas
```

**Solución.** `limpio = " ".join(cartel.split()).title()`.

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
La quinta sala tiene seis puertas. Detrás de alguna duerme un **ogro**. La runa dice: *«Revisá las puertas. Las vacías, salteálas. Si encontrás al ogro, no pelees: salí corriendo.»*
—Y si revisamos todas y no está… —susurra Gheco— mejor todavía.

**Gheco sugiere.**
Dentro de un bucle, `continue` **salta** directo a la vuelta siguiente, y `break` **corta** el bucle entero. Un `for` puede tener `else`: corre **solo si el bucle terminó sin `break`** («busqué en todos lados y no estaba»).

**Desafío.** Las puertas vacías se saltean con `continue`; si aparece el ogro, `break`. Completá.

```python
puertas = ["vacía", "vacía", "cofre", "vacía", "ogro", "cofre"]
for numero, puerta in enumerate(puertas, start=1):
    if puerta == "vacía":
        ___
    if puerta == "ogro":
        print(f"Puerta {numero}: ¡el ogro! A correr.")
        ___
    print(f"Puerta {numero}: {puerta}")
else:
    print("No había ningún ogro.")
```

**Salida esperada.**
```
Puerta 3: cofre
Puerta 5: ¡el ogro! A correr.
```

**Solución.** `continue` y `break`. (Las listas como `puertas` y `enumerate` se ven a fondo en el nodo 5: acá alcanza con saber que el `for` recorre las puertas de a una.)

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
tiradas = [random.randint(1, 6) for _ in range(3)]
print(f"Tiradas: {tiradas}")
suma = sum(tiradas)
print(f"Suma: {suma}")
print("¡Salís del Laberinto!" if suma > 8 else "Seguís adentro.")
```

**Salida esperada.**
```
Tiradas: [3, 2, 4]
Suma: 9
¡Salís del Laberinto!
```

**Solución.** `random.seed(7)`. (La línea de las tiradas usa una *comprehension* y `sum`, que se ven en el nodo 5; la última, el `if` en una línea: `a if condición else b`.)

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
