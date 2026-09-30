# RAMA S02 · Senda del Reino: datos, IA y robótica

```meta
tipo: senda
posicion: 5
```

## S02-N01 · Datos: lo que cuentan las partidas

```meta
tipo: tema
padre: R03-N08
precio: 3
moneda: comodin
criatura: goblin
ejecutable: no
temas: datos.pandas, datos.graficos
usa: arch.csv
```

### Crónica

El sendero de la derecha lleva al **Reino**, donde los magos no pelean: **responden preguntas**. En la oficina del Consejo, miles de registros de partidas esperan en una planilla: cuánto duraron, cuántas gemas se juntaron, dónde se murió más.

—Nadie puede leer dos mil filas, {heroe} —dice el consejero—. Pero Python sí. Preguntale a los datos si el juego es demasiado difícil.

### Objetivos

- Cargar un CSV con **pandas** y explorarlo (`head`, `describe`, filtros).
- Agrupar y resumir (`groupby`, promedios, porcentajes).
- Graficar con **matplotlib** y sacar conclusiones.

### Antes de empezar

CSV (R02-N04) y programación funcional (R03-N02): pandas usa las mismas ideas en tablas enteras.

### Explicación

#### Instalar

numpy, pandas y matplotlib no vienen con Python. Este nodo se hace en tu compu:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install numpy pandas matplotlib
```

#### numpy: cuentas sobre muchos números a la vez

Un `numpy.array` guarda muchos números juntos y hace las cuentas **de una**: `precios * 1.21` multiplica todos, sin `for`, y mucho más rápido (el bucle corre en C, R03-N06).

#### pandas: planillas en Python

Un `DataFrame` es una tabla con columnas con nombre:

```python
import pandas as pd
df = pd.read_csv("partidas.csv")
df.head()                        # las primeras filas
df.describe()                    # promedio, mínimo, máximo… de cada columna
df[df["dificultad"] == "difícil"]  # filtrar filas
df["gemas"].mean()               # promedio de una columna
df.groupby("dificultad")["completada"].mean()   # % de completadas por dificultad
```

- Una columna nueva se crea con una cuenta: `df["gemas_por_minuto"] = df["gemas"] / df["minutos"]`.
- `groupby` agrupa filas por una columna y resume cada grupo (como el `groupby` de itertools, pero sin ordenar antes).

#### matplotlib: gráficos

```python
import matplotlib.pyplot as plt
resumen.plot(kind="bar")
plt.savefig("balance.png")
```

#### Preguntas, no números

El análisis empieza con una **pregunta** ("¿la dificultad difícil es injusta?") y termina con una **conclusión** que alguien puede usar ("en difícil se completa el 12 %: bajemos el daño de los enemigos"). Los números del medio son la evidencia.

### Código de ejemplo

```python
"""40b - Analizar la telemetria con numpy / pandas / matplotlib.

pandas = "Excel programable": carga el CSV en un DataFrame (tabla con columnas
tipadas) y deja agrupar, filtrar y resumir en una linea.
numpy  = arrays numericos rapidos (el bucle corre en C, no en Python).
matplotlib = graficos.

Necesita:  sudo apt install python3-numpy python3-pandas python3-matplotlib
           (o  cd .. && ./crear-venv.sh)
Antes:     python3 generar_telemetria.py     (crea partidas.csv)
Correr:    python3 analizar.py               (crea balance.png)
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")            # backend sin ventana: guarda a archivo
import matplotlib.pyplot as plt

AQUI = Path(__file__).parent
CSV = AQUI / "partidas.csv"
PNG = AQUI / "balance.png"

if not CSV.exists():
    raise SystemExit("Falta partidas.csv. Corre primero:  python3 generar_telemetria.py")

# ------------------------------------------------------------------
# cargar
# ------------------------------------------------------------------
df = pd.read_csv(CSV)
print(f"{len(df)} partidas, columnas: {list(df.columns)}\n")
print(df.head(), "\n")

# ------------------------------------------------------------------
# resumen numerico (como df.describe pero eligiendo columnas)
# ------------------------------------------------------------------
print("estadisticas de duracion (segundos):")
d = df["duracion_s"].to_numpy()
print(f"  media {d.mean():.1f}  mediana {np.median(d):.1f}  "
      f"desvio {d.std():.1f}  p90 {np.percentile(d, 90):.1f}\n")

# ------------------------------------------------------------------
# groupby: el corazon de pandas
# ------------------------------------------------------------------
print("por dificultad:")
resumen = df.groupby("dificultad").agg(
    partidas=("completada", "size"),
    tasa_exito=("completada", "mean"),
    gemas_prom=("gemas", "mean"),
    muertes_prom=("muertes", "mean"),
    dur_prom=("duracion_s", "mean"),
).round(2)
# ordenar como corresponde, no alfabetico
resumen = resumen.reindex(["facil", "normal", "dificil"])
print(resumen, "\n")

# tabla cruzada dificultad x mapa: tasa de finalizacion
print("tasa de finalizacion por dificultad y mapa:")
print(pd.crosstab(df["dificultad"], df["mapa"],
                  values=df["completada"], aggfunc="mean").round(2), "\n")

# ------------------------------------------------------------------
# correlacion: mas muertes -> menos exito?
# ------------------------------------------------------------------
corr = df[["duracion_s", "gemas", "muertes", "completada"]].corr()
print("correlaciones con 'completada':")
print(corr["completada"].round(3), "\n")

# ------------------------------------------------------------------
# grafico: 4 paneles
# ------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(11, 8))
fig.suptitle("Balance de 'Junta las Gemas' - 2000 partidas", fontsize=14)

# 1. histograma de duracion por dificultad
for dif in ["facil", "normal", "dificil"]:
    axes[0, 0].hist(df.loc[df.dificultad == dif, "duracion_s"],
                    bins=30, alpha=0.6, label=dif)
axes[0, 0].set_title("Duracion de partida")
axes[0, 0].set_xlabel("segundos"); axes[0, 0].legend()

# 2. tasa de exito por dificultad (barras)
resumen["tasa_exito"].plot.bar(ax=axes[0, 1], color=["#a6e3a1", "#89b4fa", "#f38ba8"])
axes[0, 1].set_title("Tasa de finalizacion"); axes[0, 1].set_ylim(0, 1)
axes[0, 1].tick_params(axis="x", rotation=0)

# 3. gemas vs muertes (dispersión)
axes[1, 0].scatter(df["muertes"], df["gemas"], s=8, alpha=0.2)
axes[1, 0].set_title("Gemas vs muertes"); axes[1, 0].set_xlabel("muertes")
axes[1, 0].set_ylabel("gemas")

# 4. gemas promedio por mapa
df.groupby("mapa")["gemas"].mean().plot.bar(ax=axes[1, 1], color="#cba6f7")
axes[1, 1].set_title("Gemas promedio por mapa")
axes[1, 1].tick_params(axis="x", rotation=0)

fig.tight_layout()
fig.savefig(PNG, dpi=100)
print(f"grafico guardado en {PNG.name}")

# ------------------------------------------------------------------
# conclusion automatica
# ------------------------------------------------------------------
peor = resumen["tasa_exito"].idxmin()
print(f"\n=> '{peor}' tiene la tasa de exito mas baja "
      f"({resumen.loc[peor, 'tasa_exito']:.0%}). "
      "Si el objetivo es ~40%, hay que suavizarla.")
```

### ¿Para qué sirve?

Analizar datos es uno de los trabajos más pedidos con Python: ver qué productos se venden más, qué alumnos necesitan apoyo, cuándo hay más consultas en un hospital, si una campaña funcionó. Los estudios de videojuegos hacen exactamente esto con la telemetría de sus jugadores para ajustar la dificultad.

### Errores habituales

**Goblin: columnas con el tipo equivocado**: un número leído como texto (porque una fila dice "N/A"). Revisá `df.dtypes` y convertí con `pd.to_numeric(..., errors="coerce")`.

**Esqueleto: `KeyError` con el nombre de una columna**: revisá mayúsculas, tildes y espacios con `df.columns`.

**Ogro: conclusiones con pocos datos**: un promedio de 3 partidas no dice nada. Mirá siempre cuántas filas tiene cada grupo (`size()`).

**Ogro: el gráfico vacío**: con `plt.savefig` después de `plt.show()`, se guarda una imagen en blanco.

### Misión S02-N01-M1 · Gemas por minuto

```meta
entrega: archivo
monedas: 5
xp: 15
entorno: local
extensiones: py, zip, csv, png
```

#### Consigna

Generá los datos con `generar_telemetria.py` (de la carpeta del curso) y, con pandas, agregá una columna `gemas_por_minuto`. Mostrá su promedio, mínimo y máximo **por dificultad** y guardá un gráfico de barras con los promedios. En un comentario, respondé: ¿en qué dificultad se juntan gemas más rápido y por qué te parece?

#### Criterio de aprobación

- Crea la columna con una cuenta entre columnas (sin `for`).
- Resume por dificultad con `groupby`.
- Entrega el gráfico y una conclusión escrita.

### Misión S02-N01-M2 · Las partidas eternas

```meta
entrega: archivo
monedas: 5
xp: 15
entorno: local
extensiones: py, zip, csv, png
```

#### Consigna

Filtrá el 5 % de partidas **más largas** (percentil 95 de la duración, con `quantile(0.95)`). ¿Qué tienen en común? Compará su tasa de completadas, sus muertes y su dificultad con el resto.

#### Criterio de aprobación

- Usa `quantile` para el percentil 95.
- Compara el grupo filtrado con el resto en al menos tres columnas.
- Escribe una conclusión.

### Encargo S02-N01-E1 · El informe para el equipo

```meta
entrega: archivo
monedas: 1
xp: 15
entorno: local
extensiones: py, zip, csv, png
```

#### Consigna

Exportá el resumen por dificultad a `balance.csv` con `to_csv`, listo para abrir en una planilla, y armá un texto corto (5 líneas) con las tres conclusiones más importantes.

#### Criterio de aprobación

- El CSV se abre bien en una planilla.
- Las conclusiones se apoyan en números del resumen.

### Prueba del sello

#### ¿Qué ventaja tiene numpy sobre una lista para hacer cuentas?

Hace la cuenta sobre todos los elementos de una vez y mucho más rápido, sin escribir el bucle.

#### ¿Cómo filtrás las filas de un DataFrame?

Con una condición entre corchetes: `df[df["columna"] > 10]`.

#### ¿Qué hace `df.groupby("dificultad")["gemas"].mean()`?

Agrupa las filas por dificultad y calcula el promedio de gemas de cada grupo.

### Soluciones (docente)

Material original: `17-Python/40-Datos-Telemetria` (`generar_telemetria.py` solo necesita Python; `analizar.py`, numpy, pandas y matplotlib). Local porque la plataforma no carga paquetes externos.

## S02-N02 · IA: encontrar el camino (A*)

```meta
tipo: tema
padre: S02-N01
precio: 10
criatura: orco
temas: alg.grafos
usa: col.pilas-colas
```

### Crónica

En la torre de los Estrategas, un enemigo de práctica tiene que llegar hasta vos atravesando un laberinto. Los aprendices lo mueven "hacia donde estás" y se choca contra cada pared.

—Una buena criatura no camina hacia su presa, {heroe} —dice la estratega—: **busca el camino**. Y el mejor buscador del Reino se llama A*.

### Objetivos

- Entender la búsqueda de caminos en una grilla.
- Implementar A* con una cola de prioridad (`heapq`) y una heurística.
- Adaptarlo: movimiento en 8 direcciones y terrenos con distinto costo.

### Antes de empezar

Diccionarios, tuplas y conjuntos (R01), generadores (R03-N01). Recursión y el "flood fill" de R01-N09 ayudan a entender la búsqueda.

### Explicación

#### El problema

El mapa es una grilla: `.` es piso y `#` es pared. Queremos el camino **más corto** desde el enemigo (E) hasta el jugador (J).

#### Explorar por capas

La idea base: desde el inicio, visitar los vecinos, después los vecinos de los vecinos, y así, anotando **de dónde vino** cada casilla (`vino_de`). Cuando se llega a la meta, se reconstruye el camino yendo hacia atrás por `vino_de`.

#### A*: explorar primero lo prometedor

A* no explora a ciegas: para cada casilla calcula

**prioridad = costo hasta acá + estimación de lo que falta**

y siempre sigue por la de menor prioridad. La estimación es la **heurística**; con 4 direcciones, la distancia Manhattan (`|Δfila| + |Δcol|`). Si la heurística nunca exagera, A* encuentra el camino más corto explorando mucho menos que la búsqueda a ciegas.

#### La cola de prioridad: `heapq`

```python
import heapq
frontera = [(0, inicio)]
heapq.heappush(frontera, (prioridad, casilla))
prioridad, actual = heapq.heappop(frontera)   # siempre la de menor prioridad
```

#### Costos

Si pisar cada casilla cuesta 1, el camino más corto es el de menos pasos. Si hay terrenos más caros (un pantano que cuesta 5), A* suma el costo de cada terreno y puede preferir un rodeo más largo pero más barato.

### Código de ejemplo

```python
"""A*: camino mas corto en una grilla con obstaculos.

