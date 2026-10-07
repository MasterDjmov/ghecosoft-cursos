# RAMA R03 · Iteración y calidad: la Torre del Reloj

```meta
tipo: tronco
posicion: 3
```

## R03-N01 · Iteradores y generadores

```meta
tipo: tema
padre: R02-N05
precio: 10
criatura: ogro
temas: func.iteradores
```

### Crónica

Las notas del viajero, ya enteras, terminaban así: «la Torre del Reloj guarda el tiempo del Valle; yo le debo una pieza». La **Torre del Reloj** se levanta en la Gran Ciudadela de {mentor}. En su primer piso, de un portal no paran de salir enemigos: slimes, murciélagos, orcos… Nadie sabe cuántos son. Quizás infinitos.

—No hace falta conocerlos a todos de antemano —dice Gheco—. Pedilos **de a uno**, cuando los necesites. Así funciona un **generador**.

Arriba, **Maese Horas**, el relojero, cuenta que el gran reloj atrasa desde que se perdió una pieza.

### Objetivos

- Entender la diferencia entre un iterable y un iterador (`iter`, `next`, `StopIteration`).
- Escribir generadores con `yield`, también infinitos.
- Consumirlos con `for`, `islice`, `takewhile` y expresiones generadoras.

### Antes de empezar

Listas y bucles (R01), funciones (R01-N08) y clases (R02-N01).

### Explicación

#### Iterable e iterador

Un **iterable** es cualquier cosa que se puede recorrer con `for`: listas, textos, diccionarios, archivos. Un **iterador** es el objeto que hace el recorrido: sabe por dónde va.

```python
it = iter(["Mia", "Tilo"])   # pedirle al iterable un iterador
next(it)                      # "Mia"
next(it)                      # "Tilo"
next(it)                      # StopIteration: se terminó
```

Un `for` hace exactamente eso por dentro: pide un iterador y llama a `next` hasta el `StopIteration`.

#### Generadores: funciones con `yield`

```python
def cuenta_regresiva(n):
    while n > 0:
        yield n
        n -= 1
```

- Al llamar a `cuenta_regresiva(3)` **no se ejecuta nada**: se obtiene un generador (un iterador).
- Cada `next()` ejecuta el código hasta el próximo `yield`, entrega ese valor y **se pausa ahí**, recordando todas sus variables.
- Cuando la función termina, el generador lanza `StopIteration` (y el `for` se detiene).

#### Perezosos e infinitos

Un generador **no arma la lista entera**: produce cada valor cuando se lo piden. Por eso puede ser **infinito** (`while True: yield …`) sin llenar la memoria. Solo hay que consumir lo necesario:

- `itertools.islice(gen, 5)`: los primeros 5.
- `itertools.takewhile(condicion, gen)`: mientras se cumpla la condición.
- `next(gen)`: de a uno.

#### Expresiones generadoras

Como una comprehension, pero con **paréntesis**: `(x * x for x in datos)`. No arma la lista, así que conviene adentro de `sum`, `max`, `any` o `all`:

```python
total = sum(len(o) for o in oleadas)
```

#### Se gastan

Un generador se recorre **una sola vez**: después de consumirlo, está vacío. Si necesitás recorrerlo de nuevo, creá otro (o guardá los valores en una lista).

#### Un iterable propio

Si una clase define `__iter__` como generador, se puede recorrer con `for` todas las veces que quieras (cada `for` crea un generador nuevo).

### Código de ejemplo

```python
"""Iteradores y generadores: valores de a uno, cuando se piden."""

import random
from itertools import islice, takewhile

# =========================================================
# Iterable e iterador
# =========================================================
compania = ["Mia", "Tilo", "Sila"]
it = iter(compania)          # un iterador: recuerda por dónde va
print(next(it), next(it), next(it))
try:
    next(it)
except StopIteration:
    print("se terminó: StopIteration")


# =========================================================
# Generador: una función con yield
# =========================================================
def cuenta_regresiva(n):
    while n > 0:
        yield n              # entrega n y se PAUSA acá hasta el próximo pedido
        n -= 1
    yield "¡ya!"


for valor in cuenta_regresiva(3):
    print(valor)


# =========================================================
# Generador INFINITO: se consume solo lo que hace falta
# =========================================================
def oleadas(semilla=0):
    azar = random.Random(semilla)
    tipos = ["slime", "murciélago", "orco", "esqueleto"]
    numero = 1
    while True:
        enemigos = [azar.choice(tipos) for _ in range(2 + numero // 2)]
        yield {"numero": numero, "enemigos": enemigos, "jefe": numero % 5 == 0}
        numero += 1


gen = oleadas(semilla=1)
for _ in range(3):
    print(next(gen))

# islice: tomar N; takewhile: mientras se cumpla
tranquilas = list(islice((o for o in oleadas(2) if not o["jefe"]), 3))
print("tranquilas:", [o["numero"] for o in tranquilas])
chicas = list(takewhile(lambda o: len(o["enemigos"]) <= 3, oleadas(3)))
print("oleadas chicas seguidas:", [o["numero"] for o in chicas])

# Expresión generadora: como una comprehension, pero sin armar la lista
print("enemigos en 10 oleadas:", sum(len(o["enemigos"]) for o in islice(oleadas(4), 10)))

# enumerate y zip también son iteradores
for i, (nombre, vida) in enumerate(zip(["Mia", "Tilo", "Sila"], [120, 90, 150]), start=1):
    print(f"{i}. {nombre}: {vida} de vida")
```

### Salida esperada

```
Mia Tilo Sila
se terminó: StopIteration
3
2
1
¡ya!
{'numero': 1, 'enemigos': ['murciélago', 'slime'], 'jefe': False}
{'numero': 2, 'enemigos': ['orco', 'slime', 'esqueleto'], 'jefe': False}
{'numero': 3, 'enemigos': ['esqueleto', 'esqueleto', 'esqueleto'], 'jefe': False}
tranquilas: [1, 2, 3]
oleadas chicas seguidas: [1, 2, 3]
enemigos en 10 oleadas: 45
1. Mia: 120 de vida
2. Tilo: 90 de vida
3. Sila: 150 de vida
```

### ¿Para qué sirve?

Los generadores permiten procesar cosas **más grandes que la memoria**: leer un archivo de registros de varios gigas línea por línea, recorrer los resultados de una base de datos de a tandas, procesar un video cuadro por cuadro o un flujo de mensajes que no termina nunca (un chat, los sensores de una fábrica). También son la forma natural de escribir "secuencias" (ids, turnos, oleadas).

### Errores habituales

**Ogro: recorrer dos veces el mismo generador**: la segunda vez está vacío y no hay ningún error, simplemente no pasa nada.

```python
pares = (x for x in range(6) if x % 2 == 0)
print(sum(pares))    # 6
print(sum(pares))    # 0 (¡ya estaba gastado!)
```

**Ogro: un generador infinito sin corte**: `list(oleadas())` no termina nunca (en la plataforma se corta a los 5 segundos). Usá `islice` o `takewhile`.

**Goblin: pedir un índice a un generador**: `gen[0]` da `TypeError: 'generator' object is not subscriptable`. Si necesitás posiciones, convertilo en lista (o usá `islice`).

**Ogro: olvidar el `yield`** y poner `return`: la función devuelve un solo valor y termina.

### Micro-misión R03-N01-P1 · De a uno

```meta
lugar: La Torre del Reloj: el primer piso
personajes: Mia, Gheco, Tilo
carta: iter y next | it = iter(lista) · next(it) da el siguiente · al final: StopIteration
recompensa: xp 10, oro 10
```

#### Escena
La Torre del Reloj se levanta en el centro de la Gran Ciudadela, con sus engranajes a la vista. En el primer piso, de un portal no paran de salir enemigos.
—No los mires a todos juntos —dice Gheco—. Pedilos **de a uno**.

#### Gheco sugiere
`iter(lista)` te da un **iterador**: algo que sabe por dónde va. Cada `next(it)` te da el siguiente. Un `for` hace eso por dentro.

#### Desafío
Pedí los dos primeros enemigos de a uno.

#### Código inicial
```python
enemigos = ["slime", "murciélago", "orco"]
it = iter(enemigos)
print(___(it))
print(___(it))
```

#### Salida esperada
```
slime
murciélago
```

#### Solución
```python
enemigos = ["slime", "murciélago", "orco"]
it = iter(enemigos)
print(next(it))
print(next(it))
```

#### Al superarla
Un slime y un murciélago salen del portal, uno detrás del otro, y los esperás tranquila. Tilo, a tu lado, ya tiene la pértiga lista para el tercero.

#### Imagen
- El primer piso de la Torre del Reloj: engranajes gigantes en las paredes y un portal de luz en el centro.
- Un slime y un murciélago salen del portal en fila.
- Mia con el pergamino; Tilo con la pértiga del farol verde en alto.

### Micro-misión R03-N01-P2 · El portal que se pausa

```meta
lugar: La Torre del Reloj: el primer piso
personajes: Mia, Gheco, Tilo
carta: Generador | def portal(): ... yield valor · entrega uno y se PAUSA · recuerda sus variables
recompensa: xp 10, oro 10
```

#### Escena
—Este portal funciona como un hechizo que se **pausa** —dice Gheco—. Entrega un enemigo, se queda quieto, y cuando le pedís otro, sigue desde donde estaba.

#### Gheco sugiere
Una función con `yield` es un **generador**. Llamarla no ejecuta nada: cada vuelta del `for` corre hasta el próximo `yield`, entrega ese valor y se pausa ahí.

#### Desafío
Hacé que el portal **entregue** cada oleada en lugar de terminar.

#### Código inicial
```python
def oleadas(n):
    while n > 0:
        ___ n
        n -= 1

for oleada in oleadas(3):
    print(f"Oleada {oleada}")
print("El portal descansa")
```

#### Salida esperada
```
Oleada 3
Oleada 2
Oleada 1
El portal descansa
```

#### Solución
```python
def oleadas(n):
    while n > 0:
        yield n
        n -= 1

for oleada in oleadas(3):
    print(f"Oleada {oleada}")
print("El portal descansa")
```

#### Al superarla
Tres oleadas, cuenta regresiva, y el portal se apaga un momento. Tilo se sienta en el piso, resoplando.

#### Imagen
- El portal se apaga un instante; en el aire, una cuenta regresiva de luz: 3, 2, 1.
- Tilo sentado en el piso, resoplando; Gheco le abanica la cara con la cola.

### Micro-misión R03-N01-P3 · Quizás infinitos

```meta
lugar: La Torre del Reloj: el primer piso
personajes: Mia, Gheco, Tilo
carta: islice | while True: yield ... · itertools.islice(gen, 5) toma solo 5 · lo infinito no llena la memoria
recompensa: xp 15, oro 15
```

#### Escena
El portal se vuelve a encender, y esta vez no para.
—¿Cuántos son? —pregunta Tilo.
—Quizás infinitos —dice Gheco—. No importa: tomá **los que necesitás**.

#### Gheco sugiere
Un generador puede no terminar nunca (`while True:`). No pasa nada mientras **consumas solo lo necesario**: `itertools.islice(gen, 5)` toma los primeros 5.

#### Desafío
Tomá solo los primeros 5 del portal infinito.

#### Código inicial
```python
from itertools import islice

def portal():
    while True:
        yield "slime"
        yield "murciélago"

for enemigo in ___(portal(), 5):
    print(enemigo)
```

#### Salida esperada
```
slime
murciélago
slime
murciélago
slime
```

#### Solución
```python
from itertools import islice

def portal():
    while True:
        yield "slime"
        yield "murciélago"

for enemigo in islice(portal(), 5):
    print(enemigo)
```

#### Al superarla
Cinco y listo. El portal sigue echando enemigos, pero vos ya no le pedís más, y se quedan del otro lado, esperando.

#### Imagen
- Un portal que sigue brillando, con una fila infinita de siluetas esperando del otro lado.
- Cinco enemigos vencidos en el piso, ordenados como fichas.

### Micro-misión R03-N01-P4 · Sumar sin guardar

```meta
lugar: La Torre del Reloj: el primer piso
personajes: Mia, Gheco, Tilo
carta: Expresión generadora | sum(v for v in vidas if v > 20) · como una comprehension, pero sin armar la lista
recompensa: xp 10, oro 10
```

#### Escena
—Necesito saber cuánta vida tienen los fuertes —dice Tilo—, los de más de 20. Pero no me hagas otra lista, que ya no me entra nada en la cabeza.

#### Gheco sugiere
Una **expresión generadora** es una comprehension con paréntesis: `(v for v in vidas)`. No arma la lista; va dando los valores de a uno. Adentro de `sum`, `max` o `any` ni siquiera hacen falta los paréntesis extra.

#### Desafío
Sumá solo las vidas de más de 20, sin armar una lista.

#### Código inicial
```python
vidas = [12, 30, 8, 45, 25]
total = sum(___)
print(f"Vida de los fuertes: {total}")
```

#### Salida esperada
```
Vida de los fuertes: 100
```

#### Solución
```python
vidas = [12, 30, 8, 45, 25]
total = sum(v for v in vidas if v > 20)
print(f"Vida de los fuertes: {total}")
```

#### Al superarla
—Cien —dice Tilo—. Eso sí me entra.

#### Imagen
- Tres siluetas fuertes iluminadas entre cinco; sobre ellas, el número 100.
- Tilo se rasca la cabeza, contento.

### Micro-misión R03-N01-P5 · Se gastan

```meta
lugar: La Torre del Reloj: el primer piso
personajes: Mia, Gheco, Tilo, Maese Horas
carta: Se gastan | un generador se recorre UNA vez · para usarlo dos veces: list(gen)
recompensa: xp 15, oro 15
```

#### Escena
Querés sumar las vidas y después buscar la más alta, con el mismo generador. La suma sale bien… y el máximo explota: `ValueError`, la secuencia está **vacía**.
Desde una escalera, un señor bajito, con lupa de relojero en un ojo, se ríe.

#### Gheco sugiere
Un generador se **gasta**: después de recorrerlo, queda vacío. Si necesitás los valores dos veces, guardalos en una **lista** (`list(...)` o una comprehension con corchetes).

#### Desafío
Arreglalo para poder usar las vidas dos veces.

#### Código inicial
```python
vidas = (v * 2 for v in [10, 25, 15])
print(f"Total: {sum(vidas)}")
print(f"La más alta: {max(vidas)}")
```

#### Salida esperada
```
Total: 100
La más alta: 50
```

#### Solución
```python
vidas = [v * 2 for v in [10, 25, 15]]
print(f"Total: {sum(vidas)}")
print(f"La más alta: {max(vidas)}")
```

#### Al superarla
—Bien visto —dice el señor de la lupa, y baja de la escalera—. **Maese Horas**, relojero. Subí cuando puedas: el gran reloj atrasa desde que se perdió una pieza, y vos tenés cara de saber buscar.

#### Imagen
- Maese Horas, bajito, con lupa de relojero en un ojo y delantal lleno de herramientas, baja de una escalera de bronce.
- Mia lo mira desde abajo; en el pergamino, `list(...)` brilla en verde.
- Arriba, el gran reloj de la Torre, con una aguja torcida.

### Misión R03-N01-M1 · Los pares sin fin

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Escribí el generador `pares_infinitos()`, que entregue 0, 2, 4, 6… sin fin. Tomá los primeros 10 con `islice` y mostralos en una lista.

#### Criterio de aprobación

- El generador usa `while True` y `yield`.
- Se consumen solo 10 valores con `islice`.

#### Salida esperada

```
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

#### Solución de referencia

```python
from itertools import islice


def pares_infinitos():
    n = 0
    while True:
        yield n
        n += 2


print(list(islice(pares_infinitos(), 10)))
```

### Misión R03-N01-M2 · La furia que crece

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Escribí `danio_por_turno(base)`: un generador infinito que en cada turno entregue un daño que crece un 10 % respecto del anterior (redondeado a 2 decimales al entregarlo). Con base 10, mostrá los daños de los primeros 8 turnos y su total con 2 decimales.

#### Criterio de aprobación

- Es un generador infinito.
- Cada valor es un 10 % más que el anterior (10, 11.0, 12.1…).
- Suma los 8 primeros: 114.37.

#### Salida esperada

```
daño por turno: [10, 11.0, 12.1, 13.31, 14.64, 16.11, 17.72, 19.49]
total en 8 turnos: 114.37
```

#### Solución de referencia

```python
from itertools import islice


def danio_por_turno(base):
    """Cada turno el daño crece un 10 % sobre el anterior (interés compuesto)."""
    danio = base
    while True:
        yield round(danio, 2)
        danio *= 1.10


primeros = list(islice(danio_por_turno(10), 8))
print("daño por turno:", primeros)
print(f"total en 8 turnos: {sum(primeros):.2f}")
```

### Misión R03-N01-M3 · El mazo que se reparte

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Mazo` que guarde una lista de cartas y sea **iterable**: definí `__iter__` como generador. Mostrá que se puede recorrer con `for` dos veces, convertir en lista y usar con `in`.

#### Criterio de aprobación

- `__iter__` usa `yield`.
- El mazo se recorre más de una vez sin gastarse.
- Funciona con `for`, `list()` e `in`.

#### Salida esperada

```
robás: espada
robás: escudo
robás: poción
de nuevo: ['espada', 'escudo', 'poción']
¿hay poción? True
```

#### Solución de referencia

```python
class Mazo:
    """Un iterable propio: se puede recorrer con for todas las veces que quieras."""

    def __init__(self, cartas):
        self.cartas = cartas

    def __iter__(self):
        for carta in self.cartas:     # un generador: cada for arranca de cero
            yield carta


mazo = Mazo(["espada", "escudo", "poción"])
for carta in mazo:
    print("robás:", carta)
print("de nuevo:", list(mazo))
print("¿hay poción?", "poción" in mazo)
```

### Encargo R03-N01-E1 · El registro del servidor

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

El servidor del Gremio guarda un registro con líneas `INFO: …` y `ERROR: …`. Escribí el generador `leer_registro(lineas)`, que entregue solo los errores como `(número de línea, mensaje)` sin el prefijo. Mostralos y contá cuántos errores **distintos** hay.

#### Criterio de aprobación

- El generador filtra y limpia las líneas sin armar listas intermedias.
- Usa `enumerate(..., start=1)` para el número de línea.
- Cuenta los distintos con un set.

#### Salida esperada

```
línea 2: no se encontró config.txt
línea 4: la base no responde
línea 6: la base no responde
errores distintos: 2
```

#### Solución de referencia

```python
def leer_registro(lineas):
    """Genera solo las líneas de error, ya limpias, sin cargar todo en una lista."""
    for numero, linea in enumerate(lineas, start=1):
        linea = linea.strip()
        if linea.startswith("ERROR"):
            yield numero, linea.removeprefix("ERROR").strip(" :")


registro = """INFO: arranca el servidor
ERROR: no se encontró config.txt
INFO: usuario Mia conectado
ERROR: la base no responde
INFO: reintento
ERROR: la base no responde""".splitlines()

errores = list(leer_registro(registro))
for numero, mensaje in errores:
    print(f"línea {numero}: {mensaje}")
print("errores distintos:", len({mensaje for _, mensaje in errores}))
```

### Prueba del sello

#### ¿Qué diferencia hay entre un iterable y un iterador?

El iterable se puede recorrer (una lista); el iterador es quien hace el recorrido y recuerda por dónde va (lo que da `iter(lista)`).

#### ¿Qué pasa al llamar a una función que tiene `yield`?

No se ejecuta: devuelve un generador. El código corre de a pedazos con cada `next()`.

#### ¿Qué hace `yield` que no hace `return`?

Entrega un valor y **pausa** la función, que después sigue desde ahí. `return` la termina.

#### ¿Por qué un generador puede ser infinito?

Porque produce los valores de a uno cuando se los piden: nunca arma la secuencia entera.

#### ¿Qué da recorrer dos veces el mismo generador?

La segunda vez está vacío: los generadores se gastan.

### Soluciones (docente)

Reescrito desde cero a partir de `17-Python/21-Generadores` (la auditoría pedía explicar iterable vs iterador, que no estaba).

## R03-N02 · Programación funcional e itertools

```meta
tipo: tema
padre: R03-N01
precio: 10
criatura: ogro
temas: func.lambdas, func.orden-superior, func.streams
```

### Crónica

