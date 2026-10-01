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

Del otro lado de la Biblioteca se levanta la **Torre del Reloj**. En su primer piso, un río de enemigos no para de salir de un portal: slimes, murciélagos, orcos… Nadie sabe cuántos son. Quizás infinitos.

—No hace falta conocerlos a todos de antemano, {heroe} —dice {mentor}—. Pedilos **de a uno**, cuando los necesites. Así funciona un **generador**.

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
it = iter(["Kira", "Bron"])   # pedirle al iterable un iterador
next(it)                      # "Kira"
next(it)                      # "Bron"
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
compania = ["Kira", "Bron", "Mia"]
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
for i, (nombre, vida) in enumerate(zip(["Kira", "Bron", "Mia"], [120, 90, 150]), start=1):
    print(f"{i}. {nombre}: {vida} de vida")
```

### Salida esperada

```
Kira Bron Mia
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
1. Kira: 120 de vida
2. Bron: 90 de vida
3. Mia: 150 de vida
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
INFO: usuario Kira conectado
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

En el segundo piso de la Torre, el relojero ordena cientos de piezas sin tocarlas una por una. Dice "agrupalas por tamaño", "quedate con las doradas", "ordenalas por peso y después por nombre", y las piezas obedecen.

—Él no escribe **cómo** hacerlo paso a paso, {heroe} —dice {mentor}—. Escribe **qué** quiere. Esa es la magia funcional.

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
    Heroe("Kira", "pícara", 5, 90),
    Heroe("Bron", "guerrero", 7, 160),
    Heroe("Mia", "maga", 4, 70),
    Heroe("Zed", "guerrero", 6, 140),
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
['KIRA', 'BRON', 'MIA', 'ZED', 'ANA']
['Bron', 'Zed', 'Ana']
['Bron', 'Zed', 'Ana']
por nivel: ['Ana(8)', 'Bron(7)', 'Zed(6)', 'Kira(5)', 'Mia(4)']
por clase y nivel: [('guerrero', 'Bron'), ('guerrero', 'Zed'), ('maga', 'Mia'), ('pícara', 'Ana'), ('pícara', 'Kira')]
el de más vida: Bron
vida total: 570
vida total (reduce): 570
--- por clase ---
  guerrero: ['Bron', 'Zed']
  maga: ['Mia']
  pícara: ['Kira', 'Ana']
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
- Guerrero 150.0, maga 70.0 y pícara 100.0.

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
    Heroe("Kira", "pícara", 5, 90),
    Heroe("Bron", "guerrero", 7, 160),
    Heroe("Mia", "maga", 4, 70),
    Heroe("Zed", "guerrero", 6, 140),
    Heroe("Ana", "pícara", 7, 110),
]

# Calculá {clase: vida_promedio} con groupby
```

#### Salida esperada

```
guerrero    150.0
maga         70.0
pícara      100.0
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
    Heroe("Kira", "pícara", 5, 90),
    Heroe("Bron", "guerrero", 7, 160),
    Heroe("Mia", "maga", 4, 70),
    Heroe("Zed", "guerrero", 6, 140),
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
- Ana y Bron (nivel 7) quedan en orden alfabético.

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
    Heroe("Kira", "pícara", 5, 90),
    Heroe("Bron", "guerrero", 7, 160),
    Heroe("Mia", "maga", 4, 70),
    Heroe("Zed", "guerrero", 6, 140),
    Heroe("Ana", "pícara", 7, 110),
]

# Ordená por nivel (de mayor a menor) y, a igual nivel, por nombre
```

#### Salida esperada

```
 7  Ana
 7  Bron
 6  Zed
 5  Kira
 4  Mia
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
    Heroe("Kira", "pícara", 5, 90),
    Heroe("Bron", "guerrero", 7, 160),
    Heroe("Mia", "maga", 4, 70),
    Heroe("Zed", "guerrero", 6, 140),
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

En el tercer piso de la Torre, los relojeros no desarman los relojes para mejorarlos: les ponen **encima** una pieza nueva. Una que mide el tiempo, otra que repite si algo falla, otra que anota cada movimiento. El reloj sigue siendo el mismo; ahora hace más.

—Eso es un **decorador**, {heroe} —dice {mentor}—. Una función que envuelve a otra sin tocarla.

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
    return f"{quien} ataca con su espada"


for orden in ["saludar", "atacar", "bailar"]:
    accion = COMANDOS.get(orden)
    print(accion("Kira") if accion else f"no conozco '{orden}'")
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
¡Hola, Kira!
Kira ataca con su espada
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

Escribí el decorador `@requiere_vida` para **métodos**: si `self.vida <= 0`, avisa que el personaje está fuera de combate y no ejecuta el método. Aplicalo a `atacar` y `curarse` de una clase `Heroe`, y probalo con Kira (30 de vida) y Zed (0).

#### Criterio de aprobación

- La envoltura recibe `self` como primer parámetro y lo revisa.
- Con vida 0 no se ejecuta el método.
- Funciona con métodos de distintos parámetros (`*args`).

#### Salida esperada