El pathfinding clasico de un enemigo que persigue al jugador esquivando
paredes. A* = Dijkstra + una heuristica que lo guia hacia la meta.
Solo stdlib (heapq).
"""

import heapq

MAPA = [
    "..........",
    ".####.###.",
    ".#..#.#...",
    ".#.##.#.#.",
    ".#....#.#.",
    ".####.#.#.",
    "....#...#.",
    ".##.#.###.",
    ".#.......#",
    "..........",
]


def vecinos(mapa, celda):
    f, c = celda
    for df, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nf, nc = f + df, c + dc
        if 0 <= nf < len(mapa) and 0 <= nc < len(mapa[0]) and mapa[nf][nc] != "#":
            yield (nf, nc)


def heuristica(a, b):
    # distancia Manhattan (movimiento en 4 direcciones)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_estrella(mapa, inicio, meta):
    frontera = [(0, inicio)]                 # cola de prioridad (heap)
    vino_de = {inicio: None}
    costo = {inicio: 0}

    while frontera:
        _, actual = heapq.heappop(frontera)
        if actual == meta:
            break
        for sig in vecinos(mapa, actual):
            nuevo = costo[actual] + 1
            if sig not in costo or nuevo < costo[sig]:
                costo[sig] = nuevo
                prioridad = nuevo + heuristica(sig, meta)
                heapq.heappush(frontera, (prioridad, sig))
                vino_de[sig] = actual

    if meta not in vino_de:
        return None                          # no hay camino

    # reconstruir el camino desde la meta hacia atras
    camino = []
    n = meta
    while n is not None:
        camino.append(n)
        n = vino_de[n]
    camino.reverse()
    return camino


def dibujar(mapa, camino):
    marca = set(camino or [])
    for f, fila in enumerate(mapa):
        linea = ""
        for c, ch in enumerate(fila):
            if (f, c) == camino[0]:
                linea += "E"
            elif (f, c) == camino[-1]:
                linea += "J"
            elif (f, c) in marca:
                linea += "o"
            else:
                linea += ch
        print(linea)


if __name__ == "__main__":
    inicio, meta = (0, 0), (9, 9)
    camino = a_estrella(MAPA, inicio, meta)
    if camino:
        print(f"camino de {len(camino)} pasos:\n")
        dibujar(MAPA, camino)
        print("\nel enemigo (E) da el primer paso hacia:", camino[1])
    else:
        print("sin camino")
```

### Salida esperada

```
camino de 19 pasos:

Eooooo....
.####o###.
.#..#o#...
.#.##o#.#.
.#...o#.#.
.####o#.#.
....#o..#.
.##.#o###.
.#...oooo#
........oJ

el enemigo (E) da el primer paso hacia: (0, 1)
```

### ¿Para qué sirve?

A* es el algoritmo que usan los enemigos de casi todos los videojuegos para perseguirte, pero también está detrás de los GPS y los mapas del celular (buscar la ruta más rápida), de los robots que limpian la casa y de los depósitos donde los robots buscan paquetes.

### Errores habituales

**Orco: salirse del mapa**: revisá los bordes antes de mirar `mapa[f][c]` (con índices negativos, Python no da error: ¡lee del otro lado!).

**Ogro: la heurística que exagera**: si estima más de lo que realmente falta, A* puede devolver un camino que no es el más corto.

**Ogro: no guardar el mejor costo**: sin `costo[sig]`, una casilla se procesa muchas veces o queda con un camino peor.

**Ogro: no hay camino**: si la meta queda encerrada, `vino_de` nunca la tiene. Devolvé `None` y manejalo.

### Misión S02-N02-M1 · Ocho direcciones

```meta
entrega: codigo
monedas: 5
xp: 15
```

#### Consigna

Adaptá A* para que el enemigo pueda moverse también en **diagonal** (8 direcciones). Con diagonales, la heurística correcta es la distancia de **Chebyshev**: `max(|Δfila|, |Δcol|)`. Mostrá cuántos pasos tiene el camino con 4 y con 8 direcciones, y dibujá el de 8.

#### Criterio de aprobación

- Las direcciones y la heurística se pasan como parámetro (no dos copias de A*).
- Usa Chebyshev con 8 direcciones.
- Con 4 direcciones son 18 pasos; con 8, 14.

#### Salida esperada

```
4 direcciones: 18 pasos
8 direcciones: 14 pasos
o.........
o####.###.
o#..#.#...
o#.##.#.#.
o#....#.#.
o####.#.#.
.oo.#...#.
.##o#o###.
.#..o.ooo#
.........o
```

#### Solución de referencia

```python
import heapq

MAPA = [
    "..........",
    ".####.###.",
    ".#..#.#...",
    ".#.##.#.#.",
    ".#....#.#.",
    ".####.#.#.",
    "....#...#.",
    ".##.#.###.",
    ".#.......#",
    "..........",
]
CUATRO = ((1, 0), (-1, 0), (0, 1), (0, -1))
OCHO = CUATRO + ((1, 1), (1, -1), (-1, 1), (-1, -1))


def vecinos(mapa, celda, direcciones):
    f, c = celda
    for df, dc in direcciones:
        nf, nc = f + df, c + dc
        if 0 <= nf < len(mapa) and 0 <= nc < len(mapa[0]) and mapa[nf][nc] != "#":
            yield (nf, nc)


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def chebyshev(a, b):
    """Con 8 direcciones, una diagonal cuesta 1 paso: manda la distancia mayor."""
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def a_estrella(mapa, inicio, meta, direcciones, heuristica):
    frontera = [(0, inicio)]
    vino_de = {inicio: None}
    costo = {inicio: 0}
    while frontera:
        _, actual = heapq.heappop(frontera)
        if actual == meta:
            break
        for sig in vecinos(mapa, actual, direcciones):
            nuevo = costo[actual] + 1
            if sig not in costo or nuevo < costo[sig]:
                costo[sig] = nuevo
                heapq.heappush(frontera, (nuevo + heuristica(sig, meta), sig))
                vino_de[sig] = actual
    if meta not in vino_de:
        return None
    camino, n = [], meta
    while n is not None:
        camino.append(n)
        n = vino_de[n]
    return camino[::-1]


cuatro = a_estrella(MAPA, (0, 0), (9, 9), CUATRO, manhattan)
ocho = a_estrella(MAPA, (0, 0), (9, 9), OCHO, chebyshev)
print("4 direcciones:", len(cuatro) - 1, "pasos")
print("8 direcciones:", len(ocho) - 1, "pasos")
marca = set(ocho)
for f, fila in enumerate(MAPA):
    print("".join("o" if (f, c) in marca else ch for c, ch in enumerate(fila)))
```

### Misión S02-N02-M2 · El costo del pantano

```meta
entrega: codigo
monedas: 5
xp: 15
```

#### Consigna

Ahora el mapa tiene **pantanos** (`~`), que se pueden pisar pero cuestan 5 (el piso cuesta 1). Adaptá A* para que sume el costo del terreno de cada casilla que pisa, y encontrá el camino más barato de `S` a `M`. Mostrá los pasos, el costo total, cuántos pantanos pisa, y el mapa con el camino.

#### Criterio de aprobación

- El costo de cada paso depende del terreno que se pisa.
- Encuentra el camino más barato aunque tenga más pasos.
- Resultado: 18 pasos, costo 22, un solo pantano.

#### Salida esperada

```
18 pasos, costo 22, pisa 1 pantanos
Sooooooooo
~~~~~~~~#o
........#o
.######.#o
........~o
#######~#o
......~~.o
.........o
~~~~~~~~~o
.........M
```

#### Solución de referencia

```python
import heapq

# '.' piso (cuesta 1), '~' pantano (cuesta 5), '#' pared
MAPA = [
    "S.........",
    "~~~~~~~~#.",
    "........#.",
    ".######.#.",
    "........~.",
    "#######~#.",
    "......~~..",
    "..........",
    "~~~~~~~~~~",
    ".........M",
]
COSTO = {".": 1, "S": 1, "M": 1, "~": 5}


def buscar(letra):
    return next((f, c) for f, fila in enumerate(MAPA) for c, ch in enumerate(fila) if ch == letra)


def vecinos(celda):
    f, c = celda
    for df, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nf, nc = f + df, c + dc
        if 0 <= nf < len(MAPA) and 0 <= nc < len(MAPA[0]) and MAPA[nf][nc] != "#":
            yield (nf, nc)


def a_estrella(inicio, meta):
    frontera = [(0, inicio)]
    costo = {inicio: 0}
    vino_de = {inicio: None}
    while frontera:
        _, actual = heapq.heappop(frontera)
        if actual == meta:
            break
        for sig in vecinos(actual):
            nuevo = costo[actual] + COSTO[MAPA[sig[0]][sig[1]]]   # pisar sig cuesta según su terreno
            if sig not in costo or nuevo < costo[sig]:
                costo[sig] = nuevo
                heuristica = abs(sig[0] - meta[0]) + abs(sig[1] - meta[1])
                heapq.heappush(frontera, (nuevo + heuristica, sig))
                vino_de[sig] = actual
    camino, n = [], meta
    while n is not None:
        camino.append(n)
        n = vino_de[n]
    return camino[::-1], costo[meta]


camino, total = a_estrella(buscar("S"), buscar("M"))
pantanos = sum(1 for f, c in camino if MAPA[f][c] == "~")
print(f"{len(camino) - 1} pasos, costo {total}, pisa {pantanos} pantanos")
marca = set(camino[1:-1])
for f, fila in enumerate(MAPA):
    print("".join("o" if (f, c) in marca else ch for c, ch in enumerate(fila)))
```

### Prueba del sello

#### ¿Qué suma A* para decidir qué casilla explorar primero?

El costo desde el inicio hasta esa casilla más la estimación (heurística) de lo que falta.

#### ¿Para qué sirve `vino_de`?

Para reconstruir el camino al final, yendo desde la meta hacia atrás.

#### ¿Qué heurística corresponde a 4 direcciones? ¿Y a 8?

Manhattan con 4; Chebyshev con 8 (cuando la diagonal cuesta lo mismo que un paso recto).

### Soluciones (docente)

Material original: `17-Python/41-IA-Juegos/astar.py`. Corre en el navegador (solo usa `heapq`). Nota: con 8 direcciones el camino puede "cortar esquinas" entre dos paredes; si se quiere evitar, es una buena extensión para quien termina antes.

## S02-N03 · IA: rivales que piensan

```meta
tipo: tema
padre: S02-N02
precio: 10
criatura: ogro
temas: alg.ia-juegos
usa: alg.grafos
```

### Crónica

En el último salón de la torre de los Estrategas hay dos rivales. Uno juega al tres en raya y **no pierde nunca**. El otro empezó cayéndose en todos los pozos de un pasillo… y después de mil intentos, lo cruza sin dudar.

—El primero **piensa** todas las jugadas posibles, {heroe} —dice la estratega—. El segundo **aprende** de sus errores. Son las dos grandes familias de la inteligencia artificial.

### Objetivos

- Entender minimax y la poda alfa-beta para juegos por turnos.
- Entender el aprendizaje por refuerzo con una tabla Q (Q-learning).
- Medir cuánto trabajo ahorra la poda y experimentar con los parámetros del aprendizaje.

### Antes de empezar

Recursión (R01-N09), diccionarios (R01-N06) y azar reproducible (R01-N04).

### Explicación

#### Minimax: pensar todas las jugadas

En un juego por turnos (tres en raya, ajedrez), la IA prueba **cada** jugada posible, después cada respuesta del rival, y así hasta el final, con recursión. Asume que el rival juega **perfecto**:

- En su turno, la IA elige la jugada con **mayor** puntaje (MAX).
- En el turno del rival, se asume la de **menor** puntaje para la IA (MIN).

Ganar vale +10, perder −10, empatar 0 (y ganar antes vale un poco más). Contra minimax, lo mejor que se puede lograr es empatar.

#### Poda alfa-beta: no pensar lo inútil

Si ya encontraste una jugada que te asegura cierto resultado, no hace falta terminar de explorar otra rama que ya se sabe que es peor. Alfa-beta **corta** esas ramas: da la misma respuesta visitando muchísimos menos nodos.

#### Q-learning: aprender probando

El bot no conoce las reglas: **prueba** acciones y recibe **recompensas** (+1 si llega, −1 si cae en un pozo, un poquito negativo por cada paso). Guarda una tabla `Q[estado][acción]` con cuánto espera ganar, y la corrige después de cada intento:

```
Q[s][a] += ALFA * (recompensa + GAMMA * mejor_Q_del_estado_siguiente - Q[s][a])
```

- `ALFA`: cuánto pesa cada experiencia nueva.
- `GAMMA`: cuánto importa el futuro frente a la recompensa inmediata.
- **Explorar o aprovechar** (`epsilon`): al principio elige mucho al azar (explora); con el tiempo, cada vez más la mejor acción conocida.

### Código de ejemplo

```python
"""Minimax con poda alfa-beta: un rival imbatible al tres en raya.