En el segundo piso, Maese Horas ordena cientos de piezas sin tocarlas una por una. Dice «agrupalas por tamaño», «quedate con las doradas», «ordenalas por peso y después por nombre», y las piezas obedecen.

—No escribo **cómo** hacerlo paso a paso —dice el relojero—. Escribo **qué** quiero.

Entre las piezas, Mia encuentra una de **plomo y vidrio de colores** que no es de ningún reloj.

### Objetivos

- Usar `lambda`, `map`, `filter` y `functools.reduce`, y saber cuándo conviene una comprehension.
- Ordenar y elegir con `key=` (una o varias claves).
- Aprovechar `itertools`: `groupby`, `combinations`, `product`, `accumulate`, `chain`.

### Antes de empezar

Listas y diccionarios (R01), `lambda` y funciones como objetos (R01-N09), generadores (R03-N01).

### Explicación

#### Funciones que reciben funciones

En Python, una función es un valor más: se puede pasar como argumento. Muchas herramientas reciben una función que dice **qué hacer con cada elemento**:

| Herramienta | Qué hace | Equivalente con comprehension |
|---|---|---|
| `map(f, datos)` | aplica `f` a cada elemento | `[f(x) for x in datos]` |
| `filter(f, datos)` | se queda con los que cumplen `f` | `[x for x in datos if f(x)]` |
| `sorted(datos, key=f)` | ordena según `f(x)` | — |
| `max(datos, key=f)` | el que tiene el `f(x)` más grande | — |

`map` y `filter` son **perezosos** (como los generadores). En Python idiomático, la comprehension suele leerse mejor; `map` conviene cuando ya tenés la función con nombre: `map(str.upper, nombres)`.

#### `lambda`: funciones de una línea

`lambda h: h.nivel` es una función sin nombre que recibe `h` y devuelve `h.nivel`. Sirve para pasar un criterio corto. Si necesita más de una expresión, usá `def`.

#### Ordenar por varias claves

`key` puede devolver una **tupla**: se ordena por el primer valor y, en los empates, por el segundo.

```python
sorted(compania, key=lambda h: (h.clase, -h.nivel))   # clase ascendente, nivel descendente
```

El truco del `-` para invertir funciona con números. `sorted` es **estable**: en un empate, respeta el orden original.

#### `reduce`: plegar una lista a un valor

`reduce(lambda acumulado, x: acumulado + x, datos, 0)` va combinando los elementos de a uno. Casi siempre hay algo más claro (`sum`, `max`, `math.prod`, `any`, `all`), pero es bueno reconocerlo.

#### `itertools`

| Función | Qué hace |
|---|---|
| `groupby(datos, key)` | agrupa elementos **consecutivos** con la misma clave (¡ordená antes!) |
| `combinations(datos, 2)` | todas las parejas sin repetir |
| `permutations(datos, 2)` | todas las parejas ordenadas |
| `product(a, b, c)` | todas las combinaciones de un elemento de cada lista |
| `accumulate(datos)` | sumas parciales: `[1, 3, 6, 10]` |
| `chain(a, b)` | pega iterables uno después del otro |
| `islice`, `count`, `cycle` | cortar, contar sin fin, repetir sin fin |

### Código de ejemplo

```python
"""Estilo funcional: lambda, map/filter, sorted(key=...), itertools y reduce."""

from dataclasses import dataclass
from functools import reduce
import itertools as it


@dataclass(frozen=True)
class Heroe:
    nombre: str
    clase: str
    nivel: int
    vida: int


compania = [
    Heroe("Mia", "maga", 5, 90),
    Heroe("Tilo", "guerrero", 7, 160),
    Heroe("Sila", "maga", 4, 70),
    Heroe("Baldo", "guerrero", 6, 140),
    Heroe("Ana", "pícara", 8, 110),
]

# map y filter… y la comprehension equivalente (que suele leerse mejor)
print(list(map(lambda h: h.nombre.upper(), compania)))
print([h.nombre for h in filter(lambda h: h.vida >= 100, compania)])
print([h.nombre for h in compania if h.vida >= 100])

# sorted con key=: el patrón más usado
print("por nivel:", [f"{h.nombre}({h.nivel})" for h in sorted(compania, key=lambda h: h.nivel, reverse=True)])
print("por clase y nivel:", [(h.clase, h.nombre) for h in sorted(compania, key=lambda h: (h.clase, -h.nivel))])

# min / max / sum con key=
print("el de más vida:", max(compania, key=lambda h: h.vida).nombre)
print("vida total:", sum(h.vida for h in compania))
print("vida total (reduce):", reduce(lambda acumulado, h: acumulado + h.vida, compania, 0))

# groupby agrupa elementos CONSECUTIVOS: primero hay que ordenar
print("--- por clase ---")
for clase, grupo in it.groupby(sorted(compania, key=lambda h: h.clase), key=lambda h: h.clase):
    print(f"  {clase}: {[h.nombre for h in grupo]}")

# combinatoria, suma acumulada y encadenar
print("dúos posibles:", len(list(it.combinations(compania, 2))))
print("XP acumulada:", list(it.accumulate([100, 250, 400, 700])))
print("primeros 4:", list(it.islice(it.chain(["slime"] * 3, ["orco"] * 2, ["jefe"]), 4)))
```

### Salida esperada

```
['MIA', 'TILO', 'SILA', 'BALDO', 'ANA']
['Tilo', 'Baldo', 'Ana']
['Tilo', 'Baldo', 'Ana']
por nivel: ['Ana(8)', 'Tilo(7)', 'Baldo(6)', 'Mia(5)', 'Sila(4)']
por clase y nivel: [('guerrero', 'Tilo'), ('guerrero', 'Baldo'), ('maga', 'Mia'), ('maga', 'Sila'), ('pícara', 'Ana')]
el de más vida: Tilo
vida total: 570
vida total (reduce): 570
--- por clase ---
  guerrero: ['Tilo', 'Baldo']
  maga: ['Mia', 'Sila']
  pícara: ['Ana']
dúos posibles: 10
XP acumulada: [100, 350, 750, 1450]
primeros 4: ['slime', 'slime', 'slime', 'orco']
```

### ¿Para qué sirve?

Ordenar productos por precio y después por nombre, filtrar los pedidos pendientes, agrupar ventas por mes, calcular totales acumulados para un gráfico, probar todas las combinaciones de talles y colores de un catálogo: todo eso se escribe en una o dos líneas con estas herramientas. Es el estilo que vas a ver en análisis de datos (pandas usa la misma idea) y en código profesional.

### Errores habituales

**Ogro: `groupby` sin ordenar**: agrupa solo los elementos **consecutivos**, así que si la lista no está ordenada por la misma clave, una misma clase aparece en varios grupos. No da error: da un resultado mal.

**Ogro: consumir dos veces un `map` o un `groupby`**: son perezosos y se gastan, como los generadores. Además, cada grupo de `groupby` se gasta al avanzar al siguiente: si lo necesitás después, convertilo en lista.

**Goblin: `sorted` con tipos mezclados**: `sorted([3, "a"])` da `TypeError: '<' not supported between instances of 'str' and 'int'`.

**Ogro: invertir un texto con `-`**: `key=lambda h: -h.nombre` da `TypeError`. Para "descendente" en textos, usá `reverse=True` o dos ordenamientos seguidos (aprovechando que `sorted` es estable).

### Micro-misión R03-N02-P1 · Ordenalas por peso

```meta
lugar: La Torre del Reloj: el segundo piso
personajes: Mia, Gheco, Maese Horas
carta: sorted con key | sorted(piezas, key=lambda p: p[1]) · lambda: una función de una línea
recompensa: xp 10, oro 10
```

#### Escena
El segundo piso es un taller con cientos de piezas sobre una mesa. Maese Horas no las toca.
—Ordenalas por peso —dice, y espera.

#### Gheco sugiere
`sorted(datos, key=f)` ordena según lo que devuelve `f` para cada elemento. `lambda p: p[1]` es una función sin nombre que recibe `p` y devuelve `p[1]`.

#### Desafío
Ordená las piezas por peso (el segundo valor).

#### Código inicial
```python
piezas = [("engranaje", 12), ("resorte", 3), ("péndulo", 40), ("tornillo", 1)]
for nombre, peso in sorted(piezas, key=___):
    print(f"{nombre}: {peso}")
```

#### Salida esperada
```
tornillo: 1
resorte: 3
engranaje: 12
péndulo: 40
```

#### Solución
```python
piezas = [("engranaje", 12), ("resorte", 3), ("péndulo", 40), ("tornillo", 1)]
for nombre, peso in sorted(piezas, key=lambda p: p[1]):
    print(f"{nombre}: {peso}")
```

#### Al superarla
Las piezas se acomodan solas sobre la mesa, de la más liviana a la más pesada. Maese Horas asiente. —No dije **cómo**. Dije **qué**.

#### Imagen
- Un taller de relojería con cientos de piezas de bronce sobre una mesa larga.
- Las piezas se ordenan solas en fila, de la más chica a la más grande.
- Maese Horas, con los brazos cruzados, satisfecho.

### Micro-misión R03-N02-P2 · Quedate con las doradas

```meta
lugar: La Torre del Reloj: el segundo piso
personajes: Mia, Gheco, Maese Horas
carta: filter y map | filter(f, datos) se queda con los que cumplen · map(f, datos) aplica f a cada uno
recompensa: xp 10, oro 10
```

#### Escena
—Ahora quedate solo con las doradas —dice Maese Horas—, y decime sus nombres en mayúsculas, que no veo bien.

#### Gheco sugiere
`filter(f, datos)` deja pasar los elementos para los que `f` da `True`. `map(f, datos)` aplica `f` a cada uno. Los dos son perezosos, como los generadores.

#### Desafío
Completá el filtro.

#### Código inicial
```python
piezas = [
    {"nombre": "rueda", "color": "dorada"},
    {"nombre": "eje", "color": "gris"},
    {"nombre": "aguja", "color": "dorada"},
]
doradas = ___(lambda p: p["color"] == "dorada", piezas)
nombres = map(lambda p: p["nombre"].upper(), doradas)
print(list(nombres))
```

#### Salida esperada
```
['RUEDA', 'AGUJA']
```

#### Solución
```python
piezas = [
    {"nombre": "rueda", "color": "dorada"},
    {"nombre": "eje", "color": "gris"},
    {"nombre": "aguja", "color": "dorada"},
]
doradas = filter(lambda p: p["color"] == "dorada", piezas)
nombres = map(lambda p: p["nombre"].upper(), doradas)
print(list(nombres))
```

#### Al superarla
Las piezas grises se apartan y las doradas brillan solas. —Rueda y aguja —lee Maese Horas—. Ahora sí veo.

#### Imagen
- Sobre la mesa, las piezas grises se corren a un costado; las doradas brillan.
- Maese Horas se acerca la lupa, sonriendo.

### Micro-misión R03-N02-P3 · Por tamaño y después por peso

```meta
lugar: La Torre del Reloj: el segundo piso
personajes: Mia, Gheco, Maese Horas
carta: Varias claves | key=lambda p: (p["tamaño"], -p["peso"]) · el - invierte un número
recompensa: xp 10, oro 10
```

#### Escena
—Por tamaño —dice el relojero—. Y entre las del mismo tamaño, **la más pesada primero**.

#### Gheco sugiere
Si `key` devuelve una **tupla**, se ordena por el primer valor y, en los empates, por el segundo. Para invertir un número, ponele un `-` adelante.

#### Desafío
Escribí la clave con los dos criterios.

#### Código inicial
```python
piezas = [
    {"nombre": "a", "tamaño": 2, "peso": 5},
    {"nombre": "b", "tamaño": 1, "peso": 3},
    {"nombre": "c", "tamaño": 2, "peso": 9},
    {"nombre": "d", "tamaño": 1, "peso": 7},
]
orden = sorted(piezas, key=lambda p: ___)
print([p["nombre"] for p in orden])
```

#### Salida esperada
```
['d', 'b', 'c', 'a']
```

#### Solución
```python
piezas = [
    {"nombre": "a", "tamaño": 2, "peso": 5},
    {"nombre": "b", "tamaño": 1, "peso": 3},
    {"nombre": "c", "tamaño": 2, "peso": 9},
    {"nombre": "d", "tamaño": 1, "peso": 7},
]
orden = sorted(piezas, key=lambda p: (p["tamaño"], -p["peso"]))
print([p["nombre"] for p in orden])
```

#### Al superarla
Las piezas forman dos filas perfectas. Maese Horas silba bajito: la primera vez que alguien lo hace al primer intento esta semana.

#### Imagen
- Dos filas de piezas de relojería, ordenadas por tamaño y por peso.
- Maese Horas silba, con las manos en los bolsillos del delantal.

### Micro-misión R03-N02-P4 · Agrupalas

```meta
lugar: La Torre del Reloj: el segundo piso
personajes: Mia, Gheco, Maese Horas
criatura: ogro
carta: groupby | itertools.groupby(datos, key) · agrupa los CONSECUTIVOS · ¡ordená antes!
recompensa: xp 15, oro 15
```

#### Escena
—Agrupalas por tipo y contalas. —Lo hacés… y aparecen **dos** grupos de resortes. No hay error, pero está mal: un **ogro**.

#### Gheco sugiere
`groupby` solo junta los elementos **consecutivos** con la misma clave. Si los datos no están ordenados por esa clave, el mismo grupo aparece varias veces. Ordená **antes** con la misma `key`.

#### Desafío
Ordená antes de agrupar.

#### Código inicial
```python
from itertools import groupby

piezas = ["resorte", "engranaje", "resorte", "aguja", "engranaje"]
for tipo, grupo in groupby(piezas):
    print(f"{tipo}: {len(list(grupo))}")
```

#### Salida esperada
```
aguja: 1
engranaje: 2
resorte: 2
```

#### Solución
```python
from itertools import groupby

piezas = ["resorte", "engranaje", "resorte", "aguja", "engranaje"]
for tipo, grupo in groupby(sorted(piezas)):
    print(f"{tipo}: {len(list(grupo))}")
```

#### Al superarla
Tres montoncitos, uno por tipo. El ogro se queda sin lugar donde esconderse.

#### Imagen
- Tres montones prolijos de piezas: agujas, engranajes y resortes, con su número encima.
- Un ogro chiquito que se va, sin lugar donde esconderse.

### Micro-misión R03-N02-P5 · Todas las parejas

```meta
lugar: La Torre del Reloj: el segundo piso
personajes: Mia, Gheco, Maese Horas
carta: combinations | itertools.combinations(datos, 2) · todas las parejas sin repetir
recompensa: xp 10, oro 10
```

#### Escena
—Tengo cuatro engranajes —dice Maese Horas—. Quiero probar cada pareja una vez, sin repetir. ¿Cuáles encajan, porque suman 10 dientes?

#### Gheco sugiere
`combinations(datos, 2)` da todas las **parejas** posibles, sin repetir y sin importar el orden.

#### Desafío
Recorré todas las parejas.

#### Código inicial
```python
from itertools import combinations

dientes = [3, 7, 4, 6]
for a, b in ___(dientes, 2):
    if a + b == 10:
        print(f"{a} y {b} encajan")
```

#### Salida esperada
```
3 y 7 encajan
4 y 6 encajan
```

#### Solución
```python
from itertools import combinations

dientes = [3, 7, 4, 6]
for a, b in combinations(dientes, 2):
    if a + b == 10:
        print(f"{a} y {b} encajan")
```

#### Al superarla
Dos parejas de engranajes encajan y giran juntas, con un clic suave.

#### Imagen
- Dos parejas de engranajes de bronce que encajan y giran juntas.
- Maese Horas escucha el clic con el oído pegado a la mesa.

### Micro-misión R03-N02-P6 · La que brilla distinto

```meta
lugar: La Torre del Reloj: el segundo piso
personajes: Mia, Gheco, Maese Horas
carta: max con key | max(piezas, key=lambda p: p["brillo"]) · el que tiene el valor más grande
recompensa: xp 15, oro 15
item: Pieza de Vitral
```

#### Escena
Entre todas las piezas hay una que **brilla distinto**, con colores. Maese Horas no la ve: tiene la lupa sucia.

#### Gheco sugiere
`max(datos, key=f)` devuelve el **elemento** cuyo `f` es el más grande (no el número, el elemento entero).

#### Desafío
Encontrá la pieza que más brilla.

#### Código inicial
```python
piezas = [
    {"nombre": "rueda dorada", "brillo": 6},
    {"nombre": "plomo y vidrio de colores", "brillo": 9},
    {"nombre": "eje gris", "brillo": 1},
]
pieza = max(piezas, key=___)
print(pieza["nombre"])
```

#### Salida esperada
```
plomo y vidrio de colores
```

#### Solución
```python
piezas = [
    {"nombre": "rueda dorada", "brillo": 6},
    {"nombre": "plomo y vidrio de colores", "brillo": 9},
    {"nombre": "eje gris", "brillo": 1},
]
pieza = max(piezas, key=lambda p: p["brillo"])
print(pieza["nombre"])
```

#### Al superarla
Una pieza de **plomo y vidrio de colores**. No es de ningún reloj. Es… un pedacito de **vitral**. Maese Horas se limpia la lupa y la mira mucho rato.
—Esto no lo hice yo. Guardala vos.

#### Imagen
- Mia sostiene a contraluz una pieza de plomo y vidrio de colores: un pedacito de vitral.
- Los colores del vitral se proyectan sobre su cara y sobre Gheco.
- Maese Horas, serio, con la lupa recién limpia.

### Misión R03-N02-M1 · La vida por clase

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

A partir de la compañía, armá un diccionario `{clase: vida promedio}` usando `groupby` (acordate de ordenar antes) y mostralo alineado, con un decimal.

#### Criterio de aprobación

- Ordena por clase antes de agrupar.
- Calcula el promedio de cada grupo.
- Guerrero 150.0, maga 80.0 y pícara 110.0.

#### Código inicial

```python
from itertools import groupby
from dataclasses import dataclass


@dataclass(frozen=True)
class Heroe:
    nombre: str
    clase: str
    nivel: int
    vida: int


compania = [
    Heroe("Mia", "maga", 5, 90),
    Heroe("Tilo", "guerrero", 7, 160),
    Heroe("Sila", "maga", 4, 70),
    Heroe("Baldo", "guerrero", 6, 140),
    Heroe("Ana", "pícara", 7, 110),
]

# Calculá {clase: vida_promedio} con groupby
```

#### Salida esperada

```
guerrero    150.0
maga         80.0
pícara      110.0
```

#### Solución de referencia

```python
from itertools import groupby
from dataclasses import dataclass


@dataclass(frozen=True)
class Heroe:
    nombre: str
    clase: str
    nivel: int
    vida: int


compania = [
    Heroe("Mia", "maga", 5, 90),
    Heroe("Tilo", "guerrero", 7, 160),
    Heroe("Sila", "maga", 4, 70),
    Heroe("Baldo", "guerrero", 6, 140),
    Heroe("Ana", "pícara", 7, 110),
]


por_clase = sorted(compania, key=lambda h: h.clase)
promedios = {
    clase: sum(h.vida for h in grupo) / len(grupo)
    for clase, grupo in ((c, list(g)) for c, g in groupby(por_clase, key=lambda h: h.clase))
}
for clase, promedio in promedios.items():
    print(f"{clase:<10}{promedio:>7.1f}")
```

### Misión R03-N02-M2 · El orden del torneo

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Ordená la compañía por nivel **de mayor a menor** y, a igual nivel, por nombre **alfabético**, con un solo `sorted` y una `key` que devuelva una tupla. Mostrá nivel y nombre.

#### Criterio de aprobación

- Un solo `sorted` con `key=lambda h: (-h.nivel, h.nombre)` (o equivalente).
- Ana y Tilo (nivel 7) quedan en orden alfabético.

#### Código inicial

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Heroe:
    nombre: str
    clase: str
    nivel: int
    vida: int


compania = [
    Heroe("Mia", "maga", 5, 90),
    Heroe("Tilo", "guerrero", 7, 160),
    Heroe("Sila", "maga", 4, 70),
    Heroe("Baldo", "guerrero", 6, 140),
    Heroe("Ana", "pícara", 7, 110),
]

# Ordená por nivel (de mayor a menor) y, a igual nivel, por nombre
```

#### Salida esperada

```
 7  Ana
 7  Tilo
 6  Baldo
 5  Mia
 4  Sila