```
Kira ataca a un orco.
Zed no puede: está fuera de combate.
Zed no puede: está fuera de combate.
Kira se cura: vida 50.
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


kira = Heroe("Kira", 30)
zed = Heroe("Zed", 0)
kira.atacar("un orco")
zed.atacar("un orco")
zed.curarse(50)
kira.curarse(20)
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

En el cuarto piso de la Torre trabaja el **Gremio de Artífices**. Sus planos no dicen solo "acá va una pieza": dicen **qué clase** de pieza (un engranaje de bronce, un resorte de acero). Y antes de montar un reloj, lo **prueban**: si una pieza falla, lo saben en el taller y no en la plaza.

—Tu código también puede decir qué espera y comprobar que funciona, {heroe} —dice {mentor}.

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


kira = Combatiente("Kira", vida=30, ataque=8, defensa=2)
golem = Combatiente("Golem", vida=50, ataque=6, defensa=4)

probar("daño básico: 8 - 4 = 4", danio(kira, golem) == 4)
probar("el crítico duplica", danio(kira, golem, critico=True) == 8)
probar("si pega, al menos 1", danio(Combatiente("Débil", 10, 1), golem) == 1)
herido = aplicar(golem, 20)
probar("aplicar no modifica el original", herido.vida == 30 and golem.vida == 50)
probar("la vida no baja de 0", aplicar(kira, 999).vida == 0)
probar("buscar devuelve None si no está", buscar([kira, golem], "Zed") is None)



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
print(nombres_vivos([("Kira", 30), ("Zed", 0), ("Mia", 12)]))
print(buscar_objeto({"poción": 3}, "espada"))
print(aplicar_a_todos(lambda v: v * 2, [1, 2, 3]))
```

#### Salida esperada

```
100
['Kira', 'Mia']
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
print(nombres_vivos([("Kira", 30), ("Zed", 0), ("Mia", 12)]))
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

En el quinto piso, la cocinera de la Torre prepara el banquete sola. No se queda mirando cómo hierve la sopa: pone el agua, mientras tanto amasa el pan, y mientras el pan se hornea, prepara el té. Una sola persona, muchas esperas a la vez.

—No se trata de tener más manos, {heroe} —dice {mentor}—, sino de **no quedarse quieta mientras algo espera**.

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

### Misión R03-N05-M1 · El alumno que se desconecta

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Tres alumnos entregan una tarea en un aula virtual (una corrutina que espera un rato y devuelve `"<nombre> entregó"`). Bron se desconecta: su corrutina lanza `ConnectionError`. Juntalos con `gather(..., return_exceptions=True)` y mostrá, en orden, quién entregó y qué problema hubo, sin que el error de Bron corte a los demás.

#### Criterio de aprobación

- Usa `asyncio.gather` con `return_exceptions=True`.
- Distingue los errores con `isinstance(resultado, Exception)`.
- Kira y Mia entregan aunque Bron falle.

#### Salida esperada

```
ok: Kira entregó
problema: Bron se desconectó
ok: Mia entregó
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
        alumno("Kira", 0.2), alumno("Bron", 0.1, falla=True), alumno("Mia", 0.3),
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
        grupo.create_task(jugador(meta, "Kira", [10, 15, 5]))
        grupo.create_task(jugador(meta, "Bron", [20, 10]))
        grupo.create_task(jugador(meta, "Mia", [25, 5]))
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

En el último piso de la Torre, el gran reloj atrasa. Los aprendices discuten: "es el péndulo", "son los engranajes", "es el aceite". El maestro relojero no discute: saca un cronómetro y **mide** cada pieza. En cinco minutos encuentra la culpable. No era ninguna de las que decían.

—Nunca adivines dónde se va el tiempo, {heroe} —dice {mentor}—. **Medilo**.

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
['kira@valle.com', 'bron@valle.com', 'mia@valle.com', 'zed@valle.com']
atajo con dict.fromkeys: ['kira@valle.com', 'bron@valle.com', 'mia@valle.com', 'zed@valle.com']
```

#### Solución de referencia

```python
correos = ["kira@valle.com", "bron@valle.com", "kira@valle.com", "mia@valle.com",
           "bron@valle.com", "zed@valle.com", "kira@valle.com"]

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

En la cima de la Torre, el **Golem del Reloj** despierta. De su pecho salen oleadas de engranajes, resortes y péndulos, una tras otra, sin fin. Y cada siete oleadas, aparece él.

—Contalas sin guardarlas todas, {heroe} —dice {mentor}—. Ordenalas, agrupalas, y cuando llegue el Golem, que tus tres torres lo esperen **a la vez**.

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

Bajás de la Torre y el camino se abre en varios senderos. {mentor} se enrosca en una piedra, al sol, y te mira con algo parecido al orgullo.

—Ya hablás la lengua del Valle, {heroe}. Lo que sigue ya no es obligatorio: es **tuyo**. Por un sendero se llega a la Arena, donde la magia se vuelve juego. Por el otro, al Reino, donde se pone al servicio de la gente: datos, máquinas que piensan, robots.

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