Minimax explora todas las jugadas asumiendo que el rival juega perfecto.
Alfa-beta descarta ramas que no pueden cambiar el resultado (misma respuesta,
menos trabajo). Base de la IA de ajedrez, damas, Connect 4.
"""

GANADORAS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),    # filas
    (0, 3, 6), (1, 4, 7), (2, 5, 8),    # columnas
    (0, 4, 8), (2, 4, 6),               # diagonales
]


def ganador(t):
    for a, b, c in GANADORAS:
        if t[a] != "." and t[a] == t[b] == t[c]:
            return t[a]
    return None


def libres(t):
    return [i for i, v in enumerate(t) if v == "."]


def minimax(t, jugador_ia, turno, alfa=-999, beta=999, profundidad=0):
    """Devuelve (puntaje, jugada). turno es 'X' o 'O'; jugador_ia maximiza."""
    g = ganador(t)
    if g == jugador_ia:
        return 10 - profundidad, None       # ganar antes vale mas
    if g is not None:
        return profundidad - 10, None       # perder despues vale mas
    if not libres(t):
        return 0, None                       # empate

    otro = "O" if turno == "X" else "X"
    mejor_jugada = None

    if turno == jugador_ia:                   # MAX
        mejor = -999
        for i in libres(t):
            t[i] = turno
            puntaje, _ = minimax(t, jugador_ia, otro, alfa, beta, profundidad + 1)
            t[i] = "."
            if puntaje > mejor:
                mejor, mejor_jugada = puntaje, i
            alfa = max(alfa, mejor)
            if beta <= alfa:
                break                        # poda
        return mejor, mejor_jugada
    else:                                     # MIN
        peor = 999
        for i in libres(t):
            t[i] = turno
            puntaje, _ = minimax(t, jugador_ia, otro, alfa, beta, profundidad + 1)
            t[i] = "."
            if puntaje < peor:
                peor, mejor_jugada = puntaje, i
            beta = min(beta, peor)
            if beta <= alfa:
                break
        return peor, mejor_jugada


def mostrar(t):
    for f in range(0, 9, 3):
        print(" " + " | ".join(t[f:f + 3]))
        if f < 6:
            print("---+---+---")


def jugar_partida(semilla_humano, mostrar_pasos=True):
    """Humano 'X' juega al azar; IA 'O' responde con minimax. Devuelve el ganador."""
    import random
    rng = random.Random(semilla_humano)
    tablero = ["."] * 9
    turno = "X"
    while ganador(tablero) is None and libres(tablero):
        if turno == "X":
            jugada = rng.choice(libres(tablero))
        else:
            _, jugada = minimax(tablero, "O", "O")
        tablero[jugada] = turno
        if mostrar_pasos:
            print(f"\n{'humano (X)' if turno == 'X' else 'IA (O)'} juega {jugada}")
            mostrar(tablero)
        turno = "O" if turno == "X" else "X"
    return ganador(tablero)


if __name__ == "__main__":
    g = jugar_partida(semilla_humano=3)
    print("\nresultado:", f"gana {g}" if g else "empate")

    # verificacion: la IA NUNCA pierde, juegue lo que juegue el humano
    resultados = [jugar_partida(s, mostrar_pasos=False) for s in range(20)]
    print(f"\n20 partidas vs humano al azar -> "
          f"IA gana {resultados.count('O')}, empata {resultados.count(None)}, "
          f"pierde {resultados.count('X')}")
    print("(contra minimax, lo mejor a lo que podes aspirar es al empate)")
```

### Salida esperada

```
humano (X) juega 3
 . | . | .
---+---+---
 X | . | .
---+---+---
 . | . | .

IA (O) juega 0
 O | . | .
---+---+---
 X | . | .
---+---+---
 . | . | .

humano (X) juega 6
 O | . | .
---+---+---
 X | . | .
---+---+---
 X | . | .

IA (O) juega 1
 O | O | .
---+---+---
 X | . | .
---+---+---
 X | . | .

humano (X) juega 8
 O | O | .
---+---+---
 X | . | .
---+---+---
 X | . | X

IA (O) juega 2
 O | O | O
---+---+---
 X | . | .
---+---+---
 X | . | X

resultado: gana O

20 partidas vs humano al azar -> IA gana 14, empata 6, pierde 0
(contra minimax, lo mejor a lo que podes aspirar es al empate)
```

### ¿Para qué sirve?

Minimax (con muchas mejoras) es la base de los programas de ajedrez y de damas. El aprendizaje por refuerzo es lo que usan las IA que aprendieron a jugar videojuegos, a controlar robots que caminan, a manejar el aire acondicionado de un edificio gastando menos energía, y parte de cómo se entrenan los asistentes conversacionales.

### Errores habituales

**Ogro: olvidar deshacer la jugada** después de probarla (`t[i] = "."`): el tablero queda lleno de jugadas "imaginarias".

**Ogro: invertir MAX y MIN**: la IA juega para que gane el rival.

**Ogro: epsilon que nunca baja**: el bot sigue jugando al azar y no aprovecha lo que aprendió.

**Ogro: pocos episodios**: la tabla Q no llegó a aprender; el bot se sigue cayendo.

**Goblin: explorar sin límite**: minimax en un juego grande (ajedrez) no termina nunca; hay que cortar a cierta profundidad.

### Misión S02-N03-M1 · Cuánto ahorra la poda

```meta
entrega: codigo
monedas: 5
xp: 15
```

#### Consigna

Agregale a minimax un **contador de nodos visitados** (una variable global que suma 1 en cada llamada) y un parámetro `podar` para activar o desactivar la poda alfa-beta. Con el tablero donde X ya jugó en la esquina 0 y le toca a la IA (O), mostrá qué jugada elige y cuántos nodos visitó **sin** y **con** poda.

#### Criterio de aprobación

- Cuenta los nodos en cada llamada a minimax.
- Con y sin poda elige la misma jugada.
- Sin poda visita 59705 nodos; con poda, 2788.

#### Salida esperada

```
sin poda: juega 4 (puntaje 0), visitó 59705 nodos
con poda: juega 4 (puntaje 0), visitó 2788 nodos
```

#### Solución de referencia

```python
GANADORAS = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
visitados = 0


def ganador(t):
    for a, b, c in GANADORAS:
        if t[a] != "." and t[a] == t[b] == t[c]:
            return t[a]
    return None


def libres(t):
    return [i for i, v in enumerate(t) if v == "."]


def minimax(t, ia, turno, alfa=-999, beta=999, prof=0, podar=True):
    global visitados
    visitados += 1
    g = ganador(t)
    if g == ia:
        return 10 - prof, None
    if g is not None:
        return prof - 10, None
    if not libres(t):
        return 0, None
    otro = "O" if turno == "X" else "X"
    mejor, jugada = (-999, None) if turno == ia else (999, None)
    for i in libres(t):
        t[i] = turno
        puntaje, _ = minimax(t, ia, otro, alfa, beta, prof + 1, podar)
        t[i] = "."
        if turno == ia and puntaje > mejor:
            mejor, jugada = puntaje, i
        if turno != ia and puntaje < mejor:
            mejor, jugada = puntaje, i
        if turno == ia:
            alfa = max(alfa, mejor)
        else:
            beta = min(beta, mejor)
        if podar and beta <= alfa:
            break
    return mejor, jugada


tablero = list("X........")          # X ya jugó en la esquina; le toca a la IA (O)
for podar in (False, True):
    visitados = 0
    puntaje, jugada = minimax(tablero[:], "O", "O", podar=podar)
    print(f"{'con' if podar else 'sin'} poda: juega {jugada} (puntaje {puntaje}), visitó {visitados} nodos")
```

### Misión S02-N03-M2 · El pasillo de los tres pozos

```meta
entrega: codigo
monedas: 5
xp: 15
```

#### Consigna

Adaptá el Q-learning del curso a un pasillo más largo: meta en 12 y pozos en 3, 6 y 9. Entrená con 4000 episodios y `random.seed(0)`, mostrá la política aprendida y el recorrido del bot, y comprobá que llega sin caer en ningún pozo.

#### Criterio de aprobación

- Entrena con la regla de actualización de Q-learning.
- Muestra la política (una acción por posición) y el recorrido.
- El bot llega a la meta sin pisar pozos.

#### Salida esperada

```
política: » > » < > » < > » < » >
recorrido: [0, 2, 4, 5, 7, 8, 10, 12]
¿llegó sin caer? True
```

#### Solución de referencia

```python
import random

META = 12
POZOS = {3, 6, 9}
ACCIONES = (-1, +1, +2)
ALFA, GAMMA, EPISODIOS = 0.2, 0.95, 4000


def recompensa(pos):
    if pos >= META:
        return 1.0, True
    if pos in POZOS:
        return -1.0, True
    return -0.02, False


def entrenar():
    Q = {s: {a: 0.0 for a in ACCIONES} for s in range(META + 1)}
    epsilon = 1.0
    for _ in range(EPISODIOS):
        pos = random.choice([s for s in range(META) if s not in POZOS])
        terminado, pasos = False, 0
        while not terminado and pasos < 50:
            pasos += 1
            accion = random.choice(ACCIONES) if random.random() < epsilon else max(Q[pos], key=Q[pos].get)
            nueva = max(0, min(META, pos + accion))
            r, terminado = recompensa(nueva)
            futuro = 0.0 if terminado else max(Q[nueva].values())
            Q[pos][accion] += ALFA * (r + GAMMA * futuro - Q[pos][accion])
            pos = nueva
        epsilon = max(0.05, epsilon * 0.999)
    return Q


def probar(Q):
    pos, camino = 0, [0]
    for _ in range(30):
        pos = max(0, min(META, pos + max(Q[pos], key=Q[pos].get)))
        camino.append(pos)
        if pos >= META or pos in POZOS:
            break
    return camino


random.seed(0)
Q = entrenar()
simbolo = {-1: "<", 1: ">", 2: "»"}
print("política:", " ".join(simbolo[max(Q[s], key=Q[s].get)] for s in range(META)))
camino = probar(Q)
print("recorrido:", camino)
print("¿llegó sin caer?", camino[-1] == META and not POZOS & set(camino))
```

### Prueba del sello

#### ¿Qué supone minimax sobre el rival?

Que juega perfecto: siempre elige la jugada que peor le conviene a la IA.

#### ¿La poda alfa-beta cambia la jugada que elige minimax?

No: da la misma respuesta, visitando muchos menos nodos.

#### En Q-learning, ¿para qué sirve `epsilon`?

Para decidir cuánto explorar al azar y cuánto aprovechar lo aprendido; empieza alto y baja con el tiempo.

### Soluciones (docente)

Material original: `17-Python/41-IA-Juegos/minimax.py` y `qlearning.py`. El ejemplo del nodo juega 20 partidas (el original, 200) para que entre en los 5 segundos del navegador.

## S02-N04 · Robótica: el mando de Arduino

```meta
tipo: jefe
padre: S02-N03
precio: 10
criatura: troll
insignia: Artífice del Reino
insignia_descripcion: Conectaste Python con el mundo real: datos, IA y hardware.
temas: hw.serie
usa: hw.arduino
```

### Crónica

En el taller del Reino, un Arduino con un joystick y dos botones espera sobre la mesa. Cada fracción de segundo manda una línea de texto por el cable. Del otro lado, tu programa tiene que entenderla, aunque a veces llegue cortada o con basura.

—El mundo real es ruidoso, {heroe} —dice la artífice—. Un buen mago no confía en cada mensaje: **lo revisa**, y si se pierde uno, el siguiente lo corrige.

### Objetivos

- Entender un protocolo de texto por puerto serie.
- Parsear mensajes de forma robusta (descartar basura, detectar pérdidas).
- Detectar flancos (cuándo un botón **pasa** de suelto a apretado).
- Conectar con hardware real (o un simulador) usando `pyserial`.

### Antes de empezar

Strings (R01-N03), dataclasses (R02-N01), excepciones (R02-N03).

### Explicación

#### El puerto serie

Un Arduino conectado por USB aparece como un **puerto serie** (`/dev/ttyUSB0` en Linux, `COM3` en Windows): un canal por donde van y vienen bytes. Lo más simple y robusto es mandar **una línea de texto por mensaje**.

#### El protocolo

Cada línea (un *frame*) lleva el **estado completo** del mando:

```
EST ax=-0.80 ay=0.30 b1=1 b2=0 seq=42
```

- `ax`, `ay`: los ejes del joystick, de −1 a 1.
- `b1`, `b2`: los botones (0 o 1).
- `seq`: un número que sube de a uno: si salta de 41 a 43, se perdió un frame.

Como cada frame trae **todo** el estado, si uno se pierde no pasa nada grave: el siguiente corrige.

#### Parsear sin confiar

Por el cable llegan líneas cortadas, ruido y valores imposibles. El parser devuelve `None` ante cualquier cosa rara (en lugar de cortar el programa), y quien lo usa la descarta.

#### Flancos

Para un botón hay dos preguntas distintas: "¿está apretado?" (estado) y "¿**se acaba de** apretar?" (flanco). El flanco se detecta comparando con el frame anterior: `ahora.b1 and not antes.b1`. Es la misma diferencia que eventos y estado del teclado (Senda de la Arena).

#### Con hardware real: pyserial

```python
import serial
with serial.Serial("/dev/ttyUSB0", 115200, timeout=0.5) as puerto:
    linea = puerto.readline().decode(errors="replace")
```

El curso trae `simulador.py`, que crea un puerto serie **virtual** y manda frames como un Arduino: se puede probar todo sin placa.

### Código de ejemplo

```python
"""El protocolo de linea entre el Arduino y la compu (solo stdlib).