```

#### Solución de referencia

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Heroe:
    nombre: str
    clase: str
    nivel: int
    vida: int


compania = [
    Heroe("Mia", "maga", 5, 90),
    Heroe("Tilo", "guerrero", 7, 160),
    Heroe("Sila", "maga", 4, 70),
    Heroe("Baldo", "guerrero", 6, 140),
    Heroe("Ana", "pícara", 7, 110),
]


ordenados = sorted(compania, key=lambda h: (-h.nivel, h.nombre))
for h in ordenados:
    print(f"{h.nivel:>2}  {h.nombre}")
```

### Misión R03-N02-M3 · Todos los equipos posibles

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Con tres listas (armas: espada y arco; armaduras: cuero y malla; amuletos: fuego, hielo y vida), generá con `itertools.product` todas las combinaciones de equipo. Mostrá cuántas son, las primeras cuatro y las que llevan arco y amuleto de hielo.

#### Criterio de aprobación

- Usa `product` en lugar de tres `for` anidados.
- Muestra 12 combinaciones en total.
- Filtra con una comprehension.

#### Salida esperada

```
combinaciones: 12
  espada + cuero + amuleto de fuego
  espada + cuero + amuleto de hielo
  espada + cuero + amuleto de vida
  espada + malla + amuleto de fuego
con arco y hielo: [('arco', 'cuero', 'hielo'), ('arco', 'malla', 'hielo')]
```

#### Solución de referencia

```python
from itertools import product

armas = ["espada", "arco"]
armaduras = ["cuero", "malla"]
amuletos = ["fuego", "hielo", "vida"]

equipos = list(product(armas, armaduras, amuletos))
print("combinaciones:", len(equipos))
for arma, armadura, amuleto in equipos[:4]:
    print(f"  {arma} + {armadura} + amuleto de {amuleto}")
print("con arco y hielo:", [e for e in equipos if e[0] == "arco" and e[2] == "hielo"])
```

### Encargo R03-N02-E1 · La caja del almacén

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

Con la lista de ventas del día (producto, rubro, precio y cantidad), calculá en una línea cada cosa: los productos de más de $2000, los tres de mayor importe (precio × cantidad), el total del día y si hubo alguna venta de más de 10 unidades.

#### Criterio de aprobación

- Define el importe una sola vez (una `lambda` o una función) y la reutiliza.
- Usa `sorted(..., key=...)`, `sum` y `any`.

#### Salida esperada

```
productos de más de $2000: ['yerba', 'gaseosa']
top 3 por importe: ['yerba', 'pan', 'facturas']
total del día: 47000
¿alguna venta de más de 10 unidades? True
```

#### Solución de referencia

```python
ventas = [
    {"producto": "yerba", "rubro": "almacén", "precio": 3200, "cantidad": 4},
    {"producto": "pan", "rubro": "panadería", "precio": 1200, "cantidad": 10},
    {"producto": "azúcar", "rubro": "almacén", "precio": 1500, "cantidad": 2},
    {"producto": "facturas", "rubro": "panadería", "precio": 900, "cantidad": 12},
    {"producto": "gaseosa", "rubro": "bebidas", "precio": 2800, "cantidad": 3},
]

importe = lambda v: v["precio"] * v["cantidad"]
caras = [v["producto"] for v in ventas if v["precio"] > 2000]
print("productos de más de $2000:", caras)
print("top 3 por importe:", [v["producto"] for v in sorted(ventas, key=importe, reverse=True)[:3]])
print("total del día:", sum(map(importe, ventas)))
print("¿alguna venta de más de 10 unidades?", any(v["cantidad"] > 10 for v in ventas))
```

### Prueba del sello

#### ¿Qué devuelve `map(f, datos)`?

Un iterador perezoso con `f` aplicada a cada elemento (para verlo entero, `list(...)`).

#### ¿Cómo ordenás por nivel descendente y, en los empates, por nombre?

`sorted(datos, key=lambda h: (-h.nivel, h.nombre))`.

#### ¿Por qué hay que ordenar antes de usar `groupby`?

Porque solo agrupa elementos consecutivos con la misma clave.

#### ¿Qué diferencia hay entre `combinations` y `product`?

`combinations` elige grupos de una misma lista sin repetir; `product` toma un elemento de cada lista.

#### ¿Cuándo conviene `def` en lugar de `lambda`?

Cuando la función necesita más de una expresión, o un nombre para reutilizarla y documentarla.

### Soluciones (docente)

Reescrito desde cero a partir de `17-Python/22-Funcional-Itertools`.

## R03-N03 · Closures y decoradores

```meta
tipo: tema
padre: R03-N02
precio: 10
criatura: troll
temas: func.closures, func.decoradores
```

### Crónica

En el tercer piso, los relojeros no desarman los relojes para mejorarlos: les ponen **encima** una pieza nueva. Una que mide el tiempo, otra que repite si algo falla, otra que anota cada movimiento. El reloj sigue siendo el mismo; ahora hace más.

—Eso es un **decorador** —dice Maese Horas—. Una función que envuelve a otra sin tocarla.

La pieza de vidrio encaja justo en uno: es la que el viajero arregló hace mucho.

### Objetivos

- Entender los closures y usar `nonlocal`.
- Escribir decoradores, con y sin parámetros, usando `functools.wraps`.
- Aprovechar `functools.lru_cache` para no recalcular.

### Antes de empezar

Funciones como objetos, alcance y `lambda` (R01-N09), `*args` y `**kwargs` (R01-N08), excepciones (R02-N03).

### Explicación

#### Closures: funciones que recuerdan

Una función definida **adentro** de otra puede usar las variables de la de afuera, y las **recuerda** aunque la de afuera ya haya terminado:

```python
def contador():
    total = 0
    def sumar(x):
        nonlocal total      # para MODIFICAR la variable de afuera
        total += x
        return total
    return sumar

golpe = contador()
golpe(5)    # 5
golpe(8)    # 13: recuerda total
```

`nonlocal` es como `global`, pero para la función que la contiene. Solo hace falta para **asignar**; para leer, no.

#### Decoradores

Un decorador es una función que **recibe una función y devuelve otra** que la envuelve:

```python
import functools

def anunciar(func):
    @functools.wraps(func)
    def envoltura(*args, **kwargs):
        print("antes")
        resultado = func(*args, **kwargs)
        print("después")
        return resultado
    return envoltura

@anunciar
def curar(vida, cantidad): ...
```

- `@anunciar` encima de `def curar` es exactamente `curar = anunciar(curar)`.
- `*args, **kwargs` permite envolver funciones con cualquier cantidad de parámetros.
- `@functools.wraps(func)` copia el nombre y el docstring de la original a la envoltura. Ponelo siempre.
- No te olvides del `return resultado`: si no, la función decorada devuelve `None`.

#### Decoradores con parámetros

`@reintentar(veces=3)` necesita **un nivel más**: `reintentar(3)` devuelve el decorador, que recibe la función y devuelve la envoltura. Tres funciones, una adentro de la otra.

#### Decoradores que ya vienen con Python

- `@functools.lru_cache`: guarda los resultados según los argumentos. La segunda vez que se llama con lo mismo, responde al instante. Convierte recursiones lentísimas (como Fibonacci) en inmediatas.
- `@property`, `@classmethod`, `@staticmethod` (R02) y `@dataclass` también son decoradores.

#### Para qué se usan

Agregar comportamiento **sin tocar** la función: medir tiempos, registrar llamadas, validar argumentos, pedir permisos, reintentar, cachear. Y registrar funciones en una tabla (el patrón que usan los frameworks web para las rutas: `@app.route("/inicio")`).

### Código de ejemplo

```python
"""Closures y decoradores: agregar comportamiento sin tocar la función."""

import functools


# =========================================================
# Closure: una función que RECUERDA las variables de donde nació
# =========================================================
def contador_de_danio():
    total = 0

    def registrar(golpe):
        nonlocal total          # modificar la variable de la función de afuera
        total += golpe
        return total

    return registrar


golpe = contador_de_danio()
print(golpe(5), golpe(8), golpe(3))     # recuerda 'total' entre llamadas


# =========================================================
# Un decorador recibe una función y devuelve otra que la envuelve
# =========================================================
def anunciar(func):
    @functools.wraps(func)              # conserva el nombre y el docstring
    def envoltura(*args, **kwargs):
        print(f"  → {func.__name__}{args}")
        resultado = func(*args, **kwargs)
        print(f"  ← {resultado}")
        return resultado
    return envoltura


@anunciar                               # es lo mismo que: curar = anunciar(curar)
def curar(vida, cantidad):
    """Suma vida sin pasar de 100."""
    return min(100, vida + cantidad)


curar(80, 30)
print("nombre conservado:", curar.__name__, "-", curar.__doc__)


# =========================================================
# lru_cache: recordar resultados ya calculados (memoización)
# =========================================================
@functools.lru_cache(maxsize=None)
def caminos(fila, col):
    """Formas de llegar a (fila, col) moviéndose solo a la derecha o hacia abajo."""
    if fila == 0 or col == 0:
        return 1
    return caminos(fila - 1, col) + caminos(fila, col - 1)


print("caminos hasta (10, 10):", caminos(10, 10))
print(caminos.cache_info())


# =========================================================
# Decorador con parámetros: una función más de anidamiento
# =========================================================
def reintentar(veces):
    def decorador(func):
        @functools.wraps(func)
        def envoltura(*args, **kwargs):
            for intento in range(1, veces + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError as error:
                    print(f"  intento {intento} falló: {error}")
            raise RuntimeError(f"{func.__name__} falló {veces} veces")
        return envoltura
    return decorador


llamadas = 0

@reintentar(veces=3)
def conectar():
    global llamadas
    llamadas += 1
    if llamadas < 3:
        raise ConnectionError("tiempo agotado")
    return "conectado"


print(conectar())


# =========================================================
# Patrón registrador: una tabla de comandos
# =========================================================
COMANDOS = {}

def comando(nombre):
    def registrar(func):
        COMANDOS[nombre] = func
        return func
    return registrar


@comando("saludar")
def saludar(quien):
    return f"¡Hola, {quien}!"


@comando("atacar")
def atacar(quien):
    return f"{quien} lanza un rayo"


for orden in ["saludar", "atacar", "bailar"]:
    accion = COMANDOS.get(orden)
    print(accion("Mia") if accion else f"no conozco '{orden}'")
```

### Salida esperada

```
5 13 16
  → curar(80, 30)
  ← 100
nombre conservado: curar - Suma vida sin pasar de 100.
caminos hasta (10, 10): 184756
CacheInfo(hits=81, misses=120, maxsize=None, currsize=120)
  intento 1 falló: tiempo agotado
  intento 2 falló: tiempo agotado
conectado
¡Hola, Mia!
Mia lanza un rayo
no conozco 'bailar'
```

### ¿Para qué sirve?

En los frameworks web, `@login_required` bloquea una página a quien no inició sesión y `@app.route("/perfil")` conecta una dirección con una función. En las pruebas automáticas, `@pytest.mark` marca casos. En un sistema de pagos, un decorador reintenta la conexión con el banco si falla. Y `lru_cache` acelera cualquier cálculo que se repite.

### Errores habituales

**Troll: el closure que se lleva la última vuelta** (*late binding*):

```python
acciones = [lambda: print(i) for i in range(3)]
for a in acciones:
    a()          # 2, 2, 2  (no 0, 1, 2)
```

La `lambda` recuerda **la variable** `i`, no su valor en ese momento. Se arregla con un parámetro por defecto: `lambda i=i: print(i)`.

**Esqueleto: modificar sin `nonlocal`**:

```
UnboundLocalError: cannot access local variable 'total' where it is not associated with a value
```

**Ogro: olvidar el `return` en la envoltura**: la función decorada devuelve `None`.

**Ogro: olvidar `@functools.wraps`**: todas las funciones decoradas pasan a llamarse `envoltura`, y los mensajes de error y la documentación confunden.

**Goblin: `@reintentar` sin paréntesis** cuando el decorador tiene parámetros: `veces` recibe la función y todo se rompe.

### Micro-misión R03-N03-P1 · La función que recuerda

```meta
lugar: La Torre del Reloj: el tercer piso
personajes: Mia, Gheco, Maese Horas
carta: Closure | una función adentro de otra recuerda sus variables · nonlocal para cambiarlas
recompensa: xp 10, oro 10
```

#### Escena
En el tercer piso, cada reloj tiene una cuerda que **recuerda** cuántas vueltas le dieron, aunque nadie la mire.
—Hacé una igual —dice Maese Horas.

#### Gheco sugiere
Una función definida **adentro** de otra recuerda las variables de la de afuera, aunque esa ya haya terminado. Para **cambiarlas** (no solo leerlas), declaralas con `nonlocal`.

#### Desafío
Dejá que `girar` cambie las vueltas de afuera.

#### Código inicial
```python
def cuerda():
    vueltas = 0
    def girar():
        ___ vueltas
        vueltas += 1
        return vueltas
    return girar

reloj = cuerda()
reloj()
reloj()
print(f"Vueltas: {reloj()}")
```

#### Salida esperada
```
Vueltas: 3
```

#### Solución
```python
def cuerda():
    vueltas = 0
    def girar():
        nonlocal vueltas
        vueltas += 1
        return vueltas
    return girar

reloj = cuerda()
reloj()
reloj()
print(f"Vueltas: {reloj()}")
```

#### Al superarla
El relojito de práctica hace tres tics y se queda contando, satisfecho.

#### Imagen
- Un relojito de práctica con la cuerda girando; sobre él, el número 3.
- Relojes de todos los tamaños en las paredes del tercer piso.

### Micro-misión R03-N03-P2 · La pieza que va encima

```meta
lugar: La Torre del Reloj: el tercer piso
personajes: Mia, Gheco, Maese Horas
carta: Decorador | def anunciar(func): def envoltura(*args): ... return envoltura · @anunciar = f = anunciar(f)
recompensa: xp 10, oro 10
```

#### Escena
—No se desarma un reloj para mejorarlo —dice Maese Horas—. Se le pone una pieza **encima**. Esta hace «tic» antes de cada movimiento.

#### Gheco sugiere
Un **decorador** recibe una función y devuelve otra que la **envuelve**. Escribir `@anunciar` arriba de `def mover` es lo mismo que `mover = anunciar(mover)`.

#### Desafío
Ponele la pieza encima a `mover`.

#### Código inicial
```python
def anunciar(func):
    def envoltura(*args):
        print("tic")
        return func(*args)
    return envoltura

___
def mover(aguja):
    print(f"se mueve la aguja {aguja}")

mover("de las horas")
```

#### Salida esperada
```
tic
se mueve la aguja de las horas
```

#### Solución
```python
def anunciar(func):
    def envoltura(*args):
        print("tic")
        return func(*args)
    return envoltura

@anunciar
def mover(aguja):
    print(f"se mueve la aguja {aguja}")

mover("de las horas")
```

#### Al superarla
«Tic», y la aguja se mueve. El reloj es el mismo; ahora hace algo más.

#### Imagen
- Una pieza nueva de bronce montada encima de un reloj; un «tic» de luz sale de ella.
- Maese Horas le señala a Mia cómo encaja.

### Micro-misión R03-N03-P3 · La pieza que se come el resultado

```meta
lugar: La Torre del Reloj: el tercer piso
personajes: Mia, Gheco, Maese Horas
criatura: ogro
carta: return resultado | la envoltura tiene que DEVOLVER lo que devuelve func · si no, da None
recompensa: xp 10, oro 10
```

#### Escena
Le ponés la pieza al reloj que da la hora, y ahora la hora es `None`. Ningún error, todo corre… un **ogro**.

#### Gheco sugiere
La envoltura llama a la función original, pero si **no devuelve** su resultado, la función decorada devuelve `None`. Guardalo y devolvelo: `resultado = func(*args)` y `return resultado`.

#### Desafío
Que la envoltura devuelva lo que devuelve la función.

#### Código inicial
```python
def anunciar(func):
    def envoltura(*args):
        print("tic")
        func(*args)
    return envoltura

@anunciar
def hora():
    return "las siete"

print(f"Son {hora()}")
```

#### Salida esperada
```
tic
Son las siete
```

#### Solución
```python
def anunciar(func):
    def envoltura(*args):
        print("tic")
        return func(*args)
    return envoltura

@anunciar
def hora():
    return "las siete"

print(f"Son {hora()}")
```

#### Al superarla
«Son las siete», dice el reloj, y el ogro se va sin hacer ruido, como vino.

#### Imagen
- Un reloj de pared que pasa de mostrar `None` a «las siete».
- Un ogro que se va de puntillas.

### Micro-misión R03-N03-P4 · Que no pierda su nombre

```meta
lugar: La Torre del Reloj: el tercer piso
personajes: Mia, Gheco, Maese Horas
carta: functools.wraps | @functools.wraps(func) sobre la envoltura · conserva el nombre y el docstring
recompensa: xp 10, oro 10
```

#### Escena
—Ojo —dice Maese Horas—. Le pusiste la pieza encima y ahora el reloj **no sabe cómo se llama**. Dice «envoltura».

#### Gheco sugiere
La envoltura reemplaza a la función, con su nombre y todo. `@functools.wraps(func)` arriba de la envoltura copia el nombre y el docstring de la original. Ponelo siempre.

#### Desafío
Que la función decorada conserve su nombre.

#### Código inicial
```python
import functools

def anunciar(func):
    ___
    def envoltura(*args):
        print("tic")
        return func(*args)
    return envoltura

@anunciar
def girar():
    return "gira"

print(girar.__name__)
```

#### Salida esperada
```
girar
```

#### Solución
```python
import functools

def anunciar(func):
    @functools.wraps(func)
    def envoltura(*args):
        print("tic")
        return func(*args)
    return envoltura

@anunciar
def girar():
    return "gira"

print(girar.__name__)
```

#### Al superarla
El reloj recupera su nombre en la plaquita de bronce: «girar».

#### Imagen
- Una plaquita de bronce en un reloj donde «envoltura» se borra y aparece «girar».

### Micro-misión R03-N03-P5 · La memoria del oráculo

```meta
lugar: La Torre del Reloj: el tercer piso
personajes: Mia, Gheco, Maese Horas
carta: lru_cache | @functools.lru_cache · guarda resultados por argumentos · la recursión lenta se vuelve instantánea
recompensa: xp 15, oro 20
```

#### Escena
En una vitrina, el **oráculo del reloj** calcula las fases de la luna con una cuenta recursiva. Para la fase 25 hace casi un cuarto de millón de cuentas, y tarda tanto que el reloj se atrasa.

#### Gheco sugiere
`@functools.lru_cache` es un decorador que ya viene con Python: **recuerda** el resultado para cada argumento. La segunda vez que se pide lo mismo, contesta sin calcular.

#### Desafío
Ponele memoria al oráculo y mirá cuántas cuentas hace.

#### Código inicial
```python
import functools

cuentas = 0

___
def fase(n):
    global cuentas
    cuentas += 1
    if n < 2:
        return n
    return fase(n - 1) + fase(n - 2)

print(f"Fase 25: {fase(25)}")
print(f"Cuentas: {cuentas}")
```

#### Salida esperada
```
Fase 25: 75025
Cuentas: 26
```

#### Solución
```python
import functools

cuentas = 0

@functools.lru_cache
def fase(n):
    global cuentas
    cuentas += 1
    if n < 2:
        return n
    return fase(n - 1) + fase(n - 2)

print(f"Fase 25: {fase(25)}")
print(f"Cuentas: {cuentas}")
```

#### Al superarla
Veintiséis cuentas en vez de doscientas cuarenta mil. El oráculo contesta al instante.
Y al abrir la vitrina, ves un hueco con una forma conocida. Sacás la **pieza de vitral** de la mochila… y **encaja justo**. Maese Horas se queda mudo.
—Esta pieza la puso alguien hace mucho. Alguien que arregló este reloj antes que nosotros.

#### Imagen
- Una vitrina con un oráculo mecánico de la luna; en su centro, la pieza de vitral encaja y proyecta colores.
- Mia con la mano todavía en la vitrina; Maese Horas, boquiabierto.
- Gheco ilumina la escena con la cola.

