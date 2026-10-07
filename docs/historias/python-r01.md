# Python · Acto I (R01): la planilla de continuidad y las micro-misiones

Nivel 3 y 4 del método ([../JUEGO.md](../JUEGO.md) § 10) para **la Clase 0 y la rama 1** del arco de Mia ([python.md](python.md)). Personajes y aspecto: [PERSONAJES.md](PERSONAJES.md).

**Estado:**
- La planilla (§ 2) cubre la Clase 0 y los 11 nodos.
- Las micro-misiones completas (§ 3) están escritas para la **Clase 0** y el **nodo 1**, como muestra del formato y del tono.
- Con el OK del docente se escriben las de los nodos 2 a 11, siguiendo la planilla.
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