Una linea de texto por frame, con el
ESTADO COMPLETO (idempotente: si se pierde una linea, la siguiente corrige).

  EST ax=<-1..1> ay=<-1..1> b1=<0|1> b2=<0|1> seq=<n>\n

ax/ay son los ejes del joystick ya normalizados; b1/b2 los botones.
"""

from dataclasses import dataclass


@dataclass
class Frame:
    ax: float = 0.0
    ay: float = 0.0
    b1: bool = False
    b2: bool = False
    seq: int = 0


def formatear(f: Frame) -> str:
    return (f"EST ax={f.ax:.2f} ay={f.ay:.2f} "
            f"b1={int(f.b1)} b2={int(f.b2)} seq={f.seq}\n")


def parsear(linea: str) -> Frame | None:
    linea = linea.strip()
    if not linea.startswith("EST "):
        return None
    campos = {}
    for par in linea[4:].split():
        if "=" in par:
            k, v = par.split("=", 1)
            campos[k] = v
    try:
        return Frame(
            ax=float(campos.get("ax", 0)),
            ay=float(campos.get("ay", 0)),
            b1=campos.get("b1") == "1",
            b2=campos.get("b2") == "1",
            seq=int(campos.get("seq", 0)),
        )
    except ValueError:
        return None


if __name__ == "__main__":
    f = Frame(ax=-0.8, ay=0.3, b1=True, seq=42)
    linea = formatear(f)
    print("frame  ->", linea.strip())
    print("parse  ->", parsear(linea))
    print("basura ->", parsear("xyz no soy un frame"))
```

### Salida esperada

```
frame  -> EST ax=-0.80 ay=0.30 b1=1 b2=0 seq=42
parse  -> Frame(ax=-0.8, ay=0.3, b1=True, b2=False, seq=42)
basura -> None
```

### ¿Para qué sirve?

Así se conectan las computadoras con el mundo físico: estaciones meteorológicas, sistemas de riego automático, lectores de código de barras, balanzas de un comercio, brazos robóticos, controles de juego hechos en casa. Python es el lenguaje favorito para el "lado de la compu" de estos proyectos, y el Arduino (o una Raspberry Pi) el del hardware.

### Errores habituales

**Goblin: confiar en cada línea**: `float("x")` corta el programa si el mensaje llegó con ruido. Atrapá el `ValueError` y descartá la línea.

**Troll: dos programas usando el mismo puerto**: el monitor serie del IDE de Arduino y tu programa a la vez → `PermissionError` o `Device or resource busy`.

**Ogro: velocidades distintas**: si el Arduino manda a 9600 y Python lee a 115200, llega basura. Tienen que coincidir.

**Ogro: disparar en cada frame con el botón apretado**: usá el flanco, no el estado.

### Misión S02-N04-M1 · Flancos y frames perdidos

```meta
entrega: codigo
monedas: 6
xp: 30
```

#### Consigna

Procesá esta lista de líneas como si llegaran por el cable:

```
EST ax=0.00 ay=0.00 b1=0 b2=0 seq=1
EST ax=0.50 ay=0.00 b1=1 b2=0 seq=2
EST ax=0.60 ay=0.00 b1=1 b2=0 seq=3
ruido@@#
EST ax=0.60 ay=0.10 b1=0 b2=0 seq=5
EST ax=x ay=0.10 b1=1 b2=0 seq=6
EST ax=0.00 ay=0.00 b1=1 b2=1 seq=7
```

1. Descartá (y mostrá) las líneas que no se pueden parsear.
2. Cada vez que `b1` pasa de 0 a 1 (flanco), mostrá `seq N: RUMBLE ms=200` (el comando para que el mando vibre).
3. Contá cuántos frames se perdieron según `seq`.

#### Criterio de aprobación

- El parser devuelve `None` ante líneas inválidas y el programa sigue.
- Detecta el flanco comparando con el frame anterior válido.
- Resultado: RUMBLE en seq 2 y 7, dos líneas descartadas y 2 frames perdidos.

#### Salida esperada

```
seq 2: RUMBLE ms=200
descarto: 'ruido@@#'
descarto: 'EST ax=x ay=0.10 b1=1 b2=0 seq=6'
seq 7: RUMBLE ms=200
frames perdidos: 2
```

#### Solución de referencia

```python
from dataclasses import dataclass


@dataclass
class Frame:
    ax: float = 0.0
    ay: float = 0.0
    b1: bool = False
    b2: bool = False
    seq: int = 0


def parsear(linea):
    linea = linea.strip()
    if not linea.startswith("EST "):
        return None
    campos = dict(par.split("=", 1) for par in linea[4:].split() if "=" in par)
    try:
        return Frame(float(campos.get("ax", 0)), float(campos.get("ay", 0)),
                     campos.get("b1") == "1", campos.get("b2") == "1", int(campos.get("seq", 0)))
    except ValueError:
        return None


LLEGADAS = """EST ax=0.00 ay=0.00 b1=0 b2=0 seq=1
EST ax=0.50 ay=0.00 b1=1 b2=0 seq=2
EST ax=0.60 ay=0.00 b1=1 b2=0 seq=3
ruido@@#
EST ax=0.60 ay=0.10 b1=0 b2=0 seq=5
EST ax=x ay=0.10 b1=1 b2=0 seq=6
EST ax=0.00 ay=0.00 b1=1 b2=1 seq=7""".splitlines()

anterior = Frame()
perdidos = 0
for linea in LLEGADAS:
    frame = parsear(linea)
    if frame is None:
        print(f"descarto: {linea!r}")
        continue
    if frame.seq != anterior.seq + 1:
        perdidos += frame.seq - anterior.seq - 1
    if frame.b1 and not anterior.b1:           # flanco: 0 → 1
        print(f"seq {frame.seq}: RUMBLE ms=200")
    anterior = frame
print("frames perdidos:", perdidos)
```

### Misión S02-N04-M2 · El mando desconectado

```meta
entrega: archivo
monedas: 6
xp: 30
entorno: local
extensiones: py, zip, csv, png
```

#### Consigna

En tu compu, con `simulador.py` y `control.py` del curso (o con un Arduino real): agregale al simulador un modo que **deje de escribir 2 segundos** (como si se desenchufara) y hacé que `control.py` lo detecte por timeout y muestre "mando desconectado" hasta que vuelvan a llegar frames.

#### Criterio de aprobación

- El simulador tiene un modo de corte de 2 s.
- `control.py` detecta la falta de frames con un timeout y avisa.
- Cuando vuelven los frames, se recupera solo.

### Encargo S02-N04-E1 · El mando en la Arena

```meta
entrega: archivo
monedas: 2
xp: 20
entorno: local
extensiones: py, zip, csv, png
```

#### Consigna

Si hiciste la Senda de la Arena: reemplazá el teclado de "Junta las Gemas" por el mando (real o simulado): el joystick mueve al jugador y `b1` hace el dash (con flanco).

#### Criterio de aprobación

- El jugador se mueve con los ejes del mando.
- El dash usa el flanco de `b1`.

### Prueba del sello

#### ¿Por qué conviene que cada frame traiga el estado completo?

Porque si se pierde uno, el siguiente trae todo y corrige: no hay que reconstruir nada.

#### ¿Cómo detectás que un botón se acaba de apretar?

Comparando con el frame anterior: ahora está en 1 y antes estaba en 0 (un flanco).

#### ¿Para qué sirve el número de secuencia?

Para detectar frames perdidos: si salta más de uno, se perdieron los del medio.

### Soluciones (docente)

Material original: `17-Python/42-Robotica-Serial` (`protocolo.py`, `simulador.py`, `control.py`). La misión 1 corre en el navegador; la 2 necesita la compu (usa `pty`, solo Linux y Mac). Es el jefe de la Senda del Reino.