### Misión R03-N03-M1 · El contador de hechizos

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Escribí el decorador `@contar_llamadas`, que lleve la cuenta de cuántas veces se llamó a la función decorada. Guardá el contador como **atributo de la envoltura** (`envoltura.llamadas`). Decorá `lanzar_hechizo(nombre)`, llamala tres veces y mostrá el contador.

#### Criterio de aprobación

- Usa `@functools.wraps`.
- El contador es un atributo de la función envoltura.
- La función decorada sigue devolviendo su resultado.

#### Salida esperada

```
¡fuego!
¡hielo!
¡fuego!
veces que se lanzó: 3
```

#### Solución de referencia

```python
import functools


def contar_llamadas(func):
    @functools.wraps(func)
    def envoltura(*args, **kwargs):
        envoltura.llamadas += 1
        return func(*args, **kwargs)
    envoltura.llamadas = 0          # un atributo de la propia función
    return envoltura


@contar_llamadas
def lanzar_hechizo(nombre):
    return f"¡{nombre}!"


for hechizo in ["fuego", "hielo", "fuego"]:
    print(lanzar_hechizo(hechizo))
print("veces que se lanzó:", lanzar_hechizo.llamadas)
```

### Misión R03-N03-M2 · Solo con vida

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Escribí el decorador `@requiere_vida` para **métodos**: si `self.vida <= 0`, avisa que el personaje está fuera de combate y no ejecuta el método. Aplicalo a `atacar` y `curarse` de una clase `Heroe`, y probalo con Mia (30 de vida) y Baldo (0).

#### Criterio de aprobación

- La envoltura recibe `self` como primer parámetro y lo revisa.
- Con vida 0 no se ejecuta el método.
- Funciona con métodos de distintos parámetros (`*args`).

#### Salida esperada

```
Mia ataca a un orco.
Baldo no puede: está fuera de combate.
Baldo no puede: está fuera de combate.
Mia se cura: vida 50.
```

#### Solución de referencia

```python
import functools


def requiere_vida(metodo):
    @functools.wraps(metodo)
    def envoltura(self, *args, **kwargs):
        if self.vida <= 0:
            print(f"{self.nombre} no puede: está fuera de combate.")
            return None
        return metodo(self, *args, **kwargs)
    return envoltura


class Heroe:
    def __init__(self, nombre, vida):
        self.nombre = nombre
        self.vida = vida

    @requiere_vida
    def atacar(self, objetivo):
        print(f"{self.nombre} ataca a {objetivo}.")

    @requiere_vida
    def curarse(self, cantidad):
        self.vida += cantidad
        print(f"{self.nombre} se cura: vida {self.vida}.")


mia = Heroe("Mia", 30)
baldo = Heroe("Baldo", 0)
mia.atacar("un orco")
baldo.atacar("un orco")
baldo.curarse(50)
mia.curarse(20)
```

### Misión R03-N03-M3 · La memoria del oráculo

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Decorá una función recursiva de Fibonacci con `@lru_cache(maxsize=None)`, calculá `fibo(80)` y mostrá `cache_info()`. Después hacé una versión con `maxsize=4`, llamala con 10, 20, 10, 30 y 20, y compará los `misses`: ¿por qué sube cuando la memoria es chica?

#### Criterio de aprobación

- `fibo(80)` responde al instante gracias al caché.
- Muestra `cache_info()` de las dos versiones.
- Explica en un comentario por qué hay más `misses` con `maxsize=4`.

#### Salida esperada

```
fibo(80) = 23416728348467685
sin límite: CacheInfo(hits=78, misses=81, maxsize=None, currsize=81)
con maxsize=4: CacheInfo(hits=66, misses=73, maxsize=4, currsize=4)
```

#### Solución de referencia

```python
import functools


@functools.lru_cache(maxsize=None)
def fibo(n):
    return n if n < 2 else fibo(n - 1) + fibo(n - 2)


@functools.lru_cache(maxsize=4)
def fibo_chico(n):
    return n if n < 2 else fibo_chico(n - 1) + fibo_chico(n - 2)


print("fibo(80) =", fibo(80))
print("sin límite:", fibo.cache_info())

for n in [10, 20, 10, 30, 20]:
    fibo_chico(n)
print("con maxsize=4:", fibo_chico.cache_info())
```

### Encargo R03-N03-E1 · El validador del mercado

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

Escribí el decorador `@validar_positivos`, que antes de ejecutar la función revise todos sus argumentos numéricos (posicionales y por nombre) y lance `ValueError` si alguno es negativo. Decorá `cobrar(precio, cantidad, descuento=0)` y probalo con valores válidos y con una cantidad negativa.

#### Criterio de aprobación

- Revisa `args` y `kwargs`.
- Lanza `ValueError` con un mensaje que nombra la función.
- Con valores válidos, devuelve lo mismo que la función original.

#### Salida esperada

```
3600
3100
rechazado: cobrar: no se aceptan negativos (-3)
```

#### Solución de referencia

```python
import functools


def validar_positivos(func):
    """Rechaza cualquier argumento numérico negativo antes de ejecutar la función."""
    @functools.wraps(func)
    def envoltura(*args, **kwargs):
        for valor in [*args, *kwargs.values()]:
            if isinstance(valor, (int, float)) and valor < 0:
                raise ValueError(f"{func.__name__}: no se aceptan negativos ({valor})")
        return func(*args, **kwargs)
    return envoltura


@validar_positivos
def cobrar(precio, cantidad, descuento=0):
    return precio * cantidad - descuento


print(cobrar(1200, 3))
print(cobrar(1200, 3, descuento=500))
try:
    cobrar(1200, -3)
except ValueError as error:
    print("rechazado:", error)
```

### Prueba del sello

#### ¿Qué es un closure?

Una función definida dentro de otra que recuerda las variables de la función de afuera, aunque esa ya haya terminado.

#### ¿Para qué sirve `nonlocal`?

Para asignar una variable de la función que contiene a la actual (sin él, se crearía una local).

#### ¿A qué equivale `@decorador` encima de `def f`?

A escribir `f = decorador(f)` después de la definición.

#### ¿Para qué sirve `functools.wraps`?

Para que la envoltura conserve el nombre y el docstring de la función original.

#### ¿Qué hace `lru_cache`?

Guarda el resultado para cada combinación de argumentos y lo devuelve sin recalcular.

### Soluciones (docente)

Reescrito desde cero a partir de `17-Python/23-Decoradores`. El ejemplo original medía tiempos con `sleep`; se cambió por un decorador que anuncia llamadas para que la salida sea siempre la misma.

## R03-N04 · Anotaciones de tipos y pruebas

```meta
tipo: tema
padre: R03-N03
precio: 10
criatura: goblin
temas: cal.tipos, cal.pruebas, cal.build
```

### Crónica

En el cuarto piso trabaja **el Gremio de Artífices**. Sus planos no dicen solo «acá va una pieza»: dicen **qué clase** de pieza (un engranaje de bronce, un resorte de acero). Y antes de montar un reloj, lo **prueban**: si una pieza falla, lo saben en el taller y no en la plaza.

—Tu código también puede decir qué espera y comprobar que funciona, Mia —dice Gheco.

### Objetivos

- Anotar tipos en variables, parámetros y resultados (`list[int]`, `dict[str, int]`, `int | None`, `Callable`).
- Escribir pruebas con `assert` que verifiquen tus funciones.
- Conocer `venv`, `pip`, `pytest` y `mypy` para trabajar en tu compu.

### Antes de empezar

Funciones (R01-N08), dataclasses (R02-N01) y excepciones (R02-N03).

### Explicación

#### Anotaciones de tipos

```python
def curar(vida: int, cantidad: int, maximo: int = 100) -> int:
    return min(maximo, vida + cantidad)
```

- `vida: int` dice que el parámetro **debería** ser un entero; `-> int`, que devuelve un entero.
- **Python no las verifica al ejecutar**: `curar("a", "b")` corre igual (y falla adentro, o hace algo raro). Son para las personas, para el editor (autocompletado y avisos) y para herramientas como `mypy`.

| Anotación | Significa |
|---|---|
| `list[str]` | una lista de textos |
| `dict[str, int]` | un diccionario de texto a entero |
| `tuple[str, int]` | una tupla de exactamente un texto y un entero |
| `int \| None` | un entero **o** `None` (algo opcional) |
| `Callable[[int], int]` | una función que recibe un entero y devuelve un entero (de `collections.abc`) |

En las dataclasses (R02-N01) ya venías anotando: `nombre: str`.

#### Probar el código

Una **prueba** es un pedacito de código que usa tu función con datos conocidos y verifica el resultado:

```python
assert curar(80, 30) == 100, "no tendría que pasar de 100"
```

`assert condicion` no hace nada si se cumple, y lanza `AssertionError` si no. Una buena batería de pruebas cubre el caso normal, los **bordes** (cero, vacío, el máximo) y los errores esperados (que lance la excepción correcta).

Las pruebas se escriben **una vez** y se corren cada vez que cambiás algo: si rompiste algo, te enterás al instante.

#### En tu compu: entorno virtual, pytest y mypy

Para proyectos reales se trabaja en la terminal:

```bash
python3 -m venv .venv          # un Python aislado para el proyecto
source .venv/bin/activate      # activarlo (en Windows: .venv\Scripts\activate)
pip install pytest mypy        # instalar herramientas solo acá
```

- **pytest** busca los archivos `test_*.py` y ejecuta cada función `test_…`: cada una es una prueba con `assert`. Muestra cuáles pasaron y, si una falla, qué valores había.
- **mypy** lee tu código **sin ejecutarlo** y avisa si los tipos no cierran: `mypy combate.py`.

En la plataforma no se pueden instalar paquetes, así que las pruebas de acá usan `assert` directo; la misión 3 se hace en tu compu.

### Código de ejemplo

```python
"""Anotaciones de tipos y pruebas: el código que se explica y se verifica solo."""

from dataclasses import dataclass


@dataclass
class Combatiente:
    nombre: str
    vida: int
    ataque: int
    defensa: int = 0

    def vivo(self) -> bool:
        return self.vida > 0


def danio(atacante: Combatiente, defensor: Combatiente, critico: bool = False) -> int:
    """Daño que hace el atacante. Si pega, hace al menos 1."""
    base = atacante.ataque - defensor.defensa
    if critico:
        base *= 2
    return max(1, base)


def aplicar(defensor: Combatiente, cantidad: int) -> Combatiente:
    """Devuelve un combatiente NUEVO con menos vida (no modifica el original)."""
    return Combatiente(defensor.nombre, max(0, defensor.vida - cantidad), defensor.ataque, defensor.defensa)


def buscar(compania: list[Combatiente], nombre: str) -> Combatiente | None:
    """El combatiente con ese nombre, o None si no está."""
    for c in compania:
        if c.nombre == nombre:
            return c
    return None


# =========================================================
# Pruebas: afirmaciones que tienen que cumplirse siempre
# =========================================================
def probar(descripcion: str, condicion: bool) -> None:
    print(f"[{'OK   ' if condicion else 'FALLA'}] {descripcion}")


mia = Combatiente("Mia", vida=30, ataque=8, defensa=2)
golem = Combatiente("Golem", vida=50, ataque=6, defensa=4)

probar("daño básico: 8 - 4 = 4", danio(mia, golem) == 4)
probar("el crítico duplica", danio(mia, golem, critico=True) == 8)
probar("si pega, al menos 1", danio(Combatiente("Débil", 10, 1), golem) == 1)
herido = aplicar(golem, 20)
probar("aplicar no modifica el original", herido.vida == 30 and golem.vida == 50)
probar("la vida no baja de 0", aplicar(mia, 999).vida == 0)
probar("buscar devuelve None si no está", buscar([mia, golem], "Baldo") is None)



# Las anotaciones NO se verifican al ejecutar: Python no se queja acá.
def doble(x: int) -> int:
    return x * 2


print("doble de 'ja':", doble("ja"))    # anotado como int… y devuelve "jaja"
```

### Salida esperada

```
[OK   ] daño básico: 8 - 4 = 4
[OK   ] el crítico duplica
[OK   ] si pega, al menos 1
[OK   ] aplicar no modifica el original
[OK   ] la vida no baja de 0
[OK   ] buscar devuelve None si no está
doble de 'ja': jaja
```

### ¿Para qué sirve?

En los equipos de desarrollo, nadie sube código sin pruebas: cada vez que alguien cambia algo, un servidor corre miles de pruebas automáticamente (integración continua) y avisa si algo se rompió. Las anotaciones de tipos hacen que el editor te avise de errores mientras escribís y sirven de documentación: al ver `def cobrar(monto: float) -> Recibo`, ya sabés cómo usarla.

### Errores habituales

**Goblin: creer que las anotaciones protegen**: `def doble(x: int)` acepta un texto sin chistar. Para que alguien lo note, hace falta `mypy` o una validación propia.

**Ogro: probar solo el caso feliz**: la función anda con 1000, pero nunca probaste con 0, con negativos o con una lista vacía. Los errores viven en los bordes.

**Ogro: comparar decimales con `==` en una prueba**: `0.1 + 0.2 == 0.3` da `False`. Redondeá o usá `math.isclose`.

**Esqueleto: `ModuleNotFoundError: No module named 'pytest'`**: no está instalado en **ese** Python. Activá el entorno virtual antes de instalar y de ejecutar.

**Slime: `list[int]` en Pythons viejos** (antes de 3.9) da error: hay que actualizar Python o usar `from typing import List`.

### Micro-misión R03-N04-P1 · El plano dice qué va

```meta
lugar: El Gremio de Artífices
personajes: Mia, Gheco, Maese Horas
carta: Anotaciones | def curar(vida: int, cantidad: int) -> int: · son para las personas y el editor · Python no las verifica
recompensa: xp 10, oro 10
```

#### Escena
En el cuarto piso trabaja el **Gremio de Artífices**. Sus planos no dicen «acá va una pieza»: dicen **qué clase** de pieza va.
—Tu hechizo también puede decir qué espera y qué devuelve —dice Gheco.

#### Gheco sugiere
`vida: int` anota que el parámetro **debería** ser un entero, y `-> int`, que la función devuelve un entero. Python no lo comprueba al ejecutar: es para quien lee el código y para el editor.

#### Desafío
Anotá lo que devuelve `curar`.

#### Código inicial
```python
def curar(vida: int, cantidad: int) -> ___:
    return min(100, vida + cantidad)

print(curar(80, 30))
print(curar.__annotations__["return"].__name__)
```

#### Salida esperada
```
100
int
```

#### Solución
```python
def curar(vida: int, cantidad: int) -> int:
    return min(100, vida + cantidad)

print(curar(80, 30))
print(curar.__annotations__["return"].__name__)
```

#### Al superarla
El plano de tu hechizo queda colgado en la pared del Gremio, al lado de los de bronce y acero.

#### Imagen
- El Gremio de Artífices: mesas de dibujo con planos de relojes, cada pieza con una etiqueta de tipo.
- El plano del hechizo de Mia, colgado en la pared, con `-> int` en dorado.

### Micro-misión R03-N04-P2 · Puede que no esté

```meta
lugar: El Gremio de Artífices
personajes: Mia, Gheco, una artífice
carta: Tipos compuestos | dict[str, int] · list[str] · int | None: un entero o nada
recompensa: xp 10, oro 10
```

#### Escena
Una artífice busca precios en su lista. A veces la pieza no está, y el plano tiene que decirlo: devuelve un número… **o nada**.

#### Gheco sugiere
Las anotaciones pueden describir colecciones: `dict[str, int]` es un diccionario de texto a entero. Y `int | None` dice «un entero **o** `None`».

#### Desafío
Completá lo que devuelve `precio`.

#### Código inicial
```python
def precio(lista: dict[str, int], pieza: str) -> ___ | None:
    return lista.get(pieza)

lista = {"engranaje": 30, "resorte": 5}
print(precio(lista, "engranaje"))
print(precio(lista, "péndulo"))
```

#### Salida esperada
```
30
None
```

#### Solución
```python
def precio(lista: dict[str, int], pieza: str) -> int | None:
    return lista.get(pieza)

lista = {"engranaje": 30, "resorte": 5}
print(precio(lista, "engranaje"))
print(precio(lista, "péndulo"))
```

#### Al superarla
—Ahora el que use mi lista ya sabe que tiene que fijarse si vino `None` —dice la artífice—. Me ahorraste diez preguntas por día.

#### Imagen
- Una artífice con gafas de aumento y guantes de cuero revisa una lista de precios.
- Sobre la lista, el plano: `int | None`.

### Micro-misión R03-N04-P3 · Probar en el taller

```meta
lugar: El Gremio de Artífices
personajes: Mia, Gheco, Maese Horas
criatura: ogro
carta: assert | assert curar(80, 30) == 100, "mensaje" · no hace nada si se cumple · si no: AssertionError
recompensa: xp 15, oro 15
```

#### Escena
—Antes de montar un reloj en la plaza, se prueba acá —dice Maese Horas—. Si falla, que falle en el taller.
Las pruebas de tu hechizo de curar explotan: `AssertionError`. Había un **ogro** escondido.

#### Gheco sugiere
`assert condicion, "mensaje"` no hace nada si se cumple y lanza `AssertionError` si no. Una **prueba** usa tu función con datos que conocés y comprueba el resultado. Cuando falla, arreglá la **función**, no la prueba.

#### Desafío
Arreglá `curar` para que pasen las pruebas: la vida nunca supera 100.

#### Código inicial
```python
def curar(vida, cantidad):
    return vida + cantidad

assert curar(50, 20) == 70, "caso normal"
assert curar(80, 30) == 100, "no tiene que pasar de 100"
assert curar(100, 0) == 100, "borde: ya está llena"
print("Todas las pruebas pasaron")
```

#### Salida esperada
```
Todas las pruebas pasaron
```

#### Solución
```python
def curar(vida, cantidad):
    return min(100, vida + cantidad)

assert curar(50, 20) == 70, "caso normal"
assert curar(80, 30) == 100, "no tiene que pasar de 100"
assert curar(100, 0) == 100, "borde: ya está llena"
print("Todas las pruebas pasaron")
```

#### Al superarla
Tres luces verdes en la mesa de pruebas. El ogro no llegó a la plaza.

#### Imagen
- Una mesa de pruebas con tres luces verdes encendidas.
- Maese Horas le da una palmada en el hombro a Mia.

### Micro-misión R03-N04-P4 · Que falle bien

```meta
lugar: El Gremio de Artífices
personajes: Mia, Gheco, Maese Horas
carta: Probar errores | try: f(malo) · except ValueError: bien · else: la prueba falla
recompensa: xp 10, oro 10
```

#### Escena
—Una buena prueba también revisa que tu hechizo **se queje** cuando le dan algo imposible —dice el relojero—. Una pieza de peso negativo no existe.

#### Gheco sugiere
Para probar que una función **lanza** un error: llamala con un dato malo dentro de un `try`. Si cae en el `except`, la prueba pasa; si no lanzó nada, cae en el `else`, y ahí la prueba falla.

#### Desafío
Hacé que `pesar` lance `ValueError` con un peso negativo.

#### Código inicial
```python
def pesar(gramos):
    return f"{gramos} g"

assert pesar(12) == "12 g"
try:
    pesar(-3)
except ValueError:
    print("Se queja con -3: bien")
else:
    raise AssertionError("tendría que lanzar ValueError")
```

#### Salida esperada
```
Se queja con -3: bien
```

#### Solución
```python
def pesar(gramos):
    if gramos < 0:
        raise ValueError("no hay pesos negativos")
    return f"{gramos} g"

assert pesar(12) == "12 g"
try:
    pesar(-3)
except ValueError:
    print("Se queja con -3: bien")
else:
    raise AssertionError("tendría que lanzar ValueError")
```

#### Al superarla
La balanza del taller rechaza la pieza imposible con un zumbido. Maese Horas lo anota en la libreta de las pruebas.

#### Imagen
- Una balanza de bronce que rechaza una pieza fantasma con un zumbido rojo.
- Maese Horas anota en una libreta gastada.

### Micro-misión R03-N04-P5 · La batería del Gremio

```meta
lugar: El Gremio de Artífices
personajes: Mia, Gheco, Maese Horas, la maestra del Gremio
carta: Batería de pruebas | casos = [(entrada, esperado), ...] · el normal, los bordes y los errores
recompensa: xp 15, oro 20
item: Escudo de las Aserciones
```

#### Escena
La maestra del Gremio te deja probar su conversor de horas: de minutos a «h:mm». Te da una lista de casos, y quiere que los pruebes **todos de una**.

