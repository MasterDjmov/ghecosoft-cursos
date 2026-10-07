import textwrap


def m(**kw):
    for k in ("inicial", "solucion"):
        kw[k] = textwrap.dedent(kw[k]).lstrip("\n")
    return kw


CONSEJO = "La oficina del Consejo del Reino"
TORRE = "La Torre de los Estrategas"
TALLER = "El Taller del Reino"

NODOS = [
    {
        "titulo": "S02-N01 · Datos: lo que cuentan las partidas",
        "misiones": [
            m(id="S02-N01-P1", titulo="Todos los números de una",
              lugar=CONSEJO, personajes="Mia, Gheco, el Consejo del Reino",
              carta="numpy | import numpy as np · np.array([...]) · precios * 1.21 opera sobre TODOS, sin for",
              recompensa="xp 10, oro 10",
              escena="""
                  La oficina del Consejo es una sala redonda con una mesa de cristal donde flotan gráficos. Tres consejeros, de túnicas grises con números bordados en verde, te esperan.
                  —Acá no peleamos: respondemos preguntas —dice el mayor—. Primero, una cuenta simple: subí todos los precios del mercado un 21 %. Todos a la vez.
                  *(La primera vez, Python baja numpy: puede tardar unos segundos.)*
              """,
              sugiere="Un `np.array` guarda muchos números juntos, y las cuentas se hacen **sobre todos de una**: `precios * 1.21`, sin `for`. Con `.round(2)` redondeás y con `.tolist()` lo ves como lista.",
              desafio="Subí todos los precios de una sola vez.",
              inicial='''
                  import numpy as np

                  precios = np.array([100, 250, 40, 1200])
                  nuevos = ___
                  print(nuevos.round(2).tolist())
              ''',
              solucion='''
                  import numpy as np

                  precios = np.array([100, 250, 40, 1200])
                  nuevos = precios * 1.21
                  print(nuevos.round(2).tolist())
              ''',
              solucion_txt="`nuevos = precios * 1.21`.",
              al_superar="Los precios del mercado cambian todos a la vez sobre la mesa de cristal. El consejero mayor asiente. —Sin un solo `for`. Así trabaja el Reino.",
              imagen=["La oficina del Consejo: sala redonda con una mesa de cristal y gráficos holográficos flotando.",
                      "Los tres consejeros (una mujer joven y dos varones de 50 y 70) con túnicas grises bordadas con números verdes.",
                      "Una columna de precios que cambia de golpe, toda a la vez."]),
            m(id="S02-N01-P2", titulo="Lo que dicen dos mil partidas",
              lugar=CONSEJO, personajes="Mia, Gheco, el Consejo del Reino",
              carta="Resumir | arr.mean() promedio · arr.max() · (arr > 30).sum() cuántos cumplen",
              recompensa="xp 10, oro 10",
              escena="—Estas son las gemas que juntó cada jugador en la Arena —dice la consejera más joven—. Decime el promedio, el récord y cuántos pasaron de 30.",
              sugiere="Un array sabe resumirse: `.mean()` (promedio), `.max()`. Y `arr > 30` da `True`/`False` para cada uno; sumarlos cuenta los que cumplen.",
              desafio="Contá cuántos jugadores juntaron más de 30 gemas.",
              inicial='''
                  import numpy as np

                  gemas = np.array([12, 45, 30, 8, 51, 33, 27, 40])
                  print(f"Promedio: {gemas.mean():.1f}")
                  print(f"Récord: {gemas.max()}")
                  print(f"Más de 30: {___}")
              ''',
              solucion='''
                  import numpy as np

                  gemas = np.array([12, 45, 30, 8, 51, 33, 27, 40])
                  print(f"Promedio: {gemas.mean():.1f}")
                  print(f"Récord: {gemas.max()}")
                  print(f"Más de 30: {(gemas > 30).sum()}")
              ''',
              solucion_txt="`(gemas > 30).sum()`.",
              al_superar="Cuatro de ocho pasaron de 30. —La mitad —dice la consejera—. Ni muy fácil, ni muy difícil. Pero eso es en promedio. Veamos por dificultad.",
              imagen=["Un histograma de luz sobre la mesa de cristal, con una línea en 30.",
                      "La consejera más joven señala la línea con una varita de cristal."]),
            m(id="S02-N01-P3", titulo="La planilla",
              lugar=CONSEJO, personajes="Mia, Gheco, el Consejo del Reino",
              carta="pandas | import pandas as pd · df = pd.DataFrame({...}) · df[df[\"col\"] == valor] filtra filas",
              recompensa="xp 15, oro 15",
              escena="Los registros de partidas son una **planilla**: cada partida con su dificultad, sus minutos y sus gemas. —Quedate solo con las difíciles —pide el consejero de 50 años.\n*(La primera vez, Python baja pandas: puede tardar un poco más.)*",
              sugiere="Un `DataFrame` de pandas es una tabla con columnas con nombre. `df[\"dificultad\"] == \"difícil\"` da una columna de `True`/`False`, y `df[esa_condición]` se queda con esas filas.",
              desafio="Filtrá las partidas difíciles.",
              inicial='''
                  import pandas as pd

                  df = pd.DataFrame({
                      "dificultad": ["fácil", "difícil", "normal", "difícil", "fácil", "difícil"],
                      "minutos": [10, 4, 8, 3, 12, 5],
                      "gemas": [40, 9, 25, 6, 52, 12],
                  })
                  dificiles = ___
                  print(f"Partidas difíciles: {len(dificiles)}")
                  print(f"Gemas en difícil: {int(dificiles['gemas'].sum())}")
              ''',
              solucion='''
                  import pandas as pd

                  df = pd.DataFrame({
                      "dificultad": ["fácil", "difícil", "normal", "difícil", "fácil", "difícil"],
                      "minutos": [10, 4, 8, 3, 12, 5],
                      "gemas": [40, 9, 25, 6, 52, 12],
                  })
                  dificiles = df[df["dificultad"] == "difícil"]
                  print(f"Partidas difíciles: {len(dificiles)}")
                  print(f"Gemas en difícil: {int(dificiles['gemas'].sum())}")
              ''',
              solucion_txt="`df[df[\"dificultad\"] == \"difícil\"]`.",
              al_superar="La planilla se encoge y quedan solo las partidas difíciles: tres, cortitas y con pocas gemas. Algo huele mal.",
              imagen=["Una planilla holográfica que se filtra: las filas «difícil» brillan y las demás se apagan."]),
            m(id="S02-N01-P4", titulo="Gemas por minuto",
              lugar=CONSEJO, personajes="Mia, Gheco, el Consejo del Reino",
              carta="Columna nueva | df[\"por_minuto\"] = df[\"gemas\"] / df[\"minutos\"] · la cuenta se hace fila por fila, sola",
              recompensa="xp 10, oro 10",
              escena="—Las partidas difíciles duran menos —dice el consejero mayor—. Comparar gemas totales es injusto. Compará **gemas por minuto**.",
              sugiere="Una columna nueva se crea con una cuenta entre columnas: pandas la hace **fila por fila**, sin `for`. Después, `.mean()` te da el promedio.",
              desafio="Creá la columna de gemas por minuto.",
              inicial='''
                  import pandas as pd

                  df = pd.DataFrame({
                      "dificultad": ["fácil", "difícil", "normal", "difícil", "fácil", "difícil"],
                      "minutos": [10, 4, 8, 3, 12, 5],
                      "gemas": [40, 9, 25, 6, 52, 12],
                  })
                  df["por_minuto"] = ___
                  print(f"Gemas por minuto, en general: {df['por_minuto'].mean():.2f}")
                  print(f"La mejor partida: {df['por_minuto'].max():.2f}")
              ''',
              solucion='''
                  import pandas as pd

                  df = pd.DataFrame({
                      "dificultad": ["fácil", "difícil", "normal", "difícil", "fácil", "difícil"],
                      "minutos": [10, 4, 8, 3, 12, 5],
                      "gemas": [40, 9, 25, 6, 52, 12],
                  })
                  df["por_minuto"] = df["gemas"] / df["minutos"]
                  print(f"Gemas por minuto, en general: {df['por_minuto'].mean():.2f}")
                  print(f"La mejor partida: {df['por_minuto'].max():.2f}")
              ''',
              solucion_txt="`df[\"gemas\"] / df[\"minutos\"]`.",
              al_superar="Una columna nueva aparece en la planilla, calculada sola. Ahora sí se puede comparar.",
              imagen=["Una columna nueva que se llena sola en la planilla holográfica, fila por fila."]),
            m(id="S02-N01-P5", titulo="¿Es injusto el difícil?",
              lugar=CONSEJO, personajes="Mia, Gheco, el Consejo del Reino",
              carta="groupby | df.groupby(\"dificultad\")[\"col\"].mean() · un resumen por grupo · pregunta → evidencia → conclusión",
              recompensa="xp 20, oro 20",
              item="Sello del Consejo",
              escena="—La pregunta de verdad —dice el consejero mayor—: ¿el difícil es injusto? Comparalo con los demás, grupo por grupo.",
              sugiere="`df.groupby(\"dificultad\")[\"por_minuto\"].mean()` arma un grupo por cada dificultad y saca el promedio de cada uno. Con `.items()` lo recorrés como un diccionario.",
              desafio="Agrupá por dificultad.",
              inicial='''
                  import pandas as pd

                  df = pd.DataFrame({
                      "dificultad": ["fácil", "difícil", "normal", "difícil", "fácil", "difícil"],
                      "minutos": [10, 4, 8, 3, 12, 5],
                      "gemas": [40, 9, 25, 6, 52, 12],
                  })
                  df["por_minuto"] = df["gemas"] / df["minutos"]
                  resumen = df.___("dificultad")["por_minuto"].mean()
                  for nivel, valor in resumen.items():
                      print(f"{nivel}: {valor:.2f} gemas por minuto")
              ''',
              solucion='''
                  import pandas as pd

                  df = pd.DataFrame({
                      "dificultad": ["fácil", "difícil", "normal", "difícil", "fácil", "difícil"],
                      "minutos": [10, 4, 8, 3, 12, 5],
                      "gemas": [40, 9, 25, 6, 52, 12],
                  })
                  df["por_minuto"] = df["gemas"] / df["minutos"]
                  resumen = df.groupby("dificultad")["por_minuto"].mean()
                  for nivel, valor in resumen.items():
                      print(f"{nivel}: {valor:.2f} gemas por minuto")
              ''',
              solucion_txt="`df.groupby(\"dificultad\")`.",
              al_superar="""
                  En difícil se junta la mitad de gemas por minuto. —Ahí está: es injusto —dice el consejero mayor—. Bajemos el daño de los enemigos.
                  Los tres consejeros apoyan la mano sobre la mesa y te dan un **sello de cristal**: el Sello del Consejo. —No opinaste. Mostraste los datos.
              """,
              imagen=["Tres barras de luz sobre la mesa de cristal: fácil y normal altas, difícil a la mitad.",
                      "Los tres consejeros apoyan la mano sobre la mesa y le entregan a Mia un sello de cristal con números verdes."]),
        ],
    },
    {
        "titulo": "S02-N02 · IA: encontrar el camino (A*)",
        "misiones": [
            m(id="S02-N02-P1", titulo="Las casillas vecinas",
              lugar=TORRE, personajes="Mia, Gheco, la consejera del Reino",
              carta="Vecinos en una grilla | (f-1, c) (f+1, c) (f, c-1) (f, c+1) · dentro del mapa y sin pared (\"#\")",
              recompensa="xp 10, oro 10",
              escena="""
                  En la Torre de los Estrategas, un enemigo de práctica tiene que llegar hasta vos por un laberinto. La consejera más joven del Consejo entrena a los estrategas.
                  —Antes de buscar un camino, la criatura tiene que saber **a dónde puede dar un paso** desde donde está.
              """,
              sugiere="El laberinto es una lista de textos: `\"#\"` es pared y `\".\"` es piso. Desde `(fila, col)` se puede ir arriba, abajo, izquierda y derecha, si queda **dentro** del mapa y **no** es pared.",
              desafio="Completá la condición: dentro del mapa y sin pared.",
              inicial='''
                  mapa = [
                      "..#",
                      ".#.",
                      "...",
                  ]

                  def vecinos(f, c):
                      res = []
                      for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                          nf, nc = f + df, c + dc
                          if ___:
                              res.append((nf, nc))
                      return res

                  print(vecinos(0, 0))
                  print(vecinos(2, 1))
              ''',
              solucion='''
                  mapa = [
                      "..#",
                      ".#.",
                      "...",
                  ]

                  def vecinos(f, c):
                      res = []
                      for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                          nf, nc = f + df, c + dc
                          if 0 <= nf < len(mapa) and 0 <= nc < len(mapa[0]) and mapa[nf][nc] != "#":
                              res.append((nf, nc))
                      return res

                  print(vecinos(0, 0))
                  print(vecinos(2, 1))
              ''',
              solucion_txt="`0 <= nf < len(mapa) and 0 <= nc < len(mapa[0]) and mapa[nf][nc] != \"#\"`.",
              al_superar="El enemigo de práctica deja de chocarse contra las paredes: ya sabe dónde puede pisar.",
              imagen=["La Torre de los Estrategas: un laberinto de luz sobre el piso, con muros de piedra.",
                      "Un enemigo de práctica con flechas verdes hacia las casillas libres.",
                      "La consejera más joven del Consejo (túnica gris con números verdes) observa con una varita de cristal."]),
            m(id="S02-N02-P2", titulo="Explorar por capas",
              lugar=TORRE, personajes="Mia, Gheco, la consejera del Reino",
              carta="Búsqueda por capas (BFS) | una cola (deque) · se visita primero lo más cerca · distancia = pasos",
              recompensa="xp 15, oro 15",
              escena="—La forma más simple de buscar es **por capas** —dice la consejera—: primero todo lo que está a un paso, después a dos, y así.",
              sugiere="Con una **cola** (`deque`, R03-N06): sacás la primera casilla, y agregás al final sus vecinos que todavía no tienen distancia. Así se recorre por capas, y la distancia a cada casilla es la mínima.",
              desafio="Anotá la distancia de cada vecino nuevo.",
              inicial='''
                  from collections import deque

                  mapa = ["....", ".##.", "...."]

                  def vecinos(f, c):
                      for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                          nf, nc = f + df, c + dc
                          if 0 <= nf < len(mapa) and 0 <= nc < len(mapa[0]) and mapa[nf][nc] != "#":
                              yield nf, nc

                  distancia = {(0, 0): 0}
                  cola = deque([(0, 0)])
                  while cola:
                      actual = cola.popleft()
                      for v in vecinos(*actual):
                          if v not in distancia:
                              distancia[v] = ___
                              cola.append(v)
                  print(f"Hasta la esquina opuesta: {distancia[(2, 3)]} pasos")
              ''',
              solucion='''
                  from collections import deque

                  mapa = ["....", ".##.", "...."]

                  def vecinos(f, c):
                      for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                          nf, nc = f + df, c + dc
                          if 0 <= nf < len(mapa) and 0 <= nc < len(mapa[0]) and mapa[nf][nc] != "#":
                              yield nf, nc

                  distancia = {(0, 0): 0}
                  cola = deque([(0, 0)])
                  while cola:
                      actual = cola.popleft()
                      for v in vecinos(*actual):
                          if v not in distancia:
                              distancia[v] = distancia[actual] + 1
                              cola.append(v)
                  print(f"Hasta la esquina opuesta: {distancia[(2, 3)]} pasos")
              ''',
              solucion_txt="`distancia[actual] + 1`.",
              al_superar="Una onda de luz se expande por el laberinto, capa por capa, hasta tocar la esquina opuesta: cinco pasos.",
              imagen=["Ondas concéntricas de luz que se expanden por el laberinto desde una esquina, numeradas 1, 2, 3…"]),
            m(id="S02-N02-P3", titulo="Lo más prometedor primero",
              lugar=TORRE, personajes="Mia, Gheco, la consejera del Reino",
              carta="heapq | heapq.heappush(cola, (prioridad, dato)) · heappop saca SIEMPRE el de menor prioridad",
              recompensa="xp 10, oro 10",
              escena="—Por capas funciona, pero explora todo —dice la consejera—. A* mira primero lo más **prometedor**. Para eso necesita una cola que siempre te dé el mejor.",
              sugiere="`heapq` arma una **cola de prioridad**: guardás tuplas `(prioridad, dato)` con `heappush`, y `heappop` saca siempre la de **menor** prioridad, en el orden que sea que entraron.",
              desafio="Sacá las casillas de la cola en orden de prioridad.",
              inicial='''
                  import heapq

                  cola = []
                  for prioridad, casilla in [(7, "puerta"), (2, "pasillo"), (5, "escalera"), (1, "esquina")]:
                      heapq.heappush(cola, (prioridad, casilla))
                  while cola:
                      prioridad, casilla = ___
                      print(f"{prioridad}: {casilla}")
              ''',
              solucion='''
                  import heapq

                  cola = []
                  for prioridad, casilla in [(7, "puerta"), (2, "pasillo"), (5, "escalera"), (1, "esquina")]:
                      heapq.heappush(cola, (prioridad, casilla))
                  while cola:
                      prioridad, casilla = heapq.heappop(cola)
                      print(f"{prioridad}: {casilla}")
              ''',
              solucion_txt="`heapq.heappop(cola)`.",
              al_superar="Las casillas salen ordenadas, de la más prometedora a la menos. La consejera sonríe. —Eso es la mitad de A*.",
              imagen=["Una pila de fichas de luz con números que se ordena sola, de menor a mayor."]),
            m(id="S02-N02-P4", titulo="El camino entero",
              lugar=TORRE, personajes="Mia, Gheco, la consejera del Reino",
              carta="A* | prioridad = pasos hechos + distancia estimada · Manhattan: |f1 - f2| + |c1 - c2|",
              recompensa="xp 20, oro 20",
              escena="—La otra mitad —dice la consejera— es **estimar** cuánto falta. En una grilla, la distancia Manhattan: lo que falta en filas más lo que falta en columnas.",
              sugiere="A* saca de la cola la casilla con menor `pasos + estimado`. La estimación **Manhattan** entre `(f1, c1)` y `(f2, c2)` es `abs(f1 - f2) + abs(c1 - c2)`.",
              desafio="Escribí la estimación Manhattan.",
              inicial='''
                  import heapq

                  mapa = ["....#", ".##.#", "....."]
                  inicio, meta = (0, 0), (2, 4)

                  def estimado(a, b):
                      return ___

                  def vecinos(f, c):
                      for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                          nf, nc = f + df, c + dc
                          if 0 <= nf < len(mapa) and 0 <= nc < len(mapa[0]) and mapa[nf][nc] != "#":
                              yield nf, nc

                  pasos = {inicio: 0}
                  cola = [(estimado(inicio, meta), inicio)]
                  exploradas = 0
                  while cola:
                      _, actual = heapq.heappop(cola)
                      exploradas += 1
                      if actual == meta:
                          break
                      for v in vecinos(*actual):
                          if v not in pasos or pasos[actual] + 1 < pasos[v]:
                              pasos[v] = pasos[actual] + 1
                              heapq.heappush(cola, (pasos[v] + estimado(v, meta), v))
                  print(f"Llega en {pasos[meta]} pasos, explorando {exploradas} casillas")
              ''',
              solucion='''
                  import heapq

                  mapa = ["....#", ".##.#", "....."]
                  inicio, meta = (0, 0), (2, 4)

                  def estimado(a, b):
                      return abs(a[0] - b[0]) + abs(a[1] - b[1])

                  def vecinos(f, c):
                      for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                          nf, nc = f + df, c + dc
                          if 0 <= nf < len(mapa) and 0 <= nc < len(mapa[0]) and mapa[nf][nc] != "#":
                              yield nf, nc

                  pasos = {inicio: 0}
                  cola = [(estimado(inicio, meta), inicio)]
                  exploradas = 0
                  while cola:
                      _, actual = heapq.heappop(cola)
                      exploradas += 1
                      if actual == meta:
                          break
                      for v in vecinos(*actual):
                          if v not in pasos or pasos[actual] + 1 < pasos[v]:
                              pasos[v] = pasos[actual] + 1
                              heapq.heappush(cola, (pasos[v] + estimado(v, meta), v))
                  print(f"Llega en {pasos[meta]} pasos, explorando {exploradas} casillas")
              ''',
              solucion_txt="`abs(a[0] - b[0]) + abs(a[1] - b[1])`.",
              al_superar="""
                  El enemigo de práctica rodea los muros sin dudar y llega hasta vos por el camino más corto.
                  —Una buena criatura no camina hacia su presa: **busca el camino** —repite la consejera—. Arriba hay dos rivales que hacen algo más difícil todavía.
              """,
              imagen=["Un camino dorado que rodea los muros del laberinto hasta Mia; el enemigo de práctica lo recorre.",
                      "La consejera señala una escalera que sube al último salón."]),
        ],
    },
    {
        "titulo": "S02-N03 · IA: rivales que piensan",
        "misiones": [
            m(id="S02-N03-P1", titulo="¿Quién ganó?",
              lugar=TORRE, personajes="Mia, Gheco, la consejera del Reino",
              carta="Tres en raya | 8 líneas: 3 filas, 3 columnas, 2 diagonales · gana quien tiene las 3 de una línea",
              recompensa="xp 10, oro 10",
              escena="En el último salón, un rival juega al tres en raya y **no pierde nunca**. —Antes de pensar jugadas —dice la consejera—, tu programa tiene que saber cuándo alguien ganó.",
              sugiere="El tablero es una lista de 9 casillas (`\"X\"`, `\"O\"` o `\" \"`). Hay 8 líneas ganadoras. Gana quien ocupa las tres casillas de una línea (y no son espacios).",
              desafio="Completá la condición de una línea ganadora.",
              inicial='''
                  LINEAS = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

                  def ganador(t):
                      for a, b, c in LINEAS:
                          if ___:
                              return t[a]
                      return None

                  print(ganador(["X", "O", " ", "O", "X", " ", " ", " ", "X"]))
                  print(ganador(["X", "O", "X", " ", "O", " ", " ", "O", " "]))
                  print(ganador(["X", "O", "X", " ", " ", " ", " ", " ", " "]))
              ''',
              solucion='''
                  LINEAS = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

                  def ganador(t):
                      for a, b, c in LINEAS:
                          if t[a] != " " and t[a] == t[b] == t[c]:
                              return t[a]
                      return None

                  print(ganador(["X", "O", " ", "O", "X", " ", " ", " ", "X"]))
                  print(ganador(["X", "O", "X", " ", "O", " ", " ", "O", " "]))
                  print(ganador(["X", "O", "X", " ", " ", " ", " ", " ", " "]))
              ''',
              solucion_txt="`t[a] != \" \" and t[a] == t[b] == t[c]`.",
              al_superar="El tablero de cristal se ilumina en la diagonal ganadora. El rival invicto te mira por primera vez.",
              imagen=["Un tablero de tres en raya de cristal flotando, con la diagonal ganadora encendida.",
                      "Un rival autómata de bronce sentado del otro lado, mirando a Mia."]),
            m(id="S02-N03-P2", titulo="Pensar todas las jugadas",
              lugar=TORRE, personajes="Mia, Gheco, la consejera del Reino",
              carta="Minimax | yo elijo el MÁXIMO, el rival el MÍNIMO · se resuelve de abajo hacia arriba (recursión)",
              recompensa="xp 15, oro 15",
              escena="—El rival invicto **piensa todas las jugadas** —dice la consejera—. Elige lo mejor para él, sabiendo que vos vas a elegir lo peor para él. Probalo en un árbol chiquito.",
              sugiere="En un árbol de jugadas, las hojas son puntajes. En tu turno elegís el **máximo** de lo que podés lograr; en el turno del rival, él elige el **mínimo**. La función se llama a sí misma (R01-N09) alternando el turno.",
              desafio="En el turno del rival, devolvé el mínimo.",
              inicial='''
                  def minimax(nodo, mi_turno):
                      if isinstance(nodo, int):
                          return nodo
                      valores = [minimax(hijo, not mi_turno) for hijo in nodo]
                      return max(valores) if mi_turno else ___

                  arbol = [[3, 12], [8, 2], [14, 5]]
                  print(f"Lo mejor que puedo asegurar: {minimax(arbol, True)}")
              ''',
              solucion='''
                  def minimax(nodo, mi_turno):
                      if isinstance(nodo, int):
                          return nodo
                      valores = [minimax(hijo, not mi_turno) for hijo in nodo]
                      return max(valores) if mi_turno else min(valores)

                  arbol = [[3, 12], [8, 2], [14, 5]]
                  print(f"Lo mejor que puedo asegurar: {minimax(arbol, True)}")
              ''',
              solucion_txt="`min(valores)`.",
              al_superar="Cinco: aunque el 14 tienta, el rival nunca te dejaría llegar. Ahora entendés por qué el invicto no pierde: nunca se ilusiona.",
              imagen=["Un árbol de jugadas de luz: las ramas se iluminan de abajo hacia arriba hasta la raíz, que marca 5.",
                      "El 14 brilla tentador en una hoja, pero tachado."]),
            m(id="S02-N03-P3", titulo="Aprender probando",
              lugar=TORRE, personajes="Mia, Gheco, la consejera del Reino",
              carta="Q-learning | q = q + alfa * (premio + gamma * mejor_siguiente - q) · se corrige un poco cada intento",
              recompensa="xp 15, oro 15",
              escena="El otro rival empezó cayéndose en todos los pozos de un pasillo. —No piensa: **aprende** —dice la consejera—. Cada vez que prueba algo, corrige un poquito lo que cree que vale.",
              sugiere="En **Q-learning**, cada acción tiene un valor `q`. Después de probarla, se corre un poco (`alfa`) hacia lo que de verdad pasó: el premio más lo mejor que espera después (`gamma` lo descuenta).",
              desafio="Escribí la corrección de Q-learning.",
              inicial='''
                  alfa, gamma = 0.5, 0.9
                  q = 0.0
                  for intento, (premio, mejor_siguiente) in enumerate([(-10, 0), (-10, 0), (1, 5), (1, 5)], start=1):
                      q = ___
                      print(f"Intento {intento}: q = {q:.2f}")
              ''',
              solucion='''
                  alfa, gamma = 0.5, 0.9
                  q = 0.0
                  for intento, (premio, mejor_siguiente) in enumerate([(-10, 0), (-10, 0), (1, 5), (1, 5)], start=1):
                      q = q + alfa * (premio + gamma * mejor_siguiente - q)
                      print(f"Intento {intento}: q = {q:.2f}")
              ''',
              solucion_txt="`q + alfa * (premio + gamma * mejor_siguiente - q)`.",
              al_superar="Dos caídas al pozo y el valor se hunde; dos pasos buenos y empieza a subir. El rival aprende como vos: equivocándose.",
              imagen=["Un pasillo con tres pozos; el rival autómata cae, se levanta y prueba otro camino.",
                      "Un número de luz sobre su cabeza que baja y después sube."]),
            m(id="S02-N03-P4", titulo="Lo que aprendió",
              lugar=TORRE, personajes="Mia, Gheco, la consejera del Reino",
              carta="Elegir con lo aprendido | mejor = max(acciones, key=lambda a: q[(estado, a)]) · la acción de mayor valor",
              recompensa="xp 15, oro 20",
              escena="Después de mil intentos, el rival cruza el pasillo sin dudar. —Ya no prueba —dice la consejera—: en cada casilla elige la acción que **más vale** según lo que aprendió.",
              sugiere="Con la tabla `q[(estado, accion)]` aprendida, en cada casilla se elige la acción de mayor valor con `max(..., key=...)` (R03-N02).",
              desafio="Elegí la mejor acción en cada casilla.",
              inicial='''
                  q = {
                      (0, "saltar"): 2.0, (0, "avanzar"): 5.1,
                      (1, "saltar"): 6.3, (1, "avanzar"): -9.5,
                      (2, "saltar"): 1.2, (2, "avanzar"): 8.0,
                  }
                  for casilla in range(3):
                      mejor = max(["saltar", "avanzar"], key=___)
                      print(f"Casilla {casilla}: {mejor}")
              ''',
              solucion='''
                  q = {
                      (0, "saltar"): 2.0, (0, "avanzar"): 5.1,
                      (1, "saltar"): 6.3, (1, "avanzar"): -9.5,
                      (2, "saltar"): 1.2, (2, "avanzar"): 8.0,
                  }
                  for casilla in range(3):
                      mejor = max(["saltar", "avanzar"], key=lambda a: q[(casilla, a)])
                      print(f"Casilla {casilla}: {mejor}")
              ''',
              solucion_txt="`lambda a: q[(casilla, a)]`.",
              al_superar="Avanzar, saltar el pozo, avanzar: el rival cruza el pasillo de una. La consejera aplaude. —Pensar o aprender: ahora conocés las dos familias.",
              imagen=["El rival autómata cruzando el pasillo de un salto perfecto sobre el pozo del medio.",
                      "La consejera aplaudiendo; Gheco imita el salto."]),
        ],
    },
    {
        "titulo": "S02-N04 · Robótica: el mando de Arduino",
        "misiones": [
            m(id="S02-N04-P1", titulo="Leer un frame",
              lugar=TALLER, personajes="Mia, Gheco, la maestra del Gremio de Artífices",
              carta="Protocolo de texto | \"EST ax=-0.80 b1=1 seq=42\" · split() en palabras · split(\"=\") en clave y valor",
              recompensa="xp 10, oro 10",
              escena="""
                  En el Taller del Reino, un Arduino con un joystick manda una línea de texto por el cable a cada instante. La maestra del Gremio, que bajó de la Torre a ayudar, te la muestra.
                  —Cada línea trae el estado **completo** del mando. Primero, aprendé a leerla.
              """,
              sugiere="`linea.split()` separa en palabras. La primera es el tipo (`EST`); las demás son `clave=valor`, que se separan con `split(\"=\")`.",
              desafio="Separá cada par en clave y valor.",
              inicial='''
                  linea = "EST ax=-0.80 ay=0.30 b1=1 b2=0 seq=42"
                  tipo, *pares = linea.split()
                  datos = {}
                  for par in pares:
                      clave, valor = ___
                      datos[clave] = float(valor)
                  print(tipo, datos["ax"], datos["b1"], int(datos["seq"]))
              ''',
              solucion='''
                  linea = "EST ax=-0.80 ay=0.30 b1=1 b2=0 seq=42"
                  tipo, *pares = linea.split()
                  datos = {}
                  for par in pares:
                      clave, valor = par.split("=")
                      datos[clave] = float(valor)
                  print(tipo, datos["ax"], datos["b1"], int(datos["seq"]))
              ''',
              solucion_txt="`par.split(\"=\")`.",
              al_superar="Por primera vez, la pantalla del Taller muestra lo que hace el joystick: un poco a la izquierda, botón apretado.",
              imagen=["El Taller del Reino: una mesa de trabajo con un Arduino, un joystick y dos botones conectados por un cable.",
                      "La maestra del Gremio de Artífices (pelo blanco corto, gafas de varios lentes en la frente, delantal de cuero) señala una línea de texto que corre por el cable.",
                      "Mia con el pergamino; Gheco mira el cable con curiosidad."]),
            m(id="S02-N04-P2", titulo="No confiar en el cable",
              lugar=TALLER, personajes="Mia, Gheco, la maestra del Gremio de Artífices",
              criatura="slime",
              carta="Parsear sin confiar | ante cualquier cosa rara, return None · quien llama descarta y sigue",
              recompensa="xp 15, oro 15",
              escena="Por el cable empiezan a llegar líneas cortadas y basura. Tu programa se cae con la primera, y de la línea rota gotea un **slime**. —El mundo real es ruidoso —dice la maestra—. Lo que se prueba, aguanta.",
              sugiere="El parser no tiene que cortar el programa: si algo sale mal (`ValueError`, una clave que falta), devuelve `None`. Quien lo usa descarta esa línea y sigue con la próxima.",
              desafio="Atrapá los errores y devolvé `None`.",
              inicial='''
                  def leer(linea):
                      try:
                          tipo, *pares = linea.split()
                          datos = {k: float(v) for k, v in (p.split("=") for p in pares)}
                          return datos if tipo == "EST" and "seq" in datos else None
                      except ___:
                          return None

                  for linea in ["EST ax=0.5 seq=1", "EST ax=0.", "ruido!!", "EST ax=abc seq=3", "EST ax=-1 seq=4"]:
                      print(leer(linea))
              ''',
              solucion='''
                  def leer(linea):
                      try:
                          tipo, *pares = linea.split()
                          datos = {k: float(v) for k, v in (p.split("=") for p in pares)}
                          return datos if tipo == "EST" and "seq" in datos else None
                      except ValueError:
                          return None

                  for linea in ["EST ax=0.5 seq=1", "EST ax=0.", "ruido!!", "EST ax=abc seq=3", "EST ax=-1 seq=4"]:
                      print(leer(linea))
              ''',
              solucion_txt="`except ValueError:`.",
              al_superar="Las líneas rotas se descartan solas y el slime se seca sobre la mesa. El mando sigue funcionando entre el ruido.",
              imagen=["Líneas de texto rotas que caen del cable y se desarman en el aire; un slime que se seca sobre la mesa.",
                      "La maestra del Gremio asiente con los brazos cruzados."]),
            m(id="S02-N04-P3", titulo="Los frames perdidos",
              lugar=TALLER, personajes="Mia, Gheco, la maestra del Gremio de Artífices",
              carta="Número de secuencia | si seq salta de 41 a 44, se perdieron 2 · perdidos += seq - anterior - 1",
              recompensa="xp 10, oro 10",
              escena="—Cada frame trae un número que sube de a uno —dice la maestra—. Si salta, se perdió alguno en el camino. Contá cuántos.",
              sugiere="Entre dos números de secuencia seguidos, los perdidos son `seq - anterior - 1`. Si llegó el siguiente justo, da 0.",
              desafio="Sumá los frames perdidos.",
              inicial='''
                  secuencias = [40, 41, 44, 45, 46, 50]
                  perdidos = 0
                  anterior = secuencias[0]
                  for seq in secuencias[1:]:
                      perdidos += ___
                      anterior = seq
                  print(f"Llegaron {len(secuencias)} y se perdieron {perdidos}")
              ''',
              solucion='''
                  secuencias = [40, 41, 44, 45, 46, 50]
                  perdidos = 0
                  anterior = secuencias[0]
                  for seq in secuencias[1:]:
                      perdidos += seq - anterior - 1
                      anterior = seq
                  print(f"Llegaron {len(secuencias)} y se perdieron {perdidos}")
              ''',
              solucion_txt="`seq - anterior - 1`.",
              al_superar="Se perdieron cinco frames y el mando ni se enteró: como cada uno trae el estado completo, el siguiente lo corrigió.",
              imagen=["Una tira de frames numerados con huecos en 42, 43, 47, 48 y 49, marcados en rojo."]),
            m(id="S02-N04-P4", titulo="Apretar no es mantener",
              lugar=TALLER, personajes="Mia, Gheco, la maestra del Gremio de Artífices",
              carta="Flanco | se acaba de apretar: ahora and not antes · se soltó: antes and not ahora · como el teclado de la Arena",
              recompensa="xp 10, oro 10",
              escena="—Con el botón pasa lo mismo que con el teclado de la Arena —dice la maestra—. Disparar es cuando se **acaba de** apretar, no mientras está apretado.",
              sugiere="El **flanco** compara con el frame anterior: `ahora and not antes` es «se acaba de apretar», y `antes and not ahora`, «se acaba de soltar».",
              desafio="Detectá cuándo se soltó el botón.",
              inicial='''
                  b1 = [0, 1, 1, 0, 0, 1, 0]
                  antes = 0
                  for frame, ahora in enumerate(b1):
                      if ahora and not antes:
                          print(f"Frame {frame}: ¡disparo!")
                      if ___:
                          print(f"Frame {frame}: soltó el botón")
                      antes = ahora
              ''',
              solucion='''
                  b1 = [0, 1, 1, 0, 0, 1, 0]
                  antes = 0
                  for frame, ahora in enumerate(b1):
                      if ahora and not antes:
                          print(f"Frame {frame}: ¡disparo!")
                      if antes and not ahora:
                          print(f"Frame {frame}: soltó el botón")
                      antes = ahora
              ''',
              solucion_txt="`antes and not ahora`.",
              al_superar="Un disparo por apretón, ni uno más. En la pantalla del Taller, la nave de práctica dispara justo cuando querés.",
              imagen=["Una pantalla en el Taller con una nave de práctica que dispara un único rayo.",
                      "El dedo de Mia sobre el botón del mando."]),
            m(id="S02-N04-P5", titulo="La zona muerta",
              lugar=TALLER, personajes="Mia, Gheco, la maestra del Gremio de Artífices",
              carta="Zona muerta | if abs(x) < 0.1: x = 0 · el joystick suelto nunca marca 0 justo",
              recompensa="xp 20, oro 25",
              item="Mando del Reino",
              escena="Soltás el joystick y el personaje igual se mueve, muy despacito. —Un joystick suelto nunca marca **cero justo** —dice la maestra—. Ponele una zona muerta.",
              sugiere="La **zona muerta** ignora los valores muy chicos: si el valor absoluto es menor que un margen (por ejemplo 0.1), se toma como 0.",
              desafio="Aplicá la zona muerta a cada lectura.",
              inicial='''
                  def limpiar(x, margen=0.1):
                      ___

                  for lectura in [0.03, -0.08, 0.5, -0.92, 0.1]:
                      print(f"{lectura:+.2f} → {limpiar(lectura):+.2f}")
              ''',
              solucion='''
                  def limpiar(x, margen=0.1):
                      return 0.0 if abs(x) < margen else x

                  for lectura in [0.03, -0.08, 0.5, -0.92, 0.1]:
                      print(f"{lectura:+.2f} → {limpiar(lectura):+.2f}")
              ''',
              solucion_txt="`return 0.0 if abs(x) < margen else x`.",
              al_superar="""
                  Soltás el joystick y el personaje queda quieto. Lo movés y responde al instante. La maestra del Gremio desenchufa el mando y te lo da: el **Mando del Reino**.
                  —Lo probaste con todo lo que el cable pudo tirarte. Aguanta.
                  Gheco te mira desde el hombro. Desde el Taller se ve, a lo lejos, el humo de **las Forjas**.
              """,
              imagen=["La maestra del Gremio entrega a Mia un mando de Arduino con joystick, terminado y prolijo.",
                      "En la pantalla, el personaje quieto en el centro.",
                      "Por la ventana del Taller, a lo lejos, el humo de unas forjas."]),
        ],
    },
]