#### Gheco sugiere
Una **batería** es una lista de casos `(entrada, esperado)` que se recorre con un `for`, con un `assert` por caso. Incluí el caso normal y los **bordes**: cero, justo una hora, un número grande.

#### Desafío
Completá el `assert` de cada caso.

#### Código inicial
```python
def a_horas(minutos: int) -> str:
    return f"{minutos // 60}:{minutos % 60:02}"

casos = [(75, "1:15"), (0, "0:00"), (60, "1:00"), (605, "10:05")]
for entrada, esperado in casos:
    assert ___, f"{entrada} tendría que dar {esperado}"
print(f"{len(casos)} pruebas: todas bien")
```

#### Salida esperada
```
4 pruebas: todas bien
```

#### Solución
```python
def a_horas(minutos: int) -> str:
    return f"{minutos // 60}:{minutos % 60:02}"

casos = [(75, "1:15"), (0, "0:00"), (60, "1:00"), (605, "10:05")]
for entrada, esperado in casos:
    assert a_horas(entrada) == esperado, f"{entrada} tendría que dar {esperado}"
print(f"{len(casos)} pruebas: todas bien")
```

#### Al superarla
Cuatro de cuatro. La maestra del Gremio te entrega un escudo redondo, de bronce, con una marca de verificación grabada: el **Escudo de las Aserciones**.
—Lo que se prueba, aguanta.
Arriba se escucha el ruido de una cocina con mil cosas al fuego.

#### Imagen
- La maestra del Gremio, mayor, con delantal de cuero, entrega un escudo de bronce con una marca de verificación grabada.
- Mia lo recibe con las dos manos.
- Por la escalera de arriba baja vapor y olor a pan.

### Misión R03-N04-M1 · Anotá el grimorio

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Agregale anotaciones de tipos a las cuatro funciones del grimorio (parámetros y resultado), sin cambiar lo que hacen:

- `curar`: enteros.
- `nombres_vivos`: recibe una lista de tuplas `(nombre, vida)` y devuelve una lista de nombres.
- `buscar_objeto`: recibe un inventario `nombre → cantidad` y puede devolver `None`.
- `aplicar_a_todos`: recibe una función de entero a entero (`Callable`) y una lista de enteros.

Al final, mostrá `curar.__annotations__`.

#### Criterio de aprobación

- Anota parámetros y resultado de las cuatro funciones.
- Usa `list[tuple[str, int]]`, `dict[str, int]`, `int | None` y `Callable[[int], int]`.
- El comportamiento no cambia.

#### Código inicial

```python
def curar(vida, cantidad, maximo=100):
    return min(maximo, vida + cantidad)


def nombres_vivos(compania):
    return [nombre for nombre, vida in compania if vida > 0]


def buscar_objeto(inventario, nombre):
    return inventario.get(nombre)


def aplicar_a_todos(funcion, valores):
    return [funcion(v) for v in valores]


print(curar(80, 30))
print(nombres_vivos([("Mia", 30), ("Baldo", 0), ("Sila", 12)]))
print(buscar_objeto({"poción": 3}, "espada"))
print(aplicar_a_todos(lambda v: v * 2, [1, 2, 3]))
```

#### Salida esperada

```
100
['Mia', 'Sila']
None
[2, 4, 6]
{'vida': <class 'int'>, 'cantidad': <class 'int'>, 'maximo': <class 'int'>, 'return': <class 'int'>}
```

#### Solución de referencia

```python
from collections.abc import Callable


def curar(vida: int, cantidad: int, maximo: int = 100) -> int:
    return min(maximo, vida + cantidad)


def nombres_vivos(compania: list[tuple[str, int]]) -> list[str]:
    return [nombre for nombre, vida in compania if vida > 0]


def buscar_objeto(inventario: dict[str, int], nombre: str) -> int | None:
    return inventario.get(nombre)


def aplicar_a_todos(funcion: Callable[[int], int], valores: list[int]) -> list[int]:
    return [funcion(v) for v in valores]


print(curar(80, 30))
print(nombres_vivos([("Mia", 30), ("Baldo", 0), ("Sila", 12)]))
print(buscar_objeto({"poción": 3}, "espada"))
print(aplicar_a_todos(lambda v: v * 2, [1, 2, 3]))
print(curar.__annotations__)
```

### Misión R03-N04-M2 · Las pruebas del precio

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Escribí `precio_final(precio, descuento=0.0, iva=0.21)` (anotada, con docstring) que aplique el descuento, después el IVA, y redondee a 2 decimales; con precio negativo o descuento fuera de 0 a 1, lanza `ValueError`.

Escribí una función `probar(descripcion, condicion)` que muestre `[OK]` o `[FALLA]` y al menos **seis** pruebas: el caso normal, con descuento, IVA cero, el redondeo y los dos errores. Al final, mostrá `todo verde` si no falló ninguna.

#### Criterio de aprobación

- La función está anotada y documentada.
- Hay al menos seis pruebas, incluidos los dos casos de error.
- Las pruebas de error verifican que se lanza `ValueError`.

#### Salida esperada

```
[OK   ] sin descuento suma el IVA
[OK   ] el descuento va antes del IVA
[OK   ] IVA cero
[OK   ] redondea a 2 decimales
[OK   ] precio negativo es un error
[OK   ] descuento mayor que 1 es un error
todo verde
```

#### Solución de referencia

```python
def precio_final(precio: float, descuento: float = 0.0, iva: float = 0.21) -> float:
    """Aplica el descuento y después el IVA, redondeando a 2 decimales."""
    if precio < 0 or not 0 <= descuento <= 1:
        raise ValueError("precio o descuento inválido")
    return round(precio * (1 - descuento) * (1 + iva), 2)


fallas = 0


def probar(descripcion: str, condicion: bool) -> None:
    global fallas
    if not condicion:
        fallas += 1
    print(f"[{'OK   ' if condicion else 'FALLA'}] {descripcion}")


def lanza_valueerror(funcion, *args) -> bool:
    try:
        funcion(*args)
    except ValueError:
        return True
    return False


probar("sin descuento suma el IVA", precio_final(1000) == 1210.0)
probar("el descuento va antes del IVA", precio_final(1000, 0.10) == 1089.0)
probar("IVA cero", precio_final(1000, iva=0) == 1000.0)
probar("redondea a 2 decimales", precio_final(9.99, 0.15) == 10.27)
probar("precio negativo es un error", lanza_valueerror(precio_final, -5))
probar("descuento mayor que 1 es un error", lanza_valueerror(precio_final, 100, 1.5))
print("todo verde" if fallas == 0 else f"{fallas} pruebas fallaron")
```

### Misión R03-N04-M3 · El taller del Gremio

```meta
entrega: archivo
monedas: 4
xp: 10
entorno: local
extensiones: zip, py, txt, png, jpg
```

#### Consigna

En tu compu:

1. Creá una carpeta con un entorno virtual y activalo.
2. Instalá `pytest` y `mypy`.
3. Pasá tus pruebas de la misión 2 a un archivo `test_precio.py` con funciones `test_…` y `assert` (y `pytest.raises(ValueError)` para los errores), y corré `pytest -v`.
4. Corré `mypy` sobre tu código. Después **rompé un tipo a propósito** (por ejemplo, llamá a la función con un texto) y volvé a correr `mypy`.

Entregá un .zip con tus archivos y un `salida.txt` (o capturas) con lo que mostraron `pytest` y `mypy`.

#### Criterio de aprobación

- Trabaja dentro de un entorno virtual.
- `pytest -v` muestra todas las pruebas en verde.
- `mypy` detecta el tipo roto a propósito (se ve en la salida entregada).

### Encargo R03-N04-E1 · El conversor tipado

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

Modelá una lista de conversiones de unidades con una dataclass `Conversion(nombre: str, funcion: Callable[[float], float], unidad: str)`. Escribí `convertir_todo(valor, conversiones) -> dict[str, str]` y mostrá el resultado de convertir 100 con: Celsius a Fahrenheit, kilómetros a millas y kilos a libras.

#### Criterio de aprobación

- Todo está anotado, incluida la función guardada en la dataclass.
- Agregar una conversión nueva no obliga a tocar `convertir_todo`.

#### Salida esperada

```
Celsius a Fahrenheit     212.00 °F
Kilómetros a millas       62.14 mi
Kilos a libras           220.46 lb
```

#### Solución de referencia

```python
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Conversion:
    nombre: str
    funcion: Callable[[float], float]
    unidad: str


CONVERSIONES: list[Conversion] = [
    Conversion("Celsius a Fahrenheit", lambda c: c * 9 / 5 + 32, "°F"),
    Conversion("Kilómetros a millas", lambda km: km * 0.621371, "mi"),
    Conversion("Kilos a libras", lambda kg: kg * 2.20462, "lb"),
]


def convertir_todo(valor: float, conversiones: list[Conversion]) -> dict[str, str]:
    return {c.nombre: f"{c.funcion(valor):.2f} {c.unidad}" for c in conversiones}


for nombre, resultado in convertir_todo(100, CONVERSIONES).items():
    print(f"{nombre:<22}{resultado:>12}")
```

### Prueba del sello

#### ¿Python revisa las anotaciones de tipos al ejecutar?

No. Son para las personas, el editor y herramientas como `mypy`.

#### ¿Cómo anotás un parámetro que puede ser un entero o `None`?

`int | None`.

#### ¿Qué hace `assert condicion`?

Nada si la condición es verdadera; lanza `AssertionError` si es falsa.

#### ¿Qué casos conviene probar además del normal?

Los bordes (cero, vacío, el máximo) y los errores esperados.

#### ¿Para qué sirve un entorno virtual?

Para instalar los paquetes de un proyecto aislados, sin tocar el Python del sistema ni mezclar versiones entre proyectos.

### Soluciones (docente)

Reescrito desde cero a partir de `17-Python/24-TypeHints` (los archivos `combate.py`, `test_combate.py` y `sin_pytest.py` sirven para mostrar pytest en clase). La misión 3 es local porque necesita instalar paquetes.

## R03-N05 · asyncio: esperar sin frenar

```meta
tipo: tema
padre: R03-N04
precio: 10
criatura: troll
temas: conc.async, conc.sincronizacion
```

### Crónica

Del quinto piso llega el ruido de una cocina con mil cosas al fuego. La cocinera de la Torre prepara el banquete sola. No se queda mirando cómo hierve la sopa: pone el agua, mientras tanto amasa el pan, y mientras el pan se hornea, prepara el té. Una sola persona, muchas esperas a la vez.

—No se trata de tener más manos —dice la cocinera—, sino de **no quedarse quieta mientras algo espera**.

De pronto, el gran reloj se para del todo. Algo despierta en la cima.

### Objetivos

- Escribir corrutinas con `async def` y esperar con `await`.
- Correr varias tareas a la vez con `asyncio.gather` y `TaskGroup`.
- Poner límites de tiempo con `asyncio.wait_for` y proteger datos compartidos con `asyncio.Lock`.

### Antes de empezar

Funciones (R01-N08), excepciones (R02-N03) y generadores (R03-N01): una corrutina también se pausa y sigue.

### Explicación

#### El problema: esperar

Muchos programas pasan la mayor parte del tiempo **esperando**: la respuesta de un servidor, un archivo, un temporizador. Si cada espera frena todo, tres descargas de un segundo tardan tres segundos. Con **asyncio**, mientras una tarea espera, se avanza con otra: las tres tardan un segundo.

#### Corrutinas: `async def` y `await`

```python
import asyncio

async def preparar(plato, segundos):
    await asyncio.sleep(segundos)   # espera SIN frenar a las demás
    return plato

asyncio.run(preparar("sopa", 1))     # arranca el "bucle de eventos"
```

- `async def` define una **corrutina**. Llamarla no la ejecuta: devuelve algo que hay que **esperar**.
- `await algo` espera a que termine y, mientras tanto, deja que corran otras tareas.
- `await` solo se puede usar **adentro** de una función `async`.
- `asyncio.run(main())` es la puerta de entrada: se llama una vez, desde el código normal.
- Adentro de una corrutina se usa `asyncio.sleep`, **nunca** `time.sleep` (que frena todo).

#### Varias a la vez

- `await asyncio.gather(a(), b(), c())`: corre las tres a la vez y devuelve sus resultados **en el orden en que se pidieron**. Con `return_exceptions=True`, un error no cancela a las demás: aparece como resultado.
- `async with asyncio.TaskGroup() as grupo:` y `grupo.create_task(...)`: la forma moderna. Al salir del bloque, todas terminaron; si una falla, se cancelan las otras.

#### Límites de tiempo

`await asyncio.wait_for(tarea(), timeout=2)` lanza `TimeoutError` si tarda más de 2 segundos (y cancela la tarea).

#### Estado compartido: el candado

Si varias tareas leen y modifican lo mismo con un `await` en el medio, pueden pisarse: las dos leen 50, las dos suman 10 y queda 60 en lugar de 70. `asyncio.Lock` hace que entren **de a una**:

```python
async with candado:
    actual = progreso
    await guardar()
    progreso = actual + 10
```

#### asyncio no es paralelismo

Todo corre en **una sola** línea de ejecución, turnándose en cada `await`. Sirve para esperas (red, disco, temporizadores); para cálculos pesados no acelera nada.

### Código de ejemplo

```python
"""asyncio: muchas esperas a la vez, con una sola mano."""

import asyncio


async def preparar(plato, segundos):
    """Una corrutina: puede PAUSARSE en cada await mientras espera."""
    print(f"  empieza: {plato}")
    await asyncio.sleep(segundos)       # mientras espera, corren las otras
    print(f"  listo: {plato}")
    return plato


async def en_fila():
    for plato, segundos in [("sopa", 0.3), ("pan", 0.1), ("té", 0.2)]:
        await preparar(plato, segundos)     # una DESPUÉS de la otra


async def a_la_vez():
    # gather lanza las tres juntas y espera a que terminen todas
    return await asyncio.gather(preparar("sopa", 0.3), preparar("pan", 0.1), preparar("té", 0.2))


async def con_limite():
    try:
        await asyncio.wait_for(preparar("guiso", 2), timeout=0.2)
    except TimeoutError:
        print("  el guiso tardó demasiado: se cancela")


async def main():
    print("--- en fila (≈0.6 s) ---")
    await en_fila()
    print("--- a la vez (≈0.3 s) ---")
    resultados = await a_la_vez()
    print("platos:", resultados)
    print("--- con tiempo límite ---")
    await con_limite()


asyncio.run(main())
```

### Salida esperada

```
--- en fila (≈0.6 s) ---
  empieza: sopa
  listo: sopa
  empieza: pan
  listo: pan
  empieza: té
  listo: té
--- a la vez (≈0.3 s) ---
  empieza: sopa
  empieza: pan
  empieza: té
  listo: pan
  listo: té
  listo: sopa
platos: ['sopa', 'pan', 'té']
--- con tiempo límite ---
  empieza: guiso
  el guiso tardó demasiado: se cancela
```

### ¿Para qué sirve?

Un servidor web atiende a miles de personas a la vez esperando sus pedidos; un bot de chat responde varios mensajes mientras espera a la base de datos; un programa descarga cien archivos de internet en el tiempo de uno; un sistema de sensores lee muchos dispositivos al mismo tiempo. Bibliotecas modernas como FastAPI, aiohttp o discord.py están hechas sobre asyncio.

### Errores habituales

**Ogro: olvidar el `await`**: `preparar("sopa", 1)` sin `await` no hace nada y Python avisa:

```
RuntimeWarning: coroutine 'preparar' was never awaited
```

**Slime: `await` fuera de una función `async`**:

```
SyntaxError: 'await' outside async function
```

**Ogro: `time.sleep` adentro de una corrutina**: frena a **todas** las tareas; el programa se vuelve secuencial sin avisar.

**Troll: dos tareas que modifican lo mismo** con un `await` en el medio: se pisan y se pierden datos. Usá un `asyncio.Lock`.

**Goblin: llamar a `asyncio.run` dentro de una corrutina** (`RuntimeError: asyncio.run() cannot be called from a running event loop`): adentro se usa `await`.

### Micro-misión R03-N05-P1 · Esperar sin frenar

```meta
lugar: La cocina de la Torre
personajes: Mia, Gheco, la cocinera de la Torre
carta: async y await | async def preparar(): · await asyncio.sleep(1) · asyncio.run(main())
recompensa: xp 10, oro 10
```

#### Escena
La cocina de la Torre es un caos ordenado: ollas, hornos y una sola cocinera, de brazos fuertes y pañuelo en la cabeza.
—No me quedo mirando cómo hierve el agua —dice sin darse vuelta—. Pongo la olla y **espero sin frenar**.

#### Gheco sugiere
`async def` define una **corrutina**. Adentro, `await` espera algo (como `asyncio.sleep`) **dejando que otras tareas avancen**. Todo arranca con `asyncio.run(...)`.

#### Desafío
Esperá a que hierva la sopa.

#### Código inicial
```python
import asyncio

async def preparar(plato, segundos):
    ___ asyncio.sleep(segundos)
    return f"{plato} lista"

print(asyncio.run(preparar("sopa", 0.01)))
```

#### Salida esperada
```
sopa lista
```

#### Solución
```python
import asyncio

async def preparar(plato, segundos):
    await asyncio.sleep(segundos)
    return f"{plato} lista"

print(asyncio.run(preparar("sopa", 0.01)))
```

#### Al superarla
—Sopa lista —dice la cocinera, y por fin te mira—. Pero una sola cosa no es un banquete, chiquita.

#### Imagen
- La cocina de la Torre: ollas humeantes, hornos de piedra y engranajes en el techo.
- La cocinera de pañuelo en la cabeza revuelve una olla sin mirar.
- Mia con el pergamino, `await` brillando en verde.

### Micro-misión R03-N05-P2 · Tres cosas a la vez

```meta
lugar: La cocina de la Torre
personajes: Mia, Gheco, la cocinera de la Torre
carta: gather | await asyncio.gather(a(), b(), c()) · corren a la vez · devuelve en el orden en que se pidieron
recompensa: xp 10, oro 10
```

#### Escena
—Sopa, pan y té —dice la cocinera—. **A la vez**. Una sola persona, muchas esperas.

#### Gheco sugiere
`await asyncio.gather(a(), b(), c())` corre las tres corrutinas a la vez y devuelve sus resultados **en el orden en que las pediste**, aunque terminen en otro orden.

#### Desafío
Prepará los tres platos a la vez.

#### Código inicial
```python
import asyncio

async def preparar(plato, segundos):
    await asyncio.sleep(segundos)
    print(f"{plato}: listo")
    return plato

async def banquete():
    platos = await asyncio.___(
        preparar("sopa", 0.03),
        preparar("pan", 0.01),
        preparar("té", 0.02),
    )
    print(f"A la mesa: {platos}")

asyncio.run(banquete())
```

#### Salida esperada
```
pan: listo
té: listo
sopa: listo
A la mesa: ['sopa', 'pan', 'té']
```

#### Solución
```python
import asyncio

async def preparar(plato, segundos):
    await asyncio.sleep(segundos)
    print(f"{plato}: listo")
    return plato

async def banquete():
    platos = await asyncio.gather(
        preparar("sopa", 0.03),
        preparar("pan", 0.01),
        preparar("té", 0.02),
    )
    print(f"A la mesa: {platos}")

asyncio.run(banquete())
```

#### Al superarla
El pan sale primero, después el té, al final la sopa. Pero en la mesa quedan en el orden que pediste. La cocinera se seca las manos, conforme.

#### Imagen
- Tres platos que terminan a destiempo: pan, té, sopa, cada uno con un reloj de vapor encima.
- La mesa servida en orden: sopa, pan y té.

### Micro-misión R03-N05-P3 · El asado que no llega

```meta
lugar: La cocina de la Torre
personajes: Mia, Gheco, la cocinera de la Torre
carta: wait_for | await asyncio.wait_for(tarea(), timeout=2) · si tarda más: TimeoutError
recompensa: xp 10, oro 10
```

#### Escena
—El asado tarda una eternidad —se queja la cocinera—. Si no está a tiempo, se sirve sin asado. No espero para siempre.

#### Gheco sugiere
`await asyncio.wait_for(tarea(), timeout=s)` espera como mucho `s` segundos. Si se pasa, cancela la tarea y lanza `TimeoutError`.

#### Desafío
Ponele un límite de tiempo al asado.

#### Código inicial
```python
import asyncio

async def asado():
    await asyncio.sleep(1)
    return "asado"

async def main():
    try:
        print(await asyncio.___(asado(), timeout=0.05))
    except TimeoutError:
        print("Sin asado: se sirve lo que hay")

asyncio.run(main())
```

#### Salida esperada
```
Sin asado: se sirve lo que hay
```

#### Solución
```python
import asyncio

async def asado():
    await asyncio.sleep(1)
    return "asado"

async def main():
    try:
        print(await asyncio.wait_for(asado(), timeout=0.05))
    except TimeoutError:
        print("Sin asado: se sirve lo que hay")

asyncio.run(main())
```

#### Al superarla
El banquete se sirve a tiempo. El asado, cuando esté, será para la cena.

#### Imagen
- Un horno con un asado que sigue cocinándose; un relojito de arena se vacía encima.
- La cocinera sirve la mesa sin esperar.

### Micro-misión R03-N05-P4 · El candado de la despensa

```meta
lugar: La cocina de la Torre
personajes: Mia, Gheco, la cocinera de la Torre, Tilo
criatura: troll
carta: asyncio.Lock | async with candado: · de a una tarea por vez · evita que se pisen
recompensa: xp 15, oro 15
```

#### Escena
Vos y Tilo cargan la despensa a la vez: cada uno lee cuántas bolsas hay, suma 10 y anota. Había 50; tendrían que quedar 70. El cartel dice **60**. Un **troll** se ríe desde atrás de los sacos.

#### Gheco sugiere
Si dos tareas leen y modifican lo mismo con un `await` en el medio, se **pisan**: las dos leen 50. Con `async with candado:` (un `asyncio.Lock`), entran **de a una**.

#### Desafío
Que cada uno cargue con el candado puesto.

#### Código inicial
```python
import asyncio

bolsas = 50

async def cargar(candado):
    global bolsas
    async with ___:
        actual = bolsas
        await asyncio.sleep(0)
        bolsas = actual + 10

async def main():
    candado = asyncio.Lock()
    await asyncio.gather(cargar(candado), cargar(candado))
    print(f"Bolsas: {bolsas}")

asyncio.run(main())
```

#### Salida esperada
```
Bolsas: 70
```

#### Solución
```python
import asyncio

bolsas = 50

async def cargar(candado):
    global bolsas
    async with candado:
        actual = bolsas
        await asyncio.sleep(0)
        bolsas = actual + 10

async def main():
    candado = asyncio.Lock()
    await asyncio.gather(cargar(candado), cargar(candado))
    print(f"Bolsas: {bolsas}")

asyncio.run(main())
```

#### Al superarla
Setenta, justas. El troll se queda sin bolsas que esconder y se va bajo la mesa, refunfuñando.

#### Imagen
- Una despensa con sacos apilados y un candado de bronce en la puerta.
- Mia y Tilo cargan sacos de a uno; el cartel dice 70.
- Un troll refunfuña bajo la mesa.

### Micro-misión R03-N05-P5 · Que un plato quemado no arruine el banquete

```meta
lugar: La cocina de la Torre
personajes: Mia, Gheco, la cocinera de la Torre
carta: return_exceptions | gather(..., return_exceptions=True) · un error no cancela a los demás: queda como resultado
recompensa: xp 15, oro 15
```

#### Escena
El pan se quema. Y como era parte del `gather`, el error cancela **todo** el banquete.
—Un plato quemado no es motivo para tirar los demás —dice la cocinera.

#### Gheco sugiere
Con `return_exceptions=True`, si una de las tareas lanza un error, `gather` **no** cancela las demás: el error aparece en la lista de resultados, en su lugar.

#### Desafío
Que el error del pan quede como resultado y el resto se sirva.

#### Código inicial
```python
import asyncio

async def preparar(plato):
    await asyncio.sleep(0.01)
    if plato == "pan":
        raise ValueError("se quemó")
    return plato

async def main():
    resultados = await asyncio.gather(
        preparar("sopa"), preparar("pan"), preparar("té"), ___
    )
    for r in resultados:
        print(f"Error: {r}" if isinstance(r, Exception) else f"A la mesa: {r}")

asyncio.run(main())
```

#### Salida esperada
```
A la mesa: sopa
Error: se quemó
A la mesa: té
```

#### Solución
```python
import asyncio

async def preparar(plato):
    await asyncio.sleep(0.01)
    if plato == "pan":
        raise ValueError("se quemó")
    return plato

async def main():
    resultados = await asyncio.gather(
        preparar("sopa"), preparar("pan"), preparar("té"), return_exceptions=True
    )
    for r in resultados:
        print(f"Error: {r}" if isinstance(r, Exception) else f"A la mesa: {r}")

asyncio.run(main())
```

#### Al superarla
Sopa y té a la mesa; el pan, al tacho. La cocinera te da una palmada que casi te tira al piso.
Y entonces, todo se queda **quieto**. El tic-tac de la Torre se apaga. **El gran reloj se paró del todo.** Y desde la cima llega un ruido de engranajes que despiertan.

#### Imagen
- La mesa servida con sopa y té; un pan quemado humea en un rincón.
- Todos miran hacia arriba: el tic-tac se detuvo.
- Por la escalera baja una luz roja y el ruido de engranajes enormes.

### Misión R03-N05-M1 · El alumno que se desconecta

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Tres alumnos entregan una tarea en un aula virtual (una corrutina que espera un rato y devuelve `"<nombre> entregó"`). Tilo se desconecta: su corrutina lanza `ConnectionError`. Juntalos con `gather(..., return_exceptions=True)` y mostrá, en orden, quién entregó y qué problema hubo, sin que el error de Tilo corte a los demás.

#### Criterio de aprobación

- Usa `asyncio.gather` con `return_exceptions=True`.
- Distingue los errores con `isinstance(resultado, Exception)`.
- Mia y Sila entregan aunque Tilo falle.

#### Salida esperada

```
ok: Mia entregó
problema: Tilo se desconectó
ok: Sila entregó
```

#### Solución de referencia

```python
import asyncio


async def alumno(nombre, espera, falla=False):
    await asyncio.sleep(espera)
    if falla:
        raise ConnectionError(f"{nombre} se desconectó")
    return f"{nombre} entregó"


async def main():
    resultados = await asyncio.gather(
        alumno("Mia", 0.2), alumno("Tilo", 0.1, falla=True), alumno("Sila", 0.3),
        return_exceptions=True,
    )
    for r in resultados:
        print("problema:" if isinstance(r, Exception) else "ok:", r)


asyncio.run(main())
```

### Misión R03-N05-M2 · Los mapas que no llegan

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Simulá la descarga de tres mapas que tardan 0.1, 0.4 y 0.2 segundos. Descargalos uno por uno con `asyncio.wait_for(..., timeout=0.3)`: los que tardan más se cancelan con un aviso y el programa sigue con el siguiente.

#### Criterio de aprobación

- Usa `asyncio.wait_for` con `timeout`.
- Atrapa `TimeoutError` y sigue.
- La cueva (0.4 s) se cancela; el valle y la torre llegan.

#### Salida esperada

```
valle descargado
cueva: tardó más de 0.3 s, se cancela
torre descargado
```

#### Solución de referencia

```python
import asyncio


async def descargar(mapa, segundos):
    await asyncio.sleep(segundos)
    return f"{mapa} descargado"


async def main():
    pedidos = {"valle": 0.1, "cueva": 0.4, "torre": 0.2}
    for mapa, segundos in pedidos.items():
        try:
            print(await asyncio.wait_for(descargar(mapa, segundos), timeout=0.3))
        except TimeoutError:
            print(f"{mapa}: tardó más de 0.3 s, se cancela")


asyncio.run(main())
```

### Misión R03-N05-M3 · La meta compartida

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Tres jugadores aportan puntos a una meta común de 100 (una clase `Meta` con `progreso`). Cada aporte lee el progreso, espera `asyncio.sleep(0.01)` (la red) y guarda el nuevo valor, sin pasar de la meta. Corré los tres jugadores con un `asyncio.TaskGroup` y protegé el aporte con un `asyncio.Lock`.

Probá también **sin** el candado y anotá en un comentario qué pasa con el progreso final.

#### Criterio de aprobación

- Usa `asyncio.TaskGroup` y `create_task`.
- El aporte está protegido con `async with candado`.
- Con el candado, el progreso final es 90; hay un comentario que explica qué pasó sin él.

#### Salida esperada

```
progreso: 90/100
```

#### Solución de referencia

```python
import asyncio


class Meta:
    def __init__(self, objetivo):
        self.objetivo = objetivo
        self.progreso = 0
        self.candado = asyncio.Lock()

    async def aportar(self, nombre, cantidad):
        async with self.candado:            # de a uno: nadie pisa el aporte de otro
            actual = self.progreso
            await asyncio.sleep(0.01)       # la "red" tarda
            self.progreso = min(self.objetivo, actual + cantidad)


async def jugador(meta, nombre, aportes):
    for cantidad in aportes:
        await meta.aportar(nombre, cantidad)


async def main():
    meta = Meta(100)
    async with asyncio.TaskGroup() as grupo:
        grupo.create_task(jugador(meta, "Mia", [10, 15, 5]))
        grupo.create_task(jugador(meta, "Tilo", [20, 10]))
        grupo.create_task(jugador(meta, "Sila", [25, 5]))
    print(f"progreso: {meta.progreso}/{meta.objetivo}")


asyncio.run(main())
```

### Encargo R03-N05-E1 · La central de sensores

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

Una fábrica tiene tres sensores (horno, heladera, bomba), cada uno con una lista de lecturas y un límite. Escribí `vigilar(nombre, lecturas, intervalo)`, que "lea" cada valor esperando el intervalo y devuelva las alertas de las lecturas que superan el límite. Vigilá los tres a la vez con `gather` y mostrá todas las alertas juntas.

#### Criterio de aprobación

- Los tres sensores se vigilan a la vez con `gather`.
- Cada corrutina devuelve su lista de alertas.
- Hay 2 alertas: el horno y la heladera.

#### Salida esperada

```
2 alertas
 - horno: lectura 3 = 240 (límite 220)
 - heladera: lectura 3 = 12 (límite 8)
```

#### Solución de referencia

```python
import asyncio

SENSORES = {"horno": [180, 185, 240, 190], "heladera": [4, 5, 12, 6], "bomba": [60, 62, 61, 63]}
LIMITES = {"horno": 220, "heladera": 8, "bomba": 70}


async def vigilar(nombre, lecturas, intervalo):
    alertas = []
    for numero, valor in enumerate(lecturas, start=1):
        await asyncio.sleep(intervalo)
        if valor > LIMITES[nombre]:
            alertas.append(f"{nombre}: lectura {numero} = {valor} (límite {LIMITES[nombre]})")
    return alertas


async def main():
    todas = await asyncio.gather(*(vigilar(n, l, 0.05) for n, l in SENSORES.items()))
    alertas = [a for lista in todas for a in lista]
    print(f"{len(alertas)} alertas")
    for alerta in alertas:
        print(" -", alerta)


asyncio.run(main())
```

### Prueba del sello

#### ¿Qué devuelve llamar a una función `async` sin `await`?

Una corrutina sin ejecutar: hay que esperarla con `await` (o pasarla a `gather`, `create_task`…).

#### ¿Por qué adentro de una corrutina se usa `asyncio.sleep` y no `time.sleep`?

Porque `time.sleep` frena todo el programa; `asyncio.sleep` deja correr a las otras tareas mientras espera.

#### ¿En qué orden devuelve `gather` los resultados?

En el orden en que se pasaron las corrutinas, sin importar cuál terminó primero.

#### ¿asyncio usa varios núcleos del procesador?

No: todo corre en una sola línea de ejecución, turnándose en cada `await`. Sirve para esperas, no para cálculos pesados.

#### ¿Para qué sirve un `asyncio.Lock`?

Para que un tramo de código que modifica datos compartidos lo ejecute una tarea por vez.

### Soluciones (docente)

Reescrito desde cero a partir de `17-Python/30-Asyncio` (el original simulaba el aula cooperativa de Phaser). `asyncio.run` funciona en la plataforma (Pyodide), así que las misiones se hacen en el navegador.

## R03-N06 · Rendimiento: medir antes de optimizar

```meta
tipo: tema
padre: R03-N05
precio: 10
criatura: ogro
temas: cal.rendimiento, alg.complejidad
usa: col.conjuntos, col.pilas-colas
```

### Crónica

En el último piso, los aprendices discuten por qué atrasa el reloj: «es el péndulo», «son los engranajes», «es el aceite». La Mia del principio habría leído todos los manuales. Ahora saca un cronómetro y **mide** cada pieza. En cinco minutos encuentra la culpable. No era ninguna de las que decían.

—Nunca adivines dónde se va el tiempo —dice Maese Horas, sonriendo—. **Medilo**.

La pieza culpable es el corazón del Gólem.

### Objetivos

- Medir tiempos con `timeit` y encontrar lo lento con `cProfile`.
- Elegir la estructura de datos correcta (`set`, `dict`, `deque`).
- Reconocer los patrones lentos más comunes y sus reemplazos.

### Antes de empezar

Listas, diccionarios y conjuntos (R01), funciones y decoradores (R01 y R03-N03).

### Explicación

#### La regla

1. Primero, que el programa **funcione** (y tenga pruebas).
2. Si es lento, **medí** dónde.
3. Mejorá esa parte, y **volvé a medir**.

Optimizar sin medir lleva a código más complicado que no es más rápido.

#### `timeit`: comparar dos formas

```python
import timeit
timeit.timeit(lambda: sum(x * x for x in datos), number=100)
```

Ejecuta el código `number` veces y devuelve el tiempo total en segundos. Compará siempre con el **mismo** `number`, y en la misma compu (los tiempos cambian de una máquina a otra, y en el navegador todo es más lento).

#### `cProfile`: dónde se va el tiempo

`cProfile` ejecuta tu programa y anota cuántas veces se llamó cada función y cuánto tardó. Con `pstats` se ordena por tiempo acumulado (`cumulative`) y aparece, arriba, la función culpable.

#### La estructura correcta vale más que cualquier truco

| Operación | `list` | `set` / `dict` | `deque` |
|---|---|---|---|
| ¿está `x`? (`in`) | lento: recorre todo | **instantáneo** | lento |
| sacar del principio | lento: corre todo | — | **instantáneo** (`popleft`) |
| agregar al final | rápido | rápido | rápido |

Si vas a preguntar muchas veces "¿ya lo vi?", usá un `set`. Si armás una cola (el primero que entra, el primero que sale), usá `collections.deque`.

#### Complejidad: cómo crece el tiempo

Lo importante no es cuánto tarda con 10 datos, sino **cómo crece** con más:

- **O(n)**: el doble de datos, el doble de tiempo (recorrer una lista).
- **O(n²)**: el doble de datos, **cuatro veces** el tiempo (comparar todos contra todos: dos `for` anidados sobre la misma lista).
- **O(1)**: siempre lo mismo (buscar en un `set`).

Pasar de O(n²) a O(n) (por ejemplo, con un diccionario) gana más que cualquier micro-optimización.

#### Patrones lentos comunes

- Unir textos con `+=` en un bucle → `"".join(partes)`.
- Buscar con `in` en una lista grande, muchas veces → convertila en `set`.
- `lista.pop(0)` en una cola → `deque.popleft()`.
- Recalcular lo mismo una y otra vez → `lru_cache` (R03-N03).

Cuando Python puro no alcanza (millones de cálculos numéricos), se usa **numpy** (Senda del Reino), que hace los bucles en C.

### Código de ejemplo

```python
"""Rendimiento: medir antes de optimizar."""

import timeit
from collections import deque

datos = list(range(10_000))

# =========================================================
# timeit: comparar dos formas de hacer lo mismo
# =========================================================
t_bucle = timeit.timeit("t = 0\nfor x in datos:\n    t += x * x", globals=globals(), number=30)
t_sum = timeit.timeit("sum(x * x for x in datos)", globals=globals(), number=30)
print(f"bucle for:      {t_bucle:.3f} s")
print(f"sum(generador): {t_sum:.3f} s")

# =========================================================
# La estructura correcta vale más que cualquier truco
# =========================================================
nombres_lista = [f"heroe{i}" for i in range(10_000)]
nombres_set = set(nombres_lista)
t_lista = timeit.timeit(lambda: "heroe9999" in nombres_lista, number=100)
t_set = timeit.timeit(lambda: "heroe9999" in nombres_set, number=100)
print(f"buscar en list: {t_lista:.4f} s")
print(f"buscar en set:  {t_set:.4f} s")


def vaciar_lista(n):
    cola = list(range(n))
    while cola:
        cola.pop(0)          # cada pop(0) corre todos los demás un lugar


def vaciar_deque(n):
    cola = deque(range(n))
    while cola:
        cola.popleft()       # sacar del principio es instantáneo


print(f"cola con list.pop(0):   {timeit.timeit(lambda: vaciar_lista(10_000), number=1):.4f} s")
print(f"cola con deque.popleft: {timeit.timeit(lambda: vaciar_deque(10_000), number=1):.4f} s")

# =========================================================
# Unir textos: join en lugar de += en un bucle
# =========================================================
partes = ["runa"] * 10_000
t_mas = timeit.timeit("t = ''\nfor p in partes:\n    t += p", globals=globals(), number=20)
t_join = timeit.timeit("''.join(partes)", globals=globals(), number=20)
print(f"+= en bucle: {t_mas:.4f} s   join: {t_join:.4f} s")
```

### ¿Para qué sirve?

Una página que tarda 5 segundos pierde a la mitad de sus visitantes; un reporte que tarda una hora no sirve para decidir en el día. Medir y elegir bien las estructuras es lo que hace que un sistema de turnos, un buscador o un juego responda al instante aunque tenga miles de datos. Y en la nube, lo lento también cuesta más plata.

### Errores habituales

**Ogro: optimizar sin medir**: hacés el código más difícil de leer y la parte lenta era otra.

**Ogro: comparar tiempos distintos**: medir una versión con `number=10` y otra con `number=100`, o una en tu compu y otra en el navegador.

**Ogro: el O(n²) escondido**: `if x in lista` adentro de un `for` sobre otra lista grande es, en realidad, un bucle adentro de otro.

**Troll: optimizar y romper el resultado**: por eso, antes de medir, comprobá con un `assert` que la versión rápida da **lo mismo** que la lenta.

**Goblin: medir algo que se corta**: en la plataforma, un programa que tarda más de 5 segundos se corta. Achicá los datos para medir.

### Micro-misión R03-N06-P1 · Unir runas

```meta
lugar: La Torre del Reloj: el último piso
personajes: Mia, Gheco, Maese Horas
carta: join | "-".join(partes) une una lista de textos · más rápido que += en un bucle
recompensa: xp 10, oro 10
```

#### Escena
En el último piso, los aprendices discuten por qué atrasa el reloj. Uno pega las runas del registro de a una con `+=`, y el registro tarda una eternidad.
—Hay una forma de unirlas **de una sola vez** —dice Maese Horas.

#### Gheco sugiere
`separador.join(lista)` une todos los textos de la lista con el separador en el medio, de una sola vez. Pegar con `+=` en un bucle crea un texto nuevo en cada vuelta.

#### Desafío
Uní las runas con guiones.

#### Código inicial
```python
runas = ["tic", "tac", "tic", "tac"]
registro = "-".___(runas)
print(registro)
```

#### Salida esperada
```
tic-tac-tic-tac
```

#### Solución
```python
runas = ["tic", "tac", "tic", "tac"]
registro = "-".join(runas)
print(registro)
```

#### Al superarla
El registro sale entero, de un tirón. El aprendiz que pegaba de a una se pone colorado.

#### Imagen
- El último piso de la Torre: aprendices discutiendo frente al mecanismo del gran reloj, quieto.
- Una tira de runas que se une de golpe: «tic-tac-tic-tac».

### Micro-misión R03-N06-P2 · ¿Ya lo vi?

```meta
lugar: La Torre del Reloj: el último piso
personajes: Mia, Gheco, Maese Horas
carta: set | x in un_set es instantáneo · x in una_lista recorre todo · para «¿ya lo vi?», set
recompensa: xp 10, oro 10
```

#### Escena
—Para cada pieza que revisás, te fijás si ya la viste —dice Maese Horas—. Si lo anotás en una lista, cada pregunta la recorre **entera**. Con miles de piezas…

#### Gheco sugiere
Preguntar `x in lista` revisa uno por uno. En un `set`, la pregunta es **instantánea**, tenga lo que tenga. Para «¿ya lo vi?», usá un `set`: se crea con `set()` y se le agrega con `.add(x)`.

#### Desafío
Creá las piezas vistas como un `set`.

#### Código inicial
```python
revisadas = ["eje", "rueda", "eje", "aguja", "rueda"]
vistas = ___()
for pieza in revisadas:
    if pieza in vistas:
        print(f"{pieza}: repetida")
    vistas.add(pieza)
print(f"Distintas: {len(vistas)}")
```

#### Salida esperada
```
eje: repetida
rueda: repetida
Distintas: 3
```

#### Solución
```python
revisadas = ["eje", "rueda", "eje", "aguja", "rueda"]
vistas = set()
for pieza in revisadas:
    if pieza in vistas:
        print(f"{pieza}: repetida")
    vistas.add(pieza)
print(f"Distintas: {len(vistas)}")
```

#### Al superarla
Tres piezas distintas, dos repetidas. Maese Horas tacha «el péndulo» de la lista de sospechosos.

#### Imagen
- Una pizarra con sospechosos: «péndulo», «engranajes», «aceite»; el péndulo, tachado.

### Micro-misión R03-N06-P3 · La fila de las piezas

```meta
lugar: La Torre del Reloj: el último piso
personajes: Mia, Gheco, Maese Horas
carta: deque | from collections import deque · popleft() saca del principio al instante · pop(0) en una lista es lento
recompensa: xp 10, oro 10
```

#### Escena
—Las piezas que llegan se revisan en orden: la primera que entra, la primera que sale —dice el relojero—. Sacarlas del principio de una lista obliga a correr todas las demás.

#### Gheco sugiere
Una `deque` es una fila de doble punta: `append` agrega al final y `popleft()` saca del principio, **sin** mover las demás. Se importa de `collections`.

#### Desafío
Armá la fila con una `deque`.

#### Código inicial
```python
from collections import deque

fila = ___(["resorte", "eje", "aguja"])
fila.append("rueda")
while fila:
    print(f"Revisando: {fila.popleft()}")
```

#### Salida esperada
```
Revisando: resorte
Revisando: eje
Revisando: aguja
Revisando: rueda
```

#### Solución
```python
from collections import deque

fila = deque(["resorte", "eje", "aguja"])
fila.append("rueda")
while fila:
    print(f"Revisando: {fila.popleft()}")
```

#### Al superarla
La fila avanza sin trabarse. Maese Horas tacha «los engranajes».

#### Imagen
- Una cinta de piezas que avanza en fila hacia la mesa de revisión.
- La pizarra de sospechosos: péndulo y engranajes, tachados.

### Micro-misión R03-N06-P4 · Nunca adivines: medilo

```meta
lugar: La Torre del Reloj: el último piso
personajes: Mia, Gheco, Maese Horas
carta: Medir | contá o cronometrá cada parte · la culpable suele ser otra · Counter y max(..., key=...)
recompensa: xp 15, oro 15
```

#### Escena
—Es el aceite —dice un aprendiz.
—No, es el péndulo —dice otro.
La Mia del principio habría leído todos los manuales. Ahora sacás un contador y **medís** cuántas veces se mueve cada pieza en una vuelta del reloj.

#### Gheco sugiere
Antes de optimizar, **medí**. Un `Counter` cuenta cuántas veces aparece cada cosa, y `max(contador, key=contador.get)` da la que más aparece.

#### Desafío
Encontrá la pieza que más trabaja.

#### Código inicial
```python
from collections import Counter

movimientos = ["péndulo", "rueda", "corazón", "corazón", "eje", "corazón", "rueda", "corazón"]
conteo = Counter(movimientos)
culpable = max(conteo, key=___)
print(f"{culpable}: {conteo[culpable]} movimientos")
```

#### Salida esperada
```
corazón: 4 movimientos
```

#### Solución
```python
from collections import Counter

movimientos = ["péndulo", "rueda", "corazón", "corazón", "eje", "corazón", "rueda", "corazón"]
conteo = Counter(movimientos)
culpable = max(conteo, key=conteo.get)
print(f"{culpable}: {conteo[culpable]} movimientos")
```

#### Al superarla
Ni el aceite ni el péndulo: una pieza que nadie nombró, **el corazón**, se mueve el doble que las demás. Maese Horas sonríe.
—Nunca adivines dónde se va el tiempo. Medilo.

#### Imagen
- Un gráfico de barras de luz sobre el mecanismo: la barra del «corazón» es el doble que las demás.
- Los aprendices boquiabiertos; Maese Horas sonríe.

### Micro-misión R03-N06-P5 · Del cuadrado a la línea

```meta
lugar: La Torre del Reloj: el último piso
personajes: Mia, Gheco, Maese Horas
carta: Complejidad | dos for anidados: O(n²) · con un set: O(n) · el doble de datos, el doble de pasos y no el cuádruple
recompensa: xp 20, oro 20
item: Reloj de Arena
se abre: el Reloj de Arena: termina al instante una expedición en camino (se gasta al usarlo)
```

#### Escena
El corazón busca, entre cien dientes, dos que sumen 197, y lo hace comparando **todos contra todos**: casi cinco mil pasos por vuelta. Por eso atrasa el reloj.
—Recorrelos **una sola vez** —dice Maese Horas—, y anotá los que ya pasaron.

#### Gheco sugiere
Dos `for` anidados sobre la misma lista crecen como **n²**. Si por cada número preguntás si **ya viste su complemento** en un `set`, alcanza con recorrerlos una vez.

#### Desafío
Completá la pregunta: ¿ya pasó el diente que le falta a este para llegar a 197?

#### Código inicial
```python
dientes = list(range(100))
objetivo = 197
vistos = set()
pasos = 0
for d in dientes:
    pasos += 1
    if ___ in vistos:
        print(f"Par: {objetivo - d} + {d}")
        break
    vistos.add(d)
print(f"Pasos: {pasos}")
```

#### Salida esperada
```
Par: 98 + 99
Pasos: 100
```

#### Solución
```python
dientes = list(range(100))
objetivo = 197
vistos = set()
pasos = 0
for d in dientes:
    pasos += 1
    if objetivo - d in vistos:
        print(f"Par: {objetivo - d} + {d}")
        break
    vistos.add(d)
print(f"Pasos: {pasos}")
```

#### Al superarla
Cien pasos en vez de cinco mil. El reloj da un tic-tac fuerte… y se vuelve a frenar. Maese Horas te pone en la mano un **reloj de arena** chiquito.
—Para cuando no haya tiempo. Se usa una vez.
Arriba, algo enorme se mueve: **el corazón del reloj es el corazón del Gólem**.

#### Imagen
- Maese Horas pone un reloj de arena chiquito, con arena verde luminosa, en la mano de Mia.
- El mecanismo del gran reloj, con un corazón de engranajes que late en rojo.
- Por el hueco de la escalera, arriba, se asoma un ojo enorme de bronce.

### Misión R03-N06-M1 · Unir runas

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Con una lista de 5000 textos, uní todo de dos maneras: con `+=` en un bucle y con `"".join(...)`. Primero comprobá con `assert` que dan **lo mismo**; después medí las dos con `timeit` (`number=20`) y mostrá cuántas veces más rápida es una que la otra.

#### Criterio de aprobación

- Comprueba con `assert` que los dos resultados son iguales.
- Mide las dos versiones con el mismo `number`.
- Muestra la comparación.

#### Solución de referencia

```python
import timeit

partes = [f"línea {i}\n" for i in range(5_000)]


def con_mas():
    texto = ""
    for parte in partes:
        texto += parte
    return texto


def con_join():
    return "".join(partes)


assert con_mas() == con_join()          # primero: que den lo mismo
t_mas = timeit.timeit(con_mas, number=20)
t_join = timeit.timeit(con_join, number=20)
print(f"+= : {t_mas:.4f} s")
print(f"join: {t_join:.4f} s")
print(f"join es {t_mas / t_join:.0f} veces más rápido")
```

### Misión R03-N06-M2 · El culpable de la lentitud

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Perfilá con `cProfile` un programa que calcula los números primos hasta 20.000 y los pares de "primos gemelos" (p y p + 2). Mostrá el resultado y las 5 funciones con más tiempo acumulado con `pstats`. En un comentario, decí qué función se lleva el tiempo y por qué (¿cuántas veces se la llama?).

#### Criterio de aprobación

- Usa `cProfile.Profile()` con `enable`/`disable` (o `cProfile.run`).
- Muestra las estadísticas ordenadas por `cumulative`.
- Un comentario identifica la función culpable y cuántas veces se llama.

#### Solución de referencia

```python
import cProfile
import pstats


def es_primo(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True


def primos_hasta(limite):
    return [n for n in range(limite) if es_primo(n)]


def informe():
    primos = primos_hasta(20_000)
    gemelos = [(p, p + 2) for p in primos if es_primo(p + 2)]
    return len(primos), len(gemelos)


perfil = cProfile.Profile()
perfil.enable()
resultado = informe()
perfil.disable()
print("primos y pares de gemelos:", resultado)
pstats.Stats(perfil).sort_stats("cumulative").print_stats(5)
```

### Misión R03-N06-M3 · Del cuadrado a la grilla

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

La detección de choques compara todas las parejas de entidades: O(n²). Escribí una versión que reparta las entidades en **celdas** de 5×5 con un diccionario `(x // 5, y // 5) → [índices]` y compare cada entidad solo con las de su celda y las vecinas.

Con 800 entidades (`random.Random(1)`), comprobá que las dos versiones cuentan los mismos choques y medí cuánto tarda cada una.

#### Criterio de aprobación

- Las dos versiones cuentan los mismos choques (127).
- La versión rápida usa un diccionario de celdas y revisa solo las 9 celdas vecinas.
- Mide las dos y muestra la comparación.

#### Solución de referencia

```python
import random
import timeit


def crear(cantidad, semilla=1):
    azar = random.Random(semilla)
    return [(azar.uniform(0, 500), azar.uniform(0, 500)) for _ in range(cantidad)]


def choques_lento(entidades):
    """Compara TODAS las parejas: O(n²)."""
    choques = 0
    for i in range(len(entidades)):
        for j in range(i + 1, len(entidades)):
            (x1, y1), (x2, y2) = entidades[i], entidades[j]
            if abs(x1 - x2) < 5 and abs(y1 - y2) < 5:
                choques += 1
    return choques


def choques_rapido(entidades):
    """Reparte en celdas de 5x5 y compara solo con las celdas vecinas."""
    celdas = {}
    for i, (x, y) in enumerate(entidades):
        celdas.setdefault((int(x // 5), int(y // 5)), []).append(i)
    choques = 0
    for (cx, cy), indices in celdas.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in celdas.get((cx + dx, cy + dy), []):
                    for i in indices:
                        if i < j:
                            (x1, y1), (x2, y2) = entidades[i], entidades[j]
                            if abs(x1 - x2) < 5 and abs(y1 - y2) < 5:
                                choques += 1
    return choques


entidades = crear(800)
print("choques (lento): ", choques_lento(entidades))
print("choques (rápido):", choques_rapido(entidades))
t_lento = timeit.timeit(lambda: choques_lento(entidades), number=1)
t_rapido = timeit.timeit(lambda: choques_rapido(entidades), number=1)
print(f"el rápido tarda {t_rapido / t_lento:.0%} de lo que tarda el lento")
```

### Encargo R03-N06-E1 · Los correos sin repetir

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

El Gremio tiene una lista de correos con repetidos. Sacá los repetidos **conservando el orden** en que llegaron, usando un `set` para saber cuáles ya viste. Mostrá también el atajo con `dict.fromkeys`.

#### Criterio de aprobación

- Usa un `set` para "ya lo vi" (no `in` sobre la lista de resultados).
- Conserva el orden de llegada.

#### Salida esperada

```
['mia@valle.com', 'tilo@valle.com', 'sila@valle.com', 'baldo@valle.com']
atajo con dict.fromkeys: ['mia@valle.com', 'tilo@valle.com', 'sila@valle.com', 'baldo@valle.com']
```

#### Solución de referencia

```python
correos = ["mia@valle.com", "tilo@valle.com", "mia@valle.com", "sila@valle.com",
           "tilo@valle.com", "baldo@valle.com", "mia@valle.com"]

# Sin repetidos y en el orden en que llegaron: un set para "ya lo vi", una lista para el orden
vistos = set()
unicos = []
for correo in correos:
    if correo not in vistos:        # buscar en un set es instantáneo
        vistos.add(correo)
        unicos.append(correo)

print(unicos)
print("atajo con dict.fromkeys:", list(dict.fromkeys(correos)))
```

### Prueba del sello

#### ¿Qué conviene hacer antes de optimizar?

Que funcione, tener pruebas y medir dónde se va el tiempo.

#### ¿Por qué `x in un_set` es mucho más rápido que `x in una_lista`?

Porque el set busca por hash, directo; la lista tiene que recorrerse elemento por elemento.

#### ¿Qué estructura usarías para una cola donde se saca del principio?

`collections.deque`, con `popleft()`.

#### Si un algoritmo es O(n²), ¿qué pasa con el tiempo al duplicar los datos?

Se multiplica por cuatro.

#### ¿Cómo unís muchos textos de forma eficiente?

Con `"".join(lista)`, en lugar de `+=` en un bucle.

### Soluciones (docente)

Reescrito desde cero a partir de `17-Python/31-Rendimiento`, con datos más chicos para que entre en los 5 segundos del navegador. Las misiones no tienen salida esperada porque los tiempos cambian en cada ejecución.

## R03-N07 · Jefe: el Golem del Reloj

```meta
tipo: jefe
padre: R03-N06
precio: 10
criatura: dragon
insignia: Sello del Reloj
insignia_descripcion: Detuviste al Golem del Reloj: iterás, decorás y esperás como un artífice.
usa: func.iteradores, func.decoradores, conc.async
```

### Crónica

En la cima de la Torre despierta el **Gólem del Reloj**. De su pecho salen oleadas de engranajes, resortes y péndulos, una tras otra, sin fin. Y cada siete oleadas, aparece él.

—Contalas sin guardarlas todas —dice {mentor}—. Ordenalas, agrupalas, probá cada pieza y medí dónde está el problema. Y cuando llegue el Gólem, que tus tres torres lo esperen **a la vez**.

### Objetivos

- Combinar generadores, decoradores y herramientas funcionales en un mismo problema.
- Coordinar varias tareas asincrónicas que comparten una cola de trabajo.

### Antes de empezar

Toda la rama Iteración y calidad. Proyecto integrador.

### Explicación

#### Un generador que se corta a sí mismo

Un generador puede terminar cuando se cumple una condición: un `return` adentro de un generador lo termina (el `for` que lo recorre se detiene).

```python
def hasta_el_golem(oleadas):
    for oleada in oleadas:
        yield oleada
        if oleada["golem"]:
            return
```

#### Decorar un generador

Un decorador puede envolver un generador si la envoltura también es generador: recorre el original y reenvía cada valor con `yield`, contando o registrando lo que pasa.

#### Productores y consumidores con `asyncio.Queue`

Una `asyncio.Queue` es una fila de trabajo compartida: `put_nowait` agrega, `await cola.get()` saca (y espera si está vacía). Varias tareas (las torres) toman trabajo de la misma fila hasta recibir una señal de fin (`None`, una por torre).

### ¿Para qué sirve?

Así funcionan los sistemas que procesan trabajo en cola: los pedidos de un delivery que se reparten entre repartidores, los videos que se suben a una plataforma y se convierten en segundo plano, los correos que se envían de a tandas. Un generador produce el trabajo, otros lo consumen a la vez.

### Errores habituales

El Golem combina las criaturas de la Torre:

- **Ogro**: un generador infinito sin corte (el Golem nunca "llega" y el programa se corta a los 5 segundos).
- **Ogro**: `groupby` sin ordenar antes.
- **Troll**: olvidar mandar una señal de fin por cada torre: alguna queda esperando para siempre en `cola.get()`.
- **Ogro**: el decorador que no reenvía los valores (`yield`) y "se come" las oleadas.

### Micro-misión R03-N07-P1 · Las oleadas hasta el Gólem

```meta
lugar: La cima de la Torre del Reloj
personajes: Mia, Gheco, Tilo, Ofidia
criatura: ogro
carta: return en un generador | lo termina · el for que lo recorre se detiene
recompensa: xp 15, oro 15
```

#### Escena
La cima de la Torre es una plataforma abierta, con el cielo lleno de auroras. En el centro, el **Gólem del Reloj**: bronce, engranajes y un corazón rojo. De su pecho salen oleadas de piezas, una tras otra.
—Contalas sin guardarlas todas —dice {mentor}—. Y pará cuando llegue él.

#### Gheco sugiere
Un `return` adentro de un generador lo **termina**: el `for` que lo recorre se detiene ahí, aunque queden datos.

#### Desafío
Cortá el generador justo después de la oleada del Gólem.

#### Código inicial
```python
def hasta_el_golem(oleadas):
    for oleada in oleadas:
        yield oleada
        if oleada == "GÓLEM":
            ___

oleadas = ["engranajes", "resortes", "péndulos", "GÓLEM", "engranajes", "resortes"]
for oleada in hasta_el_golem(oleadas):
    print(oleada)
```

#### Salida esperada
```
engranajes
resortes
péndulos
GÓLEM
```

#### Solución
```python
def hasta_el_golem(oleadas):
    for oleada in oleadas:
        yield oleada
        if oleada == "GÓLEM":
            return

oleadas = ["engranajes", "resortes", "péndulos", "GÓLEM", "engranajes", "resortes"]
for oleada in hasta_el_golem(oleadas):
    print(oleada)
```

#### Al superarla
Tres oleadas y el Gólem da un paso al frente. Detrás de él, las oleadas que vendrían se quedan quietas: no las pediste.

#### Imagen
- La cima de la Torre bajo auroras cian; el Gólem del Reloj, de bronce, con un corazón rojo de engranajes.
- Oleadas de piezas que salen de su pecho y se detienen en el aire.
- Mia al frente, Tilo con la pértiga, Ofidia atrás, serena.

### Micro-misión R03-N07-P2 · Ordenalas y agrupalas

```meta
lugar: La cima de la Torre del Reloj
personajes: Mia, Gheco, Tilo
carta: Repaso | sorted + groupby + len(list(grupo)) · ordená por la misma clave antes de agrupar
recompensa: xp 15, oro 15
```

#### Escena
El Gólem tira una lluvia de piezas mezcladas. Para saber qué viene, tenés que **agruparlas por tipo** y contarlas.

#### Gheco sugiere
Lo del segundo piso: `groupby` agrupa los consecutivos, así que primero `sorted`. Contá cada grupo con `len(list(grupo))`.

#### Desafío
Agrupá las piezas por tipo y contalas.

#### Código inicial
```python
from itertools import groupby

lluvia = ["péndulo", "resorte", "engranaje", "resorte", "engranaje", "engranaje"]
for tipo, grupo in groupby(___):
    print(f"{tipo}: {len(list(grupo))}")
```

#### Salida esperada
```
engranaje: 3
péndulo: 1
resorte: 2
```

#### Solución
```python
from itertools import groupby

lluvia = ["péndulo", "resorte", "engranaje", "resorte", "engranaje", "engranaje"]
for tipo, grupo in groupby(sorted(lluvia)):
    print(f"{tipo}: {len(list(grupo))}")
```

#### Al superarla
Tres engranajes, un péndulo y dos resortes. Ya sabés qué viene, y Tilo los va desviando con la pértiga.

#### Imagen
- Una lluvia de piezas que se ordena en el aire en tres columnas.
- Tilo desvía piezas con la pértiga del farol verde.

### Micro-misión R03-N07-P3 · La torre probada

```meta
lugar: La cima de la Torre del Reloj
personajes: Mia, Gheco, Tilo
carta: Repaso | assert antes de la batalla · si una pieza falla, que sea en el taller
recompensa: xp 15, oro 15
```

#### Escena
Armás tres torres de defensa. Antes de ponerlas a disparar, las **probás**. Una dispara de más: hace el doble de daño contra todos, también contra Tilo.

#### Gheco sugiere
Probá la función con casos que conocés. Si el `assert` falla, arreglá la **función**.

#### Desafío
Arreglá `danio`: el bonus de 2 es solo contra el Gólem.

#### Código inicial
```python
def danio(base: int, objetivo: str) -> int:
    return base * 2

assert danio(10, "GÓLEM") == 20, "doble contra el Gólem"
assert danio(10, "engranaje") == 10, "normal contra las piezas"
assert danio(0, "GÓLEM") == 0, "borde: sin daño"
print("Las torres están probadas")
```

#### Salida esperada
```
Las torres están probadas
```

#### Solución
```python
def danio(base: int, objetivo: str) -> int:
    if objetivo == "GÓLEM":
        return base * 2
    return base

assert danio(10, "GÓLEM") == 20, "doble contra el Gólem"
assert danio(10, "engranaje") == 10, "normal contra las piezas"
assert danio(0, "GÓLEM") == 0, "borde: sin daño"
print("Las torres están probadas")
```

#### Al superarla
Las tres torres pasan las pruebas. Tilo suspira aliviado: ya no corre peligro.

#### Imagen
- Tres torres de defensa de bronce con luces verdes de «probada».
- Tilo, aliviado, se seca la frente.

### Micro-misión R03-N07-P4 · Las tres torres a la vez

```meta
lugar: La cima de la Torre del Reloj
personajes: Mia, Gheco, Tilo, Ofidia
criatura: troll
carta: asyncio.Queue | put_nowait agrega · await cola.get() saca · un None de fin por cada torre
recompensa: xp 20, oro 20
```

#### Escena
—Que tus tres torres lo esperen **a la vez** —dice {mentor}—. Una fila de piezas, y cada torre toma la próxima.
Pero cuidado: un **troll** se esconde en las torres que quedan esperando para siempre.

#### Gheco sugiere
Una `asyncio.Queue` es una fila compartida: `put_nowait` agrega y `await cola.get()` saca (y espera si está vacía). Para que cada torre sepa que terminó, mandá **un `None` por torre**.

#### Desafío
Mandá una señal de fin para cada torre.

#### Código inicial
```python
import asyncio

async def torre(nombre, cola):
    while True:
        pieza = await cola.get()
        if pieza is None:
            print(f"{nombre}: listo")
            return
        print(f"{nombre} derriba {pieza}")
        await asyncio.sleep(0)

async def main():
    cola = asyncio.Queue()
    for pieza in ["engranaje", "resorte", "péndulo"]:
        cola.put_nowait(pieza)
    for _ in range(___):
        cola.put_nowait(None)
    await asyncio.gather(torre("Torre A", cola), torre("Torre B", cola), torre("Torre C", cola))

asyncio.run(main())
```

#### Salida esperada
```
Torre A derriba engranaje
Torre B derriba resorte
Torre C derriba péndulo
Torre A: listo
Torre B: listo
Torre C: listo
```

#### Solución
```python
import asyncio

async def torre(nombre, cola):
    while True:
        pieza = await cola.get()
        if pieza is None:
            print(f"{nombre}: listo")
            return
        print(f"{nombre} derriba {pieza}")
        await asyncio.sleep(0)

async def main():
    cola = asyncio.Queue()
    for pieza in ["engranaje", "resorte", "péndulo"]:
        cola.put_nowait(pieza)
    for _ in range(3):
        cola.put_nowait(None)
    await asyncio.gather(torre("Torre A", cola), torre("Torre B", cola), torre("Torre C", cola))

asyncio.run(main())
```

#### Al superarla
Las tres torres derriban una pieza cada una, a la vez, y se apagan juntas. El Gólem, sin piezas, queda solo frente a vos.

#### Imagen
- Tres torres que disparan a la vez a tres piezas distintas.
- El Gólem, sin piezas a su alrededor, solo en la plataforma.
- Ofidia asiente desde atrás.

### Micro-misión R03-N07-P5 · El corazón del Gólem

```meta
lugar: La cima de la Torre del Reloj
personajes: Mia, Gheco, Tilo, Ofidia, Maese Horas
criatura: dragón
carta: Todo junto | generador + decorador que cuenta · medir antes de golpear
recompensa: xp 25, oro 30
item: Túnica Encendida
```

#### Escena
El corazón del Gólem late cada vez más rápido. Para llegar a él, tus golpes tienen que pasar por un decorador que los **cuenta**, y salir de un generador que los da **de a uno**.

#### Gheco sugiere
Un decorador puede envolver un **generador**, si la envoltura también es generador: recorre el original con `for` y reenvía cada valor con `yield`. Si no reenvía, se «come» los golpes.

#### Desafío
Reenviá cada golpe desde la envoltura.

#### Código inicial
```python
import functools

def contar(func):
    @functools.wraps(func)
    def envoltura(*args):
        for n, golpe in enumerate(func(*args), start=1):
            print(f"golpe {n}")
            ___ golpe
    return envoltura

@contar
def golpes(fuerza):
    for _ in range(3):
        yield fuerza

vida = 60
for g in golpes(20):
    vida -= g
print(f"Al corazón le queda: {vida}")
```

#### Salida esperada
```
golpe 1
golpe 2
golpe 3
Al corazón le queda: 0
```

#### Solución
```python
import functools

def contar(func):
    @functools.wraps(func)
    def envoltura(*args):
        for n, golpe in enumerate(func(*args), start=1):
            print(f"golpe {n}")
            yield golpe
    return envoltura

@contar
def golpes(fuerza):
    for _ in range(3):
        yield fuerza

vida = 60
for g in golpes(20):
    vida -= g
print(f"Al corazón le queda: {vida}")
```

#### Al superarla
Tres golpes contados, y el corazón del Gólem se apaga. El gigante de bronce se arrodilla despacio y se queda quieto, como una estatua más de la Ciudadela.
Abajo, **el gran reloj vuelve a andar**: tic-tac, tic-tac, por todo el Valle.
Mirás tu túnica: las runas se encendieron **enteras**, de los pies a la capucha. Es la **Túnica Encendida**.

#### Imagen
- El Gólem del Reloj arrodillado y quieto, con el corazón apagado, bajo las auroras.
- Mia de pie, con la túnica encendida entera en violeta, de los pies a la capucha.
- Tilo, Gheco y Ofidia la miran; Maese Horas llega corriendo por la escalera.
- El gran reloj de la Torre, con las agujas en movimiento.

### Misión R03-N07-M1 · Las oleadas del Golem

```meta
entrega: codigo
monedas: 6
xp: 30
```

#### Consigna

1. Escribí el generador infinito `oleadas_del_golem(semilla)`: cada oleada es un diccionario con `numero`, `enemigos` (3 tuplas `(tipo, poder)`, con tipo al azar entre engranaje, resorte y péndulo, y poder entre 5 y 20, usando `random.Random(semilla)`) y `golem` (verdadero cada 7 oleadas).
2. Decoralo con `@registrar`, un decorador que cuente cuántas oleadas se generaron (en un atributo de la envoltura).
3. Escribí el generador `hasta_el_golem(oleadas)`, que entregue oleadas hasta la del Golem inclusive.
4. Con la semilla 12: mostrá cuántas oleadas hubo, las 3 más fuertes (por poder total), y por cada tipo de enemigo cuántos hubo y su poder total (con `groupby`).

#### Criterio de aprobación

- Los dos generadores y el decorador funcionan juntos (el decorador reenvía con `yield`).
- Usa `sorted` con `key` y `groupby` sobre los datos ordenados.
- Con la semilla 12 hay 7 oleadas y las más fuertes son la 2, la 1 y la 5.

#### Salida esperada

```
oleadas hasta el Golem: 7 (generadas: 7)
las 3 más fuertes: [2, 1, 5]
  engranaje   9 enemigos, poder total 119
  péndulo     8 enemigos, poder total 107
  resorte     4 enemigos, poder total  50
primeras 2: [1, 2]
```

#### Solución de referencia

```python
import functools
import random
from itertools import groupby, islice


def registrar(func):
    """Cuenta cuántas oleadas generó el reloj."""
    @functools.wraps(func)
    def envoltura(*args, **kwargs):
        for oleada in func(*args, **kwargs):
            envoltura.generadas += 1
            yield oleada
    envoltura.generadas = 0
    return envoltura


@registrar
def oleadas_del_golem(semilla: int):
    azar = random.Random(semilla)
    tipos = ["engranaje", "resorte", "péndulo"]
    numero = 1
    while True:
        enemigos = [(azar.choice(tipos), azar.randint(5, 20)) for _ in range(3)]
        yield {"numero": numero, "enemigos": enemigos, "golem": numero % 7 == 0}
        numero += 1


def hasta_el_golem(oleadas):
    """Entrega oleadas hasta la del Golem inclusive."""
    for oleada in oleadas:
        yield oleada
        if oleada["golem"]:
            return


todas = list(hasta_el_golem(oleadas_del_golem(semilla=12)))
poder = lambda o: sum(p for _, p in o["enemigos"])

print(f"oleadas hasta el Golem: {len(todas)} (generadas: {oleadas_del_golem.generadas})")
print("las 3 más fuertes:", [o["numero"] for o in sorted(todas, key=poder, reverse=True)[:3]])
enemigos = sorted((e for o in todas for e in o["enemigos"]), key=lambda e: e[0])
for tipo, grupo in groupby(enemigos, key=lambda e: e[0]):
    poderes = [p for _, p in grupo]
    print(f"  {tipo:<10} {len(poderes):>2} enemigos, poder total {sum(poderes):>3}")
print("primeras 2:", [o["numero"] for o in islice(todas, 2)])
```

### Misión R03-N07-M2 · Las tres torres

```meta
entrega: codigo
monedas: 6
xp: 30
```

#### Consigna

Tres torres (Norte, Sur y Este) defienden a la vez. Cargá en una `asyncio.Queue` esta horda y, al final, un `None` por torre:

```python
horda = [("engranaje", 20), ("resorte", 5), ("péndulo", 35), ("engranaje", 10),
         ("resorte", 15), ("péndulo", 25), ("GOLEM", 60)]
```

Cada torre es una corrutina que saca enemigos de la cola, tarda `vida / 100` segundos en derribarlo (`asyncio.sleep`) y lo anota en un diccionario `torre → derribados`, hasta recibir `None`. Corré las tres con `gather`, mostrá qué derribó cada una y si cayó el Golem.

#### Criterio de aprobación

- Usa una `asyncio.Queue` compartida y un `None` de fin por torre.
- Las torres corren a la vez con `gather`.
- Resultado: Sur derriba al Golem.

#### Salida esperada

```
Norte engranaje(20), péndulo(25)
Sur   resorte(5), engranaje(10), resorte(15), GOLEM(60)
Este  péndulo(35)
¿cayó el Golem? True
```

#### Solución de referencia

```python
import asyncio


async def torre(nombre: str, cola: asyncio.Queue, derribados: dict[str, list[str]]) -> None:
    while True:
        enemigo = await cola.get()
        if enemigo is None:                 # la señal de fin
            return
        tipo, vida = enemigo
        await asyncio.sleep(vida / 100)     # tarda más con los enemigos fuertes
        derribados[nombre].append(f"{tipo}({vida})")


async def main() -> None:
    cola: asyncio.Queue = asyncio.Queue()
    horda = [("engranaje", 20), ("resorte", 5), ("péndulo", 35), ("engranaje", 10),
             ("resorte", 15), ("péndulo", 25), ("GOLEM", 60)]
    for enemigo in horda:
        cola.put_nowait(enemigo)
    torres = ["Norte", "Sur", "Este"]
    for _ in torres:
        cola.put_nowait(None)

    derribados: dict[str, list[str]] = {t: [] for t in torres}
    await asyncio.gather(*(torre(t, cola, derribados) for t in torres))
    for nombre, lista in derribados.items():
        print(f"{nombre:<6}{', '.join(lista)}")
    print("¿cayó el Golem?", any("GOLEM" in e for lista in derribados.values() for e in lista))


asyncio.run(main())
```

### Encargo R03-N07-E1 · El cronista de la Torre

```meta
entrega: codigo
monedas: 2
xp: 20
```

#### Consigna

Escribí un decorador `@medir` que guarde en una lista (atributo de la envoltura) cuánto tardó cada llamada. Decorá una función que ordena una lista y llamala con 1.000, 10.000 y 100.000 elementos. Mostrá los tiempos en milisegundos: ¿crecen igual que la cantidad de datos?

#### Criterio de aprobación

- El decorador guarda cada duración sin cambiar el resultado de la función.
- Muestra los tres tiempos en milisegundos.

#### Solución de referencia

```python
import functools
import time


def medir(func):
    @functools.wraps(func)
    def envoltura(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        envoltura.tiempos.append(time.perf_counter() - inicio)
        return resultado
    envoltura.tiempos = []
    return envoltura


@medir
def ordenar(datos):
    return sorted(datos)


for tamanio in [1_000, 10_000, 100_000]:
    ordenar(list(range(tamanio, 0, -1)))
for tamanio, t in zip([1_000, 10_000, 100_000], ordenar.tiempos):
    print(f"{tamanio:>7} elementos: {t * 1000:.2f} ms")
```

### Prueba del sello

#### ¿Cómo termina un generador antes de tiempo?

Con un `return` adentro: el `for` que lo recorre se detiene.

#### ¿Qué tiene que hacer un decorador que envuelve a un generador?

Ser también un generador: recorrer el original y reenviar cada valor con `yield`.

#### ¿Por qué hace falta un `None` por torre en la cola?

Porque cada torre termina al recibir uno; si falta, alguna queda esperando para siempre.

### Soluciones (docente)

Proyecto integrador nuevo. Los tiempos de la misión 2 están elegidos para que no haya empates: el reparto de la cola da siempre el mismo resultado.

## R03-N08 · La Encrucijada

```meta
tipo: ventana
padre: R03-N07
precio: 10
```

### Crónica

El reloj del Valle vuelve a andar. Mia baja de la Torre y el camino se abre en varios senderos: **la Encrucijada**. {mentor} se sienta al sol en una piedra del puente y le cuenta lo que vio hace mucho: un viajero con las manos manchadas de plomo, que buscaba la lengua más clara del mundo y siguió camino hacia las Forjas.

Mia levanta el pergamino, ya lleno, contra la luz del reloj. Por fin se lee la marca de agua: **un vitral, y debajo, «para quien llegue»**.

Tilo se queda en el Valle, como aprendiz de {mentor}. Gheco señala los caminos: las **Sendas** del Valle, y el que baja hacia **las Forjas**.

—Antes de elegir, mirá hacia atrás. ¿Qué te llevás de este viaje?

### Objetivos

- Repasar todo el camino principal y reconocer lo que aprendiste.
- Conocer las Sendas optativas que salen de acá.

### Explicación

#### Lo que ya sabés hacer

- **Fundamentos**: tipos, operadores, textos, decisiones y bucles, listas, diccionarios, referencias, funciones, recursión y módulos.
- **Objetos y errores**: clases, herencia y polimorfismo, excepciones, archivos, JSON y CSV.
- **Iteración y calidad**: generadores, programación funcional, decoradores, tipos y pruebas, asyncio y rendimiento.

Con eso ya podés escribir programas completos en Python. Lo que sigue son **especializaciones**.

#### Las Sendas

Cada Senda es un camino optativo: no hace falta para completar el curso, y su entrada se paga con **comodines** (los que ganaste con los encargos del Gremio). Adentro, los nodos se pagan con escamas, como siempre.

- **Senda de la Arena**: videojuegos con **pygame**. Ventanas, el bucle de juego, teclado, sprites y colisiones, hasta armar un juego completo. Se resuelve en tu compu.
- **Senda del Reino**: Python aplicado. Análisis de datos con **numpy, pandas y matplotlib**, **inteligencia artificial** para juegos (búsqueda de caminos, minimax, aprendizaje por refuerzo) y **robótica** con Arduino por puerto serie.

### Micro-misión R03-N08-P1 · Lo que te llevás

```meta
lugar: La Encrucijada
personajes: Mia, Gheco, Tilo, Ofidia
carta: El camino | Fundamentos · Objetos y errores · Iteración y calidad · ya podés escribir programas completos
recompensa: xp 15, oro 20
```

#### Escena
Al pie de la Ciudadela, el camino se abre en varios senderos. {mentor} se sienta al sol en una piedra del puente.
—Antes de elegir, mirá hacia atrás. ¿Cuántos lugares recorriste?

#### Gheco sugiere
Todo lo que aprendiste sirve a la vez: un diccionario, un `for` sobre sus `.items()` y una expresión generadora adentro de `sum`.

#### Desafío
Mostrá cada tramo del camino y el total de nodos.

#### Código inicial
```python
camino = {"Fundamentos": 11, "Objetos y errores": 5, "Iteración y calidad": 8}
for tramo, nodos in camino.items():
    print(f"{tramo}: {nodos} nodos")
print(f"En total: {___} nodos")
```

#### Salida esperada
```
Fundamentos: 11 nodos
Objetos y errores: 5 nodos
Iteración y calidad: 8 nodos
En total: 24 nodos
```

#### Solución
```python
camino = {"Fundamentos": 11, "Objetos y errores": 5, "Iteración y calidad": 8}
for tramo, nodos in camino.items():
    print(f"{tramo}: {nodos} nodos")
print(f"En total: {sum(n for n in camino.values())} nodos")
```

#### Al superarla
Veinticuatro nodos. {mentor} te mira un largo rato, y después cuenta lo que vio hace mucho:
—Hace mucho cruzó el Valle un viajero con las manos manchadas de plomo. Me preguntó cuál era la lengua más clara del mundo, la que cualquiera pudiera leer. Le dije que la mía. Sonrió y siguió camino hacia las Forjas.

#### Imagen
- La Encrucijada: un puente de piedra al pie de la Ciudadela, varios senderos que se abren.
- Ofidia sentada al sol en una piedra del puente, contando.
- Mia, Tilo y Gheco escuchan sentados en el pasto.

### Micro-misión R03-N08-P2 · La marca de agua

```meta
lugar: La Encrucijada
personajes: Mia, Gheco, Tilo, Ofidia
carta: Para quien llegue | lo que se escribe claro, cualquiera lo puede leer
recompensa: xp 20, oro 25
```

#### Escena
Levantás el pergamino, ya lleno, contra la luz del reloj. La marca de agua por fin se ve, pero **al revés**, como en un espejo.

#### Gheco sugiere
Un texto se da vuelta con un corte con paso negativo: `texto[::-1]`.

#### Desafío
Leé la marca de agua al derecho.

#### Código inicial
```python
marca = "eugell neiuq arap"
print(marca___)
```

#### Salida esperada
```
para quien llegue
```

#### Solución
```python
marca = "eugell neiuq arap"
print(marca[::-1])
```

#### Al superarla
**Un vitral, y debajo: «para quien llegue».**
El pergamino nunca fue de nadie en particular. Lo dejó el viajero para quien llegara, y llegaste vos.
Tilo se queda en el Valle, como aprendiz de {mentor}. Gheco se te sube al hombro y señala los caminos: las **Sendas** del Valle, y el que baja hacia **las Forjas**, por donde siguió el viajero.
—¿Vamos?

#### Imagen
- Mia levanta el pergamino contra la luz del gran reloj: se ve la marca de agua de un vitral y la frase «para quien llegue».
- Tilo, al lado de Ofidia, saluda con la pértiga.
- Gheco en el hombro de Mia señala dos caminos: uno hacia el Coliseo y otro que baja hacia unas forjas humeantes a lo lejos.

### Misión R03-N08-M1 · Mirá hacia atrás

```meta
entrega: ninguna
monedas: 0
xp: 20
```

#### Consigna

Antes de elegir tu Senda, tomate cinco minutos:

1. ¿Cuál fue el tema que más te costó? ¿Qué te ayudó a entenderlo?
2. ¿Qué programa de todo el camino te dio más orgullo?
3. ¿Qué te gustaría construir ahora con Python?

Charlalo con el profe en la próxima clase (o escribíselo). Cuando lo tengas, marcá la misión como completada.

#### Criterio de aprobación

- Respondió las tres preguntas (en clase o por escrito).

### Soluciones (docente)

Nodo Ventana: cierra el camino principal (completarlo completa el curso) y de acá brotan las Sendas S01 y S02. La misión es de reflexión, sin entrega.
